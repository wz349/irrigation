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
ACCESS_TOKEN  = 'WjTy34T0DNH8gcNKmE1O'

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()
i=0
while 1:
	try:
		while 1:
			while ser.inWaiting():
				i+=1
         			x = ser.readline()
       			 	list =x.split(';')
   				print(list)
      				weight = list[1].split(',')
      				print(weight)
				r = '\d+'
				temp = re.findall(r,weight[1])
				print(temp)
      				#intweight = int(temp[0])
    				#print(intweight)
      				#payload["weight"] = intweight
				print(list[15],list[17],list[19],list[21],list[23])
				PAR = list[16].split(',')
				payload["PAR_weatherstation"]= float(PAR[0])
				slrkW = list[18].split(',')
				payload["solar intensity"]= float(slrkW[0])
				windspeed = list[20].split(',')
				payload["wind speed"]=float(windspeed[0])
		 		RoomT = list[22].split(',')
	  			payload["RoomT"] = float(RoomT[0])
	  			RH	= list[24].split(',')
	  			payload["RH"]	   = float(RH[0])
				if i == 1 :
      					client.publish('v1/devices/me/telemetry', json.dumps(payload), 1)
					i = 0
				
	except:
		time.sleep(60)
		pass
