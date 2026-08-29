from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import assert_never

import pytest

from scripts.hermes_runtime_validation.release import (
    ReleaseDependencyError,
    build_release_inventory,
    release_membership,
)

ROOT = Path(__file__).resolve().parents[2]


class ReleaseState(StrEnum):
    CURRENT = "contract-v2.1"
    FEATURE = "contract-v2.3"


def _release_state() -> ReleaseState:
    prefix = "contract_bundle_version: "
    manifest = (ROOT / "contracts" / "manifest.yaml").read_text(encoding="utf-8")
    value = next(
        (
            line.removeprefix(prefix)
            for line in manifest.splitlines()
            if line.startswith(prefix)
        ),
        None,
    )
    try:
        return ReleaseState(value)
    except ValueError:
        pytest.fail(f"unsupported release state: {value}")


def _feature_release_members() -> set[str]:
    family = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "contracts" / "intent-compliance").rglob("*")
        if path.is_file()
    }
    implementation = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "scripts" / "intent_compliance").rglob("*.py")
    }
    tests = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests" / "intent-compliance").rglob("*.py")
    }
    return family | implementation | tests | {"scripts/validate-intent-compliance.py"}


def test_release_membership_when_registration_changes_then_transition_is_atomic() -> (
    None
):
    members = {path.as_posix() for path in release_membership(ROOT)}
    feature_members = _feature_release_members()

    match _release_state():
        case ReleaseState.CURRENT:
            assert feature_members.isdisjoint(members)
        case ReleaseState.FEATURE:
            assert feature_members | {"scripts/__init__.py"} <= members
        case unreachable:
            assert_never(unreachable)


def test_release_inventory_when_registration_changes_then_schema_pins_are_atomic() -> (
    None
):
    state = _release_state()
    inventory = build_release_inventory(ROOT, bundle_tag=state)
    entries = {
        entry["path"]: entry
        for entry in inventory["entries"]
        if isinstance(entry, dict)
    }
    schema_paths = (
        "contracts/intent-compliance/veto-class-vocabulary.schema.yaml",
        "contracts/intent-compliance/policy-allowance.schema.yaml",
        "contracts/intent-compliance/policy-allowance-revocation.schema.yaml",
        "contracts/intent-compliance/policy-allowance-registry.schema.yaml",
        "contracts/intent-compliance/compliance-decision.schema.yaml",
    )

    match state:
        case ReleaseState.CURRENT:
            assert set(schema_paths).isdisjoint(entries)
        case ReleaseState.FEATURE:
            for path in schema_paths:
                assert entries[path]["schema_id"].startswith("intent-compliance-")
                assert entries[path]["schema_version"] == 1
        case unreachable:
            assert_never(unreachable)


def test_release_membership_when_intent_registration_is_partial_then_fails_closed(
    tmp_path: Path,
) -> None:
    contract_root = tmp_path / "contracts"
    family_root = contract_root / "hermes-runtime"
    fixture_root = family_root / "fixtures"
    fixture_root.mkdir(parents=True)
    (family_root / "contract-index.yaml").write_text(
        "schema_version: 1\ncontracts: []\n", encoding="utf-8"
    )
    (fixture_root / "index.yaml").write_text(
        "schema_version: 1\ncases: []\n", encoding="utf-8"
    )
    (contract_root / "manifest.yaml").write_text(
        """schema_version: 1
contract_bundle_version: contract-v2.3
contracts:
- id: intent-compliance-veto-class-vocabulary
  path: contracts/intent-compliance/veto-class-vocabulary.schema.yaml
  type: schema
""",
        encoding="utf-8",
    )

    with pytest.raises(ReleaseDependencyError) as error:
        release_membership(tmp_path)

    assert error.value.code == "HGR-RELEASE-INTENT-REGISTRATION-INCOMPLETE"


@pytest.mark.parametrize(
    "surface_path",
    [
        "contracts/intent-compliance/veto-class-vocabulary.schema.yaml",
        "scripts/validate-intent-compliance.py",
        "scripts/intent_compliance/authority_repository.py",
        "tests/intent-compliance/test_release_boundary.py",
    ],
)
def test_release_membership_when_surface_exists_without_registration_then_fails_closed(
    tmp_path: Path,
    surface_path: str,
) -> None:
    contract_root = tmp_path / "contracts"
    family_root = contract_root / "hermes-runtime"
    fixture_root = family_root / "fixtures"
    fixture_root.mkdir(parents=True)
    (family_root / "contract-index.yaml").write_text(
        "schema_version: 1\ncontracts: []\n", encoding="utf-8"
    )
    (fixture_root / "index.yaml").write_text(
        "schema_version: 1\ncases: []\n", encoding="utf-8"
    )
    (contract_root / "manifest.yaml").write_text(
        """schema_version: 1
contract_bundle_version: contract-v2.3
contracts: []
""",
        encoding="utf-8",
    )
    surface = tmp_path / surface_path
    surface.parent.mkdir(parents=True, exist_ok=True)
    surface.write_text("schema_version: 1\n", encoding="utf-8")

    with pytest.raises(ReleaseDependencyError) as error:
        release_membership(tmp_path)

    assert error.value.code == "HGR-RELEASE-INTENT-REGISTRATION-INCOMPLETE"
