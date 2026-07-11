# Brokered-Call Feasibility Acceptance Traceability

Status: draft
Kind: register
Captured: 2026-07-10
Proposed by: qualify-avatar-brokered-call-feasibility

[`avatar-brokered-call-acceptance-map.yaml`](avatar-brokered-call-acceptance-map.yaml)
owns five `ABF-*` requirements and 19 scenarios. Automated evidence covers
harness safety, result validation, and redaction; live F0 evidence covers
provider ordering, retry, timing, revocation, and cleanup. Every provider
variance also maps to the affected contract-kernel `ACR-*` IDs through
`evidence/f0-interface-impact.yaml`.

No `ABF-*` evidence qualifies a provider profile for live use.
