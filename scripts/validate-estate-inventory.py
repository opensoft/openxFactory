#!/usr/bin/env python3
"""House validator for the ESTATE REPOSITORY INVENTORY
(release-realization / add-estate-repository-inventory).

`openspec validate` is the EXTERNAL OpenSpec CLI and cannot be extended in-tree,
so — exactly as the other `scripts/validate-*.py` contract validators do, and
exactly as the sibling `scripts/validate-code-surface.py` does for the
declaration it gates — this script is the house realization of the ADDED
requirement *The estate's repositories are enumerated in a governed inventory*,
and the pytest gate
(`tests/estate_inventory/test_estate_inventory.py::test_corpus_estate_inventory_validates`)
runs it over this repository on every pull request, so an inventory whose shape
or whose in-tree evidence has rotted reds the required `pytest-suite` check with
no workflow edit.

WHAT THE DEFAULT RUN JUDGES, AND WHAT IT CANNOT. The default run judges the
file's SHAPE and the admission evidence that lives in THIS repository's working
tree, deterministically and WITH NO NETWORK CALL. FOUR of the five admission
kinds are in reach here — `pin` a file under `contracts/`, `workflow` a file
under `.github/workflows/`, `change` a directory under `openspec/changes/`, and
`root` a constant naming no file at all. `gitlink` is the ONE kind whose
evidence lives in ANOTHER repository's tree, which an openxFactory checkout does
not contain, so the default run REPORTS its `gitlink` rows as NOT RE-CHECKED
WITH THEIR COUNT rather than passing them silently or failing them. A SILENCE IS
NEVER A PASS: a run that has not looked reports neither "named" nor "stale".

`--estate-tree <repo>=<path>` IS THE ONLY WAY A `gitlink` IS RE-CHECKED, and the
input is a path a caller ALREADY HAS. NO MODE FETCHES A TREE. A validator that
fetched would make a required check depend on a token and on read access to a
private repository, which is the cost `design.md` D1 refused the derived shape
for and which may not be readmitted at the reverse arm.

AND THE SUPPLIED TREE IS VERIFIED AS THE CARRIER BEFORE IT IS READ. **Ruled by
Brett Heap, 2026-09-18, verbatim "Bind the carrier identity."** A PATH IS AN
ASSERTION AND NOT AN IDENTITY: a caller may pass a typo'd path, a stale
worktree, or a checkout of a different repository that merely sits where the
carrier was expected, and an unverified path would let ONE repository's
`.gitmodules` discharge — or condemn — ANOTHER repository's row. The
verification reads the tree's OWN ORIGIN URL, or the carrier's record in
`contracts/policies/repository-identity.yaml` so a carrier supplied at a FORMER
address verifies through the map; a tree that FAILS it leaves the row reported
NOT RE-CHECKED and COUNTED, with the rows no tree was supplied for, NEITHER
PASSED NOR FAILED, and the report names the carrier the row expects and what the
tree actually is. Failing the row on a mismatched tree was retained and DECLINED
(`design.md` D1.2): it converts a caller's typo into a finding against the
inventory, and it breaks this arm's own rule that a run which has looked in the
wrong place has not looked.

A PINNED CARRIER IS READ AT THE COMMIT ITS PIN NAMES, AND AT NO OTHER REVISION
(`admit-code-leg-under-pinned-root`, openxFactory #1150). A `gitlink` may be
carried by a `pinned` ASSEMBLY ROOT that openxFactory pins exactly once, and for
such a carrier the supplied tree is verified exactly as above and then read at
the commit the carrier's `pin` in THIS checkout names, out of the tree's own
object store — never its working files, and never another revision, because
openxFactory consumes the root at that commit and at no other. THE READ MAKES NO
NETWORK CALL: every transport is refused, so a partial clone missing the object
cannot fetch it. A pin naming no commit, and a tree that cannot produce that
commit's `.gitmodules` locally, each leave the row NOT RE-CHECKED and COUNTED,
the report naming the pin and the commit. A GOVERNED carrier is read exactly as
before, from its working tree: openxFactory consumes none at a commit.

Usage:
    validate-estate-inventory.py [REPO_ROOT] [--estate-tree REPO=PATH ...]

    REPO_ROOT defaults to the current directory.

    exit 0  the inventory's shape is admitted and every in-tree admission is
            named by this working tree. Rows at a FORMER address and `gitlink`
            rows nothing re-checked are REPORTED here, with their counts, and do
            not change the verdict.
    exit 1  at least one row's admission evidence has GONE — an in-tree `pin`,
            `workflow` or `change` this tree does not carry (or a `pin` whose
            file no longer names the repository), a still-provisional row whose
            change has ARCHIVED, or, where a VERIFIED tree was supplied, a
            `gitlink` that tree's `.gitmodules` does not carry — for a PINNED
            carrier, its `.gitmodules` at the commit the carrier's pin names.
            The remedy is to correct the evidence or to retire the row, never
            to widen what counts as evidence.
    exit 2  the inventory cannot be USED — it is missing, reached through a
            symlink, refused by the strict loader, or malformed; two rows share
            a bare name, which REFUSES THE FILE rather than picking a row,
            because picking is how an authorization lands in the wrong
            repository; or a `--estate-tree` argument is itself unusable.

    The asymmetry is the sibling register's and `validate-code-surface.py`'s,
    deliberately: an inventory that cannot be used stops the run, because a
    membership arm that fails closed would otherwise red every declaration in
    the corpus while reading as a problem nobody named.

    --estate-tree REPO=PATH
        Supply the working tree of a repository that CARRIES a `gitlink`, so
        the rows admitted by a gitlink in REPO are re-checked in PATH. Repeat
        the flag for each carrier. The tree is verified as REPO before it is
        read; one PATH per REPO. Where REPO's row is `pinned`, PATH is read at
        the commit REPO's pin names, from PATH's own object store, and never
        at its working files; its checkout may sit at any revision.

    --inventory PATH
        Read the inventory from PATH instead of from
        `scripts/estate-repository-inventory.yaml`. The pytest gate runs this
        validator with NO such flag, so the gate is always judged against the
        inventory this repository carries; the flag exists so the tests can put
        a known inventory in front of a known tree, and so a consuming tree that
        carries its own can name it.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import estate_inventory as ei  # noqa: E402


def _parse_estate_trees(values: list[str]) -> dict[str, Path]:
    """`{carrier address: working tree}` from the repeated flag, or a refusal.

    ONE PATH PER CARRIER. Two paths for one repository is an ambiguity this arm
    may not resolve by picking, for the same reason two rows sharing a bare name
    refuse the file: whichever it picked, a reader could not tell which tree the
    verdict came from.
    """
    trees: dict[str, Path] = {}
    for value in values:
        repo, separator, path = value.partition("=")
        if not separator or not repo.strip() or not path.strip():
            raise ei.EstateInventoryError(
                f"`--estate-tree {value}` is not `<repo>=<path>`; the carrier "
                "is named so the verdict can say which tree it came from")
        repo = repo.strip()
        if not ei.ADDRESS_RE.match(repo):
            raise ei.EstateInventoryError(
                f"`--estate-tree {value}` names `{repo}`, which is not an "
                "`<owner>/<name>` address; a row names its carrier as an "
                "address, so a tree supplied under any other spelling is a "
                "tree for no row")
        if repo in trees:
            raise ei.EstateInventoryError(
                f"`--estate-tree` names {repo} twice; one working tree per "
                "carrier, so a reader can tell which tree a verdict came from")
        trees[repo] = Path(path.strip())
    return trees


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to judge (default: cwd)")
    parser.add_argument("--inventory", metavar="PATH", default=None,
                        help="inventory file (default: the one beside this "
                             "validator)")
    parser.add_argument("--estate-tree", metavar="REPO=PATH", action="append",
                        default=[],
                        help="a carrier's working tree, so its gitlink rows "
                             "are re-checked; repeatable")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    try:
        trees = _parse_estate_trees(args.estate_tree)
        inventory = ei.load_inventory(
            Path(args.inventory) if args.inventory else ei.INVENTORY_PATH)
    except ei.EstateInventoryError as exc:
        print("estate inventory validation CANNOT RUN:")
        print(f"  - {exc}")
        return 2

    transfers, transfer_findings = ei.load_transfers(repo_root)
    verdicts = ei.evidence_verdicts(inventory, repo_root)

    # --- the supplied trees, VERIFIED BEFORE THEY ARE READ --------------------
    #
    # The verification happens ONCE per carrier and not once per row: a tree is
    # one tree whatever it discharges, and re-reading it per row would let one
    # carrier's identity be answered differently at two rows of the same file.
    #
    # AND READ WHERE THE REQUIREMENT SAYS TO READ IT (`ei.carrier_members`): a
    # governed carrier from its working tree, exactly as before; a PINNED one
    # at the commit its pin names, out of the tree's own object store, never
    # its working files, with every transport refused.
    checks: dict[str, ei.CarrierCheck] = {}
    members: dict[str, ei.CarrierMembers] = {}
    for carrier, path in trees.items():
        check = ei.carrier_identity(path, carrier, transfers)
        checks[carrier] = check
        if check.verified:
            members[carrier] = ei.carrier_members(inventory, carrier, path,
                                                  repo_root)

    gone: list[ei.EvidenceVerdict] = []
    provisional_archived: list[ei.EvidenceVerdict] = []
    not_rechecked: list[tuple[ei.EvidenceVerdict, str]] = []
    named_gitlinks = 0

    for verdict in verdicts:
        if verdict.verdict == ei.NAMED:
            continue
        if verdict.verdict == ei.GONE:
            if (verdict.admission.kind == ei.CHANGE and verdict.row.provisional
                    and "ARCHIVED" in verdict.detail):
                provisional_archived.append(verdict)
            else:
                gone.append(verdict)
            continue
        # A `gitlink`: NOT RE-CHECKED unless a VERIFIED tree was supplied.
        carrier = verdict.admission.carrier
        assert carrier is not None
        check = checks.get(carrier)
        if check is None:
            not_rechecked.append((
                verdict,
                f"no working tree was supplied for the carrier {carrier}"))
            continue
        if not check.verified:
            not_rechecked.append((verdict, check.detail))
            continue
        reading = members[carrier]
        if reading.addresses is None:
            not_rechecked.append((verdict, reading.detail))
            continue
        if verdict.row.repository in reading.addresses:
            named_gitlinks += 1
        else:
            gone.append(ei.EvidenceVerdict(
                verdict.row, verdict.admission, ei.GONE,
                f"the working tree supplied for {carrier} VERIFIED as that "
                f"carrier and {reading.where} does NOT carry "
                f"`{verdict.row.repository}`"))

    former_rows = ei.former_address_rows(inventory, transfers)

    # A SUPPLIED TREE NO ROW NAMES IS REPORTED AND NOT REFUSED. Nothing in the
    # ratified text makes it a finding, and inventing one here would widen the
    # arm past what was ratified — but a caller who misspells the CARRIER gets
    # every row of that carrier reported NOT RE-CHECKED and no hint that the
    # tree they supplied went nowhere, which is the one way this flag can fail
    # silently. So it is named, and the verdict is untouched.
    carriers = {v.admission.carrier for v in verdicts
                if v.admission.kind == ei.GITLINK}
    unmatched = sorted(set(trees) - carriers)

    # --- the report ----------------------------------------------------------
    gitlink_rows = {v.row.repository for v in verdicts
                    if v.admission.kind == ei.GITLINK}
    print(
        f"estate inventory: {len(inventory.rows)} repositories — "
        f"{sum(1 for r in inventory.rows if r.governance == 'governed')} "
        f"governed, "
        f"{sum(1 for r in inventory.rows if r.governance == 'pinned')} pinned, "
        f"{sum(1 for r in inventory.rows if r.governance == 'external')} "
        f"external; "
        f"{sum(1 for r in inventory.rows if r.provisional)} provisional.")
    # EACH COUNT SAYS WHAT IT MEASURED. The in-tree tally and the gitlink tally
    # are kept apart because they answer different questions and are reached by
    # different evidence: one is a fact about this checkout on every run, the
    # other a fact about a tree a caller chose to supply. A single "gone" count
    # spanning both would report a supplied tree's absence as though this
    # repository's own evidence had rotted.
    in_tree_gone = [v for v in gone if v.admission.kind != ei.GITLINK]
    gitlink_gone = [v for v in gone if v.admission.kind == ei.GITLINK]
    print(
        f"  in-tree evidence ({', '.join(ei.IN_TREE_KINDS)}), re-checked on "
        f"EVERY run: "
        f"{sum(1 for v in verdicts if v.verdict == ei.NAMED)} named, "
        f"{len(in_tree_gone) + len(provisional_archived)} gone.")
    print(
        f"  gitlink rows: {len(gitlink_rows)} — {named_gitlinks} named in a "
        f"VERIFIED supplied tree, {len(gitlink_gone)} absent from one, "
        f"{len(not_rechecked)} NOT RE-CHECKED (no tree supplied, a tree "
        f"that does not verify as the carrier the row names, or, for a pinned "
        f"carrier, a pin naming no commit or a tree that cannot produce that "
        f"commit's `.gitmodules` locally).")

    # WHERE EACH PINNED CARRIER WAS READ, NAMED AND NOT LEFT TO BE INFERRED: the
    # commit is what the verdict rests on, so a reader of the report must be
    # able to see which revision was read, and that it was not the working tree.
    pinned_reads = [members[carrier] for carrier in sorted(members)
                    if carrier in carriers and members[carrier].pin is not None]
    if pinned_reads:
        print("estate inventory: PINNED carriers, each read at the commit its "
              "pin names and never at its working files:")
        for reading in pinned_reads:
            if reading.commit is None:
                print(f"  - {reading.carrier}: `{reading.pin}` names no commit "
                      "to read at; its rows are NOT RE-CHECKED.")
            elif reading.addresses is None:
                print(f"  - {reading.carrier}: `{reading.pin}` names "
                      f"{reading.commit}, and the supplied tree could not "
                      "produce its `.gitmodules` there; its rows are NOT "
                      "RE-CHECKED, each naming why.")
            else:
                carried = ", ".join(reading.addresses) or "no submodule at all"
                print(f"  - {reading.carrier}: `{reading.pin}` names "
                      f"{reading.commit}; its `.gitmodules` there names "
                      f"{carried}.")

    if not_rechecked:
        print("estate inventory rows NOT RE-CHECKED "
              "(counted, neither passed nor failed):")
        for verdict, why in not_rechecked:
            print(f"  - {verdict.row.repository} "
                  f"(gitlink in {verdict.admission.carrier}): {why}")
        print("  a run that has not looked, or has looked in the wrong tree, "
              "reports neither verdict — a path is an assertion and not an "
              "identity.")

    if unmatched:
        print("estate inventory: a supplied working tree carries no row's "
              "gitlink (reported, not refused):")
        for carrier in unmatched:
            print(f"  - `--estate-tree {carrier}={trees[carrier]}`: no row "
                  f"names {carrier} as the carrier of a gitlink, so this tree "
                  "re-checked nothing. Check the carrier's spelling.")

    if former_rows:
        print("estate inventory rows written at a FORMER address "
              "(reported, not refused):")
        for row, current in former_rows:
            print(f"  - row {row.position}: `{row.repository}` is a FORMER "
                  f"address; `{ei.TRANSFER_MAP}` resolves it to `{current}`. "
                  "The inventory carries CURRENT addresses only, and the "
                  "remedy is the respelling.")

    if provisional_archived:
        print("estate inventory PROVISIONAL rows whose change has ARCHIVED:")
        for verdict in provisional_archived:
            print(f"  - row {verdict.row.position} "
                  f"({verdict.row.repository}): {verdict.detail}")

    if gone:
        print("estate inventory validation FAILED — admission evidence GONE:")
        for verdict in gone:
            print(f"  - row {verdict.row.position} "
                  f"({verdict.row.repository}), {verdict.admission.site()}: "
                  f"{verdict.detail}")
        print("  the remedy is to correct the evidence or to remove the row, "
              "never to widen what counts as evidence.")

    if transfer_findings:
        print("estate inventory validation FAILED — the transfer map carries "
              "a MALFORMED row:")
        for finding in transfer_findings:
            print(f"  - {finding}")

    if gone or provisional_archived or transfer_findings:
        return 1

    print("estate inventory validation passed "
          "(every in-tree admission is named by this working tree).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
