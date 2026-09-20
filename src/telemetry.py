from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import math


@dataclass(frozen=True)
class EnergyTelemetry:
    device_id: str
    timestamp: str
    sequence: int
    pv_power_w: float
    load_power_w: float
    battery_power_w: float
    battery_soc_pct: float
    grid_power_w: float
    simulated: bool = True

    def as_dict(self) -> dict:
        return asdict(self)


def generate_sample(device_id: str, sequence: int) -> EnergyTelemetry:
    phase = sequence % 120
    daylight = max(0.0, math.sin(math.pi * phase / 120))
    pv = round(5000 * daylight, 2)
    load = round(900 + 250 * math.sin(sequence / 8), 2)

    net = pv - load
    battery = round(max(-1800, min(1800, -net * 0.45)), 2)
    grid = round(load - pv - battery, 2)
    soc = round(max(10, min(95, 55 + 20 * math.sin(sequence / 50))), 2)

    return EnergyTelemetry(
        device_id=device_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        sequence=sequence,
        pv_power_w=pv,
        load_power_w=load,
        battery_power_w=battery,
        battery_soc_pct=soc,
        grid_power_w=grid,
    )
