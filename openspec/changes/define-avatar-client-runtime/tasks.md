## 1. De-Risk And Proposal Gate

- [ ] 1.1 Run the F0 brokered-call spike: a throwaway script performing `POST /v1/realtime/calls` with atomic configuration, parallel sideband attach, and delayed-versus-immediate SDP answer against the real API using a lab project key and no tenant data; record setup/first-audio timings, the provider documentation and model versions used, and any AVC-01/AVC-02 shape corrections as a design note in this change.
- [ ] 1.2 Record a one-page trust-boundary and data-flow threat model covering client, broker, WSS control, WebRTC media, OpenAI sideband, the authority stub, and telemetry, naming the internal-live authentication mechanism (OIDC bearer at the broker plus the AVC-02 control credential).

## 2. AVC Contract Kernel

- [ ] 2.1 Create `contracts/avatar-client/` with `shared-definitions.schema.yaml` (contract identity, actor/client/subject/purpose references, consent and policy versions, trace, session epoch, media leg, state revision, retention class, redaction, retry-equivalence rule) as YAML-serialized JSON Schema draft 2020-12.
- [ ] 2.2 Implement AVC-01 (request idempotency, client instance and app version, purpose and workflow references, capability profile, contract compatibility, persona, language, platform, accessibility preferences, consent/profile versions, transient never-persisted `sdp_offer`, resume last-applied sequence) and AVC-02 (grant/session/epoch/media-leg identity, inline resolved capabilities, SDP answer, control-channel descriptor, heartbeat interval, lease expiry, initial snapshot), including grant redelivery and single-use offer-bound answer semantics.
- [ ] 2.3 Implement AVC-04 plus the event registry: observation-versus-authoritative classification, allowed producers, payload schemas including the transcript-segment payload, retention class, state-advancing flag, and the single-log sequence fields.
- [ ] 2.4 Implement AVC-11 plus the command registry (command types, payload schemas, which types require `expected_state_revision`) and the canonical accepted/rejected/duplicate/conflict/expired result mapping.
- [ ] 2.5 Implement AVC-06 as a server-issued challenge (ID, version, scope, display-safe fields, effect summary, risk class, policy/consent versions, expiry, issuing revision) with the minimal ID+version client decision, and AVC-12 (four authoritative axes, optional client presentation preferences, pending command/confirmation references, policy versions, last-event sequence, issue time).
- [ ] 2.6 Implement AVC-07 (ephemeral, operational-telemetry, and structured-record classes; reserved-forbidden transcript/audio/video/independent-transcription classes; reserved-disabled offline-draft class) and a slim AVC-08 (immutable persona ID/version, display name and role, voice profile reference, supported languages, required disclosure, lifecycle status).
- [ ] 2.7 Add fixtures for each contract: valid, invalid, boundary, unknown-field, unknown-authority, redaction, duplicate command, stale revision, gap-then-snapshot recovery, second-instance denial, lease expiry, consent withdrawal, quota blocked, and confirmation supersede.
- [ ] 2.8 Implement `scripts/validate-avatar-client.py` scoped to schema and fixture validation (matching existing `validate-*.py` conventions); register the family in `contracts/manifest.yaml`, reconcile the manifest `contract_bundle_version` with `contracts/CHANGELOG.md`, and update `contracts/README.md`.

## 3. Deterministic Reference Broker

- [ ] 3.1 Create `xfactory/avatar_runtime/` with module boundaries for broker preflight, grant issuance, control protocol, command processing, event log, snapshot projection, lease management, authority stub, usage metering, and kill switches, documented as non-deployable reference code.
- [ ] 3.2 Implement the fail-closed in-process authority stub: static policy bundle file, fixture consent records, speech-gate selection, and one reference intake workflow handler (capture subject, need, and contact preference; the single consequential action is submitting the intake record) that owns the external operation idempotency key.
- [ ] 3.3 Implement grant issuance with request-id dedupe and verbatim redelivery until first media connect or expiry, single-instance enforcement with canonical second-instance denial, epoch fencing on revocation and lease expiry, and per-tenant concurrent-session and duration caps with usage records and the canonical quota-blocked result.
- [ ] 3.4 Implement the WSS reference protocol: command/event/snapshot frames, heartbeat with lease extension and last-applied sequence, scoped reconnect credential rotation, revocation, and bounded message sizes.
- [ ] 3.5 Implement command validation (lease, epoch, allowlist, conditional expected-revision), the dedupe table returning recorded results, the single sequenced event log with producer-authority enforcement, and snapshot-only recovery.
- [ ] 3.6 Implement both kill switches (all session creation; per model profile) with optional active-lease revocation, plus session duration caps ending legs in the `session_limit_reached` resume state.
- [ ] 3.7 Add the deterministic test suite: forged body identity, cross-client isolation, duplicate command, stale revision, event gap recovery, heartbeat loss and lease expiry, control-loss stop behavior, revocation, terminal-state resume denial, consent invalidation revoking the lease, confirmation supersede, and redaction of grants/telemetry.

## 4. Avatar-First UI Standard Alignment

- [ ] 4.1 Update `docs/avatar-first-ui-standard.md` to the ratified model: four authoritative axes plus client-local presentation mode, command/event/snapshot authority, presentation duties, recording awareness, safe rendering, and handoff invariants.
- [ ] 4.2 Update `contracts/schemas/avatar-first-ui-profile.schema.yaml` as the domain overlay carrier: runtime contract compatibility, speech-gate selection, control-loss and fallback slots, persona catalog reference, consent purposes, retention overlay, and accessibility baseline, preserving compatibility for existing profiles.
- [ ] 4.3 Extend the memory-gateway consent profile schema with media-capture and provider-processing purposes (or record the decision for a dedicated avatar consent vocabulary if extension proves wrong while implementing).
- [ ] 4.4 Update `templates/ui/avatar-first.yaml` and add validated examples: customer avatar-first, client hybrid, domain conventional-first, and a Ledgerx-style confirmation-before-action profile.
- [ ] 4.5 Extend `scripts/validate-avatar-first-ui.py` for the promoted axes, runtime references, speech-gate and control-loss slots, persona references, and fallback requirements.

## 5. Ratification Hygiene And Successor Map

- [ ] 5.1 List this change and the successor-change map (`implement-avatar-client-lab`, `qualify-avatar-live-voice`, `avatar-pilot-hardening`, plus deferred-feature changes) in the README OpenSpec Records block.
- [ ] 5.2 Run `OPENSPEC_TELEMETRY=0 openspec validate define-avatar-client-runtime --strict` and `--all --strict`, all openxFactory validators, and the supporting-doc hash verification; fix any failures before requesting ratification.
