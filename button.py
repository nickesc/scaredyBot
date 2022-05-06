import RPi.GPIO as GPIO
import time
LedPin = 17  # Set GPIO17 as LED pin
BtnPin = 18  # Set GPIO18 as button pin

# Set Led status to True(OFF)
Led_status = True

# Define a setup function for some setup
def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BtnPin, GPIO.IN)

def swLed(ev=None):
    print('press!')

def main():
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=swLed)
    while True:
        time.sleep(1)


def destroy():
    GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the program
    # destroy() will be executed.
    except KeyboardInterrupt:
        destroy()