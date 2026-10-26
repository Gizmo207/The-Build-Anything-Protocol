#!/usr/bin/env python3
"""Local taskboard reference. Filesystem owner is administrator; no network authentication."""
import argparse
import json
import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path


class Denied(ValueError):
    pass


class Conflict(ValueError):
    pass


def membership_decision(evidence):
    """Pure policy: only explicit positive membership evidence grants access."""
    return evidence is True


class Taskboard:
    def __init__(self, path):
        self.path = str(path)
        with self.connection() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS memberships(
                    workspace TEXT NOT NULL, actor TEXT NOT NULL,
                    PRIMARY KEY(workspace, actor));
                CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY, workspace TEXT NOT NULL,
                    title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0,1)),
                    completion_events INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE IF NOT EXISTS receipts(
                    actor TEXT NOT NULL, request_id TEXT NOT NULL, task_id INTEGER NOT NULL,
                    PRIMARY KEY(actor, request_id), FOREIGN KEY(task_id) REFERENCES tasks(id));
            """)

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.execute("PRAGMA foreign_keys=ON")
        try:
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def authorize(db, actor, workspace):
        evidence = db.execute("SELECT 1 FROM memberships WHERE actor=? AND workspace=?",
                              (actor, workspace)).fetchone()
        if not membership_decision(bool(evidence)):
            raise Denied("actor cannot act in this workspace")

    def create_workspace(self, workspace, owner):
        # Explicit local administrator setup, not an untrusted remote endpoint.
        if not workspace.strip() or not owner.strip():
            raise ValueError("workspace and owner required")
        with self.connection() as db:
            db.execute("INSERT INTO memberships VALUES (?,?)", (workspace, owner))

    def revoke(self, workspace, actor):
        # Filesystem administrator controls this standalone local demonstration.
        with self.connection() as db:
            db.execute("DELETE FROM memberships WHERE workspace=? AND actor=?", (workspace, actor))

    def add(self, actor, workspace, title):
        if not title.strip():
            raise ValueError("title required")
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            self.authorize(db, actor, workspace)
            result = db.execute("INSERT INTO tasks(workspace,title) VALUES (?,?)", (workspace, title))
            return result.lastrowid

    @staticmethod
    def record_receipt(db, actor, request_id, task_id):
        db.execute("INSERT INTO receipts VALUES (?,?,?)", (actor, request_id, task_id))

    def complete(self, actor, task_id, request_id):
        if not request_id or len(request_id) > 128:
            raise ValueError("request_id must contain 1..128 characters")
        with self.connection() as db:
            # Serialize the read/check/write transaction, including current membership.
            db.execute("BEGIN IMMEDIATE")
            task = db.execute("SELECT workspace FROM tasks WHERE id=?", (task_id,)).fetchone()
            if task is None:
                raise Denied("task unavailable")
            self.authorize(db, actor, task[0])  # live check, including receipt replays
            receipt = db.execute("SELECT task_id FROM receipts WHERE actor=? AND request_id=?",
                                 (actor, request_id)).fetchone()
            if receipt:
                if receipt[0] != task_id:
                    raise Conflict("request_id was already used for another task")
                return {"id": task_id, "done": True, "replayed": True}
            db.execute("""UPDATE tasks SET done=1, completion_events=completion_events+1
                          WHERE id=? AND done=0""", (task_id,))
            self.record_receipt(db, actor, request_id, task_id)
            return {"id": task_id, "done": True, "replayed": False}

    def list_tasks(self, actor, workspace):
        with self.connection() as db:
            db.execute("BEGIN")  # consistent read of permission and data
            self.authorize(db, actor, workspace)
            return [dict(zip(("id", "title", "done", "completion_events"), row))
                    for row in db.execute(
                        "SELECT id,title,done,completion_events FROM tasks WHERE workspace=? ORDER BY id",
                        (workspace,))]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", type=Path, required=True)
    commands = p.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="local administrator creates workspace")
    init.add_argument("--workspace", required=True)
    init.add_argument("--owner", required=True)
    add = commands.add_parser("add")
    add.add_argument("--workspace", required=True)
    add.add_argument("--actor", required=True)
    add.add_argument("--title", required=True)
    complete = commands.add_parser("complete")
    complete.add_argument("--actor", required=True)
    complete.add_argument("--id", type=int, required=True)
    complete.add_argument("--request", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--workspace", required=True)
    listing.add_argument("--actor", required=True)
    revoke = commands.add_parser("revoke", help="local administrator revokes membership")
    revoke.add_argument("--workspace", required=True)
    revoke.add_argument("--member", required=True)
    args = p.parse_args(argv)
    try:
        board = Taskboard(args.db)
        if args.command == "init":
            board.create_workspace(args.workspace, args.owner)
            result = {"workspace": args.workspace, "owner": args.owner}
        elif args.command == "add":
            result = {"id": board.add(args.actor, args.workspace, args.title)}
        elif args.command == "complete":
            result = board.complete(args.actor, args.id, args.request)
        elif args.command == "list":
            result = board.list_tasks(args.actor, args.workspace)
        else:
            board.revoke(args.workspace, args.member)
            result = {"revoked": args.member}
        print(json.dumps(result))
        return 0
    except (ValueError, sqlite3.Error, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
