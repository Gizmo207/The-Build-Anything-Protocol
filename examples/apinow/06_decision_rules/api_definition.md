# Decision Rules: API Definition Completeness

## Purpose
Define deterministic, default-deny rules for deciding whether an API definition is complete enough to publish/execute.

## Inputs (conceptual)
- Definition evidence status (missing/present/invalid)
- Definition name
- Target resource
- Explicit inputs defined
- Explicit outputs defined

## Invariants
- Missing or partial definition defaults to incomplete.
- Invalid evidence produces invalid.

## Outcomes
- Complete
- Incomplete (default-deny)
- Invalid (hard failure)

Reference implementation (pure logic):
- `src/domains/api-definitions/pure/apiDefinitionCompletenessDecision.ts`

Note: This reference implementation path is expected to exist in an applied product repository, not in this protocol repository.
