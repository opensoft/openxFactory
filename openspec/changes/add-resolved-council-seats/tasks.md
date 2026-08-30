## 1. Governance

- [x] 1.1 Validate the complete change with `openspec validate add-resolved-council-seats --strict` and resolve every structural finding.
- [x] 1.2 Obtain and record ratification of the producer-owned resolution boundary, consumer validation boundary, provenance shape, and coordinated hard cutover.

## 2. Speckit Handoff

- [x] 2.1 Create or complete exactly one Speckit feature for the openxFactory realization, with implementation tasks owned only by that feature's `tasks.md`.
- [x] 2.2 Record the Hermes Install and codexFactory successor feature identifiers and their dependency on this ratified neutral contract.
  - `successor.hermes_install.feature: 017-validate-freeze-council-roster`
  - `successor.hermes_install.provider_dependency: opensoft/openxFactory:add-resolved-council-seats:council-convening`
  - `successor.codexfactory.feature: 017-resolve-council-seat-roster`
  - `successor.codexfactory.provider_dependency: opensoft/openxFactory:add-resolved-council-seats:council-convening`
  - `successor.codexfactory.governed_workflow_subject: opensoft/codexFactory/.github/workflows/council-lane-reusable.yml@refs/heads/main`
  - `evidence.hermes_runtime: open`
  - `evidence.codexfactory_signing: open`
  - `evidence.live_oidc: open`
  - `evidence.deployment: open`
  - `evidence.merged_successors: open`

## 3. Realization Evidence

- [ ] 3.1 Record merged and green openxFactory realization evidence without claiming downstream deployment or live OIDC proof.
- [ ] 3.2 Record Hermes and codexFactory conformance evidence for standing-roster, conditional pull-in, invalid-provenance, missing-seat, stale-head, and hard-cutover cases.
- [ ] 3.3 Archive this change only after the neutral realization and both named successor realizations have landed with their required evidence.
