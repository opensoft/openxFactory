"""Session LIFECYCLE atomicity (PR #49 adversarial review findings 3, 4, 5, 6, 7
and 12) — one family, one discipline.

The shape underneath all six: **a session's durable artifacts and the durable
record that justifies them were not in one failure domain, and the signals a
fresh process reads back were not verified.**

  * **Finding 3 (High) — the OPEN.** `resolve_session` brings five durable
    artifacts into existence (branch, worktree, live registry entry, on-disk
    snapshot, NotebookLM notebook) BEFORE the fallible gate write, with no
    unwind. Every refusal after it returned "nothing was persisted" over a
    PHANTOM live session that blocked `propose`, was re-derived live by the next
    process, and made the create permanently unretryable — the retry JOINed the
    phantom and refused on the same existing target. `create-document` was also
    the ONE session subcommand skipping the CLI identity gate, so a blank
    `--actor` died with an uncaught traceback AFTER opening the session; the HTTP
    route had the same hole one layer down (a 500 from `HumanGate`).
  * **Finding 4 (High) — the ENDINGS, the mirror image.** `abandon-session` tore
    the session down and THEN wrote the record; a record-write failure returned a
    409 "refused" over a session that had in fact ended, and the human's reason —
    the one artifact FR-022 exists to produce — was gone forever, unretryable
    because liveness (the registry entry) had already been dropped.
  * **Finding 5 (High) — the BOOTSTRAP did not verify the joint signal.**
    `worktree_paths()` threw away git's `branch`/`detached`/`prunable` records, so
    the re-derivation asked "is there a directory?" and "does a branch by this
    dir-name-decoded name exist?" instead of asking git which branch that worktree
    HOLDS. A worktree sitting on another branch was registered as the session and
    the next gate action committed onto the wrong branch.
  * **Finding 6 (High) — a FAILED teardown came back live.** The residue of a
    contained `worktree remove` failure is directory + branch, which is exactly
    the shape the bootstrap read as live.
  * **Finding 7 (High) — HTTP and CLI disagreed about what tiles exist**, so G12's
    cross-tile protections were silently OFF on the CLI; and the abandoned-branch
    detector read local refs only, so a branch surviving on the REMOTE was forked
    over.
  * **Finding 12 (Medium-High) — the notebook import was not session-bound.**
    Covered in `tests/notebooklm/test_sync_notebooklm_books.py`, beside the script.

Every test here was written against the PRE-FIX production files and fails on
them. House rules hold throughout: scratch repos with LOCAL BARE remotes,
`FakePullRequests` / `FakeNotebookAdapter` at every seam, no network, no real
`gh`, no real `nlm` (`tests/hermeticity.py` makes both unreachable), no real
checkout touched, and no sleeps anywhere.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
import yaml

from session_fixtures import (
    FakeNotebookAdapter, build_scratch_repo,
)

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import session_git as sg
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
RECORDS = gc.DEFAULT_RECORDS_DIR

CREATE_BODY = {
    "title": "First Draft",
    "summary": "The session's first document.",
    "topics": ["alpha"],
    "area": f"ideation/staging/{TOPIC}/",
    "repository_context": REPO,
    "scope_kind": bs.STAGED_TOPIC,
    "scope_id": TOPIC,
}


# --------------------------------------------------------------------------
# helpers — the same shapes test_session_gates.py uses
# --------------------------------------------------------------------------

def _registry(repo, tmp_path, *, name="main-snapshot.json"):
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _create_raw(repo, registry, *, actor="brett", notebook=None, **over):
    return gr.run_gate_action(
        "create-document", {**CREATE_BODY, **over},
        checkout_root=repo.root, actor=actor, snapshot_path=None,
        session_registry=registry, repository=repo.repository,
        session_notebook=notebook)


def _create(repo, registry, **over):
    status, payload = _create_raw(repo, registry, **over)
    assert status == 200, payload
    return payload


def _cli_create(repo, *extra, actor="brett", area=None, title="First Draft"):
    return cli_mod.main([
        "gate", "create-document",
        "--repo-root", str(repo.root), "--actor", actor,
        "--title", title, "--summary", "The session's first document.",
        "--topics", "alpha", "--repository-context", REPO,
        "--area", area or f"ideation/staging/{TOPIC}/", *extra])


class SessionArtifacts:
    """The FIVE durable artifacts one OPEN brings into existence (finding 3).

    Asserting them as a set is the point: the review's reproduction found four of
    the five surviving a refusal, and a test that checked only the branch would
    have passed over a live registry entry and a real notebook."""

    def __init__(self, repo, registry, notebook=None, branch=DRAFT):
        self.repo, self.registry, self.notebook, self.branch = (
            repo, registry, notebook, branch)

    def snapshot(self):
        return bs.session_snapshot_path(self.repo.root, self.branch)

    def present(self) -> dict:
        git = sg.SessionGit(self.repo.root)
        worktree = bs.worktree_path(self.repo.root, self.branch)
        return {
            "branch": git.branch_exists(self.branch),
            "worktree": worktree.is_dir(),
            "git_knows_worktree": any(
                Path(p).resolve() == worktree.resolve()
                for p in git.worktree_paths()),
            "registry_entry": bs.is_live(self.registry, self.repo.repository,
                                         self.branch),
            "snapshot": self.snapshot().is_file(),
            "notebook": (tuple(self.notebook.live_aliases())
                         if self.notebook is not None else ()),
        }

    def assert_none(self):
        state = self.present()
        assert state == {"branch": False, "worktree": False,
                         "git_knows_worktree": False, "registry_entry": False,
                         "snapshot": False, "notebook": ()}, state

    def assert_all(self):
        state = self.present()
        assert state["branch"] and state["worktree"] and state["registry_entry"], \
            state


# ==========================================================================
# FINDING 3 — a refused FIRST create leaves no phantom session
# ==========================================================================

def test_an_existing_target_on_a_first_create_leaves_no_phantom_session(
        scratch_repo, tmp_path):
    """The review's repro A, inverted. A `create-document` whose target already
    exists refuses as SOURCE_EDIT — and used to leave the branch, the worktree,
    the live registry entry, the snapshot AND a real notebook behind."""
    scratch_repo.write(f"ideation/staging/{TOPIC}/first-draft.md",
                       "# First Draft\n\nStatus: brainstorm\n")
    scratch_repo.commit("A document with the create's target name",
                        f"ideation/staging/{TOPIC}/first-draft.md")
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    artifacts = SessionArtifacts(scratch_repo, registry, notebook)

    status, payload = _create_raw(scratch_repo, registry, notebook=notebook)

    assert status == 409, payload
    artifacts.assert_none()


def test_a_first_create_that_cannot_commit_is_retryable(scratch_repo, tmp_path,
                                                        monkeypatch):
    """The review's repro B, inverted: a commit failure left five artifacts AND a
    staged document+record, so the identical retry refused on the same existing
    target forever. The unwind must make the SAME command work next time."""
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    artifacts = SessionArtifacts(scratch_repo, registry, notebook)
    real_commit = sg.SessionGit.commit

    def refuse_once(self, worktree, message, **kw):
        monkeypatch.setattr(sg.SessionGit, "commit", real_commit)
        raise sg.GitError(("commit",), 1, "injected: the commit could not be made")

    monkeypatch.setattr(sg.SessionGit, "commit", refuse_once)
    status, payload = _create_raw(scratch_repo, registry, notebook=notebook)
    assert status == 409, payload
    artifacts.assert_none()

    # the IDENTICAL command, with nothing cleaned up by hand
    payload = _create(scratch_repo, registry, notebook=notebook)
    assert payload["ref"] == DRAFT
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_a_first_create_whose_record_cannot_be_written_leaves_nothing(
        scratch_repo, tmp_path, monkeypatch):
    """The record-write `OSError` arm. The document is byte-complete by then, so
    the unwind also has to remove a document git never tracked."""
    registry = _registry(scratch_repo, tmp_path)
    artifacts = SessionArtifacts(scratch_repo, registry)
    monkeypatch.setattr(
        gc, "write_gate_action_record",
        lambda *a, **k: (_ for _ in ()).throw(OSError("injected: read-only")))

    status, payload = _create_raw(scratch_repo, registry)

    assert status == 409, payload
    artifacts.assert_none()


def test_a_refusal_on_a_JOINED_session_leaves_it_live(scratch_repo, tmp_path):
    """The negative control, and the reason the unwind keys on `joined`: a
    refused SECOND create must leave the human's live session exactly as it was.
    Unwinding a JOIN would delete work the failing action does not own."""
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    artifacts = SessionArtifacts(scratch_repo, registry, notebook)
    first = _create(scratch_repo, registry, notebook=notebook)
    assert first["joined"] is False

    # the same title again: create-only refuses the existing target
    status, payload = _create_raw(scratch_repo, registry, notebook=notebook)

    assert status == 409, payload
    artifacts.assert_all()
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1
    assert notebook.live_aliases() == (bs.notebook_alias(REPO, DRAFT),)


def test_a_refusal_on_a_JOINED_session_LEVEL_WITH_MAIN_leaves_it_live(
        scratch_repo, tmp_path):
    """The DISCRIMINATOR the negative control above does not test (wave 2).

    `unwind_opened_session` has TWO guards — `joined` and commits-ahead — and the
    control's JOINed branch already carries one gate-action commit, so the
    commits-ahead guard alone saves it: the wave-2 critic deleted `or
    session.joined` and all eleven finding-3 tests stayed GREEN while a reachable
    state DESTROYED a live session.

    This is that state. The human resumed their own session and reset the branch
    back to `main` in their own shell (`git reset --hard main` inside the session
    worktree — an ordinary "start this draft again" gesture), so the session is
    LIVE with ZERO commits ahead. A create that then refuses JOINs it, and with
    only the commits-ahead guard the refusal force-removes the worktree and
    deletes the branch out from under them. `joined` is what says the failing
    action does not OWN this session."""
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    artifacts = SessionArtifacts(scratch_repo, registry, notebook)
    assert _create(scratch_repo, registry, notebook=notebook)["joined"] is False
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    git = sg.SessionGit(scratch_repo.root)

    # the human's own shell, inside their own live session
    subprocess.run(["git", "reset", "--hard", "main"], cwd=str(worktree),
                   check=True, capture_output=True)
    assert git.commits_ahead("main", DRAFT) == 0
    assert bs.is_live(registry, REPO, DRAFT) is True

    # a target that exists on main, brought into the session by a fast-forward, so
    # the next create refuses as SOURCE_EDIT on a JOIN with nothing ahead
    scratch_repo.write(f"ideation/staging/{TOPIC}/second-draft.md", "# taken\n")
    scratch_repo.commit("occupy a target on main",
                        f"ideation/staging/{TOPIC}/second-draft.md")
    subprocess.run(["git", "merge", "--ff-only", "main"], cwd=str(worktree),
                   check=True, capture_output=True)

    status, payload = _create_raw(scratch_repo, registry, notebook=notebook,
                                  title="Second Draft")

    assert status == 409, payload
    artifacts.assert_all()
    assert git.commits_ahead("main", DRAFT) == 0, (
        "the state under test: the guard that saves this session must be `joined`, "
        "because there is no commit for the commits-ahead guard to see")
    assert worktree.is_dir()
    assert bs.session_snapshot_path(scratch_repo.root, DRAFT).is_file()


def test_a_refused_first_create_does_not_block_propose(scratch_repo, tmp_path):
    """The review's repro E: the phantom held the tile against FR-023. `propose`
    afterwards must proceed, because there IS no session."""
    scratch_repo.write(f"ideation/staging/{TOPIC}/first-draft.md", "# taken\n")
    scratch_repo.commit("occupy the target",
                        f"ideation/staging/{TOPIC}/first-draft.md")
    registry = _registry(scratch_repo, tmp_path)

    assert _create_raw(scratch_repo, registry)[0] == 409

    status, payload = gr.run_gate_action(
        "propose", {"topic_id": TOPIC}, checkout_root=scratch_repo.root,
        actor="brett", snapshot_path=None, session_registry=registry,
        repository=scratch_repo.repository)
    assert status == 200, payload


def test_a_refused_first_create_is_not_re_derived_live_by_a_fresh_process(
        scratch_repo, tmp_path):
    """Finding 3 MANUFACTURES the residue finding 6 resurrects: with no unwind,
    the next process's FR-008 bootstrap read the leftover worktree+branch as a
    live session."""
    scratch_repo.write(f"ideation/staging/{TOPIC}/first-draft.md", "# taken\n")
    scratch_repo.commit("occupy the target",
                        f"ideation/staging/{TOPIC}/first-draft.md")
    registry = _registry(scratch_repo, tmp_path)
    assert _create_raw(scratch_repo, registry)[0] == 409

    fresh = reg.SnapshotRegistry()
    report = bs.bootstrap_sessions(fresh, repository=REPO,
                                   checkout_root=scratch_repo.root)

    assert report.branches == ()
    assert bs.is_live(fresh, REPO, DRAFT) is False


# ---- the notebook is created by the first COMMIT, never by the open ---------

def test_no_notebook_is_created_when_the_first_create_refuses(scratch_repo,
                                                              tmp_path):
    """FR-042's quota is SHARED and scarce, and a notebook created by a refused
    action had no local retire path at all — the human's own `nlm` was the only
    way back. Deferring the create to the first successful commit removes the
    leak by removing the window."""
    scratch_repo.write(f"ideation/staging/{TOPIC}/first-draft.md", "# taken\n")
    scratch_repo.commit("occupy the target",
                        f"ideation/staging/{TOPIC}/first-draft.md")
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()

    assert _create_raw(scratch_repo, registry, notebook=notebook)[0] == 409

    assert notebook.calls == []
    assert notebook.live_aliases() == ()


def test_the_notebook_carries_the_document_the_commit_landed(scratch_repo,
                                                             tmp_path):
    """The deferral is not merely safer, it is more correct: created AFTER the
    commit, the projection sees the document the action wrote instead of an
    empty worktree."""
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()

    payload = _create(scratch_repo, registry, notebook=notebook)

    alias = bs.notebook_alias(REPO, DRAFT)
    assert notebook.live_aliases() == (alias,)
    created = [c for c in notebook.calls if c[0] == "create"]
    assert len(created) == 1
    projected = {path for path, _text in created[0][2]}
    assert payload["path"] in projected, projected


# ---- FR-019: a blank actor is refused BEFORE any session mutation ----------

def test_the_cli_refuses_a_whitespace_actor_before_opening_anything(
        scratch_repo, tmp_path, capsys, fake_cli_notebook):
    """The review's repro C: `create-document` was the ONE session subcommand
    that skipped `_session_identity_gate`, so this died with an uncaught
    `ValueError` traceback — after the open."""
    artifacts = SessionArtifacts(scratch_repo, reg.SnapshotRegistry(),
                                 fake_cli_notebook)

    code = _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC, actor="   ")

    err = capsys.readouterr().err
    assert code == 1
    assert "create-document refused:" in err
    assert "Traceback" not in err
    artifacts.assert_none()


def test_the_route_refuses_a_whitespace_actor_before_opening_anything(
        scratch_repo, tmp_path):
    """The HTTP twin: `HumanGate` is constructed AFTER `resolve_session`, so a
    whitespace actor opened the session and then 500'd out of `serve.py`'s
    catch-all with the phantom left behind."""
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    artifacts = SessionArtifacts(scratch_repo, registry, notebook)

    status, payload = _create_raw(scratch_repo, registry, actor="   ",
                                  notebook=notebook)

    assert status == 403, payload
    assert "human actor" in payload["message"]
    artifacts.assert_none()


# ---- the CLI validates the body the ROUTE validates (parity) ---------------

def test_both_surfaces_refuse_an_area_that_escapes_ideation(scratch_repo,
                                                            tmp_path, capsys,
                                                            fake_cli_notebook):
    """Found during the PR #49 adjudication, adjacent to finding 7's divergence
    family: the CLI had no body validation at all, so `--area
    'ideation/staging/../../escape/'` — a 400 on the route — created and
    COMMITTED a document outside `ideation/` on the session branch."""
    escape = "ideation/staging/../../escape/"
    registry = _registry(scratch_repo, tmp_path)

    status, payload = _create_raw(scratch_repo, registry, area=escape)
    assert status == 400, payload
    assert "repo-relative ideation directory" in payload["message"]

    code = _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC, area=escape)
    err = capsys.readouterr().err

    assert code == 1
    assert "repo-relative ideation directory" in err
    assert not (scratch_repo.root.parent / "escape").exists()
    assert not sg.SessionGit(scratch_repo.root).branch_exists(DRAFT)


@pytest.mark.parametrize("area,relpath", [
    ("openspec/changes/", "openspec/changes/first-draft.md"),
    ("scripts/", "scripts/first-draft.md"),
    (".github/workflows/", ".github/workflows/first-draft.md"),
    ("escape/", "escape/first-draft.md"),
])
def test_both_surfaces_refuse_an_area_outside_ideation(scratch_repo, tmp_path,
                                                       capsys, fake_cli_notebook,
                                                       area, relpath):
    """The refusal message has always said "a repo-relative ideation directory"
    and only the TRAVERSAL half was enforced (PR #49 wave-2 critic): an area with
    no `..` and no leading `/` that simply is not under `ideation/` was ACCEPTED
    on both surfaces, so a dashboard create dialog could drop a document into the
    governed `openspec/changes/` tree."""
    registry = _registry(scratch_repo, tmp_path)

    status, payload = _create_raw(scratch_repo, registry, area=area)
    assert status == 400, payload
    assert "repo-relative ideation directory" in payload["message"]

    code = _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC, area=area)
    err = capsys.readouterr().err

    assert code == 1
    assert "repo-relative ideation directory" in err
    assert not (scratch_repo.root / relpath).exists()
    assert not sg.SessionGit(scratch_repo.root).branch_exists(DRAFT)


def test_both_surfaces_refuse_an_area_inside_the_gate_records_tree(
        scratch_repo, tmp_path, capsys, fake_cli_notebook):
    """The composite defect the wave-2 critic found: `ideation/dashboard/
    gate-records/` IS under `ideation/`, and it is the one prefix
    `served_checkout_fingerprint` excludes (plan Constraint 10). A document routed
    there reaches the served checkout through a merged session PR and can then be
    altered or deleted with SC-002's oracle reporting no change."""
    registry = _registry(scratch_repo, tmp_path)
    inside = sg.GATE_RECORDS_PREFIX

    for area in (inside, inside.rstrip("/"), inside + "draft-demo-topic/"):
        status, payload = _create_raw(scratch_repo, registry, area=area)
        assert status == 400, (area, payload)
        assert sg.GATE_RECORDS_PREFIX in payload["message"]
        assert "SC-002" in payload["message"]

    code = _cli_create(scratch_repo, "--scope-kind", "staged-topic",
                       "--scope-id", TOPIC, area=inside)
    err = capsys.readouterr().err

    assert code == 1
    assert sg.GATE_RECORDS_PREFIX in err
    assert not (scratch_repo.root / sg.GATE_RECORDS_PREFIX
                / "first-draft.md").exists()
    assert not sg.SessionGit(scratch_repo.root).branch_exists(DRAFT)


def test_the_fingerprint_would_not_see_a_document_in_the_records_prefix(
        scratch_repo):
    """WHY the area refusal above exists, as an assertion rather than a comment:
    the immovability oracle is blind inside the records prefix by design, and
    stays blind — so the confinement is the whole protection, not a second line
    of defence. The control one directory up proves the oracle itself works."""
    git = sg.SessionGit(scratch_repo.root)
    smuggled = f"{sg.GATE_RECORDS_PREFIX}smuggled-note.md"
    control = f"ideation/staging/{TOPIC}/control-note.md"
    for rel in (smuggled, control):
        scratch_repo.write(rel, "# A note\n\nStatus: brainstorm\n")
    scratch_repo.commit("two notes", smuggled, control)

    before = git.served_checkout_fingerprint()
    (scratch_repo.root / smuggled).write_text("tampered\n", encoding="utf-8")
    assert git.served_checkout_fingerprint() == before, \
        "the records prefix is excluded from the fingerprint (Constraint 10)"

    (scratch_repo.root / control).write_text("tampered\n", encoding="utf-8")
    assert git.served_checkout_fingerprint() != before


# ==========================================================================
# FINDING 4 — the ENDINGS are failure-atomic (the mirror image of finding 3)
# ==========================================================================

def _abandon(repo, registry, *, reason="the spike answered its question",
             actor="brett", notebook=None, **over):
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC, "reason": reason}
    body.update(over)
    return gr.run_gate_action(
        "abandon-session", body, checkout_root=repo.root, actor=actor,
        snapshot_path=None, session_registry=registry,
        repository=repo.repository, session_notebook=notebook)


def _save(repo, registry, *, pull_requests, actor="brett", **over):
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC}
    body.update(over)
    return gr.run_gate_action(
        "open-pr", body, checkout_root=repo.root, actor=actor, snapshot_path=None,
        session_registry=registry, repository=repo.repository,
        session_pull_requests=pull_requests)


def _abandon_records(repo):
    return sorted((repo.root / RECORDS).rglob(
        "abandon-session-*.gate-action.yaml"))


def _pr_records(repo):
    return sorted((repo.root / RECORDS).rglob("open-pr-*.gate-action.yaml"))


def _merge_on_main(repo, branch=DRAFT):
    """The Merge Master's action, EXTERNAL and with a real merge commit (D18).
    Raw git on purpose: merging is not a session operation (FR-030)."""
    repo.git("merge", "--no-ff", "-m", f"Merge {branch}", branch)
    return repo.head("main")


class _FailOnce:
    """A record write that fails the FIRST time and works afterwards — the
    read-only mount / full disk / permissions shape, made deterministic."""

    def __init__(self, monkeypatch, real):
        self.monkeypatch, self.real, self.fired = monkeypatch, real, False

    def __call__(self, gate, records_dir, record):
        if not self.fired:
            self.fired = True
            self.monkeypatch.setattr(gc, "write_gate_action_record", self.real)
            raise OSError("injected: [Errno 13] Permission denied")
        return self.real(gate, records_dir, record)


def test_an_abandon_whose_record_cannot_be_written_ends_nothing(
        scratch_repo, tmp_path, monkeypatch):
    """The review's reproduction, inverted. The teardown used to run FIRST and
    the record LAST, so a records tree that could not be written returned a 409
    "refused" over a session that had in fact ENDED — worktree gone, liveness
    dropped, notebook retired — with the human's reason lost for good and the
    retry structurally impossible (liveness IS the registry entry, FR-008)."""
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    _create(scratch_repo, registry, notebook=notebook)
    artifacts = SessionArtifacts(scratch_repo, registry, notebook)
    artifacts.assert_all()
    monkeypatch.setattr(gc, "write_gate_action_record",
                        _FailOnce(monkeypatch, gc.write_gate_action_record))

    status, payload = _abandon(scratch_repo, registry, notebook=notebook)

    assert status == 409, payload
    # NOTHING was ended: the fallible step now runs while the session is live
    artifacts.assert_all()
    assert notebook.live_aliases() == (bs.notebook_alias(REPO, DRAFT),)
    assert _abandon_records(scratch_repo) == []

    # and the IDENTICAL retry works, which is what "retryable" means
    status, payload = _abandon(scratch_repo, registry, notebook=notebook)
    assert status == 200, payload
    written = _abandon_records(scratch_repo)
    assert len(written) == 1
    assert yaml.safe_load(written[0].read_text(encoding="utf-8"))["reason"] == \
        "the spike answered its question"
    assert bs.is_live(registry, REPO, DRAFT) is False


def test_a_teardown_that_refuses_leaves_no_record_claiming_it_happened(
        scratch_repo, tmp_path, monkeypatch):
    """The other half of one failure domain: with the record written FIRST, a
    teardown that refuses must take the record with it, or the evidence series
    would carry an abandon of a session that is still live.

    The one test in this section that also passed pre-fix (where the teardown ran
    first and nothing had been written yet). It is here as the GUARD on the new
    ordering: it is the assertion that fails if record-first ever loses its
    compensation."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    artifacts = SessionArtifacts(scratch_repo, registry)

    def refuse(*a, **k):
        raise bs.SessionRefused("injected: the teardown refused")

    monkeypatch.setattr(bs, "teardown_session", refuse)
    status, payload = _abandon(scratch_repo, registry)

    assert status == 409, payload
    assert _abandon_records(scratch_repo) == []
    artifacts.assert_all()


def test_a_save_whose_record_fails_reports_the_pull_request_as_OPEN(
        scratch_repo, tmp_path, monkeypatch):
    """FR-029 mandates push -> open-or-update -> record, so a record-write
    failure leaves the REMOTE write done. Reporting it as a bare "refused" read
    as "nothing happened", which is the opposite of the truth."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = spr.FakePullRequests()
    monkeypatch.setattr(gc, "write_gate_action_record",
                        _FailOnce(monkeypatch, gc.write_gate_action_record))

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 409, payload
    message = payload["message"]
    assert "WAS pushed" in message and port.open_prs[DRAFT].url in message
    # the session is still LIVE and FR-032 makes the retry idempotent
    assert bs.is_live(registry, REPO, DRAFT) is True
    # the pending-dispatch marker holds the URL the record could not
    marker = bs.read_dispatch_marker(scratch_repo.root, DRAFT)
    assert marker and marker["url"] == port.open_prs[DRAFT].url


def _unwritable_dispatch_dir(repo):
    """Make the container's dispatch subdirectory unwritable — the CORRELATED
    failure, and the reachable one: the condition that stops the gate-records
    write (a read-only mount, a full filesystem, a permissions change) is
    routinely the same condition that stops the marker write."""
    folder = bs.dispatch_marker_path(repo.root, DRAFT).parent
    folder.mkdir(parents=True, exist_ok=True)
    folder.chmod(0o555)
    return folder


def test_a_save_that_can_write_neither_the_record_nor_the_marker_says_so(
        scratch_repo, tmp_path, monkeypatch):
    """Finding 4, wave 2 — THE FALSE PROMISE. `write_dispatch_marker` returned None
    by construction when it could not write, and the refusal text promised the
    marker UNCONDITIONALLY: "A pending-dispatch marker holds the URL meanwhile, so
    if the pull request merges first the ending finalizes the record from it". With
    both writes failing, that sentence was false, the FR-029 record was permanently
    lost, and the human was told it was recoverable — a reader who trusts it stops
    looking for the record. The attestation is the defect as much as the loss."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = spr.FakePullRequests()
    monkeypatch.setattr(gc, "write_gate_action_record",
                        _FailOnce(monkeypatch, gc.write_gate_action_record))
    folder = _unwritable_dispatch_dir(scratch_repo)
    try:
        status, payload = _save(scratch_repo, registry, pull_requests=port)
    finally:
        folder.chmod(0o755)

    assert status == 409, payload
    message = payload["message"]
    url = port.open_prs[DRAFT].url
    # the remote write still happened, and the message still says so
    assert "WAS pushed" in message and url in message
    # ... and it no longer promises a marker that is not there
    assert bs.read_dispatch_marker(scratch_repo.root, DRAFT) is None
    assert "NO pending-dispatch marker" in message
    assert "the FR-029 record is LOST" in message
    assert "holds the URL meanwhile" not in message
    # being the only copy, the message carries the whole record: url, ref, actor, at
    assert "only copy" in message
    assert DRAFT in message and "brett" in message


def test_a_save_that_can_write_the_marker_still_promises_it(scratch_repo,
                                                            tmp_path,
                                                            monkeypatch):
    """The other side of the same conditional: when the marker IS written the
    promise is true, and it must still be made — the recovery path is real and the
    human needs to know it exists. This is what keeps the fix from being a blanket
    downgrade of the message."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = spr.FakePullRequests()
    monkeypatch.setattr(gc, "write_gate_action_record",
                        _FailOnce(monkeypatch, gc.write_gate_action_record))

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 409, payload
    marker = bs.read_dispatch_marker(scratch_repo.root, DRAFT)
    assert marker and marker["url"] == port.open_prs[DRAFT].url
    assert "holds the URL meanwhile" in payload["message"]
    assert "NO pending-dispatch marker" not in payload["message"]


def test_an_unwritable_marker_never_blocks_a_record_that_can_be_written(
        scratch_repo, tmp_path):
    """The containment the marker's contract owes: it is a RECOVERY AID, so its
    failure must never be the reason a pull request the human already has cannot be
    recorded. With the marker directory unwritable but the records tree fine, the
    save SUCCEEDS and the FR-029 record lands."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = spr.FakePullRequests()
    folder = _unwritable_dispatch_dir(scratch_repo)
    try:
        status, payload = _save(scratch_repo, registry, pull_requests=port)
    finally:
        folder.chmod(0o755)

    assert status == 200, payload
    assert len(_pr_records(scratch_repo)) == 1
    assert payload["pull_request"] == port.open_prs[DRAFT].url


def test_the_marker_writer_reports_its_failure_with_the_records_content():
    """Structural: the writer must not degrade SILENTLY. It carries the reason and
    the three values the lost FR-029 record is made of, because when both writes
    fail nothing on disk can rebuild it and the refusal text is the only copy."""
    with pytest.raises(bs.DispatchNotRecorded) as caught:
        bs.write_dispatch_marker("/proc/definitely-not-writable", DRAFT,
                                 url="https://example.invalid/pr/1",
                                 at="2026-07-27T12:00:00Z", actor="brett")

    assert caught.value.url == "https://example.invalid/pr/1"
    assert caught.value.at == "2026-07-27T12:00:00Z"
    assert caught.value.actor == "brett"
    assert caught.value.reason


def test_the_merge_ending_finalizes_a_dispatch_whose_record_was_never_written(
        scratch_repo, tmp_path, monkeypatch):
    """The durable harm the review measured: the record write failed, the pull
    request MERGED before the human retried, and the merge ending then deleted
    the branch while ASSERTING a main-resident record that never existed. The
    dispatch is now finalized from the marker before anything is destroyed."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = spr.FakePullRequests()
    monkeypatch.setattr(gc, "write_gate_action_record",
                        _FailOnce(monkeypatch, gc.write_gate_action_record))
    assert _save(scratch_repo, registry, pull_requests=port)[0] == 409
    assert _pr_records(scratch_repo) == []
    _merge_on_main(scratch_repo)

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 200, payload
    assert payload["merged"] is True and payload["branch_deleted"] is True
    written = _pr_records(scratch_repo)
    assert len(written) == 1, written
    record = yaml.safe_load(written[0].read_text(encoding="utf-8"))
    assert record["target"]["ref"] == DRAFT
    assert record["artifacts"][0]["reference"] == port.open_prs[DRAFT].url
    assert payload["record"] == str(written[0].relative_to(scratch_repo.root))
    assert "finalized" in payload["hint"]
    # and the marker is consumed, so a later run does not write a second record
    assert bs.read_dispatch_marker(scratch_repo.root, DRAFT) is None


def test_the_merged_hint_does_not_claim_a_record_that_does_not_exist(
        scratch_repo, tmp_path):
    """A session merged without ever being saved through `open-pr` has NO
    main-resident record, and the response used to assert one 'stays on `main`
    and outlives the branch' while the same call deleted the branch."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    _merge_on_main(scratch_repo)

    status, payload = _save(scratch_repo, registry,
                            pull_requests=spr.FakePullRequests())

    assert status == 200, payload
    assert payload["merged"] is True
    assert _pr_records(scratch_repo) == []
    assert "NO main-resident `open-pr` record" in payload["hint"]
    assert "outlives the branch" not in payload["hint"]


# --------------------------------------------------------------------------
# critic finding C6 — the OTHER ending's half of the same custody gap
#
# Finding 4 followed the pending-dispatch marker to the MERGE ending. Nothing
# followed it to the abandon: the marker's four call sites were all on the
# open-pr/merge arm, `teardown_session` never read it, and the response never
# mentioned the pull request. So an abandon after a failed record write ended the
# session over an OPEN pull request that no gate-action record named anywhere —
# the custody gap FR-029's main-residence rule exists to close — and left it
# permanently orphaned on the vendor org.
# --------------------------------------------------------------------------

def test_the_abandon_ending_finalizes_the_same_interrupted_dispatch(
        scratch_repo, tmp_path, monkeypatch):
    """The reproduction, inverted. The dispatch is finalized from the marker at
    THIS ending too, the open pull request is NAMED, and the verb still closes
    nothing (FR-022, G9)."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = spr.FakePullRequests()
    monkeypatch.setattr(gc, "write_gate_action_record",
                        _FailOnce(monkeypatch, gc.write_gate_action_record))
    assert _save(scratch_repo, registry, pull_requests=port)[0] == 409
    assert _pr_records(scratch_repo) == []                 # no record anywhere
    url = port.open_prs[DRAFT].url
    calls_before = list(port.calls)

    status, payload = _abandon(scratch_repo, registry)

    assert status == 200, payload
    # the dispatch now has its FR-029 record, on `main`, naming the pull request
    written = _pr_records(scratch_repo)
    assert len(written) == 1, written
    record = yaml.safe_load(written[0].read_text(encoding="utf-8"))
    assert record["target"]["ref"] == DRAFT
    assert record["artifacts"][0]["reference"] == url
    assert record["artifacts"][0]["kind"] == gc.ART_PULL_REQUEST
    # ... and the response says so, rather than reporting "saved nothing" alone
    assert payload["pull_request"] == url
    assert payload["dispatch_record"] == str(written[0].relative_to(scratch_repo.root))
    assert url in payload["hint"]
    assert any(url in note for note in payload["notes"])
    # the abandon's OWN record is there too: one ending, both custodies
    assert len(_abandon_records(scratch_repo)) == 1
    # the marker is consumed, and the pull request itself was never touched
    assert bs.read_dispatch_marker(scratch_repo.root, DRAFT) is None
    assert port.calls == calls_before
    assert port.open_prs[DRAFT].url == url


def test_a_port_that_returns_no_url_records_nothing_and_says_so(scratch_repo,
                                                                tmp_path):
    """Tail finding B5. `find_open`'s JSON read and `open_or_update`'s create
    fallback both coerce a missing url to '', and that '' flowed into the record's
    `pull-request` reference — which the pinned schema requires NON-EMPTY. The save
    returned 200, told the human it had opened a pull request, and left an FR-029
    audit record naming NOTHING in the served corpus."""
    from ideation_dashboard import session_pr as spr

    class UrllessPullRequests(spr.FakePullRequests):
        def open_or_update(self, branch, **kw):
            super().open_or_update(branch, **kw)
            self.open_prs[branch] = spr.PullRequest(url="", number=0)
            return self.open_prs[branch]

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = UrllessPullRequests()

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 409, payload
    assert "returned NO url" in payload["message"]
    assert "WAS pushed" in payload["message"]              # honest: the push happened
    assert _pr_records(scratch_repo) == [], "no record naming nothing"
    assert bs.read_dispatch_marker(scratch_repo.root, DRAFT) is None
    assert bs.is_live(registry, REPO, DRAFT) is True        # and the retry is possible


def test_an_abandon_over_a_recorded_dispatch_still_names_the_open_pull_request(
        scratch_repo, tmp_path):
    """A marker that outlived a SUCCESSFUL save (its record already on `main`)
    finalizes nothing — there is nothing missing — but the abandon must still tell
    the human a pull request is open, because this ending cannot close it and the
    branch it lives on is retained."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    port = spr.FakePullRequests()
    assert _save(scratch_repo, registry, pull_requests=port)[0] == 200
    assert len(_pr_records(scratch_repo)) == 1
    url = port.open_prs[DRAFT].url
    bs.write_dispatch_marker(scratch_repo.root, DRAFT, url=url,
                             at="2026-07-27T12:00:00Z", actor="brett")

    status, payload = _abandon(scratch_repo, registry)

    assert status == 200, payload
    assert payload["pull_request"] == url
    assert payload["dispatch_record"] is None
    assert len(_pr_records(scratch_repo)) == 1, "no second open-pr record"
    assert any("is OPEN and this verb does not close it" in note
               for note in payload["notes"])


# ==========================================================================
# FINDING 5 — the bootstrap VERIFIES the joint worktree/branch signal
# ==========================================================================

def _bootstrap(repo, *, repository=REPO):
    fresh = reg.SnapshotRegistry()
    return fresh, bs.bootstrap_sessions(fresh, repository=repository,
                                        checkout_root=repo.root)


def _stale_kinds(report):
    return sorted(note.kind for note in report.stale)


def test_a_worktree_checked_out_onto_another_branch_is_not_the_session(
        scratch_repo, tmp_path):
    """FR-008 / G13: "the worktree and the branch are a JOINT signal". The
    bootstrap asked two INDEPENDENT questions — is there a directory, and does a
    branch by this directory's decoded name exist — and never asked git which
    branch the worktree HOLDS. Reproduced through the real CLI: the response and
    the main-resident evidence chain named `draft/demo-topic` while the commit
    and its gate-action record landed on another branch entirely."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    scratch_repo.git("branch", "somebody-elses-branch")
    subprocess.run(["git", "checkout", "-q", "somebody-elses-branch"],
                   cwd=str(worktree), check=True)

    fresh, report = _bootstrap(scratch_repo)

    assert report.branches == ()
    assert bs.is_live(fresh, REPO, DRAFT) is False
    assert bs.WORKTREE_ON_ANOTHER_BRANCH in _stale_kinds(report)
    note = next(n for n in report.stale
                if n.kind == bs.WORKTREE_ON_ANOTHER_BRANCH)
    assert "somebody-elses-branch" in note.reason and DRAFT in note.reason
    # and the LIVE path agrees with the bootstrap rather than contradicting it
    with pytest.raises(bs.SessionRefused):
        bs.open_session(sg.SessionGit(scratch_repo.root), reg.SnapshotRegistry(),
                        repository=REPO, tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root)


def test_a_detached_session_worktree_is_not_the_session(scratch_repo, tmp_path):
    """The other half-agreement failure: an interrupted rebase or bisect leaves a
    DETACHED HEAD, so the worktree holds no branch at all and a commit through it
    would be reachable from no ref."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)
    subprocess.run(["git", "checkout", "-q", "--detach"], cwd=str(worktree),
                   check=True)

    fresh, report = _bootstrap(scratch_repo)

    assert report.branches == ()
    assert bs.WORKTREE_DETACHED in _stale_kinds(report)
    assert bs.is_live(fresh, REPO, DRAFT) is False


# ==========================================================================
# FINDING 5, WAVE 2 — the LIVE path verifies the joint signal too
#
# Wave 1 taught the BOOTSTRAP to ask git which branch a worktree holds, and
# `open_session`'s adoption arm (`branch_present and directory_present`) to ask the
# same. Neither is the path a long-lived `serve` takes: with a registry entry
# already live, `open_session` returns from the REGISTRY and made no git call at
# all, and `commit_gate_action` never checked either. A registry entry records the
# branch/worktree pairing ONCE, at open, and nothing revokes it — so a worktree the
# human's own shell had moved took the action's commit onto whatever it held.
#
# Reproduced end to end before the fix: the commit and its FR-029 gate-action
# record landed on `somebody-elses-branch`, `draft/demo-topic` never moved, and the
# record ATTESTED `ref: draft/demo-topic`. That is FR-006's "exactly one commit on
# the session branch" and SC-003 both broken, with the evidence orphaned.
# ==========================================================================

def _drift_worktree(repo, *, branch=DRAFT, onto="somebody-elses-branch",
                    detach=False):
    """Move the session worktree off its branch, the way a human's shell does.

    No Python is patched and no git plumbing is hand-edited: this is
    `git checkout` inside the worktree, which is exactly the reachable cause."""
    worktree = bs.worktree_path(repo.root, branch)
    if detach:
        subprocess.run(["git", "checkout", "-q", "--detach"],
                       cwd=str(worktree), check=True)
    else:
        subprocess.run(["git", "checkout", "-q", "-b", onto],
                       cwd=str(worktree), check=True)
    return worktree


def _tips(repo, *refs):
    out = {}
    for ref in refs:
        done = subprocess.run(["git", "rev-parse", ref], cwd=str(repo.root),
                              text=True, capture_output=True)
        out[ref] = done.stdout.strip() if done.returncode == 0 else None
    return out


def test_a_warm_registry_join_refuses_a_drifted_worktree(scratch_repo, tmp_path):
    """The long-lived `serve`'s path. The registry entry stays live across the
    drift, so this JOIN is the arm that made no git call — and the refusal must
    arrive BEFORE the verb's engine authors anything into the wrong directory."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    assert bs.is_live(registry, REPO, DRAFT) is True
    _drift_worktree(scratch_repo)

    with pytest.raises(bs.SessionWorktreeDrifted) as caught:
        bs.open_session(sg.SessionGit(scratch_repo.root), registry,
                        repository=REPO, tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root)

    assert caught.value.kind == bs.WORKTREE_ON_ANOTHER_BRANCH
    assert caught.value.held == "somebody-elses-branch"
    # the refusal names the condition AND the remedy, and claims no cleanup
    assert "somebody-elses-branch" in str(caught.value)
    assert "checkout draft/demo-topic" in str(caught.value)
    assert "Nothing was written" in str(caught.value)


def test_a_detached_worktree_is_refused_on_the_warm_join_too(scratch_repo,
                                                             tmp_path):
    """The interrupted-rebase shape: the worktree holds NO branch, so a commit
    through it would be reachable from no ref at all."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    _drift_worktree(scratch_repo, detach=True)

    with pytest.raises(bs.SessionWorktreeDrifted) as caught:
        bs.open_session(sg.SessionGit(scratch_repo.root), registry,
                        repository=REPO, tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root)

    assert caught.value.kind == bs.WORKTREE_DETACHED
    assert "DETACHED" in str(caught.value)


def test_a_gate_action_refuses_a_worktree_that_drifted_after_the_join(
        scratch_repo, tmp_path):
    """The JOIN check cannot be the guarantee: the drift can happen in the window
    BETWEEN the join and the commit, and the CLI reaches the commit through the
    bootstrap rather than through that join at all. So the commit itself asks,
    inside the worktree's cross-process action lock, before any write.

    The pre-fix outcome this inverts: the commit landed on the drifted branch, its
    record went with it, and the record attested to a branch that never moved."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    assert session.joined is True
    before = _tips(scratch_repo, DRAFT)

    # the drift lands AFTER the join the action was authorized by
    worktree = _drift_worktree(scratch_repo)
    doc = f"ideation/staging/{TOPIC}/note.md"
    (worktree / doc).parent.mkdir(parents=True, exist_ok=True)
    (worktree / doc).write_text("# note\n\nStatus: draft\n", encoding="utf-8")
    at = "2026-07-27T12:00:00Z"
    stamp = bs.action_stamp(at)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=at, ref=DRAFT,
        document=doc, artifacts=[bs.commit_artifact(stamp)])
    gate = gc.HumanGate(worktree, [RECORDS, "ideation/staging/"],
                        human_actor="brett")

    with pytest.raises(bs.SessionWorktreeDrifted) as caught:
        bs.commit_gate_action(gate, git, worktree=worktree, branch=DRAFT,
                              record=record, documents=[doc], session=session)

    assert caught.value.kind == bs.WORKTREE_ON_ANOTHER_BRANCH
    assert stamp in str(caught.value)
    # NOTHING landed on either branch, and no record was written anywhere
    assert _tips(scratch_repo, DRAFT) == before
    assert _tips(scratch_repo, "somebody-elses-branch")[
        "somebody-elses-branch"] == before[DRAFT]
    # and THIS action's record was never written (the create's own record, from
    # the session's first commit, is legitimately there and stays untouched)
    assert [p.name for p in (worktree / RECORDS).rglob(f"*{stamp}*")] == []


def test_the_drift_refusal_uses_the_bootstraps_own_vocabulary(scratch_repo,
                                                              tmp_path):
    """The live path and the re-derivation must not invent two names for one
    condition: a human reading a refusal and a human reading the bootstrap's
    stale report have to recognise the same problem."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    _drift_worktree(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    worktree = bs.worktree_path(scratch_repo.root, DRAFT)

    _fresh, report = _bootstrap(scratch_repo)
    with pytest.raises(bs.SessionWorktreeDrifted) as caught:
        bs.assert_git_holds_branch(git, worktree, DRAFT, during="a probe")

    assert caught.value.kind in _stale_kinds(report)
    assert bs.worktree_drift(git, worktree, DRAFT) == bs.WORKTREE_ON_ANOTHER_BRANCH
    # and an UNDRIFTED worktree is not refused — the check is a validation, never
    # a second liveness derivation
    subprocess.run(["git", "checkout", "-q", DRAFT], cwd=str(worktree), check=True)
    assert bs.worktree_drift(git, worktree, DRAFT) is None
    bs.assert_git_holds_branch(git, worktree, DRAFT, during="a probe")


def test_a_gate_action_on_an_agreeing_worktree_still_commits(scratch_repo,
                                                             tmp_path):
    """The check must not cost the ordinary path anything: with the worktree on its
    own branch, the action commits exactly as before."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    worktree = Path(session.worktree)
    doc = f"ideation/staging/{TOPIC}/note.md"
    (worktree / doc).parent.mkdir(parents=True, exist_ok=True)
    (worktree / doc).write_text("# note\n\nStatus: draft\n", encoding="utf-8")
    at = "2026-07-27T12:00:00Z"
    stamp = bs.action_stamp(at)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=at, ref=DRAFT,
        document=doc, artifacts=[bs.commit_artifact(stamp)])
    gate = gc.HumanGate(worktree, [RECORDS, "ideation/staging/"],
                        human_actor="brett")

    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=DRAFT,
                                   record=record, documents=[doc],
                                   session=session)

    assert result.sha and result.branch == DRAFT
    assert _tips(scratch_repo, DRAFT)[DRAFT] == result.sha


def test_a_double_underscore_tile_id_is_one_session_not_two_stale_rows(
        scratch_repo, tmp_path):
    """The codec sub-claim. `flatten_branch` is not injective — `draft/foo__bar`
    and `draft/foo/bar` share the directory `draft__foo__bar`, and both spellings
    pass `looks_ref_legal` AND `git check-ref-format`. With a staging folder
    literally named `foo__bar` the bootstrap produced TWO CONTRADICTORY stale rows
    for one live session and told the human to delete a live worktree, and
    `propose` was then ALLOWED over the unmerged session (the exact D15 hazard).
    Reading the branch off git's porcelain removes the inverse entirely."""
    repo = build_scratch_repo(tmp_path / "world", topic_id="foo__bar")
    registry = _registry(repo, tmp_path)
    branch = "draft/foo__bar"
    status, payload = gr.run_gate_action(
        "create-document",
        {**CREATE_BODY, "scope_id": "foo__bar",
         "area": "ideation/staging/foo__bar/", "repository_context": repo.repository},
        checkout_root=repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=repo.repository)
    assert status == 200, payload

    fresh, report = _bootstrap(repo, repository=repo.repository)

    assert report.branches == (branch,)
    assert report.stale == (), report.summary()
    assert bs.is_live(fresh, repo.repository, branch) is True
    # and the FR-023 refusal the contradictory rows had disabled is back
    with pytest.raises(bs.LiveSessionRefused):
        bs.assert_no_live_session(fresh, repo.repository,
                                  bs.Tile(bs.STAGED_TOPIC, "foo__bar"))


# ==========================================================================
# FINDING 6 — a FAILED teardown is not resurrected as live
# ==========================================================================

def _lock_worktree(repo, branch=DRAFT):
    """`git worktree lock` — the plainest way to make `git worktree remove
    --force` refuse, with no Python patched at all. A read-only container, an
    in-use directory, and an NFS or permission failure all land in the same
    contained branch of `teardown_session`."""
    repo.git("worktree", "lock", str(bs.worktree_path(repo.root, branch)))


def test_an_abandon_whose_worktree_cannot_be_removed_stays_ended(
        scratch_repo, tmp_path):
    """The review's repro 6. `teardown_session` drops liveness first and CONTAINS
    a `worktree remove` failure into `notes`, so the residue is directory +
    branch — exactly the shape the bootstrap read as LIVE. A fresh process brought
    the ended session back: `propose` was re-blocked and the next gate write
    JOINED a session the human had ended."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    _lock_worktree(scratch_repo)

    status, payload = _abandon(scratch_repo, registry)

    assert status == 200, payload
    assert any("could not be removed" in note for note in payload["notes"])

    # A FRESH PROCESS: the residue must not read as a session
    fresh, report = _bootstrap(scratch_repo)
    assert report.branches == ()
    assert bs.is_live(fresh, REPO, DRAFT) is False
    assert bs.ENDED_SESSION_RESIDUE in _stale_kinds(report)
    # the ending is recorded as an ending, durably
    marker = bs.read_ending_marker(scratch_repo.root, DRAFT)
    assert marker and marker["ending"] == "abandon"
    # what that re-enables: `propose` proceeds, and a later write does NOT join
    bs.assert_no_live_session(fresh, REPO, bs.Tile(bs.STAGED_TOPIC, TOPIC))
    with pytest.raises(bs.EndedSessionResidue):
        bs.open_session(sg.SessionGit(scratch_repo.root), fresh, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root)


def test_a_merge_ending_whose_teardown_fails_stays_ended(scratch_repo, tmp_path):
    """The merge variant, which the Phase 6 note's rationale also did not cover:
    with the worktree still attached `git branch -D` refuses too, so FR-033's
    mandatory deletion silently does not happen and a MERGED session comes back
    live — re-enabling gate writes onto a branch whose pull request has merged."""
    from ideation_dashboard import session_pr as spr

    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    _save(scratch_repo, registry, pull_requests=spr.FakePullRequests())
    _merge_on_main(scratch_repo)
    _lock_worktree(scratch_repo)

    status, payload = _save(scratch_repo, registry,
                            pull_requests=spr.FakePullRequests())

    assert status == 200, payload
    assert payload["merged"] is True
    assert payload["branch_deleted"] is False        # git refuses, as it must

    fresh, report = _bootstrap(scratch_repo)
    assert report.branches == ()
    assert bs.ENDED_SESSION_RESIDUE in _stale_kinds(report)
    marker = bs.read_ending_marker(scratch_repo.root, DRAFT)
    assert marker and marker["ending"] == "merge"
    assert any("was not deleted" in item for item in marker["residue"])


def test_a_teardown_that_completes_records_no_ending_residue(scratch_repo,
                                                             tmp_path):
    """The control: an ending that finished leaves no marker, so the next OPEN on
    the tile is an ordinary open and never a refusal about residue."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)

    assert _abandon(scratch_repo, registry)[0] == 200

    assert bs.read_ending_marker(scratch_repo.root, DRAFT) is None
    fresh, report = _bootstrap(scratch_repo)
    assert report.branches == ()
    assert bs.ENDED_SESSION_RESIDUE not in _stale_kinds(report)
    assert bs.BRANCH_WITHOUT_WORKTREE in _stale_kinds(report)


def test_resuming_an_abandoned_branch_clears_the_ending(scratch_repo, tmp_path):
    """FR-025's RESUME re-materializes a worktree over the surviving branch, and
    that session is LIVE — the ending is a fact about the past, not about the
    present. Without this the marker would make every resumed session read as
    residue."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    _lock_worktree(scratch_repo)
    assert _abandon(scratch_repo, registry)[0] == 200
    assert bs.read_ending_marker(scratch_repo.root, DRAFT) is not None
    # the human does the cleanup the stale row asked for
    scratch_repo.git("worktree", "unlock", str(bs.worktree_path(scratch_repo.root,
                                                                DRAFT)))
    scratch_repo.git("worktree", "remove", "--force",
                     str(bs.worktree_path(scratch_repo.root, DRAFT)))

    fresh = reg.SnapshotRegistry()
    bs.bootstrap_sessions(fresh, repository=REPO, checkout_root=scratch_repo.root)
    resumed = bs.open_session(sg.SessionGit(scratch_repo.root), fresh,
                              repository=REPO, tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root,
                              continuation=bs.CONTINUATION_RESUME)

    assert resumed.branch == DRAFT and resumed.joined is False
    assert bs.read_ending_marker(scratch_repo.root, DRAFT) is None
    later, report = _bootstrap(scratch_repo)
    assert report.branches == (DRAFT,), report.summary()


# ==========================================================================
# FINDING 6, WAVE 2 — an ending that cannot be made DURABLE does not happen
#
# The tests above prove the marker keeps an ending ended. They all assume the
# marker could be WRITTEN. `write_ending_marker` swallowed `OSError` and returned
# None, `teardown_session` proceeded regardless, and it then appended a note
# asserting the ending "is recorded as ENDED for every later process: <branch> is
# NOT live and will not be re-derived as live" — over a marker that did not exist.
#
# The replay pass reproduced the ORIGINAL finding-6 harm verbatim through the
# CORRELATED failure, which is the reachable one: the condition that makes
# `git worktree remove` fail (an unwritable or full container) is the same
# condition that makes the marker unwritable. The teardown reported success, the
# bootstrap re-derived the session as LIVE, a later write JOINED it, and the note
# said the opposite. A best-effort write cannot carry an ending guarantee.
#
# So the ending is made durable FIRST, before anything is destroyed, and an ending
# that cannot be recorded is REFUSED over a session that is still live.
# ==========================================================================

def _unwritable_ending_dir(repo, branch=DRAFT):
    """Make the container's `session-ended/` subdirectory unwritable — the review's
    own correlated injection, with no Python patched."""
    folder = bs.ending_marker_path(repo.root, branch).parent
    folder.mkdir(parents=True, exist_ok=True)
    folder.chmod(0o555)
    return folder


def test_an_ending_that_cannot_be_recorded_is_refused_and_ends_nothing(
        scratch_repo, tmp_path):
    """The critic's reproduction, inverted. Both failures at once — the worktree
    cannot be removed AND the marker cannot be written — which is one root cause.
    Pre-fix: `torn_down` reported the registry entry, the note claimed the ending
    was durable, the bootstrap re-derived `draft/demo-topic` as LIVE, and a later
    `open_session` JOINED it. Now the ending refuses BEFORE the first destructive
    step, so there is no state in which a response claims an ending that did not
    persist."""
    registry = _registry(scratch_repo, tmp_path)
    notebook = FakeNotebookAdapter()
    _create(scratch_repo, registry, notebook=notebook)
    artifacts = SessionArtifacts(scratch_repo, registry, notebook)
    _lock_worktree(scratch_repo)
    folder = _unwritable_ending_dir(scratch_repo)
    try:
        git = sg.SessionGit(scratch_repo.root)
        session = bs.open_session(git, registry, repository=REPO,
                                  tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                                  checkout_root=scratch_repo.root)

        with pytest.raises(bs.EndingNotDurable) as caught:
            bs.teardown_session(git, session, checkout_root=scratch_repo.root,
                                registry=registry, notebook=notebook,
                                ending="abandon")

        # the refusal's OWN claim is true: nothing was torn down
        artifacts.assert_all()
        assert notebook.live_aliases() == (bs.notebook_alias(REPO, DRAFT),)
        assert "NOTHING was torn down" in str(caught.value)
        assert "still live and still joinable" in str(caught.value)
    finally:
        folder.chmod(0o755)

    # and a fresh process agrees with the refusal rather than contradicting it:
    # the session IS live, because it never ended
    fresh, report = _bootstrap(scratch_repo)
    assert report.branches == (DRAFT,), report.summary()
    assert bs.is_live(fresh, REPO, DRAFT) is True


def test_the_ending_marker_is_written_before_the_teardown_destroys_anything(
        scratch_repo, tmp_path):
    """The ORDERING is the fix, so it is asserted directly. The marker used to be
    written last, in exactly the world where it fails; it is now the first step, so
    its durability is established while the session is still intact and refusing is
    still possible."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    seen = {}
    real_remove = sg.SessionGit.worktree_remove

    def observing_remove(self, path):
        # the first destructive step: what did the container already hold?
        seen["marker"] = bs.read_ending_marker(scratch_repo.root, DRAFT)
        seen["live"] = bs.is_live(registry, REPO, DRAFT)
        return real_remove(self, path)

    sg.SessionGit.worktree_remove = observing_remove
    try:
        torn = bs.teardown_session(git, session, checkout_root=scratch_repo.root,
                                   registry=registry, ending="abandon")
    finally:
        sg.SessionGit.worktree_remove = real_remove

    assert seen["marker"] and seen["marker"]["ending"] == "abandon"
    # ... and liveness was already dropped by then, which is why the marker has to
    # come first: from that instant there is nothing left to refuse with
    assert seen["live"] is False
    # the teardown completed, so the reservation is cleared again
    assert bs.read_ending_marker(scratch_repo.root, DRAFT) is None
    assert bs.TORN_WORKTREE in torn.torn_down


def test_a_refused_compare_and_swap_leaves_no_ending_marker(scratch_repo,
                                                            tmp_path):
    """The reservation must not fire for a teardown that never happens. FR-033's
    compare-and-swap refuses when the tip moved under the verdict, and a marker
    left behind there would make a LIVE session unjoinable — the mirror of the bug
    being fixed."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)

    with pytest.raises(bs.SessionRefused):
        bs.teardown_session(git, session, checkout_root=scratch_repo.root,
                            registry=registry, delete_branch=True,
                            expect_branch_sha="0" * 40, ending="merge")

    assert bs.read_ending_marker(scratch_repo.root, DRAFT) is None
    assert bs.is_live(registry, REPO, DRAFT) is True


def test_an_unwound_open_reports_an_undurable_ending_instead_of_raising(
        scratch_repo, tmp_path, monkeypatch):
    """`unwind_opened_session` REPORTS (finding 3's contract): it must never replace
    the caller's own refusal with a different exception. An ending that cannot be
    made durable tore nothing down, so its note says the session survives — which
    is the truth, and is what the caller's refusal then tells the human."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    # the shape `unwind_opened_session` acts on: a session this call OPENED, whose
    # first gate action has not committed anything yet
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    assert session.joined is False
    folder = _unwritable_ending_dir(scratch_repo)
    try:
        notes = bs.unwind_opened_session(git, session,
                                         checkout_root=scratch_repo.root)
    finally:
        folder.chmod(0o755)

    assert len(notes) == 1
    assert "could not be made durable" in notes[0]
    assert "still there" in notes[0]
    # nothing was unwound, which is what the note says
    assert bs.is_live(registry, REPO, DRAFT) is True
    assert git.branch_exists(DRAFT) is True


def test_a_residue_detail_that_cannot_be_added_does_not_unsay_the_ending(
        scratch_repo, tmp_path, monkeypatch):
    """The one write that stays best-effort, and why that is now safe: the ending is
    already durable from the reservation, so a failed residue REWRITE costs the
    human the residue list and nothing else. The notes say exactly that — no claim
    that the ending failed, and no claim the detail was recorded."""
    registry = _registry(scratch_repo, tmp_path)
    _create(scratch_repo, registry)
    _lock_worktree(scratch_repo)
    real = bs.write_ending_marker
    calls = {"n": 0}

    def fail_the_rewrite(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:                     # the reservation SUCCEEDS
            return real(*args, **kwargs)
        raise bs.EndingNotDurable(DRAFT, bs.ending_marker_path(
            scratch_repo.root, DRAFT), "injected: [Errno 28] No space left")

    monkeypatch.setattr(bs, "write_ending_marker", fail_the_rewrite)
    status, payload = _abandon(scratch_repo, registry)

    assert status == 200, payload
    notes = " ".join(payload["notes"])
    assert "residue detail could not be added" in notes
    assert "the ending itself is recorded and holds" in notes
    # and it IS recorded: the reservation is on disk and keeps the session ended
    marker = bs.read_ending_marker(scratch_repo.root, DRAFT)
    assert marker and marker["ending"] == "abandon"
    fresh, report = _bootstrap(scratch_repo)
    assert report.branches == ()
    assert bs.ENDED_SESSION_RESIDUE in _stale_kinds(report)


# ==========================================================================
# FINDING 7 — one tile inventory for both surfaces, and a union-backed
# abandoned-branch detector
# ==========================================================================

def _cluster_world(tmp_path, *, name="cross-tile"):
    """A checkout carrying BOTH tile `cl-foo` and tile `cl-foo-2`, so the two
    directions of the G12 ambiguity are both live: `cluster/cl-foo-2` is tile
    `cl-foo-2`'s FIRST branch and tile `cl-foo`'s SECOND."""
    repo = build_scratch_repo(tmp_path / name)
    repo.write("ideation/staging/seed/notes.md",
               "# Seed\n\nStatus: staged\nKind: reference\n"
               "Summary: seeds two cluster tiles.\nTopics: foo, foo-2\n"
               "Repository context: openxFactory\nCaptured: 2026-07-27\n\n"
               "Body long enough to be a document.\n")
    repo.write("ideation/cross-reference.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "ideation-cross-reference",
        "repository": repo.repository,
        "generation": {"source_revision": "e" * 40, "generator_version": "test"},
        "possibles_register": [
            {"id": "pos-bar", "title": "Bar", "claim": "c", "state": "latent"},
            {"id": "pos-bar-2", "title": "Bar 2", "claim": "c", "state": "latent"},
        ],
    }, sort_keys=False))
    repo.commit("two cluster tiles and two possible tiles",
                "ideation/staging/seed/notes.md", "ideation/cross-reference.yaml")
    return repo


def test_the_tile_inventory_is_the_same_on_both_surfaces(tmp_path):
    """The route held the cluster/possible ids only because it happened to hold a
    served snapshot, and every CLI session verb passed None — so the SAME checkout
    yielded two different tile universes and G12's exclusions were silently OFF on
    the CLI (FR-020's parity promise, broken in the destructive direction)."""
    repo = _cluster_world(tmp_path)

    cli_side = gr.discover_tile_inventory(repo.root)           # no snapshot
    http_side = gr.discover_tile_inventory(
        repo.root, json.loads(json.dumps(generate_snapshot(repo.root,
                                                           repo.repository))))

    assert set(cli_side.tiles) == set(http_side.tiles)
    ids = {(t.scope_kind, t.scope_id) for t in cli_side.tiles}
    assert {(bs.CLUSTER, "cl-foo"), (bs.CLUSTER, "cl-foo-2"),
            (bs.POSSIBLE, "pos-bar"), (bs.POSSIBLE, "pos-bar-2")} <= ids


def test_a_cluster_write_does_not_join_another_tiles_session_through_the_cli(
        tmp_path, capsys, fake_cli_notebook):
    """The reproduced cross-tile JOIN: with tile `cl-foo-2`'s session LIVE, a gate
    write on tile `cl-foo` resolved onto `cluster/cl-foo-2` and committed one
    tile's documents and gate-action records onto ANOTHER tile's session. Refused
    on the HTTP inventory, permitted on the CLI's."""
    repo = _cluster_world(tmp_path)

    def cli(scope_id, title):
        return cli_mod.main([
            "gate", "create-document", "--repo-root", str(repo.root),
            "--actor", "brett", "--title", title,
            "--summary", "A cluster tile's document.", "--topics", "alpha",
            "--repository-context", repo.repository,
            "--area", "ideation/staging/seed/",
            "--scope-kind", bs.CLUSTER, "--scope-id", scope_id])

    assert cli("cl-foo-2", "The Ordinal Tile") == 0
    capsys.readouterr()

    assert cli("cl-foo", "The Base Tile") == 0
    capsys.readouterr()

    git = sg.SessionGit(repo.root)
    # each tile got its OWN session and its OWN commit. Pre-fix, tile `cl-foo`
    # resolved onto `cluster/cl-foo-2` and its document and gate-action record
    # committed onto the OTHER tile's session branch, which never existed.
    assert git.branch_exists("cluster/cl-foo") is True
    assert git.commits_ahead("main", "cluster/cl-foo") == 1
    assert git.commits_ahead("main", "cluster/cl-foo-2") == 1


def test_the_cross_tile_collision_refuses_through_the_cli(tmp_path, capsys,
                                                          fake_cli_notebook):
    """The other direction of the same G12 ambiguity: `cluster/cl-foo-2` is tile
    `cl-foo-2`'s FIRST branch AND tile `cl-foo`'s SECOND. When it already exists,
    opening tile `cl-foo-2` over it cannot be attributed to one tile and MUST
    refuse naming BOTH — and it did, on HTTP, while the CLI's empty exclusion set
    made `collision_owner` return None and the branch was joined silently."""
    repo = _cluster_world(tmp_path)
    repo.git("branch", "cluster/cl-foo-2")            # tile cl-foo's ordinal 2

    code = cli_mod.main([
        "gate", "create-document", "--repo-root", str(repo.root),
        "--actor", "brett", "--title", "The Ordinal Tile",
        "--summary", "A cluster tile's document.", "--topics", "alpha",
        "--repository-context", repo.repository,
        "--area", "ideation/staging/seed/",
        "--scope-kind", bs.CLUSTER, "--scope-id", "cl-foo-2"])
    err = capsys.readouterr().err

    assert code == 1
    assert "is both the deterministic session branch of tile" in err
    assert "'cl-foo-2'" in err and "'cl-foo'" in err


def test_a_cleanup_cannot_delete_another_tiles_branch_through_the_cli(tmp_path,
                                                                      capsys):
    """The reproduced cross-tile DELETE, the other direction of the same
    ambiguity: `assert_branch_cleanup_permitted` admitted
    `git branch -D cluster/cl-foo-2` on behalf of tile `cl-foo` whenever the
    exclusion set was empty."""
    repo = _cluster_world(tmp_path)
    repo.git("branch", "cluster/cl-foo-2")
    repo.write("ideation/cross-reference.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "ideation-cross-reference",
        "repository": repo.repository,
        "generation": {"source_revision": "e" * 40, "generator_version": "test"},
        "possibles_register": [
            {"id": "pos-bar", "title": "Bar", "claim": "c", "state": "picked",
             "pick": {"staging_id": "cl-foo", "change_id": "add-foo"}},
            {"id": "pos-bar-2", "title": "Bar 2", "claim": "c", "state": "latent"},
        ],
    }, sort_keys=False))
    repo.write("openspec/changes/add-foo/proposal.md", "# Why\n\nLanded.\n")
    repo.commit("land a proposal on cl-foo", "ideation/cross-reference.yaml",
                "openspec/changes/add-foo/proposal.md")

    code = cli_mod.main([
        "gate", "cleanup-abandoned-branch", "--repo-root", str(repo.root),
        "--actor", "brett", "--scope-kind", bs.CLUSTER, "--scope-id", "cl-foo",
        "--ref", "cluster/cl-foo-2"])
    err = capsys.readouterr().err

    assert code == 1
    assert "is not a session branch of tile" in err
    assert sg.SessionGit(repo.root).branch_exists("cluster/cl-foo-2") is True


def test_a_branch_that_survives_only_on_the_remote_is_reported_not_forked(
        scratch_repo, tmp_path):
    """The abandoned-branch detector read LOCAL refs and the BASE NAME only, while
    the union-and-family helper written for the job had no production caller. A
    branch machine A had pushed was invisible here, so `open_session` forked a
    DIVERGENT local branch of the same name over its work — with no resume-or-new
    report, and `push` then dead-ended non-fast-forward."""
    registry = _registry(scratch_repo, tmp_path)
    scratch_repo.add_remote_only_branch(DRAFT)
    git = sg.SessionGit(scratch_repo.root)
    assert git.branch_exists(DRAFT) is False          # local: nothing at all

    with pytest.raises(bs.AbandonedBranchSurvives) as caught:
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root,
                        inventory=gr.discover_tile_inventory(scratch_repo.root))

    assert caught.value.remote_only == (DRAFT,)
    assert "ONLY on the remote" in str(caught.value)
    assert git.branch_exists(DRAFT) is False          # nothing was forked

    # and RESUME refuses rather than creating the divergent branch (FR-026: this
    # scan never fetches, so the human's fetch is the only route to a resume)
    with pytest.raises(bs.SessionRefused) as refused:
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root,
                        continuation=bs.CONTINUATION_RESUME,
                        inventory=gr.discover_tile_inventory(scratch_repo.root))
    assert "survives only on the remote" in str(refused.value)
    assert git.branch_exists(DRAFT) is False

    # NEW still works, and allocates over the union
    opened = bs.open_session(git, registry, repository=REPO,
                             tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                             checkout_root=scratch_repo.root,
                             continuation=bs.CONTINUATION_NEW,
                             inventory=gr.discover_tile_inventory(scratch_repo.root))
    assert opened.branch == f"{DRAFT}-2"


def test_an_abandoned_ORDINAL_branch_is_reported_and_resumed(scratch_repo,
                                                             tmp_path):
    """With only `draft/<t>-2` surviving, the base-name detector saw nothing and
    the tile opened a FRESH base branch with no report at all — the `-2` session's
    work unreachable from it. And with BOTH surviving, RESUME must take the MOST
    RECENT ordinal, not the oldest."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    scratch_repo.git("branch", f"{DRAFT}-2")
    inventory = gr.discover_tile_inventory(scratch_repo.root)

    with pytest.raises(bs.AbandonedBranchSurvives) as caught:
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root, inventory=inventory)
    assert caught.value.branch == f"{DRAFT}-2"
    assert git.branch_exists(DRAFT) is False          # no silent fresh base

    scratch_repo.git("branch", DRAFT)
    with pytest.raises(bs.AbandonedBranchSurvives) as both:
        bs.open_session(git, registry, repository=REPO,
                        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root, inventory=inventory)
    assert both.value.family == (DRAFT, f"{DRAFT}-2")
    assert both.value.branch == f"{DRAFT}-2"          # the most recent ordinal

    resumed = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root,
                              inventory=inventory,
                              continuation=bs.CONTINUATION_RESUME)
    assert resumed.branch == f"{DRAFT}-2"
