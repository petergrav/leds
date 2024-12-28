
import random
import time
import board
from neopixel import NeoPixel
import adafruit_led_animation.color as color
import adafruit_led_animation

MY_STRIP_LEN = 600
pixel_pin = board.D18
np = NeoPixel(pixel_pin, MY_STRIP_LEN, auto_write=False)

def neo_range(color, start, end):
    np.brightness = 1
    for i in range(start, end):
        np[i] = color
    np.show()

def neo_fill(color):
    np.brightness = 1
    np.fill(color)
    np.show()

def neo_sparkle(color, duration, count):
    np.brightness = 1
    for i in range(count):
        n = random.randrange(len(np))
        bkgnd = np[n]
        np[n] = color
        np.show()
        time.sleep(duration)
        np[n] = bkgnd
        
    np.show()

def neo_flash(color, range_start, range_end, on_time, off_time, count):
    np.brightness = 1
    #bkgnd = []
    #for i in range(range_start, range_end):
    #    bkgnd.append(i) == np[i]
    for i in range(count):
        neo_range(color, range_start, range_end)
        np.show()
        time.sleep(on_time)
        neo_range((0,0,0), range_start, range_end)
        np.show()
        time.sleep(off_time)
    #np.show()


def neo_sweep(color, width, duration):
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

def neo_off():
    np.brightness = 0
    np.fill(color.BLACK)
    np.show()

if __name__ == "__main__":
    #--- Test code for the above API ---
 #   MY_STRIP_LEN = 300
 #   pixel_pin = board.D18
 #   np = NeoPixel(pixel_pin, MY_STRIP_LEN)
    print("range 1")
    neo_range((0,255,0), 85, 125)
    print("range 2")
    neo_range((0,255,0), 225, 265)
    print("sparkle")
    neo_sparkle((200,200,200), 0.1, 30)
    print("sweep " + str(len(np)))
    neo_sweep((255,0,0), 10, 0)
    neo_off()
    