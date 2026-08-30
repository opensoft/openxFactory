---
code_surface: openxFactory neutral authority contract and its Hermes Install and codexFactory successor realizations
target_release: implementation_pending — archive only after the neutral realization and both named successor realizations land with their required evidence
Status: ratified
Ratified: 2026-08-28 by Brett — in-session selection of "Ratify and proceed (Recommended)" after the complete packet passed strict validation
Proposed: 2026-08-28
Origin: Investigation of the split roster-resolution boundary between Hermes admission and codexFactory conditional-seat evaluation, followed by Brett's instruction to create a dedicated neutral change
---

# Proposal: add-resolved-council-seats

## Why

The ratified substantive-review rule can require a conditional council seat for
one pull request while omitting it for another, but the neutral convening
contract carries no resolved roster from the rule-owning producer to the Hermes
admission boundary. Hermes therefore cannot validate and freeze the actual
required seats before it issues seat jobs, leaving conditional participation to
be decided too late and making fail-closed completeness unverifiable.

## What Changes

- **BREAKING**: require producers to submit a resolved,
  per-convening `council_convening.required_seats` value; payloads that omit the
  resolved roster are not accepted through a compatibility path.
- Make the trusted producer resolve required seats from the governed candidate
  class rules and candidate facts before convening admission, including any
  conditional company-policy pull-in whose declared condition holds.
- Require provenance that identifies the governed class/rule revision and the
  candidate facts used to derive the roster, so the resolution can be
  reproduced rather than trusted as an unsupported assertion.
- Require the consumer to validate and freeze the resolved roster before
  issuing seat jobs, and to use that same frozen roster for completion and
  verdict-conformance checks.
- Fail closed when the roster or its provenance is absent, malformed,
  duplicated, unknown, inconsistent with the governing rule, or cannot be
  evaluated.
- Preserve the standing domain-seat roster, the bounded conditional pull-in
  exception, and refusal when a required seat cannot be seated.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `roles-authority-model`: add the neutral producer/consumer contract for
  resolving, proving, validating, and freezing the required seat roster of one
  convening.

## Impact

- `openxFactory`: neutral authority requirements and their realization handoff.
- Hermes Install: consumer-side validation, admission snapshotting, seat-job
  issuance, and completion checks against one frozen roster.
- codexFactory: producer-side candidate-class evaluation and the convening
  workflow payload that submits the resolved roster and provenance.
- Existing producer payloads without `council_convening.required_seats` are
  intentionally rejected after cutover. This proposal claims no live GitHub
  OIDC, deployment, image, or merged-commit evidence.
