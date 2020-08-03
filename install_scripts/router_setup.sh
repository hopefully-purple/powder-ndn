#!/bin/bash

#This script is for both routers
#This sets up the connections between it and the other router

nfdset() {
	read -p "What is the ip you want to connect to? " ADDR

	#First step, make sure nfd is running
	echo "Restarting nfd"
	nfd-stop
	nfd-start

	#Create face
	echo "Creating face, connecting to $ADDR"

	nfdc face create udp4://$ADDR

	#Ask for faceid
	read -p "What is the face id? " faceid

	#Create route
	echo "Creating route with face id $faceid and prefix /ndn/dictionary"

	nfdc route add /ndn/dictionary $faceid

	#Turn off caching?
	read -p "Turn off caching?(y/n): " caching

	if [ "$caching" == "y" ]; then
		nfdc cs config serve off
	else
		nfdc cs config serve on
	fi

	#Wait for test?
	read -p "Test connection? Yes, wait until ready, otherwise no.(y/n): " testq

	if [ $testq == "y" ]; then
		read -p "Host or request?(h/r): " action
		if [ $action == "h" ]; then
			echo "On other router, execute ndnpeek -p /ndn/dictionary. Should get testing in return"
			echo "testing" | ndnpoke /ndn/dictionary
		else:
			echo "Executing ndnpeek -p /ndn/dictionary"
			ndnpeek -p /ndn/dictionary
		fi
	fi
}

change() {

	ifconfig
	read -p "What is the eth?(format: eth#) " eth

	read -p "How many milliseconds of latency? Remember to do half.(format: #ms) " latency

        #How many mbits?
        read -p "(Leave blank if no bandwidth to change) How many bits for rate?(format: #mbit) " mbit

        #How many kbits?
        read -p "(Leave blank if no bandwidth to change) How many bits for burst?(format: #kbit) " kbit

	if [ "$mbit" != "" ]; then
        	#limit the bandwidth
        	echo "Limiting . . . "
        	sudo tc qdisc add dev $eth root tbf rate $mbit burst $kbit latency $latency
	else
		echo "Changing latency . . ."
		sudo tc qdisc add dev $eth root netem delay $latency
	fi

}

#Set up nfd?
read -p "Set up nfd?(y/n): " setnfd

if [ "$setnfd" == "y" ]; then
	nfdset
fi

#Change latency?
read -p "Change Latency? Remove all?(y/n/r): " lat

if [ "$lat" == "y" ]; then
	change
elif [ "$lat" == "r" ]; then
	ifconfig
	read -p "What is the eth?(format: eth#) " eth
	
	sudo tc qdisc del dev $eth root
fi

if [ $lat == "y" ]; then
	read -p "Input eth one more time: " eth
	sudo tc qdisc show dev $eth
fi

echo "Done!"




