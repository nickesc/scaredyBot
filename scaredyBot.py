#!/usr/bin/env python3

from motion import PIR
from pycreate2 import Create2
import time
from copy import deepcopy
import RPi.GPIO as GPIO


port = '/dev/ttyUSB0'

class ScaredyBot():

    baseSpeed = 100

    def __init__(self, tty):
        self.botPort = tty  # where is your serial port?
        self.create2 = Create2(self.botPort)
        self.pir = PIR()

        self.create2.start()
        self.create2.safe()

        self.state = {'motion':False}
        self.setState()

    def stop(self):
        self.create2.drive_stop()

    # driving the bot - speed between 0 & 3; direction is 'forward' or 'back'
    def drive(self, speed = 1, dir = 'forward'):
        return

    def driveUntilYouHitAWall(self, speed, direction = 'forward'):
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

    def rotate(self, direction, degrees = 90):
        return

    def checkAround(self):
        return

    def runAway(self):
        return

    def setState(self):
        try:
            # self.state = {'bot': self.bot.get_sensors(), 'pi': piSensors.getSensors()}

            self.state = deepcopy(self.create2.get_sensors())
            self.state["motion"] = self.pir.getMotion()
            return True
        except:
            return False

    def getSensors(self, output = False):
        self.setState()

        if output:
            print(self.state)

        return self.state

    def checkMotion(self):
        return self.pir.getMotion()


def loop():
    global scaredyBot

    while True:
        print(scaredyBot.getSensors())
        time.sleep(.1)
        scaredyBot.checkMotion()
        time.sleep(.1)

def destroy():
    print("Quitting")
    GPIO.cleanup()

if __name__ == '__main__':

    scaredyBot = ScaredyBot('/dev/ttyUSB0')
    try:
        print(scaredyBot.checkMotion())
        time.sleep(.1)
        scaredyBot.driveUntilYouHitAWall(1)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

