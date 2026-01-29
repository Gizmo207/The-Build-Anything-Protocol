# Testing Strategy

## Goal
Prove the decision rules and safety invariants are correct, and prevent regressions.

## Focus
- Pure decision logic gets the most tests.
- Controllers orchestrate and should be tested at boundary level.
- Services/adapters are tested for I/O correctness and error mapping.

## Non-goals
- No snapshot testing of business rules in UI.
- No "mocked" production behavior outside tests.

## Regression anchors
- `legacy/analysis/legacy_read_report.md` is the anti-regression checklist.
- Tests should explicitly cover the mistakes V1 made (e.g., identity from headers, implicit exposure).
