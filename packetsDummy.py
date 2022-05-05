#!/usr/bin/env python3

import random
from collections import namedtuple

timer = 0
currReturn = False

# Some data is bit mapped. These namedtuples break those out for easier use
BumpsAndWheelDrop = namedtuple('BumpsAndWheelDrop', 'bump_left bump_right wheeldrop_left wheeldrop_right')
WheelOvercurrents = namedtuple('WheelOvercurrents', 'side_brush_overcurrent main_brush_overcurrent right_wheel_overcurrent left_wheel_overcurrent')
Buttons = namedtuple('Buttons', 'clean spot dock minute hour day schedule clock')
ChargingSources = namedtuple('ChargingSources', 'internal_charger home_base')
LightBumper = namedtuple('LightBumper', 'left front_left center_left center_right front_right right')
Stasis = namedtuple('Stasis', 'toggling disabled')

# This is the big kahuna ... packet 100, everything
Sensors = namedtuple('Sensors', [
    'bumps_wheeldrops',
    'wall',
    'cliff_left',
    'cliff_front_left',
    'cliff_front_right',
    'cliff_right',
    'virtual_wall',
    'overcurrents',
    'dirt_detect',
    'ir_opcode',
    'buttons',
    'distance',
    'angle',
    'charger_state',
    'voltage',
    'current',
    'temperature',
    'battery_charge',
    'battery_capacity',
    'wall_signal',
    'cliff_left_signal',
    'cliff_front_left_signal',
    'cliff_front_right_signal',
    'cliff_right_signal',
    'charger_available',
    'open_interface_mode',
    'song_number',
    'song_playing',
    'oi_stream_num_packets',
    'velocity',
    'radius',
    'velocity_right',
    'velocity_left',
    'encoder_counts_left',
    'encoder_counts_right',
    'light_bumper',
    'light_bumper_left',
    'light_bumper_front_left',
    'light_bumper_center_left',
    'light_bumper_center_right',
    'light_bumper_front_right',
    'light_bumper_right',
    'ir_opcode_left',
    'ir_opcode_right',
    'left_motor_current',
    'right_motor_current',
    'main_brush_current',
    'side_brush_current',
    'statis'
])

def SensorPacketDecoder():
    try:
        drop = bool(random.getrandbits(1))
        wall = (bool(random.getrandbits(1)))
        cliff_left = bool(random.getrandbits(1))
        cliff_front_left = bool(random.getrandbits(1))
        cliff_front_right = bool(random.getrandbits(1))
        cliff_right = bool(random.getrandbits(1))
        virtual_wall = bool(random.getrandbits(1))
        curr = random.getrandbits(1)
        dirt_detect = random.randint(0, 255)
        ir_opcode = random.randint(0, 255)
        butt = random.getrandbits(1)
        distance = random.randint(-322768, 32767)
        angle = random.randint(-322768, 32767)
        charger_state = random.randint(0, 6)
        voltage = random.randint(0, 65535)
        current = random.randint(-322768, 32767)
        temperature = random.randint(-128, 127)
        battery_charge = random.randint(0, 65535)
        battery_capacity = random.randint(0, 65535)
        wall_signal = random.randint(0, 1023)
        cliff_left_signal = random.randint(0, 4095)
        cliff_front_left_signal = random.randint(0, 4095)
        cliff_front_right_signal = random.randint(0, 4095)
        cliff_right_signal = random.randint(0, 4095)
        charger_available = random.randint(0, 3)
        open_interface_mode = random.randint(0, 3)
        song_number = random.randint(0, 4)
        song_playing = bool(random.getrandbits(1))
        oi_stream_num_packets = random.randint(0, 108)
        velocity = random.randint(-500, 500)
        radius = random.randint(-322768, 32767)
        velocity_right = random.randint(-500, 500)
        velocity_left = random.randint(-500, 500)
        encoder_counts_left = random.randint(-322768, 32767)
        encoder_counts_right = random.randint(-322768, 32767)
        charge = bool(random.getrandbits(1))
        bump = bool(random.getrandbits(1))
        light_bumper_left = random.randint(0, 4095)
        light_bumper_front_left = random.randint(0, 4095)
        light_bumper_center_left = random.randint(0, 4095)
        light_bumper_center_right = random.randint(0, 4095)
        light_bumper_front_right = random.randint(0, 4095)
        light_bumper_right = random.randint(0, 4095)
        ir_opcode_left = random.randint(0, 255)
        ir_opcode_right = random.randint(0, 255)
        left_motor_current = random.randint(-322768, 32767)
        right_motor_current = random.randint(-322768, 32767)
        main_brush_current = random.randint(-322768, 32767)
        side_brush_current = random.randint(-322768, 32767)
        stas = random.getrandbits(1)
    except:
        drop = bool(0)
        wall = (bool(0))
        cliff_left = bool(0)
        cliff_front_left = bool(0)
        cliff_front_right = bool(0)
        cliff_right = bool(0)
        virtual_wall = bool(0)
        curr = 0
        dirt_detect = 0
        ir_opcode = 0
        butt = 0
        distance = 0
        angle = 0
        charger_state = 0
        voltage = 0
        current = 0
        temperature = 0
        battery_charge = 0
        battery_capacity = 0
        wall_signal = 0
        cliff_left_signal = 0
        cliff_front_left_signal = 0
        cliff_front_right_signal = 0
        cliff_right_signal = 0
        charger_available = 0
        open_interface_mode = 0
        song_number = 0
        song_playing = bool(0)
        oi_stream_num_packets = 0
        velocity = 0
        radius = 0
        velocity_right = 0
        velocity_left = 0
        encoder_counts_left = 0
        encoder_counts_right = 0
        charge = bool(0)
        bump = bool(0)
        light_bumper_left = 0
        light_bumper_front_left = 0
        light_bumper_center_left = 0
        light_bumper_center_right = 0
        light_bumper_front_right = 0
        light_bumper_right = 0
        ir_opcode_left = 0
        ir_opcode_right = 0
        left_motor_current = 0
        right_motor_current = 0
        main_brush_current = 0
        side_brush_current = 0
        stas = 0

    """
    This function decodes a Create 2 packet 100 and returns a Sensor object,
    which is really a namedtuple. The Sensor class holds all sensor values for
    the Create 2. It is basically like a C struct.
    """


    bumps_wheeldrops = BumpsAndWheelDrop(
        bool(drop),
        bool(drop),
        bool(drop),
        bool(drop)
    )

    overcurrents = WheelOvercurrents(
        bool(curr),
        bool(curr),
        bool(curr),
        bool(curr)
    )
    # self.buttons = Buttons(data[11:12])


    buttons = Buttons(
        bool(butt),
        bool(butt),
        bool(butt),
        bool(butt),
        bool(butt),
        bool(butt),
        bool(butt),
        bool(butt)
    )
    # self.charging_sources = ChargingSources(data[39:40])

    charging_sources = ChargingSources(
        bool(charge),
        bool(not charge)
    )
    # self.light_bumper = LightBumper(data[56:57])

    light_bumper = LightBumper(
        bool(bump),
        bool(bump),
        bool(bump),
        bool(not bump),
        bool(not bump),
        bool(not bump)
    )
    # self.stasis = Stasis(data[79:80])

    stasis = Stasis(
        bool(stas),
        bool(not stas)
    )



    sensors = Sensors(

        bumps_wheeldrops,  # bumps_wheeldrops,
        wall,  # unpack_bool_byte(data[1:2])[0],         # wall
        cliff_left,  # unpack_bool_byte(data[2:3])[0],         # cliff left
        cliff_front_left,  # unpack_bool_byte(data[3:4])[0],         # cliff front left
        cliff_front_right,  # unpack_bool_byte(data[4:5])[0],         # cliff front right
        cliff_right,  # unpack_bool_byte(data[5:6])[0],         # cliff right
        virtual_wall,  # unpack_bool_byte(data[6:7])[0],         # virtual wall
        overcurrents,  # overcurrents,
        dirt_detect,  # unpack_byte(data[8:9])[0],              # dirt detect
        ir_opcode,  # unpack_unsigned_byte(data[10:11])[0],   # ir opcode
        buttons,  # buttons,
        distance,  # unpack_short(data[12:14])[0],           # distance
        angle,  # unpack_short(data[14:16])[0],           # angle
        charger_state,  # unpack_unsigned_byte(data[16:17])[0],   # charge state
        voltage,  # unpack_unsigned_short(data[17:19])[0],  # voltage
        current,  # unpack_short(data[19:21])[0],           # current
        temperature,  # unpack_byte(data[21:22])[0],            # temperature in C, use CtoF if needed
        battery_charge,  # unpack_unsigned_short(data[22:24])[0],  # battery charge
        battery_capacity,  # unpack_unsigned_short(data[24:26])[0],  # battery capacity
        wall_signal,  # unpack_unsigned_short(data[26:28])[0],  # wall
        cliff_left_signal,  # unpack_unsigned_short(data[28:30])[0],  # cliff left
        cliff_front_left_signal,  # unpack_unsigned_short(data[30:32])[0],  # cliff ront left
        cliff_front_right_signal,  # unpack_unsigned_short(data[32:34])[0],  # cliff front right
        cliff_right_signal,  # unpack_unsigned_short(data[34:36])[0],  # cliff right
        charger_available,  # charging_sources,
        open_interface_mode,  # unpack_unsigned_byte(data[40:41])[0],   # oi mode
        song_number,  # unpack_unsigned_byte(data[41:42])[0],   # song number
        song_playing,  # unpack_bool_byte(data[42:43])[0],       # song playing
        oi_stream_num_packets,  # unpack_unsigned_byte(data[43:44])[0],   # oi stream num packets
        velocity,  # unpack_short(data[44:46])[0],           # velocity
        radius,  # unpack_short(data[46:48])[0],           # turn radius
        velocity_right,  # unpack_short(data[48:50])[0],           # velocity right
        velocity_left,  # unpack_short(data[50:52])[0],           # velocity left
        encoder_counts_left,  # unpack_unsigned_short(data[52:54])[0],  # encoder left
        encoder_counts_right,  # unpack_unsigned_short(data[54:56])[0],  # encoder right
        light_bumper,  # light_bumper,
        light_bumper_left,  # unpack_unsigned_short(data[57:59])[0],  # light bump left
        light_bumper_front_left,  # unpack_unsigned_short(data[59:61])[0],  # light bmp front left
        light_bumper_center_left,  # unpack_unsigned_short(data[61:63])[0],  # light bump center left
        light_bumper_center_right,  # unpack_unsigned_short(data[63:65])[0],  # light bump center right
        light_bumper_front_right,  # unpack_unsigned_short(data[65:67])[0],  # light bump front right
        light_bumper_right,  # unpack_unsigned_short(data[67:69])[0],  # light bump right
        ir_opcode_left,  # unpack_unsigned_byte(data[69:70])[0],   # ir opcode left
        ir_opcode_right,  # unpack_unsigned_byte(data[70:71])[0],   # ir opcode right
        left_motor_current,  # unpack_short(data[71:73])[0],           # left motor current
        right_motor_current,  # unpack_short(data[73:75])[0],           # right motor current
        main_brush_current,  # unpack_short(data[75:77])[0],           # main brush current
        side_brush_current,  # unpack_short(data[77:79])[0],           # side brush current
        stasis  # stasis
    )

    return sensors


