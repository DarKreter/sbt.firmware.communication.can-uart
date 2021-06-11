#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

import can
from can.interface import Bus

import serial

from can_buffer import can_buffer

port = "/dev/ttyUSB0"

can.rc['interface'] = 'socketcan_native'
can.rc['channel'] = 'vcan0'


def rx_fcn(msg):
    my_buf.append_frame(msg)


portObj = serial.Serial(port=port, baudrate=115200, timeout=0.3)
portObj.flush()

my_buf = can_buffer()

my_bus = Bus()
notifier = can.Notifier(my_bus, [rx_fcn], 1)

while 1:
    #  printF()
    serialized = my_buf.storage_to_serialized_data()
    my_buf.clean()
    if len(serialized) == 0:
        print("no data to send")
    else:
        print("gonna send!")
        print(serialized)
        portObj.write(serialized)
    sleep(1)
