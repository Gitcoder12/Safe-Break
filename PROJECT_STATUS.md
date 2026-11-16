# Project Status — Safe-Break

**Updated:** 2026-11-16
**Current stage:** Offline simulation MVP

## Implemented
- Baseline-versus-faulted request simulation.
- Added latency, additional error probability and dependency-outage scenarios.
- Deterministic seeded runs and JSON reports.
- Input validation and unit tests.

## Not implemented
- Live service probing or fault injection.
- Kubernetes/container/process controls.
- Distributed tracing, retries, queues or multi-service dependency graphs.
- Automatic remediation or production deployment safeguards.

## Known limitations
- Results are simulated; they are not measurements from a real service.
- The model does not represent retries, queues, correlated failures or complex dependency graphs.
- Faulted latency is an input assumption, not an observed metric.

## Next steps
1. Add an explicit dependency graph and retry/backoff model.
2. Add circuit-breaker and bulkhead simulations with deterministic tests.
3. Add scenario comparison reports and configuration versioning.
4. Only consider live fault injection after a separate isolated sandbox, explicit target allowlist, dry-run mode, approval gate and rollback contract exist.

## Verification
Run `python -m unittest discover -s tests -v`. Record the command and actual result here after each change.
