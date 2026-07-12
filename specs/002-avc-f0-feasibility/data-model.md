# Phase 1 Data Model: Avatar Brokered-Call F0 Feasibility Harness

**Feature**: 002-avc-f0-feasibility | **Date**: 2026-07-11

Entities derive from the spec's Key Entities plus the registered result schema
(`f0-results.schema.yaml`) and protocol. Field names that must match the schema are noted.
All identifiers are deterministic; all provider identifiers are hashes; no field may carry a
prohibited-content class (see the redaction allowlist in
[contracts/evidence-outputs.md](./contracts/evidence-outputs.md)).

## RunConfig

The validated input to a run (never written verbatim to evidence).

| Field | Type | Rules |
|-------|------|-------|
| `lab_project_ref` | string | non-empty; a lab project reference, never a tenant/org identifier |
| `credential_source` | enum(`env`) | must be `env`; the key is read only from `OPENAI_API_KEY` (FR-001) |
| `selected_groups` | set of group IDs | subset of {F0-A…F0-F}; default = all six |
| `readiness_deadline_ms` | int | 1,000–5,000; default 3,000; **> 5,000 ⇒ preflight reject** (FR-003) |
| `acceptance_map_path` | path | repo-relative; default the kernel supporting-docs map |
| `acceptance_map_expected_sha256` | hex(64) | pinned; mismatch ⇒ `INCONCLUSIVE` (FR-018) |
| `tools_enabled` | bool | must be `false`; `true` ⇒ preflight reject |
| `tenant_fields_present` | derived bool | any tenant identifier/content ⇒ preflight reject |

**Preflight validation (fail-closed, before any provider call)**: reject tenant data, enabled
tools, credential supplied via args/tracked `.env`/config/evidence file, readiness > 5,000 ms,
or any non-lab/unpinned profile (FR-001, FR-003, SC-009).

## CandidateProfile

Immutable per run; represented as digests, never raw secrets (FR-002).

| Field | Type | Rules / schema mapping |
|-------|------|------------------------|
| `requested_model` | const | `gpt-realtime-2.1` |
| `resolved_model` | string | provider-resolved snapshot (may differ; recorded) |
| `voice` | const | `marin` |
| `interaction_mode` | const | `provider_vad` |
| `turn_detection` | object | `server_vad`, threshold 0.5, prefix 300 ms, silence 500 ms, create+interrupt enabled |
| `harness_revision` | string | source revision |
| `dependency_lock_sha256` | hex(64) | hash of the committed lock |
| `fixture_generator_params` | object | pinned TTS voice/text/params (Q7) |
| `fixture_bytes_sha256` | hex(64) | digest of the generated audio (Q7) |
| `profile_digest` | hex(64) | digest over all of the above |

**Rule**: if the candidate is unavailable or its API shape blocks a mandatory trial, the run
is `INCONCLUSIVE`; behavior is never inferred (FR-004).

## AcceptanceMapRef

The digest-verified source of `ACR-*` IDs (Q3 / FR-018).

| Field | Type | Rules |
|-------|------|-------|
| `source_path` | string | the kernel `avatar-client-acceptance-map.yaml` |
| `source_commit` | string | commit the map was read at |
| `content_sha256` | hex(64) | must equal `acceptance_map_expected_sha256` |
| `interface_baseline` | const | must equal `avatar-client-parallel-v1` |
| `known_acr_ids` | list | parsed IDs; F0-relevant: ACR-003, ACR-008, ACR-011, ACR-012 |

**Rule**: absent map, wrong baseline, or digest mismatch ⇒ run `INCONCLUSIVE`; no placeholder
IDs are minted.

## TrialGroup

Aggregate over one controlled condition; exactly six per run (schema `trial_groups`,
minItems=maxItems=6).

| Field | Type | Rules / schema mapping |
|-------|------|------------------------|
| `id` | enum | F0-A…F0-F |
| `planned` | int | F0-A=20; F0-B…F0-F=10 (schema `contains` constraints) |
| `completed` / `passed` / `failed` | int ≥ 0 | on overall PASS: completed=planned, failed=0 |

Group → condition: F0-A baseline, F0-B delayed-sideband, F0-C sideband-failure (carries the
readiness-timeout path), F0-D revocation, F0-E exact-retry, F0-F changed-retry.

## Trial

One execution; 70 per run (schema `trials`, minItems=maxItems=70).

| Field | Type | Rules / schema mapping |
|-------|------|------------------------|
| `trial_id` | string | `^F0-[A-F]-[0-9]{2}$`; deterministic |
| `group_id` | enum | F0-A…F0-F |
| `status` | enum | PASS / FAIL / INCONCLUSIVE |
| `provider_request_id_hash` | hex(64)\|null | hashed provider request ID (never raw) |
| `durations_ms` | map<string, number≥0> | monotonic offsets from t=0 |
| `assertion_ids` | list, minItems 1 | `^F0-[A-F]-[A-Z0-9_-]+$` |
| `note` | string | bounded, redaction-safe |

### TimingMarkers (populate `durations_ms`)

Offsets from `t_provider_create_accepted` (t=0): `t_offer_ready`, `t_provider_create_sent`,
`t_sideband_open`, `t_sideband_verified`, `t_answer_released`, `t_lease_ack`,
`t_media_authorized`, `t_answer_applied`, `t_first_input_sent`, `t_first_output_playable`,
`t_hangup_sent`, `t_peer_terminal`. Ordering invariant (baseline/delayed):
`sideband_verified ≤ answer_released ≤ lease_ack ≤ media_authorized ≤ answer_applied ≤ first_input_sent`.

### Trial status lifecycle

`planned → running → (PASS | FAIL | INCONCLUSIVE)`. A trial that cannot obtain sufficient
observable evidence is `INCONCLUSIVE`; a reproduced contrary observation is `FAIL`.

## Assertion

Named mandatory check (schema `assertions`).

| Field | Type | Rules |
|-------|------|-------|
| `id` | string | `^F0-[A-F]-[A-Z0-9_-]+$` (e.g. `F0-A-ORDERING`, `F0-C-NO_MEDIA`, `F0-D-TERMINAL_5S`, `F0-E-SINGLE_CALL`, `F0-F-IDEMPOTENCY`, `F0-*-REDACTION`) |
| `status` | enum | PASS / FAIL / INCONCLUSIVE |
| `passed_trials` / `failed_trials` | int ≥ 0 | on overall PASS: failed_trials=0 |

## MetricsSummary

Schema `metrics`; each is a `duration_summary` {count, p50, p95, max}.

| Metric | PASS bound |
|--------|-----------|
| `sideband_ready_ms` | p95 ≤ 3,000; max ≤ 5,000 |
| `first_playable_after_authorized_ms` | p95 ≤ 2,000 |
| `hangup_to_terminal_ms` | max ≤ 5,000 |

## RedactionScanResult

Schema `redaction_scan`.

| Field | Type | Rules |
|-------|------|-------|
| `status` | enum | PASS / FAIL / INCONCLUSIVE |
| `prohibited_findings` | int ≥ 0 | any finding ⇒ status FAIL and the run does not commit (FR-017) |

## EvidenceRecord (`f0-results.json`)

Top-level schema object: `protocol_version="1"`, `started_at`, `completed_at`, `environment`
(lab_project_ref, runtime, dependency_versions, network_type, region?, docs_retrieved_at),
`candidate`, `trial_groups`, `trials`, `metrics`, `assertions`, `redaction_scan`, `overall`,
`report_sha256`. Written directly/atomically under the change `evidence/` dir; validates
against the owned schema with zero errors (SC-008).

### Overall classification (FR-016, derivation)

- `PASS` ⇔ every mandatory trial ran **and** every assertion PASS **and** all metric bounds
  met **and** redaction PASS.
- `FAIL` ⇔ any mandatory assertion contradicted by a reproducible observation, any metric
  bound missed (a p95/hard-ceiling miss cannot be hidden by averages), or a redaction finding.
- `INCONCLUSIVE` ⇔ a mandatory trial did not run / lacked evidence, the candidate was
  unavailable, or the acceptance map was absent/mismatched — never `PASS`.

## HumanReadableSummary (`f0-results.md`)

Narrative companion: deviations, API-shape corrections, threat-model disposition, reviewer
decision. Its SHA-256 is bound into `EvidenceRecord.report_sha256`.

## InterfaceImpactReport (`f0-interface-impact.yaml`)

Always emitted (empty `variances` on a clean pass). Carries `schema_version` + `kind`;
validated against the 002-owned `f0-interface-impact.schema.yaml`
([contract](./contracts/f0-interface-impact.schema.yaml)).

| Variance field | Rules |
|----------------|-------|
| `affected_acr_ids` | ≥ 1 concrete ID from the digest-verified map (no placeholders) |
| `observed_behavior` | bounded, redaction-safe description |
| `evidence_refs` | trial_ids / assertion_ids |
| `severity` | enum (e.g. low/medium/high) |
| `proposed_correction` | neutral correction proposal (kernel owner disposes) |
| `continuation` | whether sibling work can continue behind a closed default |
