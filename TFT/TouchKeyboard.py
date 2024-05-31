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

keymap = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ']
]

tft = TFT_driver.TFT("pigpio")
tft.config()

#tft.clear()



tft.clean_touch()

tft.square(0,0,240,160, white)

#tft.draw_resize("./1366_2000.bmp", 0,160,240,160)
line = pos = 0
shifted = False
while 1:
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
                
                tft.print(char, pos,line, size=16)
                if shifted:
                    pos += 12
                else:
                    pos += 8
                if pos > 220:
                    line += 20
                    pos = 0
                if line > 140:
                    line = 0
                    pos = 0        
                    tft.square(0,0,240,160, white)
            tft.clean_touch()
        else:
            tft.square(x,y, 2,2, red)
tft.Stop()
