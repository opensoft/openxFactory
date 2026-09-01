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

    --repository NAME
        The declaring repository token, which decides which qualified entries
        normalize to the bare form (default: openxFactory).
"""
from __future__ import annotations

import argparse
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to scan (default: cwd)")
    parser.add_argument("--archive-gate", metavar="CHANGE_DIR",
                        help="run the parent-declaration retention freeze gate "
                             "on one change dir")
    parser.add_argument("--ratified-ref", metavar="REF",
                        help="git ref carrying the ratified proposal (with "
                             "--archive-gate)")
    parser.add_argument("--sweep", action="store_true",
                        help="print the re-runnable corpus sweep (a measurement, "
                             "not a gate) and exit 0")
    parser.add_argument("--repository", default=sa.DECLARING_REPOSITORY,
                        help="declaring repository token (default: "
                             f"{sa.DECLARING_REPOSITORY})")
    args = parser.parse_args(argv)

    if args.archive_gate:
        if not args.ratified_ref:
            parser.error("--archive-gate requires --ratified-ref")
        return _archive_gate(Path(args.archive_gate), args.ratified_ref)

    if args.sweep:
        print(sa.corpus_sweep(Path(args.repo_root),
                              declaring_repository=args.repository).render())
        return 0

    return validate_corpus(Path(args.repo_root), args.repository)


if __name__ == "__main__":
    raise SystemExit(main())
