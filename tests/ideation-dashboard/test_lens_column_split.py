"""THE LENS SPLIT: `lens.py` no longer reaches openxFactory's adapter column
(pre-carve split S-2, `split-opendox-two-layer-product` § 3.1).

`add_as_cluster` and `AddAsClusterResult` moved to `lens_submission.py`
UNCHANGED, byte for byte, with the `human_seen` import they use. Everything else
in `lens.py` is the openDox set-builder (design D3: "the keyword-query half of
`lens` … PULL UP"), and the scout memo measured `lens -> human_seen` as the
single `openDox -> openxFactory` import edge in the whole package. Removing it is
the ONLY point of the split, so it is the one thing a test has to hold.

PARSED, NOT GREPPED, and the difference is load-bearing here exactly as it is in
`tests/doc-health/test_import_direction.py`: `lens.py`'s docstring and its
`PENDING_PROPOSAL_NOTE` comment both still NAME `human_seen.py` in prose, and
must keep doing so — they are documenting where the submission path went. A
substring grep would call both violations, and the pressure to make it green
would be pressure to delete true documentation.

NO RE-EXPORT IS ALSO ASSERTED, and it is the failure mode this file exists for.
Leaving `from .lens_submission import add_as_cluster` in `lens.py` so callers
keep working would put `human_seen` back on `lens`'s import graph transitively —
with every other test in the suite still green, and the edge the split was for
silently restored. `tests/import_scan.py`'s `imported_modules` skips relative
imports by design (it polices a direction BETWEEN packages), so the scan below
is this file's own and reads both spellings and both nesting levels.
"""

from __future__ import annotations

import ast

from carved_reach import source as carved_source

from ideation_dashboard import lens_submission
from opendox import lens

# `lens.py` left for openDox-code in the § 5.2 shed and this test reads its
# SOURCE, so the path comes from that file's own manifest row rather than from a
# package prefix — the prefix would name the deleted root (RULED (a), `#656`
# `5625573095`; Copilot `PRRT_kwDOTAvnrs6hUpvi`).
LENS = carved_source("scripts/ideation_dashboard/lens.py")

# `scripts/__init__.py` exists, so every module under `scripts/` is importable
# BOTH as a top-level name and as `scripts.<name>`; a relative import inside the
# package is a third spelling again. All three are the same edge.
ROOTS = ("ideation_dashboard", "scripts.ideation_dashboard")


def _imports_sibling(source: str, sibling: str):
    """Every import in `source` that names the sibling module `sibling`, as
    (line, spelling). Walks the whole tree, so a lazy function-local import is
    reported exactly like a module-level one — a lazy import is still an import,
    and it is how a cycle survives review for a long time."""
    dotted = tuple(f"{root}.{sibling}" for root in ROOTS)
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):                       # import pkg.sibling
            for alias in node.names:
                if alias.name in dotted:
                    yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.module is None:             # from . import sibling
                for alias in node.names:
                    if alias.name == sibling:
                        yield node.lineno, f"from . import {sibling}"
            elif node.level and node.module == sibling:        # from .sibling import X
                yield node.lineno, f"from .{sibling} import …"
            elif not node.level and node.module in dotted:     # from pkg.sibling import X
                yield node.lineno, f"from {node.module} import …"
            elif not node.level and node.module in ROOTS:      # from pkg import sibling
                for alias in node.names:
                    if alias.name == sibling:
                        yield node.lineno, f"from {node.module} import {sibling}"


def test_lens_imports_nothing_from_human_seen():
    """The removed edge, stated as the thing it is: a DIRECTION. `lens.py` is
    openDox; `human_seen.py` is openxFactory's own engineering adapter (D3's
    third column, RULING DQ-1). openDox may not reach it — directly, or
    transitively by re-importing the module `human_seen` moved to
    (`lens_submission`); a bare `from . import lens_submission` in `lens.py`
    would restore the same reach with every other test in the suite still
    green, so the scan below covers both siblings."""
    source = LENS.read_text(encoding="utf-8")
    offenders = [f"lens.py:{line} {spelling}"
                 for sibling in ("human_seen", "lens_submission")
                 for line, spelling in _imports_sibling(source, sibling)]
    assert offenders == [], (
        "`lens.py` is the openDox set-builder and must not import openxFactory's "
        "cross-reference submission path — that is what pre-carve split S-2 "
        "removed, and `lens_submission.py` is where it went — nor may it "
        "re-import `lens_submission` itself, which would restore the "
        f"`human_seen` reach transitively. Offenders: {offenders}")


def test_the_scan_sees_every_spelling_of_the_edge():
    """The negative control, measuring the SAME input the shipped assertion
    does: a scan that silently recognised nothing would pass the test above on
    an empty file just as happily as on a clean one."""
    restored = (
        "from . import human_seen\n"
        "from .human_seen import HumanSeenSubmission\n"
        "from ideation_dashboard import human_seen as hs\n"
        "from ideation_dashboard.human_seen import SubmissionRefused\n"
        "import scripts.ideation_dashboard.human_seen\n"
        "def f():\n"
        "    from . import human_seen as lazy\n"
    )
    caught = list(_imports_sibling(restored, "human_seen"))
    assert len(caught) == 6, (
        f"the scan recognised {caught} out of six spellings — a real restoration "
        "of the edge could slip past `test_lens_imports_nothing_from_human_seen`")


def test_add_as_cluster_is_not_re_exported_from_lens():
    """A convenience re-export would put the edge back transitively, with every
    behavioural test still green. The two in-tree callers were repointed
    instead (`gate_routes.execute_lens_add_as_cluster`, `test_lens.py`)."""
    assert callable(lens_submission.add_as_cluster)
    assert lens_submission.AddAsClusterResult.__module__.endswith("lens_submission")
    for name in ("add_as_cluster", "AddAsClusterResult", "human_seen",
                 "HumanSeenSubmission", "SubmissionRefused"):
        assert not hasattr(lens, name), (
            f"`lens.{name}` still resolves — the split's whole point is that "
            "`lens.py` carries no add-as-cluster surface and no `human_seen` reach")
