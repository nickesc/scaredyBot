#!/usr/bin/env python3

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
        _state.scaredyBot.speed = 0
        time.sleep(.5)

    def execute(_state):
        while _state.scaredyBot.ready == False:
            pass
        _state.scaredyBot.changeState(_searching(_state.scaredyBot))

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())

class _searching():

    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "searching"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())
        _state.scaredyBot.speed = 75
        _state.scaredyBot.pir.light.green()

    def execute(_state):
        sense = _state.scaredyBot.getSensors(True)
        if(_state.scaredyBot.motion!=True):
            pass

        else:
            _state.scaredyBot.changeState(_running(_state.scaredyBot))

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())

class _running():
    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "running"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())
        _state.scaredyBot.speed = 250
        _state.scaredyBot.pir.light.red()


    def execute(_state):
        time.sleep(4)
        if _state.scaredyBot.looped<_state.scaredyBot.maxLoops:
            _state.scaredyBot.changeState(_searching(_state.scaredyBot))
            _state.scaredyBot.looped += 1
        else:
            _state.scaredyBot.changeState(_end(_state.scaredyBot))
        return

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())

class _end():

    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "end"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())
        _state.scaredyBot.speed = 0
        _state.scaredyBot.stop()
        _state.exit()

    def execute(_state):
        return

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())
        time.sleep(.5)
        _state.scaredyBot.destroy()
