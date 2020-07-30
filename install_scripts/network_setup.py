"""
This script handles the network setup for the powder ndn profile
"""

import argparse
from fabric import Connection


def create_faces():
    """Creates the relevant UDP faces between routers"""
    connection['up-cl'].run('nfdc face create udp4://10.10.3.2')
    connection['up-cl'].run('nfdc face create udp4://10.10.2.2')
    connection['external-dn'].run('nfdc face create udp4://10.10.2.1')
    connection['internal-dn'].run('nfdc face create udp4://10.10.3.1')


def start_nlsr():
    """Starts the NLSR routing daemon on all servers"""
    run_bg(connection['up-cl'], 'nlsr -f ~/nlsr/nlsr.conf')
    run_bg(connection['external-dn'], 'nlsr -f ~/nlsr/nlsr.conf')
    run_bg(connection['internal-dn'], 'nlsr -f ~/nlsr/nlsr.conf')


def configure_network(internal_latency, external_latency):
    """Configure latency, bandwidth, and packet loss rates to internal and external networks.
    Note that this may need to be updated if profile topolgy changes.
    """

    # note that these may need to be updated if profile topology changes
    shape_link(connection['up-cl'], 'eth3', internal_latency, latency_variation=3)
    shape_link(connection['up-cl'], 'eth2', external_latency, latency_variation=10)


def shape_link(this_connection, interface, latency, latency_variation=3):
    """Set packet loss, bandwidth, and latency on a given connection and interface."""

    # TODO: fix this to work with no latency and packet loss values

    this_connection.run(f'sudo tc qdisc replace dev {interface} root handle 1: delay {latency}ms {latency_variation}ms distribution normal')
    this_connection.run(f'sudo tc qdisc replace dev {interface} parent 1: handle 2: latency 400ms burst 100mbit')
    this_connection.run(f'sudo tc qdisc show dev {interface}')


def reset_nfd():
    """Restarts the NDN forwarding daemon."""
    for k, c in connection.items():
        if k != 'UE1':
            c.run('nfd-stop')
            c.run('nfd-start')

def clear_qdiscs():
    """Clears the two qdiscs on the up-cl router."""
    connection['up-cl'].run(f'sudo tc qdisc del dev eth2 root')
    connection['up-cl'].run(f'sudo tc qdisc del dev eth3 root')

# begin rest of script

parser = argparse.ArgumentParser()

# add mandatory pc number section
parser.add_argument("pc_number", help="the number corresponding to the pc running the POWDER experiement")

# network setup and reset options
group = parser.add_mutually_exclusive_group()
group.add_argument("-S", "--setup", help="setup the network from scratch", action="store_true")
group.add_argument("-R", "--reset", help="reset the forwarding and routing daemons", action="store_true")

# network latency and loss parameters
parser.add_argument("-i", "--internal_latency", help="set internal latency (ms)", metavar="INTERNAL_LATENCY", type=int, default=0, choices=range(1, 1000))
parser.add_argument("-e", "--external_latency", help="set external latency (ms)", metavar="EXTERNAL_LATENCY", type=int, default=0, choices=range(1, 1000))

# remove all network adjustments option
parser.add_argument("--clear", help="clear network qdiscs", action="store_true")

args = parser.parse_args()

# run methods based on command line arguments specified
if args.setup:
    create_faces()
    start_nlsr()
elif args.reset:
    reset_nfd()
    create_faces()
    start_nlsr()

# configure network latency, loss, and bandwidth parameters
if args.internal_latency != 0 or args.external_latency != 0: 
    configure_network(args.internal_latency, args.external_latency)

if args.clear:
    clear_qdiscs()



