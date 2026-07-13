# avatar-client-runtime Specification

## Purpose
TBD - created by archiving change define-avatar-client-contract-kernel. Update Purpose after archive.
## Requirements
### Requirement: Versioned neutral avatar-client contract kernel
openxFactory SHALL publish the avatar-client contract kernel under
`contracts/avatar-client/` as YAML-serialized JSON Schema (draft 2020-12)
files: AVC-01 avatar session request, AVC-02 avatar session result (a
discriminated grant, denial, or terminal outcome, with resolved runtime
capabilities inline on grants), AVC-04 avatar session event (with
transcript segments as a registered payload schema), AVC-06 structured
confirmation, AVC-07 avatar retention profile, AVC-08 avatar persona profile,
AVC-11 avatar session command, and AVC-12 avatar state snapshot. AVC-03 and
AVC-05 are absorbed as described; AVC-09 and AVC-10 remain reserved for the
live-qualification successor change and their identifiers are never reused.

Every contract SHALL declare its contract ID and `contract_schema_version`,
share definitions through a single `shared-definitions.schema.yaml`
referenced by `$ref`, and register in `contracts/manifest.yaml` under the
repository contract changelog policy. Realization SHALL allocate the next
available minor bundle version, update the manifest and changelog atomically,
and publish an annotated tag with that version. Consumers SHALL pin the exact
openxFactory commit and per-file digest; a tag alone is insufficient. Shared
definitions SHALL cover actor, client, subject, workflow purpose, consent
record reference/version/required purpose IDs, trace, session epoch, media
leg, media attempt, server-derived SDP-offer fingerprint, state revision,
last-event sequence, session outcomes, retention class, redaction, and the
retry-equivalence rule. Retry equivalence SHALL be canonical-form equality
across every non-volatile request field plus the exact offer fingerprint; only declared
client-observed timestamps MAY be volatile. Provider DTOs, model identifiers,
client widget state, and secrets MUST NOT be required neutral fields.

An unknown command, authoritative event, lifecycle state, or confirmation
decision MUST fail closed. Provider-specific unknown observations MUST remain
non-authoritative until a reviewed mapper handles them. Additive optional
fields SHALL follow the declared compatibility policy.

#### Scenario: Compatible binding reads an additive contract
- **WHEN** a consumer pinned to the same contract major receives a fixture containing a supported additive optional field
- **THEN** it MUST preserve or ignore the field according to contract policy without changing canonical behavior

#### Scenario: Consumer receives an incompatible major
- **WHEN** a client or broker cannot satisfy the required contract major
- **THEN** session preflight MUST fail before media or governed commands are enabled

#### Scenario: Consequential vocabulary is unknown
- **WHEN** a consumer receives an unknown command, authority-bearing event, confirmation decision, or lifecycle state
- **THEN** it MUST reject the transition, request a current snapshot or handoff, and MUST NOT infer a permissive meaning

### Requirement: Authenticated, purpose-bound session results
The session broker SHALL authenticate the caller through trusted transport
context and SHALL derive client/tenant, actor, subject, representative
authority, and permission scope server-side. Client-authored body fields
MUST NOT serve as proof of identity, consent, or authority.

AVC-01 SHALL carry a request idempotency key, client instance and app
version, workflow and purpose references, requested capability profile,
contract compatibility, persona, language, platform, accessibility
preferences, consent and profile versions, a transient never-persisted SDP
offer, and, on resume, the logical session ID, session epoch, and last-applied
event sequence. On receipt the broker SHALL compute `sdp_offer_sha256` from
the exact SDP bytes before discarding the body. Every response to AVC-01 SHALL
be AVC-02 with `result_kind` equal to `grant`, `denial`, or `terminal` and
common request ID, media-attempt status, safe-message key, retry guidance, and
fallback modes. Only `grant` SHALL bind grant, logical session, session epoch,
and media-leg identity, the resolved policy and capability set, the
server-derived offer fingerprint and offer-bound SDP answer, an authenticated
control-channel descriptor, heartbeat interval, lease expiry, initial
media-authorization state, and the initial AVC-12 snapshot. Before using a
grant, the client SHALL compute the fingerprint of its current local offer and
reject AVC-02 if it does not equal the server fingerprint. It SHALL NOT apply
the answer before matching `media_authorized`. Provider and control endpoints
SHALL come from server allowlists; credentials SHALL be short-lived, scoped,
and excluded from URLs.

The initial AVC-02 reason registry SHALL be closed, versioned, and contain exactly
`identity_denied`, `consent_missing`, `policy_denied`,
`contract_incompatible`, `profile_disabled`,
`interaction_mode_unsupported`, `quota_blocked`,
`second_instance_denied`, `idempotency_conflict`,
`media_readiness_timeout`, `provider_unavailable`, `grant_consumed`,
`attempt_expired`, `attempt_abandoned`, and `attempt_revoked`. Denial and
terminal variants MUST NOT contain SDP, an SDP answer, or a credential. They
SHALL carry `retryable`, MAY carry bounded `retry_after_ms`, SHALL carry only
approved `fallback_modes` from `text`, `human_handoff`, `retry_later`,
`upgrade_required`, or `none`, and SHALL use a localization-safe message key
instead of provider error text.

Each request ID SHALL identify one media attempt and one exact offer
fingerprint. While that attempt is pending, an equivalent retry from the same
authenticated actor and client instance SHALL receive the same unconsumed,
unexpired grant and answer and SHALL NOT create another provider call. A
request that reuses the request ID with a different offer fingerprint or any
other changed non-volatile field SHALL receive an AVC-02 `denial` with
`idempotency_conflict`, SHALL NOT receive the prior answer, and SHALL NOT
create another provider call.
After the first successful media connection, an equivalent retry SHALL
receive an AVC-02 `terminal` result with `grant_consumed`; expired, abandoned,
and revoked attempts SHALL return their corresponding credential-free AVC-02
terminal results.

The broker MAY retain the exact pending grant, answer, scoped control
credential, offer fingerprint, and retry context only in a secret-classified,
TTL-bounded ephemeral retry cache. The reference runtime SHALL keep that cache
in process memory only. A production shared cache MUST encrypt it in transit
and at rest, MUST disable disk persistence, snapshots, and backups, and MUST
exclude it from durable records, logs, telemetry, crash reports, and support
bundles. Every cache entry MUST be destroyed when its attempt becomes
connected, abandoned, expired, or revoked. A durable terminal idempotency
record MAY contain request ID, offer fingerprint, authorized context
references, terminal status, and a credential-free AVC-02 denial or terminal
result, but MUST NOT contain SDP, an SDP answer, or any credential.

A client that needs a regenerated offer SHALL use a fresh request ID and an
authorized logical-session/epoch resume reference. Before issuing the new
leg, the broker SHALL atomically terminate and mark any prior pending attempt
abandoned. One client instance SHALL hold the lease, and at most one pending
or connected media leg SHALL exist per logical session; a concurrent request
from another instance SHALL receive the AVC-02 denial
`second_instance_denied`
(policy-gated takeover is deferred).

Profiles SHALL declare per-tenant maximum concurrent sessions and maximum
session duration. Every media leg SHALL emit a usage record attributed to
client and workflow references, and provider capacity, rate-limit, and
budget failures SHALL map to the AVC-02 denial `quota_blocked`.

#### Scenario: Authorized session is granted
- **WHEN** authenticated identity, purpose, consent, persona, policy, retention, contract compatibility, quota, and kill-switch checks all pass
- **THEN** the broker MUST issue one AVC-02 `grant` and initial authoritative snapshot bound to the verified context

#### Scenario: Body identity is forged
- **WHEN** AVC-01 references an actor, subject, client, consent, or workflow scope not authorized by transport identity
- **THEN** the broker MUST return AVC-02 `denial` reason `identity_denied` before creating a provider call or control lease

#### Scenario: Session request is retried after a lost response
- **WHEN** the same authenticated request ID is retried equivalently while the issued grant remains unconsumed and unexpired
- **THEN** the broker MUST redeliver the ephemeral cached grant to the same client instance and MUST NOT create a second billable provider call

#### Scenario: A retry substitutes another SDP offer
- **WHEN** the same request ID arrives with a different server-computed offer fingerprint or another changed non-volatile field
- **THEN** the broker MUST return AVC-02 `denial` reason `idempotency_conflict`, MUST NOT return the prior answer, and MUST NOT create another provider call

#### Scenario: A grant answer is bound to another local offer
- **WHEN** the AVC-02 offer fingerprint does not equal the fingerprint of the client's current local offer
- **THEN** the client MUST reject the grant, MUST NOT apply the SDP answer, and MUST keep media disabled

#### Scenario: A failed pending attempt needs a regenerated offer
- **WHEN** the authorized client submits a fresh request ID and valid resume reference for the same active logical session and epoch
- **THEN** the broker MUST terminate and abandon the prior pending leg before issuing at most one fresh media leg for the new offer

#### Scenario: A second client instance requests the active session
- **WHEN** a concurrent AVC-01 arrives from a different client instance for a logical session with an active lease
- **THEN** the broker MUST return AVC-02 `denial` reason `second_instance_denied` and MUST NOT revoke the active grant

#### Scenario: Tenant quota is exhausted
- **WHEN** a request would exceed the profile's per-tenant concurrent-session cap or a provider capacity limit is reported
- **THEN** the broker MUST return AVC-02 `denial` reason `quota_blocked` and record the attributed usage outcome

#### Scenario: Non-grant result attempts to carry a secret
- **WHEN** an AVC-02 denial or terminal result contains an SDP answer, control credential, provider credential, or raw provider error
- **THEN** schema validation MUST fail and the result MUST NOT be sent or persisted

### Requirement: Brokered direct media with sideband control
The production OpenAI profile SHALL use brokered call creation: the
openxFactory server adapter calls the provider call-creation endpoint with a
server-held project-scoped key and the full server-owned session
configuration (model, voice, instructions, safety, turn detection, tools)
atomically in the create request. When the provider returns the SDP answer and
call ID, the broker SHALL hold the answer, attach the authenticated sideband
controller by call ID, and verify the configured session before releasing the
answer inside AVC-02 `grant`. The trusted first-party client media adapter
SHALL verify the offer fingerprint but MUST NOT apply the answer yet. It SHALL
first establish authenticated xFactory WSS and send `lease_ack` containing the
grant, logical session, epoch, media leg, client instance, and last-applied
event sequence. The broker SHALL validate that acknowledgement against
transport-derived identity and the active grant; body fields SHALL not prove
authority. Only after both WSS acknowledgement and sideband verification SHALL
the broker emit authoritative `media_authorized`. The trusted adapter SHALL
apply the answer and enable provider-bound microphone audio or playback only
after applying that matching event. The broker/server adapter MUST NOT initiate
a provider response earlier.

The signed first-party media adapter is inside the confidentiality trusted
computing base for disclosure, local capture, answer application, playback,
and the typed data-channel allowlist. It remains untrusted for workflow
authority. If a modified client bypasses the local controls, that is a
compromised-client incident: sideband detection and hangup contain but cannot
retroactively prevent audio disclosure. Every resulting provider event SHALL
remain non-authoritative, the authority stub or Hermes MUST reject every tool
intent while media authorization is inactive, and the broker SHALL terminate
the call as soon as sideband observes the violation. Such a violation MUST NOT
produce an external operation or authoritative workflow transition.

`media_readiness_timeout_ms` SHALL default to 3,000, SHALL be at least 1,000,
and MUST NOT exceed 5,000. The timer starts when the provider create response
is accepted. If sideband verification or WSS acknowledgement misses the
deadline, the broker SHALL revoke the attempt, invoke the provider adapter's
termination operation, and return AVC-02 `denial` reason
`media_readiness_timeout`; the client SHALL discard the unapplied answer. For
the OpenAI profile, the termination operation SHALL use
`POST /v1/realtime/calls/{call_id}/hangup`; another provider profile SHALL
identify an equivalently enforceable server-side operation before
qualification.

After media authorization, encrypted realtime media SHALL flow directly
between the client and the approved provider; xFactory MUST NOT relay or
transcode the continuous media path. Standard provider keys MUST NOT reach the
client.
Each deployment environment SHALL use a distinct project-scoped provider key
held only in deployment secret storage, and a documented manual rotation
procedure SHALL exist before internal live use. Ephemeral-token setup SHALL
be limited to a non-consequential lab profile with tools disabled, approved
test data, and no production tenant access.

The neutral live interaction mode SHALL be `provider_vad`; exact provider
turn-detection values MUST remain in a server-owned profile. The F0 OpenAI
candidate SHALL pin `server_vad` with threshold `0.5`,
`prefix_padding_ms=300`, `silence_duration_ms=500`,
`create_response=true`, and `interrupt_response=true`. A changed Server VAD
configuration or Semantic VAD profile requires separate qualification
evidence. The client provider data channel SHALL expose a typed allowlist whose
complete outbound set is `response.cancel` and `output_audio_buffer.clear`, used only for
explicit stop/cancel behavior; ordinary VAD interruption SHALL remain
provider-managed. It MUST NOT expose generic provider JSON send, session
updates, conversation or user text, instructions, tool definitions, function
outputs, `input_audio_buffer.clear`, `input_audio_buffer.commit`,
`response.create`, item truncation, or privilege-bearing provider events.
Because WebRTC push-to-talk requires those excluded events, push-to-talk SHALL
remain disabled and a request for it SHALL fail preflight into approved text or
human fallback. User text, attachment references, confirmations, and governed
actions SHALL use AVC-11 over the control channel.

#### Scenario: Production OpenAI call starts
- **WHEN** the broker creates a production OpenAI media leg
- **THEN** the full session configuration MUST be applied in the create request and the SDP answer MUST remain held until the call-ID-bound sideband is verified
- **AND** after receiving AVC-02 `grant`, the trusted client media adapter MUST leave the answer unapplied until matching `media_authorized`

#### Scenario: Both control channels become ready
- **WHEN** the broker validates the client's `lease_ack` and the provider sideband verifies the same logical session, epoch, call, and media leg
- **THEN** the broker MUST emit one authoritative `media_authorized` event and only that matching event MAY permit answer application, provider-bound audio, and playback

#### Scenario: Media is attempted before authorization
- **WHEN** client or server code attempts to transmit user audio, play provider output, initiate a response, or enable user-triggered tools before the matching `media_authorized` event
- **THEN** the trusted client or server adapter MUST reject or suppress the operation and record a redacted protocol violation

#### Scenario: A modified client bypasses the local media gate
- **WHEN** provider activity or a tool intent is observed before authoritative media authorization
- **THEN** the broker MUST classify a compromised-client incident, terminate the call, record that confidentiality prevention was no longer guaranteed, and MUST NOT permit an external operation or authoritative transition

#### Scenario: Sideband does not become ready
- **WHEN** sideband verification or WSS acknowledgement misses the profile readiness timeout
- **THEN** the broker MUST revoke and terminate the media leg, the client MUST discard the unapplied answer, and the workflow MUST receive AVC-02 `denial` reason `media_readiness_timeout`

#### Scenario: Profile exceeds the readiness ceiling
- **WHEN** a profile requests `media_readiness_timeout_ms` below 1,000 or above 5,000
- **THEN** profile validation and preflight MUST fail before a provider call is created

#### Scenario: Client attempts provider reconfiguration
- **WHEN** client code attempts to send a provider event outside the enumerated allowlist
- **THEN** the constrained adapter MUST reject the operation locally and security telemetry MUST record a redacted violation

#### Scenario: A profile requests push-to-talk
- **WHEN** a profile requests push-to-talk or disables VAD under this kernel
- **THEN** preflight MUST refuse live voice and offer only an approved text or human-handoff fallback

#### Scenario: Session ends or is revoked
- **WHEN** the logical session completes, is abandoned, is revoked, expires, or loses its required lease
- **THEN** the broker and client MUST close the media leg, discard transport authorization, and preserve only policy-required canonical records

### Requirement: Single-log command, event, and snapshot authority
AVC-11 SHALL be the only neutral client-to-control mutation envelope,
carrying a stable command ID, registered command type, session and epoch,
registry-declared payload, and client-observed time. The control API SHALL
validate authentication, active lease, epoch, and command allowlist, and
SHALL return canonical accepted, rejected, duplicate, conflict, or expired
events. The command ID SHALL be the idempotency key: retries reuse it and
receive the recorded result from a server dedupe table. Expected state
revision SHALL be required only on command types the registry flags as
revision-guarded; confirmation decisions bind through AVC-06; media and
presentation commands omit it.

AVC-04 SHALL be immutable and SHALL classify each event as observation or
authoritative with registry-declared producers. Client and provider sources
MAY emit only registered observations; only the broker, the authority stub
(later Hermes or workflow services), or an accountable human SHALL emit
authoritative policy, consent, confirmation, approval, execution, lifecycle,
workflow, or handoff results.

Each logical session SHALL have exactly one authoritative event log. The
control API SHALL be the sole sequencer, assigning a monotonic sequence at
append time. `state_revision` SHALL equal the sequence of the last
state-advancing event and SHALL be used only for state-transition concurrency.
AVC-12 SHALL separately carry `last_event_sequence`, the event sequence through
which the snapshot was projected; only `last_event_sequence` SHALL serve as
the recovery stream cursor.

Recovery SHALL be snapshot-based and atomically handed to live delivery. On a
gap, conflict, or reconnect, the control WSS SHALL establish a barrier at
sequence `B`, project AVC-12 through `B` with `last_event_sequence=B`, and
buffer events appended after `B` while sending the snapshot as the first
recovery frame. It SHALL then deliver the bounded post-barrier buffer in order
before live push. The client SHALL discard locally buffered events at or below
`B` and SHALL accept the next event only when its sequence is `B+1`. If the
buffer overflows or the next sequence is not `B+1`, both sides SHALL abandon
that handoff and establish a newer barrier. Event hash chains, snapshot
integrity digests, and historical replay protocols MUST NOT be required by the
kernel contracts.

#### Scenario: Client submits a valid command
- **WHEN** an allowed AVC-11 command matches the authenticated session, active epoch and lease, and any required expected revision
- **THEN** the control API MUST return an accepted authoritative event and process the transition under the same command ID

#### Scenario: Command is retried
- **WHEN** an accepted or terminal command is delivered again with the same command ID and an equivalent payload
- **THEN** the server MUST return the recorded canonical result and MUST NOT repeat external execution

#### Scenario: Revision-guarded command uses a stale revision
- **WHEN** a registry-flagged command carries an expected revision older than authoritative state
- **THEN** the server MUST return a conflict event and the current snapshot path without executing the command

#### Scenario: Event stream has a gap
- **WHEN** a consumer receives an authoritative sequence whose predecessor it has not applied
- **THEN** it MUST stop consequential transitions, establish a snapshot barrier, discard events at or below the snapshot's `last_event_sequence`, and require the next event in order

#### Scenario: An event arrives while a recovery snapshot is produced
- **WHEN** event `B+1` is appended after the server fixes snapshot barrier `B` but before the client applies AVC-12
- **THEN** the server MUST send AVC-12 with `last_event_sequence=B` first, then deliver event `B+1` from the bounded handoff buffer before live push

#### Scenario: Client reports a tool completed
- **WHEN** a client or provider observation claims approval, execution, tool completion, workflow completion, or consent
- **THEN** the event validator MUST reject it as an unauthorized producer and MUST NOT advance authoritative state

### Requirement: Leased control channel and deterministic recovery
The control transport SHALL be authenticated WSS carrying commands, events,
snapshots, heartbeats, and revocation. The client SHALL send a heartbeat
every declared interval carrying session epoch and last-applied sequence;
each server heartbeat response SHALL extend the lease, return the new lease
expiry, and MAY carry a fresh scoped reconnect credential bound to session,
epoch, and client instance. Every media-capable profile SHALL set
`heartbeat_interval_ms` greater than zero and no greater than 5,000 and SHALL
set initial lease expiry no later than 10,000 milliseconds after grant
issuance. Each heartbeat response MAY extend lease expiry to no later than
10,000 milliseconds after that response. Profiles MAY use stricter values but
MUST NOT raise either neutral ceiling. Control health SHALL be degraded after
one missed response and lost after the profile-declared count or lease expiry,
whichever occurs first, evaluated against the client's monotonic clock.
Command results serve as acknowledgements; per-message acknowledgement frames
MUST NOT be required.

Loss of control SHALL immediately disable governed commands and pending
confirmations and stop capture and playback; there is no speech grace
interval. Lease expiry SHALL close the media leg even while provider
connectivity remains healthy. A dropped control connection SHALL reconnect
with the newest reconnect credential while the lease remains valid;
otherwise the client starts over with AVC-01.

Revocation SHALL be client-enforced: on any revocation trigger — an explicit
revoke, control loss, or lease expiry — the client SHALL disable governed
commands and pending confirmations, stop capture and playback, close the media
leg, and issue the provider revocation request within 5,000 milliseconds of the
trigger, evaluated against the client's monotonic clock. This client-side stop
is the revocation guarantee. The provider-side authoritative termination
confirmation MAY be eventually-consistent and lag the client-side stop, and
MUST NOT be the sole evidence that revocation occurred; a profile whose provider
cannot positively confirm termination within the bound SHALL still satisfy this
requirement through the client-side stop and the accepted revocation request,
and SHALL record the provider settle behavior as evidence.

Session lifecycle, control health, media state, and workflow projection
SHALL be separate authoritative axes with a transition registry declaring
allowed predecessors, terminal states, and authority sources; presentation
mode SHALL remain client-local. Provider reconnect SHALL create a new media
leg under the same logical session only while the lease is valid; pending
consequential commands SHALL reconcile by command ID before any retry.
Terminal, revoked, expired, completed, and abandoned sessions MUST NOT
resume as active.

#### Scenario: Control channel is lost while media remains connected
- **WHEN** the declared count of heartbeat responses is missed
- **THEN** the client MUST set control health to lost, disable governed commands and confirmations, and stop capture and playback no later than lease expiry

#### Scenario: A media profile exceeds the neutral lease ceilings
- **WHEN** a profile requests a heartbeat interval above 5,000 milliseconds, an initial lease beyond 10,000 milliseconds after grant issuance, or a renewal beyond 10,000 milliseconds after its heartbeat response
- **THEN** profile validation and session preflight MUST fail before a provider call is created

#### Scenario: Control connection drops transiently
- **WHEN** the WSS drops while the lease remains valid
- **THEN** the client MUST reconnect with the newest scoped reconnect credential and resume from its last-applied sequence via snapshot recovery

#### Scenario: Pending action exists during reconnect
- **WHEN** a disconnect occurs after command acceptance but before its outcome is displayed
- **THEN** recovery MUST query the recorded command result by command ID and MUST NOT issue a new external action

#### Scenario: User pauses and resumes
- **WHEN** a non-terminal session is paused and resumed within policy limits
- **THEN** capture and playback MUST stop while paused and resume from an authoritative snapshot without creating a second workflow

#### Scenario: Revocation is client-enforced within the bound
- **WHEN** a session is explicitly revoked, control is lost, or the lease expires
- **THEN** the client MUST disable governed commands and confirmations, stop capture and playback, close the media leg, and issue the provider revocation request within 5,000 milliseconds of the trigger
- **AND** the provider-side authoritative termination confirmation MAY settle later and MUST NOT be the sole evidence that revocation occurred, provided the client-side stop and the accepted revocation request completed within the bound

### Requirement: Governed tools and effect-bound confirmation
Hermes and governed workflow services SHALL own tool selection, normalized
arguments, credentials, purpose, consent, confirmation, approval, denial,
execution, idempotency, records, and handoff; until Hermes integration
lands, the reference broker SHALL exercise that authority through a
fail-closed in-process authority stub (static policy bundle, fixture consent
records, one reference intake workflow) that is server-side and explicitly
acts on behalf of the future Hermes boundary. The client MUST NOT receive
domain credentials, execute provider functions, or treat provider arguments
as authorized. Provider tool calls SHALL be untrusted intent evidence, and
the external operation idempotency key SHALL be server-owned and stable
across retries.

AVC-06 SHALL be a server-issued confirmation challenge bound to
confirmation ID and version, action or field scope, display-safe fields, a
normalized effect summary, risk class, policy and consent versions, expiry,
and the issuing state revision. The AVC-11 decision SHALL carry only the
confirmation ID, version, decision, and command ID; actor identity SHALL
come from authenticated context. A material input or effect change SHALL
supersede the challenge and require new confirmation. Binding digests MUST
NOT be required.

#### Scenario: Model proposes a consequential action
- **WHEN** a provider emits an intent that could access protected data, change state, spend money, communicate externally, or trigger domain work
- **THEN** the server adapter MUST treat it as untrusted evidence and route a bounded intent to the authority stub or Hermes without client execution

#### Scenario: Exact effect is confirmed
- **WHEN** the user accepts a current, unexpired challenge whose version and issuing revision match server state
- **THEN** the authority MAY proceed according to policy and MUST record the exact challenge, actor, consent, policy, and resulting command

#### Scenario: Confirmation is stale or superseded
- **WHEN** the decision references an expired, superseded, or version-mismatched challenge or another epoch or actor
- **THEN** the server MUST reject it without execution and issue a new challenge when the action remains eligible

#### Scenario: Silence or transcript text resembles agreement
- **WHEN** a transcript contains affirmative language but no valid confirmation command exists
- **THEN** the workflow MUST remain unconfirmed

### Requirement: Server-owned model profiles and session-fixed persona
The client SHALL request logical capabilities and SHALL branch only on the
grant's resolved capabilities and canonical state; model and provider
identifiers stay in server profiles. Profile promotion SHALL be
configuration-controlled, human-approved, and new-session-only, recording
requested and provider-resolved model per session. `gpt-realtime-2.1` SHALL be
the initial F0 candidate but MUST remain disabled for internal-live and
production sessions until `qualify-avatar-live-voice` records approved
promotion evidence. This kernel therefore defines no qualified live provider
profile. All other profiles, including `gpt-live-1`, SHALL remain disabled
pending supported API contracts and their own qualification. Once a qualified
profile exists, rollback SHALL select the last qualified profile; if none
exists, rollback SHALL disable voice and offer text or handoff. A running media
leg MUST NOT silently change model, voice, adapter, or immutable provider
configuration.

Persona SHALL be selected at session start from the domain catalog and
remain fixed for the logical session; changing persona SHALL end the session
and start a new one. Voice SHALL be fixed per media leg. Mid-session persona
rotation is deferred.

#### Scenario: Qualified default model changes
- **WHEN** a new provider profile passes promotion
- **THEN** new sessions MUST use the approved profile without model-name branches in client widgets or neutral reducers

#### Scenario: Candidate model has not passed live qualification
- **WHEN** an internal-live or production session requests `gpt-realtime-2.1` before approved promotion evidence exists
- **THEN** preflight MUST keep live voice disabled and offer the approved text or handoff fallback

#### Scenario: Future model lacks API support
- **WHEN** a target model has no supported deployment API or required control behavior
- **THEN** its profile MUST remain disabled and the system MUST use the last qualified profile or disable voice when no qualified profile exists

#### Scenario: User asks to change persona mid-session
- **WHEN** an active logical session receives a persona-change request
- **THEN** the client MUST offer to end the session and start a new one with the requested persona and MUST NOT rotate persona in place

### Requirement: Consent-before-capture and enforceable speech gates
The resolved domain/client policy SHALL select the speech gate, and a client
request MUST NOT weaken it. `confirmation_before_action` SHALL be the
default gate and SHALL hold all consequential actions behind AVC-06 and
governed authority. `streaming_monitor` SHALL be allowed only for response
classes whose policy accepts that speech may reach the user before review.
`pre_speech_review` SHALL remain a reserved gate in this kernel: selecting
it SHALL fail preflight into an approved text or human-handoff fallback, and
its reviewed speech pipeline is deferred. An adapter that cannot satisfy the
required gate SHALL fail preflight rather than weaken policy.

The neutral consent-purpose registry SHALL define
`avatar.media_capture`, `avatar.provider_processing`, and
`avatar.structured_record`. AVC SHALL carry only the consent record reference,
version, and required purpose IDs. A server-side consent-authority port SHALL
resolve those references from the owning DomainxFactory or tenant consent
system; domain systems own evidence, legal basis, representatives, withdrawal,
and stricter purpose IDs. The memory-gateway consent profile MAY be adapted to
that port but MUST NOT become the neutral media-consent authority.

Disclosure and current authorization for `avatar.media_capture` and
`avatar.provider_processing` SHALL exist before microphone capture or provider
session creation. `avatar.structured_record` SHALL additionally be required
before retaining a structured workflow record. When a user initiates consent withdrawal in the client, the
client SHALL stop local capture and playback before sending the withdrawal
command. Consent withdrawal through any channel SHALL cancel output, revoke
the lease, terminate the media leg, and prevent new retention.

When the broker learns that a consent version bound to an active grant is no
longer valid, it SHALL immediately mark the lease revoked, push an
authoritative revocation event, and invoke the provider adapter's termination
operation. The OpenAI adapter SHALL use
`POST /v1/realtime/calls/{call_id}/hangup`. Provider-bound input and output
SHALL cease no more than 5,000 milliseconds after the broker learns of
invalidation. The next heartbeat MAY deliver the already-effective revocation
but MUST NOT define or extend this deadline. A provider profile whose adapter
cannot demonstrate termination within this bound MUST NOT become eligible for
`media_authorized`.

#### Scenario: User has not completed media disclosure
- **WHEN** required disclosure or provider-processing consent is absent, stale, or outside the workflow purpose
- **THEN** the broker MUST return AVC-02 `denial` reason `consent_missing`, MUST NOT create a provider call, and the client MUST keep microphone capture off

#### Scenario: Memory consent record is offered as media authority
- **WHEN** a memory-gateway consent profile is supplied without a server-side consent-authority adapter proving the required avatar purpose IDs
- **THEN** preflight MUST return AVC-02 `denial` reason `consent_missing` and MUST NOT infer media authorization from the memory schema alone

#### Scenario: Policy requires the reserved gate
- **WHEN** a response class resolves to `pre_speech_review` under this kernel
- **THEN** preflight MUST fail into the approved text or human-handoff fallback and MUST NOT stream unreviewed audio for that class

#### Scenario: Consent is withdrawn during speech
- **WHEN** the user initiates consent withdrawal while capture or playback is active
- **THEN** the client MUST stop local capture and playback before sending the command, and acceptance MUST cause the broker to revoke the lease and terminate the active media leg

#### Scenario: Consent is invalidated server-side
- **WHEN** the broker learns a bound consent version is no longer valid through any non-client channel
- **THEN** it MUST make revocation effective immediately, push the revocation event, and terminate provider-bound input and output within 5,000 milliseconds

#### Scenario: Provider termination cannot meet the revocation bound
- **WHEN** provider qualification cannot demonstrate media-leg termination within 5,000 milliseconds of broker revocation
- **THEN** that provider profile MUST fail qualification and MUST NOT emit `media_authorized`

### Requirement: Disposable provider context and attachment references
The provider conversation SHALL be treated as an ephemeral interaction
cache, never the workflow system of record. Session duration SHALL be capped
by profile below provider limits; on reaching a duration or context limit
the broker SHALL reconcile pending commands, issue a snapshot, and end the
media leg in an explicit session-limit-reached resume state. A reconnected
or resumed media leg SHALL be rehydrated from server-owned configuration
plus a default ephemeral same-session context carryover (a bounded
recent-turns summary within the same logical session and purpose); full
transcript carryover and cross-purpose reuse SHALL remain policy-gated and
out of kernel scope. Every new media leg SHALL reapply critical
instructions, authority boundaries, tool policy, and safety configuration
from server-owned versions. Seamless mid-conversation rollover is deferred.

Attachment bytes SHALL use a governed upload path when one exists; AVC-11
MAY carry only an opaque authorized attachment reference and display-safe
metadata, and the client MUST NOT send attachment bytes directly to the
voice provider. The attachment byte path itself is deferred.

#### Scenario: Session reaches its duration limit
- **WHEN** a media leg reaches the profile duration or context limit
- **THEN** the broker MUST reconcile pending commands, snapshot authoritative state, and end the leg in the session-limit-reached resume state

#### Scenario: Media leg reconnects after a network drop
- **WHEN** the broker authorizes a new media leg for the same logical session
- **THEN** the leg MUST be rehydrated from server-owned configuration plus the bounded same-session carryover so prior conversation context is not silently lost
- **AND** workflow gates, consent, authority, and tool policy MUST come from server-owned state, not provider memory

#### Scenario: User attaches a document
- **WHEN** a workflow permits an attachment
- **THEN** the client MUST send only an authorized reference through AVC-11 and the provider MUST receive no file bytes from the client

### Requirement: Minimal retention with no local persistence
AVC-07 SHALL distinguish ephemeral presentation, operational telemetry, and
structured workflow record classes. Captions, partial transcript deltas,
provider credentials, SDP, media, and raw provider payloads SHALL be
ephemeral. Structured confirmation decisions, consent versions, approvals,
tool outcomes, and final workflow outcomes SHALL be retained only under
their policy and purpose. Full transcript, audio, video, and independent
transcription SHALL be reserved classes that are forbidden under this
kernel and MAY be ratified only by a successor change.

Offline drafts SHALL be deferred: the client MUST NOT persist sensitive
session data locally, and the reserved offline-draft class SHALL remain
disabled. A revision-guarded command that conflicts with newer authoritative
state SHALL enter review mode for correction; the server MUST NOT silently
overwrite either side.

#### Scenario: Captions are presentation only
- **WHEN** transcript deltas are used for live captions
- **THEN** they MUST expire with the session and MUST NOT become confirmation or workflow records

#### Scenario: A reserved retention class is requested
- **WHEN** a profile or command requests full transcript, audio, video, or independent-transcription retention
- **THEN** the broker MUST refuse it as a reserved class pending its successor change

#### Scenario: Conflicting edit is submitted
- **WHEN** a revision-guarded command carries a stale expected revision
- **THEN** the client MUST present a review of the conflicting values and changed consequential values MUST require new confirmation

### Requirement: Redacted telemetry and latency evidence
Telemetry SHALL support end-to-end correlation across client, broker,
sideband, authority stub, and provider references without persisting raw
media, transcript content, SDP, credentials, arbitrary subject identifiers,
or unbounded high-cardinality payloads; a log, trace, metric, crash report,
or support bundle containing such content MUST fail validation and MUST NOT
be published. Latency evidence in this kernel SHALL be structured logging
with monotonic timestamps for broker setup, sideband attach, media
connected, and recovery, informed by the F0 spike; the formal AVC-10 latency
contract and pilot latency budgets belong to the live-qualification
successor change, and a live pilot MUST NOT proceed without approved
measured budgets from that change.

#### Scenario: Telemetry attempts to include protected content
- **WHEN** a telemetry artifact contains a credential, SDP, raw transcript, raw media, or prohibited identifier
- **THEN** validation MUST fail and the artifact MUST NOT be published

#### Scenario: Live pilot is proposed without budgets
- **WHEN** no approved measured latency and recovery budgets exist
- **THEN** the live pilot gate MUST remain blocked

### Requirement: Deterministic-first release gating and kill switches
Release rings SHALL be: deterministic lab (contracts, reference broker, and
client slices proven against canonical fixtures with no live provider),
internal live (live provider qualification plus secret scan, telemetry
redaction verification, kill-switch proof, and measured latency evidence),
and pilot (threat-model closure, data-handling review, accessibility
evidence, and rollback rehearsal). A later ring SHALL require the prior
ring's evidence, and live provider behavior SHALL NOT be release eligible
until deterministic acceptance passes. Before contract publication and
annotated tagging, the registered
threat model SHALL be accepted and the F0 protocol SHALL produce passing
machine-readable evidence for answer ordering, sideband failure containment,
readiness timing, and five-second hangup. F0 MUST NOT qualify a live model.

Every normative requirement and scenario SHALL have a stable entry in the
acceptance map naming its owning task, fixture or manual evidence ID, release
ring, and status. `scripts/validate-avatar-client.py` SHALL compare the map to
the delta specifications and fail when a requirement or scenario is unmapped,
duplicated, or points to missing evidence.

Two server kill switches SHALL exist — all new session creation, and per
model profile — each with optional revocation of active leases. Rollback
SHALL stop new sessions on the withdrawn profile, revoke affected active
leases when safety requires it, and preserve only policy-required records.

#### Scenario: Live qualification begins early
- **WHEN** deterministic-lab evidence is incomplete
- **THEN** live provider qualification MUST remain blocked

#### Scenario: Contract publication is requested without F0 evidence
- **WHEN** the threat model is unaccepted or any mandatory F0 assertion is missing or failed
- **THEN** contract publication and annotated tagging MUST remain blocked, while parallel implementation MAY continue against the recorded provisional baseline

#### Scenario: Acceptance scenario lacks traceability
- **WHEN** the acceptance map omits a normative requirement or scenario or references missing evidence
- **THEN** avatar-client validation MUST fail and the owning implementation task MUST remain incomplete

#### Scenario: Emergency kill switch is activated
- **WHEN** an operator disables a model profile or all new session creation
- **THEN** the control API MUST enforce the selected scope immediately for new work and revoke affected active leases according to the recorded policy

