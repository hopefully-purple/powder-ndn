#This will be the host data script for the routers. It would be best in the end to make it in python. 

import os
import subprocess
import random

from datetime import datetime
from numpy import random

def host(self, requests):
	
#	lines = random_lines('alice.txt')
	x = random.randint(100)

	with open('alice.txt', 'r') as alice:
		print("Opened and closed alice")


#def random_lines(file):
#	lines = open(file).read().splitlines()
#	return random.choice(lines)



def main():
	
	#clarify what files are being used for what.
	print("This script will host random data under random prefixes from alice.txt") #will move on to dictionary when ready for hardcore

	#ask for settings
	requests = input("How many satisfiable requests?:")

	#Begin when ready
	ready = input("Hit enter when ready . . .")

	if ready != "":
		print("Restarting")
		main()
	else:
		with open('nfdc_status.txt', 'w') as status:
			status.write(f"Beginning status at time: {datetime.now}\n")
			subprocess = subprocess.Popen(['nfdc', 'status', 'show'], stdout=status)

		#call host algorithm
		host(requests)



main()
