#!/usr/bin/env python3
import random
from collections import namedtuple

from powerButton import PowerButton
import sys
import time
from states import _start, _searching, _running, _end

mac = False
bot = True
if mac:
    from motionDummy import PIR
else:
    import RPi.GPIO as GPIO
    from motion import PIR

if bot:
    from pycreate2 import Create2
else:
    from create2Dummy import Create2

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

        bot.sensors = {'angle':0}
        bot.setSensors()

        #bot.changeState(_searching(bot))

        bot.power = PowerButton(bot)

        bot.loop()

    def randDir(self):
        return random.choice(['left', 'right'])

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
        speed = speed * bot.baseSpeed

        if dir == "back":
            speed = speed * -1

        bot.create2.drive_direct(speed, speed)
        noWall = True
        while noWall:
            sensors = bot.create2.get_sensors()
            bump = sensors.light_bumper
            if bump.front_left or bump.front_right:
                bot.create2.drive_stop()
                noWall = False

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

    def rotate(bot, dir):


        if dir == 'left':
            x = 1
        else:
            x=-1

        bot.create2.drive_direct(bot.baseSpeed*x,bot.baseSpeed*-1*x)
        return

    def checkAround(bot):
        return

    def runAway(bot):
        return

    def setSensors(bot):
        try:
            bot.sensors = bot.create2.get_sensors()._asdict()
            #bot.sensors.bumps_wheeldrops = bot.sensors.bumps_wheeldrops._asdict()
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

    def checkAngle(bot):
        #bot.setSensors()
        return bot.sensors['angle']

    def destroy(bot):
        print("Quitting")
        try:
            bot.pir.cleanup()
        except:
            pass
        bot.create2.close()
        sys.exit()

if __name__ == '__main__':

    scaredyBot = ScaredyBot(port)
    # try:
    #     print(scaredyBot.checkMotion())
    #     time.sleep(.1)
    #     scaredyBot.driveUntilYouHitAWall(1)
    #
    # except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    #     destroy()

