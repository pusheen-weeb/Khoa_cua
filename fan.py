import RPi.GPIO as GPIO
import time 
pwmpin = 19
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmpin, GPIO.OUT)
fan = GPIO.PWM(pwmpin, 100)
fan.start(0)

def fan():
	
	fan.ChangeDutyCycle(a)
	fan.stop()
			


