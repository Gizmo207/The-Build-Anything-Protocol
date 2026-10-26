# Relationships

These are conceptual relationships that should remain stable even if implementation details change.

## Tenant / Workspace
- Tenant 1..N TenantMemberships
- Tenant 1..N Connections
- Tenant 1..N ExposurePolicies
- Tenant 1..N ApiDefinitions
- Tenant 1..N ApiVersions
- Tenant 1..N AuditEvents
- Tenant 1..N UsageRecords

## User
- User 0..N TenantMemberships

## TenantMembership
- TenantMembership belongs to exactly 1 Tenant
- TenantMembership belongs to exactly 1 User

## Connection
- Connection belongs to exactly 1 Tenant
- Connection is referenced by 0..N ApiDefinitions

## ExposurePolicy
- ExposurePolicy belongs to exactly 1 Tenant
- ExposurePolicy is referenced by 0..N ApiDefinitions (optional depending on model)

## ApiDefinition
- ApiDefinition belongs to exactly 1 Tenant
- ApiDefinition references exactly 1 Connection
- ApiDefinition references 0..1 ExposurePolicy
- ApiDefinition 0..N ApiVersions
- ApiDefinition 0..N AuditEvents
- ApiDefinition 0..N UsageRecords

## ApiVersion
- ApiVersion belongs to exactly 1 ApiDefinition
- ApiVersion belongs to exactly 1 Tenant
- ApiVersion 0..N AuditEvents
- ApiVersion 0..N UsageRecords

## AuditEvent (later)
- AuditEvent belongs to exactly 1 Tenant
- AuditEvent optionally references User (or service actor reference)
- AuditEvent optionally references ApiDefinition and/or ApiVersion

## UsageRecord (later)
- UsageRecord belongs to exactly 1 Tenant
- UsageRecord optionally references ApiDefinition and/or ApiVersion
