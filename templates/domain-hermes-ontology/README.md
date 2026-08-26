# Domain Hermes Ontology Stewardship Templates

Status: ratified
Kind: template
Ratified by: add-domain-ontology-layer (task 5.2)
Repository context: openxFactory

Instantiation stubs for the Domain Hermes ontology stewardship records
(`contracts/domain-ontology/`). The starter seeds a live
`hermes/domain/ontology/stewardship.yaml` with deterministic defaults;
these templates cover the records Domain Hermes produces while operating
the lifecycle. Every `.template.yaml` follows the repo rule: copy, fill,
drop the `.template` suffix, never commit raw credentials.

| Template | Record | Used when |
| --- | --- | --- |
| `stewardship-policy.template.yaml` | `xfactory_ontology_stewardship_policy` | tuning council, cadence, mode workflows, triggers, quality gate, privacy floor |
| `candidate-disposition.template.yaml` | `xfactory_ontology_candidate_record` | a steward decides an open candidate (accept/reject/withdraw) |
| `release-approval.template.yaml` | `xfactory_ontology_release_record` | the accountable steward publishes a version (see `scripts/ontology-release.py`) |
| `consumer-adoption.template.yaml` | `xfactory_ontology_release_record` `adoptions` fragment | a consumer explicitly re-pins to a published version |
| `maintenance-input.template.yaml` | `xfactory_ontology_maintenance_input` | governed telemetry feeds `scripts/ontology-maintenance.py` |
