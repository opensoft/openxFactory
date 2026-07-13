# doc-health Delta: Ideation Dashboard Snapshot Lane

Status: draft
Kind: architecture
Summary: Draft spec-delta slice (MODIFIED doc-health, nightly snapshot lane) for the add-ideation-dashboard re-proposal, iterating in staging.
Topics: ideation-dashboard, doc-health, doc-management, doc-workflow
Repository context: openxFactory
Draft slice of: [ideation-dashboard staged topic](../../../ideation-dashboard.md) — demoted from the ratified proposal 2026-07-13 (Brett).

## ADDED Requirements

### Requirement: Ideation dashboard snapshot lane
The nightly doc-health run SHALL include a deterministic ideation-dashboard
snapshot lane: after the deterministic pass, the generator defined by the
`ideation-dashboard` capability regenerates the snapshot and commits it
beside the dated reports. The lane is an output artifact of the run — like
the report itself — and adds no deterministic check family; strict snapshot
and workbench-manifest validation runs in the existing per-repo validator
preflight. A skipped or failed snapshot lane MUST be reported as skipped
and MUST NOT affect deterministic results.

#### Scenario: The nightly run completes
- **WHEN** the deterministic pass finishes
- **THEN** the snapshot lane regenerates and commits the snapshot beside the dated report
- **AND** the report links the committed snapshot

#### Scenario: The snapshot lane fails
- **WHEN** snapshot generation errors or is unavailable
- **THEN** the run records the lane as skipped and deterministic findings land unaffected

#### Scenario: A snapshot violates its schema
- **WHEN** a generated snapshot fails strict validation in the preflight
- **THEN** the run MUST report the validator failure rather than committing an invalid snapshot
