# Tasks: Evidence authority and Speckit handoff

Status: ratified
Ratified: 2026-11-13 by Brett Heap. [Ratification record](review/ratification.md)

This is the governance/acceptance handoff. The sole executable implementation list remains [feature 043 tasks](../../../specs/043-private-connectivity-production/tasks.md); this packet creates no second implementation list.

## 1. Draft publication and owner review

- [x] 1.1 Publish this draft in PR #1310 and the README index, regenerate its corpus-ledger row with the sanctioned seed command and verify strict OpenSpec/sequencing validation.
- [x] 1.2 Obtain actual named-owner acceptance at T006 of the exact E files/commands, reviewed task/evidence contract and consumed C-08 custody/authentication decisions. Verify a cited ratification record and origin approval metadata; no generated text supplies acceptance.

## 2. Scoped realization handoff

- [ ] 2.1 Accept realization only through feature 043 T007–T010 after T006. Verify exact accepted source/test/CI scope, authenticated bootstrap import, required case/instance behavior, exact pin coverage and actual required-CI collection.
- [ ] 2.2 Verify merged, green realization and current evidence before promotion/archive. Distinguish E source readiness from other owner commissioning, supported neutral publication, target effects and Q1–Q5 acceptance.

T007 source checkpoint: the commissioned read-only verifier and 183 synthetic regressions are implemented. T008–T010 remain pending, so realization acceptance above stays open. No real bootstrap import, production manifest, pin registration, required feature CI collection or live-gate acceptance is claimed. PR #1310 remains draft.

Subsequent source checkpoint: T007–T009 are now complete (184 verifier tests, 27 inventory tests and 172 affected pin/sentinel tests pass). The narrow production members are FUTURE with no invented evidence population. T010 remains pending the [draft exact bootstrap-custody refinement](../amend-private-connectivity-evidence-bootstrap/proposal.md), actual custodian authentication and required feature CI. Governance acceptance 2.1/2.2 above stays open; this checkpoint does not alter the earlier owner decision or approve the proposed additional paths.
