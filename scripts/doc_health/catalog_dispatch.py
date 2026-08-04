"""Document-cataloger dispatch orchestration: the nightly bridge between
the already-realized mechanical/worker-contract modules (`catalog.py`,
`cataloger.py`, `catalog_baseline.py`) and the CLI/workflow layer.

Realizes Speckit feature `001-document-catalog-nightly` (openxFactory
`add-document-cataloging` tasks 8.1-8.4): mirrors `semantic.py`'s role for
the sibling analysis worker — `prepare_catalog_bundle` is the prepare-phase
primitive (`--catalog-prepare DIR`; computes the deterministic mechanical
entries/diff, then writes a bounded shard bundle for the asynchronous
`document-cataloger` child) and `merge_catalog_findings` is the merge-phase
primitive (`--catalog-findings-in FILE` / `--catalog-unavailable-reason`;
folds a validated recommendation artifact — or an explicit unavailability
reason — into a new immutable snapshot). Both are pure orchestration over
the already-tested `catalog.py`/`cataloger.py` functions: no new mechanical
or contract-validation logic is introduced here, and neither function ever
constructs a `Finding` or touches `result.findings` — `CatalogMeta` is a
distinct, report-only shape (FR-012).

Only `merge_catalog_findings` calls `catalog.write_snapshot` (see its own
docstring for why `prepare_catalog_bundle` deliberately does not): it always
runs — even absent any dispatch at all — so it is the single point of truth
that durably records each run's snapshot, satisfying FR-001/FR-006/FR-007's
"every run produces a full mechanical snapshot" regardless of the cataloger
child's availability.

Deviation from contracts/module-interfaces.md's illustrative sketch: that
document names a `previous_inventory` parameter mirroring
`semantic.prepare_bundle`'s. In practice the catalog's "previous state" is
the CURRENT recorded catalog snapshot itself (`catalog.load_snapshot`),
which already carries forward every prior facet_assignment  — reusing it
avoids inventing a second previous-inventory file format for the extended
(catalog) inventory shape, and match the way `document_catalog.py` (the
deterministic family) already sources "previous catalog state." Both
functions therefore take `catalog_root` instead of `previous_inventory`.

Neither function touches git: the caller (`runner.py`) builds the extended
inventory once via `inventory.build_inventory(docs, repo_paths, git=...)`
(git is injectable there, exactly as `Context.git` already is) and passes
the result in — keeping this module's own test surface hermetic without
needing a git object of its own, and matching `semantic.py`'s existing
`prepare_bundle`/`run_sweep` convention of taking a pre-built `inventory`.

Feature task T014/T015 (US2) add the `baseline_mode` branch: the mechanical,
sharded, resumable full-corpus baseline (`catalog_baseline.py`) is a SEPARATE
bookkeeping track from the always-fresh mechanical snapshot `merge_
catalog_findings` already writes every run unconditionally (US1) — it exists
solely to gate `document_catalog.py`'s "coverage" finding (disclosed
baseline-progress reporting instead of one error per legacy document until
the corpus has been mechanically walked at least once end to end), never to
make the snapshot itself more complete. Consequently `_advance_baseline`
(shared by both `prepare_catalog_bundle` and `merge_catalog_findings` in
baseline mode) never feeds into `_recompute`'s carry-forward/selection
inputs: doing so would let `cataloger.select`'s OWN internal "nothing has
ever been classified" baseline detection (an empty catalog_map) fire across
the WHOLE corpus at once the instant any repository's mechanical baseline
shard landed, defeating the very throttle FR-006 asks for. The two
throttles — mechanical-baseline shards and classification-dispatch shards
— advance independently and are only unified by the report's "Document
Catalog" section (data-model.md `baseline_progress`).

`prepare_catalog_bundle`'s baseline branch calls `catalog_baseline.
run_shard`/`merge_baseline` too, but — like every other write this module's
prepare-phase performs — that call is a deterministic PREVIEW: in the real
two-job nightly topology the `prepare` job's checkout is never committed
(only its bundle artifact is uploaded), so the durable, committed advance of
`health/document-catalog/baseline/` happens via `merge_catalog_findings`'s
OWN parallel call in the `finalize` job (which does commit `health/`) —
exactly the same "recompute independently in both phases, only merge
persists" shape `_recompute` already establishes for the non-baseline path.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

from . import DEFAULT_THRESHOLDS
from . import catalog, catalog_baseline, cataloger, document_catalog
from . import inventory as inv_mod

# Watchdog reasons (data-model.md "Watchdog reason"): the auditable string
# explaining why a dispatched child's result was or wasn't collected.
# `child_<conclusion>` reasons are formed dynamically by the workflow layer
# (e.g. `child_failure`, `child_cancelled`) and have no fixed constant here.
WORKER_UNAVAILABLE = "worker_unavailable"
CHILD_QUEUE_TIMEOUT = "child_queue_timeout"
CHILD_TIMEOUT = "child_timeout"

DEFAULT_MODEL = cataloger.DEFAULT_MODEL
# No shard-budget threshold exists yet anywhere in doc_health (unlike the
# pending-aging thresholds in DEFAULT_THRESHOLDS); this is this module's own
# default, reported as a "non-default configuration" deviation (data-model.md
# CatalogMeta.deviations) whenever a caller overrides it — full deviation
# wiring is feature task T021 (US3), out of this phase's scope.
DEFAULT_SHARD_BUDGET = 25

# The contract's six controlled facet states (data-model.md facet state
# machine), reused here only to key CatalogMeta.state_counts — this module
# validates nothing about them; `document_catalog.py`/`cataloger.py` already
# own that.
FACET_STATE_KEYS = ("pending", "suggested", "reviewed", "overridden",
                    "unclassified", "policy_blocked")


@dataclass
class CatalogMeta:
    """Report-only dispatch summary for one nightly main run (data-model.md
    "CatalogMeta"). Threaded into `report.render(..., catalog_meta=...)`,
    mirroring `semantic.SweepMeta`. Never wrapped in a `Finding`; never
    appended to `result.findings` (FR-012)."""
    snapshot_refs: list = field(default_factory=list)
    total_docs: int = 0
    cataloged: int = 0
    state_counts: dict = field(
        default_factory=lambda: dict.fromkeys(FACET_STATE_KEYS, 0))
    new_count: int = 0
    changed_count: int = 0
    deleted_count: int = 0
    stale_count: int = 0
    rejected_count: int = 0
    inventory_version: str | None = None
    taxonomy_digest: str | None = None
    classifier_version: str = cataloger.CLASSIFIER_VERSION
    prompt_version: int | None = None
    model: str | None = None
    recommendation_refs: list = field(default_factory=list)
    skipped_reason: str | None = None
    baseline_progress: dict | None = None
    # pending_aging/deviations: populated for real by feature task T021
    # (US3); this phase (US1) always reports them empty, matching the
    # "not yet baseline/aging-aware" scope this dispatch-only phase covers.
    pending_aging: dict = field(default_factory=dict)
    deviations: list = field(default_factory=list)


# --- inventory validation (prepare-phase defense in depth) -------------------

def _validate_prepared_inventory(repo_paths: dict, inventory: list[dict],
                                 docs) -> None:
    """Cross-check the caller-supplied EXTENDED inventory against the live
    `docs` (plus each repository's promoted specs — the extended inventory
    shape folds those in too, `inventory.build_inventory`'s own extended-mode
    behavior) set without touching git (mirrors `semantic.prepare_bundle`'s
    "bundle inventory differs from the deterministic corpus" guard, narrowed
    to what's derivable from content alone — `revision`/`snapshot_id`
    require the owning repo's HEAD, which only the caller's injected git
    object can resolve; that shape is validated structurally by
    `catalog.mechanical_entries` instead)."""
    from . import corpus as corpus_mod
    live = [d for d in docs if not inv_mod.is_generated_catalog_path(d.path)]
    hashes = {(d.repo, d.path): hashlib.sha256(d.text.encode()).hexdigest()
              for d in live}
    for name in sorted(repo_paths):
        repo_path = Path(repo_paths[name])
        for spec in corpus_mod.promoted_spec_paths(repo_path):
            rel = spec.relative_to(repo_path).as_posix()
            text = spec.read_text(encoding="utf-8", errors="replace")
            hashes[(name, rel)] = hashlib.sha256(text.encode()).hexdigest()
    inv_keys = {(e["repo"], e["path"]) for e in inventory
                if e.get("path") is not None}
    if set(hashes) != inv_keys:
        raise ValueError(
            "catalog bundle inventory differs from the deterministic "
            "corpus (document set mismatch)")
    by_key = {(e["repo"], e["path"]): e for e in inventory
              if e.get("path") is not None}
    for key, expected in hashes.items():
        if by_key[key].get("content_hash") != expected:
            raise ValueError(
                "catalog bundle inventory differs from the deterministic "
                "corpus (content hash mismatch)")


# --- effective taxonomy (reuses catalog.registry_input/effective_taxonomy) ---

def _effective_taxonomy(repo_paths: dict, inventory: list[dict]) -> dict:
    """The effective taxonomy for this run, built from every
    `document-tag-registry.yaml` under `repo_paths` — the same registry
    filename and rglob scan `cataloger.registered_tag_ids`/
    `document_catalog._controlled_tag_ids` already use (no new resolution
    logic). `repository_revision` comes from the extended inventory's
    per-repo `revision` field (already git-resolved by the caller) rather
    than a fresh git call, since this module takes no git object of its own
    (module docstring). `registry_revision` — provenance-only, never part of
    the digest — is recorded as that same repository revision: this module
    has no per-file git-blame primitive available to name the registry
    file's own last-modifying revision precisely; a future phase may thread
    one through."""
    revision_by_repo: dict[str, str] = {}
    for entry in inventory:
        revision_by_repo.setdefault(entry["repo"], entry.get("revision"))
    inputs = []
    for repo in sorted(repo_paths):
        rev = revision_by_repo.get(repo)
        if not rev:
            continue
        repo_path = Path(repo_paths[repo])
        for reg in sorted(repo_path.rglob(cataloger.TAG_REGISTRY_FILENAME)):
            rel = reg.relative_to(repo_path).as_posix()
            if inv_mod.is_generated_catalog_path(rel):
                continue
            inputs.append(catalog.registry_input(
                repo, rel, reg, repository_revision=rev,
                registry_revision=rev))
    return catalog.effective_taxonomy(inputs)


# --- carry-forward base (mechanical entries + prior facet_assignments) ------

def _carry_forward(curr_entries: list[dict], prev_entries: list[dict]
                    ) -> list[dict]:
    """Fresh mechanical entries as the merge base: unchanged documents (same
    locator key AND content_hash) carry forward whatever
    `facet_assignments`/`dispatch_policy` the previously recorded catalog
    already held; new/changed/missing documents start bare (mechanical
    fields only) — exactly the shape `cataloger.select`'s `new`/`changed`
    reasons expect. Never mutates either input."""
    prev_by_key = {}
    for e in prev_entries:
        try:
            key = catalog._entry_key(e)
        except (KeyError, ValueError):
            continue  # unkeyable row: nothing to carry forward from
        prev_by_key[key] = e
    base = []
    for entry in curr_entries:
        new_entry = dict(entry)
        try:
            key = catalog._entry_key(entry)
        except (KeyError, ValueError):
            base.append(new_entry)
            continue
        prev = prev_by_key.get(key)
        if prev is not None and prev.get("content_hash") == entry.get(
                "content_hash"):
            if "facet_assignments" in prev:
                new_entry["facet_assignments"] = copy.deepcopy(
                    prev["facet_assignments"])
            if "dispatch_policy" in prev:
                new_entry["dispatch_policy"] = copy.deepcopy(
                    prev["dispatch_policy"])
        base.append(new_entry)
    return base


def _state_counts(entries: list[dict]) -> dict:
    counts = dict.fromkeys(FACET_STATE_KEYS, 0)
    for entry in entries:
        for a in entry.get("facet_assignments") or []:
            if isinstance(a, dict) and a.get("state") in counts:
                counts[a["state"]] += 1
    return counts


# --- shared recompute (both prepare and merge derive the same state) --------

def _recompute(repo_paths: dict, inventory: list[dict], catalog_root,
               scope: str | None, shard_budget: int) -> dict:
    curr_entries = catalog.mechanical_entries(inventory)
    previous_run = catalog.load_snapshot(catalog_root)
    prev_entries: list[dict] = []
    if previous_run is not None:
        for doc in previous_run["repos"].values():
            prev_entries.extend(doc.get("entries") or [])
    base_entries = _carry_forward(curr_entries, prev_entries)
    base_by_repo: dict[str, list[dict]] = {}
    for entry in base_entries:
        base_by_repo.setdefault(entry["repo"], []).append(entry)

    taxonomy = _effective_taxonomy(repo_paths, inventory)
    rid = catalog.run_id(inventory, taxonomy)
    prompt_version, prompt_text = cataloger.load_prompt_contract()

    # select()'s own `baseline_mode = not catalog_map` check requires the
    # PRIOR recorded catalog's entries here (empty on a genuine first run,
    # never `base_entries` -- carry-forward's mechanical-shaped output is
    # never empty once any document exists, which would falsely defeat
    # baseline-mode detection). `previous` (used only for changed_keys) is
    # the same prior entries, or None on a first run, matching semantic.
    selections = cataloger.select(
        inventory, prev_entries if previous_run is not None else None,
        prev_entries, current_taxonomy_sha256=taxonomy["digest"],
        current_prompt_version=prompt_version)
    if scope:
        selections = [s for s in selections if s.repo == scope]
    shards = cataloger.build_shards(selections, budget=shard_budget) \
        if selections else []
    the_diff = catalog.diff(prev_entries, curr_entries)
    return {
        "curr_entries": curr_entries, "prev_entries": prev_entries,
        "base_entries": base_entries, "base_by_repo": base_by_repo,
        "taxonomy": taxonomy, "rid": rid,
        "prompt_version": prompt_version, "prompt_text": prompt_text,
        "selections": selections, "shards": shards, "diff": the_diff,
    }


# --- mechanical baseline advancement (T014/T015, shared prepare/merge) ------

def _advance_baseline(repo_paths: dict, catalog_root, as_of,
                      curr_entries: list[dict], scope: str | None,
                      shard_budget: int) -> dict:
    """Advance the sharded, resumable, mechanical full-corpus baseline
    (`catalog_baseline.py`) by exactly one bounded shard for the next
    governed repository whose recorded chain does not yet cover its
    current corpus state ("one bounded, resumable baseline shard" per
    run — spec.md US2 acceptance 1), scoped to a single repository when
    `scope` is given; once every governed repository's chain already
    covers its current corpus, attempts the deterministic merge
    (idempotent/no-op unless every repository just completed).

    Returns `catalog_baseline.progress()`'s coverage summary as a plain
    dict (`CatalogMeta.baseline_progress` / the prepare-phase meta dict's
    same-named field) — never per-document identity (US2 acceptance 2).

    Independent of classification dispatch by construction: this never
    reads or writes `cataloger.select`/`build_shards` state, only the
    mechanical entries the caller already recomputed via
    `catalog.mechanical_entries` (module docstring).

    Never raises `catalog.CatalogError`: a FORCED baseline-mode
    invocation (`--catalog-baseline`, data-model.md's operator escape
    hatch) against an already-complete baseline whose corpus has since
    drifted is refused by `catalog_baseline.run_shard` itself
    ("post-baseline corpus changes flow through the mechanical catalog
    pass") — a deliberate, narrow, operator-triggered edge case that
    `runner.py`'s auto-detection never reaches on its own (it only sets
    `baseline_mode=True` when the baseline is genuinely incomplete).
    Degrading to best-effort progress here rather than propagating
    preserves this feature's single most important invariant: the
    deterministic snapshot/report must never depend on
    `catalog_baseline`'s own state (FR-005 / Constitution Check) —
    `merge_catalog_findings`'s unconditional snapshot write is otherwise
    unaffected either way."""
    if scope is not None and scope not in repo_paths:
        raise ValueError(f"unknown baseline scope repository: {scope!r}")
    by_repo: dict[str, list[dict]] = {}
    for entry in curr_entries:
        by_repo.setdefault(entry["repo"], []).append(entry)
    candidates = [scope] if scope else sorted(repo_paths)
    try:
        advanced = False
        for repo in candidates:
            state = catalog_baseline.run_shard(
                catalog_root, repo, shard_budget, as_of,
                by_repo.get(repo, []))
            if state.processed > 0 or not state.complete:
                advanced = True
                break
        if not advanced:
            # Every candidate repository's chain already covers its
            # current corpus: the merge is the full governed set
            # regardless of `scope` (`catalog_baseline.merge_baseline`
            # requires it), and is a harmless idempotent no-op while
            # other, unscoped repositories remain incomplete.
            catalog_baseline.merge_baseline(catalog_root, as_of,
                                            sorted(repo_paths))
    except catalog.CatalogError:
        pass
    progress = catalog_baseline.progress(catalog_root)
    return {
        "cataloged": progress.cataloged, "total": progress.total,
        "repos_complete": progress.repos_complete,
        "repos_total": progress.repos_total,
        "percent": progress.percent, "complete": progress.complete,
    }


# --- pending-aging / stale counts (T021, reuse document_catalog's checks) ---

def _pending_aging_counts(catalog_root, thresholds: dict, as_of) -> dict:
    """Counts of pending classification facets crossing the 30/90-day
    warn/error boundary (data-model.md `CatalogMeta.pending_aging`) —
    reuses `document_catalog.py`'s OWN existing `_pending_aging_findings`
    aging clock (the same computation the deterministic document-catalog
    family already reports) rather than a second one; only its
    ``[pending-aging]``-classed findings count here (the same helper also
    reports a malformed `state_since` as a distinct `[taxonomy]` shape
    defect, already surfaced by the family's own findings, not aging)."""
    shim = SimpleNamespace(catalog_root=catalog_root, thresholds=thresholds,
                          as_of=as_of)
    counts = {"warning": 0, "error": 0}
    for f in document_catalog._pending_aging_findings(shim):
        if f.rule.startswith("[pending-aging]"):
            counts[f.severity] = counts.get(f.severity, 0) + 1
    return counts


def _stale_count(catalog_root, live_entries: list[dict]) -> int:
    """Count of `[stale-entry]` findings `document_catalog.py`'s existing
    `_stale_entry_findings` check would report for the CURRENT catalogued
    state against `live_entries` (this run's freshly recomputed
    mechanical entries) — reused rather than re-derived (data-model.md
    `CatalogMeta.stale_count`)."""
    shim = SimpleNamespace(catalog_root=catalog_root)
    return sum(1 for f in document_catalog._stale_entry_findings(
        shim, live_entries) if f.rule.startswith("[stale-entry]"))


def _deviations(shard_budget: int, thresholds: dict) -> list[str]:
    """Non-default configuration active this run (data-model.md
    `CatalogMeta.deviations`): the shard budget and the pending-aging
    thresholds, in the SAME string shape `runner.build_context` already
    uses for the report's top-level deviations list."""
    out = []
    if shard_budget != DEFAULT_SHARD_BUDGET:
        out.append(f"catalog shard budget={shard_budget} "
                   f"(default {DEFAULT_SHARD_BUDGET})")
    for key in ("document_catalog_pending_warning_days",
               "document_catalog_pending_error_days"):
        value = thresholds.get(key, DEFAULT_THRESHOLDS[key])
        if value != DEFAULT_THRESHOLDS[key]:
            out.append(f"threshold {key}={value} "
                       f"(default {DEFAULT_THRESHOLDS[key]})")
    return out


# --- prepare-phase primitive (T006) ------------------------------------------

def _bundle_writer(out_dir, allowed_output_root):
    boundary = Path(allowed_output_root).resolve()
    out = Path(out_dir).resolve()
    if not out.is_relative_to(boundary):
        raise ValueError(f"catalog bundle output escapes {boundary}: {out}")

    def write(relative: Path, text: str) -> None:
        dest = out / relative
        if not dest.resolve().is_relative_to(out):
            raise ValueError(f"bundle path escapes the bundle: {relative}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
    out.mkdir(parents=True, exist_ok=True)
    return write


def _write_shard_bundle(out_dir, allowed_output_root, shards, prompt_text,
                        prompt_version, taxonomy, model, as_of, docs) -> None:
    """Write the cataloger child's self-contained bundle: prompt, output
    schema, and one file per shard (job envelope + corpus excerpts for
    exactly that shard's already-protected-filtered selections) — mirrors
    `semantic.prepare_bundle`'s self-containment (module docstring: "the
    bundle is fully self-contained so the worker host needs no repository
    access at all")."""
    write = _bundle_writer(out_dir, allowed_output_root)
    write(Path("prompt.md"), prompt_text)
    schema = {
        "type": "object", "additionalProperties": False,
        "properties": {"entries": {"type": "array"}},
        "required": ["entries"],
    }
    write(Path("output.schema.json"),
          json.dumps(schema, separators=(",", ":")) + "\n")
    by_key = {(d.repo, d.path): d for d in docs}
    shard_ids = []
    for shard in shards:
        job = cataloger.envelope(as_of, model, prompt_version, shard,
                                 taxonomy["digest"])
        documents = []
        for sel in shard.selections:
            doc = by_key.get((sel.repo, sel.path))
            documents.append({
                "repo": sel.repo, "path": sel.path,
                "content_hash": sel.content_hash, "reason": sel.reason,
                "content": doc.text if doc is not None else "",
            })
        write(Path("shards") / f"{shard.shard_id}.json",
              json.dumps({"job": job, "documents": documents},
                        indent=1, sort_keys=True) + "\n")
        shard_ids.append(shard.shard_id)
    write(Path("shards.json"),
          json.dumps(shard_ids, indent=1, sort_keys=True) + "\n")


def prepare_catalog_bundle(repo_paths: dict, docs, as_of, catalog_root,
                           out_dir, model: str, inventory: list[dict],
                           allowed_output_root,
                           baseline_mode: bool = False,
                           scope: str | None = None,
                           shard_budget: int = DEFAULT_SHARD_BUDGET) -> dict:
    """Prepare-phase primitive (`--catalog-prepare DIR`).

    Non-baseline path (feature task T006):
    1. validates `inventory` (the caller's freshly-built EXTENDED inventory)
       matches the live `docs` corpus (`_validate_prepared_inventory`);
    2. computes this run's mechanical entries and diff against the latest
       recorded snapshot (`catalog.mechanical_entries`/`catalog.diff`) —
       completing the deterministic pass BEFORE any cataloger child is
       dispatched (FR-001/FR-002);
    3. selects and shards the diff's new/changed/missing/pending/stale set
       (`cataloger.select`/`build_shards`), scoped by `scope` if given;
    4. writes the self-contained shard bundle under `out_dir`, contained by
       `allowed_output_root` (mirrors `semantic.prepare_bundle`'s boundary
       check).

    Baseline path (`baseline_mode=True`, feature task T014): advances the
    mechanical, sharded, resumable full-corpus baseline
    (`_advance_baseline`) by exactly one bounded shard (or attempts the
    deterministic merge once every governed repository already covers its
    current corpus) INSTEAD of the above — no classification dispatch is
    attempted this invocation (an empty shard bundle is still written, in
    the same self-contained shape, for structural consistency with the
    non-baseline bundle). See the module docstring for why this is
    deliberately decoupled from `cataloger.select`'s own selection/dispatch
    throttle, and why this call is a PREVIEW whose durable persistence
    happens via `merge_catalog_findings`'s parallel call instead.

    Deliberately does NOT call `catalog.write_snapshot` itself (either
    path): `run_id` is a pure function of (inventory, taxonomy) alone
    (`catalog.run_id`), so a caller invoking prepare then merge against the
    SAME checkout (a real scenario — e.g. `--single-repo` local/PR-gate
    use, not only the two-job nightly workflow's separate ephemeral
    runners) would otherwise have this call and `merge_catalog_findings`'s
    later call target the identical immutable run identity with DIFFERENT
    content (mechanical-only here vs. merged-with-recommendations there) —
    catalog.py's immutability guarantee (deliberately absolute; never
    bypassed here, see module docstring) would then refuse the second
    write as a conflict. `merge_catalog_findings` ALWAYS runs (even with
    no dispatch at all — the workflow wiring passes
    `--catalog-unavailable-reason worker_unavailable` unconditionally) and
    is therefore the single point of truth that durably records this run's
    snapshot; FR-001's "before any cataloger child is dispatched" ordering
    is satisfied by this function completing its deterministic COMPUTATION
    (which would raise on any inconsistency) before the dispatch step runs,
    not by a second, redundant persisted write here.

    Returns a meta dict (mirrors `semantic.prepare_bundle`'s meta shape)
    plus the `CatalogMeta` fields available at prepare time.
    """
    _validate_prepared_inventory(repo_paths, inventory, docs)
    if baseline_mode:
        curr_entries = catalog.mechanical_entries(inventory)
        baseline_progress = _advance_baseline(
            repo_paths, catalog_root, as_of, curr_entries, scope,
            shard_budget)
        taxonomy = _effective_taxonomy(repo_paths, inventory)
        prompt_version, prompt_text = cataloger.load_prompt_contract()
        _write_shard_bundle(out_dir, allowed_output_root, [], prompt_text,
                            prompt_version, taxonomy, model, as_of, docs)
        return {
            "as_of": as_of.isoformat(),
            "scope": scope,
            "shard_count": 0,
            "selection_count": 0,
            "total_docs": len(inventory),
            # No carry-forward is computed in baseline mode (module
            # docstring: this call never consults prior classification
            # state) -- nothing is cataloged from THIS call's own view.
            "cataloged": 0,
            "new_count": 0,
            "changed_count": 0,
            "deleted_count": 0,
            "inventory_version": inventory[0]["snapshot_id"] if inventory
            else None,
            "taxonomy_digest": taxonomy["digest"],
            "classifier_version": cataloger.CLASSIFIER_VERSION,
            "prompt_version": prompt_version,
            "model": None,  # never dispatched this invocation
            "run_id": catalog.run_id(inventory, taxonomy),
            "baseline_progress": baseline_progress,
        }
    state = _recompute(repo_paths, inventory, catalog_root, scope,
                       shard_budget)

    _write_shard_bundle(
        out_dir, allowed_output_root, state["shards"], state["prompt_text"],
        state["prompt_version"], state["taxonomy"], model, as_of, docs)

    return {
        "as_of": as_of.isoformat(),
        "scope": scope,
        "shard_count": len(state["shards"]),
        "selection_count": len(state["selections"]),
        "total_docs": len(inventory),
        "cataloged": sum(1 for e in state["base_entries"]
                        if e.get("facet_assignments")),
        "new_count": len(state["diff"].added),
        "changed_count": len(state["diff"].modified),
        "deleted_count": len(state["diff"].deleted),
        "inventory_version": inventory[0]["snapshot_id"] if inventory
        else None,
        "taxonomy_digest": state["taxonomy"]["digest"],
        "classifier_version": cataloger.CLASSIFIER_VERSION,
        "prompt_version": state["prompt_version"],
        "model": model,
        "run_id": state["rid"],
    }


# --- merge-phase primitive (T007) --------------------------------------------

def _read_findings(path):
    p = Path(path)
    if not p.is_file():
        return None, "recommendation artifact file is missing"
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"recommendation artifact is unreadable: {exc}"


def _match_shard(shards, job_id, as_of, model, prompt_version,
                 taxonomy_digest):
    """The dispatched `Shard` (and its job envelope) this run's shard set
    would have produced for `job_id` — reconstructed deterministically
    (never serialized across the prepare/finalize job boundary) since
    `cataloger.build_shards`/`envelope` are pure functions of the same
    (as_of, model, prompt_version, taxonomy digest, selection set), and
    merge runs against the identical commit/corpus state prepare already
    computed within the same workflow run."""
    if not shards:
        return None, None
    if job_id is None:
        if len(shards) == 1:
            shard = shards[0]
            return shard, cataloger.envelope(
                as_of, model, prompt_version, shard, taxonomy_digest)
        return None, None
    for shard in shards:
        job = cataloger.envelope(as_of, model, prompt_version, shard,
                                 taxonomy_digest)
        if job["job"]["id"] == job_id:
            return shard, job
    return None, None


def _resolve_findings(repo_paths: dict, state: dict, as_of, model: str,
                      job_id: str | None, findings_path,
                      unavailable_reason: str | None
                      ) -> tuple[list[dict], int, str | None, str | None]:
    """The `findings_path`/`unavailable_reason` branch of
    `merge_catalog_findings` (extracted so that function's own cognitive
    complexity stays within the repo's linting budget): validates a
    findings artifact against the shard/job this run would have
    dispatched, or records why none is available. Returns
    `(validated_records, rejected_count, skipped_reason, resolved_job_id)`
    — never raises; every failure mode folds into `skipped_reason` instead
    (module docstring: catalog dispatch failures must never crash the
    deterministic run).

    `rejected_count` (data-model.md `CatalogMeta.rejected_count`: "shards
    whose output failed `cataloger.enforce_contract` whole-artifact
    validation") is set ONLY for that one failure mode — a missing/
    unreadable artifact file or a job-id/shard mismatch is an
    availability problem, not a contract-validation rejection, and is
    reported through `skipped_reason` alone (PR #6 review).

    `resolved_job_id` is the dispatched job's own id — `job_id` when the
    caller supplied it, or the `_match_shard`-reconstructed job's id when
    the caller omitted it (the single-shard auto-inference case) — so a
    caller that never passes `job_id` explicitly still gets its
    recommendation evidence persisted (PR #6 review: this was previously
    silently dropped whenever `job_id` was omitted)."""
    if findings_path is None:
        return [], 0, (unavailable_reason or WORKER_UNAVAILABLE), None

    raw_output, read_error = _read_findings(findings_path)
    if read_error is not None:
        return [], 0, read_error, None

    shard, job = _match_shard(state["shards"], job_id, as_of, model,
                              state["prompt_version"],
                              state["taxonomy"]["digest"])
    if shard is None:
        return [], 0, ("recommendation artifact does not match any shard "
                       "dispatched for this run"), None

    resolved_job_id = job_id or job["job"]["id"]
    registered_tags = cataloger.registered_tag_ids(repo_paths)
    records, rejects = cataloger.enforce_contract(
        raw_output, shard, job, registered_tags=registered_tags)
    if rejects:
        return ([], 1, ("recommendation artifact rejected: " + rejects[0]),
                resolved_job_id)
    return records, 0, None, resolved_job_id


def merge_catalog_findings(repo_paths: dict, as_of, catalog_root,
                           model: str, inventory: list[dict],
                           job_id: str | None = None,
                           findings_path=None,
                           unavailable_reason: str | None = None,
                           scope: str | None = None,
                           shard_budget: int = DEFAULT_SHARD_BUDGET,
                           baseline_mode: bool = False,
                           thresholds: dict | None = None,
                           ) -> CatalogMeta:
    """Merge-phase primitive (`--catalog-findings-in FILE` /
    `--catalog-unavailable-reason`).

    1. on `findings_path`: `cataloger.enforce_contract` the raw artifact
       against the shard/job this run would have dispatched
       (`_resolve_findings`/`_match_shard`) — whole-artifact rejection on
       any defect (`rejected_count += 1`, reason folded into
       `skipped_reason`), never a crash;
    2. `cataloger.pending_records` for every selected-but-uncovered facet,
       always (whether or not real findings arrived);
    3. `catalog.merge_recommendations` + `catalog.write_snapshot` the merged
       result per repository — the one call that durably records this run's
       catalog state (see `prepare_catalog_bundle`'s docstring for why it
       never calls `catalog.write_snapshot` itself);
    4. when `baseline_mode`: ALSO advances the mechanical baseline
       (`_advance_baseline`) — this is the call that durably persists it
       (module docstring: this runs in the `finalize` job, which commits
       `health/`, unlike `prepare_catalog_bundle`'s preview call) —
       independent of, and never gating, step 3's unconditional snapshot
       write (task T014/T015);
    5. assembles and returns the full `CatalogMeta` for `report.render()`,
       including the pending-aging/stale-entry counts and non-default-
       configuration deviations reused from `document_catalog.py`'s own
       checks (feature task T021) and, in baseline mode, the coverage
       progress from step 4.
    """
    state = _recompute(repo_paths, inventory, catalog_root, scope,
                       shard_budget)

    validated_records, rejected_count, skipped_reason, resolved_job_id = \
        _resolve_findings(repo_paths, state, as_of, model, job_id,
                         findings_path, unavailable_reason)

    # No classification is ever attempted in baseline mode (module
    # docstring / prepare_catalog_bundle's baseline branch writes zero
    # shards), regardless of whatever skipped_reason a caller passed in.
    dispatch_model = None if (baseline_mode or
                              skipped_reason == WORKER_UNAVAILABLE) else model

    # Same catalog_entries view select() used above (the prior recorded
    # catalog, not the carry-forward base) -- pending_records' own docstring:
    # "catalog_entries is the same current-catalog input select reads".
    pending = cataloger.pending_records(
        state["selections"], state["prev_entries"], as_of)
    all_records = validated_records + pending

    snapshot_refs = []
    merged_entries: list[dict] = []
    for repo in sorted(state["base_by_repo"]):
        merged = catalog.merge_recommendations(
            state["base_by_repo"][repo], all_records)
        merged_entries.extend(merged)
        path = catalog.write_snapshot(
            catalog_root, as_of, state["rid"], repo, merged,
            state["taxonomy"])
        snapshot_refs.append(str(path))

    recommendation_refs = []
    if validated_records and resolved_job_id:
        rec_path = cataloger.persist_recommendations(
            catalog_root, as_of, resolved_job_id, validated_records)
        recommendation_refs.append(str(rec_path))

    baseline_progress = None
    if baseline_mode:
        baseline_progress = _advance_baseline(
            repo_paths, catalog_root, as_of, state["curr_entries"], scope,
            shard_budget)

    effective_thresholds = dict(thresholds) if thresholds else \
        dict(DEFAULT_THRESHOLDS)
    # Read AFTER the snapshot writes above, so pending-aging/stale counts
    # reflect what this run just landed (the same persisted state
    # document_catalog.py's own family would see for this same corpus).
    pending_aging = _pending_aging_counts(
        catalog_root, effective_thresholds, as_of)
    stale_count = _stale_count(catalog_root, state["curr_entries"])
    deviations = _deviations(shard_budget, effective_thresholds)

    return CatalogMeta(
        snapshot_refs=snapshot_refs,
        total_docs=len(inventory),
        cataloged=sum(1 for e in merged_entries
                     if e.get("facet_assignments")),
        state_counts=_state_counts(merged_entries),
        new_count=len(state["diff"].added),
        changed_count=len(state["diff"].modified),
        deleted_count=len(state["diff"].deleted),
        stale_count=stale_count,
        rejected_count=rejected_count,
        inventory_version=inventory[0]["snapshot_id"] if inventory
        else None,
        taxonomy_digest=state["taxonomy"]["digest"],
        classifier_version=cataloger.CLASSIFIER_VERSION,
        prompt_version=state["prompt_version"],
        model=dispatch_model,
        recommendation_refs=recommendation_refs,
        skipped_reason=skipped_reason,
        baseline_progress=baseline_progress,
        pending_aging=pending_aging,
        deviations=deviations,
    )
