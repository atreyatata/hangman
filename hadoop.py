#!/usr/bin/env python3
r"""
Lightweight, mock hadoop.

By Andrew DeOrio <awdeorio@umich.edu>
January, 2019

Supports a subset of the hadoop command line interface, for example:
$ hadoop \
  jar $HADOOP_DIR/hadoop-streaming-2.7.2.jar \
  -D mapreduce.job.maps=4 \
  -D mapreduce.job.reduces=1 \
  -input $HADOOP_DIR/sampleInput \
  -output $HADOOP_DIR/output \
  -mapper $EXEC_DIR/map.py \
  -reducer $EXEC_DIR/reduce.py


./hadoop.py \
  jar hadoop-streaming-2.7.2.jar \
  -D mapreduce.job.maps=1 \
  -D mapreduce.job.reduces=1 \
  -input input \
  -output output \
  -mapper ./map.py \
  -reducer ./reduce.py

"""

import argparse
import collections
import os
import shutil
import sys
import glob
import sh


def main():
    """Obtain command line arguments and run the hadoop job."""
    parser = argparse.ArgumentParser(
        description='Lightweight Hadoop work-alike.'
    )

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-D', dest='properties',
                               action='append', required=True)
    required_args.add_argument('-input', dest='input', required=True)
    required_args.add_argument('-output', dest='output', required=True)
    required_args.add_argument('-mapper', dest='mapper', required=True)
    required_args.add_argument('-reducer', dest='reducer', required=True)

    args, dummy = parser.parse_known_args()
    num_map = None
    num_reduce = None

    if not args.properties:
        print("Error: add -D mapreduce.job.maps=X -D mapreduce.job.reduces=Y")
        sys.exit(1)

    for prop in args.properties:
        if prop.startswith("mapreduce.job.maps="):
            num_map = prop.split('=')[1]
        elif prop.startswith("mapreduce.job.reduces="):
            num_reduce = prop.split('=')[1]
        else:
            print("Error with option -D {}".format(prop))
            sys.exit(1)
    try:
        num_map = int(num_map)
        num_reduce = int(num_reduce)
    except ValueError:
        print("Invalid mapper or reducer values.")
        sys.exit(1)

    hadoop(
        input_dir=args.input,
        output_dir=args.output,
        map_exe=args.mapper,
        num_map=num_map,
        reduce_exe=args.reducer,
        num_reduce=num_reduce,
    )


def hadoop(input_dir, output_dir, map_exe, num_map, reduce_exe,
           num_reduce, enforce_keyspace=False):
    # pylint: disable-msg=too-many-arguments
    """End Point to run a hadoop job."""
    # Set path of the tmp directories

    # Create tmp directories, starting with {ouput_dir}/hadooptmp
    tmpdir = os.path.join(output_dir, "hadooptmp")
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    os.makedirs(tmpdir)
    map_input_dir = os.path.join(tmpdir, 'mapper-input')
    map_output_dir = os.path.join(tmpdir, 'mapper-output')
    group_output_dir = os.path.join(tmpdir, 'grouper-output')
    reduce_output_dir = os.path.join(tmpdir, 'reducer-output')
    os.makedirs(map_input_dir)
    os.makedirs(map_output_dir)
    os.makedirs(group_output_dir)
    os.makedirs(reduce_output_dir)

    # Copy and rename input files: part-00000, part-00001, etc.  Verify that
    # the number of input files is equal to the number of mappers.
    prepare_input_files(input_dir, map_input_dir, num_map)

    # Run the mapping stage
    print("Starting map stage")
    map_stage(
        exe=map_exe,
        input_dir=map_input_dir,
        output_dir=map_output_dir,
        num_map=num_map,
        enforce_keyspace=enforce_keyspace,
    )

    # Run the grouping stage
    print("Starting group stage")
    group_stage(
        input_dir=map_output_dir,
        output_dir=group_output_dir,
        num_workers=num_reduce,
    )

    # Run the reducing stage
    print("Starting reduce stage")
    reduce_stage(
        exe=reduce_exe,
        input_dir=group_output_dir,
        output_dir=reduce_output_dir,
        num_reduce=num_reduce,
        enforce_keyspace=enforce_keyspace,
    )

    # Move files from temporary output directory to user-specified output dir
    for filename in glob.glob(os.path.join(reduce_output_dir, "*")):
        shutil.copy(filename, output_dir)

    # Remind user where to find output
    print("Output directory: {}".format(output_dir))


def prepare_input_files(input_dir, output_dir, num_map):
    """Verify and copy input files.  Rename to part-00000, part-00001, etc.

    The number of input files must equal num_map.
    """
    # Count input files
    filenames = []
    for filename in glob.glob(os.path.join(input_dir, '*')):
        if not os.path.isdir(filename):
            filenames.append(filename)

    # Verify number of input files
    print(len(filenames))
    assert len(filenames) == num_map, "Num mappers != num_input_files."

    # Copy and rename input files
    for i, filename in enumerate(filenames):
        shutil.copyfile(filename, os.path.join(output_dir, part_filename(i)))


def check_num_keys(filename):
    """Check num keys."""
    key_instances = 0
    with open(filename) as file:
        for _ in file:
            key_instances += 1

    # implies we are dumping everything into one key
    if key_instances == 1:
        print('Should not carry data forward via a single key')
        sys.exit(1)


def part_filename(num):
    """Return a filename conforming to the Hadoop convention.

    EXAMPLE:
    part_filename(3) = "part-00003"
    """
    return 'part-' + str(num).zfill(5)


def map_stage(exe, input_dir, output_dir, num_map, enforce_keyspace):
    """Execute mappers."""
    for i in range(num_map):
        input_filename = os.path.join(input_dir, part_filename(i))
        output_filename = os.path.join(output_dir, part_filename(i))
        map_command = sh.Command(exe)
        print("+ {} < {} > {}".format(exe, input_filename, output_filename))
        with open(input_filename, 'r') as input_file:
            map_command(_in=input_file, _out=output_filename)

        if enforce_keyspace:
            check_num_keys(output_filename)


def group_stage(input_dir, output_dir, num_workers):
    """Run group stage."""
    # Concatenate and sort input files to sorted.out
    sorted_output_filename = os.path.join(output_dir, 'sorted.out')
    print("+ cat {}/* | sort > {}".format(input_dir, sorted_output_filename))

    # Update locale to use traditional sort, TRAVIS required 'C.UTF-8' over 'C'
    os.environ.update({'LC_ALL': 'C.UTF-8'})
    sh.sort(
        sh.cat(glob.glob(os.path.join(input_dir, '*')), _piped=True),
        _out=sorted_output_filename,
    )

    # Open grouper output files.  Store the file handles in a circular buffer.
    grouper_files = collections.deque(maxlen=num_workers)
    for i in range(num_workers):
        filename = os.path.join(output_dir, part_filename(i))
        file = open(filename, 'w')
        grouper_files.append(file)

    # Write lines to grouper output files.  Round robin allocation by key.
    prev_key = None
    with open(sorted_output_filename, 'r') as sorted_output_file:
        for line in sorted_output_file:
            # Parse the line.  Must be two strings separated by a tab.
            assert '\t' in line, "Error: no TAB found in line."
            key, _ = line.split('\t', maxsplit=2)

            # If it's a new key, then rotate circular queue of grouper files
            if prev_key is not None and key != prev_key:
                grouper_files.rotate(1)

            # Write to grouper file
            grouper_files[0].write(line)

            # Update most recently seen key
            prev_key = key

    # Close grouper output file handles
    for file in grouper_files:
        file.close()


def reduce_stage(exe, input_dir, output_dir, num_reduce, enforce_keyspace):
    """Execute reducers."""
    for i in range(num_reduce):
        input_filename = os.path.join(input_dir, part_filename(i))
        output_filename = os.path.join(output_dir, part_filename(i))
        reduce_command = sh.Command(exe)
        print("+ {} < {} > {}".format(exe, input_filename, output_filename))
        with open(input_filename, 'r') as input_file:
            reduce_command(_in=input_file, _out=output_filename)

        if enforce_keyspace:
            check_num_keys(output_filename)


if __name__ == '__main__':
    main()
