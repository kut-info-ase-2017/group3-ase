#!/usr/bin/python
###########################################################################
#Filename      :pirsensor.py
#Description   :Infrared alarm system
#Author        :alan
#Website       :www.osoyoo.com
#Update        :2017/07/05
############################################################################
import RPi.GPIO as GPIO
import time

# set BCM_GPIO 17(GPIO 0) as PIR pin
PIRPin = 17
# set BCM_GPIO 27(GPIO 1) as LED pin
LEDPIN_green = 27
# set BCM_GPIO 21(GPIO 2) as LED pin
LEDPIN_red = 21
# set BCM_GPIO 13(GPIO 3) as LED pin
LEDPIN_yellow = 13
# set BCM_GPIO 20(GPIO 4) as buzzer pin
BuzzerPin = 20

#print message at the begining ---custom function
def print_message():
    print ('==================================')
    print ('|              Alarm             |')
    print ('|     -----------------------    |')
    print ('|     PIR connect to GPIO0       |')
    print ('|                                |')
    print ('|     Buzzer connect to GPIO1    |')
    print ('|     ------------------------   |')
    print ('|                                |')
    print ('|                          OSOYOO|')
    print ('==================================\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIRPin,GPIO.IN)
    #set LEDPIN's mode to output,and initial level to LOW(0V)
    GPIO.setup(LEDPIN_green,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDPIN_red,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDPIN_yellow,GPIO.OUT,initial=GPIO.LOW)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(BuzzerPin,GPIO.OUT,initial=GPIO.HIGH)

def LED_lightup(LEDPIN):
    GPIO.output(LEDPIN,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LEDPIN,GPIO.LOW)

def take_photo():
    #return True
    return False

#main function
def main():
    #print info
    print_message()
    while True:
        #read Sw520dPin's level
        if(GPIO.input(PIRPin)!=0):
            GPIO.output(BuzzerPin,GPIO.LOW)
            print ('********************')
            print ('*     alarm!       *')
            print ('********************')
            print ('\n')
            if take_photo() == True:
                LED_lightup(LEDPIN_green)
            else:
                LED_lightup(LEDPIN_red)
            time.sleep(0.5)
        else:
            GPIO.output(BuzzerPin,GPIO.HIGH)
            print ('====================')
            print ('=    Not alarm...  =')
            print ('====================')
            print ('\n')
            LED_lightup(LEDPIN_yellow)
            time.sleep(0.5)

#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off buzzer
    GPIO.output(BuzzerPin,GPIO.HIGH)
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
        pass

