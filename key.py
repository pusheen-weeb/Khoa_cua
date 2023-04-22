import RPi.GPIO as GPIO
import time
R1 = 37
R2 = 36
R3 = 38
R4 = 40

C1 = 35
C2 = 33
C3 = 31
C4 = 29
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

password ="1234"
inputstring = ""
hidekey=""

input= ""


def readline(line, characters):
    char = None
    GPIO.output(line, GPIO.HIGH)
    time.sleep(0.02)
    if(GPIO.input(C1) == 1):
        #inputstring = inputstring +characters[0]
        #hidekey = hidekey +characters[0]
        #print(hidekey)
        char = characters[0]
        
    elif(GPIO.input(C2) == 1):
        #inputstring = inputstring +characters[1]
        #hidekey = hidekey +characters[1]
        #print(hidekey)
        char = characters[1]
       
    elif(GPIO.input(C3) == 1):
        #inputstring = inputstring +characters[2]
        #hidekey = hidekey +characters[2]
        #print(hidekey)
        char = characters[2]
       
      
    elif(GPIO.input(C4) == 1):
        char = characters[3]
        
           
    GPIO.output(line, GPIO.LOW)
    time.sleep(0.02)
    return char

def read_key():
    char = readline(R1, ["1","2","3","/"])
    if char == None:
        char = readline(R2, ["4","5","6","+"])
    if char == None:
        char = readline(R3, ["7","8","9","-"])
    if char == None:
        char = readline(R4, ["c","0","=","#"])
    return char
    
def pass_check(char,pass_):
    global inputstring
    global hidekey
    if(char ==  "#"):
            if(inputstring == pass_): # nếu mật khẩu đúng
                print("pass dung\n")
                inputstring = ""
                hidekey= ""
                return True
            else:
                print(" PASSWORD FALSE \n")
                
                time.sleep(1)
             
                inputstring = ""
                hidekey= ""
                return False
    else:
        inputstring = inputstring + char
        hidekey = hidekey + char
        print(hidekey)
    return False

#delay = 5


#print("HELLO")

#time.sleep(1)
#print("ENTER PASSWORD")

#time.sleep(1)   
#while True:
    #char = readline(R1, ["7","8","9","/"])
    #if char == None:
        #char = readline(R2, ["4","5","6","*"])
    #if char == None:
        #char = readline(R3, ["1","2","3","-"])
    #if char == None:
        #char = readline(R4, ["C","0","=","#"])
    
    #if char != None:
       # print(pass_check(char))
        #char = None
    #stime.sleep(0.1)





