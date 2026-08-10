# Lifecycle Notebook Projection

Status: standard
Kind: process
Backed by: [openspec/specs/lifecycle-notebook-projection/spec.md](../openspec/specs/lifecycle-notebook-projection/spec.md) (promoted from the archived add-lifecycle-notebook-projection change)
Extended by: add-workbench-branch-sessions (ratified 2026-07-26) — section 9,
branch-session notebooks, plus the main-only rule made explicit in section 1
Amended by: split-ideation-book-per-repo (ratified 2026-08-10) — per-repo
Ideation books, title-based resolution, the capacity guard, and the legacy
shared Ideation book's retirement, after the 300-source cap incident
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
hand-curated. Ideation is ONE BOOK PER GOVERNED REPOSITORY
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
project into the books. The three books are **MAIN-ONLY without exception**: a
lifecycle book IS the lifecycle projection, so a book carrying unmerged
sources is not a stale book but a WRONG one, asserting lifecycle states that
do not exist. Section 9 is the only surface permitted to read a worktree, and
it is not a book.

## 2. Source Titles

Titles are the authority signal chat sees on every citation:

```text
[<status>] <repo>: <file stem>          e.g. [draft] MedxFactory: care-organization-hermes
[spec] openxFactory: <capability>        promoted capability specs
[grounding] openxFactory: <stem>         grounding set (section 3)
00 [charter] Read me first               workspace charter (section 4)
```

Title rule for ambiguous stems: when the file stem is `README` (or otherwise
non-unique within a repo), the title uses `<parent-dir>/<stem>` — e.g.
`[ratified] AdxFactory: ideation/README`.

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
# 1. Authenticate (host shell with a browser; ~20 min session lifetime).
#    Credentials land in ~/.notebooklm-mcp-cli/, shared with containers
#    that mount the same home. WSL without a Linux browser: nlm login --wsl.
nlm login

# 2. Preview, then apply, from the workspace root.
python3 openxFactory/scripts/sync-notebooklm-books.py . 
python3 openxFactory/scripts/sync-notebooklm-books.py . --apply

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
Canon. A hybrid is not one of the three lifecycle books. It is a derived
analysis workspace containing exactly one Canon release line and exactly one
origin idea target:

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
notebook surface allowed to read a worktree. It is not one of the three books
and never becomes one: the books stay main-only (section 1), a session
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
whose limit was hit (the quota is one shared account, consumed by the three
books, every live `xf-wb-*` reference set, and every live `xf-session-*`, so
it scales with concurrent tiles across everyone).

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

The three books are registered as `external_source_workspace` records in
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
  the nightly integration.
- Matching is title-based; retitling rules (section 2) therefore cause a
  delete + re-add cycle on the affected sources.
- Notebook synthesis can be stale between syncs; the repo is always the
  system of record.
