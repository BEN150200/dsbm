#!/usr/bin/env python

import time as Time
import pigpio

pi = pigpio.pi()
serial = pi.serial_open("/dev/serial0",9600)

def data_available():
    rdy = pi.serial_data_available(serial)
    return rdy > 12    

def read_coords(): 
    x=y=""
    try:
        byte = chr(pi.serial_read_byte(serial))
        while byte != 'X' and pi.serial_data_available(serial) > 0:
            byte = chr(pi.serial_read_byte(serial))
        while byte != 'Y' and pi.serial_data_available(serial) > 0:
            byte = chr(pi.serial_read_byte(serial))
            if (byte != 'Y'):
                x += byte
        while byte != ';' and pi.serial_data_available(serial) > 0: 
            byte = chr(pi.serial_read_byte(serial))
            if (byte != ';'):
                y += byte
        return (int(x),int(y))
    except:        
        return (-1,-1)


while True:
    if (data_available()):
        (x,y) = read_coords()
        print((x,y))
"""
    rdy = pi.serial_data_available(serial)
   
    if rdy > 12:
        byte = chr(pi.serial_read_byte(serial))
        #print(chr(byte))
        if byte == 'X':
            #print("X=")
            while byte != 'Y':
                byte = chr(pi.serial_read_byte(serial))
                x += byte
                #print(byte)
            #print("\tY=")
            while byte != ';': 
                byte = chr(pi.serial_read_byte(serial))
                y += byte
                #print(byte)
            #print('\n')
        print("X="+x+"\tY="+y)
    x=''
    y=''
"""

pi.serial_close(self.serial)
pi.stop()




