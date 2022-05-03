#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from can_bytes_converter import *
import serial
from time import sleep

# from rx_machinery import rx_machiery


def my_on_rx(frame: can.Message):
    print("WYSOKO")
    print(frame)
    # my_bus.send(msg=frame)


m = rx_machiery(my_on_rx)

extID_input = 12
payload_input = bytearray(b'x2y4\\\\78')
print("{}#{}".format(extID_input, payload_input))

output = id_payload_to_bytes(extID_input, payload_input)

extID_output, payload_output = bytes_to_id_payload(output)

print("{}#{}".format(extID_output, payload_output))
