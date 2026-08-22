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

## Bookkeeping annotation — archived with all 4 boxes open (2026-08-22, `archive-register-rulings`)

No box is ticked here and no task text above is altered. This section records
what the archive evidence actually shows, because this ledger archived with
every box open and no annotation saying why — the anomaly enumerated as C6 in
`docs/archive-record-discrepancies.md`, ruled on 2026-08-22 by Brett
(in-session, multiple-choice round) to be annotated rather than force-ticked.

**This one differs from its three 2026-07-13 siblings, and the difference is
the point.** C6 groups four changes whose ledgers and README rows disagree
about realization. This change's row makes **no realization claim at all** —
it reads only "ACR-005 disposition: revocation is client-enforced within the
5 s bound; archived 2026-07-13" — and its proposal declares
`target_release: none`. There is therefore nothing here for the ledger to
disagree with, and nothing in this note asserts that this change was
"realized". It is a contract clarification, and the honest question is only
whether its clarified text reached the canon.

**It did.** The MODIFIED `avatar-client-runtime` requirement §1.1 carries is in
the promoted spec at `openspec/specs/avatar-client-runtime/spec.md`:
"Revocation SHALL be client-enforced: on any revocation trigger — an explicit
revoke, control loss, or lease expiry — the client SHALL disable governed
commands and pending confirmations, stop capture and playback, close the media
leg, and issue the provider revocation request within 5,000 milliseconds of the
trigger". The ACR-005 disposition §1.2 records is carried in released
artifacts — `contracts/avatar-client/kernel-handoff.yaml` reads
`revocation_model: client_enforced   # ACR-005; provider-side settle
informational`. So §1's substance landed even though neither box is ticked.

**Two of the four boxes were never this change's work.** §2 is headed
"Downstream realization (tracked in sibling changes; not gated by this change)",
so 2.1 and 2.2 are sibling-owned by the ledger's own declaration — the same
shape as `add-roster-device-admission-surface` 6.1, where an unticked box means
"owned elsewhere" and ticking it would claim work this change never did. 2.2's
subject is confirmable: `tests/avatar_runtime/test_consent_revocation.py`
exercises the 5 s bound against `ARR-005-S05`, mapped in that suite's
`conformance/scenario-test-map.yaml`.

One stale pointer worth flagging rather than fixing: §1.2 cites an evidence
note under `openspec/changes/qualify-avatar-brokered-call-feasibility/`, a path
that stopped resolving when that sibling archived on 2026-08-09. The file now
lives under
`openspec/changes/archive/2026-08-09-qualify-avatar-brokered-call-feasibility/evidence/`.
The task text is left as written; this note is the correction.

This is also the thinnest record of the four: the directory holds only
`proposal.md`, `tasks.md`, `specs/` and `.openspec.yaml` — no
`supporting-docs/`, no `evidence/`, no `review/`.
