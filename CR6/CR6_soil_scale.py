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
from datetime import datetime

# define serial parameters
# use seiral0 --> for UART at GPIO
# use ttyUSB0, ttyUSB1 --> for connection through serial to usb dongles

ser = serial.Serial(
		port='/dev/ttyUSB0',
		baudrate = 4800,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1.0
)



# thingsboard stuff

THINGSBOARD_HOST = '3.19.237.92' # thingsboard server ip address
ACCESS_TOKEN  = 'H7A7h79eenFkKWApFY4B' # thingsboard device access_token
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

payload = {}
i=0
epoch = datetime.utcfromtimestamp(0)

# this function read the output from CR6 and disect it into different value

def readCR6(payload):
	x = ser.readline()
	list =x.split(';')
	print(list)
	soil = list[9].split(',')
	print(soil)
	floatsoil = float(soil[0])
	print(floatsoil)
	payload["SoilSensor1"] = float(soil[0])
	payload["SoilSensor2"] = float(soil[1])
	payload["SoilSensor3"] = float(soil[2])
	payload["SoilSensor4"] = float(soil[3])
	payload["SoilSensor5"] = float(soil[4])
	payload["SoilSensor6"] = float(soil[5])
	payload["SoilSensor7"] = float(soil[6])
	payload["SoilSensor8"] = float(soil[7])
	payload["SoilSensor9"] = float(soil[8])
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
	now = datetime.now()
	payload["timestamp"] = (now-epoch).total_seconds() * 1000.0 

# this function locally store data that is collected from CR6

def recordLocal(payload):
	with open('soil_data.json','a') as outfile:
		json.dump(payload,outfile)

# main 

try:
	while 1:
		try:
			while ser.inWaiting():
				readCR6(payload)
				recordLocal(payload)
				client.publish('v1/devices/me/telemetry', json.dumps(payload), 1)

		except:
			# instead of crashing the function, record error and try again(need to make specific error message later)
			with open('error.log','a') as errorlog:
				now = datetime.now()
				errorlog.write(str((now-epoch).total_seconds() * 1000.0))
				errorlog.write('error occured \n')
			time.sleep(5)
			pass

except KeyboardInterrupt:
	client.loop_stop()
	client.disconnect()
