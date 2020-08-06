# This python script is for a VM node in a NDN network that is acting as a client. 

import math
import time
import re
import random
import os
import string
from code.make_requests import MakeRequests
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
        with open('code/whole_dict.txt', 'r') as input_file:
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

    def generate_request_strings(self, prefix): 
        """Takes the list of words and adds the prefix to them"""

        for item in self.list:
            request = prefix + item
            self.requests.append(request)

        print("Size of Request List: ", len(self.requests))        

        return 0

    def send_request(self, make, request, i, req_num):
        """Uses PyNDN to send a single request"""

        i += 1
        with open('data_collection/stats_file.txt', 'a') as output_file:
            output_file.write(f"Rep #{i} Req #{req_num} ")
            nl_req = request + "\n"
            output_file.write(nl_req)
       
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
        self.generate_request_strings("/ndn/dictionary/")

        #Create new in.dat and out.dat file
        with open('data_collection/in.dat', 'w') as infile:
            pass
        with open('data_collection/out.dat', 'w') as outfile:
            pass

        #Give host script a chance
        time.sleep(1)
        req_num = 0

        make = MakeRequests()

        # Loop for the number of repetitions
        print("Sending requests")
        start = datetime.now()
        for i in range(0, self.reps):
            print(f"Repetition #{i + 1} {datetime.now()}\n")
            # Send specified number of requests
            for request in self.requests:
                req_num += 1
                self.send_request(make, request, i, req_num)
            req_num = 0
            time.sleep(1)

        return start

    def attack(self):
        """ ATTACK """
        make = MakeRequests()

        self.total_reqs = 1700


        #Create a badlist of strings with /ndn/attack/<rand>
        bad_list = []
        for i in range(0, self.total_reqs):
            randstring = self.generate_random(15)
            badreq = "/ndn/dictionary/" + randstring
            bad_list.append(badreq)


        print(datetime.now())

        #This will result in out.dat and in.dat population, as well as stats_file
        i = 0
        for badreq in bad_list:
            i += 1
            if i % 100 == 0:
                print(f"{i} request {datetime.now()}")
                with open ('data_collection/terminal_output.txt', 'w') as term:
                    term.write(f"{i} request {datetime.now()}\n")
            make.run_reqs(badreq)




