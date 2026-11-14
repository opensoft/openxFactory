# Supported private connectivity contract publication

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [publish-private-connectivity-production-contract](../../proposal.md).

## Purpose

Define independently consumable supported publication and verification of the neutral private connectivity binding while preserving compatibility and keeping deployment and product authority separate.

## ADDED Requirements

### Requirement: Neutral publication has accepted owner scope

Supported binding publication SHALL require current named neutral/release-owner acceptance of its exact schema, documentation, corpus, reader, test and release surfaces before implementation. Evidence-owner acceptance or production-policy ratification SHALL NOT grant that separate scope.

#### Scenario: Only the evidence scope is accepted
- **WHEN** T006 E acceptance exists but neutral publication scope at T016 is absent
- **THEN** binding publication and reader/release edits SHALL remain blocked

#### Scenario: The normal cut requires an additional protected edit
- **WHEN** publication needs a workflow, release-builder or other path outside its accepted file list
- **THEN** that edit SHALL wait for the owning decision and task refinement

### Requirement: The supported binding preserves neutral conformance

The published binding SHALL retain the ratified optional/unbound behavior, installation/customer/environment matching, HTTPS endpoint and endpoint-bound approval scopes, closed state vocabulary, current scoped approvals, enrollment/effective-policy checks and separately approved routes. Its reader SHALL remain offline, reject invalid/duplicate input and preserve safe ordinary-file handling with redacted results. Actual TLS/reachability observations and domain/provider/product authority SHALL remain outside the neutral conformance reader.

#### Scenario: An existing manifest has no private binding
- **WHEN** a compatible consumer validates an installation without the optional binding
- **THEN** the supported contract SHALL preserve its unbound behavior without requiring a hosted subscription

#### Scenario: A binding substitutes another boundary or endpoint
- **WHEN** a binding or approval mismatches installation, customer, environment, endpoint, network or required access/route scope
- **THEN** conformance SHALL fail without exposing credentials or granting actual readiness

### Requirement: Supported artifacts are independent of the lab

The supported schema, documentation, conformance corpus and reader SHALL be consumable from the released neutral artifact set without importing feature 040 or hosted-product implementation. Feature 040 schemas, evidence and lab approvals SHALL remain historical and unchanged; fixture conformance SHALL NOT qualify a provider or customer target.

#### Scenario: A candidate names only the feature-local schema
- **WHEN** customer qualification relies solely on the 040 draft path or a local helper artifact
- **THEN** supported release acceptance SHALL remain blocked until published neutral content is verified

#### Scenario: Neutral conformance passes
- **WHEN** a consumer validates deterministic cases against the exact supported schema and reader
- **THEN** that result SHALL establish conformance only and SHALL NOT establish target execution, staging or canary acceptance

### Requirement: The release follows atomic content-addressed publication

The neutral release SHALL follow the existing versioning process, with version allocation at the authorized cut and coordinated schema/bundle identity, contract files, manifest digests, changelog and generated release inventory in the realized commit. A matching annotated remote tag and verified promotion/readback SHALL establish publication. Proposals SHALL reserve no version or advance a pin.

#### Scenario: Publication metadata and content disagree
- **WHEN** a schema/member digest, manifest, changelog, generated inventory, realized commit or annotated tag differs from the required release identity
- **THEN** publication verification SHALL fail and dependent adoption SHALL remain blocked

#### Scenario: A draft proposes publication
- **WHEN** this proposal is drafted or reviewed before the actual authorized cut
- **THEN** no version, tag, release artifact or consumer-pin advancement SHALL be represented as completed

### Requirement: Conformance and compatibility changes are verified

The accepted source/required-CI checks SHALL collect existing and published-contract conformance regressions at the exact candidate, including positive and refused boundary/authority cases. Additive publication SHALL preserve accepted compatibility. A breaking change SHALL require explicit schema-major and migration decisions through the existing governance process.

#### Scenario: Tests are omitted or behavior breaks compatibility
- **WHEN** required conformance was not collected or an accepted prior binding no longer conforms without a declared migration
- **THEN** the candidate SHALL remain unaccepted

#### Scenario: Publication reveals a breaking change
- **WHEN** realization would alter the ratified binding behavior or supported schema compatibility
- **THEN** implementation SHALL stop for its owning breaking-change decision rather than hiding it in a publication cut

### Requirement: Consumer adoption uses verified exact content

Before separately authorized consumer pin changes, the neutral handoff SHALL independently verify the supported tag, exact commit, consumed digests, reader/corpus identity and compatibility. Mutable references alone SHALL NOT establish compatibility, and publication SHALL NOT grant another owner's runtime or target authority.

#### Scenario: A consumer proposes a branch or tag alone
- **WHEN** the adoption record lacks verified exact commit/content identity and supported compatibility
- **THEN** the consumer handoff SHALL remain blocked

#### Scenario: The neutral release is verified
- **WHEN** independent readback establishes its exact supported artifact set
- **THEN** authorized owners SHALL still satisfy their own pin/release decisions, final candidate closure and applicable Q0–Q5 gates before effects or admission
