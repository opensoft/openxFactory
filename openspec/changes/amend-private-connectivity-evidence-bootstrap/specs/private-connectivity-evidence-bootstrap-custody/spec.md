# Private connectivity evidence bootstrap custody

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [amend-private-connectivity-evidence-bootstrap](../../proposal.md).

## Purpose

Bind feature 043's original source-only bootstrap and CI evidence to a reviewed immutable commissioning input without inventing historical receipts or weakening rollout authority and pin verification.

## ADDED Requirements

### Requirement: Exact source-only custody scope precedes import

The coordinator SHALL admit the additional commissioning JSON and authentication review record only after actual owner ratification of their exact paths and the corresponding T010 scope refinement. Existing source-only storage, retention, access and custodian responsibilities MUST remain explicit. Scope approval SHALL NOT authenticate unseen outputs or grant provider/customer/live authority.

#### Scenario: The original T010 file list omits the first-record transition
- **WHEN** implementation needs the commissioning records and pin declaration/census promotion outside the frozen T010 list
- **THEN** it SHALL stop that consumer, obtain owner acceptance of the concrete refinement and refresh the review freeze before those writes

#### Scenario: Source refinement is ratified
- **WHEN** the owner approves the exact additional records and T010 file assignment
- **THEN** source implementation and export preparation SHALL be bounded to that scope while full Q0 and Q1–Q5 retain their existing prerequisites

### Requirement: Contained references inherit an independent immutable anchor

Each contained evidence reference SHALL resolve only within the closed object table of the independently reviewed commissioning commit/path/content identity. Unknown, duplicate, substituted, unresolved or cyclic references MUST fail. Original source/governance artifact references MUST retain exact immutable Git identities. The format SHALL NOT require a receipt to contain its own commit or hash.

#### Scenario: An original bootstrap command is imported
- **WHEN** a T001–T009 import identifies its original source, command, actual output and human-decision provenance
- **THEN** the verifier SHALL check those immutable identities and frozen outcomes without requiring a newly fabricated T001.json–T009.json receipt

#### Scenario: A caller supplies an unanchored object or cycle
- **WHEN** a reference lacks the accepted containing anchor, does not exist, or cycles through objects
- **THEN** verification SHALL fail without executing a command or collecting live state

#### Scenario: A receipt and its containing Git commit differ
- **WHEN** the tested source, output export, receipt and reviewed manifest occupy distinct immutable revisions
- **THEN** verification SHALL preserve each identity and accept only the actual reviewed relationships without a self-referential commit proof

### Requirement: Authentication reviews actual original evidence

T010 acceptance SHALL require the custodian's recorded review of actual original command/output/source identities, required CI collection and genuine human decisions. A generated pass, selected manifest, later custody choice or structural verifier result MUST NOT substitute for that review. Failed/blocked history and redaction provenance MUST remain available.

#### Scenario: Only a generated manifest exists
- **WHEN** the export is structurally valid but actual custodian authentication or original output is missing
- **THEN** T010 SHALL remain incomplete and no owner or rollout acceptance SHALL be inferred

#### Scenario: A live observation is placed in a source container
- **WHEN** contained evidence attempts to satisfy a provider/customer/staging/production proof under source-only custody
- **THEN** it SHALL be rejected pending its separately accepted protected custody and target/gate authority

### Requirement: First-record promotion uses the measured population

The initial empty production members SHALL remain FUTURE. First-record realization SHALL promote only members with actual committed sites and measure the exact standing site/member delta. Local reachability, explicit foreign-owner proof, unknown-path refusal, existing floors/skips and feature 040 declarations MUST remain intact.

#### Scenario: The first source-only commissioning record arrives
- **WHEN** committed evidence creates the first local or foreign production inventory sites
- **THEN** the relevant member and census SHALL be deliberately updated from the actual tree, with no fabricated witness, rolling exception or widened directory grant

#### Scenario: A foreign checkout or unlisted evidence path is unavailable
- **WHEN** ownership proof cannot be established or a new path lies outside the accepted inventory
- **THEN** source readiness SHALL fail rather than classify it as verified or exclude it from the sweep
