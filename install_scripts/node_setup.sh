#!/bin/bash

#This script is for a node, setting up network

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

4gnv() {

	eth="eth1"
	latency="3.83333333ms"

	echo "Changing latency to $latency"
	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
}

4gna() {

	eth="eth1"
	latency="7.66666667ms"

	echo "Changing latency to $latency"
	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
}

5gnv() {

	eth="eth1"
	latency="0.16666667ms"

	echo "Changing latency to $latency"
	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
}

5gna() {

	eth="eth1"
	latency="0.33333333ms"

	echo "Changing latency to $latency"
	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
}


#Automation?
read -p "Automate?(4gnv/4gna/5gnv/5gna/n) " auto

if [ "$auto" == "4gnv" ]; then
	4gnv
elif [ "$auto" == "4gna" ]; then
	4gna
elif [ "$auto" == "5gnv" ]; then
	5gnv
elif [ "$auto" == "5gna" ]; then
	5gna
fi

#What do you want to do?
read -p "Change, display active, or remove?(c/d/r): " action

if [ "$action" == "d" ]; then
	#What is the eth?
	ifconfig
	read -p "What is the eth you want to effect?(format: eth#) " eth
	sudo tc qdisc show dev $eth
elif [ "$action" == "r" ]; then
	#What is the eth?
	ifconfig
	read -p "What is the eth you want to effect?(format: eth#) " eth
	sudo tc qdisc del dev $eth root
elif [ "$action" == "c" ]; then
	#What is the eth?
	ifconfig
	read -p "What is the eth you want to effect?(format: eth#) " eth
	read -p "Just latency or bandwidth as well?(l/b): " choice
	if [ "$choice" == "l" ]; then
		changelatency
		sudo tc qdisc show dev $eth
	elif [ "$choice" == "b" ]; then
		changeband
		sudo tc qdisc show dev $eth
	fi
fi

echo "Done!"
