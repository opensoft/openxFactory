## Context

The avatar-first UI guidance defines a reusable shell, channel split, persona
contract, standard controls, and different defaults for Customer, Client, and
Domain Hermes. It does not yet define the production trust boundary between a
client, the session broker, Hermes, governed workflow services, and a realtime
provider. This change ratifies that boundary and realizes its smallest
provable kernel inside openxFactory.

Provider facts verified against OpenAI documentation on 2026-07-10:
`gpt-realtime-2.1` is a released API Realtime model; `gpt-live-1` is
ChatGPT-only with no API contract. `POST /v1/realtime/calls` creates a
server-owned call from an SDP offer and accepts the full session
configuration (model, voice, instructions, tools, turn detection) atomically
in the create request. A server sideband WebSocket can attach to the call by
call ID. Voice is immutable after the model first emits audio. Sessions are
capped near 60 minutes and ~28.7k input tokens with configurable
auto-truncation. In WebRTC mode the interruption pair is `response.cancel`
plus `output_audio_buffer.clear`, and server VAD auto-truncates unplayed
audio on user interruption.

A seven-expert panel review (2026-07-10) confirmed the trust architecture and
found the draft over-specified for a one-maintainer team: redundant delivery
machinery, contracts without consumers, features without slices, gates
without users, and bindings to services that do not exist yet. The decisions
below record the simplified shape. Where a supporting document under
`supporting-docs/` disagrees with these decisions, the deltas and this design
are authoritative; the supporting documents are frozen non-normative inputs.

### Terms

- **Logical session:** the user-facing xFactory conversation and workflow
  identity. It survives media reconnects.
- **Media leg:** one provider connection with a fixed provider, model, voice,
  and transport identity.
- **Client instance:** one running client application or browser tab.
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

### Ownership And Trust Boundaries

| Component | Owns | Must not own |
| --- | --- | --- |
| openxFactory contracts | Canonical AVC meaning, fixtures, compatibility, validation | Provider DTOs or client widget state |
| openxFactory reference runtime | Deterministic broker/control reference, authority stub, OpenAI server adapter shape, kill switches | Production deployment (successor change) |
| xfactory-avatar-client (successor) | Client UI, reducer, direct WebRTC peer, constrained data channel, platform adapters | Provider API keys, policy authority, tool execution, prompt/tool configuration |
| Hermes and workflow services | Policy, consent, confirmation, approval, tool arguments, execution, records, handoff | Presentation-only client state |
| DomainxFactory | Persona catalog, language, speech-gate selection, retention overlay, consent purposes, handoff roles | Forked neutral protocol |
| Voice provider | Media processing and provider session events under the approved profile | xFactory workflow authority |

The reference runtime under `xfactory/avatar_runtime/` is non-deployable
reference code proving the contracts; the production deployment home,
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
- De-risk the brokered-call architecture with a real measurement before the
  contracts freeze.
- Preserve existing workflow-visualization and DomainxFactory ownership.

**Non-Goals:**

- Building the Flutter client, the web operations console, or any production
  deployment in this change (successor changes).
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
AVC-02 avatar_session_grant       AVC-08 avatar_persona_profile
AVC-04 avatar_session_event       AVC-11 avatar_session_command
AVC-06 structured_confirmation    AVC-12 avatar_state_snapshot
```

AVC-03 (capabilities) is absorbed into AVC-02 as an inline `capabilities`
object — it was never transported standalone. AVC-05 (transcript segment) is
a registered AVC-04 event payload schema. AVC-09 (adapter descriptor) and
AVC-10 (latency sample) are deferred to `qualify-avatar-live-voice`; their
IDs stay reserved and are never reused. Consumers pin an openxFactory commit
SHA plus per-file sha256 digests (the repository has no tag-based releases;
the existing `contract_bundle_version` registers the family). Shared
definitions cover IDs, actor context, purpose, consent, trace, session epoch,
media leg, state revision, retention class, redaction, and the
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

### 3. Broker the provider call atomically; gate consequences, not the answer

For production OpenAI sessions:

1. The client obtains microphone permission only after disclosure and
   applicable consent.
2. The client creates a WebRTC offer and submits it inside AVC-01 (a
   transient, never-persisted `sdp_offer` field) over the authenticated
   broker channel.
3. The broker validates identity, client, subject, purpose, consent,
   persona, policy, retention, model profile, quota, and kill switches.
4. The broker calls `POST /v1/realtime/calls` with its server-held key and
   the full server-owned session configuration (model, voice, instructions,
   safety, turn detection, tools) in the create request.
5. The broker releases the SDP answer to the client immediately and attaches
   the sideband WebSocket (`call_id`-bound) in parallel.
6. Tool intents and consequential responses remain blocked until sideband
   control is attached and verified; if attach fails within the profile
   bound, the broker revokes the media leg and returns a canonical blocked
   or fallback result.
7. Media flows directly between client and provider; the broker stays on
   control only.

This replaces the draft's serialized readiness-before-answer gate, which
added setup latency and re-implemented configuration the create request
already applies atomically. Standard provider keys never leave the server:
each environment uses a distinct project-scoped key held only in deployment
secret storage, with a documented manual rotation procedure required before
internal live. Ephemeral client-token setup is permitted only in a
non-consequential lab profile with tools disabled and no tenant data.

### 4. Bind grants to identity, purpose, instance, epoch, and lease

AVC-01 carries a request idempotency key, client instance and app version,
workflow and purpose references, requested capability profile, contract
compatibility, persona, language, platform, accessibility preferences,
consent/profile versions, the transient SDP offer, and (on resume) the
last-applied event sequence. AVC-02 binds grant, logical session, epoch, and
media-leg identity, the resolved policy and capability set (inline), the SDP
answer, an authenticated control-channel descriptor, heartbeat interval,
lease expiry, and the initial AVC-12 snapshot.

The broker persists the issued grant keyed by authenticated actor and
`request_id` and redelivers it verbatim to the same client instance until
first successful media connect or grant expiry; afterwards a retry returns a
canonical terminal result. SDP answers are single-use and offer-bound: a
retry whose prior call never connected receives a fresh media leg under the
same logical session rather than a replayed answer. Retry equivalence is
canonical-form equality excluding declared volatile fields (client
timestamps and the SDP offer body). One client instance holds the lease and
one media leg is active per logical session; a concurrent AVC-01 from
another instance is denied. Policy-gated takeover is deferred; the epoch
mechanism stays, because revocation and lease expiry still fence stale
grants, commands, and legs.

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
event. There are no event hash chains, no snapshot integrity digests, and no
replay protocol: on any detected gap, conflict, or reconnect the client
fetches AVC-12, discards buffered events at or below the snapshot revision,
and resumes from live push. The client reports its last-applied sequence in
heartbeats and resume requests.

### 6. Make the control channel authoritative and leased, with a real protocol

The control transport is authenticated WSS carrying commands, events,
snapshots, heartbeats, and revocation. The client sends a heartbeat every
`heartbeat_interval_ms` carrying session epoch and last-applied sequence;
each server response extends the lease and returns the new
`lease_expires_at`, and may carry a fresh scoped reconnect credential bound
to session, epoch, and client instance. Control health is `degraded` after
one missed response and `lost` after the profile-declared count. A dropped
WSS reconnects with the newest credential while the lease remains valid;
otherwise the client starts over with AVC-01. Control loss immediately
disables governed commands and stops capture and playback — there is no
speech grace interval. Lease expiry always closes the media leg even when
provider connectivity is healthy. Command results are the acknowledgement;
there are no per-message acks.

### 7. Keep provider configuration and tools server-only

The server adapter owns model, voice, prompt version, instructions, safety
configuration, turn detection, tool definitions, and sideband tool
responses. The client data-channel adapter exposes no generic send: its
complete outbound allowlist is `response.cancel` and
`output_audio_buffer.clear`; `conversation.item.truncate` and all
configuration, text, tool, and privilege events are excluded. User text,
structured actions, and confirmation decisions travel through AVC-11.

Until Hermes integration lands, the reference broker exercises consent,
policy, tool, and confirmation authority through an in-process authority
stub: a static policy bundle file, fixture consent records, and one
reference intake workflow handler. The stub is server-side and fail-closed,
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
requested and provider-resolved model recorded per session and rollback to
the last qualified profile. A running media leg never silently changes
model, voice, or adapter. Mid-session persona rotation UI and its media-leg
choreography are deferred.

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

Disclosure, media purpose, provider processing, and applicable retention
consent must be current before capture or provider session creation. Consent
withdrawal through any channel stops capture, cancels output, revokes the
media leg, and prevents new retention; when the broker learns a bound
consent version is no longer valid, it revokes the lease no later than the
next heartbeat.

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
map to one canonical blocked result. Two server kill switches exist: all new
session creation, and per model profile — each with optional revocation of
active leases. Finer-grained switch scopes (media, tools, retention, drafts)
are deferred with the features they would govern.

### 14. Keep the client architecture deterministic (standard for the successor)

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

### 15. Render provider content as untrusted; keep handoff invariants only

Transcript, model text, tool summaries, attachment names, and link labels
are untrusted: plain text or a narrow sanitized subset, URI and destination
allowlists, no provider-supplied widgets. Two web-console handoff invariants
ratify now: handoff URLs never carry bearer tokens, subject identifiers,
transcripts, or provider secrets; and any future exchange must be
server-issued, one-time, and reauthorized at the web boundary. The exchange
protocol itself is deferred until the web console exists.

### 16. Qualify accessibility where the platform can deliver it

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

- **Brokered setup adds latency** -> measured first by the F0 spike, before
  contracts freeze; configuration is atomic in the create call and the
  answer is released immediately.
- **Sideband attach races first audio** -> consequential behavior is blocked
  until attach verifies; ordinary low-risk speech may begin, matching the
  declared `streaming_monitor`/`confirmation_before_action` semantics.
- **Authority stub could drift from real Hermes** -> the stub is
  server-side, fail-closed, and behind the same AVC-04/AVC-06 authority
  registry Hermes will use; integration replaces the implementation, not the
  protocol.
- **Provider API churn** -> provider DTOs stay in the server adapter; pinned
  model profile; unknown consequential semantics fail closed.
- **WSS loss while WebRTC stays up** -> immediate stop of governed commands
  and media; expiring lease enforced on both sides.
- **Duplicate or reordered delivery** -> command-id dedupe, single sequenced
  log, snapshot-only recovery.
- **Reconnect amnesia** -> bounded ephemeral same-session carryover, without
  opening full-transcript retention.
- **Deferred features leave gaps** -> each deferral keeps a closed default
  (drafts disabled, attachments reference-only, second instance denied,
  reserved gate fails preflight) rather than unspecified behavior.

## Migration Plan

1. Run the F0 brokered-call spike; record timing evidence and any AVC-02
   shape corrections.
2. Implement shared definitions, the eight AVC schemas, registries,
   fixtures, and the schema+fixture validator; register the family in
   `contracts/manifest.yaml` (aligning the bundle version with the
   changelog) and update `contracts/README.md`.
3. Implement the deterministic in-memory reference broker: authority stub,
   grant issuance and redelivery, lease/heartbeat protocol, epoch fencing,
   command dedupe, single event log, snapshot recovery, usage records, kill
   switches, and the deterministic test suite.
4. Update the avatar-first UI standard, profile schema (as the domain
   overlay carrier), template, examples, and validator; extend the
   memory-gateway consent profile with media purposes.
5. Register the successor-change map in the README records block; validate
   strict; archive on green openxFactory realization.

Rollback for this change is deleting unreleased contracts and reference code;
nothing deploys. Successor changes carry their own rollback obligations.

## Open Questions

- Whether the memory-gateway consent profile extension is sufficient for
  media purposes or a dedicated avatar consent vocabulary is needed —
  resolved while implementing migration step 4, biased to extending the
  existing schema.
- The avatar renderer and Flutter media/storage package selections move to
  `implement-avatar-client-lab` (a one-page ADR each; static per-state
  assets are acceptable for the deterministic lab).
- The production deployment home and per-domain topology are decided by
  `qualify-avatar-live-voice`, consistent with repo-boundary-governance
  routing runtime operations to install repositories.
- GPT-Live transport and event semantics remain unknown until OpenAI
  publishes an API contract; nothing here blocks the Realtime 2.1 adapter.
