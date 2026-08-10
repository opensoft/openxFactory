# Proposal: split-ideation-book-per-repo

code_surface: openxFactory
target_release: implementation_pending

Status: ratified
Ratified: 2026-08-10 by Brett Heap — in-session, verbatim: "ratified"
(response to the proposal presentation including the cross-model decision
review and its one declined judgment, which therefore stands as authored:
headroom warning + further-delta rule, no pre-authorized splits).

## Why

On 2026-08-10 the shared Ideation book hit NotebookLM's per-notebook source
cap (300 sources) mid-sync: the run added five sources, reached the cap, and
the next `nlm source add` failed — with an empty provider error — leaving the
run dead and every subsequent ideation document across all governed repos
silently unprojected. The workflow doc's Known Limitations section
(`docs/lifecycle-notebook-projection.md` §11) anticipated exactly this and
prescribed the direction: split by repo (it expected Working Drafts to get
there first; Ideation won the race).

The measured distribution makes the shape obvious. Of the 300 capped sources:
openxFactory 188, LedgerxFactory 62, MedxFactory 36, codexFactory 11,
OpsxFactory 4 (plus charter/grounding). A single shared book cannot hold the
family's ideation corpus and never will again — ideation is the highest-churn
lifecycle state, and each repo's corpus grows independently. Per-repository
Ideation books give every repo its own full cap, and growth in one domain can
never again block another domain's projection.

Honest sizing (measured 2026-08-10, corpus scan): the cap already dropped
part of the corpus — openxFactory alone carries ~212 brainstorm/staged
documents against the 188 the capped book held, so its per-repo book opens
at roughly 216/300 with the charter and grounding seeds. The split buys the
four domain books a 20–40x runway but openxFactory a bounded one; the
capacity guard below exists so the next crossing is a warned, named,
governed event with lead time — not a dead run.

The book definitions are contract, not implementation preference (this
capability's "Projection implementation ownership" requirement), so the split
requires this delta before the sync implementation changes.

## What Changes

- **Per-repository Ideation books, resolved by title.** `brainstorm` and
  `staged` documents project into the Ideation book of their owning
  repository — title family `xFactory Ideation — <RepoName>` (the provider's
  truth and the resolution key), alias family `xf-ideation-<repo-slug>` as a
  machine-local operator convenience, re-registered idempotently and never
  fatal when absent (aliases live in a per-machine CLI store; a second host
  or CI runner must not die on them). A repo's book is created lazily on the
  first APPLY-mode sync where the repo has status-derived ideation
  membership (charter/grounding seeds never trigger creation); dry runs
  report the pending creation and mutate nothing. Creation seeds the full
  contract surface: title, `xfactory,lifecycle` tags, chat framing, charter
  + grounding, and the book's `external_source_workspace` record.
- **Working Drafts and Canon stay single** (161 and 71 sources today). Any
  book's eventual split is a further delta to this capability — and the
  guard names that owed delta for ANY book that runs low with no successor
  split defined (closed-world, not a two-book exception list; the
  openxFactory ideation book is expected to be the first to trip it).
- **Projection capacity guard (new requirement).** Projected occupancy —
  desired managed set + charter + observed unmanaged sources, against a
  named cap constant — is preflighted per book: a headroom warning at ≤ 30
  sources (lead time for ratifying the owed split), a deterministic in-cap
  prefix with the exact excess reported and a nonzero exit on overflow, and
  per-book containment of every preflightable failure (unresolvable book,
  refused creation, cap) so one bad book never kills the rest of the run.
- **Migration and retirement, sequenced honestly.** The per-repo books are
  populated by the normal reconciliation sync — but as one book per run
  (`--book`), small books first, fresh auth per session: ~345 source
  operations at ~2s each exceed a single ~20-minute nlm session, and the
  manifest now flushes per book so an interrupted run resumes instead of
  deleting and re-adding everything. The legacy book leaves the sync's book
  set at implementation (it is over-cap by construction and must not be a
  target during migration); after per-repo parity is verified by title-set
  equality against the corpus scan, the legacy book and its `xf-ideation`
  alias are retired by a recorded manual act. The legacy alias is retired,
  not repointed — an alias that silently changed meaning would corrupt
  every operator habit and doc reference at once.

## Capabilities

### Modified Capabilities

- `lifecycle-notebook-projection`: the "Derived notebook membership"
  requirement routes ideation membership per-repository; a new "Projection
  capacity guard" requirement makes the cap a reported, non-silent
  constraint.

## Impact

- `scripts/sync-notebooklm-books.py`: per-repo book derivation; title-based
  resolution with idempotent alias re-registration; apply-gated lazy create
  via the centralized create adapter pattern (`ideation_dashboard/workbench.py`
  — known `nlm notebook create` CLI drift lives there, solved once); tags +
  chat framing applied at creation (`CHAT_PROMPT` is currently applied by no
  code path — this change closes that gap for the books it creates);
  capacity preflight; dynamic `--book`; manifest keyed by the new book
  identities, flushed per book, stale `ideation` key dropped.
- `examples/lifecycle-notebook-workspaces.yaml`: per-repo book
  `external_source_workspace` records written at creation (their provider
  ids do not exist until then); the legacy ideation record retires with its
  book.
- Tests that bind to the legacy key/alias:
  `tests/notebooklm/test_sync_notebooklm_books.py` and
  `tests/ideation-dashboard/test_authoring_agent.py` (ideation-dashboard
  set-removal conformance) — updated, with a companion delta owed if the
  `ideation-dashboard` spec text itself names the legacy book.
- `docs/lifecycle-notebook-projection.md`: book table, title/alias
  resolution rule, tags, cap constant + headroom policy, grounding fan-out
  cost note (a grounding edit now re-projects into every book), migration
  record, §11 update.
- Sequenced migration runs from the workspace root, then legacy book
  retirement as a recorded manual act.
- Cross-repo follow-up (non-blocking): the aggregation repo's CLAUDE.md
  names the three legacy aliases; update its NotebookLM projection note
  after migration.
- No schema changes; no changes to hybrid notebooks, imports, drafts/canon
  membership, or scan scope. Grounding and framing requirements are
  unmodified in text; their per-book fan-out cost is acknowledged above.
