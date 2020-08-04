#!/bin/bash

#Script that saves data files in client

#echo_times.txt
#plot_timed_data.png
#timed_nfdc_status.txt
#timed_data.dat

#Take in name arguments
#EXPNAME=$1

#Check if saved_data directory exists
DIR="/users/hopew/data_collection/rosaved_data/"

[ ! -d "$DIR" ] && sudo mkdir -p "$DIR"

cp data_collection/echo_times.txt data_collection/echo_"$1".txt
sudo mv data_collection/echo_"$1".txt $DIR

cp data_collection/plot_timed_data.png data_collection/plot_"$1".png
sudo mv data_collection/plot_"$1".png $DIR

cp data_collection/timed_nfdc_status.txt data_collection/timed_nfdc_"$1".txt
sudo mv data_collection/timed_nfdc_"$1".txt $DIR

cp data_collection/timed_data.dat data_collection/timed_data_"$1".dat
sudo mv data_collection/timed_data_"$1".dat $DIR

cp data_collection/ndndump.txt data_collection/ndndump_"$1".txt
sudo mv data_collection/ndndump_"$1".txt $DIR


