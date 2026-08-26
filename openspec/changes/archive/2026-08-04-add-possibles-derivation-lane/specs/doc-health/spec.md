# doc-health Delta: Possibles Derivation Lane

## ADDED Requirements

### Requirement: Possibles derivation lane
The doc-health capability SHALL include a possibles-derivation lane: a bounded,
non-mutating worker pass — following the same execution split and bounded-worker
pattern as the agentic semantic sweep, the document-cataloger lane, and the
ideation-readiness lane — that derives candidate possibles from the promoted
`ideation-cross-reference` index and proposes `possibles_register` entries.

Lane output SHALL be recommendations with `pending_review` disposition,
resolution class `contested`, and severity at most `warning`; derived-but-
undisposed possibles SHALL appear in the report as their own section, excluded
from the Ranked Plan; the lane MUST NOT block merges, MUST NOT open regression
issues in v1, and SHALL add no deterministic check family — the strict register
validator that enforces derived-entry shape and one-way disposition runs in the
existing per-repo validator preflight (delegated to
`validate-ideation-dashboard-contracts.py`).

#### Scenario: The nightly lane executes
- **WHEN** the possibles-derivation lane runs in the nightly workflow
- **THEN** it runs after the deterministic pass against the same inventory/index snapshot
- **AND** the dated report links the updated index and its immutable derivation evidence

#### Scenario: Derived possibles are reported
- **WHEN** a run has undisposed derived possibles
- **THEN** the report MUST list them in their own section and MUST NOT rank them in the Ranked Plan

#### Scenario: The lane is skipped
- **WHEN** the derivation worker is unavailable or fails
- **THEN** the run MUST record the lane as skipped and the deterministic results MUST land unaffected
- **AND** prior derived possibles absent only because the lane did not run MUST NOT be treated as disposed

#### Scenario: Lane output fails its contract
- **WHEN** worker output does not satisfy the register evidence contract or the additive kernel shape
- **THEN** the output MUST be rejected before persistence and the rejection reported in the run
