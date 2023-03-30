import RPi.GPIO as GPIO
import face_recognize 
import time
import the_tu

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#cam button pressed
cam_butt_pressed = False
#dieu khien cua
mo_cua_cam = False
mo_cua_rfid = False

#gioi han hoat dong cua cac thanh phan
count_cam  = 0
count_rfid = 0

print("Moi thu deu on bat dau chay")

while True: # Run forever
    
    #face recognize
    #detect press
    if GPIO.input(10) == GPIO.LOW:
        print("Nhan nut camera")
        break
        cam_butt_pressed = True
        
    count_cam = count_cam + 1
    if count_cam > 200:#limit counting avoide overflow
        count_cam =200
        
    # run face detection 
    if count_cam >= 200 and cam_butt_pressed == True:#run after N iteration
        count_cam = 0
        cam_butt_pressed = False
        print("Chay camera")
        mo_cua_cam = face_recognize.face_recog()
        
    #RFID Rc522
    count_rfid = count_rfid + 1
    if count_rfid > 100:#limit counting avoide overflow
        count_rfid =100
        
    if count_rfid >= 50: #chay rfid sau 50 iteration
        id,text,mo_cua_rfid = the_tu.RFID_read()
        count_rfid = 0 
    
    
    #mo cua
    if mo_cua_cam or mo_cua_rfid:
        print("Mo cua")
        print("camera:",mo_cua_cam,sep = "")
        print("rfid__:",mo_cua_rfid,sep = "")
        
        time.sleep(10)
        
        #dong cua
        mo_cua_cam = False
        mo_cua_rfid = False
        
        print("Dong cua")
    
    
    
GPIO.cleanup()
