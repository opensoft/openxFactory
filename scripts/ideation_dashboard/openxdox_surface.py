"""The openXdox surface openxFactory's own adapter is allowed to reach.

WHY THIS FILE EXISTS. Under RULING OQ-2 openDox is pinned ONLY by openXdox, and
under `split-opendox-two-layer-product` § 5.1 (RULING F) openxFactory pins the
openXdox assembly root and nothing else. So after the carve there is no import
path from openxFactory's retained engineering adapter to openDox at all — not a
narrow one, not a lazy one. `intent_apply_lane.py` had exactly one such reach:
it rehydrated the live branch sessions from the checkout through
`branch_session.bootstrap_sessions`, and `branch_session` (5,290 lines) is
openDox under design D3.

The honest shape — and Brett Heap's ruling on `#656` (2026-09-09, "rule all OQs
as recommended", OQ-B item B-3) — is that openxFactory's lane reaches sessions
THROUGH openXdox, which already imports `branch_session` in its own right
(`cli_gate.py:46`, `gate_routes.py:70`, `doxbench_scope.py:729`). This module is
that reach made explicit and given a name, one commit before the carve rather
than as an undeclared edge discovered during it.

WHAT IT IS AND IS NOT. It is a NAMED RE-EXPORT, nothing else: no wrapper, no
adaptation, no policy. The names below are the SAME OBJECTS as
`branch_session`'s — not copies, not partials — so behaviour, signatures and
identity are unchanged and `surface.bootstrap_sessions is
branch_session.bootstrap_sessions` holds (asserted in
`tests/ideation-dashboard/test_oqb_replumb.py`). It is deliberately NOT a
general facade: a name is added here when a stays-column caller needs it and is
ruled to reach it through openXdox, and every addition is one line plus its
reason. Anything wider would be openXdox re-publishing openDox's API, which is
what pinning the assembly root already does properly.

AT THE CARVE this file travels to openXdox-code with the rest of the oXd column
(design D3), and `intent_apply_lane.py`'s import becomes a package-path rewrite
— the `import rewrites` edit class, one line — rather than an edge nothing in
the manifest's vocabulary can express.
"""

from __future__ import annotations

# Session rehydration. `intent_apply_lane._live_session_registry` derives the
# live sessions from the worktrees and branches beside the checkout, exactly as
# the CLI does, through the one bootstrap every session-bearing verb goes
# through; openXdox owns the gate and commission loop that already depends on it.
from .branch_session import bootstrap_sessions  # noqa: F401  (re-export)

__all__ = ["bootstrap_sessions"]
