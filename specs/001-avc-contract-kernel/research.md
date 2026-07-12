# Phase 0 Research: AVC Contract Kernel

**Feature**: 001-avc-contract-kernel | **Date**: 2026-07-11

The OpenSpec source is ratified-grade and the spec carries 0
`[NEEDS CLARIFICATION]` markers, so this phase records the engineering decisions
that turn the ratified requirements + seven clarify answers into a buildable
design, with rationale and rejected alternatives. Each decision cites the FR /
clarification / constitution principle it serves.

---

## D1 — Validator language, libraries, and structure

**Decision**: Implement `scripts/validate-avatar-client.py` in Python 3 using
`jsonschema.Draft202012Validator` + `PyYAML` (`yaml.safe_load`) and standard
library only (`hashlib`, `re`, `pathlib`, `argparse`, `dataclasses`, `sys`).
Mirror the repo house style: `#!/usr/bin/env python3`, `from __future__ import
annotations`, guarded imports with a clear `ERROR ...; sys.exit(2)` on missing
deps, `ROOT = Path(__file__).resolve().parents[1]`, an accumulate-then-report
error model, `--strict` flag, exit code 0 (ok) / 1 (findings) / 2 (harness
error).

**Rationale**: `Draft202012Validator` and PyYAML are already repo dependencies
(`validate-credential-contracts.py`, `validate-workflow-contracts.py`,
`validate-avatar-first-ui.py`). No new dependency; consistent operator
experience with the existing `scripts/validate-*.py` gate (Principle V; FR-020).

**Alternatives rejected**:
- *Vendored/stdlib-only JSON Schema check* — reinvents a conformant 2020-12
  validator; error-prone and non-canonical.
- *Node/Ajv* — introduces a foreign toolchain to a Python validator repo.

---

## D2 — Language-neutral, self-describing fixtures (Q5, FR-019/FR-023/SC-009)

**Decision**: Each fixture is a **fixture-case** file carrying metadata plus a
pure-JSON-compatible instance:

```yaml
schema_version: 1
kind: avatar-client-fixture-case
case_id: ACR-002-S09.denial-carries-answer
target: avc-02-session-result           # schema id OR registry id
target_kind: schema                      # schema | registry
expect: invalid                          # valid | invalid
scenario_ids: [ACR-002-S09]              # stable acceptance IDs (may be [])
evidence_id: TEST-ACR-002-S09
notes: "denial result must not carry an SDP answer"
instance: { ... }                        # the JSON-compatible document under test
```

A machine-readable `fixtures/index.yaml` enumerates every case (id, target,
expect, scenario_ids, path). Because the `instance` is pure JSON-compatible
YAML, **any** conformant draft-2020-12 implementation (including the Dart
client) can: read the index, load each `instance`, validate it against the named
schema, and assert the `expect` outcome — with no dependency on the Python
validator. The Python validator is the reference runner over the same index.

**Rationale**: Satisfies "0 additional coordination" portable conformance
(SC-009); the client is Dart, so conformance cannot require the Python tool.

**Alternatives rejected**:
- *Bare instance files with valid/invalid inferred from directory name* — not
  self-describing; couples the expected outcome to a folder convention a
  cross-language consumer must reverse-engineer.
- *JSON-only fixtures* — YAML matches repo convention and round-trips to JSON;
  the index makes language-neutrality explicit without a second serialization.

---

## D3 — Registries as first-class data files + schema/registry parity (Principle VII, FR-004/FR-005)

**Decision**: Author each closed vocabulary as a versioned registry data file
under `registries/` (`schema_version`, `kind`, ordered `members` with per-member
id + description + any producer/authority metadata). Schemas that constrain a
vocabulary embed the enum, and the validator enforces **exact set-equality**
between each schema enum and its registry file (fail on drift, extra, or missing
member). The session-result-reasons registry must contain exactly the 15 ratified
reasons; the consent-purpose registry exactly the 3 neutral purposes.

**Rationale**: JSON Schema draft 2020-12 cannot dynamically load an enum from an
external file, yet Principle VII requires closed registries as first-class,
auditable artifacts and the change requires them published. Parity-checking keeps
one canonical source (the registry file) while still enforcing closure in-schema.

**Alternatives rejected**:
- *Inline enums only* — registries would not exist as standalone governable
  artifacts (violates the change's "publish registries" requirement).
- *Registry files only, enums generated at runtime* — schemas would not be
  self-contained/statically checkable by external consumers.

---

## D4 — Dual redaction enforcement with bounded sentinels (Q3, FR-018/SC-008)

**Decision**: Two layers.
1. **Structural** — schemas forbid secret-bearing shapes where prohibited:
   `additionalProperties: false` on closed objects, prohibited fields simply
   absent from the schema, and, for AVC-02 denial/terminal variants, the
   discriminated sub-schema makes `sdp`, `sdp_answer`, and any credential field
   structurally invalid (so a secret-carrying non-grant cannot validate).
2. **Content scan** — the validator scans every committed file under
   `contracts/avatar-client/` against `redaction/denylist-patterns.yaml`
   (credential/token, SDP marker such as `v=0`/`a=`, raw-payload, transcript/
   media, and prohibited high-cardinality-identifier patterns).
   **Bounded sentinels**: synthetic secrets used inside fixtures must be declared
   in `redaction/sentinels.yaml` with a reserved, fixed, obviously-fake form
   (e.g. prefix `SENTINEL_` + fixed length); the scan allows only those exact
   bounded forms and flags any string that matches a real secret pattern but is
   not a declared bounded sentinel — so a sentinel cannot widen into a bypass.

**Rationale**: Structural proves the contract *cannot* carry secrets; the scan
catches accidental leakage in example bytes; bounded sentinels let adversarial
fixtures exercise "secret present → rejected" without smuggling a real secret or
disabling the scan (SC-008 edge case).

**Alternatives rejected**:
- *Structural only* — a real secret pasted into an otherwise-valid example passes.
- *Scan only* — does not prove structural exclusion (weaker than FR-007/FR-018).
- *Global scan ignore-list* — an unbounded allowlist is itself a bypass.

---

## D5 — Consolidated evidence/disposition register + status model (Q4, FR-032/SC-003)

**Decision**: One `evidence-register.yaml` resolves **every** acceptance-map
scenario to evidence:
- `automated` → `fixture` evidence with `evidence_id` (e.g. `TEST-<scenario>`)
  that must exist in `fixtures/index.yaml`;
- `manual` → a recorded `result` plus `reviewer` and `disposition` fields;
- `live_f0` / `successor` → `owner_change` + `fail_closed_default` describing the
  closed default that holds until that owner lands.

Each entry has a `status` from a closed set with an allowed transition graph the
validator enforces:

```text
planned → evidenced → accepted          (automated/manual)
planned → deferred(owner named)          (live_f0/successor)
```

The validator fails when: a scenario is missing from the register; an entry is
`evidence-free` (automated without an existing fixture, manual without a recorded
result, deferred without an owner + fail-closed default); a status transition is
not in the allowed graph; or a referenced fixture/artifact does not exist.

**Rationale**: One auditable file makes "no scenario is evidence-free" checkable
across all 72 scenarios regardless of evidence type, matching the traceability
doc ("named owner and fail-closed default").

**Alternatives rejected**:
- *One file per scenario* — many small files, heavier to digest/maintain.
- *Acceptance-map `status` field alone* — status is not recorded evidence.

---

## D6 — F0 publication gate: pin + validate, fail closed (Q6, FR-029/FR-033/SC-007/SC-010)

**Decision**: The F0 sibling owns and versions `f0-results.schema.yaml` and
`f0-interface-impact.schema.yaml`. `interface-lock.yaml` records an
`f0_evidence_pin` block: `{ f0_source_commit, f0_results_schema_sha256,
f0_interface_impact_schema_sha256 }`. At the gate the validator:
1. resolves the pinned F0 schemas from the F0 change path;
2. verifies each schema's SHA-256 equals the pinned digest and the F0 source
   commit matches;
3. validates the consumed `f0-results` / `f0-interface-impact` instances against
   those pinned schemas;
4. only then reads `PASS` / variance dispositions.
It **fails closed** on: missing pinned schema, digest mismatch, source-commit
mismatch, instance validation failure, unknown status value, or an unknown
variance field. Schema/fixture implementation may proceed while the gate is
pending; only the bundle **tag** is blocked (FR-029).

**Rationale**: The consumer of an external evidence contract owns the interface
it depends on *by pinning + validating*, without duplicating or co-owning the
sibling's schema (respects sibling ownership boundaries; robust fail-closed
gate).

**Alternatives rejected**:
- *Kernel defines its own consumed schema* (the clarify "Recommended" A) —
  overridden by the accepted Custom answer to avoid split/duplicated ownership.
- *Read named fields opaquely* — a malformed evidence file could be misread; not
  fail-closed.

---

## D7 — Content-addressed release, digest scope, and two completion states (Q1/Q7, FR-022/FR-024/FR-034)

**Decision**: The per-file-digested, manifest-registered **semantic consumed
set** is exactly: the 8 schemas, `shared-definitions`, the 9 registry files, the
canonical fixtures (+`index.yaml`), `acceptance-map.yaml`, `interface-lock.yaml`,
and `evidence-register.yaml`. `scripts/validate-avatar-client.py` and the
`redaction/` config ship in the release commit as reproducible tooling/config
but are **not** pinned semantic artifacts (Design Note 3). Version is allocated
at realization as the next available minor after `contract-v1.6` →
`contract-v1.7` (additive), with `manifest.yaml`, `CHANGELOG.md`, `README.md`
updated atomically and an annotated `contract-v1.7` tag on the realized commit
(Principle VI; `docs/contract-versioning-policy.md`). Two completion states:
*implementation complete, publication pending F0* (all artifacts + validator
green, gate enforced) vs *realized* (F0 `PASS`, variances dispositioned, tag +
digests recorded); the OpenSpec change stays active until realized (FR-034).

**Rationale**: Matches the enumerated Q1 digested set and the versioning policy's
recovered-baseline rule; keeps the pinned surface semantic while still shipping
the tooling reproducibly.

**Alternatives rejected**:
- *Digest everything incl. the validator* — couples consumers to a Python tool
  version and forces re-release on any validator edit (Q1 option C).
- *Reserve a version in the proposal* — forbidden by Principle VI.

---

## D8 — Shared-definitions `$ref` strategy and AVC-03/AVC-05 absorption (FR-002/FR-003)

**Decision**: One `shared-definitions.schema.yaml` holds the common `$defs`
(actor/client/subject, workflow purpose, consent ref/version/purpose IDs, trace,
session epoch, media leg/attempt, server-derived offer fingerprint, state
revision, last-event sequence, media authorization, session outcomes, retention
class, redaction, retry-equivalence). Every contract references it by **relative
`$ref`** (`shared-definitions.schema.yaml#/$defs/...`); the validator resolves
via a local reference store built from the on-disk files (no network). AVC-03 is
an inline `capabilities` object on the AVC-02 `grant` variant; AVC-05 is a
registered AVC-04 event **payload** schema (a `$defs` entry / event-registry
payload reference), not a standalone contract. AVC-09/AVC-10 identifiers are
reserved — the validator forbids their reuse.

**Rationale**: Single source for shared shapes (FR-003); faithful to design.md
Decision 1 absorption model; offline-resolvable refs keep the validator
deterministic and consumer-portable.

**Alternatives rejected**:
- *Per-contract duplicated definitions* — drift risk; violates single shared
  module requirement.
- *Absolute `$id` URLs* — introduces host/network coupling; conflicts with
  Principle IV (no host-absolute paths) and portable offline conformance.

---

## D9 — AVC-07 / AVC-08 artifact scope (Q2, FR-001)

**Decision**: Ship the AVC-07 (retention profile) and AVC-08 (persona profile)
**schemas + conformance fixtures only**. No live instances, no illustrative
`.example.yaml`, no `.template.yaml` stubs. Fixtures double as the canonical
examples. Concrete persona catalogs and retention overlays remain domain-owned.

**Rationale**: Keeps domain content out of the neutral kernel (Principle I) and
avoids implying an instantiation shape the domain layer owns.

**Alternatives rejected**: shipping examples or templates (Q2 options B/C) —
adds domain-flavored files to maintain and risks over-specifying the overlay.

---

## D10 — Compatibility policy inheritance (FR-008)

**Decision**: The "declared compatibility policy" is
`docs/contract-versioning-policy.md` (additive = minor; unknown consequential
vocabulary fails closed; consumers pin commit + digests). The ACR-001-S01
fixture proves an additive optional field on the same major is preserved/ignored;
ACR-001-S02 proves an incompatible major fails preflight; ACR-001-S03 proves an
unknown command/event/state/decision is rejected (not inferred permissive).

**Rationale**: Reuses ratified repo governance rather than inventing a per-family
policy.

**Alternatives rejected**: a kernel-local compatibility statement — redundant
with, and could drift from, the repo policy.

---

## Open questions carried forward

None. All Technical Context unknowns are resolved. Items explicitly deferred by
the ratified change (live provider qualification, deployment topology, latency
budgets, reference runtime, Flutter client, UI assets) remain out of scope and
owned by named sibling/successor changes (spec.md → Out of Scope).
