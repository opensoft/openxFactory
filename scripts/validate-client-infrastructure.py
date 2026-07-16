#!/usr/bin/env python3
"""Validate the client-infrastructure contract family (add-client-infrastructure-liaison).

Change task 2.4. The openxFactory-owned validator for the two kinds
`client_infrastructure_request` and `infrastructure_readiness_result`
(`contracts/schemas/xfactory-client-infrastructure-request.schema.yaml` and
`contracts/schemas/xfactory-infrastructure-readiness-result.schema.yaml`). Run
from the pinned openxFactory checkout, never copied into domain repos:

    python3 scripts/validate-client-infrastructure.py [PATH]

Two layers run:

1. Packaged reference examples (`examples/client-infrastructure/`, task 2.3):
   every `*.example.yaml` must validate against its `kind`'s schema AND pass
   every deterministic check; every file under `negative/` must fail, and the
   validator asserts each fails for its INTENDED reason (the self-test —
   spec scenario "Validator self-test degrades" fails closed if any negative
   stops failing for its reason or any valid example fails).
2. Optional real artifacts under PATH: `*.y*ml` whose `kind` is one of the two
   family kinds are validated (kind-keyed); files with other kinds are skipped
   with notice; instance records live in client installs, so openxFactory
   normally has none and PATH is omitted.

Deterministic checks JSON Schema cannot express (design D4/D6):
  - embedded-secret rejection (value-shaped fields scanned against the shared
    `contracts/avatar-client/redaction/` denylist; only bounded SENTINEL_ forms
    are exempt);
  - transition legality including terminal immutability and readiness-gated
    completion (freshness = valid_until not passed at the transition time,
    status ready, every mandatory check passing);
  - identity-class separation (execution actor never equals the approval
    authority nor the coordinating liaison/creator; a subject identifier never
    appears in an actor, capability, or authority field);
  - idempotency / supersedes integrity (a duplicate idempotency_key must name
    the same open request; supersedes_request_ref only from a terminal
    predecessor);
  - cancellation-acknowledgment presence when a cancelled request carries a
    handoff.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
EXAMPLES_DIR = ROOT / "examples" / "client-infrastructure"
REDACTION_DIR = ROOT / "contracts" / "avatar-client" / "redaction"

REQUEST_SCHEMA = "xfactory-client-infrastructure-request.schema.yaml"
READINESS_SCHEMA = "xfactory-infrastructure-readiness-result.schema.yaml"
KIND_TO_SCHEMA = {
    "client_infrastructure_request": REQUEST_SCHEMA,
    "infrastructure_readiness_result": READINESS_SCHEMA,
}

TERMINAL_STATES = {"completed", "declined", "cancelled"}

# Transition matrix (request-contract-and-transition-matrix fragment): each
# legal linear edge maps to the actor-role class authorized to drive it.
LINEAR_EDGES: dict[tuple[str, str], set[str]] = {
    ("identified", "request_drafted"): {"liaison_owner"},
    ("request_drafted", "awaiting_client_approval"): {"liaison_owner"},
    ("request_drafted", "submitted"): {"liaison_owner"},
    ("awaiting_client_approval", "submitted"): {"approval_authority"},
    ("awaiting_client_approval", "declined"): {"approval_authority"},
    ("submitted", "acknowledged"): {"execution_actor"},
    ("acknowledged", "scheduled"): {"execution_actor"},
    ("scheduled", "implementing"): {"execution_actor"},
    ("implementing", "validation_pending"): {"execution_actor"},
    ("validation_pending", "completed"): {"trusted_validator"},
    ("validation_pending", "validation_failed"): {"trusted_validator"},
    ("validation_failed", "scheduled"): {"execution_actor"},
}


# Intended failure reason (a coded finding) each packaged negative must raise.
NEGATIVE_EXPECTATIONS: dict[str, str] = {
    "embedded-secret-value.yaml": "embedded-secret",
    "subject-id-in-authority-field.yaml": "subject-in-typed-field",
    "actor-equals-authority.yaml": "actor-equals-authority",
    "liaison-marks-completed.yaml": "illegal-transition",
    "completed-without-fresh-readiness.yaml": "completion-without-fresh-readiness",
    "escalation-as-state.yaml": "schema",
    "terminal-mutation.yaml": "terminal-mutation",
    "digestless-package-ref.yaml": "schema",
    "cancellation-with-unacknowledged-children.yaml": "cancellation-unacknowledged-children",
}


class Finding:
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


# --------------------------- loading helpers ---------------------------

def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_schema_validators() -> dict[str, Draft202012Validator]:
    out: dict[str, Draft202012Validator] = {}
    for name in (REQUEST_SCHEMA, READINESS_SCHEMA):
        schema = load_yaml(SCHEMAS_DIR / name)
        Draft202012Validator.check_schema(schema)
        out[name] = Draft202012Validator(schema)
    return out


def load_secret_scan() -> tuple[list[tuple[str, re.Pattern[str]]], set[str]]:
    """Reuse the shared avatar-client redaction denylist + bounded sentinels
    (design D6) rather than re-declaring secret patterns here."""
    patterns: list[tuple[str, re.Pattern[str]]] = []
    allowed: set[str] = set()
    denylist = REDACTION_DIR / "denylist-patterns.yaml"
    sentinels = REDACTION_DIR / "sentinels.yaml"
    if denylist.is_file():
        doc = load_yaml(denylist) or {}
        for entry in doc.get("patterns") or []:
            patterns.append((entry["id"], re.compile(entry["regex"])))
    if sentinels.is_file():
        doc = load_yaml(sentinels) or {}
        for entry in doc.get("sentinels") or []:
            if entry.get("bounded_form"):
                allowed.add(entry["bounded_form"])
    return patterns, allowed


# --------------------------- string walk ---------------------------

def iter_strings(node: Any, path: str = "") -> Any:
    if isinstance(node, dict):
        for k, v in node.items():
            yield from iter_strings(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


# --------------------------- deterministic checks ---------------------------

def check_secret_scan(
    record: dict, patterns: list[tuple[str, re.Pattern[str]]], allowed: set[str],
) -> list[Finding]:
    out: list[Finding] = []
    for loc, value in iter_strings(record):
        if value in allowed:
            continue
        for pid, rx in patterns:
            if rx.search(value):
                out.append(Finding(
                    "embedded-secret",
                    f"{loc}: value matches secret/identifier pattern {pid!r} "
                    f"(references only; use a SENTINEL_ bounded form in fixtures)",
                ))
                break
    return out


def check_identity_separation(record: dict) -> list[Finding]:
    out: list[Finding] = []
    binding = record.get("execution_binding") or {}
    actor = binding.get("actor_ref")
    authority = (record.get("approval") or {}).get("authority_ref")
    created_by = record.get("created_by")
    if actor and authority and actor == authority:
        out.append(Finding(
            "actor-equals-authority",
            f"execution_binding.actor_ref {actor!r} equals approval.authority_ref "
            f"— execution and approval must be separate parties",
        ))
    if actor and created_by and actor == created_by:
        out.append(Finding(
            "liaison-is-executor",
            f"execution_binding.actor_ref {actor!r} equals created_by "
            f"— the coordinating liaison must not be the privileged executor",
        ))
    return out


def check_subject_separation(record: dict) -> list[Finding]:
    subjects = set(record.get("managed_subject_refs") or [])
    if record.get("subject_ref"):
        subjects.add(record["subject_ref"])
    if not subjects:
        return []
    binding = record.get("execution_binding") or {}
    approval = record.get("approval") or {}
    transition = record.get("transition") or {}
    handoff = record.get("handoff") or {}
    typed_fields = {
        "execution_binding.actor_ref": binding.get("actor_ref"),
        "execution_binding.capability_ref": binding.get("capability_ref"),
        "approval.authority_ref": approval.get("authority_ref"),
        "created_by": record.get("created_by"),
        "transition.actor_ref": transition.get("actor_ref"),
        "handoff.accepted_by_actor_ref": handoff.get("accepted_by_actor_ref"),
    }
    out: list[Finding] = []
    for loc, value in typed_fields.items():
        if value is not None and value in subjects:
            out.append(Finding(
                "subject-in-typed-field",
                f"{loc} {value!r} is a declared subject identifier — subjects are "
                f"forbidden in actor, capability, and authority fields",
            ))
    return out


def _transition_legal(from_s: Any, to_s: str, role: str) -> bool:
    if to_s == "blocked":
        return from_s not in TERMINAL_STATES and role in {"current_owner", "policy_gate"}
    if from_s == "blocked":
        return to_s not in TERMINAL_STATES and role in {"current_owner", "policy_gate"}
    if to_s == "cancelled":
        return from_s not in TERMINAL_STATES and role == "requester"
    allowed = LINEAR_EDGES.get((from_s, to_s))
    return allowed is not None and role in allowed


def check_transition(record: dict, readiness_index: list[dict]) -> list[Finding]:
    out: list[Finding] = []
    status = record.get("status")
    transition = record.get("transition")
    gate_needed = status == "completed"

    if isinstance(transition, dict):
        from_s = transition.get("from")
        to_s = transition.get("to")
        role = transition.get("actor_role")
        if from_s in TERMINAL_STATES:
            out.append(Finding(
                "terminal-mutation",
                f"transition leaves terminal state {from_s!r} -> {to_s!r}; terminals are "
                f"immutable (continue only via a new request with supersedes_request_ref)",
            ))
            return out
        if to_s != status:
            out.append(Finding(
                "transition-status-mismatch",
                f"transition.to {to_s!r} does not equal status {status!r}",
            ))
        if not _transition_legal(from_s, to_s, role):
            out.append(Finding(
                "illegal-transition",
                f"transition {from_s!r} -> {to_s!r} is not authorized for actor_role {role!r}",
            ))
            return out  # readiness gate is a guard on a LEGAL completion only
        gate_needed = to_s == "completed"

    if gate_needed:
        out.extend(_check_readiness_gate(record, readiness_index))
    return out


def _check_readiness_gate(record: dict, readiness_index: list[dict]) -> list[Finding]:
    correlation = record.get("correlation_id")
    profile_id = (record.get("validation_profile") or {}).get("id")
    subjects = set(record.get("managed_subject_refs") or [])
    transition = record.get("transition") or {}
    completion_time = transition.get("at") or record.get("created_at")

    for result in readiness_index:
        if result.get("correlation_id") != correlation:
            continue
        if (result.get("profile") or {}).get("id") != profile_id:
            continue
        if result.get("subject_ref") not in subjects:
            continue
        if result.get("status") != "ready":
            continue
        if any(
            c.get("mandatory") and c.get("outcome") != "pass"
            for c in result.get("checks") or []
        ):
            continue
        valid_until = result.get("valid_until")
        if completion_time and valid_until and valid_until < completion_time:
            continue  # stale: valid_until passed before the completion time
        return []  # a fresh passing readiness result gates this completion
    return [Finding(
        "completion-without-fresh-readiness",
        "transition to completed has no fresh passing infrastructure_readiness_result "
        "(matched by correlation_id + validation profile + subject, status ready, all "
        "mandatory checks pass, valid_until not passed at the completion time)",
    )]


def check_cancellation_acks(record: dict) -> list[Finding]:
    if record.get("status") != "cancelled":
        return []
    if not record.get("handoff"):
        return []
    if not (record.get("child_acks") or []):
        return [Finding(
            "cancellation-unacknowledged-children",
            "request is cancelled with an external handoff but records no child_acks "
            "— cancellation must propagate to every external work item / child job "
            "with a recorded acknowledgment",
        )]
    return []


def check_idempotency_supersedes(records: list[tuple[str, dict]]) -> list[Finding]:
    out: list[Finding] = []
    by_key: dict[str, list[tuple[str, dict]]] = {}
    by_id: dict[str, dict] = {}
    for label, rec in records:
        if rec.get("kind") != "client_infrastructure_request":
            continue
        by_key.setdefault(rec.get("idempotency_key"), []).append((label, rec))
        if rec.get("request_id"):
            by_id[rec["request_id"]] = rec
    for key, group in by_key.items():
        if key is None:
            continue
        ids = {rec.get("request_id") for _, rec in group}
        open_group = [rec for _, rec in group if rec.get("status") not in TERMINAL_STATES]
        if len(ids) > 1 and len(open_group) > 1:
            out.append(Finding(
                "idempotency-duplicate",
                f"idempotency_key {key!r} appears on multiple distinct open requests "
                f"{sorted(i for i in ids if i)!r} — a duplicate key must return the same open request",
            ))
    for label, rec in records:
        ref = rec.get("supersedes_request_ref")
        if ref and ref in by_id and by_id[ref].get("status") not in TERMINAL_STATES:
            out.append(Finding(
                "supersedes-nonterminal",
                f"{label}: supersedes_request_ref {ref!r} names a non-terminal predecessor "
                f"(status {by_id[ref].get('status')!r}); supersede only a terminal request",
            ))
    return out


# --------------------------- record validation ---------------------------

def schema_findings(validators: dict[str, Draft202012Validator], record: dict) -> list[Finding]:
    kind = record.get("kind")
    schema_name = KIND_TO_SCHEMA.get(kind)
    if schema_name is None:
        return [Finding("schema", f"unrecognized kind {kind!r}")]
    validator = validators[schema_name]
    out: list[Finding] = []
    for err in sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        out.append(Finding("schema", f"{loc}: {err.message}"))
    return out


def deterministic_findings(
    record: dict,
    patterns: list[tuple[str, re.Pattern[str]]],
    allowed: set[str],
    readiness_index: list[dict],
) -> list[Finding]:
    """Per-record deterministic checks (schema already passed). Cross-record
    checks (idempotency/supersedes) run separately over the whole set."""
    out: list[Finding] = []
    out.extend(check_secret_scan(record, patterns, allowed))
    if record.get("kind") == "client_infrastructure_request":
        out.extend(check_identity_separation(record))
        out.extend(check_subject_separation(record))
        out.extend(check_transition(record, readiness_index))
        out.extend(check_cancellation_acks(record))
    return out


def validate_record(
    validators: dict[str, Draft202012Validator],
    record: Any,
    patterns: list[tuple[str, re.Pattern[str]]],
    allowed: set[str],
    readiness_index: list[dict],
) -> list[Finding]:
    if not isinstance(record, dict):
        return [Finding("schema", "record is not a mapping")]
    schema = schema_findings(validators, record)
    if schema:
        return schema  # skip deterministic checks on a malformed record
    return deterministic_findings(record, patterns, allowed, readiness_index)


# --------------------------- layer 1: self-test ---------------------------

def run_self_test(
    validators: dict[str, Draft202012Validator],
    patterns: list[tuple[str, re.Pattern[str]]],
    allowed: set[str],
) -> list[Finding]:
    out: list[Finding] = []
    if not EXAMPLES_DIR.is_dir():
        return [Finding("examples-missing", f"{EXAMPLES_DIR} not found")]

    # Valid set: co-load every example so the readiness gate and
    # idempotency/supersedes checks see the whole consistent set.
    valid_records: list[tuple[str, dict]] = []
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        doc = load_yaml(path)
        if isinstance(doc, dict):
            valid_records.append((path.name, doc))
    readiness_index = [
        rec for _, rec in valid_records
        if rec.get("kind") == "infrastructure_readiness_result"
    ]
    valid_ok = 0
    for label, rec in valid_records:
        findings = validate_record(validators, rec, patterns, allowed, readiness_index)
        if findings:
            for fnd in findings:
                out.append(Finding("example-invalid", f"{label}: expected valid, got {fnd}"))
        else:
            valid_ok += 1
    for fnd in check_idempotency_supersedes(valid_records):
        out.append(Finding("example-invalid", f"valid set: expected clean, got {fnd}"))

    # Negative set: each file validated in isolation (empty readiness index)
    # must fail, and specifically for its intended reason.
    neg_dir = EXAMPLES_DIR / "negative"
    neg_ok = 0
    if not neg_dir.is_dir():
        out.append(Finding("examples-missing", f"{neg_dir} not found"))
    else:
        for path in sorted(neg_dir.glob("*.yaml")):
            doc = load_yaml(path)
            findings = validate_record(validators, doc, patterns, allowed, readiness_index=[])
            expected = NEGATIVE_EXPECTATIONS.get(path.name)
            if not findings:
                out.append(Finding(
                    "negative-should-fail",
                    f"negative/{path.name}: expected invalid, validated cleanly",
                ))
                continue
            if expected is not None and not any(f.code == expected for f in findings):
                got = sorted({f.code for f in findings})
                out.append(Finding(
                    "negative-wrong-reason",
                    f"negative/{path.name}: expected reason {expected!r}, got {got}",
                ))
                continue
            neg_ok += 1

    print(f"self-test: {valid_ok} valid example(s) confirmed valid, "
          f"{neg_ok} negative example(s) confirmed invalid for their intended reason")
    return out


# --------------------------- layer 2: real artifacts ---------------------------

def run_repo_scan(
    validators: dict[str, Draft202012Validator],
    patterns: list[tuple[str, re.Pattern[str]]],
    allowed: set[str],
    target: Path,
) -> list[Finding]:
    out: list[Finding] = []
    files = sorted(target.rglob("*.y*ml")) if target.is_dir() else [target]
    records: list[tuple[str, dict]] = []
    checked = skipped = 0
    for f in files:
        try:
            doc = load_yaml(f)
        except yaml.YAMLError as exc:
            out.append(Finding("yaml", f"{f}: parse failure: {exc}"))
            continue
        if not isinstance(doc, dict):
            continue
        kind = doc.get("kind")
        if kind not in KIND_TO_SCHEMA:
            print(f"skip  {f}: kind {kind!r} is not a client-infrastructure contract (out of scope)")
            skipped += 1
            continue
        checked += 1
        records.append((str(f), doc))
    readiness_index = [
        rec for _, rec in records if rec.get("kind") == "infrastructure_readiness_result"
    ]
    for label, rec in records:
        for fnd in validate_record(validators, rec, patterns, allowed, readiness_index):
            out.append(Finding(fnd.code, f"{label}: {fnd.message}"))
    out.extend(check_idempotency_supersedes(records))
    print(f"repo scan ({target}): {checked} contract(s) checked, {skipped} skipped")
    return out


# --------------------------- orchestration ---------------------------

def main() -> int:
    if not SCHEMAS_DIR.is_dir():
        print(f"ERROR {SCHEMAS_DIR} not found", file=sys.stderr)
        return 2
    try:
        validators = load_schema_validators()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR schema load failure: {exc}", file=sys.stderr)
        return 2
    patterns, allowed = load_secret_scan()

    findings: list[Finding] = []
    findings.extend(run_self_test(validators, patterns, allowed))

    if len(sys.argv) > 1:
        target = Path(sys.argv[1]).resolve()
        if not target.exists():
            print(f"ERROR path {target} not found", file=sys.stderr)
            return 2
        findings.extend(run_repo_scan(validators, patterns, allowed, target))

    for fnd in findings:
        print(f"ERROR {fnd}")
    verdict = "PASS" if not findings else "FAIL"
    print(f"\nvalidate-client-infrastructure: {len(findings)} finding(s) -> {verdict}")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
