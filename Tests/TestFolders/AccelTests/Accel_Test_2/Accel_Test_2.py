
import sys

sys.path.append('../project')
from Controls import ReadUSB,ServoControl
from Tests.TestUtility import CreateTestReport,uBitTests


def run(serial,report):
    control = ServoControl.ServoControl()
    control.moveXPositive(0.2)
    control.moveXNegative(0.2)
    control.moveYPositive(0.2)
    control.moveYNegative(0.2)
    control.moveAll(0.2)
    control.lowerAll(0.2)
    control.clean()
    data = ReadUSB.readBuffer(serial,report,5)

    assert report.checkEvent(str(uBitTests.ACCELEROMETER_EVT_TILT_DOWN)) == True, "Gesture event not detected"