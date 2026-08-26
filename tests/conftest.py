"""Suite-wide test configuration.

Its only job is to register the STRUCTURAL hermeticity guard
(`tests/hermeticity.py`) for every test directory under `tests/`, so no run can
reach the real `nlm` or `gh` (FR-043, PR #49 finding 17). It covers every
invocation whose rootdir sits at or above `tests/` — which is every ordinary one,
including `scripts/validate-docs.sh`. Directories that have their OWN conftest.py
register the guard there as well, because a pytest run started from inside such a
directory makes it the rootdir and `confcutdir` then excludes THIS file.

This file deliberately defines nothing else. `conftest` is an ambient top-level
module name with exactly one entry in `sys.modules`, and every test directory's
modules already import their own helpers through it, so anything exported here
would be shadowed the moment a directory conftest loads.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    hermetic_binary_path,
    hermetic_external_runners,
)
