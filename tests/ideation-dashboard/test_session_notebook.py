"""Session NOTEBOOK honesty and isolation (PR #49 adversarial review findings 11
and 13, plus the two hardening items the hermeticity stage deferred).

One shape underneath all four: **the notebook seam reported intentions instead of
outcomes, and identified notebooks by a string that did not identify them.**

  * **Finding 11 (Medium-High) — the alias was not INJECTIVE.** FR-037's transform
    strips `draft/`, lowercases, and joins repository to branch with the same
    character it substitutes for `/`, so four classes of DISTINCT valid session
    keys collapsed onto ONE alias — the cross-namespace class needing nothing but
    an unlucky staging FOLDER name. The second session then rebound the first
    session's notebook, `_sync_sources`'s drop-what-left-the-set loop deleted the
    first session's sources, and either teardown retired the notebook both were
    using. FR-037 states the opposite ("two live sessions can never share an
    alias"), so the fix is a spec delta (C11) plus a bind-time ownership refusal.
  * **Finding 13 (High) — projection and retirement reported FALSE SUCCESS.**
    `retire_session_notebook` returned "I invoked something", `_delete_sources` /
    `_sync_one` counted intent, `project_documents` hardcoded `ok=True`, and an
    ERRORED listing was collapsed into an EMPTY one ("already gone"). The failures
    were not merely mislabelled, they were INVISIBLE: no note, no hint, no FR-042
    notice, and `torn_down` claimed a notebook nobody retired.
  * **Hardening 1** — `serve._make_adapter` fell back to the REAL `nlm`-backed
    adapter whenever the notebook capability was true, and 10/10 `build_server(`
    call sites in tests pass no `adapter_factory`.
  * **Hardening 2** — `_delete_titled` deletes by TITLE MATCH, and the title was a
    caller-supplied string, so a stale or collided alias could delete a notebook
    that was not this session's on a SHARED account.

Every test here was written against the pre-fix production files and fails on
them. House rules hold: scratch repos with LOCAL BARE remotes, the REAL
`NotebookAdapter` driven by an in-memory fake `nlm` runner (never the binary —
`tests/hermeticity.py` makes it unreachable), no network, no real checkout
touched, no sleeps.
"""

from __future__ import annotations

import json

import pytest

from session_fixtures import FakeNotebookAdapter, build_scratch_repo

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import session_git as sg
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard import workbench as wb
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
RECORDS = gc.DEFAULT_RECORDS_DIR


# --------------------------------------------------------------------------
# an in-memory `nlm`, so the REAL adapter's own result handling is what is under
# test (a fake ADAPTER would prove nothing about the seams that discard results)
# --------------------------------------------------------------------------

class FakeNlm:
    """The `nlm` CLI, in memory, with per-command failure injection.

    `fail` holds command prefixes (`"notebook list"`, `"source add"`, …) that
    raise the way the real runner raises on a non-zero exit. Everything else
    behaves, so a test can fail exactly ONE operation and assert what the caller
    then reports — which is the whole subject of finding 13."""

    def __init__(self, fail: tuple[str, ...] = ()) -> None:
        self.fail = set(fail)
        self.notebooks: dict[str, dict] = {}          # id -> {id, title}
        self.sources: dict[str, list[dict]] = {}      # notebook id -> [{id,title}]
        self.calls: list[tuple] = []
        self._next = 0

    # ---- helpers a test asserts on ----
    def titles(self) -> tuple[str, ...]:
        return tuple(sorted(nb["title"] for nb in self.notebooks.values()))

    def id_of(self, title: str) -> str | None:
        return next((nid for nid, nb in self.notebooks.items()
                     if nb["title"] == title), None)

    def source_titles(self, title: str) -> tuple[str, ...]:
        nid = self.id_of(title)
        return tuple(sorted(s["title"] for s in self.sources.get(nid, [])))

    def add_notebook(self, title: str, sources: tuple[str, ...] = ()) -> str:
        nid = self._mint("nb")
        self.notebooks[nid] = {"id": nid, "title": title}
        self.sources[nid] = [{"id": self._mint("src"), "title": t} for t in sources]
        return nid

    def _mint(self, kind: str) -> str:
        self._next += 1
        return f"{kind}-{self._next}"

    # ---- the runner seam ----
    def __call__(self, *args, parse: bool = True, **kwargs):
        self.calls.append(args)
        key = " ".join(str(a) for a in args[:2])
        if key in self.fail:
            raise RuntimeError(f"exit 1: {key} failed")
        if key == "notebook create":
            nid = self.add_notebook(str(args[2]))
            return {"id": nid, "title": args[2]}
        if key == "notebook list":
            return {"notebooks": list(self.notebooks.values())}
        if key == "notebook delete":
            nid = str(args[2])
            self.notebooks.pop(nid, None)
            self.sources.pop(nid, None)
            return ""
        if key == "notebook get":
            return dict(self.notebooks.get(str(args[2]), {}))
        if key == "source list":
            return {"sources": list(self.sources.get(str(args[2]), []))}
        if key == "source add":
            nid = str(args[2])
            title = args[args.index("--title") + 1]
            self.sources.setdefault(nid, []).append(
                {"id": self._mint("src"), "title": title})
            return ""
        if key == "source delete":
            sid = str(args[2])
            for rows in self.sources.values():
                rows[:] = [s for s in rows if s["id"] != sid]
            return ""
        raise AssertionError(f"the fake nlm was asked for {args!r}")


def adapter_over(nlm: FakeNlm) -> wb.NotebookAdapter:
    """The REAL adapter, its ONE subprocess seam replaced. `available=True` is
    explicit: the guard never relaxes availability, and a test asserting failure
    HANDLING must not accidentally assert the unavailable path instead."""
    return wb.NotebookAdapter(nlm, available=True)


# --------------------------------------------------------------------------
# harness — the CLI, twice, over one scratch checkout
# --------------------------------------------------------------------------

def _cli_create(repo, *, scope_kind, scope_id, area, title, actor="brett",
                extra=()):
    return cli_mod.main([
        "gate", "create-document",
        "--repo-root", str(repo.root), "--actor", actor,
        "--title", title, "--summary", "The session's first document.",
        "--topics", "alpha", "--repository-context", REPO,
        "--area", area,
        "--scope-kind", scope_kind, "--scope-id", scope_id, *extra])


def _cli_abandon(repo, *, scope_id, actor="brett", extra=()):
    return cli_mod.main([
        "gate", "abandon-session",
        "--repo-root", str(repo.root), "--actor", actor,
        "--scope-kind", "staged-topic", "--scope-id", scope_id,
        "--reason", "the spike answered its question", *extra])


def _torn_down(out: str) -> tuple[str, ...]:
    line = next(l for l in out.splitlines() if l.strip().startswith("torn down:"))
    return tuple(part.strip() for part in
                 line.split("torn down:", 1)[1].strip().split(","))


def _live_branches(repo) -> tuple[str, ...]:
    return tuple(b for b in repo.local_branches() if b != "main")


# ==========================================================================
# FINDING 11 — the alias is injective over the valid key space, through the CLI
# ==========================================================================

# Each case is two DISTINCT tiles whose FR-037 transform is the same string, so
# pre-fix the second CLI create rebound the first tile's notebook.
_CLI_COLLISIONS = {
    # (a) a staged topic whose FOLDER NAME spells a cluster branch
    "namespace-cluster": (
        ("staged-topic", "cluster-cl-demo", "ideation/staging/cluster-cl-demo/"),
        ("cluster", "cl-demo", "ideation/clusters/cl-demo/"),
    ),
    # (a') the same, for a derived possible id
    "namespace-possible": (
        ("staged-topic", "possible-pos-derived-x",
         "ideation/staging/possible-pos-derived-x/"),
        ("possible", "pos-derived-x", "ideation/possibles/pos-derived-x/"),
    ),
}


def _collision_world(tmp_path, case):
    """A scratch checkout carrying BOTH tiles of a collision pair.

    The staging folder is what makes the staged-topic tile exist; the cluster tile
    exists because a `Topics:` keyword derives `cl-<keyword>` (`live_tile_scopes`),
    which is why the folder is seeded with the keyword the pair needs."""
    (first, second) = _CLI_COLLISIONS[case]
    keyword = second[1].removeprefix("cl-")
    return build_scratch_repo(tmp_path, topic_id=keyword,
                              extra_topics=(first[1],))


@pytest.mark.parametrize("case", sorted(_CLI_COLLISIONS))
@pytest.mark.parametrize("order", ["first-then-second", "second-then-first"])
def test_two_tiles_that_spell_one_alias_get_two_notebooks_through_the_cli(
        tmp_path, case, order, fake_cli_notebook):
    """Finding 11, BOTH directions: whichever tile opens first, the second tile's
    session gets its OWN notebook and the first tile's sources survive.

    Pre-fix the two sessions derived the identical alias, so the second create
    rebound the first's notebook — `live_aliases()` held ONE entry and the first
    tile's projected source had been deleted by the sync's drop loop."""
    repo = _collision_world(tmp_path, case)
    tiles = list(_CLI_COLLISIONS[case])
    if order == "second-then-first":
        tiles.reverse()

    for index, (kind, scope_id, area) in enumerate(tiles):
        assert _cli_create(repo, scope_kind=kind, scope_id=scope_id, area=area,
                           title=f"Tile {index}") == 0

    branches = _live_branches(repo)
    assert len(branches) == 2, branches
    aliases = {bs.notebook_alias(REPO, branch) for branch in branches}
    assert len(aliases) == 2, aliases
    # two live sessions, two notebooks, and each holds its OWN document
    assert set(fake_cli_notebook.live_aliases()) == aliases
    for alias in aliases:
        assert fake_cli_notebook.notebooks[alias].sources, alias
    projected = [sorted(path for path, _text in nb.sources)
                 for nb in fake_cli_notebook.notebooks.values()]
    assert projected[0] != projected[1], projected


@pytest.mark.parametrize("order", ["base-then-ordinal", "ordinal-then-base"])
def test_the_foo_and_foo_2_tiles_never_share_a_session_notebook(
        tmp_path, order, capsys, fake_cli_notebook):
    """The ordinal direction of the same hazard (FR-037 with G12), in both
    orders: tile `foo` continued to its `-2` ordinal and a tile literally NAMED
    `foo-2` would be one branch and therefore ONE notebook.

    A COMPANION guard rather than a repro of this stage: G12's cross-tile
    exclusion — repaired for the CLI in the phase-3 finding-7 work — is what keeps
    the two branches apart, and the alias follows the branch. It is pinned here
    because the alias is where that divergence would BITE (two tiles' unmerged
    documents in one notebook), and nothing else asserts it from the notebook
    side."""
    repo = build_scratch_repo(tmp_path, topic_id="foo", extra_topics=("foo-2",))
    tiles = [("foo", "ideation/staging/foo/"), ("foo-2", "ideation/staging/foo-2/")]
    if order == "ordinal-then-base":
        tiles.reverse()

    for scope_id, area in tiles:
        assert _cli_create(repo, scope_kind="staged-topic", scope_id=scope_id,
                           area=area, title=f"Tile {scope_id}") == 0, \
            capsys.readouterr().err

    branches = _live_branches(repo)
    assert set(branches) == {"draft/foo", "draft/foo-2"}, branches
    aliases = {bs.notebook_alias(REPO, branch) for branch in branches}
    assert len(aliases) == 2
    assert set(fake_cli_notebook.live_aliases()) == aliases


# ==========================================================================
# FINDING 8 leg (b) — a repository-key divergence is REPORTED, never claimed
# ==========================================================================

def _real_adapter_cli(monkeypatch, nlm):
    """The CLI's notebook seam, over the REAL adapter and the in-memory `nlm`.

    `fake_cli_notebook` cannot answer this question: its `retire` returns None,
    which `retire_session_notebook` takes at its word, so the seam under test —
    `_delete_titled`'s verdict on a title it cannot find — would be bypassed."""
    monkeypatch.setattr(cli_mod, "_notebook_port",
                        lambda repo_root: adapter_over(nlm))


def test_a_repository_key_divergence_orphans_the_notebook_and_says_so(
        tmp_path, capsys, monkeypatch):
    """Leg (b)'s surviving half (wave 2). `--repository MedxFactory` on the create
    inside an `openxFactory` checkout keys the session — and therefore its alias —
    on `MedxFactory`; the ending re-derives `openxFactory` from the checkout, so it
    looks for a notebook that never existed.

    Pre-fix the ending printed `torn down: worktree, registry-entry, notebook` at
    exit 0 and the real notebook survived on the shared account with that session's
    unmerged documents in it. Nothing is deleted differently now — the ending still
    completes and still never deletes a title it did not derive (hardening item 2) —
    what changed is that it no longer claims the notebook, names the orphan, and
    warns at the create that the flag must be repeated."""
    repo = build_scratch_repo(tmp_path, topic_id="demo-topic")
    nlm = FakeNlm()
    _real_adapter_cli(monkeypatch, nlm)
    orphan = bs.notebook_alias("MedxFactory", "draft/demo-topic")

    assert _cli_create(repo, scope_kind="staged-topic", scope_id="demo-topic",
                       area="ideation/staging/demo-topic/", title="First Draft",
                       extra=("--repository", "MedxFactory")) == 0
    created = capsys.readouterr()
    assert nlm.titles() == (orphan,)
    assert "--repository 'MedxFactory' is not this checkout's directory name" \
        in created.err
    assert "EVERY verb of this session must pass the same" in created.err

    assert _cli_abandon(repo, scope_id="demo-topic") == 0
    ended = capsys.readouterr()

    assert "notebook" not in _torn_down(ended.out), ended.out
    assert _torn_down(ended.out) == ("worktree", "registry-entry")
    assert "was NOT retired" in ended.err
    assert orphan in ended.err and "ORPHANED" in ended.err
    assert nlm.titles() == (orphan,)          # still there, and NOT deleted blindly
    assert not any(call[:2] == ("notebook", "delete") for call in nlm.calls)


def test_a_consistent_repository_key_still_retires_the_notebook(
        tmp_path, capsys, monkeypatch):
    """The control, and the proof the honesty fix is not a new failure mode: with
    the SAME `--repository` on both verbs the alias matches, the notebook is really
    deleted, `torn_down` claims it, and no divergence notice is printed."""
    repo = build_scratch_repo(tmp_path, topic_id="demo-topic")
    nlm = FakeNlm()
    _real_adapter_cli(monkeypatch, nlm)
    alias = bs.notebook_alias("MedxFactory", "draft/demo-topic")

    assert _cli_create(repo, scope_kind="staged-topic", scope_id="demo-topic",
                       area="ideation/staging/demo-topic/", title="First Draft",
                       extra=("--repository", "MedxFactory")) == 0
    assert nlm.titles() == (alias,)
    capsys.readouterr()

    assert _cli_abandon(repo, scope_id="demo-topic",
                        extra=("--repository", "MedxFactory")) == 0
    ended = capsys.readouterr()

    assert _torn_down(ended.out) == ("worktree", "registry-entry", "notebook")
    assert "was NOT retired" not in ended.err
    assert nlm.titles() == ()


def test_no_notice_is_printed_when_the_key_is_the_checkout_directory(
        tmp_path, capsys, monkeypatch):
    """The other control: the ordinary invocation — no flag at all — derives the
    checkout directory's name and says nothing, so the notice cannot become noise
    that a reader learns to skip."""
    repo = build_scratch_repo(tmp_path, topic_id="demo-topic")
    nlm = FakeNlm()
    _real_adapter_cli(monkeypatch, nlm)

    assert _cli_create(repo, scope_kind="staged-topic", scope_id="demo-topic",
                       area="ideation/staging/demo-topic/",
                       title="First Draft") == 0
    created = capsys.readouterr()

    assert nlm.titles() == (bs.notebook_alias(REPO, "draft/demo-topic"),)
    assert "--repository" not in created.err
    # and the explicit-but-AGREEING spelling is equally quiet
    assert _cli_abandon(repo, scope_id="demo-topic",
                        extra=("--repository", REPO)) == 0
    ended = capsys.readouterr()
    assert "--repository" not in ended.err
    assert _torn_down(ended.out) == ("worktree", "registry-entry", "notebook")


def test_a_bind_that_would_take_another_live_sessions_alias_is_refused(
        tmp_path, monkeypatch):
    """The ownership guard BEHIND the derivation (FR-037, FR-042).

    The digest makes a collision unreachable, so the guard is exercised by putting
    the lossy derivation back — `notebook_alias_stem` IS the pre-fix function, and
    the pair below is finding 11's cross-namespace class. With two live sessions
    deriving one alias the second bind must REFUSE and say so, rather than rebind
    the first session's notebook and delete its sources. That is what keeps a
    future derivation regression loud instead of destructive.

    The session still OPENS and stays usable: a notebook never blocks governed
    work (FR-042)."""
    repo = build_scratch_repo(tmp_path, topic_id="demo-topic")
    monkeypatch.setattr(bs, "notebook_alias", bs.notebook_alias_stem)
    registry = reg.SnapshotRegistry()
    first, second = "draft/cluster-cl-demo", "cluster/cl-demo"
    alias = bs.notebook_alias(REPO, first)
    assert bs.notebook_alias(REPO, second) == alias      # the pre-fix collision
    for branch in (first, second):
        registry.register(bs.session_entry(REPO, branch, repo.root / "wt"))

    assert bs.session_alias_owner(registry, alias, exclude=(REPO, second)) == \
        (REPO, first)

    notebook = FakeNotebookAdapter()
    session = bs.SessionOpen(
        repository=REPO, tile=bs.Tile(bs.CLUSTER, "cl-demo"),
        branch=second, worktree=repo.root, joined=False, entry=None,
        notebook_alias=alias, registry=registry, pending_notebook=notebook)

    session = bs.attach_session_notebook(session)

    assert session.notebook_created is False
    assert notebook.calls == []                # the first session's notebook: untouched
    assert "ALREADY OWNED" in session.notebook_notice
    assert f"{REPO}@{first}" in session.notebook_notice
    assert "never share an alias" in session.notebook_notice


def test_the_owner_scan_ignores_main_and_the_session_asking(tmp_path):
    """The guard must not refuse a session its OWN alias, and `main` is not a
    session — a scan that answered otherwise would leave every session notebookless."""
    registry = reg.SnapshotRegistry()
    branch = "draft/demo-topic"
    registry.register(bs.session_entry(REPO, branch, tmp_path / "wt"))
    registry.register(bs.session_entry(REPO, "main", tmp_path))
    alias = bs.notebook_alias(REPO, branch)

    assert bs.session_alias_owner(registry, alias) == (REPO, branch)
    assert bs.session_alias_owner(registry, alias, exclude=(REPO, branch)) is None
    assert bs.session_alias_owner(registry, bs.notebook_alias(REPO, "main")) is None


def test_a_session_that_REBINDS_an_existing_notebook_is_told_so(tmp_path):
    """The other half of finding 11, unpinned until wave 2: a REBIND is not a
    create.

    `create=False` from the projection means the account ALREADY held a notebook
    under this alias — and because the alias is key-derived, that can only be
    RESIDUE from an earlier session on this same (repository, branch). The session
    has a notebook either way, so the open succeeds; what the human must not have
    to discover in NotebookLM is that its sources came from somebody's earlier
    work. `grep -rn 'REUSED' tests/` returned nothing before this test, so the
    wave-2 critic neutered the reporting arm (`if False:`) and the whole suite
    stayed green.

    Driven through the REAL adapter over the in-memory `nlm` with the residue
    planted, because a fake adapter reports no `created` flag at all and would
    assert nothing about the seam under test."""
    repo = build_scratch_repo(tmp_path, topic_id="demo-topic")
    branch = "draft/demo-topic"
    alias = bs.notebook_alias(REPO, branch)
    nlm = FakeNlm()
    nlm.add_notebook(alias, ("a-stale-source.md",))       # residue, with content
    adapter = adapter_over(nlm)

    created, notice = bs.open_session_notebook(
        adapter, alias=alias, branch=branch, worktree=repo.root,
        repository=REPO)

    assert created is True, notice          # the session HAS a notebook (FR-042)
    assert notice is not None, "a rebind that says nothing is the defect"
    assert "REUSED" in notice
    assert alias in notice and branch in notice
    assert "residue from an earlier" in notice
    # and the control: a genuinely fresh create says nothing at all
    fresh_branch = "draft/other-topic"
    created, notice = bs.open_session_notebook(
        adapter, alias=bs.notebook_alias(REPO, fresh_branch),
        branch=fresh_branch, worktree=repo.root, repository=REPO)
    assert created is True and notice is None


# ==========================================================================
# FINDING 13 — every notebook failure degrades HONESTLY (FR-042), never as
# success
# ==========================================================================

def test_a_failing_notebook_delete_is_not_reported_as_retired():
    """(i) `nlm notebook delete` fails: the adapter says so, and the session-level
    retire must pass that verdict up instead of returning "I invoked something"."""
    nlm = FakeNlm(fail=("notebook delete",))
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    nlm.add_notebook(alias)
    adapter = adapter_over(nlm)

    result = adapter.retire(alias)

    assert result.ok is False and result.skipped is True
    assert "nlm error" in result.detail
    assert nlm.titles() == (alias,)            # it is still there
    retired, detail = bs.retire_session_notebook(
        adapter, repository=REPO, branch="draft/demo-topic")
    assert retired is False
    assert "nlm error" in detail


def test_a_failing_notebook_list_is_not_reported_as_already_gone():
    """(iii) an ERRORED listing is not an EMPTY listing: the notebook plainly
    exists, and "already gone" would be a false success over a live notebook."""
    nlm = FakeNlm(fail=("notebook list",))
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    nlm.add_notebook(alias)

    result = adapter_over(nlm).retire(alias)

    assert result.ok is False and result.skipped is True
    assert "could not determine" in result.detail
    assert "already gone" not in result.detail
    assert nlm.titles() == (alias,)


def test_a_scratch_delete_of_an_absent_notebook_is_still_a_benign_no_op():
    """The negative of the above, on the namespace where it belongs: a listing
    that SUCCEEDED and holds no match is a real answer, and the SWEEP's job is
    that an `xf-wb-*` title is gone however it got that way."""
    result = adapter_over(FakeNlm()).delete("xf-wb-something-swept")
    assert result.ok is True and result.skipped is False
    assert "already gone" in result.detail


def test_a_retire_that_finds_no_such_notebook_does_not_report_a_retirement():
    """This assertion is INVERTED from what it was, deliberately (PR #49 review
    finding 8 leg b, wave 2). It used to read "retiring an already-retired
    notebook stays a no-op" — `ok=True … (already gone)` — and that sentence is
    what made the leg-(b) divergence silent: a session opened under one repository
    key and ended under another derives a DIFFERENT alias, so the ending retired a
    title that never existed, reported `torn down: … notebook` at exit 0, and left
    the real notebook alive on the shared account holding that session's unmerged
    documents (reproduced).

    For a session RETIRE, "no notebook by this title" is therefore not success:
    the alias is derived from the session's own key, so its absence is either a
    notebook that was never created (FR-042's degraded open) or one that is
    ORPHANED — and both are things the human needs told, not hidden. The scratch
    `delete` keeps the benign no-op (test above), which is why this is a per-caller
    decision and not a change to `_delete_titled`'s whole contract."""
    nlm = FakeNlm()
    orphan = bs.notebook_alias("MedxFactory", "draft/demo-topic")
    nlm.notebooks["nb1"] = {"id": "nb1", "title": orphan}

    result = adapter_over(nlm).retire(bs.notebook_alias(REPO, "draft/demo-topic"))

    assert result.ok is False and result.skipped is True
    assert "already gone" not in result.detail
    assert "nothing was retired" in result.detail
    assert "ORPHANED" in result.detail
    assert orphan in result.detail            # the survivor is NAMED
    assert nlm.titles() == (orphan,)          # and nothing was deleted


def test_a_failing_source_add_is_not_a_successful_projection():
    """(ii) the half-failed replacement: the prior source is deleted, the new one
    fails to add, and the notebook is left EMPTY while the result claimed
    `ok=True, +1/-0 changed` — which suppressed the FR-042 notice as well."""
    nlm = FakeNlm(fail=("source add",))
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    nid = nlm.add_notebook(alias, sources=(
        wb.managed_source_title("a.md", "old"),))
    adapter = adapter_over(nlm)

    result = wb.project_documents(adapter, alias, [("a.md", "new")])

    assert result.ok is False
    assert "FAILED" in result.detail
    assert result.sources_added == 0
    assert nlm.sources[nid] == []              # the prior source really is gone
    # and the caller's honesty follows from it: the session reports NO notebook
    # and says why, instead of silently claiming one
    created, notice = bs.open_session_notebook(
        _StubCreate(result), alias=alias, branch="draft/demo-topic",
        worktree=".", repository=REPO)
    assert created is False
    assert notice is not None and "CONCURRENT TILES" in notice


def test_a_failing_source_delete_is_not_counted_as_removed():
    """`_delete_sources` incremented `removed` for every id it passed to
    `delete_source`, whatever the adapter answered."""
    nlm = FakeNlm(fail=("source delete",))
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    nlm.add_notebook(alias, sources=(wb.managed_source_title("gone.md", "old"),))

    result = wb.project_documents(adapter_over(nlm), alias, [("kept.md", "new")])

    assert result.ok is False
    assert result.sources_removed == 0
    assert "was not removed" in result.detail
    assert result.sources_added == 1           # what DID work is still reported


def test_a_failing_source_list_refuses_to_diff_against_an_unknown_state():
    """The latent member of the same family: a failed `source list` degraded to
    `[]`, so the next projection re-ADDED every source instead of diffing."""
    nlm = FakeNlm(fail=("source list",))
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    nid = nlm.add_notebook(alias, sources=(wb.managed_source_title("a.md", "x"),))

    result = wb.project_documents(adapter_over(nlm), alias, [("a.md", "x")])

    assert result.ok is False and result.skipped is True
    assert "could not be read" in result.detail
    assert len(nlm.sources[nid]) == 1          # nothing was duplicated


def test_a_failing_notebook_list_never_creates_a_duplicate_notebook():
    """`_ensure_notebook` read an unreadable listing as "absent" and would have
    created a SECOND notebook under a title the account already holds."""
    nlm = FakeNlm(fail=("notebook list",))
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    nlm.add_notebook(alias)

    result = wb.project_documents(adapter_over(nlm), alias, [("a.md", "x")])

    assert result.ok is False
    assert nlm.titles() == (alias,)
    assert not any(call[:2] == ("notebook", "create") for call in nlm.calls)


def test_an_unreadable_account_is_not_a_swept_account(tmp_path):
    """The `xf-wb-*` half of the same anti-pattern: `swept 0 orphan(s)` over a
    list that could not be read reads as a clean account."""
    result = wb.orphan_sweep(tmp_path, adapter_over(FakeNlm(fail=("notebook list",))))
    assert result.skipped is True
    assert "could not be read" in result.detail
    assert result.deleted == []


class _StubCreate:
    """An adapter whose `create_session` returns a prepared result — the seam
    `open_session_notebook` consumes, isolated from the projection."""

    def __init__(self, result):
        self.result = result

    def create_session(self, alias, documents=()):
        return self.result


# ==========================================================================
# The ENDINGS report what really happened (finding 13 through `teardown_session`)
# ==========================================================================

def _session_for(repo):
    git = sg.SessionGit(repo.root)
    registry = reg.SnapshotRegistry()
    session = bs.open_session(
        git, registry, repository=repo.repository,
        tile=bs.Tile(bs.STAGED_TOPIC, repo.topic_id),
        checkout_root=repo.root)
    return git, registry, session


def test_a_teardown_whose_retire_failed_does_not_claim_the_notebook(scratch_repo):
    """`torn_down` "lists only what was really removed" (SessionTeardown's own
    docstring). A failed retire used to land in it anyway, so the abandon response
    told the human the notebook was gone AND dropped its "no session notebook was
    retired here" caveat."""
    git, registry, session = _session_for(scratch_repo)
    nlm = FakeNlm(fail=("notebook delete",))
    nlm.add_notebook(session.notebook_alias)

    torn = bs.teardown_session(git, session, checkout_root=scratch_repo.root,
                               registry=registry, notebook=adapter_over(nlm))

    assert bs.TORN_NOTEBOOK not in torn.torn_down
    assert any("was NOT retired" in note for note in torn.notes), torn.notes
    assert any("nlm error" in note for note in torn.notes)
    assert nlm.titles() == (session.notebook_alias,)


def test_a_teardown_whose_retire_succeeded_still_claims_the_notebook(scratch_repo):
    """The negative, so the fix cannot be "never report a retire": a real deletion
    is still reported, with no note."""
    git, registry, session = _session_for(scratch_repo)
    nlm = FakeNlm()
    nlm.add_notebook(session.notebook_alias)

    torn = bs.teardown_session(git, session, checkout_root=scratch_repo.root,
                               registry=registry, notebook=adapter_over(nlm))

    assert bs.TORN_NOTEBOOK in torn.torn_down
    assert not any("notebook" in note for note in torn.notes), torn.notes
    assert nlm.titles() == ()


# ==========================================================================
# HARDENING 2 — a retire can only ever name the LIVE session's own notebook
# ==========================================================================

def test_a_retire_names_the_sessions_derived_alias_and_spares_a_title_collision(
        scratch_repo):
    """The account is SHARED, and `_delete_titled` deletes by TITLE MATCH. A
    session carrying a stale or hand-built alias must not be able to point that
    deletion at a notebook that is not its own: the alias is DERIVED from the
    session's (repository, branch) key at the moment of retirement, and the
    disagreement is reported rather than silently resolved either way."""
    import dataclasses

    git, registry, session = _session_for(scratch_repo)
    derived = bs.notebook_alias(scratch_repo.repository, session.branch)
    neighbour = bs.notebook_alias("someone-elses-repo", "draft/demo-topic")
    nlm = FakeNlm()
    nlm.add_notebook(derived)
    nlm.add_notebook(neighbour)
    tampered = dataclasses.replace(session, notebook_alias=neighbour)

    torn = bs.teardown_session(git, tampered, checkout_root=scratch_repo.root,
                               registry=registry, notebook=adapter_over(nlm))

    assert nlm.titles() == (neighbour,)        # the neighbour's notebook survives
    assert bs.TORN_NOTEBOOK in torn.torn_down  # this session's own was retired
    assert any(neighbour in note and "DERIVED" in note for note in torn.notes), \
        torn.notes


def test_the_retire_seam_takes_no_alias_argument_at_all():
    """The structural half: the target is unnameable by the caller, so no future
    call site can reintroduce the hazard by passing a string."""
    import inspect

    params = inspect.signature(bs.retire_session_notebook).parameters
    assert "alias" not in params
    assert set(params) == {"notebook", "repository", "branch"}


def test_an_adapter_without_retire_is_refused_rather_than_silently_deleting(tmp_path):
    """PR #49 second-review tail B2: the vestigial `delete` fallback is gone.

    The seam used to try `('retire', 'delete')` and the docstring said it "works
    with either" — but `NotebookAdapter.delete` is the SCRATCH operation: no
    session prefix guard, no key-derived-title guard, the `xf-wb-*` listing, and
    `missing_ok=True`. An injected adapter of the shape the contract permits, which
    exposed only `delete`, therefore returned `(True, "no notebook titled
    'xf-session-…' (already gone)")` and issued NO delete, while the session's
    notebook — holding that session's unmerged documents — survived on the shared
    account. That is the leg-(b) false success wave 2 closed on `retire`, left
    standing on the alternative.

    Proved on both sides: the delete-only adapter is refused with nothing issued,
    and the same underlying nlm's real `retire` still deletes."""
    nlm = FakeNlm()
    real = adapter_over(nlm)
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    nlm.add_notebook(alias)

    class DeleteOnly:
        """The permitted adapter shape that used to reach the fallback."""

        def delete(self, name):
            return real.delete(name)

    with pytest.raises(bs.SessionRefused) as refused:
        bs.retire_session_notebook(DeleteOnly(), repository=REPO,
                                   branch="draft/demo-topic")

    assert "exposes no `retire`" in str(refused.value)
    assert "NOT a substitute" in str(refused.value)
    assert nlm.titles() == (alias,), "nothing may be deleted by the refusal"
    assert not any(c[:2] == ("notebook", "delete") for c in nlm.calls)
    # and the real seam still retires the same notebook, so the refusal is about
    # the ADAPTER's shape and not about this alias
    retired, detail = bs.retire_session_notebook(real, repository=REPO,
                                                 branch="draft/demo-topic")
    assert retired is True, detail
    assert nlm.titles() == ()


def test_the_adapter_itself_refuses_a_session_title_no_key_could_derive(tmp_path):
    """Hardening 2's RESIDUAL, closed (wave 2). The seam above cannot be handed a
    title — but `NotebookAdapter.retire` could, by any NEW caller written directly
    against it, and its only guard was the `xf-session-` prefix. A prefix is not an
    owner: the wave-2 replay pass showed a stale pre-digest spelling
    (`xf-session-openxfactory-<topic>`, the READABLE half alone — what wave 1's
    aliases looked like) sitting on the shared account beside the live session's
    real notebook, and either title matched the prefix.

    The DERIVATION's shape is the guard a prefix cannot be: a delete may only name
    a title ending in the injective key digest, so the stale spelling and any
    hand-typed name are unnameable rather than merely unlikely. The live session's
    notebook is asserted UNTOUCHED, because the point is what survives."""
    nlm = FakeNlm()
    adapter = adapter_over(nlm)
    derived = bs.notebook_alias(REPO, "draft/demo-topic")
    stale = bs.notebook_alias_stem(REPO, "draft/demo-topic")   # the wave-1 spelling
    assert stale != derived and derived.startswith(stale)
    nlm.add_notebook(derived)
    nlm.add_notebook(stale)

    for hostile in (stale, "xf-session-anything-at-all", f"{derived}x",
                    derived[:-1], f"{stale}-kZZZZZZZZZZZZ"):
        with pytest.raises(wb.WorkbenchError) as exc:
            adapter.retire(hostile)
        assert "KEY-DERIVED" in str(exc.value)
        assert "retire_session_notebook" in str(exc.value)

    assert nlm.titles() == tuple(sorted((derived, stale)))     # nothing deleted
    # and the DERIVED alias still retires, so the guard admits exactly the
    # derivation and nothing else
    result = adapter.retire(derived)
    assert result.ok and not result.skipped, result.detail
    assert nlm.titles() == (stale,)


def test_the_key_shape_the_adapter_requires_is_the_derivations_own(tmp_path):
    """The transcription pin, the twin of the `SESSION_NOTEBOOK_PREFIX` one:
    `workbench` restates the key suffix rather than importing it (flat import
    graph), so a drift would either refuse every real ending or admit anything.
    Asserted against REAL aliases, not against the regex's source."""
    assert wb.SESSION_KEY_SEPARATOR == bs.NOTEBOOK_KEY_SEPARATOR
    assert wb.SESSION_KEY_DIGEST_CHARS == bs.NOTEBOOK_KEY_DIGEST_CHARS
    for repository, branch in ((REPO, "draft/demo-topic"),
                               (REPO, "cluster/cl-avatar-client"),
                               ("MedxFactory", "possible/pos-derived-x"),
                               (REPO, "draft/foo__bar")):
        alias = bs.notebook_alias(repository, branch)
        assert wb._require_key_derived(alias) == alias
        with pytest.raises(wb.WorkbenchError):
            wb._require_key_derived(bs.notebook_alias_stem(repository, branch))


# ==========================================================================
# HARDENING 1 — the real adapter is declared by ENTRYPOINTS, never defaulted
# ==========================================================================

def _bound_handler(httpd):
    """The BoundDashboardHandler class `build_server` stamped its declarations
    onto — `RequestHandlerClass` is the `functools.partial` that supplies the
    static directory."""
    return httpd.RequestHandlerClass.func


def _snapshot(repo, tmp_path):
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    return path


def test_a_server_built_with_no_adapter_factory_has_no_notebook_adapter(
        scratch_repo, tmp_path):
    """`build_server` used to fall back to `workbench.NotebookAdapter()`, whose
    runner is a real `nlm` subprocess, for every caller that declared none — which
    is every test call site. Absence is now the library default, and the
    capability agrees with it, so no future test can silently reach the shared
    account (FR-043)."""
    web = serve_mod.Path(serve_mod.__file__).resolve().parent / "web"
    httpd = serve_mod.build_server(web, _snapshot(scratch_repo, tmp_path),
                                   scratch_repo.root, actor="tester")
    try:
        handler = _bound_handler(httpd)
        assert handler.adapter_factory is None
        assert handler._make_adapter(handler) is None
        assert handler.capabilities["actions"]["notebook"] is False
    finally:
        httpd.server_close()


def test_an_injected_adapter_factory_is_still_the_one_the_server_uses(
        scratch_repo, tmp_path):
    """The seam is unweakened: a declared factory is used, and the capability
    follows the declaration."""
    fake = FakeNotebookAdapter()
    web = serve_mod.Path(serve_mod.__file__).resolve().parent / "web"
    httpd = serve_mod.build_server(web, _snapshot(scratch_repo, tmp_path),
                                   scratch_repo.root, actor="tester",
                                   adapter_factory=lambda: fake)
    try:
        handler = _bound_handler(httpd)
        assert handler._make_adapter(handler) is fake
        assert handler.capabilities["actions"]["notebook"] is True
    finally:
        httpd.server_close()


def test_the_serve_entrypoint_declares_the_real_adapter(monkeypatch):
    """The other half of the decision: `serve()` — what `main()` runs — opts into
    the real `nlm` adapter EXPLICITLY, so the production plane keeps its notebooks
    while the library default stays absence."""
    seen = {}

    def fake_build_server(*args, **kwargs):
        seen.update(kwargs)
        raise KeyboardInterrupt        # never start a real server in a test

    monkeypatch.setattr(serve_mod, "build_server", fake_build_server)
    with pytest.raises(KeyboardInterrupt):
        serve_mod.serve("web", "snapshot.json", ".")
    assert seen["adapter_factory"] is serve_mod.real_notebook_adapter


def test_the_generate_and_open_entrypoint_declares_the_real_adapter():
    """The CLI's local serve is the second entrypoint, and it declares the same
    factory — asserted on the source because the function generates a snapshot
    and binds a port before it gets there."""
    source = serve_mod.Path(cli_mod.__file__).read_text(encoding="utf-8")
    assert "adapter_factory=serve_mod.real_notebook_adapter" in source


def test_the_real_adapter_factory_is_the_only_place_serve_builds_one():
    """A pin on the decision itself: `workbench.NotebookAdapter(` appears in
    `serve.py` exactly once, inside `real_notebook_adapter`."""
    source = serve_mod.Path(serve_mod.__file__).read_text(encoding="utf-8")
    assert source.count("workbench.NotebookAdapter()") == 1


# ==========================================================================
# PR #49 SECOND-REVIEW FINDING 21 — the source set is bounded in COUNT and in
# WALL CLOCK, because the projection runs inside a governed write
#
# `_MAX_SESSION_SOURCE_BYTES` bounded one document; the COUNT was the corpus's own
# (176 governed documents / 1.83 MB measured on the real openxFactory checkout),
# one `nlm source add` subprocess each, sequentially, inside the `create-document`
# gate route — 176 x `NLM_TIMEOUT` = 2.2 hours of a governed write waiting on an
# external SaaS with no ceiling. D19 / plan Constraint 8 violated by arithmetic
# rather than by a bug: every individual call behaved correctly.
#
# The bounds DEFER, they do not drop: the remainder is counted, the human is told,
# and the unbounded off-request route (FR-040's `--session-ref` re-sync) completes
# it. These tests are what make the numbers a pin rather than a comment.
# ==========================================================================

class _Clock:
    """A monotonic clock that advances only when told — `time.monotonic`'s shape,
    with no sleeps anywhere (the harness rule). Injected in place of the whole
    `time` module the projection reads, so nothing global moves."""

    def __init__(self, step: float = 0.0) -> None:
        self.now = 0.0
        self.step = step

    def monotonic(self) -> float:
        return self.now

    def tick(self, *_args, **_kwargs) -> None:
        self.now += self.step


def _many_documents(count: int) -> list[tuple[str, str]]:
    return [(f"ideation/staging/demo-topic/doc-{n:03d}.md",
             f"# Doc {n}\n\nStatus: draft\n") for n in range(count)]


def test_the_at_open_projection_attempts_at_most_the_source_cap():
    """The COUNT bound, on the route that runs inside the gate action.

    `create_session` is the at-open projection, so the cap is ITS default rather
    than an argument a caller has to remember. The real corpus measures 176
    governed documents, so this bound genuinely binds there — a cap above the
    corpus would be decoration."""
    nlm = FakeNlm()
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    documents = _many_documents(200)

    result = adapter_over(nlm).create_session(alias, documents)

    adds = [c for c in nlm.calls if c[:2] == ("source", "add")]
    assert wb.SESSION_SOURCE_COUNT_CAP < 176, (
        "the cap must bind on the measured real corpus (176 governed documents)")
    assert len(adds) == wb.SESSION_SOURCE_COUNT_CAP
    assert result.sources_total == 200
    assert result.sources_added == wb.SESSION_SOURCE_COUNT_CAP
    assert result.sources_deferred == 200 - wb.SESSION_SOURCE_COUNT_CAP
    # deferring is not failing: the notebook exists and holds what it holds
    assert result.ok is True and result.skipped is False
    assert "DEFERRED" in result.detail and "D19" in result.detail
    # and WHICH sources were projected is deterministic (sorted by path), so two
    # runs over one corpus do not shuffle the notebook
    projected = sorted(s["title"].split("  #")[0] for s in nlm.sources[
        nlm.id_of(alias)])
    assert projected == [p for p, _ in documents[:wb.SESSION_SOURCE_COUNT_CAP]]


def test_a_slow_nlm_spends_the_wall_clock_budget_and_defers_the_rest(monkeypatch):
    """The WALL-CLOCK bound, which the count cap cannot supply: 60 wedged calls is
    still 45 minutes. The deadline is consulted BEFORE each add — never mid-call —
    so a slow projection stops between calls instead of abandoning one.

    Deterministic by injected clock, not by sleeping: each simulated round trip
    advances the clock by 40s against a 90s budget, so exactly three adds fit."""
    clock = _Clock(step=40.0)
    monkeypatch.setattr(wb, "time", clock)
    nlm = FakeNlm()
    nlm_call = nlm.__call__

    def timed(*args, **kwargs):
        out = nlm_call(*args, **kwargs)
        if args[:2] == ("source", "add"):
            clock.tick()
        return out

    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    adapter = wb.NotebookAdapter(timed, available=True)

    result = adapter.create_session(alias, _many_documents(20))

    assert wb.SESSION_PROJECTION_BUDGET == 90.0
    assert len([c for c in nlm.calls if c[:2] == ("source", "add")]) == 3
    assert result.sources_added == 3
    assert result.sources_deferred == 17
    assert result.ok is True
    assert "DEFERRED" in result.detail


def test_the_deferred_remainder_reaches_the_human_as_an_honest_notice():
    """FR-042's channel, used for a bound rather than a failure: the session HAS
    its notebook, so `created` is True — and the count is named, with the one
    command that completes it. A truncated projection reported as an unqualified
    success is the same dishonesty as a failed retire reported as "already gone"."""
    result = wb.ProjectionResult(
        ok=True, skipped=False, detail="bounded", alias="x", notebook_id="nb1",
        created=True, sources_total=176, sources_added=60, sources_deferred=116)

    created, notice = bs.open_session_notebook(
        _StubCreate(result), alias="xf-session-x", branch="draft/demo-topic",
        worktree=".", repository=REPO)

    assert created is True
    assert notice is not None
    assert "60 of 176" in notice and "116 were DEFERRED" in notice
    assert "Nothing failed" in notice
    assert "--session-ref draft/demo-topic --apply" in notice
    # and a projection with nothing deferred still says nothing
    assert bs.open_session_notebook(
        _StubCreate(wb.ProjectionResult(ok=True, skipped=False, detail="all",
                                        alias="x", notebook_id="nb1", created=True,
                                        sources_total=3, sources_added=3)),
        alias="xf-session-x", branch="draft/demo-topic", worktree=".",
        repository=REPO) == (True, None)


def test_the_off_request_re_sync_is_unbounded_and_completes_the_remainder():
    """The other half of preserving D19: the bound would be a silent truncation if
    the deferred sources were unreachable. `sync-notebooklm-books.py --session-ref`
    calls `project_documents` directly, with no bounds, and the diff is by content
    hash — so the re-sync adds exactly what is missing."""
    nlm = FakeNlm()
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    documents = _many_documents(80)
    adapter = adapter_over(nlm)
    adapter.create_session(alias, documents)
    before = len([c for c in nlm.calls if c[:2] == ("source", "add")])

    result = wb.project_documents(adapter, alias, documents)

    assert result.sources_deferred == 0
    assert result.sources_added == 80 - before
    assert len(nlm.sources[nlm.id_of(alias)]) == 80
    assert result.ok is True


def test_a_bounded_projection_never_prunes_what_the_re_sync_added():
    """The trap the prune loop sets. `_sync_sources` drops managed sources whose
    path LEFT the desired set — and a DEFERRED path has not left it. Reading the
    truncated set there would make a bounded open and an unbounded re-sync take
    turns undoing each other, one deleting what the other just uploaded."""
    nlm = FakeNlm()
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    documents = _many_documents(80)
    adapter = adapter_over(nlm)
    adapter.create_session(alias, documents)
    wb.project_documents(adapter, alias, documents)      # the human's re-sync
    assert len(nlm.sources[nlm.id_of(alias)]) == 80
    deletes_before = len([c for c in nlm.calls if c[:2] == ("source", "delete")])

    again = adapter.create_session(alias, documents)      # a second bounded open

    assert len(nlm.sources[nlm.id_of(alias)]) == 80, "the re-synced sources survive"
    assert len([c for c in nlm.calls
                if c[:2] == ("source", "delete")]) == deletes_before
    assert again.sources_added == 0                       # every hash already matched


def test_the_runbook_names_the_bound_by_its_production_constants():
    """The bound changes what a human SEES (a partial notebook plus a notice), so
    the runbook must state it — and it names the constants rather than
    transcribing their values, so a re-tune cannot leave the doc quietly wrong.
    Asserted through `getattr`, so a RENAME fails here too. (The port-contract
    half of this pin stayed with `specs/007-workbench-branch-sessions/contracts/
    session-ports.md` in codexFactory's Speckit surface —
    adopt-neutral-tooling-home tranche B, 2026-08-03.)"""
    from conftest import REPO_ROOT

    for name in ("SESSION_SOURCE_COUNT_CAP", "SESSION_PROJECTION_BUDGET"):
        assert isinstance(getattr(wb, name), (int, float))
        doc = REPO_ROOT / "docs" / "ideation-dashboard-session-runbook.md"
        assert name in doc.read_text(encoding="utf-8"), (doc.name, name)
