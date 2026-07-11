## 1. Package Boundary And Parallel Seam

- [ ] 1.1 Create `xfactory/avatar_runtime/` and `tests/avatar_runtime/` with documented non-deployable boundaries and tests rejecting listeners, application entrypoints, deployment files, persistence, live network SDKs, and provider credentials.
- [ ] 1.2 Add injected clock, ID, provider, policy, consent, operation, and usage ports plus deterministic in-memory implementations. Add the `avatar-client-parallel-v1` adapter only under `tests/avatar_runtime/provisional/`.

## 2. Deterministic Broker And Control Model

- [ ] 2.1 Implement logical-session and media-attempt state machines, epoch fencing, one-instance/one-leg enforcement, fresh-resume replacement, terminal transitions, per-tenant caps, and duration limits.
- [ ] 2.2 Implement AVC-02 total outcome mapping, exact-offer idempotency, changed-offer conflict, process-memory-only grant retry cache, credential-free terminal replay, cache destruction, and usage outcomes.
- [ ] 2.3 Implement fake provider create, held answer, sideband readiness, authenticated lease acknowledgement, authoritative `media_authorized`, readiness timeout, heartbeat/lease ceilings, reconnect credential rotation, and idempotent provider termination.
- [ ] 2.4 Implement command validation, revision guards, command-result dedupe, producer-authority checks, the single sequenced event log, state projection, atomic snapshot barrier, bounded post-barrier buffering, overflow restart, and no historical replay.
- [ ] 2.5 Implement fail-closed policy, consent-purpose mapping, speech-gate selection, structured confirmation, idempotent fixture operation execution, consent withdrawal/invalidation, five-second revocation behavior, kill switches, and redacted telemetry.

## 3. Conformance And Realization

- [ ] 3.1 Add deterministic tests mapped to all applicable `ACR-*` and every `ARR-*` scenario, including forged identity, cross-client isolation, all outcomes, retries, offer mismatch, sideband ordering/failure, duplicate commands, stale revisions, snapshot races, control loss, consent revocation, quota, terminal resume, confirmation supersession, and redaction.
- [ ] 3.2 Consume any accepted `f0-interface-impact.yaml` variance by its acceptance IDs and update only runtime-owned adapters/tests; record unaffected test evidence as still valid.
- [ ] 3.3 Pin the realized contract bundle tag, exact commit, per-file digests, interface-lock digest, and acceptance-map digest; run canonical fixtures with the provisional adapter disabled and prove package code cannot import it.
- [ ] 3.4 Run strict target/all OpenSpec validation, the complete deterministic suite, boundary/import checks, canonical fixture conformance, redaction checks, and `git diff --check`. Confirm that no canonical contract, F0, UI, DomainxFactory, or deployment file changed.
