"""Nightly derive-possibles lane dispatch orchestration (openxFactory
`add-possibles-derivation-lane`; change tasks 4.1-4.2, 4.4).

Mirrors `readiness_dispatch.py`'s role for the derive-possibles worker
(`derive_possibles.py`): `prepare_derive_bundle` is the prepare-phase
primitive (`--phase prepare`; reads the LANDED index from the pinned
openxFactory checkout and writes one self-contained untrusted analysis-input
file per eligible cluster, ready for the artifact-only child to feed directly
into `claude -p`) and `merge_derive_results` is the merge-phase primitive
(`--phase merge`; replays the child's raw per-cluster outputs through the
already-tested `derive_possibles` primitives, merges the surviving proposals
into the index's `possibles_register` section under the fingerprint
compare-and-swap, validates the merged index against the pinned openxFactory
schema+validator BEFORE persistence, and links the outcome from the dated
report). Neither function introduces new mechanical or contract-validation
logic: both are pure orchestration over `derive_possibles`'s own primitives
(`build_analysis_input`, `derive_cluster`, `merge_register`,
`validate_index`, `persist`).

SEQUENCING (doc-health "Possibles derivation lane" delta). Like the
ideation-readiness lane — and unlike the semantic sweep / cataloger lanes —
this lane runs AFTER the deterministic pass, in the nightly workflow's
`finalize` job, consuming the same checkout state. It additionally runs
AFTER the readiness lane's own merge, so the clusters it derives against are
this run's freshest index. Because the artifact-only child has no repository
access and cannot import `doc_health` at all, `prepare_derive_bundle`
precomputes each cluster's FULL untrusted payload text — the child's job
step is a mechanical loop: feed each file to `claude -p`, collect the raw
structured output keyed by cluster id.

SKIP-NEVER-BLOCKS (delta scenario "The worker is offline"). Whenever
`merge_derive_results` does not persist a merged register — no worker
result, a rejected artifact, a stale register, an unreachable validator, or
no openxFactory checkout at all — the lane reports SKIPPED, the register and
index stay at their prior state, and the deterministic results are never
touched (this module never constructs a deterministic `Finding`). Derived
possibles get their OWN report section and are NEVER folded into the Ranked
Plan (the delta's "A consumer counts possibles" scenario), which is exactly
where this lane's report wiring DIFFERS from the readiness lane's.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from . import corpus
from . import derive_possibles as dp

DEFAULT_MODEL = dp.DEFAULT_MODEL
WORKER_UNAVAILABLE = "worker_unavailable"
OPENX_CHECKOUT = "openxFactory"

# Per-run derivation budget (the readiness precedent's lesson twice over):
# once the readiness lane rescores, the landed index carries EVERY derived
# cluster (66 by 2026-07-23; run 29995633933's derive child was watchdog-
# cancelled mid-backlog), so each run derives against at most this many
# eligible clusters — richest member set first, id tiebreak. Applied inside
# `_eligible_clusters` so prepare and merge stay in lockstep, and the
# undisposed-pending guard keeps throttling re-derivation as humans dispose.
MAX_CLUSTERS_PER_RUN = 10


@dataclass
class DeriveLaneMeta:
    """Report-only summary of one lane run, threaded into
    `report.insert_derive_possibles_section`. Carries NO findings on
    purpose: undisposed derived possibles are excluded from the Ranked Plan
    by contract, so — unlike `ReadinessLaneMeta` — nothing here ever reaches
    it."""
    run_id: str
    model: str
    total_clusters: int = 0
    eligible_clusters: int = 0
    proposed: int = 0
    merged_added: list = field(default_factory=list)      # register ids
    merge_skipped: list = field(default_factory=list)     # (id, reason)
    skipped_clusters: list = field(default_factory=list)  # (cluster_id, reason)
    voided: list = field(default_factory=list)            # (cluster_id, title, reason)
    index_path: str | None = None
    evidence_path: str | None = None
    prompt_version: int | None = None
    source_revision: str | None = None
    validated: bool | None = None
    rejection_detail: str | None = None
    skipped_reason: str | None = None
    persisted: bool = False

    @property
    def ok(self) -> bool:
        return self.skipped_reason is None

    def log_line(self) -> str:
        if self.ok:
            return (f"derive-possibles lane: OK {len(self.merged_added)} "
                    f"possible(s) merged from {self.eligible_clusters}/"
                    f"{self.total_clusters} eligible cluster(s) "
                    f"(index={self.index_path})")
        return f"derive-possibles lane: SKIPPED — {self.skipped_reason}"

    def status_json(self) -> dict:
        """The machine-readable outcome the workflow's commit-back step
        reads (change task 4.4): whether this merge PERSISTED openxFactory
        tree changes worth committing back."""
        return {"persisted": self.persisted,
                "merged_added": list(self.merged_added),
                "index_path": self.index_path,
                "evidence_path": self.evidence_path,
                "skipped_reason": self.skipped_reason}


def _load_index(openx: Path) -> dict | None:
    index_path = openx / dp.INDEX_REL
    if yaml is None or not index_path.is_file():  # pragma: no cover
        return None
    try:
        loaded = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, dict) else None


def _register(index: dict) -> list[dict]:
    return [e for e in index.get(dp.REGISTER_KEY) or [] if isinstance(e, dict)]


def _clusters(index: dict) -> list[dict]:
    return sorted(
        (e for e in index.get("topic_entries") or []
         if isinstance(e, dict) and isinstance(e.get("id"), str)),
        key=lambda e: e["id"])


def _eligible_clusters(index: dict, by_path: dict) -> tuple[list, list]:
    """Apply the selection guard the worker module fixes (skip a cluster
    already carrying an undisposed derived possible; skip a cluster with no
    readable member content) — the SAME rule at prepare and merge time, so
    the bundle and the replay never disagree. Returns
    ``(eligible [(cluster, sources)], skipped [(cluster_id, reason)])``."""
    register = _register(index)
    eligible, skipped = [], []
    for cluster in _clusters(index):
        cid = cluster["id"]
        if dp.has_undisposed_derived(register, cid):
            skipped.append((cid, "an undisposed derived possible already "
                                 "claims this cluster"))
            continue
        sources = dp._cluster_sources(cluster, by_path)
        if not sources:
            skipped.append((cid, "no member document content available"))
            continue
        eligible.append((cluster, sources))
    # richest-first budget: the clusters with the largest member sets give
    # the derivation the most cross-document material per model call.
    eligible.sort(key=lambda cs: (-len(cs[0].get("members") or []),
                                  cs[0]["id"]))
    for cluster, _sources in eligible[MAX_CLUSTERS_PER_RUN:]:
        skipped.append((cluster["id"],
                        f"over the per-run budget of {MAX_CLUSTERS_PER_RUN} "
                        "eligible clusters (derives on a later run)"))
    return eligible[:MAX_CLUSTERS_PER_RUN], skipped


def _rel(path: Path, agg_root: Path) -> str:
    try:
        return str(path.relative_to(agg_root))
    except ValueError:
        return str(path)


# --- prepare phase ------------------------------------------------------

def prepare_derive_bundle(agg_root: Path, out_dir: Path, *, run_id: str,
                          model: str = DEFAULT_MODEL) -> dict:
    """Read the landed index from the pinned openxFactory checkout and write
    one self-contained untrusted analysis-input file per ELIGIBLE cluster
    (`<out_dir>/clusters/<cluster_id>.txt`,
    `derive_possibles.build_analysis_input`'s own output — member documents
    plus the cluster's existing possibles for dedupe steering) plus a
    manifest the child and the dispatching workflow both read. Returns the
    manifest dict (also written to `<out_dir>/manifest.json`); a missing
    checkout or index yields a zero-cluster manifest (the workflow's
    `cluster_count != '0'` guard then never dispatches)."""
    agg_root = Path(agg_root)
    out_dir = Path(out_dir)
    openx = agg_root / OPENX_CHECKOUT

    cluster_ids: list[str] = []
    prompt_version, prompt_text = dp.load_prompt_contract()
    index = _load_index(openx) if openx.is_dir() else None
    if index is not None:
        docs = corpus.load_docs(OPENX_CHECKOUT, openx)
        by_path = {d.path: d for d in docs}
        register = _register(index)
        eligible, _skipped = _eligible_clusters(index, by_path)
        clusters_dir = out_dir / "clusters"
        clusters_dir.mkdir(parents=True, exist_ok=True)
        for cluster, sources in eligible:
            existing = dp.cluster_possibles(register, cluster["id"])
            text = dp.build_analysis_input(prompt_text, cluster, sources,
                                           existing)
            (clusters_dir / f"{cluster['id']}.txt").write_text(
                text, encoding="utf-8")
            cluster_ids.append(cluster["id"])

    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run_id": run_id,
        "model": model,
        "prompt_contract_version": prompt_version,
        "cluster_count": len(cluster_ids),
        "cluster_ids": cluster_ids,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    (out_dir / "output.schema.json").write_text(
        json.dumps(dp.WORKER_OUTPUT_SCHEMA, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return manifest


# --- merge phase ---------------------------------------------------------

def _replay_clusters(eligible, raw_results: dict, register: list,
                     meta: "DeriveLaneMeta", run_meta, *, as_of, run_id: str,
                     source_revision: str, model: str, prompt) -> list[dict]:
    """Replay the child's raw per-cluster outputs through
    `derive_possibles.derive_cluster` with per-cluster failure isolation,
    threading skips/voids into both metas. Returns the surviving proposals."""
    proposals: list[dict] = []
    seen = list(register)
    for cluster, sources in eligible:
        cid = cluster["id"]
        cluster_result = raw_results.get(cid)

        def _invoke(_prompt, _model, _result=cluster_result, _cid=cid):
            if not isinstance(_result, dict) or "output" not in _result:
                detail = (_result or {}).get("error") \
                    if isinstance(_result, dict) else None
                raise RuntimeError(
                    detail or f"no remote result collected for {_cid}")
            return _result["output"]

        entries, voided, skip_reason, job_id = dp.derive_cluster(
            cluster, sources, seen, as_of=as_of, run_id=run_id,
            source_revision=source_revision, model=model, prompt=prompt,
            invoke=_invoke)
        run_meta.envelopes.append((cid, job_id))
        for title, reason in voided:
            meta.voided.append((cid, title, reason))
            run_meta.voided.append((cid, title, reason))
        if skip_reason is not None:
            meta.skipped_clusters.append((cid, skip_reason))
            run_meta.skipped_clusters.append((cid, skip_reason))
            continue
        proposals.extend(entries)
        seen.extend(entries)
        meta.proposed += len(entries)
        run_meta.proposed += len(entries)
    return proposals


def _validate_candidate_index(merged: dict, *, validator, openx: Path):
    """Validate-before-persist: stage the candidate in the OS temp dir, NOT
    the repo tree (the only repository writes this lane makes are `persist`'s
    own; spec "Non-mutating derivation bound"), and run the pinned
    openxFactory validator over it. Returns ``(ok, detail)``."""
    import tempfile
    tmp_dir = tempfile.mkdtemp(prefix="derive-possibles-")
    candidate = Path(tmp_dir) / "candidate.yaml"
    try:
        candidate.write_text(dp.render_index_yaml(merged), encoding="utf-8")
        return dp.validate_index(candidate, validator=validator, repo=openx,
                                 strict=True)
    finally:
        candidate.unlink(missing_ok=True)
        try:
            Path(tmp_dir).rmdir()
        except OSError:
            pass


def merge_derive_results(agg_root: Path, *, as_of, run_id: str,
                         findings_path=None,
                         unavailable_reason: str | None = None,
                         model: str = DEFAULT_MODEL,
                         validator: Path | None = None,
                         git=None) -> DeriveLaneMeta:
    """Replay the artifact-only child's raw per-cluster outputs (a
    `{cluster_id: {"output": {...}} | {"error": "..."}}` mapping at
    `findings_path`) through `derive_possibles.derive_cluster`, merge the
    surviving proposals into the index's `possibles_register` under the
    fingerprint compare-and-swap, validate the merged index against the
    pinned openxFactory schema+validator BEFORE persistence, and persist
    only on a clean validation. Any reason this run does NOT persist — an
    explicit `unavailable_reason`, a missing/unreadable artifact, a stale
    register, a rejected index, or no openxFactory checkout at all —
    reports the lane SKIPPED and leaves the register and index at their
    prior state (the delta's "The worker is offline" scenario).

    ``validator``/``git`` are injectable test seams (mirrors
    `merge_readiness_findings`); production leaves both at their defaults."""
    agg_root = Path(agg_root)
    openx = agg_root / OPENX_CHECKOUT

    meta = DeriveLaneMeta(run_id=run_id, model=model)

    def _skip(reason: str) -> DeriveLaneMeta:
        meta.skipped_reason = reason
        return meta

    if not openx.is_dir():
        return _skip("openxFactory checkout not found")
    index = _load_index(openx)
    if index is None:
        return _skip("cross-reference index not found or unreadable")
    meta.total_clusters = len(_clusters(index))
    if unavailable_reason:
        return _skip(unavailable_reason)
    if not findings_path or not Path(findings_path).is_file():
        return _skip(WORKER_UNAVAILABLE)

    try:
        raw_results = json.loads(Path(findings_path).read_text(
            encoding="utf-8"))
    except (OSError, ValueError):
        return _skip("derive-possibles worker findings artifact is "
                     "unreadable")
    if not isinstance(raw_results, dict):
        return _skip("derive-possibles worker findings artifact is "
                     "malformed (expected a cluster_id-keyed object)")

    source_revision = (git or corpus.RealGit()).head_sha(openx)
    if not source_revision:
        return _skip("cannot resolve openxFactory HEAD "
                     "(source_revision is the derivation evidence anchor)")

    docs = corpus.load_docs(OPENX_CHECKOUT, openx)
    by_path = {d.path: d for d in docs}
    prompt_version, prompt_text = dp.load_prompt_contract()
    meta.prompt_version = prompt_version
    meta.source_revision = source_revision

    register = _register(index)
    read_fingerprint = dp.register_fingerprint(register)
    run_meta = dp.DeriveMeta(run_id=run_id, model=model,
                             prompt_version=prompt_version,
                             source_revision=source_revision,
                             register_fingerprint=read_fingerprint)

    eligible, skipped = _eligible_clusters(index, by_path)
    meta.skipped_clusters.extend(skipped)
    meta.eligible_clusters = len(eligible)

    proposals = _replay_clusters(
        eligible, raw_results, register, meta, run_meta,
        as_of=as_of, run_id=run_id, source_revision=source_revision,
        model=model, prompt=(prompt_version, prompt_text))

    if not proposals:
        return _skip("no proposal survived contract enforcement "
                     f"({meta.proposed} proposed)")

    # The section-level compare-and-swap: refuse a stale overwrite when a
    # concurrent run advanced the on-disk register between our read and this
    # merge (the delta's "A concurrent run advanced the register" scenario).
    current = _load_index(openx)
    if current is None or dp.register_fingerprint(_register(current)) \
            != read_fingerprint:
        return _skip("possibles_register advanced during the merge "
                     "(stale overwrite refused)")
    try:
        merged, added, merge_skipped = dp.merge_register(
            index, proposals, expected_fingerprint=read_fingerprint)
    except dp.StaleRegisterError as exc:
        return _skip(str(exc))
    meta.merged_added = added
    meta.merge_skipped = merge_skipped

    ok, detail = _validate_candidate_index(merged, validator=validator,
                                           openx=openx)
    meta.validated = ok
    if ok is not True:
        meta.rejection_detail = detail
        reason = (f"merged index rejected by the pinned validator: "
                  f"{detail}") if ok is False else \
            f"index validator unreachable: {detail}"
        return _skip(reason)

    written, _boundary = dp.persist(merged, run_meta, root=openx,
                                    as_of=as_of, added=added,
                                    skipped_merge=merge_skipped)
    meta.persisted = True
    meta.index_path = _rel(openx / written["index"], agg_root)
    if "evidence" in written:
        meta.evidence_path = _rel(openx / written["evidence"], agg_root)
    return meta


# --- CLI -------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    import argparse
    from datetime import date

    ap = argparse.ArgumentParser(
        prog="derive-possibles-nightly", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-root", required=True,
                    help="the aggregation checkout root")
    ap.add_argument("--phase", required=True, choices=["prepare", "merge"])
    ap.add_argument("--as-of", required=True,
                    help="ISO date (the SAME run_date the deterministic "
                         "pass's report/inventory used this run)")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--out-dir", help="prepare phase: bundle output dir")
    ap.add_argument("--findings-in",
                    help="merge phase: the child's raw per-cluster results")
    ap.add_argument("--unavailable-reason",
                    help="merge phase: explicit skip reason (dispatch/"
                         "collection never produced a findings artifact)")
    ap.add_argument("--report-in",
                    help="merge phase: the dated report to update in place "
                         "with the Derived Possibles section (never the "
                         "Ranked Plan)")
    ap.add_argument("--status-out",
                    help="merge phase: write the machine-readable lane "
                         "outcome JSON here (the commit-back step's input)")
    args = ap.parse_args(argv)
    as_of = date.fromisoformat(args.as_of)
    agg_root = Path(args.repo_root)

    try:
        if args.phase == "prepare":
            if not args.out_dir:
                raise SystemExit("--out-dir is required for --phase prepare")
            manifest = prepare_derive_bundle(
                agg_root, Path(args.out_dir), run_id=args.run_id,
                model=args.model)
            print(f"derive-possibles prepare: {manifest['cluster_count']} "
                  f"cluster(s) bundled")
            return 0

        meta = merge_derive_results(
            agg_root, as_of=as_of, run_id=args.run_id,
            findings_path=args.findings_in,
            unavailable_reason=args.unavailable_reason, model=args.model)
        if args.report_in:
            from . import report as report_mod
            report_path = Path(args.report_in)
            text = report_path.read_text(encoding="utf-8")
            report_path.write_text(
                report_mod.insert_derive_possibles_section(text, meta),
                encoding="utf-8")
        if args.status_out:
            Path(args.status_out).write_text(
                json.dumps(meta.status_json(), indent=2, sort_keys=True)
                + "\n", encoding="utf-8")
        print(meta.log_line())
        return 0
    except Exception as exc:  # noqa: BLE001 — never fail the nightly
        print(f"derive-possibles lane: SKIPPED — unhandled "
              f"{type(exc).__name__}: {exc}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
