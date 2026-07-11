# Fail-Closed Authority, Consent & Safety Requirements Checklist: AVC Reference Runtime

**Purpose**: Release-gate validation of the *requirements* governing fail-closed policy/consent/
operation authority, confirmation, kill switches, usage/quota, revocation, and redacted telemetry —
testing requirement quality, not runtime behavior.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Governance / security / consent reviewer

## Fail-Closed Authority

- [ ] CHK001 Is the fail-closed rule (policy/consent/operation authority unavailable or unknown → deny/reject via closed outcome) specified? [Completeness, Spec §FR-010, §ARR-003-S03]
- [ ] CHK002 Are policy/consent fixtures required to be immutable? [Clarity, Spec §Requirements, design D8]
- [ ] CHK003 Is the required-neutral-purpose mapping rule (missing mapping → deny media before provider creation) specified? [Completeness, Spec §FR-028, §ARR-007-S01]
- [ ] CHK004 Are the closed registries (reason/outcome/purpose/state) specified as rejecting unrecognized values? [Completeness, data-model.md, Spec §VII]
- [ ] CHK005 Is "deferred features fail closed rather than degrade open" reflected in the requirements? [Consistency, constitution §VII]
- [ ] CHK006 Is the non-authoritative nature of model/client/provider output specified (proposes, does not dispose)? [Completeness, Spec §FR-026, constitution §VII]

## Consent & Revocation

- [ ] CHK007 Is versioned consent binding (subject_ref, version, validity) specified? [Completeness, data-model.md §ConsentBinding]
- [ ] CHK008 Is the consent-invalidation → revocation flow (push revocation, revoke lease, terminate provider) specified? [Completeness, Spec §FR-023, §ARR-005-S05]
- [ ] CHK009 Is the revocation time bound (five seconds on the *injected* clock) specified unambiguously? [Ambiguity, Spec §FR-023, §Assumptions]
- [ ] CHK010 Is the rule that the memory-gateway consent schema is NEVER media authority specified? [Completeness, Spec §FR-030, design D8]
- [ ] CHK011 Is consent-version binding to the logical session specified (which version governs an active leg)? [Clarity, data-model.md, Gap]

## Confirmation & Operation Execution

- [ ] CHK012 Is the confirmation-supersession rule (expired/superseded confirmation → no operation, fresh confirmation required) specified? [Completeness, Spec §FR-029, §ARR-007-S02]
- [ ] CHK013 Is idempotent fixture operation execution under an external-operation key specified? [Completeness, Spec §FR-029, data-model.md]
- [ ] CHK014 Is "effects recorded only after a valid, unexpired confirmation decision" specified? [Clarity, Spec §FR-029, design D8]
- [ ] CHK015 Are the confirmation validity window semantics (valid_until, superseded) defined precisely? [Clarity, data-model.md, Gap]

## Kill Switches, Usage & Quota

- [ ] CHK016 Are all-session and per-profile kill-switch scopes both specified? [Completeness, Spec §FR-031, §ARR-007-S03]
- [ ] CHK017 Is the rule "deny new matching requests; revoke active leases only when switch policy requests it" specified? [Clarity, Spec §FR-031]
- [ ] CHK018 Are usage records specified as in-memory, append-only, attributed, and credential-free? [Completeness, Spec §FR-032, data-model.md §UsageRecord]
- [ ] CHK019 Is the quota/duration cap → canonical outcome + usage record rule specified? [Completeness, Spec §FR-032, §ARR-007-S05]
- [ ] CHK020 Are the fixture-configured cap values documented as deterministic test values? [Assumption, Spec §Assumptions]

## Redacted Telemetry

- [ ] CHK021 Is the structured, redacted telemetry requirement specified (bounded records with stable ids, hashed/fixture refs, transitions, injected-clock timings, usage outcome, reason codes)? [Completeness, Spec §FR-033, data-model.md]
- [ ] CHK022 Is the protected-content prohibition enumerated (SDP, credentials, provider payloads, raw transcript/media, arbitrary high-cardinality identifiers)? [Completeness, Spec §FR-033, §SC-007]
- [ ] CHK023 Is the rule "redaction validation fails → record not published" specified? [Clarity, Spec §FR-033, §ARR-007-S04]
- [ ] CHK024 Is "0 emitted telemetry records contain protected content" specified as a measurable criterion? [Measurability, Spec §SC-007]
- [ ] CHK025 Is "arbitrary high-cardinality identifier" defined precisely enough to be checkable? [Ambiguity, Spec §FR-033, Gap]

## Requirement Consistency

- [ ] CHK026 Are fail-closed outcomes consistent across policy, consent, and operation authority requirements? [Consistency, Spec §FR-010/028/029]
- [ ] CHK027 Is the revocation bound consistent between the consent requirement and the media-authorization/lease requirements? [Consistency, Spec §FR-023, §FR-021]
- [ ] CHK028 Are redaction requirements consistent with the constitution's committed-evidence redaction mandate? [Consistency, Spec §FR-033, constitution §VII]

## Scenario Coverage (Alternate / Exception / Recovery)

- [ ] CHK029 [Exception] Are requirements defined for authority returning "unknown" (distinct from "unavailable")? [Coverage, Spec §FR-010, Gap]
- [ ] CHK030 [Exception] Are requirements defined for a kill switch activating while a lease is active? [Coverage, Spec §FR-031, §ARR-007-S03]
- [ ] CHK031 [Recovery] Are requirements defined for requiring a fresh confirmation after supersession? [Recovery, Spec §FR-029, §ARR-007-S02]
- [ ] CHK032 [Edge] Is behavior specified when a usage cap is reached exactly at the boundary (=cap vs >cap)? [Edge Case, Gap]
- [ ] CHK033 [Edge] Is behavior specified when consent invalidates during provider termination already in progress? [Edge Case, Gap]

## Traceability & Assumptions

- [ ] CHK034 Do safety success criteria (SC-007) and authority requirements map to ARR-003/005/007 scenarios? [Traceability, acceptance map]
- [ ] CHK035 Is the assumption that policy/consent fixtures resolve identity refs, purposes, speech gates, retention, quotas, and confirmation rules documented? [Assumption, design D8, data-model.md]
- [ ] CHK036 Is the dependency that Hermes ports are out of scope (fixtures stand in) documented so fail-closed behavior is testable without Hermes? [Dependency, Spec §Out of Scope, §Assumptions]

## Notes

- Items test whether the authority/consent/safety *requirements* are complete/clear/consistent — not whether enforcement code works.
