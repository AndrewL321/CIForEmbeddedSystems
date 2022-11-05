import sys
sys.path.append('../project')
from Controls import DetectLights
from Tests.TestUtility import CreateTestReport

def run(serial,report):
    data = DetectLights.DetectLights(report)
    report.addData(data)
    assert data  == [[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,1,0]], sys.stderr.write("Led array incorrect, detected array = " + str(data))
    return 1