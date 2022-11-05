import string
import serial
import time

from Tests.TestUtility.CreateTestReport import CreateTestReport

#Default timeout
defaultTime = 5

#Reads all data from buffer and reads until t, timeleft reaches 0
def readBuffer(serialPort : serial,report:CreateTestReport, t = None, Label= None ):

    #if no time use default
    if t == None:
        t = defaultTime
    serialPort.timeout = t

    finalData= ""

    #Track start time for total time reading
    startTime = time.time()
    #time left > 0
    while t > 0:
        ##read
        data = serialPort.read(1024).decode()
        if data:
            #add to buffer
            finalData += data
            #calc time passed
            newTime = time.time()
            passed = newTime - startTime
            #take from remaining time
            t = t - passed
        else:
            break
    #if label for data was provided
    if Label == None:
        report.addData(data)
    else:
        report.addLabeledData(data,Label)
    return finalData


#Read for t seconds, check ready signal received, clean buffer after
def readReady(serialPort: serial, t = None):
    if t == None:
        t = defaultTime
    serialPort.timeout = t
    finalData= ""

    startTime = time.time()
    while t > 0:
        data = serialPort.read(1024).decode()
        if data:
            finalData += data
            newTime = time.time()
            passed = newTime - startTime
            t = t - passed
        else:
            break
    cleanBuffer(serialPort)
    return finalData

#Clear input buffer
def cleanBuffer(port: serial):
    port.reset_input_buffer()



#create serial port, baudrate 115200 for micro: bit, default timeout 0
def createPortRead(path: string):

    ser = serial.Serial(path, 115200,timeout=0)

    return ser

