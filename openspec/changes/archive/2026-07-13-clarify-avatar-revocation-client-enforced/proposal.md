code_surface: openxFactory
target_release: none
Status: ratified
Ratified: 2026-07-13 — record: the archive act, commit `44f523b` "Archive 3 realized avatar changes (kernel, revocation clarify, reference runtime)", which applied this change's spec delta into `openspec/specs/avatar-client-runtime/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. One archive act closed three avatar changes, "promoting their capability specs (avatar-client-runtime, avatar-reference-runtime) into openspec/specs/". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

# Clarify Avatar Revocation as Client-Enforced

## Why

The F0 brokered-call feasibility re-run (2026-07-12, dedicated lab project) measured that the
OpenAI Realtime provider gives no positive, in-bound (≤5 s) confirmation of call termination
after an accepted hangup: the control socket drops with an abnormal close (1006) at ~2.2 s and
the earliest authoritative "call gone" (REST 404) settles at ~8.1 s. Read as "provider-confirmed
termination within 5 s," the F0-D revocation slice fails. Evidence:
`qualify-avatar-brokered-call-feasibility/evidence/f0d-revocation-rerun-notes-2026-07-12.md`.

The ACR-005 revocation guarantee already lives where it is enforceable — the reference runtime
deterministically revokes the lease and stops the client's own media within an injected 5 s
bound (`ARR-005-S05`), and the `avatar-client-runtime` requirement already states that loss of
control "stop[s] capture and playback" and closes the media leg. What is missing is an explicit
statement that this **client-side** stop is the ≤5 s guarantee and that provider-side
termination confirmation is best-effort / eventually-consistent, not the gate. F0-D's FAIL
under the provider-confirmation reading does not contradict the runtime; it confirms the
contract must not delegate the kill guarantee to provider-side confirmation timing.

## What Changes

- Clarify ACR-005 (`avatar-client-runtime`): on a revocation trigger (explicit revoke, control
  loss, or lease expiry) the client SHALL disable governed commands and confirmations, stop
  capture and playback, close the media leg, and issue the provider revocation request within
  5,000 ms of the trigger — this client-side stop is the revocation guarantee. Provider-side
  authoritative termination confirmation MAY lag and MUST NOT be the sole evidence of revocation.
- Disposition of the F0 interface variance: F0-D is re-measured to gate on the accepted provider
  revocation request within the bound; the provider-side settle verdict/time is recorded
  informationally, not gated. (F0 realization is tracked in
  `qualify-avatar-brokered-call-feasibility`, not this change.)

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `avatar-client-runtime`: the leased-control revocation requirement gains an explicit
  client-enforced ≤5 s stop and de-gates provider-side termination confirmation.
