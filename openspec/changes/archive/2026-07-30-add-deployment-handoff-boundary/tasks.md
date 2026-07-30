# Tasks: add-deployment-handoff-boundary

Realized 2026-07-30. Verification (1.1–1.3): all seven 2026-07-24
resolutions and the layered enforcement design map onto the ADDED
requirements without divergence (all-actor scope → Req 1; the
request-record crossing → Req 2; credentials-primary + grant-issuance
gate + retroactive break-glass → Req 3; structural channels + merge
authority → Req 4; correlation stamping + join audit → Req 5; standing
bench requests → Req 6; phased-never-gapped → Req 7; codex-sole-first-
consumer stays design/handoff material, correctly not a neutral
requirement); the release-realization MODIFIED delta retains both
promoted scenarios VERBATIM (machine-diffed), fully contains the
promoted requirement body, and adds only the correlation sentence +
scenario; add-proposal-origin-contract's release-realization delta is a
disjoint ADDED requirement ("Origin retention at archive") — no
conflict; strict validation green for the change and the tree (57/57).
Bookkeeping (2.1–2.3): the proposal-gate move is verified complete
(supporting-docs/ with origin README recording the 2026-07-28 move,
staging INDEX row + detail retired, ideation README promoted-list
pointer and repository README OpenSpec entry present); the escrow
coordination note is recorded IN the client-credential-escrow-registry
staging detail (custody/checkout-test/policy-window owned there,
consumed here; the phased-adoption milestone gates on the TESTED
checkout); the DTN-017 linkage is recorded in the candidate register
(the codexFactory second consumer's handoff-shaped artifacts cross on
the now-RATIFIED seam). Downstream (3.1–3.3):
[docs/deployment-handoff-realization-handoff.md](../../../docs/deployment-handoff-realization-handoff.md)
carries both successor packets — OpsxFactory (QA profile with the
approval-calibration leaning, subject-registry lookup at grant issuance,
evidence-correlation audit, ACR namespace scope map coordinated with the
worker-host-app bench pipeline, correlation-stamp conventions) and
codexFactory (release exit emits the request draft, no direct deploy
path, realization evidence carries the correlation identifier, DTN-017
alignment) — plus the preview-environment threshold leaning (exposure or
persistence beyond the producing job ⇒ subject) recorded for the
OpsxFactory decision, and the topic-exit conditions (one real
end-to-end crossing; a clean or dispositioned correlation-audit run)
stated as the successors' acceptance evidence, tracked there and never
here (4.3).

## 1. Capability And Delta

- [x] 1.1 Verify the ADDED capability requirements carry all seven locked resolutions and the layered enforcement design without divergence; any divergence goes back through a decision note, not a silent edit.
- [x] 1.2 Verify the release-realization MODIFIED delta retains every promoted scenario verbatim and that no active ratified change modifies the same requirement (add-proposal-origin-contract's delta is a disjoint ADDED requirement).
- [x] 1.3 Run strict OpenSpec validation for the change and the full tree.

## 2. Bookkeeping And Provenance

- [x] 2.1 Move the staged topic doc into `supporting-docs/` with an origin README; retire the staging INDEX row and detail section; add the ideation README promoted-list pointer and the repository README OpenSpec Records entry in the same commit.
- [x] 2.2 Record the coordination note with `client-credential-escrow-registry`: break-glass custody, checkout realization and test, and the policy window are owned there and consumed here.
- [x] 2.3 Record the DTN-017 `subject-establishment` linkage: its codexFactory second consumer produces handoff-shaped realization artifacts on this seam.

## 3. Downstream Handoff

- [x] 3.1 Produce the OpsxFactory successor-change handoff packet: QA requirements/validation profile of `deployment.yaml` (approval calibration leaning recorded), subject-registry lookup at grant issuance, evidence-correlation audit job over stamped changes, ACR namespace scope map coordinated with the worker-host-app bench pipeline, and correlation-stamp conventions (commit trailers, deployment annotations, endpoint metadata).
- [x] 3.2 Produce the codexFactory successor-change handoff packet: the release exit step emits the `client_infrastructure_request` draft (produce → hand off) and any direct deploy path is removed; release-realization evidence carries the handoff correlation identifier.
- [x] 3.3 Record the preview-environment threshold leaning (exposure or persistence beyond the producing job ⇒ subject) for decision in the OpsxFactory realization.

## 4. Ratification And Archive

- [x] 4.1 Obtain ratification approval and stamp the proposal front matter (`Status: ratified`, `Ratified by:`) — ratified by Brett 2026-07-29.
- [x] 4.2 At archive, package `supporting-docs/` as a deterministic bundle per the proposal-support archive gate; the change archives when its artifacts land (code_surface none).
- [x] 4.3 Verify the topic-exit conditions — one real release crossing the rail end-to-end and a clean or dispositioned correlation-audit run — are tracked on the OpsxFactory and codexFactory successor changes, not on this change.
