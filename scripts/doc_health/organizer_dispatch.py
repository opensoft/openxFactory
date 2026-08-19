"""Ideation-organizer dispatch orchestration: the nightly bridge between the
already-realized organizer worker-contract module (`organizer.py`) and the
CLI/workflow layer (add-cross-factory-ideation-routing tasks 7.1-7.4).

Mirrors `catalog_dispatch.py`'s role for the sibling document-cataloger:
`prepare_organizer_bundle` is the prepare-phase primitive
(`--organizer-prepare DIR`; runs the deterministic selector over the governed
routing records, applies fail-closed source/host authorization, then writes a
bounded, self-contained bundle for the asynchronous `ideation-organizer`
child) and `merge_organizer_findings` is the merge-phase primitive
(`--organizer-findings-in FILE` / `--organizer-unavailable-reason`; validates a
returned recommendation artifact against the ratified organizer contract,
applies the output-policy filter, persists immutable evidence, and links prior
evidence for the next report). Both are pure orchestration over the
already-tested `organizer.py`/`ideation_routing.py` functions: no new
mechanical or contract-validation logic is introduced here, and NEITHER
function ever constructs a `Finding` or touches `result.findings` —
`OrganizerRunMeta` is a distinct, report-only shape (spec "Organizer
recommendations are proposals, not doc-health findings or verdicts").

DETERMINISTIC-FIRST IS STRUCTURAL (task 7.1; spec "The deterministic run SHALL
complete without waiting for organizer execution"). The runner completes the
full fourteen-family suite (including the deterministic `ideation-routing`
family) BEFORE `prepare_organizer_bundle` is even called — this module never
runs a check family, never writes a routing record, a source document, or any
lifecycle state, and every failure mode (worker offline, unauthorized host,
stale signal, invalid output, failed analysis) folds into an
`OrganizerRunMeta.skipped_reason` rather than raising: a total organizer outage
can never delay or suppress the deterministic report (spec scenarios "Worker is
unavailable"/"Organizer child becomes stale"; organizer-and-sweep-contract
"semantic failure does not suppress deterministic health results").

Unlike the cataloger — whose merge ALWAYS writes a fresh mechanical snapshot —
the organizer's deterministic anchor is the fourteenth check family, which the
runner has already produced. This module therefore persists ONLY when a valid
recommendation actually returns (spec "a temporary workflow artifact alone MUST
NOT satisfy persistence"); an unavailable/rejected/unauthorized run records a
skip and writes nothing. Its ONLY disk write is through
`organizer.persist_recommendations`, whose sole write surface is
`health/ideation-organizer/` (the structural root of the organizer's
non-mutation guarantee).

`append_disposition` is the SEPARATE, authorized lifecycle-tooling adapter
(task 7.2; spec scenario "Recommendation is reviewed"): the organizer module
itself has no function that records a verdict, so this module provides the
authorized, append-only, schema-legal way for owning Domain Hermes / neutral
authority / an authorized human to record an accept/modify/reject decision plus
its evidence-record reference onto the canonical routing record. It is NEVER
invoked by the nightly (disposition is a human/Hermes action, not automation)
and never edits any dated report.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from . import corpus, ideation_routing, organizer
from .lines import split_keepends

# Watchdog reasons (spec "Organizer child becomes stale"): the auditable string
# explaining why a dispatched child's result was or wasn't collected. Mirrors
# catalog_dispatch's identical constants so the workflow layer speaks one
# vocabulary; `child_<conclusion>` reasons (child_failure, child_cancelled, ...)
# are formed dynamically by the workflow layer and have no fixed constant here.
WORKER_UNAVAILABLE = "worker_unavailable"
CHILD_QUEUE_TIMEOUT = "child_queue_timeout"
CHILD_TIMEOUT = "child_timeout"

DEFAULT_MODEL = organizer.DEFAULT_MODEL

# Watchdog default thresholds (spec: a child queued longer than ten minutes or
# running longer than thirty minutes is cancelled). These are this module's
# defaults, reported as a deviation whenever a caller overrides them (spec
# "non-default readiness or watchdog thresholds SHALL be reported").
DEFAULT_QUEUE_TIMEOUT_SECONDS = 600
DEFAULT_RUN_TIMEOUT_SECONDS = 1800

# The authorized disposition decisions an owner/Hermes may record onto the
# canonical routing record (spec "Accepted, modified, and rejected decisions
# SHALL remain preserved through evidence references in the routing record").
DISPOSITION_DECISIONS = frozenset({"accepted", "modified", "rejected"})


@dataclass
class OrganizerRunMeta:
    """Report-only dispatch summary for one nightly main run (task 7.3).
    Threaded into `report.render(..., organizer_meta=...)`, mirroring
    `semantic.SweepMeta` and `catalog_dispatch.CatalogMeta`. NEVER wrapped in a
    `Finding`; NEVER appended to `result.findings`; NEVER a regression key —
    organizer recommendations are proposals, not findings or verdicts."""
    # selection (spec "reviews new or materially changed ... ideas, manual
    # requests, new cross-domain links, aged routing items, and pre-gate")
    selected: int = 0
    dispatchable: int = 0
    by_reason: dict = field(default_factory=dict)
    # readiness (hosted preflight result, passed through from the workflow)
    ready: bool | None = None
    readiness_reason: str | None = None
    # authorization (fail-closed source/host evaluation before dispatch)
    authorized: int = 0
    authorization_denied: int = 0
    # skip / watchdog
    skipped_reason: str | None = None
    queue_timeouts: int = 0
    run_timeouts: int = 0
    runs: int = 0
    rejected: int = 0
    # recommendations / immutable evidence
    recommendation_count: int = 0
    dispatched_idea: str | None = None
    evidence_refs: list = field(default_factory=list)        # persisted this run
    linked_evidence_refs: list = field(default_factory=list)  # scanned from dir
    model: str | None = None
    prompt_version: int | None = None
    run_id: str | None = None
    deviations: list = field(default_factory=list)


# --- deterministic run identity ---------------------------------------------

def _run_id(records, as_of) -> str:
    """A deterministic, wall-clock-free run id over the governed routing corpus
    plus `as_of` (mirrors `catalog.run_id`'s content-hash approach). Prepare
    and merge, running against the same commit/corpus within one workflow run,
    compute the identical id — so the reconstructed job envelopes and the
    `<idea-id>-<run-id>.yaml` evidence path line up across the two-job boundary
    without serializing anything across it."""
    parts = sorted(f"{repo}\0{path}\0{organizer._record_fingerprint(record)}"
                   for repo, path, record in records)
    seed = as_of.isoformat() + "\n" + "\n".join(parts)
    return hashlib.sha256(seed.encode()).hexdigest()[:12]


# --- source resolution and authorization (task 7.1/7.2, spec 5.4) ------------

def _records_by_idea(records) -> dict:
    """`{idea_id: (repository, path, record)}` for every record carrying a
    string Idea ID (malformed identity is the deterministic family's concern,
    never the selector's)."""
    out = {}
    for repo, path, record in records:
        iid = record.get("idea_id")
        if isinstance(iid, str) and iid not in out:
            out[iid] = (repo, path, record)
    return out


def _resolve_sources(record: dict, repo_paths: dict, git) -> dict:
    """`{(repository, path): {"revision", "content"}}` for a routing record's
    committed sources — the self-contained input the organizer worker needs
    (it has no repository access at all). The committed revision is the
    source's declared full-commit revision, or the owning repository's current
    HEAD when the record still declares `pending_capture` (spec: "the record
    MUST acquire a committed revision before leaving intake"; "every organize
    or proposal transition SHALL use committed, resolvable revisions"). A
    source whose repository is not in the governed checkout, or whose content
    cannot be read, or whose revision cannot be resolved, yields a `None`
    revision — the caller treats such an idea as non-dispatchable (a nightly
    unavailable-path skip), never a guess."""
    sources: dict = {}
    for source in record.get("sources") or []:
        if not isinstance(source, dict):
            continue
        repo = source.get("repository")
        path = source.get("path")
        if not (isinstance(repo, str) and isinstance(path, str) and path):
            continue
        repo_path = repo_paths.get(repo)
        content = None
        revision = source.get("revision")
        if not (isinstance(revision, str)
                and ideation_routing.FULL_REVISION_RE.match(revision)):
            revision = git.head_sha(repo_path) if repo_path is not None else None
        if repo_path is not None:
            candidate = Path(repo_path) / path
            try:
                if candidate.resolve().is_relative_to(Path(repo_path).resolve()) \
                        and candidate.is_file():
                    content = candidate.read_text(encoding="utf-8",
                                                  errors="replace")
            except OSError:
                content = None
        sources[(repo, path)] = {"revision": revision, "content": content}
    return sources


def _source_descriptor(repo: str, path: str, repo_paths: dict, host: dict,
                       source_handling: dict | None) -> dict:
    """The per-source handling descriptor `organizer.authorize_dispatch`
    evaluates against the attested `host`. An explicit `source_handling`
    override wins (used by tests and by a caller with a resolved source-domain
    policy); otherwise handling is read from the source document's `Handling:`
    header (the same convention `cataloger.is_protected` uses), defaulting to
    the host's own handling class when the source declares none (an ordinary
    governed brainstorm carries no special handling and rides under the host's
    authorization). Tenant/data boundaries default to the host's, since the
    governed corpus is single-tenant; a source-domain policy that differs is
    supplied through `source_handling`."""
    if source_handling and (repo, path) in source_handling:
        return dict(source_handling[(repo, path)])
    handling = None
    repo_path = repo_paths.get(repo)
    if repo_path is not None:
        candidate = Path(repo_path) / path
        try:
            if candidate.is_file():
                text = candidate.read_text(encoding="utf-8", errors="replace")
                handling = _header_value(text, "Handling")
        except OSError:
            handling = None
    host_handling = (host.get("handling_classes") or [None])[0] \
        if isinstance(host, dict) else None
    return {
        "tenant_boundary": (host or {}).get("tenant_boundary"),
        "data_boundary": (host or {}).get("data_boundary"),
        "handling": handling or host_handling,
        "redaction_permitted": False,
    }


def _header_value(text: str, name: str) -> str | None:
    """Same real-line scan window `corpus.parse_status`/`parse_kind` use
    (`doc_health.lines.split_keepends`), so a `Handling:` header an exotic
    separator would otherwise inflate past the window is still found."""
    prefix = f"{name}: "
    for body, _ending in split_keepends(text)[:corpus.STATUS_SCAN_LINES]:
        if body.startswith(prefix):
            return body[len(prefix):].strip() or None
    return None


def _authorize_idea(sources: dict, repo_paths: dict, host: dict | None,
                    source_handling: dict | None) -> bool:
    """Fail-closed pre-dispatch authorization for one idea (task 7.2; spec
    "Before dispatch, orchestration SHALL evaluate each source's declared
    handling and source-domain policy against the host's attested tenant/data
    boundary and organizer handling authorizations"). Every source must
    authorize (mode full or redacted); ANY denied source denies the whole idea
    so no source content or identifying metadata is dispatched. A missing host
    attestation denies everything (spec "Missing readiness or authorization
    SHALL record a fail-closed skip")."""
    if not isinstance(host, dict) or not sources:
        return False
    for (repo, path) in sources:
        descriptor = _source_descriptor(repo, path, repo_paths, host,
                                        source_handling)
        if not organizer.authorize_dispatch(descriptor, host).authorized:
            return False
    return True


# --- dispatch ordering -------------------------------------------------------

def _dispatch_order(selections):
    """Dispatchable selections ordered so the highest-priority reason is first
    (an operator's manual request or a pre-gate review is dispatched before an
    incidental changed/aging signal), ties broken by the selector's own stable
    sort key. The child processes only the first entry per run (one bounded
    child per run, mirroring the cataloger's one-shard-per-run shape); the
    remaining eligible ideas simply re-qualify on a later run."""
    return sorted(
        selections,
        key=lambda s: (organizer._SELECTION_PRIORITY[s.reason], s.sort_key()))


# --- bundle writer (contained, mirrors catalog_dispatch) ---------------------

def _bundle_writer(out_dir, allowed_output_root):
    boundary = Path(allowed_output_root).resolve()
    out = Path(out_dir).resolve()
    if not out.is_relative_to(boundary):
        raise ValueError(f"organizer bundle output escapes {boundary}: {out}")

    def write(relative: Path, text: str) -> None:
        dest = out / relative
        if not dest.resolve().is_relative_to(out):
            raise ValueError(f"bundle path escapes the bundle: {relative}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
    out.mkdir(parents=True, exist_ok=True)
    return write


# --- prepare-phase primitive (task 7.1) --------------------------------------

def _selection_context(records, as_of, thresholds, manual_idea_ids,
                       pre_gate_idea_ids, cross_domain_links, catalog_signals,
                       previous_records):
    """Run the deterministic selector and return the full and dispatchable
    selection lists plus the by-reason counts — recomputed identically in both
    the prepare and merge phases (the selector is a pure function of these
    inputs)."""
    selections = organizer.select(
        records, previous_records, as_of=as_of, thresholds=thresholds,
        manual_idea_ids=manual_idea_ids, pre_gate_idea_ids=pre_gate_idea_ids,
        cross_domain_links=cross_domain_links, catalog_signals=catalog_signals)
    dispatchable = organizer.dispatchable(selections)
    by_reason = dict(Counter(s.reason for s in selections))
    return selections, dispatchable, by_reason


def prepare_organizer_bundle(records, repo_paths, as_of, out_dir, model,
                             *, allowed_output_root, git,
                             manual_idea_ids=(), pre_gate_idea_ids=(),
                             cross_domain_links=(), catalog_signals=(),
                             previous_records=None, thresholds=None,
                             host=None, source_handling=None,
                             run_id=None) -> dict:
    """Prepare-phase primitive (`--organizer-prepare DIR`), mirroring
    `catalog_dispatch.prepare_catalog_bundle`:

    1. runs the deterministic selector over the governed routing `records`
       (`organizer.select`/`dispatchable`) — the deterministic fourteen-family
       suite has ALREADY completed in the runner before this is called
       (task 7.1 / spec "The deterministic run SHALL complete without waiting
       for organizer execution");
    2. for each dispatchable idea, resolves its committed sources and applies
       fail-closed source/host authorization (`_authorize_idea`): a denied or
       unresolvable idea is never bundled, so no source content or identifying
       metadata is dispatched (spec scenarios "Organizer host is unauthorized"
       / "Organizer redaction is not authorized");
    3. writes a self-contained bundle under `out_dir` (contained by
       `allowed_output_root`): the shared prompt + output schema, one
       pre-built analysis input per authorized idea (assembled here with
       `organizer.build_analysis_input`, so the child performs NO brace-bearing
       prompt assembly — the catalog child's `str.format` KeyError lesson), and
       `ideas.json` listing the dispatchable job ids in priority order.

    Deliberately writes NO immutable evidence and NO routing state: persistence
    happens only in the merge phase, and only for a valid returned artifact
    (spec "a temporary workflow artifact alone MUST NOT satisfy persistence").
    Returns a meta dict mirroring the prepare-phase meta shape of the sibling
    lanes."""
    thresholds = thresholds or {}
    rid = run_id or _run_id(records, as_of)
    by_idea = _records_by_idea(records)
    _, dispatchable, by_reason = _selection_context(
        records, as_of, thresholds, manual_idea_ids, pre_gate_idea_ids,
        cross_domain_links, catalog_signals, previous_records)
    prompt_version, prompt_text = organizer.load_prompt_contract()

    write = _bundle_writer(out_dir, allowed_output_root)
    write(Path("prompt.md"), prompt_text)
    write(Path("output.schema.json"),
          json.dumps(organizer.WORKER_OUTPUT_SCHEMA, separators=(",", ":"))
          + "\n")

    job_ids: list[str] = []
    authorized = denied = 0
    for sel in _dispatch_order(dispatchable):
        entry = by_idea.get(sel.idea_id)
        if entry is None:
            continue
        _, _, record = entry
        sources = _resolve_sources(record, repo_paths, git)
        if not sources or any(
                meta.get("revision") is None or meta.get("content") is None
                for meta in sources.values()):
            denied += 1  # unresolvable committed source: skip (nightly)
            continue
        if not _authorize_idea(sources, repo_paths, host, source_handling):
            denied += 1
            continue
        authorized += 1
        job = organizer.envelope(as_of, sel, rid, model, prompt_version)
        job_id = job["job"]["id"]
        analysis_input = organizer.build_analysis_input(
            prompt_text, sel, sources)
        write(Path("ideas") / f"{job_id}.json",
              json.dumps({"job": job,
                          "selection_reason": sel.reason,
                          "idea_id": sel.idea_id},
                         indent=1, sort_keys=True) + "\n")
        write(Path("ideas") / f"{job_id}.input.txt", analysis_input)
        job_ids.append(job_id)
    write(Path("ideas.json"),
          json.dumps(job_ids, indent=1, sort_keys=True) + "\n")

    return {
        "as_of": as_of.isoformat(),
        "run_id": rid,
        "selected": sum(by_reason.values()),
        "dispatchable": len(dispatchable),
        "authorized": authorized,
        "authorization_denied": denied,
        "idea_count": len(job_ids),
        "by_reason": by_reason,
        "model": model,
        "prompt_version": prompt_version,
    }


# --- merge-phase primitive (task 7.2) ----------------------------------------

def _read_findings(path):
    p = Path(path)
    if not p.is_file():
        return None, "recommendation artifact file is missing"
    try:
        return organizer.parse_worker_output(
            json.loads(p.read_text(encoding="utf-8"))), None
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return None, f"recommendation artifact is unreadable: {exc}"


def _match_idea(dispatchable, by_idea, as_of, model, prompt_version, rid,
                job_id):
    """The dispatched selection (and its job envelope) this run's dispatchable
    set would have produced for `job_id` — reconstructed deterministically
    (never serialized across the prepare/finalize job boundary), since
    `organizer.envelope` is a pure function of the same
    (as_of, selection, run_id, model, prompt_version). When `job_id` is None,
    the single-idea case auto-infers it (mirrors `_match_shard`)."""
    ordered = _dispatch_order(dispatchable)
    if job_id is None:
        if len(ordered) == 1:
            sel = ordered[0]
            return sel, organizer.envelope(as_of, sel, rid, model,
                                          prompt_version)
        return None, None
    for sel in ordered:
        job = organizer.envelope(as_of, sel, rid, model, prompt_version)
        if job["job"]["id"] == job_id:
            return sel, job
    return None, None


def _relative(path, evidence_root) -> str:
    """A persisted evidence path expressed repo-relative (POSIX) when it lives
    under the evidence root, so the report links it the same way
    `linked_evidence` does; falls back to the absolute string otherwise."""
    try:
        return Path(path).resolve().relative_to(
            Path(evidence_root).resolve()).as_posix()
    except ValueError:
        return str(path)


def linked_evidence(evidence_root, limit: int = 20) -> list[str]:
    """Immutable organizer-evidence records under `health/ideation-organizer/`,
    most recent first (task 7.2; spec "the dated health report finalized after
    that evidence lands SHALL link its summary" / "the evidence MUST remain in
    its immutable organizer path and be summarized by the NEXT report"). The
    report links from THIS scan of the durable evidence tree, not from a single
    run's in-memory result, so a child whose evidence landed after a prior dated
    report was already closed is still summarized by the next report — without
    ever editing the closed one. Returns repo-relative POSIX paths; the tree is
    only read, never written."""
    root = Path(evidence_root) / organizer.EVIDENCE_DIR
    if not root.is_dir():
        return []
    found = [p for p in root.rglob("*.yaml") if p.is_file()]
    found.sort(key=lambda p: p.as_posix(), reverse=True)
    base = Path(evidence_root)
    return [p.relative_to(base).as_posix() for p in found[:limit]]


def _deviations(queue_timeout_seconds: int, run_timeout_seconds: int) -> list:
    """Non-default watchdog configuration active this run (spec "non-default
    readiness or watchdog thresholds SHALL be reported"), in the same string
    shape the report's top-level deviations list already uses."""
    out = []
    if queue_timeout_seconds != DEFAULT_QUEUE_TIMEOUT_SECONDS:
        out.append(f"organizer queue-timeout={queue_timeout_seconds}s "
                   f"(default {DEFAULT_QUEUE_TIMEOUT_SECONDS}s)")
    if run_timeout_seconds != DEFAULT_RUN_TIMEOUT_SECONDS:
        out.append(f"organizer run-timeout={run_timeout_seconds}s "
                   f"(default {DEFAULT_RUN_TIMEOUT_SECONDS}s)")
    return out


def merge_organizer_findings(records, repo_paths, as_of, model,
                             *, git, evidence_root,
                             findings_path=None, job_id=None,
                             unavailable_reason=None,
                             manual_idea_ids=(), pre_gate_idea_ids=(),
                             cross_domain_links=(), catalog_signals=(),
                             previous_records=None, thresholds=None,
                             host=None, source_handling=None,
                             output_policies=None, run_id=None,
                             ready=None, readiness_reason=None,
                             queue_timeout_seconds=DEFAULT_QUEUE_TIMEOUT_SECONDS,
                             run_timeout_seconds=DEFAULT_RUN_TIMEOUT_SECONDS
                             ) -> OrganizerRunMeta:
    """Merge-phase primitive (`--organizer-findings-in FILE` /
    `--organizer-unavailable-reason`), mirroring
    `catalog_dispatch.merge_catalog_findings` but persisting only on success:

    1. recomputes the selection this run would have dispatched (same pure
       selector inputs as prepare);
    2. on `findings_path`: reads the artifact, reconstructs the dispatched
       idea's selection/job (`_match_idea`), resolves its committed sources,
       and validates the whole artifact against the ratified organizer contract
       (`organizer.enforce_contract`) — whole-artifact rejection on any defect
       (`rejected += 1`, reason folded into `skipped_reason`), never a crash;
    3. applies the output-policy filter (`organizer.filter_recommendations`) to
       suppress protected paths/tags/owners/destinations/summaries before
       anything is persisted centrally (spec scenario "Domain evidence is
       protected");
    4. persists the filtered result as ONE immutable evidence record
       (`organizer.persist_recommendations`, status: record) — the only disk
       write, and only when a valid recommendation actually returned;
    5. scans the durable evidence tree for the next report to link
       (`linked_evidence`) and returns the full `OrganizerRunMeta`.

    Every unavailable/unauthorized/rejected mode records a `skipped_reason` and
    persists nothing; the function NEVER raises on untrusted worker output and
    NEVER touches the deterministic pass (task 7.4)."""
    thresholds = thresholds or {}
    rid = run_id or _run_id(records, as_of)
    by_idea = _records_by_idea(records)
    selections, dispatchable, by_reason = _selection_context(
        records, as_of, thresholds, manual_idea_ids, pre_gate_idea_ids,
        cross_domain_links, catalog_signals, previous_records)
    prompt_version, _ = organizer.load_prompt_contract()

    meta = OrganizerRunMeta(
        selected=len(selections), dispatchable=len(dispatchable),
        by_reason=by_reason, ready=ready, readiness_reason=readiness_reason,
        prompt_version=prompt_version, run_id=rid,
        deviations=_deviations(queue_timeout_seconds, run_timeout_seconds))

    # Authorization is reported over the dispatchable set exactly as prepare
    # decided it (recomputed here since merge may be a separate job/process).
    for sel in _dispatch_order(dispatchable):
        entry = by_idea.get(sel.idea_id)
        if entry is None:
            continue
        sources = _resolve_sources(entry[2], repo_paths, git)
        resolvable = sources and all(
            m.get("revision") is not None and m.get("content") is not None
            for m in sources.values())
        if resolvable and _authorize_idea(sources, repo_paths, host,
                                          source_handling):
            meta.authorized += 1
        else:
            meta.authorization_denied += 1

    if unavailable_reason == CHILD_QUEUE_TIMEOUT:
        meta.queue_timeouts = 1
    elif unavailable_reason == CHILD_TIMEOUT:
        meta.run_timeouts = 1

    if findings_path is None:
        meta.skipped_reason = unavailable_reason or WORKER_UNAVAILABLE
        meta.linked_evidence_refs = linked_evidence(evidence_root)
        return meta

    parsed, read_error = _read_findings(findings_path)
    resolved_job_id = job_id or Path(findings_path).stem
    if read_error is not None:
        meta.skipped_reason = read_error
        meta.linked_evidence_refs = linked_evidence(evidence_root)
        return meta

    sel, job = _match_idea(dispatchable, by_idea, as_of, model, prompt_version,
                           rid, resolved_job_id)
    if sel is None:
        meta.skipped_reason = ("recommendation artifact does not match any "
                               "idea dispatched for this run")
        meta.linked_evidence_refs = linked_evidence(evidence_root)
        return meta

    _, _, record = by_idea[sel.idea_id]
    sources = _resolve_sources(record, repo_paths, git)
    meta.runs = 1
    meta.model = model
    meta.dispatched_idea = sel.idea_id

    # Defense in depth (spec "Missing readiness or authorization SHALL record a
    # fail-closed skip"): even though prepare already gated dispatch on
    # authorization, the merge re-evaluates the dispatched idea against the
    # attested host and refuses to persist an unauthorized source's evidence
    # centrally — a valid-but-unauthorized artifact is a fail-closed skip, never
    # persisted (nothing raw ever lands in aggregation evidence this way).
    if not _authorize_idea(sources, repo_paths, host, source_handling):
        meta.skipped_reason = ("organizer host is not authorized for the "
                               "dispatched source (fail closed)")
        meta.linked_evidence_refs = linked_evidence(evidence_root)
        return meta

    committed = {key: m.get("revision") for key, m in sources.items()}
    primary = _primary_source_revision(record, sources)

    document, rejects = organizer.enforce_contract(
        parsed, sel, committed, job, source_revision=primary, as_of=as_of)
    if rejects:
        meta.rejected = 1
        meta.skipped_reason = f"organizer output rejected: {rejects[0]}"
        meta.linked_evidence_refs = linked_evidence(evidence_root)
        return meta

    filtered, _dropped, _suppressed = organizer.filter_recommendations(
        document, output_policies)
    if filtered.get("recommendations"):
        path = organizer.persist_recommendations(
            evidence_root, as_of, sel.idea_id, rid, filtered)
        meta.evidence_refs = [_relative(path, evidence_root)]
        meta.recommendation_count = len(filtered["recommendations"])
    else:
        # Every recommendation was dropped by a protected-path policy: nothing
        # is persisted centrally, and the run is recorded as a policy skip
        # (never a crash, never a partial write).
        meta.skipped_reason = ("all recommendations suppressed by source "
                               "output policy")
    meta.linked_evidence_refs = linked_evidence(evidence_root)
    return meta


def _primary_source_revision(record: dict, sources: dict) -> str | None:
    """The top-level committed `source_revision` the organizer evidence cites:
    the resolved revision of the record's first structured source. A record
    that resolves none yields a non-committed sentinel that
    `organizer.enforce_contract` then rejects (organizer evidence requires a
    committed revision)."""
    for source in record.get("sources") or []:
        if isinstance(source, dict):
            key = (source.get("repository"), source.get("path"))
            meta = sources.get(key)
            if meta and meta.get("revision") is not None:
                return meta["revision"]
    return ideation_routing.PENDING_CAPTURE


# --- authorized disposition append onto the routing record (task 7.2) --------

def append_disposition(record: dict, claim_id: str, decision: str, *,
                       actor_ref: str, evidence_ref: str, occurred_at: str,
                       authorized: bool) -> dict:
    """Append an AUTHORIZED disposition decision plus its evidence-record
    reference onto one claim of the canonical routing record (task 7.2; spec
    scenario "Recommendation is reviewed": "lifecycle tooling MAY update the
    canonical routing record with the decision and evidence reference"; spec
    "Accepted, modified, and rejected decisions SHALL remain preserved through
    evidence references in the routing record").

    This is the SEPARATE, authorized lifecycle-tooling adapter the organizer
    module deliberately lacks (its recommendations are always `pending_review`
    proposals). It is:

    - AUTHORIZED-ONLY: a falsy `authorized` fails closed (`PermissionError`)
      and changes nothing — an organizer recommendation, tag, or candidate
      owner can never self-authorize a disposition (spec "Tags, candidate
      owners, and organizer confidence MUST NOT confer ownership or
      authority");
    - APPEND-ONLY: it appends one new claim transition carrying the evidence
      reference and never edits or removes any prior transition, source, claim,
      or record field (the deep-copied input is returned untouched); and
    - SCHEMA-LEGAL: `accepted`/`modified` advance the claim one legal step
      along the normal `unresolved -> proposed -> routed` progression and
      `rejected` moves it to `rejected`, each validated against the promoted
      `CLAIM_EDGES` graph — an illegal decision for the claim's current state
      (e.g. accepting an already-`routed` claim) raises rather than fabricating
      an illegal state.

    It NEVER edits any dated report (spec "already finalized `Status: record`
    reports MUST NOT be edited") — reports are immutable records; this touches
    only the routing record, which the caller then persists through the reviewed
    lifecycle-tooling commit under the owning repository. `occurred_at` is a
    caller-supplied timestamp (kept out of this pure function so it stays
    deterministic and testable)."""
    if not authorized:
        raise PermissionError(
            "disposition append requires an authorized actor "
            "(owning Domain Hermes, neutral authority, or an authorized human)")
    if decision not in DISPOSITION_DECISIONS:
        raise ValueError(
            f"decision {decision!r} is not one of {sorted(DISPOSITION_DECISIONS)}")
    if not (isinstance(evidence_ref, str) and evidence_ref.strip()):
        raise ValueError("disposition append requires an evidence-record "
                         "reference")
    result = copy.deepcopy(record)
    claim = _find_claim(result, claim_id)
    if claim is None:
        raise ValueError(f"routing record has no claim {claim_id!r}")

    current = claim.get("disposition")
    if decision == "rejected":
        target = "rejected"
    else:  # accepted / modified: advance one normal-progression step
        target = {"unresolved": "proposed", "proposed": "routed"}.get(current)
        if target is None:
            raise ValueError(
                f"cannot record {decision!r} on a claim in disposition "
                f"{current!r} (no legal forward disposition)")
    if target not in ideation_routing.CLAIM_EDGES.get(current, set()):
        raise ValueError(
            f"illegal claim transition {current!r} -> {target!r} for "
            f"decision {decision!r}")

    claim.setdefault("transitions", []).append({
        "from": current,
        "to": target,
        "actor_ref": actor_ref,
        "occurred_at": occurred_at,
        "evidence_refs": [evidence_ref],
    })
    claim["disposition"] = target
    return result


def _find_claim(record: dict, claim_id: str) -> dict | None:
    for claim in record.get("claims") or []:
        if isinstance(claim, dict) and claim.get("claim_id") == claim_id:
            return claim
    return None
