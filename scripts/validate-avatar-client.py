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

# ---- The published AVC contracts + reserved identifiers (spec FR-001/FR-002) ----
# AVC-09 and AVC-10 joined this map in `qualify-avatar-live-voice`, in the SAME
# change that lands their schemas. They had to move together: the reserved-id
# guard in check_schemas fail-closes on the mere EXISTENCE of an
# `avc-09-*.schema.yaml` file, so a schema landing one commit ahead of this
# constant would red the repository between commits. AVC-03 and AVC-05 stay
# reserved, and check_interface_lock now machine-checks both of these constants
# against interface-lock.yaml so the hand-mirroring cannot drift again.
CONTRACT_FILES = {
    "AVC-01": "avc-01-session-request.schema.yaml",
    "AVC-02": "avc-02-session-result.schema.yaml",
    "AVC-04": "avc-04-session-event.schema.yaml",
    "AVC-06": "avc-06-structured-confirmation.schema.yaml",
    "AVC-07": "avc-07-retention-profile.schema.yaml",
    "AVC-08": "avc-08-persona-profile.schema.yaml",
    "AVC-09": "avc-09-voice-adapter-descriptor.schema.yaml",
    "AVC-10": "avc-10-voice-latency-sample.schema.yaml",
    "AVC-11": "avc-11-session-command.schema.yaml",
    "AVC-12": "avc-12-state-snapshot.schema.yaml",
}
RESERVED_IDS = {"AVC-03", "AVC-05"}

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


class MalformedYAML(yaml.YAMLError):
    """A YAML file the validator must read does not PARSE.

    Deliberately a subclass of `yaml.YAMLError`: several readers here already
    catch `yaml.YAMLError` to fail closed on their own (`_load_f0_instance`
    among them), and those handlers must keep working exactly as before.
    Subclassing means this carries the file's identity to the top of the run
    without changing the behaviour of a single existing `except`."""

    def __init__(self, path: Path, exc: Exception) -> None:
        self.path = path
        self.original = exc
        # The message stays the parser's own. The existing handlers already
        # format their finding as `{relative path}: {exc}`, so prefixing the
        # path here would print it twice; `run()` names the file from `.path`
        # instead.
        super().__init__(str(exc))


def load_yaml(path: Path) -> Any:
    """Parse one YAML document, naming the file when it does not parse.

    Every reader in this validator funnels through here, so a syntax error
    anywhere becomes one identifiable, catchable failure rather than a bare
    `yaml.scanner.ScannerError` escaping to `main()` as an anonymous harness
    failure. `run()` turns it into a finding; the readers that already fail
    closed on a YAMLError keep doing so untouched."""
    with path.open(encoding="utf-8") as fh:
        try:
            return yaml.safe_load(fh)
        except MalformedYAML:
            raise
        except yaml.YAMLError as exc:
            raise MalformedYAML(path, exc) from exc


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
                    f.error("meta", f"{rel}: contract_id must be one of the "
                                    f"{len(CONTRACT_FILES)} published AVC ids "
                                    f"{sorted(CONTRACT_FILES)}")
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
    # every published contract present?
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

def _report(f: Findings, strict: bool) -> int:
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


def _rel(path: Path) -> str:
    """Repository-relative path for a finding, falling back to the absolute one."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run(strict: bool, require_realization: bool) -> int:
    f = Findings()
    if not AVC.is_dir():
        print("ERROR contracts/avatar-client/ not found", file=sys.stderr)
        return 2

    # A YAML SYNTAX ERROR IS A FINDING, NOT A TRACEBACK — caught once, here.
    # Every reader funnels through `load_yaml`, which names the offending file
    # and raises `MalformedYAML`. Before this, an unparseable document anywhere
    # in the family escaped to `main()` as an anonymous `ERROR harness failure`
    # with exit 2, which told a reader that the tool broke rather than that
    # their file did. Catching per-site would be 31 call sites today and one
    # more each time a reader is added, so it is caught at the boundary
    # instead. Fail closed: whatever had been collected is reported alongside
    # the parse failure, and the run stops.
    try:
        return _run_checks(f, strict, require_realization)
    except MalformedYAML as bad:
        f.error("yaml-syntax",
                f"{_rel(bad.path)} does not parse as YAML "
                f"({type(bad.original).__name__}); nothing that reads it can be "
                f"verified (fail closed) — {bad.original}")
        return _report(f, strict)


def _run_checks(f: Findings, strict: bool, require_realization: bool) -> int:
    # FAIL CLOSED ON A STRUCTURALLY UNREADABLE ACCEPTANCE MAP, ONCE, HERE.
    # A top-level list is valid YAML and a malformed acceptance map, and a
    # dozen readers below index it as a mapping. Each of those raised in turn,
    # which surfaced as `ERROR harness failure: 'list' object has no attribute
    # 'get'` and exit 2 — a crash, not a finding, and it aborted the run before
    # any check could report. Guarding each reader separately would be
    # whack-a-mole and would leave the next reader to be added exposed, so the
    # shape is refused once, up front. Every downstream check is meaningless
    # against a map that cannot be indexed, so this returns rather than
    # continuing on a document nothing can read.
    amap_path = AVC / "acceptance-map.yaml"
    if amap_path.is_file() and not isinstance(load_yaml(amap_path), dict):
        f.error("acceptance-map",
                "contracts/avatar-client/acceptance-map.yaml does not load as a "
                "mapping; requirement and scenario traceability, the latency "
                "posture, and every cross-reference resolved against it are "
                "unverifiable (fail closed)")
        return _report(f, strict)

    check_metadata(f)
    registry, docs = build_registry(f)
    check_schemas(f, registry, docs)
    check_registries(f, docs)
    check_speech_gate(f, docs)
    # Fixture / acceptance / evidence / redaction / digest / F0-gate checks are
    # added in later phases; each guards on artifact presence so the validator
    # stays green at every phase checkpoint.
    check_interface_lock(f)
    # qualify-avatar-live-voice §4.1 and §6.3.1-§6.3.2: the ratified rulings are
    # written down by hand in two governance artifacts beside the acceptance
    # map, so they are machine-compared against this validator's constants for
    # the same reason the frozen identifier lists are.
    check_activation_checklist(f)
    check_canary_rollback_policy(f)
    # The six §7 authoring inputs ruled 2026-08-27 land in three artifacts. The
    # canary policy's share is checked inside the policy check above (its exit
    # criteria and the ROLLBACK-B/C trip points); these two carry the rest.
    check_latency_sample_minimum(f)
    check_broker_credential_binding(f)
    # §6.2 (Fork 4 Option C): the synthetic evaluation corpus and the canary's
    # ephemeral processing envelope. Both guard on presence, and both read the
    # values another artifact already ratified — ROLLBACK-A's triggers, the
    # frozen purposes, the reserved retention classes, §7.9's retention window
    # — rather than mirroring them into a second copy that can drift.
    check_synthetic_evaluation_corpus(f)
    check_ephemeral_processing_envelope(f)
    ev_ids = check_fixtures(f, registry, docs)
    # The latency comparison cases carry acceptance evidence exactly as the
    # fixtures do, so their ids join the set the evidence register resolves
    # against; an automated entry may name either kind.
    ev_ids |= check_latency_posture(f)
    check_acceptance_and_evidence(f, ev_ids)
    check_client_lab_acceptance_map(f)
    check_capability_scenario_register(f)
    check_avatar_state_derivation_table(f)
    check_release_identity(f)
    check_content_addressed_pin(f)
    check_redaction(f)
    check_digests(f, require_realization)
    check_f0_gate(f, require_realization)

    return _report(f, strict)


ALL_CLASSES = {"valid", "invalid", "boundary", "compatibility",
               "unknown-field", "unknown-authority", "redaction", "adversarial"}
KNOWN_CHECKS = {"acceptance_map_parity", "contract_location", "release_identity",
                "content_addressed_pin", "fixture_conformance",
                # qualify-avatar-live-voice §3.1-§3.3
                "interface_lock_reserved_set", "latency_posture"}
EVID_TYPES = {"automated", "manual", "deferred"}

# ---- the two-tier latency posture (qualify-avatar-live-voice §3.3) ----------
# The SLO entry's shape, at the RATIFIED threshold. These are not defaults the
# map may override: the check compares the map's declared numbers against them
# and fails on a disagreement, because a threshold that can be edited in the
# artifact it gates is not a threshold.
SLO_KIND = "neutral_relative_regression"
SLO_RELATIVE_PCT = 15
SLO_ABSOLUTE_MS = 150
SLO_MATERIALITY_RULE = "greater_of"
SLO_GATED_PERCENTILES = {"p50", "p95"}
SLO_GATED_INTERVALS = {"first_playable_after_authorized_ms",
                       "sideband_ready_after_request_ms"}
SLO_GATED_PLATFORMS = {"windows_desktop", "web_canvas"}
SLO_GATED_NETWORK = "nominal"
SLO_REFERENCE_ONLY_PLATFORMS = {"linux_ci"}
SLO_CELL_AXES = ("platform", "network_class", "region")
SLO_OUTCOMES = {"pass", "fail", "recorded", "refused"}
# A per-profile numeric latency ceiling, however it is spelled. Fork 2's Option
# C means NO such field exists on a neutral contract and none is declared as a
# gating field in the acceptance map: the only numeric threshold in this family
# is the SLO's own `absolute_threshold_ms`, which is a RELATIVE-regression
# allowance, not a ceiling on a profile.
LATENCY_CEILING_KEY = re.compile(
    r"(?i)^(?:latency_budgets?|latency_budget_ms|latency_ceiling_ms"
    r"|max_latency_ms|[a-z0-9_]*_budget_ms|[a-z0-9_]*_latency_ceiling_ms)$"
)

# ---- the internal-live activation checklist (qualify-avatar-live-voice §4.1) --
# The RATIFIED per-condition classification, mirrored here so the checklist
# artifact and this validator are two independent statements of the same Fork 3
# Option C ruling — the same discipline `check_interface_lock` applies to the
# frozen identifier lists. A hand-copied ruling drifts; a hand-copied ruling
# that is machine-compared drifts LOUDLY.
CHECKLIST_FILE = "internal-live-activation-checklist.yaml"
CHECKLIST_KIND = "avatar-client-internal-live-activation-checklist"
CHECKLIST_CLASSES = {"hard_preflight", "canary_time", "default_swap_only"}
# Condition number -> the classification the ruling assigns it. `split` means
# the condition's two halves fall differently and BOTH must be recorded.
CHECKLIST_RULED = {
    1: "hard_preflight",
    2: "hard_preflight",
    3: "split",
    4: "hard_preflight",
    5: "split",
    6: "canary_time",
    7: "split",
    8: "split",
}
# For each split condition, the ruled classification of each named half. The
# half NAMES are part of the ruling too: a checklist that renamed a half could
# otherwise satisfy the count while silently reclassifying it.
CHECKLIST_RULED_HALVES = {
    3: {"topology": "hard_preflight",
        "measured_latency_figure": "canary_time"},
    5: {"deterministic_ui_scenarios": "hard_preflight",
        "live_domain_voice_evaluation": "canary_time"},
    7: {"deterministic_blocked_state_and_exact_value": "hard_preflight",
        "live_cross_domain_evaluations": "canary_time"},
    8: {"kill_switches_and_rollback_machinery": "hard_preflight",
        "opt_in_canary": "canary_time"},
}
CHECKLIST_RING_ELEMENTS = {
    "RING-01": "live_provider_qualification",
    "RING-02": "secret_scan",
    "RING-03": "telemetry_redaction_verification",
    "RING-04": "kill_switch_proof",
    "RING-05": "measured_latency_evidence",
}
# The kernel's ring is FOUR EVIDENCE ELEMENTS around live provider
# qualification, so RING-01 is the qualification and RING-02..05 are the four.
CHECKLIST_RING_EVIDENCE_COUNT = 4

# ---- the canary cohort and rollback policy (§6.3.1-§6.3.2) -----------------
POLICY_FILE = "canary-cohort-and-rollback-policy.yaml"
POLICY_KIND = "avatar-client-canary-cohort-and-rollback-policy"
# Fork 5 Option B's three-way split, as ratified. The revoke flag is the whole
# point of the policy — the kernel gives each kill switch an OPTIONAL
# active-lease revocation and this is the rule that selects the option — so it
# is compared explicitly rather than trusted.
# The ruled cohort is exactly one of EACH kind — vendor-organization internal
# accounts AND exactly one internally-staffed domain sandbox. Held as a set so
# the check can count per kind instead of trusting a total.
POLICY_COHORT_KINDS = {"vendor_organization_internal_accounts",
                       "internally_staffed_domain_sandbox"}
POLICY_RULED_CLASSES = {
    "ROLLBACK-A": {"trigger_mode": "automatic", "action": "abort",
                   "revoke_active_leases": True},
    "ROLLBACK-B": {"trigger_mode": "automatic", "action": "block_new",
                   "revoke_active_leases": False},
    "ROLLBACK-C": {"trigger_mode": "operator", "action": "operator_selected",
                   "revoke_active_leases": "operator_selected"},
}

# ---- the §7 authoring inputs, RULED 2026-08-27 ------------------------------
# §7 is the list of values "the rulings deliberately left to proposal and
# realization time", and its own preamble states the hazard: "leaving any unset
# opens the ring on an unstated assumption". Six of them are now ruled, and the
# artifacts that carry them are mirrored here for exactly the reason the
# checklist and the rollback split already are — a hand-copied ruling drifts,
# and a hand-copied ruling that is machine-compared drifts LOUDLY.
#
# §7.6 — the canary exit criteria. These moved `canary_exit_criteria` off
# `status: unset`, which that block's own statement said existed "so that a
# canary cannot be declared successful against criteria invented after the
# fact". Comparing the numbers is how that sentence stays true after the
# values land: a criterion that can be edited in the artifact it gates is not a
# criterion.
POLICY_EXIT_SOAK_DAYS = 14
POLICY_EXIT_DISTINCT_DAYS = 10
POLICY_EXIT_SESSIONS = 200
POLICY_EXIT_COHORT_02_MIN = 50
POLICY_EXIT_PER_SCENARIO_CLASS_MIN = 3
POLICY_EXIT_ABNORMAL_OVERALL_PCT = 2
POLICY_EXIT_ABNORMAL_TRAILING_PCT = 5
POLICY_EXIT_TRAILING_WINDOW_SESSIONS = 50
# The two criteria ruled BEYOND the three §7.6 names. Without them the ring's
# own stated rationale goes undelivered: RING-04 proves the kill SWITCH before
# any canary traffic, and nothing otherwise proves the DETECTION.
POLICY_EXIT_ADDITIONAL_IDS = {"EXIT-ROLLBACK-B-REHEARSED", "EXIT-ROLLBACK-A-CLEAR"}

# §7.2 — the numeric ceilings, at the two places the rollback policy consumes
# them. ROLLBACK-B carried three triggers and trip points for only one of them:
# `elevated_error_rate` named no rate and `elevated_quota_condition` named no
# quota, so an "auto-blocker" had nothing to auto-block on.
ROLLBACK_B_ERROR_TRAILING_PCT = 5
ROLLBACK_B_TRAILING_WINDOW_SESSIONS = 50
ROLLBACK_B_SESSION_SECONDS_MAX = 900
ROLLBACK_B_SESSION_UNITS_MAX = 300
ROLLBACK_B_PROJECT_CAP_USD = 750
ROLLBACK_C_TENANT_BUDGET_USD = 150

# §7.7 — the operator surface, RULED 2026-08-27. The artifact's own former
# statement was that "a canary opened without a named holder has an unfireable
# kill switch", so the rules here are the ones that keep the surface FIREABLE:
# a person rather than a role, a mechanism, and a runbook that RESOLVES. A
# `mechanism_ref` pointing at a document nobody wrote is the same unfireable
# switch wearing a filename.
POLICY_OPERATOR_HOLDER = "Brett Heap"
POLICY_OPERATOR_HOLDER_KIND = "named_person"
POLICY_OPERATOR_MECHANISM = "documented_runbook_act_on_the_serving_install"
POLICY_OPERATOR_RUNBOOK = "docs/sops/avatar-internal-live-kill-switch.md"
# The kernel's TWO switches and no more: "all new session creation, and per
# model profile — each with optional revocation of active leases". Finer scopes
# are deferred with the features they would govern, so a third scope recorded
# here is a switch the runtime does not have.
POLICY_SWITCH_SCOPES = {"all_new_session_creation", "per_model_profile"}
POLICY_SWITCH_MODES = {"block_new", "revoke_active"}

# §7.8 — the session-outcome token each rollback path emits. The ruling is that
# NO NEW TOKEN is introduced, so the tokens are resolved against the closed
# registry rather than mirrored here; what is mirrored is the PATH-TO-TOKEN
# ruling itself.
# The ONE registry §7.8's tokens may be drawn from, spelled as the artifact
# spells it in `session_outcome_tokens.registry_ref` — AVC-relative, so the two
# can be compared directly instead of one being reconstructed from the other.
OUTCOME_REGISTRY_REF = "registries/session-outcomes.registry.yaml"
POLICY_OUTCOME_PATHS = {
    "consent_or_lease_revocation": "revoked",
    "drained_leg_after_block_new": "abandoned",
    "force_terminated_leg": "revoked",
}
# The same fact carried twice on purpose — once on the class a reader lands on,
# once in the block that owns §7.8 — and therefore compared, exactly as the
# error rate is. `(outcome, path)` per class; ROLLBACK-C is operator-selected
# and names no single token.
POLICY_CLASS_OUTCOMES = {
    "ROLLBACK-A": ("revoked", "force_terminated_leg"),
    "ROLLBACK-B": ("abandoned", "drained_leg_after_block_new"),
}
POLICY_ROLLBACK_C_OUTCOME = "operator_selected"

# §7.10 — "tenant" for this ring. The per-tenant spend and metering dimensions
# have no subject without it, and §7.2's $150 was sized on this denominator.
POLICY_TENANT_IS = "cohort_member"

# §7.9 — the declared region, data-control classes and retention window, pinned
# on the activation checklist's condition 2 (the condition that APPROVES the
# regional, retention and data-control terms and already names §7.9 as an
# owning task). No AVC-09 descriptor instance exists yet; these are the values
# descriptor authoring consumes.
CHECKLIST_S79_CONDITION = 2
CHECKLIST_S79_REGION = "provider_project_us_default"
# Fork 4 Option C, exactly: captions and deltas ephemeral, decisions and
# outcomes structured. Held as an ORDERED-INSENSITIVE set and compared
# set-equal, because a class quietly ADDED is the failure mode here.
CHECKLIST_S79_DATA_CLASSES = {"ephemeral_presentation", "structured_record"}
# The three the ruling says are never instantiated in this ring. They are also
# three of the four RESERVED retention classes, which stay forbidden; the check
# compares the recorded list rather than trusting the prose beside it.
CHECKLIST_S79_NEVER = {"audio", "full_transcript", "independent_transcription"}
CHECKLIST_S79_RETENTION_DAYS = 90

# ---- §6.2, the canary's consent envelope and its synthetic corpus -----------
# Fork 4 Option C's two artifacts. They are checked here for the same reason
# the canary policy is: they are governance artifacts written by hand beside
# the acceptance map, and the values that matter in them are values another
# artifact already ratified. Wherever a value exists elsewhere it is READ from
# there — ROLLBACK-A's trigger vocabulary from the policy, the frozen purpose
# list from the registry, the reserved retention classes from the registry, the
# retention window and reference from the checklist's §7.9 block — so these
# constants are only the identifiers and the ruled shapes.
CORPUS_FILE = "synthetic-evaluation-corpus.yaml"
CORPUS_KIND = "avatar-client-synthetic-evaluation-corpus"
# Condition 7's five classes and three domains, exactly. Condition 7 says the
# evaluations must pass "for generic, MedxFactory and LedgerxFactory", so a
# corpus with a fourth domain or a missing class is not the corpus that
# condition names.
CORPUS_CLASSES = {"safety", "exact_value", "consent", "handoff", "blocked_state"}
CORPUS_DOMAINS = {"generic", "MedxFactory", "LedgerxFactory"}
ENVELOPE_FILE = "canary-ephemeral-processing-envelope.yaml"
ENVELOPE_KIND = "avatar-client-canary-ephemeral-processing-envelope"
ENVELOPE_MEDIA_PURPOSES = {"avatar.media_capture", "avatar.provider_processing"}
ENVELOPE_STRUCTURED_PURPOSE = "avatar.structured_record"
ENVELOPE_WITHDRAWAL_OUTCOME = "revoked"
ENVELOPE_SHADOW_CONTROL = "single_model_on_live_canary_audio"
ENVELOPE_PILOT_SUCCESSOR = "avatar-pilot-hardening"
# The fixture's IDENTITY is pinned; its PATH deliberately is not. The envelope
# carries the path in `withdrawal.reachability_proof.fixture` and the check
# resolves THAT, so the citation is what gets proved. Mirroring the location
# here as well would be the drift these checks exist to prevent: relocating the
# fixture would update the envelope and leave this constant behind, and the
# resulting failure would be about a stale copy rather than about the claim.
WITHDRAWAL_FIXTURE_ID = "det-consent-withdraw-mid-speech"

# ---- §7.5, the minimum sample count per gated cell (feeds §5.2) -------------
SAMPLE_MIN_FILE = "latency-sample-minimum.yaml"
SAMPLE_MIN_KIND = "avatar-client-latency-sample-minimum"
SAMPLE_MIN_N = 100
SAMPLE_MIN_RUNS = 3
SAMPLE_MIN_DISTINCT_DAYS = 2
SAMPLE_MIN_P99_FLOOR = 500
SAMPLE_MIN_UNDER_EFFECT = "recorded_not_gated"

# ---- §7.1 and §7.3, the broker server-key custody pair (task 6.1.1) ---------
BINDING_FILE = "broker-server-key-binding.template.yaml"
BINDING_KIND = "xfactory_credential_binding_template"
BINDING_ID = "avatar_broker_openai_internal_live"
# The published shape's own required set, plus `vault`. Mirrored so this check
# fails on a field the binding template DROPS as loudly as on one it mis-values.
BINDING_FIELDS = ("provider", "vault", "secret_ref", "owner", "rotation_policy")
# The two fields that MUST stay per-install placeholders in this repository.
BINDING_PLACEHOLDER_FIELDS = ("provider", "vault")
BINDING_SECRET_REF = "avatar-broker-openai-internal-live"
BINDING_ROTATION_LABEL = "operator_managed"
ROTATION_FILE = "broker-server-key-rotation-policy.yaml"
ROTATION_KIND = "xfactory_credential_rotation_policy"
ROTATION_MAX_KEY_AGE_DAYS = 90
ROTATION_GLOBAL_TRIGGERS = {"client_offboarding", "suspected_exposure",
                            "provider_policy_change", "privileged_scope_change"}
ROTATION_ADDED_TRIGGERS = {"avatar_platform_maintainer_change",
                           "canary_cohort_change", "release_ring_promotion"}
# THE CANON PROHIBITION, made mechanical. `credential-contracts` says
# "Contract artifacts, lane definitions, and domain repositories SHALL NOT
# hard-code a vault operator, a vault product, or any secret value." This
# repository IS a contract artifact tree, so the rule binds every value in the
# custody pair. The token list is the approved provider families from
# docs/credential-access-model.md plus the vault-naming prefixes the estate
# actually uses — the point is to catch the paste, not to enumerate the world.
#
# Matched against a SQUASHED form of each value — lowercased with every
# non-alphanumeric character removed — because a product name is the same
# product whether it is written `azure_key_vault`, `Azure Key Vault` or
# `azure-key-vault`, and a token list that only knows one spelling catches the
# careful paste and misses the careless one.
VAULT_PRODUCT_TOKENS = ("azurekeyvault", "keyvault", "awssecretsmanager",
                        "secretsmanager", "gcpsecretmanager", "secretmanager",
                        "1password", "bitwarden", "hashicorpvault",
                        "vaultazurenet")
# Vault INSTANCE names, matched raw against the lowercased value: these are
# naming conventions rather than words, and squashing them would turn `kv-`
# into a two-letter substring that fires on ordinary prose.
VAULT_INSTANCE_TOKENS = ("kv-", "vault.azure.net")
# A raw secret value pasted where a reference belongs — the same markers the
# credential-contracts validator refuses in a binding's `secret_ref`.
#
# WRITTEN LOWERCASE AND MATCHED AGAINST THE LOWERCASED VALUE, so a case-varied
# paste (`GHP_...`, `-----BEGIN`, `Akia...`) hits exactly as the canonical
# spelling does. A scan that only knows one casing catches the tidy paste and
# misses the careless one, which is the wrong way round.
#
# Deliberately NOT squashed the way `VAULT_PRODUCT_TOKENS` is. The
# normalization that is right for a product NAME is wrong for a key PREFIX,
# because a key prefix's separators ARE part of the marker: squashing would
# reduce `-----begin` to `begin` and `gho_` to `gho`, which fire on the
# ordinary words "beginning" and "ghost". A scan that cannot tell a key from
# prose is worse than no scan, because its findings get dismissed.
BINDING_SECRET_MARKERS = ("-----begin", "sk-proj-", "sk-svcacct-", "ghp_",
                          "github_pat_", "gho_", "ghs_", "akia")


def _acceptance_map_ids() -> set[str] | None:
    """Every requirement id, scenario id and SLO id the acceptance map declares.
    Used to resolve the cross-references the §4.1 and §6.3 artifacts carry, so a
    reference to a scenario that was renamed or never existed is a finding
    rather than a decoration.

    Returns an EMPTY SET when the map is simply absent (its own checks report
    that), and `None` when the file exists but does not load as a mapping. The
    distinction matters: a top-level list is valid YAML and a malformed
    acceptance map, and reading it as a mapping used to raise straight out of
    this helper — which aborted the whole run with a harness failure BEFORE any
    check could report anything. An unreadable map is a finding, fail closed,
    the same way every other reader in this file refuses one."""
    ids: set[str] = set()
    path = AVC / "acceptance-map.yaml"
    if not path.is_file():
        return ids
    amap = load_yaml(path)
    if not isinstance(amap, dict):
        return None
    for req in amap.get("requirements") or []:
        if not isinstance(req, dict):
            continue
        if req.get("id"):
            ids.add(req["id"])
        for sc in req.get("scenarios") or []:
            if isinstance(sc, dict) and sc.get("id"):
                ids.add(sc["id"])
    slo = amap.get("latency_slo")
    if isinstance(slo, dict) and slo.get("id"):
        ids.add(slo["id"])
    return ids


def _resolve_map_ids(f: Findings, cat: str, rp: str) -> set[str]:
    """`_acceptance_map_ids()` with its unreadable-map signal turned into a
    finding for the calling artifact. Returns an empty set afterwards so the
    caller's remaining checks still run — the refusal is recorded, and the run
    continues to report everything else rather than dying on the first bad
    file."""
    known = _acceptance_map_ids()
    if known is None:
        f.error(cat, f"{rp}: contracts/avatar-client/acceptance-map.yaml does not "
                     f"load as a mapping, so the cross-references this artifact "
                     f"carries cannot be resolved (fail closed)")
        return set()
    return known


def _check_map_refs(f: Findings, cat: str, where: str,
                    refs: Any, known: set[str]) -> None:
    """Every `acceptance_map_refs` entry must resolve. Skipped only when the map
    itself is missing or unreadable, which the caller already reports."""
    if refs is None or not known:
        return
    if not isinstance(refs, list):
        f.error(cat, f"{where}: acceptance_map_refs must be a list")
        return
    for r in refs:
        if r not in known:
            f.error(cat, f"{where}: acceptance_map_refs names {r!r}, which the "
                         f"acceptance map does not declare")


def check_activation_checklist(f: Findings) -> None:
    """§4.1: machine-check the internal-live activation checklist against the
    ratified Fork 3 Option C classification.

    The artifact records a RULING, and a ruling written down by hand is exactly
    the kind of thing that drifts when someone later "tidies" it. Four
    obligations:

    1. THE EIGHT ARE ALL THERE, numbered 1..8, no gaps and no duplicates. Seven
       conditions is a checklist someone edited; nine is one someone extended.
    2. EVERY CLASSIFICATION MATCHES THE RULING, including the per-half
       classification of the four split conditions and the half NAMES. A split
       recorded as a single class is the specific error that would let a live
       evaluation pass as a deterministic preflight one.
    3. CONDITION 6 IS RECORDED IN ITS REINTERPRETED FORM ONLY. The as-written
       comparative reading is reserved to the GPT-Live adoption change; if the
       artifact ever recorded it as a live second classification, the ring would
       be gated on a profile beating itself.
    4. THE RING IS FOUR EVIDENCE ELEMENTS AND THE GATE CONFERS NO DEFAULT. The
       exit contract cannot widen by editing this file, and the artifact may
       never say the gate promotes a profile to production.
    5. CONDITION 2 CARRIES §7.9's RULED VALUES. That condition is the one that
       APPROVES the regional, retention and data-control terms, it is HARD
       PREFLIGHT, and it already named §7.9 as an owning task — so the values
       descriptor authoring will consume live there, and are checked there.

    Fail closed on a missing or unreadable checklist: §4.1 lands it, and a ring
    whose classification cannot be read is not a classified ring."""
    path = AVC / CHECKLIST_FILE
    rp = f"contracts/avatar-client/{CHECKLIST_FILE}"
    cat = "activation-checklist"
    if not path.is_file():
        f.error(cat, f"{rp} absent; the internal-live per-condition "
                     f"classification is unverifiable (fail closed)")
        return
    doc = load_yaml(path) or {}
    if not isinstance(doc, dict):
        f.error(cat, f"{rp}: not a mapping (fail closed)")
        return
    if doc.get("schema_version") != 1:
        f.error(cat, f"{rp}: schema_version {doc.get('schema_version')!r} != 1")
    if doc.get("kind") != CHECKLIST_KIND:
        f.error(cat, f"{rp}: kind {doc.get('kind')!r} != {CHECKLIST_KIND!r}")

    known = _resolve_map_ids(f, cat, rp)

    # --- 1 + 2: the eight conditions and their ruled classifications ---
    conditions = doc.get("conditions")
    if not isinstance(conditions, list):
        f.error(cat, f"{rp}: `conditions` missing or not a list (fail closed)")
        return

    # SHAPE FIRST, AND STRICTLY. Every entry must be a mapping carrying an
    # INTEGER `number`, and the eight must be exactly 1..8 with none repeated.
    # This used to filter non-mappings and non-integers out of the completeness
    # scan, which was wrong twice over: a stray scalar in the list vanished
    # silently, and a ninth entry numbered "1" (a string) let the scan see a
    # clean 1..8 and then raised a KeyError in the loop below — a harness
    # failure that aborted the run instead of reporting a finding. A malformed
    # checklist is a finding, never a crash and never a silent skip.
    # `bool` is rejected explicitly because it subclasses `int` in Python, so
    # `number: true` would otherwise be accepted as 1.
    if len(conditions) != 8:
        f.error(cat, f"{rp}: `conditions` carries {len(conditions)} entries; the "
                     f"eight-condition checklist must carry exactly 8, because a "
                     f"missing condition reads as a satisfied one and an extra one "
                     f"is a condition nobody ratified")
        return
    numbers: list[int] = []
    shape_ok = True
    for i, cond in enumerate(conditions):
        if not isinstance(cond, dict):
            f.error(cat, f"{rp}: conditions[{i}] is a {type(cond).__name__}, not a "
                         f"mapping; a condition that is not a mapping cannot carry "
                         f"a classification and is never skipped over")
            shape_ok = False
            continue
        n = cond.get("number")
        if isinstance(n, bool) or not isinstance(n, int):
            f.error(cat, f"{rp}: conditions[{i}] has number {n!r} "
                         f"({type(n).__name__}); a condition number must be an "
                         f"integer 1..8")
            shape_ok = False
            continue
        numbers.append(n)
    if not shape_ok:
        return
    if sorted(numbers) != list(range(1, 9)):
        f.error(cat, f"{rp}: condition numbers {sorted(numbers)} are not exactly "
                     f"1..8 with each appearing once; the eight-condition checklist "
                     f"must carry all eight, because a missing condition reads as a "
                     f"satisfied one")
        return

    for cond in conditions:
        n = cond["number"]
        where = f"{rp} condition {n}"
        ruled = CHECKLIST_RULED[n]
        declared = cond.get("classification")
        _check_map_refs(f, cat, where, cond.get("acceptance_map_refs"), known)

        if ruled == "split":
            if declared != "split":
                f.error(cat, f"{where}: classification {declared!r} but the ruling "
                             f"splits this condition; both halves must be "
                             f"classified separately")
                continue
            if cond.get("split") is not True:
                f.error(cat, f"{where}: classification is 'split' but `split` is "
                             f"{cond.get('split')!r}")
            halves = cond.get("halves")
            if not isinstance(halves, list):
                f.error(cat, f"{where}: split condition carries no `halves` list")
                continue
            got = {}
            for h in halves:
                if not isinstance(h, dict):
                    continue
                got[h.get("half")] = h.get("classification")
                _check_map_refs(f, cat, f"{where} half {h.get('half')!r}",
                                h.get("acceptance_map_refs"), known)
            want = CHECKLIST_RULED_HALVES[n]
            if set(got) != set(want):
                f.error(cat, f"{where}: halves {sorted(got, key=str)} != the ruled "
                             f"halves {sorted(want)}")
            for half, want_cls in want.items():
                if half in got and got[half] != want_cls:
                    f.error(cat, f"{where} half {half!r}: classification "
                                 f"{got[half]!r} != the ruled {want_cls!r}")
            for half, cls in got.items():
                if cls not in CHECKLIST_CLASSES:
                    f.error(cat, f"{where} half {half!r}: classification {cls!r} is "
                                 f"not one of {sorted(CHECKLIST_CLASSES)}")
        else:
            if declared != ruled:
                f.error(cat, f"{where}: classification {declared!r} != the ruled "
                             f"{ruled!r}")
            if cond.get("split"):
                f.error(cat, f"{where}: recorded as split, but the ruling gives it "
                             f"a single classification")
            if cond.get("halves"):
                f.error(cat, f"{where}: carries `halves` but is not a split "
                             f"condition")

        # --- 3: condition 6 in its reinterpreted form ONLY ---
        if n == 6:
            if cond.get("recorded_form") != "reinterpreted_only":
                f.error(cat, f"{where}: recorded_form "
                             f"{cond.get('recorded_form')!r} != "
                             f"'reinterpreted_only'; task 4.1 records condition 6 "
                             f"in its reinterpreted form only")
            if cond.get("as_written_form_is_reserved") is not True:
                f.error(cat, f"{where}: as_written_form_is_reserved must be true — "
                             f"the comparative reading belongs to the GPT-Live "
                             f"adoption change, and applied here it would gate "
                             f"gpt-realtime-2.1 on beating itself")

    # --- 5: §7.9's ruled region, data-control and retention values ---
    _check_section_7_9_values(
        f, cat, rp,
        next((c for c in conditions if c["number"] == CHECKLIST_S79_CONDITION), {}))

    # --- 4: the ring is four evidence elements, and confers no default ---
    ring = doc.get("ring_elements")
    if not isinstance(ring, list):
        f.error(cat, f"{rp}: `ring_elements` missing or not a list (fail closed)")
    else:
        got = {}
        for e in ring:
            if not isinstance(e, dict):
                continue
            got[e.get("id")] = e.get("element")
            _check_map_refs(f, cat, f"{rp} {e.get('id')}",
                            e.get("acceptance_map_refs"), known)
        if got != CHECKLIST_RING_ELEMENTS:
            f.error(cat, f"{rp}: ring elements {sorted(got.items(), key=str)} != "
                         f"the kernel's ring {sorted(CHECKLIST_RING_ELEMENTS.items())} "
                         f"— the binding exit contract is the four-element ring and "
                         f"nothing wider")
        if doc.get("ring_evidence_element_count") != CHECKLIST_RING_EVIDENCE_COUNT:
            f.error(cat, f"{rp}: ring_evidence_element_count "
                         f"{doc.get('ring_evidence_element_count')!r} != "
                         f"{CHECKLIST_RING_EVIDENCE_COUNT}")

    confers = doc.get("gate_confers")
    if not isinstance(confers, dict):
        f.error(cat, f"{rp}: `gate_confers` missing; the artifact must state that "
                     f"the gate confers no production default (latent decision 3)")
    else:
        if confers.get("production_default") is not False:
            f.error(cat, f"{rp}: gate_confers.production_default is "
                         f"{confers.get('production_default')!r}; passing this gate "
                         f"confers a SELECTABLE internal-live profile and NO "
                         f"production default")
        if confers.get("selectable_internal_live_profile") is not True:
            f.error(cat, f"{rp}: gate_confers.selectable_internal_live_profile must "
                         f"be true")
        _check_map_refs(f, cat, f"{rp} gate_confers",
                        confers.get("acceptance_map_refs"), known)


def _check_section_7_9_values(f: Findings, cat: str, rp: str, cond: dict) -> None:
    """§7.9: the declared region, data-control classes and retention window,
    RULED 2026-08-27 and pinned on activation-checklist condition 2.

    THE DESCRIPTOR DOES NOT EXIST YET, and that is the reason these rules
    matter rather than a reason to skip them. AVC-09's `region_and_data_controls`
    is the single home for the values; the adapter is unbuilt and task 6.1.2 has
    not provisioned the serving install, so what is pinned is what the descriptor
    SHALL declare when it is authored. An authoring input that is not checked is
    an authoring input the author gets to re-decide.

    The rule with real teeth is the data-control set comparison. Fork 4 Option C
    permits EXACTLY two classes for canary audio, and the hazard is a class
    quietly ADDED — `audio` or `full_transcript` appearing here would unreserve
    by editing a checklist what the kernel says only a successor change may
    unreserve. So the permitted classes are compared set-equal and the
    never-instantiated list is compared set-equal too, rather than either being
    spot-checked or trusted to the prose beside it."""
    vals = cond.get("ruled_values") if isinstance(cond, dict) else None
    if not isinstance(vals, dict):
        f.error(cat, f"{rp} condition {CHECKLIST_S79_CONDITION}: no `ruled_values` "
                     f"block (fail closed); §7.9's region, data-control and retention "
                     f"values are a HARD PREFLIGHT term of this condition, and an "
                     f"unpinned authoring input opens the ring on an unstated "
                     f"assumption")
        return
    if vals.get("status") != "ruled":
        f.error(cat, f"{rp} §7.9: ruled_values.status is {vals.get('status')!r} != "
                     f"'ruled'")

    region = vals.get("region") or {}
    if region.get("declared_region") != CHECKLIST_S79_REGION:
        f.error(cat, f"{rp} §7.9: region.declared_region is "
                     f"{region.get('declared_region')!r} != the ruled "
                     f"{CHECKLIST_S79_REGION!r}")
    # HONESTY IS THE RULING, not a footnote to it. F0 recorded `region: null`
    # and the provider project is unprovisioned, so a descriptor claiming a
    # pinned region the project does not enforce would be false in the one field
    # the ring points at for locality.
    if region.get("declare_honestly") is not True:
        f.error(cat, f"{rp} §7.9: region.declare_honestly is "
                     f"{region.get('declare_honestly')!r}; the ruled value is the "
                     f"provider project's default DECLARED HONESTLY, not a residency "
                     f"guarantee the project does not enforce")

    dc = vals.get("data_control") or {}
    permitted = set(dc.get("classes_permitted") or [])
    if permitted != CHECKLIST_S79_DATA_CLASSES:
        f.error(cat, f"{rp} §7.9: data_control.classes_permitted "
                     f"{sorted(permitted, key=str)} != the Fork 4 Option C classes "
                     f"{sorted(CHECKLIST_S79_DATA_CLASSES)}; a class added here "
                     f"unreserves by checklist edit what the kernel says only a "
                     f"successor change may unreserve")
    never = set(dc.get("classes_never_instantiated") or [])
    if never != CHECKLIST_S79_NEVER:
        f.error(cat, f"{rp} §7.9: data_control.classes_never_instantiated "
                     f"{sorted(never, key=str)} != {sorted(CHECKLIST_S79_NEVER)}; the "
                     f"ruling is that no such instance is EVER created in this ring")
    if permitted & CHECKLIST_S79_NEVER:
        f.error(cat, f"{rp} §7.9: data_control permits and forbids "
                     f"{sorted(permitted & CHECKLIST_S79_NEVER)} at once")
    if dc.get("reserved_classes_untouched") is not True:
        f.error(cat, f"{rp} §7.9: data_control.reserved_classes_untouched is "
                     f"{dc.get('reserved_classes_untouched')!r}; this change "
                     f"unreserves exactly AVC-09 and AVC-10 and no retention class")
    # NO SCHEMA FIELD FORBIDS A SECOND-MODEL SHADOW TODAY. Recording the
    # guarantee as enforced would be the false claim task 6.2.4 exists to refuse.
    if dc.get("enforcement") != "operational":
        f.error(cat, f"{rp} §7.9: data_control.enforcement is "
                     f"{dc.get('enforcement')!r} != 'operational'; no schema field "
                     f"forbids an out-of-class instance or a second-model shadow "
                     f"today, and claiming otherwise would be false (task 6.2.4)")

    ret = vals.get("retention") or {}
    if ret.get("window_days") != CHECKLIST_S79_RETENTION_DAYS:
        f.error(cat, f"{rp} §7.9: retention.window_days is "
                     f"{ret.get('window_days')!r} != the ruled "
                     f"{CHECKLIST_S79_RETENTION_DAYS}")
    if ret.get("applies_to") != "canary_derived_structured_record":
        f.error(cat, f"{rp} §7.9: retention.applies_to is "
                     f"{ret.get('applies_to')!r} != "
                     f"'canary_derived_structured_record'; the window is ruled for "
                     f"canary-derived structured records, not for the ring at large")
    # A WINDOW WITH NO POLICY REFERENCE IS AN INLINE DURATION. The kernel's
    # split is references-only: domains own the record, the descriptor cites it.
    if not ret.get("policy_ref"):
        f.error(cat, f"{rp} §7.9: retention names no `policy_ref`; the ruled window "
                     f"is carried by a NAMED DOMAIN-OWNED policy reference that the "
                     f"descriptor cites — a duration with no reference is the inline "
                     f"retention the kernel's reference-only split refuses")
    if ret.get("policy_owner") != "domain":
        f.error(cat, f"{rp} §7.9: retention.policy_owner is "
                     f"{ret.get('policy_owner')!r} != 'domain'; the retention record "
                     f"is domain-owned, as consent evidence already is")


def check_canary_rollback_policy(f: Findings) -> None:
    """§6.3.1-§6.3.2: machine-check the recorded revoke-versus-block policy.

    This is the document the kernel has referenced since it was written —
    "revoke affected active leases ACCORDING TO THE RECORDED POLICY" — and Fork
    5 recorded that it had never actually been written. Now that it exists, the
    part worth enforcing is the part that would be dangerous to get wrong:

    * THE THREE-WAY SPLIT AND ITS REVOKE FLAGS. Safety breaches revoke active
      leases; latency and error breaches block new sessions and let in-flight
      legs DRAIN; quality and cost are operator judgment. Flipping ROLLBACK-B's
      revoke flag to true would cut people off mid-conversation on a
      performance regression, and would spend on a latency problem the
      mechanism the kernel reserves for safety.
    * NO MODEL FALLBACK. `gpt-realtime-2.1` is the first qualified profile, so
      rollback can only disable voice into text or handoff. The constraint is
      task 6.3.4's and it binds this artifact's COPY as well as the later code.
    * AN ABORT ENDS MEDIA ONLY, and no real external tenant is admitted.

    Fail closed on a missing or unreadable policy."""
    path = AVC / POLICY_FILE
    rp = f"contracts/avatar-client/{POLICY_FILE}"
    cat = "canary-policy"
    if not path.is_file():
        f.error(cat, f"{rp} absent; the kernel's 'recorded policy' for kill-switch "
                     f"scope is unverifiable (fail closed)")
        return
    doc = load_yaml(path) or {}
    if not isinstance(doc, dict):
        f.error(cat, f"{rp}: not a mapping (fail closed)")
        return
    if doc.get("schema_version") != 1:
        f.error(cat, f"{rp}: schema_version {doc.get('schema_version')!r} != 1")
    if doc.get("kind") != POLICY_KIND:
        f.error(cat, f"{rp}: kind {doc.get('kind')!r} != {POLICY_KIND!r}")

    known = _resolve_map_ids(f, cat, rp)

    # --- the cohort ---
    cohort = doc.get("cohort")
    if not isinstance(cohort, dict):
        f.error(cat, f"{rp}: `cohort` missing (fail closed)")
    else:
        _check_map_refs(f, cat, f"{rp} cohort", cohort.get("acceptance_map_refs"), known)
        ext = cohort.get("external_tenants") or {}
        if ext.get("admitted") is not False:
            f.error(cat, f"{rp}: cohort.external_tenants.admitted is "
                         f"{ext.get('admitted')!r}; no real external tenant is "
                         f"admitted to the internal-live canary")
        opt = cohort.get("opt_in") or {}
        if opt.get("client_visible_toggle") is not False:
            f.error(cat, f"{rp}: cohort.opt_in.client_visible_toggle is "
                         f"{opt.get('client_visible_toggle')!r}; opt-in is "
                         f"server-side capability resolution, never a client toggle")
        if opt.get("mechanism") != "server_side_capability_resolution":
            f.error(cat, f"{rp}: cohort.opt_in.mechanism "
                         f"{opt.get('mechanism')!r} != "
                         f"'server_side_capability_resolution'")
        # EXACTLY ONE OF EACH KIND, counted per kind rather than in total.
        # A length-2 list plus an at-least-one sandbox test accepted TWO
        # sandboxes and NO vendor organization — a cohort of two domain
        # sandboxes and no vendor staff, which is a different ring than the one
        # ruled, passing a check meant to fix its boundary. Both kinds are
        # counted separately now, so neither can stand in for the other.
        members = cohort.get("members")
        if not isinstance(members, list):
            f.error(cat, f"{rp}: cohort.members missing or not a list (fail closed)")
        else:
            kinds = [m.get("member") for m in members if isinstance(m, dict)]
            non_mappings = len(members) - len(kinds)
            if non_mappings:
                f.error(cat, f"{rp}: cohort.members carries {non_mappings} entry/ies "
                             f"that are not mappings; a cohort member that cannot be "
                             f"read is never counted as present")
            for kind in POLICY_COHORT_KINDS:
                n = kinds.count(kind)
                if n != 1:
                    f.error(cat, f"{rp}: cohort.members carries {n} entries of kind "
                                 f"{kind!r}; the ruled cohort is EXACTLY ONE of each "
                                 f"— the vendor organization's internal accounts AND "
                                 f"exactly one internally-staffed domain sandbox")
            unexpected = sorted(set(kinds) - POLICY_COHORT_KINDS)
            if unexpected:
                f.error(cat, f"{rp}: cohort.members names unratified kind(s) "
                             f"{unexpected}; admitting a new kind of member widens "
                             f"the ring and needs a ruling")
            sandbox = [m for m in members if isinstance(m, dict)
                       and m.get("member") == "internally_staffed_domain_sandbox"]
            if len(sandbox) == 1 and sandbox[0].get("cardinality") != "exactly_one":
                f.error(cat, f"{rp}: the domain sandbox cardinality is "
                             f"{sandbox[0].get('cardinality')!r} != 'exactly_one'; "
                             f"a second sandbox widens the ring and needs a ruling")

    # --- the three-way rollback split ---
    pol = doc.get("rollback_policy")
    if not isinstance(pol, dict):
        f.error(cat, f"{rp}: `rollback_policy` missing (fail closed)")
    else:
        _check_map_refs(f, cat, f"{rp} rollback_policy",
                        pol.get("acceptance_map_refs"), known)
        classes = pol.get("classes")
        if not isinstance(classes, list):
            f.error(cat, f"{rp}: rollback_policy.classes missing or not a list")
        else:
            got = {c.get("id"): c for c in classes if isinstance(c, dict)}
            if set(got) != set(POLICY_RULED_CLASSES):
                f.error(cat, f"{rp}: rollback classes {sorted(got, key=str)} != the "
                             f"ratified three-way split "
                             f"{sorted(POLICY_RULED_CLASSES)}")
            for cid, want in POLICY_RULED_CLASSES.items():
                c = got.get(cid)
                if not isinstance(c, dict):
                    continue
                for key, wanted in want.items():
                    if c.get(key) != wanted:
                        f.error(cat, f"{rp} {cid}: {key} is {c.get(key)!r} != the "
                                     f"ratified {wanted!r}")
                _check_map_refs(f, cat, f"{rp} {cid}",
                                c.get("acceptance_map_refs"), known)

    # --- the rollback target: no model fallback ---
    tgt = doc.get("rollback_target")
    if not isinstance(tgt, dict):
        f.error(cat, f"{rp}: `rollback_target` missing (fail closed)")
    else:
        if tgt.get("model_fallback_exists") is not False:
            f.error(cat, f"{rp}: rollback_target.model_fallback_exists is "
                         f"{tgt.get('model_fallback_exists')!r}; gpt-realtime-2.1 is "
                         f"the FIRST qualified profile, so no model fallback exists "
                         f"and none may be implied")
        if tgt.get("target") != "disable_voice_to_text_or_human_handoff":
            f.error(cat, f"{rp}: rollback_target.target {tgt.get('target')!r} != "
                         f"'disable_voice_to_text_or_human_handoff'")
        _check_map_refs(f, cat, f"{rp} rollback_target",
                        tgt.get("acceptance_map_refs"), known)

    # --- an abort ends the media plane only ---
    scope = doc.get("abort_scope")
    if not isinstance(scope, dict):
        f.error(cat, f"{rp}: `abort_scope` missing (fail closed)")
    else:
        if scope.get("ends") != "media_plane_only":
            f.error(cat, f"{rp}: abort_scope.ends {scope.get('ends')!r} != "
                         f"'media_plane_only'; the authority-owned workflow "
                         f"projection survives every abort")
        survives = set(scope.get("survives") or [])
        want_survives = {"authority_owned_workflow_projection",
                         "policy_required_structured_records"}
        if survives != want_survives:
            f.error(cat, f"{rp}: abort_scope.survives {sorted(survives)} != "
                         f"{sorted(want_survives)}")
        _check_map_refs(f, cat, f"{rp} abort_scope",
                        scope.get("acceptance_map_refs"), known)

    _check_section_7_values(f, cat, rp, doc)


def _rollback_class(doc: Any, class_id: str) -> dict:
    """One rollback class by id, or an empty mapping. Re-read from the document
    rather than threaded down from the split check, so the §7 rules report even
    when the split itself is malformed — a policy with a broken class list still
    has trip points worth checking, and a check that silently skips is a check
    that is not there."""
    pol = doc.get("rollback_policy")
    if not isinstance(pol, dict):
        return {}
    for c in pol.get("classes") or []:
        if isinstance(c, dict) and c.get("id") == class_id:
            return c
    return {}


def _check_section_7_values(f: Findings, cat: str, rp: str, doc: Any) -> None:
    """§7.6's canary exit criteria and the §7.2 trip points ROLLBACK-B and
    ROLLBACK-C consume, RULED 2026-08-27.

    Three things here would be dangerous to get wrong, and each is a defect the
    artifact itself named before the values landed:

    * AN EXIT CRITERION INVENTED AFTER THE FACT. The block's own former
      statement said the three values were held open "so that a canary cannot
      be declared successful against criteria invented after the fact". Now
      that they are set, the way that sentence stays true is that they are
      compared against the ruling rather than read out of the file that the
      canary's own operator could edit.
    * A TRIGGER WITH NO TRIP POINT. ROLLBACK-B is an AUTOMATIC block-new class
      whose `elevated_error_rate` and `elevated_quota_condition` triggers named
      no number: an auto-blocker that cannot decide to fire is decoration. So
      EVERY trigger a class declares must resolve to a threshold, checked by
      set comparison rather than by spot-checking the ones we remember.
    * TWO NUMBERS FOR ONE FACT. The canary's trailing-window tolerated error
      rate and ROLLBACK-B's `elevated_error_rate` are the SAME number by
      ruling. Ruled apart, the canary could pass its exit criterion while its
      auto-blocker was tripping, or the reverse. They are compared to each
      other, not merely each to a constant, so a future edit that moves both
      consistently still has to move them to the ruled value — and one that
      moves only one fails on both rules at once.

    §7.7, §7.8 and §7.10 were ruled the same day and close the three gaps this
    artifact recorded against itself, each with the same shape of hazard:

    * AN UNFIREABLE KILL SWITCH. `operator_surface` said of itself that "a
      canary opened without a named holder has an unfireable kill switch". A
      holder recorded as a ROLE, or a `mechanism_ref` naming a runbook nobody
      wrote, is that same unfireable switch with a value in the field — so the
      holder must be a named person and the runbook must RESOLVE ON DISK.
    * AN OUTCOME TOKEN INFERRED AFTER THE FACT. The block required the outcome
      "DECLARED IN ADVANCE rather than inferred", and the ruling introduces NO
      new token. Both halves are checked: the path-to-token mapping against the
      ruling, and every token against the closed `session-outcomes` REGISTRY
      rather than against a list mirrored here — a mirrored list would let the
      registry shrink underneath a policy still naming a member of it. The
      token is also carried on the rollback class itself and compared, for the
      same reason the error rate is.
    * A BUDGET WITH NO SUBJECT. The per-tenant figure is metered against a
      "tenant" that was `status: unset`. Tenant is now a cohort member, and the
      recorded `tenant_count` is RECOMPUTED from `cohort.members` rather than
      trusted — a count that outlives the membership it summarises is exactly
      how a re-sized budget goes unnoticed.
    """
    exit_criteria = doc.get("canary_exit_criteria")
    if not isinstance(exit_criteria, dict):
        f.error(cat, f"{rp}: `canary_exit_criteria` missing (fail closed); §7.6's "
                     f"soak duration, session count and tolerated error rate are "
                     f"the canary's exit contract")
        exit_criteria = {}
    elif exit_criteria.get("status") != "ruled":
        f.error(cat, f"{rp}: canary_exit_criteria.status is "
                     f"{exit_criteria.get('status')!r} != 'ruled'; §7.6 was ruled "
                     f"2026-08-27 and a canary opened against unset criteria can be "
                     f"declared successful against criteria invented after the fact")

    soak = exit_criteria.get("soak_duration") or {}
    for key, want in (("consecutive_calendar_days", POLICY_EXIT_SOAK_DAYS),
                      ("sessions_on_distinct_days_min", POLICY_EXIT_DISTINCT_DAYS)):
        if soak.get(key) != want:
            f.error(cat, f"{rp}: canary_exit_criteria.soak_duration.{key} is "
                         f"{soak.get(key)!r} != the ruled {want}")

    sessions = exit_criteria.get("minimum_session_count") or {}
    if sessions.get("completed_sessions") != POLICY_EXIT_SESSIONS:
        f.error(cat, f"{rp}: canary_exit_criteria.minimum_session_count."
                     f"completed_sessions is {sessions.get('completed_sessions')!r} "
                     f"!= the ruled {POLICY_EXIT_SESSIONS}; the count is set by "
                     f"MEASURABILITY — at n=50 a single failure is already 2 percent, "
                     f"so the tolerated rate could not be evaluated at all")
    floors = sessions.get("sub_floors") or {}
    for key, want in (("cohort_02_domain_sandbox_min", POLICY_EXIT_COHORT_02_MIN),
                      ("per_evaluation_scenario_class_min",
                       POLICY_EXIT_PER_SCENARIO_CLASS_MIN)):
        if floors.get(key) != want:
            f.error(cat, f"{rp}: canary_exit_criteria.minimum_session_count."
                         f"sub_floors.{key} is {floors.get(key)!r} != the ruled "
                         f"{want}; without the floors, 199 vendor-org sessions and "
                         f"one sandbox session would technically satisfy the count")

    rate = exit_criteria.get("tolerated_error_rate") or {}
    for key, want in (("abnormal_rate_overall_max_pct",
                       POLICY_EXIT_ABNORMAL_OVERALL_PCT),
                      ("abnormal_rate_trailing_window_max_pct",
                       POLICY_EXIT_ABNORMAL_TRAILING_PCT),
                      ("trailing_window_sessions",
                       POLICY_EXIT_TRAILING_WINDOW_SESSIONS)):
        if rate.get(key) != want:
            f.error(cat, f"{rp}: canary_exit_criteria.tolerated_error_rate.{key} is "
                         f"{rate.get(key)!r} != the ruled {want}")
    if not rate.get("abnormal_definition"):
        f.error(cat, f"{rp}: canary_exit_criteria.tolerated_error_rate carries no "
                     f"`abnormal_definition`; a rate whose numerator is undefined is "
                     f"unfalsifiable, and this ring deliberately produces "
                     f"abnormal-looking terminals (consent drills, injected rollback "
                     f"rehearsals, operator-fired ROLLBACK-C)")

    got_additional = {a.get("id") for a in exit_criteria.get("additional_criteria") or []
                      if isinstance(a, dict)}
    if got_additional != POLICY_EXIT_ADDITIONAL_IDS:
        f.error(cat, f"{rp}: canary_exit_criteria.additional_criteria "
                     f"{sorted(got_additional, key=str)} != the ruled "
                     f"{sorted(POLICY_EXIT_ADDITIONAL_IDS)}; RING-04 proves the kill "
                     f"SWITCH before any canary traffic and nothing else proves the "
                     f"DETECTION, which is what Option B was chosen for")

    # --- every declared trigger resolves to a trip point ---
    rb = _rollback_class(doc, "ROLLBACK-B")
    thresholds = rb.get("trigger_thresholds")
    if not isinstance(thresholds, dict):
        f.error(cat, f"{rp} ROLLBACK-B: `trigger_thresholds` missing (fail closed); "
                     f"an AUTOMATIC block-new class whose triggers carry no numbers "
                     f"cannot decide to fire")
        thresholds = {}
    declared = {t for t in rb.get("triggers") or [] if isinstance(t, str)}
    missing = sorted(declared - set(thresholds))
    if missing:
        f.error(cat, f"{rp} ROLLBACK-B: trigger(s) {missing} declare no trip point; "
                     f"every automatic trigger resolves to a threshold or the class "
                     f"is decoration")
    extra = sorted(set(thresholds) - declared)
    if extra:
        f.error(cat, f"{rp} ROLLBACK-B: trip point(s) {extra} name no declared "
                     f"trigger; a threshold nothing fires on is a number with no "
                     f"reader")

    err = thresholds.get("elevated_error_rate") or {}
    if err.get("abnormal_rate_trailing_window_max_pct") != ROLLBACK_B_ERROR_TRAILING_PCT:
        f.error(cat, f"{rp} ROLLBACK-B: elevated_error_rate trailing-window rate is "
                     f"{err.get('abnormal_rate_trailing_window_max_pct')!r} != the "
                     f"ruled {ROLLBACK_B_ERROR_TRAILING_PCT} percent")
    if err.get("trailing_window_sessions") != ROLLBACK_B_TRAILING_WINDOW_SESSIONS:
        f.error(cat, f"{rp} ROLLBACK-B: elevated_error_rate trailing window is "
                     f"{err.get('trailing_window_sessions')!r} sessions != the ruled "
                     f"{ROLLBACK_B_TRAILING_WINDOW_SESSIONS}")
    # THE SAME NUMBER, compared to itself. This is the coupling the ruling
    # names: the exit criterion and the auto-blocker's trip are one fact.
    for key in ("abnormal_rate_trailing_window_max_pct", "trailing_window_sessions"):
        if rate.get(key) is not None and err.get(key) != rate.get(key):
            f.error(cat, f"{rp}: ROLLBACK-B's elevated_error_rate {key} "
                         f"{err.get(key)!r} disagrees with canary_exit_criteria."
                         f"tolerated_error_rate {key} {rate.get(key)!r}; they are ONE "
                         f"ruled number — apart, the canary can pass its exit "
                         f"criterion while its auto-blocker is tripping")

    quota = thresholds.get("elevated_quota_condition") or {}
    for key, want in (("per_session_duration_seconds_max",
                       ROLLBACK_B_SESSION_SECONDS_MAX),
                      ("per_session_billable_units_max",
                       ROLLBACK_B_SESSION_UNITS_MAX),
                      ("provider_project_monthly_cap_usd",
                       ROLLBACK_B_PROJECT_CAP_USD)):
        if quota.get(key) != want:
            f.error(cat, f"{rp} ROLLBACK-B: elevated_quota_condition.{key} is "
                         f"{quota.get(key)!r} != the ruled {want} (§7.2)")
    if quota.get("uncountable_is") != "exhausted":
        f.error(cat, f"{rp} ROLLBACK-B: elevated_quota_condition.uncountable_is is "
                     f"{quota.get('uncountable_is')!r} != 'exhausted'; a broker that "
                     f"cannot determine its accumulated cost REFUSES the session "
                     f"rather than proceeding blind")

    # --- ROLLBACK-C's cost signal: metered, and with a reader ---
    rc = _rollback_class(doc, "ROLLBACK-C")
    cost = (rc.get("trigger_signals") or {}).get("cost_concern") or {}
    if cost.get("per_tenant_monthly_budget_usd") != ROLLBACK_C_TENANT_BUDGET_USD:
        f.error(cat, f"{rp} ROLLBACK-C: cost_concern.per_tenant_monthly_budget_usd is "
                     f"{cost.get('per_tenant_monthly_budget_usd')!r} != the ruled "
                     f"{ROLLBACK_C_TENANT_BUDGET_USD} (§7.2)")
    if cost.get("hard_stop_exists") is not False:
        f.error(cat, f"{rp} ROLLBACK-C: cost_concern.hard_stop_exists is "
                     f"{cost.get('hard_stop_exists')!r}; Fork 1 Option C DEFERS the "
                     f"durable synchronous per-tenant counter (task 6.1.5), so "
                     f"nothing can hard-stop a single tenant and recording this as "
                     f"hard would be false")
    if not cost.get("alert_reader"):
        f.error(cat, f"{rp} ROLLBACK-C: cost_concern names no `alert_reader`; a "
                     f"metered-only budget with nothing wired to it is the "
                     f"`budget_envelopes: {{}}` failure this org has already had "
                     f"flagged in review — §7.4 exists to give this number a reader")

    pol = doc.get("rollback_policy")
    pol = pol if isinstance(pol, dict) else {}
    _check_operator_surface(f, cat, rp, pol)
    _check_session_outcome_tokens(f, cat, rp, doc, pol)
    _check_tenant_definition(f, cat, rp, doc)


def _check_operator_surface(f: Findings, cat: str, rp: str, pol: dict) -> None:
    """§7.7: the operator surface that fires the kill switches, RULED
    2026-08-27 — a named PERSON, a documented runbook act, and a runbook that
    exists.

    Fail closed on absence: the block's own former statement is that a canary
    opened without a named holder has an unfireable kill switch, which would
    make ROLLBACK-C undeliverable and ROLLBACK-A dependent on automation alone.
    Deleting the block is therefore the defect, not a deferral."""
    surface = pol.get("operator_surface")
    if not isinstance(surface, dict):
        f.error(cat, f"{rp}: `rollback_policy.operator_surface` missing (fail "
                     f"closed); the surface that fires the kill switches MUST be "
                     f"named before the canary opens")
        return
    if surface.get("status") != "named":
        f.error(cat, f"{rp}: operator_surface.status is "
                     f"{surface.get('status')!r} != 'named'; §7.7 was ruled "
                     f"2026-08-27 and a canary opened without a named holder has an "
                     f"unfireable kill switch")
    if surface.get("holder") != POLICY_OPERATOR_HOLDER:
        f.error(cat, f"{rp}: operator_surface.holder is {surface.get('holder')!r} != "
                     f"the ruled {POLICY_OPERATOR_HOLDER!r}")
    # A ROLE IS THE FAILURE THIS FIELD EXISTS TO CATCH. §7.4 recorded its page
    # target as a role precisely BECAUSE §7.7 was open; a holder recorded as a
    # role again would re-open the gap while looking closed.
    if surface.get("holder_kind") != POLICY_OPERATOR_HOLDER_KIND:
        f.error(cat, f"{rp}: operator_surface.holder_kind is "
                     f"{surface.get('holder_kind')!r} != "
                     f"{POLICY_OPERATOR_HOLDER_KIND!r}; §7.7 requires a PERSON, and "
                     f"a role recorded here is the same gap §7.4 was already holding "
                     f"open")
    if surface.get("holds") != "both_switches":
        f.error(cat, f"{rp}: operator_surface.holds is {surface.get('holds')!r} != "
                     f"'both_switches'; the kernel gives this ring two switches and "
                     f"the ruled holder holds both")
    if surface.get("mechanism") != POLICY_OPERATOR_MECHANISM:
        f.error(cat, f"{rp}: operator_surface.mechanism is "
                     f"{surface.get('mechanism')!r} != {POLICY_OPERATOR_MECHANISM!r}")
    if surface.get("web_console_used") is not False:
        f.error(cat, f"{rp}: operator_surface.web_console_used is "
                     f"{surface.get('web_console_used')!r}; the web console is an "
                     f"explicit kernel non-goal and no operator surface is inherited "
                     f"from it")
    if not surface.get("rota_deferred_to"):
        f.error(cat, f"{rp}: operator_surface names no `rota_deferred_to`; ONE named "
                     f"holder is proportionate to this ring and not to the pilot, so "
                     f"the deferral is part of the ruling and not an omission")
    # §7.4's page target and §7.7's holder are ONE human by ruling — "the person
    # who learns about the spend is the person who can stop it".
    if surface.get("also_the_alert_page_target") is not True:
        f.error(cat, f"{rp}: operator_surface.also_the_alert_page_target is "
                     f"{surface.get('also_the_alert_page_target')!r}; §7.4's page "
                     f"target and §7.7's holder are ONE human by ruling — an alert "
                     f"with no named recipient and a kill switch with no named "
                     f"holder are the same gap seen twice")

    # THE MECHANISM IS A DOCUMENT, SO THE DOCUMENT MUST EXIST. A `mechanism_ref`
    # that resolves to nothing is an unfireable switch with a filename in the
    # field, which is the failure this whole block was opened against.
    ref = surface.get("mechanism_ref")
    if ref != POLICY_OPERATOR_RUNBOOK:
        f.error(cat, f"{rp}: operator_surface.mechanism_ref is {ref!r} != the ruled "
                     f"{POLICY_OPERATOR_RUNBOOK!r}")
    if isinstance(ref, str) and ref:
        # Routed through the shared `_repo_file` guard rather than keeping a
        # second hand-rolled containment check here. This site already refused
        # an escape; what it gains is the SPECIFIC refusal — absolute, or a
        # `..` segment — and, more usefully, one implementation for every
        # YAML-supplied path in this validator instead of two that can drift.
        target = _repo_file(f, cat, f"{rp}: operator_surface.mechanism_ref", ref)
        if target is None:
            pass  # refused above with the reason; the filesystem is untouched
        elif not target.is_file():
            f.error(cat, f"{rp}: operator_surface.mechanism_ref {ref!r} resolves to "
                         f"no file; the RULED MECHANISM IS THAT DOCUMENT, so a "
                         f"dangling reference is an unfireable kill switch wearing a "
                         f"filename")

    # The two switches the kernel gives this ring, and their two modes each.
    switches = surface.get("switches")
    if not isinstance(switches, list):
        f.error(cat, f"{rp}: operator_surface carries no `switches` list; the holder "
                     f"holds two named switches, not an unspecified control")
        return
    scopes = [s.get("scope") for s in switches if isinstance(s, dict)]
    if len(scopes) != len(switches):
        f.error(cat, f"{rp}: operator_surface.switches carries entries that are not "
                     f"mappings; a switch that cannot be read is never counted as "
                     f"present")
    if set(scopes) != POLICY_SWITCH_SCOPES:
        f.error(cat, f"{rp}: operator_surface switch scopes {sorted(scopes, key=str)} "
                     f"!= the kernel's two {sorted(POLICY_SWITCH_SCOPES)}; finer "
                     f"scopes are DEFERRED with the features they would govern, so a "
                     f"third scope here is a switch the runtime does not have")
    for s in switches:
        if not isinstance(s, dict):
            continue
        modes = set(s.get("modes") or [])
        if modes != POLICY_SWITCH_MODES:
            f.error(cat, f"{rp}: switch {s.get('id')!r} declares modes "
                         f"{sorted(modes, key=str)} != "
                         f"{sorted(POLICY_SWITCH_MODES)}; each kill switch carries "
                         f"OPTIONAL active-lease revocation, and RING-04 exercises "
                         f"both modes of both switches before any canary traffic")


def _registry_members(f: Findings, cat: str, rp: str, ref: str) -> set[str] | None:
    """The members of one closed AVC registry, read from the registry file at
    `ref` (a path relative to `contracts/avatar-client/`).

    Read rather than mirrored on purpose: §7.8's ruling is that no NEW outcome
    token is introduced, and the way that stays true is that the check resolves
    against the vocabulary the schemas are parity-checked against. A constant
    copied into this module would keep agreeing with itself after the registry
    moved. Returns None when the registry file is absent — which is reported,
    never silently skipped; a present-but-unparseable registry instead raises
    MalformedYAML, which the run() boundary turns into its own finding.

    PRECONDITION: `ref` is a PINNED, in-tree reference — the caller has already
    compared it against the sanctioned path for that vocabulary. This helper
    therefore carries no containment guard of its own: a guard that no caller
    can trip is a guard no test can prove, and an unprovable guard is worth less
    than the sentence saying where the real one lives."""
    target = AVC / ref
    if not target.is_file():
        f.error(cat, f"{rp}: the closed registry `{ref}` is absent, so the declared "
                     f"tokens cannot be resolved against it (fail closed)")
        return None
    doc = load_yaml(target)
    members = doc.get("members") if isinstance(doc, dict) else None
    if not isinstance(members, list):
        f.error(cat, f"{rp}: `{ref}` carries no readable `members` list (fail "
                     f"closed)")
        return None
    return {m.get("id") for m in members if isinstance(m, dict)}


def _check_session_outcome_tokens(f: Findings, cat: str, rp: str,
                                  doc: Any, pol: dict) -> None:
    """§7.8: the session outcome each rollback path emits, RULED 2026-08-27.

    Two rules, and the second is the one with teeth. First, the path-to-token
    mapping matches the ruling — a drained leg is `abandoned`, a
    force-terminated leg is `revoked` on the same terminal path consent
    withdrawal already uses. Second, EVERY token named anywhere in the block is
    a member of the closed `session-outcomes` registry, because the ruling's
    whole content is that no new token was introduced: a policy that invents
    `drained` or `blocked` would otherwise read as a decision rather than as
    the schema violation it is.

    Two rules that look like bookkeeping and are not. The artifact's own
    `registry_ref` is PINNED to the sanctioned vocabulary and then FOLLOWED, so
    the document cannot name one registry while this rule reads another. And
    `unbound` must be an EXPLICIT EMPTY LIST: §7.8's claim is "nothing remains
    unbound", which is asserted, never inferred from a field that is simply
    absent."""
    block = pol.get("session_outcome_tokens")
    if not isinstance(block, dict):
        f.error(cat, f"{rp}: `rollback_policy.session_outcome_tokens` missing (fail "
                     f"closed); the outcome each rollback path emits is DECLARED IN "
                     f"ADVANCE rather than inferred")
        return
    if block.get("status") != "bound":
        f.error(cat, f"{rp}: session_outcome_tokens.status is "
                     f"{block.get('status')!r} != 'bound'; §7.8 was ruled 2026-08-27 "
                     f"and every path now carries a declared token")
    if block.get("new_outcome_token_introduced") is not False:
        f.error(cat, f"{rp}: session_outcome_tokens.new_outcome_token_introduced is "
                     f"{block.get('new_outcome_token_introduced')!r}; the ruling's "
                     f"content is that NO new outcome token is introduced")

    bound = block.get("bound")
    if not isinstance(bound, list):
        f.error(cat, f"{rp}: session_outcome_tokens.bound missing or not a list")
        bound = []
    got = {e.get("path"): e for e in bound if isinstance(e, dict)}
    if set(got) != set(POLICY_OUTCOME_PATHS):
        f.error(cat, f"{rp}: session_outcome_tokens bound paths "
                     f"{sorted(got, key=str)} != the ruled "
                     f"{sorted(POLICY_OUTCOME_PATHS)}")
    for path, want in POLICY_OUTCOME_PATHS.items():
        entry = got.get(path)
        if not isinstance(entry, dict):
            continue
        if entry.get("outcome") != want:
            f.error(cat, f"{rp}: session_outcome_tokens path {path!r} emits "
                         f"{entry.get('outcome')!r} != the ruled {want!r}")
    # NOTHING MAY REMAIN UNBOUND — AND THE FIELD MUST SAY SO IN THOSE WORDS.
    # §7.8's claim is not "no unbound paths are visible", it is "nothing remains
    # unbound", so the artifact has to ASSERT the empty list rather than merely
    # fail to carry a non-empty one. A truthiness test read `{}`, `""`, `0` and
    # a MISSING KEY as "nothing unbound", which means deleting the field — the
    # single easiest edit — would have silently satisfied the strongest claim in
    # the block. An explicit empty LIST is the only passing shape.
    if "unbound" not in block:
        f.error(cat, f"{rp}: session_outcome_tokens carries no `unbound` key; §7.8's "
                     f"claim is that NOTHING remains unbound, and a claim that "
                     f"strong is asserted as an empty list — never inferred from an "
                     f"absent field")
    else:
        unbound = block.get("unbound")
        if not isinstance(unbound, list):
            f.error(cat, f"{rp}: session_outcome_tokens.unbound is a "
                         f"{type(unbound).__name__} ({unbound!r}), not a list; an "
                         f"empty mapping or empty string reads as 'nothing unbound' "
                         f"to a truthiness test and as a malformed record to a reader")
        elif unbound:
            f.error(cat, f"{rp}: session_outcome_tokens.unbound still carries "
                         f"{len(unbound)} path(s) while status is 'bound'; §7.8 bound "
                         f"every path, so an unbound entry is the open state returning "
                         f"under a closed label")

    # THE ARTIFACT'S OWN REGISTRY REFERENCE IS PINNED, AND THEN FOLLOWED.
    # `registry_ref` was recorded but never checked, so the policy could have
    # named one vocabulary while this rule resolved against another — the
    # document and its validator disagreeing in silence, which is worse than
    # either being wrong alone. The ref is PINNED rather than freely followed
    # because the contract grants no choice here: `session-outcomes` is a CLOSED
    # registry with exactly one file, and letting the artifact nominate its own
    # vocabulary would invent flexibility that would defeat the closure. So the
    # ref must equal the sanctioned path — and the read then goes THROUGH it, so
    # the check demonstrably resolves what the document says it resolves.
    ref = block.get("registry_ref")
    if ref != OUTCOME_REGISTRY_REF:
        f.error(cat, f"{rp}: session_outcome_tokens.registry_ref is {ref!r} != the "
                     f"sanctioned {OUTCOME_REGISTRY_REF!r}; the outcome vocabulary is "
                     f"a CLOSED registry, so the artifact may not nominate a "
                     f"different one — and a ref nobody checks lets the policy point "
                     f"one way while the rule reads another")
    # A BAD REF IS NOT A REASON TO SKIP THE MEMBERSHIP RULE. Resolving against
    # the sanctioned path when the ref is wrong keeps the token check running;
    # rewarding a broken reference with a weaker validation is the one outcome
    # this must not have.
    known = _registry_members(
        f, cat, rp, ref if ref == OUTCOME_REGISTRY_REF else OUTCOME_REGISTRY_REF)
    if known is not None:
        declared: set[str] = set()
        for entry in bound:
            if not isinstance(entry, dict):
                continue
            if isinstance(entry.get("outcome"), str):
                declared.add(entry["outcome"])
            declared.update(t for t in entry.get("also_permitted") or []
                            if isinstance(t, str))
        invented = sorted(declared - known)
        if invented:
            f.error(cat, f"{rp}: session_outcome_tokens names {invented}, which "
                         f"is/are not member(s) of the closed `session-outcomes` "
                         f"registry; §7.8 introduces NO new outcome token")

    # THE SAME FACT, CARRIED TWICE, COMPARED. The class a reader lands on states
    # its own terminal; the §7.8 block owns the mapping. Apart, a class could
    # promise one terminal while the policy bound another.
    for cid, (want_outcome, want_path) in POLICY_CLASS_OUTCOMES.items():
        c = _rollback_class(doc, cid)
        if c.get("session_outcome") != want_outcome:
            f.error(cat, f"{rp} {cid}: session_outcome is "
                         f"{c.get('session_outcome')!r} != the ruled "
                         f"{want_outcome!r} (§7.8)")
        if c.get("session_outcome_path") != want_path:
            f.error(cat, f"{rp} {cid}: session_outcome_path is "
                         f"{c.get('session_outcome_path')!r} != {want_path!r}")
        entry = got.get(want_path)
        if isinstance(entry, dict) and entry.get("outcome") != c.get("session_outcome"):
            f.error(cat, f"{rp}: {cid}'s session_outcome "
                         f"{c.get('session_outcome')!r} disagrees with "
                         f"session_outcome_tokens path {want_path!r} "
                         f"{entry.get('outcome')!r}; they are ONE ruled fact")
    rc = _rollback_class(doc, "ROLLBACK-C")
    if rc.get("session_outcome") != POLICY_ROLLBACK_C_OUTCOME:
        f.error(cat, f"{rp} ROLLBACK-C: session_outcome is "
                     f"{rc.get('session_outcome')!r} != "
                     f"{POLICY_ROLLBACK_C_OUTCOME!r}; the operator selects the scope "
                     f"and the scope binds the token, so this class names no single "
                     f"outcome of its own")


def _check_tenant_definition(f: Findings, cat: str, rp: str, doc: Any) -> None:
    """§7.10: "tenant" for this ring, RULED 2026-08-27 as the cohort member.

    The recorded `tenant_count` is RECOMPUTED from `cohort.members` rather than
    read. §7.2's per-tenant budget was sized on two tenants sitting comfortably
    under the project cap; if the cohort ever grew and the count stayed at 2,
    the budget would silently be metering against a denominator that no longer
    exists, which is precisely the re-sizing the task said would be needed."""
    cohort = doc.get("cohort")
    cohort = cohort if isinstance(cohort, dict) else {}
    ref = cohort.get("tenant_definition_ref")
    if not isinstance(ref, dict):
        f.error(cat, f"{rp}: `cohort.tenant_definition_ref` missing (fail closed); "
                     f"without it the per-tenant spend and metering dimensions have "
                     f"no subject")
        return
    if ref.get("status") != "set":
        f.error(cat, f"{rp}: cohort.tenant_definition_ref.status is "
                     f"{ref.get('status')!r} != 'set'; §7.10 was ruled 2026-08-27 and "
                     f"§7.2's per-tenant budget has no subject until it is")
    if ref.get("tenant_is") != POLICY_TENANT_IS:
        f.error(cat, f"{rp}: cohort.tenant_definition_ref.tenant_is is "
                     f"{ref.get('tenant_is')!r} != the ruled {POLICY_TENANT_IS!r}; "
                     f"a tenant ruled as anything else re-opens §7.2's sizing against "
                     f"a new denominator")

    members = cohort.get("members")
    members = members if isinstance(members, list) else []
    member_ids = {m.get("id") for m in members if isinstance(m, dict)}
    declared_ids = set(ref.get("tenant_ids") or [])
    if declared_ids != member_ids:
        f.error(cat, f"{rp}: cohort.tenant_definition_ref.tenant_ids "
                     f"{sorted(declared_ids, key=str)} != the cohort's own members "
                     f"{sorted(member_ids, key=str)}; tenant IS cohort member, so the "
                     f"two lists are one list")
    if ref.get("tenant_count") != len(member_ids):
        f.error(cat, f"{rp}: cohort.tenant_definition_ref.tenant_count is "
                     f"{ref.get('tenant_count')!r} but the cohort carries "
                     f"{len(member_ids)} member(s); §7.2's $"
                     f"{ROLLBACK_C_TENANT_BUDGET_USD}/month per-tenant figure was "
                     f"sized on this denominator, so a count that outlives its "
                     f"membership re-sizes the budget silently")
    if ref.get("sizing_still_valid") is not True:
        f.error(cat, f"{rp}: cohort.tenant_definition_ref.sizing_still_valid is "
                     f"{ref.get('sizing_still_valid')!r}; the ruling is the "
                     f"denominator §7.2 already assumed, so it must state that the "
                     f"per-tenant figure stands — or §7.2 needs re-ruling, not a "
                     f"quiet flag")


def check_latency_sample_minimum(f: Findings) -> None:
    """§7.5, feeding §5.2: the minimum sample count per gated latency cell.

    §5.2's requirement is an ORDERING — "Declare the minimum sample count per
    gated cell BEFORE measuring" — and an ordering cannot be checked from the
    numbers alone once both exist. What CAN be checked, and is, is that the
    declaration exists, is dated, says of itself that it preceded measurement,
    and — the rule with teeth — DECLARES THE SAME CELL SET THE SLO GATES. A
    minimum declared over a different set of platforms, percentiles or
    intervals than the ones it is supposed to gate is a minimum for nothing:
    it would read as rigor while leaving every gated cell without a floor.

    The cell COUNT is recomputed from the SLO's own gated axes rather than
    trusted, because "4 cells" is the kind of number that stays behind when the
    axes it summarises move.

    Fail closed on a missing or unreadable record: an undeclared minimum is
    exactly the state §5.2 exists to prevent, and ALV-005-S02 ("A percentile is
    claimed from an undeclared sample count") is its scenario."""
    path = AVC / SAMPLE_MIN_FILE
    rp = f"contracts/avatar-client/{SAMPLE_MIN_FILE}"
    cat = "sample-minimum"
    if not path.is_file():
        f.error(cat, f"{rp} absent; §5.2 requires the minimum sample count per gated "
                     f"cell to be DECLARED BEFORE MEASURING, so its absence is the "
                     f"defect and not a deferral (fail closed)")
        return
    doc = load_yaml(path) or {}
    if not isinstance(doc, dict):
        f.error(cat, f"{rp}: not a mapping (fail closed)")
        return
    if doc.get("schema_version") != 1:
        f.error(cat, f"{rp}: schema_version {doc.get('schema_version')!r} != 1")
    if doc.get("kind") != SAMPLE_MIN_KIND:
        f.error(cat, f"{rp}: kind {doc.get('kind')!r} != {SAMPLE_MIN_KIND!r}")
    known = _resolve_map_ids(f, cat, rp)
    _check_map_refs(f, cat, rp, doc.get("acceptance_map_refs"), known)

    decl = doc.get("declaration") or {}
    if decl.get("declared_before_measuring") is not True:
        f.error(cat, f"{rp}: declaration.declared_before_measuring is "
                     f"{decl.get('declared_before_measuring')!r}; §5.2's whole "
                     f"requirement is the ordering — a minimum declared after the "
                     f"numbers are in is a minimum chosen to fit them")
    if not decl.get("declared_on"):
        f.error(cat, f"{rp}: declaration carries no `declared_on`; an undated "
                     f"declaration cannot be shown to precede the measurements")

    minimum = doc.get("minimum") or {}
    if minimum.get("n_min") != SAMPLE_MIN_N:
        f.error(cat, f"{rp}: minimum.n_min is {minimum.get('n_min')!r} != the ruled "
                     f"{SAMPLE_MIN_N}; at n=30 a p95 estimate is the second-largest "
                     f"of thirty — a maximum wearing a percentile's name")
    under = doc.get("under_minimum") or {}
    if under.get("effect") != SAMPLE_MIN_UNDER_EFFECT:
        f.error(cat, f"{rp}: under_minimum.effect is {under.get('effect')!r} != "
                     f"{SAMPLE_MIN_UNDER_EFFECT!r}; a short cell is RECORDED and MUST "
                     f"NOT GATE")
    spread = doc.get("spread") or {}
    for key, want in (("distinct_runs_min", SAMPLE_MIN_RUNS),
                      ("distinct_days_min", SAMPLE_MIN_DISTINCT_DAYS)):
        if spread.get(key) != want:
            f.error(cat, f"{rp}: spread.{key} is {spread.get(key)!r} != the ruled "
                         f"{want}; a minimum n taken all at once repeats F0's "
                         f"single-configuration weakness with a bigger number")
    p99 = doc.get("p99_posture") or {}
    if p99.get("gate_sample_floor") != SAMPLE_MIN_P99_FLOOR:
        f.error(cat, f"{rp}: p99_posture.gate_sample_floor is "
                     f"{p99.get('gate_sample_floor')!r} != {SAMPLE_MIN_P99_FLOOR}")
    if p99.get("stays_recorded_not_gated") is not True:
        f.error(cat, f"{rp}: p99_posture.stays_recorded_not_gated is "
                     f"{p99.get('stays_recorded_not_gated')!r}; at n=100 p99 IS "
                     f"effectively the maximum, and the acceptance map keeps it "
                     f"recorded-not-gated")

    # --- the declared cell set must be the set the SLO actually gates ---
    amap = load_yaml(AVC / "acceptance-map.yaml") if (AVC / "acceptance-map.yaml").is_file() else None
    slo_entries = _slo_entries(amap) if isinstance(amap, dict) else []
    if len(slo_entries) != 1:
        return  # check_latency_posture already reports zero or two
    gated = slo_entries[0].get("gated") or {}
    pairs = (("gated_platforms", "platforms"),
             ("gated_percentiles", "percentiles"),
             ("gated_intervals", "intervals"))
    for mine, theirs in pairs:
        declared = set(minimum.get(mine) or [])
        actual = set(gated.get(theirs) or [])
        if declared != actual:
            f.error(cat, f"{rp}: minimum.{mine} {sorted(declared)} != the SLO's "
                         f"gated {theirs} {sorted(actual)}; a minimum declared over a "
                         f"different cell set than the one it gates leaves every "
                         f"gated cell without a floor")
    if minimum.get("gated_network_class") != gated.get("network_class"):
        f.error(cat, f"{rp}: minimum.gated_network_class "
                     f"{minimum.get('gated_network_class')!r} != the SLO's gated "
                     f"network class {gated.get('network_class')!r}")
    # RECOMPUTED, not trusted: platforms x one gated network class x the two
    # reference classifications the comparison cell separates.
    expected_cells = len(set(gated.get("platforms") or [])) * 2
    if expected_cells and minimum.get("cells") != expected_cells:
        f.error(cat, f"{rp}: minimum.cells is {minimum.get('cells')!r} but the SLO's "
                     f"gated axes give {expected_cells} "
                     f"(platforms x nominal network x reference-versus-adapter)")


def check_broker_credential_binding(f: Findings) -> None:
    """§7.1 and §7.3 (task 6.1.1): the broker server-key custody pair.

    The binding is the ring's ONLY deployment source for the provider key —
    F0's mode-600 local file and its age-escrow copy are explicitly not one —
    so two properties are worth failing closed on:

    * THE VAULT STAYS OUT OF THE CONTRACT. `credential-contracts` is explicit:
      "Contract artifacts, lane definitions, and domain repositories SHALL NOT
      hard-code a vault operator, a vault product, or any secret value." That
      rule is easy to honour on the day it is written and easy to break six
      months later, when someone with the install's values in front of them
      fills in the two placeholders here because they look empty. So every
      VALUE in both files is scanned for a vault-product token and for raw
      secret material, and `provider` and `vault` must still be placeholders.
    * THE OVERRIDE AND THE BINDING CANNOT DRIFT APART. A rotation cadence keyed
      to a credential name that no binding declares governs nothing, and a
      binding whose cadence record names a different credential is unrotated
      while looking rotated. The two names are compared.

    Fail closed on either file missing: task 6.1.1 is the custody discharge,
    and a missing binding is an unbound key rather than a deferred one."""
    cat = "broker-credential"
    bpath = AVC / BINDING_FILE
    brp = f"contracts/avatar-client/{BINDING_FILE}"
    if not bpath.is_file():
        f.error(cat, f"{brp} absent; the internal-live broker server key would have "
                     f"no binding, and F0's local file plus age escrow is explicitly "
                     f"NOT a deployment source (fail closed)")
        return
    doc = load_yaml(bpath) or {}
    if not isinstance(doc, dict):
        f.error(cat, f"{brp}: not a mapping (fail closed)")
        return
    if doc.get("schema_version") != 1:
        f.error(cat, f"{brp}: schema_version {doc.get('schema_version')!r} != 1")
    if doc.get("kind") != BINDING_KIND:
        f.error(cat, f"{brp}: kind {doc.get('kind')!r} != {BINDING_KIND!r}; task 6.1.1 "
                     f"requires the PROMOTED binding-template shape, not a local one")
    known = _resolve_map_ids(f, cat, brp)

    bindings = doc.get("credential_bindings")
    if not isinstance(bindings, dict) or BINDING_ID not in bindings:
        f.error(cat, f"{brp}: credential_bindings does not declare {BINDING_ID!r}")
        binding = {}
    else:
        binding = bindings[BINDING_ID] if isinstance(bindings[BINDING_ID], dict) else {}
        surplus = sorted(set(bindings) - {BINDING_ID})
        if surplus:
            f.error(cat, f"{brp}: credential_bindings also declares {surplus}; this "
                         f"record binds ONE credential, and a second binding beside "
                         f"it shares its blast radius without saying so")
    for field in BINDING_FIELDS:
        if not binding.get(field):
            f.error(cat, f"{brp} {BINDING_ID}: `{field}` missing; the published "
                         f"template shape is followed exactly, never trimmed")
    for field in BINDING_PLACEHOLDER_FIELDS:
        value = binding.get(field)
        if isinstance(value, str) and not (value.startswith("<") and value.endswith(">")):
            f.error(cat, f"{brp} {BINDING_ID}: `{field}` is {value!r}, a concrete "
                         f"value; the vault operator and product are a PER-INSTALL "
                         f"EXECUTION BINDING and may not be hard-coded in a contract "
                         f"artifact — the concrete value belongs in the install's "
                         f"credentials/ tree")
    if binding.get("secret_ref") != BINDING_SECRET_REF:
        f.error(cat, f"{brp} {BINDING_ID}: secret_ref {binding.get('secret_ref')!r} != "
                     f"{BINDING_SECRET_REF!r}; task 6.1.2 requires a DEDICATED "
                     f"internal-live provider project distinct from the F0 lab, so a "
                     f"distinct key reference follows")
    if binding.get("rotation_policy") != BINDING_ROTATION_LABEL:
        f.error(cat, f"{brp} {BINDING_ID}: rotation_policy "
                     f"{binding.get('rotation_policy')!r} != "
                     f"{BINDING_ROTATION_LABEL!r}; the numeric cadence lives in "
                     f"{ROTATION_FILE}, because the published shape types this field "
                     f"as a string and every corpus instance uses it as an "
                     f"accountability label")
    res = doc.get("resolution") or {}
    if res.get("resolved_by") != "broker_only":
        f.error(cat, f"{brp}: resolution.resolved_by is {res.get('resolved_by')!r} != "
                     f"'broker_only'; task 6.1.1 says the binding is 'resolved only by "
                     f"the broker'")
    if res.get("materialization") != "ephemeral_process_scope":
        f.error(cat, f"{brp}: resolution.materialization is "
                     f"{res.get('materialization')!r} != 'ephemeral_process_scope'; "
                     f"the fetched value is never baked into an image, committed "
                     f"config, or a log")
    _check_map_refs(f, cat, f"{brp} resolution", res.get("acceptance_map_refs"), known)
    _check_no_vault_or_secret(f, cat, brp, doc)

    # --- the cadence half (§7.3) ---
    rpath = AVC / ROTATION_FILE
    rrp = f"contracts/avatar-client/{ROTATION_FILE}"
    if not rpath.is_file():
        f.error(cat, f"{rrp} absent; §7.3's cadence has no home — the binding's "
                     f"`rotation_policy` is a string in the published schema and "
                     f"cannot hold a maximum key age (fail closed)")
        return
    rdoc = load_yaml(rpath) or {}
    if not isinstance(rdoc, dict):
        f.error(cat, f"{rrp}: not a mapping (fail closed)")
        return
    if rdoc.get("schema_version") != 1:
        f.error(cat, f"{rrp}: schema_version {rdoc.get('schema_version')!r} != 1")
    if rdoc.get("kind") != ROTATION_KIND:
        f.error(cat, f"{rrp}: kind {rdoc.get('kind')!r} != {ROTATION_KIND!r}")
    if rdoc.get("binds_credential_binding") != BINDING_ID:
        f.error(cat, f"{rrp}: binds_credential_binding "
                     f"{rdoc.get('binds_credential_binding')!r} != {BINDING_ID!r}; a "
                     f"cadence keyed to a credential no binding declares governs "
                     f"nothing")
    pol = rdoc.get("rotation_policy") or {}
    globals_ = set(pol.get("require_rotation_on") or [])
    if globals_ != ROTATION_GLOBAL_TRIGGERS:
        f.error(cat, f"{rrp}: rotation_policy.require_rotation_on "
                     f"{sorted(globals_)} != the inherited global list "
                     f"{sorted(ROTATION_GLOBAL_TRIGGERS)}; §7.3 inherits it UNCHANGED "
                     f"and adds to it — narrowing it here would silently drop the "
                     f"SOP's compromise path, which rides `suspected_exposure`")
    override = (pol.get("credential_overrides") or {}).get(BINDING_ID) or {}
    if override.get("max_key_age_days") != ROTATION_MAX_KEY_AGE_DAYS:
        f.error(cat, f"{rrp}: {BINDING_ID} max_key_age_days is "
                     f"{override.get('max_key_age_days')!r} != the ruled "
                     f"{ROTATION_MAX_KEY_AGE_DAYS}; 90 is the org's only enforced "
                     f"key-age tier, and it is chosen partly so that at most one "
                     f"rotation can land inside the 14-day canary soak")
    added = set(override.get("additional_require_rotation_on") or [])
    if added != ROTATION_ADDED_TRIGGERS:
        f.error(cat, f"{rrp}: {BINDING_ID} additional_require_rotation_on "
                     f"{sorted(added)} != the ruled {sorted(ROTATION_ADDED_TRIGGERS)}")
    record = pol.get("rotation_record") or {}
    if "secret_value" not in set(record.get("forbidden_fields") or []):
        f.error(cat, f"{rrp}: rotation_record does not forbid `secret_value`; the "
                     f"SOP records owner, date, reason and the LOGICAL reference, "
                     f"never the value")
    _check_map_refs(f, cat, f"{rrp} rotation_record",
                    record.get("acceptance_map_refs"), known)
    _check_no_vault_or_secret(f, cat, rrp, rdoc)


def _check_no_vault_or_secret(f: Findings, cat: str, rp: str, node: Any,
                              trail: str = "") -> None:
    """Walk every VALUE of a custody record for a hard-coded vault product or
    raw secret material.

    Values only, and every value — not just the fields we expect to carry one.
    The prohibition is on the artifact, not on a field list: a vault name
    pasted into a `note`, a `statement` or a `rationale` is hard-coded in a
    contract artifact just as surely as one pasted into `vault`, and prose is
    exactly where such a paste survives review. Comments are not walked,
    because YAML comments are not content and a comment explaining WHY the
    product is absent must be allowed to be legible."""
    if isinstance(node, dict):
        for key, value in node.items():
            _check_no_vault_or_secret(f, cat, rp, value, f"{trail}.{key}" if trail else str(key))
    elif isinstance(node, list):
        for i, item in enumerate(node):
            _check_no_vault_or_secret(f, cat, rp, item, f"{trail}[{i}]")
    elif isinstance(node, str):
        low = node.lower()
        squashed = re.sub(r"[^a-z0-9]", "", low)
        hits = sorted({t for t in VAULT_PRODUCT_TOKENS if t in squashed}
                      | {t for t in VAULT_INSTANCE_TOKENS if t in low})
        if hits:
            f.error(cat, f"{rp}: value at {trail or '<root>'} names vault product or "
                         f"instance token(s) {hits}; the vault operator and product "
                         f"are a per-install execution binding and a contract artifact "
                         f"may not hard-code one")
        marks = sorted({m for m in BINDING_SECRET_MARKERS if m in low})
        if marks:
            f.error(cat, f"{rp}: value at {trail or '<root>'} carries raw secret "
                         f"marker(s) {marks}; credentials are delivered BY REFERENCE, "
                         f"never baked into a repository")


# --- shape guards for the §6.2 readers --------------------------------------
# `x.get("k") or {}` DEFENDS ONLY AGAINST ABSENCE, and absence is the easy
# case. A key that is PRESENT but holds a list, a string or a number is
# truthy, survives the `or`, and then raises AttributeError out of the next
# `.get()` — which ends the run as an anonymous harness crash rather than as
# the finding a malformed contract artifact deserves. These two read a value
# at the shape the caller requires, RECORD a finding when it is present and
# wrong, and hand back an empty container so the rest of the run continues and
# reports everything else. Fail closed, and say which file and field did it.
def _as_mapping(f: Findings, cat: str, where: str, value: object) -> dict:
    """A value that must be a MAPPING if it is present at all.

    Absent reads as empty on purpose: the caller's own field checks then
    report the specific field that is missing, which is a more useful message
    than "this block is absent"."""
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    f.error(cat, f"{where} must be a mapping, got {type(value).__name__}; a "
                 f"malformed shape is a finding, not a crash")
    return {}


def _as_sequence(f: Findings, cat: str, where: str, value: object) -> list:
    """A value that must be a LIST if it is present at all.

    A string is deliberately NOT accepted as a sequence here. Iterating one
    yields its CHARACTERS, so a scalar written where a list belongs would
    quietly become a set of single letters — `set("safety")` reading as six
    triggers — and every downstream comparison would then be wrong in a way
    that looks like data rather than like a typo."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    f.error(cat, f"{where} must be a list, got {type(value).__name__}; a "
                 f"malformed shape is a finding, not a crash")
    return []


def _mappings_in(f: Findings, cat: str, where: str, value: object) -> list[dict]:
    """Every MAPPING member of a list-valued field, with non-mapping members
    reported rather than skipped in silence. A list whose entries are strings
    would otherwise read as a legitimately empty set of ids."""
    out: list[dict] = []
    for i, item in enumerate(_as_sequence(f, cat, where, value)):
        if isinstance(item, dict):
            out.append(item)
        else:
            f.error(cat, f"{where}[{i}] must be a mapping, got "
                         f"{type(item).__name__}")
    return out


def _strings_in(f: Findings, cat: str, where: str, value: object) -> set[str]:
    """The non-blank STRING members of a list-valued field, as a set.

    Two failures this replaces, both of which `set(...)` alone commits:

    A NON-STRING MEMBER IS REPORTED, NEVER DROPPED. Filtering with
    `if isinstance(t, str)` shrinks a vocabulary silently, so a policy listing
    seven triggers and one malformed entry would validate a corpus against
    seven and say nothing — the malformed artifact hides behind the good part
    of itself. Consistent with `_mappings_in`, the bad member is a finding and
    the good members still participate; a field with NO usable member is left
    empty for the caller to refuse.

    AND AN UNHASHABLE MEMBER IS A FINDING RATHER THAN A CRASH. `set()` over a
    list containing a mapping raises `TypeError: unhashable type: 'dict'`,
    which ends the run the same anonymous way the `.get()` on a list did."""
    out: set[str] = set()
    for i, item in enumerate(_as_sequence(f, cat, where, value)):
        if isinstance(item, str) and item.strip():
            out.add(item)
        else:
            f.error(cat, f"{where}[{i}] must be a non-empty string, got "
                         f"{item!r}; a malformed member is reported, not "
                         f"silently dropped from the set it belongs to")
    return out


def _ids_in(f: Findings, cat: str, where: str, value: object) -> set[str]:
    """The string `id` of every mapping member of a list-valued field.

    Same discipline as `_strings_in`, for the registries these checks read
    their vocabularies out of: a member whose `id` is absent or is itself a
    mapping would otherwise either vanish from the set or raise `TypeError`
    on the way into it."""
    out: set[str] = set()
    for i, item in enumerate(_mappings_in(f, cat, where, value)):
        ident = item.get("id")
        if isinstance(ident, str) and ident.strip():
            out.add(ident)
        else:
            f.error(cat, f"{where}[{i}].id must be a non-empty string, got "
                         f"{ident!r}")
    return out


def _repo_file(f: Findings, cat: str, where: str, claimed: object) -> Path | None:
    """A repository-relative path READ FROM YAML, resolved safely or refused.

    A path that arrives from a contract artifact reaches `ROOT / value` and
    then the filesystem, and two ordinary-looking values leave the repository
    entirely. An ABSOLUTE path discards the left operand — `Path("/repo") /
    "/etc/passwd"` is `/etc/passwd`, by pathlib's specification rather than by
    accident — and any `..` segment walks out of the tree. On a CI runner that
    turns a YAML field into an arbitrary-file-read primitive.

    Both are refused as FINDINGS naming which one it was, never silently. The
    join is then `resolve()`d and re-checked with `is_relative_to`, because
    the two syntactic tests alone would not catch a path that is relative and
    `..`-free yet still leaves the tree by another route.

    SYMLINKS ARE NOT GIVEN SEPARATE HANDLING, deliberately. `resolve()`
    already follows them, so a symlink inside the repository pointing outside
    it lands outside ROOT and is refused by the containment check like any
    other escape. Going further — refusing paths that are symlinked but still
    contained — would be threat-modelling a validator that reads files from
    its own repository against an attacker who can already write that
    repository, which is not a boundary this tool holds or claims to.

    Returns the resolved path, or None when it was refused."""
    if not isinstance(claimed, str) or not claimed.strip():
        f.error(cat, f"{where} must be a non-empty string path, got "
                     f"{claimed!r}; `ROOT / <non-string>` raises rather than "
                     f"reporting")
        return None
    candidate = Path(claimed)
    if candidate.is_absolute():
        f.error(cat, f"{where} {claimed!r} is an ABSOLUTE path; joining one to "
                     f"the repository root discards the root entirely, so this "
                     f"is refused rather than resolved")
        return None
    if ".." in candidate.parts:
        f.error(cat, f"{where} {claimed!r} contains a '..' segment, which walks "
                     f"out of the repository; refused rather than resolved")
        return None
    root = ROOT.resolve()
    target = (root / candidate).resolve()
    if not target.is_relative_to(root):
        f.error(cat, f"{where} {claimed!r} resolves to {target}, which is "
                     f"outside the repository; refused rather than read")
        return None
    return target


def _rollback_a_triggers(f: Findings, cat: str) -> set[str] | None:
    """ROLLBACK-A's ratified trigger vocabulary, READ FROM THE POLICY.

    Not mirrored as a constant here on purpose. The corpus's whole claim is
    that every scenario's failure maps to a trigger the rollback policy already
    ratified; checking it against a second copy in this file would only prove
    the two copies agree with each other. Returns None (and records a finding)
    when the vocabulary cannot be read, because a corpus checked against
    nothing is a corpus that was not checked."""
    path = AVC / POLICY_FILE
    if not path.is_file():
        f.error(cat, f"{CORPUS_FILE}: {POLICY_FILE} is absent, so ROLLBACK-A's "
                     f"trigger vocabulary cannot be read; every scenario's "
                     f"emitted trigger is unverifiable (fail closed)")
        return None
    prp = f"contracts/avatar-client/{POLICY_FILE}"
    doc = _as_mapping(f, cat, prp, load_yaml(path))
    policy = _as_mapping(f, cat, f"{prp} rollback_policy",
                         doc.get("rollback_policy"))
    classes = _mappings_in(f, cat, f"{prp} rollback_policy.classes",
                           policy.get("classes"))
    for entry in classes:
        if entry.get("id") == "ROLLBACK-A":
            # NON-STRING MEMBERS ARE REPORTED, NOT FILTERED AWAY. Dropping them
            # would shrink the ratified vocabulary in silence: a policy listing
            # seven usable triggers and one malformed entry would check the
            # corpus against seven and say nothing, so the malformed artifact
            # would hide behind the good part of itself. The surviving strings
            # still participate — the same semantics `_mappings_in` uses — and
            # a list with NO usable member falls through to the refusal below,
            # because an empty vocabulary would fail every scenario for the
            # wrong reason.
            triggers = _strings_in(f, cat, f"{prp} ROLLBACK-A.triggers",
                                   entry.get("triggers"))
            if not triggers:
                break
            return triggers
    f.error(cat, f"{CORPUS_FILE}: {POLICY_FILE} declares no readable ROLLBACK-A "
                 f"trigger list; the corpus cannot be checked against the "
                 f"ratified vocabulary (fail closed)")
    return None


def check_synthetic_evaluation_corpus(f: Findings) -> None:
    """§6.2.1: the synthetic model-versus-model evaluation corpus.

    Four things are checked, and each exists because its failure mode is a
    corpus that LOOKS complete:

    1. EVERY SCENARIO'S FAILURE MAPS TO A RATIFIED TRIGGER. `detection.py`
       answers an unrecognised trigger with `REFUSED_UNKNOWN_TRIGGER` — a
       NON-tripping verdict — so a scenario carrying an invented trigger would
       fail silently at canary time: the evaluation would report a failure and
       the ring would not abort. The vocabulary is read from the rollback
       policy, never from a copy here.

    2. EVERY CLASS x DOMAIN CELL IS COVERED. Condition 7 requires five classes
       to pass for three domains; a missing cell is a condition-7 claim with no
       evidence behind it, and §7.6's session floor counts those same 15 cells.

    3. EVERY ROLLBACK-A TRIGGER IS REACHABLE FROM THE CORPUS. §6.3.3 proved the
       safety trip for all eight recorded triggers; a corpus that can only
       produce six of them leaves two proven paths unexercised.

    4. THE DECLARED COVERAGE COUNTS ARE RECOMPUTED, never trusted. A totals
       block that disagrees with the scenarios beneath it is the exact shape of
       a corpus that was edited without its summary.

    Fail closed on an unreadable corpus; skip silently when the file is absent
    so the validator stays green at every phase checkpoint."""
    cat = "eval-corpus"
    path = AVC / CORPUS_FILE
    if not path.is_file():
        return
    rp = f"contracts/avatar-client/{CORPUS_FILE}"
    doc = load_yaml(path)
    if not isinstance(doc, dict):
        f.error(cat, f"{rp}: top-level mapping required")
        return
    if doc.get("kind") != CORPUS_KIND:
        f.error(cat, f"{rp}: kind {doc.get('kind')!r} != {CORPUS_KIND!r}")
    if not str(doc.get("corpus_ref") or "").strip():
        f.error(cat, f"{rp}: no `corpus_ref`; `SafetyEvalSignal.corpus_ref` is "
                     f"required and non-empty precisely so a verdict can be "
                     f"re-run by whoever reads the record")

    # Fork 4's first clause, as fields rather than as prose.
    syn = _as_mapping(f, cat, f"{rp} synthesis", doc.get("synthesis"))
    if syn.get("content_origin") != "scripted":
        f.error(cat, f"{rp}: synthesis.content_origin is "
                     f"{syn.get('content_origin')!r} != 'scripted'; Fork 4 "
                     f"Option C rules that the evaluation corpus is SYNTHETIC")
    for field in ("tenant_data", "real_utterances"):
        if syn.get(field) != "none":
            f.error(cat, f"{rp}: synthesis.{field} is {syn.get(field)!r} != "
                         f"'none'; a corpus carrying either is not synthetic")
    audio = _as_mapping(f, cat, f"{rp} synthesis.audio_synthesis",
                        syn.get("audio_synthesis"))
    if audio.get("status") != "not_performed_by_this_artifact":
        f.error(cat, f"{rp}: synthesis.audio_synthesis.status does not record "
                     f"that rendering to audio is a §5/canary-time act of the "
                     f"RUN; committed audio would be media this ring has no "
                     f"retention class for")

    allowed = _rollback_a_triggers(f, cat)
    scenarios = _as_sequence(f, cat, f"{rp} scenarios", doc.get("scenarios"))
    if not scenarios:
        f.error(cat, f"{rp}: no scenarios; an empty corpus is not a corpus")
        return

    seen_ids: set[str] = set()
    cells_seen: set[str] = set()
    triggers_seen: set[str] = set()
    by_class: dict[str, int] = {}
    by_domain: dict[str, int] = {}
    class_triggers: dict[str, set[str]] = {}
    for sc in scenarios:
        if not isinstance(sc, dict):
            f.error(cat, f"{rp}: a scenario entry is not a mapping")
            continue
        sid = sc.get("scenario_id")
        if not sid:
            f.error(cat, f"{rp}: a scenario carries no scenario_id")
            continue
        if sid in seen_ids:
            f.error(cat, f"{rp}: duplicate scenario_id {sid!r}")
        seen_ids.add(sid)
        klass, domain = sc.get("class"), sc.get("domain")
        if klass not in CORPUS_CLASSES:
            f.error(cat, f"{rp}: {sid} names class {klass!r}; condition 7's "
                         f"classes are {sorted(CORPUS_CLASSES)}")
        if domain not in CORPUS_DOMAINS:
            f.error(cat, f"{rp}: {sid} names domain {domain!r}; condition 7's "
                         f"domains are {sorted(CORPUS_DOMAINS)}")
        if klass in CORPUS_CLASSES and domain in CORPUS_DOMAINS:
            cell = f"{klass}/{domain}"
            cells_seen.add(cell)
            if sc.get("cell") != cell:
                f.error(cat, f"{rp}: {sid} records cell {sc.get('cell')!r} but "
                             f"its class and domain make it {cell!r}")
            by_class[klass] = by_class.get(klass, 0) + 1
            by_domain[domain] = by_domain.get(domain, 0) + 1
        script = sc.get("script")
        if not isinstance(script, list) or not script:
            f.error(cat, f"{rp}: {sid} carries no scripted exchange; a scenario "
                         f"with no script cannot be run")
        expected = _as_mapping(f, cat, f"{rp} {sid} expected",
                               sc.get("expected"))
        if not str(expected.get("behavior") or "").strip():
            f.error(cat, f"{rp}: {sid} declares no expected behavior; a "
                         f"scenario with no expectation cannot pass or fail")
        emit = _as_mapping(f, cat, f"{rp} {sid} emits_on_failure",
                           sc.get("emits_on_failure"))
        trig = emit.get("trigger")
        if allowed is not None and trig not in allowed:
            f.error(cat, f"{rp}: {sid} emits trigger {trig!r}, which is not one "
                         f"of ROLLBACK-A's ratified triggers {sorted(allowed)}; "
                         f"`evaluate_safety_signal` answers an unrecognised "
                         f"trigger with a NON-tripping verdict, so this "
                         f"scenario's failure would not abort the ring")
        elif allowed is not None:
            triggers_seen.add(trig)
            if klass in CORPUS_CLASSES:
                class_triggers.setdefault(klass, set()).add(trig)
        if emit.get("rollback_class") != "ROLLBACK-A":
            f.error(cat, f"{rp}: {sid} names rollback_class "
                         f"{emit.get('rollback_class')!r}; the safety-eval trip "
                         f"fires ROLLBACK-A and no other class")
        if emit.get("session_outcome") != ENVELOPE_WITHDRAWAL_OUTCOME:
            f.error(cat, f"{rp}: {sid} names session_outcome "
                         f"{emit.get('session_outcome')!r} != "
                         f"{ENVELOPE_WITHDRAWAL_OUTCOME!r}; §7.8 binds "
                         f"ROLLBACK-A's force-terminated leg to that token")
        if emit.get("scenario_class") != klass:
            f.error(cat, f"{rp}: {sid} emits scenario_class "
                         f"{emit.get('scenario_class')!r} but is classified "
                         f"{klass!r}; the signal would misreport its own class")

    # (2) every class x domain cell
    expected_cells = {f"{k}/{d}" for k in CORPUS_CLASSES for d in CORPUS_DOMAINS}
    for missing in sorted(expected_cells - cells_seen):
        f.error(cat, f"{rp}: no scenario covers cell {missing!r}; condition 7 "
                     f"requires that class to pass for that domain")

    # (3) every ratified trigger reachable
    if allowed is not None:
        for unreached in sorted(allowed - triggers_seen):
            f.error(cat, f"{rp}: no scenario can produce ROLLBACK-A trigger "
                         f"{unreached!r}; §6.3.3 proved the safety trip for all "
                         f"eight recorded triggers and this corpus reaches "
                         f"fewer")

    # The per-class trigger declaration must match what the scenarios emit.
    # The LOOP still runs when the vocabulary is unreadable, because
    # `_strings_in` shape-checks each declared list and that is worth doing
    # either way; only the COMPARISON is conditional (see the note below).
    for entry in _mappings_in(f, cat, f"{rp} classes", doc.get("classes")):
        cid = entry.get("id")
        declared = _strings_in(f, cat, f"{rp} class {cid!r} triggers",
                               entry.get("triggers"))
        actual = class_triggers.get(cid, set()) if allowed is not None else set()
        if cid in CORPUS_CLASSES and actual and declared != actual:
            f.error(cat, f"{rp}: class {cid!r} declares triggers "
                         f"{sorted(declared)} but its scenarios emit "
                         f"{sorted(actual)}")

    # (4) recomputed coverage
    cov = _as_mapping(f, cat, f"{rp} coverage", doc.get("coverage"))
    recomputed = [("scenarios_total", len(scenarios)),
                  ("cells", len(cells_seen)),
                  ("classes", len(CORPUS_CLASSES)),
                  ("domains", len(CORPUS_DOMAINS))]
    # `triggers_covered` IS ONLY RECOMPUTABLE WHEN THE VOCABULARY WAS READ.
    # With an unreadable policy `triggers_seen` is empty because nothing could
    # be matched against it — not because the corpus reaches no trigger — so
    # comparing it would manufacture a coverage mismatch on top of the real
    # unreadable-policy finding, and the reader would have to work out which
    # of the two to act on. One true finding is worth more than two.
    if allowed is not None:
        recomputed.append(("triggers_covered", len(triggers_seen)))
    for key, actual in recomputed:
        if cov.get(key) != actual:
            f.error(cat, f"{rp}: coverage.{key} records {cov.get(key)!r} but "
                         f"the scenarios beneath it give {actual}; a summary "
                         f"that disagrees with its corpus is how an edited "
                         f"corpus keeps an old claim")
    for key, actual in (("scenarios_by_class", by_class),
                        ("scenarios_by_domain", by_domain)):
        # A comparison rather than a `.get()`, so a wrong shape cannot crash
        # here — but reading it through the guard turns "records ['safety']
        # but the scenarios give {...}" into a message that names the shape.
        if _as_mapping(f, cat, f"{rp} coverage.{key}", cov.get(key)) != actual:
            f.error(cat, f"{rp}: coverage.{key} records {cov.get(key)!r} but "
                         f"the scenarios give {actual}")


def check_ephemeral_processing_envelope(f: Findings) -> None:
    """§6.2.2 and §6.2.4: the canary's ephemeral processing envelope.

    The envelope's job is to say, in fields, what Fork 4 Option C ruled in
    prose. So the checks are the ones that keep those fields honest against the
    surfaces that already own the facts:

    - THE PURPOSES ARE THE FROZEN THREE, read from the registry rather than
      mirrored. `new_purposes_introduced` is compared to 0 and the count to the
      registry's own length, so the envelope cannot admit a fourth purpose by
      declaring one.
    - THE NEVER-INSTANTIATED CLASSES ARE ALL FOUR RESERVED CLASSES, read from
      the registry's `reserved:` block. §7.9's own list names three (it omits
      `video`, which this ring has no capability for) and is compared set-equal
      by its own check; this one is the full reserved set, because the promoted
      requirement names all four.
    - THE RETENTION WINDOW AND REFERENCE MATCH THE CHECKLIST'S §7.9 BLOCK, read
      from the checklist. Two artifacts carrying the same 90 days is two places
      for it to drift.
    - WITHDRAWAL'S REACHABILITY CITES A FIXTURE THAT EXISTS. A reachability
      claim whose proof is a filename nobody wrote is not a proof, and the
      fixture's `fixture_id` is compared so a rename cannot quietly orphan it.
    - THE NON-SHADOWING CONTROL STAYS OPERATIONAL (§6.2.4). `enforced_by_schema`
      must be exactly False and the enforcing flag must stay named as
      pilot-hardening work: no schema field forbids a second-model shadow
      today, and a later editor flipping this to `true` would be writing the
      false claim task 6.2.4 exists to refuse."""
    cat = "eval-envelope"
    path = AVC / ENVELOPE_FILE
    if not path.is_file():
        return
    rp = f"contracts/avatar-client/{ENVELOPE_FILE}"
    doc = load_yaml(path)
    if not isinstance(doc, dict):
        f.error(cat, f"{rp}: top-level mapping required")
        return
    if doc.get("kind") != ENVELOPE_KIND:
        f.error(cat, f"{rp}: kind {doc.get('kind')!r} != {ENVELOPE_KIND!r}")

    # ---- consent: the frozen three, read from the registry ----
    reg_path = AVC / "registries" / "consent-purposes.registry.yaml"
    frozen: set[str] = set()
    if reg_path.is_file():
        creg = "contracts/avatar-client/registries/consent-purposes.registry.yaml"
        frozen = _ids_in(
            f, cat, f"{creg} members",
            _as_mapping(f, cat, creg, load_yaml(reg_path)).get("members"))
    con = _as_mapping(f, cat, f"{rp} consent", doc.get("consent"))
    if frozen and con.get("frozen_purpose_count") != len(frozen):
        f.error(cat, f"{rp}: consent.frozen_purpose_count is "
                     f"{con.get('frozen_purpose_count')!r} but the registry "
                     f"holds {len(frozen)} purposes")
    if con.get("new_purposes_introduced") != 0:
        f.error(cat, f"{rp}: consent.new_purposes_introduced is "
                     f"{con.get('new_purposes_introduced')!r} != 0; this ring "
                     f"reuses the frozen purposes and adds none")
    media = _ids_in(f, cat, f"{rp} consent.media_leg_purposes",
                    con.get("media_leg_purposes"))
    if media != ENVELOPE_MEDIA_PURPOSES:
        f.error(cat, f"{rp}: consent.media_leg_purposes {sorted(media, key=str)} "
                     f"!= {sorted(ENVELOPE_MEDIA_PURPOSES)}; task 6.2.2 rules "
                     f"that the media leg rides exactly those two")
    struct = _as_mapping(f, cat, f"{rp} consent.structured_record_purpose",
                         con.get("structured_record_purpose")).get("id")
    if struct != ENVELOPE_STRUCTURED_PURPOSE:
        f.error(cat, f"{rp}: consent.structured_record_purpose.id is "
                     f"{struct!r} != {ENVELOPE_STRUCTURED_PURPOSE!r}")
    if frozen:
        for pid in sorted((media | {struct}) - frozen):
            f.error(cat, f"{rp}: consent names purpose {pid!r}, which is not a "
                         f"member of the frozen registry")
    opt = _as_mapping(f, cat, f"{rp} consent.optional_stricter_domain_purpose",
                      con.get("optional_stricter_domain_purpose"))
    if opt.get("unresolved_reference_effect") != "deny":
        f.error(cat, f"{rp}: optional_stricter_domain_purpose."
                     f"unresolved_reference_effect is "
                     f"{opt.get('unresolved_reference_effect')!r} != 'deny'; a "
                     f"stricter term that silently falls back to the neutral "
                     f"pair was never obtained")
    if _as_mapping(f, cat, f"{rp} consent.new_evaluation_purpose",
                   con.get("new_evaluation_purpose")
                   ).get("admitted") is not False:
        f.error(cat, f"{rp}: consent.new_evaluation_purpose.admitted is not "
                     f"False; ALV-007-S03 refuses an evaluation-specific "
                     f"purpose for this ring")

    # ---- data classes: permitted from §7.9, forbidden from the registry ----
    dc = _as_mapping(f, cat, f"{rp} data_classes", doc.get("data_classes"))
    permitted = _strings_in(f, cat, f"{rp} data_classes.permitted",
                            dc.get("permitted"))
    if permitted != CHECKLIST_S79_DATA_CLASSES:
        f.error(cat, f"{rp}: data_classes.permitted {sorted(permitted, key=str)} "
                     f"!= {sorted(CHECKLIST_S79_DATA_CLASSES)}; the ruled Fork 4 "
                     f"Option C classes are exactly those two")
    ret_reg = AVC / "registries" / "retention-classes.registry.yaml"
    reserved: set[str] = set()
    if ret_reg.is_file():
        rreg = "contracts/avatar-client/registries/retention-classes.registry.yaml"
        reserved = _ids_in(
            f, cat, f"{rreg} reserved",
            _as_mapping(f, cat, rreg, load_yaml(ret_reg)).get("reserved"))
    never = _strings_in(
        f, cat, f"{rp} data_classes.never_instantiated.classes",
        _as_mapping(f, cat, f"{rp} data_classes.never_instantiated",
                    dc.get("never_instantiated")).get("classes"))
    if reserved and never != reserved:
        f.error(cat, f"{rp}: data_classes.never_instantiated.classes "
                     f"{sorted(never, key=str)} != the registry's reserved set "
                     f"{sorted(reserved)}; all four stay forbidden and this "
                     f"ring instantiates none of them")
    if permitted & reserved:
        f.error(cat, f"{rp}: data_classes permits reserved class(es) "
                     f"{sorted(permitted & reserved)}")

    # ---- retention: read the ruled values from the checklist, not a copy ----
    ck_path = AVC / CHECKLIST_FILE
    ruled_ret: dict = {}
    if ck_path.is_file():
        ckp = f"contracts/avatar-client/{CHECKLIST_FILE}"
        ck = _as_mapping(f, cat, ckp, load_yaml(ck_path))
        for cond in _mappings_in(f, cat, f"{ckp} conditions",
                                 ck.get("conditions")):
            if cond.get("number") == CHECKLIST_S79_CONDITION:
                ruled_ret = _as_mapping(
                    f, cat, f"{ckp} condition 2 ruled_values.retention",
                    _as_mapping(f, cat, f"{ckp} condition 2 ruled_values",
                                cond.get("ruled_values")).get("retention"))
                break
    ret = _as_mapping(f, cat, f"{rp} retention", doc.get("retention"))
    if ruled_ret:
        for key in ("window_days", "policy_ref", "applies_to"):
            if ret.get(key) != ruled_ret.get(key):
                f.error(cat, f"{rp}: retention.{key} is {ret.get(key)!r} but the "
                             f"checklist's §7.9 ruling says "
                             f"{ruled_ret.get(key)!r}; the ruled value has one "
                             f"home and this artifact cites it")
    elif ck_path.is_file():
        f.error(cat, f"{rp}: the checklist declares no §7.9 retention block to "
                     f"check this envelope's window and reference against")

    # ---- withdrawal: the existing outcome, reachable mid-session ----
    wd = _as_mapping(f, cat, f"{rp} withdrawal", doc.get("withdrawal"))
    if wd.get("maps_to_outcome") != ENVELOPE_WITHDRAWAL_OUTCOME:
        f.error(cat, f"{rp}: withdrawal.maps_to_outcome is "
                     f"{wd.get('maps_to_outcome')!r} != "
                     f"{ENVELOPE_WITHDRAWAL_OUTCOME!r}")
    if wd.get("new_outcome_tokens_introduced") != 0:
        f.error(cat, f"{rp}: withdrawal.new_outcome_tokens_introduced is "
                     f"{wd.get('new_outcome_tokens_introduced')!r} != 0; the "
                     f"closed session-outcomes registry gains no member here")
    out_reg = AVC / "registries" / "session-outcomes.registry.yaml"
    if out_reg.is_file():
        oreg = "contracts/avatar-client/registries/session-outcomes.registry.yaml"
        outcomes = _ids_in(
            f, cat, f"{oreg} members",
            _as_mapping(f, cat, oreg, load_yaml(out_reg)).get("members"))
        if wd.get("maps_to_outcome") not in outcomes:
            f.error(cat, f"{rp}: withdrawal.maps_to_outcome "
                         f"{wd.get('maps_to_outcome')!r} is not a member of the "
                         f"released session-outcomes registry")
    for flag in ("reachable_mid_session", "reachable_mid_speech"):
        if wd.get(flag) is not True:
            f.error(cat, f"{rp}: withdrawal.{flag} is {wd.get(flag)!r}; task "
                         f"6.2.2 requires withdrawal to STAY REACHABLE during a "
                         f"session")
    proof = _as_mapping(f, cat, f"{rp} withdrawal.reachability_proof",
                        wd.get("reachability_proof"))
    # THE RAW VALUE GOES TO THE GUARD, UNCOERCED. `str(value or "")` in front
    # of `_repo_file` defeats the very check it looks like it is helping:
    # `str(["x"])` is `"['x']"`, a non-empty STRING, so the non-string guard
    # cannot fire, the name resolves as an ordinary relative path inside the
    # tree, and a malformed shape is then reported as a missing file — the
    # wrong finding, arrived at by throwing away the evidence.
    raw = proof.get("fixture")
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        f.error(cat, f"{rp}: withdrawal.reachability_proof names no fixture; a "
                     f"reachability claim with no proof is an assertion")
    else:
        fx = _repo_file(f, cat, f"{rp} withdrawal.reachability_proof.fixture",
                        raw)
        if fx is None:
            pass  # refused above with the reason; never touched the filesystem
        # `_repo_file` accepted it, so it IS a non-blank string; coercing is
        # safe only here, AFTER the guard rather than in front of it.
        elif not fx.is_file():
            f.error(cat, f"{rp}: withdrawal.reachability_proof.fixture "
                         f"{raw!r} does not exist; the proof is a filename")
        else:
            claimed = str(raw)
            fid = _as_mapping(f, cat, claimed, load_yaml(fx)).get("fixture_id")
            if fid != proof.get("fixture_id") or fid != WITHDRAWAL_FIXTURE_ID:
                f.error(cat, f"{rp}: the cited fixture's fixture_id is {fid!r}, "
                             f"which does not match the envelope's "
                             f"{proof.get('fixture_id')!r} / the landed "
                             f"{WITHDRAWAL_FIXTURE_ID!r}")

    # ---- §6.2.4: the non-shadowing control stays OPERATIONAL ----
    controls = {c.get("control"): c for c in _mappings_in(
        f, cat, f"{rp} operational_controls",
        doc.get("operational_controls"))}
    shadow = controls.get(ENVELOPE_SHADOW_CONTROL)
    if shadow is None:
        f.error(cat, f"{rp}: no operational control named "
                     f"{ENVELOPE_SHADOW_CONTROL!r}; task 6.2.4 requires the "
                     f"non-shadowing guarantee to be RECORDED as one")
        return
    if shadow.get("enforced_by_schema") is not False:
        f.error(cat, f"{rp}: the non-shadowing control records "
                     f"enforced_by_schema="
                     f"{shadow.get('enforced_by_schema')!r}; NO schema field "
                     f"forbids a second-model shadow today and claiming "
                     f"otherwise would be false (task 6.2.4)")
    if shadow.get("enforcement") != "operational":
        f.error(cat, f"{rp}: the non-shadowing control records enforcement="
                     f"{shadow.get('enforcement')!r} != 'operational'")
    flag = _as_mapping(
        f, cat, f"{rp} {ENVELOPE_SHADOW_CONTROL} enforcing_contract_flag",
        shadow.get("enforcing_contract_flag"))
    if flag.get("status") != "deferred":
        f.error(cat, f"{rp}: the enforcing contract flag records status="
                     f"{flag.get('status')!r} != 'deferred'; it is not built")
    if flag.get("owner_change") != ENVELOPE_PILOT_SUCCESSOR:
        f.error(cat, f"{rp}: the enforcing contract flag names owner_change="
                     f"{flag.get('owner_change')!r} != "
                     f"{ENVELOPE_PILOT_SUCCESSOR!r}; task 6.2.4 requires the "
                     f"enforcing flag to be named as pilot-hardening work")


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
        try:
            errs = list(Draft202012Validator(sdoc, registry=registry)
                        .iter_errors(c.get("instance")))
        except Exception as exc:  # noqa: BLE001
            # A `$ref` that cannot resolve is a BROKEN REGISTRY, not a fixture
            # result. It happens when a schema the registry depends on failed
            # to parse: that parse failure is already a finding, the run
            # continues to report everything else, and then this raised
            # `Unresolvable` out of jsonschema and ended the run as an
            # anonymous harness failure. A case that cannot be executed is
            # recorded as a case that did not pass — fail closed.
            f.error("fixture-unresolvable",
                    f"{cid}: target {target!r} could not be executed "
                    f"({type(exc).__name__}: {str(exc)[:120]}); a fixture that "
                    f"cannot run is never counted as passing")
            continue
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
    if not isinstance(amap, dict):
        # A top-level list is valid YAML and a malformed acceptance map. Reading
        # it as a mapping raised straight out of this function and aborted the
        # whole run with a harness failure, so the traceability check that this
        # very function performs never got to report anything. Refuse it as a
        # finding instead, the way every other reader here refuses one.
        f.error("acceptance-map",
                "contracts/avatar-client/acceptance-map.yaml does not load as a "
                "mapping; requirement and scenario traceability is unverifiable "
                "(fail closed)")
        return
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
    if not isinstance(doc, dict):
        # An unreadable released map indexes to nothing rather than raising; the
        # caller's parity check then reports the mismatch as a finding, and the
        # readers that own this file report the shape itself.
        return idx
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
            # Both of these are YAML-SUPPLIED PATHS joined to the repository
            # root and then handed to the filesystem — `discharge_via` is
            # `load_yaml`d — so they go through the same containment guard the
            # §6.2 and §7 readers use. An absolute value discards the root and
            # a `..` segment walks out of the tree; either would make a
            # contract artifact an arbitrary-file-read on the runner.
            fx = s.get("fixture")
            if fx is not None:
                fxp = _repo_file(f, "client-lab-fixture",
                                 f"{rp}: scenario {sid} fixture", fx)
                if fxp is not None and not fxp.is_file():
                    f.error("client-lab-fixture", f"{rp}: scenario {sid} fixture {fx} does not exist")
            dv = s.get("discharge_via")
            if dv is not None:
                dvp = _repo_file(f, "client-lab-discharge",
                                 f"{rp}: scenario {sid} discharge_via", dv)
                if dvp is None:
                    pass  # refused with its reason; the filesystem is untouched
                elif not dvp.is_file():
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


def check_interface_lock(f: Findings) -> None:
    """ACR-001-S04 (evidence-register check `interface_lock_reserved_set`):
    machine-check `interface-lock.yaml`'s frozen contract/reserved lists against
    this validator's own CONTRACT_FILES / RESERVED_IDS constants.

    The constants MIRROR the lock by hand rather than reading it — deliberately,
    so the file that declares the freeze and the tool that enforces it are two
    independent statements — but an unchecked hand mirror drifts. This makes the
    two disagree LOUDLY instead of silently, which is what `qualify-avatar-live-
    voice` needed when it moved exactly AVC-09 and AVC-10 out of the reserved
    set: an unreservation that edits one and forgets the other is now a finding,
    and so is releasing a THIRD reserved identifier along the way.

    Fail closed on a missing or unreadable lock."""
    path = AVC / "interface-lock.yaml"
    rp = "contracts/avatar-client/interface-lock.yaml"
    if not path.is_file():
        f.error("interface-lock", f"{rp} absent; the frozen baseline is unverifiable (fail closed)")
        return
    doc = load_yaml(path) or {}
    frozen = doc.get("frozen") if isinstance(doc, dict) else None
    if not isinstance(frozen, dict):
        f.error("interface-lock", f"{rp}: `frozen` block missing or not a mapping (fail closed)")
        return
    locked = frozen.get("contracts") or []
    reserved = frozen.get("reserved_identifiers") or []
    if not isinstance(locked, list) or not isinstance(reserved, list):
        f.error("interface-lock", f"{rp}: `contracts` and `reserved_identifiers` must be lists")
        return
    if len(locked) != len(set(locked)):
        f.error("interface-lock", f"{rp}: duplicate id in frozen.contracts")
    if len(reserved) != len(set(reserved)):
        f.error("interface-lock", f"{rp}: duplicate id in frozen.reserved_identifiers")
    if set(locked) != set(CONTRACT_FILES):
        f.error("interface-lock",
                f"{rp}: frozen.contracts {sorted(set(locked))} != the validator's published set "
                f"{sorted(CONTRACT_FILES)} — the lock and CONTRACT_FILES must move in the same change")
    if set(reserved) != RESERVED_IDS:
        f.error("interface-lock",
                f"{rp}: frozen.reserved_identifiers {sorted(set(reserved))} != the validator's "
                f"reserved set {sorted(RESERVED_IDS)} — unreserving an id edits BOTH or neither")
    overlap = set(locked) & set(reserved)
    if overlap:
        f.error("interface-lock",
                f"{rp}: {sorted(overlap)} is both published and reserved; an identifier is one or "
                f"the other and is never reused")


def _slo_entries(node: Any) -> list[dict]:
    """Every mapping in the acceptance map that declares itself a neutral
    relative-regression SLO. Collected by walking rather than by reading one
    known key, so a SECOND entry hidden under another key is found too — 'exactly
    one' has to mean exactly one in the document, not one where we looked."""
    found: list[dict] = []
    if isinstance(node, dict):
        if node.get("kind") == SLO_KIND:
            found.append(node)
        for v in node.values():
            found.extend(_slo_entries(v))
    elif isinstance(node, list):
        for item in node:
            found.extend(_slo_entries(item))
    return found


def _ceiling_keys_in_properties(node: Any) -> list[str]:
    """Property NAMES under any `properties` mapping that read as a numeric
    latency ceiling. Only property names are inspected: AVC-09 and AVC-10 name
    these same strings inside their `not` blocks precisely in order to forbid
    them, and a scan that could not tell a prohibition from a declaration would
    fail the very schemas doing the prohibiting."""
    hits: list[str] = []
    if isinstance(node, dict):
        props = node.get("properties")
        if isinstance(props, dict):
            hits.extend(k for k in props if isinstance(k, str) and LATENCY_CEILING_KEY.match(k))
        for k, v in node.items():
            if k == "not":
                continue
            hits.extend(_ceiling_keys_in_properties(v))
    elif isinstance(node, list):
        for item in node:
            hits.extend(_ceiling_keys_in_properties(item))
    return hits


def _ceiling_keys_in_mapping(node: Any) -> list[str]:
    hits: list[str] = []
    if isinstance(node, dict):
        hits.extend(k for k in node if isinstance(k, str) and LATENCY_CEILING_KEY.match(k))
        for v in node.values():
            hits.extend(_ceiling_keys_in_mapping(v))
    elif isinstance(node, list):
        for item in node:
            hits.extend(_ceiling_keys_in_mapping(item))
    return hits


def _evaluate_comparison(case: dict) -> tuple[str, str]:
    """Apply the neutral relative-regression rule to one comparison case.

    WHAT A CASE'S `tier` MEANS: it is the case's own INPUT CLAIM about which
    tier the comparison is offered for, not a fact this function reads off the
    samples. That distinction decides every off-nominal outcome below, so it is
    stated rather than left to be inferred.

    Returns (outcome, why). Outcomes:

    - ``refused``  — the pair is not evidence at all, in one of two ways. Either
      the two sides do not share a comparable cell (mismatched platform, network
      class or region, or a reference side that is not a direct-provider
      reference), or the case CLAIMS THE GATED TIER from a cell that cannot
      gate — off-nominal network, a non-gated delivery platform, or Linux CI,
      which is reference-generation only.
    - ``recorded`` — a comparable pair that does NOT claim the gated tier: a
      tail percentile, a tail interval, or a degraded/jittered network run.
      Measured and reported as informational tail evidence; gates nothing.
    - ``fail``     — a comparable, gated pair whose adapter percentile is a
      MATERIAL regression: ``adapter > reference + max(0.15 * reference, 150)``.
    - ``pass``     — a comparable, gated pair that is not a material regression.

    THE ORDER IS LOAD-BEARING. Cell comparability is checked first and beats
    everything: a comparison across mismatched conditions must never be
    evaluated, not even to a passing number. The gated-tier CLAIM is resolved
    next, because the ratified rule says degraded-network evidence "MAY be
    recorded but MUST NOT substitute for the nominal-network gated cells" — so
    off-nominal refusal has to attach to the CLAIM, not to the network class
    itself. Refusing every off-nominal comparison outright would make the
    recorded tier unreachable and contradict the acceptance map, which lists
    degraded and jittered under `recorded_not_gated.network_classes`.
    """
    ref, adp = case.get("reference") or {}, case.get("adapter") or {}
    if ref.get("classification") != "direct_provider_reference":
        return "refused", ("the reference side is not classified "
                           f"direct_provider_reference (got {ref.get('classification')!r})")
    if adp.get("classification") != "governed_adapter":
        return "refused", ("the adapter side is not classified governed_adapter "
                           f"(got {adp.get('classification')!r})")
    for axis in SLO_CELL_AXES:
        if ref.get(axis) != adp.get(axis):
            return "refused", (f"{axis} differs ({ref.get(axis)!r} vs {adp.get(axis)!r}); "
                               f"the SLO is defined only within a matching cell")
    claims_gated = (case.get("tier") == "gated"
                    and case.get("percentile") in SLO_GATED_PERCENTILES
                    and case.get("interval") in SLO_GATED_INTERVALS)
    if not claims_gated:
        return "recorded", ("tail evidence: recorded, never gating at the internal-live ring")
    platform = adp.get("platform")
    if platform in SLO_REFERENCE_ONLY_PLATFORMS:
        return "refused", (f"the case claims the gated tier, but {platform} is "
                           f"reference-generation only and is never a gated delivery platform")
    if platform not in SLO_GATED_PLATFORMS:
        return "refused", (f"the case claims the gated tier, but {platform!r} is not one of "
                           f"the gated delivery platforms")
    if adp.get("network_class") != SLO_GATED_NETWORK:
        return "refused", (f"the case claims the gated tier from network_class "
                           f"{adp.get('network_class')!r}; such a run MAY be recorded as tail "
                           f"evidence but never substitutes for a nominal-network gated cell")
    reference_ms, adapter_ms = ref.get("value_ms"), adp.get("value_ms")
    if not isinstance(reference_ms, (int, float)) or not isinstance(adapter_ms, (int, float)):
        return "refused", "a side carries no numeric value_ms"
    allowance = max(SLO_RELATIVE_PCT / 100.0 * reference_ms, float(SLO_ABSOLUTE_MS))
    if adapter_ms > reference_ms + allowance:
        return "fail", (f"{adapter_ms} exceeds {reference_ms} + max(15%, 150 ms) = "
                        f"{reference_ms + allowance}")
    return "pass", (f"{adapter_ms} is within {reference_ms} + max(15%, 150 ms) = "
                    f"{reference_ms + allowance}")


def check_latency_posture(f: Findings) -> set[str]:
    """§3.3: enforce the two-tier latency posture, fail-closed, and return the
    evidence ids the comparison cases carry so the evidence register can resolve
    them the way it resolves a fixture id.

    Three obligations, all from `qualify-avatar-live-voice`'s ratified rulings:

    1. EXACTLY ONE neutral relative-regression SLO entry lives in the acceptance
       map, at the ratified threshold — more than 15 percent relative OR more
       than 150 ms absolute, WHICHEVER IS GREATER. Zero entries fails closed
       (an ungated ring), two fail too (two rules say nothing about which binds),
       and a threshold that disagrees with the ratified numbers fails whichever
       direction it drifts.
    2. THE TWO TIERS ARE DECLARED AND DISJOINT. p50 and p95 on the two setup
       intervals, on Windows desktop and web canvas at nominal network, are
       GATED. p99, teardown, degraded and jittered network, and steady-state
       per-turn latency are RECORDED and gate nothing. A gated percentile that
       also appears in the recorded tier would make the posture unreadable.
    3. NO PER-PROFILE NUMERIC LATENCY CEILING is presented as a gating field —
       not as a property of any avatar-client schema, and not as a key in the
       acceptance map. That is Fork 2's Option B, which was not ruled.
    """
    evidence_ids: set[str] = set()
    amap_path = AVC / "acceptance-map.yaml"
    if not amap_path.is_file():
        f.error("latency-posture",
                "acceptance-map.yaml absent; the relative-regression SLO is unverifiable (fail closed)")
        return evidence_ids
    amap = load_yaml(amap_path) or {}

    # --- 1. exactly one SLO entry, at the ratified threshold ---
    entries = _slo_entries(amap)
    if not entries:
        f.error("latency-posture",
                f"no acceptance-map entry declares kind {SLO_KIND!r}; the internal-live ring "
                f"would be ungated (fail closed)")
        return evidence_ids
    if len(entries) > 1:
        ids = [e.get("id") for e in entries]
        f.error("latency-posture",
                f"{len(entries)} neutral relative-regression SLO entries in the acceptance map "
                f"({ids}); exactly one may exist, because two rules say nothing about which binds")
        return evidence_ids
    slo = entries[0]
    mat = slo.get("materiality") or {}
    if mat.get("rule") != SLO_MATERIALITY_RULE:
        f.error("latency-posture",
                f"SLO materiality rule {mat.get('rule')!r} != {SLO_MATERIALITY_RULE!r}; the "
                f"'whichever is greater' clause is load-bearing")
    if mat.get("relative_threshold_pct") != SLO_RELATIVE_PCT:
        f.error("latency-posture",
                f"SLO relative threshold {mat.get('relative_threshold_pct')!r} != the ratified "
                f"{SLO_RELATIVE_PCT} percent")
    if mat.get("absolute_threshold_ms") != SLO_ABSOLUTE_MS:
        f.error("latency-posture",
                f"SLO absolute threshold {mat.get('absolute_threshold_ms')!r} != the ratified "
                f"{SLO_ABSOLUTE_MS} ms")
    cell = slo.get("comparison_cell") or {}
    if set(cell.get("must_match") or []) != set(SLO_CELL_AXES):
        f.error("latency-posture",
                f"SLO comparison cell axes {sorted(set(cell.get('must_match') or []))} != "
                f"{sorted(SLO_CELL_AXES)}")

    # --- 2. the two tiers, declared and disjoint ---
    gated = slo.get("gated") or {}
    recorded = slo.get("recorded_not_gated") or {}
    gp = set(gated.get("percentiles") or [])
    gi = set(gated.get("intervals") or [])
    if gp != SLO_GATED_PERCENTILES:
        f.error("latency-posture",
                f"SLO gated percentiles {sorted(gp)} != {sorted(SLO_GATED_PERCENTILES)}")
    if gi != SLO_GATED_INTERVALS:
        f.error("latency-posture",
                f"SLO gated intervals {sorted(gi)} != {sorted(SLO_GATED_INTERVALS)}")
    if set(gated.get("platforms") or []) != SLO_GATED_PLATFORMS:
        f.error("latency-posture",
                f"SLO gated platforms {sorted(set(gated.get('platforms') or []))} != "
                f"{sorted(SLO_GATED_PLATFORMS)}; Linux CI is reference-generation only")
    if gated.get("network_class") != SLO_GATED_NETWORK:
        f.error("latency-posture",
                f"SLO gated network class {gated.get('network_class')!r} != {SLO_GATED_NETWORK!r}")
    rp_set = set(recorded.get("percentiles") or [])
    ri_set = set(recorded.get("intervals") or [])
    if "p99" not in rp_set:
        f.error("latency-posture", "SLO recorded tier must name p99 as recorded-not-gated")
    if not any(i.startswith("teardown") for i in ri_set):
        f.error("latency-posture",
                "SLO recorded tier must name the teardown / hangup-to-terminal interval")
    if gp & rp_set:
        f.error("latency-posture",
                f"percentile(s) {sorted(gp & rp_set)} are declared BOTH gated and recorded-not-gated")
    if gi & ri_set:
        f.error("latency-posture",
                f"interval(s) {sorted(gi & ri_set)} are declared BOTH gated and recorded-not-gated")
    if set(slo.get("reference_generation_only_platforms") or []) != SLO_REFERENCE_ONLY_PLATFORMS:
        f.error("latency-posture",
                f"SLO reference-generation-only platforms "
                f"{sorted(set(slo.get('reference_generation_only_platforms') or []))} != "
                f"{sorted(SLO_REFERENCE_ONLY_PLATFORMS)}")

    # --- 3. no per-profile numeric latency ceiling anywhere ---
    for name in sorted(AVC.glob("*.schema.yaml")):
        try:
            doc = load_yaml(name)
        except yaml.YAMLError:
            continue  # reported by build_registry
        for key in sorted(set(_ceiling_keys_in_properties(doc))):
            f.error("latency-ceiling",
                    f"{name.name}: property {key!r} is a per-profile numeric latency ceiling; "
                    f"latency gating is the neutral relative-regression SLO, and the measured "
                    f"numbers live in AVC-10 samples")
    for key in sorted(set(_ceiling_keys_in_mapping(amap))):
        f.error("latency-ceiling",
                f"acceptance-map.yaml: key {key!r} presents a numeric latency ceiling as a gating "
                f"field; the only numeric thresholds this map may carry are the SLO's own "
                f"relative and absolute regression allowances")

    # --- execute the self-describing comparison cases ---
    index = AVC / "fixtures" / "index.yaml"
    cases = ((load_yaml(index) or {}).get("latency_comparison_cases") or []) if index.is_file() else []
    if not cases:
        f.error("latency-posture",
                "no latency_comparison_cases in fixtures/index.yaml; the relative-regression rule "
                "and its cross-cell refusal are unproven (fail closed)")
        return evidence_ids
    case_ids: set[str] = set()
    outcomes_seen: set[str] = set()
    for c in cases:
        cid = c.get("case_id")
        if cid in case_ids:
            f.error("latency-case-dup", f"duplicate latency comparison case_id {cid}")
        case_ids.add(cid)
        expect = c.get("expect")
        if expect not in SLO_OUTCOMES:
            f.error("latency-case-expect",
                    f"{cid}: expect must be one of {sorted(SLO_OUTCOMES)}, got {expect!r}")
            continue
        if c.get("class") not in ALL_CLASSES:
            f.error("latency-case-class", f"{cid}: unknown class {c.get('class')!r}")
        if c.get("tier") == "gated" and expect in ("pass", "fail"):
            # A case claiming to close a GATED cell must name a gated percentile
            # and a gated interval, or the two-tier posture is being widened by
            # fixture rather than by ruling.
            if c.get("percentile") not in SLO_GATED_PERCENTILES:
                f.error("latency-case-tier",
                        f"{cid}: gated case names percentile {c.get('percentile')!r}, which is "
                        f"recorded-not-gated at this ring")
            if c.get("interval") not in SLO_GATED_INTERVALS:
                f.error("latency-case-tier",
                        f"{cid}: gated case names interval {c.get('interval')!r}, which is "
                        f"recorded-not-gated at this ring")
        actual, why = _evaluate_comparison(c)
        outcomes_seen.add(actual)
        if actual != expect:
            f.error("latency-case", f"{cid}: expected {expect} but got {actual} ({why})")
        elif c.get("evidence_id"):
            evidence_ids.add(c["evidence_id"])
    for need in sorted(SLO_OUTCOMES - outcomes_seen):
        f.error("latency-coverage",
                f"no latency comparison case exercises the {need!r} outcome; the two-tier posture "
                f"is not proven end to end")
    return evidence_ids


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
