"""WHAT THIS ASSEMBLY IS BUILT WITH: the in-tree openxFactory profile
(`split-opendox-two-layer-product` § 2.4).

The composition point. `cli.py` and `serve.py` declare the extension POINTS and
know nothing about what fills them; this module names the contributions THIS
repository's entrypoints are assembled with, and it is the one file the § 3
carve deletes rather than moves — after the carve openXdox declares its own
profile and openDox's core has no line naming any.

Deliberately minimal and additive: a tuple per extension point, nothing else. PR
3 of § 2.4 adds `ROUTE_EXTENSIONS` beside `SUBCOMMAND_EXTENSIONS` for the route
point, which is why this is a module of constants and not a class with a
constructor to negotiate.
"""

from __future__ import annotations

# Relative, like the core's own imports of the modules the § 2.4 split created:
# this tree is importable under two package spellings, and the profile must
# contribute the column belonging to the SAME spelling as the core that is
# assembling the parser — otherwise the verbs it registers are a different
# column's, bound to a different core (see `cli.py`'s note above its own
# relative import, and `cli_gate._core()`).
from . import serve_gate
from . import serve_openxfactory_lanes
from . import serve_projection

#: The route contributions this assembly's SERVER carries, in the order
#: `collect_bindings` consults them — which is observable, so the tuple is a
#: declaration and not an incidental ordering.
#:
#: Three members: openXdox's gate console and its projection/snapshot routes,
#: and openxFactory's own lane routes (RULING DQ-1 — the column that stays with
#: the adapter reaches the seam the same way the column that leaves does).
#:
#: `build_server` registers THIS tuple first and the caller's `route_extensions`
#: after it, so a server built the way all 35 in-tree call sites build one — with
#: no `route_extensions` at all — serves exactly the routes it served before the
#: seam existed. See `build_server`'s own note for why the composition is
#: additive rather than a sentinel default.
ROUTE_EXTENSIONS: tuple = (
    serve_gate.GateRoutesExtension(),
    serve_projection.ProjectionRoutesExtension(),
    serve_openxfactory_lanes.LaneRoutesExtension(),
)
