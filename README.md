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


---

## Comparison with Existing Open-Source Projects

Safe-Break is documented as an authorized resilience-learning system that turns real service incidents and controlled failure experiments into reusable engineering controls. Its current MVP is an incident casebook, with explicit safety boundaries for any future fault injection. These projects provide adjacent chaos-engineering references.

| Project | Established focus | Relationship to Safe-Break |
|---|---|---|
| [Chaos Mesh](https://github.com/chaos-mesh/chaos-mesh) | Cloud-native chaos engineering for Kubernetes environments | A mature fault-injection platform; Safe-Break's current focus is incident learning and a controlled path toward resilience experiments, not a Kubernetes chaos operator. |
| [Litmus](https://github.com/litmuschaos/litmus) | Chaos engineering framework and experiment orchestration | Provides established experiment templates and workflows; Safe-Break aims to connect incident evidence to selected resilience controls and learning records. |
| [Chaos Monkey](https://github.com/Netflix/chaosmonkey) | Randomized failure injection to test resilience in production-like systems | A foundational chaos-engineering reference; Safe-Break's intended approach is more explicitly casebook- and authorization-gated. |

### Where Safe-Break is different
- **Incident-to-control learning:** the product concept connects a documented failure mechanism to candidate controls and follow-up experiments.
- **Evidence-aware casebook:** the README distinguishes preliminary vendor statements from verified root causes and retains source links.
- **Strict authorization boundary:** future fault injection is intended only for approved local/staging targets with allowlists, time limits and rollback controls.

### Where established projects are stronger
Chaos Mesh and Litmus provide actual experiment orchestration and infrastructure integrations. Safe-Break's current MVP is a casebook, not a fault-injection engine or proof that a service is resilient.

### Safety and evidence requirements
Preserve incident source dates and evidence status, separate reported causes from independently confirmed causes, and do not generalize one outage into universal controls. Any future experiment must require target authorization, bounded duration, rate limits, stop conditions and rollback. This is a learning-workflow comparison, not a resilience certification.
