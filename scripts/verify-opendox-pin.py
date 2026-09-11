#!/usr/bin/env python3
"""Verify openxFactory's CONSUMPTION of opensoft/openDox against its pin.

openxFactory does not OWN openDox; it MOUNTS it as a submodule and CONSUMES it
at a commit and a whole-tree digest. `contracts/opendox-pin.yaml` is the whole
of that claim and this file is the running code that checks it. Modelled on
`scripts/verify-openxdox-pin.py`, which this file mirrors check-for-check for
the first four checks, departing only where the artifact departs: a SECOND
direct upstream now exists, and this tool is the one that has to prove the two
never disagree.

RULING F IS SUPERSEDED FOR THIS SECOND UPSTREAM. RULING F (Brett Heap,
`opensoft/openxFactory#656`, 2026-09-05, *"rule F openXdox only"*) held that
openxFactory pins openXdox and nothing else, and that openDox's commit is a
DERIVED value read only through openXdox's own `contracts/opendox-pin.yaml`.
Brett Heap's Q7 ruling (`#656` comment `5626248666`, 2026-09-10) supersedes
that sentence FOR OPENDOX ONLY: openxFactory now mounts the openDox assembly
root as a SECOND submodule and pins it DIRECTLY, mirroring the openXdox pin of
PR #917. `scripts/verify-openxdox-pin.py` is UNCHANGED and UNTOUCHED by this
file — it still has no openDox check of its own, on its own docstring's
"must never grow one", because that check now lives HERE instead, and the
tools are two independent verifiers rather than one tool learning a second
job.

WHY A SECOND DIRECT PIN NEEDS A LOCKSTEP CHECK, AND WHY IT DID NOT BEFORE.
Before this pin existed, openDox's commit had exactly ONE declaration in this
repository's reach: openXdox's own `contracts/opendox-pin.yaml`. Adding a
SECOND, independent declaration — this file — recreates precisely the defect
`neutral-product-pin`'s chain clause exists to end: two answers to "which
bytes are pinned" is no answer, UNLESS something holds them equal. Check 5
below is that something: it reads `openXdox/contracts/opendox-pin.yaml`'s own
`commit` as a git BLOB, from the openXdox submodule's own object store, AT THE
COMMIT THE SUPERPROJECT'S `openXdox` GITLINK RECORDS — `git show
<oid>:contracts/opendox-pin.yaml`, never the submodule's mutable working tree
— and refuses `opendox-pin-lockstep-mismatch` the moment it disagrees with
this pin's own `commit`. Reading the working tree would let an operator edit
that file, without moving the `openXdox` gitlink or its own commit, into
momentary agreement with a stale direct pin; reading the blob the gitlink
itself names is what makes two direct upstreams of the same product safe
rather than a second, driftable answer that a dirty checkout can silence.

SIX CODES, NOT FIVE: THE FIRST FIVE ARE `openxdox-pin-*`'s SHAPE RENAMED, THE
SIXTH IS NEW. `opendox-pin-tag-only`, `opendox-pin-submodule-uninitialized`,
`opendox-pin-gitlink-mismatch`, `opendox-pin-checkout-mismatch` and
`opendox-pin-digest-mismatch` are `verify-openxdox-pin.py`'s own five,
re-prefixed for this product on that file's own reasoning (a shared vocabulary
would make an openDox refusal indistinguishable from an openXdox refusal to
any caller that branches on the string). `opendox-pin-lockstep-mismatch` is
the one code this tool adds, for the one check that tool has no analogue of.

THE TRUSTED REFERENT IS `commit` PLUS `digests.tree_sha256`, AND THERE IS NO
PER-FILE LIST, on `contracts/opendox-pin.yaml`'s own reasoning: openDox's own
`contracts/manifest.yaml` declares `entries: []`, and the whole-tree digest
discharges the completeness obligation a per-file list would otherwise carry,
more strongly.

OFFLINE LAW, WITH ONE NAMED EXTENSION. Checks 1-4 read this pin file, the
`openDox` gitlink, and the `openDox/` submodule's own object store — never the
network, and never `openDox`'s own `contracts/manifest.yaml`. Check 5 ALSO
reads a blob out of the SECOND submodule this repository already mounts —
`openXdox`'s own object store, at whatever commit the superproject's `openXdox`
gitlink records (the index when it has moved the entry, HEAD otherwise,
exactly as check 2 does) — never the `openXdox` working tree and never the
network. That is a local `git show` against an object store already on disk,
so the offline property holds for the whole verifier, not only for its first
four checks.

`pin-unreadable` IS NOT IN THE VOCABULARY, on `verify-openxdox-pin.py`'s own
reasoning. The six describe a TREE that disagrees with a well-formed pin, or
two well-formed pins that disagree with EACH OTHER — each a governed finding a
reviewer can act on. `pin-unreadable` describes an ENVIRONMENT in which no
finding can be reached at all: the `openXdox` gitlink recorded nowhere, that
submodule not initialized, the gitlinked commit's blob missing from its object
store, or openXdox's own `contracts/opendox-pin.yaml` malformed (too old a
commit to carry the key) — in every case the LOCKSTEP question cannot be
ASKED, so it is not one of the six. It still exits 2 like everything else.

WHAT THIS TOOL IS NOT. It is not wired into any required check — wiring a
consumer gate is Phase 5's task 5.3, on `verify-openxdox-pin.py`'s own
precedent. It carries no `--aggregation-root` mode, for the same reason that
file does not: `opensoft/xFactory` records no `openDox` gitlink today.

USED AS A LIBRARY, on `verify-openxdox-pin.py`'s own contract. `verify()`
neither prints nor exits: it raises, and the caller decides. All printing and
all exiting lives in `main()`.

Exit codes:
  0  the pin is satisfied: the recorded gitlink and the checkout both equal
     `commit`, the tree digest recomputes to `digests.tree_sha256`, AND
     openXdox's own derived reading of openDox's commit agrees
  2  ANY refusal, and any environment failure

  There is deliberately NO exit 1, on `verify-openxwallet-pin.py`'s and
  `verify-openxdox-pin.py`'s shared reasoning: the only question a consumer
  gate asks is "may this pull request proceed", the answer to which is
  identical for every refusal and for an unreadable environment alike.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "contracts" / "opendox-pin.yaml"

# Where openXdox's OWN pin of openDox lives — the path a reader would find it
# at in a normal checkout, used here only to LABEL the value check 5 reads
# (the read itself is a `git show <oid>:contracts/opendox-pin.yaml` against
# the openXdox submodule's own object store, never a `Path` open against this
# relative path; see `_openxdox_derived_commit`). Never re-declared, only
# READ, on this file's own "two answers" reasoning.
OPENXDOX_DERIVED_PIN_RELPATH = Path("openXdox") / "contracts" / "opendox-pin.yaml"

# The ONE fixed remediation trailer for every fail-closed refusal in this
# file. Both gitlinks are named because check 5 needs openXdox initialized
# too — a caller who only ran `git submodule update --init openDox` would hit
# a SECOND environment failure immediately after fixing the first.
# `--recursive` is deliberately absent, on the estate's scoped-init
# discipline: openxFactory initializes the two submodules it has business
# with, and neither product's own `code`/`spec` legs are among them.
REMEDIATION = (
    "Remediation: run `git submodule update --init openDox openXdox` (NOT "
    "--recursive; the legs are not consumed here). If the pin itself is "
    "stale, follow `openDox/README.md#the-lockstep-invariant` for the "
    "gitlink and this pin file, or `docs/opendox-cutover-runbook.md` § 7 for "
    "the cross-repository LOCKSTEP invariant against openXdox's own pin — "
    "whichever side is stale is re-pinned in one commit.")

# The six refusal codes, in the order they can be reached. The first five are
# `verify-openxdox-pin.py`'s own shape, re-prefixed for this product; the
# sixth has no analogue there. See the module docstring.
REFUSAL_CODES: tuple[str, ...] = (
    "opendox-pin-tag-only",
    "opendox-pin-submodule-uninitialized",
    "opendox-pin-gitlink-mismatch",
    "opendox-pin-checkout-mismatch",
    "opendox-pin-digest-mismatch",
    "opendox-pin-lockstep-mismatch",
)

# Exactly 40 / 64 hex, case-insensitive, normalized to lowercase before any
# comparison, unchanged from `verify-openxdox-pin.py`.
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")

# The gitlink mode. A submodule entry is mode 160000 in `ls-tree` and in
# `ls-files -s` alike.
GITLINK_MODE = "160000"

# The ONE digest definition this tool implements, spelled exactly as the pin
# family spells it.
DIGEST_DEFINITION = "sorted-ls-tree-r-v1"
DIGEST_ALGORITHM = "sha256"

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required to read contracts/opendox-pin.yaml",
          file=sys.stderr)
    sys.exit(2)


class PinRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail`,
    unchanged from `verify-openxdox-pin.py`'s own contract: `str(exc)` renders
    code, detail and the fixed remediation trailer as one message, and
    `main()` prints exactly that.
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
    """The pin as a mapping, or `pin-unreadable`."""
    if not pin_path.is_file():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} does not exist; openxFactory consumes "
            "openDox only through this pin, so its absence is not an "
            "unpinned pass but an unanswerable question")
    try:
        loaded = yaml.safe_load(pin_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError, UnicodeDecodeError) as exc:
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
    """The `submodule_path` the pin governs."""
    raw = pin.get("submodule_path")
    if not isinstance(raw, str) or not raw.strip():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares no usable `submodule_path` (got {raw!r}); a pin "
            "with no path cannot be checked against a gitlink")
    return raw.strip()


def _pinned_commit(pin: dict) -> str:
    """The 40-hex referent, lowercased, or `opendox-pin-tag-only`."""
    revision_kind = pin.get("revision_kind")
    if revision_kind != "commit":
        raise PinRefusal(
            "opendox-pin-tag-only",
            f"the pin declares revision_kind {revision_kind!r}, not 'commit'; "
            "the trusted referent is a commit plus a tree digest, and resolving "
            "a movable name would require exactly the network read this "
            "verifier refuses to perform")
    commit = pin.get("commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit.strip()):
        raise PinRefusal(
            "opendox-pin-tag-only",
            f"the pin records commit {commit!r}, which is not exactly 40 hex "
            "characters; an abbreviated oid, a branch or a tag is not a "
            "compatibility pin")
    return commit.strip().lower()


def _pinned_tree_digest(pin: dict) -> str:
    """The recorded `digests.tree_sha256`, lowercased."""
    algorithm = pin.get("digest_algorithm")
    if algorithm != DIGEST_ALGORITHM:
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares digest_algorithm {algorithm!r}; this verifier "
            f"implements {DIGEST_ALGORITHM!r} only and cannot compute the value "
            "it is being asked to compare")
    definition = pin.get("digest_definition")
    if definition != DIGEST_DEFINITION:
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares digest_definition {definition!r}; this verifier "
            f"implements {DIGEST_DEFINITION!r} only, the one definition the "
            "openDox/openXdox pin family uses, and a definition it cannot "
            "compute is an unanswerable question rather than a finding about "
            "the tree")
    digests = pin.get("digests")
    if not isinstance(digests, dict):
        raise PinRefusal(
            "pin-unreadable",
            f"the pin's `digests` is not a mapping ({digests!r}); the tree "
            "digest is the whole of what this pin digests, so a pin that "
            "records none pins no bytes")
    recorded = digests.get("tree_sha256")
    if not isinstance(recorded, str) or not SHA256_RE.match(recorded.strip()):
        raise PinRefusal(
            "opendox-pin-digest-mismatch",
            f"the pin records digests.tree_sha256 {recorded!r}, which is not 64 "
            "hex characters; a recomputed digest can never equal a digest that "
            "is not one")
    return recorded.strip().lower()


# --------------------------------------------------------------------------
# reading gitlinks
# --------------------------------------------------------------------------

def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          capture_output=True, text=True, check=False)


def _git_bytes(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    """`_git` without text decoding — see `tree_digest`."""
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          capture_output=True, check=False)


def _gitlink_from(output: str, submodule_path: str) -> str | None:
    """The object id of the `160000` entry for `submodule_path`, or None."""
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
    """(oid, source) for the RECORDED gitlink: the index when it has moved
    the entry, HEAD otherwise.

    A ONE-COMMIT RESYNC MUST BE CHECKABLE BEFORE IT IS COMMITTED, not only
    for a BRAND NEW gitlink (`git submodule add`, nothing in HEAD yet) but
    also for an EXISTING one being moved to a new commit (`git -C openDox
    checkout <new>` then `git add openDox`, which stages the new oid over an
    old one HEAD still names). A HEAD-first read answers for the commit
    being REPLACED in that second case — `ls-tree HEAD` still finds the OLD
    160000 entry and returns it without ever consulting the index — which can
    falsely REJECT a fresh, correct re-pin (checks 2 and 3 compare the new
    checkout against the stale HEAD oid) or, for check 5's `openXdox` read via
    this same helper, falsely VALIDATE against the derived commit the pin is
    being moved away from. So both records are read, and the index wins
    whenever it disagrees with HEAD (new-and-staged, or replaced-and-staged
    alike); only when the index agrees with HEAD — the ordinary clean tree —
    or has no entry at all does HEAD's own oid answer, which is what keeps
    the success message's "read from HEAD" true for the common case instead
    of manufacturing a spurious "staged" label for bytes nothing has staged.
    """
    head = _git(repo_root, "ls-tree", "HEAD", "--", submodule_path)
    head_oid = (_gitlink_from(head.stdout, submodule_path)
               if head.returncode == 0 else None)
    index = _git(repo_root, "ls-files", "-s", "--", submodule_path)
    index_oid = (_gitlink_from(index.stdout, submodule_path)
                if index.returncode == 0 else None)
    if index_oid is not None and index_oid != head_oid:
        return index_oid, "the index (staged, not yet committed)"
    if head_oid is not None:
        return head_oid, "HEAD"
    if index_oid is not None:
        return index_oid, "the index (staged, not yet committed)"
    return None, "nowhere"


# --------------------------------------------------------------------------
# the digest
# --------------------------------------------------------------------------

def tree_digest(sub_root: Path, revision: str) -> str:
    """`sorted-ls-tree-r-v1` over `revision`'s whole tree.

    Byte-for-byte `verify-openxdox-pin.py`'s own `tree_digest`, retargeted at
    `openDox`. Re-implemented rather than imported, for the same reason that
    file gives: `repo_shape.py` lives in `opensoft/openRepoShape`, which this
    repository pins but does not mount.
    """
    proc = _git_bytes(sub_root, "ls-tree", "-r", "-z", revision)
    if proc.returncode != 0:
        raise PinRefusal(
            "pin-unreadable",
            f"`git -C {sub_root} ls-tree -r -z {revision}` failed, so the tree "
            "digest cannot be recomputed: "
            f"{proc.stderr.decode('utf-8', 'replace').strip() or 'no error output'}")
    records = sorted(r for r in proc.stdout.split(b"\x00") if r)
    digest = hashlib.sha256()
    for record in records:
        digest.update(record)
        digest.update(b"\n")
    return digest.hexdigest()


# --------------------------------------------------------------------------
# the lockstep check
# --------------------------------------------------------------------------

def _openxdox_derived_commit(root: Path) -> str:
    """The openDox commit openXdox's OWN pin derives, read from the COMMIT the
    superproject's `openXdox` gitlink names — never the mutable working tree.

    An operator can edit `openXdox/contracts/opendox-pin.yaml` ON DISK without
    moving the `openXdox` gitlink or the commit that submodule is actually
    pinned to; a check that read that working-tree file would report lockstep
    agreement even though the openXdox commit this repository is PINNED TO
    still disagrees. So this reads a git BLOB instead: `_recorded_gitlink`
    finds the `openXdox` gitlink exactly as check 2 finds `openDox`'s own (the
    index when it has moved the entry, HEAD otherwise), and `git -C openXdox
    show <oid>:contracts/opendox-pin.yaml` reads the pin file's bytes out of
    the openXdox submodule's own object store AT THAT COMMIT — a local read of
    an object this repository already has (the commit it is pinned to), never
    the network and never whatever happens to be checked out on disk.

    Every failure to locate the gitlink or to read or parse the blob it names
    is `pin-unreadable`: the LOCKSTEP question cannot be asked without it, so
    an absent or malformed derived pin is an environment fact rather than a
    finding that the two commits disagree.
    """
    openxdox_root = root / "openXdox"
    if not (openxdox_root / ".git").exists():
        raise PinRefusal(
            "pin-unreadable",
            f"{openxdox_root}/.git does not exist: the LOCKSTEP check reads "
            "openXdox's own derived reading of openDox's commit from the "
            "openXdox submodule's object store, which requires openXdox to "
            "be initialized (`git submodule update --init openXdox`)")

    oid, source = _recorded_gitlink(root, "openXdox")
    if oid is None:
        raise PinRefusal(
            "pin-unreadable",
            f"{root} records no {GITLINK_MODE} gitlink for openXdox in HEAD "
            "or in the index: the LOCKSTEP check has no openXdox commit to "
            "read openDox's derived pin from")

    blob_ref = f"{oid}:contracts/opendox-pin.yaml"
    show = _git_bytes(openxdox_root, "show", blob_ref)
    if show.returncode != 0:
        raise PinRefusal(
            "pin-unreadable",
            f"`git -C {openxdox_root} show {blob_ref}` failed (openXdox "
            f"gitlink {oid} read from {source}): "
            f"{show.stderr.decode('utf-8', 'replace').strip() or 'no error output'}; "
            "the openXdox object store may be missing this commit — run "
            "`git submodule update --init openXdox`")

    try:
        text = show.stdout.decode("utf-8")
        loaded = yaml.safe_load(text)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise PinRefusal(
            "pin-unreadable",
            f"openXdox@{oid}:contracts/opendox-pin.yaml could not be read as "
            f"YAML: {exc}") from exc
    if not isinstance(loaded, dict):
        raise PinRefusal(
            "pin-unreadable",
            f"openXdox@{oid}:contracts/opendox-pin.yaml is not a mapping "
            f"(parsed as {type(loaded).__name__})")
    commit = loaded.get("commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit.strip()):
        raise PinRefusal(
            "pin-unreadable",
            f"openXdox@{oid}:contracts/opendox-pin.yaml records commit "
            f"{commit!r}, which is not exactly 40 hex characters; the "
            "LOCKSTEP comparison cannot be made against a value that is not "
            "one")
    return commit.strip().lower()


# --------------------------------------------------------------------------
# the checks
# --------------------------------------------------------------------------

def verify(root: Path = ROOT, pin: dict | None = None) -> dict:
    """Run the ordered checks against `root`; return the pin on success.

    Checks 1-4 mirror `verify-openxdox-pin.py`'s own four, retargeted at
    `openDox`: first failure, named correctly, beats several failures that
    need triage. Check 5 is new and runs LAST, once this pin has been proved
    an accurate description of the openDox bytes actually present — only then
    is "do the two direct pins agree" the remaining question.

    Prints nothing and exits nothing.
    """
    pin = load_pin() if pin is None else pin
    submodule_path = _submodule_path(pin)
    commit = _pinned_commit(pin)
    recorded_digest = _pinned_tree_digest(pin)
    sub_root = root / submodule_path

    # ---- check 1: the submodule is initialized at all -----------------------
    if not (sub_root / ".git").exists():
        raise PinRefusal(
            "opendox-pin-submodule-uninitialized",
            f"{submodule_path}/.git does not exist: the submodule is not "
            f"initialized in {root}, so the openDox tree this repository "
            "consumes is not present to be checked")

    # ---- check 2: the RECORDED gitlink equals `commit` ---------------------
    recorded, source = _recorded_gitlink(root, submodule_path)
    if recorded is None:
        raise PinRefusal(
            "opendox-pin-gitlink-mismatch",
            f"{root} records no {GITLINK_MODE} gitlink for {submodule_path} in "
            "HEAD or in the index: the gitlink is recorded NOWHERE, so there is "
            f"nothing to compare against the pinned {commit}. A submodule "
            "present on disk but absent from the tree is not a pinned "
            "consumption")
    if recorded != commit:
        raise PinRefusal(
            "opendox-pin-gitlink-mismatch",
            f"the gitlink {root} records for {submodule_path} (read from "
            f"{source}) is {recorded}, but the pin records {commit}; the tree "
            "and the pin disagree about which openDox revision this repository "
            "consumes. The gitlink is the commit pin itself, so the two are "
            "one invariant and move in ONE commit")

    # ---- check 3: the CHECKED-OUT revision equals `commit` -----------------
    head = _git(sub_root, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise PinRefusal(
            "opendox-pin-checkout-mismatch",
            f"`git -C {sub_root} rev-parse HEAD` failed, so the checked-out "
            f"revision cannot be compared against the pinned {commit}: "
            f"{head.stderr.strip() or 'no error output'}")
    checked_out = head.stdout.strip().lower()
    if checked_out != commit:
        raise PinRefusal(
            "opendox-pin-checkout-mismatch",
            f"{submodule_path} is checked out at {checked_out}, but the pin "
            f"records {commit}; the recorded gitlink agrees with the pin, so "
            "the tree is right and the working checkout is stale")

    # ---- check 4: the tree digest recomputes -------------------------------
    actual = tree_digest(sub_root, commit)
    if actual != recorded_digest:
        raise PinRefusal(
            "opendox-pin-digest-mismatch",
            f"{submodule_path}: TREE DIGEST DRIFT ({DIGEST_DEFINITION})\n"
            f"  recorded   {recorded_digest}\n"
            f"  recomputed {actual}\n"
            f"the bytes on disk are not the bytes the pin consumes at "
            f"openDox@{commit[:12]}")

    # ---- check 5: LOCKSTEP with openXdox's own derived reading -------------
    # THE ONE CHECK WITH NO ANALOGUE IN `verify-openxdox-pin.py`. Two direct
    # declarations of one product's bytes — this pin's own `commit`, and
    # openXdox's own `contracts/opendox-pin.yaml` `commit` — must agree or
    # neither is trustworthy; this is what makes the second direct upstream
    # RULED Q7 safe rather than a second, driftable answer.
    derived = _openxdox_derived_commit(root)
    if derived != commit:
        raise PinRefusal(
            "opendox-pin-lockstep-mismatch",
            f"this pin names openDox@{commit}, but openXdox's own "
            f"{OPENXDOX_DERIVED_PIN_RELPATH} names openDox@{derived}; two "
            "direct declarations of one product's bytes disagree. Re-pin "
            "whichever side is stale, in one commit, following "
            "docs/opendox-cutover-runbook.md § 7")

    return pin


# --------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Print one line and return 0, or print the refusal to stderr and return 2."""
    parser = argparse.ArgumentParser(
        prog="verify-opendox-pin.py",
        description=("Verify contracts/opendox-pin.yaml against the openDox "
                     "gitlink, checkout, tree digest, and LOCKSTEP with "
                     "openXdox's own derived reading. Offline."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args(argv)

    try:
        pin = verify()
    except PinRefusal as exc:
        print(str(exc), file=sys.stderr)
        return 2

    _, source = _recorded_gitlink(ROOT, _submodule_path(pin))
    commit = _pinned_commit(pin)
    print(f"OK opendox-pin verified: openDox@{commit}, gitlink read from "
          f"{source}, {DIGEST_DEFINITION} tree digest recomputed "
          f"({_pinned_tree_digest(pin)}), lockstep with openXdox confirmed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
