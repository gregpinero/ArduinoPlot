# Arduino Plot

Script to show a plot of numeric data sent to serial port (set up for com4 right now, change in the code if neded).

![Arduino Monitor example screen](arduino_plot_screenshot.PNG)

## How to run

To use, simply run command below in the command line.

````bash
$ python wx_mpl_dynamic_graph.py
````

**Note:** Make sure you have your Arduino IDE closed, or it will block other programs like this one from using the serial port.

## Requirements

Install the following packages to run `Arduino Plot`:

* Python 2.6 (2.5 should probably work too)
* pyserial
* wx
* matplotlib
* numpy
* pylab