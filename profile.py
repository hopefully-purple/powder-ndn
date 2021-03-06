"""A base profile for experimenting with NDN.

Instructions:
Wait for the profile instance to start, and then log into either VM via the ssh ports specified below.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as elab


class GLOBALS(object):
    """useful constant values for setting up a powder experiment"""
    SITE_URN = "urn:publicid:IDN+emulab.net+authority+cm"
    # standard Ubuntu release
    UBUNTU18_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
    PNODE_D740 = "d740"  # 24 cores, 192 GB RAM TODO: figure out the proper amount of ram, docs are incorrect
    PNODE_D840 = "d840"  # 64 cores, 768 GB RAM


# define network parameters
portal.context.defineParameter("node_count", "Client Nodes", portal.ParameterType.INTEGER, 5)
portal.context.defineParameter("router_count", "Routers", portal.ParameterType.INTEGER, 3)

# retrieve the values the user specifies during instantiation
params = portal.context.bindParameters()

#  check parameter validity
if params.node_count < 1 or params.node_count > 30:
    portal.context.reportError(portal.ParameterError("You must choose at least 1 and no more than 30 nodes."))

#  check parameter validity
if params.router_count < 1 or params.router_count > 3:
    portal.context.reportError(portal.ParameterError("You must choose at least 1 and no more than 3 routers."))


def mkVM(name, image, instantiateOn, cores, ram):
    """Creates a VM with the specified parameters

    Returns that VM
    """
    node = request.XenVM(name)
    node.disk_image = image
    node.cores = cores
    node.ram = ram * 1024
    node.exclusive = True
    node.routable_control_ip = True
    node.InstantiateOn(instantiateOn)
    return node


def create_nodes(count=1, prefix=1, instantiateOn='pnode', cores=2, ram=4):
    """Allocates and runs an install script on a specified number of VM nodes

    Returns a list of nodes.
    """

    nodes = []
    # index nodes by their proper number (not zero-indexed)
    nodes.append(None)

    # create each VM
    for i in range(1, count + 1):
        nodes.append(mkVM('node' + str(prefix) + '-' + str(i), GLOBALS.UBUNTU18_IMG, instantiateOn=instantiateOn, cores=cores, ram=ram))

    # run install scripts on each vm to install software
    for node in nodes:
        if node is not None:
            node.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install_scripts/install_ndn_client.sh"))
            node.addService(pg.Execute(shell="sh", command="/local/repository/install_scripts/install_ndn_client.sh"))

    return nodes


def create_routers(instantiateOn='pnode', cores=4, ram=8):
    """Allocates and runs an install script on two virtualized routers

    Returns a list of routers.
    """

    routers = []
    # index routers by their proper number (not zero-indexed)
    routers.append(None)

    # create each VM
    for i in range(1, params.router_count + 1):
        routers.append(mkVM('router' + str(i), GLOBALS.UBUNTU18_IMG, instantiateOn=instantiateOn, cores=cores, ram=ram))

    # run alternating install scripts on each vm to install software
    if params.router_count == 1:
        routers[1].addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install_scripts/install1.sh"))
        routers[1].addService(pg.Execute(shell="sh", command="/local/repository/install_scripts/install1.sh"))
    elif params.router_count == 2:
        routers[1].addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install_scripts/install1.sh"))
        routers[1].addService(pg.Execute(shell="sh", command="/local/repository/install_scripts/install1.sh"))
        routers[2].addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install_scripts/install2.sh"))
        routers[2].addService(pg.Execute(shell="sh", command="/local/repository/install_scripts/install2.sh"))
    elif params.router_count == 3:
        routers[1].addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install_scripts/install1.sh"))
        routers[1].addService(pg.Execute(shell="sh", command="/local/repository/install_scripts/install1.sh"))
        routers[2].addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install_scripts/install3.sh"))
        routers[2].addService(pg.Execute(shell="sh", command="/local/repository/install_scripts/install3.sh"))
        routers[3].addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install_scripts/install2.sh"))
        routers[3].addService(pg.Execute(shell="sh", command="/local/repository/install_scripts/install2.sh"))
    
    return routers


# begin creating request
pc = portal.Context()
request = pc.makeRequestRSpec()

# declare a dedicated VM host
pnode = request.RawPC('pnode')
pnode.hardware_type = GLOBALS.PNODE_D740

# create nodes on dedicated host
nodes = create_nodes(count=params.node_count, prefix=1)
routers = create_routers()

#setup LANs
if params.router_count == 3:
    LAN = request.LAN("LAN1")
    LAN.addInterface(routers[1].addInterface())
    if nodes[1] is not None:
        LAN.addInterface(nodes[1].addInterface())

    for i in range(2, params.node_count + 1):
        lan = "LAN" + str(i)
        LAN = request.LAN(lan)
        LAN.addInterface(routers[2].addInterface())
        if nodes[i] is not None:
            LAN.addInterface(nodes[i].addInterface())
else:
    for i in range(1, params.node_count + 1):
        lan = "LAN" + str(i)
        LAN = request.LAN(lan)
        LAN.addInterface(routers[1].addInterface())
        if nodes[i] is not None:
            LAN.addInterface(nodes[i].addInterface())


# setup a link between routers
if params.router_count > 1:
    for i in range(1, params.router_count):
        request.Link(members=[routers[i], routers[i + 1]])

# output request
pc.printRequestRSpec(request)
