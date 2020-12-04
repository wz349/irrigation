# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:00:34 2019

@author: Coretib
"""
import os
from time import sleep
import paho.mqtt.client as mqtt


# thingsboard stuff
THINGSBOARD_HOST = '3.19.237.92'
ACCESS_TOKEN  = 'WjTy34T0DNH8gcNKmE1O'



experiment_running=True
myCmd1= 'sudo hologram modem disconnect'
myCmd2 = 'sudo hologram modem connect'
while experiment_running:
    received=False
    try:
	client = mqtt.Client()
	client.username_pw_set(ACCESS_TOKEN)
	# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
	client.connect(THINGSBOARD_HOST, 1883, 60)
	client.loop_start()
	print('connection normal')
    except:
	print('connection lost, reconnecting')
        #os.system(myCmd1)
        os.system(myCmd2)
    sleep(900)
