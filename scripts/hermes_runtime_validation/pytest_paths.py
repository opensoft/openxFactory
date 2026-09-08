from __future__ import annotations

from pathlib import PurePosixPath

TEST_ROOT = PurePosixPath("tests/hermes_runtime_contracts")


def valid_test_path(path: PurePosixPath) -> bool:
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and path.is_relative_to(TEST_ROOT)
        and path.suffix == ".py"
    )
