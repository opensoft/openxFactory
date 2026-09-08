# Lifecycle Notebook Projection

Status: standard
Kind: process
Backed by: [openspec/specs/lifecycle-notebook-projection/spec.md](../openspec/specs/lifecycle-notebook-projection/spec.md) (promoted from the archived add-lifecycle-notebook-projection change)
Extended by: add-workbench-branch-sessions (ratified 2026-07-26) — section 9,
branch-session notebooks, plus the main-only rule made explicit in section 1
Amended by: split-ideation-book-per-repo (ratified 2026-08-10) — per-repo
Ideation books, title-based resolution, the capacity guard, and the legacy
shared Ideation book's retirement, after the 300-source cap incident
Amended by: reconcile-lifecycle-books-count (ratified 2026-08-24) — the fixed
"three books" count retired for the topology the split ratified
Amended by: add-projection-title-uniqueness (ratified 2026-08-25) — section 2's
title rule made INJECTIVE over each repository's whole projected set, and
`--parity` amended to prove membership at the document level
Repository context: openxFactory
Purpose: define the full NotebookLM workflow for the governance corpus — how
document lifecycle states project into derived notebooks, how those notebooks
are framed against the running system, and how the sync is operated.

Authority model: [NotebookLM Source Workspaces](notebooklm-source-workspaces.md).
Lifecycle states: [Document Lifecycle](document-lifecycle.md).
Reference implementation: `scripts/sync-notebooklm-books.py` (in this
repository; invoked from the workspace root as
`openxFactory/scripts/sync-notebooklm-books.py`).

## 1. The Books

The NotebookLM books project the family's governance corpus by lifecycle
state. Membership is always derived from `Status:` headers — never
hand-curated.

**Which Google account holds them is DECLARED, not incidental**
(`add-notebook-projection-identity`, 2026-08-23). An install declares its
hosting identity in a record whose LOCATION IT CONFIGURES
(`adopt-configured-notebook-hosting-identity`, 2026-09-08 — the committed
`examples/notebook-projection-hosting.yaml` is a synthetic example of that
record, never an install's declaration), in one of two
legitimate cases: **operator-hosted**, a company-owned Google Workspace USER
account in a domain the operating party administers, or **self-hosted**, an
individual installer's own personal account. The identity must be a Google
*user* account — NotebookLM has no API and a service account cannot drive its
consumer web UI, so no service principal can host a projection. An install that
declares nothing is in a nonconforming transition state, not a third case: the
sync still runs under the CLI's default profile, but reports that the
projection is not governed by a declared account. Section 12 carries the
mechanics. Ideation is ONE BOOK PER GOVERNED REPOSITORY
(split-ideation-book-per-repo, after the shared book hit the platform's
300-source cap on 2026-08-10): each repo's ideation corpus gets its own full
cap, and growth in one domain can never block another's projection. A repo's
book is created lazily on the first apply-mode sync where the repo has
`brainstorm`/`staged` membership (seeds never create a book); creation
applies the title, tags, chat framing, charter + grounding, and the book's
source-workspace record in one run.

| Book | Statuses projected | Answers questions like |
| --- | --- | --- |
| `xFactory Ideation — <RepoName>` (one per governed repo) | `brainstorm`, `staged` in that repo | What are we considering here? How do ideas differ from the system today? |
| `xFactory — Working Drafts` | `draft` | What is the intended design? Where do drafts conflict? |
| `xFactory — Canon` | `ratified`, `standard`, promoted `openspec/specs/*/spec.md` | What is governed today? What would this idea change? |

Books are RESOLVED BY TITLE (the provider's truth). Aliases —
`xf-ideation-<repo-slug>` (repo name lowercased), `xf-drafts`, `xf-canon` —
are a machine-local CLI convenience, re-registered idempotently per run and
never fatal when absent. The legacy shared `xFactory — Ideation` book and
its `xf-ideation` alias are RETIRED: not a sync target, never repointed.

Excluded by design: `record` (immutable evidence), `superseded`, `retired`.
Scope: `openxFactory/` and `xFactories/*/`, skipping `.git`, `installs/`
(nested submodules), `openspec/changes/` (change artifacts have their own
lifecycle; promoted specs are included from `openspec/specs/`), and any
nested git working copy below a scanned repository root — feature-branch
worktree checkouts (`<repo>-worktrees/` containers, branch-session worktrees
included) and embedded clones — so unmerged or duplicate checkouts never
project into the books. The lifecycle books are **MAIN-ONLY without
exception**: a lifecycle book IS the lifecycle projection, so a book carrying
unmerged sources is not a stale book but a WRONG one, asserting lifecycle
states that do not exist. Section 9 is the only surface permitted to read a
worktree, and it is not a book.

## 2. Source Titles

Titles are the authority signal chat sees on every citation:

```text
[<status>] <repo>: <file stem>          e.g. [draft] MedxFactory: care-organization-hermes
[spec] openxFactory: <capability>        promoted capability specs
[grounding] openxFactory: <stem>         grounding set (section 3)
00 [charter] Read me first               workspace charter (section 4)
```

**A title is the projection's IDENTITY KEY, so the derivation is INJECTIVE.**
The sync derives a desired set keyed by document PATH but reconciles it
against a book's live sources BY TITLE, and holds each title at one source. So
two documents that derive one title are not two sources with the same label —
they are one source, and the loser is absent from the book while the manifest
records it as synced. Every projected document therefore receives a title
distinct from every other projected document's.

Title rule: a title carries the SHORTEST repository-relative path suffix that
distinguishes the document from every other projected document of the same
repository, and a `README` stem carries no fewer than its parent directory —
e.g. `[ratified] AdxFactory: ideation/README`. A stem that is already unique in
its repository stays bare. The uniqueness scope is the repository's WHOLE
projected set, not one book and not one lifecycle status, so a document is
never retitled because a same-stem sibling's `Status:` header moved. The
`[spec]` and `[grounding]` families sit outside that scope: they are keyed by a
promoted capability's directory name and by a fixed three-document set rather
than by a file stem, and neither can collide with one.

Worth knowing where you are reading it: the rule this replaced said "when the
file stem is `README` (or otherwise non-unique within a repo)" — the
parenthesis stated the general obligation and the implementation implemented
the example, special-casing the literal name `README` and letting everything
else fall through to a bare stem. Four MedxFactory staging topics shared one
source, and `--parity` compared title SETS, so it reported OK on books that
were missing documents. The obligation is now stated over the whole derived
set precisely so the next repeated stem is answered by the rule instead of by
a second exception, and parity proves membership at the DOCUMENT level
(`add-projection-title-uniqueness`, 2026-08-25).

## 3. Grounding Set

Every book carries these three docs under `[grounding]` titles regardless of
their own lifecycle state, so chat can compare any idea against the system's
shape:

- `docs/document-lifecycle.md`
- `docs/terminology-and-repo-topology.md`
- `docs/architecture.md`

A grounding doc also appears in its own state's book under its `[status]`
title; the duplication is intentional.

## 4. Charter And Chat Framing

Each book's first source is a charter (`00 [charter] Read me first`) stating:
the book is a derived projection; what each title prefix means; and that per
the source-workspaces model all notebook output is **L1 notebook synthesis**
— it may raise claims but never decides policy, memory, gates, or
customer-facing output.

Each book's chat is configured (`nlm chat configure <book> --goal custom`)
with the running-system framing: `[brainstorm]`/`[staged]` are ideas on top
of the running system, `[standard]`/`[spec]`/`[ratified]` describe the system
as governed, `[draft]` is intended but unratified; answers must label each
claim's origin and describe conflicts as proposed change from current, never
as fact.

Charter text and chat prompt are contract surface: they live in the reference
implementation as constants and change only through an OpenSpec delta to the
`lifecycle-notebook-projection` capability.

## 5. Sync Behavior

The sync reconciles desired state (repo scan) against actual state (notebook
source list), matched by title:

- **Add**: repo doc projected to a book it is not in.
- **Delete**: managed source (title starts `[` or is the charter) present in
  a book but no longer projected there — including hand-added strays.
- **Update**: repo content changed (SHA-256 tracked in the manifest) →
  delete + re-add.
- **Stage transition**: a status change is a delete from the old book plus an
  add to the new one on the next sync.

Operational properties: dry-run by default (`--apply` to execute; a missing
per-repo book reports `CREATE` on the dry run and mutates nothing);
idempotent (a no-op resync reports zero changes); rate-limited ~2s per
source operation; manifest at `<workspace-root>/.claude/nlm-sync-manifest.json`
(intentional local derived state — not committed; safe to delete, next apply
rebuilds it), keyed per book and FLUSHED AFTER EACH BOOK so an interrupted
run resumes as a no-op over finished books.

**Oversized documents** (issues #438, #462): a document above
`MAX_TEXT_ARG_BYTES` (100,000) cannot ride a single `--text` argv string, so it
uploads as a temp file and is renamed to its contract title — the CLI titles a
`--file` source by FILENAME. Three properties, each written after the
corresponding failure was proven live:

- **The rename is polled, then RE-VERIFIED after a settle delay**
  (`RENAME_SETTLE_DELAY_S`, 45s). A read-back proves a moment: on 2026-08-28 two
  applies each passed the poll on attempt 1 and the title later regressed to the
  temp filename when ingestion of the 279KB body completed. One re-rename is
  attempted; a regression that survives it raises.
- **A stray is ADOPTED, never duplicated.** A temp-titled `xf-sync-*.md` source
  matching the document on the manifest's digest is renamed into place. When
  that strict digest cannot match — the provider returned 281,645 bytes for a
  279,235-byte document — a bounded fallback considers only strays within
  `ADOPTION_LENGTH_TOLERANCE_BYTES` (4,096) of the projected body and adopts the
  one whose provider-normalized digest matches (JSON unwrap, NFC, line endings,
  per-line trailing whitespace, trailing newlines). Length never adopts on its
  own and a title pattern never adopts at all.
- **When the fallback cannot decide, the run STOPS instead of uploading.** A
  within-tolerance stray that does not match, or more than one match, is exactly
  the state in which adding again compounds (two applies took Canon from three
  strays to four, silently, exit 0). The book fails with every candidate named
  and the run exits nonzero; the other books still complete.

**Hand repair when the run stops** (the recipe that worked live, and the one the
error message prints): rename ONE fully-ingested stray to the contract title,
wait, verify the title is STILL present, then re-plan — it should converge to
zero operations. Delete the remaining duplicates once you have confirmed what
they are. Do NOT re-run `--apply` to repair a stray.

```bash
nlm source list xf-canon | grep xf-sync-          # what stray copies exist
nlm source rename <stray-id> "[spec] openxFactory: ideation-dashboard" \
    --notebook xf-canon
sleep 60 && nlm source list xf-canon | grep "ideation-dashboard"   # still there?
python3 openxFactory/scripts/sync-notebooklm-books.py .            # expect zero ops
```

The oversized path prints a sub-line per operation even when it succeeds
(`uploaded as <id>`, `renamed on attempt N`, `settle re-verify: title held`,
`adopted stray <id> by strict|normalized digest`), so a stray-minting run is
distinguishable from a clean one in the transcript.

**Capacity guard** (split-ideation-book-per-repo): the platform per-notebook
source cap is a named constant in the sync (`NOTEBOOK_SOURCE_CAP = 300`;
plan-dependent — change it only with the plan). Projected occupancy counts
the desired managed set + the charter + every unmanaged source the
reconciliation preserves. At ≤ 30 sources of headroom the sync warns and
names the owed remedy (an OpenSpec delta defining that book's split); over
the cap it projects the deterministic in-cap prefix, reports the exact
excess, completes every other book, and exits nonzero. Unresolvable books
and refused creations are contained the same way — one bad book never kills
the run.

## 6. Operator Runbook

```bash
# 0. Bind the shell to the install's DECLARED account. Profile selection is
#    PROCESS-GLOBAL (auth.default_profile): of the verbs this sync issues,
#    none takes a per-invocation --profile, so the sync VERIFIES the active
#    profile and refuses when it is not the declared one.
nlm config get auth.default_profile     # what the CLI would use right now
nlm login switch <declared-profile>     # bind this host to the declared one

# 1. Authenticate (host shell with a browser; ~20 min session lifetime).
#    Credentials land in ~/.notebooklm-mcp-cli/, shared with containers
#    that mount the same home. WSL without a Linux browser: nlm login --wsl.
#    First time for a profile, name it and sign in AS the declared account:
#      nlm login --profile <declared-profile>
nlm login

# 2. Preview, then apply, from the workspace root.
python3 openxFactory/scripts/sync-notebooklm-books.py . 
python3 openxFactory/scripts/sync-notebooklm-books.py . --apply

# 2b. Prove the live books against THE CORPUS SCAN (never against another
#     account's books): per-book title-set equality + a union reconciliation.
python3 openxFactory/scripts/sync-notebooklm-books.py . --parity

# 3. Books are aliased: xf-ideation-<repo-slug> (per-repo ideation family),
#    xf-drafts, xf-canon (all tagged: xfactory,lifecycle). Aliases are
#    machine-local convenience; resolution is by notebook title.
nlm source list xf-canon
nlm source list xf-ideation-opsxfactory
nlm notebook query xf-canon "What owns gate structure?"
nlm cross query "Where do drafts contradict canon?" --tags "xfactory"

# 4. Artifacts (async on Google's side).
nlm mindmap create xf-ideation-openxfactory --confirm
nlm report create xf-canon --format "Briefing Doc" --confirm
nlm studio status xf-canon
```

Cadence: manual after meaningful doc changes for now; intended to run from
the nightly doc-health action once that pipeline is implemented (see the
archived `add-doc-health-contract` OpenSpec record).

## 7. Temporary Hybrid Analysis Notebooks

Temporary hybrid notebooks support focused idea analysis against governed
Canon. A hybrid is not one of the lifecycle books. It is a derived analysis
workspace containing exactly one Canon release line and exactly one origin
idea target:

```text
Canon release line + ideation/brainstorm/<topic>/
Canon release line + ideation/staging/<topic>/
Canon release line + openspec/changes/<change-id>/supporting-docs/
```

The hybrid's charter source is titled `00 [hybrid charter] Read me first` and
names the Canon release line, the origin folder, and the rule that every
hybrid output is `L1 notebook synthesis`. Hybrid output can raise claims and
suggest deltas, but it cannot decide policy, memory, release scope, OpenSpec
approval, or customer-facing output.

When a staged topic crosses the proposal gate, its hybrid origin moves with it
to the active change's `supporting-docs/` folder. The Canon release line remains
unchanged. The archived lifecycle-notebook-hybrid-imports change retains the
source operating process and its support bundle.

## 8. Hybrid Source Return Imports

NotebookLM material returns to the repository by source membership. Scratch
notes stay inside NotebookLM. A note becomes importable only after a human
converts it to a NotebookLM source. Web, research, file, Drive, and other added
NotebookLM sources are importable as soon as they appear in the hybrid source
set.

The operator supplies the origin folder explicitly:

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py . \
  --import-new-sources "<hybrid-notebook-id-or-alias>" \
  --target-path "openxFactory/ideation/brainstorm/<topic>"

python3 openxFactory/scripts/sync-notebooklm-books.py . \
  --import-new-sources "<hybrid-notebook-id-or-alias>" \
  --target-path "openxFactory/ideation/staging/<topic>" \
  --apply

python3 openxFactory/scripts/sync-notebooklm-books.py . \
  --import-new-sources "<hybrid-notebook-id-or-alias>" \
  --target-path "openxFactory/openspec/changes/<change-id>/supporting-docs" \
  --apply
```

Import mode is dry-run by default. With `--apply`, imported material is written
to `notebooklm-ideas-YYYY-MM-DD.md` under the supplied origin folder. The file
carries `Status: brainstorm`, `Status: staged`, or `Status: draft` according
to its origin, `Kind: reference`,
`Authority: L1 notebook synthesis`, the source workspace, the NotebookLM
source id, and the NotebookLM source title. Re-running the importer skips
source ids that are already present in lifecycle files.

Before a proposal archives, run one final source-return import. Package only
after the import completes, then retire the temporary hybrid from active use.

Seed sources are context, not new material. Importers skip `00 [charter]`,
`00 [hybrid charter]`, and titles beginning `[brainstorm]`, `[staged]`,
`[draft]`, `[ratified]`, `[standard]`, `[spec]`, or `[grounding]`.

## 9. Branch-Session Notebooks

Ratified by `add-workbench-branch-sessions` (2026-07-26; decisions D11, D16).

A branch session — the workbench's working state on a git branch materialized
as a worktree — MAY carry exactly ONE session notebook, and it is the only
notebook surface allowed to read a worktree. It is not one of the lifecycle
books and never becomes one: the books stay main-only (section 1), a session
notebook MUST NEVER contribute a source, a title, or a repository name to a
book, and its existence relaxes the worktree exclusion for no book. Session
material reaches a book only after the session's pull request merges, by the
ordinary sync.

The notebook's life is the session's life. It is created when the session
opens, re-synced from the worktree on demand, and RETIRED when the session
ends by either route — merge or abandon — torn down together with the worktree
and the session's snapshot-registry entry. It is never re-pointed at `main`
(D16): after a merge there is no source left to project (the merge deletes the
branch and the teardown removes the worktree), and a re-pointed notebook would
be neither a lifecycle book nor a section 7 hybrid. If a session's ANALYSIS
must outlive its branch, the route is an explicit conversion to a section 7
hybrid under that section's charter and seeding rules — a future change, not a
silent re-point. A notebook is optional throughout: when the NotebookLM quota
is exhausted the session opens anyway, without one, and the human is told
whose limit was hit (the quota belongs to the install's ONE DECLARED HOSTING
ACCOUNT — section 1 — consumed by the lifecycle books, every live `xf-wb-*`
reference set, and every live `xf-session-*`, so it scales with concurrent
tiles across everyone sharing that account). The account being declared does
not make the ceiling bigger; it makes the ceiling's OWNER nameable, and
per-install accounts shard it the way per-repo books shard the per-notebook
source cap.

Aliases are `xf-session-<repository>-<transformed-branch>`, derived from the
(repository, branch) pair — the repository segment is required for
injectivity, since two repositories can carry the same topic or cluster id.
The transform strips a leading `draft/`, maps every remaining `/` to `-`, and
lowercases, so `(openxFactory, draft/workbench-branch-sessions)` becomes
`xf-session-openxfactory-workbench-branch-sessions`. The `xf-session-`
namespace is deliberately DISJOINT from the swept `xf-wb-*` reference-set
namespace: the book-sync mode also runs the ideation-dashboard workbench orphan
sweep, which deletes every `xf-wb-*` notebook no live workbench manifest binds,
and a session leaves NO manifest — so a session notebook titled `xf-wb-*` would
be an orphan from birth and the next routine `--apply` would delete it
mid-session. Renaming keeps the two lifecycles independent without re-cutting
the sweep's contract.

Sourced from the worktree, not the served checkout:

```bash
# Preview, then apply, from the workspace root. --session-repository is the
# tie-break when the same branch is live in more than one repository.
python3 openxFactory/scripts/sync-notebooklm-books.py . \
  --session-ref draft/workbench-branch-sessions

python3 openxFactory/scripts/sync-notebooklm-books.py . \
  --session-ref draft/workbench-branch-sessions --apply

# Retire at session end (both endings; the workbench's session teardown
# performs this — the flag is the manual equivalent).
python3 openxFactory/scripts/sync-notebooklm-books.py . \
  --session-ref draft/workbench-branch-sessions --session-retire --apply
```

The mode refuses rather than guesses: no live worktree for the branch, or a
branch live in more than one repository with no `--session-repository`, is an
error with the reason stated. Its verbs are SYNC / RETIRE / KEEP / SKIPPED,
deliberately not the books' ADD / DEL / UPD, so doc-health's
notebook-projection-drift family never counts a session operation as pending
lifecycle-book projection work.

**Branch-landing imports.** Section 8's source-return path applies unchanged,
with one difference: for a session notebook the imported file is written into
the origin folder INSIDE THE SESSION WORKTREE and lands on the session branch
as ordinary working material, committed with the session's gate action —
never into the served checkout. The imported file's header contract is
verbatim section 8's (origin lifecycle status, `Kind: reference`, source
workspace, `Authority: L1 notebook synthesis`, NotebookLM source id and
title), idempotency is still by source id, and the seed-source skip list is
unchanged. Session-notebook output carries `L1 notebook synthesis` authority
exactly as a hybrid's does: it may raise claims but decides no policy, memory,
release scope, OpenSpec approval, or customer-facing output.

## 10. Workspace Records

The lifecycle books are registered as `external_source_workspace` records in
[examples/lifecycle-notebook-workspaces.yaml](../examples/lifecycle-notebook-workspaces.yaml),
per the source-workspaces record model. A branch-session notebook is NOT
registered: it is derived state bound to a branch that outlives nothing, and
`add-workbench-branch-sessions` D10 adds no session descriptor of any kind.

## 11. Known Limitations

- NotebookLM source-count limits apply per notebook. The cap is now a named
  constant with a preflight guard (section 5): a book running low WARNS and
  names the owed split delta; a book over cap reports its exact excess and
  the run exits nonzero. The shared Ideation book hit the cap 2026-08-10 and
  was split per-repo; Working Drafts and Canon remain single books, watched
  by the same guard.
- Grounding fan-out: the three grounding docs seed EVERY book, so an edit to
  one re-projects (delete + re-add, ~2s each) into each of the 3+N books —
  batch grounding edits rather than trickling them.
- nlm sessions expire in ~20 minutes; CI use needs an auth strategy before
  the nightly integration. The current host auth blocker, the WSLg Playwright
  workaround (`scripts/nlm_auth.py`), and the machine-account direction that
  retires it are tracked as an open operational item:
  [NotebookLM Projection Sync — Open Operational Item](notebooklm-sync-open-item.md).
- Matching is title-based; retitling rules (section 2) therefore cause a
  delete + re-add cycle on the affected sources.
- Notebook synthesis can be stale between syncs; the repo is always the
  system of record.

## 12. Declared Hosting Identity, And Sharing Out From It

Ratified by `add-notebook-projection-identity` (2026-08-23), which exists
because the whole governed projection was created under one person's personal
consumer Gmail — the CLI's default profile, chosen by whoever ran `nlm login`
first — until a colleague's access request landed in that private inbox and
sat there.

### The declaration

**THERE ARE TWO INSTANCES OF THIS RECORD AND ONLY ONE OF THEM IS COMMITTED
HERE** (`adopt-configured-notebook-hosting-identity`, ratified 2026-09-08).
`examples/notebook-projection-hosting.yaml` is a SYNTHETIC EXAMPLE — every
identity in it is fictional, in `example.invalid`, every actor is a role
placeholder, and the record says so in a field both readers parse
(`hosting.instance: example`). An install's own LIVE declaration lives wherever
that install's configuration says, outside this repository.

**Why two files rather than one redacted file.** A hosting record is not prose
about an account. Its `account`, its `migration.from_account` and its roster
rows are the values `enforce_hosting_profile()` compares against the address the
`nlm` CLI profile is ACTUALLY signed in as, refusing the run when they differ.
Replacing a live address with a placeholder would not redact the record — it
would disarm the guard. And the roster is worse than configuration: it is the
record of governed share acts, so a placeholder there would falsify a record
rather than anonymise one.

**Where the live record is: resolved, in one order, by both readers.**

```text
1. $XFACTORY_NOTEBOOK_HOSTING_DECLARATION        absolute, or workspace-relative
2. <workspace>/.xfactory/notebook-hosting.yaml   declaration_path: <path>
3. nothing                                       UNDECLARED
```

The configuration file is per-machine, uncommitted and gitignored: it carries a
PATH and no credential. Three properties are deliberate:

* **The committed example is not step 3.** Defaulting to it would make every
  fresh clone declare an install it is not — the sync would bind to a profile
  named in a fixture, or refuse for the wrong reason.
* **Absent configuration is UNDECLARED**, the transition state the requirement
  already defines: reported as unmet, and non-breaking. A checkout whose private
  declaration is simply not on disk reads the same way, which is correct.
* **A configured path that resolves to a record marked as an example is
  REFUSED**, not bound. The refusal is decided by the marker inside the record
  rather than by comparing paths, because symlinks, worktrees and copies make a
  path comparison unreliable.

**How a live declaration is checked, now that CI cannot reach it.** While the
live record and the committed file were the same file, one test
(`test_the_committed_record_conforms`) was the live declaration's only automatic
conformance check. The split costs that, and three things replace it:

* `test_the_committed_example_conforms` keeps the record's SHAPE gated in CI;
* `test_a_resolved_declaration_is_validated` proves the resolved path is
  validated at all, over a synthetic declaration in a temporary tree;
* and **an operator command, before any sync `--apply`**:

```bash
python3 scripts/validate-notebook-projection-hosting.py --resolved
```

`--resolved` deliberately refuses to fall back to the committed example and
refuses a record marked as one, so a green line from it is evidence about the
live record and nothing else.

`scripts/validate-notebook-projection-hosting.py` enforces the shape either
way: the two-case vocabulary, the Workspace-user rule, the refusal of any
service account, the profile the sync binds through, and the roster's key. Not
one of those checks asks WHICH real account is named — every one is a property
of the record's shape or an equality between two of its own fields, which is why
the synthetic instance proves as much as the live one did.

The record deliberately does NOT live under `contracts/`. It is the operator's
own governance artifact for one install's tooling account — nothing else
consumes it and nothing pins it — and its sibling
`lifecycle-notebook-workspaces.yaml` sits here for the same reason.

### The approval lane: who decides a share request, and how it is recorded

Ratified by `add-notebook-projection-identity`; the actor named by Brett Heap on
2026-08-27, closing task 2.4.

**WHO. An install's designated company-policy actor is named in its own live
declaration**, as `approval.designated_actor` — a standing statement of who MAY
decide, distinct from a roster entry's `granted_by`, which records who DID. The
requirement this discharges is precise about why the designation must exist at
all: a request "SHALL NOT be left to whoever happens to read the account's
mail." In the committed example that actor is a ROLE PLACEHOLDER, ruled so on
2026-09-08 (OQ-D): a real person's name in a synthetic record asserts a grant
that instance did not make, and the validator ties `granted_by` to
`designated_actor` by equality, so the two move together.

**WHERE. In the hosting account's own interface**, signed in as the declared
account. NotebookLM exposes no administrative or sharing API
for inbound requests, so there is nothing else to act in. `nlm share invite`
performs the grant once the decision is made, and it is the same governed act
from a terminal rather than a second lane:

```bash
nlm share invite xf-canon <email> --role viewer --profile company
nlm share status  xf-canon --json --profile company    # reconcile the roster
```

**HOW A DECISION BECOMES THE RECORD.** Approving and denying land in the same
lane, and neither is an audit trail beside a list:

* **Approving WRITES the roster** — the install's own live one, not the
  committed example, whose rows are synthetic and record nothing. The share-out
  entry IS the record of the granted act — `hosting_account`, `user`, `book_or_alias`, `role`,
  `granted_at`, `granted_by`. There is no separate approval log, because a log
  beside a roster is two records of one decision that can disagree.
* **Uniqueness is the scope-and-principal triple** `(hosting_account, user,
  book_or_alias)`. Role, grant time and granting actor are ATTRIBUTES of that
  entry, not parts of its key — so a re-approval, a role change, or a grant by a
  different actor UPDATES the one live entry. A roster that is the record of
  current access cannot simultaneously assert a stale grant and a current one
  for the same person on the same book. Superseded decisions are retained as
  that entry's history.
* **Denying is recorded too**, in `denied`. A refused request is a governed act
  and is not left to expire unrecorded — which is the whole failure this lane
  was raised against.

**What is NOT designed against.** No obligation here depends on an API the
platform does not expose. Detection and relay of pending requests MAY be
automated if NotebookLM ever offers a surface for it; **the approval remains a
governed human act either way**, and `approval.automated_approval: false` says
so in the record rather than leaving it to be inferred.

### Roster test plan — add, list, and remove a collaborator

Written 2026-08-27 at Brett's ask, so the roster can be exercised rather than
only asserted. Run as the designated actor with the company profile active.

**ADD** (this is the grant; it is the governed act, not a rehearsal of one):

```bash
nlm share invite <alias> <email> --role editor --profile company   # or --role viewer
```

**LIST** — the verification half, and the only way to prove a grant landed:

```bash
nlm share status <alias> --json --profile company
```

**REMOVE — THE CLI CANNOT DO IT.** `nlm share` offers exactly `status`,
`public`, `private`, `invite` and `batch`. There is **no remove, revoke or
uninvite verb**, and `nlm delete` deletes a NOTEBOOK, not a collaborator.
Removal is therefore a **UI act**: open the book in the hosting account at
notebook.google.com, use its Share dialog, and remove the collaborator there.
Recorded plainly because a test plan that assumes a symmetric API would fail at
exactly the moment someone needed to undo a grant.

**AND THE ROSTER RECONCILES IN THE SAME STEP.** A removal at the provider is only
half the act: the `share_out` entry that recorded the grant must be updated in
the same sitting — annotated `revoked`, with the date and who revoked it, and the
superseded grant retained as that entry's history per the uniqueness rule.

This is not bookkeeping etiquette. **The share-out entry IS the record of
access** — that is the ratified design, chosen so there is no audit log beside the
roster that can drift from it. Remove at the provider and leave the entry
standing and the record asserts access the provider no longer grants, which is
precisely the record/reality split this lane exists to prevent. The same rule
runs the other way: re-adding restores the entry rather than writing a second
one, because uniqueness is keyed on `(hosting_account, user, book_or_alias)`.

**Every provider act pairs with a roster act. Neither half is the deliverable
alone**, and `nlm share status --json --profile company` is what proves the two
agree.

Note also that the CLI's exit code is not trustworthy on this path: an invite
that printed `API error (code 7)` still returned `rc=0` on 2026-08-27. **Verify
with `share status`, never with `$?`.**

#### Named future tests

1. **The remove-and-re-add cycle — six steps, not four.** Remove both accounts
   from one book through the UI; confirm with
   `nlm share status <alias> --json --profile company` that they are gone;
   **annotate the two `share_out` entries as revoked, dated, by whom**; re-add
   with `invite`; confirm again; **restore the entries**. The roster half is
   named explicitly at both ends because it is the half a tester skips — the
   provider gives immediate feedback and the YAML does not, so the record is
   where drift hides. The test passes only when the provider listing and
   `share_out` say the same thing at every stop, including the middle one where
   access is genuinely absent.
2. **Tenant-wide sharing.** Whether a whole domain can be granted at once is
   **unestablished**: `nlm share invite` takes a single email and offers no
   domain or group argument, and `batch` invites multiple named collaborators
   rather than a domain. Any tenant-wide grant would therefore be a provider-UI
   or Workspace-admin capability, not a CLI one — and it would sit against the
   2026-08-24 ruling that the posture is RESTRICT with the app as sole grantor,
   so it is a question to rule on rather than a feature to reach for.

### The legacy books: WIND-DOWN BY OWNER DELETION

Ruled 2026-08-27. The question left open at the retirement — whether the legacy
owner's continued access to the renamed books is an accepted fact or gets wound
down — is answered: **wound down, by deletion, performed by the owner himself in
his own Gmail account, on his own timing.** No agent deletes anything.

**THE CONSEQUENCE, STATED BEFORE IT HAPPENS.** Step 8 retired those books by
RENAME precisely so nothing was lost. Once they are deleted, that safety net is
gone: the pre-rename titles and the legacy content survive **only** in
`docs/notebook-projection-migration-evidence-2026-08-24.md` and in the live
company books. The evidence document stops being a record of what happened and
becomes the **only** account of what those books were called — which is why its
phase-1 listing was preserved verbatim.

### Where the account's credential lives

Ratified by `add-notebook-hosting-credential-custody` (2026-08-23). Moving off a
personal identity only half-solves the problem it was raised for: an account
nobody but its creator can sign into is still a single point of failure, just a
better-named one. So the hosting record declares WHERE the credential is held.

It declares it **by reference and nothing more**. The `custody:` block names the
binding — `binding_kind`, `binding_client`, `binding_id` — and carries no
provider, no vault, no `secret_ref`, and no value. That is deliberate to the
point of being the whole design: the reference is sufficient to find the
credential through the governed path and **insufficient to obtain it without
one**. `secret_ref` is refused by the validator even though it is not itself
secret, because it is binding detail, and carrying one field of the binding here
invites the rest to follow.

The binding instance — provider, vault, secret reference, owner, rotation
policy — lives in the **consuming install**, not in this repository. That split
is the residency redirect accepted at ratification: neutral obligations here,
concrete estate facts there. Naming a real vault in a per-client binding is
exactly what a binding is for and breaches no rule; naming one in a contract
artifact would.

**Each consuming system reaches the account through its OWN binding.** One
identity may be shared; one authority may not. The xFactory sync lane and
openXdox each hold their own access identity against the store, their own grant,
their own rotation visibility, and their own audit trail — so revoking one does
not disturb the other, and the store's log can say which system read the secret.

What revocation reaches, stated honestly because a shared bearer secret bounds
it: revoking a binding stops that system's FUTURE fetches and nothing else. It
cannot un-disclose a password already fetched, nor end a session already
established with it. Evicting a consumer that has already read the secret means
ROTATING it — and rotation necessarily reaches every consumer of that identity.
That is the one act per-system bindings cannot make independent, and it is
recorded here rather than left for someone to discover during an incident.

#### Custody is not automation

The most useful sentence in this section. Holding the password and the TOTP seed
governs **who may obtain them** and proves who did. It does not make the sign-in
unattended: Google's sign-in for this account is an interactive browser flow, and
it stays one. An operator with full vault access still completes that step by
hand.

The hosting record says so in its own `interactive_step_remains` /
`interactive_step` fields rather than leaving it to this document, and the
validator refuses silence on the question — because silence reads as "yes" to
someone planning automation, and a custody reference that implies access the
install does not have is worse than none.

#### The `nlm` session is NOT a custody subject

The profile under `~/.notebooklm-mcp-cli/` is **refreshable session state**, and
`credential-contracts` refuses to distribute that class: an ephemeral copy's
refresh silently stales the master, so two systems sharing one live session is a
defect with the copy left implicit. The session is re-established by signing in.
It is never fetched from a vault, never shared between systems, and never
recorded here — the validator refuses `session`, `cookie` and `profile` fields
outright, in both hosting cases.

That refusal holds for `self_hosted` too. The self-hosted exemption is from
DECLARING custody — no operator exists to bear the obligation — never from
keeping credential material out of the repository.

### How a run is bound to the declared account

Profile selection in the `nlm` CLI is **process-global**, through
`auth.default_profile`. Of the verbs this sync issues — `notebook`, `source`,
`alias`, `tag`, `chat` — **none accepts a per-invocation `--profile`**; only
the newer `share` and `login` verbs do. So the sync **verifies** the binding
rather than passing it, and refuses to run when the active profile is not the
declared one, printing the exact `nlm login switch` remediation. It never
switches the profile itself: that is shared user state, and other sessions on
the same host race on it.

Both the profile NAME and, when the CLI recorded one, the ACCOUNT ADDRESS are
verified. `profiles/<name>/metadata.json` carries an `email`, populated by a
recent login and left null by an older one; where it is present and disagrees
with the declared account the run refuses, and where it is null the run says so
and falls back to verifying the name alone. (An earlier draft of this section
claimed the CLI stored no email at all. Review disproved it: `farheap` carries
`<convener-workspace-identity>`, `personal` carries null.)

The binding is re-asserted **before every invocation**, not once at the start.
Because selection is process-global, another terminal running
`nlm login switch` part-way through a forty-minute re-derivation would
otherwise redirect every later add and delete into a different account. The
sync reads `~/.notebooklm-mcp-cli/config.toml` directly for this — a stat, not
a subprocess, cached on the file's own stamp — and refuses the next invocation
the moment the value moves, naming the re-bind command. The sync is idempotent,
so a resumed run is a no-op over whatever finished.

One limit remains and is stated rather than papered over: between the
assertion and the `subprocess.run` that follows it there is a microsecond
window in which the profile could still change. It cannot be closed without a
per-invocation profile flag the CLI does not offer for these verbs. What the
check removes is the realistic failure — a switch that happens minutes into a
forty-minute run and silently redirects everything after it.

The declaration's load-bearing rules are enforced on this path too — the
two-case vocabulary, the Workspace-user requirement for the operator-hosted
case, the service-account refusal, and the account-in-declared-domain check —
because a validator nothing runs is not a refusal.

While a declared migration is `pending`, the run binds to the account that
still HOLDS the books and says so. A declaration is not a migration — flipping
the binding before the books move would break every sync rather than move
anything.

### Sharing out, and the roster that records it

Individual users never authenticate against the hosting account's own
credentials. They are shared out TO, from that account, and every share act is
a governed decision that is recorded. The DECISION is a human one either way;
where it is executed — the account's own sharing UI, or `nlm share invite` from
a terminal under the declared profile — is the actor's choice, and the runbook
shows both. What is not optional is the record — the roster entry IS the record, not an
audit trail beside one. Uniqueness is the stable
`(hosting_account, user, book_or_alias)` triple; the role, the grant time and
the granting actor are attributes, so a re-approval or a role change updates
the one live entry instead of asserting a stale grant beside a current one.

**A platform correction worth recording.** The proposal reasoned that
NotebookLM "exposes no share or admin API". That is true of the half it was
about — there is still **no pending-request queue and no approval surface**, so
the approval remains a human act in the account's own UI — but it is NOT true
of sharing generally: the CLI does expose outbound share management, and these
verbs DO take `--profile`:

```bash
nlm share status <notebook> --json --profile <declared-profile>   # collaborators
nlm share invite <notebook> <email> --role viewer --profile <declared-profile>
nlm share batch  ...                                              # many at once
```

That makes two things practical which the ratified text treats as manual: a
recorded grant can be APPLIED by tooling, and the roster can be RECONCILED
against `nlm share status` to prove it matches reality. Neither changes who
decides. This correction is recorded here rather than folded into the ratified
requirement text, which permits automation of detection and relay while keeping
the approval a governed human act either way.

### The alias store is shared, and that shapes the migration

`~/.notebooklm-mcp-cli/aliases.json` is ONE FLAT FILE, not per-profile, and the
sync registers an alias whenever it resolves a book — on the found path as well
as the created one. Two consequences, both load-bearing:

- A read-only run must not touch it. `--parity` therefore resolves books with
  alias binding switched OFF, and its test asserts that no `alias set` or
  `alias delete` is issued. An alias write during a parity proof would repoint
  `xf-canon` for every account on the host.
- A migration must DELETE the legacy aliases BEFORE the first `--apply` in the
  new account, not after. Running the re-derivation first repoints them, and
  the ratified "deleted rather than repointed" rule can no longer be honoured —
  nor the legacy notebook ids recovered from the store. The runbook's step 1
  exists for exactly this, and it is the 2026-08-10 precedent's order.

### Migrating to a declared account

See [the migration runbook](notebook-projection-migration-runbook.md). The
short form: re-derive under the declared account, prove parity against the
CORPUS SCAN with `--parity`, then retire the legacy books by recorded act — and
do NOT retire the workspace record the replacement made current.
