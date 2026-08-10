"""US8 human authoring + agent create-only enforcement (T032, change 3.6/3.7):

  * the human create action (`authoring.create_scaffold`) writes a
    header-compliant skeleton (H1 with the ` — Brainstorm` suffix, the six
    required headers, a `## Possible feats` seed section) that ALSO passes
    the REAL doc-health machinery's status-validity/tag-hygiene families —
    "header-compliant" proven against the actual checker, not just field
    presence;
  * that skeleton is ABSENT from a snapshot generated before the create and
    PRESENT in one generated after (spec scenario 1: "appears in the next
    snapshot"), over the SAME tree (generate → create → regenerate);
  * scaffolding over an existing path refuses as SOURCE_EDIT (create-only,
    same semantics `boundary.create_document` already enforces for agents);
  * select-to-edit (`authoring.edit_target`/`edit_command`) resolves the path
    and a launch argv WITHOUT writing anything and WITHOUT executing anything
    itself — pure functions, asserted by absence of any subprocess/launch call;
  * the agent capture path (`authoring.agent_capture`) succeeds with complete
    headers, is REJECTED AND REPORTED (recorded on `boundary.refusals`, raised
    as `BoundaryViolation`) with incomplete headers, and its explicit
    edit/delete "attempts" (`agent_attempt_edit`/`agent_attempt_delete`) are
    ALWAYS rejected and reported — the module has no route that mutates or
    removes an existing corpus document;
  * "notebook set-removal semantics" — the LIFECYCLE PROJECTION case
    (distinct from the workbench `xf-wb-*` case T029 already covers): a
    source manually removed from a projection notebook (`xf-ideation`/
    `xf-drafts`/`xf-canon`) is restored on the NEXT
    `scripts/sync-notebooklm-books.py` run, proven against the REAL
    `sync_book` function (it recomputes each book's desired membership from
    the corpus's declared `Status:` header on every call, so a manual
    removal never survives a re-sync) — no new production code needed for
    this half of change 3.7; this test proves the existing script already
    satisfies it.
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import authoring, workbench as wb
from ideation_dashboard.boundary import (
    AGENT, HEADER_INCOMPLETE, HUMAN, SOURCE_DELETE, SOURCE_EDIT,
    BoundaryViolation, OutputBoundary,
)
from ideation_dashboard.generator import generate_snapshot

REQUIRED_HEADERS = ("Status:", "Kind:", "Summary:", "Topics:",
                    "Repository context:", "Captured:")


def _human_boundary(root: Path) -> OutputBoundary:
    return OutputBoundary(root, actor=HUMAN)


def _agent_boundary(root: Path) -> OutputBoundary:
    return OutputBoundary(root, actor=AGENT)


# ----------------------------------------------------------------------------
# human create action: header-compliant scaffold (spec scenario 1)
# ----------------------------------------------------------------------------

def test_scaffold_is_header_compliant_and_carries_the_brainstorm_suffix():
    text = authoring.render_scaffold(
        title="My New Idea", summary="A test idea worth capturing.",
        topics=["ideation-dashboard", "authoring"],
        repository_context="codexFactory",
    )
    assert text.startswith("# My New Idea — Brainstorm\n")
    for header in REQUIRED_HEADERS:
        assert header in text, f"missing required header {header!r}"
    assert "Status: brainstorm" in text
    assert "Topics: ideation-dashboard, authoring" in text
    assert "Repository context: codexFactory" in text
    assert authoring.missing_required_headers(text) == []
    # the openxFactory ideation/README.md seed section
    assert "## Possible feats" in text
    assert "- TODO" in text or "- " in text.split("## Possible feats", 1)[1]


def test_scaffold_title_already_carrying_the_suffix_is_not_doubled():
    text = authoring.render_scaffold(
        title="Already Suffixed — Brainstorm", summary="s", topics=["x"],
        repository_context="codexFactory",
    )
    assert text.startswith("# Already Suffixed — Brainstorm\n")
    assert "— Brainstorm — Brainstorm" not in text


def test_scaffold_carries_custom_possible_feats_bullets():
    text = authoring.render_scaffold(
        title="T", summary="s", topics=["x"], repository_context="codexFactory",
        possible_feats=["First candidate feat.", "Second candidate feat."],
    )
    body = text.split("## Possible feats", 1)[1]
    assert "- First candidate feat." in body
    assert "- Second candidate feat." in body


def test_scaffold_passes_the_real_doc_health_status_and_tag_hygiene_families(tmp_path):
    # "header-compliant" proven against the ACTUAL checker machinery, not just
    # our own header-presence scan.
    boundary = _human_boundary(tmp_path)
    written = authoring.create_scaffold(
        boundary, title="Doc Health Check", summary="Proves real compliance.",
        topics=["doc-health"], repository_context="codexFactory",
    )
    rel = written.relative_to(tmp_path).as_posix()
    result = wb.run_scoped_doc_health(tmp_path, [rel], repository="tmp-repo",
                                      as_of=date(2026, 7, 14))
    assert result.completed
    assert result.findings == []


# ----------------------------------------------------------------------------
# create-only: scaffolding over an existing path refuses (SOURCE_EDIT)
# ----------------------------------------------------------------------------

def test_create_scaffold_over_an_existing_path_is_refused_and_reported(tmp_path):
    boundary = _human_boundary(tmp_path)
    first = authoring.create_scaffold(
        boundary, title="Dup Title", summary="s1", topics=["x"],
        repository_context="codexFactory",
    )
    original = first.read_text(encoding="utf-8")

    with pytest.raises(BoundaryViolation) as exc:
        authoring.create_scaffold(
            boundary, title="Dup Title", summary="s2 — a rewrite attempt",
            topics=["y"], repository_context="codexFactory",
        )
    assert exc.value.refusal.kind == SOURCE_EDIT
    assert boundary.refusals[-1].kind == SOURCE_EDIT
    assert first.read_text(encoding="utf-8") == original  # untouched


def test_scaffold_relpath_is_a_safe_slug_under_the_chosen_area():
    assert authoring.scaffold_relpath("ideation/brainstorm/", "My New Idea!") == \
        "ideation/brainstorm/my-new-idea.md"
    assert authoring.scaffold_relpath("ideation/brainstorm", "Idea") == \
        "ideation/brainstorm/idea.md"


# ----------------------------------------------------------------------------
# the created doc appears in a REGENERATED snapshot, and not before
# ----------------------------------------------------------------------------

def test_created_doc_appears_only_in_a_regenerated_snapshot(tmp_path):
    (tmp_path / "ideation" / "brainstorm").mkdir(parents=True)
    pinned = "d" * 40

    before = generate_snapshot(tmp_path, "test-repo", source_revision=pinned)
    assert before["documents"] == []

    boundary = _human_boundary(tmp_path)
    written = authoring.create_scaffold(
        boundary, title="Newly Captured", summary="Appears next snapshot.",
        topics=["ideation-dashboard"], repository_context="codexFactory",
    )
    rel = written.relative_to(tmp_path).as_posix()

    # a snapshot object already in hand does NOT retroactively pick it up —
    # only a fresh generate() call scans the tree again.
    assert not any(d["id"] == rel for d in before["documents"])

    after = generate_snapshot(tmp_path, "test-repo", source_revision=pinned)
    ids = [d["id"] for d in after["documents"]]
    assert rel in ids
    doc = next(d for d in after["documents"] if d["id"] == rel)
    assert doc["stage"] == "brainstorm"
    assert doc["kind"] == "note"
    assert doc["summary"] == "Appears next snapshot."
    assert doc["topics"] == ["ideation-dashboard"]


# ----------------------------------------------------------------------------
# select-to-edit: pure resolution, no write, no execution
# ----------------------------------------------------------------------------

def test_edit_target_resolves_without_writing_anything(tmp_path):
    (tmp_path / "ideation" / "brainstorm").mkdir(parents=True)
    doc = tmp_path / "ideation" / "brainstorm" / "existing.md"
    doc.write_text("# Existing\n\nStatus: brainstorm\n", encoding="utf-8")
    before = doc.read_text(encoding="utf-8")

    resolved = authoring.edit_target(tmp_path, "ideation/brainstorm/existing.md")
    assert resolved == doc.resolve()
    assert doc.read_text(encoding="utf-8") == before  # untouched

    # listing every file under tmp_path before/after proves NOTHING new landed
    before_files = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*") if p.is_file())
    _ = authoring.edit_command(tmp_path, "ideation/brainstorm/existing.md")
    after_files = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*") if p.is_file())
    assert before_files == after_files


def test_edit_target_refuses_a_path_escaping_the_repo_root(tmp_path):
    with pytest.raises(ValueError, match="escapes the repository root"):
        authoring.edit_target(tmp_path, "../../etc/passwd")


def test_edit_command_uses_editor_override_else_xdg_open(tmp_path):
    (tmp_path / "ideation" / "brainstorm").mkdir(parents=True)
    doc = tmp_path / "ideation" / "brainstorm" / "d.md"
    doc.write_text("x", encoding="utf-8")

    argv = authoring.edit_command(tmp_path, "ideation/brainstorm/d.md")
    assert argv[0] == "xdg-open"
    assert argv[-1] == str(doc.resolve())

    argv2 = authoring.edit_command(tmp_path, "ideation/brainstorm/d.md", editor="code --wait")
    assert argv2[0] == "code"
    assert "--wait" in argv2
    assert argv2[-1] == str(doc.resolve())


# ----------------------------------------------------------------------------
# agent create-only capture: succeeds with complete headers, rejects incomplete
# ----------------------------------------------------------------------------

def test_agent_capture_succeeds_with_complete_headers_and_appears_next_snapshot(tmp_path):
    (tmp_path / "ideation" / "brainstorm").mkdir(parents=True)
    pinned = "e" * 40
    before = generate_snapshot(tmp_path, "agent-repo", source_revision=pinned)
    assert before["documents"] == []

    boundary = _agent_boundary(tmp_path)
    text = authoring.render_scaffold(
        title="Agent Captured", summary="An agent added this.",
        topics=["agent-capture"], repository_context="codexFactory",
    )
    written = authoring.agent_capture(
        boundary, path="ideation/brainstorm/agent-captured.md", text=text)
    assert written.read_text(encoding="utf-8") == text
    assert boundary.refusals == []

    after = generate_snapshot(tmp_path, "agent-repo", source_revision=pinned)
    assert "ideation/brainstorm/agent-captured.md" in [d["id"] for d in after["documents"]]


def test_agent_capture_rejects_and_reports_header_incomplete_submissions(tmp_path):
    boundary = _agent_boundary(tmp_path)
    incomplete = "# Agent Doc\n\nStatus: brainstorm\nKind: note\n"  # missing 4 headers
    with pytest.raises(BoundaryViolation) as exc:
        authoring.agent_capture(boundary, path="ideation/brainstorm/incomplete.md",
                                text=incomplete)
    assert exc.value.refusal.kind == HEADER_INCOMPLETE
    assert exc.value.refusal.actor == AGENT
    assert boundary.refusals[-1].kind == HEADER_INCOMPLETE
    for missing in ("Summary", "Topics", "Repository context", "Captured"):
        assert missing in exc.value.refusal.reason
    # nothing was written
    assert not (tmp_path / "ideation" / "brainstorm" / "incomplete.md").exists()


def test_missing_required_headers_reports_every_absent_field():
    assert authoring.missing_required_headers("# T\n\nStatus: brainstorm\n") == [
        "Kind", "Summary", "Topics", "Repository context", "Captured"]
    complete = authoring.render_scaffold(
        title="T", summary="s", topics=["x"], repository_context="codexFactory")
    assert authoring.missing_required_headers(complete) == []


def test_agent_capture_rejects_header_present_but_value_empty(tmp_path):
    # A doc whose required headers are all PRESENT but VALUE-EMPTY must NOT pass
    # the gate: the corpus parser (STATUS_RE requires a value) would read no
    # Status, and the generator would emit `stage: null`, failing the pinned
    # snapshot schema. The gate mirrors corpus semantics, so it refuses this.
    empty = ("# Empty Header Doc\n\nStatus:\nKind:\nSummary:\n"
             "Topics:\nRepository context:\nCaptured:\n")
    assert authoring.missing_required_headers(empty) == list(
        authoring.REQUIRED_HEADER_FIELDS)
    boundary = _agent_boundary(tmp_path)
    with pytest.raises(BoundaryViolation) as exc:
        authoring.agent_capture(boundary, path="ideation/brainstorm/empty.md", text=empty)
    assert exc.value.refusal.kind == HEADER_INCOMPLETE
    assert boundary.refusals[-1].kind == HEADER_INCOMPLETE
    assert not (tmp_path / "ideation" / "brainstorm" / "empty.md").exists()


def test_agent_capture_over_an_existing_path_is_rejected_and_reported(tmp_path):
    # an agent "capturing" a document at a path that already exists IS an
    # edit attempt — create-only semantics refuse it exactly like the human
    # path (spec "Agent create-only capture" scenario 2).
    boundary = _agent_boundary(tmp_path)
    text = authoring.render_scaffold(
        title="First", summary="s", topics=["x"], repository_context="codexFactory")
    existing = authoring.agent_capture(
        boundary, path="ideation/brainstorm/first.md", text=text)
    original = existing.read_text(encoding="utf-8")

    rewrite = authoring.render_scaffold(
        title="First", summary="rewritten", topics=["y"], repository_context="codexFactory")
    with pytest.raises(BoundaryViolation) as exc:
        authoring.agent_capture(boundary, path="ideation/brainstorm/first.md", text=rewrite)
    assert exc.value.refusal.kind == SOURCE_EDIT
    assert existing.read_text(encoding="utf-8") == original


# ----------------------------------------------------------------------------
# agent edit/delete "attempts" — ALWAYS rejected and reported (scenario 2)
# ----------------------------------------------------------------------------

def test_agent_attempt_edit_is_rejected_and_reported(tmp_path):
    (tmp_path / "ideation" / "brainstorm").mkdir(parents=True)
    doc = tmp_path / "ideation" / "brainstorm" / "existing.md"
    doc.write_text("# Existing\n\nStatus: brainstorm\n", encoding="utf-8")
    boundary = _agent_boundary(tmp_path)

    with pytest.raises(BoundaryViolation) as exc:
        authoring.agent_attempt_edit(boundary, "ideation/brainstorm/existing.md")
    assert exc.value.refusal.kind == SOURCE_EDIT
    assert exc.value.refusal.actor == AGENT
    assert boundary.refusals[-1].kind == SOURCE_EDIT
    assert doc.read_text(encoding="utf-8") == "# Existing\n\nStatus: brainstorm\n"


def test_agent_attempt_delete_is_rejected_and_reported(tmp_path):
    (tmp_path / "ideation" / "brainstorm").mkdir(parents=True)
    doc = tmp_path / "ideation" / "brainstorm" / "existing.md"
    doc.write_text("x", encoding="utf-8")
    boundary = _agent_boundary(tmp_path)

    with pytest.raises(BoundaryViolation) as exc:
        authoring.agent_attempt_delete(boundary, "ideation/brainstorm/existing.md")
    assert exc.value.refusal.kind == SOURCE_DELETE
    assert boundary.refusals[-1].actor == AGENT
    assert doc.exists()  # nothing deleted


def test_agent_boundary_constructor_tags_the_agent_actor(tmp_path):
    boundary = authoring.agent_boundary(tmp_path)
    assert boundary.actor == AGENT


# ----------------------------------------------------------------------------
# notebook set-removal semantics — the LIFECYCLE PROJECTION restore case
# (distinct from the workbench xf-wb-* case, already covered by test_workbench.py)
# ----------------------------------------------------------------------------

def _load_sync_notebooklm_books():
    script = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
    spec = importlib.util.spec_from_file_location("sync_notebooklm_books_authoring", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_lifecycle_projection_restores_a_manually_removed_source_on_next_sync(tmp_path):
    sync = _load_sync_notebooklm_books()
    doc_rel = "openxFactory/ideation/brainstorm/example.md"
    full = tmp_path / doc_rel
    full.parent.mkdir(parents=True)
    full.write_text("# Example — Brainstorm\n\nStatus: brainstorm\nKind: note\n",
                    encoding="utf-8")
    title = "[brainstorm] openxFactory: example"
    desired = {doc_rel: title}
    manifest: dict = {}

    def existing_empty(*args, parse=True):
        assert args[:2] == ("source", "list")
        return []

    add_calls: list[tuple] = []

    # split-ideation-book-per-repo: the projection's ideation book for
    # openxFactory, resolved by TITLE and addressed by notebook id.
    spec = sync.ideation_spec("openxFactory")
    book_id = "nb-ideation-openx"
    notebooks = [{"id": book_id, "title": spec.title}]

    def fake_nlm(existing_fn):
        def _fake(*args, parse=True):
            if args[:2] == ("notebook", "list"):
                return list(notebooks)
            if args[:2] == ("alias", "set"):
                return ""
            if args[:2] == ("source", "list"):
                return existing_fn()
            add_calls.append(args)
            return {"id": "src"}
        return _fake

    # first sync: the notebook is empty, so the source is added.
    with patch.object(sync, "nlm", fake_nlm(lambda: [])), \
            patch.object(sync.time, "sleep", lambda _s: None):
        sync.sync_book(tmp_path, spec, desired, manifest, True)
    assert any(c[:3] == ("source", "add", book_id) and title in c for c in add_calls)

    # a human manually removes the source from the notebook: the corpus
    # document and its declared Status: header are UNCHANGED, but the next
    # `source list` no longer returns it.
    add_calls.clear()
    with patch.object(sync, "nlm", fake_nlm(lambda: [])), \
            patch.object(sync.time, "sleep", lambda _s: None):
        sync.sync_book(tmp_path, spec, desired, manifest, True)

    # RESTORE: sync_book recomputes desired membership straight from the
    # corpus's declared lifecycle status on every run — never from a
    # "previously removed" memory — so the manually removed source is
    # re-added exactly as on first sync (spec "Notebook set-removal
    # semantics" scenario 2: "the next projection sync restores the set").
    assert any(c[:3] == ("source", "add", book_id) and title in c for c in add_calls)
    assert full.read_text(encoding="utf-8") == \
        "# Example — Brainstorm\n\nStatus: brainstorm\nKind: note\n"  # corpus untouched throughout
