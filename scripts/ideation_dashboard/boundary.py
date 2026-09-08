"""The interactivity boundary, re-exported from its neutral home.

The guard itself now lives in `scripts/output_boundary.py`, outside BOTH
`ideation_dashboard` and `doc_health` (`split-opendox-two-layer-product`
§ 2.1, design D2 "the neutral module, and it lands FIRST"). `doc_health` used
to import it from here, which made the two packages mutually dependent and put
a cycle across the seam openDox/openXdox has to be cut along; the class moved
so that `doc_health` can reach the guard without reaching into this package.

This module stays as a RE-EXPORT so `ideation_dashboard.boundary` remains a
live import path: roughly ten modules in this package and thirty test modules
name it, and rewriting them would be a large, mechanical diff for no gain
inside a change whose whole point is the one edge it removes. The names below
are the SAME OBJECTS as `output_boundary`'s — not copies — so `isinstance`
checks, `except BoundaryViolation` handlers and refusal-kind string
comparisons behave identically whichever path a caller imports by.

Read the guard's own documentation (its three guarantees, the create-only rule
over the corpus, and the human-only gate) at the top of `output_boundary.py`.
"""

from __future__ import annotations

from output_boundary import (  # noqa: F401  (re-export)
    AGENT,
    DOCUMENT_ESCAPE,
    GATE_SIDE_EFFECT,
    HEADER_INCOMPLETE,
    HUMAN,
    MACHINERY,
    OUTSIDE_ALLOWLIST,
    OUTSIDE_ROOT,
    SESSION_REWRITE,
    SOURCE_DELETE,
    SOURCE_EDIT,
    STAGING_DIR,
    WORKBENCH_DIR,
    BoundaryViolation,
    HumanGate,
    OutputBoundary,
    Refusal,
)

__all__ = [
    "AGENT",
    "DOCUMENT_ESCAPE",
    "GATE_SIDE_EFFECT",
    "HEADER_INCOMPLETE",
    "HUMAN",
    "MACHINERY",
    "OUTSIDE_ALLOWLIST",
    "OUTSIDE_ROOT",
    "SESSION_REWRITE",
    "SOURCE_DELETE",
    "SOURCE_EDIT",
    "STAGING_DIR",
    "WORKBENCH_DIR",
    "BoundaryViolation",
    "HumanGate",
    "OutputBoundary",
    "Refusal",
]
