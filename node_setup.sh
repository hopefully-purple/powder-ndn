#!/bin/bash

#This script is for a node, setting up network

#What is the eth?
ifconfig
read -p "What is the eth you want to effect?(format: eth#) " eth

changelatency() {

	#How many milliseconds?
	read -p "How many milliseconds? Remember, do half of what you want.(format: #ms) " latency

	#Change latency
	echo "Changing the latency"

	sudo tc qdisc add dev $eth root netem delay $latency
}

changeband() {
	#How many milliseconds?
	read -p "How many milliseconds? Remember, do half of what you want.(format: #ms) " latency

	#How many mbits?
	read -p "How many bits for rate?(format: #mbit) " mbit

	#How many kbits?
	read -p "How many bits for burst?(format: #kbit) " kbit

	#limit the bandwidth
	echo "Limiting . . . "
	sudo tc qdisc add dev $eth root tbf rate $mbit burst $kbit latency $latency
}

#What do you want to do?
read -p "Change, display active, or remove?(c/d/r): " action

if [ "$action" == "d" ]; then
	sudo tc qdisc show dev $eth
elif [ "$action" == "r" ]; then
	sudo tc qdisc del dev $eth
elif [ "$action" == "c" ]; then
	read -p "Just latency or bandwidth as well?(l/b): " choice
	if [ "$choice" == "l" ]; then
		changelatency
		sudo tc qdisc show dev $eth
	elif [ "$choice" == "b" ]; then
		changeband
		sudo tc disc show dev $eth
	fi
fi

echo "Done!"
