# AI Usage Rules

## Purpose
Define how AI is allowed to help so it remains a force multiplier instead of a source of drift.

These rules apply to any project.

## What AI is allowed to do
- Generate scaffolding that follows established structures.
- Implement changes that are explicitly requested.
- Refactor within existing boundaries when requested.
- Add tests for deterministic logic.
- Summarize current state and produce handoff reports.

## What AI must never do
- Invent business rules or policy semantics.
- Smuggle decisions into UI, controllers, or “helpers”.
- Introduce new architectures or technologies without explicit instruction.
- Make broad changes outside the requested scope.
- Add mock/fake data into non-test paths.

## Checkpoint discipline
AI changes must respect checkpoints.

- If a checkpoint says a phase is “not started,” AI must not begin it without an explicit instruction.
- AI should update checkpoint artifacts only when instructed.

## Protocol boundary discipline
AI must follow the engineering protocol and the build-anything protocol.

- Decisions remain single-owned.
- Invariants are enforced at boundaries.
- Pure logic stays pure.

## When AI is uncertain
If ownership, invariants, or scope are unclear:
- AI should stop and ask for clarification.
- No guessing.
