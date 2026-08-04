"""Session gate-action RECORD shapes, per-action (T014).

The table this asserts is data-model.md's "Per-action shape this feature MUST
emit", and the negatives are the governing change's four negative examples. The
shapes are not decoration: each one is the audit trail a reviewer reads back
from `main` after the pull request merges, and each omission has a named
failure —

| action | target | artifacts | residence |
|---|---|---|---|
| `edit-document` | `document` + `ref` | >=1 `commit` (reference = the ACTION STAMP, never a sha) | the WORKTREE, riding its own commit |
| `create-document` (in session) | `document` (+ `ref`) | `document` (+ `commit`) | the WORKTREE, riding its own commit |
| `open-pr` | `ref` | >=1 `pull-request`, NO `commit` | MAIN-RESIDENT |
| `abandon-session` | `ref` + `reason` | NO `commit` | MAIN-RESIDENT |

Each of the three new shapes IS validated against the pinned openxFactory
validator, in the last section of this file (PR #49 findings 15/B6). That guard was
missing while 15 other test modules had one, and its absence was not theoretical:
two reachable emissions committed records the same validator REJECTS — an
`edit-document` record with no `commit` artifact (B4) and an `open-pr` record whose
`pull-request` reference was the empty string, reported to the human as a success
(B5). The header here used to say the records were deliberately NOT validated
because the schema growth was openxFactory's to author; the growth landed (T091),
so the sentence became a licence for exactly that drift. The shapes are emitted
BY THEIR REAL VERBS there, because a shape validated only as a literal cannot
catch a route that builds a different one.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from conftest import find_openxfactory_validator
from session_fixtures import FakePullRequests, build_scratch_repo

from ideation_dashboard import branch_session as bs
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.boundary import HumanGate, OutputBoundary
from ideation_dashboard.generator import generate_snapshot

AT = "2026-07-26T12:00:00Z"
STAMP = "20260726T120000Z"
BRANCH = "draft/demo-topic"
RECORDS = gc.DEFAULT_RECORDS_DIR
TOPIC = "demo-topic"
VALIDATOR = find_openxfactory_validator()


def _gate(tmp_path, actor: str = "brett") -> HumanGate:
    return HumanGate(tmp_path, [RECORDS], human_actor=actor)


# --------------------------------------------------------------------------
# T011 — the enum growth, beside the existing constants
# --------------------------------------------------------------------------

def test_the_three_new_actions_exist_with_the_ratified_spellings():
    assert gc.ACTION_EDIT_DOCUMENT == "edit-document"
    assert gc.ACTION_OPEN_PR == "open-pr"
    assert gc.ACTION_ABANDON_SESSION == "abandon-session"


def test_the_two_new_artifact_kinds_exist_with_the_ratified_spellings():
    assert gc.ART_COMMIT == "commit"
    assert gc.ART_PULL_REQUEST == "pull-request"


def test_the_new_actions_are_distinct_from_the_main_resident_edit_apply():
    # FR-017: `edit-document` is a session verb; `edit-apply` is the untouched
    # main-resident redline path. Two verbs, never one renamed.
    assert gc.ACTION_EDIT_DOCUMENT != gc.ACTION_EDIT_APPLY
    assert gc.ACTION_EDIT_APPLY == "edit-apply"


# --------------------------------------------------------------------------
# T012 — `ref` on the record's target
# --------------------------------------------------------------------------

def test_build_gate_action_record_carries_the_session_ref_on_target():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT, ref=BRANCH,
        document="ideation/staging/demo-topic/note.md",
        artifacts=[bs.commit_artifact(STAMP)])
    assert record["target"]["ref"] == BRANCH
    assert record["target"]["document"] == "ideation/staging/demo-topic/note.md"


def test_ref_is_keyword_only_and_absent_when_not_passed():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_RATIFY, at=AT, change_id="add-x",
        artifacts=[{"kind": gc.ART_RATIFICATION_RECORD, "reference": "r.yaml"}])
    assert "ref" not in record["target"]
    with pytest.raises(TypeError):
        gc.build_gate_action_record(   # positional `ref` must not be accepted
            "brett", gc.ACTION_RATIFY, AT, [], BRANCH)  # type: ignore[misc]


def test_a_blank_ref_is_not_recorded():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_OPEN_PR, at=AT, ref="   ",
        artifacts=[{"kind": gc.ART_PULL_REQUEST, "reference": "https://x/1"}])
    assert "ref" not in record["target"]


def test_existing_record_shapes_are_byte_identical_without_a_ref():
    # the additive growth must not perturb any pre-existing verb's record
    before = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_PROPOSE, at=AT, topic_id="demo-topic",
        artifacts=[{"kind": gc.ART_WORKFLOW_JOB, "reference": "job.yaml"}])
    assert before["target"] == {"topic_id": "demo-topic"}
    assert list(before) == ["schema_version", "kind", "actor", "action",
                           "target", "at", "artifacts"]


# --------------------------------------------------------------------------
# T013 — the target-id resolution chain falls back to a slugged session ref
# --------------------------------------------------------------------------

def test_a_session_only_record_files_under_a_slugged_ref(tmp_path):
    """Constraint 10: an `open-pr` or `abandon-session` record on a CLUSTER or
    POSSIBLE tile names no change / possible / topic id and no document, so
    without the `ref` fallback `write_gate_action_record` would refuse and the
    verb would have nowhere to file its audit entry."""
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_OPEN_PR, at=AT, ref="cluster/cl-a",
        artifacts=[{"kind": gc.ART_PULL_REQUEST, "reference": "https://x/1"}])
    path = gc.write_gate_action_record(gate, RECORDS, record)

    rel = path.relative_to(tmp_path).as_posix()
    assert rel.startswith(RECORDS)
    target_id = rel[len(RECORDS):].split("/")[0]
    assert target_id == "cluster-cl-a"
    assert rel.endswith(f"open-pr-{STAMP}.gate-action.yaml")


def test_the_ref_fallback_comes_AFTER_document(tmp_path):
    # the chain is change/possible/topic -> document -> ref, so an
    # `edit-document` record files under its DOCUMENT exactly as
    # `create-document` already does
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT, ref=BRANCH,
        document="ideation/staging/demo-topic/note.md",
        artifacts=[bs.commit_artifact(STAMP)])
    path = gc.write_gate_action_record(gate, RECORDS, record)
    rel = path.relative_to(tmp_path).as_posix()
    assert "/ideation-staging-demo-topic-note/" in rel


def test_the_existing_chain_order_is_unchanged(tmp_path):
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_PROPOSE, at=AT, topic_id="demo-topic",
        ref=BRANCH,
        artifacts=[{"kind": gc.ART_WORKFLOW_JOB, "reference": "job.yaml"}])
    path = gc.write_gate_action_record(gate, RECORDS, record)
    # topic_id still wins over the new ref dimension
    assert f"/{RECORDS}demo-topic/" in "/" + path.relative_to(tmp_path).as_posix()


def test_a_record_naming_nothing_at_all_is_still_refused(tmp_path):
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_OPEN_PR, at=AT,
        artifacts=[{"kind": gc.ART_PULL_REQUEST, "reference": "https://x/1"}])
    with pytest.raises(gc.GateRefused):
        gc.write_gate_action_record(gate, RECORDS, record)


def test_a_hostile_ref_cannot_traverse_the_records_tree(tmp_path):
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_ABANDON_SESSION, at=AT,
        ref="../../../etc/cron.d/evil", reason="nope",
        artifacts=[{"kind": gc.ART_OTHER, "reference": "n/a"}])
    path = gc.write_gate_action_record(gate, RECORDS, record)
    rel = path.relative_to(tmp_path).as_posix()
    assert ".." not in rel
    assert rel.startswith(RECORDS)


# --------------------------------------------------------------------------
# T014 — the per-action table (data-model.md)
# --------------------------------------------------------------------------

def test_edit_document_needs_document_ref_and_a_commit_artifact():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT, ref=BRANCH,
        document="ideation/staging/demo-topic/note.md",
        artifacts=[bs.commit_artifact(STAMP)])
    assert record["target"] == {"ref": BRANCH,
                                "document": "ideation/staging/demo-topic/note.md"}
    kinds = [a["kind"] for a in record["artifacts"]]
    assert kinds == [gc.ART_COMMIT]


def test_the_commit_artifact_reference_is_the_action_stamp_and_never_a_sha():
    """FR-006: a commit cannot contain its own sha, so the reference is the
    record's own action id and resolution is the introduced-by rule."""
    artifact = bs.commit_artifact(STAMP)
    assert artifact == {"kind": "commit", "reference": STAMP}
    assert re.fullmatch(r"[0-9a-f]{7,40}", artifact["reference"]) is None
    # and the stamp is exactly the one in the record's own filename
    assert gc.gate_action_record_relpath(
        RECORDS, gc.ACTION_EDIT_DOCUMENT, "t", AT).endswith(
            f"edit-document-{STAMP}.gate-action.yaml")
    assert bs.action_stamp(AT) == STAMP


def test_create_document_in_a_session_carries_both_document_and_commit():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_CREATE_DOCUMENT, at=AT, ref=BRANCH,
        document="ideation/staging/demo-topic/new.md",
        artifacts=[{"kind": gc.ART_DOCUMENT,
                    "reference": "ideation/staging/demo-topic/new.md"},
                   bs.commit_artifact(STAMP)])
    kinds = {a["kind"] for a in record["artifacts"]}
    assert kinds == {gc.ART_DOCUMENT, gc.ART_COMMIT}
    assert record["target"]["ref"] == BRANCH


def test_open_pr_needs_ref_and_a_pull_request_artifact_and_no_commit():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_OPEN_PR, at=AT, ref=BRANCH,
        artifacts=[{"kind": gc.ART_PULL_REQUEST,
                    "reference": "https://example.invalid/pr/1"}])
    assert record["target"] == {"ref": BRANCH}
    kinds = [a["kind"] for a in record["artifacts"]]
    assert kinds == [gc.ART_PULL_REQUEST]
    assert gc.ART_COMMIT not in kinds, (
        "an open-pr record is MAIN-RESIDENT and adds no commit to the branch — a "
        "record committed after the push would never reach the pull request and "
        "would die with the branch at merge")


def test_abandon_session_needs_ref_and_reason_and_no_commit():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_ABANDON_SESSION, at=AT, ref=BRANCH,
        reason="the approach was wrong",
        artifacts=[{"kind": gc.ART_OTHER, "reference": BRANCH}])
    assert record["target"] == {"ref": BRANCH}
    assert record["reason"] == "the approach was wrong"
    assert gc.ART_COMMIT not in [a["kind"] for a in record["artifacts"]]


# ---- the negatives (chg 1.3's four negative examples) ----

def test_negative_an_edit_document_record_with_no_ref_is_incomplete():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT,
        document="ideation/staging/demo-topic/note.md",
        artifacts=[bs.commit_artifact(STAMP)])
    assert "ref" not in record["target"], (
        "the builder records only what it is given — the ROUTE is what must "
        "always populate `ref` in a session (D13)")


def test_negative_a_commit_artifact_referencing_a_sha_is_refused_by_the_write_path():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT, ref=BRANCH,
        document="d.md",
        artifacts=[{"kind": gc.ART_COMMIT, "reference": "a" * 40}])
    with pytest.raises(bs.SessionRefused):
        bs._refuse_embedded_sha(record, STAMP)


def test_a_record_naming_its_own_hex_shaped_stamp_is_refused_on_the_STAMP():
    """The second arm, reached for the first time (PR #49 second-review tail B1).

    The test above is named for the sha check but raises on the arm ABOVE it —
    `"a"*40` never equals the stamp — so the sha arm had no coverage at all. It
    also could not be right when it did run: it re-tested `reference`, which by
    then provably EQUALS `stamp`, so it was a statement about the stamp's shape in
    the wrong place. With a production `at` the stamp carries `T`/`Z` and the arm
    was dead; with a date-only `at` the stamp is `20260726`, hex-shaped, and a
    CORRECTLY formed record naming its own stamp was refused as "looks like a sha".

    Asked of the stamp it is well-founded: the refusal names the stamp, and the
    property that made the old arm exist still holds — an accepted stamp cannot be
    hex-shaped, so no accepted reference can look like a sha."""
    short_stamp = gc._stamp("2026-07-26")
    assert short_stamp == "20260726" and bs._SHA_RE.match(short_stamp), (
        "a date-only `at` really does produce a hex-shaped stamp")
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at="2026-07-26", ref=BRANCH,
        document="d.md", artifacts=[bs.commit_artifact(short_stamp)])

    with pytest.raises(bs.SessionRefused) as refused:
        bs._refuse_embedded_sha(record, short_stamp)

    assert "not a full action stamp" in str(refused.value)
    assert short_stamp in str(refused.value)
    # the well-formed stamp every route actually produces passes, and the
    # implication the old arm was reaching for holds for every accepted stamp
    bs._refuse_embedded_sha(
        gc.build_gate_action_record(
            actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT, ref=BRANCH,
            document="d.md", artifacts=[bs.commit_artifact(STAMP)]), STAMP)
    assert bs._ACTION_STAMP_RE.match(STAMP)
    assert bs._SHA_RE.match(STAMP) is None
    assert gc._stamp(gc._utcnow()) and bs._ACTION_STAMP_RE.match(gc._stamp(gc._utcnow()))


def test_negative_a_commit_artifact_referencing_another_stamp_is_refused():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT, ref=BRANCH,
        document="d.md",
        artifacts=[{"kind": gc.ART_COMMIT, "reference": "20250101T000000Z"}])
    with pytest.raises(bs.SessionRefused):
        bs._refuse_embedded_sha(record, STAMP)


def test_negative_an_open_pr_record_with_a_commit_artifact_is_the_shape_to_avoid(
        tmp_path):
    """The fourth negative: nothing in the BUILDER stops it, so the assertion has
    to live with the VERB — and it used to live nowhere at all.

    The line here read `assert gc.ART_COMMIT not in (gc.ART_PULL_REQUEST,)` — two
    module constants, no reference to any record, unfailable for any
    implementation (PR #49 second-review tail B7). Its only companion asserted the
    BAD shape IS present, so the negative the test is named for had zero coverage
    while the name said otherwise. The oracle is now the record the real `open-pr`
    route emits: main-resident, exactly one `pull-request` artifact, and no
    `commit` artifact — because a record committed after the push would never
    reach the pull request and would die with the branch at merge (FR-029, plan
    Constraint 10)."""
    permitted = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_OPEN_PR, at=AT, ref=BRANCH,
        artifacts=[{"kind": gc.ART_PULL_REQUEST, "reference": "https://x/1"},
                   bs.commit_artifact(STAMP)])
    assert gc.ART_COMMIT in [a["kind"] for a in permitted["artifacts"]], (
        "the builder records what it is given — that is why the VERB is the oracle")

    repo, registry, created = _session_world(tmp_path)
    status, saved = _act(repo, registry, "open-pr",
                         {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC},
                         session_pull_requests=FakePullRequests())

    assert status == 200, saved
    emitted = yaml.safe_load(
        (repo.root / saved["record"]).read_text(encoding="utf-8"))
    kinds = [a["kind"] for a in emitted["artifacts"]]
    assert kinds == [gc.ART_PULL_REQUEST], emitted
    assert gc.ART_COMMIT not in kinds


# --------------------------------------------------------------------------
# the written record round-trips as YAML with the ref intact
# --------------------------------------------------------------------------

def test_the_written_record_is_readable_yaml_carrying_the_ref(tmp_path):
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_ABANDON_SESSION, at=AT, ref=BRANCH,
        reason="changed my mind",
        artifacts=[{"kind": gc.ART_OTHER, "reference": BRANCH}])
    path = gc.write_gate_action_record(gate, RECORDS, record)
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert loaded["kind"] == gc.RECORD_KIND
    assert loaded["action"] == gc.ACTION_ABANDON_SESSION
    assert loaded["target"]["ref"] == BRANCH
    assert loaded["reason"] == "changed my mind"


def test_an_agent_boundary_still_cannot_author_a_session_record(tmp_path):
    """The structural human-only guard is unchanged by the growth (D16)."""
    from ideation_dashboard.boundary import BoundaryViolation
    agent = OutputBoundary(tmp_path, [RECORDS], actor="agent")
    with pytest.raises(BoundaryViolation):
        gc.require_human_gate(agent)


# ==========================================================================
# THE PINNED VALIDATOR — the three new shapes, as the REAL VERBS emit them
# (PR #49 findings 15 / B6, and the two emissions it would have caught: B4, B5)
#
# spec.md requires this feature's records to validate against openxFactory's grown
# `gate-action-record` schema, and nothing in this repo checked it while 15 other
# modules ran the pinned validator. The three shapes are emitted through their
# routes and validated as FILES on disk — session-resident for `edit-document`,
# main-resident for `open-pr` and `abandon-session` — so drift on either side of the
# `other`-kind abandon shim, or of the `commit` / `pull-request` artifact kinds,
# fails HERE instead of in the aggregation repo's own run, after the records are
# already audit evidence.
# ==========================================================================

pytestmark_validator = pytest.mark.skipif(
    VALIDATOR is None, reason="pinned openxFactory validator not reachable")


def _validate(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                          capture_output=True, text=True)


def _assert_valid(path: Path) -> None:
    proc = _validate(path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 error(s)" in proc.stdout


def _registry(repo, tmp_path):
    path = tmp_path / "main-snapshot.json"
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _act(repo, registry, verb, body, **over):
    # The gateway declares itself exactly as `serve.py`'s handler does (D23,
    # Brett's 2026-07-27 ruling item 3): the route TAKES the fact, so a caller
    # standing in for a gateway must declare one, and the records below are
    # therefore the shapes the HTTP door really emits. That the DOOR itself sets
    # this — rather than a test constant — is pinned through a live server in
    # test_gateway_provenance.py; here it is what makes the validated shape the
    # production shape.
    over.setdefault("provenance", gc.HTTP_CONSOLE_TOKEN)
    return gr.run_gate_action(
        verb, body, checkout_root=repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=repo.repository, **over)


# The block every record emitted through this file's routes must carry (D23). It
# is asserted BESIDE the pinned validator, not instead of it: the validator owns
# the two required inner fields and the two enums, and this owns "the route
# actually stamped it", which no schema can require (`provenance` is optional
# there, deliberately, so pre-growth records stay valid).
EXPECTED_PROVENANCE = {"surface": "http", "console_presence": "console-token"}


def _session_world(tmp_path):
    """A live session with one document in it, opened through the real route."""
    repo = build_scratch_repo(tmp_path)
    registry = _registry(repo, tmp_path)
    status, created = _act(repo, registry, "create-document", {
        "title": "First Draft", "summary": "The session's first document.",
        "topics": ["alpha"], "area": f"ideation/staging/{TOPIC}/",
        "repository_context": repo.repository, "repository": repo.repository,
        "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC})
    assert status == 200, created
    return repo, registry, created


@pytestmark_validator
def test_the_edit_document_record_its_verb_emits_validates(tmp_path):
    """SESSION-RESIDENT: the record rides its action's commit inside the worktree,
    so it is read back from the worktree it was committed in."""
    repo, registry, created = _session_world(tmp_path)
    content = tmp_path / "replacement.md"
    content.write_text("# First Draft\n\nrewritten.\n", encoding="utf-8")

    status, edited = _act(repo, registry, "edit-document", {
        "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
        "document": created["path"],
        "content": content.read_text(encoding="utf-8")})

    assert status == 200, edited
    worktree = bs.worktree_path(repo.root, BRANCH)
    record = worktree / edited["record"]
    assert record.is_file(), edited
    loaded = yaml.safe_load(record.read_text(encoding="utf-8"))
    assert loaded["action"] == gc.ACTION_EDIT_DOCUMENT
    assert [a["kind"] for a in loaded["artifacts"]] == [gc.ART_COMMIT]
    assert loaded["provenance"] == EXPECTED_PROVENANCE
    _assert_valid(record)


@pytestmark_validator
def test_the_open_pr_record_its_verb_emits_validates(tmp_path):
    """MAIN-RESIDENT (FR-029), which is why it is read from the served checkout."""
    repo, registry, created = _session_world(tmp_path)

    status, saved = _act(repo, registry, "open-pr",
                         {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC},
                         session_pull_requests=FakePullRequests())

    assert status == 200, saved
    record = repo.root / saved["record"]
    loaded = yaml.safe_load(record.read_text(encoding="utf-8"))
    assert loaded["action"] == gc.ACTION_OPEN_PR
    assert [a["kind"] for a in loaded["artifacts"]] == [gc.ART_PULL_REQUEST]
    assert loaded["artifacts"][0]["reference"] == saved["pull_request"]
    assert loaded["provenance"] == EXPECTED_PROVENANCE
    _assert_valid(record)


@pytestmark_validator
def test_the_abandon_session_record_its_verb_emits_validates(tmp_path):
    """The `other`-kind shim is the one that satisfies `artifacts.minItems: 1` for
    an action with no artifact of its own, so it is the shape most exposed to drift
    on either side of the seam."""
    repo, registry, created = _session_world(tmp_path)

    status, ended = _act(repo, registry, "abandon-session", {
        "scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
        "reason": "the spike answered its question"})

    assert status == 200, ended
    record = repo.root / ended["record"]
    loaded = yaml.safe_load(record.read_text(encoding="utf-8"))
    assert loaded["action"] == gc.ACTION_ABANDON_SESSION
    assert [a["kind"] for a in loaded["artifacts"]] == [gc.ART_OTHER]
    assert loaded["provenance"] == EXPECTED_PROVENANCE
    _assert_valid(record)


@pytestmark_validator
def test_the_validator_rejects_an_edit_document_record_with_no_commit_artifact(
        tmp_path):
    """B4, both halves. The validator REJECTS the shape — proving this guard would
    have caught it — and `commit_gate_action` now refuses to commit it, so the
    rejected shape can no longer reach the branch that is the evidence series."""
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=AT, ref=BRANCH,
        document="ideation/staging/demo-topic/note.md",
        artifacts=[{"kind": gc.ART_OTHER,
                    "reference": "ideation/staging/demo-topic/note.md"}])
    path = gc.write_gate_action_record(gate, RECORDS, record)

    proc = _validate(path)

    assert proc.returncode == 1, proc.stdout
    assert "artifacts" in proc.stdout
    with pytest.raises(bs.SessionRefused) as refused:
        bs._refuse_missing_commit_artifact(record, STAMP)
    assert "MUST carry" in str(refused.value)


@pytestmark_validator
def test_the_validator_rejects_an_open_pr_record_with_an_empty_reference(tmp_path):
    """B5's half of the same guard: the schema requires a NON-EMPTY reference, and
    the port coerces a missing url to ''. The route refuses that before any record
    is built (see test_session_lifecycle.py); this pins that the shape it would
    otherwise have written is one the pinned validator rejects."""
    gate = _gate(tmp_path)
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_OPEN_PR, at=AT, ref=BRANCH,
        artifacts=[{"kind": gc.ART_PULL_REQUEST, "reference": ""}])
    path = gc.write_gate_action_record(gate, RECORDS, record)

    proc = _validate(path)

    assert proc.returncode == 1, proc.stdout
    assert "non-empty" in proc.stdout
