
import random
import time
from neopixel import NeoPixel
import adafruit_led_animation.color as color
import adafruit_led_animation

def neo_range(pixel_pin, MY_STRIP_LEN, color, start, end):
    np = NeoPixel(pixel_pin, MY_STRIP_LEN, auto_write=False)
    np.brightness = 1
    for i in range(start, end):
        np[i] = color
    np.show()

def neo_fill(pixel_pin, MY_STRIP_LEN, color):
    np = NeoPixel(pixel_pin, MY_STRIP_LEN, auto_write=False)
    np.brightness = 1
    np.fill(color)
    np.show()

def neo_sparkle(pixel_pin, MY_STRIP_LEN, color, duration, count):
    np = NeoPixel(pixel_pin, MY_STRIP_LEN, auto_write=False)
    np.brightness = 1
    for i in range(count):
        n = random.randrange(len(np))
        bkgnd = np[n]
        np[n] = color
        np.show()
        time.sleep(duration)
        np[n] = bkgnd
        
    np.show()

def neo_flash(pixel_pin, MY_STRIP_LEN, color, range_start, range_end, on_time, off_time, count):
    np = NeoPixel(pixel_pin, MY_STRIP_LEN, auto_write=False)
    np.brightness = 1
    #bkgnd = []
    #for i in range(range_start, range_end):
    #    bkgnd.append(i) == np[i]
    for i in range(count):
        neo_range(pixel_pin, MY_STRIP_LEN, color, range_start, range_end)
        np.show()
        time.sleep(on_time)
        neo_range(pixel_pin, MY_STRIP_LEN, (0,0,0), range_start, range_end)
        np.show()
        time.sleep(off_time)
    #np.show()


def neo_sweep(pixel_pin, MY_STRIP_LEN, color, width, duration):
    np = NeoPixel(pixel_pin, MY_STRIP_LEN, auto_write=False)
    np.brightness = 1
    bkgnd = []
    num_pixels = len(np)
    for i in range(num_pixels + width):
        erase = i - width
        if erase >= 0:
            np[erase] = bkgnd.pop()

        if i < num_pixels:
            bkgnd.insert(0, np[i])
            np[i] = color

        np.show()
        time.sleep(duration)

def neo_off(pixel_pin, MY_STRIP_LEN):
    np = NeoPixel(pixel_pin, MY_STRIP_LEN, auto_write=False)
    np.brightness = 0
    np.fill(color.BLACK)
    np.show()

    