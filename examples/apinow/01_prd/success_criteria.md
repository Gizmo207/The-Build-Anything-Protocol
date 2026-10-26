# Success Criteria

## Product success
- A developer can go from "I have a data source" to "I have a working API" quickly, with clear guardrails.
- The system is **default-deny**: nothing is exposed or executable until explicitly defined.
- Sharing an API never requires sharing database credentials.

## Safety success
- Identity cannot be forged (no caller-controlled headers as identity).
- Data exposure is explicit and reviewable.
- Endpoint definitions are complete, consistent, and versionable.

## Engineering success
- Clear domain boundaries exist and are enforceable in code.
- Pure decision logic is isolated from I/O.
- The system remains understandable: small, cohesive files with stable responsibilities.

## Operational success
- Failures are diagnosable.
- Usage/limits are enforced on the paths that matter (execution).
- Audit records exist for access attempts and outcomes.
