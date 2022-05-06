#!/usr/bin/env python3
import random

try:
    import RPi.GPIO as GPIO
    from pycreate2 import Create2
except:
    from create2Dummy import Create2

import time

class _start():
    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "start"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())
        _state.scaredyBot.baseSpeed = 0
        time.sleep(.5)

    def execute(_state):
        while _state.scaredyBot.ready == False:
            pass
        _state.scaredyBot.changeState(_searching(_state.scaredyBot))

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())

class _searching():

    botAngle=0

    currAngle = 90
    currDir = 'left'
    goalAngle = currAngle
    angleChange = 45

    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "searching"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())
        time.sleep(5)
        _state.scaredyBot.baseSpeed = 75

        _state.scaredyBot.pir.light.green()
        _state.currDir = _state.scaredyBot.randDir()
        _state.botAngle = _state.scaredyBot.checkAngle()
        _state.scaredyBot.stop()

    def execute(_state):
        sense = _state.scaredyBot.getSensors(True)
        if(_state.scaredyBot.motion!=True):
            print(_state.currDir, sense['angle'])

        else:
            _state.scaredyBot.changeState(_running(_state.scaredyBot))

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())

class _running():

    phases = {'rotating':'rotating','running':'running','waiting':'waiting', 'done':'done'}
    phase = 'rotating'

    firstRotate = True
    newRotate = True
    rotating = True
    running = False
    waiting = False

    turnDir = 'left'
    goalAngle = 120
    currAngle = 0

    #wall = False
    #leftWall = False
    #rightWall = False

    startTime = 0
    endTime = 18

    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "running"

    def enter(_state):

        _state.turnDir = _state.scaredyBot.randDir()
        _state.goalAngle = random.randint(100,260)

        print('entering', _state.scaredyBot.getState())
        _state.scaredyBot.baseSpeed = 400
        _state.scaredyBot.pir.light.red()


    def execute(_state):
        currTime = time.time()

        print('phase',_state.phase)
        print('wall', _state.scaredyBot.wall, _state.scaredyBot.wallLeft, _state.scaredyBot.wallRight)
        print('curr', currTime)
        print('end', _state.endTime)

        if _state.phase == _state.phases['rotating']:
            if _state.firstRotate == True:
                _state.firstRotate = False
                _state.endTime = _state.endTime + currTime

            if _state.newRotate:
                bump = _state.scaredyBot.checkBump()
                print(bump)
                if _state.scaredyBot.wallRight and _state.scaredyBot.wallLeft == False:
                    _state.turnDir = 'left'
                    _state.goalAngle = random.randint(100,170)

                if _state.scaredyBot.wallRight == False and _state.scaredyBot.wallLeft:
                    _state.turnDir = 'right'
                    _state.goalAngle = random.randint(330, 280)

                if _state.scaredyBot.wallRight and _state.scaredyBot.wallLeft:
                    _state.turnDir = _state.scaredyBot.randDir()
                    _state.goalAngle = random.randint(30, 80)
                _state.currAngle = 0
                _state.startTime = currTime
                _state.endTime = _state.endTime + 3
                _state.newRotate = False
                if _state.firstRotate == False:
                    _state.scaredyBot.drive(dir = 'back')
                    time.sleep(.2)
                    _state.scaredyBot.stop()
                _state.scaredyBot.rotate(_state.turnDir)

            if abs(_state.currAngle) >= _state.goalAngle:
                _state.scaredyBot.stop()
                _state.phase = _state.phases['running']
                _state.startTime = currTime
                #_state.endTime += currTime

                _state.scaredyBot.drive()

            elif abs(_state.currAngle) < _state.goalAngle:
                _state.currAngle += _state.scaredyBot.checkAngle()

        elif _state.phase == _state.phases['running']:
            bump = _state.scaredyBot.checkBump()
            # print(bump)
            # if not _state.scaredyBot.wall:
            #     bump = _state.scaredyBot.getSensors()['light_bumper']
            #     if bump.left or bump.front_left or bump.center_left:
            #         _state.scaredyBot.wall = True
            #         _state.scaredyBot.leftWall = True
            #     if bump.center_right or bump.front_right or bump.right:
            #         _state.scaredyBot.wall = True
            #         _state.scaredyBot.rightWall = True

            #if(scaredyBot)

            if (currTime >= _state.endTime - 7):
                _state.scaredyBot.stop()
                _state.phase = _state.phases['waiting']
                _state.scaredyBot.pir.light.blue()

            if _state.scaredyBot.wall:
                _state.newRotate = True
                _state.phase = _state.phases['rotating']


        elif _state.phase == _state.phases['waiting']:
            time.sleep(.2)
            if currTime >= _state.endTime:
                _state.phase = _state.phases['done']

        elif _state.phase == _state.phases['done']:
            if _state.scaredyBot.looped<_state.scaredyBot.maxLoops:
                _state.scaredyBot.wall = False
                _state.scaredyBot.wallLeft = False
                _state.scaredyBot.wallRight = False
                _state.scaredyBot.looped += 1
                _state.scaredyBot.changeState(_searching(_state.scaredyBot))

            else:
                _state.scaredyBot.changeState(_end(_state.scaredyBot))
            #return

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())

class _end():

    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "end"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())
        _state.scaredyBot.baseSpeed = 0
        _state.scaredyBot.stop()
        _state.exit()

    def execute(_state):
        return

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())
        time.sleep(.5)
        _state.scaredyBot.destroy()
