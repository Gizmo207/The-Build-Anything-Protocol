# Invariant Enforcement Points

## Purpose
Invariants are non-negotiable truths.
This document defines **where** invariants must be enforced so they cannot be bypassed.

## What an invariant is
An invariant is a rule that must always hold.

- If an invariant is violated, the system must treat it as a hard failure or a default-deny outcome.
- Invariants are not suggestions and not “best effort”.

## Core rule
Invariants must be enforced at system boundaries.

### Boundary examples (conceptual)
- Before persisting or mutating durable state
- Before executing privileged actions
- Before publishing or making something externally available
- Before performing any irreversible operation

## UI-only enforcement is forbidden
UI validation is helpful, but it is not a safety boundary.

- UI checks can be bypassed.
- UI checks can become stale.
- UI checks cannot be trusted.

Therefore:
- Invariants must never rely on UI-only validation.

## “Checked earlier” is not a guarantee
The system must not assume a prior layer validated something.

- Re-check invariants at the boundary where they matter.
- Prefer explicit enforcement over implicit trust.
