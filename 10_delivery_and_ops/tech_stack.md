# Tech Stack (APINow V2)

## Goal
Choose a stack that:
- Ships quickly (phase 1–2)
- Enforces security invariants by default
- Keeps boundaries clean (pure decisions vs I/O)
- Can evolve into separate services without a rewrite

---

## Frontend
### Next.js (App Router) + React
Why:
- Already adopted in this repo and ecosystem
- Vercel-native deployment and ergonomics
- Strong fit for dashboards and product UX
- Server Components can reduce client complexity when used intentionally

---

## Backend / Runtime
### Next.js Route Handlers (initially)
Why:
- Lowest friction for phase 1–2
- Co-locates API surface with the product while the domain model stabilizes
- Easy migration path later (extract to a dedicated API service when pressure demands)

Principle:
- Start as a modular monolith.
- Evolve outward only when necessary.

---

## Control Plane Database (metadata)
### Firebase Firestore
Why it fits:
- Excellent for multi-tenant metadata and rapid iteration
- Strong integration with Firebase Auth
- Good match for: tenants, users, connections metadata, API definitions, policies, usage, audit events

What Firestore is for (V2):
- Control plane state (who owns what, what is configured, what is allowed)

What Firestore is not for (V2):
- Not the data plane for customer data (that remains in connected sources)

---

## Auth
### Firebase Auth (ID tokens) as the canonical identity signal
Non-negotiables:
- No caller-controlled identity headers as source of truth
- No localStorage “auth hacks” as security boundaries
- Every server request that depends on identity must verify tokens

---

## Data Plane (connected sources)
### Direct DB clients per engine, behind services
- PostgreSQL: `pg`
- MySQL/MariaDB: `mysql2`
- MongoDB: `mongodb`
- MSSQL: `mssql`
- Google Sheets: Google APIs (service account)
- SQLite: local/dev only (explicitly not a production write store)

Constraints:
- DB access is isolated behind services/adapters (I/O only)
- Controllers orchestrate only
- Decisions (identity, usability, exposure, definition completeness) are evaluated before any data access
- Secrets never reach the client

---

## Payments
### Stripe
Constraints:
- Enforcement happens on execution paths (decision/controller), not UI
- Plans/limits are measured and enforced server-side

---

## Observability
Phase 1:
- Structured server logs + Firestore audit events (control plane)

Phase 2:
- Centralized logging/metrics (provider choice is an ops decision)

---

## Summary
This stack is intentionally conservative:
- It matches your current deployment model.
- It emphasizes security and boundaries.
- It keeps a clean upgrade path to dedicated services later.
