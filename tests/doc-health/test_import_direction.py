"""The seam is one-way: `doc_health` imports NOTHING from `ideation_dashboard`.

`split-opendox-two-layer-product` § 2.1 is the task this file discharges, and
it names its own proof: "After this task `scripts/doc_health/` imports NOTHING
from `scripts/ideation_dashboard/`, proven by a test that greps for the
direction rather than by inspection."

WHY A TEST AND NOT A NOTE. The two packages used to import each OTHER.
`ideation_dashboard` imports `doc_health` in twenty-three places — that
direction is lawful and stays; under RULING Q4 it becomes the adapter's
implementation surface, code that legitimately imports doc-health in the
repository where doing so is lawful (design D2). What was NOT lawful was the
back-edge: `derive_possibles.make_boundary` and
`ideation_readiness.make_boundary` reached into `ideation_dashboard.boundary`
for `OutputBoundary`. Both were LAZY, function-local imports carrying a
`# lazy: house guard` comment — which is exactly how a cycle survives review
for a long time: it never fires at import, no test goes red, and the only
symptom is that the seam cannot be cut. § 2.1 moved the guard to
`scripts/output_boundary.py`, in neither package, and this file is the thing
that keeps it moved. Restore either import and this goes red at once.

PARSED, NOT GREPPED — and the difference is load-bearing here. Four files in
`scripts/doc_health/` mention `ideation_dashboard` in PROSE and must keep
doing so, because what they are documenting is real coupling of a different
kind: `corpus.py` and `lines.py` name the dashboard readers that must agree
with doc-health's own header scan, and `pin_class.py` / `pin_sentinels.py`
name dashboard modules as the SUBJECTS of findings. A substring grep would
call all four violations, and the pressure to make it green would be pressure
to delete true documentation. So the scan reads import STATEMENTS out of the
syntax tree; a name inside a comment, a docstring or a string literal is not
an import and is not flagged.
"""

from __future__ import annotations

import ast

from conftest import REPO_ROOT
# The two scanners below were defined HERE first, for this file's own direction
# (`split-opendox-two-layer-product` § 2.1); § 2.2/2.2a needs the identical pair
# for a different direction, so they moved to a shared helper rather than being
# copied. The three tests and every assertion in them are unchanged.
from import_scan import (
    imported_modules as _imported_modules,
    names_a_forbidden_package as _names_a_forbidden_package,
)

DOC_HEALTH = REPO_ROOT / "scripts" / "doc_health"
NEUTRAL_GUARD = REPO_ROOT / "scripts" / "output_boundary.py"
# The SECOND neutral module (OQ-B re-plumb B-1, ruled on `#656` 2026-09-09):
# `slug` moved out of `ideation_dashboard/workbench.py` so openxFactory's own
# adapter (`human_seen.py`) could stop importing openDox. Same property, same
# instrument — see `test_the_neutral_path_slug_imports_neither_package`.
NEUTRAL_SLUG = REPO_ROOT / "scripts" / "path_slug.py"

# Both spellings of the same package. `ideation_dashboard` is how every caller
# imports it today (it resolves as a top-level name off `scripts/`), but
# `scripts/__init__.py` exists, so `scripts.ideation_dashboard` is importable
# too and would reintroduce the same edge by a route a one-spelling test would
# miss.
FORBIDDEN_ROOTS = ("ideation_dashboard", "scripts.ideation_dashboard")


def test_doc_health_imports_nothing_from_ideation_dashboard():
    """§ 2.1's success criterion, stated as the thing it is: a DIRECTION.

    Every `*.py` under `scripts/doc_health/`, at every nesting depth, at module
    level and inside functions alike — a lazy import is still an import and is
    still the edge that made the two packages a cycle."""
    offenders = []
    scanned = 0
    for path in sorted(DOC_HEALTH.rglob("*.py")):
        scanned += 1
        for module, line in _imported_modules(path):
            if _names_a_forbidden_package(module, FORBIDDEN_ROOTS):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{line} imports {module!r}")

    assert offenders == [], (
        "`doc_health` must import NOTHING from `ideation_dashboard` "
        "(split-opendox-two-layer-product § 2.1): the seam openDox/openXdox is "
        "cut along cannot pass through a cycle. If the import is for the write "
        "guard, it is `from output_boundary import OutputBoundary` now. "
        f"Offending imports: {offenders}")

    # Non-vacuity. A scan that found no files would also find no offenders, and
    # would keep passing after a rename of the package it is meant to police.
    assert scanned >= 20, (
        f"only {scanned} modules scanned under {DOC_HEALTH} — the scan lost its "
        f"subject; check the path before trusting the assertion above")


def test_the_scan_would_catch_the_import_it_is_meant_to_catch():
    """A negative control, because the assertion above is a proof of ABSENCE.

    The exact two lines § 2.1 removed, fed back through the same parser: if
    this file's machinery had a hole (relative-import handling swallowing an
    absolute one, `ast.walk` missing a function-local import), the test above
    would be green over a restored cycle and nobody would know."""
    restored = (
        "def make_boundary(root):\n"
        "    from ideation_dashboard.boundary import OutputBoundary\n"
        "    return OutputBoundary(root, [])\n"
        "\n"
        "import scripts.ideation_dashboard.boundary as alt\n"
    )
    tree = ast.parse(restored)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
            found.append(node.module)
    caught = [m for m in found if _names_a_forbidden_package(m, FORBIDDEN_ROOTS)]
    assert len(caught) == 2, (
        f"the scan recognised {caught} out of {found} — a real restoration of "
        f"the back-edge could slip past `test_doc_health_imports_nothing_from_"
        f"ideation_dashboard`")


def test_the_neutral_guard_imports_neither_package():
    """`output_boundary` is neutral, and neutrality is a property of its
    imports, not of where the file sits.

    It is the module BOTH sides depend on (design D2), so an import of either
    package from inside it would put the cycle back one level down — and worse,
    would make the guard un-carveable when it travels to openDox, which has no
    notion of `doc_health` at all. It reaches for the standard library only."""
    offenders = [
        f"{NEUTRAL_GUARD.name}:{line} imports {module!r}"
        for module, line in _imported_modules(NEUTRAL_GUARD)
        if _names_a_forbidden_package(
            module, FORBIDDEN_ROOTS + ("doc_health", "scripts.doc_health"))
    ]
    assert offenders == [], (
        "the neutral write guard must depend on NEITHER package — it is the "
        "module both of them import, and it travels to openDox with the carve "
        f"(design D2). Offending imports: {offenders}")


def test_the_neutral_path_slug_imports_neither_package():
    """`path_slug` is neutral for the same reason `output_boundary` is, and it
    is proven the same way rather than asserted in its header.

    It is the module the openDox column (`workbench.slug`, and through it
    `authoring`, `gate_console`, `gate_routes`) and the openxFactory column
    (`human_seen`) BOTH depend on, so an import of either package from inside
    it would put back exactly the edge B-1 removed, one level down — and would
    make the slug un-replicable when it travels to openDox, which has no notion
    of `doc_health` at all. Like the guard above, it reaches for the standard
    library only (`re`).

    A SEPARATE test rather than a widened one: the guard's neutrality is D2's
    claim about the write path and this one is OQ-B's claim about a filename
    component. They are two rulings, they can be lost independently, and a
    single looped assertion would report only the first."""
    offenders = [
        f"{NEUTRAL_SLUG.name}:{line} imports {module!r}"
        for module, line in _imported_modules(NEUTRAL_SLUG)
        if _names_a_forbidden_package(
            module, FORBIDDEN_ROOTS + ("doc_health", "scripts.doc_health"))
    ]
    assert offenders == [], (
        "the neutral path slug must depend on NEITHER package — it is the "
        "module both columns import, and at the carve it is `not_moved` with "
        "reason `replicated_at_destination` (RULED OQ-A/OQ-C, `#656` "
        f"2026-09-09). Offending imports: {offenders}")
