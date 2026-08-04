#!/usr/bin/env python3
"""Entrypoint wrapper so the nightly snapshot lane runs without PYTHONPATH
setup (mirrors scripts/doc-health.py):

    python3 scripts/ideation-dashboard-nightly.py --repo-root <aggregation checkout>

add-ideation-dashboard task 4.1; the lane itself lives in
ideation_dashboard/nightly_lane.py. Always exits 0 — any error is reported as
SKIPPED so the deterministic doc-health run is never affected."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ideation_dashboard.nightly_lane import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
