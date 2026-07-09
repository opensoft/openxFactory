# Staged: Job Envelope Neutralization (DTN-003)

Status: staged
Kind: architecture
Repository context: openxFactory
Source: [Domain Neutralization Candidate Register](../../../docs/domain-neutralization-candidate-register.md)
entry DTN-003 (`split`, P0).
Target capability: new `neutral-job-envelope` (delta: ADDED).
Evidence: `contracts/schemas/hermes-job-envelope.schema.yaml` requires
`repository` + `feature_id` and enumerates engineering-only `job_type`
values; `hermes-job-run` requires `feature_id`; Medx
(decision-foundation-loop) and Ops (user-lifecycle) need subject, client,
workflow, focal item, gate, and artifact references the schemas cannot
express.

## Claims (the split)

1. Neutral core (canonical schemas, additive loosening — contract-v1.5):
   `repository` and `feature_id` become optional; `job_type` enum relaxes
   to a string (domain vocabularies own the values); new optional neutral
   references: `domain`, `subject_ref`, `client_ref`, `workflow_ref`,
   `focal_item_ref`, `gate_ref`, `artifact_refs[]`.
2. Engineering overlay (codexFactory keeps its nouns):
   `schemas/engineering-job-envelope.overlay.schema.yaml` re-tightens what
   the neutral core relaxed — engineering `job_type` enum, required
   `repository` + `feature_id` — applied allOf-style over the neutral core
   for engineering jobs.
3. Backward compatible both directions: every existing engineering envelope
   (project-alfa, merge-master examples) validates against the loosened
   core unchanged; non-engineering domains can now express jobs without
   fake repository fields.
4. Provenance: codexFactory declares `specializes` (overlay refines the
   neutral schema) in `stack.yaml` — first use of the field.
5. Copy-consumers (omnigent-install) stay pinned: their copies match their
   declared openxFactory ref; they pick up the neutral core at their next
   deliberate re-pin, per the pin model.

## Neutrality test plan

All existing envelope/run/event example documents in openxFactory validate
unchanged against the loosened schemas; the engineering overlay re-validates
the same examples strictly.

## Exit

Satisfied by
[neutralize-job-envelope](../../../openspec/changes/archive/2026-07-09-neutralize-job-envelope/proposal.md)
(2026-07-09). Register DTN-003: `adopted`. Bonus finding: the neutrality
test surfaced `merge_master` missing from the old canonical enum despite
canonical-example usage — stale-vocabulary drift the split repaired.
