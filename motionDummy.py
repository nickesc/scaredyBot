#!/usr/bin/env python3
import random
import time

def destroy():
    return

class PIR:

    lastReading = False
    motion = []

    def __init__(self, pin = 27):
        self.pirPin = pin

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