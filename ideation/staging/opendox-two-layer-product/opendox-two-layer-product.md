# Staged: openDox and openXdox — two open-source layers, an installable app with a database, and domain descendants that pin the integration layer

Status: staged
Kind: capability-proposal
Summary: Brett ruled on 2026-09-04 that the document-and-ideation workbench
becomes TWO open-source repositories — `opensoft/openDox`, a hosted installable
app with its own database whose objects are users, projects, documents and
ideas, keeping the git and NotebookLM integrations and the document-management
and ideation tooling, and `opensoft/openXdox`, openDox tuned for openxFactory —
with domain descendants (`MedxDox`, `codexDox`, ...) pinning openXdox in the
ratified `<Domainx><Product>` form and a DomainxFactory install bringing up its
descendant in the tenant with its own database. The ruling overrides
`docs/openxdox-naming.md`'s "openDox is taken" and departs from the wallet
precedent twice, both deliberately: the integration seam becomes its own
open-source repository rather than staying in openxFactory, and the extraction
cannot meet the byte-identical floor because `doc_health` and
`ideation_dashboard` currently import each other. What openxFactory keeps is the
corpus and its governance; what leaves is the code that reads it.
Topics: opendox, openxdox, medxdox, codexdox, ideation-dashboard, doxbench,
repo-split, two-layer-product, domain-descendant-boundary, neutral-product-pin,
corpus-adapter, tenant-install, per-tenant-database, users, projects,
notebooklm, git-integration, openxdox-naming, doc-health, document-lifecycle,
install-provisioning, feat-request
Repository context: SPLIT across four homes on purpose. `opensoft/openDox` (to
be created) becomes the neutral product's home and owns the app — accounts,
projects, documents, ideas, the editor and chat, the model plane, the branch
session, the NotebookLM integration, the install and the database schema.
`opensoft/openXdox` (to be created) becomes the integration layer's home and
owns the corpus reader, the lifecycle projection, the funnel and wheel and lens,
the gate console and its verbs, and the three lanes. openxFactory keeps the
CORPUS and its GOVERNANCE — `document-lifecycle`, `doc-health`,
`workflow-gate-contract`, the contract families, the ideation estate and all
ideation provenance — plus whatever neutral seam contract the split needs, and
consumes both products at pins. The xFactory aggregation gains submodules. The
DomainxFactories gain `<Domainx>Dox` descendants, created lazily.
Staging ID: `openxFactory:staging:opendox-two-layer-product`
Captured: 2026-09-04
Source: Brett Heap's ruling of 2026-09-04, in session, recorded verbatim in the
governing record `opensoft/openxFactory` issue #656 — filed as an issue
precisely so the ruling lives outside a chat transcript. Two utterances: the
origin complaint ("we do not have a place to store projects ... I think we need
to make this an app that installs and is hosted with a db. we should have users
and projects and can expand the feature set") and the topology ("openDox is a
dead project ... lets use that name as the core opensource repo. we have two
layers of opensource openDox and openXdox. The openXdox is openDox tuned for use
with openXfactory. we will make openDox work to just manage documents and ideas.
it will keep the integration with git and notebook lm etc and have all tools
that help for document management and ideation. then openXdox will integrate
with openXfactory"), plus the earlier descendant sentence from the same sitting
("We then further pin that down to medxDox and CodeXdox for use in those domain
factories. If I install MedxFacotry, then I get a medXdox install running in the
installed tenand with its own db"). The inventory the claims rest on was
measured against `origin/main` `6ced5d1d`/`bc1bd4ee` the same day by the
read-only openXdox review (lane openxfactory-smalls). Origin provenance is the
`ideation-dashboard` brainstorm, the doxBench packet, and the
`openxdox-install-app-provisioning` staged topic, which this topic folds.
Target capabilities: REMOVED (by SPLIT) `ideation-dashboard` from the
openxFactory corpus, with the successor location of each requirement recorded in
`opensoft/openDox` or `opensoft/openXdox`; ADDED a neutral corpus-adapter seam
capability in openxFactory (the interface a corpus reader consumes and a
governed corpus offers — enumerate, read/write, classify, assess, act);
MODIFIED `domain-descendant-boundary` (a descendant of a RUNTIME product with a
schema and migrations, which every existing descendant precedent is not);
MODIFIED `neutral-product-pin` (pinning a running product whose consumption is a
deployment with a migration, not a file read). Possibly MODIFIED `doc-health`
and MODIFIED `document-lifecycle` depending on Q4 and Q1; both carried as open
questions rather than declared. The ADDED seam capability is deliberately NOT
fenced as an `xspec:candidate` target below: it does not exist in
`openspec/specs/` or in any active change's `specs/`, so fencing it would emit
tag-hygiene unresolved-target findings. The fenced blocks target
`ideation-dashboard`, the capability this topic exists to relocate.

## Claims

The 2026-09-04 ruling is settled context. These claims are constraints on the
eventual proposal, not questions in it; the open questions below are what the
ruling did NOT settle.

1. **Two open-source layers, two repositories.** `opensoft/openDox` is the
   neutral core; `opensoft/openXdox` is openDox tuned for openxFactory. Neither
   exists today (verified 2026-09-04: `gh repo view` returns "could not resolve"
   for both). This is not one repository with a plugin directory and not a
   monorepo with two packages: the ruling names two layers of open source.
2. **openDox's scope is the app.** An app that installs and is hosted with a
   database. Users and projects. "manage documents and ideas". It "will keep the
   integration with git and notebook lm etc and have all tools that help for
   document management and ideation". The feature set is explicitly expandable
   ("can expand the feature set") — the listed scope is a seed, not a boundary.
3. **openXdox's scope is the openxFactory integration.** "then openXdox will
   integrate with openXfactory". The lifecycle interpretation, the promotion
   funnel, doc-health projection, the gate console and its verbs, and the
   nightly/refresh/apply lanes are integration, not app.
4. **Domain descendants pin openXdox, in the `<Domainx><Product>` form.**
   `MedxDox`, `codexDox`, and by extension `LedgerxDox`, `OpsxDox`, `AdxDox` —
   the same casing scheme `MedxChart`, `MedxPractice`, `LedgerxWallet` and
   `MedxAvatar` already use, ratified as a general rule by
   `domain-descendant-boundary`. Not `medXdox`, which would be a third casing
   scheme in the org; the ruling's own transcript spells it both ways and the
   ratified form governs.
5. **A DomainxFactory install brings up its descendant, in the tenant, with its
   own database.** "If I install MedxFacotry, then I get a medXdox install
   running in the installed tenand with its own db." The install composition is
   real and the database is per tenant.
6. **The naming record is overridden, and owes an Amendment 3 — carried by the
   change, not by this topic.** `docs/openxdox-naming.md` (`Status: ratified`,
   LOCKED 2026-08-13) rejected `openDox` as "the taken name" and built the
   `openX` + `dox` argument on that rejection. Brett has ruled the existing use
   dead and accepted the name. Because that record is `ratified`, the correction
   is an AMENDMENT in the change that creates the repository — the same
   discipline `split-openxwallet-repo` used for Amendment 2 — and it must state
   the collision facts as measured, listed under Evidence below. **This staging
   fragment does not edit the naming record and must not**: no contract, code,
   spec or naming-record edit belongs in this slice.
7. **A departure from the wallet precedent on the SEAM, ruled.**
   `split-openxwallet-repo`'s R3 kept the integration seam inside openxFactory —
   `governance/review-authority/` stayed, only the product left. Here the
   integration layer is itself an open-source repository. openxFactory keeps the
   corpus and its governance; the code that reads the corpus leaves entirely.
   This is a deliberate ruling, not an oversight, and the proposal must say so
   rather than reasoning as if R3 applied.
8. **A departure from the byte-identical floor, forced.** The wallet
   extraction's ratified safety property was a pure move — eight artifact
   digests matching openxFactory HEAD before the tag was cut, "because a move
   whose diff is not provably empty cannot be bisected against". That floor is
   unavailable: twelve of forty-eight modules import `doc_health`, `doc_health`
   imports back twice, and a two-way dependency cannot be carved into two
   repositories without changing code first. The extraction needs a DIFFERENT
   safety property, and inventing it is part of the work rather than a detail.
9. **The brand is already in canon.** The promoted `ideation-dashboard`
   requirement "The openDox project-first header" already says the dashboard
   header "SHALL brand as 'Opensoft openDox'". The product was being called
   openDox in ratified requirements before the ruling named the repository, so
   the ruling regularizes an existing name rather than introducing one.
10. **Ideation only in this slice.** The claim on the governing record is
    explicit: the brainstorm docs and this topic, with no contract, code, spec
    or naming-record edit. Those come with the OpenSpec change.

## Evidence and inventory (measured 2026-09-04)

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

- **Footprint of what would be split**, openxFactory `origin/main`:
  `scripts/ideation_dashboard/` 48 modules / 49,605 LOC; `web/` 40 files /
  30,410 LOC excluding the vendored `markdown-it.min.js`;
  `tests/ideation-dashboard/` 125 files / 3,927 `def test_` — **52% of this
  repository's 7,612 test functions**; `openspec/specs/ideation-dashboard/spec.md`
  289,266 bytes / **102 requirements / 472 scenarios**, the largest promoted spec
  in the corpus (next is `doc-health` at 243,924 B / 43 requirements); 4 contract
  schemas; 142 packaged examples; 5 governance docs; **30 archived changes** and
  **5 active changes** carrying an `ideation-dashboard` delta.
- **The coupling, both directions, measured.** OUTBOUND: 12 of 48 modules carry
  23 `doc_health` import statements — `authoring` (2), `cli` (1),
  `completeness` (1), `corpus_root` (1), `doxbench_packet` (1),
  `gate_console` (4), `gate_routes` (1), `generator` (3), `round_trip` (1),
  `serve` (3), `snapshot_registry` (1), `workbench` (4) — pulling `corpus`,
  `corpus.RealGit`, `lines.split_keepends`/`join_rows`, `derive_possibles`,
  `families.FAMILIES`, `TAXONOMY`, `DEFAULT_THRESHOLDS`, `staging_seed`,
  `shared_identity`, `pin_sentinels`, `ideation_readiness` and
  `runner.Context`/`run_suite`. INBOUND: exactly **two** statements —
  `doc_health/derive_possibles.py:857` and
  `doc_health/ideation_readiness.py:1351`, each `from ideation_dashboard.boundary
  import OutputBoundary  # lazy: house guard`. Every other `ideation_dashboard`
  mention inside `doc_health` (`corpus.py:193-195`, `lines.py:46-50`,
  `pin_sentinels.py:56`, `pin_class.py:413`) is a PROSE comment recording a
  co-authoritative reading window, not an import. **The back-edge is one class,
  in one 377-line module, imported lazily in two places** — which makes the
  cycle asymmetric and cheap to break in the expensive-to-fix direction's
  favour.
- **The reader's knowledge of openxFactory's tree is spread across a third of
  the package.** Path literals: `ideation/staging` in 16 modules, `contracts/`
  in 15, `docs/` in 9, `ideation/brainstorm` in 8, `openspec/changes` in 7,
  `ideation/dashboard` in 6, `openspec/specs` in 2.
- **Consumers running an instance today: zero.** codexFactory holds **0**
  tracked files under `scripts/ideation_dashboard/` or `tests/ideation-dashboard/`
  at `origin/main`, two DRAFT Speckit features (002, 010), and a comment-only
  doxBench digest pin in `stack.yaml` that states a verified fact which is false
  (declares `0e6e7e94…`/`8386566e…` and `contract-v1.29`; the actual bytes at
  its own pinned commit are `e563cc9f…`/`350bfedc…`, and openxFactory is at
  `contract-v3.3`). MedxFactory-over-notes and LedgerxFactory-over-entries exist
  only as intent in `docs/openxdox-naming.md`.
- **Live runtime state.** `openxdox.opensoft.dev` resolves and returns HTTP 401
  (auth-gated, live). The QA dispatch minter passed 6/6 readiness on 2026-08-15
  and both readiness results are EXPIRED (`valid_until` +30 minutes, twenty days
  ago). `intent-apply.yml` on the aggregation has **one run, ever** —
  2026-08-15T01:22:04Z, success. The nightly image-refresh worker has **three
  runs, zero successes** and has never produced `refresh-status.json`. The
  snapshot lane is green. OpsxFactory declares four workloads in namespace `dox`
  (`dox-auth`, `dox-dashboard`, `dox-intent-inbox`, `dox-token-minter`); the
  `openxdox` DNS A record exists on the live zone and is ungoverned
  (`prohibited_until_realized`, zone `reachable_ungoverned`).
- **The five active changes, and why sequencing is a real constraint.**
  `add-nightly-dashboard-refresh` (ratified 2026-08-25, re-ratified 2026-09-04;
  ADDED+MODIFIED on `ideation-dashboard` PLUS 7 ADDED requirements on
  `doc-health`; cross-repo across three repositories; archive gate OPEN, 13 open
  tasks) — note that it DEEPENS the exact coupling the split must break;
  `retire-doxbench-chat-turn-v1` (ratified 2026-09-01; archive gate open, 7 open
  tasks; schema bytes already moved at `contract-v3.0`);
  `add-doxchat-model-intake` (built 2026-08-26, not archived);
  `add-composed-view-authoring` and `add-lens-document-selection` (both
  `target_release: none`). Plus `add-ideation-intent-plane`, ratified
  2026-07-23, part-realized, whose target capability `ideation-intent-plane` is
  **absent from `openspec/specs/`** — ratified and unpromoted for 43 days.
- **The name-collision facts, as measured for the owed Amendment 3.** A GitHub
  organization **`opendox` exists**, created 2026-03-20, holding one public repo
  `opendox/dox` ("Rethinking Amazon Product Performance Intelligence", 357 KB,
  last pushed 2026-05-31) — so the ORG name is taken by an unrelated subject.
  GitHub search returns **six** repositories named `opendox`: `noitran/opendox`
  (22 stars, a Laravel/Lumen OpenAPI package, last pushed 2022-02-10 — the
  largest), `fum4/opendox` (0 stars, pushed 2026-07-16, "Spec + CLI + skill for
  agent-written repo docs — capture the why, never restate the code" — the
  active 2026 project in the ADJACENT agent-written-docs space, and the closest
  match to the ruling's "almost empty repo ... started with idea and stopped
  after a few days"), `dibinraj2003/opendox` (0 stars, pushed 2026-08-10),
  `andymadson/opendox` (1 star, 2025-08-27), `mfbmina/opendox` (2023-01-04) and
  `ritskush1/opendox` (2017-05-22). Neither `opensoft/openDox` nor
  `opensoft/openXdox` exists. None of these blocks `opensoft/openDox` — GitHub
  namespaces repositories per owner — but the ORG name and the adjacent-subject
  project are the facts the naming record's amendment has to state rather than
  the bare word "accepted".
- **"Open source" is aspirational for the existing family.**
  `opensoft/openxFactory` is **private** with **no license**;
  `opensoft/openXwallet`, created days ago, is likewise **private with no
  license**. So a "two layers of opensource" ruling has no in-house precedent
  for what open source concretely means here, and Q9 exists because of it.
- **The runtime precedent is in the house and live.** `xFactory-Hermes-Install`
  runs FastAPI + Postgres on AKS serving two hosts, with `migrations/` (ordered
  SQL, 0001 pinned canonical + additive), per-client instance trees under
  `config/clients/<client>/` validated by openxFactory's validator from a pinned
  checkout, `deploy/compose/` for single-node and `deploy/kubernetes/` for AKS,
  and one lifecycle CLI with 20 verbs. Its README states the discipline worth
  copying: layer contracts are owned by openxFactory and "this repo only
  installs and configures the runtime that implements them."
- **The 2026-09-04 read-only review recommended NOT NOW at medium-high
  confidence**, gating the split on the first domain that stands up an instance,
  on three grounds: the wallet precedent's own trigger (a live consumer) has not
  fired; the move is not byte-identical; five active changes are mid-flight, two
  with open archive gates. The ruling supersedes that recommendation by
  COMMISSIONING the consumer rather than waiting for it, and the proposal should
  record the disagreement rather than silently overwrite it — the review's three
  facts remain true and become the sequencing constraints below.

## Why

<!-- xspec:candidate target=ideation-dashboard -->
Brett has nowhere to put a project. Starting a new project in a new repository
and writing some specs requires cloning the aggregation, choosing a submodule,
placing the document in that repository's ideation tree, and commissioning a row
into a register file that lives in a third repository — and there is no answer at
all for a project that is not one of the eleven repositories the register knows
about. The workbench that would be the natural home for that work is not a home:
it is a reader. Its 49,605 lines of Python and 30,410 lines of front end are
built around the assumption that the record already exists, in a git checkout,
with a lifecycle header, in a corpus whose paths are hardcoded across a third of
its modules. It renders a project as navigation over repositories and cannot let
a project own anything, because a project is a row in a YAML file that the
dashboard is forbidden to write. Meanwhile the product's neutral half is
substantial and finished — a dual-buffer editor with a staleness guard, a chat
bound to the active buffer, branch sessions with commit-per-act and one pull
request, share-session hand-off, model bindings and brokered tokens, abstracts
with a digest-keyed cache, NotebookLM projection — and none of it needs to know
what an OpenSpec change is. That half has a roadmap queueing behind governance
work (an app shell, a mobile surface, context compression, notebook
reconciliation) and no release cadence of its own. Meanwhile the governance half
is what actually makes the thing installable-per-tenant impossible: a
credential-free pod serving a snapshot thawed from git by a nightly lane that
has never succeeded is not something a DomainxFactory install can stand up in a
tenant with its own database. Splitting the two is what makes both possible at
once — an app with users and projects and a database for the first requirement,
and a governance integration that consumes a corpus at a pin for the second.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=ideation-dashboard -->
The app leaves the openxFactory corpus for `opensoft/openDox` — the editor and
canvas, the chat and model plane, the branch-session and pull-request machinery,
accounts, projects, documents, ideas, the NotebookLM integration, the CLI and
the install tooling — and gains what the ruling adds: a database with users and
projects as first-class rows, a runtime that installs and is hosted, and its own
release identity. The openxFactory integration leaves for `opensoft/openXdox` —
the corpus reader and lifecycle projection, the funnel and wheel and lens, the
gate console and its verbs, the record binding and kickoff dispatch, the
snapshot registry, and the nightly, refresh and apply lanes — consuming openDox
as its base and openxFactory's corpus at a commit-and-digest pin. openxFactory
keeps the CORPUS and its GOVERNANCE: `document-lifecycle`, `doc-health`,
`workflow-gate-contract`, the contract families, the ideation estate and all
ideation provenance, plus one new neutral seam contract — the corpus adapter,
which is what makes the departure from the wallet precedent survivable. That
adapter names five operations a governed corpus offers and a reader consumes —
ENUMERATE (documents with a path, a digest, a lifecycle state and topics), READ
and WRITE (bytes, written back through a session the app owns), CLASSIFY (what
state a document is in and which transitions are legal), ASSESS (findings over
the corpus), and ACT (a governance act with an actor and a reason) — and it
replaces the 23 `doc_health` import statements and the tree-layout knowledge
spread across a third of the package with one dependency in one direction.
Before any repository is created, the two-way dependency is broken from its
cheap side: `OutputBoundary` (or its protocol) relocates out of
`ideation_dashboard` into a floor both packages may depend on, retiring the two
lazy back-edges. The byte-identity floor is replaced, because it cannot be met:
the safety property becomes a behavioural one — the 3,927 existing test
functions split with the code and both suites stay green, plus a neutral
conformance corpus for openDox on the wallet extraction's own pattern, so that a
descendant can prove conformance without openxFactory's corpus. The 102-
requirement promoted spec is split by requirement with each successor location
recorded, on the wallet precedent's REMOVED-with-successor discipline rather
than by deletion. Domain descendants follow lazily in the ratified
`<Domainx><Product>` form, pinning openXdox by commit twice, each standing up
one instance with its own database inside the tenant its DomainxFactory install
creates.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=ideation-dashboard -->
- Affected specs: `ideation-dashboard` (REMOVED by SPLIT — 102 requirements
  leave the openxFactory corpus with each requirement's successor location
  recorded in openDox or openXdox); a NEW neutral corpus-adapter seam capability
  (ADDED — the five operations, the pin discipline for a reader that runs over a
  corpus it does not own, and fail-closed behaviour when the corpus cannot be
  resolved); `domain-descendant-boundary` (MODIFIED — a descendant of a RUNTIME
  product: what "profile, never fork" means for a database schema, whether
  migrations may be profiled, and that the descendant is the deployment unit);
  `neutral-product-pin` (MODIFIED — a pin whose consumption is a deployment with
  a migration rather than a file read, so a pin bump has an operation and
  possibly downtime); possibly `doc-health` and `document-lifecycle` depending on
  Q4 and Q1.
- Affected code: openxFactory (`scripts/ideation_dashboard/` all 48 modules,
  `web/` all 40 files, `tests/ideation-dashboard/` all 125 files and
  `tests/ideation_dashboard/` the four-file underscore spelling,
  `scripts/ideation-dashboard-nightly.py`,
  `scripts/validate-ideation-dashboard-contracts.py`, the 4 contract schemas and
  142 examples, `scripts/doc_health/` where the back-edge and the shared reading
  windows live, `contracts/manifest.yaml`, `contracts/README.md`,
  `contracts/CHANGELOG.md`, `README.md`, `.github/CODEOWNERS`, the dashboard
  workflows, `docs/openxdox-naming.md` Amendment 3, and the five governance
  docs); the two NEW repositories in full; the xFactory aggregation
  (`.gitmodules`, gitlinks, `README.md`, `CLAUDE.md`, `project-register.yaml`);
  Omnigent-Install (the inbox and minter, and the installer that would provision
  a per-tenant instance); OpsxFactory (the `dox` workload set and the DNS
  discovery snapshot); codexFactory (two draft Speckit features and the false
  `stack.yaml` digest declaration).
- Not affected, to be verified: the wallet estate; the Hermes runtime, which is
  a precedent rather than a dependency; MedxChart and MedxPractice, whose
  descendant boundaries are the pattern being extended rather than changed.
- Working-rule blast radius: the aggregation's amended working rule #1 —
  "domain-neutral contracts live in openxFactory or in a neutral `open*` product
  repository that openxFactory pins by commit and digest" — already accommodates
  this split, because `split-openxwallet-repo` paid for that amendment. What it
  does NOT yet accommodate is a neutral product that is an APPLICATION rather
  than a contract family, which is the same gap `domain-descendant-boundary`
  needs modifying for.
- Branch protection and required checks: two new repositories each need a
  required check from day one, and openxFactory's dashboard-contract validation
  becomes a consumer gate over pinned tools — the shape
  `openxwallet-consumer-gate` established.
- The 289 KB spec is the largest single artifact in the corpus and its split is
  the highest-risk bookkeeping in the change; 30 archived changes carry deltas
  against it and are immutable records that get ANNOTATED, never edited into
  agreement.
<!-- /xspec:candidate -->

## Folds

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

Two prior records are FOLDED into this topic rather than proceeding alone. Both
were named as folded predecessors on the governing record, and a cross-reference
comment was posted on the second.

**`ideation/staging/openxdox-install-app-provisioning/`** (staged 2026-08-14;
`Staging ID: openxFactory:staging:openxdox-install-app-provisioning`; five open
questions; its own gate — "gated on the opensoft QA dispatch migration
completing" — MET on the 2026-08-15 readiness evidence, exit unraised twenty
days on).

- **What survives, load-bearing:** the two-App separation as a SECURITY
  INVARIANT (the exposed inbox must never hold a contents-write-capable key);
  the finding that GitHub has no app-creates-app API and the App Manifest flow
  is therefore the mechanism; tenant-ownership of the manifest-created App as
  the structural form of sovereignty; the globally-unique-App-name consequence
  and the `openXdox — <tenant>` naming convention; the small dedicated
  apply-workflow repository that keeps the dispatch blast radius minimal; and
  the observation that the tenant's only real decision is the content App's
  repository scope.
- **What changes shape:** its Q1 (contract home — a `credential-contracts`
  delta versus a new `install-app-provisioning` capability) should now be
  answered INSIDE the two-layer change, because a per-tenant app install needs
  provisioning for a database as well as for two GitHub Apps, and answering the
  credential half alone would fix the contract home before the bigger install
  contract exists.
- **What may become moot:** if openDox writes to its own database rather than
  dispatching an apply workflow into a repository, the DISPATCH App may not be
  needed at all. The CONTENT App is still needed the moment git is a publication
  target, so the topic's core does not evaporate — but its framing as
  "provisioning the intent plane's credentials" narrows.
- **Disposition:** the topic folder STAYS staged and is not deleted or rewritten
  by this slice. It is named as a predecessor here, and the eventual proposal
  either carries its five questions or explicitly re-stages what it does not
  carry.

**codexFactory issue #89** — "Plan openXdox standalone project migration", OPEN
since 2026-08-25.

- **What survives:** the topology it recorded (`xFactory → openXdox →
  codexFactory Dashboard`) and its whole obligations list, which reads as a
  checklist for the eventual change: preserve stable project, repository,
  subject and work-item identities; re-parent openXdox out of xFactory; update
  repository and submodule topology; update dashboard projections and
  project-register relationships; migrate policy, ownership and governance
  bindings; record a complete audit trail and a rollback plan. Its scope
  boundary — "leave the future re-parenting operation to a dedicated opsXfactory
  project/workflow" — remains the right home for the mechanical migration.
- **What changes:** #89 scoped a PROJECT-REGISTER re-parenting, one level of
  hierarchy. The ruling makes it a TWO-repository extraction with a runtime and
  a database, so the re-parenting is a consequence of the split rather than the
  whole of it. Its topology diagram also predates the two-layer ruling and needs
  a third level.
- **Disposition:** folded, not duplicated. A cross-reference comment was posted
  on #89 on 2026-09-04 naming issue #656 as the governing record. #89 stays open
  as the codexFactory-side record of the migration operation it describes.

## Sequencing constraints

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

1. **The cycle break lands FIRST and is worth doing alone.** Relocating
   `OutputBoundary` out of `ideation_dashboard` so `doc_health` no longer
   imports into it is a small, forward-compatible change that pays for itself
   whether or not the carve ever happens. Nothing else in this arc can start
   while the two packages import each other.
2. **The corpus adapter is named before any repository is created.** The
   adapter is the boundary; a repository created before the boundary exists will
   have the boundary drawn by whatever `git filter-repo` happened to move.
3. **`serve.py` is the boundary and it cannot be split last.** 6,733 lines
   carrying both the app server and the corpus routes, with three `doc_health`
   imports and five active changes touching the package. Its split is the
   extraction's critical path, not its cleanup.
4. **The active-change wave has to be resolved, waived or explicitly re-homed —
   and one of them deepens the coupling.** `add-nightly-dashboard-refresh` ADDS
   seven requirements to `doc-health` while this topic proposes to separate
   `doc-health` from the dashboard; those two are in tension and the tension is
   a decision, not a merge conflict. Its lane has three worker runs, no
   successes, and no status artifact, so "wait for it to archive" is not a plan
   with a date.
5. **No pin-sync discipline is waived.** A `<Domainx>Dox` descendant pins by
   commit TWICE — gitlink plus pin file, same commit — and the aggregation's
   codexFactory three-in-one-commit rule (gitlink, reusable-workflow sha, test
   PIN) is the standing warning about what happens when a pin moves alone.
6. **Shared-tree discipline.** Every commit in this arc stages explicit paths
   and commits with pathspecs, and checks the current branch before any
   submodule commit.
7. **The naming-record amendment travels with the repository creation, not
   before it.** Amending a `ratified` record ahead of the act it describes would
   leave the record describing a repository that does not exist.

## Idea notes (pre-document, non-documented)

- The brand was already in canon. "The openDox project-first header" is a
  promoted requirement that says the header "SHALL brand as 'Opensoft openDox'".
  So `docs/openxdox-naming.md` rejected `openDox` as taken while the promoted
  spec was already shipping it as the product name — a contradiction that
  existed before this ruling and that nobody caught. Worth checking whether the
  naming record and the dashboard spec have drifted anywhere else. — Added-by:
  Claude Opus 5 (session, Brett's direction) · 2026-09-04
- Three of the four objects the ruling names already exist in some form:
  projects as register rows, documents as the doxBench loaded set, ideas as
  Markdown files with a `Status:` header. The genuinely absent one is the USER,
  and it is absent by design — the promoted spec says in two separate
  requirements that the dashboard authorizes nothing on the hosted actor and
  that identity presence changes no capability verdict. So "we should have
  users" is not a login page; it is an inversion of the authorization model from
  where-the-request-came-from to who-sent-it. That is the largest conceptual
  change in the ruling and the easiest to under-read. — Added-by: Claude Opus 5
  (session, Brett's direction) · 2026-09-04
- A database might make openXdox SMALLER, not bigger. Much of the reader's
  complexity is that it recomputes lifecycle state from files on every serve. If
  documents are persisted with their state, the reader's job narrows toward
  import and export. Or the opposite, if git stays authoritative for governed
  content — in which case openXdox keeps the whole projection and the database
  is a cache. Both readings are live and the persistence brainstorm keeps them
  both. — Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04
- If openXdox becomes the home of "reading a governed corpus", the argument that
  `doc_health` (27,123 lines, openxFactory's own self-gate since
  `adopt-neutral-tooling-home`) should travel with it is uncomfortably strong —
  and openxFactory would then consume its own gate at a pin, exactly as it now
  consumes the wallet validator. That is a much bigger change than the ruling
  asked for. Raised, not proposed. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-09-04
- The NotebookLM projection is per-repo today, with a capacity guard written
  against repositories after the 300-source cap incident. Per project-in-a-
  database it would be per project, which is better shaped and a real migration
  of the guard. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-09-04
- Five descendant names implied and none built. That is correct under the lazy
  rule, but a named-and-absent repository is a thing people create by hand at
  2am, which is why the wallet arc registered names in the naming record and
  created nothing. The same treatment probably applies here. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-09-04
- The three lanes may be the biggest thing the database deletes. Their entire
  purpose is thawing a git corpus into a served snapshot. One of them has never
  succeeded. If the app persists documents, most of that machinery has no
  subject — which is an argument for the database and simultaneously an argument
  for not building any more of the refresh lane first. — Added-by: Claude Opus 5
  (session, Brett's direction) · 2026-09-04

## Conflicts

- **The 2026-09-04 read-only review recommends NOT NOW at medium-high
  confidence, and the ruling proceeds.** The review's three decisive facts are
  all still true: the wallet precedent's own trigger (a live consumer) has not
  fired, codexFactory holds zero lines of the code; the move cannot be
  byte-identical; five active changes are mid-flight with two open archive
  gates. The ruling supersedes the recommendation by commissioning the consumer
  rather than waiting for it. The reconciliation is that steps one through three
  of the sequencing (cycle break, adapter, authority ruling) are worth doing on
  their own terms, so the disagreement is about the CARVE's timing rather than
  about the direction — but until that is written into a proposal, a ratified
  review recommendation and a ruling point opposite ways. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-09-04
- **`docs/openxdox-naming.md` is `Status: ratified` and says `openDox` is
  taken.** It rejected the name and built the `openX` + `dox` argument on the
  rejection ("the splitting `X` distinguishes it from the taken name
  `openDox`"). Claim 6 contradicts it directly. Amendment 3 is the resolution;
  until it is written, the ratified naming record says the opposite of the
  ruling — and the ruling's own descendant spelling (`medXdox`, `CodeXdox` in
  the transcript) contradicts the `<Domainx><Product>` form claim 4 applies. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04
- **The wallet precedent's ratified seam rule points the other way.**
  `split-openxwallet-repo` R3 is the house's only ratified answer to "where does
  the integration seam live", and it says: in openxFactory. Claim 7 departs from
  it by ruling. Both are Brett's rulings, made two weeks apart, and the second
  does not amend the first — so an implementer reading only R3 would draw the
  boundary in the wrong place. The proposal must state the departure rather than
  reason as if R3 applied. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-09-04
- **`add-nightly-dashboard-refresh` deepens the coupling this topic proposes to
  cut.** It is ratified, cross-repo across three repositories, and ADDS seven
  requirements to `doc-health` on behalf of the dashboard. Its archive gate is
  correctly open (13 tasks) and its lane has never produced its status artifact.
  So the corpus-adapter direction and an in-flight ratified change are pulling
  the same seam in opposite directions right now. — Added-by: Claude Opus 5
  (session, Brett's direction) · 2026-09-04
- **`domain-descendant-boundary`'s "created on its first profile, not before"
  describes today's state exactly, and the ruling commissions descendants
  anyway.** The standard's own laziness rule would say `MedxDox` and `codexDox`
  do not exist yet because no domain has a profile. The ruling names them. These
  reconcile if the descendants are NAMES now and repositories later — the
  wallet arc's own treatment — but as spoken, the ruling and the standard
  disagree about when a descendant exists. — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-09-04
- **"Two layers of opensource" has no in-house precedent.** Every `open*`
  repository in this organization is PRIVATE and carries NO license, including
  `openXwallet`, created days ago under a ruling that called it a neutral
  open-source product. So either the family's openness is aspirational and this
  ruling inherits that, or openDox is the first genuinely public repository and
  needs a license, a contribution posture and a public-issue policy that nothing
  else here has. Both readings are consistent with the words. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-09-04

## Open questions

### Q1. What is the database authoritative for, and what stays git-authoritative?

Context: the whole governance estate rests on git being the record — a gate act
is a commit, a ratification is a reviewable diff, doc-health reads a tree, and
external enforcement (branch protection, required checks, codexFactory's
merge-gate floor) can only gate on refs. Adding a database with users, projects,
documents and ideas creates a second store that can disagree, and the
interesting disagreements are the governed ones. For PROJECTS this was already
ruled: D5 of `dashboard-project-scoping` (2026-08-06, promoted as "Local
register authority is declared against the tenant catalog") says the local
register is authoritative for the development plane ONLY until a tenant project
catalog exists, after which it is "a derived, replaceable workstation cache" that
"SHALL NOT override the catalog" — declared, in the topic's own words, "so the
two models cannot fork". openDox's database IS that catalog, so the ruling fires
a trigger already set. Nothing covers documents, ideas, gate acts, sessions,
abstracts or model bindings.
Recommended answer: split by OBJECT CLASS and declare it per class, on D5's own
shape. Governed content (documents carrying a lifecycle status, gate acts,
ratification records) stays git-authoritative, with the database holding a
projection linked by digest so that "which record did the gate read" is an
auditable fact. App state (users, sessions, projects, membership, settings,
threads, abstracts, caches, telemetry) is database-authoritative. An unpublished
document is database-only until the act of publication makes git authoritative
for it. And say so in a contract, because the failure mode of NOT saying it is
the exact fork D5 was written to prevent.
Explanation: a global answer fails in both directions — database-authoritative
breaks `workflow-gate-contract` and `governed-derived-model` and leaves a
ratification a merge gate cannot enforce, while git-authoritative-for-everything
answers the origin complaint with "make a repository first", which is the
complaint. The per-class split is the only reading that satisfies the
requirement and keeps external enforcement intact. Its cost is real and should
be stated: the boundary runs through the middle of the document object, so every
read path has two backends and the first publish is a migration of authority
mid-object-life. That cost is worth paying because the alternative — leaving it
unstated — produces the same split by accident and with no contract to check
against.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q2. What is the runtime shape?

Context: the ruling says "an app that installs and is hosted with a db" and says
nothing about how. The in-house precedent is `xFactory-Hermes-Install` — FastAPI
plus Postgres on AKS, ordered SQL migrations (0001 pinned canonical, additive
after), per-client instance trees validated by openxFactory's validator from a
pinned checkout, a Compose package for single-node and a kustomize adapter for
AKS, and one lifecycle CLI with 20 verbs — live and serving two hosts. The
current dashboard is a Python HTTP server plus a static front end, deployed as a
credential-free pod behind a dox-auth gateway in namespace `dox`, with three
sibling workloads.
Recommended answer: adopt the Hermes install pattern, and say explicitly which
parts are adopted: FastAPI + Postgres, ordered SQL migrations with a pinned
canonical 0001, a single lifecycle CLI, a Compose single-node package and a
kubernetes adapter, a generated (never hand-edited) stack-identity manifest that
downstream repositories digest-pin, and the discipline that the installer
installs and configures while openxFactory owns the contracts.
Explanation: the strongest argument is not elegance, it is that the same
operators already run this shape, the same validators already read its manifests,
and the same tenancy model already works — a per-client tree is exactly what a
per-tenant install needs. Inventing a second runtime idiom in the same
organization costs a second set of runbooks for no gain. The one thing worth
deliberately NOT copying is Hermes's three-layer domain vocabulary, which is its
subject rather than its shape.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q3. Does a domain install always bring its own instance and database, or may it point at a shared one?

Context: "If I install MedxFacotry, then I get a medXdox install running in the
installed tenand with its own db" reads as per-tenant, and every sovereignty
argument in the house supports it. But "its own db" is compatible with at least
three shapes: one instance and one database per tenant (maximum isolation, N
deployments to upgrade, N migration runs, N backup policies — the Hermes shape);
one shared instance with one database per tenant (data isolated, runtime
shared); or one instance and database per DOMAIN with tenants as rows (cheapest,
contradicts the ruling as spoken, and reachable by accident under cost
pressure).
Recommended answer: per-tenant instance AND per-tenant database as the
CONTRACT, with the shared-runtime shape permitted only as a declared,
named deployment profile that a tenant must consent to — never as a silent
operational default. Rule out the tenants-as-rows shape explicitly so nobody
arrives at it under cost pressure.
Explanation: the ruling's words are unambiguous about the database, and physical
tenancy is what makes the sovereignty story in the App-provisioning topic true
rather than rhetorical — the whole point of the manifest flow is that no
opensoft identity holds a key on tenant assets, and a shared runtime holding N
tenants' documents in memory undoes that on the runtime side while satisfying it
on the storage side. Naming the shared shape as a consent-gated profile rather
than banning it keeps a real cost lever available without letting it be taken
quietly.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q4. Where exactly does the corpus-adapter boundary fall, and does doc-health travel with the reader?

Context: twelve of forty-eight modules carry 23 `doc_health` imports; the
back-edge is two lazy imports of `OutputBoundary` from one 377-line module; and
the reader's knowledge of openxFactory's tree layout is spread across a third of
the package as path literals. An adapter with five operations (enumerate,
read/write, classify, assess, act) collapses all of that into one dependency —
but it does not by itself say which side of the seam `doc_health` lives on.
doc-health is 27,123 lines, is openxFactory's own self-gate, and is the natural
implementation of the adapter's CLASSIFY and ASSESS operations.
Recommended answer: name the adapter as a NEUTRAL openxFactory capability — the
seam is a contract, and openxFactory is the layer that owns contracts — and
leave `doc_health` in openxFactory for this wave, with openXdox invoking it as a
PINNED tool inside a required check, on the `neutral-product-pin` "required
check runs the pinned tool at the pinned digest" pattern the wallet split
already ratified. Revisit relocating doc-health only when a second corpus reader
exists that is not openXdox.
Explanation: the adapter has to be a contract somewhere, and putting it in
openxFactory keeps the corpus's own rules with the corpus. Leaving doc-health
put avoids the recursion of openxFactory consuming its own gate at a pin, which
is a coherent design but a much larger change than the ruling asked for and one
whose argument gets strictly stronger with a second consumer — the same shape as
the wallet's Q1, which was correctly carried rather than resolved inside a move.
The cost is that openXdox pins a large openxFactory tool and its pin bumps
become part of openXdox's release cadence.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q5. How does this sequence against the five active `ideation-dashboard` changes?

Context: five active changes carry live deltas against a 102-requirement spec
this topic proposes to split in two. Two have open archive gates and 20 open
tasks between them; one of those is cross-repo across three repositories and
ADDS seven requirements to `doc-health` — deepening the exact coupling the split
must cut — and its lane has three worker runs, zero successes, and has never
produced its status artifact. A third is built but unarchived. Two carry
`target_release: none`. Separately `add-ideation-intent-plane` has been
ratified, part-realized and unpromoted for 43 days, and its target capability is
absent from `openspec/specs/`.
Recommended answer: do NOT wait for the wave to clear, and do not carve into
it either. Take the three preparatory slices first — the cycle break, the
adapter contract, and the Q1 authority ruling — none of which conflicts with any
of the five, all of which are worth doing if the carve never happens. Require
before the CARVE itself: every active change either archived, or explicitly
re-homed with its successor repository named in its own proposal, or waived by a
recorded ruling. Treat the unpromoted `ideation-intent-plane` capability as a
blocking bookkeeping item, because a capability that is ratified and absent from
canon cannot be split by requirement.
Explanation: "wait for the wave" has no date — one gate depends on a lane that
has never succeeded — and "carve now" strands five ratified deltas against a
spec that no longer exists in one piece. The preparatory slices are the only
work that is unconditionally correct, and doing them first shortens the carve
whenever it happens. Naming the re-homing requirement per change is what stops
the carve from silently orphaning a ratified delta.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q6. How do the four residue modules split — `serve.py`, `cli.py`, `workbench.py`, `authoring.py`?

Context: a first reading puts roughly 24.3K LOC on the openDox side (editor,
chat, model plane, sessions, identity, NotebookLM), roughly 15.0K on the
openXdox side (projection, gates, lanes, corpus-shaped views), and leaves 11.4K
in four modules that do BOTH and must be split by function rather than moved:
`serve.py` (6,733 — the app server and the corpus routes in one file, three
`doc_health` imports), `cli.py` (2,456 — neutral verbs and governance verbs in
one argument parser), `workbench.py` (1,575 — neutral manifests and notebooks
plus funnel meaning, four `doc_health` imports), `authoring.py` (329 — neutral
header machinery over a governed vocabulary, co-authoritative with
`doc_health.corpus.STATUS_SCAN_LINES`).
Recommended answer: split all four by function, and do `serve.py` FIRST rather
than last — openDox keeps the server, the static and canvas routes, the chat and
model routes and `/capabilities`; openXdox contributes the snapshot, `/source`
and projection routes as a registered route module over an app-server extension
point openDox exposes. `cli.py` splits the same way, with openXdox contributing
subcommands. `workbench.py`'s manifests and notebooks go to openDox and its
funnel semantics to openXdox. `authoring.py`'s machinery goes to openDox and its
required-field vocabulary comes from the adapter's CLASSIFY operation.
Explanation: the extension-point shape is what makes the two layers composable
at all — without it the "integration layer" has to fork the server, which is a
fork rather than a profile and would break the same rule
`domain-descendant-boundary` applies one level down. Doing `serve.py` first is
uncomfortable because it is the most-changed file in the package, but every
other split decision is downstream of knowing whether the extension point
exists.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q7. Do descendants always pin openXdox, or may a domain pin openDox directly?

Context: the ruling says descendants pin openXdox, and for the
DomainxFactories that is right — they need the governance interpretation. But a
consumer who wants the app without the OpenSpec funnel (a clinic wanting a
document workbench) would want openDox. If only openXdox is pinnable, openDox
has exactly one consumer and its independence is nominal, which weakens the
whole two-layer rationale.
Recommended answer: BOTH are pinnable, and the descendant declares WHICH layer
it pins. `domain-descendant-boundary`'s modification grows a one-field
declaration rather than a second pattern. DomainxFactory descendants pin
openXdox by default because that is what the ruling says they need; a non-factory
consumer pins openDox.
Explanation: a neutral product with one possible consumer is not a neutral
product, and the two-layer split is only worth its cost if openDox can be
consumed on its own. The declaration is cheap — the descendant standard already
requires a pin file naming the product, so naming the LAYER is one more key —
and it makes the openDox/openXdox boundary testable: if nothing can pin openDox
alone, the boundary is in the wrong place.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q8. Does openDox own user accounts, or delegate identity to the gateway?

Context: the workbench today has three identity concepts and none is an account.
`hosted_actor` is display-only, resolved per request from a gateway-stamped
header, `null` when absent, and the promoted spec says in two separate
requirements that the dashboard authorizes nothing on it and that identity
presence changes no capability verdict; logout already delegates to a
gateway-owned `/logout`. The local actor exists for gate actions. Write
authority is a property of the loopback console verdict — where the request came
from — not of who sent it.
Recommended answer: openDox owns an ACCOUNT (a durable principal with
membership and ownership of projects and documents) and delegates
AUTHENTICATION to an identity provider through the existing gateway pattern. The
account is the thing a project's owner column points at; the gateway remains the
authority on who is presenting. Do not build password storage, reset flows or
invitations in a product whose subject is documents.
Explanation: the ruling's "we should have users and projects" needs an account
object — a project cannot have an owner otherwise — but nothing in it requires
openDox to become an identity provider, and the gateway delegation is live,
proven, and already how logout works. Splitting account-from-authentication also
keeps the per-tenant install honest: the tenant's own IdP is what a sovereign
install should trust. The cost is that an account row's link to a gateway
identity is a mapping that has to be administered, and the first-user bootstrap
needs designing.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q9. What does "open source" concretely mean here — license, visibility, contribution posture?

Context: measured 2026-09-04, `opensoft/openxFactory` is PRIVATE with NO
license, and `opensoft/openXwallet` — created days ago as a neutral open-source
product — is likewise private and unlicensed. So the existing `open*` family's
openness is a naming convention rather than a legal or operational posture. The
ruling says "two layers of opensource".
Recommended answer: decide the license and visibility AT REPOSITORY CREATION and
record it in the change, not later. Recommend a permissive license (Apache-2.0
for the patent grant, given that this is an organization shipping governance
tooling) and PUBLIC visibility for openDox specifically, with openXdox's
visibility a separate decision that can stay private without contradicting the
ruling, since its subject is openxFactory's own governance. Do not make either
public without a contribution and security-report policy, because a public
repository with no policy is a support obligation nobody agreed to.
Explanation: this is Brett's decision, not a recommendation the topic can
settle, but it must be ASKED before the repository exists — retro-licensing a
repository with outside contributions is materially harder than choosing at
creation, and the whole family's current posture shows how easily "open" stays
nominal by default. Naming openDox as the one that is genuinely public is the
minimum that makes the two-layer split mean something to anyone outside.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q10. Who owns `opensoft/openDox`, and what do the measured name collisions require of Amendment 3?

Context: neither `opensoft/openDox` nor `opensoft/openXdox` exists. A GitHub
ORGANIZATION named `opendox` exists (created 2026-03-20, one public repo
`opendox/dox` on an unrelated Amazon-analytics subject, last pushed 2026-05-31).
Six repositories named `opendox` exist; the largest is `noitran/opendox` (22
stars, a Laravel OpenAPI package, dormant since 2022) and the one in the
ADJACENT subject space is `fum4/opendox` (0 stars, pushed 2026-07-16, "Spec +
CLI + skill for agent-written repo docs"). GitHub namespaces repositories per
owner, so none of these blocks `opensoft/openDox` — but the org name is
unavailable and an active project in the neighbouring problem space carries the
same word.
Recommended answer: create both repositories under `opensoft`, matching every
other product in the family, and do NOT pursue the `opendox` organization.
Amendment 3 must state the collision facts as measured — the org, the six
repositories with the two that matter named and dated, and the fact that per
-owner namespacing makes the repository name available — plus Brett's acceptance
of the adjacent-subject overlap, and it must NOT repeat the bare claim that the
name is "taken", which is what the original record got wrong by not measuring.
Explanation: `opensoft` ownership is what every consumer's pin, CODEOWNERS entry
and submodule URL already assumes, and a separate organization would fragment
the review-authority and ruleset estate for a name nobody can have anyway. The
amendment's value is the measurement: the original record's one-word "taken"
justified a naming decision for three weeks without anyone checking what was
actually taken, and an amendment that repeats the same style of claim would fail
the same way.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q11. What happens to the promoted `ideation-dashboard` capability — split by requirement, or REMOVED with two successors?

Context: `ideation-dashboard` is a promoted capability with 102 requirements and
472 scenarios in a 289 KB spec, 30 archived changes carrying deltas against it,
and 5 active. `split-openxwallet-repo` established this repository's only
precedent — its first `## REMOVED Requirements` blocks and its first capability
exit — where two whole capabilities left with their successor location recorded.
Here one capability splits in two, which is a shape the corpus has never seen.
Recommended answer: REMOVE `ideation-dashboard` from the openxFactory corpus
with a per-requirement successor map — each of the 102 requirements named with
its destination repository and successor capability id — and let the two new
repositories promote their own capabilities from that map rather than inheriting
the id. Do not keep a stub `ideation-dashboard` in openxFactory.
Explanation: a per-requirement map is the only artifact that makes the split
auditable, and it substitutes for the byte-identity floor the extraction cannot
have: instead of proving the bytes did not change, prove every requirement has
exactly one home. Keeping a stub would leave openxFactory owning requirements
about code it does not hold, which is the condition the split exists to end. The
cost is that the map is large and has to be authored by hand, and that 30
archived changes then cite a capability that no longer exists in this corpus —
which is annotation work on immutable records, exactly as the wallet arc did.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q12. What replaces the byte-identical floor as the extraction's safety property?

Context: `split-openxwallet-repo`'s ratified floor was a pure move — eight
artifact digests matching openxFactory HEAD before the tag was cut, with exactly
one permitted prose carve-out — "because a move whose diff is not provably empty
cannot be bisected against". A two-repository split of a package whose modules
import a sibling package that imports back cannot meet that, and neither can a
split that adds a database.
Recommended answer: a BEHAVIOURAL floor in three parts. (1) The 3,927 existing
test functions split with the code, both suites stay green, and the collection
counts on both sides sum to the pre-split count — a number pinned by test the
way `pytest-suite.yml` already pins this repository's collection triple. (2) A
neutral conformance corpus for openDox, on the wallet extraction's pattern of
positives plus negative confirmations, so a descendant can prove conformance
without openxFactory's corpus. (3) A named equivalence run: the same corpus
served by the pre-split tree and by the two post-split repositories produces the
same snapshot digests. Each part gets its own evidence line, and none of them is
"the tests passed".
Explanation: the safety property has to be something a reviewer can check
mechanically, because that is the entire function the byte-identity floor
performed. Test-count arithmetic catches silently dropped tests, which is the
most likely way a 125-file suite loses coverage in a carve; the conformance
corpus is what makes openDox independently verifiable rather than
verifiable-only-against-this-repository; and the snapshot equivalence run is the
closest available analogue to "the diff is provably empty" for a system whose
output is a projection. The cost is that all three have to be built before the
carve, which is the point.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q13. Which layer does the intent plane land in, and does its unpromoted capability block the split?

Context: `add-ideation-intent-plane` was ratified 2026-07-23 and is
part-realized, and its target capability `ideation-intent-plane` is ABSENT from
`openspec/specs/` — ratified and unpromoted for 43 days. Its realization is the
apply lane (`intent_apply_lane.py`, one dispatch ever, 2026-08-15), the intent
inbox and the dispatch-token minter in Omnigent-Install, and the one workflow the
inbox may dispatch in the aggregation. That machinery exists to write governed
content into a repository from a credential-free serving tier.
Recommended answer: the intent plane is openXdox — its whole subject is
applying governed intents to an openxFactory-shaped corpus — and its unpromoted
capability is a BLOCKING bookkeeping item for the split, not a separate concern:
promote it (or record its non-promotion deliberately) before the per-requirement
successor map of Q11 is authored, because a capability that is ratified and
absent from canon cannot be assigned a successor home.
Explanation: the plane reads as neutral at first glance — dispatch a token,
apply a change — but every part of it is shaped by what it applies to: an
allowlist of governed repositories, a content App scoped to a corpus, a lane
that runs a corpus writer. And leaving it unpromoted through a split would lose
the only record of what was ratified, since the archived change would then be
the sole home of requirements nobody promoted. Separately, the database may
delete much of the plane's reason to exist (Q1), so promoting it first also
makes that consequence visible instead of silently obsoleting a ratified change.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

## Exit

One OpenSpec change on the `split-openxwallet-repo` shape, adapted for a
two-repository, non-byte-identical extraction of an application rather than a
contract family. It declares a code surface across at least six repositories —
openxFactory, the two new repositories, the xFactory aggregation,
Omnigent-Install and codexFactory — so under `release-realization` it archives
only on merged plus green realization evidence, never on landing.

What the change would carry: the REMOVED-by-split delta on `ideation-dashboard`
with a per-requirement successor map (Q11); the ADDED neutral corpus-adapter
seam capability; the MODIFIED `domain-descendant-boundary` delta for a
descendant of a runtime product with a schema and migrations; the MODIFIED
`neutral-product-pin` delta for a pin whose consumption is a deployment;
Amendment 3 to `docs/openxdox-naming.md` carrying the measured collision facts;
the declared authority boundary from Q1; and the three-part behavioural floor
from Q12 in place of byte identity. Speckit features follow per phase, on the
convener's standing rule that OpenSpec ratifies the boundary and Speckit builds
it: break the import cycle; name and land the corpus adapter; split `serve.py`
and the other three residue modules by function behind an app-server extension
point; scaffold and carve the two repositories and prove the behavioural floor;
consume and shed in openxFactory; aggregate the submodules; then a first
descendant, lazily, when a domain has a profile.

Three preparatory slices are worth taking BEFORE the proposal and do not depend
on it: the cycle break (relocate `OutputBoundary` so the two packages stop
importing each other), the corpus-adapter contract, and Brett's ruling on the
Q1 authority boundary. All three are unconditionally correct — they are the
debts that make the current code hard to change — and each shortens the
extraction whenever it happens.

What must be true first: Brett rules Q1 (the authority boundary), Q2 (the
runtime shape) and Q3 (per-tenant or shared), because the three of them together
decide whether openXdox keeps the projection or becomes an importer, and
therefore where the boundary of Q6 actually falls. Q9 and Q10 must be answered
before either repository is CREATED rather than before the proposal is written.
Q5's active-change wave must be resolved, re-homed or waived by a recorded
ruling before the carve phase, and the unpromoted `ideation-intent-plane`
capability of Q13 must be promoted or its non-promotion recorded before the
per-requirement map is authored. Every remaining question must carry a
disposition other than `open`, or be explicitly carried into the change as a
council question — Q4 and Q7 are the two expected to travel rather than resolve.
