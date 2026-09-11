"""The COMMITTED intent feed and the `actions.intent` capability
(add-ideation-intent-plane task 4.4; Brett Heap's rulings D-1 / Path A on
openxFactory #656).

Four claims, each failing for its own reason:

  * **THE READER AGREES WITH PYYAML.** `intent_feed` parses the committed
    `.gate-intent.yaml` files with the standard library alone, because the
    hosted image is `python:3.12-slim` with no pip dependencies and PyYAML is
    not importable in the pod that has to answer this route. A hand-written
    reader is only as good as its oracle, so PyYAML — which the TEST
    environment does have — IS the oracle here, over a matrix of the values
    its own emitter is awkward about (unicode escapes, folded long lines,
    embedded quotes and colons and newlines, number-like and bool-like
    strings) and over documents written by the REAL apply lane.
  * **THE ROUTE SERVES THE CORPUS, READ-ONLY.** None, one applied, one
    refused, a malformed file skipped, an absent directory — and the filters
    that let one client ask this feed and the inbox the same question.
  * **THE CAPABILITY IS THE PLANE.** A served (non-loopback) plane advertises
    `actions.intent`; a loopback plane does not and keeps `gate = local_human`
    byte-identical. The gateway-stamped `hosted_actor` flips neither
    (`add-dashboard-account-menu` Requirement 2 stays true).
  * **THE MIRRORED CONSTANTS STAY MIRRORED.** `intent_feed` restates the
    apply lane's intents directory and verb/target table rather than importing
    them (the lane imports PyYAML at module scope, so the serving pod cannot
    import it at all). The restatement is guarded here, the way
    `corpus_root.SCANNED_ROOTS` is guarded against `doc_health.corpus`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from ideation_dashboard import intent_apply_lane as lane
from ideation_dashboard import intent_feed
from opendox import serve as serve_mod

from test_gate_routes import _get, _serving
from test_intent_apply_lane import _apply, _corpus, _intent

BANNER = (
    "# gate-intent — one human's REQUEST for a gate-console action\n"
    "# (gate-intent.schema.yaml). The actor was stamped by the intent inbox\n"
    "# from the ingress-authenticated identity; the apply lane revalidated\n"
    "# everything server-side before this file gained its terminal status.\n"
)


def _terminal(**over) -> dict:
    doc = {
        "schema_version": 1,
        "kind": "gate-intent",
        "actor": "brett",
        "verb": "dispose-possible",
        "target": {"possible_id": "pos-derived-x"},
        "args": {"outcome": "accepted", "note": "n"},
        "requested_at": "2026-08-10T12:00:00Z",
        "snapshot_rev_seen": "0" * 40,
        "status": "applied",
        "idempotency_key": "k-1",
        "applied_at": "2026-08-10T12:01:00Z",
        "applied_record": "ideation/dashboard/records/x.gate-action-record.yaml",
    }
    doc.update(over)
    return doc


def _refused(**over) -> dict:
    """A committed REFUSAL: the lane writes `refusal_reason` and neither
    `applied_at` nor `applied_record` (its `_decide_and_land` owns each set)."""
    doc = _terminal(status="refused",
                    refusal_reason="the viewed state is unverifiable")
    doc.pop("applied_at")
    doc.pop("applied_record")
    doc.update(over)
    return doc


def _write(root: Path, doc: dict, *, name: str | None = None,
           target_dir: str | None = None) -> Path:
    where = root / intent_feed.INTENTS_DIR / (
        target_dir or doc["target"]["possible_id"])
    where.mkdir(parents=True, exist_ok=True)
    path = where / (name or (doc["idempotency_key"] + ".gate-intent.yaml"))
    path.write_text(BANNER + yaml.safe_dump(doc, sort_keys=False),
                    encoding="utf-8")
    return path


# ==========================================================================
# the reader, with PyYAML as the oracle
# ==========================================================================

# Values chosen because PyYAML's emitter reaches for a DIFFERENT style for
# each of them: a plain scalar, a folded plain scalar, a single-quoted scalar
# (the colon, the leading space, the number-like and bool-like strings), and a
# double-quoted scalar with escapes and escaped line breaks (unicode, tab).
AWKWARD = [
    "a simple reason",
    "the viewed state is unverifiable — em dash",
    "it's a reason with an apostrophe",
    'a "quoted" reason',
    "line one\nline two",
    "two\n\nblank\n\n\nlines",
    "x" * 200,
    ("the target has materially advanced past the snapshot revision the actor "
     "was viewing when they decided, so the lane refuses this intent rather "
     "than applying a decision made against a state that no longer exists"),
    "reason: with a colon",
    "  leading space",
    "reason # with hash",
    "a\tb",
    "-",
    "123",
    "true",
    "null",
    "&amp start",
    "*star start",
    "|pipe start",
    "{brace}",
    "[bracket]",
    "многоязычный отказ с очень длинным текстом который будет свёрнут",
    "a\\backslash and a \"quote\" and an — emdash in one long folded line",
]


@pytest.mark.parametrize("value", AWKWARD)
@pytest.mark.parametrize("width", [None, 30, 1000])
def test_the_stdlib_reader_agrees_with_pyyaml(value, width):
    """The reader is hand-written because the serving pod has no PyYAML. Its
    correctness is therefore not a claim but a comparison: for every document
    the lane's own emitter can produce, this reader must return exactly what
    PyYAML returns."""
    doc = _refused(refusal_reason=value,
                   args={"outcome": "rejected", "note": value})
    kwargs = {"width": width} if width else {}
    text = BANNER + yaml.safe_dump(doc, sort_keys=False, **kwargs)
    assert intent_feed.parse_intent_document(text) == yaml.safe_load(text)


@pytest.mark.parametrize("allow_unicode", [False, True])
def test_the_reader_agrees_with_pyyaml_on_unicode_emission(allow_unicode):
    """`allow_unicode` decides between a `\\uXXXX` escape and the character
    itself; the reader must read both spellings of the same reason."""
    doc = _refused(refusal_reason="отказ — the viewed state is unverifiable")
    text = BANNER + yaml.safe_dump(doc, sort_keys=False,
                                   allow_unicode=allow_unicode)
    assert intent_feed.parse_intent_document(text) == yaml.safe_load(text)


def test_the_reader_round_trips_intents_the_real_apply_lane_wrote(tmp_path):
    """The strongest form of the same claim: no synthetic document at all.
    The REAL lane applies a real intent into a real git corpus, and the reader
    reads back exactly what PyYAML reads from the file it committed."""
    root, rev, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent(rev), allowlist, tmp_path)
    assert report.outcome == "applied", report.reason
    text = (root / report.intent_path).read_text(encoding="utf-8")
    assert intent_feed.parse_intent_document(text) == yaml.safe_load(text)


def test_a_document_that_is_not_the_lanes_shape_is_skipped_not_guessed_at():
    for text in ("just some prose\nnot yaml at all\n",
                 "",
                 "- a\n- b\n",
                 BANNER,
                 "schema_version: 1\nkind: gate-intent\nbroken\n"):
        assert intent_feed.parse_intent_document(text) is None, text


def test_a_nested_or_sequence_arg_drops_that_member_not_the_document():
    """`args` is decoration — the feed's contract is the terminal fields — so a
    member the reader cannot read confidently is dropped while the document
    (and its status, and its reason) survives."""
    doc = _terminal(args={"outcome": "accepted", "items": ["a", "b"],
                          "deep": {"a": 1}})
    parsed = intent_feed.parse_intent_document(
        BANNER + yaml.safe_dump(doc, sort_keys=False))
    assert parsed["args"] == {"outcome": "accepted"}
    assert parsed["status"] == "applied"


# ==========================================================================
# the mirrored constants
# ==========================================================================

def test_the_intents_dir_and_verb_table_mirror_the_apply_lane():
    """`intent_feed` cannot IMPORT the lane (the lane imports PyYAML at module
    scope and the serving pod has none), so it restates these two. The
    restatement is only safe while a test holds it to the original."""
    assert intent_feed.INTENTS_DIR == lane.DEFAULT_INTENTS_DIR
    assert intent_feed.VERB_TARGET_KEY == lane.VERB_TARGET_KEY


def test_the_web_bundle_mirrors_the_same_verb_table():
    """The browser builds the target object the inbox digests, and the inbox
    digests the RAW object it is handed — so a browser that spells a target key
    differently from the lane mints a request identity the lane never
    recomputes, and the pending chip never resolves to its own outcome."""
    source = (Path(serve_mod.__file__).parent / "web" / "views"
              / "intent-feed.js").read_text(encoding="utf-8")
    for verb, key in intent_feed.VERB_TARGET_KEY.items():
        assert f'"{verb}": "{key}"' in source, verb


# ==========================================================================
# read_committed_intents
# ==========================================================================

def test_no_directory_is_an_empty_feed_not_an_error(tmp_path):
    """A checkout with no intents yet is the ordinary first state; the overlay
    must be able to say "nothing yet" rather than "the feed is broken"."""
    document = intent_feed.read_committed_intents(tmp_path)
    assert document["intents"] == []
    assert document["truncated"] is False


def test_one_applied_and_one_refused_come_back_newest_first(tmp_path):
    _write(tmp_path, _terminal(idempotency_key="k-applied"))
    _write(tmp_path, _refused(idempotency_key="k-refused",
                              requested_at="2026-08-11T09:00:00Z"))
    document = intent_feed.read_committed_intents(tmp_path)
    states = [(r["status"], r["idempotency_key"]) for r in document["intents"]]
    assert states == [("refused", "k-refused"), ("applied", "k-applied")]
    refused = document["intents"][0]
    assert refused["refusal_reason"] == "the viewed state is unverifiable"
    assert refused["target_id"] == "pos-derived-x"
    assert refused["source"] == "corpus"
    assert refused["path"].startswith(intent_feed.INTENTS_DIR)


def test_a_malformed_file_is_skipped_and_the_rest_still_serve(tmp_path):
    _write(tmp_path, _terminal(idempotency_key="k-good"))
    bad = tmp_path / intent_feed.INTENTS_DIR / "pos-derived-x" / \
        "broken.gate-intent.yaml"
    bad.write_text("this is not an intent at all\n", encoding="utf-8")
    document = intent_feed.read_committed_intents(tmp_path)
    assert [r["idempotency_key"] for r in document["intents"]] == ["k-good"]
    assert document["skipped"] == 1


def test_a_pending_file_is_not_served_as_a_decision(tmp_path):
    """Only TERMINAL intents are committed. A `pending` file means the corpus
    disagrees with the lane, and the feed does not launder that into a chip."""
    doc = _terminal(status="pending")
    doc.pop("applied_at")
    doc.pop("applied_record")
    _write(tmp_path, doc)
    assert intent_feed.read_committed_intents(tmp_path)["intents"] == []


def test_a_reasonless_refusal_is_skipped(tmp_path):
    """"A refused intent is visible" means WITH its reason (the delta's own
    scenario). A refusal file with no reason is a defect in the file, not a
    reasonless refusal to render."""
    doc = _refused()
    doc.pop("refusal_reason")
    _write(tmp_path, doc)
    assert intent_feed.read_committed_intents(tmp_path)["intents"] == []


def test_filters_narrow_by_actor_status_and_target(tmp_path):
    _write(tmp_path, _terminal(idempotency_key="k-brett"))
    _write(tmp_path, _terminal(actor="auditor", idempotency_key="k-auditor"))
    _write(tmp_path, _terminal(
        target={"possible_id": "pos-other"}, idempotency_key="k-other"))
    by_actor = intent_feed.read_committed_intents(tmp_path, actor="auditor")
    assert [r["idempotency_key"] for r in by_actor["intents"]] == ["k-auditor"]
    by_target = intent_feed.read_committed_intents(tmp_path, target="pos-other")
    assert [r["idempotency_key"] for r in by_target["intents"]] == ["k-other"]
    by_status = intent_feed.read_committed_intents(tmp_path, status="refused")
    assert by_status["intents"] == []


def test_the_feed_is_bounded_and_says_when_a_bound_bit(tmp_path):
    for n in range(5):
        _write(tmp_path, _terminal(idempotency_key=f"k-{n}",
                                   requested_at=f"2026-08-1{n}T12:00:00Z"))
    document = intent_feed.read_committed_intents(tmp_path, limit=2)
    assert len(document["intents"]) == 2
    assert document["truncated"] is True


def test_the_walk_itself_stops_at_the_cap_rather_than_listing_the_corpus(
        tmp_path, monkeypatch):
    """The file cap has to bind the LISTING, not only the reading.

    `sorted(rglob(...))` materialises and orders every intent in the directory
    before the first one is opened, so a request that stops at `MAX_FILES`
    still pays for the whole corpus — which nothing prunes, on a route every
    open tab polls every 15 seconds. The walk is watched here rather than the
    clock: exactly `MAX_FILES + 1` paths may be pulled, the extra one being the
    look-ahead that sets `truncated`."""
    monkeypatch.setattr(intent_feed, "MAX_FILES", 3)
    for n in range(20):
        _write(tmp_path, _terminal(idempotency_key=f"k-{n:02d}"))
    pulled: list[Path] = []
    real_rglob = Path.rglob

    def counting_rglob(self, pattern, *args, **kwargs):
        for found in real_rglob(self, pattern, *args, **kwargs):
            pulled.append(found)
            yield found

    monkeypatch.setattr(Path, "rglob", counting_rglob)
    document = intent_feed.read_committed_intents(tmp_path)
    assert len(pulled) == 4                       # MAX_FILES + 1, not 20
    assert document["scanned"] == 3
    assert document["truncated"] is True
    assert len(document["intents"]) == 3


def test_bounded_paths_never_drains_the_walk_it_is_handed():
    """Stated as a unit over an ENDLESS walk, which no cap-after-the-fact can
    survive: `bounded_paths` returns, so it took a bounded number of paths."""
    pulled = 0

    def endless():
        nonlocal pulled
        while True:
            pulled += 1
            yield (Path(intent_feed.INTENTS_DIR)
                   / f"{pulled:09d}.gate-intent.yaml")

    paths, truncated = intent_feed.bounded_paths(endless(), limit=5)
    assert pulled == 6                            # limit + 1 look-ahead
    assert len(paths) == 5
    assert truncated is True
    assert paths == sorted(paths)                 # a deterministic read order


def test_a_walk_inside_the_cap_is_not_reported_truncated():
    where = Path(intent_feed.INTENTS_DIR)
    paths, truncated = intent_feed.bounded_paths(
        iter([where / "b.gate-intent.yaml",
              where / "a.gate-intent.yaml"]), limit=5)
    assert truncated is False
    assert [p.name for p in paths] == ["a.gate-intent.yaml",
                                       "b.gate-intent.yaml"]


def test_an_oversized_file_is_skipped_rather_than_read(tmp_path, monkeypatch):
    monkeypatch.setattr(intent_feed, "MAX_FILE_BYTES", 32)
    _write(tmp_path, _terminal())
    document = intent_feed.read_committed_intents(tmp_path)
    assert document["intents"] == []
    assert document["skipped"] == 1


# ==========================================================================
# symlinks: this route is served to an unauthenticated-to-this-pod browser
# over a directory the reader does not otherwise control, so a symlink
# planted under it (file or directory) must never let the reader escape
# `ideation/dashboard/intents/`.
# ==========================================================================

def test_a_symlinked_intent_file_pointing_outside_base_is_not_read(tmp_path):
    """The leaf itself is a symlink: refused before it is ever opened,
    regardless of what it points at or what it contains."""
    outside = tmp_path / "outside"
    outside.mkdir()
    target = outside / "secret.gate-intent.yaml"
    target.write_text(
        BANNER + yaml.safe_dump(_terminal(idempotency_key="k-outside"),
                                sort_keys=False),
        encoding="utf-8")
    where = tmp_path / intent_feed.INTENTS_DIR / "pos-derived-x"
    where.mkdir(parents=True)
    (where / "evil.gate-intent.yaml").symlink_to(target)
    document = intent_feed.read_committed_intents(tmp_path)
    assert document["intents"] == []
    assert document["skipped"] == 1


def test_a_symlinked_directory_is_not_descended(tmp_path):
    """A symlinked directory under the intents tree must not be walked at
    all — nothing behind it may reach the feed. (`Path.rglob` itself already
    refuses to recurse into a symlinked directory, so nothing is even
    offered to the reader's own filter to skip; `skipped` stays 0 and the
    only observable guarantee that matters — nothing behind the symlink
    leaked into the feed — holds either way.)"""
    outside = tmp_path / "outside-dir"
    outside.mkdir()
    (outside / "k-outside.gate-intent.yaml").write_text(
        BANNER + yaml.safe_dump(_terminal(idempotency_key="k-outside"),
                                sort_keys=False),
        encoding="utf-8")
    base = tmp_path / intent_feed.INTENTS_DIR
    base.mkdir(parents=True)
    (base / "pos-derived-x").symlink_to(outside, target_is_directory=True)
    document = intent_feed.read_committed_intents(tmp_path)
    assert document["intents"] == []
    assert document["skipped"] == 0


def test_a_regular_file_is_still_read_beside_a_symlink_escape_attempt(tmp_path):
    """The fix must not cost the ordinary case: a real committed intent beside
    a symlink escape attempt is still served, and only the attempt is
    dropped."""
    outside = tmp_path / "outside"
    outside.mkdir()
    target = outside / "secret.gate-intent.yaml"
    target.write_text(
        BANNER + yaml.safe_dump(_terminal(idempotency_key="k-outside"),
                                sort_keys=False),
        encoding="utf-8")
    _write(tmp_path, _terminal(idempotency_key="k-good"))
    where = tmp_path / intent_feed.INTENTS_DIR / "pos-derived-x"
    (where / "evil.gate-intent.yaml").symlink_to(target)
    document = intent_feed.read_committed_intents(tmp_path)
    assert [r["idempotency_key"] for r in document["intents"]] == ["k-good"]
    assert document["skipped"] == 1


# ==========================================================================
# the MAX_FILES walk cap, at its real (unmocked) value
# ==========================================================================

def test_more_than_max_files_intents_is_capped_and_marked_truncated(tmp_path):
    """`test_the_walk_itself_stops_at_the_cap_rather_than_listing_the_corpus`
    covers the cap MECHANISM with `MAX_FILES` monkeypatched down to 3; this
    covers the cap at its real production value, with a real corpus that
    exceeds it, so the response's own diagnostics (not a patched constant)
    are what confirm the walk stopped short of the whole directory."""
    n = intent_feed.MAX_FILES + 2
    for i in range(n):
        _write(tmp_path, _terminal(idempotency_key=f"k-{i:05d}"))
    document = intent_feed.read_committed_intents(
        tmp_path, limit=intent_feed.MAX_LIMIT)
    assert document["truncated"] is True
    assert document["skipped"] == 0
    assert document["scanned"] == intent_feed.MAX_FILES
    assert len(document["intents"]) == intent_feed.MAX_LIMIT


# ==========================================================================
# the route
# ==========================================================================

def _seed(root: Path) -> None:
    _write(root, _terminal(idempotency_key="k-applied"))
    _write(root, _refused(idempotency_key="k-refused",
                          requested_at="2026-08-11T09:00:00Z"),
           name="refused.gate-intent.yaml")


def test_the_route_serves_an_empty_feed_before_anything_is_committed(
        tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, _root):
        status, document = _get(host, port, "/committed-intents.json")
    assert status == 200, document
    assert document["kind"] == "committed-intent-feed"
    assert document["intents"] == []


def test_the_route_serves_the_committed_intents_and_filters_them(
        tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        _seed(root)
        status, document = _get(host, port, "/committed-intents.json")
        _s2, refused = _get(host, port,
                            "/committed-intents.json?status=refused")
        _s3, mine = _get(host, port, "/committed-intents.json?actor=brett")
        _s4, other = _get(host, port, "/committed-intents.json?actor=nobody")
    assert status == 200, document
    assert [r["status"] for r in document["intents"]] == ["refused", "applied"]
    assert [r["idempotency_key"] for r in refused["intents"]] == ["k-refused"]
    assert len(mine["intents"]) == 2
    assert other["intents"] == []


def test_the_route_is_read_only_and_answers_after_the_lane_commits(
        tmp_path, monkeypatch):
    """Read PER REQUEST, like the project register: the apply lane commits
    between polls, and on the hosted plane a rebake replaces the baked tree
    under a running pod."""
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        _s, before = _get(host, port, "/committed-intents.json")
        assert before["intents"] == []
        _seed(root)
        _s2, after = _get(host, port, "/committed-intents.json")
    assert len(after["intents"]) == 2


def test_the_route_survives_a_malformed_committed_file(tmp_path, monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        _seed(root)
        bad = root / intent_feed.INTENTS_DIR / "pos-derived-x" / \
            "junk.gate-intent.yaml"
        bad.write_text("\x00 not a document\n", encoding="utf-8")
        status, document = _get(host, port, "/committed-intents.json")
    assert status == 200
    assert len(document["intents"]) == 2
    assert document["skipped"] == 1


def test_the_route_never_serves_a_pod_credential_or_a_write(tmp_path,
                                                            monkeypatch):
    """D16 / ruling D-1: the feed is a read of files the pod already has. It is
    a GET-only route — a POST to it is not a write path in disguise."""
    import http.client
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, root):
        _seed(root)
        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request("POST", "/committed-intents.json",
                     body=b"{}", headers={"Content-Type": "application/json",
                                          "Content-Length": "2"})
        status = conn.getresponse().status
        conn.close()
    assert status >= 400


# ==========================================================================
# the capability
# ==========================================================================

def test_a_loopback_plane_keeps_gate_and_offers_no_intent(tmp_path,
                                                          monkeypatch):
    with _serving(tmp_path, monkeypatch=monkeypatch) as (host, port, _root):
        _s, caps = _get(host, port, "/capabilities")
    assert caps["actions"]["gate"] is True
    assert caps["actions"]["intent"] is False


def test_a_served_plane_offers_intent_and_no_executing_gate(tmp_path,
                                                            monkeypatch):
    with _serving(tmp_path, host="0.0.0.0",
                  monkeypatch=monkeypatch) as (host, port, _root):
        _s, caps = _get(host, port, "/capabilities")
    assert caps["actions"]["intent"] is True
    for verb in ("gate", "session", "edit"):
        assert caps["actions"][verb] is False, verb


def test_the_two_transports_are_mutually_exclusive():
    """D5's pair, stated directly against the computation: exactly one of
    `gate` and `intent` is ever true, so a tray asks one question."""
    for loopback in (True, False):
        for actor in (None, "brett"):
            for real in (True, False):
                caps = serve_mod.compute_capabilities(
                    nlm_present=False, checkout_real=real, loopback=loopback,
                    actor=actor)
                actions = caps["actions"]
                assert not (actions["gate"] and actions["intent"])
                assert actions["intent"] is (not loopback)


def test_the_stamped_hosted_actor_still_flips_no_capability_verdict(
        tmp_path, monkeypatch):
    """`add-dashboard-account-menu` Requirement 2 survives this change: the
    per-request identity header changes no `actions` value, `intent`
    included."""
    import http.client

    def _caps(host, port, headers):
        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request("GET", "/capabilities", headers=headers)
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        conn.close()
        return payload

    with _serving(tmp_path, host="0.0.0.0",
                  monkeypatch=monkeypatch) as (host, port, _root):
        without = _caps(host, port, {})
        with_actor = _caps(host, port, {"X-Auth-Request-User": "alice"})
    assert without["hosted_actor"] is None
    assert with_actor["hosted_actor"] == "alice"
    assert with_actor["actions"] == without["actions"]
    assert with_actor["actions"]["intent"] is True


def test_the_pre_route_default_carries_the_new_key():
    """A hand-built handler (the shape several route tests construct) must not
    KeyError on `actions.intent`."""
    assert serve_mod._DEFAULT_CAPABILITIES["actions"]["intent"] is False
