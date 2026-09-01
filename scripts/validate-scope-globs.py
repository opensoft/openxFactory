#!/usr/bin/env python3
"""House validator for the `scope_globs:` realization-axis front-matter field
(release-realization / add-structured-scope-substrate).

`openspec validate` is the EXTERNAL OpenSpec CLI and cannot be extended in-tree,
so — exactly as the other `scripts/validate-*.py` contract validators do — this
script is the house realization of the "Structured path-scope validation"
requirement, and the pytest gate
(`tests/scope_globs/test_validate.py::test_corpus_scope_globs_all_validate`) runs
it over every active change on every pull request, so a malformed or non-dialect
`scope_globs` anywhere in the corpus reds the required `pytest-suite` check.

Every check is FLOOR-AGNOSTIC: the never-clearable floor is tree-specific and
per-repository and is applied at CHECK time by the downstream provenance-tie
verifier, never here.

Usage:
    validate-scope-globs.py [REPO_ROOT]

    REPO_ROOT defaults to the current directory. Scans REPO_ROOT/openspec/changes/
    (active changes only, never archive/) and validates every proposal that
    declares `scope_globs`. Exit 0 when all pass; exit 1 (naming the offending
    change, entry, and rule) otherwise.

    --archive-gate CHANGE_DIR --ratified-ref REF
        Scope-retention (freeze) gate — see the `scope-globs-integrity` feature.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scope_globs as sg  # noqa: E402


def _validate_change(proposal: Path) -> list[str]:
    """Return a list of problem strings for one proposal (empty when clean)."""
    try:
        front = sg.read_front_matter(proposal)
    except sg.ScopeGlobsError as exc:
        return [str(exc)]
    raw = front.get("scope_globs")
    if raw is None:
        return []  # absence is the fail-closed default, not an error
    try:
        sg.validate_scope_globs(
            raw, code_surface_repos=sg.code_surface_repositories(front)
        )
    except sg.ScopeGlobsError as exc:
        return [str(exc)]
    return []


def validate_corpus(repo_root: Path) -> int:
    changes = repo_root / "openspec" / "changes"
    problems: list[str] = []
    if changes.is_dir():
        for change_dir in sorted(changes.iterdir()):
            if not change_dir.is_dir() or change_dir.name == "archive":
                continue
            proposal = change_dir / "proposal.md"
            if not proposal.is_file():
                continue
            for problem in _validate_change(proposal):
                problems.append(f"{change_dir.name}: {problem}")
    if problems:
        print("scope_globs validation FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("scope_globs validation passed (all active changes conform).")
    return 0


def _archive_gate(change_dir: Path, ratified_ref: str) -> int:
    problem = sg.scope_retention_at_archive(change_dir, ratified_ref)
    if problem is not None:
        print("scope_globs SCOPE-RETENTION gate FAILED (contested):")
        print(f"  - {problem}")
        return 1
    print("scope_globs scope-retention gate passed (scope unchanged since ratification).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to scan (default: cwd)")
    parser.add_argument("--archive-gate", metavar="CHANGE_DIR",
                        help="run the scope-retention freeze gate on one change dir")
    parser.add_argument("--ratified-ref", metavar="REF",
                        help="git ref carrying the ratified proposal (with --archive-gate)")
    args = parser.parse_args(argv)

    if args.archive_gate:
        if not args.ratified_ref:
            parser.error("--archive-gate requires --ratified-ref")
        return _archive_gate(Path(args.archive_gate), args.ratified_ref)

    return validate_corpus(Path(args.repo_root))


if __name__ == "__main__":
    raise SystemExit(main())
