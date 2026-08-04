"""Session IDENTITY derivations, exhaustively, including the traps (T009).

Everything here is derived — a branch session persists no descriptor (D10) — so
these derivations are the whole identity of a session and a wrong one is not a
cosmetic bug: it opens the wrong branch, joins another tile's session, or points
a notebook at the wrong worktree.

The traps that earn their own tests:

  * a colon-bearing `Staging ID:` (`openxFactory:staging:<topic>`) is NOT a legal
    git ref, so taken literally the ratified requirement would make every
    staged-topic session unopenable (research R2). Reduction to the final
    segment is the fix, asserted against `git check-ref-format` itself;
  * the notebook alias is keyed on (repository, BRANCH), so `draft/<t>-2` and
    `draft/<t>` differ AND the same branch in two repositories differs
    (FR-037, spec C9) — a branch-only alias is not injective;
  * the NAMESPACE COLLISION: `draft/foo-2` is both tile `foo-2`'s FIRST
    deterministic branch and tile `foo`'s SECOND session branch. Both directions
    are asserted — `foo-2` must not JOIN it, and `foo` must not CONSUME it
    (FR-002, FR-026, data-model G12).
"""

from __future__ import annotations

import pytest

from ideation_dashboard import branch_session as bs
from ideation_dashboard import session_git as sg
from ideation_dashboard.snapshot_registry import SnapshotEntry, SnapshotRegistry

REPO = "openxFactory"


# --------------------------------------------------------------------------
# reduce_scope_id + session_branch (FR-002; research R2)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("raw,reduced", [
    ("openxFactory:staging:workbench-branch-sessions", "workbench-branch-sessions"),
    ("openxFactory:staging:demo-topic", "demo-topic"),
    ("demo-topic", "demo-topic"),
    ("  demo-topic  ", "demo-topic"),
    ("a:b", "b"),
])
def test_reduce_scope_id_takes_the_final_colon_segment(raw, reduced):
    assert bs.reduce_scope_id(raw) == reduced


@pytest.mark.parametrize("kind,scope_id,ordinal,branch", [
    ("staged-topic", "demo-topic", None, "draft/demo-topic"),
    ("staged-topic", "demo-topic", 2, "draft/demo-topic-2"),
    ("staged-topic", "demo-topic", 7, "draft/demo-topic-7"),
    # the REAL staging id from the corpus, which is not ref-legal unqualified
    ("staged-topic", "openxFactory:staging:workbench-branch-sessions", None,
     "draft/workbench-branch-sessions"),
    ("cluster", "cl-accessibility", None, "cluster/cl-accessibility"),
    ("cluster", "cl-accessibility", 3, "cluster/cl-accessibility-3"),
    ("possible", "pos-derived-thing", None, "possible/pos-derived-thing"),
])
def test_session_branch_is_deterministic_and_actor_free(kind, scope_id, ordinal, branch):
    assert bs.session_branch(kind, scope_id, ordinal=ordinal) == branch


def test_session_branch_encodes_no_actor(scratch_repo):
    # FR-002: the branch name is derived from the TILE and never from the human.
    for actor in ("brett", "team-006@opensoft.one"):
        assert actor not in bs.session_branch("staged-topic", "demo-topic")


@pytest.mark.parametrize("kind,scope_id", [
    ("staged-topic", ""),
    ("staged-topic", "   "),
    ("staged-topic", "../escape"),
    ("staged-topic", "with space"),
    ("staged-topic", "trailing.lock"),
    ("staged-topic", "has~tilde"),
    ("staged-topic", "a/b"),          # a tile id is ONE path segment, never a path
    ("staged-topic", "refs/heads/main"),
    ("unknown-kind", "demo-topic"),
])
def test_session_branch_refuses_a_name_git_would_reject(kind, scope_id):
    with pytest.raises(bs.SessionRefused):
        bs.session_branch(kind, scope_id)


@pytest.mark.parametrize("ordinal", [0, 1, -2, "2"])
def test_session_branch_refuses_a_non_ordinal_ordinal(ordinal):
    # the ratified spelling starts at -2; ordinal 1 IS the bare name (FR-025)
    with pytest.raises(bs.SessionRefused):
        bs.session_branch("staged-topic", "demo-topic", ordinal=ordinal)


def test_every_derived_branch_passes_gits_own_check_ref_format(scratch_repo):
    """The data-model's validation rule, asserted against git rather than a
    regex: the derived name must pass `git check-ref-format` BEFORE any git call
    (research R2's failure mode is exactly this)."""
    git = sg.SessionGit(scratch_repo.root)
    derived = [
        bs.session_branch("staged-topic", "openxFactory:staging:workbench-branch-sessions"),
        bs.session_branch("staged-topic", "demo-topic", ordinal=2),
        bs.session_branch("cluster", "cl-avatar-client"),
        bs.session_branch("possible", "pos-derived-lens-launch-a1b2c3"),
    ]
    for branch in derived:
        assert git.check_ref_format(branch) is True
    # and the un-reduced id would NOT have passed — the reduction is load-bearing
    assert git.check_ref_format(
        "draft/openxFactory:staging:workbench-branch-sessions") is False


# --------------------------------------------------------------------------
# worktree_path (FR-005; research R7)
# --------------------------------------------------------------------------

def test_worktree_path_flattens_the_branch_under_the_sessions_container(scratch_repo):
    path = bs.worktree_path(scratch_repo.root, "draft/demo-topic")
    assert path == scratch_repo.container / "sessions" / "draft__demo-topic"
    assert bs.container_root(scratch_repo.root) == scratch_repo.container
    assert bs.sessions_root(scratch_repo.root) == scratch_repo.container / "sessions"


def test_worktree_path_flattens_every_slash(scratch_repo):
    assert bs.worktree_path(scratch_repo.root, "cluster/cl-a").name == "cluster__cl-a"
    assert bs.worktree_path(scratch_repo.root, "a/b/c").name == "a__b__c"


def test_the_sessions_subdir_keeps_speckit_feature_worktrees_out_of_the_way(scratch_repo):
    """Speckit's own feature worktrees use the SAME container root
    (`worktree_root: ../codexFactory-worktrees`), so session worktrees live one
    level down in `sessions/` (research R7)."""
    path = bs.worktree_path(scratch_repo.root, "draft/demo-topic")
    assert path.parent.name == "sessions"
    assert path.parent.parent == scratch_repo.container


@pytest.mark.parametrize("branch", ["../escape", "/abs", "draft/../../escape"])
def test_worktree_path_refuses_a_branch_that_would_escape_the_container(scratch_repo, branch):
    with pytest.raises(bs.SessionRefused):
        bs.worktree_path(scratch_repo.root, branch)


def test_branch_from_worktree_dir_round_trips_the_flattening(scratch_repo):
    for branch in ("draft/demo-topic", "draft/demo-topic-2", "cluster/cl-a"):
        path = bs.worktree_path(scratch_repo.root, branch)
        assert bs.branch_from_worktree_dir(path) == branch


# --------------------------------------------------------------------------
# notebook_alias (FR-037, spec C9 and C11)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("repository,branch,stem", [
    (REPO, "draft/demo-topic", "xf-session-openxfactory-demo-topic"),
    (REPO, "draft/demo-topic-2", "xf-session-openxfactory-demo-topic-2"),
    (REPO, "cluster/cl-avatar-client", "xf-session-openxfactory-cluster-cl-avatar-client"),
    (REPO, "possible/pos-derived-x", "xf-session-openxfactory-possible-pos-derived-x"),
    ("codexFactory", "draft/demo-topic", "xf-session-codexfactory-demo-topic"),
])
def test_the_readable_half_of_the_alias_is_the_documented_transform(
        repository, branch, stem):
    """FR-037's transform, unchanged — it is what a human reads in NotebookLM."""
    assert bs.notebook_alias_stem(repository, branch) == stem
    assert bs.notebook_alias(repository, branch).startswith(stem + "-k")


@pytest.mark.parametrize("repository,branch,alias", [
    (REPO, "draft/demo-topic", "xf-session-openxfactory-demo-topic-kb65f0e2ccb72"),
    (REPO, "draft/demo-topic-2",
     "xf-session-openxfactory-demo-topic-2-k3aa0019da9c8"),
    (REPO, "cluster/cl-avatar-client",
     "xf-session-openxfactory-cluster-cl-avatar-client-kd41f0e1d1229"),
    (REPO, "possible/pos-derived-x",
     "xf-session-openxfactory-possible-pos-derived-x-k4ad3cf60a461"),
    ("codexFactory", "draft/demo-topic",
     "xf-session-codexfactory-demo-topic-k7e4fba6e7375"),
])
def test_notebook_alias_is_the_documented_derivation(repository, branch, alias):
    """The WHOLE alias, pinned literally (FR-037, C11): the derivation is a
    stable identity — a session that reconnects to its notebook after a restart
    re-derives this exact title, so a silent change of the digest input or width
    would orphan every existing session notebook."""
    assert bs.notebook_alias(repository, branch) == alias


def test_an_ordinal_alias_is_distinct_from_its_base_alias():
    # D11's hazard read forwards: `draft/<t>-2` must not collide with
    # `draft/<t>`'s notebook.
    assert (bs.notebook_alias(REPO, "draft/demo-topic-2")
            != bs.notebook_alias(REPO, "draft/demo-topic"))


def test_the_same_branch_in_two_repositories_yields_two_aliases():
    # FR-037 / C9: the session KEY is (repository, branch), so a branch-only
    # alias is not injective — two repositories can carry the same topic id.
    assert (bs.notebook_alias("openxFactory", "draft/demo-topic")
            != bs.notebook_alias("codexFactory", "draft/demo-topic"))


def test_the_alias_never_uses_the_swept_workbench_prefix():
    # FR-038 / D11: an `xf-wb-*` session notebook would be an orphan from birth
    # and the next routine sweep would delete it mid-session.
    alias = bs.notebook_alias(REPO, "draft/demo-topic")
    assert alias.startswith("xf-session-")
    assert not alias.startswith("xf-wb-")
    assert "xf-wb-" not in alias


def test_the_readable_half_is_lowercase_including_the_repository_segment():
    assert bs.notebook_alias_stem("OpsxFactory", "draft/Demo-Topic") == (
        "xf-session-opsxfactory-demo-topic")
    alias = bs.notebook_alias("OpsxFactory", "draft/Demo-Topic")
    assert alias == alias.lower()


def test_two_live_sessions_can_never_share_an_alias():
    keys = [("openxFactory", "draft/demo-topic"),
            ("openxFactory", "draft/demo-topic-2"),
            ("codexFactory", "draft/demo-topic"),
            ("openxFactory", "cluster/cl-demo-topic")]
    aliases = {bs.notebook_alias(r, b) for r, b in keys}
    assert len(aliases) == len(keys)


# The four collision classes PR #49 review finding 11 reproduced over DISTINCT
# VALID session keys. Each pair is two keys the transform maps to ONE alias, so
# the second session rebound the first's notebook and the projection's
# drop-what-left-the-set loop deleted the first's sources — silently, because
# `open_session_notebook` inspected only `result.ok`.
_ALIAS_COLLISION_PAIRS = [
    # (a) namespace-stripping: a staging FOLDER named `cluster-cl-demo` is all it
    #     takes — no privilege, no race
    ((REPO, "draft/cluster-cl-demo"), (REPO, "cluster/cl-demo")),
    # (a') the same, for a derived possible id
    ((REPO, "draft/possible-pos-derived-x"), (REPO, "possible/pos-derived-x")),
    # (b) case-fold: `reduce_scope_id` and `Tile` do not case-fold, so these are
    #     two DIFFERENT tiles
    ((REPO, "draft/Demo-Topic"), (REPO, "draft/demo-topic")),
    # (c) the repository/branch delimiter is also the `/` replacement
    ((REPO, "draft/a-b"), (f"{REPO}-a", "draft/b")),
    # (d) two repositories differing only in case
    (("openxfactory", "draft/demo-topic"), ("openxFactory", "draft/demo-topic")),
]


@pytest.mark.parametrize("first,second", _ALIAS_COLLISION_PAIRS)
def test_the_alias_is_injective_over_valid_session_keys(first, second):
    """FR-037/C11: distinct (repository, branch) keys derive distinct aliases.

    The readable half alone still collides on every one of these pairs — asserted
    below, so the test cannot pass by the transform quietly changing shape."""
    assert first != second
    assert bs.notebook_alias(*first) != bs.notebook_alias(*second)


@pytest.mark.parametrize("first,second", _ALIAS_COLLISION_PAIRS)
def test_the_readable_half_alone_still_collides_on_every_class(first, second):
    """Why the digest is REQUIRED rather than decorative: the FR-037 transform
    maps both keys of each pair onto one string, so an alias that is only the
    transform cannot carry FR-037's own guarantee."""
    assert bs.notebook_alias_stem(*first) == bs.notebook_alias_stem(*second)


# --------------------------------------------------------------------------
# the ordinal family and the next ordinal (FR-026, G5)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("branch,base,ordinal", [
    ("draft/demo-topic", "draft/demo-topic", 1),
    ("draft/demo-topic-2", "draft/demo-topic", 2),
    ("draft/demo-topic-17", "draft/demo-topic", 17),
    ("draft/demo-topic-and-more", "draft/demo-topic", None),
    ("draft/demo-topical", "draft/demo-topic", None),
    ("draft/demo-topic-2x", "draft/demo-topic", None),
    ("draft/demo-topic-02", "draft/demo-topic", None),   # not the ratified spelling
    ("draft/other", "draft/demo-topic", None),
])
def test_ordinal_of_reads_only_the_ratified_spelling(branch, base, ordinal):
    assert bs.ordinal_of(branch, base) == ordinal


def test_next_ordinal_is_the_highest_existing_plus_one():
    base = "draft/demo-topic"
    assert bs.next_ordinal([], base) == 2
    assert bs.next_ordinal([base], base) == 2
    assert bs.next_ordinal([base, base + "-2"], base) == 3
    assert bs.next_ordinal([base + "-5"], base) == 6
    # near-miss names are not family members
    assert bs.next_ordinal([base + "-and-more", base + "ical"], base) == 2


def test_next_ordinal_skips_a_candidate_that_is_another_tiles_deterministic_name():
    """FR-026 / G12, direction (b): tile `demo-topic`'s NEW allocation must not
    consume tile `demo-topic-2`'s deterministic name."""
    base = "draft/demo-topic"
    inventory = bs.TileInventory.from_scopes(
        staged_topics=("demo-topic", "demo-topic-2"))
    tile = bs.Tile("staged-topic", "demo-topic")
    excluded = inventory.other_branches(tile)
    assert "draft/demo-topic-2" in excluded
    # ordinal 2 is spoken for by another TILE, so the allocation skips to 3
    assert bs.next_ordinal([base], base, excluded=excluded) == 3
    # and the excluded branch does not raise the ceiling either
    assert bs.next_ordinal([base, base + "-2"], base, excluded=excluded) == 3


def test_the_excluded_branch_is_left_out_of_the_abandoned_branch_scan():
    """The same exclusion on the OTHER scan (FR-026): a `-2` branch belonging to
    another tile can neither be resumed as this tile's session nor consume its
    ordinal."""
    tile = bs.Tile("staged-topic", "demo-topic")
    inventory = bs.TileInventory.from_scopes(
        staged_topics=("demo-topic", "demo-topic-2"))
    names = ["draft/demo-topic", "draft/demo-topic-2", "draft/demo-topic-3"]
    family = bs.tile_branch_family(names, tile.branch,
                                   excluded=inventory.other_branches(tile))
    assert set(family.values()) == {"draft/demo-topic", "draft/demo-topic-3"}
    assert "draft/demo-topic-2" not in family.values()


# --------------------------------------------------------------------------
# the cross-tile collision refusal (FR-002, G12), direction (a)
# --------------------------------------------------------------------------

def test_a_tile_whose_name_is_another_tiles_ordinal_form_is_named_in_the_refusal():
    inventory = bs.TileInventory.from_scopes(
        staged_topics=("demo-topic", "demo-topic-2"))
    tile = bs.Tile("staged-topic", "demo-topic-2")
    owner = bs.collision_owner(inventory, tile)
    assert owner == bs.Tile("staged-topic", "demo-topic")

    with pytest.raises(bs.CrossTileCollision) as exc:
        bs.assert_no_cross_tile_collision(inventory, tile,
                                          existing={"draft/demo-topic-2"})
    message = str(exc.value)
    # BOTH tiles named — never a silent join (FR-002)
    assert "demo-topic-2" in message and "demo-topic" in message
    assert exc.value.tile == tile
    assert exc.value.other == owner
    assert exc.value.branch == "draft/demo-topic-2"


def test_the_collision_refusal_fires_only_when_the_branch_actually_exists():
    """Nothing to join and nothing to cross while the name is unused: the
    refusal is about an AMBIGUOUS existing branch, not about a name shape."""
    inventory = bs.TileInventory.from_scopes(
        staged_topics=("demo-topic", "demo-topic-2"))
    tile = bs.Tile("staged-topic", "demo-topic-2")
    bs.assert_no_cross_tile_collision(inventory, tile, existing=set())


def test_no_collision_when_the_other_tile_is_not_in_the_inventory():
    inventory = bs.TileInventory.from_scopes(staged_topics=("demo-topic-2",))
    tile = bs.Tile("staged-topic", "demo-topic-2")
    assert bs.collision_owner(inventory, tile) is None
    bs.assert_no_cross_tile_collision(inventory, tile,
                                      existing={"draft/demo-topic-2"})


def test_a_cluster_tile_does_not_collide_with_a_staged_topic_of_the_same_id():
    inventory = bs.TileInventory.from_scopes(staged_topics=("cl-a",),
                                             clusters=("cl-a-2",))
    tile = bs.Tile("cluster", "cl-a-2")
    # different namespaces (`draft/` vs `cluster/`) cannot collide
    assert bs.collision_owner(inventory, tile) is None


# --------------------------------------------------------------------------
# the git-backed union scan (FR-026) — remote OR local, never one alone
# --------------------------------------------------------------------------

def test_existing_branch_names_is_the_union_of_remote_and_local(scratch_repo):
    git = sg.SessionGit(scratch_repo.root)
    base = "draft/demo-topic"
    # local-only (nothing pushes before open-pr)
    git.worktree_add(base, bs.worktree_path(scratch_repo.root, base), "main")
    # remote-only (the two-machine race, D17) — created in the bare origin, no fetch
    scratch_repo.add_remote_only_branch("draft/demo-topic-4")

    names = bs.existing_branch_names(git, base)
    assert names == ("draft/demo-topic", "draft/demo-topic-4")
    assert bs.next_ordinal(names, base) == 5


def test_allocate_ordinal_uses_the_union_and_the_inventory(scratch_repo):
    git = sg.SessionGit(scratch_repo.root)
    tile = bs.Tile("staged-topic", "demo-topic")
    inventory = bs.TileInventory.from_scopes(
        staged_topics=("demo-topic", "demo-topic-2"))
    git.worktree_add(tile.branch, bs.worktree_path(scratch_repo.root, tile.branch),
                     "main")

    # ordinal 2 is tile `demo-topic-2`'s deterministic name, so NEW skips it
    assert bs.allocate_ordinal(git, inventory, tile) == 3
    assert bs.new_session_branch(git, inventory, tile) == "draft/demo-topic-3"


def test_a_remote_only_ordinal_raises_the_next_allocation(scratch_repo):
    """FR-026's mandatory remote input: a `-2` that exists ONLY in the bare
    origin must push the next allocation to `-3`."""
    git = sg.SessionGit(scratch_repo.root)
    tile = bs.Tile("staged-topic", "demo-topic")
    inventory = bs.TileInventory.from_scopes(staged_topics=("demo-topic",))
    git.worktree_add(tile.branch, bs.worktree_path(scratch_repo.root, tile.branch),
                     "main")
    scratch_repo.add_remote_only_branch("draft/demo-topic-2")

    assert bs.allocate_ordinal(git, inventory, tile) == 3


def test_abandoned_branch_candidates_exclude_another_tiles_name(scratch_repo):
    git = sg.SessionGit(scratch_repo.root)
    tile = bs.Tile("staged-topic", "demo-topic")
    inventory = bs.TileInventory.from_scopes(
        staged_topics=("demo-topic", "demo-topic-2"))
    for branch in ("draft/demo-topic", "draft/demo-topic-2", "draft/demo-topic-3"):
        git.git(scratch_repo.root, "branch", branch, "main")

    found = bs.abandoned_branch_candidates(git, inventory, tile)
    assert found == ("draft/demo-topic", "draft/demo-topic-3")


def test_new_session_branch_refuses_on_a_genuine_cross_tile_collision(scratch_repo):
    git = sg.SessionGit(scratch_repo.root)
    inventory = bs.TileInventory.from_scopes(
        staged_topics=("demo-topic", "demo-topic-2"))
    tile = bs.Tile("staged-topic", "demo-topic-2")
    git.git(scratch_repo.root, "branch", "draft/demo-topic-2", "main")

    with pytest.raises(bs.CrossTileCollision):
        bs.deterministic_session_branch(git, inventory, tile)


# --------------------------------------------------------------------------
# is_live — a REGISTRY lookup, never a branch or a directory (T010; FR-008)
# --------------------------------------------------------------------------

def test_is_live_is_a_registry_lookup(tmp_path, scratch_repo):
    registry = SnapshotRegistry()
    branch = "draft/demo-topic"
    assert bs.is_live(registry, REPO, branch) is False

    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("{}", encoding="utf-8")
    registry.register(SnapshotEntry(repository=REPO, ref=branch,
                                    snapshot_path=snapshot,
                                    source_root=scratch_repo.root))
    assert bs.is_live(registry, REPO, branch) is True

    registry.drop(REPO, branch)
    assert bs.is_live(registry, REPO, branch) is False


def test_a_branch_or_a_worktree_alone_never_reads_as_live(scratch_repo):
    """The D15 rule: an abandoned branch survives, and a crash can leave a
    worktree directory behind. Neither is a live session."""
    git = sg.SessionGit(scratch_repo.root)
    registry = SnapshotRegistry()
    branch = "draft/demo-topic"
    path = bs.worktree_path(scratch_repo.root, branch)
    git.worktree_add(branch, path, "main")

    assert git.branch_exists(branch) and path.is_dir()
    assert bs.is_live(registry, REPO, branch) is False


def test_is_live_does_not_confuse_two_repositories(tmp_path, scratch_repo):
    registry = SnapshotRegistry()
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("{}", encoding="utf-8")
    registry.register(SnapshotEntry(repository="openxFactory", ref="draft/demo-topic",
                                    snapshot_path=snapshot,
                                    source_root=scratch_repo.root))
    assert bs.is_live(registry, "openxFactory", "draft/demo-topic") is True
    assert bs.is_live(registry, "codexFactory", "draft/demo-topic") is False


def test_is_live_documents_the_single_bootstrap_exception():
    doc = bs.is_live.__doc__ or ""
    assert "T033a" in doc
    assert "bootstrap" in doc.lower()


# ==========================================================================
# SESSION OPEN — the lifecycle (T017/T018/T019; FR-001, FR-003, FR-004, FR-005)
#
# Everything above derives NAMES. Everything below opens a real session against
# a real throwaway repository, because what these tests assert is git's own
# behaviour: that a branch and a worktree came into existence, that a second
# writer JOINED instead of forking a second session, and that the SERVED
# checkout never moved while any of it happened.
# ==========================================================================

from pathlib import Path                                 # noqa: E402

from ideation_dashboard import gate_console as gc        # noqa: E402
from ideation_dashboard.boundary import HumanGate        # noqa: E402
from session_fixtures import GATE_RECORDS_PREFIX         # noqa: E402

TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
DOC = "ideation/staging/demo-topic/note.md"
ALLOWLIST = (GATE_RECORDS_PREFIX, "ideation/staging/")


def _session_world(repo):
    """The three things every lifecycle test needs: the git seam rooted at the
    SERVED checkout, an empty registry (liveness lives there and nowhere else),
    and the tile the session opens on."""
    return (sg.SessionGit(repo.root), SnapshotRegistry(),
            bs.Tile(bs.STAGED_TOPIC, TOPIC))


def _gate(worktree, actor="brett"):
    """A HumanGate rooted at the WORKTREE — which is what makes a session
    record land in the worktree's copy of the records path (plan Constraint 10:
    the file-producing verbs' records ride the session commit)."""
    return HumanGate(worktree, list(ALLOWLIST), human_actor=actor)


def _act(repo, git, worktree, *, actor="brett", at="2026-07-26T12:00:00Z",
         text="# Note\n", document=DOC):
    """One file-producing gate action inside the session, end to end."""
    target = worktree / document
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    stamp = bs.action_stamp(at)
    record = gc.build_gate_action_record(
        actor=actor, action=gc.ACTION_EDIT_DOCUMENT, at=at, ref=DRAFT,
        document=document, artifacts=[bs.commit_artifact(stamp)])
    return bs.commit_gate_action(_gate(worktree, actor), git, worktree=worktree,
                                branch=DRAFT, record=record, documents=[document])


# --------------------------------------------------------------------------
# T017 — the first gate write opens the branch and materializes the worktree
# --------------------------------------------------------------------------

def test_the_first_gate_write_opens_the_branch_and_the_worktree(scratch_repo):
    git, registry, tile = _session_world(scratch_repo)
    assert DRAFT not in scratch_repo.local_branches()

    opened = bs.open_session(git, registry, repository=REPO, tile=tile)

    assert opened.branch == DRAFT
    assert opened.joined is False                    # OPENED, not joined
    assert git.branch_exists(DRAFT)
    assert DRAFT in scratch_repo.local_branches()
    # the worktree is a real git worktree, not just a directory
    assert opened.worktree.is_dir()
    assert opened.worktree.resolve() in [p.resolve() for p in git.worktree_paths()]


def test_the_worktree_materializes_inside_the_gitignored_container(scratch_repo):
    """FR-005: the sessions container is the ALREADY-gitignored
    `<repo>-worktrees/`, one level down in `sessions/` so Speckit's own feature
    worktrees (same root) can never be mistaken for a session (research R7)."""
    git, registry, tile = _session_world(scratch_repo)
    opened = bs.open_session(git, registry, repository=REPO, tile=tile)

    assert opened.worktree == scratch_repo.container / "sessions" / "draft__demo-topic"
    assert opened.worktree.parent == bs.sessions_root(scratch_repo.root)
    assert bs.container_root(scratch_repo.root) == scratch_repo.container


def test_the_session_write_lands_in_the_worktree_and_not_the_served_checkout(scratch_repo):
    """FR-001: the write reaches the BRANCH through the branch's own worktree.
    The served checkout gains neither the document nor its record."""
    git, registry, tile = _session_world(scratch_repo)
    opened = bs.open_session(git, registry, repository=REPO, tile=tile)

    result = _act(scratch_repo, git, opened.worktree)

    assert (opened.worktree / DOC).is_file()
    assert not (scratch_repo.root / DOC).exists()
    assert not (scratch_repo.root / result.record_relpath).exists()
    # the commit is on the SESSION branch, and `main` never saw it
    assert git.commits_ahead("main", DRAFT) == 1
    listed = git.git(opened.worktree, "ls-tree", "-r", "--name-only", "main")
    assert DOC not in listed.splitlines()


def test_the_session_registers_its_liveness_entry_rooted_at_the_worktree(scratch_repo):
    """FR-008: the registry entry is the AUTHORITATIVE liveness signal, and its
    `source_root` is the worktree — which is what later lets the session's own
    panels and `/source` reads follow the branch (T033)."""
    git, registry, tile = _session_world(scratch_repo)
    opened = bs.open_session(git, registry, repository=REPO, tile=tile)

    assert bs.is_live(registry, REPO, DRAFT) is True
    entry = registry.get(REPO, DRAFT)
    assert entry is not None
    assert Path(entry.source_root).resolve() == opened.worktree.resolve()
    assert entry.ref == DRAFT
    # and it is NOT the published ref — publication refuses it as session-local
    assert entry.ref != "main"


# --------------------------------------------------------------------------
# T018 — a second actor JOINS; the branch encodes no actor (FR-003, FR-002)
# --------------------------------------------------------------------------

def test_a_second_actors_gate_write_joins_the_same_session(scratch_repo):
    git, registry, tile = _session_world(scratch_repo)
    first = bs.open_session(git, registry, repository=REPO, tile=tile)
    _act(scratch_repo, git, first.worktree, actor="brett",
         at="2026-07-26T12:00:00Z")

    # a DIFFERENT human writes on the same tile
    second = bs.open_session(git, registry, repository=REPO, tile=tile)

    assert second.joined is True                       # JOINED, never re-opened
    assert second.branch == first.branch
    assert second.worktree == first.worktree
    assert len(registry.keys()) == 1                    # ONE entry, one session
    assert git.local_ordinals("draft/demo-topic") == (DRAFT,)   # no second branch

    _act(scratch_repo, git, second.worktree, actor="dana",
         at="2026-07-26T13:00:00Z", text="# Note\n\ndana's revision.\n")
    # both humans' actions are commits on the SAME branch
    assert git.commits_ahead("main", DRAFT) == 2
    actors = git.git(second.worktree, "log", "--format=%s", f"main..{DRAFT}")
    assert len(actors.splitlines()) == 2


def test_the_session_branch_name_encodes_neither_actor(scratch_repo):
    """FR-002/FR-003: the branch is derived from the TILE. If it encoded the
    actor, the second writer could not join it — the JOIN and the actor-free
    name are the same requirement read from two sides."""
    git, registry, tile = _session_world(scratch_repo)
    brett = bs.open_session(git, registry, repository=REPO, tile=tile)
    dana = bs.open_session(git, registry, repository=REPO, tile=tile)

    for actor in ("brett", "dana", "harness"):
        assert actor not in brett.branch
        assert actor not in str(brett.worktree.name)
    assert brett.branch == dana.branch == bs.session_branch(bs.STAGED_TOPIC, TOPIC)


def test_joining_is_idempotent_and_creates_no_second_worktree(scratch_repo):
    git, registry, tile = _session_world(scratch_repo)
    bs.open_session(git, registry, repository=REPO, tile=tile)
    before = tuple(sorted(str(p) for p in git.worktree_paths()))

    for _ in range(3):
        opened = bs.open_session(git, registry, repository=REPO, tile=tile)
        assert opened.joined is True
    assert tuple(sorted(str(p) for p in git.worktree_paths())) == before


def test_two_different_tiles_open_two_different_sessions(scratch_repo):
    """The JOIN is keyed on the TILE, so a different tile is a different
    session — the idempotence of FR-003 is not a global lock."""
    git = sg.SessionGit(scratch_repo.root)
    registry = SnapshotRegistry()
    scratch_repo.write("ideation/staging/other-topic/README.md", "# Other\n")
    scratch_repo.commit("second topic", "ideation/staging/other-topic/README.md")

    one = bs.open_session(git, registry, repository=REPO,
                          tile=bs.Tile(bs.STAGED_TOPIC, TOPIC))
    two = bs.open_session(git, registry, repository=REPO,
                          tile=bs.Tile(bs.STAGED_TOPIC, "other-topic"))
    assert one.branch != two.branch
    assert one.worktree != two.worktree
    assert len(registry.keys()) == 2


# --------------------------------------------------------------------------
# T019 — the served checkout NEVER moves (FR-004, SC-002)
# --------------------------------------------------------------------------

def test_the_served_fingerprint_is_unchanged_around_every_session_operation(scratch_repo):
    """SC-002, asserted around EVERY operation rather than once at the end: the
    branch and `HEAD` stay BYTE-IDENTICAL and the working tree changes only
    inside the declared gate-records prefix."""
    git, registry, tile = _session_world(scratch_repo)
    before = scratch_repo.served_fingerprint()

    opened = bs.open_session(git, registry, repository=REPO, tile=tile)
    assert scratch_repo.served_fingerprint() == before          # after OPEN

    _act(scratch_repo, git, opened.worktree, at="2026-07-26T12:00:00Z")
    assert scratch_repo.served_fingerprint() == before          # after a WRITE

    bs.open_session(git, registry, repository=REPO, tile=tile)
    assert scratch_repo.served_fingerprint() == before          # after a JOIN

    _act(scratch_repo, git, opened.worktree, at="2026-07-26T13:00:00Z",
         text="# Note\n\nsecond revision\n")
    assert scratch_repo.served_fingerprint() == before          # after another

    # and the two anchors are literally the same strings, not merely "equal"
    after = scratch_repo.served_fingerprint()
    assert after.branch == before.branch == "main"
    assert after.head == before.head


def test_the_served_working_tree_may_change_only_inside_the_gate_records_prefix(scratch_repo):
    """The one legitimate exception (plan Constraint 10): a MAIN-RESIDENT
    `abandon-session` / `open-pr` record lands in the served checkout's
    gate-records path, exactly as `propose` / `demote` / `dispose` write today.
    The filtered fingerprint stays equal; the RAW porcelain shows the record."""
    git, registry, tile = _session_world(scratch_repo)
    before = scratch_repo.served_fingerprint()
    bs.open_session(git, registry, repository=REPO, tile=tile)

    main_gate = HumanGate(scratch_repo.root, [GATE_RECORDS_PREFIX],
                          human_actor="brett")
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_ABANDON_SESSION,
        at="2026-07-26T14:00:00Z", ref=DRAFT, reason="stopped exploring",
        artifacts=[])
    path = gc.write_gate_action_record(main_gate, gc.DEFAULT_RECORDS_DIR, record)

    assert path.is_file()
    assert scratch_repo.served_fingerprint() == before          # filtered: equal
    raw = git.git_raw(scratch_repo.root, "status", "--porcelain",
                      "--untracked-files=all")
    assert GATE_RECORDS_PREFIX in raw                           # raw: it is there
    for line in raw.splitlines():
        if line.strip():
            assert sg.porcelain_path(line).startswith(GATE_RECORDS_PREFIX), (
                "a session left the served working tree dirty OUTSIDE the one "
                "declared prefix (SC-002)")


@pytest.mark.parametrize("subcommand", ["checkout", "switch", "reset", "stash",
                                        "restore"])
def test_a_session_operation_that_would_move_the_served_checkout_fails(scratch_repo,
                                                                       subcommand):
    """FR-004 as a TEST THAT FAILS: the guard is structural, so an attempt to
    move the served checkout through the session seam raises before git runs."""
    git, registry, tile = _session_world(scratch_repo)
    opened = bs.open_session(git, registry, repository=REPO, tile=tile)
    before = scratch_repo.served_fingerprint()

    with pytest.raises(sg.ServedCheckoutImmovable):
        git.git(scratch_repo.root, subcommand, DRAFT)
    # the same subcommand inside the session's own worktree is nobody's business
    assert scratch_repo.served_fingerprint() == before
    assert opened.worktree.is_dir()


def test_the_guard_is_not_bypassable_by_a_leading_config_option(scratch_repo):
    git, _, _ = _session_world(scratch_repo)
    with pytest.raises(sg.ServedCheckoutImmovable):
        git.git(scratch_repo.root, "-c", "core.pager=cat", "checkout", "main")


def test_no_session_operation_leaves_the_served_checkout_on_the_session_branch(scratch_repo):
    git, registry, tile = _session_world(scratch_repo)
    opened = bs.open_session(git, registry, repository=REPO, tile=tile)
    _act(scratch_repo, git, opened.worktree)

    assert scratch_repo.branch() == "main"
    assert git.current_branch(scratch_repo.root) == "main"
    assert git.current_branch(opened.worktree) == DRAFT
    # `main` in the served checkout is untouched by the session's commit
    assert git.head(scratch_repo.root) == git.head(scratch_repo.root, "main")
    assert git.head(opened.worktree) != git.head(scratch_repo.root)


# --------------------------------------------------------------------------
# what open_session REFUSES rather than guesses
# --------------------------------------------------------------------------

def test_open_refuses_on_a_genuine_cross_tile_collision(scratch_repo):
    """G12 at the LIFECYCLE level: `draft/demo-topic-2` is tile `demo-topic-2`'s
    own first branch, so tile `demo-topic` must not silently JOIN it."""
    git = sg.SessionGit(scratch_repo.root)
    registry = SnapshotRegistry()
    inventory = bs.TileInventory.from_scopes(
        staged_topics=["demo-topic", "demo-topic-2"])
    git.git(scratch_repo.root, "branch", "draft/demo-topic-2", "main")

    with pytest.raises(bs.CrossTileCollision) as exc:
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, "demo-topic-2"),
                        inventory=inventory)
    assert "demo-topic-2" in str(exc.value) and "demo-topic" in str(exc.value)
    assert len(registry.keys()) == 0


def test_open_refuses_a_surviving_branch_with_no_worktree_rather_than_choosing(scratch_repo):
    """FR-025: an abandoned branch that survives must NOT be resumed silently.
    Phase 3 refuses and names both continuations; T056 turns the refusal into
    the offered choice."""
    git = sg.SessionGit(scratch_repo.root)
    registry = SnapshotRegistry()
    git.git(scratch_repo.root, "branch", DRAFT, "main")

    with pytest.raises(bs.AbandonedBranchSurvives) as exc:
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC))
    message = str(exc.value)
    assert DRAFT in message
    assert "resume" in message.lower() and "new" in message.lower()
    assert len(registry.keys()) == 0


def test_open_reports_a_worktree_whose_branch_is_gone_as_stale(scratch_repo):
    """The other half of the JOINT signal (FR-008, D10): a directory with no
    branch is NOT a session — it is stale, and a human cleans it up."""
    git = sg.SessionGit(scratch_repo.root)
    registry = SnapshotRegistry()
    orphan = bs.worktree_path(scratch_repo.root, DRAFT)
    orphan.mkdir(parents=True)
    (orphan / "left-behind.md").write_text("crash residue\n", encoding="utf-8")

    with pytest.raises(bs.StaleSessionWorktree) as exc:
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC))
    assert str(orphan) in str(exc.value)
    assert len(registry.keys()) == 0


def test_open_adopts_a_worktree_and_branch_present_together(scratch_repo):
    """The joint signal read the OTHER way: both present is the bootstrap
    re-derivation's own rule (D10), so a fresh process JOINS rather than
    opening a second session. T033a generalizes this to every worktree in the
    container at process start."""
    git = sg.SessionGit(scratch_repo.root)
    opened = bs.open_session(git, SnapshotRegistry(), repository=REPO,
                             tile=bs.Tile(bs.STAGED_TOPIC, TOPIC))

    fresh = SnapshotRegistry()                    # a NEW process's empty registry
    rejoined = bs.open_session(git, fresh, repository=REPO,
                               tile=bs.Tile(bs.STAGED_TOPIC, TOPIC))
    assert rejoined.joined is True
    assert rejoined.branch == opened.branch
    assert rejoined.worktree == opened.worktree
    assert bs.is_live(fresh, REPO, DRAFT) is True


def test_open_refuses_an_unknown_scope_kind(scratch_repo):
    git, registry, _ = _session_world(scratch_repo)
    with pytest.raises(bs.SessionRefused):
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile("not-a-scope", TOPIC))


# --------------------------------------------------------------------------
# FR-024's session-open precondition (the shape; the full gates are Phase 6)
# --------------------------------------------------------------------------

def test_open_refuses_on_a_live_proposal_and_names_demote(scratch_repo):
    git, registry, tile = _session_world(scratch_repo)
    state = bs.ProposalState(proposal_id="add-demo-topic")

    with pytest.raises(bs.LiveProposalRefused) as exc:
        bs.open_session(git, registry, repository=REPO, tile=tile, proposal=state)
    assert "demote" in str(exc.value)
    assert not git.branch_exists(DRAFT)
    assert len(registry.keys()) == 0


def test_open_says_the_proposal_has_not_landed_while_a_dispatch_is_in_flight(scratch_repo):
    """D20's distinct message: naming `demote` would name a route the human
    cannot take, because there is no proposal to demote yet."""
    git, registry, tile = _session_world(scratch_repo)
    state = bs.ProposalState(dispatch_in_flight=True)

    with pytest.raises(bs.LiveProposalRefused) as exc:
        bs.open_session(git, registry, repository=REPO, tile=tile, proposal=state)
    message = str(exc.value)
    assert "has not landed" in message
    assert "demote" not in message
    assert not git.branch_exists(DRAFT)


def test_the_in_flight_dispatch_is_read_from_the_records_tree(scratch_repo):
    """The trivially-checkable half of FR-024 is wired in Phase 3: a dispatched,
    undelivered `propose` job in the served checkout's records tree IS the
    in-flight signal (the same source `propose`'s own duplicate guard reads)."""
    from ideation_dashboard import kickoff as ko

    records_root = scratch_repo.root / gc.DEFAULT_RECORDS_DIR
    assert bs.proposal_state_for(bs.Tile(bs.STAGED_TOPIC, TOPIC),
                                 records_root=records_root).dispatch_in_flight is False

    job_dir = records_root / TOPIC
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "propose-20260726T120000Z.workflow-job.yaml").write_text(
        f"kind: {ko.ART_WORKFLOW_JOB}\nstatus: {ko.STATUS_DISPATCHED}\n"
        f"topic_id: {TOPIC}\n", encoding="utf-8")

    state = bs.proposal_state_for(bs.Tile(bs.STAGED_TOPIC, TOPIC),
                                 records_root=records_root)
    assert state.dispatch_in_flight is True
    assert state.proposal_id is None            # nothing landed — nothing to demote


# ==========================================================================
# THE CREATE-DOCUMENT ROUTE AND ITS CLI, INSIDE A SESSION
# (T023 / T023a / T025; FR-018, FR-006)
#
# T023a first, because T023 has no input without it: `scope_kind` / `scope_id`
# did not exist ANYWHERE in the transport code before this feature, so the route
# could not tell which tile — and therefore which session — a create belonged to.
#
# The invariant these tests protect in BOTH directions: inside a session the
# create lands on the branch as ONE commit with its record; outside one, every
# byte of the old behaviour is intact, because `create-document` is a
# pre-existing verb with pre-existing callers (FR-018).
# ==========================================================================

from ideation_dashboard import cli as cli_mod                     # noqa: E402
from ideation_dashboard import gate_routes as gr                  # noqa: E402
from ideation_dashboard import serve as serve_mod                 # noqa: E402

CREATE_BODY = {
    "title": "First Draft",
    "summary": "The session's first document.",
    "topics": ["alpha"],
    "area": "ideation/staging/demo-topic/",
    "repository_context": REPO,
}


def _create(repo, body, **kwargs):
    return gr.run_gate_action("create-document", dict(body),
                              checkout_root=repo.root, actor="brett",
                              snapshot_path=None, **kwargs)


def _scoped(**extra):
    return {**CREATE_BODY, "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            **extra}


def test_a_scoped_create_opens_the_session_and_commits_on_the_branch(scratch_repo):
    registry = SnapshotRegistry()
    before = scratch_repo.served_fingerprint()

    status, payload = _create(scratch_repo, _scoped(), session_registry=registry,
                              repository=REPO)

    assert status == 200 and payload["ok"] is True
    assert payload["ref"] == DRAFT
    assert payload["joined"] is False
    assert len(payload["commit"]) == 40
    # the document and the record are in the WORKTREE, not the served checkout
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    assert (worktree / payload["path"]).is_file()
    assert not (scratch_repo.root / payload["path"]).exists()
    assert (worktree / payload["record"]).is_file()
    assert not (scratch_repo.root / payload["record"]).exists()
    # ONE commit, carrying both
    git = sg.SessionGit(scratch_repo.root)
    assert git.commits_ahead("main", DRAFT) == 1
    tree = git.git(worktree, "ls-tree", "-r", "--name-only",
                   payload["commit"]).splitlines()
    assert payload["path"] in tree and payload["record"] in tree
    # SC-002
    assert scratch_repo.served_fingerprint() == before


def test_the_session_record_names_the_branch_and_embeds_no_sha(scratch_repo):
    import yaml

    registry = SnapshotRegistry()
    status, payload = _create(scratch_repo, _scoped(), session_registry=registry,
                              repository=REPO)
    assert status == 200

    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    record = yaml.safe_load((worktree / payload["record"]).read_text(encoding="utf-8"))
    assert record["action"] == gc.ACTION_CREATE_DOCUMENT
    assert record["target"]["ref"] == DRAFT                 # D13: always in a session
    assert record["target"]["document"] == payload["path"]
    kinds = {a["kind"] for a in record["artifacts"]}
    assert kinds == {gc.ART_DOCUMENT, gc.ART_COMMIT}
    assert payload["commit"] not in (worktree / payload["record"]).read_text(
        encoding="utf-8")


def test_a_second_scoped_create_joins_the_session_and_adds_one_commit(scratch_repo):
    registry = SnapshotRegistry()
    first = _create(scratch_repo, _scoped(), session_registry=registry,
                    repository=REPO)[1]
    second = _create(scratch_repo, _scoped(title="Second Draft"),
                     session_registry=registry, repository=REPO)[1]

    assert second["joined"] is True
    assert second["ref"] == first["ref"] == DRAFT
    assert second["commit"] != first["commit"]
    git = sg.SessionGit(scratch_repo.root)
    assert git.commits_ahead("main", DRAFT) == 2
    assert git.local_ordinals("draft/demo-topic") == (DRAFT,)
    assert len(registry.keys()) == 1


def test_a_create_with_no_scope_is_byte_identical_to_the_pre_session_path(scratch_repo):
    """FR-018: `create-document` is a pre-existing verb. With no tile scope it
    writes into the SERVED checkout, records exactly as before, and touches git
    not at all — no branch, no worktree, no commit."""
    registry = SnapshotRegistry()
    status, payload = _create(scratch_repo, CREATE_BODY,
                              session_registry=registry, repository=REPO)

    assert status == 200 and payload["ok"] is True
    assert set(payload) == {"ok", "verb", "path", "record", "status", "hint"}
    assert "ref" not in payload and "commit" not in payload
    assert (scratch_repo.root / payload["path"]).is_file()
    assert (scratch_repo.root / payload["record"]).is_file()
    assert scratch_repo.local_branches() == ("main",)
    assert len(registry.keys()) == 0


def test_a_scoped_create_with_no_declared_registry_takes_the_pre_session_path(scratch_repo):
    """Liveness lives in the registry and nowhere else (FR-008). A caller that
    declares none has no place to key a session, so the route does NOT
    half-open one — it takes the pre-session path, which is what keeps every
    pre-existing `run_gate_action` caller working unchanged."""
    status, payload = _create(scratch_repo, _scoped())

    assert status == 200
    assert "ref" not in payload
    assert (scratch_repo.root / payload["path"]).is_file()
    assert scratch_repo.local_branches() == ("main",)


def test_the_create_only_refusal_is_unchanged_inside_a_session(scratch_repo):
    """FR-018: every existing engine refusal holds. An existing target is still
    the create-only `SOURCE_EDIT` refusal — 409, the boundary's own report, and
    the existing document byte-identical — it is just the WORKTREE's copy now."""
    registry = SnapshotRegistry()
    first = _create(scratch_repo, _scoped(), session_registry=registry,
                    repository=REPO)[1]
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    original = (worktree / first["path"]).read_text(encoding="utf-8")
    git = sg.SessionGit(scratch_repo.root)
    ahead = git.commits_ahead("main", DRAFT)

    status, payload = _create(scratch_repo, _scoped(), session_registry=registry,
                              repository=REPO)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "source-edit" in payload["message"]
    assert (worktree / first["path"]).read_text(encoding="utf-8") == original
    assert git.commits_ahead("main", DRAFT) == ahead      # nothing persisted


@pytest.mark.parametrize("body", [
    {"scope_kind": bs.STAGED_TOPIC},                     # id missing
    {"scope_id": TOPIC},                                 # kind missing
])
def test_a_half_given_scope_is_an_invalid_body(scratch_repo, body):
    status, payload = _create(scratch_repo, {**CREATE_BODY, **body},
                              session_registry=SnapshotRegistry(), repository=REPO)
    assert status == 400
    assert payload["error"] == "invalid_body"
    assert "together" in payload["message"]
    assert scratch_repo.local_branches() == ("main",)


def test_an_unknown_scope_kind_is_an_invalid_body(scratch_repo):
    status, payload = _create(scratch_repo,
                              _scoped(**{"scope_kind": "not-a-scope"}),
                              session_registry=SnapshotRegistry(), repository=REPO)
    assert status == 400 and payload["error"] == "invalid_body"
    assert "scope_kind must be one of" in payload["message"]


def test_a_cross_tile_collision_refuses_the_create_and_persists_nothing(scratch_repo):
    """G12 through the route: the refusal is the engine's own report, at the
    established `gate_refused` 409, and no document is written."""
    scratch_repo.write("ideation/staging/demo-topic-2/README.md", "# Two\n")
    scratch_repo.commit("second tile", "ideation/staging/demo-topic-2/README.md")
    git = sg.SessionGit(scratch_repo.root)
    git.git(scratch_repo.root, "branch", "draft/demo-topic-2", "main")

    status, payload = _create(
        scratch_repo,
        _scoped(scope_id="demo-topic-2", area="ideation/staging/demo-topic-2/"),
        session_registry=SnapshotRegistry(), repository=REPO)

    assert status == 409 and payload["error"] == "gate_refused"
    assert "demo-topic-2" in payload["message"] and "demo-topic" in payload["message"]
    assert not list(scratch_repo.container.rglob("*.md"))


def test_a_scoped_create_refuses_while_a_propose_dispatch_is_in_flight(scratch_repo):
    """FR-024 at the route, the half that is trivially checkable in Phase 3."""
    from ideation_dashboard import kickoff as ko

    job_dir = scratch_repo.root / gc.DEFAULT_RECORDS_DIR / TOPIC
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "propose-20260726T120000Z.workflow-job.yaml").write_text(
        f"kind: {ko.ART_WORKFLOW_JOB}\nstatus: {ko.STATUS_DISPATCHED}\n"
        f"topic_id: {TOPIC}\n", encoding="utf-8")

    status, payload = _create(scratch_repo, _scoped(),
                              session_registry=SnapshotRegistry(), repository=REPO)
    assert status == 409 and payload["error"] == "gate_refused"
    assert "has not landed" in payload["message"]
    assert not scratch_repo.container.joinpath("sessions").exists()


def test_the_tile_inventory_is_discovered_from_the_staging_folders(scratch_repo):
    """FR-026's scans are checked against the LIVE inventory, and the route layer
    is where it is discovered — `branch_session` stays I/O-free.

    The staged-topic half comes from the STAGING FOLDERS; the cluster and possible
    halves are DERIVED FROM THE CHECKOUT (`generator.live_tile_scopes`) and no
    longer depend on the caller happening to hold a snapshot. They used to, and
    every CLI session verb passed None, so the same checkout yielded two different
    tile universes and G12's exclusions were silently OFF on the CLI (PR #49 review
    finding 7). A snapshot, when one is passed, is UNIONED in."""
    scratch_repo.write("ideation/staging/other-topic/README.md", "# Other\n")
    scratch_repo.commit("another tile", "ideation/staging/other-topic/README.md")

    inventory = gr.discover_tile_inventory(scratch_repo.root)
    staged = {t.scope_id for t in inventory.tiles
              if t.scope_kind == bs.STAGED_TOPIC}
    assert {TOPIC, "other-topic"} <= staged
    # the corpus fragment declares `Topics: demo-topic`, so its cluster tile is in
    # the inventory with NO snapshot at all — the divergence, closed
    assert bs.Tile(bs.CLUSTER, f"cl-{TOPIC}") in inventory.tiles

    with_snapshot = gr.discover_tile_inventory(
        scratch_repo.root,
        {"clusters": [{"id": "cl-a"}], "possibles": [{"id": "pos-1"}]})
    assert bs.Tile(bs.CLUSTER, "cl-a") in with_snapshot.tiles
    assert bs.Tile(bs.POSSIBLE, "pos-1") in with_snapshot.tiles
    # UNION, not replacement: a snapshot never subtracts a tile the checkout has
    assert bs.Tile(bs.CLUSTER, f"cl-{TOPIC}") in with_snapshot.tiles


# --------------------------------------------------------------------------
# T025 — the serve wiring: the route layer resolves the session EXPLICITLY
# --------------------------------------------------------------------------

def test_the_gate_route_accepts_the_explicit_session_arguments():
    import inspect

    params = inspect.signature(gr.run_gate_action).parameters
    for name in ("session_registry", "repository", "tile_inventory"):
        assert name in params, f"the route layer needs {name} to resolve a session"
    # `checkout_root` is STILL the served root — research R1's gap is closed by
    # ADDING the session inputs, never by repointing this one
    assert "checkout_root" in params


def test_serve_hands_the_route_its_registry_and_repository():
    """Research R1: `serve.py` passes the SERVED `checkout_root`, so the route
    needed the session's own resolution inputs. This asserts the wiring exists
    rather than that it merely could."""
    import inspect

    source = inspect.getsource(serve_mod.DashboardHandler._handle_gate_action)
    assert "session_registry=self._session_registry()" in source
    assert "repository=self._session_repository()" in source
    assert "checkout_root=Path(self.checkout_root)" in source   # unchanged


def test_the_session_registry_helpers_read_the_active_entry(tmp_path, scratch_repo):
    registry = SnapshotRegistry()
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("{}", encoding="utf-8")
    registry.register(SnapshotEntry(repository=REPO, ref="main",
                                    snapshot_path=snapshot,
                                    source_root=scratch_repo.root), active=True)

    class _Source:
        pass

    source = _Source()
    source.registry = registry
    bound = type("Bound", (serve_mod.DashboardHandler,), {"source": source})
    handler = object.__new__(bound)
    assert handler._session_registry() is registry
    assert handler._session_repository() == REPO

    # a hand-built handler with no source has nowhere to key liveness, so no
    # session is available and `create-document` keeps its pre-session path
    bare = object.__new__(type("Bare", (serve_mod.DashboardHandler,),
                              {"source": None}))
    assert bare._session_registry() is None
    assert bare._session_repository() is None


# --------------------------------------------------------------------------
# T023a — the CLI parity flags (quickstart step 2 depends on them existing)
# --------------------------------------------------------------------------

def _cli_create(repo, *extra):
    return cli_mod.main([
        "gate", "create-document",
        "--repo-root", str(repo.root), "--actor", "brett",
        "--title", "First Draft", "--summary", "The session's first document.",
        "--topics", "alpha", "--repository-context", REPO,
        "--area", "ideation/staging/demo-topic/", *extra])


def test_the_cli_carries_the_scope_flags_and_opens_the_session(scratch_repo, capsys,
                                                               fake_cli_notebook):
    """`fake_cli_notebook` is not decoration: the CLI create is the ONE verb that
    CREATES the session notebook (T074), so with no fake at `cli._notebook_port`
    this test ran real `nlm notebook create` + a source upload against the shared
    account (FR-043; PR #49 finding 17). The fake is what lets the create-at-open
    be ASSERTED instead of merely escaping."""
    before = scratch_repo.served_fingerprint()

    code = _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC)
    out = capsys.readouterr().out

    assert code == 0
    assert f"session branch:     {DRAFT}" in out
    assert "commit:" in out
    git = sg.SessionGit(scratch_repo.root)
    assert git.branch_exists(DRAFT)
    assert git.commits_ahead("main", DRAFT) == 1
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    assert list(worktree.glob("ideation/staging/demo-topic/*.md"))
    assert scratch_repo.served_fingerprint() == before
    # create-at-open, through the INJECTED seam: one notebook, in the session
    # namespace, carrying the worktree's governed documents (FR-036, FR-038)
    alias = bs.notebook_alias(REPO, DRAFT)
    assert fake_cli_notebook.live_aliases() == (alias,)
    created = [c for c in fake_cli_notebook.calls if c[0] == "create"]
    assert len(created) == 1 and created[0][1] == alias
    assert any(path.endswith(".md") for path, _ in created[0][2]), created[0][2]


def test_a_second_cli_create_joins_rather_than_opening_a_second_session(scratch_repo,
                                                                       capsys,
                                                                       fake_cli_notebook):
    """Each CLI verb is a FRESH PROCESS with an empty registry, so this is the
    joint worktree+branch re-derivation doing its job (D10). T033a generalizes
    it to every session in the container at process start."""
    assert _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC) == 0
    capsys.readouterr()
    assert _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC, "--title", "Second Draft") == 0
    out = capsys.readouterr().out

    assert "(joined)" in out
    git = sg.SessionGit(scratch_repo.root)
    assert git.commits_ahead("main", DRAFT) == 2
    assert git.local_ordinals("draft/demo-topic") == (DRAFT,)
    # JOINING creates no second notebook — one session, one notebook, even though
    # each verb re-derives the session from scratch (FR-036, D10)
    alias = bs.notebook_alias(REPO, DRAFT)
    assert fake_cli_notebook.live_aliases() == (alias,)
    creates = [c for c in fake_cli_notebook.calls if c[0] == "create"]
    assert [c[1] for c in creates] == [alias], creates


def test_the_cli_without_the_scope_flags_writes_to_the_served_checkout(scratch_repo,
                                                                      capsys):
    assert _cli_create(scratch_repo) == 0
    out = capsys.readouterr().out
    assert "session branch" not in out
    assert scratch_repo.local_branches() == ("main",)
    assert list((scratch_repo.root / "ideation/staging/demo-topic").glob("*.md"))


def test_the_cli_refuses_a_half_given_scope(scratch_repo, capsys):
    assert _cli_create(scratch_repo, "--scope-id", TOPIC) == 1
    assert "together or not at all" in capsys.readouterr().err
    assert scratch_repo.local_branches() == ("main",)


def test_the_cli_rejects_an_unknown_scope_kind_at_parse_time(scratch_repo):
    with pytest.raises(SystemExit):
        _cli_create(scratch_repo, "--scope-kind", "not-a-scope",
                    "--scope-id", TOPIC)


def test_the_cli_reports_a_session_refusal_verbatim_and_exits_non_zero(scratch_repo,
                                                                      capsys):
    from ideation_dashboard import kickoff as ko

    job_dir = scratch_repo.root / gc.DEFAULT_RECORDS_DIR / TOPIC
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "propose-20260726T120000Z.workflow-job.yaml").write_text(
        f"kind: {ko.ART_WORKFLOW_JOB}\nstatus: {ko.STATUS_DISPATCHED}\n"
        f"topic_id: {TOPIC}\n", encoding="utf-8")

    assert _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC) == 1
    assert "has not landed" in capsys.readouterr().err


def test_opening_a_session_never_changes_which_snapshot_is_ACTIVE(tmp_path, scratch_repo):
    """FR-014a, at the moment it could break: `SnapshotRegistry.register`
    promotes a new entry to ACTIVE when nothing is active yet, which would point
    the shared surfaces (the wheel, the funnel, the pipeline board) at a session
    branch. The session ref enters the KEY SPACE and nothing else."""
    registry = SnapshotRegistry()
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("{}", encoding="utf-8")
    registry.register(SnapshotEntry(repository=REPO, ref="main",
                                    snapshot_path=snapshot,
                                    source_root=scratch_repo.root), active=True)

    git, _, tile = _session_world(scratch_repo)
    opened = bs.open_session(git, registry, repository=REPO, tile=tile)

    assert registry.active is not None
    assert registry.active.ref == "main"
    assert registry.get(REPO, opened.branch) is not None      # keyed, not active
    assert bs.is_live(registry, REPO, opened.branch) is True
