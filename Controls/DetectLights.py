import json
import cv2
from picamera import PiCamera
import time

import os
import sys
sys.path.insert(1, '/home/pi/actions-runner/_work/Project2/Project2/')

from Tests.TestUtility import uBitTests

dirname = os.path.dirname(__file__)
devicePath = os.path.join(dirname, 'MicroBitConfig/LEDMatrix.json')

def DetectLights(report,imagePath = None):


    xStart, xOffset, yStart,yOffset =  loadDevice()
    #if no image provided, take image
    if(imagePath == None):
        imagePath = takeImage(report)
    #read image
    image = cv2.imread(imagePath)
    #to grey
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #reduce noise
    image = cv2.blur(image,(7,7))

    #Set bright pixels to 1, dimmer to 0
    ret,image = cv2.threshold(image,230,255,cv2.THRESH_BINARY)

    ledArray = [[0]*5 for i in range(5)]

    # iterate over each block in grid
    for i in range(0,5):
        for z in range(0,5):
            average = 0
            for x in range(xStart + (xOffset * i), xStart + (xOffset * i) + xOffset):
                for y in range(yStart + (yOffset * z), yStart + (yOffset * z) + yOffset):
                    average += image[y,x]
            #if average pixel value > thresh, set corresponding value in array to 1
            if average/(xOffset*yOffset) > 30:
                ledArray[z][i] = 1

    if report != None:
        report.addOutput(ledArray,uBitTests.DEVICE_ID_DISPLAY)
    return ledArray

#load device spec from json
def loadDevice():

    data = ''
    with open(devicePath, 'r') as file:
        data = json.loads(file.read())

    xOffset = int((data["xEnd"] -data["xStart"])/ data["xHops"])
    yOffset = int((data["yEnd"] -data["yStart"])/ data["yHops"])


    return data["xStart"],xOffset,data["yStart"],yOffset

#take an image and store in resilts folder
def takeImage(report):

    path = report.path

    cam = PiCamera()
    cam.start_preview()
    time.sleep(3)

    cam.capture(path + ".jpg")

    cam.close()

    return path + ".jpg"
