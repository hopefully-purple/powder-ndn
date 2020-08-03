#!/bin/bash

#This script is for a node, setting up network

#What is the eth?
ifconfig
echo "What is the eth you want to effect?(format: eth#) "
read eth

change() {

	#How many milliseconds?
	echo "How many milliseconds? Remember, do half of what you want.(format: #ms) "
	read latency

	#Change latency
	echo "Changing the latency"

	sudo tc qdisc add dev $eth root netem delay $latency
}

#What do you want to do?
echo "Change, display active, or remove?(c/d/r): "
read action

if [ "$action" == "d" ]; then
	sudo tc qdisc show dev $eth
elif [ "$action" == "r" ]; then
	sudo tc qdisc del dev $eth
elif [ "$action" == "c" ]; then
	change
	sudo tc qdisc show dev $eth
fi

echo "Done!"
