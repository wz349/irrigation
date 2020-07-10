#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import serial
import paho.mqtt.client as mqtt
import json
import random

# thingsboard stuff
THINGSBOARD_HOST = '192.168.1.117'
# meter 1 API key
ACCESS_TOKEN_1 = 'GtFg0HV2F53PJIYYnJvq'
# meter 2 API key
ACCESS_TOKEN_2 = 'bzZox7sblxUTGbj3UZLQ'
# meter 3 API key
ACCESS_TOKEN_3 = 'FV2zkSgEOQMaFervqoEe'
# meter 4 API key
ACCESS_TOKEN_4 = 'kLZNJl76dNwpXVeHCzrl'
# meter 5 API key
ACCESS_TOKEN_5 = '04aN16Gi8vLdz9UsJTxU'



client_1 = mqtt.Client()
client_1.username_pw_set(ACCESS_TOKEN_1)
client_1.connect(THINGSBOARD_HOST, 1883, 60)
client_1.loop_start()

client_2 = mqtt.Client()
client_2.username_pw_set(ACCESS_TOKEN_2)
client_2.connect(THINGSBOARD_HOST, 1883, 60)
client_2.loop_start()

client_3 = mqtt.Client()
client_3.username_pw_set(ACCESS_TOKEN_3)
client_3.connect(THINGSBOARD_HOST, 1883, 60)
client_3.loop_start()

client_4 = mqtt.Client()
client_4.username_pw_set(ACCESS_TOKEN_4)
client_4.connect(THINGSBOARD_HOST, 1883, 60)
client_4.loop_start()

client_5 = mqtt.Client()
client_5.username_pw_set(ACCESS_TOKEN_5)
client_5.connect(THINGSBOARD_HOST, 1883, 60)
client_5.loop_start()

try:
	while(1):
		time.sleep(2)
		sensor_data = {'temperature': 0, 'water_stress': 0}
		temperature =  random.randrange(1,30)
		humidity = random.randrange(1,30)
		sensor_data['temperature'] = temperature
		sensor_data['water_stress'] = humidity
#		client_1.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
		temperature =  random.randrange(1,30)
                humidity = random.randrange(1,30)
                sensor_data['temperature'] = temperature
                sensor_data['water_stress'] = humidity
		client_2.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
		temperature =  random.randrange(1,30)
                humidity = random.randrange(1,30)
                sensor_data['temperature'] = temperature
                sensor_data['water_stress'] = humidity
		client_3.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                temperature =  random.randrange(1,30)
                humidity = random.randrange(1,30)
                sensor_data['temperature'] = temperature
                sensor_data['water_stress'] = humidity
		client_4.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                temperature =  random.randrange(1,30)
                humidity = random.randrange(1,30)
                sensor_data['temperature'] = temperature
                sensor_data['water_stress'] = humidity
		client_5.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

		print("working")

except KeyboardInterrupt:
	client_1.loop_stop()
	client_1.disconnect()
