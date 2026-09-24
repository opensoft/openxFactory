"""The house reader and row-level judge for the ESTATE REPOSITORY INVENTORY
(release-realization / add-estate-repository-inventory).

WHY THIS MODULE EXISTS. `gate-code-surface-declarations` landed a grammar for
`code_surface:` and stated its own bound in the ratified text: "The gate SHALL
judge the identifier's SHAPE and SHALL NOT judge its MEMBERSHIP of any
inventory, for the measured reason that this repository defines no inventory of
the estate's repositories to resolve against." Its `tasks.md` § 6.1 named the
successor and refused to build it. `scripts/estate-repository-inventory.yaml` is
that inventory and this module is its reader: with it, a plausible misspelling
stops passing the gate on the strength of its shape.

THE INVENTORY RECORDS AN ADMISSION AND PERFORMS NONE. A repository joins the
estate when a GOVERNED TREE NAMES IT; the row is the record of that naming act,
and `admitted_by:` names the site and the kind, so a row is CHECKABLE against
the tree rather than asserted. This module does that checking for the four
kinds whose evidence lives in THIS repository's working tree, and supplies the
CARRIER-IDENTITY CHECK the fifth kind's separately invoked mode needs.

THE RE-CHECK IS BOUNDED BY WHERE THE EVIDENCE LIVES, and the bound is what makes
"deterministic, no network" a statement this module can keep. FOUR kinds name
evidence inside this checkout — `pin` a file under `contracts/`, `workflow` a
file under `.github/workflows/`, `change` a directory under `openspec/changes/`,
and `root` a constant naming no file at all — so `evidence_verdicts` re-checks
them on EVERY run. `gitlink` is the ONE kind whose evidence lives in ANOTHER
repository's tree, which an openxFactory checkout does not contain, so a row
carrying one is `NOT_RECHECKED` here and is re-checked only by
`scripts/validate-estate-inventory.py --estate-tree <repo>=<path>`, against a
tree the CALLER already has. A SILENCE IS NEVER A PASS: a run that has not
looked reports neither "named" nor "stale".

A PATH IS AN ASSERTION AND NOT AN IDENTITY, which is why `carrier_identity`
exists and why the mode above may not simply trust the path it was handed. A
caller may pass a typo'd path, a stale worktree, or a checkout of a DIFFERENT
repository that merely sits where the carrier was expected, and an unverified
path would let one repository's `.gitmodules` discharge — or condemn — another
repository's row, which is the same defect as resolving a name by asking the
provider, arriving by a different door. **Ruled by Brett Heap, 2026-09-18,
verbatim "Bind the carrier identity"**: the supplied tree is verified against
its OWN ORIGIN URL, or against the carrier's record in
`contracts/policies/repository-identity.yaml`, before its `.gitmodules` is
trusted — those being the two places this estate already states a repository's
identity, both already in the caller's hand or in this checkout. It RETURNS
verified/unverified and NEVER RAISES, so a tree that does not verify leaves the
row reported NOT RE-CHECKED rather than failing the run.

AND THE ORIGIN URL'S HOST IS PART OF THAT IDENTITY, WHICH IS A DESIGN NOTE THIS
MODULE OWES RATHER THAN A DETAIL. The ruling says a tree is verified "by the
tree's own ORIGIN URL"; a normalization that kept the `<owner>/<name>` PATH and
discarded the HOST would verify `git@attacker.example:opensoft/xFactory.git` as
this estate's aggregation, which is the same substitution the ruling refuses,
one field to the left. `contracts/policies/repository-identity.yaml` — the one
place the estate writes a repository's identity down — records an
`<owner>/<repo>` ADDRESS and carries NO HOST FIELD AT ALL, so it cannot supply
the bound, and the estate's own measured spellings are used instead: GitHub's
canonical ssh and https forms, which is every `url =` in the aggregation's
`.gitmodules` and every origin this repository is cloned from. `FORGE_HOSTS`
holds them, with that reasoning beside it, and a second forge is a one-line
addition there. A URL on any other host yields NO OBSERVED IDENTITY, so the
tree is UNVERIFIED and the row NOT RE-CHECKED — never verified against a
stranger. WHETHER THE TRANSFER MAP SHOULD CARRY THE HOST is a question about
that contract member and is not taken here.

A PINNED ASSEMBLY ROOT CARRIES A `gitlink` TOO, BUT ONLY AS FAR AS openxFactory's
OWN PIN REACHES (`admit-code-leg-under-pinned-root`, openxFactory #1150, shape
(a) ruled by Brett Heap 2026-09-24). The governed carrier is unchanged; beside
it a `pinned` row admitted by EXACTLY ONE `pin` may carry, because there the act
of admission is openxFactory's pin — a file under `contracts/` fixing the root at
one commit and one whole-tree digest — and the root's gitlink is the site that
pin reaches. `load_inventory` refuses every other carrier BY NAME
(`_pinned_carrier_refusal`): an `external` one, a `pinned` one no pin admits or
several do, and a row a pinned root itself admits, so the reach ends ONE HOP
from an openxFactory pin; and a row a pinned root admits may not declare
`governance: governed`. THE BINDING TO THE PINNED COMMIT IS WHAT MAKES THAT
SOUND. `pinned_commit` reads the commit from the carrier's one pin in THIS
checkout, and `gitmodules_addresses_at` reads the root's `.gitmodules` AS OF
THAT COMMIT out of the supplied tree's own object store — never its working
files, never another revision — so what decides membership is the tree
openxFactory chose to consume, and a root's own main line moving changes nothing
until openxFactory re-pins. AND THAT READ REFUSES EVERY TRANSPORT: an
object-store read in a partial clone would otherwise fetch a missing blob from
its promisor remote (that change's `design.md` D0.6), so every `git` this
module runs is given a protocol allow-list naming none, and a tree that cannot
answer locally leaves the row NOT RE-CHECKED rather than fetched.
`carrier_members` puts the two reads together for a verified tree, and reads a
governed carrier from its working tree exactly as before.

RESOLUTION IS BY THE ROW AND NEVER BY THE PROVIDER. An `<owner>/<name>` head
resolves against a row's address; a BARE head resolves against a row's unique
bare name; a FORMER address resolves through the transfer map. None of the three
asks GitHub, because a gate whose verdict depends on a network call gives a
different answer on a bad afternoon than it gave at the ratification, and
because the redirect that would answer it is the grace period the transfer map
exists to refuse.

THE COMPARISON IS CASE-SENSITIVE, and that is the transfer map's own rule rather
than a strictness invented here: `field_rules.current` says the estate compares
the owner segment CASE-SENSITIVELY "even where the provider compares
case-insensitively", and each row's `owner_case` names the spellings that
resolve at the provider and are NOT this estate's spelling. A case-insensitive
resolver would admit exactly those.

A PENDING TRANSFER ROW IS NOT A RESOLUTION INSTRUCTION, and this module obeys
that rather than discovering it. `contracts/policies/repository-identity.yaml`'s
own `pending_row_rule` says a reader MUST NOT resolve `former` -> `current` for
any LIVE reference while the row is `pending`, because at that point `former` is
still the only address that exists. So `load_transfers` returns the COMPLETE
rows and drops the pending ones, and a pending row therefore neither resolves a
head nor verifies a supplied tree.

THE INVENTORY IS READ THROUGH THE HOUSE STRICT LOADER
(`frontmatter_strict.strict_load`) rather than through a private scan, so this
reader and every other reader in the estate refuse the same documents and no
inventory can mean one thing to one reader and another to the next. There is NO
SECOND PARSER here.

NOTHING AUTHOR-CONTROLLED BECOMES A PATH BEFORE IT IS SHAPE-CHECKED. A `change`
admission's change id must match `CHANGE_ID_RE` before `load_inventory` returns
it and a `pin` or `workflow` admission's path must be a REPOSITORY-RELATIVE path
under the directory its kind names, because every consumer resolves them under
the scanned tree; and no path this module opens is reached through a symlink, at
the leaf or at any ancestor (`load_inventory`, `_has_symlinked_ancestor`,
`_unescaped`).

Deterministic: text/YAML reads and local git reads only, no model calls, no
writes, no network.
"""

from __future__ import annotations

import datetime
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import frontmatter_strict as fm
import yaml

#: The inventory, beside the validator that reads it — the placement
#: `design.md` D2 measured and Brett Heap's bare word took.
INVENTORY_PATH = Path(__file__).resolve().parent / "estate-repository-inventory.yaml"

#: THE ESTATE'S TRANSFER MAP, repository-relative. The ONE place a FORMER
#: address is read, and never a provider redirect.
TRANSFER_MAP = Path("contracts") / "policies" / "repository-identity.yaml"

CHANGES_DIR = Path("openspec") / "changes"
ARCHIVE_DIR = CHANGES_DIR / "archive"

#: THE AGGREGATION REPOSITORY, WHICH IS THE ONE ROW `root` MAY ADMIT. The kind's
#: whole definition is "the aggregation repository ITSELF, which no
#: `.gitmodules` can name because a superproject is not its own submodule, and
#: which would otherwise be the one member of the estate no evidence admits" —
#: a statement about ONE repository, named at `design.md` D0.2 row 1. Left
#: unbound, `root` is the kind that admits ANYTHING: it names no file, so
#: `evidence_verdicts` marks it NAMED unconditionally, and a row that wrote
#: `kind: root` would walk into the estate carrying evidence nobody can look at.
#: Every other kind points at something checkable; this one is checkable only by
#: being pinned to the single address it means.
AGGREGATION_ROOT = "opensoft/xFactory"

#: THE THREE GOVERNANCE CLASSES, closed. `governed` the estate authors its
#: contents; `pinned` openxFactory consumes it at a commit and digest and
#: authors none of it; `external` it is pinned and is NOT of this estate at all.
#: Enumerated HERE, beside the loader that enforces them, rather than only in a
#: test over the inventory this repository happens to carry: a constraint the
#: requirement states and no loader checks is a constraint a consuming tree does
#: not have.
GOVERNANCE_CLASSES = ("governed", "pinned", "external")

#: THE FIVE ADMISSION-EVIDENCE KINDS, closed, "because they are exactly the ways
#: this estate has ever named a repository" (the requirement's own words).
GITLINK, PIN, WORKFLOW, ROOT, CHANGE = (
    "gitlink", "pin", "workflow", "root", "change")
ADMISSION_KINDS = (GITLINK, PIN, WORKFLOW, ROOT, CHANGE)

#: THE FOUR KINDS WHOSE EVIDENCE IS IN THIS CHECKOUT, and so the four this
#: module re-checks on every run. `gitlink` is deliberately absent.
IN_TREE_KINDS = (PIN, WORKFLOW, ROOT, CHANGE)

#: WHERE EACH PATH-BEARING KIND'S EVIDENCE MAY LIVE. The requirement names the
#: directory for each ("`pin` a file under `contracts/`, `workflow` a file under
#: `.github/workflows/`"), so the constraint is enforced at the load rather than
#: trusted at the use — a `pin` whose path pointed into `.github/` would be an
#: admission of a kind the row does not declare.
_KIND_ROOTS = {
    PIN: Path("contracts"),
    WORKFLOW: Path(".github") / "workflows",
}

#: A CHANGE ID IS A DIRECTORY NAME AND NEVER A PATH, the sibling readers' rule
#: restated: one segment, no separator, no leading dot, so neither `..` nor
#: `a/b` can be written into the inventory and reach a path.
CHANGE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

#: AN `<owner>/<name>` ADDRESS, spelled as `code_surface.REPOSITORY_RE` spells
#: an identifier, with the owner segment REQUIRED. The inventory carries
#: addresses and never bare names in `repository:`, because a bare name in the
#: address column is exactly the ambiguity the unique-bare-name rule exists to
#: refuse.
_NAME = r"[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]"
ADDRESS_RE = re.compile(rf"^{_NAME}/{_NAME}$")
NAME_RE = re.compile(rf"^{_NAME}$")

#: THE FORGE HOSTS THIS ESTATE'S REPOSITORIES LIVE AT, and the reason the host
#: is part of the identity rather than a prefix to be discarded. The ruling is
#: "Bind the carrier identity" and its own words are that a supplied tree is
#: verified "by the tree's own ORIGIN URL"; a normalization that kept the
#: `<owner>/<name>` PATH and threw the HOST away would verify
#: `git@attacker.example:opensoft/xFactory.git` as this estate's aggregation and
#: let a tree nobody in this estate wrote discharge — or condemn — a row, which
#: is the very substitution the ruling exists to refuse, arriving one field to
#: the left.
#:
#: WHY THIS LIST AND NOT THE TRANSFER MAP'S. `contracts/policies/repository-identity.yaml`
#: records an identity as an `<owner>/<repo>` ADDRESS and carries NO host field
#: at all (`field_rules.former`, `field_rules.current`), so it cannot supply the
#: bound and a reader that waited for it would wait forever. The estate's own
#: spellings are measured instead: every `url =` in the aggregation's
#: `.gitmodules` and every origin this repository is cloned from is
#: `git@github.com:`, so GitHub's canonical ssh and https forms are what is
#: accepted and every other host yields NO OBSERVED IDENTITY — the tree is
#: UNVERIFIED and the row NOT RE-CHECKED, never verified against a stranger.
#: A second forge is a one-line addition HERE, where the reason is written down.
FORGE_HOSTS = ("github.com",)

_HOSTS = "|".join(re.escape(host) for host in FORGE_HOSTS)

#: THE ORIGIN URL SPELLINGS A WORKING TREE MAY CARRY, normalized past the
#: `git@`/`https://` forms and the `.git` suffix, which is `design.md` D1.2's
#: own description of what the verification reads — AND PAST NOTHING ELSE. The
#: host is MATCHED, not skipped, and the repository half is REQUIRED (an
#: `owner/` with no name is not an address and no longer reaches the caller as
#: one). Nothing else is accepted: a URL this does not match yields no observed
#: identity, and the tree is UNVERIFIED rather than guessed at.
_ORIGIN_RE = re.compile(
    rf"^(?:git@(?:{_HOSTS}):"
    rf"|ssh://(?:[^@/]+@)?(?:{_HOSTS})(?::\d+)?/"
    rf"|https?://(?:[^@/]+@)?(?:{_HOSTS})(?::\d+)?/)"
    rf"({_NAME}/{_NAME})(?:\.git)?/?$")

#: THE AMBIENT GIT ENVIRONMENT THE CARRIER READ REFUSES TO INHERIT, and THE
#: ESTATE'S OWN LIST rather than a second one — `scripts/carved_reach.py`,
#: `scripts/hermes_runtime_validation/content.py` and
#: `scripts/report-citation-remainder.py` carried the identical tuple as of
#: this reader's own round 2. None of the three exposes it as an importable
#: helper, so it is restated here with its citation rather than reached for
#: through a private name.
#:
#: `GIT_CONFIG` IS THE ONE ENTRY THAT MADE THE THREE DIVERGE FROM THIS FILE,
#: and the divergence is recorded rather than silently left for the next
#: reader to notice. MEASURED, NOT ASSUMED: on the git this branch tests
#: against, an ambient `GIT_CONFIG` naming a file that rewrites
#: `remote.origin.url` does not reach either call `_git` makes (`remote
#: get-url` and `rev-parse` read the ordinary config stack; `GIT_CONFIG`
#: redirects only `git config`'s OWN default file, a narrower, undecorated
#: variable from `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` above, which this
#: reader does force). It is scrubbed anyway: a caller controls its own
#: environment, a future call this reader adds may run `git config`, and
#: relying on a non-effect that is one git version's behavior and not a
#: documented contract is not a binding. The three siblings do not yet carry
#: this line — whoever next touches one of them owes either the same entry or
#: a recorded reason it does not apply there.
#:
#: WHY IT MATTERS HERE MORE THAN ANYWHERE: this read IS the carrier binding.
#: `GIT_DIR`, `GIT_COMMON_DIR` and `GIT_WORK_TREE` MOVE THE REPOSITORY OUT FROM
#: UNDER `-C`, which is not a theory — measured on this branch, a checkout of
#: `opensoft/Innocent` read under an ambient `GIT_DIR` pointing at another
#: repository answers with THAT repository's origin, so the tree verifies as a
#: carrier it is not. A caller controls its own environment and CI is an
#: environment; a binding that a variable can flip is not a binding. The rest of
#: the list is scrubbed on the estate's standing ground rather than on a fresh
#: demonstration for each: the object store and the index a git read resolves
#: through are not this reader's to inherit either.
_SCRUBBED_GIT_ENVIRONMENT = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_CONFIG",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS",
    "GIT_DIR",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_REPLACE_REF_BASE",
    "GIT_WORK_TREE",
)

_INDEXED_GIT_CONFIG_ENVIRONMENT = re.compile(r"GIT_CONFIG_(?:KEY|VALUE)_[0-9]+")

#: A `.gitmodules` `url =` LINE'S REPOSITORY. The same normalization, applied to
#: the submodule URLs a carrier's `.gitmodules` carries.
_GITMODULES_URL_RE = re.compile(r"^\s*url\s*=\s*(\S+)\s*$")

#: A COMMIT A PIN MAY NAME FOR A PINNED CARRIER TO BE READ AT, AND AN OBJECT ID
#: THE READ WILL FOLLOW: exactly 40 hex, case-insensitive and lowercased before
#: use — the shape `scripts/verify-opendox-pin.py::COMMIT_RE` accepts and
#: nothing looser. An abbreviated oid, a branch or a tag names no revision this
#: reader may read at without resolving a movable name, which is a network
#: question, and the one answer it has for that is NOT RE-CHECKED. Applied with
#: `fullmatch`, because `$` also matches before a trailing newline.
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")

#: THE PROTOCOL ALLOW-LIST EVERY `git` THIS MODULE RUNS IS GIVEN: one naming NO
#: transport. A set `GIT_ALLOW_PROTOCOL` IS the whole allow-list — git consults
#: no `protocol.*.allow` config beside it — so a list naming none refuses every
#: transport even where the repository's own config allows them all, and a
#: lazy fetch from a partial clone's promisor remote FAILS instead of reaching
#: the network. MEASURED on the Ubuntu `1:2.43.0-1ubuntu7.3` build of git
#: (`admit-code-leg-under-pinned-root`'s `design.md` D0.6, and again on this
#: branch): `fatal: transport 'file' not allowed`, exit 128, and the blob still
#: absent after, on a clone whose own config allows every transport as on one
#: that does not. `none` names no transport git carries and no remote helper
#: this estate installs. THIS IS THE GUARD RELIED ON.
#:
#: `GIT_NO_LAZY_FETCH=1` RIDES BESIDE IT AND IS A BUILD-DEPENDENT EXTRA, NOT THE
#: GUARD. On that same build it ALSO refuses the fetch (`warning: lazy fetching
#: disabled`, exit 128, the blob still absent), but whether a git honours it
#: depends on the build — one that predates the variable ignores it — so
#: nothing here rests on it, and the tests prove the allow-list holds ALONE,
#: with `GIT_NO_LAZY_FETCH` removed.
_NO_TRANSPORT = "none"

#: THE MODES A COMMIT'S `.gitmodules` ENTRY MAY CARRY TO BE READ: a regular file.
#: A SYMLINK (`120000`) is refused, as `gitmodules_addresses` refuses a symlinked
#: working-tree `.gitmodules` — its blob is a link target and not the carrier's
#: submodule list — and so is a gitlink or a tree standing at that path.
_GITMODULES_MODES = ("100644", "100755")

# --- the per-admission verdicts ----------------------------------------------
#
# NAMED and GONE are the two answers a run that HAS LOOKED may give. NOT
# RECHECKED is the third and is neither of them: the requirement forbids passing
# a `gitlink` row silently, forbids failing it, and forbids fetching the tree,
# so a run that has not looked — or has looked in the wrong tree — reports
# exactly this and counts it.
NAMED = "named"
GONE = "gone"
NOT_RECHECKED = "not-rechecked"


class EstateInventoryError(Exception):
    """A refusal this module raises: an inventory that cannot be used. Carries
    the message naming what was refused.

    IT IS RAISED FOR THE FILE AND NEVER FOR A TREE. A row whose evidence has
    gone, a supplied tree that does not verify and a head that names nothing are
    all REPORTED through the verdicts below, because each is a fact about the
    estate that a caller must be able to print; only an inventory that cannot be
    READ stops a run.
    """


@dataclass(frozen=True)
class Admission:
    """ONE naming act a row records, and the site it took place at.

    Exactly one site field is populated, and which one is fixed by `kind`:
    `carrier` for a `gitlink` (THE REPOSITORY THAT CARRIES IT — "a reader being
    unable to look in a tree the row does not name"), `path` for a `pin` or a
    `workflow`, `change` for a `change`, and none at all for `root`, which names
    no file because a superproject is not its own submodule.
    """
    kind: str
    carrier: str | None = None
    path: str | None = None
    change: str | None = None

    def site(self) -> str:
        """The site as a finding names it."""
        if self.kind == GITLINK:
            return f"a gitlink in {self.carrier}"
        if self.kind in (PIN, WORKFLOW):
            return f"{self.kind} {self.path}"
        if self.kind == CHANGE:
            return f"the ratified change {self.change}"
        return "the aggregation root itself"


@dataclass(frozen=True)
class Row:
    """ONE repository of the estate, as the inventory records it.

    `position` is the row's 1-based place in the file, carried so a refusal can
    NAME BOTH ROWS of a bare-name collision rather than describing one of them.
    """
    repository: str
    name: str
    role: str
    governance: str
    admitted_by: tuple[Admission, ...]
    provisional: bool
    position: int


@dataclass(frozen=True)
class Inventory:
    """The whole file, indexed for the two spellings the corpus writes."""
    rows: tuple[Row, ...]
    path: Path

    @property
    def by_address(self) -> dict[str, Row]:
        return {row.repository: row for row in self.rows}

    @property
    def by_name(self) -> dict[str, Row]:
        return {row.name: row for row in self.rows}


#: HOW AN IDENTIFIER RESOLVED, carried rather than inferred from the answer.
#: `FORMER` is the one that is not a plain hit: the identifier is INTERPRETABLE
#: and membership is not in doubt, so the caller REPORTS and does not refuse
#: (`design.md` D5), and it needs to know which of the three happened to say so.
BY_ADDRESS = "address"
BY_NAME = "bare name"
BY_FORMER = "former address"


@dataclass(frozen=True)
class Resolution:
    """What the inventory says about one declared identifier.

    `row` is None when nothing carries it, which is the FAIL-CLOSED case: the
    whole content of the membership arm is the difference between a name that
    resolves and a name that merely looks like one.
    """
    identifier: str
    row: Row | None
    how: str | None = None
    #: The CURRENT address a former spelling resolves to, so a finding can name
    #: it and the author need not look it up.
    current: str | None = None

    @property
    def resolved(self) -> bool:
        return self.row is not None


@dataclass(frozen=True)
class EvidenceVerdict:
    """One admission, re-checked (or deliberately not)."""
    row: Row
    admission: Admission
    verdict: str
    detail: str


@dataclass(frozen=True)
class CarrierCheck:
    """Whether a supplied working tree really is the carrier a row names.

    NEVER RAISED, ALWAYS RETURNED. A tree that cannot be read, a path that is
    not a repository, a `git` that is not installed and an origin URL in a
    spelling this estate does not write all land here as `verified=False` with
    `observed` naming what was actually found — because the one verdict this arm
    has for a tree it could not confirm is NOT RE-CHECKED, and a raise would
    turn a caller's typo into a failed run.
    """
    verified: bool
    carrier: str
    #: The identity the tree asserts, normalized, or None when none was read.
    observed: str | None
    detail: str


@dataclass(frozen=True)
class PinnedCommit:
    """The ONE revision a PINNED carrier's evidence is read at, or why there is
    none. NEVER RAISED, ALWAYS RETURNED (`pinned_commit`).

    A pin that names no commit leaves the row NOT RE-CHECKED rather than failed
    (the scenario *A pinned root's gitlink is re-checked at its pinned commit*),
    so the one thing a caller needs back is the commit or the sentence saying
    why there is none, and a raise would turn a pin written by tag into a
    stopped run.
    """
    #: The carrier row's one `pin` admission's path, as the row records it, or
    #: None when the row carries no single pin to read from.
    pin: str | None
    #: Exactly 40 hex, lowercased, or None when the pin names no commit.
    commit: str | None
    detail: str


@dataclass(frozen=True)
class CarrierMembers:
    """What a supplied tree that VERIFIED as its carrier says that carrier
    carries, and WHERE it was read (`carrier_members`). NEVER RAISED.

    `addresses` None is NOT an absence: it is a run that could not read the
    evidence, which the requirement reports NOT RE-CHECKED, counted and neither
    passed nor failed. An EMPTY tuple is an answer — the carrier's
    `.gitmodules`, where it was read, names no submodule at all.
    """
    carrier: str
    addresses: tuple[str, ...] | None
    #: The evidence's site as a finding names it: "its `.gitmodules`" for a
    #: governed carrier's working tree, and the pinned commit and its pin for a
    #: pinned one.
    where: str
    #: The pinned commit read at, for a pinned carrier whose pin names one.
    commit: str | None = None
    #: The pin that commit is read from, for a pinned carrier.
    pin: str | None = None
    #: Why `addresses` is None; empty when it is not.
    detail: str = ""


# --- the containment guards, mirrored and not approximated ---------------------


def _has_symlinked_ancestor(path: Path) -> bool:
    """Whether any directory between `path` and its own top is a symlink.

    `path.is_symlink()` answers only for the LEAF. `linkdir/inventory.yaml`,
    where `linkdir` is a symlink to an external directory, has an entirely
    ORDINARY leaf — the file itself is a regular file — so the leaf check alone
    passes it, and `read_text()` still follows `linkdir` and reads bytes from
    wherever it points, silently and differently per runner.

    THE WALK IS UNANCHORED, AND THAT IS `code_surface._has_symlinked_ancestor`'S
    EXACT SHAPE rather than an approximation of it: an inventory named on
    `--inventory` is deliberately allowed to live wherever a test tree or a
    consuming repository puts it, so there is no root to check "outside of" the
    way `_unescaped` checks outside one.
    """
    current = path.parent
    while True:
        if current.is_symlink():
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def _unescaped(repo_root: Path, relative: Path) -> Path | None:
    """`repo_root / relative`, but ONLY when it is a REAL, UNESCAPED path under
    `repo_root` — no symlink ANYWHERE between the two, not only at the leaf —
    and `None` otherwise.

    `Path.is_file()` FOLLOWS SYMLINKS, so a committed `contracts/<pin>.yaml`
    symlink — or an ordinary file inside a symlinked `contracts/` — would
    otherwise be read as this tree's own admission evidence, and a row would be
    discharged by bytes that live outside the tree being judged. A dangling link
    is the same defect wearing the other face: the evidence vanishes and the row
    reads as stale on a fact about the link rather than about the estate.
    NEITHER is a judgment about the scanned tree, which is the only thing this
    reader is entitled to make.

    The leaf's own `is_symlink()` does not settle it: a REGULAR file reached
    through a symlinked parent is not itself a symlink. So the test is: resolve
    everything, and require that you land where a symlink-free tree would have
    put you — which closes the escape at every component in ONE comparison.

    THE FAILURES THIS GUARD ABSORBS ARE THE INTERPRETER'S, NOT THE SET ITS
    AUTHOR NAMED. `Path.resolve(strict=True)` reports a missing or unreadable
    component as an `OSError` and a SYMLINK LOOP as a `RuntimeError`, which is a
    subclass of NEITHER `OSError` NOR `ValueError`: a clause naming only
    `OSError` is open at exactly the loop, and hands the caller an exception
    where this prose promised an answer. A loop may stand at the candidate's
    LEAF or at ANY PARENT COMPONENT of it, the scanned root included, and the
    answer is the same in every position, because `repo_root / relative`
    traverses the loop itself. (openxFactory #1074;
    `harden-path-escape-helpers-against-symlink-loops` § 3.1 —
    `code_surface._unescaped` is the exact shape this mirrors.)
    """
    candidate = repo_root / relative
    try:
        resolved = candidate.resolve(strict=True)
        resolved_root = repo_root.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if resolved != resolved_root / relative:
        return None
    return candidate


# --- the transfer map ---------------------------------------------------------


def load_transfers(repo_root: Path) -> tuple[dict[str, str], tuple[str, ...]]:
    """`{former address: current address}` for the COMPLETE transfers only, and
    the MALFORMED rows this pass refused rather than silently dropping.

    THE PENDING ROWS ARE DROPPED AND THAT IS THE MAP'S OWN INSTRUCTION, not a
    strictness invented here. `pending_row_rule` reads: "A row whose
    `transfer_state` is `pending` DECLARES a ruled identity change that HAS NOT
    HAPPENED. … A reader MUST NOT resolve `former` -> `current` for any LIVE
    reference while the row is `pending` — at that point `former` is still the
    only address that exists." Every use this module makes of the map is a live
    reference: a head being resolved now, a row being judged now, a working tree
    being verified now.

    A ROW CLAIMING `transfer_state: complete` IS HELD TO THE POLICY'S OWN SHAPE
    BEFORE IT BECOMES A RESOLUTION, and not to its two most convenient fields
    alone. `field_rules.transfer_state` states the one MUST this file's own
    header carries: "The two fields move together and a reader MUST treat any
    disagreement between them as a malformed row" — `transferred_on` a real
    date once `transfer_state` is `complete`, `null` while it is `pending`. A
    first cut of this reader checked only `transfer_state == "complete"` and
    never looked at `transferred_on` at all, so a row edited to add
    `transfer_state: complete` — with `transferred_on` left `null`, or absent,
    or any non-date value — resolved as an authoritative identity change on the
    strength of two string fields, bypassing the membership arm's fail-closed
    path on an edit this policy's own text already calls malformed.
    `former`/`current` are held to the same `<owner>/<name>` shape every other
    address in this module is, for the same reason: a value that is not that
    shape is not a resolvable identity, however trustworthy the row otherwise
    reads. A row that looks like an attempted transfer (`former`/`current` both
    strings) but fails this shape is REFUSED and reported rather than silently
    dropped alongside the ordinary, lawful `pending` rows — the failure mode
    Copilot's review named is exactly a malformed row treated as if it had
    passed, so this pass tells the two apart and names which one a row was.

    AN ABSENT OR UNREADABLE MAP IS AN EMPTY ONE AND NOT A REFUSAL. The map is a
    contract member this packet READS and does not own; a tree that carries no
    transfers has taken none, and a reader that refused to run without it would
    make every consuming tree carry a file to say nothing. What is lost is the
    former-address REPORT, which is a report and never an authorization — so the
    failure mode is a finding not raised, never a head wrongly admitted.
    """
    path = _unescaped(repo_root, TRANSFER_MAP)
    if path is None or not path.is_file():
        return {}, ()
    try:
        raw = path.read_text(encoding="utf-8")
        doc = fm.strict_load(raw, what=str(TRANSFER_MAP))
    except (OSError, UnicodeDecodeError, fm.StrictFrontMatterError):
        return {}, ()
    except ValueError as exc:
        # PyYAML's own timestamp constructor raises bare `ValueError` — not
        # `yaml.YAMLError` — on a scalar that LOOKS like a date but names a
        # day the calendar does not have (`2026-02-30`: "day is out of range
        # for month"). That is readable-but-malformed CONTENT, not an
        # unreadable file, so unlike the three guards above it is a finding
        # and not a silent empty map: the file exists and was meant to say
        # something, and this pass could not tell what. The parse fails
        # before any row is reached, so the whole file — not one row — is
        # what gets refused and reported.
        return {}, (f"{TRANSFER_MAP} could not be parsed: {exc}",)
    if not isinstance(doc, dict):
        return {}, ()
    transfers = doc.get("transfers")
    if not isinstance(transfers, list):
        return {}, ()
    resolved: dict[str, str] = {}
    resolved_at: dict[str, int] = {}
    malformed: list[str] = []
    duplicate_former = False
    for position, entry in enumerate(transfers, start=1):
        if not isinstance(entry, dict):
            continue
        former, current = entry.get("former"), entry.get("current")
        if not isinstance(former, str) or not isinstance(current, str):
            continue  # not shaped like an attempted transfer at all
        site = f"{TRANSFER_MAP} row {position} ({former} -> {current})"
        state = entry.get("transfer_state")
        transferred_on = entry.get("transferred_on")
        if state not in ("pending", "complete"):
            malformed.append(
                f"{site} declares `transfer_state: {state!r}`, which is "
                "neither `pending` nor `complete`; refused rather than "
                "resolved")
            continue
        if state == "pending":
            if transferred_on is not None:
                malformed.append(
                    f"{site} declares `transfer_state: pending` and a "
                    f"non-null `transferred_on` ({transferred_on!r}); the two "
                    "fields disagree, which `field_rules.transfer_state` "
                    "calls malformed, so the row is refused rather than "
                    "resolved")
            continue  # pending_row_rule: not a resolution instruction either way
        # state == "complete"
        if type(transferred_on) is not datetime.date:
            # `isinstance` alone is not enough: `datetime.datetime` SUBCLASSES
            # `datetime.date`, so a timestamp (a date WITH a time-of-day
            # component — never what a bare `YYYY-MM-DD` scalar parses to)
            # would pass an `isinstance` check here and resolve as if it were
            # the plain date `field_rules.transfer_state` requires.
            malformed.append(
                f"{site} declares `transfer_state: complete` but "
                f"`transferred_on` is {transferred_on!r} "
                f"({type(transferred_on).__name__}), not a plain date; the "
                "two fields disagree, which `field_rules.transfer_state` "
                "calls malformed, so the row is refused rather than "
                "resolved")
            continue
        if ADDRESS_RE.match(former) is None or ADDRESS_RE.match(current) is None:
            malformed.append(
                f"{site} — at least one of `former`/`current` is not an "
                "`<owner>/<name>` address; refused rather than resolved")
            continue
        if former in resolved_at:
            # Two COMPLETE rows naming the same `former` is not one malformed
            # row — each row can be individually well-shaped — it is the map
            # disagreeing with itself about where one address went, which is
            # worse than a single bad row: it is silent ambiguity about which
            # resolution is authoritative. A first cut let the second row
            # overwrite the first in `resolved` with no finding at all. This
            # pass names both rows and refuses the WHOLE FILE'S resolution
            # (not merely the duplicate pair), because a map caught
            # contradicting itself once cannot be trusted for any OTHER
            # `former` it also names.
            duplicate_former = True
            malformed.append(
                f"{site} declares `former: {former}`, which {TRANSFER_MAP} "
                f"row {resolved_at[former]} also declares `transfer_state: "
                "complete` for; two complete rows naming the same `former` "
                "address is refused for the whole file rather than resolved "
                "by whichever row this loop reached last")
            continue
        resolved[former] = current
        resolved_at[former] = position
    if duplicate_former:
        return {}, tuple(malformed)
    return resolved, tuple(malformed)


# --- the inventory ------------------------------------------------------------


def _admission(entry: object, row_index: int, position: int) -> Admission:
    """One `admitted_by:` element, shape-checked.

    THE SITE IS REQUIRED AND ITS FIELD IS FIXED BY THE KIND. "the evidence SHALL
    NAME THE REPOSITORY THAT CARRIES IT" is the requirement's own sentence about
    a `gitlink`, and it is enforced here rather than trusted, because a `gitlink`
    with no carrier is an admission no reader can check — which is precisely the
    state the whole kind was widened to escape.
    """
    where = f"row {position} admission {row_index}"
    if not isinstance(entry, dict):
        raise EstateInventoryError(f"{where} is not a mapping")
    kind = entry.get("kind")
    if kind not in ADMISSION_KINDS:
        raise EstateInventoryError(
            f"{where} declares `kind: {kind!r}`, which is not one of "
            f"{', '.join(ADMISSION_KINDS)}; the kinds are CLOSED because they "
            "are exactly the ways this estate has named a repository, and a "
            "new kind is a change to the specification rather than an "
            "inventory edit")
    extra = set(entry) - {"kind", "carrier", "path", "change"}
    if extra:
        raise EstateInventoryError(
            f"{where} carries unknown key(s) {', '.join(sorted(extra))}")

    def _required(field: str) -> str:
        value = entry.get(field)
        if not isinstance(value, str) or not value.strip():
            raise EstateInventoryError(
                f"{where} is a `{kind}` and is missing a non-empty `{field}:`; "
                "an admission whose site is unnamed is an admission no reader "
                "can check against the tree")
        return value

    def _forbidden(*fields: str) -> None:
        for field in fields:
            if entry.get(field) is not None:
                raise EstateInventoryError(
                    f"{where} is a `{kind}` and carries `{field}:`, which "
                    f"belongs to another kind's site")

    if kind == GITLINK:
        carrier = _required("carrier")
        _forbidden("path", "change")
        if not ADDRESS_RE.match(carrier):
            raise EstateInventoryError(
                f"{where} names `carrier: {carrier}`, which is not an "
                "`<owner>/<name>` address; the carrier is a REPOSITORY and a "
                "reader must be able to look in the tree the row names")
        return Admission(kind=GITLINK, carrier=carrier)
    if kind in (PIN, WORKFLOW):
        raw_path = _required("path")
        _forbidden("carrier", "change")
        candidate = Path(raw_path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise EstateInventoryError(
                f"{where} names `path: {raw_path}`, which is not a plain "
                "repository-relative path; the path is resolved under the "
                "scanned tree, so an absolute path or a `..` segment written "
                "here would reach outside it")
        root = _KIND_ROOTS[kind]
        if root not in candidate.parents:
            raise EstateInventoryError(
                f"{where} is a `{kind}` naming `path: {raw_path}`, which is "
                f"not under `{root}/`; the requirement names the directory for "
                "each kind, so an admission filed under another kind's "
                "directory is an admission of a kind the row does not declare")
        return Admission(kind=kind, path=raw_path)
    if kind == CHANGE:
        change = _required("change")
        _forbidden("carrier", "path")
        if not CHANGE_ID_RE.match(change):
            raise EstateInventoryError(
                f"{where} names `change: {change}`, which is not a "
                "change-directory name — one segment, no separator and no "
                "leading dot; the name is resolved under openspec/changes/, so "
                "a path written here would reach one")
        return Admission(kind=CHANGE, change=change)
    _forbidden("carrier", "path", "change")
    return Admission(kind=ROOT)


def load_inventory(path: Path = INVENTORY_PATH) -> Inventory:
    """The inventory, shape-checked, or a refusal naming the defect.

    AN INVENTORY THAT CANNOT BE USED REFUSES RATHER THAN BEING IGNORED: ignoring
    a malformed enumeration would make every declared identifier resolve against
    nothing, and the membership arm FAILS CLOSED, so an ignored file would red
    every declaration in the corpus while reading as an inventory problem
    nobody named.

    NO PATH IS REACHED THROUGH A SYMLINK, AT THE LEAF OR AT ANY ANCESTOR, and
    the check runs UNCONDITIONALLY before `is_file()` or `read_text()` — so it
    is the same guard whether `path` is the default argument or one a caller
    supplies, and no branch can forget one of them. `Path.is_file()` and
    `Path.read_text()` BOTH follow symlinks, so without this a committed link
    here would make the gate consume membership data from OUTSIDE the checkout,
    silently and differently per runner. This is `code_surface.load_register`'s
    guard mirrored exactly rather than approximated: a guard that is NEARLY the
    sibling's is a guard whose gaps nobody has measured.

    THE BARE-NAME COLLISION IS REFUSED HERE AND NOT REPORTED LATER, because the
    requirement forbids resolving the ambiguous spelling at all: "the validator
    SHALL REFUSE THE INVENTORY rather than pick a row, because picking is how an
    authorization lands in the wrong repository." A reader that returned the
    index and let a caller decide would have already picked.
    """
    if path.is_symlink() or _has_symlinked_ancestor(path):
        raise EstateInventoryError(
            f"the inventory {path} is reached through a symlink, refused "
            "unread rather than followed: a committed symlink here — at the "
            "inventory's own name, or at any directory between it and the top "
            "— would let the gate resolve membership against bytes from "
            "outside the checkout and vary by runner. Replace it with a "
            "regular file at an ordinary, unsymlinked path")
    if not path.is_file():
        raise EstateInventoryError(f"the inventory {path} does not exist")
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise EstateInventoryError(
            f"the inventory {path} cannot be read: {exc}") from exc
    try:
        doc = fm.strict_load(raw, what=f"the inventory {path.name}")
    except fm.StrictFrontMatterError as exc:
        raise EstateInventoryError(
            f"the inventory {path.name} is refused: {exc}") from exc
    if not isinstance(doc, dict):
        raise EstateInventoryError(
            f"the inventory {path.name} must be a mapping")
    if doc.get("schema_version") != 1:
        raise EstateInventoryError(
            f"the inventory {path.name} must carry `schema_version: 1`; every "
            "governed YAML in this repository carries `schema_version` and "
            "`kind`, and a reader that skipped the check would read a future "
            "shape as this one")
    if doc.get("kind") != "estate-repository-inventory":
        raise EstateInventoryError(
            f"the inventory {path.name} must carry "
            "`kind: estate-repository-inventory`")
    entries = doc.get("repositories")
    if not isinstance(entries, list) or not entries:
        raise EstateInventoryError(
            f"the inventory {path.name} must carry a non-empty top-level "
            "`repositories:` list")

    rows: list[Row] = []
    for position, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise EstateInventoryError(f"row {position} is not a mapping")
        extra = set(entry) - {"repository", "name", "role", "governance",
                              "admitted_by", "provisional"}
        if extra:
            raise EstateInventoryError(
                f"row {position} carries unknown key(s) "
                f"{', '.join(sorted(extra))}")
        for field in ("repository", "name", "role", "governance"):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                raise EstateInventoryError(
                    f"row {position} ({entry.get('repository')!r}) is missing "
                    f"a non-empty `{field}:`")
        repository = entry["repository"]
        name = entry["name"]
        if not ADDRESS_RE.match(repository):
            raise EstateInventoryError(
                f"row {position} names `repository: {repository}`, which is "
                "not an `<owner>/<name>` address; the inventory carries "
                "ADDRESSES, a bare name in this column being exactly the "
                "ambiguity the unique-bare-name rule refuses")
        if not NAME_RE.match(name):
            raise EstateInventoryError(
                f"row {position} ({repository}) names `name: {name}`, which is "
                "not a bare repository name")
        segment = repository.split("/")[-1]
        if name != segment:
            raise EstateInventoryError(
                f"row {position} names `repository: {repository}` and "
                f"`name: {name}`, which is not that address's final segment "
                f"(`{segment}`). THE BARE NAME IS THE ADDRESS'S OWN LAST "
                "SEGMENT AND NOT A SECOND, FREELY CHOSEN LABEL: a row free to "
                f"name itself anything could make the bare head `{name}` "
                f"authorize `{repository}` while the bare head `{segment}` — "
                "the spelling the corpus actually writes, and the one a reader "
                "checking the address would predict — resolved to nothing at "
                "all. The requirement's two columns are one repository written "
                "two ways, so they are held to agree here rather than trusted "
                "to")
        if entry["governance"] not in GOVERNANCE_CLASSES:
            raise EstateInventoryError(
                f"row {position} ({repository}) declares "
                f"`governance: {entry['governance']}`, which is not one of "
                f"{', '.join(GOVERNANCE_CLASSES)}; the classes are kept "
                "distinct because a consumer that collapsed them would "
                "authorize a change to a repository nobody here may change")
        admitted = entry.get("admitted_by")
        if not isinstance(admitted, list) or not admitted:
            raise EstateInventoryError(
                f"row {position} ({repository}) is missing a non-empty "
                "`admitted_by:` list; the inventory RECORDS an admission taken "
                "elsewhere and performs none, so a row that names no naming "
                "site records nothing")
        admissions = tuple(
            _admission(item, index, position)
            for index, item in enumerate(admitted, start=1))
        provisional = entry.get("provisional", False)
        if not isinstance(provisional, bool):
            raise EstateInventoryError(
                f"row {position} ({repository}) declares "
                f"`provisional: {provisional!r}`, which is not a boolean")
        has_change = any(a.kind == CHANGE for a in admissions)
        if provisional and not has_change:
            raise EstateInventoryError(
                f"row {position} ({repository}) is marked `provisional: true` "
                "but is admitted by no `change`; PROVISIONAL is what a "
                "`change` admission IS, so a row provisional on nothing "
                "records a state no naming act put it in")
        if has_change and not provisional:
            raise EstateInventoryError(
                f"row {position} ({repository}) is admitted by a `change` and "
                "does not say `provisional: true`; the requirement is that "
                "such a row IS provisional and SHALL SAY SO, because what "
                "expires at that change's archive is exactly this admission")
        rows.append(Row(
            repository=repository,
            name=name,
            role=entry["role"],
            governance=entry["governance"],
            admitted_by=admissions,
            provisional=provisional,
            position=position,
        ))

    seen_addresses: dict[str, Row] = {}
    seen_names: dict[str, Row] = {}
    for row in rows:
        clash = seen_addresses.get(row.repository)
        if clash is not None:
            raise EstateInventoryError(
                f"rows {clash.position} and {row.position} both name "
                f"`{row.repository}`; one row per repository, so a stale row "
                "cannot hide behind a live twin")
        seen_addresses[row.repository] = row
        clash = seen_names.get(row.name)
        if clash is not None:
            raise EstateInventoryError(
                f"rows {clash.position} ({clash.repository}) and "
                f"{row.position} ({row.repository}) share the bare name "
                f"`{row.name}`; bare names SHALL BE UNIQUE across the "
                "inventory, and the inventory is REFUSED rather than a row "
                "picked, because picking is how an authorization lands in the "
                "wrong repository")
        seen_names[row.name] = row

    # THE CARRIER AND THE ROOT ARE BOUND HERE, AFTER EVERY ADDRESS IS KNOWN,
    # because both are statements ABOUT THE INVENTORY and neither can be settled
    # while one row is being read in isolation.
    for row in rows:
        for admission in row.admitted_by:
            if admission.kind == ROOT:
                if row.repository != AGGREGATION_ROOT:
                    # `root` NAMES NO FILE, so it is the one kind whose evidence
                    # cannot be looked at — `evidence_verdicts` marks it NAMED
                    # unconditionally and correctly, the aggregation being real and
                    # unsubmodulable. Unbound, that makes it the estate's open door:
                    # write `kind: root` on any address and the row is admitted by
                    # evidence no run can contradict. It means the ONE repository
                    # the requirement says it means.
                    raise EstateInventoryError(
                        f"row {row.position} ({row.repository}) declares "
                        f"`kind: root`, which admits `{AGGREGATION_ROOT}` and no "
                        "other repository. `root` is the kind that NAMES NO FILE — "
                        "it is the aggregation repository itself, which no "
                        "`.gitmodules` can name because a superproject is not its "
                        "own submodule — so it is the one admission no run can "
                        "ever contradict, and a row that could claim it would "
                        "enter the estate on evidence nobody is able to look at. "
                        "Record this row's real naming act instead")
                if row.governance != "governed":
                    # `root` NAMES NO FILE EITHER, so nothing downstream looks
                    # at a tree to re-check this admission: `evidence_verdicts`
                    # marks a `root` admission NAMED unconditionally, and the
                    # membership arm (`scripts/validate-code-surface.py`)
                    # refuses only `governance: external`, waving a `pinned`
                    # row through unrefused. `root` denotes the aggregation
                    # ITSELF, which this estate authors directly rather than
                    # pins or stands outside of, so the row it names SHALL
                    # declare `governance: governed` — anything else would let
                    # a code surface name the aggregation as a repository this
                    # estate does not author, authorized by the one admission
                    # no run can ever contradict.
                    raise EstateInventoryError(
                        f"row {row.position} ({row.repository}) declares "
                        f"`kind: root` and `governance: {row.governance}`. "
                        "`root` denotes the aggregation repository itself, "
                        "which this estate authors directly rather than pins "
                        "or stands outside of, so the row it names SHALL "
                        "declare `governance: governed`. Change this row's "
                        "`governance:`, or its `admitted_by:` if `root` does "
                        "not belong on it")
                continue
            if admission.kind == PIN and row.governance == "governed":
                # THE KIND'S SECOND CLAUSE, AND THE ONE THE POST-PASS DID NOT
                # CHECK: "an openxFactory file under `contracts/` names the
                # repository as the source of a commit-and-digest pin … for a
                # product PINNED rather than governed" (the promoted spec's own
                # words). Every OTHER `pin`-admitted row in this estate is
                # `pinned` or `external` — never `governed` — and row 3
                # (`codeXfactory/codexFactory`) carried exactly this mismatch
                # until Brett Heap ruled it out, verbatim "Drop the pin
                # admission on row 3": `governed` and `pin`-admitted at once.
                # Unchecked, a malformed inventory could reintroduce that same
                # shape on any governed row, and the membership arm would
                # accept it — it refuses only `governance: external`, so a
                # `governed` row that also happened to declare a `pin` would
                # resolve and pass membership on a kind that was never lawful
                # evidence for it.
                raise EstateInventoryError(
                    f"row {row.position} ({row.repository}) declares "
                    f"`governance: governed` and is admitted by a `pin` "
                    f"({admission.path}). `pin` is openxFactory's act "
                    "\"for a product PINNED rather than governed\" — a "
                    "`governed` row is one this estate authors directly, so "
                    "its own tree is the estate's act of admission and a "
                    "`contracts/` pin is never that row's evidence. Drop the "
                    "`pin` admission, or change this row's `governance:` if "
                    "it is not actually governed")
            if admission.kind != GITLINK:
                continue
            assert admission.carrier is not None
            carrier_row = seen_addresses.get(admission.carrier)
            if carrier_row is None:
                raise EstateInventoryError(
                    f"row {row.position} ({row.repository}) is admitted by a "
                    f"gitlink in `{admission.carrier}`, which THIS INVENTORY "
                    "CARRIES NO ROW FOR. The kind's carrier is a GOVERNED "
                    "ESTATE REPOSITORY, or a PINNED ROOT openxFactory pins, so "
                    "the carrier is itself a member of the estate and the "
                    "inventory is where the estate's members are written down; "
                    "a carrier no row names is a tree this file cannot say the "
                    "estate has, and a re-check pointed at it would discharge "
                    "one row on the word of a repository nothing admits. Add "
                    "the carrier's own row, or record the naming act that "
                    "really happened")
            if carrier_row.governance == "governed":
                continue  # the estate's own act of admission: the wide case
            refusal = _pinned_carrier_refusal(row, carrier_row,
                                              seen_addresses)
            if refusal is not None:
                raise EstateInventoryError(refusal)

    return Inventory(rows=tuple(rows), path=path)


def _pinned_carrier_refusal(row: Row, carrier_row: Row,
                            by_address: dict[str, Row]) -> str | None:
    """Why `row`'s `gitlink` in the NON-GOVERNED `carrier_row` is refused, or
    None when the carrier is a lawful PINNED ROOT and `row` a lawful row of it.

    THE KIND'S SECOND CARRIER, AND EXACTLY AS FAR AS IT REACHES. "A PINNED
    ASSEMBLY ROOT's `.gitmodules` IS A CARRIER TOO, read AT THE COMMIT
    openxFactory's own `pin` of that root names: there the act of admission is
    openxFactory's pin, and the root's gitlink is the site that pin reaches"
    (`admit-code-leg-under-pinned-root`'s `## MODIFIED` block). The loader's
    old sentence — "Reading their submodule lists as admissions would let a
    tree nobody here writes decide who is in the estate" — is ANSWERED rather
    than overridden: the tree that decides is the one openxFactory CHOSE to
    consume, at the one commit its pin fixes (that change's `design.md` D2).
    Every clause below is the narrowest that keeps that true (the same
    design's D3 and D4), and each refusal names the row, the carrier and the
    condition, as the scenario *A gitlink names a carrier outside the two
    lawful forms* requires:

    - `external`: "An `external` repository's `.gitmodules` SHALL admit
      nothing, whatever openxFactory pins of it."
    - ONE HOP: "a row a pinned root's gitlink admits MUST NOT itself carry a
      further row's gitlink". CHECKED DIRECTLY and FIRST, and not left to the
      pin count below: a leg is ordinarily a `pinned` row no pin admits, which
      the count refuses too, but the MUST is over EVERY row a pinned root
      admits — a leg that also carried a pin of its own would pass the count.
    - EXACTLY ONE `pin`: "the commit that pin names is the one revision the
      evidence is read at, and two pins of one root would make that revision a
      pick." No pin names no revision at all.
    - THE CLASS BOUND: "A row admitted by a pinned root's `gitlink` SHALL NOT
      declare `governance: governed`" — the `pin` kind's own bound, above,
      restated for the site a pin reaches.
    """
    carrier = carrier_row.repository
    where = (f"row {row.position} ({row.repository}) is admitted by a gitlink "
             f"in `{carrier}`, whose own row {carrier_row.position}")
    if carrier_row.governance == "external":
        return (
            f"{where} declares `governance: external`. AN `external` "
            "REPOSITORY'S `.gitmodules` ADMITS NOTHING, whatever openxFactory "
            "pins of it: an `external` repository is not of this estate at "
            "all, so it performs no act of admission when its `.gitmodules` "
            "happens to name something, and reading its submodule list as one "
            "would let a tree nobody here writes decide who is in the estate. "
            "A `gitlink` carrier is a `governed` row, or a `pinned` assembly "
            "root openxFactory pins exactly once")
    # `pinned`, the one class left: `GOVERNANCE_CLASSES` is closed at the load.
    roots = sorted(
        admission.carrier for admission in carrier_row.admitted_by
        if admission.kind == GITLINK and admission.carrier is not None
        and admission.carrier in by_address
        and by_address[admission.carrier].governance == "pinned")
    if roots:
        return (
            f"{where} is itself admitted by a gitlink in the pinned root "
            f"`{roots[0]}`. THE REACH ENDS ONE HOP FROM AN openxFactory PIN: "
            "a row a pinned root's gitlink admits carries no further row's "
            "gitlink, because openxFactory reaches it only through its pin of "
            "that root, and following the chain would rest membership on a "
            "walk of trees no openxFactory file names")
    pins = [admission.path for admission in carrier_row.admitted_by
            if admission.kind == PIN and admission.path is not None]
    if not pins:
        return (
            f"{where} declares `governance: pinned` and is admitted by NO "
            "`pin`. A PINNED ROOT CARRIES A `gitlink` ONLY AS FAR AS "
            "openxFactory's OWN PIN REACHES: the commit that pin names is the "
            "one revision the root's `.gitmodules` is read at, and a `pinned` "
            "row no openxFactory pin fixes names no revision at all, so its "
            "submodule list would decide membership at whatever its tree "
            "happens to hold. Record the pin that admits it, or the naming act "
            "that really happened")
    if len(pins) > 1:
        return (
            f"{where} declares `governance: pinned` and is admitted by "
            f"{len(pins)} `pin`s ({', '.join(pins)}). A PINNED ROOT'S "
            "`.gitmodules` IS READ AT THE COMMIT ITS ONE `pin` NAMES: with "
            f"{len(pins)}, which commit the evidence is read at would be a "
            "pick, and picking is how an authorization lands in the wrong "
            "repository")
    if row.governance == "governed":
        return (
            f"row {row.position} ({row.repository}) is admitted by a gitlink "
            f"in the pinned root `{carrier}` (row {carrier_row.position}) and "
            "declares `governance: governed`. A ROW A PINNED ROOT'S GITLINK "
            "ADMITS SHALL NOT DECLARE `governance: governed`: openxFactory "
            "reaches it only through its pin of the root, at the commit that "
            "pin fixes, and authors none of it, which is what a `pin`-admitted "
            "row is too — and a `governed` row admitted by a `pin` is refused "
            "at this same load. Declare `pinned`, or `external` for a "
            "repository this estate does not author")
    return None


# --- resolution ---------------------------------------------------------------


def resolve(inventory: Inventory, identifier: str,
            transfers: dict[str, str] | None = None) -> Resolution:
    """What the inventory says about one declared identifier.

    THREE SPELLINGS RESOLVE AND NO FOURTH. An `<owner>/<name>` ADDRESS against a
    row's address; a BARE NAME against a row's unique bare name; and a FORMER
    ADDRESS through the transfer map to a current row — which REPORTS rather
    than refuses, the identifier being interpretable and the estate's membership
    not in doubt. NOTHING IS RESOLVED BY ASKING THE PROVIDER.

    THE FORMER LOOKUP IS TRIED LAST, after both live spellings have missed, so
    a map row can never shadow a live one: an address the inventory carries
    resolves as itself even if some map row also names it as a former spelling
    of something else.
    """
    transfers = transfers if transfers is not None else {}
    row = inventory.by_address.get(identifier)
    if row is not None:
        return Resolution(identifier=identifier, row=row, how=BY_ADDRESS)
    row = inventory.by_name.get(identifier)
    if row is not None:
        return Resolution(identifier=identifier, row=row, how=BY_NAME)
    current = transfers.get(identifier)
    if current is not None:
        row = inventory.by_address.get(current)
        if row is not None:
            return Resolution(identifier=identifier, row=row, how=BY_FORMER,
                              current=current)
    return Resolution(identifier=identifier, row=None)


def former_address_rows(inventory: Inventory,
                        transfers: dict[str, str]) -> tuple[tuple[Row, str], ...]:
    """`(row, current address)` for every row written at a FORMER address.

    The inventory carries CURRENT addresses only, so a row the transfer map
    records as former is a finding whose remedy is a respelling — and the
    finding names the current address so nobody has to look it up.
    """
    return tuple((row, transfers[row.repository]) for row in inventory.rows
                 if row.repository in transfers)


# --- the in-tree re-check -----------------------------------------------------


#: THE PIN KIND'S BARE-ADDRESS STRUCTURAL FIELDS, and no third of this shape.
#: Every `kind: pinned_contract_manifest` pin this estate writes
#: (`contracts/openxwallet-pin.yaml`, `opendox-pin.yaml`, `openxdox-pin.yaml`,
#: `openreposhape-pin.yaml`, `openspec-cli-pin.yaml`) states its source as
#: `source_repository:`; the one `kind: pinned_workflow` pin
#: (`contracts/review-lane-pin.yaml`) states it as `repository:`. Both are
#: TOP-LEVEL keys read off the parsed document, carrying the bare
#: `<owner>/<name>` address itself — never a value nested under another
#: mapping. `source_url:` is the estate's other lawful site (present
#: alongside `source_repository:` in `openreposhape-pin.yaml` and
#: `openspec-cli-pin.yaml`, and the ONLY site the review-round fixture for
#: this check carries): a full URL rather than a bare address, so it is
#: normalized through `normalize_origin` — the same reading a working tree's
#: own origin gets — rather than compared as a literal.
_PIN_REPOSITORY_FIELDS = ("repository", "source_repository")


def _pin_names_repository(document: object, repository: str) -> bool:
    """Whether a PARSED pin document's own structural field names `repository`.

    NOTHING ELSE IN THE FILE IS ASKED. A first cut of this check matched the
    ADDRESS anywhere in the file's TEXT (bounded so a substring of a longer
    address would not match) and that still let PROSE discharge an admission:
    `contracts/openspec-cli-pin.yaml`'s own `source_repository:` is
    `Fission-AI/OpenSpec`, and its header commentary names
    `codeXfactory/codexFactory` more than a dozen times documenting THAT
    repository's own use of the pinned CLI — a row admitted by this file for
    `codeXfactory/codexFactory` would have reported NAMED on a comment, never
    on the file's own claim about its source. See `_PIN_REPOSITORY_FIELDS`
    for the two bare-address fields and `source_url:` for the URL one.
    """
    if not isinstance(document, dict):
        return False
    for field in _PIN_REPOSITORY_FIELDS:
        value = document.get(field)
        if isinstance(value, str) and value == repository:
            return True
    source_url = document.get("source_url")
    if isinstance(source_url, str) and normalize_origin(source_url) == repository:
        return True
    return False


def _uses_repository(uses: str) -> str | None:
    """The `<owner>/<name>` a workflow step's `uses:` value names, or None.

    `uses:` is `<owner>/<name>[/<path-to-a-reusable-workflow>][@<ref>]` for a
    reusable workflow or a marketplace action. `@<ref>` is stripped first — it
    is a git ref and no part of an address — and the first TWO `/`-separated
    segments are the address; a local action (`./…`) or a Docker reference
    (`docker://…`) yields fewer than two non-empty segments and correctly
    names nothing here.
    """
    address = uses.split("@", 1)[0]
    segments = address.split("/")
    if len(segments) < 2 or not segments[0] or not segments[1]:
        return None
    return f"{segments[0]}/{segments[1]}"


def _workflow_names_repository(document: object, repository: str) -> bool:
    """Whether a PARSED workflow document's own structural sites name
    `repository`.

    THREE SITES, and no fourth. A step's `uses:` (a reusable workflow or
    action pinned AT this repository) and a step's `with.repository:` (an
    `actions/checkout`-shaped input naming which repository to check out —
    `.github/workflows/merge-master-approval.yml`'s own site for row 3's
    admission) are the two a step carries. THE THIRD IS AT THE JOB ITSELF:
    `jobs.<job_id>.uses` is how GitHub Actions calls a REUSABLE WORKFLOW at
    job granularity rather than inside a step — a job written this way has NO
    `steps:` at all (the called workflow's own steps run in its place), so a
    reader that only ever looked inside `steps[*]` would report a workflow
    admission GONE for a job written in exactly this shape, on a file whose
    structural `uses:` names the repository plainly. Every OTHER string in the
    document — a comment, a `run:` script line, an `echo`, an `::error::`
    message — is prose ABOUT the repository and not the workflow's own claim
    to dispatch into it, and is not consulted; `merge-master-approval.yml`
    names `codeXfactory/codexFactory` in exactly that prose form more than a
    dozen times beside its one (step-level) structural site.
    """
    if not isinstance(document, dict):
        return False
    jobs = document.get("jobs")
    if not isinstance(jobs, dict):
        return False
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        job_uses = job.get("uses")
        if isinstance(job_uses, str) and _uses_repository(job_uses) == repository:
            return True
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if isinstance(uses, str) and _uses_repository(uses) == repository:
                return True
            with_block = step.get("with")
            if isinstance(with_block, dict) \
                    and with_block.get("repository") == repository:
                return True
    return False


def _names_repository(path: Path, repository: str, kind: str) -> bool:
    """Whether the evidence file at `path` really names `repository`.

    PRESENCE OF THE FILE IS NOT PRESENCE OF THE EVIDENCE. A `pin` or `workflow`
    whose file stopped naming the repository — repointed at another source, or
    reduced to a template — is a row whose admission has gone as surely as a
    deleted file, and a check that asked only `is_file()` would report it as
    named.

    THE FILE'S OWN STRUCTURE IS CONSULTED, AND NOTHING ELSE — never a substring
    match over the whole text, which a comment or a `run:` line can satisfy on
    a repository the file never claims to be evidence for (`_pin_names_repository`,
    `_workflow_names_repository` carry the measured cases). The file is parsed
    ONCE, through the same refused-construct loader the inventory itself reads
    through (`frontmatter_strict.StrictLoader`) so no anchor, alias or merge key
    can make one authorized value stand in for another here either. A `pin`'s
    document goes through `strict_load` and its byte ceiling, sized for a
    front-matter document and everything this estate's five pins fit inside; a
    `workflow`'s does not — this estate's own workflow files run well past that
    ceiling on their documentation prose alone (`merge-master-approval.yml`
    alone is over 115KB), a size the ceiling was never sized to refuse, so the
    same loader is used directly without it. A file that does not parse, or is
    not evidence any more than a missing one is, returns False rather than
    raising — this function's contract, like the reader around it, is that a
    row's evidence check NEVER RAISES.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    try:
        if kind == PIN:
            document = fm.strict_load(text, what=str(path))
        else:
            document = yaml.load(text, Loader=fm.StrictLoader)
    except (fm.StrictFrontMatterError, yaml.YAMLError):
        return False
    if kind == PIN:
        return _pin_names_repository(document, repository)
    if kind == WORKFLOW:
        return _workflow_names_repository(document, repository)
    return False


def evidence_verdicts(inventory: Inventory,
                      repo_root: Path) -> tuple[EvidenceVerdict, ...]:
    """Every admission of every row, re-checked where the evidence is in reach.

    THE FOUR IN-TREE KINDS ARE JUDGED ON EVERY RUN, deterministically and with
    no network call, the evidence being a file in the tree this reader is
    already reading. `gitlink` is `NOT_RECHECKED` here without exception — not
    passed, not failed — because its evidence lives in a tree this checkout does
    not contain; `scripts/validate-estate-inventory.py` re-checks it against a
    working tree a caller supplies and that VERIFIES as the carrier.

    A `change` ADMISSION IS JUDGED IN THREE STATES AND NOT TWO. Present and
    ACTIVE is `NAMED`. Present under `openspec/changes/archive/` is `GONE`, and
    the detail says which of the two remedies is owed, because the requirement
    reaches both: a row still admitted ONLY by an archived change is a row whose
    provisional admission outlived the act that justified it, and a row whose
    other kinds now name it owes the DROP of this admission and of
    `provisional:`. Absent altogether is `GONE` on the plain ground that the
    tree does not carry what the row names.
    """
    verdicts: list[EvidenceVerdict] = []
    for row in inventory.rows:
        for admission in row.admitted_by:
            if admission.kind == GITLINK:
                verdicts.append(EvidenceVerdict(
                    row, admission, NOT_RECHECKED,
                    f"the `.gitmodules` of {admission.carrier} is not in this "
                    "checkout; supply that working tree with "
                    f"`--estate-tree {admission.carrier}=<path>` to re-check "
                    "this row"))
                continue
            if admission.kind == ROOT:
                verdicts.append(EvidenceVerdict(
                    row, admission, NAMED,
                    "the aggregation repository itself, which no `.gitmodules` "
                    "can name because a superproject is not its own submodule"))
                continue
            if admission.kind in (PIN, WORKFLOW):
                assert admission.path is not None
                resolved = _unescaped(repo_root, Path(admission.path))
                if resolved is None or not resolved.is_file():
                    verdicts.append(EvidenceVerdict(
                        row, admission, GONE,
                        f"this tree carries no `{admission.path}`"))
                elif not _names_repository(resolved, row.repository,
                                          admission.kind):
                    verdicts.append(EvidenceVerdict(
                        row, admission, GONE,
                        f"`{admission.path}` is in this tree but no longer "
                        f"names `{row.repository}`"))
                else:
                    verdicts.append(EvidenceVerdict(
                        row, admission, NAMED,
                        f"`{admission.path}` names `{row.repository}`"))
                continue
            assert admission.change is not None
            active = _unescaped(repo_root, CHANGES_DIR / admission.change)
            if active is not None and active.is_dir():
                ratified, observed = _is_ratified(repo_root, admission.change)
                if ratified:
                    verdicts.append(EvidenceVerdict(
                        row, admission, NAMED,
                        f"`{CHANGES_DIR / admission.change}` is an active "
                        "change and its proposal carries `Status: ratified`"))
                else:
                    verdicts.append(EvidenceVerdict(
                        row, admission, GONE,
                        f"`{CHANGES_DIR / admission.change}` is present but is "
                        f"{observed}, and the kind admits a RATIFIED change "
                        "alone — AN AUTHOR CANNOT ADMIT A REPOSITORY BY "
                        "DRAFTING ONE. A directory is not a ratification, so "
                        "this admission discharges nothing until that change "
                        "is ratified or another kind names the repository"))
                continue
            dated = re.compile(
                _ARCHIVED_AS.format(change=re.escape(admission.change)))
            archived = [child for child in _archive_children(repo_root)
                        if dated.fullmatch(child)]
            if archived:
                verdicts.append(EvidenceVerdict(
                    row, admission, GONE,
                    f"the change `{admission.change}` has ARCHIVED "
                    f"(`{ARCHIVE_DIR / archived[0]}`), so this PROVISIONAL "
                    "admission has outlived the act that justified it: either "
                    "another kind now names the repository and this admission "
                    "and `provisional:` are dropped with it, or nothing does "
                    "and the row is retired"))
            else:
                verdicts.append(EvidenceVerdict(
                    row, admission, GONE,
                    f"this tree carries no change `{admission.change}`, "
                    "active or archived"))
    return tuple(verdicts)


#: AN ARCHIVED PACKET'S DIRECTORY NAME, EXACTLY: the archive date and then the
#: change id, whole. A SUFFIX TEST IS NOT AN IDENTITY TEST — every id that ENDS
#: WITH another id ends with it, so `recreate-ledgerxwallet-overlay-boundary`
#: answers for `create-ledgerxwallet-overlay-boundary` and a live provisional
#: row is reported as having expired at an archive that was some other change's.
#: The separator is what makes the id's first character a boundary rather than a
#: coincidence, so it is required rather than assumed.
_ARCHIVED_AS = r"\d{{4}}-\d{{2}}-\d{{2}}-{change}"


def _archive_children(repo_root: Path) -> tuple[str, ...]:
    """The archived change-directory names, read through the same guard.

    An archived packet's directory is dated (`YYYY-MM-DD-<id>`), so the change
    id is the name's TAIL AFTER A DATED PREFIX rather than the name — which is
    why this returns the names rather than a set of ids somebody would have to
    re-derive, and why the caller matches `_ARCHIVED_AS` whole rather than
    testing a suffix.

    A SYMLINKED CHILD IS NOT AN ARCHIVED CHANGE. `Path.is_dir()` FOLLOWS
    SYMLINKS, so a link named `2026-09-18-<some live change>` and pointed at any
    directory at all would read here as that change having archived — a
    PROVISIONAL row reported as expired on the strength of a name somebody
    wrote, with the bytes it rests on living outside the tree being judged.
    That is the escape this module refuses everywhere else it opens a path
    (`_unescaped`, `load_inventory`), and the archive walk is not an exception
    to it: an entry is an archived change when it is a REAL DIRECTORY here.
    """
    archive = _unescaped(repo_root, ARCHIVE_DIR)
    if archive is None or not archive.is_dir():
        return ()
    try:
        children = list(archive.iterdir())
    except OSError:
        return ()
    return tuple(sorted(child.name for child in children
                        if not child.is_symlink() and child.is_dir()))


def _is_ratified(repo_root: Path, change: str) -> tuple[bool, str]:
    """Whether the active change `change` carries `Status: ratified`, and what
    it carries instead when it does not.

    THE KIND ADMITS A RATIFIED CHANGE AND NOT A DIRECTORY. `design.md` D1.1
    states the bound as the thing that keeps the fifth kind from being an escape
    hatch: "the evidence is a change id that must resolve under
    `openspec/changes/`, the change MUST BE RATIFIED (an author cannot admit a
    repository by drafting)". A re-check that asked only whether the directory
    exists would let any draft — one this lane wrote this morning — admit any
    repository to the estate, which is the ONE admission kind whose evidence an
    author controls completely.

    READ THROUGH THE SHIPPED STRICT LOADER AND NOT BY A SECOND PARSER.
    `frontmatter_strict.read_header_line` is the house reader for a lifecycle
    header line and applies the same window rule as `doc_health.corpus`'s own
    status reader, so this module and the checker cannot disagree about what a
    document's `Status:` is.

    AN UNREADABLE PROPOSAL IS NOT A RATIFICATION. Every failure — no
    `proposal.md`, a path reached through a symlink, bytes that are not UTF-8, a
    form the strict loader refuses, no `Status:` header at all — returns False
    with what was actually found, because the verdict this feeds REPORTS and
    never refuses the file, and an admission nobody can verify is an admission
    that discharges nothing.
    """
    proposal = _unescaped(repo_root, CHANGES_DIR / change / "proposal.md")
    if proposal is None or not proposal.is_file():
        return False, "carrying no readable `proposal.md`"
    try:
        value = fm.read_header_line(proposal, "Status")
    except (OSError, UnicodeDecodeError, fm.StrictFrontMatterError) as exc:
        return False, f"a proposal this reader cannot read ({exc})"
    if value is fm.NO_HEADER_LINE:
        return False, "a proposal carrying no `Status:` header at all"
    if not isinstance(value, str) or not value.strip():
        return False, "a proposal whose `Status:` header declares nothing"
    standing = value.strip().split()[0].strip().lower()
    if standing == "ratified":
        return True, value.strip()
    return False, f"`Status: {value.strip()}`"


# --- the carrier-identity check ----------------------------------------------


def normalize_origin(url: str) -> str | None:
    """`<owner>/<name>` for a git remote URL, or None for a spelling this estate
    does not write.

    NORMALIZED PAST THE `git@`/`https://` SPELLINGS AND THE `.git` SUFFIX, which
    is `design.md` D1.2's own description of the reading. A URL that does not
    match yields NONE rather than a guess: an unrecognized remote is a tree
    whose identity was not read, and the one verdict for that is NOT RE-CHECKED.
    """
    if not isinstance(url, str):
        return None
    match = _ORIGIN_RE.match(url.strip())
    if match is None:
        return None
    address = match.group(1)
    if address.endswith(".git"):
        address = address[: -len(".git")]
    return address if ADDRESS_RE.match(address) else None


def _sanitized_git_environment() -> dict[str, str]:
    """The environment every `git` this module runs is given.

    The scrub above, plus `GIT_NO_REPLACE_OBJECTS` beside the
    `--no-replace-objects` flag, because the two answer different halves: the
    flag covers the process this module starts and the variable covers any git
    that process starts for itself. The user's GLOBAL and SYSTEM config are not
    read either — nothing this module asks git for needs them, and an ambient
    `remote.origin.url` rewrite or `url.<base>.insteadOf` would otherwise reach
    the one read the carrier binding rests on.

    AND EVERY TRANSPORT IS REFUSED (`_NO_TRANSPORT`), because since
    `admit-code-leg-under-pinned-root` this module reads OBJECTS and not only
    config: `gitmodules_addresses_at` reads a pinned root's `.gitmodules` blob
    out of a supplied tree's object store, and in a partial clone that read
    would otherwise fetch a missing object from the promisor remote — the
    network call the requirement forbids ("THE READ SHALL MAKE NO NETWORK
    CALL"). The refusal is on for EVERY call and not for that read alone: a
    config read never needs a transport, and a guard that is always on cannot
    be left off the next call somebody adds. `GIT_NO_LAZY_FETCH` rides beside
    it for a git that honours it; the allow-list is what holds.
    """
    environment = {
        name: value for name, value in os.environ.items()
        if name not in _SCRUBBED_GIT_ENVIRONMENT
        and _INDEXED_GIT_CONFIG_ENVIRONMENT.fullmatch(name) is None
    }
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_CONFIG_SYSTEM"] = os.devnull
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    environment["GIT_ALLOW_PROTOCOL"] = _NO_TRANSPORT
    environment["GIT_NO_LAZY_FETCH"] = "1"
    return environment


def _git(tree: Path, *arguments: str) -> str | None:
    """`git -C tree …` in the sanitized environment, or `None` for any failure.

    NEVER RAISES, on `tree_origin`'s contract: the caller's one verdict for a
    tree it could not read is NOT RE-CHECKED. The 30-second bound is the
    estate's own number (`scripts/hermes_runtime_validation/content.py`,
    `scripts/report-citation-remainder.py`): a partial clone, a promisor remote
    or an unhealthy object store can make a read BLOCK rather than fail, and an
    unbounded one would hang a required check instead of reporting. With every
    transport refused (`_sanitized_git_environment`) a promisor fetch FAILS at
    once rather than blocking; the bound stays for the store that hangs anyway.
    """
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(tree), *arguments],
            capture_output=True, text=True, timeout=30, check=False,
            env=_sanitized_git_environment())
    except (OSError, ValueError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def tree_origin(tree: Path) -> str | None:
    """The identity a working tree asserts, from its OWN origin URL, or None.

    `git -C <path> remote get-url origin` is the reading `design.md` D1.2 names.
    It is a LOCAL CONFIG READ and reaches no network, which is what keeps this
    inside the bound D1 refused the derived shape for: a required check may not
    depend on a token or on read access to a private repository.

    THE READ IS TAKEN IN A SANITIZED ENVIRONMENT, because this read IS THE
    BINDING and an ambient variable would flip it. `GIT_DIR` (and
    `GIT_COMMON_DIR`, and `GIT_WORK_TREE`) move the repository out from under
    `-C`: measured on this branch, a checkout of `opensoft/Innocent` read with
    an ambient `GIT_DIR` pointing elsewhere answers with THAT repository's
    origin and verifies as a carrier it is not. See `_sanitized_git_environment`
    and `_git`.

    AND THE PATH MUST BE THE WORK-TREE ROOT ITSELF, which closes two shapes the
    origin read alone admits. A BARE REPOSITORY answers `remote get-url origin`
    perfectly well, so a bare repo with a planted `.gitmodules` beside its refs
    would discharge a row while being no checkout at all — and the mode's own
    ratified word is "a carrying repository's WORKING TREE". A SUBDIRECTORY of a
    real checkout answers too, because git discovers upward, and then
    `.gitmodules` is absent where the caller pointed and the row would be
    reported GONE — CONDEMNED on a caller's imprecise path, which is exactly the
    outcome `design.md` D1.2 retained and DECLINED ("it converts a caller's typo
    into a finding against the inventory"). `rev-parse --is-bare-repository
    --show-toplevel` answers both in one call, and the toplevel must resolve to
    the supplied path.

    EVERY FAILURE IS A `None` AND NEVER A RAISE — no `git` on the PATH, a path
    that is not a repository, a bare repository, a subdirectory of a checkout, a
    repository with no `origin`, a tree that cannot be read, a `git` that hangs
    past the timeout. The caller's one verdict for a tree it could not confirm
    is NOT RE-CHECKED, and a raise would turn a caller's typo into a failed run.
    """
    toplevel = _git(tree, "rev-parse", "--is-bare-repository",
                    "--show-toplevel")
    if toplevel is None:
        return None
    lines = toplevel.splitlines()
    if len(lines) != 2 or lines[0].strip() != "false":
        return None
    try:
        if Path(lines[1].strip()).resolve() != Path(tree).resolve():
            return None
    except (OSError, RuntimeError, ValueError):
        return None
    url = _git(tree, "remote", "get-url", "origin")
    if url is None:
        return None
    return normalize_origin(url.strip())


def carrier_identity(tree: Path, carrier: str,
                     transfers: dict[str, str] | None = None) -> CarrierCheck:
    """Whether `tree` is a checkout of `carrier`. NEVER RAISES.

    A PATH IS AN ASSERTION AND NOT AN IDENTITY. **Ruled by Brett Heap,
    2026-09-18, verbatim "Bind the carrier identity"**: a caller may pass a
    typo'd path, a stale worktree, or a checkout of a different repository that
    merely sits where the carrier was expected, and an unverified path would let
    one repository's `.gitmodules` discharge — or condemn — another repository's
    row.

    TWO SOURCES AND NO THIRD, because they are the two places this estate
    already states a repository's identity and both are already in the caller's
    hand or in this checkout: the tree's OWN ORIGIN URL, and the carrier's
    record in `contracts/policies/repository-identity.yaml`, so a carrier
    supplied at a FORMER address verifies through the map rather than being
    refused for a name the estate itself moved. No provider call is added and
    none is needed.

    A FAILED VERIFICATION IS NOT A FAILED ROW. The caller leaves the row NOT
    RE-CHECKED and COUNTED, with the rows no tree was supplied for, neither
    passed nor failed, and names the carrier the row expects and what the tree
    actually is. FAILING the row was retained and declined at `design.md` D1.2:
    it converts a caller's typo into a finding against the inventory, which
    teaches the wrong author the wrong thing, and it breaks the arm's own rule
    that a run which has not looked at the right tree reports neither verdict.
    """
    transfers = transfers if transfers is not None else {}
    observed = tree_origin(tree)
    if observed is None:
        return CarrierCheck(
            verified=False, carrier=carrier, observed=None,
            detail=f"no origin URL could be read from `{tree}` — it is not "
                   "the ROOT of a non-bare git working tree (a bare repository "
                   "and a subdirectory of a checkout are both refused here), "
                   "has no `origin` remote, or spells its remote in a form "
                   "this estate does not write")
    if observed == carrier:
        return CarrierCheck(
            verified=True, carrier=carrier, observed=observed,
            detail=f"`{tree}` is a checkout of {carrier} by its own origin URL")
    current = transfers.get(observed)
    if current == carrier:
        return CarrierCheck(
            verified=True, carrier=carrier, observed=observed,
            detail=f"`{tree}` asserts the FORMER address {observed}, which "
                   f"`{TRANSFER_MAP}` resolves to {carrier}")
    return CarrierCheck(
        verified=False, carrier=carrier, observed=observed,
        detail=f"`{tree}` is a checkout of {observed}, not of {carrier}")


def gitmodules_addresses(tree: Path) -> tuple[str, ...] | None:
    """The repositories a working tree's `.gitmodules` names, or None when it
    carries none that could be read.

    NO SECOND PARSER AND NO `git` INVOCATION: `.gitmodules` is a text file whose
    `url =` lines are what a submodule entry names, and the URL is normalized by
    exactly the function that normalizes an origin URL, so a carrier and its
    members are read by one spelling rule. A tree with no `.gitmodules` at all
    returns an EMPTY tuple, which is a real answer — the tree carries no
    submodules — and is distinct from the `None` a tree that could not be read
    returns.
    """
    relative = Path(".gitmodules")
    path = tree / relative
    try:
        path.lstat()
    except FileNotFoundError:
        return ()  # the tree carries no submodules: a real answer
    except (OSError, ValueError, RuntimeError):
        return None
    # NO PATH THIS MODULE OPENS IS REACHED THROUGH A SYMLINK, AND A SUPPLIED
    # TREE IS NOT AN EXCEPTION — it is the one tree whose bytes this repository
    # did not write. `Path.is_file()` and `Path.read_text()` BOTH follow links,
    # so a carrier presenting `.gitmodules` as a symlink would have the
    # validator discharge — or condemn — a row on bytes from wherever that link
    # points, which is the containment failure `_unescaped` exists to refuse and
    # `scripts/code_surface.py` refuses in the same shape. A DANGLING LINK LANDS
    # HERE TOO and is `None` rather than `()`: the file is present, its bytes
    # are not, and "the tree carries no submodules" would be a claim nobody
    # checked.
    if _unescaped(tree, relative) is None:
        return None
    try:
        if not path.is_file():
            return ()
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, RuntimeError):
        return None
    return _gitmodules_url_addresses(text)


def _gitmodules_url_addresses(text: str) -> tuple[str, ...]:
    """The repositories a `.gitmodules` TEXT names, in first-seen order.

    ONE PARSE FOR BOTH READS. A carrier's working-tree `.gitmodules`
    (`gitmodules_addresses`) and a pinned root's `.gitmodules` blob at its
    pinned commit (`gitmodules_addresses_at`) are read by this one function, so
    a leg's `https://` URL and a carrier's `git@` origin go through the same
    `_GITMODULES_URL_RE` and the same `normalize_origin`, and the two reads
    cannot come to disagree about what one line of the file names.
    """
    found: list[str] = []
    for line in text.splitlines():
        match = _GITMODULES_URL_RE.match(line)
        if match is None:
            continue
        address = normalize_origin(match.group(1))
        if address is not None and address not in found:
            found.append(address)
    return tuple(found)


# --- the pinned carrier: its commit, and its `.gitmodules` AT that commit -----


def pinned_commit(carrier_row: Row, repo_root: Path) -> PinnedCommit:
    """The commit a PINNED carrier's evidence is read at, from its ONE `pin` in
    THIS checkout, or the reason there is none. NEVER RAISES.

    "the row's evidence SHALL then be the carrier's `.gitmodules` AS OF THE
    COMMIT the carrier's `pin` names" (`admit-code-leg-under-pinned-root`). The
    pin is openxFactory's own file under `contracts/`, so it is read from the
    tree this run is judging — never from the supplied tree, whose bytes this
    estate did not write — and through THE HOUSE STRICT LOADER, as the pin's
    in-tree evidence re-check reads it, so the two reads of one pin cannot
    disagree about what it says.

    ONE REVISION OR NONE, IN `scripts/verify-opendox-pin.py::_pinned_commit`'S
    SHAPE AND NOTHING LOOSER: `revision_kind: commit` and a `commit:` of
    exactly 40 hex, lowercased. A tag, a branch or an abbreviated oid names no
    revision this reader may read at without resolving a movable name, and
    resolving one is a network question; so each is a REASON, and the caller's
    one verdict for it is NOT RE-CHECKED, naming the pin.

    AND THE PIN MUST STILL NAME THE CARRIER. A pin whose source moved to another
    repository records that repository's commit, not this carrier's; reading
    the carrier at it would read a revision nobody pinned. The row's in-tree
    `pin` re-check reports that pin GONE on the same run.
    """
    pins = [admission.path for admission in carrier_row.admitted_by
            if admission.kind == PIN and admission.path is not None]
    if len(pins) != 1:
        return PinnedCommit(
            pin=None, commit=None,
            detail=f"`{carrier_row.repository}` is admitted by {len(pins)} "
                   "`pin`s, not exactly one, so no one pin names the commit "
                   "its `.gitmodules` is read at")
    pin = pins[0]
    path = _unescaped(repo_root, Path(pin))
    if path is None or not path.is_file():
        return PinnedCommit(
            pin=pin, commit=None,
            detail=f"this tree carries no `{pin}` to read "
                   f"`{carrier_row.repository}`'s pinned commit from")
    try:
        document = fm.strict_load(path.read_text(encoding="utf-8"), what=pin)
    except (OSError, UnicodeDecodeError, fm.StrictFrontMatterError,
            yaml.YAMLError, ValueError) as exc:
        return PinnedCommit(
            pin=pin, commit=None,
            detail=f"`{pin}` cannot be read through the strict loader "
                   f"({exc}), so it names no commit to read at")
    if not _pin_names_repository(document, carrier_row.repository):
        return PinnedCommit(
            pin=pin, commit=None,
            detail=f"`{pin}` no longer names `{carrier_row.repository}` as its "
                   "source, so the commit it records is not that carrier's")
    assert isinstance(document, dict)  # `_pin_names_repository` requires it
    revision_kind = document.get("revision_kind")
    if revision_kind != "commit":
        return PinnedCommit(
            pin=pin, commit=None,
            detail=f"`{pin}` declares `revision_kind: {revision_kind!r}`, not "
                   "`commit`, so it names no commit to read "
                   f"`{carrier_row.repository}`'s `.gitmodules` at; resolving "
                   "a movable name would be a network read, and this run "
                   "makes none")
    commit = document.get("commit")
    if not isinstance(commit, str) \
            or COMMIT_RE.fullmatch(commit.strip()) is None:
        return PinnedCommit(
            pin=pin, commit=None,
            detail=f"`{pin}` records `commit: {commit!r}`, which is not "
                   "exactly 40 hex characters; an abbreviated oid, a branch "
                   "or a tag names no one revision to read at")
    commit = commit.strip().lower()
    return PinnedCommit(pin=pin, commit=commit,
                        detail=f"`{pin}` names {commit}")


def _gitmodules_at(tree: Path,
                   commit: str) -> tuple[tuple[str, ...] | None, str]:
    """`(addresses, "")` for the `.gitmodules` `tree`'s object store holds at
    `commit`, or `(None, why)` when it cannot produce it locally.

    FOUR READS, EACH LOCAL, EACH THROUGH THE SANITIZED, TIME-BOUNDED `_git` —
    so under the transport refusal a missing object is an ANSWER ("cannot
    produce") and never a fetch:

    1. `cat-file -t <commit>` — THE OBJECT IS A COMMIT, and not a tag, a tree or
       a blob that happens to carry the oid the pin wrote; a tag would peel to
       a commit nobody pinned.
    2. `ls-tree --full-tree <commit> -- :(literal).gitmodules` — the entry at
       the ROOT of that commit's tree, root-relative whatever prefix git
       infers, the path a NAME and never pathspec magic: the idiom
       `scripts/carved_reach.py::_tree_entry_absent` measured, where exit 0
       with nothing printed is git's one unambiguous "no such entry".
    3. THE ENTRY IS A REGULAR FILE (`_GITMODULES_MODES`): a symlink's blob is a
       link target, not the carrier's submodule list, which is why
       `gitmodules_addresses` refuses a symlinked working-tree `.gitmodules`.
    4. `cat-file blob <oid>` — the bytes, exactly as the object store holds
       them: no textconv, no attributes and no working file.

    A commit whose tree carries NO `.gitmodules` answers `((), "")`: the root
    names no submodule at the revision openxFactory consumes, so a leg the row
    claims is ABSENT there, which is a finding and not a silence.
    """
    if not isinstance(commit, str) or COMMIT_RE.fullmatch(commit) is None:
        return None, f"`{commit!r}` is not a 40-hex commit to read at"
    commit = commit.lower()
    cannot = ("its object store cannot produce {what} without a network call "
              "— a partial clone missing the object, a shallow clone, or a "
              "checkout that never fetched that commit")
    kind = _git(tree, "cat-file", "-t", commit)
    if kind is None:
        return None, cannot.format(what=f"the commit {commit}")
    if kind.strip() != "commit":
        return None, (f"its object store holds {commit} as a "
                      f"`{kind.strip()}`, not a commit")
    listing = _git(tree, "ls-tree", "-z", "--full-tree", commit, "--",
                   ":(literal).gitmodules")
    if listing is None:
        return None, cannot.format(what=f"the tree of {commit}")
    records = [record for record in listing.split("\0") if record]
    if not records:
        return (), ""  # the commit's tree carries no `.gitmodules`: an answer
    meta, tab, name = records[0].partition("\t")
    fields = meta.split(" ")
    if len(records) != 1 or not tab or name != ".gitmodules" \
            or len(fields) != 3:
        return None, (f"`git ls-tree` answered for `.gitmodules` at {commit} "
                      "in a shape this reader does not take")
    mode, object_type, oid = fields
    if mode not in _GITMODULES_MODES or object_type != "blob":
        return None, (f"at {commit} `.gitmodules` is a `{object_type}` of mode "
                      f"{mode}, not a regular file, so its object is not the "
                      "carrier's submodule list")
    if COMMIT_RE.fullmatch(oid) is None:
        return None, (f"`git ls-tree` named `.gitmodules` at {commit} by "
                      f"`{oid}`, which is not a 40-hex object id")
    blob = _git(tree, "cat-file", "blob", oid)
    if blob is None:
        return None, cannot.format(
            what=f"the `.gitmodules` blob {oid} at {commit}")
    return _gitmodules_url_addresses(blob), ""


def gitmodules_addresses_at(tree: Path, commit: str) -> tuple[str, ...] | None:
    """The repositories `tree`'s `.gitmodules` names AS OF `commit`, read out of
    the tree's OWN OBJECT STORE — never its working files, never another
    revision — or None when the store cannot produce it without the network.
    NEVER RAISES, AND NEVER FETCHES.

    "the row's evidence SHALL then be the carrier's `.gitmodules` AS OF THE
    COMMIT the carrier's `pin` names, read out of the supplied tree's own object
    store — never out of its working files, and never at another revision …
    THE READ SHALL MAKE NO NETWORK CALL" (`admit-code-leg-under-pinned-root`).
    The estate already reads a pin this way —
    `scripts/verify-opendox-pin.py::_openxdox_derived_commit` reads openXdox's
    own pin "as a git BLOB … never the openXdox working tree" — and this read
    adds the one guard that sibling does not carry: every transport refused
    (`_sanitized_git_environment`), because an object-store read in a partial
    clone would otherwise FETCH the missing blob from its promisor remote
    (`admit-code-leg-under-pinned-root`'s `design.md` D0.6).

    `None` IS NOT AN ABSENCE. It is a store that could not answer — a partial
    clone missing the object, a shallow clone, a checkout that never fetched
    the pinned commit, an object that is not a commit, a `.gitmodules` that is
    not a regular file — and the one verdict for it is NOT RE-CHECKED. An EMPTY
    tuple is the answer that the commit's tree names no submodule at all.
    `_gitmodules_at` carries the reason, for the report.
    """
    return _gitmodules_at(tree, commit)[0]


def carrier_members(inventory: Inventory, carrier: str, tree: Path,
                    repo_root: Path) -> CarrierMembers:
    """What a supplied tree that VERIFIED as `carrier` says the carrier carries,
    read WHERE THE REQUIREMENT SAYS TO READ IT. NEVER RAISES.

    CALLED ONLY FOR A VERIFIED TREE: `carrier_identity` is the first step for
    both carriers alike ("the tree supplied for it SHALL first be verified as
    the carrier on exactly the terms above"), and it is not repeated here.

    A GOVERNED CARRIER IS READ EXACTLY AS BEFORE, from its WORKING TREE
    (`gitmodules_addresses`): openxFactory consumes no governed carrier at a
    commit, so there is no revision to bind its evidence to
    (`admit-code-leg-under-pinned-root`'s `design.md` D9) — and a supplied tree
    whose carrier has no row at all, which no row's `gitlink` can then name, is
    read the same way it always was.

    A PINNED CARRIER IS READ AT THE COMMIT ITS PIN NAMES AND AT NO OTHER
    REVISION: `pinned_commit` from its one pin in this checkout, then
    `gitmodules_addresses_at` from the supplied tree's own object store. A pin
    naming no commit, and a store that cannot produce that commit's
    `.gitmodules` without a network call, each come back with `addresses` None
    and a detail naming THE PIN AND THE COMMIT, which is what the scenario asks
    the NOT RE-CHECKED report to name: a run that has looked at the wrong
    revision has not looked.
    """
    row = inventory.by_address.get(carrier)
    prefix = f"the working tree supplied for {carrier} verified, but "
    if row is None or row.governance != "pinned":
        addresses = gitmodules_addresses(tree)
        return CarrierMembers(
            carrier=carrier, addresses=addresses, where="its `.gitmodules`",
            detail="" if addresses is not None
            else prefix + "its `.gitmodules` could not be read")
    pinned = pinned_commit(row, repo_root)
    if pinned.commit is None:
        return CarrierMembers(
            carrier=carrier, addresses=None, pin=pinned.pin,
            where="its `.gitmodules` at the commit its pin names",
            detail=prefix + pinned.detail)
    where = (f"its `.gitmodules` AT {pinned.commit}, THE COMMIT "
             f"`{pinned.pin}` NAMES,")
    addresses, why = _gitmodules_at(tree, pinned.commit)
    return CarrierMembers(
        carrier=carrier, addresses=addresses, where=where,
        commit=pinned.commit, pin=pinned.pin,
        detail="" if addresses is not None
        else (f"{prefix}{why}; the commit is the one `{pinned.pin}` names, "
              "and every transport is refused, so nothing was fetched"))
