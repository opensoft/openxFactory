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
| AFU-001 Adaptive shell over orthogonal runtime state | `deterministic/offline-acceptance.yaml` (AFU-001-S01), `negative/authority-transition.yaml` (AFU-001-S03), standard §15 | — |
| AFU-002 Hermes-layer surface defaults | four archetype examples in `../domain-overlays.example.yaml`, standard §16 | — |
| AFU-003 Flutter client / web-console split | standard §21 (boundary + handoff URL rules) | `implement-avatar-client-lab` (client), workflow-visualization (console) |
| AFU-004 Standard controls, recording awareness, fallback | `negative/mode-reserved.yaml` (S01), `held-answer-active.yaml` (S02), `control-fallback-missing.yaml` (S04), `timing-out-of-range.yaml` (S05), standard §17–§18 | `implement-avatar-client-lab` (widget/live) |
| AFU-005 Accessibility & localization baseline | structured `accessibility_baseline` in examples, standard §22 | `avatar-pilot-hardening` (WCAG audit, platform qualification) |
| AFU-006 Persona presentation & disclosure | `negative/persona-unresolved.yaml` (S02), `purpose-invalid.yaml` (S03), `retention-unresolved.yaml` (S04), standard §19 | — |
| AFU-007 Untrusted content & external-action rendering | `negative/unsafe-render.yaml` (S01), standard §20 | `implement-avatar-client-lab` (widget architecture test) |
| AFU-008 Deterministic UI acceptance | `deterministic/offline-acceptance.yaml` (S01), validator determinism check | `implement-avatar-client-lab` (goldens), live-provider replay |

The negative fixtures also anchor the nine enforced validator rule classes (see
`../../../specs/004-avatar-first-ui/contracts/validator-rules.md`). The offline
validator enforces acceptance-map parity (`AFUV-PARITY-ACCEPTANCE`): 8 requirements
/ 25 scenarios, and every fixture `evidence_id` must be a real scenario ID.
