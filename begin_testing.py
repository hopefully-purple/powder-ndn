import math
import os
import time
from control import Control
from datetime import datetime
from convert_time import Convert

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
        con = Convert(requs, repets)
        con.setup()
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
    with open('stats.file.txt', 'w') as stats:
        stats.write("ATTACK RUN 5,000")

    print("Beginning attack protocol.")
    print(datetime.now())
    
    ctrl.attack()
    
    print("Attack Complete")
    print(datetime.now())

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
        con = Convert(ctrol.total_reqs, ctrl.reps)
        con.setup()


main()
