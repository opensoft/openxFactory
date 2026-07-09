# neutral-job-envelope Specification

## Purpose

Define the neutral core of the hermes job envelope, run, and event
schemas, the domain overlay pattern for stricter domain rules, and the
loosening-only compatibility guarantee for neutralization.

## Requirements

### Requirement: Neutral job envelope core
The canonical hermes job envelope, run, and event schemas SHALL be
domain-neutral: no required field and no enumerated vocabulary may encode a
single domain's nouns. The envelope SHALL offer optional neutral references
— `domain`, `subject_ref`, `client_ref`, `workflow_ref`, `focal_item_ref`,
`gate_ref`, and `artifact_refs` — and `job_type` SHALL be a string whose
values are owned by domain vocabularies.

#### Scenario: A non-engineering domain issues a job
- **WHEN** a domain expresses a governed job for a subject, workflow, or gate
- **THEN** the envelope MUST validate without repository or feature fields
- **AND** the neutral references express the job's scope

#### Scenario: A schema revision is proposed
- **WHEN** a change to the canonical job schemas is proposed
- **THEN** it MUST NOT add required fields or enum values that encode a single domain's vocabulary

### Requirement: Domain overlay pattern
A domain SHALL express its stricter job rules as an overlay schema in its
own repository that re-tightens the neutral core (required fields, type
vocabularies) for that domain's jobs, and SHALL declare the refinement via
`specializes` provenance in its `stack.yaml`.

#### Scenario: Engineering jobs stay strict
- **WHEN** codexFactory issues or validates an engineering job
- **THEN** the engineering overlay MUST enforce the engineering job_type vocabulary and required repository and feature references over the neutral core

#### Scenario: Overlay provenance is declared
- **WHEN** a domain maintains a job overlay schema
- **THEN** its stack.yaml MUST declare `specializes` naming the neutral artifact and the overlay

### Requirement: Compatibility on neutralization
Neutralizing a canonical schema SHALL be loosening-only: every document
valid against the prior canonical schema MUST remain valid against the
neutralized schema, and copy-consumers pinned to a prior ref remain
conformant until they deliberately re-pin.

#### Scenario: Existing envelopes revalidate
- **WHEN** the neutralized schemas land
- **THEN** every existing example envelope, run, and event document in openxFactory MUST validate unchanged

#### Scenario: A pinned copy-consumer lags
- **WHEN** an install repo's schema copies match its declared openxFactory ref but not current main
- **THEN** that is conformant pin lag, not contract-copy drift — drift is measured against the declared ref
