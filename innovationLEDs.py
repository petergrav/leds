import paho.mqtt.client as mqtt
import logging
import board
import neofuncs
import adafruit_led_animation.color as color

MY_STRIP_LEN = 60
PIXEL_PIN = board.D18

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
        neofuncs.neo_off(PIXEL_PIN, MY_STRIP_LEN)
    if (int(msg.payload)) == 1 :
        neofuncs.neo_range(PIXEL_PIN, MY_STRIP_LEN, color.GREEN, 10, 20)
        neofuncs.neo_range(PIXEL_PIN, MY_STRIP_LEN, color.GREEN, 30, 40)
    if (int(msg.payload)) == 2 :
        neofuncs.neo_fill(PIXEL_PIN, MY_STRIP_LEN, color.RED)
    if (int(msg.payload)) == 3 :
        neofuncs.neo_fill(PIXEL_PIN, MY_STRIP_LEN, color.GREEN)
    if (int(msg.payload)) == 4 :
        neofuncs.neo_sparkle(PIXEL_PIN, MY_STRIP_LEN, color.WHITE, 0.5, 30)
    if (int(msg.payload)) == 5 :
        neofuncs.neo_sweep(PIXEL_PIN, MY_STRIP_LEN, color.RED, 5, 1)
    if (int(msg.payload)) == 6 :
        neofuncs.neo_flash(PIXEL_PIN, MY_STRIP_LEN, color.RED, 30, 50, 0.1, 0.1, 10)
    

if __name__ == "__main__":
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect("10.169.84.20", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
    mqttc.loop_forever()