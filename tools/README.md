# Protocol evidence checker

Python 3.10+ and its standard library are sufficient. No network, services or packages are required. Run from the protocol checkout:

```text
python -m unittest discover -s tests -v
python tools/check_protocol.py --docs .
python tools/check_protocol.py --record /path/to/record.json
python tools/check_protocol.py --record /path/to/record.json --ready --revision FULL_CANDIDATE_SHA --protocol-revision FULL_PROTOCOL_SHA
```

Exit 0 means the requested hygiene checks passed; 1 means validation errors; argparse usage errors return 2. `--docs` checks local inline Markdown file targets. It ignores anchors, remote availability and intentionally historical files under examples/apinow. It is not a full Markdown renderer/linter.

## Record contract

Start with [the JSON template](../templates/protocol-record.json). Placeholders intentionally fail validation.

| Field | Meaning |
| --- | --- |
| schema_version | Record format, currently 1 |
| protocol | Exact supported version and immutable source revision |
| subject | Full 40/64 hex Git SHA, or sha256: plus 64 hex digits for an artifact |
| project | Outcome/users/scope/non-goals/constraints/authority/owner, risk and entrypoint |
| profiles | Every platform/risk-module name, applicability and reason |
| requirements | Unique ID, measurable acceptance, nonempty check IDs; include safety invariants |
| risks | All eight reliability concerns plus security/privacy/accessibility, disposition/reason/checks |
| checks | Unique ID, required/enabled flags, command/procedure, environment, UTC timestamp, result, exit outcome, subject/protocol pin, output file and SHA-256 |
| gates | All six gates, state and factual evidence/limitation |
| exceptions | Control/scope/reason/owner/human approver, approval artifact/digest, mitigation, UTC expiry and follow-up |
| release | Local-review or release mode, artifact/configuration, destination/authority/owner/reviewer, stop criteria, observation interval and recovery |

Results are `passed`, `failed`, `blocked`, `not_run`, `skipped`, or `cancelled`. A manual check uses a named procedure, recorded observations, and exit outcome 0 for satisfied or nonzero for unsatisfied; do not invent a shell invocation. Uncompleted checks use null exit outcome. Passed/failed checks require an existing output file with matching SHA-256 even in structure mode.

Structure mode allows unresolved/not-started work while checking its representation. Readiness additionally requires explicit candidate/protocol IDs matching the record, all gates passed, no unresolved profile/risk, required checks enabled/passed, and acceptance/applicable-risk links to required enabled passing checks. Expired/agent-self-approved/non-waivable exceptions fail validation. A failed required check cannot be bypassed with an exception.

Evidence paths are relative to the record directory and must resolve within it, including after aliases/symlinks. Put records with retained redacted output in a dedicated directory. SHA-256 detects changed bytes relative to the declared digest; it does not authenticate who produced them.

## Trust and enforcement limits

This tool does not run recorded commands, inspect Git/build correspondence, verify signatures/approval authority, check every profile rule, or prove commands passed without skipped internal tests. Review actual logs, material omissions and authority. A local owner who controls records and evidence can forge both. A pin comparison prevents accidental stale/unrelated references; it cannot certify malicious claims.

Distinguish:
- **Documented:** requirements and workflow exist.
- **Locally demonstrated:** commands ran against an identified candidate with retained outputs.
- **Enforced on target merge/release path:** the destination actually requires independently generated checks and protected review. This repository supplies no such branch-protection setup and makes no active-enforcement claim.

For shared releases, use independently generated CI evidence and existing protected workflows as appropriate. Supplying a workflow or this checker does not prove required checks are active. Changes to branch protections/rulesets/access require separate authorization.

## Executable examples

[The local taskboard](../examples/reference/README.md) and [tests](../tests/test_protocol.py) demonstrate good/bad behavior. [Negative fixtures](../tests/fixtures/README.md) are deliberate invalid mutations; their surrounding tests pass when rejected. Tests create scratch files inside ignored .test-tmp and clean their own temporary directories.
