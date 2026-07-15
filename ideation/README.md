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

- [Git-Native Record Vault](brainstorm/git-native-record-vault.md) — pull
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

Staged topics: see the [Staging Index](staging/INDEX.md), the kept-current
inventory of every topic under `staging/` — update it, not this list, when a
staged file is added, removed, or promoted.

Active proposals promoted from staging:

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
- [add-document-cataloging](../openspec/changes/add-document-cataloging/proposal.md)
  — user-approved split from the former umbrella proposal; owns external
  controlled tagging, immutable catalog snapshots, deterministic catalog
  validation, and the bounded document cataloger.
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

Proposal source and completed design history are retained with their active or
archived OpenSpec changes under `supporting-docs/` or
`supporting-docs.tar.gz`, with readable manifests.
