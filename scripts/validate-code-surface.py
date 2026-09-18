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
DECLARED HEAD is judged and the prose GLOSS never is.

AND SINCE `add-estate-repository-inventory`, MEMBERSHIP IS JUDGED TOO, IN THIS
SAME RUN. The bound this docstring used to state — "no repository name's
MEMBERSHIP of anything is checked, this repository defines no inventory of the
estate's repositories to resolve against" — was lifted by the act that removed
its reason and by nothing else: `scripts/estate-repository-inventory.yaml` is
that inventory. The MEMBERSHIP ARM below resolves every identifier in every
readable active head against it, and the two scans report in ONE run rather than
in two a caller may run singly, which is why this is an arm here and not a
second validator.

THE ARM FAILS CLOSED and takes NO EXCEPTION FOR THE FORWARD-LOOKING WINDOW. An
identifier the inventory does not carry is REFUSED and is never admitted on the
strength of its shape, because the whole content of this arm is the difference
between a name that resolves and a name that merely looks like one. A code
surface is FORWARD-LOOKING — it names where a change WILL write — so a
repository the estate is CREATING is declared before any gitlink, pin or
workflow can name it; that window is answered by the PROVISIONAL row the
enumeration requirement OWES (`admitted_by: change`, MUST and not MAY, ruled by
Brett Heap 2026-09-18 verbatim "MAY becomes MUST"), and never by an arm that
declines to judge.

FOUR THINGS THE ARM REPORTS RATHER THAN REFUSES, each for its own stated reason.
A head at a FORMER address (the transfer map resolves it, so the identifier is
INTERPRETABLE and membership is not in doubt; what is owed is a respelling, and
refusing "would red a required check on a packet whose declaration everybody can
read" — `design.md` D5). A ROW WHOSE IN-TREE EVIDENCE HAS GONE (the row outlived
the admission it records; the remedy is to retire it in the pull request that
made it stale, and the asymmetry is the closed register's own — an identifier
the inventory does not carry FAILS, a row nothing names REPORTS). A `gitlink`
ROW (its evidence lives in a tree this checkout does not contain, so it is NOT
RE-CHECKED — counted, neither passed nor failed — rather than named or stale).
And the ARCHIVE, read and judged never, on the same terms the grammar arm reads
it: an archived packet's front matter is frozen record, and a gate demanding an
edit nobody may make is a standing finding with no remedy.

THE ARM TAKES NO TREE ARGUMENT AND MAKES NO NETWORK CALL, so the required
check's verdict is the same on every machine. Re-checking a `gitlink` against a
supplied working tree is `scripts/validate-estate-inventory.py --estate-tree`'s
separately invoked mode and is deliberately not reachable from here: a required
check whose answer depended on which trees a runner happened to have checked out
would give a different answer on a different machine.

THE INVENTORY IS THE SCANNED TREE'S OR IT IS NOTHING, which is this
repository's own ratified rule for the file beside it restated for this one
rather than re-derived. `tests/code_surface/test_code_surface_gate.py`'s
`test_a_scanned_tree_with_NO_register_is_NOT_judged_against_the_HOUSE_one` names
the defect it closes: "A tree was then judged against exceptions it does not
carry, silently, in a message that named an entry and told its author to delete
it from a file they do not have." An inventory falls to the same failure wearing
a worse face — a tree that is no part of this estate would be told its
declaration names a repository "the estate inventory does not carry", of an
estate it is not in, and the arm FAILS CLOSED, so the fallback would refuse every
declaration in every tree but this one. The resolution order is the path
`--inventory` NAMES, else the path THE SCANNED TREE carries, else membership is
NOT JUDGED and the run SAYS SO. A present inventory that cannot be used REFUSES
and does not fall back to the one beside this validator.

A REGISTERED DECLARATION IS NOT JUDGED AND THE ARM DOES NOT FALL BACK. The
closed register suspends the grammar's refusal for ONE declaration and supplies
NO repository set — the head it tolerates is a head no reader can parse — so
there is nothing to resolve, and an arm that fell back to the whole declaration,
to the gloss, or to an empty set would authorize on text no reader can parse.

Usage:
    validate-code-surface.py [REPO_ROOT]

    REPO_ROOT defaults to the current directory.

    exit 0  every active declaration's head is one the grammar admits, or is
            named by a live register entry; no register entry is stale; and
            every identifier a readable head names resolves to an inventory row
            the estate may change.
    exit 1  at least one active declaration's head cannot be read and is not
            named by the register (the remedy belongs to the declaring packet,
            which re-punctuates its own declaration so the head ends where the
            explanation begins), OR at least one readable head names a
            repository identifier the ESTATE INVENTORY does not carry, or one
            that resolves to an `external` row. The membership arm FAILS
            CLOSED: an identifier the inventory does not carry is never
            admitted on the strength of its shape, and a change cannot change a
            repository this estate does not author.
    exit 2  the register cannot be used, or an entry in it matched nothing on a
            whole-corpus scan; or the ESTATE INVENTORY cannot be used, or one
            of its rows' in-tree admission evidence no longer appears in this
            working tree. A stale ROW is the same shape of statement a stale
            ENTRY is — the record outlived the act it records — and takes the
            same disposition, which is the asymmetry the requirement names as
            the register's own: an identifier the inventory does not carry
            FAILS, a row nothing names REPORTS. A stale entry is a statement about the REGISTER
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

    A FORMER-ADDRESS HEAD AND AN UNRE-CHECKED `gitlink` ROW CHANGE NO EXIT
    CODE, and both are printed. The first is REPORTED because the transfer map
    resolves it, so the identifier is interpretable and what is owed is a
    respelling — refusing it was retained and declined at `design.md` D5, on
    the cost that it "would red a required check on a packet whose declaration
    everybody can read". The second is reported because its evidence lives in a
    tree this checkout does not contain: a run that has not looked may report
    neither "named" nor "stale", so it reports the count and nothing else.

    --register PATH
        Read the register from PATH instead of from
        `scripts/code-surface-register.yaml`. The pytest gate runs this
        validator with NO such flag, so the gate is always judged against the
        register this repository carries; the flag exists so the tests can put
        a known register in front of a known tree, and so a consuming tree that
        carries its own register can name it. A missing register REFUSES
        (exit 2) rather than defaulting to an empty one: an exception file that
        silently becomes empty would re-fail every declaration it covers.

    --inventory PATH
        Read the estate inventory from PATH instead of from the scanned tree's
        own `scripts/estate-repository-inventory.yaml`. The pytest gate runs
        this validator with NO such flag over THIS repository, so the gate is
        always judged against the inventory this repository carries; the flag
        exists so the tests can put a known inventory in front of a known tree,
        and so a consuming tree can name one that is not at the house path. A
        NAMED inventory that is missing REFUSES (exit 2) rather than falling
        through to "not judged": the operator asked for that file, and an
        inventory that silently became empty would, with an arm that fails
        closed, refuse every declaration in the corpus.

        With no flag, a scanned tree that carries NO inventory is NOT judged
        against the one beside this validator — membership is not judged for it
        and the run says so.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import code_surface as cs  # noqa: E402
import estate_inventory as ei  # noqa: E402


# --- the membership arm -------------------------------------------------------
#
# ONE RUN, TWO SCANS, and the packet says why it is one and not two: "so the
# grammar scan and the membership scan report in one run rather than in two a
# caller may run singly". A membership gate a caller could forget to run is a
# gate that is not run.
#
# IT READS THROUGH THE SHIPPED READER AND WRITES NO SECOND PARSER. Every
# declaration it judges is fetched by `code_surface.declaration` and parsed by
# `code_surface.parse_head`, and the corpus it walks is
# `code_surface._proposals`'s — the same top-level, symlink-guarded walk the
# grammar arm makes, so the two arms cannot disagree about which documents the
# tree carries. `_proposals` is private and is used deliberately: this packet
# edits no byte of `scripts/code_surface.py` (its `proposal.md` says so in its
# own `code_surface:` declaration), so adding a public accessor there is not
# available — and re-walking the tree here would be exactly the second parser
# the house forbids.


@dataclass(frozen=True)
class MembershipFinding:
    """One identifier this arm has something to say about."""
    change: str
    path: str
    identifier: str
    detail: str


@dataclass(frozen=True)
class MembershipReport:
    """The membership scan's result. Counts are facts about the tree."""
    heads: int
    identifiers: int
    carried: int
    registered_unjudged: int
    findings: tuple[MembershipFinding, ...]
    former: tuple[MembershipFinding, ...]
    stale_rows: tuple[str, ...]
    not_rechecked: int
    inventory_rows: int
    archived_unknown: int


def _membership(repo_root: Path, inventory: ei.Inventory,
                register: list[dict]) -> MembershipReport:
    """Resolve every identifier every readable ACTIVE head names.

    FOUR POPULATIONS ARE SKIPPED AND EACH FOR ITS OWN RATIFIED REASON, none of
    them a fallback. A proposal that could not be READ at all yields no
    declaration, so there is nothing to resolve and the grammar arm already
    reports the document (this arm adding a second finding for one defect would
    be the two-faces-of-one-event confusion the cross-reference below exists to
    undo). A proposal that declares NOTHING has taken the promoted doc-only
    default. A head that is `none` declares the EMPTY surface, so there is no
    identifier. And a REGISTERED declaration has no readable head at all: the
    register supplies NO repository set, so membership is NOT judged for it and
    the arm does NOT fall back to the whole declaration, to the gloss, or to an
    empty set — an arm that invented one would authorize on text no reader can
    parse.
    """
    transfers = ei.load_transfers(repo_root)
    covered = {(entry["change"], entry["declaration"]) for entry in register}

    findings: list[MembershipFinding] = []
    former: list[MembershipFinding] = []
    resolutions: dict[str, ei.Resolution] = {}
    heads = 0
    registered_unjudged = 0

    for proposal in cs._proposals(repo_root, archived=False):
        change = proposal.parent.name
        rel = str(proposal.relative_to(repo_root))
        try:
            present, text = cs.declaration(proposal)
        except cs.CodeSurfaceError:
            continue  # unreadable: the grammar arm owns this document
        if not present or text is None:
            continue  # the promoted default; declaring nothing declares it
        try:
            head = cs.parse_head(text)
        except cs.CodeSurfaceError:
            if (change, text) in covered:
                registered_unjudged += 1
            continue  # no readable head, and NO FALLBACK
        if head.is_none:
            continue  # the empty surface declares no identifier
        heads += 1
        for identifier in head.repositories:
            resolution = ei.resolve(inventory, identifier, transfers)
            resolutions.setdefault(identifier, resolution)
            if not resolution.resolved:
                findings.append(MembershipFinding(
                    change, rel, identifier,
                    f"declares the repository identifier `{identifier}`, which "
                    f"the estate inventory `{inventory.path.name}` "
                    f"({len(inventory.rows)} rows) does not carry. THE ARM "
                    "FAILS CLOSED: an identifier is never admitted on the "
                    "strength of its shape, and it is not resolved by asking "
                    "the provider. Either the identifier is misspelled, or the "
                    "repository has been named by a governed tree and the "
                    "inventory owes the row that records it"))
                continue
            row = resolution.row
            assert row is not None
            if row.governance == "external":
                findings.append(MembershipFinding(
                    change, rel, identifier,
                    f"declares `{identifier}`, which resolves to inventory row "
                    f"{row.position} (`{row.repository}`) whose governance "
                    "class is EXTERNAL — pinned by this estate and authored "
                    "outside it. A code surface is the set of repositories "
                    "whose runtime artifacts a change CHANGES, and a change "
                    "cannot change a repository this estate does not author. "
                    "The refusal names the class so this is distinguishable "
                    "from an unknown identifier"))
                continue
            if resolution.how == ei.BY_FORMER:
                former.append(MembershipFinding(
                    change, rel, identifier,
                    f"names `{identifier}`, which "
                    f"`{ei.TRANSFER_MAP}` records as a FORMER address of "
                    f"`{resolution.current}` (inventory row {row.position}). "
                    "The identifier is INTERPRETABLE, so membership is not in "
                    "doubt and this is not a refusal; what is owed is the "
                    f"respelling to `{resolution.current}`"))

    verdicts = ei.evidence_verdicts(inventory, repo_root)
    stale_rows = tuple(
        f"row {v.row.position} ({v.row.repository}), {v.admission.site()}: "
        f"{v.detail}"
        for v in verdicts if v.verdict == ei.GONE)
    not_rechecked = len({v.row.repository for v in verdicts
                         if v.verdict == ei.NOT_RECHECKED})

    # THE ARCHIVE IS READ AND JUDGED NEVER, on the grammar arm's own terms: an
    # archived packet's front matter is frozen record, so the run COUNTS what
    # the archive carries and refuses nothing there.
    archived_unknown = 0
    for proposal in cs._proposals(repo_root, archived=True):
        try:
            present, text = cs.declaration(proposal)
        except cs.CodeSurfaceError:
            continue
        if not present or text is None:
            continue
        try:
            head = cs.parse_head(text)
        except cs.CodeSurfaceError:
            continue
        if head.is_none:
            continue
        if any(not ei.resolve(inventory, name, transfers).resolved
               for name in head.repositories):
            archived_unknown += 1

    return MembershipReport(
        heads=heads,
        identifiers=len(resolutions),
        carried=sum(1 for r in resolutions.values() if r.resolved),
        registered_unjudged=registered_unjudged,
        findings=tuple(findings),
        former=tuple(former),
        stale_rows=stale_rows,
        not_rechecked=not_rechecked,
        inventory_rows=len(inventory.rows),
        archived_unknown=archived_unknown,
    )


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


def _report_membership(membership: MembershipReport) -> None:
    """THE MEMBERSHIP COUNTS, BESIDE THE GRAMMAR COUNTS, IN ONE RUN."""
    print(
        f"membership: {membership.heads} readable heads naming "
        f"{membership.identifiers} distinct identifiers — "
        f"{membership.carried} carried by the estate inventory "
        f"({membership.inventory_rows} rows), "
        f"{len(membership.findings)} refused, "
        f"{len(membership.former)} at a former address (reported), "
        f"{membership.registered_unjudged} registered and not judged.")
    print(
        f"  inventory rows: {len(membership.stale_rows)} whose in-tree "
        f"evidence this tree no longer carries, {membership.not_rechecked} "
        f"NOT RE-CHECKED (a gitlink, whose evidence lives in a tree this "
        f"checkout does not contain).")
    print(
        f"  archive (read, never judged): {membership.archived_unknown} "
        f"records name a repository the inventory does not carry.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to scan (default: cwd)")
    parser.add_argument("--register", metavar="PATH", default=None,
                        help="register file (default: the one beside this "
                             "validator)")
    parser.add_argument("--inventory", metavar="PATH", default=None,
                        help="estate inventory file (default: the one beside "
                             "this validator)")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    try:
        register = cs.load_register(
            Path(args.register) if args.register else cs.REGISTER_PATH)
        report = cs.scan(repo_root, register)
    except cs.CodeSurfaceError as exc:
        print("code_surface validation CANNOT RUN:")
        print(f"  - {exc}")
        return 2

    # THE INVENTORY IS THE SCANNED TREE'S OR IT IS NOTHING, which is this
    # repository's OWN ratified rule for the file beside it — the closed
    # register — restated for the inventory rather than re-derived. The comment
    # that rule was written under says the defect exactly: "A tree was then
    # judged against exceptions it does not carry, silently, in a message that
    # named an entry and told its author to delete it from a file they do not
    # have." An inventory falls to the same failure wearing a worse face: a tree
    # that is no part of this estate would be told its declaration names a
    # repository "the estate inventory does not carry", of an estate it is not
    # in, and the arm FAILS CLOSED — so the fallback would refuse every
    # declaration in every tree that is not this one.
    #
    # So the resolution order is: the path `--inventory` NAMES; else the path
    # THE SCANNED TREE carries; else membership is NOT JUDGED and the run SAYS
    # SO. The absence is reported and never silent, because a membership gate
    # that quietly judged nothing is the gate not running.
    inventory: ei.Inventory | None = None
    if args.inventory:
        named = Path(args.inventory)
    else:
        # PRESENCE IN EVERY SHAPE, AND THE ANCESTRY AS WELL AS THE LEAF. A
        # dangling symlink and a symlinked `scripts/` are both PRESENT for this
        # question, and both are REFUSED by `load_inventory` rather than read —
        # which is the point of asking presence here and shape there.
        candidate = repo_root / "scripts" / ei.INVENTORY_PATH.name
        named = candidate if (candidate.is_symlink() or candidate.exists()) \
            else None
    if named is not None:
        # AN INVENTORY THAT IS PRESENT AND CANNOT BE USED REFUSES RATHER THAN
        # FALLING BACK, on `load_inventory`'s own rule and on the sibling's:
        # ignored, every declared identifier would resolve against nothing and
        # the fail-closed arm would refuse the whole corpus, reporting a
        # whole-corpus failure where the defect is one unreadable file. The
        # grammar report is printed FIRST so a run that cannot judge membership
        # still says what it did judge.
        try:
            inventory = ei.load_inventory(named)
        except ei.EstateInventoryError as exc:
            _report(report)
            print("membership validation CANNOT RUN:")
            print(f"  - {exc}")
            print("  the inventory is the SCANNED TREE'S or the one "
                  "`--inventory` names, and a present one that cannot be used "
                  "does NOT fall back to the inventory beside this validator.")
            return 2

    membership = (_membership(repo_root, inventory, register)
                  if inventory is not None else None)

    _report(report)
    if membership is not None:
        _report_membership(membership)
    else:
        print(f"membership: NOT JUDGED — the scanned tree carries no "
              f"`scripts/{ei.INVENTORY_PATH.name}`, so there is no estate "
              f"inventory for it to be resolved against. The inventory is the "
              f"SCANNED TREE'S or it is nothing: a tree judged against an "
              f"enumeration it does not carry would be refused for not "
              f"belonging to an estate it is no part of.")

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

    # THE FOUR MEMBERSHIP BLOCKS, ORDERED SO THE ACTIONABLE ONE IS FIRST.
    if membership is None:
        membership = MembershipReport(
            heads=0, identifiers=0, carried=0, registered_unjudged=0,
            findings=(), former=(), stale_rows=(), not_rechecked=0,
            inventory_rows=0, archived_unknown=0)

    if membership.former:
        print("membership: a declared head names a FORMER address "
              "(reported, NOT refused):")
        for finding in membership.former:
            print(f"  - {finding.path}: {finding.detail}")

    if membership.not_rechecked:
        print(f"membership: {membership.not_rechecked} inventory rows are NOT "
              f"RE-CHECKED by this arm — each is admitted by a `gitlink` whose "
              f"evidence lives in a tree this checkout does not contain. They "
              f"are counted, neither passed nor failed. "
              f"`scripts/validate-estate-inventory.py --estate-tree "
              f"<repo>=<path>` re-checks them against a working tree that "
              f"VERIFIES as the carrier; this arm takes no tree argument, so "
              f"its verdict is the same on every machine.")

    if membership.stale_rows:
        print("estate inventory rows whose IN-TREE evidence this tree no "
              "longer carries (reported against the ROW, never against a "
              "declaration):")
        for row in membership.stale_rows:
            print(f"  - {row}")
        print("  the row outlived the admission it records; retire it in the "
              "pull request that made it stale. An identifier the inventory "
              "does not carry FAILS; a row nothing names REPORTS.")

    if membership.findings:
        print("membership validation FAILED:")
        for finding in membership.findings:
            print(f"  - {finding.path}: {finding.detail}")

    if report.findings:
        print("code_surface validation FAILED:")
        for finding in report.findings:
            print(f"  - {finding.path}: {finding.detail}")

    if report.findings or membership.findings:
        return 1

    if report.stale or membership.stale_rows:
        return 2

    print("code_surface validation passed "
          "(every active declaration's head is admitted, and every identifier "
          "it names is carried by the estate inventory).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
