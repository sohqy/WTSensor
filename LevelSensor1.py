# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 20:53:52 2021

@author: sohqi
"""

import time 
from serial import Serial

MaxWait = 3 # seconds to try for a good reading before quitting

def Measure(portName):
    ser = Serial(portName, 9600, 8, 'N', 1, timeout=1)
    timeStart = time.time()
    valueCount = 0

    while time.time() < timeStart + maxwait:
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

def WriteData(CurrentReading):
    File = open('LevelSensorData.csv', 'a')
    File.write(CurrentReading)
    File.close()
    
def SendData(CurrentReading):
    print('Data Sent' + CurrentReading)

#%% 
serialDevice = "/dev/ttyAMA0" # default for RaspberryPi

MaxRange = 10000
ReadInterval = 60
SensorHeight = 200

while True:  # Needs to calculate water level from height installed     
    start_time = time.time()
    
    while time.time() - start_time <= ReadInterval:
        MeasuredDistance = Measure(serialDevice)
        if MeasuredDistance >= MaxRange:
            Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))) + ', ' + 'NaN' + '\n'
            print('No Target')
        else:
            Level = SensorHeight - MeasuredDistance
            Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))) + ', ' + str(Level) + '\n'
        WriteData(Reading)
        SendData(Reading)
        time.sleep(ReadInterval)
        print(Reading)
    
    

