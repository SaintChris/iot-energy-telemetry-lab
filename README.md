# IoT Energy Telemetry Lab

Public-ready learning project for synthetic solar/battery telemetry over MQTT.

## Goal

Demonstrate a small, reproducible IoT pipeline without using employer/customer data or production equipment.

```text
Synthetic PV/Battery Simulator
        ↓
       MQTT
        ↓
    Mosquitto
        ↓
Subscriber / validation
        ↓
future: time-series DB + dashboard + alerting
```

## What it demonstrates

- telemetry data modeling
- device identity
- timestamps and sequence numbers
- MQTT topic design
- connection/retry behavior
- JSON validation
- offline-safe synthetic testing
- separation of simulated and production data

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d
python -m src.publisher
```

In another terminal:

```bash
source .venv/bin/activate
python -m src.subscriber
```

## Topic model

`lab/energy/<device_id>/telemetry`

## Safety boundary

All readings are synthetic. No IREE/customer site identifiers, credentials, inverter endpoints, or production telemetry are used.
