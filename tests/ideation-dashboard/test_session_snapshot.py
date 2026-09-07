"""The SESSION VIEW: what a live session projects, where its reads are confined,
and what survives a process boundary (007-workbench-branch-sessions T028-T032,
T033b).

Phase 3 proved a session can be OPENED and WRITTEN to. This file proves it can be
SEEN — and, just as load-bearing, that seeing it changes nothing about what
everybody else sees. Four invariants earn their own sections:

  * **The projection is an ENTRY, not an overlay** (FR-009/FR-010). The session is
    a `(repository, session-branch)` row in the SAME snapshot registry, whose
    `source_root` is the worktree and whose snapshot is generated FROM that
    worktree. The discriminating assertion throughout is
    `generation.source_revision == <the action's commit>`: it proves the snapshot
    was regenerated from the worktree AFTER the action landed, which neither a
    stale file nor a `main`-derived overlay could satisfy.

  * **Confinement is BIDIRECTIONAL** (FR-014a, the ninth ADDED requirement). The
    shared surfaces — the wheel, the funnel, the pipeline board — render the
    snapshot the shell fetches with NO key, i.e. the ACTIVE entry, so "they still
    render `main`" is asserted as "the active entry is still `(repo, main)` and its
    bytes carry no session draft". In the OTHER direction a second resolved actor
    who JOINS the session sees the session's drafts: the confinement is to the
    SESSION, never to the actor who wrote first.

  * **Publication is the refused direction** (FR-012). The SERVING index still
    advertises the session ref — that is exactly the roster FR-014 validates a
    session key against — while `assert_publishable` refuses the PUBLISHED index.
    Both are asserted, because getting only the first half right is how a session
    draft reaches a published projection.

  * **Liveness survives a process, and only through the joint signal** (FR-008,
    T033b). `SnapshotRegistry._entries` is an in-process dict, so a restart is a
    real event: the bootstrap re-derives an entry for every worktree under the
    sessions container WHOSE BRANCH STILL EXISTS, and a half-signal (worktree with
    no branch, branch with no worktree) stays NON-LIVE and is reported stale for
    the human. Without that, a JOIN would open a second session and `propose`
    would proceed over unmerged drafts (the D15 hazard).

Every test builds on the `scratch_repo` harness: a throwaway checkout with a local
bare `origin`. No serve here is ever pointed at a real or fixture tree — a serve
WRITES into whatever `--checkout-root` it is given (research R10).
"""

from __future__ import annotations

import http.client
import json
import shutil
import subprocess
import threading
import urllib.parse
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import REPO_ROOT, serve_surface_source

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import session_git as sg
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
MODEL_JS = WEB / "views" / "repo-selector-model.js"
NODE = shutil.which("node")

CREATE_BODY = {
    "title": "First Draft",
    "summary": "The session's first document.",
    "topics": ["alpha"],
    "area": "ideation/staging/demo-topic/",
    "repository_context": REPO,
}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _scoped(**extra) -> dict:
    return {**CREATE_BODY, "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            **extra}


def _create(repo, registry, body=None, *, actor="brett"):
    """One `create-document` gate action through the ROUTE, exactly as `serve.py`
    dispatches it: the served checkout as `checkout_root` (never the worktree) and
    the session resolved from the body's tile scope."""
    status, payload = gr.run_gate_action(
        "create-document", dict(body if body is not None else _scoped()),
        checkout_root=repo.root, actor=actor, snapshot_path=None,
        session_registry=registry, repository=repo.repository)
    assert status == 200, payload
    return payload


def _main_snapshot_file(repo, path: Path) -> Path:
    """`main`'s snapshot, generated from the SERVED checkout at call time. Written
    outside the checkout, so generating it never changes the served tree."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    return path


def _registry_with_main(repo, tmp_path, *, name="main-snapshot.json"):
    """A registry in the shape a serve holds one: `(repository, main)` registered
    and ACTIVE with the served checkout as its source root. Every FR-014a
    assertion is measured against this starting state — with no `main` entry the
    session would become active by default and the assertion would be vacuous."""
    path = _main_snapshot_file(repo, tmp_path / name)
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry, path


def _session_entry(registry, *, repository=REPO, branch=DRAFT):
    entry = registry.get(repository, branch)
    assert entry is not None, f"no registry entry for {repository}@{branch}"
    return entry


def _session_snapshot(registry, *, repository=REPO, branch=DRAFT) -> dict:
    doc = _session_entry(registry, repository=repository, branch=branch).read_json()
    assert isinstance(doc, dict), "the session entry serves no snapshot bytes"
    return doc


def _doc_paths(snapshot) -> set[str]:
    return {d["path"] for d in (snapshot or {}).get("documents") or []}


def _index_keys(index) -> list[tuple[str, str]]:
    return [(e["repository"], e["ref"]) for e in index.get("entries") or []]


@contextmanager
def _serving(repo, snapshot_path):
    """A serve over real HTTP against the SCRATCH checkout. This is also the
    T033a bootstrap under test: `build_server` gets an empty registry and must
    re-derive the session entries before it answers anything (quickstart step 3)."""
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, actor="tester")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port, httpd
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _get(host, port, path):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", path)
    resp = conn.getresponse()
    body = resp.read()
    headers = {k.lower(): v for k, v in resp.getheaders()}
    status = resp.status
    conn.close()
    return status, headers, body


# ==========================================================================
# T028 — the session snapshot exists, `main`'s does not carry it, and the
# shared surfaces are untouched (FR-009, FR-010, FR-014a)
# ==========================================================================

def test_a_created_document_is_in_the_session_snapshot_and_absent_from_mains(
        scratch_repo, tmp_path):
    """FR-009/FR-010: the session projects through the EXISTING registry entry
    type, rooted at the worktree, generated FROM the worktree."""
    registry, _main = _registry_with_main(scratch_repo, tmp_path)

    payload = _create(scratch_repo, registry)

    entry = _session_entry(registry)
    assert isinstance(entry, reg.SnapshotEntry)          # the existing type
    assert entry.ref == DRAFT
    assert entry.source_root == bs.worktree_path(scratch_repo.root, DRAFT)
    assert entry.available is True

    session = _session_snapshot(registry)
    assert payload["path"] in _doc_paths(session)
    # the projection was generated FROM the worktree AT this action's commit —
    # neither a stale file nor a `main` overlay could satisfy this
    assert session["generation"]["source_revision"] == payload["commit"]

    # `main`, regenerated AFTER the session write, carries none of it
    fresh_main = generate_snapshot(scratch_repo.root, REPO)
    assert payload["path"] not in _doc_paths(fresh_main)
    assert not (scratch_repo.root / payload["path"]).exists()

    # exactly TWO rows: no overlay, no diff layer, no second projection path
    assert registry.keys() == [(REPO, DRAFT), (REPO, reg.DEFAULT_REF)]


def test_unregistering_the_entry_is_the_one_way_a_session_stops_being_live(
        scratch_repo, tmp_path):
    """T033's other half. A session ends by DROPPING its entry through the
    registry's EXISTING removal — no second removal path, so the two endings
    (FR-021) cannot diverge into two notions of "ended"."""
    registry, _ = _registry_with_main(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    assert bs.is_live(registry, REPO, DRAFT) is True

    bs.unregister_session_entry(registry, REPO, DRAFT)

    assert bs.is_live(registry, REPO, DRAFT) is False
    assert registry.get(REPO, DRAFT) is None
    assert registry.keys() == [(REPO, reg.DEFAULT_REF)]
    assert registry.active.ref == reg.DEFAULT_REF
    # the branch and the worktree are untouched: liveness is the ENTRY, and the
    # rest is removed by a deliberate teardown (FR-021), not by a projection change
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is True
    assert bs.worktree_path(scratch_repo.root, DRAFT).is_dir()

    # it delegates to the registry's own `drop` and does nothing else
    class _SpyRegistry:
        def __init__(self):
            self.dropped = []

        def drop(self, repository, ref=None):
            self.dropped.append((repository, ref))

    spy = _SpyRegistry()
    bs.unregister_session_entry(spy, REPO, DRAFT)
    assert spy.dropped == [(REPO, DRAFT)]
    assert [n for n in bs.__all__ if "unregister" in n] == ["unregister_session_entry"]


def test_the_shared_surfaces_keep_rendering_main_while_a_session_is_live(
        scratch_repo, tmp_path):
    """FR-014a: the wheel, the funnel, and the pipeline board render the snapshot
    the shell fetches with NO key — the ACTIVE entry. The session ref enters the
    registry's and the selector's KEY SPACE and changes nothing else."""
    registry, _main = _registry_with_main(scratch_repo, tmp_path)
    payload = _create(scratch_repo, registry)

    assert registry.active is not None
    assert registry.active.ref == reg.DEFAULT_REF
    index = registry.index_document()
    assert index["active"] == {"repository": REPO, "ref": reg.DEFAULT_REF}
    assert (REPO, DRAFT) in _index_keys(index)           # keyed, never active

    # and over HTTP, from a fresh serve whose registry was bootstrapped: the
    # unkeyed snapshot is `main`'s and carries no session draft
    main_path = _main_snapshot_file(scratch_repo, tmp_path / "served.json")
    with _serving(scratch_repo, main_path) as (host, port, _httpd):
        status, headers, body = _get(host, port, serve_mod.SNAPSHOT_ROUTE)
    assert status == 200
    assert headers["x-snapshot-ref"] == reg.DEFAULT_REF
    assert payload["path"] not in _doc_paths(json.loads(body))


# ==========================================================================
# T028a — the OTHER direction of FR-014a: a JOINING actor SEES the drafts
# ==========================================================================

def test_a_second_actor_joining_the_session_sees_the_sessions_drafts(
        scratch_repo, tmp_path):
    """FR-014a clause 3: confinement is to the SESSION, never to the first writer.
    The second actor arrives in a FRESH PROCESS (an empty registry, re-derived
    from the container), which is how a second human actually shows up."""
    first_registry, _ = _registry_with_main(scratch_repo, tmp_path, name="a.json")
    first = _create(scratch_repo, first_registry, actor="brett")

    second_registry, _ = _registry_with_main(scratch_repo, tmp_path, name="b.json")
    bs.bootstrap_sessions(second_registry, repository=REPO,
                          checkout_root=scratch_repo.root)
    second = _create(scratch_repo, second_registry, _scoped(title="Danas Draft"),
                     actor="dana")

    assert second["joined"] is True
    assert second["ref"] == first["ref"] == DRAFT
    docs = _doc_paths(_session_snapshot(second_registry))
    assert {first["path"], second["path"]} <= docs

    # the FIRST actor's process sees Dana's draft too, once it re-derives — the
    # session is the unit of visibility, and both writers share it
    refreshed, _ = _registry_with_main(scratch_repo, tmp_path, name="c.json")
    bs.bootstrap_sessions(refreshed, repository=REPO,
                          checkout_root=scratch_repo.root)
    assert {first["path"], second["path"]} <= _doc_paths(_session_snapshot(refreshed))

    # and a PUBLISHED projection still shows none of them (clause 2)
    with pytest.raises(reg.PublicationRefused):
        second_registry.index_document(published=True)
    assert not ({first["path"], second["path"]}
                & _doc_paths(generate_snapshot(scratch_repo.root, REPO)))


# ==========================================================================
# T029 — regenerated after EVERY gate action, with no manual step (FR-010)
# ==========================================================================

def test_the_session_snapshot_regenerates_after_every_gate_action(scratch_repo,
                                                                  tmp_path):
    """FR-010: no manual step between an action and its appearance in that
    session's panels. This test calls NO refresh route and NO refresh binding —
    the regeneration rides the action's own commit path, so a later verb cannot
    forget it."""
    registry, _ = _registry_with_main(scratch_repo, tmp_path)

    first = _create(scratch_repo, registry)
    after_first = _session_snapshot(registry)
    assert first["path"] in _doc_paths(after_first)
    assert after_first["generation"]["source_revision"] == first["commit"]

    second = _create(scratch_repo, registry, _scoped(title="Second Draft"))
    after_second = _session_snapshot(registry)
    assert {first["path"], second["path"]} <= _doc_paths(after_second)
    # the second action's own commit — a snapshot left at the FIRST commit would
    # be the "one manual step away" bug this requirement exists to close
    assert after_second["generation"]["source_revision"] == second["commit"]
    assert second["commit"] != first["commit"]

    git = sg.SessionGit(scratch_repo.root)
    assert git.commits_ahead("main", DRAFT) == 2
    # the derived snapshot lives OUTSIDE the worktree, so it can never be
    # committed onto the branch by a later stage-explicit-paths action
    entry = _session_entry(registry)
    assert bs.worktree_path(scratch_repo.root, DRAFT) not in \
        Path(entry.snapshot_path).parents


# ==========================================================================
# T030 — the freshness header names the SESSION BRANCH (FR-011)
# ==========================================================================

def test_the_freshness_header_names_the_session_branch_as_the_active_ref(
        scratch_repo, tmp_path):
    """FR-011 / SC-005: no rendered session panel may be ambiguous about whether
    it is showing `main` or a draft, and the transport half of that header is
    `X-Snapshot-Ref`."""
    registry, _ = _registry_with_main(scratch_repo, tmp_path)
    payload = _create(scratch_repo, registry)
    main_path = _main_snapshot_file(scratch_repo, tmp_path / "served.json")

    with _serving(scratch_repo, main_path) as (host, port, _httpd):
        keyed = _get(host, port, f"{serve_mod.SNAPSHOT_ROUTE}"
                                 f"?repository={REPO}&ref={DRAFT}")
        unkeyed = _get(host, port, serve_mod.SNAPSHOT_ROUTE)

    status, headers, body = keyed
    assert status == 200
    assert headers["x-snapshot-repository"] == REPO
    assert headers["x-snapshot-ref"] == DRAFT
    assert headers["x-snapshot-origin"] == reg.ORIGIN_LOCAL
    assert headers["x-snapshot-generated-at"]
    assert headers["x-snapshot-stale"] == "false"
    assert payload["path"] in _doc_paths(json.loads(body))
    # the same running serve still says `main` for the unkeyed read
    assert unkeyed[1]["x-snapshot-ref"] == reg.DEFAULT_REF


# ==========================================================================
# T031 — publication and indexing REFUSE, through the EXISTING check (FR-012)
# ==========================================================================

def test_publication_and_indexing_of_a_session_snapshot_refuse(scratch_repo,
                                                               tmp_path):
    """FR-012 is "exercise it, prove it", not "build it": `assert_publishable`
    already refuses any non-`main` ref (plan Constraint 12), so a session snapshot
    cannot reach a data source or a published index."""
    registry, _ = _registry_with_main(scratch_repo, tmp_path)
    _create(scratch_repo, registry)

    with pytest.raises(reg.PublicationRefused) as refusal:
        reg.assert_publishable(REPO, DRAFT)
    assert DRAFT in str(refusal.value)
    assert reg.is_publishable_ref(DRAFT) is False

    with pytest.raises(reg.PublicationRefused):
        registry.index_document(published=True)          # one bad row refuses all
    with pytest.raises(reg.PublicationRefused):
        reg.build_index(registry.entries())              # the lane's own writer

    # the SERVING index still advertises it — that IS the roster FR-014 validates
    # a session key against; publication is the refused direction, not visibility
    assert (REPO, DRAFT) in _index_keys(registry.index_document())

    # and no second publication check was introduced for sessions
    assert not [n for n in dir(bs) if "publish" in n.lower()]


# ==========================================================================
# T032 / T035 — the keyed `/source` serves the WORKTREE, confined, no fallback
# ==========================================================================

def test_the_keyed_source_returns_the_worktree_bytes_and_never_falls_back(
        scratch_repo, tmp_path):
    """FR-013: reads inside a session go through the SAME read-only pass-through,
    bound to the session worktree and confined to its root. A path that escapes
    refuses — it does NOT quietly serve the `main` copy, which would be the
    silent-wrong-data failure the whole seam exists to prevent."""
    registry, _ = _registry_with_main(scratch_repo, tmp_path)
    payload = _create(scratch_repo, registry)
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    expected = (worktree / payload["path"]).read_bytes()

    # a file that exists ONLY in the served checkout: if a session read ever fell
    # back to `main`, this is what it would return
    (scratch_repo.root / "main-only.md").write_text("main only\n", encoding="utf-8")
    main_path = _main_snapshot_file(scratch_repo, tmp_path / "served.json")
    key = f"{REPO}@{DRAFT}"

    with _serving(scratch_repo, main_path) as (host, port, _httpd):
        keyed = _get(host, port, f"/source/{key}/{payload['path']}")
        encoded = _get(host, port, "/source/"
                       + urllib.parse.quote(key, safe="") + f"/{payload['path']}")
        escaped = _get(host, port,
                       f"/source/{key}/../../../{REPO}/main-only.md")
        session_doc_unkeyed = _get(host, port, f"/source/{payload['path']}")
        plain = _get(host, port, "/source/ideation/staging/demo-topic/README.md")
        main_only = _get(host, port, "/source/main-only.md")

    assert keyed[0] == 200 and keyed[2] == expected
    assert keyed[1]["x-snapshot-ref"] == DRAFT           # the response says which ref
    assert encoded[0] == 200 and encoded[2] == expected  # both spellings of the key

    assert escaped[0] == 404
    assert b"main only" not in escaped[2]               # NO fallback to `main`

    # outside the session the pass-through is UNCHANGED: it reads the served
    # checkout, where the session's document does not exist at all
    assert session_doc_unkeyed[0] == 404
    assert plain[0] == 200
    assert plain[2] == (scratch_repo.root / "ideation" / "staging" / TOPIC
                        / "README.md").read_bytes()
    assert main_only[0] == 200 and main_only[2] == b"main only\n"


def test_the_session_source_read_is_the_existing_confinement_mechanism():
    """T035: the confinement is `registry.resolve_source` + `resolve_within`, not
    a new check bolted onto the session path. Pinned on the route's own source so
    a later "simplification" cannot re-implement containment beside it."""
    import inspect

    source = inspect.getsource(serve_mod.DashboardHandler._serve_source)
    assert "self.source.registry.resolve_source(" in source
    assert inspect.getsource(reg.SnapshotRegistry.resolve_source).count(
        "resolve_within(") == 1


# ==========================================================================
# T033b — the process boundary: bootstrap, JOIN, and the two half-signals
# ==========================================================================

def test_a_fresh_process_re_registers_the_live_session_and_a_write_joins_it(
        scratch_repo, tmp_path):
    """FR-008's bootstrap. A restart is a real event: `SnapshotRegistry._entries`
    is an in-process dict, so without re-derivation the next write would open a
    SECOND session on the same tile and the resume-or-new prompt would re-fire
    mid-session. Both are asserted by their absence: one branch, one worktree, one
    more commit, `joined is True`."""
    opening = _create(scratch_repo, _registry_with_main(scratch_repo, tmp_path,
                                                        name="a.json")[0])

    fresh, _ = _registry_with_main(scratch_repo, tmp_path, name="b.json")
    assert bs.is_live(fresh, REPO, DRAFT) is False        # a new process knows nothing

    report = bs.bootstrap_sessions(fresh, repository=REPO,
                                   checkout_root=scratch_repo.root)
    assert [e.ref for e in report.live] == [DRAFT]
    assert report.stale == ()
    assert report.errors == ()
    assert bs.is_live(fresh, REPO, DRAFT) is True
    assert fresh.get(REPO, DRAFT).source_root == \
        bs.worktree_path(scratch_repo.root, DRAFT)
    assert fresh.active.ref == reg.DEFAULT_REF            # FR-014a survives it too

    after = _create(scratch_repo, fresh, _scoped(title="After The Restart"))
    assert after["joined"] is True
    assert after["ref"] == opening["ref"] == DRAFT

    git = sg.SessionGit(scratch_repo.root)
    assert git.commits_ahead("main", DRAFT) == 2
    assert git.local_ordinals("draft/") == (DRAFT,)      # no second branch
    assert [p.name for p in sorted((scratch_repo.container / "sessions").iterdir())] \
        == [bs.flatten_branch(DRAFT)]                    # no second worktree


def test_the_bootstrap_is_the_liveness_a_fresh_propose_refusal_will_read(
        scratch_repo, tmp_path):
    """FR-023's `propose` refusal is T054 (Phase 6) and is deliberately NOT wired
    yet — this test does not pretend it is. What it pins is the thing T054 will
    consume: after a process boundary the session is LIVE through the ONE signal
    FR-008 names (`is_live`, a registry lookup), keyed on the tile's own derived
    branch. So the refusal T054 adds cannot be defeated by a restart, which is
    exactly the D15 hazard ("`propose` proceeds over unmerged drafts")."""
    _create(scratch_repo, _registry_with_main(scratch_repo, tmp_path,
                                              name="a.json")[0])

    fresh, _ = _registry_with_main(scratch_repo, tmp_path, name="b.json")
    bs.bootstrap_sessions(fresh, repository=REPO, checkout_root=scratch_repo.root)

    tile = bs.Tile(bs.STAGED_TOPIC, TOPIC)
    assert bs.is_live(fresh, REPO, bs.session_branch(tile.scope_kind,
                                                     tile.scope_id)) is True


def test_a_worktree_whose_branch_is_gone_is_not_re_registered_and_reports_stale(
        scratch_repo, tmp_path):
    """FR-008/D10: the worktree and the branch are a JOINT signal. A directory
    with no branch is crash residue — NOT a live session — and it is surfaced for
    the human-invoked cleanup rather than adopted, resurrected, or overwritten."""
    _create(scratch_repo, _registry_with_main(scratch_repo, tmp_path,
                                              name="a.json")[0])
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    # delete the ref while the worktree keeps it checked out (`git branch -D`
    # refuses that; `update-ref -d` is how the residue actually appears)
    scratch_repo.git("update-ref", "-d", f"refs/heads/{DRAFT}")

    fresh, _ = _registry_with_main(scratch_repo, tmp_path, name="b.json")
    report = bs.bootstrap_sessions(fresh, repository=REPO,
                                   checkout_root=scratch_repo.root)

    assert report.live == ()
    assert fresh.get(REPO, DRAFT) is None
    assert bs.is_live(fresh, REPO, DRAFT) is False
    assert [s.kind for s in report.stale] == [bs.WORKTREE_WITHOUT_BRANCH]
    assert report.stale[0].branch == DRAFT
    assert Path(report.stale[0].path) == worktree
    assert DRAFT in report.summary()
    assert worktree.is_dir()          # nothing was cleaned up automatically


def test_a_branch_with_no_worktree_is_not_live_and_reports_stale(scratch_repo,
                                                                 tmp_path):
    """The abandoned-branch shape (FR-022 deletes nothing at abandon time). The
    branch survives its session, so it is NOT live: the bootstrap must not
    resurrect it, and must not delete it either — FR-025 offers the human resume
    or new, and FR-028's cleanup is human-invoked."""
    _create(scratch_repo, _registry_with_main(scratch_repo, tmp_path,
                                              name="a.json")[0])
    git = sg.SessionGit(scratch_repo.root)
    git.worktree_remove(bs.worktree_path(scratch_repo.root, DRAFT))

    fresh, _ = _registry_with_main(scratch_repo, tmp_path, name="b.json")
    report = bs.bootstrap_sessions(fresh, repository=REPO,
                                   checkout_root=scratch_repo.root)

    assert report.live == ()
    assert bs.is_live(fresh, REPO, DRAFT) is False
    assert [s.kind for s in report.stale] == [bs.BRANCH_WITHOUT_WORKTREE]
    assert report.stale[0].branch == DRAFT
    assert git.branch_exists(DRAFT) is True              # nothing was deleted


def test_the_bootstrap_degrades_on_a_tree_that_is_not_a_git_checkout(tmp_path):
    """A serve is built against all sorts of trees. A bootstrap that raised there
    would take the whole dashboard down over an absent session, so it reports and
    registers nothing."""
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    registry = reg.SnapshotRegistry()

    report = bs.bootstrap_sessions(registry, repository=REPO, checkout_root=plain)

    assert report.live == () and report.stale == ()
    assert len(registry) == 0


def test_a_new_serve_process_re_registers_the_session_at_startup(scratch_repo,
                                                                 tmp_path):
    """quickstart step 3, which is deliberately a NEW serve process after the CLI
    opened the session: the fresh process must re-derive the
    `(repository, draft/demo-topic)` entry before it can answer anything. If the
    session ref 404s here, the bootstrap is missing — that is the bug, not a stale
    session."""
    payload = _create(scratch_repo, _registry_with_main(scratch_repo, tmp_path,
                                                        name="a.json")[0])
    main_path = _main_snapshot_file(scratch_repo, tmp_path / "served.json")

    with _serving(scratch_repo, main_path) as (host, port, _httpd):
        status, headers, body = _get(host, port, f"{serve_mod.SNAPSHOT_ROUTE}"
                                                 f"?repository={REPO}&ref={DRAFT}")
        _i, _ih, ibody = _get(host, port, serve_mod.SNAPSHOT_INDEX_ROUTE)

    assert status == 200
    assert headers["x-snapshot-ref"] == DRAFT
    assert payload["path"] in _doc_paths(json.loads(body))
    index = json.loads(ibody)
    assert (REPO, DRAFT) in _index_keys(index)
    assert index["active"] == {"repository": REPO, "ref": reg.DEFAULT_REF}


def test_every_cli_verb_bootstraps_its_own_process_registry(scratch_repo,
                                                            tmp_path, capsys):
    """T033a's second seam: every CLI-parity verb is a FRESH PROCESS, and
    `cli._session_registry` is the ONE place a CLI verb obtains a registry."""
    _create(scratch_repo, _registry_with_main(scratch_repo, tmp_path)[0])
    capsys.readouterr()

    registry = cli_mod._session_registry(scratch_repo.root, REPO)

    assert bs.is_live(registry, REPO, DRAFT) is True
    assert registry.get(REPO, DRAFT).source_root == \
        bs.worktree_path(scratch_repo.root, DRAFT)


# ==========================================================================
# T036 — a session key is roster-validated BEFORE URL composition (FR-014)
# ==========================================================================

_NODE_HARNESS = """
import * as m from './repo-selector-model.mjs';
import { readFileSync } from 'node:fs';
const index = JSON.parse(readFileSync(process.argv[2], 'utf8'));
// exactly the shell's restore path (app.js): stored text -> roster validation ->
// active option. A session key takes it unchanged; there is no session branch.
const restore = (text) => {
  const key = m.resolveStoredKey(index, text);
  const option = m.resolveActive(index, key);
  return { key, activeId: option ? option.id : null };
};
const active = m.resolveActive(index, null);
console.log(JSON.stringify({
  roster: m.buildRoster(index).map((o) => o.id),
  sessionRestore: restore('openxFactory@draft/demo-topic'),
  goneSessionRestore: restore('openxFactory@draft/gone-topic'),
  hostileSessionRestore: restore('openxFactory@draft/../../etc/passwd'),
  defaultActiveId: active ? active.id : null,
  hasSessionKey: m.hasKey(index, 'openxFactory@draft/demo-topic'),
  safeSegments: ['draft/demo-topic', 'cluster/cl-x', 'possible/pos-1',
                 'draft/../etc', 'draft/a b'].map((s) => m.safeKeySegment(s)),
}));
"""


def _run_model(index, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "repo-selector-model.mjs")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    data = tmp_path / "index.json"
    data.write_text(json.dumps(index), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(data)],
                          capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_a_session_key_is_validated_against_the_roster_before_url_composition(
        scratch_repo, tmp_path):
    """FR-014, G11: a session ref entering the UI's key space is validated on the
    SAME path PR #48 added for the selector's stored key — membership in the index
    roster plus the character allow-list — and a session introduces no bypass. The
    roster here is the real serving index, session row included."""
    registry, _ = _registry_with_main(scratch_repo, tmp_path)
    _create(scratch_repo, registry)

    r = _run_model(registry.index_document(), tmp_path)

    assert r["roster"] == [f"{REPO}@{DRAFT}", f"{REPO}@main"]
    # a session key the roster advertises: honoured, and rebuilt through the
    # allow-list rather than passed through from storage
    assert r["sessionRestore"]["key"] == {"repository": REPO, "ref": DRAFT}
    assert r["sessionRestore"]["activeId"] == f"{REPO}@{DRAFT}"
    assert r["hasSessionKey"] is True
    # a session that has ENDED (its entry is gone) stops being requested — the
    # same fix #48 made for a vanished repository
    assert r["goneSessionRestore"]["key"] is None
    assert r["goneSessionRestore"]["activeId"] == f"{REPO}@main"
    # and a session-shaped ref carrying `..` never composes a URL at all
    assert r["hostileSessionRestore"]["key"] is None
    assert r["hostileSessionRestore"]["activeId"] == f"{REPO}@main"
    # FR-014a once more, from the browser's side: with nothing stored, a live
    # session in the roster does not change what the page opens on
    assert r["defaultActiveId"] == f"{REPO}@main"
    assert r["safeSegments"] == ["draft/demo-topic", "cluster/cl-x",
                                 "possible/pos-1", None, None]


def test_no_bundle_file_composes_a_keyed_url_outside_the_validated_builders():
    """"Never a bypass" as a grep, not a promise: the (repository, ref) pair — a
    session ref included — reaches a URL in exactly TWO places, both in `app.js`,
    and both gated on `safeKey`. A session-specific request builder anywhere else
    would be the bypass FR-014 forbids.

    `repo-selector-model.js` is exempt because it IS the validation path (`keyId`
    composes the DOM/wire form there, and `safeKey` is what makes it request-safe);
    everything else in the HAND-WRITTEN bundle receives an already-validated base.
    `web/vendor/` is out of scope for the same reason `test_renderer.py` excludes
    it: a minified third-party asset's string literals are not this project's URL
    composition."""
    app = (WEB / "app.js").read_text(encoding="utf-8")
    assert "resolveActive(index, resolveStoredKey(index, storedKey()))" in app
    for builder in ("function snapshotUrl(active) {", "function sourceBaseFor(active) {"):
        body = app.split(builder, 1)[1].split("\n}", 1)[0]
        assert "safeKey(active)" in body, f"{builder} does not gate on safeKey"

    exempt = {"app.js", MODEL_JS.name}
    for path in sorted(WEB.rglob("*.js")):
        if path.name in exempt or "vendor" in path.relative_to(WEB).parts:
            continue
        text = path.read_text(encoding="utf-8")
        assert "ref=" not in text, f"{path.name} composes a ref query outside app.js"
        assert '"@"' not in text, f"{path.name} composes a repository@ref key"


# ==========================================================================
# T081 — THE HOSTED PLANE HAS NONE OF THIS (FR-048; chg 7.1, 8.4)
#
# FR-048 is a NEGATIVE requirement, and the only honest way to test one is to
# reach for the capability from the hosted side and be refused. Three assertions
# carry it:
#
#   * the hosted capability PROBE advertises no session — the same fail-closed
#     verdict `gate` and `notebook` already make, stated separately so a reader
#     of `/capabilities` never has to infer it from the gate leg;
#   * a hosted request naming a NON-`main` ref refuses on every read route that
#     accepts a ref — the snapshot query and the keyed `/source` form — while the
#     same requests keep working on the local plane, because confining the hosted
#     plane must not confine the local one;
#   * the ARRIVAL PATH is RECORDED and not built: a hosted session becomes
#     possible by binding the intent plane's apply-lane ref through the existing
#     (repository, ref) seam, and nothing here does that.
#
# The route tests flip `handler.loopback` rather than binding 0.0.0.0 — the
# established pattern (test_repo_selector.py's off-loopback refusals) — because
# the PLANE is the bind, not the advertised capability: the refusal must hold even
# on a handler whose capability dict still says the local plane's yes.
# ==========================================================================

def _post(host, port, path, body):
    payload = json.dumps(body).encode("utf-8")
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("POST", path, body=payload,
                 headers={"Content-Type": "application/json",
                          "Content-Length": str(len(payload))})
    resp = conn.getresponse()
    raw = resp.read()
    status = resp.status
    conn.close()
    return status, (json.loads(raw) if raw else {})


def test_the_hosted_capability_probe_advertises_no_session():
    """FR-048: no session on the hosted plane, stated by the probe. The local
    plane — a loopback bind, a real checkout, a resolved human — is the ONLY plane
    that advertises one, because the session's remote-write identity is the
    engineer's own personal credential (FR-034, D22) and a hosted plane must never
    touch one."""
    local = serve_mod.compute_capabilities(
        nlm_present=True, checkout_real=True, loopback=True, actor="brett")
    assert local["actions"]["session"] is True
    for kwargs in (
        {"nlm_present": True, "checkout_real": True, "loopback": False,
         "actor": "brett"},                      # the hosted bind
        {"nlm_present": True, "checkout_real": False, "loopback": True,
         "actor": "brett"},                      # the served image's empty tree
        {"nlm_present": True, "checkout_real": True, "loopback": True},   # no actor
    ):
        caps = serve_mod.compute_capabilities(**kwargs)
        assert caps["actions"]["session"] is False, kwargs
    # the session leg is INDEPENDENT of `nlm`: a local plane with no notebook
    # still has sessions (FR-042 — a session without its notebook is complete)
    no_nlm = serve_mod.compute_capabilities(
        nlm_present=False, checkout_real=True, loopback=True, actor="brett")
    assert no_nlm["actions"]["session"] is True
    assert no_nlm["actions"]["notebook"] is False
    # and the default (a hand-built handler) is off
    assert serve_mod._DEFAULT_CAPABILITIES["actions"]["session"] is False


def test_the_hosted_ref_predicate_refuses_only_non_main_off_loopback():
    """The pure half, so the rule is one definition three routes call."""
    assert serve_mod.hosted_ref_refused(False, DRAFT) is True
    assert serve_mod.hosted_ref_refused(False, "cluster/cl-x") is True
    assert serve_mod.hosted_ref_refused(False, "main") is False
    assert serve_mod.hosted_ref_refused(False, None) is False   # means `main`
    assert serve_mod.hosted_ref_refused(False, "") is False
    # the LOCAL plane is untouched — confining the hosted plane must not confine
    # the plane the whole feature lives on
    assert serve_mod.hosted_ref_refused(True, DRAFT) is False


def test_a_hosted_request_naming_a_non_main_ref_refuses(scratch_repo, tmp_path):
    """FR-048 over real HTTP: the session ref the LOCAL plane serves (and which
    the serving index legitimately advertises, FR-014) is refused the moment the
    bind is not loopback — on the snapshot query and on the keyed `/source` form
    alike, which are the two read routes that accept a ref."""
    registry, _ = _registry_with_main(scratch_repo, tmp_path)
    payload = _create(scratch_repo, registry)
    snapshot_path = _main_snapshot_file(scratch_repo, tmp_path / "main.json")
    with _serving(scratch_repo, snapshot_path) as (host, port, httpd):
        keyed = urllib.parse.quote(f"{REPO}@{DRAFT}", safe="")
        session_query = (f"{serve_mod.SNAPSHOT_ROUTE}?repository="
                         f"{urllib.parse.quote(REPO)}&ref={urllib.parse.quote(DRAFT)}")
        source_path = f"/source/{keyed}/{payload['path']}"
        # the LOCAL plane serves both (this is Phase 3's behaviour, unchanged)
        local_snapshot, _h, _b = _get(host, port, session_query)
        local_source, _h2, _b2 = _get(host, port, source_path)
        # now the SAME handler on a hosted bind
        handler = getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)
        handler.loopback = False
        hosted_snapshot, _h3, hosted_body = _get(host, port, session_query)
        hosted_source, _h4, _b4 = _get(host, port, source_path)
        # `main` keeps working off-loopback — that IS the hosted dashboard
        hosted_main, _h5, _b5 = _get(
            host, port, f"{serve_mod.SNAPSHOT_ROUTE}?repository={urllib.parse.quote(REPO)}"
            f"&ref=main")
    assert local_snapshot == 200 and local_source == 200
    assert hosted_snapshot == 403, hosted_snapshot
    assert json.loads(hosted_body)["error"] == "session_unavailable"
    assert hosted_source == 403
    assert hosted_main == 200


def test_the_hosted_session_arrival_path_is_recorded_and_not_built():
    """FR-048's second half: the (repository, ref) seam is named as the FUTURE
    binding point, at the refusal site, and the binding is NOT built here. The
    assertion is deliberately on the refusal site's own comment — that is where
    the next reader will be standing when they ask "why can this not be hosted?"
    """
    src = (REPO_ROOT / "scripts" / "ideation_dashboard" / "serve.py").read_text(
        encoding="utf-8")
    marker = "def hosted_ref_refused("
    assert marker in src
    block = src.split(marker, 1)[1].split("\ndef ", 1)[0]
    assert "add-ideation-intent-plane" in block
    assert "apply-lane" in block
    assert "(repository, ref)" in block
    # RECORDED, not built: no apply-lane binding exists anywhere in the serve.
    # This is an ABSENCE over the whole serve (`split-opendox-two-layer-
    # product` § 2.4 made it four files), so it is asserted over the surface,
    # not just this one file — widened, never narrowed, per the standing
    # ruling for this slice.
    assert "apply_lane" not in serve_surface_source()
    # every route that accepts a ref asks the one predicate
    assert src.count("hosted_ref_refused(") >= 4   # the definition + 3 call sites
    for route in ("_serve_snapshot", "_serve_source", "_handle_refresh_action"):
        body = src.split(f"def {route}(", 1)[1].split("\n    def ", 1)[0]
        assert "hosted_ref_refused(" in body, f"{route} does not ask the predicate"


def test_the_loopback_serve_declares_the_pull_request_port(scratch_repo, tmp_path):
    """T082's half of the same decision (Phase 7 note 6): declaring a
    `PullRequestPort` on the serve and confining the hosted plane are ONE
    decision, because the port's identity is a PERSONAL credential (FR-034, D22).
    The local plane declares one — without it the workbench's save affordance
    could not fire at all — and it is built through an injectable seam, so no test
    ever reaches a real `gh`."""
    snapshot_path = _main_snapshot_file(scratch_repo, tmp_path / "main.json")
    httpd = serve_mod.build_server(WEB, snapshot_path, scratch_repo.root,
                                   repository=scratch_repo.repository,
                                   actor="tester")
    try:
        handler = getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)
        port = handler._session_pull_requests(handler)
    finally:
        httpd.server_close()
    from ideation_dashboard import session_pr
    assert isinstance(port, session_pr.GhPullRequests)
    # the port declares exactly the three operations FR-030 permits
    for name in session_pr.PORT_OPERATIONS:
        assert callable(getattr(port, name))
    for forbidden in ("merge", "approve", "review", "enable_auto_merge",
                      "bypass_protection"):
        assert not hasattr(port, forbidden), forbidden
    # and a HOSTED handler declares none, for the same reason the probe says so
    class _Hosted(handler):
        capabilities = {"actions": {"session": False, "gate": False}}
    assert _Hosted._session_pull_requests(_Hosted) is None
    # THE PROSE THAT DESCRIBES THIS DECISION MUST SAY IT (PR #49 second-review tail
    # B9). `run_gate_action`'s docstring is the primary in-code account of the D22
    # confinement, and it went on asserting "`serve.py` declares none yet — Phase
    # 9's T082/T083 own that decision" for as long as this test has been passing:
    # it stated the opposite of the build, on exactly the question a reader comes
    # to it with. Pinned here rather than in a prose-only test, because the
    # sentence and the behaviour are one claim.
    from ideation_dashboard import gate_routes as gr
    doc = gr.run_gate_action.__doc__
    assert "declares none yet" not in doc
    assert "_session_pull_requests" in doc
    assert "session: false" in doc, "the docstring must name the real confinement"
