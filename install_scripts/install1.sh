#!/bin/bash

# this bash script installs various NDN software on router 1

# set up ppa repository
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:named-data/ppa -y
sudo apt-get update

# install nfd software
sudo apt-get install nfd -y

#install python3
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python3-pip -y

#install ndn tools
sudo apt-get install ndn-tools -y
sudo apt-get install nlsr -y
sudo apt-get install libchronosync -y
sudo apt-get install libpsync -y

#install gnuplot
sudo apt-get install gnuplot rlwrap -y
sudo apt-get install imagemagick -y

#install pyndn client software 
# Maintained version of pyndn currently does not have packet v0.3 support, so alternate version must be built
# sudo pip3 install pyndn
git clone https://github.com/Pesa/PyNDN2 ~/PyNDN2
cd ~/PyNDN2 && git merge remotes/origin/packet03
pip3 install ~/PyNDN2
sudo pip3 install python-dateutil
sudo pip3 install fabric

# create a directory for nlsr logging
mkdir -p ~/nlsr/log/

# copy the appropriate nlsr configuration file to the nlsr directory
cp /local/repository/install_scripts/nlsr1.conf ~/nlsr/nlsr.conf
cp /local/repository/install_scripts/router_setup.sh ~/

# copy a .vimrc on each VM (provides useful remappings)
cp /local/repository/.vimrc ~/

#change .bashrc for gnuplot
cp /local/repositoy/.1bashrc ~/.bashrc

#copy scripts and files
cp -R /local/repository/router/code ~/
cp -R /local/repository/router/data_collection ~/
cp /local/repository/host_data.py ~/

#cp /local/repository/host_data.py ~/
#cp /local/repository/echo_times.txt ~/
#cp /local/repository/1host_data.py ~/
#cp /local/repository/alice.txt ~/
#cp /local/repository/whole_dict.txt ~/
#cp /local/repository/run_status_show.sh ~/
#cp /local/repository/timed_nfdc_status.txt ~/
#cp /local/repository/analyze_data.gnuplot ~/
#cp /local/repository/rsave_files.sh ~/
#cp /local/repository/redo_time.py ~/
# create a udp tunnel
#nfdc face create udp4://10.10.2.2 persistency permanent
