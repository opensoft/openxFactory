#!/usr/bin/env python3
"""Validate ideation-area dashboard contract artifacts (add-ideation-dashboard).

Change task 2.4 (`openspec/changes/add-ideation-dashboard/tasks.md`): a strict
validator for the ideation-dashboard snapshot, the workbench manifest, the
possibles-register consolidation section (and its cross-snapshot TRANSITIONS),
plus the sibling project-register (task 2.6) and gate-action record (task 2.8)
schemas — the same contract family. It layers the deterministic invariants JSON
Schema alone cannot express (documented in each schema's own comments — those
comments ARE the requirements) on top of plain draft-2020-12 validation, and it
attaches a `FormatChecker` so `date`/`date-time` are actually enforced rather
than left as annotations.

The schema family under `contracts/schemas/` (all loaded into one offline
registry so the register kernel's cross-file `$ref` into the snapshot's
`evidence_pin` resolves):
    ideation-dashboard-snapshot.schema.yaml   (kind: ideation-dashboard-snapshot)
    ideation-dashboard-snapshot-index.schema.yaml
                                              (kind:
                                               ideation-dashboard-snapshot-index;
                                               the (repository, ref) locator,
                                               add-dashboard-repo-selector)
    ideation-workbench.schema.yaml            (kind: ideation-workbench)
    ideation-possibles-register.schema.yaml   (envelope-less $defs kernel;
                                               fixtures wrap it under a plain
                                               `possibles_register:` container key)
    project-register.schema.yaml              (kind: project-register)
    gate-action-record.schema.yaml            (kind: gate-action-record)

Validator-side rules beyond plain schema conformance:

  Snapshot   referential integrity: cluster `document_edges` -> existing
             `documents[].id`; possible `claiming_clusters` -> existing
             `clusters[].id`; `option_set.members` -> existing `possibles[].id`.
             `keyword_index` consistency with declared topics is a WARNING
             (the generator may deliberately scope keywords), never an error.
  Index      every (repository, ref) pair is UNIQUE within one snapshot index,
             and the index carries NO projection data (documents/clusters/
             possibles/staged_topics/changes/keyword_index, at the root or in an
             entry) — it is a locator, not a projection (D3).
  Workbench  recipe `pinned` keywords must be a subset of `checked`;
             `recipe.new_candidates` must be disjoint from members ∪ excluded;
             AND — the committed-manifest guard — a well-formed workbench
             manifest found in TRACKED repository content (outside the
             reference `examples/` tree, which is static material) is an error:
             saved manifests belong under gitignored `ideation/workbench/`.
  Register   `id` uniqueness within one register (including AI-derived entries);
             and, in TRANSITION mode (`--transition OLD NEW`), state-machine
             legality across the pair: latent->picked|rejected|superseded,
             picked->superseded only, rejected/superseded terminal, NO entry
             deletion / resurrection (a removed id is an error; a re-used id with
             a different identity is an error). Per-state field requirements
             (reason+citation for rejected/superseded; pick.staging_id for
             picked) are re-checked through the transition path.
  Derived    AI-derived register entries (add-possibles-derivation-lane; the
             kernel's additive `origin`/`derivation` delta). Single-instance:
             an `origin: ai-derived` entry carries a `derivation` block, cites at
             least one `claiming_clusters` edge AND one `supporting_evidence` pin
             (never an unsourced assertion), and its machine
             `derivation.disposition` is `pending_review` only. TRANSITION mode:
             the one-way disposition lifecycle — a possible's origin is fixed (an
             accepted derived possible retains `origin: ai-derived`), and a
             disposed derived possible (a recorded `human_disposition`) is never
             edited back to the undisposed `pending_review` state.
  Project    `id` uniqueness (projects and groups); every group-member project
             id must exist; a project in at most one group (the snapshot's
             `project_group` is singular). Repository membership is
             MULTI-PARENT (Brett's 2026-08-06 ruling): a repository may live
             in any number of projects; the snapshot's singular `project` is
             the first-declaring PRIMARY and `projects` carries them all.
  Gate       a `kickoff` record requires its target change to carry a recorded
             ratification (D17). This is a cross-instance precondition: supply
             `--context FILE|DIR` (a snapshot whose `changes[]` carry
             ratification, and/or sibling gate-action `ratify` records), or, in
             a directory sweep, sibling records provide it automatically. With
             no context available the precondition is reported SKIPPED, never
             silently passed.

Usage:
    # Default: self-test the packaged examples, scan the repo tree for real
    # instances, and run the committed-manifest guard.
    python3 scripts/validate-ideation-dashboard-contracts.py [REPO] [--strict]

    # Validate one file (kind auto-detected) or a directory sweep.
    python3 scripts/validate-ideation-dashboard-contracts.py PATH [--context F] [--strict]

    # Register transition legality across two register sections.
    python3 scripts/validate-ideation-dashboard-contracts.py --transition OLD NEW [--strict]

Exit codes: 0 ok, 1 findings (or warnings under --strict), 2 harness error.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
EXAMPLES_DIR = ROOT / "examples" / "ideation-dashboard"

SCHEMA_FILENAMES = [
    "ideation-dashboard-snapshot.schema.yaml",
    "ideation-dashboard-snapshot-index.schema.yaml",
    "ideation-workbench.schema.yaml",
    "ideation-possibles-register.schema.yaml",
    "xfactory-workbench-model-catalog.schema.yaml",
    "xfactory-workbench-chat-turn.schema.yaml",
    "project-register.schema.yaml",
    "gate-action-record.schema.yaml",
    "gate-intent.schema.yaml",
]

# Whole-document schemas keyed by the hyphenated `kind` literal each declares.
KIND_TO_SCHEMA = {
    "ideation-dashboard-snapshot": "ideation-dashboard-snapshot.schema.yaml",
    "ideation-dashboard-snapshot-index": "ideation-dashboard-snapshot-index.schema.yaml",
    "ideation-workbench": "ideation-workbench.schema.yaml",
    "project-register": "project-register.schema.yaml",
    "gate-action-record": "gate-action-record.schema.yaml",
    "gate-intent": "gate-intent.schema.yaml",
    # doxBench wire family (add-workbench-integrated-editor-chat task 2.1):
    # instance kinds use the retained `workbench-*` identifier family; the
    # chat-turn file holds three envelopes discriminated by a oneOf.
    "workbench-model-catalog": "xfactory-workbench-model-catalog.schema.yaml",
    "workbench-chat-turn": "xfactory-workbench-chat-turn.schema.yaml",
    "workbench-chat-turn-success": "xfactory-workbench-chat-turn.schema.yaml",
    "workbench-chat-turn-failure": "xfactory-workbench-chat-turn.schema.yaml",
    # The co-resident WIDENED family (contract-v1.34,
    # add-doxbench-editing-phase-b design D15). Same file, same oneOf; the v1
    # kinds above are DEPRECATED but still validated, because a deprecation that
    # stopped validating would break the clients it exists to keep working.
    "workbench-chat-turn-v2": "xfactory-workbench-chat-turn.schema.yaml",
    "workbench-chat-turn-v2-success": "xfactory-workbench-chat-turn.schema.yaml",
    "workbench-chat-turn-v2-failure": "xfactory-workbench-chat-turn.schema.yaml",
}

# The snapshot's projection collections — the data an INDEX must never carry
# (`ideation-dashboard-snapshot-index.schema.yaml`, design D3: the index is a
# locator, not a projection).
PROJECTION_KEYS = (
    "documents", "clusters", "possibles", "staged_topics", "changes",
    "keyword_index",
)
DEFAULT_REF = "main"  # a consumer that names no ref means `main` (D4)

# The possibles register is an envelope-less `$defs` kernel (no kind/envelope of
# its own — it is embedded as a section of the cross-reference index). Fixtures
# and register instances wrap the section under this plain container key, the
# same convention document-cataloging's locator/handling-gate kernels use.
REGISTER_SCHEMA = "ideation-possibles-register.schema.yaml"
REGISTER_CONTAINER_KEY = "possibles_register"
REGISTER_SECTION_REF = f"{REGISTER_SCHEMA}#/$defs/possibles_register"

# A single FormatChecker shared by every validator: the ledger's first rule is
# that date/date-time must be enforced, not merely annotated. jsonschema only
# registers the date-time checker when rfc3339-validator is importable, so a
# bare environment would silently accept malformed timestamps — fail closed
# instead of validating vacuously.
FORMAT_CHECKER = FormatChecker()
if not {"date", "date-time"} <= set(FORMAT_CHECKER.checkers):  # pragma: no cover
    print(
        "ERROR jsonschema is missing its date/date-time format checkers; "
        "install rfc3339-validator (see "
        "requirements/hermes-runtime-contracts.in) so `format: date` and "
        "`format: date-time` are enforced",
        file=sys.stderr,
    )
    sys.exit(2)

# Legal possibles-register state transitions (documented in the schema).
LEGAL_TRANSITIONS: dict[str, set[str]] = {
    "latent": {"latent", "picked", "rejected", "superseded"},
    "picked": {"picked", "superseded"},
    "rejected": {"rejected"},
    "superseded": {"superseded"},
}
TERMINAL_STATES = {"rejected", "superseded"}


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


# --------------------------- schema registry ---------------------------

def build_registry() -> tuple[Registry, dict[str, dict]]:
    """Offline registry over all five schemas so the register kernel's
    cross-file `$ref` into the snapshot's `evidence_pin` resolves (same
    approach as scripts/validate-document-catalog.py / validate-avatar-client.py)."""
    resources = []
    docs: dict[str, dict] = {}
    for name in SCHEMA_FILENAMES:
        doc = load_yaml(SCHEMAS_DIR / name)
        docs[name] = doc
        rid = doc.get("$id", name)
        resources.append((rid, Resource.from_contents(doc, default_specification=DRAFT202012)))
    return Registry().with_resources(resources), docs


def doc_validator(schema_name: str, registry: Registry, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(docs[schema_name], registry=registry, format_checker=FORMAT_CHECKER)


def section_validator(registry: Registry) -> Draft202012Validator:
    """Validator for the whole `possibles_register` section, resolved through
    the registry exactly as the cross-reference index `$ref`s it."""
    return Draft202012Validator({"$ref": REGISTER_SECTION_REF}, registry=registry,
                                format_checker=FORMAT_CHECKER)


def iter_errors(validator: Draft202012Validator, instance: Any):
    return sorted(validator.iter_errors(instance), key=lambda e: [str(p) for p in e.absolute_path])


def detect(doc: Any) -> str | None:
    """Return a routing tag for a loaded document: a known `kind`, or the
    register-section container, or None (unrecognized)."""
    if not isinstance(doc, dict):
        return None
    kind = doc.get("kind")
    if kind in KIND_TO_SCHEMA:
        return kind
    if isinstance(doc.get(REGISTER_CONTAINER_KEY), list):
        return "possibles-register-section"
    return None


# --------------------------- context (kickoff precondition) ---------------------------

def ratified_change_ids_from(doc: Any) -> set[str]:
    """Extract change ids that carry a recorded ratification from a context
    document — a snapshot (`changes[].ratification`) or a gate-action `ratify`
    record (its `target.change_id`)."""
    out: set[str] = set()
    if not isinstance(doc, dict):
        return out
    if doc.get("kind") == "ideation-dashboard-snapshot":
        for ch in doc.get("changes") or []:
            if isinstance(ch, dict) and ch.get("ratification") and ch.get("id"):
                out.add(ch["id"])
    if doc.get("kind") == "gate-action-record" and doc.get("action") == "ratify":
        cid = (doc.get("target") or {}).get("change_id")
        if cid:
            out.add(cid)
    return out


def load_context(path: Path | None) -> tuple[set[str] | None, list[str]]:
    """Return (ratified_change_ids, notes). None means no context was available
    (kickoff precondition must then be SKIPPED, not passed)."""
    if path is None:
        return None, []
    notes: list[str] = []
    ratified: set[str] = set()
    files: list[Path]
    if path.is_dir():
        files = sorted(list(path.rglob("*.yaml")) + list(path.rglob("*.yml")))
    elif path.is_file():
        files = [path]
    else:
        return None, [f"context path {path} not found; kickoff precondition unavailable"]
    for fp in files:
        try:
            ratified |= ratified_change_ids_from(load_yaml(fp))
        except yaml.YAMLError:
            continue
    notes.append(f"context: {len(ratified)} ratified change id(s) resolved from {path}")
    return ratified, notes


# --------------------- deprecation warnings (read, never restated) ---------------------

def deprecated_kinds(docs: dict[str, dict]) -> dict[str, dict]:
    """Every instance kind a loaded schema declares DEPRECATED, keyed by kind.

    Read from the schemas' own top-level `deprecated_envelopes` blocks. This
    validator never carries its own list of what is deprecated: the release owns
    that statement, and a second copy here would be a second authority that could
    disagree with the bytes consumers actually pin."""
    declared: dict[str, dict] = {}
    for doc in docs.values():
        if not isinstance(doc, dict):
            continue
        for entry in doc.get("deprecated_envelopes") or []:
            if isinstance(entry, dict) and isinstance(entry.get("kind"), str):
                declared[entry["kind"]] = entry
    return declared


def warn_if_deprecated_kind(f: Findings, label: str, tag: str,
                            docs: dict[str, dict]) -> None:
    """WARN, and still accept — the deprecating-change class the versioning
    policy defines ("the conformance validator emits warnings but still accepts
    it"). Without this the deprecation was inert: a release could claim to start
    the clock the breaking path requires while every conforming instance of the
    deprecated shape validated in silence."""
    entry = deprecated_kinds(docs).get(tag)
    if entry is None:
        return
    # CONSEQUENCE, stated: under `--strict` (opt-in, "treat warnings as errors")
    # a deprecated instance now FAILS. That is what strict mode means and what a
    # consumer asking for it wants — a way to find the shapes that will not
    # survive the removal target. The default invocation, which is what this
    # repository's own gates run, still exits 0.
    f.warnings.append(
        f"{label}: kind {tag!r} is DEPRECATED as of "
        f"{entry.get('deprecated_in', 'an unstated release')} — superseded by "
        f"{entry.get('superseded_by', 'no stated replacement')}; removal target "
        f"{entry.get('removal_target', 'unstated')}")


# --------------------- per-instance validation (schema + rules) ---------------------

def validate_instance(
    f: Findings, label: str, doc: Any, registry: Registry, docs: dict[str, dict],
    ratified_changes: set[str] | None, model_ctx: dict[str, int] | None = None,
) -> str | None:
    """Validate one loaded document by detected kind: schema conformance plus
    the family's single-instance validator-side rules. Returns the routing tag
    (so callers can aggregate), or None if unrecognized."""
    tag = detect(doc)
    if tag is None:
        f.error("kind", f"{label}: unrecognized document (no known kind, no {REGISTER_CONTAINER_KEY!r} section)")
        return None

    if tag == "possibles-register-section":
        validator = section_validator(registry)
        for e in iter_errors(validator, doc[REGISTER_CONTAINER_KEY]):
            loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
            f.error("schema", f"{label}: {REGISTER_CONTAINER_KEY}/{loc}: {e.message}")
        check_register_unique_ids(f, label, doc[REGISTER_CONTAINER_KEY])
        check_derived_entries(f, label, doc[REGISTER_CONTAINER_KEY])
        return tag

    schema_name = KIND_TO_SCHEMA[tag]
    for e in iter_errors(doc_validator(schema_name, registry, docs), doc):
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        f.error("schema", f"{label}: {loc}: {e.message}")
    warn_if_deprecated_kind(f, label, tag, docs)

    if tag == "ideation-dashboard-snapshot":
        check_snapshot_referential_integrity(f, label, doc)
    elif tag == "ideation-dashboard-snapshot-index":
        check_snapshot_index_rules(f, label, doc)
    elif tag == "ideation-workbench":
        check_workbench_rules(f, label, doc)
    elif tag == "project-register":
        check_project_register_rules(f, label, doc)
    elif tag == "gate-action-record":
        check_gate_precondition(f, label, doc, ratified_changes)
    elif tag == "workbench-model-catalog":
        check_model_catalog(f, label, doc)
    elif tag == "workbench-chat-turn":
        check_turn_request(f, label, doc, model_ctx)
    elif tag == "workbench-chat-turn-success":
        check_turn_success(f, label, doc)
    elif tag == "workbench-chat-turn-failure":
        check_turn_failure(f, label, doc)
    elif tag == "workbench-chat-turn-v2":
        check_turn_request_v2(f, label, doc, model_ctx)
    elif tag == "workbench-chat-turn-v2-success":
        check_turn_success_v2(f, label, doc)
    elif tag == "workbench-chat-turn-v2-failure":
        # The redaction and limit-pairing rules are the family's, not a
        # per-envelope invention: a v2 failure discloses exactly what a v1
        # failure does, so it is judged by exactly the same function.
        check_turn_failure(f, label, doc)
    return tag


# --------------------------- snapshot referential integrity ---------------------------

def check_snapshot_referential_integrity(f: Findings, label: str, doc: dict) -> None:
    """Internal referential integrity (snapshot schema comments: edges reference
    existing ids). keyword_index/declared-topic consistency is a WARNING."""
    doc_ids = {d.get("id") for d in doc.get("documents") or [] if isinstance(d, dict)}
    cluster_ids = {c.get("id") for c in doc.get("clusters") or [] if isinstance(c, dict)}
    possible_ids = {p.get("id") for p in doc.get("possibles") or [] if isinstance(p, dict)}

    for c in doc.get("clusters") or []:
        if not isinstance(c, dict):
            continue
        cid = c.get("id")
        for edge in c.get("document_edges") or []:
            ref = edge.get("document") if isinstance(edge, dict) else None
            if ref is not None and ref not in doc_ids:
                f.error("snapshot-dangling-edge",
                        f"{label}: cluster {cid!r} document_edge references unknown document {ref!r}")

    for p in doc.get("possibles") or []:
        if not isinstance(p, dict):
            continue
        pid = p.get("id")
        for ref in p.get("claiming_clusters") or []:
            if ref not in cluster_ids:
                f.error("snapshot-dangling-cluster-ref",
                        f"{label}: possible {pid!r} claiming_clusters references unknown cluster {ref!r}")
        opt = p.get("option_set")
        if isinstance(opt, dict):
            for ref in opt.get("members") or []:
                if ref not in possible_ids:
                    f.error("snapshot-dangling-optionset-member",
                            f"{label}: possible {pid!r} option_set references unknown possible {ref!r}")

    # keyword_index consistency vs declared Topics: — WARNING only (the
    # generator may scope keywords rather than emit every declared topic).
    declared_counts: dict[str, int] = {}
    for d in doc.get("documents") or []:
        if not isinstance(d, dict):
            continue
        for t in d.get("topics") or []:
            declared_counts[t] = declared_counts.get(t, 0) + 1
    for entry in doc.get("keyword_index") or []:
        if not isinstance(entry, dict):
            continue
        kw = entry.get("keyword")
        declared = entry.get("declared_doc_count")
        actual = declared_counts.get(kw, 0)
        if isinstance(declared, int) and declared != actual:
            f.warn("keyword-index-drift",
                   f"{label}: keyword {kw!r} declared_doc_count={declared} but {actual} document(s) "
                   f"declare it as a Topics: subject")


# --------------------------- snapshot-index rules ---------------------------

def check_snapshot_index_rules(f: Findings, label: str, doc: dict) -> None:
    """The two validator-side rules the index shape cannot express
    (`ideation-dashboard-snapshot-index.schema.yaml`; add-dashboard-repo-selector
    tasks 1.1-1.2):

      * UNIQUE (repository, ref) — two entries for one pair make "which snapshot
        is this repository's?" ambiguous; and
      * NO PROJECTION DATA — the index is a locator, so a projection collection
        at the root or inside an entry is refused (design D3).
    """
    seen: dict[tuple[str, str], int] = {}
    for entry in doc.get("entries") or []:
        if not isinstance(entry, dict):
            continue
        pair = (entry.get("repository"), entry.get("ref") or DEFAULT_REF)
        seen[pair] = seen.get(pair, 0) + 1
        _check_no_projection_data(f, label, entry, f"entry {pair[0]!r}@{pair[1]!r}")
    for (repo, ref), n in sorted(seen.items(), key=lambda kv: [str(x) for x in kv[0]]):
        if n > 1:
            f.error("snapshot-index-duplicate-repo-ref",
                    f"{label}: (repository, ref) pair ({repo!r}, {ref!r}) appears {n} times "
                    f"(every pair is unique within one index)")
    _check_no_projection_data(f, label, doc, "index root")


def _check_no_projection_data(f: Findings, label: str, obj: dict, where: str) -> None:
    """The locator-not-projection rule: none of the snapshot's projection
    collections may appear in an index (root or entry)."""
    for key in PROJECTION_KEYS:
        if key in obj:
            f.error("snapshot-index-carries-projection-data",
                    f"{label}: {where} carries projection key {key!r} — the index locates "
                    f"snapshots and never restates their contents (D3)")


# --------------------------- workbench rules ---------------------------

def check_workbench_rules(f: Findings, label: str, doc: dict) -> None:
    """Workbench manifest validator-side rules (schema comments): pinned ⊆
    checked, and new_candidates disjoint from members ∪ excluded."""
    recipe = doc.get("recipe")
    if isinstance(recipe, dict):
        checked = set(recipe.get("checked") or [])
        pinned = set(recipe.get("pinned") or [])
        stray = pinned - checked
        if stray:
            f.error("workbench-pinned-not-checked",
                    f"{label}: recipe pinned keyword(s) {sorted(stray)} are not in checked")
        member_docs = {m.get("document") for m in doc.get("members") or [] if isinstance(m, dict)}
        excluded_docs = {e.get("document") for e in doc.get("excluded") or [] if isinstance(e, dict)}
        overlap = set(recipe.get("new_candidates") or []) & (member_docs | excluded_docs)
        if overlap:
            f.error("workbench-candidate-overlap",
                    f"{label}: recipe new_candidates {sorted(overlap)} already appear in members/excluded")


# --------------------------- register single-instance ---------------------------

def check_register_unique_ids(f: Findings, label: str, entries: list) -> None:
    seen: dict[str, int] = {}
    for e in entries or []:
        if isinstance(e, dict) and "id" in e:
            seen[e["id"]] = seen.get(e["id"], 0) + 1
    for rid, n in seen.items():
        if n > 1:
            f.error("register-duplicate-id", f"{label}: register id {rid!r} appears {n} times")


# --------------------------- derived-entry (ai-derived) rules ---------------------------

def _origin(entry: dict) -> str:
    """Normalized register-entry origin — absent defaults to human-authored
    (the kernel's additive `origin` delta)."""
    return entry.get("origin") or "human-authored"


def _human_outcome(entry: dict) -> str | None:
    """The recorded human disposition outcome on a derived entry, or None when
    the entry is undisposed (the machine `derivation.disposition` is
    `pending_review` and no `human_disposition` has been recorded)."""
    deriv = entry.get("derivation")
    if isinstance(deriv, dict):
        hd = deriv.get("human_disposition")
        if isinstance(hd, dict):
            return hd.get("outcome")
    return None


def check_derived_entry(f: Findings, label: str, entry: dict) -> None:
    """Single-instance rules for an `origin: ai-derived` register entry
    (add-possibles-derivation-lane): it carries a `derivation` block, cites at
    least one `claiming_clusters` edge AND one `supporting_evidence` pin (never
    an unsourced assertion), and its machine `derivation.disposition` is
    `pending_review` only. Human-authored entries (origin absent) are skipped."""
    if not isinstance(entry, dict) or _origin(entry) != "ai-derived":
        return
    rid = entry.get("id")
    deriv = entry.get("derivation")
    if not isinstance(deriv, dict):
        # Also caught by the schema allOf; reported here with a register code so
        # the delegated register validator names it directly.
        f.error("register-derived-missing-derivation",
                f"{label}: register id {rid!r} is origin ai-derived but carries no derivation block")
        return
    if not (entry.get("claiming_clusters") or []):
        f.error("register-derived-unsourced",
                f"{label}: derived register id {rid!r} cites no claiming_clusters topic-cluster edge "
                f"(a derived possible must cite at least one cluster edge and one evidence pin)")
    if not (entry.get("supporting_evidence") or []):
        f.error("register-derived-unsourced",
                f"{label}: derived register id {rid!r} cites no supporting_evidence passage pin "
                f"(a derived possible must cite at least one cluster edge and one evidence pin)")
    if deriv.get("disposition") != "pending_review":
        f.error("register-derived-bad-disposition",
                f"{label}: derived register id {rid!r} machine derivation.disposition is "
                f"{deriv.get('disposition')!r}; machine output is always 'pending_review' "
                f"(the human verdict lives in derivation.human_disposition)")


def check_derived_entries(f: Findings, label: str, entries: list) -> None:
    for e in entries or []:
        check_derived_entry(f, label, e)


# --------------------------- register transition ---------------------------

def _entry_map(entries: list) -> dict[str, dict]:
    return {e["id"]: e for e in entries or [] if isinstance(e, dict) and "id" in e}


def _identity(entry: dict) -> tuple:
    prov = entry.get("provenance") or {}
    return (entry.get("claim"), prov.get("document"), prov.get("section"))


def check_register_transition(f: Findings, old_label: str, old: list, new_label: str, new: list) -> None:
    """State-machine legality across an (old, new) register pair (schema comments:
    legal transitions, terminal states, no deletion / no resurrection, stable
    identity). Per-state field requirements are re-checked on the new side."""
    check_register_unique_ids(f, old_label, old)
    check_register_unique_ids(f, new_label, new)
    old_map, new_map = _entry_map(old), _entry_map(new)

    # No entry deletion / no resurrection: an id present in old must remain.
    for rid in old_map:
        if rid not in new_map:
            f.error("register-deletion",
                    f"transition: register id {rid!r} present in {old_label} was removed in {new_label} "
                    f"(entries are never deleted; a returning idea gets a NEW id)")

    for rid, new_entry in new_map.items():
        old_entry = old_map.get(rid)
        if old_entry is None:
            # A brand-new entry — no transition to check, but per-state fields
            # and the derived-entry shape still apply.
            check_entry_state_fields(f, new_label, new_entry)
            check_derived_entry(f, new_label, new_entry)
            continue
        if _identity(old_entry) != _identity(new_entry):
            f.error("register-reused-id",
                    f"transition: register id {rid!r} was re-used for a different possible "
                    f"(claim/provenance identity changed between {old_label} and {new_label})")
        # A possible's origin is fixed: an accepted derived possible retains
        # `origin: ai-derived`; provenance is never laundered in place.
        if _origin(old_entry) != _origin(new_entry):
            f.error("register-derived-origin-changed",
                    f"transition: register id {rid!r} origin changed {_origin(old_entry)!r} -> "
                    f"{_origin(new_entry)!r} — a possible's origin is fixed (an accepted derived "
                    f"possible retains origin ai-derived)")
        # The derived-possible disposition is one-way: once a human_disposition
        # is recorded it is never edited back to the undisposed pending_review.
        old_outcome = _human_outcome(old_entry)
        if old_outcome in {"accepted", "rejected", "deferred"} and _human_outcome(new_entry) is None:
            f.error("register-derived-undispose",
                    f"transition: register id {rid!r} was disposed {old_outcome!r} but is now undisposed "
                    f"— a derived possible's disposition is one-way and is never edited back to pending_review")
        old_state = old_entry.get("state")
        new_state = new_entry.get("state")
        legal = LEGAL_TRANSITIONS.get(old_state, set())
        if new_state not in legal:
            hint = ""
            if old_state == "picked" and new_state == "rejected":
                hint = " (abandoning a picked possible is a supersession, never a rejection)"
            elif old_state in TERMINAL_STATES:
                hint = f" ({old_state} is terminal; a returning idea gets a NEW id, never a resurrection)"
            f.error("register-illegal-transition",
                    f"transition: register id {rid!r} {old_state!r} -> {new_state!r} is not a legal move{hint}")
        check_entry_state_fields(f, new_label, new_entry)
        check_derived_entry(f, new_label, new_entry)


def check_entry_state_fields(f: Findings, label: str, entry: dict) -> None:
    """Re-verify per-state field requirements through the transition path
    (redundant with the schema allOf, but the ledger asks for it here too)."""
    rid = entry.get("id")
    state = entry.get("state")
    if state in TERMINAL_STATES:
        if not entry.get("reason") or not entry.get("citation"):
            f.error("register-uncited-terminal",
                    f"{label}: register id {rid!r} state {state!r} requires both reason and citation")
    if state == "picked":
        pick = entry.get("pick")
        if not isinstance(pick, dict) or not pick.get("staging_id"):
            f.error("register-picked-no-staging",
                    f"{label}: register id {rid!r} state 'picked' requires pick.staging_id")


# --------------------------- project register ---------------------------

def check_project_register_rules(f: Findings, label: str, doc: dict) -> None:
    """id uniqueness (projects + groups), group-member existence, and the
    project->group single-parent rule (a project in at most one group).
    REPOSITORY membership is multi-parent since Brett's 2026-08-06 ruling on
    `add-project-scoped-selection`: a repository may live in any number of
    projects; the snapshot's singular `project` is the PRIMARY
    (first-declaring in register order) and the additive `projects` list
    carries full membership."""
    projects = doc.get("projects") or []
    groups = doc.get("project_groups") or []

    proj_ids: dict[str, int] = {}
    for p in projects:
        if not isinstance(p, dict):
            continue
        pid = p.get("id")
        if pid is not None:
            proj_ids[pid] = proj_ids.get(pid, 0) + 1
    for pid, n in proj_ids.items():
        if n > 1:
            f.error("project-duplicate-id", f"{label}: project id {pid!r} appears {n} times")

    grp_ids: dict[str, int] = {}
    proj_group_parent: dict[str, list[str]] = {}
    for g in groups:
        if not isinstance(g, dict):
            continue
        gid = g.get("id")
        if gid is not None:
            grp_ids[gid] = grp_ids.get(gid, 0) + 1
        for member in g.get("projects") or []:
            proj_group_parent.setdefault(member, []).append(gid)
            if member not in proj_ids:
                f.error("project-dangling-group-member",
                        f"{label}: project group {gid!r} references unknown project {member!r}")
    for gid, n in grp_ids.items():
        if n > 1:
            f.error("project-group-duplicate-id", f"{label}: project group id {gid!r} appears {n} times")
    for member, parents in proj_group_parent.items():
        if len(parents) > 1:
            f.error("project-multi-parent-project",
                    f"{label}: project {member!r} belongs to multiple groups {parents} "
                    f"(single-parent D10; snapshot carries a singular project_group field)")


# --------------------------- gate-action precondition ---------------------------

def check_gate_precondition(f: Findings, label: str, doc: dict, ratified_changes: set[str] | None) -> None:
    """D17: a kickoff record requires its target change to carry a recorded
    ratification. Cross-instance — SKIPPED (not passed) when no context is
    available."""
    if doc.get("action") != "kickoff":
        return
    change_id = (doc.get("target") or {}).get("change_id")
    if ratified_changes is None:
        f.note(f"{label}: kickoff precondition SKIPPED — no ratification context supplied "
               f"(pass --context or run a directory sweep with sibling ratify records)")
        return
    if change_id not in ratified_changes:
        f.error("kickoff-unratified",
                f"{label}: kickoff targets change {change_id!r} which carries no recorded "
                f"ratification in the supplied context (D17 refuses kickoff without ratification)")


# --------------------------- committed-manifest guard ---------------------------

def check_committed_manifests(f: Findings, repo: Path) -> None:
    """A well-formed workbench manifest found in TRACKED repository content is an
    error (schema comment / spec scenario "A workbench manifest is committed").
    Saved manifests belong under gitignored `ideation/workbench/`. The reference
    `examples/` tree is excluded — those are static contract material, not live
    session state — and the schema files themselves are excluded."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "*.yaml", "*.yml"],
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        f.note(f"committed-manifest guard skipped: git ls-files unavailable ({exc})")
        return
    tracked = [ln for ln in out.stdout.splitlines() if ln.strip()]
    offenders = 0
    for rel in tracked:
        if rel.startswith("examples/") or rel.startswith("contracts/schemas/"):
            continue
        try:
            doc = load_yaml(repo / rel)
        except (yaml.YAMLError, OSError):
            continue
        if isinstance(doc, dict) and doc.get("kind") == "ideation-workbench":
            f.error("committed-workbench-manifest",
                    f"{rel}: a workbench manifest is committed/tracked — saved manifests are "
                    f"session state and belong under gitignored ideation/workbench/")
            offenders += 1
    f.note(f"committed-manifest guard: {len(tracked)} tracked YAML file(s) scanned "
           f"(examples/ excluded), {offenders} committed workbench manifest(s) found")




# --------------------- doxBench wire family (task 2.4 rules) ---------------------
#
# Layered on schema conformance, mirroring each schema's own comments:
#   Catalog   model_id uniqueness; a credential/endpoint SPELLING scan over
#             every public string value (the schema already refuses extra
#             fields structurally; this catches leakage THROUGH allowed ones);
#             and since contract-v1.38 the ROUTING-RULE resolution rules —
#             dangling target, chained rule, available-rule-to-unavailable-
#             model, and the badge covering (see check_routing_rules).
#   Request   exactly one outline + one document buffer; segment-wise path
#             confinement; EXACT content-hash parity (the validator recomputes
#             SHA-256 over each buffer's content, so a mismatched identity is
#             refused rather than trusted); with a catalog context (packaged
#             examples, or --context) unknown-model and per-model input-budget
#             checks — without one those two are SKIPPED, never silently
#             passed.
#   Success   unique proposal targets.
#   Failure   the limit-pairing rule (`limit` appears IFF the error is the
#             budget refusal) and the same spelling scan on the message.
#   Sweep     duplicate client_turn_id with DIFFERENT request content across a
#             file set is refused (idempotency's conflict half, FR-019).

import hashlib as _hashlib
import json as _json
import re as _re

_CREDENTIAL_RE = _re.compile(
    r"(?i)(bearer\s+\S|api[-_]?key|authorization\s*:|sk-[A-Za-z0-9]{6,}|"
    r"BEGIN [A-Z ]*PRIVATE KEY|secret[-_]?name)")
_ENDPOINT_RE = _re.compile(r"(?i)\b(https?|wss?)://")

# The routing badge's SEGMENT GRAMMAR (contract-v1.38; adversarial review round
# 1 F1). RESTATED from `ideation_dashboard.doxbench_model` -- this validator is
# standalone and imports nothing from that package (the same convention the
# reserved-buffer-key note below records) -- and a companion test pins the two
# spellings and the two normalizers equal, so the file gate and the type gate
# cannot drift into two grammars.
ROUTING_BADGE_SEPARATOR = " / "
ROUTING_BADGE_TRAILING_PUNCTUATION = ".;,"


def normalized_badge_segment(text: Any) -> str:
    """One badge segment, in the form the covering rule compares: whitespace
    collapsed, case folded, trailing `.;,` dropped. Interior characters are
    NEVER rewritten — `on-tenant` and `non-tenant` must stay different, which is
    the pair that broke the old substring predicate."""
    collapsed = " ".join(str(text).split()).casefold()
    return collapsed.rstrip(ROUTING_BADGE_TRAILING_PUNCTUATION).strip()


def badge_segments(data_handling: Any) -> tuple[str, ...]:
    """A rule's declared badge, split into normalized non-empty segments."""
    return tuple(
        segment
        for segment in (
            normalized_badge_segment(part)
            for part in str(data_handling).split(ROUTING_BADGE_SEPARATOR)
        )
        if segment
    )


def _string_values(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _string_values(v)
    elif isinstance(node, list):
        for v in node:
            yield from _string_values(v)


def catalog_model_ids_from(doc: Any) -> dict[str, int]:
    """{model_id: input_limit_bytes} from one catalog instance (context for
    the turn-request budget/unknown-model checks)."""
    out: dict[str, int] = {}
    if isinstance(doc, dict) and doc.get("kind") == "workbench-model-catalog":
        for entry in doc.get("models") or []:
            if isinstance(entry, dict) and entry.get("model_id"):
                out[str(entry["model_id"])] = int(entry.get("input_limit_bytes") or 0)
    return out


def _scan_public_strings(f: Findings, label: str, node: Any) -> None:
    for value in _string_values(node):
        if _CREDENTIAL_RE.search(value):
            f.error("credential",
                    f"{label}: credential spelling in a public field: {value[:60]!r}")
        if _ENDPOINT_RE.search(value):
            f.error("endpoint",
                    f"{label}: raw endpoint in a public field: {value[:60]!r}")


def check_model_catalog(f: Findings, label: str, doc: dict) -> None:
    entries = [e for e in doc.get("models") or [] if isinstance(e, dict)]
    seen = set()
    for entry in doc.get("models") or []:
        mid = entry.get("model_id") if isinstance(entry, dict) else None
        if mid in seen:
            f.error("catalog", f"{label}: duplicate model_id {mid!r}")
        seen.add(mid)
    _scan_public_strings(f, label, doc.get("models"))
    check_routing_rules(f, label, entries)


def check_routing_rules(f: Findings, label: str, entries: list[dict]) -> None:
    """The contract-v1.38 routing declaration's rules that the released shape
    cannot express (`$defs/model_entry` says so in its own comments, and
    delegates them here). SEVEN of them, since adversarial review round 1.

    The shape enforces what is expressible per entry: the three fields travel
    together, `routes_to` is unique and non-empty, and a `routing_rule: false`
    entry may carry neither routing field. Everything below needs either the
    WHOLE catalog or a comparison the shape has no operator for — and the same
    seven are enforced at catalog construction in
    `scripts/ideation_dashboard/doxbench_model.py`
    (`ModelCatalog._validate_routing_targets` plus the per-entry
    `_validate_routing_declaration`, which is where rules 6 and 7 live on that
    side because one entry is enough to see them). Neither place substitutes
    for the other: an in-process catalog never becomes a file, and a file is
    never constructed through that type. The claim that the two agree is
    ASSERTED by a test over the packaged negatives, not merely stated here —
    review round 1 found this docstring claiming parity that did not hold.

    1. no dangling target;
    2. no chained rule (`resolved_model_id` records the model that ANSWERED, so
       it must name something that answers);
    3. an available rule resolves to an available model;
    4. THE BADGE COVERING — the ratified scenario's own THEN: a routing entry
       MUST "carry the handling badge of every model it may route to", and the
       entry's own `data_handling` is the one badge string the menu shows for
       it, so each target's badge must be one SEGMENT of it (see
       `normalized_badge_segment`; a target badge holding the separator is
       ill-formed and refused);
    5. a rule promises no more headroom than THE MODEL THAT ANSWERS — the
       effective turn limit is computed from the SELECTED entry, which for a
       routed turn is the RULE, so an AVAILABLE rule's declared limits must not
       exceed those of `resolved_model_id`'s entry. RULED BY BRETT 2026-08-21
       ("Swap to rule 5'"): this was first a MINIMUM over every member of
       `routes_to`, which the adversarial review upheld only with reservation.
       Under static resolution the promise that matters is the one the
       ANSWERING model has to honour; the un-resolved destinations are not
       load-bearing; and min-capping would bake in semantics that contradict
       the sanctioned per-turn fit-aware router staged as
       `ideation/staging/doxchat-auto-fit-routing/`. Unavailable rules are
       exempt, as they are from rule 3;
    6. `resolved_model_id` must be a MEMBER of `routes_to`;
    7. a rule must not name ITSELF in `routes_to`.

    RULES 6 AND 7 WERE ADDED AT ADVERSARIAL REVIEW ROUND 1 (F2), and the
    docstring they replace claimed the opposite — that they were "the
    schema's/type's per-entry business" and that "a structurally invalid
    instance never reaches this function". That was FALSE in the direction that
    matters: the schema cannot express either rule, so this file gate was
    strictly WEAKER than the type gate, and the reviewer walked a catalog past
    it whose rule was badged safe while resolving to a model badged "retained
    and used for vendor model training". Rule 7 is checked EXPLICITLY rather
    than left to fall out of rule 2, so a self-reference is reported as what it
    is instead of as "routes to something that is itself a routing rule"."""
    by_id = {str(entry.get("model_id")): entry for entry in entries}
    for entry in entries:
        if entry.get("routing_rule") is not True:
            continue
        rule_id = str(entry.get("model_id"))
        declared_segments = badge_segments(entry.get("data_handling") or "")
        targets = entry.get("routes_to")
        target_ids = [str(t) for t in targets] if isinstance(targets, list) else []
        for target_id in target_ids:
            # ALSO A DIAGNOSTIC (F2b asked for it as one: "explicit check, not
            # incidental via the chained-rule rule"). A rule that names itself
            # names a routing rule, so the chained-rule arm below refuses the
            # same catalog — reporting "routes to something that is itself a
            # routing rule", which is true and useless. Guarded by a code test.
            if target_id == rule_id:
                f.error("routing-self-reference",
                        f"{label}: routing rule {rule_id!r} names ITSELF in "
                        f"routes_to — a rule resolves to a model that answers, "
                        f"never back to the rule")
                continue
            target = by_id.get(target_id)
            if target is None:
                f.error("routing-target",
                        f"{label}: routing rule {rule_id!r} routes to "
                        f"{target_id!r}, which is not in this catalog")
                continue
            if target.get("routing_rule") is True:
                f.error("routing-target",
                        f"{label}: routing rule {rule_id!r} routes to "
                        f"{target_id!r}, which is itself a routing rule — a "
                        f"resolved model must be one that answers")
                continue
            target_badge = str(target.get("data_handling") or "")
            # A DIAGNOSTIC, not an independent refusal — and revert-testing is
            # what proved it. A badge holding the separator can never BE a
            # segment, so the covering check below refuses the same catalog
            # either way; it just refuses it with a message that sends the
            # operator to add a badge which will still not match. This arm names
            # the real cause. Its guard is therefore a test on the finding CODE,
            # not on the mere fact of refusal.
            #
            # Against the NORMALIZED badge (review re-verify N3), and not merely
            # for the message: a badge like `"read /\nwrite"` holds no raw
            # " / " but collapses onto one, so it slipped this arm AND passed
            # the covering check — a full ACCEPT of an ill-formed badge.
            if ROUTING_BADGE_SEPARATOR in normalized_badge_segment(target_badge):
                f.error("routing-badge",
                        f"{label}: the data_handling badge of {target_id!r} "
                        f"contains {ROUTING_BADGE_SEPARATOR!r}, the routing "
                        f"badge's own segment separator, so it cannot be "
                        f"carried as one")
            elif normalized_badge_segment(target_badge) not in declared_segments:
                f.error("routing-badge",
                        f"{label}: routing rule {rule_id!r} does not carry the "
                        f"data-handling badge of {target_id!r} as a SEGMENT of "
                        f"its own badge — a routing entry reports the posture "
                        f"of every model it may route to")
        resolved_id = str(entry.get("resolved_model_id"))
        resolved = by_id.get(resolved_id)
        # RULE 5' (Brett's ruling 2026-08-21): the bound is the RESOLVED
        # model's, not the minimum over `routes_to`, and it applies only while
        # the rule is selectable — the same exemption rule 3 already carries.
        if resolved is not None and entry.get("available") is True:
            for field in ("input_limit_bytes", "output_limit_bytes"):
                declared = entry.get(field)
                answering = resolved.get(field)
                if not (isinstance(declared, int) and isinstance(answering, int)):
                    continue
                if declared > answering:
                    f.error("routing-limit",
                            f"{label}: routing rule {rule_id!r} declares "
                            f"{field} {declared}, above the {answering} of "
                            f"{resolved_id!r}, the model it resolves to")
        if resolved_id not in target_ids:
            # F2: the SHAPE cannot express this, so without it a rule could be
            # badged safe and resolve to a model whose posture it never states —
            # every covering check above runs over `routes_to`, which such a
            # resolved id is not in.
            f.error("routing-resolution",
                    f"{label}: routing rule {rule_id!r} resolves to "
                    f"{resolved_id!r}, which it does not declare it may route "
                    f"to (routes_to {sorted(target_ids)}) — so nothing checked "
                    f"that its badge is carried")
        if resolved is None:
            f.error("routing-target",
                    f"{label}: routing rule {rule_id!r} resolves to "
                    f"{resolved_id!r}, which is not in this catalog")
        elif entry.get("available") is True and resolved.get("available") is not True:
            f.error("routing-availability",
                    f"{label}: routing rule {rule_id!r} is available but "
                    f"resolves to {resolved_id!r}, which is not")


def _confined(f: Findings, label: str, where: str, path_value) -> None:
    if path_value is None:
        # A not-yet-created artifact has no path yet (the null-path -> create
        # lifecycle); nullability is the schema's decision, confinement only
        # judges paths that exist.
        return
    text = str(path_value)
    if text.startswith("/") or ".." in text.split("/"):
        f.error("path", f"{label}: {where}: path escapes the checkout: {text!r}")


def check_turn_request(f: Findings, label: str, doc: dict,
                       model_ctx: dict[str, int] | None) -> None:
    buffers = [b for b in doc.get("buffers") or [] if isinstance(b, dict)]
    check_reserved_document_paths(f, label, buffers, V1_RESERVED_DOCUMENT_PATHS)
    kinds = sorted(str(b.get("kind")) for b in buffers)
    if kinds != ["document", "outline"]:
        f.error("buffers", f"{label}: exactly one outline and one document "
                           f"buffer required, got {kinds}")
    _confined(f, label, "active_document_path", doc.get("active_document_path", ""))
    total_bytes = 0
    for b in buffers:
        if not isinstance(b, dict):
            continue
        _confined(f, label, f"buffers/{b.get('kind')}/path", b.get("path", ""))
        content = str(b.get("content", ""))
        total_bytes += len(content.encode("utf-8"))
        declared = str(b.get("content_hash", ""))
        actual = _hashlib.sha256(content.encode("utf-8")).hexdigest()
        if declared != actual:
            f.error("hash", f"{label}: buffers/{b.get('kind')}: content_hash "
                            f"mismatch (declared {declared[:12]}…, actual {actual[:12]}…)")
    if model_ctx is None:
        f.warnings.append(f"{label}: model context unavailable — unknown-model "
                          f"and budget checks SKIPPED (supply a catalog instance)")
        return
    mid = str(doc.get("model_id", ""))
    if mid not in model_ctx:
        f.error("unknown-model",
                f"{label}: model_id {mid!r} is not in the approved catalog")
        return
    limit = model_ctx[mid]
    if limit and total_bytes > limit:
        f.error("budget", f"{label}: request buffers total {total_bytes} bytes "
                          f"over model {mid!r} input limit {limit}")


# THE RESERVED KEYS A DOCUMENT'S OWN PATH MAY NOT CLAIM, per lane (Codex review
# of PR #210, CODEX-3). Restated here rather than imported: this validator is
# PUBLISHED BY EXACT COMMIT and run from a pinned checkout against an arbitrary
# target repository, so it must not import the runtime package that happens to
# sit beside it in the publisher. The pairing with
# `ideation_dashboard.doxbench_turns.RESERVED_BUFFER_KEYS` /
# `V1_RESERVED_BUFFER_KEYS` is asserted by a companion test instead, which is the
# only way to make a restatement safe.
#
# The asymmetry is the runtime's own and is load-bearing. `outline` is refused on
# BOTH lanes: a document keyed there is filtered out of every downstream
# enumeration. `document` is refused on the WIDENED lane only, where the reserved
# unbacked slot can ride beside a path-backed document; the v1 envelope carries
# exactly one document whose key is `document` either way, and such a turn was
# served before this release.
V1_RESERVED_DOCUMENT_PATHS = frozenset({"outline"})
V2_RESERVED_DOCUMENT_PATHS = frozenset({"outline", "document"})


def check_reserved_document_paths(f: Findings, label: str, buffers: list,
                                  refused: frozenset) -> None:
    """Refuse a document buffer whose own PATH claims a reserved buffer key.

    Without this the family's declared owner certified an envelope the route
    always refuses — conformance for a shape that cannot be processed, which is
    worse than no verdict."""
    for buffer in buffers:
        if str(buffer.get("kind")) != "document":
            continue
        if buffer.get("path") in refused:
            f.error("reserved-key",
                    f"{label}: a document buffer's path claims the reserved "
                    f"buffer key {buffer.get('path')!r}; the route refuses this "
                    f"before any provider call")


def _buffer_key_of(buffer: dict) -> str:
    """The KEY a buffer is held under (add-doxbench-editing-phase-b design D1),
    derived exactly as the runtime derives it: the outline's key is reserved, a
    document's key IS its own path, and a document with no path yet takes the one
    reserved unbacked slot. Never invented, and never read off an adjacent field
    that answers a different question."""
    if str(buffer.get("kind")) == "outline":
        return "outline"
    path = buffer.get("path")
    return "document" if path is None else str(path)


def check_turn_request_v2(f: Findings, label: str, doc: dict,
                          model_ctx: dict[str, int] | None) -> None:
    """The widened request's rules the shape cannot express: one outline plus one
    or more DISTINCTLY KEYED documents, and a DECLARED binding that names one of
    the buffers this same request supplied. The hash, confinement, unknown-model
    and budget rules are the v1 ones, applied per buffer over a set instead of a
    pair."""
    buffers = [b for b in doc.get("buffers") or [] if isinstance(b, dict)]
    check_reserved_document_paths(f, label, buffers, V2_RESERVED_DOCUMENT_PATHS)
    outlines = [b for b in buffers if str(b.get("kind")) == "outline"]
    documents = [b for b in buffers if str(b.get("kind")) == "document"]
    if len(outlines) != 1 or not documents:
        f.error("buffers", f"{label}: exactly one outline buffer and at least "
                           f"one document buffer required, got "
                           f"{len(outlines)} outline(s) and "
                           f"{len(documents)} document(s)")
    keys: list[str] = [_buffer_key_of(b) for b in buffers]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        f.error("buffers", f"{label}: two buffers claim the same key "
                           f"{duplicates} — a document is loaded at most once, "
                           f"and 'which text did the model see' must have one "
                           f"answer")
    bound = doc.get("bound_buffer")
    if str(bound) not in keys:
        f.error("bound-buffer",
                f"{label}: bound_buffer {bound!r} names no supplied buffer "
                f"(supplied {sorted(set(keys))})")
    _confined(f, label, "bound_buffer", bound)
    total_bytes = 0
    for b in buffers:
        key = _buffer_key_of(b)
        _confined(f, label, f"buffers/{key}/path", b.get("path", ""))
        content = str(b.get("content", ""))
        total_bytes += len(content.encode("utf-8"))
        declared = str(b.get("content_hash", ""))
        actual = _hashlib.sha256(content.encode("utf-8")).hexdigest()
        if declared != actual:
            f.error("hash", f"{label}: buffers/{key}: content_hash "
                            f"mismatch (declared {declared[:12]}…, actual {actual[:12]}…)")
    if model_ctx is None:
        f.warnings.append(f"{label}: model context unavailable — unknown-model "
                          f"and budget checks SKIPPED (supply a catalog instance)")
        return
    mid = str(doc.get("model_id", ""))
    if mid not in model_ctx:
        f.error("unknown-model",
                f"{label}: model_id {mid!r} is not in the approved catalog")
        return
    limit = model_ctx[mid]
    if limit and total_bytes > limit:
        f.error("budget", f"{label}: request buffers total {total_bytes} bytes "
                          f"over model {mid!r} input limit {limit}")


def check_turn_success(f: Findings, label: str, doc: dict) -> None:
    targets = [p.get("target") for p in doc.get("proposals") or []
               if isinstance(p, dict)]
    if len(targets) != len(set(targets)):
        f.error("proposal", f"{label}: proposal targets must be unique, got {targets}")


def check_turn_success_v2(f: Findings, label: str, doc: dict) -> None:
    """The widened record's own consistency. It carries every buffer's observed
    identity by KEY, so three rules the v1 record could not state become
    checkable here: a proposal targets a buffer the turn actually held, the
    proposal count is bounded by that buffer count rather than by a literal 2,
    and the record's declared binding names one of those same buffers."""
    observed = doc.get("observed_hashes")
    observed = observed if isinstance(observed, dict) else {}
    proposals = [p for p in doc.get("proposals") or [] if isinstance(p, dict)]
    targets = [p.get("target") for p in proposals]
    if len(targets) != len(set(targets)):
        f.error("proposal", f"{label}: proposal targets must be unique, got {targets}")
    if len(proposals) > len(observed):
        f.error("proposal",
                f"{label}: {len(proposals)} proposal(s) against "
                f"{len(observed)} supplied buffer(s) — a response may never "
                f"rewrite more buffers than it was shown")
    for proposal in proposals:
        target = str(proposal.get("target"))
        if target not in observed:
            f.error("proposal-target",
                    f"{label}: proposal target {target!r} names no buffer this "
                    f"turn observed — unroutable, never guessed at")
            continue
        if str(proposal.get("base_hash")) != str(observed[target]):
            f.error("proposal",
                    f"{label}: proposal {target!r} is based on an identity the "
                    f"turn did not observe for that buffer")
    bound = str(doc.get("bound_buffer"))
    if bound not in observed:
        f.error("bound-buffer",
                f"{label}: bound_buffer {bound!r} names no buffer this turn "
                f"observed (observed {sorted(observed)})")
    selected = doc.get("selected_model")
    selected = selected if isinstance(selected, dict) else {}
    if (selected.get("routing_rule") is False
            and str(selected.get("requested_model_id")) != str(doc.get("model_id"))):
        f.error("selected-model",
                f"{label}: a non-routing catalog entry cannot resolve to a "
                f"different model (requested "
                f"{selected.get('requested_model_id')!r}, answered "
                f"{doc.get('model_id')!r})")


def check_turn_failure(f: Findings, label: str, doc: dict) -> None:
    has_limit = "limit" in doc
    is_budget = doc.get("error") == "request_limit_exceeded"
    if has_limit != is_budget:
        f.error("failure-limit",
                f"{label}: `limit` appears iff error is request_limit_exceeded "
                f"(error={doc.get('error')!r}, "
                f"limit={'present' if has_limit else 'absent'})")
    _scan_public_strings(f, label, doc.get("message"))


def check_turn_id_uniqueness(f: Findings, paths) -> None:
    """Sweep rule: the same client_turn_id with DIFFERENT request content is
    the idempotency conflict FR-019 refuses before dispatch."""
    seen: dict[str, tuple[str, str]] = {}
    for path in paths:
        doc = load_yaml(path)
        if not (isinstance(doc, dict) and doc.get("kind") in (
                "workbench-chat-turn", "workbench-chat-turn-v2")):
            continue
        tid = str(doc.get("client_turn_id"))
        # Canonicalize buffer order before hashing: a retransmission that merely
        # reorders the buffers is the SAME request, not an FR-019 conflict.
        # Ordering is by buffer KEY rather than by kind, because the widened
        # request holds N documents and every one of them declares `document`.
        canonical = dict(doc)
        canonical["buffers"] = sorted(
            (b for b in doc.get("buffers") or [] if isinstance(b, dict)),
            key=_buffer_key_of)
        digest = _hashlib.sha256(
            _json.dumps(canonical, sort_keys=True).encode()).hexdigest()
        if tid in seen and seen[tid][0] != digest:
            f.error("duplicate-turn",
                    f"{path.name}: duplicate-turn id {tid!r} with different "
                    f"content (first seen in {seen[tid][1]})")
        seen.setdefault(tid, (digest, path.name))


# --------------------- layer 1: packaged reference examples ---------------------

def check_examples(f: Findings, registry: Registry, docs: dict[str, dict]) -> None:
    """GATES self-test: every packaged example validates exactly as its filename
    and header comment claim — valid pass, each negative fails for its intended
    reason, each transition pair matches its declared expectation."""
    if not EXAMPLES_DIR.is_dir():
        f.error("examples-missing", f"{EXAMPLES_DIR} not found")
        return

    # The snapshot example doubles as ratification context for the gate examples.
    ratified_ctx: set[str] = set()
    model_ctx: dict[str, int] = {}
    valid_docs: list[tuple[str, Any, str | None]] = []
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        doc = load_yaml(path)
        ratified_ctx |= ratified_change_ids_from(doc)
        model_ctx.update(catalog_model_ids_from(doc))
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        sub = Findings()
        doc = load_yaml(path)
        tag = validate_instance(sub, path.name, doc, registry, docs, ratified_ctx,
                                model_ctx=model_ctx)
        valid_docs.append((path.name, doc, tag))
        if sub.errors:
            for e in sub.errors:
                f.error("example-invalid", f"{path.name}: expected valid: {e}")
        f.warnings.extend(sub.warnings)
    valid_count = len(valid_docs)

    invalid_count = check_negative_examples(f, registry, docs, ratified_ctx,
                                            model_ctx)
    pairs = check_transition_examples(f, registry)

    f.note(f"examples: {valid_count} valid example(s) confirmed valid, "
           f"{invalid_count} negative example(s) confirmed invalid, "
           f"{pairs} transition pair(s) confirmed")


def check_negative_examples(
    f: Findings, registry: Registry, docs: dict[str, dict], ratified_ctx: set[str],
    model_ctx: dict[str, int] | None = None,
) -> int:
    neg_dir = EXAMPLES_DIR / "negative"
    if not neg_dir.is_dir():
        f.error("examples-missing", f"{neg_dir} not found")
        return 0
    checked = 0
    for path in sorted(neg_dir.glob("*.yaml")):
        sub = Findings()
        doc = load_yaml(path)
        # Negatives are validated WITH the example ratification context so the
        # context-dependent kickoff-precondition negative can fail as intended.
        validate_instance(sub, f"negative/{path.name}", doc, registry, docs,
                          ratified_ctx, model_ctx=model_ctx)
        if not sub.errors:
            f.error("example-should-fail",
                    f"negative/{path.name}: expected invalid, produced no error")
            continue
        checked += 1
    # The duplicate-turn PAIR negative: two files whose shared client_turn_id
    # carries different content — refused by the sweep rule, not per-file.
    pair_dir = neg_dir / "duplicate-turn-pair"
    if pair_dir.is_dir():
        sub = Findings()
        check_turn_id_uniqueness(sub, sorted(pair_dir.glob("*.yaml")))
        if sub.errors:
            checked += 1
        else:
            f.error("example-should-fail",
                    "negative/duplicate-turn-pair: expected the duplicate-turn "
                    "sweep to refuse, produced no error")
    return checked


def check_transition_examples(f: Findings, registry: Registry) -> int:
    """Transition pairs live under examples/ideation-dashboard/transitions/ as
    `<case>.before.yaml` / `<case>.after.yaml`; a `valid-` prefix expects the
    transition to pass, otherwise it must fail."""
    tdir = EXAMPLES_DIR / "transitions"
    if not tdir.is_dir():
        f.error("examples-missing", f"{tdir} not found")
        return 0
    pairs = 0
    for before in sorted(tdir.glob("*.before.yaml")):
        case = before.name[: -len(".before.yaml")]
        after = tdir / f"{case}.after.yaml"
        if not after.is_file():
            f.error("transition-unpaired", f"transitions/{before.name}: no matching .after.yaml")
            continue
        old = (load_yaml(before) or {}).get(REGISTER_CONTAINER_KEY) or []
        new = (load_yaml(after) or {}).get(REGISTER_CONTAINER_KEY) or []
        sub = Findings()
        check_register_transition(sub, f"{case}.before", old, f"{case}.after", new)
        expect_pass = case.startswith("valid-")
        if expect_pass and sub.errors:
            for e in sub.errors:
                f.error("transition-invalid", f"transitions/{case}: expected legal: {e}")
        elif not expect_pass and not sub.errors:
            f.error("transition-should-fail",
                    f"transitions/{case}: expected an illegal transition, validated cleanly")
        pairs += 1
    return pairs


# --------------------- layer 2: real repository instances ---------------------

def check_repo_tree(
    f: Findings, registry: Registry, docs: dict[str, dict], repo: Path, context: set[str] | None,
) -> None:
    """Validate any real instances of the five kinds committed under the repo
    (excluding the reference examples tree, the schema files, and the test
    trees — `tests/` carries deliberately-INVALID negative fixtures for the
    dashboard runtime suite adopted by `adopt-neutral-tooling-home`, and a
    test fixture is not a real instance), and run the
    committed-workbench-manifest guard."""
    check_committed_manifests(f, repo)

    checked = 0
    for path in sorted(list(repo.rglob("*.yaml")) + list(repo.rglob("*.yml"))):
        rel = path.relative_to(repo).as_posix()
        if rel.startswith(("examples/", "contracts/schemas/", "tests/")) or "/__pycache__/" in rel:
            continue
        try:
            doc = load_yaml(path)
        except yaml.YAMLError:
            continue
        if detect(doc) is None:
            continue
        # A tracked ideation-workbench manifest is already reported by the guard.
        if isinstance(doc, dict) and doc.get("kind") == "ideation-workbench":
            continue
        validate_instance(f, rel, doc, registry, docs, context)
        checked += 1
    f.note(f"repo tree ({repo}): {checked} real ideation-dashboard-family instance(s) checked "
           f"(none is normal pre-realization)")


# --------------------------- orchestration ---------------------------

def run_default(repo: Path, strict: bool) -> int:
    f = Findings()
    if not SCHEMAS_DIR.is_dir():
        print(f"ERROR {SCHEMAS_DIR} not found", file=sys.stderr)
        return 2
    registry, docs = build_registry()
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-meta-invalid", f"{name}: {exc}")

    check_examples(f, registry, docs)
    # The packaged snapshot example supplies ratification context for any real
    # gate-action records found in the tree.
    ctx, ctx_notes = load_context(EXAMPLES_DIR / "ideation-dashboard-snapshot.example.yaml")
    for n in ctx_notes:
        f.note(n)
    check_repo_tree(f, registry, docs, repo, ctx)
    return report(f, strict)


def run_path(path: Path, context_path: Path | None, strict: bool) -> int:
    f = Findings()
    registry, docs = build_registry()
    ctx, ctx_notes = load_context(context_path)
    for n in ctx_notes:
        f.note(n)
    if path.is_dir():
        files = sorted(list(path.rglob("*.yaml")) + list(path.rglob("*.yml")))
        # Directory sweep: sibling records provide ratification context.
        if ctx is None:
            ctx = set()
            for fp in files:
                try:
                    ctx |= ratified_change_ids_from(load_yaml(fp))
                except yaml.YAMLError:
                    continue
        checked = 0
        for fp in files:
            try:
                doc = load_yaml(fp)
            except yaml.YAMLError as exc:
                f.error("yaml", f"{fp}: {exc}")
                continue
            if detect(doc) is None:
                continue
            validate_instance(f, str(fp), doc, registry, docs, ctx)
            checked += 1
        f.note(f"directory sweep {path}: {checked} recognized instance(s) checked")
    elif path.is_file():
        try:
            doc = load_yaml(path)
        except yaml.YAMLError as exc:
            print(f"ERROR {path}: {exc}", file=sys.stderr)
            return 2
        validate_instance(f, str(path), doc, registry, docs, ctx)
    else:
        print(f"ERROR path not found: {path}", file=sys.stderr)
        return 2
    return report(f, strict)


def run_transition(old_path: Path, new_path: Path, strict: bool) -> int:
    f = Findings()
    registry, docs = build_registry()
    for label, p in (("OLD", old_path), ("NEW", new_path)):
        if not p.is_file():
            print(f"ERROR {label} path not found: {p}", file=sys.stderr)
            return 2
    old_doc, new_doc = load_yaml(old_path), load_yaml(new_path)
    # Each side must itself be a well-formed register section.
    sv = section_validator(registry)
    for lbl, d in ((str(old_path), old_doc), (str(new_path), new_doc)):
        section = d.get(REGISTER_CONTAINER_KEY) if isinstance(d, dict) else None
        if not isinstance(section, list):
            f.error("transition-shape",
                    f"{lbl}: not a register section (missing {REGISTER_CONTAINER_KEY!r} list)")
            continue
        for e in iter_errors(sv, section):
            loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
            f.error("schema", f"{lbl}: {REGISTER_CONTAINER_KEY}/{loc}: {e.message}")
    if not f.errors:
        check_register_transition(
            f, str(old_path), old_doc.get(REGISTER_CONTAINER_KEY) or [],
            str(new_path), new_doc.get(REGISTER_CONTAINER_KEY) or [],
        )
    return report(f, strict)


def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    n_e, n_w = len(f.errors), len(f.warnings)
    print(f"\nvalidate-ideation-dashboard-contracts: {n_e} error(s), {n_w} warning(s)")
    if n_e or (strict and n_w):
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None,
                    help="file (kind auto-detected) or directory to validate; "
                         "omit to self-test packaged examples and scan this checkout")
    ap.add_argument("--transition", nargs=2, metavar=("OLD", "NEW"),
                    help="validate register transition legality across two register sections")
    ap.add_argument("--context", type=Path, default=None,
                    help="snapshot or directory supplying ratified-change context for kickoff preconditions")
    ap.add_argument("--repo", type=Path, default=ROOT,
                    help="repo root to scan in default mode (default: this checkout)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    try:
        if args.transition:
            return run_transition(Path(args.transition[0]).resolve(),
                                  Path(args.transition[1]).resolve(), args.strict)
        if args.path is not None:
            return run_path(Path(args.path).resolve(), args.context, args.strict)
        return run_default(Path(args.repo).resolve(), args.strict)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
