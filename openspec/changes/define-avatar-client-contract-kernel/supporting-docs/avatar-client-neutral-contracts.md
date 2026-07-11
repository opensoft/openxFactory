# Avatar Client Neutral Runtime Contracts

Status: superseded
Kind: contract design
Captured: 2026-07-10
Updated: 2026-07-10 after lead architecture review
Superseded: 2026-07-10
Superseded by: avatar-client split proposal set
Relocation note: historical body frozen; supersession links updated for the split
Repository context: openxFactory (contract-level, cross-factory topic)
Proposed by: define-avatar-client-runtime
Staging ID: openxFactory:staging:avatar-client
Target capabilities: avatar-client-runtime, shared-contract-ownership
Parent:
[Flutter Avatar Client And UI Lab](flutter-avatar-client-ui-lab.md)

> Historical pre-review input. Its 12-contract family, replay mechanics, and
> client obligations are superseded. Do not use it as implementation guidance.
> Use the [kernel design](../design.md),
> [runtime delta](../specs/avatar-client-runtime/spec.md),
> [shared-ownership delta](../specs/shared-contract-ownership/spec.md), and
> [parallel plan](avatar-client-parallel-workstream-plan.md).

This superseded proposal supporting document is non-normative and retained
only to preserve the design history that preceded the eight-contract kernel.

## Invariants

- openxFactory owns canonical meaning, shared definitions, registries,
  compatibility, fixtures, validation, and the reference server control plane.
- `xfactory-avatar-client` owns generated Dart bindings, Flutter UI, pure
  reducers, constrained client transports, and platform adapters.
- Authenticated identity, client/tenant, representative authority, consent,
  and purpose are verified server-side; request fields are not proof.
- Production OpenAI uses brokered SDP and sideband readiness. Continuous media
  is direct after negotiation; xFactory does not relay audio.
- AVC-11 commands are untrusted requests. AVC-04 events are immutable and carry
  explicit observation/authority classification. AVC-12 is the recovery source
  of truth.
- Hermes/workflow services own tools, confirmation, consent, approval,
  execution, records, and handoff.
- Provider/model names are server profile configuration, never UI switches.
- Provider credentials, SDP, raw media, and prohibited transcript content do
  not enter persisted contracts, telemetry, crash reports, or support bundles.

## Shared Envelope Definitions

Every applicable contract uses these shared definitions rather than declaring
incompatible local variants:

| Definition | Required meaning |
| --- | --- |
| Contract identity | `contract_id`, integer `contract_schema_version`, openxFactory release/commit compatibility |
| Actor context | Authenticated actor reference/type, representative authority reference when applicable |
| Scope | `client_ref`, optional subject reference, workflow reference, declared purpose |
| Policy | Immutable policy bundle, consent profile/version, retention profile/version |
| Session | Logical session ID, session epoch, client instance, media-leg ID where applicable |
| Concurrency | State revision, command idempotency, stream ID/sequence/predecessor, replay cursor |
| Trace | Trace/correlation/causation IDs plus redacted provider references |
| Time | UTC wall time for audit plus monotonic time only for local interval measurement |
| Retention | Explicit retention class and policy reference |

## Contract Family

| ID | Contract | Trusted producer | Primary consumers |
| --- | --- | --- | --- |
| AVC-01 | `avatar_session_request` | Flutter through authenticated transport | Session broker |
| AVC-02 | `avatar_session_grant` | Session broker | Flutter, control controller |
| AVC-03 | `voice_runtime_capabilities` | Approved server adapter | Broker, Flutter, Hermes |
| AVC-04 | `avatar_session_event` | Registry-authorized source | Reducer, workflow, audit, telemetry |
| AVC-05 | `transcript_segment` | Canonical transcript mapper | UI, policy-approved transcript store |
| AVC-06 | `structured_confirmation` | Hermes/workflow challenge issuer | Flutter, workflow, audit |
| AVC-07 | `avatar_retention_profile` | Domain/client policy authority | Client, broker, stores |
| AVC-08 | `avatar_persona_profile` | Domain overlay authority | Client, broker |
| AVC-09 | `voice_adapter_descriptor` | Server adapter release | Broker, compatibility validator |
| AVC-10 | `voice_latency_sample` | Client/server telemetry | Evaluation and release gates |
| AVC-11 | `avatar_session_command` | Flutter through authenticated control | Control API, Hermes/workflow |
| AVC-12 | `avatar_state_snapshot` | Broker/Hermes projection | Flutter, recovery, audit |

## AVC-01 Avatar Session Request

AVC-01 expresses requested capability and references verified context. It does
not contain a provider credential or a raw model ID.

| Field | Required | Meaning |
| --- | --- | --- |
| Contract identity | yes | AVC-01 schema/release compatibility |
| `request_id` | yes | Idempotency key scoped to authenticated actor/client |
| `requested_at` | yes | Client-observed UTC time; not authority time |
| `client_instance_id` | yes | Running app/tab identity |
| `app_version` | yes | Client release identity |
| `client_ref` | yes | Claimed client scope, checked against transport identity |
| `actor_ref` | yes | Claimed actor reference, checked server-side |
| `subject_ref` | conditional | Subject when distinct from actor |
| `representative_authority_ref` | conditional | Guardian/delegate/representative basis |
| `workflow_ref` and `purpose` | yes | Canonical workflow and bounded purpose |
| `ui_profile_ref` and `domain_overlay_ref` | yes | Immutable version/digest references |
| `persona_ref` | yes | Requested persona ID/version |
| `retention_profile_ref` | yes | Requested immutable retention profile |
| `consent_profile_ref` | yes | Consent ID/version for purpose/media/retention |
| `language` and `platform` | yes | BCP 47 language; Windows/web/iOS/Android |
| `requested_capabilities` | yes | Neutral capability IDs |
| `client_compatibility` | yes | Supported AVC contract release/major |
| `accessibility_preferences` | yes | Reduced motion, captions, text-only, etc. |
| `recovery_cursor` | no | Opaque server-issued cursor only |

Equivalent retries reuse the result. Conflicting reuse of `request_id` is a
canonical conflict and never creates another provider call.

## AVC-02 Avatar Session Grant

AVC-02 is the short-lived result of verified identity, policy, compatibility,
provider, and sideband preflight.

| Field | Required | Meaning |
| --- | --- | --- |
| Contract identity | yes | AVC-02 schema/release compatibility |
| `grant_id`, `session_id`, `request_id` | yes | Grant, logical session, and source request |
| `session_epoch`, `client_instance_id` | yes | Active authority generation and owner |
| `media_leg_id` | yes | Current provider connection identity |
| Verified scope bundle | yes | Actor/client/subject/workflow/purpose references |
| Resolved policy bundle | yes | Consent, retention, speech, prompt, and safety versions |
| `voice_profile_id`, `adapter_id`, `adapter_version` | yes | Server-selected profile/adapter |
| `capabilities` | yes | Resolved AVC-03 |
| `transport` | yes | Initially `webrtc_direct` for production Flutter |
| `authorization_mode` | yes | `brokered_sdp` for production OpenAI |
| `transport_authorization` | yes, transient | One-time SDP answer/negotiation result |
| `control_channel` | yes | Allowlisted WSS endpoint, scoped auth, protocol version |
| `heartbeat_interval_ms`, `lease_expires_at` | yes | Client/server authority lease |
| `recovery_cursor` | yes | Opaque replay/snapshot cursor |
| `initial_snapshot` | yes | AVC-12 at the granted revision |
| `audit_ref` | yes | Server audit root |

Persist only authorization fingerprint/mode/expiry. Tokens, endpoint secrets,
headers, SDP, standard provider keys, and call credentials are redacted.

## AVC-03 Voice Runtime Capabilities

| Field | Required | Allowed values or meaning |
| --- | --- | --- |
| `media_transport` | yes | `webrtc_direct`, `text_only`, or separately approved mode |
| `duplex_mode` | yes | `turn_based`, `full_duplex` |
| `interruption` | yes | `none`, `client_cancel`, `server_truncate` |
| Input/output transcript | yes | `none`, `final`, `delta_and_final` |
| `server_control` | yes | `sideband`, `equivalent_control`, `none` |
| `control_protocol` | yes | Supported AVC WSS protocol version |
| `speech_gate_modes` | yes | Gates the adapter can actually enforce |
| `tool_intent_observation` | yes | Model can propose untrusted intent evidence |
| `voice_mutability` | yes | `before_first_audio`, `per_response`, `media_leg_fixed` |
| `reconnect` | yes | `none`, `new_media_leg`, `new_session_with_cursor` |
| `concurrent_work` | yes | Conversation may continue while governed work runs |
| Image/visual support | yes | Approved input/result capability, not raw widget support |
| `max_session_seconds` | conditional | Provider/policy limit |
| `supported_languages` | yes | Approved BCP 47 tags |
| `regional_data_controls` | yes | Approved region/retention capabilities |
| `unsupported_reasons` | no | Requested capability to canonical explanation |

A required missing capability blocks live media or selects a preapproved
fallback. The client never infers capability from a model name.

## AVC-04 Avatar Session Event

| Field | Required | Meaning |
| --- | --- | --- |
| Contract and event IDs | yes | Schema identity and global idempotency |
| `event_type` | yes | Registered canonical event |
| Session scope | yes | Session, epoch, media leg when applicable, workflow |
| `source`, `source_instance` | yes | Registered producer identity |
| `authority` | yes | `observation` or `authoritative` |
| Stream chain | conditional | Stream ID, sequence, previous event ID, replay cursor |
| `state_revision` | conditional | Required for authoritative state effects |
| Time and trace | yes | Occurrence time, correlation and optional causation |
| `retention_class` | yes | Registry-compatible retention |
| `payload` | yes | Event-specific canonical schema |
| `audit_sequence` | no | Assigned asynchronously by audit storage |

The registry, not the producer's claim, determines whether a source may author
an event. Provider/client observations never become approval, execution,
consent, confirmation, workflow completion, or lifecycle authority.

## AVC-05 Transcript Segment

AVC-05 carries segment/turn/session/media-leg identity, speaker, text, language,
source kind, provisional/final/interrupted/corrected/superseded status,
playback-heard state, source reference, timing, replacement chain, confidence
when available, and retention class. Interrupted output is never displayed as
heard. Transcript content never confirms a value or action.

## AVC-06 Structured Confirmation

AVC-06 is a server-issued challenge, not a client-authored record:

| Field | Required | Meaning |
| --- | --- | --- |
| `confirmation_id`, `version` | yes | Immutable challenge identity |
| Session/epoch/workflow/actor scope | yes | Exact authority boundary |
| `intent_ref` or field/action scope | yes | Proposed consequential effect |
| `display_fields` | yes | Display-safe labels and complete values |
| `effect_summary` | yes | Canonical normalized outcome shown to user |
| `risk_class` | yes | Ordinary/consequential/regulated |
| Policy and consent versions | yes | Rules used to issue challenge |
| `state_revision`, `expires_at` | yes | Concurrency and validity |
| `binding_digest` | yes | Canonical digest over bound effect/context |
| `status` | yes | Pending/confirmed/declined/expired/superseded |

The client decision contains only challenge identity/version, digest, decision,
and AVC-11 command ID. Actor comes from authenticated context. Any material
change or stale revision supersedes the challenge.

## AVC-07 Avatar Retention Profile

AVC-07 separately controls captions, full transcript, audio, video,
independent transcription, structured workflow records, telemetry, and offline
drafts. Each retained class declares purpose, consent basis, storage authority,
region, access rule, duration, withdrawal behavior, legal-hold reference, and
redaction policy.

Offline policy includes allowed fields, maximum age, Windows key protection,
web eligibility, origin isolation, non-exportable key requirement,
synchronization, conflict behavior, and deletion/key-destruction evidence. Web
offline drafts default disabled.

## AVC-08 Avatar Persona Profile

AVC-08 carries immutable persona ID/version, domain owner, display name/role,
presentation style, approved visual asset reference and provenance/license,
animation states, provider-neutral voice profile, supported languages/contexts,
required disclosure, impersonation policy, continuity scope, media-leg rotation
rule, and lifecycle status. Selection is limited to the resolved catalog.

## AVC-09 Voice Adapter Descriptor

AVC-09 distinguishes server and client adapter components. It records adapter
ID/version, provider, supported profiles, requested model alias/snapshot,
provider-resolved model, prompt/policy/voice/turn configuration versions,
capability/event mapper versions, authorization mode, sideband readiness,
direct-media requirement, contract compatibility, region/data controls, and
experimental/candidate/approved/retired status.

`gpt-live-1` remains disabled until its published API contract and all promotion
evidence pass. Model profile changes apply to new sessions/media legs only.

## AVC-10 Voice Latency Sample

AVC-10 carries sample/session/media-leg/turn identity, adapter/profile,
platform, network, region, clock source/quality, monotonic markers, derived
intervals, direct or brokered reference classification, and reproducible fixture
reference. Markers cover broker request, provider call, sideband ready, media
connected, speech, first audio, playback, interruption, command, tool outcome,
recovery, and teardown. It contains no raw content or secrets.

## AVC-11 Avatar Session Command

| Field | Required | Meaning |
| --- | --- | --- |
| Contract and `command_id` | yes | Schema identity and idempotency |
| `command_type` | yes | Registered client request type |
| Session/epoch/client instance | yes | Active lease boundary |
| `expected_state_revision` | yes | Optimistic concurrency guard |
| `idempotency_scope` | yes | Logical operation retry scope |
| Trace/causation | yes | Command relationship |
| `payload` | yes | Command-specific schema, never raw provider JSON |
| `client_observed_at` | yes | Non-authoritative client time |

The control API derives actor authority from transport, validates lease, epoch,
purpose, policy, command type, and revision, and emits accepted, rejected,
duplicate, conflict, or expired authoritative events. Equivalent retries reuse
the command ID and result.

## AVC-12 Avatar State Snapshot

AVC-12 carries contract/session/epoch/client scope, state revision, all five
state axes, workflow projection, active persona and media leg, pending command
and confirmation references, consent/policy/retention versions, control lease
summary, replay cursor, issuance time, and integrity digest. A snapshot is
accepted only from the authoritative control source. Local presentation
preferences may survive reconciliation; stale authority projections may not.

## Provider Context And Attachment Rules

Provider conversation state is disposable. Duration/context rollover uses an
AVC-12 source snapshot and a minimal purpose-bound context packet with policy,
prompt, consent, retention, and source-snapshot digests. Full transcript is not
carried into a new media leg unless explicitly authorized. Critical authority,
tool, and safety instructions are reapplied from server-owned versions.

Attachment bytes use the governed upload/document service. AVC-11 carries only
an opaque authorized reference and display-safe metadata. Direct Flutter-to-
provider file transfer and offline attachment-byte storage are outside F1-F6.

## Versioning And Compatibility

- New contracts and optional fields are additive within a contract major.
- New required fields, enum removals, semantic/authority changes, or ordering
  changes require the repository's deprecation and major-version process.
- Generated Dart and future TypeScript bindings pin release/commit and digest.
- Unknown non-consequential provider observations remain inert; unknown
  authority, commands, decisions, and lifecycle states fail closed.
- Provider IDs stay redacted references and never replace canonical identity.
- Conformance covers minimum/full, compatible/incompatible, expired/denied,
  duplicate/conflict, replay/gap/snapshot, takeover/revocation, reconnect,
  consent withdrawal, and unsupported capability for each applicable contract.

The schema split is resolved: AVC-01 through AVC-12 are a family with shared
definitions because grants, high-volume events, commands, snapshots, retained
records, and release descriptors have different consumers and cadence.
