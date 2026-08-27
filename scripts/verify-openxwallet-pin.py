#!/usr/bin/env python3
"""Verify openxFactory's CONSUMPTION of opensoft/openXwallet against its pin.

openxFactory no longer OWNS the openxWallet contract family; it CONSUMES it at a
commit and a set of digests. `contracts/openxwallet-pin.yaml` is the whole of
that claim and this file is the running code that checks it. Everything the pin
asserts is checked here, and nothing that is not asserted is inferred.

THE TRUSTED REFERENT IS `commit` PLUS THE EIGHT `sha256`s. `contract_bundle_tag`
is a LABEL printed beside the commit, never the referent: a tag moves, and a
movable name is not a compatibility pin. A pin that declares `revision_kind`
anything other than `commit`, or a `commit` that is not exactly 40 hex, is
refused `pin-tag-only` rather than being resolved — resolving a tag is exactly
the network read this tool exists to not perform.

OFFLINE LAW. This tool reads the pin file, the gitlink, and the files the pin
names. It never reads the network, never reads an upstream tree, and never reads
openXwallet's own `contracts/manifest.yaml`. The live cross-check against the
publisher's manifest is a SYNC-TIME obligation
(`openXwallet/docs/pin-resync-runbook.md`), never a CI read. A gate that reaches
the network to decide whether it passes is a gate whose answer depends on the
network.

TWO GITLINK COMPARISONS, NOT ONE. Check 2 compares the RECORDED gitlink (what
the tree says the submodule should be) and check 3 compares the CHECKED-OUT
revision (what the submodule actually is). Neither subsumes the other: a stale
`git submodule update` leaves the recorded gitlink correct and the checkout
wrong, while a bumped-and-committed gitlink with no checkout, or a deliberately
detached checkout at some other revision, inverts that. One comparison would
pass in exactly the half of the world it is blind to. See `_recorded_gitlink`
for the HEAD-then-index resolution and why the fallback exists.

WHY THE SIX CODES ARE A FIXED VOCABULARY. `REFUSAL_CODES` is the ratified list
(FR-003) and other code — the consumer gate workflow, `validate-trust-anchor.py`
— refuses BY CODE. A refusal that reports the right fact under a new name is a
refusal nothing downstream recognizes, so no failure path here may invent a
code. Every refusal also carries the one fixed `REMEDIATION` trailer (FR-004),
because a refusal that names what is wrong without naming what to run puts the
exit in tribal memory instead of in the message.

WHAT THIS TOOL IS NOT. It is not a schema validator for the wallet family: that
is the PINNED `openXwallet/scripts/validate-openxwallet.py`, at the digest the
pin records, and the consumer gate runs it AFTER this tool. Re-implementing any
of it here was REJECTED — a second copy of a conformance rule is a second answer
to the same question, and the shed exists precisely to stop openxFactory
carrying wallet rules of its own.

USED AS A LIBRARY. `scripts/validate-trust-anchor.py` loads this module with
`importlib.util.spec_from_file_location` and calls `verify(...)`, catching
`PinRefusal`. So `verify()` and `verify_aggregation()` neither print nor exit:
they raise, and the caller decides. All printing and all exiting lives in
`main()`. There is no import-time I/O beyond the path constants below.

Exit codes:
  0  the pin is satisfied: gitlink and checkout both equal `commit`, all eight
     digests recompute, and every path-only member is present
  2  ANY refusal, and any environment failure

  There is deliberately NO exit 1. The sibling tool
  (`openXwallet/scripts/verify-contract-pin.py`) splits drift (1) from
  environment (2), and that split was REJECTED here: the consumer gate's only
  question is "may this pull request proceed", the answer to which is identical
  for "the pin is stale" and "the submodule was never initialized", and a
  two-valued failure invites a workflow that treats one of them as a warning.
  An unanswerable question is never an implicit pass.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "contracts" / "openxwallet-pin.yaml"

# The ONE fixed remediation trailer for every fail-closed refusal in this wave
# (FR-004). `--recursive` is deliberately absent and the parenthetical says so
# out loud: this wave's init is scoped to the one submodule the gate needs, and
# a remediation that recursed would pull the aggregation's whole submodule tree
# into a job that has business with exactly one of them.
REMEDIATION = (
    "Remediation: run `git submodule update --init openXwallet` (NOT "
    "--recursive; this wave's init is deliberately scoped). If the pin itself "
    "is stale, follow `openXwallet/docs/pin-resync-runbook.md`."
)

# The six ratified refusal codes, in the ratified order (spec FR-003).
#
# `pin-unreadable` is NOT here, and its absence is the point. The six describe a
# TREE that disagrees with a well-formed pin — each one is a governed finding a
# reviewer can act on. `pin-unreadable` describes an ENVIRONMENT in which no
# finding can be reached at all: the pin file is absent, does not parse, is not
# a mapping, or PyYAML is missing. Admitting it to this tuple would let a
# consumer that enumerates the vocabulary treat "we could not ask the question"
# as one of the answers. It still exits 2 like everything else — it is excluded
# from the vocabulary, not from fail-closure.
REFUSAL_CODES: tuple[str, ...] = (
    "pin-submodule-uninitialized",
    "pin-gitlink-mismatch",
    "pin-checkout-mismatch",
    "pin-digest-mismatch",
    "pin-member-missing",
    "pin-tag-only",
)

# Exactly 40 / 64 hex, case-insensitive, normalized to lowercase before any
# comparison. The shape stays strict — 40 means 40, so an abbreviated oid or a
# branch name cannot pass — but case is normalized rather than rejected: git
# emits lowercase, so an uppercase value in the pin is a hand-edit rather than a
# movable reference, and refusing it as `pin-tag-only` would name the wrong
# defect.
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")

# The gitlink mode. A submodule entry is mode 160000 in both `ls-tree` and
# `ls-files -s` output; matching on the MODE rather than on the path column is
# what makes a same-named regular file or symlink at that path fail to satisfy
# the check instead of accidentally satisfying it.
GITLINK_MODE = "160000"

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required to read contracts/openxwallet-pin.yaml",
          file=sys.stderr)
    sys.exit(2)


class PinRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail` so a
    caller can branch on the code without parsing prose, while `str(exc)`
    renders the whole thing — code, detail and the fixed remediation trailer —
    as the message a human reads. `main()` prints exactly `str(exc)`; nothing
    re-assembles the message anywhere else, so the trailer cannot be dropped by
    a caller that forgot it exists.
    """

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code, detail)

    def __str__(self) -> str:
        return f"REFUSE {self.code}: {self.detail}\n{REMEDIATION}"


# --------------------------------------------------------------------------
# reading the pin
# --------------------------------------------------------------------------

def load_pin(pin_path: Path = PIN_PATH) -> dict:
    """The pin as a mapping, or `pin-unreadable`.

    Every failure here is an environment failure rather than one of the six:
    without a parseable pin there is no claim to check, and a tool that cannot
    read its own claim must not report the tree as conformant.
    """
    if not pin_path.is_file():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} does not exist; openxFactory consumes "
            "openxWallet only through this pin, so its absence is not an "
            "unpinned pass but an unanswerable question")
    try:
        loaded = yaml.safe_load(pin_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} could not be read as YAML: {exc}") from exc
    if not isinstance(loaded, dict):
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} is not a mapping (parsed as "
            f"{type(loaded).__name__}); `kind: pinned_contract_manifest` is a "
            "mapping shape")
    return loaded


def _submodule_path(pin: dict) -> str:
    """The `submodule_path` the pin governs.

    Read from the pin rather than hard-coded, because `submodule_path` is the
    field FR-002 requires the pin to declare and a verifier that ignored it
    would check a path the pin never claimed. Its absence is `pin-unreadable`
    and not one of the six: a pin with no path cannot be compared against any
    gitlink, so the tree is not what is wrong.
    """
    raw = pin.get("submodule_path")
    if not isinstance(raw, str) or not raw.strip():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares no usable `submodule_path` (got {raw!r}); a pin "
            "with no path cannot be checked against a gitlink")
    return raw.strip()


def _pinned_commit(pin: dict) -> str:
    """The 40-hex referent, lowercased, or `pin-tag-only`.

    ORDER NOTE, and it is a deliberate departure worth naming. The ratified list
    (FR-003) puts `pin-tag-only` SIXTH. This shape validation nonetheless runs
    FIRST, as an early guard, because the ratified checks in second and third
    place — the recorded gitlink and the checked-out revision — both COMPARE
    AGAINST this value. Leaving its validation in sixth place would let a
    malformed pin (`revision_kind: tag`, an abbreviated oid, a branch name) be
    reported as `pin-gitlink-mismatch`: a code that says the TREE is wrong about
    a pin that is itself the thing that is wrong, and a code that sends a
    reviewer to `git submodule update` instead of to the pin. The refusal CODE
    is unchanged and its place in `REFUSAL_CODES` is unchanged; only the moment
    of evaluation moves, and it moves earlier, which can only ever turn a
    misnamed refusal into a correctly named one.
    """
    revision_kind = pin.get("revision_kind")
    if revision_kind != "commit":
        raise PinRefusal(
            "pin-tag-only",
            f"the pin declares revision_kind {revision_kind!r}, not 'commit'; "
            "the trusted referent is a commit plus digests, and resolving a "
            "movable name would require exactly the network read this verifier "
            "refuses to perform")
    commit = pin.get("commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit.strip()):
        raise PinRefusal(
            "pin-tag-only",
            f"the pin records commit {commit!r}, which is not exactly 40 hex "
            "characters; an abbreviated oid, a branch or a tag is not a "
            "compatibility pin")
    return commit.strip().lower()


# --------------------------------------------------------------------------
# reading gitlinks
# --------------------------------------------------------------------------

def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          capture_output=True, text=True, check=False)


def _gitlink_from(output: str, submodule_path: str) -> str | None:
    """The object id of the `160000` entry for `submodule_path`, or None.

    Parses both output shapes this module reads, because they differ only in one
    column and a single parser keeps the two call sites from drifting:

        ls-tree HEAD    160000 commit <oid>\\t<path>
        ls-files -s      160000 <oid> 0\\t<path>

    The MODE is matched, not merely the path: `ls-files -s` will happily report a
    regular file at the same path with mode 100644, and accepting that entry
    would let a directory-turned-file satisfy a gitlink check.
    """
    for line in output.splitlines():
        if not line.strip():
            continue
        head, _, path = line.partition("\t")
        if path.strip().strip('"') != submodule_path:
            continue
        fields = head.split()
        if not fields or fields[0] != GITLINK_MODE:
            continue
        for field in fields[1:]:
            if COMMIT_RE.match(field):
                return field.lower()
    return None


def _recorded_gitlink(repo_root: Path,
                      submodule_path: str) -> tuple[str | None, str]:
    """(oid, source) for the RECORDED gitlink: HEAD first, then the index.

    WHY THE INDEX FALLBACK EXISTS. `git ls-tree HEAD -- <path>` yields NOTHING
    for a gitlink that is staged but not yet committed — the state of a fresh
    `git submodule add`, and therefore the normal state of this very tree for
    the whole time the pin and this verifier are being authored. In CI the
    gitlink is always in HEAD, because CI reads a pushed commit; locally, before
    the wave's first commit, it is only in the index. Refusing on HEAD alone
    would make the tool silently UNRUNNABLE at exactly the moment its author
    most needs to run it, and "unrunnable" is the failure mode that trains
    people to skip a gate. So the index is consulted second, and the source is
    reported in the success note so a reader is never misled about which record
    answered.

    Returning a `source` string rather than printing here keeps `verify()` free
    of output; `main()` re-resolves it for the note.
    """
    head = _git(repo_root, "ls-tree", "HEAD", "--", submodule_path)
    if head.returncode == 0:
        oid = _gitlink_from(head.stdout, submodule_path)
        if oid is not None:
            return oid, "HEAD"
    index = _git(repo_root, "ls-files", "-s", "--", submodule_path)
    if index.returncode == 0:
        oid = _gitlink_from(index.stdout, submodule_path)
        if oid is not None:
            return oid, "the index (staged, not yet committed)"
    return None, "nowhere"


# --------------------------------------------------------------------------
# the six checks
# --------------------------------------------------------------------------

def verify(root: Path = ROOT, pin: dict | None = None) -> dict:
    """Run the six ordered checks against `root`; return the pin on success.

    Raises `PinRefusal` on the FIRST failure and never continues past it. That
    is deliberate, and it is the opposite of the sibling tool's accumulate-then-
    report style: the checks are ORDERED because each later one is only
    meaningful once the earlier ones hold — a digest recomputed against an
    uninitialized submodule reports eight missing files and buries the one fact
    that matters, and a digest recomputed against the WRONG revision reports
    drift when the actual defect is a stale checkout. First failure, named
    correctly, beats eight failures that need triage.

    Prints nothing and exits nothing: `validate-trust-anchor.py` loads this
    module and calls this function.
    """
    pin = load_pin() if pin is None else pin
    submodule_path = _submodule_path(pin)
    # The shape guard, ahead of the checks that compare against it. See
    # `_pinned_commit` for why this precedes check 2 despite being sixth in the
    # ratified order.
    commit = _pinned_commit(pin)
    sub_root = root / submodule_path

    # ---- check 1: the submodule is initialized at all -----------------------
    # `.exists()`, NOT `.is_dir()`. A submodule's `.git` is a FILE holding a
    # `gitdir:` pointer into the superproject's `.git/modules/`, so `.is_dir()`
    # is False for every correctly initialized submodule in a modern checkout
    # and the check would refuse exactly the trees it is meant to accept. It is
    # True for a standalone clone at that path, which is why `.exists()` accepts
    # both and the two later revision comparisons — not this one — are what
    # decide whether the thing at that path is the right thing.
    if not (sub_root / ".git").exists():
        raise PinRefusal(
            "pin-submodule-uninitialized",
            f"{submodule_path}/.git does not exist: the submodule is not "
            f"initialized in {root}, so the openxWallet contracts this "
            "repository consumes are not present to be checked")

    # ---- check 2: the RECORDED gitlink equals `commit` ---------------------
    recorded, source = _recorded_gitlink(root, submodule_path)
    if recorded is None:
        raise PinRefusal(
            "pin-gitlink-mismatch",
            f"{root} records no {GITLINK_MODE} gitlink for {submodule_path} in "
            "HEAD or in the index: the gitlink is recorded NOWHERE, so there is "
            f"nothing to compare against the pinned {commit}. A submodule "
            "present on disk but absent from the tree is not a pinned "
            "consumption")
    if recorded != commit:
        raise PinRefusal(
            "pin-gitlink-mismatch",
            f"the gitlink {root} records for {submodule_path} (read from "
            f"{source}) is {recorded}, but the pin records {commit}; the tree "
            "and the pin disagree about which openxWallet revision this "
            "repository consumes")

    # ---- check 3: the CHECKED-OUT revision equals `commit` -----------------
    # Distinct from check 2, and both are required, because only one comparison
    # catches each case. A checkout can be detached at any revision while the
    # recorded gitlink stays correct (a stale or skipped `git submodule
    # update`), and a gitlink can be bumped and committed while the working
    # checkout stays behind. Whichever half a single check omitted would be the
    # half that passes wrongly, and the digests in check 4 are recomputed
    # against the CHECKOUT — so without this check a digest disagreement would
    # be reported as content drift when the real defect is that the wrong
    # revision is on disk.
    head = _git(sub_root, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise PinRefusal(
            "pin-checkout-mismatch",
            f"`git -C {sub_root} rev-parse HEAD` failed, so the checked-out "
            f"revision cannot be compared against the pinned {commit}: "
            f"{head.stderr.strip() or 'no error output'}")
    checked_out = head.stdout.strip().lower()
    if checked_out != commit:
        raise PinRefusal(
            "pin-checkout-mismatch",
            f"{submodule_path} is checked out at {checked_out}, but the pin "
            f"records {commit}; the recorded gitlink agrees with the pin, so "
            "the tree is right and the working checkout is stale")

    # ---- check 4: every digested member recomputes to its recorded sha256 ---
    entries = pin.get("files")
    if not isinstance(entries, list) or not entries:
        raise PinRefusal(
            "pin-unreadable",
            "the pin lists no `files:` members, so it pins no bytes; an empty "
            "claim is not a satisfied claim")
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise PinRefusal(
                "pin-unreadable",
                f"the pin's files[{index}] is malformed ({entry!r}); every "
                "member must declare a `path`")
        rel = entry["path"]
        target = sub_root / rel
        recorded_digest = entry.get("sha256")
        if not isinstance(recorded_digest, str) or \
                not SHA256_RE.match(recorded_digest.strip()):
            # A recomputed digest can never equal an absent or malformed
            # recorded one, so this is drift and not a shape complaint: the
            # member is unverifiable, which is the same operational fact as a
            # member that verified wrongly.
            raise PinRefusal(
                "pin-digest-mismatch",
                f"{submodule_path}/{rel}: the pin records sha256 "
                f"{recorded_digest!r}, which is not 64 hex characters; a "
                "recomputed digest can never equal a digest that is not one")
        if not target.is_file():
            raise PinRefusal(
                "pin-member-missing",
                f"{submodule_path}/{rel} is MISSING from the checkout, but the "
                f"pin records a sha256 for it; openxWallet@{commit[:12]} is "
                "expected to carry every digested member")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != recorded_digest.strip().lower():
            raise PinRefusal(
                "pin-digest-mismatch",
                f"{submodule_path}/{rel}: DIGEST DRIFT\n"
                f"  recorded   {recorded_digest.strip().lower()}\n"
                f"  recomputed {actual}\n"
                f"the bytes on disk are not the bytes the pin consumes at "
                f"openxWallet@{commit[:12]}")

    # ---- check 5: every path-only member is PRESENT ------------------------
    # Presence only, and that is not a weaker check than it looks. The publisher
    # declares these members "content-addressed by commit; no per-file digest",
    # and inventing digests for them inside a byte-identical move would add rows
    # the publisher never published. Identity comes from checks 2 and 3: both
    # the recorded gitlink and the checked-out revision are already pinned to
    # `commit`, so a swap of any of these files is a swap of the commit and is
    # caught there. What the commit does NOT catch is a member deleted from the
    # WORKING TREE after checkout, which is what this check is for.
    path_only = pin.get("pinned_by_commit_only") or []
    if not isinstance(path_only, list):
        raise PinRefusal(
            "pin-unreadable",
            f"the pin's `pinned_by_commit_only` is not a list "
            f"({path_only!r})")
    for entry in path_only:
        if not isinstance(entry, str) or not entry.strip():
            raise PinRefusal(
                "pin-unreadable",
                f"the pin's `pinned_by_commit_only` holds a non-path entry "
                f"({entry!r})")
        target = sub_root / entry.strip()
        if not target.exists():
            raise PinRefusal(
                "pin-member-missing",
                f"{submodule_path}/{entry.strip()} is MISSING from the "
                f"checkout; the pin declares it content-addressed by "
                f"openxWallet@{commit[:12]}, and a member absent from the "
                "working tree is not content-addressed by anything")

    return pin


def verify_aggregation(aggregation_root: Path, root: Path = ROOT,
                       pin: dict | None = None) -> None:
    """Refuse unless the AGGREGATION's root gitlink equals the pinned commit.

    The xFactory aggregation repo carries its own `openXwallet` gitlink, and the
    invariant it needs is root-gitlink-equals-nested-gitlink: the wallet
    revision the aggregation records must be the wallet revision openxFactory
    consumes. That comparison is made THROUGH `commit` rather than directly
    against the nested gitlink, deliberately — `verify()` has already pinned
    both the nested recorded gitlink and the nested checkout to `commit`, so
    equality with `commit` IS equality with the nested gitlink, and routing it
    through the pin keeps ONE referent in the system instead of two things that
    have to be kept equal. `main()` runs `verify()` first for exactly that
    reason.

    The shape guard runs here too, so this function is safe called standalone
    and cannot compare a gitlink against a movable name.

    One implementation, one refusal vocabulary: this reuses
    `_recorded_gitlink`, so the aggregation gets the same HEAD-then-index
    resolution and the same two codes rather than a parallel dialect.
    """
    pin = load_pin() if pin is None else pin
    submodule_path = _submodule_path(pin)
    commit = _pinned_commit(pin)

    recorded, source = _recorded_gitlink(aggregation_root, submodule_path)
    if recorded is None:
        # NOT a pass. An aggregation that is supposed to carry this pin and
        # carries no gitlink for it at all has silently stopped participating in
        # the pin, which is the failure this check exists to catch; treating an
        # absent declaration as "nothing to disagree with" would make the whole
        # aggregation check opt-out by omission.
        raise PinRefusal(
            "pin-member-missing",
            f"the aggregation root {aggregation_root} declares no "
            f"{GITLINK_MODE} gitlink for {submodule_path} in HEAD or in its "
            "index; a consumer that is supposed to carry this pin and carries "
            "no gitlink for it is not passing, it is not participating")
    if recorded != commit:
        raise PinRefusal(
            "pin-gitlink-mismatch",
            f"the aggregation root {aggregation_root} records "
            f"{submodule_path} at {recorded} (read from {source}), but "
            f"{root}'s pin records {commit}; the aggregation and openxFactory "
            "disagree about which openxWallet revision the workspace consumes")


# --------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Print one line and return 0, or print the refusal to stderr and return 2.

    Every failure path returns 2; see the module docstring for why there is no
    exit 1.
    """
    parser = argparse.ArgumentParser(
        prog="verify-openxwallet-pin.py",
        description=("Verify contracts/openxwallet-pin.yaml against the "
                     "openXwallet gitlink, checkout and digests. Offline."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--aggregation-root", metavar="PATH", default=None,
        help=("also require the aggregation checkout at PATH to record the "
              "same openXwallet gitlink as this pin"))
    args = parser.parse_args(argv)

    try:
        pin = verify()
        if args.aggregation_root is not None:
            verify_aggregation(Path(args.aggregation_root), pin=pin)
    except PinRefusal as exc:
        print(str(exc), file=sys.stderr)
        return 2

    # Re-resolved here rather than returned from `verify()`, which is contracted
    # to return the pin and to print nothing: the source of the recorded gitlink
    # is a fact about the RUN and belongs in the run's output, and one extra
    # `ls-tree` is cheaper than widening a return type other code depends on.
    _, source = _recorded_gitlink(ROOT, _submodule_path(pin))
    commit = _pinned_commit(pin)
    digests = len(pin.get("files") or [])
    note = (f"OK openxwallet-pin verified: openXwallet@{commit} "
            f"(tag label {pin.get('contract_bundle_tag', '<unlabelled>')}), "
            f"gitlink read from {source}, {digests} digest(s) recomputed")
    if args.aggregation_root is not None:
        note += f", aggregation root {args.aggregation_root} agrees"
    print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
