# Domain-Ontology Adoption Handoff

Status: record
Kind: runbook
Ratified by: [add-domain-ontology-layer](../openspec/changes/add-domain-ontology-layer/proposal.md) (task 7.5)
Repository context: openxFactory
Purpose: the downstream handoff packets — what each consumer adopts, with
which pins, through its OWN governed change (adoption never lands from
here; repo-boundary governance holds).

Common pins: kernel `xf/core` 0.1.0, digest
`46e45f6c2da2bb8fbad910fb2aa14d667b60319cc17ecf049658453b8dd898b7` (DRAFT;
publication rides the bundle cut). Contract family
`contracts/domain-ontology/` (fourteen kinds), canonical validator
`scripts/validate-domain-ontology.py`, tools `apply-domain-starter.py`
(v13, `--answers`/`--ingest-candidates`), `ontology-maintenance.py`,
`ontology-release.py`, `ontology-compile-context.py`.

## MedxFactory (pilot: `examples/pilots/medx`)

1. Own change: adopt the ontology answer set (real roster replaces the
   pilot's placeholder stewards — DECIDED 2026-07-29 in the
   `medxfactory-domain-hermes-content` roster round: a dedicated
   `ontology-steward` persona in the eight-persona roster is the
   accountable ontology steward; MxD-MRR wears the ontology review seats
   and `high_impact_requires: [licensed_human]` carry as leanings to the
   change-A gate), run the v13 starter, review/disposition candidates,
   publish via `ontology-release.py`, and pin `domain_ontology` in
   `hermes/domain/content-manifest.yaml`.
2. External terminologies register by reference with license classes
   (`no_redistribution` clinical systems never mirror); quality gate and
   aggregation floor come from `hermes/domain/ontology/stewardship.yaml`.
3. Acceptance: `validate-domain-ontology.py <repo>` green and
   `--readiness` returning `ontology_ready`.

## codexFactory (pilot: `examples/pilots/codex`)

Same steps with the engineering answer set; the pilot demonstrates the
retiring flow (`xf/codex@2`) and the `verify`/`assemble_for_admission`
worker profiles its lanes will consume.

## hermes-install

Consumes `domain_ontology` from the content manifest during seeding: fail
closed on an invalid or digest-drifted package (the
`hermes-domain-overlay` delta and `validate-hermes-domain-overlay.py`
generated-domain completeness rule are already promoted/realized here).
Own change: seeding increment that validates and materializes the package
and records the runtime pin.

## Omnigent (the named follow-up change)

The seam is ready: `xfactory_semantic_context_profile` (per-archetype /
per-class term subsets, `truncation_allowed`) + deterministic compilation
producing closed, digest-pinned per-worker contexts, proven by fixture and
pilots. The follow-up change decides the declaration surface (leading:
the omnigent domain overlay declares worker-class profiles; the ontology
validator proves the referenced subsets exist), wires worker runtimes to
consume compiled contexts through memory-gateway packets (the
`semantic_context` block is live in both packet contracts), and leaves the
permission matrix untouched — `execute_final_action` and `access_secrets`
stay constitutionally false.
