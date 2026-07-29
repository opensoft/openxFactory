# openxFactory Contract Changelog

Status: draft

Governed by [Contract Versioning Policy](../docs/contract-versioning-policy.md).

Legacy baseline note: versions `contract-v1.1` through `contract-v1.6`
predate mandatory annotated tags and carry none. Tag enforcement begins at
`contract-v1.7` — the first realized release published with an annotated tag —
without fabricating historical tags.

## Unreleased — pending bundle registration (fold into the next cut)

- (nothing pending — the contract-v1.19 cut discharged the
  `xfactory-derived-model-conformance` registration.)

## contract-v1.19 — 2026-07-29 (additive; pattern-ledger sensing contracts + derived-model registration catch-up)

Realizes **add-pattern-ledger** (exit 1 of the `recurrence-crystallization`
staged topic; ratified and archived 2026-07-29): the five **pattern-ledger**
record schemas —
`contracts/schemas/pattern-ledger-{episode,outcome-label,recurrence-family,recurrence-forecast,crystallization-candidate}.schema.yaml`
— episodes as derived projections over existing audit/run/metering/label
streams with explicit default-deny consent tiers; append-only outcome
labels (quality is a fold, never a stored verdict); tenant-scoped
recurrence families with recorded merge/split transitions; maturity-dated,
scored forecasts with declared cost-regime assumptions; and the
nominate-never-spend crystallization candidate. The canonical validator
`scripts/validate-pattern-ledger.py` (nine named policy rules; self-testing
7 positives / 7 indexed negatives) and `examples/pattern-ledger/` (incl.
the MVP packet-capture fixture corpus hand-derived from the real
2026-07-28/29 runs) are commit-content-addressed tools and fixtures, no
per-file digest. Purely additive.

Also registers **`xfactory-derived-model-conformance`**
(`contracts/schemas/xfactory-derived-model-conformance.schema.yaml`),
realized 2026-07-23 by archived `add-governed-derived-model` but missed by
the v1.16–v1.18 cuts — the standing Unreleased note is discharged by this
cut. DTN-014 flips `implemented` → `adopted` in the candidate register as
domain pins advance past this registering ref.

## contract-v1.18 — 2026-07-24 (additive; domain content manifest + memory binding)

Realizes **add-hermes-domain-content-manifest** (seeding increment 4b's
contract half; convention-then-contract): the optional
**`hermes_domain_content_manifest`**
(`contracts/hermes-domain-overlay/content-manifest.schema.yaml`) — a domain
repo declares its seedable content set per ratified `content_kind` (exactly
one of `path`/`directory`; absent manifest, consumers keep the documented
increment-4a convention; an undeclared kind never loads silently) — and the
**`hermes_memory_binding`** record shape
(`contracts/memory-gateway/memory-binding.schema.yaml`), formalizing the
derived binding hermes-install increment 3 materializes: rails input in the
ratified gateway vocabulary (promotion gateway constitutionally
`customer_memory_gateway`, `accepted_authority_level` drawn from
`authority_levels`), never a provider binding — any provider/credential
surface fails the canonical validator. Realization anchors: the codexFactory
conventional set declared verbatim; the two LIVE-derived opensoft bindings
as the packaged example. Purely additive.

## contract-v1.17 — 2026-07-23 (additive; client-content tuning surface)

Realizes **add-client-layer-tuning-contracts** (phase 2a of the layer
activation path): the neutral tenant-layer contract set — three client
content kinds (`client_policy_overrides` with stricter_only + budget
envelopes + tracking granularity + the human-ratified auto-clear envelope,
`client_memory_boundaries` with the tenant_isolated invariant,
`client_integration_boundaries` reference-only) and the seedable
**`hermes_client_overlay`** (canonical path
`config/clients/<client_ref>/overlay.yaml`, descriptor-declared,
`client_overlays[]`-pinned). Canonical validator
`scripts/validate-client-content.py` implements the stricter-only
comparability spec with a `review_required` fallback and self-testing
fixtures. Also in this bundle: the neutral house-team roster
(`templates/client-layer/roles/` — 10 deciders incl. the Finance &
Accounting Officer + the liaison capability, voice floor locked) and the
scaffold's `cost_reporting_steward`. Purely additive.

## contract-v1.16 — 2026-07-23 (additive; omnigent contract family + layer vocabulary)

Tenth annotated-tag release. Realizes **add-omnigent-domain-overlay** (the
Omnigent execution layer's domain-tier contracts) and registers
**adopt-subject-tenant-domain-vocabulary**'s policy artifact:

- `contracts/omnigent/omnigent-domain-overlay.schema.yaml` — per-domain
  overlay payload: worker classes mapped to the five neutral archetypes
  (frame/generate/verify/challenge/assemble_for_admission), the generalized
  six-boolean permission matrix with constitutional
  `execute_final_action`/`access_secrets` `const: false`, four credential
  tiers including `never_assignable`, domain-level permission aliases,
  whole-document `worker_profiles` payload, `stricter_rule_wins`
  composition under the `domain_installation_overlay` operations.
- `contracts/omnigent/omnigent-install-manifest.schema.yaml` — the install
  manifest: hermes-install rendered runtime manifest digest-pinned as the
  single stack identity (no parallel identity by construction), exactly one
  domain overlay, the authoritative subject-workload registry, pre-rendered
  effective-profile provenance. First family with canonical
  Subject/Tenant/Domain machine spellings from birth.
- `contracts/policies/layer-vocabulary.yaml` — the ratified canonical layer
  vocabulary: names + roles, the customer→subject / client→tenant legacy
  mapping, reserved layer terms, the frozen-identifier inventory (migration
  staged dormant at `ideation/staging/layer-vocabulary-machine-migration/`),
  and the per-domain alias table.

Canonical validator `scripts/validate-omnigent-contracts.py` with packaged
examples and marked negative fixtures (commit-content-addressed tools, no
per-file digest). Realization evidence: canonical domain overlays in
codexFactory (`engineering-omnigent-overlay`) and MedxFactory
(`medical-omnigent-overlay`); Omnigent-Install's live manifest with
fail-closed compose/verify, byte-equivalent rendered coding-patch-worker
binding, and the MedxFactory second-domain params fixture. All additive:
every released path from `contract-v1.7` through `contract-v1.15` is
byte-identical.

## contract-v1.15 — 2026-07-23 (additive; hermes-domain-overlay contract surface)

Ninth annotated-tag release. Realizes **add-hermes-domain-overlay-contract**:
the neutral `hermes_domain_overlay` schema (domain identity, non-empty
approval scopes and required fields, authority boundaries with the
canonical-validator-enforced `<domain.id>_owns` naming and no-overlap rules)
and the `hermes_overlay_descriptor` role→path declaration (runtime layer
roles domain/client/customer as keys — deliberately not directory names —
with a documented-convention fallback when absent and fail-closed dangling
paths). New canonical validator `scripts/validate-hermes-domain-overlay.py`
with self-testing packaged examples/negatives under
`contracts/hermes-domain-overlay/examples/`. Realization proof: codexFactory's
live 37-authority `hermes/domain/overlay.yaml` passes unmodified via the
convention fallback. Replaces the hermes-install seeding runtime's minimal
structural check at its materialization increment (which pins this release).
Purely additive; no existing contract touched.

## contract-v1.14 — 2026-07-22 (additive; possibles-register AI-derivation intake)

Eighth annotated-tag release. Realizes the **possibles-derivation lane's
contract surface** (`add-possibles-derivation-lane`, task 2.6 registration at
the realization commit): the ADDITIVE AI-derivation intake delta on the
`ideation-possibles-register` kernel — optional `register_entry.origin`
(enum `[human-authored, ai-derived]`; absent defaults to human-authored),
optional `register_entry.derivation` (worker-run identity: correlation id /
worker profile / prompt-contract version, plus machine
`disposition: pending_review` and the `derivation_human_disposition` local
mirror of the index's `human_disposition`), and the `allOf` conditional that
requires `derivation` when `origin: ai-derived`. Modelled one-for-one on the
index topic entry's `origin` + `human_seen` intake pair; the conditional
never fires on an origin-absent entry, so `contract_schema_version` stays 1
per the kernel's additive-growth rule and every released path from prior
bundles is byte-identical.

Registered — `contracts/schemas/ideation-possibles-register.schema.yaml`
(per-file SHA-256 recorded in `contracts/manifest.yaml`; the kernel's first
manifest registration — the ideation-dashboard family was previously
registered in `contracts/README.md`'s doc index only). Packaged examples:
`examples/ideation-dashboard/derived-possible-register.example.yaml` plus
the derived negatives and one-way-disposition transition pairs, all enforced
by the delegated strict register validator
(`scripts/validate-ideation-dashboard-contracts.py`, extended at task 2.4).

Realization evidence: codexFactory `specs/004-derive-possibles` — the
derive-possibles worker (PR #25), the nightly lane + watchdog + rolling-PR
register commit-back (PR #27), and the omnigent-install `derive-possibles`
worker profile (Omnigent-Install PR #22, contract-only until host
deployment). The nightly lane reports SKIPPED until a host advertises the
profile — the readiness-scorer precedent's valid landed state.

## contract-v1.13 — 2026-07-17 (additive; client-infrastructure-request contract family)

Seventh annotated-tag release. Realizes the neutral **client-infrastructure
contract family** (`add-client-infrastructure-liaison`): the durable
`client_infrastructure_request` coordination record, the signed/traceable
`infrastructure_readiness_result` artifact, and their strict openxFactory
validator, promoted at this change's archival (task 5.1) out of the "Contracts
Pending Realization" holding area that task 2.5 added to `contracts/README.md`.
All additive: every `contract-v1.7` / `v1.8` / `v1.11` / `v1.12` released path
is byte-identical and `contract_schema_version` is unchanged.

Added — two `contracts/schemas/xfactory-*.schema.yaml` contracts
(YAML-serialized JSON Schema draft 2020-12, `contract_schema_version: 1`;
per-file SHA-256 recorded in `contracts/manifest.yaml`):

- `xfactory-client-infrastructure-request.schema.yaml` — the
  `client_infrastructure_request` durable coordination record (never a Hermes job
  envelope): six never-conflated identity-reference `$defs`, the three-mode
  `execution_binding` (`client_managed|managed_host|opsxfactory_executed`, design
  D1), the closed 13-state `status` enum, orthogonal `conditions[]`, the embedded
  `handoff` acceptance record, digest-bearing `package_refs`, cancellation
  `child_acks`, and `supersedes_request_ref`.
- `xfactory-infrastructure-readiness-result.schema.yaml` — the
  `infrastructure_readiness_result` signed/traceable readiness artifact, never a
  bare boolean: status `ready|degraded|not_ready|unknown|maintenance`,
  `valid_until` freshness, non-privileged validator + trust refs, per-check
  `mandatory`/`outcome`/evidence, and `evidence_digest`.

Also added — `scripts/validate-client-infrastructure.py`: strict validator for
both kinds — schema conformance, embedded-secret rejection (shared avatar-client
denylist), transition legality including terminal immutability and
readiness-gated completion, identity-class separation (actor ≠ authority ≠
creating liaison; a subject id never in a typed field), idempotency/supersedes
integrity, and cancellation-acknowledgment presence — self-testing the packaged
reference examples (`examples/client-infrastructure/`: 4 valid + 9
one-violation-each negatives). Registered as a tool and content-addressed by
commit; not a pinned semantic artifact, so excluded from the per-file digest set.

Governance:

- The liaison and no domain agent ever holds tenant-administration authority; an
  `infrastructure_readiness_result` is never a bare boolean and gates a
  `client_infrastructure_request` completion only when fresh (used before
  `valid_until`), overall `ready`, and every mandatory check passes. The governing
  role doc `docs/client-infrastructure-liaison.md` is ratified alongside this
  change (`Status: ratified`; `Ratified by: add-client-infrastructure-liaison`),
  with product-owner sign-off on design D1 (execution-binding tokens) and D5
  (roles-authority wording) recorded by Brett 2026-07-16 (task 4.1). It is prose
  governed by this changelog, not a per-file manifest member.
- Fail-closed validation: `scripts/validate-client-infrastructure.py` self-test
  confirms 4 valid examples and 9 negatives each failing for its intended reason;
  `OPENSPEC_TELEMETRY=0 openspec validate add-client-infrastructure-liaison
  --strict` is green. The reference validator is content-addressed by commit and
  carries no per-file digest.

Also added — `contracts/releases/contract-v1.13.digests.yaml`: the raw-Git-blob
SHA-256 release digest inventory for this bundle (built by
`scripts/validate-contract-release.py`), refreshing the closed hermes-runtime
release surface plus the `manifest.yaml` / `CHANGELOG.md` / `README.md`
auxiliaries; the client-infrastructure family is outside that closure and is
content-addressed via `manifest.yaml` per-file digests instead.

Consumers: the per-domain adoption successors (OpsxFactory binding/readiness
producer first, then the Medx/Ledger/Ad/codex aliases) pin this bundle at the
`contract-v1.13` tag and verify the per-file SHA-256 in `manifest.yaml` before
treating a copy as current; openxFactory ships no instance records (they live in
client installs, credential-contracts residency model).

## contract-v1.12 — 2026-07-15 (additive; avatar-client-lab evidence surface / P-row adoption)

Sixth annotated-tag release. Realizes the neutral **avatar-client-lab evidence
surface** (`adopt-avatar-client-lab-candidates`), the P1/P10 owning change that
adopts the panel-confirmed layer-2 evidence candidates from codexFactory
`002-avatar-client-lab` @ `3a8fbd5` (7/7 confirmed; provenance in that feature's
`upstream-drafts/STATUS.md`). All additive: every `contract-v1.7` / `v1.8` /
`v1.11` released path is byte-identical and `contract_schema_version` is unchanged.

Added — two neutral, content-addressed client-lab artifacts under
`contracts/avatar-client-lab/` (per-file SHA-256 recorded in
`contracts/manifest.yaml`):

- `avatar-state-derivation-table.yaml` — the P1 total avatar-state derivation
  table (design D3): the precedence-ordered R0..R6 derivation plus the enumerated
  healthy-control matrix mapping the four authoritative runtime axes onto the six
  FR-019 avatar presentation states, embedding the normative invariants, with
  OQ-1..OQ-6 ratified (product-owner sign-off Brett 2026-07-15). Gate
  (vi)/(ix)(a) source. Its normative `.md` companion
  (`avatar-state-derivation-table.md`) and `README.md` are prose governed by this
  changelog, not per-file manifest members.
- `capability-scenario-register.yaml` — the P10 capability-scenario register
  (9 requirements / 22 scenarios; Option B, design D2): stable `ACL-*` ids and
  verbatim `#### Scenario:` titles machine-checked fail-closed in document order
  against the `implement-avatar-client-lab` capability spec. Gate (ix)(b) source.

Added — the 20 adopted deterministic fixtures under
`examples/avatar-first-ui/fixtures/deterministic/` (per-file SHA-256 in
`manifest.yaml`), closing the state-reachability denominator via AVC-12 kernel
fields only: P7 intake breadth (5), P8 lease/epoch takeover + snapshot-barrier
recovery (4), P11 `interrupted`/`handoff` (2), and P12/P13 the eight non-control
closed `media.states` + `control_degraded` (9). The five pre-existing released
seeds already in that directory stay unregistered (not this change's members).

Added — `contracts/avatar-client/evidence-register.implement-avatar-client-lab.yaml`,
the SCO-001-S05 successor deferral-discharge register (locked decision 7 of
`implement-avatar-client-lab`, task 4.4). Registering it here — the release-time
manifest convention first used at `contract-v1.9` (bundle members join
`manifest.yaml` only when the next additive version is cut, never mid-change) —
makes the `deferred → evidenced` discharge effective WITHOUT mutating the
released, byte-identical `evidence-register.yaml` (a contract-v1.9 member).

Governance:

- Settled law L2 (the app never self-serves neutral artifacts): all candidates
  land at their upstream openxFactory source; the codexFactory
  `apps/avatar-client-lab/` app consumes them read-only as
  `vendored_evidence_inputs` at its `contract-v1.12` pin resync (this change's
  codexFactory realization surface).
- Fail-closed validation: `scripts/validate-avatar-client.py` carries
  `check_avatar_state_derivation_table` and `check_capability_scenario_register`
  (both fail-closed, with negative coverage); with the successor register now
  manifest-listed, `--require-realization` passes (0 errors).
  `scripts/validate-avatar-first-ui.py` (baseline + realization) stays green. The
  reference validators are content-addressed by commit and carry no per-file digest.

Also added — `contracts/releases/contract-v1.12.digests.yaml`: the raw-Git-blob
SHA-256 release digest inventory for this bundle (built by
`scripts/validate-contract-release.py`), refreshing the closed hermes-runtime
release surface plus the `manifest.yaml` / `CHANGELOG.md` / `README.md`
auxiliaries; the avatar-client-lab surface is outside that closure and is
content-addressed via `manifest.yaml` per-file digests instead.

Consumers: the codexFactory `apps/avatar-client-lab/` lab pins this bundle at
the `contract-v1.12` tag and verifies the per-file SHA-256 in `manifest.yaml`
before treating a vendored copy as current.

## contract-v1.11 — 2026-07-14 (additive; document-cataloging contract surface)

Fifth annotated-tag release. Realizes the neutral **document-cataloging
contract surface** (`add-document-cataloging`): six domain-neutral JSON-Schema
contracts plus their strict openxFactory validator, promoted at this change's
archival (task 8.7) out of the "Contracts Pending Realization" holding area
that task 2.4 added to `contracts/README.md`. All additive: no existing
contract path changes and `contract_schema_version` is unchanged.

Added — six `contracts/schemas/xfactory-document-*.schema.yaml` contracts
(YAML-serialized JSON Schema draft 2020-12; per-file SHA-256 recorded in
`contracts/manifest.yaml`):

- `xfactory-document-catalog-snapshot.schema.yaml` — immutable per-repository
  document-catalog snapshot.
- `xfactory-document-cataloger-recommendation.schema.yaml` — immutable,
  non-authoritative cataloger-recommendation evidence.
- `xfactory-document-tag-registry.schema.yaml` — namespaced topic-tag registry.
- `xfactory-document-tag-overrides.schema.yaml` — owner override / disposition
  file.
- `xfactory-document-opaque-locator.schema.yaml` — reusable canonical/opaque
  document-locator `$defs` kernel.
- `xfactory-document-handling-gate.schema.yaml` — reusable dispatch/handling-gate
  decision `$defs` kernel.

Also added — `scripts/validate-document-catalog.py`: strict validator over the
packaged reference examples (`examples/document-cataloging/`) and the
deterministic cross-cutting invariants JSON Schema alone cannot express
(complete coverage, unique per-snapshot identity, source and review freshness,
taxonomy resolution, override standing, immutable path layout, and the
disclosed baseline-mode coverage exception). Registered as a tool and
content-addressed by commit; not a pinned semantic artifact, so excluded from
the per-file digest set.

Governance:

- Catalog facets are descriptive discovery metadata only: they never set a
  document's lifecycle `Status:`/`Kind:`, ownership, routing state, `xspec:`
  markers, sensitivity approval, or lifecycle changes (see
  `docs/document-lifecycle.md` "Catalog Tags Are Not Lifecycle State" and the
  `document-catalog` family in `docs/doc-health.md`). The adoption guide
  `docs/document-catalog-adoption.md` is ratified alongside this change.
- Realization evidence: the deterministic mechanical baseline covers 225/225
  governed v1 documents across six repositories (xFactory aggregation
  `800a572`), byte-equal to the freshly built extended inventory with zero
  source edits and reproduced identically across two from-scratch runs; strict
  `validate-document-catalog.py` reports 0 errors / 0 warnings against the real
  artifacts and 661/661 codexFactory tests pass at the merged SHA; the
  codexFactory `document-catalog` doc-health family and the non-authoritative
  document-cataloger lane landed in codexFactory PR #4 / PR #6, and the bounded
  read-only cataloger worker profile in omnigent-install `b836a24`.

- Nightly evidence (workflow runs 29328943314 and 29330008234, 2026-07-14):
  the first post-baseline nightly produced the dated report
  `health/reports/2026-07-14.md` (xFactory aggregation `97c4754`) with a
  rendered "Document Catalog" section — 225 of 225 docs cataloged, facet
  states pending=1350 (all other states 0), changes 225 new / 0 changed /
  0 deleted / 0 stale / 0 rejected, classifier `document-cataloger/1`
  prompt contract v1, cataloger skipped fail-closed with
  `runner_labels_missing` (the document-cataloger profile is not yet
  deployed to the artifact-worker host) — and the immutable snapshot at
  `health/document-catalog/runs/2026-07-14/ee0b0ab6…/`. The
  `document-catalog` family contributed zero findings at static pins
  (run 29328943314); run 29330008234's 32 auto-fixable stale-entry
  findings were the ratified freshness contract firing on an unrelated
  mid-window codexFactory pin move, self-healed by the landed snapshot.
  No catalog recommendation entered the Ranked Plan and no catalog-caused
  critical/error regression was introduced.

Consumers: every DomainxFactory pins this bundle at the `contract-v1.11` tag
and verifies the per-file SHA-256 in `manifest.yaml` before treating a copy as
current; the codexFactory `document-catalog` doc-health family and the
document-cataloger worker consume the schemas and validator from their pinned
openxFactory checkout.

## contract-v1.10 — 2026-07-14 (additive; superseding hardening of the neutral Hermes customer-subject runtime, provider side)

Fourth annotated-tag release. A **superseding additive re-realization** of the
provider-side neutral Hermes customer-subject runtime family first cut at
`contract-v1.9`. Per the Immutable Tag Correction policy, the `contract-v1.9`
annotated tag and its digest inventory
(`contracts/releases/contract-v1.9.digests.yaml`) remain in place as immutable
provenance; this bundle carries the corrected bytes under the next available
version. No contract shape changes: `contract_schema_version` is unchanged,
every v1 contract path is untouched, and any consumer that pinned
`contract-v1.9` remains conformant until it deliberately upgrades.

Why a superseding release: after `contract-v1.9` was tagged, two governed
review findings hardened release-surface members, so the frozen v1.9 digest
inventory no longer reproduced the current tree (expected drift, not a defect):

- **F-U3** (`Harden release membership closure`) made the Decision-10 mandatory
  release auxiliaries unconditional members of the closed bundle (no
  `exists()` gate) and repaired two release-fragile tests, changing
  `scripts/hermes_runtime_validation/release.py` and the six
  `contracts/hermes-runtime/fixtures/release/*.yaml` inventory fixtures.
- **F-4 / F-7..F-9** (`Harden migration digest surface`) changed
  `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`.

This release refreshes the raw-Git-blob release digest inventory over the
current bytes and re-establishes manifest/changelog/tag/inventory agreement.

Host-local metadata removal (FR-042): `contracts/manifest.yaml`
`source_compatibility_ref.local_source_path` — a host-absolute developer path
(`/home/brett/...`) — is removed in this additive bundle after the recorded
repository-wide supported-consumer audit
(`openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/legacy-source-path-consumer-audit.md`,
`Status: record`) proved no supported consumer requires it. Canonical source
repository and source-commit provenance are retained; no consumer, validator,
or DomainxFactory `stack.yaml` resolved the removed field.

Gate G0 remains OPEN: the exact downstream `opensoft/xFactory-Hermes-Install`
consumer pin and its reproduced digests are required to close it and are owned
by that repository's own feature.

Changed:

- `contracts/manifest.yaml` — `contract_bundle_version` -> `contract-v1.10`;
  `source_compatibility_ref.local_source_path` removed (audited; provenance
  `repo`/`source_commit` retained).
- `contracts/releases/contract-v1.10.digests.yaml` — new realized release
  digest inventory (raw Git blob SHA-256; bytewise-`utf8` path order;
  self-excluded and commit-free) for this bundle.
- The `contracts/hermes-runtime/` family,
  `scripts/hermes_runtime_validation/`,
  `scripts/validate-hermes-runtime-contracts.py`,
  `scripts/validate-contract-release.py`, and the hermes-runtime docs are the
  realized surface (governed by `contracts/hermes-runtime/contract-index.yaml`;
  not tracked per-file in `manifest.yaml`), carrying the F-U3 and
  F-4/F-7..F-9 hardening above.

## contract-v1.9 — 2026-07-14 (additive; neutral Hermes customer-subject runtime, provider side)

Third annotated-tag release. Realizes the **provider side** of the neutral
Hermes customer-subject runtime contract family
(`add-hermes-customer-subject-runtime-contract`, feature
`005-customer-subject-runtime`): the domain-neutral customer-subject topology,
trusted-scope authority/binding/approval/traceability records, the PostgreSQL
15/16 operational contract with the governed v1-to-v2 migration and quarantine,
the scoped v2 job/run/event lifecycle, the supported-DomainxFactory regression
denominator, and this bundle's own raw-Git-blob release digest inventory plus
the consumer handoff receipt. All additive: existing v1 contract paths and
pinned consumers are unchanged.

This is the first release to carry a canonical release digest inventory
(`contracts/releases/contract-v1.9.digests.yaml`, schema
`contracts/releases/release-digest-inventory.schema.yaml`): raw Git blob
SHA-256 over every required semantic member, bytewise-`utf8` path order, the
inventory self-excluded and carrying no commit (the annotated tag anchors the
commit; a downstream consumer manifest pins the inventory digest externally).

Gate G0 remains OPEN: the exact downstream `opensoft/xFactory-Hermes-Install`
consumer pin and its reproduced digests are required to close it and are owned
by that repository's own feature.

Changed:

- `contracts/manifest.yaml` — `contract_bundle_version` -> `contract-v1.9`.
- `contracts/releases/contract-v1.9.digests.yaml` — new realized release digest
  inventory for this bundle.
- The `contracts/hermes-runtime/` family, `scripts/hermes_runtime_validation/`,
  `scripts/validate-hermes-runtime-contracts.py`,
  `scripts/validate-contract-release.py`, and the hermes-runtime docs are the
  realized surface (governed by `contracts/hermes-runtime/contract-index.yaml`;
  not tracked per-file in `manifest.yaml`).

## contract-v1.8 — 2026-07-13 (additive; avatar-first UI profile-schema alignment)

Second annotated-tag release. Realizes the **avatar-first UI standard alignment**
(`align-avatar-first-ui-standard`), aligning the domain-neutral
`avatar-first-ui-profile` schema to the released avatar-client (AVC) contract
kernel. This release consumes the `contract-v1.7` kernel **read-only** — each
profile's `runtime_compatibility` pins the kernel bundle tag, exact commit
`ddff475`, and per-file registry/interface-lock SHA-256 digests; no kernel file
is changed.

Changed:

- `contracts/schemas/avatar-first-ui-profile.schema.yaml` — AVC-aligned additive
  OPTIONAL blocks with closed (fail-closed) defaults (`runtime_compatibility`,
  `presentation`, `media`, `outcome_slots`, `fallback_slots`, `interaction_mode`,
  `speech_gate`, `timing`, `consent_purpose_mappings`, `persona_reference`,
  `retention_overlay`, `accessibility_baseline`, `handoff`). Top-level `required`
  keys unchanged; backward compatible. Per-file SHA-256 recorded in
  `contracts/manifest.yaml`.

Governance:

- Offline realization gate `scripts/validate-avatar-first-ui.py --mode realization`
  loads the released kernel registries read-only and fails closed
  (`AFUV-RUNTIME-DRIFT`) on any baseline drift or `runtime_compatibility`
  digest/tag/commit mismatch. The standard doc is ratified
  (`docs/avatar-first-ui-standard.md`; `Ratified by: align-avatar-first-ui-standard`).

Consumers: DomainxFactory repos pin this bundle at the `contract-v1.8` tag and
verify the profile-schema SHA-256 in `manifest.yaml` before treating a copy as
current.

## contract-v1.7 — 2026-07-12 (additive; first annotated-tag release)

First contract release published under mandatory annotated-tag enforcement
(Contract Versioning Policy). Realizes the neutral **avatar-client (AVC)
contract kernel** (`define-avatar-client-contract-kernel`) after the F0
brokered-call feasibility gate passed — 70/70 live trials, client-enforced
revocation (`qualify-avatar-brokered-call-feasibility`, harness commit
`5142065`).

Added — `contracts/avatar-client/` (23-file semantic set; per-file SHA-256
recorded in `contracts/manifest.yaml`):

- `shared-definitions.schema.yaml` plus eight `avc-*.schema.yaml` contracts
  (AVC-01/02/04/06/07/08/11/12) — YAML-serialized JSON Schema draft 2020-12.
- Nine closed registries under `registries/` (session-result-reasons = 15,
  consent-purposes = 3, events, commands, capabilities, fallback-modes,
  interaction-modes, retention-classes, session-outcomes).
- `acceptance-map.yaml`, `interface-lock.yaml` (frozen
  `avatar-client-parallel-v1` baseline + fail-closed F0 publication-gate pin),
  `evidence-register.yaml`, and the `fixtures/` conformance set
  (`index.yaml`, `f0-gate-cases.yaml`).
- `scripts/validate-avatar-client.py` — reference validator carrying the
  fail-closed F0 publication gate (content-addressed by commit; not a pinned
  semantic artifact, so excluded from the digest set).

Governance:

- ACR-005 revocation clarified to **client-enforced within the 5 s bound**
  (`change/clarify-avatar-revocation-client-enforced`); provider-side settle is
  recorded informationally. The registered avatar-client threat model is
  accepted.

Consumers: the avatar-client reference runtime (003) and avatar-first UI
standard (004) siblings pin this bundle at the `contract-v1.7` tag and verify
the per-file digests before treating a copy as current.

## contract-v1.6 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-credential-contracts.schema.yaml` — the five
  credential record shapes promoted from OpsxFactory evidence
  (promote-credential-contracts change; DTN-004).
- `scripts/validate-credential-contracts.py` — canonical credential
  contract validator.

## contract-v1.5 — 2026-07-09 (loosening, backward compatible)

Changed:

- `contracts/schemas/hermes-job-envelope.schema.yaml` — neutralized
  (neutralize-job-envelope change; DTN-003): `repository` and `feature_id`
  now optional, `job_type` a domain-owned string, new optional neutral
  references (`domain`, `subject_ref`, `client_ref`, `workflow_ref`,
  `focal_item_ref`, `gate_ref`, `artifact_refs`). Engineering strictness
  moves to codexFactory's engineering-job-envelope overlay.
- `contracts/schemas/hermes-job-run.schema.yaml` — `feature_id` optional.
- `contracts/schemas/hermes-job-event.schema.yaml` — unchanged (already
  neutral; lifecycle enums are domain-neutral vocabulary).

## contract-v1.4 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-workflow.schema.yaml` — neutral workflow
  contract and gate record/blocking vocabulary promoted from four-domain
  evidence (promote-workflow-gate-contract change; DTN-001, DTN-002).
- `scripts/validate-workflow-contracts.py` — canonical workflow contract
  validator (errors for structure, warnings for undeclared owner layers,
  out-of-scope kinds skipped with notice).

## contract-v1.3 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — optional
  `xfactory.promoted_from` and `xfactory.specializes` promotion-provenance
  fields (refine-promotion-provenance change). Backward compatible; existing
  stacks remain valid.

## contract-v1.2 — 2026-07-03 (additive)

Added:

- `contracts/memory-gateway/` — canonical xFactory Memory Gateway contract
  surface for Customer Hermes memory and Domain Omnigent expert
  memory/knowledge access. Includes vocabularies, consent profile, gateway
  request/response, provider profile, binding, mapping, subject safety,
  context packet, expert context packet, expert source, promotion, migration,
  usage, revocation, erasure, break-glass, and audit event schemas.
- `scripts/validate-memory-gateway.py` — canonical validation for gateway
  contracts, provider profiles, conformance fixtures, domain examples, and the
  first local runtime smoke path.

## contract-v1.1 — 2026-07-03 (additive + deprecating)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — canonical
  stack.yaml shape. Introduces `hermes.layers`: an ordered list of authority
  layers each bound to a canonical role (`customer` = served subject,
  `client` = tenant/operator organization, `domain` = reusable expert
  domain, `extension` = declared intermediate layer with authority_scope).
  Fixes the cross-domain vocabulary collision where "Client Hermes" meant
  the subject layer in some domains and the tenant layer in others.
- `scripts/validate-domain-factory.py` — canonical conformance validator,
  consumed (not copied) by domain repos. Replaces per-domain hand-rolled
  validators as the conformance baseline; domain validators may extend it.
- `docs/contract-versioning-policy.md` and this changelog.

Deprecated (warnings, removal at contract-v2.0):

- `hermes` flat keys (`subject_overlay`, `subject_layer_name`,
  `care_organization_overlay`, flat `client_overlay`/`customer_overlay`
  styles) in favor of `hermes.layers`.
- `openworkflow_*` owner/layer tokens in workflow gates in favor of
  `xfactory`.

## contract-v1.0 — 2026-06-26 (baseline)

- Initial canonical contract set migrated from install repos: job
  envelope/event/run schemas, clarification packets, avatar-first UI
  profile, domain installation overlay, governance and merge-risk
  policies, hermes operational Postgres DDL.
