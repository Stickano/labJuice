#!/usr/bin/python2

import getopt
import os
import sys
import time
import u12

# A couple of random variables used throughout
output  = None
wrong   = "Something went wrong! "

chn = False
out = False
inp = False
dig = False
ana = False

# Initialize the u12 function library model
try:
    device  = u12.U12()
except Exception as eRR:
    print eRR
    sys.exit()

# This whole function is legacy code.
# It will keep the application running in the terminal.
def loop():

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


# ----------------------------------------------------------
# Below here is v2 of this application. Above is legacy.
# It is much easier to handle this scripts functionality
# by parsing parameters directly via the command-line,
# which this second version allows for.
#


# CLI usage
def usage():
    print "LabJuice - Control Application for LabJack U12 Acquisition Board"
    print
    print "Use with: labjuice.py -c=CHANNEL [-h] [-a] [-d] [-in] [-out=VOLT] [-l]"
    print "  % Chose either the digital or the analog parameter."
    print "  % Chose either the input or output parameter."
    print "-h --help        Show this message."
    print "-l --loop        This is legacy functionality. ~"
    print "                 ~ Opens, and keeps running, an application with different controls."
    print "-a --analog      Select the analog ports."
    print "-d --digital     Select the digital ports."
    print "-i --input       Read the input value from a channel."
    print "-o --output      Set the output voltage of a channel."
    print "-c --channel     Which channel to interact with."
    print "     % Digital Channels:"
    print "     %     Channel: 0-3 for IO."
    print "     %     Channel: 0-7 for AI."
    print "     % Analog Channels:"
    print "     %     Channel: 0-1 for AO."
    print "     %     Channel: 0-7 for AI."
    print
    print "Usage examples:"
    print "Read AI2 (analog) input: labjuice.py -a -c=2 -in"
    print "Set 5V to AO0 (analog) output: labjuice.py -a -c=0 -out=5"
    print

# This will determine if the script is satisfied with the parameters given
def checkOpt():
    global chn
    global out
    global inp
    global dig
    global ana

    if not ana and not dig:
        assert False, "Use --help for more information: Select either analog or digital with -a and -d"
    if not inp and not out:
        assert False, "Use --help for more information: Read the input or set the output with -i and -o"
    if float(chn) < 0 or float(chn) > 7:
        assert False, "Use --help for more information: Select which channel to read or write to with -c"

    try:
        float(out)
    except:
        assert False, "Use --help for more information: Use a numeric value for --output"



# Reads and prints the input from the U12
def readInput():
    global chn
    global ana

    if ana:
        print device.eAnalogIn(channel=float(chn), gain=0)
    else:
        print device.eDigitalIn(channel=float(chn), readD=0)
    sys.exit()


# Sets the output for a channel on the U12
def setOutput():
    global chn
    global out
    global ana

    if ana:
        if out > 5:
            out = 5

        ao0 = 0
        ao1 = 0
        if chn == 0:
            ao0 = out
        else:
            ao1 = out

        result = device.eAnalogOut(analogOut0=ao0, analogOut1=ao1)
        print "Output voltage for Analog["+ str(result["idnum"]) +"] set to : " + str(out)

    else:
        result = device.eDigitalOut(channel=int(chn), state=float(out), writeD=1)
        print "Output voltage for Digital["+ str(result["idnum"]) +"] set to : " + str(out)
    sys.exit()


# This is the function that will be run when the script is initialized
def main():

    global chn
    global out
    global inp
    global dig
    global ana

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hladio:c:", ["help", "loop", "analog", "digital", "input", "output", "channel"]);
    except getopt.GetoptError as eRR:
        print str(eRR);
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-l", "--loop"):
            loop()
        elif o in ("-a", "--analog"):
            ana = True
        elif o in ("-d", "--digital"):
            dig = True
        elif o in ("-i", "--input"):
            inp = True
        elif o in ("-o", "--output"):
            out = a[1:]
        elif o in ("-c", "--channel"):
            chn = a[1:]

    try:
        checkOpt()
    except AssertionError as eRR:
        print eRR

    if inp:
        readInput()
    else:
        setOutput()


main()