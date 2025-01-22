import paho.mqtt.client as mqtt
import logging
import board
import neofuncs
import adafruit_led_animation.color as color
from neopixel import NeoPixel
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.sequence import AnimationSequence

MY_STRIP_LEN = 25 #565
PI_PIN = board.D13
np = NeoPixel(PI_PIN, MY_STRIP_LEN, brightness=1, auto_write=False)

logging.basicConfig(filename="innovationLEDs.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a')

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    log.info(f"Connected to {mqttc.host} with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("innovationLEDPattern")
    log.info(f"Subscribed to 'innovationLEDPattern' topic")

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    log.info(f"Received message '{int(msg.payload)}'")
    if (int(msg.payload)) == 0 :
        np = NeoPixel(PI_PIN, MY_STRIP_LEN, brightness=0, auto_write=False)
        np.show()        
    if (int(msg.payload)) == 1 :
        neofuncs.neo_range(PI_PIN, MY_STRIP_LEN, color.GREEN, 10, 20)
        neofuncs.neo_range(PI_PIN, MY_STRIP_LEN, color.GREEN, 30, 40)
    if (int(msg.payload)) == 2 :
        neofuncs.neo_fill(PI_PIN, MY_STRIP_LEN, color.RED)
    if (int(msg.payload)) == 3 :
        neofuncs.neo_fill(PI_PIN, MY_STRIP_LEN, color.GREEN)
    if (int(msg.payload)) == 4 :
        neofuncs.neo_sparkle(PI_PIN, MY_STRIP_LEN, color.WHITE, 0.5, 30)
    if (int(msg.payload)) == 5 :
        neofuncs.neo_sweep(PI_PIN, MY_STRIP_LEN, color.RED, 5, 1)
    if (int(msg.payload)) == 6 :
        neofuncs.neo_flash(PI_PIN, MY_STRIP_LEN, color.RED, 30, 50, 0.1, 0.1, 10)
    

if __name__ == "__main__":
    # mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # mqttc.on_connect = on_connect
    # mqttc.on_message = on_message
    # mqttc.connect("10.169.84.20", 1883, 60)
    # mqttc.loop_forever()
    
    solid = Solid(np, color=color.GREEN)
    blink = Blink(np, speed=0.5, color=color.JADE)
    colorcycle = ColorCycle(np, speed=0.4, colors=[color.MAGENTA, color.ORANGE, color.TEAL])
    chase = Chase(np, speed=0.1, color=color.WHITE, size=3, spacing=6)
    comet = Comet(np, speed=0.01, color=color.PURPLE, tail_length=10, bounce=True)
    pulse = Pulse(np, speed=0.1, color=color.AMBER, period=3)
    rainbow = Rainbow(np, speed=0.1, period=2)
    rainbow_chase = RainbowChase(np, speed=0.1, size=5, spacing=3)
    rainbow_comet = RainbowComet(np, speed=0.03, tail_length=7, bounce=True)
    rainbow_sparkle = RainbowSparkle(np, speed=0.1, num_sparkles=15)
    sparkle = Sparkle(np, speed=0.05, color=color.AMBER, num_sparkles=10)
    sparkle_pulse = SparklePulse(np, speed=0.05, period=3, color=color.JADE)


    animations = AnimationSequence(
        solid,
        # blink,
        # colorcycle,
        # chase,
        # comet,
        # pulse,
        # rainbow,
        # rainbow_chase,
        # rainbow_comet,
        # rainbow_sparkle,
        # sparkle,
        # sparkle_pulse,
        advance_interval=5,
        auto_clear=False,
    )
    #animations = solid

    while True:
        animations.animate()
        #neofuncs.neo_off(PIXEL_PIN, MY_STRIP_LEN)