# Deployment Model (APINow V2)

## Goal
Deploy safely with low operational friction while the domain model stabilizes.

---

## Phase 1–2: Vercel-hosted Next.js (monolith)
### Components
- Next.js app (UI)
- Next.js route handlers (API surface)
- Firestore (control plane)
- External databases (data plane)

### Why
- Fast iteration
- Minimal infrastructure overhead
- Keeps product + API evolution tightly coupled early

---

## Boundaries (must hold even in a monolith)
- UI: presentation only (no business decisions)
- Controllers: orchestration only
- Pure domain decisions: deterministic logic only
- Services/adapters: I/O only

---

## Phase 3+ (optional): Extract dedicated API service
Trigger conditions:
- Execution workload outgrows Next.js route handler constraints
- Need for dedicated networking, connection pooling strategies, queueing
- Need for stronger isolation between UI deploys and API deploys

What stays constant:
- Domain boundaries
- Decision rules
- Data model responsibilities

---

## Operational checklist (minimum)
- Verified identity on all protected routes
- Secrets stored server-side only
- Audit events emitted on meaningful transitions and executions
- Usage measured and enforced on execution paths
