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
        with open('out.dat', 'r') as out:
            for line in out:
                otimelist.append(line)
                #parsed_temp = dp.parse(line)
                #t_in_seconds = parsed_temp.strftime('%s')
                #otimelist.append(t_in_seconds)

        with open('in.dat', 'r') as infile:
            for line in infile:
                itimelist.append(line)
                #parsed_temp = dp.parse(line)
                #t_in_seconds = parsed_temp.strftime('%s')
                #itimelist.append(t_in_seconds)
        
        #print these lists into temp files, reformatting with rep separations
        self.datasetformat(otimelist, "temp_out.dat")
        self.datasetformat(itimelist, "temp_in.dat")

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
        with open('temp_out.dat', 'w') as temp:
            pass
        with open('temp_in.dat', 'w') as temp:
            pass
        with open('temp_outin.dat', 'w') as temp:
            pass
        with open('outin.dat', 'w') as temp:
            pass

        #call conversion method
        self.convert()
        results = []

        #put both data files into two columns of the same file
        os.system("paste temp_out.dat temp_in.dat | awk '{print > \"temp_outin.dat\"}'")

        #calculate the difference and store in results
        with open('temp_outin.dat', 'r') as outin:
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
                    
                    #result = abs(float(data[0]) - float(data[1]))
                    #if result == 1:
                        #result = 0
                    results.append(result)

        #Put results in results.dat
        self.datasetformat(results, "results.dat")

        #Put results in gnustats.dat without format
        with open("gnustats.dat", 'w') as stats:
            for number in results:
                stats.write(f"{number}\n")

        #add the column to the outin.dat
        os.system("paste temp_outin.dat results.dat | awk '{print > \"outin.dat\"}'")

        #clean up extra files
        os.system("rm temp_in.dat temp_out.dat temp_outin.dat")

        #Total time it took
        if type(self.start) is str:
            start = datetime.strptime(self.start, '%Y-%m-%d %H:%M:%S.%f')
            stop = datetime.strptime(self.stop, '%Y-%m-%d %H:%M:%S.%f')
        else:
            stop = self.stop
            start = self.start
        duration = stop - start
        print(duration)
        duration_in_s = duration.total_seconds()
        print(duration_in_s)
        total_time = divmod(duration_in_s, 60)[0]
        if total_time == 0:
            label = "{} total seconds"
            total_time = label.format(duration_in_s)
        else:
            label = "{} total minutes"
            total_time = label.format(total_time)
        print(total_time)

        with open("gnuplotstatistics.txt", 'w') as stat:
            pass
        #call gnuplot script
        os.system(f"gnuplot -persist -c \"analyze_outin.gnuplot\" \"{self.reqs} requests per rep; {self.reps} repetitions; {total_time}\" \"{self.reqs}\"")
        os.system("display plot_outin_data.png")




