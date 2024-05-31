import time as Time
import TFT_driver_original as tft
import TFT_driver

# Color def
red = 0b111111111111111111111111111100000000000000
aqua = 0x07ff
chartreuse = 0x7fe0
yellow =0xffe0	
white = 0xffff
magenta = 0xf81f

def print_background_original():
    tft.Config_Pins()
    tft.SPI_TFT_Reset()

    print("Printing background pixel by pixel...")
    start = Time.time()
    for y in range(320):
        for x in range(240):
            tft.SPI_TFT_pixel(x, y, magenta)
    end = Time.time()
    print(f"Time to print: {end-start}")

def print_background_spi():
    tft = TFT_driver.TFT("spi")
    tft.config()
    
    print("Printing background with automatic position...")
    start = Time.time()
    tft.background(chartreuse)
    end = Time.time()
    print(f"Time to print: {end-start}")
    tft.Stop()

def print_background_pigpio():
    tft = TFT_driver.TFT("pigpio")
    tft.config()
    
    print("Printing background with pigpio spi lib...")
    start = Time.time()
    tft.background(red)
    end = Time.time()
    print(f"Time to print: {end-start}")
    tft.Stop()


print_background_original()
print_background_spi()
print_background_pigpio()