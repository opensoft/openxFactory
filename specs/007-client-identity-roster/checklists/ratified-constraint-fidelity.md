# Ratified-Constraint Fidelity Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation that the requirements ENCODE the ratified
position rather than restate, soften, or quietly extend it — the five ratified
answers, the two killed flaws, Brett's Decisions A and B, and the ten binding
constraints. Encoding them is the work; relitigating them is failure.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)
**Authorities**: `openspec/changes/add-client-identity-roster/` (proposal, design,
five deltas, `clarify-questions.md`, `review/`), the seed handoff's killed-flaw
block, `clarify-rulings-2026-08-14.md`, `plan-gate-rulings-2026-08-14.md`.

## The five ratified answers

- [x] CHK101 Is residency stated as class-INDEPENDENT, with no branch on authority class anywhere in schema, validator, examples or documentation? [Constraint 1, Spec §FR-012, plan §Cluster A]
- [x] CHK102 Is the class-independence expressed as a mechanized check (a grep asserting no `authority_class` inside a residency branch) rather than as prose discipline? [Measurability, Constraint 1, tasks §1.8]
- [x] CHK103 Are all THREE blocking behaviours present as requirements — intra-repo blocks, cross-domain reports, drift refuses issuance — with none demoted to a successor? [Constraint 2, Spec §FR-022, §FR-023, §FR-028]
- [x] CHK104 Is the enrollment axis kept permissive, with `planned` legal and indefinite and per-unit/per-duty identities never penalised? [Constraint 3, Spec §FR-013, §FR-032]
- [x] CHK105 Is the ratified lever for cost pressure (the multi-tenant model with obligations) named, so the axis cannot be relaxed quietly instead? [Constraint 3, Spec §Ratified constraints]
- [x] CHK106 Are the archive blockers enumerated as contract records AND consent cascade AND doc-health family AND the two amendment-added tasks, with only the domain fragments exempt? [Constraint 4, Spec §Governing change, rulings §C2]
- [x] CHK107 Is `admission_surface` closed to exactly `business_central` and `exchange`, with the extension route named rather than left open? [Constraint 5, Spec §FR-007]
- [x] CHK108 Is the named successor for non-Entra providers (`client-infrastructure-liaison`) carried into the requirement, so the successor cannot be forgotten? [Constraint 5, Spec §FR-007, §Edge Cases]

## The two killed flaws

- [x] CHK109 Is uniqueness keyed on FIVE elements including blast-radius unit and duty, so a per-environment identity is representable? [Killed flaw (a), Spec §FR-006]
- [x] CHK110 Is there an explicit requirement that a per-unit or duty-separated identity MUST NOT be reported as an overlap, a duplicate, or any other finding? [Killed flaw (a), Spec §FR-006]
- [x] CHK111 Are the killed-flaw regression POSITIVES required as fixtures (a genuine per-unit pair and a genuine duty pair at zero findings), not merely as prose? [Killed flaw (a), Spec §FR-017, §SC-002]
- [x] CHK112 Does any rule, in any artifact, fire on a genuine per-unit or duty-separated pair? [Killed flaw (a), Spec §FR-038] — FIXED: the uniqueness rule's SCOPE was unstated, and a cross-fragment reading would have reported a domain's two clients' identical `sandbox1` tuples as one duplicate. FR-006 now scopes uniqueness within a fragment, plan §Cluster A and tasks §2.4 carry it, and repo fixture 1 (tasks §4.5) measures it with two clients' fragments at exit 0.
- [x] CHK113 Is the alias rule bounded so it cannot broaden into the killed rule, with all three predicates required together? [Killed flaw (a), Spec §FR-038]
- [x] CHK114 Is the alias rule ALSO bounded so it cannot be evaded, rather than being safe only because it is toothless? [Killed flaw (a), Spec §FR-038] — FIXED: "solely in a free token" admitted a one-token-only reading a domain could evade by inventing two spellings; FR-038, plan §Cluster B and tasks §2.4 now read "in free tokens ONLY", which cannot touch a genuine pair (they differ in `achieved_scope`, in permissions, or declare the rationale).
- [x] CHK115 Is the authority-class enumeration closed to `observe|mutate`, with a destructive class UNREPRESENTABLE rather than merely discouraged? [Killed flaw (b), Spec §FR-005]
- [x] CHK116 Is the conformant expression of destructive capability (achieved class on the `mutate` entry plus its gate obligation) stated, so refusing the class does not lose the capability? [Killed flaw (b), Spec §FR-005, tasks §1.2]
- [x] CHK117 Does any requirement demand an entry for a class whose ratified position is that the factory holds NO identity — the route by which killed flaw (b) would return? [Killed flaw (b), Spec §FR-032, §Edge Cases]
- [x] CHK118 Is the ratified `microsoft_managed_node_inventory_reader` case (provider-forced multi-surface breadth) still conformant under every rule the spec states? [Killed flaw (a), Spec §FR-009, §FR-019]

## Decisions A and B (Brett, 2026-08-14)

- [x] CHK119 Is pack enrollment stated as an ARCHIVE BLOCKER realized through pack membership, not as a successor? [Decision A, Spec §FR-022]
- [x] CHK120 Is the reason pack membership is the mechanism (it is the only promoted route conferring blocking status) carried into the requirement? [Decision A, Spec §FR-022]
- [x] CHK121 Is the `domain-conformance-checks` MODIFIED delta named as a condition of enrollment, so enrollment cannot happen as an undeclared modification? [Decision A, Spec §FR-022, packet §specs/domain-conformance-checks]
- [x] CHK122 Is the neutral home of the refusal a CLOSED `issuance_preconditions` vocabulary on the canonical credential schema, with the roster-drift member? [Decision B, Spec §FR-028]
- [x] CHK123 Is "one mechanism, never a second parallel one" stated, and is the domain-local precedent explicitly regularized rather than replaced in place? [Decision B, Spec §FR-028]
- [x] CHK124 Is the fixture-proven nature of the neutral criterion stated as a consequence of a measured fact (no live drift producer at archive), rather than as a convenience? [Decision B, Spec §SC-008]
- [x] CHK125 Are both amendments reconciled with the no-domain-edit boundary by an ADDITIVITY argument that is stated and falsifiable? [Decisions A+B, Spec §FR-030]
- [x] CHK126 Is the additivity argument complete — does it cover every place an existing artifact's behaviour changes? [Consistency, Spec §FR-030] — FIXED: FR-030 argued additivity for the optional property and the enum member but omitted the one real behaviour change, the consent cascade gate widening to `withdrawn` (ruling A-6). FR-030 now names it and gives its narrow additivity argument (it can only bind a state that could not exist before).

## Ratified text handling

- [x] CHK127 Is every ratified constraint restated in the spec traceable to the packet clause it encodes, so a reader can check the encoding rather than trust it? [Traceability, Spec §Ratified constraints]
- [x] CHK128 Where a ruling and the spec disagree, is the precedence rule stated (rulings win) rather than left to the reader? [Clarity, Spec §Governing rulings]
- [x] CHK129 Are the ruling ids that amended the plan (R-N1, A-2..A-16, A-N2..A-N4) each traceable to the artifact text that encodes them? [Traceability, plan §Plan-gate rulings applied]
- [x] CHK130 Does any requirement extend the ratified scope by adding a fifth modified capability, a new surface, or a new blocking behaviour? [Constraint fidelity, Spec §FR-031, plan §Constitution Check II]
- [x] CHK131 Is the ratified refusal of "our own ratification justifies standing" preserved — consent required, and the citation required to RESOLVE? [Constraint fidelity, Spec §FR-014]
- [x] CHK132 Is the ratified "declared, CHECKABLE, tested" degradation obligation given something to check, rather than being satisfied by a declaration nothing reads? [Constraint fidelity, Spec §FR-002, §FR-010]
- [x] CHK133 Are the ratified vendor-tenant-multi obligations carried in full (allow-list at token validation, per-client authorization state, per-client revocation evidence, credential-span statement, per-client consent amendment)? [Completeness, Spec §FR-012, packet delta §Residency]
- [x] CHK134 Is the LedgerxFactory residency conflict left to Brett rather than resolved by this feature? [Constraint fidelity, Spec §Assumptions, §Out of scope]

## Notes

- Three items carried a defect (CHK112, CHK114, CHK126); all three were fixed in
  spec.md, plan.md and tasks.md and re-marked. Two of the three protect a killed flaw
  from returning by a route the analyze loop did not sweep: the SCOPE of the uniqueness
  comparison, and the ARITY of "solely in a free token".
- No item on this checklist required touching a ruling, ratified packet text, or either
  of Brett's decisions. No ESCALATION was raised.
