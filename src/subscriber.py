from __future__ import annotations

import json
import os

import paho.mqtt.client as mqtt


BROKER = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.subscribe("lab/energy/+/telemetry", qos=1)


def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    required = {
        "device_id",
        "timestamp",
        "sequence",
        "pv_power_w",
        "battery_soc_pct",
        "simulated",
    }
    missing = required - payload.keys()
    if missing:
        raise ValueError(f"missing telemetry fields: {sorted(missing)}")
    print(message.topic, payload)


def main() -> None:
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="energy-lab-subscriber",
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
