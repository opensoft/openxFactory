## Context

The avatar-first UI guidance defines a reusable shell, channel split, persona
contract, standard controls, and different defaults for Customer, Client, and
Domain Hermes. It does not yet define the production trust boundary between a
client, the session broker, Hermes, governed workflow services, and a realtime
provider. This change ratifies the neutral contract boundary only. F0
feasibility, the executable reference runtime, and UI-standard alignment are
independent sibling changes described by the
[parallel workstream plan](supporting-docs/avatar-client-parallel-workstream-plan.md).

Provider facts verified against OpenAI documentation on 2026-07-10:
[`gpt-realtime-2.1`](https://developers.openai.com/api/docs/models/gpt-realtime-2.1)
is a released API Realtime model. No `gpt-live-1` entry or supported API
contract was found in the public OpenAI developer documentation, so the name
is treated only as a disabled roadmap target. `POST /v1/realtime/calls`
creates a server-owned call from an SDP offer and accepts the full session
configuration (model, voice, instructions, tools, turn detection) atomically
in the create request. The
[WebRTC guide](https://developers.openai.com/api/docs/guides/realtime-webrtc)
and [server-control guide](https://developers.openai.com/api/docs/guides/realtime-server-controls)
show that the provider response yields the SDP answer and call ID, after which
a server sideband WebSocket can attach by call ID; the broker can therefore
hold the answer instead of forwarding it immediately. Voice is immutable after
the model first emits audio. Sessions are capped at 60 minutes. The model page
reports a 128,000-token context window and 32,000 maximum output tokens. With
VAD enabled, WebRTC and SIP automatically cancel an interrupted response and
truncate unplayed audio.
For WebRTC push-to-talk, the documented flow additionally requires
`input_audio_buffer.clear`, `input_audio_buffer.commit`, and `response.create`
around `response.cancel` and `output_audio_buffer.clear`; push-to-talk is
therefore outside this kernel's two-event client allowlist. The authenticated
call [hangup endpoint](https://developers.openai.com/api/docs/guides/realtime-sip#hang-up-the-call)
can terminate both SIP and WebRTC Realtime sessions by call ID. The
[VAD guide](https://developers.openai.com/api/docs/guides/realtime-vad#server-vad)
documents `server_vad` and its threshold, prefix-padding, silence-duration,
automatic-response, and interruption controls.

A seven-expert panel review (2026-07-10) confirmed the trust architecture and
found the draft over-specified for a one-maintainer team: redundant delivery
machinery, contracts without consumers, features without slices, gates
without users, and bindings to services that do not exist yet. The decisions
below record the simplified shape. Where a supporting document under
`supporting-docs/` disagrees with these decisions, the deltas and this design
are authoritative. The four files marked `superseded` are frozen historical
inputs; current `draft` and `record` files are non-normative review evidence.
The current contract review is made auditable by the registered
[threat model](supporting-docs/avatar-client-threat-model.md),
[F0 protocol](../qualify-avatar-brokered-call-feasibility/supporting-docs/f0-brokered-call-spike-protocol.md),
[acceptance map](supporting-docs/avatar-client-acceptance-map.yaml), and
[validation baseline](supporting-docs/pre-review-validation-baseline-2026-07-10.md).

### Terms

- **Logical session:** the user-facing xFactory conversation and workflow
  identity. It survives media reconnects.
- **Media leg:** one provider connection with a fixed provider, model, voice,
  and transport identity.
- **Media attempt:** one AVC-01 request ID bound to the SHA-256 fingerprint of
  one exact SDP offer; retries cannot substitute a different offer.
- **Client instance:** one running client application or browser tab.
- **Trusted client media adapter:** signed first-party code inside the media
  confidentiality trusted computing base for disclosure, local capture,
  answer application, playback, and the provider-event allowlist. It is not a
  policy or workflow authority.
- **Session epoch:** a broker-issued generation that fences prior grants,
  commands, and media legs after revocation or lease expiry.
- **Control lease:** an expiring server assertion that the client instance
  and media leg remain authorized, renewed through heartbeats.
- **State revision:** the sequence number of the last state-advancing
  authoritative event in the session log.
- **Command:** an untrusted client request for a state transition or action.
- **Event:** an immutable observation or authoritative result.
- **Snapshot:** a server-issued projection used to initialize or recover
  authoritative state.
- **Session result:** AVC-02, the sole serialized response to AVC-01, with a
  discriminated `grant`, `denial`, or `terminal` variant.
- **Media-authorization barrier:** the authoritative control event that permits
  provider-bound microphone transmission and provider playback only after the
  xFactory control lease and provider sideband are ready for the same session
  epoch and media leg.

### Ownership And Trust Boundaries

| Component | Owns | Must not own |
| --- | --- | --- |
| openxFactory contracts | Canonical AVC meaning, fixtures, compatibility, validation | Provider DTOs or client widget state |
| `implement-avatar-reference-runtime` sibling | Deterministic broker/control reference, authority stub, provider-adapter port shape, kill switches | Canonical contract meaning or production deployment |
| xfactory-avatar-client (successor) | Trusted local disclosure/media gating, UI, reducer, direct WebRTC peer, constrained data channel, platform adapters | Provider API keys, policy authority, tool execution, prompt/tool configuration |
| Hermes and workflow services | Policy, consent evidence, confirmation, approval, tool arguments, execution, records, handoff | Presentation-only client state |
| DomainxFactory | Persona catalog, language, speech-gate selection, retention overlay, consent-purpose mapping, handoff roles | Forked neutral protocol or media-consent evidence inside AVC |
| Voice provider | Media processing and provider session events under the approved profile | xFactory workflow authority |

The sibling reference runtime under `xfactory/avatar_runtime/` is
non-deployable code proving these contracts; the production deployment home,
topology, and operations are decided by `qualify-avatar-live-voice`. The
intended simplest topology is one broker deployment per domain deployment,
with one project-scoped provider key per deployment. Authenticated identity
for the internal-live ring uses a named concrete mechanism — an OIDC bearer
token validated by the broker for AVC-01 plus the per-session control
credential issued in AVC-02 — recorded in the threat model; full Hermes
identity integration is deferred. Body fields are references checked against
that server-derived context, never proof by themselves.

## Goals / Non-Goals

**Goals:**

- Define one domain-neutral protocol and deterministic state model for all
  xFactories, small enough to implement and test in weeks.
- Keep continuous media off the xFactory network path while retaining
  server-side session and tool control.
- Make retries, reconnects, duplicate delivery, revocation, and stale
  confirmations deterministic and safe with the minimal mechanism set.
- Keep provider and model identifiers out of widgets and neutral contracts.
- Enforce consent-before-capture, explicit speech gates, and record
  separation.
- Consume a real sibling F0 measurement before the contract release is
  published, without blocking parallel schema and fixture implementation.
- Preserve existing workflow-visualization and DomainxFactory ownership.

**Non-Goals:**

- Executing the F0 live API harness, implementing `xfactory/avatar_runtime/`,
  updating avatar-first UI assets, building the Flutter client, building the
  web operations console, or creating a production deployment in this change.
- Supporting a second provider before a real implementation requires it.
- Relaying or transcoding microphone/model audio through xFactory.
- Offline drafts, attachment byte paths, mid-session persona changes,
  seamless provider-context rollover, multi-device takeover, or the
  web-console handoff exchange protocol (each deferred to a named change).
- Full transcript, audio, video, or independent-transcription retention.
- Inventing a GPT-Live API contract before OpenAI publishes one.
- Selecting an aggregation gitlink path in this change.

## Decisions

### 1. Ratify an eight-contract kernel with shared definitions

The canonical family lives under `contracts/avatar-client/` as
YAML-serialized JSON Schema (draft 2020-12) files, one per contract, sharing
definitions through a single `shared-definitions.schema.yaml` referenced by
`$ref`, registered as entries in `contracts/manifest.yaml` and released under
the existing contract changelog policy:

```text
AVC-01 avatar_session_request     AVC-07 avatar_retention_profile
AVC-02 avatar_session_result      AVC-08 avatar_persona_profile
AVC-04 avatar_session_event       AVC-11 avatar_session_command
AVC-06 structured_confirmation    AVC-12 avatar_state_snapshot
```

AVC-03 (capabilities) is absorbed into AVC-02 as an inline `capabilities`
object — it was never transported standalone. AVC-05 (transcript segment) is
a registered AVC-04 event payload schema. AVC-09 (adapter descriptor) and
AVC-10 (latency sample) are deferred to `qualify-avatar-live-voice`; their
IDs stay reserved and are never reused. At realization, the release allocates
the next available minor `contract_bundle_version` after considering merge
order, updates the manifest and changelog atomically, and publishes an
annotated tag with the same version. Consumers pin the exact openxFactory
commit SHA plus per-file sha256 digests; the tag identifies the release but
does not replace content-addressed pins. Shared definitions cover IDs, actor
context, purpose, consent, trace, session epoch, media leg and attempt,
server-derived SDP-offer fingerprint, state revision, last-event sequence,
media authorization, session outcomes, retention class, redaction, and the
retry-equivalence rule.

### 2. Keep authoritative state axes orthogonal; presentation stays local

Four axes cross the wire and appear in AVC-12: session lifecycle
(broker-owned), control health (lease-derived), media state (adapter
observations), and workflow projection (authority-stub/Hermes-owned).
Presentation mode (`conversation`, `work`, `review`) is client-local UI
state; snapshots may carry client presentation preferences but never treat
them as authoritative. The transition registry declares allowed
predecessors, terminal states, authority source, and recovery behavior.
Widgets render projections and cannot author lifecycle or workflow
transitions.

### 3. Broker the provider call atomically; attach sideband before answer use

For production OpenAI sessions:

1. The client obtains microphone permission only after disclosure and
   applicable consent, and creates the offer with no provider-bound microphone
   audio enabled.
2. The client creates a WebRTC offer and submits it inside AVC-01 (a
   transient, never-persisted `sdp_offer` field) over the authenticated broker
   channel. The broker computes an exact-byte SHA-256 offer fingerprint before
   discarding the body.
3. The broker validates identity, client, subject, purpose, consent,
   persona, policy, retention, model profile, quota, and kill switches.
4. The broker calls `POST /v1/realtime/calls` with its server-held key and
   the full server-owned session configuration (model, voice, instructions,
   safety, turn detection, tools) in the create request.
5. The provider response yields the SDP answer and call ID. The broker holds
   the answer, attaches the call-ID-bound sideband WebSocket, and verifies the
   configured session. It never releases an answer before sideband readiness.
6. After sideband readiness, the broker returns the AVC-02 `grant` variant with
   the held answer and authenticated xFactory WSS descriptor. The trusted
   client media adapter verifies the offer fingerprint but does not apply the
   answer yet.
7. The client establishes WSS and sends `lease_ack` with the grant, logical
   session, epoch, media leg, client instance, and last-applied event sequence.
   The broker emits authoritative `media_authorized` only after validating the
   acknowledgement against transport identity and the verified sideband.
8. Only after applying that exact event does the trusted media adapter apply
   the answer and enable provider-bound audio and playback. The conforming path
   therefore exposes neither user audio nor provider output before both
   control channels are ready.
9. The readiness timer starts when the provider create response is accepted.
   Profiles default to 3,000 milliseconds and may select 1,000 through 5,000
   milliseconds; no profile may exceed the 5,000-millisecond neutral ceiling.
   If sideband or WSS acknowledgement misses the deadline, the broker revokes
   the attempt, terminates the provider leg, and returns the AVC-02
   `media_readiness_timeout` denial. The client discards the unapplied answer.
   The OpenAI adapter terminates through
   `POST /v1/realtime/calls/{call_id}/hangup`, which applies to WebRTC calls.
10. After authorization, media flows directly between client and provider;
    the broker stays on control only.

This intentionally adds sideband-attach latency before answer release and
measures it in F0. The trusted adapter is part of the confidentiality boundary;
all commands and provider events remain untrusted for workflow authority. A
modified client that applies the answer early or bypasses its media allowlist is
a compromised-client incident: sideband can detect and terminate it but cannot
retroactively prevent audio disclosure. Pre-authorization provider events stay
non-authoritative, server tool handling rejects them, and no client bypass can
create an external operation or authoritative transition. The threat model
records this residual risk explicitly.

Standard provider keys never leave the server:
each environment uses a distinct project-scoped key held only in deployment
secret storage, with a documented manual rotation procedure required before
internal live. Ephemeral client-token setup is permitted only in a
non-consequential lab profile with tools disabled and no tenant data.

### 4. Bind typed session results to identity, purpose, instance, epoch, and
lease

AVC-01 carries a request idempotency key, client instance and app version,
workflow and purpose references, requested capability profile, contract
compatibility, persona, language, platform, accessibility preferences,
consent/profile versions, and the transient SDP offer. A resume also carries
logical session, epoch, and last-applied event sequence. Every response is
AVC-02 with `result_kind` equal to `grant`, `denial`, or `terminal` and common
request, attempt, safe-message, retry, and fallback fields. Only `grant` may
contain grant/logical-session/epoch/media-leg identity, resolved policy and
capabilities, the server-derived offer fingerprint and offer-bound SDP answer,
the authenticated control-channel descriptor, heartbeat interval, lease
expiry, initial media-authorization state, and initial AVC-12 snapshot. The
client compares that fingerprint with its current local offer before using the
grant and waits for `media_authorized` before applying the answer.

The denial/terminal reason registry is closed and versioned. It contains
`identity_denied`, `consent_missing`, `policy_denied`,
`contract_incompatible`, `profile_disabled`,
`interaction_mode_unsupported`, `quota_blocked`,
`second_instance_denied`, `idempotency_conflict`,
`media_readiness_timeout`, `provider_unavailable`, `grant_consumed`,
`attempt_expired`, `attempt_abandoned`, and `attempt_revoked`. Non-grant
variants carry no SDP or credential. They declare `retryable`, optional bounded
`retry_after_ms`, approved `fallback_modes` from `text`, `human_handoff`,
`retry_later`, `upgrade_required`, or `none`, and a localization-safe message
key; raw provider errors never cross this contract.

`request_id` identifies one media attempt, not an indefinitely reusable
logical-session request. The broker computes `sdp_offer_sha256` from the exact
offer bytes and includes that server-derived fingerprint in retry equivalence;
only client-observed timestamps remain volatile. A retry from the same
authenticated actor and client instance is equivalent only when all
non-volatile fields and the offer fingerprint match. While the attempt is
`pending`, an equivalent retry receives the same unconsumed, unexpired grant
and offer-bound answer without creating another provider call. Reusing the
request ID with another offer or any changed non-volatile field returns an
AVC-02 `denial` with `idempotency_conflict` and never returns the old answer.

The exact pending grant, including its answer and scoped control credential,
lives only in a secret-classified, TTL-bounded ephemeral retry cache. The
reference runtime keeps it in process memory only. Any production shared cache
must encrypt it in transit and at rest and disable disk persistence, snapshots,
and backups. The cache is excluded from durable records, logs, telemetry,
crash reports, and support bundles, and is destroyed when the attempt becomes
`connected`, `abandoned`, `expired`, or `revoked`. A durable terminal
idempotency record may retain request ID, offer fingerprint, context references,
status, and a credential-free AVC-02 denial or terminal result. It never
retains SDP, an SDP answer, or a credential.

After first successful media connection, an equivalent retry receives the
AVC-02 `terminal` result `grant_consumed`. A client needing a regenerated offer uses a
fresh request ID plus the authorized logical-session/epoch resume reference;
the broker first terminates and marks any prior pending attempt `abandoned`,
then may issue a fresh media leg under the same active logical session. One
client instance holds the lease and at most one pending or connected media leg
exists per logical session. A concurrent request from another instance is
denied. Policy-gated takeover is deferred; the epoch mechanism stays because
revocation and lease expiry still fence stale grants, commands, and legs.

### 5. Separate commands, events, and snapshots over one sequenced log

AVC-11 is the only client-to-control mutation envelope: `command_id`,
command type, session and epoch, registry-declared payload, and client time.
The control API derives actor authority from transport, validates lease,
epoch, and command allowlist, and returns canonical accepted, rejected,
duplicate, conflict, or expired events. `command_id` is the idempotency key;
retries reuse it and receive the recorded result from a server dedupe table.
`expected_state_revision` is required only on command types the registry
flags as revision-guarded (value edits, workflow submissions); confirmation
decisions bind through AVC-06 instead; media and presentation commands omit
it.

AVC-04 is immutable and classifies every event as `observation` or
`authoritative` with registry-declared producers. Client and provider
sources may emit only registered observations; only the broker, the
authority stub (later Hermes/workflow), or an accountable human emits
authoritative results. Each session has ONE authoritative event log: the
control API is the sole sequencer, assigns a monotonic sequence at append
time, and `state_revision` equals the sequence of the last state-advancing
event. AVC-12 separately carries `last_event_sequence`, the sequence through
which the snapshot was projected. `state_revision` guards state-changing
commands; it is never the stream cursor.

There are no event hash chains, snapshot integrity digests, or historical
replay protocol. On any detected gap, conflict, or reconnect, the control WSS
establishes a snapshot barrier at event sequence `B`, projects AVC-12 through
`B` with `last_event_sequence=B`, and buffers events appended after `B` while
the snapshot is sent. The snapshot is the first recovery frame, followed by
the bounded buffer in sequence and then live push. The client discards local
events at or below `last_event_sequence` and requires the next event to be
`B+1`. If the handoff buffer overflows or the next sequence is not `B+1`, the
server and client abandon that handoff and establish a newer barrier rather
than guessing or partially replaying history. The client reports its
last-applied event sequence in heartbeats and resume requests.

### 6. Make the control channel authoritative and leased, with a real protocol

The control transport is authenticated WSS carrying commands, events,
snapshots, heartbeats, and revocation. The client sends a heartbeat every
`heartbeat_interval_ms` carrying session epoch and last-applied sequence;
each server response extends the lease and returns the new
`lease_expires_at`, and may carry a fresh scoped reconnect credential bound
to session, epoch, and client instance. `media_readiness_timeout_ms` defaults
to 3,000, MUST be between 1,000 and 5,000, and starts when the provider create
response is accepted; missing the deadline yields the AVC-02 denial
`media_readiness_timeout` and provider hangup. For every media-capable profile,
`heartbeat_interval_ms` is greater than zero and no more than 5,000, and the
initial lease expires no more than 10,000 milliseconds after grant issuance.
Each successful heartbeat response may extend expiry to at most 10,000
milliseconds after that response. A profile may choose stricter values but
cannot raise either neutral ceiling. Control health is `degraded` after one
missed response and `lost` after the profile-declared count or lease expiry,
whichever occurs first. A dropped WSS reconnects with the newest credential
while the lease remains valid; otherwise the client starts over with AVC-01.
Control loss immediately disables governed commands and stops capture and
playback — there is no speech grace interval. Lease expiry always closes the
media leg even when provider connectivity is healthy. Command results are the
acknowledgement; there are no per-message acks.

### 7. Keep provider configuration and tools server-only

The server adapter owns model, voice, prompt version, instructions, safety
configuration, turn detection, tool definitions, and sideband tool responses.
The neutral interaction mode is `provider_vad`; exact provider turn detection
belongs only to the server profile. The F0 OpenAI profile pins `server_vad`
with threshold `0.5`, `prefix_padding_ms=300`,
`silence_duration_ms=500`, `create_response=true`, and
`interrupt_response=true`. A changed `server_vad` configuration or a
`semantic_vad` profile requires its own qualification evidence but no widget
branch. The client data-channel adapter exposes no generic send: its complete
outbound allowlist is
`response.cancel` and `output_audio_buffer.clear`, used only for explicit
stop/cancel behavior. Ordinary VAD interruption is provider-managed.
`input_audio_buffer.clear`, `input_audio_buffer.commit`, `response.create`,
`conversation.item.truncate`, and all configuration, text, tool, and privilege
events are excluded. A request for push-to-talk fails preflight into text or
human fallback until a successor change defines its expanded event surface.
User text, structured actions, and confirmation decisions travel through
AVC-11.

Until Hermes integration lands, the reference broker exercises consent,
policy, tool, and confirmation authority through server-side fail-closed
ports: a static policy bundle, a consent-authority fixture adapter, and one
reference intake workflow handler. The neutral consent-purpose registry
contains `avatar.media_capture`, `avatar.provider_processing`, and
`avatar.structured_record`. AVC carries only the consent record reference,
version, and required purpose IDs. Domain consent authorities own evidence,
legal basis, withdrawal, and stricter purpose IDs; a memory-gateway consent
profile may be one adapter but is not the neutral media-consent contract. The
stub is server-side and fail-closed,
so replacing it with real Hermes APIs (in `avatar-pilot-hardening`) tightens
rather than changes the protocol. Provider tool calls remain untrusted
intent evidence; the stub validates purpose, consent, state, and
confirmation binding, and owns the stable external operation idempotency
key.

### 8. Bind confirmation to the exact proposed effect without digests

AVC-06 is a server-issued challenge carrying confirmation ID and version,
action or field scope, display-safe fields, normalized effect summary, risk
class, policy and consent versions, expiry, and the issuing state revision.
The client decision returns only confirmation ID, version, decision, and
`command_id`; actor identity comes from authenticated context. The server
rejects decisions against expired, superseded, or version-mismatched
challenges, and any material input or effect change supersedes the challenge
and requires a new confirmation. Binding digests are dropped: a server-issued
opaque digest echoed by the client proves nothing beyond ID plus version,
and cross-language canonical serialization was the single most expensive
validator obligation in the draft. Transcript text and silence never satisfy
confirmation.

### 9. Recover the logical session with bounded context continuity

A provider disconnect creates a new media leg under the same logical session
only while the lease is valid. Recovery is snapshot-based (Decision 5), and
pending consequential commands reconcile by `command_id` before any retry. A
reconnected or resumed media leg is rehydrated from server-owned
configuration plus a default ephemeral same-session context carryover — a
bounded recent-turns summary permitted within the same logical session and
purpose — so an ordinary network drop does not produce an assistant with
amnesia. Full-transcript carryover and any cross-purpose reuse remain
policy-gated and out of scope. Session duration is capped by profile below
the provider's ~60-minute limit; reaching a duration or context limit
reconciles pending commands, snapshots, and ends the leg in an explicit
`session_limit_reached` resume state. Seamless mid-conversation rollover is
deferred. Terminal, revoked, expired, completed, and abandoned sessions
never resume as active.

### 10. Fix persona per session and voice per media leg

Persona is selected at session start from the domain catalog and stays fixed
for the logical session; changing persona ends the session and starts a new
one. Voice is fixed per media leg (OpenAI freezes voice after first audio;
the before-first-audio window is a server-adapter detail). Model and profile
promotion is server configuration: human-approved, new-session-only, with
requested and provider-resolved model recorded per session. This kernel names
`gpt-realtime-2.1` only as the F0 candidate; it defines no qualified live
profile, so internal-live and production voice remain disabled until
`qualify-avatar-live-voice` records promotion evidence. Once a qualified
profile exists, rollback selects the last qualified profile; without one,
rollback disables voice and offers text or handoff. A running media leg never
silently changes model, voice, or adapter. Mid-session persona rotation UI and
its media-leg choreography are deferred.

### 11. Select speech gates by policy; implement two, reserve one

The resolved domain/client profile — never the user request — selects the
speech gate. `confirmation_before_action` is the default and holds all
consequential actions behind AVC-06. `streaming_monitor` is permitted for
response classes whose policy accepts that speech may reach the user before
review. `pre_speech_review` remains a reserved enum value in this kernel:
selecting it fails preflight into text or human fallback, and its reviewed
speech pipeline is deferred to the change that onboards the first high-risk
domain. An adapter that cannot satisfy the required gate fails preflight
rather than weakening policy.

Disclosure and current authorization for `avatar.media_capture` and
`avatar.provider_processing` are required before capture or provider session
creation; `avatar.structured_record` is additionally required before a
structured workflow record is retained. Consent
withdrawal through the client stops local capture and playback before the
withdrawal command is sent. Withdrawal through any channel revokes the lease,
cancels output, terminates the media leg, and prevents new retention. When the
broker learns that a bound consent version is no longer valid, it immediately
marks the lease revoked, pushes the authoritative revocation event, and invokes
the provider adapter's termination operation (the OpenAI adapter uses
`POST /v1/realtime/calls/{call_id}/hangup`). Provider-bound input and output
must cease no more than 5,000 milliseconds after the broker learns of the
invalidation; a provider profile that cannot prove that termination bound is
not eligible for media authorization. The next heartbeat is a fallback
delivery path, not the definition of the deadline.

### 12. Scope retention to the minimum and persist nothing locally

AVC-07 distinguishes ephemeral presentation, operational telemetry, and
structured workflow records. Captions, partial transcripts, SDP, provider
payloads, and credentials are ephemeral by definition. Structured
confirmation decisions, consent versions, approvals, tool outcomes, and
final workflow outcomes are retained under their policy. Full transcript,
audio, video, and independent transcription are reserved classes: forbidden
in this kernel, ratifiable only by a successor change (the hole stays closed,
not unspecified). Offline drafts are deferred entirely; the client persists
no sensitive session data locally, which also removes the platform-crypto,
key-destruction, and draft-sync obligations. The online stale-revision rule
(conflicting command enters review mode) covers the conflict UX the drafts
needed.

### 13. Meter usage and keep two kill switches

Every media leg emits a usage record attributed to client and workflow
references. Profiles declare per-tenant maximum concurrent sessions and
maximum session duration; provider capacity, rate-limit, and budget failures
map to the AVC-02 `denial` reason `quota_blocked`. Two server kill switches exist: all new
session creation, and per model profile — each with optional revocation of
active leases. Finer-grained switch scopes (media, tools, retention, drafts)
are deferred with the features they would govern.

### 14. Constrain the deterministic client interface (consumed by siblings)

The client (built in `implement-avatar-client-lab`) separates generated or
hand-written contract models, a pure reducer, use-case ports (session
control, media, clock, IDs, telemetry), and adapters (deterministic fixture,
WSS control, provider WebRTC, platform). Widgets receive immutable view
state, emit typed intents, and never parse provider DTOs or perform policy
checks. The deterministic fixture adapter and the live adapter drive the
same reducer contracts. Client models prove contract compatibility by
executing the canonical fixture suite in client CI — fixture conformance is
the drift protection; code generation is an optional implementation choice,
not a requirement.

### 15. Define safe-rendering and handoff constraints for UI consumers

Transcript, model text, tool summaries, attachment names, and link labels
are untrusted: plain text or a narrow sanitized subset, URI and destination
allowlists, no provider-supplied widgets. Two web-console handoff invariants
ratify now: handoff URLs never carry bearer tokens, subject identifiers,
transcripts, or provider secrets; and any future exchange must be
server-issued, one-time, and reauthorized at the web boundary. The exchange
protocol itself is deferred until the web console exists.

### 16. Define accessibility evidence expected from UI consumers

Windows desktop is the accessibility-qualified surface for the client
kernel: keyboard-only operation, visible focus, screen-reader labels and
announcements, captions, text-only mode, reduced motion, non-color status
cues, and zoom/reflow. The Flutter web surface must be screen-reader
operable with a documented WCAG 2.2 AA exception register; the full web
WCAG audit moves to the web-console change or the pilot gate (canvas-rendered
Flutter web cannot honestly pass it today). The qualified locale set is
English plus a pseudo-locale fixture that covers long-string and
bidirectional rendering; real localization is a successor change. Golden
tests render on one pinned CI platform with one bundled font family
(including an RTL-capable face); high-contrast, reduced-motion, and
text-only verification uses semantics assertions rather than pixel goldens.

## Risks / Trade-offs

- **Sideband-before-answer adds latency** -> the feasibility sibling measures
  the readiness thresholds before contract publication; the answer is held
  only until the call-ID-bound sideband is verified.
- **A compromised client bypasses local media controls** -> the first-party
  adapter is explicitly in the confidentiality TCB; sideband termination is
  detection and containment, while all provider events remain non-authoritative
  for workflow effects.
- **A retry regenerates its SDP offer** -> the server-derived offer fingerprint
  is part of retry equivalence; a changed offer under the same request ID fails
  closed, and a new attempt uses a new request ID.
- **Authority stub could drift from real Hermes** -> the stub is
  server-side, fail-closed, and behind the same AVC-04/AVC-06 authority
  registry Hermes will use; integration replaces the implementation, not the
  protocol.
- **Provider API churn** -> provider DTOs stay in the server adapter; pinned
  model profile; unknown consequential semantics fail closed.
- **WSS loss while WebRTC stays up** -> immediate stop of governed commands
  and media; expiring lease enforced on both sides.
- **Duplicate or reordered delivery** -> command-id dedupe, single sequenced
  log, and an atomic snapshot-to-live barrier using `last_event_sequence`.
- **Consent changes while control is impaired** -> immediate push and provider
  termination, a five-second revocation ceiling, and a ten-second maximum
  client lease lifetime after its last successful heartbeat.
- **Reconnect amnesia** -> bounded ephemeral same-session carryover, without
  opening full-transcript retention.
- **Deferred features leave gaps** -> each deferral keeps a closed default
  (drafts disabled, attachments reference-only, second instance denied,
  reserved gate fails preflight) rather than unspecified behavior.

## Validation Ownership

Review completion requires strict target and all-item OpenSpec validation,
the realized avatar-client validator, acceptance-map/spec parity, contract
release consistency, supporting-document hashes, and `git diff --check`.
Installed DomainxFactory validators are compatibility observations: any
regression from this change is blocking, while a dated pre-existing failure
remains owned by that domain. The external baseline record names the current
failures so task 4.3 cannot silently absorb unrelated remediation. F0,
reference-runtime, and UI evidence remain owned by their sibling changes.

## Migration Plan

1. Ratify the threat model and parallel interface baseline. The F0 sibling,
   reference-runtime sibling, and UI-standard sibling may begin concurrently.
2. Implement shared definitions, the eight AVC schemas, registries,
   fixtures, and the schema+fixture validator; register the family in
   `contracts/manifest.yaml` without reserving a release number early.
3. Consume the F0 `PASS` result and disposition every interface variance. A
   correction is made only in this change and is published to siblings through
   the interface-lock handoff.
4. Allocate the next available minor version, update manifest, changelog, and
   README atomically, publish the matching annotated tag from the realized
   release commit, and publish exact digests for sibling pins.
5. Validate strict and archive only after the released contract surface and
   handoff evidence are green.

Rollback before publication is deleting the unreleased contracts. After
publication, rollback is a new additive or breaking contract release under the
versioning policy; sibling implementations carry their own rollback duties.

## Open Questions

- The avatar renderer and Flutter media/storage package selections move to
  `implement-avatar-client-lab` (a one-page ADR each; static per-state
  assets are acceptable for the deterministic lab).
- The production deployment home and per-domain topology are decided by
  `qualify-avatar-live-voice`, consistent with repo-boundary-governance
  routing runtime operations to install repositories.
- GPT-Live transport and event semantics remain unknown until OpenAI
  publishes an API contract; nothing here blocks the Realtime 2.1 adapter.
