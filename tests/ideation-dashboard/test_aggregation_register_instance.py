"""The aggregation-root project-register SEED instance (add-ideation-dashboard
task 4.1 / decision D10) is schema-valid under the pinned validator and mirrors
the family pins in .gitmodules. These tests are aggregation-scope: in a
standalone openxFactory checkout (no aggregation root above) they skip with
notice rather than fail — the house single-repo pattern."""

from __future__ import annotations

import re
import subprocess
import sys

import pytest
import yaml

from conftest import REPO_ROOT, find_openxfactory_validator

from ideation_dashboard.register import ProjectRegisterAdapter

VALIDATOR = find_openxfactory_validator()
AGG_ROOT = REPO_ROOT.parent  # openxFactory -> aggregation root
REGISTER = AGG_ROOT / "project-register.yaml"
GITMODULES = AGG_ROOT / ".gitmodules"

aggregation_scope = pytest.mark.skipif(
    VALIDATOR is None or not REGISTER.is_file() or not GITMODULES.is_file(),
    reason="aggregation checkout (seed register + pinned validator) not reachable")


@aggregation_scope
def test_seed_register_validates_clean_under_strict():
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(REGISTER), "--strict"],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@aggregation_scope
def test_seed_register_lists_exactly_the_pinned_submodules():
    # D10 worked example: one `xfactory` project whose repositories are the
    # family repos as pinned in .gitmodules (ids = submodule path basenames).
    pinned = sorted(
        p.rsplit("/", 1)[-1] for p in
        re.findall(r"^\s*path\s*=\s*(\S+)", GITMODULES.read_text(), re.M))
    reg = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    assert reg["kind"] == "project-register"
    assert reg["schema_version"] == 1
    listed = sorted(r for p in reg["projects"] for r in p["repositories"])
    assert listed == pinned


@aggregation_scope
def test_seed_register_leaves_grouping_to_the_human():
    # The seed deliberately declares NO project_groups (Brett has not named a
    # grouping layout); the file invites the human edit instead.
    reg = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    assert not reg.get("project_groups")


@aggregation_scope
def test_generator_adapter_resolves_openxfactory_through_the_seed():
    adapter = ProjectRegisterAdapter(REGISTER)
    assert adapter.resolve("openxFactory") == ("xfactory", None)
    assert adapter.resolve("codexFactory") == ("xfactory", None)
    # absent repositories stay ungrouped (implicit project), never an error
    assert adapter.resolve("not-a-family-repo") == (None, None)
