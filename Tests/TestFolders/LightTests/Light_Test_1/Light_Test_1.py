import sys
import time

sys.path.append('../project')
from Controls import ReadUSB,LightInput
from Tests.TestUtility import CreateTestReport,uBitTests


def run(serial,report):
    LightInput.turnOff()
    ReadUSB.readBuffer(serial,report,t=1,Label= "Before Light",)
    beforeValues = report.data["Before Light"]
    beforeTotal = 0
    for i in beforeValues:
        beforeTotal += int(i)
    LightInput.turnOn()
    ReadUSB.cleanBuffer(serial)
    ReadUSB.readBuffer(serial,report,t= 1,Label= "After Light",)

    afterValues = report.data["After Light"]
    afterTotal = 0
    for i in afterValues:
        afterTotal += int(i)

    beforeAv= beforeTotal/len(beforeValues)
    afterAv = afterTotal/len(afterValues)

    report.data["Before average light value"] = [beforeAv]
    report.data["After average light value"] = [afterAv]

    assert beforeAv < afterAv