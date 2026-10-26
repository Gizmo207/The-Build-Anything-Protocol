import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / ".test-tmp"
TEST_TEMP.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location("check_protocol", ROOT / "tools/check_protocol.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
SUBJECT = "a" * 40
PIN = "b" * 40
NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)


def valid_record(base):
    (base / "output.txt").write_text("Synthetic unit-test fixture; not project execution evidence.\n")
    digest = hashlib.sha256((base / "output.txt").read_bytes()).hexdigest()
    return {
        "schema_version": 1,
        "protocol": {"version": checker.VERSION, "source_revision": PIN},
        "subject": SUBJECT,
        "project": {"name": "Fixture", "scope": "Unit-test the checker",
                    "outcome": "Reject invalid records", "users": "Maintainer",
                    "non_goals": "Deployment", "constraints": "Local only",
                    "authority": "Unit-test scope", "owner": "Test author", "risk": "low",
                    "risk_reason": "Synthetic temporary files only", "instructions": "AGENTS.md"},
        "profiles": {p: {"status": "applicable" if p == "artifact" else "not_applicable",
                         "reason": "Local unit-test artifact" if p == "artifact" else "No such surface"}
                     for p in checker.PROFILES},
        "requirements": [{"id": "AC-1", "acceptance": "Known invalid fixture is rejected", "checks": ["T-1"]}],
        "risks": {r: {"status": "applicable" if r == "rollback" else "not_applicable",
                      "reason": "Temporary state recovery" if r == "rollback" else "No such runtime behavior",
                      "checks": ["T-1"] if r == "rollback" else []} for r in checker.CONCERNS},
        "checks": [{"id": "T-1", "required": True, "enabled": True,
                    "command": "synthetic unit-test fixture", "environment": "Python unittest fixture",
                    "recorded_at": "2020-01-01T00:00:00Z", "result": "passed", "exit_code": 0,
                    "subject": SUBJECT, "protocol_revision": PIN, "artifact": "output.txt", "sha256": digest}],
        "gates": {g: {"status": "passed", "evidence": "Synthetic fixture only"} for g in checker.GATES},
        "exceptions": [],
        "release": {"mode": "local_review", "destination": "Temporary fixture", "owner": "Test author",
                    "authorization": "Unit-test scope", "artifact": "Synthetic fixture",
                    "configuration": "Local Python", "reviewer": "Unit test, not human approval",
                    "stop_criteria": "Any unexpected pass", "observation_window": "Test duration",
                    "rollback": "Delete temporary fixture", "observability": "Unit-test assertions"}
    }


def apply_fixture(record, fixture):
    for path, value in fixture.get("set", []):
        node = record
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
    for path in fixture.get("remove", []):
        node = record
        for key in path[:-1]:
            node = node[key]
        del node[path[-1]]


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.record = valid_record(self.base)

    def validate(self, record=None, ready=True):
        return checker.validate_record(self.record if record is None else record, self.base,
                                       ready, SUBJECT, PIN, NOW)

    def test_valid_revision_bound_record(self):
        self.assertEqual(self.validate(), [])

    def test_negative_fixtures_are_rejected(self):
        fixtures = sorted((ROOT / "tests/fixtures").glob("*.json"))
        self.assertGreaterEqual(len(fixtures), 10)
        for path in fixtures:
            with self.subTest(fixture=path.name):
                record = copy.deepcopy(self.record)
                apply_fixture(record, json.loads(path.read_text()))
                for exception in record["exceptions"]:
                    exception["approval_sha256"] = record["checks"][0]["sha256"]
                self.assertTrue(self.validate(record), path.name)

    def test_all_nonpass_required_outcomes_rejected(self):
        for result in ("failed", "blocked", "not_run", "skipped", "cancelled"):
            with self.subTest(result=result):
                self.record["checks"][0].update(result=result, exit_code=1 if result == "failed" else None)
                self.assertTrue(self.validate())

    def test_disabled_required_check_rejected(self):
        self.record["checks"][0]["enabled"] = False
        self.assertTrue(self.validate())

    def test_stale_evidence_bytes_rejected(self):
        (self.base / "output.txt").write_text("Changed after test")
        self.assertTrue(any("hash mismatch" in e for e in self.validate()))

    def test_absolute_and_parent_escape_rejected(self):
        for path in ("../outside.txt", str(self.base / "output.txt")):
            with self.subTest(path=path):
                self.record["checks"][0]["artifact"] = path
                self.assertTrue(self.validate())

    def test_containment_after_alias_resolution(self):
        # Exercise resolved-path containment without requiring Windows symlink privileges.
        from unittest.mock import patch
        original = Path.resolve
        escaped = self.base.parent / "outside.txt"
        with patch.object(Path, "resolve", lambda p: escaped if p.name == "alias.txt" else original(p)):
            with self.assertRaises(ValueError):
                checker.contained_file(self.base, "alias.txt")

    def test_malformed_nested_values_report_errors_without_crash(self):
        for field, value in (("checks", [None, {"id": []}]), ("requirements", [None]),
                             ("risks", []), ("profiles", None), ("gates", [True]),
                             ("exceptions", [None]), ("release", None)):
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record[field] = value
                self.assertTrue(self.validate(record))
        self.assertTrue(self.validate([]))

    def test_wrong_expected_candidate_or_protocol_rejected(self):
        self.assertTrue(checker.validate_record(self.record, self.base, True, "c"*40, PIN, NOW))
        self.assertTrue(checker.validate_record(self.record, self.base, True, SUBJECT, "c"*40, NOW))

    def test_full_artifact_digest_supported(self):
        digest = "sha256:" + "c"*64
        self.record["subject"] = digest
        self.record["checks"][0]["subject"] = digest
        self.assertEqual(checker.validate_record(self.record, self.base, True, digest, PIN, NOW), [])

    def test_unknown_or_duplicate_check_and_requirement_ids(self):
        self.record["requirements"][0]["checks"] = ["unknown"]
        self.assertTrue(self.validate())
        self.record["requirements"][0]["checks"] = ["T-1"]
        self.record["checks"].append(copy.deepcopy(self.record["checks"][0]))
        self.record["requirements"].append(copy.deepcopy(self.record["requirements"][0]))
        self.assertTrue(self.validate())

    def test_readiness_needs_every_gate_and_no_unresolved_risk(self):
        self.record["gates"]["verify"]["status"] = "blocked"
        self.record["risks"]["failover"]["status"] = "unresolved"
        self.assertTrue(self.validate())
        # Structure-only is deliberately not a readiness claim.
        self.assertEqual(self.validate(ready=False), [])

    def test_future_and_naive_timestamps_rejected(self):
        for stamp in ("2099-01-01T00:00:00Z", "2020-01-01T00:00:00", "invalid"):
            self.record["checks"][0]["recorded_at"] = stamp
            self.assertTrue(self.validate())

    def test_pass_cannot_have_nonzero_exit_or_boolean_exit(self):
        for code in (1, None, False):
            self.record["checks"][0]["exit_code"] = code
            self.assertTrue(self.validate())

    def test_nonwaivable_and_unauthorized_exceptions_rejected(self):
        exception = {"control": "truthful_evidence", "scope": "Fixture", "reason": "Test only",
                     "owner": "Test owner", "approved_by": "self", "approver_type": "agent",
                     "mitigation": "None in test fixture", "followup": "Reject this",
                     "expires": "2099-01-01T00:00:00Z", "approval_artifact": "output.txt",
                     "approval_sha256": self.record["checks"][0]["sha256"]}
        self.record["exceptions"] = [exception]
        self.assertTrue(self.validate())
        exception.update(control="optional_review_format", approved_by="Human fixture approver",
                         approver_type="human")
        self.assertEqual(self.validate(), [])  # structural claim, authenticity needs human review
        exception["expires"] = "2020-01-01T00:00:00Z"
        self.assertTrue(any("expired" in error for error in self.validate()))

    def test_cli_accepts_actual_fixture_and_rejects_malformed_json(self):
        path = self.base / "record.json"
        path.write_text(json.dumps(self.record))
        args = [sys.executable, str(ROOT / "tools/check_protocol.py"), "--record", str(path),
                "--ready", "--revision", SUBJECT, "--protocol-revision", PIN]
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        path.write_text("{invalid")
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)

    def test_cli_ready_requires_explicit_protocol_pin(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_protocol.py"), "--record", "unused",
             "--ready", "--revision", SUBJECT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)

    def test_markdown_links_detect_missing_targets(self):
        (self.base / "README.md").write_text("[missing](missing.md)")
        self.assertTrue(checker.check_docs(self.base))
        (self.base / "missing.md").write_text("[web](https://example.com) [self](#anchor)")
        self.assertEqual(checker.check_docs(self.base), [])

    def test_version_in_code_matches_version_document(self):
        self.assertIn(checker.VERSION, (ROOT / "PROTOCOL_VERSION.md").read_text())
