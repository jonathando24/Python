import RPi.GPIO as GPIO
import time

def detect(trig, ech): #takes in two pins of utrasonic sensor and returns distance in cm
	time.sleep(.01)
	GPIO.output(trig, GPIO.HIGH)
	time.sleep(.00001)
	GPIO.output(trig,GPIO.LOW)
	starttime=time.time()
	signaloff=starttime
	while GPIO.input(ech)==0 and time.time()<starttime+.1:
		signaloff=time.time()

	signalon=time.time()
	while GPIO.input(ech)==1 and time.time()<signaloff+.1:
		signalon=time.time()
	
	timepassed=signalon-signaloff
	distance=timepassed*17000
	
	return distance

def detectL(l): #takes in pin for infrared sensor and returns what it detects
	line = GPIO.input(l)
	return line

def moveF(p): #move motor "forwards"
	t = (100*1.7)/20
	p.ChangeDutyCycle(t)
	p.start(t)
	return

def moveB(p): #move motor "backwards"
	t = (100*1.2)/20
	p.ChangeDutyCycle(t)
	p.start(t)
	return

GPIO.setmode(GPIO.BOARD)
#pin set up
eyein1=38
eyeout1=40
eyein2=35
eyeout2=37
m1=36
m2=32
switch=11
l1=16
l2=18
l3=13
l4=15
GPIO.setup(switch, GPIO.IN)
go = False
while True:
	if GPIO.input(switch) == 1: #switch to start and stop the sumobot
		if go == True: #puts sumobot in off state
			go = False
			print "off"
			time.sleep(.25)
			mm2.stop()
			mm1.stop()
		else: #puts sumobot in on state
			go = True
			print "on"
			GPIO.setup(eyeout1, GPIO.OUT) #set up the GPIO
			GPIO.setup(eyein1, GPIO.IN)
			GPIO.setup(eyein2, GPIO.IN)
			GPIO.setup(eyeout2, GPIO.OUT)
			GPIO.setup(m1, GPIO.OUT)
			GPIO.setup(m2, GPIO.OUT)
			GPIO.setup(switch, GPIO.IN)
			GPIO.setup(l1, GPIO.IN)
			GPIO.setup(l2, GPIO.IN)
			GPIO.setup(l3, GPIO.IN)
			GPIO.setup(l4, GPIO.IN)
			mm1 = GPIO.PWM(m1, 50)
			mm2 = GPIO.PWM(m2, 50)
			time.sleep(.25)
	if go==True:
		dis1 = detect(eyeout1,eyein1) #detect distance in front and behind
		dis2 = detect(eyeout2,eyein2)
		print dis1
		if dis1 < 57: #move robot towards object in front of eye1
			moveF(mm1)
			moveB(mm2)
		elif dis2 < 57: #move robot towards object in front of eye2
			moveF(mm2)
			moveB(mm1)
		elif detectL(l1) == 0: #if a white line is detected, move away from it
			moveF(mm2)
			moveB(mm1)
			time.sleep(1.5)
		elif detectL(l2) == 0: #if a white line is detected, move away from it
			moveB(mm2)
			moveF(mm1)
			time.sleep(1.5)
		else: #spin to detect robots
			moveF(mm1)
			moveF(mm2)

GPIO.cleanup()
