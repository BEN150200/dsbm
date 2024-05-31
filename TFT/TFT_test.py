import TFT_driver
import time as Time
import keyboard

# Color def
red = 0b111111111111111111111111111100000000000000
aqua = 0x07ff
chartreuse = 0x7fe0
yellow =0xffe0	
white = 0xffff
magenta = 0xf81f

tft = TFT_driver.TFT("pigpio")
tft.config()
'''
tft.flip(1,0,1)
tft.clear()
tft.draw_resize("./dragonite.bmp", 0,0,320,240)

tft.print("Dagornite", 0, 0, size=40 )
tft.print("Dagornite", 0, 50, size=40, color=0xffff, fontfile="DangerNight.otf")
tft.print("Dagornite", 0, 100, size=40, background=aqua, fontfile="DangerNight.otf")
tft.print("Dagornite", 0, 150, size=40, color=0x0000)
tft.print("Dagornite", 0, 200, size=40, color=chartreuse, background=0xffff)

tft.print_rgb("hello",100,0, size=25 )
tft.print_rgb("world",100,150, size = 25, shading=False)
'''
tft.config_touch()
tft.clean_touch()
while 1:
    (x,y) = tft.get_touch()
    if (x,y) != (-1,-1):
        print((x,y))
        tft.square(x,y,5,5,aqua)

tft.Stop()
