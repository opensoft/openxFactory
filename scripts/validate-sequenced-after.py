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

    --archive-gate CHANGE_DIR --ratified-ref REF
        Parent-declaration retention (freeze) gate.

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
        follow. `--moved-on` defaults to today.

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
    `--moved-by`, `--moved-on` and `--seeded-from` belong to `--seed-ledger`.
    `--ledger-diff --moved-by garbage` exiting 0 would tell a caller their flag
    was honoured when nothing read it.
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sequenced_after as sa  # noqa: E402


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


def validate_corpus(repo_root: Path, repository: str) -> int:
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
    return 0


def _archive_gate(change_dir: Path, ratified_ref: str) -> int:
    problem = sa.retention_at_archive(change_dir, ratified_ref)
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
    text = sa.render_ledger(
        readings, moved_by=moved_by,
        moved_on=moved_on or datetime.date.today().isoformat(),
        previous=previous, seeded_from=seeded_from)
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

    return validate_corpus(Path(args.repo_root), args.repository)


if __name__ == "__main__":
    raise SystemExit(main())
