from time import sleep
import argparse
import can
from can.interface import Bus
import serial
from can_bytes_converter import *
from rx_machinery import rx_machinery