"""Offline, deterministic chaos simulation for service-resilience experiments.

This module never opens sockets, kills processes, changes host settings, or
injects faults into a real service. It models request outcomes in memory.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Scenario:
    name: str
    requests: int = 1000
    base_latency_ms: float = 80.0
    jitter_ms: float = 10.0
    baseline_failure_rate: float = 0.01
    extra_latency_ms: float = 0.0
    additional_failure_rate: float = 0.0
    dependency_available: bool = True

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Scenario":
        if not isinstance(raw, dict):
            raise ValueError("scenario must be a JSON object")
        allowed = set(cls.__dataclass_fields__)
        unknown = set(raw) - allowed
        if unknown:
            raise ValueError(f"unknown scenario fields: {', '.join(sorted(unknown))}")
        try:
            scenario = cls(**raw)
        except TypeError as exc:
            raise ValueError(f"invalid scenario fields: {exc}") from exc
        scenario.validate()
        return scenario

    def validate(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if isinstance(self.requests, bool) or not isinstance(self.requests, int) or not 1 <= self.requests <= 100_000:
            raise ValueError("requests must be an integer from 1 to 100000")
        for key in ("base_latency_ms", "jitter_ms", "extra_latency_ms"):
            value = getattr(self, key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"{key} must be a finite non-negative number")
        if self.base_latency_ms <= 0:
            raise ValueError("base_latency_ms must be greater than zero")
        for key in ("baseline_failure_rate", "additional_failure_rate"):
            value = getattr(self, key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{key} must be a finite number between 0 and 1")
        if not isinstance(self.dependency_available, bool):
            raise ValueError("dependency_available must be a boolean")


@dataclass(frozen=True)
class RunMetrics:
    requests: int
    succeeded: int
    failed: int
    availability_pct: float
    mean_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int((len(ordered) - 1) * percentile + 0.5)))
    return round(ordered[index], 3)


def _metrics(successes: int, latencies: list[float]) -> RunMetrics:
    count = len(latencies)
    failed = count - successes
    return RunMetrics(
        requests=count,
        succeeded=successes,
        failed=failed,
        availability_pct=round((successes / count) * 100, 3) if count else 0.0,
        mean_latency_ms=round(statistics.fmean(latencies), 3) if latencies else 0.0,
        p50_latency_ms=_percentile(latencies, 0.50),
        p95_latency_ms=_percentile(latencies, 0.95),
    )


def run_simulation(scenario: Scenario, seed: int = 7) -> dict[str, Any]:
    """Compare baseline and faulted outcomes using paired random draws."""
    scenario.validate()
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    rng = random.Random(seed)
    baseline_successes = 0
    faulted_successes = 0
    baseline_latencies: list[float] = []
    faulted_latencies: list[float] = []

    for _ in range(scenario.requests):
        jitter = rng.uniform(-scenario.jitter_ms, scenario.jitter_ms)
        baseline_draw = rng.random()
        injected_failure_draw = rng.random()
        baseline_latency = max(0.0, scenario.base_latency_ms + jitter)
        faulted_latency = max(0.0, baseline_latency + scenario.extra_latency_ms)
        baseline_latencies.append(baseline_latency)
        faulted_latencies.append(faulted_latency)

        baseline_failed = baseline_draw < scenario.baseline_failure_rate
        fault_failed = injected_failure_draw < scenario.additional_failure_rate
        if not baseline_failed:
            baseline_successes += 1
        if scenario.dependency_available and not baseline_failed and not fault_failed:
            faulted_successes += 1

    return {
        "scenario": asdict(scenario),
        "seed": seed,
        "execution_mode": "offline_simulation_only",
        "baseline": asdict(_metrics(baseline_successes, baseline_latencies)),
        "faulted": asdict(_metrics(faulted_successes, faulted_latencies)),
        "limitations": [
            "This is a mathematical simulation, not a test of a deployed service.",
            "Latency values are synthetic scenario inputs and are not measured response times.",
            "The model does not capture retries, queues, correlated failures, or service dependencies beyond the single availability switch.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a safe, offline service-resilience simulation.")
    parser.add_argument("scenario", type=Path, help="Path to a scenario JSON file")
    parser.add_argument("--seed", type=int, default=7, help="Deterministic random seed")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args(argv)
    try:
        raw = json.loads(args.scenario.read_text(encoding="utf-8"))
        result = run_simulation(Scenario.from_dict(raw), seed=args.seed)
        rendered = json.dumps(result, indent=2)
        if args.output:
            args.output.write_text(rendered + "\\n", encoding="utf-8")
        else:
            print(rendered)
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"safebreak: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
