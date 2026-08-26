"""The doxBench STAGED-SET KNOWLEDGE SERVICE, v1
(add-doxbench-editing-phase-b, design §3.3 / D10 / D11, tasks §10.1, §10.2,
§10.5, §10.6).

Two layers, and keeping them apart is the whole shape of this module:

  * the **tool boundary** — what a CALLER sees. Exactly four tools
    (``search``, ``get_source``, ``promote_finding``, ``reindex``) and one
    RESERVED name (``graph_query``) that is declared and unimplemented so its
    later arrival is not a boundary change; and
  * the internal **ASSEMBLY PORT** — what a PROVIDER implements. Four members,
    product-neutral, with every other spelling banned by a companion test the
    way ``WorkbenchModelPort``'s is.

A backend swap changes neither, which is what makes the port worth having.

**IT IS AN IN-PROCESS BOUNDARY, AND SAYING SO IS THE POINT.** The ratified
delta asks for "exactly ONE tool boundary declaring a small tool contract" and
never says MCP; an earlier draft of this docstring called it "the MCP tool
boundary", which named a protocol nothing here speaks. The requirement is
satisfied by the boundary being ONE and being small, not by its transport. The
STDIO MCP server that exposes these same four tools to the harness — and the
mount-name pin `verification-findings.md` §3.2 asks for, `xd://mcp__<server>__
<tool>` — belong to the §11 bridge slice, which is the first thing that will
have a harness to expose them to.

**v1 IS GRAPH-LESS, and that is a recorded finding rather than a taste.** The
profile behind the port is LOCAL-HYBRID: lexical retrieval (BM25 over the
confined corpus) plus small embedded vectors (a deterministic hashed
token/character-n-gram projection computed here, in-process, from stdlib
``hashlib`` — no model, no download, no service) plus the structured
thread-states the session already holds. There is NO graph engine, graph store,
or graph index anywhere in this module, and ``graph_query`` stays unimplemented
until a concrete GRADUATION TRIGGER is recorded: a recurring need for
dependency traversal, contradiction detection, or change-impact analysis.

**The backend is an INSTALL-TIME DECLARATION** (D11). A turn, a prompt, or a
heuristic MUST NOT pick one, so no function here takes a turn, a message, or a
prompt at all, and a companion test asserts that against the signatures rather
than against a comment. The ratified two-case principle is enforced: a
self-hosted install declares the local-embedded profile; a hosted backend
exists only where a TENANT install declares one, and v1 ships no hosted
provider, so such a declaration resolves to an honest refusal naming the gap
rather than to a silent local fallback.

**CONFINEMENT.** Retrieval answers only within a confined ref set the CALLER
computed — the tile's own staged set plus promoted findings — and re-filters
its own answers against it, so a backend that returned something else has that
answer dropped rather than trusted. Nothing this module returns ever joins the
loaded buffer set: it has no route to one, holds no buffer type, and creates no
state.

**PROMOTION IS GATE-ONLY.** ``promote_finding`` writes nothing and stores
nothing. It returns a request naming the REVIEWED ACT that creates the target
object, read from this surface's own ``memory-gateway`` declaration so the act
has one spelling. There is no parallel decision store here, and a companion
test asserts the absence against this module's source.

Stdlib only, in-process, no network, no credential, no filesystem: the corpus
arrives through ``reindex`` and a caller-supplied reader seam, so this module
performs no I/O of its own.
"""

from __future__ import annotations

import dataclasses
import hashlib
import math
import re
import types
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Protocol, runtime_checkable

from ideation_dashboard.doxbench_memory_gateway import DECLARATION

# ---------------------------------------------------------------------------
# refusals
# ---------------------------------------------------------------------------


class KnowledgeError(ValueError):
    """Base class for every refusal this module raises."""


class BackendDeclarationRefused(KnowledgeError):
    """Raised when an install-time backend declaration is malformed or breaks
    the ratified two-case principle."""


class BackendUnavailable(KnowledgeError):
    """Raised when a DECLARED backend has no provider in this release. Distinct
    from a malformed declaration: the declaration was legal, the release simply
    does not ship that provider, and saying so is better than falling back to
    a backend the operator did not declare."""


class ReservedToolUnimplemented(KnowledgeError):
    """Raised when a caller invokes a RESERVED tool name.

    A fixed, boundary-shaped refusal rather than ``NotImplementedError``: the
    reservation is the point, so the name must EXIST at the boundary and answer
    the same way every time, and a caller must be able to tell "reserved, not
    yet admitted" from "this crashed"."""


class UnknownTool(KnowledgeError):
    """Raised when a caller invokes a name the boundary does not declare at
    all. Separate from the reserved refusal so a typo never reads as a
    governance verdict."""


class RetrievalRefused(KnowledgeError):
    """Raised when a retrieval call is malformed — an unbounded limit, an
    unconfined request, or a query that is not text."""


# ---------------------------------------------------------------------------
# the corpus and the hits
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class IndexedSource:
    """One document in the derived index: its repository-relative ref and its
    exact text.

    NO lifecycle status field, deliberately. The lifecycle-status exemption is
    applied BY THE ASSEMBLER, reading each item's own ``Status:`` header, and a
    status cached here would be a second copy of that fact for the assembler to
    trust instead of reading — which is precisely the delegation the contract
    forbids."""

    ref: str
    text: str

    def __post_init__(self) -> None:
        if not isinstance(self.ref, str) or not self.ref.strip():
            raise RetrievalRefused("an indexed source names its ref")
        if not isinstance(self.text, str):
            raise RetrievalRefused("an indexed source carries its exact text")


@dataclasses.dataclass(frozen=True, slots=True)
class RetrievalHit:
    """One selected candidate: the ref, the fused score, and the three signal
    scores that produced it, so a reader can see WHICH signal selected a
    document rather than only that something did."""

    ref: str
    score: float
    lexical: float
    vector: float
    thread: float


@dataclasses.dataclass(frozen=True, slots=True)
class IndexReport:
    """What a reindex did, in counts. Content-free by construction."""

    profile_id: str
    source_count: int
    term_count: int


# ---------------------------------------------------------------------------
# the provider profile — capability declared, authority NOT granted
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class ProviderProfile:
    """A retrieval backend's declared capability.

    ``memory-gateway``'s `Provider Profiles Declare Capability` in this
    surface's own terms: what the backend can do, what it is not, and what it
    does NOT hold. ``graph`` is declared FALSE rather than omitted, because an
    omitted capability is one a reader has to guess about, and this is the
    exact capability the graduation gate governs."""

    profile_id: str
    signals: tuple[str, ...]
    graph: bool
    networked: bool
    credentialed: bool
    notes: str

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, str) or not self.profile_id.strip():
            raise BackendDeclarationRefused("a provider profile names itself")
        if self.graph:
            raise BackendDeclarationRefused(
                "no provider profile in this release may declare a graph "
                "capability: a graph engine, store, or index is admitted only "
                "when a concrete graduation trigger is recorded, and the "
                "reserved tool name stays unimplemented until then")


SIGNAL_LEXICAL = "lexical"
SIGNAL_VECTOR = "embedded-vector"
SIGNAL_THREAD_STATE = "thread-state"

PROFILE_LOCAL_EMBEDDED = "local-embedded"

LOCAL_EMBEDDED_PROFILE = ProviderProfile(
    profile_id=PROFILE_LOCAL_EMBEDDED,
    signals=(SIGNAL_LEXICAL, SIGNAL_VECTOR, SIGNAL_THREAD_STATE),
    graph=False,
    networked=False,
    credentialed=False,
    notes=(
        "in-process local hybrid retrieval: BM25 over the confined corpus, a "
        "deterministic hashed n-gram projection computed from stdlib hashing, "
        "and the structured thread-states the session already holds; no model "
        "is downloaded, no service is reached, and no credential exists"),
)


# ---------------------------------------------------------------------------
# THE ASSEMBLY PORT (task 10.1)
# ---------------------------------------------------------------------------

# The four product-neutral members a retrieval backend implements. Deliberately
# NOT the tool names: the tool contract is what a caller sees and the port is
# what a provider implements, and giving them one vocabulary would make a
# backend swap look like a boundary change the first time the two needed to
# differ.
ASSEMBLY_PORT_MEMBERS: tuple[str, ...] = (
    "profile", "index", "retrieve", "source")


@runtime_checkable
class RetrievalAssemblyPort(Protocol):
    """The internal assembly port: the product-neutral surface a retrieval
    backend implements, behind the one tool boundary."""

    def profile(self) -> ProviderProfile:
        """The backend's declared capability."""

    def index(self, sources: Sequence[IndexedSource]) -> IndexReport:
        """Build the derived index from the confined corpus, replacing any
        previous one. A derived projection, reproducible from the sources."""

    def retrieve(self, query: str, *, confined_to: frozenset[str],
                 limit: int,
                 thread_signals: frozenset[str] = frozenset()
                 ) -> tuple[RetrievalHit, ...]:
        """Ranked candidates, drawn ONLY from ``confined_to``."""

    def source(self, ref: str) -> IndexedSource | None:
        """The exact indexed source for a ref, or None."""


# ---------------------------------------------------------------------------
# the install-time backend declaration (task 10.6, design D11)
# ---------------------------------------------------------------------------

INSTALL_SELF_HOSTED = "self_hosted"
INSTALL_TENANT = "tenant"
INSTALL_CLASSES: tuple[str, ...] = (INSTALL_SELF_HOSTED, INSTALL_TENANT)


@dataclasses.dataclass(frozen=True, slots=True)
class RetrievalBackendDeclaration:
    """What an INSTALL declares its retrieval backend to be.

    Read at server construction from the entrypoint that builds the serve, in
    the same shape every other doxBench capability is declared in: the library
    default is ABSENCE, absence is a posture rather than an error, and the
    production entrypoint names what it wants. An operator can therefore read
    what their install talks to, which is the whole reason the declaration
    exists.

    ``declared_by`` names the site that made the declaration, so a reader of a
    running server can find where to change it."""

    installation: str
    profile_id: str
    networked: bool
    credentialed: bool
    declared_by: str

    def __post_init__(self) -> None:
        if self.installation not in INSTALL_CLASSES:
            raise BackendDeclarationRefused(
                f"installation must be one of {INSTALL_CLASSES}")
        for name in ("profile_id", "declared_by"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise BackendDeclarationRefused(
                    f"a backend declaration names its {name}")
        for name in ("networked", "credentialed"):
            if not isinstance(getattr(self, name), bool):
                raise BackendDeclarationRefused(f"{name} is a declared fact")
        # THE RATIFIED TWO-CASE PRINCIPLE, enforced rather than described:
        # local-embedded for a self-hosted install, a hosted backend only where
        # a TENANT install declares one.
        if self.installation == INSTALL_SELF_HOSTED:
            if self.profile_id != PROFILE_LOCAL_EMBEDDED:
                raise BackendDeclarationRefused(
                    "a self-hosted install declares the local-embedded "
                    f"profile; {self.profile_id!r} is a hosted backend, which "
                    "only a tenant install may declare")
            if self.networked or self.credentialed:
                raise BackendDeclarationRefused(
                    "the local-embedded profile is neither networked nor "
                    "credentialed; a declaration saying otherwise describes a "
                    "different backend")
        elif self.profile_id == PROFILE_LOCAL_EMBEDDED and (
                self.networked or self.credentialed):
            raise BackendDeclarationRefused(
                "the local-embedded profile is neither networked nor "
                "credentialed, whoever declares it")


SELF_HOSTED_LOCAL_EMBEDDED = RetrievalBackendDeclaration(
    installation=INSTALL_SELF_HOSTED,
    profile_id=PROFILE_LOCAL_EMBEDDED,
    networked=False,
    credentialed=False,
    declared_by="the doxBench serve entrypoint (the self-hosted install case)",
)


# ---------------------------------------------------------------------------
# the v1 LOCAL-HYBRID backend (task 10.1)
# ---------------------------------------------------------------------------

# Tokenization: one declared rule, applied to queries and documents alike, so
# the two can never disagree about what a word is.
_TOKEN_RULE = re.compile(r"[0-9a-z]+")

# BM25's two dials at their standard values, named rather than inlined.
BM25_K1 = 1.2
BM25_B = 0.75

# The embedded vectors are SMALL on purpose: 96 dimensions of a hashed n-gram
# projection is enough for near-duplicate and morphological similarity over a
# tile-sized corpus, and small enough that building one is arithmetic rather
# than a dependency. `hashlib.blake2b` is used rather than `hash()` because
# Python's string hashing is randomized per process, and a retrieval that
# ranked differently on every restart would be untestable.
EMBEDDING_DIMENSION = 96
CHARACTER_NGRAM = 3

# The fused score's declared weights. They sum to one so a fused score reads on
# the same 0..1 scale its parts do.
WEIGHT_LEXICAL = 0.5
WEIGHT_VECTOR = 0.3
WEIGHT_THREAD = 0.2

# The largest number of candidates one retrieval may return. A bound, because
# an unbounded retrieval feeding a bounded packet just moves the refusal later.
MAX_RETRIEVAL_LIMIT = 24

# Scores are rounded before ordering so the ranking is stable across platforms
# whose floating-point sums associate differently; ties then break on the ref.
_SCORE_PRECISION = 6


def tokenize(text: str) -> tuple[str, ...]:
    """The ONE tokenization rule: lowercase alphanumeric runs."""
    if not isinstance(text, str):
        raise RetrievalRefused("tokenize reads text")
    return tuple(_TOKEN_RULE.findall(text.lower()))


def _features(tokens: Sequence[str]) -> Iterable[str]:
    """The hashed features one text contributes: every token, plus every
    character n-gram inside it.

    The n-grams are what make this a VECTOR signal rather than a second lexical
    one: `contract` and `contracts` share no token but share seven trigrams, so
    a query matches material the BM25 leg alone would rank at zero."""

    for token in tokens:
        yield token
        # `>=`, not `>` (Copilot review of PR #216). A token of EXACTLY
        # `CHARACTER_NGRAM` characters contains exactly one n-gram — itself —
        # and the strict comparison skipped it, so every three-letter token
        # contributed no n-gram feature at all while four-letter tokens
        # contributed two. That contradicted this function's own docstring, and
        # it silently weakened the vector leg for the shortest tokens, which
        # are the ones the lexical leg is already worst at generalizing over.
        if len(token) >= CHARACTER_NGRAM:
            for start in range(len(token) - CHARACTER_NGRAM + 1):
                yield "#" + token[start:start + CHARACTER_NGRAM]


def embed(tokens: Sequence[str]) -> tuple[float, ...]:
    """A deterministic, L2-normalized hashed projection of a token sequence.

    The classic hashing trick: each feature picks a dimension and a sign from
    its own digest, contributions accumulate, and the result is normalized so
    a dot product IS a cosine. No model, no vocabulary file, no download."""

    vector = [0.0] * EMBEDDING_DIMENSION
    for feature in _features(tokens):
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        index = value % EMBEDDING_DIMENSION
        vector[index] += 1.0 if (value >> 63) & 1 else -1.0
    norm = math.sqrt(sum(component * component for component in vector))
    if norm == 0.0:
        return tuple(vector)
    return tuple(component / norm for component in vector)


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


class LocalHybridBackend:
    """The v1 profile behind the assembly port: lexical + small embedded
    vectors + the structured thread-states, in this process, from the stdlib.

    The index is a DERIVED PROJECTION and nothing else: it is rebuilt from the
    sources on every ``index`` call, holds no authority, and can be discarded
    and regenerated at any time from the repository it was derived from."""

    def __init__(self) -> None:
        self._sources: dict[str, IndexedSource] = {}
        self._tokens: dict[str, tuple[str, ...]] = {}
        self._frequencies: dict[str, dict[str, int]] = {}
        self._document_frequency: dict[str, int] = {}
        self._vectors: dict[str, tuple[float, ...]] = {}
        self._average_length = 0.0

    # -- the port ----------------------------------------------------------

    def profile(self) -> ProviderProfile:
        return LOCAL_EMBEDDED_PROFILE

    def index(self, sources: Sequence[IndexedSource]) -> IndexReport:
        rows = tuple(sources)
        for row in rows:
            if not isinstance(row, IndexedSource):
                raise RetrievalRefused("the index is built from IndexedSource")
        self._sources = {row.ref: row for row in rows}
        self._tokens = {row.ref: tokenize(row.text) for row in rows}
        self._frequencies = {}
        self._document_frequency = {}
        self._vectors = {}
        for ref, tokens in self._tokens.items():
            counts: dict[str, int] = {}
            for token in tokens:
                counts[token] = counts.get(token, 0) + 1
            self._frequencies[ref] = counts
            for token in counts:
                self._document_frequency[token] = (
                    self._document_frequency.get(token, 0) + 1)
            self._vectors[ref] = embed(tokens)
        lengths = [len(tokens) for tokens in self._tokens.values()]
        self._average_length = (sum(lengths) / len(lengths)) if lengths else 0.0
        return IndexReport(profile_id=PROFILE_LOCAL_EMBEDDED,
                           source_count=len(self._sources),
                           term_count=len(self._document_frequency))

    def retrieve(self, query: str, *, confined_to: frozenset[str],
                 limit: int,
                 thread_signals: frozenset[str] = frozenset()
                 ) -> tuple[RetrievalHit, ...]:
        if not isinstance(query, str):
            raise RetrievalRefused("a retrieval query is text")
        if not isinstance(confined_to, (set, frozenset)):
            raise RetrievalRefused(
                "a retrieval is confined to a declared ref set; an unconfined "
                "retrieval is the failure this service exists to prevent")
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise RetrievalRefused("a retrieval limit is a positive integer")
        if limit > MAX_RETRIEVAL_LIMIT:
            raise RetrievalRefused(
                f"a retrieval returns at most {MAX_RETRIEVAL_LIMIT} candidates; "
                f"{limit} was asked for")
        if not isinstance(thread_signals, (set, frozenset)):
            raise RetrievalRefused("thread signals arrive as a set of refs")

        # THE CONFINEMENT IS APPLIED FIRST, before any scoring: a document
        # outside the caller's confined set is never scored, never ranked, and
        # never seen again below.
        candidates = tuple(sorted(ref for ref in self._sources
                                  if ref in confined_to))
        if not candidates:
            return ()
        query_tokens = tokenize(query)
        query_vector = embed(query_tokens)
        lexical_raw = {ref: self._bm25(ref, query_tokens) for ref in candidates}
        strongest = max(lexical_raw.values()) if lexical_raw else 0.0
        hits: list[RetrievalHit] = []
        for ref in candidates:
            lexical = (lexical_raw[ref] / strongest) if strongest > 0 else 0.0
            vector = max(0.0, _cosine(query_vector, self._vectors[ref]))
            thread = 1.0 if ref in thread_signals else 0.0
            score = (WEIGHT_LEXICAL * lexical + WEIGHT_VECTOR * vector
                     + WEIGHT_THREAD * thread)
            if round(score, _SCORE_PRECISION) <= 0.0:
                # No signal selected it. An unselected document is left out
                # rather than carried at zero: the packet names what it carries.
                continue
            hits.append(RetrievalHit(
                ref=ref, score=round(score, _SCORE_PRECISION),
                lexical=round(lexical, _SCORE_PRECISION),
                vector=round(vector, _SCORE_PRECISION),
                thread=thread))
        hits.sort(key=lambda hit: (-hit.score, hit.ref))
        selected = tuple(hits[:limit])
        # Re-filtered against the confinement AFTER ranking as well. Belt and
        # braces on purpose: this leg is what holds if a backend swap ever puts
        # a provider here whose own confinement is less careful than this one's.
        return tuple(hit for hit in selected if hit.ref in confined_to)

    def source(self, ref: str) -> IndexedSource | None:
        if not isinstance(ref, str):
            raise RetrievalRefused("a source is fetched by its ref")
        return self._sources.get(ref)

    # -- the lexical leg ---------------------------------------------------

    def _bm25(self, ref: str, query_tokens: Sequence[str]) -> float:
        counts = self._frequencies.get(ref, {})
        length = len(self._tokens.get(ref, ()))
        total = len(self._sources)
        if not total or not length:
            return 0.0
        score = 0.0
        for token in dict.fromkeys(query_tokens):
            frequency = counts.get(token, 0)
            if not frequency:
                continue
            appearances = self._document_frequency.get(token, 0)
            idf = math.log(
                1.0 + (total - appearances + 0.5) / (appearances + 0.5))
            denominator = frequency + BM25_K1 * (
                1.0 - BM25_B + BM25_B * length / (self._average_length or 1.0))
            score += idf * (frequency * (BM25_K1 + 1.0)) / denominator
        return score


def build_backend(
    declaration: RetrievalBackendDeclaration,
) -> RetrievalAssemblyPort:
    """The ONE place a retrieval backend is constructed, from the INSTALL-TIME
    declaration and from nothing else.

    Note the signature: it takes a declaration. It takes no turn, no prompt, no
    message, no scope, and no heuristic, so there is no runtime selection path
    to prove absent by inspection — the parameter that would carry one does not
    exist. A companion test asserts exactly that against this signature."""

    if not isinstance(declaration, RetrievalBackendDeclaration):
        raise BackendDeclarationRefused(
            "a backend is built from an install-time declaration")
    if declaration.profile_id == PROFILE_LOCAL_EMBEDDED:
        return LocalHybridBackend()
    raise BackendUnavailable(
        f"this install declares the {declaration.profile_id!r} retrieval "
        f"backend ({declaration.declared_by}), and this release ships only the "
        f"{PROFILE_LOCAL_EMBEDDED!r} profile — the declaration is the "
        "mechanism that names a hosted backend, and falling back to a local "
        "one nobody declared would hide which backend this install talks to")


# ---------------------------------------------------------------------------
# THE ONE TOOL BOUNDARY (task 10.2)
# ---------------------------------------------------------------------------

TOOL_SEARCH = "search"
TOOL_GET_SOURCE = "get_source"
TOOL_PROMOTE_FINDING = "promote_finding"
TOOL_REINDEX = "reindex"

IMPLEMENTED_TOOLS: tuple[str, ...] = (
    TOOL_SEARCH, TOOL_GET_SOURCE, TOOL_PROMOTE_FINDING, TOOL_REINDEX)

# RESERVED and unimplemented. Reserving a name is not building a feature: it
# means the boundary does not have to change on the day a graph provider is
# admitted, and it means a caller asking today gets a governance answer rather
# than a missing name.
RESERVED_TOOL_GRAPH_QUERY = "graph_query"
RESERVED_TOOLS: tuple[str, ...] = (RESERVED_TOOL_GRAPH_QUERY,)

DECLARED_TOOLS: tuple[str, ...] = IMPLEMENTED_TOOLS + RESERVED_TOOLS

RESERVED_REFUSAL = (
    "{tool} is RESERVED and unimplemented: v1 retrieval is graph-less, and a "
    "graph engine, store, or index is admitted only when a concrete "
    "GRADUATION TRIGGER is recorded — a recurring need for dependency "
    "traversal, contradiction detection, or change-impact analysis. The name "
    "is declared so its later arrival is not a boundary change"
)


@dataclasses.dataclass(frozen=True, slots=True)
class PromotionRequest:
    """What ``promote_finding`` returns: a REQUEST, never a record.

    It names the reviewed act that creates the target object and the provenance
    the created object must carry. Nothing is written, nothing is stored, and
    no durability follows from calling it — a human performs the act, and the
    review the act already rides is the promotion gate."""

    finding: str
    provenance: tuple[str, ...]
    act_verb: str
    act_review: str
    reason: str


class KnowledgeToolBoundary:
    """The caller-facing tool contract, in front of the assembly port.

    Dispatch goes through a FIXED table rather than ``getattr``, so a caller
    cannot reach a private helper by naming it, and the reserved name answers
    from the same table — which is what keeps the reservation visible at the
    boundary instead of being an absence."""

    def __init__(self, port: RetrievalAssemblyPort) -> None:
        for member in ASSEMBLY_PORT_MEMBERS:
            if not callable(getattr(port, member, None)):
                raise KnowledgeError(
                    f"the backend behind this boundary does not implement the "
                    f"assembly port member {member!r}")
        self._port = port

    # -- what the boundary declares ---------------------------------------

    @staticmethod
    def declared_tools() -> tuple[str, ...]:
        return DECLARED_TOOLS

    @staticmethod
    def implemented_tools() -> tuple[str, ...]:
        return IMPLEMENTED_TOOLS

    @staticmethod
    def reserved_tools() -> tuple[str, ...]:
        return RESERVED_TOOLS

    def profile(self) -> ProviderProfile:
        return self._port.profile()

    # -- the four tools ----------------------------------------------------

    def search(self, query: str, *, confined_to: frozenset[str],
               limit: int = MAX_RETRIEVAL_LIMIT,
               thread_signals: frozenset[str] = frozenset()
               ) -> tuple[RetrievalHit, ...]:
        return self._port.retrieve(query, confined_to=confined_to, limit=limit,
                                   thread_signals=thread_signals)

    def get_source(self, ref: str, *,
                   confined_to: frozenset[str]) -> IndexedSource | None:
        """The exact source for a ref — CONFINED, exactly as search is.

        A confinement that governed search but not fetch would be no
        confinement at all: a caller would simply search for something in the
        set and then fetch something outside it."""

        if not isinstance(confined_to, (set, frozenset)):
            raise RetrievalRefused(
                "a source fetch is confined to a declared ref set")
        if ref not in confined_to:
            raise RetrievalRefused(
                "the requested source is outside this tile's staged set and "
                "the promoted findings, so it is not this service's to hand "
                "over")
        return self._port.source(ref)

    def promote_finding(self, finding: str, *,
                        provenance: Sequence[str]) -> PromotionRequest:
        """Route a finding to the REVIEWED ACT that can make it durable.

        This writes nothing. The act, its review, and the reason are read from
        this surface's own ``memory-gateway`` declaration so there is exactly
        one spelling of "how a finding becomes durable here", and so a reader
        of the declaration and a caller of this tool cannot be told two
        different things."""

        if not isinstance(finding, str) or not finding.strip():
            raise KnowledgeError("a promotion request states its finding")
        refs = tuple(provenance)
        if not refs or any(not isinstance(ref, str) or not ref.strip()
                           for ref in refs):
            raise KnowledgeError(
                "a promotion request carries the provenance of what it "
                "promotes; an unattributed finding is exactly what the "
                "lifecycle verbs exist to keep out of the corpus")
        act = DECLARATION.promotion_act
        return PromotionRequest(finding=finding, provenance=refs,
                                act_verb=act.verb, act_review=act.review,
                                reason=act.reason)

    def reindex(self, sources: Sequence[IndexedSource]) -> IndexReport:
        return self._port.index(sources)

    # -- dispatch ----------------------------------------------------------

    def call(self, tool: str, /, **arguments: object) -> object:
        """Invoke a declared tool by name.

        A reserved name refuses with the fixed governance reason; an undeclared
        name refuses as unknown. The two are different verdicts and a caller
        must be able to tell them apart."""

        if tool in RESERVED_TOOLS:
            raise ReservedToolUnimplemented(RESERVED_REFUSAL.format(tool=tool))
        table: Mapping[str, Callable[..., object]] = {
            TOOL_SEARCH: self.search,
            TOOL_GET_SOURCE: self.get_source,
            TOOL_PROMOTE_FINDING: self.promote_finding,
            TOOL_REINDEX: self.reindex,
        }
        handler = table.get(tool)
        if handler is None:
            raise UnknownTool(
                f"{tool!r} is not a tool this boundary declares; the declared "
                f"names are {DECLARED_TOOLS}")
        return handler(**arguments)


# ---------------------------------------------------------------------------
# THE MODEL-DERIVED DISTILLED DOCUMENT ABSTRACT — a layer-2-class SIBLING
# (add-doxbench-distilled-abstract, ruling 4(a), design D3/D4, tasks §4)
# ---------------------------------------------------------------------------
#
# A SIBLING of layer two, and NOT layer two's owner. `CompressionLayer.owner`
# (`doxbench_packet.py:224`) is a ONE-owner field and `assert_fidelity` keys on
# the layer NUMBER, so `layer(2).owner` stays `doxbench_threads.compact_thread`
# and this type carries its own verifier instead of editing that field. What it
# shares with `compact_thread` is the DISCIPLINE: model output is passed IN,
# verified here, refused on failure, and non-authoritative and regenerable by
# CONSTRUCTION rather than by declaration.
#
# `DocumentThread` is deliberately not reused. It fixes `regenerable_from` to
# the transcript (`doxbench_threads.py:593`, refused at `:619`) and its own
# refusal rule keys on evidence refs and pending actions
# (`doxbench_threads.py:1071-1093`) that a document abstract has none of. The
# two constants below are spelled here rather than imported, so this module
# keeps its single dependency and a thread's rule can never quietly become an
# abstract's; `NON_AUTHORITATIVE` deliberately carries the SAME value, because
# one surface must not have two spellings of "not truth".

NON_AUTHORITATIVE = "non_authoritative"
REGENERABLE_FROM_DOCUMENT = "document"

# LAYER TWO'S FIDELITY WORD, which a layer-2-class sibling CARRIES (the ratified
# scenario "A sibling artifact is declared at a layer's fidelity class"). Spelled
# here rather than imported from `doxbench_packet.FIDELITY_LOSSY_BY_DESIGN` for
# the same reason the two constants above are spelled rather than imported from
# `doxbench_threads`: this module keeps its single dependency, and a layer's rule
# must not become the sibling's by an import moving underneath it. The cost of
# spelling is drift, so the equality with the layer table's own word is PINNED
# across the two modules, in `test_doxbench_document_abstract.py`'s
# `test_the_fidelity_word_is_the_SAME_word_the_layer_table_uses`.
#
# Carrying the WORD is not owning the LAYER: `CompressionLayer.owner` is a
# one-owner field and stays `doxbench_threads.compact_thread` (design D4).
FIDELITY_LOSSY_BY_DESIGN = "lossy-by-design"

# HUMAN REVIEW IS A STATED OPEN OBLIGATION, and this is where it is stated.
# Layer two is human-reviewable; the ratified scenario "Presentation is offered
# as human review" refuses the claim that a sibling inherits that adjective as
# DISCHARGED because it is rendered on a surface -- rendering an artifact in a
# pane is not a human reviewing it. So the artifact carries the obligation
# itself, as a field with exactly one legal value: every `DocumentAbstract` that
# can be constructed is UNREVIEWED, no code path can mint a reviewed one, and no
# ruled caption offers presentation as review.
REVIEW_UNREVIEWED = "unreviewed"

# The five ruled caption states (ruling 5). Exposed as an enum the route and the
# renderer share, because five string literals in three files are five strings
# that drift. Each caption states WHO derived it and WHAT it is not.
CAPTION_MODEL_DERIVED = "model-derived"
CAPTION_DETERMINISTIC = "deterministic"
CAPTION_STALE = "stale"
CAPTION_NOT_YET_GENERATED = "not-yet-generated"
CAPTION_HOSTED_PLANE = "hosted-plane"

CAPTION_STATES: tuple[str, ...] = (
    CAPTION_MODEL_DERIVED,
    CAPTION_DETERMINISTIC,
    CAPTION_STALE,
    CAPTION_NOT_YET_GENERATED,
    CAPTION_HOSTED_PLANE,
)

RULED_CAPTIONS: Mapping[str, str] = types.MappingProxyType({
    CAPTION_MODEL_DERIVED: ("Distilled by a model — not authoritative; "
                            "regenerable from the document."),
    CAPTION_DETERMINISTIC: "From the document's own headers",
    CAPTION_STALE: "Distilled from an earlier version of this document",
    CAPTION_NOT_YET_GENERATED: ("No distillation generated for this document "
                                "yet"),
    CAPTION_HOSTED_PLANE: "No distillation is available on this plane",
})

# The refusal classes. A refusal is STATED and renders nothing; there is no
# "unverified" class, because a class for unverified text is a route to
# rendering it.
ABSTRACT_REFUSED_EMPTY = "empty-abstract"
ABSTRACT_REFUSED_NO_DECLARED_BASE = "no-declared-base"
ABSTRACT_REFUSED_FOREIGN_PATH = "foreign-path"
ABSTRACT_REFUSED_SUBJECT_NOT_NAMED = "subject-not-named"
ABSTRACT_REFUSED_COVERAGE = "subject-mention-coverage"
ABSTRACT_REFUSED_PREVIOUS_COVERAGE = "previous-coverage-dropped"

ABSTRACT_REFUSAL_CODES: tuple[str, ...] = (
    ABSTRACT_REFUSED_EMPTY,
    ABSTRACT_REFUSED_NO_DECLARED_BASE,
    ABSTRACT_REFUSED_FOREIGN_PATH,
    ABSTRACT_REFUSED_SUBJECT_NOT_NAMED,
    ABSTRACT_REFUSED_COVERAGE,
    ABSTRACT_REFUSED_PREVIOUS_COVERAGE,
)

# A declared term shorter than this matches everything, so it is no evidence of
# coverage at all. A subject whose declared fields are ALL that short has no
# usable base and is refused as such rather than passed as covered.
MIN_MENTION_TERM_CHARACTERS = 3

_DIGEST_RULE = re.compile(r"[0-9a-f]{64}")

# A repository path as the RESPONSE BYTES can decide one: slash-joined segments
# that either name a file (a dotted extension on the last segment) or run at
# least two segments deep. `read/write` and `input/output` are prose, not paths,
# and a rule that refused them would be turned off by its first false refusal.
_PATH_CANDIDATE_RULE = re.compile(r"(?<![\w./-])(?:[\w.-]+/)+[\w.-]+(?![\w/])")
_NAMED_FILE_RULE = re.compile(r"[\w-]+\.[A-Za-z0-9]{1,6}")

_MENTION_NOISE = re.compile(r"[^0-9a-z]+")


class AbstractFormatRefused(KnowledgeError):
    """Raised when an abstract is CONSTRUCTED wrongly, or when a caller hands
    the verifier something it cannot verify.

    A model that answered badly is not a programming error and does not arrive
    by this route: it comes back as an ``AbstractRefused`` value."""


def document_content_digest(content: str) -> str:
    """The subject's content digest — sha256, hex, lowercase.

    One spelling, because the abstract cache keys on ``(subject path, content
    digest)`` and a second spelling would be a second key for one document."""

    if not isinstance(content, str):
        raise AbstractFormatRefused(
            "a content digest is taken over the document's SAVED text")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _validated_abstract_line(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise AbstractFormatRefused(f"{field} must be a string")
    text = value.strip()
    if not text or "\n" in text or "\r" in text:
        raise AbstractFormatRefused(f"{field} must be one non-empty line")
    return text


def _validated_subject_path(value: object, *, field: str = "subject_path") -> str:
    """One document-path rule, mirroring ``doxbench_threads``' own: a subject is
    repository-relative POSIX, so an absolute path names a tree this surface
    cannot place and a traversal segment names one it must not reach."""

    path = _validated_abstract_line(value, field=field)
    if "\\" in path or path.startswith("/"):
        raise AbstractFormatRefused(
            f"refusing {path!r} as a {field}: a subject path is "
            "repository-relative POSIX")
    if any(segment in ("", ".", "..") for segment in path.split("/")):
        raise AbstractFormatRefused(
            f"refusing {path!r} as a {field}: an empty or traversal segment "
            "names a document this surface cannot place")
    return path


def _validated_digest(value: object, *, field: str = "subject_digest") -> str:
    if not isinstance(value, str) or not _DIGEST_RULE.fullmatch(value):
        raise AbstractFormatRefused(
            f"{field} is a sha256 digest in LOWERCASE hex: a digest that "
            "differs only in case would be two cache keys for one document")
    return value


@dataclasses.dataclass(frozen=True, slots=True)
class DocumentAbstract:
    """One document's model-derived distilled abstract: the subject it
    describes, the SAVED bytes it describes them from, the model that produced
    it, and the prose itself.

    ``authority`` and ``regenerable_from`` are FIELDS with exactly one legal
    value each rather than constants a renderer adds, so the refusal lands where
    the claim is made — a caller that tries to construct an authoritative
    abstract fails at construction, which is the same guarantee
    ``DocumentThread`` gives and the reason a cache, a route or a renderer can
    hold one of these safely.

    ``fidelity`` and ``review`` are the same shape, and they carry the two
    ratified sentences about a LAYER-2-CLASS SIBLING: it declares layer two's
    fidelity word (lossy by design) and no other, and it inherits layer two's
    human-reviewable adjective as an OPEN OBLIGATION rather than as something a
    surface discharged by rendering it. What it does NOT declare is layer two's
    own job -- there is no field and no method here spelling commitments, their
    preservation, or the thread-state header, and a frozen slotted type cannot
    have one attached later.

    There is NO generated-at field. Generation order, where a caller needs it,
    is a monotonic ``generation`` sequence: a wall clock would put a moving
    value inside an artifact this surface expects to be reproducible from its
    inputs, and nothing here needs to know what time it is."""

    subject_path: str
    subject_digest: str
    model_id: str
    prose: str
    covered: tuple[str, ...] = ()
    generation: int = 0
    authority: str = NON_AUTHORITATIVE
    regenerable_from: str = REGENERABLE_FROM_DOCUMENT
    fidelity: str = FIDELITY_LOSSY_BY_DESIGN
    review: str = REVIEW_UNREVIEWED

    def __post_init__(self) -> None:
        _validated_subject_path(self.subject_path)
        _validated_digest(self.subject_digest)
        _validated_abstract_line(self.model_id, field="model_id")
        if not isinstance(self.prose, str) or not self.prose.strip():
            raise AbstractFormatRefused(
                "an abstract with no prose is an absence, and an absence is "
                "STATED by its caption rather than rendered as an empty one")
        if not isinstance(self.covered, tuple) or any(
                not isinstance(term, str) or not term.strip()
                for term in self.covered):
            raise AbstractFormatRefused(
                "covered names the declared subjects this abstract mentions")
        if isinstance(self.generation, bool) or not isinstance(
                self.generation, int) or self.generation < 0:
            raise AbstractFormatRefused(
                "generation is a monotonic, non-negative sequence number and "
                "never a clock reading")
        if self.authority != NON_AUTHORITATIVE:
            raise AbstractFormatRefused(
                f"an abstract's authority is {NON_AUTHORITATIVE!r} by "
                "construction: a distillation does not become truth by being "
                "cached, rendered, copied, or projected")
        if self.regenerable_from != REGENERABLE_FROM_DOCUMENT:
            raise AbstractFormatRefused(
                f"an abstract is regenerable from {REGENERABLE_FROM_DOCUMENT!r}"
                "; a thread's transcript is another type's origin and this one "
                "keeps none")
        if self.fidelity != FIDELITY_LOSSY_BY_DESIGN:
            raise AbstractFormatRefused(
                f"a layer-2-class sibling is declared at "
                f"{FIDELITY_LOSSY_BY_DESIGN!r} and at no other fidelity "
                "class: it borrows layer two's "
                "fidelity word, and a derived artifact that claimed selection's "
                "lossless-by-reference or offload's reversibility would be "
                "describing work nothing here does")
        if self.review != REVIEW_UNREVIEWED:
            raise AbstractFormatRefused(
                f"an abstract's review state is {REVIEW_UNREVIEWED!r} by "
                "construction: layer two's human-reviewable adjective is "
                "inherited as a STATED OPEN OBLIGATION, and rendering an "
                "artifact on a surface is not a human reviewing it")

    def caption_state_for(self, *, current_digest: str) -> str:
        """Which ruled caption this abstract shows against the subject's CURRENT
        content: an abstract whose subject has moved past its digest is SHOWN
        and LABELLED STALE, never silently discarded or presented as current."""

        digest = _validated_digest(current_digest, field="current_digest")
        return (CAPTION_MODEL_DERIVED if digest == self.subject_digest
                else CAPTION_STALE)


@dataclasses.dataclass(frozen=True, slots=True)
class AbstractRefused:
    """What verification returns when it fails: a STATED refusal that renders
    nothing.

    It deliberately carries no prose, no text and no abstract field. The refused
    bytes do not leave the verifier, so a downstream surface cannot silently
    downgrade a failure into rendering the unverified answer — the guarantee is
    structural rather than a rule someone must remember."""

    code: str
    reason: str
    subject_path: str
    caption_state: str = CAPTION_NOT_YET_GENERATED

    def __post_init__(self) -> None:
        if self.code not in ABSTRACT_REFUSAL_CODES:
            raise AbstractFormatRefused(
                f"{self.code!r} is not a declared abstract refusal class; the "
                f"declared classes are {ABSTRACT_REFUSAL_CODES}")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise AbstractFormatRefused("a refusal states its reason")
        _validated_subject_path(self.subject_path)
        if self.caption_state not in CAPTION_STATES:
            raise AbstractFormatRefused(
                f"{self.caption_state!r} is not one of the ruled caption "
                f"states {CAPTION_STATES}")


def _mention_text(value: str) -> str:
    return " " + _MENTION_NOISE.sub(" ", value.lower()).strip() + " "


def _destination_terms(destinations: object) -> tuple[str, ...]:
    """The declared destinations, as the names an abstract would MENTION.

    Both snapshot shapes are accepted: the raw ``destinations`` object of kind
    -> names, and the flattened ``kind: name`` lands the surface builds from it
    (`staging-workbench-model.js:1566-1571`), so a route is never forced to
    reshape a snapshot field in order to have it verified."""

    if isinstance(destinations, str):
        raise AbstractFormatRefused(
            "declared_destinations is the snapshot's destinations object or "
            "its flattened lands, never one string")
    terms: list[str] = []
    if isinstance(destinations, Mapping):
        for names in destinations.values():
            if isinstance(names, str):
                terms.append(names)
                continue
            terms.extend(str(name) for name in names)
        return tuple(terms)
    for entry in destinations:
        text = str(entry)
        _kind, separator, name = text.partition(":")
        terms.append(name.strip() if separator and name.strip() else text.strip())
    return tuple(terms)


def _declared_terms(topics: object, destinations: object) -> tuple[str, ...]:
    if isinstance(topics, str):
        raise AbstractFormatRefused(
            "declared_topics is the snapshot's topics array, never one string")
    terms = [str(topic) for topic in topics]
    terms.extend(_destination_terms(destinations))
    usable = [term for term in terms
              if len(_mention_text(term).strip()) >= MIN_MENTION_TERM_CHARACTERS]
    return tuple(dict.fromkeys(usable))


def _named_repository_paths(text: str) -> tuple[str, ...]:
    found: list[str] = []
    for match in _PATH_CANDIDATE_RULE.finditer(text):
        candidate = match.group(0).rstrip(".")
        if not candidate:
            continue
        if candidate.count("/") >= 2 or _NAMED_FILE_RULE.fullmatch(
                candidate.rsplit("/", 1)[-1]):
            found.append(candidate)
    return tuple(dict.fromkeys(found))


def named_repository_paths(text: str) -> tuple[str, ...]:
    """THE PATH RULE, as a public name — every repository path ``text`` names,
    in first-appearance order and without duplicates.

    ``verify_document_abstract`` refuses any path an abstract names that its
    request did not carry, so a route that puts a document's own content into
    a request has to derive the paths that content names with THE SAME rule the
    verifier applies. Deriving them with a second rule anywhere else is how the
    two drift and a faithful quotation of a document's own links becomes a
    refusal. This is that one rule, exported so a caller never has to reach for
    the private spelling.

    The result is candidates, not validated paths: a caller that feeds them
    back as ``request_paths`` still filters them to the shapes
    ``_validated_subject_path`` accepts."""

    return _named_repository_paths(text)


def _carried_by_the_request(candidate: str, carried: frozenset[str]) -> bool:
    # An ANCESTOR directory of a path the request carried names no document the
    # request did not carry, so it is not a leak; a sibling file is.
    return candidate in carried or any(
        path.startswith(candidate + "/") for path in carried)


def verify_document_abstract(
    dispatch_result: str,
    *,
    subject_path: str,
    subject_digest: str,
    model_id: str,
    declared_topics: Sequence[str] = (),
    declared_destinations: object = (),
    request_paths: Iterable[str] = (),
    subject_title: str | None = None,
    previous: DocumentAbstract | None = None,
    generation: int = 0,
) -> DocumentAbstract | AbstractRefused:
    """Verify a returned abstract BEFORE anything renders it, and return either
    a ``DocumentAbstract`` or a stated ``AbstractRefused``.

    ``dispatch_result`` is the assistant PROSE a dispatch returned — a string.
    No turn, message, prompt or envelope crosses this seam, which is this
    module's standing rule and is asserted against the signature.

    Two rules, and the honesty of their names is load-bearing:

      1. **SUBJECT-MENTION COVERAGE** over the SNAPSHOT'S OWN declared fields —
         its ``topics`` and its ``destinations``, the same fields the surface
         reads (`staging-workbench-model.js:1566-1573`). The base is the
         snapshot's, so the rule fires on generation #1 rather than only on a
         regeneration; a previously generated abstract is an ADDITIONAL base
         when one exists and never the only one, and it can only TIGHTEN — a
         regeneration that drops every declared subject its predecessor covered
         is refused.

         ``previous`` IS A PREDECESSOR OF THE SAME QUESTION, and SELECTING one
         is the caller's job exactly as deriving ``request_paths`` is. The
         question is `(scope, subject path, model)` — ruled 2026-08-26,
         SHOULD-FIX 6 — so a caller offers only an abstract of THIS document
         produced by the SAME resolved model. Another model's answer is not
         this generation's base: the clause can only tighten, so offering one
         would make a FIRST generation under a newly selected model defend
         coverage it never claimed, and two models may distil one document
         differently without either being wrong.

         **It is NOT a fidelity check, and it must never be described as one.**
         A dispatch returns assistant prose as ONE OPAQUE STRING
         (`doxbench_model.py:985`), so nothing downstream can establish that a
         mentioned subject was treated faithfully. What is decidable is whether
         the answer mentions any declared subject of the document it claims to
         describe. Calling that faithfulness would be this surface committing
         the exact error the check exists to catch.

      2. **THE PATH RULE** — name the subject's path or title, and name NO
         repository path the request did not carry. This is the one clause the
         RESPONSE BYTES can decide, and it refuses the wrong-document answer and
         the leaked-neighbour answer with the same test.

    ``request_paths`` is every repository path the request actually carried; the
    subject's own path is always one of them, so a caller may leave it empty.
    Where a route puts a document's own content into the request, the paths that
    content names are carried too and belong in this set.

    A verification failure renders NOTHING: the refusal carries a code and a
    reason and does not carry the refused text, so there is no downgrade path to
    rendering it unverified."""

    if not isinstance(dispatch_result, str):
        raise AbstractFormatRefused(
            "verify_document_abstract verifies the assistant PROSE a dispatch "
            "returned, which is one string")
    subject = _validated_subject_path(subject_path)
    digest = _validated_digest(subject_digest)
    model = _validated_abstract_line(model_id, field="model_id")
    if previous is not None:
        if not isinstance(previous, DocumentAbstract):
            raise AbstractFormatRefused(
                "previous is the abstract this subject already has, if any")
        if previous.subject_path != subject:
            raise AbstractFormatRefused(
                "previous belongs to another subject; an abstract is verified "
                "against ITS OWN document's fields")
    if subject_title is not None:
        subject_title = _validated_abstract_line(
            subject_title, field="subject_title")

    prose = dispatch_result.strip()
    if not prose:
        return AbstractRefused(
            code=ABSTRACT_REFUSED_EMPTY, subject_path=subject,
            reason=("the provider returned no prose; an absence is stated by "
                    "the not-yet-generated caption, never rendered as an empty "
                    "abstract"))

    declared = _declared_terms(declared_topics, declared_destinations)
    if not declared:
        return AbstractRefused(
            code=ABSTRACT_REFUSED_NO_DECLARED_BASE, subject_path=subject,
            reason=(f"the snapshot declares no topics and no destinations for "
                    f"{subject}, so subject-mention coverage has no base and "
                    "this abstract cannot be verified against anything the "
                    "document itself declares"))

    carried = frozenset(_validated_subject_path(path, field="request_paths")
                        for path in request_paths) | {subject}
    named_paths = _named_repository_paths(prose)
    foreign = tuple(path for path in named_paths
                    if not _carried_by_the_request(path, carried))
    if foreign:
        return AbstractRefused(
            code=ABSTRACT_REFUSED_FOREIGN_PATH, subject_path=subject,
            reason=(f"the abstract names {foreign[0]}, a repository path its "
                    f"request did not carry: the request carried exactly one "
                    f"document ({subject}), so this is a wrong-document answer "
                    "or a leaked neighbour and is refused either way"))

    haystack = _mention_text(prose)
    names_subject = subject in named_paths or (
        subject_title is not None
        and _mention_text(subject_title) in haystack)
    if not names_subject:
        return AbstractRefused(
            code=ABSTRACT_REFUSED_SUBJECT_NOT_NAMED, subject_path=subject,
            reason=(f"the abstract names neither the path nor the title of "
                    f"{subject}, so nothing in the returned bytes says it "
                    "describes this document"))

    covered = tuple(term for term in declared
                    if _mention_text(term) in haystack)
    if not covered:
        return AbstractRefused(
            code=ABSTRACT_REFUSED_COVERAGE, subject_path=subject,
            reason=("subject-mention coverage failed: the abstract mentions no "
                    f"declared topic and no declared destination of {subject}, "
                    f"whose declared subjects are {list(declared)}"))

    if previous is not None and previous.covered:
        held = tuple(term for term in previous.covered if term in declared)
        if held and not set(held) & set(covered):
            return AbstractRefused(
                code=ABSTRACT_REFUSED_PREVIOUS_COVERAGE, subject_path=subject,
                reason=("this regeneration mentions none of the declared "
                        f"subjects its predecessor covered ({list(held)}); a "
                        "previous abstract is an additional base and can only "
                        "tighten the coverage the declared fields already "
                        "require"))

    return DocumentAbstract(
        subject_path=subject, subject_digest=digest, model_id=model,
        prose=prose, covered=covered, generation=generation)
