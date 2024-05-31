#!/usr/bin/env python
import time as Time
import TFT_driver_pigpio
from PIL import Image, ImageFont, ImageDraw
import numpy as np

class TFT:
    def __init__(self, driver):
        self.Orig_X=0
        self.Orig_Y=0
        self.Size_X=240
        self.Size_Y=320
        if driver == 'pigpio':
            self.SPI = TFT_driver_pigpio.TFT_Driver()
        self.topLeft = (234, 229)
        self.topRight = (392, 883)
        self.bottomLeft = (869,293)
        self.bottomRight = (847,867)
        self.touchSizeX = self.bottomRight[0] - self.topLeft[0]       
        self.touchSizeY = self.bottomRight[1] - self.topLeft[1]       
    
    def config(self):
        self.SPI.Config_Pins()
        self.reset()

    #TFT Level Functions
    def reset(self):
        #Reset the TFT 	
        self.SPI.Reset_TFT(0)
        Time.sleep(0.25) 
        self.SPI.Reset_TFT(1)               
        Time.sleep(0.006)   

        #Start Initial Sequence
        self.SPI.Write_SPI_TFT_Reg(0xEA, 0x0000)    #Reset Power Control 1 
        self.SPI.Write_SPI_TFT_Reg(0xEB, 0x0020)    #Power Control 2   
        self.SPI.Write_SPI_TFT_Reg(0xEC, 0x000C)    #Power Control 3   
        self.SPI.Write_SPI_TFT_Reg(0xED, 0x00C4)    #Power Control 4   
        self.SPI.Write_SPI_TFT_Reg(0xE8, 0x0040)    #Source OPON_N     
        self.SPI.Write_SPI_TFT_Reg(0xE9, 0x0038)    #Source OPON_I     
        self.SPI.Write_SPI_TFT_Reg(0xF1, 0x0001)                
        self.SPI.Write_SPI_TFT_Reg(0xF2, 0x0010)                 
        self.SPI.Write_SPI_TFT_Reg(0x27, 0x00A3)    #Display Control 2 

        # Power On sequence 
        self.SPI.Write_SPI_TFT_Reg(0x1B, 0x001B)    #Power Control 2 
        self.SPI.Write_SPI_TFT_Reg(0x1A, 0x0001)    #Power Control 1
        self.SPI.Write_SPI_TFT_Reg(0x24, 0x002F)    #Vcom Control 2
        self.SPI.Write_SPI_TFT_Reg(0x25, 0x0057)    #Vcom Control 3                       
        self.SPI.Write_SPI_TFT_Reg(0x23, 0x008D)    #Vcom Control 1
    
        # Gamma settings
        self.SPI.Write_SPI_TFT_Reg(0x40,0x00)
        self.SPI.Write_SPI_TFT_Reg(0x41,0x00)
        self.SPI.Write_SPI_TFT_Reg(0x42,0x01)
        self.SPI.Write_SPI_TFT_Reg(0x43,0x13)
        self.SPI.Write_SPI_TFT_Reg(0x44,0x10)
        self.SPI.Write_SPI_TFT_Reg(0x45,0x26)
        self.SPI.Write_SPI_TFT_Reg(0x46,0x08)
        self.SPI.Write_SPI_TFT_Reg(0x47,0x51)
        self.SPI.Write_SPI_TFT_Reg(0x48,0x02)
        self.SPI.Write_SPI_TFT_Reg(0x49,0x12)
        self.SPI.Write_SPI_TFT_Reg(0x4A,0x18)
        self.SPI.Write_SPI_TFT_Reg(0x4B,0x19)
        self.SPI.Write_SPI_TFT_Reg(0x4C,0x14)
        self.SPI.Write_SPI_TFT_Reg(0x50,0x19)
        self.SPI.Write_SPI_TFT_Reg(0x51,0x2F)
        self.SPI.Write_SPI_TFT_Reg(0x52,0x2C)
        self.SPI.Write_SPI_TFT_Reg(0x53,0x3E)
        self.SPI.Write_SPI_TFT_Reg(0x54,0x3F)
        self.SPI.Write_SPI_TFT_Reg(0x55,0x3F)
        self.SPI.Write_SPI_TFT_Reg(0x56,0x2E)
        self.SPI.Write_SPI_TFT_Reg(0x57,0x77)
        self.SPI.Write_SPI_TFT_Reg(0x58,0x0B)
        self.SPI.Write_SPI_TFT_Reg(0x59,0x06)
        self.SPI.Write_SPI_TFT_Reg(0x5A,0x07)
        self.SPI.Write_SPI_TFT_Reg(0x5B,0x0D)
        self.SPI.Write_SPI_TFT_Reg(0x5C,0x1D)
        self.SPI.Write_SPI_TFT_Reg(0x5D,0xCC)
    
        #Power + Osc 
        self.SPI.Write_SPI_TFT_Reg(0x18,0x0036)      #OSC Control 1 
        self.SPI.Write_SPI_TFT_Reg(0x19,0x0001)      #OSC Control 2
        self.SPI.Write_SPI_TFT_Reg(0x01,0x0000)      #Display Mode Control
        self.SPI.Write_SPI_TFT_Reg(0x1F,0x0088)      #Power Control 6
        Time.sleep(0.005)             
        self.SPI.Write_SPI_TFT_Reg(0x1F,0x0080)      #Power Control 6              
        Time.sleep(0.005)                                      
        self.SPI.Write_SPI_TFT_Reg(0x1F,0x0090)      #Power Control 6
        Time.sleep(0.005)             
        self.SPI.Write_SPI_TFT_Reg(0x1F,0x00D0)      #Power Control 6
        Time.sleep(0.005)                                        
    
        #Appearance
        self.SPI.Write_SPI_TFT_Reg(0x17,0x0005)      #Colmod 16Bit/Pixel
        self.SPI.Write_SPI_TFT_Reg(0x36,0x0000)      #Panel Characteristic
        self.SPI.Write_SPI_TFT_Reg(0x28,0x0038)      #Display Control 3        
        Time.sleep(0.04)                 
        self.SPI.Write_SPI_TFT_Reg(0x28,0x003C)      #Display Control 3
        Time.sleep(0.002)             
        self.SPI.Write_SPI_TFT_Reg(0x16,0x0008)	    #Orientation
        # 0  0  0  0  0  0 0 0
        # MY MX MV X RGB X X X
        self.SPI.Write_SPI_TFT_Reg(0x03,(self.Orig_X>>0)) #Set Dimensions
        self.SPI.Write_SPI_TFT_Reg(0x02,(self.Orig_X>>8))
        self.SPI.Write_SPI_TFT_Reg(0x05,(self.Size_X-1>>0))
        self.SPI.Write_SPI_TFT_Reg(0x04,(self.Size_X-1>>8))
        self.SPI.Write_SPI_TFT_Reg(0x07,(self.Orig_Y>>0))
        self.SPI.Write_SPI_TFT_Reg(0x06,(self.Orig_Y>>8))
        self.SPI.Write_SPI_TFT_Reg(0x09,(self.Size_Y-1>>0))
        self.SPI.Write_SPI_TFT_Reg(0x08,(self.Size_Y-1>>8))

    def clear(self):
        white = 0xffff
        self.background(white)

    def background(self,color):
        self.area(0, 0, self.Size_X-1, self.Size_Y-1, color)


    """
    Flips the x, y axis and change the printing orientation from cols to rows    
    """
    def flip(self,x, y, rot):
        if rot == 1:
            self.Size_X=320
            self.Size_Y=240
        else:
            self.Size_X=240
            self.Size_Y=320
        data = 0x08
        data |= (y << 7)
        data |= (x << 6)
        data |= (rot << 5)
        self.SPI.Write_SPI_TFT_Reg(0x16,data)

    def set_start(self,x, y):
        """set_start set start position x, y on the TFT to print
        
        Args:
            x (int): column of the TFT in pixels to limit the start point
            y (int): row of the TFT in pixels to limit the start point
        """        
        self.SPI.Write_SPI_TFT_Reg(0x03,(x>>0))
        self.SPI.Write_SPI_TFT_Reg(0x02,(x>>8))
        self.SPI.Write_SPI_TFT_Reg(0x07,(y>>0))
        self.SPI.Write_SPI_TFT_Reg(0x06,(y>>8)) 

    def set_end(self,x, y):
        """set_end set end position x, y on the TFT to print
        
        Args:
            x (int): column of the TFT in pixels to limit the end point
            y (int): row of the TFT in pixels to limit the end point
        """
        self.SPI.Write_SPI_TFT_Reg(0x05,(x>>0))
        self.SPI.Write_SPI_TFT_Reg(0x04,(x>>8))
        self.SPI.Write_SPI_TFT_Reg(0x09,(y>>0))
        self.SPI.Write_SPI_TFT_Reg(0x08,(y>>8))    
    

    def pixel(self,x,y,color):
        #Sets a Pixel X,Y to a Color
        self.set_start(x, y)
        self.SPI.Write_SPI_TFT_Cmd(0x22)
        self.SPI.Write_SPI_TFT_Dat(color)

    """
    Print an area in one color form point (x,y) to (xe, ye)
    """
    def area(self,x, y, xe, ye, color):
        self.set_start(x, y)
        self.set_end(xe,ye)
        self.SPI.Write_SPI_TFT_Cmd(0x22)
        for i in range((xe-x+1) * (ye-y+1)):
            self.SPI.Write_SPI_TFT_Dat(color)

    """
    Print an square in one color in point (x,y) with size (sx, sy)
    """
    def square(self,x, y, sx, sy, color):
        xe = x + sx
        ye = y + sy
        self.area(x, y, xe, ye, color)


    def array(self,x, y, sx, sy, px_arr):
        xe = x + sx
        ye = y + sy
        self.set_start(x, y) 
        self.set_end(xe, ye)
        self.SPI.Write_SPI_TFT_Cmd(0x22)
        for i in px_arr:
            self.SPI.Write_SPI_TFT_Dat(int(i))

    def transparent_array(self,x, y, sx, sy, px_arr, color=0xffff):
        xe = x + sx
        ye = y + sy
        self.set_start(x, y) 
        self.set_end(xe, ye)
        self.SPI.Write_SPI_TFT_Cmd(0x22)
        for i in px_arr:
            if i == color:
                self.SPI.Read_SPI_TFT_Reg(0x22)
            else:
                self.SPI.Write_SPI_TFT_Dat(int(i))

    def rgb_array(self,x, y, sx, sy, px_arr):
        xe = x + sx
        ye = y + sy
        self.set_start(x, y) 
        self.set_end(xe, ye)
        self.SPI.Write_SPI_TFT_Cmd(0x22)
        for i in px_arr:
            self.SPI.Write_SPI_TFT_Dat(self.pixel_convert(int(i[0]),int(i[1]),int(i[2])))


    def draw(self,path, x, y):
        img = Image.open(path)
        w, h = img.size
        img_array = np.asarray(img)
        img_array = np.resize(img_array, (-1,3))
        self.rgb_array(x,y,w-1,h-1,img_array)


    def draw_resize(self,path, x, y, sx, sy):
        img = Image.open(path)
        img = img.resize((sx,sy))
        w, h = img.size
        img_array = np.asarray(img)
        img_array = np.resize(img_array, (-1,3))
        self.rgb_array(x,y,w-1,h-1,img_array)

        
    def pixel_convert(self, red8, green8, blue8):	
        red5 = np.round(red8 / 255 * 31)
        # Convert 8-bit green to 6-bit green.
        green6 = np.round(green8 / 255 * 63)
        # Convert 8-bit blue to 5-bit blue.
        blue5 = np.round(blue8 / 255 * 31)

        # Shift the red value to the left by 11 bits.
        red5_shifted = np.uint16(red5) << np.uint16(11)
        # Shift the green value to the left by 5 bits.
        green6_shifted = np.uint16(green6) << np.uint16(5)

        # Combine the red, green, and blue values.
        rgb565 = red5_shifted | green6_shifted | np.uint16(blue5)

        return rgb565


    def print(self, txt, x, y, size=12, color=None, background=None, fontfile='COMICSANS.TTF'):
        if fontfile.lower().find(".otf") > -1:
            font = ImageFont.truetype(fontfile,size, encoding='utf-8')
        else:
            font = ImageFont.truetype(fontfile,size)

        # Get the sizes 
        ascent, descent = font.getmetrics()
        (width, baseline), (offset_x, offset_y) = font.font.getsize(txt)
        text_height = ascent+descent
        height = text_height
        transparent = None
        if color == None and background != None:
            color = 0xffff - background
            low = color & 0xff
            color = color<<8 & color 
            print(hex(color))
            transparent = color
        elif color == None:
            color = 0x0000
            background = 0xffff - color
            transparent = background
        if background == None:
            background = 0xffff - color
            transparent = background

        img = Image.new("I;16", (width,height), color=background)
        d = ImageDraw.Draw(img)
        d.fontmode = '1'
        d.text((0,0), txt, font=font, fill=color)
        img_array = np.asarray(img)
        img_array = np.resize(img_array, (-1,1))
        if transparent != None:
            self.transparent_array(x,y,width-1,height-1,img_array, transparent)
        else:
            self.array(x,y,width-1,height-1,img_array)
        

    def print_rgb(self,txt, x, y, size=12, color=0x0000, background=0xffffff, shading=True, fontfile='COMICSANS.TTF'):
        if fontfile.lower().find(".otf") > -1:
            font = ImageFont.truetype(fontfile,size, encoding='utf-8')
        else:
            font = ImageFont.truetype(fontfile,size)

        # Get the sizes 
        ascent, descent = font.getmetrics()
        (width, baseline), (offset_x, offset_y) = font.font.getsize(txt)
        text_height = ascent+descent
        height = text_height

        img = Image.new('RGB', (width,height), color=color)
        d = ImageDraw.Draw(img)
        if shading:
            d.fontmode = 'RGB'
        else:
            d.fontmode = '1'
            
        d.text((0,0), txt, font=font, fill=background)
        img_array = np.asarray(img)
        img_array = np.resize(img_array, (-1,3))
        self.rgb_array(x,y,width-1,height-1,img_array)


    def elipse(self,x, y, sx, sy):
        img = Image.new('I;16', (sx,sy), color=0xffff)
        d = ImageDraw.Draw(img)
        d.ellipse((0,0, sx-1, sy-1))
        img_array = np.asarray(img)
        img_array = np.resize(img_array, (-1,1))
        self.array(x,y,sx-1,sy-1,img_array)

    def scroll(self):
        #Vertical scroll Top Fixed Area
        self.SPI.Write_SPI_TFT_Reg(0x0F, 0x00)
        self.SPI.Write_SPI_TFT_Reg(0x0E, 0x00)
        #Vertical scroll Bottom Fixed Area
        self.SPI.Write_SPI_TFT_Reg(0x13, 0x00)
        self.SPI.Write_SPI_TFT_Reg(0x12, 0x00)
        #Vertical scroll Height Area
        self.SPI.Write_SPI_TFT_Reg(0x11, 0x64)
        self.SPI.Write_SPI_TFT_Reg(0x10, 0x00)
        
        self.SPI.Write_SPI_TFT_Reg(0x18, 0x02)
        #Vertical scroll Start Address Area
        self.SPI.Write_SPI_TFT_Reg(0x15, 0x32)

    def off(self):
        self.SPI.Write_SPI_TFT_Reg(0x26, 0x00)

    def on(self):
        self.SPI.Write_SPI_TFT_Reg(0x26, 0x08)

    def wait_touch(self):
        (x,y) = self.SPI.Read_Touch()
        while (x > 900 or y > 900) or ( x < 100 or y < 100):
            (x,y) = self.SPI.Read_Touch()
        Time.sleep(1)
        trash = self.SPI.pi.serial_data_available(self.SPI.serial)
        self.SPI.pi.serial_read(self.SPI.serial, trash)
        return (x,y) 
    

    
   
    def config_touch(self):
        self.square(0, 0, 5,5, 0xf81f)
        self.topLeft = self.wait_touch()
        print (self.topLeft)
        self.square(self.Size_X-5, 0, 5, 5, 0xf81f)
        self.topRight = self.wait_touch()
        print (self.topRight)
        self.square(0, self.Size_Y-5, 5, 5, 0xf81f)
        self.bottomLeft = self.wait_touch()
        print (self.bottomLeft)
        self.square(self.Size_X-5, self.Size_Y-5, 5, 5, 0xf81f)
        self.bottomRight = self.wait_touch()
        print (self.bottomRight)
      
       

    def transform_cords(self, x, y):
        trans_x = ((x - self.topLeft[0])/self.touchSizeX) * self.Size_X 
        trans_y = ((y - self.topLeft[1])/self.touchSizeY) * self.Size_Y
        return (int(trans_x), int(trans_y))
    
    def clean_touch(self):
        trash = self.SPI.pi.serial_data_available(self.SPI.serial)
        self.SPI.pi.serial_read(self.SPI.serial, trash)

    def get_touch(self): 
        (y,x) = self.SPI.Read_Touch()
        if (x > 900 or y > 900) or ( x < 100 or y < 100):
            return (-1,-1)
        return self.transform_cords(x,y) 



    def Stop(self):
        self.SPI.Stop()

