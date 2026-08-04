"""The SESSION-ONLY rewrite `edit-document` and the SAVE `open-pr`
(007-workbench-branch-sessions T037-T041 and T058-T062; FR-015-FR-017, FR-019,
FR-029-FR-034).

Phase 3 proved a session can be opened and written to; Phase 4 proved it can be
seen. This file proves the ONE verb that changes a document that already exists —
and, just as load-bearing, that it cannot reach anything outside the session —
then the verb that CLOSES the loop by pushing the branch into the existing
Merge-Master ritual.

Four claims earn their own section for `edit-document`:

  * **One action, one commit, no redline** (FR-015, FR-017). The rewrite lands in
    the WORKTREE and rides a single commit with its own gate-action record. There
    is deliberately no redline artifact: `edit-apply`'s redline is the ceremony
    that makes a MAIN-RESIDENT source edit reviewable, and on an unmerged branch
    the pull request is that ceremony instead (D18). The discriminating assertion
    is `git show --name-only` == {document, record} for exactly one new commit.

  * **The verb is session-ONLY, and its confinement is a refusal** (FR-016). No
    live session is a refusal that NAMES `edit-apply` and opens nothing — no
    branch, no worktree, no record. A path that resolves outside the session
    worktree refuses rather than falling back to the served checkout, a
    delete-shaped call refuses because no session verb grants delete authority,
    and a target that does not exist refuses because creation stays
    `create-document`. Every one of them persists nothing.

  * **FR-019 is enforced on BOTH surfaces** (route and CLI). The HTTP route
    inherits it from `serve.py::_handle_gate_action`, which refuses off-loopback
    and unresolved-actor calls BEFORE the body is parsed — asserted by sending a
    body that is not even a JSON object and still getting the identity refusal.
    The CLI is a FRESH PROCESS with no handler in front of it, so it enforces the
    same obligation per-verb, and that is asserted separately.

  * **`edit-apply` is untouched** (FR-017). Two verbs, never one renamed: with a
    session LIVE, `edit-apply` still writes the SERVED checkout's document, still
    emits its redline artifact, and adds NO commit to the session branch.

And four more for `open-pr` (US5):

  * **The record is MAIN-RESIDENT and it is written LAST** (FR-029). Ordering is
    push → open-or-update → record, asserted STRUCTURALLY: the fake port snapshots
    the served checkout's `open-pr` record count at every call, so a record written
    before either remote step is visible as a non-zero count. The record lands in
    the SERVED checkout, names the branch in `target.ref`, carries the pull request
    as a `pull-request` artifact and NO `commit` artifact, adds no commit to the
    branch — and is STILL READABLE after the merge path deletes that branch, which
    is the whole reason the residence is what it is.

  * **The verb holds no approval authority** (FR-030). Asserted on the PORT's
    ABSENT operations — there is no `merge`, `approve`, `review`, or
    `bypass_protection` anywhere on the protocol, the fake, or the real adapter —
    and on the route, which offers no such verb and no such flag.

  * **NEITHER readiness mechanism is consulted** (FR-031, D21). The topic's live
    health is genuinely NOT `ready`, and `kickoff._require_ready` is proven
    NOT REACHED by replacing it with a spy that raises: D21's deadlock is that a
    session's documents reach the served checkout only when the PR merges, so a
    readiness-gated save could never merge.

  * **Re-invocation updates, and the MERGE ends the session** (FR-032, FR-033). A
    second `open-pr` reports the SAME pull request and opens no second one; once
    the branch is merged into `main` the verb RECONCILES instead of pushing —
    teardown, branch DELETION, main-view refresh.

Every test builds on the `scratch_repo` harness (a throwaway checkout with a
local bare `origin`). No serve here is ever pointed at a real or fixture tree — a
serve WRITES into whatever `--checkout-root` it is given (research R10). Every
`open-pr` test runs against `FakePullRequests`: nothing here reaches a network,
a real `gh`, or a real pull request (FR-043; quickstart step 6's rule).
"""

from __future__ import annotations

import dataclasses
import http.client
import inspect
import json
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import kickoff as kickoff_mod
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import session_git as sg
from ideation_dashboard import session_pr as spr
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.boundary import (
    BoundaryViolation, HumanGate, OutputBoundary,
)
from ideation_dashboard.generator import generate_snapshot, live_topic_health

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
EDIT_ROUTE = "/actions/gate/edit-document"
OPEN_PR_ROUTE = "/actions/gate/open-pr"
RECORDS = gc.DEFAULT_RECORDS_DIR

CREATE_BODY = {
    "title": "First Draft",
    "summary": "The session's first document.",
    "topics": ["alpha"],
    "area": "ideation/staging/demo-topic/",
    "repository_context": REPO,
    "scope_kind": bs.STAGED_TOPIC,
    "scope_id": TOPIC,
}

NEW_TEXT = """# First Draft — Brainstorm

Status: brainstorm
Summary: The session's first document.
Topics: alpha
Repository context: openxFactory

## Notes

Rewritten inside the session.
"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _registry(repo, tmp_path, *, name="main-snapshot.json"):
    """A registry in the shape a serve holds one: `(repository, main)` registered
    and ACTIVE, with the served checkout as its source root. Written OUTSIDE the
    checkout, so building it never moves the served tree."""
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _create(repo, registry, **over):
    """One `create-document` through the ROUTE — the gesture that OPENS the
    session and gives `edit-document` something to rewrite."""
    status, payload = gr.run_gate_action(
        "create-document", {**CREATE_BODY, **over},
        checkout_root=repo.root, actor=over.pop("actor", "brett"),
        snapshot_path=None, session_registry=registry, repository=repo.repository)
    assert status == 200, payload
    return payload


def _edit(repo, registry, *, document, content=NEW_TEXT, actor="brett", **over):
    """One `edit-document` through the ROUTE, dispatched exactly as `serve.py`
    does it: the SERVED checkout as `checkout_root` (never the worktree)."""
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            "document": document}
    if content is not None:
        body["content"] = content
    body.update(over)
    return gr.run_gate_action(
        "edit-document", body, checkout_root=repo.root, actor=actor,
        snapshot_path=None, session_registry=registry,
        repository=repo.repository)


def _session(repo, tmp_path, **over):
    """A live session with one document in it: the starting state of every
    edit-document test. Returns (registry, created_payload, worktree)."""
    registry = _registry(repo, tmp_path, **over)
    created = _create(repo, registry)
    return registry, created, bs.worktree_path(repo.root, DRAFT)


def _files_in(worktree: Path, sha: str) -> list[str]:
    return subprocess.run(["git", "show", "--name-only", "--format=", sha],
                          cwd=str(worktree), text=True, capture_output=True,
                          check=True).stdout.split()


def _record_of(worktree: Path, payload: dict) -> dict:
    return yaml.safe_load((worktree / payload["record"]).read_text("utf-8"))


@contextmanager
def _serving(repo, snapshot_path, *, host="127.0.0.1", actor="tester"):
    """A serve over real HTTP against the SCRATCH checkout — the surface whose
    handler owns the FR-019 refusals every route inherits."""
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, host=host,
                                   actor=actor)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    bind_host, port = httpd.server_address[:2]
    try:
        yield ("127.0.0.1" if bind_host in ("0.0.0.0", "") else bind_host, port)
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _served_snapshot(repo, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    return path


def _console_token(host, port):
    """The per-serve human-console token (FR-019's third clause; PR #49 review
    finding 2), read the ONLY way the served page can read it — a same-origin
    `GET /capabilities`. A test that drives the route drives it as the CONSOLE
    does; the refusal for a caller that cannot is asserted in
    `test_session_confinement.py`."""
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("GET", "/capabilities")
    response = conn.getresponse()
    caps = json.loads(response.read().decode("utf-8"))
    conn.close()
    return caps.get("console_token")


def _post_raw(host, port, path, raw: bytes):
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(raw))}
    token = _console_token(host, port)
    if token:
        headers["X-XF-Console-Token"] = token
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("POST", path, body=raw, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))
    conn.close()
    return response.status, data


def _post(host, port, path, body):
    return _post_raw(host, port, path, json.dumps(body).encode("utf-8"))


def _redlines(*roots: Path) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        out += sorted(root.rglob("*.redline.yaml"))
    return out


# ==========================================================================
# T037 — the rewrite lands in the worktree as ONE commit with its record, and
# no redline artifact is required or produced (FR-015, FR-017)
# ==========================================================================

def test_edit_document_rewrites_in_the_worktree_as_one_commit_with_its_record(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    before_fingerprint = scratch_repo.served_fingerprint()
    assert git.commits_ahead("main", DRAFT) == 1          # the create's commit

    status, payload = _edit(scratch_repo, registry, document=created["path"])

    assert status == 200, payload
    assert payload["ok"] is True
    assert payload["verb"] == "edit-document"
    assert payload["ref"] == DRAFT
    assert payload["document"] == created["path"]
    assert payload["commit"] == git.head(worktree)

    # the WORKTREE holds the new bytes; the served checkout holds no such file
    assert (worktree / created["path"]).read_text(encoding="utf-8") == NEW_TEXT
    assert not (scratch_repo.root / created["path"]).exists()

    # exactly ONE more commit, carrying exactly the document and its record
    assert git.commits_ahead("main", DRAFT) == 2
    assert sorted(_files_in(worktree, payload["commit"])) == sorted(
        [created["path"], payload["record"]])

    record = _record_of(worktree, payload)
    assert record["action"] == gc.ACTION_EDIT_DOCUMENT
    assert record["actor"] == "brett"
    assert record["target"] == {"ref": DRAFT, "document": created["path"]}
    # the ONE artifact is the commit, referenced by the ACTION STAMP (never a sha)
    stamp = bs.action_stamp(record["at"])
    assert record["artifacts"] == [{"kind": gc.ART_COMMIT, "reference": stamp}]
    assert payload["record"].endswith(f"edit-document-{stamp}.gate-action.yaml")
    assert f"Gate-Action: {stamp}" in git.git(worktree, "log", "-1", "--format=%B")
    assert git.introduced_by(payload["record"], cwd=worktree) == payload["commit"]

    # FR-017: no redline artifact is REQUIRED (the call carried none) and none is
    # produced, in the worktree or in the served checkout
    assert _redlines(worktree, scratch_repo.root) == []
    assert gc.ART_REDLINE not in [a["kind"] for a in record["artifacts"]]

    # FR-010 rides the same commit path: the session's projection is already
    # regenerated at THIS action's commit, with no manual step
    assert registry.get(REPO, DRAFT).read_json()["generation"][
        "source_revision"] == payload["commit"]
    # and FR-014a still holds — the shared surfaces did not follow the session
    assert registry.active.ref == reg.DEFAULT_REF
    # SC-002: the served checkout never moved
    assert scratch_repo.served_fingerprint() == before_fingerprint


def test_a_second_edit_is_a_second_commit_and_the_record_is_never_main_resident(
        scratch_repo, tmp_path):
    registry, first_doc, worktree = _session(scratch_repo, tmp_path)
    second_doc = _create(scratch_repo, registry, title="Second Draft")
    git = sg.SessionGit(scratch_repo.root)

    first = _edit(scratch_repo, registry, document=first_doc["path"])[1]
    second = _edit(scratch_repo, registry, document=second_doc["path"],
                   content=NEW_TEXT + "\nA second pass.\n",
                   notes="tightened the claim")[1]

    assert first["commit"] != second["commit"]
    assert git.commits_ahead("main", DRAFT) == 4          # 2 creates + 2 edits
    assert _record_of(worktree, second)["notes"] == "tightened the claim"
    # every edit record rides the BRANCH: none of them is in the served checkout
    assert sorted(p.name for p in
                  (scratch_repo.root / RECORDS).rglob("*.gate-action.yaml")) == []
    assert len(list((worktree / RECORDS).rglob("edit-document-*.gate-action.yaml"))) == 2


def test_a_re_submitted_edit_in_the_same_second_refuses_and_persists_nothing(
        scratch_repo, tmp_path, monkeypatch):
    """A gate-action record's filename carries its stamp at SECOND resolution, and
    `edit-document` is the first verb that can emit two records for one target id
    (a double-clicked save). Overwriting the first record would leave its commit no
    longer the one that INTRODUCED it — so the second submission is refused ahead
    of the rewrite, with the branch and the worktree exactly as they were.

    The clock is frozen rather than raced: the collision is what is under test, so
    it must happen every run and not only on a fast machine."""
    monkeypatch.setattr(gc, "_utcnow", lambda: "2026-07-26T12:00:00Z")
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    landed = _edit(scratch_repo, registry, document=created["path"])[1]
    after_first = (worktree / created["path"]).read_bytes()

    status, payload = _edit(scratch_repo, registry, document=created["path"],
                            content=NEW_TEXT + "\nA re-submitted pass.\n")

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "same second" in payload["message"]
    assert git.commits_ahead("main", DRAFT) == 2          # the create + ONE edit
    assert git.head(worktree) == landed["commit"]
    assert (worktree / created["path"]).read_bytes() == after_first
    assert git.dirty_paths(worktree) == ()
    assert len(list((worktree / RECORDS).rglob("edit-document-*.gate-action.yaml"))) == 1


def test_edit_document_over_http_lands_through_the_serve_handler(scratch_repo,
                                                                 tmp_path):
    """The route as `serve.py` dispatches it — which is also what proves the serve
    hands the session registry and repository down (research R1's gap)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")

    with _serving(scratch_repo, served) as (host, port):
        status, payload = _post(host, port, EDIT_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            "document": created["path"], "content": NEW_TEXT})

    assert status == 200, payload
    assert payload["ref"] == DRAFT
    assert (worktree / created["path"]).read_text(encoding="utf-8") == NEW_TEXT
    assert _record_of(worktree, payload)["actor"] == "tester"
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 2


def test_the_verb_is_declared_and_dispatched(scratch_repo, tmp_path):
    """`EXECUTING_VERBS` is the declaration and the if-chain is the dispatch —
    both, or the verb is either undeclared or unreachable (research R5)."""
    assert "edit-document" in gr.EXECUTING_VERBS
    status, payload = gr.run_gate_action(
        "edit-documents", {}, checkout_root=scratch_repo.root, actor="brett")
    assert status == 404 and payload["error"] == "unknown_verb"


# ==========================================================================
# T038 — session-only: no live session, and never the served checkout's `main`
# (FR-016)
# ==========================================================================

def test_edit_document_with_no_active_session_refuses_and_opens_nothing(
        scratch_repo, tmp_path):
    """The refusal must not become a session: a verb that opened one to satisfy
    itself would make `edit-document` a second way to start work, and the tile's
    one-session-at-a-time rule would be decided by whoever typed first."""
    registry = _registry(scratch_repo, tmp_path)
    scratch_repo.write("ideation/staging/demo-topic/note.md", "# Note\n")
    scratch_repo.commit("Add a main-resident note",
                        "ideation/staging/demo-topic/note.md")
    before = scratch_repo.served_fingerprint()

    status, payload = _edit(scratch_repo, registry,
                            document="ideation/staging/demo-topic/note.md")

    assert status == 409
    assert payload["error"] == "gate_refused"
    # the refusal names the main-resident alternative rather than merely failing
    assert "edit-apply" in payload["message"]
    assert DRAFT in payload["message"] or TOPIC in payload["message"]

    git = sg.SessionGit(scratch_repo.root)
    assert git.branch_exists(DRAFT) is False              # no branch was opened
    assert not (scratch_repo.container / "sessions").exists()
    assert bs.is_live(registry, REPO, DRAFT) is False
    assert registry.keys() == [(REPO, reg.DEFAULT_REF)]
    # nothing persisted, and the served checkout's document is untouched
    assert (scratch_repo.root / "ideation" / "staging" / TOPIC / "note.md"
            ).read_text(encoding="utf-8") == "# Note\n"
    assert scratch_repo.served_fingerprint() == before


def test_a_document_that_lives_only_on_main_is_refused_from_inside_a_session(
        scratch_repo, tmp_path):
    """FR-016's other half: inside a session, `main`'s copy is not reachable. The
    served checkout's bytes are the assertion — a fallback would have rewritten
    them."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    rel = "main-only.md"
    scratch_repo.write(rel, "main only\n")
    scratch_repo.commit("A document only main has", rel)
    before_bytes = (scratch_repo.root / rel).read_bytes()
    git = sg.SessionGit(scratch_repo.root)
    ahead = git.commits_ahead("main", DRAFT)

    relative = _edit(scratch_repo, registry, document=rel)
    absolute = _edit(scratch_repo, registry, document=str(scratch_repo.root / rel))

    for status, payload in (relative, absolute):
        assert status == 409, payload
        assert payload["error"] == "gate_refused"
    assert (scratch_repo.root / rel).read_bytes() == before_bytes
    assert not (worktree / rel).exists()                 # nothing was created
    assert git.commits_ahead("main", DRAFT) == ahead      # no commit either way


def test_a_session_that_ended_refuses_again_even_though_its_branch_survives(
        scratch_repo, tmp_path):
    """Liveness is the registry ENTRY (FR-008): the branch and the worktree
    survive an ending by design, so an edit after one must refuse — otherwise
    `edit-document` would resurrect a session nobody resumed."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    bs.unregister_session_entry(registry, REPO, DRAFT)
    before = (worktree / created["path"]).read_bytes()

    status, payload = _edit(scratch_repo, registry, document=created["path"])

    assert status == 409 and "edit-apply" in payload["message"]
    assert (worktree / created["path"]).read_bytes() == before
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_with_no_declared_session_registry_the_verb_refuses(scratch_repo):
    """A plane that declares no registry has nowhere for liveness to live, so
    there is no session to be inside — and `create-document`'s pre-session
    fallthrough is deliberately NOT this verb's behaviour (FR-016)."""
    status, payload = gr.run_gate_action(
        "edit-document",
        {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
         "document": "ideation/staging/demo-topic/README.md", "content": "# x\n"},
        checkout_root=scratch_repo.root, actor="brett")

    assert status == 409 and payload["error"] == "gate_refused"
    assert not (scratch_repo.container / "sessions").exists()


def test_a_body_naming_no_tile_is_a_shaping_error(scratch_repo, tmp_path):
    registry, created, _ = _session(scratch_repo, tmp_path)
    for body in ({"document": created["path"], "content": NEW_TEXT},
                 {"scope_kind": bs.STAGED_TOPIC, "document": created["path"],
                  "content": NEW_TEXT},
                 {"scope_id": TOPIC, "document": created["path"],
                  "content": NEW_TEXT},
                 {"scope_kind": "not-a-kind", "scope_id": TOPIC,
                  "document": created["path"], "content": NEW_TEXT},
                 {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
                  "content": NEW_TEXT}):                      # no document
        status, payload = gr.run_gate_action(
            "edit-document", body, checkout_root=scratch_repo.root,
            actor="brett", session_registry=registry, repository=REPO)
        assert status == 400, body
        assert payload["error"] == "invalid_body", body


# ==========================================================================
# T039 — confinement and the delete shape (FR-016)
# ==========================================================================

def test_a_path_outside_the_session_worktree_refuses_and_persists_nothing(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    before = scratch_repo.served_fingerprint()
    outside = tmp_path / "outside.md"
    outside.write_text("untouched\n", encoding="utf-8")

    for document in ("../escape.md",
                     f"../../{REPO}/ideation/staging/{TOPIC}/README.md",
                     str(outside),
                     "../../../etc/passwd"):
        status, payload = _edit(scratch_repo, registry, document=document)
        assert status == 409, document
        assert payload["error"] == "gate_refused", document

    assert outside.read_text(encoding="utf-8") == "untouched\n"
    assert not (worktree.parent / "escape.md").exists()
    assert git.commits_ahead("main", DRAFT) == 1           # only the create
    assert git.dirty_paths(worktree) == ()                 # nothing left behind
    assert scratch_repo.served_fingerprint() == before


def test_a_delete_shaped_invocation_refuses(scratch_repo, tmp_path):
    """No session verb grants delete authority, and an empty file is how a delete
    would be spelled if one tried."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    target = worktree / created["path"]
    before = target.read_bytes()

    for content in (None, "", "   ", "\n\t\n"):
        status, payload = _edit(scratch_repo, registry,
                                document=created["path"], content=content)
        assert status == 409, repr(content)
        assert payload["error"] == "gate_refused", repr(content)
        assert "delete" in payload["message"], repr(content)

    assert target.read_bytes() == before                   # never emptied
    assert target.is_file()                                # and never removed
    assert git.commits_ahead("main", DRAFT) == 1
    assert git.dirty_paths(worktree) == ()


def test_a_target_that_does_not_exist_refuses_because_creation_is_the_other_verb(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)

    status, payload = _edit(scratch_repo, registry,
                            document="ideation/staging/demo-topic/absent.md")

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert not (worktree / "ideation" / "staging" / TOPIC / "absent.md").exists()
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_content_that_is_not_text_is_a_shaping_error(scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    before = (worktree / created["path"]).read_bytes()

    for content in ([NEW_TEXT], {"text": NEW_TEXT}, 7):
        status, payload = gr.run_gate_action(
            "edit-document",
            {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
             "document": created["path"], "content": content},
            checkout_root=scratch_repo.root, actor="brett",
            session_registry=registry, repository=REPO)
        assert status == 400, repr(content)
        assert payload["error"] == "invalid_body", repr(content)

    assert (worktree / created["path"]).read_bytes() == before


def test_a_byte_identical_replacement_refuses_instead_of_committing_nothing(
        scratch_repo, tmp_path):
    """A no-op rewrite has no commit to ride, and the split-write guard would
    report it as an already-committed document — true, and useless to the human.
    So it is refused in its own words, with nothing persisted."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    unchanged = (worktree / created["path"]).read_text(encoding="utf-8")

    status, payload = _edit(scratch_repo, registry, document=created["path"],
                            content=unchanged)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "identical" in payload["message"]
    assert git.commits_ahead("main", DRAFT) == 1
    assert git.dirty_paths(worktree) == ()
    assert len(list((worktree / RECORDS).rglob("edit-document-*.gate-action.yaml"))) == 0


# ==========================================================================
# T040 — FR-019 on BOTH surfaces: the route inherits it, the CLI owns it
# ==========================================================================

def test_the_route_refuses_off_loopback_before_the_body_is_parsed(scratch_repo,
                                                                  tmp_path):
    """The body sent here is not even a JSON object: an `invalid_body` answer
    would prove the parse ran first, which is the ordering FR-019 forbids."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")
    before = (worktree / created["path"]).read_bytes()

    with _serving(scratch_repo, served, host="0.0.0.0") as (host, port):
        shaped = _post(host, port, EDIT_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            "document": created["path"], "content": NEW_TEXT})
        unparseable = _post_raw(host, port, EDIT_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "loopback_only", payload
    assert (worktree / created["path"]).read_bytes() == before
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_the_route_fails_closed_with_no_resolved_actor_before_the_body_is_parsed(
        scratch_repo, tmp_path, monkeypatch):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")
    before = (worktree / created["path"]).read_bytes()
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *a, **k: None)

    with _serving(scratch_repo, served, actor=None) as (host, port):
        shaped = _post(host, port, EDIT_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
            "document": created["path"], "content": NEW_TEXT})
        unparseable = _post_raw(host, port, EDIT_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "action_unavailable", payload
    assert (worktree / created["path"]).read_bytes() == before


def test_the_agent_path_is_rejected_and_reported_before_anything_is_written(
        scratch_repo, tmp_path):
    """Structural (D16): an `OutputBoundary` — the machinery/agent chokepoint —
    is refused by `require_human_gate` before the rewrite is attempted, and the
    refusal is REPORTED on the offending object's own ledger."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    before = (worktree / created["path"]).read_bytes()
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    agent = OutputBoundary(worktree, [RECORDS], actor="agent",
                           session_root=worktree)

    with pytest.raises(BoundaryViolation):
        gr.execute_edit_document(agent, document=created["path"],
                                 content=NEW_TEXT, records_dir=RECORDS,
                                 session=session, git=git)

    assert agent.refusals and agent.refusals[0].kind == "gate-side-effect"
    assert (worktree / created["path"]).read_bytes() == before
    assert git.commits_ahead("main", DRAFT) == 1
    assert git.dirty_paths(worktree) == ()


def test_the_cli_verb_enforces_the_human_gate_itself(scratch_repo, tmp_path,
                                                     capsys):
    """The CLI is a FRESH PROCESS with no `serve.py` handler in front of it, so
    FR-019 is a PER-VERB obligation here (contracts/cli.md): the human gate is
    constructed and required by this subcommand, before the content file is read
    and before any session is resolved."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    content_file = tmp_path / "new.md"
    content_file.write_text(NEW_TEXT, encoding="utf-8")
    before = (worktree / created["path"]).read_bytes()
    # The gate is required through the SHARED `_session_identity_gate` — the one
    # all five session subcommands call — rather than by a per-verb inline copy
    # (PR #49 review finding 2: the inline copy is exactly how this verb missed
    # FR-019's agent/automation clause when that clause arrived). The pin follows
    # the obligation to where it is discharged, and is STRICTER for it: it now
    # asserts the shared implementation, so the four siblings are covered too.
    source = inspect.getsource(cli_mod.cmd_gate_edit_document)
    assert "_session_identity_gate(" in source
    shared = inspect.getsource(cli_mod._session_identity_gate)
    assert "require_human_gate" in shared
    assert "human_console_present()" in shared

    # a MISSING actor is argparse's fail-closed refusal — no write, no session
    with pytest.raises(SystemExit) as exited:
        cli_mod.main(["gate", "edit-document", "--repo-root",
                      str(scratch_repo.root), "--scope-kind", bs.STAGED_TOPIC,
                      "--scope-id", TOPIC, "--document", created["path"],
                      "--content-file", str(content_file)])
    assert exited.value.code != 0
    assert (worktree / created["path"]).read_bytes() == before

    # a BLANK actor is refused too: a gate action with no identified human is
    # structurally invalid, and it must not reach a traceback
    capsys.readouterr()
    rc = cli_mod.main(["gate", "edit-document", "--repo-root",
                       str(scratch_repo.root), "--actor", "   ",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--document", created["path"],
                       "--content-file", str(content_file)])
    assert rc == 1
    assert "refused" in capsys.readouterr().err
    assert (worktree / created["path"]).read_bytes() == before
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_the_cli_verb_edits_the_session_and_reports_the_commit(scratch_repo,
                                                               tmp_path, capsys):
    """CLI parity (FR-020, contracts/cli.md): `--content-file` rather than inline
    text so a shell cannot mangle a document, and the process re-derives its own
    session registry (T033a) — without that a CLI verb sees no session at all."""
    _registry_and = _session(scratch_repo, tmp_path)
    created, worktree = _registry_and[1], _registry_and[2]
    content_file = tmp_path / "new.md"
    content_file.write_text(NEW_TEXT, encoding="utf-8")
    capsys.readouterr()

    rc = cli_mod.main(["gate", "edit-document", "--repo-root",
                       str(scratch_repo.root), "--actor", "dana",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--document", created["path"],
                       "--content-file", str(content_file),
                       "--notes", "sharpened the summary"])

    assert rc == 0
    out = capsys.readouterr().out
    assert created["path"] in out
    assert DRAFT in out
    git = sg.SessionGit(scratch_repo.root)
    assert (worktree / created["path"]).read_text(encoding="utf-8") == NEW_TEXT
    assert git.commits_ahead("main", DRAFT) == 2
    records = sorted((worktree / RECORDS).rglob("edit-document-*.gate-action.yaml"))
    assert len(records) == 1
    record = yaml.safe_load(records[0].read_text(encoding="utf-8"))
    assert record["actor"] == "dana"
    assert record["target"] == {"ref": DRAFT, "document": created["path"]}
    assert record["notes"] == "sharpened the summary"
    assert _redlines(worktree, scratch_repo.root) == []


def test_the_cli_verb_reports_the_engines_refusal_verbatim(scratch_repo,
                                                           tmp_path, capsys):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    content_file = tmp_path / "new.md"
    content_file.write_text(NEW_TEXT, encoding="utf-8")
    bs.unregister_session_entry(registry, REPO, DRAFT)   # only THIS process's view
    capsys.readouterr()

    rc = cli_mod.main(["gate", "edit-document", "--repo-root",
                       str(scratch_repo.root), "--actor", "brett",
                       "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
                       "--document", "ideation/staging/demo-topic/absent.md",
                       "--content-file", str(content_file)])

    assert rc == 1
    err = capsys.readouterr().err
    assert "refused" in err
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_the_cli_offers_no_inline_content_and_no_bypass_flag():
    """`--content-file`, never inline text; and no flag skips the gate, the
    confinement, or the record (the pre-existing pin, extended)."""
    source = Path(cli_mod.__file__).read_text(encoding="utf-8")
    for flag in ("--force", "--override", "--overwrite", "--no-record",
                 "--skip-gate", "--no-gate", "--content ", "--delete"):
        assert flag not in source, flag
    parser = cli_mod.build_parser()
    args = parser.parse_args(["gate", "edit-document", "--repo-root", ".",
                              "--actor", "brett", "--scope-kind",
                              bs.STAGED_TOPIC, "--scope-id", TOPIC,
                              "--document", "d.md", "--content-file", "c.md"])
    assert args.func is cli_mod.cmd_gate_edit_document
    assert args.records_dir == gc.DEFAULT_RECORDS_DIR      # _add_gate_identity_args
    with pytest.raises(SystemExit):                        # --document is required
        parser.parse_args(["gate", "edit-document", "--repo-root", ".",
                           "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC,
                           "--scope-id", TOPIC, "--content-file", "c.md"])
    with pytest.raises(SystemExit):                        # so is --content-file
        parser.parse_args(["gate", "edit-document", "--repo-root", ".",
                           "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC,
                           "--scope-id", TOPIC, "--document", "d.md"])


# ==========================================================================
# T041 — `edit-apply` is behaviourally unchanged (FR-017)
# ==========================================================================

def test_edit_apply_still_writes_main_and_its_redline_while_a_session_is_live(
        scratch_repo, tmp_path):
    """Two verbs, never one renamed: with a session LIVE, the main-resident
    redline path still rewrites the SERVED checkout's document, still emits its
    redline artifact, and adds NO commit to the session branch."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    rel = "ideation/staging/demo-topic/README.md"
    original = (scratch_repo.root / rel).read_text(encoding="utf-8")
    gate = HumanGate(scratch_repo.root, [RECORDS], human_actor="brett")

    result = gc.edit_apply(gate, "add-demo-change", rel,
                           gc.Redline(old_text=original,
                                      new_text=original + "\nRevised.\n"),
                           tree_root=scratch_repo.root)

    # the SERVED checkout's document changed, and only there
    assert (scratch_repo.root / rel).read_text(encoding="utf-8").endswith(
        "\nRevised.\n")
    assert (worktree / rel).read_text(encoding="utf-8") == original
    assert result.redline_path.is_file()                   # the redline artifact
    record = yaml.safe_load(result.record_path.read_text(encoding="utf-8"))
    assert record["action"] == gc.ACTION_EDIT_APPLY
    assert [a["kind"] for a in record["artifacts"]] == [gc.ART_REDLINE]
    assert "ref" not in record["target"]                   # no session dimension
    assert git.commits_ahead("main", DRAFT) == 1           # the create's, only


def test_the_two_verbs_stay_distinct_in_name_and_in_signature():
    """FR-017 as a pin: `edit-apply` gained no session parameter and
    `edit-document` accepts no redline, so neither can drift into the other."""
    assert gc.ACTION_EDIT_DOCUMENT != gc.ACTION_EDIT_APPLY
    apply_params = set(inspect.signature(gc.edit_apply).parameters)
    # `provenance` joined every record-writing verb on 2026-07-27 (D23, Brett's
    # ruling item 3): the gateway fact this verb's own record must carry. It is a
    # SURFACE parameter, not a session one, so the pin stays an EXACT set — the
    # claim it defends is "no session dimension leaked into `edit-apply`", and the
    # assertions below still forbid every session and redline spelling.
    assert apply_params == {"gate", "change_id", "document", "redline", "at",
                            "records_dir", "tree_root", "provenance"}
    edit_params = set(inspect.signature(gr.execute_edit_document).parameters)
    assert "redline" not in edit_params
    assert {"session", "git", "document", "content"} <= edit_params
    # and the session verb is not implemented by calling the main-resident one,
    # nor by building a redline of any kind (the word survives only in the
    # refusal prose that POINTS a refused human at `edit-apply`)
    source = inspect.getsource(gr.execute_edit_document)
    assert "edit_apply" not in source
    assert "Redline" not in source
    assert "redline_artifact" not in source
    assert "ART_REDLINE" not in source


# ==========================================================================
# open-pr helpers — every one of them against `FakePullRequests` (FR-043)
# ==========================================================================

def _pr_records(root: Path) -> list[Path]:
    return sorted((root / RECORDS).rglob("open-pr-*.gate-action.yaml"))


class ObservingPullRequests(spr.FakePullRequests):
    """`FakePullRequests` that snapshots the SERVED checkout's `open-pr` record
    count at every port call.

    This is how the FR-029 ordering (push → open-or-update → write the record) is
    asserted STRUCTURALLY rather than by reading the implementation: a record
    written before either remote step shows up as a non-zero count beside that
    step's name."""

    def __init__(self, root: Path, **kw) -> None:
        super().__init__(**kw)
        self.root = Path(root)
        self.seen: list[tuple[str, int]] = []

    def _snap(self, name: str) -> None:
        self.seen.append((name, len(_pr_records(self.root))))

    @property
    def order(self) -> list[str]:
        return [name for name, _ in self.seen]

    def push(self, branch):
        self._snap("push")
        return super().push(branch)

    def open_or_update(self, branch, **kw):
        self._snap("open_or_update")
        return super().open_or_update(branch, **kw)

    def find_open(self, branch):
        self._snap("find_open")
        return super().find_open(branch)


def _save(repo, registry, *, pull_requests, actor="brett", scope_id=TOPIC, **over):
    """One `open-pr` through the ROUTE, dispatched exactly as `serve.py` does it:
    the SERVED checkout as `checkout_root`, and the pull-request port INJECTED."""
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": scope_id}
    body.update(over)
    return gr.run_gate_action(
        "open-pr", body, checkout_root=repo.root, actor=actor, snapshot_path=None,
        session_registry=registry, repository=repo.repository,
        session_pull_requests=pull_requests)


@pytest.fixture
def ticking_clock(monkeypatch):
    """Wall-clock stamps that ADVANCE by one second per gate action.

    The `open-pr` record is REF-keyed, so two saves inside ONE second legitimately
    collide and are refused (that refusal has its own test). A test about the
    SECOND save therefore needs the clock to move the way it really does, rather
    than to race it."""
    ticks = iter(f"2026-07-26T12:00:{second:02d}Z" for second in range(1, 60))
    monkeypatch.setattr(gc, "_utcnow", lambda: next(ticks))


def _merge_on_main(repo, branch=DRAFT):
    """The Merge Master's action, simulated EXTERNALLY: a real MERGE COMMIT on the
    served checkout's `main` (D18 — never a squash). This is deliberately done with
    raw git rather than through `session_git`, because merging is not a session
    operation and no session verb may perform it (FR-030)."""
    repo.git("merge", "--no-ff", "-m", f"Merge {branch}", branch)
    return repo.head("main")


# ==========================================================================
# T058 — the record names the branch, references the PR, and is MAIN-RESIDENT,
# written AFTER the push and the open-or-update (FR-029)
# ==========================================================================

def test_open_pr_records_the_pull_request_on_main_after_pushing(scratch_repo,
                                                                tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    port = ObservingPullRequests(scratch_repo.root)
    ahead = git.commits_ahead("main", DRAFT)
    head_before = git.head(ref=DRAFT)
    assert _pr_records(scratch_repo.root) == []

    status, payload = _save(scratch_repo, registry, pull_requests=port,
                            title="Session: demo-topic", body="the first draft")

    assert status == 200, payload
    assert payload["ok"] is True
    assert payload["verb"] == "open-pr"
    assert payload["ref"] == DRAFT
    assert payload["updated"] is False
    assert payload["merged"] is False
    assert payload["pull_request"] == port.open_prs[DRAFT].url

    # the branch was PUSHED, and the PR was opened for it with `main` as base
    assert port.pushed == [DRAFT]
    assert ("open_or_update", DRAFT, "main", "Session: demo-topic",
            "the first draft") in port.calls

    # ORDERING, structurally: no record existed at either remote step
    assert port.order == ["find_open", "push", "open_or_update"]
    assert [count for _, count in port.seen] == [0, 0, 0]

    # the record is MAIN-RESIDENT: the SERVED checkout's gate-records tree
    record_path = scratch_repo.root / payload["record"]
    assert record_path.is_file()
    assert payload["record"].startswith(RECORDS)
    assert _pr_records(scratch_repo.root) == [record_path]
    assert not (worktree / payload["record"]).exists()

    record = yaml.safe_load(record_path.read_text(encoding="utf-8"))
    assert record["kind"] == gc.RECORD_KIND
    assert record["action"] == gc.ACTION_OPEN_PR
    assert record["actor"] == "brett"
    assert record["target"] == {"ref": DRAFT}          # NAMES the branch
    assert record["artifacts"] == [{"kind": gc.ART_PULL_REQUEST,
                                    "reference": payload["pull_request"]}]
    # NO `commit` artifact, and no commit on the branch to carry one
    assert gc.ART_COMMIT not in [a["kind"] for a in record["artifacts"]]
    assert "commit" not in payload
    assert git.commits_ahead("main", DRAFT) == ahead
    assert git.head(ref=DRAFT) == head_before
    assert payload["record"] not in git.git(
        scratch_repo.root, "log", "--format=", "--name-only", DRAFT).split()


def test_the_open_pr_record_survives_the_merge_that_deletes_the_branch(
        scratch_repo, tmp_path):
    """The discriminating assertion for the residence (FR-029, plan Constraint 10):
    a record committed onto the branch after the push would never reach the pull
    request AND would die with the branch at merge. Merge, reconcile, read it
    back."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    saved = _save(scratch_repo, registry, pull_requests=port)[1]

    _merge_on_main(scratch_repo)
    result = bs.reconcile_merged_session(
        sg.SessionGit(scratch_repo.root),
        bs.open_session(sg.SessionGit(scratch_repo.root), registry,
                        repository=REPO, tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                        checkout_root=scratch_repo.root),
        checkout_root=scratch_repo.root)

    assert result.merged is True
    assert sg.SessionGit(scratch_repo.root).branch_exists(DRAFT) is False
    reread = yaml.safe_load(
        (scratch_repo.root / saved["record"]).read_text(encoding="utf-8"))
    assert reread["target"]["ref"] == DRAFT
    assert reread["artifacts"][0]["kind"] == gc.ART_PULL_REQUEST
    assert reread["artifacts"][0]["reference"] == saved["pull_request"]


def test_open_pr_with_no_active_session_refuses_and_pushes_nothing(scratch_repo,
                                                                   tmp_path):
    registry = _registry(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    before = scratch_repo.served_fingerprint()

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert port.calls == []                           # nothing was pushed
    assert _pr_records(scratch_repo.root) == []
    assert scratch_repo.served_fingerprint() == before


def test_open_pr_reports_a_port_failure_verbatim_and_records_nothing(scratch_repo,
                                                                     tmp_path):
    """contracts/gate-routes.md: a push or PR failure is the engine's reason,
    VERBATIM, as a 409 — and no record may claim a pull request that never
    opened."""
    registry, created, worktree = _session(scratch_repo, tmp_path)

    pushed = _save(scratch_repo, registry,
                   pull_requests=spr.FakePullRequests(
                       fail_push="gh: no upstream configured for draft/demo-topic"))
    opened = _save(scratch_repo, registry,
                   pull_requests=spr.FakePullRequests(
                       fail_open="gh: pull request create failed (protected base)"))

    assert pushed[0] == 409 and "no upstream configured" in pushed[1]["message"]
    assert opened[0] == 409 and "protected base" in opened[1]["message"]
    assert _pr_records(scratch_repo.root) == []


def test_a_re_submitted_save_in_the_same_second_refuses_and_records_once(
        scratch_repo, tmp_path, monkeypatch):
    """The `open-pr` record is REF-keyed, so the same-second collision Phase 5
    found for `edit-document` is reachable here too: a second record for one
    branch in one second would OVERWRITE the first, destroying the only durable
    trace of the pull request. Refused ahead of the push, so nothing is
    re-pushed."""
    monkeypatch.setattr(gc, "_utcnow", lambda: "2026-07-26T12:00:00Z")
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    first = _save(scratch_repo, registry, pull_requests=port)[1]
    port.calls.clear()

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 409
    assert "same second" in payload["message"]
    assert port.calls == []                           # refused BEFORE the push
    assert _pr_records(scratch_repo.root) == [scratch_repo.root / first["record"]]


def test_the_save_verb_is_declared_and_dispatched(scratch_repo):
    assert "open-pr" in gr.EXECUTING_VERBS
    for verb in ("open-prs", "merge-pr", "approve-pr", "merge-session"):
        status, payload = gr.run_gate_action(
            verb, {}, checkout_root=scratch_repo.root, actor="brett")
        assert status == 404 and payload["error"] == "unknown_verb", verb


def test_a_save_body_naming_no_tile_is_a_shaping_error(scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    for body in ({}, {"scope_kind": bs.STAGED_TOPIC}, {"scope_id": TOPIC},
                 {"scope_kind": "not-a-kind", "scope_id": TOPIC}):
        status, payload = gr.run_gate_action(
            "open-pr", body, checkout_root=scratch_repo.root, actor="brett",
            session_registry=registry, repository=REPO,
            session_pull_requests=port)
        assert status == 400, body
        assert payload["error"] == "invalid_body", body
    assert port.calls == []


def test_with_no_declared_pull_request_port_the_save_refuses(scratch_repo,
                                                             tmp_path):
    """The port is INJECTED, exactly like the notebook adapter (FR-029's
    "injectable seam"): a plane that declares none cannot save, and it says so
    naming the CLI parity command rather than inventing a credential."""
    registry, created, worktree = _session(scratch_repo, tmp_path)

    status, payload = _save(scratch_repo, registry, pull_requests=None)

    assert status == 409
    assert payload["error"] == "gate_refused"
    assert "open-pr" in payload["message"]
    assert _pr_records(scratch_repo.root) == []


# ==========================================================================
# T058a — the three per-verb FR-019 refusals, on the route AND the CLI
# ==========================================================================

def test_the_save_route_refuses_off_loopback_before_the_body_is_parsed(
        scratch_repo, tmp_path):
    """The body sent here is not even a JSON object: an `invalid_body` answer
    would prove the parse ran first, which is the ordering FR-019 forbids."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")

    with _serving(scratch_repo, served, host="0.0.0.0") as (host, port):
        shaped = _post(host, port, OPEN_PR_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC})
        unparseable = _post_raw(host, port, OPEN_PR_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "loopback_only", payload
    assert _pr_records(scratch_repo.root) == []
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_the_save_route_fails_closed_with_no_resolved_actor(scratch_repo,
                                                            tmp_path,
                                                            monkeypatch):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    served = _served_snapshot(scratch_repo, tmp_path / "served.json")
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *a, **k: None)

    with _serving(scratch_repo, served, actor=None) as (host, port):
        shaped = _post(host, port, OPEN_PR_ROUTE, {
            "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC})
        unparseable = _post_raw(host, port, OPEN_PR_ROUTE, b"[not an object")

    for status, payload in (shaped, unparseable):
        assert status == 403, payload
        assert payload["error"] == "action_unavailable", payload
    assert _pr_records(scratch_repo.root) == []


def test_the_save_agent_path_is_rejected_before_the_branch_is_pushed(scratch_repo,
                                                                      tmp_path):
    """Structural (D16): an `OutputBoundary` — the machinery/agent chokepoint — is
    refused by `require_human_gate` BEFORE the body's title/body are used and
    before the port is touched, and the refusal is REPORTED on the offending
    object's own ledger."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    port = spr.FakePullRequests()
    agent = OutputBoundary(scratch_repo.root, [RECORDS], actor="agent")

    with pytest.raises(BoundaryViolation):
        gr.execute_open_pr(agent, git, session=session, pull_requests=port,
                           records_dir=RECORDS, checkout_root=scratch_repo.root)

    assert agent.refusals and agent.refusals[0].kind == "gate-side-effect"
    assert port.calls == []
    assert _pr_records(scratch_repo.root) == []
    assert bs.is_live(registry, REPO, DRAFT) is True


def test_the_save_cli_verb_enforces_the_human_gate_itself(scratch_repo, tmp_path,
                                                          capsys):
    """The CLI is a FRESH PROCESS with no `serve.py` handler in front of it, so
    FR-019 is a PER-VERB obligation here (contracts/cli.md) — discharged through
    the ONE shared helper, called FIRST, before any read and any resolution."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    assert "_session_identity_gate" in inspect.getsource(cli_mod.cmd_gate_open_pr)
    assert "require_human_gate" in inspect.getsource(cli_mod._session_identity_gate)

    with pytest.raises(SystemExit) as exited:              # missing --actor
        cli_mod.main(["gate", "open-pr", "--repo-root", str(scratch_repo.root),
                      "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC])
    assert exited.value.code != 0

    capsys.readouterr()
    rc = cli_mod.main(["gate", "open-pr", "--repo-root", str(scratch_repo.root),
                       "--actor", "   ", "--scope-kind", bs.STAGED_TOPIC,
                       "--scope-id", TOPIC])
    assert rc == 1
    assert "refused" in capsys.readouterr().err
    assert _pr_records(scratch_repo.root) == []
    assert sg.SessionGit(scratch_repo.root).commits_ahead("main", DRAFT) == 1


def test_the_save_cli_verb_opens_the_pull_request_and_reports_it(scratch_repo,
                                                                  tmp_path,
                                                                  capsys,
                                                                  monkeypatch):
    """CLI parity (FR-020, contracts/cli.md): `--body-file` rather than inline
    text, and the process re-derives its own session registry (T033a). The port is
    injected here — the real adapter would perform an actual remote write with the
    engineer's own credential, which no test may do (quickstart step 6)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    monkeypatch.setattr(cli_mod, "_pull_request_port", lambda *a, **k: port)
    body_file = tmp_path / "pr-body.md"
    body_file.write_text("Two documents, one session.\n", encoding="utf-8")
    capsys.readouterr()

    rc = cli_mod.main(["gate", "open-pr", "--repo-root", str(scratch_repo.root),
                       "--actor", "dana", "--scope-kind", bs.STAGED_TOPIC,
                       "--scope-id", TOPIC, "--title", "Demo topic session",
                       "--body-file", str(body_file)])

    assert rc == 0
    out = capsys.readouterr().out
    assert DRAFT in out
    assert port.open_prs[DRAFT].url in out
    assert port.pushed == [DRAFT]
    assert ("open_or_update", DRAFT, "main", "Demo topic session",
            "Two documents, one session.\n") in port.calls
    records = _pr_records(scratch_repo.root)
    assert len(records) == 1
    record = yaml.safe_load(records[0].read_text(encoding="utf-8"))
    assert record["actor"] == "dana"
    assert record["target"] == {"ref": DRAFT}
    assert record["artifacts"][0]["kind"] == gc.ART_PULL_REQUEST


def test_the_save_cli_reports_the_engines_refusal_verbatim(scratch_repo, tmp_path,
                                                            capsys, monkeypatch):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    monkeypatch.setattr(cli_mod, "_pull_request_port",
                        lambda *a, **k: spr.FakePullRequests(
                            fail_push="gh auth login required"))
    capsys.readouterr()

    rc = cli_mod.main(["gate", "open-pr", "--repo-root", str(scratch_repo.root),
                       "--actor", "brett", "--scope-kind", bs.STAGED_TOPIC,
                       "--scope-id", TOPIC])

    assert rc == 1
    assert "gh auth login required" in capsys.readouterr().err
    assert _pr_records(scratch_repo.root) == []


def test_the_save_cli_offers_no_token_and_no_bypass_flag():
    """contracts/cli.md + D22: the CLI never accepts a token argument (the identity
    is the invoking engineer's ambient `gh` auth), and no flag merges, approves, or
    skips the record."""
    parser = cli_mod.build_parser()
    args = parser.parse_args(["gate", "open-pr", "--repo-root", ".", "--actor",
                              "brett", "--scope-kind", bs.STAGED_TOPIC,
                              "--scope-id", TOPIC])
    assert args.func is cli_mod.cmd_gate_open_pr
    assert args.records_dir == gc.DEFAULT_RECORDS_DIR       # _add_gate_identity_args
    assert args.title is None and args.body_file is None    # both OPTIONAL
    source = Path(cli_mod.__file__).read_text(encoding="utf-8")
    for flag in ("--token", "--gh-token", "--github-token", "--merge",
                 "--approve", "--admin", "--auto-merge", "--squash"):
        assert flag not in source, flag
    with pytest.raises(SystemExit):                         # --scope-id required
        parser.parse_args(["gate", "open-pr", "--repo-root", ".", "--actor",
                           "brett", "--scope-kind", bs.STAGED_TOPIC])


# ==========================================================================
# T059 — no path merges, approves, self-reviews, or bypasses protection: the
# PORT's ABSENT operations are the enforcement (FR-030)
# ==========================================================================

FORBIDDEN_PORT_OPERATIONS = (
    "merge", "merge_pull_request", "approve", "review", "self_review",
    "submit_review", "bypass", "bypass_protection", "enable_auto_merge",
    "auto_merge", "admin_merge", "squash", "rebase_merge", "protect",
    "set_protection", "dismiss_review",
)


def test_the_port_exposes_only_three_operations_and_none_of_them_approves():
    """The ABSENCE is the enforcement (contracts/session-ports.md): a test asserts
    on the absence, not on a refusal message, because a refusal could be removed
    while an absent method cannot be called at all."""
    assert spr.PORT_OPERATIONS == ("push", "open_or_update", "find_open")
    surfaces = (spr.PullRequestPort, spr.FakePullRequests, spr.GhPullRequests)
    for surface in surfaces:
        public = {name for name in dir(surface) if not name.startswith("_")}
        for forbidden in FORBIDDEN_PORT_OPERATIONS:
            assert forbidden not in public, (surface.__name__, forbidden)
        assert set(spr.PORT_OPERATIONS) <= public, surface.__name__
    # the protocol declares exactly the three, so a fourth cannot arrive quietly
    declared = {name for name in vars(spr.PullRequestPort)
                if not name.startswith("_")}
    assert declared == set(spr.PORT_OPERATIONS)


def test_the_pull_request_object_carries_nothing_that_could_merge():
    """`PullRequest` carries `url`, `number`, `state` and nothing that would let a
    caller merge or approve (contracts/session-ports.md)."""
    pr = spr.PullRequest(url="https://example.invalid/pr/1", number=1)
    assert {f.name for f in dataclasses.fields(pr)} == {"url", "number", "state"}
    assert pr.state == "open"
    for forbidden in FORBIDDEN_PORT_OPERATIONS:
        assert not hasattr(pr, forbidden), forbidden


def test_no_route_or_adapter_path_merges_approves_or_bypasses(scratch_repo,
                                                               tmp_path):
    """On the ROUTE as well as the port: the verb offers no merge/approve
    affordance, the engine calls none, and the real adapter shells out to no
    `gh pr merge` / `gh pr review` / `--admin`. The pin is on the COMMANDS and
    flags, not on the words — the module docstrings say `approve` and `bypass`
    precisely to record that neither is reachable."""
    for source in (inspect.getsource(gr.execute_open_pr),
                   inspect.getsource(gr._open_pr),
                   Path(spr.__file__).read_text(encoding="utf-8")):
        lowered = source.lower()
        for spelling in ("pr merge", "pr review", "pr ready", "pr approve",
                         "--admin", "--auto", "--approve", "--bypass",
                         "--squash", "--rebase"):
            assert spelling not in lowered, spelling

    # and the route accepts no body field that would ask for any of it
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    status, payload = _save(scratch_repo, registry, pull_requests=port,
                            merge=True, approve=True, admin=True)
    assert status == 200, payload                       # the extras are IGNORED
    assert port.open_prs[DRAFT].state == "open"         # never merged by the verb
    assert [name for name, *_ in port.calls] == ["find_open", "push",
                                                  "open_or_update"]


# ==========================================================================
# T060 — NEITHER readiness mechanism is consulted (FR-031, D21)
# ==========================================================================

def test_open_pr_proceeds_on_an_unready_topic_without_reaching_require_ready(
        scratch_repo, tmp_path, monkeypatch):
    """D21's deadlock is the reason: the blocking gate evaluates the SERVED
    checkout, a session's documents reach it only when the PR merges, so a
    readiness-gated save could never merge. Asserted NOT REACHED — not merely
    "the verb succeeded" — by replacing the helper with a spy that raises."""
    # a STANDING OPEN ITEM in the served checkout is what the blocking gate refuses
    # on, so the topic this session belongs to is genuinely not `ready`
    scratch_repo.write(f"ideation/staging/{TOPIC}/open.md",
                       "# Open Question\n\nStatus: brainstorm\n\n"
                       "## Notes\n\nTODO: decide the shape of the answer.\n")
    scratch_repo.commit("A standing open item on the tile",
                        f"ideation/staging/{TOPIC}/open.md")
    registry, created, worktree = _session(scratch_repo, tmp_path)
    health = live_topic_health(scratch_repo.root, TOPIC)
    assert health.get("status") != "ready", health
    with pytest.raises(gc.GateRefused):
        kickoff_mod._require_ready(scratch_repo.root, TOPIC)

    reached: list[tuple] = []

    def _spy(*args, **kwargs):
        reached.append((args, kwargs))
        raise AssertionError("open-pr reached kickoff._require_ready (FR-031)")

    monkeypatch.setattr(kickoff_mod, "_require_ready", _spy)
    monkeypatch.setattr(
        "ideation_dashboard.generator.live_topic_health",
        lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("open-pr consulted live topic health (FR-031)")))

    port = spr.FakePullRequests()
    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 200, payload
    assert payload["pull_request"] == port.open_prs[DRAFT].url
    assert reached == []
    assert len(_pr_records(scratch_repo.root)) == 1


def test_the_save_engine_names_no_readiness_mechanism_at_all(scratch_repo):
    """Structural, so the absence cannot be reintroduced by a later edit: neither
    mechanism's IDENTIFIER appears in the verb's own source, and the module that
    owns the blocking gate is not reachable from it at all (FR-031, G7)."""
    for source in (inspect.getsource(gr.execute_open_pr),
                   inspect.getsource(gr._open_pr)):
        lowered = source.lower()
        for spelling in ("require_ready", "live_topic_health", "topic_health",
                         "completeness", "kickoff"):
            assert spelling not in lowered, spelling


# ==========================================================================
# T061 — a second invocation UPDATES and reports the SAME pull request (FR-032)
# ==========================================================================

def test_a_second_save_updates_and_reports_the_same_pull_request(scratch_repo,
                                                                  tmp_path,
                                                                  ticking_clock):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = ObservingPullRequests(scratch_repo.root)
    first = _save(scratch_repo, registry, pull_requests=port,
                  title="First pass", body="one document")[1]
    # a second gate action on the branch, so the second save has something to push
    second_doc = _create(scratch_repo, registry, title="Second Draft")

    status, second = _save(scratch_repo, registry, pull_requests=port,
                           title="Second pass", body="two documents")

    assert status == 200, second
    assert second["pull_request"] == first["pull_request"]
    assert second["updated"] is True                   # reported as an UPDATE
    assert first["updated"] is False
    # exactly ONE pull request for the branch, ever
    assert len(port.open_prs) == 1
    assert [c for c in port.calls if c[0] == "open_or_update"] == [
        ("open_or_update", DRAFT, "main", "First pass", "one document"),
        ("open_or_update", DRAFT, "main", "Second pass", "two documents")]
    assert port.pushed == [DRAFT, DRAFT]               # pushed again, not re-opened
    # two records: an audit entry per action, neither overwriting the other
    assert len(_pr_records(scratch_repo.root)) == 2
    assert second["record"] != first["record"]


# ---- R2-13: a save never overwrites reviewer-facing text a human wrote --------

# as the route's own body parse hands it on (`_str_or_none` strips, and has since
# before this feature): the text a human typed into the save form's Body field
REVIEWER_BODY = ("Reviewer-facing description: this session carries the FDA "
                 "evidence documents D18-a and D18-b, reviewed by QA on 07-20.")


def test_a_blank_second_save_leaves_the_human_authored_title_and_body_intact(
        scratch_repo, tmp_path, ticking_clock):
    """Second-review finding R2-13, reproduced and closed. The route substituted
    its GENERATED title and the merge-commit notice on the UPDATE path as well as
    the create path, so a second save with the form left blank issued
    `gh pr edit --title 'Session draft/<topic>: <topic>' --body '<the notice>'` and
    replaced the reviewer-facing description of a series whose per-action commits
    are FDA-clearance traceability evidence (D18) — silently, reported as
    `updated: true`, while the UI copy said blank meant unchanged.

    Blank now means "supplied nothing", so the existing text is left alone and the
    response SAYS so."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    first = _save(scratch_repo, registry, pull_requests=port,
                  title="Session: FDA evidence", body=REVIEWER_BODY)[1]
    assert port.text(DRAFT) == ("Session: FDA evidence", REVIEWER_BODY)
    _create(scratch_repo, registry, title="Second Draft")

    status, second = _save(scratch_repo, registry, pull_requests=port)

    assert status == 200, second
    assert second["updated"] is True
    assert second["pull_request"] == first["pull_request"]
    # the human's text SURVIVES the save that reported "updated"
    assert port.text(DRAFT) == ("Session: FDA evidence", REVIEWER_BODY)
    assert [c for c in port.calls if c[0] == "open_or_update"] == [
        ("open_or_update", DRAFT, "main", "Session: FDA evidence", REVIEWER_BODY),
        ("open_or_update", DRAFT, "main", "Session: FDA evidence", REVIEWER_BODY)]
    # neither generated default reached the port on the update path
    assert gr.MERGE_COMMIT_NOTICE not in json.dumps(port.calls)
    assert f"Session {DRAFT}" not in json.dumps(port.calls)
    # and the human is TOLD which of the two things happened
    assert any("UNCHANGED" in note for note in second["notes"]), second
    assert any("never overwrites" in note for note in second["notes"]), second


def test_a_second_save_replaces_only_the_field_it_supplied(scratch_repo, tmp_path,
                                                           ticking_clock):
    """The other half: a human who DOES retitle the pull request gets exactly that
    — the title changes, the body they wrote earlier does not, and the response
    names what changed. "Preserve unless replaced" is not "never editable"."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    _save(scratch_repo, registry, pull_requests=port,
          title="Session: FDA evidence", body=REVIEWER_BODY)
    _create(scratch_repo, registry, title="Second Draft")

    status, second = _save(scratch_repo, registry, pull_requests=port,
                           title="Session: FDA evidence (ready for review)")

    assert status == 200, second
    assert port.text(DRAFT) == ("Session: FDA evidence (ready for review)",
                                REVIEWER_BODY)
    assert any("title was updated" in note for note in second["notes"]), second


def test_a_whitespace_only_field_is_not_authorship(scratch_repo, tmp_path,
                                                   ticking_clock):
    """A field holding spaces or a newline is a blank field a human tabbed
    through, not a title. Treating it as supplied would blank the pull request's
    title on the remote — the same destruction by a shorter path."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()
    _save(scratch_repo, registry, pull_requests=port,
          title="Session: FDA evidence", body=REVIEWER_BODY)
    _create(scratch_repo, registry, title="Second Draft")

    status, second = _save(scratch_repo, registry, pull_requests=port,
                           title="   ", body="\n \n")

    assert status == 200, second
    assert port.text(DRAFT) == ("Session: FDA evidence", REVIEWER_BODY)
    assert any("UNCHANGED" in note for note in second["notes"]), second


def test_the_first_save_still_names_the_pull_request_when_nothing_is_supplied(
        scratch_repo, tmp_path, ticking_clock):
    """The CREATE path is untouched by the preservation rule: a pull request has to
    be named something, so a first save with nothing supplied still gets the
    generated title and the merge-commit-never-squash notice (D18)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    port = spr.FakePullRequests()

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 200, payload
    assert payload["updated"] is False
    assert payload["notes"] == []
    title, body = port.text(DRAFT)
    assert title == f"Session {DRAFT}: {TOPIC}"
    assert body == gr.MERGE_COMMIT_NOTICE
    assert "MERGE COMMIT" in body


def test_the_real_adapter_edits_only_the_fields_the_save_supplied(scratch_repo):
    """R2-13 at the seam that actually speaks to GitHub: `gh pr edit --title X
    --body Y` REPLACES both fields, so an update must send only what was supplied —
    and a save that supplied neither must issue no `gh pr edit` at all, because
    there is nothing to edit and `gh` would refuse an empty edit anyway."""
    def adapter():
        runner = RecordingRunner(replies={
            "gh pr list": json.dumps([
                {"number": 12, "url": "https://example.invalid/pr/12",
                 "state": "OPEN"}])})
        return runner, _gh(runner, scratch_repo.root)

    runner, port = adapter()
    port.open_or_update(DRAFT, base="main", title="", body="",
                        default_title="Session x", default_body="notice")
    assert not any(command[:3] == ("gh", "pr", "edit")
                   for command in runner.commands), runner.commands

    runner, port = adapter()
    port.open_or_update(DRAFT, base="main", title="Retitled", body="",
                        default_title="Session x", default_body="notice")
    assert ("gh", "pr", "edit", DRAFT, "--title", "Retitled") in runner.commands

    runner, port = adapter()
    port.open_or_update(DRAFT, base="main", title="", body="A new description",
                        default_title="Session x", default_body="notice")
    assert ("gh", "pr", "edit", DRAFT, "--body",
            "A new description") in runner.commands

    # the CREATE path is where the defaults belong, and only there
    runner = RecordingRunner(replies={
        "gh pr list": "[]",
        "gh pr create": "https://example.invalid/pr/13\n"})
    port = _gh(runner, scratch_repo.root)
    port.open_or_update(DRAFT, base="main", title="", body="",
                        default_title="Session x", default_body="notice")
    assert ("gh", "pr", "create", "--head", DRAFT, "--base", "main",
            "--title", "Session x", "--body", "notice") in runner.commands


def test_the_second_save_still_writes_its_record_last(scratch_repo, tmp_path,
                                                     ticking_clock):
    """FR-029's ordering holds on the UPDATE path too: one record existed when the
    second save started, and no second one appeared before `open_or_update`."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    _save(scratch_repo, registry, pull_requests=spr.FakePullRequests())
    port = ObservingPullRequests(scratch_repo.root)
    port.open_or_update(DRAFT, base="main", title="t", body="b")   # the open PR
    port.seen.clear()
    port.calls.clear()

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 200, payload
    assert port.order == ["find_open", "push", "open_or_update"]
    assert [count for _, count in port.seen] == [1, 1, 1]
    assert len(_pr_records(scratch_repo.root)) == 2


# ==========================================================================
# T062 — on merge the session tears down, the BRANCH is deleted, and the main
# view refreshes (FR-033)
# ==========================================================================

def test_the_merge_ends_the_session_deletes_the_branch_and_refreshes_main(
        scratch_repo, tmp_path):
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    notebook_alias = session.notebook_alias
    from session_fixtures import FakeNotebookAdapter
    notebook = FakeNotebookAdapter()
    notebook.create(notebook_alias)
    _save(scratch_repo, registry, pull_requests=spr.FakePullRequests())
    snapshot = bs.session_snapshot_path(scratch_repo.root, DRAFT)
    assert snapshot.is_file()

    _merge_on_main(scratch_repo)                        # the Merge Master's action
    result = bs.reconcile_merged_session(git, session,
                                         checkout_root=scratch_repo.root,
                                         notebook=notebook)

    assert result.merged is True
    # TEARDOWN: worktree, registry entry, notebook (FR-021's three halves)
    assert sorted(result.teardown.torn_down) == ["notebook", "registry-entry",
                                                 "worktree"]
    assert not worktree.exists()
    assert worktree not in git.worktree_paths()
    assert not snapshot.exists()
    assert bs.is_live(registry, REPO, DRAFT) is False
    assert notebook.notebooks[notebook_alias].retired is True
    # the BRANCH is DELETED — the one thing the abandon ending never does
    assert result.teardown.branch_deleted is True
    assert result.teardown.branch_retained is False
    assert git.branch_exists(DRAFT) is False
    # and the MAIN VIEW refreshed: the merged document is in the shared snapshot
    assert result.teardown.main_view is not None
    assert registry.keys() == [(REPO, reg.DEFAULT_REF)]
    assert registry.active.ref == reg.DEFAULT_REF
    documents = [d.get("path") for d in
                 registry.get(REPO, reg.DEFAULT_REF).read_json()["documents"]]
    assert created["path"] in documents


def test_an_unmerged_session_is_not_ended_by_the_reconciliation(scratch_repo,
                                                                tmp_path):
    """The reconciliation OBSERVES; it never asserts. A session whose pull request
    has not merged is left exactly as it was — ending it would be
    `abandon-session`'s authority, and this path holds none."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)

    result = bs.reconcile_merged_session(git, session,
                                         checkout_root=scratch_repo.root)

    assert result.merged is False
    assert result.teardown is None
    assert result.reason and DRAFT in result.reason
    assert worktree.is_dir()
    assert bs.is_live(registry, REPO, DRAFT) is True
    assert git.branch_exists(DRAFT) is True


def test_a_session_with_no_commits_is_never_mistaken_for_a_merged_one(
        scratch_repo, tmp_path):
    """The trap in ancestry-based detection: a session opened with NOTHING written
    has a branch tip IDENTICAL to `main`, which is trivially an ancestor of it. It
    is not merged — nothing was — so the tip must also have to DIFFER."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    assert git.commits_ahead("main", DRAFT) == 0
    assert git.head(ref=DRAFT) == git.head(ref="main")

    state = bs.merge_state(git, DRAFT)

    assert state.merged is False
    assert bs.reconcile_merged_session(
        git, session, checkout_root=scratch_repo.root).merged is False
    assert git.branch_exists(DRAFT) is True


def test_a_squashed_landing_leaves_the_session_visible_rather_than_ending_it(
        scratch_repo, tmp_path):
    """D18 mandates a MERGE COMMIT, never a squash, because the per-action commit
    series is FDA traceability evidence. The detector therefore recognises exactly
    that shape: a squash-landed branch is NOT an ancestor of `main`, so the session
    stays live and visible — which SURFACES the D18 violation instead of hiding
    it. Nothing here changes a repository merge setting (plan Constraint 7)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    session = bs.open_session(git, registry, repository=REPO,
                              tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                              checkout_root=scratch_repo.root)
    scratch_repo.git("merge", "--squash", DRAFT)
    scratch_repo.git("commit", "-m", f"Squash {DRAFT}")

    result = bs.reconcile_merged_session(git, session,
                                         checkout_root=scratch_repo.root)

    assert result.merged is False
    assert git.branch_exists(DRAFT) is True
    assert worktree.is_dir()
    assert bs.is_live(registry, REPO, DRAFT) is True


def test_the_save_verb_reconciles_a_merged_branch_instead_of_pushing_it(
        scratch_repo, tmp_path):
    """The TRIGGER: `open-pr` is the one verb that knows about the pull request, so
    a re-invocation on a branch that has already merged ENDS the session rather
    than pushing merged work and opening a second pull request for it (FR-032,
    FR-033)."""
    registry, created, worktree = _session(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    port = spr.FakePullRequests()
    saved = _save(scratch_repo, registry, pull_requests=port)[1]
    _merge_on_main(scratch_repo)
    port.calls.clear()

    status, payload = _save(scratch_repo, registry, pull_requests=port)

    assert status == 200, payload
    assert payload["verb"] == "open-pr"
    assert payload["merged"] is True
    assert payload["branch_deleted"] is True
    assert sorted(payload["torn_down"]) == ["registry-entry", "worktree"]
    # NOTHING was pushed and NO second pull request was opened
    assert port.calls == []
    assert len(port.open_prs) == 1
    assert not worktree.exists()
    assert git.branch_exists(DRAFT) is False
    assert bs.is_live(registry, REPO, DRAFT) is False
    # and the reconciliation writes NO record: the durable audit is the
    # MAIN-RESIDENT `open-pr` record, which OUTLIVES the branch
    assert payload.get("record") is None
    assert len(_pr_records(scratch_repo.root)) == 1
    assert yaml.safe_load((scratch_repo.root / saved["record"]).read_text(
        encoding="utf-8"))["target"]["ref"] == DRAFT


def test_the_merge_ending_reuses_the_one_shared_teardown(scratch_repo, tmp_path):
    """FR-021/G8: ONE teardown, both endings. The merge ending adds exactly the
    branch deletion — it does not fork a second mechanism."""
    source = inspect.getsource(bs.reconcile_merged_session)
    assert "teardown_session(" in source
    assert "delete_branch=True" in source
    assert "worktree_remove" not in source              # not a second teardown
    assert "unregister_session_entry" not in source
    params = inspect.signature(bs.reconcile_merged_session).parameters
    assert {"git", "session", "checkout_root", "notebook"} <= set(params)


# ==========================================================================
# T064 — the REAL adapter: the invoking engineer's OWN ambient `gh` auth, and
# nothing else (FR-034, D22). No test here reaches a network or a real `gh`.
# ==========================================================================

class RecordingRunner:
    """An injected command runner. Every `GhPullRequests` test drives THIS — the
    real `gh` is never invoked, so no test can reach a network, a real credential,
    or a real pull request (FR-043, quickstart step 6)."""

    def __init__(self, replies=None, fail=None) -> None:
        self.commands: list[tuple[str, ...]] = []
        self.replies = dict(replies or {})
        self.fail = dict(fail or {})

    def run(self, *args, cwd=None):
        self.commands.append(tuple(args))
        key = " ".join(args[:3])
        code, err = self.fail.get(key, (0, ""))
        return subprocess.CompletedProcess(
            list(args), code, self.replies.get(key, ""), err)


def _gh(runner, root):
    return spr.GhPullRequests(root, runner=runner)


def test_the_real_adapter_accepts_no_token_and_stores_none():
    """D22: the identity is the INVOKING ENGINEER'S OWN `gh` authentication — no
    App, no stored token, and no hosted mode (the hosted plane's openxfactory App
    is normative but out of scope, FR-048)."""
    params = inspect.signature(spr.GhPullRequests.__init__).parameters
    for forbidden in ("token", "gh_token", "github_token", "credential",
                      "password", "app_id", "private_key", "installation",
                      "hosted", "plane"):
        assert forbidden not in params, forbidden
    source = Path(spr.__file__).read_text(encoding="utf-8")
    for spelling in ("GH_TOKEN", "GITHUB_TOKEN", "--with-token", "app_id",
                     "private_key", "installation_id"):
        assert spelling not in source, spelling
    adapter = spr.GhPullRequests(Path("."), runner=RecordingRunner())
    assert not [name for name in vars(adapter) if "token" in name.lower()]


def test_the_real_adapter_pushes_and_opens_with_the_ambient_auth(scratch_repo):
    runner = RecordingRunner(replies={
        "gh pr list": "[]",
        "gh pr create": "https://github.com/opensoft/openxFactory/pull/7\n",
    })
    adapter = _gh(runner, scratch_repo.root)

    adapter.push(DRAFT)
    pr = adapter.open_or_update(DRAFT, base="main", title="T", body="B")

    assert runner.commands[0] == ("git", "push", "--set-upstream", "origin", DRAFT)
    assert ("gh", "pr", "create", "--head", DRAFT, "--base", "main",
            "--title", "T", "--body", "B") in runner.commands
    assert pr.url == "https://github.com/opensoft/openxFactory/pull/7"
    assert pr.number == 7
    assert pr.state == "open"
    # no command carries a credential of any kind
    for command in runner.commands:
        assert not any(part.lower().startswith("--with-token")
                       or "token" in part.lower() for part in command), command


def test_the_real_adapter_updates_an_existing_pull_request(scratch_repo):
    """FR-032 in the adapter: an existing open PR is EDITED and reported, never
    re-created."""
    runner = RecordingRunner(replies={
        "gh pr list": json.dumps([
            {"number": 12, "url": "https://example.invalid/pr/12",
             "state": "OPEN"}]),
    })
    adapter = _gh(runner, scratch_repo.root)

    found = adapter.find_open(DRAFT)
    pr = adapter.open_or_update(DRAFT, base="main", title="T2", body="B2")

    assert found is not None and found.number == 12
    assert pr.number == 12
    assert pr.url == "https://example.invalid/pr/12"
    assert ("gh", "pr", "edit", DRAFT, "--title", "T2",
            "--body", "B2") in runner.commands
    assert not any(command[:3] == ("gh", "pr", "create")
                   for command in runner.commands)


def test_the_real_adapter_reports_a_missing_gh_auth_verbatim(scratch_repo):
    """contracts/cli.md: a missing or invalid `gh` auth is reported VERBATIM as the
    engine's refusal — the human is told what `gh` said, not a paraphrase."""
    message = ("gh: To get started with GitHub CLI, please run: gh auth login\n"
               "Alternatively, populate the GH_TOKEN environment variable")
    runner = RecordingRunner(fail={"gh pr list": (4, message),
                                   "gh auth status": (1, message)})
    adapter = _gh(runner, scratch_repo.root)

    with pytest.raises(spr.PullRequestRefused) as refused:
        adapter.find_open(DRAFT)

    assert "gh auth login" in str(refused.value)
    assert message.splitlines()[0] in str(refused.value)


def test_the_real_adapter_reports_a_push_failure_verbatim(scratch_repo):
    runner = RecordingRunner(fail={
        "git push --set-upstream": (128, "remote: Permission denied to brett.")})
    adapter = _gh(runner, scratch_repo.root)

    with pytest.raises(spr.PullRequestRefused) as refused:
        adapter.push(DRAFT)

    assert "Permission denied to brett." in str(refused.value)


def test_the_real_adapter_never_shells_out_to_anything_but_git_and_gh(scratch_repo):
    runner = RecordingRunner(replies={
        "gh pr list": "[]",
        "gh pr create": "https://example.invalid/pr/1\n"})
    adapter = _gh(runner, scratch_repo.root)

    adapter.push(DRAFT)
    adapter.open_or_update(DRAFT, base="main", title="T", body="B")
    adapter.find_open(DRAFT)

    assert {command[0] for command in runner.commands} == {"git", "gh"}
    for command in runner.commands:
        assert "shell" not in command
        assert not any(part.startswith("&&") or ";" in part for part in command)


def test_the_fake_and_the_real_adapter_satisfy_the_same_port(scratch_repo):
    """One port, two implementations, identical signatures — so a test against the
    fake is a test of the shape the real adapter must honour."""
    for name in spr.PORT_OPERATIONS:
        fake = inspect.signature(getattr(spr.FakePullRequests, name))
        real = inspect.signature(getattr(spr.GhPullRequests, name))
        assert list(fake.parameters) == list(real.parameters), name
    assert isinstance(spr.FakePullRequests(), spr.PullRequestPort)
    assert isinstance(spr.GhPullRequests(scratch_repo.root,
                                         runner=RecordingRunner()),
                      spr.PullRequestPort)


def test_the_harness_fake_is_the_production_fake():
    """T063's move: `session_fixtures` re-exports the ONE definition rather than
    keeping a second one that could drift from the port."""
    from session_fixtures import FakePullRequests as harness_fake
    from session_fixtures import PullRequest as harness_pr

    assert harness_fake is spr.FakePullRequests
    assert harness_pr is spr.PullRequest
