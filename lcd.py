import RPi.GPIO as GPIO
import time
import os

#
GPIO.setwarnings(False)
# các chân GPIO của rasp với LCD

LCD_RS = 29
LCD_E  = 13
LCD_D4 = 23
LCD_D5 = 21
LCD_D6 = 19
LCD_D7 = 15
LCD_WIDTH = 16    # số kí tự tối đa trên mỗi dòng
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # địa chỉ RAM lcd cho dong thứ nhất
LCD_LINE_2 = 0xC0 # địa chỉ RAM lcd cho dong thứ 2

# ham khoi tao man hinh
def lcd_init():
    GPIO.setmode(GPIO.BCM ) 
    GPIO.setup(LCD_E, GPIO.OUT) # output E
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

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

def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    
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

def main():
    
    
    lcd_init()
    lcd_string("Hello",LCD_LINE_1)
    time.sleep(1)
    lcd_string("ENTER PASSWORD",LCD_LINE_1)
    time.sleep(1)
