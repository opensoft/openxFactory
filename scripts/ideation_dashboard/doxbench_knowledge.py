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
        if len(token) > CHARACTER_NGRAM:
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
