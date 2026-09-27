#!/usr/bin/env python3
"""Entrypoint wrapper so the nightly ideation-dashboard IMAGE REFRESH lane runs
without PYTHONPATH setup (mirrors scripts/ideation-dashboard-nightly.py):

    python3 scripts/dashboard-refresh-nightly.py --repo-root <aggregation checkout>

add-nightly-dashboard-refresh tasks 4.3/4.7; the lane itself lives in
ideation_dashboard/dashboard_refresh_lane.py. Exits 0 — every error is
reported as a recorded outcome (`skipped` / `strict_failed`) so the
deterministic doc-health run and the delivered report are never affected —
except a seal phase that could not write its own seal result, which exits
non-zero (`SEAL_RESULT_UNWRITTEN_EXIT`) so that its continue-on-error step,
not a result it did not write, withholds the dispatch."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ideation_dashboard.dashboard_refresh_lane import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
