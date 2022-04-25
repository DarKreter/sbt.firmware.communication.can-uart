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


# Serial init
portObj = serial.Serial(port=args.uart_interface, baudrate=115200, timeout=0.3)
portObj.flush()

print("GO!")

while 1:
    for msg in my_bus:
        bytes = can_frame_to_bytes(msg)

        print("gonna send!")
        print(bytes)
        portObj.write(bytes)