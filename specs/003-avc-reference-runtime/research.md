# Phase 0 Research: AVC Reference Runtime

**Feature**: 003-avc-reference-runtime | **Date**: 2026-07-11

All open questions for this feature were resolved during the clarify phase
(spec `## Clarifications`, Session 2026-07-11, Q1–Q8) and by the ratified OpenSpec
`design.md`. **No `NEEDS CLARIFICATION` markers remain.** This file consolidates the
resulting decisions in Decision / Rationale / Alternatives form so downstream `/speckit-tasks`
and `/speckit-implement` inherit a settled technical baseline.

## R1 — Test framework & determinism proof (Q1, SC-003)

- **Decision**: Use `pytest` with `pytest-randomly`. Parametrize the ARR/ACR matrix; run the
  suite under multiple recorded seeds; a failing seed must be reproducible from reported output.
- **Rationale**: `pytest` parametrization/fixtures fit a 34-scenario (+ applicable ACR) matrix;
  `pytest-randomly` prints and pins the seed, giving order-independence evidence and a
  reproducible failing case directly, satisfying SC-003 without hand-built shuffling.
- **Alternatives considered**: stdlib `unittest` (no third-party dep, but heavy boilerplate for
  the matrix and no built-in seeded randomization); a bespoke `scripts/validate-*.py` harness
  (matches repo gate style but reinvents discovery/assertion/reporting). Rejected as costlier
  and weaker on the determinism proof.

## R2 — Language floor (Q2)

- **Decision**: Target Python 3.11+; no 3.12-only syntax in the reference package.
- **Rationale**: Matches the de facto floor already in `xfactory/` (`datetime.UTC`, `from
  __future__ import annotations`, dataclasses); unlocks `Self`, exception groups, and stable
  dataclass/`typing.Protocol` ergonomics needed for the ports and state values.
- **Alternatives considered**: 3.12+ (newer typing, but narrows environments beyond current
  repo usage); 3.10+ (adds `match`, but below the existing `datetime.UTC` usage, forcing a
  helper refactor). Rejected.

## R3 — Dependency policy: stdlib-only core (Q3, FR-001, SC-005)

- **Decision**: `xfactory/avatar_runtime/` imports only the Python standard library. Tests and
  the validator gate may use pinned repo-approved deps (`pytest`, `pytest-randomly`, `PyYAML`,
  `jsonschema`). The boundary validator enforces that the runtime package imports no test,
  provider, or network dependency.
- **Rationale**: A stdlib-only core is trivially non-deployable and trivially boundary-provable;
  it cannot pull a network/provider SDK by construction. Tests still validate canonical YAML /
  JSON-Schema fixtures with the same libraries the repo already uses in `scripts/validate-*.py`.
- **Alternatives considered**: both core and tests stdlib-only (would force hand-rolled YAML /
  schema validation); both may use third-party libs (weakens the no-SDK guarantee). Rejected.

## R4 — Boundary & provisional-import enforcement (Q4, FR-004, FR-004a, SC-010)

- **Decision**: Enforce the non-deployable boundary and the provisional-import prohibition with
  **execution-free static AST/import/export/file-surface analysis**. Ship it two ways from one
  pure scanner (`tests/avatar_runtime/boundary/scanner.py`): an in-suite boundary test and a
  standalone `scripts/validate-avatar-runtime.py` repo gate. The scan detects provisional-test
  imports, network/provider SDKs, listeners, application factories, persistence, credential
  loading, deployment files, and forbidden entrypoints — without importing/executing runtime code.
- **Rationale**: Static analysis is deterministic and cannot be defeated by an un-imported
  module; a shared scanner guarantees the gate and the test enforce identical rules; the
  standalone script matches the repo's `validate-*.py` gate + README-index convention and
  surfaces SC-010 output on its own.
- **Alternatives considered**: in-suite boundary test only (not a standalone gate); runtime
  import-guard raising at load (only catches executed imports, not a static guarantee). Rejected.

## R5 — Applicable ACR-* source of truth (Q5 Custom, FR-034a, Assumptions)

- **Decision**: Derive the applicable `ACR-*` set from an acceptance map, never a second
  hand-maintained enumeration. During parallel work the conformance checker reads the versioned
  shared baseline map
  `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`
  (`avatar-client-parallel-v1`), verifying its source commit and digest. At realization it
  switches to the digest-pinned released `contracts/avatar-client/acceptance-map.yaml`.
  Non-applicability dispositions live in the scenario→test map (R6).
- **Rationale**: One digest-verified source removes drift risk and keeps the provisional→canonical
  seam a single pinned file swap; it makes SC-002 provable before the kernel lands.
- **Alternatives considered**: a checked-in ACR enumeration mirrored under the runtime tests, or
  a standalone provisional ACR fixture (both create a second list to keep in sync); defer ACR
  mapping to realization (leaves SC-002 unprovable during parallel work). Rejected per the user's
  custom answer.
- **Read-only note**: both acceptance-map paths are **sibling-owned** and consumed read-only;
  this feature never edits them (FR-036).

## R6 — Scenario→test mapping enforcement (Q6, FR-034)

- **Decision**: A checked-in `tests/avatar_runtime/conformance/scenario-test-map.yaml` binds each
  required ARR/ACR scenario ID to one or more collected `pytest` node IDs, or to an allowed
  non-applicability disposition with rationale. `check_conformance.py` compares it against the
  acceptance map(s) and the collected test set and **fails on missing, duplicate, dangling,
  skipped-required, or unknown mappings**.
- **Rationale**: An explicit, diffable artifact fails closed and aligns with the acceptance map's
  `evidence_id_template: TEST-{scenario_id}`; a machine check prevents silent coverage gaps.
- **Alternatives considered**: naming/marker convention embedding IDs in test names (discipline-
  dependent, no separate source of truth); a manual Markdown traceability table (not fail-closed,
  drifts). Rejected.

## R7 — Realization pin & conformance evidence location (Q7, FR-005, SC-006)

- **Decision**: Record the five release coordinates (tag, exact commit, per-file digests,
  interface-lock digest, acceptance-map digest) and final conformance results in
  `tests/avatar_runtime/conformance/realization-pin.yaml`, carrying explicit `schema_version`
  and `kind`, validated as part of final conformance.
- **Rationale**: Keeps evidence inside the feature's path ownership (satisfies SC-008/FR-036),
  co-located with the tests it pins, and follows repo YAML discipline (Principle IV).
- **Alternatives considered**: under `specs/003-avc-reference-runtime/` (separates the pin from
  the code); a new top-level `conformance/`/`evidence/` dir (new tracked root + README-index
  obligation). Rejected.

## R8 — Validation-gate integration & documentation index (Q8, FR-036, SC-008, Principle IV/V)

- **Decision**: Add `scripts/validate-avatar-runtime.py` to the README validator index and run it
  plus the deterministic `pytest` suite for every feature commit and before push. This validator
  script + its single README line is the declared narrow governance exception to the runtime/test
  paths and edits no sibling-owned contract, F0, UI, domain, deployment, or release-metadata path.
- **Rationale**: Matches the repo's existing `validate-*.py` gate + README-index convention
  (Principle IV/V), guards intermediate commits during parallel work, and gives reviewers/CI a
  single command.
- **Alternatives considered**: run only the pytest suite (diverges from the gate pattern, no
  standalone boundary validator); keep the suite out of the shared gate until realization (risks
  unguarded intermediate commits). Rejected.

## R9 — Design invariants inherited from the OpenSpec `design.md` (no new decision)

Adopted verbatim as design constraints (not re-litigated here): non-deployable package boundary
(D1); inject every nondeterministic/authoritative dependency via seven ports (D2); test-only
provisional seam (D3); separate logical-session vs media-attempt state with one instance / one
leg and fresh-resume replacement (D4); AVC-02 as one total `grant|denial|terminal` function with
a process-memory-only TTL grant cache and credential-free terminal replay (D5); two-channel media
authorization barrier over sideband + identity-checked `lease_ack` (D6); one event log + atomic
snapshot barrier `B` with bounded post-barrier buffering and overflow restart (D7); fail-closed
policy/consent/operation authority, memory-gateway consent is **not** media authority (D8);
structured redacted telemetry (D9); parallel implementation separated from ordered realization,
accepted variance reopens only mapped IDs (D10).

## Open items deferred to sibling changes (not this feature)

- Production deployment home, network framework, provider SDK, distributed cache, operational
  telemetry → `qualify-avatar-live-voice`.
- Hermes ports replacing fixtures → `avatar-pilot-hardening`.

These are explicitly **out of scope** here (spec §Out of Scope) and require no decision now.
