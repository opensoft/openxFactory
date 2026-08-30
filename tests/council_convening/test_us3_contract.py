from __future__ import annotations

import re
from collections.abc import Mapping

import pytest

from tests.council_convening.support import (
    ACCEPTANCE_MAP_PATH,
    FEATURE_SPEC_PATH,
    OPENSPEC_SPEC_PATH,
    REPOSITORY_ROOT,
    AcceptanceMap,
    GateEntry,
    load_acceptance_map,
    mapping_at,
    markdown_ids,
    valid_convening,
    validation_keywords,
)


def _successor_records() -> Mapping[str, str]:
    tasks_path = (
        REPOSITORY_ROOT
        / "openspec"
        / "changes"
        / "add-resolved-council-seats"
        / "tasks.md"
    )
    records: dict[str, str] = {}
    for match in re.finditer(
        r"^  - `([a-z0-9_.-]+): ([^`]+)`$",
        tasks_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    ):
        key, value = match.groups()
        records[key] = value
    return records


@pytest.mark.parametrize(
    ("path", "field"),
    [
        ((), "private_key"),
        (("required_seats_provenance",), "root_key"),
        (("required_seats_provenance", "resolution"), "shared_key"),
        ((), "roster_seed"),
        ((), "reconstruct_required_seats"),
        (("required_seats_provenance",), "required_seats_seed"),
    ],
)
def test_closed_convening_refuses_key_and_roster_reconstruction_fields(
    path: tuple[str, ...],
    field: str,
) -> None:
    # Given a valid neutral convening carrying prohibited key or compatibility state
    document = valid_convening()
    mapping_at(document, *path)[field] = "forbidden"

    # When the Draft 2020-12 contract validates the mutated boundary
    keywords = validation_keywords(document)

    # Then structural closure rejects the uncontracted field.
    assert keywords & {"additionalProperties", "unevaluatedProperties"}


def _blocking_external_gates(acceptance_map: AcceptanceMap) -> tuple[GateEntry, ...]:
    return tuple(
        gate
        for gate in acceptance_map.gates
        if gate.external and gate.blocks_on_failure and gate.owner != "openxFactory"
    )


def test_runtime_requirements_map_to_blocking_external_or_cutover_gates() -> None:
    # Given machine-readable successor and coordinated-cutover gates
    gates = _blocking_external_gates(load_acceptance_map())
    required = {f"FR-{number:03d}" for number in range(8, 15)}

    # When explicit requirement-to-gate mappings are combined
    mapped = {
        requirement_id for gate in gates for requirement_id in gate.requirement_ids
    }

    # Then every runtime-only requirement has an owning external blocking gate.
    assert required <= mapped


def test_runtime_outcomes_map_to_blocking_external_or_cutover_gates() -> None:
    # Given machine-readable successor and coordinated-cutover gates
    gates = _blocking_external_gates(load_acceptance_map())
    required = {f"SC-{number:03d}" for number in range(3, 8)}

    # When explicit outcome-to-gate mappings are combined
    mapped = {outcome_id for gate in gates for outcome_id in gate.outcome_ids}

    # Then every runtime-only outcome has an owning external blocking gate.
    assert required <= mapped


def test_successor_records_pin_exact_features_and_provider_dependency() -> None:
    # Given the OpenSpec handoff ledger
    records = _successor_records()

    # When its structured successor records are inspected
    successor_records = {
        key: value for key, value in records.items() if key.startswith("successor.")
    }

    # Then both exact features pin the ratified neutral provider contract.
    assert successor_records == {
        "successor.codexfactory.feature": "017-resolve-council-seat-roster",
        "successor.codexfactory.governed_workflow_subject": (
            "opensoft/codexFactory/.github/workflows/"
            "council-lane-reusable.yml@refs/heads/main"
        ),
        "successor.codexfactory.provider_dependency": (
            "opensoft/openxFactory:add-resolved-council-seats:council-convening"
        ),
        "successor.hermes_install.feature": "017-validate-freeze-council-roster",
        "successor.hermes_install.provider_dependency": (
            "opensoft/openxFactory:add-resolved-council-seats:council-convening"
        ),
    }


def test_unavailable_successor_and_live_evidence_remains_open() -> None:
    # Given the OpenSpec handoff ledger
    records = _successor_records()

    # When every external evidence state is collected
    evidence_states = {
        key: value for key, value in records.items() if key.startswith("evidence.")
    }

    # Then no unperformed runtime, signing, identity, deployment, or merge act is claimed.
    assert evidence_states == {
        "evidence.codexfactory_signing": "open",
        "evidence.deployment": "open",
        "evidence.hermes_runtime": "open",
        "evidence.live_oidc": "open",
        "evidence.merged_successors": "open",
    }


def test_acceptance_map_has_exact_governing_spec_parity() -> None:
    assert ACCEPTANCE_MAP_PATH.is_file()
    acceptance_map = load_acceptance_map()
    mapped_requirements = acceptance_map.openspec_parity
    openspec_requirements = markdown_ids(OPENSPEC_SPEC_PATH, r"^### Requirement: .+$")
    openspec_scenarios = markdown_ids(OPENSPEC_SPEC_PATH, r"^#### Scenario: .+$")
    mapped_scenarios = {
        scenario_id
        for requirement in mapped_requirements
        for scenario_id in requirement.scenario_ids
    }

    assert acceptance_map.expected_openspec_requirement_count == 3
    assert acceptance_map.expected_openspec_scenario_count == 11
    assert len(mapped_requirements) == len(openspec_requirements) == 3
    assert len(mapped_scenarios) == len(openspec_scenarios) == 11


def test_acceptance_map_has_exact_feature_requirement_and_outcome_parity() -> None:
    acceptance_map = load_acceptance_map()
    feature_requirements = markdown_ids(FEATURE_SPEC_PATH, r"^- \*\*(FR-\d{3})\*\*:")
    feature_outcomes = markdown_ids(FEATURE_SPEC_PATH, r"^- \*\*(SC-\d{3})\*\*:")
    mapped_requirements = {
        requirement
        for story in acceptance_map.stories
        for requirement in story.requirements
    }
    mapped_outcomes = {
        outcome for story in acceptance_map.stories for outcome in story.outcomes
    }

    assert mapped_requirements == feature_requirements
    assert mapped_outcomes == feature_outcomes
    assert len(feature_requirements) == 14
    assert len(feature_outcomes) == 7
