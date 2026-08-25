#!/usr/bin/env python3
"""Entrypoint wrapper so the ideation-readiness lane runs without PYTHONPATH
setup (mirrors scripts/doc-health.py / scripts/ideation-dashboard-nightly.py):

    python3 scripts/ideation-readiness-nightly.py --repo-root <aggregation checkout> \\
        --phase prepare --out-dir <bundle dir> --as-of <YYYY-MM-DD> --run-id <id>

    python3 scripts/ideation-readiness-nightly.py --repo-root <aggregation checkout> \\
        --phase merge --as-of <YYYY-MM-DD> --run-id <id> \\
        [--findings-in <file>] [--unavailable-reason <reason>] \\
        [--report-in <dated report path>]

openxFactory change add-ideation-cross-reference-readiness, tasks 4.1/4.3; the
lane itself lives in doc_health/readiness_dispatch.py. The merge phase always
exits 0 — any error is reported as SKIPPED so the deterministic doc-health run
(already committed to disk by the time this lane runs) is never affected."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from doc_health.readiness_dispatch import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
