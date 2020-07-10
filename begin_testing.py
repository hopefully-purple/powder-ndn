import math
import time
from control import Control

def questions(ctrl):
    """ Function that asks the user questions about the setup for the test"""

    # String that stores whether the user wants the control case or the victim case
    control_or_victim = input("Control Case or Victim?(c/v): ")

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
    
    ready = input("Hit enter when ready . . .")
    
    if ready == "":
        return control_or_victim
    else:
        return "a"
    
    #return control_or_victim


def main():
    
    ctrl = Control(100, 15)

    # Start by asking the user set up questions
    case = questions(ctrl)
    
    # Begin running user specified case
    if case == "c":
        #ctrl = Control(100, 15) #gack this could pose a problem!
        print("Call control algorithm")
        ctrl.test()
        print("Done!")
    elif case == "v":
        print("That poor poor victim")
    elif case == "a":
        main()

    again = input("Run again?(y/n):")
    if again == "y":
        main()
    elif again == "n":
        print("Peace out")


main()
