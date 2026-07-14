# Design: implement-avatar-client-lab

Non-normative. The authoritative obligations are in
`specs/avatar-client-lab/spec.md`; this records the shape and the load-bearing
decisions, promoted from the `avatar-client-lab` staged topic
(`openxFactory:staging:avatar-client-lab` — the four organized fragments now in
`supporting-docs/`), which itself organized the 2026-07-13 v1 brainstorm.

## Load-bearing property: bit-exact determinism

The lab exists to prove the interaction and authority model without a live
service. Everything follows from one property: **the same fixture replayed twice
yields identical view-state**, so goldens and conformance run in CI with no
network. This is why the session core is a pure, synchronous reducer over an
ordered event log (a direct mirror of `xfactory/avatar_runtime`), and why clocks
and IDs are injected ports rather than ambient calls.

## Architecture

```
openxFactory (pinned, vendored, SHA-256 verified)
  contract-v1.7 kernel · contract-v1.8 avatar-first-ui-profile + fixtures
        │
  avc_contracts (pure)   gen enums + hand-written sealed envelopes
                         + schema-conformance runner (CI ground truth)
        │
  avc_session (pure)     reduce(State, InboundFrame) -> (State, [Effect])
                         ordered log · sequence/recovery cursor · revision/epoch
                         media-authorized-once · producer-authority · revocation
                         snapshot barrier · fail-closed
                         ports: Clock · IdSource · SessionTransport · CommandSink · Media
        │
  avc_adapters_fixture (v1)          avc_adapters_live (LATER — interface only)
  replays ordered scenario YAML      WSS control + WebRTC media plane;
  on a virtual clock                 swap behind SessionTransport → zero
                                     reducer/UI change
        │ immutable derived view-state
  Flutter: app · ui_kit · avatar_view
  Riverpod Notifier · go_router · 5 regions · AuthorityStatusStrip
  AvatarView seam ← deriveAvatarState(viewState)
```

## Decisions (with the runner-up and why-not)

- **State management — Riverpod 2 wrapping a pure core, not flutter_bloc.** The
  reducer is pure and synchronous; Bloc's Stream/async layer would inject
  ordering nondeterminism where the runtime has none. Keep Riverpod to one thin
  `Notifier` so a later swap is a wrapper change. Both wrap the same pure core.
- **Avatar — pure-Dart CustomPainter now; Rive as a later interface-compatible
  swap.** Rive owns its own animation clock (fragile goldens) and drags a
  CanvasKit-bound native dependency into a deterministic offline lab. The golden
  contract for any future renderer is the reduced-motion static frame + selector
  wiring + per-state non-color cue — not animated pixel equality — so a swap
  cannot silently void the determinism guarantee.
- **Contracts → Dart — hybrid.** Generate the volatile closed enums; hand-write
  the small stable envelope surface; prove faithfulness by replaying every
  fixture through the real schema. Pure codegen cannot represent AVC-02's
  grant/non-grant `oneOf`, the `not/anyOf` credential-exclusions, or AVC-04's
  producer-authority `if/then`.
- **Contract provenance — vendored, content-addressed, both bundles.** Record
  `contract-v1.7` and `contract-v1.8` refs (commit + per-file SHA-256) in one
  `contract_pin.yaml`; they evolve on different cadences, so CI gates both digest
  sets. No submodule; a tag-only pin fails.
- **Repository boundary.** The Flutter app + Dart bindings live in
  `xfactory-avatar-client`; openxFactory owns neutral contracts, fixtures, and
  acceptance. Aggregation-repo pinning is a separate change.

## Locked decisions (staging, 2026-07-13)

All six formerly-open forks were locked at the staging stage with rationale —
the full decision records live in
[supporting-docs/open-decisions.md](supporting-docs/open-decisions.md):

1. Dart 2020-12 validator: adopt Workiva `json_schema` (Apache-2.0) behind a
   bounded spike over all `fixtures/index.yaml` classes, with a named fallback
   trigger to port the keyword subset. The risky 2020-12 features
   (`$dynamicRef`, `unevaluatedProperties`, `prefixItems`) are absent from the
   AVC schemas. It is the CI type-faithfulness ground truth — a budgeted first
   task, decided before the dependency is pinned.
2. State binding: Riverpod 2, one thin `Notifier` over the pure core.
3. Contract pin: one `contract_pin.yaml`, both bundles' digest sets, verified
   against `contracts/manifest.yaml` (the authoritative published index); the
   v1.8 UI-profile set enumerated explicitly.
4. Web accessibility: qualify a11y on Windows desktop for v1; documented WCAG
   exception register for canvas-rendered web; no web AA claim in F1-F4.
5. Golden platform: authoritative goldens on the Linux CI job only, pinned font
   + SDK; Windows + web run all tests except pixel goldens; a golden flake is a
   determinism bug, never a tolerance to widen.
6. Fixture duality: one loader normalizing both released fixture formats into a
   common in-memory record; `fixtures/index.yaml` authoritative for conformance,
   the UI-example fixtures are scenario seeds; neutral scenarios contributed
   upstream first.

The acceptance surface (F1-F4 foci, the inherited scenario map from the released
acceptance maps that already name this change as an owner change, and the nine
CI gates) is enumerated in
[supporting-docs/acceptance-and-tests.md](supporting-docs/acceptance-and-tests.md).
One M0 correction from staging: the released `offline-acceptance.yaml` fixture
proves only the `listening` baseline, so M0 also contributes a neutral
`thinking -> speaking` extension fixture upstream.

## What stays out, and why the seam is clean

Live model, WebRTC/media, brokered SDP, real broker, real Hermes, mic/VAD,
lip-sync, native mobile, real i18n, web token-exchange, real multi-device
takeover, and latency SLOs are all deferred to `qualify-avatar-live-voice` and
`avatar-pilot-hardening`. In this change they are port interfaces with fixture
adapters and fail-closed defaults (voice/push-to-talk fail preflight to
text/handoff, web drafts disabled, attachments reference-only, second instance
denied). The live change supplies a transport behind the existing
`SessionTransport` port; the reducer and UI do not change.
