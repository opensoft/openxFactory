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
summary — and the wheel's own column titles are gone, since the tiles carry
them. Each wheel column keeps its 👁 hide control, and a hidden column still
names itself on its vertical rail. The two rows share ONE GRID: the wheel
scales its columns so the visible ones exactly span the port, and the tiles
use the deck's own six-column layout and gap, so tile N sits over column N.
A side effect worth having — the deck no longer pages at the default width,
so the sixth column is whole instead of part-cut.

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
  reading every label. Deliberately subtle, and THEME-AWARE: code chooses only
  the hue (`--h`); saturation, lightness and opacity come from per-theme tokens
  (`--tint-s`, `--tint-l`, `--tint-arc-l`) in the stylesheet. Composing a whole
  `hsl()` in a view shipped tints that read on white and vanished on the dark
  panel (Brett, 2026-08-08: "black on black"); a test now forbids it.
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
- **The lens screen takes the page** (Brett, 2026-08-08) — on the Lens tab the
  stage tiles hide (they head the STAGE views and say nothing about a keyword
  or repository set) and the lens fills the height. The region itself does not
  scroll: the RADAR HOLDS while the document matrix beneath it and the
  vocabulary rail beside it scroll on their own. The lens has no title block
  and the radar has no header: the tab names the view, the
  `305 Keywords | 5 Repositories` switch lives in the RAIL'S HEADER — each
  button STATES ITS COUNT (Brett, 2026-08-09), because two bare lowercase
  words were easy to miss and the count answers "how much is over there?"
  before you switch to find out. Where the header cannot fit them they
  abbreviate to `305 KW | 5 Repos`; which spelling fits is MEASURED after
  mount, not guessed from a character count, because the width depends on
  the theme's font and the reader's zoom. The switch appears only where
  ON EVERY PLANE (Brett, 2026-08-09: "I do not see those buttons") — it used
  to render only where both vocabularies had something to say, so it
  vanished from every single-repository view, and a control that comes and
  goes cannot be learned. Where there is no member set the repository
  button is OFFERED and DISABLED with the reason on it: `1 Repository` is
  worth stating, and a lens over one member draws every document in one
  ring and compares nothing. The rail
  carries a summary card — how many documents are on the radar, over how many
  of the vocabulary, and what a dot and a ring MEAN. Repository rows are
  TILES: each says how much of that repository's corpus is shared with
  another visible repository and how much is its alone. The rail's box is a
  SEARCH, not a filter — it finds rows and never changes what is applied; a
  row still has to be ticked. Beside it, `all` / `none` check or uncheck the
  rows the search is showing (every row when the box is empty). Matching is
  forgiving: every word must appear, in any order, with hyphens read as spaces
  (`work doc` finds `doc-workflow`) — but NOT fuzzy, because a typo quietly
  returning the wrong keyword is worse than returning nothing when the result
  decides what the radar is about. A scrolling pane RESERVES its scrollbar
  gutter (`scrollbar-gutter: stable`): the overlay bar fades, and with it the
  only sign that there is more below.
- **Finding an overlap** (Brett, 2026-08-08) — the keyword rail ranks by
  CONNECTIVITY (how many other keywords a keyword shares documents with), not
  the alphabet, and collapses the long tail: keywords carried by a single
  document wait behind a toggle. Above the rows, RELATIONSHIPS lists the pairs
  that already share documents, strongest first; opening one checks exactly
  that pair, so the radar starts on a real overlap instead of an empty centre.
  From there the existing path applies: the forming pane saves the set as a
  cluster, and `derive-possibles` turns a cluster into candidate ideas.
  The relationship count carries its unit (`14 docs` — documents carrying
  BOTH), because a number that has to be hovered to be understood has not been
  labelled.
- **One document, two views, one hover** (Brett, 2026-08-08) — the radar's
  dot and the matrix's row publish the same key, and pointing at either lights
  the other (the signature grid was a third and has since left this pane; the
  join is written over `[data-doc]`, so it covers however many views publish
  the key). The lit dot PULSES (opacity, not
  size — the packing put the dots as close as they legibly sit, so a growing
  dot would touch its neighbours); a ring of 32 identical circles is a field
  the eye must search, and motion is the one channel it finds without
  searching. The pulse is dropped under `prefers-reduced-motion`, where the
  outline and bold label still carry the join. The lens does the join once,
  in the pane; no renderer knows about another, so a redraw cannot strand a
  binding.
- **A dot is its document's checkbox** (Brett, 2026-08-09) — clicking a dot
  toggles that document's selection: the dot turns `--picked` and its matrix
  row ticks, because both write the same state. The radar is where the
  convergence is READ, so it is where the selection is made. The BOX stays the
  keyboard path (95 focusable dots would flood the tab order), and a dot click
  never fires the region beneath it, which drills in.
- **A switch re-renders IN PLACE** (Brett, 2026-08-09) — the five controls
  that change what is shown (repository jump, repository/project selector,
  refresh, clearing a drill-in) call `render()` instead of reloading the page.
  No navigation, no flash, and the active view is remembered and restored, so
  a jump taken from the wheel stays on the wheel. The TAB is the only thing
  kept: after a repository jump the tile you were on does not exist in the
  repository you jumped to.
  THE RULE THAT MAKES IT SAFE: one `AbortController` per render. Everything a
  render binds outside its own root passes `{ signal }`, and starting the next
  render aborts the last, so no view needs a `destroy()`. Without it the
  second Escape press runs two handlers and the third runs three. Measured
  across four switches: live document listeners flat at 4/1/1/1 against 27
  registrations, and zero navigations. The settings gear stays bound ONCE for
  the page's life — it owns no snapshot state.
- **A page that outlived its serve repairs itself** (Brett, 2026-08-09) — every
  serve start mints a new console token and the page reads `/capabilities`
  ONCE, at load, so a tab left open across a restart presents the old token and
  every guarded write refuses. That refusal fires exactly where it costs most:
  the human has typed a title, a summary and a body, and pressed create. THE
  REPAIR IS A RE-READ, NOT A RELOAD — `location.reload()` would fix the header
  by discarding the textarea, the selection and the drafted seed, which is the
  work the refusal interrupted. So the page re-probes `/capabilities` ONCE,
  takes the new token, and sends the SAME request again, unchanged. It is safe
  to re-send because the two console refusals (`agent_invocation` on the gate
  and edit routes, `console_required` on the doxBench model routes) are raised
  BEFORE the body is read and before any write — the server did nothing, so a
  second attempt cannot double anything. A refusal that might have half-landed
  is deliberately not in that set and stays with the human. Two attempts, never
  a third: a second refusal (or a token that came back unchanged) says
  `this page was loaded against an earlier serve — reload to continue`, and the
  raw FR-019 sentence is never surfaced. This only became necessary once the
  shell started re-rendering IN PLACE (the ruling directly above): before that
  most actions navigated, and a navigation quietly re-read the token on the way
  past. WHAT IS AND IS NOT COVERED: the create and the four session verbs
  (`edit-document`, `open-pr`, `abandon-session`, and doxBench's governed Save)
  retry themselves. Select-to-edit (`edit.js`, a standalone module by test
  pin) and the doxBench chat/catalog do not retry — they carry no unsaved
  text — but they read the token at call time from the same capability object
  the repair writes into, so once anything has repaired it they work again
  without a reload.
- **A live session is a row in the repo filter** (Brett, 2026-08-10: "how do I
  get to the rest of the workbench on this doc?") — under each repository the
  filter (⧩) lists that repository's live session branches,
  `⎇ draft/<topic> · LIVE SESSION`, and selecting one keys the whole dashboard
  to that branch. The serving index has advertised a session as an ordinary
  `(repository, ref)` row all along (FR-014); these lines are that roster shown,
  not a second question asked. TWO defects made a just-created document look
  lost: the repository row resolved to the FIRST roster option for that
  repository and refs sort `draft/…` before `main`, so clicking a repository
  name keyed the dashboard to whichever branch sorted first — a session nobody
  chose; and the selector re-derived its roster only on a five-minute poll, so a
  session opened mid-page was missing from the one control that could address it
  until a reload. A repository row is now `main` deliberately, sessions are
  their own rows, and a create nudges the header so its branch appears at once.
- **The lens opens on the whole corpus** (Brett, 2026-08-10: "we need to have
  all existing docs listed in the main lens screen") — with no keyword checked
  the matrix lists every document in the view, ring column `—`. The RADAR still
  draws nothing, correctly: its rings mean "how many of the checked keywords
  does this carry", so it has nothing to say yet. The matrix is a list, and it
  used to open EMPTY over a corpus of hundreds saying "no documents match the
  checked keywords" — with the document ticks that build a staging seed living
  on those rows, so the seed could not be started at all. Checking a keyword
  returns the matrix to the recipe's membership, unchanged.
- **The draft says what you already have on this topic** (Brett, 2026-08-10:
  "if same keywords, then we want to list it in the doxBench too. so the user
  knows he now has two of this topic") — above the body editor, doxBench lists
  the existing documents that declare any of the seed's shared terms, with the
  ones already sitting in the folder this create aims at FIRST and marked
  `same folder`, because those are the ones a create refuses create-only. It is
  a NOTICE, not a block: a second document on a shared topic is ordinary. The
  reason it exists is that every create-only refusal on 2026-08-10 was this
  same fact arriving from the engine AFTER the press.
- **A session belongs to the SERVE's repository, and the page asks rather than
  infers** (Brett, 2026-08-10) — a create from a PROJECT view landed (`200`, the
  branch opened, the session snapshot generated) and the page then asked for
  `snapshot.json?repository=<project id>&ref=draft/…` and got
  `404 no such snapshot`, so the session opened and its document view never did.
  A session ref can only exist in the repository the serve WRITES to — a create
  naming any other is refused by the route — and `/capabilities` declares it.
  The create already followed that ruling; the RE-KEY after the create did not,
  because under a composed view the shell's own key resolves to the project id,
  which names no repository. Both now read the same declaration.
- **A running write says so on its own button** (Brett, 2026-08-10: "i pressed
  create twice") — a create OPENS A BRANCH SESSION: worktree, branch, commit and
  the session's own regenerated snapshot. On the multi-repository plane, under
  two concurrent presses, that measured 90 seconds. The button only greyed out,
  so the second press joined the session the first had just opened, found the
  document already there, and returned the create-only refusal
  (`corpus documents are create-only`) 77 seconds BEFORE the create that landed
  answered — the human read the refusal of their own duplicate as the outcome of
  their work. `disabled` says "not now" and nothing about "working", so the
  create and the three session verbs now carry a running label for as long as
  the request is in flight, restored afterwards so a refusal is retriable in
  place. The duplicate itself is still refused, and correctly: the create is
  create-only inside a session too (FR-018).
- **The create is the END of the draft** (Brett, 2026-08-10: "after it is
  created, the tabs for the window are not functional. I cannot do anything
  from that point on that document") — a draft stands `docs`/`lens`/`outline`
  down because they read a TILE and a draft has none. The create MAKES the
  tile, so leaving them held ended the create with nothing to do next, over a
  reason (`there is no tile until it is created`) the create had just made
  false. The overlay now stops being a draft and becomes that tile's workbench
  on the session snapshot: the tabs come back, the head names the topic, the
  docs pane lists the created document and the session bar offers rewrite /
  save / abandon. WHICH TILE is matched on the created document's PATH, never
  on the seed's `scopeId` — **two different things are called `staging_id`**:
  the staging seed's is the branch session's composite scope
  (`<repository>:staging:<topic>`) and the snapshot's `staged_topics[]` entry
  is the bare topic. They are not interchangeable, and passing one where the
  other is expected resolves nothing and fails silently.
- **The drafted body really is written** (2026-08-10) — the create-then-edit's
  second verb never fired: `writeBody` built a save buffer of its own shape
  rather than the one `doxbench-save.js` reads, and every mismatch failed
  closed AND silently (no `dirty`, so the planner skipped the row; `document`
  instead of `path`, from which the action is derived; no `owned`; no
  `current_hash`; and both identities un-awaited, `contentIdentity` being
  async). The plan reported `unchanged`, the transport was never called, and
  the note said `the save was refused` over a document that had simply been
  left alone. The verdict was also read as a map when `runSave` reports an
  ARRAY of per-buffer rows. Both are fixed and pinned field-by-field against
  their readers. THE LESSON: this shape is checked at RUNTIME by a pure
  planner, so a wrong field is invisible to every structural test — only
  driving it in a browser found it.
- **A staged tile opens its packet, not its repository** (Brett, 2026-08-09) —
  on a composed view a staged topic offers `read` and `open workbench` and NO
  `open in <repo>`. A staged topic is a packet whose material can span
  members; the workbench opens it scoped, with no reload and no repointing of
  the dashboard. Every other wheel keeps the jump, where the tile IS one
  repository's document.
- **A selection has its own colour** — `--picked` (magenta), on the dot, the
  matrix row and the grid row. Its own token deliberately: every other accent
  already means a stage, and the first attempt reused `--edge-pick`, which is
  the same teal as `--st-staged` — a selected dot measured identical to an
  unselected one.
- **Selecting documents** — every matrix row carries a checkbox (with a
  select-all over the listed rows), and a selection drafts a STAGING-QUEUE
  fragment: the queue's own format, as text, at a folder name that does not
  collide with a topic already staged. The evidence is computed — the
  documents, their repositories, the terms all of them share, the terms only
  some do — and the ARGUMENT is not: the summary, why-now, claims, open
  questions and exit path arrive marked `TO WRITE`, because a drafter that
  argued its own case would be the machine deciding what is worth staging.
  Nothing is written. The panel is a VIEWPORT with ONE ROW OF CHROME (Brett,
  2026-08-08): title, action and dismiss share the title line, the placement
  instructions are that line's HOVER (read once, re-read rarely — a permanent
  note costs the viewport under it on every draft), and the panel itself does
  not scroll, the drafted text inside it does. Two nested scrollers put the
  chrome out of reach of the scroll trying to read the text.
  The panel appears DIRECTLY UNDER THE RADAR (it began as
  a full-width block below the whole layout; the foot of the pane was no
  better at 2,772px down) and can be dismissed — nothing was written, and the
  same selection redrafts it byte for byte.
  Its one action is **open in doxBench**, and it WORKS ON A PROJECT VIEW
  (Brett, 2026-08-08: "yes, we need to draft from a project view"). D10 strips
  every acting capability from a composed snapshot because a gate verb binds
  to one served checkout — true of a TILE-BOUND verb, whose repository this
  serve cannot write to. A NEW document binds to no tile: it lands in the
  serve's OWN checkout. So this one affordance asks whether the SERVE can
  create, not whether the VIEW is a projection; every other surface keeps the
  stripped capabilities unchanged.
  The serve DECLARES the repository it writes to on `/capabilities`, from the
  same authority `refuse_foreign_repository` compares against. The browser
  must never infer it: under a composed view the rendered snapshot's
  `repository` is the PROJECT id, which names no repository and is refused
  (measured — the create carried `Repository context: domains` before this).
  Where the serve cannot create, the panel says so where the button would be,
  and offers a JUMP (`open <repo> to draft`) when exactly one member owns the
  selection — one owner is a destination, not a decision. Offering the button
  anyway and refusing after the click gave a near-empty overlay (Brett: "it
  was blank"). Not copy (Brett, 2026-08-08: "we
  need to not 'copy' this"). Copying makes the human the transport. The seed
  travels instead, as a prefilled GOVERNED create: the staging area, the
  shared terms as Topics, `staged` status, and the provenance line — with
  Title and Summary left empty, because the create refuses without them,
  which is the same rule the seed states by marking them `TO WRITE`. The
  create opens or joins a branch session, so the draft lands on a branch and
  never on main, and save/abandon are the ones that already exist.
  doxBench's DRAFT VIEW lands on the DOCUMENT (Brett, 2026-08-09: "go
  direct in to let the user start working on the doc"): the drafted
  fragment first, its header fields behind a `details` tab, already
  filled in. It renders read-only and says why — `create-document`
  writes the header contract and the BODY is written in the editor that
  opens on the created file, so text typed before the document exists
  would have nowhere to land. TITLE AND SUMMARY STAY EMPTY: the route
  refuses without them and the summary is "yours to write, never
  generated here" (an
  abandoned session's branch SURVIVES — that is the non-committed list you
  return to).
- **The selection bar** — `clear N` at the LEFT, under the checkbox column it
  undoes and carrying the count instead of repeating it in a sentence; the
  draft action CENTRED, because it is the one thing the bar is for, in a
  three-cell grid so a changing label never drags the centre. Over an existing
  draft it reads `re-draft`, not `draft` — it replaces that panel rather than
  making a second, separate seed.
  (The repository lens's `draft seed` is the OTHER seed — a DTN
  candidate-register row, answering whether two factories carry the same
  artifact.)
- **What the dashboard is** — the standing footer paragraph is a
  `what is this?` link opening a modal, so it costs no layout until asked for.
- **The banner row** carries the STALE-FALLBACK warning only. An empty station
  says so in place, which is where the requirement puts it, so the row no
  longer repeats it.
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

### One command instead of the two above: `reserve-dashboard.sh`

The recipe above is what the dashboard NEEDS; it is not what you should type.
Two power cuts in two days (2026-08-12, 2026-08-13) killed a hand-started
fourteen-argument `nohup` serve, and both recoveries depended on an argv file
that happened to survive in a dead session's `/tmp` scratchpad. Neither the argv
nor the plane belonged there.

```bash
scripts/reserve-dashboard.sh              # ensure the plane, then serve
scripts/reserve-dashboard.sh --status     # up or down, exit 0/1
scripts/reserve-dashboard.sh --stop       # stop whatever holds the port
scripts/reserve-dashboard.sh --rebuild    # republish every registered repo first
scripts/reserve-dashboard.sh --supervise  # restart the serve if it CRASHES
```

Three things it does that the manual recipe cannot:

- **The plane has a durable home** — `${XDG_STATE_HOME:-~/.local/state}/xfactory-dashboard/local-plane`,
  not a per-session scratchpad. Override with `XF_DASHBOARD_PLANE`.
- **The argument list is derived, never remembered.** The serving checkout is the
  repo the script lives in, the aggregation root is the nearest ancestor carrying
  `project-register.yaml`, and one `--source-root` is emitted per repository the
  lane actually published — read back out of the `index.json` it just wrote, so
  the serve cannot disagree with the plane about who is in it. `openxFactory`
  resolves to the SERVING checkout, because that is the tree the gate acts on.
- **It is safe to run when already up**, so it is the right thing to type after
  any reboot without checking first.

**What it does NOT do: survive a reboot.** `--supervise` is a restart loop in one
process, so it covers a crash and nothing more. Boot-start needs a service
manager, and this host has none: measured 2026-08-13, `/etc/wsl.conf` carries
`[boot] systemd=false`, PID 1 is `init(Ubuntu-24.04)`, and `systemctl --user`
refuses with "System has not been booted with systemd as init system."
`scripts/systemd/xfactory-dashboard.service` is committed ready for the day
systemd is enabled — its header carries the four enabling steps plus
`loginctl enable-linger`, which is required rather than optional: without it a
user unit waits for a login, so a power cut with nobody logged in still leaves
the dashboard down. The two non-systemd routes (a `[boot] command=` in
`/etc/wsl.conf`, or Windows Task Scheduler at logon) are named in that same
header.

Until one of those is chosen, treat `reserve-dashboard.sh` as the first thing you
type after a power cut.

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

### 2c. doxBench's two model routes have a FOURTH prerequisite

`GET /workbench/model-catalog` and `POST /actions/workbench/chat-turn` need the
three session conditions above **and** one more: the released doxBench wire
schemas must actually resolve. They are read per request — digests re-verified
every time — so a checkout that drifts mid-run stops being trusted at the next
request rather than at the next restart.

How that resolves depends on which repository you are serving from, and the two
postures are deliberately different:

| Serving from | How the contract is verified |
| --- | --- |
| **openxFactory** (the publisher) | the released BYTES: sha256 against the module pin, plus parity with the checkout's own `contracts/manifest.yaml` |
| **a consumer repo** | the same two byte checks, PLUS that repo's `stack.yaml` declaring `xfactory.contract_ref` |

The publisher declares no consumption pin on itself and must not grow one, so
asking it for a `stack.yaml` is a question with no honest answer — that is the
`align-doxbench-contract-pin-to-publisher` ruling (2026-08-10). Nothing else was
relaxed: a drifted digest or a manifest disagreeing with its own bytes still
refuses, in both postures, on the request that sees it.

**When it fails, it fails SILENTLY, and you need to know that.** A contract that
cannot be read gives you `500 catalog_unavailable` / "the model catalog could not
be assembled safely", and nothing else — no stderr line, no reason. The
swallowing is correct on the wire (the real error names checkout paths and
digests, which must never reach a response body), but it means the 500 tells you
only *that* it failed. Do not go looking at providers or credentials; ask the
seam directly:

```bash
# from the served repo root — prints the pin and the checkout it resolved,
# and RAISES the real reason the route is hiding
PYTHONPATH=scripts python3 -c "
from ideation_dashboard import doxbench_contracts as c
print(c.CONTRACT_TAG, '->', c.resolve_root())
c.validators()"
```

Two things that are NOT this failure, and read differently:

- **An empty catalog is a SUCCESS.** With no provider port configured you get
  `200 {kind: workbench-model-catalog, models: []}` and a chat rail that says no
  allowed model is configured, with both editors still usable. That is the
  honest editor-only posture, not a fault.
- **`console_required` (403)** is the console gate one step earlier, not the
  contract — see §0's re-read repair.

Historically this bit for a week: relocating the runtime into openxFactory
(`adopt-neutral-tooling-home`, 2026-08-03) left the consumer-shaped `stack.yaml`
check running inside the publisher, so both routes failed closed from every
checkout of this repo until 2026-08-10. It stayed invisible because the
released-contract test rung was opt-in behind `OPENXFACTORY_ROOT`; it now runs by
default from a publisher checkout, so this class of break surfaces as a test
failure instead of a runtime 500.

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

# delete an abandoned session's local branch after durable retention release
python3 scripts/ideation_dashboard/cli.py gate cleanup-abandoned-branch \
  --repo-root <served checkout> --actor "<name>" \
  --scope-kind staged-topic --scope-id <topic-id> --ref <branch> \
  [--retention-release-reason "<why this orphan may be discarded>"] \
  [--superseding-reference <durable reference>] \
  [--repository <repository>]
```

Cleanup resolves retention independently from current tile presence. Its closed
machine-evidence set is:

1. an active change with the exact declared staged origin (or a surviving
   possibles-pick compatibility edge),
2. an archived change whose own `.openspec.yaml` retains that exact staged
   origin, or
3. an executed demotion to that exact topic. New `gate demote --execute` runs
   write a `demotion-execution-receipt`; legacy demotions require both their
   transition manifest and an exact returned README, INDEX, or round-trip
   fragment. A transition plan or manifest alone never proves execution. An
   execution receipt is accepted only when it accounts for every planned move,
   every returned path stays inside the checkout and exists, and the source
   change folder is gone.

Machine evidence is correlated to this abandonment, not merely to the same tile
id. A new `abandon-session` record captures the exact branch head; active/archive
evidence must be committed, and its commit time (or a demotion receipt's
execution time) must be no earlier than the abandonment. If the evidence is
older, the branch advanced after abandonment, or only a legacy ending marker is
available, the machine lane stays closed and the operator must review the
current head through a fresh explicit retention release.

Cluster, possible, renamed, missing, duplicate, superseded, and otherwise true
orphan branches use `--retention-release-reason`. The reason is mandatory on
that lane; `--superseding-reference` may be repeated to identify where material
was preserved. Missing files, a missing tile, a missing worktree, age, or an
undelivered `propose` dispatch never count as positive evidence.

Every successful cleanup remains human-invoked and local-only. Before deletion
it verifies branch ownership, no live session or attached worktree, and a durable
`abandon-session` proof; then it validates and writes a main-resident
`cleanup-abandoned-branch` gate-action record containing the exact pre-delete
head and retention evidence. The record is filed under the exact ref and moves
from `prepared` to `completed` only after Git atomically deletes that expected
head. The operation holds the repository action lock and refuses if the gate,
Git service, and checkout roots differ. It never deletes the remote branch. If
deletion fails, the prepared record is removed; if record finalization fails,
the exact ref is restored when safe. A surviving `prepared` record therefore
signals recovery work and never claims a completed deletion.

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

To read a session's own drafts, open the header's **repo filter (⧩)** and click
the session's own line under its repository — `⎇ draft/<topic> · LIVE SESSION`.
The serving index advertises a live session as an ordinary `(repository, ref)`
row, so these lines are that roster shown rather than a second question asked.
The freshness header then names the branch, and the workbench's docs panel
resolves the session's documents. A document created from a `main`-keyed page is
on the session branch, so the read-only viewer answers HTTP 404 for it until you
switch refs — that is what the switch is for.

**This paragraph was stale, and the way it was stale cost a real evening**
(Brett, 2026-08-10: "how do I get to the rest of the workbench on this doc?").
It used to say "switch the header's repository selector to
`<repository> @ <branch>`", and the project-first header had replaced that
ref-bearing selector with a per-repository filter. Worse, the repository row
resolved to the FIRST roster option for that repository, and refs sort with
`draft/…` before `main`: clicking a repository name keyed the whole dashboard to
whichever branch happened to sort first — a session nobody had chosen. So a
session was reachable only by accident and under the wrong name, which is why a
document a create had just landed looked lost. A repository row is now `main`
deliberately, and every live session is an addressable row of its own.

### 4a. A session torn down by hand: reconcile its notebook

The two governed endings retire the session notebook. A session removed any
OTHER way — a probe clearing up, crash residue swept, a `git worktree remove`
by hand — retires nothing, and its notebook survives on the account shared
across the family.

`--session-ref --session-retire` cannot clean that up, BY DESIGN: it resolves
liveness first and refuses a dead branch, which is exactly what stops it
inventing a session and retiring a LIVE one's notebook. Do not try to relax it.
The dead case has its own door, which establishes death differently — from no
live session anywhere claiming the notebook:

```bash
# report (default): what is live, what is orphaned, what belongs elsewhere
python3 openxFactory/scripts/sync-notebooklm-books.py . --session-sweep
# and then, having read it:
python3 openxFactory/scripts/sync-notebooklm-books.py . --session-sweep --apply
```

It REFUSES rather than guesses. A repository it cannot enumerate — absent
checkout, git failure, unreadable container — looks exactly like a repository
whose sessions have all ended, so any such repository refuses the whole run and
retires nothing. A notebook naming a repository this workspace does not carry is
another workspace's and is reported out of scope. A workspace resolving no
session repositories retires nothing at all.

**Run it from the WORKSPACE ROOT**, not from a feature worktree. Liveness is
sought across every worktree git lists for each session repository, because a
session's container is keyed on the checkout it was opened FROM — the first
implementation asked only canonical checkouts and reported two live sessions as
dead (2026-08-10), which is why that enumeration is now complete and why the
report is worth reading before `--apply`.

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
  `cleanup-abandoned-branch` verb — permitted only after exact active, archived,
  or executed-demotion custody is proved, or after a human records a separate
  explicit retention-release reason for a true orphan.

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
