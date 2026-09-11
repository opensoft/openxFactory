"""openxFactory #793 — the ideation cross-reference projection's `Status:` line
is declared ONCE, so the two generators cannot disagree about it.

`ideation/cross-reference.md` carries `Status: projection`
(`docs/document-lifecycle.md`; `declare-generated-projection-status`,
2026-08-28, commit `fc788825`). Two code paths produce that file's content:
`scripts/render-ideation-cross-reference.py::render_markdown`, and
`doc_health/ideation_readiness.py::_render_markdown` — the path every
nightly/packet run actually writes through, reused by
`doc_health/derive_possibles.py::persist`.

The second one does not render. It loads WHICHEVER copy of the first the
`OPENXFACTORY_ROOT` env var or the ancestor walk resolves, so its `Status:`
line used to be as current as that snapshot and no more: a consuming repository
pinned before `fc788825` still emitted the superseded `Status: record`. PR #785
hit precisely that and hand-corrected the landed file.

WHAT THESE TESTS HOLD, and why each is here rather than one of them standing in
for the rest:

* the value reads `projection`, in the one place it is declared;
* the in-tree renderer no longer types it at all, so the declaration cannot be
  forked by editing one site;
* both paths, run against the real index in ONE process, produce byte-identical
  Markdown — drift is caught here rather than only when a stale pin is in play;
* a DELIBERATELY STALE renderer — the #785 condition, reconstructed — cannot
  regress the line, neither through `_render_markdown` nor through `persist()`
  on disk, and changes nothing else about the projection in the process.
"""

from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path

import pytest
import yaml

import projection_header as ph
from conftest import REPO_ROOT
from doc_health import ideation_readiness as ir
from import_scan import imported_modules, names_a_forbidden_package

RENDERER_REL = Path("scripts") / "render-ideation-cross-reference.py"
RENDERER = REPO_ROOT / RENDERER_REL
INDEX_YAML = REPO_ROOT / "ideation" / "cross-reference.yaml"
INDEX_MD = REPO_ROOT / "ideation" / "cross-reference.md"
DECLARATION = REPO_ROOT / "scripts" / "projection_header.py"
AS_OF = date(2026, 7, 9)

#: The status line as it stood BEFORE `fc788825`. Written out here, not built
#: from the module under test, because a fixture that derived the superseded
#: value from the canonical one could never be wrong about it — and being wrong
#: about it is the whole failure this file exists to catch.
SUPERSEDED_STATUS_LINE = "Status: record"

#: A pre-`fc788825` openxFactory checkout, reduced to the one function
#: `_render_markdown`'s lookup calls. This is the #785 condition made local and
#: deterministic: a resolvable renderer whose projection is stale.
STALE_RENDERER_SOURCE = (
    "def render_markdown(index):\n"
    "    lines = ['# Ideation Cross-Reference Readiness Index', '']\n"
    f"    lines.append({SUPERSEDED_STATUS_LINE!r})\n"
    "    lines.append('Kind: report')\n"
    "    lines.append('Repository context: openxFactory')\n"
    "    lines.append('')\n"
    "    for entry in index.get('topic_entries') or []:\n"
    "        lines.append('- ' + str(entry.get('id')))\n"
    "    return '\\n'.join(lines) + '\\n'\n"
)


def _load_renderer(path: Path):
    """The renderer at `path`, loaded the way `_render_markdown` loads it — by
    file location, not by import — so these tests exercise the real seam."""
    spec = importlib.util.spec_from_file_location(
        "_xref_renderer_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_stale_pin(root: Path) -> Path:
    """Lay down the stale checkout in the `OPENXFACTORY_ROOT` layout and return
    its root. Kept OUTSIDE any persist root by every caller, so a boundary
    allowlist assertion over the written tree stays honest."""
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / RENDERER_REL.name).write_text(
        STALE_RENDERER_SOURCE, encoding="utf-8")
    return root


def _status_line_of(markdown: str) -> str:
    """The header's status line, by prefix rather than by position: a test that
    read line 3 by index would go green on a projection whose header had
    quietly lost the line."""
    for line in markdown.split("\n")[:12]:
        if line.startswith("Status:"):
            return line
    return ""


def _real_index() -> dict:
    if not INDEX_YAML.is_file():  # pragma: no cover - present in every checkout
        pytest.skip(f"no {INDEX_YAML.relative_to(REPO_ROOT).as_posix()} "
                    f"in this checkout to render")
    return yaml.safe_load(INDEX_YAML.read_text(encoding="utf-8"))


# --- the declaration --------------------------------------------------------

def test_the_status_value_is_declared_once_and_reads_projection():
    """The projection is rewritten in place from the YAML on every run, so it
    has no captured state to be immutable against: `projection`, never
    `record` (`declare-generated-projection-status`, 2026-08-28)."""
    assert ph.PROJECTION_STATUS == "projection"
    assert ph.STATUS_LINE == "Status: projection"
    assert ph.STATUS_LINE != SUPERSEDED_STATUS_LINE


def test_the_in_tree_renderer_does_not_type_the_status_line_itself():
    """A second typed copy is a second place to edit, which is how the two
    generators came apart. The renderer emits `STATUS_LINE`; the string is not
    in its source at all."""
    source = RENDERER.read_text(encoding="utf-8")
    assert "Status:" not in source, (
        f"{RENDERER_REL.as_posix()} types a `Status:` line of its own — the "
        f"value is declared once, in "
        f"{DECLARATION.relative_to(REPO_ROOT).as_posix()} (#793)")
    assert "STATUS_LINE" in source


def test_the_declaration_imports_neither_package():
    """It sits beside `scripts/output_boundary.py`, in NEITHER package, and for
    the same reason: `doc_health` reaches it, and `doc_health` must not be made
    to reach `ideation_dashboard` to do so
    (`tests/doc-health/test_import_direction.py`)."""
    forbidden = ("doc_health", "scripts.doc_health",
                 "ideation_dashboard", "scripts.ideation_dashboard")
    offenders = [f"{DECLARATION.name}:{line} imports {module!r}"
                 for module, line in imported_modules(DECLARATION)
                 if names_a_forbidden_package(module, forbidden)]
    assert offenders == []


# --- the two paths agree ----------------------------------------------------

def test_both_generators_render_the_real_index_byte_identically(monkeypatch):
    """THE regression this file is named for. One process, one index, both
    paths — identical output, `Status:` line included. Drift in either site
    goes red here immediately, not months later when a stale pin happens to be
    reachable in someone else's repository."""
    index = _real_index()
    monkeypatch.setenv("OPENXFACTORY_ROOT", str(REPO_ROOT))

    direct = _load_renderer(RENDERER).render_markdown(index)
    delegated = ir._render_markdown(index)

    assert delegated is not None
    assert _status_line_of(direct) == ph.STATUS_LINE
    assert _status_line_of(delegated) == ph.STATUS_LINE
    assert delegated == direct


def test_the_committed_projection_carries_the_declared_status():
    """The landed artifact, not only the generators that write it."""
    if not INDEX_MD.is_file():  # pragma: no cover - present in every checkout
        pytest.skip("no committed projection in this checkout")
    assert _status_line_of(
        INDEX_MD.read_text(encoding="utf-8")) == ph.STATUS_LINE


# --- a stale pin cannot regress it ------------------------------------------

def test_a_stale_pinned_renderer_cannot_regress_the_status_line(
        tmp_path, monkeypatch):
    """The #785 condition: the lookup resolves a renderer that predates
    `fc788825`. Its `Status: record` is corrected — and NOTHING else about its
    projection is touched, which is what makes this a stamp and not a
    re-render."""
    monkeypatch.setenv(
        "OPENXFACTORY_ROOT", str(_write_stale_pin(tmp_path / "stale-pin")))
    index = {"topic_entries": [{"id": "cl-alpha"}, {"id": "cl-beta"}]}

    stale = _load_renderer(
        tmp_path / "stale-pin" / RENDERER_REL).render_markdown(index)
    assert _status_line_of(stale) == SUPERSEDED_STATUS_LINE  # the fixture IS stale

    stamped = ir._render_markdown(index)

    assert _status_line_of(stamped) == ph.STATUS_LINE
    assert SUPERSEDED_STATUS_LINE not in stamped
    assert stamped == stale.replace(SUPERSEDED_STATUS_LINE, ph.STATUS_LINE)


def test_persist_writes_the_declared_status_through_a_stale_renderer(
        tmp_path, monkeypatch):
    """Same condition, at the surface that lands files. `persist()` is the
    write path the nightly takes and the one `derive_possibles.persist` reuses,
    so the `.md` on disk carries the declared status whatever the lookup
    resolved."""
    monkeypatch.setenv(
        "OPENXFACTORY_ROOT", str(_write_stale_pin(tmp_path / "stale-pin")))
    root = tmp_path / "repo"
    index = {
        "schema_version": 1,
        "kind": ir.INDEX_KIND,
        "repository": "openxFactory",
        "generation": {"source_revision": "0" * 40,
                       "generator_version": ir.GENERATOR_VERSION},
        "topic_entries": [{"id": "cl-alpha"}],
    }
    meta = ir.ReadinessMeta(run_id="run-793", model="stub",
                            prompt_version=1, source_revision="0" * 40)

    written, boundary = ir.persist(index, meta, root=root, as_of=AS_OF)

    assert boundary.refusals == []
    assert written.get("md") == ir.INDEX_MD_REL
    md = (root / ir.INDEX_MD_REL).read_text(encoding="utf-8")
    assert _status_line_of(md) == ph.STATUS_LINE
    assert SUPERSEDED_STATUS_LINE not in md


# --- the stamp itself -------------------------------------------------------

def test_correct_markdown_passes_through_byte_identical():
    """A current renderer's output is returned unchanged — the stamp costs the
    happy path nothing and cannot perturb a projection that is already right."""
    index = _real_index()
    correct = _load_renderer(RENDERER).render_markdown(index)
    assert ph.apply_status_line(correct) == correct


def test_an_unreachable_renderer_still_skips_the_md():
    """`_render_markdown` answers None when nothing resolves and the `.md` write
    is skipped (the yaml stays the source of truth). The stamp preserves that
    fail-open rather than raising on it."""
    assert ph.apply_status_line(None) is None


def test_a_projection_with_no_status_header_gets_one():
    """Rather than landing headerless. Seated under the title block, ahead of
    the rest of the header."""
    stamped = ph.apply_status_line("# Title\n\nKind: report\n\nbody\n")
    assert stamped == f"# Title\n\n{ph.STATUS_LINE}\nKind: report\n\nbody\n"
    assert ph.apply_status_line(stamped) == stamped  # idempotent


def test_a_body_status_line_is_not_rewritten():
    """Only the HEADER is the stamp's business. A `Status:` far down the
    rendered body belongs to the content being projected."""
    body = "# Title\n\n" + ph.STATUS_LINE + "\n\n" + "x\n" * 20 + \
        SUPERSEDED_STATUS_LINE + "\n"
    assert ph.apply_status_line(body) == body
