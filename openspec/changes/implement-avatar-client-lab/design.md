# Design: implement-avatar-client-lab

Non-normative. The authoritative obligations are in
`specs/avatar-client-lab/spec.md`; this records the shape and the load-bearing
decisions, drawn from the v1 brainstorm.

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

## Open decisions carried into implementation

1. Dart 2020-12 validator: spike Workiva `json_schema` against all
   `fixtures/index.yaml` classes; port the keyword subset if it or its license
   fails. It is the CI type-faithfulness ground truth — budget it as a task.
2. Web accessibility: qualify a11y on Windows desktop for v1; ship a documented
   WCAG exception register for canvas-rendered web; do not claim web AA in F1-F4.
3. Golden platform: authoritative goldens on the Linux CI job only, pinned font +
   SDK; Windows + web run all tests except pixel goldens.
4. Fixture duality: one normalization loader; `fixtures/index.yaml` is
   authoritative for conformance, the UI-example fixtures are scenario seeds.

## What stays out, and why the seam is clean

Live model, WebRTC/media, brokered SDP, real broker, real Hermes, mic/VAD,
lip-sync, native mobile, real i18n, web token-exchange, real multi-device
takeover, and latency SLOs are all deferred to `qualify-avatar-live-voice` and
`avatar-pilot-hardening`. In this change they are port interfaces with fixture
adapters and fail-closed defaults (voice/push-to-talk fail preflight to
text/handoff, web drafts disabled, attachments reference-only, second instance
denied). The live change supplies a transport behind the existing
`SessionTransport` port; the reducer and UI do not change.
