# openDox and openXdox — Two Open-Source Layers — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Brett ruled on 2026-09-04 that the document-and-ideation workbench
splits into two open-source repositories — `opensoft/openDox`, a hosted
installable app with its own database, users and projects that manages documents
and ideas with git and NotebookLM integration, and `opensoft/openXdox`, openDox
tuned for openxFactory — with domain descendants (`MedxDox`, `codexDox`) pinning
openXdox and installing per tenant with their own database; this packet is the
entry point to the four documents that work out what each layer owns, where the
boundary falls in today's 80K lines, what the database is authoritative for, and
what a tenant install actually is.
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
> factories. If I install MedxFacotry, then I get a medXdox install running in
> the installed tenand with its own db."

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
- **The DB may make openXdox smaller than it looks.** A great deal of the
  reader's complexity today is that it recomputes lifecycle state from files on
  every serve. If openDox persists documents with their state, openXdox's job
  narrows toward *importing* a git corpus into that store and *exporting*
  governance acts back to it — which is a smaller surface than 30K lines of
  projection.
- **Or the opposite.** If git stays authoritative for governed content (and the
  gate contract arguably requires it — a ratification that exists only in a
  database is not a reviewable commit), then openXdox keeps the whole projection
  and the database is a cache. These two readings contradict each other; the
  persistence document works through both and does not resolve them.

## Where the other documents go

- [openDox — the core product](opendox-core-product.md) — users, projects,
  documents, ideas; the git and NotebookLM integrations; and the
  "no place to store projects" complaint that started this.
- [openDox / openXdox — where the boundary falls](opendox-openxdox-boundary.md)
  — a measured first cut over the 48 modules, 40 web files and 125 test files,
  and the corpus-adapter seam that has to exist for any of it.
- [openDox persistence and truth](opendox-persistence-and-truth.md) — database
  versus git, the D5 precedent that already ruled this once for projects, and
  what a gate means when the record lives in Postgres.
- [openDox install and tenancy — synthesis](opendox-synthesis-install-and-tenancy.md)
  — the runtime shape, the per-tenant instance, and what a DomainxFactory
  install actually has to do.

The governing record is issue #656 and the staged topic
[`opendox-two-layer-product`](../staging/opendox-two-layer-product/opendox-two-layer-product.md);
this packet is non-normative exploration and may contradict itself.
