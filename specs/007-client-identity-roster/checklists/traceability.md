# Traceability Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation that every ratified obligation can be followed
forward to an artifact and a probe, and every artifact backward to the clause that
demanded it — packet clause → requirement → task → verification → traceability row.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Forward: packet → requirement

- [x] CHK1101 Does every requirement of the ADDED capability delta map to at least one FR? [Traceability, packet §specs/client-identity-roster]
- [x] CHK1102 Does every SCENARIO of the ADDED delta map to a requirement or an acceptance scenario? [Traceability, Spec §US1–US6]
- [x] CHK1103 Does each of the four MODIFIED deltas map to at least one FR and one SC? [Traceability, Spec §FR-022/023/026/028, §SC-006/007/008/009]
- [x] CHK1104 Are the packet's numbered proposal items each traceable into the spec, so an item cannot be dropped silently? [Traceability, proposal §What Changes]
- [x] CHK1105 Is each of the twelve clarify rulings traceable into the requirement it produced? [Traceability, Spec §Clarifications]
- [x] CHK1106 Is each plan-gate ruling traceable into the artifact text that encodes it? [Traceability, plan §Plan-gate rulings applied]
- [x] CHK1107 Is R-N1's verification obligation recorded as DISCHARGED, with the sweep it required? [Traceability, plan §preamble, research §Ruling R-N1]
- [x] CHK1108 Are the two escalated decisions traceable from the ruling that raised them to the outcome Brett gave? [Traceability, rulings §Escalated]

## Forward: requirement → task → verification

- [x] CHK1109 Does every FR appear in the requirement→task coverage table? [Traceability, tasks §Requirement → task coverage]
- [x] CHK1110 Does every SC appear there too, rather than only the FRs? [Traceability, tasks §Requirement → task coverage]
- [x] CHK1111 Does every task name its TARGET FILES and its VERIFICATION, so no task can be "done" by assertion? [Measurability, tasks §Format]
- [x] CHK1112 Are the coverage-table rows accurate against the task text after this pass's edits? [Consistency, tasks §Requirement → task coverage] — FIXED with the fixture additions: FR-006 now cites fixture 1, FR-013 cites the `retired` entry, SC-014 cites the drift-status negative and the schema task that declares the set.
- [x] CHK1113 Does every user story have at least one task carrying its label? [Traceability, tasks §Format]
- [x] CHK1114 Are the acceptance scenarios of each story each answerable by a named probe or explicitly declared unmeasurable? [Measurability, Spec §US1–US6] — Two are declarations rather than probes and are now BOTH declared: live refuse-then-allow (SC-008) and the pack's no-copy clause (plan §Cluster F, fixed this pass).
- [x] CHK1115 Are the rules that have no packaged home routed to a named alternative corpus rather than dropped? [Traceability, plan §Cluster C, research §Decision 7]
- [x] CHK1116 Is each negative fixture traceable to the requirement it confirms, by filename and by registration? [Traceability, tasks §4.1–4.4]
- [x] CHK1117 Are the fixtures added by this pass traceable to their requirement clause? [Traceability, tasks §4.1, §4.3] — `undeclared-act-surface` → FR-009; `per-unit-principal-undeclared` → FR-008; `drift-finding-status-out-of-vocabulary` → FR-035/SC-014.

## The traceability record itself

- [x] CHK1118 Is a machine-readable traceability record required, in a named shape? [Completeness, tasks §10.1]
- [x] CHK1119 Is that shape anchored to the ACTUAL precedent file rather than to a description of it? [Consistency, tasks §10.1]
- [x] CHK1120 Are the record's field names specified (statement, artifact, enforced_by, negative_confirmation, red_proven) rather than paraphrased? [Clarity, tasks §10.1]
- [x] CHK1121 Is the extension over the precedent (SC rows) declared as an extension? [Clarity, tasks §10.1]
- [x] CHK1122 Is `red_proven` defined operationally, and is the reason the record is deferred to implementation stated? [Measurability, tasks §10.1]
- [x] CHK1123 Is an explicit `n/a` with a reason required for positive-only criteria, so a blank cannot pass as coverage? [Fail-closed, tasks §10.1]
- [x] CHK1124 Is the record required to carry a schema envelope like every other YAML in the tree? [Consistency, tasks §10.1]
- [x] CHK1125 Is a coverage check over the record required (every id has a row; no row's `red_proven` is unset)? [Measurability, tasks §10.1]
- [x] CHK1126 Are the residual notes that must travel with specific rows named, so a known limitation reaches the reviewer? [Completeness, tasks §5.3, §10.1]

## Backward: artifact → clause

- [x] CHK1127 Can every NEW file in the project structure be traced to the requirement that demands it? [Traceability, plan §Project structure]
- [x] CHK1128 Can every MODIFIED file be traced to a task and a requirement? [Traceability, plan §Project structure]
- [x] CHK1129 Is every NOT-EDITED entry justified by a stated rule rather than by omission? [Clarity, plan §Project structure]
- [x] CHK1130 Are the plan's own decisions listed for review, with the rulings that upheld, amended or broke each? [Traceability, plan §Decisions this plan makes]
- [x] CHK1131 Are decisions added after the plan gate marked with their origin (analyze pass, checklist pass), so a reader can date each? [Traceability, plan §decisions 18–30]
- [x] CHK1132 Does the research record carry a derivation for each decision rather than a preference? [Clarity, research §Decisions 1–9]
- [x] CHK1133 Are measured facts distinguished from assumed ones throughout, with dates on the measurements? [Honesty, research §Convention and tree findings]
- [x] CHK1134 Are the line-number citations into the tree accurate? [Traceability, research §Decision 5, §Decision 6, plan §Cluster I] — Spot-verified in this pass: the consent schema's status enums, the dependent-ref enum, the cascade check, `NEUTRAL_STATUSES`, `PAST_SIGNATURE_STATUSES`, the credential validator's self-test line, `make_ctx`'s default, the doc-health registry lines, `FAMILY_IDS`, the release-surface path tuple and the two determinism/fixture-scan tests all resolve to the cited lines.

## Notes

- One item carried a bookkeeping defect (CHK1112), corrected with the fixture additions.
- CHK1134 was resolved by reading the cited lines rather than trusting them; every
  citation in research.md and plan.md that names a file and a line resolved correctly,
  which is what makes the "measured, not assumed" claim in those files load-bearing.
