
import random
import time
import board
from neopixel import NeoPixel

def neo_range(np, color, start, end):
    for i in range(start, end):
        np[i] = color

def neo_fill(np, color):
    neo_range(np, color, 0, len(np))

def neo_sparkle(np, color, duration, count):
    for i in range(count):
        n = random.randrange(len(np))
        bkgnd = np[n]
        np[n] = color
        np.show()
        time.sleep(duration)
        np[n] = bkgnd
        
    np.show()

def neo_sweep(np, color, width, duration):
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

if __name__ == "__main__":
    #--- Test code for the above API ---
    MY_STRIP_LEN = 300
    pixel_pin = board.D18
    np = NeoPixel(pixel_pin, MY_STRIP_LEN)
    print("range 1")
    neo_range( np,(0,255,0), 85, 125)
    print("range 2")
    neo_range( np, (0,255,0), 225, 265)
    print("sparkle")
    neo_sparkle(np, (200,200,200), 0.1, 30)
    print("sweep " + str(len(np)))
    neo_sweep(np, (255,0,0), 10, 0)
    np.show()
    