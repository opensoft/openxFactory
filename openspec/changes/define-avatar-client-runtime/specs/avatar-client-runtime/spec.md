# avatar-client-runtime Specification

## ADDED Requirements

### Requirement: Versioned neutral avatar-client contract kernel
openxFactory SHALL publish the avatar-client contract kernel under
`contracts/avatar-client/` as YAML-serialized JSON Schema (draft 2020-12)
files: AVC-01 avatar session request, AVC-02 avatar session grant (with
resolved runtime capabilities inline), AVC-04 avatar session event (with
transcript segments as a registered payload schema), AVC-06 structured
confirmation, AVC-07 avatar retention profile, AVC-08 avatar persona profile,
AVC-11 avatar session command, and AVC-12 avatar state snapshot. AVC-03 and
AVC-05 are absorbed as described; AVC-09 and AVC-10 remain reserved for the
live-qualification successor change and their identifiers are never reused.

Every contract SHALL declare its contract ID and `contract_schema_version`,
share definitions through a single `shared-definitions.schema.yaml`
referenced by `$ref`, and register in `contracts/manifest.yaml` under the
repository contract changelog policy. Consumers SHALL pin an openxFactory
commit and per-file digest. Shared definitions SHALL cover actor, client,
subject, workflow purpose, consent version, trace, session epoch, media leg,
state revision, retention class, redaction, and the retry-equivalence rule
(canonical-form equality excluding declared volatile fields). Provider DTOs,
model identifiers, client widget state, and secrets MUST NOT be required
neutral fields.

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

### Requirement: Authenticated, purpose-bound session grants
The session broker SHALL authenticate the caller through trusted transport
context and SHALL derive client/tenant, actor, subject, representative
authority, and permission scope server-side. Client-authored body fields
MUST NOT serve as proof of identity, consent, or authority.

AVC-01 SHALL carry a request idempotency key, client instance and app
version, workflow and purpose references, requested capability profile,
contract compatibility, persona, language, platform, accessibility
preferences, consent and profile versions, a transient never-persisted SDP
offer, and, on resume, the last-applied event sequence. AVC-02 SHALL bind
grant, logical session, session epoch, and media-leg identity, the resolved
policy and capability set, the SDP answer, an authenticated control-channel
descriptor, heartbeat interval, lease expiry, and the initial AVC-12
snapshot. Provider and control endpoints SHALL come from server allowlists;
credentials SHALL be short-lived, scoped, excluded from URLs, and absent
from persisted records, logs, and telemetry.

The broker SHALL persist each issued grant keyed by authenticated actor and
request ID and SHALL redeliver it verbatim to the same client instance until
first successful media connect or grant expiry; after consumption or expiry
a retry SHALL receive a canonical terminal result, and a retry whose prior
call never connected MAY receive a fresh media leg under the same logical
session. One client instance SHALL hold the lease and one media leg SHALL be
active per logical session; a concurrent request from another instance SHALL
be denied with a canonical result (policy-gated takeover is deferred).

Profiles SHALL declare per-tenant maximum concurrent sessions and maximum
session duration. Every media leg SHALL emit a usage record attributed to
client and workflow references, and provider capacity, rate-limit, and
budget failures SHALL map to one canonical blocked result.

#### Scenario: Authorized session is granted
- **WHEN** authenticated identity, purpose, consent, persona, policy, retention, contract compatibility, quota, and kill-switch checks all pass
- **THEN** the broker MUST issue one bounded grant and initial authoritative snapshot bound to the verified context

#### Scenario: Body identity is forged
- **WHEN** AVC-01 references an actor, subject, client, consent, or workflow scope not authorized by transport identity
- **THEN** the broker MUST deny the request before creating a provider call or control lease

#### Scenario: Session request is retried after a lost response
- **WHEN** the same authenticated request ID is retried equivalently while the issued grant remains unconsumed and unexpired
- **THEN** the broker MUST redeliver the recorded grant to the same client instance and MUST NOT create a second billable provider call

#### Scenario: A second client instance requests the active session
- **WHEN** a concurrent AVC-01 arrives from a different client instance for a logical session with an active lease
- **THEN** the broker MUST deny it with a canonical result and MUST NOT revoke the active grant

#### Scenario: Tenant quota is exhausted
- **WHEN** a request would exceed the profile's per-tenant concurrent-session cap or a provider capacity limit is reported
- **THEN** the broker MUST return the canonical blocked result and record the attributed usage outcome

### Requirement: Brokered direct media with sideband control
The production OpenAI profile SHALL use brokered call creation: the
openxFactory server adapter calls the provider call-creation endpoint with a
server-held project-scoped key and the full server-owned session
configuration (model, voice, instructions, safety, turn detection, tools)
atomically in the create request, releases the SDP answer to the client
immediately, and attaches the authenticated sideband controller in parallel.
Tool intents and consequential responses SHALL remain blocked until sideband
control is attached and verified; if attach fails within the profile bound,
the broker SHALL revoke the media leg and return a canonical blocked or
fallback result.

After SDP negotiation, encrypted realtime media SHALL flow directly between
the client and the approved provider; xFactory MUST NOT relay or transcode
the continuous media path. Standard provider keys MUST NOT reach the client.
Each deployment environment SHALL use a distinct project-scoped provider key
held only in deployment secret storage, and a documented manual rotation
procedure SHALL exist before internal live use. Ephemeral-token setup SHALL
be limited to a non-consequential lab profile with tools disabled, approved
test data, and no production tenant access.

The client provider data channel SHALL expose a typed allowlist whose
complete outbound set is `response.cancel` and `output_audio_buffer.clear`.
It MUST NOT expose generic provider JSON send, session updates,
conversation or user text, instructions, tool definitions, function
outputs, item truncation, or privilege-bearing provider events. User text,
attachment references, confirmations, and governed actions SHALL use AVC-11
over the control channel.

#### Scenario: Production OpenAI call starts
- **WHEN** the broker creates a production OpenAI media leg
- **THEN** the full session configuration MUST be applied in the create request and the SDP answer released without waiting on sideband attach
- **AND** tool intents and consequential responses MUST remain blocked until the sideband controller is attached and verified

#### Scenario: Sideband does not become ready
- **WHEN** the sideband controller cannot attach or verify within the profile bound
- **THEN** the broker MUST revoke the media leg and return a canonical blocked or fallback result

#### Scenario: Client attempts provider reconfiguration
- **WHEN** client code attempts to send a provider event outside the enumerated allowlist
- **THEN** the constrained adapter MUST reject the operation locally and security telemetry MUST record a redacted violation

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
append time; state revision SHALL equal the sequence of the last
state-advancing event. Recovery SHALL be snapshot-based: on any detected
gap, conflict, or reconnect the client fetches AVC-12, discards buffered
events at or below the snapshot revision, and resumes from live push. Event
hash chains, snapshot integrity digests, and replay protocols MUST NOT be
required by the kernel contracts.

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
- **THEN** it MUST stop consequential transitions, fetch AVC-12, discard events at or below the snapshot revision, and resume in order

#### Scenario: Client reports a tool completed
- **WHEN** a client or provider observation claims approval, execution, tool completion, workflow completion, or consent
- **THEN** the event validator MUST reject it as an unauthorized producer and MUST NOT advance authoritative state

### Requirement: Leased control channel and deterministic recovery
The control transport SHALL be authenticated WSS carrying commands, events,
snapshots, heartbeats, and revocation. The client SHALL send a heartbeat
every declared interval carrying session epoch and last-applied sequence;
each server heartbeat response SHALL extend the lease, return the new lease
expiry, and MAY carry a fresh scoped reconnect credential bound to session,
epoch, and client instance. Control health SHALL be degraded after one
missed response and lost after the profile-declared count, evaluated against
the client's monotonic clock. Command results serve as acknowledgements;
per-message acknowledgement frames MUST NOT be required.

Loss of control SHALL immediately disable governed commands and pending
confirmations and stop capture and playback; there is no speech grace
interval. Lease expiry SHALL close the media leg even while provider
connectivity remains healthy. A dropped control connection SHALL reconnect
with the newest reconnect credential while the lease remains valid;
otherwise the client starts over with AVC-01.

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

#### Scenario: Control connection drops transiently
- **WHEN** the WSS drops while the lease remains valid
- **THEN** the client MUST reconnect with the newest scoped reconnect credential and resume from its last-applied sequence via snapshot recovery

#### Scenario: Pending action exists during reconnect
- **WHEN** a disconnect occurs after command acceptance but before its outcome is displayed
- **THEN** recovery MUST query the recorded command result by command ID and MUST NOT issue a new external action

#### Scenario: User pauses and resumes
- **WHEN** a non-terminal session is paused and resumed within policy limits
- **THEN** capture and playback MUST stop while paused and resume from an authoritative snapshot without creating a second workflow

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
requested and provider-resolved model per session, with rollback to the last
qualified profile. The first qualified profile is `gpt-realtime-2.1`; all
other profiles, including `gpt-live-1`, remain disabled pending their own
qualification. A running media leg MUST NOT silently change model, voice,
adapter, or immutable provider configuration.

Persona SHALL be selected at session start from the domain catalog and
remain fixed for the logical session; changing persona SHALL end the session
and start a new one. Voice SHALL be fixed per media leg. Mid-session persona
rotation is deferred.

#### Scenario: Qualified default model changes
- **WHEN** a new provider profile passes promotion
- **THEN** new sessions MUST use the approved profile without model-name branches in client widgets or neutral reducers

#### Scenario: Future model lacks API support
- **WHEN** a target model has no supported deployment API or required control behavior
- **THEN** its profile MUST remain disabled and the last qualified profile MUST remain active

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

Disclosure, media purpose, provider processing authorization, and applicable
retention consent SHALL be current before microphone capture or provider
session creation. Consent withdrawal through any channel SHALL stop capture,
cancel output, revoke the media leg, and prevent new retention; when the
broker learns that a consent version bound to an active grant is no longer
valid, it SHALL revoke the lease no later than the next heartbeat interval.

#### Scenario: User has not completed media disclosure
- **WHEN** required disclosure or provider-processing consent is absent, stale, or outside the workflow purpose
- **THEN** the broker MUST NOT create a provider call and the client MUST keep microphone capture off

#### Scenario: Policy requires the reserved gate
- **WHEN** a response class resolves to `pre_speech_review` under this kernel
- **THEN** preflight MUST fail into the approved text or human-handoff fallback and MUST NOT stream unreviewed audio for that class

#### Scenario: Consent is withdrawn during speech
- **WHEN** a valid consent-withdrawal command is accepted
- **THEN** the client and broker MUST stop capture and output and revoke the active media leg before further provider input is sent

#### Scenario: Consent is invalidated server-side
- **WHEN** the broker learns a bound consent version is no longer valid through any non-client channel
- **THEN** it MUST revoke the lease and close the media leg no later than the next heartbeat interval

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
until deterministic acceptance passes. Every acceptance scenario SHALL map
to automated evidence, manual evidence, or both.

Two server kill switches SHALL exist — all new session creation, and per
model profile — each with optional revocation of active leases. Rollback
SHALL stop new sessions on the withdrawn profile, revoke affected active
leases when safety requires it, and preserve only policy-required records.

#### Scenario: Live qualification begins early
- **WHEN** deterministic-lab evidence is incomplete
- **THEN** live provider qualification MUST remain blocked

#### Scenario: Emergency kill switch is activated
- **WHEN** an operator disables a model profile or all new session creation
- **THEN** the control API MUST enforce the selected scope immediately for new work and revoke affected active leases according to the recorded policy
