# Safe-Break — Skills Index

These are task-specific playbooks for coding agents and human contributors. Read the relevant skill before changing that part of the system.

## Canonical skills

### `chaos-scenario-design`

Design deterministic offline failure scenarios for Safe-Break. Use when adding or reviewing latency, error, dependency-outage or resilience scenarios; do not use this skill to target or disrupt real systems.

- Canonical: [`.agents/skills/chaos-scenario-design/SKILL.md`](.agents/skills/chaos-scenario-design/SKILL.md)
- Claude Code discovery: [`.claude/skills/chaos-scenario-design/SKILL.md`](.claude/skills/chaos-scenario-design/SKILL.md)

### `simulation-model-review`

Review Safe-Break's simulation mathematics, metrics and deterministic behavior. Use when changing the simulator, probability model, latency generation, percentiles or report interpretation.

- Canonical: [`.agents/skills/simulation-model-review/SKILL.md`](.agents/skills/simulation-model-review/SKILL.md)
- Claude Code discovery: [`.claude/skills/simulation-model-review/SKILL.md`](.claude/skills/simulation-model-review/SKILL.md)

### `safe-chaos-release-review`

Perform the safety and release gate for Safe-Break. Use before merging changes that touch scenarios, execution, integrations, outputs or claims about real infrastructure.

- Canonical: [`.agents/skills/safe-chaos-release-review/SKILL.md`](.agents/skills/safe-chaos-release-review/SKILL.md)
- Claude Code discovery: [`.claude/skills/safe-chaos-release-review/SKILL.md`](.claude/skills/safe-chaos-release-review/SKILL.md)


## Required workflow for all skills
1. Read root `AGENTS.md` and the selected skill.
2. Inspect the relevant implementation and tests before proposing changes.
3. State assumptions and stop when required evidence or product semantics are missing.
4. Implement a minimal patch with tests.
5. Run the documented checks and report exact results.
6. Update docs and `PROJECT_STATUS.md` only when supported by code and verification.

## Portability
- Codex-style repository skill discovery: `.agents/skills/<skill-name>/SKILL.md`.
- Claude Code project skill discovery: `.claude/skills/<skill-name>/SKILL.md`.
- Other coding models: read `AGENTS.md` and this index, then open the selected canonical skill.

The Claude entries are intentionally short pointers to the canonical documents to reduce duplication. When moving or renaming a canonical skill, update its Claude discovery entry and this index in the same change.

## `multi-agent-review-handoff`

Coordinate research, implementation, independent review and verification across coding models for Safe-Break. Use for any non-trivial simulator or resilience change.

- Canonical: [`.agents/skills/multi-agent-review-handoff/SKILL.md`](.agents/skills/multi-agent-review-handoff/SKILL.md)
- Claude discovery: [`.claude/skills/multi-agent-review-handoff/SKILL.md`](.claude/skills/multi-agent-review-handoff/SKILL.md)
