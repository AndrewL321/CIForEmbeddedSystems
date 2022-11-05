import RPi.GPIO as GPIO
import time
"""
    For controlling servos movement

    Layout:

    1----2
    |    |
    3----4

    Servo pins:

    1 == pin 11
    2 == pin 12
    3 == pin 13
    4 == pin 15

"""

class ServoControl:


    #controls for each axis
    def moveXPositive(self,holdTime = None):
        self.moveSpecified([1,3],holdTime)

    def moveXNegative(self,holdTime =None):
        self.moveSpecified([2,4],holdTime)

    def moveYPositive(self,holdTime =None):
        self.moveSpecified([1,2],holdTime)

    def moveYNegative(self,holdTime =None):
        self.moveSpecified([3,4],holdTime)


    #move specified up
    def servoUp(self, Servo: GPIO.PWM):
        Servo.ChangeDutyCycle(self.upDuty)
        return
    #down
    def servoDown(self, Servo: GPIO.PWM):
        Servo.ChangeDutyCycle(self.downDuty)
        return

    #for all
    def moveAll(self,holdTime =None):
        self.moveSpecified([1,2,3,4],holdTime)
        return

    #lower all
    def lowerAll(self):
        GPIO.setmode(GPIO.BOARD)

        for i in range(self.NumberOfServos):
            self.servoDown(self.Servos[i])

        #delay to allow them to move 
        time.sleep(0.5)
        pass

    #clean gpio, call when done
    def clean(self):
        GPIO.setmode(GPIO.BOARD)

        for i in range(self.NumberOfServos):
            self.Servos[i].stop()
        GPIO.cleanup()
        return

    #specific
    def moveSpecified(self, ToMove: list[int],HoldTime = None):
        GPIO.setmode(GPIO.BOARD)

        for i in ToMove:
            self.servoUp(self.Servos[i-1])

        if HoldTime != None:
            time.sleep(HoldTime)
            self.lowerAll()
        return

    #creates 4 pwm pins in list. sets to freq = 50, duty  cycle 3
    def __init__(self):

        GPIO.setmode(GPIO.BOARD)

        self.NumberOfServos = 4
        self.Servos = [None] * self.NumberOfServos
        self.ServoPin = [11,12,13,15]

        self.upDuty = 7.5
        #Use 3 instead of 2.5 to avoid getting stuck
        self.downDuty = 3


        for i in range(self.NumberOfServos):
            GPIO.setup(self.ServoPin[i], GPIO.OUT)
            self.Servos[i] = GPIO.PWM(self.ServoPin[i],50)
            self.Servos[i].start(self.downDuty)
        pass