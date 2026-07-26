# openxFactory

`openxFactory` documents the open reference stack and domain-neutral xFactory
layer used by Opensoft domain factory projects.

Use these terms precisely:

- `xFactory` is the top-level product family and aggregation repository.
- `openxFactory` is the open reference stack and canonical contract source.
- The `xFactory layer` is the domain-neutral stack composition and workflow
  governance layer inside `openxFactory` and every DomainxFactory. It defines
  which stack parts are required for a domain and how work moves through gates,
  routing, traceability, source authority, memory promotion, credentials, and
  audit. It also governs memory and knowledge provider bindings, migrations,
  metering, and bounded context packets for Subject Hermes and Domain
  Omnigent.
- A `DomainxFactory` is an instantiated domain stack such as `MedxFactory`,
  `LedgerxFactory`, `OpsxFactory`, `AdxFactory`, or `codexFactory`.

See [Terminology And Repository Topology](docs/terminology-and-repo-topology.md)
for the stack, layer, and submodule ownership model.

It defines reusable contracts for:

- workflow gates
- state transitions
- traceability
- routing
- approval handoffs
- review records
- audit expectations
- authority boundaries between governance, workflow, execution, and enforcement layers

## Core Boundary

`openxFactory` is domain-neutral, but it is a stack, not only a layer.

```text
Hermes
  owns intent, policy, memory, approval, and governance history.

xFactory layer
  owns stack composition, contracts, gates, traceability, routing, state
  transitions, memory/knowledge provider governance, and audit.

Domain factory repos
  own domain-specific execution behavior.

Domain Omnigent layers
  run bounded domain agents under Hermes policy and xFactory layer gates,
  including expert memory and knowledge DB access through xFactory context
  packets.

External enforcement systems
  enforce final state where applicable.
```

Domain examples:

```text
codexFactory
  uses Omnigent to run coding and engineering agents.

MedxFactory
  uses Omnigent to run clinical and medical reasoning agents.

OpsxFactory
  uses Omnigent to run sysops, devops, and IT administration agents.
```

## Documentation

Core domain-neutral docs:

- [Architecture](docs/architecture.md)
- [Terminology And Repository Topology](docs/terminology-and-repo-topology.md)
- [Party Ladder](docs/party-ladder.md) (author/operator → tenant → subject → third parties; frozen-word reading rules)
- [xFactory Domain Factory Model](docs/xfactory-domain-factory-model.md)
- [Governed Derived Model](docs/governed-derived-model.md)
- [xFactory Taxonomy Model](docs/factory-taxonomy-model.md)
- [Domain Factory Implementation Checklist](docs/domain-factory-implementation-checklist.md)
- [Domain Stack Pin Implementation Plan](docs/domain-stack-pin-implementation-plan.md)
- [xFactory Domain Factory Starter Pack](docs/domain-factory-starter-pack.md)
- [Domain Instantiation Pre-Run Questionnaire](docs/domain-instantiation-pre-run-questionnaire.md)
- [Domain Instantiation Setup Runbook](docs/domain-instantiation-setup-runbook.md)
- [openxFactory Installation Spine And Domain Overlays](docs/openxfactory-installation-spine.md)
- [xFactory Intake And Installer Plan](docs/intake-and-installer-plan.md)
- [TUI Spec Questionnaire](docs/tui-spec-questionnaire.md)
- [Self-Hosted Runtime Binding Plan](docs/self-hosted-runtime-binding-plan.md)
- [Runtime Services Plan](docs/runtime-services-plan.md)
- [Deploy Artifacts Plan](docs/deploy-artifacts-plan.md)
- [Intake Template Catalog](templates/intake/README.md)
- [Intake Subtype Install Readiness Report](docs/intake-subtype-install-readiness-report.md)
- [Intake Subtype Install Runbook](docs/intake-subtype-install-runbook.md)
- [Intake Subtype Second-Pass Gap Report](docs/intake-subtype-second-pass-gap-report.md)
- [Domain Pre-Run Simulation Report](docs/domain-pre-run-simulation-report.md)
- [Domain Repo Review Improvements](docs/domain-repo-review-improvements.md)
- [Document Lifecycle](docs/document-lifecycle.md)
- [Release Realization Flow](docs/release-realization-flow.md)
- [Doc-Health Contract](docs/doc-health.md)
- [Document Catalog Adoption Guide](docs/document-catalog-adoption.md)
- [Cross-Factory Ideation Routing Adoption Guide](docs/ideation-routing-adoption.md)
- [Domain-To-Neutral Promotion Process](docs/domain-to-neutral-promotion-process.md)
- [Domain Neutralization Candidate Register](docs/domain-neutralization-candidate-register.md)
- [Installation Template Catalog](templates/installation/README.md)
- [xFactory Credential Access Model](docs/credential-access-model.md)
- [Standard Operating Procedures](docs/sops/README.md)
- [OpenAI Realtime F0 Lab Credential SOP](docs/sops/openai-realtime-f0-lab-credential.md)
- [Avatar-First UI Standard](docs/avatar-first-ui-standard.md)
  ([profile examples](examples/avatar-first-ui/README.md) ·
  [deterministic fixtures](examples/avatar-first-ui/fixtures/README.md))
- [Avatar-Client (AVC) Contract Kernel](contracts/avatar-client/README.md)
  (neutral session/consent/revocation contract family; realized at
  `contract-v1.7` with a fail-closed F0 publication gate)
- [Workflow Visualization Standard](docs/workflow-visualization-standard.md)
- [Subject Hermes Memory Model](docs/customer-hermes-memory-model.md)
- [Customer Memory Fill And Maintenance Taxonomy](docs/customer-memory-fill-maintenance-taxonomy.md)
- [xFactory Memory Gateway Architecture](docs/customer-memory-gateway-architecture.md)
- [xFactory Memory Gateway Contracts](contracts/memory-gateway/README.md)
- [Omnigent Contract Family](contracts/omnigent/README.md)
  (domain-overlay payload + install manifest; realized by
  `add-omnigent-domain-overlay`, pending bundle registration)
- [Worker Enrollment Contract Family](contracts/worker-enrollment/README.md)
  (one enrollment point / two authentication modes, renewable LEASES instead of
  registrations, fail-closed minimum-app-version floor, temp-estate segregation
  by trust tier, the brokered remove-token issuance shape, and audit records no
  token value can enter; realized by
  `add-worker-enrollment-broker`, pending bundle registration)
- [Tenant Hermes Product And Service Scaffold](docs/client-hermes-product-service-scaffold.md)
- [Client Infrastructure Liaison](docs/client-infrastructure-liaison.md)
- [Client Installation Discovery And Workflow Migration](docs/client-installation-discovery-and-migration.md)
- [Workflow Visualization Tooling Exploration](ideation/brainstorm/workflow-visualization-tooling.md)
- [Hermes Mixture Of Agents For xFactory](docs/hermes-mixture-of-agents-for-xfactory.md)
- [NotebookLM Source Workspaces](docs/notebooklm-source-workspaces.md)
- [Lifecycle Notebook Projection](docs/lifecycle-notebook-projection.md)
- [Ideation Work Area](ideation/README.md) (ratified convention; see
  [Document Lifecycle](docs/document-lifecycle.md))
- [Workflow Contract](docs/workflow-contract.md)
- [Traceability Model](docs/traceability-model.md)
- [Roles and Authority](docs/roles-and-authority.md)
- [Repository Boundary Governance](openspec/specs/repo-boundary-governance/spec.md)
- [Shared Contract Ownership](openspec/specs/shared-contract-ownership/spec.md)

Engineering-domain implementation docs now belong in `opensoft/codexFactory`.

Medical-domain implementation docs belong in `opensoft/MedxFactory`.

IT operations-domain implementation docs now belong in `opensoft/OpsxFactory`.

## Domain Implementations

- `opensoft/codexFactory` — software, code, repo, and engineering xFactory domain stack.
- `opensoft/MedxFactory` — medical xFactory domain stack for clinical agents and medical workflows.
- `opensoft/OpsxFactory` — IT operations, sysops, devops, identity, infrastructure, and tenant administration xFactory domain stack.
- `opensoft/LedgerxFactory` — accounting, finance, and ledger xFactory domain stack.
- `opensoft/AdxFactory` — marketing and advertising xFactory domain stack.

## Conformance

Every DomainxFactory must validate against the canonical contract:

- Stack shape: [xfactory-domain-stack schema](contracts/schemas/xfactory-domain-stack.schema.yaml)
  — Hermes layers are declared as `hermes.layers` with role keys
  `customer|client|domain`: frozen v1 machine spellings for the canonical
  **Subject / Tenant / Domain** layers (served subject / tenant-operator
  organization / reusable expert domain; mapping published at
  [contracts/policies/layer-vocabulary.yaml](contracts/policies/layer-vocabulary.yaml)).
- Validator: `scripts/validate-domain-factory.py <domain-repo> [--strict]`
  — run from the pinned openxFactory checkout, never copied into domain repos.
- Credential contracts: [xfactory-credential-contracts schema](contracts/schemas/xfactory-credential-contracts.schema.yaml)
  and `scripts/validate-credential-contracts.py <domain-repo>` — the five
  credential record kinds under `credentials/` (DTN-004).
- Workflow contracts: [xfactory-workflow schema](contracts/schemas/xfactory-workflow.schema.yaml)
  and `scripts/validate-workflow-contracts.py <domain-repo>` — every
  `<domain>_workflow_contract` under `workflows/` validates against the
  neutral shape (DTN-001/002).
- Memory gateway: [contracts/memory-gateway](contracts/memory-gateway/README.md)
  and `scripts/validate-memory-gateway.py` validate the canonical gateway
  schemas, provider examples, conformance fixtures, and first runtime smoke
  path for `xfactory.memory.*`.
- Avatar reference runtime: `scripts/validate-avatar-runtime.py` statically
  proves the non-deployable, stdlib-only boundary of `xfactory/avatar_runtime/`
  (no listener, provider SDK, persistence, credential loading, or provisional
  import) for feature `specs/003-avc-reference-runtime`.
- Versioning: [Contract Versioning Policy](docs/contract-versioning-policy.md)
  and [contracts/CHANGELOG.md](contracts/CHANGELOG.md).

## OpenSpec Records

Active changes:

- [add-worker-enrollment-broker](openspec/changes/add-worker-enrollment-broker/proposal.md)
  — authored 2026-07-26, exit 1 of the `worker-enrollment-broker` staged
  topic: the neutral contract for how a machine becomes a governed worker and
  stays one, ratified BEFORE its three realizations are built. The Worker Host
  App cannot register a host today because the only way to hand it a runner
  registration token is to put administration-tier minting authority on the
  host, which the App identity tiers forbid — the decision parked at PRs
  #36/#37. Brett resolved it on 2026-07-26 by widening the question to two
  estates (the Intune fleet, and staff workstations volunteering as
  long-lived temp workers) served by ONE enrollment point with two
  authentication modes: fleet hosts by per-host identity in an Opsx key vault
  (broker ACCESS, never minting), volunteers as the ENGINEER by device code
  with no standing secret ever written to the machine. Minting authority — for
  registration AND remove tokens — lives only in the broker, under the
  ratified administration-tier custody shapes. The governing inversion is
  ruling 4: enrollment grants a renewable LEASE (id, TTL, trust tier, runner
  group) rather than a permanent registration, so staleness, revocation,
  trust, and audit all become properties of a renewal decision the platform
  re-takes — the only kind of control that works on hardware nobody manages.
  Every renewal response carries the current minimum app version, and a
  below-floor or revoked worker FAILS CLOSED (runner services stop, heartbeat
  reports `update_required`) until the engineer updates; revocation is simply
  refusing the next renewal, needing no reach into the machine. Package policy
  splits by estate (fleet hard-pins version + sha256 with self-update off and
  bumps ride manifest rollouts; temp workers self-update with the observed
  version informational), volunteered hardware lands in a dedicated runner
  group with a trust tier lanes can decline, and every enrollment, renewal,
  refusal, and revocation is audited by a record shape in which no token value
  can appear. Ships seven schemas — the seventh, `worker_removal_grant`, added by
  the 2026-07-26 amendment that is task 2.5's contract half: the remove-token
  issuance response, on the enrollment grant's transient-token discipline, with no
  registration token and no runner package by shape, so drift repair can never
  re-enrol a host — plus packaged positive/negative examples and a
  canonical validator; the broker SERVICE (home unresolved — design D1, the
  first decision), the Omnigent-Install registration/renewal integration, and
  the OpsxFactory custody/policy/runner-group work are named successor
  changes.
- [add-workbench-branch-sessions](openspec/changes/add-workbench-branch-sessions/proposal.md)
  — authored AND RATIFIED 2026-07-26, the single exit of the
  `workbench-branch-sessions` staged topic; twenty-one decisions locked and no
  open questions, after a five-lens adversarial review (two findings confirmed
  and fixed) and a rename-completeness audit. Realization is unblocked; it
  archives on merged plus green realization evidence, not on ratification.
  The workbench becomes a place to CREATE and EDIT documents
  without loosening a gate, because the working state moves onto a git branch
  and the PULL REQUEST is the formal re-entry into the governed doc system.
  The first gate write against a tile spawns `draft/<staging-id>` (named for
  the TILE, so two humans join one session) and materializes a git WORKTREE —
  the served checkout never switches branches, which dissolves the
  shared-checkout hazard by construction. Every gate action is ONE commit
  carrying its documents and its gate-action record together, so the audit
  trail falls out of version control; on-branch edits arrive as a new gated
  `edit-document` verb valid ONLY inside a session (the PR review is the
  governance — the ratified gates-happen-on-main rule read forwards), while
  the `edit-apply` redline path keeps its ceremony for main-resident
  documents. Session panels read a snapshot addressed `(repository,
  session-branch)` through the registry `add-dashboard-repo-selector` lands —
  no overlay machinery — regenerated after every gate action, with the
  freshness header naming the branch; drafts are visible ONLY inside their
  session, so `main` stays the shared truth on the wheel, the funnel, and the
  hosted site. "Saving" is a gated `open-pr` verb that pushes the branch into
  the existing Merge-Master ritual and holds no approval authority; merge (or
  explicit abandon) tears down the worktree, the registry entry, and the
  session notebook, and a MERGE additionally deletes the session branch, whose
  work `main` now holds. Because proposal ends the staging pipeline, `propose`
  REFUSES while a tile carries an unresolved session, naming both resolutions
  — merge the pull request, or abandon to discard — so a proposal is never
  commissioned from drafts stranded on an unmerged branch. Canon notebooks
  stay MAIN-ONLY; per-session `xf-session-<topic>` notebooks sync from the
  worktree, in a namespace deliberately disjoint from the workbench's swept
  `xf-wb-*` scratch notebooks. Local plane only until the intent plane's apply
  lane (§4) can produce a ref. Sequenced strictly after
  `add-dashboard-repo-selector` and `add-propose-verb`.
- [add-dashboard-repo-selector](openspec/changes/add-dashboard-repo-selector/proposal.md)
  — authored 2026-07-26, exit 1 of the `dashboard-repo-selector` staged
  topic: a repository selector whose roster is the project register (sparse
  repositories render whatever stations they have data for and are never
  refused), a snapshot source keyed on the PAIR (repository, ref) with
  `ref` defaulting to `main` and one serving-side registry behind it, a new
  additive snapshot-INDEX contract (its own schema — the snapshot schema is
  not grown), and the snapshot/image decoupling Brett decided 2026-07-25
  after a document landed minutes past a rebake and stayed invisible: bake
  the APP and fetch the DATA at runtime, with the baked snapshot demoted to
  a first-boot/offline fallback that shows a never-silent stale banner, a
  freshness header (`repo @ ref · source_revision · generated-at`), one
  refresh affordance with two plane bindings (served re-fetch; local
  regenerate), and `workflow_dispatch` on the publication lane — the pod
  gains no build or rollout authority by any path. Sequenced strictly
  before `add-workbench-branch-sessions`, which consumes the seam.
- [add-workbench-bullseye-and-create](openspec/changes/add-workbench-bullseye-and-create/proposal.md)
  — authored 2026-07-25: two coupled deltas to the staged workbench — the
  `lens` panel renders the match-count bullseye at tile scope (the scoped
  derivation already computes the geometry) above the always-present matrix,
  with the checked-keyword selection persisting across tab switches; and a
  human-only `create-document` gate verb drives the existing tested
  authoring scaffold (create-only; an existing target refuses) with per-tab
  seeding — the tile's keywords on `docs`, the live checked set plus a
  recipe citation on `lens` (the brainstorm's centre-ring gesture), a new
  fragment in the topic on `outline` for staged scopes — recorded as a
  gate-action record, rendered as copyable CLI descriptors where the gate
  capability is off.
- [add-lens-gate-verbs](openspec/changes/add-lens-gate-verbs/proposal.md)
  — authored 2026-07-25: two human-only gate-console verbs executing the
  keyword lens's plans through the tested engines (`lens-save-recipe` →
  workbench manifest; `lens-add-as-cluster` → manifest + pending_review
  human-seen submission), recorded dispatches with the engines' refusals
  surfaced at the route; the generated cross-reference index stays
  untouched; plan-only posture preserved where the gate capability is off.
- [add-hermes-customer-subject-runtime-contract](openspec/changes/add-hermes-customer-subject-runtime-contract/proposal.md)
  — ratified 2026-07-12: domain-neutral Hermes runtime-topology and
  governed-record-integrity contracts separating the Customer/Client/Domain
  role templates from their runtime layer instances, with repeatable
  pseudonymous Customer subject instances, fail-closed default-deny
  isolation, explicit expiring directional bindings, parallel v2 job
  envelope/run/event and Postgres operational contracts, an idempotent
  v1-to-v2 migration with reconciliation and quarantine, and a versioned
  additive release bundle that Hermes Install must pin before multi-subject
  implementation proceeds (code surface: openxFactory; at the
  acceptance-gate stage — its tasks accept Speckit realization evidence;
  Hermes Install Gate G0/T009 stays closed until the published evidence
  independently reproduces)
- [add-ideation-dashboard](openspec/changes/add-ideation-dashboard/proposal.md)
  — re-proposed 2026-07-13 and **re-ratified 2026-07-14** (D1–D17; the
  07-12 ratification was set aside at a design-round demotion);
  staged-origin change for the generated ideation dashboard: realization
  funnel snapshot over a possibles register, cluster canvas working
  surface (D12), keyword lens set-builder with cluster-as-recipe
  persistence (D13), project grouping roll-ups (D10), drill-down explorer
  and read-only Markdown viewer (D14/D15), the human gate console and
  next-step kickoff (D16/D17), per-actor authoring authority, non-mutating
  machinery, and the nightly snapshot lane; web-based v1 served per
  Option C on the internal xForge plane. **Realized + deployed
  2026-07-14**: codexFactory feature 002-ideation-dashboard merged
  (231 tests, adversarial review ACCEPT), nightly lane green (first
  snapshot committed), live at ideation-dashboard.xforge.us (Nextest,
  boundary validator PASSED). At 26/27 — remaining: task 3.5 human-seen
  submission, gated on add-ideation-cross-reference-readiness's
  pending_review intake contract (landed 2026-07-14 — 3.5 is now
  unblocked pending its codexFactory implementation); archives on the archive-gate
  ledger (contract registration + additive snapshot-schema deltas)
  once those land (code surface: openxFactory, codexFactory, xFactory;
  ideation-cross-reference delta sequenced with
  add-ideation-cross-reference-readiness)
- [add-proposal-origin-contract](openspec/changes/add-proposal-origin-contract/proposal.md)
  — staged-origin proposal requiring every OpenSpec change to declare one
  durable staged or approved ad-hoc origin in `.openspec.yaml`, with gate
  rejections, archive retention, history migration, and the fifteenth
  deterministic doc-health family (code surface: codexFactory; ratified
  2026-07-12 — admitted intent, active until realization evidence lands;
  implementation follows ideation routing)
- [add-ideation-cross-reference-readiness](openspec/changes/add-ideation-cross-reference-readiness/proposal.md)
  — staged-origin proposal for the unified cross-stage ideation topic index,
  three-tier Hermes readiness panel (min >= 8 recommendation gate), and the
  nightly ideation-readiness doc-health lane (code surface: openxFactory,
  codexFactory, xFactory, omnigent-install; ratified 2026-07-12).
  **Realized 2026-07-14**: index contract + strict validator + the living
  bootstrap index (`ideation/cross-reference.yaml` + generated md; 11
  clusters after the 2026-07-16 staging exits);
  scorer worker merged (codexFactory 003-ideation-readiness at 1fc0bd7,
  pre-merge review ACCEPT WITH FIXES); nightly lane + readiness-scorer
  profile landed (lane SKIPPED until host deployment — valid landed
  state). **First-lane-run evidence 2026-07-23** (nightly run
  30000105423): the readiness-scorer child ran on the deployed CPC rider
  profile and 2 clusters persisted scored readiness panels into
  `ideation/cross-reference.yaml` (openxFactory PR #38, delivered by the
  derive lane's rolling commit-back; a readiness-only run still lacks its
  own commit-back — scores persist when the derive lane also merges).
  At 15/16 (5.2 records through archive); archives on the
  release-realization flow
- [add-possibles-derivation-lane](openspec/changes/add-possibles-derivation-lane/proposal.md)
  — ad-hoc-origin proposal (ideation-dashboard brainstorm v5 candidate 1 +
  the Brett-approved THE WHEEL locked spec, 2026-07-16) for the AI-assisted
  derive-possibles worker lane: a bounded read-only Omnigent lane that derives
  CANDIDATE possibles from the landed cross-reference index and proposes
  `possibles_register` entries carrying `origin: ai-derived`, worker-run
  provenance, and `pending_review` disposition, humans disposing on the gate
  console. Adds the small ADDITIVE possibles-register kernel delta (`origin` +
  a `derivation` $def, no `contract_schema_version` bump) modelled on the
  human-seen intake pair; carries the document-cataloger lane's artifact-worker,
  model-worker (orchestration-authoritative identifiers), immutable-evidence,
  and concurrency-protected next-run-merge invariants; derived-undisposed
  possibles stay a distinct non-`indexed` WHEEL class excluded from any Ranked
  Plan (code surface: codexFactory, openxFactory, xFactory, omnigent-install;
  realization follows the ideation-readiness two-repo split; release allocated
  at realization). **§3 worker realized 2026-07-22** (codexFactory
  `specs/004-derive-possibles`, PR #25: worker + prompt contract,
  orchestration-authoritative identifiers, fingerprint-CAS merge, one-way
  gate dispositions, boundary-guarded persistence, 33 tests). **§4 lane +
  2.6 registration realized 2026-07-22**: nightly dispatch + 10/30-minute
  watchdog + dormant rolling-PR register commit-back (codexFactory PR #27 +
  the xFactory artifact-only child workflow), the omnigent-install
  `derive-possibles` profile v1 (Omnigent-Install PR #22, contract-only),
  and the kernel delta registered as **contract-v1.14**. The lane reports
  SKIPPED until a host advertises the profile (the readiness precedent's
  valid landed state). **§5.1 tests realized 2026-07-22** including THE
  WHEEL (codexFactory PR #28, `web/views/wheel.js` + `wheel-model.js`:
  the locked Track C deck with class-coded threads — undisposed derived
  possibles render non-`indexed` `inferred`, demo placeholders
  `synthesized`). **FIRST LANE RUN 2026-07-23** (nightly run 30000105423,
  CPC rider profile live): 3 contract-clean `pending_review` possibles
  derived from cl-codexfactory merged into `possibles_register` via the
  rolling commit-back PR (openxFactory #38, approved + merged) — the
  register's bootstrap-empty era is over; humans dispose on the gate
  console. At 19/20; remaining: 5.2 records through archive
- [add-ideation-intent-plane](openspec/changes/add-ideation-intent-plane/proposal.md)
  — staged-origin proposal (ideation-action-plane topic, organized 2026-07-23
  from the dashboard-action-center + cloud-workstation-topology brainstorms;
  ratified 2026-07-23) for the intent plane that makes the dashboard the
  process action center WITHOUT weakening D16: a click emits a signed
  `gate-intent` (actor, verb, target, snapshot_rev_seen); a dispatch-only
  inbox wakes the apply lane; the gate-console engine revalidates and commits
  intent + gate-action record + artifacts atomically via rolling PR
  (second-touch DECIDED: custody-not-decision, batched auto-merge). Two-plane
  rendering (snapshot + intent-feed overlay + refusal panel), identity ladder
  (per-user htpasswd -> Keycloak, contract-invisible), dispose tray as the
  first verb (local loopback-executing routes first, hosted intents second),
  Flutter verdict terminal as the same client class. Also carries the
  document-lifecycle GATES-HAPPEN-ON-MAIN delta (a transition is not real
  until merged). (code surface: codexFactory, openxFactory, omnigent-install,
  xFactory; release allocated at realization)
- [add-propose-verb](openspec/changes/add-propose-verb/proposal.md)
  — gate-console verb `propose` (Brett's 2026-07-24 action-center direction:
  take a staging tile to a proposal from the dashboard): kickoff's
  recorded-dispatch mechanic at the staging→proposal boundary — a human-only
  `workflow-job` commission (workflow `proposal-authoring`, target
  `topic_id`) + gate-action record; the authoring runs externally and lands
  as an ordinary change under the existing review/ratify gates. Additive
  gate-intent / gate-action-record enum + `topic_id` target extension.
  (code surface: codexFactory, openxFactory; release allocated at
  realization)
- [add-wheel-action-verbs](openspec/changes/add-wheel-action-verbs/proposal.md)
  — four gate-verb rulings Brett made 2026-07-25 for the wheel's
  expanded-tile action row: `demote` promoted from descriptor-only to an
  executing dashboard verb (plan + record on the click, the corpus move stays
  the separate human-run step), plus three recorded commissions on propose's
  mechanic — `promote-to-staging` (an ACCEPTED possible organized into
  `ideation/staging/<topic>/`; dispose-possible is a strict upstream and the
  pick edge lands with the fragment, not at commission), `derive-possibles`
  (a cluster-scoped run of the ratified possibles-derivation lane) and
  `research-brief` (a pre-verdict evidence brief accompanying a possible,
  never a precondition for disposing). Additive gate-intent /
  gate-action-record enum + `cluster_id` target extension; the three
  fulfilment lanes are out of scope (a terminal session fulfils dispatched
  commissions in the interim, as with propose). (code surface: codexFactory,
  openxFactory; release allocated at realization)
- [add-staging-workbench](openspec/changes/add-staging-workbench/proposal.md)
  — Brett's Track B ruling 2026-07-25 (the staging area is where the real
  proposal gets developed): the workbench as that area's READ-ONLY
  foundation. Derived-model growth first — a deterministic per-document
  completeness signal computed at snapshot generation time (structure,
  length, open markers, keyword coverage, link degree; fixed weights as v1
  contract constants, no LLM judgment so it stays testable and
  byte-identical) emitted as an additive `documents[].completeness` object,
  informational only and never gating anything. Then the scoped view: a
  full-screen workbench over ONE topic-bearing tile (cluster, possible, or
  staged topic) with `docs` (the tile's doc set with completeness bars),
  `lens` (interconnectedness re-scoped from the existing
  keyword_index/degree derivation, no new analysis) and `outline` (the
  topic's outline read through the viewer's `/source` pass-through) panels,
  plus an ungated read-only `open workbench` row on the wheel's
  expanded-tile action point. The AI chat layer — and outline editing, and
  every workbench write path — is Track C, a later change. (code surface:
  codexFactory, openxFactory; release allocated at realization)
- [add-cross-factory-ideation-routing](openspec/changes/add-cross-factory-ideation-routing/proposal.md)
  — staged-origin proposal for unknown-owner/cross-domain claim routing,
  destination acceptance, the fourteenth deterministic doc-health family, and
  bounded ideation-organizer lane; implementation follows document cataloging
- [qualify-avatar-brokered-call-feasibility](openspec/changes/qualify-avatar-brokered-call-feasibility/proposal.md)
  — tenant-data-free F0 harness for sideband-before-answer ordering, retries,
  readiness, revocation, redacted evidence, and contract interface impacts;
  F0 does not qualify live use. **Realized (F0 `PASS`); kept active** because the
  realized kernel's `interface-lock.yaml` F0 pin resolves this change's evidence —
  archiving it would break the fail-closed F0 gate or force a `contract-v1.7` re-tag
- [implement-avatar-client-lab](openspec/changes/implement-avatar-client-lab/proposal.md)
  — staged-origin change (exit of `ideation/staging/avatar-client-lab`, six
  decisions locked 2026-07-13) for the offline, deterministic Flutter avatar
  client UI lab: content-addressed consumption of `contract-v1.7` +
  `contract-v1.8`, fixture-replay determinism through a pure session core, the
  replaceable six-state avatar seam, five-region adaptive shell with the
  authority status strip, gating accessibility baseline, and fail-closed
  deferral of voice/WebRTC/Hermes to `qualify-avatar-live-voice` (code surface:
  openxFactory, codexFactory — the Flutter app lives in codexFactory under
  `apps/avatar-client-lab/`; openxFactory owns the neutral fixtures and acceptance
  map; codexFactory's pin is a routine submodule-pointer sync; archives on
  realization evidence)

The avatar-client kernel (`contract-v1.7`), reference runtime, and avatar-first UI
standard (`contract-v1.8`) are realized. The contract kernel, the revocation
clarification, the reference runtime, and the avatar-first UI standard all archived
2026-07-13 (below); **only F0 feasibility remains active** — its evidence is resolved
by the realized kernel's `interface-lock.yaml` F0 pin, so archiving it would break the
fail-closed F0 gate or force a `contract-v1.7` re-tag. The avatar client itself is
**now proposed** as the active change `implement-avatar-client-lab` (staged origin
`ideation/staging/avatar-client-lab`, six decisions locked 2026-07-13; ratified and
in realization 2026-07-14), and its successors are now
staged too: `qualify-avatar-live-voice` (internal-live provider qualification;
blocked on open questions + a released client) and `avatar-pilot-hardening` (real
Hermes/domains/audits + pilot; structurally last) — see the
[Staging Index](ideation/staging/INDEX.md).

Archived changes:

- [add-hermes-domain-content-manifest](openspec/changes/archive/2026-07-24-add-hermes-domain-content-manifest/proposal.md)
  — **ratified, realized, and archived 2026-07-24** (seeding increment 4b,
  contract half; released as `contract-v1.18`, annotated tag verified): the
  optional `hermes_domain_content_manifest` declaring a domain repo's
  seedable content set (convention-then-contract successor to increment
  4a's well-known-path list) and the `hermes_memory_binding` record schema
  formalizing increment 3's derived gateway-rails input; canonical
  validator extensions green over fixtures and the real codexFactory tree,
  with the live-derived opensoft bindings as the packaged example.
- [add-governed-derived-model](openspec/changes/archive/2026-07-23-add-governed-derived-model/proposal.md)
  — **ratified, realized, and archived 2026-07-23** (same-day promotion of
  the governed-derived-model staging topic; DTN-014): the
  `governed-derived-model` capability — conformance declaration
  (`xfactory_derived_model_conformance`) with `governed`/`calibrated`
  tiers, five line-verified invariants, six declared dials (incl.
  `person_modeling`), the vocabulary doc
  (`docs/governed-derived-model.md`), and
  `scripts/validate-derived-models.py` with positive/negative fixtures.
  Realization evidence: MedxFactory conforms at `governed`
  declaration-only (0987bca, unchanged ratified templates); AdxFactory
  is the first `calibrated`-tier conformer (eb98f84, via
  `add-adx-object-model`). Deferred to the contract-v1.16 cut: manifest
  entry + DTN-014 `adopted` flip.
- [add-client-infrastructure-liaison](openspec/changes/archive/2026-07-17-add-client-infrastructure-liaison/proposal.md)
  — exit of `ideation/staging/client-infrastructure-liaison`: the neutral
  Client Infrastructure Liaison coordination profile (promoted capabilities
  `client-infrastructure-liaison` + `client-infrastructure-request`) and the
  `client_infrastructure_request` contract family — two schemas, reference
  examples, and the strict validator — with three execution bindings
  (client-managed / managed-host / OpsxFactory-executed), readiness-gated
  completion, and the OpsxFactory handoff boundary; MODIFIES
  `roles-authority-model` so client-tenant infrastructure execution routes
  here (closing the github-administration-plane carve-out). PO gate signed
  off by Brett 2026-07-16; realized as **`contract-v1.13`** and archived
  2026-07-17 with the verified supporting-doc bundle. Successor per-domain
  adoption changes (OpsxFactory binding/readiness producer first, then
  Medx/Ledger/Ad/codex aliases) are proposed per the impact map's sequence
- [adopt-avatar-client-lab-candidates](openspec/changes/archive/2026-07-16-adopt-avatar-client-lab-candidates/proposal.md)
  — the owning change for the avatar-client-lab P-ledger escalations and
  fixture adoptions: landed the P1 neutral avatar-state derivation table and
  the P10 22-capability-scenario register (new `avatar-lab-evidence`
  capability), adopted the panel-confirmed P7/P8/P11/P12/P13 deterministic
  fixture families into `examples/avatar-first-ui/`, and cut `contract-v1.12`
  (also manifest-registering the successor evidence register so the
  SCO-001-S05 discharge takes effect). Realized via codexFactory PR #17
  (avatar-client-lab contract-pin resync, nine gates green on the resynced
  pin; Brett Tier-1 approval, merge `0fed12c`), archived 2026-07-16
- [add-github-app-identity-tiers](openspec/changes/archive/2026-07-14-add-github-app-identity-tiers/proposal.md)
  — exit of `ideation/staging/github-administration-plane`: extended
  `roles-authority-model`'s structural-parking requirement so any identity
  able to modify a GitHub enforcement gate is authority-separated from any
  identity doing ordinary content/workflow work on the same surface, adding
  the content-vs-administration App identity tiers and administration-tier
  credential-custody requirements (code surface: none — doc/spec only);
  ratified and archived on landing 2026-07-14. Sibling OpsxFactory change
  `add-github-administration-workflow` (realized, archived 2026-07-15)
  instantiates the tiering concretely; live rollout done
- [add-document-cataloging](openspec/changes/archive/2026-07-14-add-document-cataloging/proposal.md)
  — external governed-document catalog, controlled discovery taxonomy,
  immutable snapshots, thirteenth deterministic doc-health family, and the
  bounded document-cataloger lane; realized as `contract-v1.11` with the
  225/225 full-corpus mechanical baseline and nightly dispatch wiring,
  archived 2026-07-14
- [define-avatar-client-contract-kernel](openspec/changes/archive/2026-07-13-define-avatar-client-contract-kernel/proposal.md)
  — canonical eight-contract AVC kernel, registries, fixtures, validator, and
  repository-boundary rules; realized as `contract-v1.7`, archived 2026-07-13
- [clarify-avatar-revocation-client-enforced](openspec/changes/archive/2026-07-13-clarify-avatar-revocation-client-enforced/proposal.md)
  — ACR-005 disposition: revocation is client-enforced within the 5 s bound;
  archived 2026-07-13
- [implement-avatar-reference-runtime](openspec/changes/archive/2026-07-13-implement-avatar-reference-runtime/proposal.md)
  — non-deployable deterministic broker/control reference realized against
  `contract-v1.7`, with archive-safe content-addressed conformance (FR-034a);
  archived 2026-07-13
- [align-avatar-first-ui-standard](openspec/changes/archive/2026-07-13-align-avatar-first-ui-standard/proposal.md)
  — avatar-first UI standard, domain profile carrier, template, examples, and
  offline realization validator; realized as `contract-v1.8` (acceptance map
  relocated to `examples/avatar-first-ui/` so the validator survives archive);
  archived 2026-07-13
- [define-human-escalation-contract](openspec/changes/archive/2026-07-12-define-human-escalation-contract/proposal.md)
  — route/park/interrupt escalation ladder with a deliberately high interrupt
  bar (containment failure only, cited classes), parked-decision packets at
  existing gates, fail-closed silence, the Merge Master low-risk envelope,
  and structural parking in external enforcement; ratified 2026-07-12,
  archived on landing (`code_surface: none`); resolves the dangling `HR`
  consultation in the engineering escalation table
- [add-proposal-supporting-doc-lifecycle](openspec/changes/archive/2026-07-09-add-proposal-supporting-doc-lifecycle/proposal.md)
  — proposal-owned supporting documents, deterministic archive bundles, and
  proposal-stage NotebookLM returns (ratified and realized 2026-07-09)
- [add-release-realization-flow](openspec/changes/archive/2026-07-09-add-release-realization-flow/proposal.md)
- [add-lifecycle-notebook-hybrid-imports](openspec/changes/archive/2026-07-09-add-lifecycle-notebook-hybrid-imports/proposal.md)
- [neutralize-job-envelope](openspec/changes/archive/2026-07-09-neutralize-job-envelope/proposal.md)
- [split-roles-authority](openspec/changes/archive/2026-07-09-split-roles-authority/proposal.md)
- [promote-credential-contracts](openspec/changes/archive/2026-07-09-promote-credential-contracts/proposal.md)

- [add-contested-finding-rule](openspec/changes/archive/2026-07-09-add-contested-finding-rule/proposal.md)

- [promote-workflow-gate-contract](openspec/changes/archive/2026-07-09-promote-workflow-gate-contract/proposal.md)

- [refine-promotion-provenance](openspec/changes/archive/2026-07-09-refine-promotion-provenance/proposal.md)
- [adopt-workflow-visualization-stack](openspec/changes/archive/2026-07-09-adopt-workflow-visualization-stack/proposal.md)

- [add-doc-health-contract](openspec/changes/archive/2026-07-09-add-doc-health-contract/proposal.md)
- [concretize-prose-tagging-syntax](openspec/changes/archive/2026-07-09-concretize-prose-tagging-syntax/proposal.md)
- [add-lifecycle-notebook-projection](openspec/changes/archive/2026-07-09-add-lifecycle-notebook-projection/proposal.md)
- [add-document-lifecycle-vocabulary](openspec/changes/archive/2026-07-09-add-document-lifecycle-vocabulary/proposal.md)
- [reconcile-domain-neutral-and-engineering-spec-ownership](openspec/changes/archive/2026-07-09-reconcile-domain-neutral-and-engineering-spec-ownership/proposal.md)

- [add-customer-memory-gateway-architecture](openspec/changes/archive/2026-07-08-add-customer-memory-gateway-architecture/proposal.md)
- [enable-live-openxfactory](openspec/changes/archive/2026-06-26-enable-live-openxfactory/proposal.md)
- [restructure-factory-repo-boundaries](openspec/changes/archive/2026-06-26-restructure-factory-repo-boundaries/proposal.md)
- [migrate-canonical-policy-to-openxfactory](openspec/changes/archive/2026-06-26-migrate-canonical-policy-to-openxfactory/proposal.md)

Canonical specs:

- [canonical-contract-migration](openspec/specs/canonical-contract-migration/spec.md)
- [canonical-policy-migration](openspec/specs/canonical-policy-migration/spec.md)
- [memory-gateway](openspec/specs/memory-gateway/spec.md)
- [reference-proof-placement](openspec/specs/reference-proof-placement/spec.md)
- [repo-boundary-governance](openspec/specs/repo-boundary-governance/spec.md)
- [shared-contract-ownership](openspec/specs/shared-contract-ownership/spec.md)

## Install Repo Pins

`openxFactory` pins approved install repo revisions under `installs/` when needed.
Long-term workspace aggregation belongs in the top-level `xFactory` repo, not in
`openxFactory`. DomainxFactory repos should pin the `openxFactory` version they
consume; `openxFactory` should not need to pin every DomainxFactory consumer.

Current submodules:

- [installs/omnigent-install](installs/omnigent-install) -> `opensoft/Omnigent-Install`

Clone or refresh with:

```bash
git submodule update --init --recursive
```

Hermes install is not yet a submodule. Its canonical remote decision is still open; see [Decision 0001](docs/decisions/0001-install-repo-submodules.md).

## Status

This repository is documentation-first. It should not contain live credentials, production memory-provider databases, runtime secrets, generated agent workspaces, or domain-specific runtime data.
