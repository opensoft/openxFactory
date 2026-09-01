from __future__ import annotations

from pathlib import Path

import pytest

from scripts.hermes_runtime_validation.pytest_count import count_static_pytest_nodes
from tests.hermes_runtime_contracts.static_evidence_helpers import collect, write_test


def test_invalid_ancestor_conftest_is_unproved(tmp_path: Path) -> None:
    conftest = tmp_path / "tests/hermes_runtime_contracts/conftest.py"
    conftest.parent.mkdir(parents=True)
    conftest.write_text("def broken(:\n", encoding="utf-8")
    path = write_test(tmp_path, "def test_case(): pass\n")
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_collection_hook_is_unproved(tmp_path: Path) -> None:
    conftest = tmp_path / "tests/hermes_runtime_contracts/conftest.py"
    conftest.parent.mkdir(parents=True)
    conftest.write_text(
        "def pytest_collection_modifyitems(items): items.clear()\n",
        encoding="utf-8",
    )
    path = write_test(tmp_path, "def test_case(): pass\n")
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_root_collection_hook_is_unproved(tmp_path: Path) -> None:
    conftest = tmp_path / "tests/conftest.py"
    conftest.parent.mkdir(parents=True)
    conftest.write_text(
        "def pytest_collection_modifyitems(items): items.clear()\n",
        encoding="utf-8",
    )
    path = write_test(tmp_path, "def test_case(): pass\n")
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_aliased_collection_hook_is_unproved(tmp_path: Path) -> None:
    conftest = tmp_path / "tests/hermes_runtime_contracts/conftest.py"
    conftest.parent.mkdir(parents=True)
    conftest.write_text(
        "def hide(items): items.clear()\npytest_collection_modifyitems = hide\n",
        encoding="utf-8",
    )
    path = write_test(tmp_path, "def test_case(): pass\n")
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_imported_root_autouse_skip_is_unproved(tmp_path: Path) -> None:
    tests_root = tmp_path / "tests"
    tests_root.mkdir()
    (tests_root / "ambient.py").write_text(
        "import pytest\n"
        "@pytest.fixture(autouse=True)\n"
        "def stop(): pytest.skip('ambient')\n",
        encoding="utf-8",
    )
    (tests_root / "conftest.py").write_text(
        "from ambient import stop\n",
        encoding="utf-8",
    )
    path = write_test(tmp_path, "def test_case(): pass\n")
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_imported_root_parameter_fixture_contributes_node_id(tmp_path: Path) -> None:
    tests_root = tmp_path / "tests"
    tests_root.mkdir()
    (tests_root / "ambient.py").write_text(
        "import pytest\n"
        "@pytest.fixture(autouse=True, params=[pytest.param(1, id='ambient')])\n"
        "def source(request): return request.param\n",
        encoding="utf-8",
    )
    (tests_root / "conftest.py").write_text(
        "from ambient import source\n",
        encoding="utf-8",
    )
    path = write_test(tmp_path, "def test_case(): pass\n")
    node = f"{path}::test_case[ambient]"
    assert collect(tmp_path, node).collected == (node,)


@pytest.mark.parametrize("marker", ["pytest.mark.skip"])
def test_nonexecuting_marker_is_reported_as_skipped(
    tmp_path: Path, marker: str
) -> None:
    path = write_test(
        tmp_path,
        f"import pytest\n@{marker}\ndef test_case(): pass\n",
    )
    node = f"{path}::test_case"
    assert collect(tmp_path, node).skipped == (node,)


@pytest.mark.parametrize(
    "marker",
    [
        "pytest.mark.xfail",
        "pytest.mark.xfail(strict=True)",
        "pytest.mark.xfail(run=True)",
        "pytest.mark.xfail(run=False)",
    ],
)
def test_xfail_marker_is_never_mandatory_evidence(
    tmp_path: Path, marker: str
) -> None:
    path = write_test(
        tmp_path,
        f"import pytest\n@{marker}\ndef test_case(): assert False\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_module_usefixtures_requires_parameterized_fixture_id(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "import pytest\n"
        "@pytest.fixture(params=[pytest.param(1, id='one')])\n"
        "def ambient(request): return request.param\n"
        "pytestmark = pytest.mark.usefixtures('ambient')\n"
        "def test_case(): pass\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected


def test_foreign_parametrize_static_count_is_rejected(tmp_path: Path) -> None:
    path = write_test(
        tmp_path,
        "class Fake:\n"
        "    def parametrize(self, *args): return lambda function: function\n"
        "fake = Fake()\n"
        "@fake.parametrize('value', [1, 2, 3])\n"
        "def test_case(value): pass\n",
    )
    with pytest.raises(ValueError, match="unsupported pytest decorator"):
        count_static_pytest_nodes(tmp_path, [path])


def test_cumulative_static_evaluation_budget_is_fail_closed(tmp_path: Path) -> None:
    values = ",".join(str(value) for value in range(1_000))
    copies = "".join(f"COPY_{index} = [item for item in VALUES]\n" for index in range(100))
    path = write_test(
        tmp_path,
        f"VALUES = ({values})\n{copies}\ndef test_case(): pass\n",
    )
    node = f"{path}::test_case"
    assert node not in collect(tmp_path, node).collected
