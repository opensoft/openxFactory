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
             id must exist; single-parent hierarchy — a repository in at most
             one project, a project in at most one group (the D10 reading, since
             the snapshot carries singular project/project_group fields).
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
# that date/date-time must be enforced, not merely annotated.
FORMAT_CHECKER = FormatChecker()

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


# --------------------- per-instance validation (schema + rules) ---------------------

def validate_instance(
    f: Findings, label: str, doc: Any, registry: Registry, docs: dict[str, dict],
    ratified_changes: set[str] | None,
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
    single-parent D10 hierarchy (a repo in at most one project, a project in at
    most one group)."""
    projects = doc.get("projects") or []
    groups = doc.get("project_groups") or []

    proj_ids: dict[str, int] = {}
    repo_parent: dict[str, list[str]] = {}
    for p in projects:
        if not isinstance(p, dict):
            continue
        pid = p.get("id")
        if pid is not None:
            proj_ids[pid] = proj_ids.get(pid, 0) + 1
        for repo in p.get("repositories") or []:
            repo_parent.setdefault(repo, []).append(pid)
    for pid, n in proj_ids.items():
        if n > 1:
            f.error("project-duplicate-id", f"{label}: project id {pid!r} appears {n} times")
    for repo, parents in repo_parent.items():
        if len(parents) > 1:
            f.error("project-multi-parent-repo",
                    f"{label}: repository {repo!r} belongs to multiple projects {parents} "
                    f"(single-parent D10; snapshot carries a singular project field)")

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
    valid_docs: list[tuple[str, Any, str | None]] = []
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        doc = load_yaml(path)
        ratified_ctx |= ratified_change_ids_from(doc)
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        sub = Findings()
        doc = load_yaml(path)
        tag = validate_instance(sub, path.name, doc, registry, docs, ratified_ctx)
        valid_docs.append((path.name, doc, tag))
        if sub.errors:
            for e in sub.errors:
                f.error("example-invalid", f"{path.name}: expected valid: {e}")
        f.warnings.extend(sub.warnings)
    valid_count = len(valid_docs)

    invalid_count = check_negative_examples(f, registry, docs, ratified_ctx)
    pairs = check_transition_examples(f, registry)

    f.note(f"examples: {valid_count} valid example(s) confirmed valid, "
           f"{invalid_count} negative example(s) confirmed invalid, "
           f"{pairs} transition pair(s) confirmed")


def check_negative_examples(
    f: Findings, registry: Registry, docs: dict[str, dict], ratified_ctx: set[str],
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
        validate_instance(sub, f"negative/{path.name}", doc, registry, docs, ratified_ctx)
        if not sub.errors:
            f.error("example-should-fail",
                    f"negative/{path.name}: expected invalid, produced no error")
            continue
        checked += 1
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
    (excluding the reference examples tree and the schema files), and run the
    committed-workbench-manifest guard."""
    check_committed_manifests(f, repo)

    checked = 0
    for path in sorted(list(repo.rglob("*.yaml")) + list(repo.rglob("*.yml"))):
        rel = path.relative_to(repo).as_posix()
        if rel.startswith("examples/") or rel.startswith("contracts/schemas/") or "/__pycache__/" in rel:
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
