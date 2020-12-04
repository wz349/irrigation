# a routine irrigation operation 
# based on flow rate measured on 8/5/2020
# Author: Weichen Zhou

# TODO, change this to account for MPC

import RPi.GPIO as GPIO
import time
from datetime import datetime
import sys

irrigation_argv = sys.argv

# define the measured flow rate of drippers

VALVE1_FLOWRATE = 0.165
VALVE2_FLOWRATE = 0.1
VALVE3_FLOWRATE = 0.165
VALVE4_FLOWRATE = 0.175

VALVE_FLOWRATE = [
	0.165,
	0.1,
	0.165,
	0.17
]

# Goal volume of water irrigation

GOAL_VOLUME = 3.200

# Estimated Leak volume

ESTIMATED_LEAK 	= 0.200

# code part

GPIO.setmode(GPIO.BOARD)

# Four GPIO pins that controls irrigation

gpio_state = {11: True, 12: True, 13: True, 15: True}

# Set output mode for all GPIO pins

for pin in gpio_state:
	
	GPIO.setup(pin, GPIO.OUT)

# initialize as Ture, as the valve control is running on inversed logic (Ture = close, False = open)

GPIO.output(11,True)
GPIO.output(12,True)
GPIO.output(13,True)
GPIO.output(15,True)
time.sleep(5)

def irrigation_all(irrigation_amount) :

	start_time = time.time()
	GOAL_VOLUME = irrigation_amount
	# set flags 

	a=1
	b=1
	c=1
	d=1

	# Open all valves

	GPIO.output(11,False)
	GPIO.output(12,False)
	GPIO.output(13,False)
	GPIO.output(15,False)

	# Record irrigation in a document with date and time.

	f = open('irrigation_record','a')
	now = datetime.now()
	f.write(now.strftime("%m/%d/%Y, %H:%M:%S"))
	f.write('\n')

	# individually stop irrigation when the desiganated amount of water is irrgated.

	while a or b or c or d :
		if (GOAL_VOLUME-ESTIMATED_LEAK)/VALVE1_FLOWRATE * 60 <(time.time()-start_time) and a:
			GPIO.output(11,True)
			print(time.time()-start_time, '#1')
			a = 0
			f.write('#1 finished in ')
			f.write(str(time.time()-start_time))
			f.write('s\n')
		if (GOAL_VOLUME-ESTIMATED_LEAK)/VALVE2_FLOWRATE * 60 <(time.time()-start_time) and b :
			GPIO.output(13,True)
			print(time.time()-start_time, '#2')
			b = 0
			f.write('#2 finished in ')
			f.write(str(time.time()-start_time))
			f.write('s\n')
		if (GOAL_VOLUME-ESTIMATED_LEAK)/VALVE3_FLOWRATE * 60 <(time.time()-start_time) and c :
			GPIO.output(12,True)
			print(time.time()-start_time, '#3')
			c = 0
			f.write('#3 finished in ')
			f.write(str(time.time()-start_time))
			f.write('s\n')
		if (GOAL_VOLUME-ESTIMATED_LEAK)/VALVE4_FLOWRATE * 60 <(time.time()-start_time) and d:
			GPIO.output(15,True) 
			print(time.time()-start_time, '#4')
			d = 0
			f.write('#4 finished in ')
			f.write(str(time.time()-start_time))
			f.write('s\n')

	print('finish')
	f.close()

def GPIO_pin_switcher(i):
	switcher = {
		1:11,
		2:13,
		3:12,
		4:15
	}
	return switcher.get(i,"invalid")

def irrigation_single(tree,irrigation_amount) :
	# record start time
	start_time = time.time()
	GOAL_VOLUME = irrigation_amount

	# set flags 
	a=1

	# Open target valve
	pin = GPIO_pin_switcher(tree)
	GPIO.output(pin,False)

	# Record irrigation in a document with date and time.
	f = open('irrigation_record','a')
	now = datetime.now()
	f.write(now.strftime("%m/%d/%Y, %H:%M:%S"))
	f.write('\n')

	# individually stop irrigation when the desiganated amount of water is irrgated.
	while a :
		if (GOAL_VOLUME-ESTIMATED_LEAK)/VALVE_FLOWRATE[tree-1] * 60 <(time.time()-start_time) and a:
			GPIO.output(pin,True)
			print(time.time()-start_time,'#',tree)
			a = 0
			f.write(str(tree))
			f.write('finished in')
			f.write(str(time.time()-start_time))
			f.write('s\n')

	print('finish')
	f.close()

# read args
tree = irrigation_argv[1]
irrigation_amonut = irrigation_argv[2]

if tree == 'a' :
	irrigation_all(float(irrigation_amonut))
else:
	irrigation_single(int(tree), float(irrigation_amonut))
