#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def destroy():

    GPIO.cleanup()

class PIR:

    lastReading = False
    motion = []

    class Light:
        colors = {'red' : 0xFF0000, 'green' : 0x00FF00, 'blue' : 0x0000FF}

        def __init__(light, rPin = 13, gPin = 19, bPin = 26):

            light.r = rPin
            light.g = gPin
            light.b = bPin

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(light.r, GPIO.OUT)
            GPIO.setup(light.g, GPIO.OUT)
            GPIO.setup(light.b, GPIO.OUT)

            light.p_R = GPIO.PWM(light.r, 2000)
            light.p_G = GPIO.PWM(light.g, 2000)
            light.p_B = GPIO.PWM(light.b, 2000)
            light.p_R.start(0)
            light.p_G.start(0)
            light.p_B.start(0)

        def red(light):
            light.setColor(light.colors['red'])
        def green(light):
            light.setColor(light.colors['green'])
        def blue(light):
            light.setColor(light.colors['blue'])

        def MAP(light, x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        # Define a function to set up colors
        def setColor(light, color):
            # configures the three LEDs' luminance with the inputted color value.
            R_val = (color & 0xFF0000) >> 16
            G_val = (color & 0x00FF00) >> 8
            B_val = (color & 0x0000FF) >> 0

            # Map color value from 0~255 to 0~100
            R_val = light.MAP(R_val, 0, 255, 0, 100)
            G_val = light.MAP(G_val, 0, 255, 0, 100)
            B_val = light.MAP(B_val, 0, 255, 0, 100)

            # Change the colors
            light.p_R.ChangeDutyCycle(R_val)
            light.p_G.ChangeDutyCycle(G_val)
            light.p_B.ChangeDutyCycle(B_val)

    def __init__(pir, pin = 27):
        pir.pirPin = pin

        pir.light = pir.Light(rPin = 13, gPin = 19, bPin = 26)

        GPIO.setmode(GPIO.BCM)  # Set the GPIO modes to BCM Numbering
        GPIO.setup(pir.pirPin, GPIO.IN) # set up motion pin

    def getMotion(pir):
        if (GPIO.input(pir.pirPin) == 0):
            pir.lastReading = False
        else:
            pir.lastReading = True

        pir.motion = [pir.lastReading] + pir.motion
        pir.motion.pop()

        return pir.lastReading

    def getLastReading(pir):
        return pir.lastReading

    def getMotionList(pir):
        return pir.motion

    def getSensors(pir,output = False):
        data = {'motion': pir.getMotion()}
        if (output):
            print(data)
        return (data)

    def cleanup(pir):
        pir.light.p_R.stop()
        pir.light.p_G.stop()
        pir.light.p_B.stop()
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
        pir.cleanup()
        destroy()
