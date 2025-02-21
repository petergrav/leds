import time
import socket
from enum import Enum
#from rpi_ws281x import PixelStrip, Color
from neopixel import NeoPixel
import board
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.helper import PixelSubset

# Configuration for different Raspberry Pis based on hostname
HOSTNAME_CONFIG = {
    "petepi": {
        "LED_COUNT": 26,
        "LED_PIN": 18,
        "SEGMENTS": Enum("LEDSegment", {
            "SEGMENT1": (0, 9),
            "SEGMENT2": (10, 1),
            "SEGMENT3": (20, 25),
            "WHOLE_STRIP": (0, 25)
        })
    },
    "raspberrypi2": {
        "LED_COUNT": 30,
        "LED_PIN": 13,
        "SEGMENTS": Enum("LEDSegment", {
            "SEGMENT1": (0, 9),   # LEDs 0-9
            "SEGMENT2": (10, 19), # LEDs 10-19
            "SEGMENT3": (20, 29)  # LEDs 20-29
        })
    },
    # Add more hostnames and configurations as needed
    "default": {
        "LED_COUNT": 60,
        "LED_PIN": 18,
        "SEGMENTS": Enum("LEDSegment", {
            "SEGMENT1": (0, 19),
            "SEGMENT2": (20, 39),
            "SEGMENT3": (40, 59)
        })
    }
}

# Common LED strip settings
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal
LED_BRIGHTNESS = 1  # Set to 0-1 (max brightness)
LED_INVERT = False    # True to invert the signal
LED_CHANNEL = 0       # Set to 1 for GPIOs 13, 19, 41, 45, or 53

class CustomSolid(Animation):
    def __init__(self, pixel_object, color, name=None):
        super().__init__(pixel_object, speed=0, color=color, name=name)
        self.fill(color)

    # def draw(self):
    #     pass  # No need to update the color repeatedly

    def show(self):
        self.fill(self.color)
        self.pixel_object.show()

class LEDController:
    def __init__(self):
        # Get the hostname and select configuration
        hostname = socket.gethostname()
        config = HOSTNAME_CONFIG.get(hostname, HOSTNAME_CONFIG["default"])
        print(f"Running on {hostname} with config: {config['LED_COUNT']} LEDs, pin {config['LED_PIN']}")

        # Set configuration variables
        self.LED_COUNT = config["LED_COUNT"]
        self.LED_PIN = config["LED_PIN"]
        self.LEDSegment = config["SEGMENTS"]

        # Initialize the LED strip
        self.neopixel = NeoPixel(pin=board.D18 if self.LED_PIN == 18 else board.D13, n=self.LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)
        
        # Animation definitions
        self.animation_types = {
            "off": lambda pixels, start, end: CustomSolid(PixelSubset(pixels, start, end + 1), color=(0, 0, 0)),
            "solid_red": lambda pixels, start, end: CustomSolid(PixelSubset(pixels, start, end + 1), color=(255, 0, 0)),
            "rainbow": lambda pixels, start, end: Rainbow(PixelSubset(pixels, start, end + 1), speed=0.1, period=5),
            "chase": lambda pixels, start, end: Chase(PixelSubset(pixels, start, end + 1), speed=0.05, size=3, spacing=6, color=(255, 255, 0)),
            "comet": lambda pixels, start, end: Comet(PixelSubset(pixels, start, end + 1), speed=0.1, color=(0, 255, 255), tail_length=10)
        }
        
        # Dictionary to store animations for each segment
        self.animations = {}
        self.set_default_animations()

    def set_default_animations(self):
        """Set all segments to 'off' as default."""
        for segment in self.LEDSegment:
            start_idx, end_idx = segment.value
            self.animations[segment] = self.animation_types["off"](self.neopixel, start_idx, (end_idx + 1))

    def set_animation(self, segment_name, pattern):
        """Set an animation for a predefined segment."""
        try:
            segment = self.LEDSegment[segment_name]
        except KeyError:
            print(f"Unknown segment: {segment_name} for this device")
            return
        
        if pattern not in self.animation_types:
            print(f"Unknown pattern: {pattern}, using 'off'")
            pattern = "off"

        start_idx, end_idx = segment.value
        self.animations[segment] = self.animation_types[pattern](self.neopixel, start_idx, end_idx)
        print(f"Set {pattern} for {segment_name} (pixels {start_idx} to {end_idx + 1})")

    def run_animation(self):
        """Run all segment animations and update the strip."""
        for segment, animation in self.animations.items():
            if isinstance(animation, CustomSolid):
                # For CustomSolid animations, set the color once and skip animate
                animation.show()
            else:
                animation.animate()
        self.neopixel.show()

    def cleanup(self):
        """Turn off all LEDs and clean up."""
        self.neopixel.fill((0, 0, 0))
        self.neopixel.show()
        self.neopixel.deinit()

def main():
    # Simple test loop for standalone testing
    controller = LEDController()
    try:
        controller.set_animation("SEGMENT1", "solid_red")
        # controller.set_animation("SEGMENT2", "chase")
        # controller.set_animation("SEGMENT3", "comet")
        while True:
            controller.run_animation()
            time.sleep(0.01)
    except KeyboardInterrupt:
        controller.cleanup()

if __name__ == "__main__":
    main()