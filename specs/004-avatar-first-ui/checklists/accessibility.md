# Accessibility & Localization Checklist: Avatar-First UI Standard Alignment

**Purpose**: Release-gate validation of requirement quality for the accessibility
and localization baseline. "Unit tests for the requirements" — checking whether
the accessibility requirements are complete, clear, consistent, and measurable,
NOT whether a client is accessible.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / accessibility

## Requirement Completeness

- [ ] CHK001 Is the full per-capability accessibility set enumerated (keyboard operation, stable focus, visible focus, screen-reader announcements, captions, text-only mode, reduced motion, high contrast, non-color cues, zoom/reflow, pseudo-locale coverage)? [Completeness, Spec §FR-028]
- [ ] CHK002 Does each accessibility capability have a defined closed default? [Completeness, Spec §FR-028, §SC-004]
- [ ] CHK003 Is the localization baseline defined (English plus a long-string/bidirectional pseudo-locale)? [Completeness, Spec §FR-010]
- [ ] CHK004 Is the boundary between declarable standard requirements and later platform qualification evidence (Windows qualification, web WCAG 2.2 AA audit + exception register, extra locales) explicitly drawn? [Completeness, Spec §FR-010]
- [ ] CHK005 Is the "animation is never the sole state carrier" requirement present for all state classes (listening, thinking, speaking, interruption, control health, authority, errors, confirmations, outcomes)? [Completeness, Spec §FR-008, §FR-010]

## Requirement Clarity

- [ ] CHK006 Is "individually validator-checkable" defined so each accessibility field is objectively testable? [Clarity, Spec §FR-028]
- [ ] CHK007 Is "screen reader announces the meaningful state once" precise enough to distinguish from repeated decorative announcements? [Clarity, Spec §FR-010]
- [ ] CHK008 Is "reflow without hiding, clipping, overlapping, or disabling required commands" stated with measurable conditions (max qualified zoom, qualified viewports)? [Clarity, Spec §US2, Edge Cases]
- [ ] CHK009 Is the pseudo-locale fixture's coverage (long-string + bidirectional) unambiguously scoped? [Clarity, Spec §FR-010]

## Requirement Consistency

- [ ] CHK010 Do FR-010 (standard baseline) and FR-028 (schema per-capability declarations) use the same capability names without divergence? [Consistency, Spec §FR-010, §FR-028]
- [ ] CHK011 Is the structured accessibility model consistent with the existing template `interaction_surface.accessibility` block it replaces/extends? [Consistency, research §D9]
- [ ] CHK012 Are the non-color/reduced-motion requirements consistent with the "no status by animation, audio, or color alone" rule? [Consistency, Spec §FR-008, §FR-010]

## Acceptance Criteria Quality

- [ ] CHK013 Can each accessibility capability be objectively verified by the validator (present/closed-default)? [Measurability, Spec §FR-028, §FR-020]
- [ ] CHK014 Is there a measurable criterion tying pseudo-locale/zoom coverage to a deterministic fixture? [Measurability, Spec §SC-006, contracts/fixture-shape.md]
- [ ] CHK015 Are the accessibility acceptance scenarios framed as observable WHEN/THEN (reduced motion / text-only, pseudo-locale + zoom, screen-reader transition)? [Acceptance Criteria, Spec §US2]

## Scenario Coverage (Primary / Alternate / Exception / Non-Functional)

- [ ] CHK016 Primary: Are requirements defined for reduced-motion / text-only operation keeping every state perceivable and operable? [Coverage, Spec §US2]
- [ ] CHK017 Alternate: Are requirements defined for pseudo-locale long-strings + bidirectional + maximum qualified zoom reflow? [Coverage, Spec §US2]
- [ ] CHK018 Exception: Are requirements defined for dynamic status text that must not resize fixed controls or cause clipping/unreachable commands/horizontal scroll? [Coverage, Exception Flow, Spec §FR-010]
- [ ] CHK019 Non-Functional: Is the qualified-viewport set (wide, narrow, zoomed) referenced for accessibility evidence without overclaiming platform qualification? [Coverage, Spec §FR-010, §US2]

## Edge Case Coverage

- [ ] CHK020 Is the case where audio is unavailable (permission denied / no device / policy off) covered with a text + structured-control fallback preserving authority and traceability? [Edge Case, Spec §FR-007, Edge Cases]
- [ ] CHK021 Is the missing-control accessibility fallback (documented policy or platform fallback) specified? [Edge Case, Spec §FR-007]

## Dependencies & Assumptions

- [ ] CHK022 Is the assumption explicit that formal accessibility qualification is a named successor's responsibility (`avatar-pilot-hardening`), not this feature? [Assumption, Spec §Assumptions]
- [ ] CHK023 Is the dependency on a pinned bundled font family (incl. an RTL-capable face) documented as a fixture input rather than a shipped asset here? [Assumption, contracts/fixture-shape.md]

## Ambiguities & Conflicts

- [ ] CHK024 Is there any ambiguity about which accessibility items are attestations vs machine-checkable declarations? [Ambiguity, Spec §FR-028]
- [ ] CHK025 Are there conflicting accessibility expectations between the Windows-qualified surface and the web surface exception register? [Conflict, Spec §FR-010]
