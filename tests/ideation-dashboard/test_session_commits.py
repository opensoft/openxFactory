"""ONE commit per gate action, carrying documents AND record (T015; FR-006).

The invariant: a file-producing session verb (`create-document`,
`edit-document`) produces exactly ONE commit on the session branch, carrying
both what it wrote and the gate-action record attesting to it. A two-commit
trace is a defect, and an amend is not an option at all — a commit cannot
contain its own sha, and the amend-then-restamp dance leaves the record naming
a pre-amend sha the amend made unreachable.

So the chain is: the record carries its own action stamp, the commit message
repeats it as a `Gate-Action: <stamp>` trailer, the record's `commit`-kind
artifact references the STAMP, and that reference resolves by the introduced-by
rule to the commit that added the record file — which immediately after the
action is the branch TIP. The sha is RETURNED to the caller for the response and
never committed.

Phase 3's T020 extends this file with its two discriminating assertions (the
commit's TREE reachability, and `rev-list --count <fork>..<branch>` == N after a
sequence of N actions) and T021's externally-dispatching-verb refusal.
"""

from __future__ import annotations

import re
import subprocess

import pytest
import yaml

from session_fixtures import GATE_RECORDS_PREFIX

from ideation_dashboard import branch_session as bs
from ideation_dashboard import gate_console as gc
from ideation_dashboard import session_git as sg
from ideation_dashboard.boundary import BoundaryViolation, HumanGate, OutputBoundary
from ideation_dashboard.snapshot_registry import SnapshotRegistry

AT = "2026-07-26T12:00:00Z"
BRANCH = "draft/demo-topic"
DOC = "ideation/staging/demo-topic/note.md"
ALLOWLIST = (GATE_RECORDS_PREFIX, "ideation/staging/")


@pytest.fixture
def session(scratch_repo):
    """A live-ish session: the branch, its worktree, and a HumanGate rooted at
    the WORKTREE (not the served checkout), which is what makes the session
    record land in the worktree's copy of the records path (plan Constraint 10:
    session records for the file-producing verbs ride the session commit)."""
    git = sg.SessionGit(scratch_repo.root)
    worktree = bs.worktree_path(scratch_repo.root, BRANCH)
    git.worktree_add(BRANCH, worktree, "main")
    gate = HumanGate(worktree, list(ALLOWLIST), human_actor="brett")
    return git, worktree, gate, scratch_repo


def _record(*, at: str = AT, action: str = gc.ACTION_EDIT_DOCUMENT,
            document: str = DOC, artifacts=None) -> dict:
    stamp = bs.action_stamp(at)
    return gc.build_gate_action_record(
        actor="brett", action=action, at=at, ref=BRANCH, document=document,
        artifacts=artifacts if artifacts is not None else [bs.commit_artifact(stamp)])


def _write(worktree, relpath: str, text: str) -> str:
    target = worktree / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return relpath


# --------------------------------------------------------------------------
# the happy path: one commit, both files, sha returned not committed
# --------------------------------------------------------------------------

def test_one_gate_action_is_one_commit_carrying_document_and_record(session):
    git, worktree, gate, repo = session
    before = repo.served_fingerprint()
    _write(worktree, DOC, "# Note\n\nrewritten in the session.\n")

    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                   record=_record(), documents=[DOC])

    assert result.sha == git.head(worktree)
    assert git.commits_ahead("main", BRANCH) == 1
    listed = subprocess.run(["git", "show", "--name-only", "--format=", result.sha],
                            cwd=str(worktree), text=True, capture_output=True,
                            check=True).stdout.split()
    assert DOC in listed
    assert result.record_relpath in listed
    # SC-002: the served checkout never moved
    assert repo.served_fingerprint() == before


def test_the_commit_message_carries_the_matching_gate_action_trailer(session):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                   record=_record(), documents=[DOC])

    message = git.git(worktree, "log", "-1", "--format=%B").strip()
    assert f"Gate-Action: {result.stamp}" in message
    # the stamp is the one in the record's own FILENAME — the two must agree, or
    # the walk from record to commit and back is broken
    assert result.record_relpath.endswith(
        f"edit-document-{result.stamp}.gate-action.yaml")


def test_the_record_embeds_no_sha_and_the_sha_is_returned_instead(session):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                   record=_record(), documents=[DOC])

    committed = git.git(worktree, "show", f"{result.sha}:{result.record_relpath}")
    loaded = yaml.safe_load(committed)
    references = [a["reference"] for a in loaded["artifacts"]]
    assert result.stamp in references
    for reference in references:
        assert re.fullmatch(r"[0-9a-f]{7,40}", str(reference)) is None
    assert result.sha not in committed
    # the sha reaches the caller for the RESPONSE, and only there (FR-006)
    assert len(result.sha) == 40


def test_the_commit_artifact_resolves_through_introduced_by_to_the_branch_tip(session):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                   record=_record(), documents=[DOC])

    resolved = git.introduced_by(result.record_relpath, cwd=worktree)
    assert resolved == result.sha == git.head(worktree)


def test_a_sequence_of_actions_is_exactly_one_commit_each(session):
    git, worktree, gate, _ = session
    fork = git.head(worktree)
    stamps = []
    for n, at in enumerate(["2026-07-26T12:00:0%dZ" % i for i in range(3)], start=1):
        _write(worktree, DOC, f"# Note\n\nrevision {n}\n")
        result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                       record=_record(at=at), documents=[DOC])
        stamps.append(result.stamp)
        assert git.commits_ahead("main", BRANCH) == n

    # no amend anywhere: N actions, N commits, N distinct records
    assert len(set(stamps)) == 3
    count = int(subprocess.run(["git", "rev-list", "--count", f"{fork}..{BRANCH}"],
                               cwd=str(worktree), text=True, capture_output=True,
                               check=True).stdout.strip())
    assert count == 3


def test_the_records_stay_inside_the_worktree_and_not_in_the_served_checkout(session):
    git, worktree, gate, repo = session
    _write(worktree, DOC, "# Note\n")
    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                   record=_record(), documents=[DOC])

    assert result.record_path.is_file()
    assert worktree in result.record_path.parents
    assert not (repo.root / result.record_relpath).exists()
    assert not (repo.root / DOC).exists()


# --------------------------------------------------------------------------
# the refusals FR-006 asks for
# --------------------------------------------------------------------------

def test_a_caller_splitting_document_and_record_is_refused(session):
    """The realistic split: the documents are committed FIRST and the record is
    asked to follow. Then the record could only ride a second commit."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    git.stage(worktree, [DOC])
    git.commit(worktree, "documents only\n\nGate-Action: premature")
    ahead = git.commits_ahead("main", BRANCH)

    with pytest.raises(bs.SessionRefused) as exc:
        bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                              record=_record(), documents=[DOC])
    assert "different commit" in str(exc.value)
    # nothing was persisted by the refusal
    assert git.commits_ahead("main", BRANCH) == ahead


def test_an_action_with_no_document_cannot_use_the_commit_path(session):
    """`open-pr` and `abandon-session` are MAIN-RESIDENT and carry no commit
    artifact, so they must never reach this path (plan Constraint 10)."""
    git, worktree, gate, _ = session
    with pytest.raises(bs.SessionRefused):
        bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                              record=_record(action=gc.ACTION_OPEN_PR,
                                             document=None,
                                             artifacts=[{"kind": gc.ART_PULL_REQUEST,
                                                         "reference": "https://x/1"}]),
                              documents=[])


def test_a_record_with_no_commit_artifact_at_all_is_refused_before_any_write(session):
    """Tail finding B4 — the PRESENCE check the five sha checks assumed. The record
    of a file-producing action must NAME its commit: without this, an
    `edit-document` record whose only artifact was an `other` reference to the
    document was accepted and committed onto the session branch, where the pinned
    openxFactory validator rejects it (`artifacts: ... does not contain items
    matching the given schema`) — a schema-invalid governance record permanently on
    the branch that IS the traceability evidence, with nothing for FR-006's
    introduced-by chain to resolve."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    ahead = git.commits_ahead("main", BRANCH)

    with pytest.raises(bs.SessionRefused) as refused:
        bs.commit_gate_action(
            gate, git, worktree=worktree, branch=BRANCH, documents=[DOC],
            record=_record(artifacts=[{"kind": gc.ART_OTHER, "reference": DOC}]))

    assert "MUST carry" in str(refused.value)
    assert gc.ART_COMMIT in str(refused.value)
    assert git.commits_ahead("main", BRANCH) == ahead
    assert not list((worktree / GATE_RECORDS_PREFIX).rglob("*.gate-action.yaml"))


def test_a_record_whose_commit_artifact_names_a_sha_is_refused_before_any_write(session):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    ahead = git.commits_ahead("main", BRANCH)
    with pytest.raises(bs.SessionRefused):
        bs.commit_gate_action(
            gate, git, worktree=worktree, branch=BRANCH, documents=[DOC],
            record=_record(artifacts=[{"kind": gc.ART_COMMIT,
                                       "reference": "0" * 40}]))
    assert git.commits_ahead("main", BRANCH) == ahead
    assert not list((worktree / GATE_RECORDS_PREFIX).rglob("*.gate-action.yaml"))


def test_a_record_whose_commit_artifact_names_another_stamp_is_refused(session):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    with pytest.raises(bs.SessionRefused):
        bs.commit_gate_action(
            gate, git, worktree=worktree, branch=BRANCH, documents=[DOC],
            record=_record(artifacts=[{"kind": gc.ART_COMMIT,
                                       "reference": "20200101T000000Z"}]))


def test_the_commit_path_demands_a_human_gate(session):
    git, worktree, _, _ = session
    _write(worktree, DOC, "# Note\n")
    agent = OutputBoundary(worktree, list(ALLOWLIST), actor="agent")
    with pytest.raises(BoundaryViolation):
        bs.commit_gate_action(agent, git, worktree=worktree, branch=BRANCH,
                              record=_record(), documents=[DOC])


def test_the_commit_path_never_stages_everything(session):
    """The shared-tree house rule, at the session seam: an unrelated dirty file
    in the worktree must NOT be swept into the action's commit."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    _write(worktree, "ideation/staging/demo-topic/unrelated.md", "someone else\n")

    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                   record=_record(), documents=[DOC])
    listed = subprocess.run(["git", "show", "--name-only", "--format=", result.sha],
                            cwd=str(worktree), text=True, capture_output=True,
                            check=True).stdout.split()
    assert "ideation/staging/demo-topic/unrelated.md" not in listed
    assert "unrelated.md" in "".join(git.dirty_paths(worktree))


def test_a_document_outside_the_worktree_is_refused(session):
    git, worktree, gate, _ = session
    with pytest.raises(bs.SessionRefused) as exc:
        bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                              record=_record(document="../escape.md"),
                              documents=["../escape.md"])
    assert "not a fallback" in str(exc.value)


# --------------------------------------------------------------------------
# T016 — the execution-lane reconciliation is STATED, not implied
# --------------------------------------------------------------------------

def test_a_gate_action_record_is_not_an_execution_lane_result():
    """plan Constraint 13: `execution_lane/result.py`'s `PROHIBITED_CLAIMS`
    forbids a worker RESULT from claiming a branch, commit, pull request,
    approval, or merge. A gate-action RECORD is a different artifact by a
    different author (a human, under their own authority), which is exactly why
    it MAY name a branch, a commit, and a pull request. The two must never be
    unified, and the reconciliation is written down where a later reader will
    find it.

    (The `execution_lane.result` half of this pin — PROHIBITED_CLAIMS'
    exact tuple and the lane-result shape check — stayed with the
    engineering-owned `execution_lane` package in codexFactory
    (adopt-neutral-tooling-home tranche B, 2026-08-03; design D6 keeps that
    lane there). What remains here is the half this repo owns: the
    branch-session docstring carries the reconciliation, and the session
    vocabulary really does use the overlapping names.)"""
    doc = bs.__doc__ or ""
    assert "PROHIBITED_CLAIMS" in doc
    assert "execution_lane/result.py" in doc
    assert "never routed through the execution-lane result type" in doc

    # and the session record vocabulary really does use the forbidden names —
    # the overlap is the reason the comment has to exist
    assert gc.ART_COMMIT == "commit"
    assert gc.ART_PULL_REQUEST == "pull-request"
    record = _record()
    assert "ref" in record["target"]


# ==========================================================================
# T020 — the TWO DISCRIMINATING assertions
#
# Everything above this line asserts SHAPE. The two tests below assert the two
# things a plausible-but-wrong implementation would fail:
#
#   (a) REACHABILITY, not a string in a YAML field. The record's `commit`
#       artifact is resolved by the DEFINED rule — `git log --diff-filter=A
#       --format=%H <branch> -- <record-path>`, spelled out here rather than
#       borrowed from `SessionGit.introduced_by`, because a test that resolves
#       with the implementation's own helper would pass an implementation that
#       lied identically in both directions — and the resolved commit's TREE is
#       asserted to contain BOTH the document and the record. `git show
#       --name-only` reports a DIFF; `git ls-tree -r` reports what the commit
#       actually points at, which is the reviewer's real question.
#
#   (b) `git rev-list --count <fork>..<branch>` == N after N actions. This is
#       SC-003's promise, and it is the assertion an amend-based implementation
#       could never pass: amending would leave N-1, and a record-then-document
#       split would leave 2N.
# ==========================================================================


def _rule_resolved_commit(worktree, branch: str, record_relpath: str) -> str:
    """The introduced-by rule, spelled literally (the DEFINED resolution of a
    session record's `commit` artifact, data-model SessionCommit step 2)."""
    out = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%H", branch, "--",
         record_relpath],
        cwd=str(worktree), text=True, capture_output=True, check=True).stdout
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    assert lines, f"{record_relpath!r} was never ADDED on {branch}"
    return lines[-1]                      # the commit that INTRODUCED it


def _tree_paths(worktree, sha: str) -> set[str]:
    """What the commit's TREE contains — reachability, not a diff."""
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha],
                         cwd=str(worktree), text=True, capture_output=True,
                         check=True).stdout
    return {l.strip() for l in out.splitlines() if l.strip()}


def test_the_record_resolves_by_the_rule_to_the_tip_whose_tree_carries_both(session):
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n\nthe session's first revision.\n")

    result = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                   record=_record(), documents=[DOC])

    tip = subprocess.run(["git", "rev-parse", BRANCH], cwd=str(worktree),
                         text=True, capture_output=True, check=True).stdout.strip()
    resolved = _rule_resolved_commit(worktree, BRANCH, result.record_relpath)
    assert resolved == tip, (
        "the record's commit artifact must resolve, by the introduced-by rule, "
        "to the session branch TIP immediately after the action (FR-006)")
    assert resolved == result.sha

    tree = _tree_paths(worktree, resolved)
    assert DOC in tree
    assert result.record_relpath in tree, (
        "the document and its record must be REACHABLE from one commit — the "
        "artifact is a reachability claim, not a field value (FR-006)")


def test_the_rule_still_resolves_the_right_commit_after_later_actions(session):
    """The introduced-by rule is not "the tip": it is the commit that ADDED the
    record. After two more actions the FIRST record still resolves to the FIRST
    commit, which is what makes the reference durable rather than positional."""
    git, worktree, gate, _ = session
    _write(worktree, DOC, "# Note\n")
    first = bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                                 record=_record(at="2026-07-26T12:00:00Z"),
                                 documents=[DOC])
    for at in ("2026-07-26T12:00:01Z", "2026-07-26T12:00:02Z"):
        _write(worktree, DOC, f"# Note\n\n{at}\n")
        bs.commit_gate_action(gate, git, worktree=worktree, branch=BRANCH,
                              record=_record(at=at), documents=[DOC])

    assert _rule_resolved_commit(worktree, BRANCH, first.record_relpath) == first.sha
    tip = subprocess.run(["git", "rev-parse", BRANCH], cwd=str(worktree),
                         text=True, capture_output=True, check=True).stdout.strip()
    assert first.sha != tip
    assert first.record_relpath in _tree_paths(worktree, first.sha)


def test_after_n_gate_actions_the_branch_is_exactly_n_commits_ahead_of_its_fork(session):
    """SC-003, counted: N actions, N commits, no amend and no split. `fork` is
    the merge-base with `main`, so the count is the SESSION's own history and
    not an artefact of where `main` happens to be."""
    git, worktree, gate, _ = session
    fork = subprocess.run(["git", "merge-base", "main", BRANCH], cwd=str(worktree),
                          text=True, capture_output=True,
                          check=True).stdout.strip()

    documents = [
        "ideation/staging/demo-topic/one.md",
        "ideation/staging/demo-topic/two.md",
        "ideation/staging/demo-topic/three.md",
        "ideation/staging/demo-topic/four.md",
    ]
    records = []
    for n, document in enumerate(documents, start=1):
        _write(worktree, document, f"# Document {n}\n")
        result = bs.commit_gate_action(
            gate, git, worktree=worktree, branch=BRANCH,
            record=_record(at="2026-07-26T12:00:0%dZ" % n, document=document),
            documents=[document])
        records.append(result)
        count = int(subprocess.run(
            ["git", "rev-list", "--count", f"{fork}..{BRANCH}"], cwd=str(worktree),
            text=True, capture_output=True, check=True).stdout.strip())
        assert count == n, (
            f"after {n} gate actions the branch must be EXACTLY {n} commits "
            f"ahead of its fork point; it is {count} (SC-003, FR-006)")

    # every action's record resolves to its OWN commit, and each commit's tree
    # carries that action's document beside it
    for document, result in zip(documents, records):
        resolved = _rule_resolved_commit(worktree, BRANCH, result.record_relpath)
        assert resolved == result.sha
        assert {document, result.record_relpath} <= _tree_paths(worktree, resolved)
    assert len({r.sha for r in records}) == 4


# ==========================================================================
# T021 — an externally-dispatching verb inside a session refuses and reports
#
# FR-007: a verb whose effect reaches OUTSIDE the branch — a workflow dispatch
# that actually runs, a publication, an image build, a rollout — cannot be
# performed from inside a session, because the branch is unmerged exploration
# and the outside world would be acting on work no gate has accepted.
# ==========================================================================


def test_every_externally_dispatching_verb_is_refused_at_the_session_entry(scratch_repo):
    git = sg.SessionGit(scratch_repo.root)
    tile = bs.Tile(bs.STAGED_TOPIC, "demo-topic")

    assert bs.EXTERNALLY_DISPATCHING_VERBS, "the refusal set must not be empty"
    for verb in bs.EXTERNALLY_DISPATCHING_VERBS:
        registry = SnapshotRegistry()
        with pytest.raises(bs.ExternalDispatchRefused) as exc:
            bs.open_session(git, registry, repository="openxFactory", tile=tile,
                            verb=verb)
        message = str(exc.value)
        assert verb in message                       # the refusal REPORTS the verb
        assert "session" in message.lower()
        # nothing was persisted by the refusal
        assert len(registry.keys()) == 0
        assert not git.branch_exists("draft/demo-topic")


def test_the_refusal_names_why_rather_than_only_that(scratch_repo):
    git = sg.SessionGit(scratch_repo.root)
    with pytest.raises(bs.ExternalDispatchRefused) as exc:
        bs.open_session(git, SnapshotRegistry(), repository="openxFactory",
                        tile=bs.Tile(bs.STAGED_TOPIC, "demo-topic"),
                        verb="kickoff")
    message = str(exc.value)
    assert "FR-007" in message
    assert "outside" in message.lower()


def test_the_file_producing_session_verbs_are_not_in_the_refused_set():
    """The set is the OUTSIDE-reaching verbs, not "every verb": a session exists
    precisely so `create-document` and `edit-document` can run inside it."""
    for verb in ("create-document", "edit-document", "open-pr",
                 "abandon-session"):
        assert verb not in bs.EXTERNALLY_DISPATCHING_VERBS


def test_a_session_verb_opens_normally_while_a_dispatching_one_would_not(scratch_repo):
    git = sg.SessionGit(scratch_repo.root)
    registry = SnapshotRegistry()
    tile = bs.Tile(bs.STAGED_TOPIC, "demo-topic")

    opened = bs.open_session(git, registry, repository="openxFactory", tile=tile,
                             verb="create-document")
    assert opened.branch == BRANCH and opened.worktree.is_dir()

    with pytest.raises(bs.ExternalDispatchRefused):
        bs.open_session(git, registry, repository="openxFactory", tile=tile,
                        verb="publish")
    # the refusal did not tear the live session down
    assert bs.is_live(registry, "openxFactory", BRANCH) is True
