# Reporting and Diagnostics Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements governing what a run SAYS —
finding messages, notices, skips with reasons, counts, resolution classes, and report
sections. A check whose output cannot be acted on is a check that will be ignored.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Finding messages

- [x] CHK1401 Does each rule's requirement state what its finding NAMES, rather than only that it fires? [Clarity, Spec §FR-006, §FR-009, §FR-036]
- [x] CHK1402 Is the duplicate finding required to name EVERY element of the tuple, so the reader can see which entry to change? [Clarity, Spec §FR-006]
- [x] CHK1403 Is the undeclared-reach finding required to name both the surface and the permission that reaches it? [Clarity, Spec §FR-009]
- [x] CHK1404 Is the misplacement finding required to name both the offending path and the declared placement? [Clarity, Spec §FR-036]
- [x] CHK1405 Is the closed-vocabulary refusal required to name the vocabulary AND the extension route? [Clarity, Spec §FR-007, §FR-034]
- [x] CHK1406 Is the per-unit-principal finding required to name the AVAILABLE principal, not merely to report a mismatch? [Clarity, Spec §FR-008]
- [x] CHK1407 Is the name-check finding required to name the token it matched, so the reader can see why it fired? [Clarity, Spec §FR-010]
- [x] CHK1408 Is the scope-excess finding required to name the act, its achieved scope, and the unit it exceeds? [Clarity, Spec §FR-010, plan §Cluster B]
- [x] CHK1409 Are the findings added by this pass each specified to name their subject? [Clarity, Spec §FR-008, §FR-009] — `undeclared-act-surface` names the act and the surface; `per-unit-principal-undeclared` names the surface; the drift-status refusal names the closed set.
- [x] CHK1410 Is a consistent finding format specified (a kebab code plus a message), anchored to a sibling validator? [Consistency, plan §Cluster B, research §Validator shape]
- [x] CHK1411 Is the named message required to survive a document that is ALSO schema-invalid? [Gap, tasks §2.2] — FIXED this pass: rules run to completion and raise their own codes; the expectations table pins the named one.
- [x] CHK1412 Is `oneOf` sub-error noise required to be filtered, so the reported message is the branch-specific one? [Clarity, research §Validator shape]

## Notices, skips and counts

- [x] CHK1413 Is the absence case required to print an EXPLICIT notice rather than exiting quietly? [Observability, Spec §FR-022, §SC-013]
- [x] CHK1414 Is a count of records checked required, so a run that checked nothing is distinguishable from a clean run? [Observability, Spec §US2-AS1]
- [x] CHK1415 Is a closing verdict line required? [Observability, plan §Cluster B, research §Validator shape]
- [x] CHK1416 Are the cross-domain family's skips required to carry a REASON, with both skip cases enumerated? [Observability, Spec §FR-023, §US5-AS3]
- [x] CHK1417 Is the expected skip-with-notice from the neighbouring credential validator declared as EXPECTED, so it is not read as a coverage gap? [Clarity, Spec §FR-020]
- [x] CHK1418 Is the difference between a skip, a pass, and a pass-with-notice stated clearly enough that a gate author can tell them apart? [Clarity, Spec §FR-022, §US3-AS4]

## Classification and reports

- [x] CHK1419 Is the resolution class specified per finding, with the rule for choosing it? [Clarity, Spec §FR-023]
- [x] CHK1420 Is the contested class required for a finding that contradicts a ratified capability, and is that requirement testable? [Measurability, Spec §US5-AS5, tasks §6.6]
- [x] CHK1421 Is the family's registration in the report id list required, so the family renders a section rather than reporting into a void? [Observability, tasks §6.4]
- [x] CHK1422 Is the pre-existing family that has no report section recorded, so the asymmetry is not mistaken for this feature's defect? [Honesty, research §Decision 6]
- [x] CHK1423 Is the drift record's shape sufficient for a reader to act (both values, both timestamps, the rule that produced it, the fragment it cites)? [Completeness, Spec §FR-035]
- [x] CHK1424 Is the drift record explicitly NOT claimed to be stored in a doc-health register that does not exist? [Honesty, Spec §FR-035]
- [x] CHK1425 Is the effective reach REPORTED rather than only computed, so a reader can see the union the ratified scenario describes? [Observability, Spec §FR-003, plan §Cluster B]
- [x] CHK1426 Is the unverified state visible in the output rather than only in the record? [Observability, Spec §FR-003, §US1-AS2]

## Diagnosability of the corpus itself

- [x] CHK1427 Are the five self-test failure modes required to be distinguishable, so a corpus defect names itself? [Observability, Spec §FR-018]
- [x] CHK1428 Is the negative header dialect required to state the requirement and the rule violated, so a human reviewer can adjudicate as the harness does? [Clarity, research §Examples layout]
- [x] CHK1429 Is the packaged README required to explain the family's layout to an instantiating domain? [Completeness, Spec §FR-019, tasks §3.1]
- [x] CHK1430 Is the consumption rule required to tell a consumer where fragments live and what the expected skip means? [Completeness, Spec §FR-020, tasks §9.1]

## Notes

- One item carried a defect (CHK1411), fixed jointly with the closedness and determinism
  checklists. The failure it prevents is subtle: every closed-vocabulary refusal in the
  feature is required to NAME its vocabulary and route, and a schema-first-return
  validator would have satisfied none of those requirements while appearing to refuse
  correctly.
