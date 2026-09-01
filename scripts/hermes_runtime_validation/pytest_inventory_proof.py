from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from scripts.hermes_runtime_validation.pytest_bindings import (
    BindingAnalysis,
    analyze_bindings,
)
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
    test_decorators_supported,
)
from scripts.hermes_runtime_validation.pytest_targets import (
    find_test_target,
    function_argument_names,
)


@dataclass(frozen=True, slots=True)
class ModuleContext:
    module: ast.Module
    analysis: BindingAnalysis
    fixture_sources: tuple[FixtureSource, ...]


@dataclass(frozen=True, slots=True)
class TargetProof:
    decorated_skip: bool
    variants: tuple[ParameterVariant, ...]


def module_context(
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


def target_proof(
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


def parameter_skip(proof: TargetProof | None, parameter_id: str | None) -> bool | None:
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


def target_selectors(
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
                target_selectors(
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
        names = tuple(
            (alias.name, alias.asname or alias.name) for alias in statement.names
        )
        sources.append(FixtureSource(resolved, names))
    return tuple(sources)
