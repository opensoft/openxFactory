code_surface: openxFactory (the `contracts/domain-ontology/` family and core kernel package, the canonical semantic validator and its fixtures, `scripts/apply-domain-starter.py` and the pre-run questionnaire, the Hermes domain content-manifest schema and validator, memory-gateway context-packet contracts, and the `contracts/policies/layer-vocabulary.yaml` role text); DomainxFactory and hermes-install adoption lands through their own governed changes
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)

## Why

xFactory already relies on a neutral semantic model and domain-owned ontology
inputs, but those meanings are distributed across prose, schemas, validators,
taxonomies, and overlay examples without one governed, machine-readable
extension contract. New DomainxFactories therefore lack a repeatable way to
seed their ontology, and existing domains lack an accountable lifecycle for
reviewing semantic drift, publishing compatible revisions, and updating pinned
runtime consumers.

## What Changes

- Introduce an xFactory semantic kernel that distinguishes ontology from
  taxonomy, record schema, policy, evidence, and instance knowledge graphs;
  a kernel term publishes only with two independent resolvable adopters, and
  only openxFactory classifies a kernel revision.
- Define content-addressed ontology packages with stable concept and relation
  identifiers, ownership, provenance, imports, compatibility classification,
  lifecycle state, mappings, and deterministic validation, retained
  byte-identically at their digest for as long as any pin or historical
  artifact references them.
- Require DomainxFactory ontology packages to specialize, rather than redefine,
  the neutral xFactory kernel; domain ontology content remains in the owning
  DomainxFactory repository.
- Define a reproducible domain-ontology generation pipeline for new domains:
  intake and taxonomy binding, governed source inventory, candidate extraction,
  kernel mapping, conflict and gap reporting, review fixtures, Domain Hermes
  ratification, publication, and runtime pinning.
- Make Domain Hermes accountable for domain-ontology stewardship, including
  review councils, source authority, semantic compatibility decisions,
  correction, supersession, deprecation, retirement, and release promotion.
- Make Domain Hermes accountable for measurable ontology quality: every
  release publishes coverage, unknown-term, mapping-resolution, and
  classification fixture accuracy signals with declared numerators,
  denominators, windows, and pinned fixture sets, kept separate from pass/fail
  validator conformance; degradation past domain-defined thresholds is itself
  a maintenance trigger and blocks publication without a reviewed exception.
- Require external terminologies and licensed code systems to be mapped by
  reference with recorded license classes; packages never mirror restricted
  source content.
- Define continuous ontology maintenance driven by authoritative-source
  changes, unresolved terms, mapping failures, workflow drift, domain
  expansion, and de-identified promotion candidates. Automated agents may
  discover and propose changes but may not publish or silently mutate active
  ontology meaning.
- Bind ontology packages into the domain Hermes content manifest and
  installation overlay so generated domains seed a pinned ontology and
  existing domains can migrate additively.
- Add bounded semantic-context artifacts for workflows, memory retrieval, and
  agent execution — including worker-scoped semantic-context profiles so each
  bounded Omnigent worker receives only the term subset its archetype and
  purpose need, closed over specialization ancestors and relation endpoints or
  explicitly truncated — while preserving the rule that semantic inference
  cannot grant authority, consent, approval, or cross-layer access, enforced by
  a closed field vocabulary and a ban on naming authority-plane records.
- Keep subject facts and tenant-private records outside ontology packages and
  outside the candidate registers, reports, review fixtures, and quality
  telemetry emitted beside them, with an aggregation floor on term-level
  signals; only reviewed, de-identified reusable concepts or patterns may enter
  a domain ontology through existing promotion and source-authority gates.

## Capabilities

### New Capabilities

- `xfactory-semantic-kernel`: Defines the neutral ontology meta-contract,
  stable semantic identifiers, package composition, provenance, compatibility,
  validation, bounded runtime context, and the separation between semantic and
  authority planes.
- `domain-ontology-lifecycle`: Defines how a new domain ontology is generated,
  reviewed, ratified, published, filled, monitored, corrected, superseded, and
  retired under Domain Hermes stewardship.

### Modified Capabilities

- `layer-vocabulary`: Makes domain-ontology stewardship an explicit Domain
  Hermes responsibility without moving subject facts, tenant policy, or
  xFactory contract ownership into the domain layer.
- `hermes-domain-overlay`: Adds the domain ontology package as a declarable,
  pinned, validator-covered Domain Hermes content kind and requires newly
  generated domains to provide it.
- `memory-gateway`: Requires semantic context included in bounded customer or
  expert context packets to identify the exact active ontology package and
  prevents ontology inference from bypassing existing rails.

## Impact

- New neutral ontology contracts, fixtures, validators, and compiled-context
  formats under `contracts/`
- Domain generation templates, intake outputs, source inventories, candidate
  reports, and ontology review artifacts
- Domain Hermes overlay content manifests, installation overlay bindings, and
  content-addressed release pins
- Memory gateway context-packet metadata and semantic-context validation
- DomainxFactory validation chains and generated-domain acceptance checks
- Documentation for semantic ownership, generation, maintenance, compatibility,
  promotion, and runtime consumption
- Future DomainxFactory repositories such as MedxFactory, LedgerxFactory,
  OpsxFactory, AdxFactory, and codexFactory, while preserving additive
  migration for existing pinned consumers
- Omnigent domain overlays and worker runtimes consume the worker-scoped
  semantic-context seam through a follow-up omnigent change; this change
  defines the profile contract and compilation only
