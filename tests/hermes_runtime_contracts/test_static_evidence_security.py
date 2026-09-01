from __future__ import annotations

from pathlib import Path

from scripts.hermes_runtime_validation.pytest_inventory import (
    collect_evidence_test_nodes,
)


def _register(node_id: str) -> dict[str, object]:
    return {"entries": [{"test_node_ids": [node_id]}]}


def _write_test(
    repo_root: Path,
    source: str,
    relative: Path = Path("tests/hermes_runtime_contracts/test_evidence.py"),
) -> str:
    path = repo_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return relative.as_posix()


def test_parameterized_node_when_id_injects_unknown_segment_then_rejected(
    tmp_path: Path,
) -> None:
    path = _write_test(
        tmp_path,
        "import pytest\n\n"
        "@pytest.mark.parametrize('left', ['x'])\n"
        "@pytest.mark.parametrize('right', ['y'])\n"
        "def test_combined(left, right):\n"
        "    assert left and right\n",
    )
    forged = f"{path}::test_combined[y-FORGED-x]"

    inventory = collect_evidence_test_nodes(tmp_path, _register(forged))

    assert forged not in inventory.collected


def test_evidence_node_when_statically_skipped_then_reported_as_skipped(
    tmp_path: Path,
) -> None:
    path = _write_test(
        tmp_path,
        "import pytest\n\n"
        "@pytest.mark.skip(reason='not executable')\n"
        "def test_skipped():\n"
        "    assert True\n",
    )
    node_id = f"{path}::test_skipped"

    inventory = collect_evidence_test_nodes(tmp_path, _register(node_id))

    assert inventory.collected == (node_id,)
    assert inventory.skipped == (node_id,)


def test_parameterized_node_when_ids_use_prior_name_and_comprehension_then_proved(
    tmp_path: Path,
) -> None:
    path = _write_test(
        tmp_path,
        "import pytest\n\n"
        "CASES = (('alpha', 1), ('beta', 2))\n"
        "CASE_IDS = [case_id for case_id, _ in CASES]\n\n"
        "@pytest.mark.parametrize('value', [value for _, value in CASES], ids=CASE_IDS)\n"
        "def test_named_ids(value):\n"
        "    assert value\n",
    )
    node_id = f"{path}::test_named_ids[beta]"

    inventory = collect_evidence_test_nodes(tmp_path, _register(node_id))

    assert inventory.collected == (node_id,)


def test_node_when_transitive_fixture_is_parameterized_then_fixture_id_prefixes(
    tmp_path: Path,
) -> None:
    postgres_root = Path("tests/hermes_runtime_contracts/postgres")
    conftest = tmp_path / postgres_root / "conftest.py"
    conftest.parent.mkdir(parents=True)
    conftest.write_text(
        "import pytest\n\n"
        "MAJORS = (\n"
        "    pytest.param('15', id='15'),\n"
        "    pytest.param('16', id='16', marks=pytest.mark.skip(reason='static')),\n"
        ")\n\n"
        "@pytest.fixture(params=MAJORS)\n"
        "def postgres_cluster(request):\n"
        "    return request.param\n\n"
        "@pytest.fixture\n"
        "def postgres_database(postgres_cluster):\n"
        "    return postgres_cluster\n",
        encoding="utf-8",
    )
    path = _write_test(
        tmp_path,
        "import pytest\n\n"
        "@pytest.mark.parametrize('left', ['x'])\n"
        "@pytest.mark.parametrize('right', ['y'])\n"
        "def test_transitive(postgres_database, left, right):\n"
        "    assert postgres_database and left and right\n",
        postgres_root / "test_evidence.py",
    )
    selected = f"{path}::test_transitive[15-y-x]"
    skipped = f"{path}::test_transitive[16-y-x]"

    inventory = collect_evidence_test_nodes(
        tmp_path,
        {"entries": [{"test_node_ids": [selected, skipped]}]},
    )

    assert inventory.collected == (selected, skipped)
    assert inventory.skipped == (skipped,)
