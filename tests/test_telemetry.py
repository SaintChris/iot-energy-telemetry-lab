import unittest

from src.subscriber import validate_payload
from src.telemetry import generate_sample


class TelemetryTests(unittest.TestCase):
    def test_sample_is_marked_simulated(self):
        sample = generate_sample("device-1", 1)
        self.assertTrue(sample.simulated)

    def test_soc_is_bounded(self):
        for sequence in range(250):
            sample = generate_sample("device-1", sequence)
            self.assertGreaterEqual(sample.battery_soc_pct, 0)
            self.assertLessEqual(sample.battery_soc_pct, 100)

    def test_sequence_and_identity_are_preserved(self):
        sample = generate_sample("device-42", 17)
        self.assertEqual(sample.device_id, "device-42")
        self.assertEqual(sample.sequence, 17)

    def test_power_balance_is_consistent(self):
        for sequence in range(120):
            sample = generate_sample("device-1", sequence)
            expected_grid = round(
                sample.load_power_w - sample.pv_power_w - sample.battery_power_w,
                2,
            )
            self.assertAlmostEqual(sample.grid_power_w, expected_grid, places=2)

    def test_generated_payload_satisfies_contract(self):
        payload = generate_sample("device-1", 1).as_dict()
        validate_payload(payload)

    def test_payload_requires_simulation_marker(self):
        payload = generate_sample("device-1", 1).as_dict()
        payload["simulated"] = False
        with self.assertRaises(ValueError):
            validate_payload(payload)

    def test_payload_requires_all_power_fields(self):
        payload = generate_sample("device-1", 1).as_dict()
        del payload["grid_power_w"]
        with self.assertRaises(ValueError):
            validate_payload(payload)


if __name__ == "__main__":
    unittest.main()
