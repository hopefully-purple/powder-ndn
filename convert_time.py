#Python script for converting time to seconds

import os
import sys
import getopt
import dateutil.parser as dp
from datetime import datetime

class Convert():
    """This class converts time from in and out files into total seconds"""

    def __init__(self, requs, repes):
        self.reqs = int(requs)
        self.reps = int(repes)

    def convert(self):
        otimelist = []
        itimelist = []
        #Take the out and in files, convert each time into seconds, populate corresponding lists
        with open('out.dat', 'r') as out:
            for line in out:
                parsed_temp = dp.parse(line)
                t_in_seconds = parsed_temp.strftime('%s')
                otimelist.append(t_in_seconds)

        with open('in.dat', 'r') as infile:
            for line in infile:
                parsed_temp = dp.parse(line)
                t_in_seconds = parsed_temp.strftime('%s')
                itimelist.append(t_in_seconds)
        
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
        os.system("paste temp_out.dat temp_in.dat | awk '{$3=\"\"; print > \"temp_outin.dat\"}'")

        #calculate the difference and store in results
        with open('temp_outin.dat', 'r') as outin:
            for line in outin:
                if "Rep" in line or "1" not in line:
                    continue
                else:
                    data = line.split()
                    result = float(data[0]) - float(data[1])
                    results.append(result)

        #Put results in results.dat
        self.datasetformat(results, "results.dat")

        #add the column to the outin.dat
        os.system("paste temp_outin.dat results.dat | awk '{$4=\"\"; print > \"outin.dat\"}'")

        #clean up extra files
        os.system("rm temp_in.dat temp_out.dat temp_outin.dat")

        #call gnuplot script
        os.system(f"gnuplot -persist -c \"analyze_outin.gnuplot\" \"{self.reqs} requests per rep; {self.reps} repetitions\" \"{self.reqs}\"")
        os.system("display plot_outin_data.png")




