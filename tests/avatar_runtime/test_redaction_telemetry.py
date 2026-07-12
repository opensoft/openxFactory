"""Redaction validator rejects protected content; safe records publish (ARR-007-S04, FR-033, SC-007)."""

from __future__ import annotations

from xfactory.avatar_runtime.telemetry import TelemetryRecord, TelemetrySink


def _rec(refs):
    return TelemetryRecord(test_id="t1", transition="x", clock_ts=5, reason="ok", refs=refs)


def test_sdp_content_is_rejected():
    assert not _rec({"blob": "a=candidate:1 1 udp 2130706431 10.0.0.1 5000 typ host"}).redaction_ok()


def test_credential_is_rejected():
    assert not _rec({"auth": "token=abcd1234EFGH5678ijkl"}).redaction_ok()
    assert not _rec({"key": "sk-ABCDEFGHIJKLMNOPQRSTUVWX"}).redaction_ok()


def test_forbidden_key_is_rejected():
    assert not _rec({"answer": "anything"}).redaction_ok()
    assert not _rec({"credential": "fixture:x"}).redaction_ok()


def test_raw_uuid_is_rejected():
    assert not _rec({"id": "123e4567-e89b-12d3-a456-426614174000"}).redaction_ok()


def test_safe_references_are_allowed():
    assert _rec({"grant_ref": "sha256:deadbeef", "profile": "fixture:profile-a"}).redaction_ok()


def test_sink_drops_protected_and_publishes_safe():
    sink = TelemetrySink()
    assert sink.publish(_rec({"grant_ref": "sha256:ok"})) is True
    assert sink.publish(_rec({"answer": "m=audio 9 UDP"})) is False
    assert len(sink.published) == 1 and sink.dropped == 1
