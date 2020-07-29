#!/bin/bash

#This script runs the nfdc status show command and outputs to the timed_nfdc_status.txt 
#It will run the command every minute for the given amount of minutes, or every given second. 
#User must specify the lengths.

interval=5
duration=2

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
echo "# Data file for nfdc stats\n" > timed_data.dat

for i in 0 1 2 3 4 5; do
	echo "" > temp"$i"_timed_data.dat
done
echo "" > temp_nfdc_status.txt

#ENDT=""
#Error handling attempt
ERROR=false
#set -e
trap 'catch $? $LINENO' ERR

catch(){
	echo "NFDC STATUS SHOW STOPPED RESPONDING"
	if [ "$1" != "0" ]; then
		ERROR=true
		echo "ERROR = true"
		#$ENDT='date "+%F_%T"'
	fi
}

for (( c=$START; c<=$END; c++ ))
do
	nfdc status show >> timed_nfdc_status.txt #append to nfdc_status
	nfdc status show > temp_nfdc_status.txt #overwrite inbetween file
	
	if [ "$ERROR" == true ]; then
		break
	fi

	if [ $((c % 14)) -eq 0 ]; then
		echo "Keeping connection alive"
	fi

	awk -F"=" 'NR!=1{print $2 > "temp0_timed_data.dat"}' temp_nfdc_status.txt #delimit by =
	cat temp0_timed_data.dat | awk '{print > "temp1_timed_data.dat"}' ORS='\t' #put it all in one line separated by tabs	
	echo "\n" >> temp1_timed_data.dat #add a new line?
	cat temp1_timed_data.dat >> temp2_timed_data.dat #append to temp2 

	sleep $interval
done

#$ENDT=date +$F_%T
#if [ "$ERROR" == false ]; then 
#	$ENDT=$(date +$F_%T)
#fi

echo "Finished timing"
now="$(date)"
printf "Ended %s\n" "$now"

edit(){
	#Edit timed data
	#Remove version, startimte, and uptime columns
	awk '{ print $3, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18 > "temp3_timed_data.dat"}' temp2_timed_data.dat

	#call redo_time.py, it will put the converted time into temp4
	python3 redo_time.py 

	#Remove currenttime column from temp3, put in temp 5
	awk '{print $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14 > "temp5_timed_data.dat"}' temp3_timed_data.dat

	#Add the new time column in temp4 to the beginning of temp5 into temp0
	paste temp4_timed_data.dat temp5_timed_data.dat | awk '{$15=""; print > "temp0_timed_data.dat"}'
	#Get rid of unwanted date number on current time 12 includes mniutes?, 17 is just milliseconds
	cat temp0_timed_data.dat | cut -c 5- > temp1_timed_data.dat
	#Put in timed_data under the correct file
	cat temp1_timed_data.dat >> timed_data.dat

	#clean up directory
	for i in 0 1 2 3 4 5; do
		rm temp"$i"_timed_data.dat
	done
	rm temp_nfdc_status.txt
}

edit

#fg echo "Plot?(y/n): "
echo "PLOTTING . . . "
#read PLOT

#if [ PLOT == "y" ]; then
	#make plot and table
gnuplot -persist -c "analyze_data.gnuplot" "$interval seconds for $duration minutes" $interval
#feh plot_timed_data.png & 
display plot_timed_data.png &
#fi

echo "Finished"


