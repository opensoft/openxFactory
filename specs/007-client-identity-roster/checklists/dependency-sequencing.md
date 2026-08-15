# Dependency and Sequencing Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements governing ORDER — phase
dependencies, hard gates, verification timing, parallelism claims, and the external
preconditions without which a later measurement cannot be made at all.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Preconditions and gates

- [x] CHK1501 Are the preconditions that must hold before work begins separated from the work itself? [Clarity, tasks §Phase 0]
- [x] CHK1502 Does each precondition state exactly what it gates, rather than being "advisory"? [Clarity, tasks §Phase 0 checkpoint]
- [x] CHK1503 Is the hard gate on the packaged-examples phase stated on every task in that phase, so it cannot be entered sideways? [Fail-closed, tasks §Phase 3 preamble] — the gate FIRED and is RULED (2026-08-15): 0.1 failed, the escalation ran, and Decision C (Brett) satisfies the gate by relocating the case rather than by supplying a citation. The Phase 3 preamble now states the ruled basis and forbids reintroducing a packaged multi-surface reader, so the phase still cannot be entered sideways.
- [x] CHK1504 Is the baseline precondition required BEFORE the first edit to any modified capability, with the reason it cannot be captured later? [Dependency, tasks §0.3]
- [x] CHK1505 Is the estate sweep required before the edit whose safety it establishes? [Dependency, tasks §0.2, §8.2]
- [x] CHK1506 Are the external checkouts the later measurements need established as a precondition rather than discovered at measurement time? [Dependency, tasks §0.3]
- [x] CHK1507 Is each precondition's failure branch an escalation rather than a workaround? [Fail-closed, tasks §0.1, §0.2, §0.3]

## Phase dependencies

- [x] CHK1508 Does every phase state what it depends on and what it blocks? [Completeness, tasks §Phase headers]
- [x] CHK1509 Is the one deliberate departure from cluster order explained by a real dependency (positives live inside packaged fragments)? [Clarity, tasks §Phase order] — RE-CHECKED after Decision C: the departure still holds for THREE of the four positives, which do live inside packaged fragments. The fourth no longer does — 4.9's synthetic fixture lives in Cluster C's own `tests/` tree and therefore depends on Phases 1-2 only, not on Phase 3. That is recorded on the Phase 4 header as an explicit exception, so the departure's rationale is not overstated.
- [x] CHK1510 Is the distinction between a task's WORK and its VERIFICATION landing in different phases stated, so an apparent cycle is not re-raised? [Clarity, tasks §Format]
- [x] CHK1511 Is the phase that has no build dependency but names an artifact fixed elsewhere explained rather than left ambiguous? [Clarity, tasks §Phase 7 header]
- [x] CHK1512 Does the registration phase depend on every phase whose CONTENT it digests? [Dependency, tasks §Phase 9 header]
- [x] CHK1513 Is the ordering WITHIN the registration phase correct with respect to the release surface? [Dependency, tasks §9.4] — FIXED: `contracts/CHANGELOG.md` and `contracts/README.md` are release-surface members, so the inventory must be generated after 9.1, 9.2 AND 9.3; the pre-fix text declared only `9.1 → 9.4 → 9.6` sequential and marked 9.2/9.3 `[P]`, which permitted generating over files still being edited.
- [x] CHK1514 Does the final phase depend on everything, so the green bar cannot be claimed early? [Dependency, tasks §Phase 10 header]
- [x] CHK1515 Are the phases that may run in parallel identified by the files they touch rather than by convenience? [Clarity, tasks §Parallel opportunities]
- [x] CHK1516 Does every `[P]` marker mean "different files, no dependency", and is that definition stated? [Clarity, tasks §Notes]
- [x] CHK1517 Is any `[P]` marker used where a shared registry or a release-surface file makes concurrency unsafe? [Consistency, tasks §Parallel opportunities] — FIXED with CHK1513: the 9.2/9.3 pair is now explicitly parallel with each other only.
- [x] CHK1518 Is the in-module parallelism claim qualified (two finding classes in one module are parallel only if authored as separate functions first)? [Clarity, tasks §Parallel opportunities]

## Verification timing

- [x] CHK1519 Are tasks whose verification runs later marked as such, with the task NOT checked off until its verification has run? [Clarity, tasks §Format]
- [x] CHK1520 Is the self-test task's dependency on corpora authored in later phases stated where the task lives? [Clarity, tasks §2.2]
- [x] CHK1521 Is the schema field-list assertion's home (a module created in a later phase) stated where the field list is authored? [Clarity, tasks §1.5]
- [x] CHK1522 Is the cross-corpus assertion assigned to exactly one module, with the rejected alternative named? [Clarity, tasks §6.7]
- [x] CHK1523 Is the fixture-conformance requirement stated in the task that AUTHORS the fixtures, not only in the task that reads them? [Dependency, tasks §6.5, §6.7]

## Blocking and stop conditions

- [x] CHK1524 Are the STOP conditions stated with what they forbid as well as what they require? [Fail-closed, tasks §The two STOP conditions]
- [x] CHK1525 Is the killed-flaw STOP condition tied to the acceptance test the seed handoff states in the same terms? [Traceability, tasks §10.5, seed handoff §Two flaws]
- [x] CHK1526 Is the escalation path for the provider-fact precondition explicit about the two things that must NOT be done (synthesize; soften)? [Fail-closed, tasks §0.1, research §Decision 8]
- [x] CHK1527 Is the consequence of skipping the baseline stated (a requirement becomes unmeasurable, not merely unrecorded)? [Honesty, tasks §Phase 0 checkpoint]
- [x] CHK1528 Are commits required to use explicit pathspecs, given the shared checkout hazard? [Fail-closed, tasks §Notes]

## Notes

- Two items carried the same defect (CHK1513, CHK1517) — a release-surface ordering
  hazard that would have surfaced as a confusing release-verifier failure over files
  the same commit had just edited. Fixed in tasks §9.4, the parallel-opportunities note,
  and plan §Cluster E.
