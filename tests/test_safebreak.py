import unittest

from safebreak import Scenario, run_simulation


class ScenarioTests(unittest.TestCase):
    def test_rejects_invalid_request_count(self):
        with self.assertRaises(ValueError):
            Scenario.from_dict({"name": "bad", "requests": 0})

    def test_rejects_unknown_fields(self):
        with self.assertRaises(ValueError):
            Scenario.from_dict({"name": "bad", "shell_command": "rm -rf /"})

    def test_seed_makes_results_reproducible(self):
        scenario = Scenario(name="repeatable", requests=200, additional_failure_rate=0.2)
        self.assertEqual(run_simulation(scenario, 42), run_simulation(scenario, 42))

    def test_no_fault_baseline_and_faulted_match(self):
        scenario = Scenario(name="control", requests=500, jitter_ms=0)
        result = run_simulation(scenario, 3)
        self.assertEqual(result["baseline"], result["faulted"])

    def test_total_outage_has_zero_availability(self):
        scenario = Scenario(name="outage", requests=50, dependency_available=False)
        result = run_simulation(scenario, 1)
        self.assertEqual(result["faulted"]["availability_pct"], 0.0)
        self.assertEqual(result["faulted"]["failed"], 50)

    def test_latency_fault_increases_latency_not_success_count(self):
        scenario = Scenario(name="slow", requests=100, extra_latency_ms=125, jitter_ms=0)
        result = run_simulation(scenario, 7)
        self.assertGreater(result["faulted"]["mean_latency_ms"], result["baseline"]["mean_latency_ms"])
        self.assertEqual(result["faulted"]["succeeded"], result["baseline"]["succeeded"])


if __name__ == "__main__":
    unittest.main()
