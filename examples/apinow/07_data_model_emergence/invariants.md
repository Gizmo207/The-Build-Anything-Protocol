# Invariants (Control Plane)

This document defines the **durable truths** the control plane must enforce.

These are not implementation details.
They are the invariants implied by:
- The proven decision rules (`build_anything_protocol/06_decision_rules/`)
- The entity model (`entities.md`) and relationships (`relationships.md`)

---

## Identity invariants
Reference: `06_decision_rules/identity.md`

- Identity evidence status is always one of: missing, present, invalid.
- If identity evidence is not present, the system must not treat an actor as identified.
- If an actor reference exists for a request context, identity evidence must be present.
- If a tenant/workspace association exists for a request context, an actor reference must exist.
- Any invariant violation represents an invalid identity attempt (hard failure), not “unauthenticated”.

---

## Tenant and membership invariants
- All control-plane objects are scoped to exactly one tenant.
- A user may only act within a tenant if there exists an active `TenantMembership` linking that user to that tenant.
- Membership changes are auditable events.

---

## Connection invariants
Reference: `06_decision_rules/connections.md`

- A `Connection` belongs to exactly one tenant.
- A connection is only usable when:
  - Evidence is present
  - `connectionId` and `connectionType` are both present
- If a connection is referenced by an API definition, the connection must exist and belong to the same tenant.
- Connection secrets are never stored in client-accessible fields; they are referenced via `secretRef` (server-side only).

---

## Data exposure invariants
Reference: `06_decision_rules/exposure.md`

- Data exposure must be explicit.
- An empty or missing selection set is treated as blocked (default-deny).
- Exposure policies are reviewable based solely on declared selections.
- If an API definition references an exposure policy, it must belong to the same tenant.

---

## API definition invariants
Reference: `06_decision_rules/api_definition.md`

- An API definition is incomplete unless:
  - Evidence is present
  - `name` and `resource` are present
  - `inputsDefined` and `outputsDefined` are true
- An incomplete API definition must not be publishable or executable.
- An API definition references exactly one connection.

---

## API version invariants
- `ApiVersion` is the consumer stability boundary.
- Once published, an `ApiVersion` is immutable.
- A version references exactly one API definition (and belongs to the same tenant).
- Audit and usage records may reference API definitions and/or API versions depending on granularity.

---

## Audit invariants (later, but required)
- Audit events are append-only.
- Audit events are tenant-scoped.
- Audit events can be linked to actor, API definition, and optionally API version.

---

## Usage invariants (later, but required)
- Usage is measured and enforced on execution paths.
- Usage records are tenant-scoped and linkable to API definition and optionally API version.
