# a routine irrigation operation 
# based on flow rate measured on 8/5/2020
# Author: Weichen Zhou

import RPi.GPIO as GPIO
import time
from datetime import datetime

VALVE1_FLOWRATE = 0.165
VALVE2_FLOWRATE = 0.1
VALVE3_FLOWRATE = 0.165
VALVE4_FLOWRATE = 0.170

GOAL_VOLUME = 3.200

ESTIMATED_LEAK 	= 0.200

GPIO.setmode(GPIO.BOARD)

gpio_state = {11: True, 12: True, 13: True, 15: True}

for pin in gpio_state:
    # Set output mode for all GPIO pins
    GPIO.setup(pin, GPIO.OUT)
GPIO.output(11,True)
GPIO.output(12,True)
GPIO.output(13,True)
GPIO.output(15,True)

time.sleep(5)
start_time = time.time()
a=1
b=1
c=1
d=1

GPIO.output(11,False)
GPIO.output(12,False)
GPIO.output(13,False)
GPIO.output(15,False)
f = open('irrigation_record','a')
now = datetime.now()
f.write(now.strftime("%m/%d/%Y, %H:%M:%S"))
f.write('\n')
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
