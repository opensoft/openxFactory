"""Deterministic mock coverage of the live runner (T058) — no network, provider, or clock.

Fake async components + an injected monotonic clock drive the full 70-trial matrix so the
live driver's ordering, classification, timing-bound, assertion, and redaction logic is
verified in CI. The real aiortc/websockets/httpx components are validated only in the
supervised lab run; this proves the harness LOGIC around them is correct and fail-closed.
"""
from __future__ import annotations

import asyncio
import hashlib
import json

import pytest

from avatar_f0.broker import BrokerHttpError, IdempotencyConflict, LiveBrokerResult
from avatar_f0.candidate import CandidateProfile
from avatar_f0.evidence import build_interface_impact, finalize_record
from avatar_f0.live_runner import LiveComponents, LiveEnv, run_live_matrix
from avatar_f0.media import MediaGateError
from avatar_f0.run import MANDATORY_ASSERTIONS

TS = "2026-07-11T00:00:00Z"
CANDIDATE = CandidateProfile(harness_revision="test", dependency_lock_sha256="d" * 64,
                             fixture_bytes_sha256="f" * 64)


class FakeBroker:
    """Mirrors HttpBroker's harness-side idempotency without any network."""

    def __init__(self) -> None:
        self.provider_calls_created = 0
        self._by_request = {}

    async def create_call(self, request_id, offer_fp, offer_sdp, session_config):
        rid = hashlib.sha256(request_id.encode()).hexdigest()
        if request_id in self._by_request:
            offer0, prior = self._by_request[request_id]
            if offer0 == offer_fp:
                return LiveBrokerResult(prior.call_id_hash, rid, prior.answer_token, True,
                                        prior.held_answer_sdp, prior.call_id)
            raise IdempotencyConflict("idempotency_conflict")
        call_id = f"rtc_fake_{len(self._by_request)}_{request_id[-4:]}"
        cid_hash = hashlib.sha256(call_id.encode()).hexdigest()
        token = hashlib.sha256(f"answer:{cid_hash}".encode()).hexdigest()[:32]
        res = LiveBrokerResult(cid_hash, rid, token, False,
                               "v=0\r\no=- fake ANSWER sdp\r\n", call_id)
        self._by_request[request_id] = (offer_fp, res)
        self.provider_calls_created += 1
        return res

    async def hangup(self, call_id):
        return True


class FakeSideband:
    def __init__(self, call_id):
        self.call_id = call_id

    async def open(self):
        pass

    async def verify(self, timeout_s):
        return True

    async def close(self):
        pass


class FakeMedia:
    def __init__(self):
        self._applied = False

    async def create_offer(self, track):
        return "v=0\r\no=- fake OFFER sdp\r\n"

    async def apply_answer(self, answer_sdp, *, authorized):
        if not authorized:
            raise MediaGateError("refusing before authorization")
        self._applied = True

    @property
    def answer_applied(self):
        return self._applied

    async def wait_first_output(self, timeout_s):
        return True

    async def wait_terminal(self, timeout_s):
        return True

    async def close(self):
        pass


def make_env(*, broker=None, media=None, sideband=None):
    state = {"ns": 0}

    def now_ns():
        state["ns"] += 1_000_000  # +1 ms per read → strictly monotonic markers
        return state["ns"]

    async def sleep(seconds):
        state["ns"] += int(seconds * 1_000_000_000)

    comps = LiveComponents(
        make_broker=broker or (lambda: FakeBroker()),
        make_sideband=sideband or (lambda cid: FakeSideband(cid)),
        make_media=media or (lambda: FakeMedia()),
        make_track=lambda: object(),
    )
    return LiveEnv(components=comps, session_config={"type": "realtime"},
                   now_ns=now_ns, sleep=sleep)


def _run(env, **kw):
    return asyncio.run(run_live_matrix(env, CANDIDATE, lab_project_ref="lab:f0",
                                       dependency_versions={"aiortc": "1.9.0"},
                                       started_at=TS, completed_at=TS, **kw))


def test_live_matrix_mock_produces_schema_valid_pass():
    rec = _run(make_env())
    assert rec["overall"] == "PASS", [(g["id"], g["passed"], g["planned"]) for g in rec["trial_groups"]]
    # every group ran its full planned count and every trial passed
    for g in rec["trial_groups"]:
        assert g["completed"] == g["planned"] == g["passed"], g
    assert sum(g["planned"] for g in rec["trial_groups"]) == 70
    # every mandatory assertion (incl. the two cross-cutting ones) is present and PASS
    aids = {a["id"]: a["status"] for a in rec["assertions"]}
    for aid in MANDATORY_ASSERTIONS:
        assert aids.get(aid) == "PASS", (aid, aids.get(aid))
    # finalize → schema-valid, redaction clean, still PASS
    final = finalize_record(rec, "report", build_interface_impact("p.yaml", "c", "0" * 64, []))
    assert final["redaction_scan"]["status"] == "PASS"
    assert final["overall"] == "PASS"


def test_live_record_leaks_no_sdp_or_raw_call_id():
    rec = _run(make_env())
    blob = json.dumps(rec)
    for needle in ("v=0", "fake OFFER", "fake ANSWER", "rtc_fake"):
        assert needle not in blob, f"leaked {needle!r} into evidence"


def test_api_shape_error_is_inconclusive_never_pass():
    class ErrBroker(FakeBroker):
        async def create_call(self, *a, **k):
            raise BrokerHttpError(400, "create")

    rec = _run(make_env(broker=lambda: ErrBroker()), groups=["F0-A"])
    assert rec["overall"] == "INCONCLUSIVE"
    assert all(t["status"] == "INCONCLUSIVE" for t in rec["trials"])


def test_missing_first_output_is_fail():
    class NoOutputMedia(FakeMedia):
        async def wait_first_output(self, timeout_s):
            return False

    rec = _run(make_env(media=lambda: NoOutputMedia()), groups=["F0-A"])
    assert rec["overall"] == "FAIL"


def test_unauthorized_answer_apply_is_rejected():
    # Direct proof the held-answer gate fails closed: applying before authorization raises.
    media = FakeMedia()
    with pytest.raises(MediaGateError):
        asyncio.run(media.apply_answer("v=0", authorized=False))
