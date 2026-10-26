# Plain-English Protocol (for non-technical readers)

Start with the [v2 core](../CORE.md). Every build needs a clear goal, rules, checks and a receipt showing which version was checked. Small changes can use a short receipt; dangerous changes need stronger evidence and the existing human approvals. Missing or failed checks must stay visible.

The "rooms" and "memory" below describe responsibilities, not a requirement to install services or databases. A document, local tool, game and deployed app use the same core with relevant [profiles](../profiles/README.md).

This folder explains how this project is built using simple ideas and analogies.

If you imagine the system as a building:
- **Rules** are the posted signs that say what is allowed.
- **Locks** are what physically stop bad actions.
- **Gates** are checkpoints that decide “yes” or “no” before anything happens.
- **Memory** is where the system stores the truth so it can’t be forgotten.

## What you can read here
- `checkpoints.md` — “save points” where we stop and write down what is true.
- `architecture.md` — how the building is organized into rooms with clear responsibilities.
- `decision_rules.md` — the system’s rulebooks that always give the same answer.
- `governance.md` — who is allowed to make rules, and how we prevent chaos.
- `control_plane.md` — the part of the system that stores truth and permissions.
