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

## BYOD (Bring Your Own Database)

### Explain like I’m 10
Imagine APINow is like a universal power strip.

- **[the database is the thing you plug in]**
  - Your database can be many kinds: SQLite, Postgres, MySQL, MSSQL, Mongo, Google Sheets.

- **[an adapter is the plug shape]**
  - An adapter exists for a *family* of databases, not for every company that sells a database.
  - That means we do not need “60 adapters” for “60 providers”.

- **[why we don’t need 60 adapters]**
  - Many providers use the same underlying database family.
  - If two providers both speak “Postgres-style SQL”, they can use the same adapter family.

- **[the adapter does not decide who is allowed]**
  - Adapters are execution-only: they run the query.
  - Adapters do not control access.
  - Adapters do not make decisions.

### Explain like I’m a developer

BYOD in APINow V2 is implemented by separating:
- **[decisions]** control-plane gates (CP-2)
- **[execution]** execution-plane adapters + runtime wiring (CP-3)

This gives the “bring your own database” property:
- Adding a database family is primarily: implement adapter + register it.
- Runtime stays stable because adapter selection is explicit and centralized.

#### Adapter families (explicit)
- **[SQLite]**
  - SQLite adapter executes read-only queries against a local SQLite file.

- **[SQL-family (Postgres / MySQL / MSSQL)]**
  - One adapter family covers multiple SQL engines that share the same overall query model.
  - A driver port can later implement the engine-specific details, but the adapter boundary stays the same.

- **[Mongo]**
  - Mongo adapter family covers MongoDB-style query execution.

- **[Google Sheets]**
  - Google Sheets adapter family covers read access via the Sheets API.

#### Are adapters per database or per provider?
- **[per database family]**
  - APINow targets a small set of adapter families.
  - A “provider” is not an adapter concern.

#### Why APINow does NOT need 60 adapters
- **[because providers collapse into families]**
  - Most “different databases” are really the same engine with different hosting.
  - The adapter speaks the database family’s protocol, not the vendor’s brand.

#### How SQL-family adapters support many databases
- **[shared contract, pluggable driver]**
  - A SQL-family adapter implements the same `SqlQueryExecutorPort` as SQLite.
  - The adapter delegates low-level execution to a driver interface.
  - That means Postgres/MySQL/MSSQL support can share the same adapter shape.

#### Why this design is safe and scalable
- **[safe: default-deny]**
  - Execution does not happen unless CP-2 gates return allowed.

- **[safe: adapters are execution-only]**
  - Adapters do not make decisions and do not control access.

- **[scalable: stable runtime]**
  - Runtime orchestration does not grow linearly with database providers.
  - New support is added by implementing and registering adapters, not rewriting runtime logic.
