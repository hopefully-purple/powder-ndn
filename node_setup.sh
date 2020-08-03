#!/bin/bash

#This script is for a node, setting up network

#What is the eth?
ifconfig
echo "What is the eth you want to effect?(format: eth#) "
read eth

changelatency() {

	#How many milliseconds?
	echo "How many milliseconds? Remember, do half of what you want.(format: #ms) "
	read latency

	#Change latency
	echo "Changing the latency"

	sudo tc qdisc add dev $eth root netem delay $latency
}

changeband() {
	#How many milliseconds?
	echo "How many milliseconds? Remember, do half of what you want.(format: #ms) "
	read latency

	#How many mbits?
	echo "How many bits for rate?(format: #mbit) "
	read mbit

	#How many kbits?
	echo "How many bits for burst?(format: #kbit) "
	read kbit

	#limit the bandwidth
	echo "Limiting . . . "
	sudo tc qdisc add dev $eth root tbf rate $mbit burst $kbit latency $latency
}

#What do you want to do?
echo "Change, display active, or remove?(c/d/r): "
read action

if [ "$action" == "d" ]; then
	sudo tc qdisc show dev $eth
elif [ "$action" == "r" ]; then
	sudo tc qdisc del dev $eth
elif [ "$action" == "c" ]; then
	echo "Just latency or bandwidth as well?(l/b): "
	read choice
	if [ "$choice" == "l" ]; then
		changelatency
		sudo tc qdisc show dev $eth
	elif [ "$choice" == "b" ]; then
		changeband
		suco tc disc show dev $eth
	fi
fi

echo "Done!"
