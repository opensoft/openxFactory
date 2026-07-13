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
| [avatar-client-lab](#avatar-client-lab) | ADDED `avatar-client-lab` | 3 | Blocked — 6 open decisions unresolved (see topic); design direction settled |
| [client-infrastructure-liaison](#client-infrastructure-liaison) | ADDED `client-infrastructure-liaison`; ADDED `client-infrastructure-request`; MODIFIED `roles-authority-model` | 6 | Ready to propose — recommended ID `add-client-infrastructure-liaison` |
| [github-administration-plane](#github-administration-plane) | MODIFIED `roles-authority-model` (neutral App-identity tiers); new OpsxFactory-owned `github-administration` capability | 1 | Blocked — 6 open questions unresolved; exit note says do NOT propose yet |
| [proposal-origin-contract](#proposal-origin-contract) | none yet — retained rationale for a future regulated-traceability profile | 1 | Held as read-only evidence; the origin contract itself was promoted from this topic 2026-07-12 (pointer in `ideation/README.md`'s promoted list) |

## avatar-client-lab

- Staging ID: `openxFactory:staging:avatar-client-lab`
- Repository context: openxFactory (neutral acceptance + fixtures); Flutter application realized in the private `xfactory-avatar-client` repository.
- Source: v1 brainstorm 2026-07-13 (six-dimension synthesis); named successor in the avatar-client parallel-workstream plan; supersedes the historical `flutter-avatar-client-ui-lab` exploration.
- Claim: an offline, deterministic Flutter avatar client UI lab (F1-F4) rendering the full avatar-first interaction and authority model from replayed fixtures — no live model/voice/WebRTC/broker; a pure reducer mirroring the reference-runtime invariants, ports so voice is a later adapter swap, and a replaceable six-state avatar. openxFactory owns the neutral acceptance; the Flutter app lives in a private repo.
- Files:
  - [avatar-client-lab.md](avatar-client-lab/avatar-client-lab.md) — primary: problem, capability + `avatar-client-lab` (ADDED) delta, scope in/out, acceptance summary, exit.
  - [architecture-and-stack.md](avatar-client-lab/architecture-and-stack.md) — the v1 architecture and recommended stack (pure reducer, Riverpod-over-core, ports/adapters, CustomPainter avatar, hybrid contracts, monorepo, M0).
  - [open-decisions.md](avatar-client-lab/open-decisions.md) — the six blocking open decisions with recommended resolutions.
- Open questions (blocking — this is why the topic is not yet ready to propose): Dart 2020-12 schema validator (Workiva vs port the subset); web accessibility conformance claim; fixture-format duality; plus state-binding, contract-pin, and golden-platform forks with strong recommendations.
- Exit: create `implement-avatar-client-lab` (`code_surface: openxFactory, xfactory-avatar-client`); at the proposal gate move this folder's files into that change's `supporting-docs/`, preserving the staging origin, and author the full `avatar-client-lab` spec deltas + F1-F4 tasks in the change.

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

- Staging ID: `openxFactory:staging:github-administration-plane`
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

## proposal-origin-contract

- Staging ID: `openxFactory:staging:proposal-origin-contract`
- Source: Brett review of the archived `add-proposal-supporting-doc-lifecycle` change, 2026-07-09.
- Partial promotion 2026-07-12: the primary origin-contract doc crossed the
  proposal gate (pointer in `ideation/README.md`'s "Active proposals promoted
  from staging" list); this topic now holds only the regulatory rationale.
- Claim (remaining file): origin provenance is a necessary first traceability
  edge but is **not** by itself sufficient for FDA SaMD compliance; the
  rationale scopes the additional trace graph/QMS/validation work a regulated
  domain (e.g. MedxFactory) would still need.
- Files:
  - [fda-samd-traceability-rationale.md](proposal-origin-contract/fda-samd-traceability-rationale.md) — read-only regulatory rationale retained for a future regulated-traceability profile.
- Exit: the rationale exits with a future regulated-traceability-profile
  topic when a regulated domain needs it; it does not exit with the origin
  contract.
