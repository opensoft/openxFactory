from __future__ import annotations

import ast
from dataclasses import dataclass
from itertools import product
from typing import TypeAlias

from scripts.hermes_runtime_validation.pytest_static_values import (
    EvaluationBudget,
    StaticBindings,
    StaticBudgetError,
    StaticParameter,
    StaticProofError,
    StaticValue,
    evaluate_static,
    static_collection,
)


@dataclass(frozen=True, slots=True)
class ParameterVariant:
    identifier: str
    skipped: bool = False


ParameterDimension: TypeAlias = tuple[ParameterVariant, ...]
MAX_PARAMETER_VARIANTS = 10_000


def parameter_dimensions(
    decorators: list[ast.expr], bindings: StaticBindings, budget: EvaluationBudget
) -> tuple[ParameterDimension, ...] | None:
    dimensions: list[ParameterDimension] = []
    try:
        for decorator in reversed(decorators):
            if not _is_parametrize(decorator):
                continue
            assert isinstance(decorator, ast.Call)
            dimensions.append(_parametrize_dimension(decorator, bindings, budget))
    except StaticBudgetError:
        raise
    except StaticProofError:
        return None
    return tuple(dimensions)


def fixture_parameter_dimension(
    expression: ast.expr,
    ids: ast.expr | None,
    bindings: StaticBindings,
    budget: EvaluationBudget,
) -> ParameterDimension | None:
    try:
        return _variants(expression, ids, bindings, argument_count=1, budget=budget)
    except StaticBudgetError:
        raise
    except StaticProofError:
        return None


def combined_parameter_variants(
    dimensions: tuple[ParameterDimension, ...],
    budget: EvaluationBudget,
) -> tuple[ParameterVariant, ...] | None:
    if not dimensions:
        return ()
    total = 1
    for dimension in dimensions:
        budget.consume()
        total *= len(dimension)
        if total > MAX_PARAMETER_VARIANTS:
            return None
    variants: list[ParameterVariant] = []
    for items in product(*dimensions):
        budget.consume()
        variants.append(
            ParameterVariant(
                identifier="-".join(item.identifier for item in items),
                skipped=any(item.skipped for item in items),
            )
        )
    identifiers = {variant.identifier for variant in variants}
    return tuple(variants) if len(identifiers) == len(variants) else None


def parametrized_names(decorators: list[ast.expr]) -> frozenset[str] | None:
    names: set[str] = set()
    for decorator in decorators:
        if not _is_parametrize(decorator):
            continue
        assert isinstance(decorator, ast.Call)
        if not decorator.args:
            return None
        expression = decorator.args[0]
        literal_names = _literal_parameter_names(expression)
        if literal_names is None or names.intersection(literal_names):
            return None
        names.update(literal_names)
    return frozenset(names)


def _parametrize_dimension(
    decorator: ast.Call, bindings: StaticBindings, budget: EvaluationBudget
) -> ParameterDimension:
    if len(decorator.args) != 2:
        raise StaticProofError("pytest parametrization requires argument values")
    if any(keyword.arg != "ids" for keyword in decorator.keywords):
        raise StaticProofError("unsupported pytest parametrization keyword")
    names = _literal_parameter_names(decorator.args[0])
    if names is None or not names or len(set(names)) != len(names):
        raise StaticProofError("pytest parametrization names must be literal")
    ids = next(
        (keyword.value for keyword in decorator.keywords if keyword.arg == "ids"),
        None,
    )
    if ids is not None:
        try:
            return _variants(
                decorator.args[1], ids, bindings, len(names), budget=budget
            )
        except StaticBudgetError:
            raise
        except StaticProofError:
            values = decorator.args[1]
            if not isinstance(values, (ast.List, ast.Tuple)):
                raise StaticProofError(
                    "explicit IDs require a literal value collection"
                ) from None
            identifiers = static_collection(
                evaluate_static(ids, bindings, budget=budget)
            )
            if len(identifiers) != len(values.elts) or not identifiers:
                raise StaticProofError(
                    "pytest ids and values have unequal lengths"
                ) from None
            if not all(isinstance(identifier, str) for identifier in identifiers):
                raise StaticProofError("pytest ids must be literal strings") from None
            if not all(
                _safe_identifier(identifier)
                for identifier in identifiers
                if isinstance(identifier, str)
            ):
                raise StaticProofError(
                    "pytest ID requires unsupported escaping"
                ) from None
            if len(set(identifiers)) != len(identifiers):
                raise StaticProofError(
                    "pytest parametrization IDs must be unique"
                ) from None
            if len(names) > 1 and any(
                not isinstance(value, (ast.List, ast.Tuple))
                or len(value.elts) != len(names)
                for value in values.elts
            ):
                raise StaticProofError("pytest values have incorrect arity") from None
            if any(
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Attribute)
                and value.func.attr == "param"
                and isinstance(value.func.value, ast.Name)
                and value.func.value.id == "pytest"
                for value in values.elts
            ):
                raise StaticProofError(
                    "pytest.param values require complete static proof"
                ) from None
            return tuple(
                ParameterVariant(identifier)
                for identifier in identifiers
                if isinstance(identifier, str)
            )
    return _variants(decorator.args[1], ids, bindings, len(names), budget=budget)


def _variants(
    expression: ast.expr,
    ids_expression: ast.expr | None,
    bindings: StaticBindings,
    argument_count: int,
    *,
    budget: EvaluationBudget,
) -> ParameterDimension:
    if isinstance(expression, (ast.Set, ast.SetComp)):
        raise StaticProofError("set parametrization has unstable cardinality")
    values = static_collection(evaluate_static(expression, bindings, budget=budget))
    explicit_ids: tuple[StaticValue, ...] | None = None
    if ids_expression is not None:
        explicit_ids = static_collection(
            evaluate_static(ids_expression, bindings, budget=budget)
        )
        if len(explicit_ids) != len(values):
            raise StaticProofError("pytest ids and values have unequal lengths")
    variants: list[ParameterVariant] = []
    for index, value in enumerate(values):
        budget.consume()
        explicit = None if explicit_ids is None else explicit_ids[index]
        if explicit is not None and not isinstance(explicit, str):
            raise StaticProofError("pytest ids must be literal strings")
        variants.append(_variant(value, explicit, argument_count))
    if not variants:
        raise StaticProofError("pytest parametrization must be non-empty")
    if len({variant.identifier for variant in variants}) != len(variants):
        raise StaticProofError("pytest parametrization IDs must be unique")
    return tuple(variants)


def _variant(
    value: StaticValue, explicit_id: str | None, argument_count: int
) -> ParameterVariant:
    if isinstance(value, StaticParameter):
        if len(value.values) != argument_count:
            raise StaticProofError("pytest.param values have incorrect arity")
        return ParameterVariant(value.identifier, value.skipped)
    parts = value if argument_count > 1 and isinstance(value, tuple) else (value,)
    if len(parts) != argument_count:
        raise StaticProofError("pytest values have incorrect arity")
    if explicit_id is not None:
        if not _safe_identifier(explicit_id):
            raise StaticProofError("pytest ID requires unsupported escaping")
        return ParameterVariant(explicit_id)
    if not all(_is_id_scalar(part) for part in parts):
        raise StaticProofError("pytest values require explicit static ids")
    return ParameterVariant("-".join(str(part) for part in parts))


def _is_id_scalar(value: StaticValue) -> bool:
    return (
        value is None
        or isinstance(value, (int, float, bool))
        or (isinstance(value, str) and _safe_identifier(value))
    )


def _safe_identifier(value: str) -> bool:
    return (
        bool(value)
        and value.isascii()
        and all(character.isprintable() for character in value)
        and "::" not in value
        and "[" not in value
        and "]" not in value
    )


def _is_parametrize(decorator: ast.expr) -> bool:
    return (
        isinstance(decorator, ast.Call)
        and isinstance(decorator.func, ast.Attribute)
        and decorator.func.attr == "parametrize"
        and isinstance(decorator.func.value, ast.Attribute)
        and decorator.func.value.attr == "mark"
        and isinstance(decorator.func.value.value, ast.Name)
        and decorator.func.value.value.id == "pytest"
    )


def _literal_parameter_names(expression: ast.expr) -> tuple[str, ...] | None:
    if isinstance(expression, ast.Constant) and isinstance(expression.value, str):
        names = tuple(part.strip() for part in expression.value.split(","))
        return names if all(names) and len(set(names)) == len(names) else None
    if isinstance(expression, (ast.List, ast.Tuple)) and all(
        isinstance(part, ast.Constant) and isinstance(part.value, str)
        for part in expression.elts
    ):
        names = tuple(
            part.value
            for part in expression.elts
            if isinstance(part, ast.Constant) and isinstance(part.value, str)
        )
        return names if all(names) and len(set(names)) == len(names) else None
    return None
