#!/usr/bin/env python3

from packetsDummy import SensorPacketDecoder


class Create2(object):
    def __init__(self, port):
        self.port = port

    def close(self):
        return

    def start(self):
        return

    def getMode(self):
        return

    def wake(self):
        return

    def reset(self):
        return

    def stop(self):
        return

    def safe(self):
        return

    def full(self):
        return

    def power(self):
        return

    def drive_stop(self):
        return

    def limit(self, val, low, hi):
        return

    def drive_direct(self, r_vel, l_vel):
        return

    def drive_pwm(self, r_pwm, l_pwm):
        return

    def led(self, led_bits = 0, power_color = 0, power_intensity = 0):
        return

    def digit_led_ascii(self, display_string):
        return

    def clearSongMemory(self):
        return

    def createSong(self, song_num, notes):
        return

    def playSong(self, song_num):
        return

    def get_sensors(self):
        sensors = SensorPacketDecoder()

        return sensors
