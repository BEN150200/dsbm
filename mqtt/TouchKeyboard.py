import TFT_driver
import time as Time
import keyboard
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import threading

light=0
sendTime=5
sending=False

measure_pin = 38
output_pin = 40

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
	Time.sleep(0.001)
	
	GPIO.setup(measure_pin, GPIO.IN)
	GPIO.setup(output_pin, GPIO.OUT)

def read_analog():
	discharge() 
	start_time = Time.time()
	GPIO.output(output_pin, True) # Set pin to 1 to charge the capacitor
	while not GPIO.input(measure_pin):
		pass
	#GPIO.wait_for_edge(measure_pin, GPIO.RISING) # Wait for the input to detect a 1
	end_time = Time.time()
	GPIO.output(output_pin, False)
	elapse_time = end_time - start_time
	return elapse_time

# read the resistance based on the time to charge the capacitor
def read_resistance():
	time = read_analog()
	resistance = time / (cap * 0.5833)
	return resistance


def on_message(client, userdata, msg):
    tft.print(str(msg.payload,'utf-8'), 0,0, size=16, color=red, background=white)
    print(msg.payload)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("light/data")


def send_data(time):
    while True:
        mqttc.publish("light/sensor", light)
        Time.sleep(time)
        print(light)

def start_send_data():
    sending=True
    t=threading.Thread(target=send_data,args=(sendTime,))
    t.start()

def stop_send_data():
    sending = False 

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("10.10.73.214")

mqttc.loop_start()

# Color def
red = 0b111111111111111111111111111100000000000000
aqua = 0x07ff
chartreuse = 0x7fe0
yellow =0xffe0	
white = 0xffff
magenta = 0xf81f

keymap = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ']
]

tft = TFT_driver.TFT("pigpio")
tft.config()

set_up()
message = ""

tft.clean_touch()

clear = input("Clean screen?")
if clear == "y":
    tft.square(0,0,240,120, white)

printKeyboard = input("Print keyboard??")
if printKeyboard == "y":
    tft.draw_resize("./1366_2000.bmp", 0,160,240,160) 
    tft.square(0,120,80,40, red) 
    tft.square(80,120,80,40, yellow)
    tft.square(160,120,80,40, aqua)



line = pos = 0
shifted = False
while 1:
    light = read_resistance()
    (x,y) = tft.get_touch()
    row = col = -1
    if (x,y) != (-1,-1):
        if y >= 160:
            row = (y-160) / 40
            if row < 3:
                col = x / 24
            elif x < 36:
                shifted = not shifted
            else:
                col = (x - 36) / 24
            if -1 < row < 4 and -1 < col < 10:
                char = keymap[int(row)][int(col)]
                print(keymap[int(row)][int(col)])
                if row > 0 and shifted:
                    char = char.upper()
                message += char
                tft.print(char, pos,line, size=16)
                if shifted:
                    pos += 12
                else:
                    pos += 8
                if pos > 220:
                    line += 20
                    pos = 0
                if line > 100:
                    line = 0
                    pos = 0        
                    tft.square(0,0,240,120, white)
                    
        else:
            if y >= 120:
                if x < 80:
                    mqttc.publish("light/sensor", light ,qos=0)
                  #  stop_send_data()
                elif x < 160:
                    start_send_data()
                   
                else:
                    mqttc.publish("message/pol-biel", message ,qos=0)
                    message=""
                    tft.square(0,0,240,120, white)
                    
        tft.clean_touch()
tft.Stop()
mqttc.loop_stop()
