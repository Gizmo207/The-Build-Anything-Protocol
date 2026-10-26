# Protocol version

**2.0.0-draft.1** — proposed for review; not a published release. Core, profiles, and checker travel together at one pinned repository revision.

v1.0 was locked. Its contract is preserved at historical commit [01bdeb9328361205a04abbcaaf9c10b251525dbd](https://github.com/Gizmo207/The-Build-Anything-Protocol/tree/01bdeb9328361205a04abbcaaf9c10b251525dbd). This is a new version, not a behavior change inside v1.0. Do not rewrite published history or move tags.

## Version policy

- Major: change required behavior, gates, or compatibility.
- Minor: compatible additions/optional profiles.
- Patch: clarifications/fixes without requirement changes.
- Drafts are explicit proposals. A maintainer reviews and chooses the release version before publication.
- Pin version plus full source commit or artifact SHA-256; a moving branch is insufficient.
- Published artifacts are immutable. Corrections create a new version with migration notes.
- Profile and tool changes receive the same review as the core.

## Migrate from v1

1. Preserve existing instructions, invariants, checkpoints, and approvals. Do not auto-update consumers.
2. Record current pin, actual state, gaps, owner, and proposed adoption scope.
3. Replace implicit product assumptions with selected profiles; the historical product example is informative only.
4. Map CP-1 through CP-3 to actual historical artifacts. Never manufacture retrospective passes. CP-4 remains authorized execution in an applied project. Do not advance a checkpoint marked not started without explicit instruction.
5. Add measurable acceptance, exact-version evidence, exceptions, delivery/recovery, and entrypoint instructions.
6. Review safety equivalence and unresolved gaps, then explicitly adopt the new pin. Until then v2 adoption is pending.

The six core gates supplement the 01–10 reasoning sequence and do not reinterpret old checkpoint claims.
