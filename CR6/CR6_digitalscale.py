#encoding: utf-8 -*-
"""
Created on Fri May 17 12:22:07 2019

@author: Coretib
"""

import time
import json
import numpy as np
import serial
import paho.mqtt.client as mqtt
import json


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

THINGSBOARD_HOST = '3.19.237.92'
ACCESS_TOKEN  = 'H7A7h79eenFkKWApFY4B'

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()
try:
	while 1:
		while ser.inWaiting():
         		x = ser.readline()
       		 	list =x.split(';')
   			print(list)
      			weight = list[1].split(',')
      			print(weight)
      			intweight = int(weight[0])
      			print(intweight)
      			payload["weight"] = intweight
      			client.publish('v1/devices/me/telemetry', json.dumps(payload), 1)

except KeyboardInterrupt:
	GPIO.cleanup()
        client.loop_stop()
        client.disconnect()
