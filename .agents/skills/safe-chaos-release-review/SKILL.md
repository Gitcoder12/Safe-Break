---
name: safe-chaos-release-review
description: Perform the safety and release gate for Safe-Break. Use before merging changes that touch scenarios, execution, integrations, outputs or claims about real infrastructure.
---

# Safe-Break Safety and Release Review

## Scope gate
Confirm that all code remains offline and deterministic. Search changed files for network clients, socket creation, subprocess execution, shell invocation, process termination, container APIs, Kubernetes clients and host mutation. Any such capability is outside the MVP and must not be slipped in as a convenience.

## Integrity gate
- Scenario parsing rejects unknown fields and invalid values.
- Input files are not modified.
- Output paths do not overwrite files without explicit consent.
- Reports identify the execution mode as simulation.
- Synthetic examples are named and described as synthetic.
- No secrets, user data or environment details are committed.

## Correctness gate
- Run `python -m unittest discover -s tests -v`.
- Run each documented CLI example.
- Parse generated JSON with Python's JSON parser.
- Verify deterministic output with the same seed.
- Inspect edge cases and error messages.

## Documentation gate
README must distinguish implemented, not implemented and future work. Every metric must define its unit and computation. Any caveat about model omissions must remain visible.

## Reviewer report
Provide changed files, commands, actual pass/fail counts, behavior changes, residual risks and rollback instructions. Never claim a check was run if it was not. Do not merge automatically.
