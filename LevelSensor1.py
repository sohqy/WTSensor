# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 20:53:52 2021

@author: sohqi
"""

from time import time 
from time import sleep
from serial import Serial

def measure(portName):
    ser = Serial(portName, 9600, 8, 'N', 1, timeout=1)
    timeStart = time()
    valueCount = 0

    while time() < timeStart + maxwait:
        if ser.inWaiting():
            bytesToRead = ser.inWaiting()
            valueCount += 1
            if valueCount < 2: # 1st reading may be partial number; throw it out
                continue
            testData = ser.read(bytesToRead)
            if not testData.startswith(b'R'):
                # data received did not start with R
                continue
            try:
                sensorData = testData.decode('utf-8').lstrip('R')
            except UnicodeDecodeError:
                # data received could not be decoded properly
                continue
            try:
                mm = int(sensorData)
            except ValueError:
                # value is not a number
                continue
            ser.close()
            return(mm)

    ser.close()
    raise RuntimeError("Expected serial data not received")

#%% 
serialDevice = "/dev/ttyAMA0" # default for RaspberryPi
maxwait = 3 # seconds to try for a good reading before quitting

maxRange = 10000
sleepTime = 5

while True:  # Needs to calculate water level from height installed     
    mm = measure(serialDevice)
    if mm >= maxRange:
        print('No Target')
    
    print('Distance: ' + mm)
