#!/usr/bin/python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
import sys
import cv2.cv as cv
import numpy as np
from optparse import OptionParser

import RPi.GPIO as GPIO
import time
import requests

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

def post():
    return 'false'
    """
    res = requests.post('https://localhost:3000',
                      files = {
                          "data": ("photo.jpg", open("./photo.jpg", "rb"),
                          "image/jpeg")
                          }, verify=False)
    print(res.text)
    """

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0

facecount = 0
nofacecount = 0

def detect_face(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)
    
    if (cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        print "facecount   = ",facecount
        print "nofacecount = ",nofacecount
        return faces
    return None

def detect_and_draw(img, cascade):
    print('detect_and_draw: ')
    print(facecount)
    print(nofacecount)
    faces = detect_face(img, cascade)
    if faces:
        global facecount
        nofacecount = 0
        facecount = facecount+1
        if facecount == 10:
            cv.SaveImage("photo.jpg",img)
            facecount=0
            return 1
        for ((x, y, w, h), n) in faces:
            # the input to cv.HaarDetectObjects was resized, so scale the 
            # bounding box of each face and convert it to two CvPoints
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
    else:
        global nofacecount
        facecount = 0
        nofacecount = nofacecount + 1
        if nofacecount == 50:
            nofacecount = 0
            return 2
    return 0
                
    #cv.ShowImage("result", img)


def main():
    args = ['0']
    options = {'cascade': 'face.xml'}
    cascade = cv.Load(options['cascade'])
    
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    input_name = args[0]
    if input_name.isdigit():
        capture = cv.CreateCameraCapture(int(input_name))
    else:
        capture = None

    #cv.NamedWindow("result", 1)

    width = 320 #leave None for auto-detection
    height = 240 #leave None for auto-detection

    if width is None:
    	width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
    else:
    	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

    if height is None:
	height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
    else:
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

    mode = 0
    count = 0
    if capture:
        frame_copy = None
        while True:
            if mode == 0:
                print('mode0')
                if(GPIO.input(PIRPin)!=0):
                    #GPIO.output(BuzzerPin,GPIO.LOW)
                    print('Camera On!!!')
                    mode = 1
                else:
                    #GPIO.output(BuzzerPin,GPIO.HIGH)
                    print('.')
                    LED_lightup(LEDPIN_yellow)
                    time.sleep(0.5)
            elif mode == 1:
                print('mode1')
                frame = cv.QueryFrame(capture)
                if not frame:
                    cv.WaitKey(0)
                    break
                if not frame_copy:
                    frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
                if frame.origin == cv.IPL_ORIGIN_TL:
                    cv.Copy(frame, frame_copy)
                else:
                    cv.Flip(frame, frame_copy, 0)
            
                result = detect_and_draw(frame_copy, cascade)
                if result == 1:
                    post_res = post()
                    print('DETECT!!!')
                    if post_res == 'true':
                        mode = 2
                    elif post_res == 'false':
                        mode = 3
                elif result == 2:
                    print('Camera Off')
                    mode = 0

                
            elif mode == 2:
                print('mode2')
                print(count)
                LED_lightup(LEDPIN_green)
                time.sleep(0.5)
                count = count + 1
                if (count > 10):
                    count = 0
                    mode = 0
            elif mode == 3:
                print('mode3')
                print(count)
                LED_lightup(LEDPIN_red)
                GPIO.output(BuzzerPin,GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(BuzzerPin,GPIO.HIGH)
                frame = cv.QueryFrame(capture)
                if not frame:
                    cv.WaitKey(0)
                    break
                faces = detect_face(frame, cascade)
                print(faces)
                if not faces:
                    count = count + 1
                    if (count > 3):
                        mode = 0
                        count = 0
                else:
                    count = 0

            if cv.WaitKey(10) >= 0:
                break
    else:
        image = cv.LoadImage(input_name, 1)
        detect_and_draw(image, cascade)
        cv.WaitKey(0)

    #cv.DestroyWindow("result")

def destroy():
    #turn off buzzer
    GPIO.output(BuzzerPin,GPIO.HIGH)
    #release resource
    GPIO.cleanup()
#

if __name__ == '__main__':
    setup()
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
        pass


