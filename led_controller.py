import time
#from rpi_ws281x import PixelStrip, Color
from neopixel import NeoPixel
import board
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet

# LED strip configuration
LED_COUNT = 26        # Number of LED pixels
LED_PIN = 18         # GPIO pin connected to the pixels (18 uses PWM)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal
LED_BRIGHTNESS = 0.2  # Set to 0-1 (max brightness)
LED_INVERT = False    # True to invert the signal
LED_CHANNEL = 0       # Set to 1 for GPIOs 13, 19, 41, 45, or 53

class LEDController:
    def __init__(self):
        # Initialize the LED strip
        #self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        #self.strip.begin()
        self.neopixel = NeoPixel(pin=board.D18, n=LED_COUNT, bpp=3, brightness=LED_BRIGHTNESS, auto_write=False)
        # Animation definitions
        self.animation_types = {
            "off": lambda pixels: Solid(pixels, color=(0, 0, 0)),
            "solid_red": lambda pixels: Solid(pixels, color=(255, 0, 0)),
            "rainbow": lambda pixels: Rainbow(pixels, speed=0.1, period=5),
            "chase": lambda pixels: Chase(pixels, speed=0.05, size=3, spacing=6, color=(255, 255, 0)),
            "comet": lambda pixels: Comet(pixels, speed=0.1, color=(0, 255, 255), tail_length=10)
        }
        
        # List to store active animations with their pixel ranges
        self.animations = []  # Format: [(start_idx, end_idx, animation_obj), ...]
        self.set_default_animation()

    def set_default_animation(self):
        """Set all pixels to 'off' as default."""
        self.animations = [(0, LED_COUNT - 1, self.animation_types["off"](self.neopixel))]

    def set_animation(self, start_idx, end_idx, pattern):
        """Set an animation for a specific range of pixels."""
        start_idx = max(0, min(start_idx, LED_COUNT - 1))
        end_idx = max(start_idx, min(end_idx, LED_COUNT - 1))
        
        if pattern not in self.animation_types:
            print(f"Unknown pattern: {pattern}, using 'off'")
            pattern = "off"

        # Create a new animation for the range
        new_animation = self.animation_types[pattern](self.neopixel)
        
        # Adjust existing animations to accommodate the new range
        updated_animations = []
        for anim_start, anim_end, anim in self.animations:
            if anim_end < start_idx or anim_start > end_idx:
                # No overlap, keep as is
                updated_animations.append((anim_start, anim_end, anim))
            else:
                # Overlap detected, split the existing range
                if anim_start < start_idx:
                    updated_animations.append((anim_start, start_idx - 1, anim))
                if anim_end > end_idx:
                    updated_animations.append((end_idx + 1, anim_end, anim))

        # Add the new animation
        updated_animations.append((start_idx, end_idx, new_animation))
        self.animations = sorted(updated_animations, key=lambda x: x[0])  # Sort by start index
        print(f"Set {pattern} for pixels {start_idx} to {end_idx}")

    def run_animation(self):
        """Run all animations and update the strip."""
        for start_idx, end_idx, animation in self.animations:
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
        controller.set_animation(0, 9, "rainbow")  # First 10 LEDs
        controller.set_animation(10, 19, "chase")  # Next 10 LEDs
        controller.set_animation(20, 29, "comet")  # Next 10 LEDs
        while True:
            controller.run_animation()
            time.sleep(0.01)
    except KeyboardInterrupt:
        controller.cleanup()

if __name__ == "__main__":
    main()