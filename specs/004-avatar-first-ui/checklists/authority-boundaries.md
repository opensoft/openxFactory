# Authority Boundaries Checklist: Avatar-First UI Standard Alignment

**Purpose**: Release-gate validation of requirement quality for the authority,
state-ownership, and presentation-vs-authoritative boundaries this feature
defines. These are "unit tests for the requirements" — they check whether the
requirements are complete, clear, consistent, and measurable, NOT whether any
implementation behaves.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / governance

## Requirement Completeness

- [ ] CHK001 Are the four authoritative runtime axes (session lifecycle, control health, media state, workflow projection) each enumerated with a named owner? [Completeness, Spec §FR-001]
- [ ] CHK002 Are the three client-local presentation modes (conversation, work, review) each defined with a distinct purpose? [Completeness, Spec §FR-001]
- [ ] CHK003 Are the Hermes-layer surface defaults (Customer avatar-first, Client hybrid, Domain conventional-first) each specified together with the override attributes a DomainxFactory must record? [Completeness, Spec §FR-003]
- [ ] CHK004 Is the reusable-client vs conventional-web-console responsibility split enumerated on both sides (what each owns)? [Completeness, Spec §FR-005]
- [ ] CHK005 Are handoff-URL prohibitions (no bearer token, subject id, transcript, provider secret) fully listed? [Completeness, Spec §FR-006]
- [ ] CHK006 Are all media/authority states the surface must distinguish (permission, capture authorized/pending, active, listening, speaking, control degraded/lost, governed-action pending, retention active) enumerated? [Completeness, Spec §FR-008]
- [ ] CHK007 Is the persona-authority chain (catalog-owned identity, disclosure, fixed-for-session, impersonation-prohibited default) fully specified? [Completeness, Spec §FR-011]
- [ ] CHK008 Are the consent-purpose authority constraints (reference-only, no consent evidence, not authoritative over memory-gateway) documented? [Completeness, Spec §FR-014]

## Requirement Clarity

- [ ] CHK009 Is "presentation may not author an authoritative transition" stated unambiguously enough to be machine-checkable? [Clarity, Spec §FR-016]
- [ ] CHK010 Is the held-answer boundary ("verified but unapplied provider answer shows as connecting/pending, never active") stated with a precise trigger condition (matching `media_authorized`)? [Clarity, Spec §FR-009]
- [ ] CHK011 Is the distinction between control loss and media loss defined with the exact options offered for each (stop/reconnect/handoff)? [Clarity, Spec §FR-009]
- [ ] CHK012 Is "avatar text is not authoritative" defined precisely enough to distinguish it from canonical authoritative events? [Clarity, Spec §FR-003, §FR-012]
- [ ] CHK013 Is the meaning of "read-only" consumption of kernel registries unambiguous (no edits vs no reads)? [Clarity, Spec §FR-017]
- [ ] CHK014 Is "consequential value" defined by an explicit enumerated class (names, ids, dates, money, addresses, consent, proposed effects)? [Clarity, Spec §FR-004]

## Requirement Consistency

- [ ] CHK015 Are the authoritative axes described identically across the standard requirement, the key entities, and the data model? [Consistency, Spec §FR-001, Key Entities]
- [ ] CHK016 Do the persona-reference authority rules in FR-011 and FR-013 agree (reference-only, fail-closed, catalog out of scope)? [Consistency, Spec §FR-011, §FR-013]
- [ ] CHK017 Are the Hermes-layer defaults in the spec consistent with the existing standard §11 and template `hermes_layer_ui_guidance` they update? [Consistency, Spec §FR-003]
- [ ] CHK018 Do the workflow-boundary requirements avoid conflict with the workflow-visualization standard's ownership? [Consistency, Spec §FR-005]

## Acceptance Criteria Quality

- [ ] CHK019 Is there a measurable criterion that every one of the eight requirements has exactly one owner (Hermes layer / runtime axis / kernel registry / named successor)? [Measurability, Spec §SC-005]
- [ ] CHK020 Can "no authoritative axis is authored by presentation" be objectively verified by the validator? [Measurability, Spec §FR-016, §SC-004]
- [ ] CHK021 Are the authority-boundary acceptance scenarios expressed as observable WHEN/THEN conditions rather than narrative? [Acceptance Criteria, Spec §US2]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK022 Primary: Are requirements defined for guided intake exposing avatar + required controls + workflow context? [Coverage, Spec §US1]
- [ ] CHK023 Alternate: Are requirements defined for mode switching preserving session/workflow/persona/focus/pending-decision/state-revision/trace context? [Coverage, Spec §FR-002]
- [ ] CHK024 Exception: Are requirements defined for control lost while media remains connected? [Coverage, Exception Flow, Spec §FR-009]
- [ ] CHK025 Recovery: Are requirements defined for an AVC-12 authoritative snapshot reconciling stale projection and surfacing discarded local intent? [Coverage, Recovery, Spec §FR-002]
- [ ] CHK026 Are requirements defined for edit/policy actions handing off to the web console rather than embedding an editor? [Coverage, Spec §FR-005]

## Edge Case Coverage

- [ ] CHK027 Is the boundary case of a provider/tool summary that looks like an approval/denial addressed (treat as non-authoritative until a canonical event)? [Edge Case, Spec §FR-012]
- [ ] CHK028 Is the case of persona change mid-session addressed (ends session, not in-place substitution)? [Edge Case, Spec §FR-011]
- [ ] CHK029 Is the case of a future handoff exchange addressed (server-issued, one-time, purpose-bound, reauthorized) even though deferred? [Edge Case, Spec §FR-006]

## Dependencies & Assumptions

- [ ] CHK030 Is the dependency on `avatar-client-runtime` owning the axes and control-loss options explicitly stated and validated? [Assumption, Spec §Assumptions]
- [ ] CHK031 Is the assumption that authoritative state is runtime-owned (not carried in the profile) documented? [Assumption, research §D1]

## Ambiguities & Conflicts

- [ ] CHK032 Is there any residual ambiguity between "surface default" (schema) and "Hermes-layer default" (standard) that needs reconciling? [Ambiguity, Spec §FR-003, §FR-013]
- [ ] CHK033 Is the authority owner named for every fail-closed path (persona, consent, retention, timing) without conflict? [Conflict, Spec §FR-011, §FR-014, §FR-026, §FR-027]
