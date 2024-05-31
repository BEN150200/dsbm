#!/usr/bin/env python

import RPi.GPIO as GPIO
import time as Time
#Connections, TFT pin = board pin

CS_Pin    =  24 #Poseu els Pins vostres aqui
Reset_Pin =  11	#Poseu els Pins vostres aqui
SCLK_Pin  =  23	#Poseu els Pins vostres aqui
SDO_Pin   =  21	#Poseu els Pins vostres aqui
SDI_Pin   =  19	#Poseu els Pins vostres aqui

IM1_Pin = 36
IM2_Pin = 38
IM3_Pin = 40

#TFT Interface Functions

class TFT_Driver:

    def __init__(self):
        pass

    def Config_Pins(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(IM1_Pin,GPIO.OUT)
        GPIO.setup(IM2_Pin,GPIO.OUT)
        GPIO.setup(IM3_Pin,GPIO.OUT)
        GPIO.setup(CS_Pin,GPIO.OUT)
        GPIO.setup(Reset_Pin,GPIO.OUT)
        GPIO.setup(SCLK_Pin,GPIO.OUT)
        GPIO.setup(SDI_Pin,GPIO.OUT)
        GPIO.setup(SDO_Pin,GPIO.IN)
        #Initial values
        GPIO.output(IM1_Pin,False)
        GPIO.output(IM2_Pin,True)
        GPIO.output(IM3_Pin,False)
        GPIO.output(CS_Pin,True)
        GPIO.output(Reset_Pin,True)
        GPIO.output(SCLK_Pin,False)
        Time.sleep(0.2) 

    def CS_TFT(self, value):				
        GPIO.output(CS_Pin,value)

    def Reset_TFT(self, value):				
        GPIO.output(Reset_Pin,value)

    def Clock_SPI(self):
        GPIO.output(SCLK_Pin,False)
        GPIO.output(SCLK_Pin,True)

    def Send_SPI(self, value):
        GPIO.output(SDI_Pin, value)
        self.Clock_SPI()   

    def Recv_SPI(self):
        self.Clock_SPI()
        return GPIO.Input(SDO_Pin)

    def Send_SPI_8(self,value):
        for i in range(8):
            if(value&128):
                self.Send_SPI(True)
            else:		
                self.Send_SPI(False)
            value=value<<1

    def Recv_SPI_8(self):
        value = 0
        for i in range(8):
            value = value | (self.Recv_SPI() << i)
        return value


    #SPI Level Functions

    # SPI_START 0x70
    # SPI_RD 0x01
    # SPI_WR 0x00
    # SPI_DATA 0x02
    # SPI_INDEX 0x00

    def Write_SPI_TFT_Cmd(self,reg):
        #Reg is 8 bit
        self.CS_TFT(False)
        #Send Start,Write,Index
        self.Send_SPI_8(0x70)
        #Send the value
        self.Send_SPI_8(reg)
        self.CS_TFT(True)

    def Write_SPI_TFT_Dat(self,value):
        #value is 16 bit
        self.CS_TFT(False)
        #Send Start,Write,Data
        self.Send_SPI_8(0x72)
        #Send the value	
        self.Send_SPI_8(value>>8)
        self.Send_SPI_8(value)
        self.CS_TFT(True)

    def Write_SPI_TFT_Reg(self,reg,value):
        #Sets a value to a reg
        self.Write_SPI_TFT_Cmd(reg)
        self.Write_SPI_TFT_Dat(value)

    def Read_SPI_TFT_Reg(self,reg):
        #Sets a value to a reg
        self.Write_SPI_TFT_Cmd(reg)
        #Caldria llegir 16 bits
        return(0x0000)

    def Stop(self):
        GPIO.cleanup()


   
