# Analysis: 032-govern-archived-record-edits

**Date**: 2026-09-08 | **Artifacts**: `spec.md`, `plan.md`, `tasks.md`, plus the
eight checklists under `checklists/` (331 items, every item carrying a
traceability reference).

The loop ran to ZERO findings in two rounds. Round 1's inputs were the four
checklist lanes' `[Gap]`/`[Conflict]`/`[Ambiguity]` items and the orchestrator's
own coverage map; round 2 re-ran every detection pass against the amended
artifacts.

## Round 1 — 18 findings, all resolved

| ID | Category | Severity | Location | Finding | Resolution |
| --- | --- | --- | --- | --- | --- |
| F1 | Inconsistency | HIGH | spec FR-009 vs FR-017 | "No ratified requirement text may be reworded" read as forbidding FR-017's amendment of three ratified `tasks.md` sentences. | FR-009 rescoped to REQUIREMENT AND SCENARIO TEXT in the delta plus archived bytes, and names the boundary explicitly. |
| F2 | Coverage | HIGH | spec FR-016 | No task carried "write no checker, edit no pin, repair no pin". | New T032 checks the diff names nothing under `scripts/`, `.github/`, `contracts/`, `tests/`. |
| F3 | Coverage | HIGH | spec FR-019 | No task committed the Speckit tree. | New T033; FR-019 enumerates the files. |
| F4 | Underspecification | HIGH | spec § Requirements | Only the pass path of the gates was specified; nothing said what a FAILING gate obliges. | New FR-020 (a failing gate is a blocker) plus a Failure-handling block in `tasks.md`. |
| F5 | Inconsistency | MEDIUM | tasks T003 | Cross-referenced T028 as the frozen-set re-check; T028 is the `proposal.md` note. | Corrected to T030 (the SC-007 path-set check). |
| F6 | Ambiguity | MEDIUM | spec FR-002, tasks T005 | "The edited file's own lifecycle-header block" could be read as governing where THIS bullet sits. | FR-002 and T005 state that it describes a future archived-record edit's note, and that the bullet is body prose. |
| F7 | Underspecification | MEDIUM | spec § Assumptions | Nothing said whether the ratified archived-record rule binds this feature's edits to the packet's own ACTIVE files. | New FR-022: it does not; the discipline is followed anyway and said so. |
| F8 | Underspecification | MEDIUM | spec § Architect rulings | The three flagged vetoes had no reversal path. | Each is now a single named reversal act, forward-only under FR-021. |
| F9 | Underspecification | MEDIUM | spec, tasks | No rollback story for a defective bullet, a bad tick, or an invalidated evidence entry. | New FR-021 (forward-only corrections; superseded evidence struck, never deleted) + T029. |
| F10 | Ambiguity | MEDIUM | tasks T029 | Interim vs final-head results had no disposition rule. | T029 strikes a superseded interim result with a dated line naming the replacing head. |
| F11 | Underspecification | MEDIUM | spec § Success Criteria | Nothing distinguished LOCAL gate evidence from CI. | New FR-023; T011 records it in the evidence header; CI named in § Out of scope. |
| F12 | Ambiguity | LOW | spec FR-006 | The line between citing and paraphrasing a record was unstated. | FR-006: a note may restate what a record states and may not attribute words. |
| F13 | Method defect | MEDIUM | tasks T016, quickstart § 3 | The doc-health diff recipe would have used `--previous-report`, which REFUSES on a repo-identity mismatch (the stamp is the checkout slug). | Two independent `--report-out` runs and a normalized diff, with the refusal named. |
| F14 | Measurability | LOW | spec SC-002 | A dispositioned-exception count that moved DOWN was not treated as a difference. | SC-002 compares the count with the ratified baseline in both directions. |
| F15 | Completeness | LOW | spec FR-015 | The prohibition list did not name `gh`. | FR-015 names `gh` in every form, and lists the lane's acts. |
| F16 | Underspecification | LOW | spec FR-007 | Task 3.1's "re-checked once both heads settle" has no actor and no trigger in the packet. | FR-007: the note records the re-check as still OWED and invents neither actor nor trigger. |
| F17 | Coverage | LOW | spec § Out of scope | A README Records-row union re-derivation (Rule 7) was unassigned. | Named as the lane's act at landing. |
| F18 | Coverage | MEDIUM | spec SC-006 | No task counted the 28 boxes. | T032 counts them: every box ticked with a dated note or unticked with a dated NOT-OWED line. |

**One finding came from a measurement rather than a reading, and it changed a
ruling's implementation.** F-A (folded into F5's fix and FR-010a): the architect's
Q10 answer places the realization note in `proposal.md`'s "front-matter area".
Measured, `parse_status` finds `Status: ratified` at REAL-LINE INDEX 8 of a
15-line header window, with the whole folded `code_surface:` scalar counting as
ONE real line. Anything inserted above `Status:` moves that header toward the
window's edge, and editing the folded scalar would change a ratified front-matter
value the archive gate reads. The note therefore sits immediately AFTER the
`Lane:` line and QUOTES the enumeration sentence it corrects. The ruling stands;
its anchor is now measured rather than assumed.

## Round 2 — zero findings

- **A. Duplication**: no near-duplicate requirement. FR-009/FR-017 were the
  candidate pair and are now disjoint by scope.
- **B. Ambiguity**: no unresolved placeholder, no `NEEDS CLARIFICATION` marker,
  no vague adjective without a measure. The phrases the checklists flagged
  ("front-matter area", "minimal prose", "verifiably DONE", "beside the header
  rules") each now carry an anchor, a measurement or an enumeration.
- **C. Underspecification**: every FR names an object and an outcome; every user
  story carries acceptance scenarios; every task names its paths.
- **D. Constitution alignment**: Principles I–VII checked in `plan.md`'s
  Constitution Check table; Principle V (validation gates, NON-NEGOTIABLE) is
  carried by FR-011, FR-020 and Phase 6.
- **E. Coverage**: 24 functional requirements (FR-001..FR-023 plus FR-010a) and
  8 success criteria, each mapped to at least one task; 34 tasks, each mapped to
  at least one requirement. FR-020..FR-023 are cross-cutting and are carried by
  the Failure-handling block plus T011, T016, T029 by name.
- **F. Inconsistency**: terminology is consistent across the three artifacts —
  "the packet's `tasks.md`" versus "the feature's `tasks.md`" is disambiguated in
  § *Path conventions*; the S1–S7 sequence maps to T-numbers in `plan.md`; task
  ordering matches the dependency block (US1 → US3 → US2, because a tick may not
  land ahead of its evidence).

**Metrics**: requirements 24 + 8 SC; tasks 34; requirement coverage 100%;
unmapped tasks 0; ambiguity count 0; duplication count 0; CRITICAL issues 0.

## Next action

Proceed to implementation (Phase 3 onward) after the architect's STOP (B)
clearance. The per-scenario refutation panel is the architect's to convene.
