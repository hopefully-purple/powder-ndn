#Temporary setup just to get interface connections

from fabric import Connection
import os

def create_faces():
    """Creates the relevant UDP faces between routers"""
    #connection['up-cl'].run('nfdc face create udp4://10.10.3.2')
    #connection['up-cl'].run('nfdc face create udp4://10.10.2.2')
    os.system('nfdc face create udp4://10.10.2.1')
    os.system('nfdc face create udp4://10.10.2.2')



