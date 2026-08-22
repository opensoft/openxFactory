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
    # POST-D7 worked example (Brett's 2026-08-06 ruling on the openxFactory
    # staging topic `dashboard-project-scoping`, xFactory commits dd1179e +
    # 380da26 landing it): the register is split BY ROLE — core / domains /
    # medx-clinical / installs — plus the human-managed `openxfactory` and
    # `xfactory` projects. D8 (same day) made membership multi-parent, so
    # openxFactory lives in both `core` (primary — first declaring) and
    # `openxfactory`, and MedxFactory lives in both `domains` (primary) and
    # `medx-clinical`. Pin the exact membership per role rather than diffing
    # the flattened list against the full .gitmodules pin set: newer
    # submodules (openAvatar 2026-08-03, medx-roottruth-install 2026-08-09,
    # keycloak-install/openxpki-install 2026-08-21) are real pins awaiting
    # human triage into a project via edit-project — the register's D5
    # authority posture is development-plane-authoritative, not an
    # auto-mirror of .gitmodules, so their absence here is legal.
    reg = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    assert reg["kind"] == "project-register"
    assert reg["schema_version"] == 1
    by_id = {p["id"]: sorted(p["repositories"]) for p in reg["projects"]}
    assert by_id == {
        "core": ["openxFactory"],
        "domains": ["AdxFactory", "LedgerxFactory", "MedxFactory",
                     "OpsxFactory", "codexFactory"],
        "medx-clinical": ["HealthLinc", "MedxEHR", "MedxFactory", "openChart"],
        "installs": ["agenttower", "cloudpc-install", "hermes-install",
                      "omnigent-install", "xfactory-installer"],
        "openxfactory": ["openxFactory"],
        "xfactory": ["AdxFactory", "LedgerxFactory"],
    }
    # Every repository the register names must still be a REAL pinned
    # submodule (catches a typo'd or renamed id); the converse — every
    # pinned submodule triaged into a project — is deliberately not
    # required (see the untriaged pins noted above).
    pinned = set(
        p.rsplit("/", 1)[-1] for p in
        re.findall(r"^\s*path\s*=\s*(\S+)", GITMODULES.read_text(), re.M))
    listed = set(r for repos in by_id.values() for r in repos)
    assert listed <= pinned


@aggregation_scope
def test_seed_register_leaves_grouping_to_the_human():
    # The seed deliberately declares NO project_groups (Brett has not named a
    # grouping layout); the file invites the human edit instead.
    reg = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    assert not reg.get("project_groups")


@aggregation_scope
def test_generator_adapter_resolves_openxfactory_through_the_seed():
    # POST-D7: openxFactory's primary is `core` (it declares first, before
    # the multi-parent `openxfactory` view — D8's first-wins rule); the
    # `xfactory` project name was reused the same day for an unrelated
    # empty-then-edited project (AdxFactory + LedgerxFactory) and no longer
    # holds either repo below.
    adapter = ProjectRegisterAdapter(REGISTER)
    assert adapter.resolve("openxFactory") == ("core", None)
    assert adapter.resolve("codexFactory") == ("domains", None)
    # absent repositories stay ungrouped (implicit project), never an error
    assert adapter.resolve("not-a-family-repo") == (None, None)
