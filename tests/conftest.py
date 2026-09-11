"""Suite-wide test configuration.

Its only job is to register the STRUCTURAL hermeticity guard
(`tests/hermeticity.py`) for every test directory under `tests/`, so no run can
reach the real `nlm` or `gh` (FR-043, PR #49 finding 17). It covers every
invocation whose rootdir sits at or above `tests/` — which is every ordinary one,
including `.github/workflows/pytest-suite.yml`'s required
`python3 -m pytest tests/ -q -m "not postgres"`. Directories that have their
OWN conftest.py register the guard there as well, because a pytest run started
from inside such a directory makes it the rootdir and `confcutdir` then
excludes THIS file.

This file deliberately defines nothing else. `conftest` is an ambient top-level
module name with exactly one entry in `sys.modules`, and every test directory's
modules already import their own helpers through it, so anything exported here
would be shadowed the moment a directory conftest loads.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --------------------------------------------------------------------------
# § 5.2 SHED REACH (RULED (a), `#656` comment `5625573095`; RULED Q7,
# `5626248666`). The shed removed 319 declared paths from this repository, and
# 36 files that STAY still name 38 of those modules. They are read from the two
# PINNED legs — `openDox/code/src` and `openXdox/code/src` — through the ONE
# resolver, `scripts/carved_reach.py`, which refuses by name rather than
# degrading to a skip when a gitlink is not materialized. Installed HERE, in
# the suite-wide conftest `pytest.ini`'s rootdir anchor guarantees is in every
# run's conftest chain, so no test module carries its own copy of the reach.
# --------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from carved_reach import (  # noqa: E402
    bind_composition_point,
    install as install_carved_reach,
)

install_carved_reach(tests=True)

# --------------------------------------------------------------------------
# THE COMPOSITION POINT (§ 4.3, RULED ASK-2 option (2), `#656` comment
# `5628886636`). `opendox.serve.build_server` and `opendox.cli.build_parser`
# still name `profile_openxfactory` as a BARE GLOBAL with no import anywhere —
# the line the § 3 carve deleted rather than moved. openxFactory owns the real
# module (`scripts/profile_openxfactory.py`) and REGISTERS it, which is the
# openxFactory half of the ruling; openDox-code's lazy proxy, the other half,
# is not built yet, so `bind_composition_point()` binds the module into each
# consumer as it loads. Registered for the whole suite rather than per test
# module, for the same reason the reach above is: one place to read, one place
# to delete the day the proxy lands.
# --------------------------------------------------------------------------

bind_composition_point()

from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    hermetic_binary_path,
    hermetic_external_runners,
)
