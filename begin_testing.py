import math
import time
from control import Control

def questions():
    """ Function that asks the user questions about the setup for the test"""

    # String that stores whether the user wants the control case or the victim case
    control_or_victim = input("Control Case or Victim?(c/v): ")
    # String that stores whether the user wants to adjust the settings or not.
    adjust_settings = input("Adjust settings?(y/n): ")

    if adjust_settings == "y" and control_or_victim == "c":
        ctrl = Control(100, 15)
        print("Total Number of Requests per Repetition =", ctrl.total_reqs, ": ")
       #if number != "":
       #    ctrl.total_reqs = number
        print("Number of Repetitions =", ctrl.reps, ": ")    
    return control_or_victim


def main():
    # Start by asking the user set up questions
    case = questions()
    
    # Begin running user specified case
    if case == "c":
        ctrl = Control(100, 15) #gack this could pose a problem!
        print("Call control algorithm")
        ctrl.test()
        print("Done!")
    elif case == "v":
        print("That poor poor victim")

    again = input("Run again?(y/n):")
    if again == "y":
        main()
    elif again == "n":
        print("Peace out")


main()
