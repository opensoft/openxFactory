#!/usr/bin/env python3
"""House validator for the landing arrival of a declared former identity
(`release-realization` / `add-declared-former-id`, `tasks.md` § 2.4 and § 4).

The CLI half of `scripts/former_id_arrival.py`, which carries the whole of the
reasoning. In the shape `gate-realization-axis-vocabulary` established and
this repository already runs: a module under `scripts/`, this validator beside
it, and `tests/former_id_arrival/test_former_id_arrival.py` exercising both
over fixtures and over the live corpus.

WHAT IT JUDGES

  1. THE RANGE ARM — every commit of this pull request's own range, asked one
     at a time: did a change packet directory arrive HERE by a MOVE from
     another change packet directory whose identity has EVER declared
     `Status: ratified`, and if so does the arriving packet declare that move
     in `former_ids:` IN THE SAME COMMIT? Plus the two rules that bind a
     declaration to the commit that writes it: an entry is added only by the
     commit that performs the move it records, and the list is append-only
     ACROSS commits and not only within one.
  2. THE CORPUS ARM — the whole-tree declaration sweep: the `former_ids:`
     shape, a declared id that still STANDS as a live directory, and the
     ownership sweep that says a former identity has exactly one owner. This
     arm runs on every invocation, range or no range.

Usage:
    validate-former-id-arrival.py [REPO_ROOT] [--base REV] [--head REV]

    REPO_ROOT defaults to the current directory.

    exit 0  no landing in the range is refused and the corpus declares
            nothing this gate refuses.
    exit 1  `former-id-undeclared` — a landing brings a packet in by a move
            from a ratified identity and does not declare it — or a
            declaration refusal from the corpus sweep. The refusal names the
            commit, the source path, the destination path and the one repair.
    exit 2  `former-id-arrival-unreadable` — CANNOT RUN. A read this checkout
            could not perform, named. A checkout that cannot read its own
            history refuses rather than reporting that no arrival was found.

    --base REV / --head REV
        NAME the commit range instead of deriving it from the checkout. On a
        GitHub `pull_request` run neither is passed and the range is
        `HEAD^1..HEAD^2` — the checkout is the merge commit GitHub built, so
        its first parent is the base tip and its second is the pull request
        head. Outside such a run, with neither flag, there is no range: the
        corpus arm runs alone and the report SAYS SO rather than reporting a
        clean range it never read.

THERE IS NO BYPASS FLAG, and there is not going to be one (#690, and
`design.md` D3 in as many words): *"a flag would be the declaration nobody
writes"*. `--base`/`--head` are not one — they name which commits are read,
they cannot silence a refusal taken over the commits they name, the corpus arm
runs regardless of them, and CI passes neither.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import former_id_arrival as fia  # noqa: E402


def _report(report: fia.Report) -> None:
    print(f"former-id arrival gate: {report.range_note}.")
    if report.base is not None:
        print(f"  moves paired: {report.moves_seen} packet-directory "
              f"move(s) — {report.moves_excepted_archive} archive "
              f"relocation(s) excepted by id, {report.moves_unqualified} of "
              f"a packet no identity of which has ever declared "
              f"`Status: ratified`.")
    print(f"  corpus sweep: {report.active_packets} active and "
          f"{report.archived_packets} archived packet(s) read for their "
          f"`former_ids:` declaration, their standing ids and the ownership "
          f"of every identity claimed.")


def parser() -> argparse.ArgumentParser:
    """THE WHOLE COMMAND LINE, in one place a test can read.

    `tests/former_id_arrival/test_former_id_arrival.py::
    test_there_is_no_bypass_flag` enumerates every option string this returns
    and asserts that none of them is a bypass. A flag would be the declaration
    nobody writes, and the cheapest way for one to appear is for it to be
    added where nothing enumerates it.
    """
    built = argparse.ArgumentParser(
        description="Refuse an undeclared rename arrival at its landing.")
    built.add_argument("repo_root", nargs="?", default=".",
                       help="repository root to scan (default: cwd)")
    built.add_argument("--base", metavar="REV", default=None,
                       help="base revision of the range (default: derived "
                            "from the checkout)")
    built.add_argument("--head", metavar="REV", default=None,
                       help="head revision of the range (default: derived "
                            "from the checkout)")
    return built


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)

    try:
        report = fia.scan(Path(args.repo_root), base=args.base,
                          head=args.head)
    except fia.ArrivalCannotRun as exc:
        print("former-id arrival gate CANNOT RUN:")
        print(f"  - {exc}")
        return 2
    except fia.support.FormerIdError as exc:
        print("former-id arrival gate FAILED:")
        print(f"  - {exc}")
        return 1

    _report(report)

    if report.findings:
        arrivals = [f for f in report.findings if f.status == fia.UNDECLARED]
        declarations = [f for f in report.findings if f.status is None]
        print("former-id arrival gate FAILED:")
        for finding in arrivals:
            print(f"  - [{finding.status}] {finding.message}")
        if declarations:
            print(f"  the declaration refusals this gate also carries "
                  f"(`release-realization` § \"{fia.DECLARATION_REQUIREMENT}\""
                  f"), which name no status token of their own:")
            for finding in declarations:
                print(f"  - {finding.message}")
        return 1

    print("former-id arrival gate passed (every packet-directory move in "
          "range is a draft's, an archive relocation, or declared).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
