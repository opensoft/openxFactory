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

from ideation_dashboard import gate_console as gc
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
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t",
         "commit", "-q", "-m", "seed corpus")
    rev = _git(root, "rev-parse", "HEAD").stdout.strip()
    allowlist = tmp_path / "allowlist.json"
    allowlist.write_text(json.dumps({
        "actors": {"brett": ["dispose-possible", "ratify"], "viewer": []},
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
    # the target's entry advances past the intent's view: dispose it first
    first = _apply(root, _intent(rev), allowlist, tmp_path)
    assert first.outcome == "applied"
    report = _apply(root, _intent(rev, idempotency_key="k-test-2",
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
