# Avatar Client Contract-Kernel Acceptance Traceability

Status: draft
Kind: register
Captured: 2026-07-10
Proposed by: define-avatar-client-contract-kernel

The machine-readable
[`avatar-client-acceptance-map.yaml`](avatar-client-acceptance-map.yaml) assigns
stable IDs to the 17 requirements and 72 scenarios owned by this change across
`avatar-client-runtime`, `repo-boundary-governance`, and
`shared-contract-ownership`. The original 25-requirement program map was split:
`AFU-*` entries now belong to `align-avatar-first-ui-standard`, while F0 and the
reference runtime have new `ABF-*` and `ARR-*` registers.

## Evidence Rules

- Requirement prefixes are `ACR`, `RBG`, and `SCO`.
- Scenario IDs append `-Snn` in specification order.
- Planned automated evidence uses `TEST-<scenario-id>`.
- F0 evidence is owned by `qualify-avatar-brokered-call-feasibility` and maps
  observations back to affected `ACR-*` IDs.
- Runtime and UI siblings own implementation evidence and must pin the released
  kernel; their evidence cannot complete a kernel task.
- A kernel task completes only when every current-change scenario has passing
  contract/fixture/manual evidence and every successor-owned behavior retains a
  named owner and fail-closed default.

Task 3.2 realizes this map under `contracts/avatar-client/` and makes
`scripts/validate-avatar-client.py` compare it to the OpenSpec deltas. Missing,
duplicate, renamed, or evidence-free requirements and scenarios fail release.
