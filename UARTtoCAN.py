#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __headers__ import *

# Call parameters
parser = argparse.ArgumentParser()
parser.add_argument("--can_socket", type=str,
                    help="can0 or vcan0", required=True)
parser.add_argument("--uart_interface", type=str, required=True,
                    help="ie. /dev/ttyUSB0")
args = parser.parse_args()

# Init can socket
can.rc['interface'] = 'socketcan'
can.rc['channel'] = args.can_socket
can.rc['bitrate'] = 250000
my_bus = Bus()

def my_on_rx(frame: can.Message):
    print("Received frame:")
    print("{}#{}".format(frame.arbitration_id, frame.data))
    my_bus.send(msg=frame)
    
m = rx_machinery(my_on_rx)


# Serial init
portObj = serial.Serial(port=args.uart_interface, baudrate=115200, timeout=0.5)
portObj.flush()

print("GO")

while 1:
    msg = portObj.read(1)
    if len(msg) == 0:
        continue
    else:
        # there's byte of payload
        m.put_data(msg)
