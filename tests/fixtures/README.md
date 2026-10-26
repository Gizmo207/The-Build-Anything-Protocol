# Deliberately invalid record fixtures

Each JSON file describes mutations applied to the valid, explicitly synthetic record built by `valid_record` in [test_protocol.py](../test_protocol.py). They are not project attestations and cannot be submitted as readiness evidence.

The test runner loads every fixture and requires rejection. Cases cover stale subject/protocol/evidence, wrong version, missing evidence, failed/skipped/cancelled/not-run checks, disabled required checks, and expired/unauthorized exceptions. A rejected fixture makes its test pass; no unexplained failing CI is expected.
