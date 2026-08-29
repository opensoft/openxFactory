from __future__ import annotations

import ast
from collections.abc import Sequence
from pathlib import Path, PurePosixPath

from scripts.hermes_runtime_validation.pytest_bindings import analyze_bindings
from scripts.hermes_runtime_validation.pytest_config import pytest_config_supported
from scripts.hermes_runtime_validation.pytest_parameter_ids import (
    combined_parameter_variants,
    parameter_dimensions,
    parametrized_names,
)
from scripts.hermes_runtime_validation.pytest_paths import valid_test_path
from scripts.hermes_runtime_validation.pytest_source import parse_bounded_module
from scripts.hermes_runtime_validation.pytest_static_values import (
    EvaluationBudget,
    StaticBindings,
    StaticBudgetError,
    StaticProofError,
)
from scripts.hermes_runtime_validation.pytest_support import (
    module_collection_supported,
    test_decorators_supported,
)
from scripts.hermes_runtime_validation.pytest_targets import (
    function_argument_names,
    pytestmarks,
)

MAX_STATIC_TEST_NODES = 100_000


def count_static_pytest_nodes(repo_root: Path, module_paths: Sequence[str]) -> int:
    if not pytest_config_supported(repo_root):
        raise ValueError("unsupported pytest collection configuration")
    total = 0
    budget = EvaluationBudget()
    for module_path in module_paths:
        path = PurePosixPath(module_path)
        if not valid_test_path(path):
            raise ValueError(f"invalid pytest module path: {module_path}")
        module = parse_bounded_module(repo_root, path)
        if module is None or not module_collection_supported(module):
            raise ValueError(f"pytest module is not a bounded Python file: {module_path}")
        try:
            total += _count_tests(module.body, {}, (), False, budget)
        except StaticBudgetError as error:
            raise ValueError("static pytest analysis budget exceeded") from error
        except StaticProofError as error:
            raise ValueError(f"unsupported static pytest module: {module_path}") from error
        _check_total(total)
    if total == 0:
        raise ValueError("static pytest inventory returned zero tests")
    return total


def _count_tests(
    body: list[ast.stmt],
    inherited: StaticBindings,
    inherited_decorators: tuple[ast.expr, ...],
    inherited_pytest: bool,
    budget: EvaluationBudget,
) -> int:
    analysis = analyze_bindings(
        body,
        inherited,
        canonical=inherited_pytest,
        budget=budget,
    )
    marks = pytestmarks(body)
    if marks is None:
        raise ValueError("pytestmark final binding requires exact static proof")
    if marks and not analysis.canonical_final:
        raise ValueError("canonical pytest binding is required for pytestmark")
    total = 0
    for statement in body:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (
                statement.name.startswith("test_")
                and analysis.definitions.get(statement.name) is statement
            ):
                decorators = (*inherited_decorators, *marks, *statement.decorator_list)
                _validate_target(
                    statement,
                    decorators,
                    analysis.canonical_before[id(statement)],
                )
                total += _parameter_multiplier(
                    list(decorators),
                    analysis.before[id(statement)],
                    budget,
                )
        elif (
            isinstance(statement, ast.ClassDef)
            and statement.name.startswith("Test")
            and analysis.definitions.get(statement.name) is statement
        ):
            decorators = (*inherited_decorators, *marks, *statement.decorator_list)
            canonical = analysis.canonical_before[id(statement)]
            _validate_decorators(decorators, canonical)
            total += _count_tests(
                statement.body,
                analysis.before[id(statement)],
                tuple(decorators),
                canonical,
                budget,
            )
        _check_total(total)
    return total


def _validate_target(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
    decorators: tuple[ast.expr, ...],
    canonical: bool,
) -> None:
    _validate_decorators(decorators, canonical)
    names = parametrized_names(list(decorators))
    if names is None or not names.issubset(function_argument_names(function)):
        raise ValueError("pytest parameter names must match the signature")


def _validate_decorators(decorators: tuple[ast.expr, ...], canonical: bool) -> None:
    if not test_decorators_supported(decorators):
        raise ValueError("unsupported pytest decorator")
    if decorators and not canonical:
        raise ValueError("canonical pytest binding is required")


def _parameter_multiplier(
    decorators: list[ast.expr],
    values: StaticBindings,
    budget: EvaluationBudget,
) -> int:
    dimensions = parameter_dimensions(decorators, values, budget)
    if dimensions is None:
        raise ValueError("pytest parametrization requires exact static proof")
    variants = combined_parameter_variants(dimensions, budget)
    if variants is None:
        raise ValueError("pytest parametrization exceeds the variant limit")
    return len(variants) if variants else 1


def _check_total(total: int) -> None:
    if total > MAX_STATIC_TEST_NODES:
        raise ValueError("static pytest inventory exceeds the test-count limit")
