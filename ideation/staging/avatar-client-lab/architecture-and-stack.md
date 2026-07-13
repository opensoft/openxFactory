# Architecture and Stack — avatar client lab

Status: staged
Kind: architecture
Summary: The v1 architecture and recommended stack for the avatar client lab —
a pure deterministic reducer mirroring the reference runtime, ports/adapters so
voice is a later swap, a replaceable six-state avatar, and content-addressed
contract bindings.
Topics: avatar-client, flutter, architecture, reducer, riverpod, ports-adapters, determinism, rive, contracts
Repository context: openxFactory (neutral) with the Flutter realization in `xfactory-avatar-client`
Staging ID: openxFactory:staging:avatar-client-lab
Source: v1 brainstorm 2026-07-13 (six-dimension synthesis)

Supporting fragment for [avatar-client-lab.md](avatar-client-lab.md). Design
direction, not final spec text.

## Load-bearing property: bit-exact determinism

The lab proves the interaction and authority model with no live service, so the
one property everything follows from is: **the same fixture replayed twice yields
identical view-state**. Goldens and conformance then run in CI with no network.

## Claims

1. **The session core is a pure, synchronous reducer over an ordered event log**,
   `reduce(State, InboundFrame) -> (State, [Effect])`, with no `dart:async` in the
   reduce path — a direct mirror of the Python `xfactory/avatar_runtime`
   invariants: single ordered log, monotonic sequence and recovery cursor,
   `state_revision`/epoch fencing, media-authorized-observed-once, producer-authority
   guard, revocation bound, snapshot barrier, and fail-closed handling of unknown
   enums/producers/keys. It is pure Dart, headless-testable under `dart test`.

2. **State binding is Riverpod 2 wrapping the pure core, not flutter_bloc.** The
   reducer is pure and synchronous; Bloc's Stream/async layer would inject
   ordering nondeterminism where the runtime has none. Keep Riverpod to one thin
   `Notifier` (which doubles as DI, and whose override mechanism *is* the
   fixture-replay/injected-clock seam) so a later swap is a wrapper change.

3. **Live concerns sit behind ports; v1 ships only fixture adapters.** A
   `SessionTransport` port takes a `FixtureScenarioTransport` now and a live
   WebRTC/broker transport later; the reducer and UI require no change to consume
   the live adapter. This is what makes voice an adapter swap, not a rewrite.

4. **The avatar is a pure-Dart CustomPainter now, Rive later, behind a
   replaceable `AvatarView` seam.** Six states (listening/thinking/speaking/
   interrupted/blocked/handoff), no lip-sync. Presentation state is DERIVED from
   authority by an app-land selector; the renderer sees no kernel state, owns no
   clock (phase is injected → goldens are frame-exact), and cannot affect
   authority. Control-lost ⇒ `blocked`, never `speaking`. Rive is rejected for v1
   because it owns its own animation clock (fragile goldens) and drags a
   CanvasKit-bound native dependency into a deterministic offline lab; its swap
   stays interface-compatible. The full media/control → six-state derivation
   table (the released schema's ten `media.states` plus AVC-12
   `control_health`/`session_outcome`, mapped down to the six avatar states) is
   an acceptance artifact authored in
   [acceptance-and-tests.md](acceptance-and-tests.md).

5. **Contracts → Dart is hybrid.** Generate the volatile closed enums from the
   pinned registry YAML; hand-write the ~8 stable sealed AVC envelopes; prove
   faithfulness by replaying every fixture through the real draft-2020-12 schema
   in CI. Pure codegen cannot represent AVC-02's grant/non-grant `oneOf`, the
   `not/anyOf` credential-exclusions, or AVC-04's producer-authority `if/then` —
   the exact invariants the contract is consumed for.

6. **Contract provenance is vendored and content-addressed for both bundles.**
   Record `contract-v1.7` and `contract-v1.8` refs (exact commit + per-file
   SHA-256) in one `contract_pin.yaml`, gated in CI; they evolve on different
   cadences so a partial bump could mix incompatible minors. No submodule; a
   tag-only pin fails. `contracts/manifest.yaml` is the authoritative published
   per-file-digest index for BOTH bundles — the pin verifies against it rather
   than maintaining a divergent list. (Note: the v1.7 kernel's digested set is
   enumerated in the avatar-client README, but the v1.8 UI-profile set — the
   profile schema plus its fixtures and acceptance map — has no equivalent
   published enumeration beyond the manifest; the pin must enumerate it.)

7. **Repository boundary.** The Flutter app + generated Dart bindings live in the
   private `xfactory-avatar-client` repo; openxFactory owns the neutral contracts,
   conformance fixtures, and acceptance. Aggregation-repo pinning is a separate
   change. New neutral scenarios are contributed upstream, not forked.

## Sketch

```
openxFactory (pinned, vendored, SHA-256 verified)
  contract-v1.7 kernel · contract-v1.8 avatar-first-ui-profile + fixtures
        v
  avc_contracts (pure)   gen enums + hand-written sealed envelopes
                         + schema-conformance runner (CI ground truth)
        v
  avc_session (pure)     reduce(State, InboundFrame) -> (State, [Effect])
                         ordered log · sequence/recovery · revision/epoch
                         media-authorized-once · producer-authority · revocation
                         snapshot barrier · fail-closed
                         ports: Clock · IdSource · SessionTransport · CommandSink · Media
        v
  avc_adapters_fixture (v1)        avc_adapters_live (LATER — interface only)
  replays scenario YAML on a       WSS control + WebRTC media; swap behind
  virtual clock                    SessionTransport -> zero reducer/UI change
        v  immutable derived view-state
  Flutter: app · ui_kit · avatar_view
  Riverpod Notifier · go_router · 5 regions · AuthorityStatusStrip
  AvatarView seam <- deriveAvatarState(viewState)
```

## Project shape

Lean monorepo (pub workspaces + thin melos), hard pure-Dart / Flutter split:
`avc_contracts` (pure), `avc_session` (pure), `avc_adapters_fixture`,
`avatar_view` (Flutter), `ui_kit` (Flutter), `app` (Flutter). The dev harness is
a separate `main_lab.dart` entrypoint, compiled out of and asserted absent from
production; every harness control reduces to feeding canonical AVC data through
the reducer, so each dev poke is CI-replayable and re-runnable against the future
live adapter.

## First runnable milestone (M0)

A tracer bullet through F1+F2: one fixture wired end-to-end (reducer + static
avatar + two of five regions + three harness controls), green on three gates —
`fixtures/index.yaml` conformance, replay determinism, one golden. Seed with the
released `examples/avatar-first-ui/fixtures/deterministic/offline-acceptance.yaml`
(fixed clock `2026-07-11T00:00:00Z`, session `sess-0001`, `session_started` →
`media_authorized` → `capture_authorized`) — note it proves only the `listening`
baseline; it emits no thinking/speaking events. M0 therefore also contributes a
small neutral extension fixture upstream (per claim 7) carrying the
`listening -> thinking -> speaking` arc, so the six-state selector has a
replayable proof path. After M0, F1-F4 is pure breadth.
