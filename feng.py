#coding=utf8
import RPi.GPIO as GPIO
import time
import send

def init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(18,GPIO.OUT)
	GPIO.setup(7,GPIO.OUT)
	GPIO.output(7,GPIO.LOW)
	pass
def beep():
	GPIO.output(18,GPIO.HIGH)
	GPIO.output(7,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(7,GPIO.LOW)
	GPIO.output(18,GPIO.LOW)
	time.sleep(0.5)
def begin():
	time.sleep(2)
	init()
	for i in range(1,10):
		a = send.rece()
		if (a == 1):
			GPIO.output(7,GPIO.LOW)
			GPIO.output(18,GPIO.LOW)
			break
		else:
			beep()
	GPIO.cleanup()


