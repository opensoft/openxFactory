#!/usr/bin/env python3
"""Validate document-cataloging contract artifacts (add-document-cataloging).

Change task 2.3 (`openspec/changes/add-document-cataloging/tasks.md`):
strict validation for the six schemas under
`contracts/schemas/xfactory-document-*.schema.yaml` plus the cross-cutting
deterministic invariants that JSON Schema alone cannot express — complete
coverage, unique per-snapshot identity, source freshness against the
issuing run, review-binding freshness against the owner override file
(spec scenario "Source content changes after review"), taxonomy resolution
against the merged tag registries, owner override standing (checked on the
override file AND on every snapshot entry's `review.authority`, the merged
surface where reviewed/overridden state actually lives), immutable
run/evidence path layout, and the spec's disclosed baseline-mode coverage
exception. It never decides whether a
suggested classification is semantically correct (that judgment belongs to
`document-cataloging`'s reviewing authority) and never edits a source
document, lifecycle header, or `xspec:` marker.

Usage:
    python3 scripts/validate-document-catalog.py [REPO] [--inventory FILE]
        [--baseline] [--strict]

Two layers always run:

1. Packaged reference examples (`examples/document-cataloging/`, task 2.2):
   every non-negative example must validate against the schema its `kind`
   (or, for the two pure-`$defs` locator/handling-gate kernels, its
   documented fragment shape) names; every file under `negative/` must fail.
   This is the GATES self-test: "valid pass, each invalid fails for its
   intended reason."
2. Real artifacts under REPO (default: this checkout): `contracts/
   document-tag-registry.yaml`, `catalog/document-tag-registry.yaml`,
   `catalog/document-tag-overrides.yaml`, and
   `health/document-catalog/{runs,recommendations}/**`. Absent paths are
   reported as skipped, never silently omitted (doc-health convention;
   `scripts/validate-credential-contracts.py` and siblings do the same).

`--inventory FILE` supplies an external `{repo, path|document_ref}` list
(the shared doc-health inventory this validator does not itself own —
codexFactory task 3.x) to check exact coverage; without it, coverage
checking is limited to the duplicate-identity half it can prove alone.
`--baseline` discloses that complete-coverage enforcement is not yet
active (spec requirement "Full baseline and incremental refresh", scenario
"First catalog run begins"): missing-coverage findings become warnings
instead of errors, and the report says so.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
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
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
EXAMPLES_DIR = ROOT / "examples" / "document-cataloging"

SCHEMA_FILENAMES = [
    "xfactory-document-catalog-snapshot.schema.yaml",
    "xfactory-document-cataloger-recommendation.schema.yaml",
    "xfactory-document-tag-registry.schema.yaml",
    "xfactory-document-tag-overrides.schema.yaml",
    "xfactory-document-opaque-locator.schema.yaml",
    "xfactory-document-handling-gate.schema.yaml",
]

KIND_TO_SCHEMA = {
    "xfactory_document_catalog": "xfactory-document-catalog-snapshot.schema.yaml",
    "xfactory_document_catalog_recommendation": "xfactory-document-cataloger-recommendation.schema.yaml",
    "xfactory_document_tag_registry": "xfactory-document-tag-registry.schema.yaml",
    "xfactory_document_tag_overrides": "xfactory-document-tag-overrides.schema.yaml",
}

# Two schemas in this family are pure `$defs` kernels (never a whole
# top-level document; see each file's own description). Their packaged
# examples wrap fragment instances under a plain container key.
FRAGMENT_DEFS = {
    "document-opaque-locator.example.yaml": (
        "xfactory-document-opaque-locator.schema.yaml", "document_locator", "locators",
    ),
    "document-handling-gate.example.yaml": (
        "xfactory-document-handling-gate.schema.yaml", "dispatch_decision", "decisions",
    ),
}
NEGATIVE_FRAGMENT_DEFS = {
    "opaque-locator-both-present.yaml": ("xfactory-document-opaque-locator.schema.yaml", "document_locator"),
    "opaque-locator-neither.yaml": ("xfactory-document-opaque-locator.schema.yaml", "document_locator"),
    "handling-gate-blocked-missing-reference.yaml": ("xfactory-document-handling-gate.schema.yaml", "dispatch_decision"),
    "handling-gate-allowed-missing-attestation.yaml": ("xfactory-document-handling-gate.schema.yaml", "dispatch_decision"),
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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
    """Offline referencing.Registry over the six schemas (same approach as
    scripts/validate-avatar-client.py for the avatar-client kernel)."""
    resources = []
    docs: dict[str, dict] = {}
    for name in SCHEMA_FILENAMES:
        doc = load_yaml(SCHEMAS_DIR / name)
        docs[name] = doc
        rid = doc.get("$id", name)
        resources.append((rid, Resource.from_contents(doc, default_specification=DRAFT202012)))
    return Registry().with_resources(resources), docs


def doc_validator(schema_name: str, registry: Registry, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(docs[schema_name], registry=registry)


def def_validator(schema_name: str, def_name: str, registry: Registry) -> Draft202012Validator:
    """Validator for one named `$def` inside a pure-kernel schema, resolved
    through the registry exactly as the other five schemas `$ref` it."""
    return Draft202012Validator({"$ref": f"{schema_name}#/$defs/{def_name}"}, registry=registry)


def iter_errors(validator: Draft202012Validator, instance: Any):
    return sorted(validator.iter_errors(instance), key=lambda e: [str(p) for p in e.absolute_path])


# --------------------- layer 1: packaged reference examples ---------------------

def check_examples(f: Findings, registry: Registry, docs: dict[str, dict]) -> None:
    """Task 2.3 GATES self-test: every example under
    examples/document-cataloging/ must validate exactly as its filename and
    header comment claim (task 2.2)."""
    if not EXAMPLES_DIR.is_dir():
        f.error("examples-missing", f"{EXAMPLES_DIR} not found")
        return

    snapshot_docs: list[tuple[str, dict]] = []
    overrides_doc: dict | None = None
    valid_checked = 0

    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        if path.name in FRAGMENT_DEFS:
            continue  # handled by check_fragment_examples below
        doc = load_yaml(path)
        kind = doc.get("kind")
        schema_name = KIND_TO_SCHEMA.get(kind)
        if schema_name is None:
            f.error("example-kind", f"{path.name}: unrecognized kind {kind!r}")
            continue
        errs = iter_errors(doc_validator(schema_name, registry, docs), doc)
        if errs:
            for e in errs:
                loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
                f.error("example-invalid", f"{path.name}: expected valid, got {loc}: {e.message}")
            continue
        valid_checked += 1
        if kind == "xfactory_document_catalog":
            snapshot_docs.append((path.name, doc))
        elif kind == "xfactory_document_tag_overrides":
            overrides_doc = doc

    invalid_checked = check_negative_examples(f, registry, docs)
    check_fragment_examples(f, registry, docs)

    # Cross-cutting self-test: every shipped snapshot example must also
    # satisfy the deterministic checks task 2.3 owns, proving they do not
    # false-positive on real valid data.
    for label, doc in snapshot_docs:
        check_unique_identity(f, label, doc)
        check_source_freshness(f, label, doc)
        check_complete_coverage(f, label, doc, inventory=None, baseline=False)
        check_capability_resolution(f, label, doc)
        check_snapshot_review_standing(f, label, doc)
        check_review_source_freshness(f, label, doc, overrides_doc)
    if snapshot_docs:
        check_taxonomy_digest_consistency(f, snapshot_docs)
    if overrides_doc is not None:
        check_override_standing(f, "document-tag-overrides.example.yaml", overrides_doc)

    f.note(
        f"examples: {valid_checked} valid example(s) confirmed valid, "
        f"{invalid_checked} negative example(s) confirmed invalid"
    )


def check_negative_examples(f: Findings, registry: Registry, docs: dict[str, dict]) -> int:
    neg_dir = EXAMPLES_DIR / "negative"
    checked = 0
    if not neg_dir.is_dir():
        f.error("examples-missing", f"{neg_dir} not found")
        return checked
    for path in sorted(neg_dir.glob("*.yaml")):
        doc = load_yaml(path)
        if path.name in NEGATIVE_FRAGMENT_DEFS:
            schema_name, def_name = NEGATIVE_FRAGMENT_DEFS[path.name]
            validator = def_validator(schema_name, def_name, registry)
        else:
            kind = doc.get("kind")
            schema_name = KIND_TO_SCHEMA.get(kind)
            if schema_name is None:
                f.error("example-kind", f"negative/{path.name}: unrecognized kind {kind!r}")
                continue
            validator = doc_validator(schema_name, registry, docs)
        errs = iter_errors(validator, doc)
        if not errs:
            f.error("example-should-fail", f"negative/{path.name}: expected invalid, validated cleanly")
            continue
        checked += 1
    return checked


def check_fragment_examples(f: Findings, registry: Registry, docs: dict[str, dict]) -> None:
    for filename, (schema_name, def_name, container_key) in FRAGMENT_DEFS.items():
        path = EXAMPLES_DIR / filename
        if not path.is_file():
            f.error("examples-missing", f"{path} not found")
            continue
        validator = def_validator(schema_name, def_name, registry)
        items = (load_yaml(path) or {}).get(container_key) or []
        if not items:
            f.error("fragment-example-empty", f"{filename}: no items under {container_key!r}")
        for i, item in enumerate(items):
            errs = iter_errors(validator, item)
            if errs:
                f.error("fragment-example-invalid", f"{filename}[{i}]: expected valid: {errs[0].message}")


# --------------------------- shared entry helpers ---------------------------

def _entry_key(entry: dict) -> tuple:
    if "path" in entry:
        return (entry.get("repo"), "path", entry["path"])
    return (entry.get("repo"), "opaque", entry.get("document_ref"))


# --------------------------- 2. complete coverage ---------------------------

def check_complete_coverage(
    f: Findings, label: str, doc: dict, inventory: list[dict] | None, baseline: bool,
) -> None:
    """Spec requirement "Governed document catalog coverage", scenario
    "Catalog entry is missing or duplicated" (the missing half; duplication
    is check_unique_identity below), and "Full baseline and incremental
    refresh" scenario "First catalog run begins" (the disclosed baseline
    exception). Without an external `--inventory` this validator holds no
    ground truth for "missing" and says so rather than fabricating a count."""
    if inventory is None:
        f.note(f"{label}: coverage cross-check skipped (no --inventory supplied); "
               f"duplicate-identity remains enforced")
        return
    seen_keys = {_entry_key(e) for e in doc.get("entries") or []}
    expected_keys = {_entry_key(e) for e in inventory}
    missing = expected_keys - seen_keys
    extra = seen_keys - expected_keys
    report_missing = f.warn if baseline else f.error
    baseline_note = " (baseline mode: disclosed progress, not a regression)" if baseline else ""
    for key in sorted(missing, key=repr):
        report_missing("coverage-missing", f"{label}: inventory locator {key} has no matching catalog entry{baseline_note}")
    for key in sorted(extra, key=repr):
        f.error("coverage-extra", f"{label}: catalog entry {key} is not present in the current inventory (stale or phantom)")
    if baseline:
        f.note(f"{label}: coverage enforcement running in disclosed baseline mode ({len(missing)} pending)")


# --------------------------- 3. unique identity ---------------------------

def check_unique_identity(f: Findings, label: str, doc: dict) -> None:
    """Spec scenario "Catalog entry is missing or duplicated" (the
    duplication half): no locator key may appear more than once in one
    complete snapshot."""
    seen: dict[tuple, int] = {}
    for entry in doc.get("entries") or []:
        key = _entry_key(entry)
        seen[key] = seen.get(key, 0) + 1
    for key, count in seen.items():
        if count > 1:
            f.error("duplicate-identity", f"{label}: locator {key} appears {count} times in one snapshot")


# --------------------------- 4. source freshness ---------------------------

def check_source_freshness(f: Findings, label: str, doc: dict) -> None:
    """Spec scenario "Catalog entry is stale": a full mechanical snapshot
    updates every entry's current repository revision and inventory
    snapshot id from its own run. An entry recording a different revision
    or snapshot_id than the run that carries it is evidence stale relative
    to that run, never current — the one freshness dimension this
    validator can prove without the live shared inventory (codexFactory
    task 3.x owns cross-inventory freshness)."""
    run = doc.get("run") or {}
    run_rev = run.get("repository_revision")
    run_snap = run.get("inventory_snapshot_id")
    for entry in doc.get("entries") or []:
        key = _entry_key(entry)
        if run_rev is not None and entry.get("revision") != run_rev:
            f.error(
                "stale-revision",
                f"{label}: entry {key} revision {entry.get('revision')!r} != run.repository_revision {run_rev!r}",
            )
        if run_snap is not None and entry.get("snapshot_id") != run_snap:
            f.error(
                "stale-snapshot",
                f"{label}: entry {key} snapshot_id {entry.get('snapshot_id')!r} != run.inventory_snapshot_id {run_snap!r}",
            )


def check_review_source_freshness(
    f: Findings, label: str, doc: dict, overrides_doc: dict | None,
) -> None:
    """Spec scenario "Source content changes after review": an override's
    `source_content_hash` binds the disposition to one content state, so a
    snapshot facet still `reviewed`/`overridden` on an entry whose live
    `content_hash` no longer matches any matching override's bound hash has
    silently retained stale standing — it must re-enter classification
    instead. The one binding this validator can prove is against the
    override file it is given (the packaged example pair, or the scanned
    repo's `catalog/document-tag-overrides.yaml`); a reviewed facet with no
    matching override in that file is disclosed as unverifiable here, not
    silently accepted — the owning repository's own overrides pass holds
    that ground truth (same disclosure pattern as capability_refs above)."""
    overrides = (overrides_doc or {}).get("overrides") or []
    by_target: dict[tuple, list[dict]] = {}
    for ov in overrides:
        by_target.setdefault((_entry_key(ov), ov.get("facet")), []).append(ov)

    unverifiable = 0
    for entry in doc.get("entries") or []:
        key = _entry_key(entry)
        content_hash = entry.get("content_hash")
        for fa in entry.get("facet_assignments") or []:
            if fa.get("state") not in ("reviewed", "overridden"):
                continue
            candidates = by_target.get((key, fa.get("facet")), [])
            if not candidates:
                unverifiable += 1
                continue
            bound = sorted({ov.get("source_content_hash") for ov in candidates})
            if content_hash not in bound:
                f.error(
                    "stale-review",
                    f"{label}: entry {key} facet {fa.get('facet')!r} is {fa.get('state')} but no "
                    f"override binds the current content_hash {content_hash!r} (bound: {bound!r}) "
                    f"— source content changed after review, so the entry must re-enter "
                    f"classification, not retain reviewed standing",
                )
    if unverifiable:
        f.note(
            f"{label}: {unverifiable} reviewed/overridden facet(s) have no matching override in "
            f"the supplied override file; their hash binding is checked by the owning "
            f"repository's own catalog/document-tag-overrides.yaml pass, not here"
        )


# --------------------- 5. taxonomy resolution against registries ---------------------

def check_taxonomy_registries(f: Findings, registries: dict[str, dict]) -> None:
    """Spec scenario "Namespace ownership collides": the effective registry
    is the deterministic merge of every pinned registry file; a namespace
    id, tag id, or alias claimed by more than one owner across the merge is
    invalid."""
    namespace_owner: dict[str, tuple[str, str]] = {}
    tag_owner: dict[str, tuple[str, str]] = {}
    for label, doc in registries.items():
        for ns in doc.get("namespaces") or []:
            nid, owner = ns.get("id"), ns.get("owner")
            if nid in namespace_owner and namespace_owner[nid][0] != owner:
                f.error(
                    "namespace-collision",
                    f"namespace {nid!r} claimed by both {namespace_owner[nid]} and ({owner!r}, {label!r})",
                )
            else:
                namespace_owner.setdefault(nid, (owner, label))
        for bucket in ("tags", "proposed_tags", "retired_tags"):
            for tag in doc.get(bucket) or []:
                for tid in [tag.get("id")] + list(tag.get("aliases") or []):
                    if tid in tag_owner and tag_owner[tid][0] != tag.get("namespace"):
                        f.error(
                            "tag-collision",
                            f"tag id/alias {tid!r} claimed by both namespace {tag_owner[tid][0]!r} "
                            f"({tag_owner[tid][1]!r}) and {tag.get('namespace')!r} ({label!r})",
                        )
                    else:
                        tag_owner.setdefault(tid, (tag.get("namespace"), label))


def _effective_active_tags(registries: dict[str, dict]) -> set[str]:
    active: set[str] = set()
    for doc in registries.values():
        for tag in doc.get("tags") or []:
            if tag.get("status") == "active":
                active.add(tag["id"])
                active.update(tag.get("aliases") or [])
    return active


def check_topic_tag_resolution(f: Findings, label: str, doc: dict, registries: dict[str, dict]) -> None:
    """Spec scenario "Topic tag is unknown": a value absent from the merged
    active registry must remain a proposed tag and never enter the
    effective catalog."""
    active = _effective_active_tags(registries)
    for entry in doc.get("entries") or []:
        key = _entry_key(entry)
        for fa in entry.get("facet_assignments") or []:
            if fa.get("facet") != "topic_tags":
                continue
            for v in fa.get("values") or []:
                if v not in active:
                    f.error(
                        "topic-unresolved",
                        f"{label}: entry {key} topic_tags value {v!r} is not an active tag in the "
                        f"effective registry (must stay proposed, not effective)",
                    )


def check_capability_resolution(f: Findings, label: str, doc: dict) -> None:
    """Spec scenario "Capability cannot resolve", narrowed to what this
    checkout can itself verify: a `capability_refs` value naming
    `openxFactory` must resolve to a promoted (`openspec/specs/`) or active
    (`openspec/changes/`) capability id. A value naming any other
    repository is out of this checkout's reach and is left to that
    repository's own doc-health pass — noted, not silently accepted."""
    specs_dir = ROOT / "openspec" / "specs"
    changes_dir = ROOT / "openspec" / "changes"
    promoted = {p.name for p in specs_dir.iterdir() if p.is_dir()} if specs_dir.is_dir() else set()
    active = (
        {p.name for p in changes_dir.iterdir() if p.is_dir() and p.name != "archive"}
        if changes_dir.is_dir() else set()
    )
    known = promoted | active
    for entry in doc.get("entries") or []:
        key = _entry_key(entry)
        for fa in entry.get("facet_assignments") or []:
            if fa.get("facet") != "capability_refs":
                continue
            for v in fa.get("values") or []:
                if v.get("repository") != "openxFactory":
                    continue
                if v.get("capability") not in known:
                    f.error(
                        "capability-unresolved",
                        f"{label}: entry {key} capability_refs {v} does not resolve to a promoted "
                        f"or active openxFactory capability",
                    )


def check_taxonomy_digest_consistency(f: Findings, snapshots: list[tuple[str, dict]]) -> None:
    """Spec scenario "Registry repository changes elsewhere": the effective
    taxonomy digest is a function of ordered (repository, path,
    content_sha256, registry_version) tuples only — repository_revision and
    registry_revision are provenance and must never change it. This
    validator checks that invariant across every snapshot it is given
    rather than recomputing the digest bit-for-bit (recomputation is
    codexFactory's `document_catalog.py`, task 5.x)."""
    seen: dict[tuple, tuple[str, str]] = {}
    for label, doc in snapshots:
        taxonomy = doc.get("taxonomy") or {}
        sig = tuple(
            (i.get("repository"), i.get("path"), i.get("content_sha256"), i.get("registry_version"))
            for i in taxonomy.get("inputs") or []
        )
        digest = taxonomy.get("digest")
        if sig in seen and seen[sig][0] != digest:
            f.error(
                "taxonomy-digest-inconsistent",
                f"{label}: taxonomy inputs {sig} previously produced digest {seen[sig][0]!r} "
                f"(from {seen[sig][1]!r}) but this snapshot declares {digest!r}",
            )
        else:
            seen.setdefault(sig, (digest, label))


# --------------------------- 6. override standing ---------------------------

def _repo_domain_name(repo: str) -> str | None:
    if repo.startswith("xFactories/"):
        return repo.split("/", 1)[1]
    return None


def _standing_violation(repo: str, actor: str) -> str | None:
    """Reason `actor` lacks ownership standing for `repo`, or None if it
    holds standing (spec requirement "External catalog application and
    disposition authority": Domain Hermes for a domain-owned document, the
    openxFactory ratify authority for neutral/cross-repository documents).

    Neither the spec nor the schema mandates one literal actor string, so
    this checks the correct owning-authority CLASS for the correct
    repository (openxFactory ratify authority naming both "openxfactory"
    and "ratify"; a domain's Domain Hermes naming that domain specifically)
    rather than hardcoding the sibling codexFactory realization's exact
    `_owning_authority` convention (`scripts/doc_health/document_catalog.py`
    / `semantic.NEUTRAL_DISPOSER`) verbatim — that convention may reasonably
    reword without becoming a contract violation. Verifying the actor's
    real-world identity against a live authority directory is outside a
    static contract check."""
    lowered = (actor or "").lower()
    domain = _repo_domain_name(repo)
    if domain is None:
        if "openxfactory" not in lowered or "ratify" not in lowered:
            return (f"repo {repo!r} is neutral/cross-repository; "
                    f"does not name the openxFactory ratify authority")
        return None
    if domain.lower() not in lowered:
        return (f"repo {repo!r} is domain-owned; "
                f"does not name {domain}'s Domain Hermes authority")
    return None


def check_override_standing(f: Findings, label: str, doc: dict) -> None:
    """Spec scenario "Unauthorized override is supplied", applied to the
    owner override file: each override's `actor` must hold ownership
    standing for its target repository (see `_standing_violation`)."""
    for i, ov in enumerate(doc.get("overrides") or []):
        reason = _standing_violation(ov.get("repo") or "", ov.get("actor") or "")
        if reason is not None:
            f.error("override-standing", f"{label}[{i}]: actor {ov.get('actor')!r}: {reason}")


def check_snapshot_review_standing(f: Findings, label: str, doc: dict) -> None:
    """Spec scenario "Unauthorized override is supplied", applied to the
    artifact where reviewed/overridden state actually lives: a catalog
    snapshot entry's `facet_assignments[].review.authority` must hold
    ownership standing for that entry's `repo` (see `_standing_violation`)
    — the spec's "aggregation-side edits or actors without standing MUST
    NOT create reviewed or overridden state" is otherwise unenforceable on
    a committed `status: record` snapshot. The codexFactory realization's
    `_override_standing_findings` checks this same merged surface."""
    for entry in doc.get("entries") or []:
        key = _entry_key(entry)
        repo = entry.get("repo") or ""
        for fa in entry.get("facet_assignments") or []:
            review = fa.get("review")
            if not isinstance(review, dict):
                # reviewed/overridden without a review block is a schema
                # violation caught before this check runs.
                continue
            reason = _standing_violation(repo, review.get("authority") or "")
            if reason is not None:
                f.error(
                    "override-standing",
                    f"{label}: entry {key} facet {fa.get('facet')!r} review.authority "
                    f"{review.get('authority')!r}: {reason}",
                )


# --------------------------- 7. immutable path layout ---------------------------

def check_immutable_path_layout(f: Findings, repo: Path, path: Path, doc: dict, kind: str) -> None:
    """Spec requirement "Governed document catalog coverage" (snapshot path)
    and "Bounded cataloger execution and protected evidence" (recommendation
    path): evidence must live at
    `health/document-catalog/runs/YYYY-MM-DD/<run-id>/<repo-with-slashes>.yaml`
    or `health/document-catalog/recommendations/YYYY-MM-DD/<job-id>.yaml`.
    Only applies to files discovered under a real `health/document-catalog/`
    tree — the packaged reference examples are static material outside that
    tree by design (see `examples/document-cataloging/README.md`)."""
    rel = path.relative_to(repo)
    parts = rel.parts
    if kind == "snapshot":
        if len(parts) < 6 or parts[0:3] != ("health", "document-catalog", "runs"):
            f.error("path-layout", f"{rel}: snapshot not under health/document-catalog/runs/<date>/<run-id>/")
            return
        date, run_id = parts[3], parts[4]
        if not DATE_RE.match(date):
            f.error("path-layout", f"{rel}: run date segment {date!r} is not YYYY-MM-DD")
        run = doc.get("run") or {}
        if run_id != run.get("run_id"):
            f.error("path-layout", f"{rel}: run-id path segment {run_id!r} != run.run_id {run.get('run_id')!r}")
        repo_from_path = str(Path(*parts[5:]).with_suffix(""))
        declared_repo = run.get("repository")
        if repo_from_path != declared_repo:
            f.error("path-layout", f"{rel}: repo-derived path {repo_from_path!r} != run.repository {declared_repo!r}")
    elif kind == "recommendation":
        if len(parts) != 5 or parts[0:3] != ("health", "document-catalog", "recommendations"):
            f.error("path-layout", f"{rel}: expected health/document-catalog/recommendations/<date>/<job-id>.yaml")
            return
        date, filename = parts[3], parts[4]
        if not DATE_RE.match(date):
            f.error("path-layout", f"{rel}: recommendation date segment {date!r} is not YYYY-MM-DD")
        job_id_from_path = filename[: -len(".yaml")] if filename.endswith(".yaml") else filename
        if job_id_from_path != doc.get("job_id"):
            f.error("path-layout", f"{rel}: filename {filename!r} != job_id {doc.get('job_id')!r}")
    else:  # pragma: no cover - programmer error
        raise ValueError(f"unknown path-layout kind {kind!r}")


# --------------------------- layer 2: real repo tree ---------------------------

def load_inventory(path: Path) -> list[dict]:
    doc = load_yaml(path)
    if isinstance(doc, list):
        return doc
    return (doc or {}).get("entries") or []


def check_repo_tree(
    f: Findings, registry: Registry, docs: dict[str, dict], repo: Path,
    baseline: bool, inventory: list[dict] | None,
) -> None:
    checked = 0
    registries: dict[str, dict] = {}

    neutral = repo / "contracts" / "document-tag-registry.yaml"
    domain = repo / "catalog" / "document-tag-registry.yaml"
    for label, path in (("neutral", neutral), ("domain", domain)):
        if not path.is_file():
            f.note(f"{path.relative_to(repo)} not present; skipped")
            continue
        doc = load_yaml(path)
        errs = iter_errors(doc_validator("xfactory-document-tag-registry.schema.yaml", registry, docs), doc)
        if errs:
            for e in errs:
                f.error("registry-invalid", f"{path.relative_to(repo)}: {e.message}")
            continue
        checked += 1
        registries[label] = doc
    if registries:
        check_taxonomy_registries(f, registries)
    else:
        f.note("no document-tag-registry.yaml files present; taxonomy cross-registry checks skipped")

    overrides_doc: dict | None = None
    overrides_path = repo / "catalog" / "document-tag-overrides.yaml"
    if overrides_path.is_file():
        doc = load_yaml(overrides_path)
        errs = iter_errors(doc_validator("xfactory-document-tag-overrides.schema.yaml", registry, docs), doc)
        if errs:
            for e in errs:
                f.error("overrides-invalid", f"{overrides_path.relative_to(repo)}: {e.message}")
        else:
            checked += 1
            check_override_standing(f, str(overrides_path.relative_to(repo)), doc)
            overrides_doc = doc
    else:
        f.note(f"{overrides_path.relative_to(repo)} not present; override-file standing checks skipped "
               f"(snapshot review.authority standing is still checked per snapshot)")

    runs_dir = repo / "health" / "document-catalog" / "runs"
    snapshot_files = sorted(runs_dir.rglob("*.yaml")) if runs_dir.is_dir() else []
    snapshot_docs: list[tuple[str, dict]] = []
    for path in snapshot_files:
        doc = load_yaml(path)
        if doc.get("kind") != "xfactory_document_catalog":
            continue
        rel = str(path.relative_to(repo))
        errs = iter_errors(doc_validator("xfactory-document-catalog-snapshot.schema.yaml", registry, docs), doc)
        if errs:
            for e in errs:
                f.error("snapshot-invalid", f"{rel}: {e.message}")
            continue
        checked += 1
        check_unique_identity(f, rel, doc)
        check_source_freshness(f, rel, doc)
        run_repo = (doc.get("run") or {}).get("repository")
        repo_inventory = [i for i in inventory if i.get("repo") == run_repo] if inventory else None
        check_complete_coverage(f, rel, doc, repo_inventory, baseline)
        check_immutable_path_layout(f, repo, path, doc, kind="snapshot")
        if registries:
            check_topic_tag_resolution(f, rel, doc, registries)
        check_capability_resolution(f, rel, doc)
        check_snapshot_review_standing(f, rel, doc)
        check_review_source_freshness(f, rel, doc, overrides_doc)
        snapshot_docs.append((rel, doc))
    if snapshot_docs:
        check_taxonomy_digest_consistency(f, snapshot_docs)
    if not snapshot_files:
        f.note("no snapshots under health/document-catalog/runs/; deterministic catalog checks skipped (pre-baseline)")

    rec_dir = repo / "health" / "document-catalog" / "recommendations"
    rec_files = sorted(rec_dir.rglob("*.yaml")) if rec_dir.is_dir() else []
    for path in rec_files:
        doc = load_yaml(path)
        if doc.get("kind") != "xfactory_document_catalog_recommendation":
            continue
        rel = str(path.relative_to(repo))
        errs = iter_errors(doc_validator("xfactory-document-cataloger-recommendation.schema.yaml", registry, docs), doc)
        if errs:
            for e in errs:
                f.error("recommendation-invalid", f"{rel}: {e.message}")
            continue
        checked += 1
        check_immutable_path_layout(f, repo, path, doc, kind="recommendation")
    if not rec_files:
        f.note("no recommendation evidence under health/document-catalog/recommendations/; skipped")

    f.note(f"repo tree ({repo}): {checked} real document-cataloging artifact(s) checked")


# --------------------------- orchestration ---------------------------

def run(repo: Path, baseline: bool, strict: bool, inventory_path: Path | None) -> int:
    f = Findings()
    if not SCHEMAS_DIR.is_dir():
        print(f"ERROR {SCHEMAS_DIR} not found", file=sys.stderr)
        return 2

    registry, docs = build_registry()
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-invalid", f"{name}: {exc}")

    inventory = load_inventory(inventory_path) if inventory_path else None

    check_examples(f, registry, docs)
    check_repo_tree(f, registry, docs, repo, baseline, inventory)

    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)

    n_e, n_w = len(f.errors), len(f.warnings)
    print(f"\nvalidate-document-catalog: {n_e} error(s), {n_w} warning(s)")
    if n_e or (strict and n_w):
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default=str(ROOT),
                     help="repo root to scan for real document-cataloging artifacts (default: this checkout)")
    ap.add_argument("--inventory", type=Path, default=None,
                     help="optional shared-inventory file ({repo, path|document_ref} list) for exact coverage checking")
    ap.add_argument("--baseline", action="store_true",
                     help="disclose baseline mode: downgrade missing-coverage findings to warnings")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    try:
        return run(Path(args.repo).resolve(), args.baseline, args.strict, args.inventory)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
