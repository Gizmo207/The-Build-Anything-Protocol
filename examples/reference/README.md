# Finished local reference: taskboard CLI

This small runnable project completes tasks in a local SQLite file. It demonstrates scoped requirements, an authoritative permission boundary, atomic/idempotent mutation, failure recovery, tests and exact-version evidence. It is a local educational artifact, not a deployed multi-user service or a production security claim.

Python 3.10+ with standard-library SQLite is enough. From a clean checkout:

```text
python examples/reference/taskboard.py --db demo.db init --workspace home --owner alice
python examples/reference/taskboard.py --db demo.db add --workspace home --actor alice --title "Review protocol"
python examples/reference/taskboard.py --db demo.db complete --actor alice --id 1 --request first
python examples/reference/taskboard.py --db demo.db complete --actor alice --id 1 --request first
python examples/reference/taskboard.py --db demo.db list --workspace home --actor alice
python -m unittest discover -s tests -v
```

The first completion returns `replayed: false`; the retry returns `true`. Listing shows `done: 1` and `completion_events: 1`. Choose a new database filename for a fresh run. The file is ignored by Git.

A denied direct call returns exit 1 and no task mutation:

```text
python examples/reference/taskboard.py --db demo.db complete --actor bob --id 1 --request denied
```

The CLI's `--actor` models an already established caller identity. Anyone with filesystem access to the database is the local administrator and can alter it; this example has no remote authentication. A service must verify identity before supplying the actor and protect its database. The explicit local `init` and `revoke` commands are administrator setup, not remote endpoints. No UI is shipped; the UI-only check below is a test model.

## Requirements and boundaries

| ID | Acceptance | Evidence |
| --- | --- | --- |
| AC-R1 | Caller outside task workspace is denied and stored task is unchanged | Direct cross-workspace test |
| AC-R2 | Duplicate/concurrent retries produce one stored completion event | Retry and two-worker tests |
| AC-R3 | Reusing a request key for another task fails without mutation | Conflict test |
| AC-R4 | Membership revocation blocks an old valid receipt replay | Revocation test |
| AC-R5 | Failure between task update and receipt rolls back both; retry succeeds | Injected transaction-failure test |
| AC-R6 | CLI supports create/add/complete/list and recovers from a denied attempt | Subprocess end-to-end test |
| AC-R7 | Missing/stale/failed/unauthorized evidence cannot pass readiness | Checker suite and negative fixtures |

The pure policy owner is `membership_decision`; `Taskboard.authorize` gathers current membership evidence and invokes it. The mutation owner is `Taskboard.complete`. A single SQLite transaction locks before reading permissions and mutating state, uses parameterized queries, records request identity, and rolls back on error. A new idempotency key cannot increment completion a second time. Live authorization precedes replay lookup. Each `add` intentionally creates a new task; its semantics differ from retry-safe completion. No distributed lock/service is needed.

## Bad versus good: UI-only validation

Deliberately unsafe code exists only in [tests/educational_unsafe.py](../../tests/educational_unsafe.py); the CLI never imports it.

```python
# BAD: hiding a UI action cannot protect this directly callable mutation.
def unsafe_complete(board, actor, task_id):
    with board.connection() as db:
        db.execute("UPDATE tasks SET done=1, completion_events=completion_events+1 WHERE id=?",
                   (task_id,))  # ignores actor
```

A UI wrapper can reject Bob, yet a direct call to this function still mutates Alice's task. The test proves the stored unauthorized event exists. The actual good path in [taskboard.py](taskboard.py) checks the stored task workspace and current membership inside the mutation transaction:

```python
db.execute("BEGIN IMMEDIATE")
task = db.execute("SELECT workspace FROM tasks WHERE id=?", (task_id,)).fetchone()
if task is None:
    raise Denied("task unavailable")
self.authorize(db, actor, task[0])
```

The corresponding good-path test calls the boundary directly and proves both done and event count remain zero after denial.

## Bad versus good: retries and partial failure

The unsafe specimen ignores request identity and increments the event count on every retry. Its test demonstrates two stored events for the same request. The actual good path binds the key to actor/task, rejects conflicting reuse, performs the state change only when incomplete, and stores a receipt atomically:

```python
db.execute("UPDATE tasks SET done=1, completion_events=completion_events+1 WHERE id=? AND done=0",
           (task_id,))
self.record_receipt(db, actor, request_id, task_id)
```

Tests verify duplicate/concurrent calls result in one event, a failure before receipt creation rolls back the state, and a later retry recovers. Fault injection exists in the test via monkeypatching; production code has no injected-failure switch.

## Bad versus good: evidence

A JSON string saying passed is not a test run. The checker tests construct clearly synthetic fixtures to verify validation behavior: matching subject/protocol/output succeeds; wrong revision, changed bytes, missing evidence, non-pass/disabled checks and expired/unauthorized exceptions fail. Those fixtures do not claim project verification.

For a real adoption record, resolve the candidate with `git rev-parse HEAD`, execute checks, retain their actual output plus command/environment/UTC/exit result, hash those output files, and fill the [manifest](../../templates/protocol-record.json). Validate with the two explicit revisions shown in [ADOPTION.md](../../ADOPTION.md). Keep evidence outside the subject commit to avoid self-reference. Changed source requires a new candidate and affected checks.

## Release, recovery, and limits

Scope is local review with no deployment, billing, real customer data, or network service. Medium-risk controls are demonstrated because this example mutates durable state. Applicable profiles/modules: automation, artifact, backend, identity and data. Other profiles are excluded because there is no browser/mobile UI, payment, integration or deployed service.

Rollback for a failed completion is a transaction rollback; tests verify it. Before replacing a real database file, its owner needs a separate backup/restore plan. Deleting a demo file is not an application/data-recovery strategy for production. Observe exit codes and list stored state after each example operation. The local file owner handles errors and can retain a prior file/code version.

Not established: remote authentication, multi-host SQLite access, load capacity, backup/restore objectives, crash/power-loss guarantees, mobile/web accessibility, or production operations. No application integration is authorized by this example.
