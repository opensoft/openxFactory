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
import sys
import tempfile
import webbrowser
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# The SUBCOMMAND EXTENSION POINT (`split-opendox-two-layer-product` § 2.4,
# design § D2). A neutral module at the top of `scripts/`, belonging to neither
# package and importing neither, for the same three reasons `output_boundary`
# and `corpus_adapter` sit there. Spelled as a bare top-level import, like
# `boundary.py` spells `output_boundary`.
import subcommand_extension  # noqa: E402

from ideation_dashboard import actor_identity as actor_mod  # noqa: E402
from ideation_dashboard import authoring as authoring_mod  # noqa: E402
from ideation_dashboard import branch_session as branch_session_mod  # noqa: E402
from ideation_dashboard import doxbench_install as install_mod  # noqa: E402
from ideation_dashboard import doxbench_knowledge as knowledge_mod  # noqa: E402
from ideation_dashboard import gate_console as gate_mod  # noqa: E402
from ideation_dashboard import profile_openxfactory  # noqa: E402
from ideation_dashboard import serve as serve_mod  # noqa: E402
from ideation_dashboard import snapshot as snapshot_mod  # noqa: E402
from ideation_dashboard import workbench as workbench_mod  # noqa: E402
from ideation_dashboard.boundary import (  # noqa: E402
    BoundaryViolation, HumanGate, OutputBoundary,
)
from ideation_dashboard.corpus_root import (  # noqa: E402
    SCANNED_ROOTS, corpus_root_refusal,
)
from ideation_dashboard.generator import (  # noqa: E402
    generate_snapshot, is_rfc3339_datetime,
)

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


class GeneratedAtRefused(Exception):
    """`--generated-at` was given something that is not an RFC 3339 date-time.

    REFUSED, not degraded — deliberately unlike every other timestamp path in
    this package. `RealGitDates.commit_date` returns None on any failure and the
    stamp is simply omitted, which is right for a value the run tried to
    DISCOVER. This one was TYPED, and the only reason to type it is that the
    scanned tree cannot supply it (the sealed source artifact
    `add-nightly-dashboard-refresh` hands the child is not a git checkout). So
    degrading here would drop the anchor in silence and produce the very
    snapshot the flag exists to prevent: `generated_at` is OPTIONAL in
    `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`, so even
    `--strict` would pass, the image would ship, and the served plane would lose
    its freshness stamp with nothing anywhere saying why."""


def _refuse_malformed_generated_at(args: argparse.Namespace) -> None:
    """Raise `GeneratedAtRefused` unless `--generated-at`, when given, is an
    RFC 3339 date-time (`generator.is_rfc3339_datetime` — the shape the snapshot
    schema declares for `generation.generated_at`)."""
    value = getattr(args, "generated_at", None)
    if value is None or is_rfc3339_datetime(value):
        return
    raise GeneratedAtRefused(
        f"--generated-at is not an RFC 3339 date-time: {value!r}\n"
        f"  required: a full date, an explicit time and an explicit offset — "
        f"e.g. 2026-09-04T01:23:45Z or 2026-09-04T01:23:45+00:00\n"
        f"  the value is recorded in the snapshot EXACTLY as given (it is an "
        f"anchor copied from elsewhere, never normalised), which is why a "
        f"malformed one is refused here instead of repaired\n"
        f"  a sealed-source run passes its manifest's source committer "
        f"timestamp, the `git show -s --format=%cI` of the sealed revision")


def _generate_and_write(args: argparse.Namespace, output: Path) -> tuple[dict, Path]:
    """Generate the deterministic snapshot from the working tree and write it
    through the interactivity boundary (the output file is the whole declared
    allowlist, rooted at its own directory). Shared by `generate` and
    `generate-and-open`.

    A `--repo-root` that cannot be a corpus checkout is REFUSED here — the ONE
    guard both verbs pass through, ahead of the generation and the write, because
    an empty snapshot that exits 0 is indistinguishable from an honest one (T092;
    see `corpus_root.corpus_scan_defect`). A malformed `--generated-at` is
    refused in the same place and for the same reason, one anchor over: both
    verbs, ahead of the write, so no snapshot file can survive a refused run."""
    _refuse_non_corpus_repo_root(args)
    _refuse_malformed_generated_at(args)
    repo_root = Path(args.repo_root).resolve()
    snapshot = generate_snapshot(
        repo_root,
        args.repository,
        source_revision=args.source_revision,
        generated_at=args.generated_at,
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
    # Printed even when absent: a missing freshness stamp used to be invisible
    # (the schema makes it optional, so nothing downstream complains), and a run
    # that meant to pin one needs to see whether it landed.
    print(f"  generated_at={snapshot['generation'].get('generated_at', '<absent>')}")
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


def cmd_generate_and_open(args: argparse.Namespace, *, opener=webbrowser.open) -> int:
    """Regenerate the snapshot from the working tree into a run dir, start the
    local server, print the URL (ALWAYS), and open the browser. `--no-open`
    suppresses the browser; `--no-serve` returns after printing the URL without
    blocking (used by tests). `opener` is injectable for testing."""
    # Ahead of minting the run dir, so a refused root leaves not even an empty
    # temp directory behind. `_generate_and_write` is still the guard that MATTERS
    # (it is the one no caller can skip); these are the same checks, earlier.
    _refuse_non_corpus_repo_root(args)
    _refuse_malformed_generated_at(args)
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

    # The model adapter's session root: the flag when given, else beside the
    # snapshot this run just wrote.
    model_session_root = (Path(args.model_session_root).resolve()
                          if getattr(args, "model_session_root", None)
                          else install_mod.session_root_beside(written))
    httpd = serve_mod.build_server(WEB_DIR, written, checkout_root,
                                   host=args.host, port=args.port,
                                   actor=getattr(args, "actor", None),
                                   # the ENTRYPOINT declares the real notebook
                                   # adapter; `build_server` never reaches for one
                                   # on a caller's behalf (PR #49 hardening item 1)
                                   adapter_factory=serve_mod.real_notebook_adapter,
                                   # and the MODEL PROVIDER, for the third time
                                   # in the same idiom and for the same reason:
                                   # an operator must be able to read what their
                                   # install talks to. Without a declaration HERE
                                   # no model consumer on this surface can reach
                                   # a provider at all — `_workbench_model_port`
                                   # returns None and every consumer's honest
                                   # posture is an absent capability
                                   # (add-doxbench-distilled-abstract D9).
                                   #
                                   # ONE bridge for the life of this process: the
                                   # adapter is stateful (it holds the per-thread
                                   # harness sessions), and `_workbench_model_port`
                                   # resolves per REQUEST. The factory takes no
                                   # arguments, so nothing about the adapter can
                                   # become a per-turn input; the three
                                   # install-time inputs it cannot supply itself
                                   # — catalog, session root, launch config — are
                                   # declared in `doxbench_install`.
                                   #
                                   # SINCE add-model-provider-broker (ratified
                                   # 2026-08-26) this is
                                   # `declared_model_port_factory`: it reads
                                   # the checkout's model-provider BINDINGS and
                                   # resolves the broker-backed port when one is
                                   # declared, and the harness factory this line
                                   # used to name when none is — so an install
                                   # that never heard of a broker is unchanged.
                                   model_port_factory=install_mod.declared_model_port_factory(
                                       model_session_root,
                                       checkout_root=checkout_root),
                                   # and the same discipline for the doxBench
                                   # knowledge service: the ENTRYPOINT makes the
                                   # install-time retrieval-backend declaration
                                   # (add-doxbench-editing-phase-b D11), which is
                                   # the self-hosted half of the ratified
                                   # two-case principle
                                   knowledge_declaration=(
                                       knowledge_mod.SELF_HOSTED_LOCAL_EMBEDDED))
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


# ---- gate console (US9): human-only executable gate actions ----------------
# Every action constructs a `HumanGate` (the distinct human-only entrypoint) —
# there is no machinery/agent code path to a gate action here.
#
# `--actor` USED TO BE FREE TEXT (the accepted v1 risk recorded at
# `ideation/brainstorm/ideation-dashboard.md` item 25, still present tense in
# `contracts/identity-brokering/README.md`): the flag NAMED the acting human and
# nothing anywhere asked whether the invocation was that human, so every
# authority-bearing record the console wrote was unattributable. It is now
# AUTHENTICATED at this boundary — the one place the untrusted claim enters —
# against whatever identity the deployment already proves
# (`actor_identity.authenticate_actor`), and the record carries the trusted
# source's CANONICAL spelling rather than the caller's. No principal, no gate
# action: `_gate_actor` raises and `main` turns it into a refusal + exit 1,
# before any HumanGate exists and therefore before any write.
#
# This does NOT close D22: an agent running AS the engineer, in the engineer's
# own checkout, still satisfies the local sources. It closes the strictly larger
# hole underneath — an invocation naming a human it has no relation to at all.


def _gate_actor(repo_root: Path, args: argparse.Namespace) -> str:
    """The AUTHENTICATED acting human for this invocation, or a refusal.

    Called by every gate-gate construction path in this module. Raises
    `actor_identity.ActorUnauthenticated`, which `main` renders as a refusal —
    deliberately an exception rather than a return code, so a call site cannot
    forget to check it and reach a HumanGate anyway."""
    authenticated = actor_mod.authenticate_actor(
        getattr(args, "actor", None), checkout_root=repo_root)
    # The canonical spelling is what everything downstream records and prints.
    args.actor = authenticated.actor
    return authenticated.actor

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
    return HumanGate(repo_root, [args.records_dir],
                     human_actor=_gate_actor(repo_root, args))


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
                     human_actor=_gate_actor(repo_root, args))


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
        # AUTHENTICATE the claim before it can become a record. Deliberately
        # AFTER the console-presence test and before the HumanGate: presence is
        # the question "is a human here at all", identity is the question "which
        # human", and an invocation that fails the first must hear that first.
        _gate_actor(repo_root, args)
    except actor_mod.ActorUnauthenticated as exc:
        print(f"{verb} refused: {exc}", file=sys.stderr)
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


def _stats(snapshot: dict) -> dict[str, int]:
    return {k: len(snapshot.get(k, [])) for k in (
        "documents", "clusters", "possibles", "staged_topics", "changes", "keyword_index")}


def _add_generate_args(sub: argparse.ArgumentParser) -> None:
    """Generation arguments shared by `generate` and `generate-and-open`."""
    sub.add_argument("--repo-root", required=True, help="repository to scan")
    sub.add_argument("--repository", required=True, help="canonical repository id for the snapshot")
    sub.add_argument("--source-revision", default=None,
                     help="pin the source_revision anchor (default: the repo's git HEAD)")
    # The SECOND generation anchor, at the same altitude as the first because
    # the two are pinned together or not at all. Without it the only source of
    # `generated_at` is `git show -s --format=%cI` run inside the scanned tree,
    # which yields nothing when that tree is not a checkout — a sealed source
    # artifact, an export, a copied context — and the snapshot then ships with
    # the stamp silently missing (add-nightly-dashboard-refresh task 3.6).
    sub.add_argument("--generated-at", default=None, metavar="RFC3339",
                     help="pin the generated_at anchor, recorded verbatim "
                          "(default: --source-revision's committer date read "
                          "from the scanned tree's git, omitted when that tree "
                          "is not a checkout)")
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


def build_parser(*, subcommand_extensions: tuple = ()) -> argparse.ArgumentParser:
    """The command line, plus whatever this invocation was ASSEMBLED with.

    `subcommand_extensions` is the SUBCOMMAND EXTENSION POINT
    (`split-opendox-two-layer-product` § 2.4, design § D2): a tuple of
    `subcommand_extension.SubcommandExtension`s, each attaching its own
    subcommands to the SAME subparsers action the core commands are added
    through. The default `()` is today's parser exactly — byte-identical help
    text for every entry point, which is the parity a golden snapshot asserts.

    An extension registers LAST, after every core subcommand, so the help text
    reads core-first and a contributed name can never displace a core one:
    `argparse` refuses a duplicate subcommand name outright, and refusing the
    contributed one is the right direction of that refusal.

    The IN-TREE PROFILE (`profile_openxfactory.SUBCOMMAND_EXTENSIONS`) is
    registered here too, at the ordinal its column has always occupied, and NOT
    passed in by `main()`. `build_parser()` names the whole of THIS assembly's
    command line — which is what every caller, every golden and every existing
    test already reads it as — so what this repository is built with belongs
    inside it, and `subcommand_extensions` stays the seam for whatever a caller
    adds on top. It is also the one line the § 3 carve deletes rather than
    moves: afterwards the core names no profile and openXdox declares its own.
    """
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
    # The model adapter's SESSION ROOT — the third install-time input the
    # entrypoint's `model_port_factory` declaration needs, beside its catalog
    # and its launch config (see the `build_server` call in
    # `cmd_generate_and_open`). A PATH ARGUMENT, defaulted like the others: with
    # no flag it sits beside the served snapshot, in the run directory this
    # process already owns, so a harness child writes into scratch space rather
    # than into the served checkout.
    gao.add_argument("--model-session-root", default=None,
                     help="where the model adapter's harness sessions live "
                          f"(default: <run-dir>/{install_mod.MODEL_SESSIONS_DIRNAME})")
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

    # `model-binding` (openDox's provider column), at the position it has always
    # been registered in. It used to be the opening line of
    # `_add_gate_subcommands` — an accident of growth, not a coupling — so § 2.4
    # calls it from here rather than letting it travel into openXdox's column
    # with the gate verbs.
    _add_model_binding_parser(sub)

    # ...and then `gate` (openXdox's column), CONTRIBUTED. These were a call to
    # `_add_gate_subcommands(sub)` on this line; they now reach the parser
    # through the extension point like any other contribution — the same `sub`,
    # the same `add_parser`, the same `set_defaults(func=...)`, at the same
    # ordinal — which is why the help text is byte-identical to the one that
    # preceded the seam.
    subcommand_extension.register_all(
        profile_openxfactory.SUBCOMMAND_EXTENSIONS, sub)
    subcommand_extension.register_all(subcommand_extensions, sub)
    return parser


def _command_label(args: argparse.Namespace) -> str:
    """`gate ratify`-style label for a refusal line."""
    parts = [getattr(args, "command", None), getattr(args, "gate_command", None)]
    return " ".join(p for p in parts if p) or "command"


def main(argv: list[str] | None = None, *,
         subcommand_extensions: tuple = ()) -> int:
    """The entrypoint, unchanged except that it PASSES THROUGH what it was
    assembled with (§ 2.4).

    The dispatch below needs no clause of its own: a contributed subcommand set
    `func` on the same subparsers action every core one does, so `args.func(args)`
    dispatches both by the identical line. That is the point of handing the real
    parser to the extension rather than a wrapper."""
    args = build_parser(
        subcommand_extensions=subcommand_extensions).parse_args(argv)
    try:
        return args.func(args)
    except actor_mod.ActorUnauthenticated as exc:
        # The unauthenticated-`--actor` gap, refused at the OUTERMOST edge: the
        # claim is checked where it enters and the command never reaches a write.
        # One catch site rather than a return code at nine gate constructions, so
        # no future gate verb can be added that forgets to check.
        print(f"{_command_label(args)} refused: {exc}", file=sys.stderr)
        return 1
    except GeneratedAtRefused as exc:
        # Same altitude and same exit status as the `--repo-root` refusal below:
        # a generation anchor that was TYPED and is malformed ends the run on
        # stderr, rather than degrading to a stamp that is quietly absent.
        print(str(exc), file=sys.stderr)
        return 1
    except RepoRootRefused as exc:
        # The refusal is the whole message (`corpus_root.corpus_root_refusal`);
        # stderr and a non-zero status, so a wrapper script cannot mistake a
        # refused run for a generated snapshot.
        print(str(exc), file=sys.stderr)
        return 1


# ---------------------------------------------------------------------------
# THE MOVED SURFACE, RE-EXPORTED (`split-opendox-two-layer-product` § 2.4,
# PR 4 of 4)
#
# The verbs below now live in the column modules beside this one, and are bound
# back onto `cli` because THIS module is the name every caller already holds:
# `build_parser` sets `func=cmd_create`, and the suite asserts `args.func is
# cli_mod.cmd_gate_edit_document`. A re-export keeps those identities exact —
# the same function object under both names — so the move is invisible to every
# caller, which is the whole claim this PR makes.
#
# At the BOTTOM of the file on purpose: the column modules resolve this module
# lazily (`_core()`), so the direction of the dependency is decided here, once,
# and neither import order can produce a half-initialised module.
# ---------------------------------------------------------------------------

from ideation_dashboard.cli_gate import (  # noqa: E402,F401
    cmd_gate_abandon_session, cmd_gate_cleanup_abandoned_branch,
    cmd_gate_create_document, cmd_gate_create_project, cmd_gate_demote,
    cmd_gate_derive_possibles, cmd_gate_dispose_possible, cmd_gate_edit_apply,
    cmd_gate_edit_document, cmd_gate_edit_project, cmd_gate_kickoff,
    cmd_gate_lens_add_as_cluster, cmd_gate_lens_save_recipe, cmd_gate_open_pr,
    cmd_gate_promote_to_staging, cmd_gate_propose, cmd_gate_ratify,
    cmd_gate_research_brief, cmd_gate_share_session,
)
from ideation_dashboard.cli_model_binding import (  # noqa: E402,F401
    _add_model_binding_parser, cmd_model_binding_add, cmd_model_binding_edit,
    cmd_model_binding_list, cmd_model_binding_remove,
    cmd_model_binding_set_credential,
)
from ideation_dashboard.cli_project import (  # noqa: E402,F401
    cmd_create, cmd_edit, cmd_generate,
)


if __name__ == "__main__":
    sys.exit(main())
