<!--
starter_source: openxFactory/domain-factory-starter-pack
starter_version: 14
domain_id: medx
managed_mode: scaffold
-->

# MedxFactory Domain Ontology (DRAFT)

Starter-seeded draft package under the openxFactory domain-ontology
contract (`contracts/domain-ontology/`). Domain Hermes owns everything in
this tree.

Rules:

1. `package.yaml`, `concepts.yaml`, and `sources.yaml` are digest-closed
   package CONTENT. The starter seeds them once and never overwrites; a
   rerun reports differences as conflicts.
2. Candidate records (`candidate-*.yaml`) are APPEND-ONLY. Model-assisted
   extraction enters only through
   `apply-domain-starter.py --ingest-candidates <batch.yaml>` — proposals
   from approved sources, carrying an extraction-run identity and
   confidence; a rerun never deletes, replaces, or resurrects a candidate
   or its recorded disposition.
3. Publication is a governed Domain Hermes release decision by the
   accountable steward. Validate with
   `python3 scripts/validate-domain-ontology.py <this repo>` from the
   pinned openxFactory checkout.
4. `coverage-gap-report.yaml` is starter-owned and refreshed on rerun;
   `review-fixtures.yaml` is seeded once and then review-owned.
