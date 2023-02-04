#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from gpiozero import Motor
import smbus


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Shift register set up pin.
dataPin = 5
clockPin = 6
latchPin = 13

LSBFIRST = 1
MSBFIRST = 2

#LED set up
YellowPin1 = 20
YellowPin2 = 19

GPIO.setup(YellowPin1, GPIO.OUT)   # Set Yellow's mode is output
GPIO.output(YellowPin1, GPIO.HIGH) # Set Yellow high(+3.3V) to turn off led

GPIO.setup(YellowPin2, GPIO.OUT)   # Set Yellow's mode is output
GPIO.output(YellowPin2, GPIO.HIGH) # Set Yellow high(+3.3V) to turn off led

# HighBeam set up
HighBeam = 26
GPIO.setup(HighBeam, GPIO.OUT)   # Set White HighBeam light 's mode is output
#GPIO.output(HighBeam, GPIO.HIGH) # Set White HighBeam light high(+3.3V) to turn

# Fan set up
Fan = 4
GPIO.setup(Fan, GPIO.OUT)
#GPIO.output(Fan, GPIO.HIGH)

# Motor Set Up
directionPin = 22
motorOnPin = 18
GPIO.setup(motorOnPin,GPIO.OUT)
GPIO.setup(directionPin,GPIO.OUT)

# Push Button
Left_Button = 25
Right_Button = 24
White_Button = 16
Emer_button = 12
Fan_button = 23
Engine_button = 27
Backward_button = 21

# Set 7 ButtonPin's mode as input with the internal pullup 
GPIO.setup(Left_Button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Right_Button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(White_Button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Emer_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Fan_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Engine_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Backward_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def setup():
        GPIO.setmode(GPIO.BCM)    # Number GPIOs by its physical location
        GPIO.setup(dataPin, GPIO.OUT)
        GPIO.setup(latchPin, GPIO.OUT)
        GPIO.setup(clockPin, GPIO.OUT)
        
#shiftOut function, use bit serial transmission.
        
# Using the defined pins, set the 6 leds, where each bit is 0 for off, 1 for on
def shiftOut(dPin,cPin,lPin,order,val):
        val2 = val ^ 0xff
        GPIO.output(lPin, GPIO.LOW)
        GPIO.output(cPin, GPIO.LOW)
        for i in range(0,8):
                GPIO.output(cPin,GPIO.LOW);
                if(order == LSBFIRST):
                        GPIO.output(dPin,(0x01&(val2>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
                elif(order == MSBFIRST):
                        GPIO.output(dPin,(0x80&(val2<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
                        
                GPIO.output(cPin,GPIO.HIGH);
        GPIO.output(lPin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(lPin, GPIO.LOW)
        time.sleep(0.1)

def LEDonoff(whichLED, state):
    global currentLEDstate
    if state:
        retval = currentLEDstate | pow(2, whichLED)
    else:
        retval = currentLEDstate & ~pow(2, whichLED)
    return retval

#LCD pin assignments, constants, etc
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable it

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# LCD commands
LCD_CMD_4BIT_MODE = 0x28   # 4 bit mode, 2 lines, 5x8 font
LCD_CMD_CLEAR = 0x01
LCD_CMD_HOME = 0x02   # goes to position 0 in line 0
LCD_CMD_POSITION = 0x80  # Add this to DDRAM address


#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

# functions not in the original library
# -------------------------------------

# Positions the cursor so that the next write to the LCD
# appears at a specific row & column, 0-org'd
# Updated for 4-line displays 2/14/20
def lcd_xy(col, row):
        lcd_byte(LCD_CMD_POSITION+col+(64*row)-(0x6c*(row > 1)), LCD_CMD)

# Begins writing a string to the LCD at the current cursor
# position. It doesn't concern itself with whether the cursor
# is visible or not. Go off the screen? Your bad.
def lcd_msg(msg_string):
        for i in range(0, len(msg_string)):
                lcd_byte(ord(msg_string[i]), LCD_CHR)
# PWM
p = GPIO.PWM(motorOnPin, 1000)
p.start(0)

setup()
currentLEDstate = 0  # all off
shiftOut(dataPin, clockPin, latchPin, MSBFIRST, currentLEDstate) # Turn off all of the LEDs 
nextblink = time.time()
blinkstate = 0
GPIO.output(Fan, GPIO.LOW)
# For coding
HighBeam_was_on = True 
LED_was_on = True
EMER_was_on = True
RIGHT_was_on = True
LEFT_was_on = True
HighBeam_was_on = True
Engine_was_on = True
Backward = True
Fan_was_on = True
lcd_init()

while True:
        # HEADLIGHT and TAILIGHT FUNCTION
        
        if (0 == GPIO.input(White_Button)):
                print('...is pressed')
                if (True == LED_was_on):# is pressed
                        
                        print('passed 1')
        #               currentLEDstate = currentLEDstate | 0x10  # bit 4 on
                        currentLEDstate = LEDonoff(0, 1)
                        currentLEDstate = LEDonoff(1, 1)
                        currentLEDstate = LEDonoff(4, 1)
                        currentLEDstate = LEDonoff(5, 1)
                        GPIO.output(HighBeam, GPIO.LOW)
                        lcd_string("   Headline On  ", LCD_LINE_1)
                        lcd_string("       **       ", LCD_LINE_2)
                        LED_was_on = False
                        HighBeam_was_on = False
                        time.sleep(0.1)

                        while (0 == GPIO.input(White_Button)): # wait until the user to release the bottom.
                                time.sleep(0.1)
                                pass
                        
                #HIGHBEAM FUNCTION
        if (0 == GPIO.input(White_Button)): 
                if (False == LED_was_on) and (False == HighBeam_was_on):
                        print('passed 2')
                        currentLEDstate = LEDonoff(0, 1)
                        currentLEDstate = LEDonoff(1, 1)
                        currentLEDstate = LEDonoff(4, 1)
                        currentLEDstate = LEDonoff(5, 1)
                        GPIO.output(HighBeam, GPIO.HIGH)
                        lcd_string("   Highbean On  ", LCD_LINE_1)
                        lcd_string("       **       ", LCD_LINE_2)
                        LED_was_on = False
                        HighBeam_was_on = True
                        time.sleep(0.1)
                        
                        while (0 == GPIO.input(White_Button)): # wait until the user to release the bottom.
                                time.sleep(0.1)
                                pass
                        
                elif(LED_was_on == False) and (HighBeam_was_on == True):
                        currentLEDstate = LEDonoff(0, 0)
                        currentLEDstate = LEDonoff(1, 0)
                        currentLEDstate = LEDonoff(4, 0)
                        currentLEDstate = LEDonoff(5, 0)
                        GPIO.output(HighBeam, GPIO.LOW)
                        lcd_string("   Headline Off  ", LCD_LINE_1)
                        lcd_string("   Highbeam Off ", LCD_LINE_2)
                        time.sleep(1)
                        lcd_string("                ", LCD_LINE_1)
                        lcd_string("                ", LCD_LINE_2)
                        LED_was_on = True
                        HighBeam_was_on = False
                        time.sleep(0.1)
                        
                        while (0 == GPIO.input(White_Button)): # wait until the user to release the bottom.
                                time.sleep(0.1)
                                pass
        # EMERGENCY LIGHT                
        if time.time() > nextblink:
                blinkstate = 1 - blinkstate
                nextblink = time.time() + 0.5
        
        if (0 == GPIO.input(Emer_button)):  # is pressed
                if (True == EMER_was_on):
                        while True:
                                if (0 == GPIO.input(Emer_button)):
                                        if (False == EMER_was_on):
                                                EMER_was_on = True
                                                time.sleep(0.1)
                                                break
                                                while (0 == GPIO.input(Emer_button)): # wait until the user to release the bottom.
                                                        time.sleep(0.1)
                                                        pass
                                print('...emergency on!!!')
                                GPIO.output(YellowPin1, GPIO.LOW) #left yellow on
                                GPIO.output(YellowPin2, GPIO.LOW) #right yellow on
                                lcd_string("<<            >>", LCD_LINE_1)
                                time.sleep(0.5)
                                GPIO.output(YellowPin1, GPIO.HIGH)   #left yellow off
                                GPIO.output(YellowPin2, GPIO.HIGH)  #right yellow off
                                lcd_string("                ", LCD_LINE_1)
                                time.sleep(0.5)
                                EMER_was_on = False

                        while (0 == GPIO.input(Emer_button)): # wait until the user to release the bottom.
                                time.sleep(0.1)
                                pass

        #TAIL LIGHT RIGHT REAR
        if (0 == GPIO.input(Right_Button)):  # is pressed
                if (True == RIGHT_was_on):
                        while True:
                                if (0 == GPIO.input(Right_Button)):
                                        if (False == RIGHT_was_on):
                                                RIGHT_was_on = True
                                                time.sleep(0.1)
                                                break
                                        while (0 == GPIO.input(Right_Button)): # wait until the user to release the bottom.
                                                time.sleep(0.1)
                                                pass
                                print('...right rear on!!!')
                                GPIO.output(YellowPin1, GPIO.LOW)  # yellow on
                                lcd_string("              >>", LCD_LINE_1)
                                time.sleep(0.5)
                                GPIO.output(YellowPin1, GPIO.HIGH)  # yellow on
                                lcd_string("                ", LCD_LINE_1)
                                time.sleep(0.5)
                                RIGHT_was_on = False

                        while (0 == GPIO.input(Right_Button)): # wait until the user to release the bottom.
                                time.sleep(0.1)
                                pass
        #TAIL LIGHT LEFT REAR
        if (0 == GPIO.input(Left_Button)):  # is pressed
                if (True == LEFT_was_on):
                        while True:
                                if (0 == GPIO.input(Left_Button)):
                                        if (False == LEFT_was_on):
                                                LEFT_was_on = True
                                                time.sleep(0.1)
                                                break
                                        while (0 == GPIO.input(Left_Button)): # wait until the user to release the bottom.
                                                time.sleep(0.1)
                                                pass
                                print('...left rear on!!!')
                                GPIO.output(YellowPin2, GPIO.LOW)  # yellow on
                                lcd_string("<<              ", LCD_LINE_1)
                                time.sleep(0.5)
                                GPIO.output(YellowPin2, GPIO.HIGH)  # yellow on
                                lcd_string("                ", LCD_LINE_1)
                                time.sleep(0.5)
                                LEFT_was_on = False

                        while (0 == GPIO.input(Left_Button)): # wait until the user to release the bottom.
                                time.sleep(0.1)
                                pass
                        
        # Motor forward
        if (0 == GPIO.input(Engine_button)): 
                if (True == Engine_was_on):
                        while True:
                                if (0 == GPIO.input(Engine_button)):
                                        if (False == Engine_was_on):
                                                Engine_was_on = True
                                                p.ChangeDutyCycle(0)
                                                GPIO.output(Fan, GPIO.LOW)
                                                lcd_string("                ", LCD_LINE_1)
                                                lcd_string("   Stop Moving   ", LCD_LINE_2)
                                                time.sleep(0.5)
                                                lcd_string("                ", LCD_LINE_1)
                                                lcd_string("                ", LCD_LINE_2)
                                                time.sleep(0.1)
                                                break
                                        while (0 == GPIO.input(Engine_button)): # wait until the user to release the bottom.
                                                time.sleep(0.1)
                                                pass
                                GPIO.output(directionPin, 1)        
                                print('..running...forward...')
                                lcd_string("  Moving Forward  ", LCD_LINE_1)
                                lcd_string("    Fan is on   ", LCD_LINE_2)
                                p.ChangeDutyCycle(50)
                                GPIO.output(Fan, GPIO.HIGH)
                                Engine_was_on = False
        # Motor backward
        if (0 == GPIO.input(Backward_button)):
                if (True == Backward):
                        while True:
                                if (0 == GPIO.input(Backward_button)):
                                        if (False == Backward):
                                                Backward = True
                                                p.ChangeDutyCycle(0)
                                                GPIO.output(Fan, GPIO.LOW)
                                                print('Fan is off')
                                                lcd_string("                ", LCD_LINE_1)
                                                lcd_string("   Stop Moving   ", LCD_LINE_2)
                                                time.sleep(0.5)
                                                lcd_string("                ", LCD_LINE_1)
                                                lcd_string("                ", LCD_LINE_2)
                                                time.sleep(0.1)
                                                break
                                        while (0 == GPIO.input(Backward_button)): # wait until the user to release the bottom.
                                                time.sleep(0.1)
                                                pass    
                                GPIO.output(directionPin, 0)        
                                print('...running..backward..')
                                lcd_string(" Moving Backward ", LCD_LINE_1)
                                lcd_string("    Fan is on   ", LCD_LINE_2)
                                p.ChangeDutyCycle(50)
                                print('Fan is turning')
                                GPIO.output(Fan, GPIO.HIGH)
                                Backward = False

    #else:
#        currentLEDstate = currentLEDstate & ~0x10  # bit 4 off
         #currentLEDstate = LEDonoff(2, 0)
        shiftOut(dataPin, clockPin, latchPin, MSBFIRST, currentLEDstate) # Turn off all of the LEDs 
            
  

def destroy():   # When 'Ctrl+C' is pressed, the function is executed. 
        GPIO.cleanup()
 



                        
        
