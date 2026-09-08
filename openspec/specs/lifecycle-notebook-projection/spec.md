# lifecycle-notebook-projection Specification

## Purpose

Define the derived NotebookLM books over the governance corpus: membership
derived from document lifecycle states, authority framing, grounding
context, and sync implementation ownership.
## Requirements
### Requirement: Derived notebook membership
Lifecycle notebooks SHALL derive their source membership from document
`Status:` headers via the canonical projection: `brainstorm` and `staged`
into the owning repository's Ideation book — one Ideation book per governed
repository, title family `xFactory Ideation — <RepoName>`, alias family
`xf-ideation-<repo-slug>` (repository name lowercased) — `draft` into the
shared Working Drafts book, and `ratified`, `standard`, and promoted
OpenSpec capability specs into the shared Canon book. Documents with
`record`, `superseded`, or `retired` status SHALL be excluded. A
repository's ideation membership is the status-derived set alone: charter
and grounding seeds do not constitute membership and SHALL NOT cause a
book's creation. Books SHALL be resolved by notebook title (the provider's
truth); the alias family is a machine-local operator convenience whose
registration is idempotent per run and whose absence is never fatal.
Membership SHALL be reconciled by the sync implementation, never
hand-curated. A repository's Ideation book SHALL be created — with contract
title, tags, chat framing, charter and grounding seeds, and its source
workspace record — on the first apply-mode sync where that repository has
ideation membership; a dry run SHALL report the pending creation without
mutating the provider. At implementation the legacy shared Ideation book
leaves the sync's book set; after per-repository parity is verified the
legacy book and its `xf-ideation` alias SHALL be retired by a recorded
manual act, and the alias SHALL NOT be repointed to any successor book.

#### Scenario: An ideation document projects into its owning repository's book
- **WHEN** a document with `brainstorm` or `staged` status lives in governed repository R
- **THEN** the sync projects its source into R's Ideation book
- **AND** no other repository's Ideation book receives it

#### Scenario: A repository gains its first ideation document
- **WHEN** an apply-mode sync finds a governed repository with status-derived ideation membership and no existing book with the contract title
- **THEN** the sync MUST create the book, apply the contract title, tags, and chat framing, seed charter and grounding, write its source workspace record, and project into it in the same run
- **AND** a dry-run sync over the same state MUST report the pending creation and MUST NOT mutate the provider

#### Scenario: A repository has seeds but no ideation documents
- **WHEN** a governed repository has zero `brainstorm` or `staged` documents
- **THEN** no Ideation book is created for it, regardless of charter or grounding seeding rules

#### Scenario: A book's alias is missing on this machine
- **WHEN** the sync runs on a machine whose local alias store lacks a book's alias
- **THEN** the sync resolves the book by its contract title and re-registers the alias
- **AND** the missing alias MUST NOT abort the book or the run

#### Scenario: A document changes lifecycle state
- **WHEN** a governance document's `Status:` header changes to a state mapped to a different book
- **THEN** the next sync MUST remove its source from the previous book and add it to the book mapped for its new state and owning repository

#### Scenario: A source is added by hand
- **WHEN** a source matching the managed title prefixes exists in a lifecycle notebook without a corresponding repo document
- **THEN** the sync MUST remove it (or report it when running in dry-run mode)

#### Scenario: A document's content changes without a state change
- **WHEN** a projected document is edited in the repository
- **THEN** the sync MUST replace the notebook source so notebook content matches the repository

#### Scenario: The legacy shared Ideation book after the split
- **WHEN** the per-repository book family is implemented
- **THEN** the legacy shared book is no longer a sync target in any mode
- **AND** after every governed repository's Ideation book holds parity with the corpus scan, the legacy book and the `xf-ideation` alias are retired by a recorded manual act
- **AND** no later sync creates, repoints, or writes to that alias

### Requirement: Authority framing
Every lifecycle notebook SHALL frame its content against the running system:
source titles carry a `[status]` prefix, a charter source states the
projection and the L1-synthesis rule, and the notebook chat configuration
instructs answers to distinguish running-system claims from proposals.

A source title is also the projection's IDENTITY KEY. The sync derives a
desired set keyed by document path but reconciles it against a book's live
source list BY TITLE, and holds each title at one source. The title
derivation SHALL therefore be INJECTIVE over each book's desired set: every
projected document SHALL receive a title distinct from every other projected
document's, so that a book holds exactly one source per member document and
no member is silently displaced by a namesake. A derivation from a
document's file stem ALONE is not injective, and a filename-by-filename
exception to it is not a rule — the obligation is stated over the whole
derived set precisely so that the next repeated stem is answered by the rule
rather than by a further exception.

The derivation SHALL qualify a stem with the SHORTEST repository-relative
path suffix that distinguishes the document from every other projected
document of the same repository, and a `README` stem SHALL carry no fewer
than its parent directory. The uniqueness scope SHALL be the repository's
whole projected document set rather than one book or one lifecycle status,
so that a document is never retitled because a same-stem sibling's `Status:`
header changed. The `[spec]` and `[grounding]` title families are keyed by
the capability directory name and by a fixed document set rather than by a
file stem, and SHALL be outside this scope.

The sync's parity mode SHALL prove membership at the DOCUMENT level, not at
the title level. Comparing a set of derived titles against a set of live
titles cannot observe a document that never received a title of its own, so
equality of those two sets alone SHALL NOT be reported as parity; the mode
SHALL report a derived title carrying more than one document as a parity
FAILURE that names those documents.

#### Scenario: An idea is discussed in chat
- **WHEN** notebook chat answers a question involving `[brainstorm]`, `[staged]`, or `[draft]` sources
- **THEN** the configured framing MUST cause the answer to label those claims as proposals layered on the running system, not current behavior

#### Scenario: Output is consumed downstream
- **WHEN** any lifecycle notebook output (answer, report, mind map, audio) is used in xFactory work
- **THEN** it carries `L1 notebook synthesis` authority per the source-workspaces model and MUST NOT directly drive gates, memory, policy, or customer-facing output

#### Scenario: Two documents of one repository share a file stem
- **WHEN** two or more projected documents of the same repository derive the same bare stem
- **THEN** each MUST receive a distinct title, qualified by the shortest repository-relative path suffix that distinguishes it from the others
- **AND** the book MUST hold one source per document, never one source standing for several
- **AND** the sync MUST NOT record a document as synced in its manifest unless that document holds a source of its own

#### Scenario: A stem repeats but the documents carry different statuses
- **WHEN** two documents of one repository share a stem and their `Status:` headers place them in different books
- **THEN** both MUST still be qualified, because the uniqueness scope is the repository's whole projected set
- **AND** a later change to either document's status MUST NOT change either title

#### Scenario: Parity is proven over documents
- **WHEN** the parity mode compares the corpus scan against a live book
- **THEN** it MUST report a derived title that carries more than one document as a parity failure naming those documents
- **AND** a book whose live title set equals the derived title set MUST NOT be reported as at parity while any derived title carries more than one document

#### Scenario: The derivation changes and titles move
- **WHEN** a projected document's derived title changes because the derivation changed
- **THEN** the next apply-mode sync MUST delete the source carrying the old title and add one carrying the new title
- **AND** the manifest MUST carry the new title for that document
- **AND** a dry run over the same state MUST report those operations without mutating the provider

### Requirement: Grounding context
Every lifecycle notebook SHALL include the grounding source set — the
document lifecycle doc, the terminology and topology doc, and the
architecture doc — with `[grounding]` titles, regardless of those documents'
own lifecycle states, so chat can compare ideas against the system's shape.

#### Scenario: Grounding doc changes state
- **WHEN** a grounding document's own `Status:` changes
- **THEN** it remains in every book under its `[grounding]` title while also appearing in its state's book under its `[status]` title

### Requirement: Projection implementation ownership
`openxFactory` SHALL own this projection contract, the workflow
documentation, and the conforming sync implementation
(`scripts/sync-notebooklm-books.py`). Book identity, charter text, title
prefixes, and chat framing SHALL be treated as contract conformance, not
implementation preference.

The sync SHALL run under the install's DECLARED hosting identity, selecting the `nlm` CLI profile bound to that identity rather than taking the tool's default profile. Which account the projection is created in is contract conformance, not an incidental property of the host the sync happens to run on: the CLI is profile-aware, so the selection is between existing mechanisms, and an implementation that cannot name the account it is writing to cannot claim conformance.

#### Scenario: The sync implementation is modified

- **WHEN** the sync implementation changes book definitions, prefixes, charter, exclusions, or chat framing
- **THEN** the change MUST be preceded by an OpenSpec delta to this capability

#### Scenario: A workspace names the sync manager

- **WHEN** a lifecycle notebook declares its `managed_by` implementation
- **THEN** the declared path resolves inside openxFactory, and the invocation is run from the workspace root against every pinned repo

#### Scenario: The sync runs for an install with a declared hosting identity

- **WHEN** the sync runs against an install that declares a hosting identity
- **THEN** every CLI invocation it makes is bound to that identity's profile
- **AND** a run that cannot resolve the declared identity's profile fails rather than silently falling back to the default profile

### Requirement: Hybrid analysis notebooks
The lifecycle notebook projection SHALL support temporary hybrid NotebookLM
notebooks that combine exactly one Canon release line with exactly one origin
idea or proposal-support target. The origin target SHALL be a brainstorm folder
under `ideation/brainstorm/<topic>/`, a staged folder under
`ideation/staging/<topic>/`, or an active proposal folder under
`openspec/changes/<change-id>/supporting-docs/`. Hybrid notebooks SHALL be
derived analysis workspaces, not canonical lifecycle books.

#### Scenario: A brainstorm hybrid is created
- **WHEN** an operator creates a hybrid notebook for `ideation/brainstorm/<topic>/`
- **THEN** the hybrid MUST identify the Canon release line being compared
- **AND** the hybrid MUST identify `ideation/brainstorm/<topic>/` as the origin folder for any returned source material

#### Scenario: A staged hybrid is created
- **WHEN** an operator creates a hybrid notebook for `ideation/staging/<topic>/`
- **THEN** the hybrid MUST identify the Canon release line being compared
- **AND** the hybrid MUST identify `ideation/staging/<topic>/` as the origin folder for any returned source material

#### Scenario: A proposal hybrid is continued
- **WHEN** a staged topic moves into `openspec/changes/<change-id>/supporting-docs/`
- **THEN** its hybrid MUST identify the active supporting-documents folder as the new origin for returned source material
- **AND** the hybrid MUST retain the Canon release line being compared

#### Scenario: Hybrid output is consumed
- **WHEN** any chat answer, note, report, mind map, audio, or other output from a hybrid notebook is used in xFactory work
- **THEN** the output MUST carry `L1 notebook synthesis` authority
- **AND** it MUST NOT decide policy, memory, release scope, OpenSpec approval, or customer-facing output

### Requirement: Hybrid source return imports
Hybrid notebook source return SHALL be based on NotebookLM source membership.
Any non-seed source in a hybrid notebook SHALL be eligible to import back into
the hybrid's origin folder. Eligible sources include notes converted to
sources, web sources, sources discovered through NotebookLM research, files,
Drive sources, and any other NotebookLM source type exposed to the importer.
NotebookLM notes that have not been converted to sources SHALL remain scratch
material inside NotebookLM and SHALL NOT be imported.

#### Scenario: A note is converted to a source
- **WHEN** a human creates a NotebookLM note inside a hybrid notebook and converts that note to a source
- **THEN** the converted source MUST be eligible for import into the hybrid's origin folder
- **AND** the source title MUST NOT need manual renaming or export tagging

#### Scenario: A source is added through research or upload
- **WHEN** an operator adds a web, research, file, Drive, or other source to a hybrid notebook after the seed set is created
- **THEN** that source MUST be eligible for import into the hybrid's origin folder
- **AND** the importer MUST preserve the NotebookLM source title and source id in the imported entry

#### Scenario: A scratch note remains unconverted
- **WHEN** a NotebookLM note exists only as a note and has not been converted into a source
- **THEN** the importer MUST NOT import that note into the repository

### Requirement: Hybrid seed source exclusions
Hybrid importers SHALL skip seed sources that exist only to provide analysis
context. Seed sources include the hybrid charter, copied Canon sources,
grounding sources, and originally projected lifecycle sources. Managed seed
titles SHALL include `00 [charter]`, `00 [hybrid charter]`, and titles
beginning `[brainstorm]`, `[staged]`, `[draft]`, `[ratified]`, `[standard]`,
`[spec]`, or `[grounding]`.

#### Scenario: Canon context exists in the hybrid
- **WHEN** a hybrid notebook contains copied Canon sources with `[ratified]`, `[standard]`, or `[spec]` titles
- **THEN** the importer MUST NOT write those sources back into the origin brainstorm or staged folder as new ideas

#### Scenario: Grounding context exists in the hybrid
- **WHEN** a hybrid notebook contains `[grounding]` sources or the lifecycle charter source
- **THEN** the importer MUST treat those sources as seed context
- **AND** it MUST NOT import them as new source material

### Requirement: Imported source material provenance
Every imported hybrid source entry SHALL be written to the origin folder as
governed lifecycle material. The imported file SHALL carry the origin lifecycle
status (`brainstorm` for brainstorm origins, `staged` for staged origins, and
`draft` for active proposal supporting-document origins), `Kind: reference`,
the source workspace id or alias, `Authority: L1 notebook synthesis`, the
NotebookLM source id, and the NotebookLM source title. An operator MAY classify
immutable evidence as `record`. Import MUST be idempotent by NotebookLM source
id.

#### Scenario: A source imports into a brainstorm origin
- **WHEN** an eligible source is imported from a hybrid whose origin is `ideation/brainstorm/<topic>/`
- **THEN** the imported file MUST be written under that origin folder
- **AND** the imported file MUST carry `Status: brainstorm`

#### Scenario: A source imports into a staged origin
- **WHEN** an eligible source is imported from a hybrid whose origin is `ideation/staging/<topic>/`
- **THEN** the imported file MUST be written under that origin folder
- **AND** the imported file MUST carry `Status: staged`

#### Scenario: A source imports into a proposal origin
- **WHEN** an eligible source is imported from a hybrid whose origin is an active change's `supporting-docs/` folder
- **THEN** the imported file MUST be written under that folder
- **AND** the imported file MUST carry `Status: draft` unless explicitly classified as immutable evidence

#### Scenario: The importer is run twice
- **WHEN** a NotebookLM source id already appears in imported lifecycle material
- **THEN** a subsequent import run MUST skip that source id
- **AND** it MUST NOT duplicate the imported entry

### Requirement: Hybrid import review gate
Changes to hybrid notebook import behavior SHALL be review-ready only after
implementation tests for the touched tooling pass, the owning repo validation
suite passes, and OpenSpec validation passes in that order.

#### Scenario: An implementation change modifies hybrid import behavior
- **WHEN** a change modifies the hybrid importer, seed-source rules, imported file shape, or return-path workflow
- **THEN** local implementation tests for the importer MUST run before OpenSpec validation
- **AND** the owning repo validation suite MUST pass before the change is marked ready for review

### Requirement: Hybrid finalization before proposal archive
An active proposal hybrid SHALL receive one final source-return import before
its supporting documents are packaged. After the proposal archives, the hybrid
SHALL be retired from active analysis use.

#### Scenario: A proposal reaches its archive gate
- **WHEN** an active change with a proposal hybrid is ready to archive
- **THEN** the archive checklist MUST record a final source-return import
- **AND** packaging MUST run only after that import completes

### Requirement: Corpus scan scope
The LIFECYCLE BOOKS' projection — one Ideation book per governed repository, plus the shared Working Drafts and Canon books — SHALL scan exactly the governed corpus at the default branch: the openxFactory repository and each DomainxFactory checked out under `xFactories/`. Nested git working copies below a scanned repository root — feature-branch worktree checkouts (including `<repo>-worktrees/` containers and branch-session worktrees), embedded clones, and nested submodule installs — MUST be excluded from every lifecycle book, so an unmerged or duplicate checkout can never project sources into one: a lifecycle book IS the lifecycle projection, and a projection of unmerged work is a misprojection. Branch-session notebooks (`xf-session-<topic>`) SHALL be the ONLY notebook surface permitted to read a worktree; they are never lifecycle books, they MUST NEVER contribute a source, a title, or a repository name to one, and their existence MUST NOT relax the exclusion above for any book. OpenSpec change artifacts remain excluded from status scanning while promoted capability specs project into the Canon book, and deliberate-violation test fixture corpora remain excluded.

#### Scenario: A worktree container sits under the scan root
- **WHEN** a directory under `xFactories/` holds git worktree checkouts rather than being a governed repository
- **THEN** the lifecycle-book sync MUST NOT scan it
- **AND** no source or repository title may derive from its contents

#### Scenario: A nested working copy sits inside a governed repository
- **WHEN** a directory below a scanned repository root carries its own `.git` entry
- **THEN** documents below that directory MUST be excluded from every lifecycle book

#### Scenario: A governed document also exists in a checkout
- **WHEN** an excluded working copy contains a document that also exists in the governed corpus
- **THEN** only the governed copy projects and no duplicate or colliding source title is created

#### Scenario: A canon book is offered a branch session's drafts
- **WHEN** a branch session holds unmerged drafts in its worktree and any lifecycle book — Ideation, Working Drafts, or Canon — is synced
- **THEN** those drafts MUST NOT appear in any lifecycle book, under any title
- **AND** they MUST reach a lifecycle book only after the session's pull request merges to the default branch

### Requirement: Projection capacity guard
The sync implementation SHALL treat the platform per-notebook source cap as
a first-class, preflighted constraint over each book's projected occupancy —
defined as the desired managed set plus the charter plus every unmanaged
source observed in that book's source listing — where the cap is a named
constant declared in the sync implementation and recorded in the workflow
documentation. The sync SHALL warn when a book's remaining headroom (cap
minus projected occupancy) falls to thirty sources or fewer, naming the
book, the occupancy, the cap, and — for any book with no successor split
defined by this capability — the owed remedy: a further OpenSpec delta to
this capability defining that book's split. When projected occupancy would
exceed the cap, the sync SHALL project the deterministic in-cap prefix of
the desired set (stable path order), report the book and the exact excess
sources that cannot project, complete every other book, and exit nonzero.
Predictable, preflightable conditions — a book over its cap, an
unresolvable book, a refused notebook creation — SHALL be contained to the
affected book and reported; they SHALL never abort the remaining books,
fail silently, or surface first as a provider error mid-book.

#### Scenario: A book's headroom runs low
- **WHEN** a book's projected occupancy comes within thirty sources of the cap
- **THEN** the sync emits a warning naming the book, the projected occupancy, and the cap
- **AND** if no successor split is defined for that book, the warning names the owed OpenSpec delta

#### Scenario: A book would exceed the cap
- **WHEN** a book's projected occupancy exceeds the platform cap
- **THEN** the sync projects only the deterministic in-cap prefix of the desired set and reports the exact excess sources
- **AND** it completes the sync of every other book
- **AND** the run exits nonzero

#### Scenario: Unmanaged sources occupy real capacity
- **WHEN** a book holds hand-added sources that the reconciliation deliberately preserves
- **THEN** those sources count toward projected occupancy in both the warning and the overflow computation

#### Scenario: A book fails a preflightable condition
- **WHEN** a book cannot be resolved or its creation is refused by the provider
- **THEN** the sync reports that book's condition, skips it, completes every other book, and exits nonzero

### Requirement: The session namespace is reconciled against live sessions
The sync SHALL provide a RECONCILIATION mode over the `xf-session-` notebook namespace that retires the notebook of every session that no longer exists, because a branch session's notebook is bound to a LIVE session and a session can end without either governed ending — a probe or a crash-residue cleanup removes a worktree and a branch directly, so no abandon runs and no retirement is recorded. Without reconciliation such a notebook survives its session indefinitely on the hosting account, holding quota and misstating the set of live sessions to every later reader.

Dead SHALL be established FORWARD, never by inverting a title. The alias derivation is lossy — it strips the `draft/` prefix and lowercases — so a notebook title cannot be resolved back to a `(repository, branch)` key. The mode SHALL compute the alias of every LIVE session, using the same joint worktree-and-branch liveness signal the session bootstrap uses, and SHALL treat an `xf-session-` notebook that matches no live session's alias as dead. A notebook matching a live session's alias SHALL never be retired.

Liveness SHALL be sought across EVERY WORKTREE of each session repository, not only its canonical checkout. A session's worktree container is keyed on the checkout the session was opened FROM, and sessions are routinely opened from a feature worktree, so a run that asks only the canonical checkout finds no sessions there — a legitimate answer for that checkout, and indistinguishable from the sessions living in another worktree of the same repository. The repository's own worktree list is what makes the enumeration completable, and a run that cannot read it SHALL treat that as an error rather than as an answer.

The mode SHALL FAIL CLOSED on incomplete knowledge. A session repository that cannot be enumerated — an absent checkout, a git failure, an unreadable worktree list, an unreadable session container — is indistinguishable from a repository whose sessions have all ended, and the difference cannot be recovered after a retirement. Any repository the run cannot enumerate SHALL refuse the whole reconciliation, naming the repository and the reason, and SHALL retire nothing.

Where the run resolves NO session repositories in scope at all, it SHALL retire nothing: a workspace carrying none of the repositories a session notebook could belong to has no standing to judge one, so pointing the mode at the wrong root is inert rather than destructive.

The mode SHALL be scoped to the session repositories of the workspace it is run against. One hosting account serves every workspace of its install, so a session notebook whose repository segment names a repository this workspace does not carry belongs to another workspace's sessions; such a notebook SHALL be reported as out of scope and SHALL NOT be retired. This scoping rule is unchanged by the hosting identity becoming declared: what was previously true of an undeclared shared account is true of a declared one, and the reconciliation SHALL be performed within the declared account rather than across accounts.

The mode SHALL report by default and act only when application is requested, and SHALL retire through the same adapter operation the governed endings use rather than a scratch-namespace delete, so the session-prefix and key-derived-title guards apply identically. The report SHALL state, for each dead notebook, how many sources a retirement would discard, because a notebook carrying hand-added sources is the one case where retirement loses something a human may want first.

#### Scenario: A session torn down outside a governed ending is reconciled
- **WHEN** the reconciliation runs against a workspace where an `xf-session-` notebook matches no live session's alias
- **THEN** the notebook is reported as dead, naming its title and the number of sources a retirement would discard
- **AND** with application requested it is retired through the session retire operation
- **AND** the run reports the retirement as its own act rather than as a governed ending

#### Scenario: A live session's notebook is never retired
- **WHEN** the reconciliation runs while a session is live
- **THEN** that session's notebook matches a live alias and is left untouched in both report and apply modes

#### Scenario: A session opened from a feature worktree is live
- **WHEN** a session's worktree container belongs to a FEATURE worktree of a session repository rather than to that repository's canonical checkout
- **THEN** the reconciliation still finds it live and leaves its notebook untouched
- **AND** a run that examined only the canonical checkout MUST NOT report it dead

#### Scenario: No session repository in scope retires nothing
- **WHEN** the reconciliation resolves no session repositories at all for the workspace it is run against
- **THEN** every session notebook is out of scope and nothing is retired

#### Scenario: A repository that cannot be enumerated refuses the run
- **WHEN** any session repository in the workspace cannot be enumerated for live sessions
- **THEN** the reconciliation refuses, names the repository and the reason, and retires nothing
- **AND** the refusal is reported as a refusal rather than as an empty result

#### Scenario: Another workspace's session notebook is out of scope
- **WHEN** an `xf-session-` notebook names a repository this workspace does not carry
- **THEN** it is reported as out of scope and is never retired

#### Scenario: An adapter without the retire operation refuses
- **WHEN** application is requested against an adapter exposing no session retire operation
- **THEN** the run refuses loudly and retires nothing, rather than reporting a retirement it did not perform

### Requirement: Branch-session notebooks
A branch session MAY carry ONE per-session NotebookLM notebook, named `xf-session-<topic>` for the session's tile, whose sources SHALL be synced FROM the session's git WORKTREE rather than from the served checkout, and it SHALL NOT be one of the lifecycle books. A session notebook's title MUST NOT use the `xf-wb-` workbench reference-set prefix: the two namespaces SHALL be DISJOINT, so the reference-set orphan sweep — which deletes every `xf-wb-*` notebook that no live workbench manifest binds — can never take a live session's notebook as a candidate, and a session needs no workbench manifest to survive it. A session notebook SHALL be created when its session starts and SHALL be RETIRED when the session ends by merge or abandon, torn down together with the worktree and the session's registry entry — its life is the session's life, so a stale notebook cannot outlive the branch it projected. The workbench SHALL offer a "refresh notebook" session action that re-syncs the session notebook from the worktree after edits, granting no authority beyond the sync the projection tooling already performs. Hybrid source-return imports for a session notebook SHALL write into the origin folder INSIDE THE SESSION WORKTREE, landing on the session branch as ordinary working material committed with the session's gate action, and the imported file's header contract — origin lifecycle status, `Kind: reference`, source workspace, `Authority: L1 notebook synthesis`, NotebookLM source id and title, and idempotency by source id — SHALL apply verbatim and unchanged. A session notebook's output SHALL carry `L1 notebook synthesis` authority exactly as a hybrid's does and MUST NOT decide policy, memory, release scope, OpenSpec approval, or customer-facing output. This is a projection-TOOLING capability only: NotebookLM knows uploaded SOURCES and not git, so nothing in the notebook family's contract changes beyond declaring the rule and the naming.

#### Scenario: A session notebook is created and synced
- **WHEN** a branch session starts with a session notebook
- **THEN** the notebook MUST be created as `xf-session-<topic>` for that tile and its sources MUST be synced from the session's worktree, not from the served checkout
- **AND** its title MUST NOT carry the `xf-wb-` reference-set prefix, so the workbench orphan sweep never treats it as a candidate

#### Scenario: A session's drafts change
- **WHEN** a human edits documents in the session worktree and invokes the refresh-notebook action
- **THEN** the session notebook's sources MUST be re-synced from the worktree so the notebook matches the branch's current drafts

#### Scenario: A session ends
- **WHEN** a branch session ends by merge or by abandon
- **THEN** its session notebook MUST be retired — torn down with the worktree and the session's registry entry — and MUST NOT continue to project the branch

#### Scenario: A session notebook returns source material
- **WHEN** an eligible non-seed source is imported from a session notebook
- **THEN** it MUST be written into the origin folder inside the SESSION WORKTREE and land on the session branch
- **AND** the imported file's header contract and idempotency rules MUST apply exactly as they do for a hybrid import on `main`

#### Scenario: Session-notebook output is consumed
- **WHEN** any answer, note, report, mind map, or audio from a session notebook is used in xFactory work
- **THEN** it MUST carry `L1 notebook synthesis` authority and MUST NOT decide policy, memory, release scope, OpenSpec approval, or customer-facing output

### Requirement: The hosting record declares where the hosting identity's credential is held, by reference only
An install declaring an operator-hosted projection SHALL record WHERE that account's credential is held — a reference to the governed custody binding that resolves it — and SHALL NOT record the credential itself. The hosting record already names the account; naming its custody is what makes the account operable by someone other than whoever created it, which is the whole point of moving off a personal identity.

The reference SHALL identify the binding, not the secret's value, and SHALL be sufficient to find the credential through the governed path and insufficient to obtain it without one. A password, a recovery code, a TOTP seed, a session cookie or an exported profile SHALL NOT appear in the hosting record, in the repository, or in any projection artifact.

A SELF-HOSTED declaration SHALL NOT be required to name custody. An individual operating their own account under their own authority has no operator to bear the obligation, exactly as the two-case model already holds elsewhere.

The record SHALL state the custody's honest reach: which secrets the binding covers, and — where the platform's sign-in cannot be performed from that material alone — that the remaining step is interactive. A custody reference that implies unattended access the install does not have is worse than none, because it invites a reader to plan on it.

#### Scenario: An operator-hosted install declares custody
- **WHEN** an install declares the operator-hosted case
- **THEN** its hosting record carries a reference to the governed custody binding for that account's credential
- **AND** the record carries no credential material of any kind

#### Scenario: A secret is placed in the hosting record
- **WHEN** a password, recovery code, TOTP seed, session cookie or exported profile is written into the hosting record
- **THEN** the record is non-conforming, and the remedy is a binding reference rather than redaction in place

#### Scenario: A self-hosted install declares no custody
- **WHEN** an individual declares the self-hosted case against their own account
- **THEN** the absence of a custody reference is conforming, because no operator exists to bear the obligation

#### Scenario: The custody covers less than the sign-in needs
- **WHEN** the declared custody holds material insufficient to complete the platform's sign-in unaided
- **THEN** the record says so plainly, naming the interactive step that remains
- **AND** the projection is not described as having unattended access to its own hosting account

### Requirement: The projection's hosting identity is declared at install
An xFactory install SHALL declare which Google identity hosts its NotebookLM projection, as an intake fact of standing that install up rather than an incidental consequence of whoever authenticated the `nlm` CLI first. The declaration SHALL name exactly one of two cases: OPERATOR-HOSTED, a company-owned account belonging to the operating party, or SELF-HOSTED, an individual installer's own personal account. Both cases are legitimate; the second is not a degraded form of the first.

The declared identity SHALL be a Google USER account. This is a platform constraint, not a preference: NotebookLM exposes no API and a provider service account cannot drive its consumer web UI, so no service-principal identity can host a projection at all.

An operator-hosted declaration SHALL name a Google Workspace user account in a domain the operating party controls, and SHALL NOT name a consumer account merely designated as the company's. A consumer account carries a personal recovery path back to one individual, no administrative console, and no enforceable organizational policy — it would be the operator-hosted case wearing the self-hosted case's risk.

An install that declares NOTHING is NONCONFORMING with this requirement — a transition state, not a third case. Every install predating this requirement is in it, so the sync SHALL NOT break on it: it falls back to the CLI's default profile, which is today's behavior. What it SHALL NOT do is present that install as governed. The projection SHALL be reported as carrying no declared hosting identity, and the undeclared state SHALL be reported as unmet rather than as a legitimate configuration, so an implementation and a validator agree about what is expected of it.

#### Scenario: An operating party declares the company account
- **WHEN** an install's intake declares operator-hosted and names a Google Workspace user account in the operating party's own domain
- **THEN** the declaration is valid, and every book, alias and session notebook of that install is created under the named account
- **AND** Opensoft's own install is such a declaration, naming `xFactor001@opensoft.one`

#### Scenario: An individual installer keeps their own books
- **WHEN** a person installs the system for themselves and declares self-hosted against their own personal Google account
- **THEN** the declaration is valid and complete, no company account is implied, and no share-approval governance obligation attaches

#### Scenario: A consumer account is offered as the company account
- **WHEN** an operator-hosted declaration names a consumer Google account rather than a Workspace user in a controlled domain
- **THEN** the declaration is refused, naming the missing administrative control rather than the account's label

#### Scenario: A service account is offered as the hosting identity
- **WHEN** a declaration names a provider service account or any non-user principal
- **THEN** the declaration is refused on the platform constraint: NotebookLM has no API and the identity could never drive the projection

#### Scenario: An install has not declared yet
- **WHEN** no hosting identity is declared for an install
- **THEN** the sync runs under the CLI's default profile as it does today, rather than breaking
- **AND** the install is reported as NOT MEETING this requirement — a transition state, never a third legitimate case

### Requirement: Access to the projection is shared out from the hosting account, and each share act is recorded
Where an install declares the operator-hosted case, individual users SHALL reach the projection only through an explicit share-out FROM the hosting account, and SHALL NOT each authenticate independently against the hosting account's own credentials. A shared login is not an access model: it defeats attribution, cannot be revoked per person, and is exactly the posture this declaration exists to retire.

A pending share request SHALL be decided by a designated company-policy actor as a GOVERNED ACT, in the hosting account's own interface, and SHALL NOT be left to whoever happens to read the account's mail. The decision SHALL be recorded whether it grants or denies.

The record of a granted share act SHALL BE the share-out roster entry itself, not a separate audit trail beside a list. Approving a request writes or updates the roster; denying one is recorded in the same lane.

A roster entry SHALL carry the hosting account, the person, the book or alias, the role, the grant time and the granting actor. Its UNIQUENESS SHALL be keyed on the stable scope-and-principal triple `(hosting_account, user, book_or_alias)`, with `role`, `granted_at` and `granted_by` held as ATTRIBUTES of that entry rather than as parts of its key. A re-approval, a role change, or a grant by a different actor therefore UPDATES the one live entry instead of creating a second: a roster that is the record of current access cannot simultaneously assert a stale grant and a current one for the same person on the same book. Superseded decisions SHALL be retained as history rather than as competing live entries.

The grantee SHALL be part of the key. That is the whole structural difference from the client-identity roster, whose uniqueness tuple omits the grantee and therefore collides when one scope is granted to two people.

An entry SHALL reference a governed persona wherever the identity-brokering family resolves one for that human, falling back to a bare address only where no persona resolves.

The share-out roster SHALL be its own artifact and SHALL NOT be carried by the client-identity roster, whose uniqueness key admits one principal against many scopes while a share-out list is the transposed shape — one scope against many principals.

Detection and relay of pending requests MAY be automated if and when the platform offers a surface for it; the approval SHALL remain a governed human act either way. No obligation in this requirement depends on an administrative or sharing API that NotebookLM does not currently expose.

#### Scenario: A share request is approved
- **WHEN** a person requests access to a book hosted by a declared operator-hosted account, and the designated company-policy actor approves it
- **THEN** the share is granted from the hosting account
- **AND** a share-out roster entry records the account, the person, the book or alias, the role, the grant time and the granting actor
- **AND** the entry references that person's governed persona where one resolves

#### Scenario: A share request is denied
- **WHEN** the designated actor denies a pending request
- **THEN** the denial is recorded in the same lane as approvals, rather than leaving the request to expire unrecorded

#### Scenario: Two people are granted the same book
- **WHEN** two different people are granted access to one book on one hosting account
- **THEN** both entries stand as distinct roster records, because the grantee is part of the key

#### Scenario: An existing grantee's access is re-decided
- **WHEN** a person already holding a recorded grant on a book is re-approved, has their role changed, or is granted again by a different actor
- **THEN** the existing entry is UPDATED, carrying the new role, grant time and granting actor
- **AND** no second live entry is created, so the roster never asserts a stale grant beside the current one
- **AND** the superseded decision is retained as history

#### Scenario: Individual authentication against the hosting account is attempted
- **WHEN** a user is given the hosting account's own credentials instead of a share
- **THEN** that is a violation of this requirement, not an alternative access route

### Requirement: A hosting-account migration re-derives, proves parity, then retires the originals by recorded act
Moving a projection from one hosting account to another SHALL be performed as a RE-DERIVATION, not as a data migration: membership is always derived from `Status:` headers and never hand-curated, so the books under the new account are reconstructed from the corpus rather than copied.

Parity SHALL be proven BEFORE anything is retired, and SHALL be established against the CORPUS SCAN rather than against the legacy books, which are the very artifact whose fidelity is in question. Parity SHALL consist of per-book title-set equality plus a union reconciliation against the corpus scan, followed by a final dry run showing zero pending additions, deletions or updates.

The migration SHALL account for the SESSION namespace explicitly. A lifecycle-book reconciliation does not create session notebooks, so every live `xf-session-*` notebook SHALL be re-created under the new account — through a bulk migration mode or per-session runs — before the old account is retired. A migration that moves the lifecycle books alone leaves live sessions hosted on the account being abandoned.

The migration SHALL replace each book's workspace record rather than merely retiring it. A re-created book keeps its derived key and therefore its record id, but carries a NEW provider notebook id; a registration step that refuses to overwrite an existing record, combined with retiring that record, would leave the new book with no active workspace record at all. The replacement SHALL be explicit and SHALL leave exactly one active record per live book.

Only once parity holds SHALL the previous account's books be RETIRED BY RECORDED ACT — archive-renamed, and their aliases DELETED rather than repointed. Retirement SHALL be declared, never implicit: a book left merely untouched is a book no one has judged, which is how the shared Ideation book reached its source cap before anyone called it old.

The retirement SHALL NOT retire the workspace record the replacement step just made current. Because the record id is derived from the book's key and that key is unchanged, the replaced record IS the live book's registration; retiring it would reproduce the unregistered-book failure the replacement exists to prevent. What is retired is the legacy PROVIDER NOTEBOOK, and the retirement is preserved in the recorded act and in the record's own history. Only where a migration leaves a genuinely SEPARATE legacy record — a distinct record id, as the 2026-08-10 per-repo split produced — SHALL that record be retired in place.

#### Scenario: The lifecycle books are re-derived under a new account
- **WHEN** an install's declared hosting identity changes and the sync next applies
- **THEN** the lifecycle books are re-created under the newly declared account from the corpus, as a re-derivation

#### Scenario: Parity is claimed against the legacy books
- **WHEN** a migration proposes to prove parity by comparing the new books against the old ones
- **THEN** that is insufficient: parity is established against the corpus scan, with a final zero-pending dry run

#### Scenario: Sessions are live at cutover
- **WHEN** any branch session is live when the hosting account changes
- **THEN** each live session's notebook is re-created under the new account before the old account is retired
- **AND** a lifecycle-only run is not accepted as having migrated them

#### Scenario: A re-created book collides with its own workspace record
- **WHEN** a re-created book resolves to an existing record id holding a different provider notebook id
- **THEN** the record is explicitly replaced, leaving one active record for the live book
- **AND** retiring the old record without that replacement is refused as leaving the book unregistered

#### Scenario: The previous account's books are retired
- **WHEN** parity has been proven and the new account's books are live
- **THEN** the previous books are archive-renamed and their aliases deleted rather than repointed
- **AND** the retirement is recorded as an act rather than left implicit

#### Scenario: The retirement is asked to retire the replacement record
- **WHEN** the retirement step would retire a workspace record whose id the replacement step reused for the live book
- **THEN** it is refused, because that record is the live book's registration and retiring it leaves the book unregistered
- **AND** the legacy provider notebook is retired instead, with the act preserved in the record's history

#### Scenario: A migration leaves a genuinely separate legacy record
- **WHEN** the migration produces a successor under a NEW record id, leaving the legacy record distinct and unreferenced
- **THEN** that legacy record is retired in place, as the 2026-08-10 split precedent did

