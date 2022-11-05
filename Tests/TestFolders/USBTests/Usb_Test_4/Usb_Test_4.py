import sys

sys.path.append('../project')
from Controls import ReadUSB
from Tests.TestUtility import CreateTestReport,uBitTests


def run(serial,report : CreateTestReport):
    data = ReadUSB.readBuffer(serial,report)
    assert "Word" in data