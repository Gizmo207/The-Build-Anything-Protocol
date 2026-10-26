# Entities

This is where database schemas "really" come from.

Schemas emerge from:
- Decision inputs
- Invariants
- Lifecycle transitions
- Ownership boundaries

They do not come directly from user stories.

## Control-plane entities (truth model)

The control plane is the durable, auditable source of truth for:
- Ownership (who owns what)
- Configuration (what is intended)
- Policy (what is allowed)
- Lifecycle state (draft/published/versioned)

This is distinct from the data plane (the connected databases themselves).

---

## Tenant / Workspace
**Owns**
- Connections
- Exposure policies
- API definitions
- API versions
- Usage and audit records

**Durability**
- Durable
- Auditable (at least for membership and high-impact config changes)

**Fields (conceptual)**
- tenantId
- name
- status

---

## User (identity linkage only)
This entity exists only to link an upstream identity provider user to a tenant.
It does not contain “authorization logic”; it is reference data for identity decisions.

**Durability**
- Durable
- Auditable (membership changes)

**Fields (conceptual)**
- userId
- identityProvider
- identityProviderSubject
- status

---

## TenantMembership
Represents that a user belongs to a tenant (and optionally their role).

**Durability**
- Durable
- Auditable (membership and role changes)

**Fields (conceptual)**
- membershipId
- tenantId
- userId
- role
- status

---

## Connection
Represents a registered data source reference.

**Decision alignment**
- Provides the durable source for `connectionId` and `connectionType` inputs.

**Durability**
- Durable
- Auditable (creation, updates, disable/revoke)

**Fields (conceptual)**
- connectionId
- tenantId
- connectionType
- status
- secretRef (server-side only)

---

## ExposurePolicy
Represents explicit exposure selections.

**Decision alignment**
- Provides the durable source for `selections` (explicit exposure intent).

**Durability**
- Durable
- Auditable (policy edits)

**Fields (conceptual)**
- exposurePolicyId
- tenantId
- selections (resource + optional fields)
- status

---

## ApiDefinition
Represents the user’s intended API definition (draft state).

**Decision alignment**
- Provides the durable source for:
  - `name`
  - `resource`
  - `inputsDefined`
  - `outputsDefined`

**Durability**
- Durable
- Auditable (definition changes)

**Fields (conceptual)**
- apiDefinitionId
- tenantId
- name
- resource
- inputsDefined
- outputsDefined
- status
- connectionId (reference)
- exposurePolicyId (reference, optional depending on model)

---

## ApiVersion
Represents an immutable, published snapshot of an API definition.
This is the stability boundary for consumers.

**Versioning**
- Immutable once published
- Identified by `(apiDefinitionId, version)` or a unique `apiVersionId`

**Durability**
- Durable
- Auditable (publish events)

**Fields (conceptual)**
- apiVersionId
- apiDefinitionId
- tenantId
- version
- publishedAt
- definitionSnapshot (frozen copy or references to frozen copies)

---

## AuditEvent (later, but must be modeled)
Records access attempts and outcomes.

**Durability**
- Durable
- Append-only semantics

**Fields (conceptual)**
- auditEventId
- tenantId
- actorRef (userId/serviceId)
- apiDefinitionId
- apiVersionId (optional)
- outcome
- occurredAt

---

## UsageRecord (later, but must be modeled)
Represents metering and limit enforcement inputs.

**Durability**
- Durable (aggregated or event-based)

**Fields (conceptual)**
- usageRecordId
- tenantId
- apiDefinitionId
- apiVersionId (optional)
- metric
- countedAt
