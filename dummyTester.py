import time

from create2Dummy import Create2

if __name__ == '__main__':
    create2 = Create2('nothing!')
    while True:

        print(create2.get_sensors())
        time.sleep(.5)