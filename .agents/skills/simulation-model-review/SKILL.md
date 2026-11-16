---
name: simulation-model-review
description: Review Safe-Break's simulation mathematics, metrics and deterministic behavior. Use when changing the simulator, probability model, latency generation, percentiles or report interpretation.
---

# Simulation Model Review

## Review the model before the code
Write down the random variables, their distributions, dependencies and the meaning of each parameter. Confirm whether the baseline and faulted runs are paired or independent. Do not silently change the experiment design.

## Metric rules
- Availability = successful simulated requests / total simulated requests.
- Failed requests must reconcile exactly with total minus succeeded.
- Latency summaries must document whether they include failed requests; preserve the current implementation's convention or explicitly migrate it with tests and release notes.
- Percentile method must be documented. Do not compare percentile values across implementations without checking the definition.
- Round only for presentation; retain adequate precision during calculation.

## Statistical discipline
- Avoid claiming confidence intervals, reliability estimates or significance unless implemented and mathematically justified.
- A single seeded run is a reproducibility fixture, not a statistical conclusion.
- For distributional claims, run multiple predeclared seeds and report sample count and dispersion.
- Test boundary conditions: 1 request, maximum requests, 0%/100% failure probabilities, zero jitter and large finite latency values.
- Check that paired random draws do not accidentally couple unrelated failure mechanisms.

## Change procedure
1. State old and new equations.
2. Add focused tests for both normal and boundary cases.
3. Update README formulas and report interpretation.
4. Run full unit tests and CLI smoke tests.
5. Record exact commands and observed results.
6. Keep the change small enough to review.

## Forbidden shortcuts
Never change expected outputs merely to make a test pass. Never call synthetic outputs "production metrics." Never insert arbitrary safety or reliability scores without an explicit, tested formula.
