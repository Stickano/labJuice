#!/usr/bin/python2

import u12
import time

# Used during TS
import sys
print sys.path

# Initialize the u12 function library model
device  = u12.U12(debug=True)
output  = NULL

# Usage documentation
def usage();
    print "LabJuice - Controll Application for LabJack U12 Acquisition Board"
    print
    print "digital [channel] [in/out[=V]] -- Reads, or sets, the digital input and output."
    print "analog  [channel] [in/out[=V]] -- Reads, or sets, the analog  input and output."

# Run the program in a loop
while True:

    usage()
    if output != NULL:
        print "\r\n" + output + "\r\n"


    userInput = raw_input("$ ~> ")
    userInput = userInput.split(" ")

    if len(userInput) != 3:
        output = "Something went wrong! Expecting 3 parameters: [input] [channel] [in/out]"
        continue

    read    = userInput[0]
    channel = userInput[1]
    action  = userInput[2]

    # Handle digital requests
    if userInput[0].lower() == "digital":
        if userInput[1].lower()[:3] == "out":
