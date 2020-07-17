import time
from pyndn import Name
from pyndn import Face
from pyndn import Interest
from pyndn.transport import UdpTransport
from pyndn.security import KeyChain
from datetime import datetime

class Counter():
    
    def __init__(self):
        self._callbackCount = 0
    
    def onData(self, interest, data):
        time = datetime.now()
        self._callbackCount += 1
        dump("Got data packet with name", data.getName().toUri())
        dump(f"<<{time}<<\n", data.getContent().toRawStr()) 
        

    def onTimeout(self, interest):
        time = datetime.now()
        self._callbackCount += 1
        dump("Time out for interest", interest.getName().toUri())
        dump(f"<<{time}\n")


    def onNetworkNack(self, interest, networkNack):
        time = datetime.now()
        self._callbackCount += 1
        dump("Network nack for interest", interest.getName().toUri())
        dump(f"<<{time}<<\n")


def dump(*list):
    """Prints all parameters"""

    result = ""
    for element in list:
        result += (element if type(element) is str else str(element)) + " "
    with open('stats_file.txt', 'a') as output:    
        output.write(f"{result}\n")
