# Tasks: Clarify Avatar Revocation as Client-Enforced

## 1. Contract clarification (this change)

- [ ] 1.1 Ratify the MODIFIED `avatar-client-runtime` requirement clarifying client-enforced
  revocation (client-side media stop + accepted provider revocation request within 5,000 ms)
  and de-gating provider-side termination confirmation.
- [ ] 1.2 Record the ACR-005 disposition against the F0 variance evidence note
  (`qualify-avatar-brokered-call-feasibility/evidence/f0d-revocation-rerun-notes-2026-07-12.md`).

## 2. Downstream realization (tracked in sibling changes; not gated by this change)

- [ ] 2.1 F0 (`qualify-avatar-brokered-call-feasibility`): redefine F0-D to gate on the accepted
  provider revocation request within the bound; record the provider-side settle verdict/time
  informationally; retire the `hangup_to_terminal_ms` gate in favor of a request-accepted bound.
- [ ] 2.2 Runtime (`implement-avatar-reference-runtime`): confirm `ARR-005-S05` already satisfies
  the clarified requirement (no change expected); record the conformance note.
