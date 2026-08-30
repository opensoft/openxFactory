from __future__ import annotations

from pathlib import Path

from scripts.hermes_runtime_validation.pytest_inventory import (
    collect_evidence_test_nodes,
)


def _collect(tmp_path: Path, source: str, node: str):
    relative = Path("tests/hermes_runtime_contracts/test_edge.py")
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    node_id = f"{relative.as_posix()}::{node}"
    register = {"entries": [{"test_node_ids": [node_id]}]}
    return node_id, collect_evidence_test_nodes(tmp_path, register)


def test_explicit_ids_when_cardinality_differs_then_node_is_unproved(tmp_path: Path) -> None:
    node, inventory = _collect(
        tmp_path,
        "import pytest\n@pytest.mark.parametrize('value', [1], ids=['ok', 'forged'])\ndef test_case(value): pass\n",
        "test_case[forged]",
    )
    assert node not in inventory.collected


def test_pytest_param_when_arity_differs_then_node_is_unproved(tmp_path: Path) -> None:
    node, inventory = _collect(
        tmp_path,
        "import pytest\n@pytest.mark.parametrize('left,right', [pytest.param(1, id='forged')])\ndef test_case(left, right): pass\n",
        "test_case[forged]",
    )
    assert node not in inventory.collected


def test_module_pytestmark_when_skipped_then_node_is_reported(tmp_path: Path) -> None:
    node, inventory = _collect(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.skip(reason='ambient')\ndef test_case(): pass\n",
        "test_case",
    )
    assert inventory.collected == (node,)
    assert inventory.skipped == (node,)


def test_autouse_alias_fixture_when_parameterized_then_id_is_required(tmp_path: Path) -> None:
    node, inventory = _collect(
        tmp_path,
        "import pytest\n@pytest.fixture(name='ambient', autouse=True, params=[pytest.param(1, id='one')])\ndef source(request): return request.param\ndef test_case(): pass\n",
        "test_case[one]",
    )
    assert inventory.collected == (node,)


def test_parameter_product_when_over_budget_then_node_is_unproved(tmp_path: Path) -> None:
    values = ",".join(str(value) for value in range(101))
    node, inventory = _collect(
        tmp_path,
        f"import pytest\n@pytest.mark.parametrize('left', [{values}])\n@pytest.mark.parametrize('right', [{values}])\ndef test_case(left, right): pass\n",
        "test_case[0-0]",
    )
    assert node not in inventory.collected
