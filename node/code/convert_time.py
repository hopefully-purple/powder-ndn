#Python script for converting time to seconds

import os
import sys
import getopt
import dateutil.parser as dp
from datetime import datetime

class Convert():
    """This class converts time from in and out files into total seconds"""

    def __init__(self, requs, repes, sta, sto):
        self.reqs = int(requs)
        self.reps = int(repes)
        self.start = sta
        self.stop = sto

    def convert(self):
        otimelist = []
        itimelist = []
        #Take the out and in files, convert each time into seconds, populate corresponding lists
        with open('data_collection/out.dat', 'r') as out:
            for line in out:
                otimelist.append(line)

        with open('data_collection/in.dat', 'r') as infile:
            for line in infile:
                itimelist.append(line)
        
        #print these lists into temp files, reformatting with rep separations
        self.datasetformat(otimelist, "data_collection/temp_out.dat")
        self.datasetformat(itimelist, "data_collection/temp_in.dat")

    def datasetformat(self, inlist, filename):
        with open(filename, 'w') as outfile:
            i = 0 #keeps track of line number
            j = 1 #keeps track of repetitions
            outfile.write(f"Repetition #{j}\n")
            for number in inlist:
                i+= 1
                outfile.write(f"{number}\n")
                if i == self.reqs and j != self.reps:
                    j+= 1
                    outfile.write("\n\n") #skip two lines and reset i
                    outfile.write(f"Repetition #{j}\n")
                    i = 0


    def setup(self):
        #Create temp files
        with open('data_collection/temp_out.dat', 'w') as temp:
            pass
        with open('data_collection/temp_in.dat', 'w') as temp:
            pass
        with open('data_collection/temp_outin.dat', 'w') as temp:
            pass
        with open('data_collection/outin.dat', 'w') as temp:
            pass

        #call conversion method
        self.convert()
        results = []

        #put both data files into two columns of the same file
        os.system("paste data_collection/temp_out.dat data_collection/temp_in.dat | awk '{print > \"data_collection/temp_outin.dat\"}'")

        #calculate the difference and store in results
        with open('data_collection/temp_outin.dat', 'r') as outin:
            for line in outin:
                if "Rep" in line or "0" not in line:
                    continue
                else:
                    data = line.split()
                    start = data[0] + " " + data[1]
                    stop = data[2] + " " + data[3]
                    dout = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
                    din = datetime.strptime(stop, '%Y-%m-%d %H:%M:%S.%f')
                    duration = din - dout #stop - start incoming - outgoing receive - send
                    result = duration.total_seconds()
                    results.append(result)

        #Put results in results.dat
        self.datasetformat(results, "data_collection/results.dat")

        #Put results in gnustats.dat without format
        with open("data_collection/gnustats.dat", 'w') as stats:
            for number in results:
                stats.write(f"{number}\n")

        #add the column to the outin.dat
        os.system("paste data_collection/temp_outin.dat data_collection/results.dat | awk '{print > \"data_collection/outin.dat\"}'")

        #clean up extra files
        os.system("rm data_collection/temp_in.dat data_collection/temp_out.dat data_collection/temp_outin.dat")

        #Total time it took
        if type(self.start) is str:
            start = datetime.strptime(self.start, '%Y-%m-%d %H:%M:%S.%f')
            stop = datetime.strptime(self.stop, '%Y-%m-%d %H:%M:%S.%f')
        else:
            stop = self.stop
            start = self.start
        duration = stop - start
        duration_in_s = duration.total_seconds()
        total_time = divmod(duration_in_s, 60)[0]
        if total_time == 0:
            label = "{} total seconds"
            total_time = label.format(duration_in_s)
        else:
            label = "{} total minutes"
            total_time = label.format(total_time)

        with open("data_collection/gnuplotstatistics.txt", 'w') as stat:
            pass
        #call gnuplot script
        os.system(f"gnuplot -persist -c \"code/analyze_outin.gnuplot\" \"{self.reqs} requests per rep; {self.reps} repetitions; {total_time}\" \"{self.reqs}\"")
        os.system("display data_collection/plot_outin_data.png")




