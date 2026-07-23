# Ideation Work Area

Status: ratified
Kind: process
Ratified by: [add-document-lifecycle-vocabulary](../openspec/changes/archive/2026-07-09-add-document-lifecycle-vocabulary/proposal.md)
Repository context: openxFactory
Purpose: provide the governed pre-proposal pipeline that turns free-form
thinking into OpenSpec proposals, so prose never silently becomes (or
contradicts) policy.

## Lifecycle

```text
brainstorm/<topic>.md      free-form discussion and design exploration;
                           explicitly NON-NORMATIVE — nothing here is policy,
                           and doc-health checks ignore contradictions here
      |
      |  organize gate: pieces get identity, duplicates merge,
      |  each fragment names the spec or capability it targets
      v
staging/<topic>/           structured fragments ready for proposal drafting:
                           claim, target capability, delta type
                           (ADDED / MODIFIED / REMOVED), evidence links
      |
      |  proposal gate: selected files move with Git history
      v
openspec/changes/<name>/   a normal OpenSpec change proposal with source
  supporting-docs/        material and a manifest; from here the standard
                           flow applies (approve -> implement -> archive)
      |
      |  archive gate: support becomes a verified tar-gzip bundle
      v
openspec/changes/archive/  proposal history + promoted spec delta + bundle
```

Rules while this convention is in draft:

- Content in `brainstorm/` may contradict promoted specs freely; that is what
  the area is for. Everywhere else, prose that changes promoted policy must be
  an explicit delta (see the doc-health pipeline brainstorm).
- Moving material from `brainstorm/` to `staging/` and from `staging/` to an
  OpenSpec change are deliberate, reviewed steps. Selected staged files are
  moved, not copied, into the change's `supporting-docs/` folder. Unselected
  files remain staged for a later proposal.
- `ideation/staging/` lists only organized work that has not crossed a proposal
  gate. Completed proposal source is retained with the active or archived
  OpenSpec change, not as a stale staged topic.
- Each DomainxFactory keeps its own `ideation/` area for domain-scoped topics;
  cross-factory and contract-level topics belong here in openxFactory.

## Ideation Header Format

Every file under `brainstorm/` uses this title and header, in this order:

- Title: `# <Title> — Brainstorm` — always end the H1 with the
  ` — Brainstorm` suffix (imported/evidence files keep an identifying
  prefix, e.g. `# NotebookLM Ideas: <workspace> — Brainstorm`), so
  `grep '— Brainstorm$'` finds every brainstorm doc by title alone.
- `Status:` — `brainstorm` (raw capture) or `staged` (organized; kept as
  design history) per the [document lifecycle](../docs/document-lifecycle.md)
  taxonomy. Status tracks lifecycle state, not folder — an organized
  brainstorm file stays physically in `brainstorm/` with `Status: staged`.
- `Kind:` — required; one of the recommended vocabulary (`architecture |
  plan | process | runbook | report | register | template | reference`).
- `Summary:` — required; one sentence stating what the document concludes or
  proposes, not its intent — write it so a reader never has to open
  `## Problem` to know what's inside.
- `Topics:` — required; a comma-separated list of subject keywords (target
  capability names where one exists, plus free-text terms), so `grep
  'Topics:'` across `ideation/` surfaces every doc touching a subject
  without reading prose bodies. Standard tag: `feat-request` marks an
  enhancement request against an existing or realized capability — the
  request is an ordinary brainstorm capture that clusters with its
  capability via Topics, seeds `Possible feats`, and realizes as a
  MODIFIED-capability OpenSpec delta when picked.
- `Repository context:` — required.
- `Captured:` — the date free-form thinking was captured here. Imported
  evidence (e.g. a NotebookLM export) uses `Source workspace:` / `Source
  workspace id:` / `Origin:` instead, since it wasn't authored in-session.
- `Organized:` — present once the ideas move on; the date plus a link to
  every destination (OpenSpec change, doc, or staged topic) they landed in,
  and each link's current lifecycle word (`proposed` / `ratified`). Point
  destination links at the change's *current* location (active vs.
  archived) — a link left pointing at an active path after that change
  archives, or a status word left saying "proposed" after it ratifies, is
  the defect this format exists to catch.
- `Participants:` — optional; who was in the design session.
- `Purpose:` — optional; use in place of a `Problem` section for
  evidence/reference-gathering brainstorms rather than design-exploration
  ones.
- `## Possible feats` — a body section (not a header field) that every
  design-exploration brainstorm seeds at capture: the candidate feats this
  thinking could spawn, one per bullet. These seed the possibles register
  the cross-reference index consolidates (states, pick citations, and
  transition rules per the possibles-register contract,
  [`contracts/schemas/ideation-possibles-register.schema.yaml`](../contracts/schemas/ideation-possibles-register.schema.yaml),
  and the `add-ideation-dashboard` document-lifecycle delta) and the
  realization funnel renders — an unpicked possible is durable backlog,
  not failure. Evidence/reference-gathering brainstorms may omit it.

Every file under `staging/<topic>/` carries the same `Status:` (always
`staged`), `Kind:`, `Summary:`, and `Topics:` fields, in that order, before
`Repository context:`, followed by the staging-specific fields: `Staging ID:`
(`<repo>:staging:<topic-slug>`, durable after the folder moves or is
compressed), `Source:`, and — wherever the doc declares deltas —
`Target capabilities:` naming each target with its delta type
(ADDED / MODIFIED / REMOVED). The topic's primary doc H1 uses the
`# Staged: <Title>` prefix; supporting fragments use plain titles. `Topics:`
complements `Target capabilities:` — free subject keywords versus declared
deltas — so a subject grep spans both stages with one field name.

## Cross-Reference Readiness Index

`ideation/cross-reference.md` is the unified cross-stage **topic cluster and
readiness** surface: it clusters related material by topic across `brainstorm/`,
`staging/`, and archived change material (bootstrapped from the `Topics:` and
`Target capabilities:` fields above), records each cluster's extension-fit
against promoted capabilities, and carries the three-tier Hermes readiness panel
and its minimum-score recommendation gate. It answers "what recurs across stages,
and what is mature enough to propose?" — distinct from the
[Staging Index](staging/INDEX.md), which is the flat inventory of staged files;
the two MUST NOT restate each other (the cross-reference index references
members; the inventory tracks staged files). The `.md` is a generated projection
of the source-of-truth `ideation/cross-reference.yaml` — never hand-edit it.

The normative shape and rules live in
[`contracts/schemas/ideation-cross-reference.schema.yaml`](../contracts/schemas/ideation-cross-reference.schema.yaml)
and the ratified `add-ideation-cross-reference-readiness` `ideation-cross-reference`
requirements (Cross-reference index contract, Extension-fit citation,
Hermes-tier readiness panel, Readiness recommendation gate, Non-mutating
execution bound) — referenced here, not duplicated. Regenerate the seed with
`scripts/bootstrap-ideation-cross-reference.py` and validate with
`scripts/validate-ideation-cross-reference.py`. The current bootstrap seeds
header-derived clusters with every readiness tier unscored until the scoring
worker (codexFactory) realizes; the possibles register folds in later via the
ideation-dashboard flows.

**AI-derived possibles.** A bounded, read-only derive-possibles worker may
propose candidate possibles into the register (`origin: ai-derived` with a
`derivation` worker-run block) for humans to dispose on the gate console — the
possibles-side analog of human-seen cluster intake. The additive kernel shape
lives in
[`contracts/schemas/ideation-possibles-register.schema.yaml`](../contracts/schemas/ideation-possibles-register.schema.yaml)
(`origin` + `derivation`), and the rules live in the `add-possibles-derivation-lane`
`ideation-cross-reference` requirements (Derived possible register entry and
provenance; Orchestration-authoritative identifiers and hashes; One-way
derived-possible disposition on the gate console; Bounded derivation worker,
immutable evidence, and concurrency-protected merge; Derived possibles are a
distinct class until disposed; Non-mutating derivation bound) — referenced here,
not duplicated. The derived register-entry shape and the one-way disposition
lifecycle are enforced by the delegated register validator
`scripts/validate-ideation-dashboard-contracts.py`.

## Contents

Brainstorm (design history; fully organized into staging or an archived
proposal):

- [Doc Health Pipeline](brainstorm/doc-health-pipeline.md) — split into the
  prose-tagging, doc-health-checks, and semantic-health-sweep staged topics;
  its lifecycle/ideation sections were ratified by
  add-document-lifecycle-vocabulary.
- [Domain-To-Neutral Concept Promotion](brainstorm/domain-to-neutral-promotion.md)
  — organized into the promotion process doc, the candidate register, and the
  promotion-refinements staged topic.
- [Workflow Visualization Tooling](brainstorm/workflow-visualization-tooling.md)
  — organized into the workflow-visualization staged topic; kept as license
  evidence.
- [OpenSpec × Speckit Release Flow](brainstorm/openspec-speckit-release-flow.md)
  — organized into the archived
  [add-release-realization-flow](../openspec/changes/archive/2026-07-09-add-release-realization-flow/proposal.md)
  change: release targets, delta-driven feat decomposition, and the archive
  gate binding to merge evidence.
- [Ideation Cross-Reference Readiness Index](brainstorm/ideation-cross-reference-readiness.md)
  — organized 2026-07-12 after all seven open questions were decided, and
  promoted the same day into the add-ideation-cross-reference-readiness
  proposal; kept as design history with the decisions inline.
- [Ideation Area Dashboard](brainstorm/ideation-dashboard.md) — organized
  2026-07-12 into the ideation-dashboard staged topic (six-column docs-first
  realization funnel over a possibles register, pipeline board, doc list,
  and non-mutating workbench; drafts gate artifacts, never executes gates),
  promoted the same day into the add-ideation-dashboard proposal (ratified
  2026-07-12), demoted back to the staged topic 2026-07-13 for continued
  design (D11–D13 added there), and re-proposed later that day; kept as
  design history with the in-session decisions inline.
- [Cluster Combining GUI](brainstorm/cluster-combining-gui.md) — organized
  2026-07-13: the cluster canvas and keyword lens entered the
  add-ideation-dashboard re-proposal as D12/D13; kept as design history
  with the full option space inline.

Brainstorm (active):

- [openxWallet — Wallets, Grants, and Certification](brainstorm/agent-certification-wallets.md)
  — every AI agent gets a DID wallet; certified qualification levels grant
  scoped autonomous authority bound to a quantified agent identity
  (config hash + behavioral battery); change beyond tolerance = no longer
  the certified agent = recertify (2026-07-15).
- [openxVault — Git-Native Record Vault](brainstorm/git-native-record-vault.md) — pull
  PHI out of governed docs into a SOPS/KMS-audited vault plane; sanitized
  analysis plane + commodity bulk plane (de-identified, research-reusable)
  + encrypted vault plane = a basic document-EMR / CPA client vault on the
  custody-tier model (2026-07-15).

- Lens feat requests (2026-07-14, from using the deployed dashboard;
  tagged `feat-request`, expected to stage together as
  `lens-enhancements`):
  [keyword search + ad-hoc keywords](brainstorm/lens-keyword-search-and-adhoc.md) ·
  [brainstorm-session launch from the center ring](brainstorm/lens-brainstorm-session-launch.md) ·
  [ring combination explorer](brainstorm/lens-ring-combination-explorer.md)
- [Keycloak Identity Brokering and the Single Persona](brainstorm/keycloak-identity-brokering.md)
  — self-hosted Keycloak as the family identity broker: bring-your-own
  IdP (GitHub/Google/Entra/any OIDC), federated logins link into one
  durable persona per human with organizations as memberships; dashboard
  auth swap first, gate-console authenticated principals second,
  editor-product login third.
- [Contract Release Identity and Stack-Surface Gaps](brainstorm/contract-release-and-stack-surface.md)
  — three upstream gaps from the codexFactory conformance-gate hardening;
  seeds a future openxFactory proposal.
- [Hermes-Governed Nightly Sweep](brainstorm/hermes-governed-nightly-sweep.md)
  — umbrella for the practice-adoption pipeline: the hand-wired doc-health sweep
  should become an OUTPUT of the three-layer flow (domain suggests, client
  clears, project realizes). Companions below (2026-07-20).
- [Domain Practice Suggestion Generation](brainstorm/domain-practice-suggestion-generation.md)
  — how the Domain Hermes autonomously generates practice-adoption suggestions:
  a practice catalog of adoption profiles, a read-only gap scan, a structured
  suggestion record, and a hard autonomy boundary (the domain may only SUGGEST)
  (2026-07-20).
- [Practice Clearance and Project Realization](brainstorm/practice-clearance-and-project-realization.md)
  — the clearance (client auto-clear envelope + human liaison) and realization
  (project implements through the factory's own PR/review front door) legs of
  the pipeline (2026-07-20).
- [Topic Compilation Tree](brainstorm/topic-compilation-tree.md)
  — link-not-copy supporting docs, and a generated per-topic tree compilation:
  a one-line-summary index opening to per-passage abstracts linked to sources
  (2026-07-19).
- [Three-Layer Hermes Content & Seeding](brainstorm/hermes-layer-content-seeding.md)
  — how each Hermes layer gets its personality/memory/policy *content* (not
  just structural topology): Domain authored once in codexFactory (same for all
  installs), Client scaffolded + tuned by a policy wizard, Project scaffolded
  from a project-type template library; hinges on whether the runtime loads the
  inert `overlay_ref`. Substrate under the practice-pipeline brainstorms
  (`hermes-governed-nightly-sweep.md` + its two companions) (2026-07-21).

Staged topics: see the [Staging Index](staging/INDEX.md), the kept-current
inventory of every topic under `staging/` — update it, not this list, when a
staged file is added, removed, or promoted.

Active proposals promoted from staging:

- [add-governed-derived-model](../openspec/changes/archive/2026-07-23-add-governed-derived-model/proposal.md)
  — promoted 2026-07-23 (same-day capture → decisions → promotion →
  **ratified, realized, archived 2026-07-23**); owns the former
  `governed-derived-model` staged topic (DTN-014) under
  `supporting-docs/`. Neutralizes the pattern three domains instantiate
  independently (Medx Dream Object/Simulation Scenario, Adx
  Persona/Campaign Simulation, Ledgerx Counterparty Health
  Profile/Financial Scenario): five verified invariants, `governed` /
  `calibrated` conformance tiers, six declared dials, a
  `xfactory_derived_model_conformance` declaration, and
  `validate-derived-models.py`. Canonical spec:
  `openspec/specs/governed-derived-model/`. Conformers: Medx
  (`governed`, declaration-only), Adx (`calibrated`, first).
- [add-ideation-dashboard](../openspec/changes/add-ideation-dashboard/proposal.md)
  — re-proposed 2026-07-13 after a design-round demotion (second
  transition); owns the former `ideation-dashboard` staged packet (primary
  doc plus the interactive mockup) under `supporting-docs/` and defines
  the realization funnel snapshot, possibles register, cluster canvas
  (D12), keyword lens with cluster-as-recipe persistence (D13), project
  grouping (D10), drill-down explorer, viewer, gate console, and next-step
  kickoff (D14–D17), per-actor authoring authority, workbench, and nightly
  snapshot lane; web-based v1 served per Option C alongside the
  Hermes-stack surfaces; **re-ratified 2026-07-14**.
- [codexFactory Domain Hermes Content & Roster](brainstorm/codexfactory-domain-hermes-content.md)
  — fills the Software Engineering domain layer: the Plane-1 authority-persona
  roster (seven Leads + a Scrum Coordinator), domain policy/memory/practice-catalog
  storage map, and the Merge-Master-as-operator / cross-layer Gate-Rules-Council
  reframing; keeps the Plane-2 execution workers in the Omnigent install
  (2026-07-21).
- [Hermes-Layer Persona Character Model](brainstorm/hermes-persona-character-model.md)
  — how much personality a Hermes decider should carry (technical disposition →
  full authored character), the dimensions of character, five options (A–E,
  leaning a trait-framework-plus-prose hybrid), and the guardrail that character
  shapes *how* not *whether* a persona decides (2026-07-21).
- [codexFactory Domain Plane-1 Roster — Draft Role Objects](brainstorm/codexfactory-domain-roster-draft.md)
  — the eight drafted domain decider personas (seven Leads + Scrum Coordinator)
  under the Option-E character model: a trait-axis framework (disposition
  domain-locked, voice client-tunable), authored prose for the three flagship
  deciders, and no house style — deliberately distinct personas (2026-07-21).
- [codexFactory Domain Policy — Store the Delta, Not the Textbook](brainstorm/codexfactory-domain-policy-model.md)
  — what belongs in *stored* domain policy/memory vs. what the model improvises:
  pin only the choices that must be consistent, the rules a gate must enforce,
  the fail-closed boundaries, the staked positions, and the accumulated learning;
  leave generic best practice to the model. Includes the decision test and the
  filled codex policy categories (2026-07-21).
- [codexFactory Domain Deliberation](brainstorm/codexfactory-domain-deliberation.md)
  — the roster-adjacent stored content: MoA agent-mix profiles (declaring the
  review-lane ensemble as `panel_synthesis`; Plane 3 profile lives in Hermes,
  execution in Omnigent), escalation routing + stop conditions remapped onto the
  personas, and the two review councils (per-PR merge-readiness vs. cross-layer
  gate-rules) (2026-07-21).
- [codexFactory Domain Memory & Practice Catalog](brainstorm/codexfactory-domain-memory-and-practices.md)
  — the learning-side content: memory boundaries (cross-client domain learning
  vs. never-touch client-private, promoted only through the ratified memory
  gateway) and the practice catalog (adoption profiles over the promoted codex
  capabilities, feeding the suggestion pipeline) (2026-07-21).
- [Client (Company Policy) Layer Scaffold](brainstorm/client-layer-scaffold.md)
  — scaffolds and lists the Client layer: three-tier composition (neutral
  scaffold → domain specialization → per-client wizard tuning), the plane split
  (house-team deciders vs. the 18 steward workers), the object model, file shape,
  and the policy wizard; the key contrast is that client content is per-client
  and wizard-loaded, not authored once (2026-07-21).
- [Client (Company Policy) Plane-1 Roster — Draft House Team](brainstorm/client-layer-roster-draft.md)
  — the ten house-team decider personas, clustered as policy core (Company Policy
  Lead, Change Approvals Authority), a Risk & Assurance bench (Legal & Compliance
  Counsel, Reputation & Brand Steward, Product Liability & Insurance Officer),
  Security, Ops (Integrations Steward, Infrastructure Liaison, Delivery & SLA
  Lead), and Customer & Communications — all sharing a coherent house-style
  voice, itself client-tunable; a **neutral** roster (openxFactory scaffold),
  domain-specialized and client-tuned (2026-07-21).
- [Hermes Legal & Compliance Model](brainstorm/hermes-legal-compliance-model.md)
  — a dedicated Legal & Compliance Counsel (IP/licensing, age-appropriate,
  financial, data-protection, accessibility, export) that enforces human-ratified
  legal constraints, fails closed, and escalates novel legal questions to human
  counsel — never practices law; cross-layer (client authority, domain
  license-scan practice, project audience expectations) (2026-07-21).
- [Client Risk & Assurance Bench](brainstorm/client-risk-and-assurance-model.md)
  — groups legal, a Reputation & Brand Steward (harm to the company's
  reputation), and a Product Liability & Insurance Officer (product-liability
  exposure + Errors & Omissions coverage) into one bench; all enforce stored
  constraints, fail closed, and escalate to a human, convening as a launch/
  release Risk & Assurance review (2026-07-21).
- [Client Layer Content — policy/memory/integration boundaries](brainstorm/client-layer-content-draft.md)
  — fills the three client content files: policy overrides (the client's stored
  delta, stricter-than-domain only), the four per-tenant memory buckets with the
  domain-promotion gate, and integration boundaries (credential references only);
  each a domain default plus a wizard-tuned per-client instance (2026-07-21).
- [Client Policy Wizard](brainstorm/client-policy-wizard.md)
  — the guided elicitation that turns a scaffolded client into a tuned one:
  the bounded question set, the auto-clear-envelope generator (the clearance
  pipeline's input), conservative park-by-default safety, idempotent re-tuning
  with disposition feedback, and the stricter-only guard (2026-07-21).
- [Project/Customer (Subject) Layer Scaffold](brainstorm/project-layer-scaffold.md)
  — the subject-centric layer: its content model (identity, scope, acceptance,
  consent, private memory, journey state), a small Plane-1 roster (Product Owner
  + Project Manager) with the three-layer coordination boundary (domain Scrum
  Coordinator / project PM / client Delivery Lead), provisioning from an
  archetype, and the manual-writer as a Plane-2 worker (2026-07-21).
- [Project-Type Template Library — Draft Archetypes](brainstorm/project-type-template-library-draft.md)
  — six project archetypes (service, library, cli, application, infra-iac, spike)
  a project is provisioned from, each a bundle of default policy, expected
  practices, workflows, and default agents; the stricter-only invariant chains
  domain→client→project-type, and the spike shows safe gate *relaxation* via
  quarantine (2026-07-21).
- [Hermes Knowledge-Base Architecture](brainstorm/hermes-knowledge-base-architecture.md)
  — applies the Cerebras knowledge-base pattern (federate over sources, unified
  evidence rows, structure-before-embed, hybrid retrieval + RRF + age decay,
  planner→executor→synthesizer, primitives-not-answers) inside the ratified
  memory gateway's consent / tenant-isolation / source-authority rails; the
  client layer is the star case (federate over the operating org's real systems
  via the scaffold's source-inventory + memory-steward agents) (2026-07-21).
- [Client Ingestion-Adapter Contract](brainstorm/client-ingestion-adapter-contract.md)
  — the governed connector from a client source system (chat, VCS, tickets, CRM,
  …) to tenant-scoped evidence rows: a `client_source_adapter` manifest composing
  the ratified provider/consent contracts, an `evidence_row` output schema, the
  differential-sync + structure-before-embed + redact pipeline, and the
  non-negotiables (credential-reference-only, tenant isolation, consent-gated,
  source-authority tagged); runs as a read-only Plane-2 worker (2026-07-21).
- [Hermes Retrieval Primitives](brainstorm/hermes-retrieval-primitives-contract.md)
  — the read side: governed low-level primitives (`search`, `search_<source>`,
  `who_knows`, `recall`) returning context-packets, a planner→executor→
  synthesizer pipeline that only *advises* (Hermes decides), the hybrid + RRF +
  age-decay ranking recipe, per-query consent/tenant/ACL/source-authority
  enforcement, and MCP tool exposure (2026-07-21).
- [Subject Recall & Consent Path](brainstorm/subject-recall-and-consent-path.md)
  — the hardest case: recalling a person-subject's (patient's) private memory
  with consent checked per query — a subject-owned consent model (who/what/why/
  how-long/where, default deny), purpose-bound + minimized recall with an
  explained denial list and a subject-visible audit log, immediate revocation/
  erasure, and an audited dual-authorized break-glass exception for life-critical
  domains (2026-07-21).
- [Hermes Layer Seeding Mechanism](brainstorm/hermes-layer-seeding-mechanism.md)
  — the runtime `seed-layer-content` step that makes the drafted content live:
  resolve the pinned overlay_ref → verify digest → compose the overlay stack →
  validate → split into three destinations (enforceable slice → runtime records,
  memory → gateway bindings, persona prose → pinned reference); deterministic,
  digest-pinned, idempotent, re-seeds on re-pin (client-consented), fails closed
  to a safe structural-only layer (2026-07-21).
- [Tech-Stack Benches as Governed Worker Toolchains](brainstorm/tech-stack-benches.md)
  — adopt the operator's per-stack bench containers as governed worker
  execution environments: neutral bench-manifest contract, digest-pinned
  `toolchain_bindings` in domain overlays, per-job bench selection, heartbeat
  bench inventory, and Intune-deployed worker-host-agent pre-pull; first
  bench-enabled host is the idle Omni-001 Cloud PC (2026-07-23).
- [Omnigent Lane Activation Path](brainstorm/omnigent-lane-activation-path.md)
  — the sequenced path from today's govern/record plane to a Hermes-managed
  omnigent lane that autonomously codes: P0 runtime (live) → P1 seed+enforce
  content → P2 governed job lifecycle → P3 omnigent run loop → P4 governed close
  → P5 self-host; the ordering answer is that Hermes layer *content* (seeded +
  enforceable) gates a *managed* lane while the execution machinery builds in
  parallel and converges (2026-07-21).

- [qualify-avatar-brokered-call-feasibility](../openspec/changes/qualify-avatar-brokered-call-feasibility/proposal.md)
  — approved split owning the isolated F0 harness and empirical evidence; still
  active. Its sibling avatar changes promoted from the same staged packet — the
  AVC kernel (`define-avatar-client-contract-kernel`, realized `contract-v1.7`),
  the reference runtime (`implement-avatar-reference-runtime`), and the UI standard
  (`align-avatar-first-ui-standard`, realized `contract-v1.8`) — were realized and
  archived 2026-07-13 (see the root README's Archived changes).
- [add-cross-factory-ideation-routing](../openspec/changes/add-cross-factory-ideation-routing/proposal.md)
  — owns the former `ideation-routing` staged packet under
  `supporting-docs/` and proposes capture-first claim routing, destination
  acceptance, deterministic routing validation, and a bounded organizer.
- [add-document-cataloging](../openspec/changes/archive/2026-07-14-add-document-cataloging/proposal.md)
  — user-approved split from the former umbrella proposal; owns external
  controlled tagging, immutable catalog snapshots, deterministic catalog
  validation, and the bounded document cataloger; realized as
  `contract-v1.11` and **archived 2026-07-14**.
- [add-proposal-origin-contract](../openspec/changes/add-proposal-origin-contract/proposal.md)
  — owns the former `proposal-origin-contract` primary doc under
  `supporting-docs/` and proposes the mandatory staged/ad-hoc origin
  declaration, gate rejections, archive retention, migration, and the
  proposal-origin doc-health family; the FDA SaMD rationale deliberately
  remains staged.
- [add-ideation-cross-reference-readiness](../openspec/changes/add-ideation-cross-reference-readiness/proposal.md)
  — owns the former `ideation-cross-reference-readiness` staged packet under
  `supporting-docs/` and proposes the unified cross-stage topic index,
  three-tier Hermes readiness panel, minimum-score recommendation gate, and
  nightly readiness lane.
- [implement-avatar-client-lab](../openspec/changes/implement-avatar-client-lab/proposal.md)
  — exit of the `avatar-client-lab` staged topic (six decisions locked
  2026-07-13, promoted 2026-07-14); owns the four staged fragments under
  `supporting-docs/` and realizes the offline, deterministic Flutter avatar
  client UI lab against `contract-v1.7`/`contract-v1.8`.
- [add-client-infrastructure-liaison](../openspec/changes/archive/2026-07-17-add-client-infrastructure-liaison/proposal.md)
  — exit of the `client-infrastructure-liaison` staged topic (promoted
  2026-07-16); owns the six staged fragments (bundled as
  `supporting-docs.tar.gz` at archive) and adds the neutral Client
  Infrastructure Liaison coordination profile plus the
  `client_infrastructure_request` contract family; realized as
  `contract-v1.13` and **archived 2026-07-17**.

Proposal source and completed design history are retained with their active or
archived OpenSpec changes under `supporting-docs/` or
`supporting-docs.tar.gz`, with readable manifests.
