# reference-proof-placement Specification

## Purpose
Decide and record the canonical home for reference examples and proof
harnesses before any are moved, so that runnable proofs stay next to the
runtime that executes them while openxFactory keeps only domain-neutral
reference material.
## Requirements
### Requirement: Reference proof placement decision
The system SHALL decide the canonical home for reference examples and proof
harnesses before moving them.

#### Scenario: Proof example is considered canonical
- **WHEN** an end-to-end example explains the factory workflow rather than only testing an install repo
- **THEN** Hermes MUST approve whether it belongs in `openxFactory/examples/`, a future `factory-lab` repo, or remains temporarily in the install repo

#### Scenario: Proof harness has runtime dependencies
- **WHEN** a proof harness depends on install repo scripts, generated workspaces, live credentials, or runtime state
- **THEN** it MUST NOT be moved until replacement validation exists

### Requirement: No generated state migration
Reference migrations SHALL exclude generated runtime state.

#### Scenario: Example files are copied
- **WHEN** reference examples are copied into `openxFactory`
- **THEN** `.local`, credentials, token files, databases, generated workspaces, and runtime logs MUST be excluded

### Requirement: Reference validation
Each reference migration feature SHALL prove that moved examples remain
understandable and safe.

#### Scenario: Reference feature is ready for PR
- **WHEN** a reference example is ready for PR
- **THEN** the PR MUST include source provenance, referenced file checks, and secret/runtime-state exclusion evidence

