# -*- coding: utf-8 -*-
"""
UWHS LEVEL SENSOR DATA LOGGING SCRIPT 
=============================
MaxBotix MB7366, Serial Output. 

All-inclusive script for measuring water level in UWHS tanks. 
----- INITIALISATION OPTIONS: 
    - Start time wait
    - Read interval
    - Sensor height input (!) 

----- INDICATOR OVERVIEW:
    - Script initialized: Yellow LED blinks 5 times.
    - Infinite loop is running: Green LED slow blink.
    - Data is writing: Red LED on.

Created by Qiao Yan Soh 11 Mar 2021
Last updated 27 July 2021
"""

from gpiozero import LED
import time
import numpy as np
from serial import Serial

# ========== INDICATOR SET UP
Red = LED(26)
Yellow = LED(19)
Green = LED(13)

Yellow.blink(on_time = 0.5, off_time = 0.5, n = 5)  # Script initialised

# ========== SENSOR SET UP

MaxWait = 3     # Number of seconds to wait for reading

def Measure(portName):
    ser = Serial(portName, 9600, 8, 'N', 1, timeout=1)
    timeStart = time.time()         # Get current time
    valueCount = 0

    while time.time() < timeStart + MaxWait:
        if ser.inWaiting():             # if there are things to read
            bytesToRead = ser.inWaiting()
            valueCount += 1
            if valueCount < 2:          # 1st reading may be partial number; throw it out
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
    Red.on()
    File = open('/home/pi/Har_LevelSensorData.csv', 'a')     # Add name of tank here.
    File.write(CurrentReading)
    File.close()
    Red.off()

#%%
serialDevice = "/dev/ttyAMA0"   # default for RaspberryPi

MaxRange = 9999        # Outputs in mm.
SensorHeight = 2000     # mm. TO BE ADJUSTED ACCORDINGLY

ReadInterval = 60       # Seconds

# ----- Set up storage file 
File = open('/home/pi/Har_LevelSensorData.csv', 'a')
File.write('Datetime,Water Level\n')
File.close()

time.sleep((5 - time.localtime().tm_min%5) * 60 - time.localtime().tm_sec)   # Wait to start on the minute
Next = time.time()
Green.blink(on_time = 0.5, off_time = 60)
while True:
    Next += ReadInterval
    MeasuredDistance = []
    i = 0
    while i < 5:
        Distance = Measure(serialDevice)
        if Distance >= MaxRange:
            MeasuredDistance.append(np.nan)
        else:
            MeasuredDistance.append(Distance)
        i += 1
    #MeasuredDistance = Measure(serialDevice)
    MeasureTime = time.time()
    #if MeasuredDistance >= MaxRange:
    #    Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(MeasureTime))) + ',' + 'NaN' + '\n'
    #else:
        #Level = SensorHeight - MeasuredDistance
    #    Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(MeasureTime))) + ',' + str(MeasuredDistance) + '\n'
    Reading = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(MeasureTime))) + ',' + str(np.mean(MeasuredDistance)) + '\n'
    WriteData(Reading)
    print(Reading, MeasuredDistance)
    #time.sleep(ReadInterval)    # Wait.
    time.sleep(Next - time.time())
