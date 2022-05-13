from time import sleep
import argparse
import can
import crc16
from can.interface import Bus
import serial
from enum import Enum
import threading
from shutil import ExecError

can_baudrate = 250000

start_byte = 'x'
end_byte = 'y'
escape_byte = '\\'

start_sequence_length = 3
end_sequence_length = 3

start_sequence_bytes = bytes(start_sequence_length * start_byte, 'ascii')
end_sequence_bytes = bytes(end_sequence_length * end_byte, 'ascii')