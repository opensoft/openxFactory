"""A workbench manifest the pinned openDox leg writes validates against the
pinned openXdox validator: a composition test moved here under R1Q2 (a), on
F11.1's `HOST_TESTS` surface.

MOVED HERE by plan 034 T035 (opensoft/openDox-code#51, landed `80acead1`).
The three cases left `tests/test_workbench.py` at openDox-code `68be484a`
(`:119-126`, `:129-140` and `:212-224`), where they SKIPPED: they need
`scripts/validate-ideation-dashboard-contracts.py`, which the § 5.2 shed sent
to openXdox-code, and openDox-code composes no openXdox leg. openxFactory
composes both: `_composed_validator()` below resolves the validator through
its manifest row and `doxbench_contracts._composed_validator`, as
`tests/ideation-dashboard/conftest.py`'s `find_openxfactory_validator()`
does, so here the three RUN.

The cases' bodies and their helpers (`_seeded_set`, `_boundary`,
`_init_git_repo`, `_commit`) are #51's source, verbatim. `wb` is the pinned
openDox leg's `opendox.workbench`, which the root conftest puts on the path.

WHY `tests/domain_profile/`, AND NOT THE PROPOSED `tests/ideation-dashboard/`
PATH. `tests/ideation-dashboard/` is inside the carve surface
(`docs/opendox-carve-manifest.yaml` `moved_paths:`), where
`scripts/validate-carve-manifest.py` refuses a NEW file that no row declares
(`carve-file-undeclared`), and F11.1 forbids adding the row. This directory is
outside that surface, and it is F11.1's own `HOST_TESTS` prefix. The root
`tests/conftest.py` installs the reach and makes the host's one call here too,
so a case that composes the pinned legs composes the same ones it would have
composed there.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from carved_reach import source as carved_source
from ideation_dashboard import doxbench_contracts

from opendox import workbench as wb
from opendox.boundary import OutputBoundary


def _composed_validator() -> Path | None:
    """The validator the carve sent to openXdox-code, composed with its
    schemas: `tests/ideation-dashboard/conftest.py`'s `_shed_validator()`
    resolution, which that directory's `find_openxfactory_validator()`
    answers there. None only if the leg is not on disk."""
    moved = carved_source("scripts/validate-ideation-dashboard-contracts.py")
    if not moved.is_file():
        return None
    return doxbench_contracts._composed_validator(moved)


VALIDATOR = _composed_validator()

NOW = "2026-07-14T08:00:00Z"


def _boundary(root: Path, *extra: str) -> OutputBoundary:
    return OutputBoundary(root, [wb.WORKBENCH_DIR, *extra])


def _seeded_set() -> wb.Workbench:
    w = wb.Workbench.create("fixture-repo", "Dashboard readiness sweep",
                            seed=wb.SEED_CLUSTER, cluster_id="cl-x", now=NOW)
    w.add_member("ideation/brainstorm/dtn-register.md", wb.VIA_CLUSTER_SEED, now=NOW)
    w.add_member("ideation/brainstorm/legacy-note.md", wb.VIA_MANUAL_INCLUDE,
                 reason="belongs in the readiness sweep even though it predates the cluster", now=NOW)
    w.exclude("ideation/brainstorm/doc-health-checks.md", "out of dashboard scope", now=NOW)
    w.set_recipe({"checked": ["ideation-dashboard", "keyword-lens"],
                  "pinned": ["ideation-dashboard"]}, now=NOW)
    w.bind_notebook(now=NOW)
    return w


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_saved_manifest_validates_clean_against_the_pinned_validator(tmp_path):
    w = _seeded_set()
    # save(validate=True) re-runs the pinned validator and raises on any failure
    written = wb.save(w, _boundary(tmp_path), validate=True, validator=VALIDATOR)
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(written)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_recipe_seeded_manifest_carries_the_recipe_block_and_validates(tmp_path):
    # seed.kind == recipe ⇒ the recipe block is REQUIRED (schema conditional)
    w = wb.Workbench.create("fixture-repo", "Lens recipe set", seed=wb.SEED_RECIPE,
                            recipe={"checked": ["ideation-dashboard", "keyword-lens"],
                                    "pinned": ["keyword-lens"],
                                    "last_run": {"source_revision": "abcd" * 10}}, now=NOW)
    w.add_member("ideation/brainstorm/dtn-register.md", wb.VIA_RECIPE_MATCH, now=NOW)
    written = wb.save(w, _boundary(tmp_path), validate=True, validator=VALIDATOR)
    reloaded = wb.Workbench.load(written)
    assert reloaded.data["seed"]["kind"] == "recipe"
    assert reloaded.data["recipe"]["checked"] == ["ideation-dashboard", "keyword-lens"]


# ----------------------------------------------------------------------------
# committed-manifest guard, the validator's half
# ----------------------------------------------------------------------------

def _init_git_repo(root: Path) -> None:
    for args in (["init", "-q"], ["config", "user.email", "t@t"],
                 ["config", "user.name", "t"]):
        subprocess.run(["git", "-C", str(root), *args], check=True,
                       capture_output=True, text=True)


def _commit(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", rel], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "x"], check=True, capture_output=True)


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_committed_manifest_is_rejected_by_the_pinned_validator(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _init_git_repo(root)
    manifest = wb.Workbench.create("repo", "leaked set", now=NOW)
    manifest.add_member("docs/x.md", wb.VIA_RECIPE_MATCH, now=NOW)
    _commit(root, "docs/leaked.workbench.yaml", manifest.render())
    proc = subprocess.run([sys.executable, str(VALIDATOR), "--repo", str(root)],
                          capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    assert "committed-workbench-manifest" in out, out
    assert proc.returncode != 0
