# Decision Rules: Identity

## Purpose
Define deterministic, default-deny rules for deciding whether a request has an identifiable actor.

## Inputs (conceptual)
- Identity evidence status (missing/present/invalid)
- Actor (type + id) when evidence is present
- Tenant/workspace association

## Invariants
- Actor may only be present when evidence is present.
- Tenant/workspace may only be present when actor is present.
- Any invariant violation is treated as an invalid identity attempt.

## Outcomes
- Identified
- Unauthenticated (default-deny)
- Invalid (hard failure)

Reference implementation (pure logic):
- `src/domains/identity-access/pure/identityDecision.ts`
