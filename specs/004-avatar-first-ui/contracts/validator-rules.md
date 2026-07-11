# Contract: Offline Validator Rules & Stable Error/Evidence IDs

**Target file**: `scripts/validate-avatar-first-ui.py` (extend the existing
PyYAML validator)
**Principle**: offline only — no provider or runtime service (FR-020). Every
rejected rule prints `ERROR <error-id> <message>` so error IDs are stable
evidence anchors (D10, FR-020, SC-002).

## Modes (D13)

- `--mode baseline` (default): resolve kernel IDs and timing ceilings against the
  frozen `avatar-client-parallel-v1` baseline fixture data. Used during parallel
  work; keeps offline runs green without the kernel release.
- `--mode realization`: load the exact released kernel registries read-only and
  fail closed on any drift (content-addressed tag + commit + digests). Used in
  Phase 3.

## Structure / parity rules

| Rule | Error ID | Evidence |
|------|----------|----------|
| Schema `name`/`schema_version`/`kind` correct; required top-level keys present | `AFUV-SCHEMA-SHAPE` | schema check |
| Template `kind`, `avatar_is_presentation_only: true`, 4 channels, required controls | `AFUV-TEMPLATE-SHAPE` | template check |
| Example/profile parity with schema (all four archetypes validate) | `AFUV-PARITY-EXAMPLE` | examples check |
| Acceptance-map parity: 8 requirements / 25 scenarios present and mapped | `AFUV-PARITY-ACCEPTANCE` | acceptance-map parity |
| Fixture references a real `AFU-*` evidence ID | `AFUV-EVIDENCE-UNKNOWN` | fixtures check |

## Enforced rule classes (each has ≥1 negative fixture — Q6=A)

| # | Rule class | Error ID | Negative fixture (under `fixtures/negative/`) | Source |
|---|-----------|----------|-----------------------------------------------|--------|
| 1 | Presentation authors an authoritative axis transition | `AFUV-AUTHORITY-TRANSITION` | `authority-transition.yaml` | FR-001, FR-016 |
| 2 | Selected readiness/heartbeat/lease exceeds kernel-owned ceiling (or ceiling unresolvable) | `AFUV-TIMING-OUT-OF-RANGE` | `timing-out-of-range.yaml` | FR-013, FR-026 |
| 3 | Required control missing its declared fallback | `AFUV-CONTROL-FALLBACK-MISSING` | `control-fallback-missing.yaml` | FR-007 |
| 4 | Unknown/invalid persona reference (unresolvable) | `AFUV-PERSONA-UNRESOLVED` | `persona-unresolved.yaml` | FR-011 |
| 5 | Reserved/forbidden interaction mode selected (server_vad / push_to_talk) without fallback | `AFUV-MODE-RESERVED` | `mode-reserved.yaml` | FR-015 |
| 6 | Unsafe rendering: HTML/executable/provider widget/unsafe URI or non-allowlisted destination | `AFUV-UNSAFE-RENDER` | `unsafe-render.yaml` | FR-012 |
| 7 | Missing/invalid consent-purpose mapping (non-neutral or unmapped) | `AFUV-PURPOSE-INVALID` | `purpose-invalid.yaml` | FR-014 |
| 8 | Held answer rendered as active capture/playback (no matching `media_authorized`) | `AFUV-HELD-ANSWER-ACTIVE` | `held-answer-active.yaml` | FR-008, FR-009 |

Additional fail-closed checks reuse the class above them:
- Unresolvable retention-policy reference ⇒ `AFUV-PURPOSE-INVALID` family? No —
  use a dedicated `AFUV-RETENTION-UNRESOLVED` for clarity; add a negative fixture
  `retention-unresolved.yaml` (FR-027) if a distinct rule class is warranted at
  implement time.

## Positive & compatibility checks

- All four representative archetypes validate clean in `baseline` mode
  (`AFUV-PARITY-EXAMPLE` must not fire).
- ≥1 compatibility fixture under `fixtures/compatibility/` (pre-alignment profile,
  incl. legacy embedded `persona_catalog`) validates clean (D7, D12, SC-003).
- Every new optional field, when omitted, resolves to its closed default and the
  validator reports zero fields defaulting open (SC-004).

## Determinism (SC-006)

Given identical inputs, the validator's verdict, emitted error IDs, and any
fixture-derived expected shapes are byte-stable across runs. No clock, RNG, or
network is consulted; fixtures pin their own clock/IDs.

## Notes for implement phase

- Keep the existing `REQUIRED_CONTROL_IDS` / `REQUIRED_CHANNELS` checks; extend
  rather than replace.
- Error IDs above are the proposed stable set; if implement renames any, update
  `data-model.md`, the fixtures' `expect_error`, and the acceptance map together.
- Exit non-zero on any `ERROR`; print `OK ...` only when clean (preserve current
  contract).
