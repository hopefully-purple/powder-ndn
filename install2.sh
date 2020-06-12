#!/bin/bash

# this bash script installs various NDN software

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

# create a directory for nlsr logging
mkdir -p ~/nlsr/log/

# copy the appropriate nlsr configuration file to the nlsr directory
cp /local/repository/nlsr2.conf ~/nlsr/nlsr.conf

# copy a .vimrc on each VM (provides useful remappings)
cp /local/repository/.vimrc ~/

# create a udp tunnel
nfdc face create udp4://10.10.1.1