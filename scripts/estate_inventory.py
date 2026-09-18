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

Deterministic: text/YAML reads only, no model calls, no writes, no network.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import frontmatter_strict as fm

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

#: A `.gitmodules` `url =` LINE'S REPOSITORY. The same normalization, applied to
#: the submodule URLs a carrier's `.gitmodules` carries.
_GITMODULES_URL_RE = re.compile(r"^\s*url\s*=\s*(\S+)\s*$")

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


def load_transfers(repo_root: Path) -> dict[str, str]:
    """`{former address: current address}` for the COMPLETE transfers only.

    THE PENDING ROWS ARE DROPPED AND THAT IS THE MAP'S OWN INSTRUCTION, not a
    strictness invented here. `pending_row_rule` reads: "A row whose
    `transfer_state` is `pending` DECLARES a ruled identity change that HAS NOT
    HAPPENED. … A reader MUST NOT resolve `former` -> `current` for any LIVE
    reference while the row is `pending` — at that point `former` is still the
    only address that exists." Every use this module makes of the map is a live
    reference: a head being resolved now, a row being judged now, a working tree
    being verified now.

    AN ABSENT OR UNREADABLE MAP IS AN EMPTY ONE AND NOT A REFUSAL. The map is a
    contract member this packet READS and does not own; a tree that carries no
    transfers has taken none, and a reader that refused to run without it would
    make every consuming tree carry a file to say nothing. What is lost is the
    former-address REPORT, which is a report and never an authorization — so the
    failure mode is a finding not raised, never a head wrongly admitted.
    """
    path = _unescaped(repo_root, TRANSFER_MAP)
    if path is None or not path.is_file():
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
        doc = fm.strict_load(raw, what=str(TRANSFER_MAP))
    except (OSError, UnicodeDecodeError, fm.StrictFrontMatterError):
        return {}
    if not isinstance(doc, dict):
        return {}
    transfers = doc.get("transfers")
    if not isinstance(transfers, list):
        return {}
    resolved: dict[str, str] = {}
    for entry in transfers:
        if not isinstance(entry, dict):
            continue
        former, current = entry.get("former"), entry.get("current")
        if not isinstance(former, str) or not isinstance(current, str):
            continue
        if entry.get("transfer_state") != "complete":
            continue  # pending_row_rule: not a resolution instruction
        resolved[former] = current
    return resolved


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
            if admission.kind == ROOT and row.repository != AGGREGATION_ROOT:
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
            if admission.kind != GITLINK:
                continue
            assert admission.carrier is not None
            carrier_row = seen_addresses.get(admission.carrier)
            if carrier_row is None:
                raise EstateInventoryError(
                    f"row {row.position} ({row.repository}) is admitted by a "
                    f"gitlink in `{admission.carrier}`, which THIS INVENTORY "
                    "CARRIES NO ROW FOR. The kind is a GOVERNED ESTATE "
                    "REPOSITORY's `.gitmodules`, so the carrier is itself a "
                    "member of the estate and the inventory is where the "
                    "estate's members are written down; a carrier no row names "
                    "is a tree this file cannot say the estate has, and a "
                    "re-check pointed at it would discharge one row on the "
                    "word of a repository nothing admits. Add the carrier's "
                    "own row, or record the naming act that really happened")
            if carrier_row.governance != "governed":
                raise EstateInventoryError(
                    f"row {row.position} ({row.repository}) is admitted by a "
                    f"gitlink in `{admission.carrier}`, whose own row "
                    f"{carrier_row.position} declares "
                    f"`governance: {carrier_row.governance}`. THE KIND SAYS "
                    "GOVERNED and means it: a `pinned` repository is one this "
                    "estate consumes at a commit and digest and authors none "
                    "of, and an `external` one is not of this estate at all, "
                    "so neither performs an ACT OF ADMISSION when its "
                    "`.gitmodules` happens to name something. Reading their "
                    "submodule lists as admissions would let a tree nobody "
                    "here writes decide who is in the estate")

    return Inventory(rows=tuple(rows), path=path)


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


#: AN ADDRESS'S OWN BOUNDARIES, so a match is the repository and not a prefix of
#: a longer one. `opensoft/openXwallet` contains the characters of
#: `opensoft/open`, and a plain `in` test therefore lets ANY row whose address
#: is a prefix of a real member's be discharged by that member's evidence — the
#: row `opensoft/open` reading a pin that names only `opensoft/openXwallet` and
#: reporting NAMED. The owner side has the same hole in the other direction
#: (`soft/openDox` inside `opensoft/openDox`).
#:
#: A NAME CHARACTER ON EITHER SIDE IS WHAT IS REFUSED, and `/` deliberately is
#: NOT: the estate's own evidence writes addresses inside URLs
#: (`source_url: https://github.com/opensoft/openRepoShape`), so a leading `/`
#: is the ordinary lawful case and forbidding it would report the estate's real
#: pins as gone. A TRAILING `.git` IS ADMITTED EXPLICITLY, because a
#: `.gitmodules` or workflow writes `…/opensoft/openDox.git` and `.` is
#: otherwise a name character — but only that exact suffix, so
#: `opensoft/openDox-code` still does not discharge `opensoft/openDox`.
_ADDRESS_BOUNDARY = r"(?<![A-Za-z0-9._-]){address}(?:\.git)?(?![A-Za-z0-9._-])"


def _names_repository(path: Path, repository: str) -> bool:
    """Whether the evidence file at `path` really names `repository`.

    PRESENCE OF THE FILE IS NOT PRESENCE OF THE EVIDENCE. A `pin` whose file
    stopped naming the repository — repointed at another source, or reduced to a
    template — is a row whose admission has gone as surely as a deleted file,
    and a check that asked only `is_file()` would report it as named. The match
    is on the ADDRESS, the spelling the row itself carries, so a file naming
    only a bare name does not discharge an address row by accident.

    AND THE ADDRESS IS MATCHED WHOLE. A SUBSTRING IS NOT A NAMING: an address
    embedded in a longer address is a DIFFERENT REPOSITORY, and an admission
    discharged by one is a row whose evidence was never about it. See
    `_ADDRESS_BOUNDARY` for which characters bound it and why `/` is not one.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return re.search(
        _ADDRESS_BOUNDARY.format(address=re.escape(repository)),
        text) is not None


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
                elif not _names_repository(resolved, row.repository):
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


def tree_origin(tree: Path) -> str | None:
    """The identity a working tree asserts, from its OWN origin URL, or None.

    `git -C <path> remote get-url origin` is the reading `design.md` D1.2 names.
    It is a LOCAL CONFIG READ and reaches no network, which is what keeps this
    inside the bound D1 refused the derived shape for: a required check may not
    depend on a token or on read access to a private repository.

    EVERY FAILURE IS A `None` AND NEVER A RAISE — no `git` on the PATH, a path
    that is not a repository, a repository with no `origin`, a tree that cannot
    be read, a `git` that hangs past the timeout. The caller's one verdict for a
    tree it could not confirm is NOT RE-CHECKED, and a raise would turn a
    caller's typo into a failed run.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(tree), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=30, check=False)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return normalize_origin(result.stdout.strip())


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
            detail=f"no origin URL could be read from `{tree}` — it is not a "
                   "git working tree, has no `origin` remote, or spells its "
                   "remote in a form this estate does not write")
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
    found: list[str] = []
    for line in text.splitlines():
        match = _GITMODULES_URL_RE.match(line)
        if match is None:
            continue
        address = normalize_origin(match.group(1))
        if address is not None and address not in found:
            found.append(address)
    return tuple(found)
