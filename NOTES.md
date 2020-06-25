# Experimental Notes

**To-do:**
* Experiment with ndn-traffic-generator
* Write a program for easier experimental router configuration? (nlsr.conf)
* Experiment with ndn client-side libraries
* Better understand the routing software
  * configuration files?
  * autogenerate routes to producers
  * avoid manual setup of routes
* Get NDN working over ethernet
* Get NDN working over a 4G or 5G network


**Things we've learned:**
* Use `ndnpeek` and `ndnpoke` to transmit request and data packets
	*  `ndnpoke` transmits a single data packet; however, multiple requests for that data can be satisfied if the data is cached in the Content Store.
* Routes are one-way, and they must exist in the RIB before interests can be satisfied
* `nfd-status` prints lots of useful information
* A correct udp4 face must be created before nlsr will work properly. Use something like `nfdc face create udp4://10.10.x.x`
* Use `ifconfig` or `ip link` to find MAC addresses of the various VMs.
* NFD configuration file is located at `/etc/ndn/nfd.conf`
* See FAQ for setting up ethernet faces
* Use `nfdc` to view all subcommands
* Use the `nfdc cs` commands to manipulate the content store
* ndn-traffic-generator (`ndn-traffic-server` and `ndn-traffic-client`) may need to be run from a bash shell, not the defualt c shell
* Use the `tc` command to configure network behavior (note that it often must be run as root). Latency, packet loss, packet corruption, and all sorts of interesting things can be done.


**Questions to ask:**
* What are the channels found with the `nfdc channel list` command? How are they different from the faces found with `nfdc face list`
* Figure out how to add ethernet faces - we're stuck here
* Figure out why 75% of packets are being lost when packet loss is set to 50% with `sudo tc qdisc add dev eth1 root netem loss 10%`.



__________________
Hope's Notes and To Do List:
1. Figure out how to constrain PIT
2. Add a second node to the LAN and play with requesting
3. Begin victim script (just get the control case to work)
	3.1 Get requests to work
	3.2 Figure out how to time and record

Things I've discovered: 
When Router2 hosts data that the client wants, NDN works successfully with Router1 as the middle.
Routers can hold multiple data under different prefixes at once: echo "data" | ndnpoke /ndn/data &

ProTips:
Router1: nfdc route add /ndn/ udp4://10.10.2.2
Router2: nfdc route add /ndn/ udp4://10.10.2.1

When you create a route, the router you ran "route add" on will then be able to *receive* data hosted by the router you connected to. 
Example:
router1-1:~> nfdc route add /ndn/ udp4:10.10.2.2
router2-1:~> echo "data" | ndnpoke /ndn/data
router1-1:~> ndnpeek -p /ndn/data
data

nfdc face list | grep "udp4"



