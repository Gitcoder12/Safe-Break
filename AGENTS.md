# Safe-Break — Agent Engineering Contract

## Mission
An offline, deterministic service-resilience simulator. It models baseline and faulted request outcomes; it does not inject faults into real infrastructure.

## Codebase map
`safebreak.py` contains Scenario validation, seeded simulation and metric reporting. `examples/latency-and-errors.json` is a synthetic scenario. `tests/test_safebreak.py` holds the regression suite.

## First actions for every task
1. Read this file, `SKILLS.md`, `PROJECT_STATUS.md` and the relevant skill before editing.
2. Inspect the current branch and working tree. Do not assume the repository is at the revision described in old notes.
3. Trace the complete execution path for the behavior being changed. Search callers, tests, CLI entry points and documentation.
4. State the problem, expected behavior, affected files, risks and verification plan before making a broad change.
5. Prefer the smallest coherent patch. Preserve public interfaces unless an intentional migration is documented.

## Non-negotiable invariants
- The product is offline simulation only: no sockets, target URLs, shell commands, process termination, container/Kubernetes controls or host-setting changes.
- Never describe generated latency as measured latency or simulated availability as production SLO evidence.
- Preserve deterministic results for the same scenario, seed and source revision.
- Baseline and faulted runs must use documented paired random draws; explain which random variables represent baseline and injected failures.
- Validate all scenario values and keep request limits that bound runtime and memory.
- Do not add live chaos injection without a separately approved threat model, isolated sandbox, target allowlist, explicit human approval, rollback contract and independent safety review.

## Environment and verification
Use Python 3.10+ and the standard library unless a dependency is deliberately proposed and justified.

Run the relevant commands:
- `python -m unittest discover -s tests -v`
- `python safebreak.py examples/latency-and-errors.json --seed 7`
- `python safebreak.py examples/latency-and-errors.json --seed 7 --output report.json`

If a command cannot run in the environment, report it as **not run**. Never convert a syntax check into a claim that the whole application works. Add or update regression tests for every behavior change. Inspect actual output files, not just exit codes.

## Engineering standards
- Use type hints and small, cohesive functions.
- Validate untrusted input at boundaries; errors should identify the invalid field and safe correction.
- Keep deterministic behavior where the domain permits it.
- Avoid hidden network calls, background tasks, telemetry and global mutable state.
- Preserve source data and provenance. Write outputs atomically where practical and guard overwrite behavior.
- Keep dependencies minimal. Explain licensing, supply-chain and maintenance impact before adding one.
- Never commit credentials, API keys, private datasets or machine-specific paths.
- Do not invent performance numbers, benchmark results, source records or user-facing capabilities.

## Documentation contract
When behavior changes, update README commands, examples, limitations and `PROJECT_STATUS.md`. Mark a feature as implemented only when code and tests support it. Keep implemented, experimental, planned and unsupported capabilities visibly separate.

## Review and delivery
Every change report must state:
1. What changed and why.
2. Files changed.
3. Exact commands executed and their actual results.
4. Tests not run and why.
5. Data/model assumptions and known limitations.
6. Security or safety implications.
7. Suggested manual review steps.

Do not merge, force-push, rewrite history, edit `main`, or close issues/PRs unless the user explicitly requests that action. Never claim perfect correctness; surface residual risk.

## Skills
Canonical, progressive-disclosure skills live under `.agents/skills/`. Claude Code discovery entries live under `.claude/skills/` and point to the canonical skill. See `SKILLS.md` for the complete index.