import sys
sys.path.append('../Project2')
import time

from Controls import ServoControl


new = ServoControl.ServoControl()
new.moveAll()
time.sleep(10)
new.lowerAll()
new.clean()
