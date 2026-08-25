"""Thirteenth deterministic doc-health family: document-catalog
integrity (US3; feature tasks T013/T014).

Realizes the openxFactory `add-document-cataloging` contract's
deterministic-family requirement (FR-006/FR-007): validates the
mechanical catalog's own coverage, structural integrity, and reported
classification-facet shape against the live corpus and the promoted
contract's controlled vocabularies — never mutating source content,
never judging or auto-fixing a structurally valid but semantically
debatable classification (spec US3 acceptance 3), never converting a
catalog value into routing or lifecycle authority (FR-007).

Twelve finding classes exist here (module-interfaces.md), encoded as a
``[<class>] `` prefix on each finding's ``rule`` text (this family's own
convention — the ``Finding`` dataclass has no dedicated "check" field,
so the bracket tag is what lets tests and report consumers select a
specific check's findings, the same way other multi-check families
disambiguate through distinctive rule wording):

    coverage, duplicate-key, stale-entry, artifact-type, taxonomy
    (controlled facet/state/value vocabularies, a malformed
    ``state_since``, tag-registry topic tags, and the recorded taxonomy
    block), resolution (capability_refs), confidence, provenance,
    override-standing, immutable-path, recursion, pending-aging

A thirteenth defensive class, ``catalog-integrity``, is not a per-defect
check but the family's last line of defense: an unparseable, torn, or
wrong-shape PERSISTED catalog artifact (run.yaml, snapshot, baseline
shard, marker, or merged fold) surfaces from the load helpers as a
controlled ``catalog.CatalogError`` and is reported as one
``catalog-integrity`` finding rather than crashing the whole doc-health
run (the contract rule every checker relies on: malformed persisted data
is reported, never fatal).

Resolution semantics (research D6): the twelve classes are NOT
uniformly auto-fixable or contested, so — unlike the wholly-contested
families in ``families.FAMILY_RESOLUTION`` — this family is
deliberately absent from that table and instead sets ``resolution``
per finding below (mechanical/regeneration-fixable classes keep the
``Finding`` default ``auto-fixable``; override standing, aging
escalations, and semantic-disagreement classes are always
``contested``, exactly as D6 specifies). Adding "document-catalog" to
``FAMILY_RESOLUTION`` would force one resolution onto every class here
and contradict D6's own wording.

Data sources this family reads (never writes):

- The live corpus, rebuilt fresh via ``inventory.build_inventory`` /
  ``catalog.mechanical_entries`` from ``ctx.docs`` — the same corpus
  every other family sees.
- Whatever the mechanical catalog has already recorded under
  ``ctx.catalog_root`` (the completed baseline fold, plus the latest
  incremental run snapshot layered on top — module-interfaces.md
  ``catalog.load_snapshot``/``catalog_baseline.load_baseline``).

Classification facets — the contract's six controlled facets
(``factory_scope``, ``domain_contexts``, ``capability_refs``,
``topic_tags``, ``document_role``, ``sensitivity_signal``), carried on
each entry as the ``facet_assignments`` LIST of ``{facet, values,
state, state_since, provenance, transitions, review}`` items per the
promoted ``document-catalog.template.yaml`` (never a dict keyed by
facet name) — are not yet written by any module in this feature slice
(the cataloger worker is a later phase) — but this family validates
whatever facet data IS present on a persisted entry, per the
data-model.md facet state machine, independent of which process wrote
it. A persisted entry lacking a ``facet_assignments`` key entirely is
simply outside the classification lifecycle so far and is invisible to
the facet-shaped checks (taxonomy, resolution, confidence, provenance,
override-standing, pending-aging) — only coverage/stale-entry/
duplicate-key/artifact-type/immutable-path/recursion apply to every
entry unconditionally.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from . import AUTO_FIXABLE, CONTESTED, ERROR, INFO, WARNING, Finding, Skip
from . import catalog, catalog_baseline, inventory
from .semantic import NEUTRAL_DISPOSER, NEUTRAL_REPO

FAMILY = "document-catalog"

# The contract's six controlled classification facets ("Controlled
# classification facets and provenance"). Entries carry them as a
# `facet_assignments` LIST of {facet, values, state, state_since,
# provenance, transitions, review} items (document-catalog.template.yaml)
# — never a dict keyed by facet name.
FACET_NAMES = ("factory_scope", "domain_contexts", "capability_refs",
               "topic_tags", "document_role", "sensitivity_signal")

# Closed value vocabularies the contract fixes directly (taxonomy
# class). `capability_refs` values are {repository, capability} pairs
# resolved against promoted/active OpenSpec capabilities via
# ctx.capabilities (resolution class — see _resolves_capability);
# `topic_tags` resolve against the versioned namespaced tag registries
# (taxonomy class — see _controlled_tag_ids); `domain_contexts` values
# are canonical repository IDs with no closed contract vocabulary and
# no in-corpus registry authority, so they receive the shared shape/
# state/provenance validation only.
FACTORY_SCOPES = ("neutral", "domain", "cross_domain", "aggregation",
                  "install_runtime", "unknown")
DOCUMENT_ROLES = ("policy", "contract", "architecture", "process",
                  "runbook", "template", "example", "evidence",
                  "register", "idea", "specification", "other")
SENSITIVITY_SIGNALS = ("unspecified", "potentially_sensitive")
CLOSED_VOCABULARIES = {
    "factory_scope": FACTORY_SCOPES,
    "document_role": DOCUMENT_ROLES,
    "sensitivity_signal": SENSITIVITY_SIGNALS,
}

# The contract's six facet states; model output only ever *suggests*.
FACET_STATES = ("pending", "suggested", "reviewed", "overridden",
                "unclassified", "policy_blocked")

ARTIFACT_TYPES = {inventory.GOVERNANCE_MARKDOWN, inventory.PROMOTED_SPEC}

PENDING_WARNING_DAYS_DEFAULT = 30
PENDING_ERROR_DAYS_DEFAULT = 90

CONFIDENCE_RANGE = (0.0, 1.0)
# Per-facet provenance shape per the promoted template: these scalar
# fields must be present and non-empty. `confidence` nests INSIDE the
# provenance block and is checked separately as a numeric in [0, 1];
# `evidence_refs` must be present as a list — an empty list is a valid
# recorded value (the template records `evidence_refs: []`), so
# presence-as-a-list, not truthiness, is what is checked;
# `prompt_contract_version` is likewise checked separately — the
# contract snapshot schema fixes it as `{type: integer, minimum: 1}`
# (cataloger.py's `_prompt_contract_version` enforces the same at write
# time), so a bare truthiness check would let a hand-authored string
# like `"2"` slip past even though it fails the contract schema; `bool`
# is excluded explicitly since it is an `int` subclass in Python.
PROVENANCE_FIELDS = ("taxonomy_sha256", "method", "classifier_version",
                     "model", "section", "passage_sha256")

# Facet states that legitimately carry NO classifier output, out of the
# contract's six-state vocabulary (pending / suggested / reviewed /
# overridden / unclassified / policy_blocked — "Controlled
# classification facets and provenance"): `pending` precedes any
# recommendation; `unclassified` records that no controlled value could
# resolve ("Capability cannot resolve"); and a `policy_blocked` facet
# was never dispatched to a classifier at all — orchestration records
# only an opaque blocker reference ("Host is not authorized for
# protected content"). None of these is a confidence/provenance shape
# defect; only states produced from a validated recommendation
# (suggested, plus the reviewed/overridden dispositions layered on one)
# must carry a bounded confidence and complete provenance.
NO_CLASSIFIER_OUTPUT_STATES = ("pending", "unclassified", "policy_blocked")

REGISTRY_FILENAME = "document-tag-registry.yaml"
_TAG_ID_RE = re.compile(r"^\s*-\s*id:\s*(\S+)\s*$", re.MULTILINE)
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _finding(cls: str, severity: str, repo: str, path: str, detail: str,
            action: str, resolution: str = AUTO_FIXABLE) -> Finding:
    return Finding(severity, FAMILY, repo, path, f"[{cls}] {detail}", action,
                  resolution=resolution)


# --- shared corpus/catalog state --------------------------------------------

def _live_mechanical_entries(ctx) -> list[dict] | None:
    """Live mechanical entries recomputed from the current corpus, or
    None when the owning repositories' HEAD revisions cannot be
    resolved (e.g. a checkout without git metadata) — coverage and
    staleness degrade to silence rather than crash the family
    (``corpus.RealGit`` precedent: every git-derived fact degrades to
    None on failure so callers can skip-with-notice instead of
    crashing)."""
    try:
        inv = inventory.build_inventory(ctx.docs, ctx.repo_paths, git=ctx.git)
    except ValueError:
        return None
    return catalog.mechanical_entries(inv)


def _entries_of(doc) -> list:
    """The persisted document's ``entries`` as a list — tolerant of a
    corrupt or foreign snapshot/baseline that lacks the key or carries a
    non-list under it. Unparseable/non-object files are already rejected
    at load time (``catalog._load_yaml_json`` / ``load_baseline`` raise
    ``CatalogError`` the family surfaces as an integrity finding); this
    guard keeps a merely-incomplete-but-parseable record from raising a
    ``KeyError``/``AttributeError`` mid-check, so every entry-shaped check
    reads only well-formed rows."""
    entries = doc.get("entries") if isinstance(doc, dict) else None
    return entries if isinstance(entries, list) else []


def _baseline_entries(ctx) -> list[dict]:
    baseline = catalog_baseline.load_baseline(ctx.catalog_root)
    return _entries_of(baseline) if baseline else []


def _persisted_snapshot_repos(ctx) -> dict:
    """{repo: snapshot_document} for the latest recorded run, or {}."""
    latest = catalog.load_snapshot(ctx.catalog_root)
    return latest["repos"] if latest else {}


def _all_raw_persisted_entries(ctx) -> list[dict]:
    entries = list(_baseline_entries(ctx))
    for doc in _persisted_snapshot_repos(ctx).values():
        entries.extend(_entries_of(doc))
    return entries


def _key_map(entries) -> dict:
    """Best-effort locator -> entry map: generated-catalog paths are
    excluded (the recursion check reports those separately) and
    ambiguous or duplicate-keyed rows are skipped (the duplicate-key
    check — ``_duplicate_key_findings``, including its
    ``_ambiguous_locator_findings`` scan — reports those) — every
    other check below compares only well-formed, in-scope entries, so
    one corrupted row never silently corrupts an unrelated check's
    result."""
    out = {}
    for e in entries:
        path = e.get("path")
        if path and inventory.is_generated_catalog_path(path):
            continue
        try:
            key = catalog._entry_key(e)
        except ValueError:
            continue
        out.setdefault(key, e)
    return out


def _catalogued_key_map(ctx) -> dict:
    """(repo, locator) -> entry across the merged baseline and the
    latest incremental run, latest-run entries taking precedence
    (module-interfaces.md: ``load_snapshot`` returns the latest
    recorded run; post-baseline changes flow through it)."""
    out = _key_map(_baseline_entries(ctx))
    for doc in _persisted_snapshot_repos(ctx).values():
        out.update(_key_map(_entries_of(doc)))
    return out


def _label(entry: dict, key: tuple) -> str:
    return entry.get("path", key[1])


def _facet_assignments(entry: dict) -> list:
    """The entry's recorded ``facet_assignments`` items that are shaped
    as mappings. The list-shape and item-shape violations themselves are
    reported by ``_taxonomy_findings`` (contract entry shape: a LIST of
    assignment items, never a dict keyed by facet name), so every other
    facet check reads only well-formed items and never double-reports
    the same shape defect."""
    assignments = entry.get("facet_assignments")
    if not isinstance(assignments, list):
        return []
    return [a for a in assignments if isinstance(a, dict)]


def _assignment_values(assignment: dict) -> list:
    values = assignment.get("values")
    if values is None:
        return []
    return list(values) if isinstance(values, list) else [values]


# --- coverage (post-baseline only) and stale-entry ---------------------------

def _baseline_progress_findings(ctx) -> list[Finding]:
    bp = catalog_baseline.progress(ctx.catalog_root)
    return [_finding(
        "coverage", INFO, "(baseline)", "(progress)",
        f"baseline coverage {bp.cataloged}/{bp.total} entries "
        f"({bp.percent:.1f}%) across {bp.repos_complete}/{bp.repos_total} "
        "repositories",
        "resume the sharded baseline build to enable complete-coverage "
        "enforcement")]


def _coverage_findings(ctx, live_entries) -> list[Finding]:
    if not catalog_baseline.is_baseline_complete(ctx.catalog_root):
        # US2 acceptance 2 / US3 acceptance 4: progress, never one
        # missing-entry finding per legacy document.
        return _baseline_progress_findings(ctx)
    if live_entries is None:
        return []
    catalogued = _catalogued_key_map(ctx)
    findings = []
    for entry in live_entries:
        key = catalog._entry_key(entry)
        if key not in catalogued:
            findings.append(_finding(
                "coverage", ERROR, entry["repo"], _label(entry, key),
                "document has no catalog entry",
                "run the mechanical catalog pass to add this document"))
    return findings


def _stale_entry_findings(ctx, live_entries) -> list[Finding]:
    """Spec US3 acceptance 2 / contract scenario "Catalog entry is
    stale": an entry whose HASH OR REVISION no longer matches the
    inventory is stale. Revision staleness is deliberately broader than
    ``catalog.diff``'s content-hash-only "modified" semantics (design
    decision 8 governs snapshot diffs, not evidence freshness): an
    unrelated commit moving the owning repository's HEAD makes the
    recorded entry unusable as CURRENT catalog evidence even when its
    content happens to be byte-identical, and the doc-health contract
    spec ("Catalog entry does not match inventory") requires a
    stale-catalog finding for exactly that case."""
    catalogued = _catalogued_key_map(ctx)
    if not catalogued or live_entries is None:
        return []
    live_map = {catalog._entry_key(e): e for e in live_entries}
    findings = []
    for key, entry in sorted(catalogued.items()):
        live_entry = live_map.get(key)
        label = _label(entry, key)
        if live_entry is None:
            findings.append(_finding(
                "stale-entry", ERROR, entry.get("repo", key[0]), label,
                "catalog entry's document no longer exists in the "
                "governed corpus",
                "run the mechanical catalog pass to refresh the catalog"))
            continue
        if live_entry["content_hash"] != entry.get("content_hash"):
            findings.append(_finding(
                "stale-entry", ERROR, entry.get("repo", key[0]), label,
                "catalog entry's content hash no longer matches the "
                "governed document",
                "run the mechanical catalog pass to refresh the catalog"))
        if live_entry["revision"] != entry.get("revision"):
            findings.append(_finding(
                "stale-entry", ERROR, entry.get("repo", key[0]), label,
                "catalog entry's repository revision no longer matches "
                "the owning repository",
                "run the mechanical catalog pass to refresh the catalog"))
    return findings


# --- duplicate-key (unique-key integrity) ---------------------------------------

def _first_duplicate(entries) -> tuple | None:
    seen = set()
    for e in entries:
        try:
            key = catalog._entry_key(e)
        except ValueError:
            continue  # unkeyable: _ambiguous_locator_findings reports it
        if key in seen:
            return key
        seen.add(key)
    return None


def _ambiguous_locator_findings(entries, where: str, action: str) \
        -> list[Finding]:
    """Recorded rows whose document locator is ambiguous (contract
    scenario "Locator is ambiguous": a persisted path plus an opaque
    reference, or neither). No unique catalog key can be derived from
    such a row, so it is reported under this unique-key integrity
    check (FR-006 "unique-key") rather than silently dropped — a
    hand-corrupted row with no live counterpart would otherwise be
    invisible to every check, including the stale-entry orphan scan."""
    findings = []
    for e in entries:
        path = e.get("path")
        if path and inventory.is_generated_catalog_path(path):
            continue  # the recursion check reports these
        try:
            catalog._entry_key(e)
        except ValueError as exc:
            findings.append(_finding(
                "duplicate-key", ERROR, e.get("repo", "(unknown)"),
                path or e.get("document_ref") or "(unknown locator)",
                f"entry recorded in {where} has an ambiguous document "
                f"locator, so no unique catalog key exists: {exc}",
                action))
    return findings


def _duplicate_key_findings(ctx) -> list[Finding]:
    findings = []
    for repo, doc in sorted(_persisted_snapshot_repos(ctx).items()):
        run_action = "regenerate the snapshot from a clean mechanical pass"
        findings.extend(_ambiguous_locator_findings(
            _entries_of(doc), f"the latest run for repository {repo!r}",
            run_action))
        dup = _first_duplicate(_entries_of(doc))
        if dup:
            findings.append(_finding(
                "duplicate-key", ERROR, dup[0], dup[1],
                f"duplicate catalog key recorded in the latest run for "
                f"repository {repo!r}", run_action))
    baseline_action = "re-run the baseline merge from clean shard chains"
    findings.extend(_ambiguous_locator_findings(
        _baseline_entries(ctx), "the merged baseline", baseline_action))
    dup = _first_duplicate(_baseline_entries(ctx))
    if dup:
        findings.append(_finding(
            "duplicate-key", ERROR, dup[0], dup[1],
            "duplicate catalog key recorded in the merged baseline",
            baseline_action))
    return findings


# --- artifact-type -------------------------------------------------------------

def _artifact_type_findings(ctx) -> list[Finding]:
    findings = []
    for key, entry in sorted(_catalogued_key_map(ctx).items()):
        at = entry.get("artifact_type")
        if at not in ARTIFACT_TYPES:
            findings.append(_finding(
                "artifact-type", ERROR, entry.get("repo", key[0]),
                _label(entry, key),
                f"artifact_type {at!r} is outside the contract "
                f"vocabulary ({', '.join(sorted(ARTIFACT_TYPES))})",
                "correct artifact_type and regenerate the entry"))
    return findings


# --- taxonomy / controlled-value ----------------------------------------------

def _controlled_tag_ids(ctx) -> set[str]:
    """Every tag id declared by a ``document-tag-registry.yaml`` found
    under any repository in scope (regex-parsed, matching
    ``catalog.registry_input``'s minimal-parse precedent — no new YAML
    dependency)."""
    ids = set()
    for repo_path in ctx.repo_paths.values():
        repo_path = Path(repo_path)
        for reg in sorted(repo_path.rglob(REGISTRY_FILENAME)):
            rel = reg.relative_to(repo_path).as_posix()
            if inventory.is_generated_catalog_path(rel):
                continue
            ids.update(_TAG_ID_RE.findall(reg.read_text(encoding="utf-8")))
    return ids


def _facet_shape_findings(entry: dict, repo: str, path: str) \
        -> list[Finding]:
    """Contract entry-shape violations: ``facet_assignments`` must be a
    LIST of assignment mappings (document-catalog.template.yaml), and no
    facet may be assigned twice — the dict-keyed shape made duplicates
    structurally impossible, so the list shape carries an explicit
    uniqueness check instead."""
    findings = []
    raw = entry.get("facet_assignments")
    if raw is None:
        return findings
    if not isinstance(raw, list):
        return [_finding(
            "taxonomy", ERROR, repo, path,
            "facet_assignments is not a list of facet-assignment items "
            "(the contract entry shape is a list of {facet, values, "
            "state, ...} items, never a mapping keyed by facet name)",
            "regenerate the entry in the contract facet_assignments "
            "shape")]
    for item in raw:
        if not isinstance(item, dict):
            findings.append(_finding(
                "taxonomy", ERROR, repo, path,
                f"facet_assignments item {item!r} is not a "
                "facet-assignment mapping",
                "regenerate the entry in the contract facet_assignments "
                "shape"))
    seen = set()
    for assignment in _facet_assignments(entry):
        facet = assignment.get("facet")
        if facet in seen:
            findings.append(_finding(
                "taxonomy", ERROR, repo, path,
                f"facet {facet!r} is assigned more than once in "
                "facet_assignments",
                "collapse the duplicate assignments into one per facet"))
        seen.add(facet)
    return findings


def _taxonomy_findings(ctx) -> list[Finding]:
    findings = []
    for repo, doc in sorted(_persisted_snapshot_repos(ctx).items()):
        try:
            catalog._validate_taxonomy(doc.get("taxonomy"))
        except ValueError as exc:
            findings.append(_finding(
                "taxonomy", ERROR, repo, "(taxonomy)",
                f"recorded taxonomy block is invalid: {exc}",
                "regenerate the snapshot with a valid effective-taxonomy "
                "block"))
    tag_ids = _controlled_tag_ids(ctx)
    for key, entry in sorted(_catalogued_key_map(ctx).items()):
        repo = entry.get("repo", key[0])
        path = _label(entry, key)
        findings.extend(_facet_shape_findings(entry, repo, path))
        for assignment in _facet_assignments(entry):
            facet = assignment.get("facet")
            if facet not in FACET_NAMES:
                findings.append(_finding(
                    "taxonomy", ERROR, repo, path,
                    f"facet {facet!r} is not one of the contract's six "
                    f"controlled facets ({', '.join(FACET_NAMES)})",
                    "regenerate the assignment under a controlled facet"))
                continue
            state = assignment.get("state")
            if state not in FACET_STATES:
                findings.append(_finding(
                    "taxonomy", ERROR, repo, path,
                    f"{facet} facet state {state!r} is outside the "
                    "contract's six-state vocabulary "
                    f"({', '.join(FACET_STATES)})",
                    "record one of the contract facet states"))
            vocabulary = CLOSED_VOCABULARIES.get(facet)
            # Cardinality: the contract's closed-vocabulary facets are
            # exactly its three single-valued ones ("factory_scope SHALL
            # be one of ...", "document roles SHALL be ...", "sensitivity
            # signals SHALL be only ...") — never a list of more than one
            # value. Skipped for no-classifier-output states (pending /
            # unclassified / policy_blocked), which legitimately carry
            # `values: []` (contract scenario "Pending input changes
            # again"; the confidence/provenance checks below use the same
            # scope).
            if (vocabulary is not None
                    and state not in NO_CLASSIFIER_OUTPUT_STATES):
                count = len(_assignment_values(assignment))
                if count != 1:
                    findings.append(_finding(
                        "taxonomy", ERROR, repo, path,
                        f"{facet} carries {count} values but the "
                        "contract requires exactly one single value "
                        f"({', '.join(vocabulary)})",
                        "record exactly one contract vocabulary value "
                        "for this single-valued facet"))
            for value in _assignment_values(assignment):
                if vocabulary is not None and value not in vocabulary:
                    findings.append(_finding(
                        "taxonomy", ERROR, repo, path,
                        f"{facet} value {value!r} is outside the contract "
                        f"vocabulary ({', '.join(vocabulary)})",
                        "correct the facet to a contract vocabulary "
                        "value", resolution=CONTESTED))
                elif facet == "topic_tags" and value not in tag_ids:
                    # Contract "Topic tag is unknown": an unregistered
                    # tag may exist only as a PROPOSED tag (the
                    # template's `proposed_values`), never in the
                    # effective `values`.
                    findings.append(_finding(
                        "taxonomy", ERROR, repo, path,
                        f"topic_tags value {value!r} is not a controlled "
                        "tag registry value",
                        "correct the tag to a registered controlled "
                        "value or keep it in proposed_values until the "
                        "owning registry accepts it",
                        resolution=CONTESTED))
    return findings


# --- resolution (capability_refs) ----------------------------------------------

def _resolves_capability(ctx, repository: str, capability: str) -> bool:
    """A capability reference resolves when its own named canonical
    repository publishes a promoted or active OpenSpec capability of
    that name (contract: capability references SHALL name a canonical
    repository AND a promoted-or-active capability). ``ctx.capabilities``
    is the same per-repository promoted/active capability index
    ``families._resolve_capability`` reads; the lookup key here is the
    reference's OWN declared repository — the contract value shape
    carries it — rather than the entry's owning repo."""
    return capability in ctx.capabilities.get(repository, set())


def _resolution_findings(ctx) -> list[Finding]:
    findings = []
    for key, entry in sorted(_catalogued_key_map(ctx).items()):
        repo = entry.get("repo", key[0])
        path = _label(entry, key)
        for assignment in _facet_assignments(entry):
            if assignment.get("facet") != "capability_refs":
                continue
            for value in _assignment_values(assignment):
                if not (isinstance(value, dict) and value.get("repository")
                        and value.get("capability")):
                    findings.append(_finding(
                        "resolution", WARNING, repo, path,
                        f"capability_refs value {value!r} does not name "
                        "a canonical repository and capability",
                        "record the reference as a {repository, "
                        "capability} pair", resolution=CONTESTED))
                    continue
                if not _resolves_capability(ctx, value["repository"],
                                            value["capability"]):
                    findings.append(_finding(
                        "resolution", WARNING, repo, path,
                        f"capability {value['capability']!r} does not "
                        "resolve to a promoted or active OpenSpec "
                        f"capability in repository "
                        f"{value['repository']!r}",
                        "point the reference at an existing OpenSpec "
                        "capability or leave the facet unclassified",
                        resolution=CONTESTED))
    return findings


# --- confidence / provenance shape --------------------------------------------

def _confidence_provenance_findings(ctx) -> list[Finding]:
    findings = []
    lo, hi = CONFIDENCE_RANGE
    for key, entry in sorted(_catalogued_key_map(ctx).items()):
        repo = entry.get("repo", key[0])
        path = _label(entry, key)
        for assignment in _facet_assignments(entry):
            facet = assignment.get("facet")
            state = assignment.get("state")
            if state in NO_CLASSIFIER_OUTPUT_STATES \
                    or state not in FACET_STATES:
                # No classifier output (see NO_CLASSIFIER_OUTPUT_STATES),
                # or an out-of-vocabulary state the taxonomy check
                # already reports — neither is a shape defect here.
                continue
            provenance = assignment.get("provenance") or {}
            confidence = provenance.get("confidence")
            if (isinstance(confidence, bool)
                    or not isinstance(confidence, (int, float))
                    or not (lo <= confidence <= hi)):
                findings.append(_finding(
                    "confidence", ERROR, repo, path,
                    f"{facet} facet provenance confidence {confidence!r} "
                    "is not a numeric value in [0, 1]",
                    "reject the recommendation artifact and re-classify",
                    resolution=CONTESTED))
            missing = [f for f in PROVENANCE_FIELDS if not provenance.get(f)]
            if not isinstance(provenance.get("evidence_refs"), list):
                missing.append("evidence_refs")
            prompt_contract_version = provenance.get("prompt_contract_version")
            if (isinstance(prompt_contract_version, bool)
                    or not isinstance(prompt_contract_version, int)
                    or prompt_contract_version < 1):
                missing.append("prompt_contract_version")
            if missing:
                findings.append(_finding(
                    "provenance", ERROR, repo, path,
                    f"{facet} facet provenance is incomplete (missing "
                    f"{', '.join(missing)})",
                    "reject the recommendation artifact and re-classify",
                    resolution=CONTESTED))
    return findings


# --- override-standing ---------------------------------------------------------

def _owning_authority(repo: str) -> str:
    """Disposition authority follows content ownership — the same
    convention ``semantic.assign_disposer`` uses for contested semantic
    findings: the neutral ratify gate for openXFactory, the owning
    factory's Domain Hermes otherwise."""
    return NEUTRAL_DISPOSER if repo == NEUTRAL_REPO \
        else f"{repo} authority (Domain Hermes)"


def _override_standing_findings(ctx) -> list[Finding]:
    findings = []
    for key, entry in sorted(_catalogued_key_map(ctx).items()):
        repo = entry.get("repo", key[0])
        path = _label(entry, key)
        for assignment in _facet_assignments(entry):
            if assignment.get("state") not in ("reviewed", "overridden"):
                continue
            # The template's per-assignment `review` block records the
            # disposition; its `authority` must hold ownership standing
            # (contract: aggregation-side edits or actors without
            # standing MUST NOT create reviewed/overridden state).
            review = assignment.get("review") or {}
            authority = review.get("authority")
            if authority != _owning_authority(repo):
                findings.append(_finding(
                    "override-standing", ERROR, repo, path,
                    f"{assignment.get('facet')} facet "
                    f"{assignment['state']} by {authority!r}, "
                    "which does not hold ownership standing for this "
                    "repository",
                    "record the review under the owning authority",
                    resolution=CONTESTED))
    return findings


# --- immutable-path -------------------------------------------------------------

def _is_recognized_run_path(rest: tuple) -> bool:
    if not rest:
        return False
    if rest[0] == ".sequence":
        return (len(rest) == 2 and rest[1].endswith(".yaml")
                and rest[1][:-len(".yaml")].isdigit())
    if not _DATE_RE.match(rest[0]) or len(rest) < 3:
        return False
    run_id, tail = rest[1], rest[2:]
    if not run_id or run_id.startswith("."):
        return False
    if tail == (catalog.RUN_META_NAME,):
        return True
    return bool(tail) and tail[-1].endswith(".yaml") and all(
        seg and not seg.startswith(".") for seg in tail)


def _is_recognized_baseline_path(rest: tuple) -> bool:
    if not rest:
        return False
    if rest[0] == "shards":
        tail = rest[1:]
        return (len(tail) >= 2 and tail[-1].endswith(".yaml")
                and tail[-1][:-len(".yaml")].isdigit()
                and all(seg and not seg.startswith(".") for seg in tail[:-1]))
    if len(rest) == 1:
        name = rest[0]
        return (name in (catalog_baseline.MERGED_NAME,
                        catalog_baseline.MARKER_NAME)
                or (name.startswith("merged.") and name.endswith(".yaml")))
    return False


def _is_recognized_recommendation_path(rest: tuple) -> bool:
    # Forward-declared per data-model.md; the cataloger worker that
    # writes here is a later feature phase, but this check must not
    # flag its output as misplaced once it lands.
    return (len(rest) == 2 and bool(_DATE_RE.match(rest[0]))
            and rest[1].endswith(".yaml") and not rest[1].startswith("."))


def _is_recognized_catalog_path(parts: tuple) -> bool:
    if not parts:
        return False
    top, rest = parts[0], parts[1:]
    if top == "runs":
        return _is_recognized_run_path(rest)
    if top == "baseline":
        return _is_recognized_baseline_path(rest)
    if top == "recommendations":
        return _is_recognized_recommendation_path(rest)
    return False


def _immutable_path_findings(ctx) -> list[Finding]:
    root = Path(ctx.catalog_root) / catalog.CATALOG_DIR
    if not root.is_dir():
        return []
    findings = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if not _is_recognized_catalog_path(rel.parts):
            findings.append(_finding(
                "immutable-path", ERROR, "(catalog)", rel.as_posix(),
                "artifact does not conform to the recognized catalog "
                "run/baseline/recommendation layout",
                "move or remove the misplaced catalog artifact"))
    return findings


# --- recursion -------------------------------------------------------------

def _recursion_findings(ctx) -> list[Finding]:
    findings = []
    for entry in _all_raw_persisted_entries(ctx):
        path = entry.get("path")
        if path and inventory.is_generated_catalog_path(path):
            findings.append(_finding(
                "recursion", ERROR, entry.get("repo", "(unknown)"), path,
                "generated catalog record entered the catalog itself",
                "exclude health/document-catalog/ from corpus discovery "
                "and regenerate the snapshot"))
    return findings


# --- pending-aging --------------------------------------------------------------

def _parse_state_since(value):
    """Parse a persisted facet ``state_since`` (snapshot schema
    ``state_since: {format: date}``) to a ``date``, or ``None`` when the
    persisted value is malformed. Persisted catalog data is untrusted — a
    bad merge, hand-edit, or foreign artifact can carry any bytes (e.g.
    ``"2026-13-99"``, whose digit shape passes ``_DATE_RE`` but is not a
    real date) — and this family's contract is to REPORT malformed data
    as a finding, never crash the whole doc-health run on a
    ``ValueError`` out of ``date.fromisoformat`` (Copilot #2)."""
    if not (isinstance(value, str) and _DATE_RE.match(value)):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _pending_aging_findings(ctx) -> list[Finding]:
    warn = ctx.thresholds.get("document_catalog_pending_warning_days",
                              PENDING_WARNING_DAYS_DEFAULT)
    err = ctx.thresholds.get("document_catalog_pending_error_days",
                             PENDING_ERROR_DAYS_DEFAULT)
    findings = []
    for key, entry in sorted(_catalogued_key_map(ctx).items()):
        repo = entry.get("repo", key[0])
        path = _label(entry, key)
        for assignment in _facet_assignments(entry):
            if assignment.get("state") != "pending":
                continue
            since = assignment.get("state_since")
            if not since:
                continue
            facet = assignment.get("facet")
            since_date = _parse_state_since(since)
            if since_date is None:
                # Malformed persisted state_since: report it as a shape
                # defect instead of crashing the family (and every other
                # family after it) on an unparseable date.
                findings.append(_finding(
                    "taxonomy", ERROR, repo, path,
                    f"{facet} facet state_since {since!r} is not a valid "
                    "YYYY-MM-DD date, so its pending-aging clock cannot be "
                    "computed",
                    "regenerate the entry with a valid state_since date"))
                continue
            days = (ctx.as_of - since_date).days
            if days >= err:
                findings.append(_finding(
                    "pending-aging", ERROR, repo, path,
                    f"{facet} facet pending {days} days (error at {err})",
                    "classify or escalate the pending facet",
                    resolution=CONTESTED))
            elif days >= warn:
                findings.append(_finding(
                    "pending-aging", WARNING, repo, path,
                    f"{facet} facet pending {days} days (warning at "
                    f"{warn})",
                    "classify or escalate the pending facet",
                    resolution=CONTESTED))
    return findings


# --- entry point -----------------------------------------------------------------

def fam_document_catalog(ctx):
    root = getattr(ctx, "catalog_root", None)
    if root is None:
        return Skip(FAMILY, "no catalog root in scope for this run")
    try:
        live_entries = _live_mechanical_entries(ctx)
        findings = []
        findings += _coverage_findings(ctx, live_entries)
        findings += _stale_entry_findings(ctx, live_entries)
        findings += _duplicate_key_findings(ctx)
        findings += _artifact_type_findings(ctx)
        findings += _taxonomy_findings(ctx)
        findings += _resolution_findings(ctx)
        findings += _confidence_provenance_findings(ctx)
        findings += _override_standing_findings(ctx)
        findings += _immutable_path_findings(ctx)
        findings += _recursion_findings(ctx)
        findings += _pending_aging_findings(ctx)
        return findings
    except catalog.CatalogError as exc:
        # A corrupt/torn/foreign persisted catalog artifact (unparseable
        # or wrong-shape run.yaml, snapshot, baseline shard, marker, or
        # merged fold) surfaces from the load helpers as a controlled
        # CatalogError. This family exists to SURFACE catalog-integrity
        # problems, so it reports the corruption as a finding rather than
        # letting the exception abort the whole 13-family doc-health run
        # (run_suite has no per-family guard). The tool only ever writes
        # atomically, so it never self-produces such an artifact.
        return [_finding(
            "catalog-integrity", ERROR, "(catalog)", "(persisted state)",
            f"persisted catalog state could not be read: {exc}",
            "repair or remove the corrupt catalog artifact and re-run the "
            "mechanical catalog pass")]
