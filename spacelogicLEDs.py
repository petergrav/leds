import paho.mqtt.client as mqtt
import LEDStates
import neofuncs
import board
from neopixel import NeoPixel
import adafruit_led_animation.color as color

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("LEDPattern")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
   # MY_STRIP_LEN = 300
   # pixel_pin = board.D18
   # np = NeoPixel(pixel_pin, MY_STRIP_LEN)
    print(int(msg.payload))
    if (int(msg.payload)) == 0 :
        neofuncs.neo_off()
    if (int(msg.payload)) == 1 :
        neofuncs.neo_range(color.GREEN, 80, 120)
        neofuncs.neo_range(color.GREEN, 225, 265)
    if (int(msg.payload)) == 2 :
        neofuncs.neo_fill((color.RED))
    if (int(msg.payload)) == 3 :
        neofuncs.neo_fill((color.GREEN))
    if (int(msg.payload)) == 4 :
        neofuncs.neo_sparkle((color.WHITE), 0.1, 30)
    if (int(msg.payload)) == 5 :
        neofuncs.neo_sweep((color.RED), 10, 0)
    if (int(msg.payload)) == 6 :
        neofuncs.neo_flash((color.RED), 225, 265, 0.1, 0.1, 10)
    

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("10.169.84.20", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()