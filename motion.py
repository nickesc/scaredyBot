#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def destroy():
    GPIO.cleanup()

class PIR:

    lastReading = False
    motion = []

    def __init__(self, pin = 27):
        self.pirPin = pin

        GPIO.setmode(GPIO.BCM)  # Set the GPIO modes to BCM Numbering
        GPIO.setup(self.pirPin, GPIO.IN) # set up motion pin

    def getMotion(self):
        if (GPIO.input(self.pirPin) == 0):
            self.lastReading = False
        else:
            self.lastReading = True

        self.motion = [self.lastReading] + self.motion
        self.motion.pop()

        return self.lastReading

    def getLastReading(self):
        return self.lastReading

    def getMotionList(self):
        return self.motion

    def getSensors(self,output = False):
        data = {'motion': self.getMotion()}
        if (output):
            print(data)
        return (data)

    def cleanup(self):
        destroy()

def loop(pir):
    while True:
        pir.getSensors(output = True)
        time.sleep(.3)

if __name__ == '__main__':  # Program start from here

    pir = PIR(27) # PIR motion pin = GPIO27 (BCM) / 13 (board)

    try:
        loop(pir)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
