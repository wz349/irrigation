#encoding: utf-8 -*-
"""
Read weather station data through serial port from CR6 and publish them on thingsboard

@author: Weichen Zhou (based on previous version by Coretib)
"""

import time
import json
import numpy as np
import serial
import paho.mqtt.client as mqtt
import json
import re
import math
from datetime import datetime


THINGSBOARD_HOST = '3.19.237.92' # thingsboard server ip address
ACCESS_TOKEN  = 'WjTy34T0DNH8gcNKmE1O'	# thingsboard device access_token
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN) 
client.connect(THINGSBOARD_HOST, 1883, 60) # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.loop_start()

# define serial parameters
# use seiral0 --> for UART at GPIO
# use ttyUSB0, ttyUSB1 --> for connection through serial to usb dongles

ser = serial.Serial(
		port='/dev/serial0',  # UART through GPIO pins
		baudrate = 4800,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1.0
)

payload = {}

i=0

epoch = datetime.utcfromtimestamp(0)


# this function read the output from CR6 and disect it into different value

def readCR6(payload):
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
	payload["RH"] = float(RH[0])
	now = datetime.now()
	payload["timestamp"] = (now-epoch).total_seconds() * 1000.0 
	payload["VPDkPa"] = calculateVPD(payload)

# this function locally store data that is collected from CR6

def recordLocal(payload):
	with open('weather_data.json','a') as outfile:
		json.dump(payload,outfile)

# This function use Room Temperature and Relative Humidity to calculate VPD

def calculateVPD(payload):
	A=17.2693882 #Constant for calculating Psat in kPa
	B=35.86 #Constant
	C=0.61078 #Constant
	airTKM = payload['RoomT']+273.15
	airRHM = payload['RH']
	Psat=C*math.exp(A*(airTKM-273.15)/(airTKM-B)) #kPa
	VPDkPa=(100-airRHM)/100*Psat #kPa                           
	#VPDPa=VPDkPa*10**3 #Pa
	return VPDkPa

# main funciton

while 1:
	try:
		while 1:
			while ser.inWaiting():
				i+=1
				readCR6(payload)
				recordLocal(payload)
				if i == 1 :   # set this number higher if there is need to reduce frequency of uploading data to the cloud
					client.publish('v1/devices/me/telemetry', json.dumps(payload), 1)

					i = 0
	except:
		# instead of crashing the function, record error and try again(need to make specific error message later)
		time.sleep(60)
		with open('error.log','a') as errorlog:
			now = datetime.now()
			errorlog.write(str((now-epoch).total_seconds() * 1000.0))
			errorlog.write('error occured \n')
		time.sleep(60)
		pass
