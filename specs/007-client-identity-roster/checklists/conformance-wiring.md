# Conformance Wiring Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements for the THREE ratified
wirings — intra-repo conformance that BLOCKS, cross-domain composition that
REPORTS, and drift that REFUSES issuance — including the split between them and the
residuals each carries at archive.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## The blocking wiring (pack membership)

- [x] CHK601 Is the mechanism that confers blocking status named, rather than "blocking" being asserted? [Clarity, Spec §FR-022]
- [x] CHK602 Is the pack's existing consumption contract stated as applying unchanged to the new member? [Consistency, Spec §FR-022]
- [x] CHK603 Is the absence behaviour of the new member specified (exit 0 with a notice), so adding a fourth blocking check cannot break a repo with nothing to declare? [Edge Case, Spec §FR-022, §Edge Cases]
- [x] CHK604 Is the requirement that a `mutate` entry with no ratified capability ERRORS rather than reports stated as its own clause? [Clarity, Spec §FR-014, §US3-AS2]
- [x] CHK605 Are the pack behaviours to be exercised enumerated, and traceable to the delta scenarios they come from? [Traceability, tasks §5.1]
- [x] CHK606 Is the pack's COUNT-bearing prose identified as the only such site this feature owns? [Scope, tasks §5.2]
- [x] CHK607 Is the promoted pack spec explicitly excluded from edits, with the same rule and reason as doc-health's? [Consistency, plan §decision 15, tasks §5.2]
- [x] CHK608 Is the residual that pack blocking is NOMINAL at archive recorded, with the two domain-gate facts that make it so? [Honesty, plan §Cluster F, ruling A-N2]
- [x] CHK609 Is the follow-up that would make it fire (domain-gate wiring) named as out of scope BY REQUIREMENT rather than by omission? [Scope, Spec §FR-030, §SC-012]
- [x] CHK610 Is the claim this feature is entitled to make stated exactly, so "blocking" is not read as "already firing in a domain's CI"? [Clarity, plan §Cluster F, tasks §5.3]
- [x] CHK611 Is the pack's no-copy clause — asserted in a spec acceptance scenario — either probed or declared unprobed? [Measurability, Spec §US3-AS3] — FIXED: no probe exists anywhere in the estate (the conformance-gate suite's fifteen tests cover inventory, parity and pin behaviour only), and building a copy-detector would be a new check rather than a realization of FR-022. plan §Cluster F now records it as a second residual beside A-N2's, so the clause is not read as measured.
- [x] CHK612 Is the naming asymmetry between the pack's `check-*` members and this `validate-*` member dispositioned rather than "fixed"? [Consistency, plan §Cluster F]

## The reporting wiring (doc-health family)

- [x] CHK613 Is the family's scope restricted to CROSS-DOMAIN concerns, with duplication of intra-repo rules forbidden by requirement? [Scope, Spec §FR-023]
- [x] CHK614 Is that prohibition given a measurement (no intra-repo finding code ever appears in the family's output)? [Measurability, tasks §6.6]
- [x] CHK615 Are the two finding classes defined by PREDICATE rather than by the delta's prose names? [Clarity, research §Decision 6]
- [x] CHK616 Is `shared-identity-material` keyed on identity MATERIAL rather than on collocation, so FR-024's non-finding survives? [Constraint fidelity, Spec §FR-024, research §Decision 6] — the item's wording stands, but it passed for the wrong reason before gate ruling G4: the second disjunct read `principal_locations[]`, which carries TENANT identifiers, so read literally it intersected on the shared client tenant and refused FR-024's non-finding. The disjunct is now equal `provider_object_ref` declared by BOTH entries, and the claim is true as stated.
- [x] CHK617 Is the FR-024 non-finding required to be measured by a fixture, not only stated? [Measurability, tasks §6.5, §6.6]
- [x] CHK618 Are the family's skips required to be EXPLICIT with a reason, rather than silence or a false pass? [Observability, Spec §FR-023, §US5-AS3]
- [x] CHK619 Is the skip's granularity specified (corpus-level, not per client), with the reason a per-client skip would suppress real findings? [Clarity, research §Decision 6]
- [x] CHK620 Is the resolution-class requirement stated per FINDING rather than per family, with the registry mechanics that force that choice? [Clarity, Spec §FR-023, research §Decision 6]
- [x] CHK621 Is the contested-classification rule given a test, rather than being authored and measured by nothing? [Measurability, tasks §6.6]
- [x] CHK622 Is the family id checked against the collision it was ruled to avoid, with the evidence that the neighbouring module is not a family? [Consistency, Spec §FR-023, research §Decision 6]
- [x] CHK623 Is the family's registration surface enumerated (import, `FAMILIES`, `FAMILY_IDS`) with the consequence of each? [Completeness, tasks §6.4]
- [x] CHK624 Is the pre-existing `FAMILY_IDS` omission recorded as another capability's defect and explicitly not fixed here? [Scope, research §Decision 6]

## The refusal wiring (issuance precondition)

- [x] CHK625 Is the refusal expressed as ONE neutral mechanism, with a second parallel mechanism forbidden by requirement? [Clarity, Spec §FR-028]
- [x] CHK626 Is the vocabulary's shape justified against a measured fact about live records, rather than chosen for elegance? [Traceability, research §Decision 3]
- [x] CHK627 Is the value narrowing (`const: true`) argued, so "declared false" cannot read as governance while asserting nothing? [Clarity, ruling A-3a, research §Decision 3]
- [x] CHK628 Is the semantic mirror declared STRUCTURALLY required, with the validator fact that makes it so? [Measurability, ruling A-3a, research §Decision 4]
- [x] CHK629 Are BOTH failure shapes (out-of-vocabulary member, false-valued member) required to raise the named finding? [Completeness, Spec §FR-028, tasks §7.2]
- [x] CHK630 Is the drift record's consumption by the refusal specified deterministically (an `open` status against the covering entry is the whole predicate)? [Clarity, Spec §FR-035]
- [x] CHK631 Is the scope fence stated (the vocabulary governs the credential requirement record only, not the workflow record that shares the key name)? [Scope, research §Decision 3, plan §Cluster H]
- [x] CHK632 Is the un-measurability of live refuse-then-allow stated as a consequence of a measured absence, with the measurement's real home named? [Honesty, Spec §SC-008]

## The split itself

- [x] CHK633 Is the blocking/reporting split stated as a measurable pair (nonzero exit on intra-repo nonconformance; a doc-health finding leaving the gate exit unchanged)? [Measurability, Spec §SC-006]
- [x] CHK634 Is the second half of that pair proven across BOTH corpora, rather than asserted about a corpus nothing ran? [Measurability, ruling A-N4, tasks §6.7]
- [x] CHK635 Is the test that proves it named in ONE module, so the assertion cannot land in two places or neither? [Clarity, tasks §6.7]
- [x] CHK636 Is the blocking check at least as strong as the reporting pass on the same evidence? [Consistency, Spec §FR-009, §FR-023] — FIXED: the cross-domain family's reach predicate reads admission ACTS while the intra-repo rule read only `granted_permissions[].reaches[]`, so the REPORTING pass could see reach the BLOCKING gate could not — inverting the ratified split. FR-009 now covers the act side (`undeclared-act-surface`), with a rule at tasks §2.6 and a negative at tasks §4.1.

## Notes

- Two items carried a defect (CHK611, CHK636). CHK636 is the more consequential: the
  ratified split assigns intra-repo conformance to the blocking gate, and the pre-fix
  requirements left one class of reach visible only to the nightly reporting pass.
