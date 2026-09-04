# openDox — The Core Product: Users, Projects, Documents, Ideas — Brainstorm

Status: brainstorm
Kind: architecture
Summary: openDox is the neutral half of the 2026-09-04 ruling — an installable,
hosted app with its own database whose four first-class objects are users,
projects, documents and ideas, keeping the git and NotebookLM integrations and
the document-management and ideation tooling the workbench already has; the
origin of the requirement is Brett's complaint that there is nowhere to put a
project, three of the four objects already exist in some form and only the USER
is genuinely absent, and Brett's Q5 direction sets the test that governs
everything here — openDox must be useful ALONE to a student or a lab assistant,
which turns "what is neutral?" into "what would someone with no notion of
factories, gates or tenants use?" and makes a named pull-up wave part of the
product rather than a nicety.
Topics: opendox, ideation-dashboard, doxbench, projects, project-register,
users, hosted-actor, documents, ideas, notebooklm, git-integration,
branch-session, document-management, feat-request
Repository context: openxFactory authors this while it still owns the code; the
eventual home is `opensoft/openDox`, which does not exist yet
Captured: 2026-09-04

## Possible feats

- **A project is a stored object, not a register row** — a project with an
  owner, members, repositories, documents and its own state, persisted (Q1:
  projects and the project-to-repository mapping are database rows), created
  from the app rather than commissioned into an aggregation YAML file.
- **A user is a first-class principal** — an account row, not a display-only
  header the gateway stamps, with authentication delegated to the broker.
- **Repository creation as a first-class act** — Q1 keeps specs in git, so a new
  project needs a repository the app can create, or "no good place to store my
  projects" returns one level down.
- **The pull-up wave** — the knowledge/compression stack, abstracts, the lens
  set-builder and the NotebookLM connection, moved up so a lab assistant gets
  them with no factory at all.
- **A document store with git as a backing remote** — documents live in the
  app, and git is where they are published, versioned and reviewed.
- **The idea object** — brainstorm capture, clustering, the possibles register
  and the promotion funnel expressed as data rather than as headers parsed out
  of Markdown on every request.
- **NotebookLM as an app integration** — the projection and the notes-return
  path as a per-project setting rather than a repo-wide sync script.
- **Bring your own repo** — start a project against a new empty repository the
  app creates for you, which is the literal thing the ruling asks for.

## The standalone test (Q5 direction, 2026-09-04)

> "we want to make openDox useful on its own, it shoudl be able to still manage
> docs and do brainstorming and connect to notebook lm. it is domain neutral and
> external from openXfactory … a student could use openDox or a lab assistant.
> so we want that to still be useful on its own"

That is the acceptance criterion for this layer, and it is sharper than
"neutral": a module belongs in openDox if someone with no notion of factories,
gates or tenants would use it. It also creates an obligation the packet has to
discharge — actively finding what to PULL UP out of today's dashboard so openDox
is a genuinely good brainstorming and research-analysis tool rather than a
governance dashboard with the governance removed.

The pull-up shortlist, worked in full in
[the boundary document](opendox-openxdox-boundary.md):

| Pull up | Why a lab assistant wants it |
| --- | --- |
| The knowledge and compression stack (`doxbench_knowledge`, 1,231 LOC) | Assemble a bounded context packet over the documents you selected, with declared fidelity. The core research move; filed as governance today only because its input set is called "the staged set". |
| Abstracts (`doxbench_abstract_store` + the generation surface) | Deterministic abstracts that state their own absences, plus a separately-invoked distilled abstract verified against the document's declared fields, cached by path-digest-model. A literature-review tool. |
| The lens set-builder (the keyword-query half of `lens`) | Naming an intensional set the machine clustering missed is how a human organizes twenty papers. |
| NotebookLM connection (`notebook_action`, 239 LOC) | Named in the direction. What must NOT come up is the stage-to-book mapping — a per-project book is the neutral shape. |
| The editor and chat bound to the active buffer | The surface the other four are used through. |

Two things deliberately not pulled up: Adx's `calibrated`-tier calibration loop
(domain machinery, and openDox has no outcome to read) and the gate console (a
student has nobody to gate against).

## What the rulings already settled about this layer

- **Q1 — the database owns identity and coordination.** Users, memberships,
  projects, the project-to-repository mapping, sessions and unsaved drafts are
  openDox database rows. Governed documents stay in git, written back only
  through the apply lane. So of the four objects below, the USER and the PROJECT
  become real database objects; the DOCUMENT stays a git artifact with a
  database-held draft; and the IDEA — since the ideas-in-the-DB-until-promoted
  hybrid was explicitly rejected — is a governed document from its first save.
- **Q2 — identity is delegated, accounts are owned.** OIDC through the Keycloak
  broker, on the Hermes install's deployment pattern. openDox holds an account
  as a durable principal that a project's owner column points at; it does not
  become an identity provider with password resets.
- **Q3 — one instance and one database per tenant, always.** Which means the
  "student or lab assistant" case is a single-tenant install of the same
  artifact, not a special mode.

## The origin: "we have no good place to store my projects"

The complaint is precise and worth not paraphrasing away. Brett wants to start a
new project in a new repo, write some specs, and have somewhere for them to
live. Today the answer is: clone the aggregation, pick a submodule, put the
document in that repo's `ideation/` tree, and add a row to
`project-register.yaml` in a third repository. Every one of those steps assumes
you are already inside the xFactory workspace. There is no answer at all for a
project that is not one of the eleven repositories the register knows about.

That is the requirement. Everything below is what it implies.

## The four objects

### Users

**The one that is genuinely absent.** The workbench today has three different
identity concepts and none of them is an account:

- `hosted_actor` — a display-only string resolved per request from the
  gateway-stamped `X-Auth-Request-User` header. The promoted spec is emphatic
  that the dashboard "authorizes nothing on the hosted actor": it is
  presentation data, the dox-auth gateway is the identity authority, and trust
  rests on a NetworkPolicy boundary. A `null` value is normal.
- The local actor — resolved by `actor_identity.py` for gate actions, which
  exists specifically to close "the unauthenticated `--actor`".
- The loopback console verdict — what actually gates every write: a loopback
  bind, a real checkout, a resolved local actor and a per-serve console token.
  Identity presence changes no capability verdict.

So today write authority is a property of WHERE the request came from, not WHO
sent it. An app with users inverts that. This is the single largest conceptual
change in the ruling and it is easy to under-read: "we should have users" is not
a login page, it is a different authorization model.

**Answered by Q1 + Q2:** openDox owns the ACCOUNT (a durable principal, a
database row, the thing a project's owner column points at) and delegates
AUTHENTICATION to OIDC through the Keycloak broker. It does not own password
reset. What remains genuinely open is the first-user bootstrap in a fresh
per-tenant install, and how an account row is linked to a broker identity
without that mapping becoming an administrative surface of its own.

### Projects

**Exists, as a register row in another repository.** `project-register.yaml`
lives in the xFactory aggregation; openxFactory owns the neutral
`project-register` schema; the dashboard can COMMISSION a project
(`create-project` writes a `workflow-job` descriptor plus a gate-action record)
but deliberately never writes the register itself, and a fulfilment lane applies
the edit. Membership is multi-parent — "a project is a named view over
repositories, not an owner" (Brett, 2026-08-06). The header already brands as
"Opensoft openDox" and is already project-first: a project dropdown whose first
line is New Project, and repository selection as a visibility filter inside the
current project.

The name in the brand is not a coincidence. The promoted requirement is called
"The openDox project-first header". The product was already being called openDox
in canon before the ruling named the repository.

What is missing is that a project cannot own anything. It has an id, a name and
a repository list. It cannot own documents, members, settings, a NotebookLM
book, a model binding, or a state. In an app with a database, all of those are
project columns.

### Documents

**Exists, and is the most developed of the four.** doxBench already has: a
loaded set (the outline plus what the human loaded), a docs tile carrying read /
load-for-editing / save, an Editor and Preview canvas with one Save and one
Cancel, a per-buffer staleness guard, a session thread per loaded document with
a structured state header, share-session hand-off to a colleague, deterministic
and model-derived abstracts with a cache keyed by path-digest-model, and a chat
bound to the active buffer selection. Seventeen `doxbench_*` modules and about
30K lines of front end.

Almost all of that is neutral. It is about editing a Markdown document with a
model's help and saving it through a review gate. Nothing in it needs to know
what an OpenSpec change is.

### Ideas

**Exists as documents-in-a-directory, which is the interesting part.** An idea
today IS a Markdown file with a `Status: brainstorm` header in
`ideation/brainstorm/`, plus a `Topics:` line that a grep can cluster on, plus a
row in a possibles register the cross-reference index consolidates, plus a
position in a funnel the dashboard renders. The lens is a set-builder over
keywords. Clustering is derived.

Q1 rejected the hybrid where ideas live in the database until promoted, so an
idea is a governed document in git from its first save. That is consistent, and
it makes the brainstorm stage heavier than a lab assistant may want — a student
jotting a half-thought writes a file through an apply lane. Whether openDox
needs a pre-governed scratch space that is not a "draft of a document" is a real
residual, and it is separate from the question of whether "ideas" is a distinct
OBJECT TYPE, where the two readings still pull the boundary in opposite
directions:

- **Ideas are documents with a state.** Then the lifecycle vocabulary is
  openDox's — the app knows a document can be a brainstorm — and openXdox only
  adds the governance meaning of each state. Simple, but it puts a nine-word
  controlled taxonomy that `document-lifecycle` owns into the neutral layer.
- **Ideas are their own object.** Then openDox has an idea store with capture,
  relate, cluster and promote, and openXdox maps promotion onto the OpenSpec
  pipeline. Cleaner boundary, more to build, and the mapping is where all the
  work hides.

## The two integrations the ruling names

**Git.** "it will keep the integration with git". Today this is
`branch_session.py` (5,290 lines — the largest module after the server),
`session_git.py`, `session_pr.py`, and the discipline that every governed write
happens on a branch session and every gate act is a commit. That machinery is
neutral: branch-per-working-set, commit-per-act, one pull request per session.
What is NOT neutral is which acts exist and what they are called, and that
belongs above.

Note the direction change a database forces. Today git IS the store and the
branch session is how you write to it safely. With a database, the app writes to
Postgres and git becomes a PUBLISHING target — which is a different integration
with the same name.

**NotebookLM.** Today: `notebook_action.py` (an "Open in NotebookLM" tile
action — the first dashboard action ever), plus the projection standard
(`docs/lifecycle-notebook-projection.md`, one Ideation book per governed repo,
books resolved by title, a capacity guard after the 300-source cap incident),
plus `sync-notebooklm-books.py`, plus a notes-return import path, plus two
staged topics on reconciliation and share-access governance. The projection is
lifecycle-shaped — the books mirror the stages — so it straddles the boundary:
the *integration* is neutral, the *stage-to-book mapping* is not.

## "and have all tools that help for document management and ideation"

This clause is the expansion licence and it should be read as one. The listed
scope — documents, ideas, git, NotebookLM — is not a closed set; it is the seed
of a product whose feature set Brett explicitly said "can expand". Candidate
tools already sitting in this repository's ideation as separate topics, which
would become openDox features rather than dashboard features: the workstation
app shell, the mobile surface, context compression, session-notebook
reconciliation, the auto-fit model routing, the polyglot graph memory
experiment.

That is an argument for the two-layer split independent of the tenant story: the
neutral product has a roadmap of its own that has been queueing behind
governance work.

## What openDox must NOT know

A discipline worth writing down now, because it is the thing that will erode:

- The nine-word `Status:` taxonomy and what each word licenses.
- What an OpenSpec change, a spec delta, a requirement or a scenario is.
- doc-health, its check families, its severities, its dispositions.
- The promotion funnel's stages and their gates.
- `openspec/`, `contracts/`, `governance/` as meaningful paths.
- The ratification act, the convener, operator authority.

Every one of those appears in the current code, most of them in modules that
also do neutral work. The boundary document counts them.
