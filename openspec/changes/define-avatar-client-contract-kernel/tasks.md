## 1. Interface Baseline And Publication Gate

- [x] 1.1 Record and accept the avatar-client threat model, trust boundaries, stable acceptance IDs, and `avatar-client-parallel-v1` workstream baseline without treating a modified client as preventable by the broker.
- [ ] 1.2 Consume `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0-results.json` and `f0-interface-impact.yaml`; require `PASS` and a disposition for every interface variance before contract publication. Permit schema and fixture implementation to proceed while this gate is pending.
- [ ] 1.3 Freeze the realized field, registry, ordering, timeout, lease, and closed-default decisions in `contracts/avatar-client/interface-lock.yaml`; if F0 changes the baseline, update only this change and notify siblings through the variance protocol.

## 2. AVC Schemas And Registries

- [ ] 2.1 Create `contracts/avatar-client/shared-definitions.schema.yaml` with contract identity, authenticated reference shapes, consent record/version/required purpose IDs, trace, session epoch, media leg and attempt, server-derived offer fingerprint, state revision, last-event sequence, media authorization, session outcomes, retention, redaction, and retry-equivalence definitions.
- [ ] 2.2 Implement AVC-01 and AVC-02, including exact-offer idempotency, `grant | denial | terminal` discrimination, credential-free non-grants, held answers, scoped control descriptors, bounded readiness/heartbeat/lease fields, resume semantics, fallback modes, and the closed reason registry.
- [ ] 2.3 Implement AVC-04, AVC-11, and AVC-12 plus closed event and command registries, allowed producers, authoritative versus observational classification, revision guards, one-log sequence fields, snapshot barriers, and result mappings.
- [ ] 2.4 Implement AVC-06, AVC-07, and AVC-08 with effect-bound confirmation, minimal retention classes, reserved forbidden/disabled classes, immutable persona identity, disclosure, language, and lifecycle fields.
- [ ] 2.5 Add capability, interaction-mode, model-profile, session-outcome, fallback, and neutral consent-purpose registries. Keep provider-native VAD values in server profiles and keep the memory-gateway consent schema unchanged and non-authoritative for avatar media.

## 3. Conformance And Contract Release

- [ ] 3.1 Add valid, invalid, boundary, compatibility, unknown-field, unknown-authority, redaction, and adversarial fixtures for every schema and every `ACR-*`, `SCO-*`, and `RBG-*` scenario owned by this change.
- [ ] 3.2 Implement `scripts/validate-avatar-client.py` to validate schemas, references, closed registries, fixtures, acceptance-map parity, evidence presence, secret exclusion, and interface-lock consistency. The validator MUST fail on missing, duplicate, renamed, or evidence-free normative scenarios.
- [ ] 3.3 Register the complete family in `contracts/manifest.yaml`, allocate the next available minor bundle version after merge order is known, update `contracts/CHANGELOG.md` and `contracts/README.md` atomically, and publish the matching annotated tag from the realized release commit with per-file digests.

## 4. Governance, Handoffs, And Realization

- [ ] 4.1 Verify the shared-contract and repository-boundary deltas against the realized files, including content-addressed consumer pinning, canonical fixture execution, private-client boundaries, and separately approved production deployment.
- [ ] 4.2 Publish a machine-readable kernel handoff containing the release tag, exact commit, per-file digests, interface-lock digest, acceptance-map digest, and compatibility instructions for the reference-runtime and UI-standard siblings.
- [ ] 4.3 Run strict target/all OpenSpec validation, `validate-avatar-client.py`, manifest/changelog/tag consistency, supporting-document hashes, `git diff --check`, and the recorded DomainxFactory compatibility validators. Block regressions introduced by this change, not dated pre-existing domain debt.
