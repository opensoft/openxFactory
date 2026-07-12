"""AVC-02 broker preflight — one total ``grant | denial | terminal`` result.

Takes the runtime facade (duck-typed) to avoid a circular import. Only a grant
carries an answer or control credential (FR-012). Exact retries coalesce to the
same cached grant with at most one provider call; a changed non-volatile field
conflicts; connected/expired/abandoned/revoked replay a credential-free
terminal.
"""

from __future__ import annotations

from .attempt import MediaAttempt
from .authority import PolicyResolver
from .killswitch import KillSwitchGate
from .values import (
    AttemptStatus,
    ControlDescriptor,
    Grant,
    OutcomeCode,
    PreflightResult,
    Request,
)


def preflight(rt, request: Request) -> PreflightResult:
    now = rt.clock.monotonic()
    session = rt.registry.get_or_create(request.session_id)
    profile = request.offer.model_profile
    fp = request.fingerprint()

    # 1. Kill switch (all-session / per-profile).
    if KillSwitchGate.blocks_new(rt.kill_switch, profile):
        return PreflightResult.of_terminal(request.request_id, OutcomeCode.KILLED)

    # 2. Idempotency (before any side effect): retry / conflict / terminal replay.
    seen_fp = rt.grants.seen_fingerprint(request.request_id)
    if seen_fp is not None:
        if seen_fp != fp:
            # Changed offer / non-volatile field: conflict, no answer, no 2nd call.
            return PreflightResult.of_denial(
                request.request_id, OutcomeCode.IDEMPOTENCY_CONFLICT
            )
        grant = rt.grants.active_grant(request.request_id, now)
        if grant is not None:
            return PreflightResult.of_grant(grant)  # same grant, no new call
        term = rt.grants.terminal(request.request_id)
        return PreflightResult.of_terminal(
            request.request_id, term or OutcomeCode.EXPIRED
        )

    # 3. Fail-closed policy resolution.
    bundle = rt.policy_resolver.resolve(request.subject_id)
    if bundle is None:
        rt.usage_meter.record(
            request.tenant_ref,
            request.request_id,
            OutcomeCode.AUTHORITY_UNAVAILABLE,
            rt.clock.wall(),
        )
        return PreflightResult.of_denial(
            request.request_id, OutcomeCode.AUTHORITY_UNAVAILABLE
        )

    # 4. Purpose mapping — deny BEFORE any provider creation.
    if not PolicyResolver.purposes_mapped(bundle, request.purposes):
        return PreflightResult.of_denial(request.request_id, OutcomeCode.PURPOSE_UNMAPPED)

    # 5. Consent (fail closed on unavailable/unknown/invalid).
    if not rt.consent_gate.is_valid_now(request.subject_id):
        return PreflightResult.of_denial(request.request_id, OutcomeCode.CONSENT_REVOKED)

    # 6. Usage caps (concurrency).
    cap = rt.usage_meter.cap_outcome(bundle, request.tenant_ref)
    if cap is not None:
        rt.usage_meter.record(
            request.tenant_ref, request.request_id, cap, rt.clock.wall()
        )
        return PreflightResult.of_terminal(request.request_id, cap)

    # 7. Second instance under an active lease -> deny, do not revoke the active one.
    pending = session.pending_attempt
    if (
        session.active_instance_id is not None
        and session.active_instance_id != request.instance_id
        and pending is not None
        and pending.lease is not None
        and getattr(pending.lease, "active", False)
    ):
        return PreflightResult.of_denial(
            request.request_id, OutcomeCode.SECOND_INSTANCE_DENIED
        )

    # 8. Fresh authorized resume atomically replaces a pending leg (≤1 leg).
    if pending is not None:
        if request.resume_ref is not None and request.epoch == session.epoch:
            if pending.provider_call_ref:
                rt.provider.hangup(pending.provider_call_ref)
            pending.terminate(AttemptStatus.ABANDONED, OutcomeCode.ABANDONED)
            rt.grants.invalidate(pending.request_id, OutcomeCode.ABANDONED)
            session.pending_attempt = None
        else:
            return PreflightResult.of_denial(
                request.request_id, OutcomeCode.SECOND_INSTANCE_DENIED
            )

    # 9. Fresh leg + grant (the only place a provider call is created).
    session.active_instance_id = request.instance_id
    call_ref = rt.provider.create(request.offer.sdp_media)
    transport_identity = f"transport-{request.instance_id}"
    lease = rt.lease_manager.create(
        rt.ids,
        session_id=session.session_id,
        epoch=session.epoch,
        instance_id=request.instance_id,
        attempt_id=request.request_id,
        transport_identity=transport_identity,
        now=now,
        heartbeat_ttl=rt.HEARTBEAT_TTL,
        expiry_ttl=rt.LEASE_EXPIRY_TTL,
    )
    control = ControlDescriptor(lease_id=lease.lease_id, scope_digest="sha256:scope")
    answer = f"answer-for-{call_ref}"
    grant = Grant(
        request_id=request.request_id,
        offer_fingerprint=fp,
        answer=answer,
        control=control,
        expires_at=now + rt.GRANT_TTL,
    )
    attempt = MediaAttempt(
        request_id=request.request_id,
        offer_fingerprint=fp,
        instance_id=request.instance_id,
        epoch=session.epoch,
        provider_call_ref=call_ref,
        held_answer=answer,
        control_descriptor=control,
        readiness_deadline=now + rt.READINESS_TTL,
        lease=lease,
    )
    attempt.to(AttemptStatus.PROVIDER_CALL_CREATED)
    attempt.to(AttemptStatus.ANSWER_HELD)
    session.pending_attempt = attempt
    rt.attempts_by_request[request.request_id] = attempt
    rt.grants.put(request.request_id, grant, fp)
    return PreflightResult.of_grant(grant)
