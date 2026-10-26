# Adoption and enforcement

1. Read [the core](CORE.md) and [profile selector](profiles/README.md); inspect actual project state and existing rules.
2. Vendor a reviewed snapshot or use an available pinned checkout. Record version and full source commit/digest; never release against an unpinned moving branch.
3. Merge [entrypoint instructions](templates/AGENTS.md) into existing instructions without overwriting stronger rules. Human developers follow the same gates.
4. Record the change. Low-risk work may use the concise [checkpoint](templates/checkpoint.md), including grouped exclusions; use [the JSON manifest](templates/protocol-record.json) for machine validation or when the project requires it. Independently released work needs its own subject/evidence.
5. Use [checkpoints](templates/checkpoint.md) at major phase boundaries. Existing projects record baseline/gaps without retrospective passes.
6. Run [validation](tools/README.md), inspect actual evidence/artifacts, and complete [review](templates/pull_request_template.md).
7. Add commands to existing CI only through the normal reviewed process. Preserve checks/protections; changing required checks is a separately authorized owner action.

## Commands

Python 3.10+, standard library only, from this protocol checkout:

```text
python -m unittest discover -s tests -v
python tools/check_protocol.py --docs .
python tools/check_protocol.py --record /path/to/project/protocol-record.json
python tools/check_protocol.py --record /path/to/project/protocol-record.json --ready --revision FULL_CANDIDATE_COMMIT --protocol-revision FULL_PROTOCOL_COMMIT
python examples/reference/taskboard.py --help
```

Windows paths work with the same commands. Evidence paths resolve relative to the record. Readiness needs an explicit full Git SHA or `sha256:` plus 64 hex digits for an artifact.

Keep attestations separate from their subject to avoid self-reference: commit/build a candidate, verify it, then write the record referring to it. An attestation-only commit may follow; identify both revisions and verify no subject files changed. Source/build/configuration changes require a new candidate and affected checks. Resolve the intended subject explicitly in CI; a similarly named branch is insufficient.

## What enforcement does and does not establish

The checker validates shape, traceability, candidate IDs, readiness states, exception dates, and evidence bytes. It never executes recorded commands or establishes that an approval is authentic. Reviewers inspect evidence quality, source coverage, profile compliance, exception authority, and candidate/build correspondence. A fabricated JSON pass remains false evidence.

Run real project build/tests/security checks alongside record validation. Retain redacted logs as durable artifacts. A check may be required by the adopted policy or readiness record; the manifest's `required` flag expresses that obligation. Claim enforcement on a target merge/release path only after verifying that the destination actually enforces the check.

## Existing application assessment

Before integration, read-only assess the real application against the selected core/profiles at an exact revision. Report observed behavior, evidence, gaps, missing access, and suggested changes. Implementation needs its own scope. This protocol change does not itself adopt v2 in another application.
