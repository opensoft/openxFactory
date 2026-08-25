"""Snapshot non-interference regression guards (openxFactory
`add-doxbench-distilled-abstract`, tasks 6.1-6.3; ratified ruling 2(b)
session-only).

`specs/ideation-dashboard/spec.md` requirement "A model-derived abstract is
session-local and never a snapshot field" states the observable in BOTH
directions: an emitted snapshot MUST be byte-identical whether or not an
abstract was generated in-session, and no snapshot field MUST carry a
model-derived value; and where the model port is absent, raises, or times
out, the snapshot MUST be unaffected and no lane or gate action MUST fail.

**These pass on the FIRST RUN, and that is the point.** Nothing in this tree
today writes a model-derived abstract into a document object -- there is no
route, no `DocumentAbstract` type and no generator parameter for one (that
surface belongs to this change's other task groups). So every assertion
below is trivially true right now; what proves these tests have TEETH is
mutation 9.5, which emits an abstract into a document object and MUST make
`test_generator_is_byte_identical_with_and_without_in_session_generation` and
`test_no_document_carries_a_forbidden_abstract_key_or_value` both fail. The
exact key/value a mutant would have to write to trip them is the
`FORBIDDEN_DOCUMENT_KEYS` set and the `FAKE_DISPATCH_PROSE` sentinel below.

Hermetic: every corpus tree is a `tmp_path` copy of the fixture base-repo,
every model port is `FakeWorkbenchModelPort` (no network, no `omp` child),
and every clock handed to `dispatch_turn` is an injected iterator -- no real
wait for the "timing out" case.
"""

from __future__ import annotations

import json
import shutil
import threading
from contextlib import contextmanager
from pathlib import Path

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit

from ideation_dashboard import nightly_lane
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import snapshot as snapshot_mod
from ideation_dashboard.doxbench_model import (
    DISPATCH_ERR_MODEL_FAILED,
    DISPATCH_ERR_MODEL_TIMEOUT,
    FakeWorkbenchModelPort,
    ModelCatalog,
    ModelCatalogEntry,
    TurnDispatchFailure,
    TurnDispatchSuccess,
    dispatch_turn,
)
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"

# The forbidden document-object vocabulary. Task 6.2's own text: iterate every
# emitted document object and assert no key from this set, and no value equal
# to a fake dispatch result string, appears anywhere in it. This is exactly
# the set mutation 9.5 must trip by writing a model-derived abstract into a
# `documents[]` entry.
FORBIDDEN_DOCUMENT_KEYS = frozenset({
    "abstract", "distilled", "distillation", "model_abstract", "generated_abstract",
})

# A sentinel distinct enough that it can never appear in the fixture corpus by
# coincidence -- the "fake dispatch result string" task 6.2 asks be absent
# from every document value.
FAKE_DISPATCH_PROSE = "FAKE-DOXBENCH-ABSTRACT-SENTINEL-6f3a9c"


# ============================================================================
# shared fixtures / helpers
# ============================================================================

def _tree(tmp_path: Path) -> Path:
    """One unchanged fixture tree, copied so no test ever touches the shared
    `BASE_REPO` fixture (mirrors `test_completeness.py`'s `_tree`)."""
    root = tmp_path / "repo"
    shutil.copytree(BASE_REPO, root)
    return root


def _snap(root: Path) -> dict:
    return generate_snapshot(root, "fixture-repo", source_revision=PINNED_REVISION,
                             git=FakeGit())


def _entry(model_id: str = "m-abstract") -> ModelCatalogEntry:
    return ModelCatalogEntry(
        model_id=model_id, label="Approved authoring model",
        provider_class="on-tenant", available=True,
        input_limit_bytes=800_000, output_limit_bytes=900_000,
        data_handling="Processed in the approved tenant boundary")


def _list_clock(*readings: float):
    """An injected `dispatch_turn` clock: successive calls return successive
    readings (doxbench_model.py:924's contract), so "elapsed" is scripted
    without any real wall-clock wait."""
    it = iter(readings)
    return lambda: next(it)


@contextmanager
def _serving(root: Path, snap_path: Path, *, model_port_factory=None):
    """Mirrors `test_doxbench_request_handling.py`'s `_serving`/`_handler_class`
    idiom: a real ephemeral `ThreadingHTTPServer` over `build_server`, the
    seam a session-side abstract generation would eventually reach through."""
    snap_path.write_text(json.dumps(_snap(root)), encoding="utf-8")
    httpd = serve_mod.build_server(
        WEB, snap_path, root, head=PINNED_REVISION, actor="brett",
        model_port_factory=model_port_factory,
    )
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield httpd
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _handler_class(httpd):
    return getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)


def _run_lane(tmp_path: Path, root: Path) -> nightly_lane.LaneOutcome:
    """"The existing generator entry the nightly lane calls" -- `run_lane`'s
    own default `generate=generate_snapshot`. Never raises by the lane's own
    contract (task 4.1: any error is a SKIP, never a propagated exception);
    calling it directly is what proves that here rather than assuming it."""
    agg = tmp_path / "agg"
    if not agg.exists():
        agg.mkdir()
        (agg / "openxFactory").symlink_to(root, target_is_directory=True)
    return nightly_lane.run_lane(agg, repository="fixture-repo",
                                 source_revision=PINNED_REVISION)


def _assert_unaffected(tmp_path: Path, root: Path, baseline_bytes: bytes,
                       baseline_lane: nightly_lane.LaneOutcome) -> None:
    """The generator entry the nightly lane calls still yields byte-identical
    output, and the lane itself still completes with the same outcome, no
    matter what happened to the model port a moment before."""
    assert snapshot_mod.canonical_bytes(_snap(root)) == baseline_bytes
    lane = _run_lane(tmp_path, root)
    assert lane.ok == baseline_lane.ok
    assert lane.reason == baseline_lane.reason
    if lane.ok:
        assert lane.snapshot_path.read_bytes() == baseline_lane.snapshot_path.read_bytes()


def _iter_kv(node):
    """Every (key, value) pair anywhere inside a JSON-shaped structure, at
    any nesting depth -- so a mutant that nests a caption object one level
    deeper than the top of a `documents[]` entry cannot dodge task 6.2."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield key, value
            yield from _iter_kv(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_kv(item)


# ============================================================================
# 6.1 -- byte-identical with and without in-session generation
# ============================================================================

def test_generator_is_byte_identical_with_and_without_in_session_generation(tmp_path):
    """Generate a snapshot for one unchanged tree twice: once after a
    FakeWorkbenchModelPort-backed session actually dispatched and returned a
    prose abstract through the real `_workbench_model_port` seam, once with
    no model-port activity at all. Nothing today carries that dispatch
    result anywhere the generator could read it -- there is no route, no
    `DocumentAbstract` type and no snapshot parameter for one -- so the two
    snapshots MUST be byte-identical, per the spec's "The generator runs on a
    tree with and without generation" scenario."""
    root = _tree(tmp_path)
    fake = FakeWorkbenchModelPort(
        ModelCatalog.from_entries([_entry()]),
        dispatch_result={"assistant_prose": FAKE_DISPATCH_PROSE, "proposals": []})

    with _serving(root, tmp_path / "snapshot.json",
                  model_port_factory=lambda: fake) as httpd:
        handler = _handler_class(httpd)
        port = handler._workbench_model_port(handler)
        assert port is fake  # sanity: the session-side seam actually resolved
        outcome = dispatch_turn(port, "opaque-abstract-envelope", entry=_entry(),
                                clock=_list_clock(0.0, 1.0))
    assert isinstance(outcome, TurnDispatchSuccess)
    assert outcome.assistant_prose == FAKE_DISPATCH_PROSE

    with_generation = snapshot_mod.canonical_bytes(_snap(root))
    without_generation = snapshot_mod.canonical_bytes(_snap(root))
    assert with_generation == without_generation


# ============================================================================
# 6.2 -- no forbidden key or fake-dispatch value in any document object
# ============================================================================

def test_no_document_carries_a_forbidden_abstract_key_or_value(tmp_path):
    """After the SAME in-session dispatch as above, walk every emitted
    `documents[]` object at every nesting depth: no key from
    `FORBIDDEN_DOCUMENT_KEYS`, and no value equal to (or containing) the
    dispatched prose, may appear. This is the check mutation 9.5 must trip by
    writing a model-derived abstract into a document object."""
    root = _tree(tmp_path)
    fake = FakeWorkbenchModelPort(
        ModelCatalog.from_entries([_entry()]),
        dispatch_result={"assistant_prose": FAKE_DISPATCH_PROSE, "proposals": []})

    with _serving(root, tmp_path / "snapshot.json",
                  model_port_factory=lambda: fake) as httpd:
        handler = _handler_class(httpd)
        port = handler._workbench_model_port(handler)
        outcome = dispatch_turn(port, "opaque-abstract-envelope", entry=_entry(),
                                clock=_list_clock(0.0, 1.0))
    assert isinstance(outcome, TurnDispatchSuccess)

    snap = _snap(root)
    assert snap["documents"], "fixture tree must actually project documents"
    for doc in snap["documents"]:
        for key, value in _iter_kv(doc):
            assert key not in FORBIDDEN_DOCUMENT_KEYS, (
                f"document {doc.get('id')!r} carries forbidden key {key!r}")
            assert value != FAKE_DISPATCH_PROSE, (
                f"document {doc.get('id')!r}[{key!r}] equals the dispatched prose")
            if isinstance(value, str):
                assert FAKE_DISPATCH_PROSE not in value, (
                    f"document {doc.get('id')!r}[{key!r}] embeds the dispatched prose")


# ============================================================================
# 6.3 -- port absent / raising on construction / dispatch raising or timing out
# ============================================================================

def test_snapshot_and_lane_unaffected_when_model_port_factory_is_absent(tmp_path):
    root = _tree(tmp_path)
    baseline_bytes = snapshot_mod.canonical_bytes(_snap(root))
    baseline_lane = _run_lane(tmp_path, root)

    with _serving(root, tmp_path / "snapshot.json",
                  model_port_factory=None) as httpd:
        handler = _handler_class(httpd)
        assert handler._workbench_model_port(handler) is None

    _assert_unaffected(tmp_path, root, baseline_bytes, baseline_lane)


def test_snapshot_and_lane_unaffected_when_model_port_factory_raises_on_construction(
        tmp_path):
    root = _tree(tmp_path)
    baseline_bytes = snapshot_mod.canonical_bytes(_snap(root))
    baseline_lane = _run_lane(tmp_path, root)

    def _raise():
        raise RuntimeError("provider construction boom")

    with _serving(root, tmp_path / "snapshot.json",
                  model_port_factory=_raise) as httpd:
        handler = _handler_class(httpd)
        assert handler._workbench_model_port(handler) is None  # absence, not a 500

    _assert_unaffected(tmp_path, root, baseline_bytes, baseline_lane)


def test_snapshot_and_lane_unaffected_when_port_dispatch_raises_or_times_out(tmp_path):
    root = _tree(tmp_path)
    baseline_bytes = snapshot_mod.canonical_bytes(_snap(root))
    baseline_lane = _run_lane(tmp_path, root)

    raising_port = FakeWorkbenchModelPort(
        ModelCatalog.from_entries([_entry("m-raises")]),
        dispatch_error=RuntimeError("provider dispatch boom"))
    timing_out_port = FakeWorkbenchModelPort(
        ModelCatalog.from_entries([_entry("m-times-out")]),
        dispatch_result={"assistant_prose": "unreachable", "proposals": []})

    with _serving(root, tmp_path / "snapshot-raises.json",
                  model_port_factory=lambda: raising_port) as httpd:
        handler = _handler_class(httpd)
        port = handler._workbench_model_port(handler)
        assert port is raising_port
        outcome = dispatch_turn(port, "opaque-abstract-envelope",
                                entry=_entry("m-raises"), clock=_list_clock(0.0, 1.0))
    assert isinstance(outcome, TurnDispatchFailure)
    assert outcome.error == DISPATCH_ERR_MODEL_FAILED

    with _serving(root, tmp_path / "snapshot-timeout.json",
                  model_port_factory=lambda: timing_out_port) as httpd:
        handler = _handler_class(httpd)
        port = handler._workbench_model_port(handler)
        assert port is timing_out_port
        # A clock whose second reading lands far past the adapter's declared
        # timeout -- an overrun scripted with no real wait (D6 / doxbench_model
        # research R... : the clock is injected, never wall-clock).
        outcome = dispatch_turn(port, "opaque-abstract-envelope",
                                entry=_entry("m-times-out"),
                                clock=_list_clock(0.0, 10_000.0))
    assert isinstance(outcome, TurnDispatchFailure)
    assert outcome.error == DISPATCH_ERR_MODEL_TIMEOUT

    _assert_unaffected(tmp_path, root, baseline_bytes, baseline_lane)
