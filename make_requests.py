import time
from pyndn import Name
from pyndn import Face
from pyndn import Interest
from pyndn.transport import UdpTransport
from pyndn.security import KeyChain
from counter import Counter

def dump(*list):
    """Prints all parameters"""

    result = ""
    for element in list:
        result += (element if type(element) is str else str(element)) + " "
    with open('stats_file.txt', 'a') as output:    
        output.write(f"{result}\n")
    


class MakeRequests():
    """This class makes requests to an NDN router using PyNDN"""

    def __init__(self):
        self.something = 0

    def run_reqs(self, request):
        # silence the warning from interest wire encode
        Interest.setDefaultCanBePrefix(True)

        # set up a face that connects to the remote forwarder
        udp_connection_info = UdpTransport.ConnectionInfo("10.10.1.1", 6363)
        udp_transport = UdpTransport()
        face = Face(udp_transport, udp_connection_info)

        #  face.setCommandSigningInfo(KeyChain(), certificateName)
        #  face.registerPrefix(Name("/ndn"), onInterest, onRegisterFailed)

        counter = Counter()

        # try to fetch from provided name
        #name_text = input("Enter a name to request content from: ")
        name = Name(request)
        dump("Express name", name.toUri())

        # face.expressInterest(name, counter.onData, counter.onTimeout, counter.onNetworkNack)
        interest = Interest(name)
        interest.setMustBeFresh(False)
        face.expressInterest(interest, counter.onData, counter.onTimeout, counter.onNetworkNack)
        
        # try to fetch anything
        #  name2 = Name("/")
        #  dump("Express name", name2.toUri())
        #  face.expressInterest(name2, counter.onData, counter.onTimeout, counter.onNetworkNack)

        while counter._callbackCount < 1:
            face.processEvents()

            # don't use 100% of the CPU
            time.sleep(0.01)

        face.shutdown()
        



