#!/usr/bin/env python3

try:
    import RPi.GPIO as GPIO
    from motion import PIR
    from pycreate2 import Create2
except:
    from motionDummy import PIR
    from create2Dummy import Create2

import sys
import time
from copy import deepcopy
from states import _start, _searching, _running, _end

port = '/dev/ttyUSB0'

class ScaredyBot():

    baseSpeed = 100
    state = None

    motion = False

    looped = 0
    maxLoops = 10

    def __init__(self, tty):
        self.state = _start(self)
        self.state.enter()

        self.botPort = tty  # where is your serial port?
        self.create2 = Create2(self.botPort)
        self.pir = PIR()

        self.create2.start()
        self.create2.safe()

        self.sensors = {'motion':False}
        self.setSensors()

        self.changeState(_searching(self))

        self.loop()

    def changeState(self, state):
        self.state.exit()
        self.state = state
        self.state.enter()

    def loop(self):
        self.state.execute()
        time.sleep(.1)
        self.loop()


    def getState(self):
        return self.state.getName()

    def stop(self):
        self.create2.drive_stop()

    # driving the bot - speed between 0 & 3; direction is 'forward' or 'back'
    def drive(self, speed = 1, dir = 'forward'):
        return

    def driveUntilWall(self, speed, direction = 'forward'):

        speed=speed*self.baseSpeed

        if direction=="back":
            speed = speed*-1

        self.create2.drive_direct(speed, speed)
        noWall = True
        while noWall:
            sensors = self.create2.get_sensors()
            bump = sensors.light_bumper
            if bump.front_left or bump.front_right:
                self.create2.drive_stop()
                noWall = False

    def driveOne(self, speed = 1, dir = 'forward'):
        return

    def rotate(self, dir, degrees = 90):
        return

    def checkAround(self):
        return

    def runAway(self):
        return

    def setSensors(self):
        try:
            self.sensors = self.create2.get_sensors()
            self.motion = self.pir.getMotion()
            return True
        except:
            return False

    def getSensors(self, output = False):
        self.setSensors()

        if output:
            print(self.sensors, "\nMotion:", self.motion)

        return self.sensors

    def checkMotion(self):
        self.motion = self.pir.getMotion()
        return self.motion

    def destroy(self):
        print("Quitting")
        try:
            GPIO.cleanup()
        except:
            pass
        self.create2.close()
        sys.exit()

if __name__ == '__main__':

    scaredyBot = ScaredyBot('/dev/ttyUSB0')
    # try:
    #     print(scaredyBot.checkMotion())
    #     time.sleep(.1)
    #     scaredyBot.driveUntilYouHitAWall(1)
    #
    # except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    #     destroy()

