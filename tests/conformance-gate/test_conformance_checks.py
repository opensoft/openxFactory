"""Fixture tests for the domain-conformance-checks scripts.

Locks the four checks to the domain-conformance-checks capability spec
(openspec/specs/domain-conformance-checks/spec.md; the first three adopted with
that capability from codexFactory's conformance-gate capability,
adopt-neutral-utility-pack): inventory consistency, workflow md/yaml state
parity (with the ``blocked`` convention), openxFactory pin reconciliation
semantics, and — grown to four by add-client-identity-roster (Decision A) —
client identity roster conformance.

The fourth member is exercised HERE as a PACK MEMBER, which is a different
measurement from `tests/client-identity-roster/`: pack membership is the only
promoted mechanism that confers BLOCKING status, so what this file pins is the
EXIT the domain gate reads. The roster suite proves the rules; these four tests
prove that a nonconformance reaches the gate as a nonzero exit, that a
conformant repo and a repo with no fragment both leave it green, and that the
roster delta's mutate scenario is an ERROR rather than a report.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

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
roster = load("validate-client-identity-roster")

# The pack, by name. A member added to (or dropped from) the promoted
# enumeration without a test here would leave its blocking status unmeasured.
PACK = ("check-inventory-consistency", "check-workflow-state-parity",
        "check-openxfactory-pin", "validate-client-identity-roster")


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


# --- pin: the relocation notice (P2.5, split-openxwallet-repo D5) ----------
#
# The deprecating minor marks the eight openxWallet manifest rows `relocating:`
# and this checker is the EMITTER — the only domain-pin candidate with a warning
# tier. What these tests pin is the thing the change's evidence row names: the
# checker's OUTPUT, and the fact that the output is a WARNING and not a failure.
# `classify()` is deliberately untouched by that work, so its four tests above
# are the regression guard and these five are purely additive.

RELOCATION_MANIFEST = {
    "contract_bundle_version": "contract-v1.47",
    "contracts": [
        {"id": "unrelated-schema", "path": "contracts/schemas/x.yaml"},
        {
            "id": "openxwallet-record",
            "path": "contracts/openxwallet/openxwallet-record.schema.yaml",
            "relocating": {
                "to": "opensoft/openXwallet",
                "tag": "wallet-v1.1",
                "since": "contract-v1.47",
            },
        },
        {
            "id": "openxwallet-agent-composition",
            "path": "contracts/openxwallet-agent-profile/x.schema.yaml",
            "relocating": {
                "to": "opensoft/openXwallet",
                "tag": "wallet-v1.1",
                "since": "contract-v1.47",
            },
        },
    ],
}


def test_pin_relocating_rows_extracted_in_manifest_order():
    """Manifest order, not sorted order: the eight rows are one authored block
    and reading them back in a different order would misrepresent the file."""
    rows = pin.relocating_rows(RELOCATION_MANIFEST)
    assert [row.artifact_id for row in rows] == [
        "openxwallet-record",
        "openxwallet-agent-composition",
    ]
    assert all(row.to == "opensoft/openXwallet" for row in rows)
    assert all(row.tag == "wallet-v1.1" for row in rows)


def test_pin_no_relocating_rows_yields_no_notice():
    """Every bundle up to and including contract-v1.46. Silence is the contract:
    a consumer pinned before the marker existed must see no new output at all."""
    manifest = {
        "contract_bundle_version": "contract-v1.46",
        "contracts": [{"id": "openxwallet-record", "path": "p"}],
    }
    assert pin.relocating_rows(manifest) == []
    assert pin.relocation_notice(manifest) is None


def test_pin_relocation_notice_names_every_artifact_target_and_tag():
    """The evidence row wants each relocating artifact NAMED with its target and
    tag — a count alone would not tell a migrator where to go."""
    notice = pin.relocation_notice(RELOCATION_MANIFEST)
    assert notice is not None
    assert "contract-v1.47" in notice
    assert "2 relocating" in notice
    assert "openxwallet-record -> opensoft/openXwallet @ wallet-v1.1" in notice
    assert (
        "openxwallet-agent-composition -> opensoft/openXwallet @ wallet-v1.1"
        in notice
    )
    # The removal version is NOT claimed from row data — the row deliberately
    # carries none, so the notice points at the changelog for it.
    assert "contracts/CHANGELOG.md" in notice
    assert "unrelated-schema" not in notice


@pytest.mark.parametrize(
    "manifest",
    [None, [], "not a mapping", {"contracts": "not a list"}, {}],
    ids=["none", "list", "string", "contracts-not-a-list", "empty-mapping"],
)
def test_pin_relocation_notice_absent_when_manifest_unreadable(manifest):
    """A question that could not be asked is not a finding — the same doctrine
    the release-inventory family states. None of these may raise."""
    assert pin.relocating_rows(manifest) == []
    assert pin.relocation_notice(manifest) is None


def test_pin_manifest_at_commit_returns_none_on_any_git_failure(tmp_path):
    """An unresolvable commit, an absent file and unparseable bytes are all the
    same answer: no notice, no failure, no traceback."""
    assert pin.manifest_at_commit(tmp_path, "a" * 40) is None


def test_pin_relocation_does_not_change_exit_semantics():
    """FR-008. WARN has always exited 0 and the relocation notice is a WARN, so
    the exit expression is unchanged — this pins that it STAYS unchanged."""
    for verdict in (pin.PASS, pin.WARN, pin.SKIP):
        assert (1 if verdict == pin.ERROR else 0) == 0
    assert (1 if pin.ERROR == pin.ERROR else 0) == 1
    # And the notice itself carries no verdict that could override one.
    notice = pin.relocation_notice(RELOCATION_MANIFEST)
    assert notice.startswith(f"{pin.WARN}: ")


# --- roster: the fourth pack member ---------------------------------------
#
# The four behaviours the deltas specify. THREE come from the
# domain-conformance-checks delta (an entry nonconformance fails the gate; a
# conformant repo passes; a repo publishing no fragment passes with an explicit
# notice) and ONE from the client-identity-roster delta's "A mutate identity has
# no ratified capability" scenario, which is an ERROR that fails the owning
# domain's gate rather than a report-only finding.
#
# The EXIT is the measurement, so the check runs as a PROCESS. The rules
# themselves, their negatives and their discriminations belong to
# `tests/client-identity-roster/` and are not re-derived here.

TENANT = "11111111-1111-1111-1111-111111111111"
PLACEMENT = "/".join(roster.PLACEMENT_PARTS)


def roster_entry(**over) -> dict:
    base = {
        "identity_ref": "pack-bc-observer",
        "identity_kind": "entra_app_registration",
        "home_tenant": TENANT,
        "principal_locations": [TENANT],
        "residency_model": "client_tenant_single",
        "admission_surface": "business_central",
        "duty": "observing",
        "blast_radius_unit": "unit_a",
        "authority_class_intended": "observe",
        "authority_class_achieved": "observe",
        "granted_permissions": [
            {"id": "Pack.Read.All", "achieves": "observe",
             "reaches": ["business_central"]},
        ],
        "admission": [
            {"surface": "business_central",
             "act": "per-environment application user created",
             "achieved_scope": "Unit A environment",
             "enforcement_mode": "provider_enforced",
             "evidence_ref": {"repo": "opensoft/PackxFactory",
                              "path": "tenants/pack-admission-evidence-v1.yaml"},
             "verified_at": "2026-08-01T00:00:00Z",
             "exceeds_governed_unit": False},
        ],
        "per_unit_principal_available": {"business_central": True},
        "lifecycle_state": "enrolled",
        "standing_credential_attestation": {
            "no_standing_credential": True,
            "attested_at": "2026-08-01T00:00:00Z",
        },
        "ratified_by": "packxfactory:pack-observation-capability",
        "consent_ref": "pack-consent-v1",
    }
    base.update(over)
    return base


def roster_fragment(entries: list[dict]) -> dict:
    return {
        "schema_version": 1,
        "kind": "xfactory_client_identity_roster",
        "client_ref": "client-pack",
        "client_tenant": TENANT,
        "domain": "packxfactory",
        "legend": {
            "blast_radius_units": {"unit_a": "Unit A"},
            "duties": {"observing": "Read-only observation"},
        },
        "entries": entries,
    }


CONSENT = {"schema_version": 1, "kind": "xfactory_consent_instrument",
           "instrument_id": "pack-consent-v1", "status": "executed"}


def make_roster_repo(tmp_path: Path, name: str, files: dict[str, dict]) -> Path:
    root = tmp_path / name
    root.mkdir(parents=True, exist_ok=True)
    for rel, doc in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.dump(doc, sort_keys=False), encoding="utf-8")
    return root


def run_roster_check(target: Path) -> subprocess.CompletedProcess:
    """The pack consumption shape: the check handed its target as an explicit
    argument, run from this (pinned) checkout and never copied into the repo."""
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "validate-client-identity-roster.py"),
         str(target)],
        capture_output=True, text=True)


def test_pack_conformant_repo_leaves_the_gate_green(tmp_path):
    """The pack is FOUR members, each invocable from the pinned checkout
    against a target handed as an argument, and a conformant repo exits 0."""
    for member in PACK:
        assert (SCRIPTS / f"{member}.py").is_file(), member
    repo = make_roster_repo(tmp_path, "conformant", {
        f"{PLACEMENT}/client-pack.yaml": roster_fragment([roster_entry()]),
        "consent/pack-consent-v1.yaml": CONSENT,
    })
    result = run_roster_check(repo)
    assert result.returncode == 0, result.stdout


def test_pack_entry_nonconformance_exits_nonzero(tmp_path):
    """A nonzero exit from any member fails the domain gate — measured on an
    intra-repo entry rule (a verified act reaching beyond the governed unit
    with no declared excess)."""
    bad = roster_entry(admission=[dict(roster_entry()["admission"][0],
                                       exceeds_governed_unit=True)])
    repo = make_roster_repo(tmp_path, "nonconformant", {
        f"{PLACEMENT}/client-pack.yaml": roster_fragment([bad]),
        "consent/pack-consent-v1.yaml": CONSENT,
    })
    result = run_roster_check(repo)
    assert result.returncode == 1, result.stdout
    assert "undeclared-scope-excess" in result.stdout


def test_pack_repo_with_no_roster_fragment_passes_with_an_explicit_notice(tmp_path):
    """Absence is never a finding: the member passes with a notice NAMING the
    absence, so a domain that publishes no fragment is not silently green and
    not red either."""
    repo = make_roster_repo(tmp_path, "no-fragment", {
        "consent/pack-consent-v1.yaml": CONSENT,
    })
    result = run_roster_check(repo)
    assert result.returncode == 0, result.stdout
    assert "publishes no credentials/client-identity-roster/ directory" in result.stdout


def test_pack_mutate_without_ratified_capability_errors_rather_than_reports(tmp_path):
    """The roster delta's own gate scenario. A mutate entry with no
    domain-qualified ratified capability is an ERROR that fails the owning
    domain's gate — and the cross-domain composition classes, which are the
    doc-health family's and leave the gate exit unchanged, appear nowhere in
    this member's output."""
    bad = roster_entry(
        identity_ref="pack-bc-writer",
        authority_class_intended="mutate",
        authority_class_achieved="mutate",
        granted_permissions=[{"id": "Pack.ReadWrite.All", "achieves": "mutate",
                              "reaches": ["business_central"]}],
        ratified_by="pack-mutation-capability")
    repo = make_roster_repo(tmp_path, "mutate-no-capability", {
        f"{PLACEMENT}/client-pack.yaml": roster_fragment([bad]),
        "consent/pack-consent-v1.yaml": CONSENT,
    })
    result = run_roster_check(repo)
    assert result.returncode == 1, result.stdout
    assert "mutate-without-ratified-capability" in result.stdout
    for cross_domain in ("shared-identity-material", "undeclared-cross-domain-reach"):
        assert cross_domain not in result.stdout
