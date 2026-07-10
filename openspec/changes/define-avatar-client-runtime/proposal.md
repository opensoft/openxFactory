code_surface: openxFactory
target_release: implemented

## Why

xFactories need one reusable avatar client and runtime contract in which
low-latency conversation remains responsive while identity, consent, workflow,
tools, approvals, retention, and records remain under xFactory authority.
Without ratified decisions, each DomainxFactory would invent incompatible
session state, and a patient-facing implementation such as MedxFactory could
expose raw provider behavior, duplicate consequential actions after reconnect,
or couple the UI to a temporary model API.

A seven-expert review of the first draft (2026-07-10) found the trust
architecture sound but the scope unimplementable for this team: it specified a
production distributed system across two repositories (one not yet created),
bound to Hermes services that are still scaffolds, with 93 tasks and five
release rings. This revision keeps the ratified standard intact and shrinks
the realized surface to the smallest kernel that proves it: neutral contracts,
a deterministic reference runtime in openxFactory, updated UI-standard assets,
and an early de-risk spike. Client implementation and live-provider
qualification follow in named successor changes that pin this kernel.

## What Changes

- Ratify the adaptive avatar-first UI standard as presentation duties:
  conversation, work, and review modes, conventional fallback, accessible
  controls, safe content rendering, persona presentation, disclosure,
  recording indicators, and consent-aware handoff. Behavior and policy rules
  live in `avatar-client-runtime`; the UI capability states what the client
  must display and preserve.
- Define the AVC contract kernel — eight contracts: AVC-01 session request,
  AVC-02 session grant (runtime capabilities inline), AVC-04 session event
  (transcript segments as registered payloads), AVC-06 structured
  confirmation, AVC-07 retention profile, AVC-08 persona profile, AVC-11
  session command, and AVC-12 state snapshot. Contracts are YAML-serialized
  JSON Schema (draft 2020-12) under `contracts/avatar-client/`, registered in
  `contracts/manifest.yaml`. AVC-03 and AVC-05 are absorbed; AVC-09 and
  AVC-10 are reserved for the live-qualification successor change.
- Separate untrusted client commands, immutable authoritative events, and
  recovery snapshots. One control-API-sequenced event log per session;
  `command_id` idempotency with a shared retry-equivalence rule; expected
  state revision only on registry-flagged consequential commands; recovery is
  always snapshot-based (no replay protocol, no event hash chains, no
  snapshot digests).
- Require brokered OpenAI session creation: the server calls
  `/v1/realtime/calls` with the full server-owned configuration in the create
  request, releases the SDP answer immediately, and attaches the sideband
  WebSocket in parallel. Tool intents and consequential responses stay
  blocked until sideband control is verified; the media leg is revoked if
  attach fails. Continuous media flows directly between client and provider;
  xFactory never relays audio. The client data channel is constrained to
  `response.cancel` and `output_audio_buffer.clear`.
- Bind every grant, command, event, media leg, and snapshot to authenticated
  server-derived context, workflow purpose, consent version, session epoch,
  and an expiring control lease with a specified heartbeat/renewal protocol.
  One client instance and one media leg per logical session; a second
  instance is denied (policy-gated takeover is deferred).
- Keep provider configuration, prompts, and tools server-owned. Until Hermes
  integration lands, the reference broker exercises consent, policy, and
  confirmation authority through a fail-closed in-process stub with static
  policy fixtures, explicitly acting on behalf of the future Hermes boundary.
- Make reconnect deterministic: control loss immediately stops governed
  commands and media (no grace interval); lease expiry always closes media;
  a reconnected media leg rehydrates from the authoritative snapshot plus a
  default ephemeral same-session context carryover so the assistant does not
  lose the conversation; session duration is capped below provider limits
  with an explicit limit-reached resume state.
- Keep provider and model identifiers inside versioned server profiles. The
  first profile is `gpt-realtime-2.1`; `gpt-live-1` and all other profiles
  remain disabled pending their own qualification. Persona is fixed per
  logical session; voice is fixed per media leg.
- Enforce consent-before-capture, server-side consent invalidation (lease
  revoked no later than the next heartbeat), per-tenant usage records and
  session caps with canonical quota-blocked results, and two kill switches:
  all new session creation, and per model profile, each with optional
  active-lease revocation.
- Scope retention to ephemeral-by-default plus structured workflow records.
  Full transcript, audio, video, independent transcription, offline drafts,
  and attachment byte paths are explicitly out of scope: reserved, disabled,
  and forbidden until their successor changes ratify them.
- Run a bounded F0 spike before contract freeze: a throwaway brokered-call
  script measuring `/v1/realtime/calls` + sideband setup timing against the
  real API with a lab key, feeding AVC-02 field shapes and latency
  assumptions.
- Record the successor-change map: `implement-avatar-client-lab` (private
  Flutter repository, deterministic client slices), `qualify-avatar-live-voice`
  (local media, live OpenAI adapter, deployment home and topology, latency
  budgets, AVC-09/AVC-10), and `avatar-pilot-hardening` (Hermes integration,
  domain onboarding, SBOM/chaos/accessibility-audit/rollback evidence), plus
  deferred features: offline drafts, attachments, mid-session persona change,
  seamless context rollover, web-console handoff protocol, multi-device
  takeover, GPT-Live.

## Capabilities

### New Capabilities

- `avatar-first-ui`: presentation duties of the adaptive shell — modes,
  Hermes-layer defaults, controls, recording awareness, accessibility
  baseline, persona presentation, disclosure, safe rendering, fallback, and
  the Flutter/web responsibility split.
- `avatar-client-runtime`: the AVC contract kernel, trusted session setup,
  command/event/snapshot authority, brokered direct media with sideband
  control, lease and recovery behavior, speech gates, consent enforcement,
  retention scope, usage controls, and deterministic-first release gating.

### Modified Capabilities

- `shared-contract-ownership`: canonical AVC ownership in openxFactory;
  consumers pin an openxFactory commit and per-file digest and prove
  conformance by executing the canonical fixture suite (hand-written bindings
  permitted; code generation optional).
- `repo-boundary-governance`: boundary and release rules for the future
  private `xfactory-avatar-client` repository (created by a successor
  change); supply-chain evidence activates at the internal-live gate;
  aggregation pinning and the web console remain separately proposed.

## Impact

- **openxFactory:** `contracts/avatar-client/` schemas, fixtures, and
  validator; `xfactory/avatar_runtime/` deterministic reference broker
  (non-deployable reference code); updated avatar-first UI standard, profile
  schema, template, and validator; README records; F0 spike results.
- **xfactory-avatar-client:** not created here. This change ratifies its
  boundary rules; `implement-avatar-client-lab` creates it against the
  pinned kernel.
- **DomainxFactories:** author one avatar-first UI profile (the domain
  overlay carrier) plus consent purposes via the extended memory-gateway
  consent profile; no neutral-protocol forks.
- **Hermes and workflow services:** authority model ratified now; live
  integration explicitly deferred to `avatar-pilot-hardening`.
- **Compatibility:** existing static avatar-first profiles remain valid;
  runtime additions are new contracts.
