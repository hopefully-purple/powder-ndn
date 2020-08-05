#!/bin/bash

#This script is for both routers
#This sets up the connections between it and the other router

nfdset() {
	read -p "What is the ip you want to connect to? " ADDR

	#First step, make sure nfd is running
	read -p "Restart nfd?(y/n): " restart
	if [ $restart == "y" ]; then
		echo "Restarting nfd"
		nfd-stop
		nfd-start
	fi

	#Create face
	echo "Creating face, connecting to $ADDR"

	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR

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
		echo "Pinging 4 times to $ADDR under dictionary and attack prefixes"
		ndnping -c 4 -t /ndn/dictionary
		ndnping -c 4 -t /ndn/attack
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

4gr1()
{
	read -p "Restart nfd?(y/n): " restart
	if [ $restart == "y" ]; then
		echo "Restarting nfd"
		#nfdc face destroy udp4://10.10.6.2
		nfd-stop
		nfd-start
	fi

	ADDR=10.10.6.2
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve off
		
	#----------------
	echo "Router 2"
	eth="eth1"
	latency="3.83333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#----------------

	#----------------
	echo "Node 1"
	eth="eth2"
	latency="3.83333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#----------------

}

4gr2()
{
	read -p "Restart nfd?(y/n): " restart
	if [ $restart == "y" ]; then
		echo "Restarting nfd"
		nfd-stop
		nfd-start
	fi

	#-------------------
	echo "Router 3"
	ADDR=10.10.7.2
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve off
		
	eth="eth2"
	latency="3.83333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 2"
	eth="eth3"
	latency="7.66666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 3"
	eth="eth4"
	latency="7.66666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 4"
	eth="eth5"
	latency="7.66666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 5"
	eth="eth6"
	latency="7.66666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Router 1"
	ADDR=10.10.6.1
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve off
		
	eth="eth1"
	latency="3.83333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

}

4gr3()
{
	read -p "Restart nfd?(y/n): " restart
	if [ $restart == "y" ]; then
		echo "Restarting nfd"
		nfd-stop
		nfd-start
	fi

	ADDR=10.10.7.1
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve on
		
	eth="eth1"
	latency="3.83333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth

}

5gr1()
{
	read -p "Restart nfd?(y/n): " restart
	if [ $restart == "y" ]; then
		echo "Restarting nfd"
		nfd-stop
		nfd-start
	fi

	ADDR=10.10.6.2
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve off

	#----------------
	echo "Router 2"
	eth="eth1"
	latency="0.16666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#----------------

	#----------------
	echo "Node 1"
	eth="eth2"
	latency="0.16666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#----------------
		
}

5gr2()
{
	read -p "Restart nfd?(y/n): " restart
	if [ $restart == "y" ]; then
		echo "Restarting nfd"
		nfd-stop
		nfd-start
	fi

	#-------------------
	echo "Router 3"
	ADDR=10.10.7.2
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve off
		
	eth="eth2"
	latency="0.16666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 2"
	eth="eth3"
	latency="0.33333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 3"
	eth="eth4"
	latency="0.33333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 4"
	eth="eth5"
	latency="0.33333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Node 5"
	eth="eth6"
	latency="0.33333333ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------

	#-------------------
	echo "Router 1"
	ADDR=10.10.6.1
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve off
		
	eth="eth1"
	latency="0.16666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth
	#-------------------
}	

5gr3()
{
	read -p "Restart nfd?(y/n): " restart
	if [ $restart == "y" ]; then
		echo "Restarting nfd"
		nfd-stop
		nfd-start
	fi

	ADDR=10.10.7.1
	nfdc face create udp4://$ADDR

	echo "Creating route with prefix /ndn/dictionary to nexthop $ADDR"
	nfdc route add prefix /ndn/dictionary nexthop udp4://$ADDR
	
	echo "Creating route with prefix /ndn/attack to nexthop $ADDR"
	nfdc route add prefix /ndn/attack nexthop udp4://$ADDR
	
	nfdc cs config serve on
		
	eth="eth1"
	latency="0.16666667ms"

	sudo tc qdisc del dev $eth root
	sudo tc qdisc add dev $eth root netem delay $latency
	sudo tc qdisc show dev $eth

}

#Automation?
read -p "Automation?(4g1/4g2/4g3/5g1/5g2/5g3/n): " auto

if [ "$auto" == "4g1" ]; then
	4gr1
elif [ "$auto" == "4g2" ]; then
	4gr2
elif [ "$auto" == "4g3" ]; then
	4gr3
elif [ "$auto" == "5g1" ]; then
	5gr1
elif [ "$auto" == "5g2" ]; then
	5gr2
elif [ "$auto" == "5g3" ]; then
	5gr3
fi

#Set up nfd?
read -p "Set up nfd?(y/n): " setnfd

if [ "$setnfd" == "y" ]; then
	nfdset
fi

#Change latency?
read -p "Change? Display? Remove?(c/d/r): " lat

if [ "$lat" == "c" ]; then
	change
elif [ "$lat" == "r" ]; then
	ifconfig
	read -p "What is the eth?(format: eth#) " eth
	
	sudo tc qdisc del dev $eth root
elif [ "$lat" == "d" ]; then
	ifconfig
	read -p "What is the eth?(format: eth#) " eth

	sudo tc qdisc show dev $eth
fi

if [ "$lat" == "c" ]; then
	read -p "Input eth one more time: " eth
	sudo tc qdisc show dev $eth
fi

echo "Done!"




