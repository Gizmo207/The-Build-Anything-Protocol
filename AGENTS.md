# Protocol repository instructions

Read README.md, START_HERE.md, CORE.md, PROTOCOL_VERSION.md, applicable profiles and 08_governance before edits. Apply the protocol to its own documents, examples, and checker. Record scope, candidate, acceptance, risk, evidence, limitations, review status.

- Preserve locked v1 history and published/checkpoint artifacts. Behavior changes require a new version.
- One core, additive profiles. Product specifics belong only in labeled examples.
- Preserve safety/confirmation requirements. Do not change permissions, branch protection, credentials, billing or deploy services in protocol maintenance.
- Keep changes local until publication destination and authorized action are explicit.
- Run `python -m unittest discover -s tests -v` and `python tools/check_protocol.py --docs .`.
- Validator tests cover valid/invalid records, stale subjects/evidence, containment, malformed input, expired exceptions and non-pass outcomes.
- Standard-library Python only. Unsafe educational examples stay isolated from normal paths.
- Structural validation does not establish truth of evidence, approval, or production readiness.
