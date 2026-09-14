#!/usr/bin/env python3
"""A PACKET REFERENCE RESOLVES BY ITS IDENTITY, AND NEVER BY THE PATH IT WAS
SPELLED AS (`release-realization` — *A packet reference resolves by identity,
not by path*; `add-declared-former-id` §§ 5.1, 5.1a, 5.2, 5.2a; issue #833).

THE DEFECT, AND WHY IT IS NOBODY'S FAULT. A path written into a record is a
SPELLING OF AN IDENTITY AT ONE MOMENT; the identity is what the record meant,
and it is the identity that has to resolve. Every packet in this corpus moves
exactly once — `openspec/changes/<id>/` becomes
`openspec/changes/archive/<YYYY-MM-DD>-<id>/` — and at that moment every record
citing it by path goes stale, by an act nobody thinks of as breaking anything.
Since `add-declared-former-id` a packet may also move by RENAME, declaring where
it came from in `former_ids:`, and the same sentence covers that: a reference is
dangling only when it resolves to NOTHING under the identity rule.

A PACKET-RELATIVE PATH CARRIES THE ID IT ADDRESSES, which is what makes the rule
reach citations written as paths and not only citations written as ids: the
second segment of `openspec/changes/<id>/…` names the packet and the remainder
names a file within it.

THE FOUR ANSWERS, AND WHY EACH IS ITS OWN ANSWER.

  * `RESOLVED` — the id stands in exactly one place and that packet carries the
    cited file. **A reference that resolves owes the citing record no edit**:
    where a reference resolves by identity it is not a defect and nothing is
    owed, the reader resolves it. This module therefore offers no corrected
    spelling for a caller to write back — offering one is how a reader becomes
    an editor, and "correcting a record is not the remedy this requirement
    imposes".
  * `DANGLING`, half `identity` — the id stands nowhere: no active directory, no
    dated archive directory, no packet declaring it. A defect of the citing
    record, which is the only one of the four that is.
  * `DANGLING`, half `file` — the id stands, and the packet it stands in does
    not carry the remainder. **BOTH HALVES SHALL RESOLVE, AND A FAILURE SHALL
    SAY WHICH HALF FAILED**; this one is reported AGAINST THE FILE and never
    against the packet, because resolving the identity alone would accept a
    citation to a file deleted, renamed or never written.
  * `AMBIGUOUS` — the id would stand in more than one place. **RESOLUTION IS TO
    EXACTLY ONE PACKET, OR TO NOTHING, AND NEVER TO A SET**: two dated archive
    directories for one id, a live directory beside somebody's declared former
    id, or two packets declaring the same former id are reported and never
    settled by preferring a candidate. "A resolver that silently picks one
    candidate makes the record's meaning depend on sort order." The defect
    belongs to the DECLARATION that made one identity resolve twice, not to the
    citing record.

AND A FIFTH ANSWER THAT IS NOT AN OUTCOME: `NOT_A_PACKET_REFERENCE`. A path that
addresses no packet — a script, a contract, or a file that merely sits under
`openspec/changes/` without naming a packet, such as this corpus's own
`openspec/changes/README.md` — is handed straight back, and the caller's own
path resolution is left exactly where it was. That boundary is load-bearing: a
resolver that read `README.md` as a change id would report the corpus's own
README dangling.

THE CROSS-REPOSITORY CASE IS NOT DECIDED HERE (§ 5.2). A reference to another
repository's packet "is no evidence about that reference" on the tree being
read, and the classification that keeps it out of scope belongs to the caller —
in this estate, `scripts/validate-pin-registrations.py`'s `read_citation`, whose
`qualified` kind reads the repository vocabulary the pin itself declares. So
this module holds NO repository vocabulary and NO module-level root: it resolves
against the root it is handed, and the same reference answers differently
against two roots, which is precisely why it cannot be the reader that says a
packet is somebody else's.

WHAT IS IMPORTED AND WHAT IS BUILT HERE, STATED. The declaration grammar, the id
grammar and the archive-date rule are `scripts/proposal-support.py`'s and are
IMPORTED (`CHANGE_ID_RE`, `change_id_of`, `ARCHIVE_DATE_PREFIX`,
`declared_former_ids_of`, `FormerIdError`, `FORMER_IDS_KEY`, and
`packet_identities_of` for the archive's two-reading ambiguity) rather than
respelled. What is built here is the WORKING-TREE LOCATION INDEX, and it is
built rather than reused for a reason the packet's own plan states: that
module's `identity_paths_at` resolves the same two-candidate rule AT A REVISION
for the archive gate and RAISES on ambiguity, while a citation is resolved IN
THE WORKING TREE and ambiguity is a third OUTCOME beside resolved and dangling,
which a reporting reader must be able to return rather than raise. Forcing one
function to be both would make the archive gate's refusal depend on a citation
reader's tolerance. `former_identity_claimants` is the neighbouring corpus
sweep and answers a different question — who OWNS an identity, rendered as
prose for a finding — where this answers where a packet now STANDS, as a path.
`tests/packet_reference/` pins the two in step, and states the one difference:
the sweep deliberately does not read an archived directory's own id, and
resolution needs it.

IMPORT COST, DISCLOSED. `scripts/proposal-support.py` inserts `scripts/` at
`sys.path[0]` when it loads, to reach `doc_health.pin_sentinels` (a sibling that
"depends on nothing outside the standard library", in its own words). Under the
documented invocation of every consumer that is already `sys.path[0]`; under a
`spec_from_file_location` load it is an addition, and the suite that performs
one already loads that module. Named here rather than discovered later.

Run: this module is a library and has no CLI. Its consumer is
`scripts/validate-pin-registrations.py`'s `check_citations`.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

#: The statuses `resolve` returns. Strings rather than an enum so a finding can
#: carry one and a caller in another repository can compare without importing.
RESOLVED = "resolved"
DANGLING = "dangling"
AMBIGUOUS = "ambiguous"
NOT_A_PACKET_REFERENCE = "not-a-packet-reference"

#: Which half of a two-half reference failed. Lowercase because they are read
#: back out of the report sentence as well as off the `Resolution`.
IDENTITY_HALF = "identity"
FILE_HALF = "file"

#: How a packet directory claims an identity.
ACTIVE = "active"
ARCHIVED = "archived"
DECLARED = "declared"

CHANGES_ROOT = "openspec/changes"
ARCHIVE_ROOT = f"{CHANGES_ROOT}/archive"
ARCHIVE_SEGMENT = "archive"


def _support():
    """`scripts/proposal-support.py`, loaded by location.

    The file is HYPHENATED and therefore unimportable by name — the reason
    `tests/proposal-support/` and `tests/pin_registrations/` both load their
    subjects this way. `sys.modules` is consulted first so a process that has
    already loaded it (the test suite does, under `proposal_support`) gets the
    one copy rather than a second, and `sys.path` is not mutated here:
    "a library module that inserts its own directory at `sys.path[0]` changes
    import resolution for every caller in the process" (`scripts/sequenced_after.py`).
    """
    for name in ("proposal_support", "proposal-support"):
        loaded = sys.modules.get(name)
        if loaded is not None and hasattr(loaded, "declared_former_ids_of"):
            return loaded
    path = Path(__file__).resolve().parent / "proposal-support.py"
    spec = importlib.util.spec_from_file_location("proposal_support", path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"cannot locate proposal support at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["proposal_support"] = module
    spec.loader.exec_module(module)
    return module


support = _support()


@dataclass(frozen=True)
class Claim:
    """One packet directory's claim on one identity, in the working tree.

    `rel` is the corpus's own spelling of the directory, so a finding reads the
    same on a runner and on a developer machine. `why` is the sentence that says
    what makes it a claim, because an AMBIGUOUS report is only actionable if it
    says which act created each candidate.
    """

    identity: str
    path: Path
    rel: str
    kind: str
    declared_by: str | None = None

    @property
    def why(self) -> str:
        if self.kind == ACTIVE:
            return f"`{self.rel}` is the active packet directory for this id"
        if self.kind == ARCHIVED:
            return f"`{self.rel}` is a dated archive directory for this id"
        return (f"`{self.declared_by}` declares `{self.identity}` in "
                f"`{support.FORMER_IDS_KEY}:`")

    def carries(self, remainder: str, root: Path) -> bool:
        """Whether this packet carries the remainder a citation names.

        `.exists()` and not `.is_file()`, in step with the consumer this reader
        was built for: "a citation legitimately names a change packet's
        directory", so a remainder naming a subdirectory resolves.

        `root` IS PASSED AND NOT STORED: a `Claim` is a location within
        whatever tree `PacketIndex` was built over and carries no root of its
        own. It is needed here because `remainder` is CITATION-SUPPLIED text —
        never a `.`/`..` segment (`packet_reference` refuses those before this
        is reached), but still free to name a path segment that happens to be
        a symlink escaping `root` from inside an otherwise legitimate packet
        directory, and `.exists()` would follow it. `_contained` is applied to
        `self.path` too, even though `PacketIndex._build` only ever
        constructs a `Claim` from a directory that already passed the same
        check — belt and suspenders over an invariant a future caller could
        otherwise break by constructing one directly.
        """
        target = self.path if not remainder else self.path / remainder
        contained = _contained(root, target)
        return contained is not None and contained.exists()


@dataclass(frozen=True)
class Resolution:
    """What one reference resolved to, and — when it did not — which half
    failed and whose defect it is."""

    status: str
    claimed: str
    identity: str | None = None
    remainder: str = ""
    location: Claim | None = None
    candidates: tuple[Claim, ...] = ()
    half: str | None = None
    report: str = ""

    @property
    def ok(self) -> bool:
        """True where nothing is owed by anybody: the reference resolved, or it
        was never a packet reference and belongs to the caller's own path
        resolution."""
        return self.status in (RESOLVED, NOT_A_PACKET_REFERENCE)

    @property
    def resolved_rel(self) -> str | None:
        """The path the reference resolves TO, as the corpus spells it."""
        if self.location is None:
            return None
        if not self.remainder:
            return self.location.rel
        return f"{self.location.rel}/{self.remainder}"

    @property
    def relocated(self) -> bool:
        """True where the reference resolved somewhere OTHER than the path it
        was spelled as — the citation the archive relocation or a declared
        rename would otherwise have broken. Reported by a caller so a reader can
        see the resolver working; never an instruction to rewrite the record."""
        if self.status != RESOLVED:
            return False
        return self.resolved_rel != _normalised(self.claimed)


def _normalised(claimed: str) -> str:
    """A claimed path with its empty segments dropped, so a trailing slash is
    not a different reference from the same path without one."""
    return "/".join(part for part in str(claimed).split("/") if part)


def _contained(root: Path, path: Path) -> Path | None:
    """`path` resolved — following every symlink in the chain — and returned
    only where it still stands inside `root`; `None` where it does not, or
    where resolving it cannot be done at all (a symlink loop, an unreadable
    segment).

    `Path.is_dir()`, `Path.is_file()` and `Path.exists()` all follow symlinks,
    and every path this module tests one of them against is either a WORKING
    TREE ENTRY (`PacketIndex._build`'s directory scan) or built by joining a
    CITATION-SUPPLIED remainder onto one (`Claim.carries`, `resolve`'s own
    fallback) — both a hostile or careless commit controls. Mirrors
    `scripts/validate-pin-registrations.py`'s `resolve_in_tree` containment
    idiom (`.resolve()` then `is_relative_to`) rather than inventing a second
    one: this module's own docstring already credits that function with the
    judgement "a reference that walks out of the tree is the caller's
    containment question and never this reader's" — true of a citation's
    SPELLING, and equally true of a directory this module discovers by
    walking the tree that spelling names.
    """
    try:
        resolved_root = root.resolve()
        resolved = path.resolve()
    except (OSError, RuntimeError):
        return None
    return resolved if resolved.is_relative_to(resolved_root) else None


def _contained_dir(root: Path, path: Path) -> bool:
    """True where `path` is a directory that stays inside `root` once every
    symlink in it is resolved; False otherwise, INCLUDING where `path` is a
    symlink to a directory OUTSIDE `root` — the case `Path.is_dir()` alone
    answers wrongly, because it follows the link and reports the target's own
    type rather than anything about where the link itself sits. A directory
    that fails this contributes NO CLAIM, exactly as `PacketIndex._build`
    already treats a malformed `former_ids:` declaration: "a resolver that
    raised here would turn one packet's malformed declaration into a refusal
    of every citation in the corpus" — true in the same words of one hostile
    symlink.
    """
    resolved = _contained(root, path)
    return resolved is not None and resolved.is_dir()


def packet_reference(claimed) -> tuple[str, str] | None:
    """`(identity, remainder)` for a path that ADDRESSES A PACKET, else None.

    BOTH SPELLINGS ARE READ, because both are written into this corpus's
    records: `openspec/changes/<id>/<remainder>` names a packet by the id
    directly, and `openspec/changes/archive/<YYYY-MM-DD>-<id>/<remainder>` names
    it through the dated directory the archive relocation created. The DATE IS
    PART OF THE SPELLING AND NOT PART OF THE IDENTITY — this estate corrects an
    archive directory's date (`proposal-support.py`'s
    `assert_archived_directory_date`), and a citation written against the old
    date names the same packet afterwards. The id is read out of the dated name
    by `change_id_of`, the estate's own rule, rather than by a second regex
    written here.

    A REMAINDER MAY BE EMPTY: a citation legitimately names a packet directory.

    WHAT IS REFUSED AS "NOT A PACKET REFERENCE", each for its own reason: a path
    that is absolute or carries a `.`/`..` segment, because a reference that
    walks out of the tree is the caller's containment question and never this
    reader's (`resolve_in_tree` in the consumer refuses it in those words, and a
    library that trusted its caller's containment would hand the next caller a
    read outside the repository); `openspec/changes/archive` itself and a
    directory under it whose name carries no archive date, because neither names
    a packet; and a second segment that is not a change id by the grammar this
    estate resolves a packet with, or is the literal `archive`, which
    `active_change_dir` refuses by name for the same reason.
    """
    if not isinstance(claimed, str) or not claimed.strip():
        return None
    raw = claimed.strip()
    if raw.startswith("/"):
        return None
    parts = [part for part in raw.split("/") if part]
    if any(part in (".", "..") for part in parts):
        return None
    if len(parts) < 3 or parts[0] != "openspec" or parts[1] != "changes":
        return None
    if parts[2] == ARCHIVE_SEGMENT:
        if len(parts) < 4 or not support.ARCHIVE_DATE_PREFIX.match(parts[3]):
            return None
        # `change_id_of` strips the date only where the PARENT it is handed is
        # named `archive` (`RESERVED_CHANGE_ID`) — the fix landed at main
        # 701c8fde so an ACTIVE directory whose own id happens to look dated
        # (this corpus's `2026-08-04-add-dated`) is read verbatim rather than
        # mis-stripped. `parts[3]` is a bare leaf read out of a citation
        # string, with no real parent of its own, so it is handed to
        # `change_id_of` prefixed with the segment that citation already
        # proved it sits under (`parts[2] == ARCHIVE_SEGMENT`, just above) —
        # never the bare leaf alone, which `change_id_of` would now read as an
        # unparented name and return it un-stripped, unchanged.
        identity = support.change_id_of(Path(ARCHIVE_SEGMENT) / parts[3])
        remainder = parts[4:]
    else:
        identity = parts[2]
        remainder = parts[3:]
    if identity == ARCHIVE_SEGMENT or not support.CHANGE_ID_RE.fullmatch(identity):
        return None
    return identity, "/".join(remainder)


class PacketIndex:
    """Every identity this working tree carries -> the packets carrying it.

    THREE CLAIMS, AND THE REQUIREMENT NAMES ALL THREE as the places an id can
    stand: the ACTIVE directory `openspec/changes/<id>/`, every dated ARCHIVE
    directory `openspec/changes/archive/<YYYY-MM-DD>-<id>/`, and every packet —
    active or archived — DECLARING that id in `former_ids:`. A declaration
    travels with the packet into its archived directory, so an archived
    packet's lineage is still a claim.

    BUILT ONCE AND PASSED DOWN. A caller resolving a dozen citations asks about
    a dozen identities over one tree; building the map per question would read
    every packet's `.openspec.yaml` a dozen times. The build is LAZY so a caller
    with no packet reference to resolve pays nothing, and there is deliberately
    NO cache keyed on the root: a resolver that remembered a tree would answer
    stale in exactly the suites that build a tree, mutate it and ask again.

    A MALFORMED DECLARATION CONTRIBUTES NO CLAIM and is not raised over, on
    `former_identity_claimants`'s stated precedent: "this is the corpus sweep,
    and `former_id_problems` is the reader that reports shape". A resolver that
    raised here would turn one packet's malformed declaration into a refusal of
    every citation in the corpus.

    A DIRECTORY THAT ESCAPES `root` CONTRIBUTES NO CLAIM EITHER, on the same
    ground. `Path.is_dir()` and `Path.iterdir()` follow symlinks, and a
    symlinked packet directory pointing outside `root` — committed by a
    hostile or careless PR — would otherwise be indexed and read through the
    link, exactly as `check_citations`'s own containment check
    (`resolve_in_tree`) already refuses for a citation's raw spelling; that
    check alone does not reach here, because it containment-checks the path a
    citation was WRITTEN as, and this index is built by walking the tree, not
    by re-deriving it from any one citation. `_build` applies the identical
    `.resolve()`-then-`is_relative_to` containment (`_contained_dir`) to every
    directory it discovers.
    """

    def __init__(self, root) -> None:
        self._root = Path(root)
        self._claims: dict[str, list[Claim]] | None = None

    @property
    def root(self) -> Path:
        return self._root

    def _add(self, claims: dict[str, list[Claim]], claim: Claim) -> None:
        held = claims.setdefault(claim.identity, [])
        if all(existing.path != claim.path for existing in held):
            held.append(claim)

    def _rel(self, directory: Path) -> str:
        return f"{CHANGES_ROOT}/{directory.relative_to(self._root / 'openspec' / 'changes').as_posix()}"

    def _build(self) -> dict[str, list[Claim]]:
        claims: dict[str, list[Claim]] = {}
        root = self._root
        changes = root / "openspec" / "changes"
        if not _contained_dir(root, changes):
            return claims
        live = [d for d in sorted(changes.iterdir())
                if d.name != ARCHIVE_SEGMENT
                and support.CHANGE_ID_RE.fullmatch(d.name)
                and _contained_dir(root, d)]
        archive = changes / ARCHIVE_SEGMENT
        archived = ([d for d in sorted(archive.iterdir())
                     if support.ARCHIVE_DATE_PREFIX.match(d.name)
                     and _contained_dir(root, d)]
                    if _contained_dir(root, archive) else [])
        for directory in live:
            self._add(claims, Claim(identity=directory.name, path=directory,
                                    rel=self._rel(directory), kind=ACTIVE))
        # AN ARCHIVED DIRECTORY CAN STAND FOR TWO IDENTITIES, NOT ONE.
        # `archive_directory_name` preserves an already-dated id UNCHANGED, so
        # `archive/2026-09-09-foo` is indistinguishably the archived `foo` AND
        # the archived `2026-09-09-foo` (`change_id_of`'s own docstring, and
        # `packet_identities_of` is its plural sibling "for the callers that
        # must not silently choose the shorter reading"). Indexing only the
        # stripped reading dropped the literal one, so a citation to
        # `openspec/changes/2026-09-09-foo/…` for a packet whose OWN id
        # begins with a date reported IDENTITY-DANGLING although that exact
        # proposal stands in the archived directory. (Copilot
        # `PRRT_kwDOTAvnrs6iSjPt`, Codex P2 `PRRT_kwDOTAvnrs6iSmuD`.)
        #
        # THE LITERAL READING YIELDS TO A LIVE PACKET OF THAT NAME, and only
        # the literal one does — `_archive_dir_carries`'s own guard, mirrored
        # here rather than reused because that function answers one identity
        # at a time and this loop is building the index all of them are
        # looked up against. A change that is LIVE has not been archived, so
        # an archive directory spelled exactly like a live id cannot be that
        # packet's own archive; it is the dated archive of the STRIPPED id,
        # and the stripped reading carries no such guard (`declared_former_
        # ids_in_tree`'s working-tree precedent: the guard sat on the
        # stripped arm once and suppressed a legitimate match).
        live_ids = {directory.name for directory in live}
        for directory in archived:
            for identity in support.packet_identities_of(directory):
                if identity == directory.name and identity in live_ids:
                    continue
                self._add(claims, Claim(identity=identity, path=directory,
                                        rel=self._rel(directory), kind=ARCHIVED))
        for directory in live + archived:
            # THE MARKER ITSELF IS CONTAINMENT-CHECKED, not only `directory`:
            # `directory` already passed `_contained_dir` above, but a single
            # committed file inside an otherwise legitimate packet can still
            # be a symlink of its own, and `.is_file()` follows it exactly as
            # `.is_dir()` does.
            marker = _contained(root, directory / ".openspec.yaml")
            if marker is None or not marker.is_file():
                continue
            # THE SELF-CLAIM CHECK IS ASKED UNDER BOTH READINGS TOO, on
            # `former_identity_claimants`'s already-landed precedent: passing
            # `identities[0]` (the directory's own literal name) is what lets
            # `former_id_problems`'s "an entry equal to the packet's OWN id"
            # refusal see the literal reading, and the `any(...)` guard below
            # catches a self-claim spelled under the STRIPPED one instead —
            # `former_id_problems` can only be asked about one id at a time.
            identities = support.packet_identities_of(directory)
            try:
                declared = support.declared_former_ids_of(directory,
                                                          identities[0])
            except support.FormerIdError:
                continue
            except (UnicodeDecodeError, OSError):
                # A MARKER THAT CANNOT BE READ AT ALL IS NO LESS "MALFORMED"
                # THAN ONE THAT PARSES TO THE WRONG SHAPE. `marker.is_file()`
                # above only proved the path was a regular file at that
                # instant; `load_packet` catches `yaml.YAMLError` around its
                # own read but not a bad encoding or a file gone unreadable
                # between the two calls, and neither of those is a
                # `FormerIdError`. Left uncaught, one such packet would abort
                # this index build entirely and crash pin validation, rather
                # than contributing no claim the way every other malformed
                # declaration already does. (Copilot `PRRT_kwDOTAvnrs6iTGJQ`.)
                continue
            if any(identity in declared for identity in identities):
                continue
            for identity in declared:
                self._add(claims, Claim(identity=identity, path=directory,
                                        rel=self._rel(directory), kind=DECLARED,
                                        declared_by=self._rel(directory)))
        return claims

    def _loaded(self) -> dict[str, list[Claim]]:
        if self._claims is None:
            self._claims = self._build()
        return self._claims

    def claims(self, identity: str) -> tuple[Claim, ...]:
        """Every packet claiming `identity`, in a deterministic order that is
        NEVER used to prefer one — `resolve` refuses a set rather than reading
        an element of it."""
        return tuple(self._loaded().get(identity, ()))

    def identities(self) -> tuple[str, ...]:
        """Every identity this tree carries, sorted."""
        return tuple(sorted(self._loaded()))


def _identity_half_report(identity: str) -> str:
    return (f"the packet id `{identity}` resolves to NOTHING in this tree — no "
            f"active `{CHANGES_ROOT}/{identity}/`, no dated "
            f"`{ARCHIVE_ROOT}/<YYYY-MM-DD>-{identity}/`, and no packet "
            f"declaring `{identity}` in `{support.FORMER_IDS_KEY}:` — so the "
            f"IDENTITY half of this reference is the half that failed. A "
            f"reference that resolves to no identity at all is a defect of the "
            f"record that wrote it")


def _file_half_report(identity: str, remainder: str, location: Claim) -> str:
    return (f"the packet id `{identity}` RESOLVES — {location.why} — and that "
            f"packet does not carry `{remainder}`, so the FILE half of this "
            f"reference is the half that failed. Reported against the file and "
            f"not against the packet: resolving the identity alone would accept "
            f"a citation to a file deleted, renamed or never written")


def _ambiguous_report(identity: str, candidates) -> str:
    return (f"the packet id `{identity}` resolves to MORE THAN ONE packet — "
            + "; ".join(claim.why for claim in candidates)
            + " — so this reference is AMBIGUOUS and is NOT resolved by "
              "preferring one candidate: a resolver that picked one would make "
              "this record's meaning depend on sort order. The defect belongs "
              "to the declaration that made one identity resolve twice and not "
              "to the citing record, which owes no edit")


def _resolved_report(identity: str, location: Claim,
                     resolution_rel: str, claimed: str) -> str:
    moved = ("" if resolution_rel == _normalised(claimed)
             else f", which is not the path the record spells (`{claimed}`)")
    return (f"the packet id `{identity}` resolves to `{resolution_rel}`"
            f"{moved} — {location.why}. A reference that resolves by identity "
            f"owes the citing record no edit")


def resolve(root, claimed: str, *, index: PacketIndex | None = None
            ) -> Resolution:
    """Resolve one reference against one working tree.

    The only entry point a consumer needs. `index` is the tree's claim map when
    the caller already built one — a caller resolving several references over
    one tree should, and every one of this module's own corpus assertions does.
    """
    parsed = packet_reference(claimed)
    if parsed is None:
        return Resolution(
            status=NOT_A_PACKET_REFERENCE, claimed=claimed,
            report=(f"`{claimed}` addresses no packet in this tree, so it is "
                    f"resolved as a path and not as an identity"))
    identity, remainder = parsed
    index = index if index is not None else PacketIndex(root)
    candidates = index.claims(identity)

    if len(candidates) > 1:
        return Resolution(status=AMBIGUOUS, claimed=claimed, identity=identity,
                          remainder=remainder, candidates=candidates,
                          report=_ambiguous_report(identity, candidates))

    if not candidates:
        # NOTHING CLAIMS THE ID. Where the path is nonetheless present, the
        # second segment was never an identity — `openspec/changes/README.md`
        # is the corpus's own case — and the reference is a plain path, handed
        # back to the caller's own resolution. Where it is absent too, the
        # identity half is the half that failed. CONTAINMENT APPLIES HERE TOO:
        # a claimed path is free text once it clears `packet_reference`'s own
        # `.`/`..`/absolute refusal, and a segment that is itself a symlink
        # escaping `root` must not be read as "present" any more than a
        # symlinked packet directory may be indexed as one.
        present = _contained(Path(root), Path(root) / _normalised(claimed))
        if present is not None and present.exists():
            return Resolution(
                status=NOT_A_PACKET_REFERENCE, claimed=claimed,
                identity=identity, remainder=remainder,
                report=(f"`{claimed}` is present in this tree and no packet "
                        f"claims `{identity}`, so its second segment names no "
                        f"identity and it is resolved as a path"))
        return Resolution(status=DANGLING, claimed=claimed, identity=identity,
                          remainder=remainder, half=IDENTITY_HALF,
                          report=_identity_half_report(identity))

    location = candidates[0]
    if not location.carries(remainder, Path(root)):
        return Resolution(status=DANGLING, claimed=claimed, identity=identity,
                          remainder=remainder, location=location,
                          candidates=candidates, half=FILE_HALF,
                          report=_file_half_report(identity, remainder,
                                                   location))
    resolved_rel = (location.rel if not remainder
                    else f"{location.rel}/{remainder}")
    return Resolution(
        status=RESOLVED, claimed=claimed, identity=identity,
        remainder=remainder, location=location, candidates=candidates,
        report=_resolved_report(identity, location, resolved_rel, claimed))
