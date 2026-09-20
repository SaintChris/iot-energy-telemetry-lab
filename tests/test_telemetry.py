import unittest

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


if __name__ == "__main__":
    unittest.main()
