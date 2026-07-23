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
| [avatar-pilot-hardening](#avatar-pilot-hardening) | ADDED `avatar-pilot-hardening` | 1 | Blocked — last successor; gated on `qualify-avatar-live-voice` + the client lab landing, plus its own open forks |
| [client-credential-escrow-registry](#client-credential-escrow-registry) | MODIFIED `credential-contracts` (escrow registry + break-glass custody; possibly a sixth record kind); touches `client-infrastructure-liaison` | 1 | Ready to iterate — design inputs settled with Brett 2026-07-19; 6 open questions (delta shape + break-glass topology hardest); first consumer live (opensoft self-client QA install) |
| [client-layer-tuning](#client-layer-tuning) | MODIFIED client scaffold (`roles/` + FAO + `cost_reporting_steward`); ADDED client content schemas + `validate-client-content`; wizard verb in hermes-install | 1 | Ready to iterate — decisions settled 2026-07-22; neutral scaffold/schema change first; wizard gated on schemas; avatar surface gated on the avatar topics |
| [codexfactory-domain-hermes-content](#codexfactory-domain-hermes-content) | codexFactory `hermes/domain/` content (changes A + B) + Omnigent overlay extension in lockstep | 1 | **COMPLETE 2026-07-23** — both changes ratified, realized, archived: change A 2026-07-22 (roles + policies + closure + Omnigent lockstep) and change B 2026-07-23 (mixes, councils, escalation, memory, catalog); canonical spec `domain-hermes-content` carries all nine requirements. The Omnigent extension rode the `add-omnigent-domain-overlay` realization. Primary doc + openspec/ drafts retained as provenance. Change B COMPLETE — ratified + archived 2026-07-23 (`archive/2026-07-23-add-domain-hermes-councils-and-memory`) |
| [github-administration-plane](#github-administration-plane) | MODIFIED `roles-authority-model` (neutral App-identity tiers); new OpsxFactory-owned `github-administration` capability | 1 | COMPLETE 2026-07-15 — both exit changes ratified, realized, archived (2026-07-14-add-github-app-identity-tiers, openxFactory; 2026-07-15-add-github-administration-workflow, OpsxFactory); live rollout done, 2026-07-10 incident closed; primary doc retained as `superseded` provenance |
| [layer-content-materialization](#layer-content-materialization) | ADDED neutral `hermes_domain_overlay` contract + `overlay_path` (openxFactory); hermes-install seeding increment 2 (`layer_content` kernel + materialization) | 1 | **COMPLETE 2026-07-23** — both exits ratified, realized, archived: `add-hermes-domain-overlay-contract` (openxFactory, `contract-v1.15` tag verified) and `add-layer-content-materialization` (hermes-install PR #6 merged 696ec48, archived 2026-07-23; capability spec carries increments 1+2). Deferred increments 3–6 + gate wiring recorded in the capability spec; primary doc retained as provenance |
| [proposal-origin-contract](#proposal-origin-contract) | none yet — retained rationale for a future regulated-traceability profile | 1 | Held as read-only evidence; the origin contract itself was promoted from this topic 2026-07-12 (pointer in `ideation/README.md`'s promoted list) |
| [qualify-avatar-live-voice](#qualify-avatar-live-voice) | ADDED `avatar-live-voice` (incl. the reserved AVC-09/AVC-10 contracts) | 1 | Blocked — 5 open questions (credential custody + spend cap and activation-gate scope hardest); also gated on a released client from the lab |

## client-credential-escrow-registry

- Staging ID: `openxFactory:staging:client-credential-escrow-registry`
- Repository context: openxFactory (neutral contract — likely a
  `credential-contracts` delta + the sanctioned repo-policy exception);
  registry realization in the operator's Client Hermes tree
  (`xFactory-Hermes-Install` `config/clients/<client_ref>/credentials/`);
  escrow runbook steps in install repos (`Omnigent-Install` first);
  managed-install obligation in OpsxFactory workflow contracts.
- Source: named by Brett Heap during track-1 QA secret-custody design
  (2026-07-19); first concrete case = the opensoft self-client QA
  install's `kv-opensoft-xfactory-qa` secrets + the Flux deploy key.
- Claim: per-client SOPS/age-encrypted credential escrow, written at
  secret create/rotate and read only at break-glass; exactly ONE
  break-glass key per operator scope in the password manager (public
  recipient committed, so routine escrow never touches the key);
  multi-recipient adds optional client-held recovery; custody is
  operator-side OUTSIDE the client estate (survives client-tenant +
  client-GitHub destruction); under `opsxfactory_executed` escrow is an
  explicit testable obligation, with a drift audit (every `vaultref://`
  has a registry entry) checkable without decryption.
- Files:
  - [client-credential-escrow-registry.md](client-credential-escrow-registry/client-credential-escrow-registry.md) — primary: custody model, 7 claims, 6 open questions, exit.
- Open questions (blocking): delta shape (MODIFIED `credential-contracts`
  vs new capability); master-key rotation/blast-radius runbook;
  break-glass authorization topology + post-use rotation; dedicated
  registry-repo escalation criteria; MUST-escrow scope boundary
  (non-vault plumbing credentials like deploy keys); validator for
  registry structure + SOPS-metadata lint.
- Exit: one openxFactory OpenSpec change; archives only on the first
  escrowed install (opensoft self-client QA) with drift audit green and a
  REHEARSED break-glass restore drill recorded.

## avatar-pilot-hardening

- Staging ID: `openxFactory:staging:avatar-pilot-hardening`
- Repository context: openxFactory (neutral capability + pilot-gate acceptance); real Hermes adapters in `installs/hermes-install`; domain overlays/personas in the DomainxFactory repos; the live client in the private `xfactory-avatar-client` repo.
- Source: named the last successor in the avatar-client parallel-workstream plan; the threat model's deferred-to-pilot items; the reference authority stub in `xfactory/avatar_runtime/`.
- Claim: replace the reference runtime's static fail-closed authority stub with real Hermes control + delegation behind the frozen ports ("tightens rather than changes the protocol"); add per-domain overlays/personas; commission the formal WCAG audit; stand up operations/telemetry; run a staged live pilot with rollback — closing the threat-model items the kernel deferred to pilot (client-integrity TM-03, privacy review, penetration test, production authorization).
- Files:
  - [avatar-pilot-hardening.md](avatar-pilot-hardening/avatar-pilot-hardening.md) — primary: scope, claims, gates (qualified live profile + SBOM + license review + formal a11y audit), open questions, exit.
- Open questions (blocking): see the fragment — plus it is structurally last: it cannot propose until `qualify-avatar-live-voice` publishes a qualified live profile and the client lab lands.
- Exit: create `avatar-pilot-hardening` (`code_surface: openxFactory, xfactory-avatar-client, installs/hermes-install, xFactories/*`); archives only on merged + green + recorded pilot-gate evidence.

## client-layer-tuning

- Staging ID: `openxFactory:staging:client-layer-tuning`
- Repository context: openxFactory (scaffold `roles/`, content schemas,
  `validate-client-content`) + codexFactory `hermes/client/` (domain
  defaults) + `xFactory-Hermes-Install` (wizard verb).
- Source: 2026-07-22 review pass over the client brainstorm cluster
  (`client-layer-scaffold.md`, `client-layer-roster-draft.md`,
  `client-layer-content-draft.md`, `client-policy-wizard.md`).
- Claim: per-client tuning made real — house-team `roles/` join the neutral
  scaffold (11 personas incl. the new Finance & Accounting Officer +
  `cost_reporting_steward` worker; voice floor locked); the facts rule splits
  domain defaults from wizard-only values; stricter-only is enforced
  mechanically per the comparability spec (review fallback); the wizard
  (avatar-assisted first, CLI on the same elicitation schema) drafts and a
  human ratifies the auto-clear envelope (per-unit allowed), emits a park-map
  every run, and commits its output as a per-client overlay that seeds
  through the standard pipeline.
- Files:
  - [client-layer-tuning.md](client-layer-tuning/client-layer-tuning.md) — primary: claims, three exit changes, open questions.
- Open questions (blocking): validator host repo; wizard-overlay digest-pin
  signing (shared with layer-content-materialization); default
  aggressiveness; RBS's directed steward; FAO↔domain efficiency-audit seam;
  avatar-flow prerequisites.
- Exit: three changes — openxFactory scaffold+schemas, codexFactory client
  defaults, hermes-install wizard verb (in that order).

## codexfactory-domain-hermes-content

- Staging ID: `openxFactory:staging:codexfactory-domain-hermes-content`
- Repository context: codexFactory (`hermes/domain/` +
  `omnigent/domain-overlay.yaml` in lockstep); neutral persona/mix/council
  schemas in openxFactory later.
- Source: 2026-07-22 review pass over the domain brainstorm cluster (5
  codexfactory-domain docs + `hermes-persona-character-model.md`); harvest
  map verified against the codexFactory tree.
- Claim: author the Domain Hermes content the seeding runtime is starved for —
  8 Option-E personas (trait vocabulary v1, decide-then-speak guardrail,
  escalation-target audit applied), the stored policy delta (position table,
  contested-position schema, coverage ratchet), two-tier councils with
  enumerated triggers, memory boundaries (worker-proposes/Lead-accepts,
  de-id schema + attestation), and the practice catalog (`promoted_in` +
  `owning_lead`); promotion extends `codex_owns` and adds the two missing
  Omnigent workers in the same change or the seed-time closure check fails.
- Files:
  - [codexfactory-domain-hermes-content.md](codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md) — primary: claims, exit changes A/B + Omnigent extension, open questions.
- Open questions (carried): gate-rules council seats; `council_small` seat
  sourcing; efficiency-audit ownership; neutral schema timing;
  `finding_class` vocabulary.
- Exit: codexFactory change A (`add-domain-hermes-roles-and-policies` —
  **raised 2026-07-22**, proposal + tasks + `domain-hermes-content` spec
  delta on codexFactory main, strict validation green; the topic's
  `openspec/` drafts are its provenance), then change B (councils/mixes/
  escalation/memory/catalog); the Omnigent extension rides change A.

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
- Exit: COMPLETE — the two planned OpenSpec changes were proposed, ratified,
  realized, and archived: (1) neutral `add-github-app-identity-tiers`
  (openxFactory, archived 2026-07-14) extending `roles-authority-model` with
  the GitHub App identity tiers; (2) `add-github-administration-workflow`
  (OpsxFactory, archived 2026-07-15) instantiating the
  `github-administration` capability. Live rollout done; the 2026-07-10
  incident is closed. The primary doc remains here as `superseded`
  provenance (its header names both successors).

## layer-content-materialization

- Staging ID: `openxFactory:staging:layer-content-materialization`
- Repository context: openxFactory (neutral `hermes_domain_overlay` contract +
  machine-readable `overlay_path`) + `xFactory-Hermes-Install` (seeding
  increment 2).
- Source: 2026-07-22 review pass over `hermes-layer-content-seeding.md` +
  `hermes-layer-seeding-mechanism.md`; increment 1 realized and archived
  2026-07-22 (hermes-install `add-seed-layer-content`, capability spec
  `layer-content-seeding`).
- Claim: take the proven read-only load path to enforcement — hybrid seam
  decided; generic `layer_content` kernel `(layer_id, content_kind,
  enforceable_payload, provenance)` + views; build-time render + seed-time
  verify; seeding-order invariant (domain → client → project,
  REFUSED-not-skip); the field-level enforceable-slice cut list is drafted;
  wizard-written client overlays unify into the same pipeline.
- Files:
  - [layer-content-materialization.md](layer-content-materialization/layer-content-materialization.md) — primary: claims, two exit changes, sequencing.
- Open questions (carried): per-kind `enforceable_payload` schemas; render
  ownership; wizard-overlay pin home/signing; re-pin range recording;
  partial re-seed.
- Exit: openxFactory `add-hermes-domain-overlay-contract` (independent, ready
  now) ∥ domain change A → hermes-install seeding increment 2.

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
