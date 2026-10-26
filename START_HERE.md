# Start here

1. Read existing instructions, protocol records and checkpoints. Inspect actual artifacts, tests, dependencies, and working tree before editing; preserve unrelated work.
2. Pin the protocol version and source revision, select profiles, and classify risk using [ADOPTION.md](ADOPTION.md).
3. Follow all [core gates](CORE.md). On existing projects, record a baseline and gaps rather than fabricating historical passes.
4. Retain evidence for the exact candidate and hand it off for review. Release only to an authorized destination.

## The familiar phase map

The numbered phases remain the canonical reasoning sequence. Inspect in the order that helps orientation, then resolve dependencies in this sequence. Revisit earlier decisions when evidence changes. Small fixes reuse approved artifacts and record relevant deltas; ten separate documents are not required.

| Phase | Question | Result |
| --- | --- | --- |
| [01 PRD](01_prd/README.md) | Why, for whom, and what outcome? | Scope and measurable acceptance |
| [02 Users](02_user_stories/README.md) | Who acts or is affected? | Actors, goals, accessibility needs |
| [03 Journeys](03_user_journeys/README.md) | What happens, including failure? | Flows and state transitions |
| [04 Capabilities](04_capabilities/README.md) | What must it do? | Abilities and exclusions |
| [05 Domain map](05_domain_map/README.md) | Who owns decisions/state? | Boundaries and dependencies |
| [06 Rules](06_decision_rules/README.md) | What must always hold? | Contracts and enforcement |
| [07 Data](07_data_model_emergence/README.md) | What truth survives/changes? | Integrity and recovery |
| [08 Governance](08_governance/README.md) | Who may decide/approve? | Authority and exceptions |
| [09 Testing](09_testing_strategy/README.md) | What supports each claim? | Risk-based results |
| [10 Delivery](10_delivery_and_ops/README.md) | How is it delivered/recovered? | Release and observation |

No database, cloud account, login, control-plane service, or distributed architecture is implied.
