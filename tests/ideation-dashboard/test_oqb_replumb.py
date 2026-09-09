"""OQ-B's pre-carve re-plumb, kept re-plumbed.

Two edges made openxFactory's OWN retained adapter column import openDox, which
RULING OQ-2 forbids after the carve (openDox is pinned ONLY by openXdox) and
`split-opendox-two-layer-product` § 5.1 (RULING F) forbids one level up
(openxFactory pins the openXdox assembly root and nothing else). Brett Heap
ruled on `#656` (2026-09-09, "rule all OQs as recommended") that each is
re-plumbed BEFORE the carve rather than filed as an edit class:

  * **B-1** `human_seen.py:46` `from .workbench import slug` — `slug` is neutral
    text machinery and moved to `scripts/path_slug.py`, beside the neutral write
    guard, where every column may import it.
  * **B-3** `intent_apply_lane.py:472` `branch_session.bootstrap_sessions` —
    openxFactory's lane reaches sessions THROUGH openXdox, which already imports
    `branch_session` in its own right; `openxdox_surface.py` is that reach given
    a name.

WHY A TEST AND NOT A NOTE. Both re-plumbings are one import line each. Either
is undone by a single "just import it directly" edit that no other test would
notice — the behaviour is identical by construction, so nothing goes red. The
edge is the property, and an edge is only kept by something that measures it.

PARSED, NOT GREPPED, and this file needs a scanner `tests/import_scan.py` does
NOT provide: that module's `imported_modules` deliberately SKIPS relative
imports, because it exists to police a direction between top-level PACKAGES,
where a relative import can never reach. Here the forbidden direction runs
BETWEEN SIBLINGS OF ONE PACKAGE — `from .workbench import slug` is the exact
edge B-1 removed — so the scan below resolves all three spellings the package
uses: `from .X import`, `from . import X`, and the absolute
`ideation_dashboard.X` / `scripts.ideation_dashboard.X` pair (`scripts/__init__.py`
exists, so both absolute spellings resolve and a one-spelling scan is a hole).
"""

from __future__ import annotations

import ast

from conftest import REPO_ROOT

import path_slug
from ideation_dashboard import branch_session, human_seen, openxdox_surface, workbench

PACKAGE = REPO_ROOT / "scripts" / "ideation_dashboard"

# Every openDox-column module the adapter must not reach directly (design D3's
# three-column assignment; these three are the ones OQ-B and memo § 3.6 name).
OPENDOX_SESSION_MODULES = ("branch_session", "session_git", "workbench")

_ABSOLUTE_ROOTS = ("ideation_dashboard", "scripts.ideation_dashboard")


def sibling_imports(tree):
    """Every SIBLING module of `ideation_dashboard` a parsed file imports, with
    the line it does it on.

    Takes a TREE rather than a path so the negative control at the bottom can
    feed the identical scanner a restored-edge source string instead of writing
    a file into the package this test polices. Walks the whole tree, so a lazy
    function-local import is reported exactly like a module-level one:
    `intent_apply_lane`'s reach WAS function-local, and a lazy import is still
    an import and still the edge the carve cannot cross.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level == 1:
                if node.module:                      # from .X import a
                    yield node.module.split(".")[0], node.lineno
                else:                                # from . import X, Y
                    for alias in node.names:
                        yield alias.name, node.lineno
            elif node.level == 0 and node.module:
                for root in _ABSOLUTE_ROOTS:
                    if node.module == root:          # from ideation_dashboard import X
                        for alias in node.names:
                            yield alias.name, node.lineno
                        break
                    if node.module.startswith(root + "."):
                        yield node.module[len(root) + 1:].split(".")[0], node.lineno
                        break
        elif isinstance(node, ast.Import):
            for alias in node.names:
                for root in _ABSOLUTE_ROOTS:
                    if alias.name.startswith(root + "."):  # import ideation_dashboard.X
                        yield alias.name[len(root) + 1:].split(".")[0], node.lineno
                        break


def sibling_imports_of(name: str):
    """`sibling_imports` over one module of the package, by module name."""
    path = PACKAGE / f"{name}.py"
    return sibling_imports(ast.parse(path.read_text(encoding="utf-8"),
                                     filename=str(path)))


def _reaches(name: str, forbidden=OPENDOX_SESSION_MODULES):
    return [f"{name}.py:{line} imports .{module}"
            for module, line in sibling_imports_of(name) if module in forbidden]


# --------------------------------------------------------------------------
# B-1 — the neutral slug
# --------------------------------------------------------------------------

def test_the_adapter_reaches_the_slug_at_its_neutral_home():
    """`human_seen` is openxFactory's own engineering adapter and STAYS (design
    D3); `workbench` is openDox. The import that used to cross that line is
    gone, and nothing else in the file crosses it either."""
    assert _reaches("human_seen") == [], (
        "openxFactory's cross-reference adapter must not import openDox: "
        "`slug` lives at `scripts/path_slug.py` now (OQ-B B-1, `#656` "
        "2026-09-09). Offending imports: " + str(_reaches("human_seen")))


def test_the_slug_is_ONE_object_at_every_import_path():
    """A relocation, not a fork. Every caller — the adapter that imports the
    neutral module, and the openDox module that re-exports it for the readers
    that have always said `workbench.slug` — gets the SAME function, so no
    behaviour, identity or bound can drift between the two paths.

    The two constants matter as much as the function: `lens-model.js` pins its
    own copy of the bound against `workbench.MAX_SLUG_CHARS` by name, and
    `test_lens.py::test_js_and_python_persistence_constants_agree` compares the
    two derivations output-for-output."""
    assert workbench.slug is path_slug.slug
    assert human_seen.slug is path_slug.slug
    assert workbench.MAX_SLUG_CHARS is path_slug.MAX_SLUG_CHARS
    assert workbench._SLUG_KEY_SEPARATOR is path_slug._SLUG_KEY_SEPARATOR
    assert workbench._SLUG_KEY_DIGEST_CHARS is path_slug._SLUG_KEY_DIGEST_CHARS
    assert workbench._slug_key_digest is path_slug._slug_key_digest


def test_the_relocated_slug_behaves_exactly_as_it_did():
    """The four behaviours the moved text promises, pinned at the new home:
    a slug under the bound is UNCHANGED (every existing set keeps its path), a
    degenerate name is `untitled`, a long name is truncated AND keyed, and the
    result never exceeds the bound."""
    assert path_slug.slug("Lens Recipe Set!!") == "lens-recipe-set"
    assert path_slug.slug("   ") == "untitled"
    long_name = "lens " + " ".join(f"keyword{n}" for n in range(40))
    keyed = path_slug.slug(long_name)
    assert len(keyed) == path_slug.MAX_SLUG_CHARS
    assert path_slug._SLUG_KEY_SEPARATOR in keyed
    assert keyed != path_slug.slug(long_name + " and-one-more")


# --------------------------------------------------------------------------
# B-3 — the openXdox surface
# --------------------------------------------------------------------------

def test_the_lane_reaches_sessions_only_through_the_openxdox_surface():
    """`intent_apply_lane` is one of the three lanes design D3 keeps in
    openxFactory; `branch_session` (5,290 lines) is openDox. The lane rehydrates
    live sessions through openXdox, which already imports `branch_session` in
    its own right — so the edge that remains is `oXd -> oD`, which the carve
    permits, instead of `stays -> oD`, which it does not."""
    assert _reaches("intent_apply_lane") == [], (
        "openxFactory's apply lane must not import openDox directly (OQ-B B-3, "
        "`#656` 2026-09-09): sessions are reached through "
        "`ideation_dashboard.openxdox_surface`. Offending imports: "
        + str(_reaches("intent_apply_lane")))
    # Non-vacuity: the reach still EXISTS, it just goes the lawful way. A lane
    # that had simply stopped rehydrating sessions would also pass the above.
    reached = [m for m, _ in sibling_imports_of("intent_apply_lane")]
    assert "openxdox_surface" in reached, reached


def test_the_surface_re_exports_the_same_object():
    """A named re-export, not a wrapper: the surface hands back the function
    `branch_session` defines, so signature, behaviour and identity are the
    module's own and there is no second implementation to keep in step."""
    assert openxdox_surface.bootstrap_sessions is branch_session.bootstrap_sessions


def test_the_surface_stays_a_named_re_export_and_does_not_become_a_facade():
    """The module's own claim, kept: a name is added when a stays-column caller
    is ruled to reach it through openXdox, one line plus its reason. A facade
    that grew its own functions would be openXdox re-publishing openDox's API,
    which pinning the assembly root already does properly (§ 5.1, RULING F)."""
    source = (PACKAGE / "openxdox_surface.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    defined = [node.name for node in tree.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                    ast.ClassDef))]
    assert defined == [], f"the surface defines its own {defined} — re-export only"
    assert openxdox_surface.__all__ == ["bootstrap_sessions"]


# --------------------------------------------------------------------------
# the negative control
# --------------------------------------------------------------------------

def test_the_scan_would_catch_every_spelling_of_the_import_it_removed():
    """Both assertions above are proofs of ABSENCE, so the scanner has to be
    shown catching the thing it is meant to catch — through the SAME function,
    not a second copy of it, which is how a scanner drifts into passing over a
    restored edge.

    All five spellings the package actually uses: the two relative forms, the
    two absolute ones `scripts/__init__.py` makes possible, and the
    function-local form `intent_apply_lane` used before B-3."""
    restored = (
        "from .workbench import slug\n"
        "from . import branch_session\n"
        "import ideation_dashboard.session_git\n"
        "from scripts.ideation_dashboard.workbench import slug as s2\n"
        "def rehydrate():\n"
        "    from ideation_dashboard import branch_session as bs\n"
        "    return bs\n"
    )
    caught = sorted(module for module, _line
                    in sibling_imports(ast.parse(restored))
                    if module in OPENDOX_SESSION_MODULES)
    assert caught == ["branch_session", "branch_session", "session_git",
                      "workbench", "workbench"], caught

    # Non-vacuity for the two live scans: they must be looking at real files
    # with real import statements in them, so a scan over a missing, empty or
    # unparseable file cannot pass as a proof of absence.
    #
    # Deliberately NOT "at least one SIBLING import" (Copilot round 1). That
    # would be a check coupled to an import this arc is already scheduled to
    # remove: `human_seen.py`'s remaining sibling reach is `.boundary`, the
    # 62-line re-export memo § 2.3 files as *already solved* — repoint it at
    # the neutral `output_boundary` and the file legitimately imports no
    # sibling at all, while the two assertions above go on proving exactly
    # what they were written to prove. A non-vacuity guard that fails on the
    # very edit the packet exists to make is a guard that will be deleted.
    for name in ("human_seen", "intent_apply_lane"):
        path = PACKAGE / f"{name}.py"
        assert path.is_file()
        statements = [node for node in ast.walk(
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path)))
            if isinstance(node, (ast.Import, ast.ImportFrom))]
        assert statements, (
            f"{name}.py parses to no import statement at all — the scan lost "
            f"its subject; check the path before trusting the assertions above")
