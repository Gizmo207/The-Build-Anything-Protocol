# Decision Rules: Data Exposure

## Purpose
Define deterministic, default-deny rules for deciding whether data exposure is allowed.

## Inputs (conceptual)
- Exposure evidence status (missing/present/invalid)
- Explicit exposure selections (resources and optional fields)

## Invariants
- Implicit exposure is forbidden.
- Empty or missing selections default to blocked.
- Exposure decisions must be reviewable from declared selections alone.

## Outcomes
- Allowed
- Blocked (default-deny)
- Invalid (hard failure)

Reference implementation (pure logic):
- `src/domains/data-exposure-policy/pure/dataExposureDecision.ts`

Note: This reference implementation path is expected to exist in an applied product repository, not in this protocol repository.
