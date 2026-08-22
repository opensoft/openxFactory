# Scope Containment Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements that keep the feature inside
its ratified boundary — no domain-repository edit, no client-tenant act, no credential
minting, no live provider call, no completeness enforcement, no surface outside the
first-release vocabulary, and no fifth modified capability.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## No domain-repository edit

- [x] CHK1001 Is the no-domain-edit boundary stated as a requirement, not only as an intention? [Scope, Spec §FR-030]
- [x] CHK1002 Is it given a measurement (clean porcelain under the domain tree of an aggregation checkout)? [Measurability, Spec §SC-012, tasks §10.6]
- [x] CHK1003 Are the domain follow-ups NAMED, so they are carried rather than lost? [Completeness, Spec §Assumptions, proposal §Impact]
- [x] CHK1004 Is the one task that READS a domain checkout constrained to a read (exit code plus no file modified)? [Scope, tasks §7.4]
- [x] CHK1005 Is the domain-gate wiring that would make pack blocking fire identified as a domain edit and therefore out of scope? [Scope, plan §Cluster F]
- [x] CHK1006 Is the domain-local `issuance_preconditions` instance explicitly protected from edit, with "regularizes rather than replaces in place" given an operative reading? [Scope, Spec §FR-028, research §Decision 3]
- [x] CHK1007 Is the LedgerxFactory residency conflict left unresolved by this feature, with the reason (it touches live client consent instruments)? [Scope, Spec §Assumptions]

## No live act

- [x] CHK1008 Is every class of live act forbidden by requirement (client-tenant act, credential minting, provider call, network access)? [Scope, Spec §FR-029]
- [x] CHK1009 Is the prohibition extended to the feature's TESTS and to anything the artifacts could ENABLE, not only to the tasks? [Scope, Spec §FR-029, §SC-012]
- [x] CHK1010 Is drift handling forbidden from creating, modifying, widening, narrowing or removing anything? [Scope, Spec §FR-027]
- [x] CHK1011 Is that no-mutation claim given a source-level measurement rather than a schema description? [Measurability, tasks §10.6]
- [x] CHK1012 Is automated remediation forbidden with its ratified reason (it would itself require a broadly privileged identity in the client tenant)? [Traceability, Spec §FR-027, proposal §item 12]
- [x] CHK1013 Is the one task that needs provider facts constrained to offline sources with an escalation branch? [Scope, tasks §0.1]

## No completeness enforcement

- [x] CHK1014 Is the absence of a completeness rule stated as a REQUIREMENT rather than as a silence? [Scope, Spec §FR-032]
- [x] CHK1015 Are both absences covered (no fragment, and no entry), so one cannot become a finding while the other stays exempt? [Completeness, Spec §FR-032, §SC-013]
- [x] CHK1016 Is the derivation of an expected entry set forbidden from ANY source, not only from the credential requirement classes? [Scope, Spec §FR-032]
- [x] CHK1017 Is that prohibition measured by a negative assertion over the source, rather than by behaviour alone? [Measurability, Spec §SC-013, tasks §4.7]
- [x] CHK1018 Is the evidence that made the invented predicate unacceptable recorded (it fired permanently on 14 of 16 requirement classes and re-admitted a killed flaw)? [Traceability, Spec §FR-032, rulings §R5]
- [x] CHK1019 Is scoped completeness recorded as a NAMED SUCCESSOR rather than deferred vaguely? [Scope, Spec §FR-032]
- [x] CHK1020 Are the guards that keep the permissive axis from silently acquiring a completeness rule identified and retained? [Coverage, Spec §FR-031, §Edge Cases]
- [x] CHK1021 Is the `planned` scenario's "not reported as missing" explicitly protected from being read as evidence that a missing-entry check exists? [Ambiguity, Spec §FR-032]

## Vocabulary and capability scope

- [x] CHK1022 Is adding a surface outside the first-release vocabulary forbidden by requirement? [Scope, Spec §FR-031]
- [x] CHK1023 Are identities on out-of-scope surfaces explicitly NOT treated as missing roster entries? [Coverage, Spec §FR-031, §Edge Cases]
- [x] CHK1024 Is the out-of-scope-surface edge case retained precisely because a completeness rule would have fired on it? [Traceability, Spec §Edge Cases]
- [x] CHK1025 Does the feature declare exactly the five capabilities the amended packet declares, with no sixth? [Scope, Spec §Capabilities realized, plan §Constitution II]
- [x] CHK1026 Are the requirements added by this pass all realizations of existing FRs rather than new capability surface? [Scope, plan §decisions 25-30] — Checked item by item: each of the six is a firing predicate, a scope clarification, or a probe for a rule already stated in FR-002, FR-006, FR-008, FR-009, FR-035 or FR-038.
- [x] CHK1027 Is the additivity of both amendments stated as the CONDITION of their conformance with the boundary, rather than as a description? [Clarity, Spec §FR-030]
- [x] CHK1028 Does that additivity argument cover every artifact whose behaviour changes? [Completeness, Spec §FR-030] — FIXED: the consent cascade gate's widening was outside the argument; FR-030 now names it and gives its narrow additivity argument.
- [x] CHK1029 Is an escalation required (rather than absorption) if any of the three ceases to be additive? [Fail-closed, Spec §FR-030]

## Out-of-scope inventory

- [x] CHK1030 Is there a single place that enumerates everything out of scope, so a reader need not reconstruct it? [Completeness, plan §Out of scope, by ratification]
- [x] CHK1031 Does that list agree with the packet's own "Out of scope, deliberately" section? [Consistency, proposal §Out of scope]
- [x] CHK1032 Are the items that are out of scope for a REASON distinguished from those merely not yet done? [Clarity, plan §Out of scope, Spec §Assumptions]

## Notes

- One item carried a defect (CHK1028), fixed in FR-030 and cross-listed on the
  consent-cascade and ratified-fidelity checklists.
- CHK1026 is the item this pass had to answer about ITSELF: six requirements were
  sharpened or given predicates, and none adds capability surface, a new vocabulary
  member, or a new blocking behaviour.
