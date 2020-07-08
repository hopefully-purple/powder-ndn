#This will be the host data script for the routers. It would be best in the end to make it in python. 

import os
import subprocess
import random

from datetime import datetime

def read_file(requests):
	
	data_list = []

	with open('alice.txt', 'r') as alice:
		num = 0
		for line in alice:
			for word in line.split():
				if num < requests:
					num += 1
					data_list.append(word)
				else:
					break

	return data_list

def host(data_list):

	for data in data_list:
		prefix = "/ndn/" + data
		os.system(f"echo {data} | ndnpoke {prefix} &")
		with open('nfdc_status.txt', 'a') as status:
			status.write("----")
			status.write(f"{prefix}\t {datetime.now()}\n")
			subprocess.Popen(['nfdc', 'status', 'show'], stdout=status)
			status.write("-")
		print(f"done echoing {prefix}\n")


def main():
	
	#clarify what files are being used for what.
	print("This script will host random data under random prefixes from alice.txt") #will move on to dictionary when ready for hardcore

	#ask for settings
	requests = input("How many satisfiable requests per repitition?:")
	requests = int(requests)

	#Begin when ready
	ready = input("Hit enter when ready . . .")

	if ready != "":
		print("Restarting")
		main()
	else:
		with open('nfdc_status.txt', 'w') as status:
			status.write(f"Beginning status at time: {datetime.now()}\n")
			subprocess.Popen(['nfdc', 'status', 'show'], stdout=status)
			status.write("---------")

		#call host algorithm
		host(read_file(requests))



main()
