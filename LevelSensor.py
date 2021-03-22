from time import time 
from time import sleep
from serial import Serial 

SerialDevice = "/dev/ttyAMA0" 	# Serial Port on RPi
maxWaitTime = 3	                # Time window for reading a good value

def measure(PortName):
	Ser = Serial(PortName, 9600, 8, 'N', 1, timeout = 1)
    StartTime = time()
    Count = 0
    
    while time() < StartTime + maxWaitTime:
        if Ser.inWaiting():                 # Get number of bytes in receive buffer
            BytesToRead = Ser.inWaiting()
            Count += 1 
            
            if Count < 2:
                continue
            
            TestData = Ser.read(BytesToRead)
            if not TestData.startswith(b'R'):
                continue
            
            try: 
                SensorData = TestData.deconde('utf-8').lstrip('R')
            except UnicodeDecodeError:
                continue
            
            try:
                mm = int(SensorData)
            except ValueError:      # Value received is not a number 
                continue
            
            Ser.close()
            return (mm)
            
    Ser.close()
    raise RuntimeError("Expected data not received")
    
Range = 10000
SleepTime = 5
minMM = 9999
maxMM = 0

while True: 
    mm = measure(SerialDevice)
    if mm >= Range:
        print("No Target Found.")
        sleep(SleepTime)
        continue
        
    if mm < minMM:
        minMM = mm
    if mm > maxMM:
        maxMM = mm
        
    print('Distance: ', mm, " min: ", minMM, " max: ", maxMM)
    sleep(SleepTime)