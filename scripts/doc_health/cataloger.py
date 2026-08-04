"""Bounded, non-mutating document-cataloger worker module (US4/US5;
feature tasks T016-T023).

Realizes the openxFactory `add-document-cataloging` contract's "Bounded
cataloger execution and protected evidence" requirement's deterministic
half: a versioned prompt contract (`cataloger-prompt.md`), a
change-driven selector, a bounded shard builder with protected-content
filtering applied BEFORE dispatch, a neutral job envelope, and a
whole-artifact output validator — the same envelope/validator split
`semantic.py` proved for the sibling analysis worker (research D7).

Owner dispositions and content/taxonomy/prompt invalidation (US5,
feature tasks T021/T022) are realized by `apply_dispositions` and
`invalidate` below: authority-checked reviewed/overridden decisions
that apply only through a snapshot merge (never in place), and the
carry-forward/invalidation rule research D8 derives from the
contract's "Full baseline and incremental refresh" requirement — a
content, taxonomy, or prompt-contract change returns affected facets
to `pending` and resets their `state_since` for the new semantic
input, recording a `pending` -> `pending` invalidation event when a
facet was already pending.

Non-mutation and isolation (FR-013): nothing in this module ever writes
outside `health/document-catalog/recommendations/`; a worker failure or
invalid output is always the CALLER's concern to record as a skip
(mirroring `semantic.run_sweep`) — this module raises only on
programmer error (a malformed job envelope, an invalid path), never on
untrusted worker output, which is always reported through
`enforce_contract`'s `(records, rejects)` return.

Whole-artifact rejection (spec edge case "Classifier emits partially
valid output"): unlike `semantic.enforce_contract`, which drops
individual malformed findings, `enforce_contract` here rejects the
ENTIRE artifact on any single defect — valid entries are never rescued
from an invalid one (data-model.md "Recommendation record"; contract
FR-009).

Explicit pending state (data-model.md facet state machine: `pending`
precedes any recommendation): a validated artifact may legitimately
cover only some of the six controlled facets, so the dispatch caller
MUST also merge `pending_records` for its dispatched selections —
that is what keeps a never-assigned facet visible to `select`'s
`pending` reselection class and to the deterministic family's
30/90-day pending-aging findings, and what keeps selected entries
"visibly pending" when the worker is offline or rejected.
"""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import catalog, catalog_baseline, inventory
from .semantic import NEUTRAL_DISPOSER, NEUTRAL_REPO

PROMPT_FILE = Path(__file__).parent / "cataloger-prompt.md"
PROMPT_VERSION_RE = re.compile(r"^Prompt-Contract-Version:\s*(\S+)", re.M)

DEFAULT_MODEL = "claude-sonnet-5"
DISPATCH_TIMEOUT = 1800
CLASSIFIER_VERSION = "document-cataloger/1"

# The contract's six controlled classification facets and closed
# vocabularies (document_catalog.py's own copy, kept independently here
# — cataloger.py validates classifier OUTPUT before persistence;
# document_catalog.py validates persisted entries after the fact; the
# two never import each other's constants so neither module's checks
# depend on the other's module boundary).
FACET_NAMES = ("factory_scope", "domain_contexts", "capability_refs",
               "topic_tags", "document_role", "sensitivity_signal")
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
CONFIDENCE_RANGE = (0.0, 1.0)

SELECTION_CLASSES = (
    "baseline", "new", "changed", "missing", "pending", "stale")

RECOMMENDATIONS_DIR = catalog.CATALOG_DIR / "recommendations"
RECOMMENDATION_KIND = "xfactory_document_catalog_recommendation"

# The effective-taxonomy digest pattern the contract fixes for every
# inferred facet's provenance (openxFactory
# `xfactory-document-catalog-snapshot.schema.yaml` #/$defs/provenance:
# `taxonomy_sha256: {pattern: "^[0-9a-f]{64}$"}`).
_TAXONOMY_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


def _valid_evidence_ref(ref) -> bool:
    """True when one provenance ``evidence_refs`` element satisfies the
    contract evidence-reference shape (snapshot schema #/$defs/evidence_ref
    ``oneOf``: a non-empty string, OR a ``{repo, path}`` mapping of
    non-empty strings and no other keys). A worker-emitted evidence
    reference of any other shape (an empty string, a partial or
    over-populated mapping, a non-string/non-object) would persist a
    schema-invalid recommendation record and is rejected whole by
    ``enforce_contract``."""
    if isinstance(ref, bool):
        return False
    if isinstance(ref, str):
        return len(ref) >= 1
    if isinstance(ref, dict):
        return (set(ref) == {"repo", "path"}
                and isinstance(ref.get("repo"), str) and bool(ref["repo"])
                and isinstance(ref.get("path"), str) and bool(ref["path"]))
    return False


# --- contract-shape coercion / validation (schema-arbiter alignment) ---------

def _prompt_contract_version(value) -> int:
    """Coerce a prompt-contract version to the integer >= 1 the contract
    provenance shape requires (openxFactory
    `xfactory-document-catalog-snapshot.schema.yaml` #/$defs/provenance:
    `prompt_contract_version: {type: integer, minimum: 1}`). The versioned
    prompt file's `Prompt-Contract-Version:` header is a regex capture
    (a string) and a hand-built envelope may carry either form; a value
    that is not an integer >= 1 is a malformed contract/envelope and
    raises rather than persisting a non-integer into provenance."""
    if isinstance(value, bool):
        raise ValueError(
            f"prompt_contract_version must be an integer >= 1: {value!r}")
    if isinstance(value, int):
        version = value
    elif isinstance(value, str) and value.strip():
        try:
            version = int(value.strip())
        except ValueError:
            raise ValueError(
                f"prompt_contract_version must be an integer >= 1: {value!r}")
    else:
        raise ValueError(
            f"prompt_contract_version must be an integer >= 1: {value!r}")
    if version < 1:
        raise ValueError(
            f"prompt_contract_version must be an integer >= 1: {value!r}")
    return version


def _require_taxonomy_digest(taxonomy_sha256) -> str:
    """The effective-taxonomy digest, validated against the contract
    pattern (schema #/$defs/provenance `taxonomy_sha256`: `^[0-9a-f]{64}$`).
    The contract requires that "Every inferred facet SHALL record the
    effective taxonomy digest" ("Controlled classification facets and
    provenance"), so a missing or malformed digest is a caller/programmer
    error and raises rather than silently persisting `null` (or a
    non-conforming value) into provenance."""
    if not (isinstance(taxonomy_sha256, str)
            and _TAXONOMY_DIGEST_RE.match(taxonomy_sha256)):
        raise ValueError(
            "taxonomy_sha256 must be a 64-character lowercase hex effective "
            f"taxonomy digest: {taxonomy_sha256!r}")
    return taxonomy_sha256


def _as_of_datetime(as_of_str: str) -> str:
    """The deterministic RFC 3339 date-time a bare `YYYY-MM-DD` run date
    denotes for a transition's `occurred_at` (snapshot schema
    #/$defs/transition `occurred_at: {format: date-time}`): midnight UTC on
    that date. A facet's `state_since` stays the bare date (schema
    `state_since: {format: date}`); only transition timestamps are
    date-time. Never wall clock — derived only from the `as_of` date."""
    return f"{as_of_str}T00:00:00Z"


def _date_part(occurred_at: str) -> str:
    """The bare `YYYY-MM-DD` date portion of a disposition timestamp — the
    value a facet's `state_since` carries (snapshot schema `state_since:
    {format: date}`) even though a disposition's `occurred_at` is a full
    RFC 3339 date-time (override schema `occurred_at: {format: date-time}`)."""
    return str(occurred_at).split("T", 1)[0]


def _ensure_datetime(occurred_at: str) -> str:
    """Normalize a disposition `occurred_at` to an RFC 3339 date-time (the
    form the snapshot schema requires for #/$defs/transition and
    #/$defs/review `occurred_at`). A value already carrying a time is kept
    verbatim; a bare `YYYY-MM-DD` date is promoted to midnight UTC — the
    same deterministic convention `_as_of_datetime` applies to run dates."""
    text = str(occurred_at)
    return text if "T" in text else f"{text}T00:00:00Z"


# --- selection (T017) --------------------------------------------------------

@dataclass(frozen=True)
class Selection:
    """One document selected for semantic (re)classification
    (data-model.md "Recommendation record" target).

    ``entry`` is the full extended inventory entry (data-model.md
    "Inventory entry") for this document — inventory entries always
    carry a real ``path`` (never the mechanical catalog's opaque
    locator swap), so selection and shard-building key on ``path``
    directly and never need to resolve an opaque reference; a document
    whose handling policy prohibits path persistence is exactly the
    class of document ``build_shards`` filters out before it would
    ever need one.
    """
    repo: str
    path: str
    content_hash: str
    reason: str  # one of SELECTION_CLASSES
    entry: dict


def _facet_pending(assignments) -> bool:
    return any(isinstance(a, dict) and a.get("state") == "pending"
               for a in (assignments or []))


def _facet_incompatible(assignments, taxonomy_sha256, prompt_version) -> bool:
    """True when a recorded facet's provenance no longer matches the
    CURRENT effective taxonomy digest or prompt-contract version
    (contract "Taxonomy has a breaking change"). A facet recording no
    provenance value for one of these (e.g. a disposition-only
    ``review``-derived state) never counts as incompatible on its own —
    only a recorded, differing value does."""
    for a in assignments or []:
        if not isinstance(a, dict):
            continue
        provenance = a.get("provenance") or {}
        if taxonomy_sha256 is not None and provenance.get(
                "taxonomy_sha256") not in (None, taxonomy_sha256):
            return True
        if prompt_version is not None and provenance.get(
                "prompt_contract_version") not in (None, prompt_version):
            return True
    return False


def select(inv, previous, catalog_entries, *, current_taxonomy_sha256=None,
          current_prompt_version=None) -> list[Selection]:
    """Deterministic, change-driven selection for semantic classification
    (contract "Full baseline and incremental refresh"; FR-014).

    - ``inv``: the current extended inventory (data-model.md).
    - ``previous``: the prior inventory, or ``None`` when no previous
      mechanical run exists — every current entry is then eligible for
      the new/changed checks (mirrors ``semantic.select_corpus``'s
      "no previous inventory" full-sweep branch).
    - ``catalog_entries``: the CURRENT catalog's entries (baseline plus
      latest incremental run — whatever a caller has already merged),
      or empty/``None`` when nothing has ever been classified. Entries
      keyed by the mechanical catalog's opaque locator (handling policy
      prohibits path persistence) are invisible to this plain-path
      lookup by construction — exactly the documents ``build_shards``
      would filter out before dispatch regardless of their selection
      reason.
    - ``current_taxonomy_sha256``/``current_prompt_version``: when
      supplied, a facet recorded against a DIFFERENT taxonomy digest or
      prompt-contract version is ``stale`` (reclassify); omitting them
      (the default) skips that check rather than falsely flagging
      every facet stale before any taxonomy/prompt baseline exists.

    Exactly one reason is assigned per selected document, in priority
    order ``baseline > new > changed > missing > pending > stale``; an
    unchanged, fully classified, taxonomy/prompt-compatible document is
    not selected at all (SC-004: zero selection on an unchanged
    corpus). A facet counts as ``pending`` only through an EXPLICIT
    ``state: pending`` assignment item — the dispatch flow records one
    for every dispatched-but-unresolved facet (``pending_records``), so
    partial worker coverage stays reselectable here instead of
    silently settling. Never mutates any input.
    """
    catalog_map = {(e.get("repo"), e.get("path")): e
                  for e in (catalog_entries or []) if e.get("path") is not None}
    baseline_mode = not catalog_map
    if previous is None:
        changed_keys = {(e["repo"], e["path"]) for e in inv}
    else:
        changed_keys = inventory.changed_paths(inv, previous)

    selections = []
    for entry in inv:
        path = entry.get("path")
        if path and inventory.is_generated_catalog_path(path):
            continue
        key = (entry["repo"], path)
        cat_entry = catalog_map.get(key)
        reason = None
        if baseline_mode:
            reason = "baseline"
        elif cat_entry is None:
            reason = "new"
        elif key in changed_keys and \
                cat_entry.get("content_hash") != entry.get("content_hash"):
            reason = "changed"
        elif not cat_entry.get("facet_assignments"):
            reason = "missing"
        elif _facet_pending(cat_entry.get("facet_assignments")):
            reason = "pending"
        elif _facet_incompatible(cat_entry.get("facet_assignments"),
                                 current_taxonomy_sha256,
                                 current_prompt_version):
            reason = "stale"
        if reason is None:
            continue
        selections.append(Selection(
            repo=entry["repo"], path=path, content_hash=entry["content_hash"],
            reason=reason, entry=dict(entry)))
    selections.sort(key=lambda s: (s.repo, s.path))
    return selections


# --- bounded shards with protected filtering (T017) --------------------------

@dataclass(frozen=True)
class Shard:
    """A bounded, self-contained group of selections ready for dispatch
    (module-interfaces.md ``build_shards``). Protected-filtering has
    already happened by the time a ``Shard`` exists — nothing in it
    needs a second policy check before being handed to the worker."""
    shard_id: str
    selections: tuple


def is_protected(entry: dict) -> bool:
    """Fail-closed protected-content filter (contract "Bounded
    cataloger execution and protected evidence": the worker MUST NOT
    receive a document's content or identifying metadata unless the
    host attests the required tenant/data-boundary and handling
    authorization — attestation this engineering slice does not yet
    wire, per the feature's Assumptions). A source-declared ``protected``
    handling (data-model.md "Inventory entry"; test_catalog.py's
    ``prohibit_protected`` precedent) is never dispatched."""
    return entry.get("handling") == "protected"


def _has_declared_handling(entry: dict) -> bool:
    """True for ANY source-declared handling annotation, not just
    ``protected`` — the broader set contract scenario "Sensitivity
    inference lowers caution" guards: a document need not be fully
    ``protected`` (and therefore filtered from dispatch entirely by
    ``is_protected``) for the classifier to still be barred from
    claiming it is LESS restricted than source policy already
    declares."""
    return bool(entry.get("handling"))


def build_shards(selections, budget) -> list[Shard]:
    """Bounded, deterministically ordered, protected-filtered shards.

    Protected filtering happens HERE, before anything is bundled for
    dispatch (module-interfaces.md: "protected filtering applied
    before dispatch") — a protected selection never enters any shard,
    so it can never reach ``envelope``/``enforce_contract`` or leave
    this process's memory. ``budget`` bounds each shard's entry count
    (mirrors ``catalog_baseline.run_shard``'s budget semantics).
    """
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
        raise ValueError(f"shard budget must be a positive int: {budget!r}")
    eligible = sorted((s for s in selections if not is_protected(s.entry)),
                      key=lambda s: (s.repo, s.path))
    shards = []
    for i in range(0, len(eligible), budget):
        batch = tuple(eligible[i:i + budget])
        keys = "|".join(f"{s.repo}:{s.path}:{s.content_hash}" for s in batch)
        shard_id = "CATSHARD-{:04d}-{}".format(
            i // budget, hashlib.sha256(keys.encode()).hexdigest()[:10])
        shards.append(Shard(shard_id=shard_id, selections=batch))
    return shards


# --- prompt contract (T016 load path) ----------------------------------------

def load_prompt_contract() -> tuple[int, str]:
    """Load the versioned cataloger prompt contract, returning
    ``(prompt_contract_version, text)``. The version is coerced to the
    integer >= 1 the contract provenance shape requires
    (``_prompt_contract_version``); a non-integer ``Prompt-Contract-Version``
    in the prompt file is a malformed contract and raises."""
    text = PROMPT_FILE.read_text(encoding="utf-8")
    m = PROMPT_VERSION_RE.search(text)
    if not m:
        raise ValueError("cataloger-prompt.md missing Prompt-Contract-Version")
    return _prompt_contract_version(m.group(1)), text


# --- job envelope (T018) ------------------------------------------------------

def envelope(as_of: date, model: str, prompt_version, shard: Shard,
            taxonomy_sha256: str) -> dict:
    """Neutral Hermes job envelope for one shard's classification
    dispatch (contract "Bounded cataloger execution and protected
    evidence": a distinct, bounded, read-only ``document-cataloger``
    Omnigent job, no repository credentials, no write authority — the
    same envelope shape ``semantic.envelope`` uses for the sibling
    analysis worker, with a distinct job type and worker profile so
    this is never mistaken for a third doc-health semantic finding
    family). The id is deterministic over (date, model, prompt
    version, shard) — never wall clock — so a same-day rerun of the
    identical shard references the same job.

    ``taxonomy_sha256`` is REQUIRED and validated against the contract
    digest pattern (``_require_taxonomy_digest``): the contract requires
    every inferred facet to record the effective taxonomy digest, and
    ``enforce_contract`` copies this value straight into each accepted
    facet's provenance, so a missing or malformed digest must raise here
    rather than persist a ``null``/invalid ``taxonomy_sha256``.
    ``prompt_version`` is coerced to the contract's integer form
    (``_prompt_contract_version``) so the persisted provenance carries an
    integer, never the prompt file's raw string capture."""
    digest = _require_taxonomy_digest(taxonomy_sha256)
    prompt_version = _prompt_contract_version(prompt_version)
    seed = f"{as_of.isoformat()}|{model}|{prompt_version}|{shard.shard_id}"
    job_id = "CATJOB-" + hashlib.sha256(seed.encode()).hexdigest()[:12]
    return {"job": {
        "id": job_id,
        "schema_version": 1,
        "issued_by": "Hermes",
        "job_type": "document_cataloger",
        "domain": "codex",
        "project": "xfactory-doc-health",
        "orchestrator": "doc-health-runner",
        "routing_policy": "single_bounded_worker",
        "auth_profile": "read_only_no_credentials",
        "worker_selector": {"profile": "document-cataloger",
                            "model": model,
                            "prompt_contract_version": prompt_version},
        "allowed_phase": "classification",
        "approval_policy": "report_only_v1",
        "required_outputs": ["catalog_recommendation_artifact"],
        "traceability": {"capability": "document-catalog",
                         "shard_id": shard.shard_id,
                         "shard_size": len(shard.selections),
                         "as_of": as_of.isoformat(),
                         "taxonomy_sha256": digest},
        "stop_conditions": {"timeout_seconds": DISPATCH_TIMEOUT,
                            "max_repo_writes": 0},
    }}


# --- whole-artifact output validation (T018) ---------------------------------

# The versioned namespaced tag registries the merged topic-tag
# vocabulary is read from: the same registry-file convention and
# minimal regex parse the document-catalog family uses
# (``document_catalog._controlled_tag_ids``; ``catalog.registry_input``
# precedent — no YAML dependency). The constants are this module's own
# copy, per the CLOSED_VOCABULARIES note above.
TAG_REGISTRY_FILENAME = "document-tag-registry.yaml"
_TAG_ID_RE = re.compile(r"^\s*-\s*id:\s*(\S+)\s*$", re.MULTILINE)


def registered_tag_ids(repo_paths) -> frozenset:
    """The merged controlled topic-tag vocabulary: every tag id declared
    by a ``document-tag-registry.yaml`` under any governed repository in
    scope (``repo_paths``: ``{repo: checkout path}``), deterministically
    merged across registries. A pure function of explicit paths — no
    runner ``Context`` — so the dispatch caller can hand
    ``enforce_contract`` the same registry authority the deterministic
    family validates persisted entries against. Generated catalog
    output is excluded so the catalog can never register tags for
    itself."""
    ids = set()
    for repo in sorted(repo_paths):
        repo_path = Path(repo_paths[repo])
        for reg in sorted(repo_path.rglob(TAG_REGISTRY_FILENAME)):
            rel = reg.relative_to(repo_path).as_posix()
            if inventory.is_generated_catalog_path(rel):
                continue
            ids.update(_TAG_ID_RE.findall(reg.read_text(encoding="utf-8")))
    return frozenset(ids)


def _job_field(job: dict, *path):
    node = job
    for key in path:
        if not isinstance(node, dict) or key not in node:
            raise ValueError(
                f"job envelope is missing required field: {'.'.join(map(str, path))}")
        node = node[key]
    return node


def enforce_contract(raw_output, shard: Shard, job: dict,
                     registered_tags=None) -> tuple[list[dict], list[str]]:
    """Validate the worker's raw structured output against the
    cataloger output contract (FR-009; contract "Controlled
    classification facets and provenance" + "Sensitivity inference
    lowers caution"; ``cataloger-prompt.md``'s "Hard prohibitions").

    Rejection is WHOLE-ARTIFACT (spec edge case "Classifier emits
    partially valid output"): any single defect anywhere in the raw
    output voids the entire artifact — valid entries are never rescued
    from an invalid one. A second entry for the same ``(repo, path)``
    within one artifact is itself a defect: conflicting records for one
    document must never leave validation to race a downstream merge.
    Returns ``(records, rejects)``: on success, ``records`` are
    complete per-document recommendation dicts (the contract
    facet-assignment shape, ready for ``persist_recommendations``) and
    ``rejects`` is empty; on rejection, ``records`` is ``[]`` and
    ``rejects`` names every violation found (never just the first).

    ``registered_tags`` is the merged controlled topic-tag vocabulary
    (``registered_tag_ids``' return value): an effective ``topic_tags``
    value absent from it rejects the artifact whole — an unregistered
    tag may travel only as a PROPOSED tag in ``proposed_values``,
    never as an effective suggestion (contract scenario "Topic tag is
    unknown"). ``None`` (no tag registry in scope for this corpus)
    skips registry resolution and keeps the shape-only validation;
    whenever the governed workspace declares registries, the dispatch
    caller MUST pass the merged vocabulary.

    ``job`` is the envelope this shard was dispatched under
    (``envelope()``'s return value) — it supplies the provenance the
    worker itself never reports (model id, prompt-contract version,
    effective taxonomy digest, classifier implementation version, and
    the dispatch date used as every accepted facet's ``state_since``).
    A malformed envelope (missing one of these) is a caller/programmer
    error and raises ``ValueError`` rather than a silent artifact
    rejection.
    """
    model = _job_field(job, "job", "worker_selector", "model")
    prompt_version = _prompt_contract_version(
        _job_field(job, "job", "worker_selector", "prompt_contract_version"))
    as_of_str = _job_field(job, "job", "traceability", "as_of")
    # A malformed envelope (missing or non-conforming digest) is a
    # caller/programmer error and raises here, so an accepted facet's
    # provenance can never carry a null/invalid effective taxonomy digest.
    taxonomy_sha256 = _require_taxonomy_digest(
        _job_field(job, "job", "traceability", "taxonomy_sha256"))

    rejects = []
    if not isinstance(raw_output, dict) or not isinstance(
            raw_output.get("entries"), list):
        return [], ["worker output is not an object with an entries array"]

    by_key = {(s.repo, s.path): s for s in shard.selections}
    records = []
    seen_documents = set()
    for i, raw in enumerate(raw_output["entries"]):
        prefix = f"entry {i}"
        if not isinstance(raw, dict):
            rejects.append(f"{prefix}: not an object")
            continue
        repo, path = raw.get("repo"), raw.get("path")
        # Prompt contract v3: the worker no longer echoes `content_hash`.
        # A worker echo carried no integrity — every entry is matched to
        # its shard selection by (repo, path) below, and the shard's own
        # `selection.content_hash` (the authoritative dispatched-corpus
        # value) is what persists. Echoing a machine-precision identifier
        # only invited transcription drift: live run 29349336374 / child
        # 29349393119 classified all 25 shard documents correctly but
        # entry 23 dropped a single hex character from the 64-char hash it
        # echoed (...184c45095009cb1a vs ...184c95009cb1a, 63 chars), and
        # the v2 validator rejected the whole 24-of-25-correct artifact. A
        # worker-supplied `content_hash` is now an unread key like any
        # other (ignored, never validated, never persisted).
        if not (isinstance(repo, str) and repo
                and isinstance(path, str) and path):
            # Guard BEFORE any (repo, path) keying: a malformed worker
            # may return non-string (even non-hashable) values here, and
            # untrusted output must reject, never raise (module
            # docstring invariant). A shard key is always a string
            # pair, so a non-string value could never match anyway.
            rejects.append(
                f"{prefix}: repo/path are not non-empty strings: "
                f"{repo!r}:{path!r}")
            continue
        if (repo, path) in seen_documents:
            rejects.append(
                f"{prefix}: duplicate entry for {repo}:{path} in one "
                "artifact (conflicting records must never race a "
                "downstream merge)")
            continue
        seen_documents.add((repo, path))
        selection = by_key.get((repo, path))
        if selection is None:
            rejects.append(
                f"{prefix}: {repo}:{path} is not in the dispatched shard")
            continue
        assignments_raw = raw.get("facet_assignments")
        if not isinstance(assignments_raw, list) or not assignments_raw:
            rejects.append(
                f"{prefix}: {repo}:{path} has no facet_assignments")
            continue
        handled = _has_declared_handling(selection.entry)
        assignments, seen_facets = [], set()
        for j, item in enumerate(assignments_raw):
            where = f"{prefix} facet {j}"
            if not isinstance(item, dict):
                rejects.append(f"{where}: not an object")
                continue
            facet = item.get("facet")
            if facet not in FACET_NAMES:
                rejects.append(
                    f"{where}: unknown or invented facet {facet!r}")
                continue
            if facet in seen_facets:
                rejects.append(
                    f"{where}: facet {facet!r} assigned more than once")
                continue
            values = item.get("values")
            if not isinstance(values, list) or not values:
                rejects.append(f"{where}: {facet} has no values")
                continue
            vocabulary = CLOSED_VOCABULARIES.get(facet)
            if vocabulary is not None:
                invented = [v for v in values if v not in vocabulary]
                if invented:
                    rejects.append(
                        f"{where}: {facet} has invented value(s) outside "
                        f"the contract vocabulary: {invented!r}")
                    continue
            if facet == "sensitivity_signal" and handled \
                    and "unspecified" in values:
                rejects.append(
                    f"{where}: sensitivity_signal attempts to lower "
                    f"caution below source-declared handling for "
                    f"{repo}:{path}")
                continue
            if facet == "capability_refs":
                bad = [v for v in values if not (
                    isinstance(v, dict) and v.get("repository")
                    and v.get("capability"))]
                if bad:
                    rejects.append(
                        f"{where}: capability_refs value(s) do not name a "
                        f"{{repository, capability}} pair: {bad!r}")
                    continue
            if facet in ("domain_contexts", "topic_tags"):
                bad = [v for v in values
                      if not (isinstance(v, str) and v.strip())]
                if bad:
                    rejects.append(
                        f"{where}: {facet} value(s) are not non-empty "
                        f"strings: {bad!r}")
                    continue
            if facet == "topic_tags" and registered_tags is not None:
                unresolved = sorted(
                    v for v in values if v not in registered_tags)
                if unresolved:
                    rejects.append(
                        f"{where}: topic_tags value(s) do not resolve in "
                        f"the merged tag registries (an unregistered tag "
                        f"may only be proposed, never effective): "
                        f"{unresolved!r}")
                    continue
            confidence = item.get("confidence")
            lo, hi = CONFIDENCE_RANGE
            if (isinstance(confidence, bool)
                    or not isinstance(confidence, (int, float))
                    or not (lo <= confidence <= hi)):
                rejects.append(
                    f"{where}: confidence {confidence!r} is not numeric "
                    "in [0, 1]")
                continue
            section = item.get("section")
            # Prompt contract v2: the worker returns the grounding PASSAGE
            # verbatim, NOT a hash. The cataloger child runs tool-less and
            # single-turn (`claude -p --tools "" --max-turns 1`), so it
            # cannot compute SHA-256; on the first live run it rationally
            # returned empty entries rather than fabricate one (runs
            # 29344503264 / 29344452894). Orchestration computes the digest
            # here — the same worker-returns-text / orchestration-hashes
            # seam `semantic.py` already proved for the sibling analysis
            # worker (`semantic.passage_id`). A worker-supplied
            # `passage_sha256` (a v1 leftover, or any other unread key) is
            # IGNORED, never persisted and never rejected: this validator
            # reads only the keys it needs and has never rejected
            # unexpected per-assignment keys, so the COMPUTED digest — never
            # a worker-copied (fabricatable, meaningless) one — is what
            # lands in provenance.
            #
            # Protected content: the passage is raw document text, but no
            # new leakage surface is introduced. `build_shards` filters
            # protected documents (`is_protected`) out BEFORE dispatch, so
            # a protected document's content — and therefore its passage —
            # never reaches the worker at all; for a dispatched document
            # the full content already traveled outbound in the shard
            # bundle, and the returning passage is consumed for hashing
            # only (never written into the persisted record — the schema
            # provenance has no `passage` field, only `passage_sha256`),
            # so it is dropped the moment the digest is taken.
            passage = item.get("passage")
            if not (isinstance(section, str) and section.strip()):
                rejects.append(f"{where}: missing section evidence")
                continue
            if not (isinstance(passage, str) and passage.strip()):
                rejects.append(f"{where}: missing passage evidence")
                continue
            # Normalize EXACTLY as `semantic.passage_id` does
            # (`" ".join(passage.split())`: collapse every whitespace run —
            # spaces, tabs, newlines — to a single space and strip the
            # ends) so the two doc-health lanes derive byte-identical
            # digests from the same passage. The schema fixes
            # provenance.passage_sha256 as a 64-char lowercase hex digest
            # (snapshot schema #/$defs/provenance `passage_sha256:
            # {pattern: "^[0-9a-f]{64}$"}`), which hexdigest() satisfies by
            # construction.
            passage_sha256 = hashlib.sha256(
                " ".join(passage.split()).encode()).hexdigest()
            evidence_refs = item.get("evidence_refs", [])
            if not isinstance(evidence_refs, list):
                rejects.append(f"{where}: evidence_refs must be a list")
                continue
            bad_refs = [r for r in evidence_refs if not _valid_evidence_ref(r)]
            if bad_refs:
                # Each element must satisfy the contract evidence_ref
                # shape (snapshot schema #/$defs/evidence_ref oneOf: a
                # non-empty string, or a {repo, path} mapping of non-empty
                # strings and no other keys); anything else persists a
                # schema-invalid record.
                rejects.append(
                    f"{where}: evidence_refs element(s) are not a non-empty "
                    f"string or a {{repo, path}} mapping: {bad_refs!r}")
                continue
            seen_facets.add(facet)
            proposed = item.get("proposed_values") or []
            if not isinstance(proposed, list):
                rejects.append(f"{where}: proposed_values must be a list")
                continue
            assignments.append({
                "facet": facet,
                "values": list(values),
                "proposed_values": list(proposed),
                "state": "suggested",
                "state_since": as_of_str,
                "provenance": {
                    "taxonomy_sha256": taxonomy_sha256,
                    "method": "classifier",
                    "classifier_version": CLASSIFIER_VERSION,
                    "model": model,
                    "prompt_contract_version": prompt_version,
                    "confidence": confidence,
                    "section": section,
                    "passage_sha256": passage_sha256,
                    "evidence_refs": list(evidence_refs),
                },
                "transitions": [{"from": "pending", "to": "suggested",
                                 "occurred_at": _as_of_datetime(as_of_str),
                                 "evidence_refs": []}],
                "review": None,
            })
        if not assignments:
            rejects.append(
                f"{prefix}: {repo}:{path} has no valid facet_assignments")
            continue
        records.append({
            # The persisted record shape is unchanged — it still carries a
            # `content_hash` — but its SOURCE is now the matched shard
            # selection (the authoritative dispatched-corpus value), never
            # a worker echo. merge_recommendations still discards a record
            # whose hash mismatches the live entry, so merge-time staleness
            # stays independently guarded.
            "repo": repo, "path": path,
            "content_hash": selection.content_hash,
            "facet_assignments": sorted(assignments,
                                        key=lambda a: a["facet"]),
        })
    if rejects:
        return [], rejects  # whole-artifact rejection: nothing is rescued
    return records, []


# --- explicit pending / policy-blocked marking for never-assigned facets ------

# Domain separator for deterministic opaque blocker references
# (contract "Host is not authorized for protected content": the facets
# of a never-dispatched protected document are recorded
# ``policy_blocked`` with an opaque blocker reference, never ordinary
# ``pending``). The reference is derived ONLY from the blocking policy
# class and the document's already-opaque US1 locator
# (``catalog.opaque_locator``'s ``document_ref``), so it can never
# reveal identifying metadata the locator itself does not.
_BLOCKER_REF_DOMAIN = "xfactory-cataloger-policy-blocker"
PROTECTED_HANDLING_BLOCKER = "protected_handling"

# The source-policy evidence reference and reason code a policy-blocked
# dispatch decision records (handling-gate schema #/$defs/dispatch_decision
# `source_policy_ref`; #/$defs/blocker_reference `reason_code`). This
# engineering slice does not yet wire real host attestation (the feature's
# Assumptions), so the defense-in-depth block that bars a protected
# document from dispatch cites the source-declared handling annotation that
# triggered it — a deterministic, non-identifying reference — under the
# "Host is not authorized for protected content" reason class.
PROTECTED_HANDLING_SOURCE_POLICY_REF = "source-declared-handling:protected"
PROTECTED_HANDLING_REASON_CODE = "handling_authorization_missing"


def blocker_reference(document_ref: str, policy_class: str) -> str:
    """Deterministic opaque blocker reference for one policy-blocked
    document: stable across runs (so diffs and carry-forward key
    correctly, mirroring ``catalog.opaque_locator``'s stability) and
    opaque by construction — a domain-separated hash over the blocking
    policy class and the opaque ``document_ref``, never over the path
    or any other identifying metadata. Returned as the 64-character
    lowercase hex digest the contract fixes for a blocked document's
    blocker reference (openxFactory
    `xfactory-document-opaque-locator.schema.yaml` #/$defs/blocker_reference:
    `blocker_ref: {pattern: "^[0-9a-f]{64}$"}`)."""
    seed = f"{_BLOCKER_REF_DOMAIN}\n{policy_class}\n{document_ref}\n"
    return hashlib.sha256(seed.encode()).hexdigest()


def blocked_dispatch_policy(document_ref: str) -> dict:
    """The entry-level dispatch/handling-gate decision recorded for a
    never-dispatched protected document (snapshot schema #/$defs/entry
    ``dispatch_policy`` -> handling-gate #/$defs/dispatch_decision:
    ``state: blocked``, a ``source_policy_ref``, and the opaque
    ``blocked_reference``). Dispatch is a per-DOCUMENT gate, so the
    blocker reference lives HERE — on the entry's single decision — never
    on a ``facet_assignment`` (the snapshot facet_assignment shape is
    ``additionalProperties: false`` and carries no blocker field; a
    ``policy_blocked`` facet cites this decision's ``blocked_reference``
    instead)."""
    return {
        "state": "blocked",
        "source_policy_ref": PROTECTED_HANDLING_SOURCE_POLICY_REF,
        "blocked_reference": {
            "blocker_ref": blocker_reference(
                document_ref, PROTECTED_HANDLING_BLOCKER),
            "reason_code": PROTECTED_HANDLING_REASON_CODE,
        },
    }


def pending_records(selections, catalog_entries, as_of) -> list[dict]:
    """Explicit ``pending``-state recommendation records for every
    selected document's NEVER-ASSIGNED controlled facets (data-model.md
    facet state machine: ``pending`` precedes any recommendation;
    contract "Classifier is unavailable": selected entries MUST remain
    visibly pending).

    ``cataloger-prompt.md`` sanctions partial coverage ("as many of the
    six controlled facets as the content supports"), so a validated
    artifact routinely leaves some facets with no assignment item at
    all — and a facet with no item is invisible to ``select()``'s
    ``pending`` reselection class and to the deterministic family's
    pending-aging findings (both key on an explicit ``state:
    pending``). The dispatch caller therefore merges these records
    (``catalog.merge_recommendations``) alongside the validated ones —
    or alone, when the worker is offline or its output was rejected —
    so every selected-but-unresolved facet lands in the next snapshot
    in an explicit ``pending`` state with ``state_since`` starting its
    30/90-day aging clock (research D8).

    Only never-assigned facets are marked. A facet already carrying ANY
    assignment item is left alone: an already-``pending`` facet must
    keep its original ``state_since`` (the contract's carry-forward
    rule — re-marking would reset the aging clock every run), and a
    suggested/reviewed/overridden facet may return to ``pending`` only
    through content/taxonomy/prompt invalidation (``invalidate``,
    feature task T022, not this function). For the facets the worker
    DID cover in the same dispatch, merge precedence guarantees the
    validated suggestion always beats this marker (equal
    ``state_since``; a pending marker has no provenance confidence).

    Defense in depth for protected content (contract "Bounded cataloger
    execution and protected evidence", scenario "Host is not authorized
    for protected content"): this function applies the
    protected-handling policy ITSELF instead of trusting its caller to
    pre-filter. On the offline/skip path ("Cataloger is offline") the
    caller operates on raw ``select()`` output — no shard is ever
    built, so ``build_shards``'s protected filter never runs — and a
    protected selection (``is_protected``) must never surface as
    ordinary ``pending``: its never-assigned facets are recorded
    ``policy_blocked``, and the deterministic opaque blocker reference is
    carried on an entry-level ``dispatch_policy`` handling-gate decision
    (``blocked_dispatch_policy``), NEVER on a facet_assignment — the
    snapshot facet_assignment shape forbids a blocker field, and dispatch
    is a per-document gate (a ``policy_blocked`` facet cites the entry's
    one ``dispatch_policy.blocked_reference``). The record also carries
    the US1 opaque locator (``catalog.opaque_locator``: ``document_ref``
    + ``path_sha256``) in place of the real path, so no identifying
    metadata can reach ``persist_recommendations`` or a later merge.
    The carry-forward rule applies identically: a facet already
    recorded ``policy_blocked`` under the opaque locator key is never
    re-marked. ``policy_blocked`` facets never enter the 30/90-day
    aging clocks (the deterministic family keys on explicit ``pending``
    state only).

    ``selections`` are the documents the caller selected for dispatch —
    dispatched ``build_shards`` output, or raw ``select()`` output on
    the offline/skip path; ``catalog_entries`` is the same
    current-catalog input ``select`` reads. Pure and deterministic:
    records sorted by ``(repo, path)``, facets sorted within each
    record; never mutates any input; never touches disk.
    """
    as_of_str = catalog._as_of_str(as_of)
    assigned = {}
    for entry in catalog_entries or []:
        try:
            key = catalog._entry_key(entry)
        except (KeyError, ValueError):
            continue  # unkeyable row: nothing to carry forward from
        assigned[key] = {
            a.get("facet") for a in entry.get("facet_assignments") or []
            if isinstance(a, dict)}
    records = []
    for sel in sorted(selections, key=lambda s: (s.repo, s.path)):
        protected = is_protected(sel.entry)
        locator = catalog.opaque_locator(sel.repo, sel.path) \
            if protected else None
        key = (sel.repo, locator["document_ref"]) if protected \
            else (sel.repo, sel.path)
        existing = assigned.get(key, frozenset())
        unassigned = sorted(f for f in FACET_NAMES if f not in existing)
        if not unassigned:
            continue
        if protected:
            records.append({
                "repo": sel.repo,
                "document_ref": locator["document_ref"],
                "path_sha256": locator["path_sha256"],
                "content_hash": sel.content_hash,
                # The blocker rides on the entry-level dispatch decision,
                # not on any facet (schema-forbidden there); a merge
                # carries it onto the snapshot entry (merge_recommendations).
                "dispatch_policy": blocked_dispatch_policy(
                    locator["document_ref"]),
                "facet_assignments": [{
                    "facet": facet,
                    "values": [],
                    "proposed_values": [],
                    "state": "policy_blocked",
                    "state_since": as_of_str,
                    "transitions": [],
                    "review": None,
                } for facet in unassigned],
            })
            continue
        records.append({
            "repo": sel.repo, "path": sel.path,
            "content_hash": sel.content_hash,
            "facet_assignments": [{
                "facet": facet,
                "values": [],
                "proposed_values": [],
                "state": "pending",
                "state_since": as_of_str,
                "transitions": [],
                "review": None,
            } for facet in unassigned],
        })
    return records


# --- immutable recommendation persistence (T019) -----------------------------

def _canonical_records(records) -> list[dict]:
    """Canonical, order-independent form of one job's validated
    recommendation records: entries ordered by ``(repo, path,
    content_hash)`` and each entry's ``facet_assignments`` ordered by
    facet. A retried dispatch whose worker emitted logically identical
    JSON in a different entry or assignment order therefore renders
    byte-identically and stays the documented idempotent no-op instead
    of failing closed as a phantom conflict. Never mutates the caller's
    records (new dicts and lists throughout)."""
    canonical = []
    for record in records:
        item = dict(record)
        assignments = item.get("facet_assignments")
        if isinstance(assignments, list):
            item["facet_assignments"] = sorted(
                assignments,
                key=lambda a: str(a.get("facet")) if isinstance(a, dict)
                else str(a))
        canonical.append(item)
    canonical.sort(key=lambda r: (str(r.get("repo")), str(r.get("path")),
                                  str(r.get("content_hash"))))
    return canonical


def persist_recommendations(root, as_of, job_id, records) -> Path:
    """Persist one job's validated recommendation records as ONE
    immutable artifact (data-model.md "Recommendation record"; contract
    "Bounded cataloger execution and protected evidence": "Validated
    recommendation evidence SHALL be immutable at
    health/document-catalog/recommendations/YYYY-MM-DD/<job-id>.yaml
    with status: record").

    Exclusive write (``catalog_baseline._write_exclusive`` precedent):
    the content lands complete in a unique per-invocation temp file,
    then a hard link publishes it — a second write for the SAME job id
    with DIFFERENT content fails closed with ``CatalogError`` (never
    truncates or blends); identical content is an idempotent no-op, so
    a retried dispatch never double-records. "Identical" is judged over
    the CANONICAL record order (``_canonical_records``), so a retry
    whose worker returned the same records in a different JSON order is
    still the no-op, never a phantom immutability conflict.
    """
    root = Path(root)
    day = catalog._as_of_str(as_of)
    jid = str(job_id)
    if not jid or "/" in jid or jid in (".", "..") or jid.startswith("."):
        raise ValueError(f"invalid job id: {job_id!r}")
    document = {
        "schema_version": catalog.SCHEMA_VERSION,
        "kind": RECOMMENDATION_KIND,
        "status": "record",
        "job_id": jid,
        "as_of": day,
        "entries": _canonical_records(records),
    }
    rendered = catalog.render(document)
    out_dir = root / RECOMMENDATIONS_DIR / day
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{jid}.yaml"
    if path.is_file():
        if path.read_text(encoding="utf-8") != rendered:
            raise catalog.CatalogError(
                "immutable recommendation record already exists with "
                f"different content: {path}")
        return path  # completed no-op: identical retry
    try:
        catalog_baseline._write_exclusive(path, rendered)
    except catalog.CatalogError:
        if path.read_text(encoding="utf-8") != rendered:
            raise  # a genuinely conflicting concurrent write
    return path


# --- owner dispositions (T021) ------------------------------------------------

# The contract's two owner-disposition decisions ("External catalog
# application and disposition authority"). Model output is only ever
# `suggested`; only an authorized disposition may produce these.
DISPOSITION_DECISIONS = ("reviewed", "overridden")


def _disposition_authority(repo: str) -> str:
    """Disposition authority follows repository-context ownership
    (contract "External catalog application and disposition
    authority"): the neutral ratify gate for openxFactory classifications,
    the owning factory's Domain Hermes otherwise — the identical
    convention ``document_catalog._owning_authority`` validates
    PERSISTED entries against. Kept as cataloger.py's own copy (see the
    module docstring's note on ``FACET_NAMES``/``CLOSED_VOCABULARIES``:
    this module validates authority BEFORE persistence; document_catalog.py
    validates it after the fact; neither imports the other's constants
    so neither module's checks depend on the other's module boundary)."""
    return NEUTRAL_DISPOSER if repo == NEUTRAL_REPO \
        else f"{repo} authority (Domain Hermes)"


def apply_dispositions(snapshot, override_artifacts) -> list[dict]:
    """Fold authority-checked owner dispositions into a NEW catalog
    entry set (data-model.md "Owner override / disposition"; contract
    "External catalog application and disposition authority").

    ``snapshot`` is one repository's CURRENT catalog entries (mechanical
    fields plus whatever ``facet_assignments`` an earlier merge already
    recorded) — the base state this fold applies onto; it is never
    mutated, and duplicate or ambiguous locator keys are rejected up
    front exactly as ``catalog.merge_recommendations`` requires of its
    own ``snapshot`` argument.

    Each item in ``override_artifacts`` is one owner override, keyed by the
    merged openxFactory arbiter schema
    ``xfactory-document-tag-overrides.schema.yaml`` (#/$defs/override) — the
    exact field names this function reads: ``repo``, the locator, ``facet``,
    ``decision`` (``reviewed`` or ``overridden``), replacement ``values``
    (for an override), the disposing ``actor``, the ``source_content_hash``
    the override binds to, ``occurred_at``, ``rationale``, and
    ``evidence_refs``. An artifact is applied only when EVERY one of these
    holds, and is otherwise silently discarded — never raised, never
    partially applied, and the targeted entry's prior state is always
    retained unchanged (contract scenario "Unauthorized override is
    supplied": "the override MUST be ignored and the catalog MUST retain
    the prior state"):

    - ``decision`` is one of ``reviewed``/``overridden`` and ``facet``
      is one of the contract's six controlled facets;
    - ``actor`` holds ownership standing for the target repository
      (``_disposition_authority``) — an aggregation-side or
      non-owning-layer actor has none;
    - ``occurred_at`` is a non-empty timestamp and both ``rationale`` (a
      non-empty string) and ``evidence_refs`` (a list) are present — the
      override schema requires them, and the merged ``review`` block
      cannot be schema-valid without them;
    - the artifact names an unambiguous locator (a persisted ``path``,
      or an opaque ``document_ref``/``path_sha256`` pair — the same
      shape ``catalog._entry_key`` resolves everywhere else) that
      matches a live entry in ``snapshot``;
    - the artifact's ``source_content_hash`` matches that entry's CURRENT
      content hash (contract scenario "Source content changes after
      review": a stale override — recorded against superseded content —
      must never silently apply, the same binding the openxFactory
      validator's ``check_review_source_freshness`` enforces on committed
      snapshots); and
    - the target facet already has a recorded assignment — an owner
      reviews or overrides an EXISTING classification (contract:
      "Domain Hermes SHALL review classifications..."); a facet the
      cataloger has never touched at all has nothing to dispose of yet.

    A valid ``overridden`` decision requires non-empty replacement
    ``values`` in the artifact; a ``reviewed`` decision always affirms
    the EXISTING assignment's own recorded values — any ``values`` an
    artifact supplies alongside ``reviewed`` are ignored, never a
    second route to changing them (that is what ``overridden`` is for).
    The prior assignment's ``provenance`` (evidence, confidence,
    taxonomy/prompt versions) is preserved unchanged — a disposition
    layers a ``review`` block on top of the classifier's own evidence in
    the snapshot schema's shape (#/$defs/review, required: ``decision``,
    ``authority``, ``occurred_at``, ``rationale``, ``evidence_refs``; the
    override's ``actor`` becomes the block's ``authority``); it never
    fabricates new evidence. The assignment's ``state`` becomes the
    decision, ``state_since`` resets to the disposition's ``occurred_at``
    DATE (bare ``YYYY-MM-DD`` per the snapshot ``state_since`` format,
    even though ``occurred_at`` itself is a date-time), and a ``{from, to,
    occurred_at, evidence_refs}`` transition event (``occurred_at`` a
    date-time) is appended to its history.

    Returns a brand-new, deep-copied entry list sorted by
    ``(repo, locator)`` — "applied only through snapshot merge"
    (feature task T021): this function never touches disk; the caller
    writes the result into a NEW immutable snapshot via
    ``catalog.write_snapshot``, exactly as ``merge_recommendations``
    requires of its own output.
    """
    catalog._keyed(snapshot, "disposition base")  # unique, unambiguous keys
    base = {catalog._entry_key(e): copy.deepcopy(e) for e in snapshot}
    for artifact in override_artifacts or []:
        if not isinstance(artifact, dict):
            continue
        repo = artifact.get("repo")
        decision = artifact.get("decision")
        facet = artifact.get("facet")
        actor = artifact.get("actor")
        occurred_at = artifact.get("occurred_at")
        rationale = artifact.get("rationale")
        evidence_refs = artifact.get("evidence_refs")
        if not (isinstance(repo, str) and repo):
            continue
        if decision not in DISPOSITION_DECISIONS:
            continue
        if facet not in FACET_NAMES:
            continue
        if not (isinstance(occurred_at, str) and occurred_at):
            continue
        # The override schema requires a rationale and evidence_refs, and
        # the merged snapshot `review` block requires both — an artifact
        # missing either is not a schema-valid override and is discarded.
        if not (isinstance(rationale, str) and rationale):
            continue
        if not isinstance(evidence_refs, list):
            continue
        if actor != _disposition_authority(repo):
            continue  # invalid standing: ignored, prior state retained
        try:
            key = catalog._entry_key(artifact)
        except (KeyError, ValueError):
            continue  # no unambiguous locator — never guesses a target
        entry = base.get(key)
        if entry is None:
            continue  # no matching catalog entry — never invents one
        if entry.get("content_hash") != artifact.get("source_content_hash"):
            # Contract scenario "Source content changes after review": the
            # override's bound `source_content_hash` must match the entry's
            # CURRENT content hash, or the disposition is stale and never
            # applies — the same binding the openxFactory validator's
            # `check_review_source_freshness` enforces on committed
            # snapshots (reconciliation item 5).
            continue
        existing_list = entry.get("facet_assignments")
        if not isinstance(existing_list, list):
            continue
        existing = next(
            (a for a in existing_list
             if isinstance(a, dict) and a.get("facet") == facet), None)
        if existing is None:
            continue  # nothing recorded for this facet yet to dispose of
        if decision == "overridden":
            values = artifact.get("values")
            if not (isinstance(values, list) and values):
                continue  # a valid override MUST supply replacement values
        else:  # reviewed: affirms the existing assignment's own values
            values = existing.get("values")
            if not (isinstance(values, list) and values):
                continue
        occurred_dt = _ensure_datetime(occurred_at)
        new_assignment = copy.deepcopy(existing)
        new_assignment["values"] = list(values)
        new_assignment["state"] = decision
        # `state_since` is a bare date (snapshot schema `state_since:
        # {format: date}`) even though a disposition's `occurred_at` is a
        # full date-time (override schema `occurred_at: {format: date-time}`).
        new_assignment["state_since"] = _date_part(occurred_at)
        new_assignment.pop("blocker_ref", None)
        # The merged `review` block follows the snapshot schema #/$defs/review
        # exactly (required: decision, authority, occurred_at, rationale,
        # evidence_refs); the override file's `actor` becomes `authority`.
        new_assignment["review"] = {
            "decision": decision, "authority": actor,
            "occurred_at": occurred_dt, "rationale": rationale,
            "evidence_refs": list(evidence_refs)}
        transitions = list(new_assignment.get("transitions") or [])
        transitions.append({"from": existing.get("state"), "to": decision,
                            "occurred_at": occurred_dt, "evidence_refs": []})
        new_assignment["transitions"] = transitions
        entry["facet_assignments"] = [
            new_assignment if isinstance(a, dict) and a.get("facet") == facet
            else a for a in existing_list]
    return [base[k] for k in sorted(base)]


# --- content/taxonomy/prompt invalidation (T022) ------------------------------

# Facet states carrying a CURRENT semantic classification that a
# content, taxonomy, or prompt change can invalidate (data-model.md
# facet state machine: "any -> pending: only by content/taxonomy/prompt
# invalidation"). `unclassified` IS invalidatable: it is a
# content/taxonomy-grounded classification RESULT (contract scenario
# "Capability cannot resolve": a facet stays `unclassified` "rather than
# inventing a capability"), so a content change makes that determination
# stale exactly like a `suggested`/`reviewed`/`overridden` one and it
# must re-enter `pending` for reclassification (contract "Full baseline
# and incremental refresh": classification carries forward only "when ...
# content hash ... remain[s] unchanged"). Carrying no provenance, it can
# only be invalidated by a change to its OWN document's content (its lack
# of a recorded taxonomy/prompt version makes the version-mismatch and
# reference-propagation branches inert for it), which is the correct and
# only trigger. `policy_blocked` remains deliberately EXCLUDED — it is the
# protected-content defense in depth ``pending_records`` applies (a
# never-dispatched, typically opaque document whose facets never enter the
# ordinary pending/aging machinery at all), never a classification result,
# and an opaque entry has no path to resolve against ``inv`` regardless
# (reconciliation item 7; data-model.md "any -> pending" carve-out).
_INVALIDATABLE_STATES = ("pending", "suggested", "reviewed", "overridden",
                         "unclassified")


def _provenance_incompatible(provenance, taxonomy_sha256, prompt_version) \
        -> bool:
    """True when one recorded assignment's OWN provenance no longer
    matches the CURRENT effective taxonomy digest or prompt-contract
    version (contract "Taxonomy has a breaking change"; single-
    assignment granularity of ``select()``'s ``_facet_incompatible`` —
    FR-011's "affected facets" is per-facet, so ``invalidate`` flips
    only the specific incompatible facet, never the whole document).
    Absent comparison values (``None``) skip that check; a facet
    recording no value for one of these never counts as incompatible
    on its own — only a recorded, differing value does."""
    if not isinstance(provenance, dict):
        return False
    if taxonomy_sha256 is not None and provenance.get(
            "taxonomy_sha256") not in (None, taxonomy_sha256):
        return True
    if prompt_version is not None and provenance.get(
            "prompt_contract_version") not in (None, prompt_version):
        return True
    return False


def _document_reference(ref):
    """Resolve one provenance ``evidence_refs`` element to the
    ``(repo, path)`` document identity used throughout this module, or
    ``None`` when the element does not deterministically denote a
    resolvable document. The recognized form is a mapping carrying
    non-empty string ``repo`` and ``path`` keys — the same identity
    ``select()``, ``merge_recommendations``, and the inventory key
    documents by. Every other element shape (strings, partial mappings,
    opaque ``document_ref`` locators) is opaque here and never resolves:
    an opaque reference cannot be matched against the inventory without
    the very metadata it exists to conceal — the same defense-in-depth
    rule ``invalidate`` applies to an opaque ENTRY's own locator."""
    if not isinstance(ref, dict):
        return None
    repo, path = ref.get("repo"), ref.get("path")
    if isinstance(repo, str) and repo and isinstance(path, str) and path:
        return (repo, path)
    return None


def _changed_references(item, changed) -> list[dict]:
    """The deterministic (sorted, de-duplicated) list of documents this
    recorded assignment's provenance ``evidence_refs`` cite whose
    content changed this run — the propagation channel of the contract
    scenario "One document changes" ("only that entry and any entries
    invalidated by its references MUST become pending classification").
    A facet whose classification was grounded in evidence from content
    that has since changed is a new classification question exactly like
    a facet on the changed document itself. Empty when the assignment
    carries no provenance, no resolvable references, or none citing a
    changed document."""
    if not changed:
        return []
    provenance = item.get("provenance")
    if not isinstance(provenance, dict):
        return []
    refs = provenance.get("evidence_refs")
    if not isinstance(refs, list):
        return []
    hits = {key for key in map(_document_reference, refs) if key in changed}
    return [{"repo": repo, "path": path} for repo, path in sorted(hits)]


def invalidate(entries, inv, as_of, *, current_taxonomy_sha256=None,
               current_prompt_version=None) -> list[dict]:
    """Return affected facets to ``pending`` for a content, taxonomy, or
    prompt-contract change (research D8; contract "Full baseline and
    incremental refresh": "Content/taxonomy/prompt invalidation SHALL
    move the facet to pending and reset it; if the facet was already
    pending, the system SHALL record a pending to pending invalidation
    event and reset the timestamp").

    ``entries`` are catalog entries (mechanical fields plus whatever
    ``facet_assignments`` a prior merge recorded) — this function is
    the semantic-transition half of "carry classification forward";
    mechanical-field refresh (content hash, revision, snapshot id) is
    ``catalog.mechanical_entries``'s concern, not this one, so entries
    are returned with their OTHER fields untouched. ``inv`` is the
    freshly built extended inventory (data-model.md) this run's live
    content hashes are read from. ``as_of`` is the run date every reset
    ``state_since`` and invalidation-event timestamp uses — never wall
    clock (research D4/D8).

    A document's CONTENT is judged changed when its live inventory
    content hash (matched by ``(repo, path)``) differs from the entry's
    OWN recorded ``content_hash`` — the SAME identity the entry's
    facets were classified against (``catalog.merge_recommendations``
    only ever applies a record whose ``content_hash`` matches the live
    entry at merge time, so a persisted entry's ``content_hash`` and its
    ``facet_assignments`` are always in lockstep until content moves).
    A content change invalidates EVERY invalidatable facet on that
    document — all were derived from the same superseded content.
    ``current_taxonomy_sha256``/``current_prompt_version`` (optional;
    omitting either skips that check, mirroring ``select()``'s identical
    convention) invalidate only the SPECIFIC facet whose own recorded
    provenance disagrees, independent of content change.

    A content change also PROPAGATES BY REFERENCE (contract "One
    document changes": "only that entry and any entries invalidated by
    its references MUST become pending classification"): on every OTHER
    entry, the specific facet whose provenance ``evidence_refs`` cite a
    changed document (``_changed_references``; resolvable references
    are ``{repo, path}`` mappings — anything else is opaque and never
    propagates) likewise returns to ``pending`` — its classification
    was grounded in evidence from content that no longer exists.
    Propagation is single-hop BY CONSTRUCTION, exactly the blast radius
    the contract's "only" bounds: a reference-invalidated entry's own
    content is unchanged, so it never joins the changed set and entries
    citing IT stay valid (their evidence about its content still
    holds). Registry/topic references need no walk here — a registry
    content change flows through the effective taxonomy digest and is
    the taxonomy-mismatch branch above. A reference to a DELETED
    document does not propagate: deletion is a mechanical/diff concern
    (``catalog.diff``), the same boundary as the deleted entry itself
    below.

    Per invalidated facet (``_INVALIDATABLE_STATES``): ``state``
    becomes ``pending``, ``values``/``proposed_values`` reset to `[]`,
    ``provenance`` is dropped entirely (a ``pending`` facet carries none
    — the ``pending_records`` shape), ``review`` resets to ``None``, a
    ``{from, to, occurred_at, evidence_refs}`` transition event is
    APPENDED (history is never erased; a reference-triggered event
    records the citing ``{repo, path}`` references as its
    ``evidence_refs`` so the trigger survives the provenance drop),
    and ``state_since`` resets to ``as_of``. An already-``pending``
    facet hit by the same trigger
    records a ``pending`` -> ``pending`` event and likewise resets
    ``state_since`` (contract scenario "Pending input changes again").
    A facet whose state and semantic identity are BOTH unchanged is
    returned byte-identical — untouched, no event recorded — which is
    exactly what lets ``state_since`` carry forward (research D8).

    An entry absent from ``inv`` entirely (its document no longer
    exists) is returned untouched — a deletion is a mechanical/diff
    concern (``catalog.diff``), not a semantic one. An OPAQUE entry (no
    persisted ``path`` — handling policy prohibited it) is likewise
    never matched against ``inv``: this function has no authorized way
    to resolve which inventory document an opaque reference denotes
    without the real path it exists to conceal, so it is always left
    exactly as recorded — the identical defense-in-depth precedent
    ``pending_records`` applies to protected documents. Pure and
    deterministic: entries and their assignments are deep-copied, never
    mutated in place; neither ``entries`` nor ``inv`` is altered.
    """
    as_of_str = catalog._as_of_str(as_of)
    live_content_hash = {}
    for item in inv or []:
        path = item.get("path")
        if path is None:
            continue
        live_content_hash[(item.get("repo"), path)] = item.get("content_hash")

    # Pre-pass: the complete changed-document set — every entry whose
    # recorded ``content_hash`` (the identity its facets were classified
    # against) differs from the live inventory hash. Hoisted out of the
    # per-entry loop so reference propagation below can consult the FULL
    # set regardless of entry order. Opaque entries (``path is None``)
    # never resolve against ``inv`` (see docstring) and never join it.
    changed = set()
    for entry in entries or []:
        path = entry.get("path")
        if path is None:
            continue
        key = (entry.get("repo"), path)
        live_hash = live_content_hash.get(key)
        if live_hash is not None and live_hash != entry.get("content_hash"):
            changed.add(key)

    result = []
    for entry in entries or []:
        new_entry = copy.deepcopy(entry)
        assignments = new_entry.get("facet_assignments")
        if not isinstance(assignments, list):
            result.append(new_entry)
            continue
        path = new_entry.get("path")
        content_changed = (path is not None
                           and (new_entry.get("repo"), path) in changed)
        updated = []
        for item in assignments:
            if not isinstance(item, dict):
                updated.append(item)
                continue
            state = item.get("state")
            incompatible = _provenance_incompatible(
                item.get("provenance"), current_taxonomy_sha256,
                current_prompt_version)
            referenced = _changed_references(item, changed)
            if state not in _INVALIDATABLE_STATES or not (
                    content_changed or incompatible or referenced):
                updated.append(item)  # unchanged: state_since carries forward
                continue
            new_item = copy.deepcopy(item)
            transitions = list(new_item.get("transitions") or [])
            transitions.append({"from": state, "to": "pending",
                                "occurred_at": _as_of_datetime(as_of_str),
                                "evidence_refs": referenced})
            new_item["transitions"] = transitions
            new_item["state"] = "pending"
            new_item["state_since"] = as_of_str
            new_item["values"] = []
            if "proposed_values" in new_item:
                new_item["proposed_values"] = []
            new_item.pop("provenance", None)
            new_item["review"] = None
            updated.append(new_item)
        new_entry["facet_assignments"] = updated
        result.append(new_entry)
    return result
