#!/usr/bin/env python3
"""Entrypoint wrapper so the dashboard serve runs from THIS repository, POST-SHED
(mirrors `scripts/ideation-dashboard-nightly.py` and `scripts/doc-health.py`):

    python3 scripts/ideation-dashboard-serve.py --snapshot … --checkout-root …

WHY A WRAPPER APPEARED HERE. Before `split-opendox-two-layer-product` § 5.2 the
serve was `python3 -m ideation_dashboard.serve` with `PYTHONPATH=scripts`, and
that one line did three things at once: it found the module, it found every
sibling column the module imports, and it got openxFactory's composition point
bound because `serve.py` sat in the same package as `profile_openxfactory.py`.
The shed moved `serve.py` to openDox-code and deleted the profile's old path
(the manifest's single `deleted_at_carve` row), so the old line now finds
nothing — and would still be wrong if it did, because none of the three things
it used to do happens by itself any more:

  * the module is at a PINNED leg, and reading it lawfully means reading it
    through this repository's own pin (RULED Q7, `#656` `5626248666`);
  * the serve's columns span BOTH legs — `openxdox.serve_gate` and
    `openxdox.serve_projection` are openXdox's — so one `src/` on the path is
    not enough and a single-leg install fails on the seventeenth import
    (measured: `ideation/brainstorm/opendox-shed-exit-a-post-shed-mode-measured.md`);
  * `build_server` names `profile_openxfactory` as a BARE GLOBAL with no
    import anywhere, so the profile has to be REGISTERED with it — § 4.3's
    hole, answered by RULED ASK-2 option (2) (`#656` `5628886636`).

`carved_reach` does all three, and this file is the one place a person or a
service unit runs to get them. It is what `scripts/reserve-dashboard.sh`
executes; the Copilot finding that prompted it (`PRRT_kwDOTAvnrs6hbVwB`) is
exactly that a registration performed only by two pytest conftests is not a
registration a real server process ever receives.

REFUSES RATHER THAN DEGRADES. `require()` is the EAGER check — this process is
about to serve, so an uninitialized gitlink is a checkout that cannot do the
job, not a condition to work around, and finding out here beats finding out at
the first request. The message it raises names the leg, the missing path and
the command that fixes it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import carved_reach  # noqa: E402

carved_reach.require()
carved_reach.install()
carved_reach.bind_composition_point()

from opendox.serve import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
