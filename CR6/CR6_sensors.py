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
		port='/dev/serial0',
		baudrate = 4800,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1.0
)




THINGSBOARD_HOST = '3.19.237.92'
ACCESS_TOKEN  = 'H7A7h79eenFkKWApFY4B'

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

payload = {}
i=0
epoch = datetime.utcfromtimestamp(0)

#Coeff for sensor1 

COEFF_MP1 = -47.31956
COEFF_BP1 = 252.593
COEFF_OFFSET1 = 4.83
COEFF_BT1 = -333.6849448
COEFF_MT1 = 0.2367422265
COEFF_BPT1 = 5.555694
COEFF_MPT1 = -0.00636919

#Coeff for sensor2  

COEFF_MP2 = -47.31956
COEFF_BP2 = 252.593
COEFF_OFFSET2 = 4.83
COEFF_BT2 = -333.6849448
COEFF_MT2 = 0.2367422265
COEFF_BPT2 = 5.555694
COEFF_MPT2 = -0.00636919



#Coeff for sensor3  

COEFF_MP3 = -47.31956
COEFF_BP3 = 252.593
COEFF_OFFSET3 = 4.83
COEFF_BT3 = -333.6849448
COEFF_MT3 = 0.2367422265
COEFF_BPT3 = 5.555694
COEFF_MPT3 = -0.00636919

#Coeff for sensor4  

COEFF_MP4 = -47.31956
COEFF_BP4 = 252.593
COEFF_OFFSET4 = 4.83
COEFF_BT4 = -333.6849448
COEFF_MT4 = 0.2367422265
COEFF_BPT4 = 5.555694
COEFF_MPT4 = -0.00636919

# Coeff for sensor5

COEFF_MP5 = -47.31956
COEFF_BP5 = 252.593
COEFF_OFFSET5 = 4.83
COEFF_BT5 =  -296.2587
COEFF_MT5 = 0.2010998
COEFF_BPT5 = 5.555694
COEFF_MPT5 = -0.00636919



# this function read the output from CR6 and disect it into different value

def readCR6(payload):
	x = ser.readline() 							# read all output from CR6
	list =x.split(';')							# Example:  'FullBr =; 3.069614,2.62522,-2.713635,2.15358,7.79965,;Res =1632.696,-218.3582,1528.023,78.85131,1613.411,'
	print(list)									# Split by ';' and ',' to get values we need
	br1 = list[2].split(',')
	prt1 = list[4].split(',')
	payload["brgSig1"]= float(br1[0])
	payload["prt1"] = float(prt1[0])
	payload["brgSig2"]= float(br1[1])
	payload["prt2"] = float(prt1[1])
	payload["brgSig3"]= float(br1[2])
	payload["prt3"] = float(prt1[2])
	payload["brgSig4"]= float(br1[3])
	payload["prt4"] = float(prt1[3])
	payload["brgSig5"]= float(br1[4])
	payload["prt5"] = float(prt1[4])

	# conversions

	payload["water_stress_test"] = (float(br1[4])-COEFF_OFFSET5)*COEFF_MP5 # method suggested by prof Stroock
	#payload["timestamp"] = (now-epoch).total_seconds() * 1000.0 
	payload["temperature1"] =  float(prt1[0])*COEFF_MT1+ COEFF_BT1
	payload["temperature2"] =  float(prt1[1])*COEFF_MT2+ COEFF_BT2
	payload["temperature3"] =  float(prt1[2])*COEFF_MT3+ COEFF_BT3
	payload["temperature4"] =  float(prt1[3])*COEFF_MT4+ COEFF_BT4
	payload["temperature5"] =  float(prt1[4])*COEFF_MT5+ COEFF_BT5   # this is named 'temperature' becaues it is the first sensor we installed, should rename to temperature5
	#payload["water_stress_test3"] = (float(br1[4])-COEFF_OFFSET)*COEFF_MP
	
	print("cp.5")
	payload["w_s1"] =(float(br1[0])- ((payload["temperature1"])*COEFF_MPT1 + COEFF_BPT1))*COEFF_MP1 + COEFF_BP1
	payload["w_s2"] =(float(br1[1])- ((payload["temperature2"])*COEFF_MPT2 + COEFF_BPT2))*COEFF_MP2 + COEFF_BP2
	payload["w_s3"] =(float(br1[2])- ((payload["temperature3"])*COEFF_MPT3 + COEFF_BPT3))*COEFF_MP3 + COEFF_BP3
	payload["w_s4"] =(float(br1[3])- ((payload["temperature4"])*COEFF_MPT4 + COEFF_BPT4))*COEFF_MP4 + COEFF_BP4
	payload["w_s5"] =(float(br1[4])- ((payload["temperature5"])*COEFF_MPT5 + COEFF_BPT5))*COEFF_MP5 + COEFF_BP5
	print("cp1")

# this function locally store data that is collected from CR6

def recordLocal(payload):
	with open('sensor_data.json','a') as outfile:
		json.dump(payload,outfile)


try:
	while 1:
		try:
			while ser.inWaiting():
				readCR6(payload)
				recordLocal(payload)
				print("cp2")
				for i in range(4):
					if i == 3 :
						client.publish('v1/devices/me/telemetry', json.dumps(payload), 1)
				print("cp3")

		except:
			with open('error.log','a') as errorlog:
				now = datetime.now()
				errorlog.write(str((now-epoch).total_seconds() * 1000.0))
				errorlog.write('error occured \n')
			print('error')
			time.sleep(5)
			pass

except KeyboardInterrupt:
	client.loop_stop()
	client.disconnect()
