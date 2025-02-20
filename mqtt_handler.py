import asyncio
import paho.mqtt.client as mqtt
from led_controller import LEDController

# MQTT configuration
MQTT_BROKER = "10.169.84.20"  # Replace with your MQTT broker address
MQTT_PORT = 1883
MQTT_TOPIC = "backAlleyTest"

class MQTTHandler:
    def __init__(self):
        self.led_controller = LEDController()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT broker")
            client.subscribe(MQTT_TOPIC)
        else:
            print(f"Failed to connect with code: {reason_code}")

    def on_message(self, client, userdata, msg):
        """Handle incoming messages on the 'led_pattern' topic."""
        payload = msg.payload.decode().strip()
        print(f"Received message: {payload}")
        try:
            # Expected format: "start:end:pattern"
            start_idx, end_idx, pattern = payload.split(":")
            start_idx = int(start_idx)
            end_idx = int(end_idx)
            self.led_controller.set_animation(start_idx, end_idx, pattern)
        except ValueError:
            print(f"Invalid message format: {payload}, expected 'start:end:pattern'")

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        print(f"Disconnected from MQTT broker with code: {reason_code}")

    async def run_mqtt(self):
        """Start the MQTT client in a non-blocking way."""
        self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        self.client.loop_start()
        
        try:
            while True:
                self.led_controller.run_animation()
                await asyncio.sleep(0.01)  # Small delay to prevent CPU hogging
        except asyncio.CancelledError:
            print("MQTT loop cancelled")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            self.led_controller.cleanup()

async def main():
    handler = MQTTHandler()
    await handler.run_mqtt()

if __name__ == "__main__":
    asyncio.run(main())