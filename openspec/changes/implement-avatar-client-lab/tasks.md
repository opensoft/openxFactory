# Tasks: implement-avatar-client-lab

Order is roughly M0 walking skeleton → F1-F4 breadth → realization. The
openxFactory-side work (fixtures, acceptance map, boundary) is done here; the
Flutter work lands in codexFactory under `apps/avatar-client-lab/`.

Note: the Flutter implementation tasks (sections 2-8) run in dedicated
flutterBench sessions, not in factory doc sessions.

## 1. Repository and boundary

- [ ] 1.1 Bootstrap `apps/avatar-client-lab/` inside codexFactory: create the directory skeleton and an app README stating the ownership boundary (Flutter app + Dart bindings here; neutral contracts/fixtures/acceptance in openxFactory); wire it into codexFactory's validation so the app tree is treated as code, not docs, and is excluded from the doc-health and doc validators (check `scripts/validate-docs.sh` conventions in codexFactory only if needed).
- [ ] 1.2 Bootstrap the monorepo skeleton under `apps/avatar-client-lab/` (pub workspaces + thin melos): packages `avc_contracts`, `avc_session`, `avc_adapters_fixture`, `avatar_view`, `ui_kit`, and `app`; FVM-pin the Flutter SDK.
- [ ] 1.3 Add the boundary check that fails if the `apps/avatar-client-lab/` app edits a neutral contract, registry, or shared fixture (ownership stays in openxFactory).
- [ ] 1.4 Add the pure-Dart / Flutter split guard (pure packages import no Flutter) and the forbidden-API grep gate (`DateTime.now`, `Random`, sockets in pure packages).

## 2. Content-addressed contracts and bindings

- [ ] 2.1 Vendor the pinned semantic set of `contract-v1.7` (`contracts/avatar-client/`) and `contract-v1.8` (`avatar-first-ui-profile` + `examples/avatar-first-ui/`) into `avc_contracts/assets/`; record both refs (exact commit + per-file SHA-256) in one `contract_pin.yaml`.
- [ ] 2.2 Implement `verify_pin.dart` (runs first in CI; fails closed on drift; rejects a tag-only pin) and `sync_contracts.dart` (the only tool that reads a local openxFactory checkout).
- [ ] 2.3 Generate the closed registry enums from the vendored registry YAML (`gen_contracts.dart --check` asserts no divergence).
- [ ] 2.4 Hand-write the ~8 sealed AVC envelopes (session request/result, event, command, snapshot, structured confirmation, retention, persona) with value equality and JSON.
- [ ] 2.5 Implement the Dart draft-2020-12 schema-conformance runner over `contracts/avatar-client/fixtures/index.yaml` as the CI type-faithfulness ground truth (locked decision 1: adopt Workiva `json_schema` behind a bounded spike over all fixture classes, with the named fallback trigger to port the keyword subset — see `supporting-docs/open-decisions.md`). The spike is a budgeted first task.

## 3. Session core (pure, deterministic)

- [ ] 3.1 Implement `reduce(SessionState, InboundFrame) -> (SessionState, [Effect])` over a single ordered log, mirroring the reference-runtime invariants: monotonic sequence, `last_event_sequence` recovery cursor, `state_revision`/epoch fencing, `command_id` idempotency.
- [ ] 3.2 Enforce media-authorized-observed-once (the barrier that unlocks speak/capture), the producer-authority guard (authoritative ⇒ approved producer), the revocation bound (→ credential-free terminal), and the snapshot barrier (fix, buffer, drain once, overflow → restart).
- [ ] 3.3 Fail closed on unknown enum, unknown producer, or forbidden key → a safe view-state.
- [ ] 3.4 Define the ports: `Clock`, `IdSource`, `SessionTransport`, `CommandSink`, `MediaTransport`. Live adapters are interfaces only in this change.

## 4. Fixture adapter and scenarios

- [ ] 4.1 Implement `FixtureScenarioTransport` and `FixtureCommandSink`: replay an ordered scenario event stream on a virtual clock; script accepted/rejected/conflict command responses to close the loop.
- [ ] 4.2 Add the openxFactory-owned neutral client-lab conformance fixtures and a client acceptance map, wiring in the inherited scenario set — the released `contracts/avatar-client/acceptance-map.yaml` and `examples/avatar-first-ui/avatar-first-ui-acceptance-map.yaml` already name this change as an owner change for named ACR/SCO/RBG/AFU scenarios (enumerated in `supporting-docs/acceptance-and-tests.md`); reuse `examples/avatar-first-ui/fixtures/` where they apply; contribute new neutral scenarios upstream.
- [ ] 4.3 Seed M0 from the released `examples/avatar-first-ui/fixtures/deterministic/offline-acceptance.yaml`; one loader normalizes the portable-conformance vs UI-example fixture shapes (locked decision 6: `index.yaml` authoritative for conformance, UI-example fixtures as scenario seeds). The seed fixture proves only the `listening` baseline — contribute a neutral `listening→thinking→speaking` extension fixture upstream so the six-state selector has a replayable proof path.

## 5. Avatar renderer

- [ ] 5.1 Define the `AvatarView` leaf interface (`AvatarInput`: derived state, opaque intensity, injected phase, reducedMotion, opaque style token, semantics label) — no ticker, RNG, or wall clock.
- [ ] 5.2 Implement `deriveAvatarState(viewState)`: authority → the six states, fail-closed (control-lost ⇒ `blocked`, never `speaking`).
- [ ] 5.3 Implement `LightweightPortraitAvatar` (pure-Dart CustomPainter, app-owned animation controller) and a peer `TextOnlyAvatar`; per-state non-color cue; reduced-motion static frame. (Rive is a documented later swap behind the same interface.)

## 6. UI shell, modes, and accessibility

- [ ] 6.1 Build `AdaptiveAvatarShell`: five persistent regions (avatar_stage, conversation_rail, context_panel, action_bar; handoff/settings as side-sheets) + an always-on `AuthorityStatusStrip` binding the four authoritative axes; responsive compact→kiosk; `textScaler`-aware; reflow at 400% zoom.
- [ ] 6.2 Implement the three presentation modes (conversation/work/review) as client-local view emphasis over the same regions — never routes, never hiding authoritative status; seed from `profile.surface_default`.
- [ ] 6.3 Implement `ui_kit`: the governed-action cards (canonical intent/approval only), the untrusted-content sanitizer (AFU-007), a11y primitives (live-region announcer, focus order, high-contrast + reduced-motion themes).
- [ ] 6.4 Make the eleven accessibility-baseline capabilities gating tests; prove keyboard-only F1-F4 completion; pseudo-locale + RTL.

## 7. Developer lab harness

- [ ] 7.1 Ship the harness behind a separate `main_lab.dart` entrypoint + `XF_LAB` compile-out + an `assert` that trips if harness widgets mount when `!kLab`.
- [ ] 7.2 Implement the controls as fixture operations only: scenario selector, event step/scrub by sequence, latency + failure injection, viewport switch, pseudo-locale + reduced-motion toggles, emitted-event inspector (ordered AVC-04 log + `state_revision` + `last_event_sequence`).

## 8. Slice acceptance (F1-F4)

- [ ] 8.1 M0 walking skeleton: one fixture end-to-end (reducer + static avatar + avatar_stage/conversation_rail + three harness controls) green on three gates — fixtures/index conformance, replay determinism, one VP-01 golden. The six-state transition arc (`listening→thinking→speaking`) is proven by the upstream extension fixture from task 4.3.
- [ ] 8.2 F1 Shell: regions, status strip, responsiveness, keyboard/text-only/reduced-motion, persona continuity.
- [ ] 8.3 F2 Deterministic session: every canonical state reached by a fixture with a golden + event assertion; retention asymmetry; event-gap → AVC-12 recovery; lease/epoch takeover.
- [ ] 8.4 F3 Service intake: happy path, ask-only-the-gap, consequential correction (supersede AVC-06), decline/withdraw, offline draft (desktop; web closed-default), idempotency-keyed conflict.
- [ ] 8.5 F4 Governed actions: intent/approval rendering only, confirmation-first bound to the exact effect, denied ≠ failed ≠ cancelled, policy-loss pauses actions, handoff shows scope with no token.
- [ ] 8.6 Author the golden strategy (locked decision 5: authoritative goldens on the Linux CI job only, bundled pinned font + version-pinned SDK; Windows + web run all tests except pixel goldens; web = headless-Chrome smoke); every golden flake treated as a determinism bug, never a tolerance to widen.

## 9. Realization

- [ ] 9.1 [GATE] Confirm the offline lab is green on the implemented target: `verify_pin` + schema conformance + replay determinism + boundary/forbidden-API gates + keyboard-only F1-F4 + the golden set, on Windows + web (locked decision 4: a11y qualified on Windows desktop; a documented WCAG exception register for canvas web; no web AA claim in F1-F4).
- [ ] 9.2 Record the client release evidence (pinned contract refs, fixture-conformance result, dependency lock, license check, secret scan, test + golden result) in codexFactory.
- [ ] 9.3 Land the openxFactory-side artifacts (client-lab conformance fixtures + acceptance map + boundary rule) and link the codexFactory `apps/avatar-client-lab/` path in the openxFactory README OpenSpec Records; sync the codexFactory pin as a routine submodule-pointer commit.
- [ ] 9.4 Archive this change once merge evidence and a green run exist on both code surfaces.
