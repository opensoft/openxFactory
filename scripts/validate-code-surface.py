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
    beside it, so neither is hidden by the other. AND WHERE BOTH NAME THE SAME
    CHANGE, the run says so in one line ABOVE the two blocks: that is not two
    faults but one — a declaration edited without being brought into the
    grammar — and the remedy is to conform the declaration (which retires the
    entry in the same act) or to re-register the new text (an entry AND its
    baseline pair, in one diff), never to delete the stale entry alone.

    THAT LINK IS DRAWN ONLY FOR AN OFF-GRAMMAR FINDING. A finding also stands
    for a proposal that could not be READ at all (a strict-loader refusal,
    bytes that are not UTF-8, an I/O failure), and a stale entry beside one of
    those is a THIRD case with its own line: the entry shows as stale only
    because the declaration it was granted for could not be fetched to compare
    against, so whether the declaration changed is UNKNOWN rather than
    answered. Neither half of the remedy above applies — there is nothing to
    conform and nothing readable to re-register — and deleting the entry would
    retire an exception on evidence nobody has. The document is made readable
    first, and the entry's status becomes decidable only then.

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

    # ONE EVENT IS REPORTED AS ONE EVENT. The two sections below are the two
    # ASYMMETRIC refusals, and keeping them asymmetric is the requirement's own
    # instruction — but a change that appears in BOTH is not two faults. It is
    # one: its declaration was EDITED, so the entry recording the old text
    # matches nothing (stale), and the new text is off-grammar too (a finding).
    # Printed as two unrelated blocks, the obvious reading is "delete the stale
    # entry", which leaves the finding standing — and the other obvious reading,
    # appending the new text to the register, is the closed-register violation
    # the baseline refuses. So the link is drawn explicitly, BEFORE either
    # block, and it names both halves of the remedy and the one that is not.
    #
    # KEYED ON THE FINDING'S CLASS AS WELL AS ITS CHANGE, because `findings`
    # carries TWO classes and only one of them is this event. An UNREADABLE
    # proposal (a strict-loader refusal, bytes that are not UTF-8, an I/O
    # failure) yields a finding too, and keyed on the change id alone a stale
    # entry beside one was reported as "the declaration was edited without
    # being brought into the grammar" — advising an author to conform or
    # RE-REGISTER TEXT NOBODY CAN READ. Worse, the claim is not merely unhelpful
    # but unfounded: nothing was read, so whether the declaration changed at all
    # is UNKNOWN. That case gets its own line, below, saying exactly that.
    off_grammar = {f.change for f in report.findings
                   if f.kind == cs.OFF_GRAMMAR}
    unreadable = {f.change for f in report.findings if f.kind == cs.UNREADABLE}
    stale_changes = set(report.stale_changes)

    same_event = sorted(stale_changes & off_grammar)
    if same_event:
        print("code_surface: the two reports below name the SAME CHANGE — one "
              "event, not two:")
        for change in same_event:
            print(f"  - {change}: the register entry is stale AND the live "
                  f"declaration is off-grammar — the declaration was edited "
                  f"without being brought into the grammar. CONFORM THE "
                  f"DECLARATION (which retires the entry in the same act) or "
                  f"RE-REGISTER the new text (an entry AND its baseline pair, "
                  f"in one reviewable diff). Do NOT just delete the entry: "
                  f"that leaves the finding standing.")

    # THE UNREADABLE CASE IS A DIFFERENT EVENT AND SAYS SO. The entry shows as
    # stale ONLY because the text it was granted for could not be fetched to
    # compare against; that is not evidence the declaration was edited, and the
    # remedy is neither half of the one above. Ordered AFTER the same-event
    # block so a run reporting both keeps the actionable edit first.
    unreadable_stale = sorted(stale_changes & unreadable)
    if unreadable_stale:
        print("code_surface: a register entry below names a change whose "
              "proposal CANNOT BE READ — a THIRD case, and not the one above:")
        for change in unreadable_stale:
            print(f"  - {change}: the entry shows as stale ONLY because the "
                  f"declaration it was granted for could not be fetched to "
                  f"compare against — the document does not read at all. "
                  f"WHETHER THE DECLARATION CHANGED IS UNKNOWN, not answered, "
                  f"so this is NOT the edited-declaration event: do not "
                  f"conform, and do not RE-REGISTER text no reader can read. "
                  f"MAKE THE DOCUMENT READABLE FIRST — the finding below names "
                  f"the defect — and the entry's status is decidable only "
                  f"then. Deleting the entry now would retire an exception on "
                  f"evidence nobody has.")

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
