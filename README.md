# Safe-Break

**Purpose:** turn real service incidents and controlled failure experiments into reusable resilience improvements.

Safe-Break is not an internet-wide attack tool. It is an engineering learning system for authorized staging environments, local test services and sourced incident records.

## MVP: incident casebook

Install with `python -m pip install -e .`, then run `safe-break list` or `safe-break report`.

## Microsoft 365 / Outlook incident (12–13 November 2026)

The preliminary vendor explanation described three interacting factors: a latent gateway defect introduced in a July change, Teams traffic shifting to the primary gateway after a failover, and nearly 14% of gateway capacity being unavailable. The resulting overload made recovery difficult as queued traffic accumulated. Microsoft said there was no evidence of malicious activity. This record is marked as preliminary, reported evidence; final vendor review remains pending in the cited reporting.

Sources: [BleepingComputer, 16 Nov 2026](https://www.bleepingcomputer.com/news/microsoft/microsoft-says-months-old-bug-caused-global-microsoft-365-outage/), [The Verge, 17 Nov 2026](https://www.theverge.com/tech/1035364/microsoft-outlook-outage-notepad), [AP, 17 Nov 2026](https://apnews.com/article/6376045281feb430c0b923e3a4b251c2).

## Resilience controls

- Realistic heterogeneous load testing.
- Reserve capacity and load shedding.
- Backpressure, bounded queues and rate-limited recovery.
- Failure-domain-aware failover.
- Retry budgets, exponential backoff and jitter.
- Independent synthetic health checks.
- Staged canaries and tested rollback.
- Recovery drills with realistic backlog replay.

## Safety boundary

Start with disposable local or staging targets. Any future fault injector must require explicit target allowlisting, authorization proof, a maximum test duration, rate limits, rollback/stop conditions and a production-target denylist. Do not run destructive tests against third-party or production services without formal authorization.

Run tests with `pytest -q`. Controls are candidates for architecture-specific review and validation, not proof of resilience.

---

## Examples Used
- Studying a cloud-service outage caused by gateway overload
- Testing backpressure and bounded queues in a staging service
- Practising rollback after a controlled failure experiment
