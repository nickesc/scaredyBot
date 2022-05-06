try:
    import RPi.GPIO as GPIO
except:
    pass

from states import _start, _searching, _running, _end

class PowerButton:
    def __init__(button, bot, pin = 20):
        button.buttonPin = pin
        button.scaredyBot = bot

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(button.buttonPin, GPIO.IN)
            GPIO.add_event_detect(button.buttonPin, GPIO.FALLING, callback = button.startScaredyBot)
        except:
            button.scaredyBot.ready = True

    def startScaredyBot(button, ev = None):
        try:
            GPIO.remove_event_detect(button.buttonPin)
            button.scaredyBot.ready = True
            GPIO.add_event_detect(button.buttonPin, GPIO.FALLING, callback = button.endScaredyBot)
        except:
            pass
        print("start!")

    def endScaredyBot(button, ev = None):
        button.scaredyBot.changeState(_end(button.scaredyBot))
        print("start!")
