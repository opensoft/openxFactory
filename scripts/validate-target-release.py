#!/usr/bin/env python3
"""House validator for the `target_release:` realization-axis declaration
(release-realization / gate-realization-axis-vocabulary).

`openspec validate` is the EXTERNAL OpenSpec CLI and cannot be extended in-tree,
so — exactly as the other `scripts/validate-*.py` contract validators do — this
script is the house realization of the ADDED requirement *Realization axis
vocabulary is gated*, and the pytest gate
(`tests/target_release/test_validate.py::test_corpus_target_release_validates`)
runs it over every active change on every pull request, so a declaration
outside the ratified vocabulary reds the required `pytest-suite` check.

WHAT IT JUDGES, AND WHAT IT DOES NOT. Only ACTIVE proposals
(`openspec/changes/<change>/proposal.md`) are judged. Archived proposals are
frozen record: they are READ and COUNTED so the run can say what the archive
carries, and refused never. A proposal that declares no `target_release:` at
all is taking the promoted doc-only default and passes.

Usage:
    validate-target-release.py [REPO_ROOT]

    REPO_ROOT defaults to the current directory.

    exit 0  every active declaration is inside the vocabulary or is named by a
            live register entry, and no register entry is stale.
    exit 1  at least one active declaration is outside the vocabulary and is
            not named by the register. The remedy belongs to the declaring
            packet: correct the declaration.
    exit 2  the register cannot be used, or an entry in it matched nothing on a
            whole-corpus scan. A stale entry is a statement about the REGISTER
            — the exception outlived the condition it was granted for — and the
            remedy is to delete the entry in the pull request that made it
            stale. The asymmetry is `scripts/validate-openspec-cli-pin.py`'s,
            deliberately: silently tolerating a stale exception is how an
            exception list rots into a blanket, and refusing makes the
            correction (or the archive) the event that forces the
            re-examination.

    Where BOTH occur, the run reports both and exits 1: an off-vocabulary
    declaration is the more actionable defect and the stale block is printed
    beside it, so neither is hidden by the other.

    --register PATH
        Read the register from PATH instead of from
        `scripts/target-release-register.yaml`. The pytest gate runs this
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

import target_release as tr  # noqa: E402


def _report(report: tr.Report) -> None:
    print(
        f"target_release: {report.active_total} active proposals, "
        f"{report.active_declaring} declaring — "
        f"{report.inside_implemented} `implemented`, "
        f"{report.inside_release} a named release, "
        f"{len(report.grandfathered)} named by the register, "
        f"{len(report.findings)} outside the vocabulary.")
    print(
        f"  archive (read, never judged): {report.archived_total} proposals, "
        f"{report.archived_off_vocabulary} of them outside the vocabulary.")
    if not report.registry_present:
        print(f"  note: no {tr.RELEASE_REGISTRY_DIR} in this tree, so a release "
              "name is accepted on its SHAPE alone.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to scan (default: cwd)")
    parser.add_argument("--register", metavar="PATH", default=None,
                        help="register file (default: the one beside this "
                             "validator)")
    args = parser.parse_args(argv)

    try:
        register = tr.load_register(
            Path(args.register) if args.register else tr.REGISTER_PATH)
        report = tr.scan(Path(args.repo_root), register)
    except tr.TargetReleaseError as exc:
        print("target_release validation CANNOT RUN:")
        print(f"  - {exc}")
        return 2

    _report(report)

    if report.stale:
        print("target_release register entries matched NOTHING (stale):")
        for entry in report.stale:
            print(f"  - {entry}")
        print("  delete the entry: the exception outlived its condition.")

    if report.findings:
        print("target_release validation FAILED:")
        for finding in report.findings:
            print(f"  - {finding.path}: `{finding.token}` {finding.detail}")
        return 1

    if report.stale:
        return 2

    print("target_release validation passed "
          "(every active declaration is admitted).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
