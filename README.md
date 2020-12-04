# irrigation

Files:

/connect_internet.py    : Check the internet connection after x minutes. Reboot 3g-dongle if connection lost. 

/irrigation_routine.py  : Irrigate certain amount based on flow rate. Run by cron each day

/CR6/CR6_sensors.py     : Communicating with CR6 that was connected to sensors, uploading to thingsboard. Data conversion included

/CR6/CR6_soil_scale     : Communicating with CR6 that was connected to soild sensors and digital scale, uploading to thingsboard.

/CR6/CR6_weather_station.py : Communicating with CR6 that was connected to weater station,  uploading to thingsboard.

/thingsboard/GPIO.py  : Coordinate with thingsboard gadget to control GPIO pins on PI remotely. Used to control valves this summer.

