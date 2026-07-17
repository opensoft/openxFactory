# Tasks: implement-avatar-client-lab

Order is roughly M0 walking skeleton → F1-F4 breadth → realization. The
openxFactory-side work (fixtures, acceptance map, boundary) is done here; the
Flutter work lands in codexFactory under `apps/avatar-client-lab/`.

Checkbox sweep 2026-07-17 (housecleaning): sections 1-8 and 9.2 verified
per-task against the realized codexFactory tree (apps/avatar-client-lab at
main, post PR #16/#17 merges) and openxFactory artifacts; 9.1 and 9.4 remain
open — see the 9.1 note.

Note: the Flutter implementation tasks (sections 2-8) run in dedicated
flutterBench sessions, not in factory doc sessions.

## 1. Repository and boundary

- [x] 1.1 Bootstrap `apps/avatar-client-lab/` inside codexFactory: create the directory skeleton and an app README stating the ownership boundary (Flutter app + Dart bindings here; neutral contracts/fixtures/acceptance in openxFactory); wire it into codexFactory's validation so the app tree is treated as code, not docs, and is excluded from the doc-health and doc validators (check `scripts/validate-docs.sh` conventions in codexFactory only if needed). — Swept 2026-07-17: skeleton, code-not-docs validator exclusion, and boundary gate (boundary_check.dart) verified; caveat — the ownership boundary is stated in pubspec.yaml/melos.yaml header comments rather than a standalone app README.
- [x] 1.2 Bootstrap the monorepo skeleton under `apps/avatar-client-lab/` (pub workspaces + thin melos): packages `avc_contracts`, `avc_session`, `avc_adapters_fixture`, `avatar_view`, `ui_kit`, and `app`; FVM-pin the Flutter SDK.
- [x] 1.3 Add the boundary check that fails if the `apps/avatar-client-lab/` app edits a neutral contract, registry, or shared fixture (ownership stays in openxFactory).
- [x] 1.4 Add the pure-Dart / Flutter split guard (pure packages import no Flutter) and the forbidden-API grep gate (`DateTime.now`, `Random`, sockets in pure packages).

## 2. Content-addressed contracts and bindings

- [x] 2.1 Vendor the pinned semantic set of `contract-v1.7` (`contracts/avatar-client/`) and `contract-v1.8` (`avatar-first-ui-profile` + `examples/avatar-first-ui/`) into `avc_contracts/assets/`; record both refs (exact commit + per-file SHA-256) in one `contract_pin.yaml`.
- [x] 2.2 Implement `verify_pin.dart` (runs first in CI; fails closed on drift; rejects a tag-only pin) and `sync_contracts.dart` (the only tool that reads a local openxFactory checkout).
- [x] 2.3 Generate the closed registry enums from the vendored registry YAML (`gen_contracts.dart --check` asserts no divergence).
- [x] 2.4 Hand-write the ~8 sealed AVC envelopes (session request/result, event, command, snapshot, structured confirmation, retention, persona) with value equality and JSON.
- [x] 2.5 Implement the Dart draft-2020-12 schema-conformance runner over `contracts/avatar-client/fixtures/index.yaml` as the CI type-faithfulness ground truth (locked decision 1: adopt Workiva `json_schema` behind a bounded spike over all fixture classes, with the named fallback trigger to port the keyword subset — see `supporting-docs/open-decisions.md`). The spike is a budgeted first task.

## 3. Session core (pure, deterministic)

- [x] 3.1 Implement `reduce(SessionState, InboundFrame) -> (SessionState, [Effect])` over a single ordered log, mirroring the reference-runtime invariants: monotonic sequence, `last_event_sequence` recovery cursor, `state_revision`/epoch fencing, `command_id` idempotency.
- [x] 3.2 Enforce media-authorized-observed-once (the barrier that unlocks speak/capture), the producer-authority guard (authoritative ⇒ approved producer), the revocation bound (→ credential-free terminal), and the snapshot barrier (fix, buffer, drain once, overflow → restart).
- [x] 3.3 Fail closed on unknown enum, unknown producer, or forbidden key → a safe view-state.
- [x] 3.4 Define the ports: `Clock`, `IdSource`, `SessionTransport`, `CommandSink`, `MediaTransport`. Live adapters are interfaces only in this change.

## 4. Fixture adapter and scenarios

- [x] 4.1 Implement `FixtureScenarioTransport` and `FixtureCommandSink`: replay an ordered scenario event stream on a virtual clock; script accepted/rejected/conflict command responses to close the loop.
- [x] 4.2 Add the openxFactory-owned neutral client-lab conformance fixtures and a client acceptance map, wiring in the inherited scenario set — the released `contracts/avatar-client/acceptance-map.yaml` and `examples/avatar-first-ui/avatar-first-ui-acceptance-map.yaml` already name this change as an owner change for named ACR/SCO/RBG/AFU scenarios (enumerated in `supporting-docs/acceptance-and-tests.md`); reuse `examples/avatar-first-ui/fixtures/` where they apply; contribute new neutral scenarios upstream. The openxFactory half landed: `contracts/avatar-client-lab/client-acceptance-map.yaml` transcribes the 13-requirement / 42-scenario inherited slice verbatim with per-scenario client evidence class (fixture/golden/successor), the nine gates, and the eleven a11y capabilities, machine-checked fail-closed by `scripts/validate-avatar-client.py::check_client_lab_acceptance_map` (+ tests); the three worked-scenario deterministic seeds (governed-denial, control-lost-failure, consent-withdraw-mid-speech) were contributed upstream to `examples/avatar-first-ui/fixtures/deterministic/`. The Flutter half remains: the codexFactory `apps/avatar-client-lab/` app consuming the map + fixtures to produce the reducer/golden evidence that flips scenario statuses. Box stays unchecked until that lands.
- [x] 4.3 Seed M0 from the released `examples/avatar-first-ui/fixtures/deterministic/offline-acceptance.yaml`; one loader normalizes the portable-conformance vs UI-example fixture shapes (locked decision 6: `index.yaml` authoritative for conformance, UI-example fixtures as scenario seeds). The seed fixture proves only the `listening` baseline — contribute a neutral `listening→thinking→speaking` extension fixture upstream so the six-state selector has a replayable proof path.
- [x] 4.4 Extend `scripts/validate-avatar-client.py` for successor-register deferral discharge (locked decision 7): (a) collect successor registers matching `contracts/avatar-client/evidence-register.*.yaml` alongside the released `evidence-register.yaml`, add that glob to `SEMANTIC_GLOBS`, and require every successor register to be listed in `contracts/manifest.yaml` so it is content-addressed; (b) allow a released `deferred` entry to be discharged by exactly one successor entry with `discharges_deferred: true` whose `owner_change` matches the released entry (keep the in-place `deferred->evidenced` flip illegal — `deferred` stays terminal; relax evidence-dup only for that released+discharging pair). Author `contracts/avatar-client/evidence-register.implement-avatar-client-lab.yaml` discharging this change's owned deferred inventory (SCO-001-S05; seedable from the dry-run artifact on `dryrun/fr040-evidence-discharge` @ d736fbe), and add negative coverage — a discharging entry with a mismatched `owner_change`, and a duplicate discharge of the same deferred entry, must both fail. Leaves the released register, acceptance map, and manifest byte-identical (no v1.10 re-release). Manifest registration of the successor register is deferred to this change's release realization step (the 005/v1.9 release-time manifest convention — bundle members are added to `contracts/manifest.yaml` only when the next additive contract version is cut, never mid-change); the validator therefore implements the manifest-listing requirement as release-time: it defers the successor's manifest-membership check pre-realization (a note) and fails it closed under `--require-realization`. This box stays unchecked until that release step registers the successor with its computed sha256. — DONE: successor register + validator discharge logic (`check_successor_discharge`, `--require-realization` manifest-membership, negative coverage) landed `d48ad25`; release-time manifest registration with computed sha256 (`8598efd…`) satisfied by `adopt-avatar-client-lab-candidates` task 5.1 in `d8cd3c2` (contract-v1.12 cut).

## 5. Avatar renderer

- [x] 5.1 Define the `AvatarView` leaf interface (`AvatarInput`: derived state, opaque intensity, injected phase, reducedMotion, opaque style token, semantics label) — no ticker, RNG, or wall clock.
- [x] 5.2 Implement `deriveAvatarState(viewState)`: authority → the six states, fail-closed (control-lost ⇒ `blocked`, never `speaking`).
- [x] 5.3 Implement `LightweightPortraitAvatar` (pure-Dart CustomPainter, app-owned animation controller) and a peer `TextOnlyAvatar`; per-state non-color cue; reduced-motion static frame. (Rive is a documented later swap behind the same interface.)

## 6. UI shell, modes, and accessibility

- [x] 6.1 Build `AdaptiveAvatarShell`: five persistent regions (avatar_stage, conversation_rail, context_panel, action_bar; handoff/settings as side-sheets) + an always-on `AuthorityStatusStrip` binding the four authoritative axes; responsive compact→kiosk; `textScaler`-aware; reflow at 400% zoom.
- [x] 6.2 Implement the three presentation modes (conversation/work/review) as client-local view emphasis over the same regions — never routes, never hiding authoritative status; seed from `profile.surface_default`.
- [x] 6.3 Implement `ui_kit`: the governed-action cards (canonical intent/approval only), the untrusted-content sanitizer (AFU-007), a11y primitives (live-region announcer, focus order, high-contrast + reduced-motion themes).
- [x] 6.4 Make the eleven accessibility-baseline capabilities gating tests; prove keyboard-only F1-F4 completion; pseudo-locale + RTL.

## 7. Developer lab harness

- [x] 7.1 Ship the harness behind a separate `main_lab.dart` entrypoint + `XF_LAB` compile-out + an `assert` that trips if harness widgets mount when `!kLab`.
- [x] 7.2 Implement the controls as fixture operations only: scenario selector, event step/scrub by sequence, latency + failure injection, viewport switch, pseudo-locale + reduced-motion toggles, emitted-event inspector (ordered AVC-04 log + `state_revision` + `last_event_sequence`).

## 8. Slice acceptance (F1-F4)

- [x] 8.1 M0 walking skeleton: one fixture end-to-end (reducer + static avatar + avatar_stage/conversation_rail + three harness controls) green on three gates — fixtures/index conformance, replay determinism, one VP-01 golden. The six-state transition arc (`listening→thinking→speaking`) is proven by the upstream extension fixture from task 4.3.
- [x] 8.2 F1 Shell: regions, status strip, responsiveness, keyboard/text-only/reduced-motion, persona continuity.
- [x] 8.3 F2 Deterministic session: every canonical state reached by a fixture with a golden + event assertion; retention asymmetry; event-gap → AVC-12 recovery; lease/epoch takeover.
- [x] 8.4 F3 Service intake: happy path, ask-only-the-gap, consequential correction (supersede AVC-06), decline/withdraw, offline draft (desktop; web closed-default), idempotency-keyed conflict.
- [x] 8.5 F4 Governed actions: intent/approval rendering only, confirmation-first bound to the exact effect, denied ≠ failed ≠ cancelled, policy-loss pauses actions, handoff shows scope with no token.
- [x] 8.6 Author the golden strategy (locked decision 5: authoritative goldens on the Linux CI job only, bundled pinned font + version-pinned SDK; Windows + web run all tests except pixel goldens; web = headless-Chrome smoke); every golden flake treated as a determinism bug, never a tolerance to widen. — Swept 2026-07-17: strategy encoded (test_config/golden_config.dart Linux-only golden authority + ci.yaml matrix); the Windows + web legs have not actually executed — tracked under the open 9.1 gate.

## 9. Realization

- [ ] 9.1 [GATE] Confirm the offline lab is green on the implemented target: `verify_pin` + schema conformance + replay determinism + boundary/forbidden-API gates + keyboard-only F1-F4 + the golden set, on Windows + web (locked decision 4: a11y qualified on Windows desktop; a documented WCAG exception register for canvas web; no web AA claim in F1-F4). — Housecleaning 2026-07-17: NOT satisfied as-worded — only the Linux bench run is recorded (release-evidence.md); apps/avatar-client-lab/.github/workflows/ci.yaml is a non-triggering template with no repo-root caller, so no Windows/web evidence exists. Discharge options parked for Brett: (a) stand up a repo-root CI caller and record a real Windows+web matrix run, or (b) ratify a disposition that Linux-bench green + the portable suite + the WCAG web exception register is the accepted v1 realization with Windows/web deferred.
- [x] 9.2 Record the client release evidence (pinned contract refs, fixture-conformance result, dependency lock, license check, secret scan, test + golden result) in codexFactory. — Swept 2026-07-17: docs/release-evidence.md (T102) records pinned refs, gate results, and suite outcomes; note it predates the 2026-07-16 v1.12 resync, whose vendored P7/P8 fixtures closed the 18 tracked gaps it lists.
- [x] 9.3 Land the openxFactory-side artifacts (client-lab conformance fixtures + acceptance map + boundary rule) and link the codexFactory `apps/avatar-client-lab/` path in the openxFactory README OpenSpec Records; sync the codexFactory pin as a routine submodule-pointer commit. — Complete 2026-07-16: openxFactory artifacts landed (558c254 + adopt-change realization); README link present; final clause satisfied by aggregation pointer sync `5dfc06f` (codexFactory → 0fed12c = PR #17 merge, openxFactory → 06f0be3). The earlier "satisfied by adopt 6.1" note conflated the app-internal vendored-pin resync with this submodule-pointer sync — they are distinct; both now done.
- [ ] 9.4 Archive this change once merge evidence and a green run exist on both code surfaces.
