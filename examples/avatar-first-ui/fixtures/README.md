# Avatar-First UI Deterministic Fixtures

Status: draft
Kind: register
Repository context: openxFactory
Proposed by: align-avatar-first-ui-standard

Deterministic UI fixture shapes for the avatar-first UI standard. These are
**separate** from the domain profile examples in
`../domain-overlays.example.yaml`: examples are carrier profiles; fixtures are
deterministic UI test shapes checked offline by
`scripts/validate-avatar-first-ui.py` (no live model, provider, clock, or RNG).

## Layout

```text
fixtures/
├── README.md                 # this index + evidence map
├── compatibility/            # pre-alignment profiles that MUST still validate
│   └── legacy-persona-catalog.yaml
├── deterministic/            # offline-replayable canonical AVC command/event/snapshot -> view-state
│   ├── offline-acceptance.yaml          # listening (capture_authorized) baseline
│   ├── six-state-transition-arc.yaml    # listening -> thinking -> speaking extension (task 4.3)
│   ├── governed-action-denial.yaml      # governed denial outcome; avatar never speaks (task 4.2, claim 5b)
│   ├── control-lost-failure.yaml        # fail-closed control loss -> avatar blocked (task 4.2, claim 5b)
│   ├── consent-withdraw-mid-speech.yaml # consent withdrawn while speaking -> media terminated (task 4.2, claim 5c)
│   │   # --- adopted client-lab candidates (adopt-avatar-client-lab-candidates) ---
│   │   # P7 intake-set breadth (FR-025); all AFU-001-anchored
│   ├── intake-happy-path.yaml                 # guided intake -> AVC-06 confirm -> outcome_slot completion
│   ├── intake-ask-only-the-gap.yaml           # asks only the missing slot; never re-asks filled ones
│   ├── intake-supersede-correction.yaml       # AVC-06 v1 voided by superseding v2; stale decision rejected
│   ├── intake-decline-withdraw.yaml           # resemblance-only transcript decides nothing; explicit decline -> abandoned
│   ├── intake-idempotency-conflict.yaml       # idempotent retry no double-apply; changed field -> idempotency_conflict
│   │   # P8 takeover/epoch-fence + snapshot-barrier recovery
│   ├── stale-revision-command-fenced.yaml     # ACR-004-S03 stale state_revision fenced (command_conflict)
│   ├── lease-epoch-takeover.yaml              # second-instance denied; stale epoch fenced (command_rejected/second_instance_denied)
│   ├── snapshot-barrier-recovery.yaml         # ACR-004-S05 gap -> buffer -> drain once
│   ├── snapshot-barrier-overflow-restart.yaml # overflow -> restart, never a silent drop
│   │   # P11 the two FR-019 avatar states no landed seed reached
│   ├── avatar-interrupted-barge-in.yaml       # barge-in supersedes in-flight speaking -> interrupted
│   ├── avatar-handoff-escalation.yaml         # workflow escalates to a human -> handoff
│   │   # P12/P13 kernel-media.state reachability denominator (evidenced via canonical.snapshot, not view_state)
│   ├── det-media-state-permission.yaml        # kernel media_state: permission
│   ├── det-media-state-capture-pending.yaml   # kernel media_state: capture_pending
│   ├── det-media-state-capture-authorized.yaml# kernel media_state: capture_authorized
│   ├── det-media-state-capture-active.yaml    # kernel media_state: capture_active
│   ├── det-media-state-listening.yaml         # kernel media_state: listening
│   ├── det-media-state-speaking.yaml          # kernel media_state: speaking
│   ├── det-media-state-governed-action-pending.yaml # kernel media_state: governed_action_pending
│   ├── det-media-state-retention-active.yaml  # kernel media_state: retention_active
│   └── det-control-degraded.yaml              # kernel control_health: degraded -> control_degraded (P13)
└── negative/                 # ≥1 fixture per enforced rule class (nine classes; 12 fixtures)
    ├── authority-transition.yaml       # AFUV-AUTHORITY-TRANSITION      (class 1)
    ├── timing-out-of-range.yaml        # AFUV-TIMING-OUT-OF-RANGE       (class 2)
    ├── timing-float-out-of-range.yaml  # AFUV-TIMING-OUT-OF-RANGE       (class 2, non-int type)
    ├── control-fallback-missing.yaml   # AFUV-CONTROL-FALLBACK-MISSING  (class 3)
    ├── control-required-missing.yaml   # AFUV-CONTROL-FALLBACK-MISSING  (class 3, required omitted)
    ├── persona-unresolved.yaml         # AFUV-PERSONA-UNRESOLVED        (class 4)
    ├── mode-reserved.yaml              # AFUV-MODE-RESERVED             (class 5)
    ├── unsafe-render.yaml              # AFUV-UNSAFE-RENDER             (class 6)
    ├── purpose-invalid.yaml            # AFUV-PURPOSE-INVALID           (class 7)
    ├── held-answer-active.yaml         # AFUV-HELD-ANSWER-ACTIVE        (class 8)
    ├── retention-unresolved.yaml       # AFUV-RETENTION-UNRESOLVED      (class 9)
    └── accessibility-invalid.yaml      # AFUV-ACCESSIBILITY-INVALID     (structural accessibility check)
```

## Evidence-ID convention

Each fixture's `evidence_ids` are the acceptance map's scenario IDs
(`AFU-<req>-S<nn>`, e.g. `AFU-001-S01`). The acceptance map
(`examples/avatar-first-ui/avatar-first-ui-acceptance-map.yaml`)
derives each evidence ID via `evidence_id_template: TEST-{scenario_id}` (e.g.
`TEST-AFU-001-S01`). Fixtures never hand-author `TEST-` IDs; the parity check
(`AFUV-PARITY-ACCEPTANCE`) resolves fixture scenario IDs against the map.

## Requirement → evidence map

Every `AFU-*` requirement resolves to owned offline evidence (a fixture or the
examples/validator) or a named successor. Fixture `evidence_ids` are scenario IDs
(`AFU-*-S*`); the acceptance map derives each evidence ID as `TEST-{scenario_id}`.
Flutter widget, golden, platform-accessibility, and live-provider evidence remain
successor-owned.

| Requirement | Owned offline evidence (this change) | Successor-owned (deferred) |
| --- | --- | --- |
| AFU-001 Adaptive shell over orthogonal runtime state | `deterministic/offline-acceptance.yaml` (AFU-001-S01), `deterministic/six-state-transition-arc.yaml` (AFU-001-S01), `negative/authority-transition.yaml` (AFU-001-S03), standard §15 | — |
| AFU-002 Hermes-layer surface defaults | four archetype examples in `../domain-overlays.example.yaml`, standard §16 | — |
| AFU-003 Flutter client / web-console split | standard §21 (boundary + handoff URL rules) | `implement-avatar-client-lab` (client), workflow-visualization (console) |
| AFU-004 Standard controls, recording awareness, fallback | `negative/mode-reserved.yaml` (S01), `held-answer-active.yaml` (S02), `deterministic/governed-action-denial.yaml` (S03), `control-fallback-missing.yaml` (S04), `timing-out-of-range.yaml` + `deterministic/control-lost-failure.yaml` (S05), standard §17–§18 | `implement-avatar-client-lab` (widget/live) |
| AFU-005 Accessibility & localization baseline | structured `accessibility_baseline` in examples, `deterministic/six-state-transition-arc.yaml` (AFU-005-S03), standard §22 | `avatar-pilot-hardening` (WCAG audit, platform qualification) |
| AFU-006 Persona presentation & disclosure | `negative/persona-unresolved.yaml` (S02), `purpose-invalid.yaml` + `deterministic/consent-withdraw-mid-speech.yaml` (S03), `retention-unresolved.yaml` (S04), standard §19 | — |
| AFU-007 Untrusted content & external-action rendering | `negative/unsafe-render.yaml` (S01), standard §20 | `implement-avatar-client-lab` (widget architecture test) |
| AFU-008 Deterministic UI acceptance | `deterministic/offline-acceptance.yaml` (S01), `deterministic/six-state-transition-arc.yaml` (S01, listening→thinking→speaking extension), validator determinism check | `implement-avatar-client-lab` (goldens), live-provider replay |

The three task-4.2 deterministic seeds (`governed-action-denial`,
`control-lost-failure`, `consent-withdraw-mid-speech`) are the replayable
worked-scenario seeds for the client-lab acceptance map
(`contracts/avatar-client-lab/client-acceptance-map.yaml`); they carry the
denial-vs-failure and consent-withdraw distinctions the lab must render
(`supporting-docs/acceptance-and-tests.md` claim 5).

The negative fixtures also anchor the nine enforced validator rule classes (see
`../../../specs/004-avatar-first-ui/contracts/validator-rules.md`). The offline
validator enforces acceptance-map parity (`AFUV-PARITY-ACCEPTANCE`): 8 requirements
/ 25 scenarios, and every fixture `evidence_id` must be a real scenario ID.

## Adopted client-lab candidate fixtures (adopt-avatar-client-lab-candidates)

Twenty deterministic seeds adopted verbatim (D6 header swap only) from codexFactory
branch `002-avatar-client-lab` @ `3a8fbd5` (7/7 panel-confirmed; provenance in
`specs/002-avatar-client-lab/upstream-drafts/STATUS.md`). They lift the deterministic
seed count from 5 to 25. All `evidence_ids` reuse existing scenarios, so the map's
`8`/`25` requirement/scenario counts are unchanged. The P12/P13 seeds evidence the
closed kernel `media.state` reachability **denominator** from `canonical.snapshot`
(settled law L4 — kernel fields, never `expected.view_state`); the others evidence
intake-workflow, takeover/recovery, and `interrupted`/`handoff` avatar-state scenarios.

| Fixture | Family / P-row | Evidences | `evidence_ids` |
| --- | --- | --- | --- |
| `intake-happy-path.yaml` | P7 intake (FR-025) | ACR-006-S02 exact-effect confirm | AFU-001-S01, AFU-001-S02 |
| `intake-ask-only-the-gap.yaml` | P7 intake | ask-only-the-gap breadth | AFU-001-S01 |
| `intake-supersede-correction.yaml` | P7 intake | ACR-006-S03 stale/superseded confirmation | AFU-001-S02, AFU-001-S03 |
| `intake-decline-withdraw.yaml` | P7 intake | ACR-006-S04 resemblance-only + explicit decline | AFU-001-S02 |
| `intake-idempotency-conflict.yaml` | P7 intake | ACR-004-S02 + ACR-010-S03 idempotency | AFU-001-S01, AFU-001-S03 |
| `stale-revision-command-fenced.yaml` | P8 takeover | ACR-004-S03 stale-revision fence | AFU-001-S03, AFU-008-S01 |
| `lease-epoch-takeover.yaml` | P8 takeover | second-instance denial + epoch fence (T106; no ACR home) | AFU-004-S03, AFU-008-S01 |
| `snapshot-barrier-recovery.yaml` | P8 recovery | ACR-004-S05 barrier drain-once | AFU-001-S03, AFU-008-S01 |
| `snapshot-barrier-overflow-restart.yaml` | P8 recovery | barrier overflow -> restart (no ACR home) | AFU-001-S03, AFU-008-S01 |
| `avatar-interrupted-barge-in.yaml` | P11 avatar-state | `interrupted` reachability (FR-012/SC-002) | AFU-008-S01, AFU-001-S01, AFU-005-S03 |
| `avatar-handoff-escalation.yaml` | P11 avatar-state | `handoff` reachability (FR-012/SC-002) | AFU-006-S04, AFU-001-S01, AFU-008-S01 |
| `det-media-state-permission.yaml` | P12 denominator | kernel `media_state: permission` | AFU-008-S01, AFU-006-S01 |
| `det-media-state-capture-pending.yaml` | P12 denominator | kernel `media_state: capture_pending` | AFU-008-S01, AFU-004-S02 |
| `det-media-state-capture-authorized.yaml` | P12 denominator | kernel `media_state: capture_authorized` | AFU-008-S01, AFU-004-S01 |
| `det-media-state-capture-active.yaml` | P12 denominator | kernel `media_state: capture_active` | AFU-008-S01, AFU-004-S01 |
| `det-media-state-listening.yaml` | P12 denominator | kernel `media_state: listening` | AFU-008-S01, AFU-001-S01 |
| `det-media-state-speaking.yaml` | P12 denominator | kernel `media_state: speaking` | AFU-008-S01, AFU-001-S01 |
| `det-media-state-governed-action-pending.yaml` | P12 denominator | kernel `media_state: governed_action_pending` | AFU-008-S01, AFU-001-S02 |
| `det-media-state-retention-active.yaml` | P12 denominator | kernel `media_state: retention_active` | AFU-008-S01, AFU-006-S04 |
| `det-control-degraded.yaml` | P13 denominator | kernel `control_health: degraded` -> `control_degraded` | AFU-008-S01, AFU-004-S05 |

By requirement, the adopted fixtures anchor: **AFU-001** (all five P7 seeds; P8
`stale-revision-command-fenced`/`snapshot-barrier-recovery`/`snapshot-barrier-overflow-restart`;
both P11 seeds; P12 `listening`/`speaking`/`governed-action-pending`); **AFU-004**
(P8 `lease-epoch-takeover`; P12 `capture-pending`/`capture-authorized`/`capture-active`;
P13 `control-degraded`); **AFU-005** (P11 `avatar-interrupted-barge-in`); **AFU-006**
(P11 `avatar-handoff-escalation`; P12 `permission`/`retention-active`); **AFU-008**
(the P8, P11, and all nine P12/P13 seeds). Two P12/P13 anchors are nearest-fit, not
dedicated (`control-degraded` -> AFU-004-S05 "control lost"; `retention-active` ->
AFU-006-S04 "handoff") — noted so no dedicated control-degraded/retention scenario
coverage is inferred.
