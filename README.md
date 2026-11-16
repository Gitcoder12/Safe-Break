# Safe-Break

Break systems, expose weaknesses and build resilience — **safely**.

Safe-Break starts with an offline chaos-engineering simulator. It compares a baseline service model with a faulted model and reports availability and latency changes. It does not connect to, interrupt, or reconfigure real systems.

## Current scope

- Deterministic baseline-versus-fault comparison.
- Simulated added latency, additional request failures and dependency outage.
- Request count, success/failure count, availability, mean, p50 and p95 latency.
- JSON scenario input and JSON report output.
- Seeded runs for reproducible tests.

Not implemented: live network proxies, container control, Kubernetes integration, process termination, production fault injection, automatic remediation or distributed tracing.

## Requirements

- Python 3.10 or later
- No third-party runtime dependencies

## Run

```bash
python safebreak.py examples/latency-and-errors.json --seed 7
python safebreak.py examples/latency-and-errors.json --seed 7 --output report.json
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Scenario fields

| Field | Meaning |
|---|---|
| `requests` | Number of simulated requests (1–100,000) |
| `base_latency_ms` | Baseline model latency in milliseconds |
| `jitter_ms` | Maximum uniform latency variation |
| `baseline_failure_rate` | Baseline request failure probability (0–1) |
| `extra_latency_ms` | Added latency in the faulted model |
| `additional_failure_rate` | Additional failure probability applied by the fault |
| `dependency_available` | Set false to simulate a complete dependency outage |

## Safety boundary

This release is a mathematical simulation only. It does not accept target URLs or shell commands, open sockets, stop processes, change host resources, or modify infrastructure. Do not interpret simulated latency or availability as measurements of a real deployment.

## Reproducibility

Provide an explicit `--seed` value and keep the scenario JSON with the output report. Results are deterministic for the same source version, scenario and seed.
