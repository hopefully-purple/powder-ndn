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


cp -R /local/repository/node/code ~/
cp -R /local/repository/node/data_collection ~/
cp /local/repository/begin_testing.py ~/
cp /local/repository/install_scripts/node_setup.sh ~/
chmod +x node_setup.sh

#copy modified bashrc 
cp /local/repository/.1bashrc ~/.bashrc

