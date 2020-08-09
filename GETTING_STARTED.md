# Getting Started

**POWDER Setup**

Create a POWDER profile - the provided profile contained in profile.py provides a good starting point. The default is 5 nodes and 3 routers, but it can be set to numbers less than that. Further tinkering with the script would be required for more.

**Once you've ssh'd in**

Once the experiment is complete and you set up your terminals, you must `chmod +x` the node_setup.sh and the router_setup.sh that should be in the ~ directory. From there, you must use `./` to execute those scripts and set up the network settings and nfd communications. Be advised that to guarantee that Router2 will look to Router3, run the router_setup on Router1, then Router3, and lastly Router2.

For each node, you must go to the make_requests.py under the code directory and uncomment the udp connection line that contains the correct ip address of the router it is connected to. Looking at the Manifest on the POWDER profile will tell you which address to use. You also need to change request_data.py on the same line to the righ ip address if you want to use the single interest script.

**NFD (Named Data Networking Forwarding Daemon):**

Install NFD on nodes if necessary (if the provided profile is used, the software will automatically be installed). Detailed instructions can be found here: http://named-data.net/doc/NFD/current/INSTALL.html (note that installing from the PPA repository with apt-get is much simpler than building from source).

The NDN forwarding daemon should start automatically. This can be checked with `nfd-status`. To manually start and stop the forwarder, use `nfd-start` and `nfd-stop`.

Create routes between nodes with `nfdc route add`. For example, to create a UDP tunnel that serves all names under /ndn/hello, use: `nfdc route add prefix /ndn/hello nexthop <face-uri | face-id>`.
Faces (and their respective URIS or IDs) for creating routes can be found with `nfdc face list`.

**Testing**

Send test packets between nodes with `ndnpoke` and `ndnpeek`. If the PPA repository previously mentioned has been set up, these tools can easily be installed from it. If not, they can be built from source. For example, on the producer node, enter `echo "Hello World" | ndnpoke /ndn/demo/hello`. This will host one data packet containing the string "Hello World" located at `/ndn/demo/hello`. To request this data from another consumer node, use `ndnpeek -p /ndn/demo/hello`. 

For testing node connection to the routers, you can set up the request_data.py and run it. It will express one interest to the router it is connected to, and will print the response. 

**NLSR (Named-Data Link State Routing) Setup**

Install NLSR from the PPA repository or build from source. Modify the provided configuration file to appropriatly name routers and their neighbors (if a two-node network was used, the network should be automatically configured properly). The advertising section of the configuration files can also be modified to tell the network what data is available where.
