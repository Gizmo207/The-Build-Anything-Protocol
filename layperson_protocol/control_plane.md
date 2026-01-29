# Control Plane (Plain-English)

## Think of the control plane as the system’s “memory of truth”
It is the place where we store:
- Who owns what
- What is allowed
- What exists
- What is published

It is like a **library** of official records.

## Why we need it
If the system keeps truth only in people’s heads or only on the screen:
- Someone can forget.
- Someone can bypass it.
- Different parts of the system can disagree.

A control plane prevents that by keeping one durable source of truth.

## How it relates to action
The part of the system that “does things” must follow the control plane’s truth.

Control plane = “what is true and allowed”
Execution = “do the action, but only after the gates say yes”

## The big idea
The control plane makes safety and ownership durable.
