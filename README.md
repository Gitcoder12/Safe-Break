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

## Branch Activity & Development History

**Audit date:** 2026-11-18 · **Comparison base:** `main`

| Branch | Difference from `main` | Observed work / changed paths |
|---|---:|---|
| `feat/offline-chaos-simulator-mvp-20261116` | 20 ahead / 2 behind | Offline chaos simulator, scenario examples, simulation/release review skills, agent guidance and tests |
| `feat/outage-casebook` | 7 / 1 | Outage casebook dataset, safe-break implementation, CI/package configuration and tests |

### Open pull requests observed during this audit

- [PR #1 — offline chaos simulator MVP](https://github.com/Gitcoder12/Safe-Break/pull/1)

**Review note:** Keep the simulator offline and bounded. Review scenario assumptions, safety limits and test coverage before merging; the branch comparison does not prove resilience in a live environment. No branches have been merged or deleted by this documentation update.
