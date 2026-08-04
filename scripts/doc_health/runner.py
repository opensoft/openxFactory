"""Suite runner CLI.

Modes:
  --repo-root <aggregation checkout>   full family-corpus run
  --single-repo <repo path>            one repo (PR self-gate); families
                                       needing the aggregation scope skip
                                       with notice

Determinism: identical inputs (commit states, config, --as-of date) yield
byte-identical findings and report. Wall-clock enters only through the
explicit --as-of default.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

from . import DEFAULT_THRESHOLDS, ERROR, CRITICAL, Finding, RunResult, Skip
from . import corpus, report
from .families import FAMILIES
from .preflight import run_preflight

SYNC_SCRIPT = "openxFactory/scripts/sync-notebooklm-books.py"


@dataclass
class Context:
    repo_paths: dict
    docs: list
    capabilities: dict
    change_ids: dict
    git: object
    thresholds: dict
    as_of: date
    agg_root: Path | None
    notebook_dryrun: object = field(default=lambda: None)
    # add-document-cataloging (feature task T014): the document-catalog
    # family's storage root. Aggregation runs use agg_root (the catalog
    # spans every pinned repo); a single-repo run falls back to that one
    # repo's own path, so a self-contained checkout can still carry its
    # own health/document-catalog/ tree. Baseline-mode resolution
    # (catalog_baseline.is_baseline_complete) and previous-run lookup
    # (catalog.load_snapshot) both key off this one field — no other
    # context extension is needed.
    catalog_root: Path | None = field(default=None)


def _real_notebook_dryrun(agg_root: Path | None):
    def run():
        if agg_root is None or not (agg_root / SYNC_SCRIPT).is_file():
            return None
        try:
            probe = subprocess.run(["nlm", "notebook", "list"],
                                   capture_output=True, text=True, timeout=60)
            if probe.returncode != 0:
                return None
            proc = subprocess.run(
                ["python3", SYNC_SCRIPT, "."], cwd=agg_root,
                capture_output=True, text=True, timeout=600)
            return proc.stdout if proc.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            return None
    return run


def build_context(args) -> Context:
    if args.single_repo:
        root = Path(args.single_repo).resolve()
        repos = [(root.name, root)]
        agg_root = None
    else:
        agg_root = Path(args.repo_root).resolve()
        repos = corpus.discover_repos(agg_root)
    repo_paths = dict(repos)
    docs, capabilities, change_ids = [], {}, {}
    for name, path in repos:
        docs.extend(corpus.load_docs(name, path))
        capabilities[name] = corpus.spec_capabilities(path)
        change_ids[name] = corpus.change_ids(path)

    thresholds = dict(DEFAULT_THRESHOLDS)
    deviations = []
    if args.config:
        if yaml is None:
            sys.exit("pyyaml required for --config")
        cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8")) or {}
        for key, value in sorted((cfg.get("thresholds") or {}).items()):
            if key not in thresholds:
                sys.exit(f"unknown threshold {key!r}")
            if thresholds[key] != value:
                deviations.append(
                    f"threshold {key}={value} (default {thresholds[key]})")
                thresholds[key] = value
    if args.single_repo:
        deviations.append(
            f"scope limited to single repo {repo_paths and repos[0][0]}")
    if args.family:
        deviations.append(f"scope limited to family {args.family}")
    if getattr(args, "routing_strict", False):
        deviations.append("ideation-routing strict organize/proposal mode "
                          "(referenced pinned repositories must materialize)")

    # Catalog root (T014): the aggregation checkout when one is in
    # scope; otherwise the one single-repo path, so a lone repo can
    # still carry its own health/document-catalog/ tree.
    catalog_root = agg_root if agg_root is not None else (
        repos[0][1] if len(repos) == 1 else None)

    ctx = Context(repo_paths=repo_paths, docs=docs,
                  capabilities=capabilities, change_ids=change_ids,
                  git=corpus.RealGit(), thresholds=thresholds,
                  as_of=date.fromisoformat(args.as_of),
                  agg_root=agg_root,
                  notebook_dryrun=_real_notebook_dryrun(agg_root),
                  catalog_root=catalog_root)
    ctx.deviations = deviations
    # add-cross-factory-ideation-routing task 4.3: nightly by default (an
    # unavailable external path is reported as skipped); strict organize/
    # proposal mode requires every referenced pinned repository to materialize.
    ctx.routing_strict = getattr(args, "routing_strict", False)
    return ctx


def _contained_cli_path(raw: str, root: Path, label: str) -> Path:
    """Resolve a workflow-supplied path inside its immutable checkout."""
    boundary = root.resolve()
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = boundary / candidate
    resolved = candidate.resolve()
    if not resolved.is_relative_to(boundary):
        raise SystemExit(f"{label} must stay inside {boundary}")
    return resolved


def _organizer_host(args):
    """The attested host descriptor for organizer source/host authorization
    (add-cross-factory-ideation-routing task 7.2). Requires all three boundary
    flags; absent any, returns None so authorization fails closed (spec
    "Missing readiness or authorization SHALL record a fail-closed skip without
    sending source content or identifying metadata")."""
    if (args.organizer_tenant_boundary and args.organizer_data_boundary
            and args.organizer_handling_class):
        return {"tenant_boundary": args.organizer_tenant_boundary,
                "data_boundary": args.organizer_data_boundary,
                "handling_classes": [args.organizer_handling_class]}
    return None


def run_suite(ctx, only_family: str | None, skip: set[str]) -> RunResult:
    result = RunResult()
    if only_family is None:
        pf_findings, pf_log = run_preflight(ctx.repo_paths)
        result.findings.extend(pf_findings)
        result.preflight = pf_log
    for family, fn in FAMILIES.items():
        if only_family and family != only_family:
            continue
        if family in skip:
            result.skips.append(Skip(family, "skipped by run configuration"))
            continue
        out = fn(ctx)
        if isinstance(out, Skip):
            result.skips.append(out)
        else:
            result.findings.extend(out)
    result.findings.sort(key=Finding.sort_key)
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="doc-health")
    scope = ap.add_mutually_exclusive_group(required=True)
    scope.add_argument("--repo-root", help="aggregation checkout")
    scope.add_argument("--single-repo", help="one repo (self-gate mode)")
    ap.add_argument("--family", choices=sorted(FAMILIES),
                    help="run one check family")
    ap.add_argument("--skip-family", action="append", default=[],
                    choices=sorted(FAMILIES), help="skip a family with notice")
    ap.add_argument("--as-of",
                    default=datetime.now(timezone.utc).date().isoformat(),
                    help="aging reference date (YYYY-MM-DD; default: today UTC)")
    ap.add_argument("--routing-strict", action="store_true",
                    help="ideation-routing: strict organize/proposal mode — "
                         "referenced pinned repositories must be materialized "
                         "(default: nightly, unavailable external paths are "
                         "reported as skipped)")
    ap.add_argument("--config", help="YAML threshold overrides")
    ap.add_argument("--report-out", help="write the report here")
    ap.add_argument("--previous-report",
                    help="previous report path for the regression diff")
    ap.add_argument("--new-findings-out",
                    help="write new critical/error regressions as JSON")
    ap.add_argument("--fail-on", choices=["critical", "error"],
                    help="exit 1 when findings at/above this severity exist")
    ap.add_argument("--emit-inventory",
                    help="write the doc inventory (JSON) here")
    ap.add_argument("--inventory-in",
                    help="deterministic inventory emitted by prepare; it "
                         "must exactly match this checkout")
    ap.add_argument("--previous-inventory",
                    help="previous inventory for the changed-docs diff")
    ap.add_argument("--semantic-sweep", action="store_true",
                    help="run the agentic semantic sweep after the "
                         "deterministic pass (non-fatal; failures are "
                         "recorded as skips)")
    ap.add_argument("--semantic-model", default=None,
                    help="pinned model id for the analysis worker")
    ap.add_argument("--semantic-prepare", metavar="DIR",
                    help="write the analysis worker's corpus bundle here "
                         "and exit (dispatch mode, prepare phase)")
    ap.add_argument("--semantic-findings-in", metavar="FILE",
                    help="merge a worker findings artifact instead of "
                         "invoking the worker (dispatch mode, merge phase)")
    ap.add_argument("--semantic-unavailable-reason",
                    help="auditable reason a dispatched findings artifact "
                         "is unavailable")
    ap.add_argument("--semantic-claude-bin", default="claude",
                    help=argparse.SUPPRESS)  # testability: fake worker binary
    ap.add_argument("--catalog-prepare", metavar="DIR",
                    help="write the document-cataloger's shard bundle here "
                         "and exit (dispatch mode, prepare phase)")
    ap.add_argument("--catalog-findings-in", metavar="FILE",
                    help="merge a validated cataloger recommendation "
                         "artifact instead of skipping (dispatch mode, "
                         "merge phase)")
    ap.add_argument("--catalog-unavailable-reason",
                    help="auditable reason a dispatched cataloger "
                         "recommendation is unavailable")
    ap.add_argument("--catalog-model", default=None,
                    help="pinned model id for the cataloger worker")
    ap.add_argument("--catalog-baseline", action="store_true",
                    help="force baseline-shard mode this run (an operator "
                         "escape hatch; baseline mode is otherwise "
                         "auto-detected from recorded completion state)")
    ap.add_argument("--catalog-scope", default=None,
                    help="optional manual incremental scope override (a "
                         "single repository)")
    ap.add_argument("--catalog-claude-bin", default="claude",
                    help=argparse.SUPPRESS)  # testability: fake worker binary
    # add-cross-factory-ideation-routing task 7.1-7.4: the ideation-organizer
    # dispatch lane (organizer_dispatch.py). Mirrors the cataloger's
    # prepare/merge CLI shape; dispatch-only (no inline fallback), so the
    # organizer worker's model call happens only in the artifact-only child.
    ap.add_argument("--organizer-prepare", metavar="DIR",
                    help="write the ideation-organizer's self-contained bundle "
                         "here and exit (dispatch mode, prepare phase)")
    ap.add_argument("--organizer-findings-in", metavar="FILE",
                    help="merge a validated organizer recommendation artifact "
                         "instead of skipping (dispatch mode, merge phase); "
                         "named after the dispatched job id")
    ap.add_argument("--organizer-unavailable-reason",
                    help="auditable reason a dispatched organizer "
                         "recommendation is unavailable (worker_unavailable, "
                         "child_queue_timeout, child_timeout, child_<conclusion>)")
    ap.add_argument("--organizer-model", default=None,
                    help="pinned model id for the organizer worker")
    ap.add_argument("--organizer-manual-idea", action="append", default=[],
                    metavar="XFI-YYYY-NNN",
                    help="manually request organizer review of a named Idea ID "
                         "(repeatable); serves the 'manual requests' trigger")
    ap.add_argument("--organizer-tenant-boundary", default=None,
                    help="attested host tenant boundary for organizer "
                         "source/host authorization (all three boundary flags "
                         "required, else dispatch/persist fails closed)")
    ap.add_argument("--organizer-data-boundary", default=None,
                    help="attested host data boundary for organizer "
                         "authorization")
    ap.add_argument("--organizer-handling-class", default=None,
                    help="attested host handling class for organizer "
                         "authorization")
    args = ap.parse_args(argv)

    ctx = build_context(args)

    if args.semantic_prepare:
        from . import semantic as _semantic
        # Dispatch preparation runs the deterministic pass first. If it
        # cannot complete and emit this inventory, no semantic bundle exists
        # and the artifact worker is never dispatched.
        run_suite(ctx, args.family, set(args.skip_family))
        inventory = _semantic.build_inventory(ctx.docs)
        prev_inv = None
        if args.previous_inventory:
            prev_inv = _semantic.load_previous(args.previous_inventory)
        bundle_root = ctx.agg_root or Path(args.single_repo).resolve()
        bundle_out = _contained_cli_path(
            args.semantic_prepare, bundle_root, "semantic bundle output")
        meta = _semantic.prepare_bundle(
            ctx.repo_paths, ctx.docs, ctx.as_of, prev_inv,
            bundle_out,
            model=args.semantic_model or _semantic.DEFAULT_MODEL,
            inventory=inventory, allowed_output_root=bundle_root)
        print(f"sweep bundle written: {args.semantic_prepare} "
              f"({meta['corpus_size']} docs; {meta['scope']})")
        return 0

    if args.catalog_prepare:
        from . import catalog_baseline as _catalog_baseline
        from . import catalog_dispatch as _catalog_dispatch
        from . import inventory as _cat_inventory
        # Deterministic-first, async-second (FR-001/FR-002): the full
        # 13-family suite (including the document-catalog family's own
        # structural checks) completes before the shard bundle is built and
        # the child would be dispatched — mirrors --semantic-prepare.
        run_suite(ctx, args.family, set(args.skip_family))
        cat_inv = _cat_inventory.build_inventory(
            ctx.docs, ctx.repo_paths, git=ctx.git)
        bundle_root = ctx.agg_root or Path(args.single_repo).resolve()
        bundle_out = _contained_cli_path(
            args.catalog_prepare, bundle_root, "catalog bundle output")
        catalog_root = ctx.catalog_root or bundle_root
        # --catalog-baseline is an explicit escape hatch (data-model.md);
        # absent it, normal baseline progress happens automatically across
        # scheduled runs until catalog_baseline.is_baseline_complete().
        baseline_mode = args.catalog_baseline or not \
            _catalog_baseline.is_baseline_complete(catalog_root)
        meta = _catalog_dispatch.prepare_catalog_bundle(
            ctx.repo_paths, ctx.docs, ctx.as_of, catalog_root, bundle_out,
            args.catalog_model or _catalog_dispatch.DEFAULT_MODEL,
            cat_inv, allowed_output_root=bundle_root,
            baseline_mode=baseline_mode, scope=args.catalog_scope)
        print(f"catalog bundle written: {args.catalog_prepare} "
              f"({meta['shard_count']} shard(s), "
              f"{meta['selection_count']} selected)")
        return 0

    if args.organizer_prepare:
        from . import ideation_routing as _ideation_routing
        from . import organizer_dispatch as _organizer_dispatch
        # Deterministic-first, async-second (task 7.1): the full fourteen-family
        # suite (including the deterministic ideation-routing family) completes
        # here BEFORE the organizer bundle is built and the child would be
        # dispatched — identical to --catalog-prepare / --semantic-prepare.
        run_suite(ctx, args.family, set(args.skip_family))
        records = _ideation_routing._collect(ctx)[0]
        bundle_root = ctx.agg_root or Path(args.single_repo).resolve()
        bundle_out = _contained_cli_path(
            args.organizer_prepare, bundle_root, "organizer bundle output")
        meta = _organizer_dispatch.prepare_organizer_bundle(
            records, ctx.repo_paths, ctx.as_of, bundle_out,
            args.organizer_model or _organizer_dispatch.DEFAULT_MODEL,
            allowed_output_root=bundle_root, git=ctx.git,
            manual_idea_ids=args.organizer_manual_idea,
            thresholds=ctx.thresholds, host=_organizer_host(args))
        print(f"organizer bundle written: {args.organizer_prepare} "
              f"({meta['idea_count']} idea(s) of {meta['dispatchable']} "
              f"dispatchable; {meta['authorized']} authorized, "
              f"{meta['authorization_denied']} denied)")
        return 0

    result = run_suite(ctx, args.family, set(args.skip_family))

    from dataclasses import replace as _replace
    from .families import FAMILY_RESOLUTION
    result.findings = [
        _replace(f, resolution=FAMILY_RESOLUTION.get(f.family, f.resolution))
        for f in result.findings]

    from . import semantic
    inventory = semantic.build_inventory(ctx.docs)
    inventory_error = None
    if args.inventory_in:
        try:
            inventory_root = ctx.agg_root or Path(args.single_repo).resolve()
            inventory_path = _contained_cli_path(
                args.inventory_in, inventory_root, "prepared inventory")
            prepared_inventory = json.loads(
                inventory_path.read_text(encoding="utf-8"))  # NOSONAR: contained
            if prepared_inventory != inventory:
                inventory_error = (
                    "prepared deterministic inventory does not match checkout")
            else:
                inventory = prepared_inventory
        except (OSError, json.JSONDecodeError):
            inventory_error = "prepared deterministic inventory is unreadable"
        if inventory_error and not args.semantic_findings_in:
            raise SystemExit(inventory_error)
    if args.emit_inventory:
        Path(args.emit_inventory).parent.mkdir(parents=True, exist_ok=True)
        Path(args.emit_inventory).write_text(
            json.dumps(inventory, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"inventory written: {args.emit_inventory}")

    semantic_meta = None
    if args.semantic_sweep or args.semantic_findings_in:
        prev_inv = None
        if args.previous_inventory:
            prev_inv = semantic.load_previous(args.previous_inventory)
        model = args.semantic_model or semantic.DEFAULT_MODEL

        if inventory_error:
            def _invoke(prompt, mdl):
                raise RuntimeError(inventory_error)
        elif args.semantic_findings_in:
            _invoke = semantic.findings_file_invoke(
                args.semantic_findings_in,
                unavailable_reason=args.semantic_unavailable_reason)
        else:
            def _invoke(prompt, mdl):
                return semantic.real_invoke(
                    prompt, mdl, claude_bin=args.semantic_claude_bin)

        sem_findings, semantic_meta = semantic.run_sweep(
            ctx.repo_paths, ctx.docs, ctx.as_of, ctx.agg_root, prev_inv,
            model=model, invoke=_invoke, inventory=inventory)
        result.findings.extend(sem_findings)
        result.findings.sort(key=Finding.sort_key)

    # Document-cataloger merge phase (--catalog-findings-in /
    # --catalog-unavailable-reason). Mirrors the semantic sweep's dispatch
    # gate exactly: engaged only when one of the two catalog flags is
    # present, so a plain run (no catalog CLI flags at all) never touches
    # catalog_dispatch — catalog_meta stays None and report.render()'s
    # placeholder section is skipped, just like semantic_meta today.
    catalog_meta = None
    if args.catalog_findings_in or args.catalog_unavailable_reason:
        from . import catalog_baseline as _catalog_baseline
        from . import catalog_dispatch
        from . import inventory as _cat_inventory
        cat_inv = _cat_inventory.build_inventory(
            ctx.docs, ctx.repo_paths, git=ctx.git)
        catalog_root = ctx.catalog_root or (
            ctx.agg_root or Path(args.single_repo).resolve())
        findings_path = None
        job_id = None
        if args.catalog_findings_in:
            findings_root = ctx.agg_root or Path(args.single_repo).resolve()
            findings_path = _contained_cli_path(
                args.catalog_findings_in, findings_root,
                "catalog recommendation artifact")
            # Convention: the merge-phase findings artifact is named after
            # the dispatched job id (mirroring cataloger.persist_
            # recommendations' <job-id>.yaml naming) so it can be recovered
            # from the filename alone across the prepare/finalize job
            # boundary, with no extra CLI flag needed for it.
            job_id = findings_path.stem
        # Same auto-detection as the prepare-phase branch above (recomputed
        # independently here since this may be a separate process/job in
        # the real two-job workflow topology — catalog_dispatch.py module
        # docstring); this call is the one that durably persists any
        # baseline advancement.
        baseline_mode = args.catalog_baseline or not \
            _catalog_baseline.is_baseline_complete(catalog_root)
        catalog_meta = catalog_dispatch.merge_catalog_findings(
            ctx.repo_paths, ctx.as_of, catalog_root,
            args.catalog_model or catalog_dispatch.DEFAULT_MODEL, cat_inv,
            job_id=job_id, findings_path=findings_path,
            unavailable_reason=args.catalog_unavailable_reason,
            scope=args.catalog_scope, baseline_mode=baseline_mode,
            thresholds=ctx.thresholds)

    # Ideation-organizer merge phase (--organizer-findings-in /
    # --organizer-unavailable-reason). Engaged only when one of the two
    # organizer flags is present, so a plain run (no organizer CLI flags at
    # all) never touches organizer_dispatch — organizer_meta stays None and
    # report.render()'s section is skipped, exactly like catalog_meta. The
    # deterministic pass above has already completed; this only decides whether
    # organizer EVIDENCE persists and how the report SUMMARIZES it (task 7.2).
    organizer_meta = None
    if args.organizer_findings_in or args.organizer_unavailable_reason:
        from . import ideation_routing as _ideation_routing
        from . import organizer_dispatch as _organizer_dispatch
        records = _ideation_routing._collect(ctx)[0]
        organizer_root = ctx.catalog_root or (
            ctx.agg_root or Path(args.single_repo).resolve())
        findings_path = None
        if args.organizer_findings_in:
            findings_root = ctx.agg_root or Path(args.single_repo).resolve()
            findings_path = _contained_cli_path(
                args.organizer_findings_in, findings_root,
                "organizer recommendation artifact")
        organizer_meta = _organizer_dispatch.merge_organizer_findings(
            records, ctx.repo_paths, ctx.as_of,
            args.organizer_model or _organizer_dispatch.DEFAULT_MODEL,
            git=ctx.git, evidence_root=organizer_root,
            findings_path=findings_path,
            unavailable_reason=args.organizer_unavailable_reason,
            manual_idea_ids=args.organizer_manual_idea,
            thresholds=ctx.thresholds, host=_organizer_host(args))

    previous_keys = previous_contested = None
    if args.previous_report and Path(args.previous_report).is_file():
        previous_keys, previous_contested = report.parse_previous(
            Path(args.previous_report).read_text(encoding="utf-8"))
    dispositions = set()
    dispo_path = (ctx.agg_root / "health" / "dispositions.yaml"
                  if ctx.agg_root else None)
    if dispo_path and dispo_path.is_file():
        import yaml as _yaml
        for d in (_yaml.safe_load(dispo_path.read_text()) or []):
            if isinstance(d, dict) and d.get("cite"):
                dispositions.add((d.get("family"), d.get("repo"),
                                  d.get("path")))
    unavailable_families = set()
    if semantic_meta is not None and semantic_meta.skipped_reason:
        unavailable_families.update(semantic.SEMANTIC_FAMILY_IDS)
    # The ideation-readiness lane's `contested` findings are folded into the
    # ranked plan AFTER this render (report.insert_readiness_section, from the
    # readiness merge step), so they are NEVER in `result.findings` at this
    # deterministic point. Without this exclusion, every prior report's
    # readiness finding would look "resolved without citation" here and become
    # an `uncited-resolution` ERROR — which the nightly then files as a
    # regression issue, violating the doc-health delta's "the lane MUST NOT
    # open regression issues in v1" (and "a finding absent only because the
    # lane did not run MUST NOT be treated as resolved"). The lane owns its own
    # findings' lifecycle; the deterministic pass never adjudicates them.
    from . import ideation_readiness as _ir
    unavailable_families.add(_ir.FAMILY_ID)
    result.findings += report.uncited_resolutions(
        result.findings, previous_contested, dispositions,
        unavailable_families=unavailable_families)
    new = report.regressions(result.findings, previous_keys)

    spec_words = 0
    for _, path in sorted(ctx.repo_paths.items()):
        for spec in corpus.promoted_spec_paths(path):
            spec_words += len(spec.read_text(encoding="utf-8").split())

    text = report.render(ctx.as_of, result.findings, result.skips,
                         result.preflight, ctx.docs, spec_words,
                         ctx.deviations, new, semantic_meta=semantic_meta,
                         catalog_meta=catalog_meta, organizer_meta=organizer_meta)
    if args.report_out:
        Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report_out).write_text(text, encoding="utf-8")
        print(f"report written: {args.report_out}")
    else:
        print(text)

    if args.new_findings_out:
        Path(args.new_findings_out).write_text(json.dumps(
            [f.__dict__ for f in new], indent=2, sort_keys=True) + "\n",
            encoding="utf-8")

    if args.fail_on:
        gate = {CRITICAL} if args.fail_on == "critical" else {CRITICAL, ERROR}
        if any(f.severity in gate for f in result.findings):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
