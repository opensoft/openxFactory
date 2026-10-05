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


@needs_validator
def test_the_default_validator_is_the_products_own_never_an_enclosing_copy(tmp_path):
    """With no `validator=`, the lane validates with the openxdox product's OWN
    validator, composed runnable, and publishes. It used to ask
    `find_validator(agg_root)`, a walk up for
    `openxFactory/scripts/validate-ideation-dashboard-contracts.py`. That file
    was shed at `cc4ae9d3`. From openXdox-code `e28930bf` on, the locator
    confines to the product's own tree, so that call could never find anything
    (split-opendox-two-layer-product § 8.9 residue (iii)).

    The decoy is that defect class itself: a stale pre-shed copy one level up,
    exactly where the old walk looked, which rejects everything. Adopting it
    would skip the lane with "snapshot rejected"."""
    outer = tmp_path / "outer"
    decoy = (outer / "openxFactory" / "scripts"
             / "validate-ideation-dashboard-contracts.py")
    decoy.parent.mkdir(parents=True)
    decoy.write_text("import sys\nprint('ERROR decoy adopted')\nsys.exit(1)\n",
                     encoding="utf-8")
    (outer / "agg").mkdir()
    agg = _agg_root(outer / "agg")
    _register(agg)

    out = lane.run_lane(agg, repository="fixture-repo",
                        source_revision=PINNED_REVISION)

    assert out.ok, out.reason
    assert (agg / "health/ideation-dashboard/fixture-repo-snapshot.json").is_file()


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


def test_a_product_without_its_validator_skips_naming_the_product_tree(
        tmp_path, monkeypatch):
    """The skip names the one place the default is looked for, the openxdox
    product's own tree. It never names the aggregation root, which is no longer
    searched. No `@needs_validator`: the point is a product that has none."""
    agg = _agg_root(tmp_path)
    _register(agg)
    monkeypatch.setattr(lane.snapshot_mod, "find_validator",
                        lambda start=None: None)

    out = lane.run_lane(agg, repository="fixture-repo",
                        source_revision=PINNED_REVISION)

    assert not out.ok
    assert out.reason.startswith("pinned openxdox validator not found ("), \
        out.reason
    assert str(agg) not in out.reason, out.reason
    assert not (agg / "health/ideation-dashboard/fixture-repo-snapshot.json").exists()


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


def test_main_is_skipped_rather_than_raised_when_registration_fails(
        tmp_path, capsys, monkeypatch):
    """§ 4.3/§ 4.4 widened `main()` to register the domain profile before
    anything else runs (Copilot review, PR #984): a missing leg, a malformed
    profile, or a registration conflict must not escape as an uncaught
    exception, because this function's own contract (its docstring) is that
    EVERY error is a SKIP at exit 0 — never a nonzero exit. This runs BEFORE
    `run_lane()`'s own try/except, so it needs its own, proven here directly
    against `register_openxfactory()` rather than against a leg genuinely
    missing (which the rest of this suite cannot simulate: `tests/ideation-
    dashboard/conftest.py` already registered the real profile for the whole
    session before this test runs).

    Second round (Copilot review, PR #984, thread on this SKIP path): the
    failure must ALSO be recorded in `lane-status.json`, the same as every
    other SKIP this lane produces — a print alone left a missing/malformed
    leg with no current status artifact for a consumer that only reads the
    file, and the previous run's artifact (or none at all) looked current."""
    import opendox_host

    def _boom():
        raise RuntimeError("simulated registration failure")

    monkeypatch.setattr(opendox_host, "register_openxfactory", _boom)
    assert lane.main(["--repo-root", str(tmp_path)]) is None
    out = capsys.readouterr().out
    assert "ideation-dashboard lane: SKIPPED" in out
    assert "RuntimeError" in out
    assert "simulated registration failure" in out
    status = json.loads(
        (tmp_path / "health/ideation-dashboard/lane-status.json").read_text())
    assert status["result"] == "skipped"
    assert "RuntimeError" in status["reason"]
    assert "simulated registration failure" in status["reason"]
    assert status["repository"] == lane.DEFAULT_REPOSITORY


def test_main_registration_failure_writes_index_status_for_repositories_mode(
        tmp_path, capsys, monkeypatch):
    """The same registration guard, requested through `--repositories` — the
    form BOTH real production call sites use (`scripts/reserve-dashboard.sh`
    and `.github/workflows/doc-health-reusable.yml` each always pass
    `--repositories registered`): the artifact a consumer of THIS mode reads
    is `index-status.json`, not `lane-status.json`, so the failure must land
    there instead. No project register or repository checkout is needed —
    registration fails before `run_multi_lane()` is ever reached, so no
    repository is ever resolved."""
    import opendox_host

    def _boom():
        raise RuntimeError("simulated registration failure")

    monkeypatch.setattr(opendox_host, "register_openxfactory", _boom)
    assert lane.main(["--repo-root", str(tmp_path),
                      "--repositories", "registered"]) is None
    out = capsys.readouterr().out
    assert "ideation-dashboard lane: SKIPPED" in out
    assert not (tmp_path / "health/ideation-dashboard/lane-status.json").exists()
    status = json.loads(
        (tmp_path / "health/ideation-dashboard/index-status.json").read_text())
    assert status["result"] == "skipped"
    assert "RuntimeError" in status["reason"]
    assert "simulated registration failure" in status["reason"]
    assert status["published"] == []
    assert status["skipped"] == []


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


# ---------------------------------------------------------------------------
# openxFactory #1208: a checkout is used only when it is POPULATED, and a
# register id reaches the nested product legs through the `.gitmodules` of
# the checkouts the workspace declares. The nightly initialises only
# `^(openxFactory|xFactories/)` plus openxFactory's nested openDox/openXdox
# and their legs, so every other declared submodule is an EMPTY directory
# inside the aggregation's work tree, and `git rev-parse HEAD` there answers
# the aggregation's own head.
# ---------------------------------------------------------------------------

def _commit_repo(path: Path, gitmodules: str | None = None) -> Path:
    """`git init` plus one commit at `path`, optionally declaring
    `.gitmodules` (read from the work tree, as the lane reads it)."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(path)], check=True)
    if gitmodules is not None:
        (path / ".gitmodules").write_text(gitmodules, encoding="utf-8")
        subprocess.run(["git", "-C", str(path), "add", ".gitmodules"], check=True)
    subprocess.run(
        ["git", "-C", str(path), "-c", "user.name=Fixture",
         "-c", "user.email=fixture@example.invalid",
         "commit", "-q", "--allow-empty", "-m", "fixture"],
        check=True,
    )
    return path


def _never_generate(*args, **kwargs):
    raise AssertionError("the generator must not run over an uninitialised checkout")


def test_an_uninitialised_submodule_directory_is_skipped_never_published(tmp_path):
    agg = _commit_repo(tmp_path / "agg")
    (agg / "openxFactory").mkdir()  # declared, never initialised: empty
    # The hazard the fixture reproduces: git walks up out of the empty
    # directory and answers the AGGREGATION's head.
    assert lane._head_sha(agg / "openxFactory") == lane._head_sha(agg)

    out = lane.run_lane(agg, generate=_never_generate)

    assert not out.ok
    assert out.reason.startswith("submodule not initialised: "), out.reason
    assert "the aggregation root" in out.reason, out.reason
    assert str(tmp_path) not in out.reason, out.reason  # no absolute path
    assert out.source_revision is None
    out_dir = agg / "health/ideation-dashboard"
    assert not (out_dir / "openxFactory-snapshot.json").exists()
    assert not (out_dir / "openxFactory-snapshot.json.candidate").exists()
    status = json.loads((out_dir / "lane-status.json").read_text())
    assert status["result"] == "skipped"
    assert status["reason"] == out.reason
    assert status["source_revision"] is None


def test_the_populated_predicate(tmp_path):
    agg = _commit_repo(tmp_path / "agg")
    (agg / "empty").mkdir()
    populated = _commit_repo(agg / "populated")
    gitfile = agg / "gitfile"
    gitfile.mkdir()
    # a submodule checkout carries a `.git` FILE, not a directory
    (gitfile / ".git").write_text("gitdir: ../.git/modules/gitfile\n", encoding="utf-8")
    plain = tmp_path / "plain"
    plain.mkdir()

    assert lane._borrowed_toplevel(agg / "empty") == agg.resolve()
    assert lane._borrowed_toplevel(populated) is None
    assert lane._borrowed_toplevel(gitfile) is None
    assert lane._borrowed_toplevel(agg) is None
    # in no work tree at all: nothing to borrow, and the HEAD skip still names it
    assert lane._borrowed_toplevel(plain) is None


def test_multi_lane_skips_an_uninitialised_submodule_by_name(tmp_path):
    agg = _commit_repo(tmp_path, gitmodules=(
        '[submodule "ghost-sub"]\n\tpath = installs/ghost-sub\n'
        '\turl = git@example.invalid:ghost-sub.git\n'))
    (agg / "installs" / "ghost-sub").mkdir(parents=True)

    out = lane.run_multi_lane(agg, repositories=["ghost-sub", "nowhere"],
                              generate=_never_generate)

    assert out.published == [] and out.index_path is None
    assert out.outcomes[0].reason == (
        "submodule not initialised for repository 'ghost-sub': "
        "installs/ghost-sub declared but not checked out")
    out_dir = agg / "health/ideation-dashboard"
    assert not (out_dir / "ghost-sub-snapshot.json").exists()
    status = json.loads((out_dir / "index-status.json").read_text())
    assert status["skipped"] == [
        {"repository": "ghost-sub", "reason": "submodule not initialised",
         "paths": ["installs/ghost-sub"]},
        {"repository": "nowhere", "reason": "checkout not found"}]


def _nested_agg_root(tmp_path: Path, *, legs_initialised: bool = True) -> Path:
    """The nightly's nested shape: the aggregation declares `openxFactory`
    (populated) and `openDox` (declared, never initialised); openxFactory
    declares its own `openDox` (populated) and an uninitialised install; the
    openDox assembly root declares its `spec` and `code` legs under URLs whose
    repository names are the register ids `openDox-spec` / `openDox-code`."""
    agg = _commit_repo(tmp_path / "agg", gitmodules=(
        '[submodule "openxFactory"]\n\tpath = openxFactory\n'
        '\turl = git@github.com:opensoft/openxFactory.git\n'
        '[submodule "openDox"]\n\tpath = openDox\n'
        '\turl = git@github.com:opensoft/openDox.git\n'))
    (agg / "openDox").mkdir()
    ox = _commit_repo(agg / "openxFactory", gitmodules=(
        '[submodule "installs/omnigent-install"]\n'
        '\tpath = installs/omnigent-install\n'
        '\turl = git@github.com:opensoft/Omnigent-Install.git\n'
        '[submodule "openDox"]\n\tpath = openDox\n'
        '\turl = git@github.com:opensoft/openDox.git\n'))
    (ox / "installs" / "omnigent-install").mkdir(parents=True)
    product = _commit_repo(ox / "openDox", gitmodules=(
        '[submodule "spec"]\n\tpath = spec\n'
        '\turl = https://github.com/opensoft/openDox-spec.git\n'
        '[submodule "code"]\n\tpath = code\n'
        '\turl = https://github.com/opensoft/openDox-code.git\n'))
    if legs_initialised:
        _copy_git_fixture(product / "spec")
        _commit_repo(product / "code")
    else:
        (product / "spec").mkdir()
        (product / "code").mkdir()
    return agg


def test_nested_product_legs_resolve_through_the_declaring_gitmodules(tmp_path):
    agg = _nested_agg_root(tmp_path)
    # the aggregation root's own basename map never reaches a leg
    assert "openDox-spec" not in lane.submodule_paths(agg)

    declared = lane.declared_checkouts(agg)
    assert declared["openDox-spec"] == ["openxFactory/openDox/spec"]
    assert declared["openDox-code"] == ["openxFactory/openDox/code"]
    assert declared["openDox"] == ["openDox", "openxFactory/openDox"]  # shallowest first
    assert declared["spec"] == ["openxFactory/openDox/spec"]  # the path basename still keys it

    assert lane.resolve_checkout(agg, "openDox-spec") == "openxFactory/openDox/spec"
    assert lane.resolve_checkout(agg, "openDox-code") == "openxFactory/openDox/code"
    # the aggregation root's openDox is declared but empty, so the populated
    # nested copy is the checkout, and the empty one is recorded as tried
    located = lane.locate_checkout(agg, "openDox")
    assert (located.path, located.uninitialised) == ("openxFactory/openDox", ["openDox"])
    # declared at two depths and initialised at neither: nothing resolves
    located = lane.locate_checkout(agg, "omnigent-install")
    assert located.path is None
    assert located.uninitialised == ["openxFactory/installs/omnigent-install"]


def test_nested_legs_that_were_never_initialised_are_skipped_by_name(tmp_path):
    agg = _nested_agg_root(tmp_path, legs_initialised=False)
    out = lane.run_multi_lane(agg, repositories=["openDox-spec", "openDox-code"],
                              generate=_never_generate)
    assert out.published == []
    status = json.loads(
        (agg / "health/ideation-dashboard/index-status.json").read_text())
    assert status["skipped"] == [
        {"repository": "openDox-spec", "reason": "submodule not initialised",
         "paths": ["openxFactory/openDox/spec"]},
        {"repository": "openDox-code", "reason": "submodule not initialised",
         "paths": ["openxFactory/openDox/code"]}]


@needs_validator
def test_multi_lane_publishes_the_nested_legs_under_their_own_revisions(tmp_path):
    agg = _nested_agg_root(tmp_path)
    repos = ["openDox", "openDox-spec", "openDox-code"]
    out = lane.run_multi_lane(agg, repositories=repos, validator=VALIDATOR)
    assert [o.ok for o in out.outcomes] == [True, True, True], \
        [o.reason for o in out.outcomes]

    borrowed = {lane._head_sha(agg), lane._head_sha(agg / "openxFactory")}
    published = agg / "health/ideation-dashboard"
    for repository, checkout in (("openDox", "openxFactory/openDox"),
                                 ("openDox-spec", "openxFactory/openDox/spec"),
                                 ("openDox-code", "openxFactory/openDox/code")):
        snap = json.loads((published / f"{repository}-snapshot.json").read_text())
        revision = snap["generation"]["source_revision"]
        assert revision == lane._head_sha(agg / checkout), repository
        assert revision not in borrowed, repository
    spec = json.loads((published / "openDox-spec-snapshot.json").read_text())
    assert spec["documents"], "the leg's own corpus reaches its snapshot"
    index = json.loads((published / "index.json").read_text())
    assert [e["repository"] for e in index["entries"]] == sorted(repos)


def test_declared_checkouts_ignores_declarations_that_climb_out(tmp_path):
    agg = _commit_repo(tmp_path, gitmodules=(
        "# a comment line\n"
        '[submodule "up"]\n\tpath = ../outside\n\turl = git@example.invalid:up.git\n'
        '[submodule "abs"]\n\tpath = /etc\n\turl = git@example.invalid:abs.git\n'
        '[submodule "ok"]\n\tpath = nested/ok\n\turl = https://example.invalid/x/Ok-Name\n'
        '[submodule "quoted"]\n\tpath = "sp ace"\n'))
    assert lane.declared_checkouts(agg) == {
        "ok": ["nested/ok"], "Ok-Name": ["nested/ok"], "sp ace": ["sp ace"]}


@pytest.mark.parametrize("url,name", [
    ("git@github.com:opensoft/openDox-spec.git", "openDox-spec"),
    ("https://github.com/opensoft/openXdox-code.git", "openXdox-code"),
    ("https://github.com/opensoft/openXdox-code/", "openXdox-code"),
    ("../sibling.git", "sibling"),
    ("git@example.invalid:alpha.git", "alpha"),
    (None, None),
])
def test_repository_name_is_the_url_tail(url, name):
    assert lane._repository_name(url) == name


def test_no_candidate_source_can_resolve_outside_the_aggregation_root(tmp_path):
    """Copilot review, PR #1209: containment held only for NESTED
    declarations, while the id used as a path and the root `.gitmodules` map
    were tried unchanged. The escape target here is a real populated checkout,
    so only containment refuses it."""
    outside = _commit_repo(tmp_path / "outside")
    agg = _commit_repo(tmp_path / "agg", gitmodules=(
        '[submodule "esc"]\n\tpath = ../outside\n\turl = git@example.invalid:esc.git\n'))
    assert lane._borrowed_toplevel(outside) is None  # populated, so reachable
    assert lane.submodule_paths(agg) == {"outside": "../outside"}

    assert lane.resolve_checkout(agg, "../outside") is None       # the id as a path
    assert lane.resolve_checkout(agg, "outside") is None          # the root map
    assert lane.resolve_checkout(agg, str(outside)) is None       # an absolute id
    out = lane.run_multi_lane(agg, repositories=["../outside", "outside"],
                              generate=_never_generate)
    assert out.published == []


def test_an_undecodable_nested_gitmodules_declares_nothing(tmp_path):
    """Copilot review, PR #1209: `UnicodeDecodeError` is not an `OSError`, so
    one malformed `.gitmodules` in a pinned repository aborted the whole run
    before `index-status.json` was written."""
    agg = _nested_agg_root(tmp_path)
    (agg / "openxFactory" / "openDox" / ".gitmodules").write_bytes(
        b'\xff\xfe[submodule "spec"]\n\tpath = spec\n')

    declared = lane.declared_checkouts(agg)
    assert "openDox-spec" not in declared
    assert declared["openDox"] == ["openDox", "openxFactory/openDox"]

    out = lane.run_multi_lane(agg, repositories=["openDox-spec"],
                              generate=_never_generate)
    assert out.published == []
    status = json.loads(
        (agg / "health/ideation-dashboard/index-status.json").read_text())
    assert status["skipped"] == [
        {"repository": "openDox-spec", "reason": "checkout not found"}]


def test_only_a_submodule_section_declares_a_checkout(tmp_path):
    """Copilot review, PR #1209, second round: every bracketed header used to
    open a candidate section, so a `path =` under `[include]` (or any other
    section) became a checkout declaration. Only `[submodule "..."]` (and
    git's legacy `[submodule.name]`) declares one, and every header closes the
    section before it. The `[include]` target here is a real populated
    checkout, so only the parser refuses it."""
    agg = _commit_repo(tmp_path / "agg", gitmodules=(
        '[include]\n\tpath = nested/repo\n'
        '[submodule "real"]\n\tpath = sub/real\n'
        '[core]\n\turl = git@example.invalid:stray.git\n'
        '[Submodule.legacy]\n\tpath = sub/legacy\n'))
    _commit_repo(agg / "nested" / "repo")

    assert lane.submodule_paths(agg) == {"real": "sub/real", "legacy": "sub/legacy"}
    # the `[core]` url never attaches to the `real` section above it
    assert lane.declared_checkouts(agg) == {
        "real": ["sub/real"], "legacy": ["sub/legacy"]}
    assert lane.resolve_checkout(agg, "repo") is None
    assert lane.resolve_checkout(agg, "stray") is None


def test_gitmodules_is_read_with_gits_own_grammar(tmp_path):
    """Copilot review, PR #1209, third and fourth rounds: a hand parser kept
    drifting from git-config's grammar (an unanchored header, then an inline
    comment or quoting kept inside a value, which made an initialised leg
    declared as `path = spec # product leg` resolve as missing).
    `.gitmodules` is now read by git's OWN config parser with includes off, so
    comments, quoting, escapes, dotted names and the one-line form are exactly
    git's. The `[include]` target is a real populated checkout, so only the
    parser refuses it."""
    agg = _commit_repo(tmp_path / "agg", gitmodules=(
        '[include]\n\tpath = nested/repo\n'
        '[submodule "leg"] # a comment after the header\n'
        '\tpath = sub/spec # product leg\n'
        '\turl = https://github.com/opensoft/openDox-spec.git ; inline comment\n'
        '[submodule "quoted"]\n\tpath = "sub/q x" ; quoted, then a comment\n'
        '[submodule "esc\\"aped"]\n\tpath = sub/esc\n'
        '[submodule "a.b"]\n\tpath = sub/ab\n'
        '[submodule "inline"] path = sub/inline\n'))
    _commit_repo(agg / "nested" / "repo")
    _commit_repo(agg / "sub" / "spec")

    assert lane.submodule_paths(agg) == {
        "spec": "sub/spec", "q x": "sub/q x", "esc": "sub/esc",
        "ab": "sub/ab", "inline": "sub/inline"}
    assert lane.declared_checkouts(agg)["openDox-spec"] == ["sub/spec"]
    # the initialised leg declared with an inline comment resolves
    assert lane.resolve_checkout(agg, "openDox-spec") == "sub/spec"
    # an `[include]` path is never a checkout, and the include is not followed
    assert lane.resolve_checkout(agg, "repo") is None


def test_a_gitmodules_git_refuses_declares_nothing(tmp_path):
    """git refuses a whole file over one bad header line (`fatal: bad config
    line`, rc 128), and so does the lane: an unreadable file declares nothing,
    never a partial reading git would not make."""
    agg = _commit_repo(tmp_path / "agg", gitmodules=(
        '[submodule "ok"]\n\tpath = sub/ok\n'
        '[submodule "spaced" ]\n\tpath = sub/spaced\n'))
    _commit_repo(agg / "sub" / "ok")
    assert lane.submodule_paths(agg) == {}
    assert lane.declared_checkouts(agg) == {}
    assert lane.resolve_checkout(agg, "ok") is None


def test_git_config_null_output_is_key_newline_value(tmp_path):
    """The exact shape `_gitmodules_entries` reads, pinned against the real
    git (Copilot review, PR #1209, which twice claimed `key\\0value\\0`). With
    `--null`, git separates the key from its value with a NEWLINE and ends each
    value with NUL (git-config `-z`/`--null`), and a valueless boolean key
    arrives as `key\\0`. If git ever changed this, this test would fail rather
    than the roster silently emptying."""
    gitmodules = tmp_path / ".gitmodules"
    gitmodules.write_text(
        '[submodule "a"]\n\tpath = sub/a\n'
        '\turl = https://example.invalid/x/A.git\n\tflag\n', encoding="utf-8")
    raw = subprocess.run(
        ["git", "config", "--file", str(gitmodules), "--no-includes", "--null",
         "--get-regexp", r"^submodule\."],
        capture_output=True, check=True).stdout
    assert raw == (b"submodule.a.path\nsub/a\0"
                   b"submodule.a.url\nhttps://example.invalid/x/A.git\0"
                   b"submodule.a.flag\0")
    assert lane._gitmodules_entries(gitmodules) == [
        ("sub/a", "https://example.invalid/x/A.git")]


@pytest.mark.parametrize("value", ["C:\\x", "C:/x", "sub\\x", "\\\\srv\\share"])
def test_a_windows_absolute_or_backslash_path_is_never_a_candidate(value):
    """Copilot review, PR #1209: `PurePosixPath` does not see a drive or UNC
    anchor as absolute, so on Windows `root / rel` could leave the
    aggregation root. Any backslash, or a drive or UNC anchor, is refused."""
    assert lane._declared_rel("", value) is None


def test_a_drive_prefixed_gitmodules_path_never_resolves(tmp_path):
    """The same refusal through a real `.gitmodules`: git reads `C:/x` as a
    legal path, and on Linux `C:` is an ordinary directory name, so the
    target here is a real populated checkout and only containment refuses
    it."""
    agg = _commit_repo(tmp_path / "agg", gitmodules=(
        '[submodule "w"]\n\tpath = C:/x\n\turl = git@example.invalid:w.git\n'))
    _commit_repo(agg / "C:" / "x")
    assert lane.resolve_checkout(agg, "x") is None
    assert lane.resolve_checkout(agg, "w") is None


def _bare_clone(source: Path, destination: Path) -> Path:
    """A bare repository with a resolvable HEAD (`git clone --bare`)."""
    subprocess.run(["git", "clone", "-q", "--bare", str(source), str(destination)],
                   check=True)
    return destination


def test_a_repository_without_a_work_tree_is_not_populated(tmp_path):
    """Copilot review, PR #1209 ("previously missed"): a bare repository has
    no `.git` child and `--show-toplevel` fails there, yet `rev-parse HEAD`
    succeeds, so it read as a populated checkout and could publish an empty
    snapshot under its own HEAD. The same holds inside a `.git` directory."""
    agg = _commit_repo(tmp_path / "agg")
    bare = _bare_clone(_commit_repo(tmp_path / "work"), agg / "bare")
    (agg / "empty").mkdir()
    populated = _commit_repo(agg / "populated")
    plain = tmp_path / "plain"
    plain.mkdir()
    assert lane._head_sha(bare)  # the hazard: HEAD resolves in a bare repo

    assert lane._without_work_tree(bare) is True
    assert lane._without_work_tree(agg / ".git") is True
    assert lane._without_work_tree(populated) is False
    assert lane._without_work_tree(agg / "empty") is False  # borrowed, not bare
    assert lane._without_work_tree(plain) is False          # no repository at all


def test_a_bare_repository_is_skipped_never_published(tmp_path):
    agg = _commit_repo(tmp_path / "agg", gitmodules=(
        '[submodule "bare"]\n\tpath = bare\n\turl = git@example.invalid:bare.git\n'))
    _bare_clone(_commit_repo(tmp_path / "work"), agg / "bare")

    single = lane.run_lane(agg, checkout="bare", repository="bare",
                           generate=_never_generate)
    assert not single.ok
    assert single.reason.startswith("submodule not initialised: "), single.reason
    assert "no work tree" in single.reason, single.reason

    out = lane.run_multi_lane(agg, repositories=["bare"], generate=_never_generate)
    assert out.published == []
    out_dir = agg / "health/ideation-dashboard"
    assert not (out_dir / "bare-snapshot.json").exists()
    status = json.loads((out_dir / "index-status.json").read_text())
    assert status["skipped"] == [
        {"repository": "bare", "reason": "submodule not initialised",
         "paths": ["bare"]}]
