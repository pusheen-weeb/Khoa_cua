#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
GPIO.setwarnings(False)
reader = SimpleMFRC522.SimpleMFRC522()

def RFID_read():

    try:
        id, text = reader.read()
        #print(id)
        #print(text)
        if len(text) >0:
            return [id,text,True]
        else:
            return [0,"",False]
        
    except:
        #print("Loi the tu")
        return [0,"",False]
        
        
def RFID_write(text="default"):
    try: 
        #print("Now place your tag to write")
        reader.write(text)
        #print("Written")
    
    except:
        print("Loi the tu")    
def RFID_wipe():
    reader.wipe()