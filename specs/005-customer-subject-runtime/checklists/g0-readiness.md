# Gate G0 Requirements Readiness Checklist: Neutral Hermes Customer-Subject Runtime

Status: draft

**Purpose**: Formal reviewer gate for requirement completeness, clarity, consistency, measurability, and failure-path coverage before task generation
**Created**: 2026-07-12
**Feature**: [spec.md](../spec.md)
**Audience / timing**: Architecture, contract/data, security, operations, and release reviewers before implementation tasks

## Neutral Ownership And Scope

- [x] CHK001 Are the boundaries between openxFactory-neutral contracts, DomainxFactory aliases/policy, and the xFactory Hermes installer explicit and non-overlapping? [Completeness, Spec §FR-001–FR-003, §FR-038]
- [x] CHK002 Is the single static role-template versus repeatable runtime-instance distinction stated consistently in OpenSpec, the feature spec, and the data model? [Consistency, Spec §FR-001–FR-002, OpenSpec §HCS-001]
- [x] CHK003 Are project, patient, client-company, and future domain meanings treated only as mappings to one neutral Customer-subject shape? [Neutrality, Spec §FR-003–FR-004, OpenSpec §HCS-002]
- [x] CHK004 Is the one-installation/one-stack G0 boundary explicit without implying that general multi-stack support is delivered? [Scope, Spec §Assumptions, Data Model §Installation]
- [x] CHK005 Are excluded capabilities—runtime service implementation, domain policy, automatic downstream edits, and early dependent work—documented clearly enough to prevent scope expansion? [Completeness, Spec §Out of Scope, Plan §Summary]

## Topology, Identity, And Lifecycle

- [x] CHK006 Are all installation, stack, and layer state values and allowed transitions closed and unambiguous, including suspended recovery and terminal retirement? [Clarity, Spec §FR-005, OpenSpec §HCS-003]
- [x] CHK007 Are initial identity registrations, predecessor-linked lifecycle events, and non-authoritative projections distinguished as separate sources and views of state? [Consistency, Spec §FR-005, Data Model §Topology And Identity]
- [x] CHK008 Are direct mutation, event update/delete, predecessor forks, projection drift, and transition out of retired all specified as fail-closed cases? [Exception Coverage, Spec §FR-005, OpenSpec §HCS-003-S06]
- [x] CHK009 Are installing, configured, operational, suspended, and retired cardinality effects specified for Client, Domain, and Customer layers? [Completeness, Spec §FR-005–FR-006]
- [x] CHK010 Are layer ID, policy namespace, subject tuple, idempotency key, tombstone, and no-reuse requirements mutually consistent? [Consistency, Spec §FR-007, §FR-039]
- [x] CHK011 Is pseudonymous subject-reference construction constrained without claiming universal semantic PII detection? [Clarity, Spec §FR-003–FR-004, Research §Decision 1]
- [x] CHK012 Are exact file and recursive overlay pin requirements complete for missing, extra, traversing, symlinked, submodule, tag-only, and digest-drift cases? [Edge Cases, Spec §FR-008, OpenSpec §HCS-004]

## Isolation, Principals, And Authority

- [x] CHK013 Is the scope tuple defined consistently for layer-owned records, cross-layer records, and installation administration? [Consistency, Spec §FR-009, OpenSpec §HGR-001]
- [x] CHK014 Are default-deny outcomes specified for read, enumeration, write, delete, storage-probe, cross-installation, and pooled-connection leakage attempts? [Coverage, Spec §FR-010–FR-011, §FR-019]
- [x] CHK015 Is authenticated `session_user` binding explicit, with `current_user` prohibited as authority inside security-definer functions? [Clarity, Spec §FR-011, Research §Decision 6]
- [x] CHK016 Are principal lifecycle, database-login binding, grant expiry/revocation, and layer retirement effects defined for every new and already-pooled transaction? [Completeness, Spec §FR-011–FR-013]
- [x] CHK017 Are trust-anchor genesis, rotation, revocation, historical as-of validation, chain acyclicity, and scope narrowing specified together without mutable-root ambiguity? [Consistency, Spec §FR-012–FR-013, §FR-044]
- [x] CHK018 Are cross-layer bindings bounded by exact source/target scope, resource, digest, action, purpose, time, and required acceptance authority? [Completeness, Spec §FR-014–FR-017]
- [x] CHK019 Is serialization behavior measurable for operation-versus-revocation races, including the only two permitted outcomes? [Measurability, Spec §FR-016, User Story 2 Scenario 4]
- [x] CHK020 Are wildcard, inherited, transitive, reversed, self-bound, cyclic, expired, revoked, and wrong-scope authority cases explicitly rejected? [Exception Coverage, Spec §FR-017]

## Governed Evidence And Jobs

- [x] CHK021 Are artifact identity, immutable metadata, content digest/size, storage namespace, and reverification points all specified? [Completeness, Spec §FR-018]
- [x] CHK022 Is the anti-oracle requirement bounded to pre-blob-lookup response shape/status and absence of semantic cross-layer signals? [Clarity, Spec §FR-019, OpenSpec §HGR-005]
- [x] CHK023 Are approval request, policy, actual reviewer decision, supersession authority, conflict, and target-drift semantics complete and consistent? [Consistency, Spec §FR-020–FR-022, §FR-040]
- [x] CHK024 Are trace edges defined as immutable evidence that cites exact endpoints and authority without becoming authority themselves? [Clarity, Spec §FR-023]
- [x] CHK025 Are v2 envelope, run, and event scope/lifecycle requirements neutral while unchanged v1 consumers remain supported? [Compatibility, Spec §FR-024–FR-025, OpenSpec §NJE-004]

## PostgreSQL, Migration, And Recovery

- [x] CHK026 Are supported PostgreSQL 15/16 versions and the no-skip release expectation explicit? [Dependency, Spec §FR-041, Plan §Technical Context]
- [x] CHK027 Does security-drift scope include role attributes/memberships, ownership/ACLs, RLS flags, function security/search path, PUBLIC privileges, trusted schemas, and quarantine grants? [Completeness, Spec §FR-026]
- [x] CHK028 Are migration mapping authority, source snapshot, subject/admin/principal mappings, single-default proof, and dataset-digest framing fully defined? [Completeness, Spec §FR-027, Data Model §Migration]
- [x] CHK029 Are source-write freezing, atomic abort, row/ID preservation, reconciliation, and immutable ledger requirements mutually consistent? [Consistency, Spec §FR-028–FR-029]
- [x] CHK030 Are concurrent identical retry, crash recovery, changed-input replay, terminal success, and attempt-event outcomes specified deterministically? [Recovery Coverage, Spec §FR-029, Postgres Contract §Migration]
- [x] CHK031 Is quarantine unambiguously non-authoritative and inaccessible to runtime, authoritative references, views, foreign keys, and gates? [Security, Spec §FR-030]

## Validation, Publication, And Consumer Pin

- [x] CHK032 Is the fixture/evidence model required to cover positive, negative, two-Customer, and project/patient/client-company cases with stable IDs and findings? [Measurability, Spec §FR-031, Contracts §Acceptance Map]
- [x] CHK033 Are all supported DomainxFactory regression entries fixed to canonical repository, commit, `stack.yaml` path/digest, and expected pin/result? [Completeness, Spec §FR-037, Release Contract §Domain Regression Denominator]
- [x] CHK034 Is release membership closed over schemas, catalogs, fixtures, validators, requirements locks, PostgreSQL image locks, static compatibility surfaces, and normative docs? [Completeness, Spec §FR-032, Research §Decision 10]
- [x] CHK035 Are candidate, exact-commit, promotion, main-line, annotated-tag, and realization phases ordered without requiring evidence before it can exist? [Consistency, Spec §FR-033, Quickstart §§6–8]
- [x] CHK036 Are release version races, merge-generated commit changes, tag immutability, and superseding-release behavior specified? [Recovery Coverage, Spec §FR-033, §FR-042]
- [x] CHK037 Is online/offline verification defined over exact remote/tag/Git objects rather than mutable working-tree bytes? [Clarity, Spec §FR-034–FR-036]
- [x] CHK038 Is the Gate G0 consumer fixed to `opensoft/xFactory-Hermes-Install`, with the distinct `FarHeap/Hermes-Install` product explicitly rejected before object resolution? [Dependency, Spec §FR-043]
- [x] CHK039 Are downstream receipt path/schema, exact landed commit, exact `commit:path` reproduction, and missing-object exit behavior specified? [Completeness, Spec §FR-043, Release Contract §Hermes Install Closure Packet]
- [x] CHK040 Is Gate G0 closure prohibited until provider publication and downstream positive/negative pin evidence independently reproduce every required digest? [Acceptance Criteria, Spec §SC-012, OpenSpec §Tasks 5]

## Notes

- All items were assessed against the ratified OpenSpec change and the reviewed Speckit planning snapshot on 2026-07-12.
- Architecture/contract, PostgreSQL security, and release/downstream-pin expert reviews reported no remaining P1/P2 or constitution blockers.
- Implementation conformance remains to be proven by the generated task plan, test fixtures, release evidence, and downstream receipt; this checklist assesses requirement quality only.
