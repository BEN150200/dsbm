#!/usr/bin/env python

import time as Time
import pigpio
#Connections, TFT pin = board pin

""" CS_Pin    =  24 #Poseu els Pins vostres aqui
Reset_Pin =  11	#Poseu els Pins vostres aqui
SCLK_Pin  =  23	#Poseu els Pins vostres aqui
SDO_Pin   =  21	#Poseu els Pins vostres aqui
SDI_Pin   =  19	#Poseu els Pins vostres aqui

IM1_Pin = 36
IM2_Pin = 38
IM3_Pin = 40 """

CS_Pin    =  8 #Poseu els Pins vostres aqui
Reset_Pin =  17	#Poseu els Pins vostres aqui
SCLK_Pin  =  11	#Poseu els Pins vostres aqui
SDO_Pin   =  9	#Poseu els Pins vostres aqui
SDI_Pin   =  10	#Poseu els Pins vostres aqui

IM1_Pin = 5
IM2_Pin = 6
IM3_Pin = 13

#TFT Interface Functions

class TFT_Driver:

    def __init__(self):
        self.pi = pigpio.pi()
        self.spi = self.pi.spi_open(0, 30000000, 3)
        self.serial = self.pi.serial_open("/dev/serial0",9600)

    def data_available(self):
        rdy = self.pi.serial_data_available(self.serial)
        return rdy > 12    

    def Read_Touch(self): 
        x=y=""
        try:
            byte = chr(self.pi.serial_read_byte(self.serial))
            while byte != 'X' and self.pi.serial_data_available(self.serial) > 0:
                byte = chr(self.pi.serial_read_byte(self.serial))
            while byte != 'Y' and self.pi.serial_data_available(self.serial) > 0:
                byte = chr(self.pi.serial_read_byte(self.serial))
                if (byte != 'Y'):
                    x += byte
            while byte != ';' and self.pi.serial_data_available(self.serial) > 0: 
                byte = chr(self.pi.serial_read_byte(self.serial))
                if (byte != ';'):
                    y += byte
            return (int(x),int(y))
        except:        
            return (-1,-1)
   
    def Config_Pins(self):
        self.pi.set_mode(IM1_Pin,pigpio.OUTPUT)
        self.pi.set_mode(IM2_Pin,pigpio.OUTPUT)
        self.pi.set_mode(IM3_Pin,pigpio.OUTPUT)
        self.pi.set_mode(Reset_Pin,pigpio.OUTPUT)

        #Initial values
        self.pi.write(IM1_Pin,0)
        self.pi.write(IM2_Pin,1)
        self.pi.write(IM3_Pin,0)
        self.pi.write(Reset_Pin,1)
        Time.sleep(0.2) 

    def Reset_TFT(self,value):			
        self.pi.write(Reset_Pin,value)


    #SPI Level Functions

    # SPI_START 0x70
    # SPI_RD 0x01
    # SPI_WR 0x00
    # SPI_DATA 0x02
    # SPI_INDEX 0x00
    def Write_SPI_TFT_Cmd(self,reg):
        self.pi.spi_write(self.spi, [0x70, reg])

    def Write_SPI_TFT_Dat(self,value):
        self.pi.spi_write(self.spi, [0x72, (value>>8) &0xFF, value&0xFF])

    def Write_SPI_TFT_Reg(self, reg,value):
        self.pi.spi_write(self.spi, [0x70, reg])
        self.pi.spi_write(self.spi, [0x72, (value>>8) &0xFF, value&0xFF])
       
    def Read_SPI_TFT_Reg(self,reg):
        #Sets a value to a reg
        data = self.pi.spi_xfer(self.spi, [0x73, reg])
        #Caldria llegir 16 bits
        return data
    
    def Stop(self):
        self.pi.spi_close(self.spi)
        self.pi.serial_close(self.serial)
        self.pi.stop()
