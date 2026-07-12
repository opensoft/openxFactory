"""Exact OpenSpec, acceptance-map, evidence, and collected-test parity."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping

_REQUIREMENT = "### Requirement:"
_SCENARIO = "#### Scenario:"
_EMBEDDED_REQUIREMENT_ID = re.compile(r"\b([A-Z][A-Z0-9]*-\d{3})\b")
_EMBEDDED_SCENARIO_ID = re.compile(r"\b([A-Z][A-Z0-9]*-\d{3}-S\d{2})\b")
_FAILURE_KEYS = (
    "count_mismatch",
    "missing",
    "duplicate",
    "dangling",
    "skipped_required",
    "title_mismatch",
)


def extract_openspec_inventory(specs_root: Path) -> dict[str, object]:
    """Extract requirement/scenario titles from exact OpenSpec delta files."""

    requirements: list[dict[str, object]] = []
    for spec_path in sorted(specs_root.rglob("spec.md"), key=lambda path: path.as_posix()):
        capability = spec_path.parent.name
        current: dict[str, object] | None = None
        for raw_line in spec_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line.startswith(_REQUIREMENT):
                title = line[len(_REQUIREMENT) :].strip()
                match = _EMBEDDED_REQUIREMENT_ID.search(title)
                current = {
                    "capability": capability,
                    "title": title,
                    "scenario_titles": [],
                }
                if match:
                    current["id"] = match.group(1)
                requirements.append(current)
            elif line.startswith(_SCENARIO):
                if current is None:
                    raise ValueError(f"scenario appears before a requirement in {spec_path}")
                title = line[len(_SCENARIO) :].strip()
                current["scenario_titles"].append(title)
                match = _EMBEDDED_SCENARIO_ID.search(title)
                if match:
                    current.setdefault("scenario_ids", []).append(match.group(1))
    return {"requirements": requirements}


def _display_requirement(requirement: Mapping[str, object]) -> str:
    return str(
        requirement.get("id")
        or f"{requirement.get('capability')}:{requirement.get('title')}"
    )


def check_parity(
    openspec_inventory: Mapping[str, object],
    acceptance_map: Mapping[str, object],
    evidence_register: Mapping[str, object],
    *,
    collected_node_ids: Iterable[str] = (),
    skipped_node_ids: Iterable[str] = (),
) -> dict[str, list[str]]:
    """Return deterministic categorized parity failures for all required evidence."""

    failures: dict[str, list[str]] = {key: [] for key in _FAILURE_KEYS}
    requirements = list(openspec_inventory.get("requirements", []) or [])
    mappings = list(acceptance_map.get("openspec_parity", []) or [])

    actual_by_key = {
        (str(item.get("capability")), str(item.get("title"))): item
        for item in requirements
        if isinstance(item, Mapping)
    }
    mapped_by_key: dict[tuple[str, str], Mapping[str, object]] = {}
    mapping_ids: list[str] = []
    scenario_ids: list[str] = []
    for mapping in mappings:
        if not isinstance(mapping, Mapping):
            failures["dangling"].append("non-object acceptance mapping")
            continue
        mapping_id = str(mapping.get("id", ""))
        mapping_ids.append(mapping_id)
        key = (str(mapping.get("capability")), str(mapping.get("title")))
        if key in mapped_by_key:
            failures["duplicate"].append(mapping_id or f"{key[0]}:{key[1]}")
        else:
            mapped_by_key[key] = mapping
        scenario_ids.extend(str(item) for item in (mapping.get("scenario_ids", []) or []))

    for mapping_id, count in Counter(mapping_ids).items():
        if mapping_id and count > 1:
            failures["duplicate"].append(mapping_id)
    for scenario_id, count in Counter(scenario_ids).items():
        if count > 1:
            failures["duplicate"].append(scenario_id)

    for key, requirement in actual_by_key.items():
        mapping = mapped_by_key.get(key)
        if mapping is None:
            failures["missing"].append(_display_requirement(requirement))
            continue
        mapped_scenarios = [str(item) for item in (mapping.get("scenario_ids", []) or [])]
        actual_titles = list(requirement.get("scenario_titles", []) or [])
        if len(mapped_scenarios) != len(actual_titles):
            failures["count_mismatch"].append(
                f"{mapping.get('id')}: {len(mapped_scenarios)} mapped scenarios != "
                f"{len(actual_titles)} OpenSpec scenarios"
            )
        embedded_ids = [str(item) for item in (requirement.get("scenario_ids", []) or [])]
        if embedded_ids:
            for missing in sorted(set(embedded_ids) - set(mapped_scenarios)):
                failures["missing"].append(missing)
            for extra in sorted(set(mapped_scenarios) - set(embedded_ids)):
                failures["dangling"].append(extra)

    for key, mapping in mapped_by_key.items():
        if key not in actual_by_key:
            failures["dangling"].append(str(mapping.get("id") or f"{key[0]}:{key[1]}"))

    actual_requirement_count = len(requirements)
    actual_scenario_count = sum(
        len(item.get("scenario_titles", []) or [])
        for item in requirements
        if isinstance(item, Mapping)
    )
    expected_requirement_count = acceptance_map.get("expected_openspec_requirement_count")
    expected_scenario_count = acceptance_map.get("expected_openspec_scenario_count")
    if expected_requirement_count != actual_requirement_count:
        failures["count_mismatch"].append(
            f"requirements: expected {expected_requirement_count}, OpenSpec has "
            f"{actual_requirement_count}"
        )
    if expected_scenario_count != actual_scenario_count:
        failures["count_mismatch"].append(
            f"scenarios: expected {expected_scenario_count}, OpenSpec has "
            f"{actual_scenario_count}"
        )
    if len(mappings) != actual_requirement_count:
        failures["count_mismatch"].append(
            f"acceptance mappings: {len(mappings)} != {actual_requirement_count}"
        )
    if len(scenario_ids) != actual_scenario_count:
        failures["count_mismatch"].append(
            f"acceptance scenarios: {len(scenario_ids)} != {actual_scenario_count}"
        )

    required_scenarios = set(scenario_ids)
    entries = list(evidence_register.get("entries", []) or [])
    evidence_ids = [
        str(entry.get("scenario_id", ""))
        for entry in entries
        if isinstance(entry, Mapping)
    ]
    evidence_counts = Counter(evidence_ids)
    for scenario_id in sorted(required_scenarios - set(evidence_ids)):
        failures["missing"].append(scenario_id)
    for scenario_id in sorted(set(evidence_ids) - required_scenarios):
        failures["dangling"].append(scenario_id)
    for scenario_id, count in evidence_counts.items():
        if scenario_id and count > 1:
            failures["duplicate"].append(scenario_id)

    collected = set(collected_node_ids)
    skipped = set(skipped_node_ids)
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        scenario_id = str(entry.get("scenario_id", ""))
        if entry.get("status") == "skipped":
            failures["skipped_required"].append(scenario_id)
        for node in entry.get("test_node_ids", []) or []:
            node_id = str(node)
            if node_id not in collected:
                failures["dangling"].append(f"{scenario_id} -> {node_id}")
            elif node_id in skipped:
                failures["skipped_required"].append(f"{scenario_id} -> {node_id}")

    for key in failures:
        failures[key] = sorted(set(failures[key]))
    return failures
