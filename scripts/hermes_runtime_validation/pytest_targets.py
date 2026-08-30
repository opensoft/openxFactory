from __future__ import annotations

import ast
from dataclasses import dataclass

from scripts.hermes_runtime_validation.pytest_bindings import (
    final_assignment,
    final_named_statement,
)


@dataclass(frozen=True, slots=True)
class TestTarget:
    function: ast.FunctionDef | ast.AsyncFunctionDef
    decorators: tuple[ast.expr, ...]
    required_fixtures: tuple[str, ...]
    binding_anchor: ast.stmt


def find_test_target(module: ast.Module, selectors: tuple[str, ...]) -> TestTarget | None:
    body: list[ast.stmt] = module.body
    marks = pytestmarks(body)
    if marks is None:
        return None
    decorators: list[ast.expr] = list(marks)
    required_fixtures: list[str] = list(_usefixtures(list(marks)))
    function: ast.FunctionDef | ast.AsyncFunctionDef | None = None
    binding_anchor: ast.stmt | None = None
    for index, selector in enumerate(selectors):
        candidate = _candidate(body, selector, index == len(selectors) - 1)
        if candidate is None:
            return None
        if binding_anchor is None:
            binding_anchor = candidate
        decorators.extend(candidate.decorator_list)
        required_fixtures.extend(_usefixtures(candidate.decorator_list))
        if isinstance(candidate, ast.ClassDef):
            body = candidate.body
            marks = pytestmarks(body)
            if marks is None:
                return None
            decorators.extend(marks)
            required_fixtures.extend(_usefixtures(list(marks)))
        else:
            function = candidate
    if function is None or binding_anchor is None:
        return None
    return TestTarget(
        function=function,
        decorators=tuple(decorators),
        required_fixtures=tuple(required_fixtures),
        binding_anchor=binding_anchor,
    )


def pytestmarks(body: list[ast.stmt]) -> tuple[ast.expr, ...] | None:
    value = final_assignment(body, "pytestmark")
    if value is None:
        return None
    if isinstance(value, (ast.List, ast.Tuple)):
        return tuple(value.elts)
    return (value,)


def function_argument_names(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
) -> frozenset[str]:
    return frozenset(
        argument.arg
        for argument in (
            *function.args.posonlyargs,
            *function.args.args,
            *function.args.kwonlyargs,
        )
    )


def _candidate(
    body: list[ast.stmt], selector: str, final: bool
) -> ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | None:
    statement = final_named_statement(body, selector)
    if (
        final
        and isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef))
        and statement.name.startswith("test_")
    ):
        return statement
    if not final and isinstance(statement, ast.ClassDef) and statement.name.startswith("Test"):
        return statement
    return None


def _usefixtures(decorators: list[ast.expr]) -> tuple[str, ...]:
    names: list[str] = []
    for decorator in decorators:
        if not (
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "usefixtures"
        ):
            continue
        for argument in decorator.args:
            if not isinstance(argument, ast.Constant) or not isinstance(
                argument.value, str
            ):
                return ("<unproved-usefixtures>",)
            names.append(argument.value)
    return tuple(names)
