# This python script is for a VM node in a NDN network that is acting as a client. 
# There are two options for testing
# The first is the control case and the second is the victim case
# 
# The control case has a few default settings, which can be changed by the user when prompted before it begins behavior.
# Control Case:
	# Settings:
		# Total Number of Requests per Repetition
		# Number of Repetitions
		# I have an idea for two other settings, but I'm starting with this much to not get overwhelmed.
	#Functionality:
		# The idea (currently) is to take a file and put each string in an array, including duplicates to make it more realistic and decomplicate my algorithm (although this could change)
		# Then, it will take each item, add it to the /ndn/ prefix, and store it in a new array? Not very efficient . . replace each item with the prefix + item?
		# Next, it will enter a loop, and for each item in the array, it will send a request/Interest Packet. Now here is the tricky part.
			# I need to figure out how best to time the router response. Investigate the PyNDN tools that are already there, or try to extract the timestamps from the IP and DP
		# Once the result from the interest comes, add the timestamp and other information to the stats_file.txt
		# Loop to the next item.
		# Once that loop is done, repeat the that previous loop for the given amount of repetitions, making sure there is a separation in the stats_file.txt
			# This makes me nervous, because at this point the router should have all of these requests in the CS, which means the response time will be faster. 
			# I also need to decide if I'm going to involve another router, and mix up which one hosts what data. 
			# I feel that if I want this control case to work properly, these CS and PIT and FIBs need to be wiped clean. 
			# I guess I could turn off caching on the routers, although I feel that becomes a breach of emulating a real NDN scenario. 
		# When that is finished, store stats at the end of stats_file.txt and print completion messages.
			# stats include: reps, total requs, avg router response time
			# I'm unsure how I'll get it to do that avg math, worry when I get there
		# Ask user if they want to run it again. Start all the way from the control or victim option.

import math
import time
#from pyndn import Name
from make_requests import MakeRequests


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
        with open('random.txt', 'r') as input_file:
            print("successfully opened file")
            num = 0
            for line in input_file:
                for word in line.split():
#                   if "<" in word or ">" in word:
#                       pass
                    if num < self.total_reqs:
                        num += 1
                        self.list.append(word)
                    else:
                        break
        print("Populated list")
        return 0

    def generate_request_strings(self):
        """Takes the list of words and adds the prefix to them"""
        print("Generating requests")

        for item in self.list:
            request = "/ndn/" + item
            self.requests.append(request)

        print("Size of Request List: ", len(self.requests))        

       #with open('stats_file.txt', 'a') as output_file:
       #    for item in self.list:
       #        request = "/ndn/" + item + "\n"
       #        output_file.write(request)
        
        return 0

    def send_request(self, request, i):
        """Uses PyNDN to send a single request"""
       #print("Send a request")

        with open('stats_file.txt', 'a') as output_file:
            output_file.write(f"Rep #{i}")
            nl_req = request + "\n"
            output_file.write(nl_req)
            print(f"|{request}|")            
       
        make = MakeRequests()
        make.run_reqs(request)

        return 0

    def test(self):
        """ Send requests, and repeat it accordingly"""
        # Read the given(?) file
        self.read_file()
        
        # Generate requests with list of strings
        self.generate_request_strings()

        # Loop for the number of repetitions
        print("Sending requests")
        for i in range(0, self.reps):
            print(f"Repition #{i}\n")
            # Send specified number of requests
            for request in self.requests:
                self.send_request(request, i)


