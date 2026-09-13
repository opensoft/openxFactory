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
        CHANGE_DIR may name either the change's ACTIVE or its ARCHIVED
        directory — the ratified-side proposal is always located BY CHANGE ID
        against REF's own tree (active path first, then any archived
        `<date>-<id>` directory), never by reusing CHANGE_DIR's current path, so
        the gate still runs after the change has moved from its active location
        to `openspec/changes/archive/<date>-<id>/` between ratification and
        archive. CHANGE_DIR may be absolute or relative (including `.` from
        inside the change directory itself) and MUST live under
        `openspec/changes/` of its repository, because the ratified-side lookup
        is anchored there.

        EVERY failure of this gate to RUN is a named finding with exit 2, never
        a traceback: the id has no proposal.md at REF, REF does not name a
        commit, CHANGE_DIR is not inside a git work tree, CHANGE_DIR carries no
        proposal.md in the WORKING TREE, or the ratified or current front-matter
        cannot be read. A scope MUTATION — the gate running and finding a broken
        freeze — is exit 1.
"""
from __future__ import annotations

import argparse
import subprocess
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
        # THE CHANGE ID TRAVELS WITH THE FRONT MATTER (gate-code-surface-
        # declarations § 3.5b). The derivation may return the ABSENCE of a
        # head-derived repository set — for a declaration whose head the
        # ratified `code_surface:` grammar cannot read — and the refusal that
        # absence raises must name the PROPOSAL and the register entry carrying
        # its declaration. The directory name is the change id, which this
        # function already holds, so the consumer owes nothing it did not have.
        sg.validate_scope_globs(
            raw,
            code_surface_repos=sg.code_surface_repositories(
                front, change=proposal.parent.name),
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
    try:
        problem = sg.scope_retention_at_archive(change_dir, ratified_ref)
    except (sg.ScopeGlobsError, subprocess.CalledProcessError,
            OSError, ValueError) as exc:
        # UNRUNNABLE IS NOT A MUTATION FINDING (exit 1) AND NOT A TRACEBACK: the
        # id names no proposal.md at `ratified_ref`, `ratified_ref` names no
        # commit, CHANGE_DIR is not inside a work tree, or a proposal on either
        # side cannot be read at all. That is a distinct fact, reported the way
        # every other refusal in this CLI is — a named finding and exit 2, the
        # same shape `validate-sequenced-after.py` uses for its own gate.
        #
        # The catch is on `ScopeGlobsError`, the module's BROAD class, not only
        # on the `ScopeGlobsResolutionError` subclass — so a malformed or
        # non-dialect declaration on EITHER side arrives here too, where before
        # it raised out of `main()` as a traceback (exit 1). `CalledProcessError`
        # is caught beside it as a backstop: no git call on this path is
        # expected to reach the caller unhandled, and if one ever does it is
        # still reported rather than traced. `OSError` and `ValueError` are a
        # SECOND backstop, alongside `scope_retention_at_archive`'s own
        # `Path.resolve()`/`subprocess.run` hardening: this module's own
        # docstring promises every failure to run is a named finding, never a
        # traceback, independent of which layer catches it.
        print("scope_globs SCOPE-RETENTION gate CANNOT RUN:")
        print(f"  - {exc}")
        return 2
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
