"""CLI parity for the two keyword-lens gate verbs (add-lens-gate-verbs).

`ideation-dashboard gate lens-save-recipe` / `gate lens-add-as-cluster` execute
the SAME tested engines the loopback route drives — the CLI is the terminal
surface of the one choke point (the propose precedent, test_readiness_gate.py).
Hermetic: the snapshot generation is stubbed with the fixture corpus (no git),
and the pinned validators are pointed at the real openxFactory checkout so the
manifest/queue writes are schema-validated exactly as production.
"""

from __future__ import annotations

import yaml as yaml_mod

import pytest

from conftest import BASE_REPO, PINNED_REVISION, FakeGit, find_openxfactory_validator

from opendox import cli
from ideation_dashboard import human_seen as hs
from opendox import workbench as wb

VALIDATOR = find_openxfactory_validator()
XREF_VALIDATOR = hs.find_cross_reference_validator(BASE_REPO)

_SKIP = pytest.mark.skipif(VALIDATOR is None or XREF_VALIDATOR is None,
                           reason="pinned openxFactory validator(s) not reachable")


def _snapshot():
    from openxdox.generator import generate_snapshot
    return generate_snapshot(BASE_REPO, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())


def _wire(monkeypatch):
    """Stub snapshot generation with the fixture corpus and point the two pinned
    validators at the real openxFactory checkout (the CLI auto-finds them from
    the checkout in production; the tmp checkout is outside the workspace)."""
    snap = _snapshot()
    monkeypatch.setattr(*_generation_site(), lambda *a, **k: snap)
    _point_the_workbench_validator(monkeypatch)
    monkeypatch.setattr(hs, "find_cross_reference_validator", lambda *a, **k: XREF_VALIDATOR)
    monkeypatch.setattr(hs, "XREF_VALIDATOR_RELPATH", XREF_VALIDATOR)


def _base_args(root, verb):
    return ["gate", verb, "--repo-root", str(root), "--actor", "brett",
            "--repository", "fixture-repo", "--source-revision", PINNED_REVISION,
            "--name", "Governance lens", "--checked", "ideation-governance"]


@_SKIP
def test_cli_lens_save_recipe_lands_manifest_and_record(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch)
    rc = cli.main(_base_args(tmp_path, "lens-save-recipe"))
    assert rc == 0
    out = capsys.readouterr().out
    assert "lens-save-recipe" in out
    manifest = tmp_path / "ideation" / "workbench" / "governance-lens.workbench.yaml"
    assert manifest.is_file()
    loaded = yaml_mod.safe_load(manifest.read_text("utf-8"))
    assert loaded["kind"] == "ideation-workbench"
    assert loaded["recipe"]["checked"] == ["ideation-governance"]
    records = list(tmp_path.rglob("lens-save-recipe-*.gate-action.yaml"))
    assert len(records) == 1
    record = yaml_mod.safe_load(records[0].read_text("utf-8"))
    assert record["action"] == "lens-save-recipe" and record["actor"] == "brett"


@_SKIP
def test_cli_lens_save_recipe_reasonless_override_refused(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch)
    args = _base_args(tmp_path, "lens-save-recipe") + [
        "--include", "ideation/brainstorm/avatar-client-lab.md"]  # bare doc, no =reason
    with pytest.raises(SystemExit) as ei:
        cli.main(args)
    assert ei.value.code != 0
    assert not list(tmp_path.rglob("*.workbench.yaml"))


@_SKIP
def test_cli_lens_add_as_cluster_lands_manifest_pending_and_record(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch)
    args = _base_args(tmp_path, "lens-add-as-cluster") + [
        "--proposer", "brett",
        "--evidence-repository", "fixture-repo",
        "--evidence-path", "ideation/brainstorm/dtn-register.md",
        "--revision", PINNED_REVISION,
        "--section", "Notes",
        "--passage-sha256", "b0f04c299263dd2496c601fbbd812d645ebade162c5a9aa15e8fe8b7a656bc7a",
        "--rationale", "Grouping two governance notes for review.",
        "--confidence", "0.6",
        "--alternative", "Fold into an existing governance cluster instead.",
    ]
    rc = cli.main(args)
    assert rc == 0
    manifest = tmp_path / "ideation" / "workbench" / "governance-lens.workbench.yaml"
    assert manifest.is_file()
    pending = list(tmp_path.rglob("*.human-seen.yaml"))
    assert len(pending) == 1
    entry = yaml_mod.safe_load(pending[0].read_text("utf-8"))["topic_entries"][0]
    assert entry["origin"] == "human-seen"
    assert entry["human_seen"]["disposition"] == "pending_review"
    records = list(tmp_path.rglob("lens-add-as-cluster-*.gate-action.yaml"))
    assert len(records) == 1
    # the generated cross-reference index is NEVER written by this verb.
    assert not (tmp_path / "ideation" / "cross-reference.yaml").exists()


@_SKIP
def test_cli_lens_add_as_cluster_missing_evidence_refused(tmp_path, monkeypatch, capsys):
    _wire(monkeypatch)
    # no evidence flags => the human_seen contract refuses before persistence.
    rc = cli.main(_base_args(tmp_path, "lens-add-as-cluster"))
    assert rc == 1
    err = capsys.readouterr().err
    assert "refused" in err and "evidence" in err
    assert not list(tmp_path.rglob("*.workbench.yaml"))
    assert not list(tmp_path.rglob("*.human-seen.yaml"))


def test_cli_exposes_no_gate_bypass_flag():
    import inspect
    from pathlib import Path
    source = Path(inspect.getsourcefile(cli)).read_text("utf-8")
    for flag in ("--force", "--override", "--skip-readiness", "--no-gate"):
        assert flag not in source, flag


def _generation_site():
    """Where the gate verbs' `_gate_snapshot` generates, at the pinned openDox
    leg, as the `(object, name)` `_wire` stubs (plan 034 T066). Before
    openDox-code #59 (`fa140875`, T055) it reads `generate_snapshot` out of
    `cli`'s own globals; from #59 it generates through the generator seam,
    `cli.generator_seam.generate`, and `cli` binds no `generate_snapshot`. So
    the stub reaches the same one reader at both pins, and `_gate_snapshot`
    itself stays under test."""
    if hasattr(cli, "generate_snapshot"):
        return cli, "generate_snapshot"
    return cli.generator_seam, "generate"


def _point_the_workbench_validator(monkeypatch):
    """Point the workbench's manifest validation at the pinned openxFactory
    validator where the pinned openDox leg looks one up (plan 034 T066).
    Before openDox-code #59 (`fa140875`, T055) `opendox.workbench` binds
    `find_validator`, the consumer's lookup, and this points it at the real
    openxFactory checkout, as production finds it. From #59 the workbench
    validates its own `ideation-workbench` kind with openDox's validator, as
    production does, and binds no `find_validator`, so there is nothing to
    point."""
    if hasattr(wb, "find_validator"):
        monkeypatch.setattr(wb, "find_validator", lambda *a, **k: VALIDATOR)
