import sys

sys.path.append('../project')
from Controls import ReadUSB,ServoControl
from Tests.TestUtility import CreateTestReport,uBitTests


def run(serial,report):
    control = ServoControl.ServoControl()
    control.moveXPositive(0.5)
    control.moveXNegative(0.5)
    control.moveYPositive(0.5)
    control.moveYNegative(0.5)
    control.moveAll(0.5)
    control.lowerAll()
    control.clean()
    ReadUSB.readBuffer(serial,report)
    assert report.checkEvent(str(uBitTests.ACCELEROMETER_EVT_TILT_UP)) == True, "Gesture event not detected"