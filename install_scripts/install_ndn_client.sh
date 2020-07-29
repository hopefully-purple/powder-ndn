#!/bin/bash

# this bash script installs the NDN python client library for python3
sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python3-pip -y

#install gnuplot
sudo apt-get install gnuplot rlwrap -y
sudo apt-get install imagemagick -y

# Maintained version of pyndn currently does not have packet v0.3 support, so alternate version must be built
git clone https://github.com/Pesa/PyNDN2 ~/PyNDN2
cd ~/PyNDN2 && git merge remotes/origin/packet03
pip3 install ~/PyNDN2
sudo pip3 install python-dateutil


cp -R /local/repository/node ~/
cp /local/repository/begin_testing.py ~/

# copy the client code to the user's home directory
#cp /local/repository/request_data.py ~/

# copy the testing code to the user's home directory
#cp /local/repository/begin_testing.py ~/

#copy modified bashrc 
cp /local/repository/.1bashrc ~/.bashrc

# copy the stats file to the user's home directory
#cp /local/repository/stats_file.txt ~/

# copy the control file to the user's home directory
#cp /local/repository/control.py ~/
#cp /local/repository/nsave_files.sh ~/
#cp /local/repository/counter.py ~/
#cp /local/repository/convert_time.py ~/
#cp /local/repository/make_requests.py ~/
#cp /local/repository/analyze_outin.gnuplot ~/
# copy the two .txt files into the user's home directory
#cp /local/repository/alice.txt ~/
#cp /local/repository/whole_dict.txt ~/
