#Python script that takes in a list of times stamps and returns a list of seconds

import os
import sys
import getopt
import dateutil.parser as dp
from datetime import datetime

timelist = []

with open('data_collection/temp3_timed_data.dat', 'r') as temp:
	for line in temp:
		for word in line.split():
			if "2020" in word and "T" in word:
				timelist.append(word)
newlist = []
for item in timelist:
	parsed_temp = dp.parse(item)
	t_in_seconds = parsed_temp.strftime('%s')
	newlist.append(t_in_seconds)

with open('data_collection/temp4_timed_data.dat', 'a') as temp:
	for item in newlist:
		temp.write(f"{item}\n")
