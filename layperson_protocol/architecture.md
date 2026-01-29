# Architecture (Plain-English)

## Think of the system like a building
A good building has:
- Rooms with clear purposes
- Signs that tell you what each room is for
- Doors that control where you can go

A messy building has:
- A kitchen inside the bathroom
- Important switches in random closets
- No one knows where anything belongs

## Our rule
Every “room” has **one job**.

## Why this matters
It prevents a common failure:
- "We put the rule here just for now" → and then it becomes permanent.

## How we keep it clean
- The **rulebooks** (decision rules) live in their own place.
- The **memory** (truth storage) lives in its own place.
- The **actions** (doing things in the world) happen only after passing gates.

## The big idea
Clear architecture is how we keep the system understandable as it grows.
