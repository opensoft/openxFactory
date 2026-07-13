#!/usr/bin/env python3
"""Deterministic command-line entrypoint for Hermes runtime contract checks."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any

# ``python scripts/validate-hermes-runtime-contracts.py`` otherwise places only
# the scripts directory on sys.path.  Add the selected implementation's repo
# root so this thin entrypoint uses the reusable validation package.
_ENTRYPOINT_REPO = Path(__file__).resolve().parents[1]
if str(_ENTRYPOINT_REPO) not in sys.path:
    sys.path.insert(0, str(_ENTRYPOINT_REPO))

from scripts.hermes_runtime_validation.acceptance import (  # noqa: E402
    check_parity,
    extract_openspec_inventory,
)
from scripts.hermes_runtime_validation.catalog import (  # noqa: E402
    CatalogError,
    ContractCatalog,
    load_contract_catalog,
)
from scripts.hermes_runtime_validation.fixtures import (  # noqa: E402
    dependency_order,
    validate_index,
)
from scripts.hermes_runtime_validation.schema_registry import (  # noqa: E402
    SchemaRegistryError,
    build_offline_registry,
)
from scripts.hermes_runtime_validation import (  # noqa: E402
    consumer_handoff,
    domain_regression,
    release,
)
from scripts.hermes_runtime_validation.loader import (  # noqa: E402
    YamlLoadError,
    load_yaml_document,
)

FAMILY_PATH = PurePosixPath("contracts/hermes-runtime")
FIXTURE_INDEX_PATH = "fixtures/index.yaml"
FIXTURE_ROOT_PATH = "contracts/hermes-runtime/fixtures"
TEST_ROOT_PATH = "tests/hermes_runtime_contracts"
CATALOG_RELATIVE_PATH = "contracts/hermes-runtime/contract-index.yaml"
DOMAIN_REGRESSION_INVENTORY_PATH = (
    "contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml"
)
CHANGE_ID = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,126}[a-z0-9])?$")

REQUIRED_CATALOG_MEMBERS = {
    "hermes-runtime-contract-index": ("contract-index.yaml", "contract-index"),
    "hermes-runtime-acceptance-map": ("acceptance-map.yaml", "acceptance-map"),
    "hermes-runtime-evidence-register": ("evidence-register.yaml", "evidence-register"),
    "hermes-runtime-fixture-index": (FIXTURE_INDEX_PATH, "fixture-index"),
    "shared-definitions": ("shared-definitions.schema.yaml", "schema"),
}

EXPECTED_DOCUMENT_KINDS = {
    "hermes-runtime-acceptance-map": "openxfactory-hermes-runtime-acceptance-map",
    "hermes-runtime-evidence-register": "openxfactory-hermes-runtime-evidence-register",
    "hermes-runtime-fixture-index": "openxfactory-hermes-runtime-fixture-index",
}

PARITY_CODES = {
    "count_mismatch": "HRC-PARITY-COUNT-MISMATCH",
    "missing": "HRC-PARITY-MISSING",
    "duplicate": "HRC-PARITY-DUPLICATE",
    "dangling": "HRC-PARITY-DANGLING",
    "skipped_required": "HRC-PARITY-SKIPPED-REQUIRED",
    "title_mismatch": "HRC-PARITY-TITLE-MISMATCH",
}


def classify_exit_code(
    findings: Sequence[Mapping[str, Any]],
    *,
    strict: bool,
    dependency_error: bool = False,
) -> int:
    """Apply the stable 0=pass, 1=finding, 2=harness/dependency contract."""

    if dependency_error:
        return 2
    severities = {str(finding.get("severity", "error")) for finding in findings}
    if "error" in severities or (strict and "warning" in severities):
        return 1
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--case", dest="case_id")
    parser.add_argument(
        "--phase", choices=("structural", "semantic", "all"), default="all"
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--require-candidate", action="store_true")
    parser.add_argument("--require-realization", action="store_true")
    parser.add_argument("--repo", type=Path)
    parser.add_argument(
        "--domain-repo", action="append", default=[], metavar="REPO=CHECKOUT"
    )
    parser.add_argument("--domain-repo-root", type=Path)
    parser.add_argument("--handoff-receipt", type=Path)
    parser.add_argument(
        "--consumer-repo", action="append", default=[], metavar="REPO=CHECKOUT"
    )
    parser.add_argument("--consumer-repo-root", type=Path)
    return parser


def _finding(
    code: str,
    message: str,
    *,
    case_id: str = "",
    path: str = "",
    severity: str = "error",
) -> dict[str, str]:
    return {
        "code": code,
        "severity": severity,
        "case_id": case_id,
        "path": path,
        "message": message,
    }


def _normalize_findings(
    findings: Sequence[Mapping[str, object]],
) -> list[dict[str, str]]:
    return [
        {
            "code": str(item.get("code", "HRC-UNKNOWN-FINDING")),
            "severity": str(item.get("severity", "error")),
            "case_id": str(item.get("case_id", "")),
            "path": str(item.get("path", "")),
            "message": str(item.get("message", "validation failed")),
        }
        for item in findings
    ]


def _git_root(path: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    try:
        return Path(result.stdout.strip()).resolve(strict=True)
    except OSError:
        return None


def _render(
    findings: list[dict[str, str]],
    *,
    mode: str,
    as_json: bool,
    exit_code: int,
    selection: Mapping[str, object],
    summary: Mapping[str, int],
) -> None:
    findings.sort(
        key=lambda item: (
            item["case_id"],
            item["path"],
            item["code"],
            item["message"],
        )
    )
    if as_json:
        payload = {
            "exit_code": exit_code,
            "findings": findings,
            "mode": mode,
            "selection": dict(selection),
            "status": "pass" if exit_code == 0 else "error",
            "summary": dict(summary),
        }
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return
    if not findings:
        print(
            "Hermes runtime contracts: pass "
            f"({summary.get('catalog_members', 0)} contracts, "
            f"{summary.get('schema_members', 0)} schemas, "
            f"{summary.get('fixture_cases', 0)} fixtures, "
            f"{summary.get('openspec_requirements', 0)} requirements, "
            f"{summary.get('openspec_scenarios', 0)} scenarios, "
            f"{summary.get('collected_test_nodes', 0)} tests collected)"
        )
        return
    for finding in findings:
        case = f" case={finding['case_id']}" if finding["case_id"] else ""
        path = f" path={finding['path']}" if finding["path"] else ""
        print(
            f"{finding['code']} {finding['severity']}{case}{path}: "
            f"{finding['message']}"
        )


def _catalog_document(
    catalog: ContractCatalog,
    contract_id: str,
    findings: list[dict[str, str]],
) -> Mapping[str, object] | None:
    expected_path, expected_type = REQUIRED_CATALOG_MEMBERS[contract_id]
    member = catalog.by_id.get(contract_id)
    if member is None:
        findings.append(
            _finding(
                "HRC-CATALOG-REQUIRED-MEMBER",
                f"required catalog member {contract_id!r} is absent",
                path="contracts/hermes-runtime/contract-index.yaml",
            )
        )
        return None
    if member.path != expected_path or member.type != expected_type:
        findings.append(
            _finding(
                "HRC-CATALOG-REQUIRED-MEMBER",
                f"{contract_id!r} must be {expected_type} at {expected_path}",
                path=f"contracts/hermes-runtime/{member.path}",
            )
        )
        return None
    try:
        document = catalog.document_for(member)
    except CatalogError as error:
        findings.append(
            _finding(
                "HRC-CATALOG-DOCUMENT",
                str(error),
                path=f"contracts/hermes-runtime/{expected_path}",
            )
        )
        return None
    if not isinstance(document, Mapping):
        findings.append(
            _finding(
                "HRC-CATALOG-DOCUMENT",
                "catalog document must be a mapping",
                path=f"contracts/hermes-runtime/{expected_path}",
            )
        )
        return None
    expected_kind = EXPECTED_DOCUMENT_KINDS.get(contract_id)
    if expected_kind is not None and document.get("kind") != expected_kind:
        findings.append(
            _finding(
                "HRC-CATALOG-DOCUMENT-KIND",
                f"expected kind {expected_kind!r}",
                path=f"contracts/hermes-runtime/{expected_path}",
            )
        )
    return document


def _schema_coverage_findings(
    catalog: ContractCatalog, family_root: Path
) -> list[dict[str, str]]:
    cataloged = {entry.path for entry in catalog.schema_entries()}
    actual: set[str] = set()
    findings: list[dict[str, str]] = []
    for path in family_root.rglob("*.schema.yaml"):
        relative = path.relative_to(family_root).as_posix()
        if path.is_symlink() or not path.is_file():
            findings.append(
                _finding(
                    "HRC-CATALOG-SCHEMA-NONREGULAR",
                    "schema family members must be regular non-symlink files",
                    path=f"contracts/hermes-runtime/{relative}",
                )
            )
        else:
            actual.add(relative)
    for relative in sorted(actual - cataloged):
        findings.append(
            _finding(
                "HRC-CATALOG-SCHEMA-UNINDEXED",
                "schema file is not a canonical catalog member",
                path=f"contracts/hermes-runtime/{relative}",
            )
        )
    for relative in sorted(cataloged - actual):
        findings.append(
            _finding(
                "HRC-CATALOG-SCHEMA-MISSING",
                "cataloged schema file is unavailable",
                path=f"contracts/hermes-runtime/{relative}",
            )
        )
    return findings


def _fixture_coverage_findings(
    fixture_index: Mapping[str, object], fixture_root: Path
) -> list[dict[str, str]]:
    indexed: set[str] = set()
    for case in fixture_index.get("cases", []) or []:
        if isinstance(case, Mapping):
            indexed.update(str(path) for path in (case.get("inputs", []) or []))
    actual = {
        path.relative_to(fixture_root).as_posix()
        for path in fixture_root.rglob("*.yaml")
        if path.name != "index.yaml" and path.is_file() and not path.is_symlink()
    }
    findings: list[dict[str, str]] = []
    for relative in sorted(actual - indexed):
        findings.append(
            _finding(
                "HRC-FIXTURE-UNINDEXED",
                "fixture YAML is not owned by an indexed case",
                path=f"{FIXTURE_ROOT_PATH}/{relative}",
            )
        )
    return findings


def collect_pytest_node_ids(repo_root: Path) -> tuple[str, ...]:
    """Collect real pytest node IDs without executing a test body."""

    test_root = repo_root / TEST_ROOT_PATH
    if not test_root.is_dir():
        raise FileNotFoundError(TEST_ROOT_PATH)
    environment = os.environ.copy()
    environment.update(
        {
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PYTEST_ADDOPTS": "",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "TZ": "UTC",
        }
    )
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-p",
                "no:cacheprovider",
                "--collect-only",
                "-q",
                TEST_ROOT_PATH,
            ],
            cwd=repo_root,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError("pytest collection dependency is unavailable") from error
    if completed.returncode != 0:
        raise RuntimeError(f"pytest collection failed with exit {completed.returncode}")
    nodes = tuple(
        sorted(
            {
                line.strip()
                for line in completed.stdout.splitlines()
                if line.startswith("tests/") and "::" in line
            }
        )
    )
    if not nodes:
        raise RuntimeError("pytest collection returned no Hermes runtime nodes")
    return nodes


def _validate_ratified_inventory(
    repo_root: Path,
    governed_change: object,
    findings: list[dict[str, str]],
) -> Mapping[str, object] | None:
    if not isinstance(governed_change, str) or not CHANGE_ID.fullmatch(governed_change):
        findings.append(
            _finding(
                "HRC-OPENSPEC-CHANGE-ID",
                "governed_change must be one canonical change identifier",
                path="contracts/hermes-runtime/fixtures/index.yaml",
            )
        )
        return None
    specs_root = repo_root / "openspec/changes" / governed_change / "specs"
    if not specs_root.is_dir():
        return None
    spec_paths = sorted(specs_root.rglob("spec.md"), key=lambda path: path.as_posix())
    if not spec_paths:
        return None
    for spec_path in spec_paths:
        try:
            lines = spec_path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as error:
            findings.append(
                _finding(
                    "HRC-OPENSPEC-READ",
                    str(error),
                    path=spec_path.relative_to(repo_root).as_posix(),
                )
            )
            continue
        status = next((line.strip() for line in lines if line.strip()), "")
        if status != "Status: ratified":
            findings.append(
                _finding(
                    "HRC-OPENSPEC-NOT-RATIFIED",
                    "only ratified delta specs may define the acceptance inventory",
                    path=spec_path.relative_to(repo_root).as_posix(),
                )
            )
    if findings:
        return None
    try:
        return extract_openspec_inventory(specs_root)
    except (OSError, UnicodeError, ValueError) as error:
        findings.append(
            _finding(
                "HRC-OPENSPEC-INVENTORY",
                str(error),
                path=specs_root.relative_to(repo_root).as_posix(),
            )
        )
        return None


def _cross_document_findings(
    fixture_index: Mapping[str, object],
    acceptance_map: Mapping[str, object],
    evidence_register: Mapping[str, object],
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    governed_changes = {
        str(document.get("governed_change", ""))
        for document in (fixture_index, acceptance_map, evidence_register)
    }
    if len(governed_changes) != 1 or "" in governed_changes:
        findings.append(
            _finding(
                "HRC-GOVERNED-CHANGE-MISMATCH",
                "fixture, acceptance, and evidence documents must name one exact change",
                path="contracts/hermes-runtime",
            )
        )
    if acceptance_map.get("fixture_index") != FIXTURE_INDEX_PATH:
        findings.append(
            _finding(
                "HRC-ACCEPTANCE-REFERENCE",
                f"fixture_index must equal {FIXTURE_INDEX_PATH!r}",
                path="contracts/hermes-runtime/acceptance-map.yaml",
            )
        )
    if acceptance_map.get("evidence_register") != "evidence-register.yaml":
        findings.append(
            _finding(
                "HRC-ACCEPTANCE-REFERENCE",
                "evidence_register must equal 'evidence-register.yaml'",
                path="contracts/hermes-runtime/acceptance-map.yaml",
            )
        )
    if evidence_register.get("expected_scenario_count") != acceptance_map.get(
        "expected_openspec_scenario_count"
    ):
        findings.append(
            _finding(
                "HRC-EVIDENCE-COUNT-MISMATCH",
                "evidence and acceptance expected scenario counts must agree",
                path="contracts/hermes-runtime/evidence-register.yaml",
            )
        )

    requirement_ids: set[str] = set()
    scenario_metadata: dict[str, tuple[str, str]] = {}
    for mapping in acceptance_map.get("openspec_parity", []) or []:
        if not isinstance(mapping, Mapping):
            continue
        requirement_id = str(mapping.get("id", ""))
        requirement_ids.add(requirement_id)
        scenarios = list(mapping.get("scenario_ids", []) or [])
        titles = list(mapping.get("scenario_titles", []) or [])
        for index, scenario_id in enumerate(scenarios):
            title = str(titles[index]) if index < len(titles) else ""
            scenario_metadata[str(scenario_id)] = (requirement_id, title)

    case_ids: set[str] = set()
    for position, case in enumerate(fixture_index.get("cases", []) or []):
        if not isinstance(case, Mapping):
            continue
        case_id = str(case.get("case_id", ""))
        case_ids.add(case_id)
        if not case.get("evidence_id"):
            findings.append(
                _finding(
                    "HRC-FIXTURE-EVIDENCE-ID",
                    "every fixture case requires an evidence_id",
                    case_id=case_id,
                    path=f"contracts/hermes-runtime/fixtures/index.yaml:cases[{position}]",
                )
            )
        for requirement_id in case.get("requirement_ids", []) or []:
            if str(requirement_id) not in requirement_ids:
                findings.append(
                    _finding(
                        "HRC-FIXTURE-REQUIREMENT-DANGLING",
                        f"unknown requirement {requirement_id!r}",
                        case_id=case_id,
                        path="requirement_ids",
                    )
                )
        for scenario_id in case.get("scenario_ids", []) or []:
            if str(scenario_id) not in scenario_metadata:
                findings.append(
                    _finding(
                        "HRC-FIXTURE-SCENARIO-DANGLING",
                        f"unknown scenario {scenario_id!r}",
                        case_id=case_id,
                        path="scenario_ids",
                    )
                )

    for position, entry in enumerate(evidence_register.get("entries", []) or []):
        if not isinstance(entry, Mapping):
            findings.append(
                _finding(
                    "HRC-EVIDENCE-ENTRY-TYPE",
                    "evidence entries must be mappings",
                    path=f"contracts/hermes-runtime/evidence-register.yaml:entries[{position}]",
                )
            )
            continue
        scenario_id = str(entry.get("scenario_id", ""))
        expected = scenario_metadata.get(scenario_id)
        if expected is not None and (
            entry.get("requirement_id") != expected[0]
            or entry.get("scenario_title") != expected[1]
        ):
            findings.append(
                _finding(
                    "HRC-EVIDENCE-METADATA-MISMATCH",
                    "evidence requirement and title must exactly repeat acceptance metadata",
                    path=f"contracts/hermes-runtime/evidence-register.yaml:entries[{position}]",
                )
            )
        fixture_refs = entry.get("fixture_case_ids", []) or []
        if not isinstance(fixture_refs, list):
            findings.append(
                _finding(
                    "HRC-EVIDENCE-FIXTURE-TYPE",
                    "fixture_case_ids must be a list",
                    path=f"contracts/hermes-runtime/evidence-register.yaml:entries[{position}]",
                )
            )
        else:
            for fixture_id in fixture_refs:
                if str(fixture_id) not in case_ids:
                    findings.append(
                        _finding(
                            "HRC-EVIDENCE-FIXTURE-DANGLING",
                            f"unknown fixture case {fixture_id!r}",
                            path=f"contracts/hermes-runtime/evidence-register.yaml:entries[{position}]",
                        )
                    )
        nodes = entry.get("test_node_ids", []) or []
        if not isinstance(nodes, list) or any(
            not isinstance(node, str) or not node for node in nodes
        ):
            findings.append(
                _finding(
                    "HRC-EVIDENCE-NODE-TYPE",
                    "test_node_ids must be a list of non-empty node IDs",
                    path=f"contracts/hermes-runtime/evidence-register.yaml:entries[{position}]",
                )
            )
        elif len(nodes) != len(set(nodes)):
            findings.append(
                _finding(
                    "HRC-EVIDENCE-NODE-DUPLICATE",
                    "one evidence entry cannot repeat a test node ID",
                    path=f"contracts/hermes-runtime/evidence-register.yaml:entries[{position}]",
                )
            )
    return findings


def _selection(
    fixture_index: Mapping[str, object],
    *,
    case_id: str | None,
    phase: str,
) -> tuple[dict[str, object], list[dict[str, str]], bool]:
    cases = {
        str(case.get("case_id")): case
        for case in fixture_index.get("cases", []) or []
        if isinstance(case, Mapping) and isinstance(case.get("case_id"), str)
    }
    findings: list[dict[str, str]] = []
    dependency_error = False
    if case_id is not None:
        selected = cases.get(case_id)
        if selected is None:
            findings.append(
                _finding(
                    "HRC-CASE-NOT-INDEXED",
                    "the selected case is not present in the fixture index",
                    case_id=case_id,
                    path=f"{FIXTURE_ROOT_PATH}/index.yaml",
                )
            )
            dependency_error = True
            case_ids: tuple[str, ...] = ()
        elif selected.get("phase") == "database":
            findings.append(
                _finding(
                    "HRC-CASE-DATABASE-RUNNER-REQUIRED",
                    "database cases execute through run-hermes-runtime-postgres-tests.sh",
                    case_id=case_id,
                    path="phase",
                )
            )
            dependency_error = True
            case_ids = ()
        elif phase != "all" and selected.get("phase") != phase:
            findings.append(
                _finding(
                    "HRC-CASE-PHASE-MISMATCH",
                    f"selected case is phase {selected.get('phase')!r}, not {phase!r}",
                    case_id=case_id,
                    path="phase",
                )
            )
            dependency_error = True
            case_ids = ()
        else:
            try:
                case_ids = dependency_order(fixture_index, selected_case_ids=[case_id])
            except ValueError as error:
                findings.append(
                    _finding(
                        "HRC-CASE-DEPENDENCY",
                        str(error),
                        case_id=case_id,
                        path="depends_on",
                    )
                )
                dependency_error = True
                case_ids = ()
    else:
        selected_phases = {"structural", "semantic"} if phase == "all" else {phase}
        case_ids = tuple(
            sorted(
                identifier
                for identifier, case in cases.items()
                if case.get("phase") in selected_phases
            )
        )
    return (
        {"case_id": case_id, "case_ids": list(case_ids), "phase": phase},
        findings,
        dependency_error,
    )


def _validate_repository(
    repo_root: Path,
    *,
    case_id: str | None,
    phase: str,
) -> tuple[list[dict[str, str]], bool, dict[str, object], dict[str, int]]:
    findings: list[dict[str, str]] = []
    dependency_error = False
    selection: dict[str, object] = {"case_id": case_id, "case_ids": [], "phase": phase}
    summary = {
        "catalog_members": 0,
        "schema_members": 0,
        "fixture_cases": 0,
        "openspec_requirements": 0,
        "openspec_scenarios": 0,
        "collected_test_nodes": 0,
    }
    family_root = repo_root.joinpath(*FAMILY_PATH.parts)
    catalog_path = family_root / "contract-index.yaml"
    if not family_root.is_dir() or not catalog_path.is_file():
        if case_id:
            findings.append(
                _finding(
                    "HRC-CASE-NOT-INDEXED",
                    "the selected case is not present in an available fixture index",
                    case_id=case_id,
                    path=f"{FIXTURE_ROOT_PATH}/index.yaml",
                )
            )
        else:
            findings.append(
                _finding(
                    "HRC-HARNESS-CATALOG-MISSING",
                    "canonical Hermes runtime contract catalog is unavailable",
                    path="contracts/hermes-runtime/contract-index.yaml",
                )
            )
        return findings, True, selection, summary

    try:
        catalog = load_contract_catalog(catalog_path, family_root)
    except CatalogError as error:
        findings.append(
            _finding(
                "HRC-CATALOG-INVALID",
                str(error),
                path="contracts/hermes-runtime/contract-index.yaml",
            )
        )
        return findings, False, selection, summary
    summary["catalog_members"] = len(catalog)
    summary["schema_members"] = len(catalog.schema_entries())
    findings.extend(_schema_coverage_findings(catalog, family_root))
    try:
        build_offline_registry(catalog)
    except SchemaRegistryError as error:
        findings.append(
            _finding(
                "HRC-SCHEMA-REGISTRY",
                str(error),
                path="contracts/hermes-runtime/contract-index.yaml",
            )
        )

    documents: dict[str, Mapping[str, object]] = {}
    for contract_id in REQUIRED_CATALOG_MEMBERS:
        document = _catalog_document(catalog, contract_id, findings)
        if document is not None:
            documents[contract_id] = document
    required_documents = {
        "hermes-runtime-fixture-index",
        "hermes-runtime-acceptance-map",
        "hermes-runtime-evidence-register",
    }
    if findings or not required_documents <= documents.keys():
        return _normalize_findings(findings), dependency_error, selection, summary

    fixture_index = documents["hermes-runtime-fixture-index"]
    acceptance_map = documents["hermes-runtime-acceptance-map"]
    evidence_register = documents["hermes-runtime-evidence-register"]
    summary["fixture_cases"] = len(list(fixture_index.get("cases", []) or []))
    if fixture_index.get("fixture_root") != FIXTURE_ROOT_PATH:
        findings.append(
            _finding(
                "HRC-FIXTURE-ROOT",
                f"fixture_root must equal {FIXTURE_ROOT_PATH!r}",
                path=f"{FIXTURE_ROOT_PATH}/index.yaml",
            )
        )
    fixture_root = family_root / "fixtures"
    findings.extend(
        _normalize_findings(
            validate_index(
                fixture_index,
                fixture_root=fixture_root,
                repository_root=repo_root,
            )
        )
    )
    findings.extend(_fixture_coverage_findings(fixture_index, fixture_root))
    selection, selection_findings, selection_dependency = _selection(
        fixture_index, case_id=case_id, phase=phase
    )
    findings.extend(selection_findings)
    dependency_error = dependency_error or selection_dependency
    findings.extend(
        _cross_document_findings(fixture_index, acceptance_map, evidence_register)
    )
    if findings or dependency_error or phase == "structural":
        return _normalize_findings(findings), dependency_error, selection, summary

    governed_change = fixture_index.get("governed_change")
    inventory_findings: list[dict[str, str]] = []
    inventory = _validate_ratified_inventory(
        repo_root, governed_change, inventory_findings
    )
    findings.extend(inventory_findings)
    if inventory is None:
        if not inventory_findings:
            findings.append(
                _finding(
                    "HRC-OPENSPEC-INVENTORY-MISSING",
                    "ratified OpenSpec delta inventory is unavailable",
                    path=f"openspec/changes/{governed_change}/specs",
                )
            )
            dependency_error = True
        return _normalize_findings(findings), dependency_error, selection, summary
    requirements = [
        item
        for item in (inventory.get("requirements", []) or [])
        if isinstance(item, Mapping)
    ]
    summary["openspec_requirements"] = len(requirements)
    summary["openspec_scenarios"] = sum(
        len(list(item.get("scenario_titles", []) or [])) for item in requirements
    )
    try:
        collected_nodes = collect_pytest_node_ids(repo_root)
    except (FileNotFoundError, RuntimeError) as error:
        findings.append(
            _finding(
                "HRC-PYTEST-COLLECTION",
                str(error),
                path=TEST_ROOT_PATH,
            )
        )
        return _normalize_findings(findings), True, selection, summary
    summary["collected_test_nodes"] = len(collected_nodes)
    parity = check_parity(
        inventory,
        acceptance_map,
        evidence_register,
        collected_node_ids=collected_nodes,
        skipped_node_ids=(),
    )
    for category, items in parity.items():
        code = PARITY_CODES.get(category, "HRC-PARITY-INVALID")
        for item in items:
            findings.append(
                _finding(
                    code,
                    str(item),
                    path="contracts/hermes-runtime/evidence-register.yaml",
                )
            )
    return _normalize_findings(findings), dependency_error, selection, summary


def _parse_repo_mappings(
    pairs: Sequence[str],
) -> tuple[dict[str, Path], list[dict[str, str]]]:
    """Parse repeated ``REPO=CHECKOUT`` resolver options into a mapping."""

    mappings: dict[str, Path] = {}
    findings: list[dict[str, str]] = []
    for pair in pairs or []:
        key, separator, value = str(pair).partition("=")
        if not separator or not key or not value:
            findings.append(
                _finding(
                    "HRC-RESOLVER-MAPPING-INVALID",
                    f"repository mapping must be REPO=CHECKOUT: {pair!r}",
                    path="mode",
                )
            )
            continue
        mappings[key] = Path(value)
    return mappings, findings


def _run_domain_regression(
    repo_root: Path,
    domain_mappings: Mapping[str, Path],
    domain_repo_root: Path | None,
) -> tuple[list[dict[str, str]], bool]:
    """Resolve and validate the realized domain-regression inventory live."""

    inventory_path = repo_root / DOMAIN_REGRESSION_INVENTORY_PATH
    try:
        inventory = load_yaml_document(inventory_path)
    except (OSError, ValueError) as error:
        return (
            [
                _finding(
                    "HGR-REGRESSION-DEPENDENCY",
                    f"domain regression inventory is unavailable: {error}",
                    path=DOMAIN_REGRESSION_INVENTORY_PATH,
                )
            ],
            True,
        )
    try:
        resolver = domain_regression.build_repository_resolver(
            domain_mappings or None, domain_repo_root
        )
        result = domain_regression.validate_domain_regression(
            inventory, resolver=resolver
        )
    except domain_regression.DomainRegressionDependencyError as error:
        return (
            [_finding(error.code, str(error), path="domain-regression")],
            True,
        )
    return _normalize_findings(result), False


def _run_release_mode(
    repo_root: Path,
    *,
    mode: str,
    domain_supplied: bool,
    domain_mappings: Mapping[str, Path],
    domain_repo_root: Path | None,
    base_dependency: bool,
) -> tuple[list[dict[str, str]], bool]:
    """Run candidate/realization release validation plus required domain resolution."""

    if not domain_supplied:
        return (
            [
                _finding(
                    "HRC-DOMAIN-RESOLVER-REQUIRED",
                    f"{mode} mode requires --domain-repo or --domain-repo-root for "
                    "live domain-regression resolution",
                    path="mode",
                )
            ],
            True,
        )
    try:
        catalog_document = load_yaml_document(repo_root / CATALOG_RELATIVE_PATH)
    except (OSError, ValueError) as error:
        return (
            [
                _finding(
                    "HGR-RELEASE-DEPENDENCY",
                    f"contract catalog is unavailable: {error}",
                    path=CATALOG_RELATIVE_PATH,
                )
            ],
            True,
        )
    if not isinstance(catalog_document, Mapping):
        return (
            [
                _finding(
                    "HGR-RELEASE-DEPENDENCY",
                    "contract catalog is not a mapping",
                    path=CATALOG_RELATIVE_PATH,
                )
            ],
            True,
        )
    try:
        if mode == "candidate":
            release_findings = release.validate_candidate(
                repo_root, catalog=catalog_document
            )
        else:
            release_findings = release.validate_realization(
                repo_root, catalog=catalog_document
            )
    except release.ReleaseDependencyError as error:
        return ([_finding(error.code, str(error), path="mode")], True)

    findings = _normalize_findings(release_findings)
    unrealized = any(
        str(item.get("code"))
        in {"HGR-RELEASE-INVENTORY-MISSING", "HGR-RELEASE-INVENTORY-SHAPE"}
        for item in release_findings
    )
    if unrealized or base_dependency:
        return findings, False
    domain_findings, domain_dependency = _run_domain_regression(
        repo_root, domain_mappings, domain_repo_root
    )
    findings.extend(domain_findings)
    return findings, domain_dependency


def _run_consumer_handoff(
    receipt_path: Path,
    *,
    consumer_supplied: bool,
    consumer_mappings: Mapping[str, Path],
    consumer_repo_root: Path | None,
) -> tuple[list[dict[str, str]], bool]:
    """Validate a Gate G0 consumer handoff receipt against the consumer resolver."""

    if not consumer_supplied:
        return (
            [
                _finding(
                    "HRC-CONSUMER-RESOLVER-REQUIRED",
                    "--handoff-receipt requires a resolvable consumer repository "
                    "(--consumer-repo or --consumer-repo-root)",
                    path="mode",
                )
            ],
            True,
        )
    try:
        receipt = load_yaml_document(receipt_path)
    except (OSError, ValueError) as error:
        return (
            [
                _finding(
                    "HGR-HANDOFF-DEPENDENCY",
                    f"handoff receipt is unavailable: {error}",
                    path=str(receipt_path),
                )
            ],
            True,
        )
    if not isinstance(receipt, Mapping):
        return (
            [
                _finding(
                    "HGR-HANDOFF-DEPENDENCY",
                    "handoff receipt is not a mapping",
                    path=str(receipt_path),
                )
            ],
            True,
        )
    try:
        resolver = consumer_handoff.build_consumer_resolver(
            consumer_mappings or None, consumer_repo_root
        )
        result = consumer_handoff.validate_handoff_receipt(
            receipt, consumer_resolver=resolver
        )
    except consumer_handoff.ConsumerHandoffDependencyError as error:
        return ([_finding(error.code, str(error), path="handoff-receipt")], True)
    return _normalize_findings(result), False


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    mode = (
        "realization"
        if arguments.require_realization
        else "candidate" if arguments.require_candidate else "standard"
    )
    findings: list[dict[str, str]] = []
    dependency_error = False
    selection: dict[str, object] = {
        "case_id": arguments.case_id,
        "case_ids": [],
        "phase": arguments.phase,
    }
    summary: dict[str, int] = {
        "catalog_members": 0,
        "schema_members": 0,
        "fixture_cases": 0,
        "openspec_requirements": 0,
        "openspec_scenarios": 0,
        "collected_test_nodes": 0,
    }

    if arguments.require_candidate and arguments.require_realization:
        findings.append(
            _finding(
                "HRC-MODE-MUTUALLY-EXCLUSIVE",
                "candidate and realization modes are mutually exclusive",
                case_id=arguments.case_id or "",
            )
        )
        dependency_error = True
    else:
        requested_root = arguments.repo or _ENTRYPOINT_REPO
        repo_root = _git_root(requested_root)
        if repo_root is None:
            findings.append(
                _finding(
                    "HRC-REPO-NOT-AVAILABLE",
                    "the selected repository is not an available Git root",
                    case_id=arguments.case_id or "",
                )
            )
            dependency_error = True
        else:
            (
                repository_findings,
                repository_dependency,
                selection,
                summary,
            ) = _validate_repository(
                repo_root,
                case_id=arguments.case_id,
                phase=arguments.phase,
            )
            findings.extend(repository_findings)
            dependency_error = dependency_error or repository_dependency

            domain_mappings, domain_parse = _parse_repo_mappings(arguments.domain_repo)
            consumer_mappings, consumer_parse = _parse_repo_mappings(
                arguments.consumer_repo
            )
            findings.extend(domain_parse)
            findings.extend(consumer_parse)
            if domain_parse or consumer_parse:
                dependency_error = True
            domain_supplied = (
                bool(arguments.domain_repo) or arguments.domain_repo_root is not None
            )
            consumer_supplied = (
                bool(arguments.consumer_repo)
                or arguments.consumer_repo_root is not None
            )

            if mode in {"candidate", "realization"}:
                mode_findings, mode_dependency = _run_release_mode(
                    repo_root,
                    mode=mode,
                    domain_supplied=domain_supplied,
                    domain_mappings=domain_mappings,
                    domain_repo_root=arguments.domain_repo_root,
                    base_dependency=dependency_error,
                )
                findings.extend(mode_findings)
                dependency_error = dependency_error or mode_dependency
            elif domain_supplied and not dependency_error:
                domain_findings, domain_dependency = _run_domain_regression(
                    repo_root, domain_mappings, arguments.domain_repo_root
                )
                findings.extend(domain_findings)
                dependency_error = dependency_error or domain_dependency

            if arguments.handoff_receipt is not None:
                handoff_findings, handoff_dependency = _run_consumer_handoff(
                    arguments.handoff_receipt,
                    consumer_supplied=consumer_supplied,
                    consumer_mappings=consumer_mappings,
                    consumer_repo_root=arguments.consumer_repo_root,
                )
                findings.extend(handoff_findings)
                dependency_error = dependency_error or handoff_dependency

    exit_code = classify_exit_code(
        findings, strict=arguments.strict, dependency_error=dependency_error
    )
    _render(
        findings,
        mode=mode,
        as_json=arguments.as_json,
        exit_code=exit_code,
        selection=selection,
        summary=summary,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
