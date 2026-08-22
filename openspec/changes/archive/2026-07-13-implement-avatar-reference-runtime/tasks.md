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

## Bookkeeping annotation — archived with all 11 boxes open (2026-08-22, `archive-register-rulings`)

No box is ticked here and no task text above is altered. This section records
what the archive evidence actually shows, because this ledger and this change's
README row disagree with no reconciliation on the record — the anomaly
enumerated as C6 in `docs/archive-record-discrepancies.md`, ruled on 2026-08-22
by Brett (in-session, multiple-choice round) to be annotated rather than
force-ticked.

**What the ledger says.** Eleven boxes across three sections — the package
boundary and parallel seam (§1), the deterministic broker and control model
(§2), conformance and realization (§3) — and every one of them is open. It
archived that way on 2026-07-13 in `44f523b` ("Archive 3 realized avatar
changes (kernel, revocation clarify, reference runtime)"), whose message
reports the gates green ("003 --final, 97 runtime tests, openspec --all
--strict (25 passed)") and says nothing about the open boxes.

**What the README row claims.** "non-deployable deterministic broker/control
reference realized against `contract-v1.7`, with archive-safe content-addressed
conformance (FR-034a); archived 2026-07-13." Note the row's own wording:
realized **against** `contract-v1.7`, not **as** it — this change consumed the
kernel's bundle and cut none of its own.

**Where the realization evidence actually lives — not in this ledger.**

- The runtime package §1 specifies exists: `xfactory/avatar_runtime/`, with the
  injected-port modules the boundary tests require, paired with
  `tests/avatar_runtime/` and its `boundary/`, `conformance/`, `fakes/` and
  `provisional/` trees (the last being §1's quarantined
  `avatar-client-parallel-v1` seam).
- §3.3's content-addressed pin is populated:
  `tests/avatar_runtime/conformance/realization-pin.yaml` carries
  `tag: contract-v1.7`, the exact commit `ddff475f75…`, the interface-lock and
  acceptance-map digests, and the per-file digest set — which is FR-034a, the
  mechanism that makes the conformance evidence survive this directory being
  archived.
- The capability was promoted: `openspec/specs/avatar-reference-runtime/spec.md`.
- `contract-v1.7`, the bundle it was realized against, is a real annotated tag:
  `ddff475`, 2026-07-12.
- **The ticking happened elsewhere.** The execution ledger was the Speckit
  feature `specs/003-avc-reference-runtime/tasks.md`, at 65 of 65 tasks done, 0
  open. It was never mirrored back into these eleven boxes.

So the gap is bookkeeping, not evidence.
