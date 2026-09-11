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

from carved_reach import source as carved_source

import path_slug
from ideation_dashboard import human_seen
from opendox import branch_session, workbench
from opendox import path_slug as leg_path_slug
from openxdox import openxdox_surface


def package_source(name: str):
    """`scripts/ideation_dashboard/<name>.py`, wherever the § 5.2 shed left it.

    The modules this test reads sit on BOTH sides of the carve now —
    `human_seen.py`, `intent_apply_lane.py` stayed, `workbench.py` went to
    openDox-code, `openxdox_surface.py` to openXdox-code — so the package
    prefix that used to answer for all four cannot (RULED (a), `#656`
    `5625573095`; Copilot `PRRT_kwDOTAvnrs6hUpv1`). `carved_reach.source()`
    answers each from its own manifest row, which is also what keeps this
    test's own reporting spelling the pre-shed path every reader recognises.
    """
    return carved_source(f"scripts/ideation_dashboard/{name}.py")


# Every openDox-column module the adapter must not reach directly (design D3's
# three-column assignment; these three are the ones OQ-B and memo § 3.6 name).
OPENDOX_SESSION_MODULES = ("branch_session", "session_git", "workbench")

# The two DESTINATION package roots join the two pre-shed ones rather than
# replacing them (Copilot `PRRT_kwDOTAvnrs6hVaMK`). After the shed the lawful
# reach is spelled `from openxdox.openxdox_surface import ...` and the
# forbidden one would be spelled `from opendox import branch_session`; a
# scanner left at the old roots would see NEITHER — it would report the
# positive B-3 assertion as failed (an empty set where `openxdox_surface` must
# appear) while a restored direct edge to openDox passed unnoticed. Both
# spellings of the pre-shed package stay: `scripts/__init__.py` still exists
# and the negative control still feeds all of them through this scanner.
_ABSOLUTE_ROOTS = ("ideation_dashboard", "scripts.ideation_dashboard",
                   "opendox", "openxdox")


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
    path = package_source(name)
    return sibling_imports(ast.parse(path.read_text(encoding="utf-8"),
                                     filename=str(path)))


def _reaches(name: str, forbidden=OPENDOX_SESSION_MODULES):
    return [f"{name}.py:{line} imports .{module}"
            for module, line in sibling_imports_of(name) if module in forbidden]


_SLUG_FAMILY_NAMES = ("MAX_SLUG_CHARS", "_SLUG_KEY_SEPARATOR",
                      "_SLUG_KEY_DIGEST_CHARS", "_slug_key_digest", "slug")


def _own_bindings(source: str, names, *, filename="<scratch>"):
    """Every name in `names` that the parsed `source` BINDS itself — an
    `Assign`/`AnnAssign` target, or a `FunctionDef`/`AsyncFunctionDef`/
    `ClassDef` name — anywhere in the module. Walks the whole tree rather
    than reading `tree.body` alone, so a binding nested inside a function or
    a conditional is not missed either.

    Deliberately excludes `ImportFrom`: importing a name IS the re-export
    this guard exists to prove, so the question this asks is narrower — does
    the module ALSO define the name itself, which an `is` comparison on an
    interned int or string cannot answer (Copilot round 2, 2026-09-09, on an
    earlier revision's `:126-128` — see the test below)."""
    tree = ast.parse(source, filename=filename)
    bound = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in names:
                bound.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    bound.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id in names:
                bound.add(node.target.id)
    return bound


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
    two derivations output-for-output.

    NOTE the three constant checks below are necessary but not sufficient:
    `200`, `"-k"` and `16` are interned by CPython, so `is` on them would
    pass just the same if `workbench.py` DEFINED its own copies with those
    values instead of importing them (Copilot round 2, 2026-09-09). The two
    function-object checks stay real evidence — functions are never interned
    — and `test_workbench_source_re_exports_the_slug_family_rather_than_
    redefining_it` below is the assertion that actually closes the gap, at
    the source rather than the value.

    EACH SIDE ASKED OF ITS OWN LEG AFTER THE § 5.2 SHED, and that change is the
    finding rather than a loosening. `scripts/path_slug.py` is a
    `replicated_at_destination` row (RULED OQ-A/OQ-C: a REPLICA, not a module
    shared across a repository boundary with no pin), so post-shed there are
    two byte-identical copies — openxFactory's, which `human_seen` imports, and
    openDox's, which `workbench` re-exports through `from .path_slug import`.
    A cross-leg `is` was true only while they were one file. It is now FALSE
    for `slug` and `_slug_key_digest`, which is what caught this — and would
    have stayed misleadingly TRUE for `200`, `"-k"` and `16`, which is the
    worse half and exactly the interning trap this docstring already warns
    about, one seam further out. "A relocation, not a fork" is therefore
    asserted twice, once per leg; that the two copies are the same TEXT is the
    manifest's claim and `tests/carve_conformance` is where it is enforced."""
    assert workbench.slug is leg_path_slug.slug
    assert human_seen.slug is path_slug.slug
    assert workbench.MAX_SLUG_CHARS is leg_path_slug.MAX_SLUG_CHARS
    assert workbench._SLUG_KEY_SEPARATOR is leg_path_slug._SLUG_KEY_SEPARATOR
    assert workbench._SLUG_KEY_DIGEST_CHARS is leg_path_slug._SLUG_KEY_DIGEST_CHARS
    assert workbench._slug_key_digest is leg_path_slug._slug_key_digest


def test_workbench_source_re_exports_the_slug_family_rather_than_redefining_it():
    """The proof Copilot round 2 actually asked for (suppressed comment,
    2026-09-09, on an earlier revision's `:126-128`): `workbench.X is
    path_slug.X` on the three constants above is not evidence of a
    re-export, because `200`, `"-k"` and `16` are interned by CPython — the
    same assertions would pass just the same if `workbench.py` DEFINED its
    own copies of them instead of importing them. Copilot's own proposed fix
    (value equality) is weaker still: a redefinition with the same value is
    also equal.

    So the family is checked at the SOURCE, not the value: `workbench.py`
    must bind none of the five names by assignment or definition anywhere in
    the module, and the only place any of them appears must be the
    `from path_slug import (...)` at its top."""
    workbench_path = package_source("workbench")
    source = workbench_path.read_text(encoding="utf-8")

    own = _own_bindings(source, _SLUG_FAMILY_NAMES, filename=str(workbench_path))
    assert own == set(), (
        f"workbench.py defines {sorted(own)} itself — it must re-export the "
        "slug family from path_slug, never redefine any of it")

    tree = ast.parse(source, filename=str(workbench_path))
    imported = {
        alias.asname or alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "path_slug"
        for alias in node.names
    }
    assert set(_SLUG_FAMILY_NAMES) <= imported, (
        "workbench.py must import the whole slug family from path_slug; "
        f"missing {sorted(set(_SLUG_FAMILY_NAMES) - imported)}")

    # Non-vacuity (the fix this round exists to make): on a scratch COPY of
    # the source — a string, never the real file — add back exactly
    # Copilot's scenario, `workbench.py` keeping the import but ALSO binding
    # its own `MAX_SLUG_CHARS`, and show the SAME function catches it.
    redefined = source + "\nMAX_SLUG_CHARS = 200\n"
    caught = _own_bindings(redefined, _SLUG_FAMILY_NAMES,
                            filename="<scratch: workbench.py + a redefinition>")
    assert caught == {"MAX_SLUG_CHARS"}, (
        "the non-vacuity control failed to catch a scratch redefinition of "
        f"MAX_SLUG_CHARS: {caught}")


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
    source = package_source("openxdox_surface").read_text(encoding="utf-8")
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

    All five pre-shed spellings the package used — the two relative forms, the
    two absolute ones `scripts/__init__.py` makes possible, and the
    function-local form `intent_apply_lane` used before B-3 — PLUS the two
    POST-SHED ones, which are the only way the forbidden edge could actually be
    spelled today: `from opendox import branch_session` and
    `import opendox.session_git`. A control that stopped at the pre-shed
    spellings would prove the scanner catches an edge nobody can write any
    more, while the one anybody CAN write walked past it."""
    restored = (
        "from .workbench import slug\n"
        "from . import branch_session\n"
        "import ideation_dashboard.session_git\n"
        "from scripts.ideation_dashboard.workbench import slug as s2\n"
        "from opendox import branch_session as direct\n"
        "import opendox.session_git\n"
        "def rehydrate():\n"
        "    from ideation_dashboard import branch_session as bs\n"
        "    return bs\n"
    )
    caught = sorted(module for module, _line
                    in sibling_imports(ast.parse(restored))
                    if module in OPENDOX_SESSION_MODULES)
    assert caught == ["branch_session", "branch_session", "branch_session",
                      "session_git", "session_git",
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
        path = package_source(name)
        assert path.is_file()
        statements = [node for node in ast.walk(
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path)))
            if isinstance(node, (ast.Import, ast.ImportFrom))]
        assert statements, (
            f"{name}.py parses to no import statement at all — the scan lost "
            f"its subject; check the path before trusting the assertions above")
