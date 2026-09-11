"""OQ-B B-2's pre-carve re-plumb, kept re-plumbed.

One edge made openxFactory's OWN retained adapter column import openDox, which
RULING OQ-2 forbids after the carve (openDox is pinned ONLY by openXdox) and
`split-opendox-two-layer-product` § 5.1 (RULING F) forbids one level up
(openxFactory pins the openXdox assembly root and nothing else):
`serve_openxfactory_lanes.py:52` read four names out of `serve_wire.py`, the
shared wire vocabulary, which goes WHOLE to openDox under design D3.

Brett Heap ruled it on `#656` (2026-09-09, verbatim "rule B-2 (i')") after the
measurement on PR #848 showed the four names do not take one disposition:

  * **the three fixed wire strings** (`JSON_CTYPE`,
    `JSON_OBJECT_BODY_REQUIRED`, `HOSTED_SESSION_REFUSAL`) are `str` literals,
    so they carry no dependency and are neutral by construction. They took
    `slug`'s B-1 treatment: a neutral module beside the neutral write guard,
    `scripts/wire_messages.py`, `not_moved / replicated_at_destination` at the
    carve (RULED OQ-A/OQ-C). `serve_wire.py` re-exports them, so every openDox
    and openXdox reader keeps resolving them off the old name.
  * **`hosted_ref_refused`** could NOT follow them: its body reaches
    `snapshot_registry.is_publishable_ref`, and `snapshot_registry` is the
    openXdox column, so a module replicated at every destination could not
    resolve it and restating the ref rule would be the second spelling
    `serve_wire.py`'s own import comments exist to refuse. Its DEFINITION moved
    into `serve_projection.py` instead — openXdox, already importing
    `snapshot_registry`, already holding `hosted_index` (pre-carve split S-3,
    the precedent), already holding three of the predicate's four call sites,
    and already in the serve surface `conftest.py` scans. So the adapter column
    reaches the predicate through openXdox, which is the allowed direction and
    the one OQ-B **B-3** took for the sessions reach.

WHY A TEST AND NOT A NOTE. The re-plumb is import lines. It is undone by a
single "just import it from `serve_wire` again" edit that no other test would
notice — the objects are identical by construction, so nothing goes red. The
edge is the property, and an edge is only kept by something that measures it.
Two of the four assertions here are ABSENCES (no reach, no binding), which is
why each has a non-vacuity or negative-control companion below.

PARSED, NOT GREPPED, and this file needs a scanner `tests/import_scan.py` does
NOT provide: that module's `imported_modules` deliberately SKIPS relative
imports, because it exists to police a direction between top-level PACKAGES,
where a relative import can never reach. Here the forbidden direction runs
BETWEEN SIBLINGS OF ONE PACKAGE, so the scan below resolves all FIVE spellings
the package can use — `from .X import`, `from . import X`,
`from ideation_dashboard.X import`, `from scripts.ideation_dashboard.X import`
and `import ideation_dashboard.X` / `import scripts.ideation_dashboard.X`
(`scripts/__init__.py` exists, so both absolute spellings resolve and a
one-spelling scan is a hole). It walks the whole tree, so a lazy
function-local import is reported exactly like a module-level one.

DELIBERATELY A NEW FILE. `tests/ideation-dashboard/test_oqb_replumb.py` and
`tests/doc-health/test_import_direction.py` belong to OQ-B part 1 (PR #843),
which is in flight on its own branch; extending either would have made two
independent re-plumbs share one file and one review. The neutrality test below
is therefore a SIBLING of the guard's own neutrality test rather than a
widening of it, for the reason #843 gives for its own: two neutral modules can
lose the property independently, and one looped assertion would report only
the first.
"""

from __future__ import annotations

import ast

import pytest

from carved_reach import source as carved_source
from conftest import REPO_ROOT

import wire_messages
from opendox import serve as serve_mod
from ideation_dashboard import serve_openxfactory_lanes
from opendox import serve_wire
from opendox import wire_messages as leg_wire_messages
from openxdox import serve_projection

NEUTRAL_WIRE_MESSAGES = REPO_ROOT / "scripts" / "wire_messages.py"

#: The three names the ruling sent to the neutral module, and which
#: `serve_wire.py` re-exports.
WIRE_STRINGS = ("HOSTED_SESSION_REFUSAL", "JSON_CTYPE", "JSON_OBJECT_BODY_REQUIRED")

# The two DESTINATION package roots join the two pre-shed ones rather than
# replacing them (Copilot `PRRT_kwDOTAvnrs6hVaMZ`). After the § 5.2 shed the
# lawful edge this file proves — the adapter column reaching the projection
# column — is spelled `from openxdox.serve_projection import hosted_ref_refused`,
# and the forbidden one would be spelled `from opendox import serve_wire`. A
# scanner left at the two pre-shed roots would see NEITHER: the positive
# assertion would fail over an empty set while a restored `serve_wire` edge
# walked past the absence. Both pre-shed spellings stay — `scripts/__init__.py`
# still exists and the negative control still feeds all of them through here.
_ABSOLUTE_ROOTS = ("ideation_dashboard", "scripts.ideation_dashboard",
                   "opendox", "openxdox")

# Both spellings of each package, for the neutrality scan. `scripts/__init__.py`
# exists, so every package under `scripts/` is importable BOTH as a top-level
# name and as `scripts.<name>`, and a one-spelling forbidden list is a hole.
# `opendox` and `openxdox` are the POST-SHED spellings of the same two columns
# and are forbidden for the identical reason: `wire_messages.py` travels to
# openDox as a replica, and a replica that imported `openxdox` — or `opendox`,
# naming its own destination package from inside openxFactory — would be
# un-carveable in exactly the way this test exists to prevent.
FORBIDDEN_FOR_A_NEUTRAL_MODULE = (
    "ideation_dashboard", "scripts.ideation_dashboard",
    "doc_health", "scripts.doc_health",
    "opendox", "openxdox",
)


# --------------------------------------------------------------------------
# the scanners
# --------------------------------------------------------------------------

def sibling_imports(tree):
    """Every SIBLING module of `ideation_dashboard` a parsed file imports, with
    the line it does it on, in all five spellings.

    Takes a TREE rather than a path so the negative control at the bottom can
    feed the identical scanner a restored-edge source string instead of writing
    a file into the package this test polices.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level:
                if node.module:                       # from .X import a
                    yield node.module.split(".")[0], node.lineno
                else:                                 # from . import X, Y
                    for alias in node.names:
                        yield alias.name, node.lineno
            elif node.module:
                for root in _ABSOLUTE_ROOTS:
                    if node.module == root:           # from ideation_dashboard import X
                        for alias in node.names:
                            yield alias.name, node.lineno
                        break
                    if node.module.startswith(root + "."):
                        yield node.module[len(root) + 1:].split(".")[0], node.lineno
                        break
        elif isinstance(node, ast.Import):
            for alias in node.names:
                for root in _ABSOLUTE_ROOTS:
                    if alias.name.startswith(root + "."):   # import ideation_dashboard.X
                        yield alias.name[len(root) + 1:].split(".")[0], node.lineno
                        break


def module_tree(name: str):
    """One module of the pre-shed package, parsed — wherever it is TODAY.

    The three modules this file reads sit on both sides of the carve now
    (`serve_wire.py` went to openDox-code, `serve_openxfactory_lanes.py` is a
    `stays_openxfactory_adapter` row), so the package prefix that used to
    answer for all of them cannot (RULED (a), `#656` `5625573095`; Copilot
    `PRRT_kwDOTAvnrs6hUpwC`). `carved_reach.source()` answers each from its own
    manifest row, and the name passed in is still the pre-shed one every
    reader of this repository's history recognises.
    """
    path = carved_source(f"scripts/ideation_dashboard/{name}.py")
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def imported_module_names(tree):
    """Every module name a parsed file IMPORTS, with its line — absolute
    spellings only, which is all a neutrality question needs (a relative import
    is confined to its own package, and a neutral module is in no package).

    Takes a TREE for the same reason `sibling_imports` does: the negative
    control at the bottom feeds this very function a lost-neutrality source
    string, rather than a second copy of its body.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name, node.lineno
        elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
            yield node.module, node.lineno


def parse_file(path):
    """One file on disk, parsed."""
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def names_a_forbidden_package(module: str, forbidden) -> bool:
    """True when `module` IS one of `forbidden` or sits underneath one."""
    return any(module == f or module.startswith(f + ".") for f in forbidden)


def bound_at_module_level(tree, name: str):
    """Every line at which a parsed module BINDS `name` itself — by `def`, by
    `class`, by assignment or by import-as — so "not reachable here" can be
    asserted about the SOURCE rather than about an attribute lookup that a
    re-export would satisfy just as well."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == name:
                yield node.lineno
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    yield node.lineno
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if (alias.asname or alias.name.split(".")[0]) == name:
                    yield node.lineno


# --------------------------------------------------------------------------
# 1. the edge itself: the adapter column reaches `serve_wire` NOT AT ALL
# --------------------------------------------------------------------------

def test_the_adapter_column_imports_nothing_from_the_wire_module():
    """The STRONG form, and it is available because the residual reach is
    empty: PR #848 measured `serve_openxfactory_lanes` -> `serve_wire` at
    exactly ONE statement carrying exactly these four names, so once they are
    re-plumbed there is nothing left to allow. Any spelling, module level or
    function-local — a lazy import is still an import and still the edge the
    carve cannot cross."""
    offenders = [f"serve_openxfactory_lanes.py:{line} imports {module!r}"
                 for module, line in sibling_imports(
                     module_tree("serve_openxfactory_lanes"))
                 if module == "serve_wire"]
    assert offenders == [], (
        "openxFactory's own adapter column must import NOTHING from "
        "`serve_wire` (OQ-B B-2, ruled on `#656` 2026-09-09): the wire module "
        "goes WHOLE to openDox and openxFactory may not import openDox after "
        "the carve. The predicate is `from ideation_dashboard.serve_projection "
        "import hosted_ref_refused` now and the three strings are "
        f"`from wire_messages import ...`. Offending imports: {offenders}")


def test_the_adapter_column_still_reaches_both_new_homes():
    """Non-vacuity for the absence above, in the shape that matters: a column
    that had simply STOPPED confining the hosted plane, or stopped answering
    JSON, would also import nothing from `serve_wire` and would also pass."""
    siblings = {module for module, _ in
                sibling_imports(module_tree("serve_openxfactory_lanes"))}
    assert "serve_projection" in siblings, (
        "the adapter column no longer imports `serve_projection` — it has "
        "stopped reaching the hosted-plane ref confinement, not been "
        "re-plumbed")
    assert serve_openxfactory_lanes.hosted_ref_refused is \
        serve_projection.hosted_ref_refused
    for name in WIRE_STRINGS:
        assert getattr(serve_openxfactory_lanes, name) is \
            getattr(wire_messages, name), name


# --------------------------------------------------------------------------
# 2. the wire module keeps NO binding of the predicate, and its openXdox
#    dependency went with it
# --------------------------------------------------------------------------

def test_the_wire_module_binds_the_predicate_nowhere():
    """Both halves matter and neither implies the other for the carve manifest
    (the same reasoning S-3's own guard records for `hosted_index`): the wire
    module is an openDox row, so an openXdox rule DEFINED in it — or merely
    RE-EXPORTED from it for a caller's convenience — is a path with two
    columns, which is the shape § 3.1 cannot file. The source scan catches
    both, since a `def` and an `import` bind the same module attribute."""
    tree = module_tree("serve_wire")
    bindings = sorted(bound_at_module_level(tree, "hosted_ref_refused"))
    assert bindings == [], (
        "`hosted_ref_refused` is bound in `serve_wire.py` again at "
        f"{bindings} — B-2 re-homed it into `serve_projection.py` and left no "
        "re-export; see `serve_wire.py`'s module docstring")
    assert getattr(serve_wire, "hosted_ref_refused", None) is None


def test_the_wire_module_no_longer_imports_the_openxdox_registry():
    """The edge the move ALSO removed, which is why it is worth an assertion of
    its own: `snapshot_registry` is the openXdox column and the predicate was
    `registry_mod`'s only reader in this file, so an openDox -> openXdox import
    left the wire module with the predicate. Restoring the import would be the
    first step of putting the predicate back, and it would go unnoticed."""
    offenders = [f"serve_wire.py:{line} imports {module!r}"
                 for module, line in sibling_imports(module_tree("serve_wire"))
                 if module == "snapshot_registry"]
    assert offenders == [], (
        "`serve_wire.py` imports `snapshot_registry` again — nothing in the "
        "module needs it since `hosted_ref_refused` left, and the import is "
        f"an openDox -> openXdox edge. Offending imports: {offenders}")
    assert getattr(serve_wire, "registry_mod", None) is None


def test_the_scan_would_catch_a_restored_edge_in_every_spelling():
    """A negative control, because the three assertions above are proofs of
    ABSENCE. Fed through the SAME scanner the tests use — not a copy of it —
    so a hole in the spelling handling (relative handling swallowing an
    absolute one, `ast.walk` missing a function-local import) cannot leave
    those tests green over a restored edge."""
    restored = (
        "from .serve_wire import hosted_ref_refused\n"
        "from . import serve_wire as wire_mod\n"
        "from ideation_dashboard.serve_wire import JSON_CTYPE\n"
        "from scripts.ideation_dashboard.serve_wire import HOSTED_SESSION_REFUSAL\n"
        "import ideation_dashboard.serve_wire\n"
        "\n"
        "def _late():\n"
        "    import scripts.ideation_dashboard.serve_wire as lazy_mod\n"
        "    from ideation_dashboard import serve_wire as also_lazy\n"
        "    return lazy_mod, also_lazy\n"
    )
    caught = [line for module, line in sibling_imports(ast.parse(restored))
              if module == "serve_wire"]
    assert len(caught) == 7, (
        f"the scanner recognised {len(caught)} of the 7 restorations "
        f"(lines {caught}) — a real restoration of the edge could slip past "
        "`test_the_adapter_column_imports_nothing_from_the_wire_module`")
    # and the binding scan, on the same restored source
    assert sorted(bound_at_module_level(ast.parse(restored),
                                        "hosted_ref_refused")) == [1]


# --------------------------------------------------------------------------
# 3. the public surface the move preserved: the SAME objects, not copies
# --------------------------------------------------------------------------

@pytest.mark.parametrize("name", WIRE_STRINGS)
def test_the_wire_module_re_exports_the_neutral_string_itself(name):
    """`serve_wire.<string> is wire_messages.<string>`: a re-export, not a
    second spelling of the same prose. `ideation_dashboard/boundary.py`'s
    precedent, and the property every existing openDox and openXdox reader
    depends on — `serve_gate.py`, `serve_project.py`, `serve_workbench.py`,
    `serve_projection.py` and `serve.py` all still import them from
    `serve_wire`, which the carve permits for their columns.

    ASKED OF openDox'S OWN REPLICA AFTER THE § 5.2 SHED. `scripts/wire_messages.py`
    is a `replicated_at_destination` row (RULED OQ-A/OQ-C — the module both
    sides depend on travels as a REPLICA rather than as a module shared across
    a boundary with no pin), so post-shed `serve_wire` re-exports openDox's
    copy while `serve_openxfactory_lanes` binds openxFactory's. Both halves of
    "a re-export, not a second spelling" are still asserted, each against the
    module its own leg actually carries: this one against
    `opendox.wire_messages`, and the openxFactory one in
    `test_the_adapter_column_still_reaches_both_new_homes` above against the
    root `wire_messages`. A cross-leg `is` on these three was true only while
    the two copies were one file — and on interned string constants it would
    have gone on passing for the wrong reason if any of the three were ever
    redefined rather than imported, which is why
    `test_the_wire_module_defines_none_of_the_three_strings_itself` below reads
    the SOURCE and is the assertion that actually closes the gap."""
    assert getattr(serve_wire, name) is getattr(leg_wire_messages, name)
    assert getattr(serve_mod, name) is getattr(leg_wire_messages, name)


def test_the_wire_module_defines_none_of_the_three_strings_itself():
    """Identity on interned `str` constants is not by itself evidence of a
    re-export — two equal literals can be the same object. So the SOURCE is
    asserted too: `serve_wire.py` binds each name exactly once, and that
    binding is the import."""
    tree = module_tree("serve_wire")
    for name in WIRE_STRINGS:
        lines = sorted(bound_at_module_level(tree, name))
        assert len(lines) == 1, (
            f"`serve_wire.py` binds {name} at {lines} — B-2 left exactly one "
            "binding, the re-export from `wire_messages`")
        assert not any(
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == name
                    for t in node.targets)
            for node in ast.walk(tree)), (
            f"`serve_wire.py` ASSIGNS {name} again — the neutral module is "
            "the one definition, and a second one is the drift the module's "
            "own import comments refuse")


def test_serve_re_exports_the_predicate_from_its_new_home():
    """The public surface B-2 preserved, S-3's own guard one name along:
    `serve.hosted_ref_refused` still resolves, and resolves to the projection
    column's function rather than to a second copy left in the wire module.
    `test_session_snapshot.py:781-788` reads it exactly this way."""
    assert serve_mod.hosted_ref_refused is serve_projection.hosted_ref_refused


def test_the_relocated_predicate_still_answers_as_it_did():
    """The behaviour the moved text promises, so "byte-identical relocation"
    is not taken on faith: loopback is never confined, `main` and the two
    spellings that MEAN `main` are publishable, and a session ref is refused
    off loopback (FR-048)."""
    refused = serve_projection.hosted_ref_refused
    assert refused(False, "draft/some-topic") is True
    assert refused(False, "cluster/cl-x") is True
    assert refused(False, "main") is False
    assert refused(False, None) is False     # None means `main`
    assert refused(False, "") is False       # blank means `main`
    assert refused(True, "draft/some-topic") is False


# --------------------------------------------------------------------------
# 4. the new neutral module is neutral, by parsing
# --------------------------------------------------------------------------

def test_the_neutral_wire_messages_module_imports_neither_package():
    """`wire_messages` is neutral, and neutrality is a property of its imports,
    not of where the file sits.

    It is a module BOTH sides depend on, so an import of either package from
    inside it would make it un-carveable when it travels to openDox as a
    replica (`not_moved / replicated_at_destination`, RULED OQ-A/OQ-C) —
    openDox has no notion of `doc_health` at all, and `snapshot_registry` is
    openXdox, which is exactly why the predicate could not come here. It
    reaches for the standard library only.

    A SIBLING of `tests/doc-health/test_import_direction.py`'s
    `test_the_neutral_guard_imports_neither_package` rather than a widening of
    it: that one is design D2's claim about the write path, this one is OQ-B's
    about three wire strings; they can be lost independently, and one looped
    assertion would report only the first."""
    offenders = [f"wire_messages.py:{line} imports {module!r}"
                 for module, line in imported_module_names(
                     parse_file(NEUTRAL_WIRE_MESSAGES))
                 if names_a_forbidden_package(
                     module, FORBIDDEN_FOR_A_NEUTRAL_MODULE)]
    assert offenders == [], (
        "the neutral wire strings must depend on NEITHER package — the module "
        "is replicated at every destination and travels to openDox with the "
        f"carve. Offending imports: {offenders}")
    # Non-vacuity: a scan of a file that could not be read, or of the wrong
    # path, would also find no offenders.
    assert NEUTRAL_WIRE_MESSAGES.is_file()
    assert [m for m, _ in
            imported_module_names(parse_file(NEUTRAL_WIRE_MESSAGES))] == \
        ["__future__"], "the neutral module's import list is no longer stdlib-only"


def test_the_neutrality_scan_would_catch_either_package():
    """A negative control for the absence above, in both spellings of both
    packages and in a lazy import, fed through the SAME two functions the test
    uses — `imported_module_names` and `names_a_forbidden_package`, not copies
    of them — so a hole in either (a missed `import a.b` form, `ast.walk`
    missing a function-local import) cannot leave that test green over a
    module that has lost the property."""
    restored = (
        "from ideation_dashboard import snapshot_registry\n"
        "import scripts.ideation_dashboard.serve_wire\n"
        "from doc_health import pin_sentinels\n"
        "from opendox import serve_wire\n"
        "import openxdox.snapshot_registry\n"
        "\n"
        "def _late():\n"
        "    import scripts.doc_health.corpus\n"
    )
    found = list(imported_module_names(ast.parse(restored)))
    caught = [f"{module} (line {line})" for module, line in found
              if names_a_forbidden_package(
                  module, FORBIDDEN_FOR_A_NEUTRAL_MODULE)]
    assert len(caught) == 6, (
        f"the scan recognised {caught} out of {found} — a real loss of "
        "neutrality could slip past "
        "`test_the_neutral_wire_messages_module_imports_neither_package`")
