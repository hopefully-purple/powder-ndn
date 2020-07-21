#!/bin/bash

#Script that saves data files in client

#echo_times.txt
#plot_timed_data.png
#timed_nfdc_status.txt
#timed_data.dat

#Take in name arguments
#EXPNAME=$1

#Check if saved_data directory exists
DIR="/users/hopew/rosaved_data/"

[ ! -d "$DIR" ] && sudo mkdir -p "$DIR"

cp echo_times.txt echo_"$1".txt
sudo mv echo_"$1".txt $DIR

cp plot_timed_data.png plot_"$1".png
sudo mv plot_"$1".png $DIR

cp timed_nfdc_status.txt timed_nfdc_"$1".txt
sudo mv timed_nfdc_"$1".txt $DIR

cp timed_data.dat timed_data_"$1".dat
sudo mv timed_data_"$1".dat $DIR

