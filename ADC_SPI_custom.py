#coding=utf-8

import RPi.GPIO as GPIO
import time

clk = 3
cs = 8
dOut = 7 #ADC In
dIn = 5 #ADC Out
Tfreq = 0.05 #está en micro segs

def tSample():
	time.sleep(3*(Tfreq/1000000))

def setUp():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(clk, GPIO.OUT)
	GPIO.setup(dOut, GPIO.OUT)
	GPIO.setup(cs, GPIO.OUT)
	GPIO.setup(dIn, GPIO.IN)

def clkUP():
	GPIO.output(clk,1)
	time.sleep(Tfreq/1000000)

def clkDOWN():
	GPIO.output(clk,0)
	time.sleep(Tfreq/1000000)

def clkSignal():
	# the value is ready to be read by the device
	clkUP() # say to the device the value is ready	
	# the device is reading the value
	clkDOWN() # the value is not present


def send(pin, value):	
	GPIO.output(pin, value)
	clkSignal()

def read(pin):
	GPIO.output(clk, 1)
	value = GPIO.input(pin) # read the value
	time.sleep(Tfreq/1000000)
	clkDOWN()
	return value


def start():
	send(cs,0)
	send(dOut,1)
	send(dOut,1) 	#set mode single-ended
	clkSignal()
	send(dOut,0)    #set CH0
	send(dOut,0)	


def analog_read():
	start()
	tSample()	
	read(dIn)
	bits = []
	for i in range(10):
		bits.append(read(dIn))
	result = 0
	for bit in bits:
		result = (result >> 1) | bit
	return result

setUp()	
while(True):
	print(analog_read())
