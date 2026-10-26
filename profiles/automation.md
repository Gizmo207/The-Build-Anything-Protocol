# Automation, CLI, and infrastructure profile

MUST bound targets/authority before mutations and verify resolved paths, accounts, environments, least privilege, inputs, exit codes, and useful errors. Test safe reruns, partial failure, cancellation, concurrent execution and idempotency where applicable.

Consequential/destructive actions MUST preserve confirmations, provide a reviewable plan/dry run where feasible, and define recovery. Dry-run success does not prove execution. Do not perform live destructive experiments.

Jobs MUST have owner, schedule/timezone, overlap policy, retry limits and failure signals. Infrastructure/configuration changes need drift/dependency review, prior configuration availability and rollback/repair. Checklist compliance grants no permission to alter credentials, access, billing or production.
