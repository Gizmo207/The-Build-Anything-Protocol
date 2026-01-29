# Build Anything Protocol

Plain-English explanation for non-technical readers → [layperson_protocol/README.md](./layperson_protocol/README.md)


This folder captures product and system thinking.
It answers:
- What are we building?
- Why are we building it?
- What must be true?

This protocol is intentionally framework-agnostic.

---

## Checkpoint System

### What checkpoints are
Checkpoints are **checkpointed architectural accountability**.
They are repo-local “save points” that capture what is true at major milestones.

### Why checkpoints exist
- Prevents drifting away from protocol invariants
- Makes architecture and intent reviewable over time
- Creates a durable paper trail for future engineers and AI assistants
- Forces explicit statements about what is complete vs intentionally not started

### Where checkpoints live
- `/checkpoints/`

### Discipline
- Each checkpoint is written once.
- If revised, add dated sections rather than rewriting history.
- Major phases should not advance without an explicit checkpoint.
