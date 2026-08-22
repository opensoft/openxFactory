"""The BOUNDED CONTEXT PACKET and the rails that assemble it
(add-doxbench-editing-phase-b, design §3.1–§3.4, tasks §10.3, §10.4, §10.5,
§10.7; the delta's `The staged-set knowledge service assembles a bounded
context packet` and `Context compression is a three-layer stack with declared
fidelity`).

The pipeline this module owns, in the order design §3.1 fixes:

  1. **CONFINEMENT** — the admissible ref set is computed FIRST, from the
     tile's own staged set plus the promoted findings, and nothing else. This
     runs before any retrieval provider is reached, and the provider is handed
     the set rather than trusted to respect one.

     WHY THAT IS THE COHERENT READING, recorded because design §3.1 does not
     read cleanly on its own: step 2's own box CONTAINS "evidence: knowledge
     service search", and the prose beneath it says steps 2–3 run "before any
     retrieval provider or model provider is reached". Those cannot both be
     literally true, so this module takes the reading that preserves what the
     rails are FOR — the rail that governs the retrieval provider (the
     confinement) precedes and constrains it, and selection, the exemption and
     the bounds fit all precede the MODEL provider. Reordering so that no
     provider is touched until after selection would mean selecting evidence
     before knowing what evidence exists, which is not a stricter reading of
     the requirement but an incoherent one.
  2. **SELECTION** (compression layer one, LOSSLESS BY REFERENCE) — the
     selected document's thread in full, the OTHER loaded documents' thread
     STATE HEADERS only, and the evidence the confined retrieval selected. What
     is left out is one retrieval call away, and the packet names what it
     carries.
  3. **THE LIFECYCLE-STATUS EXEMPTION RAIL** — each item's own ``Status:``
     header is read HERE, by the assembler, and approved/ratified content is
     marked exempt from aggressive compression. Upstream of any compressor, and
     never delegated: only this stage can read a lifecycle status.
  4. **THE BOUNDS CHECK** — refuse with the MEASURED DIMENSION. No truncation,
     ever, and no packet content in the refusal.
  5. **DETERMINISTIC ASSEMBLY** — the packet, and the prompt sections it
     contributes, in one declared order.

**A REFUSAL DISCLOSES NO PACKET CONTENT.** Every exception below carries
dimensions, limits, and vocabulary this module wrote itself — never a source's
text, and never a caller's message.

**THE PACKET IS A LEASH.** It declares its purpose, the exact sources it
carries with their refs, its bound scope, and its expiry, and
``require_valid`` refuses it for another purpose, another scope, or after it
expires — so a consumer handed a stale or foreign packet asks for a new one
instead of using it.

**DEGRADED POSTURE.** With no knowledge service, the turn does NOT fail and
does NOT reach for an unbounded substitute: it degrades to the DECLARED reduced
packet — the selected thread and the loaded buffers — with the reduced posture
STATED in the packet's own declaration section. The rails still run; nothing is
bypassed to reach a provider.

Stdlib only, pure, and no I/O: threads arrive already parsed, the corpus
arrives through the injected knowledge boundary, and this module reads no file
and reaches no network.
"""

from __future__ import annotations

import dataclasses
import re
import time
from collections.abc import Callable, Mapping, Sequence

from doc_health.lines import split_keepends
from ideation_dashboard.doxbench_hash import utf8_size
from ideation_dashboard.doxbench_scope import ScopeKey, ScopeProjection
from ideation_dashboard.doxbench_threads import (
    DocumentThread, render_state_header, render_thread,
)

# ---------------------------------------------------------------------------
# refusals
# ---------------------------------------------------------------------------


class PacketError(ValueError):
    """Base class for every packet refusal. Carries dimensions and declared
    vocabulary only; a packet refusal never discloses packet content."""


class PacketBoundExceeded(PacketError):
    """Raised when the assembled packet exceeds a declared bound. Names the
    MEASURED DIMENSION and the limit, and nothing is truncated to fit: a
    silently shortened context is a context nobody can reason about.

    ``limit`` carries the same three fields every other doxBench bound refusal
    reports -- the dimension's NAME, what was measured, and the maximum -- so a
    caller learns which bound it hit and by how much. Three values this module
    computed itself: no ref, no text, and nothing caller-supplied."""

    def __init__(self, dimension: str, measured: int, maximum: int) -> None:
        self.limit = {"dimension": dimension, "measured": measured,
                      "maximum": maximum}
        super().__init__(
            f"packet {dimension} {measured} exceeds the bound {maximum}")


class PacketRejected(PacketError):
    """Base class for the three ways a packet is invalid as input."""


class PacketPurposeMismatch(PacketRejected):
    """The packet was issued for a different purpose."""


class PacketScopeMismatch(PacketRejected):
    """The packet was issued for a different scope."""


class PacketExpired(PacketRejected):
    """The packet's declared expiry has passed."""


# ---------------------------------------------------------------------------
# the lifecycle-status read (task 10.3) — the assembler's own, never delegated
# ---------------------------------------------------------------------------

# The SAME rule the repository's doc-health corpus reader uses: a `Status:`
# line inside the document's own header block, found by scanning the SAME
# shared real-line primitive corpus.parse_status scans through
# (`doc_health.lines.split_keepends` — CR/LF/CRLF only, so an exotic
# separator cannot inflate this window past a line that is plainly there).
# The window/regex/loop are still spelled out here rather than calling
# `corpus.parse_status` itself, because the exemption is the ASSEMBLER'S to
# apply and this is the read it applies it from; a companion test asserts
# the two readers agree, including on a synthetic exotic-separator fixture
# rather than real corpus documents alone (the corpus carries none today —
# measured zero across 1227 governed aggregation files — so an agreement
# check limited to it would pass vacuously).
_STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$")
STATUS_SCAN_LINES = 15

# The statuses whose content is EXEMPT from aggressive compression.
#
# The delta names "approved or ratified". This repository's own lifecycle
# vocabulary spells the approved end `ratified` (a change has ratified it) and
# `standard` (it has been promoted to canon), and the source-ranking hierarchy
# this same change ratified ranks "ratified or standard canon" TOGETHER at the
# top. Exempting `ratified` while compressing `standard` would therefore
# compress the most authoritative material this surface has, which is the
# opposite of what the exemption is for.
#
# `approved` is FOREIGN-CORPUS TOLERANCE, not a fourth local status: the delta
# names it, this repository's lifecycle vocabulary does not contain it, and a
# corpus-wide grep finds ZERO documents carrying it. It is honoured so a corpus
# that does use the word is not silently compressed, and it is recorded here as
# tolerance so no reader mistakes it for a status this repository issues.
EXEMPT_STATUSES: frozenset[str] = frozenset({"approved", "ratified", "standard"})

# A `Status:` value may carry a DECORATION after the status word — this corpus
# already holds `record · 2026-08-01T01:21Z (session of …)` and
# `record (in progress — …)` — so the exemption reads the leading status WORD
# and ignores what follows. Without this, a decorated `Status: ratified (…)`
# would silently lose its exemption, which is the exact failure this rail
# exists to prevent. `lifecycle_status` still returns the RAW value, so it goes
# on agreeing byte for byte with the repository's own corpus reader.
_STATUS_DECORATORS = "(·|,"


def lifecycle_status(text: str) -> str | None:
    """The document's own declared `Status:`, or None when it declares none."""
    if not isinstance(text, str):
        return None
    for body, _ending in split_keepends(text)[:STATUS_SCAN_LINES]:
        match = _STATUS_RE.match(body)
        if match:
            return match.group(1)
    return None


def status_word(status: str | None) -> str | None:
    """The leading status WORD of a possibly-decorated `Status:` value."""
    if status is None:
        return None
    value = status.strip().lower()
    for decorator in _STATUS_DECORATORS:
        value = value.split(decorator, 1)[0]
    parts = value.split()
    return parts[0] if parts else None


def is_compression_exempt(text: str) -> bool:
    """Whether this content is exempt from aggressive compression, read from
    its OWN lifecycle status header."""
    return status_word(lifecycle_status(text)) in EXEMPT_STATUSES


# ---------------------------------------------------------------------------
# the three-layer compression stack, declared (task: the fidelity pins)
# ---------------------------------------------------------------------------

FIDELITY_LOSSLESS_BY_REFERENCE = "lossless-by-reference"
FIDELITY_LOSSY_BY_DESIGN = "lossy-by-design"
FIDELITY_MECHANICAL_REVERSIBLE = "mechanical-reversible"


@dataclasses.dataclass(frozen=True, slots=True)
class CompressionLayer:
    """One layer of the stack and its DECLARED fidelity contract. No layer does
    another's work, and no layer may be described as having another's
    fidelity — which is why the contract is data with a checker rather than a
    sentence in a docstring."""

    number: int
    name: str
    fidelity: str
    owner: str
    realized: bool
    note: str


COMPRESSION_LAYERS: tuple[CompressionLayer, ...] = (
    CompressionLayer(
        number=1, name="selection", fidelity=FIDELITY_LOSSLESS_BY_REFERENCE,
        owner="the staged-set knowledge service (this module's selection rail)",
        realized=True,
        note=("material left out of a packet remains one retrieval call away "
              "and the packet names what it carries, so nothing is lost — it "
              "is referenced")),
    CompressionLayer(
        number=2, name="semantic compaction", fidelity=FIDELITY_LOSSY_BY_DESIGN,
        owner="doxbench_threads.compact_thread", realized=True,
        note=("lossy over the TRANSCRIPT and a defect over the header: "
              "human-reviewable, promotion-gated, non-authoritative and "
              "regenerable, preserving commitments and discarding narrative")),
    CompressionLayer(
        number=3, name="mechanical reversible compression",
        fidelity=FIDELITY_MECHANICAL_REVERSIBLE,
        owner="the model-boundary offload (add-doxbench-editing-phase-b §11)",
        realized=False,
        note=("heavy material offloads to session artifacts behind recoverable "
              "placeholders and MUST be retrievable in full by the same "
              "session; it is NOT realized here, and the lifecycle-status "
              "exemption above sits deliberately upstream of where it will "
              "run, because a compressor with no caller-metadata surface is "
              "disqualified from carrying that exemption by construction")),
)


class FidelityClaimRefused(PacketError):
    """Raised when a layer is described with another layer's fidelity."""


def layer(number: int) -> CompressionLayer:
    for row in COMPRESSION_LAYERS:
        if row.number == number:
            return row
    raise FidelityClaimRefused(f"there is no compression layer {number}")


def assert_fidelity(number: int, claimed: str) -> None:
    """Refuse a claim that a layer has a fidelity it does not have.

    The delta's first compression scenario in executable form: selection is not
    lossy, semantic compaction is not lossless, and mechanical offload is not a
    semantic summary."""

    declared = layer(number)
    if claimed != declared.fidelity:
        raise FidelityClaimRefused(
            f"compression layer {number} ({declared.name}) is "
            f"{declared.fidelity}, not {claimed!r}: the three fidelity "
            "contracts are what make the stack readable")


@dataclasses.dataclass(frozen=True, slots=True)
class WatchListedCandidate:
    """A component recorded WITH its adoption gates rather than adopted
    provisionally. Nothing in this capability may depend on one."""

    name: str
    layer: int
    gates: tuple[str, ...]
    adopted: bool = False

    def __post_init__(self) -> None:
        if self.adopted:
            raise PacketError(
                f"{self.name} is watch-listed: a candidate is admitted only "
                "when every recorded gate holds, including a sandboxed trial "
                "measuring net benefit on this surface's own workload rather "
                "than a published headline")


WATCH_LISTED_CANDIDATES: tuple[WatchListedCandidate, ...] = (
    WatchListedCandidate(
        name="Headroom", layer=3,
        gates=(
            "the credential findings are fixed and SECURITY.md is truthful",
            "telemetry is default-off in the OSS build",
            "prompt-cache fidelity is stable across releases",
            "a sandboxed trial shows net savings on doxBench's own workload",
            "a caller-metadata hook exists, without which the lifecycle-status "
            "exemption could not live inside it even if everything else "
            "cleared",
        )),
)


# ---------------------------------------------------------------------------
# the packet
# ---------------------------------------------------------------------------

PACKET_PURPOSE_CHAT_TURN = "doxbench-chat-turn"

SOURCE_SELECTED_THREAD = "selected-thread"
SOURCE_THREAD_STATE = "thread-state"
SOURCE_EVIDENCE = "evidence"
SOURCE_KINDS: tuple[str, ...] = (
    SOURCE_SELECTED_THREAD, SOURCE_THREAD_STATE, SOURCE_EVIDENCE)

POSTURE_FULL = "full"
POSTURE_REDUCED = "reduced"

# The provider id a packet carries when NO retrieval provider was reached at
# all. A declared label rather than an empty string or a `None`, for the same
# reason the telemetry's absences are declared: a blank reads as "not filled in
# yet" and invites someone to fill it in.
PROVIDER_NONE = "no-retrieval-provider"


@dataclasses.dataclass(frozen=True, slots=True)
class CorpusCoverage:
    """How much of the tile's confined staged set the derived index actually
    covered, and WHY the rest is missing.

    The two omission classes are kept apart (Codex review of PR #216, CODEX-C)
    because they mean different things to a reader: an UNREADABLE document is
    absent at this revision and will stay absent until it is fixed, while a
    BEYOND-BOUND one exists and would be retrievable under a larger bound.
    Merging them let the declaration blame the index bound for omissions the
    bound had nothing to do with."""

    indexed: int
    unreadable: int
    total: int

    def __post_init__(self) -> None:
        for field in ("indexed", "unreadable", "total"):
            value = getattr(self, field)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise PacketError(f"coverage.{field} is a non-negative count")
        if self.indexed + self.unreadable > self.total:
            raise PacketError(
                "coverage accounts for more documents than the tile holds")

    @property
    def beyond_bound(self) -> int:
        return self.total - self.indexed - self.unreadable

    @property
    def complete(self) -> bool:
        return self.indexed == self.total

REDUCED_NO_KNOWLEDGE_SERVICE = (
    "the staged-set knowledge service is unavailable, so this packet carries "
    "the selected thread and the loaded buffers only, with NO corpus evidence; "
    "no unbounded context was substituted and no rail was bypassed to reach a "
    "provider"
)

REDUCED_RETRIEVAL_REFUSED = (
    "the staged-set knowledge service refused this retrieval, so this packet "
    "carries the selected thread and the loaded buffers only, with NO corpus "
    "evidence; no unbounded context was substituted and no rail was bypassed "
    "to reach a provider"
)

# The packet's declared lifetime. Short, because a packet is a leash on ONE
# turn: a packet that outlived the turn it was assembled for would be a
# standing grant to material the next turn never asked for.
PACKET_TTL_SECONDS = 300.0

# The declared bounds. Refusing at these names the measured dimension and
# truncates nothing. They are the PACKET's own bounds and sit beside — never
# instead of — the request-side byte validators the turn module already runs
# against the model entry's effective input limit.
MAX_PACKET_BYTES = 256_000
MAX_PACKET_SOURCES = 48

# What the assembled prompt spends OUTSIDE the packet and outside the request
# bytes the route has already measured: the fixed system-contract and
# response-instruction constants, the model-data-handling and scope-metadata
# sections, and every FIXED section's label and separators.
#
# It exists because the packet's bound must compose with the MODEL's declared
# input limit (Codex review of PR #216, CODEX-B): the route knows what the
# request already spends, and the packet has to fit in what is left MINUS this
# scaffolding. Deliberately generous, and its adequacy is MEASURED rather than
# asserted — a companion test renders a real turn at a narrowed catalog ceiling
# and checks the assembled prompt against that ceiling.
#
# IT IS NO LONGER THE WHOLE RESERVE (tasks.md §11.5's recorded obligation,
# discharged by the slice that breached it). This number used to be subtracted
# FLAT, and a flat number could only ever be right for one section count: the
# shape §10 shipped (evidence, no threads) fitted comfortably, while the shape
# §11 creates — one section per loaded document's thread plus the evidence —
# spent ~19.7 KB of section scaffolding at 24 thread-states and 6 evidence refs
# of 120 characters, and ~31.2 KB at the packet's own 48-source bound. Both are
# past this number, so a turn near its model's ceiling could be ACCEPTED and
# then dispatch a prompt over that ceiling — the exact defect CODEX-B closed for
# the evidence-only shape.
#
# FIX OPTION (a) WAS TAKEN: the RENDERED section scaffolding is charged against
# the budget, per source, from the same literals the renderer uses (see
# `PER_SOURCE_SCAFFOLD_BYTES`), and this constant keeps only what is genuinely
# FIXED. Option (b) — scaling one flat number by `MAX_PACKET_SOURCES` — was
# rejected because it charges every turn for 48 sources it will not carry, which
# on a narrow catalog ceiling refuses turns that would have fitted; charging what
# the turn's OWN refs render is both the honest measurement and the cheaper one.
PROMPT_SCAFFOLD_RESERVE_BYTES = 16_384

# The rendered preambles, extracted as TEMPLATES so the reserve arithmetic and
# `packet_sections` read the same literals. A second copy of these strings is
# exactly how a reserve stops matching what the prompt actually spends.
SELECTED_THREAD_PREAMBLE = "SELECTED DOCUMENT THREAD — {ref}\n({note})\n\n"
THREAD_STATE_PREAMBLE = (
    "THREAD STATE HEADER — {ref}\n({note}; the transcript it summarizes is not "
    "carried here)\n\n")
EVIDENCE_PREAMBLE = "EVIDENCE — {ref} [{status}] [{exemption}]\n\n"
DECLARATION_LINE = "  - {kind} {ref} [{status}] [{exemption}]"

# Sections are joined by a blank line when a prompt is rendered for dispatch, so
# each section costs its own separator too.
SECTION_SEPARATOR_BYTES = 2

# The per-item section KEYS. Declared here, above the arithmetic that charges
# for them and used by `expand_group`/`packet_sections` below — one literal
# each.
PACKET_SECTION_SELECTED_THREAD = "selected_thread"
THREAD_STATE_SECTION_PREFIX = "thread_state:"
EVIDENCE_SECTION_PREFIX = "evidence:"

# The evidence slots one turn may fill. Declared here rather than left as a
# bare default on `assemble_packet`, because the ROUTE has to charge the
# scaffolding for the same number the assembler will select against, and two
# spellings of one number is how a reserve stops matching a prompt.
DEFAULT_EVIDENCE_LIMIT = 6

# The observed ref length the §11.5 obligation measured against. Used only where
# a ref is not yet known — the evidence SLOTS a turn reserves room for, whose
# refs the retrieval has not chosen yet.
OBSERVED_REF_BYTES = 120

# The note every thread section carries. Declared HERE, above the arithmetic
# that charges for it, and used by `packet_sections` below — ONE literal.
_NON_AUTHORITATIVE_NOTE = (
    "NON-AUTHORITATIVE and regenerable from the transcript it summarizes: it "
    "is not governed truth and does not become truth by being carried here")

# The WIDEST value each rendered label can take. A companion test pins each
# against the label helper that produces it, so a wider label breaks a test
# rather than a budget.
WIDEST_KIND_LABEL = max(SOURCE_KINDS, key=len)
WIDEST_STATUS_LABEL = "no Status: header"
WIDEST_EXEMPTION_LABEL = "EXEMPT from aggressive compression"


def _widest_per_source_bytes() -> int:
    """The widest rendered per-source scaffolding, with an EMPTY ref — the ref's
    own bytes are charged separately, once per place it renders."""

    filled = {"ref": "", "note": _NON_AUTHORITATIVE_NOTE,
              "status": WIDEST_STATUS_LABEL,
              "exemption": WIDEST_EXEMPTION_LABEL,
              "kind": WIDEST_KIND_LABEL}
    widest_section = max(
        utf8_size(template.format(**filled))
        for template in (SELECTED_THREAD_PREAMBLE, THREAD_STATE_PREAMBLE,
                         EVIDENCE_PREAMBLE))
    # EVERY section key a source can carry, not only the two prefixed ones
    # (PR #223, Copilot CP3): the SELECTED thread's key is the fixed
    # `selected_thread`, which is longer than `thread_state:` and was left out
    # — so a selected-thread source undercounted its key bytes.
    widest_key = max(utf8_size(PACKET_SECTION_SELECTED_THREAD),
                     utf8_size(THREAD_STATE_SECTION_PREFIX),
                     utf8_size(EVIDENCE_SECTION_PREFIX))
    return (widest_section + SECTION_SEPARATOR_BYTES + widest_key
            + utf8_size(DECLARATION_LINE.format(**filled)) + 1)


# One source costs: its own prompt section's preamble, that section's separator,
# and one line in the packet's declaration (plus that line's newline). DERIVED
# from the templates above rather than typed in, so the two cannot drift.
PER_SOURCE_SCAFFOLD_BYTES = _widest_per_source_bytes()

# HOW MANY TIMES ONE SOURCE'S REF RENDERS, and why the answer is three rather
# than the two a reading of `packet_sections` alone would give: the packet's
# declaration line carries it, the section's own preamble carries it, and the
# section KEY carries it a third time. The keys are not part of `section.text`
# and the bridge's own renderer does not emit them — but an adapter that labels
# its sections spends them, and this measurement is the one place where being
# generous is the safe direction. It is also what brings the reserve above the
# §11.5 obligation's OWN two recorded measurements (19,745 bytes at 24
# thread-states plus 6 evidence refs of 120 characters, and 31,211 at the
# 48-source bound), which were taken against a shape this module can no longer
# reproduce exactly; matching them from above rather than from below is the
# honest way to honour a number somebody else measured.
REF_RENDERINGS = 3

# WHAT THIS COSTS, RECORDED RATHER THAN HIDDEN (adversarial review P3-15). The
# reserve over-charges: the 24-document measurement charges ~31.5 KB against
# ~16.5 KB actually spent, roughly 2x. Over-reserving is the safe direction for
# the model's ceiling — an under-charge dispatches a prompt past it, which is
# the defect §11.5 exists to close — but it is not free: a turn near its
# ceiling reaches a zero evidence budget, and eventually the 409, earlier than
# it strictly must. That is the same cost cited to reject fix option (b), paid
# here in a smaller amount, and it is the reason the tests assert
# `spent <= charged` rather than a tight band: a tight band would fail on every
# harmless change to a section label. Tightening this is a future measurement
# exercise, not a correctness one.


def packet_scaffold_reserve(*, thread_refs: Sequence[str] = (),
                            evidence_slots: int = 0,
                            evidence_ref_bytes: int = OBSERVED_REF_BYTES) -> int:
    """The bytes the assembled prompt spends on SCAFFOLDING for this turn: the
    fixed constants, plus the rendered per-source overhead for the thread refs
    the route holds and the evidence slots it may fill.

    A ref is charged `REF_RENDERINGS` times — see that constant for why the
    answer is three rather than the two places `packet_sections` renders it.
    Evidence refs are not known until retrieval answers, so their slots are
    charged at the observed ref length the §11.5 obligation measured against.

    Defaults reproduce the FLAT pre-§11 number exactly, which is what keeps a
    caller carrying neither threads nor evidence on the arithmetic it was
    measured under."""

    refs = tuple(thread_refs)
    slots = max(0, int(evidence_slots))
    ref_bytes = max(0, int(evidence_ref_bytes))
    per_thread = sum(PER_SOURCE_SCAFFOLD_BYTES + REF_RENDERINGS * utf8_size(ref)
                     for ref in refs)
    per_evidence = slots * (PER_SOURCE_SCAFFOLD_BYTES
                            + REF_RENDERINGS * ref_bytes)
    return PROMPT_SCAFFOLD_RESERVE_BYTES + per_thread + per_evidence


def packet_budget_for(*, input_limit_bytes: int, request_bytes: int,
                      thread_refs: Sequence[str] = (),
                      evidence_slots: int = 0) -> int:
    """The bytes a packet may spend on a turn whose request already spends
    ``request_bytes`` against a model declaring ``input_limit_bytes``.

    Never more than the packet's own bound, never negative. A budget of zero is
    a legal answer and NOT an error: it means this turn has no room for
    evidence, so the fit carries none and says which refs it dropped — which is
    a better turn than one refused for a limit the caller cannot see.

    ``thread_refs`` and ``evidence_slots`` describe the SHAPE this turn will
    render, and they are what turned the flat reserve into a measured one
    (tasks.md §11.5). Omitting them is the pre-§11 shape and yields the pre-§11
    number; a caller that carries threads and does not declare them gets a
    budget that is too generous, which is why the route passes both."""

    reserve = packet_scaffold_reserve(thread_refs=thread_refs,
                                      evidence_slots=evidence_slots)
    remaining = int(input_limit_bytes) - int(request_bytes) - reserve
    return max(0, min(MAX_PACKET_BYTES, remaining))


@dataclasses.dataclass(frozen=True, slots=True)
class PacketSource:
    """One item the packet carries: what it is, where it came from, its own
    declared lifecycle status, and whether the exemption rail marked it."""

    ref: str
    kind: str
    text: str
    status: str | None
    compression_exempt: bool

    def __post_init__(self) -> None:
        if self.kind not in SOURCE_KINDS:
            raise PacketError(f"a packet source is one of {SOURCE_KINDS}")
        if not isinstance(self.ref, str) or not self.ref.strip():
            raise PacketError("a packet source names its ref")
        if not isinstance(self.text, str):
            raise PacketError("a packet source carries its exact text")

    @property
    def byte_count(self) -> int:
        return utf8_size(self.text)


@dataclasses.dataclass(frozen=True, slots=True)
class ContextPacket:
    """A bounded context packet: purpose, sources with refs, bound scope, and
    expiry, plus the posture under which it was assembled."""

    purpose: str
    scope: ScopeKey
    posture: str
    sources: tuple[PacketSource, ...]
    issued_at: float
    expires_at: float
    provider_id: str = PROVIDER_NONE
    reduced_reason: str | None = None
    absent_threads: tuple[str, ...] = ()
    # Evidence the bounds rail SELECTED OUT so the packet would fit. Named
    # rather than counted, because "lossless by reference" is only true if the
    # packet says which references it is standing on (task 10.3/F2).
    dropped_evidence: tuple[str, ...] = ()
    # How much of this tile's staged set the derived index covered, and why
    # the rest is missing. A shortfall means refs that ARE confined were not
    # retrievable this turn, which the declaration must state rather than let a
    # reader infer full coverage from silence (F6).
    corpus_coverage: "CorpusCoverage | None" = None
    # The revision the evidence BYTES were read at. Evidence comes from the
    # served checkout at the projection's own revision — never from the
    # session worktree — so a packet that carries evidence has to say which
    # bytes those are (F5).
    source_revision: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.provider_id, str) or not self.provider_id.strip():
            raise PacketError(
                "a packet names the retrieval provider profile that produced "
                "its evidence, or declares that none was reached")
        if self.posture not in (POSTURE_FULL, POSTURE_REDUCED):
            raise PacketError(
                f"a packet posture is {POSTURE_FULL!r} or {POSTURE_REDUCED!r}")
        if self.posture == POSTURE_REDUCED and not self.reduced_reason:
            raise PacketError(
                "a reduced packet STATES the reduced posture's reason; a "
                "reduction nobody can read is a silent degradation")
        # `is not None`, NOT truthiness (Copilot review of PR #256, finding 1,
        # extended to the CONSTRUCTION gate by the contract-v1.40 slice). This
        # read `and self.reduced_reason`, so `reduced_reason=""` constructed a
        # FULL packet carrying a reduction-reason field — and the release claims
        # in writing that this type, the released shape and the delegated
        # validator "assert this one rule". They did not agree at the blank
        # string: the shape forbids the field's PRESENCE on a full posture and
        # this forbade only a useful value. Aligned so the claim is true.
        #
        # The REDUCED arm above is deliberately left on truthiness: there a blank
        # is refused for being unusable, which is the shape's `minLength: 1`. Two
        # rules, not one predicate.
        if self.posture == POSTURE_FULL and self.reduced_reason is not None:
            raise PacketError(
                "a full packet carries no reduction reason")
        if self.expires_at <= self.issued_at:
            raise PacketError("a packet expires after it is issued")
        if self.corpus_coverage is not None and not isinstance(
                self.corpus_coverage, CorpusCoverage):
            # THE ONE FIELD WITH NO CONSTRUCTOR VALIDATION, until now. It used
            # to be a plain `(indexed, total)` tuple, and a caller still passing
            # one — a stale test, a §11 seam written against the old shape —
            # would sail through construction and then raise `AttributeError`
            # deep inside `declaration_text`, which is the T104 F4 class: a
            # failure that kills the handler mid-turn and drops the connection
            # instead of refusing. Refused HERE, where the wrong shape arrives.
            raise PacketError(
                "corpus_coverage is a CorpusCoverage; it stopped being a "
                "(indexed, total) tuple when the two omission classes had to "
                "be told apart")

    # -- readers -----------------------------------------------------------

    def refs(self) -> tuple[str, ...]:
        return tuple(source.ref for source in self.sources)

    def of_kind(self, kind: str) -> tuple[PacketSource, ...]:
        return tuple(source for source in self.sources if source.kind == kind)

    @property
    def byte_count(self) -> int:
        return sum(source.byte_count for source in self.sources)

    @property
    def exempt_count(self) -> int:
        return sum(1 for source in self.sources if source.compression_exempt)


def require_valid(packet: ContextPacket, *, purpose: str, scope: ScopeKey,
                  now: float) -> ContextPacket:
    """Refuse a packet presented for another purpose, another scope, or after
    it expired. A consuming surface calls this and asks for a NEW packet on
    refusal; it never uses the one it was handed."""

    if not isinstance(packet, ContextPacket):
        raise PacketRejected("a context packet was expected")
    if packet.purpose != purpose:
        raise PacketPurposeMismatch(
            f"this packet was issued for {packet.purpose!r} and was presented "
            f"for {purpose!r}: request a new packet for the actual purpose")
    if packet.scope != scope:
        raise PacketScopeMismatch(
            "this packet was issued for another scope: request a new packet "
            "for the scope actually in hand")
    if now >= packet.expires_at:
        raise PacketExpired(
            "this packet's declared expiry has passed: request a new packet, "
            "which re-runs the rails")
    return packet


# ---------------------------------------------------------------------------
# RAIL 1 — CONFINEMENT (task 10.5), before any retrieval provider is reached
# ---------------------------------------------------------------------------


def confined_refs(projection: ScopeProjection,
                  promoted_findings: Sequence[str] = ()) -> frozenset[str]:
    """The ONLY refs evidence may be drawn from: this tile's own staged set,
    plus the promoted findings.

    ``projection.context_paths`` IS the tile's staged set — every resolved
    document this tile's scope contains, and nothing from another tile. The
    promoted findings are passed in because promotion is a lifecycle act
    performed elsewhere; this rail confines, it does not decide what was
    promoted.

    Computed BEFORE any provider is asked anything, and handed to the provider
    rather than left for it to respect."""

    if not isinstance(projection, ScopeProjection):
        raise PacketError("the confinement rail reads a scope projection")
    refs = set(projection.context_paths)
    for ref in promoted_findings:
        if not isinstance(ref, str) or not ref.strip():
            raise PacketError("a promoted finding is named by its ref")
        refs.add(ref)
    return frozenset(refs)


def thread_signals(threads: Mapping[str, DocumentThread]) -> frozenset[str]:
    """The refs the session's own threads already cite — the third retrieval
    signal, drawn from the STRUCTURED thread-states rather than from their
    prose."""

    signals: set[str] = set()
    for thread in threads.values():
        signals.update(thread.state.evidence_refs)
        for fact in thread.state.accepted_facts:
            if fact.evidence:
                signals.add(fact.evidence)
    return frozenset(signals)


# ---------------------------------------------------------------------------
# RAIL 2 — SELECTION (compression layer one, lossless by reference)
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class _Evidence:
    ref: str
    text: str


# The refusal classes a retrieval backend behind the port may raise, which the
# assembler turns into the DECLARED reduced posture rather than into a dead
# turn. Deliberately NOT a bare `Exception` (that would swallow defects), and
# deliberately not `doxbench_knowledge.KnowledgeError` by import: the knowledge
# seam is duck-typed, and importing it here to name one exception would turn an
# injected collaborator into a hard dependency. `KnowledgeError` derives from
# `ValueError`, so it is caught by the first entry.
RETRIEVAL_FAILURES = (ValueError, LookupError, OSError, TimeoutError)


def selection_rail(
    *,
    selected_key: str | None,
    loaded_keys: Sequence[str],
    threads: Mapping[str, DocumentThread],
    evidence: Sequence[_Evidence] = (),
) -> tuple[tuple[PacketSource, ...], tuple[str, ...]]:
    """The selected document's thread IN FULL, the other loaded documents'
    thread STATE HEADERS only, then the selected evidence — in that order.

    Returns the sources and the loaded documents that have NO thread yet. An
    absent thread produces NO section and is named in the packet's declaration
    instead: an invented empty thread would be a claim that a conversation
    happened."""

    sources: list[PacketSource] = []
    absent: list[str] = []
    if selected_key is not None:
        thread = threads.get(selected_key)
        if thread is None:
            absent.append(selected_key)
        else:
            sources.append(PacketSource(
                ref=selected_key, kind=SOURCE_SELECTED_THREAD,
                text=render_thread(thread), status=None,
                compression_exempt=False))
    for key in loaded_keys:
        if key == selected_key:
            continue
        thread = threads.get(key)
        if thread is None:
            absent.append(key)
            continue
        sources.append(PacketSource(
            ref=key, kind=SOURCE_THREAD_STATE,
            text=render_state_header(thread), status=None,
            compression_exempt=False))
    for item in evidence:
        sources.append(PacketSource(
            ref=item.ref, kind=SOURCE_EVIDENCE, text=item.text,
            status=None, compression_exempt=False))
    return tuple(sources), tuple(absent)


# ---------------------------------------------------------------------------
# RAIL 3 — THE LIFECYCLE-STATUS EXEMPTION (task 10.3)
# ---------------------------------------------------------------------------


def exemption_rail(
    sources: Sequence[PacketSource],
) -> tuple[PacketSource, ...]:
    """Mark approved/ratified content EXEMPT from aggressive compression,
    keyed on each item's OWN ``Status:`` header, read here.

    Upstream of any compressor by construction: this runs inside the assembler,
    before the packet exists, and the marking travels WITH the item. It is
    never delegated — a compressor that cannot read a lifecycle status could
    not apply it, and one that could would be a second place this rule lives."""

    marked: list[PacketSource] = []
    for source in sources:
        status = lifecycle_status(source.text)
        marked.append(dataclasses.replace(
            source, status=status,
            compression_exempt=is_compression_exempt(source.text)))
    return tuple(marked)


# ---------------------------------------------------------------------------
# RAIL 4 — THE BOUNDS CHECK (task 10.3)
# ---------------------------------------------------------------------------


def bounds_rail(
    sources: Sequence[PacketSource],
    *,
    max_bytes: int = MAX_PACKET_BYTES,
    max_sources: int = MAX_PACKET_SOURCES,
) -> tuple[tuple[PacketSource, ...], tuple[str, ...]]:
    """Make the packet FIT its bound by SELECTING less, and refuse only when
    selecting less cannot help.

    Two different things were being conflated before this rail was written the
    way it is now, and the difference is the whole reason layer one has a
    fidelity contract:

      * EVIDENCE is what the knowledge service SELECTED. Carrying less of it is
        selection, which is LOSSLESS BY REFERENCE — the packet names what it
        dropped and every dropped ref is one retrieval call away. So an
        oversized packet drops evidence from the LOWEST-RANKED end until it
        fits, and names what it dropped. No source is ever shortened: a source
        is carried whole or not at all, which is what keeps this selection
        rather than truncation.
      * THE THREADS are not selected — they are the session's own working
        memory, and the packet is the only place they appear. There is nothing
        to drop, so if they alone exceed the bound the packet REFUSES, naming
        the measured dimension. That refusal is actionable: layer two
        (`compact_thread`) exists precisely to bring a thread back inside a
        bound.

    Ranking is the selection criterion, so the fit is GREEDY BY RANK: evidence
    is walked best-ranked first and an item is kept when it fits the remaining
    budget and dropped when it does not. Dropping strictly from the tail was
    the obvious alternative and is worse — one oversized top hit would evict
    every smaller, better-than-nothing item behind it, so the packet would end
    up carrying nothing at all rather than the three items that fit.

    The lifecycle-status exemption deliberately does NOT reorder this: that
    exemption governs aggressive COMPRESSION, and fitting-by-rank is selection.
    Reading it as a selection priority would be one layer claiming another's
    job, which the fidelity contracts exist to prevent.

    THE CONSEQUENCE, STATED (re-verify NF7): a ratified or standard canon
    document CAN be dropped here — by its byte size and its rank, like anything
    else — while a draft that fits is carried. That is not the exemption
    failing; the exemption promises such a document will not be aggressively
    COMPRESSED if it is carried, and promises nothing about whether selection
    carries it. The dropped ref is named, so the reader can see it went.

    Returns the sources that fit, in their original order, and the refs that
    were dropped, in rank order."""

    rows = tuple(sources)
    max_bytes = max(0, int(max_bytes))
    max_sources = max(0, int(max_sources))
    fixed = [row for row in rows if row.kind != SOURCE_EVIDENCE]
    fixed_bytes = sum(row.byte_count for row in fixed)
    if len(fixed) > max_sources:
        raise PacketBoundExceeded("context_packet_sources", len(fixed),
                                  max_sources)
    if fixed_bytes > max_bytes:
        raise PacketBoundExceeded("context_packet_bytes", fixed_bytes,
                                  max_bytes)

    kept: set[int] = set()
    dropped: list[str] = []
    remaining_bytes = max_bytes - fixed_bytes
    remaining_slots = max_sources - len(fixed)
    for index, row in enumerate(rows):
        if row.kind != SOURCE_EVIDENCE:
            continue
        if remaining_slots > 0 and row.byte_count <= remaining_bytes:
            kept.add(index)
            remaining_bytes -= row.byte_count
            remaining_slots -= 1
        else:
            dropped.append(row.ref)

    fitted = tuple(row for index, row in enumerate(rows)
                   if row.kind != SOURCE_EVIDENCE or index in kept)
    return fitted, tuple(dropped)


# ---------------------------------------------------------------------------
# ASSEMBLY (task 10.3/10.4/10.7)
# ---------------------------------------------------------------------------


def assemble_packet(
    *,
    projection: ScopeProjection,
    scope: ScopeKey,
    selected_key: str | None,
    loaded_keys: Sequence[str],
    query: str,
    threads: Mapping[str, DocumentThread] | None = None,
    knowledge: object | None = None,
    promoted_findings: Sequence[str] = (),
    evidence_limit: int = DEFAULT_EVIDENCE_LIMIT,
    already_carried: Sequence[str] = (),
    corpus_coverage: "CorpusCoverage | None" = None,
    max_packet_bytes: int = MAX_PACKET_BYTES,
    clock: Callable[[], float] = time.monotonic,
    ttl_seconds: float = PACKET_TTL_SECONDS,
) -> ContextPacket:
    """Assemble one turn's bounded context packet, rails in the declared order.

    ``knowledge`` is the tool boundary, duck-typed exactly as the model port is
    (``search`` and ``get_source``). ``None`` is a POSTURE, not an error: the
    result is the DECLARED reduced packet — the selected thread and the loaded
    buffers, with the reduction stated — and the rails still run.

    ``already_carried`` are refs the prompt carries verbatim in their own
    sections (the outline and every loaded document buffer). Evidence excludes
    them, because a document carried twice spends the packet's bound on bytes
    the prompt already has, and a reader cannot tell which copy is authoritative.
    """

    threads = dict(threads or {})
    loaded = tuple(loaded_keys)
    confined = confined_refs(projection, promoted_findings)
    carried = set(already_carried) | set(loaded)
    if selected_key is not None:
        carried.add(selected_key)

    posture = POSTURE_FULL
    reduced_reason: str | None = None
    provider_id = PROVIDER_NONE
    evidence: list[_Evidence] = []
    if knowledge is None:
        posture = POSTURE_REDUCED
        reduced_reason = REDUCED_NO_KNOWLEDGE_SERVICE
    else:
        try:
            profile = knowledge.profile()
            provider_id = getattr(profile, "profile_id", PROVIDER_NONE)
            available = frozenset(ref for ref in confined if ref not in carried)
            hits = knowledge.search(
                query, confined_to=available, limit=evidence_limit,
                thread_signals=thread_signals(threads))
            for hit in hits:
                ref = getattr(hit, "ref", None)
                # RE-FILTERED AT THE ASSEMBLER as well as at the provider. A
                # retrieval that would return material outside the tile's staged
                # set and the promoted findings has it EXCLUDED here, whatever
                # the backend behind the port believed.
                if not isinstance(ref, str) or ref not in available:
                    continue
                source = knowledge.get_source(ref, confined_to=available)
                text = getattr(source, "text", None)
                if not isinstance(text, str):
                    continue
                evidence.append(_Evidence(ref=ref, text=text))
        except RETRIEVAL_FAILURES:
            # A BACKEND THAT REFUSES IS THE DEGRADED POSTURE, not a dead turn.
            # v1's in-process backend cannot realistically fail here, but the
            # port exists so another one can sit behind it, and "the knowledge
            # service cannot answer" is a case the delta already rules on: the
            # turn degrades to the declared reduced packet. Evidence gathered
            # before the failure is discarded rather than half-carried, because
            # a packet claiming full posture with an arbitrary prefix of its
            # evidence would be a worse answer than the honest reduced one.
            posture = POSTURE_REDUCED
            reduced_reason = REDUCED_RETRIEVAL_REFUSED
            provider_id = PROVIDER_NONE
            evidence = []

    selected, absent = selection_rail(
        selected_key=selected_key, loaded_keys=loaded, threads=threads,
        evidence=tuple(evidence))
    marked = exemption_rail(selected)
    bounded, dropped = bounds_rail(marked, max_bytes=max_packet_bytes)
    issued = float(clock())
    return ContextPacket(
        purpose=PACKET_PURPOSE_CHAT_TURN,
        scope=scope,
        posture=posture,
        sources=bounded,
        issued_at=issued,
        expires_at=issued + float(ttl_seconds),
        provider_id=provider_id,
        reduced_reason=reduced_reason,
        absent_threads=absent,
        dropped_evidence=dropped,
        corpus_coverage=corpus_coverage,
        source_revision=(projection.source_revision or None) if evidence else None,
    )


def reduced_packet(
    *,
    projection: ScopeProjection,
    scope: ScopeKey,
    selected_key: str | None,
    loaded_keys: Sequence[str],
    threads: Mapping[str, DocumentThread] | None = None,
    clock: Callable[[], float] = time.monotonic,
    ttl_seconds: float = PACKET_TTL_SECONDS,
) -> ContextPacket:
    """The DECLARED degraded posture, spelled once.

    It is exactly ``assemble_packet`` with no knowledge service, which is the
    point: the reduced packet is not a different pipeline with the rails
    skipped, it is the same pipeline with one input absent."""

    return assemble_packet(
        projection=projection, scope=scope, selected_key=selected_key,
        loaded_keys=loaded_keys, query="", threads=threads, knowledge=None,
        clock=clock, ttl_seconds=ttl_seconds)


# ---------------------------------------------------------------------------
# the packet's PROMPT SECTIONS (task 5.4's packet half)
# ---------------------------------------------------------------------------

# The four section GROUPS the packet contributes to `PROMPT_SECTION_ORDER`, in
# design §3.1 step 5's own order: the packet's declaration, the selected
# thread, the other threads' state headers, then the evidence with refs. Two of
# them EXPAND (one section per other thread, one per evidence item) exactly as
# `document_buffers` does, and `expand_group` is the one place that expansion
# is decided so the concrete keys and the rendered sections cannot disagree.
PACKET_SECTION_DECLARATION = "context_packet"
PACKET_SECTION_THREAD_STATES = "thread_state_headers"
PACKET_SECTION_EVIDENCE = "evidence"

PACKET_SECTION_GROUPS: tuple[str, ...] = (
    PACKET_SECTION_DECLARATION,
    PACKET_SECTION_SELECTED_THREAD,
    PACKET_SECTION_THREAD_STATES,
    PACKET_SECTION_EVIDENCE,
)

_LOSSLESS_NOTE = (
    "Material this packet does not carry is NOT lost: selection is lossless "
    "BY REFERENCE — the packet names what it carries, and anything omitted "
    "from the covered corpus is one retrieval call away. Where a line above "
    "says otherwise, that line is the exception and this sentence does not "
    "override it."
)


def expand_group(group: str, packet: ContextPacket | None) -> tuple[str, ...]:
    """The concrete section keys one packet group contributes, in order.

    A group whose packet has nothing contributes NOTHING — no empty section, no
    placeholder — because a section announcing that it is empty is a claim the
    prompt does not need to make twice: the declaration section already names
    every absence."""

    if group not in PACKET_SECTION_GROUPS:
        raise PacketError(f"{group!r} is not a packet section group")
    if packet is None:
        return ()
    if group == PACKET_SECTION_DECLARATION:
        return (PACKET_SECTION_DECLARATION,)
    if group == PACKET_SECTION_SELECTED_THREAD:
        return tuple(PACKET_SECTION_SELECTED_THREAD
                     for _ in packet.of_kind(SOURCE_SELECTED_THREAD))
    if group == PACKET_SECTION_THREAD_STATES:
        return tuple(THREAD_STATE_SECTION_PREFIX + source.ref
                     for source in packet.of_kind(SOURCE_THREAD_STATE))
    return tuple(EVIDENCE_SECTION_PREFIX + source.ref
                 for source in packet.of_kind(SOURCE_EVIDENCE))


def _exemption_label(source: PacketSource) -> str:
    if source.compression_exempt:
        return "EXEMPT from aggressive compression"
    return "ordinary compression"


def _status_label(source: PacketSource) -> str:
    if source.status is None:
        return "no Status: header"
    return f"Status: {source.status}"


def declaration_text(packet: ContextPacket) -> str:
    """The packet's own declaration, rendered for the prompt: what it is for,
    what scope it is bound to, when it expires, exactly what it carries with
    refs, and — when the posture is reduced — that it is reduced and why."""

    lines = [
        "CONTEXT PACKET — this turn's bounded context, assembled and bounded "
        "before any retrieval or model provider was reached.",
        f"purpose: {packet.purpose}",
        f"scope: repository={packet.scope.repository} ref={packet.scope.ref} "
        f"tile_kind={packet.scope.tile_kind} tile_id={packet.scope.tile_id}",
        f"posture: {packet.posture}",
        f"retrieval provider profile: {packet.provider_id}",
        f"expires: {packet.expires_at - packet.issued_at:.0f} seconds after "
        "issue, after which it is invalid and a new packet must be requested",
    ]
    if packet.reduced_reason:
        lines.append(f"reduced because: {packet.reduced_reason}")
    lines.append(
        f"carries {len(packet.sources)} source(s), of which "
        f"{packet.exempt_count} are exempt from aggressive compression:")
    for source in packet.sources:
        lines.append(DECLARATION_LINE.format(
            kind=source.kind, ref=source.ref,
            status=_status_label(source),
            exemption=_exemption_label(source)))
    if not packet.sources:
        lines.append("  (none)")
    if packet.absent_threads:
        lines.append(
            "no thread exists yet for: "
            + ", ".join(packet.absent_threads)
            + " — nothing has been mirrored into those sidecars, so no thread "
              "is claimed for them")
    if packet.of_kind(SOURCE_EVIDENCE) or packet.dropped_evidence:
        # F5: evidence is the SERVED CHECKOUT's bytes at the projection's own
        # revision. A session's unsaved work rides as buffers, and a session's
        # SAVED work lands in the session worktree, which this evidence has not
        # been read from — so the packet says which bytes these are rather than
        # letting a reader assume they are the session's.
        #
        # THE CAVEAT IS NOT CONDITIONAL ON THE STRING IT WARNS ABOUT (re-verify
        # NF4). This used to be gated on `packet.source_revision`, so a
        # projection whose snapshot declared no revision dropped the whole
        # disclosure — the worktree warning vanished exactly where the reader
        # had least information. The condition is now "does this packet stand
        # on retrieved bytes at all", which is what the warning is about, and a
        # missing revision is SAID rather than used as a reason to say nothing.
        lines.append(
            f"evidence bytes are the served checkout at revision "
            f"{packet.source_revision or 'unknown'} — NOT this session's "
            "worktree, so a document saved or created in this session appears "
            "here at its pre-session bytes, or not at all")
    if packet.dropped_evidence:
        lines.append(
            "selected out to fit this packet's bound, best-ranked first: "
            + ", ".join(packet.dropped_evidence)
            + " — each is named because it remains one retrieval call away; "
              "nothing was shortened")
    if packet.corpus_coverage is not None:
        # "THE INDEX covered", not "retrieval covered" (re-verify NF2): the
        # number is about what was INDEXED, and under the reduced-retrieval
        # posture no retrieval happened at all — so the two sentences would
        # contradict each other on the same packet.
        coverage = packet.corpus_coverage
        if coverage.complete:
            lines.append(
                f"the index covered all {coverage.total} documents in this "
                "tile's staged set")
        else:
            causes = []
            if coverage.unreadable:
                causes.append(
                    f"{coverage.unreadable} could not be read at this revision")
            if coverage.beyond_bound:
                causes.append(
                    f"{coverage.beyond_bound} were beyond the declared index "
                    "bound")
            lines.append(
                f"the index covered {coverage.indexed} of {coverage.total} "
                f"documents in this tile's staged set: "
                + " and ".join(causes)
                + " — those were NOT retrievable for this turn, so they are "
                  "not one retrieval call away either")
    lines.append(_LOSSLESS_NOTE)
    return "\n".join(lines)


def packet_sections(
    packet: ContextPacket | None,
) -> tuple[tuple[str, str], ...]:
    """Every (key, text) pair the packet contributes, in the declared order.

    The keys returned here are exactly the keys ``expand_group`` declares for
    the same packet, which a companion test asserts directly rather than by
    reading both and hoping."""

    if packet is None:
        return ()
    sections: list[tuple[str, str]] = [
        (PACKET_SECTION_DECLARATION, declaration_text(packet)),
    ]
    for source in packet.of_kind(SOURCE_SELECTED_THREAD):
        sections.append((
            PACKET_SECTION_SELECTED_THREAD,
            SELECTED_THREAD_PREAMBLE.format(
                ref=source.ref, note=_NON_AUTHORITATIVE_NOTE) + source.text))
    for source in packet.of_kind(SOURCE_THREAD_STATE):
        sections.append((
            THREAD_STATE_SECTION_PREFIX + source.ref,
            THREAD_STATE_PREAMBLE.format(
                ref=source.ref, note=_NON_AUTHORITATIVE_NOTE) + source.text))
    for source in packet.of_kind(SOURCE_EVIDENCE):
        sections.append((
            EVIDENCE_SECTION_PREFIX + source.ref,
            EVIDENCE_PREAMBLE.format(
                ref=source.ref, status=_status_label(source),
                exemption=_exemption_label(source)) + source.text))
    return tuple(sections)
