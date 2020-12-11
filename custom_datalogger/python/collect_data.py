#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import serial
import requests
import paho.mqtt.client as mqtt
import json

# test function. No usage in real collection

def blink():
	GPIO.output(14,1)
	time.sleep(.5)
	GPIO.output(14,0)
	time.sleep(.5)

#  Address and data and different fromat. Mainly to accomendate data that is longer than 1 byte

def sendAddress(a):
  GPIO.output(4,GPIO.HIGH)
  time.sleep(.5)
  ser.write(chr(a | 0x80))

def sendData(d):
    GPIO.output(4,GPIO.HIGH)
    time.sleep(.5)
    first = 0
    current = 0
    rest = 0
    if(d > 0x3F):                            # if data is greater than 6 bits and need extended mode
        rest = d
        first = 1
        while(rest is not 0):
            current = rest & 0x3F              # gets rid of everthing but last 6 bits
            rest = rest >> 6
            if(first or (rest == 0)):
                current = current | 0x40         # places 1 in 6th bit to indicate start or end of "extended" transmission
                first = ~first

            ser.write(chr(current))

    else:
        ser.write(chr(d))

# Passive mode to listen to the bus. return a integer “data”

def listen():
    # decide if the transmitted address is the same as this machines ADDRESS
    GPIO.output(4, GPIO.LOW)
    more = False
    last = True
    i = 0
    while True:
      while(ser.in_waiting > 0):
          address = ord(ser.read(1))
          #print "Address: ", bin(address)
          if(address >> 7):
  				# get rid of 7th bit (address bit)
              address = address & 0x7F
              if(address == ADDRESS):
                  while(1):
                      if(ser.in_waiting > 0):
                          data = ord(ser.read(1))
          print "Input: ", bin(data)
  							# if another address is transmitted than stop listening
                          if(data >> 7):
                              break
  							# if tranmission is start or end of extended mode
                          if(data >> 6):
  								# get rid of 6th bit (extended bit)
                              data = data & 0x3F
  								# if this is the start of extended mode
                              if(more == False):
                                  buffer = data
  				  #print(buffer)					#print "* ", bin(buffer)
                                  last = more
                                  more = True
  								# else this is the end of extended mode
                              else:
                                  i = i+1
                                  buffer = (data << (6*i)) | buffer
  				  #print "! ", bin(buffer)
                                  data = buffer
                                  last = more
                                  more = False
  							# else this is either a normal transmission or in the middle of extended mode
                          else:
                              last = more
  							# if transmission is done, whether normal or extended mode
                          if (more == False):
  								# print data and write to file
                              print data, " ", bin(data)
                              #f.write("%d, " % data)
                              #url = "https://api.thingspeak.com/update.json?api_key=" + API_KEY + "&field1=" + str(data)
                              #response = requests.get(url)
                              buffer = 0
                              more = False
                              last = False
                              i=0
                              return data
  							# else if this is the middle of extended mode
                          elif((more == True) and (last == True)):
                              i= i+1
                              buffer = (data << (6*i)) | buffer


# define serial parameters
# use seiral0 --> for UART at GPIO
# use ttyUSB0, ttyUSB1 --> for connection through serial to usb dongles

port = "/dev/serial0"
#port = "/dev/ttyACM0"
ser = serial.Serial(port, 9600)

# set GPIO parameters
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

# create/open csv file and append
f = open("input.csv","a+")

# thingspeak stuff
#API_KEY = "9VY9ICR776NZBLM8"

# thingsboard stuff
THINGSBOARD_HOST = '3.128.34.25'
ACCESS_TOKEN  = 'H7A7h79eenFkKWApFY4B'
ACCESS_TOKEN2 = 'U2eO2SUSixY2dLHrWo1q'

sensor_data = {'temperature': 0, 'water_stress': 0}
payload = {'prtR':0,'brgSig':0}
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

client2 = mqtt.Client()
client2.username_pw_set(ACCESS_TOKEN2)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client2.connect(THINGSBOARD_HOST, 1883, 60)
client2.loop_start()





# adc converion function input: 5(reference voltage), raw prtVal, raw brgVal

def adcConversion(refV,prtVal,brgVal):

    # convert adcVal to voltage

    refVal = 2**14                                  # adc reading when 0 Volts is measured
    prtV = ((float)(prtVal-refVal))/refVal*5
    brgRefV = 5*2347.0/(22000.0+2347.1)             # will change later to account for varies in reference R
    brgV = ((float)(brgVal-refVal))/refVal*5/128    # the bridge signal is amplified by 128
    brgSig = brgV/brgRefV*1000*100                  # brgSig measured in ratio * 1000
    print "prtV=",prtV, "brgV=",brgV, "brgRefV=" ,brgRefV, "brgSig=" ,brgSig

    # convert voltage to R
    resRef = 22000
    prtR = ((float)(resRef*prtV))/(5-prtV)
    print "prtR=" ,prtR

    # coefficients
    bp     = 64.68
    mp     = -29.448
    bpt    = 2.44794
    mpt    = -0.0049445
    bt     = -288.74
    mt     =  0.18118
   
    # Temperature convertion

    T = bt + mt*prtR
   
    print("temp=",T)
    print("signal Voltage=",prtV)
    print("resistance =",prtR)
   
    # Calculate V0
   
    voT = bpt + mpt * T

    print "v0T=",voT

    # Calculate P
    P = mp*(brgSig-voT) + bp

    return(prtR,brgSig)                             # return resistance and bridge signal for now, can switch to pressure and temperature.




# initalize variables
more = False
last = True
i = 0
ADDRESS = 4
role = 1

toggle = 1

try:
  while(1):
  	for i in range(3):
      # reduce the frequency of uploading data to the cloud but keep a higher frequency to record data locally.
	  	current_sensor =6 # address of datalogger
      while (current_sensor<8):
        time.sleep(1)
        sendAddress(current_sensor)
        print "ad " , current_sensor
        time.sleep(1)
        sendData(2)
        print "cmd 2"
        time.sleep(1)
        sensor_data['water_stress'] = listen()
        time.sleep(1)
        sendAddress(current_sensor)
        print "ad ", current_sensor
        time.sleep(1)
        sendData(3)
        print "cmd 3"
        time.sleep(1)
        sensor_data['temperature'] = listen()
        (T,P) = adcConversion(5,sensor_data['temperature'],sensor_data['water_stress'])
        (payload['prtR'],payload['brgSig']) = adcConversion(5,sensor_data['temperature'],sensor_data['water_stress'])
        print "temp = ",T,"pressure = ", P
        if i == 2 :
          if current_sensor == 6 :
          # currently only one sensor available
                client.publish('v1/devices/me/telemetry', json.dumps(payload), 1)
            if current_sensor == 7 :
                client2.publish('v1/devices/me/telemetry', json.dumps(payload), 1)
        current_sensor+=1

  time.sleep(300)

except KeyboardInterrupt:
GPIO.cleanup()
client.loop_stop()
client.disconnect()
f.close()
GPIO.cleanup()

