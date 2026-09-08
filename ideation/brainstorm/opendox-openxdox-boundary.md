# openDox / openXdox / Descendant — Where the Boundary Falls in 80K Lines — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A three-column first-pass assignment of today's 48 modules and 102
promoted requirements under Brett's Q5 three-layer test — would someone with no
notion of factories, gates or tenants use it (openDox), is it the machinery
common to how Medx, Ledgerx and Adx map onto the workbench (openXdox), or is it
one domain's own mapping (a descendant) — with the pull-up candidates that make
openDox a stronger brainstorming and research-analysis tool named explicitly,
and the corpus-adapter seam ruled by Q4 (openDox defines the interface, openXdox
implements it, the two back-imports move to a small neutral module, the
dependency points one way) as the change that has to land before any of it.
Topics: opendox, openxdox, codexdox, ideation-dashboard, doc-health, repo-split,
corpus-adapter, module-boundary, import-cycle, coupling, doxbench,
domain-descendant-boundary, neutral-product-pin, pull-up, feat-request
Repository context: measures `openxFactory` at `origin/main` `bc1bd4ee`
(2026-09-04); proposes a three-column assignment across two repositories that do
not exist yet and the descendants below them
Captured: 2026-09-04

## Possible feats

- **The corpus adapter, as ruled** — openDox declares how documents are listed,
  read, written back and checked with no knowledge of OpenSpec or doc-health;
  openXdox implements it over openxFactory's corpus and check families.
- **The neutral module both sides depend on** — the two `doc_health` →
  `ideation_dashboard.boundary` back-imports move there, and the dependency
  points one way for the first time.
- **Split `serve.py` behind an app-server extension point** — 6,733 lines
  carrying both the app server and the corpus routes; the extension point is
  what lets openXdox contribute routes without forking the server.
- **The pull-up wave** — move the abstracts, knowledge and compression stack,
  the lens, the generic half of the notebook projection and the editor/chat
  surface up into openDox so a lab assistant gets them with no factory at all.
- **Split the test suite with the code** — 125 test files and 3,927 test
  functions, 52% of this repository's whole test count, with the post-split
  collection counts summing to the pre-split count.

## The test, as directed

Brett's Q5 direction of 2026-09-04 replaces "app versus integration" with three
questions asked of every module and every requirement:

1. **openDox** — would someone with no notion of factories, gates or tenants
   use it? A student. A lab assistant. Manage documents, brainstorm, do research
   analysis, connect to NotebookLM. Domain-neutral and external to openxFactory.
2. **openXdox** — is it the core machinery common to how MedxFactory (patient
   management and research), LedgerxFactory (financial simulations, accounting
   questions) and AdxFactory (marketing analysis) each map onto the workbench?
3. **Descendant** — is it one domain's own mapping?

The third column is the one that changes the arithmetic, and
[the domain-mappings document](opendox-domain-mappings.md) argues it takes a
great deal more than expected: most of what an "integration layer" does today is
openxFactory-and-OpenSpec-specific, which under this test is `codexDox`, not the
common core. That claim is held there as a hypothesis. This document assigns
under the CONSERVATIVE reading — openxFactory's governance vocabulary counts as
neutral governance rather than one domain's mapping — and flags every row where
the aggressive reading would move it.

## What we are cutting

Measured at `origin/main` `bc1bd4ee`, 2026-09-04:

| Surface | Size |
| --- | --- |
| `scripts/ideation_dashboard/` | 48 modules, 49,605 LOC |
| `web/` | 40 files, 30,410 LOC (excluding vendored `markdown-it.min.js`) |
| `tests/ideation-dashboard/` | 125 files, 3,927 `def test_` — 52% of the repo's 7,612 |
| `openspec/specs/ideation-dashboard/spec.md` | 289,266 B, 102 requirements, 472 scenarios |
| Contract schemas | 4 (`*-snapshot`, `*-snapshot-index`, workbench model-catalog, chat-turn) |
| Packaged examples | 142 under `examples/ideation-dashboard/` |
| Archived changes with a delta | 30 |
| Active changes with a delta | 5 (two with open archive gates) |

## Three-column assignment — the 102 promoted requirements

Cluster counts read off the requirement titles; clusters overlap and the sum is
under 102, so this is a reading rather than a partition.

| Cluster (approx. count) | openDox | openXdox | Descendant | Note |
| --- | --- | --- | --- | --- |
| doxBench surface and editor (17) | **yes** | | | Pure app. A student edits a document. |
| Branch sessions (10) | **yes** | | | Git safety is neutral; WHICH acts exist is not. |
| Abstracts (8) | **yes — PULL UP** | | | Deterministic + distilled abstracts are a research tool. |
| Provider and broker (6) | **yes** | | | Model access is app infrastructure. |
| Hosted actor and account (4) | **yes** | | | Q1 puts users in the openDox database. |
| Knowledge / compression / chat (4) | **yes — PULL UP** | | | Bounded context packets over a document set: the research-analysis core. |
| Projects (9) | **yes** | partly | | Q1 puts projects and the project↔repo map in the database; the COMMISSION loop is openXdox machinery. |
| Lens (4) | **PULL UP the set-builder** | the lifecycle regions | | A keyword set-builder is neutral; "convergent regions draft candidate-register seeds" is not. |
| Gate console and verbs (17) | | **yes** (the loop) | the verb vocabulary | Record-intent / name-human / gate-on-authority / dispatch is common to all three domains; `ratify`, `promote`, `demote` are codex's words. |
| Projection and snapshot (8) | | **yes** (the mechanism) | the status vocabulary | A freshness-keyed projection that refuses honestly is common; a nine-word taxonomy is not. |
| Funnel and wheel (7) | | **yes** (the shape) | the stage names | Every domain has a pipeline with gates; `brainstorm → staged → ratified` is codex's. |

Under the aggressive reading of the domain-mappings document, the last three
rows' "descendant" halves grow and their "openXdox" halves shrink to the
parameterized engine only.

## Three-column assignment — the 48 modules

Sizes in LOC. **PULL UP** marks a module the direction asks us to move up into
openDox to make it a better brainstorming and research-analysis tool.

### openDox — the app a student or a lab assistant would use (~24.9K)

**Editing and canvas** — `doxbench_turns` 1,857 · `doxbench_threads` 1,417 ·
`doxbench_model` 1,343 · `canvas_drafts` 221 · `doxbench_hash` 112.

**Research and analysis — the pull-up wave** — `doxbench_knowledge` 1,231
(**PULL UP**: bounded context packets over a selected document set — the single
most valuable module for a lab assistant, currently filed as a governance
concern because its input is a "staged set") · `doxbench_abstract_store` 446
(**PULL UP**) · plus the abstract-generation surface inside `doxbench_turns`.

**Model plane** — `doxbench_bridge` 1,605 · `doxbench_provider` 906 ·
`doxbench_intake` 736 · `doxbench_binding` 557 · `doxbench_mcp` 567 ·
`doxbench_memory_gateway` 608 · `doxbench_telemetry` 380.

**Git and sessions** — `branch_session` 5,290 · `session_git` 1,199 ·
`session_pr` 443. Neutral by the test: a student who keeps notes in a git
repository wants branch-per-working-set and one pull request, and needs no
notion of a gate.

**Identity, accounts and app plumbing** — `actor_identity` 304 · `boundary` 377
(its `OutputBoundary` is what Q4 moves to the shared neutral module) ·
`action_errors` 45 · `fixtures` 101 · `doxbench_install` 339 · `__init__` 18.

**NotebookLM** — `notebook_action` 239 (**PULL UP** — "Open in NotebookLM" is
exactly the connection the direction names, and it is 239 lines).

**Set-building** — the keyword-query half of `lens` 282 (**PULL UP**; the
candidate-register half stays above).

### openXdox — the machinery common to the three domain mappings (~10.9K, plus what does not exist yet)

**The adapter implementation and projection mechanism** — `corpus_root` 101 ·
`generator` 912 · `snapshot` 223 · `snapshot_registry` 1,318 · `register` 185 ·
`completeness` 543 · `round_trip` 370.

**The gate and commission loop** — `gate_console` 2,207 · `gate_routes` 3,552 ·
`kickoff` 1,006 · `record_binding` 259 · `register_edit_lane` 337.

**Scope and ownership authority** — `doxbench_scope` 841 (derives ordered
sections and editable ownership from the snapshot — the "who may edit what"
machinery every domain needs).

**Missing entirely, and the largest gap:** the model/scenario workbench for
`governed-derived-model` families. All three domains declare one — Medx's Dream
Object / Simulation Scenario at the `governed` tier with ratified templates,
Adx's Persona / Campaign Simulation at `calibrated`, Ledgerx's Counterparty
Health Profile / Financial Scenario — and there is no UI for any of them
anywhere in these 80K lines. Likewise the evidence-and-provenance surface
(invariant 2's evidence traces and assumption registers) and the
role-and-authority projection.

### Descendant — one domain's own mapping (~5.0K under the conservative reading)

**codexDox: the OpenSpec-and-doc-health specifics** — `doxbench_packet` 1,375
(lifecycle status, packet shape) · `doxbench_contracts` 780 (the released
contract pin) · `human_seen` 476 (cross-reference recommendation queue) ·
`nightly_lane` 589 · `dashboard_refresh_lane` 2,071 · `intent_apply_lane` 744.

The three lanes are the clearest descendant content in the package: their whole
subject is thawing a git corpus into a served snapshot for openxFactory's own
repositories, and Q1's ruling ("git owns governed artifacts, read from
repositories and written back only through the apply lane") makes the apply lane
a permanent fixture of the openxFactory mapping specifically.

Under the aggressive reading this column also takes the status vocabulary out of
`generator`/`snapshot_registry`, the stage names out of the funnel, and the verb
vocabulary out of `gate_console` — roughly 3–5K more, all of it as
parameterization rather than as moved files.

### The residue that must be split by function (10.9K, and this is the real work)

- **`serve.py` — 6,733 lines.** The app server AND the corpus server in one
  file, with three `doc_health` imports. openDox keeps the server, static and
  canvas routes, chat and model routes, and `/capabilities`; openXdox
  contributes snapshot, `/source` and projection routes through an extension
  point openDox exposes. Without that extension point the integration layer has
  to fork the server, which is a fork rather than a profile and breaks the same
  rule `domain-descendant-boundary` applies one level down.
- **`cli.py` — 2,456 lines.** Neutral verbs and governance verbs in one argument
  parser; splits the same way, with openXdox contributing subcommands.
- **`workbench.py` — 1,575 lines.** Reference-set manifests and scratch
  notebooks are openDox (a lab assistant's working set); what a reference set
  MEANS in a promotion funnel is above. Four `doc_health` imports.
- **`authoring.py` — 329 lines.** Header-authoring machinery is openDox; its
  required-field vocabulary comes from the adapter's classify operation.
  `REQUIRED_HEADER_FIELDS` is co-authoritative with
  `doc_health.corpus.STATUS_SCAN_LINES` today.

Roughly: 24.9K openDox + 10.9K openXdox + 5.0K descendant + 10.9K residue
against a measured 49.6K. The residue is where the three columns actually meet,
so treat the split as three columns plus a seam rather than as four buckets.

## What to pull up, and why each one

The direction asks specifically what to pull up "to make openDox more useful as
a brainstorming and research analysis tool". Ranked by value to a lab assistant
who has never heard of a factory:

1. **The knowledge and compression stack** (`doxbench_knowledge` 1,231, plus the
   three-layer compression contract). Assembling a bounded context packet over a
   set of documents you selected, with declared fidelity, is the core research
   move. It is currently filed as governance only because its input set is named
   "the staged set".
2. **Abstracts** (`doxbench_abstract_store` 446 plus the generation surface).
   Deterministic abstracts that state their own absences, and a separately
   invoked model-derived distilled abstract verified against the document's
   declared fields, with a cache keyed by path-digest-model. This is a literature
   -review tool that happens to live in a governance dashboard.
3. **The lens set-builder** (the keyword-query half of `lens` 282). Naming an
   intensional set the machine clustering missed is how a human actually
   organizes twenty papers.
4. **NotebookLM connection** (`notebook_action` 239, plus the generic half of
   the projection). The direction names it explicitly. What must NOT come up is
   the stage-to-book mapping: one Ideation book per governed repo mirroring the
   lifecycle stages is openxFactory's mapping. A per-project book is the neutral
   shape.
5. **The editor and chat bound to the active buffer** (the `doxbench_*` editor
   family). Already assigned to openDox; listed here because it is the surface
   the other four are used through.
6. **Branch sessions and projects.** Already assigned; the pull-up content is
   the FRAMING — a project that owns documents and a session that owns a branch
   are app concepts, and Q1's ruling puts both in the openDox database.

Two things deliberately NOT pulled up: the calibration loop (Adx's
`calibrated`-tier predicted-versus-actual writer — it is domain machinery, and
openDox has no outcome to read) and the gate console (a student has nobody to
gate against).

## The coupling — measured, and now ruled

**Outbound: 12 of 48 modules, 23 import statements.** `authoring` (2),
`cli` (1), `completeness` (1), `corpus_root` (1), `doxbench_packet` (1),
`gate_console` (4), `gate_routes` (1), `generator` (3), `round_trip` (1),
`serve` (3), `snapshot_registry` (1), `workbench` (4). What they pull: `corpus`
and `corpus.RealGit`, `lines.split_keepends`/`join_rows`, `derive_possibles`,
`families.FAMILIES`, `TAXONOMY`, `DEFAULT_THRESHOLDS`, `staging_seed`,
`shared_identity`, `pin_sentinels`, `ideation_readiness`, and
`runner.Context`/`run_suite`.

**Inbound: exactly two statements.** `doc_health/derive_possibles.py:857` and
`doc_health/ideation_readiness.py:1351`, each
`from ideation_dashboard.boundary import OutputBoundary  # lazy: house guard`.
Every other `ideation_dashboard` mention inside `doc_health`
(`corpus.py:193-195`, `lines.py:46-50`, `pin_sentinels.py:56`,
`pin_class.py:413`) is a prose comment recording a co-authoritative reading
window, not an import.

**Brett ruled the resolution on 2026-09-04 (Q4).** openDox DEFINES the
corpus-adapter interface — how documents are listed, read, written back and
checked, with no knowledge of OpenSpec or doc-health. openXdox IMPLEMENTS that
interface over openxFactory's corpus and check families. The two back-imports
move into a small neutral module both sides depend on. **The dependency points
one way: openXdox depends on openDox, never the reverse.** Rejected: openDox
pinning doc-health as a library, which inverts the layering; and openXdox as a
tuned copy with no shared interface, which guarantees divergence and makes every
fix land twice.

So the seam is settled in shape. What remains is the five operations' signatures
and where the neutral module lives — and the observation that under Q4's
direction, the 23 outbound imports become the adapter's implementation surface
rather than a dependency to remove: they move to openXdox, where importing
doc-health is legitimate.

## The web tier

40 files, 30,410 lines, and it was not measured for this split. The same three
columns are visible from the promoted requirements: the account menu, canvas,
editor, chat, docs tile and theme controls are openDox; the gate console and
drill-in are the gate loop; the wheel, funnel and lens regions carry stage names
that are one domain's mapping. The front end has no package boundary at all
today, so it needs one invented rather than discovered — and it is where a
"student-usable openDox" is won or lost, because the app's whole value to a lab
assistant is its surface.

## What contradicts what

Marked as contradiction because this is a brainstorm and this is where it is
legal:

1. **This document's conservative assignment contradicts the domain-mappings
   document's aggressive one** over roughly 15K lines: whether the projection,
   gates, lanes and lens vocabulary are the common core or `codexDox`. The
   conservative reading is what an extraction of today's code would produce; the
   aggressive one is what the three-layer test implies. Unresolved on purpose.
2. **`serve.py` is the boundary AND cannot be split last.** The split is only
   meaningful once the route families separate, and it is the most-changed module
   in the package with five active changes touching it. Both true; they conflict
   on sequencing.
3. **The LOC ratio and the requirement ratio agree, which may be luck.** About
   49 of 102 requirements read as openDox, about 36 as openXdox-or-descendant,
   9 as projects on the fence — roughly matching the LOC cut closely enough to
   be suspicious of both readings.
4. **Five active changes make any cut wrong.**
   `add-nightly-dashboard-refresh` (13 open tasks, cross-repo across three
   repositories, ADDS seven `doc-health` requirements — deepening the exact
   coupling Q4 rules should point one way, and its lane has three runs and no
   successes), `retire-doxbench-chat-turn-v1` (7 open, schema bytes already
   moved), `add-doxchat-model-intake` (built, unarchived),
   `add-composed-view-authoring` and `add-lens-document-selection`. A cut now
   strands or re-homes all five; waiting for all five means waiting on a lane
   that has never succeeded.
