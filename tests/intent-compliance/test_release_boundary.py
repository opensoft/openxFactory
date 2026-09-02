from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import assert_never

import pytest

from scripts.hermes_runtime_validation.release import (
    INTENT_REQUIRED_REGISTRATIONS,
    ReleaseDependencyError,
    build_release_inventory,
    release_membership,
)

ROOT = Path(__file__).resolve().parents[2]


class ReleaseState(StrEnum):
    """The bundle values this boundary test has been told how to classify.

    A bundle this enum does not name fails LOUDLY at ``_release_state`` rather
    than being classified by inference, and that tripwire is deliberate: the
    library floor (``INTENT_RELEASE_FLOOR``) is an at-or-after comparison, so
    nothing here would notice a bump on its own, and the whole point of this
    file is that the family's release membership and its manifest registration
    move TOGETHER. Every cut past the floor therefore states, by hand and on
    the record, which side of the boundary its bundle falls on. Advanced at the
    ``contract-v2.4`` cut (add-binding-consumer-identity's §5 release ritual):
    v2.4 is past the floor, the family is registered and present, so it is
    classified with the introducing release and asserts the same membership.
    Advanced again at the ``contract-v2.5`` cut (add-signed-execution-chain task
    4.7) on the same reading, and for the same reason it is a hand act: that cut
    registers a DIFFERENT family, so nothing about it touches intent-compliance's
    membership — which is exactly the fact a human has to state, because the
    library cannot tell "unchanged" from "unnoticed".
    Advanced again at the ``contract-v2.6`` cut (add-chain-attestation task
    5.9) on the same reading: that cut extends the signed-execution-chain
    family and touches no intent-compliance member, so the membership this
    file asserts is UNCHANGED — stated by hand, on the record, because that
    is the one fact the library cannot observe.
    """

    CURRENT = "contract-v2.1"
    FEATURE = "contract-v2.3"
    FEATURE_SUCCESSOR = "contract-v2.4"
    FEATURE_SUCCESSOR_2 = "contract-v2.5"
    FEATURE_SUCCESSOR_3 = "contract-v2.6"


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


def _write_release_fixture(
    root: Path,
    bundle_tag: str,
    registrations: tuple[tuple[str, str, str], ...] = (),
) -> None:
    family_root = root / "contracts" / "hermes-runtime"
    fixture_root = family_root / "fixtures"
    fixture_root.mkdir(parents=True)
    (family_root / "contract-index.yaml").write_text(
        "schema_version: 1\ncontracts: []\n", encoding="utf-8"
    )
    (fixture_root / "index.yaml").write_text(
        "schema_version: 1\ncases: []\n", encoding="utf-8"
    )
    registration_yaml = "".join(
        f"- id: {identifier}\n  path: {path}\n  type: {artifact_type}\n"
        "  schema_version: 1\n"
        for identifier, path, artifact_type in registrations
    )
    contracts_yaml = (
        f"contracts:\n{registration_yaml}" if registration_yaml else "contracts: []\n"
    )
    (root / "contracts" / "manifest.yaml").write_text(
        f"schema_version: 1\ncontract_bundle_version: {bundle_tag}\n{contracts_yaml}",
        encoding="utf-8",
    )


def _write_registration_targets(root: Path, excluded_path: str | None = None) -> None:
    for _, path, _ in INTENT_REQUIRED_REGISTRATIONS:
        if path == excluded_path:
            continue
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("schema_version: 1\n", encoding="utf-8")


def test_release_membership_when_registration_changes_then_transition_is_atomic() -> (
    None
):
    members = {path.as_posix() for path in release_membership(ROOT)}
    feature_members = _feature_release_members()

    match _release_state():
        case ReleaseState.CURRENT:
            assert feature_members.isdisjoint(members)
        case (
            ReleaseState.FEATURE
            | ReleaseState.FEATURE_SUCCESSOR
            | ReleaseState.FEATURE_SUCCESSOR_2
            | ReleaseState.FEATURE_SUCCESSOR_3
        ):
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
        case (
            ReleaseState.FEATURE
            | ReleaseState.FEATURE_SUCCESSOR
            | ReleaseState.FEATURE_SUCCESSOR_2
            | ReleaseState.FEATURE_SUCCESSOR_3
        ):
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


@pytest.mark.parametrize(
    "bundle_tag", ["contract-v2.3", "contract-v2.4", "contract-v3.0"]
)
def test_release_membership_when_v23_or_successor_omits_family_then_fails_closed(
    tmp_path: Path,
    bundle_tag: str,
) -> None:
    _write_release_fixture(tmp_path, bundle_tag)

    with pytest.raises(ReleaseDependencyError) as error:
        release_membership(tmp_path)

    assert error.value.code == "HGR-RELEASE-INTENT-REGISTRATION-INCOMPLETE"


def test_release_membership_allows_absent_family_before_v23(tmp_path: Path) -> None:
    _write_release_fixture(tmp_path, "contract-v2.2")

    members = {path.as_posix() for path in release_membership(tmp_path)}

    assert not any("intent-compliance" in path for path in members)


def test_release_fails_when_registered_intent_schema_is_missing(tmp_path: Path) -> None:
    missing_path = "contracts/intent-compliance/policy-allowance.schema.yaml"
    _write_release_fixture(tmp_path, "contract-v2.3", INTENT_REQUIRED_REGISTRATIONS)
    _write_registration_targets(tmp_path, missing_path)

    with pytest.raises(ReleaseDependencyError) as error:
        release_membership(tmp_path)

    assert error.value.code == "HGR-RELEASE-INTENT-MEMBER-MISSING"
    assert missing_path in str(error.value)


def test_release_fails_when_intent_registration_set_is_not_exact(
    tmp_path: Path,
) -> None:
    extra_path = "contracts/intent-compliance/extra.schema.yaml"
    extra_registration = ("intent-compliance-extra", extra_path, "schema")
    _write_release_fixture(
        tmp_path,
        "contract-v2.3",
        (*INTENT_REQUIRED_REGISTRATIONS, extra_registration),
    )
    _write_registration_targets(tmp_path)
    extra = tmp_path / extra_path
    extra.parent.mkdir(parents=True, exist_ok=True)
    extra.write_text("schema_version: 1\n", encoding="utf-8")

    with pytest.raises(ReleaseDependencyError) as error:
        release_membership(tmp_path)

    assert error.value.code == "HGR-RELEASE-INTENT-REGISTRATION-INCOMPLETE"
