"""RED tests for exact OpenSpec/acceptance/evidence parity (T011)."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from scripts.hermes_runtime_validation.acceptance import (
    check_parity,
    extract_openspec_inventory,
)

REQUIREMENTS = (
    ("HCS-001", "hermes-customer-subject-runtime", 3),
    ("HCS-002", "hermes-customer-subject-runtime", 5),
    ("HCS-003", "hermes-customer-subject-runtime", 6),
    ("HCS-004", "hermes-customer-subject-runtime", 4),
    ("HCS-005", "hermes-customer-subject-runtime", 3),
    ("HCS-006", "hermes-customer-subject-runtime", 3),
    ("HGR-001", "hermes-governed-record-integrity", 3),
    ("HGR-002", "hermes-governed-record-integrity", 7),
    ("HGR-003", "hermes-governed-record-integrity", 5),
    ("HGR-004", "hermes-governed-record-integrity", 6),
    ("HGR-005", "hermes-governed-record-integrity", 6),
    ("HGR-006", "hermes-governed-record-integrity", 6),
    ("HGR-007", "hermes-governed-record-integrity", 3),
    ("HGR-008", "hermes-governed-record-integrity", 8),
    ("HGR-009", "hermes-governed-record-integrity", 5),
    ("NJE-004", "neutral-job-envelope", 5),
    ("SCO-002", "shared-contract-ownership", 7),
)


def _write_openspec(specs_root: Path) -> None:
    grouped: dict[str, list[tuple[str, int]]] = {}
    for requirement_id, capability, scenario_count in REQUIREMENTS:
        grouped.setdefault(capability, []).append((requirement_id, scenario_count))
    for capability, requirements in grouped.items():
        lines = ["Status: ratified", "", "## ADDED Requirements", ""]
        for requirement_id, scenario_count in requirements:
            lines.extend(
                [
                    f"### Requirement: Requirement {requirement_id}",
                    "Synthetic normative statement.",
                    "",
                ]
            )
            for number in range(1, scenario_count + 1):
                lines.extend(
                    [
                        f"#### Scenario: Scenario {requirement_id}-S{number:02d}",
                        "- **WHEN** synthetic input is evaluated",
                        "- **THEN** deterministic evidence is required",
                        "",
                    ]
                )
        path = specs_root / capability / "spec.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")


def _acceptance_map() -> dict:
    return {
        "expected_openspec_requirement_count": 17,
        "expected_openspec_scenario_count": 85,
        "openspec_parity": [
            {
                "id": requirement_id,
                "capability": capability,
                "title": f"Requirement {requirement_id}",
                "scenario_ids": [
                    f"{requirement_id}-S{number:02d}"
                    for number in range(1, scenario_count + 1)
                ],
            }
            for requirement_id, capability, scenario_count in REQUIREMENTS
        ],
    }


def _evidence_register() -> tuple[dict, set[str]]:
    entries = []
    nodes = set()
    for requirement in _acceptance_map()["openspec_parity"]:
        for scenario_id in requirement["scenario_ids"]:
            node = f"tests/synthetic/test_acceptance.py::test_{scenario_id.lower()}"
            nodes.add(node)
            entries.append(
                {
                    "scenario_id": scenario_id,
                    "status": "evidenced",
                    "evidence_id": f"TEST-{scenario_id}",
                    "test_node_ids": [node],
                }
            )
    return {"entries": entries}, nodes


def _valid_inputs(tmp_path: Path):
    specs_root = tmp_path / "specs"
    _write_openspec(specs_root)
    inventory = extract_openspec_inventory(specs_root)
    evidence, nodes = _evidence_register()
    return inventory, _acceptance_map(), evidence, nodes


def test_extracts_exact_ratified_17_requirement_85_scenario_inventory(tmp_path: Path) -> None:
    inventory, _, _, _ = _valid_inputs(tmp_path)

    assert len(inventory["requirements"]) == 17
    assert sum(len(item["scenario_titles"]) for item in inventory["requirements"]) == 85


def test_exact_acceptance_and_evidence_parity_has_no_failures(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)

    failures = check_parity(
        inventory,
        acceptance_map,
        evidence,
        collected_node_ids=nodes,
        skipped_node_ids=set(),
    )

    assert all(not items for items in failures.values())


def test_missing_acceptance_mapping_fails(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)
    acceptance_map["openspec_parity"].pop()

    failures = check_parity(inventory, acceptance_map, evidence, collected_node_ids=nodes)

    assert "SCO-002" in failures["missing"]


def test_duplicate_acceptance_mapping_fails(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)
    acceptance_map["openspec_parity"].append(
        deepcopy(acceptance_map["openspec_parity"][0])
    )

    failures = check_parity(inventory, acceptance_map, evidence, collected_node_ids=nodes)

    assert "HCS-001" in failures["duplicate"]


def test_dangling_acceptance_mapping_fails(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)
    acceptance_map["openspec_parity"].append(
        {
            "id": "HCS-999",
            "capability": "hermes-customer-subject-runtime",
            "title": "Requirement HCS-999",
            "scenario_ids": ["HCS-999-S01"],
        }
    )

    failures = check_parity(inventory, acceptance_map, evidence, collected_node_ids=nodes)

    assert "HCS-999" in failures["dangling"]


def test_missing_and_duplicate_evidence_entries_fail(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)
    missing = evidence["entries"].pop()
    duplicate = deepcopy(evidence["entries"][0])
    evidence["entries"].append(duplicate)

    failures = check_parity(inventory, acceptance_map, evidence, collected_node_ids=nodes)

    assert missing["scenario_id"] in failures["missing"]
    assert duplicate["scenario_id"] in failures["duplicate"]


def test_dangling_test_node_fails(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)
    entry = evidence["entries"][0]
    original = entry["test_node_ids"][0]
    entry["test_node_ids"] = ["tests/synthetic/test_missing.py::test_absent"]
    nodes.remove(original)

    failures = check_parity(inventory, acceptance_map, evidence, collected_node_ids=nodes)

    assert entry["scenario_id"] in " ".join(failures["dangling"])


def test_skipped_required_evidence_fails(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)
    node = evidence["entries"][0]["test_node_ids"][0]

    failures = check_parity(
        inventory,
        acceptance_map,
        evidence,
        collected_node_ids=nodes,
        skipped_node_ids={node},
    )

    assert evidence["entries"][0]["scenario_id"] in " ".join(
        failures["skipped_required"]
    )


def test_expected_counts_cannot_be_self_redefined(tmp_path: Path) -> None:
    inventory, acceptance_map, evidence, nodes = _valid_inputs(tmp_path)
    acceptance_map["expected_openspec_scenario_count"] = 84

    failures = check_parity(inventory, acceptance_map, evidence, collected_node_ids=nodes)

    assert failures["count_mismatch"]
