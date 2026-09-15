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
    change, entry, and rule) otherwise; exit 2 when the scan CANNOT RUN.

    DISCOVERY IS THE SIBLING'S GUARDED WALK, NOT A BARE `is_file()` SCAN.
    `code_surface._proposals` is called for the active corpus, so this gate and
    the code-surface gate judge THE SAME PROPOSALS — every candidate path taken
    through `code_surface._unescaped`, which resolves both sides and requires
    the path to land where a symlink-free tree would have put it. `Path.is_dir()`
    and `Path.is_file()` FOLLOW SYMLINKS, so the plain walk this replaced read a
    symlinked `openspec/changes/<id>/proposal.md` — or an ordinary `proposal.md`
    inside a symlinked CHANGE DIRECTORY, or anything under a symlinked
    `openspec/` — as an active proposal of the scanned tree. That mattered here
    once the cross-consistency check became a CODE-SURFACE CONSUMER: bytes
    outside the tree supplied the `code_surface:` declaration the scope key is
    checked against, and matched the register entry the refusal names, so the
    escaped document could both grant an authorization the tree never declared
    and be judged as one the tree carries. The escape is DROPPED rather than
    reported, for `_unescaped`'s own reason: neither face of it is a judgment
    about the scanned tree, which is the only thing this gate may make.

    --code-surface-register PATH
        Read the CODE-SURFACE register (`gate-code-surface-declarations`) from
        PATH. The cross-consistency check derives each change's declared
        repository set from its `code_surface:` HEAD, and where that head is one
        the grammar cannot read the refusal must name the REGISTER ENTRY that
        tolerates it — so the register has to be the one belonging to the tree
        being SCANNED. THE FLAG IS SPELLED FOR THE FIELD IT BELONGS TO rather
        than as the sibling's bare `--register`, because this validator's own
        subject is `scope_globs:` and an unqualified "register" here would read
        as a register of scopes.

        RESOLUTION ORDER, AND THE REASON FOR EACH STEP. With the flag, PATH is
        used and a register that cannot be used REFUSES (exit 2), the sibling's
        semantics: an operator who named a file is owed a refusal rather than a
        silent fallback. Without it, `REPO_ROOT/scripts/code-surface-register.yaml`
        is used when it exists — so a scanned tree is judged against ITS OWN
        exceptions and not against whichever register happens to sit beside the
        imported module, which for REPO_ROOT `.` in this repository is the same
        file either way. With neither, the derivation's own on-demand load
        applies: an absent exception file yields an entry-less refusal rather
        than an exception, because the absence of an exception file may never
        turn a fail-closed into a fail-open.

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


def _code_surface():
    """The sibling `scripts/code_surface.py`, imported ON FIRST USE.

    IMPORTED HERE AND NOT AT MODULE LEVEL, on `scope_globs._code_surface()`'s
    reason: the import is paid only on the paths that need it, and an absent
    sibling arrives as a NAMED FINDING rather than as an import traceback out
    of a gate.

    THE OLD CLAIM THAT THIS CLI "MUST KEEP RUNNING IN A TREE THAT DOES NOT
    CARRY `scripts/code_surface.py`" IS CORRECTED HERE, WHERE IT WAS MADE, and
    it never held for the corpus scan anyway: `code_surface_repositories` calls
    the sibling for every proposal whose `code_surface:` is present and
    readable, so a sibling-less tree already refused every real proposal in
    this repository. What is true, and all that is claimed now, is that
    `--archive-gate` needs NO `code_surface` (the scope-retention freeze reads
    `scope_globs:` on both sides and nothing else; it DOES need
    `sequenced_after`, a separate sibling and a separate fact — the first
    wording of this paragraph said "sibling-free", and the test written to pin
    it FAILED on that sibling, which is how the overclaim was caught), and that
    module IMPORT needs neither.
    THE CORPUS SCAN NOW REQUIRES THE SIBLING OUTRIGHT, because its guarded walk
    is the sibling's, and a guard that silently disappears when a file is
    missing is exactly the fail-closed-turned-fail-open this module refuses
    elsewhere. Missing, the scan REFUSES (exit 2) and names what to copy.
    """
    import code_surface as cs  # deliberate local import, see the docstring
    return cs


def _load_code_surface_register(path: Path) -> list[dict]:
    """The code-surface register at `path`, loaded through the sibling reader."""
    return _code_surface().load_register(path)


def _validate_change(proposal: Path,
                     register: list[dict] | None = None) -> list[str]:
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
        #
        # AND SO DOES THE REGISTER, FOR THE OTHER HALF OF THE SAME REFUSAL.
        # Left to load itself, the derivation reads the register beside the
        # IMPORTED MODULE, which is the right file only when the scanned tree
        # IS this one — so for a temp or consuming tree an entry that tree
        # carries reads as unregistered and the refusal cannot name it.
        # `main` resolves the register against REPO_ROOT and passes it down.
        sg.validate_scope_globs(
            raw,
            code_surface_repos=sg.code_surface_repositories(
                front, change=proposal.parent.name, register=register),
        )
    except sg.ScopeGlobsError as exc:
        return [str(exc)]
    return []


def _active_proposals(repo_root: Path) -> list[Path]:
    """Every ACTIVE `proposal.md` the scanned tree REALLY carries.

    THE SIBLING'S WALK, CALLED — NOT A SECOND COPY OF IT. `code_surface`
    already owns the anchored path check (`_unescaped`: resolve `repo_root` and
    the candidate, and require the candidate to land exactly where a
    symlink-free tree would have put it, which closes an escape at EVERY
    component in one comparison) and already applies it to `openspec/changes`,
    to each change directory and to each `proposal.md`, one level deep, skipping
    `archive/`. That is this walk, to the letter, and calling it is what makes
    the two gates provably judge the SAME corpus rather than two corpora that
    agree until a symlink separates them — which is pinned by
    `test_the_two_gates_walk_THE_SAME_CORPUS`.

    The returned paths are `repo_root / openspec / changes / <id> / proposal.md`
    UNRESOLVED, so `proposal.parent.name` is still the change id.
    """
    return _code_surface()._proposals(repo_root, archived=False)


def validate_corpus(repo_root: Path,
                    register: list[dict] | None = None) -> int:
    try:
        proposals = _active_proposals(repo_root)
    except Exception as exc:  # reported as a finding, never traced
        # THE GUARD IS NOT OPTIONAL, SO ITS ABSENCE REFUSES. Scanning on with a
        # bare `is_file()` walk would be a fail-closed silently becoming a
        # fail-open — the precise thing the register resolution below refuses to
        # do — so a sibling that cannot be loaded stops the scan and says what
        # to copy, in this CLI's own "CANNOT RUN … exit 2" shape.
        print("scope_globs validation CANNOT RUN:")
        print(f"  - the corpus walk is guarded by the sibling module "
              f"`code_surface` (its anchored `_unescaped` path check), and it "
              f"could not be loaded: {exc}. Copy `scripts/code_surface.py` "
              f"beside this validator. The scan does NOT fall back to an "
              f"unguarded walk: a symlinked proposal or change directory would "
              f"then supply a `code_surface:` declaration, and a register "
              f"match, from bytes outside the tree being judged")
        return 2
    problems: list[str] = []
    for proposal in proposals:
        for problem in _validate_change(proposal, register):
            problems.append(f"{proposal.parent.name}: {problem}")
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
    parser.add_argument("--code-surface-register", metavar="PATH", default=None,
                        help="code-surface register for the scanned tree "
                             "(default: REPO_ROOT/scripts/"
                             "code-surface-register.yaml when it exists)")
    args = parser.parse_args(argv)

    if args.archive_gate:
        if not args.ratified_ref:
            parser.error("--archive-gate requires --ratified-ref")
        return _archive_gate(Path(args.archive_gate), args.ratified_ref)

    repo_root = Path(args.repo_root)
    register: list[dict] | None = None
    if args.code_surface_register:
        # NAMED BY AN OPERATOR, SO A FAILURE IS A REFUSAL AND NOT A FALLBACK.
        try:
            register = _load_code_surface_register(
                Path(args.code_surface_register))
        except Exception as exc:  # reported as a finding, never traced
            print("scope_globs validation CANNOT RUN:")
            print(f"  - the code-surface register "
                  f"{args.code_surface_register} cannot be used: {exc}")
            return 2
    else:
        default = repo_root / "scripts" / "code-surface-register.yaml"
        if default.is_file():
            # UNNAMED AND PRESENT: used, but a failure here falls back to the
            # derivation's own on-demand load rather than refusing, because
            # nobody named this file and an exception file that cannot be read
            # must never turn a fail-closed into a fail-open.
            try:
                register = _load_code_surface_register(default)
            except Exception:  # see the comment above
                register = None

    return validate_corpus(repo_root, register)


if __name__ == "__main__":
    raise SystemExit(main())
