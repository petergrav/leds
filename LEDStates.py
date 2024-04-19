# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, auto_write=True, pixel_order=ORDER
)

def off():
    pixels.brightness = 0
    pixels.fill((0, 0, 0))

def green():
    pixels.brightness = 0.8
    pixels.fill((0, 255, 0))

def red():
    pixels.brightness = 0.5
    pixels.fill((255, 0, 0))

def blue():
    pixels.brightness = 0.5
    pixels.fill((0, 0, 255))
