"""Nightly ideation-readiness lane dispatch orchestration (openxFactory
`add-ideation-cross-reference-readiness`; change tasks 4.1-4.3).

Mirrors `catalog_dispatch.py`'s role for the readiness scorer
(`ideation_readiness.py`): `prepare_readiness_bundle` is the prepare-phase
primitive (`--phase prepare`; derives clusters from the CURRENT checkout and
writes one self-contained untrusted analysis-input file per cluster, ready
for the artifact-only child to feed directly into `claude -p`) and
`merge_readiness_findings` is the merge-phase primitive (`--phase merge`;
folds the child's raw per-cluster outputs — or an explicit unavailability
reason — into a freshly assembled index, validates it against the pinned
openxFactory schema+validator BEFORE persistence, and derives the
`ideation-readiness` findings the dated report links). Neither function
introduces new mechanical or contract-validation logic: both are pure
orchestration over the already-tested `ideation_readiness.py` primitives
(`derive_clusters`, `build_analysis_input`, `score_cluster`, `validate_index`,
`persist`, `readiness_findings`).

SEQUENCING (doc-health "Ideation readiness lane" ADDED requirement — the one
respect in which this lane's dispatch shape DIFFERS from the semantic sweep
and document-cataloger lanes it otherwise clones): those two dispatch BEFORE
the deterministic pass, against the previous day's inventory. This lane's own
requirement binds it to run AFTER the deterministic pass, against the SAME
inventory snapshot that pass just emitted — so both phases here run in the
nightly workflow's `finalize` job, after "Run doc-health suite", never in
`prepare`. Because the artifact-only child workflow has no repository access
and cannot import `doc_health` at all (the same reason
`doc-health-cataloger-worker.yml` embeds only stdlib json, never a package
import), `prepare_readiness_bundle` precomputes each cluster's FULL untrusted
payload text — not just raw ingredients — so the child's job step is a
mechanical loop: feed each file to `claude -p`, collect the raw structured
output keyed by cluster id.

SKIP-NOT-RESOLVED (doc-health "Ideation readiness lane" scenario "The lane is
skipped" / change task 5.1's last case): whenever `merge_readiness_findings`
does not persist a freshly scored index — no worker result, a rejected
artifact, an unreachable validator, or no openxFactory checkout at all — its
`.findings` are read back from the EXISTING on-disk index (the last
successfully persisted state) rather than left empty. A prior finding that is
absent only because THIS run's lane did not score is therefore never treated
as resolved; the deterministic results are never touched either way (this
module never constructs or returns a deterministic `Finding` from the
`FAMILY_IDS` list — only `ideation_readiness.readiness_findings`' own
report-only, `contested`, at-most-`warning` family).
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
from . import ideation_readiness as ir

DEFAULT_MODEL = ir.DEFAULT_MODEL
WORKER_UNAVAILABLE = "worker_unavailable"
OPENX_CHECKOUT = "openxFactory"

# Per-run scoring budget. The corpus outgrew the 15-cluster bootstrap the
# child's 30-minute job cap was shaped around (67 clusters by 2026-07-23:
# run 29992091770's child was watchdog-cancelled mid-backlog), so each run
# bundles at most this many clusters, UNSCORED-FIRST against the on-disk
# index (a cluster already carrying a scored readiness panel re-scores only
# after every unscored one has had a turn). The merge phase already handles
# a partial result set — clusters without results fall back to the unscored
# skeleton and skip-not-resolved keeps prior findings — so the budget
# converges the whole corpus across successive nightly runs.
MAX_CLUSTERS_PER_RUN = 12


@dataclass
class ReadinessLaneMeta:
    """Report-only summary of one lane run, threaded into
    `report.insert_readiness_section`. Unlike `CatalogMeta` (whose
    recommendations never reach the Ranked Plan), `.findings` here DOES —
    the ADDED requirement's own scenario puts `ideation-readiness` findings
    in the ranked plan as report-only `contested`/`warning` items."""
    run_id: str
    model: str
    total_clusters: int = 0
    scored_clusters: int = 0
    skipped_clusters: list = field(default_factory=list)  # (cluster_id, reason)
    index_path: str | None = None
    index_md_path: str | None = None
    evidence_path: str | None = None
    prompt_version: int | None = None
    source_revision: str | None = None
    validated: bool | None = None
    rejection_detail: str | None = None
    skipped_reason: str | None = None
    findings: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.skipped_reason is None

    def log_line(self) -> str:
        if self.ok:
            return (f"ideation-readiness lane: OK {self.scored_clusters}/"
                    f"{self.total_clusters} clusters scored "
                    f"(index={self.index_path})")
        return f"ideation-readiness lane: SKIPPED — {self.skipped_reason}"


def _readiness_docs(agg_root: Path) -> list[corpus.Doc]:
    """The openxFactory ideation corpus this lane clusters over — ONLY the
    pinned `openxFactory` checkout, never the whole family. The index is the
    openxFactory-hosted `ideation/cross-reference.yaml` (schema
    `repository: openxFactory`; check-matrix §9: "writes only the openxFactory
    index"), and its bootstrap + reproduction guarantee is byte-equivalence
    with `bootstrap-ideation-cross-reference.py`, which scans openxFactory
    alone. Scanning `xFactories/*` too would fold sibling repos' own
    `ideation/brainstorm|staging` docs into the index (path-keyed clustering
    even collides same-relative-path members across repos) and silently
    replace the landed 15-cluster bootstrap with a divergent family-wide
    index — breaking the "worker- and bootstrap-derived index agree on an
    unchanged corpus" invariant `derive_clusters` promises."""
    openx = Path(agg_root) / OPENX_CHECKOUT
    if not openx.is_dir():
        return []
    return corpus.load_docs(OPENX_CHECKOUT, openx)


def _rel(path: Path, agg_root: Path) -> str:
    try:
        return str(path.relative_to(agg_root))
    except ValueError:
        return str(path)


def _load_existing_index(index_path: Path) -> dict | None:
    if yaml is None or not index_path.is_file():  # pragma: no cover
        return None
    try:
        loaded = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, dict) else None


# --- prepare phase ------------------------------------------------------

def prepare_readiness_bundle(agg_root: Path, out_dir: Path, *, run_id: str,
                             model: str = DEFAULT_MODEL) -> dict:
    """Derive clusters from the current checkout and write one
    self-contained untrusted analysis-input file per cluster
    (`<out_dir>/clusters/<cluster_id>.txt`, `ideation_readiness.
    build_analysis_input`'s own output) plus a manifest the child and the
    dispatching workflow both read. Returns the manifest dict (also written
    to `<out_dir>/manifest.json`)."""
    agg_root = Path(agg_root)
    out_dir = Path(out_dir)
    openx = agg_root / OPENX_CHECKOUT

    docs = _readiness_docs(agg_root)
    by_path = {d.path: d for d in docs}
    catalog_tags = ir.load_catalog_tags(agg_root)
    clusters = ir.derive_clusters(docs, catalog_tags=catalog_tags)
    capabilities = sorted(ir.resolve_capability_set(
        openx if openx.is_dir() else None))
    prompt_version, prompt_text = ir.load_prompt_contract()

    # Unscored-first budget (MAX_CLUSTERS_PER_RUN): rank clusters the on-disk
    # index has never scored ahead of already-scored ones, id-order tiebreak.
    existing = _load_existing_index(openx / ir.INDEX_REL) or {}
    scored_ids = {
        e.get("id") for e in existing.get("topic_entries") or []
        if isinstance(e, dict)
        and isinstance(e.get("readiness"), dict)
        and e["readiness"].get("recommendation") is not None
    }
    total_clusters = len(clusters)
    clusters = sorted(
        clusters, key=lambda c: (c["id"] in scored_ids, c["id"]))
    clusters = clusters[:MAX_CLUSTERS_PER_RUN]

    clusters_dir = out_dir / "clusters"
    clusters_dir.mkdir(parents=True, exist_ok=True)
    cluster_ids = []
    for cluster in clusters:
        sources = ir._cluster_sources(cluster, by_path)
        text = ir.build_analysis_input(prompt_text, cluster, sources,
                                       capabilities)
        (clusters_dir / f"{cluster['id']}.txt").write_text(
            text, encoding="utf-8")
        cluster_ids.append(cluster["id"])

    manifest = {
        "run_id": run_id,
        "total_clusters": total_clusters,
        "model": model,
        "prompt_contract_version": prompt_version,
        "cluster_count": len(cluster_ids),
        "cluster_ids": cluster_ids,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    (out_dir / "output.schema.json").write_text(
        json.dumps(ir.WORKER_OUTPUT_SCHEMA, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return manifest


# --- merge phase ---------------------------------------------------------

def merge_readiness_findings(agg_root: Path, *, as_of, run_id: str,
                             findings_path=None,
                             unavailable_reason: str | None = None,
                             model: str = DEFAULT_MODEL,
                             validator: Path | None = None,
                             git=None) -> ReadinessLaneMeta:
    """Fold the artifact-only child's raw per-cluster outputs (a
    `{cluster_id: {"output": {...}} | {"error": "..."}}` mapping at
    `findings_path`) into a freshly assembled index, validate it against the
    pinned openxFactory schema+validator BEFORE persistence, and persist only
    on a clean validation. Any reason this run does NOT persist a fresh index
    — an explicit `unavailable_reason`, a missing/unreadable artifact, a
    rejected index, or no openxFactory checkout at all — reports the lane
    SKIPPED and reads `.findings` back from the EXISTING on-disk index
    instead of leaving it empty (skip-not-resolved).

    ``validator``/``git`` are injectable test seams (mirrors
    ``ir.validate_index``'s own ``validator`` and ``conftest.FakeGit``
    elsewhere in this suite): production leaves both at their defaults (the
    pinned openxFactory validator; `corpus.RealGit`)."""
    agg_root = Path(agg_root)
    openx = agg_root / OPENX_CHECKOUT
    index_path = openx / ir.INDEX_REL

    docs = _readiness_docs(agg_root)
    by_path = {d.path: d for d in docs}
    catalog_tags = ir.load_catalog_tags(agg_root)
    clusters = ir.derive_clusters(docs, catalog_tags=catalog_tags)

    meta = ReadinessLaneMeta(run_id=run_id, model=model,
                             total_clusters=len(clusters))

    def _skip(reason: str) -> ReadinessLaneMeta:
        meta.skipped_reason = reason
        existing = _load_existing_index(index_path)
        if existing is not None:
            meta.index_path = _rel(index_path, agg_root)
            md_path = openx / ir.INDEX_MD_REL
            if md_path.is_file():
                meta.index_md_path = _rel(md_path, agg_root)
            meta.findings = ir.readiness_findings(
                existing, repo=openx if openx.is_dir() else None)
        return meta

    if not openx.is_dir():
        return _skip("openxFactory checkout not found")
    if unavailable_reason:
        return _skip(unavailable_reason)
    if not findings_path or not Path(findings_path).is_file():
        return _skip(WORKER_UNAVAILABLE)

    try:
        raw_results = json.loads(Path(findings_path).read_text(
            encoding="utf-8"))
    except (OSError, ValueError):
        return _skip("readiness worker findings artifact is unreadable")
    if not isinstance(raw_results, dict):
        return _skip("readiness worker findings artifact is malformed "
                     "(expected a cluster_id-keyed object)")

    source_revision = (git or corpus.RealGit()).head_sha(openx)
    if not source_revision:
        return _skip("cannot resolve openxFactory HEAD "
                     "(source_revision is the deterministic anchor)")

    capabilities = ir.resolve_capability_set(openx)
    prompt_version, prompt_text = ir.load_prompt_contract()
    meta.prompt_version = prompt_version
    meta.source_revision = source_revision

    entries = []
    for cluster in clusters:
        sources = ir._cluster_sources(cluster, by_path)
        cluster_result = raw_results.get(cluster["id"])

        def _invoke(_prompt, _model, _result=cluster_result,
                    _cid=cluster["id"]):
            if not isinstance(_result, dict) or "output" not in _result:
                detail = (_result or {}).get("error") \
                    if isinstance(_result, dict) else None
                raise RuntimeError(
                    detail or f"no remote result collected for {_cid}")
            return _result["output"]

        entry, _job_id = ir.score_cluster(
            cluster, sources, capabilities, as_of=as_of, run_id=run_id,
            source_revision=source_revision, model=model,
            prompt=(prompt_version, prompt_text), invoke=_invoke)
        entries.append(entry)

        readiness = entry.get("readiness") or {}
        if readiness.get("recommendation") is not None:
            meta.scored_clusters += 1
        else:
            reason = next(
                (t.get("unscored_reason") for t in
                 readiness.get("tiers") or []
                 if isinstance(t, dict) and t.get("unscored_reason")),
                "unscored")
            meta.skipped_clusters.append((cluster["id"], reason))

    index = {
        "schema_version": 1,
        "kind": ir.INDEX_KIND,
        "repository": "openxFactory",
        "generation": {"source_revision": source_revision,
                      "generator_version": ir.GENERATOR_VERSION},
        "topic_entries": entries,
    }
    # Carry the EXISTING possibles_register section through unchanged: the
    # register is the derive-possibles lane's write target
    # (add-possibles-derivation-lane), never this lane's — a readiness
    # re-score that dropped it would silently destroy merged possibles and
    # their disposition audit trails. An absent section is the documented
    # bootstrap state and stays absent.
    existing = _load_existing_index(index_path)
    if existing is not None and isinstance(
            existing.get("possibles_register"), list):
        index["possibles_register"] = existing["possibles_register"]

    # Validate-before-persist stages the candidate in the OS temp dir, NOT the
    # repo tree: the only repository writes this lane makes are the persisted
    # index/evidence through the OutputBoundary (spec "Non-mutating execution
    # bound"). A repo-root candidate would be a transient write outside the
    # declared outputs and could survive a crash between write and unlink.
    import tempfile
    tmp_dir = tempfile.mkdtemp(prefix="ideation-readiness-")
    candidate = Path(tmp_dir) / "candidate.yaml"
    try:
        candidate.write_text(ir.render_index_yaml(index), encoding="utf-8")
        ok, detail = ir.validate_index(candidate, validator=validator,
                                       repo=openx, strict=True)
    finally:
        candidate.unlink(missing_ok=True)
        try:
            Path(tmp_dir).rmdir()
        except OSError:
            pass
    meta.validated = ok
    if ok is not True:
        meta.rejection_detail = detail
        reason = (f"assembled index rejected by the pinned validator: "
                  f"{detail}") if ok is False else \
            f"index validator unreachable: {detail}"
        return _skip(reason)

    run_meta = ir.ReadinessMeta(run_id=run_id, model=model,
                               prompt_version=prompt_version,
                               source_revision=source_revision,
                               scored_clusters=meta.scored_clusters,
                               skipped_clusters=meta.skipped_clusters)
    written, _boundary = ir.persist(index, run_meta, root=openx, as_of=as_of)
    meta.index_path = _rel(openx / written["index"], agg_root)
    if "md" in written:
        meta.index_md_path = _rel(openx / written["md"], agg_root)
    if "evidence" in written:
        meta.evidence_path = _rel(openx / written["evidence"], agg_root)
    meta.findings = ir.readiness_findings(index, repo=openx)
    return meta


# --- CLI -------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    import argparse
    from datetime import date

    ap = argparse.ArgumentParser(
        prog="ideation-readiness-nightly", description=__doc__,
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
                         "with the Ideation Readiness section + ranked-plan "
                         "lines")
    args = ap.parse_args(argv)
    as_of = date.fromisoformat(args.as_of)
    agg_root = Path(args.repo_root)

    try:
        if args.phase == "prepare":
            if not args.out_dir:
                raise SystemExit("--out-dir is required for --phase prepare")
            manifest = prepare_readiness_bundle(
                agg_root, Path(args.out_dir), run_id=args.run_id,
                model=args.model)
            print(f"ideation-readiness prepare: {manifest['cluster_count']} "
                 f"cluster(s) bundled")
            return 0

        meta = merge_readiness_findings(
            agg_root, as_of=as_of, run_id=args.run_id,
            findings_path=args.findings_in,
            unavailable_reason=args.unavailable_reason, model=args.model)
        if args.report_in:
            from . import report as report_mod
            report_path = Path(args.report_in)
            text = report_path.read_text(encoding="utf-8")
            report_path.write_text(
                report_mod.insert_readiness_section(text, meta),
                encoding="utf-8")
        print(meta.log_line())
        return 0
    except Exception as exc:  # noqa: BLE001 — never fail the nightly
        print(f"ideation-readiness lane: SKIPPED — unhandled "
             f"{type(exc).__name__}: {exc}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
