# Ideation Dashboard — Branch-Session Runbook

Status: draft
Kind: process
Repository context: openxFactory
Purpose: operate the ideation dashboard's branch sessions — the verbs, their CLI parity, where the derived artifacts live, and the rules that must not be broken while testing

Realizes the operating half of openxFactory `add-workbench-branch-sessions`
(engineering surface: codexFactory `specs/007-workbench-branch-sessions/`). The
dashboard surface itself is summarized in codexFactory's `docs/check-matrix.md`
§8; this document is what you run.

## 0. The openDox header, item by item

The header (post `add-opendox-project-header`, Brett's D12–D16 rulings) is
project-first. Left to right:

```text
Opensoft openDox   [ <project> ▾ ]   ⧩ <project>   [search…]   repo @ ref · sha · date   ◆hint   ↻   ◐ ⚙
realization funnel · the wheel · pipeline board · cluster canvas · lens · doc list · lineage
Documents · Topic clusters · Possibles · Staged topics · Active proposals · Archived changes
```

Three lines, in that order (Brett, 2026-08-08): the PROJECT line, then the
VIEW line, then the STAGE tiles. The tiles carry the same six stages in the
same order as the wheel's columns and the funnel's lanes, so they read as
the header of whichever view is below them rather than as a separate
summary.

- **Opensoft openDox** — the brand. Static.
- **The project dropdown** — the CURRENT project; you are always in one
  (last-used, else the first register project). Its first line, **New
  Project…**, opens the create form: name it, tick member repos, and
  `commission` records a `create-project` register edit — the register
  changes only when a terminal session fulfils it, and until then the
  project shows as a non-selectable "(commissioned — pending fulfilment)"
  entry. Gate off, New Project is disabled.
- **The repo filter (⧩)** — the current project's repositories, one popover.
  Its label states the VISIBLE count (`⧩ 3 of 5 Repos`), so the header says
  what the wheels span without opening anything:
  - **＋ add repository…** (first line, gate only): pick a known repository
    and commission its addition to the project (`edit-project`).
  - **The view row** (D19/D20) — `∪ union` / `∩ shared` toggles what the
    visible set MEANS: union renders everything the ticked repositories
    have; **shared** renders only what TWO OR MORE of them carry (matched
    on the item's identity — for documents the repo-relative path, for
    clusters the `cl-…` topic). The threshold is two rather than all,
    because convergence between any pair is the finding: across the
    five-factory `domains` project, all-of-them keeps 2 documents while
    two-or-more surfaces the topics the factories actually share. Shared
    filters rather than merges, so each repository's copy stays its own
    openable, badged row — which is how you read two factories' takes on
    one document side by side. `all` and `none` are the bulk moves. The
    toggle is inert with one repository visible (the modes agree), and
    where no member publishes a snapshot the row degrades to naming the
    merged view unavailable.
  - **One row per member** — the 👁 eyeball TICKS that repository into or
    out of the view; clicking the NAME makes it the only visible one; the
    🗑 trash on the right (gate only) arms on first click and commissions
    the repository's REMOVAL from the project on the second. Membership
    edits badge as pending (netted across the queue) until fulfilled.
  - **One visible repository = the interactive single view**: its own
    snapshot, every verb available. **Two or more = the composed, READ-ONLY
    merged view** with per-tile "open in <repo>" jumps. **None** empties the
    view honestly. Switching projects lands on the merged view when the
    project has one. The set is remembered per project and resolved against
    current membership, so a repository that leaves simply drops out.
- **The lens tab, repository vocabulary** (D21) — on a multi-repo view the
  Lens tab offers a `keywords | repositories` switch. The repository lens
  draws one dot per DOCUMENT IDENTITY on rings by CARRIER COUNT (centre =
  every visible repository has it, ring 1 = only one does), sectored by the
  exact repository combination. It is the filter's union/shared toggle drawn
  out, and the rail's ticks are the same visible set — change it in either
  place. Activating the centre or a sector, from the bullseye or from the
  drill-in pane beside it, SCOPES the whole dashboard to those documents;
  a banner states what you are scoped to and clears it.
- **Indexes on the radar** (Brett, 2026-08-07) — the bullseye labels by index,
  never by name, in TWO ALPHABETS so a label is never ambiguous about what it
  names: **documents are numbers** (a dot carries its row number in the matrix
  below) and the **vocabulary is letters** — keywords, or repositories in the
  repository lens — so a sector reads "A ∧ G". Letters continue past Z exactly
  as a spreadsheet does (AA, AB, … ZZ, AAA). The rail and the matrix are the
  legend, both printing index and name, and every full name stays one hover
  away in the SVG title. Names were unreadable at corpus scale: an 18-keyword
  conjunction ran 464px inside a 520px box and half were clipped.
  Each vocabulary term also carries a HUE, shown on its rail letter and on
  its portion of the ring as a thin tinted arc — a combination sector shows
  one segment per term — so you can find A's area by colour instead of
  reading every label. Deliberately subtle: only the hue is chosen in code,
  and the weight and opacity stay in the stylesheet.
  A sector's label sits at ITS OWN RING, beside the dots it names — how far
  from the centre a label is tells you which ring it belongs to — and its
  divider spans only that band. Ring labels are the match count (`3 ✓`,
  `all 14 ✓`), each placed in the widest arc its own ring leaves empty, so a
  dot can never sit on one.
- **Dots never touch** (Brett, 2026-08-07) — a cell (one ring band × one
  sector) packs its documents across as many lanes as the band admits and as
  many per lane as the slice admits, shrinking the dot only when the area
  demands it, so there is always clear space between two dots. The lanes in
  use are CENTRED on the band's midline, so a cell sits in its ring rather
  than clinging to the line above it, and a lone dot lands on the midline.
  Where the slice has ROOM the dots grow instead — big enough to carry their
  number INSIDE them, spread across the slice rather than bunched at its
  centre line — and every one of them is numbered, because an inside number
  collides with nothing. Congested cells keep the small dots and the
  outside-label rules. Consecutive
  dots label in two lanes radially outward of their dot. NUMBERS FOLLOW THE
  LAYOUT: cell by cell (centre outward), then column by column, each column
  running from the outer lane inward — so the dots inboard of a numbered one
  are simply +1, +2, +3. The outer lane carries the numbers; in a CROWDED cell
  (one whose columns sit closer than a label needs) only every other column
  does, and the column between two labels starts where the labelled one
  ended, one column deeper. A roomy cell numbers every column. Every dot still names itself on hover, and the
  matrix — sorted by the same numbers — is the full legend. Sector numbers
  ride their own lane further out, clear of the dot labels.
- **The search box** — fans out to the active view's own search.
- **The freshness header** — `repo @ ref · short-sha · generated <date>`
  (or `<project> · N repos · composed <date>` on a merged view): which
  data you are looking at, against a stated revision.
- **◆ newer-data hint** — appears when the publication lane advertises a
  newer snapshot than the one loaded; clicking it refreshes. Never
  auto-reloads.
- **↻ regenerate / refresh** — the plane's one refresh affordance: local
  serves re-run the generator against the checkout; served planes re-fetch
  published data.
- **◐ / ⚙** — theme toggle and settings.

### The register-edit fulfilment lane (add-register-edit-lane)

Project commissions (create-project, edit-project) are fulfilled by the
LANE, two ways:

- **the apply button** — "⟳ apply N pending" appears in the header whenever
  recorded commissions await; one click makes the serve run the lane once
  (validate → write → deliver → commit register-only → push);
- **the job that watches** — run beside the serve:

  ```bash
  PYTHONPATH=scripts python3 -m ideation_dashboard.register_edit_lane \
      --repo-root . --watch --interval 30
  ```

Failures are fail-closed: a stale commission (project vanished, member
conflict) or a git failure leaves the descriptor `dispatched` with the
reason in the run report; nothing is half-applied silently.

### Serving the MULTI-REPOSITORY local plane (merged views need members)

A serve launched with `generate-and-open --repository <one repo>` carries
exactly one snapshot, so `⊞ all repositories in <project>` disables for
every project whose members are not that repository: a merged view is
composed from PUBLISHED member snapshots, and one repository publishes one.
To work across repositories locally — and to exercise merged views — publish
the whole register roster first, then serve the resulting index:

```bash
# 1. one snapshot per register repository + the index the selector reads.
#    An ABSOLUTE --out-dir keeps the shared aggregation checkout clean;
#    a repository whose checkout is missing or unscannable is SKIPPED
#    (see index-status.json), never a failure.
PYTHONPATH=scripts python3 -m ideation_dashboard.nightly_lane \
    --repo-root /path/to/xFactory --repositories registered \
    --out-dir /abs/scratch/local-plane

# 2. serve that index. --source-root is per entry and fail-closed: an entry
#    with no declared root serves no documents.
PYTHONPATH=scripts python3 -m ideation_dashboard.serve \
    --snapshot /abs/scratch/local-plane/openxFactory-snapshot.json \
    --checkout-root . --local-index /abs/scratch/local-plane/index.json \
    --repository openxFactory --actor "$(git config user.name)" --port 8765 \
    --project-register /path/to/xFactory/project-register.yaml \
    --source-root openxFactory=. \
    --source-root AdxFactory=/path/to/xFactory/xFactories/AdxFactory
    # …one --source-root per published repository
```

Every register project then derives its merged view (D11), and the
freshness header reads `<project> · N repos · composed <date>`.

Two things worth knowing:

- The lane renders each repository from its **aggregation submodule
  checkout**, which may trail that repository's `main`. When you want a
  repository rendered from a live worktree instead (typically the one you
  are working in), publish that one separately with
  `--repositories <id> --checkout /abs/path/to/worktree` into the same
  out-dir before writing the index, or accept the pinned rendering.
- `--checkout-root` stays the tree the GATE acts on. Gate verbs and the
  register-edit lane therefore keep writing into that one checkout no
  matter which repository is on screen; the composed view itself is
  read-only by contract, with per-tile "open in \<repo\>" jumps.

## 1. What a branch session IS

A branch session is **derived state, not an artifact**. There is no session
descriptor, no session manifest, and no session schema anywhere in the
repository. A session IS exactly these four things, and any of them can be read
back at any time:

```text
its BRANCH            draft/<topic-id> | <kind>/<id> [ -<ordinal> ]
its WORKTREE          <repo>-worktrees/sessions/<branch with / flattened to __>/
its REGISTRY ENTRY    the (repository, session-branch) row in the running
                      serve's snapshot registry — liveness IS this entry
its NOTEBOOK ALIAS    xf-session-<repository>-<topic>, derived from the tile
```

Its action history is the **commit series on the branch**: one commit per
recorded human gate action, each carrying that action's `gate-action-record`.
Nothing else is written to describe it, and a restart re-derives the live
sessions from the worktrees and their branches rather than reading a file.

Two consequences worth internalizing:

- **The served checkout never moves.** No session verb switches its branch,
  resets it, or stashes in it. The only path a session writes inside the served
  checkout is the declared gate-records prefix
  `ideation/dashboard/gate-records/`, where the main-resident `open-pr` and
  `abandon-session` records land so they outlive the branch they name.
- **A draft never appears in a shared surface.** The wheel, the funnel, and the
  pipeline board always render the snapshot fetched with the ACTIVE
  `(repository, ref)` key; on `main` a session's documents are simply not there.

## 2. Prerequisites for the live affordances

The session verbs are **human-only** and appear as live controls only when all
three conditions hold (the `/capabilities` probe reports them as
`actions.session`):

```text
loopback bind        the local serve (127.0.0.1), never a hosted plane
real checkout        the served checkout is a real corpus checkout — named
                     `--repo-root` on `cli.py generate-and-open` below, and
                     `--checkout-root` on `serve.py`'s own entrypoint, which is
                     the same value under a second spelling
resolved actor       --actor, or the checkout's `git config user.name`
```

Anything less and every affordance degrades to a **copyable CLI descriptor** —
the same action, transportable to where the authority lives. The hosted
dashboard exposes none of this: it advertises `session: false`, and a hosted
request naming a non-`main` ref is refused.

Start the local surface from the repository root. **Both flags are REQUIRED** —
`generate-and-open` has no default for either, and without them argparse exits 2:

```bash
python3 scripts/ideation_dashboard/cli.py generate-and-open \
  --repo-root /workspace/projects/xFactory/openxFactory \
  --repository openxFactory
```

- `--repo-root` — the SERVED CHECKOUT: the corpus tree the snapshot is generated
  from, the tree `/source/` reads, and the tree a session's worktree container is
  created beside. It never moves (§1).
- `--repository` — the canonical repository id of that snapshot, and **the SAME
  value every session verb's `--repository` must carry**: it is the repository
  half of the session key, so a verb that spells it differently addresses a
  different session (§3, `--repository`). It defaults to nothing here; on
  `serve.py` it defaults to the snapshot's own `repository` field.

It prints the corpus counts it projected, the snapshot it wrote, and the URL on
a line of its own — `documents=… clusters=… possibles=… staged_topics=…`, then
`http://127.0.0.1:<port>/index.html`. `--no-open` prints the URL without
launching a browser.

### 2a. A wrong `--repo-root` is REFUSED — it never serves an empty funnel

This is the failure a human actually hits, and it is the one the T092 pass hit in
its first minutes: the path was real somewhere else — a container path, typed on
the host. The value is checked BEFORE anything is generated or written, and a path
that cannot be a corpus checkout is refused on stderr with a non-zero exit, naming
the resolved absolute path and what was looked for:

```text
--repo-root is not a corpus checkout: the path does not exist
  checked      /the/path/as/it/actually/resolved
  looked for   a directory holding at least one of contracts/, docs/, examples/,
               ideation/, openspec/, templates/
```

Three consequences worth knowing before you start:

- **A refused run writes no snapshot at all.** The refusal happens ahead of the
  write, so nothing is left behind to be mistaken for a result. It used to write
  an empty snapshot and exit 0, and the dashboard then rendered its own
  empty-state copy over the typo.
- **Existing is not enough — it must be the corpus tree itself.** The aggregation
  root ABOVE the checkout holds none of those roots and is refused too, and the
  path must resolve in the namespace where this command runs.
- **A real checkout that projects ZERO documents warns and continues.** An empty
  corpus is legal, so the run succeeds and says on stderr that nothing was
  projected. The dashboard's empty funnel looks identical either way, so read that
  warning as "check `--repo-root`" unless the tree really is empty.

`serve.py`'s `--checkout-root` — the same value under its second spelling, above —
is checked the same way: a path that cannot be a checkout is refused before the
socket is bound, and an existing directory holding no corpus (the served image's
empty sentinel) serves with every checkout-bound affordance OFF and says which.

### 2b. Validation on launch has THREE outcomes, not two

The launch checks the snapshot it is about to serve against the pinned schema,
and the result is one of exactly three things. They are worth separating,
because two of them look alike on a red terminal and only one is your corpus's
fault.

| Outcome | What you see | Exit | Serves? |
| --- | --- | --- | --- |
| **VALIDATED** | `validation: … 0 error(s), 0 warning(s)` | 0 | yes |
| **NOT CONFORMANT** | `validation FAILED — the pinned validator REJECTED …`, then the findings | 1 | **no** |
| **VALIDATOR UNAVAILABLE** | `validation SKIPPED — this snapshot was NOT checked against the pinned schema` | 0 | **yes**, unchecked |

**NOT CONFORMANT** is the one that stops you, and it should: the validator ran,
reached a verdict, and the snapshot is genuinely wrong. The message says so in
those words and prints the errors, so you can act on them.

**VALIDATOR UNAVAILABLE** means the check could not be performed at all, which
is not the same as failing it — nothing at all is known about the snapshot. The
dashboard starts anyway, exit 0, because a governance view you cannot open helps
you less than one whose schema check was skipped. Two ways to get here:

- *Nothing to run.* Neither the OUTPUT directory (searched first) nor
  `--repo-root` (the fallback) has `openxFactory/scripts/validate-ideation-dashboard-contracts.py`
  above it; the message names both directories it walked up from. Render a
  checkout inside an aggregation checkout, or point `--run-dir` into one. This
  used to happen on EVERY ordinary launch — the search started only at the
  output file, `generate-and-open` defaults `--run-dir` to a temp directory, and
  no ancestor of `/tmp` holds an aggregation checkout — so the advertised schema
  check silently never ran (T092 defect 8).
- *Found it, could not run it.* Almost always the validator's python
  dependencies are missing from the interpreter that runs it — a SEPARATE
  process from whatever installed openxFactory, so the libraries must exist on
  the machine serving the dashboard. The warning quotes the validator's own
  complaint and gives the remedy:

  ```bash
  pip install 'jsonschema>=4.18' referencing
  ```

  Install those and the launch validates normally. (This is also what makes
  workbench set-saves work: a save re-validates its manifest and REFUSES the
  write when it cannot, because that one is a write into your tree.)

Add `--strict` and the third outcome becomes fatal too: a run that could not be
validated exits non-zero rather than serving unchecked. That is what the flag is
for — use it in a lane or a check, not when you just want the dashboard up.

Either way, do not read the SKIPPED line as routine: the snapshot really was not
checked.

## 3. The session verbs, and their CLI parity

Every session route has a `gate` subcommand, so the whole feature is usable with
no surface at all — and the gate-off workbench renders exactly these command
lines, filled in for the open tile.

| Session verb | Where it lives on the surface | Gate route |
| --- | --- | --- |
| `create-document` (opens or joins the session) | the workbench's `＋ new document` on any tab | `/actions/gate/create-document` |
| `edit-document` (rewrite inside the session) | the session bar's `✎ rewrite a document in this session` | `/actions/gate/edit-document` |
| `open-pr` (save: push + open/update the PR) | the session bar's `⇪ save — open the pull request` | `/actions/gate/open-pr` |
| `abandon-session` (end without saving) | the session bar's `⌧ abandon this session` | `/actions/gate/abandon-session` |
| `cleanup-abandoned-branch` (delete an abandoned branch) | CLI only | `/actions/gate/cleanup-abandoned-branch` |
| notebook re-sync | the session bar's descriptor, in BOTH gate postures | not a gate route at all |

### 3a. What a session may rewrite — the tile's OWN material

`edit-document` rewrites the tile's own material and nothing else:

- a STAGED-TOPIC tile's session may rewrite documents under
  `ideation/staging/<topic-id>/`, the folder the tile is named after;
- ANY tile's session may rewrite a document THAT SESSION CREATED (a path the
  session worktree has and the served checkout does not) — which is what a
  cluster or possible tile's session may rewrite, since neither owns a folder;
- everything else is READ-ONLY CONTEXT and is refused, on both surfaces, with
  nothing written: another topic's staged document, an `ideation/brainstorm/`
  capture, a cluster-neighbourhood or inherited row, and an inbound document
  that merely declares this topic as a destination.

The workbench's rewrite picker offers exactly that set, so the refusal is rarely
seen from the surface — but the route is the boundary, and it refuses a
hand-shaped body and the CLI verb identically. Editing a document that lives on
`main` outside this tile's material stays `edit-apply`, the main-resident redline
path (FR-017); to rewrite another topic's document in a session, open the
workbench on ITS tile.

Why it is spelled out: worktree containment is not topic ownership. The session
worktree is a whole checkout of the corpus, so "inside the worktree" admitted
every document in it — and the T092 acceptance pass replaced another topic's
1,460-word staged document with a five-line probe, committed onto this tile's
branch under a gate-action record that read as authorised.

The CLI forms (`--actor` is REQUIRED here — the CLI never guesses an identity;
`--content-file` / `--body-file` rather than inline text, so a shell cannot
mangle a document):

```bash
# open or join the tile's session by writing the first document in it
python3 scripts/ideation_dashboard/cli.py gate create-document \
  --repo-root <served checkout> --actor "<name>" \
  --scope-kind staged-topic --scope-id <topic-id> \
  --title "..." --summary "..." --topic <keyword> --area ideation/staging/<topic-id>/ \
  --repository-context <repository> \
  [--continuation resume|new] [--repository <repository>]

# rewrite an existing document INSIDE the session worktree
python3 scripts/ideation_dashboard/cli.py gate edit-document \
  --repo-root <served checkout> --actor "<name>" \
  --scope-kind staged-topic --scope-id <topic-id> \
  --document <path in the worktree> --content-file <file> \
  [--notes "..."] [--repository <repository>]

# save: push the branch and open (or update) its pull request
python3 scripts/ideation_dashboard/cli.py gate open-pr \
  --repo-root <served checkout> --actor "<name>" \
  --scope-kind staged-topic --scope-id <topic-id> \
  [--title "..."] [--body-file <file>] [--repository <repository>]

# end the session without saving; the reason is REQUIRED and durable
python3 scripts/ideation_dashboard/cli.py gate abandon-session \
  --repo-root <served checkout> --actor "<name>" \
  --scope-kind staged-topic --scope-id <topic-id> \
  --reason "<why this exploration stopped>" [--repository <repository>]

# delete an abandoned session's branch, once the topic's proposal exists
python3 scripts/ideation_dashboard/cli.py gate cleanup-abandoned-branch \
  --repo-root <served checkout> --actor "<name>" \
  --scope-kind staged-topic --scope-id <topic-id> --ref <branch> \
  [--repository <repository>]
```

Four flags are easy to miss, and each answers a question the surface asks:

- `--continuation resume|new` — the ANSWER to the resume-or-new report. On a
  tile whose abandoned branch survives, the first write is REFUSED with a report
  naming the branch, both continuations, and the ordinal a `new` session would
  allocate. Omit the flag to be SHOWN the choice; `resume` keeps the existing
  branch and its history, `new` opens the next ordinal.
- `--repository` — the registry key's repository half, on every session verb,
  `create-document` included. Defaults to the checkout directory's name (the same
  convention the worktree container is derived from), and it must be **the same
  value §2's `generate-and-open --repository` carries** — that is the value the
  running serve keys its own sessions on, for the whole process, and a CLI verb
  spelling it differently addresses a different session. Two repositories can carry
  the same tile id, so a branch alone is not a session key. **If you pass it, pass
  the SAME value to every verb of that session.** Nothing on disk records the key —
  the worktree path comes from the checkout and the branch from the tile — and its
  one cross-process artifact is the session's `xf-session-*` notebook alias, which
  is derived from it. A value that differs between the create and the ending
  therefore looks for a notebook that was never created and leaves the real one
  ORPHANED on the shared account (PR #49 review finding 8, leg b). Every verb prints
  a note on stderr when the flag disagrees with the checkout directory's name, and
  an ending that cannot find its notebook says so instead of reporting it retired.
- `--session-repository` — the tie-break for the notebook re-sync when the same
  branch is live in more than one repository.
- `--session-retire` — with `--session-ref`, RETIRE the session notebook because
  the session has ended. There is no re-point at `main`: there is no
  post-session notebook and no route to one.

The notebook re-sync is a plain command against the **aggregation workspace**
(the parent of `openxFactory/` and `xFactories/`), never the served checkout, and
it is dry-run by default — run it without `--apply` first and eyeball the op
list:

```bash
python3 scripts/sync-notebooklm-books.py <workspace root> --session-ref <branch>
python3 scripts/sync-notebooklm-books.py <workspace root> --session-ref <branch> --apply
python3 scripts/sync-notebooklm-books.py <workspace root> --session-ref <branch> \
  --session-retire --apply
```

**The notebook a session OPENS with is deliberately a PARTIAL projection.** The
at-open create runs inside the `create-document` gate action, and the worktree's
governed corpus is large (176 documents on `openxFactory` today) with one `nlm`
upload per document, so that projection carries an aggregate bound — at most
`workbench.SESSION_SOURCE_COUNT_CAP` sources and
`workbench.SESSION_PROJECTION_BUDGET` seconds of wall clock — and the response's
`notebook_notice` says how many sources were projected and how many were
DEFERRED. Nothing failed when you see that notice: a governed write is not
allowed to wait on an external service (D19). The re-sync above is the unbounded
route and it is resumable — it diffs by content hash, so running it adds exactly
the sources that are missing.

## 4. Reading the session on the surface

The workbench's **session bar** is a row of its own, distinct from the
capability pill beside the title: the pill states this plane's AUTHORITY, the bar
states which BRANCH the view is on. Its chip is derived from the active
`(repository, ref)` key plus the serving index's roster — no extra route, no
second liveness signal — and it reads one of:

```text
no branch session · this view is main
session live · <branch> · this view is main
DRAFT VIEW · <branch>
DRAFT VIEW · <ref> · another tile's session
DRAFT VIEW · <ref> · AMBIGUOUS session
session ENDED · <ref>                       (ended during this page's life)
session AMBIGUOUS · <ref> · also tile <id>'s branch
```

The two AMBIGUOUS readings are the honest answer to a question the page cannot
resolve: `draft/<t>-2` is tile `<t>`'s SECOND session and tile `<t>-2`'s FIRST, and
only the engine knows which tile OPENED it (that is what `session-owner/` records —
§5). So when a live ref in this tile's ordinal family is also another advertised
tile's own session branch, the bar says so instead of claiming it, and the notebook
re-sync descriptor fills in no ref — re-syncing that branch could re-sync another
tile's notebook from another tile's worktree. Session verbs still work: they ask the
engine, which answers from the recorded owner and refuses, naming both tiles, when
the answer is genuinely ambiguous. Resolve it by ending that session from the tile
that owns it, or by renaming one tile.

To read a session's own drafts, switch the header's repository selector to
`<repository> @ <branch>` — the serving index advertises a live session as an
ordinary row. The freshness header then names the branch, and the workbench's
docs panel resolves the session's documents. A document created from a
`main`-keyed page is on the session branch, so the read-only viewer answers HTTP
404 for it until you switch refs — that is what the switch is for.

## 5. Where the derived artifacts live

```text
<repo>-worktrees/sessions/<flattened-branch>/            the session worktree
<repo>-worktrees/session-snapshots/<flattened>.snapshot.json   its derived
                                                         snapshot
<repo>-worktrees/session-owner/<flattened>.owner.json    which TILE opened it
<repo>-worktrees/session-dispatch/<flattened>.dispatch.json   a pull request
                                                         opened whose record
                                                         is not written yet
<repo>-worktrees/session-ended/<flattened>.ended.json    an ending that could
                                                         not finish
<served checkout>/ideation/dashboard/gate-records/       main-resident records
```

The last two are the only durable trace of a HALF-FINISHED ending, and both
deliberately outlive the branch:

- `session-dispatch/<flattened>.dispatch.json` — written the moment `open-pr`'s
  push and pull request succeed, cleared the moment its main-resident record
  lands. Finding one means a pull request EXISTS whose FR-029 record may not:
  it carries the branch, the URL, the actor and the time. Do not delete it by
  hand — run `open-pr` again (which updates the SAME pull request, FR-032, and
  writes the record) or `abandon-session`; both finalize the record from the
  marker and then clear it. Deleting it instead discards the only copy of a
  dispatch nothing else names.
- `session-ended/<flattened>.ended.json` — written when an ending (merge or
  abandon) could not finish its teardown, recording which ending it was and what
  residue remains. It is why the next process start reports the leftovers as
  `ended-session-residue` rather than adopting them as a live session — a session
  ends ONCE (FR-021). Finish the teardown the stale report names (remove the
  worktree directory, `git worktree prune`, and delete the branch only if the
  ending was a MERGE), then delete the `.ended.json`. Any open/resume/new on that
  branch clears it too, so a genuinely re-opened session is never reported ended.

Neither file is a session descriptor and neither is a governed artifact (D10):
they are derived operational state, which is why they sit in the container beside
the derived snapshots rather than in the gate-records tree the validators own.

The owner file is what lets the next process — every CLI verb is a new one — say
whose session a branch is. It cannot be derived from the ref (`draft/<t>-2` is tile
`<t>-2`'s first session and tile `<t>`'s second) and the FR-008 bootstrap re-derives
liveness from worktrees, which name a branch and never a tile. Delete it and a live
ordinal session on a tile whose sibling tile spells that ordinal reads as
AMBIGUOUS — the verb refuses and names both tiles, which is the honest answer;
nothing is lost, and the next verb on the owning tile records it again.

The `*-worktrees/` container is already gitignored by the aggregation repository
and already excluded from the NotebookLM scan, so none of this needs a new ignore
entry. The session snapshot deliberately lives OUTSIDE the worktree: inside it,
a derived file would show up in that branch's `git status` and would be one
careless `git add` away from being committed onto a branch whose whole purpose is
reviewable authored content.

## 6. Ending a session

There are exactly two endings, and the dashboard performs neither merge nor
review:

- **The merge ending**, which is THREE steps and the middle one is yours:

  1. The Merge Master merges the pull request in the existing ritual. That moves
     the REMOTE `main`; the served checkout is not told and does not move.
  2. **You update the served checkout — a REQUIRED step, not a courtesy.** On
     `main`, in your own shell:

     ```bash
     git -C <the served checkout> fetch origin main
     git -C <the served checkout> merge --ff-only origin/main
     ```

     No session verb does this for you: nothing in this dashboard fetches
     (FR-026/D17), and the merge happened somewhere this checkout cannot see. Skip
     it and the next `open-pr` refuses `base_stale` — HTTP 409, naming these two
     commands — with the session still live and nothing torn down. That is a
     REFUSAL rather than a failure: the base the merge advanced is not the base
     visible here, so whether the branch merged cannot be observed, and neither
     re-pushing (which would resurrect the head branch the merge deleted) nor
     tearing down (which would delete a branch on a guess) is honest.
  3. The next `open-pr` (from the surface or the CLI) then OBSERVES that the base
     contains the branch, and reconciles: worktree removed, registry entry
     dropped, notebook retired, branch deleted, main view refreshed. The
     main-resident `open-pr` record stays and outlives the branch.

  **The pull request MUST be landed with a merge commit, never a squash** — see
  codexFactory's `docs/pr-admission-merge-readiness.md` §7b for the rule and why
  it is review-only. A squash-landed branch is not an ancestor of `main`, so its
  session stays live on purpose.
- **The abandon ending.** `abandon-session` with a durable reason. The worktree,
  the registry entry, and the notebook go; the branch and any pushed history
  SURVIVE, and deleting the branch later is the separate, human-invoked
  `cleanup-abandoned-branch` verb — offered only once the topic's proposal
  exists.

## 7. Testing rule: a serve used in testing points at a SCRATCH checkout ONLY

**Never point a serve at a real or fixture tree while testing sessions.** A
serve with `--checkout-root` WRITES INTO whatever tree it is given (a proven
hazard, not a theoretical one): gate records land in it, and a session verb
creates a worktree container beside it.

Every session test builds a throwaway repository with a local bare `origin`
(`tests/ideation-dashboard/session_fixtures.py::build_scratch_repo`) under
`tmp_path`, and the same rule governs the browser smoke (the smoke script lives
in codexFactory's `specs/007-workbench-branch-sessions/` Speckit surface — run
it from that checkout):

```bash
python3 specs/007-workbench-branch-sessions/playwright-smoke.py
```

That script builds its own scratch world, constructs the server **in Python** so
the two seams can be fakes — `pull_request_factory` (no `gh`, no network) and
`adapter_factory` (no real NotebookLM notebook) — and drives the whole session
lifecycle through the real browser. It never touches a real checkout, and the
CLI entrypoint is deliberately NOT used for it, because `open-pr` with the real
port pushes with the invoking engineer's own `gh` credential — a real remote
write.

Related invariants the tests assert and you should not work around:

- `nlm` is stubbed in tests; no test creates a real notebook.
- The session's remote write uses the invoking engineer's OWN `gh`
  authentication. There is no token argument anywhere, and a hosted plane never
  gets a pull-request port at all.
