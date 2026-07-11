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
└── negative/                 # one fixture per enforced rule class (nine)
    ├── authority-transition.yaml       # AFUV-AUTHORITY-TRANSITION
    ├── timing-out-of-range.yaml        # AFUV-TIMING-OUT-OF-RANGE
    ├── control-fallback-missing.yaml   # AFUV-CONTROL-FALLBACK-MISSING
    ├── persona-unresolved.yaml         # AFUV-PERSONA-UNRESOLVED
    ├── mode-reserved.yaml              # AFUV-MODE-RESERVED
    ├── unsafe-render.yaml              # AFUV-UNSAFE-RENDER
    ├── purpose-invalid.yaml            # AFUV-PURPOSE-INVALID
    ├── held-answer-active.yaml         # AFUV-HELD-ANSWER-ACTIVE
    └── retention-unresolved.yaml       # AFUV-RETENTION-UNRESOLVED
```

## Evidence-ID convention

Each fixture's `evidence_ids` are the acceptance map's scenario IDs
(`AFU-<req>-S<nn>`, e.g. `AFU-001-S01`). The acceptance map
(`openspec/changes/align-avatar-first-ui-standard/supporting-docs/avatar-first-ui-acceptance-map.yaml`)
derives each evidence ID via `evidence_id_template: TEST-{scenario_id}` (e.g.
`TEST-AFU-001-S01`). Fixtures never hand-author `TEST-` IDs; the parity check
(`AFUV-PARITY-ACCEPTANCE`) resolves fixture scenario IDs against the map.

## Requirement → evidence map

The evidence map binding each `AFU-*` requirement/scenario to a fixture or a
named successor is populated in the US3 phase (task T025); the negative fixtures
also anchor the nine enforced validator rule classes (see
`../../../specs/004-avatar-first-ui/contracts/validator-rules.md`). Flutter
widget, golden, platform-accessibility, and live-provider evidence remain
successor-owned (`implement-avatar-client-lab`, `avatar-pilot-hardening`).
