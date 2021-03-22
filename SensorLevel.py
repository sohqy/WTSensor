from time import sleep
import Level as ll

SerialDevice = '/dev/ttyAMA0'   # Port name on RPi

Range = 10000       # Sensors we have has 10m range
SleepTime = 5       # Time interval for recording data
minMM = 9999        # Maximum observed data
maxMM = 0           # Minimum observed data

while True: 
    mm = ll.measure(SerialDevice)
    if mm >= Range:                 # Target is out of range. 
        print("No Target Found.")
        sleep(SleepTime)
        continue
        
    # Record minimum and maximum observed levels    
    if mm < minMM:
        minMM = mm
    if mm > maxMM:
        maxMM = mm
        
    print('Distance: ', mm, " Observed Min: ", minMM, " Observed max: ", maxMM)
    sleep(SleepTime)
