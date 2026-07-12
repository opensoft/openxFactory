# Staging Index

Status: staged
Kind: register
Repository context: openxFactory
Purpose: single kept-current inventory of every topic under `ideation/staging/`
— one row per topic, one detail section per topic. This file is the source of
truth for what is staged; `ideation/README.md` links here instead of
duplicating the list.

## Maintenance rule

Update this index in the same commit as any of:

- **New topic folder** created under `ideation/staging/` — add a row to the
  table and a detail section below.
- **File added to or removed from** an existing topic — update its Files list
  and Target capabilities if they changed.
- **Partial promotion** (some files move to an OpenSpec change's
  `supporting-docs/`) — drop the moved files from the Files list; keep the row
  if any staged file remains.
- **Full promotion** (no files remain staged) — delete the row and detail
  section here; the pointer belongs in `ideation/README.md`'s "Active
  proposals promoted from staging" list instead.

## Topics

| Topic | Delta (target capability) | Files | Readiness |
| --- | --- | --- | --- |
| [client-infrastructure-liaison](#client-infrastructure-liaison) | ADDED `client-infrastructure-liaison`; ADDED `client-infrastructure-request`; MODIFIED `roles-authority-model` | 6 | Ready to propose — recommended ID `add-client-infrastructure-liaison` |
| [github-administration-plane](#github-administration-plane) | MODIFIED `roles-authority-model` (neutral App-identity tiers); new OpsxFactory-owned `github-administration` capability | 1 | Blocked — 6 open questions unresolved; exit note says do NOT propose yet |
| [ideation-cross-reference-readiness](#ideation-cross-reference-readiness) | ADDED `ideation-cross-reference`; MODIFIED `doc-health` (nightly readiness lane) | 1 | Ready to propose — recommended ID `add-ideation-cross-reference-readiness` |
| [proposal-origin-contract](#proposal-origin-contract) | MODIFIED `document-lifecycle`; MODIFIED `doc-health`; MODIFIED `release-realization` | 2 | Ready to propose — recommended ID `add-proposal-origin-contract` |

## client-infrastructure-liaison

- Staging ID: `openxFactory:staging:client-infrastructure-liaison`
- Source: Southside Clinic MedxFactory and OpsxFactory operating-model review, 2026-07-09.
- Claim: defines a neutral Client Hermes coordination role and a structured
  `client_infrastructure_request` lifecycle for client-managed, managed-host,
  or OpsxFactory-executed infrastructure dependencies, without granting domain
  agents tenant administration authority.
- Files:
  - [client-infrastructure-liaison.md](client-infrastructure-liaison/client-infrastructure-liaison.md) — primary: problem, capability, responsibilities, authority boundary, request contract, lifecycle, required deltas/tests, exit.
  - [request-contract-and-transition-matrix.md](client-infrastructure-liaison/request-contract-and-transition-matrix.md) — the `client_infrastructure_request` artifact boundary and state transitions.
  - [role-authority-and-operating-models.md](client-infrastructure-liaison/role-authority-and-operating-models.md) — capability shape and coordination-vs-execution authority split.
  - [opsx-handoff-and-readiness-contract.md](client-infrastructure-liaison/opsx-handoff-and-readiness-contract.md) — the neutral request vs. OpsxFactory service-request handoff boundary.
  - [proposal-impact-and-adoption-map.md](client-infrastructure-liaison/proposal-impact-and-adoption-map.md) — locked decisions and per-domain adoption impact.
  - [southside-operating-model-scenarios.md](client-infrastructure-liaison/southside-operating-model-scenarios.md) — worked customer-managed / managed-host / OpsxFactory-bound scenarios.
- Exit: create `add-client-infrastructure-liaison`; at the proposal gate move
  this folder's files into that change's `supporting-docs/`, preserving the
  staging origin.

## github-administration-plane

- Repository context: openxFactory (neutral) with an OpsxFactory-owned realization.
- Source: xFactory family decision 2026-07-10 (review-lane first live run
  exposed the factory App holding org-wide `Contents: write` and bypassing
  branch protection).
- Claim: GitHub is a managed platform under the OpsxFactory service-subject
  model; separate the content-only App identity from a new
  administration-tier App identity, and put GitHub administration in
  OpsxFactory alongside Entra/Intune/endpoint management.
- Files:
  - [multi-app-identity-and-github-administration.md](github-administration-plane/multi-app-identity-and-github-administration.md) — claims, open questions, interim stop-gap state, exit.
- Open questions (unresolved — this is why the topic is blocked):
  - one administration App or several scoped ones?
  - org-level rulesets vs. per-repo branch protection?
  - gated through a generalized `endpoint_management` workflow or a dedicated github-administration workflow?
  - credential custody/rotation for the administration App key?
  - exact scope and explicit prohibited actions for the administration App?
  - is GitHub administration a second profile of `endpoint_management`, or its own capability?
- Interim state already applied (stop-gap, to be superseded): a manual
  codexFactory `main` ruleset requiring PR + 1 approval with OrganizationAdmin
  bypass; the `openxfactory` App holds org-wide `Contents: write` +
  `Pull requests: write` pending the split.
- Exit: two OpenSpec changes once the open questions are settled — do not
  propose yet. (1) neutral: extend `roles-authority-model` with GitHub App
  identity tiers; (2) OpsxFactory: a new `github-administration` capability.

## ideation-cross-reference-readiness

- Staging ID: `openxFactory:staging:ideation-cross-reference-readiness`
- Source: [brainstorm](../brainstorm/ideation-cross-reference-readiness.md)
  design session 2026-07-12; all seven open questions decided by Brett
  2026-07-12.
- Claim: a unified cross-stage topic index (`ideation/`-level, stage column)
  clustering brainstorm/staging/archive material by `Topics:`/`Target
  capabilities:` tags, scored 1-10 by three Hermes-tier reviewers
  (engineering-buildability, company/openxFactory, domain) with the full
  organizer/cataloger evidence contract; minimum score >= 8 flags "propose
  for authorization" as a recommendation only, run as a nightly doc-health
  lane, non-mutating over source docs.
- Files:
  - [ideation-cross-reference-readiness.md](ideation-cross-reference-readiness/ideation-cross-reference-readiness.md) — primary: problem, decided contract, decision record, required deltas/tests, exit.
- Exit: create `add-ideation-cross-reference-readiness` (openxFactory contract
  change paired with a codexFactory worker delta, the ideation-routing /
  document-cataloging two-repo split pattern); at the proposal gate move this
  folder's file into that change's `supporting-docs/`, preserving the staging
  origin.

## proposal-origin-contract

- Staging ID: `openxFactory:staging:proposal-origin-contract`
- Source: Brett review of the archived `add-proposal-supporting-doc-lifecycle` change, 2026-07-09.
- Claim: every OpenSpec proposal must declare exactly one origin (staged or
  approved ad-hoc) in `.openspec.yaml`, so a proposal can never bypass
  brainstorm/staging without a machine-checkable exception.
- Files:
  - [origin-contract.md](proposal-origin-contract/origin-contract.md) — problem, proposed contract (staged/ad-hoc origin kinds), proposal/archive gates, doc-health enforcement, migration, required tests, exit.
  - [fda-samd-traceability-rationale.md](proposal-origin-contract/fda-samd-traceability-rationale.md) — regulatory rationale: the origin contract is a necessary first traceability edge but is **not** by itself sufficient for FDA SaMD compliance; scopes the additional trace graph/QMS/validation work a domain (e.g. MedxFactory) would still need.
- Exit: create `add-proposal-origin-contract`; at the proposal gate move
  `origin-contract.md` into that change's `supporting-docs/`. The resulting
  `.openspec.yaml` must declare this topic's staged ID and path as the
  self-application acceptance proof. Must not claim FDA/SaMD compliance on its
  own.
