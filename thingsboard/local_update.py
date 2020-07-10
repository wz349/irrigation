#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import serial
import paho.mqtt.client as mqtt
import json
import random


# thingsboard stuff
THINGSBOARD_HOST = '192.168.1.117'
# fake_sensor 1  API key
ACCESS_TOKEN_1 = "GtFg0HV2F53PJIYYnJvq"

client_1 = mqtt.Client()
client_1.username_pw_set(ACCESS_TOKEN_1)
client_1.connect(THINGSBOARD_HOST, 1883, 60)
client_1.loop_start()
sensor_data = {'temperature': 0, 'humidity': 0}

try:
	while(1):
		time.sleep(2)
		data = random.randrange(1,30)
		sensor_data['temperature'] = data
		data = random.randrange(1,30)
		sensor_data['humidity'] = data
		client_1.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
		print('sending message to local server')
except KeyboardInterrupt:
	client_1.loop_stop()
	client_1.disconnect()
