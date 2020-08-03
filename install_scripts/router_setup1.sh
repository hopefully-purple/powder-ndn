#!/bin/bash

#This script is for router 1. 
#This sets up the connections between it and router 2.


#Arguments: $1 = udp4 address to connect to, $2 is the eth
ADDR=$1
#ETH=$2

if [ "$ADDR" == "" ]; then
	echo "What is the ip you want to connect to?"
	read ip
	$ADDR=ip
fi

#First step, make sure nfd is running
echo "Making sure nfd is running . . ."
nfd-start

#Create face
echo "Creating face, connecting to $ADDR"

nfdc face create udp4://$ADDR

#Ask for faceid
echo "What is the face id?"
read faceid

#Create route
echo "Creating route with face id $faceid and prefix /ndn/dictionary"

nfdc route add /ndn/dictionary $faceid

#Turn off caching?
echo "Turn off caching?(y/n): "
read caching

if [ "$caching" == "y" ]; then
	nfdc cs config serve off
else
	nfdc cs config serve on
fi

#Wait for test?
echo "Test connection? Yes, wait until ready, otherwise no.(y/n): "
read test

if [ "$test" == "y" ]; then
	echo "testing" | ndnpoke /ndn/dictionary
fi

#Change latency?
echo "Change Latency? if yes, enter the ms.(#ms/n): "
read latency

change() {

	ifconfig
	echo "What is the eth?(format: eth#) "
	read eth

        #How many mbits?
        echo "(Leave blank if no bandwidth to change) How many bits for rate?(format: #mbit) "
        read mbit

        #How many kbits?
        echo "(Leave blank if no bandwidth to change) How many bits for burst?(format: #kbit) "
        read kbit

	if [ "$mbit" != "" ]; then
        	#limit the bandwidth
        	echo "Limiting . . . "
        	sudo tc qdisc add dev $eth root tbf rate $mbit burst $kbit latency $latency
	else
		sudo tc qdisc add dev $eth root netem delay $latency
	fi

}

if [ "$latency" != "n" ]; then
	change()
	sudo tc qdisc show dev $eth
fi

echo "Done!"




