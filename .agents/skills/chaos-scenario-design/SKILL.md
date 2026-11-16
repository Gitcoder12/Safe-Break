---
name: chaos-scenario-design
description: Design deterministic offline failure scenarios for Safe-Break. Use when adding or reviewing latency, error, dependency-outage or resilience scenarios; do not use this skill to target or disrupt real systems.
---

# Chaos Scenario Design

## Goal
Create minimal, interpretable, reproducible offline scenarios that isolate one failure mechanism at a time.

## Workflow
1. Read `README.md`, `safebreak.py`, the example JSON and current tests before changing scenario semantics.
2. State the hypothesis in one sentence (for example: "an unavailable dependency drives faulted availability to zero").
3. Start from a control scenario with no injected fault. Add one changed variable for the experiment.
4. Use only the supported schema: `name`, `requests`, `base_latency_ms`, `jitter_ms`, `baseline_failure_rate`, `extra_latency_ms`, `additional_failure_rate`, and `dependency_available`.
5. Choose explicit values and explain their units and ranges. Rates are probabilities from 0 to 1, not percentages from 0 to 100.
6. Record the random seed and preserve the JSON scenario with any report.
7. Explain what the model omits: retries, queues, correlated failures, multi-hop dependencies and real infrastructure behavior.
8. Add a test for the expected direction of the result, not a brittle exact statistical value unless the seed makes the case deterministic.

## Required checks
- The no-fault control has equal baseline and faulted metrics.
- A dependency outage gives zero faulted availability.
- Added latency increases modeled latency but does not itself change success count.
- Additional failure probability cannot improve expected availability.
- Invalid, non-finite, negative or out-of-range inputs are rejected.
- Same scenario and seed produce identical output.

## Output format
For each scenario provide: hypothesis, changed parameters, seed, command, observed output, interpretation, limitations and regression test.

## Safety boundary
Do not convert an offline scenario into a live endpoint, shell command, process kill, infrastructure mutation or production fault-injection action.
