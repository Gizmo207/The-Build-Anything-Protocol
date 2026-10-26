import concurrent.futures
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / ".test-tmp"
TEST_TEMP.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "examples" / "reference"))
from taskboard import Conflict, Denied, Taskboard, membership_decision
from educational_unsafe import ui_complete, unsafe_complete, unsafe_retry


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "tasks.db"
        self.board = Taskboard(self.path)
        self.board.create_workspace("alpha", "alice")
        self.board.create_workspace("beta", "bob")
        self.task = self.board.add("alice", "alpha", "Ship the artifact")

    def state(self):
        return self.board.list_tasks("alice", "alpha")[0]

    def test_pure_policy_defaults_to_deny_for_missing_or_invalid_evidence(self):
        self.assertTrue(membership_decision(True))
        for evidence in (False, None, "yes", 1):
            self.assertFalse(membership_decision(evidence))

    def test_bad_ui_only_validation_can_be_bypassed(self):
        with self.assertRaises(Denied):
            ui_complete(self.board, "bob", self.task)
        unsafe_complete(self.board, "bob", self.task)
        self.assertEqual(self.state()["completion_events"], 1)  # demonstrates the bug

    def test_good_boundary_denies_direct_cross_workspace_call_without_mutation(self):
        with self.assertRaises(Denied):
            self.board.complete("bob", self.task, "request-1")
        self.assertEqual(self.state()["done"], 0)
        self.assertEqual(self.state()["completion_events"], 0)

    def test_bad_retry_duplicates_durable_events(self):
        for _ in range(2):
            unsafe_retry(self.board, "alice", self.task, "same-request")
        self.assertEqual(self.state()["completion_events"], 2)  # demonstrates the bug

    def test_good_retry_and_repeated_action_change_state_once(self):
        first = self.board.complete("alice", self.task, "same")
        second = self.board.complete("alice", self.task, "same")
        self.board.complete("alice", self.task, "new-request")
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(self.state()["completion_events"], 1)

    def test_same_request_cannot_apply_to_another_task(self):
        other = self.board.add("alice", "alpha", "Other")
        self.board.complete("alice", self.task, "same")
        with self.assertRaises(Conflict):
            self.board.complete("alice", other, "same")
        self.assertEqual(self.board.list_tasks("alice", "alpha")[1]["done"], 0)

    def test_revocation_denies_even_a_previously_valid_replay(self):
        self.board.complete("alice", self.task, "same")
        self.board.revoke("alpha", "alice")
        with self.assertRaises(Denied):
            self.board.complete("alice", self.task, "same")
        with self.board.connection() as db:
            self.assertEqual(db.execute("SELECT completion_events FROM tasks").fetchone()[0], 1)

    def test_partial_failure_rolls_back_and_retry_recovers(self):
        with patch.object(Taskboard, "record_receipt", side_effect=sqlite3.OperationalError("injected test failure")):
            with self.assertRaises(sqlite3.OperationalError):
                self.board.complete("alice", self.task, "same")
        self.assertEqual(self.state()["done"], 0)
        with self.board.connection() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM receipts").fetchone()[0], 0)
        self.board.complete("alice", self.task, "same")
        self.assertEqual(self.state()["completion_events"], 1)

    def test_two_workers_replay_atomically(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as workers:
            results = list(workers.map(
                lambda _: Taskboard(self.path).complete("alice", self.task, "same"), range(2)))
        self.assertEqual(sum(r["replayed"] for r in results), 1)
        self.assertEqual(self.state()["completion_events"], 1)

    def test_query_parameterization_preserves_data(self):
        title = "x'); DROP TABLE tasks; --"
        self.board.add("alice", "alpha", title)
        self.assertEqual(self.board.list_tasks("alice", "alpha")[1]["title"], title)

    def test_cli_end_to_end_failure_then_recovery(self):
        def run(*args, expected=0):
            result = subprocess.run(
                [sys.executable, str(ROOT / "examples/reference/taskboard.py"),
                 "--db", str(self.path), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stderr)
            return json.loads(result.stdout if expected == 0 else result.stderr)
        denied = run("complete", "--actor", "bob", "--id", str(self.task), "--request", "cli", expected=1)
        self.assertIn("error", denied)
        result = run("complete", "--actor", "alice", "--id", str(self.task), "--request", "cli")
        self.assertFalse(result["replayed"])
        self.assertTrue(run("complete", "--actor", "alice", "--id", str(self.task),
                            "--request", "cli")["replayed"])
        self.assertEqual(run("list", "--actor", "alice", "--workspace", "alpha")[0]["completion_events"], 1)
