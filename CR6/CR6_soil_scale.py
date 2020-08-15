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
import re

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
		try:
			while ser.inWaiting():
         			x = ser.readline()
       			 	list =x.split(';')
   				print(list)
      				soil = list[9].split(',')
      				print(soil)
      				floatsoil = float(soil[0])
      				print(floatsoil)
      				payload["SoilSensor1"] = float(soil[0])
				payload["SoilSensor2"] = float(soil[1])
				payload["SoilSensor4"] = float(soil[3])
				payload["SoilSensor5"] = float(soil[4])
				payload["SoilSensor7"] = float(soil[6])
                	        payload["SoilSensor8"] = float(soil[7])
                	        payload["SoilSensor10"] = float(soil[9])
                	        payload["SoilSensor11"] = float(soil[10])
				temp = list[4].split(',')
                	        payload["SoilTemp"] = float(temp[0])
				weight = list[10].split(',')
				print(weight)
				r = '\d+'
				temp = re.findall(r,weight[1])
				intweight = int(temp[0])
    				print(intweight)
      				payload["weight"] = intweight
      				client.publish('v1/devices/me/telemetry', json.dumps(payload), 1)
		except:
			pass

except KeyboardInterrupt:
	client.loop_stop()
        client.disconnect()
