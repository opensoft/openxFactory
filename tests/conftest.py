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

from carved_reach import install as install_carved_reach  # noqa: E402

install_carved_reach(tests=True)

# --------------------------------------------------------------------------
# THE ONE PROCESS-START REGISTRATION (§ 4.3, RULED ASK-2 option (2), `#656`
# comment `5628886636`; § 4.4, RULING C2 and RULED ASK-4 Q5, `5634195861`).
# `opendox.cli.build_parser` and `opendox.serve.build_server` read
# `profile_openxfactory` through openDox-code's lazy proxy and REFUSE when no
# host has registered a profile; openXdox's lifecycle engine reads its status
# vocabulary from the same registration by delegation. This suite builds both
# parsers and servers in-process, so it is an ASSEMBLY POINT and makes the
# call. Once for the whole suite rather than per test module, for the same
# reason the reach above is installed once: one place to read.
# --------------------------------------------------------------------------

from opendox_host import register_openxfactory  # noqa: E402

register_openxfactory()

from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    hermetic_binary_path,
    hermetic_external_runners,
)
