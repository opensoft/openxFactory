# Tasks: add-deployment-handoff-boundary

Source: the single staged doc in `supporting-docs/` (moved at the proposal
gate; origin recorded in `supporting-docs/README.md`). All seven clarifying
resolutions (2026-07-24) are carried as design decisions 2–9; decision 1
confirms the capability home from the staging lean. Shared checkout:
explicit paths, `git status -sb` before every commit.

## 1. Capability And Delta

- [ ] 1.1 Verify the ADDED capability requirements carry all seven locked resolutions and the layered enforcement design without divergence; any divergence goes back through a decision note, not a silent edit.
- [ ] 1.2 Verify the release-realization MODIFIED delta retains every promoted scenario verbatim and that no active ratified change modifies the same requirement (add-proposal-origin-contract's delta is a disjoint ADDED requirement).
- [ ] 1.3 Run strict OpenSpec validation for the change and the full tree.

## 2. Bookkeeping And Provenance

- [ ] 2.1 Move the staged topic doc into `supporting-docs/` with an origin README; retire the staging INDEX row and detail section; add the ideation README promoted-list pointer and the repository README OpenSpec Records entry in the same commit.
- [ ] 2.2 Record the coordination note with `client-credential-escrow-registry`: break-glass custody, checkout realization and test, and the policy window are owned there and consumed here.
- [ ] 2.3 Record the DTN-017 `subject-establishment` linkage: its codexFactory second consumer produces handoff-shaped realization artifacts on this seam.

## 3. Downstream Handoff

- [ ] 3.1 Produce the OpsxFactory successor-change handoff packet: QA requirements/validation profile of `deployment.yaml` (approval calibration leaning recorded), subject-registry lookup at grant issuance, evidence-correlation audit job over stamped changes, ACR namespace scope map coordinated with the worker-host-app bench pipeline, and correlation-stamp conventions (commit trailers, deployment annotations, endpoint metadata).
- [ ] 3.2 Produce the codexFactory successor-change handoff packet: the release exit step emits the `client_infrastructure_request` draft (produce → hand off) and any direct deploy path is removed; release-realization evidence carries the handoff correlation identifier.
- [ ] 3.3 Record the preview-environment threshold leaning (exposure or persistence beyond the producing job ⇒ subject) for decision in the OpsxFactory realization.

## 4. Ratification And Archive

- [x] 4.1 Obtain ratification approval and stamp the proposal front matter (`Status: ratified`, `Ratified by:`) — ratified by Brett 2026-07-29.
- [ ] 4.2 At archive, package `supporting-docs/` as a deterministic bundle per the proposal-support archive gate; the change archives when its artifacts land (code_surface none).
- [ ] 4.3 Verify the topic-exit conditions — one real release crossing the rail end-to-end and a clean or dispositioned correlation-audit run — are tracked on the OpsxFactory and codexFactory successor changes, not on this change.
