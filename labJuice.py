#!/usr/bin/python2

import u12
import time
import sys
import os

# A couple of random variables used throughout
output  = None
wrong   = "Something went wrong! "

# Initialize the u12 function library model
try:
    device  = u12.U12()
except Exception as eRR:
    print eRR
    sys.exit()

# Usage documentation
def usage():
    print "LabJuice - Control Application for LabJack U12 Acquisition Board"
    print
    print "Usage:"
    print "digital [channel] [in/out=V] -- Reads, or sets, the digital input and output."
    print "     Channel: 0-3 for IO"
    print "     Channel: 0-7 for AI"
    print "analog  [channel] [in/out=V] -- Reads, or sets, the analog  input and output."
    print "     Channel: 0-1 for AO"
    print "     Channel: 0-7 for AI"
    print

# Run the program in a loop
while True:

    # Clear terminal window
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print out the usage of the program, and the response from latest command
    usage()
    if output != None:
        print "\r\n" + output + "\r\n"

    # Ask for input and split that input
    userInput = raw_input("$ ~> ")
    userInput = userInput.split(" ")

    # Confirm there is 3 input values
    if len(userInput) < 3:
        output = wrong + "Expecting 3 parameters: [input] [channel] [in/out]"
        continue

    # User-input in a nicer format
    read    = userInput[0].lower()
    action  = userInput[2].lower()

    # Check our first parameter is either digital or analog
    if read != "digital" and read != "analog":
        output = wrong + "[input] (first parameter) should be either digital or analog"
        continue

    # Check that the channel is an integer value
    try:
        channel = int(userInput[1])
    except ValueError:
        output = wrong + "[channel] should be of type int"
        continue

    # Check that third parameter is either in or out
    if action != "in" and action[:3] != "out":
        output = wrong + "[action] (third parameter) should be either in or out/out=V"
        continue

    # Checks if you're trying to set an output and checks that the value is an integer
    if action[:3] == "out":
        inp = action.split("=")
        try:
            state = int(inp[1])
        except ValueError:
            output = wrong + "[out=] value should be of type int"
            continue
        except IndexError:
            output = wrong + "[out] is missing a value"
            continue

    # Handle digital requests
    if read == "digital":

        # Read the input of the digital channel
        if action == "in":
            out    = device.eDigitalIn(channel=channel, readD=0)
            output = "Input voltage for Digital["+ str(out["idnum"]) +"]: "
            output += str(out["state"])

        # Set the output of the digital channel
        if action[:3] == "out":
            out    = device.eDigitalOut(channel=channel, state=state, writeD=1)
            output = "Output voltage for Digital["+ str(out["idnum"]) +"] set to : "
            output += str(state)

    # Handle analog requests
    if read == "analog":

        # Read the input of the digital channel
        if action == "in":

            # Make sure we are calling the correct input (range)
            if channel > 7:
                output = wrong + "[channel] should be between 0-7"
                continue

            # Set the output for next loop
            out    = device.eAnalogIn(channel=channel, gain=0)
            output = "Input voltage for Analog["+ str(out["idnum"]) +"]: "
            output += str(out["voltage"])

        # Set the output of the digital channel
        if action[:3] == "out":

            ao0 = 0
            ao1 = 0

            # Make sure we are calling the correct output (range)
            if channel > 1:
                output = wrong + "[channel] should be either 0 or 1 (AO)"
                continue

            # Max 5 V
            if state > 5:
                state = 5

            # Set the Volt for the correct output (0/1)
            if channel == 0:
                ao0 = state
            else:
                ao1 = state

            # Set the output for next loop
            out    = device.eAnalogOut(analogOut0=ao0, analogOut1=ao1)
            output = "Output voltage for Analog["+ str(out["idnum"]) +"] set to : "
            output += str(state)