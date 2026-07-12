#!/usr/bin/env python3
"""Validate the neutral avatar-client (AVC) contract kernel.

Reference runner and gate for the contract kernel under
``contracts/avatar-client/``: schema validity + offline ``$ref`` resolution,
closed-registry parity, self-describing fixture conformance, acceptance-map
parity, evidence-register completeness, dual redaction (structural + content
scan with bounded sentinels), per-file digests, and the fail-closed F0
publication gate.

Reproducible reference tooling only — NOT a pinned semantic artifact and NOT a
required consumer dependency (spec FR-020/FR-023). Consumers may execute the
self-describing fixtures with any conformant draft 2020-12 implementation.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""

from __future__ import annotations

import argparse
import hashlib
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
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
AVC = ROOT / "contracts" / "avatar-client"

# The OpenSpec change that owns the authoritative requirement/scenario deltas
# this kernel realizes (spec FR-020: the validator compares the acceptance map to
# the delta specifications and fails on a renamed/missing/duplicate scenario).
CHANGE_DIR = ROOT / "openspec" / "changes" / "define-avatar-client-contract-kernel"

# Allowed field set for an F0 interface-impact variance entry (spec FR-033). Any
# variance carrying a field outside this set fails the F0 gate closed. The F0
# sibling OWNS the schema; this mirrors its declared variance shape so an
# unexpected field never silently passes into the pinned baseline.
ALLOWED_VARIANCE_FIELDS = {
    "id", "field", "baseline", "baseline_value", "measured", "measured_value",
    "severity", "disposition", "rationale", "owner_change",
}

# ---- The eight AVC contracts + reserved identifiers (spec FR-001/FR-002) ----
CONTRACT_FILES = {
    "AVC-01": "avc-01-session-request.schema.yaml",
    "AVC-02": "avc-02-session-result.schema.yaml",
    "AVC-04": "avc-04-session-event.schema.yaml",
    "AVC-06": "avc-06-structured-confirmation.schema.yaml",
    "AVC-07": "avc-07-retention-profile.schema.yaml",
    "AVC-08": "avc-08-persona-profile.schema.yaml",
    "AVC-11": "avc-11-session-command.schema.yaml",
    "AVC-12": "avc-12-state-snapshot.schema.yaml",
}
RESERVED_IDS = {"AVC-03", "AVC-05", "AVC-09", "AVC-10"}

# ---- Semantic consumed set for per-file digests (spec FR-022 / Q1) ----
# Directories/files whose members are digested + manifest-registered. The
# validator script and redaction/ config are deliberately excluded (Design
# Note 3): shipped as tooling, content-addressed by commit, not pinned-semantic.
SEMANTIC_GLOBS = [
    "shared-definitions.schema.yaml",
    "avc-*.schema.yaml",
    "registries/*.registry.yaml",
    "fixtures/index.yaml",
    "fixtures/**/*.yaml",
    "acceptance-map.yaml",
    "interface-lock.yaml",
    "evidence-register.yaml",
]

# ---- schema/registry parity map: registry_id -> (schema file, JSON-pointer to enum) ----
# Only registries directly enumerated by a schema participate in set-equality.
PARITY = {
    "session-result-reasons": ("avc-02-session-result.schema.yaml", "reason"),
    "fallback-modes": ("avc-02-session-result.schema.yaml", "fallback"),
    "consent-purposes": ("shared-definitions.schema.yaml", "consent_purpose"),
    "commands": ("avc-11-session-command.schema.yaml", "command_type"),
    "events": ("avc-04-session-event.schema.yaml", "event_type"),
    "interaction-modes": ("avc-01-session-request.schema.yaml", "interaction_mode"),
    "capabilities": ("avc-01-session-request.schema.yaml", "capability"),
    "session-outcomes": ("shared-definitions.schema.yaml", "session_outcome"),
    "retention-classes": ("avc-07-retention-profile.schema.yaml", "retention_class"),
}
EXACT_COUNTS = {"session-result-reasons": 15, "consent-purposes": 3}

EVID_STATUS_TRANSITIONS = {
    "planned": {"evidenced", "deferred"},
    "evidenced": {"accepted"},
    "accepted": set(),
    "deferred": set(),
}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(f"note  {msg}")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def schema_files() -> list[Path]:
    files = sorted(AVC.glob("*.schema.yaml"))
    return files


def build_registry(f: Findings) -> tuple[Registry, dict[str, dict]]:
    """Build an offline referencing.Registry from every *.schema.yaml file."""
    resources = []
    docs: dict[str, dict] = {}
    for path in schema_files():
        try:
            doc = load_yaml(path)
        except yaml.YAMLError as exc:
            f.error("yaml", f"{path.name}: {exc}")
            continue
        if not isinstance(doc, dict):
            f.error("schema-shape", f"{path.name}: not a mapping")
            continue
        rid = doc.get("$id", path.name)
        docs[path.name] = doc
        try:
            resources.append((rid, Resource.from_contents(doc, default_specification=DRAFT202012)))
        except Exception as exc:  # noqa: BLE001
            f.error("resource", f"{path.name}: {exc}")
    registry = Registry().with_resources(resources)
    return registry, docs


# ----------------------------- checks -----------------------------

def check_metadata(f: Findings) -> None:
    """Every data YAML carries schema_version + kind; schema files carry $schema
    (+ contract_id/contract_schema_version for the eight contracts)."""
    for path in sorted(AVC.rglob("*.yaml")):
        rel = path.relative_to(ROOT)
        try:
            doc = load_yaml(path)
        except yaml.YAMLError as exc:
            f.error("yaml", f"{rel}: {exc}")
            continue
        if not isinstance(doc, dict):
            f.error("shape", f"{rel}: top-level mapping required")
            continue
        if path.name.endswith(".schema.yaml"):
            if "$schema" not in doc:
                f.error("meta", f"{rel}: JSON-Schema file missing $schema")
            cid = doc.get("contract_id")
            if path.name in CONTRACT_FILES.values():
                if cid not in CONTRACT_FILES:
                    f.error("meta", f"{rel}: contract_id must be one of the 8 AVC ids")
                if "contract_schema_version" not in doc:
                    f.error("meta", f"{rel}: missing contract_schema_version")
        else:
            if doc.get("schema_version") is None:
                f.error("meta", f"{rel}: missing schema_version")
            if not doc.get("kind"):
                f.error("meta", f"{rel}: missing kind")


def check_schemas(f: Findings, registry: Registry, docs: dict[str, dict]) -> None:
    """Schema validity, reserved-id guard, and offline $ref resolution."""
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-invalid", f"{name}: {exc}")
        cid = doc.get("contract_id")
        if cid in RESERVED_IDS:
            f.error("reserved-id", f"{name}: uses reserved contract_id {cid}")
    # reserved contract files must not exist
    for rid in RESERVED_IDS:
        stem = rid.lower()  # "AVC-09" -> "avc-09"
        for p in AVC.glob(f"{stem}-*.schema.yaml"):
            f.error("reserved-id", f"{p.name}: reserved identifier {rid} must not be published")
    # resolve every $ref
    for name, doc in docs.items():
        base = doc.get("$id", name)
        for ref in _iter_refs(doc):
            try:
                registry.resolver(base_uri=base).lookup(ref)
            except Exception as exc:  # noqa: BLE001
                f.error("ref", f"{name}: unresolved $ref {ref!r}: {exc}")
    # all eight contracts present?
    present = {d.get("contract_id") for d in docs.values()}
    for cid, fname in CONTRACT_FILES.items():
        if cid not in present:
            f.note(f"contract {cid} ({fname}) not yet authored")


def _iter_refs(node: Any):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                yield v
            else:
                yield from _iter_refs(v)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_refs(item)


def _find_enum(node: Any, marker: str) -> list | None:
    """Find an enum whose sibling `x-vocab` equals marker (deterministic bind)."""
    if isinstance(node, dict):
        if node.get("x-vocab") == marker and isinstance(node.get("enum"), list):
            return node["enum"]
        for v in node.values():
            found = _find_enum(v, marker)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = _find_enum(item, marker)
            if found is not None:
                return found
    return None


def check_registries(f: Findings, docs: dict[str, dict]) -> None:
    reg_dir = AVC / "registries"
    if not reg_dir.is_dir():
        return
    registries: dict[str, list[str]] = {}
    for path in sorted(reg_dir.glob("*.registry.yaml")):
        doc = load_yaml(path)
        if doc.get("kind") != "avatar-client-registry":
            f.error("registry-kind", f"{path.name}: kind must be avatar-client-registry")
            continue
        rid = doc.get("registry_id")
        members = doc.get("members") or []
        ids = [m.get("id") for m in members if isinstance(m, dict)]
        if len(ids) != len(set(ids)):
            f.error("registry-dup", f"{path.name}: duplicate member ids")
        registries[rid] = ids
    # parity + exact counts
    for rid, (sfile, marker) in PARITY.items():
        if rid not in registries:
            f.note(f"registry {rid} not yet authored")
            continue
        if rid in EXACT_COUNTS and len(registries[rid]) != EXACT_COUNTS[rid]:
            f.error("registry-count", f"{rid}: expected exactly {EXACT_COUNTS[rid]} members, got {len(registries[rid])}")
        sdoc = docs.get(sfile)
        if sdoc is None:
            f.note(f"parity for {rid} deferred (schema {sfile} absent)")
            continue
        enum = _find_enum(sdoc, marker)
        if enum is None:
            f.error("parity-missing", f"{sfile}: no enum bound to registry {rid} (x-vocab: {marker})")
            continue
        if set(enum) != set(registries[rid]):
            f.error("parity", f"{rid}: schema enum {sorted(set(enum))} != registry {sorted(set(registries[rid]))}")


def check_speech_gate(f: Findings, docs: dict[str, dict]) -> None:
    sd = docs.get("shared-definitions.schema.yaml")
    if sd is None:
        return
    enum = _find_enum(sd, "speech_gate")
    if enum is None:
        f.error("speech-gate", "shared-definitions: closed speech-gate enum (x-vocab: speech_gate) missing (analyze A3)")
        return
    required = {"confirmation_before_action", "streaming_monitor", "pre_speech_review"}
    if set(enum) != required:
        f.error("speech-gate", f"speech-gate enum must equal {sorted(required)}, got {sorted(set(enum))}")


# --------------------------- orchestration ---------------------------

def run(strict: bool, require_realization: bool) -> int:
    f = Findings()
    if not AVC.is_dir():
        print("ERROR contracts/avatar-client/ not found", file=sys.stderr)
        return 2

    check_metadata(f)
    registry, docs = build_registry(f)
    check_schemas(f, registry, docs)
    check_registries(f, docs)
    check_speech_gate(f, docs)
    # Fixture / acceptance / evidence / redaction / digest / F0-gate checks are
    # added in later phases; each guards on artifact presence so the validator
    # stays green at every phase checkpoint.
    ev_ids = check_fixtures(f, registry, docs)
    check_acceptance_and_evidence(f, ev_ids)
    check_release_identity(f)
    check_content_addressed_pin(f)
    check_redaction(f)
    check_digests(f)
    check_f0_gate(f, require_realization)

    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)

    n_e, n_w = len(f.errors), len(f.warnings)
    print(f"\nvalidate-avatar-client: {n_e} error(s), {n_w} warning(s)")
    if n_e or (strict and n_w):
        return 1
    return 0


ALL_CLASSES = {"valid", "invalid", "boundary", "compatibility",
               "unknown-field", "unknown-authority", "redaction", "adversarial"}
KNOWN_CHECKS = {"acceptance_map_parity", "contract_location", "release_identity",
                "content_addressed_pin", "fixture_conformance"}
EVID_TYPES = {"automated", "manual", "deferred"}


def check_fixtures(f: Findings, registry: Registry, docs: dict[str, dict]) -> set[str]:
    """US2 (T032): execute every self-describing fixture to its declared `expect`
    and check per-schema + per-class coverage. Returns the set of fixture
    evidence_ids for the evidence-register cross-check."""
    evidence_ids: set[str] = set()
    index = AVC / "fixtures" / "index.yaml"
    if not index.is_file():
        return evidence_ids
    idx = load_yaml(index)
    cases = idx.get("cases") or []
    schema_valid: dict[str, set[str]] = {}
    classes_seen: set[str] = set()
    case_ids: set[str] = set()
    for c in cases:
        cid = c.get("case_id")
        if cid in case_ids:
            f.error("fixture-dup", f"duplicate case_id {cid}")
        case_ids.add(cid)
        target, expect, klass = c.get("target"), c.get("expect"), c.get("class")
        if klass not in ALL_CLASSES:
            f.error("fixture-class", f"{cid}: unknown class {klass!r}")
        classes_seen.add(klass)
        if expect not in ("valid", "invalid"):
            f.error("fixture-expect", f"{cid}: expect must be valid|invalid")
            continue
        sdoc = docs.get(target)
        if sdoc is None:
            f.error("fixture-target", f"{cid}: unknown target schema {target!r}")
            continue
        errs = list(Draft202012Validator(sdoc, registry=registry).iter_errors(c.get("instance")))
        actual = "valid" if not errs else "invalid"
        if actual != expect:
            detail = errs[0].message[:120] if errs else ""
            f.error("fixture", f"{cid}: expected {expect} but got {actual} {detail}")
        else:
            schema_valid.setdefault(target, set()).add(expect)
        if c.get("evidence_id"):
            evidence_ids.add(c["evidence_id"])
    # per-schema coverage: every contract schema has >=1 valid and >=1 invalid
    for fname in CONTRACT_FILES.values():
        have = schema_valid.get(fname, set())
        for need in ("valid", "invalid"):
            if need not in have:
                f.error("coverage-schema", f"{fname}: missing a passing {need} fixture case")
    # per-class coverage across the suite
    for klass in sorted(ALL_CLASSES - classes_seen):
        f.error("coverage-class", f"no fixture case of class {klass}")
    return evidence_ids


def _delta_titles() -> tuple[list[str], list[str]] | None:
    """Extract the authoritative requirement + scenario titles declared in the
    OpenSpec change deltas (spec FR-020). Returns None if no delta specs are
    present so the parity cross-check is skipped rather than false-failing."""
    specs_dir = CHANGE_DIR / "specs"
    if not specs_dir.is_dir():
        return None
    md_files = sorted(specs_dir.rglob("spec.md"))
    if not md_files:
        return None
    req_titles: list[str] = []
    scen_titles: list[str] = []
    for md in md_files:
        for line in md.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("### Requirement:"):
                req_titles.append(s[len("### Requirement:"):].strip())
            elif s.startswith("#### Scenario:"):
                scen_titles.append(s[len("#### Scenario:"):].strip())
    return req_titles, scen_titles


def _legal_statuses_for(evidence_type: str) -> set[str]:
    """Statuses reachable for an entry of this evidence_type through the
    EVID_STATUS_TRANSITIONS graph (spec FR-032). A `deferred` entry takes the
    planned->deferred edge (terminal); every other type takes planned->evidenced
    (->accepted). Enforces the graph, not flat membership: e.g. a deferred entry
    marked `accepted`, or an automated entry marked `deferred`, is illegal."""
    first = "deferred" if evidence_type == "deferred" else "evidenced"
    legal = {"planned", first}
    frontier = [first]
    while frontier:
        node = frontier.pop()
        for nxt in EVID_STATUS_TRANSITIONS.get(node, set()):
            if nxt not in legal:
                legal.add(nxt)
                frontier.append(nxt)
    return legal


def check_acceptance_and_evidence(f: Findings, fixture_evidence_ids: set[str]) -> None:
    """US2 (T033): acceptance-map parity + evidence-register completeness, legal
    status, and referenced-artifact existence (spec FR-020/FR-032; ACR-012-S03)."""
    amap_path = AVC / "acceptance-map.yaml"
    if not amap_path.is_file():
        return
    amap = load_yaml(amap_path)
    reqs = amap.get("requirements") or []
    scen_ids: list[str] = []
    map_req_titles: list[str] = []
    map_scen_titles: list[str] = []
    for r in reqs:
        map_req_titles.append((r.get("title") or "").strip())
        for s in r.get("scenarios") or []:
            scen_ids.append(s["id"])
            map_scen_titles.append((s.get("title") or "").strip())
    if len(reqs) != amap.get("expected_requirement_count"):
        f.error("map-count", f"requirement count {len(reqs)} != expected {amap.get('expected_requirement_count')}")
    if len(scen_ids) != amap.get("expected_scenario_count"):
        f.error("map-count", f"scenario count {len(scen_ids)} != expected {amap.get('expected_scenario_count')}")
    if len(scen_ids) != len(set(scen_ids)):
        f.error("map-dup", "duplicate scenario ids in acceptance map")
    map_set = set(scen_ids)

    # Cross-check the map against the AUTHORITATIVE OpenSpec change deltas (spec
    # FR-020): a renamed, missing, or duplicate requirement/scenario must fail,
    # not merely disagree with the map's own expected_*_count self-reference.
    delta = _delta_titles()
    if delta is not None:
        delta_req_titles, delta_scen_titles = delta
        if len(delta_scen_titles) != len(set(delta_scen_titles)):
            dups = sorted({t for t in delta_scen_titles if delta_scen_titles.count(t) > 1})
            f.error("delta-parity", f"duplicate scenario titles in OpenSpec deltas: {dups}")
        for t in sorted(set(delta_req_titles) - set(map_req_titles)):
            f.error("delta-parity", f"requirement {t!r} declared in an OpenSpec delta is absent from the acceptance map")
        for t in sorted(set(map_req_titles) - set(delta_req_titles)):
            f.error("delta-parity", f"acceptance-map requirement {t!r} is not declared in any OpenSpec delta (renamed/removed?)")
        for t in sorted(set(delta_scen_titles) - set(map_scen_titles)):
            f.error("delta-parity", f"scenario {t!r} declared in an OpenSpec delta is absent from the acceptance map")
        for t in sorted(set(map_scen_titles) - set(delta_scen_titles)):
            f.error("delta-parity", f"acceptance-map scenario {t!r} is not declared in any OpenSpec delta (renamed/removed?)")

    reg_path = AVC / "evidence-register.yaml"
    if not reg_path.is_file():
        f.error("evidence", "evidence-register.yaml missing")
        return
    reg = load_yaml(reg_path)
    entries = reg.get("entries") or []
    reg_ids = [e["scenario_id"] for e in entries]
    reg_set = set(reg_ids)
    for missing in sorted(map_set - reg_set):
        f.error("evidence-missing", f"scenario {missing} has no evidence-register entry")
    for extra in sorted(reg_set - map_set):
        f.error("evidence-extra", f"evidence-register entry {extra} is not in the acceptance map")
    if len(reg_ids) != len(reg_set):
        f.error("evidence-dup", "duplicate scenario ids in evidence register")

    valid_status = {"planned", "evidenced", "accepted", "deferred"}
    for e in entries:
        sid = e.get("scenario_id")
        et = e.get("evidence_type")
        st = e.get("status")
        if et not in EVID_TYPES:
            f.error("evidence-type", f"{sid}: unknown evidence_type {et!r}")
        if st not in valid_status:
            f.error("evidence-status", f"{sid}: illegal status {st!r}")
        elif et in EVID_TYPES and st not in _legal_statuses_for(et):
            # Enforce the EVID_STATUS_TRANSITIONS graph, not flat membership
            # (spec FR-032): an illegal progression for this evidence_type fails.
            f.error("evidence-status",
                    f"{sid}: status {st!r} is not a legal transition for evidence_type {et!r} "
                    f"(allowed: {sorted(_legal_statuses_for(et))})")
        if et == "automated":
            if e.get("evidence_id"):
                if e["evidence_id"] not in fixture_evidence_ids:
                    f.error("evidence-fixture", f"{sid}: evidence_id {e['evidence_id']} not found in fixtures index")
            elif e.get("check"):
                if e["check"] not in KNOWN_CHECKS:
                    f.error("evidence-check", f"{sid}: unknown validator check {e['check']!r}")
            else:
                f.error("evidence-free", f"{sid}: automated entry has neither evidence_id nor check")
        elif et == "manual":
            for k in ("result", "reviewer", "disposition"):
                if not e.get(k):
                    f.error("evidence-manual", f"{sid}: manual entry missing {k}")
        elif et == "deferred":
            for k in ("owner_change", "fail_closed_default"):
                if not e.get(k):
                    f.error("evidence-deferred", f"{sid}: deferred entry missing {k}")


def check_redaction(f: Findings) -> None:
    """US2 (T034): dual redaction. Structural exclusion lives in the schemas; this
    is the committed-content scan with a bounded-sentinel allowlist (spec FR-018)."""
    denylist_path = AVC / "redaction" / "denylist-patterns.yaml"
    sentinels_path = AVC / "redaction" / "sentinels.yaml"
    if not denylist_path.is_file():
        return
    patterns = (load_yaml(denylist_path).get("patterns") or [])
    if not patterns:
        return
    sentinels = {s["bounded_form"] for s in (load_yaml(sentinels_path).get("sentinels") or [])}
    # structural sanity: sentinels must be obviously-fake bounded forms
    for s in (load_yaml(sentinels_path).get("sentinels") or []):
        bf = s.get("bounded_form", "")
        if not bf.startswith("SENTINEL_") or len(bf) > int(s.get("max_len", 0) or 0):
            f.error("sentinel", f"sentinel {s.get('id')} is not a bounded SENTINEL_ form within max_len")
    compiled = [(p["id"], re.compile(p["regex"])) for p in patterns]
    for path in sorted(AVC.rglob("*")):
        if not path.is_file():
            continue
        # The redaction/ config necessarily contains pattern fragments and the
        # bounded-sentinel forms; excluding it avoids self-matching (it is
        # validator config, not semantic contract content).
        if "redaction" in path.relative_to(AVC).parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pid, rx in compiled:
            for m in rx.finditer(text):
                if m.group(0) in sentinels:
                    continue
                f.error("redaction", f"{path.relative_to(ROOT)}: denylist pattern {pid} matched non-sentinel content: {m.group(0)[:40]!r}")


def _pin_is_content_addressed(pin: dict) -> bool:
    """A consumer pin is content-addressed iff it records the EXACT commit AND a
    per-file digest for each pinned file (spec FR-023). A tag-only pin — a tag
    with no commit and no per-file digests — is NOT content-addressed and MUST
    fail conformance (SCO-001-S03)."""
    if not isinstance(pin, dict):
        return False
    commit = pin.get("commit")
    digests = pin.get("file_digests")
    has_commit = isinstance(commit, str) and len(commit) >= 7
    has_digests = (
        isinstance(digests, dict)
        and len(digests) > 0
        and all(isinstance(v, str) and len(v) == 64 for v in digests.values())
    )
    return has_commit and has_digests


def check_content_addressed_pin(f: Findings) -> None:
    """SCO-001-S03 (evidence-register check `content_addressed_pin`): execute the
    self-describing pin cases and assert a tag-only pin is rejected while a full
    commit+digest pin is accepted. Fail closed if no cases are authored."""
    index = AVC / "fixtures" / "index.yaml"
    if not index.is_file():
        f.error("content-addressed-pin", "fixtures/index.yaml absent; tag-only-pin rejection is unproven (fail closed)")
        return
    cases = (load_yaml(index) or {}).get("release_pin_cases") or []
    if not cases:
        f.error("content-addressed-pin",
                "no release_pin_cases in fixtures/index.yaml; tag-only-pin rejection is unproven (fail closed)")
        return
    saw_invalid = False
    for c in cases:
        expect = c.get("expect")
        actual = "valid" if _pin_is_content_addressed(c.get("pin") or {}) else "invalid"
        if expect == "invalid":
            saw_invalid = True
        if actual != expect:
            f.error("content-addressed-pin",
                    f"{c.get('case_id')}: expected {expect} pin but got {actual}")
    if not saw_invalid:
        f.error("content-addressed-pin",
                "release_pin_cases lack a negative (tag-only) case; SCO-001-S03 is unproven (fail closed)")


def check_release_identity(f: Findings) -> None:
    """SCO-001-S02 (evidence-register check `release_identity`): verify the release
    identifiers agree across the artifacts that carry them, to the extent
    available pre-realization (spec FR-022). Fail closed if a cited artifact
    cannot be loaded. Full manifest/tag/commit/digest agreement is realized and
    enforced by check_digests once contracts/manifest.yaml is authored."""
    cited = {
        "interface-lock": (AVC / "interface-lock.yaml", ("change_id", "interface_baseline")),
        "acceptance-map": (AVC / "acceptance-map.yaml", ("change_id", "interface_baseline")),
        "evidence-register": (AVC / "evidence-register.yaml", ("change_id",)),
    }
    seen: dict[str, dict] = {}
    for label, (path, keys) in cited.items():
        if not path.is_file():
            f.error("release-identity", f"release identity uncheckable: {label} absent (fail closed)")
            return
        doc = load_yaml(path) or {}
        seen[label] = {k: doc.get(k) for k in keys}
    change_ids = {lbl: v.get("change_id") for lbl, v in seen.items()}
    if len(set(change_ids.values())) != 1 or None in change_ids.values():
        f.error("release-identity", f"release identifiers disagree: change_id {change_ids}")
    baselines = {lbl: v["interface_baseline"] for lbl, v in seen.items() if "interface_baseline" in v}
    if len(set(baselines.values())) != 1 or None in baselines.values():
        f.error("release-identity", f"release identifiers disagree: interface_baseline {baselines}")
    # Post-realization: once the avatar-client bundle is registered in
    # contracts/manifest.yaml (T046), its release identity — a declared bundle
    # version alongside the per-file digests (checked by check_digests) — must be
    # present. Pre-realization the kernel is not yet in the shared manifest, so
    # there is nothing to cross-check here.
    manifest = ROOT / "contracts" / "manifest.yaml"
    if manifest.is_file():
        mdoc = load_yaml(manifest) or {}
        avc_registered = any(
            str(c.get("path", "")).startswith("contracts/avatar-client/")
            for c in (mdoc.get("contracts") or [])
        )
        version = (mdoc.get("contract_bundle_version")
                   or mdoc.get("bundle_version") or mdoc.get("version"))
        if avc_registered and not version:
            f.error("release-identity",
                    "avatar-client bundle registered in contracts/manifest.yaml but no bundle version is declared")


def check_digests(f: Findings) -> None:
    """US3 (T036): per-file SHA-256 over the semantic consumed set + manifest/digest
    identity. The real contracts/manifest.yaml entries are authored at realization
    (T046); until then the digest set is computed and reported (A6). At realization
    the manifest digests must match the computed set (SCO-001-S02/S03)."""
    files = semantic_files()
    if not files:
        return
    computed = {str(p.relative_to(ROOT)): digest_file(p) for p in files}
    manifest = ROOT / "contracts" / "manifest.yaml"
    avc_entries: list[dict] = []
    if manifest.is_file():
        mdoc = load_yaml(manifest) or {}
        avc_entries = [c for c in (mdoc.get("contracts") or [])
                       if str(c.get("path", "")).startswith("contracts/avatar-client/")]
    if not avc_entries:
        f.note(f"release manifest/digests authored at realization (T046); "
               f"provisional per-file digest set computed over {len(computed)} semantic files")
        return
    manifest_paths = {c["path"]: c.get("sha256") for c in avc_entries}
    for path, dg in computed.items():
        if path not in manifest_paths:
            f.error("digest-missing", f"{path} not registered in contracts/manifest.yaml")
        elif manifest_paths[path] != dg:
            f.error("digest-mismatch", f"{path}: manifest sha256 != computed digest")
    for path in manifest_paths:
        if path not in computed:
            f.error("digest-extra", f"manifest lists {path} outside the semantic set")


def _load_f0_instance(path: Path) -> Any:
    """Load a consumed F0 evidence instance (JSON or YAML). Returns None when the
    file is absent or unparseable so the gate fails closed on it."""
    if not path.is_file():
        return None
    try:
        return load_yaml(path)  # yaml.safe_load also parses JSON
    except (yaml.YAMLError, OSError):
        return None


def f0_gate_decision(s: dict) -> tuple[bool, str]:
    """Pure fail-closed decision for the F0 publication gate (spec FR-033). Returns
    (unblocked, reason). Unblocks ONLY on a fully-satisfied PASS."""
    if not s.get("schema_present"):
        return False, "pinned F0 evidence schema absent"
    if not s.get("digest_match"):
        return False, "F0 schema digest mismatch"
    if not s.get("commit_match"):
        return False, "F0 source commit mismatch"
    if not s.get("instance_valid"):
        return False, "F0 evidence instance fails the pinned schema"
    if s.get("unknown_variance_field"):
        return False, "unknown variance field in F0 interface-impact evidence"
    st = s.get("status")
    if st not in ("PASS", "FAIL", "INCONCLUSIVE"):
        return False, f"unknown F0 status {st!r}"
    if st != "PASS":
        return False, f"F0 status {st}"
    if not s.get("variances_dispositioned"):
        return False, "an interface variance is undispositioned"
    return True, "F0 gate satisfied"


def check_f0_gate(f: Findings, require_realization: bool) -> None:
    """US4 (T039): fail-closed F0 publication gate + self-test of the adverse table."""
    # T040 self-test: prove the fail-closed table (does not need real F0 files).
    cases_path = AVC / "fixtures" / "f0-gate-cases.yaml"
    if cases_path.is_file():
        for c in (load_yaml(cases_path).get("cases") or []):
            unblocked, _ = f0_gate_decision(c.get("state") or {})
            if (not unblocked) != bool(c.get("expect_blocked")):
                f.error("f0-gate-selftest",
                        f"{c.get('id')}: expected blocked={c.get('expect_blocked')} got {not unblocked}")

    lock = AVC / "interface-lock.yaml"
    if not lock.is_file():
        if require_realization:
            f.error("f0-gate", "realization required but interface-lock.yaml absent")
        return
    pin = (load_yaml(lock).get("f0_evidence_pin") or {})
    if pin.get("status") != "ready":
        msg = "F0 publication gate: pending F0 PASS (pin status not ready); tag withheld"
        if require_realization:
            f.error("f0-gate", msg)
        else:
            f.note(msg + "; parallel implementation unaffected")
        return
    # pin claims ready -> verify the resolved, pinned F0 artifacts and fail closed.
    # The F0 evidence (schemas + instances) is OWNED by the sibling F0 change and
    # is NOT present in this worktree; when it is absent every dimension below
    # resolves False/unknown and the gate stays BLOCKED, exactly like the
    # tag-withheld `pending` path above.
    f0_dir = ROOT / (pin.get("f0_change_path") or "")
    rs = f0_dir / (pin.get("f0_results_schema") or "")
    iis = f0_dir / (pin.get("f0_interface_impact_schema") or "")
    schema_present = rs.is_file() and iis.is_file()

    # Load the consumed F0 evidence INSTANCES (f0-results + f0-interface-impact).
    ev_dir = f0_dir / "evidence"
    results_inst = (_load_f0_instance(ev_dir / "f0-results.json")
                    or _load_f0_instance(ev_dir / "f0-results.yaml"))
    impact_inst = (_load_f0_instance(ev_dir / "f0-interface-impact.yaml")
                   or _load_f0_instance(ev_dir / "f0-interface-impact.json"))

    # instance_valid: the instances must LOAD and VALIDATE against the pinned,
    # digest-checked F0 schemas. Absent or unvalidatable -> fail closed.
    instance_valid = False
    if schema_present and isinstance(results_inst, dict) and isinstance(impact_inst, dict):
        try:
            r_schema = load_yaml(rs)
            i_schema = load_yaml(iis)
            r_ok = not list(Draft202012Validator(r_schema).iter_errors(results_inst))
            i_ok = not list(Draft202012Validator(i_schema).iter_errors(impact_inst))
            instance_valid = r_ok and i_ok
        except Exception:  # noqa: BLE001
            instance_valid = False

    # commit_match: the pinned commit must equal the commit recorded in the
    # consumed F0 evidence instance. Missing on either side -> fail closed.
    recorded_commit = None
    if isinstance(results_inst, dict):
        recorded_commit = results_inst.get("source_commit") or results_inst.get("f0_source_commit")
    pinned_commit = pin.get("f0_source_commit")
    commit_match = bool(pinned_commit) and recorded_commit == pinned_commit

    # unknown_variance_field: any variance entry carrying a field outside the
    # allowed set -> fail closed.
    variances: list = []
    if isinstance(impact_inst, dict):
        variances = impact_inst.get("variances") or impact_inst.get("interface_variances") or []
    unknown_variance = any(
        isinstance(v, dict) and (set(v) - ALLOWED_VARIANCE_FIELDS) for v in variances
    )

    # variances_dispositioned: every reported variance carries a disposition.
    variances_dispositioned = all(
        isinstance(v, dict) and v.get("disposition") for v in variances
    ) if variances else bool(results_inst)

    status = None
    if isinstance(results_inst, dict):
        status = results_inst.get("status") or results_inst.get("f0_status")

    state = {
        "schema_present": schema_present,
        "digest_match": schema_present
        and pin.get("f0_results_schema_sha256") == digest_file(rs)
        and pin.get("f0_interface_impact_schema_sha256") == digest_file(iis),
        "commit_match": commit_match,
        "instance_valid": instance_valid,
        "unknown_variance_field": unknown_variance,
        "status": status,
        "variances_dispositioned": variances_dispositioned,
    }
    unblocked, reason = f0_gate_decision(state)
    if not unblocked:
        msg = f"F0 publication gate BLOCKED: {reason}"
        if require_realization:
            f.error("f0-gate", msg)
        else:
            f.note(msg + "; parallel implementation unaffected")


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_files() -> list[Path]:
    seen: dict[Path, None] = {}
    for pattern in SEMANTIC_GLOBS:
        for p in AVC.glob(pattern):
            if p.is_file():
                seen[p] = None
    return sorted(seen)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the AVC contract kernel")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--require-realization", action="store_true",
                    help="fail unless the F0 publication gate is satisfied (realization)")
    args = ap.parse_args()
    try:
        return run(args.strict, args.require_realization)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
