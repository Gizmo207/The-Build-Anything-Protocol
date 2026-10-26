# Web profile

MUST define supported browsers/viewports and critical flows. Inspect rendered output, keyboard/focus, labels, error/loading/empty states, and chosen accessibility criteria. Use [W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/); automated scans alone cannot establish conformance.

MUST select identity/backend modules for authenticated or data-changing flows. Browser state/UI visibility is never authority. Check encoding, sessions/cookies, cross-origin protections, sensitive caching, repeated submissions and navigation/cancellation as applicable.

SHOULD test representative mobile input and network failure. Measure relevant performance against stated budgets when risk warrants it; record browser/device evidence and coverage gaps.
