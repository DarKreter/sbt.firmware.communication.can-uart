#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import can
from can.interface import Bus

import pyserial

from myFrames import rx_machiery


# ARGV handling
import sys
if len(sys.argv) != 3:
    print(sys.argv[0]+' canIf uartIf')
    sys.exit('')

can_interface = sys.argv[1]
uart_interface = sys.argv[2]

print("CAN:  {}".format(can_interface))
print("UART: {}".format(uart_interface))


port = uart_interface

# can init
can.rc['interface'] = 'socketcan_native'
can.rc['channel'] = can_interface

my_bus = Bus()


def my_on_rx(frame: can.Message):
    print("WYSOKO")
    print(frame)
    my_bus.send(msg=frame)


m = rx_machiery(my_on_rx)

# serial init
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
