# Tasks: Promote Workflow Gate Contract

## 1. Canonical Artifacts

- [ ] 1.1 Write `contracts/schemas/xfactory-workflow.schema.yaml` per the
      staged neutralization draft (envelope, workflow object, gate record
      with both blocking styles, owner-layer constraint).
- [ ] 1.2 Write `scripts/validate-workflow-contracts.py <domain-repo>`
      validating `workflows/*.yaml` against the schema (errors/warnings per
      the capability).
- [ ] 1.3 Record contract-v1.4 in `contracts/CHANGELOG.md`.
- [ ] 1.4 Link the schema from the README Conformance section.

## 2. Neutrality Test

- [ ] 2.1 Run the validator against all five domains; the four evidence
      workflows pass unchanged; capture the codexFactory envelope errors as
      expected adoption findings.

## 3. Register And Staging

- [ ] 3.1 Move DTN-001 and DTN-002 to `openspec` status referencing this
      change; close the staged topic with its exit.

## 4. Adoption (cross-repo; gates register `adopted`, not archival)

- [ ] 4.1 **CROSS-REPO (codexFactory)** Add `schema_version`/`kind`
      envelopes to its workflow YAMLs; validate clean.
- [ ] 4.2 **CROSS-REPO (all five domains)** Declare `promoted_from`
      (candidate ids DTN-001, DTN-002) in each `stack.yaml`; re-validate;
      move register entries to `adopted`.

## 5. Validation

- [ ] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate promote-workflow-gate-contract --strict`
      and `--all --strict` pass.
