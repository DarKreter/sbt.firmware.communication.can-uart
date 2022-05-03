#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from can_bytes_converter import *
import serial
from time import sleep
from rx_machinery import rx_machinery


def my_on_rx(frame: can.Message):
    print("\tReceived:\t{}#{}".format(frame.arbitration_id, frame.data))
    


m = rx_machinery(my_on_rx)

def all_tests():
    TEST.test_1(123456789 , b'12345678')
    TEST.test_1(123456789 , b'12345678')
    TEST.test_1(9123456789 , b'12345678') # Too long ID
    TEST.test_1(45824 , b'123456781234567812345678') # Too long payload
    TEST.test_1(12 , b'')
    TEST.test_1(123 , b'xxxxxxxx')
    TEST.test_1(123 , b'yyyyyyyy')
    TEST.test_1(123 , b'\\\\\\\\\\\\\\\\')
    TEST.test_1(123 , b'xy\\xxyyy')
    TEST.test_2(b'xxx\x0c\x00\x00\x0012345678i\x86yyy')
    TEST.test_2(b'xxx\x15\xcd[\x0712345678\xb8\xe4yyy') # invalid CRC
    TEST.test_2(b'xxx{\x00\x00\x00\\xx\\x\\x\\x\\x\\x\\x\x98\xbcyyy') # x in payload without escape byte
    TEST.test_2(b'xxx{\x00\x00\x00\\xy\\x\\x\\x\\x\\x\\x\x98\xbcyyy') # y in payload without escape byte
    TEST.test_2(b'xxx{\x00\x00\x00\\x\\w\\x\\x\\x\\x\\x\\x\x98\xbcyyy') # \ in payload without escape byte
    TEST.test_2(b'r2312asfxxx\x0c\x00\x00\x0012345678i\x86yyyf2fdsd') # Some trash before and after frame
    TEST.test_2(b'aw\\yxxx\x0c\x00\x00\x0012345678i\x86yyy') # escape byte in start sentence


class TEST:
    counter = 1
    @staticmethod
    def test_1(extID, payload):
        try:
            print()
            print(60*'-')
            print("Test #{}:".format(TEST.counter))
            TEST.counter += 1

            print("\tSending:\t{}#{}".format(extID, payload))
            
            output = id_payload_to_bytes(extID, payload)
            # print(output)
            m.put_data(output)
        except Exception as e:
            print('\033[91m' + "ERROR!")
            print(e)
            print('\033[0m', end = '')
            return
            
    @staticmethod
    def test_2(data):
        try:
            print()
            print(60*'-')
            print("Test #{}:".format(TEST.counter))
            TEST.counter += 1

            print("\tSending:\t{}".format(data))
            
            # print(data)
            m.put_data(data)
        except Exception as e:
            print('\033[91m' + "ERROR!")
            print(e)
            print('\033[0m', end = '')
            return
        
            


all_tests()
