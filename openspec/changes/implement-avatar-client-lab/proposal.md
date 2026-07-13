code_surface: openxFactory, xfactory-avatar-client
target_release: implemented

## Why

The avatar-client kernel (`contract-v1.7`), the avatar-first UI standard
(`contract-v1.8`), and the non-deployable reference runtime are realized, but
none of them can be exercised by a person. The reference runtime is a
conformance proof, not a client; the contracts and profiles are YAML. To
actually *test the avatar* — the interaction, consent, approval, handoff, and
recovery model — a real client is required.

A live-voice client entangles two questions that must be separated:

- Does the interaction work for the user? — provable **deterministically**.
- Can a live model and governed runtime drive it correctly? — a separate,
  online, credential-bearing question.

This change builds only the first: an **offline, deterministic Flutter UI lab**
that renders the complete avatar-first interaction and authority model from
replayed fixtures, with no live model, voice, WebRTC, session broker, or
provider credential. Live voice, real Hermes, and provider qualification are
deliberately deferred to `qualify-avatar-live-voice` and `avatar-pilot-hardening`
and appear here only as fail-closed seams. openxFactory owns the neutral
acceptance and conformance fixtures for the lab; the Flutter application itself
lives in a separate private repository.

## What Changes

- Create a new private repository `xfactory-avatar-client` holding the Flutter
  avatar client. openxFactory does not own the Flutter application; it owns the
  neutral contracts, conformance fixtures, and acceptance requirements the
  client is measured against. Aggregation-repo pinning is a separate change.
- Build the client as an offline **deterministic UI lab** (slices F1-F4): an
  adaptive shell with five persistent regions and an always-on authoritative
  status strip; three client-local presentation modes (conversation, work,
  review); a generic service-intake workflow; and governed-action cards that
  render canonical intent and approval state only.
- Render a lightly-animated, non-photorealistic avatar with exactly six states
  (`listening`, `thinking`, `speaking`, `interrupted`, `blocked`, `handoff`),
  no lip-sync, behind a replaceable renderer interface. Presentation state is
  DERIVED from authority; the renderer sees no kernel state and cannot affect
  authority.
- Consume the released kernel and UI profile by content address: pin the exact
  commit and per-file SHA-256 of `contract-v1.7` (`contracts/avatar-client/`)
  and `contract-v1.8` (`avatar-first-ui-profile` + `examples/avatar-first-ui/`),
  verified fail-closed in CI. A tag-only pin fails.
- Drive every session by replaying an ordered `AVC-04` event stream (plus
  `AVC-12` snapshots) through a pure, synchronous session core that mirrors the
  reference-runtime invariants: single ordered log, monotonic sequence and
  recovery cursor, `state_revision`/epoch fencing, media-authorized-observed-once,
  producer-authority guard, revocation bound, snapshot barrier, and fail-closed
  handling of unknown enums, producers, or keys.
- Isolate live concerns behind ports: v1 ships only a fixture transport and
  fixture command sink; the live WebRTC/broker/Hermes adapters are interfaces
  with no implementation in this change. Each deferred capability keeps a
  fail-closed default (voice/push-to-talk fail preflight to text/handoff, web
  offline drafts disabled, attachments reference-only, second instance denied).
- Add openxFactory-owned neutral conformance fixtures and a client acceptance
  map for the lab, reusing the existing avatar-first UI fixtures where they
  apply; contribute any new neutral scenarios upstream rather than forking them
  into the client repo.
- Make accessibility first-class and gating: the eleven avatar-first UI
  accessibility-baseline capabilities, keyboard-only completion of F1-F4,
  non-color state cues, and a text-only peer renderer.
- Ship the developer lab instrumentation (scenario selector, event step/scrub,
  latency and failure injection, viewport switch, pseudo-locale and
  reduced-motion toggles, emitted-event inspector) as a separate entrypoint that
  is compiled out of and asserted absent from any production build.

Out of scope (deferred; seam only, no live code): any live model or provider
credential; WebRTC, media plane, brokered SDP, real session broker, real Hermes
control channel; microphone/audio/VAD; lip-sync; interactive workflow editing
(owned by the separate web console); native iOS/Android; real internationalization
beyond a pseudo-locale; web token-exchange handoff; real multi-device takeover;
latency SLOs and production telemetry.

## Capabilities

### New Capabilities

- `avatar-client-lab` — the neutral acceptance requirements for the offline,
  deterministic avatar client UI lab: its non-production boundary,
  content-addressed contract consumption, fixture-replay determinism,
  re-derives-never-decides authority posture, the replaceable six-state avatar
  seam, the accessibility baseline, the repository boundary, and the fail-closed
  deferral of voice/WebRTC/Hermes.
