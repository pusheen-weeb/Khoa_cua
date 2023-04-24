# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import serial
import adafruit_fingerprint
import rpi_lcd as lcd

lcd = lcd.LCD() # khoi tao LCD
# import board
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
# uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi 3 with pi3-disable-bt
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################


def get_fingerprint():
    i = 0
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    lcd.text("Waiting",1)
    while finger.get_image() != adafruit_fingerprint.OK:
        i =  i+1
        if i == 100:
            return False
        pass
    print("Templating...")
    lcd.text("Templating",1)
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    lcd.text("Searching",1)
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="")
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="")
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="")
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


# pylint: disable=too-many-statements
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
            lcd.text("Place finger",1)
        else:
            print("Place same finger again...", end="")
            lcd.text("Place finger again",1)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                lcd.text("Image taken",1)
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                lcd.text("Imaging error",1)
                return False
            else:
                print("Other error")
                lcd.text("Other error",1)
                return False

        print("Templating...", end="")
        lcd.text("Templating",1)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
            lcd.text("Templated",1)
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
                lcd.text("Image too messy",1)
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
                lcd.text("Could not identify features",1)
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
                lcd.text("Image invalid",1)
            else:
                print("Other error")
                lcd.text("Other error",1)
            return False

        if fingerimg == 1:
            print("Remove finger")
            lcd.text("Remove finger",1)
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    lcd.text("Creating model",1)
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
        lcd.text("Created",1)
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True


def save_fingerprint_image(filename):
    """Scan fingerprint then save image to filename."""
    while finger.get_image():
        pass

    # let PIL take care of the image headers and file structure
    from PIL import Image  # pylint: disable=import-outside-toplevel

    img = Image.new("L", (256, 288), "white")
    pixeldata = img.load()
    mask = 0b00001111
    result = finger.get_fpdata(sensorbuffer="image")

    # this block "unpacks" the data received from the fingerprint
    #   module then copies the image data to the image placeholder "img"
    #   pixel by pixel.  please refer to section 4.2.1 of the manual for
    #   more details.  thanks to Bastian Raschke and Danylo Esterman.
    # pylint: disable=invalid-name
    x = 0
    # pylint: disable=invalid-name
    y = 0
    # pylint: disable=consider-using-enumerate
    for i in range(len(result)):
        pixeldata[x, y] = (int(result[i]) >> 4) * 17
        x += 1
        pixeldata[x, y] = (int(result[i]) & mask) * 17
        if x == 255:
            x = 0
            y += 1
        else:
            x += 1

    if not img.save(filename):
        return True
    return False


##################################################


def get_num(max_number,ID):
    """Use input() to get a valid number from 0 to the maximum size
    of the library. Retry till success!"""
    i = -1
    while (i > max_number - 1) or (i < 0):
        try:
            i = ID
            #i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))
        except ValueError:
            pass
    return i

#dieu khien van tay
def finger_command(c = "",ID = 0):
    lcd.clear()
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        #raise RuntimeError("Failed to read templates")
        return "Failed to read templates"
    print("Fingerprint templates: ", str(finger.templates))
    if finger.count_templates() != adafruit_fingerprint.OK:
        #raise RuntimeError("Failed to read templates")
        return "Failed to read templates"
    print("Number of templates found: ", str(finger.template_count))
    if finger.read_sysparam() != adafruit_fingerprint.OK:
        #raise RuntimeError("Failed to get system parameters")
        return "Failed to get system parameters"
    print("Size of template library: ", (finger.library_size))
    print("1) enroll print")
    print("2) find print")
    print("d) delete print")
    print("s) save fingerprint image")
    print("3) reset library")
    print("q) quit")
    print("----------------")
    #c = input("> ")

    if c == "1":
       enroll_finger(get_num(300,ID))
    if c == "2":
        if get_fingerprint():
            print("Detected #", finger.finger_id, "with confidence", finger.confidence)
            lcd.text("Detected #" + str(finger.finger_id),1)
            return "match"
        else:
            print("Finger not found")
            lcd.text("Finger not found",1)
            return "not match"
    if c == "d":
        if finger.delete_model(get_num(300,ID)) == adafruit_fingerprint.OK:
            print("Deleted!")
        else:
            print("Failed to delete")
    if c == "s":
        if save_fingerprint_image("fingerprint.png"):
            print("Fingerprint image saved")
        else:
            print("Failed to save fingerprint image")
    if c == "3":
        if finger.empty_library() == adafruit_fingerprint.OK:
            print("Library empty!")
            lcd.text("Library empty!",1)
        else:
            print("Failed to empty library")
            lcd.text("Failed to empty",1)
    #if c == "q":
        #print("Exiting fingerprint example program")
        #raise SystemExit
    return None

