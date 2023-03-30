#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def RFID_read():
    reader = SimpleMFRC522()

    try:
        id, text = reader.read()
        #print(id)
        #print(text)
        if len(text) >0:
            return [id,text,True]
        else:
            return [0,"",False]
        
    except:
        print("Loi the tu")
        return [0,"",False]
        
        
def RFID_write():
    reader = SimpleMFRC522()

    try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
    
    except:
        print("Loi the tu")    
