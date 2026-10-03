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


class QualityArgs(argparse.Namespace):
    show_surface: bool

    def __init__(self) -> None:
        super().__init__()
        self.show_surface = False


def resolve_programming_checker() -> Path:
    configured = os.environ.get("PROGRAMMING_CHECKER")
    if configured:
        explicit = Path(configured).expanduser()
        if not explicit.is_file():
            raise SystemExit(
                "configured programming checker unavailable: " + str(explicit)
            )
        return explicit
    candidates = (
        Path.home()
        / ".cache/opencode/packages/oh-my-opencode@latest/node_modules/oh-my-opencode/dist/skills/programming/scripts/python/check-no-excuse-rules.py",
        Path.home()
        / ".cache/opencode/node_modules/oh-my-opencode/dist/skills/programming/scripts/python/check-no-excuse-rules.py",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit(
        "programming checker unavailable; set PROGRAMMING_CHECKER to "
        + "check-no-excuse-rules.py"
    )


def quality_commands(
    checker: Path, root: Path | None = None
) -> tuple[QualityCommand, ...]:
    repository = Path(__file__).resolve().parents[2] if root is None else root
    surface = tuple(
        str((repository / path).resolve().relative_to(repository))
        for path in QUALITY_SURFACE
    )
    return (
        QualityCommand("ruff", ("uvx", "ruff@0.16.10", "check", *surface)),
        QualityCommand(
            "basedpyright",
            ("uvx", "basedpyright@1.40.1", *surface),
        ),
        QualityCommand(
            "programming-checker",
            (sys.executable, str(checker), *surface),
        ),
    )


def run_quality_gate(root: Path) -> int:
    checker = resolve_programming_checker()
    for command in quality_commands(checker, root):
        print(f"[{command.name}] {' '.join(command.arguments)}", flush=True)
        completed = subprocess.run(command.arguments, cwd=root, check=False)
        if completed.returncode != 0:
            return completed.returncode
    return 0


def parse_args(arguments: Sequence[str]) -> QualityArgs:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--show-surface", action="store_true")
    return parser.parse_args(arguments, namespace=QualityArgs())


def main(arguments: Sequence[str] | None = None) -> int:
    options = parse_args(sys.argv[1:] if arguments is None else arguments)
    if options.show_surface:
        print("\n".join(QUALITY_SURFACE))
        return 0
    root = Path(__file__).resolve().parents[2]
    return run_quality_gate(root)


if __name__ == "__main__":
    raise SystemExit(main())
