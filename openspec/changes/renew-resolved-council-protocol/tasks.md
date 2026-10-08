# Governance and handoff tasks

Executable implementation tasks belong only to the one Speckit feature allocated after ratification. This list tracks packet preparation, gates and evidence acceptance.

## 1. Preparation

- [x] 1.1 Prepare proposal, complete spec delta, D1–D5 design, decision packet and provider handoff; verify packet strict validation and all links.
- [x] 1.2 Record old #517 disposition, current bundle and sibling/ownership inspection; verify no release reservation or inherited ratification.

## 2. Owner decision and feature handoff

- [ ] 2.1 OWNER: Brett ratifies this exact reviewed packet or supplies amendments; retain the box and record verbatim words, reviewed head and date beside it.
  - Recorded 2026-10-03: Brett Heap, verbatim **"ratify all three as disclosed"**, over reviewed head `b5cdf154208c1a5fd59e3936b483f37448ca85f9`; **RATIFIED AS DISCLOSED**, without amendments. See [ratification record](review/ratification-2026-10-03.md). Owner-act box intentionally retained.
- [x] 2.2 After ratification, accept/claim provider ownership and allocate exactly one Speckit feature; verify its explicit backlink and constitution gate where applicable.
  - Recorded 2026-10-08, under Brett Heap's ruling verbatim "Dated correction + tick 2.2 (Recommended)" (brett-wip `lanes/log/codeXfactory-2.md`, RULED 2026-10-08T23:03:35Z). Ownership: lane codeXfactory-2 CLAIMED this scope at 2026-10-07T10:39:11Z after a sibling search; builder ruled 2026-10-08T17:43:04Z, "This lane, 035 then 025 (Recommended)". Feature: [`035-renew-resolved-council-protocol`](../../../specs/035-renew-resolved-council-protocol/spec.md), the sole one. Backlink: its spec names this change as its governing change and links the [ratification record](review/ratification-2026-10-03.md). Constitution gate: [plan.md § Constitution Check](../../../specs/035-renew-resolved-council-protocol/plan.md#constitution-check); coverage: the requirement and spec-delta tables in [tasks.md](../../../specs/035-renew-resolved-council-protocol/tasks.md#requirement-coverage) and [analysis.md](../../../specs/035-renew-resolved-council-protocol/analysis.md). Ticked in opensoft/openxFactory#1268; see the [allocation record](implementation-handoff.md#allocation-record-2026-10-08).

## 3. Release and successor evidence

- [ ] 3.1 Accept provider feature realization evidence; verify merged/green validators, corpus and regression inventory from exact candidate commits.
- [ ] 3.2 OWNER: allocate/publish the deprecation and removal releases through the governed process; retain the box and record native verification/tag/inventory evidence.
- [ ] 3.3 Accept linked producer/consumer realization and paired rehearsal evidence; verify compatible pins, independently scoped jobs and managing-factory deployment records.
- [ ] 3.4 OWNER: coordinate activation/rollback and record the exact matched configurations; retain the box and reject partial or hypothetical evidence.
- [ ] 3.5 Archive only after proposal exit evidence is complete; verify lifecycle/origin retention and linked feature/PR closure.
