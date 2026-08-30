from __future__ import annotations

import ast

from scripts.hermes_runtime_validation.pytest_parameter_variants import (
    MAX_PARAMETER_VARIANTS as _MAX_PARAMETER_VARIANTS,
)
from scripts.hermes_runtime_validation.pytest_parameter_variants import (
    ParameterDimension as _ParameterDimension,
)
from scripts.hermes_runtime_validation.pytest_parameter_variants import (
    ParameterVariant as _ParameterVariant,
)
from scripts.hermes_runtime_validation.pytest_parameter_variants import (
    combined_parameter_variants as _combined_parameter_variants,
)
from scripts.hermes_runtime_validation.pytest_parameter_variants import (
    fixture_parameter_dimension as _fixture_parameter_dimension,
)
from scripts.hermes_runtime_validation.pytest_parameter_variants import (
    parameter_dimensions as _parameter_dimensions,
)
from scripts.hermes_runtime_validation.pytest_parameter_variants import (
    parametrized_names as _parametrized_names,
)
from scripts.hermes_runtime_validation.pytest_static_values import (
    EvaluationBudget,
    StaticBindings,
    StaticBudgetError,
    StaticProofError,
    evaluate_static,
)
from scripts.hermes_runtime_validation.pytest_support import pytest_marker

MAX_PARAMETER_VARIANTS = _MAX_PARAMETER_VARIANTS
ParameterDimension = _ParameterDimension
ParameterVariant = _ParameterVariant
combined_parameter_variants = _combined_parameter_variants
fixture_parameter_dimension = _fixture_parameter_dimension
parameter_dimensions = _parameter_dimensions
parametrized_names = _parametrized_names


def is_statically_skipped(
    decorators: list[ast.expr], bindings: StaticBindings, budget: EvaluationBudget
) -> bool | None:
    for decorator in decorators:
        marker = pytest_marker(decorator)
        if marker is None:
            continue
        name, call = marker
        if name == "skip":
            return True
        if name == "xfail" and call is not None:
            run = next(
                (keyword.value for keyword in call.keywords if keyword.arg == "run"),
                None,
            )
            if isinstance(run, ast.Constant) and run.value is False:
                return True
        if name != "skipif" or call is None or not call.args:
            continue
        try:
            condition = evaluate_static(call.args[0], bindings, budget=budget)
        except StaticBudgetError:
            raise
        except StaticProofError:
            return None
        if not isinstance(condition, bool):
            return None
        if condition:
            return True
    return False
