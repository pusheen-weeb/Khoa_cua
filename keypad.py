import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD ) 
GPIO.setwarnings(False)

# các chân GPIO của rasp với LCD
LCD_RS = 3
LCD_E  = 5
LCD_D4 = 7
LCD_D5 = 11
LCD_D6 = 13
LCD_D7 = 15

# các chân GPIO của rasp với keypad

R1 = 37
R2 = 36
R3 = 38
R4 = 40

C1 = 35
C2 = 33
C3 = 31
C4 = 29



E_PULSE = 0.0005
E_DELAY = 0.0005
#password
secretkey = "9922" 
inputstring = ""
hidekey=""
#setup chân kết nối với lcd là output
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_E, GPIO.OUT) 
GPIO.setup(LCD_D4, GPIO.OUT) 
GPIO.setup(LCD_D5, GPIO.OUT) 
GPIO.setup(LCD_D6, GPIO.OUT) 
GPIO.setup(LCD_D7, GPIO.OUT)
# setup chan ket noi vs cac hang cua keypad la output
GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)
# setup chan ket noi vs cac cot cua keypad la output
GPIO.setup(C1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
 

# Define some device constants
LCD_WIDTH = 16    # số kí tự tối đa trên mỗi dòng
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # địa chỉ RAM lcd cho dong thứ nhất
LCD_LINE_2 = 0xC0 # địa chỉ RAM lcd cho dong thứ 2

# ham khoi tao man hinh
def lcd_init():
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x06,LCD_CMD) # 000110 hướng di chuyển con trỏ
    lcd_byte(0x0C,LCD_CMD) # 001100 hiển thị Bật con trỏ tắt, tắt nhấp nháy
    lcd_byte(0x28,LCD_CMD) # 101000 độ dài dữ liệu, số dòng, cỡ chữ
    lcd_byte(0x01,LCD_CMD) # 000001 xóa màn hình
    time.sleep(E_DELAY)

def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)
def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    GPIO.output(LCD_RS, mode) # RS
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    lcd_toggle_enable()
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
 
    # Toggle 'Enable' pin
    lcd_toggle_enable()



def lcd_string(message,line):
    # Send string to display
 
    message = message.ljust(LCD_WIDTH," ")
 
    lcd_byte(line, LCD_CMD)
 
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
# hàm đọc gia ki tự dòng- line , ki tu 
def readline(line, characters):
    global inputstring
    global hidekey
    GPIO.output(line, GPIO.HIGH)
    time.sleep(0.02)
    if(GPIO.input(C1) == 1):
        inputstring = inputstring +characters[0]
        hidekey = hidekey +"*"
        #print(inputstring)
        lcd_string(hidekey,LCD_LINE_2) # hien thi hidekey ở dòng thứ 2
    elif(GPIO.input(C2) == 1):
        inputstring = inputstring +characters[1]
        hidekey = hidekey +"*"
        #print(inputstring)
        lcd_string(hidekey,LCD_LINE_2)
    elif(GPIO.input(C3) == 1):
        inputstring = inputstring +characters[2]
        hidekey = hidekey +"*"
        #print(inputstring)
        lcd_string(hidekey,LCD_LINE_2)
      
    elif(GPIO.input(C4) == 1):
        if(characters[3] ==  "#"):
            if(inputstring == secretkey): # nếu mật khẩu đúng
                lcd_string("OPEN Gate",LCD_LINE_2) 
                #print("OPEN Gate")
                time.sleep(1)
       
                lcd_string("",LCD_LINE_2)
                inputstring = ""
                hidekey= ""
            else:
                lcd_string(" PASSWORD FALSE",LCD_LINE_2)
                #print("PASSWORD FALSE")
                time.sleep(1)
                lcd_string("AGAIN",LCD_LINE_2)
                #print("AGAIN")
                inputstring = ""
                hidekey= ""
        else:
            inputstring = inputstring +characters[3]
            hidekey = hidekey +"*"
            print(inputstring)
            lcd_string(hidekey,LCD_LINE_2)
    GPIO.output(line, GPIO.LOW)
    time.sleep(0.02)

delay = 5
lcd_init()
lcd_string("Hello",LCD_LINE_1)
#print("Hello")
time.sleep(2)
#print("ENTER PASSWORD")
lcd_string("ENTER PASSWORD",LCD_LINE_1)
time.sleep(1)

while 1:
   readline(R1, ["7","8","9","/"])
   readline(R2, ["4","5","6","*"])
   readline(R3, ["1","2","3","-"])
   readline(R4, ["C","0","=","#"])
