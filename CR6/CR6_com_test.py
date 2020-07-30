#encoding: utf-8 -*-
"""
Created on Fri May 17 12:22:07 2019

@author: Coretib
"""

import time
import json
import numpy as np
import serial

ser = serial.Serial(
        port=r'/dev/ttyS0',
        baudrate = 4800,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1.0
)

i=0
while 1:
    print(i)
    i+=1
    x=ser.readline()

    print (x)
