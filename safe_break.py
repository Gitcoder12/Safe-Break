"""Offline incident casebook and resilience-control recommendations.

Safe-Break records sourced incidents and maps documented failure modes to
human-reviewable engineering controls. It does not probe or modify production
systems and does not infer root cause from correlation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_CASEBOOK = Path(__file__).resolve().parents[1] / "data" / "incidents.json"

CONTROL_LIBRARY: dict[str, tuple[str, ...]] = {
    "latent_software_defect": (
        "representative load tests across hardware and traffic profiles",
        "staged canary releases with automatic rollback criteria",
        "feature flags and versioned configuration",
        "change-to-impact correlation in incident telemetry",
    ),
    "dependency_failover": (
        "failure-domain-aware routing across independent dependencies",
        "capacity-aware failover rather than unconditional traffic redirection",
        "chaos exercises for simultaneous dependency and capacity loss",
    ),
    "capacity_loss": (
        "reserve headroom and explicit overload thresholds",
        "bounded queues, backpressure and load shedding",
        "capacity alarms that include unavailable infrastructure, not only active traffic",
    ),
    "retry_storm": (
        "exponential backoff with jitter and a strict retry budget",
        "idempotency keys for retried operations",
        "circuit breakers and bounded concurrency",
    ),
    "recovery_backlog": (
        "rate-controlled backlog draining after restoration",
        "recovery load tests with realistic queued traffic",
        "separate recovery capacity from steady-state capacity",
    ),
    "health_check_blind_spot": (
        "independent synthetic health checks",
        "health probes that exercise real user paths and dependencies",
        "cross-region agreement checks with stale-signal detection",
    ),
}


def load_casebook(path: Path = DEFAULT_CASEBOOK) -> dict[str, Any]:
    """Load and structurally validate the incident casebook."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema_version") != "1.0":
        raise ValueError("casebook must be a schema_version 1.0 JSON object")
    incidents = raw.get("incidents")
    if not isinstance(incidents, list):
        raise ValueError("casebook incidents must be an array")
    identifiers: set[str] = set()
    for index, incident in enumerate(incidents):
        if not isinstance(incident, dict):
            raise ValueError(f"incident {index} must be an object")
        required = (
            "id", "organization", "services", "start", "end",
            "failure_modes", "failure_chain", "sources", "evidence_status",
        )
        missing = [field for field in required if field not in incident]
        if missing:
            raise ValueError(f"incident {index} is missing: {', '.join(missing)}")
        incident_id = incident["id"]
        if not isinstance(incident_id, str) or not incident_id.strip():
            raise ValueError(f"incident {index} has an invalid id")
        if incident_id in identifiers:
            raise ValueError(f"duplicate incident id: {incident_id}")
        identifiers.add(incident_id)
        if not isinstance(incident["services"], list) or not incident["services"]:
            raise ValueError(f"{incident_id}: services must be a non-empty array")
        if not isinstance(incident["failure_modes"], list):
            raise ValueError(f"{incident_id}: failure_modes must be an array")
        unknown_modes = set(incident["failure_modes"]) - CONTROL_LIBRARY.keys()
        if unknown_modes:
            raise ValueError(
                f"{incident_id}: unknown failure modes: {', '.join(sorted(unknown_modes))}"
            )
        if not isinstance(incident["failure_chain"], list) or not incident["failure_chain"]:
            raise ValueError(f"{incident_id}: failure_chain must be a non-empty array")
        if not isinstance(incident["sources"], list) or not incident["sources"]:
            raise ValueError(f"{incident_id}: at least one source is required")
        for source in incident["sources"]:
            url = source.get("url") if isinstance(source, dict) else None
            if not isinstance(url, str) or not url.startswith(("https://", "http://")):
                raise ValueError(f"{incident_id}: every source needs an HTTP(S) URL")
    return raw


def recommend_controls(incident: dict[str, Any]) -> dict[str, list[str]]:
    """Return controls keyed by observed failure mode."""
    modes = incident.get("failure_modes")
    if not isinstance(modes, list):
        raise ValueError("incident failure_modes must be a list")
    unknown = set(modes) - CONTROL_LIBRARY.keys()
    if unknown:
        raise ValueError(f"unknown failure modes: {', '.join(sorted(unknown))}")
    return {mode: list(CONTROL_LIBRARY[mode]) for mode in modes}


def build_report(casebook: dict[str, Any]) -> dict[str, Any]:
    """Produce an auditable summary; unknown customer impact remains unknown."""
    reports = []
    for incident in casebook["incidents"]:
        reports.append(
            {
                "id": incident["id"],
                "organization": incident["organization"],
                "services": incident["services"],
                "evidence_status": incident["evidence_status"],
                "failure_chain": incident["failure_chain"],
                "controls_by_failure_mode": recommend_controls(incident),
                "impact": incident.get("impact", {"customer_count": None}),
                "source_urls": [source["url"] for source in incident["sources"]],
                "interpretation": (
                    "Engineering controls are candidate mitigations. Validate them against "
                    "the target service architecture and test them before production use."
                ),
            }
        )
    return {"incident_count": len(reports), "incidents": reports}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe-Break outage casebook")
    parser.add_argument("--casebook", type=Path, default=DEFAULT_CASEBOOK)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list incident identifiers and organizations")
    sub.add_parser("report", help="show failure chains and resilience controls")
    args = parser.parse_args(argv)
    try:
        casebook = load_casebook(args.casebook)
        if args.command == "list":
            result = [
                {"id": item["id"], "organization": item["organization"], "services": item["services"]}
                for item in casebook["incidents"]
            ]
        else:
            result = build_report(casebook)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"safe-break: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
