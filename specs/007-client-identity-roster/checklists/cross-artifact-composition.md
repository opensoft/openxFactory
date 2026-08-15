# Cross-Artifact Composition Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation that the FOUR artifacts (spec, plan, tasks,
research) plus the two rulings files compose into one coherent statement — that the
49 analyze-round fixes are all still present, that no fix was undone by a later one,
and that a term means the same thing wherever it appears.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## The analyze-round fixes are all still standing

- [x] CHK801 Is the `tests/` self-scan exclusion (round 1, F-001, the loop's one HIGH) present in BOTH plan and tasks, with its justification? [Traceability, plan §Cluster B, tasks §2.9]
- [x] CHK802 Is the OpenSpec-vs-Speckit task-numbering ambiguity (F-002) resolved by an explicit statement of which numbering a citation uses? [Clarity, Spec §Governing change]
- [x] CHK803 Are member spellings still snake_case at every declaration site after F-003's fix? [Consistency, Spec §FR-034, plan §Cluster A]
- [x] CHK804 Do the vocabulary-negative counts still reconcile after F-004 and F-027 corrected them, and after this pass added a seventh set? [Consistency, tasks §1.2, §2.3, §4.2, §4.3]
- [x] CHK805 Does plan.md's MODIFIED file list still contain only files a task touches (F-005)? [Consistency, plan §Project structure]
- [x] CHK806 Is the invented legend rule still absent, with its absence argued (F-006)? [Scope, plan §Cluster A, tasks §2.8]
- [x] CHK807 Does research Decision 3 carry its post-A-3a wording rather than the pre-gate draft (F-007)? [Consistency, research §Decision 3]
- [x] CHK808 Does ruling A-N4's test have exactly one named home (F-008)? [Clarity, tasks §6.7]
- [x] CHK809 Do the coverage-table rows still match the tasks that realize each requirement after F-009's corrections and this pass's three additions? [Traceability, tasks §Requirement → task coverage]
- [x] CHK810 Is the FR-030 baseline still written OUTSIDE the tracked tree (F-010), given every commit in this lane stages the feature directory wholesale? [Scope, tasks §0.3]
- [x] CHK811 Is the verification-timing convention (work and verification may land in different phases) still stated, so F-011's apparent cycle is not re-raised? [Clarity, tasks §Format]
- [x] CHK812 Do the negative totals reconcile after F-012's correction and this pass's additions? [Consistency, plan §Cluster C]
- [x] CHK813 Does Phase 7 still state why it has no build dependency despite naming an artifact fixed in Phase 1 (F-013)? [Clarity, tasks §Phase 7 header]
- [x] CHK814 Are the three external-checkout dependencies still established by a Phase 0 task (F-014)? [Dependency, tasks §0.3]
- [x] CHK815 Are the README claims in research still true of the tree (F-015)? [Traceability, research §Examples layout]
- [x] CHK816 Do the `admission_surface` member descriptions still carry act-and-mechanism content (F-016)? [Completeness, tasks §1.2]
- [x] CHK817 Is the "two acts → two surfaces" reconciliation still present in BOTH research and plan (F-017)? [Consistency, research §Decision 1, plan §Cluster D]
- [x] CHK818 Does the `traceability.yaml` specification still match the 006 file's ACTUAL shape (F-018)? [Consistency, tasks §10.1]
- [x] CHK819 Is the pack-scenario provenance still stated across two deltas rather than miscounted (F-019)? [Traceability, tasks §5.1]
- [x] CHK820 Is `duty_separation_rationale` still declared as a field wherever the alias rule reads it (F-020)? [Completeness, Spec §FR-001, §FR-038]
- [x] CHK821 Does `standing_credential_attestation` still carry a shape that keeps its falsification record-internal (F-021)? [Clarity, Spec §FR-013, plan §Cluster A]
- [x] CHK822 Is FR-014's citation RESOLUTION still specified with a mechanism (F-022, F-036), and still intra-repo? [Completeness, Spec §FR-014, plan §Cluster B]
- [x] CHK823 Is `ratified_by` still explicitly NOT resolved (F-028's revert of an over-reach)? [Scope, Spec §FR-014, plan §decision 19]
- [x] CHK824 Does the green bar still include the feature's own test package (F-029)? [Completeness, plan §The green bar]
- [x] CHK825 Is the doc-health invocation still expressed from a cwd where the path exists (F-030)? [Clarity, tasks §6.4, §10.3]
- [x] CHK826 Is `granted_permissions[]` still specified as objects at every site that reads it (F-037, F-042, F-043)? [Consistency, Spec §FR-004, plan §Cluster A, tasks §1.5, §2.4]
- [x] CHK827 Is `per_unit_principal_available` still per-surface at every site (F-038)? [Consistency, Spec §FR-008, tasks §1.5, §1.7]
- [x] CHK828 Does FR-010's name check still read a field the ratified record has (F-039)? [Consistency, Spec §FR-010]
- [x] CHK829 Is `exceeds_governed_unit` still present as field, rule, positive and negative (F-040, F-041, F-047)? [Traceability, Spec §FR-002, plan §Cluster A/B/D, tasks §1.6, §2.5, §3.2, §4.1]
- [x] CHK830 Do Key Entities and the Constitution I row still describe the design as it now is (F-044, F-045, F-046)? [Consistency, Spec §Key Entities, §Assumptions, plan §Constitution Check]
- [x] CHK831 Is FR-001's exhaustiveness claim still reconciled with FR-002's act-level addition (F-048)? [Consistency, Spec §FR-001, §FR-002]
- [x] CHK832 Are the artifacts free of the wrap defects rounds 4, 7 and 8 fixed (F-035, F-049)? [Clarity, all four artifacts]

## Terminology and internal agreement

- [x] CHK833 Does each coined term have exactly one spelling across all four artifacts? [Consistency, all four artifacts]
- [x] CHK834 Do the two globs used to find fragments agree? [Consistency, plan §Cluster G, research §Decision 6] — FIXED: research read `*.yaml`, plan and tasks `*.y*ml`; research now matches, and the consequence of the mismatch (a `.yml` fragment visible to the gate and invisible to the reporting pass) is recorded.
- [x] CHK835 Do the finding-code names used in plan and tasks match one another? [Consistency, plan §Cluster B, tasks §2.5–2.9]
- [x] CHK836 Are the new codes introduced by this pass spelled identically in spec, plan and tasks? [Consistency, Spec §FR-008/§FR-009, plan §Cluster B, tasks §2.6]
- [x] CHK837 Do the requirement ids run without gaps or duplicates (FR-001..FR-039, SC-001..SC-014)? [Traceability, Spec §Requirements, §Success Criteria]
- [x] CHK838 Does every plan cluster map to exactly one task phase, and vice versa? [Consistency, plan §Design by deliverable cluster, tasks §Phase order]
- [x] CHK839 Are the plan's reviewable decisions numbered continuously as later passes add to them? [Traceability, plan §Decisions this plan makes]
- [x] CHK840 Does research.md remain the derivations record rather than duplicating plan prose? [Scope, research §preamble] — Checked after this pass: the six checklist additions are recorded as Decision 9 with derivations, and the plan carries them as decisions 25-30 in one line each.
- [x] CHK841 Is every ruling id referenced by an artifact actually present in one of the two rulings files? [Traceability, plan §Plan-gate rulings applied]
- [x] CHK842 Do the artifacts agree on what is an archive blocker and what is a follow-up? [Consistency, Spec §Governing change, plan §Cluster F, tasks §5.3]

## Notes

- One item carried a defect (CHK834). The 49 prior fixes were all found intact; three of
  them (F-020, F-037, F-040) are the direct ancestors of this pass's own findings — each
  was "a rule with no field to read", and this pass found the same shape three more times
  (act-side reach, mapping coverage, the verification pair).
