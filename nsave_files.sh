#!/bin/bash

#Script that saves data files in client

#plot_outin_data.png
#stats_file.txt
#outin.dat

#Take in name arguments
#EXPNAME=$1

#Check if saved_data directory exists
DIR="/users/hopew/clsaved_data/"

[ ! -d "$DIR" ] && sudo mkdir -p "$DIR"

cp plot_outin_data.png plot_"$1".png
sudo mv plot_"$1".png $DIR 

cp stats_file.txt stats_"$1".txt
sudo mv stats_"$1".txt $DIR

cp outin.dat outin_"$1".txt
sudo mv outin_"$1".txt $DIR

cp results.dat results_"$1".dat
sudo mv results_"$1".dat $DIR
