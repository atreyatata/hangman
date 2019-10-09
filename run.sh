#!/bin/bash

echo "Building environment to run python program"
virtualenv hangman_env
echo "Activating environment"
source hangman_env/bin/activate
echo "Installing dependencies"
pip install -r requirements.txt

echo "Running program"
python hangman.py $1 $2

echo "Deactivating environment"
deactivate
echo "Cleaning up environment"
rm -rf hangman_env
