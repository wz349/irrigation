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
        port='/dev/serial0',
        baudrate = 4800,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1.0
)


payload = {}
i=0
while 1:
    while ser.inWaiting():
      x = ser.readline()
      list =x.split(';')
      print(list)
      weight = list[1].split(',')
      print(weight)
      intweight = int(weight[0])
      print(intweight)
