from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import TypeAlias

StaticScalar: TypeAlias = str | int | float | bool | None


class StaticProofError(Exception):
    pass


class StaticBudgetError(StaticProofError):
    pass


@dataclass(slots=True)
class EvaluationBudget:
    remaining: int = 100_000

    def consume(self) -> None:
        self.remaining -= 1
        if self.remaining < 0:
            raise StaticBudgetError("static evaluation budget exceeded")


@dataclass(frozen=True, slots=True)
class StaticParameter:
    values: tuple[StaticValue, ...]
    identifier: str
    skipped: bool


StaticValue: TypeAlias = (
    StaticScalar
    | tuple["StaticValue", ...]
    | dict[str, "StaticValue"]
    | StaticParameter
)
StaticBindings: TypeAlias = dict[str, StaticValue]


def evaluate_static(
    expression: ast.expr,
    bindings: StaticBindings,
    local: StaticBindings | None = None,
    *,
    budget: EvaluationBudget | None = None,
) -> StaticValue:
    if budget is None:
        budget = EvaluationBudget()
    budget.consume()
    names = bindings if local is None else bindings | local
    match expression:
        case ast.Constant(value=value) if value is None or isinstance(
            value, (str, int, float, bool)
        ):
            return value
        case ast.Name(id=name):
            if name not in names:
                raise StaticProofError(f"unknown static name: {name}")
            return names[name]
        case ast.List(elts=elements) | ast.Tuple(elts=elements):
            return tuple(
                evaluate_static(element, bindings, local, budget=budget)
                for element in elements
            )
        case ast.Dict(keys=keys, values=values):
            result: dict[str, StaticValue] = {}
            for key_node, value_node in zip(keys, values, strict=True):
                if key_node is None:
                    raise StaticProofError("dictionary unpacking is not static")
                key = evaluate_static(key_node, bindings, local, budget=budget)
                if not isinstance(key, str):
                    raise StaticProofError("static dictionary keys must be strings")
                result[key] = evaluate_static(value_node, bindings, local, budget=budget)
            return result
        case ast.Call() as call if _call_name(call.func) == "sorted":
            if len(call.args) != 1 or call.keywords:
                raise StaticProofError("sorted() must have exactly one argument")
            values = static_collection(
                evaluate_static(call.args[0], bindings, local, budget=budget)
            )
            if all(isinstance(value, str) for value in values):
                return tuple(sorted(value for value in values if isinstance(value, str)))
            if all(isinstance(value, int) for value in values):
                return tuple(sorted(value for value in values if isinstance(value, int)))
            if all(isinstance(value, float) for value in values):
                return tuple(sorted(value for value in values if isinstance(value, float)))
            raise StaticProofError("sorted() values must be uniform comparable scalars")
        case ast.Call() as call if _call_name(call.func) == "pytest.param":
            return _evaluate_pytest_param(call, bindings, local, budget)
        case ast.ListComp() | ast.GeneratorExp() as comprehension:
            return _evaluate_comprehension(comprehension, bindings, local, budget)
        case ast.Subscript(value=container_node, slice=index_node):
            container = evaluate_static(container_node, bindings, local, budget=budget)
            index = evaluate_static(index_node, bindings, local, budget=budget)
            if isinstance(container, tuple) and isinstance(index, int):
                try:
                    return container[index]
                except IndexError as error:
                    raise StaticProofError("static tuple index is out of range") from error
            if isinstance(container, dict) and isinstance(index, str):
                try:
                    return container[index]
                except KeyError as error:
                    raise StaticProofError("static dictionary key is absent") from error
            raise StaticProofError("unsupported static subscript")
        case _:
            raise StaticProofError(f"unsupported static expression: {ast.unparse(expression)}")


def static_collection(value: StaticValue) -> tuple[StaticValue, ...]:
    if isinstance(value, tuple):
        return value
    if isinstance(value, dict):
        return tuple(value)
    raise StaticProofError("expression is not a static collection")


def _evaluate_comprehension(
    expression: ast.ListComp | ast.GeneratorExp,
    bindings: StaticBindings,
    local: StaticBindings | None,
    budget: EvaluationBudget,
) -> tuple[StaticValue, ...]:
    if len(expression.generators) != 1 or expression.generators[0].ifs:
        raise StaticProofError("only one unfiltered comprehension generator is static")
    generator = expression.generators[0]
    values = static_collection(
        evaluate_static(generator.iter, bindings, local, budget=budget)
    )
    result: list[StaticValue] = []
    for value in values:
        iteration = {} if local is None else dict(local)
        _bind_target(generator.target, value, iteration)
        result.append(evaluate_static(expression.elt, bindings, iteration, budget=budget))
    return tuple(result)


def _bind_target(target: ast.expr, value: StaticValue, bindings: StaticBindings) -> None:
    match target:
        case ast.Name(id=name):
            bindings[name] = value
        case ast.Tuple(elts=targets):
            values = static_collection(value)
            if len(targets) != len(values):
                raise StaticProofError("comprehension tuple unpacking has unequal arity")
            for nested, item in zip(targets, values, strict=True):
                _bind_target(nested, item, bindings)
        case _:
            raise StaticProofError("unsupported comprehension target")


def _evaluate_pytest_param(
    call: ast.Call,
    bindings: StaticBindings,
    local: StaticBindings | None,
    budget: EvaluationBudget,
) -> StaticParameter:
    identifier: str | None = None
    skipped = False
    for keyword in call.keywords:
        match keyword.arg:
            case "id":
                value = evaluate_static(keyword.value, bindings, local, budget=budget)
                if not isinstance(value, str):
                    raise StaticProofError("pytest.param id must be a literal string")
                identifier = value
            case "marks":
                skipped = _marks_skip(keyword.value, bindings, local, budget)
            case _:
                raise StaticProofError("unsupported pytest.param keyword")
    if identifier is None:
        raise StaticProofError("pytest.param requires an explicit static id")
    values = tuple(
        evaluate_static(value, bindings, local, budget=budget) for value in call.args
    )
    return StaticParameter(values=values, identifier=identifier, skipped=skipped)


def _marks_skip(
    expression: ast.expr,
    bindings: StaticBindings,
    local: StaticBindings | None,
    budget: EvaluationBudget,
) -> bool:
    if isinstance(expression, (ast.List, ast.Tuple)):
        return any(_marks_skip(item, bindings, local, budget) for item in expression.elts)
    name = _call_name(expression.func) if isinstance(expression, ast.Call) else _call_name(expression)
    if name.endswith(".xfail"):
        raise StaticProofError("xfail parameters cannot prove mandatory evidence")
    if name.endswith(".skip"):
        return True
    if name.endswith(".skipif"):
        if not isinstance(expression, ast.Call) or not expression.args:
            raise StaticProofError("pytest skipif requires a static condition")
        condition = evaluate_static(expression.args[0], bindings, local, budget=budget)
        if not isinstance(condition, bool):
            raise StaticProofError("pytest skipif condition must be boolean")
        return condition
    return False


def _call_name(expression: ast.expr) -> str:
    match expression:
        case ast.Name(id=name):
            return name
        case ast.Attribute(value=value, attr=attribute):
            prefix = _call_name(value)
            return f"{prefix}.{attribute}" if prefix else attribute
        case _:
            return ""
