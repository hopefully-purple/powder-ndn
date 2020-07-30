#!/bin/bash

#Script that saves data files in client

#plot_outin_data.png
#stats_file.txt
#outin.dat

#Take in name arguments
#EXPNAME=$1

#Check if saved_data directory exists
DIR="/users/hopew/data_collection/clsaved_data/"

[ ! -d "$DIR" ] && sudo mkdir -p "$DIR"

cp data_collection/plot_outin_data.png data_collection/plot_"$1".png
sudo mv data_collection/plot_"$1".png $DIR 

cp data_collection/stats_file.txt data_collection/stats_"$1".txt
sudo mv data_collection/stats_"$1".txt $DIR

cp data_collection/outin.dat data_collection/outin_"$1".txt
sudo mv data_collection/outin_"$1".txt $DIR

cp data_collection/results.dat data_collection/results_"$1".dat
sudo mv data_collection/results_"$1".dat $DIR

cp data_collection/gnuplotstatistics.txt data_collection/gnuplotstats_"$1".txt
sudo mv data_collection/gnuplotstats_"$1".txt $DIR

