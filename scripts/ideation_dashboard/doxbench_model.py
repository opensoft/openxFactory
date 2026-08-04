"""Public model-catalog types and the narrow provider port for doxBench chat
(010-doxbench-editor-chat T013/T020; data-model.md Section 6,
contracts/model-catalog.md, research.md R6/R9, plan.md Constraints).

This module owns exactly five things:

* the immutable public catalog shape (``ModelCatalogEntry`` / ``ModelCatalog``);
* the PURE projection of a catalog into the RELEASED
  ``workbench-model-catalog`` wire envelope (``catalog_wire_envelope``), added
  once the additive openxFactory schema was released and pinned at
  contract-v1.27 (``d09d5820de5b63b9528f6baea884a6dccde9b158``);
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
# contracts/model-catalog.md). Nothing else may ever appear in a public dict
# this module produces.
PUBLIC_ENTRY_FIELDS: tuple[str, ...] = (
    "model_id",
    "label",
    "provider_class",
    "available",
    "input_limit_bytes",
    "output_limit_bytes",
    "data_handling",
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


class DuplicateModelIdError(ModelCatalogError):
    """Two entries in one catalog share a ``model_id`` (data-model.md
    Section 6: ``model_id`` is unique). Raised by
    ``ModelCatalog.__post_init__`` -- for both ``ModelCatalog.from_entries(...)``
    and a direct ``ModelCatalog(entries=...)`` construction; the whole
    catalog refuses rather than dropping the later entry."""


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
    it to the browser (data-model.md Section 6). The seven fields below are
    the whole public surface: nothing else may be constructed, because this
    dataclass is slotted and every extra keyword argument is a ``TypeError``
    at construction.

    ``provider_class`` and ``data_handling`` are free-form, non-blank
    strings, not a closed enum: data-model.md Section 6 calls
    ``provider_class`` "enum/string" without naming the value set, and a
    fixture using one value (like the contract example's on-tenant posture)
    does not make it the only legal one."""

    model_id: str
    label: str
    provider_class: str
    available: bool
    input_limit_bytes: int
    output_limit_bytes: int
    data_handling: str

    def __post_init__(self) -> None:
        _require_non_blank_str("model_id", self.model_id)
        _require_non_blank_str("label", self.label)
        _require_non_blank_str("provider_class", self.provider_class)
        _require_non_blank_str("data_handling", self.data_handling)
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

    def as_public_dict(self) -> dict:
        """Exactly ``PUBLIC_ENTRY_FIELDS``, in that order. No version marker
        and no discriminator marker -- see the module docstring's deferral
        list."""
        return {
            "model_id": self.model_id,
            "label": self.label,
            "provider_class": self.provider_class,
            "available": self.available,
            "input_limit_bytes": self.input_limit_bytes,
            "output_limit_bytes": self.output_limit_bytes,
            "data_handling": self.data_handling,
        }


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
    the dataclass constructor, not the only safe entry point."""

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
    entry's own seven-field public dict, in catalog order.

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
