#Python script that takes in a list of times stamps and returns a list of seconds

import os
import sys
import getopt
#import dateutil.parser as dp
from datetime import datetime

timelist = []

with open('temp3_timed_data.dat', 'r') as temp:
	for line in temp:
		for word in line.split():
			if "2020" in word:
				timelist.append(word)
newlist = []
for item in timelist:
	temp = datetime.parse(item)
	print(temp)
	
