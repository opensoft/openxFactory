# Safe Rendering & Security Checklist: Avatar-First UI Standard Alignment

**Purpose**: Release-gate validation of requirement quality for untrusted-content
rendering, external-action safety, and provider-text authority. "Unit tests for
the requirements" — checking whether the safe-rendering requirements are
complete, clear, consistent, and measurable, NOT whether code sanitizes.
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / security

## Requirement Completeness

- [ ] CHK001 Is the full set of untrusted inputs enumerated (transcript text, model output, tool summaries, attachment names, URLs, visual result data, provider error text)? [Completeness, Spec §FR-012]
- [ ] CHK002 Is the full set of forbidden render forms enumerated (arbitrary HTML, executable content, provider-supplied widgets, unsafe URI schemes)? [Completeness, Spec §FR-012]
- [ ] CHK003 Are the prohibited uses of provider text enumerated (authority, confirmation, hidden command, widget identifier, analytics key, localization resource key)? [Completeness, Spec §FR-012]
- [ ] CHK004 Are the external-navigation/download safety requirements (destination allowlist, origin labeling, policy-appropriate confirmation) all specified? [Completeness, Spec §FR-012]
- [ ] CHK005 Are the safe outcome-rendering requirements (message key, retry guidance, approved fallback only; provider errors excluded) specified for AVC-02 denial/terminal results? [Completeness, Spec §FR-009]
- [ ] CHK006 Is the held-answer safety requirement (no active capture/playback until matching `media_authorized`) present? [Completeness, Spec §FR-008, §FR-009]

## Requirement Clarity

- [ ] CHK007 Is "narrow sanitized format" defined precisely enough to distinguish allowed from disallowed markup? [Clarity, Spec §FR-012]
- [ ] CHK008 Is "safe URI scheme" / "allowlisted destination" defined by explicit criteria rather than example? [Clarity, Ambiguity, Spec §FR-012]
- [ ] CHK009 Is "localization-safe message key" distinguished clearly from provider-supplied text? [Clarity, Spec §FR-009]
- [ ] CHK010 Is "display-safe canonical field" defined so consequential cards/actions can be objectively sourced? [Clarity, Spec §FR-012]

## Requirement Consistency

- [ ] CHK011 Do the untrusted-content rules in FR-012 and the outcome-slot rules in FR-009 agree that provider error text never enters widget state? [Consistency, Spec §FR-009, §FR-012]
- [ ] CHK012 Is the safe-rendering vocabulary consistent between the standard requirement, the schema `outcome_slots`/`fallback_slots`, and the validator rule `AFUV-UNSAFE-RENDER`? [Consistency, contracts/validator-rules.md]
- [ ] CHK013 Are "non-authoritative provider text" requirements consistent with the authority-boundaries requirements (FR-003)? [Consistency, Spec §FR-003, §FR-012]

## Acceptance Criteria Quality

- [ ] CHK014 Is there a measurable criterion that a negative fixture exists for unsafe rendering/HTML or unsafe URI, failing with a stable error id? [Measurability, Spec §FR-019, contracts/validator-rules.md]
- [ ] CHK015 Can "renders inert or rejects" be objectively verified through the deterministic fixtures? [Measurability, Spec §FR-012, §SC-002]
- [ ] CHK016 Is the requirement that outcome slots reference only kernel outcome-registry IDs objectively checkable? [Measurability, Spec §FR-009, research §D2]

## Scenario Coverage (Primary / Alternate / Exception)

- [ ] CHK017 Primary: Are requirements defined for rendering model output containing markup or a dangerous link as inert/rejected? [Coverage, Spec §FR-012]
- [ ] CHK018 Exception: Are requirements defined for a provider summary that appears to approve/deny/complete an action (treat as non-authoritative)? [Coverage, Exception Flow, Spec §FR-012]
- [ ] CHK019 Exception: Are requirements defined for an AVC-02 denial/terminal outcome exposing only safe text + retry + approved fallback? [Coverage, Exception Flow, Spec §FR-009]
- [ ] CHK020 Alternate: Are requirements defined for external navigation to a non-allowlisted destination? [Coverage, Spec §FR-012]

## Edge Case Coverage

- [ ] CHK021 Is the boundary of provider text used as an analytics key or localization resource key explicitly forbidden? [Edge Case, Spec §FR-012]
- [ ] CHK022 Is the case of an attachment name containing markup/script covered as untrusted? [Edge Case, Spec §FR-012]
- [ ] CHK023 Is a hidden-command-in-transcript case addressed (must not execute/navigate/load remote active content)? [Edge Case, Spec §FR-012]

## Non-Functional / Security posture

- [ ] CHK024 Does the spec require that no raw provider payloads/credentials/tenant data/high-cardinality identifiers appear in committed evidence/fixtures? [Coverage, Constitution §VII]
- [ ] CHK025 Is the fail-closed principle for deferred/unsafe features stated (degrade closed, not open)? [Coverage, Spec §FR-016, Constitution §VII]

## Dependencies & Assumptions

- [ ] CHK026 Is the assumption that canonical authoritative events (not provider text) drive consequential actions documented and validated? [Assumption, Spec §FR-012]

## Ambiguities & Conflicts

- [ ] CHK027 Is there any ambiguity about whether plain text vs sanitized format is the default rendering mode? [Ambiguity, Spec §FR-012]
- [ ] CHK028 Are there conflicting statements about which fields may drive consequential cards (canonical vs provider)? [Conflict, Spec §FR-012]
