from __future__ import annotations

import ast

from scripts.hermes_runtime_validation.pytest_bindings import statement_binding_names

COLLECTION_HOOKS = frozenset(
    {
        "pytest_collect_file",
        "pytest_collection",
        "pytest_collection_finish",
        "pytest_collection_modifyitems",
        "pytest_generate_tests",
        "pytest_ignore_collect",
        "pytest_make_collect_report",
        "pytest_pycollect_makeitem",
    }
)
COLLECTION_CONTROL_NAMES = frozenset(
    {"__test__", "collect_ignore", "collect_ignore_glob", "pytest_plugins"}
)


def module_collection_supported(module: ast.Module) -> bool:
    final_bindings: set[str] = set()
    for statement in module.body:
        names = statement_binding_names(statement)
        if isinstance(statement, ast.Delete):
            final_bindings.difference_update(names)
        else:
            final_bindings.update(names)
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Attribute) and target.attr == "__test__"
            for target in statement.targets
        ):
            return False
    return not final_bindings.intersection(COLLECTION_HOOKS | COLLECTION_CONTROL_NAMES)


def canonical_pytest_before(
    module: ast.Module, stop_at: ast.stmt, *, initially: bool = False
) -> bool:
    canonical = initially
    for statement in module.body:
        if statement is stop_at:
            break
        if isinstance(statement, ast.Import):
            for alias in statement.names:
                binding = alias.asname or alias.name.partition(".")[0]
                if binding == "pytest":
                    canonical = alias.name == "pytest" and alias.asname in (None, "pytest")
            continue
        if "pytest" in statement_binding_names(statement):
            canonical = False
    return canonical


def test_decorators_supported(decorators: tuple[ast.expr, ...]) -> bool:
    return all(_test_decorator_supported(decorator) for decorator in decorators)


def pytest_marker(decorator: ast.expr) -> tuple[str, ast.Call | None] | None:
    expression = decorator.func if isinstance(decorator, ast.Call) else decorator
    if not (
        isinstance(expression, ast.Attribute)
        and isinstance(expression.value, ast.Attribute)
        and expression.value.attr == "mark"
        and isinstance(expression.value.value, ast.Name)
        and expression.value.value.id == "pytest"
    ):
        return None
    return expression.attr, decorator if isinstance(decorator, ast.Call) else None


def pytest_fixture_call(decorator: ast.expr) -> ast.Call | None:
    expression = decorator.func if isinstance(decorator, ast.Call) else decorator
    if not (
        isinstance(expression, ast.Attribute)
        and expression.attr == "fixture"
        and isinstance(expression.value, ast.Name)
        and expression.value.id == "pytest"
    ):
        return None
    return decorator if isinstance(decorator, ast.Call) else ast.Call(expression, [], [])


def looks_like_fixture_decorator(decorator: ast.expr) -> bool:
    expression = decorator.func if isinstance(decorator, ast.Call) else decorator
    return (
        isinstance(expression, ast.Attribute) and expression.attr == "fixture"
    ) or isinstance(expression, ast.Name) and expression.id == "fixture"


def has_runtime_suppression(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
) -> bool:
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr in {"skip", "xfail"}
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "pytest"
        ):
            return True
    return False


def _test_decorator_supported(decorator: ast.expr) -> bool:
    marker = pytest_marker(decorator)
    if marker is None:
        return False
    name, call = marker
    if name == "postgres":
        return call is None or not call.args and not call.keywords
    if name == "parametrize":
        return call is not None
    if name == "skip":
        return call is None or _reason_only(call)
    if name == "skipif":
        return call is not None and _skipif_supported(call)
    if name == "xfail":
        return False
    if name == "usefixtures":
        return call is not None and not call.keywords and all(
            isinstance(argument, ast.Constant) and isinstance(argument.value, str)
            for argument in call.args
        )
    return False


def _reason_only(call: ast.Call) -> bool:
    return not call.args and all(
        keyword.arg == "reason"
        and isinstance(keyword.value, ast.Constant)
        and isinstance(keyword.value.value, str)
        for keyword in call.keywords
    )


def _skipif_supported(call: ast.Call) -> bool:
    return (
        len(call.args) == 1
        and all(
            keyword.arg == "reason"
            and isinstance(keyword.value, ast.Constant)
            and isinstance(keyword.value.value, str)
            for keyword in call.keywords
        )
    )
