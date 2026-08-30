#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def _run() -> int:
    try:
        if __package__:
            from .council_convening_validation.cli import main
        else:
            sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
            from scripts.council_convening_validation.cli import main
    except ModuleNotFoundError as error:
        dependency = error.name or "Python dependency"
        print(f"ERROR [CC-DEPENDENCY] {dependency} is required", file=sys.stderr)
        return 2
    return main()


if __name__ == "__main__":
    raise SystemExit(_run())
