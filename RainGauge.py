""" 
RAINGAUGE DATA LOGGING SCRIPT 
=============================
PRONAMIC Rain-O-Matic Pro, PCB 9601, Single reed switch.

All-inclusive script for local data collection of the raingauge. 
----- INITIALISATION OPTIONS: 
    - Start time wait
    - Read interval

----- INDICATOR OVERVIEW:
    - Script initialized: Yellow LED blinks 5 times.
    - Infinite loop is running: Green LED slow blink.
    - Data is writing: Red LED on.

Created by Qiao Yan Soh 11 Mar 2021
Last updated 12 May 2022

"""

from gpiozero import Button 
from gpiozero import LED
import time 

# ----- INDICATOR SET UP
Red = LED(22)
Yellow = LED(27)
Green = LED(17)

Yellow.blink(on_time = 0.5, off_time = 0.5, n = 5)  # Script initialised

# ----- SENSOR SET UP 
sensor = Button(5) 		# Spoon is connected to RPi GPIO 5 (Pin 29)
Spoonsize = 0.2			# Manufacturer information 
count = 0               # Initialize counter
interval = 300 			# Seconds

# ----- Set up storage file
def NewFile(Date):
	fname = 'RainGaugeData' + Date + '.csv' 
	File = open(fname, 'a')
	File.write('Datetime, Rainfall \n')
	File.close()
	
# ----- Functions 
def Tip():
	global count
	count += 1
	
def ResetCount():
	global count
	count = 0
	
def WriteData(CurrentReading):
	Red.on()
	fname = 'RainGaugeData' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.csv'
	File = open(fname, 'a')
	File.write(CurrentReading)
	File.close()
	Red.off()
	
# ==========
sensor.when_pressed = Tip

time.sleep(60 - time.localtime().tm_sec)
Next = time.time()
ResetCount()
Green.blink(on_time = 2, off_time = 58)

while True:         # Run forever
	Date = str(time.strftime('%Y-%m-%d', time.localtime(Next)))
	if (time.localtime(Next).tm_hour == 0) & (time.localtime(Next).tm_min == 0):
		NewFile(Date)
	Next += interval
	time.sleep(Next - time.time())
	Rainfall = count * Spoonsize
	ResetCount()
	Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + ',' + '{:.1f}'.format(Rainfall)
	WriteData(Reading)
