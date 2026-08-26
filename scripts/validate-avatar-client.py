#!/usr/bin/env python3
"""Validate the neutral avatar-client (AVC) contract kernel.

Reference runner and gate for the contract kernel under
``contracts/avatar-client/``: schema validity + offline ``$ref`` resolution,
closed-registry parity, self-describing fixture conformance, acceptance-map
parity, evidence-register completeness, dual redaction (structural + content
scan with bounded sentinels), per-file digests, and the fail-closed F0
publication gate.

Successor-register deferral discharge (locked decision 7 of
implement-avatar-client-lab): a released ``deferred`` scenario is NEVER
discharged by an in-place ``deferred->evidenced`` flip of the released,
content-addressed ``evidence-register.yaml`` (that stays terminal in
``EVID_STATUS_TRANSITIONS`` and byte-identical). Instead the discharging change
adds a SUCCESSOR register beside it — ``evidence-register.<change>.yaml`` —
carrying one ``discharges_deferred: true`` entry per discharged scenario whose
``owner_change`` matches the released deferred entry. These successors join the
semantic/digest surface (``SEMANTIC_GLOBS``) and, at release realization, must be
manifest-registered like any other bundle member. Rules (all fail-closed):
non-discharging entries are ILLEGAL in a successor register (completeness stays
single-sourced on the acceptance map + released register; brand-new scenarios
belong to a future bundle's map + released register, not a successor); each
released deferred entry may be discharged by EXACTLY ONE successor entry
(duplicate discharge fails); and a ``planned`` discharge is treated as DECLARED
but not yet effective — the released deferred entry stays authoritative and the
discharging entry's ``evidence_id`` is not required to resolve until the entry
flips to ``evidenced`` (a one-line change once the evidence fixture lands).

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
import tarfile
from pathlib import Path, PurePosixPath
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
    # Successor deferral-discharge registers (decision 7) join the digested,
    # manifest-registered semantic surface too. The pattern requires a middle
    # segment (`.<change>.`), so it is disjoint from the released
    # `evidence-register.yaml` above and never double-collects it.
    "evidence-register.*.yaml",
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

# ---- Client-lab acceptance map (implement-avatar-client-lab task 4.2) ----
# The neutral, openxFactory-owned client-lab acceptance map DECLARES what the
# offline avatar client lab proves. It lives OUTSIDE contracts/avatar-client/ (so
# it is untouched by the AVC digest/metadata/redaction scans) and inherits a fixed
# scenario slice from the two released acceptance maps. This validator fail-closes
# on drift between the map and those released maps, mirroring
# check_successor_discharge. It owns NONE of the released bytes.
CLIENT_LAB_MAP = ROOT / "contracts" / "avatar-client-lab" / "client-acceptance-map.yaml"
AFU_ACCEPTANCE_MAP = (ROOT / "examples" / "avatar-first-ui"
                      / "avatar-first-ui-acceptance-map.yaml")
CLIENT_LAB_CHANGE = "implement-avatar-client-lab"
CLIENT_LAB_GATES = {
    "schema_conformance", "content_addressed_pin", "replay_determinism", "golden",
    "accessibility", "authority_derivation", "production_boundary",
    "fail_closed_seam", "evidence_completeness",
}
CLIENT_LAB_A11Y = {
    "keyboard_operation", "stable_focus", "visible_focus",
    "screen_reader_announcements", "captions", "text_only_mode", "reduced_motion",
    "high_contrast", "non_color_cues", "zoom_reflow", "pseudo_locale_coverage",
}
CLIENT_EVIDENCE_CLASSES = {"fixture", "golden", "successor"}
CLIENT_LAB_FOCI = {"M0", "F1", "F2", "F3", "F4", "cross_cutting"}

# ---- Capability-scenario register (adopt-avatar-client-lab-candidates task 3.1/P10) ----
# The neutral, openxFactory-owned register that enumerates the 22 avatar-client-lab
# capability scenarios (9 requirements) gate (ix)(b) resolves, each with a stable
# ACL-* id and a VERBATIM `#### Scenario:` title transcribed from the
# implement-avatar-client-lab capability spec delta (design D2, Option B). Landed as a
# distinct register (not an extension of the client-lab map). check_capability_scenario_register
# fail-closes on any drift between the register and that spec (mirrors
# check_client_lab_acceptance_map). It owns none of the released bytes.
CAP_REGISTER = ROOT / "contracts" / "avatar-client-lab" / "capability-scenario-register.yaml"
# Authoritative title source: the PROMOTED capability spec once
# implement-avatar-client-lab archives; until then the change-delta copy. The check
# re-verifies against the promoted path if it exists, else falls back to the delta.
CAP_SPEC_PROMOTED = ROOT / "openspec" / "specs" / "avatar-client-lab" / "spec.md"
CAP_SPEC_DELTA = (ROOT / "openspec" / "changes" / "implement-avatar-client-lab"
                  / "specs" / "avatar-client-lab" / "spec.md")
CAP_REGISTER_KIND = "avatar-client-lab-capability-scenario-register"
CAP_ID_REQ = re.compile(r"^ACL-\d{3}$")
CAP_ID_SCEN = re.compile(r"^ACL-\d{3}-S\d{2}$")

# ---- Avatar-state derivation table (adopt-avatar-client-lab-candidates task 4.3 / P1) ----
# The neutral, openxFactory-owned table (design D3) that maps the four authoritative runtime
# axes onto the six FR-019 avatar presentation states.
# check_avatar_state_derivation_table fail-closes on: an `outputs` set != the six FR-019 states;
# an `inputs.media_states` axis != the closed ten; any landed deterministic seed that DECLARES an
# avatar state not resolving to it under the table's precedence (R0..R6 over the seed's reduced/
# kernel fields); a `reachability_named_combinations` set != the gate (ix)(a) set; or an
# invariant-contradiction row (control loss mapped to anything but `blocked`). It owns none of the
# released bytes and is guarded on the table's presence (pre-landing compat).
DERIV_TABLE_YAML = ROOT / "contracts" / "avatar-client-lab" / "avatar-state-derivation-table.yaml"
DERIV_TABLE_KIND = "avatar-client-registry"
DERIV_SEEDS_DIR = ROOT / "examples" / "avatar-first-ui" / "fixtures" / "deterministic"
# The six FR-019 avatar presentation states (the table's `outputs`).
DERIV_STATES = {"listening", "thinking", "speaking", "interrupted", "blocked", "handoff"}
# The ten closed media.states (avatar-first-ui-profile.schema.yaml media.states; FR-012 denominator).
DERIV_MEDIA_STATES = {
    "permission", "capture_authorized", "capture_pending", "capture_active",
    "listening", "speaking", "control_degraded", "control_lost",
    "governed_action_pending", "retention_active",
}
# Presentation-superset media_state values a reducer may emit that are NOT denominator members;
# each is recognized (intercepted by R1-R4, or by an R3 terminal), never an R0 unknown (table §1).
DERIV_PRESENTATION_EXTRA = {"idle", "blocked", "revoked", "handoff", "interrupted"}
# The six terminal session_outcome values that trip R3 (the gate (ix)(a) terminal set).
DERIV_TERMINAL_OUTCOMES = {
    "denied", "revoked", "abandoned", "expired", "completed", "session_limit_reached",
}
# session_lifecycle signals: handoff (trip R2) and processing (raise the R5 `thinking` overlay).
DERIV_HANDOFF_SIGNALS = {"handoff_requested", "handoff_active"}
DERIV_PROCESSING_SIGNALS = {"tool_request_pending", "workflow_waiting",
                            "comprehension_or_confirmation_check"}


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
    check_client_lab_acceptance_map(f)
    check_capability_scenario_register(f)
    check_avatar_state_derivation_table(f)
    check_release_identity(f)
    check_content_addressed_pin(f)
    check_redaction(f)
    check_digests(f, require_realization)
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

    # Decision 7: successor registers discharge released `deferred` entries
    # WITHOUT touching this released register (which stays byte-identical above).
    check_successor_discharge(f, entries, fixture_evidence_ids)


def _is_successor_register(name: str) -> bool:
    """A successor deferral-discharge register is `evidence-register.<change>.yaml`
    (a middle `<change>` segment) — never the released `evidence-register.yaml`."""
    return (name.startswith("evidence-register.")
            and name.endswith(".yaml")
            and name != "evidence-register.yaml")


def successor_register_files() -> list[Path]:
    return sorted(p for p in AVC.glob("evidence-register.*.yaml")
                  if p.is_file() and _is_successor_register(p.name))


def check_successor_discharge(f: Findings, released_entries: list,
                              fixture_evidence_ids: set[str]) -> None:
    """Decision 7 (locked): machine-check the successor-register discharge of
    released `deferred` scenarios. A released `deferred` entry MAY be discharged
    by EXACTLY ONE successor entry carrying `discharges_deferred: true` whose
    `owner_change` matches the released deferred entry. The released register and
    acceptance map stay byte-identical; the in-place `deferred->evidenced` flip
    remains illegal (enforced separately by EVID_STATUS_TRANSITIONS on the
    released register). Design rules encoded here, all fail-closed:

    - Non-discharging entries are ILLEGAL in a successor register. Successors exist
      ONLY to discharge; a brand-new scenario belongs to a future bundle's
      acceptance map + released register, so completeness stays single-sourced on
      the released register and the map (which this function never re-derives).
    - Each released deferred scenario is dischargeable exactly once across all
      successor entries/files; any duplicate discharge fails (`successor-dup`).
      This is the ONLY relaxation of the evidence-dup rule — the released register
      keeps its deferred entry and the successor adds the single discharging one.
    - A `planned` discharge is DECLARED but not yet effective: the released deferred
      entry stays authoritative and the discharging `evidence_id` need not resolve
      to a fixture yet. Only an EFFECTIVE (`evidenced`/`accepted`) automated
      discharge must name an `evidence_id` present in the fixtures index; an
      effective manual discharge must carry result/reviewer/disposition.
    - The `change_id` field must match the filename suffix so a successor register
      cannot masquerade as owned by a different change.
    """
    released_by_id = {e.get("scenario_id"): e for e in released_entries}
    released_deferred = {
        sid: e for sid, e in released_by_id.items()
        if e.get("evidence_type") == "deferred" and e.get("status") == "deferred"
    }
    discharged: dict[str, str] = {}  # scenario_id -> file that discharged it
    for path in successor_register_files():
        rel = str(path.relative_to(ROOT))
        doc = load_yaml(path) or {}
        if not isinstance(doc, dict):
            f.error("successor-meta", f"{rel}: top-level mapping required")
            continue
        if doc.get("schema_version") is None:
            f.error("successor-meta", f"{rel}: missing schema_version")
        if doc.get("kind") != "avatar-client-evidence-register":
            f.error("successor-meta", f"{rel}: kind must be avatar-client-evidence-register")
        change_id = doc.get("change_id")
        suffix = path.name[len("evidence-register."):-len(".yaml")]
        if not change_id:
            f.error("successor-meta", f"{rel}: missing change_id")
        elif change_id != suffix:
            f.error("successor-change-id",
                    f"{rel}: change_id {change_id!r} does not match filename suffix {suffix!r}")
        for e in doc.get("entries") or []:
            sid = e.get("scenario_id")
            if not e.get("discharges_deferred"):
                f.error("successor-nondischarge",
                        f"{rel}: entry {sid!r} lacks discharges_deferred: true; a successor "
                        f"register may only discharge released deferred scenarios (a new scenario "
                        f"belongs to a future bundle's acceptance map + released register)")
                continue
            owner = e.get("owner_change")
            if sid not in released_by_id:
                f.error("successor-no-deferred",
                        f"{rel}: discharge of {sid!r} has no matching scenario in the released register")
                continue
            if sid not in released_deferred:
                f.error("successor-target-not-deferred",
                        f"{rel}: {sid!r} is not a released `deferred` entry and cannot be discharged")
                continue
            released_owner = released_deferred[sid].get("owner_change")
            if not owner or owner != released_owner:
                f.error("successor-owner-mismatch",
                        f"{rel}: discharge of {sid!r} names owner_change {owner!r} but the released "
                        f"deferred entry names {released_owner!r}")
                continue
            if sid in discharged:
                f.error("successor-dup",
                        f"{rel}: {sid!r} is already discharged by {discharged[sid]}; a released "
                        f"deferred entry may be discharged by exactly one successor entry")
                continue
            discharged[sid] = rel
            et = e.get("evidence_type")
            st = e.get("status")
            if et not in EVID_TYPES or et == "deferred":
                f.error("successor-type",
                        f"{rel}: {sid!r} discharge evidence_type must be automated|manual, got {et!r}")
                continue
            if st not in _legal_statuses_for(et):
                f.error("successor-status",
                        f"{rel}: {sid!r} status {st!r} is not a legal transition for evidence_type "
                        f"{et!r} (allowed: {sorted(_legal_statuses_for(et))})")
                continue
            if st == "planned":
                # Declared, not yet effective: released deferred entry remains
                # authoritative; evidence need not resolve until the flip.
                continue
            if et == "automated":
                ev = e.get("evidence_id")
                if not ev:
                    f.error("successor-evidence",
                            f"{rel}: {sid!r} effective automated discharge missing evidence_id")
                elif ev not in fixture_evidence_ids:
                    f.error("successor-evidence",
                            f"{rel}: {sid!r} evidence_id {ev!r} not found in fixtures index")
            elif et == "manual":
                for k in ("result", "reviewer", "disposition"):
                    if not e.get(k):
                        f.error("successor-manual", f"{rel}: {sid!r} manual discharge missing {k}")


def _release_map_index(path: Path) -> dict[str, dict]:
    """Index a released acceptance map as {requirement_id: {title, owner_changes,
    scenarios{sid: title}}} for the client-lab parity cross-check."""
    doc = load_yaml(path) or {}
    idx: dict[str, dict] = {}
    for r in doc.get("requirements") or []:
        rid = r.get("id")
        scen = {s.get("id"): (s.get("title") or "").strip()
                for s in (r.get("scenarios") or [])}
        idx[rid] = {
            "title": (r.get("title") or "").strip(),
            "owner_changes": set(r.get("owner_changes") or []),
            "scenarios": scen,
        }
    return idx


def check_client_lab_acceptance_map(f: Findings) -> None:
    """Task 4.2 (locked decision after FR-040): machine-check the neutral,
    openxFactory-owned client-lab acceptance map against the two released
    acceptance maps it inherits from, fail-closed (mirroring
    check_successor_discharge). The client-lab map DECLARES what the offline lab
    proves; it owns none of the released bytes. Rules:

    - Metadata: schema_version + kind == avatar-client-lab-acceptance-map +
      change_id == implement-avatar-client-lab.
    - Gating frame: the gates block is EXACTLY the nine offline CI gates and the
      accessibility_baseline is EXACTLY the eleven capabilities; F1-F4 foci present.
    - Verbatim parity: every listed requirement/scenario id + title must match its
      source released map exactly (no fabricated or renamed item), and every listed
      requirement must name this change as an owner_change in that released map
      (no overclaiming).
    - Requirement-level completeness: every requirement that names this change as an
      owner_change in EITHER released map must appear here (no silently dropped
      inherited requirement). Scenario-level slicing (e.g. ACR-003's media-gate
      slice) is allowed — only listed scenarios are parity-checked.
    - Evidence class ∈ {fixture, golden, successor} (FR-040: reducer + widget
      behaviour, not schema re-proof); any referenced gate is one of the nine; any
      referenced fixture path exists; a `discharge_via` successor register exists
      and actually discharges that scenario (consistency with decision 7).
    - Counts self-check.

    Guarded on the map's presence so a kernel-only checkout stays green.
    """
    if not CLIENT_LAB_MAP.is_file():
        return
    doc = load_yaml(CLIENT_LAB_MAP) or {}
    rp = str(CLIENT_LAB_MAP.relative_to(ROOT))
    if not isinstance(doc, dict):
        f.error("client-lab-meta", f"{rp}: top-level mapping required")
        return
    if doc.get("schema_version") is None:
        f.error("client-lab-meta", f"{rp}: missing schema_version")
    if doc.get("kind") != "avatar-client-lab-acceptance-map":
        f.error("client-lab-meta", f"{rp}: kind must be avatar-client-lab-acceptance-map")
    if doc.get("change_id") != CLIENT_LAB_CHANGE:
        f.error("client-lab-meta", f"{rp}: change_id must be {CLIENT_LAB_CHANGE!r}")

    gate_ids = [g.get("id") for g in (doc.get("gates") or [])]
    if len(gate_ids) != len(set(gate_ids)) or set(gate_ids) != CLIENT_LAB_GATES:
        f.error("client-lab-gates",
                f"{rp}: gates must be exactly the nine {sorted(CLIENT_LAB_GATES)}, "
                f"got {sorted(set(gate_ids))}")

    caps = (doc.get("accessibility_baseline") or {}).get("capabilities") or []
    if len(caps) != len(set(caps)) or set(caps) != CLIENT_LAB_A11Y:
        f.error("client-lab-a11y",
                f"{rp}: accessibility_baseline.capabilities must be exactly the "
                f"eleven {sorted(CLIENT_LAB_A11Y)}, got {sorted(set(caps))}")

    focus_ids = {x.get("id") for x in (doc.get("acceptance_foci") or [])}
    for need in ("F1", "F2", "F3", "F4"):
        if need not in focus_ids:
            f.error("client-lab-foci", f"{rp}: acceptance_foci missing {need}")

    src = {
        "avatar-client": _release_map_index(AVC / "acceptance-map.yaml"),
        "avatar-first-ui": _release_map_index(AFU_ACCEPTANCE_MAP),
    }
    if not src["avatar-client"] or not src["avatar-first-ui"]:
        f.error("client-lab-source",
                f"{rp}: a released source acceptance map is missing/empty (fail closed)")
        return

    # Requirements that name this change as owner in EITHER released map.
    owed_reqs = {(key, rid)
                 for key, idx in src.items()
                 for rid, meta in idx.items()
                 if CLIENT_LAB_CHANGE in meta["owner_changes"]}

    listed_reqs: set[tuple[str, str]] = set()
    all_sids: list[str] = []
    for block in (doc.get("inherited_scenarios") or []):
        key = block.get("source_map")
        rid = block.get("requirement")
        idx = src.get(key)
        if idx is None:
            f.error("client-lab-scenario", f"{rp}: requirement {rid} has unknown source_map {key!r}")
            continue
        rmeta = idx.get(rid)
        if rmeta is None:
            f.error("client-lab-scenario", f"{rp}: requirement {rid} is not in the released {key} map")
            continue
        listed_reqs.add((key, rid))
        if (block.get("title") or "").strip() != rmeta["title"]:
            f.error("client-lab-parity",
                    f"{rp}: requirement {rid} title != released title {rmeta['title']!r}")
        if CLIENT_LAB_CHANGE not in rmeta["owner_changes"]:
            f.error("client-lab-owner",
                    f"{rp}: requirement {rid} does not name {CLIENT_LAB_CHANGE} as an "
                    f"owner_change in the released {key} map (overclaimed)")
        if block.get("focus") not in CLIENT_LAB_FOCI:
            f.error("client-lab-foci",
                    f"{rp}: requirement {rid} focus {block.get('focus')!r} not in {sorted(CLIENT_LAB_FOCI)}")
        for s in (block.get("scenarios") or []):
            sid = s.get("id")
            all_sids.append(sid)
            rel_title = rmeta["scenarios"].get(sid)
            if rel_title is None:
                f.error("client-lab-parity",
                        f"{rp}: scenario {sid} is not a released scenario of {rid} in the {key} map")
            elif (s.get("title") or "").strip() != rel_title:
                f.error("client-lab-parity",
                        f"{rp}: scenario {sid} title != released title {rel_title!r}")
            cls = s.get("client_evidence_class")
            if cls not in CLIENT_EVIDENCE_CLASSES:
                f.error("client-lab-class",
                        f"{rp}: scenario {sid} client_evidence_class {cls!r} not in "
                        f"{sorted(CLIENT_EVIDENCE_CLASSES)}")
            g = s.get("gate")
            if g is not None and g not in CLIENT_LAB_GATES:
                f.error("client-lab-gates", f"{rp}: scenario {sid} gate {g!r} is not one of the nine gates")
            fx = s.get("fixture")
            if fx is not None and not (ROOT / fx).is_file():
                f.error("client-lab-fixture", f"{rp}: scenario {sid} fixture {fx} does not exist")
            dv = s.get("discharge_via")
            if dv is not None:
                dvp = ROOT / dv
                if not dvp.is_file():
                    f.error("client-lab-discharge", f"{rp}: scenario {sid} discharge_via {dv} does not exist")
                else:
                    reg = load_yaml(dvp) or {}
                    discharged = {e.get("scenario_id") for e in (reg.get("entries") or [])
                                  if e.get("discharges_deferred")}
                    if sid not in discharged:
                        f.error("client-lab-discharge",
                                f"{rp}: scenario {sid} names discharge_via {dv} but that "
                                f"successor register does not discharge it")

    for key, rid in sorted(owed_reqs - listed_reqs):
        f.error("client-lab-incomplete",
                f"{rp}: released {key} requirement {rid} names {CLIENT_LAB_CHANGE} as an "
                f"owner_change but is absent from the client-lab map (dropped inherited requirement)")

    if len(all_sids) != len(set(all_sids)):
        f.error("client-lab-dup", f"{rp}: duplicate scenario ids in the client-lab map")

    n_reqs = len(doc.get("inherited_scenarios") or [])
    if doc.get("expected_requirement_count") != n_reqs:
        f.error("client-lab-count",
                f"{rp}: expected_requirement_count {doc.get('expected_requirement_count')} != {n_reqs} listed")
    if doc.get("expected_scenario_count") != len(all_sids):
        f.error("client-lab-count",
                f"{rp}: expected_scenario_count {doc.get('expected_scenario_count')} != {len(all_sids)} listed")


def _capability_spec_titles() -> tuple[str, list[str], list[str]] | None:
    """Extract the authoritative avatar-client-lab requirement + scenario titles from
    the capability spec, in document order (spec FR-020 style). Reads the PROMOTED
    ``openspec/specs/avatar-client-lab/spec.md`` once ``implement-avatar-client-lab``
    archives, else the change-delta copy. Returns (source_label, req_titles,
    scen_titles), or None if neither spec path exists (so the caller fails closed).
    Mirrors _delta_titles: the requirement/scenario heading keyword must be on the
    line's start."""
    if CAP_SPEC_PROMOTED.is_file():
        path, label = CAP_SPEC_PROMOTED, "promoted"
    elif CAP_SPEC_DELTA.is_file():
        path, label = CAP_SPEC_DELTA, "change-delta"
    else:
        return None
    req_titles: list[str] = []
    scen_titles: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("### Requirement:"):
            req_titles.append(s[len("### Requirement:"):].strip())
        elif s.startswith("#### Scenario:"):
            scen_titles.append(s[len("#### Scenario:"):].strip())
    return label, req_titles, scen_titles


def check_capability_scenario_register(f: Findings) -> None:
    """P10 (adopt-avatar-client-lab-candidates task 3.2; design D2): machine-check the
    neutral avatar-client-lab capability-scenario register against the authoritative
    capability spec, fail-closed, mirroring check_client_lab_acceptance_map.

    The register enumerates the 22 avatar-client-lab capability scenarios (9
    requirements) gate (ix)(b) resolves, each with a stable ACL-* id and a VERBATIM
    ``#### Scenario:`` title transcribed from the implement-avatar-client-lab
    capability spec delta. All rules fail closed:

    - Metadata: schema_version + kind == avatar-client-lab-capability-scenario-register.
    - Counts self-check: expected_requirement_count == the number of requirement
      blocks (9); expected_scenario_count == the number of scenarios listed (22).
    - Ids unique and pattern-conformant (^ACL-\\d{3}$ / ^ACL-\\d{3}-S\\d{2}$).
    - VERBATIM title fidelity IN DOCUMENT ORDER: the ordered list of requirement titles
      and the ordered list of scenario titles must byte-match the spec's
      ``### Requirement:`` / ``#### Scenario:`` headings exactly. This is an ordered
      element-wise compare, so a fabricated, renamed, dropped, OR reordered entry all
      fail (a reorder fails even though the sets are equal).

    Source path (design D2): the PROMOTED openspec/specs/avatar-client-lab/spec.md once
    implement-avatar-client-lab archives; until then the change-delta copy — the check
    is pinned to re-verify against the promoted path the moment it exists. Guarded on
    the register's presence so a checkout without it stays green.
    """
    if not CAP_REGISTER.is_file():
        return
    rp = str(CAP_REGISTER.relative_to(ROOT))
    doc = load_yaml(CAP_REGISTER) or {}
    if not isinstance(doc, dict):
        f.error("cap-register-meta", f"{rp}: top-level mapping required")
        return
    if doc.get("schema_version") is None:
        f.error("cap-register-meta", f"{rp}: missing schema_version")
    if doc.get("kind") != CAP_REGISTER_KIND:
        f.error("cap-register-meta", f"{rp}: kind must be {CAP_REGISTER_KIND!r}")

    reqs = doc.get("requirements") or []
    reg_req_titles: list[str] = []
    reg_scen_titles: list[str] = []
    ids: list[str] = []
    for r in reqs:
        if not isinstance(r, dict):
            f.error("cap-register-shape", f"{rp}: requirement entry must be a mapping")
            continue
        rid = r.get("id")
        ids.append(rid)
        if not (isinstance(rid, str) and CAP_ID_REQ.match(rid)):
            f.error("cap-register-id", f"{rp}: requirement id {rid!r} must match ^ACL-\\d{{3}}$")
        reg_req_titles.append((r.get("title") or "").strip())
        for s in r.get("scenarios") or []:
            if not isinstance(s, dict):
                f.error("cap-register-shape", f"{rp}: scenario entry must be a mapping")
                continue
            sid = s.get("id")
            ids.append(sid)
            if not (isinstance(sid, str) and CAP_ID_SCEN.match(sid)):
                f.error("cap-register-id",
                        f"{rp}: scenario id {sid!r} must match ^ACL-\\d{{3}}-S\\d{{2}}$")
            reg_scen_titles.append((s.get("title") or "").strip())

    # Counts self-check.
    if doc.get("expected_requirement_count") != len(reqs):
        f.error("cap-register-count",
                f"{rp}: expected_requirement_count {doc.get('expected_requirement_count')} "
                f"!= {len(reqs)} requirement blocks listed")
    if doc.get("expected_scenario_count") != len(reg_scen_titles):
        f.error("cap-register-count",
                f"{rp}: expected_scenario_count {doc.get('expected_scenario_count')} "
                f"!= {len(reg_scen_titles)} scenarios listed")

    # Id uniqueness.
    concrete = [i for i in ids if i is not None]
    if len(concrete) != len(set(concrete)):
        dups = sorted({i for i in concrete if concrete.count(i) > 1})
        f.error("cap-register-dup", f"{rp}: duplicate ids {dups}")

    # Verbatim title fidelity, IN DOCUMENT ORDER, against the authoritative spec.
    titles = _capability_spec_titles()
    if titles is None:
        f.error("cap-register-source",
                f"{rp}: neither the promoted openspec/specs/avatar-client-lab/spec.md nor the "
                f"change-delta openspec/changes/implement-avatar-client-lab/specs/avatar-client-lab/"
                f"spec.md capability spec exists (fail closed)")
        return
    src_label, spec_req_titles, spec_scen_titles = titles
    if reg_req_titles != spec_req_titles:
        f.error("cap-register-parity",
                f"{rp}: requirement titles do not byte-match the {src_label} capability spec in "
                f"document order (no fabricated/renamed/dropped/reordered entry): "
                f"register {reg_req_titles} != spec {spec_req_titles}")
    if reg_scen_titles != spec_scen_titles:
        f.error("cap-register-parity",
                f"{rp}: scenario titles do not byte-match the {src_label} capability spec in "
                f"document order (no fabricated/renamed/dropped/reordered entry): "
                f"register {reg_scen_titles} != spec {spec_scen_titles}")


def _canon_control(value: Any) -> Any:
    """Canonicalize the control axis to {healthy, degraded, lost} (table §2.2; data-model §4 / L4):
    the already-flavored `control_lost` / `control_degraded` denominator spellings fold to the
    canonical `lost` / `degraded` enum; `healthy` / `degraded` / `lost` pass through."""
    return {"control_lost": "lost", "control_degraded": "degraded"}.get(value, value)


def _derive_avatar_state(view_state: dict, snapshot: dict, media_state_map: dict) -> str:
    """Faithful reimplementation of the table's precedence (§4 R0..R6; first match wins) over a
    seed's reduced `expected.view_state` (+ the kernel `canonical.snapshot` for session_outcome /
    session_lifecycle). Returns one of the six avatar states. The R5 base map is read from the
    table's own `media_state_map`, so the OQ-5 mapping (governed_action_pending => listening) and
    the OQ-6 fail-closed `blocked` are whatever the landed table declares. R4 keys on the reducer's
    surfaced `media_state == interrupted`; R2 keys on a handoff signal (§4.1 note: R1..R4 intercept
    every control/handoff/terminal/interruption value before R5 reads media_state)."""
    media = view_state.get("media_state")
    control = _canon_control(view_state.get("control_state")
                             if view_state.get("control_state") is not None
                             else snapshot.get("control_health"))
    outcome = (snapshot.get("session_outcome")
               if snapshot.get("session_outcome") is not None
               else view_state.get("session_outcome"))
    workflow = view_state.get("workflow_projection") or snapshot.get("workflow_projection")
    lifecycle = snapshot.get("session_lifecycle") or view_state.get("session_lifecycle")
    recognized_media = DERIV_MEDIA_STATES | DERIV_PRESENTATION_EXTRA

    # R0 — fail-closed / indeterminate: unknown enum on any consumed axis, or an axis
    # inconsistency (a control media.state while control_health = healthy) => blocked (OQ-6).
    if control is not None and control not in {"healthy", "degraded", "lost"}:
        return "blocked"
    if outcome is not None and outcome not in (DERIV_TERMINAL_OUTCOMES | {"granted"}):
        return "blocked"
    if media is not None and media not in recognized_media:
        return "blocked"
    if media in {"control_lost", "control_degraded"} and control == "healthy":
        return "blocked"

    # R1 — control-health safety trip => blocked (INV-1; never speaking).
    if control in {"degraded", "lost"} or media in {"control_degraded", "control_lost"}:
        return "blocked"

    # R2 — handoff (control healthy) => handoff (INV-3).
    if lifecycle in DERIV_HANDOFF_SIGNALS or workflow == "handoff" or media == "handoff":
        return "handoff"

    # R3 — authored terminal / clean revocation (kernel session_outcome only) => listening (INV-4).
    if outcome in DERIV_TERMINAL_OUTCOMES:
        return "listening"

    # R4 — interruption of an active turn (reducer surfaces it as media_state == interrupted).
    if media == "interrupted":
        return "interrupted"

    # R5 — live media-state presentation (+ the command-in-flight `thinking` overlay, which does
    # NOT override speaking), from the table's own base map.
    if lifecycle in DERIV_PROCESSING_SIGNALS and media != "speaking":
        return "thinking"
    return media_state_map.get(media, "listening")


def _check_derivation_reachability(f: Findings, rp: str, reach: list) -> None:
    """(iv) `reachability_named_combinations` must be EXACTLY the gate (ix)(a) set the table
    names: control_health lost=>control_lost and degraded=>control_degraded, one media_state group
    (the eight non-control denominator states), and the six terminal session_outcomes — no more."""
    control_vals: dict[Any, Any] = {}
    media_groups = 0
    outcome_groups: list[set] = []
    extra: list = []
    for entry in reach:
        if not isinstance(entry, dict):
            f.error("derivation-reachability", f"{rp}: reachability entry must be a mapping")
            continue
        axis = entry.get("axis")
        if axis == "control_health":
            control_vals[entry.get("value")] = entry.get("evidences_media_state")
        elif axis == "media_state":
            media_groups += 1
        elif axis == "session_outcome":
            outcome_groups.append(set(entry.get("values") or []))
        else:
            extra.append(axis)
    if (set(control_vals) != {"lost", "degraded"}
            or control_vals.get("lost") != "control_lost"
            or control_vals.get("degraded") != "control_degraded"):
        f.error("derivation-reachability",
                f"{rp}: reachability control_health combinations must be exactly "
                f"lost=>control_lost and degraded=>control_degraded, got {control_vals!r}")
    if media_groups != 1:
        f.error("derivation-reachability",
                f"{rp}: reachability must name exactly one non-control media_state group, "
                f"got {media_groups}")
    if len(outcome_groups) != 1 or outcome_groups[0] != DERIV_TERMINAL_OUTCOMES:
        f.error("derivation-reachability",
                f"{rp}: reachability session_outcome terminals must be exactly "
                f"{sorted(DERIV_TERMINAL_OUTCOMES)}, got {[sorted(g) for g in outcome_groups]}")
    if extra:
        f.error("derivation-reachability", f"{rp}: unexpected reachability axis/entries {extra!r}")
    if len(reach) != 4:
        f.error("derivation-reachability",
                f"{rp}: reachability must declare exactly the 4 gate (ix)(a) combinations, "
                f"got {len(reach)}")


def check_avatar_state_derivation_table(f: Findings) -> None:
    """P1 (adopt-avatar-client-lab-candidates task 4.3; design D3): machine-check the neutral
    avatar-state derivation table, fail-closed, mirroring check_capability_scenario_register.
    All rules fail closed:

    (i)   `outputs` == exactly the six FR-019 avatar states.
    (ii)  `inputs.media_states` == exactly the closed ten.
    (iii) every landed deterministic seed that DECLARES an avatar/presentation state resolves to
          that state under the table's precedence (R0..R6 evaluated over the seed's reduced/kernel
          fields). A seed declares a state via the table's `landed_seed_crosscheck` (the five
          worked seeds) or by carrying `expected.view_state.media_state` ∈ the six avatar states;
          every seed's precedence result must be one of the six (totality).
    (iv)  `reachability_named_combinations` == exactly the gate (ix)(a) set the table declares.
    (v)   invariant-contradiction rows fail closed: `media_state_map` must map control_lost and
          control_degraded to `blocked`, and precedence R1's output must be `blocked` (INV-1).
    (vi)  absent table => skipped (pre-landing compat); present-but-malformed => error.

    Guarded on the table's presence so a checkout without it stays green.
    """
    if not DERIV_TABLE_YAML.is_file():
        return
    rp = str(DERIV_TABLE_YAML.relative_to(ROOT))
    try:
        doc = load_yaml(DERIV_TABLE_YAML)
    except yaml.YAMLError as exc:
        f.error("derivation-malformed", f"{rp}: unparseable YAML: {exc}")
        return
    if not isinstance(doc, dict):
        f.error("derivation-malformed", f"{rp}: top-level mapping required")
        return
    if doc.get("schema_version") is None:
        f.error("derivation-meta", f"{rp}: missing schema_version")
    if doc.get("kind") != DERIV_TABLE_KIND:
        f.error("derivation-meta", f"{rp}: kind must be {DERIV_TABLE_KIND!r}")

    # (i) outputs == the six FR-019 states.
    outputs = doc.get("outputs")
    if (not isinstance(outputs, list) or set(outputs) != DERIV_STATES
            or len(outputs) != len(DERIV_STATES)):
        f.error("derivation-outputs",
                f"{rp}: outputs must be exactly the six FR-019 states "
                f"{sorted(DERIV_STATES)}, got {outputs!r}")

    # (ii) media_states axis == the closed ten.
    inputs = doc.get("inputs")
    media_states = inputs.get("media_states") if isinstance(inputs, dict) else None
    if (not isinstance(media_states, list) or set(media_states) != DERIV_MEDIA_STATES
            or len(media_states) != len(DERIV_MEDIA_STATES)):
        f.error("derivation-media-states",
                f"{rp}: inputs.media_states must be exactly the closed ten "
                f"{sorted(DERIV_MEDIA_STATES)}, got {media_states!r}")

    # (v) invariant-contradiction rows fail closed (INV-1): control loss => blocked.
    media_state_map = doc.get("media_state_map")
    if not isinstance(media_state_map, dict):
        f.error("derivation-malformed", f"{rp}: media_state_map mapping required")
        media_state_map = {}
    for cstate in ("control_lost", "control_degraded"):
        if media_state_map.get(cstate) not in (None, "blocked"):
            f.error("derivation-invariant",
                    f"{rp}: media_state_map[{cstate}] must be `blocked` (INV-1), "
                    f"got {media_state_map.get(cstate)!r}")
    prec = doc.get("precedence") or []
    r1 = next((p for p in prec if isinstance(p, dict) and p.get("id") == "R1"), None)
    if r1 is None:
        f.error("derivation-malformed",
                f"{rp}: precedence rule R1 (control-health safety trip) missing")
    elif r1.get("output") != "blocked":
        f.error("derivation-invariant",
                f"{rp}: precedence R1 output must be `blocked` (INV-1), got {r1.get('output')!r}")

    # (iv) reachability_named_combinations == the gate (ix)(a) set.
    reach = doc.get("reachability_named_combinations")
    if not isinstance(reach, list):
        f.error("derivation-malformed", f"{rp}: reachability_named_combinations list required")
    else:
        _check_derivation_reachability(f, rp, reach)

    # (iii) seed resolution over the table's precedence.
    crosscheck: dict[str, Any] = {}
    for c in (doc.get("landed_seed_crosscheck") or []):
        if isinstance(c, dict) and c.get("seed"):
            d = c.get("derived")
            crosscheck[c["seed"]] = d[-1] if isinstance(d, list) and d else d
    if DERIV_SEEDS_DIR.is_dir():
        for path in sorted(DERIV_SEEDS_DIR.glob("*.yaml")):
            try:
                seed = load_yaml(path) or {}
            except yaml.YAMLError as exc:
                f.error("derivation-seed", f"{path.name}: unparseable seed YAML: {exc}")
                continue
            expected = seed.get("expected") if isinstance(seed.get("expected"), dict) else {}
            canonical = seed.get("canonical") if isinstance(seed.get("canonical"), dict) else {}
            view_state = expected.get("view_state") if isinstance(expected.get("view_state"), dict) else {}
            snapshot = canonical.get("snapshot") if isinstance(canonical.get("snapshot"), dict) else {}
            if not isinstance(view_state, dict) or not isinstance(snapshot, dict):
                continue
            derived = _derive_avatar_state(view_state, snapshot, media_state_map)
            # Totality: the precedence must resolve to one of the six states for EVERY seed.
            if derived not in DERIV_STATES:
                f.error("derivation-seed",
                        f"{path.name}: table precedence resolved to {derived!r}, not one of the "
                        f"six avatar states")
                continue
            declared = crosscheck.get(path.name)
            if declared is None and view_state.get("media_state") in DERIV_STATES:
                declared = view_state["media_state"]
            if declared is not None and derived != declared:
                f.error("derivation-seed",
                        f"{path.name}: table precedence derives {derived!r} but the seed declares "
                        f"{declared!r}")


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
    sentinel_entries = (load_yaml(sentinels_path).get("sentinels") or [])
    sentinels = {s["bounded_form"] for s in sentinel_entries}
    # structural sanity: a sentinel must be an obviously-fake bounded form that
    # cannot widen into a real secret — EITHER the reserved SENTINEL_ prefix
    # (credential/SDP and prefix-compatible identifier forms) OR, for
    # high-cardinality identifier classes whose pattern cannot carry that prefix,
    # one of these documented reserved/invalid canonical values that can never be
    # a real identifier (RFC 4122 nil UUID; an unassignable NANP number).
    RESERVED_INVALID_IDS = {
        "00000000-0000-0000-0000-000000000000",  # RFC 4122 nil UUID
        "000-000-0000",                           # unassignable NANP number
    }
    for s in sentinel_entries:
        bf = s.get("bounded_form", "")
        max_len = int(s.get("max_len", 0) or 0)
        prefixed_ok = bf.startswith("SENTINEL_") and len(bf) <= max_len
        reserved_ok = (s.get("form") == "reserved_invalid"
                       and bf in RESERVED_INVALID_IDS and len(bf) <= max_len)
        if not (prefixed_ok or reserved_ok):
            f.error("sentinel", f"sentinel {s.get('id')} is not a bounded SENTINEL_ form "
                    f"or documented reserved-invalid identifier within max_len")
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


def check_digests(f: Findings, require_realization: bool = False) -> None:
    """US3 (T036): per-file SHA-256 over the semantic consumed set + manifest/digest
    identity. The real contracts/manifest.yaml entries are authored at realization
    (T046); until then the digest set is computed and reported (A6). At realization
    the manifest digests must match the computed set (SCO-001-S02/S03).

    Successor deferral-discharge registers (decision 7) join the digested semantic
    surface via SEMANTIC_GLOBS, but — following the release-time manifest convention
    (the 005/v1.9 pattern: bundle members are registered in contracts/manifest.yaml
    only when the next additive contract version is cut, not mid-change) — a
    successor register is manifest-registered at THIS change's release realization,
    not when it is authored. So an unregistered successor register is DEFERRED to a
    note pre-realization and fails closed (`digest-missing`) under
    ``--require-realization``. A successor register that IS listed still has its
    digest verified. The released register and every other semantic file must be
    registered unconditionally."""
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
            if _is_successor_register(Path(path).name):
                msg = (f"{path} not yet registered in contracts/manifest.yaml; "
                       f"successor deferral-discharge registers are content-addressed "
                       f"at this change's release realization (release-time convention)")
                if require_realization:
                    f.error("digest-missing", msg)
                else:
                    f.note(msg)
                continue
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


def _resolve_f0_dir(pin: dict) -> Path:
    """The pinned F0 change directory, following it into the archive once the
    owning change archives (issue #30, option C). The pin's path stays
    authoritative: the fallback fires only when the live directory is gone,
    and only on an UNAMBIGUOUS dated-archive match — zero or several matches
    return the absent pinned path so every dimension downstream resolves
    False and the gate stays BLOCKED. The schema digests and source_commit
    pins still verify the bytes wherever the directory is found."""
    pinned = ROOT / (pin.get("f0_change_path") or "")
    if pinned.is_dir():
        return pinned
    if pinned.name:
        matches = sorted((ROOT / "openspec" / "changes" / "archive").glob(f"*-{pinned.name}"))
        if len(matches) == 1 and matches[0].is_dir():
            return matches[0]
    return pinned


def _f0_member_bytes(f0_dir: Path, rel: str) -> bytes | None:
    """Bytes of a pinned F0 artifact: the loose file, or — in a packaged
    archive, where proposal-support tarballs supporting-docs/ on archive —
    the identically named member of supporting-docs.tar.gz. Missing, unsafe,
    or unreadable resolves None so every gate dimension downstream stays
    False and the gate stays BLOCKED."""
    if not rel:
        return None
    loose = f0_dir / rel
    if loose.is_file():
        return loose.read_bytes()
    parts = PurePosixPath(rel).parts
    if len(parts) < 2 or parts[0] != "supporting-docs":
        return None
    bundle = f0_dir / "supporting-docs.tar.gz"
    if not bundle.is_file():
        return None
    member = "/".join(parts[1:])
    try:
        with tarfile.open(bundle, "r:gz") as archive:
            info = archive.getmember(member)
            if not info.isfile():
                return None
            stream = archive.extractfile(info)
            return stream.read() if stream is not None else None
    except (tarfile.TarError, KeyError, OSError):
        return None


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
    f0_dir = _resolve_f0_dir(pin)
    rs_bytes = _f0_member_bytes(f0_dir, pin.get("f0_results_schema") or "")
    iis_bytes = _f0_member_bytes(f0_dir, pin.get("f0_interface_impact_schema") or "")
    schema_present = rs_bytes is not None and iis_bytes is not None

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
            r_schema = yaml.safe_load(rs_bytes.decode("utf-8"))
            i_schema = yaml.safe_load(iis_bytes.decode("utf-8"))
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
        # The F0 result record's terminal field is `overall` (f0-results.schema); accept the
        # legacy `status`/`f0_status` aliases too.
        status = (results_inst.get("overall") or results_inst.get("status")
                  or results_inst.get("f0_status"))

    state = {
        "schema_present": schema_present,
        "digest_match": schema_present
        and pin.get("f0_results_schema_sha256") == hashlib.sha256(rs_bytes).hexdigest()
        and pin.get("f0_interface_impact_schema_sha256") == hashlib.sha256(iis_bytes).hexdigest(),
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
