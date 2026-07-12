# Protocol-Semantics Requirements Checklist: AVC Reference Runtime

**Purpose**: Release-gate validation of the *requirements* governing broker preflight, session/
media-attempt lifecycle, AVC-02 outcomes, two-channel media authorization, leased control, the
single event log, commands, and snapshot recovery — testing requirement quality, not runtime behavior.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Protocol owner / reviewer

## Session & Media-Attempt Lifecycle

- [ ] CHK001 Is the separation of logical-session state from media-attempt state specified as a requirement? [Completeness, Spec §FR-011, data-model.md]
- [ ] CHK002 Are the invariants "≤1 active instance" and "≤1 pending/connected media leg per session" both stated? [Completeness, Spec §FR-011]
- [ ] CHK003 Are the media-attempt statuses and their allowed transitions specified (reject unknown predecessor / terminal mutation)? [Completeness, data-model.md, design D4]
- [ ] CHK004 Is the fresh-resume replacement rule (atomically terminate+abandon pending leg before ≤1 replacement) specified? [Completeness, Spec §FR-015, §ARR-004-S03]
- [ ] CHK005 Is the second-instance rule (`second_instance_denied`, active instance untouched) specified? [Completeness, Spec §FR-017, §ARR-004-S05]
- [ ] CHK006 Are epoch-fencing semantics (epoch bump on authorized resume; stale epoch rejected) specified? [Completeness, Spec §FR-022, data-model.md]
- [ ] CHK007 Is "terminal states are immutable" stated as a requirement? [Clarity, data-model.md, design D4]

## Broker Preflight & AVC-02 Outcomes

- [ ] CHK008 Is the total-function requirement (exactly one `grant | denial | terminal` per request) stated? [Completeness, Spec §FR-012, §ARR-004]
- [ ] CHK009 Is the rule that only a grant may carry an answer/control credential specified? [Completeness, Spec §FR-012, data-model.md]
- [ ] CHK010 Is exact-offer idempotency (same cached grant, ≤1 provider call) specified with the "before consumption or expiry" precondition? [Clarity, Spec §FR-013, §ARR-004-S01]
- [ ] CHK011 Is changed-offer conflict (`idempotency_conflict`, no prior answer disclosed, no 2nd call) specified? [Completeness, Spec §FR-014, §ARR-004-S02]
- [ ] CHK012 Are the terminal/denial outcome codes enumerated as a closed set (fail-closed on unknown)? [Completeness, data-model.md §OutcomeCode, Spec §VII]
- [ ] CHK013 Is "credential-free terminal replay" specified (terminal record replayable without secret material)? [Completeness, Spec §FR-016, §SC-009]
- [ ] CHK014 Is the grant retry cache specified as process-memory-only and TTL-bounded? [Clarity, Spec §Key Entities, design D5]
- [ ] CHK015 Is secret-cache destruction on connect/expiry/abandonment/revocation specified? [Completeness, Spec §FR-016, §ARR-004-S04]
- [ ] CHK016 Are tenant concurrency/duration caps specified as producing canonical quota/duration outcomes? [Completeness, Spec §FR-032, §ARR-007-S05]

## Two-Channel Media Authorization & Leased Control

- [ ] CHK017 Is the requirement that `media_authorized` is emitted *exactly once* and only on the conjunction of sideband verification + identity-matched lease_ack specified? [Completeness, Spec §FR-018, §ARR-005-S01]
- [ ] CHK018 Are the five identity dimensions that must match (session, epoch, instance, attempt, media leg) enumerated? [Completeness, Spec §FR-018, data-model.md]
- [ ] CHK019 Is the hostile/forged-identity rule (transport-derived identity mismatch → rejected, no contribution to authorization) specified? [Completeness, Spec §FR-019, §Edge Cases]
- [ ] CHK020 Is the sideband-readiness-timeout rule (withhold, terminate leg, closed timeout outcome) specified? [Completeness, Spec §FR-020, §ARR-005-S02]
- [ ] CHK021 Is the lease-expiry rule (stop governed commands + authorization, idempotent provider termination) specified? [Completeness, Spec §FR-021, §ARR-005-S03]
- [ ] CHK022 Is the stale-epoch/rotated-credential reconnect rule (rejected without state change) specified? [Completeness, Spec §FR-022, §ARR-005-S04]
- [ ] CHK023 Are heartbeat and lease-expiry deadlines specified as injected-clock bounds? [Clarity, data-model.md, Spec §FR-008]
- [ ] CHK024 Is idempotent provider termination specified as reachable from every terminating path (timeout, expiry, revoke, kill)? [Consistency, contracts/ports.md, Spec §FR-021]

## Single Event Log, Commands & Snapshot Recovery

- [ ] CHK025 Is the single-sequenced-event-log requirement (one ordered sequence) specified? [Completeness, Spec §FR-026, data-model.md]
- [ ] CHK026 Are producer-authority checks specified (only runtime authority may append authoritative results; client/provider observations claiming authority rejected)? [Completeness, Spec §FR-026, §ARR-006-S05]
- [ ] CHK027 Is command validation against lease/epoch/allowlist/expected-revision fully enumerated? [Completeness, Spec §FR-024]
- [ ] CHK028 Is command dedupe by command ID (return first recorded result, no repeated effect) specified? [Completeness, Spec §FR-025, §ARR-006-S01]
- [ ] CHK029 Is the stale-revision-guard rule (reject without appending transition) specified? [Completeness, Spec §FR-024, §ARR-006-S02]
- [ ] CHK030 Is the atomic snapshot barrier `B` specified (projection through B, `last_event_sequence = B`)? [Completeness, Spec §FR-027, §ARR-006-S03]
- [ ] CHK031 Is bounded post-barrier buffering with ordered exactly-once drain specified? [Completeness, Spec §FR-027, §ARR-006-S03]
- [ ] CHK032 Is the buffer-overflow rule (abort + restart from fresh snapshot, no partial/historical replay) specified? [Completeness, Spec §FR-027, §ARR-006-S04]
- [ ] CHK033 Is the absence of a historical-replay endpoint stated as a requirement? [Clarity, Spec §FR-027, design D7]

## Requirement Consistency

- [ ] CHK034 Are epoch semantics consistent across session, attempt, lease, and reconnect requirements? [Consistency, Spec §FR-011/018/021/022]
- [ ] CHK035 Is "at most one provider call per grant" consistent between the idempotency requirement and the media-authorization flow? [Consistency, Spec §FR-013, §FR-018]
- [ ] CHK036 Are the terminating outcomes consistent between the attempt lifecycle and the AVC-02 outcome set? [Consistency, data-model.md §AttemptStatus/§OutcomeCode]

## Scenario Coverage (Alternate / Exception / Recovery)

- [ ] CHK037 [Alternate] Are requirements defined for sideband and lease_ack arriving in either order before authorization? [Coverage, Spec §FR-009, §FR-018]
- [ ] CHK038 [Exception] Are requirements defined for lease_ack from a mismatched transport identity? [Coverage, Spec §FR-019]
- [ ] CHK039 [Exception] Are requirements defined for an event appended during snapshot projection (race)? [Coverage, Spec §ARR-006-S03]
- [ ] CHK040 [Recovery] Are requirements defined for recovery restart after buffer overflow? [Recovery, Spec §FR-027, §ARR-006-S04]
- [ ] CHK041 [Edge] Is behavior specified when a fresh resume arrives while the pending leg is mid-authorization? [Edge Case, Spec §FR-015, Gap]
- [ ] CHK042 [Edge] Is behavior specified when a duplicate command arrives after its recorded result was superseded by revision? [Edge Case, Gap]

## Traceability

- [ ] CHK043 Does each protocol requirement group map to its ARR scenarios (ARR-004/005/006)? [Traceability, acceptance map]
- [ ] CHK044 Are all `#### Scenario:` blocks from the OpenSpec spec delta reflected as spec requirements or edge cases? [Traceability, Spec §Requirements, openspec spec.md]

## Ambiguities & Conflicts

- [ ] CHK045 Is it unambiguous what "non-volatile field" means for changed-offer conflict detection? [Ambiguity, Spec §FR-014, Gap]
- [ ] CHK046 Is there any conflict between "≤1 pending/connected leg" and fresh-resume creating a replacement leg (ordering of terminate-then-create)? [Conflict, Spec §FR-011, §FR-015]

## Notes

- Items test whether protocol *requirements* are complete/clear/consistent, never whether the state machine executes correctly.
