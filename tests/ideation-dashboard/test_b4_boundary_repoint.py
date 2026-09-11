"""B-4's repoint, kept repointed: the adapter column reads the neutral write
guard directly, not through the openDox re-export shim.

`scripts/ideation_dashboard/boundary.py` is a 62-line RE-EXPORT of
`scripts/output_boundary.py` — the guard moved out of the package at
`split-opendox-two-layer-product` § 2.1 (design D2, PR #724) and the shim was
kept so the roughly forty existing `ideation_dashboard.boundary` readers did
not all have to be rewritten inside that change. The shim's column is openDox
(design D3; memo `carve-3-1` § 2.2 files `boundary` 62 as `oD` / `IR`), so
three modules of openxFactory's OWN retained adapter column reaching it were
three `stays -> oD` edges that RULING OQ-2 forbids after the carve, and one
more ran out of the test tree.

Brett Heap ruled on `#656` (2026-09-09, verbatim "rule B-4 a"): they are
repointed at `output_boundary` PRE-CARVE, one import line each, and the shim
stays for its openDox-side readers.

  * `human_seen.py:45`             `from output_boundary import OutputBoundary`
  * `dashboard_refresh_lane.py:121`                    "        (# noqa: E402)
  * `nightly_lane.py:89`                               "        (# noqa: E402)
  * `tests/notebooklm/test_workbench_sweep_wiring.py:97`  (function-local)

WHY A TEST AND NOT A NOTE — the same reason `test_oqb_replumb.py` gives for
B-1 and B-3. Each repoint is one import line whose behaviour is identical by
construction: the shim re-exports the SAME objects, so a "just import it from
`.boundary` like everything else does" edit restores the edge and nothing else
in the suite goes red. The edge is the property, and an edge is only kept by
something that measures it.

PARSED, NOT GREPPED, and the scan resolves all five spellings the tree can
reach the shim by — the two relative forms available inside the package, the
two absolute ones `scripts/__init__.py` makes possible (`ideation_dashboard.X`
and `scripts.ideation_dashboard.X`), and `import ...` — walking the whole tree
so a function-local import is reported exactly like a module-level one. The
sweep-wiring reach WAS function-local, and a lazy import is still an import
and still the edge the carve cannot cross.

Deliberately a NEW file: `test_import_direction.py` polices the direction
between the two top-level packages and `test_oqb_replumb.py` polices OQ-B's
own two re-plumbings, and neither is this one.
"""

from __future__ import annotations

import ast

from conftest import REPO_ROOT

import output_boundary
from ideation_dashboard import boundary as boundary_shim
from ideation_dashboard import dashboard_refresh_lane, human_seen, nightly_lane

PACKAGE = REPO_ROOT / "scripts" / "ideation_dashboard"
SHIM = PACKAGE / "boundary.py"

# The four files RULING B-4 (a) repoints, by path — three in the adapter
# column plus the one in the test tree.
RULED_FILES = (
    PACKAGE / "human_seen.py",
    PACKAGE / "dashboard_refresh_lane.py",
    PACKAGE / "nightly_lane.py",
    REPO_ROOT / "tests" / "notebooklm" / "test_workbench_sweep_wiring.py",
)

_ABSOLUTE_ROOTS = ("ideation_dashboard", "scripts.ideation_dashboard")


def boundary_imports(tree):
    """Every reach of the `ideation_dashboard.boundary` shim a parsed file
    makes, as `(spelling, lineno)`.

    Takes a TREE rather than a path so the negative control at the bottom can
    feed the identical scanner a restored-edge source STRING, instead of
    writing a file into the package this test polices.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level:                                    # relative
                if node.module:
                    if node.module.split(".")[0] == "boundary":
                        yield "from .boundary import ...", node.lineno
                else:
                    for alias in node.names:                  # from . import boundary
                        if alias.name == "boundary":
                            yield "from . import boundary", node.lineno
                continue
            if not node.module:
                continue
            for root in _ABSOLUTE_ROOTS:
                if node.module == f"{root}.boundary":
                    yield f"from {root}.boundary import ...", node.lineno
                    break
                if node.module == root:                       # from <root> import boundary
                    for alias in node.names:
                        if alias.name == "boundary":
                            yield f"from {root} import boundary", node.lineno
                    break
        elif isinstance(node, ast.Import):
            for alias in node.names:
                for root in _ABSOLUTE_ROOTS:
                    if alias.name == f"{root}.boundary":
                        yield f"import {root}.boundary", node.lineno
                        break


def _reaches(path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    return [f"{path.relative_to(REPO_ROOT).as_posix()}:{line} {spelling}"
            for spelling, line in boundary_imports(tree)]


# --------------------------------------------------------------------------
# the repoint
# --------------------------------------------------------------------------

def test_the_four_ruled_files_reach_the_guard_at_its_neutral_home():
    """None of the four names the shim, in any spelling, at any nesting.

    The three modules are openxFactory's own engineering adapter and STAY
    (design D3's third column, RULING DQ-1); `boundary` is openDox. The fourth
    is the test-tree reach the same ruling covers."""
    offenders = [edge for path in RULED_FILES for edge in _reaches(path)]
    assert offenders == [], (
        "RULING B-4 (a) (`#656`, 2026-09-09) repointed these at the neutral "
        "`scripts/output_boundary.py`; the `boundary` re-export shim is "
        "openDox and the adapter column must not reach it. Offending "
        f"imports: {offenders}")


def test_each_repointed_name_is_the_neutral_guards_own_object():
    """A repoint, not a fork. Every module binds the SAME class object the
    neutral module defines, so `isinstance` checks and
    `except BoundaryViolation` handlers behave exactly as they did.

    `OutputBoundary` is a class, never interned, so `is` here is real evidence
    (the trap `test_oqb_replumb.py` documents for interned ints and strings
    does not apply)."""
    assert human_seen.OutputBoundary is output_boundary.OutputBoundary
    assert dashboard_refresh_lane.OutputBoundary is output_boundary.OutputBoundary
    assert nightly_lane.OutputBoundary is output_boundary.OutputBoundary


def test_the_repoint_is_a_no_op_because_the_shim_re_exports_the_same_object():
    """WHY the repoint could be mechanical: the shim never made a copy. Every
    name it re-exports is the neutral module's own object, so the four callers
    were already using `output_boundary`'s guard and only the import path
    changed. If this ever stopped holding, B-4 would have been a behaviour
    change and the three edges would need a different answer."""
    for name in boundary_shim.__all__:
        assert getattr(boundary_shim, name) is getattr(output_boundary, name), (
            f"the shim's {name} is not `output_boundary`'s own object — B-4 "
            "assumed a pure re-export")


def test_the_sweep_wiring_test_names_the_neutral_module_where_it_used_to_name_the_shim():
    """Non-vacuity for the fourth file. It has no module-level binding to
    compare identities on — its import is function-local inside
    `_live_manifest` — so the proof of absence above is paired with a proof
    that the reach still EXISTS and goes to the neutral home. A file that had
    simply stopped constructing a boundary would also pass the scan."""
    path = REPO_ROOT / "tests" / "notebooklm" / "test_workbench_sweep_wiring.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    reaches = [node.lineno for node in ast.walk(tree)
               if isinstance(node, ast.ImportFrom)
               and not node.level and node.module == "output_boundary"
               and any(a.name == "OutputBoundary" for a in node.names)]
    assert reaches, (
        "the sweep-wiring test must import `OutputBoundary` from "
        "`output_boundary`; it imports it from nowhere at all")


def test_the_shim_stays_for_its_opendox_readers():
    """What B-4 deliberately did NOT do. The shim is kept — memo § 2.2 files
    it as an openDox module carried at the carve with an `import rewrites`
    edit, and the openDox-column and test-tree readers that name it are none
    of this change's business. A later edit that deletes `boundary.py` because
    "nothing needs it" has to fail here first."""
    assert SHIM.is_file(), "scripts/ideation_dashboard/boundary.py was removed"
    readers = [p for p in sorted(PACKAGE.glob("*.py"))
               if p != SHIM and _reaches(p)]
    assert readers, (
        "no module in the package reaches the shim any more — if that is "
        "true the shim should be retired by its own change, not left "
        "unreferenced")


# --------------------------------------------------------------------------
# the negative control
# --------------------------------------------------------------------------

def test_the_scan_would_catch_every_spelling_of_the_import_it_removed():
    """The assertion above is a proof of ABSENCE, so the scanner has to be
    shown catching the thing it is meant to catch — through the SAME function,
    not a second copy of it, which is how a scanner drifts into passing over a
    restored edge.

    All five spellings, including the function-local form the sweep-wiring
    test actually used, and the `scripts.` prefixed absolute one that
    `scripts/__init__.py` makes resolvable."""
    restored = (
        "from .boundary import OutputBoundary\n"
        "from . import boundary\n"
        "import ideation_dashboard.boundary\n"
        "from scripts.ideation_dashboard.boundary import HumanGate\n"
        "from ideation_dashboard import boundary as b\n"
        "def make(root):\n"
        "    from ideation_dashboard.boundary import OutputBoundary as OB\n"
        "    return OB(root, [])\n"
    )
    caught = sorted(spelling for spelling, _line
                    in boundary_imports(ast.parse(restored)))
    assert caught == [
        "from . import boundary",
        "from .boundary import ...",
        "from ideation_dashboard import boundary",
        "from ideation_dashboard.boundary import ...",
        "from scripts.ideation_dashboard.boundary import ...",
        "import ideation_dashboard.boundary",
    ], caught

    # And nothing that merely mentions the word is caught: the scan must not
    # go off on the neutral import the repoint installed, or on a local
    # variable called `boundary_root` (the sweep-wiring test has one).
    clean = (
        "from output_boundary import OutputBoundary\n"
        "boundary_root = repo\n"
        "from doc_health import boundary_notes\n"
    )
    assert list(boundary_imports(ast.parse(clean))) == []

    # Non-vacuity for the live scans: they must be looking at real files with
    # real import statements in them, so a scan over a missing, empty or
    # renamed file cannot pass as a proof of absence.
    for path in RULED_FILES:
        assert path.is_file(), path
        statements = [node for node in ast.walk(
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path)))
            if isinstance(node, (ast.Import, ast.ImportFrom))]
        assert statements, (
            f"{path} parses to no import statement at all — the scan lost its "
            "subject; check the path before trusting the assertions above")
