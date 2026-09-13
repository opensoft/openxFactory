#!/usr/bin/env python3
"""House validator for the `code_surface:` realization-axis declaration
(release-realization / gate-code-surface-declarations).

`openspec validate` is the EXTERNAL OpenSpec CLI and cannot be extended in-tree,
so — exactly as the other `scripts/validate-*.py` contract validators do, and
exactly as the sibling `scripts/validate-target-release.py` does for the other
half of the same promoted sentence — this script is the house realization of the
ADDED requirement *Code-surface declaration grammar is gated*, and the pytest
gate
(`tests/code_surface/test_code_surface_gate.py::test_corpus_code_surface_validates`)
runs it over every active change on every pull request, so a declaration whose
head no reader can parse reds the required `pytest-suite` check.

WHAT IT JUDGES, AND WHAT IT DOES NOT. Only ACTIVE proposals
(`openspec/changes/<change>/proposal.md`, ONE level deep) are judged. Archived
proposals are frozen record: they are READ and COUNTED so the run can say what
the archive carries, and refused never. A proposal that declares no
`code_surface:` at all is taking the promoted doc-only default and passes. The
DECLARED HEAD is judged and the prose GLOSS never is, and no repository name's
MEMBERSHIP of anything is checked — this repository defines no inventory of the
estate's repositories to resolve against, which is measured in the packet's
`design.md` D1 and named there as the successor that would lift the bound.

Usage:
    validate-code-surface.py [REPO_ROOT]

    REPO_ROOT defaults to the current directory.

    exit 0  every active declaration's head is one the grammar admits, or is
            named by a live register entry, and no register entry is stale.
    exit 1  at least one active declaration's head cannot be read and is not
            named by the register. The remedy belongs to the declaring packet,
            which re-punctuates its own declaration so the head ends where the
            explanation begins.
    exit 2  the register cannot be used, or an entry in it matched nothing on a
            whole-corpus scan. A stale entry is a statement about the REGISTER
            — the exception outlived the condition it was granted for — and the
            remedy is to delete the entry in the pull request that made it
            stale. The asymmetry is the sibling's and
            `scripts/validate-openspec-cli-pin.py`'s, deliberately: silently
            tolerating a stale exception is how an exception list rots into a
            blanket, and refusing makes the correction (or the archive) the
            event that forces the re-examination.

    Where BOTH occur, the run reports both and exits 1: an unreadable
    declaration is the more actionable defect and the stale block is printed
    beside it, so neither is hidden by the other.

    --register PATH
        Read the register from PATH instead of from
        `scripts/code-surface-register.yaml`. The pytest gate runs this
        validator with NO such flag, so the gate is always judged against the
        register this repository carries; the flag exists so the tests can put
        a known register in front of a known tree, and so a consuming tree that
        carries its own register can name it. A missing register REFUSES
        (exit 2) rather than defaulting to an empty one: an exception file that
        silently becomes empty would re-fail every declaration it covers.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import code_surface as cs  # noqa: E402


def _report(report: cs.Report) -> None:
    print(
        f"code_surface: {report.active_total} active proposals, "
        f"{report.active_declaring} declaring — "
        f"{report.inside_none} `none`, "
        f"{report.inside_repositories} a repository list, "
        f"{len(report.registered)} named by the register, "
        f"{len(report.findings)} outside the grammar.")
    print(
        f"  archive (read, never judged): {report.archived_total} proposals, "
        f"{report.archived_declaring} declaring, "
        f"{report.archived_off_grammar} of them outside the grammar.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to scan (default: cwd)")
    parser.add_argument("--register", metavar="PATH", default=None,
                        help="register file (default: the one beside this "
                             "validator)")
    args = parser.parse_args(argv)

    try:
        register = cs.load_register(
            Path(args.register) if args.register else cs.REGISTER_PATH)
        report = cs.scan(Path(args.repo_root), register)
    except cs.CodeSurfaceError as exc:
        print("code_surface validation CANNOT RUN:")
        print(f"  - {exc}")
        return 2

    _report(report)

    if report.stale:
        print("code_surface register entries matched NOTHING (stale):")
        for entry in report.stale:
            print(f"  - {entry}")
        print("  delete the entry: the exception outlived its condition.")

    if report.findings:
        print("code_surface validation FAILED:")
        for finding in report.findings:
            print(f"  - {finding.path}: {finding.detail}")
        return 1

    if report.stale:
        return 2

    print("code_surface validation passed "
          "(every active declaration's head is admitted).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
