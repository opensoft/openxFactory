---
code_surface: none (a governance capability plus a release-realization spec delta; the runtime surfaces — the OpsxFactory QA deployment profile, subject-registry lookup at grant issuance, evidence-correlation audit, and ACR namespace scope map, and the codexFactory release exit step — land through named successor changes in their owning repositories per repo-boundary-governance)
target_release: implemented (doc-only; archives when the ratified artifacts land and the supporting bundle packages)
Status: ratified
Ratified: Brett's approval of `add-deployment-handoff-boundary` on 2026-07-29, on his seven clarifying resolutions of 2026-07-24 carried as design decisions 2–9 (all-actor scope, credentials-primary enforcement, grant-issuance and GitOps-merge gates, correlation stamping, standing bench requests, retroactive break-glass with escrow-owned custody, phased-never-gapped adoption, codexFactory sole first consumer) plus the capability-home confirmation at the proposal gate; the four residual questions (QA approval calibration, ACR namespace scope map, preview-environment threshold, break-glass window) are deliberately deferred to the successor realizations
---

# Proposal: add-deployment-handoff-boundary

## Why

Who executes a deployment is today only implied: OpsxFactory's `deployment`
workflow exists at `production_critical`, and the
`cir-opensoft-qa-codexfactory-install` precedent already routes the
codexFactory install surface on the QA cluster through
`client-infrastructure-execution`. But no ratified neutral requirement says a
producing factory must hand a release to the factory that manages the target
surface, nothing binds human engineers and CI pipelines to the same rule as
workers, and nothing makes an out-of-band change detectable rather than
merely forbidden. The failure this permits is the known disease: a second
operator silently mutating a managed surface, drift with no evidence trail,
and recovery by archaeology. Source: operator ruling 2026-07-24 (Brett,
during the worker-host-app kickoff), confirmed as the managed-subject
formulation with seven clarifying resolutions the same day.

## What Changes

- Ratify the managed-subject test as the sole deployment routing rule:
  execution authority follows management of the target surface, never the
  environment tier; tier calibrates governance depth only. The rule binds
  every actor class — factory workers, CI pipelines, and human engineers.
- Make the ratified `client_infrastructure_request` the handoff crossing (a
  deployment requirements-profile of it; no new record kind), with the
  producing factory's authority ending at the release artifact, digests, and
  realization evidence.
- Ratify credential non-possession as the primary enforcement: only
  managing-factory execution identities hold standing write credentials to
  managed surfaces; producing-factory identities keep build-namespace push
  only; deployment grants issue per accepted request against a registered
  subject and revoke on completion; human access is break-glass with a
  retroactive request.
- Ratify structural channels where the surface supports them: pull-only
  reconciliation from a managing-factory-governed configuration tree (merge
  is the deployment) or managed endpoint assignment; push-path mutation is a
  grant-gated exception.
- Make out-of-band change detectable: correlation identifiers stamped into
  every touched change surface and a periodic evidence-correlation audit in
  which an uncorrelated change is a first-class finding.
- Put cadenced publication (bench rebuilds and similar) on one standing
  approved request per policy period with per-run correlation and digest
  evidence.
- Adopt phased-never-gapped migration: existing standing admin is a named,
  dispositioned exception until the break-glass checkout path is realized
  and tested, then a dated milestone removes standing assignments.
- Modify `release-realization`: realization evidence for a deployment onto a
  managed subject references the completed handoff request by correlation
  identifier.
- Name the successor realization changes: OpsxFactory (QA
  requirements/validation profile of the deployment workflow,
  subject-registry lookup at grant issuance, evidence-correlation audit, ACR
  namespace scope map) and codexFactory (release exit step emits the request
  draft; no direct deploy path). Break-glass custody and the policy window
  stay with `client-credential-escrow-registry` — coordinate, don't fork.

## Capabilities

### New Capabilities

- `deployment-handoff-boundary`: the managed-subject routing rule, the
  handoff crossing artifact, credential non-possession, structural channels,
  out-of-band detectability, standing maintenance requests, and
  phased-never-gapped adoption.

### Modified Capabilities

- `release-realization`: realization evidence for a release deploying onto a
  registered managed subject of another factory references the completed
  handoff request by correlation identifier (correlation, not duplication).

## Impact

- New capability spec and the release-realization delta in openxFactory;
  no openxFactory runtime artifacts
- Successor changes in OpsxFactory and codexFactory carry all realization;
  their pin and workflow updates stay in their owning governed changes
- Coordination surface with `client-credential-escrow-registry` (break-glass
  custody, checkout, policy window) and with the worker-host-app bench
  pipeline (ACR namespace scope map — same registry, same decision)
- Staging bookkeeping: the topic doc moves to `supporting-docs/`, the
  staging INDEX row and detail section retire, and the ideation README
  promoted list and repository README OpenSpec Records gain entries
- DTN-017 `subject-establishment` consumes this seam for its codexFactory
  second consumer, where the designing domain and the applying administrator
  are different factories
