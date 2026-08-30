from __future__ import annotations

from pathlib import Path

from scripts.hermes_runtime_validation.pytest_inventory import (
    collect_static_pytest_nodes,
)
from tests.hermes_runtime_contracts.static_evidence_helpers import collect, write_test

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_postgres_cluster_exposes_explicit_major_node_ids() -> None:
    nodes = collect_static_pytest_nodes(
        REPOSITORY_ROOT,
        ("tests/hermes_runtime_contracts/postgres/test_clean_apply.py",),
    )

    assert {
        "tests/hermes_runtime_contracts/postgres/test_clean_apply.py::"
        "test_clean_apply_to_empty_database_passes_the_locked_boundary[15]",
        "tests/hermes_runtime_contracts/postgres/test_clean_apply.py::"
        "test_clean_apply_to_empty_database_passes_the_locked_boundary[16]",
    } <= set(nodes)


def test_plain_tuple_with_wrong_arity_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('left,right', [(1,)], ids=['forged'])\n"
        "def test_case(left, right): pass\n",
    )
    node = f"{path}::test_case[forged]"
    assert node not in collect(tmp_path, node).collected


def test_set_with_runtime_deduplication_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('value', {1, 1}, ids=['one', 'forged'])\n"
        "def test_case(value): pass\n",
    )
    node = f"{path}::test_case[forged]"
    assert node not in collect(tmp_path, node).collected


def test_dynamic_reassignment_invalidates_stale_parameter_ids(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "CASES = [pytest.param(1, id='forged')]\n"
        "def build(): return [pytest.param(2, id='actual')]\n"
        "CASES = build()\n"
        "@pytest.mark.parametrize('value', CASES)\n"
        "def test_case(value): pass\n",
    )
    node = f"{path}::test_case[forged]"
    assert node not in collect(tmp_path, node).collected


def test_missing_indirect_fixture_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('missing', [1], ids=['forged'], indirect=True)\n"
        "def test_case(missing): pass\n",
    )
    node = f"{path}::test_case[forged]"
    assert node not in collect(tmp_path, node).collected


def test_foreign_fixture_decorator_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "class Evil:\n"
        "    def fixture(self, **kwargs): return lambda function: function\n"
        "evil = Evil()\n"
        "@evil.fixture(params=[1])\n"
        "def ambient(): return 1\n"
        "def test_case(ambient): pass\n",
    )
    node = f"{path}::test_case[1]"
    assert node not in collect(tmp_path, node).collected


def test_dynamic_fixture_alias_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\nALIAS = 'ambient'\n"
        "@pytest.fixture(name=ALIAS)\n"
        "def source(): return 1\n"
        "def test_case(source): pass\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_dynamic_autouse_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\nAUTO = True\n"
        "@pytest.fixture(autouse=AUTO, params=[pytest.param(1, id='one')])\n"
        "def ambient(request): return request.param\n"
        "def test_case(): pass\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_unknown_test_decorator_is_unproved(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "def hide(function): return None\n"
        "@hide\ndef test_case(): pass\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected
