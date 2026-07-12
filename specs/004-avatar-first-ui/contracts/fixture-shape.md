# Contract: Deterministic UI Fixture Shape

**Target directory**: `examples/avatar-first-ui/fixtures/` (NEW — Q3=A, FR-023)
**Kind**: `xfactory_avatar_first_ui_fixture` (each fixture carries
`schema_version` + `kind`)
**Determinism**: fixtures pin their own inputs; two identical runs yield
equivalent `expected` shapes and identical `evidence_ids` (SC-006). No live
model, provider, clock, or RNG.

Fixtures are **separate** from the profile examples in
`examples/avatar-first-ui/domain-overlays.example.yaml`: examples are carrier
profiles; fixtures are deterministic UI test shapes.

## Directory layout

```text
examples/avatar-first-ui/fixtures/
├── README.md                 # index + evidence-ID → fixture map (linked from examples/README.md)
├── compatibility/            # pre-alignment profiles that MUST still validate
│   └── legacy-persona-catalog.yaml
└── negative/                 # one fixture per enforced rule class (9; see validator-rules.md)
    ├── authority-transition.yaml
    ├── timing-out-of-range.yaml
    ├── control-fallback-missing.yaml
    ├── persona-unresolved.yaml
    ├── mode-reserved.yaml
    ├── unsafe-render.yaml
    ├── purpose-invalid.yaml
    ├── held-answer-active.yaml
    └── retention-unresolved.yaml
```

## Fixture shape (positive / determinism)

```yaml
schema_version: 1
kind: xfactory_avatar_first_ui_fixture
fixture_id: <stable-id>
evidence_ids: [AFU-00X-S0Y, ...]     # AFU SCENARIO IDs attested; the acceptance map's
                                     # evidence ID derives via evidence_id_template:
                                     # TEST-{scenario_id} (e.g. TEST-AFU-001-S01)
inputs:
  clock: "2026-07-11T00:00:00Z"      # fixed
  ids: [ ... ]                       # fixed IDs (session, workflow, persona ref)
  font: "<pinned bundled family incl. RTL face>"
  locale: en | pseudo-longstring-bidi
  platform_capabilities: { keyboard: true, screen_reader: true, ... }
canonical:                            # canonical AVC inputs (no provider DTOs)
  commands: [ ... ]
  events: [ ... ]                     # e.g. media_authorized, control_lost, avc12_snapshot
  snapshot: { ... }
expected:                             # declared canonical view-state / record shapes
  view_state: { presentation_mode, media_state, control_state, workflow_projection }
  records: [ ... ]
```

## Fixture shape (negative)

Same as above plus a single expected failure:

```yaml
expect_error: AFUV-<RULE>            # the ONE stable error/evidence ID this fixture triggers
```

A negative fixture MUST fail exactly its `expect_error` rule (one primary rule
per fixture — Q6=A). The validator asserts the emitted `ERROR <id>` matches.

## Compatibility fixture

A pre-alignment profile (including the legacy embedded `persona_catalog`, no new
runtime blocks) that MUST validate clean under `--mode baseline`, proving
additive-with-closed-defaults compatibility (D7, D12, FR-016, SC-003).

## Evidence mapping

`fixtures/README.md` maps each `AFU-*` requirement/scenario to the fixture(s)
that attest it (automated evidence) or to the named successor that owns deferred
evidence (`implement-avatar-client-lab`, `avatar-pilot-hardening`). This mirrors
the OpenSpec acceptance map
(`openspec/changes/align-avatar-first-ui-standard/supporting-docs/avatar-first-ui-acceptance-map.yaml`)
and is checked by `AFUV-PARITY-ACCEPTANCE`. Evidence-ID convention: a fixture's
`evidence_ids` are the acceptance map's scenario IDs (`AFU-*-S0Y`); the map's
evidence ID for each is derived by its `evidence_id_template: TEST-{scenario_id}`
(e.g. `TEST-AFU-001-S01`). The parity check binds fixtures to the map on that
derivation, so fixtures never hand-author `TEST-` IDs.
