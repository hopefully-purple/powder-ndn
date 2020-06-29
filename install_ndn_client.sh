#!/bin/bash

# this bash script installs the NDN python client library for python3
sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python3-pip -y
sudo pip3 install pyndn

# copy the client code to the user's home directory
cp /local/repository/request_data.py ~/

# copy the testing code to the user's home directory
cp /local/repository/begin_testing.py ~/

# copy the stats file to the user's home directory
cp /local/repository/stats_file.txt ~/

# copy the control file to the user's home directory
cp /local/repository/control.py ~/

# copy the two .txt files into the user's home directory
cp /local/repository/dictionary.txt ~/
cp /local/repository/alicewonderland.txt ~/
