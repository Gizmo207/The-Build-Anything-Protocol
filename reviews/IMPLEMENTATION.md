# v2 implementation review

## Scope and findings

Base: `01bdeb9328361205a04abbcaaf9c10b251525dbd` (2026-01-30), all 41 tracked Markdown files read before edits. No repository AGENTS.md, .agents/skills, CI, or validator existed at that revision.

The strongest existing principles were default-deny/server authority, single decision ownership, explicit boundary invariants, modular-monolith-first evolution, immutable checkpoints and agent drift safeguards. Their retained governance documents remain authoritative.

The urgent flaw was product-specific assumptions presented as a universal protocol. Missing adoption/evidence mechanics also made it impossible to substantiate repeated compliance. Missing product code here was not itself a flaw: v1 deliberately placed execution in applied repositories.

## Change plan and independent review disposition

One new versioned core plus additive profiles; preserve v1 via immutable history; move product specifics to a historical illustration; provide entrypoint/record/checkpoint/review templates, an evidence checker and tested runnable examples.

Independent reviewer findings incorporated:
- Adoption, measurable acceptance, invariant/risk-to-evidence traceability and exact-version claims.
- Risk-scaled controls, small-change deltas and explicit applicable/not-applicable/unresolved reasoning.
- Actor/action/resource authority, cross-owner denial, verified-token headers, revocation, secret lifecycle, privacy/retention, injection and outbound controls.
- Atomicity, idempotency, current permissions despite immutable receipts, partial failure and all eight reliability concerns.
- Real critical flows, negative checks, resource/accessibility prompts and honest mock/local limits.
- Release artifact/configuration/target, health/stop signals, ownership, code rollback versus data recovery, pre-release audit/usage gates.
- Pinned provenance, untrusted-content handling, context-loss handoff and preserved approval/checkpoint boundaries.
- Paired unsafe/good examples with stored-state assertions and a small finished CLI rather than a large sample app.

## Safety preservation

The four original governance detail files remain unchanged; v2 adds adoption/evidence guidance without relaxing them. APINow product files are moved intact; the product-specific plain-English section is isolated. Historical wording is explicitly qualified by the example README. Published v1 is neither retagged nor rewritten.

The draft does not adopt itself in applications. No Card Ledger file, repository protection, permission, credential, OAuth grant, billing setting or deployed service was changed.

## Validation and review limits

See the task's external evidence directory and checkpoint for exact candidate, actual command outputs, environment/timestamps, digests, and readiness validation. Automated checks are local demonstrations. There is no claim of enforced target merge/release gates, independently generated CI, maintainer approval, a published v2 release, or completed Card Ledger assessment.

The checker validates declared structure/traceability and evidence bytes; a malicious local owner can forge both. Human review of evidence quality, approvals and candidate/build correspondence remains necessary. Local-link checking does not validate anchors or remote availability.

## Publication and next review step

Intended destination, after review and explicit authorization: a feature branch and pull request in `Gizmo207/The-Build-Anything-Protocol`, based on `main`. No push or PR creation is part of this local preparation. Review the diff and evidence, choose the published version, then authorize that destination/action. Never push to or merge main as part of this task.

Before application work resumes, use the exact local protocol candidate for a read-only Card Ledger gap assessment and keep/fix/replace decision. No application implementation should precede that assessment.
