import RPi.GPIO as GPIO
import face_recognize 
import time
import the_tu
import key
import relay_4
import rpi_lcd as lcd # thu vien hien thi len lcd

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
pwmpin = 32
GPIO.setup(pwmpin, GPIO.OUT) # set pin 32 as pwm
f = GPIO.PWM(pwmpin, 100)
f.start(0)

#cam button pressed
#cam_butt_pressed = False
#dieu khien cua

#gioi han hoat dong cua cac thanh phan
count_cam  = 0
count_rfid = 0

#id
new_id = 0
#pass
pass_word = "1"

#thiet bi
door_state = False #False = close True = Open
relay = [False,False,False,False]
#close all relay at start
relay_4.control_relay(relay[0],relay[1],relay[2],relay[3])

fan = 0
lcd = lcd.LCD() # khoi tao LCD
print("Moi thu deu on bat dau chay") # thay bang "HELLO"
lcd.text("HELLO",1)
#hien manin menu
print("1.Client menu","2.Admin menu",sep = '\n')

while True: # Run forever
    lcd.text ("1.Client menu",1)
    lcd.text ("2.Admin menu",2)
    #read keypad
    char = key.read_key()
    #time.sleep(0.1)
    if char == "1":
        key.inputstring = ""#reset input string
        client_access = False
        time.sleep(1)
        lcd.clear
        
        while True:
            print("1.Password","2.Camera","3.The tu","4.Van tay")
            lcd.text ("1.Pass 3.TheTu ",1)  # viet tat cho du nh
            lcd.text ("2.Cam  4.VanTay",2)
            #time.sleep(0.1)
            char = key.read_key()
            lcd.clear()
            if char == "c":
                lcd.text("Back",1)
                time.sleep(1)
                lcd.clear ()
                break
            
            #password
            if char == "1":
                print("Password")
                lcd.text("Password",1)
                time.sleep(1)
                lcd.clear()
                while True:
                    #time.sleep(0.1)
                    lcd.text("Nhap pass",1)
                    char = key.read_key()
                    lcd.text(key.inputstring,2)
                    lcd.clear()
                    if char == "c":
                        key.inputstring = ""#reset input string
                        lcd.text ("Back",2)
                        break
                    if char != None:
                        tem_client_access = key.pass_check(char,pass_word)
                        if tem_client_access == True:
                            client_access = True
                            break
                    char = None
                    #time.sleep(0.1) 
                    lcd.clear()
                time.sleep(1) 
                lcd.clear()

                
                            
                
            #face recognize
            #detect press
            if char == "2":
                time.sleep(1)
                print("Chay camera")
                lcd.text ("Chay camera",1)
                tem_client_access = face_recognize.face_recog()
                if tem_client_access == True:
                    client_access = True
                
                time.sleep(1) 
                lcd.clear()

            
            if char == "3":
                time.sleep(1)
                while True:
                    print("Doc the tu")
                    lcd.text("Doc the tu",1)
                    time.sleep(0.3)
                    char = key.read_key()
                    if char == "c":
                        lcd.text ("Back",1)
                        break
                    try:
                        id,text,tem_client_access = the_tu.RFID_read()
                    except:
                        id = 0
                        text = "none"
                        tem_client_access = False
            
                    if tem_client_access == True:
                        client_access = True
                        break 
                    lcd.clear()
                time.sleep(1) 
                lcd.clear()


                
            char = None
            #mo cua
            if client_access:#client access = True
                print("Client granted")
                lcd.text("Client granted",1)
                time.sleep(1)
                
                while client_access:
                    print("1.Door 2.Led 3.Fan")
                    lcd.text("1.Door  2.Led",1)
                    lcd.text("    3 Fan    ",2)
                    char = key.read_key()
                    #time.sleep(0.1)
                    lcd.clear()

                    if char == "c":
                        while True:
                            print("Log out ? 7/8 = y/n")
                            lcd.text("Log out? 7/8=y/n",1)
                            char = key.read_key()
                            if char == "7":
                                print("log out")
                                lcd.text("    Log out",2)
                                #time.sleep(0.1)
                                client_access = False
                                char = None
                                break
                            if char == "8":
                                print("keep access")
                                lcd.text("  Keep access",2)
                                char = None
                                time.sleep(1)
                                break
                            #time.sleep(0.1)
                            lcd.clear()
                        time.sleep(1)
                        lcd.clear()
                    
                    if char == "1":#door
                        relay[3] = True
                        relay_4.control_relay(relay[0],relay[1],relay[2],relay[3])
                        lcd.text("Opened",1)
                        time.sleep(6)
                        relay[3] = False
                        relay_4.control_relay(relay[0],relay[1],relay[2],relay[3])
                        lcd.text("Closed",1)
                    
                    if char == "2":#Led
                        #time.sleep(0.1)
                        while True:
                            print("Led")
                            print("1-3 on/off")
                            lcd.text("Led 1-3 on/off",1)
                            char = key.read_key()
                            if char == "c":
                                lcd.text("back",1)
                                time.sleep(0.2)
                                break
                            #time.sleep(0.1)
                            if char == "1":
                                relay[0] = not relay[0]
                            if char == "2":
                                relay[1] = not relay[1]
                            if char == "3":
                                relay[2] = not relay[2]
                            
                            #dieu khien led
                            mess = ""
                            mess = mess + "".join([str(int(x)) for x in relay[0:3]])
                            lcd.text(mess,2)
                            
                            relay_4.control_relay(relay[0],relay[1],relay[2],relay[3])
                            
                            char = None
                    
                    if char == "3":#fan
                        while True:
                            print("Fan","+ -")
                            lcd.text("Fan: + -",1)
                            
                            mess= "Fan:" +'{}'.format(fan)
                            lcd.text(mess,2)
                            char = key.read_key()
                            if char == "c":
                                lcd.text("Back",1)
                                break
                            #time.sleep(0.1)
                            if char == "+":
                                print("fan +")
                                fan = fan + 10
                            if char == "-":
                                print("fan -")
                                fan = fan - 10
                            if fan > 100:
                                fan = 100
                            if fan < 0  :
                                fan = 0
                            
                            f.ChangeDutyCycle(fan)
                            
                            char = None
                            lcd.clear()
                        time.sleep(1)
                        lcd.clear()
                    char = None
        lcd.clear                  
    #admin menu
    elif char == "2":
        admin_access = False
        time.sleep(1)
        key.inputstring = ""#reset input string
        while True:
            print("Log in admin")
            lcd.text("Nhap pass admin",1)
            char = key.read_key()
            lcd.text(key.inputstring,2)
            ##time.sleep(0.1)
            lcd.clear ()
            if char == "c":
                key.inputstring = ""#reset input string
                lcd.text("Back",1)
                break
            #time.sleep(0.1)
            if char != None:
                admin_access = key.pass_check(char,"1111")
                if admin_access == True:
                    print("log in")
                    lcd.text("Log in",1)
                    time.sleep(1)
                    print("Ad granted")
                    lcd.text("Ad granted",2)
                    time.sleep (1)
                    lcd.clear()
                    
                    
                    while admin_access:
                        #menu admin
                        print("1Pass 2Cam 3The 4VanT")
                        lcd.text ("1.Pass 3.TheTu ",1)  
                        lcd.text ("2.Cam  4.VanTay",2)
                        char = key.read_key()
                        #time.sleep(0.1)
                        lcd.clear()
                        if char == "c":
                            while True:
                                print("Log out ? 7/8 = y/n")
                                lcd.text("Log out? 7/8=y/n",1)
                                char = key.read_key()
                                if char == "7":
                                    print("log out")
                                    lcd.text("log out",2)
                                    #time.sleep(0.1)
                                    admin_access = False
                                    char = None
                                    break
                                if char == "8":
                                    print("keep access")
                                    lcd.text("Keep access",2)
                                    char = None
                                    time.sleep(1)
                                    break
                                #time.sleep(0.1)
                                lcd.clear()

                        if char == "1":
                            print("change pass")
                            lcd.text("Change pass",1)
                            time.sleep(0.5)
                            pass_word = ""
                            while True:
                                char = key.read_key()
                                if char == "#":
                                    print("saved pass")
                                    lcd.text("Saved pass",2)
                                    break
                                #time.sleep(0.1)
                                if char != None:
                                    pass_word = pass_word + char
                                print(pass_word) 
                                lcd.text(pass_word,2)
                            time.sleep(1)
                            lcd.clear()  
                        if char == "2":
                            char = None

                        if char == "3":
                            while True:
                                print("1Addcard 2Clear")
                                lcd.text("1Addcard 2Clear",1)
                                char = key.read_key()
                                #time.sleep(0.1)
                                lcd.clear()
                                if char == "c":
                                    lcd.text("Back", 1)
                                    break
                                ##time.sleep(0.1)
                                if char == "1":
                                    print("Add card")
                                    lcd.text ("Add card",1)
                                    the_tu.RFID_write(str(new_id))
                                    print("Write success")
                                    lcd.text ("Write success",2)
                                    new_id = new_id + 1
                                
                                if char == "2":
                                    the_tu.RFID_wipe()
                                    print("cleared")
                                    lcd.text ("cleared",1)
                            
                            char = None
                            #time.sleep(0.1)
                            lcd.clear()
                        if char == "4":
                            char = None
                        char = None
                    
                    lcd.clear()
            #time.sleep(0.1)
            lcd.clear()
        #time.sleep(0.1)
        lcd.clear()

    
GPIO.cleanup()