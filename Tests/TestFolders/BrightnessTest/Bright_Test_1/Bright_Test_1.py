from Controls import Brightness


def run(serial,report):
    brightness = Brightness.DetectBrightness(report,"/home/pi/actions-runner/_work/Project2/Project2/ControlTests/brightTest.jpg")
    threshold = 105
    assert brightness > threshold