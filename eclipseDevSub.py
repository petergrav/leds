import paho.mqtt.client as mqtt
import neopixeltest
import neopixelEBO

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("LEDPattern")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(int(msg.payload))
    if (int(msg.payload)) == 1 :
        neopixelEBO.green()
    if (int(msg.payload)) == 2 :
        neopixelEBO.red()
    if (int(msg.payload)) == 3 :
        neopixelEBO.blue()
    if (int(msg.payload)) == 0 :
        neopixelEBO.off()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("10.169.84.20", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()