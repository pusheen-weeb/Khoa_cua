import RPi.GPIO as GPIO
import face_recognize 
import time
import the_tu

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)

face_active_time = time.time()
temp_face_active_time = face_active_time
#dieu khien cua
mo_cua_cam = False
mo_cua_rfid = False

#gioi han hoat dong cua cac thanh phan
count_rfid = 0

print("Moi thu deu on bat dau chay")

while True: # Run forever
    
    #face recognize
    #measure elapse time to make wait time
    temp_face_active_time = time.time()
    time_diff = temp_face_active_time - face_active_time     
    #detect press and waited 5s
    if (GPIO.input(10) == GPIO.LOW) and time_diff > 7.0:
        print("Nhan nut camera")
        mo_cua_cam = face_recognize.face_recog()
        face_active_time = temp_face_active_time
    
    if time_diff > 2000:#avoid overflow
        face_active_time = temp_face_active_time
    
    #RFID Rc522
    if count_rfid == 50 #chay rfid sau 50 iteration
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
