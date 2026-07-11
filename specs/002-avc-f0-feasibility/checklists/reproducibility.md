# Reproducibility & Determinism Requirements Checklist: 002-avc-f0-feasibility

**Purpose**: Release-gate validation of the *requirements quality* for pinned inputs,
immutable profile identity, deterministic fixture, and digest-verified external inputs.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Scope**: FR-002, FR-004, FR-018; Clarifications Q3/Q7; Assumptions; Dependencies; data-model

## Requirement Completeness

- [ ] CHK001 Are the components of the immutable candidate-profile digest enumerated (harness revision, dependency-lock digest, model, voice, turn settings, timeout settings, fixture digest)? [Completeness, Spec §FR-002]
- [ ] CHK002 Is the deterministic audio-fixture requirement fully specified (one fixture per harness revision; generator parameters + generated-byte digest pinned in run metadata)? [Completeness, Spec §FR-002/§Clarifications Q7]
- [ ] CHK003 Are deterministic trial identifiers required (fixed `F0-<A–F>-NN` pattern)? [Completeness, Spec §Key Entities/data-model]
- [ ] CHK004 Is the acceptance-map digest verification specified (record source commit + digest; mismatch ⇒ INCONCLUSIVE)? [Completeness, Spec §FR-018/§Clarifications Q3]
- [ ] CHK005 Is a pinned runtime + hash-locked dependency set required? [Completeness, Spec §Assumptions/Plan §Technical Context]
- [ ] CHK006 Is the "no committed binary audio and no real-user recording" constraint stated? [Completeness, Spec §Clarifications Q7/§Dependencies]

## Requirement Clarity

- [ ] CHK007 Is "enough detectable speech and trailing silence to trigger the pinned `server_vad` profile" expressed with criteria that make triggering objectively assessable? [Ambiguity, Spec §Clarifications Q7]
- [ ] CHK008 Is "immutable per-run candidate profile" clearly scoped to prohibit any mid-run mutation? [Clarity, Spec §FR-002]
- [ ] CHK009 Is the relationship between the pinned dependency lock and the profile digest clearly specified? [Clarity, Spec §FR-002]

## Requirement Consistency

- [ ] CHK010 Is the fixture policy consistent across FR-002, Dependencies, and Clarifications Q7 (deterministic, digest-pinned, no committed binary, no real recording)? [Consistency, Spec §FR-002/§Dependencies]
- [ ] CHK011 Is candidate pinning consistent between FR-002, Assumptions, and the registered protocol's fixed profile (model/voice/VAD params)? [Consistency, Spec §FR-002/§Assumptions]

## Acceptance Criteria Quality / Measurability

- [ ] CHK012 Is fixture determinism objectively verifiable (regeneration reproduces the pinned byte digest)? [Measurability, Spec §Clarifications Q7]
- [ ] CHK013 Is profile immutability verifiable via a single reproducible digest? [Measurability, Spec §FR-002]
- [ ] CHK014 Is acceptance-map integrity verifiable via digest comparison against a pinned expected value? [Measurability, Spec §FR-018]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK015 Primary — Are requirements defined for a fully pinned profile + valid digest-matched map allowing the run to proceed? [Coverage/Primary, Spec §US2-S1/§FR-018]
- [ ] CHK016 Exception — Are requirements defined for candidate unavailability / API-shape mismatch ⇒ INCONCLUSIVE with no inferred behavior? [Coverage/Exception, Spec §US2-S3/§FR-004]
- [ ] CHK017 Exception — Are requirements defined for acceptance-map absence / digest or baseline mismatch ⇒ INCONCLUSIVE with no placeholder IDs? [Coverage/Exception, Spec §Edge Cases/§FR-018]
- [ ] CHK018 Alternate — Is recording the resolved-model snapshot (when it differs from the requested model) required? [Coverage/Alternate, Spec §Assumptions/data-model]

## Edge Case Coverage

- [ ] CHK019 Is behavior specified when fixture regeneration yields a non-matching digest (nondeterminism detected)? [Edge Case/Gap, Spec §Clarifications Q7]
- [ ] CHK020 Is behavior specified when the dependency lock changes (profile digest necessarily changes for that revision)? [Edge Case, Spec §FR-002]

## Dependencies & Assumptions

- [ ] CHK021 Is the frozen `avatar-client-parallel-v1` baseline dependency documented and marked read-only? [Dependency, Spec §Dependencies]
- [ ] CHK022 Is the assumption "generated audio only; provider-create acceptance is t=0" stated where reproducibility depends on it? [Assumption, Spec §Assumptions]

## Ambiguities & Conflicts

- [ ] CHK023 Is there any residual ambiguity about whether the fixture is generated at build/run time vs pre-generated, given the "per harness revision" phrasing? [Ambiguity, Spec §Clarifications Q7]
