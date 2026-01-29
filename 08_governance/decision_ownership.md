# Decision Ownership

## Purpose
Prevent duplication, drift, and confusion by making it explicit **who is allowed to decide what**.

## Core rule
Each decision belongs to **exactly one** owner.

- A decision has one authoritative owner.
- Other parts of the system may supply inputs to a decision, but they do not redefine the decision.

## Domain ownership
Decisions are owned by domains.

- Domains own outcomes and invariants.
- Domains are responsible for maintaining the clarity and stability of their decisions.

## UI ownership rule
UI never owns decisions.

- UI may display states and collect user intent.
- UI must not contain business rules, safety rules, or policy rules.

## Controller ownership rule
Controllers orchestrate, they do not decide.

- Controllers compose decisions by gathering inputs and invoking the authoritative decision.
- Controllers may route outcomes (allow/deny, complete/incomplete) but must not redefine the rules.

## When ownership is unclear
If it is unclear who owns a decision:
- Do not implement it.
- Resolve ownership first.
- Only then proceed.
