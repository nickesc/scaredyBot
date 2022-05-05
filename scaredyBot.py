#!/usr/bin/env python3

from motion import PIR
#from pycreate2 import Create2
from create2Dummy import Create2
import time
from copy import deepcopy
import RPi.GPIO as GPIO


port = '/dev/ttyUSB0'


class _start():
    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "start"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())

    def execute(_state):
        return

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())


class _running():
    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "running"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())

    def execute(_state):
        time.sleep(5)
        scaredyBot.changeState(_end(scaredyBot))
        return

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())


class _searching():

    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "end"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())

    def execute(_state):
        time.sleep(5)
        scaredyBot.changeState(_running(scaredyBot))

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())


class _end():

    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "end"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())

    def execute(_state):
        return

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())
        scaredyBot.destroy()

class ScaredyBot():

    baseSpeed = 100
    state = None

    def __init__(self, tty):
        self.state = _start(self)

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

    def rotate(self, dir, degrees = 90):
        return

    def checkAround(self):
        return

    def runAway(self):
        return

    def setSensors(self):
        try:
            # self.state = {'bot': self.bot.get_sensors(), 'pi': piSensors.getSensors()}

            self.sensors = dict(self.create2.get_sensors()._asdict())
            self.sensors["motion"] = self.pir.getMotion()
            return True
        except:
            return False

    def getSensors(self, output = False):
        self.setSensors()

        if output:
            print(self.sensors)

        return self.sensors

    def checkMotion(self):
        return self.pir.getMotion()

    def destroy(self):
        print("Quitting")
        GPIO.cleanup()
        self.create2.close()
        quit()

if __name__ == '__main__':

    scaredyBot = ScaredyBot('/dev/ttyUSB0')
    # try:
    #     print(scaredyBot.checkMotion())
    #     time.sleep(.1)
    #     scaredyBot.driveUntilYouHitAWall(1)
    #
    # except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    #     destroy()

