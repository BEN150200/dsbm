import RPi.GPIO as GPIO
import time

measure_pin = 5
output_pin = 7

cap = 0.000000950 	# 950nF
res = 215		# 215 ohm

def set_up():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(output_pin, GPIO.OUT)
	GPIO.setup(measure_pin, GPIO.IN)

def discharge():
	GPIO.setup(measure_pin, GPIO.OUT)
	GPIO.setup(output_pin, GPIO.IN)
	GPIO.output(measure_pin, False)
	time.sleep(0.001)
	
	GPIO.setup(measure_pin, GPIO.IN)
	GPIO.setup(output_pin, GPIO.OUT)

def read_analog():
	discharge() 
	start_time = time.time()
	GPIO.output(output_pin, True) # Set pin to 1 to charge the capacitor
	while not GPIO.input(measure_pin):
		pass
	#GPIO.wait_for_edge(measure_pin, GPIO.RISING) # Wait for the input to detect a 1
	end_time = time.time()
	GPIO.output(output_pin, False)
	elapse_time = end_time - start_time
	return elapse_time

# read the resistance based on the time to charge the capacitor
def read_resistance():
	time = read_analog()
	resistance = time / (cap * 0.5833)
	return resistance
	

set_up()
while True:
	print(read_resistance())
	

