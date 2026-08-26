from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

QUALITY_SURFACE: tuple[str, ...] = (
    "scripts/sync-notebooklm-books.py",
    "scripts/notebooklm_sync",
    "tests/notebooklm",
)


@dataclass(frozen=True, slots=True)
class QualityCommand:
    name: str
    arguments: tuple[str, ...]


def resolve_programming_checker() -> Path:
    configured = os.environ.get("PROGRAMMING_CHECKER")
    candidates = (
        Path(configured).expanduser() if configured else None,
        Path.home()
        / ".cache/opencode/packages/oh-my-opencode@latest/node_modules/"
        "oh-my-opencode/dist/skills/programming/scripts/python/"
        "check-no-excuse-rules.py",
        Path.home()
        / ".cache/opencode/node_modules/oh-my-opencode/dist/skills/"
        "programming/scripts/python/check-no-excuse-rules.py",
    )
    for candidate in candidates:
        if candidate is not None and candidate.is_file():
            return candidate
    raise SystemExit(
        "programming checker unavailable; set PROGRAMMING_CHECKER to "
        "check-no-excuse-rules.py"
    )


def quality_commands(checker: Path) -> tuple[QualityCommand, ...]:
    return (
        QualityCommand("ruff", ("uvx", "ruff", "check", *QUALITY_SURFACE)),
        QualityCommand(
            "basedpyright",
            ("uvx", "basedpyright", *QUALITY_SURFACE),
        ),
        QualityCommand(
            "programming-checker",
            (sys.executable, str(checker), *QUALITY_SURFACE),
        ),
    )


def run_quality_gate(root: Path) -> int:
    checker = resolve_programming_checker()
    for command in quality_commands(checker):
        print(f"[{command.name}] {' '.join(command.arguments)}", flush=True)
        completed = subprocess.run(command.arguments, cwd=root, check=False)
        if completed.returncode != 0:
            return completed.returncode
    return 0


def parse_args(arguments: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-surface", action="store_true")
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> int:
    options = parse_args(sys.argv[1:] if arguments is None else arguments)
    if options.show_surface:
        print("\n".join(QUALITY_SURFACE))
        return 0
    root = Path(__file__).resolve().parents[2]
    return run_quality_gate(root)


if __name__ == "__main__":
    raise SystemExit(main())
