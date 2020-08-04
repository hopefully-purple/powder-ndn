import time
import os
from pyndn import Name
from pyndn import Face
from pyndn import Interest
from pyndn.transport import UdpTransport
from pyndn.security import KeyChain
from code.counter import Counter
from datetime import datetime

def dump(*list):
    """Prints all parameters"""

    result = ""
    for element in list:
        result += (element if type(element) is str else str(element)) + " "
    with open('data_collection/stats_file.txt', 'a') as output:    
        output.write(f"{result}\n")
    


class MakeRequests():
    """This class makes requests to an NDN router using PyNDN"""

    def __init__(self):
        self.something = 0

    def run_reqs(self, request):
        # silence the warning from interest wire encode
        Interest.setDefaultCanBePrefix(True)

        # set up a face that connects to the remote forwarder
        #udp_connection_info = UdpTransport.ConnectionInfo("10.10.1.1", 6363)
        #udp_connection_info = UdpTransport.ConnectionInfo("10.10.2.1", 6363)
        #udp_connection_info = UdpTransport.ConnectionInfo("10.10.3.1", 6363)
        #udp_connection_info = UdpTransport.ConnectionInfo("10.10.4.1", 6363)
        #udp_connection_info = UdpTransport.ConnectionInfo("10.10.5.1", 6363)
        udp_transport = UdpTransport()
        face = Face(udp_transport, udp_connection_info)


        counter = Counter()

        # try to fetch from provided name
        name = Name(request)
        dump("Express name", name.toUri())

        interest = Interest(name)
        interest.setMustBeFresh(False)
        date = datetime.now()
        face.expressInterest(interest, counter.onData, counter.onTimeout, counter.onNetworkNack)
        dump(f">>{date}>>")

        with open('data_collection/out.dat', 'a') as outfile:
            outfile.write(f"{date}\n")

        while counter._callbackCount < 1:
            face.processEvents()

            # don't use 100% of the CPU
            time.sleep(0.01)

        face.shutdown()
        



