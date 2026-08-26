code_surface: openxFactory
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified: user approval of `add-omnigent-domain-overlay` on 2026-07-22
Realized: contracts registered at contract-v1.16; all gated realizations landed (final: worker-readiness cutover, 2026-07-24)

## Why

`installs/omnigent-install` has two of the three tiers the Hermes installs
proved out: a domain-neutral core (worker runtime, containers, generic
validators, pinned openxFactory contracts) and a per-tenant instantiation
tree (`clients/opensoft/`). It has **no domain tier**: nothing in the repo
says the current install is a software-engineering Omnigent (the bias is
implicit in the worker profiles), "Software Engineering Omnigent" content
has no home, and there is no path to a medical, accounting, ops, or
marketing Omnigent other than copy-fork — exactly the failure mode the
Hermes core/overlay/params pattern was built to prevent.
`docs/xfactory-domain-factory-model.md` names the Omnigent overlay as a
first-class part of every DomainxFactory but never designed its shape or
consumption mechanism.

The staged topic `ideation/staging/omnigent-core-domain-split/` settled the
architecture with Brett (2026-07-22): openxFactory contract first, shared
stack identity with the Hermes install, readiness ports to hermes-install,
manifest + verify as the first realization increment. The medical-harness
research (`ideation/brainstorm/medical-omnigent-harness-adaptation.md`)
contributed the neutral worker vocabulary the overlay payload needs — five
worker archetypes shared by codexFactory agent classes and MedxFactory
specialist pods, a generalized permission matrix with two constitutional
booleans, and a `never_assignable` credential tier — with a drafted
second-domain consumer already staged at
`MedxFactory/ideation/staging/medical-omnigent-overlay/`.

## What Changes

- Add the **`omnigent-domain-overlay`** capability: per-domain Omnigent
  content is authored once in each DomainxFactory repo under `omnigent/`
  (sibling of `hermes/domain/`) and consumed by install repos only via
  digest pin; the overlay payload carries worker-profile deltas, prompt
  packs, toolchain container bindings, domain validators, methodology
  preseed deltas, and lane/scaleout policy deltas under the existing
  `domain_installation_overlay` operations (`supplement/replace/constrain/
  veto`, `stricter_rule_wins: true`); every declared worker class maps to
  exactly one neutral archetype (`frame`, `generate`, `verify`, `challenge`,
  `assemble_for_admission`) and declares the generalized permission matrix
  (`read_workspace / write_artifacts / run_validations / propose_admission /
  execute_final_action / access_secrets`) with `execute_final_action` and
  `access_secrets` constitutionally false; credential requirement families
  gain a `never_assignable` tier stronger than `unassigned_by_default`.
- Add the **`omnigent-install-manifest`** capability: the Omnigent install
  manifest digest-pins the Hermes runtime manifest as the single source of
  stack identity (no parallel identity document); cardinality is exactly one
  tenant, exactly one domain overlay, N subject workloads; subject workloads
  are registry entries carrying activation state and validator mode;
  composition core→domain→tenant is digest-verified fail-closed, emits
  evidence records using the seeding vocabulary (resolve / fetch /
  digest-verify / validate / activate), and produces pre-rendered effective
  worker profiles committed with provenance annotations.
- Contract-generation decision: the new family consumes the v2
  `contracts/hermes-runtime/` set as its first install-side consumer
  (`overlay-manifest.schema.yaml` supplies the file-inventory + sha256 +
  `git_overlay_pin` shape); the frozen v1 `contracts/schemas/` set is not
  extended.
- Vocabulary: as a new contract family under
  `adopt-subject-tenant-domain-vocabulary`, machine identifiers use
  Subject/Tenant/Domain spellings from their first version. Legacy
  `customer|client` spellings appear only inside the pinned upstream Hermes
  runtime manifest and are interpreted via the published layer-vocabulary
  mapping.
- MODIFIED guidance doc: `docs/xfactory-domain-factory-model.md` gains the
  prescribed DomainxFactory `omnigent/` tree shape and its consumption
  mechanism.
- Explicitly out of scope (gated follow-up changes per the staged topic):
  the omnigent-install realization (manifest quartet + read-only
  compose/verify increment), the hermes-install worker-readiness port and
  pilot `hermes_service/` retirement, codexFactory's first `omnigent/`
  overlay authoring, and the MedxFactory second-domain params fixture.
  Worker-host mutation verbs and multi-domain fleet federation are rejected
  for this generation.

## Capabilities

### New Capabilities

- `omnigent-domain-overlay`: domain overlay home and pinned consumption,
  payload composition semantics, neutral worker archetype vocabulary,
  generalized permission matrix with constitutional booleans, and the
  `never_assignable` credential tier.
- `omnigent-install-manifest`: shared stack identity by digest pin, stack
  cardinality, subject-workload registry, fail-closed compose/verify with
  seeding-vocabulary evidence, pre-rendered effective profiles, and
  canonical vocabulary from birth.

## Impact

- Affected specs: `omnigent-domain-overlay`, `omnigent-install-manifest`
  (both new; ADDED requirements only).
- Affected contracts (at realization): new payload and install-manifest
  schemas alongside `contracts/hermes-runtime/`; no released contract file
  changes; v1 `contracts/schemas/` untouched.
- Affected docs: `docs/xfactory-domain-factory-model.md` (omnigent tree
  shape), README doc index and OpenSpec Records block.
- Downstream (gated follow-ups, not this change):
  `installs/omnigent-install`, `installs/hermes-install`,
  `xFactories/codexFactory`, `xFactories/MedxFactory` (second-domain
  fixture from its staged overlay draft).
