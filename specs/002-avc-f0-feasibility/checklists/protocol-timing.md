# Protocol & Timing Coverage Requirements Checklist: 002-avc-f0-feasibility

**Purpose**: Release-gate validation of the *requirements quality* for the trial matrix,
ordering guarantees, timing bounds, retry semantics, revocation, and instrumentation.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Scope**: FR-006–FR-014; SC-001–SC-006; US1/US4; Clarifications Q4; Edge Cases; Assumptions

## Requirement Completeness

- [ ] CHK001 Are all six trial groups enumerated with exact counts (F0-A=20; F0-B…F0-F=10 each; 70 total)? [Completeness, Spec §FR-006]
- [ ] CHK002 Are the separate observation points enumerated (provider call creation, sideband readiness, media authorization, answer application, first media)? [Completeness, Spec §FR-007]
- [ ] CHK003 Are the required monotonic markers enumerated (offsets from provider-create acceptance)? [Completeness, Spec §FR-011]
- [ ] CHK004 Is the readiness default (3,000 ms) and hard ceiling (5,000 ms) specified? [Completeness, Spec §FR-012]
- [ ] CHK005 Is the revocation bound (5 s) with separate request/observed offsets specified? [Completeness, Spec §FR-013]
- [ ] CHK006 Are the retry behaviors specified for both exact retry (at-most-one call, equivalent unconsumed result) and changed retry (no disclosure, no second call)? [Completeness, Spec §FR-010]
- [ ] CHK007 Is the mapping of readiness-timeout to the F0-C path and interrupted-run/cleanup as cross-cutting assertions (not extra groups) specified? [Completeness, Spec §FR-006/§Clarifications Q4]

## Requirement Clarity

- [ ] CHK008 Is the ordering invariant stated as a precise partial order (`sideband_verified ≤ answer_released ≤ lease_ack ≤ media_authorized ≤ answer_applied ≤ first_input_sent`)? [Clarity, Spec §FR-008/§US1-S1]
- [ ] CHK009 Is the per-group readiness deadline (the "selected 1,000–5,000 ms value") resolved so each trial's deadline is unambiguous? [Ambiguity, Spec §US4-S1]
- [ ] CHK010 Are "exact offer identity" and "changed offer fingerprint or non-volatile field" defined precisely enough to classify a retry? [Clarity, Spec §FR-010]
- [ ] CHK011 Is "observable terminal signal" defined for the revocation assertion (what counts as confirmed termination)? [Clarity, Spec §FR-013/§FR-014]

## Requirement Consistency

- [ ] CHK012 Are the timing bounds consistent across FR-012, FR-013, SC-002, SC-003, SC-005, and Assumptions? [Consistency, Spec §FR-012/§SC-002]
- [ ] CHK013 Is the trial matrix consistent between FR-006, US1/US4, and the result-schema group/count constraints? [Consistency, Spec §FR-006]
- [ ] CHK014 Is the "a p95/hard-ceiling miss cannot be hidden by averages" rule consistent between the Edge Cases and SC-002/SC-003? [Consistency, Spec §Edge Cases/§SC-002]

## Acceptance Criteria Quality / Measurability

- [ ] CHK015 Are the timing success criteria expressed with specific percentile/max thresholds rather than vague adjectives? [Measurability, Spec §SC-002/§SC-003/§SC-005]
- [ ] CHK016 Is "exactly one provider call per request" objectively countable (via hashed request IDs)? [Measurability, Spec §SC-001/§SC-006]
- [ ] CHK017 Is the first-playable p95 (2,000 ms) explicitly labeled an architecture threshold, not a production SLA, to prevent misinterpretation? [Clarity, Spec §SC-003/§Assumptions]
- [ ] CHK018 Is the ordering assertion expressed as a 100%-of-trials measurable criterion? [Measurability, Spec §SC-001]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK019 Primary — Are requirements defined for the baseline handshake (ordered authorization + single provider call)? [Coverage/Primary, Spec §US1-S1]
- [ ] CHK020 Alternate — Are requirements defined for delayed-sideband within the deadline (answer held; pass only after ordered authorization)? [Coverage/Alternate, Spec §US1-S2]
- [ ] CHK021 Exception — Are requirements defined for sideband failure (no media, no answer, call terminated)? [Coverage/Exception, Spec §US1-S3]
- [ ] CHK022 Exception — Are requirements defined for readiness exceeding the deadline (withhold authorization, terminate, fail if media/answer occurred)? [Coverage/Exception, Spec §US4-S2]
- [ ] CHK023 Exception — Are requirements defined for exact-retry and changed-retry outcomes? [Coverage/Exception, Spec §US1-S4/§US1-S5]
- [ ] CHK024 Exception — Are requirements defined for revocation where termination cannot be confirmed (FAIL or INCONCLUSIVE, never success)? [Coverage/Exception, Spec §US4-S4/§FR-014]
- [ ] CHK025 Recovery — Are requirements defined for interrupted-run bounded cleanup of every known call ID? [Coverage/Recovery, Spec §US1-S6/§FR-005]

## Edge Case Coverage

- [ ] CHK026 Are requirements defined for network jitter obscuring thresholds (multiple trials + raw monotonic durations recorded)? [Edge Case, Spec §Edge Cases]
- [ ] CHK027 Are requirements defined for weak/absent termination confirmation (request-accepted vs termination-observed kept distinct)? [Edge Case, Spec §Edge Cases/§FR-013]
- [ ] CHK028 Are requirements defined for a latency miss requiring an explicit design disposition? [Edge Case, Spec §Edge Cases]

## Dependencies & Assumptions

- [ ] CHK029 Is the timing origin (t=0 = provider-create acceptance) stated as an assumption? [Assumption, Spec §Assumptions/§FR-011]
- [ ] CHK030 Is "wall-clock timestamps are coarse metadata only; monotonic clock authoritative" stated? [Assumption, Spec §Assumptions/§FR-011]
