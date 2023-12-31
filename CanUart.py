#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __headers__ import *
from can_bytes_converter import *
from rx_machinery import rx_machinery

class Direction(Enum):
    can2uart = 'can2uart'
    uart2can = 'uart2can'
    bidirectional = 'bidirectional'

# Call parameters
parser = argparse.ArgumentParser()
parser.add_argument("--can_socket", type=str,
                    help="can0 or vcan0", required=True)
parser.add_argument("--uart_interface", type=str, required=True,
                    help="ie. /dev/ttyUSB0")
parser.add_argument("--direction", type=Direction, choices=list(Direction), default=Direction.bidirectional,
                    help="direction of communication: \"can2uart\", \"uart2can\" or \"bidirectional\"")
args = parser.parse_args()


# Init can socket
can.rc['interface'] = 'socketcan'
can.rc['channel'] = args.can_socket
can.rc['bitrate'] = can_baudrate
my_bus = Bus()

def my_on_rx(frame: can.Message):
    print("Received frame:")
    print("{}#{}".format(frame.arbitration_id, frame.data))
    my_bus.send(msg=frame)
    
m = rx_machinery(my_on_rx)


# Serial init
portObj = serial.Serial(port=args.uart_interface, baudrate=115200, timeout=0.5)
portObj.flush()

def Uart2Can():
    while 1:
        try:
            msg = portObj.read(1)
            if len(msg) == 0:
                continue
            else:
                # there's byte of payload
                m.put_data(msg)
        except Exception as e:
            print("Error!!!")
            print(e)


def Can2Uart():
    while 1:
        for msg in my_bus:
            try:
                bytes = can_frame_to_bytes(msg)

                print("gonna send!")
                print(bytes)
                portObj.write(bytes)
            except Exception as e:
                print("Unknown frame: {}#{}".format(msg.arbitration_id, msg.data))
                print("Error: {}".format(e))
                print()


threads = []

if args.direction == Direction.bidirectional or args.direction == Direction.uart2can:
    threads.append(threading.Thread(target=Uart2Can))
    
if args.direction == Direction.bidirectional or args.direction == Direction.can2uart:
    threads.append(threading.Thread(target=Can2Uart))
    
print("GO!")

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()