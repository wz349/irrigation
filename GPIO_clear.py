import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(11,True)
GPIO.output(12,True)
GPIO.output(13,True)
GPIO.output(15,True)
GPIO.cleanup()
