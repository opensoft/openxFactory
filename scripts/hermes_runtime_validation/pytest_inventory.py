from __future__ import annotations

import ast
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from scripts.hermes_runtime_validation.pytest_bindings import (
    BindingAnalysis,
    analyze_bindings,
)
from scripts.hermes_runtime_validation.pytest_config import pytest_config_supported
from scripts.hermes_runtime_validation.pytest_fixtures import (
    FixtureSource,
    fixture_dimensions,
)
from scripts.hermes_runtime_validation.pytest_parameter_ids import (
    ParameterVariant,
    combined_parameter_variants,
    is_statically_skipped,
    parameter_dimensions,
    parametrized_names,
)
from scripts.hermes_runtime_validation.pytest_paths import valid_test_path
from scripts.hermes_runtime_validation.pytest_source import (
    parse_bounded_module,
    parse_optional_bounded_module,
)
from scripts.hermes_runtime_validation.pytest_static_values import (
    EvaluationBudget,
    StaticBudgetError,
    StaticProofError,
)
from scripts.hermes_runtime_validation.pytest_support import (
    has_runtime_suppression,
    module_collection_supported,
    pytest_marker,
    test_decorators_supported,
)
from scripts.hermes_runtime_validation.pytest_targets import (
    find_test_target,
    function_argument_names,
)


@dataclass(frozen=True, slots=True)
class EvidenceTestNodes:
    collected: tuple[str, ...]
    skipped: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ModuleContext:
    module: ast.Module
    analysis: BindingAnalysis
    fixture_sources: tuple[FixtureSource, ...]


@dataclass(frozen=True, slots=True)
class TargetProof:
    decorated_skip: bool
    variants: tuple[ParameterVariant, ...]


def collect_static_pytest_nodes(
    repo_root: Path, module_paths: Sequence[str]
) -> tuple[str, ...]:
    if not pytest_config_supported(repo_root):
        raise ValueError("unsupported pytest collection configuration")
    budget = EvaluationBudget()
    nodes: list[str] = []
    try:
        for module_path in module_paths:
            path = PurePosixPath(module_path)
            if not valid_test_path(path):
                raise ValueError(f"invalid pytest module path: {module_path}")
            context = _module_context(repo_root, path, budget)
            if context is None:
                raise ValueError(f"unsupported static pytest module: {module_path}")
            for selectors in _target_selectors(
                context.module.body,
                context.analysis,
                budget,
            ):
                proof = _target_proof(context, selectors, budget)
                target = find_test_target(context.module, selectors)
                if proof is None or target is None:
                    raise ValueError(f"unproved pytest target: {module_path}::{selectors[-1]}")
                if not any(
                    marker is not None and marker[0] == "postgres"
                    for marker in (pytest_marker(item) for item in target.decorators)
                ):
                    raise ValueError(f"PostgreSQL target lacks marker: {module_path}::{selectors[-1]}")
                base = f"{module_path}::{'::'.join(selectors)}"
                if proof.decorated_skip or any(item.skipped for item in proof.variants):
                    raise ValueError(f"PostgreSQL target is statically skipped: {base}")
                if proof.variants:
                    nodes.extend(f"{base}[{item.identifier}]" for item in proof.variants)
                else:
                    nodes.append(base)
    except StaticBudgetError as error:
        raise ValueError("static pytest analysis budget exceeded") from error
    ordered = tuple(sorted(nodes))
    if not ordered or len(ordered) != len(set(ordered)):
        raise ValueError("static pytest node inventory is empty or duplicated")
    return ordered


def collect_evidence_test_nodes(
    repo_root: Path, evidence_register: Mapping[str, object]
) -> EvidenceTestNodes:
    if not pytest_config_supported(repo_root):
        return EvidenceTestNodes((), ())
    budget = EvaluationBudget()
    contexts: dict[PurePosixPath, ModuleContext | None] = {}
    proofs: dict[tuple[PurePosixPath, tuple[str, ...]], TargetProof | None] = {}
    collected: list[str] = []
    skipped: list[str] = []
    try:
        for node_id in _requested_nodes(evidence_register):
            budget.consume()
            path, selectors, parameter_id = _node_parts(node_id)
            if path is None or not selectors:
                continue
            if path not in contexts:
                contexts[path] = _module_context(repo_root, path, budget)
            context = contexts[path]
            if context is None:
                continue
            key = (path, selectors)
            if key not in proofs:
                proofs[key] = _target_proof(context, selectors, budget)
            proof = _parameter_skip(proofs[key], parameter_id)
            if proof is None:
                continue
            collected.append(node_id)
            if proof:
                skipped.append(node_id)
    except StaticBudgetError:
        return EvidenceTestNodes((), ())
    return EvidenceTestNodes(tuple(collected), tuple(skipped))


def _requested_nodes(evidence_register: Mapping[str, object]) -> tuple[str, ...]:
    nodes: set[str] = set()
    entries = evidence_register.get("entries")
    if not isinstance(entries, list):
        return ()
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        values = entry.get("test_node_ids", []) or []
        if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
            nodes.update(str(value) for value in values if isinstance(value, str))
    return tuple(sorted(nodes))


def _node_parts(
    node_id: str,
) -> tuple[PurePosixPath | None, tuple[str, ...], str | None]:
    path_text, *selectors = node_id.split("::")
    path = PurePosixPath(path_text)
    if not valid_test_path(path):
        return None, (), None
    parameter_id: str | None = None
    if selectors and "[" in selectors[-1] and selectors[-1].endswith("]"):
        selectors[-1], parameter_id = selectors[-1][:-1].split("[", maxsplit=1)
    return path, tuple(selectors), parameter_id


def _module_context(
    repo_root: Path, path: PurePosixPath, budget: EvaluationBudget
) -> ModuleContext | None:
    module = parse_bounded_module(repo_root, path)
    if module is None or not module_collection_supported(module):
        return None
    try:
        analysis = analyze_bindings(module.body, budget=budget)
    except StaticBudgetError:
        raise
    except StaticProofError:
        return None
    fixtures: list[FixtureSource] = []
    directory = PurePosixPath()
    if not _append_conftest(repo_root, directory, fixtures, budget):
        return None
    for component in path.parent.parts:
        directory /= component
        if not _append_conftest(repo_root, directory, fixtures, budget):
            return None
    fixtures.append(FixtureSource(module))
    return ModuleContext(
        module=module,
        analysis=analysis,
        fixture_sources=tuple(fixtures),
    )


def _target_proof(
    context: ModuleContext,
    selectors: tuple[str, ...],
    budget: EvaluationBudget,
) -> TargetProof | None:
    target = find_test_target(context.module, selectors)
    if target is None:
        return None
    if has_runtime_suppression(target.function):
        return None
    decorators = list(target.decorators)
    if decorators and (
        not context.analysis.canonical_before[id(target.binding_anchor)]
        or not context.analysis.canonical_final
        or not test_decorators_supported(target.decorators)
    ):
        return None
    bindings = context.analysis.before[id(target.binding_anchor)]
    direct = parameter_dimensions(decorators, bindings, budget)
    direct_names = parametrized_names(decorators)
    if direct is None or direct_names is None:
        return None
    if not direct_names.issubset(function_argument_names(target.function)):
        return None
    fixtures = fixture_dimensions(
        context.fixture_sources,
        target.function,
        direct_names,
        target.required_fixtures,
        budget=budget,
    )
    if fixtures is None:
        return None
    variants = combined_parameter_variants((*fixtures, *direct), budget)
    if variants is None:
        return None
    decorated_skip = is_statically_skipped(decorators, bindings, budget)
    if decorated_skip is None:
        return None
    return TargetProof(decorated_skip=decorated_skip, variants=variants)


def _parameter_skip(proof: TargetProof | None, parameter_id: str | None) -> bool | None:
    if proof is None:
        return None
    if parameter_id is None:
        return proof.decorated_skip if not proof.variants else None
    variant = next(
        (item for item in proof.variants if item.identifier == parameter_id),
        None,
    )
    if variant is None:
        return None
    return proof.decorated_skip or variant.skipped


def _target_selectors(
    body: list[ast.stmt],
    analysis: BindingAnalysis,
    budget: EvaluationBudget,
    prefix: tuple[str, ...] = (),
) -> tuple[tuple[str, ...], ...]:
    selectors: list[tuple[str, ...]] = []
    for statement in body:
        budget.consume()
        if not isinstance(
            statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            continue
        if analysis.definitions.get(statement.name) is not statement:
            continue
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if statement.name.startswith("test_"):
                selectors.append((*prefix, statement.name))
            continue
        if isinstance(statement, ast.ClassDef) and statement.name.startswith("Test"):
            nested = analyze_bindings(
                statement.body,
                analysis.before[id(statement)],
                canonical=analysis.canonical_before[id(statement)],
                budget=budget,
            )
            selectors.extend(
                _target_selectors(
                    statement.body,
                    nested,
                    budget,
                    (*prefix, statement.name),
                )
            )
    return tuple(selectors)


def _append_conftest(
    repo_root: Path,
    directory: PurePosixPath,
    fixtures: list[FixtureSource],
    budget: EvaluationBudget,
) -> bool:
    present, conftest = parse_optional_bounded_module(
        repo_root, directory / "conftest.py"
    )
    if not present:
        return True
    if conftest is None or not module_collection_supported(conftest):
        return False
    try:
        _ = analyze_bindings(conftest.body, budget=budget)
    except StaticBudgetError:
        raise
    except StaticProofError:
        return False
    imported = _imported_fixture_sources(repo_root, directory, conftest)
    if imported is None:
        return False
    fixtures.extend(imported)
    fixtures.append(FixtureSource(conftest))
    return True


def _imported_fixture_sources(
    repo_root: Path, directory: PurePosixPath, module: ast.Module
) -> tuple[FixtureSource, ...] | None:
    sources: list[FixtureSource] = []
    for statement in module.body:
        if not isinstance(statement, ast.ImportFrom) or statement.module is None:
            continue
        if any(alias.name == "*" for alias in statement.names):
            return None
        relative = PurePosixPath(*statement.module.split(".")).with_suffix(".py")
        candidates = (directory / relative, relative)
        resolved: ast.Module | None = None
        present = False
        for candidate in candidates:
            candidate_present, candidate_module = parse_optional_bounded_module(
                repo_root, candidate
            )
            if candidate_present:
                present = True
                resolved = candidate_module
                break
        if not present:
            continue
        if resolved is None or not module_collection_supported(resolved):
            return None
        names = tuple((alias.name, alias.asname or alias.name) for alias in statement.names)
        sources.append(FixtureSource(resolved, names))
    return tuple(sources)
