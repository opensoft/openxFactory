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

### Additional three-tier packet overviews

These overviews organize the packet material added by the brainstorm-packet
migration into reusable atomic, synthesis, and whole-system tiers. They remain
non-normative and may cite staged or proposed artifacts as read-only context.
The current Recurrence Crystallization packet is retained in the active list
below with its lifecycle notes.

- [Ontology-Grounded Execution](brainstorm/ontology-overview.md) — semantic
  context compilation, routing, caching, and maintenance proposals.
- [Domain Ontology Lifecycle](brainstorm/domain-ontology-overview.md) —
  governed generation, publication, drift, and renewal.
- [Omnigent Micro-Agents](brainstorm/omnigent-micro-agent-overview.md) —
  bounded task contracts, routing, composition, evaluation, and economics.
- [Client Hermes Layer](brainstorm/client-overview.md) — tenant authority,
  policy tuning, assurance, content, and source ingestion.
- [codexFactory Domain Hermes](brainstorm/codexfactory-domain-overview.md) —
  software-domain personas, deliberation, policy, memory, and practices.
- [Three-Layer Hermes Runtime](brainstorm/hermes-overview.md) — deterministic
  layer seeding, authority, personas, legal boundaries, retrieval, and
  non-mutating learning.
- [Hermes Memory and Retrieval](brainstorm/memory-retrieval-overview.md)
  — source authority, per-query consent, minimized context, and recall audit.
- [Governed Practice Adoption](brainstorm/practice-adoption-overview.md) —
  domain suggestion, client clearance, project realization, outcomes, and
  accounting.
- [Project and Subject Hermes](brainstorm/project-overview.md) — template
  provisioning, subject identity, scope, consent, acceptance, and catalog
  boundaries.
- [Dashboard Integrated Document Workbench](brainstorm/dashboard-workbench-overview.md)
  — shared Outline/Document editing, subject-aware chat, model selection, and
  human/AI draft turns.
- [Identity and Custody](brainstorm/identity-custody-overview.md) — brokered
  people, qualified agents, grants, vault tiers, and explainable access.
- [Governed Worker Execution](brainstorm/worker-execution-overview.md) —
  enrolled hosts, digest-pinned benches, bounded jobs, evidence, and external
  enforcement.
- [Medical Domain Hermes and Omnigent](brainstorm/medical-domain-overview.md)
  — clinical-domain authority, bounded workers, safety, and clinician handoff.
- [Contract Release and Document Lifecycle](brainstorm/release-lifecycle-overview.md)
  — immutable source provenance, explicit promotion, signed releases, and
  stack adoption.
- [Avatar Live Voice](brainstorm/avatar-live-voice-overview.md) — visible
  client states, privacy, brokered-call evidence, qualification, and hardening
  boundaries.

- [doxBench Overview](brainstorm/doxbench-overview.md) — entry point for the
  three-tier doxBench packet: six atomic documents describe surface/scope,
  dual buffers, grounded chat, typed proposal review, governed persistence,
  and the provider boundary; two syntheses relate the human/AI authoring loop
  and governed runtime. The packet is non-normative design exploration; the
  active `add-workbench-integrated-editor-chat` change owns proposed
  requirements and implementation gates (2026-07-28).
- [Agent-Assisted App Testing Overview](brainstorm/agent-assisted-app-testing-overview.md)
  — anchors a twenty-document packet (sixteen atomic docs, three syntheses, and
  one overview) for turning browser annotations, Hermes UI audits, and
  regressions into Project Hermes-managed specialist design work, layered
  functional/visual evidence, repo-owned approved UI snapshots, deterministic
  diff review, experience-council admission, bounded agent-only merge handoff,
  human/professional exception gates, a v1 SDLC session protocol, and a pinned
  Chromium/Loki render manifest, with a platform-neutral seam for a later
  Flutter adapter (2026-08-02).
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

- [add-subject-establishment](../openspec/changes/add-subject-establishment/proposal.md)
  — raised 2026-08-28 as the FULL promotion of the `subject-establishment`
  staged topic, whose row and detail section leave
  [staging/INDEX.md](staging/INDEX.md) with this pointer. The topic took its
  OWN declared exit path: both of its stated gates had cleared — the
  LedgerxFactory first instantiation reached proposal and archived on
  2026-08-04, and codexFactory new-project was decided as the second consumer
  on 2026-07-28 — and Brett's ruling of 2026-08-28, verbatim "Progress both",
  is the instruction that raised the exit. It ADDS the NEW neutral
  `subject-establishment` capability in eleven requirements: the ordered
  pipeline over two artifact kinds (neutral subject design, platform
  realization), provenance-graded facts, a vendor-free design and a
  one-system-per-realization overlay, the reference-archetype lifecycle whose
  harvest never invalidates a subject retroactively, conformance tiering
  expressed as `roles-authority-model`'s ratified route/park/interrupt ladder,
  the cross-factory apply seam riding `deployment-handoff-boundary`'s
  client-infrastructure-request crossing rather than a new record kind,
  verify-by-read-back with pre-authorization probes refused by name, the two
  authority classes that never share a grant, the audit-lift mirror, and layer
  ownership without a storage rule. Registered as DTN-017, whose register row
  moves `staged` → `openspec` in the same commit. Owns the single staged
  fragment (`subject-establishment.md`) under `supporting-docs/`.
  `Status: ratified` with `code_surface: none` and `target_release: none` —
  but it does NOT archive on landing: six orchestrator decisions are flagged
  for veto and six open questions carry recommendations and no decisions, and
  the archive gate is merge plus green PLUS that ruling round. The two artifact
  kinds' SCHEMAS are deliberately absent and named as the successor
  `add-subject-establishment-contracts` (OD-1, against a live counter-precedent
  from the same day).
- [qualify-avatar-live-voice](../openspec/changes/qualify-avatar-live-voice/proposal.md)
  — raised 2026-08-26 as the FULL promotion of the
  `qualify-avatar-live-voice` staged topic, whose row and detail section
  leave [staging/INDEX.md](staging/INDEX.md) with this pointer. The topic had
  declared itself not ready to propose behind five blocking forks; Brett Heap
  ruled all five and all three latent decisions in session on 2026-08-26, and
  this change is the Exit those rulings authorized. It ADDS the neutral
  `avatar-live-voice` capability — the AVC-09 adapter descriptor and AVC-10
  latency sample lifted from reserved to defined using their RESERVED SHAPES
  AS-IS, the internal-live activation gate as the kernel's four-element ring
  with the eight-condition GPT-Live-1 list demoted to its evidence-producing
  checklist, a neutral relative-regression latency SLO at the ratified
  >15% relative OR >150 ms absolute threshold, broker-held custody with two
  independent fail-closed spend layers, synthetic evaluation audio with a
  strictly ephemeral single-model consented canary, the written
  revoke-versus-block rollback policy the kernel required and never had, and
  the deferrals named rather than implied. It MODIFIES three
  `avatar-client-runtime` requirements plus the two repository-boundary
  requirements, because latent decision 1 makes this the change that extracts
  `openAvatar` from codexFactory `apps/avatar-client-lab` — a job
  canon required and no change had ever owned. Owns both former staged
  fragments (`qualify-avatar-live-voice.md`, `fork-decision-memo.md`) under
  `supporting-docs/`; design history stays in the
  [avatar-live-voice brainstorms](brainstorm/avatar-live-voice-overview.md).
  `Status: draft` — the rulings are locked staging decisions, not a
  ratification, and with `code_surface: openxFactory, openAvatar`
  and `target_release: implementation_pending` it archives only on merged
  plus green internal-live realization evidence. Aggregation admission of the
  client repository, the GPT-Live-1 default swap, and the
  `avatar-pilot-hardening` deferrals are explicitly NOT in it.
- [add-identity-brokering](../openspec/changes/add-identity-brokering/proposal.md)
  — raised, RATIFIED and REALIZED 2026-08-21 (registered at
  `contract-v1.37`) as the FULL promotion of the `identity-brokering-plane`
  staged topic, whose row and detail section leave
  [staging/INDEX.md](staging/INDEX.md) with this pointer: exit 1 of the
  topic's three exits, the neutral `identity-brokering` capability — one
  persona per human within a broker INSTANCE, organizations realizing company
  boundaries on the persona, the broker asserting identity and membership only
  (never mirroring the tenancy graph), explicit linking or admin-approved
  merge with no third mode, workloads-are-not-personas, broker credentials as
  `credential-contracts` records, and isolation escalating by broker instance
  with the contract SILENT on instance count. Owns the former
  `identity-brokering-plane.md` fragment under `supporting-docs/`; design
  history stays in the 2026-07-14
  [keycloak-identity-brokering](brainstorm/keycloak-identity-brokering.md)
  brainstorm. Sibling of `add-trust-anchor` from the same 2026-08-21 session —
  rulings R1 (install repos) and R7 (the ownership split) were made ONCE for
  both topics — and its repo admission landed as an ADDED per-repo
  `repo-boundary-governance` requirement rather than the shared MODIFIED
  enumeration, so the two siblings cannot collide on one requirement at
  archive time. Exits 2 (`keycloak-administration` in OpsxFactory) and 3 (the
  `Keycloak-Install` creation) remain, tracked as named successors on
  the change.
- [add-trust-anchor](../openspec/changes/add-trust-anchor/proposal.md)
  — raised, RATIFIED and REALIZED 2026-08-21 (registered at
  `contract-v1.37`) as the FULL promotion of the `pki-trust-anchor-plane`
  staged topic, whose row and detail section leave
  [staging/INDEX.md](staging/INDEX.md) with this pointer: exit 1 of three, the
  neutral `trust-anchor` capability — anchors as governed records with
  certificates trusted only derivatively, issuance only under recorded
  authority, declared chain custody DERIVING what a certificate evidences
  (composing with `openxwallet` at run time rather than restating it),
  renewal-as-rebind over dependents enumerated in advance, revocation
  propagating to the authority the certificate supported, CA material as a
  `credential-contracts` record, and the declared-degraded-obligation rule —
  product-agnostic because two realizations are real (live Intune Cloud PKI
  canary; OpenXPKI planned for the Opensoft production core). Owns the former
  `pki-trust-anchor-plane.md` fragment under `supporting-docs/`. **The one
  deliberate divergence from the topic**, recorded here so a reader is not
  left to infer it: the topic's R1 called for the `repo-boundary-governance`
  install-repository enumeration to be MODIFIED, and the change instead ADDS a
  per-repo requirement for the `OpenXPKI-Install` boundary (design
  D8) — the collision avoidance the sibling `add-identity-brokering` mirrors.
  Topic-folder and change ids differ deliberately (`pki-trust-anchor-plane`
  vs `add-trust-anchor`), and R1/R7 were ruled once across this topic and
  `identity-brokering-plane`. Exits 2 (`pki-administration` in OpsxFactory,
  plus the time-critical `add-openxpki-qa-image-pipeline` Impact amendment)
  and 3 (the `OpenXPKI-Install` creation, moving the QA deployment
  topology in per R2 while image custody stays in `opensoft/Opensoft-Tenant`)
  remain, tracked as named successors on the change.
- [add-worker-enrollment-broker](../openspec/changes/add-worker-enrollment-broker/proposal.md)
  — raised, RATIFIED and phase-1 REALIZED 2026-07-26 (the contract family
  registered at `contract-v1.29`) as the FULL promotion of the
  `worker-enrollment-broker` staged topic, whose row and detail section leave
  [staging/INDEX.md](staging/INDEX.md) with this pointer. It ADDS the neutral
  `worker-enrollment` capability — one enrollment point serving two estates
  (Intune fleet hosts authenticating per-host, volunteer workstations as the
  engineer under device code), renewable LEASES in place of permanent
  registrations, minting authority held by the broker alone (registration and
  remove tokens both, so no administration-tier App key ever reaches a host),
  a minimum-app-version floor enforced fail-closed at renewal, estate-split
  runner packaging (fleet hard-pinned by manifest rollout, temp self-updating),
  temp segregation behind a first-class trust tier, revocation as refusal, and
  audit records whose token values are unrepresentable by shape. Seven schemas
  shipped with 11 valid and 27 intended-invalid examples and the canonical
  `scripts/validate-worker-enrollment.py`. The topic's ten open questions were
  carried into `design.md` as decisions D1–D10 and ALL TEN ADOPTED AS DECIDED
  by Brett's approval on 2026-07-26 — D1 settled the broker's home (a new
  Opsx-owned repo, container app on the existing platform subscription,
  deliberately NOT the QA AKS cluster), so none of the ten is a live gate. Owns
  the former `worker-enrollment-broker.md` fragment under `supporting-docs/`.
  The heartbeat/readiness lease-state projection is deliberately excluded and
  left to a coordinated three-places change. The three realizations are named
  successors rather than this change's surface, and that is where the remaining
  work sits: the broker service itself is MERGED (its PRs #1 2026-07-27 and #2
  2026-07-28), while Omnigent-Install **PR #40** (the enrollment-broker client,
  leases, fail-closed floor) and OpsxFactory
  `add-worker-enrollment-broker-service` **tasks 8.1/8.2** (Brett's
  hosting-target and deployment-credential gates) are open.
- [add-consent-instrument](../openspec/changes/archive/2026-08-06-add-consent-instrument/proposal.md)
  — raised 2026-08-03 (ratified same day; archived 2026-08-06 at contract-v1.30) as the full promotion of the
  `consent-instrument-contract` staged topic (both docs moved to
  `supporting-docs/`): the neutral consent-instrument capability, DTN-016,
  authored against the nine 2026-07-31 rulings with two conformant
  instances (Ledgerx engagement consent, Medx patient consent).
- [add-capability-steward](../openspec/changes/archive/2026-07-30-add-capability-steward/proposal.md)
  — raised and RATIFIED 2026-07-29, realized (`contract-v1.21`), and
  **archived 2026-07-30** as exit 3 (final) of the `recurrence-crystallization`
  staged topic (partial promotion — the dials register remains staged as
  the topic's living remainder); owns the former `steward-contracts.md`
  fragment under `supporting-docs/` and proposes the
  crystallized-capability registry (proof-gated status spine, artifacts
  pinned while authority is live-read), the dispatch junction (fences,
  effect-class admission, fallback taxonomy, audit-shape parity), and
  capability-health (proof ladder, mandatory sentinels, drift responses,
  sentinel-anchored accounting, renewal write-backs).
- [add-crystallizer-contracts](../openspec/changes/archive/2026-07-29-add-crystallizer-contracts/proposal.md)
  — raised, RATIFIED, realized (`contract-v1.20`), and **archived
  2026-07-29** as exit 2 of the `recurrence-crystallization` staged
  topic (partial promotion — steward and dials fragments remain staged for
  exit 3); owns the former `crystallizer-contracts.md` and
  `authority-and-consent.md` fragments under `supporting-docs/` and
  proposes the crystallization decision (the only path from candidate to
  spend), the episode-mined build contracts (corpus, fence, effect class,
  provenance), the T1/T2/T3 consent tiers with the approval braid, and the
  crystallized-executor + rung-ceiling additions to the Omnigent overlay
  under strict authority conservation.
- [add-pattern-ledger](../openspec/changes/archive/2026-07-29-add-pattern-ledger/proposal.md)
  — raised, RATIFIED, realized (`contract-v1.19`), and **archived
  2026-07-29** as exit 1 of the `recurrence-crystallization` staged
  topic (partial promotion — the topic keeps its crystallizer, authority,
  steward, and dials fragments for exits 2 and 3); owns the former
  `pattern-ledger-contracts.md` fragment under `supporting-docs/` and
  proposes the five sensing record kinds (episode, outcome-label,
  recurrence-family, recurrence-forecast, crystallization-candidate), the
  derived-projection posture, consent-scope gating, scored forecasts, and
  the candidate autonomy boundary (nominate, never spend).
- [add-deployment-handoff-boundary](../openspec/changes/archive/2026-07-30-add-deployment-handoff-boundary/proposal.md)
  — fully promoted 2026-07-28, RATIFIED 2026-07-29, and archived 2026-07-30:
  owns the former
  `deployment-handoff-boundary`
  staged topic under `supporting-docs/`. The managed-subject test routes
  deployment execution — authority follows management of the target surface,
  never the environment tier — binding workers, CI, and human engineers
  alike; credential non-possession is the primary enforcement, correlation
  stamping makes out-of-band change a first-class finding, cadenced
  publication rides standing maintenance requests, and release-realization
  evidence correlates to the completed handoff request. OpsxFactory (QA
  profile, grant-issuance registry lookup, correlation audit, ACR scope map)
  and codexFactory (release exit emits the request draft) are named
  successor realization changes; break-glass custody stays with the
  `client-credential-escrow-registry` topic.
- [add-omnigent-domain-overlay](../openspec/changes/archive/2026-07-24-add-omnigent-domain-overlay/proposal.md)
  — fully promoted 2026-07-23: owns the former `omnigent-core-domain-split`
  staged topic under `supporting-docs/`. Both archive-gate halves proven
  the same day — the live coding-patch-worker binding renders
  byte-equivalently from the codexFactory overlay
  (`author-execution-lane-profile-in-overlay` + omnigent-install
  `render-effective-profiles`, ratified + archived 2026-07-23), and the
  MedxFactory second-domain fixture renders as a params-only delta with
  zero core edits. The change itself stays active until its remaining task
  (hermes-install readiness port) and bundle registration land.
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
- [add-ideation-dashboard](../openspec/changes/archive/2026-07-29-add-ideation-dashboard/proposal.md)
  — re-proposed 2026-07-13 after a design-round demotion (second
  transition); owns the former `ideation-dashboard` staged packet (primary
  doc plus the interactive mockup) under `supporting-docs/` and defines
  the realization funnel snapshot, possibles register, cluster canvas
  (D12), keyword lens with cluster-as-recipe persistence (D13), project
  grouping (D10), drill-down explorer, viewer, gate console, and next-step
  kickoff (D14–D17), per-actor authoring authority, workbench, and nightly
  snapshot lane; web-based v1 served per Option C alongside the
  Hermes-stack surfaces; **re-ratified 2026-07-14, realized, and ARCHIVED
  2026-07-29** — the `ideation-dashboard` capability spec is promoted (15
  requirements, plus the created `ideation-cross-reference` spec and
  doc-health/document-lifecycle additions) and the supporting bundle
  manifest was hash-refreshed at the archive preflight.
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
- [Tenant Project Catalog and Engineer Workstation Projection](brainstorm/tenant-project-catalog-and-workstation-cache.md)
  — separates the company runtime's authoritative project/repository catalog
  and principal assignments from the engineer workstation's tenant-scoped
  cache and local preferences; defines Company Projects, My Projects,
  native Windows/WSL state locations, and the single-project request boundary
  (2026-07-27).
- [Ontology and Omnigent Micro-Agent Exploration Map](brainstorm/ontology-and-micro-agent-exploration-map.md)
  — anchors a twelve-document collection covering the ontology and micro-agent
  foundations, ontology generation/maintenance/context compilation, bounded
  Omnigent task/routing/evaluation contracts, and the combined semantic
  routing, caching, and ontology-maintenance fleet ideas (2026-07-28).
- [Governed Recursive Inference Overview](brainstorm/governed-recursive-inference-overview.md)
  — anchors a sixteen-document packet (eleven atomic docs + four syntheses)
  adapting Recursive Language Models to xFactory as a bounded Omnigent
  inference strategy: authorized context capsules, typed sandboxed context
  computation, subordinate task families with monotone authority, depth/cost
  limits, coverage and trajectory evidence, strategy routing, domain pilots,
  and council-ready assurance packets (2026-07-30).
- [Hermes Recursive Subject Establishment Overview](brainstorm/hermes-recursive-subject-establishment-overview.md)
  — anchors an eighteen-document companion packet (thirteen atomic docs + four
  syntheses) placing bounded recursive inference in Subject Hermes for durable
  company, patient, project, or estate establishment: recursive evidence
  frontiers, heterogeneous evidence manifests, governed acquisition
  obligations, modality and specialist routing, relationship-scope and lineage
  controls, purpose-bound derived subject models, qualified readiness, and
  Ledgerx/Medx proof profiles (2026-07-30).
- [Polyglot Graph Memory Overview](brainstorm/polyglot-graph-memory-overview.md)
  — anchors a nine-document packet (six atomic docs + two syntheses) on using
  purpose-specific graph providers across doxBench, the three Hermes layers,
  DomainxFactories, and Omnigent while standardizing identity, provenance,
  bounded context, routing roles, derived-projection authority, disagreement,
  promotion, and migration through the Memory Gateway (2026-07-30).
- [Recurrence Crystallization Overview](brainstorm/crystallization-overview.md)
  — anchors a nineteen-document packet (fifteen atomic docs + three arc
  syntheses: Pattern Ledger, Crystallizer, Capability Steward) on turning
  repeatedly-AI-solved task families into governed cheaper paths: an episode
  ledger over existing audit/metering, recurrence + stability forecasting, a
  budget-consented build decision on a seven-rung automation ladder,
  episode-mined micro-specs with acceptance corpora and scope fences,
  codexFactory-built capabilities under authority conservation, and
  fence-guarded dispatch with sentinel sampling so learning, drift detection,
  and savings claims stay honest (2026-07-28). Organized 2026-07-29 into the
  [recurrence-crystallization staged topic](staging/recurrence-crystallization/recurrence-crystallization.md)
  with decisions D1–D11 and verifications V1–V2 locked; the
  [cross-tenant fragment](brainstorm/crystallization-cross-tenant.md) stays
  active brainstorm for a later wave.
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

- [qualify-avatar-brokered-call-feasibility](../openspec/changes/archive/2026-08-09-qualify-avatar-brokered-call-feasibility/proposal.md)
  — approved split owning the isolated F0 harness and empirical evidence;
  realized and archived 2026-08-09. Its sibling avatar changes promoted from
  the same staged packet — the
  AVC kernel (`define-avatar-client-contract-kernel`, realized `contract-v1.7`),
  the reference runtime (`implement-avatar-reference-runtime`), and the UI standard
  (`align-avatar-first-ui-standard`, realized `contract-v1.8`) — were realized and
  archived 2026-07-13 (see the root README's Archived changes).
- [add-cross-factory-ideation-routing](../openspec/changes/archive/2026-08-06-add-cross-factory-ideation-routing/proposal.md)
  — realized and archived 2026-08-06; owns the former `ideation-routing` staged packet under
  `supporting-docs/` and proposes capture-first claim routing, destination
  acceptance, deterministic routing validation, and a bounded organizer.
- [add-document-cataloging](../openspec/changes/archive/2026-07-14-add-document-cataloging/proposal.md)
  — user-approved split from the former umbrella proposal; owns external
  controlled tagging, immutable catalog snapshots, deterministic catalog
  validation, and the bounded document cataloger; realized as
  `contract-v1.11` and **archived 2026-07-14**.
- [add-proposal-origin-contract](../openspec/changes/archive/2026-08-06-add-proposal-origin-contract/proposal.md)
  — owns the former `proposal-origin-contract` primary doc under
  `supporting-docs/` and proposes the mandatory staged/ad-hoc origin
  declaration, gate rejections, archive retention, migration, and the
  proposal-origin doc-health family; the FDA SaMD rationale deliberately
  remains staged.
- [add-ideation-cross-reference-readiness](../openspec/changes/archive/2026-08-04-add-ideation-cross-reference-readiness/proposal.md)
  — realized and archived 2026-08-04; owns the former
  `ideation-cross-reference-readiness` staged packet under
  `supporting-docs/` and proposes the unified cross-stage topic index,
  three-tier Hermes readiness panel, minimum-score recommendation gate, and
  nightly readiness lane.
- [implement-avatar-client-lab](../openspec/changes/archive/2026-08-04-implement-avatar-client-lab/proposal.md)
  — exit of the `avatar-client-lab` staged topic (six decisions locked
  2026-07-13, promoted 2026-07-14, realized and archived 2026-08-04); owns the four staged fragments under
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
