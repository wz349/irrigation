#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import serial
import paho.mqtt.client as mqtt
import json

def blink():
	GPIO.output(14,1)
	time.sleep(.5)
	GPIO.output(14,0)
	time.sleep(.5)

def sendAddress(a):
  GPIO.output(4,GPIO.HIGH)                # enable DE/RO pin for transmit 
  time.sleep(.5)
  ser.write(chr(a | 0x80))                # send address with 1 in MSB place

def sendData(d):
    GPIO.output(4,GPIO.HIGH)              # enable DE/RO pin for transmit
    time.sleep(.5)
    first = 0
    current = 0
    rest = 0
    if(d > 0x3F):                         # if data is greater than 6 bits then start extended mode
        rest = d
        first = 1
        while(rest is not 0):             # while the next transmission is not empty, keep transmitting
            current = rest & 0x3F         # gets rid of everthing but last 6 bits
            rest = rest >> 6
            if(first or (rest == 0)):
                current = current | 0x40  # places 1 in 6th bit to indicate start or end of extended mode
                first = ~first

            ser.write(chr(current))

    else:                                 # else transmit data as is
        ser.write(chr(d))

def listen():
    GPIO.output(4, GPIO.LOW)                                   # make sure DE/RO pin is low for receiving
    more = False
    last = True
    i = 0
    while True:
      while(ser.in_waiting > 0):                               # while there is stuff to read
          address = ord(ser.read(1))                           # read one byte and convert to char for comparisons
         #print "Address: ", bin(address)                      # print debug to show binary value of address
          if(address >> 7):                                    # if MSB is a 1
              address = address & 0x7F                         # get rid of 7th bit (address bit)
              if(address == ADDRESS):                          # if transmitted address matches this device's address
                  while(1):                                    # listen for data
                      if(ser.in_waiting > 0):                  # if there is stuff to read
                          data = ord(ser.read(1))              # read one byte and convert to char for comparisons
  			                  #print "Input: ", bin(data)
                          if(data >> 7):                       # if another address is transmitted than stop listening
                              break
                          if(data >> 6):                       # if 6th bit is a 1
                              data = data & 0x3F               # get rid of 6th bit (extended bit)
                              if(more == False):               # more starts at False, toggled after entering extended mode, and toggled after exiting
                                  buffer = data
                                  last = more
                                  more = True
                              else:                            # else this is the end of extended mode
                                  i = i+1
                                  buffer = (data << (6*i)) | buffer       # add current transmission to previous ones
                                  data = buffer
                                  last = more
                                  more = False
                          else:                                # else this is either a normal transmission or in the middle of extended mode 
                              last = more
                          if (more == False):                  # if transmission is done, whether normal or extended mode
                              print data, " ", bin(data)       # print data and write to file if uncommented
                              #f.write("%d, " % data)
                              buffer = 0
                              more = False
                              last = False
                              i=0
                              return data
                          elif((more == True) and (last == True)):        # else if this is the middle of extended mode
                              i= i+1
                              buffer = (data << (6*i)) | buffer




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    client.subscribe('v1/devices/me/rpc/response/+')
    # Sending current irrigation status
    client.publish('v1/devices/me/attributes', get_irrigation_status(), 1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print 'Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload)
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'setValue1':
        set_irrigation_status(1, data['params'])
        client.publish(msg.topic.replace('request','response'), get_irrigation_status(), 1)
        client.publish('v1/devices/me/attributes', get_irrigation_status(), 1)
        print get_irrigation_status()
    elif data['method'] == 'setValue2':
        set_irrigation_status(2, data['params'])
        client.publish(msg.topic.replace('request','response'), get_irrigation_status(), 1)
        client.publish('v1/devices/me/attributes', get_irrigation_status(), 1)
        print get_irrigation_status()
    elif data['method'] == 'checkStatus':
        client.publish(msg.topic.replace('request','response'), get_irrigation_status(), 1)
        client.publish('v1/devices/me/attributes', get_irrigation_status(), 1)
        print get_irrigation_status()
    else:
        print('Unknown method: '+ data['method']) 

# Get current irrigation status as a dictionary
def get_irrigation_status():
    return json.dumps(irrigation_state)

# Set valve to on of off
def set_irrigation_status(valve, status):
    irrigation_state["value"+ str(valve)] = status
    if(valve == 1): GPIO.output(26, status)
    elif(valve == 2): GPIO.output(16, status)




# Define serial parameters
port = "/dev/serial0"
ser = serial.Serial(port, 9600)

# Set GPIO parameters
GPIO.setmode(GPIO.BCM)
# RS485 enable pin
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
# LED output
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)


# create/open csv file and append
f = open("input.csv","a+")



# thingsboard stuff
THINGSBOARD_HOST = 'demo.thingsboard.io'
# Barometer 7 API key
ACCESS_TOKEN_7 = '9vVrDcjXdKgqCLJybDaZ'
# Barometer 6 API key
ACCESS_TOKEN_6 = '1Grgt8krPI6PvNTGQz8W'
# Pi API key
ACCESS_TOKEN_PI = 'WtTT49JhTMCWgxPAb6Hv'

sensor_data = {'temperature': 0, 'humidity': 0}
irrigation_state = {"value1": False, "value2": False}

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client_7 = mqtt.Client()
client_7.username_pw_set(ACCESS_TOKEN_7)
client_7.connect(THINGSBOARD_HOST, 1883, 60)
client_7.loop_start()

client_6 = mqtt.Client()
client_6.username_pw_set(ACCESS_TOKEN_6)
client_6.connect(THINGSBOARD_HOST, 1883, 60)
client_6.loop_start()

client_pi = mqtt.Client()
# Register connect and message callback only for Pi
client_pi.on_connect = on_connect
client_pi.on_message = on_message
client_pi.username_pw_set(ACCESS_TOKEN_PI)
client_pi.connect(THINGSBOARD_HOST, 1883, 60)
client_pi.loop_start()


# Initalize variables
more = False
last = True
i = 0
ADDRESS = 4
role = 1

# Toggles which sensor to read from
toggle = 1

try:
  while(1):
    time.sleep(.5)
    if(toggle):
        sendAddress(6)
        print "Connecting to sensor 6 (ad 6)..."
    else:
        sendAddress(7)
        print "Connecting to sensor 7 (ad 7)..."
    time.sleep(.5)
    sendData(2)
    print "Requesting humidity (cmd 2)..."
    time.sleep(.5)
    print "Humidity = "
    sensor_data['humidity'] = listen()
    time.sleep(.5)
    if(toggle):
        sendAddress(6)
        print "Connecting to sensor 6 (ad 6)..."
    else:
        sendAddress(7)
        print "Connecting to sensor 7 (ad 7)..."
    time.sleep(.5)
    sendData(3)
    print "Requesting temperature (cmd 3)..."
    time.sleep(.5)
    print "Temperature = "
    sensor_data['temperature'] = listen()
    if(toggle):
        client_6.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    else:
        client_7.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    toggle = not toggle

except KeyboardInterrupt:
	GPIO.cleanup()
  client_6.loop_stop()
  client_6.disconnect()
	client_7.loop_stop()
	client_7.disconnect()
	client_pi.loop_stop()
	client_pi.disconnect()
  f.close()
  GPIO.cleanup()
