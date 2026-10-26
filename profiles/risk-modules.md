# Risk-triggered controls

These modules add controls to [the core](../CORE.md). Mark applicability in the record.

## Identity and authorization

MUST define trusted identity verification, actor/action/resource authorization, least privilege, ownership/tenant boundaries and negative tests. Do not trust arbitrary identity headers or local client state. Cryptographically verified bearer tokens can legitimately be transported in headers. Define expiry, revocation/session invalidation policy and stale-permission behavior. Recheck live authorization at consequential actions; immutable content snapshots do not preserve old access rights.

## Data and privacy

MUST define authoritative state, schema/integrity constraints, atomic transitions, conflict handling, classification, minimization, retention/deletion, and redacted logs. Use parameterization/encoding rather than string-built queries. Define migration/compatibility, backups or repair, and recovery evidence proportionate to impact. Secrets need provision, storage, access, rotation, revocation and incident response; never put credentials in client artifacts/logs.

## Payments and value

MUST verify provider authenticity and authoritative amounts/currency/account ownership. Use idempotency, atomic durable records/reconciliation and replay protection as applicable. Test duplicate/delayed/out-of-order delivery, partial failure, and refund/repair boundaries. Enforcement and metering required for safety or billing must work before release. Sandbox tests do not prove live settlement. Spending/refunds/billing changes retain required human authorization.

## External integrations

MUST identify targets, permissions, timeouts, retry limits, failure mapping and side-effect ownership. Validate outbound destinations where user-supplied locations can cause SSRF; control schemes, addresses/redirects and network reachability appropriate to the environment. Use least-privileged credentials, contract tests, and representative dependency failure/recovery checks. No blind retry of non-idempotent effects.

## Operations

MUST record exact artifact/configuration/target, health/smoke checks, owner, success/abort thresholds, observation interval, incident response and recovery. Audit/usage controls required by security or billing are release gates, not indefinite later work. Prefer staged rollout for material risk when feasible. Test data restoration/repair separately from application rollback.
