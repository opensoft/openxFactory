# Requirements Quality Checklist: Client Identity Roster Neutral Contracts

Status: draft

**Purpose**: Cross-cutting release-gate validation of the requirements themselves —
completeness, clarity, consistency, acceptance-criteria quality, dependencies and
assumptions, ambiguities and conflicts. Unit tests for the English, not verification
of an implementation that does not exist yet.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)
**Depth**: formal release gate (no-argument invocation = maximum coverage; no item cap)
**Inputs read**: spec.md, plan.md, tasks.md, research.md, clarify-rulings-2026-08-14.md,
plan-gate-rulings-2026-08-14.md, analyze-round-1..8, the amended packet
(`openspec/changes/add-client-identity-roster/`), and the seed handoff.
**Resolution**: every item resolved 2026-08-14. `[x]` = passes as written; items whose
defect was fixed in this pass carry a FIXED note naming the edit.

## Requirement Completeness

- [x] CHK001 Are all thirteen ratified roster requirements of the packet's ADDED capability represented by at least one FR? [Completeness, packet §specs/client-identity-roster]
- [x] CHK002 Is every field of the ratified entry list (OpenSpec task 2.1) enumerated in the spec rather than summarized? [Completeness, Spec §FR-001]
- [x] CHK003 Are the additions to the ratified field list (legend, `duty_separation_rationale`, `exceeds_governed_unit`) each justified in the requirement that adds them, so a reviewer can see they are not scope creep? [Completeness, Spec §FR-001, §FR-002]
- [x] CHK004 Does every one of the five capabilities (one ADDED, four MODIFIED) carry at least one requirement of its own? [Completeness, Spec §Capabilities realized, §FR-022/023/026/028]
- [x] CHK005 Are requirements defined for all three ratified wirings (blocking gate, reporting family, issuance refusal) rather than only for the contract records? [Completeness, Spec §FR-022, §FR-023, §FR-028]
- [x] CHK006 Are the deliberately-absent behaviours (completeness enforcement, freshness decay, enrollment automation, drift remediation) each stated as an explicit NON-requirement rather than left unmentioned? [Completeness, Spec §FR-029, §FR-032, §FR-033]
- [x] CHK007 Is the drift-finding record's field list complete enough to be authored from the spec alone (identity ref, fragment ref, rule id, both values, both timestamps, status, disposition)? [Completeness, Spec §FR-035]
- [x] CHK008 Does the spec state where domain fragments live, so "the contract exists but is unreachable" is not a possible outcome? [Completeness, Spec §FR-020]
- [x] CHK009 Are registration obligations (manifest row, digest, CHANGELOG, bundle, consumption rule) stated for every schema the feature edits, not only the new one? [Completeness, Spec §FR-021]
- [x] CHK010 Is the fixture obligation stated as a per-rule floor rather than a fixed count, so a rule added later inherits the obligation? [Completeness, Spec §FR-016]
- [x] CHK011 Are the six user stories each given an independent test, so no story's value depends on a later story landing? [Completeness, Spec §US1–US6]
- [x] CHK012 Does every requirement that introduces a check also say what the finding NAMES, so the message is specified and not left to the implementer? [Completeness, Spec §FR-006, §FR-009, §FR-034, §FR-036]

## Requirement Clarity

- [x] CHK013 Is "admission surface" defined by the act that admits rather than by a product name, so the closed vocabulary is falsifiable? [Clarity, Spec §FR-007, §Key Entities]
- [x] CHK014 Is "effective reach" defined concretely (the set of `(surface, achieved_scope)` pairs over verified acts plus the derived exceedance flag) rather than as the word "union"? [Clarity, Spec §FR-003]
- [x] CHK015 Is "in force" for a consent instrument defined against the consent family's own closed lifecycle rather than left as a judgement? [Clarity, Spec §FR-014]
- [x] CHK016 Is "checkable against granted permissions" given a shape (declared `achieves`/`reaches[]` beside each provider-native id) rather than implying a provider-catalogue lookup? [Clarity, Spec §FR-004, §Assumptions]
- [x] CHK017 Is the distinction between the entry's string `identity_ref` and the drift record's object `identity_ref` stated where both appear? [Clarity, Spec §FR-035, plan §Cluster A]
- [x] CHK018 Are member spellings fixed to one dialect (snake_case tokens; hyphenated English only as prose), so a reader cannot infer two vocabularies? [Clarity, Spec §FR-034]
- [x] CHK019 Is "declared placement" stated as a path pattern a validator can test rather than as guidance? [Clarity, Spec §FR-020, §FR-036]
- [x] CHK020 Is the unverified admission state defined by an observable absence (no evidence reference and no verification time) rather than by an author-assertable flag? [Clarity, Spec §FR-002, §FR-003] — FIXED: the evidence/time PAIR is now stated in FR-002 and FR-003; before this pass the state was described but the record could carry a verification time with no evidence, which no requirement dispositioned.
- [x] CHK021 Is the scope of the uniqueness comparison (which entries are compared with which) stated? [Clarity, Ambiguity, Spec §FR-006] — FIXED: FR-006 now scopes uniqueness WITHIN a fragment; the unscoped reading pooled a repo's fragments and would have reported two clients' per-unit identities as one duplicate.
- [x] CHK022 Is "solely in a free token" unambiguous as to whether one or both free tokens may differ? [Ambiguity, Spec §FR-038] — FIXED: FR-038 now reads "in free tokens ONLY", closing a two-spelling evasion.

## Requirement Consistency

- [x] CHK023 Do the spec's ten binding constraints agree with the packet's proposal, design and five deltas without any softening? [Consistency, Spec §Ratified constraints]
- [x] CHK024 Does the spec's own count of MODIFIED capabilities (four) agree with the amended proposal and with SC-010 and FR-030? [Consistency, Spec §FR-030, §SC-010]
- [x] CHK025 Do FR-016's named-rule list, plan.md's coverage table, and tasks.md's fixture tasks agree on which rules are homed where? [Consistency, Spec §FR-016, plan §Cluster C, tasks §4.1–4.8]
- [x] CHK026 Do the requirement, the plan cluster, and the task that realize each rule use the same finding-code spelling? [Consistency, Spec §FR-036, plan §Cluster B, tasks §2.9]
- [x] CHK027 Is the treatment of promoted spec text consistent across all three modified promoted capabilities (never edited here; rewritten at archive)? [Consistency, Spec §FR-025, plan §decision 15]
- [x] CHK028 Are the two documents that define "archive blockers" (spec front matter and ruling C2) in agreement about which tasks block? [Consistency, Spec §Governing change, rulings §C2]
- [x] CHK029 Does the glob used to read fragments agree between the intra-repo validator and the cross-domain family? [Consistency, plan §Cluster G, research §Decision 6] — FIXED: research.md read `*.yaml` where plan/tasks read `*.y*ml`; a `.yml` fragment the gate accepts would have been invisible to the reporting pass.

## Acceptance Criteria Quality

- [x] CHK030 Is every success criterion stated as an outcome a run can decide, rather than as an intention? [Measurability, Spec §SC-001–SC-014]
- [x] CHK031 Are criteria that cannot be measured in this release explicitly declared unmeasurable, with the measurement's real home named? [Measurability, Spec §SC-008]
- [x] CHK032 Is the killed-flaw criterion expressed as a DISCRIMINATION (genuine pairs clean in the same run the alias pair is refused) rather than as two separate assertions? [Measurability, Spec §SC-002]
- [x] CHK033 Does the "absence is never a finding" criterion include a negative measurement (no code path derives an expected entry set), not only positive ones? [Measurability, Spec §SC-013]
- [x] CHK034 Is the closed-vocabulary criterion quantified by a probe per closed set rather than by the phrase "every closed vocabulary"? [Measurability, Spec §SC-014] — FIXED: SC-014 enumerated six sets while the family has seven (the drift record's `status`); it now names all seven and points the credential-side set at SC-008.
- [x] CHK035 Is the green bar expressed as runnable commands with an expected exit, and does it match the tasks that run them? [Measurability, plan §The green bar, tasks §10.2–10.6]

## Dependencies and Assumptions

- [x] CHK036 Is every assumption stated as an assumption, with the fact it rests on and how it was verified? [Assumption, Spec §Assumptions]
- [x] CHK037 Are the assumptions that later proved stale corrected in place rather than left standing (the BC evidence chain's branch)? [Assumption, Spec §Assumptions, research §BC evidence chain]
- [x] CHK038 Are the external artifacts the work depends on (aggregation checkout, OpsxFactory checkout) named, with an escalation path when absent? [Dependency, tasks §0.3]
- [x] CHK039 Is the one provider fact the packaged corpus needs treated as a precondition with a stop-and-escalate branch rather than as a discovery? [Dependency, tasks §0.1, research §Decision 8]
- [x] CHK040 Are dependencies on ACTIVE concurrent lanes (the `shared_identity` module, `add-dispatch-credential-contract`) identified and dispositioned? [Dependency, Spec §FR-023, research §Decision 6]
- [x] CHK041 Is the assumption that promoted text may lag the implementation stated with the reason it is safe (no automated count assertion)? [Assumption, Spec §FR-025, §Assumptions]

## Ambiguities and Conflicts

- [x] CHK042 Are the two things that LOOK like contradictions between the packet and this feature recorded so a later reader does not re-open them? [Conflict, plan §Contradictions found]
- [x] CHK043 Is the packaging conflict (packet's single example file vs the directory convention) dispositioned by an explicit supersession rather than by silence? [Conflict, Spec §Assumptions, tasks §Format]
- [x] CHK044 Is the "two acts → two surfaces" delta scenario reconciled with the one-surface BC worked case, with the measured reason? [Conflict, research §Decision 1, plan §Cluster D]
- [x] CHK045 Is the FR-021 wording gap (a "refresh" for a schema with no row) recorded rather than silently performed? [Ambiguity, plan §decision 13, research §A registration gap]
- [x] CHK046 Does any `[NEEDS CLARIFICATION]` marker remain anywhere in the artifacts? [Ambiguity, Spec §Governing rulings]
- [x] CHK047 Where a requirement admits two readings, is the chosen reading recorded as a reading (with the rejected one named) rather than asserted? [Ambiguity, Spec §FR-014, plan §decisions 18–19]

## Notes

- Domains generated in this pass: 17 files (see the directory). Domains CONSIDERED and
  deliberately not generated: `ux`, `accessibility` and `performance` (the feature ships
  YAML contracts, a batch validator and a nightly deterministic family — no interface, no
  latency budget, no requirement in spec.md touches any of the three); `api` (no service
  surface; contract consumption is covered by versioning-registration and
  conformance-wiring); `configuration` and `idempotency` (folded into
  validator-determinism, whose determinism and single-argument consumption items cover
  them); `deployment`/`rollback` (folded into versioning-registration, where the bundle
  cut and the digest inventory live).
- Every item above was resolved against the artifacts on 2026-08-14. Seven items carried
  a defect; each was fixed in the artifact and re-marked, in the same discipline the
  eight analyze rounds used.
