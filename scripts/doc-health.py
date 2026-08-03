#!/usr/bin/env python3
"""Entrypoint wrapper so the suite runs without PYTHONPATH setup:
python3 scripts/doc-health.py --repo-root <aggregation checkout> [...]"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from doc_health.runner import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
