import math
import os
import time
from control import Control
from datetime import datetime

def questions(ctrl):
    """ Function that asks the user questions about the setup for the test"""

    # String that stores whether the user wants the control case or the victim case
    control_or_victim = input("Control Case or Victim or Attacker?(c/v/a/p): ")

    if control_or_victim == "v":
        victim()
        return control_or_victim
    elif control_or_victim == "a":
        return control_or_victim
    elif control_or_victim == "p":
        requs = input("requests = ")
        repets = input("repetitions = ")
        plot(requs, repets)
        return control_or_victim

    num_reqs = input(f"Total Number of Requests per Repetition = {ctrl.total_reqs} : ")
    if num_reqs != "":
        ctrl.total_reqs = int(num_reqs) 
    num_reps = input(f"Number of Repetitions = {ctrl.reps} : ")
    if num_reps != "":
        ctrl.reps = int(num_reps)    
    
    wipe = input("Wipe stats_file?(y/n):")
        
    if wipe == "y":
        with open('stats_file.txt', 'w') as stats:
            stats.write("A clean slate!\n") #Eventually print out the settings
            stats.write(f"Requests per Rep: {ctrl.total_reqs}\t Total Reps: {ctrl.reps}\n")
            stats.write("CONTROL CASE\n")
    elif wipe == "n":
        with open('stats_file.txt', 'a') as stats:
            stats.write("\n ANOTHER RUN\n")
            stats.write(f"Requests per Rep: {ctrl.total_reqs}\t Total Reps: {ctrl.reps}\n")
            
    ready = input("Hit enter when ready . . .")
    
    if ready == "":
        return control_or_victim
    else:
        return "empty"
    
    #return control_or_victim

def victim():
    print("GACK")

def attacker(ctrl):
    print("Attack protocol will populate the same files as a regular use case.")
    print("Beginning attack protocol.")
    print(datetime.now())
    ctrl.attack()
    print("Attack Complete")

def plot(reqs, reps):

    #Create temp files
    with open('temp_out.dat', 'w') as temp:
        pass
    with open('temp_in.dat', 'w') as temp:
        pass
    with open('temp_outin.dat', 'w') as temp:
        pass
    with open('outin.dat', 'w') as outin:
        pass

    #Take off the first 18 characters of the in.dat and out.dat to get rid of unwanted date info
    os.system("cat in.dat | cut -c 21- > temp_out.dat")
    os.system("cat out.dat | cut -c 21- > temp_in.dat")

    #Put both data into two columns in the same file 
    os.system("paste temp_out.dat temp_in.dat | awk '{$3=\"\"; print > \"temp_outin.dat\"}'")

    results = []
    #calculate the difference and store in results
    with open('temp_outin.dat', 'r') as outin:
        for line in outin:
            data = line.split()
            result = int(data[0]) - int(data[1])
            results.append(result)

    with open('temp_results.dat', 'w') as temp:
        for number in results:
            temp.write(f"{number}\n")

    #put results list in a temp file
    with open('results.dat', 'w') as temp:
        i = 0 #Keeps track of line number
        j = 1 #Keeps track of repetitions
        temp.write(f"Repetition #{j}\n")
        for number in results:
            i+= 1
            temp.write(f"{number}\n")
            if i == reqs and j != reps:
                j += 1
                temp.write("\n\n")#Skip two lines and reset i
                temp.write(f"Repetition #{j}\n")
                i = 0

    #add the column to the outin.dat
    os.system("paste temp_outin.dat temp_results.dat | awk '{$4=\"\"; print > \"outin.dat\"}'")

    #Call gnuplot script
    os.system(f"gnuplot -persist -c \"analyze_outin.gnuplot\" \"{reqs} per rep; {reps} repetitions\" \"{reqs}\"")
    os.system("display plot_outin_data.png")

    #Clean up extra files
    os.system("rm temp_in.dat temp_out.dat temp_results.dat temp_outin.dat")

def main():
    
    ctrl = Control(100, 15)

    # Start by asking the user set up questions
    case = questions(ctrl)
    
    # Begin running user specified case
    if case == "c":
        #ctrl = Control(100, 15) #gack this could pose a problem!
        print("Call control algorithm")
        ctrl.test()
        print(f"Done! {datetime.now()}")
    elif case == "v":
        print("That poor poor victim")
    elif case == "a":
        attacker(ctrl)

    again = input("Run again?(y/ys/n/p):")
    if again == "y":
        main()
    elif again == "ys":
        questions(ctrl)
        ctrl.test()
        print("Done!")
    elif again == "n":
        print("Peace out")
    elif again == "p":
        plot(ctrl.total_reqs, ctrl.reps)


main()
