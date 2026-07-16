# avatar-first-ui — deterministic acceptance delta

## MODIFIED Requirements

### Requirement: Deterministic UI acceptance
Deterministic client slices SHALL use fixed clocks, IDs, fonts, locale
fixtures, platform capabilities, and canonical AVC commands, events, and
snapshots without a live model, and every acceptance scenario SHALL map to
automated evidence, manual evidence, or both. Avatar presentation-state
derivation SHALL conform to the landed neutral avatar-state derivation table
(the `avatar-lab-evidence` capability), which subsumes the former
interim-invariant-only posture; the deterministic fixture corpus SHALL give
every closed `media.state` — and the intake-remainder, takeover/recovery,
and `interrupted`/`handoff` scenario families — a replayable proof path
evidenced through kernel fields only. Golden tests SHALL render on
one pinned CI platform with one bundled font family including an
RTL-capable face, covering the qualified wide, narrow, and zoomed viewports
plus one long-string/bidirectional composite; high-contrast, reduced-motion,
and text-only verification SHALL use semantics and behavior assertions
rather than pixel goldens. Live provider tests SHALL reuse the same reducer
and view projections.

#### Scenario: Offline acceptance is replayed
- **WHEN** the same fixture, seed, decisions, and contract version run twice
- **THEN** canonical view state, commands, events, records, and normalized goldens MUST be equivalent

#### Scenario: Provider DTO reaches a widget test
- **WHEN** a widget or golden test depends directly on a provider event or model name
- **THEN** the test MUST fail architecture validation because widgets consume only canonical view state

#### Scenario: Required UI evidence is missing
- **WHEN** any required viewport, accessibility mode, control-loss state, confirmation state, or handoff state lacks evidence
- **THEN** the corresponding implementation slice MUST remain incomplete

#### Scenario: Derivation deviates from the landed table
- **WHEN** a client's presentation-state derivation resolves any axis combination differently from the landed avatar-state derivation table
- **THEN** the deviation MUST fail the client's authority-derivation acceptance rather than being carried as an implementation variance

#### Scenario: Closed media state lacks a kernel-evidenced fixture
- **WHEN** any of the ten closed `media.states` has no deterministic fixture evidencing it through kernel fields
- **THEN** state-reachability acceptance MUST report the gap as open rather than satisfied by presentation-field or derived-in-app evidence
