"""CLI parity for the wheel action-row verbs (011 add-wheel-action-verbs).

`gate promote-to-staging` / `gate derive-possibles` / `gate research-brief` are
the terminal surface of the SAME engines the loopback routes drive — one choke
point, two doors. These tests pin the CLI half of that equivalence
(contracts/cli-surface.md L1–L6), plus the `gate demote` help amendment naming
its executing-route peer.

Argument style is REQUIRED FLAGS, not positionals (plan decision P6): the
governing task prose writes `gate promote-to-staging <possible-id>`, but no gate
subcommand in this CLI takes a positional target, and consistency wins.
"""

from __future__ import annotations

import yaml as yaml_mod

import pytest

from ideation_dashboard import cli
from ideation_dashboard import gate_console as gc
from ideation_dashboard import kickoff as ko
from ideation_dashboard.boundary import HumanGate

AT = "2026-08-02T09:00:00Z"
CLUSTERS = {"clusters": [{"id": "cl-a", "name": "A"}]}


def _entry(pid="pos-a", state="latent", origin=None, outcome=None):
    """One possibles-register entry. Local by design — test modules do not
    import each other's private helpers."""
    e = {"id": pid, "title": "T", "claim": "c", "state": state,
         "provenance": {"document": "d", "section": "s"}}
    if origin:
        e["origin"] = origin
    if origin == "ai-derived":
        e["derivation"] = {"worker_run": {"correlation_id": "D-1",
                                          "worker_profile": "derive-possibles",
                                          "prompt_contract_version": "v1"},
                           "disposition": "pending_review"}
        if outcome:
            e["derivation"]["human_disposition"] = {"outcome": outcome,
                                                    "authority": "brett"}
    return e


def _checkout(tmp_path, register=None, name="checkout"):
    root = tmp_path / name
    (root / "ideation").mkdir(parents=True)
    index = {"schema_version": 1, "kind": "ideation-cross-reference",
             "repository": "openxFactory",
             "generation": {"source_revision": "e" * 40, "generator_version": "t"},
             "topic_entries": [{"id": "cl-a", "name": "A",
                                "members": [{"path": "p", "stage": "staged"}]}],
             "possibles_register": [_entry()] if register is None else register}
    (root / "ideation" / "cross-reference.yaml").write_text(
        yaml_mod.safe_dump(index, sort_keys=False), encoding="utf-8")
    return root


def _wire_snapshot(monkeypatch, snapshot=None):
    """`derive-possibles` validates its cluster against the SNAPSHOT; stub the
    generation the way the lens CLI tests do, so the case stays hermetic."""
    monkeypatch.setattr(
        cli, "generate_snapshot",
        lambda *a, **k: CLUSTERS if snapshot is None else snapshot)


def _args(root, verb, *rest):
    return ["gate", verb, "--repo-root", str(root), "--actor", "brett", *rest]


def _snapshot_args(root, verb, *rest):
    return _args(root, verb, "--repository", "fixture-repo",
                 "--source-revision", "e" * 40, *rest)


def _written(root):
    rec = root / gc.DEFAULT_RECORDS_DIR
    return sorted(p for p in rec.rglob("*") if p.is_file()) if rec.is_dir() else []


def _descriptor(root):
    return yaml_mod.safe_load(
        next(p for p in _written(root)
             if p.name.endswith(".workflow-job.yaml")).read_text("utf-8"))


# ---- L1: the accept paths -------------------------------------------------

def test_cli_promote_to_staging_commissions(tmp_path, capsys):
    """L1: rc 0, a summary on stdout, and exactly the two commission files."""
    root = _checkout(tmp_path)
    rc = cli.main(_args(root, "promote-to-staging", "--possible-id", "pos-a"))
    assert rc == 0
    out = capsys.readouterr().out
    assert "promote-to-staging" in out and "pos-a" in out
    assert len(_written(root)) == 2


def test_cli_research_brief_commissions(tmp_path, capsys):
    """L1: the pre-verdict brief is commissionable from the terminal."""
    root = _checkout(tmp_path)
    rc = cli.main(_args(root, "research-brief", "--possible-id", "pos-a"))
    assert rc == 0
    assert "research-brief" in capsys.readouterr().out
    assert len(_written(root)) == 2


def test_cli_derive_possibles_commissions(tmp_path, monkeypatch, capsys):
    """L1: the cluster-scoped run is commissionable, validated against the
    SNAPSHOT rather than the register."""
    root = _checkout(tmp_path)
    _wire_snapshot(monkeypatch)
    rc = cli.main(_snapshot_args(root, "derive-possibles", "--cluster-id", "cl-a"))
    assert rc == 0
    assert "derive-possibles" in capsys.readouterr().out
    assert len(_written(root)) == 2


# ---- L2: refusals exit 1 with the engine's reason on stderr ---------------

def test_cli_promote_refuses_a_non_promotable_possible(tmp_path, capsys):
    """L2: the engine's reason reaches stderr verbatim, and nothing is written."""
    root = _checkout(tmp_path, register=[_entry(origin="ai-derived")])
    rc = cli.main(_args(root, "promote-to-staging", "--possible-id", "pos-a"))
    assert rc == 1
    err = capsys.readouterr().err
    assert "promote-to-staging refused" in err and "disposition" in err
    assert _written(root) == []


@pytest.mark.parametrize("verb", ["promote-to-staging", "research-brief"])
def test_cli_possibles_verbs_refuse_an_unknown_id(tmp_path, capsys, verb):
    """L2: the target must exist in the pinned checkout's register."""
    root = _checkout(tmp_path)
    rc = cli.main(_args(root, verb, "--possible-id", "pos-nope"))
    assert rc == 1
    assert "pos-nope" in capsys.readouterr().err
    assert _written(root) == []


def test_cli_derive_possibles_refuses_an_unknown_cluster(tmp_path, monkeypatch, capsys):
    """L2: a cluster absent from the snapshot's cluster set is refused."""
    root = _checkout(tmp_path)
    _wire_snapshot(monkeypatch)
    rc = cli.main(_snapshot_args(root, "derive-possibles", "--cluster-id", "cl-nope"))
    assert rc == 1
    assert "cl-nope" in capsys.readouterr().err
    assert _written(root) == []


def test_cli_duplicate_commission_is_refused_naming_the_descriptor(tmp_path, capsys):
    """L2 + FR-026: the refusal points at the file whose status to edit."""
    root = _checkout(tmp_path)
    assert cli.main(_args(root, "research-brief", "--possible-id", "pos-a")) == 0
    capsys.readouterr()
    rc = cli.main(_args(root, "research-brief", "--possible-id", "pos-a"))
    assert rc == 1
    assert ".workflow-job.yaml" in capsys.readouterr().err
    assert len(_written(root)) == 2      # the second wrote nothing


def test_cli_one_verb_does_not_block_another_on_the_same_target(tmp_path):
    """FR-027 holds on the terminal surface too."""
    root = _checkout(tmp_path)
    assert cli.main(_args(root, "research-brief", "--possible-id", "pos-a")) == 0
    assert cli.main(_args(root, "promote-to-staging", "--possible-id", "pos-a")) == 0


# ---- L3: a missing required flag is an argparse error, not a partial write -

@pytest.mark.parametrize("verb", ["promote-to-staging", "research-brief"])
def test_cli_missing_required_flag_exits_and_writes_nothing(tmp_path, verb):
    """L3: argparse rejects before any engine call, so nothing is persisted."""
    root = _checkout(tmp_path)
    with pytest.raises(SystemExit):
        cli.main(_args(root, verb))
    assert _written(root) == []


# ---- L4: route/CLI artifact equivalence -----------------------------------

def test_cli_and_engine_produce_the_same_descriptor(tmp_path):
    """L4: the CLI adds nothing and omits nothing — the same target through
    either door yields the same commission, modulo the dispatch timestamp."""
    cli_root = _checkout(tmp_path, name="via-cli")
    assert cli.main(_args(cli_root, "promote-to-staging",
                          "--possible-id", "pos-a", "--topic", "my-topic")) == 0
    cli_job = _descriptor(cli_root)

    eng_root = _checkout(tmp_path, name="via-engine")
    gate = HumanGate(eng_root, [gc.DEFAULT_RECORDS_DIR], human_actor="brett")
    eng_job = ko.promote_to_staging(gate, "pos-a", topic="my-topic", at=AT).job

    drop = {"dispatched_at"}
    assert {k: v for k, v in cli_job.items() if k not in drop} == \
           {k: v for k, v in eng_job.items() if k not in drop}


# ---- the optional topic slug ----------------------------------------------

def test_cli_topic_slug_is_recorded_only_when_supplied(tmp_path):
    """FR-012: optional means optional — present when given, absent when not."""
    with_slug = _checkout(tmp_path, name="with-slug")
    assert cli.main(_args(with_slug, "promote-to-staging",
                          "--possible-id", "pos-a", "--topic", "chosen")) == 0
    assert _descriptor(with_slug)["topic_slug"] == "chosen"

    without = _checkout(tmp_path, name="without-slug")
    assert cli.main(_args(without, "promote-to-staging",
                          "--possible-id", "pos-a")) == 0
    assert "topic_slug" not in _descriptor(without)


# ---- L5: the demote help amendment ----------------------------------------

def test_gate_demote_help_names_its_executing_dashboard_peer(capsys):
    """L5: the terminal command points at the dashboard route, so a reader
    learns the two are peers and that only THIS one can execute the plan."""
    with pytest.raises(SystemExit):
        cli.main(["gate", "demote", "--help"])
    assert "dashboard" in capsys.readouterr().out.lower()


# ---- L6: the pre-existing gate surface is unchanged ------------------------

def test_pre_existing_gate_subcommands_still_parse(capsys):
    """L6: adding three subcommands must not disturb the existing ones."""
    for verb in ("propose", "demote", "ratify", "kickoff", "dispose-possible"):
        with pytest.raises(SystemExit):
            cli.main(["gate", verb, "--help"])
        assert capsys.readouterr().out
