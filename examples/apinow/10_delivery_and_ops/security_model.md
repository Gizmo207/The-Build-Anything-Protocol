# Security Model (APINow V2)

## Goal
Make unsafe states impossible by default.

This model is explicitly designed to avoid V1 failure modes:
- trusting caller-provided identity headers
- storing secrets client-side
- implicit exposure
- UI-driven “security”

---

## Identity
Source of truth:
- Firebase Auth ID tokens verified server-side

Rules:
- Identity must be verified on every request that depends on identity
- Caller-controlled headers are never accepted as identity signals

---

## Authorization
Principles:
- Default-deny when rules are missing or ambiguous
- Ownership boundaries are enforced server-side

---

## Secrets
Principles:
- Secrets never reach the browser
- Secrets are stored server-side only (control plane secret storage strategy)

Rules:
- API execution uses connection IDs / secret references
- Connection strings/passwords are never returned in API responses

---

## Data Exposure
Principles:
- Exposure must be explicit and reviewable
- Unselected data is not exposed

Rules:
- Execution is gated by the exposure decision outcome

---

## API Definitions
Principles:
- Definitions exist server-side and are auditable
- Incomplete definitions are not publishable or executable

Rules:
- Execution is gated by the definition completeness decision outcome

---

## Usage / Rate limits
Principles:
- Enforcement occurs on the execution path
- Measurement is server-side

---

## Auditability
Principles:
- Record access attempts and outcomes
- Make it possible to answer: who accessed what, when, and with what outcome

---

## Threat model reminders
- Never trust the client.
- Never trust headers.
- Treat UI as an untrusted presenter.
- Decisions must be centralized and deterministic.
