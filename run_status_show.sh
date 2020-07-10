#!/bin/bash

#This script runs the nfdc status show command and outputs to the timed_nfdc_status.txt 
#It will run the command every minute for the given amount of minutes, or every given second. 
#User must specify the lengths.

#Default will be every 30 seconds for 5 minutes.

#echo "Wipe timed_nfdc_status.txt?(y/n)"
#read wipe

#if [ "$wipe" == "y" ]; then
echo "This is the show status output for a unrelated timer, to be run during experiments." > timed_nfdc_status.txt
#elif [ "$wipe" == "n" ]; then
#	echo -e "ANOTHER RUN\n" >> timed_nfdc_status.txt
#fi

#echo "Default: every 60 seconds for 10 minutes" >> timed_nfdc_status.txt
echo "Custom: every 1 seconds for 1 minutes" >> timed_nfdc_status.txt


#read choice

interval=1
duration=1

#if [[ $choice == "n" ]]; then
#	echo "How often?"
#	read often
#	interval=often
#	echo "How long?"
#	read long
#	duration=long
#fi

totalseconds=$((duration * 60))
iterations=$((totalseconds / interval))

START=1
END=$iterations

echo "Now beginning . . . ."
echo "Will end in $duration minutes at:"
date --date="+$totalseconds seconds" +"%Y-%m-%d %H:%M:%S"
#echo "Before timing loop" >> timed_nfdc_status.txt

#nfdc status show >> timed_nfdc_status.txt

for (( c=$START; c<=$END; c++ ))
do
	nfdc status show >> timed_nfdc_status.txt
#	echo -n "$c " >> timed_nfdc_status.txt
	sleep $interval
done

echo "Finished"
