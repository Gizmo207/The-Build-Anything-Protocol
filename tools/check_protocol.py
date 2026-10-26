#!/usr/bin/env python3
"""Validate evidence hygiene, not correctness or approval authenticity. No execution/network."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

VERSION = "2.0.0-draft.1"
PROFILES = ("web", "mobile", "backend", "automation", "artifact",
            "identity", "data", "payments", "integration", "operations")
CONCERNS = ("deadlocks", "resource_leaks", "n_plus_one", "distributed_locks",
            "eventual_consistency", "failover", "load_balancing", "rollback",
            "security", "privacy", "accessibility")
GATES = ("scope", "design", "build", "verify", "deliver", "operate")
RESULTS = ("passed", "failed", "blocked", "not_run", "skipped", "cancelled")
NON_WAIVABLE = ("truthful_evidence", "authority", "secrets", "default_deny",
                "safety_boundaries")


def revision(value):
    return isinstance(value, str) and bool(re.fullmatch(
        r"(?:[0-9a-f]{40}|[0-9a-f]{64}|sha256:[0-9a-f]{64})", value))


def utc(value):
    if not isinstance(value, str):
        return None
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return stamp if stamp.utcoffset() is not None and stamp.utcoffset().total_seconds() == 0 else None
    except ValueError:
        return None


def contained_file(base, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing path")
    candidate = (base / value).resolve()
    if Path(value).is_absolute() or not candidate.is_relative_to(base.resolve()):
        raise ValueError("path must stay inside the record directory")
    if not candidate.is_file():
        raise ValueError("file is missing")
    return candidate


def validate_record(data, base, ready=False, expected=None, protocol_expected=None, now=None):
    """Return all useful errors, including malformed nested input; never run commands."""
    errors = []
    now = now or datetime.now(timezone.utc)

    def obj(value, label):
        if not isinstance(value, dict):
            errors.append(f"{label}: expected object")
            return {}
        return value

    def array(value, label):
        if not isinstance(value, list):
            errors.append(f"{label}: expected array")
            return []
        return value

    def text(value, label):
        if not isinstance(value, str) or not value.strip() or "REPLACE" in value:
            errors.append(f"{label}: required non-placeholder text")

    def evidence(item, path_key, hash_key, label):
        try:
            path = contained_file(base, item.get(path_key))
            digest = item.get(hash_key)
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ValueError("expected SHA-256")
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError("evidence hash mismatch (stale or changed bytes)")
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append(f"{label}: {exc}")

    data = obj(data, "record")
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    protocol = obj(data.get("protocol"), "protocol")
    if protocol.get("version") != VERSION:
        errors.append(f"protocol.version: expected {VERSION}")
    pin = protocol.get("source_revision")
    if not revision(pin):
        errors.append("protocol.source_revision: immutable revision required")
    subject = data.get("subject")
    if not revision(subject):
        errors.append("subject: full Git SHA or sha256 digest required")
    if ready:
        if not revision(expected) or subject != expected:
            errors.append("subject: does not match explicit --revision")
        if not revision(protocol_expected) or pin != protocol_expected:
            errors.append("protocol.source_revision: does not match --protocol-revision")

    project = obj(data.get("project"), "project")
    for key in ("name", "scope", "outcome", "users", "non_goals", "constraints",
                "authority", "owner", "risk_reason", "instructions"):
        text(project.get(key), f"project.{key}")
    if project.get("risk") not in ("low", "medium", "high"):
        errors.append("project.risk: low, medium or high required")

    profiles = obj(data.get("profiles"), "profiles")
    for name in PROFILES:
        item = obj(profiles.get(name), f"profile {name}")
        if item.get("status") not in ("applicable", "not_applicable", "unresolved"):
            errors.append(f"profile {name}: invalid status")
        text(item.get("reason"), f"profile {name}.reason")
        if ready and item.get("status") == "unresolved":
            errors.append(f"profile {name}: unresolved applicability")

    check_items = array(data.get("checks"), "checks")
    checks = {}
    for index, raw in enumerate(check_items):
        c = obj(raw, f"checks[{index}]")
        cid = c.get("id")
        text(cid, f"checks[{index}].id")
        if not isinstance(cid, str):
            continue
        if cid in checks:
            errors.append(f"check {cid}: duplicate id")
        checks[cid] = c
        for key in ("command", "environment"):
            text(c.get(key), f"check {cid}.{key}")
        for key in ("required", "enabled"):
            if type(c.get(key)) is not bool:
                errors.append(f"check {cid}.{key}: expected boolean")
        result = c.get("result")
        if result not in RESULTS:
            errors.append(f"check {cid}: invalid result")
        if c.get("subject") != subject or c.get("protocol_revision") != pin:
            errors.append(f"check {cid}: stale subject or protocol revision")
        stamp = utc(c.get("recorded_at"))
        if stamp is None or stamp > now:
            errors.append(f"check {cid}: invalid/future UTC timestamp")
        exit_code = c.get("exit_code")
        if result == "passed" and (type(exit_code) is not int or exit_code != 0):
            errors.append(f"check {cid}: pass requires exit_code 0")
        if result == "failed" and (type(exit_code) is not int or exit_code == 0):
            errors.append(f"check {cid}: failed requires nonzero exit_code")
        if result in ("blocked", "not_run", "skipped", "cancelled") and exit_code is not None:
            errors.append(f"check {cid}: uncompleted check requires null exit_code")
        if ready and c.get("required") and (not c.get("enabled") or result != "passed"):
            errors.append(f"check {cid}: required check disabled or not passed")
        if result in ("passed", "failed"):
            evidence(c, "artifact", "sha256", f"check {cid}")

    def references(value, label, required):
        ids = array(value, label)
        if required and not ids:
            errors.append(f"{label}: at least one check required")
        for cid in ids:
            if not isinstance(cid, str) or cid not in checks:
                errors.append(f"{label}: unknown check {cid!r}")
            elif ready and (not checks[cid].get("required") or not checks[cid].get("enabled")
                            or checks[cid].get("result") != "passed"):
                errors.append(f"{label}: acceptance/risk needs required enabled passing check")

    reqs = array(data.get("requirements"), "requirements")
    if not reqs:
        errors.append("requirements: at least one required")
    seen = set()
    for index, raw in enumerate(reqs):
        req = obj(raw, f"requirements[{index}]")
        rid = req.get("id")
        text(rid, f"requirements[{index}].id")
        if isinstance(rid, str):
            if rid in seen:
                errors.append(f"requirement {rid}: duplicate id")
            seen.add(rid)
        text(req.get("acceptance"), f"requirement {rid}.acceptance")
        references(req.get("checks"), f"requirement {rid}.checks", True)

    risks = obj(data.get("risks"), "risks")
    for name in CONCERNS:
        risk = obj(risks.get(name), f"risk {name}")
        status = risk.get("status")
        if status not in ("applicable", "not_applicable", "unresolved"):
            errors.append(f"risk {name}: invalid status")
        text(risk.get("reason"), f"risk {name}.reason")
        references(risk.get("checks"), f"risk {name}.checks", status == "applicable")
        if ready and status == "unresolved":
            errors.append(f"risk {name}: unresolved")
    gates = obj(data.get("gates"), "gates")
    for name in GATES:
        gate = obj(gates.get(name), f"gate {name}")
        if gate.get("status") not in ("passed", "failed", "blocked", "not_started"):
            errors.append(f"gate {name}: invalid status")
        text(gate.get("evidence"), f"gate {name}.evidence")
        if ready and gate.get("status") != "passed":
            errors.append(f"gate {name}: not passed")

    for index, raw in enumerate(array(data.get("exceptions"), "exceptions")):
        e = obj(raw, f"exceptions[{index}]")
        for key in ("control", "scope", "reason", "owner", "approved_by",
                    "mitigation", "followup"):
            text(e.get(key), f"exception {index}.{key}")
        if e.get("control") in NON_WAIVABLE:
            errors.append(f"exception {index}: control is non-waivable")
        if e.get("approver_type") != "human" or e.get("approved_by") == "self":
            errors.append(f"exception {index}: authorized human approver required")
        expiry = utc(e.get("expires"))
        if expiry is None or expiry <= now:
            errors.append(f"exception {index}: expired or invalid expiry")
        evidence(e, "approval_artifact", "approval_sha256", f"exception {index} approval")

    release = obj(data.get("release"), "release")
    if release.get("mode") not in ("local_review", "release"):
        errors.append("release.mode: local_review or release required")
    for key in ("destination", "owner", "authorization", "artifact", "configuration",
                "reviewer", "stop_criteria", "observation_window", "rollback", "observability"):
        text(release.get(key), f"release.{key}")
    return errors


def check_docs(root):
    """Check local Markdown link targets, excluding intentionally historical examples."""
    errors = []
    root = root.resolve()
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(p in (".git", "__pycache__", ".test-tmp") for p in relative.parts):
            continue
        if relative.parts[:2] == ("examples", "apinow"):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8-sig")):
            target = target.strip("<>")
            parts = urlsplit(target)
            if parts.scheme or target.startswith("#"):
                continue
            local = (path.parent / unquote(parts.path)).resolve()
            if not local.is_relative_to(root) or not local.exists():
                errors.append(f"{relative}: missing/outside local link {target}")
    return errors


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record", type=Path)
    p.add_argument("--docs", type=Path)
    p.add_argument("--ready", action="store_true")
    p.add_argument("--revision")
    p.add_argument("--protocol-revision")
    args = p.parse_args(argv)
    if not args.record and not args.docs:
        p.error("provide --record or --docs")
    if args.ready and (not args.record or not args.revision or not args.protocol_revision):
        p.error("--ready requires --record, --revision and --protocol-revision")
    errors = []
    if args.docs:
        if not args.docs.is_dir():
            errors.append("docs: directory missing")
        else:
            errors.extend(check_docs(args.docs))
    if args.record:
        try:
            data = json.loads(args.record.read_text(encoding="utf-8-sig"))
            errors.extend(validate_record(data, args.record.parent, args.ready,
                                          args.revision, args.protocol_revision))
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append(f"record: {exc}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print("PASS: evidence hygiene / local links only; review evidence quality and authority separately.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
