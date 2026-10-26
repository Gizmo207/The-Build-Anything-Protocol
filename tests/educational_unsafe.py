"""DELIBERATELY UNSAFE educational specimens. Imported by tests only, never the CLI."""


def ui_complete(board, actor, task_id):
    # A UI may hide the button, but direct calls to unsafe_complete bypass this.
    with board.connection() as db:
        workspace = db.execute("SELECT workspace FROM tasks WHERE id=?", (task_id,)).fetchone()[0]
        board.authorize(db, actor, workspace)
    unsafe_complete(board, actor, task_id)


def unsafe_complete(board, actor, task_id):
    # BAD: actor is ignored; no authoritative permission check.
    with board.connection() as db:
        db.execute("UPDATE tasks SET done=1, completion_events=completion_events+1 WHERE id=?",
                   (task_id,))


def unsafe_retry(board, actor, task_id, request_id):
    # BAD: ignores duplicate request identity and adds an event on every retry.
    unsafe_complete(board, actor, task_id)
