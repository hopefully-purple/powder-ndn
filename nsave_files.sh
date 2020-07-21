#!/bin/bash

#Script that saves data files in client

#plot_outin_data.png
#stats_file.txt
#outin.dat

#Take in name arguments
EXPNAME=ARG1

#Check if saved_data directory exists
DIR="/clsaved_data/"
if [ -d "$DIR" ]; then
	echo "Moving files"
else
	#Make the directory
	mkdir /clsaved_data/


