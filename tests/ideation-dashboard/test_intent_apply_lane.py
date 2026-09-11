"""The intent apply lane (add-ideation-intent-plane task 4.3).

A real git corpus per test: a pending_review derived possible in the
cross-reference index, committed, with the committed revision playing the
part of `snapshot_rev_seen`. The spec's lane scenarios drive the cases —
stale view refused, applied atomically (intent + record + artifacts in ONE
commit), refusals committed and never silent, allowlist rechecked
fail-closed, idempotent skip, dirty checkout refused.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import yaml

from carved_reach import source as carved_source

from openxdox import gate_console as gc
from ideation_dashboard import intent_apply_lane as lane

from test_gate_console import _accepting_validator, _derived_entry, _dispose_root

PID = "pos-derived-x"


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=False)


def _corpus(tmp_path) -> tuple[Path, str, Path]:
    """A committed dispose-able corpus: (root, seen_revision, allowlist)."""
    root = _dispose_root(tmp_path)
    (root / "ideation" / "cross-reference.md").write_text("seed\n",
                                                          encoding="utf-8")
    _git(root, "init", "-q", "-b", "main")
    # Repo-LOCAL identity, not just `-c` on the calls below. The apply lane
    # commits through its own `git commit` invocation, which carries no `-c`
    # flags and so falls back to ambient identity — present on a developer's
    # machine, absent on a CI runner, where all 21 tests in this file died with
    # "Author identity unknown (rolled back)". Setting it in the repo keeps the
    # fixture hermetic with respect to the host's global git config; reproduce
    # the failure with GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1.
    _git(root, "config", "user.name", "t")
    _git(root, "config", "user.email", "t@t")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t",
         "commit", "-q", "-m", "seed corpus")
    rev = _git(root, "rev-parse", "HEAD").stdout.strip()
    allowlist = tmp_path / "allowlist.json"
    allowlist.write_text(json.dumps({
        "actors": {"brett": ["dispose-possible", "ratify", "edit-apply",
                             "demote"],
                   "viewer": []},
    }), encoding="utf-8")
    return root, rev, allowlist


def _intent(rev: str, **over) -> dict:
    base = {
        "schema_version": 1, "kind": "gate-intent", "actor": "brett",
        "verb": "dispose-possible", "target": {"possible_id": PID},
        "args": {"outcome": "accepted", "note": "n"},
        "requested_at": "2026-08-10T12:00:00Z",
        "snapshot_rev_seen": rev, "status": "pending",
        "idempotency_key": "k-test-1",
    }
    base.update(over)
    return base


def _apply(root, intent, allowlist, tmp_path, **over):
    kwargs = dict(allowlist_path=allowlist,
                  index_validator=_accepting_validator(tmp_path), git=True)
    kwargs.update(over)
    return lane.apply_intent(root, intent, **kwargs)


def test_applied_atomically_intent_record_artifacts_one_commit(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent(rev), allowlist, tmp_path)
    assert report.outcome == "applied", report.reason
    assert report.record and report.intent_path
    # ONE commit past the seed carries intent + record + register together
    assert _git(root, "rev-list", "--count", "HEAD").stdout.strip() == "2"
    files = _git(root, "show", "--name-only", "--format=", "HEAD").stdout
    assert report.intent_path in files
    assert report.record in files
    assert "ideation/cross-reference.yaml" in files
    assert not _git(root, "status", "--porcelain").stdout.strip()
    # the committed intent carries the request->act chain
    doc = yaml.safe_load((root / report.intent_path).read_text())
    assert doc["status"] == "applied"
    assert doc["applied_record"] == report.record
    assert doc["actor"] == "brett"


def test_applied_record_carries_intent_plane_provenance(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent(rev), allowlist, tmp_path)
    record = yaml.safe_load((root / report.record).read_text())
    assert record["provenance"] == {"surface": "intent-plane",
                                    "console_presence": "ingress-auth"}


def test_stale_view_is_refused_and_the_refusal_committed(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    allowlist.write_text(json.dumps({
        "actors": {"brett": ["dispose-possible"],
                   "casey": ["dispose-possible"]},
    }), encoding="utf-8")
    # the target's entry advances past the second actor's view: brett
    # disposes it first, then casey decides on the OLD view (a distinct
    # request identity — a same-identity resubmission is a SKIP, per the
    # kernel's idempotency definition)
    first = _apply(root, _intent(rev), allowlist, tmp_path)
    assert first.outcome == "applied"
    report = _apply(root, _intent(rev, actor="casey",
                                  args={"outcome": "deferred"}),
                    allowlist, tmp_path)
    assert report.outcome == "refused"
    assert "materially advanced" in report.reason
    doc = yaml.safe_load((root / report.intent_path).read_text())
    assert doc["status"] == "refused" and doc["refusal_reason"]
    assert not _git(root, "status", "--porcelain").stdout.strip()  # committed


def test_unknown_snapshot_rev_is_unverifiable_and_refused(tmp_path):
    root, _, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent("f" * 40), allowlist, tmp_path)
    assert report.outcome == "refused"
    assert "unverifiable" in report.reason


def test_allowlist_rechecked_fail_closed(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent(rev, actor="viewer"), allowlist, tmp_path)
    assert report.outcome == "refused"
    assert "allowlist" in report.reason
    report = _apply(root, _intent(rev, actor="stranger",
                                  idempotency_key="k-3"), allowlist, tmp_path)
    assert report.outcome == "refused"
    missing = tmp_path / "absent.json"
    report = _apply(root, _intent(rev, idempotency_key="k-4"),
                    allowlist, tmp_path, allowlist_path=missing)
    assert report.outcome == "refused"


def test_engine_refusal_is_recorded_not_silent(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    intent = _intent(rev, target={"possible_id": "pos-unknown"},
                     idempotency_key="k-5")
    report = _apply(root, intent, allowlist, tmp_path)
    assert report.outcome == "refused"
    doc = yaml.safe_load((root / report.intent_path).read_text())
    assert doc["status"] == "refused"
    # no register change and no gate-action record landed
    files = _git(root, "show", "--name-only", "--format=", "HEAD").stdout
    assert "cross-reference.yaml" not in files
    assert ".gate-action.yaml" not in files


def test_already_applied_idempotency_key_skips(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    assert _apply(root, _intent(rev), allowlist, tmp_path).outcome == "applied"
    report = _apply(root, _intent(rev), allowlist, tmp_path)
    assert report.outcome == "skipped"
    assert _git(root, "rev-list", "--count", "HEAD").stdout.strip() == "2"


def test_dirty_checkout_is_refused_before_anything_is_read(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    (root / "stray.txt").write_text("uncommitted\n", encoding="utf-8")
    report = _apply(root, _intent(rev), allowlist, tmp_path)
    assert report.outcome == "error"
    assert "not clean" in report.reason


def test_shape_errors_persist_nothing(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    for bad in (
        _intent(rev, kind="not-an-intent"),
        _intent(rev, verb="create-document"),
        _intent(rev, target={"change_id": "wrong-key"}),
        _intent(rev, status="applied"),
        _intent(rev, actor=""),
        _intent(rev, snapshot_rev_seen="abc"),
    ):
        report = _apply(root, bad, allowlist, tmp_path)
        assert report.outcome == "error"
    assert _git(root, "rev-list", "--count", "HEAD").stdout.strip() == "1"


def test_args_carrying_a_target_key_are_refused_as_shape(tmp_path):
    """Codex P1 (PR #157): args must never override the validated target."""
    root, rev, allowlist = _corpus(tmp_path)
    bad = _intent(rev, args={"outcome": "accepted", "possible_id": "pos-other"})
    report = _apply(root, bad, allowlist, tmp_path)
    assert report.outcome == "error"
    assert "target keys" in report.reason
    assert _git(root, "rev-list", "--count", "HEAD").stdout.strip() == "1"


def test_validated_target_wins_any_body_collision(tmp_path, monkeypatch):
    """Belt under the brace: even if a clash slipped shape checks, the
    dispatched body carries the VALIDATED target."""
    root, rev, allowlist = _corpus(tmp_path)
    seen = {}

    def capture(verb, body, **kwargs):
        seen["body"] = body
        return 409, {"ok": False, "error": "gate_refused", "message": "x"}

    monkeypatch.setattr(lane, "run_gate_action", capture)
    monkeypatch.setattr(lane, "shape_error", lambda intent: None)
    bad = _intent(rev, args={"outcome": "accepted", "possible_id": "pos-other"})
    _apply(root, bad, allowlist, tmp_path)
    assert seen["body"]["possible_id"] == PID


def test_traversal_target_id_is_refused_before_any_write(tmp_path):
    """Codex P1 (PR #157): a path-shaped target id never reaches the tree."""
    root, rev, allowlist = _corpus(tmp_path)
    for evil in ("../../../escape", "a/b", "..", ".hidden", "-flag"):
        report = _apply(
            root, _intent(rev, target={"possible_id": evil}), allowlist,
            tmp_path)
        assert report.outcome == "error", evil
        assert "safe path segment" in report.reason
    assert not (root / ".github").exists()
    assert _git(root, "rev-list", "--count", "HEAD").stdout.strip() == "1"


def test_lane_deferred_verb_is_refused_with_the_reason_on_record(tmp_path):
    """Codex P2 (PR #157): edit-apply/kickoff have no executing route yet —
    the refusal says so instead of an anonymous unknown-verb 404."""
    root, rev, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent(rev, verb="edit-apply",
                                  target={"change_id": "some-change"},
                                  args={}, idempotency_key="k-def"),
                    allowlist, tmp_path)
    assert report.outcome == "refused"
    assert "not yet routable" in report.reason
    doc = yaml.safe_load((root / report.intent_path).read_text())
    assert doc["status"] == "refused"


def test_snapshot_verbs_get_a_fresh_snapshot_path(tmp_path, monkeypatch):
    """Codex P2 (PR #157): demote/derive-possibles routes demand a snapshot;
    the lane generates one and cleans it up after dispatch."""
    root, rev, allowlist = _corpus(tmp_path)
    seen = {}
    marker = tmp_path / "snap.json"

    def fake_snapshot(_root, _repository):
        marker.write_text("{}", encoding="utf-8")
        return marker

    def capture(verb, body, **kwargs):
        seen["snapshot_path"] = kwargs.get("snapshot_path")
        seen["existed"] = (kwargs.get("snapshot_path") is not None
                           and kwargs["snapshot_path"].exists())
        return 409, {"ok": False, "error": "gate_refused", "message": "x"}

    monkeypatch.setattr(lane, "_fresh_snapshot", fake_snapshot)
    monkeypatch.setattr(lane, "run_gate_action", capture)
    monkeypatch.setattr(lane, "stale_reason", lambda _root, _intent: None)
    _apply(root, _intent(rev, verb="demote",
                         target={"change_id": "some-change"},
                         args={"reason": "r"}, idempotency_key="k-snap"),
           allowlist, tmp_path)
    assert seen["snapshot_path"] == marker and seen["existed"]
    assert not marker.exists()  # unlinked after dispatch

    seen.clear()
    _apply(root, _intent(rev, idempotency_key="k-snap2"), allowlist, tmp_path)
    assert seen["snapshot_path"] is None


def test_engine_refusal_reason_is_the_engines_message(tmp_path):
    """Codex P2 (PR #157): the committed refusal carries the engine's own
    explanation, not the generic error code."""
    root, rev, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent(rev, target={"possible_id": "pos-unknown"},
                                  idempotency_key="k-msg"),
                    allowlist, tmp_path)
    assert report.outcome == "refused"
    assert report.reason != "gate_refused"
    assert "pos-unknown" in report.reason or "register" in report.reason


def test_same_second_intents_from_distinct_actors_never_collide(tmp_path):
    """Codex round-2 P1 (PR #157): two requests for one target in one second
    land as two artifacts; the second never overwrites the first."""
    root, rev, allowlist = _corpus(tmp_path)
    allowlist.write_text(json.dumps({
        "actors": {"brett": ["dispose-possible"],
                   "casey": ["dispose-possible"]},
    }), encoding="utf-8")
    first = _apply(root, _intent(rev), allowlist, tmp_path)
    assert first.outcome == "applied"
    second = _apply(root, _intent(rev, actor="casey", idempotency_key="k-2"),
                    allowlist, tmp_path)
    assert second.outcome == "refused"          # target advanced past its view
    assert second.intent_path != first.intent_path
    assert (root / first.intent_path).exists()
    assert (root / second.intent_path).exists()
    first_doc = yaml.safe_load((root / first.intent_path).read_text())
    assert first_doc["status"] == "applied"     # history intact


def test_re_refused_same_request_keeps_both_artifacts(tmp_path):
    """A same-identity re-decision suffixes an ordinal rather than
    overwriting the first refusal."""
    root, rev, allowlist = _corpus(tmp_path)
    bad = _intent(rev, target={"possible_id": "pos-unknown"},
                  idempotency_key="k-rr")
    one = _apply(root, bad, allowlist, tmp_path)
    two = _apply(root, bad, allowlist, tmp_path)
    assert one.outcome == two.outcome == "refused"
    assert one.intent_path != two.intent_path
    assert (root / one.intent_path).exists()
    assert (root / two.intent_path).exists()


def test_requested_at_is_required_and_must_parse(tmp_path):
    """Codex round-2 P2 (PR #157): a terminal intent must be
    schema-valid — requested_at present and RFC 3339."""
    root, rev, allowlist = _corpus(tmp_path)
    no_stamp = _intent(rev)
    del no_stamp["requested_at"]
    for bad in (no_stamp, _intent(rev, requested_at="not-a-date"),
                _intent(rev, requested_at=20260810)):
        report = _apply(root, bad, allowlist, tmp_path)
        assert report.outcome == "error"
        assert "requested_at" in report.reason
    assert _git(root, "rev-list", "--count", "HEAD").stdout.strip() == "1"


def test_stale_check_runs_even_on_the_test_seam(tmp_path, monkeypatch):
    """Codex round-2 P2 (PR #157): git=False skips commit mechanics, never
    the stale-view guard."""
    root, rev, allowlist = _corpus(tmp_path)
    seen = {}
    monkeypatch.setattr(lane, "stale_reason",
                        lambda _r, _i: seen.setdefault("ran", True) and "stale")
    report = _apply(root, _intent(rev), allowlist, tmp_path, git=False)
    assert seen.get("ran") is True
    assert report.outcome == "refused"


def test_the_cli_has_no_git_bypass():
    """Codex round-2 P2 (PR #157): --no-git left the public CLI."""
    import pytest as _pytest
    with _pytest.raises(SystemExit) as exc:
        lane.main(["--repo-root", "x", "--allowlist", "y",
                   "--intent-json", "{}", "--no-git"])
    assert exc.value.code == 2  # argparse: unrecognized argument


def test_requested_at_must_be_rfc3339_with_time_and_offset(tmp_path):
    """Codex round-3 P2 (PR #157): fromisoformat admits date-only and
    offset-less spellings the kernel's format checker rejects."""
    root, rev, allowlist = _corpus(tmp_path)
    for bad in ("2026-08-10", "2026-08-10T12:00:00", "2026-08-10 12:00:00Z"):
        report = _apply(root, _intent(rev, requested_at=bad), allowlist,
                        tmp_path)
        assert report.outcome == "error", bad
        assert "RFC 3339" in report.reason
    for good in ("2026-08-10T12:00:00Z", "2026-08-10T12:00:00.5+02:00"):
        assert lane.shape_error(_intent(rev, requested_at=good)) is None, good


def test_project_roster_unions_register_and_snapshot_index(tmp_path):
    """Codex round-3 P2 (PR #157): a registered repository not yet in any
    project must still be reachable for the project verbs."""
    register = tmp_path / "project-register.yaml"
    register.write_text(
        "projects:\n"
        "  - id: core\n"
        "    repositories:\n"
        "      - openxFactory\n"
        "  - id: domains\n"
        "    repositories:\n"
        "      - MedxFactory\n",
        encoding="utf-8")
    index_dir = tmp_path / "health" / "ideation-dashboard"
    index_dir.mkdir(parents=True)
    (index_dir / "index.json").write_text(json.dumps({
        "entries": [{"repository": "openxFactory"},
                    {"repository": "BrandNewRepo"}],
    }), encoding="utf-8")
    roster = lane._project_roster(tmp_path, register)
    names = sorted(row.repository for row in roster.entries())
    assert names == ["BrandNewRepo", "MedxFactory", "openxFactory"]


def test_unresolvable_register_yields_an_empty_roster(tmp_path):
    roster = lane._project_roster(tmp_path / "nowhere")
    assert roster.entries() == ()


def test_project_verbs_dispatch_with_the_roster(tmp_path, monkeypatch):
    """The route receives a registry whose entries carry the roster; other
    verbs keep dispatching without one."""
    root, rev, allowlist = _corpus(tmp_path)
    allowlist.write_text(json.dumps({
        "actors": {"brett": ["dispose-possible", "edit-project"]},
    }), encoding="utf-8")
    register = tmp_path / "project-register.yaml"
    register.write_text(
        "projects:\n  - id: core\n    repositories:\n      - openxFactory\n",
        encoding="utf-8")
    seen = {}

    def capture(verb, body, **kwargs):
        registry = kwargs.get("session_registry")
        seen[verb] = (None if registry is None
                      else [r.repository for r in registry.entries()])
        seen[verb + ":register"] = kwargs.get("project_register")
        return 409, {"ok": False, "error": "gate_refused", "message": "x"}

    monkeypatch.setattr(lane, "run_gate_action", capture)
    _apply(root, _intent(rev, verb="edit-project",
                         target={"project_id": "core"},
                         args={"add": ["openxFactory"]},
                         idempotency_key="k-r1"),
           allowlist, tmp_path, project_register=register)
    assert seen["edit-project"] == ["openxFactory"]
    assert seen["edit-project:register"] == register  # round-4: threaded through
    _apply(root, _intent(rev, idempotency_key="k-r2"), allowlist, tmp_path)
    assert seen["dispose-possible"] is None
    assert seen["dispose-possible:register"] is None


def test_forged_idempotency_key_never_suppresses_execution(tmp_path):
    """Codex round-5 P2 (PR #157): a reused applied key on an UNRELATED
    request must not skip — identity is recomputed lane-side."""
    root, rev, allowlist = _corpus(tmp_path)
    first = _apply(root, _intent(rev), allowlist, tmp_path)
    assert first.outcome == "applied"
    applied_doc = yaml.safe_load((root / first.intent_path).read_text())
    forged = _intent(rev, target={"possible_id": "pos-unrelated"},
                     idempotency_key=applied_doc["idempotency_key"])
    report = _apply(root, forged, allowlist, tmp_path)
    assert report.outcome != "skipped"          # it executes (and refuses on
    assert report.outcome == "refused"          # the unknown possible), on
    assert report.intent_path                   # the record


def test_dedupe_binds_to_identity_not_the_client_string(tmp_path):
    """The same request with a DIFFERENT client-supplied key still skips,
    and the committed artifact carries the lane-derived key."""
    root, rev, allowlist = _corpus(tmp_path)
    first = _apply(root, _intent(rev), allowlist, tmp_path)
    doc = yaml.safe_load((root / first.intent_path).read_text())
    assert doc["idempotency_key"] == lane.request_digest(doc)
    report = _apply(root, _intent(rev, idempotency_key="totally-different"),
                    allowlist, tmp_path)
    assert report.outcome == "skipped"


def test_propose_dispatches_with_the_rehydrated_session_registry(tmp_path, monkeypatch):
    """Codex round-6 P2 (PR #157): the live-session guard disables on a None
    registry — propose must carry the rehydrated one plus the repository key."""
    root, rev, allowlist = _corpus(tmp_path)
    allowlist.write_text(json.dumps({
        "actors": {"brett": ["dispose-possible", "propose"]},
    }), encoding="utf-8")
    seen = {}

    def capture(verb, body, **kwargs):
        seen[verb] = {"registry": kwargs.get("session_registry"),
                      "repository": kwargs.get("repository")}
        return 409, {"ok": False, "error": "gate_refused", "message": "x"}

    monkeypatch.setattr(lane, "run_gate_action", capture)
    monkeypatch.setattr(lane, "stale_reason", lambda _r, _i: None)
    _apply(root, _intent(rev, verb="propose", target={"topic_id": "some-topic"},
                         args={}, idempotency_key="k-p1"),
           allowlist, tmp_path, repository="openxFactory")
    assert seen["propose"]["registry"] is not None
    assert callable(seen["propose"]["registry"].entries)
    assert seen["propose"]["repository"] == "openxFactory"
    _apply(root, _intent(rev, idempotency_key="k-p2"), allowlist, tmp_path)
    assert seen["dispose-possible"]["registry"] is None
    assert seen["dispose-possible"]["repository"] is None


def test_manifest_digest_matches_the_grown_schema():
    """Codex round-6 P1 (PR #157): the registered digest tracks the bytes."""
    import hashlib
    repo = Path(__file__).resolve().parents[2]
    # POST-SHED (§ 5.2, RULED (a)): the schema is a `moved_verbatim` row at the
    # openXdox-spec leg and the digest `contracts/manifest.yaml` records is
    # unchanged, which is exactly what this test asserts — the manifest tracks
    # the BYTES, and the bytes did not move.
    schema = carved_source("contracts/schemas/gate-action-record.schema.yaml")
    manifest = (repo / "contracts/manifest.yaml").read_text()
    digest = hashlib.sha256(schema.read_bytes()).hexdigest()
    assert f"sha256: {digest}" in manifest


def test_terminal_artifacts_carry_validated_fields_only(tmp_path):
    """Codex round-7 P2 (PR #157): wire junk — schema-known fields with
    invalid values, unknown keys, junk target keys — never reaches the
    committed feed on either terminal path."""
    root, rev, allowlist = _corpus(tmp_path)
    poisoned = _intent(rev, idempotency_key="k-poison")
    poisoned["applied_record"] = []
    poisoned["refusal_reason"] = []
    poisoned["applied_at"] = {"not": "a time"}
    poisoned["dispatch_error"] = 42
    poisoned["junk_key"] = "junk"
    poisoned["target"] = {"possible_id": PID, "junk_target": "x",
                          "change_id": ""}
    report = _apply(root, poisoned, allowlist, tmp_path)
    assert report.outcome == "applied", report.reason
    doc = yaml.safe_load((root / report.intent_path).read_text())
    assert set(doc) == {"schema_version", "kind", "actor", "verb", "target",
                        "args", "requested_at", "snapshot_rev_seen", "status",
                        "idempotency_key", "applied_record", "applied_at"}
    assert doc["target"] == {"possible_id": PID}
    assert isinstance(doc["applied_record"], str) and doc["applied_record"]

    refused = _intent(rev, actor="viewer", idempotency_key="k-poison2")
    refused["refusal_reason"] = ["wire-supplied"]
    report = _apply(root, refused, allowlist, tmp_path)
    assert report.outcome == "refused"
    doc = yaml.safe_load((root / report.intent_path).read_text())
    assert set(doc) == {"schema_version", "kind", "actor", "verb", "target",
                        "args", "requested_at", "snapshot_rev_seen", "status",
                        "idempotency_key", "refusal_reason"}
    assert isinstance(doc["refusal_reason"], str)
    assert "allowlist" in doc["refusal_reason"]


def test_junk_target_member_cannot_bypass_the_idempotency_skip(tmp_path):
    """Codex round-8 P1 (PR #157): the digest and the stored artifact use
    ONE canonical target, so replaying a wire intent that carried a junk
    target member still skips."""
    root, rev, allowlist = _corpus(tmp_path)
    wire = _intent(rev, idempotency_key="k-junk1")
    wire["target"] = {"possible_id": PID, "junk_target": "x"}
    first = _apply(root, wire, allowlist, tmp_path)
    assert first.outcome == "applied", first.reason
    replay = _apply(root, dict(wire, idempotency_key="k-junk2"),
                    allowlist, tmp_path)
    assert replay.outcome == "skipped"
    clean = _apply(root, _intent(rev, idempotency_key="k-junk3"),
                   allowlist, tmp_path)
    assert clean.outcome == "skipped"  # junk spelling == clean spelling


def test_rejected_push_resets_the_decided_commit(tmp_path):
    """Codex round-9 P1 (PR #157): a non-fast-forward push never
    rebase-republishes the decision — the commit resets and the run errors
    so a fresh run revalidates."""
    root, rev, allowlist = _corpus(tmp_path)
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "--bare", "-q", "-b", "main", str(bare)],
                   check=True)
    _git(root, "remote", "add", "origin", str(bare))
    _git(root, "push", "-q", "-u", "origin", "main")
    # someone else lands on the remote after our clone
    other = tmp_path / "other"
    subprocess.run(["git", "clone", "-q", str(bare), str(other)], check=True)
    # Same reason as _corpus: repo-local identity so nothing here depends on
    # the host having a global git config.
    _git(other, "config", "user.name", "o")
    _git(other, "config", "user.email", "o@o")
    (other / "someone-elses.md").write_text("x\n", encoding="utf-8")
    _git(other, "-c", "user.name=o", "-c", "user.email=o@o", "add", "-A")
    _git(other, "-c", "user.name=o", "-c", "user.email=o@o",
         "commit", "-q", "-m", "concurrent work")
    pushed = _git(other, "push", "-q", "origin", "HEAD:main")
    assert pushed.returncode == 0, pushed.stderr

    report = _apply(root, _intent(rev), allowlist, tmp_path, push=True)
    assert report.outcome == "error"
    assert "push rejected" in report.reason
    assert report.committed is None
    # the decided commit is GONE locally; nothing landed remotely
    assert _git(root, "rev-parse", "HEAD").stdout.strip() == rev
    assert not _git(root, "status", "--porcelain").stdout.strip()
    remote_head = _git(root, "ls-remote", "origin", "main").stdout.split()[0]
    log = _git(other, "log", "--oneline", "-1").stdout
    assert "concurrent work" in log and remote_head


def test_out_of_range_rfc3339_components_are_rejected(tmp_path):
    """Codex round-9 P2 (PR #157): fromisoformat NORMALIZES +00:60 instead
    of rejecting it — the regex must range-check every component."""
    root, rev, allowlist = _corpus(tmp_path)
    for bad in ("2026-08-10T12:00:00+00:60", "2026-08-10T24:00:00Z",
                "2026-13-10T12:00:00Z", "2026-08-32T12:00:00Z",
                "2026-08-10T12:60:00Z"):
        report = _apply(root, _intent(rev, requested_at=bad), allowlist,
                        tmp_path)
        assert report.outcome == "error", bad
        assert "RFC 3339" in report.reason


def test_symbolic_refs_cannot_be_a_viewed_revision(tmp_path):
    """Codex round-10 P1 (PR #157): refs/heads/main always resolves to
    CURRENT, which would compare the target with itself."""
    root, rev, allowlist = _corpus(tmp_path)
    for bad in ("refs/heads/main", "mainbranch", "HEAD", "deadbeefXY"):
        report = _apply(root, _intent(rev, snapshot_rev_seen=bad),
                        allowlist, tmp_path)
        assert report.outcome == "error", bad
        assert "commit id" in report.reason


def test_abbreviated_and_full_revisions_share_one_identity(tmp_path):
    """The viewed revision canonicalizes to the full object id before the
    digest, so spelling length cannot mint a fresh identity."""
    root, rev, allowlist = _corpus(tmp_path)
    first = _apply(root, _intent(rev[:12], idempotency_key="k-abbr"),
                   allowlist, tmp_path)
    assert first.outcome == "applied", first.reason
    doc = yaml.safe_load((root / first.intent_path).read_text())
    assert doc["snapshot_rev_seen"] == rev  # full oid stored
    replay = _apply(root, _intent(rev, idempotency_key="k-full"),
                    allowlist, tmp_path)
    assert replay.outcome == "skipped"


def test_extra_kernel_known_target_member_does_not_mint_identity(tmp_path):
    """Codex round-10 P1 (PR #157): the canonical target is the verb's own
    member only."""
    base = {"schema_version": 1, "kind": "gate-intent", "actor": "b",
            "verb": "edit-project", "target": {"project_id": "core"},
            "args": {}, "requested_at": "2026-08-10T12:00:00Z",
            "snapshot_rev_seen": "a" * 40, "status": "pending"}
    with_extra = dict(base, target={"project_id": "core",
                                    "possible_id": "pos-stray"})
    assert lane.request_digest(base) == lane.request_digest(with_extra)
    assert lane.canonical_target("edit-project", with_extra["target"]) == {
        "project_id": "core"}


def test_commit_failure_rolls_the_checkout_back(tmp_path):
    """Codex round-10 P2 (PR #157): a failed commit must not strand a
    dirty tree that bricks every later run at the clean-tree gate."""
    root, rev, allowlist = _corpus(tmp_path)
    hook = root / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)
    report = _apply(root, _intent(rev), allowlist, tmp_path)
    assert report.outcome == "error"
    assert "rolled back" in report.reason
    assert _git(root, "rev-parse", "HEAD").stdout.strip() == rev
    assert not _git(root, "status", "--porcelain").stdout.strip()
    hook.unlink()
    retry = _apply(root, _intent(rev, idempotency_key="k-retry"),
                   allowlist, tmp_path)
    assert retry.outcome == "applied"  # the rolled-back run left no residue


def test_distinct_args_from_one_view_both_execute(tmp_path, monkeypatch):
    """Codex round-11 P1 (PR #157): edit-project add-A then add-B from ONE
    view are two decisions (D18 queueing) — identity alone must not
    swallow the second; a true duplicate still skips."""
    root, rev, allowlist = _corpus(tmp_path)
    allowlist.write_text(json.dumps({"actors": {"brett": ["edit-project"]}}),
                         encoding="utf-8")
    calls = []

    def capture(verb, body, **kwargs):
        calls.append(dict(body))
        return 200, {"ok": True, "verb": verb,
                     "record": "ideation/dashboard/gate-records/r.yaml"}

    monkeypatch.setattr(lane, "run_gate_action", capture)
    monkeypatch.setattr(lane, "stale_reason", lambda _r, _i: None)
    add_a = _intent(rev, verb="edit-project", target={"project_id": "core"},
                    args={"add": ["RepoA"]}, idempotency_key="k-a")
    add_b = _intent(rev, verb="edit-project", target={"project_id": "core"},
                    args={"add": ["RepoB"]}, idempotency_key="k-b")
    assert _apply(root, add_a, allowlist, tmp_path).outcome == "applied"
    assert _apply(root, add_b, allowlist, tmp_path).outcome == "applied"
    assert len(calls) == 2 and calls[1]["add"] == ["RepoB"]
    dup = _apply(root, dict(add_a, idempotency_key="k-c"), allowlist, tmp_path)
    assert dup.outcome == "skipped"
    assert len(calls) == 2


def test_terminal_write_failure_rolls_the_whole_pass_back(tmp_path, monkeypatch):
    """Codex round-11 P2 (PR #157): an intent write that throws AFTER the
    engine updated governed artifacts must not strand a dirty tree."""
    root, rev, allowlist = _corpus(tmp_path)

    def boom(_root, _dir, _intent):
        raise OSError("disk full")

    monkeypatch.setattr(lane, "_write_intent", boom)
    report = _apply(root, _intent(rev), allowlist, tmp_path)
    assert report.outcome == "error"
    assert "rolled back" in report.reason and "disk full" in report.reason
    assert _git(root, "rev-parse", "HEAD").stdout.strip() == rev
    assert not _git(root, "status", "--porcelain").stdout.strip()
    monkeypatch.undo()
    retry = _apply(root, _intent(rev, idempotency_key="k-after"),
                   allowlist, tmp_path)
    assert retry.outcome == "applied"


def test_intent_plane_provenance_pair_is_sanctioned():
    assert gc.SURFACE_INTENT in gc.SURFACES
    assert gc.PRESENCE_INGRESS in gc.CONSOLE_PRESENCES
    assert gc.INTENT_INGRESS.as_record() == {
        "surface": "intent-plane", "console_presence": "ingress-auth"}


def test_cli_applies_from_json(tmp_path, capsys):
    root, rev, allowlist = _corpus(tmp_path)
    rc = lane.main([
        "--repo-root", str(root), "--allowlist", str(allowlist),
        "--intent-json", json.dumps(_intent(rev)),
        "--index-validator", str(_accepting_validator(tmp_path)),
    ])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["outcome"] == "applied"
