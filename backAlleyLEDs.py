import paho.mqtt.client as mqtt
import logging
import time
import board
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

logging.basicConfig(filename="backAlleyLEDs.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a')

log = logging.getLogger()
log.setLevel(logging.DEBUG)
#parameters for mqtt
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60
#parameters for LED strip
MY_STRIP_LEN = 26
PI_PIN = board.D18
np = NeoPixel(PI_PIN, MY_STRIP_LEN, brightness=1, auto_write=False)
current_message = 9

off = Solid(np, color=color.BLACK)
solid = Solid(np, color=color.GREEN)
blink = Blink(np, speed=0.5, color=color.RED)
colorcycle = ColorCycle(np, speed=0.4, colors=[color.MAGENTA, color.ORANGE, color.TEAL])
chase = Chase(np, speed=0.005, color=color.WHITE, size=3, spacing=6)
comet = Comet(np, speed=0.01, color=color.PURPLE, tail_length=10, bounce=True)
pulse = Pulse(np, speed=0.1, color=color.AMBER, period=3)
rainbow = Rainbow(np, speed=0.1, period=2)
rainbow_chase = RainbowChase(np, speed=0.1, size=5, spacing=3)
rainbow_comet = RainbowComet(np, speed=0.03, tail_length=7, bounce=True)
rainbow_sparkle = RainbowSparkle(np, speed=0.1, num_sparkles=15)
sparkle = Sparkle(np, speed=0.05, color=color.AMBER, num_sparkles=10)
sparkle_pulse = SparklePulse(np, speed=0.05, period=3, color=color.JADE)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    log.info(f"Connected to {mqttc.host} with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("backAlleyLEDPattern")
    log.info(f"Subscribed to 'backAlleyLEDPattern' topic")
    blink.animate()

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    log.info("Disconnected with result code: %s", reason_code)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        log.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            log.info("Reconnected successfully!")
            return
        except Exception as err:
            log.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    log.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global current_message
    log.info(f"Received message '{int(msg.payload)}'")
    previous_message = None
    current_message = int(msg.payload)
    if current_message != previous_message:
        log.info(f"Payload changed to '{current_message}'")
        previous_message = current_message

def executeAnimations(current_message):
    match current_message:
        case 0:
            off.animate()       
        case 1 :
            solid.animate()
        case 2 :
            blink.animate()
        case 3 :
            colorcycle.animate()
        case 4 :
            chase.animate()
        case 5 :
            comet.animate()
        case 6 :
            pulse.animate()
        case 7 :
            rainbow.animate()
        case 8 :
            rainbow_chase.animate()
        case 9 :
            rainbow_comet.animate()
        case 10 :
            rainbow_sparkle.animate()
        case 11 :
            sparkle.animate()
        case 12 :
            sparkle_pulse.animate()
        case 13 :
            animations = AnimationSequence(
                blink,
                colorcycle,
                chase,
                comet,
                pulse,
                rainbow,
                rainbow_chase,
                rainbow_comet,
                rainbow_sparkle,
                sparkle,
                sparkle_pulse,
                advance_interval=3,
                auto_clear=True,
            )
            animations.animate()

if __name__ == "__main__":

    # mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # mqttc.on_connect = on_connect
    # mqttc.on_message = on_message
    # mqttc.on_disconnect = on_disconnect

    # mqttc.connect("10.169.84.20", 1883, 60)
    # while True:
    #     executeAnimations(current_message)
    #     try:
    #         mqttc.loop()
    #     except KeyboardInterrupt:
    #         off.animate()
    #         log.info("Exiting")
    #         break
    #     except Exception as e:
    #         log.error(f"Error: {e}")
    #         break


    for i in range(24, 26):
        np[i] = color.GREEN
    np.show()
    #off.animate()
