# This python script is for a VM node in a NDN network that is acting as a client. 

import math
import time
import re
import random
import os
import string
from make_requests import MakeRequests
from datetime import datetime

class Control():
    """This class holds settings and algorithms for the Control Case"""
    def __init__(self, reqs, repits):
        self.total_reqs = int(reqs)
        self.reps = int(repits)
        self.list = []
        self.requests = []

    def read_file(self):
        """Reads file and stores each word in a list. Only stores the specified number of requests"""
        print("Reading File")

        # Open nlsr.conf and read in specified number of words
        with open('whole_dict.txt', 'r') as input_file:
            print("successfully opened file")
            num = 0
            for line in input_file:
                for word in line.split():
                    if num < self.total_reqs:
                        num += 1
                        self.list.append(word)
                    else:
                        break
        return 0

    def generate_request_strings(self):
        """Takes the list of words and adds the prefix to them"""

        for item in self.list:
            request = "/ndn/" + item
            self.requests.append(request)

        print("Size of Request List: ", len(self.requests))        

        return 0

    def send_request(self, request, i, req_num):
        """Uses PyNDN to send a single request"""

        i += 1
        with open('data_collection/stats_file.txt', 'a') as output_file:
            output_file.write(f"Rep #{i} Req #{req_num} ")
            nl_req = request + "\n"
            output_file.write(nl_req)
       
        make = MakeRequests()
        make.run_reqs(request)

        return 0

    def generate_random(self, length):
        """Creates a random string"""

        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))

        return result_str


    def test(self):
        """ Send requests, and repeat it accordingly"""
        # Read the given(?) file
        self.read_file()
        
        # Generate requests with list of strings
        self.generate_request_strings()

        #Create new in.dat and out.dat file
        with open('data_collection/in.dat', 'w') as infile:
            pass
        with open('data_collection/out.dat', 'w') as outfile:
            pass

        #Give host script a chance
        time.sleep(1)
        
        req_num = 0

        # Loop for the number of repetitions
        print("Sending requests")
        start = datetime.now()
        for i in range(0, self.reps):
            print(f"Repetition #{i + 1} {datetime.now()}\n")
            # Send specified number of requests
            for request in self.requests:
                req_num += 1
                self.send_request(request, i, req_num)
            req_num = 0

        return start

    def attack(self):
        """ ATTACK """
        make = MakeRequests()

        self.total_reqs = 5000

        #This will result in out.dat and in.dat population, as well as stats_file
        for i in range(1, self.total_reqs):
            if self.total_reqs % i == 0:
                print(f"{i} repetition {datetime.now()}")
                with open ('data_collection/terminal_output.txt', 'w') as term:
                    term.write(f"{i} repetition {datetime.now()}\n")
            randstring = self.generate_random(15)
            make.run_reqs(randstring)


        





