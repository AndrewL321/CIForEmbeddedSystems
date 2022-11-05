import sys
import time

sys.path.append('../project')
from Controls import ReadUSB,ServoControl
from Tests.TestUtility import CreateTestReport,uBitTests


def run(serial,report : CreateTestReport):
    time.sleep(1)
    ReadUSB.readBuffer(serial,report,t=2,Label= "Before Move")
    beforeValues = report.data["Before Move"]
    beforeValues = [int(i) for i in beforeValues]

    servo = ServoControl.ServoControl()
    servo.moveXPositive()
    time.sleep(1)
    servo.lowerAll()
    servo.clean()
    ReadUSB.readBuffer(serial,report,t= 2,Label= "After Move")

    afterValues = report.data["After Move"]
    afterValues = [int(i) for i in afterValues]


    maxBefore = int(max(beforeValues))
    maxAfter = int(max(afterValues))

    report.addLabeledData(str(maxBefore),"Max Before")
    report.addLabeledData(str(maxAfter),"Max After")

    assert maxBefore > -80 and maxBefore < 80
    assert maxAfter > 100

