"""The distilled abstract's own bounded cache — SEPARATE from the chat surface's
turn-idempotency ledger, and separately bounded (add-doxbench-distilled-abstract
§5.3, design D5, clarification N1).

WHY A SECOND STORE AND NOT THE CHAT ONE. The shape below is deliberately
`doxbench_turns.TurnStore`'s: one in-flight entry per key with attach-and-wait,
identical-key replay with no second dispatch, deterministic non-clock eviction,
ingress/egress isolation. The INSTANCE cannot be shared, and neither can the
bounds. There is exactly one `TurnStore` per served process
(`serve.py`'s "ONE fresh turn-idempotency ledger per served process"), bounded at
`MAX_IDEMPOTENCY_ENTRIES = 64` entries and `MAX_IDEMPOTENCY_BYTES = 16 MiB`. A
scope holding more documents than that bound is the ORDINARY case for abstracts,
not an edge case — a 200-document scope exceeds 64 threefold — so abstract churn
through a shared ledger would evict the chat turns' idempotency records and a
chat retry that should replay would re-dispatch (N1). That is the failure this
module exists to make impossible: two stores, two bounds, and no line of code
here that can reach the chat ledger.

THE KEY IS `(scope, subject path, content digest, resolved model id)`, and both
the digest and the model are IN it rather than compared against it. `TurnStore`
refuses a differing digest under one key as a CONFLICT; an abstract cache keyed
on path alone would therefore hard-refuse every regeneration after every
document edit. Here a changed digest is simply a NEW KEY, which is what makes
"regenerate after an edit" ordinary rather than an error, and re-dispatch after
eviction is stated expected behaviour for the same reason. The RESOLVED MODEL ID
is in it for the mirror-image reason: a human can change the selected model
while the document stands still, so without it that second request is IDENTICAL
and the first model's prose would replay while the artifact records the model
the reader just picked.

AND A THIRD REQUEST MODE: AN EXPLICIT REFRESH. Replay on an identical key and a
working RE-GENERATE control are in direct conflict — a regeneration against
unchanged content and an unchanged model has an identical key by construction,
so plain replay made that control inert except by the accident of eviction. A
reservation carrying `refresh=True` INVALIDATES the completed entry for its key,
takes the in-flight slot and dispatches; its answer replaces the entry. The
one-in-flight arm stays UNCONDITIONAL in both modes: a refresh arriving while a
generation is already in flight for the same key ATTACHES to it, so an impatient
double-click spends one model call and not two. The invalidated entry's verified
abstract rides back on the lease, because invalidating an answer out of the
replay index must not also invalidate it out of the verifier's reach.

WHAT IS CACHED, AND WHAT IS NOT. Only an ANSWER is completed into this store — a
verified abstract the route is about to send. A refusal is RELEASED instead: the
key goes back to being unknown, so the re-generate control can try again against
unchanged content. Caching refusals would make one bad answer permanent for that
digest, which is the opposite of what a regenerate control is for.

NOTHING HERE IS AUTHORITATIVE. The contents are session-local, live only in this
process's memory, and are never written to a corpus, snapshot, register or gate
artifact. The store holds a bounded, already-validated result object and the key
it was produced for; it holds no document content of its own, no credential and
no provider material.

NO CLOCK. Recency is an increasing integer counter guarded by the same lock, so
eviction order is reproducible for a given sequence of operations. A wall-clock
ordering would make the same operations evict different entries on a different
machine, and this module imports nothing that could tell it the time.
"""

from __future__ import annotations

import copy
import dataclasses
import itertools
import threading

# ---------------------------------------------------------------------------
# the bounds — this store's OWN, never the chat ledger's
# ---------------------------------------------------------------------------

# How many ANSWERED abstracts one served process keeps. Sized for a reader
# moving through a scope's documents rather than for a whole corpus: past this,
# the least recently used answer is dropped and asking for it again re-dispatches
# (stated expected behaviour, not an error).
MAX_ABSTRACT_ENTRIES = 64

# The total bytes those answers may hold. Three orders of magnitude below the
# chat ledger's 16 MiB, and deliberately so: an abstract is bounded at
# `doxbench_turns.MAX_ABSTRACT_PROSE_BYTES` (1_500 bytes) plus its small
# response envelope, so 1 MiB is generous headroom for a full 64 entries — while
# borrowing the chat number would have declared room for material this store can
# never hold.
MAX_ABSTRACT_BYTES = 1_048_576

ABSTRACT_STATE_IN_FLIGHT = "in_flight"
ABSTRACT_STATE_COMPLETED = "completed"


class AbstractStoreError(ValueError):
    """Base class for this store's refusals. A ``ValueError``, like every other
    refusal on this surface, and none of them echoes an abstract's text."""


class AbstractStoreConflictError(AbstractStoreError):
    """Raised when a caller tries to resolve an entry that is not in flight —
    it was never reserved, or somebody else already resolved it. Never raised
    for a key that simply differs: a different key is a different question."""


@dataclasses.dataclass(frozen=True, slots=True)
class AbstractKey:
    """The ruled cache key: the SCOPE, the subject's repository-relative path,
    the content digest of the SAVED bytes the abstract was generated from, AND
    the RESOLVED id of the model that answered it.

    THE SCOPE IS IN IT — added 2026-08-25 after the adversarial review's S3, and
    for the same reason `OmpHarnessBridge.conversation_key` carries it. The key
    used to be `(subject_path, content_digest)` alone, while the store is a
    single per-served-process dict and one process resolves EVERY repository its
    registry knows and every ref of each. `ideation/staging/<topic>/README.md`
    exists in most repositories on this surface, so two scopes holding identical
    bytes at one path shared a cache entry — and `latest_for_path` then handed
    repository A's abstract to repository B as its PREVIOUS VERIFICATION BASE,
    which is a cross-repository leak arriving through the key rather than
    through a route.

    THE RESOLVED MODEL ID IS IN IT — added 2026-08-25 after the packet review
    (Codex on PR #352), and for the mirror image of the digest's reason. This
    surface lets a human change the selected model while the document stands
    still: on a key without the model that second request is IDENTICAL, so the
    first model's prose replayed while `DocumentAbstract.model_id` recorded the
    model the reader had just picked — an artifact lying about its own
    provenance, and a violation of the provider boundary's rule that every
    consumer resolves a catalog model id. It is the RESOLVED id and never the
    requested one: an `auto` routing entry keys on the model that ACTUALLY
    ANSWERED, for the same reason a turn records that model, and keying on the
    rule's own id would collide every routed abstract into one bucket while
    sharing none of them with the plain model's.

    The components are FIELDS rather than a composed string, so the injectivity
    the bridge's JSON composition buys is here by construction: a frozen
    dataclass hashes and compares as the tuple of its fields, and there is no
    separator for a repository name, a ref, a document path or a model id to
    contain."""

    repository: str
    ref: str
    subject_path: str
    content_digest: str
    resolved_model_id: str


@dataclasses.dataclass(frozen=True, slots=True)
class AbstractRecord:
    """One reserved-or-answered entry. Holds the key, a state, the bounded
    already-validated result, and its place in the recency order — no document
    content, no prompt, no provider material."""

    key: AbstractKey
    state: str
    result: object | None
    size_bytes: int
    last_access_order: int
    # The VERIFIED artifact this answer carried, kept beside the wire result so
    # a later generation of the SAME DOCUMENT under a different digest can be
    # verified against it as an additional base. Never a second copy of the
    # answer: the route stores the frozen `DocumentAbstract` the verifier
    # returned, and the wire body stays the only thing that is ever sent.
    abstract: object | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class AbstractLease:
    """The outcome of a ``reserve``: whether this caller must dispatch, the
    entry's state, and — for a replay — the answer to hand back unchanged with
    no second dispatch.

    ``invalidated_abstract`` is the verified artifact an EXPLICIT REFRESH just
    invalidated, handed back so the route can offer it to the verifier as that
    generation's PREVIOUS base. The verification rule makes a previously
    generated abstract an ADDITIONAL base "where one exists", and RE-GENERATE is
    the one path where one always exists: dropping it at the moment of
    invalidation would make the refresh path verify against a strictly weaker
    base than every other path. ``None`` on every reservation that invalidated
    nothing."""

    should_dispatch: bool
    state: str
    result: object | None
    invalidated_abstract: object | None = None


class AbstractStore:
    """A bounded, thread-safe, per-instance abstract cache.

    ``reserve`` on an unknown key creates the in-flight entry and tells the
    caller to dispatch. ``reserve`` on an in-flight key ATTACHES: it waits until
    the holder resolves, then replays the holder's answer — or, if the holder
    RELEASED the key (a refusal, which is not an answer), takes the in-flight
    slot itself and dispatches. ``reserve`` on an answered key replays it and
    touches its recency — unless it carries the EXPLICIT REFRESH INTENT, which
    invalidates that answer and dispatches instead.

    The lock is held only for the brief in-memory bookkeeping each method does,
    never across a caller's or a provider's work. Deep copies run OUTSIDE it on
    both sides — ingress copies before acquiring, egress captures a reference
    under the lock and copies after releasing — so an arbitrarily slow
    ``__deepcopy__`` can never stall an unrelated key. This is
    ``doxbench_turns.TurnStore``'s own discipline, followed deliberately: the
    shape is shared even though the instance and the bounds are not.

    Two instances share no state: every field below is set on ``self``.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._records: dict[AbstractKey, AbstractRecord] = {}
        self._resolved_bytes_total = 0
        self._order_counter = itertools.count(1)
        self._generation_counter = itertools.count(1)

    # -- the recency counter, and the generation sequence beside it ---------

    def _next_order_locked(self) -> int:
        return next(self._order_counter)

    def next_generation(self) -> int:
        """The next generation number, for stamping a new abstract.

        An increasing integer sequence and never a clock reading — the same rule
        ``doxbench_knowledge.DocumentAbstract`` states for its own ``generation``
        field, which exists so a caller can order two answers without putting a
        moving wall-clock value inside an artifact this surface expects to be
        reproducible from its inputs."""
        with self._lock:
            return next(self._generation_counter)

    # -- reserve / attach / replay ------------------------------------------

    def reserve(self, key: AbstractKey, *,
                refresh: bool = False) -> AbstractLease:
        """Reserve, attach to, or replay the entry for ``key``.

        ``refresh`` is the EXPLICIT REFRESH INTENT the RE-GENERATE control
        issues, and nothing else does: it MUST NOT be inferred from a selection
        change, a mount, a tile re-entry, or any other event that is not the
        human control being invoked. Set, and only where this caller finds a
        COMPLETED entry without having waited for one, it invalidates that entry
        and takes the in-flight slot. Unset, the method behaves exactly as it
        always did.

        THE ATTACH PATH IS NOT A REFRESH PATH, deliberately. A caller that
        WAITED on an in-flight generation replays the holder's answer even when
        it asked for a refresh: turning round and invalidating the answer it
        just waited for would make two clicks cost two model calls, which is the
        precise defect the one-in-flight arm exists to prevent."""
        replayed: AbstractRecord | None = None
        invalidated: object | None = None
        with self._condition:
            attached = False
            while True:
                record = self._records.get(key)
                if record is None:
                    self._records[key] = AbstractRecord(
                        key=key,
                        state=ABSTRACT_STATE_IN_FLIGHT,
                        result=None,
                        size_bytes=0,
                        last_access_order=self._next_order_locked(),
                        abstract=None,
                    )
                    return AbstractLease(should_dispatch=True,
                                         state=ABSTRACT_STATE_IN_FLIGHT,
                                         result=None)
                if record.state == ABSTRACT_STATE_IN_FLIGHT:
                    # ONE in-flight generation per key: wait for the holder
                    # rather than spending a second provider call on a question
                    # already being asked. `wait()` releases the lock, so
                    # unrelated keys are never serialized behind this. This arm
                    # is UNCONDITIONAL — a refresh gets no exemption from it.
                    attached = True
                    self._condition.wait()
                    continue
                if refresh and not attached:
                    # THE BYPASS. The completed entry is invalidated — removed
                    # from the replay index and from the byte total it was
                    # charged against — and this caller takes the in-flight slot
                    # and dispatches. Its answer replaces the entry.
                    del self._records[key]
                    self._resolved_bytes_total -= record.size_bytes
                    self._records[key] = AbstractRecord(
                        key=key,
                        state=ABSTRACT_STATE_IN_FLIGHT,
                        result=None,
                        size_bytes=0,
                        last_access_order=self._next_order_locked(),
                        abstract=None,
                    )
                    invalidated = record.abstract
                    break
                replayed = self._touch_locked(key, record)
                break
        if replayed is None:
            return AbstractLease(should_dispatch=True,
                                 state=ABSTRACT_STATE_IN_FLIGHT, result=None,
                                 invalidated_abstract=copy.deepcopy(invalidated))
        return AbstractLease(should_dispatch=False, state=replayed.state,
                             result=copy.deepcopy(replayed.result))

    def _touch_locked(self, key: AbstractKey,
                      record: AbstractRecord) -> AbstractRecord:
        touched = dataclasses.replace(
            record, last_access_order=self._next_order_locked())
        self._records[key] = touched
        return touched

    # -- resolve: an answer is completed, a refusal is released -------------

    def complete(self, key: AbstractKey, result: object, *,
                 size_bytes: int, abstract: object | None = None) -> None:
        """Resolve the in-flight entry for ``key`` with a bounded, already
        validated ``result``, waking every attached waiter.

        ``abstract`` is the VERIFIED artifact that answer carried, kept so a
        later generation of the same document — necessarily under a different
        key, because the digest is IN the key — can be verified against it as an
        additional base. It is optional: a caller with nothing to remember
        passes nothing, and the snapshot's own declared fields remain the base
        that always exists.

        Both stored values are deep copies of the caller's objects (ingress
        isolation), made BEFORE the lock is acquired. A refused resolution
        mutates nothing."""
        if size_bytes < 0 or size_bytes > MAX_ABSTRACT_BYTES:
            raise AbstractStoreError(
                "an abstract result's declared size is within this store's own "
                "byte bound")
        copied = copy.deepcopy(result)
        copied_abstract = copy.deepcopy(abstract)
        with self._condition:
            previous = self._records.get(key)
            if previous is None or previous.state != ABSTRACT_STATE_IN_FLIGHT:
                raise AbstractStoreConflictError(
                    "no in-flight generation exists to resolve for this subject, "
                    "content digest and model")
            self._records[key] = dataclasses.replace(
                previous,
                state=ABSTRACT_STATE_COMPLETED,
                result=copied,
                size_bytes=size_bytes,
                last_access_order=self._next_order_locked(),
                abstract=copied_abstract,
            )
            self._resolved_bytes_total += size_bytes
            self._enforce_bounds_locked()
            self._condition.notify_all()

    def release(self, key: AbstractKey) -> None:
        """Give up the in-flight entry for ``key`` WITHOUT caching anything, and
        wake every attached waiter so one of them can dispatch.

        This is what a REFUSAL does. A refusal is not an answer, so it must not
        occupy the key: the re-generate control has to be able to try again
        against unchanged content, and a cached refusal would make one bad
        answer permanent for that digest. Idempotent — releasing a key that is
        not in flight leaves an answered entry exactly as it is."""
        with self._condition:
            record = self._records.get(key)
            if record is not None and record.state == ABSTRACT_STATE_IN_FLIGHT:
                del self._records[key]
            self._condition.notify_all()

    # -- bounds --------------------------------------------------------------

    def _enforce_bounds_locked(self) -> None:
        """Evict ANSWERED entries, least recently used first, until both bounds
        hold. In-flight entries are never evicted — a generation somebody is
        waiting on is not spare capacity."""
        answered = [key for key, record in self._records.items()
                    if record.state != ABSTRACT_STATE_IN_FLIGHT]
        while answered and (len(answered) > MAX_ABSTRACT_ENTRIES
                            or self._resolved_bytes_total > MAX_ABSTRACT_BYTES):
            oldest = min(answered,
                         key=lambda entry: self._records[entry].last_access_order)
            record = self._records.pop(oldest)
            self._resolved_bytes_total -= record.size_bytes
            answered.remove(oldest)

    # -- read-only peek ------------------------------------------------------

    def latest_for_path(self, *, repository: str, ref: str,
                        subject_path: str) -> object | None:
        """The most recently used ANSWERED abstract for ``subject_path`` IN ONE
        SCOPE, under any digest AND UNDER ANY MODEL, or ``None``.

        MODEL-AGNOSTIC, deliberately, even though the model is in the key. This
        answers "what abstract does this document already have", which the
        ratified verification rule takes as an ADDITIONAL base: an answer from
        another model is still a previous answer about THIS document, and the
        rule says nothing that would narrow it to one model. The SCOPE is a
        different matter — see below — because another repository's answer for
        an identically-named document is a different document's abstract.

        SCOPE-QUALIFIED, and keyword-only so the three components cannot be
        transposed at a call site (S3). "The abstract this document already has"
        is a question about one repository at one ref: another repository's
        answer for an identically-named document is a different document's
        abstract, and handing it to the verifier as a base would refuse a
        perfectly good answer for dropping coverage of a document this scope
        never held.

        This is the "previously generated abstract" the verification rule takes
        as an ADDITIONAL base. It is a CACHE and never a record: an evicted entry
        takes its abstract with it, and the next generation is then verified
        against the snapshot's own declared fields alone — which is the base the
        rule requires to exist on generation #1 in any case.

        Bounded by construction: the scan is over at most
        ``MAX_ABSTRACT_ENTRIES`` answered entries."""
        with self._lock:
            candidates = [record for record in self._records.values()
                          if record.state == ABSTRACT_STATE_COMPLETED
                          and record.abstract is not None
                          and record.key.subject_path == subject_path
                          and record.key.repository == repository
                          and record.key.ref == ref]
            newest = max(candidates, key=lambda record: record.last_access_order,
                         default=None)
        if newest is None:
            return None
        return copy.deepcopy(newest.abstract)

    def snapshot(self, key: AbstractKey) -> AbstractRecord | None:
        """The current record for ``key``, or ``None``. A read-only peek that
        never mutates recency order; the returned ``result`` is a fresh deep copy
        (egress isolation), taken after the lock is released."""
        with self._lock:
            record = self._records.get(key)
        if record is None:
            return None
        return dataclasses.replace(record, result=copy.deepcopy(record.result))
