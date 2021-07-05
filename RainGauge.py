""" 
RAINGAUGE DATA LOGGING SCRIPT 
=============================
PRONAMIC Rain-O-Matic Pro, PCB 9601, Single reed switch.

Created by Qiao Yan Soh 11 Mar 2021
Last updated 5 July 2021

"""

from gpiozero import Button 
import time 

sensor = Button(5) 		# Spoon is connected to RPi GPIO 5 (Pin 29)
Spoonsize = 0.2			# Manufacturer information 
count = 0               # Initialize counter
interval = 300 			# Seconds

# ----- Set up storage file
File = open('RainGaugeData.csv', 'a')
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
	File = open('RainGaugeData.csv', 'a')
	File.write(CurrentReading)
	File.close()
	
def SendData(CurrentReading):
	print('Data Sent: ' + CurrentReading)
	
# ========== 
sensor.when_pressed = Tip

time.sleep(60 - time.localtime().tm_sec) # Wait to start on the minute. TO BE CHANGED

while True:         # Run forever   
    ResetCount()
    Rainfall = count * Spoonsize
    Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))) + ', ' + '{:.1f}'.format(Rainfall) + '\n'
    WriteData(Reading)
    SendData(Reading)
    time.sleep(interval)

