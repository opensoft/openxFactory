"""THE SCOPE SPLIT: the direction it removed, and the surface it kept
(`split-opendox-two-layer-product` § 3.1, pre-carve split S-1).

`doxbench_scope.py` held two columns' worth of code. The five FROZEN types
(`ScopeConfinementError`, `ScopeKey`, `ScopeDocument`, `ScopeSection`,
`ScopeProjection`) are openDox; the ownership authority that produces them —
`resolve_scope`, the registry-root confinement, the editable classification —
is openXdox. § 3.1's carve manifest files every path under exactly ONE
disposition, so a file whose halves go to two repositories cannot be filed at
all; the types moved to `doxbench_scope_types.py` so that the carve is a pure
per-file move.

WHAT THIS FILE KEEPS TRUE, and why each half needs saying:

  1. **THE DIRECTION.** Three openDox modules — `doxbench_packet`,
     `doxbench_telemetry`, `doxbench_turns` — imported the types alone out of
     the openXdox module. That is openDox reaching UP into openXdox, which the
     one-chain ruling (`design.md` D3a, RULING OQ-2) forbids across the carve:
     openXdox pins openDox, never the reverse. The three now import
     `doxbench_scope_types`, and the remaining edge runs openXdox → openDox,
     which is lawful. Reintroducing `from ideation_dashboard.doxbench_scope
     import ScopeKey` in any of the three would restore the unlawful direction
     while every behavioural test stayed green, so it is asserted rather than
     noted.

  2. **THE SURFACE.** `doxbench_scope` re-exports all six names, which is what
     lets forty-odd landed test modules and `serve_workbench`'s four lazy
     imports keep working unchanged. A re-export that COPIED instead of
     re-binding would pass an equality test and fail `isinstance` and
     `except ScopeConfinementError` in production, so identity is what is
     asserted — `is`, not `==`.

  3. **THE BOTTOM OF THE GRAPH.** `doxbench_scope_types` imports nothing from
     this package. It is where `SCOPE_KINDS` now lives (`ScopeKey.__post_init__`
     validates against it, so the tuple is the frozen type's own value domain);
     an import back into `doxbench_scope` would be a cycle AND would put the
     removed edge back by another route.

PARSED, NOT GREPPED, and with a scanner of this file's own rather than
`tests/import_scan.py`'s. That helper deliberately SKIPS relative imports —
correct for its own question, which is about other top-level packages, and
wrong for this one: `from .doxbench_scope import ScopeKey` is exactly the edge
this file exists to catch, and it names no top-level package at all. All four
spellings the package admits are read: absolute `from ideation_dashboard.X
import`, `from scripts.ideation_dashboard.X import`, `from ideation_dashboard
import X`, and relative `from . import X` / `from .X import`.
"""

from __future__ import annotations

import ast

import pytest

from conftest import REPO_ROOT

from ideation_dashboard import doxbench_scope, doxbench_scope_types

PACKAGE = REPO_ROOT / "scripts" / "ideation_dashboard"

#: The openDox modules whose repoint IS split S-1. Each must import the types
#: module and must not name the authority module.
REPOINTED = ("doxbench_packet", "doxbench_telemetry", "doxbench_turns")

#: Every name `doxbench_scope` re-exports, and the whole of what moved.
MOVED_NAMES = (
    "SCOPE_KINDS", "ScopeConfinementError", "ScopeKey", "ScopeDocument",
    "ScopeSection", "ScopeProjection",
)


def _module(name, lineno):
    """One edge, kept only when `name` is a MODULE of this package rather than
    a name re-exported from `__init__` (`from . import GENERATOR_VERSION`)."""
    if (PACKAGE / f"{name}.py").is_file():
        yield name, lineno


def _sibling_modules(path):
    """Every module of THIS package `path` imports, with the line it does it on.

    Covers the FIVE spellings a module in this package can use, and the fifth
    is the one a scanner forgets: `from . import doxbench_scope` parses as an
    `ImportFrom` with `level=1` and `module=None`, so a helper that reads
    `node.module` sees nothing at all. It is not a hypothetical spelling — the
    package uses it forty times (`gate_routes.py:70`, `kickoff.py:61`,
    `doxbench_scope.py:730` and the rest), and missing it would have let the
    exact back-edge these tests exist to prevent walk straight past them
    (Copilot review of PR #837).

    A name in a comment, a docstring or a string literal is not an import and
    is not reported — `doxbench_scope.py` is named in prose by several modules
    that must keep naming it. `from pkg import X` and `from . import X` can
    also name a NAME rather than a module (`generator.py:70` imports
    `GENERATOR_VERSION` that way), so a yielded name is kept only when a
    sibling module of that name actually exists.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level:
                if module:                                  # from .X import a
                    yield from _module(module.split(".")[0], node.lineno)
                else:
                    for alias in node.names:                # from . import X
                        yield from _module(alias.name, node.lineno)
            elif module in ("ideation_dashboard", "scripts.ideation_dashboard"):
                for alias in node.names:                    # from pkg import X
                    yield from _module(alias.name, node.lineno)
            else:
                for prefix in ("ideation_dashboard.", "scripts.ideation_dashboard."):
                    if module.startswith(prefix):           # from pkg.X import a
                        yield from _module(module[len(prefix):].split(".")[0],
                                           node.lineno)
                        break
        elif isinstance(node, ast.Import):
            for alias in node.names:
                for prefix in ("ideation_dashboard.", "scripts.ideation_dashboard."):
                    if alias.name.startswith(prefix):       # import pkg.X
                        yield from _module(alias.name[len(prefix):].split(".")[0],
                                           node.lineno)
                        break


@pytest.mark.parametrize("module", REPOINTED)
def test_openDox_readers_import_the_types_and_not_the_authority(module):
    """The removed edge stays removed, and the assertion is not vacuous."""
    edges = list(_sibling_modules(PACKAGE / f"{module}.py"))
    named = {target: line for target, line in edges}
    assert "doxbench_scope_types" in named, (
        f"{module}.py no longer imports doxbench_scope_types — this test has "
        f"lost its subject rather than passed")
    offenders = [line for target, line in edges if target == "doxbench_scope"]
    assert not offenders, (
        f"{module}.py is openDox and imports the openXdox ownership authority "
        f"at line(s) {offenders}; import the types from doxbench_scope_types")


def test_types_module_is_the_bottom_of_the_scope_graph():
    """No back-edge, by any of the four spellings — cycle and edge at once."""
    edges = list(_sibling_modules(PACKAGE / "doxbench_scope_types.py"))
    assert not edges, (
        f"doxbench_scope_types imports {edges} from its own package; it must "
        f"import nothing from it, doxbench_scope least of all")


def test_doxbench_scope_re_exports_the_same_objects():
    """`is`, not `==`: a copy would pass equality and break `isinstance`."""
    for name in MOVED_NAMES:
        assert getattr(doxbench_scope, name) is getattr(doxbench_scope_types, name), (
            f"doxbench_scope.{name} is not doxbench_scope_types.{name}")


def test_scope_kinds_is_the_key_validation_domain():
    """`SCOPE_KINDS` moved WITH `ScopeKey` because it is that type's own value
    domain — proven by the refusal, so the move cannot be undone by copying the
    tuple back and leaving the validator reading a stale one."""
    for kind in doxbench_scope_types.SCOPE_KINDS:
        assert doxbench_scope.ScopeKey(
            repository="r", ref="main", tile_kind=kind, tile_id="t").tile_kind == kind
    with pytest.raises(ValueError, match="tile_kind must be one of"):
        doxbench_scope.ScopeKey(
            repository="r", ref="main", tile_kind="not-a-kind", tile_id="t")
