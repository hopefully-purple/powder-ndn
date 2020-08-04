#This will be the host data script for the routers. It would be best in the end to make it in python. 

import os
import subprocess
import random
import time
from datetime import datetime

def read_file(requests):
	
	data_list = []

	with open('code/whole_dict.txt', 'r') as alice:
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

	os.system("echo "" > data_collection/echo_times.txt")

	for data in data_list:
		prefix = "/ndn/dictionary/" + data
		os.system(f"echo {data} | ndnpoke {prefix} &")
		time = datetime.now()
		with open('data_collection/echo_times.txt', 'a') as times:
			times.write(f"{prefix}\t {time}\n")


def main():

	#begin ndndump
	os.system("sudo ndndump -i any -v > data_collection/ndndump.txt &")
	
	#clarify what files are being used for what.
	print("This script will host random data under random prefixes from whole_dict.txt") #will move on to dictionary when ready for hardcore

	#ask for settings
	requests = input("How many satisfiable requests per repetition?: ")
	requests = int(requests)

	#Prep list
	req_list = read_file(requests)

	#Begin when ready
	ready = input("Hit enter when ready . . .")

	print("On 10, start requesting")
	#Begin timer
	for number in range(1,10):
		if number != 10:
			print(f"{number}")
			time.sleep(1)
		else:
			print("GO!\n")
	#Start the test
	os.system("./code/run_status_show.sh &")
	print("Just called run")
		
	#call host algorithm
	host(req_list)
	time.sleep(61)
	print("DONE")


main()
