import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

r1 = 15#led 1
r2 = 13#led 2
r3 = 11#led 3
r4 = 7 #khoa cua

GPIO.setup(r1, GPIO.OUT)
GPIO.setup(r2, GPIO.OUT)
GPIO.setup(r3, GPIO.OUT)
GPIO.setup(r4, GPIO.OUT)

def control_relay(c1=False,c2=False,c3=False,c4=False):
    if c1 == True:
        GPIO.output(r1,False)        
    else:
        GPIO.output(r1,True)
        
    if c2 == True:
        GPIO.output(r2,False)        
    else:
        GPIO.output(r2,True)
        
    if c3 == True:
        GPIO.output(r3,False)        
    else:
        GPIO.output(r3,True)
        
    if c4 == True:
        GPIO.output(r4,False)
    else:
        GPIO.output(r4,True)
        