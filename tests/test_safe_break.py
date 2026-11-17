"""Tests for Safe-Break incident evidence and control recommendations."""

from __future__ import annotations

import json

import pytest

from safe_break import build_report, load_casebook, recommend_controls


def test_casebook_loads_sourced_microsoft_outage_record():
    casebook = load_casebook()
    assert casebook["incidents"]
    record = casebook["incidents"][0]
    assert record["organization"] == "Microsoft"
    assert record["impact"]["customer_count"] is None
    assert record["sources"]


def test_outage_report_maps_capacity_failover_and_backlog_to_controls():
    casebook = load_casebook()
    report = build_report(casebook)
    controls = report["incidents"][0]["controls_by_failure_mode"]

    assert "reserve headroom and explicit overload thresholds" in controls["capacity_loss"]
    assert "capacity-aware failover rather than unconditional traffic redirection" in controls["dependency_failover"]
    assert "rate-controlled backlog draining after restoration" in controls["recovery_backlog"]


def test_unknown_failure_mode_is_rejected():
    with pytest.raises(ValueError, match="unknown failure modes"):
        recommend_controls({"failure_modes": ["magic_root_cause"]})


def test_duplicate_incident_ids_are_rejected(tmp_path):
    source = load_casebook()
    source["incidents"].append(source["incidents"][0])
    path = tmp_path / "duplicates.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate incident id"):
        load_casebook(path)


def test_source_url_is_required(tmp_path):
    source = load_casebook()
    source["incidents"][0]["sources"][0]["url"] = "file:///etc/passwd"
    path = tmp_path / "bad-url.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(ValueError, match="HTTP"):
        load_casebook(path)
