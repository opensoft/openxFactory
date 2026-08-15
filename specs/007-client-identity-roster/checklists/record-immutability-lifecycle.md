# Record Immutability and Document Lifecycle Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements governing GOVERNANCE
DOCUMENTS this feature touches or creates — `Status: record` immutability, promoted
spec text, status headers and provenance, the doc index, and the self-gating risk
that doc-health reports a finding against the very change that grows it.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Records are never edited

- [x] CHK901 Is the immutability of the packet's `Status: record` review files stated as a rule the feature must not break? [Constraint, plan §Constitution III, tasks §Notes]
- [x] CHK902 Is the sanctioned route for a further amendment named (a sibling record file, never an append or edit)? [Clarity, research §Record immutability]
- [x] CHK903 Is the precedent for that route cited from the tree itself rather than asserted? [Traceability, research §Record immutability]
- [x] CHK904 Is the severity of breaking it stated (the doc-health family treats a changed record as CRITICAL), so the rule is not read as etiquette? [Clarity, research §Record immutability]
- [x] CHK905 Does any task in the feature write to a path under the packet's `review/`? [Scope, tasks §Notes, plan §Project structure]
- [x] CHK906 Are the rulings files of this feature (themselves decision records) excluded from casual edit, with precedence stated instead? [Clarity, Spec §Governing rulings]

## Promoted spec text

- [x] CHK907 Is the rule that promoted spec text is rewritten by the archive step, not by this feature, stated for doc-health? [Scope, Spec §FR-025]
- [x] CHK908 Is the same rule extended to the OTHER promoted specs this change modifies, rather than left implicit? [Consistency, plan §decision 15]
- [x] CHK909 Are the three promoted spec paths named explicitly in the NOT-EDITED list? [Completeness, plan §Project structure, tasks §Notes]
- [x] CHK910 Is the measurement of agreement stated as agreement with the RATIFIED DELTA wording rather than with promoted text? [Clarity, Spec §FR-025]
- [x] CHK911 Is the tolerated window (promoted text says fifteen while the code implements sixteen) declared, with the evidence that it is already the tree's state? [Honesty, Spec §Assumptions]
- [x] CHK912 Is the absence of any automated count assertion recorded as the fact that makes the window safe? [Traceability, Spec §FR-025, research §Decision 6]
- [x] CHK913 Is the distinction between a COUNT and an ORDINAL stated, with the ordinal sites explicitly left alone? [Clarity, Spec §FR-025]
- [x] CHK914 Are the count-bearing prose sites this feature OWNS enumerated exhaustively, so "at minimum" cannot hide a missed site? [Completeness, Spec §FR-025, research §Decision 6]

## New documents and their headers

- [x] CHK915 Is a status header required on every new governance document the feature creates? [Completeness, plan §Constitution III]
- [x] CHK916 Is the header's CONTENT specified (`Status: ratified` plus a `Ratified by:` line naming the change and the bundle), with the precedent it follows? [Clarity, tasks §3.1, research §Examples layout]
- [x] CHK917 Is the provenance line required to resolve to an OpenSpec change that exists while the change is still ACTIVE, rather than only after archive? [Edge Case, tasks §3.1] — Checked against the family that would fire: it accepts an active or archived change id, so a `Status: ratified` document naming this still-active change is green today.
- [x] CHK918 Are the new documents required to be linked into the repository's document index? [Completeness, tasks §9.5, plan §Constitution IV]
- [x] CHK919 Is the schema envelope requirement (`schema_version` + `kind`) stated for every new YAML, including the traceability record? [Completeness, plan §Constitution IV, tasks §10.1]
- [x] CHK920 Are example files declared as instantiation stubs rather than live configuration? [Clarity, plan §Constitution IV]

## Self-gating

- [x] CHK921 Is "doc-health reports no new finding against this change or its documents" stated as an explicit success criterion rather than assumed? [Measurability, Spec §SC-009, §SC-010]
- [x] CHK922 Is that measurement scheduled as a runnable step over an aggregation checkout? [Measurability, tasks §10.3]
- [x] CHK923 Is the risk that the feature's own new family fires on the feature's own documents considered? [Edge Case, Spec §FR-023] — The family reads only `credentials/client-identity-roster/` fragments and skips a single-repo run; the feature's documents are not in its input set. The whole-repo sweep's `tests/` and `examples/` exclusions cover the other direction.
- [x] CHK924 Are the checklist files created by THIS pass outside the governed corpus, so they cannot themselves produce a status-validity finding? [Edge Case, doc-health §GOVERNED_ROOTS] — Verified: the governed roots are `contracts`, `docs`, `examples`, `ideation`, `templates`; `specs/` is not scanned, which is also why the five earlier features' checklists carry no consequences.
- [x] CHK925 Is the retained `retired` roster entry reconciled with record-immutability expectations elsewhere in the corpus? [Edge Case, Spec §Edge Cases] — Retention is an entry-level lifecycle state inside a YAML contract record, not a `Status: record` governance document; the immutability family reads document status headers only, and SC-010's no-new-finding measurement is the guard if that ever changed.
- [x] CHK926 Is the amendment record's own precedent (a companion file rather than an append) preserved by this pass? [Consistency, research §Record immutability] — This pass wrote no file under the packet; its decisions live in the feature's own artifacts and in this checklist set.

## Notes

- No item on this checklist carried a defect. Three items (CHK917, CHK923, CHK924) were
  resolved by reading the mechanism rather than the prose, because each is a place where
  a plausible-sounding rule would have produced a finding against the feature itself.
