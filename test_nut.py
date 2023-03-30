#test button
import RPi.GPIO as GPIO
import the_tu
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reader = SimpleMFRC522()

while True:
    if (GPIO.input(10) == GPIO.LOW):
        print("button 10 pressed")
        break
    #id, text = reader.read()
    #print(id,text)