"""Nightly snapshot-lane tests (openxFactory add-ideation-dashboard task 4.1).

The aggregation lane's contract: after the deterministic doc-health pass it
writes the CURRENT snapshot + a status artifact under
`health/ideation-dashboard/`, validates the render with the pinned validator
BEFORE publishing, and on ANY error reports SKIPPED (status artifact + log
line) with exit 0 — never a failure that could affect the deterministic run —
leaving the previously committed snapshot untouched. `source_revision` is the
pinned checkout's HEAD sha (injected here so the fixture tree is stable).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, find_openxfactory_validator

from ideation_dashboard import nightly_lane as lane

VALIDATOR = find_openxfactory_validator()

needs_validator = pytest.mark.skipif(
    VALIDATOR is None, reason="pinned openxFactory validator not reachable")


def _agg_root(tmp_path: Path) -> Path:
    """A miniature aggregation root: the fixture base-repo standing in as the
    pinned openxFactory checkout."""
    (tmp_path / "openxFactory").symlink_to(BASE_REPO, target_is_directory=True)
    return tmp_path


def _register(agg: Path) -> None:
    (agg / "project-register.yaml").write_text(
        "schema_version: 1\n"
        "kind: project-register\n"
        "projects:\n"
        "  - id: xfactory\n"
        "    name: xFactory\n"
        "    repositories: [fixture-repo]\n",
        encoding="utf-8")


# ---------------------------------------------------------------------------
# happy path: generate -> validate -> publish, status ok, register resolved
# ---------------------------------------------------------------------------

@needs_validator
def test_lane_publishes_a_validated_snapshot_with_ok_status(tmp_path):
    agg = _agg_root(tmp_path)
    _register(agg)
    out = lane.run_lane(agg, repository="fixture-repo",
                        source_revision=PINNED_REVISION, validator=VALIDATOR)
    assert out.ok and out.reason is None
    assert out.source_revision == PINNED_REVISION

    snap_path = agg / "health/ideation-dashboard/fixture-repo-snapshot.json"
    assert out.snapshot_path == snap_path
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    assert snap["repository"] == "fixture-repo"
    assert snap["generation"]["source_revision"] == PINNED_REVISION
    # the AGGREGATION-ROOT register was passed explicitly (D10 wiring): the
    # repository resolves through it, not through the fixture repo's own
    # discovery path.
    assert snap["project"] == "xfactory"

    status = json.loads(
        (agg / "health/ideation-dashboard/lane-status.json").read_text())
    assert status["result"] == "ok" and status["reason"] is None
    assert status["source_revision"] == PINNED_REVISION
    # Fix 2: the ok status carries the (empty, here) exclusion list and the
    # diagnostic stamps — the fixture corpus is well-formed, so nothing excluded
    assert status["excluded_documents"] == []
    assert status["detail"] == []
    assert status["generated_at"].endswith("Z")
    assert "run_id" in status  # None locally; the CI run id under Actions
    # the candidate render never lingers next to the published snapshot
    assert not snap_path.with_name(snap_path.name + ".candidate").exists()


@needs_validator
def test_lane_reruns_keep_a_byte_identical_snapshot_and_stable_status(tmp_path):
    agg = _agg_root(tmp_path)
    _register(agg)
    kwargs = {"repository": "fixture-repo",
              "source_revision": PINNED_REVISION, "validator": VALIDATOR}
    assert lane.run_lane(agg, **kwargs).ok
    snap_path = agg / "health/ideation-dashboard/fixture-repo-snapshot.json"
    status_path = agg / "health/ideation-dashboard/lane-status.json"
    first_snap = snap_path.read_bytes()
    first_status = json.loads(status_path.read_text())
    assert lane.run_lane(agg, **kwargs).ok
    # the SNAPSHOT is byte-identical per pin state (the determinism contract)
    assert snap_path.read_bytes() == first_snap
    # the status is identical too, except its diagnostic wall-clock stamp
    second_status = json.loads(status_path.read_text())
    for s in (first_status, second_status):
        s.pop("generated_at")
    assert second_status == first_status


@needs_validator
def test_missing_register_is_legal_and_renders_ungrouped(tmp_path):
    agg = _agg_root(tmp_path)  # no project-register.yaml at the agg root
    out = lane.run_lane(agg, repository="not-in-any-register",
                        source_revision=PINNED_REVISION, validator=VALIDATOR)
    assert out.ok
    snap = json.loads(out.snapshot_path.read_text(encoding="utf-8"))
    assert "project" not in snap  # ungrouped implicit project (D10)


# ---------------------------------------------------------------------------
# failure isolation: any error -> SKIPPED, exit 0, previous snapshot untouched
# ---------------------------------------------------------------------------

def test_generator_error_is_reported_skipped_and_keeps_the_previous_snapshot(tmp_path):
    agg = _agg_root(tmp_path)
    out_dir = agg / "health/ideation-dashboard"
    out_dir.mkdir(parents=True)
    previous = out_dir / "fixture-repo-snapshot.json"
    previous.write_text('{"previous": "good"}\n', encoding="utf-8")

    def boom(*args, **kwargs):
        raise RuntimeError("generator exploded")

    out = lane.run_lane(agg, repository="fixture-repo",
                        source_revision=PINNED_REVISION, generate=boom)
    assert not out.ok
    assert "generator exploded" in out.reason
    # the previously committed snapshot is still the current one
    assert previous.read_text(encoding="utf-8") == '{"previous": "good"}\n'
    status = json.loads((out_dir / "lane-status.json").read_text())
    assert status["result"] == "skipped"
    assert "generator exploded" in status["reason"]
    assert status["source_revision"] == PINNED_REVISION


@needs_validator
def test_a_rejected_render_is_never_published(tmp_path):
    agg = _agg_root(tmp_path)
    out_dir = agg / "health/ideation-dashboard"

    def bad_generate(*args, **kwargs):
        # schema-invalid on purpose: required snapshot fields are missing
        return {"schema_version": 1, "kind": "ideation-dashboard-snapshot"}

    out = lane.run_lane(agg, repository="fixture-repo",
                        source_revision=PINNED_REVISION,
                        generate=bad_generate, validator=VALIDATOR)
    assert not out.ok
    assert "pinned validator" in out.reason
    assert not (out_dir / "fixture-repo-snapshot.json").exists()
    assert not (out_dir / "fixture-repo-snapshot.json.candidate").exists()
    status = json.loads((out_dir / "lane-status.json").read_text())
    assert status["result"] == "skipped"
    # Fix 2: the validator's per-error diagnosis is retained, not discarded —
    # the one-line reason is no longer the whole record.
    assert isinstance(status["detail"], list) and status["detail"]
    assert any("required property" in line for line in status["detail"])
    assert len(status["detail"]) <= 50
    assert status["generated_at"].endswith("Z")
    assert "run_id" in status


def test_an_unrunnable_validator_skips_without_blaming_the_snapshot(tmp_path):
    """The lane's DECISION is right and unchanged — it publishes to a location
    others read, so a snapshot nobody checked must not land there, exactly as
    when no validator is found at all. Its DIAGNOSIS was wrong: "snapshot
    rejected by the pinned validator" over a lane host that simply lacks
    `jsonschema` sends whoever reads lane-status.json hunting a corpus defect
    that does not exist, when the fix is one pip install on the host.

    No `@needs_validator`: the point is a validator that cannot run, so the stub
    IS the fixture."""
    agg = _agg_root(tmp_path)
    _register(agg)
    stub = tmp_path / "deps-missing.py"
    stub.write_text("import sys\n"
                    "print('ERROR jsonschema>=4.18 and referencing are required',"
                    " file=sys.stderr)\nsys.exit(2)\n", encoding="utf-8")

    out = lane.run_lane(agg, repository="fixture-repo",
                        source_revision=PINNED_REVISION, validator=stub)

    assert not out.ok
    assert "could NOT RUN" in out.reason, out.reason
    assert "pip install 'jsonschema>=4.18' referencing" in out.reason, out.reason
    assert "rejected" not in out.reason, out.reason
    out_dir = agg / "health/ideation-dashboard"
    assert not (out_dir / "fixture-repo-snapshot.json").exists()
    status = json.loads((out_dir / "lane-status.json").read_text())
    assert status["result"] == "skipped"


@needs_validator
def test_headerless_doc_no_longer_doses_the_lane_and_is_reported(tmp_path):
    # The reproduced defect (openxFactory 7bb6c4e, nightly run 29330008234): a
    # doc lacking a Status: header made the generator emit stage:null and the
    # pinned validator reject the whole snapshot, skipping the entire lane. The
    # generator now degrades per-document, so the lane PUBLISHES and reports the
    # excluded doc on the ok outcome.
    ox = tmp_path / "openxFactory"
    (ox / "ideation/brainstorm").mkdir(parents=True)
    (ox / "ideation/brainstorm/good.md").write_text(
        "Status: brainstorm\nTopics: alpha\n\nbody\n", encoding="utf-8")
    (ox / "ideation/brainstorm/headerless.md").write_text(
        "# no header\n\nprose\n", encoding="utf-8")

    out = lane.run_lane(tmp_path, repository="fixture-repo",
                        source_revision=PINNED_REVISION, validator=VALIDATOR)
    assert out.ok, out.reason
    status = json.loads(
        (tmp_path / "health/ideation-dashboard/lane-status.json").read_text())
    assert status["result"] == "ok"
    assert status["excluded_documents"] == [
        {"path": "ideation/brainstorm/headerless.md",
         "reason": "missing or unparseable Status: header"}]
    assert status["generated_at"].endswith("Z")
    snap = json.loads(out.snapshot_path.read_text(encoding="utf-8"))
    assert {d["path"] for d in snap["documents"]} == {"ideation/brainstorm/good.md"}


def test_missing_checkout_is_skipped(tmp_path):
    out = lane.run_lane(tmp_path)  # no openxFactory dir at all
    assert not out.ok and "pinned checkout not found" in out.reason


def test_unresolvable_head_is_skipped(tmp_path):
    (tmp_path / "openxFactory").mkdir()  # a directory, but not a git checkout
    out = lane.run_lane(tmp_path)
    assert not out.ok and "HEAD" in out.reason


def test_main_never_fails_when_the_lane_skips(tmp_path, capsys):
    # The CLI surface the nightly invokes: main is void and never raises (so
    # the process exits 0) even on total failure, with the skip reported on
    # stdout and in the status artifact.
    assert lane.main(["--repo-root", str(tmp_path)]) is None
    assert "SKIPPED" in capsys.readouterr().out
    status = json.loads(
        (tmp_path / "health/ideation-dashboard/lane-status.json").read_text())
    assert status["result"] == "skipped"


@needs_validator
def test_main_never_fails_on_the_happy_path(tmp_path, capsys):
    agg = _agg_root(tmp_path)
    _register(agg)
    assert lane.main(["--repo-root", str(agg), "--repository", "fixture-repo",
                      "--source-revision", PINNED_REVISION,
                      "--validator", str(VALIDATOR)]) is None
    assert "ideation-dashboard lane: OK" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# per-repository iteration + the snapshot INDEX
# (add-dashboard-repo-selector task 3.1; verification 5.2)
# ---------------------------------------------------------------------------

def _copy_git_fixture(destination: Path) -> None:
    shutil.copytree(BASE_REPO, destination)
    subprocess.run(
        ["git", "init", "-q", "-b", "main", str(destination)],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "add", "."],
        check=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(destination),
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "fixture",
        ],
        check=True,
    )


def _multi_agg_root(tmp_path: Path) -> Path:
    """An aggregation root with TWO repositories — one at the top level, one
    under `xFactories/` reachable only through `.gitmodules` — plus a register
    that declares both by id (the roster, design D9)."""
    _copy_git_fixture(tmp_path / "alpha")
    (tmp_path / "xFactories").mkdir()
    _copy_git_fixture(tmp_path / "xFactories" / "beta")
    (tmp_path / ".gitmodules").write_text(
        '[submodule "alpha"]\n\tpath = alpha\n\turl = git@example.invalid:alpha.git\n'
        '[submodule "beta"]\n\tpath = xFactories/beta\n\turl = git@example.invalid:beta.git\n',
        encoding="utf-8")
    (tmp_path / "project-register.yaml").write_text(
        "schema_version: 1\n"
        "kind: project-register\n"
        "projects:\n"
        "  - id: xfactory\n"
        "    repositories: [alpha, beta]\n",
        encoding="utf-8")
    return tmp_path


def test_submodule_paths_and_checkout_resolution(tmp_path):
    agg = _multi_agg_root(tmp_path)
    assert lane.submodule_paths(agg) == {"alpha": "alpha", "beta": "xFactories/beta"}
    assert lane.resolve_checkout(agg, "alpha") == "alpha"
    assert lane.resolve_checkout(agg, "beta") == "xFactories/beta"
    assert lane.resolve_checkout(agg, "gamma") is None  # never guessed


def test_registered_repositories_is_the_register_roster(tmp_path):
    agg = _multi_agg_root(tmp_path)
    assert lane.registered_repositories(agg) == ["alpha", "beta"]
    assert lane.registered_repositories(tmp_path / "nowhere") == []


@needs_validator
def test_multi_lane_publishes_a_snapshot_per_repository_plus_the_index(tmp_path):
    agg = _multi_agg_root(tmp_path)
    out = lane.run_multi_lane(agg, validator=VALIDATOR, aggregate_id="xFactory")
    assert [o.ok for o in out.outcomes] == [True, True]
    published = agg / "health/ideation-dashboard"
    assert (published / "alpha-snapshot.json").is_file()
    assert (published / "beta-snapshot.json").is_file()

    index = json.loads((published / "index.json").read_text(encoding="utf-8"))
    assert index["kind"] == "ideation-dashboard-snapshot-index"
    assert [(e["repository"], e["ref"], e["snapshot"]) for e in index["entries"]] == [
        ("alpha", "main", "alpha-snapshot.json"),
        ("beta", "main", "beta-snapshot.json")]
    assert all(e["source_revision"] for e in index["entries"])
    # the composed view names its members and carries no projection of its own
    assert index["aggregates"][0]["id"] == "xFactory"
    assert index["aggregates"][0]["members"] == [
        {"repository": "alpha", "ref": "main"}, {"repository": "beta", "ref": "main"}]
    for forbidden in ("documents", "clusters", "possibles", "keyword_index"):
        assert forbidden not in index

    status = json.loads((published / "index-status.json").read_text(encoding="utf-8"))
    assert status["result"] == "ok"
    assert [p["repository"] for p in status["published"]] == ["alpha", "beta"]
    assert status["skipped"] == []


@needs_validator
def test_multi_lane_publishes_a_complete_named_aggregate_subset(tmp_path):
    agg = _multi_agg_root(tmp_path)
    lane.run_multi_lane(
        agg,
        validator=VALIDATOR,
        aggregate_id="medx-clinical",
        aggregate_members=["beta"],
        aggregate_display_name="Medx clinical",
    )

    index = json.loads(
        (agg / "health/ideation-dashboard/index.json").read_text(encoding="utf-8"))
    assert [entry["repository"] for entry in index["entries"]] == ["alpha", "beta"]
    assert index["aggregates"] == [{
        "id": "medx-clinical",
        "display_name": "Medx clinical",
        "members": [{"repository": "beta", "ref": "main"}],
    }]


@needs_validator
def test_multi_lane_omits_an_incomplete_named_aggregate_subset(tmp_path):
    agg = _multi_agg_root(tmp_path)
    lane.run_multi_lane(
        agg,
        validator=VALIDATOR,
        aggregate_id="medx-clinical",
        aggregate_members=["alpha", "ghost"],
    )

    index = json.loads(
        (agg / "health/ideation-dashboard/index.json").read_text(encoding="utf-8"))
    assert "aggregates" not in index


@needs_validator
def test_multi_lane_skips_an_unresolvable_repository_without_failing_the_run(tmp_path):
    agg = _multi_agg_root(tmp_path)
    out = lane.run_multi_lane(agg, repositories=["alpha", "ghost"], validator=VALIDATOR)
    assert out.published and len(out.published) == 1
    index = json.loads((agg / "health/ideation-dashboard/index.json").read_text())
    assert [e["repository"] for e in index["entries"]] == ["alpha"]
    status = json.loads((agg / "health/ideation-dashboard/index-status.json").read_text())
    assert status["skipped"] == [{"repository": "ghost", "reason": "checkout not found"}]


def test_multi_lane_with_nothing_publishable_skips_the_index(tmp_path):
    out = lane.run_multi_lane(tmp_path, repositories=["ghost"])
    assert out.index_path is None
    status = json.loads((tmp_path / "health/ideation-dashboard/index-status.json").read_text())
    assert status["result"] == "skipped"
    assert status["reason"] == "no repository snapshot was published"


@needs_validator
def test_multi_lane_cli_never_fails_the_nightly(tmp_path, capsys):
    agg = _multi_agg_root(tmp_path)
    assert lane.main(["--repo-root", str(agg), "--repositories", "registered",
                      "--validator", str(VALIDATOR)]) is None
    out = capsys.readouterr().out
    assert "2/2 repository snapshot(s) published" in out


@needs_validator
def test_multi_lane_cli_accepts_an_explicit_aggregate_subset(tmp_path):
    agg = _multi_agg_root(tmp_path)
    assert lane.main([
        "--repo-root", str(agg),
        "--repositories", "registered",
        "--validator", str(VALIDATOR),
        "--aggregate", "medx-clinical",
        "--aggregate-members", "beta",
        "--aggregate-display-name", "Medx clinical",
    ]) is None
    index = json.loads(
        (agg / "health/ideation-dashboard/index.json").read_text(encoding="utf-8"))
    assert index["aggregates"][0]["members"] == [
        {"repository": "beta", "ref": "main"}]
    assert (agg / "health/ideation-dashboard/index.json").is_file()


def test_reusable_nightly_publishes_the_registered_repository_index():
    workflow = (
        Path(__file__).resolve().parents[2]
        / ".github/workflows/doc-health-reusable.yml"
    ).read_text(encoding="utf-8")
    command = (
        "python3 openxFactory/scripts/ideation-dashboard-nightly.py "
        "\\\n            --repo-root . \\\n"
        "            --repositories registered"
    )
    assert command in workflow
    assert "--aggregate medx-clinical" in workflow
    assert "--aggregate-members MedxFactory,openChart,MedxEHR,HealthLinc" in workflow
    assert '--aggregate-display-name "Medx clinical"' in workflow
