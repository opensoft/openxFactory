# Interface Surface Inventory (plan-level): AVC Contract Kernel

**Feature**: 001-avc-contract-kernel | **Date**: 2026-07-11

Plan-level inventory of the interfaces this feature exposes. The actual schema
bodies are authored in the implementation phase under
`contracts/avatar-client/`; this file records *what* interfaces exist and their
contracts, so tasks and reviewers share one map. Field-level semantics:
[data-model.md](../data-model.md) and OpenSpec `design.md`.

## 1. Canonical data contracts (consumed by clients, brokers, workflow services, domains)

- **8 AVC schemas** + `shared-definitions.schema.yaml` — YAML-serialized JSON
  Schema draft 2020-12; each declares contract id + `contract_schema_version`;
  shared shapes via relative `$ref`. (AVC-01, -02, -04, -06, -07, -08, -11, -12;
  AVC-03 inline on AVC-02, AVC-05 as AVC-04 payload, AVC-09/-10 reserved.)
- **9 closed registries** (`registries/*.registry.yaml`) — session-result
  reasons (15), events, commands, retention classes, capabilities, interaction
  modes, session outcomes, fallback modes, consent purposes (3). Unknown values
  rejected; schema enums must set-equal registry members.

**Compatibility contract**: `docs/contract-versioning-policy.md` (additive =
minor; consumers pin exact commit + per-file digests; tag alone is not a pin).

## 2. Validator CLI contract (`scripts/validate-avatar-client.py`)

- **Invocation**: `python3 scripts/validate-avatar-client.py [--strict]`.
- **Checks**: schema validity + `$ref` resolution; schema/registry parity + exact
  counts; fixture index completeness + per-case `expect`; acceptance-map parity
  (17/72); evidence-register completeness + legal status transitions +
  referenced-artifact existence; dual redaction (structural + content scan with
  bounded sentinels); digest/manifest/changelog/tag identity; F0 gate
  (pin + validate + fail-closed).
- **Exit codes**: `0` ok · `1` findings · `2` harness error. Accumulate-then-report.
- **Status**: reproducible reference tooling; **not** a pinned semantic artifact
  and **not** a required consumer dependency (FR-020, FR-023, Q5).

## 3. Self-describing fixture contract (`fixtures/`)

- **`fixtures/index.yaml`** enumerates cases; each `fixtures/<schema>/<case>.yaml`
  is a `avatar-client-fixture-case` (`target`, `target_kind`, `expect`,
  `scenario_ids`, `evidence_id`, `instance`). Any conformant draft-2020-12
  implementation can execute the suite — the portable conformance contract (SC-009).

## 4. Traceability + evidence contracts

- **`acceptance-map.yaml`** — realized map (ACR-*/SCO-*/RBG-*), 17 req / 72 scen.
- **`evidence-register.yaml`** — consolidated evidence/disposition register
  (automated→fixture, manual→recorded result, live_f0/successor→owner +
  fail-closed default); closed status state machine.

## 5. Consumed external interface — F0 evidence (owned by the F0 sibling)

- `qualify-avatar-brokered-call-feasibility` owns/versions
  `f0-results.schema.yaml` and `f0-interface-impact.schema.yaml`.
- **This kernel does not co-own them.** It pins `{f0_source_commit,
  f0_results_schema_sha256, f0_interface_impact_schema_sha256}` in
  `interface-lock.yaml`, validates the consumed instances against the pinned
  schemas, and fails closed on any mismatch (FR-033, Q6).

## 6. Release + governance contracts (serialized final step)

- **`contracts/manifest.yaml`** entries (per-file `sha256` over the semantic
  consumed set) · **`contracts/CHANGELOG.md`** `contract-v1.7` entry ·
  annotated `contract-v1.7` tag on the realized commit · handoff artifact
  (tag, commit, digests, interface-lock digest, acceptance-map digest).
- **Boundary ratifications** (governance, not code): future private
  `xfactory-avatar-client` repo; internal-live release-evidence gate; deferred
  aggregation + web-console integration (FR-025–FR-028; SCO-002, RBG-001–003).
