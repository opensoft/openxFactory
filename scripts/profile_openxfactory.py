"""WHAT THIS ASSEMBLY IS BUILT WITH: openxFactory's composition point, POST-SHED
(`split-opendox-two-layer-product` § 2.4; § 4.3, RULED ASK-2 option (2),
`#656` comment `5628886636`).

THE FILE THIS REPLACES AND WHY IT IS NOT THE SAME FILE.
`scripts/ideation_dashboard/profile_openxfactory.py` is the carve manifest's
single `deleted_at_carve` row: the § 3 carve deleted it rather than moving it,
because a composition point is not a thing a core or a consumer can own — it
names the contributions THIS assembly's entrypoints are built with, and after
the carve openDox's core names no profile and openXdox declares its own. The
§ 5.2 shed removed that path with the other 318. This module is openxFactory's
composition point AFTER the shed, at a path OUTSIDE the carve surface
(`moved_paths:` covers `scripts/ideation_dashboard/`, not `scripts/`), carrying
the same two tuples re-spelled for the two pinned legs.

WHY THE SPELLINGS CHANGED AND THE RELATIVE IMPORTS DID NOT SURVIVE. The deleted
module imported its three route columns RELATIVELY (`from . import serve_gate`)
for one reason, recorded in its own docstring: `scripts/__init__.py` made the
old tree importable under TWO package spellings (`ideation_dashboard.X` and
`scripts.ideation_dashboard.X`), which are two different module objects, and a
profile had to contribute the column belonging to the SAME spelling as the
entrypoint assembling it. After the shed each column has exactly ONE importable
spelling — `openxdox.serve_gate`, `openxdox.serve_projection`,
`openxdox.cli_gate` at the pinned openXdox leg and
`ideation_dashboard.serve_openxfactory_lanes` here — so the ambiguity the
relative import existed to close no longer exists, and absolute imports say
plainly which leg each column comes from. The identity property that rested on
it still holds and is still asserted (`profile.cli_gate is gate` in
`test_cli_column_split.py`): an absolute import resolves through `sys.modules`
exactly as a relative one does.

`SUBCOMMAND_EXTENSIONS` IS STILL RESOLVED ON ACCESS, for the reason the deleted
module gave and that the shed did not change: `cli_gate` reaches `authoring` ->
`workbench` -> PyYAML, which the hosted image deliberately does not carry
(`test_hosted_posts_do_not_load_notebook_only_dependencies`), while
`ROUTE_EXTENSIONS` is read by `build_server` on EVERY startup, hosted included.
A plain module-scope import of `cli_gate` here would put the CLI column's whole
dependency chain into a server process that only ever wanted the route table.
PEP 562 holds it out; only `cli.py`'s own read of `SUBCOMMAND_EXTENSIONS` pays.

HOW THE CONSUMERS REACH IT — AND WHAT IS STILL OWED. `opendox.serve.build_server`
(`serve.py:1377`) and `opendox.cli.build_parser` (`cli.py:915`) still name
`profile_openxfactory` as a BARE GLOBAL with no import anywhere, which is the
§ 4.3 hole RULING ASK-2 answers: option (2), a LAZY PROXY in openDox-code that
resolves the profile at first attribute access, with openxFactory REGISTERING
THE REAL MODULE AT PROCESS START. This file is that real module. The proxy is
openDox-code's half and is NOT YET BUILT, so the registration is performed here
by `carved_reach.bind_composition_point()`, which binds this module into each
consumer's namespace as that consumer loads. When the proxy lands, that binding
collapses into the one `register()` call the ruling describes and this module
stops moving. § 4.3's box stays OPEN either way: nothing in this file is the
proxy, and PR-2 ticks no § 4 box.
"""

from __future__ import annotations

# ABSOLUTE, and from the leg each column actually lives at now — see the module
# docstring for why the deleted file's relative imports were the right answer to
# a question the shed removed. The openXdox spellings resolve through the pinned
# `openXdox/code/src` that `carved_reach.install()` puts on the path; the lane
# column is openxFactory's own `stays_openxfactory_adapter` row and stays here.
from ideation_dashboard import serve_openxfactory_lanes
from openxdox import serve_gate
from openxdox import serve_projection

#: The route contributions this assembly's SERVER carries, in the order
#: `collect_bindings` consults them — which is observable, so the tuple is a
#: declaration and not an incidental ordering.
#:
#: Three members, unchanged by the shed: openXdox's gate console and its
#: projection/snapshot routes, and openxFactory's own lane routes (RULING DQ-1 —
#: the column that stays with the adapter reaches the seam the same way the
#: column that leaves does).
#:
#: `build_server` registers THIS tuple first and the caller's `route_extensions`
#: after it, so a server built with no `route_extensions` at all serves exactly
#: the routes it served before the seam existed.
ROUTE_EXTENSIONS: tuple = (
    serve_gate.GateRoutesExtension(),
    serve_projection.ProjectionRoutesExtension(),
    serve_openxfactory_lanes.LaneRoutesExtension(),
)


def __getattr__(name: str):
    """`SUBCOMMAND_EXTENSIONS` and `cli_gate` — resolved on first access rather
    than bound at import time (PEP 562).

    Carried across the shed verbatim in behaviour: the tuple's shape and every
    caller's read of it (`cli.py`'s `profile_openxfactory.SUBCOMMAND_EXTENSIONS`,
    the `len(...) == 1` and `isinstance(...[0], cli_gate.GateSubcommands)` pins
    in `test_cli_column_split.py`) are what they were. Only WHEN the import
    happens is held back, never what it returns.

    `cli_gate` is answered here too, for the identity reason a module-scope
    import would have satisfied for free:
    `test_a_library_caller_gets_the_columns_of_its_own_core` asserts
    `profile.cli_gate is gate` — this module's reference to the column must be
    the SAME module object a sibling import of `openxdox.cli_gate` produces, not
    a second one. Any import resolves through `sys.modules`, so answering it on
    first access gives back that identical singleton.
    """
    if name == "SUBCOMMAND_EXTENSIONS":
        from openxdox import cli_gate
        return (cli_gate.GateSubcommands(),)
    if name == "cli_gate":
        from openxdox import cli_gate
        return cli_gate
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
