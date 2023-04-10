import RPi.GPIO as GPIO
import time
R1 = 31
R2 = 33
R3 = 35
R4 = 37

C1 = 40
C2 = 38
C3 = 36
C4 = 32
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

password ="9922"
inputstring = ""
hidekey=""

input= ""


def readline(line, characters):
    global inputstring
    global hidekey
    GPIO.output(line, GPIO.HIGH)
    time.sleep(0.02)
    if(GPIO.input(C1) == 1):
        inputstring = inputstring +characters[0]
        hidekey = hidekey +"*"
        print(hidekey)
        
    elif(GPIO.input(C2) == 1):
        inputstring = inputstring +characters[1]
        hidekey = hidekey +"*"
        print(hidekey)
       
    elif(GPIO.input(C3) == 1):
        inputstring = inputstring +characters[2]
        hidekey = hidekey +"*"
        print(hidekey)
   
      
    elif(GPIO.input(C4) == 1):
        if(characters[3] ==  "#"):
            if(inputstring == password): # nếu mật khẩu đúng
                print("OPEN gate\n")
              
                time.sleep(1)
       
               
                inputstring = ""
                hidekey= ""
            else:
                print(" PASSWORD FALSE \n AGAIN")
            
                time.sleep(1)
             
                inputstring = ""
                hidekey= ""
        else:
            inputstring = inputstring +characters[3]
            hidekey = hidekey +"*"
            print(hidekey)
           
    GPIO.output(line, GPIO.LOW)
    time.sleep(0.02)    


delay = 5


print("HELLO")

time.sleep(1)
print("ENTER PASSWORD")

time.sleep(1)   
while True:
    readline(R1, ["7","8","9","/"])
    readline(R2, ["4","5","6","*"])
    readline(R3, ["1","2","3","-"])
    readline(R4, ["C","0","=","#"])
    time.sleep(0.1)





