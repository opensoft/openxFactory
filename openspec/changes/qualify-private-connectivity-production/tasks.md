# Tasks: Governance and Speckit handoff

Status: ratified
Ratified: 2026-11-12 by Brett Heap. [Ratification record](review/ratification-2026-11-12.md)

This is the governance and acceptance handoff. The sole executable implementation
task list belongs to one new coordinating Speckit feature. Allocate its number
through the repository's feature hook when commissioned; no new Speckit feature
or runtime task list is created by this proposal. Feature 040 stays completed.

Coordinating successor: [043-private-connectivity-production](../../../specs/043-private-connectivity-production/spec.md), created at Brett Heap's request on 2026-11-13. Its specification, [implementation plan](../../../specs/043-private-connectivity-production/plan.md) and sole executable [task list](../../../specs/043-private-connectivity-production/tasks.md) cover all three delivery tracks, all four offering paths, owner commissioning and Q0–Q5 dependencies/validation. The complete artifact handoff is verified in the feature's [validation checklist](../../../specs/043-private-connectivity-production/checklists/requirements.md), completing task 2.1 only. Speckit analysis, T001–T006 bootstrap/exact E acceptance and T007–T009 source verification/inventory/registration are complete. Task 2.2, T010–T068 and all live gates remain open. The [draft bootstrap-custody refinement](../amend-private-connectivity-evidence-bootstrap/proposal.md) records the exact T010 source-only gap for owner review. Full program Q0 still requires the remaining owner scopes and consumed decisions; PR #1310 remains draft.

## 1. Review and publication

- [x] 1.1 Review and ratify the production qualification policy and owner boundaries. Verify an explicit ratification record identifying this packet and distinguishing policy acceptance from implementation, staging, canary, commercial release and expansion authority.
- [x] 1.2 Publish draft PR #1309 in the repository index and regenerate the corpus ledger with the sanctioned seed command using #1309. Verify the strict OpenSpec check, sequencing sweep and ledger diff; the assigned PR and generated row are recorded in review/validation-2026-11-12.md.

## 2. Implementation handoff

- [x] 2.1 Commission exactly one new coordinating Speckit feature, linking this change, the immutable 040 lab baseline and owner governance. Verify the feature's identity and spec/plan/tasks trace all three delivery tracks, all four offering paths and Q0–Q5; executable owner work is represented there once.
- [ ] 2.2 Establish Q0 decisions and owner-scoped realization authority before implementation. Verify concrete repository/code/CI/schema scope, supported release and contract publication needs, target/platform/integration decisions, numeric operating limits, custody, named roles and verification commands; unresolved required values block their consuming gate.

## 3. Acceptance and release governance

- [ ] 3.1 Review Q1–Q2 staging acceptance when its implementation evidence is available. Verify target-appropriate execution authority, including accepted requests for managed targets and grants where required, exact candidate/profile pins, actual platform/integration observations, all four offering paths, operating measurements and reviewed closure of failures; fixtures or lab observations cannot replace deployed evidence.
- [ ] 3.2 Record Q3–Q4 canary decisions separately from staging and policy approval. Verify explicit customer/site/domain/region/data/capacity/spend/time bounds, execution and rollback authority, actual observation and current owner acceptance before a commercial or expansion decision.
- [ ] 3.3 Record each Q5 offer or expansion wave against accepted canary evidence and exact eligible profiles. Verify bounded scope, current approvals and change-impact requalification; retain the stop/remediate/rerun/resume chain and preserve unrelated authorized access.
- [ ] 3.4 Close the commissioned realization and handoff before archive. Verify its Speckit work and PRs have landed and any required canonical promotion follows the existing governed process; archiving supplies no missing operational or commercial permission.
