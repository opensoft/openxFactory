# openDox and openXdox — Two Open-Source Layers — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Brett ruled on 2026-09-04 that the document-and-ideation workbench
splits into two open-source repositories — `opensoft/openDox`, a hosted
installable app with its own database, users and projects that manages documents
and ideas with git and NotebookLM integration, and `opensoft/openXdox`, openDox
tuned for openxFactory — with domain descendants (`MedxDox`, `codexDox`) pinning
openXdox and installing per tenant with their own database; over the following
half hour he ruled four of the open questions (the database owns identity and
coordination while git owns governed artifacts; the runtime reuses the Hermes
install pattern; one instance and one database per tenant always; openDox
defines the corpus-adapter interface and openXdox implements it, one way) and
gave a THREE-LAYER test for the module split — openDox must be useful alone to a
student or a lab assistant, openXdox holds the machinery common to how Medx,
Ledgerx and Adx map onto the workbench, and descendants hold the domain-specific
mapping; this packet is the entry point to the five documents that work that out.
Topics: opendox, openxdox, ideation-dashboard, doxbench, repo-split,
domain-descendant-boundary, neutral-product-pin, two-layer-product,
tenant-install, per-tenant-database, users, projects, notebooklm, git-integration,
openxdox-naming, feat-request
Repository context: openxFactory authors this packet because it owns the
`ideation-dashboard` capability, the corpus the workbench reads, and the naming
record the ruling overrides. The eventual homes are two NEW repositories,
`opensoft/openDox` and `opensoft/openXdox`, neither of which exists today; the
domain descendants land in the DomainxFactories.
Captured: 2026-09-04

## Possible feats

- **openDox neutral core repository** — carve the document/idea/project/user app
  out of `scripts/ideation_dashboard/` + `web/` into `opensoft/openDox`, with
  its own release identity and its own conformance suite.
- **openXdox integration repository** — the corpus reader, lifecycle projection,
  gate console and lanes, consuming openDox as a library or a base image and
  openxFactory's corpus at a pin.
- **openDox hosted install with a database** — users, projects, documents and
  ideas persisted in Postgres, on the Hermes-install runtime pattern (FastAPI +
  Postgres + ordered migrations + a lifecycle CLI + a Compose package and an AKS
  adapter).
- **Per-tenant descendant install** — `MedxDox` / `codexDox` as
  `<Domainx><Product>` descendants that pin openXdox and stand up one instance
  with its own database inside the tenant a DomainxFactory install creates.
- **The corpus adapter** — one named seam that breaks today's two-way
  `doc_health` ↔ `ideation_dashboard` import cycle so the reader can leave the
  corpus behind.
- **openDox project store** — the thing Brett actually asked for: a place to
  start a new project in a new repo, write some specs, and have them live
  somewhere that is not a scratch directory.

## The ruling

Verbatim, 2026-09-04, recorded in `opensoft/openxFactory` issue #656:

> "we do not have a place to store projects. If i want to start a new project in
> a new repo, and make some specs, we have no good place to store my projects. I
> think we need to make this an app that installs and is hosted with a db. we
> should have users and projects and can expand the feature set."
>
> "openDox is a dead project. it has almost empty repo. I think someone started
> with idea and stopped after a few days. lets use that name as the core
> opensource repo. we have two layers of opensource openDox and openXdox. The
> openXdox is openDox tuned for use with openXfactory. we will make openDox work
> to just manage documents and ideas. it will keep the integration with git and
> notebook lm etc and have all tools that help for document management and
> ideation. then openXdox will integrate with openXfactory."

And earlier in the same sitting:

> "We then further pin that down to medxDox and CodeXdox for use in those domain
> factories. If I install MedxFacotry [sic], then I get a medXdox install running in
> the installed tenand [sic] with its own db."

## What Brett ruled within the hour (issue #656)

Four rulings and one direction, all 2026-09-04, all recorded as comments on the
governing record. They are settled context for the whole packet; the documents
below work under them rather than reopening them.

- **Q1 — the database owns identity and coordination; git owns governed
  artifacts.** Users, memberships, projects, the project-to-repository mapping,
  sessions and unsaved drafts live in the openDox database. Specs, changes,
  ideation documents and contracts stay in git, read from repositories and
  **written back only through the apply lane**. Every existing gate stays valid;
  the database is disposable relative to the corpus. Rejected: documents in the
  database with git as an export, and the hybrid where ideas live in the
  database until promoted.
- **Q2 — reuse the Hermes install pattern.** FastAPI + Postgres, deployed the
  way `xFactory-Hermes-Install` is (live on AKS since 2026-07-19), OIDC through
  the Keycloak broker being adopted in QA, growing into the OpsxFactory `dox`
  workload set. Rejected: bolting a database onto today's stdlib `serve.py`
  monolith, and a new full-stack platform.
- **Q3 — one instance and one database per tenant, always**, in both the
  operator-hosted (Case A) and tenant-hosted (Case B) cases. No cross-tenant
  data ever shares a store. Rejected: shared multi-tenant with row-level
  isolation, and a per-tenant default with a pooled operator option.
- **Q4 — openDox defines the corpus-adapter interface; openXdox implements
  it.** openDox declares how documents are listed, read, written back and
  checked, with no knowledge of OpenSpec or doc-health. The two
  `doc_health` → `ideation_dashboard.boundary` back-imports move into a small
  neutral module both sides depend on. **The dependency points ONE way: openXdox
  depends on openDox, never the reverse.** Rejected: openDox pinning doc-health
  as a library (inverts the layering), and openXdox as a tuned copy with no
  shared interface (guarantees divergence).
- **Q5 — a DIRECTION, not a module ruling.** Verbatim: *"we want to make openDox
  useful on its own … it is domain neutral and external from openXfactory. we
  need to make sure openXfactory brings in the core machinery to map to domains.
  we need to think how a patient managment [sic] and research maps to the openXdox.
  and how a finacial [sic] simulations or accounting questions would map in
  ledgerXfactory. same for marketing analysis in adXfactory. what is core to
  these that we pull out and put in openXdox. and what can pull up to openDox
  that does not rely on openXfactory … a student could use openDox or a lab
  assistant. so we want that to still be useful on its own"*. The per-module
  assignment is design work under that test, carried by this packet.

## The test the direction sets

Three questions, asked of every module and every requirement:

1. **openDox** — would someone with no notion of factories, gates or tenants use
   it? A student. A lab assistant. Then it belongs here — and the packet must
   actively look for what to PULL UP from today's dashboard to make openDox a
   better brainstorming and research-analysis tool.
2. **openXdox** — is it the core machinery common to how MedxFactory (patient
   management and research), LedgerxFactory (financial simulations, accounting
   questions) and AdxFactory (marketing analysis) each map onto the workbench?
3. **Descendant** — is it one domain's own mapping?

That third column is what makes this harder than a two-way split, and
[the domain-mappings document](opendox-domain-mappings.md) argues it may take a
great deal more than expected.

## The four layers, top to bottom

```text
openDox      the product. An installable, hosted app with a database.
             Users, projects, documents, ideas. Git and NotebookLM
             integration. Every tool that helps document management and
             ideation. Knows nothing about openxFactory.

openXdox     openDox tuned for openxFactory. The corpus reader: lifecycle
             status, the promotion funnel, doc-health projection, the gate
             console and its verbs, the nightly and apply lanes. Knows
             what a `Status:` header means and what an OpenSpec change is.

MedxDox      domain descendants, in the ratified `<Domainx><Product>` form.
codexDox     Pin openXdox by commit, twice. Carry profile — the domain's
LedgerxDox   corpus vocabulary, branding, deploy config — never a fork.
OpsxDox      Created lazily, on the domain's first profile.
AdxDox

<tenant>     a running instance. A DomainxFactory install brings up its
             descendant with its own database inside the tenant it created.
```

The bottom two rows are the ones that make the top row necessary. A per-tenant
instance with its own database is not a thing you can ship as a static site
generated from a git checkout, which is what the workbench is today.

## What each layer owns — a first reading

**openDox owns the app.** Identity and accounts. Projects as first-class
persisted objects rather than a register file. Documents: read, load for
editing, edit, save, thread. Ideas: capture, cluster, relate, promote. Git: the
branch session, the commit-per-act discipline, the pull request. NotebookLM: the
projection and the return path. The model plane: providers, bindings, brokered
tokens, chat over a bound buffer, abstracts. The editor and canvas. The CLI and
the install tooling.

**openXdox owns the interpretation.** That a document carries a controlled
`Status:` header from a nine-word taxonomy. That `ideation/brainstorm/` →
`ideation/staging/` → an OpenSpec change → `openspec/specs/` is a pipeline with
gates. That a `## ADDED Requirements` block is a delta. That doc-health has
twenty-three check families whose findings have severities and dispositions.
That a ratification is an act with an actor and a record. The funnel, the wheel,
the lens over lifecycle state, and the three lanes.

**A descendant owns the domain's vocabulary.** What a "document" is in a clinic
versus a dev team. Which corpora exist. What the tenant is called.

## Why the split is not the wallet split

`split-openxwallet-repo` (ratified 2026-08-26) is the house precedent for
extracting a neutral product, and this ruling departs from it in one specific
way that has to be said out loud.

The wallet split kept the INTEGRATION SEAM inside openxFactory:
`governance/review-authority/` stayed, and only the product left. Brett's ruling
here puts the integration layer in its OWN open-source repository. That is
deliberate — openXdox is a product other people could run over their own
governed corpus, not a private adapter — but it means openxFactory ends up
keeping less than the wallet precedent would predict: the corpus itself and its
governance, and nothing of the code that reads it.

The second departure is arithmetic. The wallet split's ratified floor was a
**byte-identical pure move** — eight artifact digests had to match before the
tag was cut, because a move whose diff is not provably empty cannot be bisected
against. That floor is not available here. Twelve of the forty-eight dashboard
modules import `doc_health`, and `doc_health` imports back into
`ideation_dashboard` twice. A two-repository extraction of a package that is
half of a mutual dependency is a design change before it is a move.

## Speculation, marked as speculation

- **openDox may want to be genuinely public.** Everything in this org is
  private and unlicensed today, including `openxFactory` and the freshly-created
  `openXwallet`. "Open source" as a description of the existing `open*` family
  is aspirational. openDox is the first one where a real outside user is
  plausible — a person who wants a document-and-idea app with git integration
  and no interest in xFactory at all — which makes the license question live
  rather than theoretical.
- **The "DB makes openXdox smaller" reading is now closed.** Q1 keeps governed
  content in git, so openXdox keeps the whole projection and the database holds
  coordination state. What the ruling DOES shrink is the risk: an unstated split
  was the failure mode, and there is now a stated one.
- **But it opens a new one: openXdox may be the wrong shape entirely.** If the
  common core is the domain-mapping machinery (Q5's second layer) rather than
  the openxFactory corpus reader, then most of today's reader is `codexDox` and
  openXdox is largely unbuilt. The domain-mappings document holds that as a
  hypothesis against the boundary document's conservative cut; they disagree
  about roughly 15K lines.

## Where the other documents go

- [openDox — the core product](opendox-core-product.md) — users, projects,
  documents, ideas; the git and NotebookLM integrations; the standalone
  student-and-lab-assistant test; and the "no place to store projects"
  complaint that started this.
- [openDox domain mappings](opendox-domain-mappings.md) — the three mappings the
  direction asks for, worked explicitly against measured domain facts (Medx
  patient management and research, Ledgerx financial simulations and accounting
  questions, Adx marketing analysis), the seven machineries common to them, and
  the uncomfortable finding about what that makes today's reader.
- [openDox / openXdox / descendant — where the boundary falls](opendox-openxdox-boundary.md)
  — a three-column assignment of the 48 modules and 102 requirements under the
  direction's test, the named pull-up candidates, and the corpus-adapter seam.
- [openDox persistence and truth](opendox-persistence-and-truth.md) — Q1's
  ruling, the option space it was chosen from, the D5 precedent it fires, and
  the consequences the ruling makes concrete.
- [openDox install and tenancy — synthesis](opendox-synthesis-install-and-tenancy.md)
  — Q2 and Q3's rulings, what per-tenant-always costs, and what
  `domain-descendant-boundary` has to grow for a product with a schema.

The governing record is issue #656 and the staged topic
[`opendox-two-layer-product`](../staging/opendox-two-layer-product/opendox-two-layer-product.md);
this packet is non-normative exploration and may contradict itself — and
between the boundary document and the domain-mappings document it deliberately
does.
