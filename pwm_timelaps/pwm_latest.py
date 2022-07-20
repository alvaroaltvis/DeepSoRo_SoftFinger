import RPi.GPIO as GPIO
import time 
from picamera import PiCamera

# If using multiple cameras
# from timelaps_new import *

#Code for the pump
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

pwm = GPIO.PWM(12,100)
pwmo = GPIO.PWM(13,100)

pwm.start(0)
pwmo.start(0)

#Set up for the camera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.vflip = True
#camera.saturation = 0.2

# Take embeded image
def capture(name):
    for i in range(3):
        camera.capture("/home/raspberrypi/Desktop/EmbededImages/" + name + f"camera{i}.jpg")
        
def inflate(name):
    max_time = 1
    start_time = time.time()
    while time.time() < max_time + start_time:
        GPIO.output(6, 0)
        pwm.ChangeDutyCycle(int(dutycycle))
    else:
        capture(name)
        pwm.ChangeDutyCycle(0)

## If two cameras were to be used 
#def deflate():  
#    max_time = 0.5
#    start_time = time.time()
#    while time.time() < max_time + start_time:
#        pwmo.ChangeDutyCycle(int(dutycycle))
#    else: 
#        pwmo.ChangeDutyCycle(0)
        
stopit = False

while(stopit!= True):
    dutycycle = input("Enter the percentage of Duty Cycle, 100 max value, 1 to quit: ")
    if int(dutycycle) == 1:
        stopit = True
        break
    name = input("Enter the name of the pictures: ")
    inflate(name)
    GPIO.output(6, 1)
    #deflate()
   
GPIO.cleanup()
print("Finish")
