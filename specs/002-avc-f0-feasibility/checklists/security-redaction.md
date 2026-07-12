# Security & Credential / Redaction Requirements Checklist: 002-avc-f0-feasibility

**Purpose**: Release-gate validation of the *requirements quality* for credential handling and
evidence redaction — are these requirements complete, unambiguous, consistent, and measurable?
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)
**Scope**: FR-001, FR-003, FR-017; SC-007, SC-009; Clarifications Q2; Edge Cases; Key Entities

## Requirement Completeness

- [ ] CHK001 Are the acceptable credential sources exhaustively enumerated (process env var, gitignored `.env` as populate-only, CI/secret-store injection)? [Completeness, Spec §FR-001/§Clarifications Q2]
- [ ] CHK002 Is the exact credential environment variable name (`OPENAI_API_KEY`) specified as the contract? [Completeness, Spec §FR-001]
- [ ] CHK003 Are all prohibited credential sources named (CLI arguments, tracked `.env`/config/evidence files)? [Completeness, Spec §FR-001/§FR-003]
- [ ] CHK004 Are all prohibited-content classes for committed evidence enumerated (credentials, SDP, raw provider payloads, raw media/audio, transcripts, arbitrary/high-cardinality identifiers, unbounded strings)? [Completeness, Spec §FR-017]
- [ ] CHK005 Does the requirement state that redaction covers logs, traces, and crash output in addition to the evidence files? [Completeness, Spec §FR-017/§Edge Cases]
- [ ] CHK006 Are the preflight rejection triggers for unsafe credential/config handling enumerated? [Completeness, Spec §FR-003]
- [ ] CHK007 Is the treatment of a gitignored `.env` specified as populate-only (never read as a result artifact, copied, printed, or committed)? [Completeness, Spec §Clarifications Q2]

## Requirement Clarity

- [ ] CHK008 Is "unbounded strings" quantified (an explicit length cap) so the redaction rule is objectively enforceable? [Clarity, Spec §FR-017]
- [ ] CHK009 Is "high-cardinality subject identifiers" defined precisely enough to distinguish a permitted hash from a prohibited raw identifier? [Clarity, Spec §FR-017/§Key Entities]
- [ ] CHK010 Is the meaning of an "approved secret store" scoped/defined rather than left open? [Ambiguity, Spec §FR-001/§Clarifications Q2]
- [ ] CHK011 Is the SDP/ICE prohibition specified at a level (markers/patterns) that is unambiguous to implement? [Clarity, Spec §FR-017]

## Requirement Consistency

- [ ] CHK012 Are the prohibited-content classes stated consistently across FR-017, SC-007, and the Key Entities/Dependencies descriptions? [Consistency, Spec §FR-017/§SC-007]
- [ ] CHK013 Is the credential contract stated consistently across FR-001, FR-003, Assumptions, and Dependencies with no conflicting allowance? [Consistency, Spec §FR-001/§Dependencies]

## Acceptance Criteria Quality / Measurability

- [ ] CHK014 Is the redaction success criterion measurable as zero prohibited-content findings across evidence, logs, traces, and crash output? [Measurability, Spec §SC-007]
- [ ] CHK015 Is the redaction-failure consequence expressed as an observable outcome (run `FAIL` + commit prevented) rather than a vague guarantee? [Measurability, Spec §FR-017]
- [ ] CHK016 Is the preflight-rejection criterion measurable (100% of unsafe-config runs rejected before any provider call)? [Measurability, Spec §SC-009]

## Scenario Coverage (Primary / Alternate / Exception / Recovery)

- [ ] CHK017 Primary — Are requirements defined for a clean run producing zero redaction findings? [Coverage/Primary, Spec §SC-007]
- [ ] CHK018 Alternate — Are requirements defined for credential injection via CI/secret store vs local `.env` yielding identical behavior? [Coverage/Alternate, Spec §Clarifications Q2]
- [ ] CHK019 Exception — Are requirements defined for a redaction finding detected before write (fail-closed, no commit)? [Coverage/Exception, Spec §FR-017]
- [ ] CHK020 Exception — Are requirements defined for a credential supplied via a prohibited source (rejected at preflight)? [Coverage/Exception, Spec §FR-003]
- [ ] CHK021 Recovery — Is the interaction between atomic evidence writing and a redaction-failure abort specified (no partial/leaky evidence left behind)? [Coverage/Recovery, Spec §FR-015/§FR-017]

## Edge Case Coverage

- [ ] CHK022 Is behavior specified when the credential is absent (no provider call attempted, no fabricated artifact) as a security outcome? [Edge Case, Spec §SC-013/§Assumptions]
- [ ] CHK023 Is behavior specified when prohibited content appears only in crash output/stack traces rather than the evidence files? [Edge Case, Spec §FR-017]
- [ ] CHK024 Is the "publishable by construction" allowlist approach (allow-list out) specified rather than only a denylist scrub? [Coverage/Gap, Spec §FR-017]

## Dependencies & Assumptions

- [ ] CHK025 Is the assumption that env/secret-store injection is trusted stated and bounded? [Assumption, Spec §Assumptions]
- [ ] CHK026 Is the threat-model disposition requirement (recorded in the human-readable summary) referenced and traceable? [Traceability, Spec §Key Entities]

## Ambiguities & Conflicts

- [ ] CHK027 Is there any residual conflict about where a key may legitimately live (env vs `.env` vs args) that must be resolved? [Conflict, Spec §FR-001/§FR-003]
