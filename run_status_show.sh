#!/bin/bash

#This script runs the nfdc status show command and outputs to the timed_nfdc_status.txt 
#It will run the command every minute for the given amount of minutes, or every given second. 
#User must specify the lengths.

#Default will be every 30 seconds for 5 minutes.
interval=10
duration=1

echo "This is the show status output for a unrelated timer, to be run during experiments." > timed_nfdc_status.txt
echo "Every $interval seconds for $duration minutes" >> timed_nfdc_status.txt

totalseconds=$((duration * 60))
iterations=$((totalseconds / interval))

START=1
END=$iterations

echo "Now beginning . . . ."
echo "Will end in $duration minutes at:"
date --date="+$totalseconds seconds" +"%Y-%m-%d %H:%M:%S"

#echo "CurrentTime\tFib\tPit\tMeasurements\tCs\tInInterests\tOutInterests\tInData\tOutData\tInNacks\tOutNacks\tSatisfiedInterests\tUnsatisfiedInterests\n" > timed_data.dat
echo "" > timed_data.dat
echo "" > temp0_timed_data.dat
echo "" > temp1_timed_data.dat
echo "" > temp2_timed_data.dat
echo "" > temp3_timed_data.dat

echo "" > temp_nfdc_status.txt

for (( c=$START; c<=$END; c++ ))
do
	nfdc status show >> timed_nfdc_status.txt #append to nfdc_status
	nfdc status show > temp_nfdc_status.txt #overwrite inbetween file

	awk -F"=" 'NR!=1{print $2 > "temp0_timed_data.dat"}' temp_nfdc_status.txt #delimit by =
	cat temp0_timed_data.dat | awk '{print > "temp1_timed_data.dat"}' ORS='\t' #put it all in one line separated by tabs	
	echo "\n" >> temp1_timed_data.dat #add a new line?
	cat temp1_timed_data.dat >> temp2_timed_data.dat #append to temp2 

	sleep $interval
done

echo "Finished timing"

#Edit timed data
#Remove version, startimte, and uptime columns
awk '{ print $3, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18 > "temp3_timed_data.dat"}' temp2_timed_data.dat
#Get rid of unwanted date number on current time
cat temp3_timed_data.dat | cut -c 12- > temp0_timed_data.dat
#Put in timed_data under labels
cat temp0_timed_data.dat >> timed_data.dat

#clean up directory
rm temp0_timed_data.dat
rm temp1_timed_data.dat
rm temp2_timed_data.dat
rm temp3_timed_data.dat

rm temp_nfdc_status.txt

#make plot and table
gnuplot -persist -c "analyze_data.gnuplot" "$interval seconds for $duration minutes"
display plot_timed_data.png &

echo "Finished"



