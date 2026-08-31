"""Public model-catalog types and the narrow provider port for doxBench chat
(010-doxbench-editor-chat T013/T020; data-model.md Section 6,
contracts/model-catalog.md, research.md R6/R9, plan.md Constraints).

This module owns exactly five things:

* the immutable public catalog shape (``ModelCatalogEntry`` / ``ModelCatalog``);
* the PURE projection of a catalog into the RELEASED
  ``workbench-model-catalog`` wire envelope (``catalog_wire_envelope``), added
  once the additive openxFactory schema was released and pinned at
  contract-v1.27 (``d09d5820de5b63b9528f6baea884a6dccde9b158``), grown at
  contract-v1.38 to carry a ROUTING RULE's declaration (task 11.7) and at
  contract-v2.2 to carry an entry's INPUT-MODALITY declaration
  (add-model-capability-vocabulary);
* the pure byte-limit arithmetic a turn must apply before disclosure
  (``effective_limit_bytes``);
* the narrow ``WorkbenchModelPort`` seam (research R6) plus its
  deterministic ``FakeWorkbenchModelPort`` -- the ONLY adapter this slice
  defines. There is no real provider adapter here and none is implied;
* ``dispatch_turn`` (T049): the ONE boundary that hands an assembled prompt
  envelope to an adapter and maps every provider outcome -- unavailable
  model, deadline overrun, adapter failure, malformed or oversize output --
  to a FIXED, redacted refusal. Timeout enforcement takes an INJECTED
  monotonic ``clock`` callable so this module needs no ``time`` import and
  every test stays hermetic and sleep-free (research R14).

Deliberately absent, and deferred to later tasks (see each name's own
docstring for the exact task):

* typed-proposal validation -- T061 (doxbench_turns.py, US3) owns it;
  until it lands ``dispatch_turn`` REFUSES any proposal-bearing response
  (fail closed), so nothing unvalidated can pass through this seam;
* the route-side dispatch arm (T051): ``serve.py`` decides when a turn may
  reach ``dispatch_turn`` at all, and its production posture stays
  refused-by-absence until an approved deployment adapter exists (T099);
* catalog sorting, default selection, and freshness/revalidation timing --
  declared gaps in checklists/provider-boundary.md (CHK005/CHK006), not
  invented here.

Pure standard library only: ``dataclasses`` and ``typing``. Nothing in this
file reaches a network, reads an environment variable, spawns a process, or
holds a credential-shaped value of any kind.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

# ---------------------------------------------------------------------------
# constants (plan.md "Constraints")
# ---------------------------------------------------------------------------

# "Provider calls have an adapter-declared timeout no greater than 120
# seconds."
MAX_ADAPTER_TIMEOUT_SECONDS = 120

# "The route-specific request maximum is 1,048,576 UTF-8 bytes." This is the
# SAME number serve.py declares as its own route-specific request bound
# (T024's per-route cap, not the global tile-action cap); the companion test
# suite pins the two constants together so they cannot drift apart. This
# module does not reference serve.py directly -- the pin is a test-side
# equality check only.
SERVER_MAX_INPUT_LIMIT_BYTES = 1_048_576

# "total validated response content is at most 900,000 bytes."
SERVER_MAX_OUTPUT_LIMIT_BYTES = 900_000

# "Assistant prose is at most 65,536 bytes." The SAME number
# doxbench_turns.py declares as MAX_ASSISTANT_PROSE_BYTES; that module
# imports from this one, so the constant is restated here rather than
# imported (no cycle) and the companion test pins the two spellings equal.
MAX_ASSISTANT_PROSE_BYTES = 65_536

# The exact, ordered public-field allowlist (data-model.md Section 6,
# contracts/model-catalog.md). These seven are the REQUIRED base every entry
# carries, and they are what a plain entry's public dict holds -- exactly, in
# this order, and nothing else.
PUBLIC_ENTRY_FIELDS: tuple[str, ...] = (
    "model_id",
    "label",
    "provider_class",
    "available",
    "input_limit_bytes",
    "output_limit_bytes",
    "data_handling",
)

# The ROUTING-RULE declaration (contract-v1.38, add-doxbench-editing-phase-b
# task 11.7). Optional, and all three travel together: a routing entry declares
# every one of them, a plain entry declares none. They are disclosed only by an
# entry that IS a routing rule -- see ``ModelCatalogEntry.as_public_dict`` for
# why present-only-when-declared rather than always-present-with-defaults.
ROUTING_ENTRY_FIELDS: tuple[str, ...] = (
    "routing_rule",
    "routes_to",
    "resolved_model_id",
)

# The CAPABILITY declaration (contract-v2.2, add-model-capability-vocabulary).
# One optional field saying WHAT KIND of input a model accepts, disclosed only
# by an entry that actually declares it -- the same present-only-when-declared
# idiom the routing fields use, and for the same reason: an entry that declares
# nothing projects the bytes it always projected.
CAPABILITY_ENTRY_FIELDS: tuple[str, ...] = (
    "modalities",
)

# Every key any public dict this module produces may hold, in projection order.
# Nothing outside this tuple may ever appear.
#
# THE BASE SEVEN STAY A PREFIX. That is the property callers rely on, and it is
# the one asserted; the capability group was INSERTED between the base seven and
# the routing three rather than appended after them, so the routing keys did
# move within this tuple. Nothing indexes it, and each optional group is still
# emitted only by an entry that declares it, so a plain entry's projection is
# unchanged either way.
DECLARABLE_ENTRY_FIELDS: tuple[str, ...] = (
    PUBLIC_ENTRY_FIELDS + CAPABILITY_ENTRY_FIELDS + ROUTING_ENTRY_FIELDS
)

# ---- the CLOSED input-modality vocabulary (contract-v2.2) ----
#
# Exactly two members, and the set EXTENDS ONLY BY THE CHANGE THAT GOVERNS A NEW
# MEMBER -- the rule the client-identity roster's `admission_surface` states.
# `image` is here because a turn carrying an image is the named near-term
# consumer; audio, video, tool-calling, structured output, latency class and
# cost class are not, because nothing consumes them and a vocabulary guessed
# ahead of its consumers is one nothing validates against.
#
# RESTATED from the released schema's `items.enum`, not read from it, for the
# reason every bound in this module is restated: the whole import list is
# `dataclasses` and `typing`, so this module cannot open the schema. The
# companion test reads the RELEASED BYTES and pins these equal to them.
CATALOG_MODALITIES: tuple[str, ...] = ("text", "image")

# The member the released schema's `contains: {const: text}` requires wherever
# the field is declared. A chat turn always carries text, so a model that cannot
# accept text is not a model this catalog can route a turn to at all.
REQUIRED_MODALITY = "text"

# ---- the routing badge's SEGMENT GRAMMAR (contract-v1.38, adversarial review
# round 1 F1) ----
#
# A routing rule's `data_handling` is a SEPARATOR-JOINED LIST of badge segments,
# and the covering rule is SEGMENT MEMBERSHIP: each routed model's own badge must
# be one of those segments. It is NOT substring containment, which the review
# broke twice on the released bytes -- a rule badged "Routes to a non-tenant
# endpoint." was accepted as carrying a target badged "on-tenant" (the menu then
# shows the INVERSE of the target's posture), and a rule ending "...retain
# nothing." was accepted as carrying a target badged "retain".
#
# The separator is SPACE SLASH SPACE. Chosen because a badge is free prose and
# any separator can collide with it: `;` `.` `,` all occur in the packaged
# badges, `/` does not. The collision that remains is refused rather than hoped
# away -- a target badge that itself contains the separator cannot BE a segment,
# so `ModelCatalog` refuses that catalog (see `_validate_routing_targets`).
#
# This spelling is restated in `scripts/validate-ideation-dashboard-contracts.py`
# (a standalone validator that imports nothing from this package, the same
# convention `RESERVED_BUFFER_KEYS` follows) and a companion test pins the two
# equal, so the two gates cannot drift into two grammars.
# The released schema's `maxItems` on `routes_to`. RESTATED, not read: this
# module's whole import list is `dataclasses` and `typing`, so it cannot open the
# schema -- the same reason `SERVER_MAX_INPUT_LIMIT_BYTES` is a literal here. The
# companion test reads the RELEASED BYTES and pins this equal to them, so the two
# cannot drift; that pin, not this literal, is what makes the bound authoritative.
MAX_ROUTING_TARGETS = 64

# ...and its OPERATIVE maximum is 63, not 64. `models` is itself capped at 64,
# and a routing rule occupies one of those slots, so the largest routable set a
# WIRE-CONFORMANT catalog can express is rule + 63 targets. 64 is the right
# number to enforce here -- it is `routes_to`'s own bound -- but a reader
# reasoning about real catalogs should reason about 63. Since contract-v2.2 the
# catalog-level bound is enforced too, by `MAX_CATALOG_ENTRIES` below, so a
# 65-entry catalog no longer constructs and the "wire-conformant" qualifier is
# now redundant rather than load-bearing.

# The released schema's `models.maxItems`. Enforced at contract-v2.2
# (add-model-capability-vocabulary, Brett's ALL-FIVE ruling of 2026-08-24 and
# the batched follow-up it rode with): before it, a 65-entry catalog constructed
# cleanly in process while `GET /workbench/model-catalog` refused to serve the
# very catalog holding it, because the route validates the projected envelope
# against the released schema. RESTATED, not read, for the reason every bound in
# this module is restated, and pinned to the released bytes by the companion
# test.
MAX_CATALOG_ENTRIES = 64

# The released schema's `items.maxLength` / `items.pattern` on `routes_to`, which
# `resolved_model_id` and `model_id` all repeat. RESTATED for the same reason the
# cap is, and pinned to the released bytes by the same companion test.
MODEL_REFERENCE_MAX_LENGTH = 128
MODEL_REFERENCE_PATTERN = "^[A-Za-z0-9][A-Za-z0-9._-]*$"

# The released schema's `maxLength` on the three DESCRIPTIVE string fields.
# Enforced at contract-v2.2; before it each was checked for blankness alone, so
# 201-, 65- and 501-character values all constructed while the wire refused
# them. After this release EVERY string bound the released schema declares is
# enforced at construction, with no residue -- which is what makes the parity
# requirement checkable rather than aspirational, and what the schema-driven
# companion test asserts by walking the released `$defs/model_entry` rather than
# by listing these four names a second time.
LABEL_MAX_LENGTH = 200
PROVIDER_CLASS_MAX_LENGTH = 64
DATA_HANDLING_MAX_LENGTH = 500


def _is_conformant_model_reference(value: str) -> bool:
    """``MODEL_REFERENCE_PATTERN``, evaluated WITHOUT importing ``re``.

    This module's whole import list is ``dataclasses`` and ``typing`` and the
    docstring at the top says so; a regex import to check four character classes
    would be the wrong trade. The pattern is "one ASCII alphanumeric, then ASCII
    alphanumerics and ``. _ -``", which is exactly what this evaluates -- the
    ``isascii()`` guards matter, because ``str.isalnum()`` is True for plenty of
    non-ASCII characters the released pattern refuses.

    The equivalence is not asserted by eye: the companion test reads the pattern
    out of the RELEASED BYTES, pins it equal to the constant above, and exercises
    this predicate against the boundary cases."""
    if not value:
        return False
    head, tail = value[0], value[1:]
    if not (head.isascii() and head.isalnum()):
        return False
    return all(c.isascii() and (c.isalnum() or c in "._-") for c in tail)


def _require_model_reference(field: str, value: object) -> None:
    """A model id, held to the released schema's own bounds.

    Applied to ALL THREE id-bearing fields since contract-v2.2: ``model_id``
    itself, ``routes_to`` members and ``resolved_model_id``. The released schema
    gives every one of them the same ``maxLength: 128`` and the same character
    pattern, so one spelling holds all three.

    ``model_id`` JOINED THEM at contract-v2.2 (review N7, closed). It had
    accepted over-length and out-of-pattern values since the seven-field type
    shipped, and the deferral reason recorded here was that tightening it "would
    be a behaviour change belonging to no release". That release arrived: the
    change that added ``modalities`` opened ``$defs/model_entry`` and this
    construction gate anyway, so the fix rode with it at no additional release
    surface. What changes is WHERE such an id fails, not whether -- it was
    always unservable, because the route validates the projected envelope
    against the released schema."""
    _require_non_blank_str(field, value)
    if len(value) > MODEL_REFERENCE_MAX_LENGTH:
        raise InvalidCatalogEntryError(
            f"{field} is {len(value)} characters, above the "
            f"{MODEL_REFERENCE_MAX_LENGTH} the released catalog schema permits")
    if not _is_conformant_model_reference(value):
        raise InvalidCatalogEntryError(
            f"{field} {value!r} does not match the released catalog schema's "
            f"model-id pattern {MODEL_REFERENCE_PATTERN}")

ROUTING_BADGE_SEPARATOR = " / "

# The closed set of trailing characters a segment comparison ignores. See
# `normalized_badge_segment` for why these three and nothing else.
ROUTING_BADGE_TRAILING_PUNCTUATION = ".;,"


def normalized_badge_segment(text: object) -> str:
    """One badge segment, in the form the covering rule compares.

    THREE normalizations, each chosen because it cannot make two DIFFERENT
    handling postures compare equal (adversarial review round 1 F1 called the
    byte-exact comparison over-strict in the harmless direction):

    * whitespace runs collapse and the ends are stripped, so a badge copied
      across a line wrap still matches;
    * case is folded, so `ON-TENANT` matches `on-tenant`;
    * trailing characters in ``ROUTING_BADGE_TRAILING_PUNCTUATION`` are
      dropped, so a rule that joins badges into a sentence and loses or gains a
      full stop still matches.

    DELIBERATELY NOT normalized: anything that removes or rewrites INTERIOR
    characters. Hyphens, negations and stop words all stay, because that is
    exactly where the difference between `on-tenant` and `non-tenant` lives --
    the pair the review used to break the old predicate. A normalization that
    could flip a posture would be worse than no normalization at all.

    ONE PRECISION on "interior characters are never rewritten" (review re-verify
    N2): ``casefold`` IS an interior rewrite for the multi-character folds --
    German sharp s becomes `ss`, the `ﬁ` ligature becomes `fi`, and a handful of
    others expand rather than merely lowercase. The claim is therefore not that
    no byte inside a segment ever changes; it is that no fold CASEFOLD PERFORMS
    can separate or merge two handling POSTURES. Every such fold maps
    case-or-orthography variants of the same word onto one form, which is the
    property being relied on -- none of them adds, removes or negates a word, so
    none can turn a posture into a different one. If a future normalization step
    is added, that is the test it has to pass, not "leaves the bytes alone"."""
    collapsed = " ".join(str(text).split()).casefold()
    return collapsed.rstrip(ROUTING_BADGE_TRAILING_PUNCTUATION).strip()


def badge_segments(data_handling: object) -> tuple[str, ...]:
    """A rule's declared badge, split into normalized segments.

    Empty segments are dropped: a trailing or doubled separator is sloppy
    authoring, not a segment that anything may match."""
    return tuple(
        segment
        for segment in (
            normalized_badge_segment(part)
            for part in str(data_handling).split(ROUTING_BADGE_SEPARATOR)
        )
        if segment
    )

# ---- the RELEASED catalog wire envelope (T020 wire clause) ----
#
# `xfactory-workbench-model-catalog.schema.yaml` at contract-v1.27
# (`d09d5820de5b63b9528f6baea884a6dccde9b158`) is the AUTHORITY for these two
# discriminators; ``doxbench_contracts`` is where those bytes are loaded,
# digest-verified, and enforced. They are restated here as constants for one
# reason only: this module must stay import-free of any schema library (its
# whole import list is ``dataclasses`` and ``typing``), so the projection
# cannot read the schema itself. The companion test pins
# ``CATALOG_WIRE_KIND == doxbench_contracts.KIND_MODEL_CATALOG``, so the two
# spellings cannot drift, and the route validates every produced envelope
# against the released schema before it reaches a client -- this constant is
# never the last word on conformance.
CATALOG_WIRE_SCHEMA_VERSION = 1
CATALOG_WIRE_KIND = "workbench-model-catalog"

# The released envelope's exact, ordered key set. Three keys, closed.
WIRE_ENVELOPE_FIELDS: tuple[str, ...] = ("schema_version", "kind", "models")


# ---------------------------------------------------------------------------
# errors
# ---------------------------------------------------------------------------


class ModelCatalogError(ValueError):
    """Base class for every catalog-shaped refusal this module raises."""


class InvalidCatalogEntryError(ModelCatalogError):
    """A single ``ModelCatalogEntry`` field failed value-level validation
    (blank/whitespace-only string, non-positive limit, or a limit above the
    server cap). Wrong Python types raise ``TypeError`` instead -- see
    ``ModelCatalogEntry.__post_init__`` for the exact split."""


class CatalogEntryCountError(ModelCatalogError):
    """A catalog declares more entries than the released schema's
    ``models.maxItems`` permits (contract-v2.2).

    A WHOLE-CATALOG refusal, and its own class for the same reason
    ``DuplicateModelIdError`` is: no single entry is wrong, so
    ``InvalidCatalogEntryError`` -- whose docstring says "a single
    ``ModelCatalogEntry`` field failed value-level validation" -- would be a
    false statement about what happened. The split this module keeps is by HOW
    MUCH CONTEXT THE REFUSAL NEEDS, and this one needs the whole list.

    Not ``InvalidRoutingRuleError`` either: that class's first sentence is that
    every member of it is a routing inconsistency, and an over-large catalog of
    plain entries is not one."""


class DuplicateModelIdError(ModelCatalogError):
    """Two entries in one catalog share a ``model_id`` (data-model.md
    Section 6: ``model_id`` is unique). Raised by
    ``ModelCatalog.__post_init__`` -- for both ``ModelCatalog.from_entries(...)``
    and a direct ``ModelCatalog(entries=...)`` construction; the whole
    catalog refuses rather than dropping the later entry."""


class InvalidRoutingRuleError(ModelCatalogError):
    """A routing declaration is not consistent with the catalog it sits in
    (contract-v1.38). ONE class for every CROSS-ENTRY routing refusal, and the
    list is exhaustive -- an incomplete one is what the PR #244 bot round caught
    here. Raised for:

    1. a ``routes_to`` reference no entry in this catalog answers to;
    2. a target that is itself a routing rule (no chained resolution);
    3. a target whose own ``data_handling`` this rule's badge does not carry as
       a SEGMENT (the covering rule);
    4. a target whose badge holds the segment separator, so it could never BE a
       segment -- a DIAGNOSTIC arm, since (3) would refuse the same catalog
       under a message that misdirects;
    5. an AVAILABLE rule whose declared limits exceed those of the model it
       resolves to (rule 5', Brett's ruling 2026-08-21);
    6. an AVAILABLE rule resolving to a model that is not available.

    They share one consequence: this catalog cannot honestly offer this routing
    rule, so the whole catalog refuses rather than serving a menu entry that
    misstates what it routes to.

    EVERY ONE OF THE SIX NEEDS A SECOND ENTRY TO SEE, which is what makes
    "cross-entry" the honest framing rather than a label. PER-ENTRY routing
    inconsistencies are ``InvalidCatalogEntryError`` instead -- the three fields
    not travelling together, a rule naming itself, a resolved id outside
    ``routes_to``, a repeated target, and ``routes_to`` above the released
    schema's 64-target cap. They need no second entry, exactly like a blank
    label or an over-cap ``input_limit_bytes``, and the cap is precisely that:
    an over-cap value on one field of one entry.

    (Codex's P2 suggested raising the cap as an ``InvalidRoutingRuleError``.
    Declined, and flagged: doing so would make this class's own first sentence
    false, since the cap is visible without a catalog at all. The split is by
    HOW MUCH CONTEXT THE REFUSAL NEEDS, not by which field it names.)"""


class AdapterTimeoutError(ValueError):
    """A declared adapter timeout violates ``0 < value <=
    MAX_ADAPTER_TIMEOUT_SECONDS``. Raised by ``validated_timeout_seconds``
    for every failure mode -- wrong type, boolean, non-finite, zero,
    negative, or over the cap -- so callers have exactly one exception to
    catch for "this declared timeout cannot be honoured"."""


# ---------------------------------------------------------------------------
# ModelCatalogEntry / ModelCatalog
# ---------------------------------------------------------------------------


def _require_non_blank_str(field: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a str, got {type(value).__name__}")
    if not value.strip():
        raise InvalidCatalogEntryError(f"{field} must not be blank")


def _require_bounded_str(field: str, value: object, maximum: int) -> None:
    """A non-blank string held to the released schema's ``maxLength`` for its
    field (contract-v2.2).

    The three DESCRIPTIVE fields -- ``label``, ``provider_class`` and
    ``data_handling`` -- were checked for blankness alone until this release, so
    a 201-, 65- or 501-character value constructed cleanly while
    ``GET /workbench/model-catalog`` refused to serve the catalog holding it.
    The id-bearing fields take ``_require_model_reference`` instead, which adds
    the character pattern those three do not carry."""
    _require_non_blank_str(field, value)
    if len(value) > maximum:
        raise InvalidCatalogEntryError(
            f"{field} is {len(value)} characters, above the {maximum} the "
            f"released catalog schema permits")


def _require_positive_capped_int(field: str, value: object, cap: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field} must be a non-bool int, got {type(value).__name__}")
    if value <= 0:
        raise InvalidCatalogEntryError(f"{field} must be strictly positive")
    if value > cap:
        raise InvalidCatalogEntryError(f"{field} must not exceed {cap}")


@dataclass(frozen=True, slots=True)
class ModelCatalogEntry:
    """One approved, selectable model choice as doxBench chat may disclose
    it to the browser (data-model.md Section 6). The seven REQUIRED fields
    below plus the three OPTIONAL routing-declaration fields are the whole
    public surface: nothing else may be constructed, because this dataclass
    is slotted and every extra keyword argument is a ``TypeError`` at
    construction.

    ``provider_class`` and ``data_handling`` are free-form, non-blank
    strings, not a closed enum: data-model.md Section 6 calls
    ``provider_class`` "enum/string" without naming the value set, and a
    fixture using one value (like the contract example's on-tenant posture)
    does not make it the only legal one.

    THE ROUTING DECLARATION (contract-v1.38, task 11.7). An entry may declare
    itself a ROUTING RULE -- an `auto` entry this capability resolves to a
    model by role -- rather than a directly answering provider model. The
    three fields travel together and their DEFAULTS are the plain-model
    posture, so every construction that predates this release means exactly
    what it always meant: ``routing_rule=False``, no routable set, no resolved
    id. Every rule enforced here mirrors the released schema's own
    (`$defs/model_entry`); the rules that need a SECOND entry to see -- a
    dangling target, a chained rule, an unavailable resolved model, the badge
    covering -- belong to ``ModelCatalog`` because that is the smallest scope
    that can answer them.

    THE MODALITY DECLARATION (contract-v2.2, add-model-capability-vocabulary).
    An entry MAY declare which input modalities it accepts, from the closed
    two-member vocabulary ``CATALOG_MODALITIES``. It is OPTIONAL and its default
    is ``None`` -- UNDECLARED, which is not a capability claim in either
    direction: an entry that declares nothing is a producer that predates the
    field. ``None`` and an EMPTY set are deliberately different values here,
    exactly as they are on the wire: the released schema has no key for the
    first and ``minItems: 1`` for the second, so ``modalities=()`` is a refusal
    rather than a synonym for absence.

    NOTHING IN THIS RELEASE READS THE DECLARATION TO CHOOSE A DESTINATION. The
    field is declared, validated and projected; fit-aware routing is exit (b) of
    the staged topic and consumes it. ``routing_modalities`` states the safe
    reading a router will apply, and ``declares_modalities`` keeps that
    conservative default distinguishable from a stated capability.

    NOT ON THIS TYPE, deliberately: the harness provider id. Task 11.6 placed
    it on ``LaunchConfig.provider_id``, the install-side declaration, precisely
    so a harness-routing fact could not be smuggled into a governance record;
    widening the entry does not reopen that ruling. `routes_to` and
    `resolved_model_id` name opaque CATALOG handles and nothing else."""

    model_id: str
    label: str
    provider_class: str
    available: bool
    input_limit_bytes: int
    output_limit_bytes: int
    data_handling: str
    modalities: tuple[str, ...] | None = None
    routing_rule: bool = False
    routes_to: tuple[str, ...] = ()
    resolved_model_id: str | None = None

    def __post_init__(self) -> None:
        # EVERY BOUND THE RELEASED SCHEMA DECLARES, enforced here (contract-v2.2,
        # Brett's ALL-FIVE ruling of 2026-08-24). `model_id` takes the reference
        # spelling because the schema gives it a character pattern as well as a
        # length; the three descriptive fields take the length alone, which is
        # all the schema declares for them.
        _require_model_reference("model_id", self.model_id)
        _require_bounded_str("label", self.label, LABEL_MAX_LENGTH)
        _require_bounded_str("provider_class", self.provider_class,
                             PROVIDER_CLASS_MAX_LENGTH)
        _require_bounded_str("data_handling", self.data_handling,
                             DATA_HANDLING_MAX_LENGTH)
        if not isinstance(self.available, bool):
            raise TypeError(
                f"available must be a bool, got {type(self.available).__name__}"
            )
        _require_positive_capped_int(
            "input_limit_bytes", self.input_limit_bytes, SERVER_MAX_INPUT_LIMIT_BYTES
        )
        _require_positive_capped_int(
            "output_limit_bytes", self.output_limit_bytes, SERVER_MAX_OUTPUT_LIMIT_BYTES
        )
        self._validate_modalities()
        self._validate_routing_declaration()

    def _validate_modalities(self) -> None:
        """The closed input-modality vocabulary (contract-v2.2).

        Three refusals, each one the released schema's own: a member outside the
        closed set (`items.enum`), an empty declared set (`minItems: 1`), and a
        declared set omitting ``text`` (`contains: {const: text}`). Plus the
        repeat the schema's ``uniqueItems`` refuses.

        ABSENCE IS ``None`` AND RETURNS EARLY, before any of them. That is the
        additive property at the type: every construction written before this
        release names no ``modalities`` and is judged exactly as it was."""
        if self.modalities is None:
            return
        if isinstance(self.modalities, (str, bytes)):
            raise TypeError(
                "modalities must be an iterable of modality names, not a "
                f"single {type(self.modalities).__name__}")
        try:
            declared = tuple(self.modalities)
        except TypeError as error:
            raise TypeError(
                "modalities must be an iterable of modality names, got "
                f"{type(self.modalities).__name__}") from error
        object.__setattr__(self, "modalities", declared)
        if not declared:
            raise InvalidCatalogEntryError(
                "a declared modality set must not be empty; omit the field "
                "entirely to declare nothing, which is not a claim in either "
                "direction")
        for member in declared:
            if not isinstance(member, str):
                raise TypeError(
                    "modalities members must be str, got "
                    f"{type(member).__name__}")
            if member not in CATALOG_MODALITIES:
                raise InvalidCatalogEntryError(
                    f"modalities member {member!r} is outside the closed "
                    f"vocabulary {list(CATALOG_MODALITIES)}; the vocabulary is "
                    "extended by the change that governs a new modality, never "
                    "by a wider field")
        if len(set(declared)) != len(declared):
            raise InvalidCatalogEntryError(
                "modalities must not repeat a member")
        if REQUIRED_MODALITY not in declared:
            raise InvalidCatalogEntryError(
                f"a declared modality set must contain {REQUIRED_MODALITY!r}: "
                "a chat turn always carries text, so a model that cannot "
                "accept text is not routable here")

    @property
    def declares_modalities(self) -> bool:
        """Whether this entry MADE a modality declaration at all.

        The half of the absence rule that must not be lost: a reader that only
        ever saw ``routing_modalities`` could not tell a conservative default
        from a stated capability, and the requirement says both facts are
        recorded."""
        return self.modalities is not None

    @property
    def routing_modalities(self) -> tuple[str, ...]:
        """The modality set a router READS for this entry -- the declared set,
        or ``("text",)`` where nothing was declared.

        THE SAFE READING, stated once so no consumer has to invent it: never
        route a turn carrying an image to a model that has not said it accepts
        images. This is a projection of the ratified absence rule and NOT a
        routing decision -- nothing in this release chooses a destination by it;
        exit (b) is where that happens."""
        if self.modalities is None:
            return (REQUIRED_MODALITY,)
        return self.modalities

    def _validate_routing_declaration(self) -> None:
        """The PER-ENTRY half of the contract-v1.38 routing rules, mirroring
        the released schema's `dependentRequired` and its two conditionals.

        ``routes_to`` is materialized to a ``tuple`` the same way
        ``ModelCatalog`` materializes its entries, so a caller's source list
        cannot mutate an entry after construction."""
        if not isinstance(self.routing_rule, bool):
            raise TypeError("routing_rule must be a bool, got "
                            f"{type(self.routing_rule).__name__}")
        if isinstance(self.routes_to, (str, bytes)):
            raise TypeError("routes_to must be an iterable of model ids, not a "
                            f"single {type(self.routes_to).__name__}")
        try:
            targets = tuple(self.routes_to)
        except TypeError as error:
            raise TypeError("routes_to must be an iterable of model ids, got "
                            f"{type(self.routes_to).__name__}") from error
        object.__setattr__(self, "routes_to", targets)
        for target in targets:
            _require_model_reference("routes_to member", target)
        if len(set(targets)) != len(targets):
            raise InvalidCatalogEntryError(
                "routes_to must not repeat a model id")
        # THE 64-TARGET CAP (Codex review of PR #244, P2). Without it the type
        # accepted a 65-member `routes_to` that the released schema refuses, so
        # the TYPE gate was weaker than the WIRE gate -- the F2 divergence in the
        # other direction. The consequence was concrete: such a rule constructed
        # fine and could be dispatched by the turn route (which checks only
        # `isinstance(catalog, ModelCatalog)`), while `GET /workbench/model-catalog`
        # refused to serve the very catalog holding it, because serve.py validates
        # the projected envelope against the released schema.
        #
        # `InvalidCatalogEntryError`, NOT `InvalidRoutingRuleError` -- see that
        # class's docstring for the split this keeps: one entry is enough to see
        # this, exactly like an over-cap `input_limit_bytes`.
        if len(targets) > MAX_ROUTING_TARGETS:
            raise InvalidCatalogEntryError(
                f"routes_to declares {len(targets)} models, above the "
                f"{MAX_ROUTING_TARGETS} the released catalog schema permits")
        if self.resolved_model_id is not None:
            _require_model_reference("resolved_model_id", self.resolved_model_id)
        # The three travel together, in both directions.
        if self.routing_rule is True:
            if not targets:
                raise InvalidCatalogEntryError(
                    "a routing_rule entry must declare the models it may route "
                    "to (routes_to)")
            if self.resolved_model_id is None:
                raise InvalidCatalogEntryError(
                    "a routing_rule entry must declare the model it currently "
                    "resolves to (resolved_model_id)")
            if self.model_id in targets:
                raise InvalidCatalogEntryError(
                    f"routing rule {self.model_id!r} must not route to itself")
            if self.resolved_model_id not in targets:
                raise InvalidCatalogEntryError(
                    f"resolved_model_id {self.resolved_model_id!r} is not among "
                    f"the models this rule declares it may route to")
            return
        if targets or self.resolved_model_id is not None:
            raise InvalidCatalogEntryError(
                "an entry that is not a routing rule must declare neither "
                "routes_to nor resolved_model_id")

    def as_public_dict(self) -> dict:
        """Exactly ``PUBLIC_ENTRY_FIELDS``, in that order, then ``modalities``
        WHEN AND ONLY WHEN this entry declared one, then
        ``ROUTING_ENTRY_FIELDS`` WHEN AND ONLY WHEN this entry is a routing
        rule. No version marker and no discriminator marker -- see the module
        docstring's deferral list.

        PRESENT-ONLY-WHEN-DECLARED, and that is a decision (task 11.7's tick
        flags it). The alternative -- always emitting the three keys with their
        plain-model defaults -- would change the bytes of every catalog
        response that exists, hand every consumer a `resolved_model_id: null`
        it never asked for, and put `routes_to: []` on entries the released
        schema forbids to carry it at all. Omission means what it has always
        meant, so a plain entry's public dict is byte-identical across the
        release boundary. The released schema tolerates BOTH producers: an
        explicit `routing_rule: false` with no siblings is valid there, it is
        simply not what this projection emits.

        ``modalities`` FOLLOWS THAT IDIOM, and projecting it at all is
        deliberate rather than automatic (contract-v2.2; the pre-ratification
        bot round found the gap). This method emits an EXPLICIT key list rather
        than serializing the dataclass, so a declared set would otherwise have
        been validated in process and then silently dropped by
        `GET /workbench/model-catalog` -- leaving consumers and the routing
        successor with nothing to read, which is the entire purpose of the
        field. An UNDECLARED entry emits no key, so its public dict stays
        byte-identical across this release boundary too. Absence on the wire
        carries exactly what absence carries here: no claim in either
        direction."""
        public = {
            "model_id": self.model_id,
            "label": self.label,
            "provider_class": self.provider_class,
            "available": self.available,
            "input_limit_bytes": self.input_limit_bytes,
            "output_limit_bytes": self.output_limit_bytes,
            "data_handling": self.data_handling,
        }
        if self.modalities is not None:
            # A LIST (JSON has no tuple), freshly built, so a caller mutating
            # the projection cannot reach the frozen entry.
            public["modalities"] = list(self.modalities)
        if self.routing_rule is True:
            public["routing_rule"] = True
            public["routes_to"] = list(self.routes_to)
            public["resolved_model_id"] = self.resolved_model_id
        return public


@dataclass(frozen=True, slots=True)
class ModelCatalog:
    """An ordered, duplicate-free collection of approved
    ``ModelCatalogEntry`` values. The invariants below hold for EVERY
    construction path, not only ``from_entries``: ``__post_init__`` coerces
    ``entries`` to an immutable ``tuple`` (so a caller's source list cannot
    mutate the catalog after construction), rejects any non-
    ``ModelCatalogEntry`` element, and rejects a repeated ``model_id`` --
    whether the catalog was built as ``ModelCatalog(entries=...)`` directly
    or through ``from_entries``. ``from_entries`` remains the
    intention-revealing constructor of choice; it is a thin wrapper around
    the dataclass constructor, not the only safe entry point.

    Since contract-v1.38 the same ``__post_init__`` also enforces the routing
    rules that need MORE THAN ONE entry to see -- see
    ``_validate_routing_targets``. A catalog holding an inconsistent routing
    declaration refuses as a whole, exactly as a duplicated ``model_id``
    refuses as a whole: a menu that misstates what an entry routes to is worse
    than no menu, and dropping the offending entry would leave the operator's
    declaration silently unserved."""

    entries: tuple[ModelCatalogEntry, ...]

    def __post_init__(self) -> None:
        materialized = tuple(self.entries)
        object.__setattr__(self, "entries", materialized)
        seen_ids: set[str] = set()
        for entry in materialized:
            if not isinstance(entry, ModelCatalogEntry):
                raise TypeError(
                    "catalog entries must be ModelCatalogEntry, got "
                    f"{type(entry).__name__}"
                )
            if entry.model_id in seen_ids:
                raise DuplicateModelIdError(f"duplicate model_id: {entry.model_id!r}")
            seen_ids.add(entry.model_id)
        # THE ENTRY-COUNT CAP (contract-v2.2). The released schema caps `models`
        # at 64 and this type did not, so a 65-entry catalog constructed cleanly
        # and could be dispatched by the turn route -- which checks only
        # `isinstance(catalog, ModelCatalog)` -- while
        # `GET /workbench/model-catalog` refused to serve the very catalog
        # holding it, because serve.py validates the projected envelope against
        # the released schema. The same divergence `MAX_ROUTING_TARGETS` closed
        # for `routes_to`, one level up.
        #
        # It is checked AFTER the element-type and duplicate scans so those two
        # refusals are unchanged for every catalog that has them, and BEFORE the
        # routing walk so an over-large catalog is named for what is wrong with
        # it rather than for the first routing rule in it.
        if len(materialized) > MAX_CATALOG_ENTRIES:
            raise CatalogEntryCountError(
                f"catalog declares {len(materialized)} entries, above the "
                f"{MAX_CATALOG_ENTRIES} the released catalog schema permits")
        self._validate_routing_targets(materialized)

    @staticmethod
    def _validate_routing_targets(
        entries: tuple[ModelCatalogEntry, ...],
    ) -> None:
        """The CROSS-ENTRY half of the contract-v1.38 routing rules -- the SIX
        the released schema cannot express and the delegated validator
        (`scripts/validate-ideation-dashboard-contracts.py`) enforces on the
        wire. Both places enforce the same six; neither is the other's
        substitute, because a catalog assembled in-process never becomes a
        validated file and a catalog file is never constructed here.

        Numbered 1-5 below, with the separator-collision DIAGNOSTIC folded into
        rule 4 because it is that rule's well-formedness precondition rather
        than a rule of its own. `InvalidRoutingRuleError`'s docstring lists all
        six as raised, which is the view a caller catching it needs.

        1. NO DANGLING TARGET. Every `routes_to` id must name an entry in this
           same catalog. A rule that routes somewhere the catalog does not
           offer is a rule whose badge nobody can check.
        2. NO CHAINED RULE. A target must not itself be a routing rule.
           ``resolved_model_id`` is recorded as the model that ANSWERED, so it
           has to name something that answers rather than another indirection.
        3. AN AVAILABLE RULE RESOLVES TO AN AVAILABLE MODEL. `dispatch_turn`
           checks availability on the SELECTED entry, and the adapter then
           sets the harness to the RESOLVED id -- so without this an available
           `auto` could dispatch to a model the catalog itself calls
           unavailable. When the rule is unavailable nothing can select it, so
           its targets' availability is not this rule's business.
        4. THE BADGE COVERING (the ratified scenario's own THEN: a routing
           entry "MUST ... carry the handling badge of every model it may route
           to"), as SEGMENT MEMBERSHIP over ``ROUTING_BADGE_SEPARATOR``. The
           rule's own badge is the ONE string the menu shows for it, so each
           target's badge must be one of that badge's segments. A target badge
           that itself contains the separator is refused as ILL-FORMED: it
           could never be a segment, and the alternative is a grammar that
           silently splits a badge in half. Extra segments are permitted -- a
           rule may carry its own lead-in beside the badges it must carry.
           CORRECTED at adversarial review round 1 (F1): this was raw substring
           containment, which the reviewer broke twice on the released bytes.
           See ``normalized_badge_segment`` for the whole argument and for what
           is deliberately NOT normalized.
        5. A RULE PROMISES NO MORE HEADROOM THAN THE MODEL THAT ANSWERS.
           ``effective_limit_bytes`` is computed from the SELECTED entry, which
           for a routed turn is the RULE -- so a rule declaring limits above the
           model that actually answers would pass a turn that model cannot take.
           An AVAILABLE rule's declared limits must therefore not exceed those
           of ``resolved_model_id``'s entry. Unavailable rules are exempt for
           the same reason they are exempt from rule 3: nothing can select one,
           so its promise is not load-bearing -- and that exemption is what
           keeps the bridge's degraded projection constructible.
           RULED BY BRETT 2026-08-21 ("Swap to rule 5'"). This was first
           shipped as a MINIMUM over every member of ``routes_to``, which the
           adversarial review upheld only WITH RESERVATION, and the ruling
           narrowed it to the resolved model alone. Three reasons, recorded
           because the shape of the rule is a design commitment and not an
           implementation detail:
           * under this release's STATIC resolution the promise that matters is
             that the menu's declared limits are honoured by the model that
             actually answers -- which is precisely what this checks;
           * the un-resolved destinations are not load-bearing: no turn reaches
             them while the rule resolves elsewhere, so capping against them
             constrains a promise nobody can call in;
           * min-capping would BAKE IN semantics that contradict the sanctioned
             future direction -- a per-turn, fit-aware router that chooses a
             destination BY the assembled packet's size (and by other
             capability dimensions), staged as
             ``ideation/staging/doxchat-auto-fit-routing/``. Under that design a
             rule's declared ceiling is the widest thing it can serve, not the
             narrowest, and a min-cap would have had to be undone to get
             there."""
        by_id = {entry.model_id: entry for entry in entries}
        for entry in entries:
            if entry.routing_rule is not True:
                continue
            declared_segments = badge_segments(entry.data_handling)
            for target_id in entry.routes_to:
                target = by_id.get(target_id)
                if target is None:
                    raise InvalidRoutingRuleError(
                        f"routing rule {entry.model_id!r} routes to "
                        f"{target_id!r}, which is not in this catalog")
                if target.routing_rule is True:
                    raise InvalidRoutingRuleError(
                        f"routing rule {entry.model_id!r} routes to "
                        f"{target_id!r}, which is itself a routing rule")
                # A DIAGNOSTIC rather than an independent refusal: a badge
                # holding the separator can never be a segment, so the covering
                # check below would refuse this catalog anyway — with a message
                # telling the operator to add a badge that still would not
                # match. Proven redundant-as-a-refusal by revert-test; kept
                # because naming the real cause is worth one branch.
                #
                # Tested against the NORMALIZED badge, not the raw string
                # (review re-verify N3), and this is NOT only about the message:
                # a badge written `"read /\nwrite"` does not contain " / "
                # raw, but DOES after whitespace collapse -- so it slipped this
                # arm AND then satisfied the covering check, because the rule's
                # own badge normalizes to the same segment. That is a full
                # ACCEPT of an ill-formed badge, not a misdirected message.
                if ROUTING_BADGE_SEPARATOR in normalized_badge_segment(
                        target.data_handling):
                    raise InvalidRoutingRuleError(
                        f"the data_handling badge of {target_id!r} contains "
                        f"{ROUTING_BADGE_SEPARATOR!r}, the routing badge's own "
                        f"segment separator, so it cannot be carried as one")
                if normalized_badge_segment(
                        target.data_handling) not in declared_segments:
                    raise InvalidRoutingRuleError(
                        f"routing rule {entry.model_id!r} does not carry the "
                        f"data-handling badge of {target_id!r} as a segment of "
                        f"its own badge")
            resolved = by_id[entry.resolved_model_id]
            if entry.available is True:
                # RULE 5' — the bound is the RESOLVED model's, not the minimum
                # over `routes_to`. Both halves of that are Brett's ruling; see
                # `_validate_routing_targets`' docstring for the argument.
                for field in ("input_limit_bytes", "output_limit_bytes"):
                    declared = getattr(entry, field)
                    answering = getattr(resolved, field)
                    if declared > answering:
                        raise InvalidRoutingRuleError(
                            f"routing rule {entry.model_id!r} declares {field} "
                            f"{declared}, above the {answering} of "
                            f"{entry.resolved_model_id!r}, the model it "
                            f"resolves to")
                if resolved.available is not True:
                    raise InvalidRoutingRuleError(
                        f"routing rule {entry.model_id!r} is available but "
                        f"resolves to {entry.resolved_model_id!r}, which is not")

    @classmethod
    def from_entries(cls, entries) -> "ModelCatalog":
        """Accept any iterable, in the order supplied. This function never
        sorts and never picks a default: ordering and selection policy are
        declared gaps (checklists/provider-boundary.md CHK005/CHK006), not
        this module's to invent.

        Fails closed: a non-``ModelCatalogEntry`` element or a repeated
        ``model_id`` refuses construction of the whole catalog. Nothing is
        silently dropped or reordered to make room for a later fix.

        A thin, intention-revealing wrapper only: ``__post_init__`` is what
        actually enforces the invariants above, identically for this
        constructor and for calling ``ModelCatalog(entries=...)`` directly."""
        return cls(entries=entries)

    def available_entries(self) -> tuple[ModelCatalogEntry, ...]:
        """Order-preserving filter on ``available is True``."""
        return tuple(entry for entry in self.entries if entry.available is True)

    def entry_for(self, model_id: str) -> ModelCatalogEntry | None:
        """Exact-match lookup only -- no case-folding, no normalization."""
        for entry in self.entries:
            if entry.model_id == model_id:
                return entry
        return None

    def selectable_entry_for(self, model_id: str) -> ModelCatalogEntry | None:
        """The entry, but only when it both exists and is available
        (data-model.md Section 6: "Only true entries may be selected").
        Returns ``None`` on any refusal -- public failure codes for a turn
        belong to T049/T051, not this slice."""
        entry = self.entry_for(model_id)
        if entry is not None and entry.available is True:
            return entry
        return None

    def as_public_dict(self) -> dict:
        """Exactly one key, ``models``, holding each entry's own public
        dict, in order -- nothing else."""
        return {"models": [entry.as_public_dict() for entry in self.entries]}


EMPTY_CATALOG = ModelCatalog(())
"""The FR-025 / research R6 empty-catalog posture: an absent or unreachable
model capability is a supported editor-only state, not an error."""


# ---------------------------------------------------------------------------
# released wire projection (T020 wire clause)
# ---------------------------------------------------------------------------


def catalog_wire_envelope(catalog: ModelCatalog) -> dict:
    """The RELEASED ``workbench-model-catalog`` success envelope for
    ``catalog``: exactly ``WIRE_ENVELOPE_FIELDS``, in that order, with each
    entry's own public dict -- the seven base fields, plus a routing entry's
    three-field declaration where it has one -- in catalog order.

    A PURE function, not a port member and not a deployment adapter: it takes
    a catalog and returns a fresh plain dict, reaching no network, reading no
    environment variable, and consulting no provider. Turn DISPATCH stays
    absent from ``WorkbenchModelPort`` (T049) and the approved deployment
    adapters stay unbuilt (T047 remainder, governing 5.1); this clause adds
    the wire SHAPE the released schema governs and nothing else.

    An EMPTY ``models`` array is a successful editor-only posture
    (FR-025/SC-008), never an error -- the released schema says so explicitly,
    so no caller needs to special-case it.

    ``ModelCatalog.as_public_dict`` is deliberately left as it was: the
    one-key ``{"models": [...]}`` internal projection has callers that want no
    discriminators, and widening it in place would have made every internal
    reader carry a wire envelope it never asked for. The two projections share
    each entry's ``as_public_dict``, which is the part that must never drift.

    Refuses a non-``ModelCatalog`` with ``TypeError``: an unvalidated mapping
    that merely looks catalog-shaped must never be blessed as the released
    envelope."""
    if not isinstance(catalog, ModelCatalog):
        raise TypeError(
            f"catalog must be a ModelCatalog, got {type(catalog).__name__}"
        )
    return {
        "schema_version": CATALOG_WIRE_SCHEMA_VERSION,
        "kind": CATALOG_WIRE_KIND,
        "models": [entry.as_public_dict() for entry in catalog.entries],
    }


# ---------------------------------------------------------------------------
# pure limit helper
# ---------------------------------------------------------------------------


def effective_limit_bytes(*, server_maximum: int, entry_limit: int) -> int:
    """The stricter (smaller) of a server constant and a selected catalog
    entry's declared limit (plan.md: "The effective turn limit is the
    stricter of server constants and the selected catalog entry; no silent
    truncation is permitted"). Performs no content inspection and no
    truncation -- it only compares two already-validated integers."""
    for field, value in (("server_maximum", server_maximum), ("entry_limit", entry_limit)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{field} must be a non-bool int")
        if value <= 0:
            raise ValueError(f"{field} must be strictly positive")
    return min(server_maximum, entry_limit)


# ---------------------------------------------------------------------------
# narrow provider port
# ---------------------------------------------------------------------------


@runtime_checkable
class WorkbenchModelPort(Protocol):
    """The narrow injected seam a doxBench server declares for chat
    (research R6). Exactly three members -- nothing else -- so a
    ``__protocol_attrs__`` reader can prove the surface never grew a second
    provider verb by accident.

    ``timeout_seconds`` is the adapter-declared timeout (plan.md
    Constraints), read-only, expressed in seconds.

    ``catalog()`` returns the approved public ``ModelCatalog`` this adapter
    currently offers.

    ``dispatch(prompt_envelope)`` hands ONE opaque, already-assembled prompt
    envelope to the adapter and returns the provider's raw answer, unread.
    PIN EVOLUTION (T049, sanctioned by research R6's own rationale): this
    member was deliberately absent while the ``xfactory-workbench-chat-turn``
    envelope was unreleased; the contract is now released and pinned
    (contract-v1.27, ``d09d5820de5b63b9528f6baea884a6dccde9b158``), and R6's
    argument was for ONE named capability per genuine need, not for two
    members forever. The seam stays exactly this narrow: prompt assembly
    lives in doxbench_turns.py, outcome mapping/validation lives in
    ``dispatch_turn`` beside this protocol, and every other provider-verb
    spelling stays banned by the companion test's ``FORBIDDEN_PORT_MEMBERS``.
    Declaring the member is NOT a deployment claim -- the route reaches an
    adapter only through its own T051 boundary, and no real adapter exists in
    this repository (T099 is operator-gated).

    ``runtime_checkable`` protocols with non-method members support
    ``isinstance()`` checks but not ``issubclass()`` checks -- use
    ``isinstance`` only, and only in tests."""

    @property
    def timeout_seconds(self) -> float | int: ...

    def catalog(self) -> ModelCatalog: ...

    def dispatch(self, prompt_envelope: object) -> object: ...


def validated_timeout_seconds(value: object) -> float:
    """Pure validator: accepts a real, non-bool number strictly greater than
    zero and no greater than ``MAX_ADAPTER_TIMEOUT_SECONDS``; refuses every
    other value -- wrong type, ``bool``, non-finite, zero, negative, or over
    the cap -- with the single ``AdapterTimeoutError``."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AdapterTimeoutError(
            "declared timeout must be a real, non-bool number of seconds"
        )
    numeric = float(value)
    if numeric != numeric:  # a NaN is the only float that is not equal to itself
        raise AdapterTimeoutError("declared timeout must not be NaN")
    if not (0 < numeric <= MAX_ADAPTER_TIMEOUT_SECONDS):
        raise AdapterTimeoutError(
            "declared timeout must be greater than 0 and at most "
            f"{MAX_ADAPTER_TIMEOUT_SECONDS} seconds"
        )
    return numeric


# ---------------------------------------------------------------------------
# turn dispatch: fixed failure mapping, timeout enforcement, response bounds,
# redacted diagnostics (T049)
# ---------------------------------------------------------------------------

# The CLOSED set of dispatch failure codes, in refusal-order. Every spelling
# matches the released failure envelope's `error` pattern
# (`^[a-z][a-z0-9_]{2,63}$`, contract-v1.27); `model_unavailable` is the SAME
# spelling serve.py already uses for its pre-dispatch precondition 7 refusal
# (the companion test pins the equality), and the other three are this
# slice's own judgement-call spellings for outcome classes only dispatch can
# observe. The route (T051) owns HTTP statuses and caller-facing messages;
# this module carries codes and FIXED diagnostics only.
DISPATCH_ERR_MODEL_UNAVAILABLE = "model_unavailable"
DISPATCH_ERR_MODEL_TIMEOUT = "model_timeout"
DISPATCH_ERR_MODEL_FAILED = "model_failed"
DISPATCH_ERR_RESPONSE_INVALID = "response_invalid"

DISPATCH_FAILURE_CODES: tuple[str, ...] = (
    DISPATCH_ERR_MODEL_UNAVAILABLE,
    DISPATCH_ERR_MODEL_TIMEOUT,
    DISPATCH_ERR_MODEL_FAILED,
    DISPATCH_ERR_RESPONSE_INVALID,
)

# Fixed, module-level diagnostics (FR-020/FR-022): NEVER composed from
# request data, provider output, or exception text. A provider exception's
# own message must not reach any loggable surface, so every failure carries
# one of exactly these strings and nothing else.
_DIAG_ADAPTER_MISDECLARED = "the adapter declared an unusable timeout"
_DIAG_MODEL_UNAVAILABLE = "the selected model is not available for dispatch"
_DIAG_TIMEOUT_EXCEEDED = "the provider did not answer within the declared timeout"
_DIAG_PROVIDER_RAISED = "the provider failed and its details are withheld by design"
_DIAG_RESPONSE_MALFORMED = "the provider response did not match the expected shape"
_DIAG_PROPOSALS_UNSUPPORTED = "proposal-bearing responses are not accepted here"
_DIAG_PROPOSALS_REFUSED = "the typed-proposal validation refused this response"
_DIAG_RESPONSE_OVERSIZE = "the provider response exceeds the permitted size"

FIXED_DISPATCH_DIAGNOSTICS: frozenset[str] = frozenset({
    _DIAG_ADAPTER_MISDECLARED,
    _DIAG_MODEL_UNAVAILABLE,
    _DIAG_TIMEOUT_EXCEEDED,
    _DIAG_PROVIDER_RAISED,
    _DIAG_RESPONSE_MALFORMED,
    _DIAG_PROPOSALS_UNSUPPORTED,
    _DIAG_PROPOSALS_REFUSED,
    _DIAG_RESPONSE_OVERSIZE,
})


@dataclass(frozen=True, slots=True)
class TurnDispatchSuccess:
    """A validated, prose-only provider answer. ``proposals`` is always the
    empty tuple in this slice: typed-proposal validation is T061
    (doxbench_turns.py, US3), and until that validator exists
    ``dispatch_turn`` refuses proposal-bearing responses rather than passing
    anything unvalidated through this type."""

    assistant_prose: str
    proposals: tuple = ()


@dataclass(frozen=True, slots=True)
class TurnDispatchFailure:
    """A fixed, redacted dispatch refusal: one code from
    ``DISPATCH_FAILURE_CODES`` and one diagnostic from
    ``FIXED_DISPATCH_DIAGNOSTICS``. Deliberately carries NO payload, no
    partial prose, and no exception text -- there is no attribute a caller
    could log that discloses provider or request content."""

    error: str
    diagnostic: str


def dispatch_turn(port, prompt_envelope, *, entry, clock, proposal_validator=None):
    """Hand ``prompt_envelope`` to ``port`` exactly once and map every
    outcome to a ``TurnDispatchSuccess`` or a fixed ``TurnDispatchFailure``
    (T049). This is the ONLY call site in the module that touches an
    adapter's ``dispatch``, and it never raises for a provider-shaped
    outcome -- only a caller programming error (a non-``ModelCatalogEntry``
    ``entry``) raises.

    ``clock`` is an INJECTED zero-argument monotonic reader (seconds as
    float). The route supplies a real monotonic clock at T051; tests supply
    deterministic fakes. Enforcement rule: the clock is read once before and
    once after the dispatch call, and when the elapsed time EXCEEDS the
    adapter's validated ``timeout_seconds`` the deadline outcome dominates
    everything else -- a result or error arriving after the deadline is
    discarded unread. Equality is not an overrun: an answer landing exactly
    at the declared timeout is honoured.

    Refusal order, first match wins:

    1. misdeclared adapter timeout        -> ``model_failed`` (no dispatch);
    2. ``entry`` not available            -> ``model_unavailable`` (no dispatch);
    3. elapsed > validated timeout        -> ``model_timeout`` (result discarded);
    4. adapter raised                     -> ``model_failed`` (text redacted);
    5. malformed shape                    -> ``response_invalid``;
    6. any proposal present (pre-T061)    -> ``response_invalid`` (fail closed);
    7. prose over ``MAX_ASSISTANT_PROSE_BYTES`` or over the stricter of the
       server output cap and the entry's declared output limit
       (``effective_limit_bytes``)        -> ``response_invalid``.

    Bounds measure exact UTF-8 BYTES, never code points, matching the
    feature's content-identity rule."""
    if not isinstance(entry, ModelCatalogEntry):
        raise TypeError(
            f"entry must be a ModelCatalogEntry, got {type(entry).__name__}"
        )
    try:
        timeout = validated_timeout_seconds(port.timeout_seconds)
    except AdapterTimeoutError:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_MODEL_FAILED, diagnostic=_DIAG_ADAPTER_MISDECLARED)
    if entry.available is not True:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_MODEL_UNAVAILABLE, diagnostic=_DIAG_MODEL_UNAVAILABLE)

    started = clock()
    raw: object = None
    raised = False
    try:
        raw = port.dispatch(prompt_envelope)
    except Exception:
        # The exception object is dropped HERE, unread: its text must never
        # reach a loggable surface (FR-020/FR-022).
        raised = True
    elapsed = clock() - started
    if elapsed > timeout:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_MODEL_TIMEOUT, diagnostic=_DIAG_TIMEOUT_EXCEEDED)
    if raised:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_MODEL_FAILED, diagnostic=_DIAG_PROVIDER_RAISED)

    if not isinstance(raw, dict) or set(raw) != {"assistant_prose", "proposals"}:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_RESPONSE_INVALID, diagnostic=_DIAG_RESPONSE_MALFORMED)
    prose = raw["assistant_prose"]
    proposals = raw["proposals"]
    if not isinstance(prose, str) or not isinstance(proposals, list):
        return TurnDispatchFailure(
            error=DISPATCH_ERR_RESPONSE_INVALID, diagnostic=_DIAG_RESPONSE_MALFORMED)
    if proposals and proposal_validator is None:
        # Fail closed for every caller that has not opted into typed
        # validation: an unvalidated proposal must never pass this seam.
        return TurnDispatchFailure(
            error=DISPATCH_ERR_RESPONSE_INVALID, diagnostic=_DIAG_PROPOSALS_UNSUPPORTED)
    prose_bytes = len(prose.encode("utf-8"))
    permitted = effective_limit_bytes(
        server_maximum=SERVER_MAX_OUTPUT_LIMIT_BYTES,
        entry_limit=entry.output_limit_bytes)
    if prose_bytes > MAX_ASSISTANT_PROSE_BYTES or prose_bytes > permitted:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_RESPONSE_INVALID, diagnostic=_DIAG_RESPONSE_OVERSIZE)
    if not proposals:
        return TurnDispatchSuccess(assistant_prose=prose, proposals=())
    # T061 widening (the exact evolution the original refusal's docstring
    # promised): typed validation stays OUT of this module — doxbench_turns
    # imports this one, so the validator arrives INJECTED. Its refusal text
    # is dropped unread, like every other upstream detail (FR-020/FR-022).
    try:
        validated = proposal_validator(raw)
    except Exception:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_RESPONSE_INVALID, diagnostic=_DIAG_PROPOSALS_REFUSED)
    # PR #63 review (Codex P2): the entry's output limit bounds the WHOLE
    # validated response. Proposal content is measured the same exact-UTF-8
    # way as prose; a narrow model cannot smuggle a large total through
    # small prose.
    total_bytes = prose_bytes + sum(
        len(str(item["content"] if isinstance(item, dict) else item.content)
            .encode("utf-8"))
        for item in validated.proposals)
    if total_bytes > permitted:
        return TurnDispatchFailure(
            error=DISPATCH_ERR_RESPONSE_INVALID, diagnostic=_DIAG_RESPONSE_OVERSIZE)
    return TurnDispatchSuccess(
        assistant_prose=prose, proposals=tuple(validated.proposals))


# Sentinel for "no scripted dispatch result": ``None`` is a REAL (malformed)
# provider payload a test must be able to script, so absence needs its own
# marker object.
_UNSET_DISPATCH_RESULT = object()


class FakeWorkbenchModelPort:
    """An in-memory, deterministic ``WorkbenchModelPort`` -- the ONLY
    adapter this slice defines; there is no real provider adapter here.

    ``catalog()`` always returns the SAME ``ModelCatalog`` object
    (determinism) unless a pre-seeded ``catalog_error`` is present, in which
    case it raises that error instead -- every call is still appended to the
    public ``calls`` log first, so a future test can prove a refusal
    happened before any fake dispatch occurred, and so a deterministic
    catalog-assembly failure (the posture behind
    contracts/model-catalog.md's ``catalog_unavailable`` code) is observable
    without guessing at internal state.

    ``dispatch(prompt_envelope)`` (T046) is scripted the same way: every
    call appends ``"dispatch"`` to ``calls`` and the envelope to
    ``dispatched`` FIRST, then raises the pre-seeded ``dispatch_error`` if
    one is present, then returns the pre-seeded ``dispatch_result``.
    ``None`` is a legitimate (malformed) scripted result, so "no script"
    is the private ``_UNSET_DISPATCH_RESULT`` sentinel, in which case a
    minimal valid prose-only payload is returned. Timeout behaviour is NOT
    simulated here: ``dispatch_turn``'s clock is injected, so a test scripts
    an overrun by handing it a clock whose second reading is late.

    This adapter reaches no network, reads no environment variable, and
    holds no credential-shaped value: it is backed by nothing but the
    ``ModelCatalog`` object and scripted values handed to its constructor."""

    def __init__(
        self,
        catalog: ModelCatalog = EMPTY_CATALOG,
        *,
        timeout_seconds: float = 30.0,
        catalog_error: BaseException | None = None,
        dispatch_result: object = _UNSET_DISPATCH_RESULT,
        dispatch_error: BaseException | None = None,
    ) -> None:
        if not isinstance(catalog, ModelCatalog):
            raise TypeError(
                f"catalog must be a ModelCatalog, got {type(catalog).__name__}"
            )
        self._timeout_seconds = validated_timeout_seconds(timeout_seconds)
        self._catalog = catalog
        self._catalog_error = catalog_error
        self._dispatch_result = dispatch_result
        self._dispatch_error = dispatch_error
        self.calls: list[str] = []
        self.dispatched: list[object] = []

    @property
    def timeout_seconds(self) -> float:
        return self._timeout_seconds

    def catalog(self) -> ModelCatalog:
        self.calls.append("catalog")
        if self._catalog_error is not None:
            raise self._catalog_error
        return self._catalog

    def dispatch(self, prompt_envelope: object) -> object:
        self.calls.append("dispatch")
        self.dispatched.append(prompt_envelope)
        if self._dispatch_error is not None:
            raise self._dispatch_error
        if self._dispatch_result is _UNSET_DISPATCH_RESULT:
            return {"assistant_prose": "fake grounded answer", "proposals": []}
        return self._dispatch_result

    def __repr__(self) -> str:
        return (
            f"FakeWorkbenchModelPort(entries={len(self._catalog.entries)}, "
            f"timeout_seconds={self._timeout_seconds})"
        )
