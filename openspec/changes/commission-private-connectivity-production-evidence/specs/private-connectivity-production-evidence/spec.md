# Production qualification evidence controls

Status: ratified
Ratified: 2026-11-13 by Brett Heap. [Ratification record](../../review/ratification.md)

## Purpose

Define authenticated, scoped and fail-closed evidence controls for the private connectivity production feature without creating deployment authority or replacing owner acceptance.

## ADDED Requirements

### Requirement: Evidence implementation requires accepted scope

The coordinator SHALL implement evidence controls only after the named owner accepts the exact source/test/CI surfaces, verification commands and consumed custody/authentication decisions. A draft, policy ratification or lab acceptance SHALL NOT supply that acceptance or target authority.

#### Scenario: The evidence owner has not accepted
- **WHEN** the successor proposal is draft or consumed evidence custody/authentication is missing
- **THEN** helper, shared-reader and required-CI implementation SHALL remain blocked at T006

#### Scenario: A proposed edit lies outside the accepted files
- **WHEN** evidence implementation requires an additional source, test, workflow or protected path
- **THEN** that edit SHALL wait for an updated owning decision rather than widening the accepted scope

### Requirement: Verification binds actual outputs to closed cases

The verifier SHALL require the reviewed task, owner, required-case, command, revision, evidence-class and scope identities with immutable actual output and current authority. It SHALL reject unknown, duplicate, missing, substituted or wrong-scope evidence and invalid or non-finite numeric measurements. A successful structural check SHALL NOT create an approval.

#### Scenario: A copied verdict substitutes for an observation
- **WHEN** a record claims pass without authenticated command/output/revision and expected-outcome evidence
- **THEN** verification SHALL fail without executing an owner command or collecting target state

#### Scenario: The measured result exceeds an approved limit
- **WHEN** a required numeric result is missing, invalid, non-finite, over its accepted bound or lacks required event/coverage anchors
- **THEN** the affected acceptance SHALL fail and absent monitoring time SHALL NOT count as healthy observation

### Requirement: Bootstrap evidence uses an authenticated closed bridge

Bootstrap dependencies T001–T009 SHALL be verified from their original governance/source artifacts, actual command outputs and source identities under accepted custody. Later tasks SHALL NOT require nonexistent new bootstrap receipts or accept fabricated replacements, and later custody SHALL NOT retroactively grant authority.

#### Scenario: Original bootstrap outputs are available
- **WHEN** the accepted bridge can authenticate all required original task artifacts, commands, outputs and current approving decisions
- **THEN** the dependent source-CI check SHALL use those immutable references without demanding new T001–T009 task receipts

#### Scenario: A bootstrap approval is self-reported
- **WHEN** a generated record or verifier result is offered as its own approving human decision
- **THEN** import SHALL fail until actual owner acceptance is independently established

### Requirement: Scoped child progress is distinct from aggregate completion

Canary, offer and wave evidence SHALL use frozen approved instance identities and same-scope child dependencies. Full program Q2 SHALL precede each canary, an admitted offer SHALL precede its wave, and each wave SHALL have its own current decision. Aggregate task completion SHALL require every commissioned child.

#### Scenario: One offering is ready while another canary is pending
- **WHEN** a child has its own genuine accepted predecessors and current authority while an unrelated aggregate is incomplete
- **THEN** only that approved child SHALL be eligible to advance and the incomplete aggregate checkbox SHALL remain open

#### Scenario: Another profile or wave supplies a pass
- **WHEN** a child attempts to reuse a foreign candidate/profile/customer/site decision or a previous wave's authority
- **THEN** that child SHALL remain ineligible until its exact required evidence and decisions are accepted

### Requirement: Feature pin registration preserves coverage boundaries

Feature 043 evidence references SHALL have exact declared local/foreign ownership and reachability treatment within their reviewed task/instance inventory. Existing 040 declarations, uncovered-site checks and existing pin floors SHALL remain effective; unknown references SHALL NOT pass through a prefix exception.

#### Scenario: An undeclared evidence reference appears
- **WHEN** a reference is outside the accepted 043 inventory or lacks the required local/foreign ownership proof
- **THEN** the coverage or reachability check SHALL fail rather than widening a declaration or accepting an unavailable tree

#### Scenario: Inventory check mode is selected
- **WHEN** the reference checker runs in read-only check mode
- **THEN** it SHALL report mismatches without rewriting receipts, inventories or historical observations

### Requirement: Required CI proves exact source collection

Required coordinator CI SHALL explicitly collect the accepted feature verifier and registration suites at the exact candidate head and retain their actual results. Existing required checks, validation floors and skip obligations SHALL remain intact. Source CI SHALL NOT substitute for intended-platform, production or human acceptance.

#### Scenario: A generic job passes without the feature tests
- **WHEN** CI is green but the required feature suites were omitted or their dependency/collection failed
- **THEN** source readiness SHALL remain failed

#### Scenario: Source evidence is submitted at a live gate
- **WHEN** a source/fixture or lab result is offered instead of required actual staging or canary observations
- **THEN** the live gate SHALL remain blocked
