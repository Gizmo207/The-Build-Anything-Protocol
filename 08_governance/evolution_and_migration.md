# Evolution and Migration Rules

## Purpose
Define how behavior and public artifacts evolve over time without silent breaking changes.

## Core principle
Change is inevitable. Breaking changes must be explicit.

## Versioning over mutation
When behavior is relied upon by others:
- Prefer creating a new version rather than mutating the existing one.

This prevents:
- Silent breaking changes
- Confusing rollbacks
- “Works yesterday, broken today” failures

## Immutability of published artifacts
Once something is published (made available to external consumers):
- Treat it as immutable.
- If changes are required, create a new version.

## Migration discipline
When introducing a new version:
- Provide a clear migration path.
- Make compatibility expectations explicit.
- Avoid "flag days" where all consumers must change at once.

## Backwards compatibility is a deliberate choice
Compatibility should be:
- explicit
- tested
- documented

Never assume compatibility “just happens.”
