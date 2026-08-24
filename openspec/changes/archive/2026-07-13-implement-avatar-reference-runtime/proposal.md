code_surface: openxFactory
target_release: implemented
Status: ratified
Ratified: 2026-07-13 — record: the archive act, commit `44f523b` "Archive 3 realized avatar changes (kernel, revocation clarify, reference runtime)", which applied this change's spec delta into `openspec/specs/avatar-reference-runtime/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. One archive act closed three avatar changes, "promoting their capability specs (avatar-client-runtime, avatar-reference-runtime) into openspec/specs/". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

Schemas alone cannot prove idempotency, lease fencing, event ordering,
revocation, snapshot recovery, or fail-closed authority behavior. A small,
deterministic implementation is needed to exercise the AVC protocol without
creating a production service or coupling contract review to a live provider.

This change isolates that implementation under exclusive runtime and test
paths. It can proceed in parallel against `avatar-client-parallel-v1`, then
must prove conformance against the exact released kernel before realization.

## What Changes

- Create non-deployable Python reference modules under
  `xfactory/avatar_runtime/` for broker preflight, media attempts, AVC-02
  outcomes, ephemeral grant retry, control leases, media authorization,
  commands, one event log, snapshots, authority ports, consent revocation,
  usage, and kill switches.
- Use injected deterministic clocks, ID sources, provider ports, policy ports,
  and consent-authority ports. No test depends on wall time, randomness, a
  network provider, or Hermes availability.
- Provide a test-only provisional interface adapter scoped to
  `tests/avatar_runtime/` so coding can start before the kernel release. It is
  disabled for final conformance and cannot be imported by distributable code.
- Implement an in-memory fake provider and fail-closed authority fixtures. No
  standard provider key, OpenAI network adapter, deployment entrypoint, HTTP
  server, or persistence layer is added.
- Map deterministic tests to every applicable `ACR-*` acceptance ID, including
  hostile identity, retries, duplicate commands, stale revisions, snapshot
  races, control loss, revocation, quota, terminal outcomes, and redaction.
- Finish by pinning the exact kernel commit and digests, running canonical
  fixtures, and proving that no provisional interface path is active.

## Capabilities

### New Capabilities

- `avatar-reference-runtime`: Defines the deterministic, non-deployable
  reference implementation and conformance obligations for the neutral AVC
  protocol.

## Impact

- **openxFactory:** `xfactory/avatar_runtime/` and `tests/avatar_runtime/`.
- **Contract kernel:** read-only provisional baseline during parallel work and
  exact content-addressed pin for final realization; this change does not edit
  canonical contracts or release metadata.
- **F0:** no dependency for implementation because the provider is fake; an
  accepted F0 interface variance may reopen only mapped tests.
- **UI and Flutter client:** no files or widgets; they consume the same kernel
  independently.
- **Operations:** nothing deploys, listens on a socket, holds a provider key, or
  processes tenant data.
- **Compatibility:** additive reference code with no existing runtime consumer.
