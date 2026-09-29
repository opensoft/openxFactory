"""The workbench's scoped doc-health runs openxFactory's real checker through
the seam the host registers: a composition test moved here under R1Q2 (a), on
F11.1's `HOST_TESTS` surface.

MOVED HERE by plan 034 T035 (opensoft/openDox-code#51, landed `80acead1`).
The three cases left `tests/test_workbench.py` at openDox-code `68be484a`
(`:456-466`, `:469-475` and `:478-486`). There, two FAILED and the third
passed only because an empty findings list satisfies its `all(...)`: the
check they drive is openxFactory's `doc_health`, which openDox cannot install.
From plan 034 T026 on, `workbench.run_scoped_doc_health` runs whatever check a
host registered with `workbench.register_health_check`, and openxFactory's
host registers its own (T046, `opendox_host.scoped_doc_health`) at the one
process-start call `tests/conftest.py` makes. So the cases compose here: the
pinned openDox leg's workbench, this repository's checker, and this
repository's `base-repo` fixture.

The cases' bodies are #51's source, verbatim. `BASE_REPO` is
`tests/ideation-dashboard/fixtures/base-repo`, the fixture openDox-code's copy
was taken from.

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

from datetime import date
from pathlib import Path

from opendox import workbench as wb

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE_REPO = REPO_ROOT / "tests" / "ideation-dashboard" / "fixtures" / "base-repo"

NOW = "2026-07-14T08:00:00Z"


def test_scoped_doc_health_runs_real_machinery_over_the_fixture():
    docs = ["ideation/brainstorm/dtn-register.md", "ideation/brainstorm/legacy-note.md"]
    w = wb.Workbench.create("fixture-repo", "DH scope", now=NOW)
    result = wb.run_scoped_doc_health(BASE_REPO, docs, repository="fixture-repo",
                                      as_of=date(2026, 7, 14), wb=w)
    assert result.completed
    # every finding (if any) is confined to the scoped documents
    assert all(f.path in set(docs) for f in result.findings)
    # a doc-health action was recorded with a scoped reference
    assert w.data["action_history"][-1]["action"] == "doc-health"
    assert w.data["action_history"][-1]["reference"].startswith("health/scoped/")


def test_scoped_doc_health_finds_a_real_missing_status(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "bad.md").write_text("# No status header\n\nbody\n", encoding="utf-8")
    result = wb.run_scoped_doc_health(tmp_path, ["docs/bad.md"], repository="tmp",
                                      as_of=date(2026, 7, 14))
    families = {(f.family, f.rule) for f in result.findings}
    assert ("status-validity", "missing status header") in families


def test_scoped_doc_health_ignores_out_of_scope_docs(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "bad.md").write_text("# No status\n\nbody\n", encoding="utf-8")
    (tmp_path / "docs" / "good.md").write_text(
        "# Good\n\nStatus: brainstorm\nKind: brainstorm\n", encoding="utf-8")
    # scope to good.md only ⇒ bad.md's finding is not surfaced
    result = wb.run_scoped_doc_health(tmp_path, ["docs/good.md"], repository="tmp",
                                      as_of=date(2026, 7, 14))
    assert all(f.path == "docs/good.md" for f in result.findings)
