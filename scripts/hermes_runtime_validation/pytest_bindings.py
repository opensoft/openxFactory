from __future__ import annotations

import ast
from dataclasses import dataclass

from scripts.hermes_runtime_validation.pytest_static_values import (
    EvaluationBudget,
    StaticBindings,
    StaticBudgetError,
    StaticProofError,
    evaluate_static,
)


@dataclass(frozen=True, slots=True)
class BindingAnalysis:
    before: dict[int, StaticBindings]
    final: StaticBindings
    canonical_before: dict[int, bool]
    canonical_final: bool
    definitions: dict[str, ast.stmt]


def analyze_bindings(
    body: list[ast.stmt],
    inherited: StaticBindings | None = None,
    *,
    canonical: bool = False,
    budget: EvaluationBudget | None = None,
) -> BindingAnalysis:
    active_budget = budget if budget is not None else EvaluationBudget()
    bindings = {} if inherited is None else dict(inherited)
    before: dict[int, StaticBindings] = {}
    canonical_before: dict[int, bool] = {}
    definitions: dict[str, ast.stmt] = {}
    for statement in body:
        before[id(statement)] = dict(bindings)
        canonical_before[id(statement)] = canonical
        names = statement_binding_names(statement)
        update_bindings(statement, bindings, active_budget)
        canonical = _updated_pytest_binding(statement, names, canonical)
        for name in names:
            if (
                isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and statement.name == name
            ):
                definitions[name] = statement
            else:
                _ = definitions.pop(name, None)
    return BindingAnalysis(
        before=before,
        final=dict(bindings),
        canonical_before=canonical_before,
        canonical_final=canonical,
        definitions=definitions,
    )


def module_bindings(
    module: ast.Module,
    *,
    stop_at: ast.stmt | None = None,
    budget: EvaluationBudget | None = None,
) -> StaticBindings:
    analysis = analyze_bindings(module.body, budget=budget)
    if stop_at is None:
        return analysis.final
    try:
        return analysis.before[id(stop_at)]
    except KeyError as error:
        raise StaticProofError("binding anchor is outside the analyzed scope") from error


def update_bindings(
    statement: ast.stmt,
    bindings: StaticBindings,
    budget: EvaluationBudget,
) -> None:
    budget.consume()
    names = statement_binding_names(statement)
    expression: ast.expr | None = None
    match statement:
        case ast.Assign(targets=targets, value=value) if all(
            isinstance(target, ast.Name) for target in targets
        ):
            expression = value
        case ast.AnnAssign(target=ast.Name(), value=value) if value is not None:
            expression = value
        case ast.Delete(targets=targets):
            for name in names:
                _ = bindings.pop(name, None)
            return
        case _:
            for name in names:
                _ = bindings.pop(name, None)
            return
    try:
        value = evaluate_static(expression, bindings, budget=budget)
    except StaticBudgetError:
        raise
    except StaticProofError:
        for name in names:
            _ = bindings.pop(name, None)
        return
    for name in names:
        bindings[name] = value


def statement_binding_names(statement: ast.stmt) -> set[str]:
    match statement:
        case ast.Assign(targets=targets):
            return _targets_names(targets)
        case ast.AnnAssign(target=target) | ast.AugAssign(target=target):
            return _target_names(target)
        case ast.Import(names=aliases) | ast.ImportFrom(names=aliases):
            return {alias.asname or alias.name.partition(".")[0] for alias in aliases}
        case ast.FunctionDef(name=name) | ast.AsyncFunctionDef(name=name) | ast.ClassDef(
            name=name
        ):
            return {name}
        case ast.For(target=target, body=body, orelse=orelse) | ast.AsyncFor(
            target=target, body=body, orelse=orelse
        ):
            return _target_names(target) | _body_names((*body, *orelse))
        case ast.While(body=body, orelse=orelse) | ast.If(body=body, orelse=orelse):
            return _body_names((*body, *orelse))
        case ast.With(items=items, body=body) | ast.AsyncWith(items=items, body=body):
            item_names: set[str] = set()
            for item in items:
                if item.optional_vars is not None:
                    item_names.update(_target_names(item.optional_vars))
            return item_names | _body_names(tuple(body))
        case ast.Try(body=body, handlers=handlers, orelse=orelse, finalbody=finalbody):
            handler_names: set[str] = {
                handler.name for handler in handlers if handler.name is not None
            }
            handler_bodies = tuple(
                nested for handler in handlers for nested in handler.body
            )
            return handler_names | _body_names(
                (*body, *handler_bodies, *orelse, *finalbody)
            )
        case ast.Match(cases=cases):
            return _body_names(
                tuple(nested for case in cases for nested in case.body)
            ) | _patterns_names(tuple(case.pattern for case in cases))
        case ast.Expr(value=ast.Call() as call):
            return _mutation_names(call)
        case _:
            return set()


def final_named_statement(body: list[ast.stmt], name: str) -> ast.stmt | None:
    bound: ast.stmt | None = None
    for statement in body:
        if name not in statement_binding_names(statement):
            continue
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound = statement if statement.name == name else None
        else:
            bound = None
    return bound


def final_assignment(body: list[ast.stmt], name: str) -> ast.expr | None:
    value: ast.expr | None = None
    seen = False
    for statement in body:
        if name not in statement_binding_names(statement):
            continue
        seen = True
        match statement:
            case ast.Assign(targets=targets, value=expression) if all(
                isinstance(target, ast.Name) for target in targets
            ):
                value = expression
            case ast.AnnAssign(target=ast.Name(), value=expression) if expression is not None:
                value = expression
            case _:
                value = None
    return value if seen else ast.Tuple(elts=[], ctx=ast.Load())


def _body_names(body: tuple[ast.stmt, ...]) -> set[str]:
    names: set[str] = set()
    for statement in body:
        names.update(statement_binding_names(statement))
    return names


def _targets_names(targets: list[ast.expr]) -> set[str]:
    names: set[str] = set()
    for target in targets:
        names.update(_target_names(target))
    return names


def _target_names(target: ast.expr) -> set[str]:
    match target:
        case ast.Name(id=name):
            return {name}
        case ast.List(elts=items) | ast.Tuple(elts=items):
            return _targets_names(items)
        case ast.Attribute(value=value) | ast.Subscript(value=value):
            return _target_names(value)
        case _:
            return set()


def _pattern_names(pattern: ast.pattern) -> set[str]:
    return {
        node.name
        for node in ast.walk(pattern)
        if isinstance(node, ast.MatchAs) and node.name is not None
    }


def _patterns_names(patterns: tuple[ast.pattern, ...]) -> set[str]:
    names: set[str] = set()
    for pattern in patterns:
        names.update(_pattern_names(pattern))
    return names


def _mutation_names(call: ast.Call) -> set[str]:
    expressions = (*call.args, *(keyword.value for keyword in call.keywords))
    if isinstance(call.func, ast.Attribute):
        expressions = (call.func.value, *expressions)
    return {
        node.id
        for expression in expressions
        for node in ast.walk(expression)
        if isinstance(node, ast.Name)
    }


def _updated_pytest_binding(
    statement: ast.stmt, names: set[str], canonical: bool
) -> bool:
    if "pytest" not in names:
        return canonical
    if isinstance(statement, ast.Import):
        return any(
            alias.name == "pytest" and alias.asname in (None, "pytest")
            for alias in statement.names
            if (alias.asname or alias.name.partition(".")[0]) == "pytest"
        )
    return isinstance(statement, ast.Try) and _optional_pytest_import(statement)


def _optional_pytest_import(statement: ast.Try) -> bool:
    imports_pytest = any(
        isinstance(item, ast.Import)
        and any(alias.name == "pytest" and alias.asname is None for alias in item.names)
        for item in statement.body
    )
    assigns_none = any(
        isinstance(item, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "pytest" for target in item.targets)
        and isinstance(item.value, ast.Constant)
        and item.value.value is None
        for handler in statement.handlers
        for item in handler.body
    )
    catches_missing = any(
        isinstance(handler.type, ast.Name)
        and handler.type.id == "ModuleNotFoundError"
        for handler in statement.handlers
    )
    return imports_pytest and catches_missing and assigns_none
