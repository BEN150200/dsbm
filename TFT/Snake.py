import TFT_driver
import time as Time
import keyboard
from random import randrange, randint

# Color def
red = 0b111111111111111111111111111100000000000000
aqua = 0x07ff
chartreuse = 0x7fe0
yellow =0xffe0	
white = 0xffff
magenta = 0xf81f

tft = TFT_driver.TFT("pigpio")
tft.config()

tft.clear()
snake_size = 8
playing = True
direction = 'R'
food = False
points = 0
width = 240
heigh = 320
top = 32

tft.print(f"Points:",10,0,20)
tft.print(f"{points}",50,0,20, color=0x0000, background=0xffff)
snake = [(0,top+30),(snake_size*1,snake_size*8),(snake_size*2,top+30),(snake_size*3,top+30),(snake_size*4,top+30)]

for b in snake:
    tft.square(b[0], b[1], snake_size, snake_size, chartreuse)

tft.square(0, top-1, width, 0, 0x0000)

while playing:    
    if food == False:
        global food_pos 
        food_pos = (randint(0,width/snake_size)*snake_size, (randint(0, (heigh-top)/snake_size)*snake_size)+top)
        tft.square(food_pos[0], food_pos[1], snake_size, snake_size, red)
        food = True
        if food_pos[0] > width-snake_size:
            food_pos = (0, food_pos[1])
        elif food_pos[1] > heigh-snake_size:
            food_pos = (food_pos[0], top)
        if food_pos[0] < 0:
            food_pos = (width-snake_size, food_pos[1])
        if food_pos[1] < top:
            food_pos = (food_pos[0], heigh-snake_size)
    
    if keyboard.is_pressed('a') and direction != 'R':
        direction = 'L'
    elif keyboard.is_pressed('d') and direction != 'L':
        direction = 'R'
    elif keyboard.is_pressed('w') and direction != 'D':
        direction = 'U'
    elif keyboard.is_pressed('s') and direction != 'U':
        direction = 'D'
    elif keyboard.is_pressed('esc'):
        playing = False
        
    head = snake[len(snake)-1]
    if food_pos == head:
        points += 1
        #tft.square(food_pos[0], food_pos[1], snake_size, snake_size, white)
        food = False
        tft.print(f"{points}",50,0,20, color=0x0000, background=0xffff)

    else:
        tail = snake.pop(0)
    if direction == 'R':
        head = (head[0]+snake_size, head[1])
    elif direction == 'L':
        head = (head[0]-snake_size, head[1])
    elif direction == 'U':
        head = (head[0], head[1]-snake_size)
    elif direction == 'D':
        head = (head[0], head[1]+snake_size)

    if head[0] > width-snake_size:
        head = (0, head[1])
    elif head[1] > heigh-snake_size:
        head = (head[0], top)
    if head[0] < 0:
        head = (width-snake_size, head[1])
    if head[1] < top:
        head = (head[0], heigh-snake_size)

    snake.append(head)
    tft.square(tail[0], tail[1], snake_size, snake_size, white)
    tft.square(head[0], head[1], snake_size, snake_size, chartreuse)
   

tft.Stop()
