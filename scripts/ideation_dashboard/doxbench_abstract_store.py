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

THE KEY IS `(subject path, content digest)`, and the digest is IN it rather than
compared against it. `TurnStore` refuses a differing digest under one key as a
CONFLICT; an abstract cache keyed on path alone would therefore hard-refuse every
regeneration after every document edit. Here a changed digest is simply a NEW
KEY, which is what makes "regenerate after an edit" ordinary rather than an
error, and re-dispatch after eviction is stated expected behaviour for the same
reason.

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
    """The ruled cache key: the subject's repository-relative path AND the
    content digest of the SAVED bytes the abstract was generated from."""

    subject_path: str
    content_digest: str


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
    no second dispatch."""

    should_dispatch: bool
    state: str
    result: object | None


class AbstractStore:
    """A bounded, thread-safe, per-instance abstract cache.

    ``reserve`` on an unknown key creates the in-flight entry and tells the
    caller to dispatch. ``reserve`` on an in-flight key ATTACHES: it waits until
    the holder resolves, then replays the holder's answer — or, if the holder
    RELEASED the key (a refusal, which is not an answer), takes the in-flight
    slot itself and dispatches. ``reserve`` on an answered key replays it and
    touches its recency.

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

    def reserve(self, key: AbstractKey) -> AbstractLease:
        """Reserve, attach to, or replay the entry for ``key``."""
        replayed: AbstractRecord | None = None
        with self._condition:
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
                    # unrelated keys are never serialized behind this.
                    self._condition.wait()
                    continue
                replayed = self._touch_locked(key, record)
                break
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
                    "no in-flight generation exists to resolve for this subject "
                    "and content digest")
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

    def latest_for_path(self, subject_path: str) -> object | None:
        """The most recently used ANSWERED abstract for ``subject_path``, under
        any digest, or ``None``.

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
                          and record.key.subject_path == subject_path]
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
