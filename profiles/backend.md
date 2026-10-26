# API, backend, and worker profile

MUST define contracts, validation, actor/action/resource authorization, errors, resource limits, compatibility, and state ownership. Test denied/cross-owner/tenant access where applicable. Verified bearer tokens may arrive in headers; unverified caller claims cannot establish identity.

MUST review transactions/constraints, check/use races, concurrency, pagination/query counts, timeouts, bounded retries, idempotency, cancellation and partial failure where relevant. Workers need duplicate/out-of-order and poison-message handling. Prefer atomic operations over distributed locks; if locks are needed address ownership, lease expiry and stale writers.

MUST test relevant integration/persistence paths against representative dependencies. Define retention/deletion, secret references, redacted audit, backup/restore, migration compatibility, rollout/stop thresholds and code/data recovery. Load/failover claims require measurements for the stated topology. Select applicable risk modules.
