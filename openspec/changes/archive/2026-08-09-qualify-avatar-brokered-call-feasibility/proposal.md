code_surface: openxFactory
target_release: implemented
Status: ratified
Ratified: 2026-08-09 — record: the archive act, commit `e34dce6` "Archive F0 feasibility: the gate follows its pin into the packaged archive (#30)", which applied this change's spec delta into `openspec/specs/avatar-brokered-call-feasibility/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The archive act was taken on Brett's word, named in the commit body: "Option C of issue #30, accepted by Brett 2026-08-09, superseding the 2026-08-04 hold". That acceptance lifted an archive HOLD rather than ratifying the change, so it is recorded here as the word the archive act was taken on, not as the ratification itself. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

> **Archive hold (ruled by Brett, 2026-08-04): kept active by design.** The
> avatar-client kernel's `contracts/avatar-client/interface-lock.yaml`
> `f0_evidence_pin.f0_change_path` resolves this change's ACTIVE path, and that
> file is digest-pinned in the `contract-v1.7` bundle — archiving would break
> the fail-closed F0 gate or force a contract re-cut. Do NOT archive this
> change in a housekeeping sweep; archive it only inside a contract re-cut
> that repoints `f0_change_path` (and its schema digests) to the archive path.

## Why

The avatar protocol assumes that an OpenAI broker can create a WebRTC call,
attach and verify sideband control before releasing the SDP answer, keep the
client from applying that answer until xFactory control authorizes media, and
terminate the provider leg within the required bound. Those are
empirical provider behaviors, not facts that schemas or mocks can prove.

This change isolates that uncertainty in a reproducible, tenant-data-free F0
experiment. It may run in parallel with contract, runtime, and UI work. Its
result gates contract publication but does not mutate canonical contracts or
qualify a model for internal-live use.

## What Changes

- Add a disposable harness under `experiments/avatar-brokered-call/` using a
  lab project key, generated audio, a pinned candidate profile, deterministic
  trial IDs, monotonic timing, and redacted structured output.
- Execute baseline, delayed-sideband, sideband-failure, readiness-timeout,
  exact-retry, changed-retry, revocation, and provider-hangup trials from the
  registered protocol.
- Verify sideband-before-answer ordering, authoritative media authorization,
  the 3,000-millisecond default and 5,000-millisecond hard readiness ceiling,
  no duplicate provider call for an exact retry, no answer disclosure for a
  changed retry, and provider termination within five seconds.
- Write schema-valid `evidence/f0-results.json` and a human-readable companion
  with overall status `PASS`, `FAIL`, or `INCONCLUSIVE`.
- Write `evidence/f0-interface-impact.yaml` for every observed mismatch between
  the provider and `avatar-client-parallel-v1`. The contract-kernel change owns
  any resulting neutral correction.
- Keep all credentials, SDP, raw provider payloads, audio, transcripts, and
  high-cardinality identifiers out of committed evidence.
- Explicitly prohibit F0 `PASS` from enabling internal-live or production use.

## Capabilities

### New Capabilities

- `avatar-brokered-call-feasibility`: Defines the safe lab protocol, required
  trial matrix, timing assertions, evidence classification, variance handoff,
  and non-qualification boundary for brokered realtime-call feasibility.

## Impact

- **openxFactory:** `experiments/avatar-brokered-call/` plus evidence owned by
  this change.
- **Contract kernel:** consumes the result and variance report at publication;
  this change cannot edit `contracts/avatar-client/` or release metadata.
- **Reference runtime and UI:** may continue in parallel against the frozen
  baseline; only accepted interface variances can invalidate affected tests.
- **Provider operations:** one bounded lab workload using generated input and
  no tenant data; no deployment or standing service.
- **Compatibility:** no existing runtime or contract consumer is changed.
