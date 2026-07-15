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
- **Demotion** (a proposal returns to staging for continued design) — the
  reverse of promotion: the change's artifacts come back as the topic (its
  OpenSpec docs into the topic's `openspec/` drafts), the row and detail
  return here, and the README promoted-list pointer is removed.

## Draft-proposal workspace convention

A staging topic may carry an `openspec/` subfolder holding working drafts
of its future proposal — proposal, design, tasks, and spec-delta slices,
each `Status: draft` with a "Draft slice of:" pointer to the topic's
primary doc. Drafts iterate freely in staging; at the proposal gate they
move to `openspec/changes/<change-id>/` (front-matter restored, draft
headers stripped) and the topic's source docs follow into
`supporting-docs/` per the document lifecycle. Adopted 2026-07-13 (Brett),
first used by ideation-dashboard; formalizing the convention in the
document-lifecycle spec is a candidate for the next lifecycle change.

## Topics

| Topic | Delta (target capability) | Files | Readiness |
| --- | --- | --- | --- |
| [avatar-client-lab](#avatar-client-lab) | ADDED `avatar-client-lab` | 4 | Ready to propose — 6 decisions locked 2026-07-13; recommended ID `implement-avatar-client-lab` |
| [avatar-pilot-hardening](#avatar-pilot-hardening) | ADDED `avatar-pilot-hardening` | 1 | Blocked — last successor; gated on `qualify-avatar-live-voice` + the client lab landing, plus its own open forks |
| [client-infrastructure-liaison](#client-infrastructure-liaison) | ADDED `client-infrastructure-liaison`; ADDED `client-infrastructure-request`; MODIFIED `roles-authority-model` | 6 | Ready to propose — recommended ID `add-client-infrastructure-liaison` |
| [github-administration-plane](#github-administration-plane) | MODIFIED `roles-authority-model` (neutral App-identity tiers); new OpsxFactory-owned `github-administration` capability | 1 | COMPLETE 2026-07-15 — both exit changes ratified, realized, archived (2026-07-14-add-github-app-identity-tiers, openxFactory; 2026-07-15-add-github-administration-workflow, OpsxFactory); live rollout done, 2026-07-10 incident closed |
| [proposal-origin-contract](#proposal-origin-contract) | none yet — retained rationale for a future regulated-traceability profile | 1 | Held as read-only evidence; the origin contract itself was promoted from this topic 2026-07-12 (pointer in `ideation/README.md`'s promoted list) |
| [qualify-avatar-live-voice](#qualify-avatar-live-voice) | ADDED `avatar-live-voice` (incl. the reserved AVC-09/AVC-10 contracts) | 1 | Blocked — 5 open questions (credential custody + spend cap and activation-gate scope hardest); also gated on a released client from the lab |

## avatar-client-lab

- Staging ID: `openxFactory:staging:avatar-client-lab`
- Repository context: openxFactory (neutral acceptance + fixtures); Flutter application realized in the private `xfactory-avatar-client` repository.
- Source: v1 brainstorm 2026-07-13 (six-dimension synthesis); named successor in the avatar-client parallel-workstream plan; supersedes the historical `flutter-avatar-client-ui-lab` exploration.
- Claim: an offline, deterministic Flutter avatar client UI lab (F1-F4) rendering the full avatar-first interaction and authority model from replayed fixtures — no live model/voice/WebRTC/broker; a pure reducer mirroring the reference-runtime invariants, ports so voice is a later adapter swap, and a replaceable six-state avatar. openxFactory owns the neutral acceptance; the Flutter app lives in a private repo.
- Files:
  - [avatar-client-lab.md](avatar-client-lab/avatar-client-lab.md) — primary: problem, capability + `avatar-client-lab` (ADDED) delta, scope in/out, acceptance summary, exit.
  - [architecture-and-stack.md](avatar-client-lab/architecture-and-stack.md) — the v1 architecture and recommended stack (pure reducer, Riverpod-over-core, ports/adapters, CustomPainter avatar, hybrid contracts, monorepo, M0).
  - [open-decisions.md](avatar-client-lab/open-decisions.md) — the six formerly blocking forks, locked 2026-07-13 with rationale (schema validator with fallback trigger, Riverpod binding, contract pin, web a11y claim, golden platform, fixture-duality loader).
  - [acceptance-and-tests.md](avatar-client-lab/acceptance-and-tests.md) — the F1-F4 acceptance foci, the inherited scenario map (released acceptance maps already name `implement-avatar-client-lab` as an owner change), and the CI gate set.
- Readiness: the six decisions are locked; the topic is ready to promote.
- Exit: create `implement-avatar-client-lab` (`code_surface: openxFactory, xfactory-avatar-client`); at the proposal gate move this folder's files into that change's `supporting-docs/`, preserving the staging origin, and author the full `avatar-client-lab` spec deltas + F1-F4 tasks (including the acceptance/evidence map and CI gates from acceptance-and-tests.md).

## avatar-pilot-hardening

- Staging ID: `openxFactory:staging:avatar-pilot-hardening`
- Repository context: openxFactory (neutral capability + pilot-gate acceptance); real Hermes adapters in `installs/hermes-install`; domain overlays/personas in the DomainxFactory repos; the live client in the private `xfactory-avatar-client` repo.
- Source: named the last successor in the avatar-client parallel-workstream plan; the threat model's deferred-to-pilot items; the reference authority stub in `xfactory/avatar_runtime/`.
- Claim: replace the reference runtime's static fail-closed authority stub with real Hermes control + delegation behind the frozen ports ("tightens rather than changes the protocol"); add per-domain overlays/personas; commission the formal WCAG audit; stand up operations/telemetry; run a staged live pilot with rollback — closing the threat-model items the kernel deferred to pilot (client-integrity TM-03, privacy review, penetration test, production authorization).
- Files:
  - [avatar-pilot-hardening.md](avatar-pilot-hardening/avatar-pilot-hardening.md) — primary: scope, claims, gates (qualified live profile + SBOM + license review + formal a11y audit), open questions, exit.
- Open questions (blocking): see the fragment — plus it is structurally last: it cannot propose until `qualify-avatar-live-voice` publishes a qualified live profile and the client lab lands.
- Exit: create `avatar-pilot-hardening` (`code_surface: openxFactory, xfactory-avatar-client, installs/hermes-install, xFactories/*`); archives only on merged + green + recorded pilot-gate evidence.

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
- Open questions — resolved 2026-07-14 (see the primary doc's "Open questions
  — resolved" section for full recommendations):
  - one administration App or several scoped ones? → one App, narrowed via
    scoped credential grants, not App count (scoped to Opensoft's own org;
    client-tenant execution routes through `client-infrastructure-liaison`).
  - org-level rulesets vs. per-repo branch protection? → org rulesets for
    Opensoft's own org (Enterprise confirmed); client tenants need a
    plan-tier-aware org/repo/classic fallback ladder.
  - gated through a generalized `endpoint_management` workflow or a dedicated
    github-administration workflow? → dedicated workflow, extending the
    existing read-only `github-admin` command class.
  - credential custody/rotation for the administration App key? → DTN-004
    shape unchanged, at the family's strictest existing tier (15-min grants,
    Key Vault, 90-day max age, environment-gated).
  - exact scope and explicit prohibited actions for the administration App?
    → 7-repo Tier 1 now, `installs/*` deferred; rulesets/branch-protection
    only, enforced at the workflow/credential layer.
  - is GitHub administration a second profile of `endpoint_management`, or
    its own capability? → own capability, sibling to `endpoint_management`.
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

## qualify-avatar-live-voice

- Staging ID: `openxFactory:staging:qualify-avatar-live-voice`
- Repository context: openxFactory owns the neutral live-voice acceptance, the ADDED AVC-09/AVC-10 contract schemas, the `interface-lock.yaml` unreservation, and the acceptance-map/validator updates; the live transport (`avc_adapters_live`) is realized in the private `xfactory-avatar-client` repo.
- Source: named successor in the avatar-client-lab staging topic and the F0 feasibility spec; draws the live-voice baseline, GPT-Live-1 activation gate, latency requirement, and voice-session topology from the archived `flutter-avatar-client-ui-lab` exploration.
- Claim: internal-live provider qualification — the live WebRTC/broker/media plane behind the existing `SessionTransport` port (brokered SDP, direct Flutter↔provider media, `gpt-realtime-2.1` candidate), adding AVC-09 (adapter descriptor) and AVC-10 (latency sample) as the ADDED live contracts, with a latency-instrumented activation gate, canary, and rollback. F0 proved feasibility; this change qualifies live use.
- Files:
  - [qualify-avatar-live-voice.md](qualify-avatar-live-voice/qualify-avatar-live-voice.md) — primary: scope, claims (AVC-09/AVC-10, activation gate, latency budgets), open questions, exit.
- Open questions (blocking): credential custody + spend cap; latency-budget derivation; the activation-gate scope; data-control/consent for evaluation audio; canary/rollback shape. Also gated on a released, code-signed client from the lab.
- Exit: create `qualify-avatar-live-voice` (`code_surface: openxFactory, xfactory-avatar-client`); archives only on merged + green internal-live realization evidence.
