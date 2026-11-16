---
name: multi-agent-review-handoff
description: Coordinate research, implementation, independent review and verification across coding models for Safe-Break. Use for any non-trivial simulator or resilience change.
---

# Multi-Agent Review Handoff — Safe-Break

## Roles
- **Research lead (for example, Claude):** frame the resilience question, find primary references where needed, define the model assumptions and propose falsifiable behavior. Deliver a short evidence/method note; do not edit source files during this phase.
- **Implementation engineer (for example, ChatGPT/Codex):** implement the approved scenario/model change on one feature branch, update tests and docs, and report exact commands.
- **Independent reviewer (for example, DeepSeek):** inspect the diff read-only. Challenge probability semantics, hidden coupling, metric definitions, reproducibility and safety boundaries. Do not edit the same files as the implementer.
- **Verifier:** run tests, CLI examples, deterministic repeat checks and inspect report output. It may be a different model or the human maintainer.
- **Human maintainer:** approves scope, resolves disagreements and merges.

## Handoff contract
Every task begins with a one-page brief: hypothesis, current behavior, desired behavior, supported scenario fields, model assumptions, non-goals, files expected to change and acceptance tests.

Research notes must distinguish literature-supported claims from assumptions. Code changes must not turn a paper's benchmark or an illustrative number into a simulator default without justification.

## Parallel-work rules
- One writer owns a given file at a time.
- Reviewer works read-only against a pinned commit SHA.
- If reviewer finds a defect, implementation engineer makes the correction in a new commit; reviewer checks the new SHA.
- Do not let two agents modify probability equations, metric definitions or scenario schema concurrently.
- Adjudicate disagreements using explicit equations, code, tests and evidence—not majority vote.

## Release gate
The final handoff lists commit SHA, diff summary, tests actually run, tests not run, output sample, known model limitations and residual safety risks. Simulated output must remain labelled synthetic. No live fault injection or production access is authorized by this workflow.
