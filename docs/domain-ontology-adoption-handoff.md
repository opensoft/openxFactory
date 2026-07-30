# Domain-Ontology Adoption Handoff

Status: record
Kind: runbook
Ratified by: [add-domain-ontology-layer](../openspec/changes/add-domain-ontology-layer/proposal.md) (task 7.5)
Repository context: openxFactory
Purpose: the downstream handoff packets — what each consumer adopts, with
which pins, through its OWN governed change (adoption never lands from
here; repo-boundary governance holds).

Common pins: kernel `xf/core` 0.1.0, digest
`9d4ea5fa3e44505bbe1c3e00c5f007941cf0a30f6cbd0f2030cd83250dd505a5` (DRAFT;
publication rides the bundle cut). Contract family
`contracts/domain-ontology/` (eighteen kinds), canonical validator
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

## Omnigent (REALIZED — `add-omnigent-semantic-wiring`, 2026-07-30)

The named follow-up landed at contract-v1.23. The declaration surface is
the omnigent domain overlay: a worker class MAY carry
`semantic_context: {profile_id, package_id}` (identity only; digests ride
compiled contexts), resolved in repo mode by
`validate-omnigent-contracts.py <domain-repo>` against the repo's
inventoried `xfactory_semantic_context_profile` documents with
worker_scope archetype-or-class agreement. The install surface is the
omnigent install manifest's `semantic_contexts` section: exact kernel and
domain package pins plus one compiled artifact per declaring worker,
both-direction completeness and per-artifact pin/digest/scope agreement
fail-closed (`install_wiring_errors`, exercised by
`test-omnigent-semantic-wiring.py`). Workers consume the artifact through
memory-gateway packets (the `semantic_context` block live in both packet
contracts), the compile tool refuses drifted package bytes and itemizes
truncation transitively, and the permission matrix stays untouched —
`execute_final_action` and `access_secrets` constitutionally false.
First consumer: MedxFactory (80a81af) — two inventoried profiles,
declarations on `data_reverification_agent` (archetype-scoped) and
`case_framing_agent` (class-scoped). Install repositories adopt through
their own governed changes.
