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

COEFF_MP = -47.31956
COEFF_BP = 252.593
COEFF_OFFSET = 4.83
COEFF_BT =  -296.2587
COEFF_MT = 0.2010998
COEFF_BPT = 5.555694
COEFF_MPT = -0.00636919

COEFF_MP3 = -47.31956
COEFF_BP3 = 252.593
COEFF_OFFSET3 = 4.83
COEFF_BT3 = -333.6849448
COEFF_MT3 = 0.2367422265
COEFF_BPT3 = 5.555694
COEFF_MPT3 = -0.00636919



def readCR6(payload):
	x = ser.readline()
	list =x.split(';')
	print(list)
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
	payload["water_stress_test"] = (float(br1[4])-COEFF_OFFSET)*COEFF_MP
	#payload["timestamp"] = (now-epoch).total_seconds() * 1000.0 
	payload["temperature"] =  float(prt1[4])*COEFF_MT+ COEFF_BT
	#payload["water_stress_test3"] = (float(br1[4])-COEFF_OFFSET)*COEFF_MP
        payload["temperature3"] =  float(prt1[2])*COEFF_MT3+ COEFF_BT3
	print("cp.5")
	payload["w_s"] =(float(br1[4])- ((payload["temperature"])*COEFF_MPT + COEFF_BPT))*COEFF_MP + COEFF_BP
	print("cp1")
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
