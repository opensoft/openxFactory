"""add-doxbench-distilled-abstract §5.3/§5.4: the abstract cache is a SEPARATE
bounded store, and abstract churn never touches the chat surface's ledger.

RED FIRST. `ideation_dashboard.doxbench_abstract_store` does not exist in this
checkout, so this module fails at import (a collection error) until it does —
which is the fail-closed direction: a store test that skipped when its store was
missing would report green for an absent store.

WHAT IS PINNED HERE, and each clause is a ratified sentence rather than an
implementation preference (`specs/ideation-dashboard/spec.md`, "The abstract
cache is a separate bounded store keyed by content digest"; clarification N1):

  * the store is SEPARATE and SEPARATELY BOUNDED — its own entry and byte
    constants, never the chat store's, because a scope larger than the bound is
    the ORDINARY case here and shared bounds would evict chat idempotency
    records under abstract churn (N1, task 5.4);
  * the key is `(subject path, content digest)`, so a regeneration after an edit
    is a NEW KEY and never a same-key conflict — the failure mode N1 names, in
    which a path-only key hard-refuses every regeneration after every edit;
  * at most ONE in-flight generation per key, a concurrent request for the same
    key ATTACHING to it rather than dispatching a second time;
  * an identical key REPLAYS a completed result with no second dispatch;
  * eviction is DETERMINISTIC and NOT clock-ordered, and a re-dispatch after
    eviction is stated expected behaviour rather than an error.

WHAT IS DELIBERATELY NOT PINNED HERE: anything about HTTP. The store is a pure
in-memory collaborator, so it is exercised with no server, no route and no
provider — the route's own consumption of it is
`test_doxbench_abstract_route.py`'s subject.
"""

from __future__ import annotations

import copy
import threading

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_abstract_store as store_mod
from ideation_dashboard import doxbench_scope
from ideation_dashboard import doxbench_turns

MODULE_PATH = (REPO_ROOT / "scripts" / "ideation_dashboard"
               / "doxbench_abstract_store.py")

DIGEST_A = "a" * 64
DIGEST_B = "b" * 64
SUBJECT = "ideation/staging/ideation-governance/README.md"
OTHER_SUBJECT = "ideation/staging/other-topic/README.md"

# The SCOPE the key is qualified by (adversarial review 2026-08-25, S3). One
# served process can hold several repositories and several refs of one
# repository, and `(path, digest)` alone made two of them one question.
REPOSITORY = "fixture-repo"
REF = "main"


def _key(path=SUBJECT, digest=DIGEST_A, *, repository=REPOSITORY, ref=REF):
    return store_mod.AbstractKey(repository=repository, ref=ref,
                                 subject_path=path, content_digest=digest)


def _result(text="an abstract"):
    return {"status": 200, "body": {"ok": True, "prose": text}}


def _fill(store, count, *, prefix="ideation/staging/topic-"):
    """`count` completed entries, in order, each under its own key."""
    keys = []
    for index in range(count):
        key = _key(path=f"{prefix}{index:04d}/README.md")
        assert store.reserve(key).should_dispatch is True
        store.complete(key, _result(f"abstract {index}"), size_bytes=64)
        keys.append(key)
    return keys


# ---------------------------------------------------------------------------
# separateness: its own bounds, its own instance, no shared state
# ---------------------------------------------------------------------------

def test_the_store_declares_its_own_bounds_and_never_the_chat_stores():
    """N1's first clause. The chat ledger is bounded for 16 MiB of chat turns;
    this one holds answers whose own bound is 1_500 bytes, so it declares its
    own numbers — and the byte bound in particular must not be the chat one,
    which is what a copy-paste of `TurnStore` would leave behind."""
    assert isinstance(store_mod.MAX_ABSTRACT_ENTRIES, int)
    assert isinstance(store_mod.MAX_ABSTRACT_BYTES, int)
    assert store_mod.MAX_ABSTRACT_ENTRIES > 0
    assert store_mod.MAX_ABSTRACT_BYTES > 0
    assert store_mod.MAX_ABSTRACT_BYTES != doxbench_turns.MAX_IDEMPOTENCY_BYTES


def test_two_stores_share_no_state():
    first, second = store_mod.AbstractStore(), store_mod.AbstractStore()
    key = _key()
    assert first.reserve(key).should_dispatch is True
    first.complete(key, _result(), size_bytes=32)
    assert second.snapshot(key) is None
    assert second.reserve(key).should_dispatch is True


def test_the_store_reads_no_clock():
    """Eviction is deterministic and MUST NOT be ordered by wall-clock time. The
    behavioural pin is below; this is the house's purity/import guard, which is
    the one place a source-text assertion is legitimate — a store that imported
    a clock could order by one tomorrow without failing a behavioural test that
    only ever runs fast."""
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "import time" not in source
    assert "datetime" not in source
    assert "time.monotonic" not in source
    assert "time.time" not in source


# ---------------------------------------------------------------------------
# the key: path AND digest
# ---------------------------------------------------------------------------

def test_a_changed_digest_is_a_new_key_and_never_a_conflict():
    """N1's second clause, and the reason the digest is IN the key: the chat
    store refuses a differing digest under one key as a conflict, so a path-only
    abstract key would hard-refuse every regeneration after every edit."""
    store = store_mod.AbstractStore()
    first = _key(digest=DIGEST_A)
    store.reserve(first)
    store.complete(first, _result("from the old bytes"), size_bytes=32)

    second = _key(digest=DIGEST_B)
    lease = store.reserve(second)  # must NOT raise a conflict
    assert lease.should_dispatch is True
    store.complete(second, _result("from the new bytes"), size_bytes=32)

    assert store.snapshot(first).result == _result("from the old bytes")
    assert store.snapshot(second).result == _result("from the new bytes")


def test_the_same_digest_under_a_different_path_is_a_different_key():
    store = store_mod.AbstractStore()
    mine = _key(path=SUBJECT, digest=DIGEST_A)
    theirs = _key(path=OTHER_SUBJECT, digest=DIGEST_A)
    store.reserve(mine)
    store.complete(mine, _result("mine"), size_bytes=32)
    assert store.reserve(theirs).should_dispatch is True


# ---------------------------------------------------------------------------
# one in-flight per key, attach-and-wait, replay without a second dispatch
# ---------------------------------------------------------------------------

def test_an_identical_key_replays_with_no_second_dispatch():
    store = store_mod.AbstractStore()
    key = _key()
    assert store.reserve(key).should_dispatch is True
    store.complete(key, _result("answered once"), size_bytes=32)

    lease = store.reserve(key)
    assert lease.should_dispatch is False
    assert lease.result == _result("answered once")
    assert lease.state == store_mod.ABSTRACT_STATE_COMPLETED


def test_a_concurrent_request_for_one_key_attaches_and_waits():
    """One in-flight per key. The second caller must not dispatch: it waits for
    the holder and is handed the holder's own answer."""
    store = store_mod.AbstractStore()
    key = _key()
    assert store.reserve(key).should_dispatch is True

    attached = {}
    started = threading.Event()

    def _attach():
        started.set()
        attached["lease"] = store.reserve(key)

    waiter = threading.Thread(target=_attach, daemon=True)
    waiter.start()
    started.wait(timeout=2)
    # The waiter is parked inside `reserve`; it cannot have decided anything.
    waiter.join(timeout=0.2)
    assert waiter.is_alive() is True
    assert "lease" not in attached

    store.complete(key, _result("the holder's answer"), size_bytes=32)
    waiter.join(timeout=5)
    assert waiter.is_alive() is False
    assert attached["lease"].should_dispatch is False
    assert attached["lease"].result == _result("the holder's answer")


def test_a_waiter_dispatches_itself_when_the_holder_releases():
    """A refused generation is RELEASED rather than cached, so the key is free
    for a later attempt — and a caller already attached to it must then dispatch
    rather than wait forever for an answer that will never arrive."""
    store = store_mod.AbstractStore()
    key = _key()
    store.reserve(key)

    attached = {}
    waiter = threading.Thread(
        target=lambda: attached.update(lease=store.reserve(key)), daemon=True)
    waiter.start()
    waiter.join(timeout=0.2)
    assert waiter.is_alive() is True

    store.release(key)
    waiter.join(timeout=5)
    assert attached["lease"].should_dispatch is True
    assert attached["lease"].result is None


def test_a_released_key_is_free_for_a_later_attempt():
    store = store_mod.AbstractStore()
    key = _key()
    store.reserve(key)
    store.release(key)
    assert store.snapshot(key) is None
    assert store.reserve(key).should_dispatch is True


def test_completing_a_key_that_was_never_reserved_is_refused():
    store = store_mod.AbstractStore()
    with pytest.raises(store_mod.AbstractStoreConflictError):
        store.complete(_key(), _result(), size_bytes=32)


def test_completing_twice_is_refused_and_leaves_the_first_answer_standing():
    store = store_mod.AbstractStore()
    key = _key()
    store.reserve(key)
    store.complete(key, _result("first"), size_bytes=32)
    with pytest.raises(store_mod.AbstractStoreConflictError):
        store.complete(key, _result("second"), size_bytes=32)
    assert store.snapshot(key).result == _result("first")


# ---------------------------------------------------------------------------
# isolation: nothing a caller holds can rewrite what the store kept
# ---------------------------------------------------------------------------

def test_ingress_and_egress_are_isolated():
    store = store_mod.AbstractStore()
    key = _key()
    handed_in = _result("as stored")
    store.reserve(key)
    store.complete(key, handed_in, size_bytes=32)

    handed_in["body"]["prose"] = "mutated after the fact"
    assert store.snapshot(key).result == _result("as stored")

    handed_out = store.snapshot(key).result
    handed_out["body"]["prose"] = "mutated on the way out"
    assert store.snapshot(key).result == _result("as stored")


# ---------------------------------------------------------------------------
# eviction: deterministic, counter-ordered, and a re-dispatch afterwards
# ---------------------------------------------------------------------------

def test_eviction_is_deterministic_and_counter_ordered():
    """Over the entry bound the LEAST RECENTLY USED completed entry goes, and
    "recently used" is the store's own monotonic counter — a replay TOUCHES an
    entry, so the key a reader came back to survives while an older untouched
    one does not."""
    store = store_mod.AbstractStore()
    keys = _fill(store, store_mod.MAX_ABSTRACT_ENTRIES)
    # Come back to the OLDEST entry: it is now the most recently used.
    assert store.reserve(keys[0]).should_dispatch is False

    overflow = _key(path="ideation/staging/one-too-many/README.md")
    store.reserve(overflow)
    store.complete(overflow, _result("the newcomer"), size_bytes=64)

    assert store.snapshot(keys[0]) is not None, "the touched entry was evicted"
    assert store.snapshot(keys[1]) is None, "the least recently used survived"
    assert store.snapshot(overflow) is not None


def test_eviction_is_reproducible_across_two_identical_runs():
    """Determinism, asserted as determinism: the same operations in the same
    order evict the same keys, which a clock-ordered store cannot promise."""
    def _run():
        store = store_mod.AbstractStore()
        keys = _fill(store, store_mod.MAX_ABSTRACT_ENTRIES + 5)
        return tuple(store.snapshot(key) is not None for key in keys)

    assert _run() == _run()


def test_a_re_dispatch_after_eviction_is_expected_and_not_an_error():
    store = store_mod.AbstractStore()
    keys = _fill(store, store_mod.MAX_ABSTRACT_ENTRIES + 1)
    evicted = keys[0]
    assert store.snapshot(evicted) is None
    lease = store.reserve(evicted)  # not a conflict, not an error
    assert lease.should_dispatch is True


def test_the_byte_bound_evicts_too():
    store = store_mod.AbstractStore()
    big = store_mod.MAX_ABSTRACT_BYTES // 2
    first = _key(path="ideation/staging/first/README.md")
    second = _key(path="ideation/staging/second/README.md")
    third = _key(path="ideation/staging/third/README.md")
    for key in (first, second, third):
        store.reserve(key)
        store.complete(key, _result(), size_bytes=big)
    assert store.snapshot(first) is None
    assert store.snapshot(third) is not None


def test_an_in_flight_entry_is_never_evicted():
    store = store_mod.AbstractStore()
    held = _key(path="ideation/staging/held/README.md")
    store.reserve(held)
    _fill(store, store_mod.MAX_ABSTRACT_ENTRIES + 2)
    record = store.snapshot(held)
    assert record is not None
    assert record.state == store_mod.ABSTRACT_STATE_IN_FLIGHT


# ---------------------------------------------------------------------------
# task 5.4 (N1, explicitly): the chat ledger survives abstract churn
# ---------------------------------------------------------------------------

def _chat_key(index):
    return doxbench_scope.ScopeKey(repository="fixture-repo", ref="main",
                                   tile_kind="staged",
                                   tile_id=f"topic-{index:03d}")


def test_abstract_churn_never_evicts_the_chat_turn_stores_records():
    """TASK 5.4, asserted against the chat `TurnStore`'s OWN CONTENTS.

    A scope larger than the abstract bound is the ordinary case (N1: a
    200-document scope exceeds a 64-entry bound threefold), so this churns
    THREE TIMES the abstract bound and then reads every chat record back. A
    shared instance — the obvious implementation N1 refuses — fails here: the
    chat records would be the least recently used entries and would go first."""
    chat = doxbench_turns.TurnStore()
    abstracts = store_mod.AbstractStore()

    chat_keys = []
    for index in range(8):
        key = _chat_key(index)
        digest = f"{index:064d}"
        chat.reserve(key, "turn-0001", digest)
        chat.complete(key, "turn-0001", {"status": 200, "body": {"turn": index}},
                      size_bytes=128)
        chat_keys.append((key, digest))

    _fill(abstracts, store_mod.MAX_ABSTRACT_ENTRIES * 3)

    for index, (key, digest) in enumerate(chat_keys):
        record = chat.snapshot(key, "turn-0001")
        assert record is not None, f"chat record {index} was evicted"
        assert record.state == doxbench_turns.TURN_STATE_COMPLETED
        assert record.request_digest == digest
        assert record.validated_result == {"status": 200, "body": {"turn": index}}
        # And the chat surface still REPLAYS it, which is the observable N1 is
        # actually about: a retry that should replay must not re-dispatch.
        assert chat.reserve(key, "turn-0001", digest).should_dispatch is False

    # The abstract store really did churn past its own bound, so the assertion
    # above is about a store under eviction pressure and not an empty one.
    assert abstracts.snapshot(_key(path="ideation/staging/topic-0000/README.md")) is None


def test_the_two_stores_are_different_types_with_different_keys():
    """The shape is shared; the instance and the bound are not. Restated as a
    type pin so a later refactor cannot quietly make `AbstractStore` an alias of
    the chat ledger and keep every behavioural test above green."""
    assert store_mod.AbstractStore is not doxbench_turns.TurnStore
    assert not issubclass(store_mod.AbstractStore, doxbench_turns.TurnStore)
    key = _key()
    assert (key.repository, key.ref, key.subject_path, key.content_digest) == (
        REPOSITORY, REF, SUBJECT, DIGEST_A)
    assert copy.copy(key) == key


# ---------------------------------------------------------------------------
# the previous abstract, which the verifier takes as an ADDITIONAL base
# ---------------------------------------------------------------------------

def test_the_store_hands_back_the_latest_abstract_for_a_path():
    """The ratified rule is that a previously generated abstract is an
    ADDITIONAL verification base where one exists. Under the ruled key it can
    never be found under THIS key — a cached answer for the same bytes is
    replayed before any verification runs — so what "previously generated"
    means is the answer for an EARLIER DIGEST of the same document, and the
    store is what remembers it across the edit."""
    store = store_mod.AbstractStore()
    old = _key(digest=DIGEST_A)
    store.reserve(old)
    store.complete(old, _result("about the old bytes"), size_bytes=32,
                   abstract={"marker": "old"})
    assert store.latest_for_path(repository=REPOSITORY, ref=REF, subject_path=SUBJECT) == {"marker": "old"}

    new = _key(digest=DIGEST_B)
    store.reserve(new)
    store.complete(new, _result("about the new bytes"), size_bytes=32,
                   abstract={"marker": "new"})
    assert store.latest_for_path(repository=REPOSITORY, ref=REF, subject_path=SUBJECT) == {"marker": "new"}
    assert store.latest_for_path(repository=REPOSITORY, ref=REF,
                                 subject_path=OTHER_SUBJECT) is None


def test_the_latest_abstract_is_isolated_from_its_caller():
    store = store_mod.AbstractStore()
    key = _key()
    held = {"marker": "kept"}
    store.reserve(key)
    store.complete(key, _result(), size_bytes=32, abstract=held)
    held["marker"] = "mutated"
    assert store.latest_for_path(repository=REPOSITORY, ref=REF, subject_path=SUBJECT) == {"marker": "kept"}
    handed_out = store.latest_for_path(repository=REPOSITORY, ref=REF, subject_path=SUBJECT)
    handed_out["marker"] = "mutated on the way out"
    assert store.latest_for_path(repository=REPOSITORY, ref=REF, subject_path=SUBJECT) == {"marker": "kept"}


def test_an_evicted_entry_takes_its_abstract_with_it():
    """The previous-abstract base is a CACHE and never a record: once an entry
    is evicted the base is gone, and the next generation is verified against the
    snapshot's declared fields alone — which is the base that always exists."""
    store = store_mod.AbstractStore()
    first = _key(path="ideation/staging/evicted/README.md")
    store.reserve(first)
    store.complete(first, _result(), size_bytes=64, abstract={"marker": "gone"})
    _fill(store, store_mod.MAX_ABSTRACT_ENTRIES)
    assert store.snapshot(first) is None
    assert store.latest_for_path(repository=REPOSITORY, ref=REF,
                                 subject_path="ideation/staging/evicted/README.md") is None


# ---------------------------------------------------------------------------
# S3 (adversarial review, 2026-08-25) — THE KEY IS SCOPE-QUALIFIED
# ---------------------------------------------------------------------------
#
# `(subject path, content digest)` is one question per document only inside ONE
# scope. A served process reaches every repository its registry resolves and
# every ref of each, and `ideation/staging/x/README.md` exists in most of them —
# so two repositories that happen to hold identical bytes at one path shared a
# cache entry, and, worse, `latest_for_path` handed repository A's abstract to
# repository B as its PREVIOUS verification base. The key therefore carries the
# whole scope, exactly as the harness conversation key does; here the components
# are dataclass FIELDS, which are injective by construction, so no separator and
# no string composition is involved at all.


def test_two_scopes_holding_one_path_and_one_digest_are_two_keys():
    """Same document path, same content digest, two scopes: two questions. The
    second must DISPATCH rather than replay the first's answer."""
    store = store_mod.AbstractStore()
    mine = _key(repository="repo-a", ref="main")
    other_repo = _key(repository="repo-b", ref="main")
    other_ref = _key(repository="repo-a", ref="session/2026-08-25")
    assert len({mine, other_repo, other_ref}) == 3

    store.reserve(mine)
    store.complete(mine, _result("about repo-a@main"), size_bytes=32)
    # NOT a replay, and not an attach: a different scope is a different question
    assert store.reserve(other_repo).should_dispatch is True
    assert store.reserve(other_ref).should_dispatch is True
    assert store.snapshot(mine).result == _result("about repo-a@main")


def test_the_previous_base_never_crosses_a_scope():
    """The sharpest form of the same defect: `latest_for_path` feeds the
    VERIFIER, so a cross-scope hit would verify repository B's abstract against
    repository A's answer and could refuse it for dropping coverage of a
    document B never had."""
    store = store_mod.AbstractStore()
    mine = _key(repository="repo-a", ref="main")
    store.reserve(mine)
    store.complete(mine, _result(), size_bytes=32, abstract={"marker": "repo-a"})

    assert store.latest_for_path(repository="repo-a", ref="main",
                                 subject_path=SUBJECT) == {"marker": "repo-a"}
    assert store.latest_for_path(repository="repo-b", ref="main",
                                 subject_path=SUBJECT) is None
    assert store.latest_for_path(repository="repo-a", ref="session/x",
                                 subject_path=SUBJECT) is None
