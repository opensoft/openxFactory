from __future__ import annotations

from pathlib import Path

import pytest

from scripts.hermes_runtime_validation.pytest_count import count_static_pytest_nodes
from tests.hermes_runtime_contracts.static_evidence_helpers import collect, write_test


def test_shadowed_pytest_binding_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "class Fake:\n"
        "    mark = pytest.mark\n"
        "pytest = Fake()\n"
        "@pytest.mark.parametrize('value', [1], ids=['forged'])\n"
        "def test_case(value): pass\n",
    )
    node = f"{path}::test_case[forged]"
    assert node not in collect(tmp_path, node).collected
    with pytest.raises(ValueError, match="canonical pytest binding"):
        count_static_pytest_nodes(tmp_path, [path])


def test_decorator_uses_binding_at_definition_time(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "CASES = [pytest.param(1, id='real')]\n"
        "@pytest.mark.parametrize('value', CASES)\n"
        "def test_case(value): pass\n"
        "CASES = [pytest.param(2, id='forged')]\n",
    )
    real = f"{path}::test_case[real]"
    forged = f"{path}::test_case[forged]"
    assert collect(tmp_path, real).collected == (real,)
    assert forged not in collect(tmp_path, forged).collected


def test_conditional_reassignment_invalidates_parameter_binding(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "CASES = [pytest.param(1, id='forged')]\n"
        "if True:\n"
        "    CASES = [pytest.param(2, id='actual')]\n"
        "@pytest.mark.parametrize('value', CASES)\n"
        "def test_case(value): pass\n",
    )
    forged = f"{path}::test_case[forged]"
    assert forged not in collect(tmp_path, forged).collected


def test_final_plain_test_definition_replaces_parameterized_definition(
    tmp_path: Path,
) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('value', [1], ids=['forged'])\n"
        "def test_case(value): pass\n"
        "def test_case(): pass\n",
    )
    forged = f"{path}::test_case[forged]"
    plain = f"{path}::test_case"
    assert forged not in collect(tmp_path, forged).collected
    assert collect(tmp_path, plain).collected == (plain,)


def test_final_parameterized_definition_replaces_plain_definition(
    tmp_path: Path,
) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "def test_case(): pass\n"
        "@pytest.mark.parametrize('value', [1], ids=['actual'])\n"
        "def test_case(value): pass\n",
    )
    plain = f"{path}::test_case"
    actual = f"{path}::test_case[actual]"
    assert plain not in collect(tmp_path, plain).collected
    assert collect(tmp_path, actual).collected == (actual,)


def test_final_module_pytestmark_controls_collection(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "pytestmark = []\n"
        "def test_case(): pass\n"
        "pytestmark = pytest.mark.skip(reason='final')\n",
    )
    node = f"{path}::test_case"
    assert collect(tmp_path, node).skipped == (node,)


def test_final_empty_pytestmark_restores_runnable_test(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "pytestmark = pytest.mark.skip(reason='stale')\n"
        "def test_case(): pass\n"
        "pytestmark = []\n",
    )
    node = f"{path}::test_case"
    inventory = collect(tmp_path, node)
    assert inventory.collected == (node,)
    assert inventory.skipped == ()


def test_duplicate_explicit_ids_are_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('value', [1, 2], ids=['same', 'same'])\n"
        "def test_case(value): pass\n",
    )
    node = f"{path}::test_case[same]"
    assert node not in collect(tmp_path, node).collected


def test_non_ascii_explicit_id_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('value', [1], ids=['café'])\n"
        "def test_case(value): pass\n",
    )
    node = f"{path}::test_case[café]"
    assert node not in collect(tmp_path, node).collected


def test_parameter_name_missing_from_signature_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('missing', [1], ids=['forged'])\n"
        "def test_case(): pass\n",
    )
    node = f"{path}::test_case[forged]"
    assert node not in collect(tmp_path, node).collected


def test_parameterized_builtin_fixture_override_requires_id(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.fixture(params=[pytest.param('x', id='override')])\n"
        "def tmp_path(request): return request.param\n"
        "def test_case(tmp_path): pass\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


@pytest.mark.parametrize("suppression", ["skip", "xfail"])
def test_fixture_body_runtime_suppression_is_unproved(
    tmp_path: Path, suppression: str
) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.fixture\n"
        f"def ambient(): pytest.{suppression}('not executed')\n"
        "def test_case(ambient): pass\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_test_body_runtime_skip_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "def test_case(): pytest.skip('not executed')\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_mutated_parameter_binding_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "CASES = [pytest.param(1, id='stale')]\n"
        "CASES.clear()\n"
        "CASES.append(pytest.param(2, id='actual'))\n"
        "@pytest.mark.parametrize('value', CASES)\n"
        "def test_case(value): pass\n",
    )
    node = f"{path}::test_case[stale]"
    assert node not in collect(tmp_path, node).collected


def test_collection_altering_pytest_ini_is_unproved(tmp_path: Path) -> None:
    (tmp_path / "pytest.ini").write_text(
        "[pytest]\npython_functions = check_*\n",
        encoding="utf-8",
    )
    path = write_test(tmp_path, "def test_case(): pass\n")
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected
