
import os
import json
#import picamera
import time
import cv2
from cv2 import imshow

dirname = os.path.dirname(__file__)
devicePath = os.path.join(dirname, 'MicroBitConfig/LEDMatrix.json')


#Detects brightness in LED matrix of area and return average pixel intensity

def DetectBrightness(report,imagePath = None):
    #Take picture if none provided
    if(imagePath == None):
        imagePath = takeImage(report)
    #read image
    image = cv2.imread(imagePath)
    #to grey
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #Load pixel coords of led matrix
    xStart,xEnd,yStart,yEnd = loadDevice() 
    average = 0
    #total counted pixels
    totalPixels = (xEnd - xStart)*(yEnd- yStart)
    #go through each and add to total
    for x in range(xStart,xEnd):
        for y in range(yStart,yEnd):
            #calc as average here so no big numbers
            average+= (image[y,x]/totalPixels)

    if report != None:
        report.addOutput(average, "Brightness")
    return average

def loadDevice():

    data = ''
    with open(devicePath, 'r') as file:
        data = json.loads(file.read())
    return data["xStart"],data["xEnd"],data["yStart"],data["yEnd"]


def takeImage(report):
    pass
    # path = report.path

    # cam = PiCamera()
    # cam.start_preview()
    # time.sleep(3)

    # cam.capture(path + ".jpg")

    # cam.close()

    # return path + ".jpg"
