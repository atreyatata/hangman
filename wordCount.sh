#!/bin/bash
#
# Example of how to chain mapreduce jobs together.  The output of one
# job is the input to the next.
#
# Hadoop options
# jar index/hadoop/hadoop-streaming-2.7.2.jar   # Hadoop configuration
# -D mapreduce.job.maps=<int>                   # Number of mappers
# -D mapreduce.job.reduces=<int>                # Number of reducers
# -input <directory>                            # Input directory
# -output <directory>                           # Output directory
# -mapper <exec_name>                           # Mapper executable
# -reducer <exec_name>                          # Reducer executable

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

# Run first MapReduce job
hadoop \
  jar hadoop-streaming-2.7.2.jar \
  -D mapreduce.job.maps=30 \
  -D mapreduce.job.reduces=5 \
  -input output.txt \
  -output wordCount.txt \
  -mapper ./map.py \
  -reducer ./reduce.py \
