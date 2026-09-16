"""The PURE, NON-EXECUTING adapter for `pinned_contract_manifest` records.

Ratified by `extend-prose-tagging-target-to-pinned-capabilities` (design D-2,
task 3.1). The pinned-target arm of `families.fam_tag_hygiene` asks ONE question
of a pin record — is this a record of an ADMITTED RECORD SHAPE, complete for that
shape? — and this module is the single place that judgement is made.

WHAT MAKES IT THE ROUTE, AND WHY A RECORD MAY NOT CHOOSE ITS OWN JUDGE. A pin
record is DATA under judgement. A member of it — `verify_pin:` or any other — is
NEVER a dispatch key, an import target or a path to run, because a record that
selects the code that judges it is a record that judges itself, and an added
`contracts/<anything>-pin.yaml` could then point the judgement at any path in
the checkout. So this module READS THE RECORD AND NOTHING ELSE. It opens no
file, imports no verifier, starts no subprocess and reaches no network; every
function here is a pure function of a mapping. `verify_pin:` is data this module
may be COMPARED against (`TRACKED_VERIFIERS`) and never followed.

WHAT THE TABLE HOLDS, AND WHERE EVERY ENTRY CAME FROM. A shape's required set is
that shape's SHAPE-GUARD-REQUIRED SET: exactly the top-level members the shape's
in-tree pin verifier REFUSES-WHEN-ABSENT IN ITS PURE, SOURCE-FREE GUARDS — the
refusals whose only input is the record, which is what those verifiers' reader
and guard functions run before any checkout, `git` call or network read. Every
entry below carries the MEASURED CITATION it was read from (script and line),
and `tests/doc-health/test_pin_shape_adapter.py` holds the table to those guards
with a two-leg equivalence test (task 3.3(p)) rather than to a promise: a RECORD
leg over each real record in `contracts/`, and a GUARD leg that imports each
verifier at its FIXED, AUTHORED path and calls the cited guard on the record with
the member removed. Where a member's refusal is reachable only inside that
verifier's `verify()` — measured, exactly `files:` under shape (a), once per
shape-(a) verifier — the citation instead carries the refusal TEXT and the test
re-READS it at the cited line, a read of the verifier rather than a run of it.

NECESSARY, AND BY DESIGN NOT SUFFICIENT. This adapter judges whether a NAME
resolves to a pin record OF AN ADMITTED SHAPE. It never judges whether the pin is
FAITHFUL TO ITS SOURCE, and it cannot: a source-dependent check such as
`scripts/validate-openreposhape-pin.py`'s `pin-surface-undeclared` (`:515-530`,
over `source.paths()` `:520`) has no offline answer. On a landed tree every
record in `contracts/` has already passed its FULL verifier, those verifiers
being required checks; what this adapter defends is the OFFLINE JUDGEMENT over
arbitrary trees — a fixture tree, an aggregate of repositories, a `--single-repo`
run over an arbitrary checkout, an added `contracts/evil-pin.yaml` — where no pin
verifier has run at all.

THE SHAPE IS THE KEY, NOT THE `revision_kind`. Two of the five records on
`origin/main` declare `revision_kind: commit` and are complete on different
member sets, so a table keyed on the revision kind alone would refuse a valid
record this repository ships.
"""

from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass, field
from typing import Callable

#: The one kind a pinned target may name. `kind: pinned_workflow`
#: (`contracts/review-lane-pin.yaml`) is EXCLUDED: it pins executable governance
#: code rather than a product whose units are capabilities, so it has no
#: capability set for a name to be about. The arm gates on this BEFORE any shape
#: is selected, which is why `kind` is a member of no shape's table.
KIND = "pinned_contract_manifest"

# ---------------------------------------------------------------------------
# Forms, transcribed by reference from the verifiers' own module constants.
# These are TRANSCRIPTIONS, never extensions: a verifier that changes its form
# is a verifier whose guard leg in `tests/doc-health/test_pin_shape_adapter.py`
# moves, which is what makes the transcription checkable rather than trusted.
# ---------------------------------------------------------------------------
_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")        # verify-openxwallet-pin.py:116
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")        # verify-openxwallet-pin.py:117
_VERSION_RE = re.compile(                            # validate-openspec-cli-pin.py:372
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
_INTEGRITY_RE = re.compile(r"^sha512-[A-Za-z0-9+/]+={0,2}$")   # :375
_SHA1_RE = re.compile(r"^[0-9a-fA-F]{40}$")                    # :376
_PACKAGE_RE = re.compile(r"^(?:@[a-z0-9][\w.-]*/)?[a-z0-9][\w.-]*$")   # :377
_LOCKFILE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.json$")  # :671

#: The digest kinds a published-artifact pin may declare as its referent
#: (`validate-openspec-cli-pin.py:382`).
CONTENT_ADDRESSED_KINDS: tuple[str, ...] = ("package_integrity",)

#: The one digest definition the shape-(b) verifiers implement
#: (`verify-opendox-pin.py:157-158`, `verify-openxdox-pin.py:186-187`). Each
#: refuses a value other than the one it implements, because a definition it
#: cannot compute is an unanswerable question rather than a finding about a tree.
DIGEST_ALGORITHM = "sha256"
DIGEST_DEFINITION = "sorted-ls-tree-r-v1"

COMMIT_REVISION_KIND = "commit"


def _is_text(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_commit(value) -> bool:
    return isinstance(value, str) and bool(_COMMIT_RE.match(value.strip()))


def _is_tree_digest(value) -> bool:
    return isinstance(value, str) and bool(_SHA256_RE.match(value.strip()))


def _exactly(expected) -> Callable:
    def form(value) -> bool:
        return value == expected
    return form


def _one_of(expected: tuple[str, ...]) -> Callable:
    def form(value) -> bool:
        return value in expected
    return form


def _is_source_repository(value) -> bool:
    """`<owner>/<name>`, the shape `_source_repository` requires
    (`validate-openreposhape-pin.py:258-264`: a string carrying exactly one
    `/`)."""
    return _is_text(value) and value.count("/") == 1


def _is_digests_mapping(value) -> bool:
    return isinstance(value, dict)


def _is_files_list(value) -> bool:
    """A non-empty list of mappings, each carrying a `path` and its `sha256`.

    Two refusals in one form, both reading the record alone: the LIST is refused
    when it is absent, not a list, or empty ("an empty claim is not a satisfied
    claim" — `verify-openxwallet-pin.py:392-397`,
    `validate-openreposhape-pin.py:438-443`), and an ENTRY is refused when it is
    not a mapping declaring a `path` (`:398-403`, `:446-450`) or when its
    recorded `sha256` is not 64 hex characters (`:406-417`), a digest that is
    not one being a digest no recomputation can ever equal.
    """
    if not isinstance(value, list) or not value:
        return False
    for entry in value:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            return False
        if not _is_tree_digest(entry.get("sha256")):
            return False
    return True


def _is_path_only_list(value) -> bool:
    """A list of PATH-ONLY STRINGS — the valid form of `pinned_by_commit_only:`.

    EVERY FALSEY VALUE IS EMPTY AND ADMITTED, not only absence: both verifiers
    read `pin.get("pinned_by_commit_only") or []`
    (`verify-openxwallet-pin.py:443-452`,
    `validate-openreposhape-pin.py:487-495`), so `None` and `""` are exactly as
    empty as an absent member or an explicit `[]` to the guard this adapter
    tracks — an adapter that refused them would be WIDER than the guard.

    A mapping entry is the wrong form and is refused; an entry carrying no
    `sha256` is NOT, the publisher having published no per-file digest for these
    members, so demanding one would demand an invented row
    (`verify-openxwallet-pin.py:443-452`,
    `validate-openreposhape-pin.py:487-495`).
    """
    if not value:
        return True
    if not isinstance(value, list):
        return False
    return all(_is_text(entry) for entry in value)


def _is_version(value) -> bool:
    return isinstance(value, str) and bool(_VERSION_RE.match(value.strip()))


def _is_integrity(value) -> bool:
    """`sha512-<base64>` decoding to the 64 bytes a SHA-512 digest occupies
    (`validate-openspec-cli-pin.py:619-643`). A truncated address addresses
    nothing, so the length is part of the form rather than a later check."""
    if not isinstance(value, str) or not _INTEGRITY_RE.match(value.strip()):
        return False
    try:
        raw = base64.b64decode(value.strip()[len("sha512-"):], validate=True)
    except (binascii.Error, ValueError, TypeError):
        return False
    return len(raw) == 64


def _is_shasum(value) -> bool:
    return isinstance(value, str) and bool(_SHA1_RE.match(value.strip()))


def _is_package(value) -> bool:
    return isinstance(value, str) and bool(_PACKAGE_RE.match(value.strip()))


def _is_lockfile_name(value) -> bool:
    return isinstance(value, str) and bool(_LOCKFILE_NAME_RE.match(value.strip()))


def _is_lockfile_packages(value) -> bool:
    """A positive whole number, however the record spells it
    (`validate-openspec-cli-pin.py:731-745`, which takes `int(str(...).strip())`
    and refuses anything below 1)."""
    try:
        return int(str(value).strip()) >= 1
    except (TypeError, ValueError):
        return False


def _is_binary(value) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "/" not in value


def _is_disposition_list(value) -> bool:
    """A list of entries, or `None`. Absent OR NULL is EMPTY at this guard
    (`validate-openspec-cli-pin.py:801-803`: `raw = pin.get("dispositions")`
    then `if raw is None: return []`), so `dispositions:` is not a required
    member and an explicit `null` is no more malformed than an absent key;
    present, non-null and not a list is refused (`:804-809`)."""
    return value is None or isinstance(value, list)


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Citation:
    """One measured guard site: where a verifier refuses this member.

    `guard` names the IMPORTABLE, SOURCE-FREE function the refusal is reachable
    through, or is `None` where the refusal sits inside that verifier's
    `verify()` behind its source checks and cannot be called source-free. In the
    second case `quote` and `quote_line` carry the refusal TEXT and the line it
    is on, and the equivalence test asserts that line still holds that text.
    """
    script: str
    line: int
    guard: str | None = None
    quote: str | None = None
    quote_line: int | None = None


@dataclass(frozen=True)
class Member:
    """One entry of a shape's required-member table.

    `spellings` is normally one name. It is TWO for shape (a)'s product-identity
    entry, whose spelling differs with how the product is mounted; which of the
    two that entry REQUIRES is decided per pin id by `required_spellings` — the
    record grain — and both are admitted only where the pin id is one this
    checker has measured no verifier for. See `_PRODUCT_IDENTITY`.
    """
    spellings: tuple[str, ...]
    form: Callable
    citations: tuple[Citation, ...]
    nested: str | None = None
    #: Per-spelling forms, where the two spellings are not judged alike: each
    #: guard reads its own member and refuses its own shape.
    forms: dict = field(default_factory=dict)

    # NO `name` ACCESSOR. One flattening both spellings into a single string
    # was exactly what made the entry regime-blind; the live name of an entry is
    # `" or ".join(required_spellings(member, pin_id))`, which cannot be spelled
    # without saying WHICH PIN it is the name for.

    def form_for(self, spelling: str) -> Callable:
        return self.forms.get(spelling, self.form)


_OPENXWALLET = "scripts/verify-openxwallet-pin.py"
_OPENREPOSHAPE = "scripts/validate-openreposhape-pin.py"
_OPENDOX = "scripts/verify-opendox-pin.py"
_OPENXDOX = "scripts/verify-openxdox-pin.py"
_OPENSPEC_CLI = "scripts/validate-openspec-cli-pin.py"

#: The refusal the two shape-(a) verifiers reach only inside `verify()`. Quoted
#: here and re-read at the cited line by the equivalence test's citation route.
_FILES_REFUSAL = "the pin lists no `files:` members, so it pins no bytes"

# SHAPE (a)'s PRODUCT-IDENTITY ENTRY, AND HOW IT RESOLVES AT THE RECORD GRAIN.
# `verify-openxwallet-pin.py:194` refuses a record without `submodule_path`;
# `validate-openreposhape-pin.py:258` refuses one without `source_repository`;
# neither verifier reads the other's member. So the shape requires EXACTLY ONE
# PRODUCT-IDENTITY MEMBER and, at the record grain, it is the one THAT RECORD's
# own verifier reads (design D-2).
#
# THE ADAPTER CANNOT ASK THE RECORD WHICH VERIFIER JUDGES IT — that is the
# record choosing its own judge, and `verify_pin:` is exactly the member D-2
# withdraws from that role. IT MAY CONSULT ITS OWN CODE-FIXED MAP, keyed by the
# PIN ID the MARKER named and the REGISTRY stem carries:
# `PRODUCT_IDENTITY_BY_PIN` below, reviewed with the resolver like every other
# row of this table. So the entry has TWO REGIMES, and the difference is which
# input it is keyed on rather than which code runs:
#
#   - a KNOWN pin id — one this checker has measured a verifier's guards for —
#     requires THAT record's own spelling, and the other spelling is a NON-TABLE
#     member of that record. This is what keeps the adapter from being NARROWER
#     than the guard it tracks: `contracts/openxwallet-pin.yaml` carries BOTH
#     spellings, so an entry satisfied by either would ACCEPT that record with
#     `submodule_path` deleted while `verify-openxwallet-pin.py:194` REFUSES it.
#     Task 3.3(p)'s measurement says the same thing from the other side, listing
#     `source_repository` among that record's NINE non-table members.
#   - an UNKNOWN pin id — a fixture, an added `contracts/<anything>-pin.yaml`,
#     any future product — keeps the ALTERNATION: either WELL-FORMED spelling
#     satisfies the entry (a present spelling in the wrong form is MALFORMED, as
#     any present-and-malformed member is), a record may carry both, and a
#     record carrying NEITHER is refused, which is the failure the
#     design names ("the INTERSECTION would admit a record naming no product at
#     all"). Selecting the regime by the PRESENCE of `submodule_path` instead
#     would be the record choosing again, and would accept the deletion above.
_PRODUCT_IDENTITY = Member(
    spellings=("submodule_path", "source_repository"),
    form=_is_text,
    citations=(Citation(_OPENXWALLET, 194, guard="_submodule_path"),
               Citation(_OPENREPOSHAPE, 258, guard="_source_repository")),
    forms={"submodule_path": _is_text,
           "source_repository": _is_source_repository})


@dataclass(frozen=True)
class Shape:
    key: str
    label: str
    revision_kinds: tuple[str, ...]
    required: tuple[Member, ...]
    optional: tuple[Member, ...] = ()

    @property
    def title(self) -> str:
        return f"shape ({self.key}) {self.label}"


SHAPE_A = Shape(
    key="a",
    label="the enumerated commit-pinned source pin",
    revision_kinds=(COMMIT_REVISION_KIND,),
    required=(
        Member(("revision_kind",), _exactly(COMMIT_REVISION_KIND),
               (Citation(_OPENXWALLET, 219, guard="_pinned_commit"),
                Citation(_OPENREPOSHAPE, 239, guard="pinned_commit"))),
        Member(("commit",), _is_commit,
               (Citation(_OPENXWALLET, 227, guard="_pinned_commit"),
                Citation(_OPENREPOSHAPE, 247, guard="pinned_commit"))),
        _PRODUCT_IDENTITY,
        Member(("files",), _is_files_list,
               (Citation(_OPENXWALLET, 392, quote=_FILES_REFUSAL,
                         quote_line=396),
                Citation(_OPENREPOSHAPE, 438, quote=_FILES_REFUSAL,
                         quote_line=442))),
    ),
    # NOT refused-when-absent at either guard, and therefore NOT required —
    # both read it with an absent-is-empty default — but refused when PRESENT
    # and of the wrong form. A table that demanded it would refuse a record
    # those guards admit.
    # The citations carry NO guard: each verifier reads this member with an
    # absent-is-empty default, so there is nothing for the equivalence test's
    # guard leg to call — the leg ranges over the REQUIRED table, which is what
    # "the shape-guard-required set" names.
    optional=(
        Member(("pinned_by_commit_only",), _is_path_only_list,
               (Citation(_OPENXWALLET, 443), Citation(_OPENREPOSHAPE, 487))),
    ))

SHAPE_B = Shape(
    key="b",
    label="the whole-tree digest commit-pinned source pin",
    revision_kinds=(COMMIT_REVISION_KIND,),
    required=(
        Member(("submodule_path",), _is_text,
               (Citation(_OPENDOX, 215, guard="_submodule_path"),
                Citation(_OPENXDOX, 257, guard="_submodule_path"))),
        Member(("revision_kind",), _exactly(COMMIT_REVISION_KIND),
               (Citation(_OPENDOX, 226, guard="_pinned_commit"),
                Citation(_OPENXDOX, 276, guard="_pinned_commit"))),
        Member(("commit",), _is_commit,
               (Citation(_OPENDOX, 234, guard="_pinned_commit"),
                Citation(_OPENXDOX, 284, guard="_pinned_commit"))),
        Member(("digest_algorithm",), _exactly(DIGEST_ALGORITHM),
               (Citation(_OPENDOX, 246, guard="_pinned_tree_digest"),
                Citation(_OPENXDOX, 307, guard="_pinned_tree_digest"))),
        Member(("digest_definition",), _exactly(DIGEST_DEFINITION),
               (Citation(_OPENDOX, 253, guard="_pinned_tree_digest"),
                Citation(_OPENXDOX, 314, guard="_pinned_tree_digest"))),
        Member(("digests",), _is_digests_mapping,
               (Citation(_OPENDOX, 262, guard="_pinned_tree_digest"),
                Citation(_OPENXDOX, 322, guard="_pinned_tree_digest")),
               nested="tree_sha256"),
    ))

SHAPE_C = Shape(
    key="c",
    label="the published-artifact pin",
    revision_kinds=CONTENT_ADDRESSED_KINDS,
    required=(
        Member(("revision_kind",), _one_of(CONTENT_ADDRESSED_KINDS),
               (Citation(_OPENSPEC_CLI, 599, guard="pinned_version"),)),
        Member(("version",), _is_version,
               (Citation(_OPENSPEC_CLI, 608, guard="pinned_version"),)),
        Member(("integrity",), _is_integrity,
               (Citation(_OPENSPEC_CLI, 626, guard="pinned_integrity"),)),
        Member(("shasum",), _is_shasum,
               (Citation(_OPENSPEC_CLI, 653, guard="pinned_integrity"),)),
        Member(("package",), _is_package,
               (Citation(_OPENSPEC_CLI, 665, guard="pinned_package"),)),
        Member(("lockfile",), _is_lockfile_name,
               (Citation(_OPENSPEC_CLI, 705, guard="pinned_lockfile"),)),
        Member(("lockfile_integrity",), _is_integrity,
               (Citation(_OPENSPEC_CLI, 715, guard="pinned_lockfile"),)),
        Member(("lockfile_packages",), _is_lockfile_packages,
               (Citation(_OPENSPEC_CLI, 738, guard="pinned_lockfile"),)),
        Member(("binary",), _is_binary,
               (Citation(_OPENSPEC_CLI, 755, guard="pinned_binary"),)),
    ),
    # Absent-is-empty at its guard (`:801-803`), so NOT required and not on the
    # guard leg; refused only when PRESENT and not a list.
    optional=(
        Member(("dispositions",), _is_disposition_list,
               (Citation(_OPENSPEC_CLI, 808),)),
    ))

SHAPES: tuple[Shape, ...] = (SHAPE_A, SHAPE_B, SHAPE_C)

#: The verifier this checker TRACKS for each pin id — the script whose guards
#: the citations above were measured from. COMPARED against a record's
#: `verify_pin:` and NEVER followed: a differing value is a controlled finding
#: BESIDE the resolution, never a redirection (design D-2, task 3.3(n)). A pin id
#: this table does not carry has no expectation, so it yields no disagreement.
TRACKED_VERIFIERS: dict[str, str] = {
    "openxwallet": _OPENXWALLET,
    "openreposhape": _OPENREPOSHAPE,
    "opendox": _OPENDOX,
    "openxdox": _OPENXDOX,
    "openspec-cli": _OPENSPEC_CLI,
}

#: WHICH PRODUCT-IDENTITY SPELLING SHAPE (a) REQUIRES OF A KNOWN PIN — the
#: record grain, held in code beside the verifier map and keyed by the same pin
#: id, never read out of the record. `submodule_path` for a submodule-mounted
#: product (`scripts/verify-openxwallet-pin.py:194`, `_submodule_path`) and
#: `source_repository` for one resolved from its host
#: (`scripts/validate-openreposhape-pin.py:258`, `_source_repository`); neither
#: verifier reads the other's member. A pin id absent from this map gets the
#: alternation — see `_PRODUCT_IDENTITY`'s two regimes. Only shape-(a) pins
#: appear here: the other shapes name their identity member outright.
PRODUCT_IDENTITY_BY_PIN: dict[str, str] = {
    "openxwallet": "submodule_path",
    "openreposhape": "source_repository",
}

# ---------------------------------------------------------------------------
# The judgement
# ---------------------------------------------------------------------------

MISSING = "missing"
MALFORMED = "malformed"
MIXED = "mixed"
UNKNOWN_REVISION_KIND = "unknown-revision-kind"
NOT_A_MAPPING = "not-a-mapping"


@dataclass(frozen=True)
class Failure:
    shape: str | None          # the shape TRIED, or None where none could be
    member: str
    defect: str

    def render(self) -> str:
        where = f"{self.shape}: " if self.shape else ""
        return f"{where}`{self.member}` {self.defect}"


@dataclass(frozen=True)
class Verdict:
    shape: Shape | None
    failures: tuple[Failure, ...]

    @property
    def accepted(self) -> bool:
        return self.shape is not None and not self.failures

    def render(self) -> str:
        """The failing members, shape by shape, for a finding's rule text."""
        return "; ".join(failure.render() for failure in self.failures)

    def names(self, member: str) -> bool:
        return any(member in failure.member for failure in self.failures)


def required_spellings(member: Member, pin_id: str | None) -> tuple[str, ...]:
    """The spellings THIS PIN's table entry requires, at the record grain.

    One for every single-spelling member. For shape (a)'s product-identity
    entry: the spelling `PRODUCT_IDENTITY_BY_PIN` holds for a KNOWN pin id —
    its own verifier's member, the other spelling being non-table for that
    record — and BOTH for an unknown one, where the entry is an alternation:
    MISSING only when NEITHER spelling is present, and any spelling that IS
    present is judged by its own form, a present-but-malformed one being
    MALFORMED exactly as an optional member present in the wrong form is. See
    `_PRODUCT_IDENTITY`'s two regimes.
    """
    if len(member.spellings) == 1:
        return member.spellings
    required = PRODUCT_IDENTITY_BY_PIN.get(pin_id)
    if required in member.spellings:
        return (required,)
    return member.spellings


def _first_failure(shape: Shape, record: dict,
                   pin_id: str | None = None) -> Failure | None:
    for member in shape.required:
        spellings = required_spellings(member, pin_id)
        present = [name for name in spellings if name in record]
        if not present:
            return Failure(shape.title, " or ".join(spellings), MISSING)
        for name in present:
            if not member.form_for(name)(record.get(name)):
                return Failure(shape.title, name, MALFORMED)
        if member.nested is not None:
            holder = record.get(member.spellings[0])
            if member.nested not in holder:
                return Failure(shape.title,
                               f"{member.spellings[0]}.{member.nested}", MISSING)
            if not _is_tree_digest(holder.get(member.nested)):
                return Failure(shape.title,
                               f"{member.spellings[0]}.{member.nested}",
                               MALFORMED)
    for member in shape.optional:
        for name in member.spellings:
            if name in record and not member.form_for(name)(record.get(name)):
                return Failure(shape.title, name, MALFORMED)
    return None


def _carries_tree_digest(record: dict) -> bool:
    digests = record.get("digests")
    return isinstance(digests, dict) and "tree_sha256" in digests


def shapes_for(record: dict) -> tuple[Shape, ...]:
    """The shapes a record's `revision_kind` admits, in table order."""
    revision_kind = record.get("revision_kind")
    return tuple(shape for shape in SHAPES
                 if revision_kind in shape.revision_kinds)


def judge(record, pin_id: str | None = None) -> Verdict:
    """Is `record` a COMPLETE record of an ADMITTED SHAPE? Pure; reads nothing.

    The caller has already established that the record is a mapping declaring
    `kind: pinned_contract_manifest` — that precondition is gated on BEFORE any
    shape is selected, which is why `kind` is a member of no shape's table.

    `pin_id` is the identifier the MARKER named and the registry stem carries —
    an input of this function, never a member read out of the record. It selects
    nothing but a TABLE ROW: shape (a)'s product-identity spelling for a pin this
    checker has measured (`PRODUCT_IDENTITY_BY_PIN`), which is how the entry
    resolves AT THE RECORD GRAIN without the record choosing its own judge. Omit
    it — or pass one this checker does not know — and that entry is the
    alternation instead. Every other row is the same for every caller, and the
    function stays pure: same two inputs, same verdict.
    """
    if not isinstance(record, dict):
        return Verdict(None, (Failure(None, "record", NOT_A_MAPPING),))

    # THE MIXTURE, REFUSED BEFORE EITHER SHAPE IS TRIED. A record carrying both a
    # whole-tree `digests.tree_sha256` and a `files:` list matches neither (a)
    # nor (b): `neutral-product-pin`'s ratified text is SILENT on the whole-tree
    # shape — the spellings `digest_definition`, `digests` and `tree_sha256`
    # occur nowhere under `openspec/specs/` — so no text admits the mixture and
    # that capability's own fail-closed rule governs (`spec.md:89`). Refused
    # NAMING BOTH SHAPES TRIED rather than resolving on the strength of
    # whichever half is complete.
    if record.get("revision_kind") == COMMIT_REVISION_KIND \
            and _carries_tree_digest(record) and "files" in record:
        return Verdict(None, (Failure(SHAPE_A.title, "digests.tree_sha256", MIXED),
                              Failure(SHAPE_B.title, "files", MIXED)))

    candidates = shapes_for(record)
    if not candidates:
        return Verdict(None, (Failure(
            None, "revision_kind",
            MISSING if "revision_kind" not in record
            else UNKNOWN_REVISION_KIND),))

    failures = []
    for shape in candidates:
        failure = _first_failure(shape, record, pin_id)
        if failure is None:
            return Verdict(shape, ())
        failures.append(failure)
    return Verdict(None, tuple(failures))


# ---------------------------------------------------------------------------
# The capability enumeration — the SECOND and THIRD prerequisites
# ---------------------------------------------------------------------------

ENUMERATION_MEMBER = "capabilities"

#: A capability name takes the same kebab-case shape an in-tree capability id
#: takes — measured to be the shape of every capability id under
#: `openspec/specs/`.
CAPABILITY_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

ABSENT = "absent"
WELL_FORMED = "well-formed"


@dataclass(frozen=True)
class Enumeration:
    state: str                       # ABSENT | MALFORMED | WELL_FORMED
    names: tuple[str, ...] = ()
    detail: str = ""

    def carries(self, capability: str) -> bool:
        return capability in self.names


def enumeration(record: dict) -> Enumeration:
    """The record's OWN capability enumeration — ONE NAMED MEMBER, not a search.

    The resolver reads a top-level `capabilities:` sequence and NOTHING ELSE. It
    does not go looking for `files:`, `digests:` or `pinned_members:` and read
    capability names out of them: none of those is a capability list, and
    guessing between them is exactly the non-determinism the prerequisite exists
    to remove.

    ABSENT and MALFORMED are TWO states with ONE outcome, and they are kept apart
    because their remedies differ: a malformed member is REPAIRED by whoever
    wrote it, an absent one is PUBLISHED by the pinned product's publisher. An
    EMPTY sequence is MALFORMED and not absent — it is not a statement that the
    product has no capabilities, it is a broken member.
    """
    if ENUMERATION_MEMBER not in record:
        return Enumeration(ABSENT)
    raw = record.get(ENUMERATION_MEMBER)
    if not isinstance(raw, list):
        return Enumeration(MALFORMED,
                           detail=f"it is {type(raw).__name__} and not a sequence")
    if not raw:
        return Enumeration(MALFORMED, detail="it is an empty sequence")
    for item in raw:
        if not isinstance(item, str) or not CAPABILITY_RE.fullmatch(item):
            return Enumeration(
                MALFORMED,
                detail=f"it carries {item!r}, which is not a capability name")
    return Enumeration(WELL_FORMED, tuple(raw))
