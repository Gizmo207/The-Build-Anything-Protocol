# Decision Rules: Connections

## Purpose
Define deterministic, default-deny rules for deciding whether a connection is usable.

## Inputs (conceptual)
- Connection evidence status (missing/present/invalid)
- Connection identifier
- Connection type

## Invariants
- If evidence is invalid, the connection is invalid.
- If connectionId is present, connectionType must also be present.
- Missing or insufficient evidence defaults to unusable.

## Outcomes
- Usable
- Unusable (default-deny)
- Invalid (hard failure)

Reference implementation (pure logic):
- `src/domains/connections/pure/connectionUsabilityDecision.ts`

Note: This reference implementation path is expected to exist in an applied product repository, not in this protocol repository.
