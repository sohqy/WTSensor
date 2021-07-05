# -*- coding: utf-8 -*-
"""
UWHS LEVEL SENSOR DATA LOGGING SCRIPT 
=============================
MaxBotix MB7366, Serial Output. 

Created by Qiao Yan Soh 11 Mar 2021
Last updated 5 July 2021
"""

import time 
from serial import Serial

MaxWait = 3     # Number of seconds to wait for reading

def Measure(portName):  
    ser = Serial(portName, 9600, 8, 'N', 1, timeout=1)
    timeStart = time.time()
    valueCount = 0

    while time.time() < timeStart + MaxWait:
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
serialDevice = "/dev/ttyAMA0"   # default for RaspberryPi

MaxRange = 10000        # Outputs in mm.
SensorHeight = 2000     # mm. TO BE ADJUSTED ACCORDINGLY

ReadInterval = 60       # Seconds

# ----- Set up storage file 
File = open('LevelSensorData.csv', 'a')
File.write('Datetime, Water Level \n')
File.close()

time.sleep(60 - time.localtime().tm_sec)   # Wait to start on the minute

while True:          
    MeasuredDistance = Measure(serialDevice)
    MeasureTime = time.time()
    if MeasuredDistance >= MaxRange:
        Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(MeasureTime))) + ', ' + 'NaN' + '\n'
    else:
        Level = SensorHeight - MeasuredDistance
        Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(MeasureTime))) + ', ' + str(Level) + '\n'
    WriteData(Reading)
    SendData(Reading)
    time.sleep(ReadInterval)    # Wait.

    
    

