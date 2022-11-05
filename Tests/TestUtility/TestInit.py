from datetime import datetime
from Controls import ReadUSB
import os

class testInit:


    def initTest(self):

        #creates file with current date and time in results folder
        date = datetime.today()
        date = date.strftime("%Y-%m-%d")

        now = datetime.now()
        now = now.strftime("%H:%M:%S")

        final = date + "--" + now

        self.path = "Results/" + final
        os.mkdir(self.path)

        self.resultsFile = open(self.path +  '/Results.txt','a+')
        #open serial port to micro: bit

        self.serial = ReadUSB.createPortRead('/dev/ttyACM0')

    def __init__(self) -> None:
        self.initTest()
