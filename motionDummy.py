#!/usr/bin/env python3
import random
import time

def destroy():
    return

class PIR:

    lastReading = False
    motion = []

    class Light:
        colors = {'red' : 0xFF0000, 'green' : 0x00FF00, 'blue' : 0x0000FF}

        def __init__(light, rPin = 13, gPin = 19, bPin = 26):
            return

        def red(light):
            return
        def green(light):
            return
        def blue(light):
            return

        def MAP(light, x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        # Define a function to set up colors
        def setColor(light, color):
            return


    def __init__(self, pin = 27):
        self.pirPin = pin
        self.light = self.Light(rPin = 13, gPin = 19, bPin = 26)

    def getMotion(self):

        sample = 1000

        switchTest = random.randint(0,sample)
        if (switchTest>float(sample*.95) and self.lastReading == False) or self.lastReading==True:
            self.lastReading = not self.lastReading

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