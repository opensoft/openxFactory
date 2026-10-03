# Governance and handoff tasks

Executable implementation tasks belong only to the one Speckit feature allocated after ratification. This list tracks packet preparation, gates and evidence acceptance.

## 1. Preparation

- [x] 1.1 Prepare proposal, complete spec delta, D1–D5 design, decision packet and provider handoff; verify packet strict validation and all links.
- [x] 1.2 Record old #517 disposition, current bundle and sibling/ownership inspection; verify no release reservation or inherited ratification.

## 2. Owner decision and feature handoff

- [ ] 2.1 OWNER: Brett ratifies this exact reviewed packet or supplies amendments; retain the box and record verbatim words, reviewed head and date beside it.
  - Recorded 2026-10-03: Brett Heap, verbatim **"ratify all three as disclosed"**, over reviewed head `b5cdf154208c1a5fd59e3936b483f37448ca85f9`; **RATIFIED AS DISCLOSED**, without amendments. See [ratification record](review/ratification-2026-10-03.md). Owner-act box intentionally retained.
- [ ] 2.2 After ratification, accept/claim provider ownership and allocate exactly one Speckit feature; verify its explicit backlink and constitution gate where applicable.

## 3. Release and successor evidence

Feature allocation note (2026-10-03): the sole Speckit feature is [`035-renew-resolved-council-protocol`](../../../specs/035-renew-resolved-council-protocol/spec.md). Created through the configured hook from clean current remote main using an isolated base copy, then linked to the owning repository with the unchanged ratified history. Specification and quality checklist exist. Task 2.2 remains open until the feature's constitution check and full task/scenario coverage are verified; no existing-lane acceptance or claim is fabricated.

Verification (2026-10-03): packet strict validation through the content-addressed OpenSpec 1.12.0 entrypoint exited 0. Header/citation, frozen-origin, local-link and feature-selection checks passed. The new packet has zero findings in the canonical status-validity and ratified-provenance scans. Whole-repository scans remain qualified: status-validity has 0 errors, ratified-provenance has 27 existing critical findings; every finding names a file byte-identical to `origin/main`. These are not clean whole-repository results. No runtime code, release, pin, credential, deployment or activation act is included in this preparation. Commits remain local until the required publication gates are run.

- [ ] 3.1 Accept provider feature realization evidence; verify merged/green validators, corpus and regression inventory from exact candidate commits.
- [ ] 3.2 OWNER: allocate/publish the deprecation and removal releases through the governed process; retain the box and record native verification/tag/inventory evidence.
- [ ] 3.3 Accept linked producer/consumer realization and paired rehearsal evidence; verify compatible pins, independently scoped jobs and managing-factory deployment records.
- [ ] 3.4 OWNER: coordinate activation/rollback and record the exact matched configurations; retain the box and reject partial or hypothetical evidence.
- [ ] 3.5 Archive only after proposal exit evidence is complete; verify lifecycle/origin retention and linked feature/PR closure.
