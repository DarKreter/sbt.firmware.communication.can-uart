#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import can
from can.interface import Bus

import serial

from myFrames import rx_machiery

port = "/dev/ttyUSB0"

can.rc['interface'] = 'socketcan_native'
can.rc['channel'] = 'vcan0'

my_bus = Bus()


def my_on_rx(frame: can.Message):
    print("WYSOKO")
    print(frame)
    my_bus.send(msg=frame)


m = rx_machiery(my_on_rx)

portObj = serial.Serial(port=port, baudrate=115200, timeout=0.3)
portObj.flush()


def tick():
    msg = portObj.read(1)
    if len(msg) == 0:
        return None
    else:
        # there's byte of payload
        m.put_data(msg)


while 1:
    tick()
