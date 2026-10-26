# Build Anything Protocol

An engineering standard operating procedure for every build and consequential change: define the outcome, preserve safety boundaries, implement within scope, and produce evidence for the exact version delivered.

**Proposed version: 2.0.0-draft.1.** One core with additive profiles, not separate forks. It reduces avoidable failures; it does not promise perfect software or certify production readiness.

Start with [START_HERE.md](START_HERE.md), follow [CORE.md](CORE.md), and use the [adoption kit](ADOPTION.md). [Plain-English explanations](layperson_protocol/README.md) explain the same rules.

## What is mandatory

Record scope, ownership, requirements, risk, applicable profiles, verification, delivery/recovery, and remaining limits on every change. Scale evidence to risk; a small artifact can use one short record and reuse approved design artifacts with a relevant delta. Unknown is not a pass.

Preserve stronger project rules and user confirmation requirements. The protocol never grants authority to deploy, publish, spend, change access, or perform destructive actions.

## Repository map

- [Core gates](CORE.md): universal requirements.
- [Profiles](profiles/README.md): platform and risk-triggered additions.
- [01–10 phase map](START_HERE.md): familiar planning vocabulary.
- [Templates](templates/README.md): entrypoint, manifest, checkpoint, review.
- [Validation](tools/README.md): executable checks and their limits.
- [Runnable project and bad/good code](examples/reference/README.md): demonstrated behavior and tests.
- [Historical APINow example](examples/apinow/README.md): illustration, never a default architecture.
- [Version policy](PROTOCOL_VERSION.md) and [public sources](SOURCES.md).

This repository applies its own gates when changing the protocol or tooling. Product execution checkpoints remain in applied product repositories.
