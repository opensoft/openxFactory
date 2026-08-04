"""Independent server scope authority and browser projection parity for doxBench."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from conftest import FIXTURES, REPO_ROOT

from ideation_dashboard import branch_session, gate_console
from ideation_dashboard.doxbench_scope import (
    ScopeConfinementError,
    ScopeKey,
    created_paths_from_records,
    primary_fragment_path,
    resolve_scope,
    session_created_paths,
    session_created_paths_for_scope,
)

CASES_PATH = FIXTURES / "doxbench_scope_cases.json"
WEB_VIEWS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
MODEL_JS = WEB_VIEWS / "staging-workbench-model.js"
WHEEL_MODEL_JS = WEB_VIEWS / "wheel-model.js"
NODE = shutil.which("node")


def _fixture() -> dict:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def _server_projections(source_root: Path) -> dict[str, dict | None]:
    fixture = _fixture()
    snapshot = fixture["snapshot"]
    projections = {}
    for case in fixture["cases"]:
        key = ScopeKey(
            repository=case["repository"],
            ref=case["ref"],
            tile_kind=case["tile_kind"],
            tile_id=case["tile_id"],
        )
        projection = resolve_scope(
            snapshot,
            key,
            source_root=source_root,
            created_paths=case["created_paths"],
        )
        projections[case["name"]] = (
            projection.as_dict() if projection is not None else None
        )
    return projections


def _browser_projections(tmp_path: Path) -> dict[str, dict | None]:
    if NODE is None:
        pytest.skip("node not available for browser scope parity")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    shutil.copy(WHEEL_MODEL_JS, tmp_path / "wheel-model.mjs")
    cases_path = tmp_path / "scope-cases.json"
    cases_path.write_text(CASES_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    harness = tmp_path / "scope-harness.mjs"
    harness.write_text(
        """
import { readFileSync } from 'node:fs';
import { doxbenchScopeProjection } from './staging-workbench-model.mjs';
import { primaryFragmentPath } from './wheel-model.mjs';

const fixture = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const output = {};
for (const row of fixture.cases) {
  output[row.name] = doxbenchScopeProjection(
    fixture.snapshot,
    row.tile_kind,
    row.tile_id,
    {
      repository: row.repository,
      ref: row.ref,
      createdDocuments: row.created_paths,
      outlinePathFor: (outline) =>
        primaryFragmentPath(outline.stagingId, outline.files),
    },
  );
}
console.log(JSON.stringify(output));
""".strip()
        + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [NODE, str(harness), str(cases_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_server_and_actual_browser_projection_are_byte_shape_equivalent(tmp_path):
    assert _server_projections(tmp_path) == _browser_projections(tmp_path)


def test_cluster_is_all_context_and_session_created_material_is_context_and_editable(
    tmp_path,
):
    """FR-043: a session-created document joins BOTH sets, so it is
    chat-eligible under the unchanged FR-015 dual-membership turn guard.

    A cluster tile owns no folder, so its created document is the ONLY editable
    path here — and it is also the one context path the snapshot does not carry,
    which is exactly the case the old editable-only overlay could not express.
    """
    projection = _server_projections(tmp_path)["cluster"]
    assert projection["key"] == {
        "repository": "fixture-repo",
        "ref": "main",
        "tile_kind": "cluster",
        "tile_id": "cl-alpha",
    }
    assert [section["key"] for section in projection["sections"]] == ["members"]
    assert projection["context_paths"] == [
        "ideation/brainstorm/a.md",
        "ideation/brainstorm/b.md",
        "ideation/staging/topic-x/topic-x.md",
        "ideation/brainstorm/session-created.md",
    ]
    assert projection["editable_paths"] == [
        "ideation/brainstorm/session-created.md"
    ]
    # the dual-membership the turn guard reads, stated as a set relation rather
    # than re-listing the paths (data-model.md Section 2 validation rule)
    assert set(projection["editable_paths"]) <= set(projection["context_paths"])
    # PIN CORRECTED (T104 F2, P1 doxbench_scope.py:398). This assertion used to
    # read `candidates == context_paths`, which pinned the DEFECT as intent: it
    # made every readable path a candidate while `doxbench_turns.
    # _require_in_scope_and_editable` requires membership in context_paths AND
    # editable_paths, so on this very fixture case the tile advertised four
    # candidates of which three refused the turn -- including the default,
    # candidates[0], which is what the canvas opens. The candidate list is now
    # what that guard would ACCEPT, and the guard itself is unchanged; the new
    # join test in test_doxbench_turns.py runs every published candidate here
    # through the real `revalidate_scope` so the two halves can never drift
    # apart again silently.
    assert projection["active_document_candidates"] == [
        "ideation/brainstorm/session-created.md"
    ]
    assert set(projection["active_document_candidates"]) <= set(
        projection["editable_paths"])
    assert projection["outline_path"] is None


def test_possible_keeps_cited_and_inherited_disjoint_and_read_only(tmp_path):
    projection = _server_projections(tmp_path)["possible"]
    cited, inherited = projection["sections"]
    assert (cited["key"], cited["inherited"], cited["owned"]) == (
        "cited",
        False,
        False,
    )
    assert (inherited["key"], inherited["inherited"], inherited["owned"]) == (
        "inherited",
        True,
        False,
    )
    assert [row["id"] for row in cited["documents"]] == [
        "ideation/brainstorm/a.md",
        "docs/missing.md",
    ]
    assert cited["documents"][1]["resolved"] is False
    assert projection["context_paths"] == [
        "ideation/brainstorm/a.md",
        "ideation/brainstorm/b.md",
        "ideation/staging/topic-x/topic-x.md",
    ]
    assert projection["editable_paths"] == []
    assert projection["outline_path"] is None


def test_a_picked_possibles_out_of_scope_outline_is_withheld_not_published(tmp_path):
    """PIN CORRECTED (T104 F2, P1 doxbench_scope.py:384 /
    staging-workbench-model.js:379). This test used to be named
    `..._outline_is_declared_context_not_edit_authority` and asserted that the
    PICKED topic's fragment is published as this possible's `outline_path`
    while `editable_paths` stays empty. That combination cannot be served:

      * the name's own claim was already false -- the picked topic's fragment
        is not in this tile's `context_paths` either (its sections are its
        cited evidence alone), so it was declared as neither context nor
        authority, just published;
      * the outline buffer rides EVERY turn (`build_prompt_envelope` passes
        `projection.outline_path` into the FR-015 guard itself), and that guard
        requires a non-null outline path to be in-scope AND editable --
        disclosure requires edit authority. So every chat turn on a picked
        possible refused, whatever document was active, and the refusal named
        a path the operator never chose;
      * declaring it editable is not the available fix: a possible tile owns no
        folder (`gate_routes.tile_owned_prefix` -> None), so the Save path
        refuses that same path. A scope authority granting what the Save
        authority denies is precisely the drift both are written to prevent.

    So it is WITHHELD -- which is the posture every other cluster/possible tile
    already has -- and the tile keeps a working chat rail. The picked topic
    remains reachable where it belongs: on the staged tile that owns it."""
    projection = _server_projections(tmp_path)["picked-possible"]
    assert projection["outline_path"] is None
    assert projection["editable_paths"] == []
    assert projection["active_document_candidates"] == []
    # the pick itself is untouched -- only the OUTLINE PUBLICATION changed
    assert projection["context_paths"] == ["ideation/brainstorm/a.md"]


def test_staged_scope_owns_only_resolved_folder_material_and_created_paths(tmp_path):
    projection = _server_projections(tmp_path)["staged"]
    assert [section["key"] for section in projection["sections"]] == [
        "folder",
        "declaring",
        "neighbourhood",
    ]
    assert [section["owned"] for section in projection["sections"]] == [
        True,
        False,
        False,
    ]
    assert projection["context_paths"] == [
        "ideation/staging/topic-x/topic-x.md",
        "ideation/brainstorm/b.md",
        "docs/neighbour.md",
        "ideation/staging/topic-x/new.md",
    ]
    assert projection["editable_paths"] == [
        "ideation/staging/topic-x/topic-x.md",
        "ideation/staging/topic-x/new.md",
    ]
    # FR-043 again, on the tile that DOES own folder material: the created path
    # is appended after the sections in both sets, so ownership of the tile's own
    # material is unchanged and the created path is additive.
    assert set(projection["editable_paths"]) <= set(projection["context_paths"])
    assert projection["outline_path"] == (
        "ideation/staging/topic-x/topic-x.md"
    )
    # PIN CORRECTED (T104 F2, P1 staging-workbench-model.js:414). The old
    # `candidates == context_paths` pinned two defects at once on this tile:
    # `ideation/brainstorm/b.md` and `docs/neighbour.md` are readable but not
    # editable, so the turn guard refuses them; and `topic-x.md` is the OUTLINE
    # path, so offering it as the active DOCUMENT gave the operator two
    # independent working copies of one file -- two Save rows for one document,
    # the second refused forever on a base the first had just moved, and
    # Discard reverting the second to pre-Save text. Candidates are now the
    # intersection minus the outline: exactly the paths a turn may name and a
    # Save may land, which here is the session-created document.
    assert projection["active_document_candidates"] == [
        "ideation/staging/topic-x/new.md"
    ]
    assert projection["outline_path"] not in \
        projection["active_document_candidates"]


def test_a_single_document_staged_topic_publishes_its_outline_and_no_candidates(
    tmp_path,
):
    """G-1 (PR #63 re-verification, 2026-08-02), as a fixture.

    Measured against the real corpus, 16 of 21 staged topics are THIS shape:
    exactly one editable path, which is the topic's own primary fragment, which
    doxBench loads as the OUTLINE. T104 F2 correctly excludes the outline from
    the document candidates (one file cannot be two independent working
    copies), so the candidate set is empty — and that is not a defect but the
    honest description of the tile. What it makes impossible is a turn that
    must NAME a document, which is why contract-v1.28 makes the request's
    `active_document_path` nullable, mirroring `buffer_state.path`."""
    projection = _server_projections(tmp_path)["single-document-staged"]
    assert projection["context_paths"] == [
        "ideation/staging/solo-topic/solo-topic.md"
    ]
    assert projection["editable_paths"] == [
        "ideation/staging/solo-topic/solo-topic.md"
    ]
    # the one editable path IS the outline, so it is not offered as a document
    assert projection["outline_path"] == (
        "ideation/staging/solo-topic/solo-topic.md"
    )
    assert projection["active_document_candidates"] == []


def test_empty_and_missing_scopes_are_honest(tmp_path):
    projections = _server_projections(tmp_path)
    assert projections["empty-staged"]["context_paths"] == []
    assert projections["empty-staged"]["editable_paths"] == []
    assert projections["empty-staged"]["outline_path"] is None
    assert projections["missing"] is None


@pytest.mark.parametrize(
    ("staging_id", "files", "expected"),
    [
        ("topic-x", ["nested/draft.md", "root.md", "topic-x.MD"], "topic-x.MD"),
        ("topic-x", ["nested/draft.md", "root.md"], "root.md"),
        ("topic-x", ["manifest.yaml", "notes.txt"], None),
        ("", ["b/second.md", "a/first.md"], "b/second.md"),
    ],
)
def test_primary_fragment_path_matches_the_existing_stable_rule(
    staging_id,
    files,
    expected,
):
    assert primary_fragment_path(staging_id, files) == expected


def test_resolver_refuses_snapshot_paths_that_escape_the_selected_root(tmp_path):
    snapshot = {
        "documents": [{"id": "bad", "path": "../outside.md"}],
        "clusters": [
            {
                "id": "cl-bad",
                "name": "Bad",
                "document_edges": [{"document": "bad"}],
            }
        ],
    }
    key = ScopeKey("fixture-repo", "main", "cluster", "cl-bad")

    with pytest.raises(ScopeConfinementError, match="outside the selected root"):
        resolve_scope(snapshot, key, source_root=tmp_path)


def test_resolver_refuses_absolute_and_session_created_escape_paths(tmp_path):
    fixture = _fixture()
    key = ScopeKey("fixture-repo", "main", "staged", "topic-x")

    with pytest.raises(ScopeConfinementError, match="repo-relative"):
        resolve_scope(
            fixture["snapshot"],
            key,
            source_root=tmp_path,
            created_paths=["/tmp/escape.md"],
        )
    with pytest.raises(ScopeConfinementError, match="outside the selected root"):
        resolve_scope(
            fixture["snapshot"],
            key,
            source_root=tmp_path,
            created_paths=["../escape.md"],
        )


def test_resolver_refuses_ambiguous_created_path_collections(tmp_path):
    fixture = _fixture()
    key = ScopeKey("fixture-repo", "main", "staged", "topic-x")

    with pytest.raises(ScopeConfinementError, match="created_paths"):
        resolve_scope(
            fixture["snapshot"],
            key,
            source_root=tmp_path,
            created_paths="ideation/staging/topic-x/new.md",
        )


def test_resolver_refuses_hidden_source_families_even_when_in_root(tmp_path):
    snapshot = {
        "documents": [{"id": "secret", "path": ".git/config"}],
        "clusters": [
            {
                "id": "cl-secret",
                "name": "Secret",
                "document_edges": [{"document": "secret"}],
            }
        ],
    }

    with pytest.raises(ScopeConfinementError, match="dot-directory"):
        resolve_scope(
            snapshot,
            ScopeKey("fixture-repo", "main", "cluster", "cl-secret"),
            source_root=tmp_path,
        )


def test_resolver_refuses_a_symlink_that_resolves_outside_the_selected_root(tmp_path):
    source_root = tmp_path / "source"
    outside = tmp_path / "outside.md"
    source_root.mkdir()
    outside.write_text("private\n", encoding="utf-8")
    (source_root / "link.md").symlink_to(outside)
    snapshot = {
        "documents": [{"id": "link.md", "path": "link.md"}],
        "clusters": [
            {
                "id": "cl-link",
                "name": "Link",
                "document_edges": [{"document": "link.md"}],
            }
        ],
    }

    with pytest.raises(ScopeConfinementError, match="outside the selected root"):
        resolve_scope(
            snapshot,
            ScopeKey("fixture-repo", "main", "cluster", "cl-link"),
            source_root=source_root,
        )


def test_resolution_is_deterministic_and_does_not_mutate_the_snapshot(tmp_path):
    fixture = _fixture()
    snapshot = fixture["snapshot"]
    before = copy.deepcopy(snapshot)
    key = ScopeKey("fixture-repo", "main", "staged", "topic-x")

    first = resolve_scope(snapshot, key, source_root=tmp_path)
    second = resolve_scope(snapshot, key, source_root=tmp_path)

    assert first == second
    assert snapshot == before


# ============================================================================
# T107 / FR-043: the SERVER-HELD created-in-session record
#
# The chat-turn route used to pass NO `created_paths` at all, so there was no
# created-in-session authority anywhere on the server and the overlay could only
# ever come from the browser's page-lifetime Map (`swb-session.js
# createdDocuments`) -- which is request content and therefore forgeable
# (security-privacy CHK012).
#
# The record these tests pin is the one the 007 predecessor ALREADY writes: a
# session `create-document` commits the new document AND its gate-action record
# into the session worktree as one commit (`gate_routes._create_document`), and
# that record names the document and the session branch. Nothing here invents a
# new store, and nothing here reads a request.
# ============================================================================

SESSION_BRANCH = "cluster/cl-alpha"
CREATED_DOC = "ideation/brainstorm/session-created.md"


def _write_created_record(worktree, document, *, branch=SESSION_BRANCH,
                          at="2026-07-30T12:00:00+00:00", action=None,
                          write_document=True):
    """One COMMITTED session `create-document` record, in the real shape.

    Built through `gate_console.build_gate_action_record` and filed at
    `gate_console.gate_action_record_relpath` rather than hand-rolled, so this
    test pins the record the route actually writes and cannot drift from it.
    """
    resolved_action = action or gate_console.ACTION_CREATE_DOCUMENT
    record = gate_console.build_gate_action_record(
        actor="brett",
        action=resolved_action,
        at=at,
        document=document,
        artifacts=[
            {"kind": gate_console.ART_DOCUMENT, "reference": document},
            branch_session.commit_artifact(branch_session.action_stamp(at)),
        ],
        ref=branch,
    )
    rel = gate_console.gate_action_record_relpath(
        gate_console.DEFAULT_RECORDS_DIR,
        record["action"],
        gate_console.document_target_id(document),
        record["at"],
    )
    path = Path(worktree) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
    if write_document:
        target = Path(worktree) / document
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("Status: brainstorm\n\n# created\n", encoding="utf-8")
    return record


class _FakeRegistry:
    """The registry surface the derivation reads, and nothing more.

    `keys()` + `get()` is exactly what `branch_session.live_session_branches` and
    `recorded_session_tile` ask for, and liveness IS the entry (FR-008) -- so a
    dict states liveness directly without opening a session, touching git, or
    writing anything.
    """

    def __init__(self, entries):
        self._entries = dict(entries)

    def keys(self):
        return list(self._entries)

    def get(self, repository, ref=None):
        if (repository, ref) not in self._entries:
            return None
        return SimpleNamespace(
            repository=repository,
            ref=ref,
            session_tile=self._entries[(repository, ref)],
        )


# ---- the PURE record filter -------------------------------------------------

def test_created_paths_from_records_reads_only_this_branchs_create_documents():
    records = [
        {"action": "create-document", "target": {"document": "a.md",
                                                 "ref": SESSION_BRANCH}},
        # another action on the same branch: an edit is not a create
        {"action": "edit-document", "target": {"document": "edited.md",
                                               "ref": SESSION_BRANCH}},
        # a create on ANOTHER branch's session
        {"action": "create-document", "target": {"document": "other.md",
                                                 "ref": "cluster/cl-beta"}},
        # a MAIN-resident pre-session create: no `ref` at all
        {"action": "create-document", "target": {"document": "main.md"}},
        # duplicate, and a shapeless entry
        {"action": "create-document", "target": {"document": "a.md",
                                                 "ref": SESSION_BRANCH}},
        "not a record",
        {"action": "create-document", "target": {"ref": SESSION_BRANCH}},
    ]

    assert created_paths_from_records(records, branch=SESSION_BRANCH) == ("a.md",)


def test_created_paths_from_records_is_empty_without_a_branch():
    records = [{"action": "create-document",
                "target": {"document": "a.md", "ref": SESSION_BRANCH}}]

    assert created_paths_from_records(records, branch="") == ()


# ---- the thin worktree reader ----------------------------------------------

def test_session_created_paths_reads_the_committed_record_in_the_worktree(tmp_path):
    _write_created_record(tmp_path, CREATED_DOC)

    assert session_created_paths(tmp_path, SESSION_BRANCH) == (CREATED_DOC,)


def test_session_created_paths_is_empty_with_no_records_tree(tmp_path):
    assert session_created_paths(tmp_path, SESSION_BRANCH) == ()


def test_session_created_paths_ignores_another_branchs_session_record(tmp_path):
    _write_created_record(tmp_path, CREATED_DOC, branch="cluster/cl-beta")

    assert session_created_paths(tmp_path, SESSION_BRANCH) == ()


def test_session_created_paths_ignores_non_create_actions(tmp_path):
    _write_created_record(tmp_path, CREATED_DOC,
                          action=gate_console.ACTION_EDIT_DOCUMENT)

    assert session_created_paths(tmp_path, SESSION_BRANCH) == ()


def test_session_created_paths_drops_a_record_whose_document_is_gone(tmp_path):
    """A path that is not readable cannot be chat-eligible.

    Dropped rather than raised: the record is SERVER-held, and one stale record
    must not refuse every turn on the tile.
    """
    _write_created_record(tmp_path, CREATED_DOC, write_document=False)

    assert session_created_paths(tmp_path, SESSION_BRANCH) == ()


def test_session_created_paths_drops_an_escaping_or_unsafe_recorded_path(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    (tmp_path / "outside.md").write_text("private\n", encoding="utf-8")
    for document in ("../outside.md", "/etc/passwd", ".git/config"):
        _write_created_record(worktree, document, write_document=False)

    assert session_created_paths(worktree, SESSION_BRANCH) == ()


def test_session_created_paths_survives_a_malformed_record(tmp_path):
    _write_created_record(tmp_path, CREATED_DOC)
    broken = (Path(tmp_path) / gate_console.DEFAULT_RECORDS_DIR
              / "broken" / "create-document-20260730.gate-action.yaml")
    broken.parent.mkdir(parents=True, exist_ok=True)
    broken.write_text("this: [is: not: yaml\n", encoding="utf-8")

    assert session_created_paths(tmp_path, SESSION_BRANCH) == (CREATED_DOC,)


def test_session_created_paths_is_ordered_by_creation_stamp(tmp_path):
    _write_created_record(tmp_path, "ideation/brainstorm/second.md",
                          at="2026-07-30T12:00:02+00:00")
    _write_created_record(tmp_path, "ideation/brainstorm/first.md",
                          at="2026-07-30T12:00:01+00:00")

    assert session_created_paths(tmp_path, SESSION_BRANCH) == (
        "ideation/brainstorm/first.md",
        "ideation/brainstorm/second.md",
    )


# ---- the liveness-gated composition ----------------------------------------

def test_session_created_paths_for_scope_reads_a_live_session_branch(tmp_path):
    _write_created_record(tmp_path, CREATED_DOC)
    registry = _FakeRegistry({("fixture-repo", SESSION_BRANCH):
                              ("cluster", "cl-alpha")})
    key = ScopeKey("fixture-repo", SESSION_BRANCH, "cluster", "cl-alpha")

    assert session_created_paths_for_scope(
        registry, key, repository="fixture-repo", ref=SESSION_BRANCH,
        source_root=tmp_path,
    ) == (CREATED_DOC,)


def test_session_created_paths_for_scope_is_empty_on_main(tmp_path):
    """No live session for the scope -> empty, byte-identical to pre-T107."""
    _write_created_record(tmp_path, CREATED_DOC)
    registry = _FakeRegistry({("fixture-repo", "main"): None})
    key = ScopeKey("fixture-repo", "main", "cluster", "cl-alpha")

    assert session_created_paths_for_scope(
        registry, key, repository="fixture-repo", ref="main",
        source_root=tmp_path,
    ) == ()


def test_session_created_paths_for_scope_is_empty_without_a_registry_entry(tmp_path):
    """The branch and the worktree both exist; the registry does not know it.

    Neither a branch nor a worktree proves liveness on its own (D15), so a
    session that is not in the registry contributes nothing.
    """
    _write_created_record(tmp_path, CREATED_DOC)
    registry = _FakeRegistry({})
    key = ScopeKey("fixture-repo", SESSION_BRANCH, "cluster", "cl-alpha")

    assert session_created_paths_for_scope(
        registry, key, repository="fixture-repo", ref=SESSION_BRANCH,
        source_root=tmp_path,
    ) == ()


def test_session_created_paths_for_scope_refuses_another_tiles_session(tmp_path):
    """A live session recorded against a DIFFERENT tile is not this tile's."""
    _write_created_record(tmp_path, CREATED_DOC)
    registry = _FakeRegistry({("fixture-repo", SESSION_BRANCH):
                              ("cluster", "cl-beta")})
    key = ScopeKey("fixture-repo", SESSION_BRANCH, "cluster", "cl-alpha")

    assert session_created_paths_for_scope(
        registry, key, repository="fixture-repo", ref=SESSION_BRANCH,
        source_root=tmp_path,
    ) == ()


def test_session_created_paths_for_scope_requires_the_tiles_own_branch_family(tmp_path):
    """FR-002: a session branch is TILE-derived. A live entry on a branch that is
    not this tile's family member is not this tile's session, whatever it holds.
    """
    _write_created_record(tmp_path, CREATED_DOC, branch="cluster/cl-beta")
    registry = _FakeRegistry({("fixture-repo", "cluster/cl-beta"):
                              ("cluster", "cl-alpha")})
    key = ScopeKey("fixture-repo", "cluster/cl-beta", "cluster", "cl-alpha")

    assert session_created_paths_for_scope(
        registry, key, repository="fixture-repo", ref="cluster/cl-beta",
        source_root=tmp_path,
    ) == ()


def test_session_created_paths_for_scope_maps_staged_tiles_to_the_draft_namespace(
    tmp_path,
):
    branch = "draft/topic-x"
    document = "ideation/staging/topic-x/new.md"
    _write_created_record(tmp_path, document, branch=branch)
    registry = _FakeRegistry({("fixture-repo", branch):
                              (branch_session.STAGED_TOPIC, "topic-x")})
    key = ScopeKey("fixture-repo", branch, "staged", "topic-x")

    assert session_created_paths_for_scope(
        registry, key, repository="fixture-repo", ref=branch,
        source_root=tmp_path,
    ) == (document,)


def test_session_created_paths_for_scope_survives_a_registry_without_the_surface(
    tmp_path,
):
    _write_created_record(tmp_path, CREATED_DOC)
    key = ScopeKey("fixture-repo", SESSION_BRANCH, "cluster", "cl-alpha")

    assert session_created_paths_for_scope(
        None, key, repository="fixture-repo", ref=SESSION_BRANCH,
        source_root=tmp_path,
    ) == ()


def test_session_created_paths_for_scope_lands_in_both_projection_sets(tmp_path):
    """The end-to-end scope consequence FR-043 asks for, without a route."""
    fixture = _fixture()
    _write_created_record(tmp_path, CREATED_DOC)
    registry = _FakeRegistry({("fixture-repo", SESSION_BRANCH):
                              ("cluster", "cl-alpha")})
    key = ScopeKey("fixture-repo", SESSION_BRANCH, "cluster", "cl-alpha")

    created = session_created_paths_for_scope(
        registry, key, repository="fixture-repo", ref=SESSION_BRANCH,
        source_root=tmp_path,
    )
    projection = resolve_scope(
        fixture["snapshot"], key, source_root=tmp_path, created_paths=created,
    )

    assert CREATED_DOC in projection.context_paths
    assert CREATED_DOC in projection.editable_paths
    assert CREATED_DOC in projection.active_document_candidates
