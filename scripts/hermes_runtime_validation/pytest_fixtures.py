from __future__ import annotations

import ast
from dataclasses import dataclass

from scripts.hermes_runtime_validation.pytest_bindings import analyze_bindings
from scripts.hermes_runtime_validation.pytest_parameter_ids import (
    ParameterDimension,
    fixture_parameter_dimension,
)
from scripts.hermes_runtime_validation.pytest_static_values import EvaluationBudget
from scripts.hermes_runtime_validation.pytest_support import (
    has_runtime_suppression,
    looks_like_fixture_decorator,
    pytest_fixture_call,
)

PYTEST_BUILTIN_FIXTURES = frozenset(
    {
        "cache",
        "capfd",
        "capfdbinary",
        "caplog",
        "capsys",
        "capsysbinary",
        "doctest_namespace",
        "monkeypatch",
        "pytestconfig",
        "record_property",
        "record_testsuite_property",
        "record_xml_attribute",
        "recwarn",
        "request",
        "tmp_path",
        "tmp_path_factory",
        "tmpdir",
        "tmpdir_factory",
    }
)


@dataclass(frozen=True, slots=True)
class FixtureProvider:
    dependencies: tuple[str, ...]
    dimension: ParameterDimension | None
    proof_complete: bool
    autouse: bool


@dataclass(frozen=True, slots=True)
class FixtureSource:
    module: ast.Module
    imported_names: tuple[tuple[str, str], ...] = ()


def fixture_dimensions(
    sources: tuple[FixtureSource, ...],
    function: ast.FunctionDef | ast.AsyncFunctionDef,
    direct_names: frozenset[str],
    required_names: tuple[str, ...] = (),
    *,
    budget: EvaluationBudget,
) -> tuple[ParameterDimension, ...] | None:
    providers: dict[str, FixtureProvider] = {}
    for source in sources:
        module_providers = _module_fixtures(source, budget)
        if module_providers is None:
            return None
        providers.update(module_providers)
    dimensions: list[ParameterDimension] = []
    resolved: set[str] = set()
    resolving: set[str] = set()

    def resolve(name: str) -> bool:
        budget.consume()
        if name in direct_names or name == "self":
            return True
        if name in resolved:
            return True
        if name in resolving:
            return False
        provider = providers.get(name)
        if provider is None:
            return name in PYTEST_BUILTIN_FIXTURES
        if not provider.proof_complete:
            return False
        resolving.add(name)
        if not all(resolve(dependency) for dependency in provider.dependencies):
            return False
        resolving.remove(name)
        resolved.add(name)
        if provider.dimension is not None:
            dimensions.append(provider.dimension)
        return True

    roots = (*_function_arguments(function), *required_names)
    roots += tuple(name for name, provider in providers.items() if provider.autouse)
    if not all(resolve(name) for name in roots):
        return None
    return tuple(dimensions)


def _module_fixtures(
    source: FixtureSource, budget: EvaluationBudget
) -> dict[str, FixtureProvider] | None:
    module = source.module
    providers: dict[str, FixtureProvider] = {}
    analysis = analyze_bindings(module.body, budget=budget)
    imported = dict(source.imported_names)
    for statement in module.body:
        if not isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        fixture_like = tuple(
            item
            for item in statement.decorator_list
            if looks_like_fixture_decorator(item)
        )
        if not fixture_like:
            continue
        if imported and statement.name not in imported:
            continue
        if len(fixture_like) != 1 or len(statement.decorator_list) != 1:
            return None
        decorator = fixture_like[0]
        call = pytest_fixture_call(decorator)
        if call is None or not analysis.canonical_before[id(statement)]:
            return None
        if call.args or any(
            keyword.arg not in {"autouse", "ids", "name", "params", "scope"}
            for keyword in call.keywords
        ):
            return None
        if len({keyword.arg for keyword in call.keywords}) != len(call.keywords):
            return None
        bindings = analysis.before[id(statement)]
        params = next(
            (keyword.value for keyword in call.keywords if keyword.arg == "params"),
            None,
        )
        ids = next(
            (keyword.value for keyword in call.keywords if keyword.arg == "ids"),
            None,
        )
        dimension = (
            None
            if params is None
            else fixture_parameter_dimension(params, ids, bindings, budget)
        )
        if params is not None and dimension is None:
            return None
        alias = imported.get(statement.name, statement.name)
        autouse = False
        for keyword in call.keywords:
            if keyword.arg == "name":
                if not (
                    isinstance(keyword.value, ast.Constant)
                    and isinstance(keyword.value.value, str)
                    and keyword.value.value
                ):
                    return None
                alias = keyword.value.value
            elif keyword.arg == "autouse":
                if not (
                    isinstance(keyword.value, ast.Constant)
                    and isinstance(keyword.value.value, bool)
                ):
                    return None
                autouse = keyword.value.value
            elif keyword.arg == "scope":
                if not (
                    isinstance(keyword.value, ast.Constant)
                    and keyword.value.value
                    in {"class", "function", "module", "package", "session"}
                ):
                    return None
        providers[alias] = FixtureProvider(
            dependencies=_function_arguments(statement),
            dimension=dimension,
            proof_complete=not has_runtime_suppression(statement),
            autouse=autouse,
        )
    return providers


def _function_arguments(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
) -> tuple[str, ...]:
    arguments = (*function.args.posonlyargs, *function.args.args, *function.args.kwonlyargs)
    return tuple(argument.arg for argument in arguments)
