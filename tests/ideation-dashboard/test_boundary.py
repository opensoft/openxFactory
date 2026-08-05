"""The interactivity boundary is the crux of the whole feature: every machinery
and agent write passes through it, and every refusal is reported, not silent
(spec 'Interactivity boundary'; FR-015/FR-018; SC-003/SC-006)."""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import boundary
from ideation_dashboard.boundary import (
    AGENT, MACHINERY, OUTSIDE_ALLOWLIST, OUTSIDE_ROOT,
    SOURCE_DELETE, SOURCE_EDIT, BoundaryViolation, HumanGate, OutputBoundary,
)


# ---- declared output-path allowlist ----

def test_output_write_under_allowlist_succeeds(tmp_path):
    b = OutputBoundary(tmp_path, ["out/"])
    p = b.write_output("out/snapshot.json", "{}\n")
    assert p == (tmp_path / "out" / "snapshot.json").resolve()
    assert p.read_text() == "{}\n"
    assert b.refusals == []


def test_output_write_outside_allowlist_is_rejected_and_reported(tmp_path):
    b = OutputBoundary(tmp_path, ["out/"])
    with pytest.raises(BoundaryViolation) as exc:
        b.write_output("ideation/staging/topic/README.md", "corrupt")
    # rejected...
    assert exc.value.refusal.kind == OUTSIDE_ALLOWLIST
    # ...AND reported: on the ledger and in the message.
    assert b.refusals and b.refusals[-1].kind == OUTSIDE_ALLOWLIST
    assert "output allowlist" in str(exc.value)
    assert not (tmp_path / "ideation").exists()  # no write landed


def test_output_write_escaping_root_is_rejected(tmp_path):
    b = OutputBoundary(tmp_path, ["out/"])
    with pytest.raises(BoundaryViolation) as exc:
        b.write_output("../escape.json", "x")
    assert exc.value.refusal.kind == OUTSIDE_ROOT
    assert b.refusals[-1].kind == OUTSIDE_ROOT


def test_bytes_and_text_both_write(tmp_path):
    b = OutputBoundary(tmp_path, ["out/"])
    assert b.write_output("out/a.bin", b"\x00\x01").read_bytes() == b"\x00\x01"
    assert b.write_output("out/b.txt", "hi").read_text() == "hi"


# ---- draft-organize must stay OUTSIDE ideation/staging/ ----

def test_draft_skeleton_outside_staging_is_permitted(tmp_path):
    b = OutputBoundary(tmp_path, ["ideation/workbench/"])
    p = b.permit_draft_skeleton("ideation/workbench/draft-topic/README.md")
    assert p.name == "README.md"


def test_draft_skeleton_into_staging_is_rejected(tmp_path):
    # Even if staging is (mistakenly) allowlisted, a draft skeleton into it is refused.
    b = OutputBoundary(tmp_path, ["ideation/staging/"])
    with pytest.raises(BoundaryViolation) as exc:
        b.permit_draft_skeleton("ideation/staging/topic/README.md")
    assert exc.value.refusal.kind == OUTSIDE_ALLOWLIST
    assert "outside ideation/staging/" in str(exc.value)


# ---- create-only corpus capture (human scaffold + agent capture) ----

def test_agent_create_new_document_succeeds(tmp_path):
    b = OutputBoundary(tmp_path, actor=AGENT)
    p = b.create_document("ideation/brainstorm/new-idea.md", "# New Idea\n")
    assert p.read_text() == "# New Idea\n"
    assert b.refusals == []


def test_create_document_is_deliberately_allowlist_independent(tmp_path):
    """INTENDED behaviour, asserted rather than silently relied on
    (add-workbench-bullseye-and-create design D10 consequence a, task 6.5):
    `create_document` does NOT consult the declared output allowlist, because
    its target is a SOURCE directory like `ideation/brainstorm/` — never a
    declared output path. The create-ONLY rule is the whole protection, and it
    is what the gated `create-document` verb relies on. The machinery OUTPUT
    path is unaffected: a write_output to the same directory is still refused,
    so the two paths stay distinct."""
    b = OutputBoundary(tmp_path, ["ideation/dashboard/gate-records/"])
    created = b.create_document("ideation/staging/topic-x/fragment.md", "# F\n")
    assert created.is_file() and b.refusals == []
    # the same location is NOT an allowed machinery output target
    with pytest.raises(BoundaryViolation) as exc:
        b.write_output("ideation/staging/topic-x/other.md", "x")
    assert exc.value.refusal.kind == OUTSIDE_ALLOWLIST
    # and containment still holds: a create outside the root is refused
    with pytest.raises(BoundaryViolation) as exc:
        b.create_document("../escape.md", "x")
    assert exc.value.refusal.kind == OUTSIDE_ROOT


def test_agent_edit_existing_document_via_create_is_rejected_and_reported(tmp_path):
    b = OutputBoundary(tmp_path, actor=AGENT)
    existing = tmp_path / "ideation" / "brainstorm" / "existing.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("# Original\n")
    with pytest.raises(BoundaryViolation) as exc:
        b.create_document("ideation/brainstorm/existing.md", "# Rewritten\n")
    assert exc.value.refusal.kind == SOURCE_EDIT
    assert b.refusals[-1].kind == SOURCE_EDIT
    assert existing.read_text() == "# Original\n"  # unchanged


def test_explicit_agent_edit_refusal_is_reported(tmp_path):
    b = OutputBoundary(tmp_path, actor=AGENT)
    doc = tmp_path / "ideation" / "brainstorm" / "d.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("x")
    with pytest.raises(BoundaryViolation) as exc:
        b.refuse_edit("ideation/brainstorm/d.md")
    assert exc.value.refusal.kind == SOURCE_EDIT
    assert b.refusals[-1].actor == AGENT


def test_explicit_agent_delete_refusal_is_reported(tmp_path):
    b = OutputBoundary(tmp_path, actor=AGENT)
    doc = tmp_path / "ideation" / "brainstorm" / "d.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("x")
    with pytest.raises(BoundaryViolation) as exc:
        b.refuse_delete("ideation/brainstorm/d.md")
    assert exc.value.refusal.kind == SOURCE_DELETE
    assert doc.exists()  # nothing deleted


# ---- human-only gates are a DISTINCT entrypoint, not a role flag ----

def test_machinery_boundary_has_no_gate_capability():
    # By construction: OutputBoundary carries no method that performs a gate
    # side effect — the only way to write a gate artifact is HumanGate.
    assert not hasattr(OutputBoundary, "write_gate_artifact")
    assert hasattr(HumanGate, "write_gate_artifact")


def test_human_gate_requires_an_identified_human(tmp_path):
    with pytest.raises(ValueError, match="identified human actor"):
        HumanGate(tmp_path, ["records/"], human_actor="")


def test_human_gate_writes_artifact_attributed_to_human(tmp_path):
    g = HumanGate(tmp_path, ["records/"], human_actor="brett")
    p = g.write_gate_artifact("records/ratify-001.yaml", "kind: gate-action-record\n")
    assert p.read_text().startswith("kind: gate-action-record")
    assert g.output.actor == "human:brett"


def test_human_gate_artifact_still_bound_by_allowlist(tmp_path):
    g = HumanGate(tmp_path, ["records/"], human_actor="brett")
    with pytest.raises(BoundaryViolation) as exc:
        g.write_gate_artifact("ideation/brainstorm/sneak.md", "not a record")
    assert exc.value.refusal.kind == OUTSIDE_ALLOWLIST


# ---- refusal reporting shape ----

def test_refusal_report_is_descriptive(tmp_path):
    b = OutputBoundary(tmp_path, ["out/"], actor=MACHINERY)
    with pytest.raises(BoundaryViolation) as exc:
        b.write_output("nope/x", "y")
    r = exc.value.refusal
    assert isinstance(r, boundary.Refusal)
    assert r.actor == MACHINERY and r.target == "nope/x"
    assert r.report() == str(exc.value)


# ---- the ONE rewrite allowance: an existing target inside a session worktree ----
#
# 007-workbench-branch-sessions T026 / FR-015. `create_document` above stays
# create-only for machinery and agents; this is a DIFFERENT method with a
# DIFFERENT precondition, and the precondition is a construction-time DECLARATION
# rather than a flag a caller can flip per call. The tests below are the shape
# `edit-document` (Phase 5) builds on.

def test_a_declared_session_worktree_may_rewrite_an_existing_document(tmp_path):
    worktree = tmp_path / "wt"
    (worktree / "ideation" / "staging" / "t").mkdir(parents=True)
    target = worktree / "ideation" / "staging" / "t" / "note.md"
    target.write_text("# original\n", encoding="utf-8")

    g = HumanGate(worktree, ["records/"], human_actor="brett",
                  session_root=worktree)
    written = g.rewrite_session_document("ideation/staging/t/note.md",
                                         "# rewritten\n")
    assert written == target.resolve()
    assert target.read_text(encoding="utf-8") == "# rewritten\n"
    assert g.session_root == worktree.resolve()


def test_without_a_declared_session_worktree_the_rewrite_is_refused(tmp_path):
    """No declaration, no allowance: an ordinary boundary keeps refusing an
    existing target, so no pre-existing caller gains rewrite power by accident."""
    target = tmp_path / "note.md"
    target.write_text("# original\n", encoding="utf-8")
    b = OutputBoundary(tmp_path, ["out/"])
    assert b.session_root is None

    with pytest.raises(BoundaryViolation) as exc:
        b.rewrite_session_document("note.md", "# rewritten\n")
    assert exc.value.refusal.kind == boundary.SESSION_REWRITE
    assert "DECLARED session worktree" in str(exc.value)
    assert target.read_text(encoding="utf-8") == "# original\n"
    assert b.refusals and b.refusals[-1].kind == boundary.SESSION_REWRITE


def test_a_target_outside_the_declared_worktree_is_refused_not_fallen_back(tmp_path):
    worktree = tmp_path / "wt"
    worktree.mkdir()
    outside = tmp_path / "served.md"
    outside.write_text("# main's copy\n", encoding="utf-8")

    b = OutputBoundary(tmp_path, ["out/"], session_root=worktree)
    with pytest.raises(BoundaryViolation) as exc:
        b.rewrite_session_document("served.md", "# rewritten\n")
    assert exc.value.refusal.kind == boundary.SESSION_REWRITE
    assert "never a fallback" in str(exc.value)
    assert outside.read_text(encoding="utf-8") == "# main's copy\n"


def test_the_rewrite_refuses_a_target_that_does_not_exist(tmp_path):
    """This path REWRITES. Bringing a document into existence stays the
    create-only create path, so the two can never be confused."""
    worktree = tmp_path / "wt"
    worktree.mkdir()
    b = OutputBoundary(tmp_path, ["out/"], session_root=worktree)
    with pytest.raises(BoundaryViolation) as exc:
        b.rewrite_session_document("wt/absent.md", "# new\n")
    assert exc.value.refusal.kind == SOURCE_EDIT
    assert not (worktree / "absent.md").exists()


@pytest.mark.parametrize("text", [None, "", "   \n"])
def test_a_delete_shaped_rewrite_is_refused(tmp_path, text):
    worktree = tmp_path / "wt"
    worktree.mkdir()
    target = worktree / "note.md"
    target.write_text("# original\n", encoding="utf-8")

    b = OutputBoundary(tmp_path, ["out/"], session_root=worktree)
    with pytest.raises(BoundaryViolation) as exc:
        b.rewrite_session_document("wt/note.md", text)
    assert exc.value.refusal.kind == SOURCE_DELETE
    assert "delete authority" in str(exc.value)
    assert target.read_text(encoding="utf-8") == "# original\n"


def test_the_rewrite_still_cannot_escape_the_repository_root(tmp_path):
    worktree = tmp_path / "wt"
    worktree.mkdir()
    b = OutputBoundary(worktree, ["out/"], session_root=worktree)
    with pytest.raises(BoundaryViolation) as exc:
        b.rewrite_session_document("../escape.md", "# rewritten\n")
    assert exc.value.refusal.kind == OUTSIDE_ROOT


def test_create_document_stays_create_only_even_with_a_session_declared(tmp_path):
    """The allowance is one METHOD, not a mode: declaring a session worktree does
    not relax `create_document`, which is what FR-018 keeps intact."""
    worktree = tmp_path / "wt"
    worktree.mkdir()
    target = worktree / "note.md"
    target.write_text("# original\n", encoding="utf-8")

    b = OutputBoundary(tmp_path, ["out/"], session_root=worktree)
    with pytest.raises(BoundaryViolation) as exc:
        b.create_document("wt/note.md", "# overwritten\n")
    assert exc.value.refusal.kind == SOURCE_EDIT
    assert target.read_text(encoding="utf-8") == "# original\n"


# ---- the two governed writes pin newline="" at the SOURCE (T104 F10 / FR-045) ----

def test_the_two_governed_write_sites_spell_newline_empty_at_the_source():
    """WEAK BY NECESSITY, and said out loud (wave re-review P3).

    `create_document` and `rewrite_session_document` both write with
    `newline=""` so the governed bytes land exactly as composed on EVERY
    platform (T104 F10 / FR-045). On Linux — the only platform this suite
    runs on — that argument is UNOBSERVABLE: `write_text`'s default
    translates "\\n" to `os.linesep`, and `os.linesep` here IS "\\n", so a
    revert produces byte-identical files and no behavioral test can go red.
    The regression would surface only on a Windows checkout, long after the
    revert merged. So this pin is textual — it greps the module source for
    the exact spelling at exactly the two governed write sites — because a
    grep is the strongest assertion this platform admits. If a third
    governed write site lands (count -> 3) or a revert drops one
    (count -> 2 becomes 1), the count forces the author to face this
    docstring and decide deliberately."""
    src = Path(boundary.__file__).read_text(encoding="utf-8")
    sites = src.count('write_text(text, encoding="utf-8", newline="")')
    assert sites == 2, (
        f"expected exactly the two governed write sites (create_document, "
        f"rewrite_session_document) to spell newline=\"\"; found {sites}")
