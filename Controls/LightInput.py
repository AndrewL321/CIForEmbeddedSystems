import RPi.GPIO as GPIO
import threading
import time



#Turns on light, create thread fot delayed turn off
def turnOn():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT) 
    GPIO.output(8,GPIO.HIGH)
    thread = threading.Thread(target=delayedTurnoff)
    thread.start()

#Turn off light
def turnOff():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT) 
    GPIO.output(8,GPIO.LOW)
    GPIO.cleanup()
#delayed turn off
def delayedTurnoff():
    time.sleep(10)
    turnOff()

