from __future__ import annotations

from pathlib import Path

import tomllib


def test_ruff_exception_is_one_path_and_one_rule() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    document = tomllib.loads(
        (repository_root / "ruff.toml").read_text(encoding="utf-8")
    )

    assert document == {
        "lint": {
            "per-file-ignores": {
                "scripts/validate-council-convening.py": ["N999"],
            },
        },
    }
