"""Live trial execution against the real provider (T058).

Live counterpart of :mod:`avatar_f0.trials.base`. Drives the real broker / sideband /
media components on a REAL monotonic clock, but reuses the exact same evidence shape and
classification as the offline path — so a live PASS is subject to identical rules
(ordering, single-call, timing bounds, redaction, every mandatory assertion). It never
fabricates a measurement: any step it cannot observe becomes INCONCLUSIVE, never PASS.

Determinism seam: ``now_ns`` and ``sleep`` are injectable, so the offline mock test drives
the whole matrix deterministically with no network, provider, or real clock.

Redaction: evidence carries only hashes and bounded reason codes — never SDP, a credential,
a raw call id, or provider payload.
"""
from __future__ import annotations

import asyncio
import hashlib
import time
from dataclasses import dataclass
from typing import Awaitable, Callable, List, Optional

from . import CHANGE_ID, FAIL, GROUP_PLANNED, INCONCLUSIVE, PASS, PROTOCOL_VERSION  # noqa: F401
from .assertions import aggregate_assertions
from .broker import BrokerHttpError, IdempotencyConflict
from .candidate import READINESS_CEILING_MS, READINESS_DEFAULT_MS, REVOCATION_BOUND_MS
from .classify import classify_overall
from .cleanup import CallRegistry
from .clock import TrialClock
from .control_stub import ControlError, ControlLeaseStub
from .media import MediaGateError
from .metrics import build_metrics
from .models import AssertionResult, GroupResult, TrialResult
from .run import (CROSS_CUTTING_ASSERTIONS, GROUP_ASSERTIONS, _candidate, _environment,
                  _serialize_assertions, _serialize_groups, _serialize_trials)

# The ordering invariant (baseline/delayed): each marker must be <= the next.
ORDER = (
    "t_sideband_verified",
    "t_answer_released",
    "t_lease_ack",
    "t_media_authorized",
    "t_answer_applied",
    "t_first_input_sent",
)


def build_session_config(candidate) -> dict:
    """The GA ``session`` object POSTed with the SDP offer (voice + server_vad turn detection)."""
    return {
        "type": "realtime",
        "model": candidate.requested_model,
        "audio": {
            "output": {"voice": candidate.voice},
            "input": {"turn_detection": dict(candidate.turn_detection)},
        },
    }


@dataclass
class LiveComponents:
    """Injected component factories (real by default, fakes in the offline mock test)."""

    make_broker: Callable[[], object]        # fresh broker per trial (owns idempotency cache)
    make_sideband: Callable[[str], object]   # (call_id) -> sideband
    make_media: Callable[[], object]         # -> media peer
    make_track: Callable[[], object]         # -> audio track


@dataclass
class LiveEnv:
    components: LiveComponents
    session_config: dict
    deadline_ms: int = READINESS_DEFAULT_MS
    ceiling_ms: int = READINESS_CEILING_MS
    delayed_extra_ms: int = 800              # F0-B injected delay (< deadline)
    revocation_bound_ms: int = REVOCATION_BOUND_MS
    first_output_timeout_ms: int = 4000
    now_ns: Callable[[], int] = time.monotonic_ns
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep


@dataclass
class _HS:
    """Per-handshake bookkeeping (never serialized verbatim)."""
    request_id_hash: Optional[str] = None
    call_id_hash: Optional[str] = None
    call_id: str = ""                        # raw id, in-memory only (for hangup); never serialized
    verified: bool = False
    authorized: bool = False
    answer_applied: bool = False
    first_output: bool = False
    timed_out: bool = False
    terminated: bool = False
    duplicate: bool = False
    conflict: bool = False
    provider_calls_created: int = 0
    error: Optional[str] = None              # "api_shape:<s>" ⇒ INCONCLUSIVE; "ordering" ⇒ FAIL
    media: object = None
    control: object = None
    sideband: object = None                  # kept open for F0-D's active terminal probe


def _offer_fp(offer_sdp: str) -> str:
    return hashlib.sha256(offer_sdp.encode()).hexdigest()[:16]


async def _hangup(broker, hs: _HS, registry: CallRegistry) -> None:
    """Best-effort provider hangup for this handshake's call; mark terminated on confirmation."""
    if not hs.call_id:
        return
    try:
        if await broker.hangup(hs.call_id):
            hs.terminated = True
            if hs.call_id_hash:
                registry.mark_terminated(hs.call_id_hash)
    except Exception:
        pass


async def _drive(env: LiveEnv, clock: TrialClock, registry: CallRegistry, broker,
                 request_id: str, *, variant: str, keep_sideband: bool = False) -> _HS:
    """Offer → create (held answer) → sideband verify + control authorize → apply → first media."""
    hs = _HS()
    media = env.components.make_media()
    hs.media = media
    sideband = None
    try:
        clock.mark("t_offer_ready", env.now_ns())
        track = env.components.make_track()
        offer_sdp = await media.create_offer(track)
        offer_fp = _offer_fp(offer_sdp)
        clock.mark("t_provider_create_sent", env.now_ns())

        origin = env.now_ns()
        result = await broker.create_call(request_id, offer_fp, offer_sdp, env.session_config)
        clock.mark("t_provider_create_accepted", origin)         # t=0 origin
        hs.request_id_hash = result.provider_request_id_hash
        hs.call_id_hash = result.call_id_hash
        hs.call_id = result.call_id
        hs.duplicate = result.duplicate
        hs.provider_calls_created = getattr(broker, "provider_calls_created", 1)
        registry.register(result.call_id_hash)

        sideband = env.components.make_sideband(result.call_id)
        hs.sideband = sideband        # exposed so F0-D can reuse it for the terminal probe
        await sideband.open()
        clock.mark("t_sideband_open", env.now_ns())

        if variant == "delayed":
            await env.sleep(env.delayed_extra_ms / 1000.0)
        if variant == "readiness_timeout":
            await env.sleep((env.deadline_ms + 200) / 1000.0)    # readiness never lands in time
            verified = False
        elif variant == "sideband_fail":
            verified = False                                     # harness withholds verification
        else:
            verified = await sideband.verify(env.deadline_ms / 1000.0)
        hs.verified = verified

        elapsed_ms = (env.now_ns() - origin) / 1_000_000.0
        over_deadline = elapsed_ms > env.deadline_ms

        if not verified or over_deadline:
            hs.timed_out = over_deadline
            clock.mark("t_hangup_sent", env.now_ns())
            await _hangup(broker, hs, registry)                  # terminate the held call
            return hs

        clock.mark("t_sideband_verified", env.now_ns())
        control = ControlLeaseStub()
        hs.control = control
        clock.mark("t_answer_released", env.now_ns())
        control.request_readiness()
        control.lease_ack()
        clock.mark("t_lease_ack", env.now_ns())
        control.grant_authorization(sideband_verified=hs.verified)
        clock.mark("t_media_authorized", env.now_ns())
        hs.authorized = control.is_authorized

        await media.apply_answer(result.held_answer_sdp, authorized=hs.authorized)
        clock.mark("t_answer_applied", env.now_ns())
        hs.answer_applied = media.answer_applied
        clock.mark("t_first_input_sent", env.now_ns())

        if await media.wait_first_output(env.first_output_timeout_ms / 1000.0):
            clock.mark("t_first_output_playable", env.now_ns())
            hs.first_output = True
        return hs
    except BrokerHttpError as exc:
        hs.error = f"api_shape:{getattr(exc, 'status', '?')}"    # → INCONCLUSIVE
        return hs
    except (MediaGateError, ControlError):
        hs.error = "ordering"                                    # → FAIL
        return hs
    except Exception:
        # Any provider / library / transport failure (httpx, websockets, aiortc, timeout)
        # degrades to INCONCLUSIVE — never a crash. NO exception text is copied anywhere:
        # it may carry SDP or provider payload (redaction / FR-017). Only a bounded code.
        hs.error = "api_shape:runtime"
        return hs
    finally:
        # F0-D keeps the sideband open for its post-hangup terminal probe and closes it in
        # _run_trial's finally; every other path closes it here.
        if sideband is not None and not keep_sideband:
            try:
                await sideband.close()
            except Exception:
                pass


def _ordering_ok(clock: TrialClock) -> bool:
    offs = clock.offsets_ms()
    seq = [offs[m] for m in ORDER if m in offs]
    return len(seq) == len(ORDER) and all(seq[i] <= seq[i + 1] + 1e-6 for i in range(len(seq) - 1))


async def _create_retry(env: LiveEnv, clock: TrialClock, registry: CallRegistry, broker,
                        request_id: str, *, changed: bool) -> _HS:
    """Create a call, then retry (exact or changed) — proving no second provider call."""
    hs = _HS()
    media = env.components.make_media()
    hs.media = media
    try:
        track = env.components.make_track()
        offer_sdp = await media.create_offer(track)
        fp1 = _offer_fp(offer_sdp)
        origin = env.now_ns()
        r1 = await broker.create_call(request_id, fp1, offer_sdp, env.session_config)
        clock.mark("t_provider_create_accepted", origin)
        hs.call_id_hash = r1.call_id_hash
        hs.request_id_hash = r1.provider_request_id_hash
        hs.call_id = r1.call_id
        registry.register(r1.call_id_hash)
        try:
            fp2 = fp1 if not changed else (fp1[:-1] + ("0" if fp1[-1] != "0" else "1"))
            r2 = await broker.create_call(request_id, fp2, offer_sdp, env.session_config)
            hs.duplicate = r2.duplicate
        except IdempotencyConflict:
            hs.conflict = True
        hs.provider_calls_created = getattr(broker, "provider_calls_created", 1)
    except BrokerHttpError as exc:
        hs.error = f"api_shape:{getattr(exc, 'status', '?')}"
    except Exception:
        hs.error = "api_shape:runtime"     # transport/library failure → INCONCLUSIVE (no text)
    return hs


async def _run_trial(env: LiveEnv, registry: CallRegistry, trial_id: str, group_id: str,
                     *, variant: str) -> TrialResult:
    clock = TrialClock(now_ns=env.now_ns)
    broker = env.components.make_broker()
    request_id = f"f0-live-{trial_id}"
    assertion_ids = list(GROUP_ASSERTIONS[group_id])
    status, note = INCONCLUSIVE, ""
    hs = _HS()

    try:
        if group_id in ("F0-A", "F0-B"):
            hs = await _drive(env, clock, registry, broker, request_id, variant=variant)
            if hs.error and hs.error.startswith("api_shape"):
                status, note = INCONCLUSIVE, "provider api shape prevented the trial"
            elif hs.error == "ordering":
                status, note = FAIL, "ordering violated"
            elif (hs.authorized and hs.answer_applied and hs.first_output
                  and _ordering_ok(clock) and hs.provider_calls_created == 1):
                status = PASS
            else:
                status, note = FAIL, "handshake incomplete"
            await _hangup(broker, hs, registry)

        elif group_id == "F0-C":
            hs = await _drive(env, clock, registry, broker, request_id, variant=variant)
            assertion_ids = (["F0-C-NO_MEDIA", "F0-C-READINESS_TIMEOUT"]
                             if variant == "readiness_timeout" else ["F0-C-NO_MEDIA"])
            if hs.error and hs.error.startswith("api_shape"):
                status, note = INCONCLUSIVE, "provider api shape prevented the trial"
            elif not hs.authorized and not hs.answer_applied and hs.terminated:
                status = PASS
            else:
                status, note = FAIL, "media authorized despite sideband failure/timeout"
            await _hangup(broker, hs, registry)  # idempotent; already terminated in _drive

        elif group_id == "F0-D":
            hs = await _drive(env, clock, registry, broker, request_id, variant="baseline",
                              keep_sideband=True)
            if hs.error and hs.error.startswith("api_shape"):
                status, note = INCONCLUSIVE, "provider api shape prevented the trial"
            elif not (hs.authorized and hs.first_output):
                status, note = FAIL, "revocation precondition (authorized active media) not met"
                await _hangup(broker, hs, registry)
            else:
                clock.mark("t_revocation_request", env.now_ns())
                hs.control.revoke()
                accepted = await broker.hangup(hs.call_id)
                clock.mark("t_hangup_sent", env.now_ns())
                # ACTIVE terminal probe on the control channel (passive media teardown is not
                # observable within the bound). Inverted polarity: "terminated" = revocation
                # observed; "alive" = call still live = revocation FAILED; "inconclusive" =
                # no attributable signal. Only a POSITIVE termination signal passes.
                verdict = "inconclusive"
                if hs.sideband is not None:
                    try:
                        verdict = await hs.sideband.probe_terminated(env.revocation_bound_ms / 1000.0)
                    except Exception:
                        verdict = "inconclusive"
                if verdict == "terminated":
                    clock.mark("t_peer_terminal", env.now_ns())
                    registry.mark_terminated(hs.call_id_hash)
                    hs.terminated = True
                offs = clock.offsets_ms()
                within = ("t_peer_terminal" in offs
                          and (offs["t_peer_terminal"] - offs["t_hangup_sent"]) <= env.revocation_bound_ms)
                if not accepted:
                    status, note = INCONCLUSIVE, "provider did not accept hangup"
                elif verdict == "alive":
                    status, note = FAIL, "revocation failed: call still live after hangup"
                elif verdict == "inconclusive":
                    status, note = INCONCLUSIVE, "no conclusive termination signal within bound"
                elif within:
                    status = PASS
                else:
                    status, note = FAIL, "termination confirmed but exceeded the 5s bound"

        elif group_id == "F0-E":
            hs = await _create_retry(env, clock, registry, broker, request_id, changed=False)
            if hs.error and hs.error.startswith("api_shape"):
                status, note = INCONCLUSIVE, "provider api shape prevented the trial"
            elif hs.provider_calls_created == 1 and hs.duplicate:
                status = PASS
            else:
                status, note = FAIL, "exact retry created a second provider call"
            await _hangup(broker, hs, registry)

        elif group_id == "F0-F":
            hs = await _create_retry(env, clock, registry, broker, request_id, changed=True)
            if hs.error and hs.error.startswith("api_shape"):
                status, note = INCONCLUSIVE, "provider api shape prevented the trial"
            elif hs.conflict and hs.provider_calls_created == 1:
                status = PASS
            else:
                status, note = FAIL, "changed retry did not conflict / created a second call"
            await _hangup(broker, hs, registry)
    finally:
        # Always release the peer connection and the (F0-D) kept-open sideband, on every
        # path (crash-safety / no leak).
        if hs.media is not None:
            try:
                await hs.media.close()
            except Exception:
                pass
        if hs.sideband is not None:
            try:
                await hs.sideband.close()
            except Exception:
                pass

    durations = clock.offsets_ms() if clock.has("t_provider_create_accepted") else {}
    return TrialResult(
        trial_id=trial_id, group_id=group_id, status=status,
        provider_request_id_hash=hs.request_id_hash, durations_ms=durations,
        assertion_ids=assertion_ids, note=note,
        provider_calls_created=hs.provider_calls_created,
        media_authorized=hs.authorized, answer_applied=hs.answer_applied,
    )


async def _interruption_drill(env: LiveEnv, registry: CallRegistry) -> tuple:
    """Cross-cutting drill (FR-005/FR-006). Create a call and LEAVE IT OPEN (simulated
    interruption — no in-line hangup), then run bounded cleanup and confirm every still-open
    call is reaped within the revocation bound. Fail-closed: if the drill cannot be exercised
    or any open call is not reaped in time, both assertions are INCONCLUSIVE (never PASS)."""
    broker = env.components.make_broker()
    media = env.components.make_media()
    call_map = {}          # call_id_hash -> raw call_id (in-memory; never serialized)
    created = False
    try:
        track = env.components.make_track()
        offer_sdp = await media.create_offer(track)
        r = await broker.create_call("f0-live-INTERRUPT", _offer_fp(offer_sdp), offer_sdp,
                                     env.session_config)
        registry.register(r.call_id_hash)
        call_map[r.call_id_hash] = r.call_id
        created = True
        # Interruption: control is lost here; the call is deliberately NOT hung up in-line.
    except Exception:
        created = False    # could not even create → cannot exercise the drill
    finally:
        try:
            await media.close()
        except Exception:
            pass
    if not created:
        return False, False

    # Bounded cleanup: reap every still-open call within the revocation bound.
    start = env.now_ns()
    all_reaped = True
    for cid_hash in list(registry.open_calls()):
        raw = call_map.get(cid_hash, "")
        ok = False
        if raw:
            try:
                ok = await broker.hangup(raw)
            except Exception:
                ok = False
        if ok:
            registry.mark_terminated(cid_hash)
        else:
            all_reaped = False          # an open call we could not confirm terminated
    within_bound = ((env.now_ns() - start) / 1_000_000.0) <= env.revocation_bound_ms
    ok = all_reaped and within_bound and len(registry.open_calls()) == 0
    return ok, ok


async def run_live_matrix(env: LiveEnv, candidate, *, groups: Optional[List[str]] = None,
                          lab_project_ref: str, dependency_versions: dict,
                          started_at: str, completed_at: str,
                          resolved_model: Optional[str] = None,
                          source_commit: Optional[str] = None) -> dict:
    """Run the registered matrix live and assemble the terminal evidence record."""
    wanted = set(groups) if groups else set(GROUP_PLANNED)
    trials: List[TrialResult] = []
    group_results: List[GroupResult] = []
    registry = CallRegistry()

    # Every registered group appears in the result. A group that is NOT selected stays at
    # completed=0 so a PARTIAL run (e.g. --groups F0-A) can never classify as a full PASS —
    # a PASS requires all six groups' planned trials (classify_overall enforces this).
    for gid in GROUP_PLANNED:
        planned = GROUP_PLANNED[gid]
        gr = GroupResult(id=gid, planned=planned)
        if gid in wanted:
            base_variant = {"F0-A": "baseline", "F0-B": "delayed", "F0-D": "baseline",
                            "F0-E": "baseline", "F0-F": "baseline"}.get(gid, "baseline")
            for i in range(1, planned + 1):
                trial_id = f"{gid}-{i:02d}"
                variant = ("readiness_timeout" if (gid == "F0-C" and i % 2 == 0)
                           else "sideband_fail" if gid == "F0-C" else base_variant)
                t = await _run_trial(env, registry, trial_id, gid, variant=variant)
                trials.append(t)
                gr.completed += 1
                if t.status == PASS:
                    gr.passed += 1
                elif t.status == FAIL:
                    gr.failed += 1
        else:
            # Un-selected group: emit INCONCLUSIVE placeholder rows so the evidence always
            # carries all 70 trials (schema minItems/maxItems=70) and the group stays
            # incomplete (→ overall INCONCLUSIVE for a partial run).
            for i in range(1, planned + 1):
                trials.append(TrialResult(
                    trial_id=f"{gid}-{i:02d}", group_id=gid, status=INCONCLUSIVE,
                    provider_request_id_hash=None, durations_ms={},
                    assertion_ids=list(GROUP_ASSERTIONS[gid]),
                    note="not executed (group not selected)"))
        group_results.append(gr)

    interrupted_ok, bounded_ok = await _interruption_drill(env, registry)

    assertions = aggregate_assertions(trials)
    for aid in CROSS_CUTTING_ASSERTIONS:
        ok = interrupted_ok if aid == "F0-D-INTERRUPTED" else bounded_ok
        assertions.append(AssertionResult(id=aid, status=(PASS if ok else INCONCLUSIVE),
                                          passed_trials=0, failed_trials=0))

    metrics = build_metrics(trials)
    overall = classify_overall(group_results, trials, assertions, metrics, "PASS",
                               environment_inconclusive=False)
    record = {
        "protocol_version": PROTOCOL_VERSION,
        "started_at": started_at,
        "completed_at": completed_at,
        "environment": _environment(lab_project_ref, dependency_versions, network_type="webrtc"),
        "candidate": _candidate(resolved_model=resolved_model or candidate.requested_model),
        "trial_groups": _serialize_groups(group_results),
        "trials": _serialize_trials(trials),
        "metrics": metrics,
        "assertions": _serialize_assertions(assertions),
        "overall": overall,
    }
    # Record the harness/F0 source commit so the kernel publication gate can match it against
    # its pinned f0_source_commit (validate-avatar-client.py commit_match). Live runs only —
    # the offline INCONCLUSIVE record stays commit-free and byte-stable.
    if source_commit:
        record["source_commit"] = source_commit
    return record


def real_live_components(api_key: str, pcm16: bytes) -> LiveComponents:
    """Factory bundle wiring the real aiortc / websockets / httpx components (lab run)."""
    from .broker import HttpBroker
    from .media import AiortcMediaPeer, fixture_audio_track
    from .sideband import WssSideband

    return LiveComponents(
        make_broker=lambda: HttpBroker(api_key),
        make_sideband=lambda cid: WssSideband(cid, api_key),
        make_media=lambda: AiortcMediaPeer(),
        make_track=lambda: fixture_audio_track(pcm16),
    )


def live_report_md(record: dict) -> str:
    """Redaction-safe human summary of a live run (counts / status only, never payloads)."""
    lines = [
        "# Avatar F0 Brokered-Call Feasibility — Results (live run)",
        "",
        f"Change: {CHANGE_ID}",
        "",
        f"## Overall: {record['overall']}",
        "",
        "| Group | planned | completed | passed | failed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for g in record["trial_groups"]:
        lines.append(f"| {g['id']} | {g['planned']} | {g['completed']} | {g['passed']} | {g['failed']} |")
    lines += [
        "",
        "## Assertions",
        "",
    ]
    for a in record["assertions"]:
        lines.append(f"- `{a['id']}`: {a['status']} (passed {a['passed_trials']}, failed {a['failed_trials']})")
    lines += [
        "",
        "## Redaction / threat-model disposition",
        "",
        "Evidence carries only hashes, bounded reason codes, and monotonic offsets — no SDP, "
        "credential, raw call id, transcript, media, or high-cardinality identifier. The record "
        "is re-scanned before writing and a finding fails the run closed.",
        "",
        "## Reviewer decision",
        "",
        f"Terminal `{record['overall']}` record from the supervised live lab run.",
        "",
    ]
    return "\n".join(lines)
