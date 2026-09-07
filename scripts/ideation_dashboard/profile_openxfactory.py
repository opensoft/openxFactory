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
# contribute the column belonging to the SAME spelling as the entrypoint
# assembling it — otherwise the verbs `cli.py` registers, or the routes
# `serve.py` registers, are a different column's, bound to a different core
# (see `cli.py`'s note above its own relative import, `cli_gate._core()`, and
# each server column module's own `sys.path` idiom above `build_server`'s lazy
# import of this module).
#
# `cli_gate` is named here too (`relative_sibling_imports` in
# `test_cli_column_split.py` finds it regardless of the statement's nesting),
# but NOT at module scope — see `__getattr__` below for why.
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
#: after it, so a server built the way all 31 in-tree test `build_server(...)`
#: call sites across 27 test files build one — with no `route_extensions` at
#: all — serves exactly the routes it served before the seam existed. See
#: `build_server`'s own note for why the composition is additive rather than a
#: sentinel default.
ROUTE_EXTENSIONS: tuple = (
    serve_gate.GateRoutesExtension(),
    serve_projection.ProjectionRoutesExtension(),
    serve_openxfactory_lanes.LaneRoutesExtension(),
)


def __getattr__(name: str):
    """`SUBCOMMAND_EXTENSIONS` — resolved on first access rather than bound at
    import time (PEP 562).

    THE CATCH-UP MERGE THIS FIXES (§ 2.4 PR 3 of 4 onto PR 4's landed
    `cli_gate.GateSubcommands`). PR 4 (#742) put `SUBCOMMAND_EXTENSIONS` in
    this module as a plain `from . import cli_gate` at the top — harmless
    there, because on `main` nothing but `cli.py` ever imported this module.
    This PR adds `ROUTE_EXTENSIONS`, which `serve.py`'s `build_server` imports
    on EVERY startup, hosted included — and `cli_gate` pulls in
    `authoring` -> `workbench` -> PyYAML, which the hosted image deliberately
    does not carry
    (`test_hosted_posts_do_not_load_notebook_only_dependencies`). A plain
    top-level import here would load `cli_gate`'s whole dependency chain into
    a server process that only ever wanted `ROUTE_EXTENSIONS`, for a name
    (`SUBCOMMAND_EXTENSIONS`) it never reads.

    Resolved on access instead: only `cli.py`'s own read of
    `SUBCOMMAND_EXTENSIONS` pays for `cli_gate`, exactly as `authoring.py`'s
    own `__getattr__` resolves `REQUIRED_HEADER_FIELDS` on access rather than
    at import time, for the same reason (an import graph should not carry a
    dependency that only ONE caller of a shared module actually needs). The
    tuple's shape and every caller's read of it (`cli.py`'s
    `profile_openxfactory.SUBCOMMAND_EXTENSIONS`, the `len(...) == 1` and
    `isinstance(...[0], cli_gate.GateSubcommands)` pins in
    `test_cli_column_split.py`) are unchanged — this only moves WHEN the
    import happens, never what it returns.

    `cli_gate` itself is answered here too, and for the same identity reason
    a plain `from . import cli_gate` would have satisfied for free:
    `test_a_library_caller_gets_the_columns_of_its_own_core` asserts
    `profile.cli_gate is gate` — the profile's own reference to the column
    must be the SAME module object a sibling import of `cli_gate` under the
    same package spelling produces, not a second one. A relative import
    always resolves through `sys.modules`, so answering it here — on
    first access, from whichever spelling's `profile_openxfactory` is asking —
    gives back that identical singleton exactly as the eager import did.
    """
    if name == "SUBCOMMAND_EXTENSIONS":
        from . import cli_gate
        return (cli_gate.GateSubcommands(),)
    if name == "cli_gate":
        from . import cli_gate
        return cli_gate
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
