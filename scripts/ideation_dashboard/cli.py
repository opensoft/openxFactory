"""`generate` + (later) `generate-and-open` action subcommands (plan "cli.py";
change task 3.3).

Path-agnostic argparse front-end: `--output`-style arguments, no baked-in
snapshot path (the aggregation nightly lane wires the committed path). The
`generate` subcommand (this wave, T006) regenerates the deterministic snapshot
from the working tree, writes it through the interactivity boundary, and
validates it against the pinned openxFactory validator. The `generate-and-open`
subcommand (T012, US2) will layer `serve.py` + browser open on top of the same
generation path.

Runnable both as a module (`python3 -m ideation_dashboard.cli`) and as a script
(`python3 scripts/ideation_dashboard/cli.py`); it self-inserts `scripts/` onto
the import path so the sibling `doc_health` package resolves either way.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ideation_dashboard import authoring as authoring_mod  # noqa: E402
from ideation_dashboard import branch_session as branch_session_mod  # noqa: E402
from ideation_dashboard import gate_console as gate_mod  # noqa: E402
from ideation_dashboard import gate_routes as gate_routes_mod  # noqa: E402
from ideation_dashboard import human_seen as human_seen_mod  # noqa: E402
from ideation_dashboard import kickoff as kickoff_mod  # noqa: E402
from ideation_dashboard import serve as serve_mod  # noqa: E402
from ideation_dashboard import session_git as session_git_mod  # noqa: E402
from ideation_dashboard import session_pr as session_pr_mod  # noqa: E402
from ideation_dashboard import snapshot as snapshot_mod  # noqa: E402
from ideation_dashboard import workbench as workbench_mod  # noqa: E402
from ideation_dashboard.boundary import (  # noqa: E402
    HUMAN, BoundaryViolation, HumanGate, OutputBoundary,
)
from ideation_dashboard.corpus_root import (  # noqa: E402
    SCANNED_ROOTS, corpus_root_refusal,
)
from ideation_dashboard.generator import generate_snapshot  # noqa: E402

WEB_DIR = Path(__file__).resolve().parent / "web"

# The shape a correct invocation has, shown in the `--repo-root` refusal below.
# PLACEHOLDERS only — nobody's home directory and no container path belongs in a
# message whose whole job is to end a path-namespace confusion — and only flags
# this parser really accepts.
_GENERATE_SHAPE = (
    "python3 scripts/ideation_dashboard/cli.py generate-and-open \\\n"
    "  --repo-root <path to the corpus checkout> \\\n"
    "  --repository <that checkout's repository id>"
)


class RepoRootRefused(Exception):
    """`--repo-root` does not name a corpus checkout (`corpus_root.corpus_scan_defect`).

    Raised from the ONE shared generation chokepoint, BEFORE any scan and before
    the `OutputBoundary` write, so no snapshot file exists to be mistaken for a
    result; `main` reports it on stderr and exits non-zero. Carries the whole
    operator-facing refusal as its message."""


def _refuse_non_corpus_repo_root(args: argparse.Namespace) -> None:
    """Raise `RepoRootRefused` unless `--repo-root` could be a corpus checkout."""
    refusal = corpus_root_refusal(args.repo_root, shape=_GENERATE_SHAPE)
    if refusal is not None:
        raise RepoRootRefused(refusal)


def _generate_and_write(args: argparse.Namespace, output: Path) -> tuple[dict, Path]:
    """Generate the deterministic snapshot from the working tree and write it
    through the interactivity boundary (the output file is the whole declared
    allowlist, rooted at its own directory). Shared by `generate` and
    `generate-and-open`.

    A `--repo-root` that cannot be a corpus checkout is REFUSED here — the ONE
    guard both verbs pass through, ahead of the generation and the write, because
    an empty snapshot that exits 0 is indistinguishable from an honest one (T092;
    see `corpus_root.corpus_scan_defect`)."""
    _refuse_non_corpus_repo_root(args)
    repo_root = Path(args.repo_root).resolve()
    snapshot = generate_snapshot(
        repo_root,
        args.repository,
        source_revision=args.source_revision,
        project_register_source=Path(args.project_register).resolve() if args.project_register else None,
        possibles_source=Path(args.possibles).resolve() if args.possibles else None,
    )
    boundary = OutputBoundary(output.parent, [output.name])
    written = snapshot_mod.write_snapshot(snapshot, output, boundary)
    return snapshot, written


def _report(snapshot: dict, written: Path, repo_root: Path) -> None:
    stats = _stats(snapshot)
    print(f"wrote {written}")
    print(f"  repository={snapshot['repository']} "
          f"project={snapshot.get('project', '<ungrouped>')} "
          f"project_group={snapshot.get('project_group', '<none>')}")
    print(f"  source_revision={snapshot['generation']['source_revision']}")
    print(f"  documents={stats['documents']} clusters={stats['clusters']} "
          f"possibles={stats['possibles']} staged_topics={stats['staged_topics']} "
          f"changes={stats['changes']} keywords={stats['keyword_index']}")
    _warn_on_empty_projection(stats, repo_root)


def _warn_on_empty_projection(stats: dict[str, int], repo_root: Path) -> None:
    """A projection that produced ZERO documents WARNS loudly and does not fail.

    The decision, deliberately: an empty corpus is LEGAL — a fresh repository, a
    domain factory before its first document — and a hard failure here would make
    an honestly-empty tree unusable, which is a worse defect than the one being
    fixed. But the guard in `_generate_and_write` proves only that the tree COULD
    be scanned, not that it is the tree the human meant: a checkout whose
    `ideation/` exists but holds nothing passes it, and the dashboard then renders
    the same empty funnel it renders for an honest one, over copy that reads as a
    legitimate result. So the emptiness is stated on stderr, with the roots that
    let the path through, and the human decides."""
    if stats["documents"]:
        return
    present = ", ".join(f"{root}/" for root in SCANNED_ROOTS
                        if (repo_root / root).is_dir())
    print(f"  WARNING: ZERO documents were projected from {repo_root} — this "
          f"snapshot is EMPTY", file=sys.stderr)
    print(f"    it was accepted as a corpus checkout because it holds {present}, "
          f"but nothing under those roots produced a governed document",
          file=sys.stderr)
    print("    an empty corpus is legal, so this is a WARNING, not a failure — but "
          "the usual cause is a --repo-root naming the wrong tree, and the "
          "dashboard's empty funnel reads the same either way", file=sys.stderr)


def _locate_validator(written: Path, repo_root: Path) -> Path | None:
    """The pinned validator, searched from the OUTPUT path and then from the
    SERVED CHECKOUT (T092 acceptance sweep, defect 8).

    `snapshot.find_validator` walks UP from where it is started, and `_validate`
    started it only at the output file's directory. `generate-and-open` defaults
    its run dir to `tempfile.mkdtemp()`, so on the DOCUMENTED human launch the
    search began in /tmp, no ancestor there ever holds an aggregation checkout,
    and every such run printed "validation SKIPPED — no reachable openxFactory
    checkout" and served an unvalidated snapshot. SC-002's fail-loud validation
    therefore never fired for a real user, and the message blamed the one thing
    that WAS present: `--repo-root` is by definition the openxFactory checkout
    being rendered, and it carries the validator.

    The output path is still tried FIRST, so a run that deliberately writes
    beside a different aggregation checkout keeps using that one; `--repo-root`
    is the fallback that makes the ordinary launch validate."""
    return (snapshot_mod.find_validator(written.parent)
            or snapshot_mod.find_validator(repo_root))


def _warn_validator_not_found(written: Path, repo_root: Path) -> None:
    """VALIDATOR UNAVAILABLE, sub-case "nothing to run".

    NOT routine, and — now that `_locate_validator` falls back to `--repo-root`
    — no longer the ordinary launch's fate either. Both roots were searched, so
    the message names BOTH and blames neither on its own: reaching here means no
    aggregation checkout is reachable from the OUTPUT path OR from the served
    checkout, and the snapshot went unvalidated however good the corpus was. The
    old one-liner ("no reachable openxFactory checkout") read as routine while
    quietly meaning "unvalidated", and pointed at a checkout that was present and
    fine — which is exactly where it sent the T092 pass."""
    print("  validation SKIPPED — this snapshot was NOT checked against the "
          "pinned schema", file=sys.stderr)
    print(f"    no {snapshot_mod.VALIDATOR_RELPATH} exists above "
          f"{written.parent} (the OUTPUT path, searched first) or above "
          f"{repo_root} (--repo-root, the fallback)", file=sys.stderr)
    print("    render a checkout that sits inside an aggregation checkout, "
          "or write the snapshot into one (--output on generate, --run-dir "
          "on generate-and-open), to have it validated", file=sys.stderr)


def _warn_validator_could_not_run(result) -> None:
    """VALIDATOR UNAVAILABLE, sub-case "found it, could not run it".

    The validator's OWN words are relayed verbatim rather than paraphrased: it
    is the thing that knows which dependency it wanted, and quoting it keeps
    this warning correct when that message changes. What we add is the part it
    cannot know — WHICH interpreter it was run under (a separate `sys.executable`
    process, so the libraries have to exist wherever the dashboard runs, not
    wherever openxFactory is developed), the remedy, and the reassurance that
    the corpus is not the accused."""
    print("  validation SKIPPED — this snapshot was NOT checked against the "
          "pinned schema", file=sys.stderr)
    print(f"    the validator was found ({result.validator}) but could not run: "
          f"{result.unavailable_reason}", file=sys.stderr)
    for line in (result.stderr or result.stdout).strip().splitlines()[-10:]:
        print(f"      {line}", file=sys.stderr)
    print(f"    it runs under {sys.executable} — a SEPARATE interpreter from "
          f"whatever installed openxFactory — and the usual cause is that this "
          f"one lacks its libraries. Remedy:", file=sys.stderr)
    print(f"      {sys.executable} -m {snapshot_mod.DEPENDENCY_REMEDY}",
          file=sys.stderr)


def _report_non_conformance(written: Path, result) -> None:
    """NOT CONFORMANT — the validator ran, reached a verdict, and rejected the
    snapshot. The one thing this message must never be mistaken for is the
    warning above it, so it says whose fault it is out loud and prints the
    findings themselves; "1 error(s)" alone told a human nothing he could act
    on."""
    print(f"  validation FAILED — the pinned validator REJECTED {written}. This "
          f"is the SNAPSHOT, not the environment: the validator ran fine and "
          f"found the data non-conformant.", file=sys.stderr)
    for line in (result.stdout or result.stderr).strip().splitlines()[-20:]:
        print(f"    {line}", file=sys.stderr)


def _validate(written: Path, args: argparse.Namespace, *,
              continues: str = "this command continues and exits 0") -> int:
    """Post-render validation, with THREE outcomes (see `snapshot.VALIDATED`).

    A snapshot the validator REJECTS still fails the command. A validator that
    could not RUN warns loudly and returns 0 — for `generate-and-open` because a
    human who cannot start his dashboard because his laptop lacks a python
    library has been handed a worse problem than the one the check guards
    against, and for plain `generate` for the same reason plus symmetry: the
    file is written either way, the environment is what failed, and one policy
    across both verbs is one thing to explain. `--strict` overrides that in both
    — asking for strictness and getting "we skipped the check" would make the
    flag a lie. `validate_or_raise` is untouched and still raises: that is the
    generator's deliberate fail-loud path, and it is chosen by code, not by a
    human waiting on a browser tab."""
    if args.no_validate:
        print("  validation skipped (--no-validate)")
        return 0
    repo_root = Path(args.repo_root).resolve()
    validator = _locate_validator(written, repo_root)
    result = snapshot_mod.validate_snapshot(written, strict=args.strict,
                                            validator=validator)
    if not result.available:
        if result.validator is None:
            _warn_validator_not_found(written, repo_root)
        else:
            _warn_validator_could_not_run(result)
        if args.strict:
            print("    --strict was given and it means what it says: a run that "
                  "COULD NOT be validated FAILS rather than continuing "
                  "unchecked", file=sys.stderr)
            return 1
        print(f"    this is the ENVIRONMENT, not the snapshot — nothing here "
              f"says the corpus is wrong, only that no one checked it, so "
              f"{continues}", file=sys.stderr)
        return 0
    if not result.ok:
        _report_non_conformance(written, result)
        return 1
    print(f"  validation: {result.summary()}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    output = Path(args.output).resolve()
    snapshot, written = _generate_and_write(args, output)
    _report(snapshot, written, Path(args.repo_root).resolve())
    return _validate(written, args,
                     continues="the snapshot file stands and this command "
                               "exits 0")


def cmd_generate_and_open(args: argparse.Namespace, *, opener=webbrowser.open) -> int:
    """Regenerate the snapshot from the working tree into a run dir, start the
    local server, print the URL (ALWAYS), and open the browser. `--no-open`
    suppresses the browser; `--no-serve` returns after printing the URL without
    blocking (used by tests). `opener` is injectable for testing."""
    # Ahead of minting the run dir, so a refused root leaves not even an empty
    # temp directory behind. `_generate_and_write` is still the guard that MATTERS
    # (it is the one no caller can skip); this is the same check, earlier.
    _refuse_non_corpus_repo_root(args)
    run_dir = Path(args.run_dir).resolve() if args.run_dir else Path(
        tempfile.mkdtemp(prefix="ideation-dashboard-"))
    run_dir.mkdir(parents=True, exist_ok=True)
    output = run_dir / "snapshot.json"

    checkout_root = Path(args.repo_root).resolve()
    snapshot, written = _generate_and_write(args, output)
    _report(snapshot, written, checkout_root)
    # A validator that could not RUN warns and returns 0 here — the server
    # starts. Only a snapshot the validator actually REJECTED (or --strict)
    # returns non-zero and stops before `build_server`.
    rc = _validate(written, args,
                   continues="the dashboard SERVES this unchecked snapshot")
    if rc != 0:
        return rc

    httpd = serve_mod.build_server(WEB_DIR, written, checkout_root,
                                   host=args.host, port=args.port,
                                   actor=getattr(args, "actor", None),
                                   # the ENTRYPOINT declares the real notebook
                                   # adapter; `build_server` never reaches for one
                                   # on a caller's behalf (PR #49 hardening item 1)
                                   adapter_factory=serve_mod.real_notebook_adapter)
    url = serve_mod.server_url(httpd, "/index.html")
    print(f"  serving {url}")
    print(f"  snapshot {serve_mod.server_url(httpd, '/snapshot.json')}")
    print(url)  # the URL is ALWAYS printed on its own line

    if not args.no_open:
        try:
            opener(url)
        except Exception as exc:  # a headless box has no browser — never fatal
            print(f"  (could not open a browser: {exc}; open the URL above manually)")

    if args.no_serve:
        httpd.server_close()
        return 0

    print("  serving until interrupted (Ctrl-C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


def cmd_create(args: argparse.Namespace, *, launcher=subprocess.Popen) -> int:
    """The human create action (US8/T030): scaffold a header-compliant doc into
    `--area` and, unless `--no-open`, launch the human's editor over it. The
    write is `authoring.create_scaffold`'s one `boundary.create_document` call
    (create-only — an existing target refuses); this command performs no
    further mutation itself.

    `--area` goes through the SAME confinement the gated create uses
    (`authoring.area_refusal` — inside `ideation/`, never inside the gate-records
    prefix). This verb records nothing and opens no session, but it writes into the
    SERVED checkout directly, so a document it drops into the records prefix would
    sit in exactly the blind spot SC-002's fingerprint excludes (PR #49 wave-2
    critic). One definition, every create path."""
    repo_root = Path(args.repo_root).resolve()
    refusal = authoring_mod.area_refusal(args.area)
    if refusal is not None:
        print(f"create refused: {refusal}", file=sys.stderr)
        return 1
    boundary = OutputBoundary(repo_root, actor=HUMAN)
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    written = authoring_mod.create_scaffold(
        boundary, area=args.area, title=args.title, summary=args.summary,
        topics=topics, repository_context=args.repository_context,
        kind=args.kind, possible_feats=args.possible_feat,
    )
    rel = written.relative_to(repo_root).as_posix()
    print(f"wrote {rel}")
    print(written)
    if args.no_open:
        return 0
    argv = authoring_mod.edit_command(repo_root, rel, editor=args.editor)
    try:
        launcher(argv)
    except Exception as exc:  # no editor/opener available — never fatal
        print(f"  (could not launch an editor: {exc}; open {written} manually)")
    return 0


def cmd_edit(args: argparse.Namespace, *, launcher=subprocess.Popen) -> int:
    """Select-to-edit (US8/T030): launch the human's editor over any listed
    document. Read-only from the dashboard's side — `edit_target` only
    resolves the path; the dashboard itself modifies nothing."""
    repo_root = Path(args.repo_root).resolve()
    path = authoring_mod.edit_target(repo_root, args.path)
    print(path)
    if args.no_open:
        return 0
    argv = authoring_mod.edit_command(repo_root, args.path, editor=args.editor)
    try:
        launcher(argv)
    except Exception as exc:  # no editor/opener available — never fatal
        print(f"  (could not launch an editor: {exc}; open {path} manually)")
    return 0


# ---- gate console (US9): human-only executable gate actions ----------------
# Human identity is `--actor`; hardening that identity (authn) is the xForge
# host's concern (change section 4), not this local CLI. Every action
# constructs a `HumanGate` (the distinct human-only entrypoint) — there is no
# machinery/agent code path to a gate action here.

def _gate_snapshot(args: argparse.Namespace) -> tuple[Path, dict]:
    """Regenerate the snapshot the gate action plans against (the same
    deterministic generation the dashboard reads)."""
    repo_root = Path(args.repo_root).resolve()
    snapshot = generate_snapshot(
        repo_root, args.repository, source_revision=args.source_revision,
        project_register_source=Path(args.project_register).resolve() if args.project_register else None,
        possibles_source=Path(args.possibles).resolve() if args.possibles else None)
    return repo_root, snapshot


def _human_gate(repo_root: Path, args: argparse.Namespace) -> HumanGate:
    return HumanGate(repo_root, [args.records_dir], human_actor=args.actor)


def cmd_gate_demote(args: argparse.Namespace) -> int:
    """Reject / move a proposal back to staging — the mechanized reverse
    transition. Records the transition manifest, the executable plan, the
    register-update note, and the gate-action record; with `--execute` it also
    applies the moves to this checkout (the human-driven transition)."""
    repo_root, snapshot = _gate_snapshot(args)
    console = gate_mod.GateConsole(_human_gate(repo_root, args), records_dir=args.records_dir)
    res = console.demote(snapshot, args.change_id, reason=args.reason,
                         staging_topic=args.staging_topic,
                         provenance=cli_provenance())
    print(f"demote {args.change_id} → staging topic {res.plan.staging_topic!r} (by {args.actor})")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  transition manifest: {res.manifest_path.relative_to(repo_root)}")
    print(f"  executable plan:     {res.plan_path.relative_to(repo_root)}")
    print(f"  register-update:     {res.register_update_path.relative_to(repo_root)}")
    print(f"  planned moves: {len(res.plan.moves)}; withdrawn picks: {list(res.plan.withdrawn_picks)}")
    if args.execute:
        ex = gate_mod.execute_demotion_plan(res.plan, repo_root)
        print(f"  EXECUTED: {len(ex.moved)} file(s) moved into {res.plan.topic_path}/openspec/; "
              f"README+INDEX updated; change folder removed={ex.removed_change_folder}")
    else:
        print("  (plan only — rerun with --execute to apply the moves to this checkout)")
    return 0


def cmd_gate_ratify(args: argparse.Namespace) -> int:
    """Approve a proposal: write the ratification record (ratifier, date) + a
    register-update note; the gate-action record carries the ratification-record
    reference (schema contains-rule)."""
    repo_root = Path(args.repo_root).resolve()
    console = gate_mod.GateConsole(_human_gate(repo_root, args), records_dir=args.records_dir)
    res = console.ratify(args.change_id, args.ratifier or args.actor, date=args.date,
                         provenance=cli_provenance())
    print(f"ratify {args.change_id} (ratifier {res.ratification['ratifier']}, {res.ratification['date']})")
    print(f"  gate-action record:  {res.record_path.relative_to(repo_root)}")
    print(f"  ratification record: {res.ratification_path.relative_to(repo_root)}")
    print(f"  register-update:     {res.register_update_path.relative_to(repo_root)}")
    return 0


def _commission_cli(verb: str, args: argparse.Namespace, target: str,
                    **engine_kwargs) -> int:
    """The shared half of the three wheel-verb subcommands (011).

    Terminal parity with the executing routes: same console facade, same
    engine, same guards. The CLI adds nothing of its own except the printing —
    which is exactly what makes the two surfaces equivalent."""
    repo_root = Path(args.repo_root).resolve()
    console = gate_mod.GateConsole(_human_gate(repo_root, args),
                                   records_dir=args.records_dir)
    try:
        res = getattr(console, verb.replace("-", "_"))(
            target, outline=args.outline, workflow=args.workflow,
            note=args.note, provenance=cli_provenance(), **engine_kwargs)
    except gate_mod.GateRefused as exc:
        print(f"{verb} refused: {exc}", file=sys.stderr)
        return 1
    print(f"{verb} {target} \u2192 workflow {res.job['workflow']!r} "
          f"(status {res.job['status']}, by {args.actor})")
    print(f"  workflow-job:       {res.job_path.relative_to(repo_root)}")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    return 0


def cmd_gate_promote_to_staging(args: argparse.Namespace) -> int:
    """Commission the organization of an ACCEPTED possible into a staging
    fragment. Refuses (exit 1) an absent register id, a possible that is not
    promotable, and a duplicate undelivered commission. Writes NOTHING to the
    possibles register: the pick edge lands when the fragment is delivered."""
    return _commission_cli("promote-to-staging", args, args.possible_id,
                           topic=args.topic)


def cmd_gate_research_brief(args: argparse.Namespace) -> int:
    """Commission a pre-verdict evidence brief for a possible. Legal while the
    possible is undisposed AND after — the engine carries no state guard
    (FR-018a); it never disposes the possible or edits its entry."""
    return _commission_cli("research-brief", args, args.possible_id)


def cmd_gate_derive_possibles(args: argparse.Namespace) -> int:
    """Commission a cluster-scoped run of the ratified derivation lane. The
    cluster is validated against the SNAPSHOT (hence the snapshot args); the
    console derives nothing and creates no register entry."""
    repo_root, snapshot = _gate_snapshot(args)
    args.repo_root = str(repo_root)
    return _commission_cli("derive-possibles", args, args.cluster_id,
                           snapshot=snapshot)


def cmd_gate_dispose_possible(args: argparse.Namespace) -> int:
    """Dispose a pending_review ai-derived possible: the ONE human verdict the
    derivation lane's whole contract funnels toward. Writes the updated index
    (validated by the pinned validator BEFORE persistence), its `.md`
    projection, and the gate-action record. `--repo-root` is the pinned
    openxFactory checkout (where `ideation/cross-reference.yaml` lives)."""
    from doc_health import derive_possibles as dp
    repo_root = Path(args.repo_root).resolve()
    gate = HumanGate(
        repo_root,
        [args.records_dir, dp.INDEX_REL, dp.INDEX_MD_REL],
        human_actor=args.actor)
    console = gate_mod.GateConsole(gate, records_dir=args.records_dir)
    res = console.dispose_possible(
        args.possible_id, args.outcome, reason=args.reason,
        citation=args.citation, note=args.note, provenance=cli_provenance())
    entry = res.entry
    print(f"dispose-possible {res.possible_id} -> {res.outcome} "
          f"(state {entry.get('state')}, origin {entry.get('origin')})")
    print(f"  index:              {res.index_path.relative_to(repo_root)}")
    if res.index_md_path:
        print(f"  index projection:   {res.index_md_path.relative_to(repo_root)}")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print("  (commit + push the openxFactory checkout to publish; the next")
    print("   snapshot regeneration folds the disposition into the dashboard)")
    return 0


def cmd_gate_edit_apply(args: argparse.Namespace) -> int:
    """Apply a HUMAN-approved redline to a change document. The redline is read
    from files (never re-authored here) so the console applies exactly what the
    human supplies."""
    repo_root = Path(args.repo_root).resolve()
    if args.full_text_file:
        redline = gate_mod.Redline(
            full_text=Path(args.full_text_file).read_text(encoding="utf-8"), concept=args.concept)
    elif args.old_file and args.new_file:
        redline = gate_mod.Redline(
            old_text=Path(args.old_file).read_text(encoding="utf-8"),
            new_text=Path(args.new_file).read_text(encoding="utf-8"), concept=args.concept)
    else:
        print("edit-apply requires either --full-text-file or both --old-file and --new-file", file=sys.stderr)
        return 2
    console = gate_mod.GateConsole(_human_gate(repo_root, args), records_dir=args.records_dir)
    res = console.edit_apply(args.change_id, args.document, redline,
                             tree_root=repo_root, provenance=cli_provenance())
    print(f"edit-apply {args.document} ({redline.form()}) by {args.actor}")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  redline artifact:   {res.redline_path.relative_to(repo_root)}")
    return 0


def cmd_gate_propose(args: argparse.Namespace) -> int:
    """Commission proposal authoring for a staging topic (add-propose-verb):
    the recorded workflow-job dispatch + gate-action record. Refuses (exit 1)
    a missing topic, a duplicate undelivered commission, a topic that is not
    `ready`, and — 007-workbench-branch-sessions T054, FR-023 — a tile whose BRANCH
    SESSION is still live. The authoring runs externally and lands as an ordinary
    OpenSpec change.

    The session refusal needs a registry, and a CLI verb is a FRESH PROCESS whose
    registry starts empty, so this re-derives it through `_session_registry`
    (T033a) before asking: without that, a CLI `propose` would proceed over
    unmerged drafts, which is the exact hazard D15 exists to prevent."""
    repo_root = Path(args.repo_root).resolve()
    console = gate_mod.GateConsole(_human_gate(repo_root, args), records_dir=args.records_dir)
    # The registry key's repository half, through the SAME derivation the session
    # verbs use (`_session_repository_key`) — this verb only READS liveness, but it
    # has to read it under the key the session was opened with or FR-023's refusal
    # simply does not fire.
    repository = _session_repository_key(repo_root, args)
    try:
        res = console.propose(
            args.topic_id, outline=args.outline, workflow=args.workflow,
            note=args.note,
            session_precondition=gate_routes_mod.session_precondition_for(
                _session_registry(repo_root, repository), repository=repository,
                topic_id=args.topic_id,
                tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root)),
            provenance=cli_provenance())
    except branch_session_mod.SessionRefused as exc:   # a live branch session
        print(f"propose refused: {exc.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"propose refused: {exc}", file=sys.stderr)
        return 1
    print(f"propose {args.topic_id} → workflow {res.job['workflow']!r} "
          f"(status {res.job['status']}, by {args.actor})")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  workflow-job:       {res.job_path.relative_to(repo_root)}")
    return 0


def cmd_gate_kickoff(args: argparse.Namespace) -> int:
    """Dispatch a ratified change's next step as a recorded, gated workflow job.
    Refuses (exit 1) a change with no recorded ratification (D17). The workflow
    itself runs externally; this records the dispatch descriptor only."""
    repo_root, snapshot = _gate_snapshot(args)
    console = gate_mod.GateConsole(_human_gate(repo_root, args), records_dir=args.records_dir)
    try:
        res = console.kickoff(args.change_id, snapshot=snapshot,
                              outline=args.outline, workflow=args.workflow,
                              provenance=cli_provenance())
    except gate_mod.GateRefused as exc:
        print(f"kickoff refused: {exc}", file=sys.stderr)
        return 1
    print(f"kickoff {args.change_id} → workflow {res.job['workflow']!r} "
          f"(status {res.job['status']}, by {args.actor})")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  workflow-job:       {res.job_path.relative_to(repo_root)}")
    return 0


# ---- lens gate verbs (add-lens-gate-verbs): human-only recipe dispatches ----

def _parse_pairs(pairs: list[str], flag: str) -> dict[str, str]:
    """`document=reason` overrides from repeatable flags. Refuses a bare
    `document` (the reasoned-override guard's terminal reason lives in the
    engine, but a CLI include/exclude with no reason is a usage error)."""
    out: dict[str, str] = {}
    for raw in pairs or []:
        doc, sep, reason = raw.partition("=")
        if not sep or not doc.strip() or not reason.strip():
            raise SystemExit(f"{flag} expects document=reason (got {raw!r})")
        out[doc.strip()] = reason.strip()
    return out


def _lens_gate(repo_root: Path, args: argparse.Namespace) -> HumanGate:
    """A HumanGate whose allowlist admits BOTH the records dir and the gitignored
    workbench tree (manifest + cross-reference queue live under WORKBENCH_DIR)."""
    return HumanGate(repo_root, [args.records_dir, workbench_mod.WORKBENCH_DIR],
                     human_actor=args.actor)


def cmd_gate_lens_save_recipe(args: argparse.Namespace) -> int:
    """Save a keyword-lens recipe as a gitignored workbench manifest through the
    gate — the same recorded dispatch the dashboard's execute button posts. The
    recipe is re-evaluated against the freshly generated snapshot; the reasoned-
    override guard, duplicate-name refusal, and schema validation all fire in
    the engine and surface here (exit 1)."""
    repo_root, snapshot = _gate_snapshot(args)
    try:
        result = gate_routes_mod.execute_lens_save_recipe(
            _lens_gate(repo_root, args),
            repository=args.repository, name=args.name,
            checked=list(args.checked), pinned=list(args.pinned or []),
            snapshot=snapshot,
            includes=_parse_pairs(args.include, "--include"),
            excludes=_parse_pairs(args.exclude, "--exclude"),
            records_dir=args.records_dir, provenance=cli_provenance())
    except (workbench_mod.WorkbenchError, workbench_mod.ManifestInvalid) as exc:
        print(f"lens-save-recipe refused: {exc}", file=sys.stderr)
        return 1
    print(f"lens-save-recipe {args.name!r} → {result['members']} member(s) (by {args.actor})")
    print(f"  manifest:           {result['manifest']}")
    print(f"  gate-action record: {result['record']}")
    return 0


def cmd_gate_lens_add_as_cluster(args: argparse.Namespace) -> int:
    """Add a keyword-lens set as a cluster: the recipe-seeded manifest PLUS the
    pending_review human-seen submission into the cross-reference queue. The
    evidence contract is enforced BEFORE persistence; the generated index is
    never written (acceptance stays a governed human edit)."""
    repo_root, snapshot = _gate_snapshot(args)
    submission = human_seen_mod.HumanSeenSubmission(
        proposer=args.proposer or args.actor,
        repository=args.evidence_repository or args.repository,
        path=args.evidence_path or "",
        revision=args.revision or "",
        section=args.section or "",
        passage_sha256=args.passage_sha256 or "",
        rationale=args.rationale or "",
        confidence=args.confidence,
        alternatives=list(args.alternative or []),
        recipe_reference=args.recipe_reference)
    try:
        result = gate_routes_mod.execute_lens_add_as_cluster(
            _lens_gate(repo_root, args),
            repository=args.repository, name=args.name,
            checked=list(args.checked), pinned=list(args.pinned or []),
            snapshot=snapshot,
            includes=_parse_pairs(args.include, "--include"),
            excludes=_parse_pairs(args.exclude, "--exclude"),
            submission=submission, records_dir=args.records_dir,
            provenance=cli_provenance())
    except (human_seen_mod.SubmissionRefused, human_seen_mod.SubmissionInvalid,
            workbench_mod.WorkbenchError, workbench_mod.ManifestInvalid) as exc:
        print(f"lens-add-as-cluster refused: {exc}", file=sys.stderr)
        return 1
    print(f"lens-add-as-cluster {args.name!r} → cluster {result['cluster_id']} (by {args.actor})")
    print(f"  manifest:           {result['manifest']}")
    print(f"  pending entry:      {result['pending_entry']}")
    print(f"  gate-action record: {result['record']}")
    return 0


def _session_registry(checkout_root: Path, repository: str | None):
    """A registry for THIS process, with the live sessions RE-DERIVED
    (007-workbench-branch-sessions T033a; FR-008, D10, G13).

    Every CLI verb is its own process and `SnapshotRegistry._entries` is an
    in-process dict, so a verb starts with NO session entries at all. The
    BOOTSTRAP is what makes liveness survive that boundary: it re-registers every
    worktree under the sessions container WHOSE BRANCH STILL EXISTS, reading the
    two signals jointly, so a CLI create on a tile that already has a session JOINS
    it, `propose` cannot proceed over unmerged drafts, and the resume-or-new prompt
    cannot re-fire mid-session.

    Half-signals are REPORTED, never repaired: a worktree with no branch (crash
    residue) and a branch with no worktree (an abandoned session) each print their
    own remedy on stderr, and this function deletes nothing.

    This is the ONE place a CLI verb obtains a registry — every session-bearing
    verb this feature adds goes through it."""
    from ideation_dashboard.snapshot_registry import SnapshotRegistry

    registry = SnapshotRegistry()
    report = branch_session_mod.bootstrap_sessions(
        registry, repository=repository or "", checkout_root=Path(checkout_root))
    for note in report.stale:
        print(f"  session note ({note.kind}): {note.reason}", file=sys.stderr)
    for message in report.errors:
        print(f"  session note: {message}", file=sys.stderr)
    return registry


def _session_repository_key(repo_root: Path, args: argparse.Namespace) -> str:
    """The registry/notebook key's repository half, for EVERY session verb — one
    derivation, in one place (007-workbench-branch-sessions FR-005/R7).

    `--repository`, else the checkout directory's name: the `<repo>` beside
    `<repo>-worktrees/` convention `branch_session.container_root` already relies
    on. The registry is per-PROCESS, so within one verb any value at all is
    self-consistent — which is exactly what made the divergence invisible.

    THE NOTICE (PR #49 review finding 8, leg b, wave 2). Nothing on disk records
    which value a session was opened under: the worktree path comes from the
    CHECKOUT and the branch from the TILE, so the key survives only as long as the
    process. Its one cross-process artifact is the session's NotebookLM alias,
    which is derived from it — so `create-document --repository MedxFactory` in an
    `openxFactory` checkout, then an `abandon-session` with no flag, retires an
    alias that was never created and ORPHANS the real notebook on the shared
    account (reproduced; before wave 2 the ending also REPORTED it retired, which
    `workbench._delete_titled` no longer does). A flag whose value must be repeated
    to be correct must say so, and it says so HERE, where every verb derives it,
    rather than in five docstrings. Not a refusal: the flag's declared purpose is a
    checkout directory named something other than the repository, and refusing that
    would remove the use case instead of the silence."""
    named = str(getattr(args, "repository", None) or "").strip()
    derived = repo_root.name
    if named and named != derived:
        print(f"  session note:       --repository {named!r} is not this "
              f"checkout's directory name {derived!r}. The key is not recorded "
              "anywhere, so EVERY verb of this session must pass the same "
              f"--repository {named!r}; one that does not derives a different "
              "notebook alias and leaves this session's notebook orphaned "
              "(FR-037).", file=sys.stderr)
    return named or derived


def _notebook_port(repo_root: Path):
    """The session notebook adapter for a CLI verb (T074; FR-036, FR-021, D16).

    A CLI verb is unambiguously LOCAL — a human at a shell in their own checkout —
    so it declares the real `nlm`-backed adapter and does not consult a capability
    probe the way `serve.py` must. The adapter DEGRADES on its own when `nlm` is
    absent (`available()` False, every action `skipped`), so this is safe to
    declare unconditionally: the session opens either way, and the FR-042 notice
    carries the reason.

    A named seam purely so a test injects `FakeNotebookAdapter`: no test may create
    a real notebook (FR-043)."""
    from ideation_dashboard import workbench as wb_mod

    return wb_mod.NotebookAdapter()


def _unwind_cli_session(verb: str, session, git, repo_root: Path,
                        message: str) -> int:
    """Print a CLI session refusal, having first undone a session THIS
    invocation opened (PR #49 review finding 3).

    The CLI half of the route's `_unwound`: same rule, same helper
    (`branch_session.unwind_opened_session`), so the two surfaces cannot diverge
    on what a refused first create leaves behind (FR-020). A JOIN is never
    unwound, a branch carrying gate-action commits is never deleted, and
    whatever the unwind could not remove is printed rather than swallowed."""
    notes = ()
    if session is not None and git is not None:
        notes = branch_session_mod.unwind_opened_session(
            git, session, checkout_root=repo_root)
    print(f"{verb} refused: {message}", file=sys.stderr)
    for note in notes:
        print(f"  session note:       {note}", file=sys.stderr)
    return 1


def cmd_gate_create_document(args: argparse.Namespace) -> int:
    """Create a NEW header-compliant ideation document through the GATE
    (add-workbench-bullseye-and-create) — the same recorded human dispatch the
    workbench's create dialog posts, driving the same tested authoring scaffold
    and writing the same gate-action record. Distinct from the non-gated
    `create` subcommand, which scaffolds + opens an editor and records nothing.
    Create-only: an existing target refuses (exit 1) and is never overwritten.

    With `--scope-kind` / `--scope-id` (007-workbench-branch-sessions T023a) the
    create resolves the tile's BRANCH SESSION first: the document and its record
    land in the session worktree and are committed together as that action's ONE
    commit, and the resulting sha is printed rather than written into the record.
    Without them, the behaviour is exactly what it was.

    FR-019 is a PER-VERB obligation here, and this verb is where it was missing:
    `create-document` was the ONE session subcommand that skipped
    `_session_identity_gate`, so a blank `--actor` reached `HumanGate` inside the
    try and died with an UNCAUGHT `ValueError` traceback — after the session had
    already been opened (PR #49 review finding 3). The gate now runs FIRST, ahead
    of the registry bootstrap and ahead of any resolution, exactly as every other
    session verb's does.

    The BODY is validated by the route's own `parse_create_document_body`, not by
    a second CLI-shaped approximation: the two surfaces drive the same engine, so
    an `--area` the HTTP route refuses must not be committable here."""
    repo_root = Path(args.repo_root).resolve()
    refused = _session_identity_gate("create-document", repo_root, args)
    if refused is not None:
        return refused
    scope_kind = getattr(args, "scope_kind", None)
    scope_id = getattr(args, "scope_id", None)
    if bool(scope_kind) != bool(scope_id):
        print("create-document refused: --scope-kind and --scope-id are given "
              "together or not at all — one without the other names no tile, so "
              "no branch session can be resolved from it", file=sys.stderr)
        return 1
    parsed, message = gate_routes_mod.parse_create_document_body({
        "area": args.area, "title": args.title, "summary": args.summary,
        "topics": [t.strip() for t in (args.topics or "").split(",") if t.strip()],
        "repository_context": args.repository_context, "kind": args.kind,
        "status": args.status, "source": args.source,
        "possible_feats": list(args.possible_feat or []),
        "scope_kind": scope_kind, "scope_id": scope_id,
        "continuation": getattr(args, "continuation", None),
    })
    if message is not None:
        print(f"create-document refused: {message}", file=sys.stderr)
        return 1
    parsed.pop("_scope", None)
    continuation = parsed.pop("_continuation", None)
    session = git = None
    # The registry/notebook key, through the ONE derivation every session verb
    # uses (`_session_repository_key`). It is NOT `--repository-context`, which is
    # a document header field: keying the open off a header value made
    # `create-document` disagree with the verbs that end the session it opened (PR
    # #49 review finding 8, leg b).
    repository = _session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (scope_kind, scope_id), checkout_root=repo_root,
            registry=(_session_registry(repo_root, repository)
                      if scope_kind else None),
            repository=repository,
            records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="create-document",
            # the human's answer to the FR-025 resume-or-new report, when they have
            # been shown it (T056); absent, a surviving abandoned branch reports the
            # choice instead of having one made for it
            continuation=continuation,
            # the ONE verb that can open a session carries the notebook adapter
            # (T074, FR-036) — the notebook itself is created by the first
            # SUCCESSFUL commit, never by the open (finding 3)
            notebook=_notebook_port(repo_root) if scope_kind else None)
        gate_root = session.worktree if session is not None else repo_root
        result = gate_routes_mod.execute_create_document(
            HumanGate(gate_root, [args.records_dir], human_actor=args.actor),
            records_dir=args.records_dir, session=session, git=git,
            # THE GATEWAY FACT (D23): surface `cli`, and the proof
            # `_session_identity_gate` above already required — a tty, or an
            # explicit `XF_HUMAN_CONSOLE` declaration. Observed HERE, where it is
            # known, and never re-derived by the engine.
            provenance=cli_provenance(), **parsed)
    # THE OPEN IS INSIDE THE CREATE'S FAILURE DOMAIN (finding 3): every refusal
    # below can arrive after `resolve_session` opened a branch, a worktree, a live
    # registry entry and a snapshot. `_unwind_cli_session` ends a session THIS
    # invocation opened and leaves a JOINED one exactly as it was.
    except BoundaryViolation as exc:          # existing target (create-only), etc.
        return _unwind_cli_session("create-document", session, git, repo_root,
                                   exc.refusal.report())
    except gate_mod.GateRefused as exc:
        return _unwind_cli_session("create-document", session, git, repo_root,
                                   str(exc))
    except branch_session_mod.SessionRefused as exc:   # collision, live proposal
        return _unwind_cli_session("create-document", session, git, repo_root,
                                   exc.report())
    except session_git_mod.SessionGitRefused as exc:   # a STRUCTURAL git refusal
        return _unwind_cli_session("create-document", session, git, repo_root,
                                   str(exc))
    except session_git_mod.GitError as exc:            # git's own reason, verbatim
        return _unwind_cli_session("create-document", session, git, repo_root,
                                   str(exc))
    except OSError as exc:                    # unwritable area, bad path
        return _unwind_cli_session("create-document", session, git, repo_root,
                                   f"the create could not be written: {exc}")
    print(f"create-document {result['path']} "
          f"(status {result['status']}, by {args.actor})")
    print(f"  document:           {result['path']}")
    print(f"  gate-action record: {result['record']}")
    if result.get("ref"):
        print(f"  session branch:     {result['ref']}"
              f"{' (joined)' if result.get('joined') else ''}")
        print(f"  commit:             {result['commit']}")
    if result.get("notebook_notice"):
        # FR-042: a NOTIFICATION, not a failure — stderr so it cannot be mistaken
        # for part of the created document's report, exit code still 0
        print(f"  session note:       {result['notebook_notice']}", file=sys.stderr)
    return 0


def cmd_gate_edit_document(args: argparse.Namespace) -> int:
    """Rewrite an EXISTING document inside the tile's branch session
    (007-workbench-branch-sessions T043, FR-015/FR-020) — the CLI parity surface
    of `POST /actions/gate/edit-document`, driving the SAME engine.

    Session-ONLY: with no live session on the tile this refuses and names
    `edit-apply`, the main-resident redline path, which is untouched by this
    feature (FR-017). The replacement arrives as `--content-file` rather than
    inline text so a shell cannot mangle a document, and the whole action is ONE
    commit on the session branch carrying the document and its gate-action record.

    FR-019 is a PER-VERB obligation here: a CLI verb is a FRESH PROCESS with no
    `serve.py` handler in front of it, so this function constructs the HumanGate
    and requires it ITSELF — before the content file is read and before any
    session is resolved — and re-derives the process's session registry through
    `_session_registry` (T033a), without which a CLI verb would see no session at
    all."""
    repo_root = Path(args.repo_root).resolve()
    # The IDENTITY gate, run first and purely to enforce FR-019 ahead of every
    # read and every resolution — through the SHARED `_session_identity_gate`, so
    # this verb cannot drift from its four siblings on any of the three clauses
    # (it used to construct its own gate inline and therefore missed the
    # agent/automation clause when that clause arrived; PR #49 finding 2). The
    # WRITING gate is a second one, rooted at (and declaring) the worktree once
    # the session is known — that declaration is what unlocks the narrow rewrite
    # allowance at all (T026).
    refused = _session_identity_gate("edit-document", repo_root, args)
    if refused is not None:
        return refused
    try:
        content = Path(args.content_file).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"edit-document refused: the replacement could not be read: {exc}",
              file=sys.stderr)
        return 1
    # The registry key's repository half, DERIVED so the contract's flag surface
    # stays as short as it reads: the checkout directory name IS the repository
    # name by the same convention `branch_session.container_root` already relies
    # on (`<repo>` beside `<repo>-worktrees/`, FR-005/R7). The registry is
    # per-PROCESS, so all that is required is that the bootstrap below and the
    # resolution beside it agree — and `--repository` overrides both together for
    # a checkout whose directory is named something else.
    repository = _session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (args.scope_kind, args.scope_id), checkout_root=repo_root,
            registry=_session_registry(repo_root, repository),
            repository=repository, records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="edit-document", require_live=True,
            remedy=gate_routes_mod.EDIT_REMEDY)
        result = gate_routes_mod.execute_edit_document(
            HumanGate(session.worktree, [args.records_dir],
                      human_actor=args.actor, session_root=session.worktree),
            document=args.document, content=content, notes=args.notes,
            records_dir=args.records_dir, session=session, git=git,
            # the SERVED checkout: the base this session branched from, and
            # therefore the engine's answer to "did THIS session create this
            # document, or does it belong to another tile" (T092 defect 1)
            checkout_root=repo_root,
            provenance=cli_provenance())
    except branch_session_mod.SessionRefused as exc:   # no session, collision, …
        print(f"edit-document refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:          # confinement, absent target, delete
        print(f"edit-document refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.SessionGitRefused as exc:   # a STRUCTURAL git refusal
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:   # git's own reason, verbatim
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:                    # unreadable staging tree / target
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    print(f"edit-document {result['document']} (by {args.actor})")
    print(f"  session branch:     {result['ref']}")
    print(f"  commit:             {result['commit']}")
    print(f"  gate-action record: {result['record']}")
    return 0


# FR-019's THIRD clause on the CLI (PR #49 review finding 2). `--actor` is free
# text the caller supplies, so a scripted `cli.main(["gate", "abandon-session",
# "--actor", "codex-agent-bot", …])` tore a session down with exit 0 and a record
# naming the bot — the clause had no runtime realization at all.
#
# The CLI's evidence of a human is the one it has always implicitly relied on and
# never checked: an INTERACTIVE TERMINAL. A person at a shell has one; a CI step,
# an agent harness, and a `subprocess.run` do not. A non-interactive HUMAN shell
# (a `nohup`, a remote exec) declares presence explicitly with the environment
# variable below, which makes the declaration auditable instead of assumed.
#
# The honest limit, same as the route's: an agent running AS the engineer can set
# the variable. Hardening that is the xForge host's concern (the ruling recorded
# at `_human_gate`, and D22), not this local CLI's. What the check removes is the
# invocation that never even claimed to be a human console.
HUMAN_CONSOLE_ENV = "XF_HUMAN_CONSOLE"
_TRUTHY = ("1", "true", "yes", "on")

AGENT_INVOCATION_REFUSAL = (
    "a session gate verb is human-only (FR-019) and this invocation is not an "
    f"interactive human console. Run it from a terminal, or set "
    f"{HUMAN_CONSOLE_ENV}=1 to declare human presence in a non-interactive shell")


def console_presence() -> str | None:
    """HOW this invocation shows it is a human at a console, or None when it
    cannot (design D23; Brett's 2026-07-27 ruling item 3).

    The same two proofs `human_console_present` has always accepted, now NAMED so
    the gate-action record can say which one was shown — the CLI is the only place
    that knows, and a record that says only "a human did this" hides the very
    difference between them.

    ORDER: the DECLARATION wins over the terminal. An operator who exports
    `XF_HUMAN_CONSOLE=1` and then types the verb at a real tty is recorded as
    `declared`, the WEAKEST of the three proofs — deliberately, because an audit
    consumer filtering for `declared` must not be able to miss one. It is also the
    order `human_console_present` already used, so nothing about WHO is admitted
    changes here."""
    declared = os.environ.get(HUMAN_CONSOLE_ENV, "")
    if str(declared).strip().lower() in _TRUTHY:
        return gate_mod.PRESENCE_DECLARED
    try:
        if sys.stdin.isatty():
            return gate_mod.PRESENCE_TTY
    except (AttributeError, OSError, ValueError):
        return None
    return None


def human_console_present() -> bool:
    """Whether this invocation can show it is a human at a console."""
    return console_presence() is not None


def cli_provenance():
    """This invocation's GATEWAY fact (D23): surface `cli`, plus the proof of
    console presence `console_presence` observed. None when presence was not
    shown at all — the session verbs never reach a record in that state
    (`_session_identity_gate` refuses first), and a pre-existing verb writes the
    pre-growth shape rather than a guessed one, because the vocabulary has no
    value meaning "not shown"."""
    presence = console_presence()
    if presence is None:
        return None
    return gate_mod.Provenance(gate_mod.SURFACE_CLI, presence)


def _session_identity_gate(verb: str, repo_root: Path,
                           args: argparse.Namespace) -> int | None:
    """FR-019, enforced PER VERB on the CLI: a session subcommand is a FRESH
    PROCESS with no `serve.py` handler in front of it, so it constructs its own
    `HumanGate` and requires it BEFORE any read, any resolution, and any write.
    Returns an exit code to propagate, or None when the identity is good.

    ALL THREE of FR-019's clauses are discharged here, in the order the route
    discharges them: locality is structural (a CLI verb runs in the human's own
    checkout), then the AGENT/AUTOMATION clause (`human_console_present`), then
    the unresolved-actor clause.

    A BLANK `--actor` must fail closed with a refusal rather than a traceback: a
    gate action with no identified human is structurally invalid, and the human who
    typed it needs to be told that, not shown a stack."""
    if not human_console_present():
        print(f"{verb} refused: {AGENT_INVOCATION_REFUSAL}", file=sys.stderr)
        return 1
    try:
        gate_mod.require_human_gate(
            HumanGate(repo_root, [args.records_dir], human_actor=args.actor))
    except ValueError as exc:                  # blank actor -> fail closed
        print(f"{verb} refused: {exc}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:           # structurally unreachable here
        print(f"{verb} refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    return None


def _pull_request_port(repo_root: Path):
    """The LOCAL plane's pull-request port (FR-034, D22).

    The identity is RULED: the INVOKING ENGINEER'S OWN `gh` authentication. This
    factory therefore constructs the real adapter with the checkout and NOTHING
    ELSE — no token argument is accepted anywhere on this path, nothing is stored,
    and no credential is synthesized. The hosted plane's openxfactory-App identity
    is normative but out of scope (FR-048), so there is no plane switch to make
    here either.

    It is a named seam purely so a test can inject `FakePullRequests`: no test may
    perform a real remote write (quickstart step 6)."""
    from ideation_dashboard.session_pr import GhPullRequests

    return GhPullRequests(repo_root)


def cmd_gate_open_pr(args: argparse.Namespace) -> int:
    """Push the tile's session branch and open (or update) its pull request
    (007-workbench-branch-sessions T065, FR-029/FR-032/FR-020) — the CLI parity
    surface of `POST /actions/gate/open-pr`, driving the SAME engine.

    The remote write uses the invoking engineer's own ambient `gh` authentication
    (FR-034, D22): a missing or invalid `gh` auth is reported VERBATIM as the
    engine's refusal, because a paraphrase of an auth failure cannot be acted on.

    NO readiness signal of either kind is consulted (FR-031, D21), the verb merges
    and approves nothing (FR-030), and the gate-action record is MAIN-RESIDENT so it
    outlives the branch the merge deletes (FR-029). If the branch has ALREADY
    merged, this ends the session instead of pushing it again (FR-033).

    FR-019 is a PER-VERB obligation here: a CLI verb is a FRESH PROCESS with no
    `serve.py` handler in front of it, so the identity gate runs FIRST — before the
    body file is read and before any session is resolved."""
    repo_root = Path(args.repo_root).resolve()
    refused = _session_identity_gate("open-pr", repo_root, args)
    if refused is not None:
        return refused
    body = None
    if args.body_file:
        try:
            body = Path(args.body_file).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"open-pr refused: the pull-request body could not be read: "
                  f"{exc}", file=sys.stderr)
            return 1
    repository = _session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (args.scope_kind, args.scope_id), checkout_root=repo_root,
            registry=_session_registry(repo_root, repository),
            repository=repository, records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="open-pr", require_live=True,
            remedy=gate_routes_mod.OPEN_PR_REMEDY)
        result = gate_routes_mod.execute_open_pr(
            HumanGate(repo_root, [args.records_dir], human_actor=args.actor),
            git, session=session, pull_requests=_pull_request_port(repo_root),
            records_dir=args.records_dir, checkout_root=repo_root,
            title=args.title, body=body, provenance=cli_provenance(),
            # retire-at-teardown on the MERGE ending too (T074): before Phase 8
            # the CLI declared no adapter and reported honestly that there was no
            # notebook to retire — now both surfaces have one (FR-021, D16)
            notebook=_notebook_port(repo_root))
    except branch_session_mod.SessionRefused as exc:   # no session, live proposal
        print(f"open-pr refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:
        print(f"open-pr refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    except session_pr_mod.PullRequestRefused as exc:   # `gh`'s own words, verbatim
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:            # git's own reason, verbatim
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    if result.get("merged"):
        print(f"open-pr {result['ref']} had already MERGED — the session ended "
              f"(by {args.actor})")
        print(f"  torn down:          {', '.join(result['torn_down']) or '(nothing)'}")
        print("  branch:             "
              f"{'DELETED' if result['branch_deleted'] else 'retained'} "
              f"({result['ref']})")
        for note in result.get("notes") or []:
            print(f"  session note:       {note}", file=sys.stderr)
        return 0
    print(f"open-pr {result['ref']} "
          f"({'updated' if result['updated'] else 'opened'}, by {args.actor})")
    print(f"  pull request:       {result['pull_request']}")
    print(f"  gate-action record: {result['record']}")
    # what this save did to the reviewer-facing TEXT (finding R2-13): "updated"
    # alone cannot distinguish a save that renamed the pull request from one that
    # left a human's description exactly as it was
    for note in result.get("notes") or []:
        print(f"  pull-request text:  {note}")
    return 0


def cmd_gate_abandon_session(args: argparse.Namespace) -> int:
    """End the tile's branch session WITHOUT saving, carrying the required reason
    (007-workbench-branch-sessions T053, FR-021/FR-022/FR-020) — the CLI parity
    surface of `POST /actions/gate/abandon-session`, driving the SAME engine.

    Tears down the worktree, the registry entry, and the session notebook, and
    deletes NOTHING: the branch, its pushed history, and any open pull request
    survive, and `branch_retained` is read back from git rather than assumed. The
    record is MAIN-RESIDENT — the served checkout's gate-records tree — because
    FR-028's cleanup deletes the branch and would take a branch-resident
    reason-record with it."""
    repo_root = Path(args.repo_root).resolve()
    refused = _session_identity_gate("abandon-session", repo_root, args)
    if refused is not None:
        return refused
    repository = _session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (args.scope_kind, args.scope_id), checkout_root=repo_root,
            registry=_session_registry(repo_root, repository),
            repository=repository, records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="abandon-session", require_live=True,
            remedy=gate_routes_mod.ABANDON_REMEDY)
        result = gate_routes_mod.execute_abandon_session(
            HumanGate(repo_root, [args.records_dir], human_actor=args.actor),
            git, session=session, reason=args.reason, notes=args.notes,
            records_dir=args.records_dir, checkout_root=repo_root,
            provenance=cli_provenance(),
            # the session notebook is RETIRED at this ending too (T074, FR-021,
            # D16) — never re-pointed at `main`
            notebook=_notebook_port(repo_root))
    except branch_session_mod.SessionRefused as exc:   # no session, live proposal
        print(f"abandon-session refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:
        print(f"abandon-session refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"abandon-session refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:            # git's own reason, verbatim
        print(f"abandon-session refused: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"abandon-session refused: {exc}", file=sys.stderr)
        return 1
    print(f"abandon-session {result['ref']} (by {args.actor})")
    print(f"  reason:             {result['reason']}")
    print(f"  torn down:          {', '.join(result['torn_down']) or '(nothing)'}")
    print("  branch:             "
          f"{'RETAINED' if result['branch_retained'] else 'gone'} "
          f"({result['ref']})")
    print(f"  gate-action record: {result['record']}")
    # An OPEN pull request this ending does not close (FR-022, G9) is named, and so
    # is the FR-029 record finalized for it — the custody gap critic finding C6
    # found was silent on both counts.
    if result.get("pull_request"):
        print(f"  pull request:       OPEN, {result['pull_request']} "
              "(this verb closes none)")
    if result.get("dispatch_record"):
        print(f"  dispatch record:    {result['dispatch_record']} "
              "(finalized from the pending-dispatch marker)")
    for note in result.get("notes") or []:
        print(f"  session note:       {note}", file=sys.stderr)
    return 0


def cmd_gate_cleanup_abandoned_branch(args: argparse.Namespace) -> int:
    """Delete an ABANDONED session's surviving branch, once the topic's PROPOSAL
    exists (007-workbench-branch-sessions T056, FR-028/FR-020).

    HUMAN-INVOKED, always: nothing automatic ever calls this, and a `propose`
    DISPATCH is explicitly not enough — the commissioned authoring may never
    deliver a proposal, and the abandoned branch is the only surviving evidence of
    that exploration until it does."""
    repo_root = Path(args.repo_root).resolve()
    refused = _session_identity_gate("cleanup-abandoned-branch", repo_root, args)
    if refused is not None:
        return refused
    repository = _session_repository_key(repo_root, args)
    try:
        result = gate_routes_mod.execute_cleanup_abandoned_branch(
            HumanGate(repo_root, [args.records_dir], human_actor=args.actor),
            session_git_mod.SessionGit(repo_root),
            tile=branch_session_mod.Tile(args.scope_kind, args.scope_id),
            ref=args.ref, registry=_session_registry(repo_root, repository),
            repository=repository, checkout_root=repo_root,
            records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root))
    except branch_session_mod.SessionRefused as exc:
        print(f"cleanup-abandoned-branch refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:
        print(f"cleanup-abandoned-branch refused: {exc.refusal.report()}",
              file=sys.stderr)
        return 1
    except session_git_mod.SessionGitRefused as exc:
        print(f"cleanup-abandoned-branch refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:
        print(f"cleanup-abandoned-branch refused: {exc}", file=sys.stderr)
        return 1
    print(f"cleanup-abandoned-branch {result['ref']} deleted (by {args.actor})")
    # What was VERIFIED, not what ought to exist: the line used to assert that "the
    # abandon record on `main` survives it" whether or not any abandon had ever
    # happened (PR #49 second-review finding 3).
    print(f"  the abandon this ends was verified first: {result['abandon_proof']}")
    return 0


def _stats(snapshot: dict) -> dict[str, int]:
    return {k: len(snapshot.get(k, [])) for k in (
        "documents", "clusters", "possibles", "staged_topics", "changes", "keyword_index")}


def _add_generate_args(sub: argparse.ArgumentParser) -> None:
    """Generation arguments shared by `generate` and `generate-and-open`."""
    sub.add_argument("--repo-root", required=True, help="repository to scan")
    sub.add_argument("--repository", required=True, help="canonical repository id for the snapshot")
    sub.add_argument("--source-revision", default=None,
                     help="pin the source_revision anchor (default: the repo's git HEAD)")
    sub.add_argument("--project-register", default=None,
                     help="override the project-register source (default: discovered under repo-root)")
    sub.add_argument("--possibles", default=None,
                     help="override the possibles-register source (default: discovered under repo-root)")
    sub.add_argument("--strict", action="store_true",
                     help="treat validator warnings as failures — and make a "
                          "validation that could not RUN AT ALL (the validator "
                          "is unreachable, or its python dependencies are "
                          "missing) fatal too, instead of the warning an "
                          "ordinary run gets")
    sub.add_argument("--no-validate", action="store_true", help="skip post-render validation")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ideation-dashboard", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="regenerate the deterministic snapshot")
    _add_generate_args(gen)
    gen.add_argument("--output", required=True, help="snapshot output path (JSON)")
    gen.set_defaults(func=cmd_generate)

    gao = sub.add_parser("generate-and-open",
                         help="regenerate the snapshot, serve it locally, and open the browser")
    _add_generate_args(gao)
    gao.add_argument("--run-dir", default=None,
                     help="run-local output directory for the snapshot (default: a temp dir)")
    gao.add_argument("--actor", default=None,
                     help="human identity for loopback gate actions "
                          "(default: the checkout's git user.name)")
    gao.add_argument("--host", default=serve_mod.DEFAULT_HOST,
                     help="bind host (default: 127.0.0.1, loopback only)")
    gao.add_argument("--port", type=int, default=0, help="bind port (default: ephemeral)")
    gao.add_argument("--no-open", action="store_true", help="do not launch a browser (print the URL only)")
    gao.add_argument("--no-serve", action="store_true",
                     help="generate + print the URL, then exit without serving (non-blocking)")
    gao.set_defaults(func=cmd_generate_and_open)

    create = sub.add_parser(
        "create", help="scaffold a new header-compliant ideation doc and open it for editing")
    create.add_argument("--repo-root", required=True, help="repository to scaffold into")
    create.add_argument("--area", default=authoring_mod.DEFAULT_AREA,
                        help=f"target ideation area (default: {authoring_mod.DEFAULT_AREA})")
    create.add_argument("--title", required=True, help="document title (H1, without the — Brainstorm suffix)")
    create.add_argument("--summary", required=True, help="Summary: one sentence")
    create.add_argument("--topics", required=True, help="comma-separated Topics: list")
    create.add_argument("--repository-context", required=True, help="Repository context: value")
    create.add_argument("--kind", default=authoring_mod.DEFAULT_KIND, help="Kind: value")
    create.add_argument("--possible-feat", action="append", default=[],
                        help="a ## Possible feats bullet (repeatable)")
    create.add_argument("--editor", default=None, help="override $EDITOR / xdg-open")
    create.add_argument("--no-open", action="store_true", help="scaffold only; do not launch an editor")
    create.set_defaults(func=cmd_create)

    edit = sub.add_parser(
        "edit", help="select-to-edit: launch the human's editor over a listed document")
    edit.add_argument("--repo-root", required=True, help="the pinned checkout root")
    edit.add_argument("path", help="repo-relative path to the document")
    edit.add_argument("--editor", default=None, help="override $EDITOR / xdg-open")
    edit.add_argument("--no-open", action="store_true", help="print the resolved path only")
    edit.set_defaults(func=cmd_edit)

    _add_gate_subcommands(sub)
    return parser


def _add_gate_identity_args(sub: argparse.ArgumentParser) -> None:
    """Identity + records location shared by EVERY gate action. `--actor` is the
    human identity; authn hardening is the xForge host's concern (section 4)."""
    sub.add_argument("--repo-root", required=True, help="the pinned checkout root")
    sub.add_argument("--actor", required=True, help="the acting human's identity (recorded in the gate-action record)")
    sub.add_argument("--records-dir", default=gate_mod.DEFAULT_RECORDS_DIR,
                     help=f"records output directory (default: {gate_mod.DEFAULT_RECORDS_DIR})")


def _add_gate_snapshot_args(sub: argparse.ArgumentParser) -> None:
    """Snapshot-generation args for the actions that plan against the snapshot
    (demote, kickoff)."""
    sub.add_argument("--repository", required=True, help="canonical repository id for the snapshot")
    sub.add_argument("--source-revision", default=None, help="pin the source_revision anchor (default: git HEAD)")
    sub.add_argument("--project-register", default=None, help="override the project-register source")
    sub.add_argument("--possibles", default=None, help="override the possibles-register source")


def _add_gate_subcommands(sub) -> None:
    gate = sub.add_parser("gate", help="human-only gate console actions (US9): demote / ratify / edit-apply / kickoff")
    gsub = gate.add_subparsers(dest="gate_command", required=True)

    demote = gsub.add_parser(
        "demote",
        help="reject a proposal back to staging (mechanized reverse transition); "
             "peer of the executing dashboard route POST /actions/gate/demote, which "
             "PLANS and RECORDS only \u2014 this command is the only surface that can "
             "also --execute the recorded plan")
    _add_gate_identity_args(demote)
    _add_gate_snapshot_args(demote)
    demote.add_argument("--change-id", required=True, help="the change to demote")
    demote.add_argument("--reason", required=True, help="the required reason a change went back to staging")
    demote.add_argument("--staging-topic", default=None,
                        help="target staging topic (default: the change's recorded origin staging id)")
    demote.add_argument("--execute", action="store_true",  # unreachable from the dashboard route by design (NG-005)
                        help="apply the moves to this checkout (default: emit the plan only)")
    demote.set_defaults(func=cmd_gate_demote)

    ratify = gsub.add_parser("ratify", help="approve a proposal (write the ratification record + register update)")
    _add_gate_identity_args(ratify)
    ratify.add_argument("--change-id", required=True, help="the change to ratify")
    ratify.add_argument("--ratifier", default=None, help="the ratifying authority (default: --actor)")
    ratify.add_argument("--date", default=None, help="ratification date YYYY-MM-DD (default: today)")
    ratify.set_defaults(func=cmd_gate_ratify)

    edit = gsub.add_parser("edit-apply", help="apply a HUMAN-approved redline to a change document")
    _add_gate_identity_args(edit)
    edit.add_argument("--change-id", required=True, help="the change owning the document")
    edit.add_argument("--document", required=True, help="repo-relative path of the change document to revise")
    edit.add_argument("--old-file", default=None, help="file holding the exact block to replace (replacement-block form)")
    edit.add_argument("--new-file", default=None, help="file holding the replacement block")
    edit.add_argument("--full-text-file", default=None, help="file whose contents replace the whole document (full-text form)")
    edit.add_argument("--concept", default=None, help="the listed concept this redline revises (optional)")
    edit.set_defaults(func=cmd_gate_edit_apply)

    dispose = gsub.add_parser(
        "dispose-possible",
        help="dispose a pending_review ai-derived possible (accept / reject / defer)")
    _add_gate_identity_args(dispose)
    dispose.add_argument("--possible-id", required=True,
                         help="the possibles-register entry id (pos-derived-...)")
    dispose.add_argument("--outcome", required=True,
                         choices=("accepted", "rejected", "deferred"),
                         help="the human verdict (one-way; only deferred may be re-disposed)")
    dispose.add_argument("--reason", default=None,
                         help="REQUIRED with --outcome rejected: the durable why")
    dispose.add_argument("--citation", default=None,
                         help="REQUIRED with --outcome rejected: what the rejection cites")
    dispose.add_argument("--note", default=None, help="optional free-text note on the disposition")
    dispose.set_defaults(func=cmd_gate_dispose_possible)

    kick = gsub.add_parser("kickoff", help="dispatch a ratified change's next step (refused without ratification)")
    _add_gate_identity_args(kick)
    _add_gate_snapshot_args(kick)
    kick.add_argument("--change-id", required=True, help="the ratified change to kick off")
    kick.add_argument("--outline", default=None, help="the realization outline (default: a Speckit realization descriptor)")
    kick.add_argument("--workflow", default=kickoff_mod.DEFAULT_WORKFLOW, help="workflow id (default: speckit-realization)")
    kick.set_defaults(func=cmd_gate_kickoff)

    prop = gsub.add_parser("propose", help="commission proposal authoring for a staging topic (add-propose-verb)")
    _add_gate_identity_args(prop)
    prop.add_argument("--topic-id", required=True, help="the staging topic to take toward proposal (ideation/staging/<topic-id>/)")
    prop.add_argument("--outline", default=None, help="the authoring outline (default: a standard OpenSpec-change commission)")
    prop.add_argument("--workflow", default=kickoff_mod.DEFAULT_PROPOSAL_WORKFLOW,
                      help="workflow id (default: proposal-authoring)")
    prop.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    prop.set_defaults(func=cmd_gate_propose)

    # ---- the wheel action-row commissions (011 add-wheel-action-verbs) ----
    # REQUIRED FLAGS, not positionals (plan decision P6): no gate subcommand in
    # this CLI takes a positional target, and consistency wins over the task
    # prose's shorthand.
    promote = gsub.add_parser(
        "promote-to-staging",
        help="commission a staging fragment for an ACCEPTED possible (add-wheel-action-verbs)")
    _add_gate_identity_args(promote)
    promote.add_argument("--possible-id", required=True,
                         help="the possibles-register id to promote")
    promote.add_argument("--topic", default=None,
                         help="optional proposed destination topic slug (the fulfilling step chooses when omitted)")
    promote.add_argument("--outline", default=None, help="the commissioning outline (default: a standard organize commission)")
    promote.add_argument("--workflow", default=kickoff_mod.DEFAULT_STAGING_FRAGMENT_WORKFLOW,
                         help=f"workflow id (default: {kickoff_mod.DEFAULT_STAGING_FRAGMENT_WORKFLOW})")
    promote.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    promote.set_defaults(func=cmd_gate_promote_to_staging)

    brief = gsub.add_parser(
        "research-brief",
        help="commission a PRE-VERDICT evidence brief for a possible (add-wheel-action-verbs)")
    _add_gate_identity_args(brief)
    brief.add_argument("--possible-id", required=True,
                       help="the possibles-register id to research")
    brief.add_argument("--outline", default=None, help="the commissioning outline (default: a standard research commission)")
    brief.add_argument("--workflow", default=kickoff_mod.DEFAULT_RESEARCH_BRIEF_WORKFLOW,
                       help=f"workflow id (default: {kickoff_mod.DEFAULT_RESEARCH_BRIEF_WORKFLOW})")
    brief.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    brief.set_defaults(func=cmd_gate_research_brief)

    derive = gsub.add_parser(
        "derive-possibles",
        help="commission a CLUSTER-SCOPED run of the possibles-derivation lane (add-wheel-action-verbs)")
    _add_gate_identity_args(derive)
    _add_gate_snapshot_args(derive)   # the cluster is validated against the snapshot
    derive.add_argument("--cluster-id", required=True,
                        help="the topic cluster to scope the derivation run to")
    derive.add_argument("--outline", default=None, help="the commissioning outline (default: a standard derivation commission)")
    derive.add_argument("--workflow", default=kickoff_mod.DEFAULT_DERIVE_POSSIBLES_WORKFLOW,
                        help=f"workflow id (default: {kickoff_mod.DEFAULT_DERIVE_POSSIBLES_WORKFLOW})")
    derive.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    derive.set_defaults(func=cmd_gate_derive_possibles)

    _add_lens_gate_subcommands(gsub)
    _add_create_document_subcommand(gsub)
    _add_edit_document_subcommand(gsub)
    _add_open_pr_subcommand(gsub)
    _add_session_ending_subcommands(gsub)


def _add_create_document_subcommand(gsub) -> None:
    """`gate create-document` (add-workbench-bullseye-and-create task 4.5): the
    parity surface for the workbench's create affordance. The flag names mirror
    the non-gated `create` subcommand so the two read the same, and the gate-off
    CLI DESCRIPTOR the workbench renders is exactly this invocation."""
    doc = gsub.add_parser(
        "create-document",
        help="create a NEW header-compliant ideation document through the gate "
             "(create-only, recorded; add-workbench-bullseye-and-create)")
    _add_gate_identity_args(doc)
    # The TILE's scope identity (007-workbench-branch-sessions T023a, FR-018).
    # OPTIONAL and given TOGETHER: with both, the create opens or joins the tile's
    # branch session and lands on the branch as one commit with its record; with
    # neither, the create behaves exactly as it did before this feature. This is
    # the pair quickstart step 2 invokes.
    doc.add_argument("--scope-kind", default=None,
                     choices=list(branch_session_mod.SCOPE_KINDS),
                     help="the tile's scope kind — resolves the branch session "
                          "(requires --scope-id; omit both for a main-resident "
                          "create)")
    doc.add_argument("--scope-id", default=None,
                     help="the tile id: a staging FOLDER name, a cl-*, or a pos-* "
                          "(requires --scope-kind)")
    doc.add_argument("--area", default=authoring_mod.DEFAULT_AREA,
                     help=f"target ideation area (default: {authoring_mod.DEFAULT_AREA})")
    doc.add_argument("--title", required=True,
                     help="document title (H1, without the — Brainstorm suffix)")
    doc.add_argument("--summary", required=True, help="Summary: one sentence")
    doc.add_argument("--topics", required=True, help="comma-separated Topics: list")
    doc.add_argument("--repository-context", required=True,
                     help="Repository context: value — a DOCUMENT HEADER field "
                          "(the route defaults it from the served snapshot; the "
                          "CLI asks for it). It is not the registry key: see "
                          "--repository")
    # THE REGISTRY/NOTEBOOK KEY (PR #49 review finding 8, leg b). Every sibling
    # session verb has had this flag and derives the key as `--repository or the
    # checkout directory's name`; `create-document` — the ONE verb that OPENS a
    # session — had no such flag and used `--repository-context`, a document
    # HEADER value, instead. A create with `--repository-context "openxFactory
    # ideation"` therefore keyed its session and named its notebook one way while
    # every later verb keyed the same session another, so the abandon reported a
    # notebook torn down that it had never looked at. One derivation now, shared.
    doc.add_argument("--repository", default=None,
                     help="the registry key's repository half (default: the "
                          "checkout directory's name, the same convention the "
                          "worktree container is derived from)")
    doc.add_argument("--kind", default=authoring_mod.DEFAULT_KIND, help="Kind: value")
    doc.add_argument("--status", default=None,
                     choices=authoring_mod.CREATABLE_STATUSES,
                     help="Status: value (default: brainstorm, in EVERY area — "
                          "a created document's tie to a staging packet is its "
                          "placement in that folder, not its status header)")
    doc.add_argument("--source", default=None,
                     help="optional Source: provenance citation (the workbench "
                          "scope, or the keyword-lens recipe at a source_revision)")
    doc.add_argument("--possible-feat", action="append", default=[],
                     help="a ## Possible feats bullet (repeatable)")
    # The ANSWER to the FR-025 resume-or-new report (T056). Not in
    # contracts/cli.md's flag list, and added because FR-020 owes the choice a CLI
    # surface: the report is a REFUSAL naming both continuations, so without a way
    # to answer it a CLI-only human could never continue an abandoned tile at all.
    # Optional by design — the first write sends none and gets the report.
    doc.add_argument("--continuation", default=None,
                     choices=list(branch_session_mod.CONTINUATIONS),
                     help="answer the resume-or-new report on a tile whose "
                          "abandoned branch survives: `resume` keeps the existing "
                          "branch and its history, `new` opens the next ordinal "
                          "(FR-025; omit it to be SHOWN the choice)")
    doc.set_defaults(func=cmd_gate_create_document)


def _add_edit_document_subcommand(gsub) -> None:
    """`gate edit-document` (007-workbench-branch-sessions T043, FR-020): the
    parity surface for the session's rewrite affordance, and the copyable
    descriptor the gate-off workbench renders for it (FR-046).

    The flag surface is contracts/cli.md's, exactly: the tile scope that resolves
    the session, the document, `--content-file` (never inline text, so a shell
    cannot mangle a document), and optional notes. There is deliberately no
    `--dry-run` — a partial session write is worse than no affordance — and no
    flag that creates or deletes: this verb REWRITES, creation stays
    `create-document`, and no session verb grants delete authority."""
    doc = gsub.add_parser(
        "edit-document",
        help="rewrite an EXISTING document inside the tile's branch session "
             "(session-only, recorded, one commit; 007-workbench-branch-sessions)")
    _add_gate_identity_args(doc)
    doc.add_argument("--scope-kind", required=True,
                     choices=list(branch_session_mod.SCOPE_KINDS),
                     help="the tile's scope kind — resolves the branch session "
                          "this rewrite happens in")
    doc.add_argument("--scope-id", required=True,
                     help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    doc.add_argument("--document", required=True,
                     help="the document to rewrite, as a path inside the session "
                          "worktree (a path outside it refuses)")
    doc.add_argument("--content-file", required=True,
                     help="file whose contents REPLACE the document (never inline "
                          "text; an empty file is refused as a delete in disguise)")
    doc.add_argument("--notes", default=None,
                     help="optional free-text note recorded on the action")
    doc.add_argument("--repository", default=None,
                     help="the registry key's repository half (default: the "
                          "checkout directory's name, the same convention the "
                          "worktree container is derived from)")
    doc.set_defaults(func=cmd_gate_edit_document)


def _add_open_pr_subcommand(gsub) -> None:
    """`gate open-pr` (007-workbench-branch-sessions T065, FR-020/FR-029): the
    parity surface for the session's SAVE affordance, and the copyable descriptor
    the gate-off workbench renders for it (FR-046).

    The flag surface is contracts/cli.md's, exactly: the tile scope that resolves
    the session, an optional `--title`, and `--body-file` rather than inline text so
    a shell cannot mangle a pull-request body. There is deliberately NO `--dry-run`
    (a partial session write is worse than no affordance), NO flag that merges,
    approves, or bypasses protection (FR-030 — the verb holds no such authority),
    and — the ruled one — NO token flag of any kind: the push identity is the
    INVOKING ENGINEER's own ambient `gh` authentication (FR-034, D22), so a
    credential argument would create a second, unruled identity path."""
    save = gsub.add_parser(
        "open-pr",
        help="push the tile's session branch and open (or update) its pull "
             "request into the existing Merge-Master ritual")
    _add_gate_identity_args(save)
    save.add_argument("--scope-kind", required=True,
                      choices=list(branch_session_mod.SCOPE_KINDS),
                      help="the tile's scope kind — resolves the session to save")
    save.add_argument("--scope-id", required=True,
                      help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    save.add_argument("--title", default=None,
                      help="the pull request's title. Omitted: the FIRST save "
                           "names the session branch and its tile, a LATER save "
                           "leaves the existing title unchanged")
    save.add_argument("--body-file", default=None,
                      help="file whose contents become the pull request BODY "
                           "(never inline text). Omitted: the FIRST save carries "
                           "the merge-commit-never-squash notice (D18), a LATER "
                           "save leaves the existing body unchanged — a save never "
                           "overwrites reviewer-facing text a human wrote")
    save.add_argument("--repository", default=None,
                      help="the registry key's repository half (default: the "
                           "checkout directory's name)")
    save.set_defaults(func=cmd_gate_open_pr)


def _add_session_ending_subcommands(gsub) -> None:
    """`gate abandon-session` and `gate cleanup-abandoned-branch`
    (007-workbench-branch-sessions T053/T056, FR-020) — the CLI parity surfaces of
    the two FR-021/FR-028 routes, and the copyable descriptors the gate-off
    workbench renders for them (FR-046).

    The flag surface is contracts/cli.md's, exactly. There is deliberately no
    `--dry-run` (a partial session write is worse than no affordance), no flag that
    skips the record, and — on the abandon — nothing that deletes a branch: FR-022
    deletes nothing at abandon time, and the branch's end of life is the SEPARATE,
    human-invoked cleanup below, which is why they are two verbs."""
    end = gsub.add_parser(
        "abandon-session",
        help="end the tile's branch session without saving, with the required "
             "reason (recorded on `main`; the branch survives)")
    _add_gate_identity_args(end)
    end.add_argument("--scope-kind", required=True,
                     choices=list(branch_session_mod.SCOPE_KINDS),
                     help="the tile's scope kind — resolves the session to end")
    end.add_argument("--scope-id", required=True,
                     help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    end.add_argument("--reason", required=True,
                     help="the durable why this exploration stopped (required, "
                          "exactly as a demotion's reason is)")
    end.add_argument("--notes", default=None,
                     help="optional free-text note recorded on the action")
    end.add_argument("--repository", default=None,
                     help="the registry key's repository half (default: the "
                          "checkout directory's name)")
    end.set_defaults(func=cmd_gate_abandon_session)

    clean = gsub.add_parser(
        "cleanup-abandoned-branch",
        help="delete an ABANDONED session's surviving branch, once the topic's "
             "proposal exists (human-invoked, never automatic)")
    _add_gate_identity_args(clean)
    clean.add_argument("--scope-kind", required=True,
                       choices=list(branch_session_mod.SCOPE_KINDS),
                       help="the tile's scope kind — the branch is checked against "
                            "the tile that OWNS it")
    clean.add_argument("--scope-id", required=True,
                       help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    clean.add_argument("--ref", required=True,
                       help="the abandoned session branch to delete (must be this "
                            "tile's own branch or one of its ordinal forms)")
    clean.add_argument("--repository", default=None,
                       help="the registry key's repository half (default: the "
                            "checkout directory's name)")
    clean.set_defaults(func=cmd_gate_cleanup_abandoned_branch)


def _add_lens_recipe_args(sub: argparse.ArgumentParser) -> None:
    """Recipe + override args shared by the two lens verbs. Snapshot-generation
    args supply the corpus the recipe is re-evaluated against."""
    _add_gate_identity_args(sub)
    _add_gate_snapshot_args(sub)
    sub.add_argument("--name", required=True, help="the workbench set name (slugged for the manifest path)")
    sub.add_argument("--checked", action="append", required=True,
                     help="a checked keyword (stratify); repeatable — at least one required")
    sub.add_argument("--pinned", action="append", default=[],
                     help="a pinned keyword (require = hard filter); repeatable (MUST be a subset of --checked)")
    sub.add_argument("--include", action="append", default=[],
                     help="a manual-include override document=reason (near-miss pulled in; reason required); repeatable")
    sub.add_argument("--exclude", action="append", default=[],
                     help="an excluded override document=reason (recipe match removed; reason required); repeatable")


def _add_lens_gate_subcommands(gsub) -> None:
    save = gsub.add_parser("lens-save-recipe",
                           help="save a keyword-lens recipe as a workbench manifest (add-lens-gate-verbs)")
    _add_lens_recipe_args(save)
    save.set_defaults(func=cmd_gate_lens_save_recipe)

    cluster = gsub.add_parser("lens-add-as-cluster",
                              help="add a keyword-lens set as a pending_review human-seen cluster (add-lens-gate-verbs)")
    _add_lens_recipe_args(cluster)
    cluster.add_argument("--proposer", default=None, help="the proposing human (default: --actor)")
    cluster.add_argument("--evidence-repository", default=None,
                         help="the evidence source_ref repository (default: --repository)")
    cluster.add_argument("--evidence-path", default=None, help="the evidence source_ref repo-relative path")
    cluster.add_argument("--revision", default=None, help="the FULL committed revision the passage is pinned at (40/64-hex)")
    cluster.add_argument("--section", default=None, help="the evidence source_ref section")
    cluster.add_argument("--passage-sha256", default=None, help="the 64-hex sha256 of the pinned passage")
    cluster.add_argument("--rationale", default=None, help="the organizer rationale for the cluster")
    cluster.add_argument("--confidence", type=float, default=None, help="the organizer confidence in [0, 1]")
    cluster.add_argument("--alternative", action="append", default=[],
                         help="an alternative interpretation considered (repeatable; may be empty)")
    cluster.add_argument("--recipe-reference", default=None,
                         help="optional re-runnable recipe pointer (default: derived from the set name + keywords)")
    cluster.set_defaults(func=cmd_gate_lens_add_as_cluster)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except RepoRootRefused as exc:
        # The refusal is the whole message (`corpus_root.corpus_root_refusal`);
        # stderr and a non-zero status, so a wrapper script cannot mistake a
        # refused run for a generated snapshot.
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
