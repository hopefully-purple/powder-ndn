#!/bin/bash

# this bash script installs various NDN software on router 1

# set up ppa repository
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:named-data/ppa -y
sudo apt-get update

# install ndn software
sudo apt-get install nfd -y
sudo apt-get install ndn-tools -y
sudo apt-get install ndn-traffic-generator -y
sudo apt-get install nlsr -y
sudo apt-get install libchronosync -y
sudo apt-get install libpsync -y

#install x11 apps
sudo apt-get install x11-apps -y 
sudo apt-get install strace -y

#install wireshark
sudo apt-get install wireshark -y

# create a directory for nlsr logging
mkdir -p ~/nlsr/log/

# copy the appropriate nlsr configuration file to the nlsr directory
cp /local/repository/nlsr1.conf ~/nlsr/nlsr.conf

# copy a .vimrc on each VM (provides useful remappings)
cp /local/repository/.vimrc ~/

#copy scripts and files
cp /local/repository/host_data.py ~/
cp /local/repository/nfdc_status.txt ~/

cp /local/repository/alice.txt ~/
cp /local/repository/whole_dict.txt ~/

# create a udp tunnel
#nfdc face create udp4://10.10.2.2 persistency permanent
