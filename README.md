# labJuice
Controll Application for LabJack U12 Acquisition Board

&nbsp;

# Usage
This application does not bring much value to be honest. It allows you to set and get the inputs & outputs (I/O) of a LabJack U12 acquisition board.

### CLI
Invoke this script with parameters to read and set the IO ports/channels. 
```
LabJuice - Control Application for LabJack U12 Acquisition Board

Use with: labjuice.py -c=CHANNEL [-h] [-a] [-d] [-in] [-out=VOLT] [-l]
  % Chose either the digital or the analog parameter.
  % Chose either the input or output parameter.
-h --help        Show this message.
-l --loop        This is legacy functionality. ~
                 ~ Opens, and keeps running, an application with different controls.
-a --analog      Select the analog ports.
-d --digital     Select the digital ports.
-i --input       Read the input value from a channel.
-o --output      Set the output voltage of a channel.
-c --channel     Which channel to interact with.
     % Digital Channels:
     %     Channel: 0-3 for IO.
     %     Channel: 0-7 for AI.
     % Analog Channels:
     %     Channel: 0-1 for AO.
     %     Channel: 0-7 for AI.

Usage examples:
Read AI2 (analog) input: labjuice.py -a -c=2 -in
Set 5V to AO0 (analog) output: labjuice.py -a -c=0 -out=5
```

### Loop 
This is the legacy way of running this application - In a constant loop. It has a custom CLI. Pretty useless. 
```
LabJuice - Control Application for LabJack U12 Acquisition Board

Usage:
digital [channel] [in/out=V] -- Reads, or sets, the digital input and output.
     Channel: 0-3 for IO
     Channel: 0-7 for AI
analog  [channel] [in/out=V] -- Reads, or sets, the analog  input and output.
     Channel: 0-1 for AO
     Channel: 0-7 for AI


Input voltage for Analog[0]: 5.048828125

$ ~> 
```

&nbsp;

# Driver, library and Python module installation
We will be installing LabJack’s function library and driver on our glorious Linux system.

You can download the (required) Exodriver from LabJack’s own website. Same goes for the function library. 

https://labjack.com/support/software/installers/u12

https://labjack.com/support/software/installers/exodriver

### Exodriver
Extract the Exodriver, navigate to its folder and build the driver with help of the included shell script:
```
$ sudo ./install.sh
```

Then install the example programs:
```
$ cd examples/U12/
$ make 
```

Connect the LabJack and run the example program with:
```
$ ./u12AISample
```

Be aware that the U12 will not accept the first command right after being plugged into the computer, so the above command might have to fired twice before you’ll get an response. 


### Function Library
For the library, extract and navigate to the libljacklm/ folder. Edit the Makefile as described in the INSTALL file (one folder up).
```
$ vim Makefile
```
```
...
ARCHFLAGS = -arch i386 -arch x86_64
# Build for only the host architecture
#ARCHFLAGS =
```

And build the package:
```
$ make clean
$ make
$ sudo make install
```

### Lastly, the Python Module
We will be playing a bit with this device through a couple of Python scripts, so be sure to catch their Python module, from their website, as well:
https://labjack.com/support/software/examples/ud/labjackpython 

Extract and navigate into the newly created LabJackPython-* directory. Run the installation:
```
$ sudo python2 setup.py install
```
