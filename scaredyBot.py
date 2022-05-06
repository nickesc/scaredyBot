#!/usr/bin/env python3

try:
    import RPi.GPIO as GPIO
    from motion import PIR
    #from pycreate2 import Create2
except:
    from motionDummy import PIR
from create2Dummy import Create2

from powerButton import PowerButton
import sys
import time
from copy import deepcopy
from states import _start, _searching, _running, _end

port = '/dev/ttyUSB0'

class ScaredyBot:

    baseSpeed = 100
    state = None

    motion = False

    looped = 0
    maxLoops = 10

    ready = False

    def __init__(bot, tty):
        bot.state = _start(bot)
        bot.state.enter()

        bot.botPort = tty  # where is your serial port?
        bot.create2 = Create2(bot.botPort)
        bot.pir = PIR()

        bot.create2.start()
        bot.create2.safe()

        bot.sensors = {'motion':False}
        bot.setSensors()

        #bot.changeState(_searching(bot))

        bot.power = PowerButton(bot)

        bot.loop()

    def changeState(bot, state):
        bot.state.exit()
        bot.state = state
        bot.state.enter()

    def loop(bot):
        bot.state.execute()
        time.sleep(.01)
        bot.loop()


    def getState(bot):
        return bot.state.getName()

    def stop(bot):
        bot.create2.drive_stop()

    # driving the bot - speed between 0 & 3; direction is 'forward' or 'back'
    def drive(bot, speed = 1, dir = 'forward'):
        return

    def driveUntilWall(bot, speed, direction = 'forward'):

        speed=speed*bot.baseSpeed

        if direction=="back":
            speed = speed*-1

        bot.create2.drive_direct(speed, speed)
        noWall = True
        while noWall:
            sensors = bot.create2.get_sensors()
            bump = sensors.light_bumper
            if bump.front_left or bump.front_right:
                bot.create2.drive_stop()
                noWall = False

    def driveOne(bot, speed = 1, dir = 'forward'):
        return

    def rotate(bot, dir, degrees = 90):
        return

    def checkAround(bot):
        return

    def runAway(bot):
        return

    def setSensors(bot):
        try:
            bot.sensors = bot.create2.get_sensors()
            bot.motion = bot.pir.getMotion()
            return True
        except:
            return False

    def getSensors(bot, output = False):
        bot.setSensors()

        if output:
            print(bot.sensors, "\nMotion:", bot.motion)

        return bot.sensors

    def checkMotion(bot):
        bot.motion = bot.pir.getMotion()
        return bot.motion

    def destroy(bot):
        print("Quitting")
        try:
            bot.pir.cleanup()
        except:
            pass
        bot.create2.close()
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

