"""The (repository, ref) snapshot registry, the data-source seam, and the
per-repository publication index (openxFactory change
`add-dashboard-repo-selector`, tasks 2.1-2.4, 3.1, 3.3-3.4 and verification 5.1-5.3).

What is pinned here:

  * KEY RESOLUTION — a ref-less request resolves to `main`, and two refs of one
    repository serve independently with no cross-contamination (task 2.1/D4);
  * PER-ENTRY CONFINEMENT — a `/source` read through one entry cannot escape that
    entry's root, and an entry with no declared root serves nothing at all
    (task 2.2, fail-closed);
  * PUBLICATION REFUSAL — a non-`main` snapshot refuses publication and refuses
    entry into a published index (task 2.3);
  * THE INDEX — built from the registry, parsed back read-side, and conformant to
    the PINNED openxFactory `ideation-dashboard-snapshot-index` schema (the same
    delegation the snapshot uses: the contract is never restated here);
  * RUNTIME FETCH + FALLBACK — a reachable source renders fetched data; an
    unreachable one renders the baked snapshot WITH a stale reason; a snapshot
    published after the image was built is reflected with no rebuild
    (tasks 3.3/3.4);
  * THE TWO REFRESH BINDINGS — `refetch` writes nothing and re-pulls; `regenerate`
    re-runs the generator and rewrites only the derived snapshot (task 3.6);
  * THE PASSIVE HINT — the served index advertises what the source has without
    pulling it (Brett's 2026-07-26 ruling on open question 2).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, FakeGit, find_openxfactory_validator

from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

VALIDATOR = find_openxfactory_validator()
needs_validator = pytest.mark.skipif(
    VALIDATOR is None, reason="pinned openxFactory validator not reachable")


def _snapshot(repository="fixture-repo", revision=PINNED_REVISION):
    return generate_snapshot(BASE_REPO, repository, source_revision=revision,
                             git=FakeGit(head=revision))


def _write_snapshot(path: Path, repository="fixture-repo", revision=PINNED_REVISION):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_snapshot(repository, revision)), encoding="utf-8")
    return path


def _published_tree(root: Path, repos=("alpha", "beta"), index_name="index.json"):
    """A published data source: one snapshot per repository plus the index."""
    entries = []
    for i, repository in enumerate(repos):
        revision = f"{i + 1}" * 40
        path = _write_snapshot(root / f"{repository}-snapshot.json", repository, revision)
        entry = reg.entry_from_snapshot_file(path, repository=repository)
        entry.location = path.name
        entries.append(entry)
    (root / index_name).write_text(
        json.dumps(reg.build_index(entries, published=True)), encoding="utf-8")
    return entries


# ---------------------------------------------------------------------------
# keys: a ref-less request means `main` (task 2.1 / design D4)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ref", [None, "", "   ", "main"])
def test_refless_request_resolves_to_main(ref):
    assert reg.snapshot_key("openxFactory", ref) == ("openxFactory", "main")
    assert reg.normalize_ref(ref) == "main"


def test_key_id_round_trips_including_slashed_refs():
    assert reg.key_id("openxFactory") == "openxFactory@main"
    assert reg.parse_key_id("openxFactory@feat/wheel") == ("openxFactory", "feat/wheel")
    assert reg.parse_key_id("openxFactory") is None
    assert reg.parse_key_id("@main") is None


def test_registry_lookup_defaults_the_ref(tmp_path):
    registry = reg.SnapshotRegistry()
    path = _write_snapshot(tmp_path / "a.json", "alpha")
    registry.register(reg.entry_from_snapshot_file(path, repository="alpha"))
    assert registry.get("alpha") is registry.get("alpha", "main")
    assert registry.get("alpha", "feat/x") is None
    # an existing ref-less consumer keeps working: no repository named at all
    # resolves to the ACTIVE entry, which is what /snapshot.json has always meant
    assert registry.resolve(None) is registry.get("alpha")


def test_two_refs_of_one_repository_serve_independently(tmp_path):
    registry = reg.SnapshotRegistry()
    main_root = tmp_path / "main-root"
    branch_root = tmp_path / "branch-root"
    for root in (main_root, branch_root):
        (root / "docs").mkdir(parents=True)
    (main_root / "docs" / "a.md").write_text("main copy\n", encoding="utf-8")
    (branch_root / "docs" / "a.md").write_text("branch copy\n", encoding="utf-8")
    registry.register(reg.SnapshotEntry(
        repository="alpha", ref="main", source_root=main_root,
        payload=b'{"repository": "alpha", "ref": "main"}', source_revision="a" * 40))
    registry.register(reg.SnapshotEntry(
        repository="alpha", ref="feat/x", source_root=branch_root,
        payload=b'{"repository": "alpha", "ref": "feat/x"}', source_revision="b" * 40))

    assert registry.get("alpha").source_revision == "a" * 40
    assert registry.get("alpha", "feat/x").source_revision == "b" * 40
    assert registry.resolve_source("alpha", "main", "docs/a.md").read_text() == "main copy\n"
    assert registry.resolve_source("alpha", "feat/x", "docs/a.md").read_text() == "branch copy\n"


# ---------------------------------------------------------------------------
# per-entry source confinement (task 2.2)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tail", [
    "../../../../etc/passwd",
    "%2e%2e/%2e%2e/etc/passwd",
    "/etc/passwd",
    "docs/../../outside.md",
    "does/not/exist.md",
    "",
])
def test_confinement_refuses_every_escape(tmp_path, tail):
    registry = reg.SnapshotRegistry()
    root = tmp_path / "root"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "a.md").write_text("inside\n", encoding="utf-8")
    (tmp_path / "outside.md").write_text("secret\n", encoding="utf-8")
    registry.register(reg.SnapshotEntry(repository="alpha", source_root=root,
                                        payload=b"{}"))
    assert registry.resolve_source("alpha", None, tail) is None


def test_entry_without_a_declared_root_serves_nothing(tmp_path):
    """Fail-closed: an entry with no root NEVER falls back to another entry's
    checkout, even when that other entry could serve the path."""
    registry = reg.SnapshotRegistry()
    root = tmp_path / "root"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "a.md").write_text("inside\n", encoding="utf-8")
    registry.register(reg.SnapshotEntry(repository="alpha", source_root=root, payload=b"{}"))
    registry.register(reg.SnapshotEntry(repository="beta", payload=b"{}"))
    assert registry.resolve_source("alpha", None, "docs/a.md") is not None
    assert registry.resolve_source("beta", None, "docs/a.md") is None
    assert registry.resolve_source("gamma", None, "docs/a.md") is None  # unknown pair


# ---------------------------------------------------------------------------
# publication refusal (task 2.3)
# ---------------------------------------------------------------------------

def test_non_main_snapshot_refuses_publication():
    reg.assert_publishable("alpha", None)      # main by default — legal
    reg.assert_publishable("alpha", "main")
    with pytest.raises(reg.PublicationRefused):
        reg.assert_publishable("alpha", "feat/x")


def test_published_index_refuses_a_non_main_entry(tmp_path):
    entries = [
        reg.SnapshotEntry(repository="alpha", ref="main", source_revision="a" * 40,
                          location="alpha-snapshot.json"),
        reg.SnapshotEntry(repository="alpha", ref="feat/x", source_revision="b" * 40,
                          location="alpha-feat-snapshot.json"),
    ]
    with pytest.raises(reg.PublicationRefused):
        reg.build_index(entries, published=True)
    # the SERVED plane's own (local) index may hold a session-local entry — what is
    # refused is PUBLICATION, i.e. making it shared state
    local = reg.build_index(entries, published=False)
    assert {(e["repository"], e["ref"]) for e in local["entries"]} == {
        ("alpha", "main"), ("alpha", "feat/x")}


# ---------------------------------------------------------------------------
# the index: build, parse, and PINNED-schema conformance
# ---------------------------------------------------------------------------

def test_index_locates_snapshots_and_carries_no_projection_data(tmp_path):
    entries = _published_tree(tmp_path)
    document = reg.build_index(entries, published=True)
    assert document["kind"] == "ideation-dashboard-snapshot-index"
    assert document["schema_version"] == 1
    assert [e["repository"] for e in document["entries"]] == ["alpha", "beta"]
    for entry in document["entries"]:
        assert entry["ref"] == "main"
        assert entry["snapshot"].endswith("-snapshot.json")
        assert entry["source_revision"]
        for forbidden in ("documents", "clusters", "possibles", "staged_topics",
                          "changes", "keyword_index"):
            assert forbidden not in entry
    for forbidden in ("documents", "clusters", "possibles", "keyword_index"):
        assert forbidden not in document


def test_parse_index_is_tolerant_and_defaults_the_ref():
    entries, aggregates = reg.parse_index({
        "schema_version": 1, "kind": "ideation-dashboard-snapshot-index",
        "entries": [
            {"repository": "alpha", "snapshot": "alpha.json", "source_revision": "a"},
            {"repository": "beta", "ref": "main", "snapshot": "beta.json"},
            {"snapshot": "orphan.json"},            # no repository -> dropped
            {"repository": "gamma"},                 # no location -> dropped
            "not-a-mapping",
        ],
        "aggregates": [
            {"id": "xFactory", "members": [{"repository": "alpha"},
                                           {"repository": "beta", "ref": "main"}]},
            {"id": "empty"},                        # no members -> dropped
        ],
        "unknown_future_field": {"ignored": True},
    })
    assert [(e["repository"], e["ref"]) for e in entries] == [("alpha", "main"), ("beta", "main")]
    assert len(aggregates) == 1
    assert aggregates[0].members == [("alpha", "main"), ("beta", "main")]


@needs_validator
def test_built_index_conforms_to_the_pinned_openxfactory_schema(tmp_path):
    """Delegated conformance: the pinned validator owns the index contract, so a
    lane-written index is checked by the SAME validator the snapshot goes
    through — including the uniqueness and locator-not-projection rules."""
    entries = _published_tree(tmp_path)
    document = reg.build_index(entries, published=True,
                               aggregates=[reg.Aggregate(id="xFactory",
                                                         members=[e.key for e in entries])])
    path = tmp_path / "index-for-validation.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(path), "--strict"],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@needs_validator
def test_pinned_validator_refuses_a_duplicate_pair_and_projection_data(tmp_path):
    duplicate = {
        "schema_version": 1, "kind": "ideation-dashboard-snapshot-index",
        "entries": [
            {"repository": "alpha", "ref": "main", "snapshot": "a.json", "source_revision": "a" * 40},
            {"repository": "alpha", "ref": "main", "snapshot": "b.json", "source_revision": "b" * 40},
        ],
    }
    projection = {
        "schema_version": 1, "kind": "ideation-dashboard-snapshot-index",
        "entries": [
            {"repository": "alpha", "ref": "main", "snapshot": "a.json",
             "source_revision": "a" * 40, "clusters": [{"id": "c1"}]},
        ],
    }
    for name, doc, code in (("duplicate.json", duplicate, "snapshot-index-duplicate-repo-ref"),
                            ("projection.json", projection, "snapshot-index-carries-projection-data")):
        path = tmp_path / name
        path.write_text(json.dumps(doc), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                              capture_output=True, text=True)
        assert proc.returncode != 0, f"{name} should be refused"
        assert code in proc.stdout + proc.stderr


# ---------------------------------------------------------------------------
# runtime fetch, the baked fallback, and staleness (tasks 3.3/3.4)
# ---------------------------------------------------------------------------

def test_reachable_source_renders_fetched_data_not_the_baked_snapshot(tmp_path):
    published = tmp_path / "published"
    published.mkdir()
    _published_tree(published, repos=("alpha", "beta"))
    baked = _write_snapshot(tmp_path / "baked" / "snapshot.json", "alpha", "0" * 40)

    source = reg.SnapshotSource(
        baked_snapshot=baked, repository="alpha",
        data_source=reg.DirectoryDataSource(published))
    source.bootstrap()

    active = source.registry.active
    assert active.repository == "alpha"
    assert active.origin == reg.ORIGIN_FETCHED
    assert active.stale is False
    assert active.source_revision == "1" * 40      # the PUBLISHED revision, not the baked one
    # every published repository is selectable, with no application change
    assert [e.repository for e in source.registry.entries()] == ["alpha", "beta"]


def test_unreachable_source_falls_back_to_the_baked_snapshot_loudly(tmp_path):
    baked = _write_snapshot(tmp_path / "baked" / "snapshot.json", "alpha", "0" * 40)
    source = reg.SnapshotSource(
        baked_snapshot=baked, repository="alpha",
        data_source=reg.DirectoryDataSource(tmp_path / "nowhere"))
    source.bootstrap()

    active = source.registry.active
    assert active.origin == reg.ORIGIN_BAKED
    assert active.stale is True
    assert active.stale_reason and "unreachable" in active.stale_reason
    assert active.freshness()["generated_at"] is not None  # the banner names it
    assert source.errors, "the failure is recorded, never silent"


def test_no_declared_source_is_todays_single_snapshot_plane(tmp_path):
    """Graceful degradation: no data source, no index — one local entry, not
    stale, and the local regenerate binding."""
    baked = _write_snapshot(tmp_path / "snapshot.json", "alpha")
    source = reg.SnapshotSource(baked_snapshot=baked, repository="alpha",
                               checkout_root=BASE_REPO)
    source.bootstrap()
    active = source.registry.active
    assert len(source.registry) == 1
    assert (active.origin, active.stale) == (reg.ORIGIN_LOCAL, False)
    assert source.refresh_binding == reg.BINDING_REGENERATE


def test_a_snapshot_published_after_the_image_was_built_needs_no_rebuild(tmp_path):
    """The motivating incident, mechanised: the image's baked snapshot is old,
    the source publishes a newer one, and a refresh — not a rebake — shows it."""
    published = tmp_path / "published"
    published.mkdir()
    _published_tree(published, repos=("alpha",))
    baked = _write_snapshot(tmp_path / "baked.json", "alpha", "0" * 40)
    source = reg.SnapshotSource(baked_snapshot=baked, repository="alpha",
                               data_source=reg.DirectoryDataSource(published))
    source.bootstrap()
    assert source.registry.active.source_revision == "1" * 40

    # the lane republishes with a new revision AFTER this process started
    newer = _write_snapshot(published / "alpha-snapshot.json", "alpha", "9" * 40)
    entry = reg.entry_from_snapshot_file(newer, repository="alpha")
    entry.location = newer.name
    (published / "index.json").write_text(
        json.dumps(reg.build_index([entry], published=True)), encoding="utf-8")

    result = source.refresh()
    assert result["binding"] == reg.BINDING_REFETCH
    assert source.registry.active.source_revision == "9" * 40
    assert result["source_revision"] == "9" * 40


def test_an_unfetchable_entry_is_reported_unavailable_without_breaking_the_view(tmp_path):
    published = tmp_path / "published"
    published.mkdir()
    entries = _published_tree(published, repos=("alpha", "beta"))
    (published / "beta-snapshot.json").unlink()   # indexed but not retrievable

    source = reg.SnapshotSource(baked_snapshot=None, repository="alpha",
                               data_source=reg.DirectoryDataSource(published))
    source.bootstrap()
    alpha = source.registry.get("alpha")
    beta = source.registry.get("beta")
    assert alpha.available and source.registry.active is alpha
    assert not beta.available and beta.unavailable_reason
    document = source.index_document(peek=False)
    beta_entry = next(e for e in document["entries"] if e["repository"] == "beta")
    assert beta_entry["available"] is False
    assert entries  # sanity: the tree really did carry two entries


# ---------------------------------------------------------------------------
# the two refresh bindings (task 3.6)
# ---------------------------------------------------------------------------

def test_refetch_writes_nothing_and_keeps_the_prior_view_on_failure(tmp_path):
    published = tmp_path / "published"
    published.mkdir()
    _published_tree(published, repos=("alpha",))
    source = reg.SnapshotSource(baked_snapshot=None, repository="alpha",
                               data_source=reg.DirectoryDataSource(published))
    source.bootstrap()
    before = sorted(p.name for p in published.iterdir())
    assert source.refresh()["binding"] == reg.BINDING_REFETCH
    assert sorted(p.name for p in published.iterdir()) == before  # a read, nothing written

    # the source goes away mid-session: the refresh refuses and the registry keeps
    # serving what it already had
    (published / "index.json").unlink()
    with pytest.raises(reg.DataSourceError):
        source.refresh()
    assert source.registry.active.source_revision == "1" * 40


def test_regenerate_rewrites_only_the_derived_snapshot(tmp_path):
    run_dir = tmp_path / "run"
    snapshot_path = _write_snapshot(run_dir / "snapshot.json", "fixture-repo", "0" * 40)
    sentinel = run_dir / "keep.txt"
    sentinel.write_text("untouched\n", encoding="utf-8")

    source = reg.SnapshotSource(baked_snapshot=snapshot_path, repository="fixture-repo",
                               checkout_root=BASE_REPO,
                               generator=lambda root, repository, **kw: _snapshot(
                                   repository, "7" * 40))
    source.bootstrap()
    assert source.refresh_binding == reg.BINDING_REGENERATE
    result = source.refresh()
    assert result["binding"] == reg.BINDING_REGENERATE
    assert result["source_revision"] == "7" * 40
    # the derived snapshot is the ONLY thing rewritten
    assert json.loads(snapshot_path.read_text())["generation"]["source_revision"] == "7" * 40
    assert sentinel.read_text() == "untouched\n"
    # and the registry serves it immediately — no restart
    assert source.registry.active.source_revision == "7" * 40


def test_regenerate_refuses_an_unknown_pair(tmp_path):
    snapshot_path = _write_snapshot(tmp_path / "snapshot.json", "fixture-repo")
    source = reg.SnapshotSource(baked_snapshot=snapshot_path, repository="fixture-repo",
                               checkout_root=BASE_REPO)
    source.bootstrap()
    with pytest.raises(ValueError):
        source.refresh(repository="nope", ref="main")


def test_no_binding_when_there_is_neither_a_source_nor_a_checkout(tmp_path):
    snapshot_path = _write_snapshot(tmp_path / "snapshot.json", "alpha")
    source = reg.SnapshotSource(baked_snapshot=snapshot_path, repository="alpha")
    source.bootstrap()
    assert source.refresh_binding is None
    with pytest.raises(reg.DataSourceError):
        source.refresh()


# ---------------------------------------------------------------------------
# the passive newer-data hint (Brett 2026-07-26, open question 2)
# ---------------------------------------------------------------------------

def test_index_advertises_newer_source_data_without_pulling_it(tmp_path):
    published = tmp_path / "published"
    published.mkdir()
    _published_tree(published, repos=("alpha",))
    source = reg.SnapshotSource(baked_snapshot=None, repository="alpha",
                               data_source=reg.DirectoryDataSource(published))
    source.bootstrap()
    loaded = source.registry.active.source_revision

    # the lane publishes a newer snapshot; the index moves, the loaded bytes do not
    newer = _write_snapshot(published / "alpha-snapshot.json", "alpha", "5" * 40)
    entry = reg.entry_from_snapshot_file(newer, repository="alpha")
    entry.location = newer.name
    (published / "index.json").write_text(
        json.dumps(reg.build_index([entry], published=True)), encoding="utf-8")

    source._peek_at = 0.0  # expire the peek cache rather than sleep
    document = source.index_document()
    advertised = document["entries"][0]
    assert document["newer_available"] is True
    assert advertised["latest_source_revision"] == "5" * 40
    assert advertised["source_revision"] == loaded          # the loaded bytes are untouched
    assert source.registry.active.source_revision == loaded  # no auto-pull, no auto-reload


def test_a_failed_peek_is_silent(tmp_path):
    published = tmp_path / "published"
    published.mkdir()
    _published_tree(published, repos=("alpha",))
    source = reg.SnapshotSource(baked_snapshot=None, repository="alpha",
                               data_source=reg.DirectoryDataSource(published))
    source.bootstrap()
    (published / "index.json").unlink()
    source._peek_at = 0.0
    document = source.index_document()
    assert "newer_available" not in document
    assert "latest_source_revision" not in document["entries"][0]


def test_peek_is_cached_so_polling_viewers_do_not_hammer_the_source(tmp_path):
    published = tmp_path / "published"
    published.mkdir()
    _published_tree(published, repos=("alpha",))
    reads: list[str] = []

    class Counting(reg.DirectoryDataSource):
        def read(self, relpath):
            reads.append(relpath)
            return super().read(relpath)

    source = reg.SnapshotSource(baked_snapshot=None, repository="alpha",
                               data_source=Counting(published))
    source.bootstrap()
    reads.clear()
    for _ in range(5):
        source.index_document()
    assert reads.count("index.json") == 1


# ---------------------------------------------------------------------------
# the data-source seam: directory, URL, and the RULED raw-file binding
# ---------------------------------------------------------------------------

def test_directory_source_is_confined_to_its_root(tmp_path):
    root = tmp_path / "published"
    root.mkdir()
    (root / "index.json").write_text("{}", encoding="utf-8")
    (tmp_path / "secret.json").write_text("{}", encoding="utf-8")
    source = reg.DirectoryDataSource(root)
    assert source.read("index.json") == b"{}"
    with pytest.raises(reg.DataSourceError):
        source.read("../secret.json")


def test_url_source_composes_the_ruled_raw_file_binding_and_sends_the_token(monkeypatch):
    calls = []

    class FakeResponse:
        def __init__(self, body):
            self._body = body

        def read(self, _cap=None):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def opener(request, timeout=None):
        calls.append((request.full_url, dict(request.header_items()), timeout))
        return FakeResponse(b'{"kind": "ideation-dashboard-snapshot-index"}')

    monkeypatch.setenv("XF_DASHBOARD_SOURCE_TOKEN", "read-only-secret")
    base = reg.github_raw_base_url("opensoft/xFactory")
    assert base == "https://raw.githubusercontent.com/opensoft/xFactory/main/health/ideation-dashboard/"
    source = reg.UrlDataSource(base, token_env="XF_DASHBOARD_SOURCE_TOKEN", opener=opener)
    assert source.read("index.json").startswith(b"{")
    url, headers, _timeout = calls[0]
    assert url == base + "index.json"
    # the credential travels in the request header and comes from a NAMED env var —
    # never from a repository, and never anywhere the browser can see
    assert headers.get("Authorization") == "Bearer read-only-secret"


def test_url_source_refuses_traversal_and_non_http_schemes():
    source = reg.UrlDataSource("https://example.invalid/base", opener=lambda *a, **k: None)
    with pytest.raises(reg.DataSourceError):
        source.read("../../etc/passwd")
    file_source = reg.UrlDataSource("https://example.invalid/base")
    file_source.base_url = "file:///etc/"
    with pytest.raises(reg.DataSourceError):
        file_source.read("passwd")


def test_github_raw_base_url_rejects_a_malformed_slug():
    with pytest.raises(ValueError):
        reg.github_raw_base_url("not-a-slug")


def test_data_source_from_options_picks_directory_then_url_then_none(tmp_path):
    assert isinstance(reg.data_source_from_options(directory=tmp_path), reg.DirectoryDataSource)
    assert isinstance(reg.data_source_from_options(url="https://example.invalid/x"),
                      reg.UrlDataSource)
    assert reg.data_source_from_options() is None


# ---------------------------------------------------------------------------
# aggregate composition: from the index, never a repository scan
# ---------------------------------------------------------------------------

def test_aggregate_composes_from_member_snapshots_with_namespaced_ids(tmp_path):
    registry = reg.SnapshotRegistry()
    for repository in ("alpha", "beta"):
        snapshot = {
            "schema_version": 1, "kind": "ideation-dashboard-snapshot",
            "repository": repository,
            "generation": {"source_revision": repository * 8,
                           "generated_at": "2026-07-2" + ("5" if repository == "alpha" else "6")
                                           + "T00:00:00+00:00"},
            "documents": [{"id": "doc-shared", "path": "ideation/x.md", "stage": "brainstorm"}],
            "clusters": [{"id": "cl-shared", "name": "shared",
                          "document_edges": [{"document": "doc-shared"}],
                          "tallies": {"document_links": 1}}],
            "possibles": [{"id": "pos-shared", "claiming_clusters": ["cl-shared"]}],
            "staged_topics": [], "changes": [], "keyword_index": [],
        }
        registry.register(reg.SnapshotEntry(
            repository=repository, payload=json.dumps(snapshot).encode("utf-8"),
            source_revision=repository * 8))
    registry.register_aggregate(reg.Aggregate(
        id="xFactory", members=[("alpha", "main"), ("beta", "main")]))

    composed = registry.compose_aggregate("xFactory")
    assert composed["repository"] == "xFactory"
    assert [d["id"] for d in composed["documents"]] == ["alpha::doc-shared", "beta::doc-shared"]
    assert [(d["repository"], d["ref"]) for d in composed["documents"]] == [
        ("alpha", "main"), ("beta", "main")]
    # edges follow their own repository — no cross-repository contamination
    for cluster in composed["clusters"]:
        repo = cluster["repository"]
        assert cluster["document_edges"][0]["document"] == f"{repo}::doc-shared"
    assert [p["claiming_clusters"] for p in composed["possibles"]] == [
        ["alpha::cl-shared"], ["beta::cl-shared"]]
    assert composed["generation"]["generated_at"] == "2026-07-26T00:00:00+00:00"
    assert len(composed["generation"]["composed_from"]) == 2
    assert registry.compose_aggregate("nope") is None


def test_aggregate_skips_members_with_no_available_snapshot(tmp_path):
    registry = reg.SnapshotRegistry()
    registry.register(reg.SnapshotEntry(repository="alpha", payload=json.dumps({
        "repository": "alpha", "documents": [{"id": "d1"}]}).encode("utf-8")))
    registry.register(reg.SnapshotEntry(repository="beta"))  # indexed, unfetchable
    registry.register_aggregate(reg.Aggregate(id="xFactory",
                                              members=[("alpha", "main"), ("beta", "main"),
                                                       ("gamma", "main")]))
    composed = registry.compose_aggregate("xFactory")
    assert [d["id"] for d in composed["documents"]] == ["alpha::d1"]


# ---------------------------------------------------------------------------
# a LOCAL index: the multi-repository local plane
# ---------------------------------------------------------------------------

def test_local_index_registers_every_repository_with_its_declared_root(tmp_path):
    published = tmp_path / "local"
    published.mkdir()
    _published_tree(published, repos=("alpha", "beta"))
    alpha_root = tmp_path / "checkouts" / "alpha"
    (alpha_root / "docs").mkdir(parents=True)
    (alpha_root / "docs" / "a.md").write_text("alpha doc\n", encoding="utf-8")

    source = reg.SnapshotSource(
        baked_snapshot=None, repository="alpha",
        local_index=published / "index.json",
        source_roots={"alpha": alpha_root})
    source.bootstrap()
    assert [e.repository for e in source.registry.entries()] == ["alpha", "beta"]
    assert all(e.origin == reg.ORIGIN_LOCAL for e in source.registry.entries())
    assert source.registry.resolve_source("alpha", None, "docs/a.md").read_text() == "alpha doc\n"
    # beta declared no root -> it serves no documents (fail-closed)
    assert source.registry.resolve_source("beta", None, "docs/a.md") is None
