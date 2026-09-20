from __future__ import annotations

import json
import os
import time

import paho.mqtt.client as mqtt

from .telemetry import generate_sample


BROKER = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
DEVICE_ID = os.getenv("DEVICE_ID", "synthetic-site-01")
INTERVAL_SECONDS = float(os.getenv("PUBLISH_INTERVAL", "2"))


def main() -> None:
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"{DEVICE_ID}-publisher",
    )
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    try:
        sequence = 0
        while True:
            sample = generate_sample(DEVICE_ID, sequence)
            topic = f"lab/energy/{DEVICE_ID}/telemetry"
            payload = json.dumps(sample.as_dict(), separators=(",", ":"))
            info = client.publish(topic, payload=payload, qos=1, retain=False)
            info.wait_for_publish()
            print(topic, payload)
            sequence += 1
            time.sleep(INTERVAL_SECONDS)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
