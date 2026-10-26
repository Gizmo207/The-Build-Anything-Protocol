# Decision Rules (Plain-English)

## What is a decision rule?
A decision rule is like a **rulebook**.

If you ask it the same question twice, it must give the same answer.
It does not guess.

Here "same question" means the same explicit inputs, including current verified permissions. If permissions change, a later action must use the new truth; an old saved result does not grant access forever.

## Why we treat decision rules as special
Decision rules are the system’s **gates**.
They decide “yes” or “no” before anything dangerous or irreversible happens.

## Default behavior: lock first
When the system is unsure, it should act like a door with a lock:
- If we don’t have enough information → the door stays locked.

This prevents accidents.

## What decision rules are NOT
- They are not “opinions.”
- They are not “UI checks.”
- They are not “best effort.”

## The big idea
Decision rules make safety predictable.
They are how we avoid repeating past mistakes.
