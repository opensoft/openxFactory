#!/usr/bin/env python3
"""Verify openxFactory's CONSUMPTION of opensoft/openXdox against its pin.

openxFactory does not OWN openXdox; it MOUNTS it as a submodule and CONSUMES it
at a commit and a whole-tree digest. `contracts/openxdox-pin.yaml` is the whole
of that claim and this file is the running code that checks it. Everything the
pin asserts is checked here, and nothing that is not asserted is inferred.

RULING F (Brett Heap, `opensoft/openxFactory#656`, 2026-09-05, *"rule F openXdox
only"*). openxFactory pins openXdox and NOTHING ELSE. openDox's commit is a
DERIVED value, read through openXdox's own `contracts/opendox-pin.yaml` at the
commit this pin names, and it is never separately declared, pinned or mounted
here. This tool therefore has no openDox check and must never grow one: a second
declaration of a transitive upstream's commit is the "two answers to which bytes
are pinned" defect the `neutral-product-pin` chain clause exists to end.

THE TRUSTED REFERENT IS `commit` PLUS `digests.tree_sha256`, AND THERE IS NO
PER-FILE LIST. That is a departure from `contracts/openxwallet-pin.yaml`, which
carries eight `files:` digests and a `pinned_by_commit_only:` list, and the
reason is not economy:

  * openXdox's own `contracts/manifest.yaml` declares `contract_bundle_version:
    none` and `entries: []`. `neutral-product-pin` keys the per-file obligation
    to "every artifact the product's own manifest digests per file", and that
    set is EMPTY — the list has no members to carry, rather than members left
    out.
  * The whole-tree digest discharges the completeness obligation those two
    lists exist to serve, and discharges it more strongly. The capability's own
    words for the published-artifact medium apply verbatim to a whole-tree
    digest over a source tree: "ONE digest addresses EVERY byte inside it, so no
    member can be undeclared and none can be added or altered without changing
    the referent."
  * It is the shape the rest of this carve's pin family already uses.
    `openXdox/contracts/code-pin.yaml` and `spec-pin.yaml` carry
    `digest_definition: sorted-ls-tree-r-v1` and `digests.tree_sha256` and no
    per-file list at all, and `docs/opendox-cutover-runbook.md` § 7 names what
    this file carries as "`carve_commit:` … beside the commit and tree digest".

WHY THE NESTED `code` AND `spec` GITLINKS ARE NOT DESCENDED INTO. openXdox is an
assembly root whose own code lives one level further down, in its `code`
submodule. openxFactory's mount is NOT recursive, so those two paths are empty
directories in this checkout, and the digest does not need them: `git ls-tree
-r` reports a gitlink as an opaque `160000 commit <oid>` record and never reads
through it. A leg pin moving inside openXdox therefore still changes this
digest — the oid is in the record — while requiring no nested materialization to
detect. Descending would make the check depend on two more clones and would
verify bytes this pin does not name.

OFFLINE LAW. This tool reads the pin file, the gitlink, and the submodule's own
object store. It never reads the network, never reads an upstream tree, and
never reads openXdox's own `contracts/manifest.yaml` or `contracts/opendox-pin.yaml`.
A gate that reaches the network to decide whether it passes is a gate whose
answer depends on the network.

TWO GITLINK COMPARISONS, NOT ONE, on `verify-openxwallet-pin.py`'s reasoning
unchanged. Check 2 compares the RECORDED gitlink (what the tree says the
submodule should be) and check 3 compares the CHECKED-OUT revision (what the
submodule actually is). Neither subsumes the other: a stale `git submodule
update` leaves the recorded gitlink correct and the checkout wrong, while a
bumped-and-committed gitlink with no checkout inverts that. One comparison would
pass in exactly the half of the world it is blind to. Check 4 recomputes the
digest against the CHECKOUT, so without check 3 a wrong revision on disk would
be reported as content drift.

WHY THE CODES ARE PREFIXED `openxdox-`. `verify-openxwallet-pin.py`'s six codes
are a RATIFIED vocabulary (wallet spec FR-003) and other code — the consumer
gate workflow, `validate-trust-anchor.py` — refuses BY CODE against it. Reusing
those exact tokens here would make an openXdox refusal indistinguishable from a
wallet refusal to any consumer that branches on the string, so this tool
declares its own five and prefixes them. The tuple is imported from nowhere and
imports nothing: two products, two vocabularies, no shared mutable list.

`pin-member-missing` HAS NO ANALOGUE HERE, and the reason is narrower than it
first looks. The wallet's fifth code exists to report a `files:` or
`pinned_by_commit_only:` member absent from the checkout; this pin enumerates no
members, so there is no such finding to name.

WHAT THAT LEAVES UNCHECKED, STATED PLAINLY RATHER THAN GLOSSED. `tree_digest`
runs `git ls-tree -r -z <commit>`, which reads the COMMIT'S TREE OBJECT — so
this verifier answers "does the commit this repository consumes contain the
bytes the pin says it contains", and it does NOT answer "is the working tree
below the gitlink still those bytes". A file deleted or edited under `openXdox/`
after checkout leaves every check here passing, and
`tests/openxdox_pin/test_openxdox_pin_verifier.py::
test_a_working_tree_deletion_is_deliberately_not_drift` pins that behaviour so
the claim cannot rot back into the overclaim it replaced. This is a REAL
NARROWING against `verify-openxwallet-pin.py`, whose `pin-member-missing` does
catch a working-tree deletion, and it is recorded as OWED rather than argued
away: whether the consumer gate wired in task 5.3 (Phase 5) also needs a
dirty-checkout refusal is that task's call to make, with this paragraph as the
input. In CI the question is close to moot — the checkout is materialized from
the gitlink on every run — so the exposure is a local run, which is exactly
where a reader most needs the tool to say what it did and did not check.

`pin-unreadable` IS NOT IN THE VOCABULARY, on the wallet verifier's own
reasoning. The five describe a TREE that disagrees with a well-formed pin —
each is a governed finding a reviewer can act on. `pin-unreadable` describes an
ENVIRONMENT in which no finding can be reached at all: the pin is absent, does
not parse, is not a mapping, names a digest definition this tool does not
implement, or PyYAML is missing. It still exits 2 like everything else — it is
excluded from the vocabulary, not from fail-closure.

WHAT THIS TOOL IS NOT. It is not wired into any required check. `Phase 4`
(`docs/opendox-cutover-runbook.md` § 7) mounts the submodule and writes the pin;
wiring a consumer gate that runs this file is task 5.3, Phase 5. Nor does it
carry the wallet's `--aggregation-root` mode: `opensoft/xFactory` records no
`openXdox` gitlink at all today, so an aggregation-parity check would refuse by
construction, and adding that gitlink is a change to a different repository.
The aggregation half of `neutral-product-pin`'s *The consuming repository's pin
is authoritative among reachable checkouts* is therefore OWED, not discharged.

USED AS A LIBRARY, on the wallet verifier's contract. `verify()` neither prints
nor exits: it raises, and the caller decides. All printing and all exiting lives
in `main()`. There is no import-time I/O beyond the path constants below.

Exit codes:
  0  the pin is satisfied: the recorded gitlink and the checkout both equal
     `commit`, and the tree digest recomputes to `digests.tree_sha256`
  2  ANY refusal, and any environment failure

  There is deliberately NO exit 1, on the wallet verifier's reasoning. The only
  question a consumer gate asks is "may this pull request proceed", the answer
  to which is identical for "the pin is stale" and "the submodule was never
  initialized", and a two-valued failure invites a workflow that treats one of
  them as a warning. An unanswerable question is never an implicit pass.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "contracts" / "openxdox-pin.yaml"

# The ONE fixed remediation trailer for every fail-closed refusal in this file.
# `--recursive` is deliberately absent and the parenthetical says so out loud,
# matching the wallet verifier's own trailer and this repository's scoped-init
# discipline: openxFactory initializes the one submodule it has business with,
# and openXdox's own `code`/`spec` legs are not among them.
REMEDIATION = (
    "Remediation: run `git submodule update --init openXdox` (NOT --recursive; "
    "openXdox's own code/spec legs are not consumed here). If the pin itself "
    "is stale, follow `openXdox/README.md#the-lockstep-invariant` — the "
    "gitlink and this pin file move in ONE commit."
)

# The five refusal codes, in the order they can be reached.
#
# Prefixed `openxdox-` rather than reusing the wallet's ratified six: see the
# module docstring. Nothing downstream consumes this vocabulary yet — the
# consumer gate is task 5.3, Phase 5 — which is exactly why it is fixed now,
# before something starts branching on a string that has not settled.
REFUSAL_CODES: tuple[str, ...] = (
    "openxdox-pin-tag-only",
    "openxdox-pin-submodule-uninitialized",
    "openxdox-pin-gitlink-mismatch",
    "openxdox-pin-checkout-mismatch",
    "openxdox-pin-digest-mismatch",
)

# Exactly 40 / 64 hex, case-insensitive, normalized to lowercase before any
# comparison. The shape stays strict — 40 means 40, so an abbreviated oid or a
# branch name cannot pass — but case is normalized rather than rejected: git
# emits lowercase, so an uppercase value in the pin is a hand-edit rather than a
# movable reference, and refusing it as a tag would name the wrong defect.
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")

# The gitlink mode. A submodule entry is mode 160000 in `ls-tree` and in
# `ls-files -s` alike; matching on the MODE rather than on the path column is
# what makes a same-named regular file or symlink at that path fail to satisfy
# the check instead of accidentally satisfying it.
GITLINK_MODE = "160000"

# The ONE digest definition this tool implements, spelled exactly as the pin
# family spells it (`openXdox/contracts/code-pin.yaml`,
# `openXdox/contracts/spec-pin.yaml`, `openXdox/contracts/opendox-pin.yaml`). A
# pin naming any other definition is `pin-unreadable` and NOT drift: this tool
# cannot compute the value it is being asked to compare, so the tree is not what
# is wrong.
DIGEST_DEFINITION = "sorted-ls-tree-r-v1"
DIGEST_ALGORITHM = "sha256"

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required to read contracts/openxdox-pin.yaml",
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

    Every failure here is an environment failure rather than one of the five:
    without a parseable pin there is no claim to check, and a tool that cannot
    read its own claim must not report the tree as conformant.
    """
    if not pin_path.is_file():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} does not exist; openxFactory consumes "
            "openXdox only through this pin, so its absence is not an unpinned "
            "pass but an unanswerable question")
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

    Read from the pin rather than hard-coded, because a verifier that ignored
    the field the pin declares would check a path the pin never claimed. Its
    absence is `pin-unreadable` and not one of the five: a pin with no path
    cannot be compared against any gitlink, so the tree is not what is wrong.
    """
    raw = pin.get("submodule_path")
    if not isinstance(raw, str) or not raw.strip():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares no usable `submodule_path` (got {raw!r}); a pin "
            "with no path cannot be checked against a gitlink")
    return raw.strip()


def _pinned_commit(pin: dict) -> str:
    """The 40-hex referent, lowercased, or `openxdox-pin-tag-only`.

    Evaluated FIRST, ahead of the gitlink comparisons that read it. Leaving the
    shape guard until after them would let a malformed pin (`revision_kind:
    tag`, an abbreviated oid, a branch name) be reported as a gitlink mismatch:
    a code that says the TREE is wrong about a pin that is itself the thing that
    is wrong, and a code that sends a reviewer to `git submodule update`
    instead of to the pin.
    """
    revision_kind = pin.get("revision_kind")
    if revision_kind != "commit":
        raise PinRefusal(
            "openxdox-pin-tag-only",
            f"the pin declares revision_kind {revision_kind!r}, not 'commit'; "
            "the trusted referent is a commit plus a tree digest, and resolving "
            "a movable name would require exactly the network read this "
            "verifier refuses to perform")
    commit = pin.get("commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit.strip()):
        raise PinRefusal(
            "openxdox-pin-tag-only",
            f"the pin records commit {commit!r}, which is not exactly 40 hex "
            "characters; an abbreviated oid, a branch or a tag is not a "
            "compatibility pin")
    return commit.strip().lower()


def _pinned_tree_digest(pin: dict) -> str:
    """The recorded `digests.tree_sha256`, lowercased.

    THE DEFINITION IS CHECKED BEFORE THE VALUE, and the two failures are
    deliberately different codes. A pin naming a digest definition or algorithm
    this tool does not implement is `pin-unreadable`: the question cannot be
    asked, and reporting it as drift would send a reviewer to look for a changed
    byte that is not there. A pin naming THIS definition with a malformed value
    is `openxdox-pin-digest-mismatch`, on the wallet verifier's own reasoning —
    a recomputed digest can never equal a digest that is not one, so the member
    is unverifiable, which is the same operational fact as a member that
    verified wrongly.
    """
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
            "openXdox pin family uses, and a definition it cannot compute is "
            "an unanswerable question rather than a finding about the tree")
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
            "openxdox-pin-digest-mismatch",
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
    """`_git` without text decoding.

    SEPARATE FROM `_git` ON PURPOSE. The digest is defined over the raw bytes of
    `ls-tree -r -z`, and a path that is not valid UTF-8 would be replaced or
    would raise under text mode — either way producing a digest over bytes that
    are not the bytes in the tree. The definition says raw records, so the read
    is raw.
    """
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          capture_output=True, check=False)


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
    """(oid, source) for the RECORDED gitlink: a successful index read
    whenever it DISAGREES with HEAD, HEAD when the two agree, "nowhere" when
    neither has one.

    A ONE-COMMIT RESYNC MUST BE CHECKABLE BEFORE IT IS COMMITTED, not only
    for a BRAND NEW gitlink (`git submodule add`, nothing in HEAD yet) but
    also for an EXISTING one being moved to a new commit (`git -C openXdox
    checkout <new>` then `git add openXdox`, which stages the new oid over an
    old one HEAD still names). A HEAD-first read answers for the commit
    being REPLACED in that second case — `ls-tree HEAD` still finds the OLD
    160000 entry and returns it without ever consulting the index — which can
    falsely REJECT a fresh, correct re-pin (check 2 compares the staged
    checkout against the stale HEAD oid) or falsely label the source `main()`
    prints as "HEAD" when the true answer, mid-resync, is the index.

    A REMOVED OR TYPE-CHANGED GITLINK MUST ALSO NOT ANSWER FROM STALE HEAD
    DATA. `git rm --cached openXdox` or staging a regular file over the same
    path both make `git ls-files -s` stop reporting a `160000` entry for
    `submodule_path` — indistinguishable, at that call alone, from each
    other, but NEVER indistinguishable from "nothing has changed": either
    way, `_gitlink_from` on the index's own output no longer names the oid
    HEAD does, which is precisely the disagreement this function exists to
    prefer the index for. So the comparison is UNCONDITIONAL — `None` counts
    as an index answer like any other — and only a FAILED index read (an
    environment problem, not a staged one) falls back to HEAD without
    comparing at all.

    The index wins whenever a successful read of it disagrees with HEAD
    (new-and-staged, replaced-and-staged, or removed/type-changed-and-staged
    alike, in every case INCLUDING when that disagreement is "no gitlink at
    all"); only when the index agrees with HEAD — the ordinary clean tree —
    does HEAD's own oid answer, which is what keeps the success message's
    "read from HEAD" true for the common case instead of manufacturing a
    spurious "staged" label for bytes nothing has staged.

    Ported from `scripts/verify-opendox-pin.py`'s own `_recorded_gitlink`
    (PR #932 fix rounds `d4ac93a3` / `a3f1b8bc`), which carried this same
    HEAD-first gap until its own review caught it; this file carried the
    gap unnoticed — recorded owed on #932's landing note, `#656` comment
    `5628145815`.
    """
    head = _git(repo_root, "ls-tree", "HEAD", "--", submodule_path)
    head_oid = (_gitlink_from(head.stdout, submodule_path)
               if head.returncode == 0 else None)

    index = _git(repo_root, "ls-files", "-s", "--", submodule_path)
    if index.returncode == 0:
        index_oid = _gitlink_from(index.stdout, submodule_path)
        if index_oid != head_oid:
            return index_oid, "the index (staged, not yet committed)"

    if head_oid is not None:
        return head_oid, "HEAD"
    return None, "nowhere"


# --------------------------------------------------------------------------
# the digest
# --------------------------------------------------------------------------

def tree_digest(sub_root: Path, revision: str) -> str:
    """`sorted-ls-tree-r-v1` over `revision`'s whole tree, as the family defines it.

        records = `git ls-tree -r -z <commit>` split on NUL, empties dropped
        each record is `<mode> SP <type> SP <oid> TAB <path>`, path UNQUOTED
        sort the records bytewise ascending
        digest  = sha256(b"".join(record + b"\\n" for record in records))

    Byte-for-byte the definition `openXdox/contracts/code-pin.yaml` states in
    its own comment block and `scripts/repo_shape.py` implements upstream. It is
    re-implemented here rather than imported for one reason: `repo_shape.py`
    lives in `opensoft/openRepoShape`, which openxFactory pins
    (`contracts/openreposhape-pin.yaml`) but does NOT mount, so there is no
    checkout to import from at the moment this runs. The definition is
    reproduced in the comment above so the two spellings can be diffed by eye,
    which is the best available substitute for sharing one.

    THE EXPLICIT REVISION, NEVER `HEAD`. Check 3 has already proved the checkout
    is at `revision`, so the two are equal when this is reached — and naming the
    revision keeps the digest a statement about the commit the pin pins rather
    than about whatever is checked out, which is what makes this function safe
    to call from anywhere.

    `-z` is what makes the paths UNQUOTED: without it git quotes and escapes any
    path outside a narrow character set, and the digest would then be taken over
    an escaping scheme rather than over the tree.
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
# the checks
# --------------------------------------------------------------------------

def verify(root: Path = ROOT, pin: dict | None = None) -> dict:
    """Run the ordered checks against `root`; return the pin on success.

    Raises `PinRefusal` on the FIRST failure and never continues past it, on the
    wallet verifier's reasoning: the checks are ORDERED because each later one
    is only meaningful once the earlier ones hold. A digest recomputed against
    an uninitialized submodule reports an empty tree and buries the one fact
    that matters, and a digest recomputed against the WRONG revision reports
    drift when the actual defect is a stale checkout. First failure, named
    correctly, beats several failures that need triage.

    Prints nothing and exits nothing.
    """
    pin = load_pin() if pin is None else pin
    submodule_path = _submodule_path(pin)
    # The shape guards, ahead of every check that compares against them.
    commit = _pinned_commit(pin)
    recorded_digest = _pinned_tree_digest(pin)
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
            "openxdox-pin-submodule-uninitialized",
            f"{submodule_path}/.git does not exist: the submodule is not "
            f"initialized in {root}, so the openXdox tree this repository "
            "consumes is not present to be checked")

    # ---- check 2: the RECORDED gitlink equals `commit` ---------------------
    recorded, source = _recorded_gitlink(root, submodule_path)
    if recorded is None:
        raise PinRefusal(
            "openxdox-pin-gitlink-mismatch",
            f"{root} records no {GITLINK_MODE} gitlink for {submodule_path} in "
            "HEAD or in the index: the gitlink is recorded NOWHERE, so there is "
            f"nothing to compare against the pinned {commit}. A submodule "
            "present on disk but absent from the tree is not a pinned "
            "consumption")
    if recorded != commit:
        raise PinRefusal(
            "openxdox-pin-gitlink-mismatch",
            f"the gitlink {root} records for {submodule_path} (read from "
            f"{source}) is {recorded}, but the pin records {commit}; the tree "
            "and the pin disagree about which openXdox revision this repository "
            "consumes. RULED OQ-L makes the gitlink the commit pin itself, so "
            "the two are one invariant and move in ONE commit")

    # ---- check 3: the CHECKED-OUT revision equals `commit` -----------------
    # Distinct from check 2, and both are required, because only one comparison
    # catches each case — and because check 4 recomputes against the CHECKOUT,
    # so without this check a digest disagreement would be reported as content
    # drift when the real defect is that the wrong revision is on disk.
    head = _git(sub_root, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise PinRefusal(
            "openxdox-pin-checkout-mismatch",
            f"`git -C {sub_root} rev-parse HEAD` failed, so the checked-out "
            f"revision cannot be compared against the pinned {commit}: "
            f"{head.stderr.strip() or 'no error output'}")
    checked_out = head.stdout.strip().lower()
    if checked_out != commit:
        raise PinRefusal(
            "openxdox-pin-checkout-mismatch",
            f"{submodule_path} is checked out at {checked_out}, but the pin "
            f"records {commit}; the recorded gitlink agrees with the pin, so "
            "the tree is right and the working checkout is stale")

    # ---- check 4: the tree digest recomputes -------------------------------
    # THE WHOLE SURFACE IN ONE COMPARISON. There is no per-file loop because
    # there is no per-file list: one digest over every record in the tree
    # addresses every byte at `commit`, so a file added, removed, edited, or
    # having its mode changed all land here, and so does a nested leg gitlink
    # moving inside openXdox.
    actual = tree_digest(sub_root, commit)
    if actual != recorded_digest:
        raise PinRefusal(
            "openxdox-pin-digest-mismatch",
            f"{submodule_path}: TREE DIGEST DRIFT ({DIGEST_DEFINITION})\n"
            f"  recorded   {recorded_digest}\n"
            f"  recomputed {actual}\n"
            f"the bytes on disk are not the bytes the pin consumes at "
            f"openXdox@{commit[:12]}")

    return pin


# --------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Print one line and return 0, or print the refusal to stderr and return 2.

    Every failure path returns 2; see the module docstring for why there is no
    exit 1.
    """
    parser = argparse.ArgumentParser(
        prog="verify-openxdox-pin.py",
        description=("Verify contracts/openxdox-pin.yaml against the openXdox "
                     "gitlink, checkout and tree digest. Offline."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args(argv)

    try:
        pin = verify()
    except PinRefusal as exc:
        print(str(exc), file=sys.stderr)
        return 2

    # Re-resolved here rather than returned from `verify()`, which is contracted
    # to return the pin and to print nothing: the source of the recorded gitlink
    # is a fact about the RUN and belongs in the run's output, and one extra
    # `ls-tree` is cheaper than widening a return type other code depends on.
    _, source = _recorded_gitlink(ROOT, _submodule_path(pin))
    commit = _pinned_commit(pin)
    print(f"OK openxdox-pin verified: openXdox@{commit}, gitlink read from "
          f"{source}, {DIGEST_DEFINITION} tree digest recomputed "
          f"({_pinned_tree_digest(pin)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
