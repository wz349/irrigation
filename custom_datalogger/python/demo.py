#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import serial
import requests

def blink():
	GPIO.output(14,1)
	time.sleep(.5)
	GPIO.output(14,0)
	time.sleep(.5)
 
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
 
def listen():
    # decide if the transmitted address is the same as this machines ADDRESS
    GPIO.output(4, GPIO.LOW)
    more = False
    last = True
    i = 0
    while True:
      while(ser.inWaiting()):
          address = ord(ser.read(1))
          if(address >> 7):
  				# get rid of 7th bit (address bit)
              address = address & 0x7F
              if(address == ADDRESS):
                  while(1):
                      if(ser.inWaiting()):
                          data = ord(ser.read(1))
  			#print "Input: ", bin(data), " ", more
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
  									#print "* ", bin(buffer)
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
                              url = "https://api.thingspeak.com/update.json?api_key=" + API_KEY + "&field1=" + str(data)
                              response = requests.get(url)
                              buffer = 0
                              more = False
                              last = False
                              i=0
  							# else if this is the middle of extended mode
                          elif((more == True) and (last == True)):
                              i= i+1
                              buffer = (data << (6*i)) | buffer


# define serial parameters
port = "/dev/serial0"
#port = "/dev/ttyACM0"
ser = serial.Serial(port, 9600)

# set GPIO parameters
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

# create/open csv file and append
f = open("input.csv","a+")

# thingspeak stuff
API_KEY = "9VY9ICR776NZBLM8"

# initalize variables
more = False
last = True
i = 0
ADDRESS = 4

try:
  #sendAddress(6)
  #print "sent ad 6"
  #time.sleep(1)
  #sendData(100)
  time.sleep(1)
  sendAddress(3)
  print "sent ad 3"
  time.sleep(2)
  sendData(2)
  print "sent 2"
  time.sleep(4)
  #time.sleep(4)
  #sendData(2)
  #print "sent 88"
  listen()
  time.sleep(5)
  
except KeyboardInterrupt:
	GPIO.cleanup()
	f.close()

