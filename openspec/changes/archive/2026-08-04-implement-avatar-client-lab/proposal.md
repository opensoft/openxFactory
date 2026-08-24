code_surface: openxFactory, codexFactory
target_release: implemented
Status: ratified
Ratified: 2026-08-04 — record: the archive act, commit `25d8e1c` "Archive implement-avatar-client-lab under Brett's 9.1 disposition; record the F0 archive-hold ruling", which applied this change's spec delta into `openspec/specs/avatar-client-lab/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The archive act was taken on Brett's word, named in the commit subject and body: "9.1 discharged by disposition (ruled 2026-08-04) ... 9.4 archived on the recorded 9.3 merge evidence", and in the change's own tasks.md 9.1, "DISCHARGED by disposition, ruled by Brett 2026-08-04 (option b, decision round)". That disposition discharged a REALIZATION gate rather than ratifying the change, so it is recorded here as the word the archive act was taken on, not as the ratification itself. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

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
lives in codexFactory under `apps/avatar-client-lab/`.

## What Changes

- Build the Flutter avatar client as a lab (v1) inside codexFactory under
  `apps/avatar-client-lab/`. openxFactory does not own the Flutter application;
  it owns the neutral contracts, conformance fixtures, and acceptance
  requirements the client is measured against. codexFactory is already an
  aggregation-repo submodule, so syncing its pin here is a routine
  submodule-pointer commit, not a separate change.
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
  into the codexFactory app.
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
