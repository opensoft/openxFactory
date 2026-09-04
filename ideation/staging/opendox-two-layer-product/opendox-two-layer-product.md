# Staged: openDox and openXdox — two open-source layers, an installable app with a database, and domain descendants that hold each domain's mapping

Status: staged
Kind: capability-proposal
Summary: Brett ruled on 2026-09-04 that the document-and-ideation workbench
becomes TWO open-source repositories — `opensoft/openDox`, a hosted installable
app with its own database whose objects are users, projects, documents and
ideas, and `opensoft/openXdox`, openDox tuned for openxFactory — with domain
descendants (`MedxDox`, `codexDox`, `LedgerxDox`, `AdxDox`) pinning openXdox and
a DomainxFactory install standing one up in the tenant with its own database.
Within the hour he ruled four more: the database owns IDENTITY AND COORDINATION
while git owns GOVERNED ARTIFACTS written back only through the apply lane; the
runtime REUSES the Hermes install pattern with OIDC through the Keycloak broker;
ONE INSTANCE AND ONE DATABASE PER TENANT, ALWAYS, in both operating cases; and
openDox DEFINES the corpus-adapter interface while openXdox IMPLEMENTS it, with
the dependency pointing one way. His Q5 direction then replaced the two-way
module split with a THREE-LAYER TEST — openDox must be useful alone to a student
or a lab assistant, openXdox holds the machinery common to how Medx, Ledgerx and
Adx each map onto the workbench, descendants hold the domain-specific mapping —
making the per-module assignment design work this topic carries. Two questions
remain for Brett: sequencing against the five active `ideation-dashboard`
changes, and repository ownership, license and the measured `opendox`
name collisions.
Topics: opendox, openxdox, medxdox, codexdox, ledgerxdox, adxdox,
ideation-dashboard, doxbench, repo-split, two-layer-product, three-layer-test,
domain-mappings, domain-descendant-boundary, neutral-product-pin,
corpus-adapter, tenant-install, per-tenant-database, keycloak-broker, users,
projects, notebooklm, git-integration, openxdox-naming, doc-health,
document-lifecycle, governed-derived-model, install-provisioning, feat-request
Repository context: SPLIT across four homes on purpose. `opensoft/openDox` (to
be created) owns the APP and DEFINES the corpus-adapter interface — accounts,
projects, documents, ideas, the editor and chat, the model plane, the branch
session, the NotebookLM connection, the install and the database schema — and
must be useful with no openxFactory anywhere. `opensoft/openXdox` (to be
created) IMPLEMENTS that interface and owns the machinery common to how the
domains map onto the workbench. openxFactory keeps the CORPUS and its
GOVERNANCE — `document-lifecycle`, `doc-health`, `workflow-gate-contract`,
`governed-derived-model`, `roles-authority-model`, the contract families, the
ideation estate and all provenance — plus the neutral seam contract, and
consumes both products at pins. The xFactory aggregation gains submodules. The
DomainxFactories gain `<Domainx>Dox` descendants holding their own domain
mapping, created lazily, each the deployment unit for one tenant instance.
Staging ID: `openxFactory:staging:opendox-two-layer-product`
Captured: 2026-09-04
Source: Brett Heap's rulings of 2026-09-04, in session, recorded verbatim on the
governing record `opensoft/openxFactory` issue #656 — filed as an issue
precisely so they live outside a chat transcript. The founding ruling is two
utterances: the origin complaint ("we do not have a place to store projects ... I
think we need to make this an app that installs and is hosted with a db. we
should have users and projects and can expand the feature set") and the topology
("openDox is a dead project ... lets use that name as the core opensource repo.
we have two layers of opensource openDox and openXdox. The openXdox is openDox
tuned for use with openXfactory. we will make openDox work to just manage
documents and ideas. it will keep the integration with git and notebook lm etc
and have all tools that help for document management and ideation. then openXdox
will integrate with openXfactory"), plus the descendant sentence from earlier in
the same sitting ("We then further pin that down to medxDox and CodeXdox for use
in those domain factories. If I install MedxFacotry, then I get a medXdox
install running in the installed tenand with its own db"). Four further rulings
(Q1 the authority boundary at 15:24Z, Q2 the runtime at 15:31Z, Q3 the instance
topology at 15:32Z, Q4 the seam at 15:34Z) and one direction (Q5 the three-layer
test at 15:48Z) followed the same afternoon and are carried as claims below. The
inventory the claims rest on was measured against `origin/main`
`6ced5d1d`/`bc1bd4ee` the same day by the read-only openXdox review (lane
openxfactory-smalls). Origin provenance is the `ideation-dashboard` brainstorm,
the doxBench packet, and the `openxdox-install-app-provisioning` staged topic,
which this topic folds.
Target capabilities: REMOVED (by SPLIT) `ideation-dashboard` from the
openxFactory corpus, with the successor location of each requirement recorded in
`opensoft/openDox`, `opensoft/openXdox` or a named descendant; ADDED a neutral
corpus-adapter seam capability in openxFactory (the interface openDox declares
and openXdox implements — how documents are listed, read, written back and
checked — plus the pin discipline for a reader running over a corpus it does not
own, and fail-closed behaviour when the corpus cannot be resolved); ADDED a
neutral domain-mapping declaration capability (what a `<Domainx>Dox` descendant
must declare to map its domain onto the workbench: artifact kinds, their
lifecycle vocabulary, the acts and their gates, the evidence classes, the
promoting authorities); MODIFIED `domain-descendant-boundary` (a descendant of a
RUNTIME product with a schema and migrations, and the descendant as the
per-tenant deployment unit — which no existing descendant precedent is);
MODIFIED `neutral-product-pin` (a pin whose consumption is a deployment with a
migration rather than a file read). Possibly MODIFIED `document-lifecycle` (if
the lifecycle vocabulary becomes parameterized rather than fixed) and
`governed-derived-model` (if the model/scenario workbench needs a contract
surface it does not have); both carried as design work rather than declared. The
two ADDED capabilities are deliberately NOT fenced as `xspec:candidate` targets
below: neither exists in `openspec/specs/` or in any active change's `specs/`,
so fencing them would emit tag-hygiene unresolved-target findings. The fenced
blocks target `ideation-dashboard`, the capability this topic exists to
relocate.

## Claims

The 2026-09-04 rulings are settled context. These claims are constraints on the
eventual proposal, not questions in it; the open questions below are what the
rulings did NOT settle.

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
   integrate with openXfactory" — refined by claim 15 into the machinery COMMON
   to the domain mappings.
4. **Domain descendants pin openXdox, in the `<Domainx><Product>` form.**
   `MedxDox`, `codexDox`, `LedgerxDox`, `AdxDox`, `OpsxDox` — the same casing
   scheme `MedxChart`, `MedxPractice`, `LedgerxWallet` and `MedxAvatar` already
   use, ratified as a general rule by `domain-descendant-boundary`. Not
   `medXdox`, which would be a third casing scheme in the org; the ruling's own
   transcript spells it both ways and the ratified form governs.
5. **A DomainxFactory install brings up its descendant, in the tenant, with its
   own database.** "If I install MedxFacotry, then I get a medXdox install
   running in the installed tenand with its own db."
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
11. **RULED Q1 (15:24Z) — the database owns identity and coordination; git owns
    governed artifacts.** Users, memberships, projects, the
    project-to-repository mapping, sessions and unsaved drafts live in the
    openDox database. Specs, changes, ideation documents and contracts stay in
    git, read from repositories and **written back only through the apply
    lane**. Every existing gate therefore stays valid — doc-health still reads a
    tree, OpenSpec still validates packets, the PR checks still gate on refs —
    and the database is **disposable relative to the corpus**. REJECTED:
    documents in the database with git as an export; and the hybrid where ideas
    live in the database until promoted.
12. **RULED Q2 (15:31Z) — reuse the Hermes install pattern.** FastAPI +
    Postgres, deployed the way `xFactory-Hermes-Install` is (live on AKS since
    2026-07-19), with **OIDC through the Keycloak broker** being adopted in QA.
    The OpsxFactory `dox` workload set — `dox-auth`, `dox-dashboard`,
    `dox-intent-inbox`, `dox-token-minter` — is the deployment shape it grows
    into. REJECTED: bolting a database onto today's stdlib `serve.py` monolith;
    and a new full-stack platform.
13. **RULED Q3 (15:32Z) — one instance and one database per tenant, always.**
    Every domain-factory install brings its own descendant instance and its own
    database inside the tenant, whether Opensoft operates it (the credential
    runbook's Case A, operator vault) or the tenant does (Case B, tenant
    provider). **No cross-tenant data ever shares a store.** REJECTED: a shared
    multi-tenant openDox with row-level isolation; and a per-tenant default with
    a pooled option for operator-hosted tenants — so a "consent-gated shared
    profile" is explicitly off the table. Consequence: the descendant IS the
    deployment unit.
14. **RULED Q4 (15:34Z) — openDox defines the corpus-adapter interface;
    openXdox implements it.** openDox declares how documents are listed, read,
    written back and checked, with **no knowledge of OpenSpec or doc-health**.
    openXdox implements that interface over openxFactory's corpus and check
    families. The two back-imports from `scripts/doc_health/` into
    `ideation_dashboard.boundary` (`derive_possibles.py:857`,
    `ideation_readiness.py:1351`) move into a **small neutral module both sides
    depend on**. **The dependency points ONE way: openXdox depends on openDox,
    never the reverse.** REJECTED: openDox pinning doc-health as a library,
    which inverts the layering; and openXdox as a tuned copy with no shared
    interface, which guarantees divergence and makes every fix land twice.
15. **DIRECTION Q5 (15:48Z) — a THREE-layer test, and the per-module assignment
    is design work under it.** Verbatim: *"we want to make openDox useful on its
    own, it shoudl be able to still manage docs and do brainstorming and connect
    to notebook lm. it is domain neutral and external from openXfactory. we need
    to make sure openXfactory brings in the core machinery to map to domains. we
    need to think how a patient managment and research maps to the openXdox. and
    how a finacial simulations or accounting questions would map in
    ledgerXfactory. same for marketing analysis in adXfactory. what is core to
    these that we pull out and put in openXdox. and what can pull up to openDox
    that does not rely on openXfactory. and what do we need to try to pull from
    openXdox to openDox to make openDox more useful as a braintorming and
    reserch analysis tool. a student could use openDox or a lab assistant. so we
    want that to still be useful on its own"*. Three settled consequences:
    (a) **openDox must be useful ALONE** to a student or a lab assistant —
    manage documents, brainstorm, do research analysis, connect to NotebookLM —
    domain-neutral and external to openxFactory, and the module test is "would
    someone with no notion of factories, gates or tenants use it?", with an
    active obligation to find what to PULL UP from today's dashboard to make
    openDox a better brainstorming and research-analysis tool; (b) **openXdox
    holds the machinery COMMON** to how MedxFactory (patient management and
    research), LedgerxFactory (financial simulations, accounting questions) and
    AdxFactory (marketing analysis) each map onto the workbench, and those three
    mappings must be worked explicitly to extract that core; (c) **descendants
    hold the domain-specific mapping**. The per-module assignment is therefore
    NOT ruled module by module — it is design work carried by the brainstorm set
    and this topic.

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
  in one 377-line module, imported lazily in two places** — which is why Q4's
  "move them to a small neutral module" is a small change, and why the
  dependency can be made one-way before any repository exists.
- **The reader's knowledge of openxFactory's tree is spread across a third of
  the package.** Path literals: `ideation/staging` in 16 modules, `contracts/`
  in 15, `docs/` in 9, `ideation/brainstorm` in 8, `openspec/changes` in 7,
  `ideation/dashboard` in 6, `openspec/specs` in 2. Under Q4 these become the
  adapter's openXdox-side implementation surface rather than a dependency to
  remove.
- **The three domain mappings rest on measured, ratified facts.** Per
  `docs/domain-instantiation-pre-run-questionnaire.md`,
  `contracts/policies/layer-vocabulary.yaml` and `docs/governed-derived-model.md`:
  MedxFactory — Patient Hermes / Care Organization Hermes, objects "patient and
  care context", sensitive acts care-affecting action, patient privacy, clinical
  authority, derived family Dream Object / Simulation Scenario with **ratified
  templates** at the `governed` tier. LedgerxFactory — Engagement Hermes / Firm
  Hermes, objects "ledger, filing, report, transaction, obligation", sensitive
  acts money movement, filing accuracy, audit, compliance, derived family
  Counterparty Health Profile / Financial Scenario (staged). AdxFactory —
  Advertiser Hermes / Marketing Organization Hermes, objects "campaign,
  audience, offer, channel, account", sensitive acts brand risk, external send,
  paid spend, privacy, attribution, derived family Persona / Campaign Simulation
  at the `calibrated` tier. codexFactory — Project Hermes / Engineering
  Organization Hermes, objects "feature, repo, PR, release, incident".
- **The model/scenario workbench does not exist anywhere in the 80K lines.** All
  three domains declare a `governed-derived-model` family — a `model` member and
  an optional `scenario` member, five invariants at `governed` (non-authoritative
  by construction, full provenance, read-only truth store with zero action
  authority, declared scope with no cross-scope data without review, human-gated
  promotion whose output enum is exactly
  `hypothesis_proposed | no_signal | discarded`), six dials, and a named human
  promoting authority — and there is no UI for any of it. This is the largest
  genuinely missing piece of the openXdox common core.
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
  2026-08-15T01:22:04Z, success — which Q1 promotes to the ONLY governed write
  path. The nightly image-refresh worker has **three runs, zero successes** and
  has never produced `refresh-status.json`. The snapshot lane is green.
  OpsxFactory declares the four `dox` workloads at
  `workflows/aks-administration.yaml:412-431`; the `openxdox` DNS A record
  exists on the live zone and is ungoverned (`prohibited_until_realized`, zone
  `reachable_ungoverned`).
- **The five active changes, and why sequencing is a real constraint.**
  `add-nightly-dashboard-refresh` (ratified 2026-08-25, re-ratified 2026-09-04;
  ADDED+MODIFIED on `ideation-dashboard` PLUS 7 ADDED requirements on
  `doc-health`; cross-repo across three repositories; archive gate OPEN, 13 open
  tasks) — note that it DEEPENS the exact coupling Q4 rules should point one
  way; `retire-doxbench-chat-turn-v1` (ratified 2026-09-01; archive gate open, 7
  open tasks; schema bytes already moved at `contract-v3.0`);
  `add-doxchat-model-intake` (built 2026-08-26, not archived);
  `add-composed-view-authoring` and `add-lens-document-selection` (both
  `target_release: none`). Plus `add-ideation-intent-plane`, ratified
  2026-07-23, part-realized, whose target capability `ideation-intent-plane` is
  **absent from `openspec/specs/`** — ratified and unpromoted for 43 days, and
  now the capability behind Q1's only write path.
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
  for what open source concretely means here, and Q7 exists because of it.
- **The runtime precedent Q2 adopts.** `xFactory-Hermes-Install` runs FastAPI +
  Postgres on AKS serving two hosts, with `migrations/` (ordered SQL, 0001
  pinned canonical + additive), per-client instance trees under
  `config/clients/<client>/` validated by openxFactory's validator from a pinned
  checkout, `deploy/compose/` for single-node and `deploy/kubernetes/` for AKS,
  and one lifecycle CLI with 20 verbs. Its README states the discipline worth
  copying: layer contracts are owned by openxFactory and "this repo only
  installs and configures the runtime that implements them."
- **The 2026-09-04 read-only review recommended NOT NOW at medium-high
  confidence**, gating the split on the first domain that stands up an instance,
  on three grounds: the wallet precedent's own trigger (a live consumer) has not
  fired; the move is not byte-identical; five active changes are mid-flight, two
  with open archive gates. The rulings supersede that recommendation by
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
with a digest-keyed cache, bounded knowledge packets over a selected document
set, a keyword set-builder, a NotebookLM connection — and a student or a lab
assistant would use every one of those with no notion of factories, gates or
tenants, if they could reach them. They cannot: those tools are filed as
governance features of a corpus reader. And the third layer is the reason the
split cannot be deferred: what openxFactory brings to a domain — a lifecycle, a
gate loop, an evidence trail, a model-and-scenario pair, a role projection, a
review lane — is machinery MedxFactory, LedgerxFactory and AdxFactory each need
in the same shape with different nouns, and today it exists once, hardcoded to
one domain's vocabulary, inside a reader that no domain can install.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=ideation-dashboard -->
The app leaves the openxFactory corpus for `opensoft/openDox` — the editor and
canvas, the chat and model plane, the branch-session and pull-request machinery,
accounts, projects, documents, ideas, the NotebookLM connection, the CLI and the
install tooling — and gains what the rulings add: a Postgres database owning
identity and coordination (users, memberships, projects, the
project-to-repository mapping, sessions, unsaved drafts), a FastAPI runtime on
the Hermes install's deployed shape with OIDC through the Keycloak broker, one
instance and one database per tenant in both operating cases, and the
corpus-adapter INTERFACE as openDox's own declaration — how documents are
listed, read, written back and checked, with no knowledge of OpenSpec or
doc-health. A named pull-up wave moves the research-analysis tools up with it:
the bounded-knowledge and compression stack, the abstract store and its
generation surface, the lens set-builder, and the NotebookLM connection's
generic half — everything a lab assistant needs and nothing that mentions a
stage name. The openxFactory integration leaves for `opensoft/openXdox`, which
IMPLEMENTS that interface over openxFactory's corpus and check families and owns
the machinery common to the three domain mappings: the lifecycle engine, the
gate-and-commission loop, the evidence-and-provenance surface, the model/
scenario workbench that today exists nowhere, the role-and-authority projection,
and the review lane. The two `doc_health` back-imports move into a small neutral
module both sides depend on, and the dependency points one way for the first
time. Governed content does not move into any database: specs, changes, ideation
documents and contracts stay in git, read from repositories and written back
only through the apply lane — so doc-health still reads a tree, OpenSpec still
validates packets, the PR checks still gate on refs, and the database stays
disposable relative to the corpus. openxFactory keeps the CORPUS and its
GOVERNANCE plus two new neutral seam contracts: the corpus adapter, and the
domain-mapping declaration a `<Domainx>Dox` descendant must carry — artifact
kinds, lifecycle vocabulary, acts and gates, evidence classes, promoting
authorities. The byte-identity floor is replaced, because it cannot be met: the
safety property becomes behavioural — the 3,927 existing test functions split
with the code with post-split collection counts summing to the pre-split count,
a neutral conformance corpus for openDox on the wallet extraction's own pattern,
and a named equivalence run proving the same corpus yields the same snapshot
digests before and after. The 102-requirement promoted spec is split by
requirement across three destinations with each successor location recorded.
Descendants follow lazily in the ratified `<Domainx><Product>` form, each the
deployment unit for one tenant instance with its own database.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=ideation-dashboard -->
- Affected specs: `ideation-dashboard` (REMOVED by SPLIT — 102 requirements
  leave the openxFactory corpus with each requirement's successor location
  recorded in openDox, openXdox or a named descendant); a NEW neutral
  corpus-adapter seam capability (ADDED — the interface openDox declares and
  openXdox implements, the pin discipline for a reader over a corpus it does not
  own, and fail-closed behaviour when the corpus cannot be resolved); a NEW
  neutral domain-mapping declaration capability (ADDED — what a descendant must
  declare to map its domain onto the workbench); `domain-descendant-boundary`
  (MODIFIED — a descendant of a RUNTIME product: what "profile, never fork"
  means for a database schema, whether migrations may be profiled, and that the
  descendant is the per-tenant deployment unit); `neutral-product-pin`
  (MODIFIED — a pin whose consumption is a deployment with a migration, so a pin
  bump has an operation and possibly downtime); possibly `document-lifecycle`
  (if the taxonomy becomes parameterized) and `governed-derived-model` (if the
  model/scenario workbench needs a contract surface).
- Affected code: openxFactory (`scripts/ideation_dashboard/` all 48 modules,
  `web/` all 40 files, `tests/ideation-dashboard/` all 125 files and
  `tests/ideation_dashboard/` the four-file underscore spelling,
  `scripts/ideation-dashboard-nightly.py`,
  `scripts/validate-ideation-dashboard-contracts.py`, the 4 contract schemas and
  142 examples, `scripts/doc_health/` where the two back-imports and the shared
  reading windows live, `contracts/manifest.yaml`, `contracts/README.md`,
  `contracts/CHANGELOG.md`, `README.md`, `.github/CODEOWNERS`, the dashboard
  workflows, `docs/openxdox-naming.md` Amendment 3, and the five governance
  docs); the two NEW repositories in full; the xFactory aggregation
  (`.gitmodules`, gitlinks, `README.md`, `CLAUDE.md`, `project-register.yaml`);
  Omnigent-Install (the inbox, the minter, and the installer that provisions a
  per-tenant instance and its database); OpsxFactory (the `dox` workload set,
  now per tenant, and the DNS discovery snapshot); codexFactory (two draft
  Speckit features and the false `stack.yaml` digest declaration); and each
  DomainxFactory that stands up a descendant.
- New operating surface created by Q3: N runtime deployments, N databases, N
  migration runs per release, N backup and restore policies, N credential sets,
  in both the operator-hosted and tenant-hosted cases. The Hermes install pays
  exactly this bill today, which is the practical force behind Q2's pattern
  reuse.
- The apply lane is promoted by Q1 from a demo to the ONLY governed write path,
  with one dispatch in its entire history — so its hardening is a precondition
  of the split rather than a follow-up, and `ideation-intent-plane`'s
  unpromoted capability becomes load-bearing bookkeeping.
- Working-rule blast radius: the aggregation's amended working rule #1 already
  accommodates a neutral `open*` product openxFactory pins. What it does NOT yet
  accommodate is a neutral product that is an APPLICATION with a schema rather
  than a contract family — the same gap `domain-descendant-boundary` needs
  modifying for.
- Branch protection and required checks: two new repositories each need a
  required check from day one, and openxFactory's dashboard-contract validation
  becomes a consumer gate over pinned tools — the shape
  `openxwallet-consumer-gate` established.
- The 289 KB spec is the largest single artifact in the corpus and its
  three-way split is the highest-risk bookkeeping in the change; 30 archived
  changes carry deltas against it and are immutable records that get ANNOTATED,
  never edited into agreement.
<!-- /xspec:candidate -->

## Design work carried under the Q5 direction

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

The per-module assignment is explicitly NOT ruled. It is carried here and in the
brainstorm packet as design work under the three-layer test, and these are its
current findings — a first pass, to be contested rather than implemented.

**A three-column first pass over the 48 modules** (LOC measured; see
`ideation/brainstorm/opendox-openxdox-boundary.md` for the module-by-module
table):

- **openDox, ~24.9K** — the editor and canvas family, the model plane, branch
  sessions and pull requests, accounts and app plumbing, the NotebookLM action,
  and the pull-up wave.
- **openXdox, ~10.9K plus a large unbuilt remainder** — the adapter
  implementation and projection mechanism, the gate-and-commission loop, scope
  and ownership authority; and the machineries that do not exist yet at all: the
  model/scenario workbench, the evidence-and-provenance surface, the
  role-and-authority projection.
- **Descendant (`codexDox`), ~5.0K under the conservative reading** — the
  OpenSpec-and-doc-health specifics (`doxbench_packet`, `doxbench_contracts`,
  `human_seen`) and the three lanes, whose whole subject is thawing
  openxFactory's own git corpus into a served snapshot.
- **Residue that must be split by function, 10.9K** — `serve.py` (6,733; the app
  server and the corpus server in one file, needing an app-server extension
  point so openXdox can contribute routes without forking the server),
  `cli.py` (2,456), `workbench.py` (1,575), `authoring.py` (329).

**The named pull-up candidates**, ranked by value to a lab assistant who has
never heard of a factory: the bounded-knowledge and compression stack
(`doxbench_knowledge`, 1,231 — filed as governance only because its input set is
called "the staged set"); abstracts (`doxbench_abstract_store` 446 plus the
generation surface); the lens set-builder (the keyword-query half of `lens`,
282); the NotebookLM connection (`notebook_action`, 239 — with the stage-to-book
mapping left behind, since a per-project book is the neutral shape); and the
editor-and-chat surface the other four are used through. Deliberately NOT pulled
up: Adx's `calibrated`-tier calibration loop (domain machinery, and openDox has
no outcome to read) and the gate console (a student has nobody to gate against).

**The seven machineries common to the three mappings**, which is the extraction
Q5(b) asks for: the corpus-adapter implementation; the lifecycle engine (a
controlled status vocabulary, legal transitions, the authority each requires,
and the point of immutability-with-addenda — all three domains have one and only
the words differ); the gate-and-commission loop; the evidence-and-provenance
surface (a chart citation, a ledger tie-out and an attribution chain are one
machinery); the model/scenario workbench; the role-and-authority projection; and
the review lane.

**The finding that most needs contesting.** Under the strict reading of the
three-layer test, most of today's "integration layer" is openxFactory-and-
OpenSpec-specific — the lifecycle taxonomy, the promotion funnel, the change/
spec/delta vocabulary, doc-health's families, the three lanes — and therefore
belongs to `codexDox` rather than to the common core, which would mean openXdox
is largely UNBUILT and openDox takes more than the first cut assumed. The
cheaper reading is that openxFactory is the neutral layer rather than a domain,
so its governance vocabulary is genuinely neutral and the current reader IS the
common core. The two readings disagree about roughly 15K lines, and the test
between them is concrete: would a clinician ever see the word "requirement"?

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
  repository scope. Q3's per-tenant-always ruling STRENGTHENS all of it: the
  manifest flow now runs once per tenant, by construction.
- **What changes shape:** its Q1 (contract home) should now be answered INSIDE
  the two-layer change, because a per-tenant install provisions a DATABASE as
  well as two GitHub Apps. And its Case A / Case B distinction is now
  load-bearing rather than incidental — Brett's Q3 ruling names both cases
  explicitly and applies the same topology to each.
- **What is now settled that was open there:** the dispatch App does NOT become
  moot. Q1 makes the apply lane the ONLY write path to governed content, so both
  Apps stay — the content App because git remains authoritative, and the
  dispatch App because the credential-free serving tier still must not hold a
  contents-write key.
- **Disposition:** the topic folder STAYS staged and is not deleted or rewritten
  by this slice. It is named as a predecessor here, and the eventual proposal
  either carries its five questions or explicitly re-stages what it does not
  carry.

**codexFactory issue #89** — "Plan openXdox standalone project migration", OPEN
since 2026-08-25.

- **What survives:** the topology it recorded and its whole obligations list,
  which reads as a checklist for the eventual change: preserve stable project,
  repository, subject and work-item identities; re-parent openXdox out of
  xFactory; update repository and submodule topology; update dashboard
  projections and project-register relationships; migrate policy, ownership and
  governance bindings; record a complete audit trail and a rollback plan. Its
  scope boundary — "leave the future re-parenting operation to a dedicated
  opsXfactory project/workflow" — remains the right home for the mechanical
  migration.
- **What changes:** #89 scoped a PROJECT-REGISTER re-parenting, one level of
  hierarchy. The rulings make it a TWO-repository extraction with a runtime, a
  database and a third layer of descendants, so the re-parenting is a
  consequence of the split rather than the whole of it. Its topology diagram
  predates the two-layer ruling and needs a third level. Q1 also changes its
  subject: the project register itself becomes database-held coordination state,
  so "update project-register relationships" is a migration into the openDox
  schema rather than a YAML edit.
- **Disposition:** folded, not duplicated. A cross-reference comment was posted
  on #89 on 2026-09-04 naming issue #656 as the governing record. #89 stays open
  as the codexFactory-side record of the migration operation it describes.

## Sequencing constraints

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

1. **The one-way dependency lands FIRST and is worth doing alone.** Q4's small
   neutral module — receiving `OutputBoundary` so `doc_health` no longer imports
   into `ideation_dashboard` — is a small, forward-compatible change that pays
   for itself whether or not the carve ever happens. Nothing else in this arc
   can start while the two packages import each other.
2. **The corpus adapter's operations are named before any repository is
   created.** Q4 settles WHO defines and WHO implements; it does not settle the
   signatures. A repository created before the interface exists will have the
   boundary drawn by whatever `git filter-repo` happened to move.
3. **The apply lane is hardened before it becomes the only write path.** Q1
   promotes a path with ONE dispatch in its history to carrying every governed
   write from every tenant instance. That is a precondition, not a follow-up —
   and `ideation-intent-plane`'s unpromoted capability is the record of what was
   ratified about it.
4. **`serve.py` is the boundary and it cannot be split last.** 6,733 lines
   carrying both the app server and the corpus routes, with three `doc_health`
   imports and five active changes touching the package. Its split — behind an
   app-server extension point, so openXdox contributes routes rather than
   forking the server — is the extraction's critical path.
5. **The active-change wave has to be resolved, waived or explicitly re-homed —
   and one of them deepens the coupling.** `add-nightly-dashboard-refresh` ADDS
   seven requirements to `doc-health` on the dashboard's behalf while Q4 rules
   the dependency one-way; those two are in tension and the tension is a
   decision, not a merge conflict. Its lane has three worker runs, no successes,
   and no status artifact, so "wait for it to archive" is not a plan with a date.
6. **The three domain mappings are worked before the openXdox boundary is
   fixed.** Q5(b) requires the common core to be EXTRACTED from three mappings
   rather than asserted from one. Fixing openXdox's contents from today's code
   alone would produce a layer Medx and Ledgerx cannot use, which is the failure
   the direction exists to prevent.
7. **No pin-sync discipline is waived.** A `<Domainx>Dox` descendant pins by
   commit TWICE — gitlink plus pin file, same commit — and the aggregation's
   codexFactory three-in-one-commit rule (gitlink, reusable-workflow sha, test
   PIN) is the standing warning about what happens when a pin moves alone.
8. **Shared-tree discipline.** Every commit in this arc stages explicit paths
   and commits with pathspecs, and checks the current branch before any
   submodule commit.
9. **The naming-record amendment travels with the repository creation, not
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
  and it was absent by design — the promoted spec says in two separate
  requirements that the dashboard authorizes nothing on the hosted actor and
  that identity presence changes no capability verdict. Q1 and Q2 together
  invert that: an account is a durable database row, authentication is delegated
  to the Keycloak broker, and authorization stops being a property of
  where-the-request-came-from. That is the largest conceptual change in the
  rulings and the easiest to under-read. — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-09-04
- Q1 answers the ORIGIN COMPLAINT with its coordination half, not its document
  half. "No good place to store my projects" is solved by projects, members and
  the project-to-repository map living in a database every tenant install has —
  while the specs themselves still land in a repository. Which means openDox
  must be able to CREATE that repository as a first-class act, or the complaint
  returns one level down. Nothing in the rulings says who creates the repo. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04
- The rejected hybrid has a cost worth naming. Ideas-in-the-database-until-
  promoted was rejected, so an idea is a governed document in git from its first
  save — consistent, and heavier than a lab assistant may want. A student
  jotting a half-thought writes a file through an apply lane. Whether openDox
  needs a pre-governed scratch space that is NOT a "draft of a document" is a
  real residual and it is not any of the open questions below. — Added-by:
  Claude Opus 5 (session, Brett's direction) · 2026-09-04
- The model/scenario workbench is the biggest thing nobody has built. All three
  domains declare a `governed-derived-model` family, Medx's templates are
  RATIFIED, Adx conforms at `calibrated`, and there is no UI for a model or a
  scenario anywhere in 80K lines. If openXdox is the common core, this is its
  centre of gravity — and it is greenfield, which changes the character of the
  work from "carve" to "carve and build". — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-09-04
- Research analysis is where the three-layer test bites hardest, in a good way.
  A lab assistant reading twenty papers, clustering them, summarizing them,
  keeping a notebook and drafting a protocol is MedxFactory's own research half
  with no domain machinery at all. That is the strongest confirmation that "a
  student could use openDox" is not a concession to hypothetical users — it is
  half of a real domain's mapping. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-09-04
- The three lanes may be the clearest descendant content in the package. Their
  whole subject is thawing openxFactory's git corpus into a served snapshot; one
  of them has never succeeded; and Q1 makes the apply lane a permanent fixture
  of the openxFactory mapping specifically. Under the three-layer test that is
  `codexDox`, not the core. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-09-04
- Five descendant names implied and none built. That is correct under the lazy
  rule, but a named-and-absent repository is a thing people create by hand at
  2am, which is why the wallet arc registered names in the naming record and
  created nothing. The same treatment probably applies here. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-09-04
- The NotebookLM projection is per-repo today, with a capacity guard written
  against repositories after the 300-source cap incident. Per project-in-a-
  database it would be per project, which is better shaped and a real migration
  of the guard — and the generic half is a named pull-up while the stage-to-book
  mapping stays above. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-09-04

## Conflicts

- **The 2026-09-04 read-only review recommends NOT NOW at medium-high
  confidence, and the rulings proceed.** The review's three decisive facts are
  all still true: the wallet precedent's own trigger (a live consumer) has not
  fired, codexFactory holds zero lines of the code; the move cannot be
  byte-identical; five active changes are mid-flight with two open archive
  gates. The rulings supersede that by commissioning the consumer rather than
  waiting for it, and the three facts become the sequencing constraints. Until
  that is written into a proposal, a recorded review recommendation and a set of
  rulings point opposite ways. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-09-04
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
- **Q5's second layer and the layer's own NAME disagree.** The direction says
  "openXfactory brings in the core machinery to map to domains" and asks what is
  common to the Medx, Ledgerx and Adx mappings — which describes a
  DOMAIN-MAPPING CORE. The founding ruling says openXdox is "openDox tuned for
  use with openXfactory" — which describes one domain's integration. If the
  first reading holds, most of today's reader is `codexDox` and openXdox is
  largely unbuilt; if the second holds, the domain-mapping core has no home and
  each descendant reinvents it. Both readings are consistent with the words and
  the packet keeps both. — Added-by: Claude Opus 5 (session, Brett's direction)
  · 2026-09-04
- **`add-nightly-dashboard-refresh` deepens the coupling Q4 rules one-way.** It
  is ratified, cross-repo across three repositories, and ADDS seven requirements
  to `doc-health` on behalf of the dashboard. Its archive gate is correctly open
  (13 tasks) and its lane has never produced its status artifact. So a ratified
  in-flight change and a ruled seam direction are pulling the same dependency in
  opposite directions right now. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-09-04
- **`domain-descendant-boundary`'s "created on its first profile, not before"
  describes today's state exactly, and the rulings commission descendants
  anyway.** The standard's laziness rule would say `MedxDox` and `codexDox` do
  not exist yet because no domain has a profile. Q3 makes each one the
  deployment unit for a tenant install. These reconcile if the descendants are
  NAMES now and repositories on first profile — the wallet arc's own
  treatment — but as spoken, the rulings and the standard disagree about when a
  descendant exists. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-09-04
- **"Two layers of opensource" has no in-house precedent.** Every `open*`
  repository in this organization is PRIVATE and carries NO license, including
  `openXwallet`, created days ago under a ruling that called it a neutral
  open-source product. So either the family's openness is aspirational and these
  rulings inherit that, or openDox is the first genuinely public repository and
  needs a license, a contribution posture and a public-issue policy that nothing
  else here has. Both readings are consistent with the words; Q7 asks. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04
- **Q1 keeps documents in git while Q5 asks openDox to be useful alone.** A
  student with no repository and no apply lane cannot save a governed document
  at all under Q1, so a standalone openDox either ships its own trivial adapter
  implementation over a plain local git repository — which is probably what "no
  knowledge of OpenSpec or doc-health" implies — or the standalone case is not
  actually served. The rulings compose only under the first reading, and nothing
  states it. — Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

## Open questions

Two questions await Brett (Q6, Q7 — the numbering follows the governing record,
where Q1-Q5 are the rulings above). Four more (Q8-Q11) are secondary: they are
real, they have recommendations, and they are expected to travel into the change
rather than be ruled now.

### Q6. How does this sequence against the five active `ideation-dashboard` changes?

Context: five active changes carry live deltas against a 102-requirement spec
this topic proposes to split three ways. Two have open archive gates and 20 open
tasks between them; one of those is cross-repo across three repositories and
ADDS seven requirements to `doc-health` — deepening the exact coupling Q4 ruled
should point one way — and its lane has three worker runs, zero successes, and
has never produced its status artifact. A third is built but unarchived. Two
carry `target_release: none`. Separately `add-ideation-intent-plane` has been
ratified, part-realized and unpromoted for 43 days, its capability is absent
from `openspec/specs/`, and Q1 has just made its apply lane the only governed
write path.
Recommended answer: do NOT wait for the wave to clear, and do not carve into it
either. Take four preparatory slices first — Q4's one-way dependency and its
neutral module, the corpus adapter's operation signatures, the apply lane's
hardening, and the three domain mappings worked out — none of which conflicts
with any of the five, all of which are worth doing if the carve never happens.
Require before the CARVE itself: every active change either archived, or
explicitly re-homed with its successor destination named in its own proposal, or
waived by a recorded ruling. Treat the unpromoted `ideation-intent-plane`
capability as a blocking bookkeeping item, because a capability that is ratified
and absent from canon cannot be assigned a successor home — and it is now the
record of the write path everything depends on.
Explanation: "wait for the wave" has no date — one gate depends on a lane that
has never succeeded — and "carve now" strands five ratified deltas against a
spec that no longer exists in one piece. The preparatory slices are the only
work that is unconditionally correct, and doing them first shortens the carve
whenever it happens. Naming the re-homing requirement per change is what stops
the carve from silently orphaning a ratified delta. The one genuine conflict —
`add-nightly-dashboard-refresh` adding `doc-health` requirements for the
dashboard while Q4 separates them — needs a decision rather than a merge:
either its seven requirements are authored against the adapter instead, or the
split waits for it, and the second option has no date.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q7. Who owns the repositories, under what license, and what do the measured `opendox` collisions require?

Context: neither `opensoft/openDox` nor `opensoft/openXdox` exists. Measured
2026-09-04: `opensoft/openxFactory` is PRIVATE with NO license, and
`opensoft/openXwallet` — created days ago as a neutral open-source product — is
likewise private and unlicensed, so the existing `open*` family's openness is a
naming convention rather than a legal or operational posture. A GitHub
ORGANIZATION named `opendox` exists (created 2026-03-20, one public repo
`opendox/dox` on an unrelated Amazon-analytics subject, last pushed 2026-05-31).
Six repositories named `opendox` exist; the largest is `noitran/opendox` (22
stars, a Laravel OpenAPI package, dormant since 2022) and the one in the
ADJACENT subject space is `fum4/opendox` (0 stars, pushed 2026-07-16, "Spec +
CLI + skill for agent-written repo docs"). GitHub namespaces repositories per
owner, so none of these blocks `opensoft/openDox` — but the org name is
unavailable and an active project in the neighbouring problem space carries the
same word. And the ruling says "two layers of opensource".
Recommended answer: create both repositories under `opensoft`, matching every
other product in the family, and do NOT pursue the `opendox` organization.
Decide license and visibility AT REPOSITORY CREATION and record it in the
change: a permissive license (Apache-2.0 for the patent grant, given an
organization shipping governance tooling) and PUBLIC visibility for openDox
specifically, with openXdox's visibility a separate decision that may stay
private without contradicting the ruling since its subject is openxFactory's own
governance. Do not make either public without a contribution and
security-report policy. Amendment 3 must state the collision facts as measured —
the org, the six repositories with the two that matter named and dated, and the
fact that per-owner namespacing makes the repository name available — plus
Brett's acceptance of the adjacent-subject overlap, and it must NOT repeat the
bare claim that the name is "taken".
Explanation: `opensoft` ownership is what every consumer's pin, CODEOWNERS entry
and submodule URL already assumes, and a separate organization would fragment
the review-authority and ruleset estate for a name nobody can have anyway. The
license half is Brett's decision and not one this topic can settle, but it must
be ASKED before the repository exists — retro-licensing a repository with
outside contributions is materially harder than choosing at creation, and the
family's current posture shows how easily "open" stays nominal by default. The
amendment's value is the measurement: the original record's one-word "taken"
justified a naming decision for three weeks without anyone checking what was
actually taken, and an amendment that repeats the same style of claim would fail
the same way. Q5's "a student could use openDox" also gives the visibility
question a product answer rather than only a legal one: a student cannot use a
private repository.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q8. What happens to the promoted `ideation-dashboard` capability — split by requirement across three destinations, or REMOVED with successors?

Context: `ideation-dashboard` is a promoted capability with 102 requirements and
472 scenarios in a 289 KB spec, 30 archived changes carrying deltas against it,
and 5 active. `split-openxwallet-repo` established this repository's only
precedent — its first `## REMOVED Requirements` blocks and its first capability
exit — where two whole capabilities left with their successor location recorded.
Here one capability splits THREE ways under the Q5 test, which is a shape the
corpus has never seen.
Recommended answer: REMOVE `ideation-dashboard` from the openxFactory corpus
with a per-requirement successor map — each of the 102 requirements named with
its destination (openDox, openXdox, or a named descendant) and its successor
capability id — and let the destinations promote their own capabilities from that
map rather than inheriting the id. Do not keep a stub in openxFactory.
Explanation: a per-requirement map is the only artifact that makes a three-way
split auditable, and it substitutes for the byte-identity floor the extraction
cannot have: instead of proving the bytes did not change, prove every
requirement has exactly one home. Keeping a stub would leave openxFactory owning
requirements about code it does not hold, which is the condition the split
exists to end. The cost is that the map is large and hand-authored, and that 30
archived changes then cite a capability absent from this corpus — annotation work
on immutable records, exactly as the wallet arc did.
Disposition status: open (secondary — expected to travel into the change)
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q9. What replaces the byte-identical floor as the extraction's safety property?

Context: `split-openxwallet-repo`'s ratified floor was a pure move — eight
artifact digests matching openxFactory HEAD before the tag was cut, with exactly
one permitted prose carve-out — "because a move whose diff is not provably empty
cannot be bisected against". A three-way split of a package whose modules import
a sibling that imports back cannot meet that, and neither can a split that adds
a database and a runtime.
Recommended answer: a BEHAVIOURAL floor in three parts. (1) The 3,927 existing
test functions split with the code, all suites stay green, and the post-split
collection counts SUM to the pre-split count — a number pinned by test the way
`pytest-suite.yml` already pins this repository's collection triple. (2) A
neutral conformance corpus for openDox, on the wallet extraction's pattern of
positives plus negative confirmations, so a descendant — and a student — can
prove conformance without openxFactory's corpus. (3) A named equivalence run:
the same corpus served by the pre-split tree and by the post-split repositories
produces the same snapshot digests. Each part gets its own evidence line, and
none of them is "the tests passed".
Explanation: the safety property must be mechanically checkable, because that is
the whole function the byte-identity floor performed. Test-count arithmetic
catches silently dropped tests, the most likely way a 125-file suite loses
coverage in a carve; the conformance corpus is what makes openDox independently
verifiable rather than verifiable-only-against-this-repository, which Q5's
standalone test now requires anyway; and the snapshot-equivalence run is the
closest available analogue to "the diff is provably empty" for a system whose
output is a projection. The cost is that all three must be built before the
carve, which is the point.
Disposition status: open (secondary — expected to travel into the change)
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q10. May a consumer pin openDox directly, or is openXdox always the pinned layer?

Context: the founding ruling says descendants pin openXdox, and for the
DomainxFactories that is right — they need the domain-mapping machinery. Q5 then
requires openDox to be useful ALONE to a student or a lab assistant, and Q4
makes the dependency one-way (openXdox depends on openDox, never the reverse),
which makes a standalone openDox structurally possible. If nothing may pin
openDox alone, then openDox has exactly one consumer and its independence is
nominal — which would contradict Q5's test.
Recommended answer: BOTH are pinnable, and the consumer DECLARES which layer it
pins. `domain-descendant-boundary`'s modification grows a one-field declaration
rather than a second pattern. DomainxFactory descendants pin openXdox because
that is what the ruling says they need; a non-factory consumer — the student, the
lab, an outside user — pins or simply installs openDox.
Explanation: a neutral product with one possible consumer is not a neutral
product, and Q5's standalone test is unsatisfiable if openDox can only be
reached through openXdox. The declaration is cheap: the descendant standard
already requires a pin file naming the product, so naming the LAYER is one more
key. It also makes the boundary testable — if nothing can pin openDox alone, the
boundary is in the wrong place, which is the same check Q5's "would a student
use it?" applies at module grain.
Disposition status: open (secondary — expected to travel into the change)
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

### Q11. Does the lifecycle vocabulary become parameterized, or does openXdox ship openxFactory's taxonomy?

Context: Q5(b) says openXdox holds the machinery COMMON to the three domain
mappings. Each domain has a lifecycle — a clinical note drafted, attested,
filed, immutable-with-addenda; an accounting question raised, researched,
concluded, professionally reviewed, filed as a defensible position; a campaign
brief drafted, brand-reviewed, spend-approved, launched, measured, retired — and
they differ in their WORDS, not their shape. openxFactory's own nine-word
`Status:` taxonomy is hardcoded across the reader today, and
`document-lifecycle` owns it as a contract. Whether the common core carries a
parameterized lifecycle engine or a fixed taxonomy decides whether Medx and
Ledgerx can use openXdox at all.
Recommended answer: parameterize. openXdox carries the ENGINE — a declared
status vocabulary, legal transitions, the authority each transition requires,
and the point of immutability-with-addenda — and each descendant declares its
own vocabulary in the domain-mapping declaration. openxFactory's nine words
become `codexDox`'s declaration, and `document-lifecycle` gains a MODIFIED delta
saying the taxonomy it owns is one instance of the declared shape rather than
the shape itself.
Explanation: the three mappings differ only in vocabulary, which is precisely the
signature of something that should be data rather than code — and the cheapest
possible test of whether openXdox is the common core is whether a clinician
would ever see the word "requirement". The cost is real and should be stated: a
parameterized lifecycle means the reader can no longer pattern-match on
`Status: ratified`, every check that reads a status becomes a lookup, and
`document-lifecycle`'s contract grows a level of indirection. The alternative
cost is worse — openXdox ships one domain's words and the other four
descendants each fork it.
Disposition status: open (secondary — expected to travel into the change)
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-09-04

## Exit

One OpenSpec change on the `split-openxwallet-repo` shape, adapted for a
two-repository, non-byte-identical extraction of an APPLICATION rather than a
contract family, with a third layer of descendants below it. It declares a code
surface across at least six repositories — openxFactory, the two new
repositories, the xFactory aggregation, Omnigent-Install and codexFactory — so
under `release-realization` it archives only on merged plus green realization
evidence, never on landing.

What the change would carry: the REMOVED-by-split delta on `ideation-dashboard`
with a per-requirement successor map across three destinations (Q8); the ADDED
neutral corpus-adapter seam capability, in the shape Q4 ruled — declared by
openDox, implemented by openXdox, dependency one way; the ADDED neutral
domain-mapping declaration capability the descendants carry; the MODIFIED
`domain-descendant-boundary` delta for a descendant of a runtime product with a
schema and migrations that is also the per-tenant deployment unit; the MODIFIED
`neutral-product-pin` delta for a pin whose consumption is a deployment;
Amendment 3 to `docs/openxdox-naming.md` carrying the measured collision facts;
the declared authority boundary from Q1 written as a contract; and the
three-part behavioural floor from Q9 in place of byte identity. Speckit features
follow per phase, on the convener's standing rule that OpenSpec ratifies the
boundary and Speckit builds it: land the one-way dependency and its small
neutral module; name and land the corpus adapter's operations; harden the apply
lane; split `serve.py` and the other three residue modules by function behind an
app-server extension point; scaffold and carve, proving the behavioural floor;
consume and shed in openxFactory; aggregate the submodules; then a first
descendant, lazily, when a domain has a profile.

Four preparatory slices are worth taking BEFORE the proposal and do not depend
on it: Q4's one-way dependency (relocate `OutputBoundary` into the small neutral
module), the corpus adapter's operation signatures, the apply lane's hardening
(Q1 promotes a path with one dispatch in its history to the only governed write
path), and working the three domain mappings out far enough to extract the
common core. All four are unconditionally correct — they are the debts that make
the current code hard to change, and the last one is the direction's own
homework.

What must be true first: Brett answers Q6 (sequencing against the five active
changes) and Q7 (ownership, license and the collision facts) — Q7 before either
repository is CREATED rather than before the proposal is written. Q6's
active-change wave must be resolved, re-homed or waived by a recorded ruling
before the carve phase, and the unpromoted `ideation-intent-plane` capability
must be promoted or its non-promotion recorded before the per-requirement map is
authored. The four secondary questions carry recommendations and are expected to
travel into the change as council questions rather than resolve here; Q11 is the
one whose answer most changes the shape of what gets built, because a fixed
lifecycle taxonomy and a parameterized one produce different repositories.
