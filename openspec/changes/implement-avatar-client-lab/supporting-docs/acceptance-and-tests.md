# Acceptance and Tests — avatar client lab

Status: draft
Proposed by: implement-avatar-client-lab
Kind: architecture
Summary: The F1-F4 acceptance foci, the released scenario IDs the lab discharges
across the avatar-client (contract-v1.7) and avatar-first-ui (contract-v1.8)
acceptance maps, and the determinism/golden/conformance/pin CI gate set — the
acceptance surface a proposal author needs before writing spec deltas.
Topics: avatar-client, acceptance, conformance, determinism, golden, ci-gates, scenario-map, accessibility, fixtures
Repository context: openxFactory (neutral acceptance map + conformance fixtures); the Flutter evidence is produced in codexFactory `apps/avatar-client-lab/`
Staging ID: openxFactory:staging:avatar-client-lab
Source: v1 brainstorm 2026-07-13 (six-dimension synthesis); grounded in the released `contracts/avatar-client/` kernel (contract-v1.7) and `contracts/schemas/avatar-first-ui-profile.schema.yaml` + `examples/avatar-first-ui/` (contract-v1.8)

Supporting fragment for [avatar-client-lab.md](avatar-client-lab.md). The primary
fragment scopes the lab and [architecture-and-stack.md](architecture-and-stack.md)
gives the design; this one names the acceptance obligations the proposal inherits
so `implement-avatar-client-lab` can be authored without re-deriving them. The
whole topic says "F1-F4" nine times and never defines it, and the two released
acceptance maps already name `implement-avatar-client-lab` as an owner of specific
deferred scenarios that no current fragment records. That is the gap this closes.
Not final spec text.

## Claims

1. **F1-F4 are acceptance foci, not delivery rings — and the proposal must state
   them.** Recommended decomposition, to confirm or override: **F1 Adaptive shell
   & authority status** — five persistent regions + always-on authoritative status
   strip + three client-local presentation modes, projection derived from an AVC-12
   snapshot (AFU-001, AFU-002, AFU-003 client half). **F2 Governed interaction &
   confirmation** — service-intake workflow, governed-action cards rendering only
   canonical intent/approval, effect-bound AVC-06 confirmation, denial-vs-failure
   rendering, consent-before-capture surfacing (AFU-004, AFU-007; client-behavioral
   half of ACR-004/005/006/009/010). **F3 Avatar presentation seam** — the six-state
   avatar behind `AvatarView`, state derived from authority, control-lost ⇒
   `blocked`, no lip-sync, reduced-motion static golden (AFU-006 + the derivation
   invariants). **F4 Accessibility, localization & determinism harness** — the
   eleven baseline capabilities, keyboard-only completion, non-color cues, text-only
   peer renderer, pseudo-locale, the dev harness, and the determinism/golden/
   conformance gates (AFU-005, AFU-008). M0 is a tracer through F1+F2 only.

2. **The lab both ADDs `avatar-client-lab` and discharges named scenarios in four
   already-released capabilities.** The proposal is not greenfield: the released
   maps list `implement-avatar-client-lab` as an `owner_change` for a fixed,
   enumerable set. It must be recorded verbatim, not re-invented. From
   `contracts/avatar-client/acceptance-map.yaml` (avatar-client-runtime):
   ACR-004, ACR-005, ACR-006, ACR-009, ACR-010, and the fail-closed media-gate
   slice of ACR-003. From the same map: SCO-001 (the lab is the first real
   content-addressed *consumer*), SCO-002, RBG-001 (client-repo boundary), and —
   the one scenario the evidence-register defers *explicitly* to this change —
   SCO-001-S05 (a provider event is added → it stays in the owning adapter unless a
   reviewed neutral evolution justifies it). From
   `examples/avatar-first-ui/avatar-first-ui-acceptance-map.yaml`: AFU-003, AFU-005,
   AFU-007, AFU-008. The `avatar-client-lab` capability the primary fragment ADDs
   carries the lab-native requirements (non-production boundary, dual-bundle
   content-addressed consumption, fixture-replay determinism, re-derives-never-
   decides authority, the replaceable six-state seam, the accessibility baseline,
   the repo boundary, the fail-closed deferral seam).

3. **The lab's evidence is client behavior, not schema re-proof.** The kernel
   already evidences the schema layer of the shared scenarios (e.g.
   `TEST-ACR-004-S06` unauthorized-producer, `TEST-ACR-008-S03` weakened gate) by
   replaying `fixtures/index.yaml` through the real draft-2020-12 validator. The lab
   does not re-author those assertions; it adds the *behavioral half* — that the
   pure reducer and the widgets react correctly to the same canonical inputs (an
   unauthorized-producer event is dropped by the reducer and never reaches an
   authoritative transition; a weakened gate never enables speech). Schema
   faithfulness stays the CI ground truth (arch claim 5); the lab layers reducer +
   golden evidence on top.

4. **Nine CI gates, all offline and network-free.** (i) *Schema-conformance* —
   replay every `contracts/avatar-client/fixtures/index.yaml` case and the twelve
   `examples/avatar-first-ui/fixtures/negative/*` cases through the real validator;
   each `expect: valid|invalid` and each `AFUV-*`/error class fires exactly as
   declared. (ii) *Content-addressed pin* — a `contract_pin.yaml` records the exact
   openxFactory commit and per-file SHA-256 for both bundles' digested sets and
   verifies them against the published `contracts/manifest.yaml`; a tag-only pin
   fails (SCO-001-S03, `release_pin_cases`). (iii) *Replay determinism* — each
   canonical fixture replayed twice yields byte-identical normalized view-state
   (AFU-008-S01). (iv) *Golden* — frame-exact goldens on the Linux CI job only,
   injected phase, reduced-motion static frame as the renderer-swap contract; any
   flake is a determinism bug, not a tolerance to widen (open-decision 5). (v)
   *Accessibility* — the eleven `accessibility_baseline` capabilities as gating
   tests + keyboard-only F1-F4 completion + per-state non-color-cue presence, on
   desktop (open-decision 4). (vi) *Authority derivation* — presentation state is a
   pure function of media/control authority; control_lost/control_degraded never map
   to `speaking`; the client emits no authoritative event and executes no tool call
   (AFU-004-S05, ACR-004-S06, ACR-005-S01). (vii) *Production boundary* — the
   `main_lab.dart` harness is compiled out of and asserted absent from the
   production build; no provider credential or server tool handler exists in the
   owned surface (RBG-001). (viii) *Fail-closed seam* — the deferred live ports ship
   fixture adapters whose defaults hold the `interface-lock` closed set
   (offline_drafts disabled, attachments reference_only, second_instance denied,
   reserved mode/gate preflight-fails-to-text_or_handoff). (ix) *Evidence
   completeness* — every `avatar-client-lab` scenario resolves to a fixture, a
   golden, or a named successor, or CI fails; this is the lab's self-gating analog
   of ACR-012-S03 / AFU-008-S03.

5. **Three worked scenarios the proposal must carry — because their absence hides
   the load-bearing distinctions.** (a) *M0 tracer* binds to the one released
   deterministic fixture, `examples/avatar-first-ui/fixtures/deterministic/
   offline-acceptance.yaml`: fixed clock `2026-07-11T00:00:00Z`, session `sess-0001`,
   persona `neutral.guide` v1; canonical `start_session` → authoritative
   `session_started`, `media_authorized` → expected view-state {presentation_mode:
   conversation, media_state: capture_authorized, control_state: healthy,
   workflow_projection: intake} with two records, carrying evidence_ids AFU-008-S01,
   AFU-001-S01, AFU-004-S01. Note this fixture stops at `capture_authorized` and
   emits no speaking event, so the avatar arc it can prove is listening → (idle),
   *not* the listening → thinking → speaking arc the arch M0 narrative asserts;
   driving `speaking` needs additional canonical response events the lab must
   contribute upstream (arch claim 7). (b) *Governed-action denial vs failure* — a
   denial is an authoritative negative *outcome* rendered faithfully (AVC-02
   `result_kind: denial`, e.g. `reason: consent_missing`, `fallback_modes:
   [text, human_handoff]`, `safe_message_key`; AVC-02 makes denial/terminal
   structurally incapable of carrying a credential or SDP), surfaced through
   `outcome_slots`/`fallback_slots`, with the avatar never entering `speaking`
   (AFU-004-S03). A failure is a *fail-closed local safety transition* nobody
   authored (control_lost or an event-sequence gap): avatar → `blocked`, governed
   commands disabled, snapshot recovery required (ACR-005-S01, ACR-004-S04). The two
   must render differently; a proposal that conflates them ships a client that
   treats governance denials as crashes. (c) *Consent-withdraw mid-speech* — a
   fixture drives an authoritative consent-withdrawn event while `speaking`; the
   fixture adapter terminates the media leg within the revocation bound, the avatar
   leaves `speaking`, capture stops, and media-gated governed commands disable
   (AFU-006-S03, ACR-008-S04 client-behavioral half).

6. **The eleven accessibility capabilities are named, gating, and split by
   platform.** The released `accessibility_baseline` block enumerates exactly
   eleven booleans — keyboard_operation, stable_focus, visible_focus,
   screen_reader_announcements, captions, text_only_mode, reduced_motion,
   high_contrast, non_color_cues, zoom_reflow, pseudo_locale_coverage. The lab binds
   each to a gating test on the qualified desktop platform (open-decision 4) and
   records the web-canvas WCAG exceptions in a register rather than claiming web AA.
   `pseudo_locale_coverage` + `zoom_reflow` prove the localization/reflow path
   without real i18n; `text_only_mode` is the text-only peer renderer.

7. **The content-addressed pin anchors to the published manifest, and the v1.8 set
   still needs an index.** `contracts/manifest.yaml` (contract_bundle_version:
   contract-v1.8) already publishes per-file SHA-256 for both the AVC kernel
   (contract-v1.7) and the avatar-first-ui-profile schema, so the lab verifies its
   pin against that manifest rather than maintaining a divergent digest list. But
   the v1.7 README enumerates only the kernel's digested semantic set (8 schemas +
   shared-definitions + 9 registries + fixtures/index + acceptance-map +
   interface-lock + evidence-register); the v1.8 UI-profile set (the schema, its
   acceptance map, and its per-file fixtures — which have *no* `index.yaml`) has no
   published index, so the lab's conformance runner must enumerate it and cover two
   different fixture manifest shapes (self-describing index vs per-file
   `expect_error`).

## Open questions

1. **Does discharging a deferred scenario owned by a released capability require a
   MODIFIED spec delta to that capability, or only an evidence-register update
   recorded under `implement-avatar-client-lab`?** The lab flips scenarios like
   SCO-001-S05 and the AFU-003/005/007/008 successor slots from deferred to
   evidenced across capabilities it does not own. *Recommendation:* record the
   client evidence in each released capability's evidence-register under this change
   (no requirement text changes), and reserve a MODIFIED delta only where a scenario's
   fail-closed default is actually restated — but confirm this against the OpenSpec
   parity validator before authoring, since it gates strict validation.

2. **Confirm or override the F1-F4 acceptance-focus boundary (claim 1).** It is
   currently undefined anywhere in the topic; the proposal cannot enumerate task
   groups until the four foci and their scenario clusters are locked. *Recommendation:*
   adopt the four-way split above; it aligns cleanly to the AFU-001..008 clusters and
   keeps M0 inside F1+F2.

3. **Is the manifest the authoritative pin source, or a `contract_pin.yaml` derived
   from it (claim 7)?** *Recommendation:* pin the exact commit and verify per-file
   digests against `contracts/manifest.yaml`; treat any lab-local digest list as a
   cache that CI re-derives, so the pin can never silently drift from the published
   bundle. Resolves the two-bundle half of open-decision 3.

## Exit

Fold this fragment into `implement-avatar-client-lab` (`code_surface: openxFactory,
codexFactory`; `target_release: implemented`) alongside the other three.
At the proposal gate its claims become the change's acceptance map + evidence
register (the inherited scenario IDs of claim 2 wired to fixtures, goldens, and
named successors) and the F1-F4 task grouping; claim 4's nine gates become the
change's CI contract.
