#!/usr/bin/env python3
"""House validator for the `sequenced_after:` realization-axis front-matter field
(release-realization / add-sequenced-after-substrate).

`openspec validate` is the EXTERNAL OpenSpec CLI and cannot be extended in-tree,
so — exactly as `scripts/validate-scope-globs.py` and the other
`scripts/validate-*.py` contract validators do — this script is the house
realization of the "Parent-declaration validation" requirement, and the pytest
gate (`tests/sequenced_after/test_validate.py::test_corpus_sequenced_after_all_validate`)
runs it over every active change on every pull request, so a malformed, dangling,
ambiguous or cyclic declaration anywhere in the corpus reds the required
`pytest-suite` check.

It imposes NO DEPTH LIMIT and NO FAN-OUT LIMIT: a two-parent declaration and a
chain deeper than any consuming gate would walk both VALIDATE. Depth, fan-out and
composition are the AUTHORIZATION POLICY of the gate that acts on a chain, and a
number baked into the neutral field would bind repositories that never adopt the
consuming axis while drifting from the one gate that enforces it. A CYCLE is
refused, because no consumer's policy can resolve a chain that revisits an id to
a root.

Usage:
    validate-sequenced-after.py [REPO_ROOT]

    REPO_ROOT defaults to the current directory. Scans REPO_ROOT/openspec/changes/
    (active changes only) and validates every proposal that DECLARES
    `sequenced_after`; resolution consults the ACTIVE and ARCHIVED corpora both,
    because a chain's root is its oldest change and therefore the first to
    archive. Exit 0 when all pass; exit 1 (naming the offending change, entry and
    rule) otherwise.

    THE PLAIN RUN ALSO REPORTS ARCHIVE-DATE AGREEMENT: every archived change's
    `archive/<YYYY-MM-DD>-<id>` directory against the `moved_on` of its ledger
    row. The two are ONE FACT — the OpenSpec CLI names that directory at the
    moment it archives — and issue #790 measured them drifting, because the CLI
    reads its own LOCAL clock and `--seed-ledger` read the machine's. The
    findings are NAMED AND COUNTED but do not change the exit status while the
    124 pre-existing rows measured on 2026-09-08 remain unrepaired;
    `--strict-archive-dates` gates on them (exit 1), and is how a repair run
    proves the count reached zero. A missing or unreadable ledger is not this
    arm's finding — `--ledger-diff` owns that class — so the arm says it did not
    run and the verdict is unchanged.

    --archive-gate CHANGE_DIR --ratified-ref REF
        Parent-declaration retention (freeze) gate. CHANGE_DIR may name either
        the change's ACTIVE or its ARCHIVED directory — the ratified-side
        proposal is always located BY CHANGE ID against REF's own tree (active
        path first, then any archived `<date>-<id>` directory), never by
        reusing CHANGE_DIR's current path, so the gate still runs after the
        change has moved from its active location to
        `openspec/changes/archive/<date>-<id>/` between ratification and
        archive. CHANGE_DIR may be absolute or relative (including `.` from
        inside the change directory itself) and MUST live under
        `openspec/changes/` of its repository, because the ratified-side lookup
        is anchored there.

        A FAILURE TO READ EITHER SIDE is a named finding with exit 2 rather
        than a traceback — EVERY `SequencedAfterError` out of the gate is
        reported that way, not an enumerated few: CHANGE_DIR is not inside a
        git work tree; REF does not name a commit (an unresolvable ref is named
        as such, NOT reported as a change absent at a resolvable one); the id
        has no proposal.md at REF at all; CHANGE_DIR carries no proposal.md IN
        THE WORKING TREE (the CURRENT declaration cannot be read, so the gate
        cannot run, and the absent file is NOT read as `ABSENT` and compared,
        which would report a mutation nobody made or a retention nobody
        earned); or the front matter on EITHER side is malformed or
        unparseable. A declaration MUTATION — the gate running and finding a
        broken freeze — is exit 1.

        THE REFUSAL SET IS NOW THE SIBLING'S. `validate-scope-globs.py`
        --archive-gate refuses the same inputs, in the same order, with the
        same exit codes; `tests/sequenced_after/test_gate_parity.py` runs both
        CLIs over one set of git fixtures and asserts it, so a future divergence
        reds a check rather than being discovered by an operator.

    --sweep
        THE CORPUS SWEEP, re-runnable: the change-id population, the
        co-modified / sole-modifier split at REQUIREMENT granularity, how many
        changes declare the field, how many declare an explicit `[]` root claim,
        the surviving prose `Sequenced-after:` headers, and THE DEEPEST DECLARED
        CHAIN it resolves. Re-running it is what makes the
        "measured, not assumed" obligation discharge over time instead of ageing
        into a stale sentence. Exit 0 — a measurement is not a gate.

    --ledger-diff
        THE PER-CHANGE SWEEP LEDGER, checked against the live corpus. Prints the
        LEDGER-DERIVED reading — or the MEASURED one when the ledger cannot be
        read, so the re-runnable report survives a broken file — and then every
        stale, missing or extra ROW BY NAME. Exit 1 when the ledger disagrees
        with the corpus — unlike `--sweep`, this IS a gate, because a ledger
        that no longer describes the corpus is a stale pin rather than a
        measurement. Exit 2 when the ledger cannot be READ AT ALL, which is a
        different fact from a stale one: a stale ledger is repaired by moving a
        row, an unreadable one by fixing the file, and reporting them under one
        code would send an author to the wrong repair.

    --seed-ledger --moved-by '#PR' [--moved-on YYYY-MM-DD] [--seeded-from SHA]
        REWRITE the ledger from the live corpus, stamping `moved_by`/`moved_on`
        on the rows that actually moved and PRESERVING the provenance of every
        row that did not. This is how an author moves a row: run it, then read
        the diff as the list of rows the change moved. `--moved-by` is REQUIRED
        — a moved row with no moving pull request is provenance nobody can
        follow. `--moved-on` defaults to TODAY IN UTC, never the machine's local
        date.

        A MOVED ROW WHOSE STATE IS `archived` TAKES ITS DIRECTORY'S DATE, not
        the run's: `moved_on` and `archive/<YYYY-MM-DD>-<id>` are one fact. An
        explicit `--moved-on` that disagrees with such a row's directory is
        REFUSED (exit 2, naming the rows and their dates) rather than silently
        overridden — a caller who typed a date and got another one written was
        told their flag was honoured when it was not.

        AN EXISTING LEDGER TOO MALFORMED TO READ DOES NOT BLOCK THE REPAIR: the
        seeder says so on stderr and rewrites from the live corpus, stamping
        EVERY row (none of the old provenance could be read, so none of it can
        be preserved) and dropping `seeded_from` unless `--seeded-from` is
        given. Refusing here would leave the only tool that can fix the file
        unusable on the only file that needs fixing.

    --repository NAME
        The declaring repository token, which decides which qualified entries
        normalize to the bare form (default: openxFactory).

    `--archive-gate`, `--sweep`, `--ledger-diff` and `--seed-ledger` are MODES
    and are mutually exclusive: combining two can only mean the caller believed
    both would run, and silently running whichever the dispatch reaches first is
    the answer to a question nobody asked.

    A FLAG OUTSIDE ITS MODE IS REFUSED FOR THE SAME REASON, rather than accepted
    and ignored. `--ratified-ref` belongs to `--archive-gate`;
    `--moved-by`, `--moved-on` and `--seeded-from` belong to `--seed-ledger`;
    `--strict-archive-dates` belongs to the plain run, which is the only place
    the archive-date arm runs. `--ledger-diff --moved-by garbage` exiting 0
    would tell a caller their flag was honoured when nothing read it.
"""
from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sequenced_after as sa  # noqa: E402


def _utc_today() -> str:
    """TODAY IN UTC — what an unspecified `--moved-on` stamps.

    `datetime.date.today()` read the MACHINE'S LOCAL clock, so a row moved at
    23:35 local recorded the previous UTC day (issue #790, the same defect
    `scripts/proposal-support.py` carried on the other side of the same
    archive). Every other date in this estate is UTC, and a provenance date
    whose meaning depends on where the author was sitting is provenance nobody
    can place.
    """
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def _validate_change(repo_root: Path, change_id: str, proposal: Path,
                     repository: str) -> list[str]:
    """Return a list of problem strings for one proposal (empty when clean)."""
    try:
        raw = sa.read_declaration(proposal)
    except sa.SequencedAfterError as exc:
        return [str(exc)]
    if raw is sa.ABSENT:
        # ABSENCE IS NOT AN ERROR AND IS NOT A ROOT CLAIM. The change has made no
        # declaration about its chain position; the prose sequencing obligation
        # remains sufficient for every purpose other than a mechanical walk.
        return []
    try:
        sa.validate_declaration(repo_root, change_id, raw,
                                declaring_repository=repository)
    except sa.SequencedAfterError as exc:
        return [str(exc)]
    return []


def _archive_date_arm(repo_root: Path) -> tuple[list[str], str | None]:
    """The archive-date findings, or the reason the arm could not run.

    The ledger is READ HERE and nowhere else on this path, and a ledger that is
    missing or unparseable is NOT this arm's finding: `--ledger-diff` owns
    ledger readability and answers it with exit 2, a status this run does not
    have and must not invent. So the arm says it could not run, and the plain
    run's own verdict is untouched.
    """
    path = sa.ledger_path(repo_root)
    if not path.is_file():
        return [], f"there is no per-change sweep ledger at {path}"
    try:
        ledger = sa.load_ledger(path)
    except sa.SequencedAfterError as exc:
        return [], (f"the per-change sweep ledger could not be read ({exc}); "
                    "--ledger-diff reports that class")
    return sa.archive_date_problems(repo_root, ledger), None


def validate_corpus(repo_root: Path, repository: str,
                    strict_archive_dates: bool = False) -> int:
    problems: list[str] = []
    declared = 0
    active = sa.active_change_dirs(repo_root)
    for change_id, change_dir in active.items():
        proposal = change_dir / "proposal.md"
        if not proposal.is_file():
            continue
        try:
            if sa.read_declaration(proposal) is not sa.ABSENT:
                declared += 1
        except sa.SequencedAfterError:
            pass  # reported by _validate_change below
        for problem in _validate_change(repo_root, change_id, proposal, repository):
            problems.append(f"{change_id}: {problem}")
    if problems:
        print("sequenced_after validation FAILED:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"sequenced_after validation passed ({len(active)} active changes, "
          f"{declared} declaring the field).")

    # THE ARCHIVE-DATE ARM, AND IT WARNS RATHER THAN GATES — a disclosed,
    # measured, temporary class, not a preference. It was measured against this
    # corpus when it was written (2026-09-08): 124 of the 143 archived rows
    # already disagree with their directories, because `moved_on` has until now
    # meant "the date this row was last re-seeded" and a row is re-seeded by
    # every change that touches it. Shipping the arm as an ERROR would red the
    # required `pytest-suite` check on 124 rows that no author in flight put
    # there and that this pull request deliberately does NOT re-seed (a
    # repair of 124 provenance stamps is its own act, with its own pull
    # request to stamp them with). So: NAMED, COUNTED and PRINTED on every
    # plain run, gating on none of them, and `--strict-archive-dates` is the
    # switch the repair flips — it is what proves the count reached zero, and
    # what a follow-up makes the default.
    findings, unavailable = _archive_date_arm(repo_root)
    if unavailable is not None:
        print(f"archive-date arm NOT RUN: {unavailable}.")
        return 0
    if findings:
        label = "FAILED" if strict_archive_dates else "WARNING"
        print(f"archive-date agreement {label} ({len(findings)} archived "
              f"row(s) whose moved_on is not the date on their directory):")
        for problem in findings:
            print(f"  - {problem}")
        if strict_archive_dates:
            return 1
        print("  These are REPORTED, not gated: an archived row's moved_on has "
              "historically recorded the last re-seed rather than the archive. "
              "`--strict-archive-dates` gates on them, and is what a repair "
              "run proves itself with.")
        return 0
    print("archive-date agreement passed (every archived row's moved_on is the "
          "date on its directory).")
    return 0


def _archive_gate(change_dir: Path, ratified_ref: str) -> int:
    try:
        problem = sa.retention_at_archive(change_dir, ratified_ref)
    except (sa.SequencedAfterError, subprocess.CalledProcessError) as exc:
        # UNRUNNABLE IS NOT A MUTATION FINDING (exit 1) AND NOT A TRACEBACK.
        # THE CATCH IS DELIBERATELY ON THE WHOLE ERROR CLASS, not on an
        # enumerated few: the id names no proposal.md at `ratified_ref`,
        # CHANGE_DIR carries no proposal.md in the working tree so the
        # current-side declaration cannot be read, the front matter on either
        # side does not parse — every one of them is the same distinct fact,
        # that the gate could not READ what it compares, and every one is
        # reported the way every other refusal in this CLI is: a named finding
        # and exit 2, the same shape `validate-scope-globs.py` uses for its own
        # gate. A new refusal added to the substrate lands here correctly
        # without this comment having to be revised.
        #
        # `CalledProcessError` is caught BESIDE it as a backstop, the same way
        # `validate-scope-globs.py` does: no git call on this path is expected
        # to reach the caller unhandled any more — the work-tree probe and the
        # ref-commit probe are the two that used to — and if one ever does, it
        # is still reported rather than traced.
        print("sequenced_after PARENT-DECLARATION-RETENTION gate CANNOT RUN:")
        print(f"  - {exc}")
        return 2
    if problem is not None:
        print("sequenced_after PARENT-DECLARATION-RETENTION gate FAILED (contested):")
        print(f"  - {problem}")
        return 1
    print("sequenced_after retention gate passed (declaration unchanged since "
          "ratification).")
    return 0


def _ledger_diff(repo_root: Path, repository: str) -> int:
    """Report the ledger against the live corpus. Exit 1 when it is stale.

    Prints the LEDGER-DERIVED reading where the ledger can be read, and the
    MEASURED one otherwise, so the re-runnable report survives a stale file.
    """
    readings = sa.classify_corpus(repo_root, declaring_repository=repository)
    measured = sa.corpus_sweep(repo_root, declaring_repository=repository)
    problems: list[str] = []
    path = sa.ledger_path(repo_root)
    ledger = None
    if not path.is_file():
        problems.append(f"malformed ledger: {path} does not exist")
    else:
        try:
            ledger = sa.load_ledger(path)
        except sa.SequencedAfterError as exc:
            # UNREADABLE IS NOT STALE. Exit 2 rather than 1, because the two
            # want different repairs: a stale ledger is fixed by re-seeding a
            # row, an unreadable one by fixing the file it could not parse.
            print(measured.render())
            print()
            print(f"per-change sweep ledger CANNOT BE READ:\n  - {exc}")
            print("Fix the file, or rewrite it with: python3 "
                  "scripts/validate-sequenced-after.py . --seed-ledger "
                  "--moved-by '#<PR>'")
            return 2
    if ledger is not None:
        problems.extend(sa.ledger_problems(readings, ledger))
        try:
            derived = sa.sweep_from_readings(sa.readings_from_ledger(ledger))
        except sa.SequencedAfterError as exc:
            problems.append(str(exc))
            derived = None
    else:
        derived = None
    if derived is not None:
        print(derived.render())
        problems.extend(sa.sweep_mismatches(derived, measured))
    else:
        print(measured.render())
    print()
    if problems:
        print(f"per-change sweep ledger STALE ({len(problems)} finding(s)):")
        for problem in problems:
            print(f"  - {problem}")
        print("Re-seed with: python3 scripts/validate-sequenced-after.py . "
              "--seed-ledger --moved-by '#<PR>'")
        return 1
    print(f"per-change sweep ledger consistent with the corpus "
          f"({len(readings)} rows).")
    return 0


def _seed_ledger(repo_root: Path, repository: str, moved_by: str,
                 moved_on: str | None, seeded_from: str | None) -> int:
    """Rewrite the ledger from the live corpus, preserving unmoved provenance.

    EVERY refusal below the CLI arrives as a MESSAGE AND AN EXIT CODE, never as
    a traceback: a stack trace tells an author where the library gave up and
    not what they should type instead, and this command's whole purpose is to
    be the thing an author runs when something is wrong with the ledger.
    """
    try:
        return _seed_ledger_inner(repo_root, repository, moved_by, moved_on,
                                  seeded_from)
    except sa.SequencedAfterError as exc:
        print(f"--seed-ledger refused: {exc}", file=sys.stderr)
        return 2


def _seed_ledger_inner(repo_root: Path, repository: str, moved_by: str,
                       moved_on: str | None, seeded_from: str | None) -> int:
    readings = sa.classify_corpus(repo_root, declaring_repository=repository)
    path = sa.ledger_path(repo_root)
    previous = None
    if path.is_file():
        try:
            previous = sa.load_ledger(path)
        except sa.SequencedAfterError as exc:
            # THE SEEDER IS THE REPAIR. Refusing to read a broken ledger would
            # leave the only tool that can rewrite it unusable on the only file
            # that needs rewriting, so it says what it could not read and
            # re-seeds from the corpus instead.
            print(f"the existing ledger could not be read ({exc}); re-seeding "
                  f"from the live corpus, so EVERY row is stamped "
                  f"{moved_by} and `seeded_from` is dropped unless "
                  f"--seeded-from is given", file=sys.stderr)
    # THE ROWS THIS RUN MOVES, from the same helper the renderer stamps by, so
    # the summary cannot overcount: a row that merely already carried this pull
    # request is NOT one this run moved.
    moved = sa.moved_rows(readings, previous)
    dates = sa.archive_dates(repo_root)
    # AN EXPLICIT `--moved-on` THAT THE ARCHIVE DIRECTORIES CONTRADICT IS
    # REFUSED, never quietly overridden. An archived row's `moved_on` and its
    # `archive/<YYYY-MM-DD>-<id>` directory are ONE FACT (issue #790), so the
    # directory wins — but a caller who typed a date and got a different one
    # written was told their flag was honoured when it was not, which is the
    # same mistake `_mode_only` refuses one level up.
    if moved_on is not None:
        disagreeing = [
            (change_id, dates[change_id]) for change_id in moved
            if readings[change_id].state == sa.STATE_ARCHIVED
            and change_id in dates and dates[change_id] != moved_on]
        if disagreeing:
            listed = ", ".join(f"{cid} ({on})" for cid, on in disagreeing[:5])
            more = ("" if len(disagreeing) <= 5
                    else f", … and {len(disagreeing) - 5} more")
            raise sa.SequencedAfterError(
                f"--moved-on {moved_on!r} disagrees with the archived "
                f"directory of {len(disagreeing)} row(s) this re-seed moves: "
                f"{listed}{more}. An archived row's moved_on IS the date its "
                f"archive/<YYYY-MM-DD>-<id> directory carries — they are one "
                f"fact — so a re-seed cannot stamp another day on it. Drop "
                f"--moved-on (an archived row then takes its directory's date "
                f"and every other row takes today in UTC), or pass the date "
                f"those directories carry")
    text = sa.render_ledger(
        readings, moved_by=moved_by,
        moved_on=moved_on or _utc_today(),
        previous=previous, seeded_from=seeded_from, archive_dates=dates)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path} ({len(readings)} rows, {len(moved)} moved by "
          f"{moved_by}).")
    for change_id in moved[:20]:
        print(f"  - {change_id}")
    if len(moved) > 20:
        print(f"  … and {len(moved) - 20} more; read the diff.")
    return 0


def _mode_only(parser: argparse.ArgumentParser, args: argparse.Namespace,
               flag: str, given: bool, mode: str, mode_selected: object) -> None:
    """Refuse `flag` unless `mode` is the selected mode."""
    if given and not mode_selected:
        parser.error(f"{flag} is only meaningful with {mode}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to scan (default: cwd)")
    # THE MODES ARE MUTUALLY EXCLUSIVE, declared rather than resolved by the
    # order of the dispatch below: combining two of them can only mean the
    # caller believed both would run, and silently running the first is the
    # answer to a question nobody asked.
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--archive-gate", metavar="CHANGE_DIR",
                       help="run the parent-declaration retention freeze gate "
                            "on one change dir")
    parser.add_argument("--ratified-ref", metavar="REF",
                        help="git ref carrying the ratified proposal (with "
                             "--archive-gate)")
    modes.add_argument("--sweep", action="store_true",
                       help="print the re-runnable corpus sweep (a measurement, "
                            "not a gate) and exit 0")
    modes.add_argument("--ledger-diff", action="store_true",
                       help="check the per-change sweep ledger against the "
                            "live corpus, naming every stale row; exit 1 when "
                            "it is stale")
    modes.add_argument("--seed-ledger", action="store_true",
                       help="rewrite the per-change sweep ledger from the live "
                            "corpus, preserving the provenance of unmoved rows")
    parser.add_argument("--moved-by", metavar="#PR",
                        help="the pull request stamped on the rows this "
                             "re-seed moves; REQUIRED with --seed-ledger")
    parser.add_argument("--moved-on", metavar="YYYY-MM-DD",
                        help="the date stamped on the rows this re-seed moves "
                             "(default: today)")
    parser.add_argument("--seeded-from", metavar="SHA",
                        help="record the commit the ledger was first seeded "
                             "from; omitted, the existing value is preserved")
    parser.add_argument("--strict-archive-dates", action="store_true",
                        help="gate on the archive-date agreement arm (exit 1) "
                             "instead of only reporting it; the plain run "
                             "WARNS while the pre-existing rows are unrepaired")
    parser.add_argument("--repository", default=sa.DECLARING_REPOSITORY,
                        help="declaring repository token (default: "
                             f"{sa.DECLARING_REPOSITORY})")
    args = parser.parse_args(argv)

    # A FLAG OUTSIDE ITS MODE IS REFUSED, NOT SILENTLY IGNORED. The modes
    # already refuse to combine on the reasoning that "combining two can only
    # mean the caller believed both would run"; accepting `--ledger-diff
    # --moved-by garbage` and exiting 0 is the same mistake wearing a different
    # hat — the caller believed the flag did something, and it did nothing.
    _mode_only(parser, args, "--ratified-ref", args.ratified_ref is not None,
               "--archive-gate", args.archive_gate)
    if args.strict_archive_dates and (args.archive_gate or args.sweep
                                      or args.ledger_diff or args.seed_ledger):
        parser.error("--strict-archive-dates is only meaningful on the plain "
                     "validation run, which is where the archive-date arm runs")
    for flag, given in (("--moved-by", args.moved_by is not None),
                        ("--moved-on", args.moved_on is not None),
                        ("--seeded-from", args.seeded_from is not None)):
        _mode_only(parser, args, flag, given, "--seed-ledger", args.seed_ledger)

    if args.archive_gate:
        if not args.ratified_ref:
            parser.error("--archive-gate requires --ratified-ref")
        # A RELATIVE CHANGE_DIR RESOLVES AGAINST `repo_root`, like every other
        # mode's paths, not against the current directory. Absolute paths are
        # unaffected, and so is the ordinary `--archive-gate openspec/changes/x`
        # run from the repo root, `repo_root` defaulting to `.`. What changes is
        # `validate-sequenced-after.py path/to/repo --archive-gate
        # openspec/changes/x`, which resolved against the CWD: at best it failed
        # to find the directory, and at worst it found a DIFFERENT repository's
        # change of the same name and gated THAT — the failure mode a gate can
        # least afford, because it passes.
        change_dir = Path(args.archive_gate)
        if not change_dir.is_absolute():
            change_dir = Path(args.repo_root) / change_dir
        return _archive_gate(change_dir, args.ratified_ref)

    if args.ledger_diff:
        return _ledger_diff(Path(args.repo_root), args.repository)

    if args.seed_ledger:
        # ARGUMENT SHAPE IS ARGPARSE'S TO REFUSE, at the boundary and in its own
        # voice, rather than a library exception surfacing as a stack trace six
        # frames down.
        if not args.moved_by:
            parser.error("--seed-ledger requires --moved-by '#<PR>'")
        if not sa.MOVED_BY.match(args.moved_by):
            parser.error(f"--moved-by must be a pull request reference like "
                         f"'#620', not {args.moved_by!r}")
        if args.moved_on is not None and not sa.is_moved_on(args.moved_on):
            parser.error(f"--moved-on must be an ISO date (YYYY-MM-DD), not "
                         f"{args.moved_on!r}")
        return _seed_ledger(Path(args.repo_root), args.repository,
                            args.moved_by, args.moved_on, args.seeded_from)

    if args.sweep:
        print(sa.corpus_sweep(Path(args.repo_root),
                              declaring_repository=args.repository).render())
        return 0

    return validate_corpus(Path(args.repo_root), args.repository,
                           strict_archive_dates=args.strict_archive_dates)


if __name__ == "__main__":
    raise SystemExit(main())
