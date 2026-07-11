# Phase 1 Data Model: AVC Contract Kernel

**Feature**: 001-avc-contract-kernel | **Date**: 2026-07-11

This model describes the **artifacts this feature produces** and the neutral
field groups they carry. Deep per-field AVC semantics are owned by the OpenSpec
`design.md` (Decisions 1–16) and the `avatar-client-runtime` delta; this document
captures entity identity, relationships, validation rules, and state machines at
the altitude the plan needs. Every YAML artifact carries `schema_version` and
`kind` (constitution Principle IV).

---

## A. Contract schemas (8) + shared definitions

### Shared definitions (`shared-definitions.schema.yaml`)
- **Kind**: JSON Schema draft 2020-12 `$defs` module.
- **`$defs` groups**: actor / client / subject reference; workflow purpose;
  consent record reference + version + required purpose IDs; trace; session
  epoch; media leg; media attempt; server-derived SDP-offer fingerprint
  (`sdp_offer_sha256`); state revision; last-event sequence; media authorization
  state; session outcomes; retention class; redaction marker; retry-equivalence
  rule.
- **Relationships**: referenced by all 8 contracts via relative `$ref`.
- **Rules**: no field in `$defs` may require a provider DTO, model identifier,
  client widget state, or secret (FR-006).

### The eight contracts
| ID | File | Key neutral field groups | Notable rules |
|----|------|--------------------------|---------------|
| AVC-01 | `avc-01-session-request.schema.yaml` | idempotency/request key, client instance + app version, workflow + purpose refs, requested capability profile, contract compat, persona, language, platform, a11y prefs, consent/profile versions, transient `sdp_offer`, resume {logical session, epoch, last-applied seq} | `sdp_offer` transient/never-persisted; body fields are references, not proof (FR-009) |
| AVC-02 | `avc-02-session-result.schema.yaml` | discriminator `result_kind ∈ {grant,denial,terminal}`; common {request id, media-attempt status, safe-message key, retry guidance, fallback modes}; grant-only {grant/session/epoch/media-leg identity, resolved policy+capabilities (absorbed AVC-03), offer fingerprint, offer-bound SDP answer, control descriptor, heartbeat interval, lease expiry, initial media-auth state, initial AVC-12} | denial/terminal MUST be structurally incapable of carrying SDP / SDP answer / credential (FR-007); reasons from closed registry |
| AVC-04 | `avc-04-session-event.schema.yaml` | event id, sequence, class `observation|authoritative`, registered producer, payload (incl. AVC-05 transcript-segment payload) | immutable; producer/class from registry (FR-011) |
| AVC-06 | `avc-06-structured-confirmation.schema.yaml` | confirmation id + version, action/field scope, display-safe fields, normalized effect summary, risk class, policy+consent versions, expiry, issuing state revision | no binding digest required (FR-013) |
| AVC-07 | `avc-07-retention-profile.schema.yaml` | retention class distinctions (ephemeral presentation / operational telemetry / structured record); reserved-forbidden classes | reserved classes forbidden this kernel; schema+fixtures only, no instances (FR-017, Q2) |
| AVC-08 | `avc-08-persona-profile.schema.yaml` | persona identity, disclosure, language, lifecycle fields; immutable-per-session persona | schema+fixtures only, no catalog instances (FR-014, Q2) |
| AVC-11 | `avc-11-session-command.schema.yaml` | command id (idempotency key), registered command type, session + epoch, registry-declared payload, client-observed time; optional `expected_state_revision` on revision-guarded types | media/presentation commands omit revision guard (FR-011) |
| AVC-12 | `avc-12-state-snapshot.schema.yaml` | four authoritative axes projection, `last_event_sequence` (recovery cursor), `state_revision`; client-local presentation preferences (non-authoritative) | `last_event_sequence` is the only stream cursor (FR-011) |

**Reserved**: AVC-03 absorbed inline (AVC-02 `capabilities`), AVC-05 = AVC-04
payload, AVC-09/AVC-10 reserved — identifiers never reused (FR-002).

---

## B. Registries (closed vocabularies)

**Entity**: registry data file (`kind: avatar-client-registry`).
**Fields**: `schema_version`, `kind`, `registry_id`, `registry_version`,
ordered `members[]` (`id`, `description`, optional `producer`/`authority`/
`class` metadata).

| registry_id | Members (closed) |
|-------------|------------------|
| `session-result-reasons` | exactly 15: identity_denied, consent_missing, policy_denied, contract_incompatible, profile_disabled, interaction_mode_unsupported, quota_blocked, second_instance_denied, idempotency_conflict, media_readiness_timeout, provider_unavailable, grant_consumed, attempt_expired, attempt_abandoned, attempt_revoked |
| `events` | registered event types + producer + observation/authoritative class |
| `commands` | registered command types + revision-guarded flag |
| `retention-classes` | ephemeral-presentation, operational-telemetry, structured-record + reserved/forbidden classes |
| `capabilities` | logical capability identifiers |
| `interaction-modes` | includes `provider_vad`; excludes push-to-talk (fails preflight) |
| `session-outcomes` | terminal/lifecycle outcome values |
| `fallback-modes` | text, human_handoff, retry_later, upgrade_required, none |
| `consent-purposes` | exactly 3: avatar.media_capture, avatar.provider_processing, avatar.structured_record |

**Rules**: closed (unknown value rejected, Principle VII); **schema/registry
parity** — every schema enum bound to a registry must set-equal that registry's
member ids (validator-enforced, D3); member id sets for `session-result-reasons`
(15) and `consent-purposes` (3) are exact (SC-004).

---

## C. Acceptance map (`acceptance-map.yaml`)
- **Kind**: realized copy of the supporting-docs acceptance map under
  `contracts/avatar-client/` (traceability doc: "Task 3.2 realizes this map").
- **Fields**: `schema_version`, `change_id`, `interface_baseline`,
  `expected_requirement_count: 17`, `expected_scenario_count: 72`,
  `requirements[]` (`id` ACR-*/SCO-*/RBG-*, capability, title, owner_tasks,
  owner_changes, evidence_types, `scenarios[]` {id `-Snn`, title}).
- **Rules**: parity with the three deltas (0 unmapped/duplicated/renamed);
  counts must equal 17 / 72 (SC-003); every scenario resolves in the evidence
  register (§D).

---

## D. Evidence / disposition register (`evidence-register.yaml`)
- **Kind**: `avatar-client-evidence-register` (consolidated, Q4/FR-032).
- **Entry fields**: `scenario_id`, `evidence_type ∈ {automated, manual, live_f0,
  successor}`, `status`, and type-specific:
  - automated → `evidence_id` (must exist in `fixtures/index.yaml`);
  - manual → `result`, `reviewer`, `disposition`;
  - live_f0 / successor → `owner_change`, `fail_closed_default`.
- **Relationships**: one entry per acceptance-map scenario (bijective over the 72).

**Status state machine** (validator-enforced, D5):

```text
            ┌──────────── automated / manual ────────────┐
planned ──▶ evidenced ──▶ accepted
   │
   └──────▶ deferred            (live_f0 / successor; requires owner_change +
                                 fail_closed_default)
```

- Allowed transitions: `planned→evidenced`, `evidenced→accepted`,
  `planned→deferred`. No others.
- **Fail conditions**: scenario missing; automated entry with no existing
  fixture; manual entry with no recorded result/reviewer/disposition; deferred
  entry with no owner_change or fail_closed_default; illegal status transition;
  referenced artifact absent (all → validation failure, SC-003).

---

## E. Interface lock (`interface-lock.yaml`)
- **Kind**: `avatar-client-interface-lock` (frozen realized decisions +
  `avatar-client-parallel-v1` baseline reconciliation, FR-030).
- **Fields**: frozen `fields`, `registries`, `ordering`, `timeouts`
  (media_readiness 1000–5000; heartbeat >0..5000; lease ≤10000), `leases`,
  `closed_defaults`; plus **`f0_evidence_pin`** block (Q6/D6):
  `{ f0_source_commit, f0_results_schema_sha256, f0_interface_impact_schema_sha256 }`.
- **Rules**: corrections made only in this change; the `f0_evidence_pin`
  digests/commit gate publication (§H); the validator recomputes and compares.

---

## F. Fixture-case (`fixtures/<schema>/<case>.yaml`) + index
- **Kind**: `avatar-client-fixture-case` (self-describing, D2).
- **Fields**: `case_id`, `target`, `target_kind ∈ {schema,registry}`,
  `expect ∈ {valid,invalid}`, `scenario_ids[]`, `evidence_id`, `notes`,
  `instance` (pure JSON-compatible).
- **`fixtures/index.yaml`**: enumerates every case
  (`case_id`, `target`, `expect`, `scenario_ids`, `path`, `evidence_id`).
- **Coverage rules (FR-019)**: for every schema — valid, invalid, boundary,
  compatibility, unknown-field, unknown-authority, redaction, adversarial; for
  every ACR-*/SCO-*/RBG- scenario owned by this change — at least one case whose
  `scenario_ids` contains it (or an evidence-register manual/deferred entry for
  non-automatable types).
- **Redaction rules (D4)**: any synthetic secret appears only as a declared
  bounded sentinel from `redaction/sentinels.yaml`.

---

## G. Redaction config (validator config, not pinned semantic set)
- **`redaction/denylist-patterns.yaml`** (`kind: avatar-client-redaction-denylist`):
  ordered `patterns[]` (`id`, `regex`, `class ∈ {credential, sdp, raw_payload,
  transcript_media, high_cardinality_id}`).
- **`redaction/sentinels.yaml`** (`kind: avatar-client-redaction-sentinels`):
  `sentinels[]` (`id`, `bounded_form`, `max_len`) — reserved fixed forms the scan
  permits; anything matching a denylist pattern but not an exact bounded sentinel
  fails (SC-008).

---

## H. Contract bundle release (realization)
- **Semantic consumed set (per-file SHA-256 digested + manifest-registered,
  FR-022/Q1)**: 8 schemas, shared-definitions, 9 registries, fixtures (+index),
  acceptance-map, interface-lock, evidence-register.
- **Shipped but not pinned-semantic (Design Note 3)**:
  `scripts/validate-avatar-client.py`, `redaction/*` (content-addressed by commit).
- **Release identity (Principle VI / versioning policy)**: `contract_bundle_version`
  = next minor after `contract-v1.6` (→ `contract-v1.7`); matching
  `contracts/CHANGELOG.md` entry; annotated `contract-v1.7` tag on the realized
  commit; per-file digests; `contracts/manifest.yaml` entries (`id`, `path`,
  `type`, `schema_version`, `sha256`, `intended_consumers`).
- **F0 gate (FR-029/FR-033)**: tag blocked until F0 `PASS`, all variances
  dispositioned, and `f0_evidence_pin` validation passes (fail-closed on any
  mismatch).
- **Completion states (FR-034)**: *implementation complete, publication pending
  F0* → *realized*.

---

## Cross-artifact validation rules (enforced by `validate-avatar-client.py`)
1. Every schema parses as valid draft 2020-12 and all `$ref`s resolve offline (SC-001).
2. Schema/registry enum parity; exact member counts for the two exact registries (SC-004).
3. Fixture index complete; every case validates to its declared `expect` under
   the reference runner (SC-002); coverage present for every schema + owned scenario.
4. Acceptance-map parity (17/72; 0 unmapped/duplicated/renamed) and bijective
   evidence-register resolution with legal status (SC-003).
5. Dual redaction: structural (schema construction) + content scan with bounded
   sentinels; 0 secret-bearing files pass (SC-005/SC-008).
6. Digest/manifest/changelog/tag identity over the consumed set; tag-only pin
   fails (SC-006).
7. F0 gate pin + validate + fail-closed; no tag under adverse F0 (SC-007/SC-010).
