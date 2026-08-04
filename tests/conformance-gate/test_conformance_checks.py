"""Fixture tests for the domain-conformance-checks scripts.

Locks the three checks to the domain-conformance-checks capability spec
(openspec/specs/domain-conformance-checks/spec.md; adopted with them from
codexFactory's conformance-gate capability, adopt-neutral-utility-pack):
inventory consistency, workflow md/yaml state parity (with the ``blocked``
convention), and openxFactory pin reconciliation semantics.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = REPO_ROOT / "scripts"

# The two real-repo self-gate tests below target the HOSTING repo. They were
# written for a domain-shaped host (codexFactory, which self-gates via
# scripts/validate-docs.sh); openxFactory is the publisher, not a domain repo
# — no stack.yaml, no workflows/ — so in this checkout they skip. They stay
# adopted so a domain-shaped host running this suite keeps its self-gate.
DOMAIN_SHAPED = (REPO_ROOT / "stack.yaml").is_file()


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


inventory = load("check-inventory-consistency")
parity = load("check-workflow-state-parity")
pin = load("check-openxfactory-pin")


# --- fixtures -------------------------------------------------------------

STACK = """\
schema_version: 1
kind: xfactory_domain_stack
schemas:
  artifact_root: schemas
  required:
    - a.schema.json
workflows:
  root: workflows
  required:
    - flow.md
xfactory:
  contract_ref: {ref}
"""

FLOW_MD = """\
# Flow

## Purpose
x

## States

| State | Meaning |
| --- | --- |
| `start` | s |
| `middle` | m |
| `done` | d |
| `blocked` | b |

## Transitions

| From | To | Gate |
| --- | --- | --- |
| `start` | `middle` | g1 |
| `middle` | `done` | g2 |
| Any | `blocked` | g3 |

## Required Output
x
"""

FLOW_YAML = """\
schema_version: 1
kind: codex_workflow_contract
workflow:
  id: flow
  gates:
    - id: g1
      requires: [x]
      produces: [{produces}]
      blocks_when: [y]
"""


def make_repo(tmp_path: Path, ref: str = "a" * 40) -> Path:
    (tmp_path / "schemas").mkdir()
    (tmp_path / "workflows").mkdir()
    (tmp_path / "stack.yaml").write_text(STACK.format(ref=ref))
    (tmp_path / "schemas" / "a.schema.json").write_text("{}")
    (tmp_path / "schemas" / "README.md").write_text("| A | [a.schema.json](a.schema.json) |\n")
    (tmp_path / "workflows" / "flow.md").write_text(FLOW_MD)
    (tmp_path / "workflows" / "flow.yaml").write_text(FLOW_YAML.format(produces="middle, done"))
    return tmp_path


# --- inventory ------------------------------------------------------------

def test_inventory_valid_fixture_passes(tmp_path):
    assert inventory.check(make_repo(tmp_path)) == []


def test_inventory_flags_unlisted_shipped_schema(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "schemas" / "extra.schema.yaml").write_text("{}")
    errors = inventory.check(repo)
    assert any("extra.schema.yaml" in e and "not listed" in e for e in errors)


def test_inventory_flags_declared_missing_artifact(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "workflows" / "flow.md").unlink()
    errors = inventory.check(repo)
    assert any("flow.md" in e and "missing on disk" in e for e in errors)


def test_inventory_flags_readme_drift_both_directions(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "schemas" / "README.md").write_text("| G | [ghost.schema.json](ghost.schema.json) |\n")
    errors = inventory.check(repo)
    assert any("omits shipped schema: a.schema.json" in e for e in errors)
    assert any("lists nonexistent schema: ghost.schema.json" in e for e in errors)


def test_inventory_flags_missing_yaml_pair(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "workflows" / "flow.yaml").unlink()
    errors = inventory.check(repo)
    assert any("missing its .yaml gate contract pair" in e for e in errors)


@pytest.mark.skipif(not DOMAIN_SHAPED, reason="publisher checkout is not a domain repo; the self-gate runs in domain repos")
def test_inventory_real_repo_is_consistent():
    assert inventory.check(REPO_ROOT) == []


# --- parity ---------------------------------------------------------------

@pytest.mark.skipif(not DOMAIN_SHAPED, reason="publisher checkout is not a domain repo; the self-gate runs in domain repos")
def test_parity_all_real_pairs_pass():
    assert parity.check(REPO_ROOT / "workflows") == []


def test_parity_valid_fixture_passes(tmp_path):
    assert parity.check(make_repo(tmp_path) / "workflows") == []


def test_parity_flags_divergent_pair_naming_states(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "workflows" / "flow.yaml").write_text(FLOW_YAML.format(produces="middle, rogue"))
    errors = parity.check(repo / "workflows")
    assert len(errors) == 1
    assert "flow" in errors[0] and "rogue" in errors[0] and "done" in errors[0]


def test_parity_blocked_is_excluded_by_convention(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "workflows" / "flow.yaml").write_text(
        FLOW_YAML.format(produces="middle, done, blocked")
    )
    assert parity.check(repo / "workflows") == []


# --- pin ------------------------------------------------------------------

def test_pin_equal_passes():
    verdict, _ = pin.classify("a" * 40, "a" * 40, lambda a, b: True)
    assert verdict == pin.PASS


def test_pin_stale_behind_warns_with_refresh_instruction():
    verdict, message = pin.classify("a" * 40, "b" * 40, lambda a, b: True)
    assert verdict == pin.WARN
    assert "refresh" in message and "b" * 40 in message


def test_pin_divergent_errors():
    verdict, message = pin.classify("a" * 40, "b" * 40, lambda a, b: False)
    assert verdict == pin.ERROR
    assert "not an ancestor" in message


def test_pin_skips_outside_aggregation(tmp_path):
    assert pin.find_aggregation_root(tmp_path / "x" / "y") is None


def test_pin_hands_git_absolute_directories(tmp_path, monkeypatch):
    """Both roots can come from the command line, and a relative path that
    began with a dash would be read by git as an option. Resolving first is
    what removes that shape — so the argv git actually receives is pinned."""
    seen = []

    class Completed:
        returncode = 0
        stdout = "160000 commit " + "a" * 40 + "\topenxFactory"

    def fake_run(argv, **kwargs):
        seen.append(argv)
        return Completed()

    monkeypatch.setattr(pin.subprocess, "run", fake_run)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "-dashed").mkdir()

    pin.recorded_pointer(Path("-dashed"))
    pin.git_is_ancestor(Path("-dashed"))("a" * 40, "b" * 40)

    assert len(seen) == 2
    for argv in seen:
        directory = argv[argv.index("-C") + 1]
        assert Path(directory).is_absolute()
        assert not directory.startswith("-")
