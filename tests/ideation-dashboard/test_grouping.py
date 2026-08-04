"""US3 project grouping roll-ups (T014-T016, change 3.8):

  * T014's generator-side `repository` -> `project` -> `project_group`
    resolution was already delivered at T006 (wave 2, `register.py`'s
    ProjectRegisterAdapter) and is already covered by
    `test_generator.py::test_project_grouping_resolves_from_the_register` /
    `test_unregistered_repository_renders_ungrouped`. This file adds the
    MULTI-repo aggregation case those single-snapshot tests don't reach, plus
    the pure `buildGroupingModel` roll-up derivation in
    `web/views/grouping.js`, run in node against real generated snapshots
    exactly like test_renderer.py's model.js harness;
  * the doctored-snapshot technique (same base-repo fixture tree, different
    `repository=` labels) is the same one
    `test_unregistered_repository_renders_ungrouped` already uses — the
    fixture `project-register.yaml` already maps `fixture-repo` ->
    `fixture-core`, and `fixture-repo-b`/`fixture-repo-c` -> `fixture-siblings`,
    both -> `fixture-family` (see tests/ideation-dashboard/fixtures/base-repo/
    project-register.yaml), so no new on-disk fixture is needed for the
    multi-repo scenarios;
  * wiring assertions (grep-based, matching test_renderer.py's asset-integrity
    style) confirm the roll-up is mounted on the funnel, pipeline board, and
    stats strip, and that it issues no fetch of its own (snapshot-only,
    already-loaded data — the "no new fetch" rule)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import textwrap

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit  # noqa: F401

from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
GROUPING_JS = WEB / "views" / "grouping.js"
NODE = shutil.which("node")


def _snap(repository, **over):
    kwargs = {"source_revision": PINNED_REVISION, "git": FakeGit()}
    kwargs.update(over)
    return generate_snapshot(BASE_REPO, repository, **kwargs)


_HARNESS = """
import { buildGroupingModel } from './grouping.mjs';
import { readFileSync } from 'node:fs';
const snaps = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(buildGroupingModel(snaps)));
"""


def _run_node_grouping(snapshots, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(GROUPING_JS, tmp_path / "grouping.mjs")
    (tmp_path / "harness.mjs").write_text(_HARNESS, encoding="utf-8")
    snaps_path = tmp_path / "snapshots.json"
    snaps_path.write_text(json.dumps(snapshots), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "harness.mjs"), str(snaps_path)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ----------------------------------------------------------------------------
# single-repo v1 reality: resolved project/group, and the absent-fields
# fallback — both MUST render, never fail (spec edge case)
# ----------------------------------------------------------------------------

def test_single_repo_with_resolved_project_renders_under_its_project(tmp_path):
    snap = _snap("fixture-repo")
    model = _run_node_grouping([snap], tmp_path)
    assert [p["label"] for p in model["projects"]] == ["fixture-core"]
    assert model["projects"][0]["implicit"] is False
    assert [g["label"] for g in model["groups"]] == ["fixture-family"]
    assert model["ungroupedProjects"] == []
    # a single repo's project tallies mirror its own snapshot counts exactly
    assert model["projects"][0]["tallies"]["documents"] == len(snap["documents"])
    assert model["projects"][0]["tallies"]["clusters"] == len(snap["clusters"])


def test_unregistered_repository_renders_as_its_own_implicit_project(tmp_path):
    snap = _snap("not-registered")
    assert "project" not in snap and "project_group" not in snap
    model = _run_node_grouping([snap], tmp_path)
    assert len(model["projects"]) == 1
    proj = model["projects"][0]
    assert proj["implicit"] is True
    assert proj["id"] is None
    assert proj["label"] == "not-registered"
    assert proj["projectGroup"] is None
    assert model["groups"] == []
    assert [p["label"] for p in model["ungroupedProjects"]] == ["not-registered"]
    # never a failure: the same tally shape as a registered repo
    assert proj["tallies"]["documents"] == len(snap["documents"])


# ----------------------------------------------------------------------------
# multi-repo project aggregation (fixture-repo-b/-c share fixture-siblings)
# ----------------------------------------------------------------------------

def test_multi_repo_project_aggregates_member_repositories_under_one_heading(tmp_path):
    snap_b = _snap("fixture-repo-b")
    snap_c = _snap("fixture-repo-c")
    model = _run_node_grouping([snap_b, snap_c], tmp_path)
    assert [p["label"] for p in model["projects"]] == ["fixture-siblings"]
    siblings = model["projects"][0]
    assert {r["repository"] for r in siblings["repositories"]} == {"fixture-repo-b", "fixture-repo-c"}
    # aggregate tallies SUM the member repositories' own counts, never re-derived
    assert siblings["tallies"]["documents"] == 2 * len(snap_b["documents"])
    assert siblings["tallies"]["clusters"] == 2 * len(snap_b["clusters"])
    assert siblings["tallies"]["possibles"] == 2 * len(snap_b["possibles"])


def test_per_repository_detail_reachable_beneath_the_project(tmp_path):
    # US3 independent test: "per-repository detail reachable beneath" — the
    # project's own `repositories` list carries each member's UNAGGREGATED
    # tallies, so per-repo detail never disappears once rolled up.
    snap_b = _snap("fixture-repo-b")
    snap_c = _snap("fixture-repo-c")
    model = _run_node_grouping([snap_b, snap_c], tmp_path)
    siblings = model["projects"][0]
    assert len(siblings["repositories"]) == 2
    by_repo = {r["repository"]: r for r in siblings["repositories"]}
    assert by_repo["fixture-repo-b"]["tallies"]["documents"] == len(snap_b["documents"])
    assert by_repo["fixture-repo-c"]["tallies"]["documents"] == len(snap_c["documents"])


# ----------------------------------------------------------------------------
# group tallies aggregate ALL member projects' repositories
# ----------------------------------------------------------------------------

def test_group_tallies_aggregate_all_member_projects(tmp_path):
    snap_a = _snap("fixture-repo")
    snap_b = _snap("fixture-repo-b")
    snap_c = _snap("fixture-repo-c")
    model = _run_node_grouping([snap_a, snap_b, snap_c], tmp_path)
    assert [g["label"] for g in model["groups"]] == ["fixture-family"]
    family = model["groups"][0]
    assert {p["label"] for p in family["projects"]} == {"fixture-core", "fixture-siblings"}
    archived = len([c for c in snap_a["changes"] if c["status"] == "archived"])
    active = len([c for c in snap_a["changes"] if c["status"] == "active"])
    assert family["tallies"]["documents"] == 3 * len(snap_a["documents"])
    assert family["tallies"]["changes_archived"] == 3 * archived
    assert family["tallies"]["changes_active"] == 3 * active


def test_group_view_also_surfaces_ungrouped_projects_alongside_groups(tmp_path):
    # A group-scoped roll-up must not hide a repository that has no group —
    # it renders standalone (spec edge case: absence is never a failure).
    model = _run_node_grouping([_snap("fixture-repo"), _snap("not-registered")], tmp_path)
    assert [g["label"] for g in model["groups"]] == ["fixture-family"]
    assert [p["label"] for p in model["ungroupedProjects"]] == ["not-registered"]


# ----------------------------------------------------------------------------
# register-edit-requires-regeneration: the roll-up reads ONLY what the
# generator already resolved into each snapshot; it never re-reads the
# project register itself (spec US3 acceptance scenario 4).
# ----------------------------------------------------------------------------

def test_grouping_reflects_only_the_already_generated_snapshot_not_a_live_register(tmp_path):
    # The roll-up model has no path to the project register at all —
    # `buildGroupingModel` only ever sees whatever `project`/`project_group`
    # fields are already baked into the snapshot(s) it is handed.  Grouping
    # changes only when a NEW snapshot is generated against the edited
    # register, never for an already-generated snapshot object still in hand.
    before_dir = tmp_path / "before"
    after_dir = tmp_path / "after"
    before_dir.mkdir()
    after_dir.mkdir()

    edited_register = tmp_path / "project-register.yaml"
    edited_register.write_text(textwrap.dedent("""\
        schema_version: 1
        kind: project-register
        projects:
          - id: edited-project
            name: Edited project
            repositories: [fixture-repo]
        project_groups: []
        """), encoding="utf-8")

    original = _snap("fixture-repo")
    regenerated = _snap("fixture-repo", project_register_source=edited_register)
    assert original["project"] == "fixture-core"
    assert regenerated["project"] == "edited-project"

    before = _run_node_grouping([original], before_dir)
    after = _run_node_grouping([regenerated], after_dir)
    assert before["projects"][0]["label"] == "fixture-core"
    assert after["projects"][0]["label"] == "edited-project"


# ----------------------------------------------------------------------------
# wiring: the roll-up is actually mounted on the funnel, pipeline board, and
# stats strip (change 3.8) — and it fetches nothing of its own.
# ----------------------------------------------------------------------------

def test_grouping_js_exists_and_is_importable_standalone():
    assert GROUPING_JS.is_file()
    text = GROUPING_JS.read_text(encoding="utf-8")
    assert "export function buildGroupingModel" in text
    assert "export function renderGroupingBar" in text
    assert "fetch(" not in text


def test_rollup_mounts_once_in_the_header_only():
    # v3 sweep (register #17): the roll-up used to mount THREE times — once in
    # the header and again inside funnel.js and board.js — stacking duplicate
    # bars on those two tabs. It now mounts exactly ONCE, in the header, and the
    # per-view mounts (and their grouping.js import) are gone.
    funnel = (WEB / "views" / "funnel.js").read_text(encoding="utf-8")
    board = (WEB / "views" / "board.js").read_text(encoding="utf-8")
    app = (WEB / "app.js").read_text(encoding="utf-8")
    index_html = (WEB / "index.html").read_text(encoding="utf-8")

    # the single header mount survives
    assert 'import { renderGroupingBar } from "./views/grouping.js"' in app
    assert 'renderGroupingBar(document.getElementById("rollup")' in app
    assert 'id="rollup"' in index_html

    # the duplicate per-view mounts are removed
    assert "renderGroupingBar(" not in funnel
    assert "grouping.js" not in funnel
    assert "renderGroupingBar(" not in board
    assert "grouping.js" not in board


def test_grouping_bar_aggregates_an_array_not_a_single_snapshot():
    # Multi-repo readiness (spec): the exported render entrypoint takes a
    # LIST, even though every current call site passes a single-element array.
    text = GROUPING_JS.read_text(encoding="utf-8")
    assert re.search(r"export function renderGroupingBar\(root, snapshots", text)
    assert re.search(r"export function buildGroupingModel\(snapshots\)", text)


def test_no_new_fetch_introduced_by_grouping():
    # Extends test_renderer.py's asset-integrity rule locally: grouping.js
    # itself must never fetch — it only aggregates already-loaded snapshot(s).
    for path in [WEB / "views" / "grouping.js"]:
        assert "fetch(" not in path.read_text(encoding="utf-8")
