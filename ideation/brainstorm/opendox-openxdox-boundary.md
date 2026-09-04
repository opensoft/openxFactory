# openDox / openXdox — Where the Boundary Falls in 80K Lines — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A measured first cut of today's workbench into the two ruled layers —
about 24K lines of the 49.6K Python plausibly neutral (the editor, chat,
provider, session-git, model and account families), about 15K plausibly
integration (the projection, the gate console and routes, the three lanes,
completeness and round-trip), and a hard residue of three modules totalling
11.4K lines that do both and must be split by function rather than by file —
plus the corpus adapter, the one seam that has to exist first because
`doc_health` and `ideation_dashboard` currently import each other.
Topics: opendox, openxdox, ideation-dashboard, doc-health, repo-split,
corpus-adapter, module-boundary, import-cycle, coupling, doxbench,
neutral-product-pin, feat-request
Repository context: measures `openxFactory` at `origin/main` `bc1bd4ee`
(2026-09-04); proposes a first cut into two repositories that do not exist yet
Captured: 2026-09-04

## Possible feats

- **The corpus adapter** — a named interface openXdox implements and openDox
  consumes, replacing the direct `doc_health` imports and breaking the back-edge
  that `doc_health` currently has into `ideation_dashboard.boundary`.
- **Relocate `boundary.py` to the shared floor** — the entire reverse dependency
  is two lazy imports of one class in one 377-line module; moving it is the
  cheapest cycle break available.
- **Split `serve.py` by route family** — 6,733 lines carrying both the app
  server and the corpus routes; the split is the boundary made executable.
- **Split the test suite with the code** — 125 test files and 3,927 test
  functions, 52% of this repository's whole test count, have to land on one side
  or the other, and a suite that cannot be split is a boundary that is not real.
- **A neutral conformance corpus for openDox** — the wallet extraction's 17
  positives and 36 negative confirmations are the pattern; openDox needs its own
  so a descendant can prove conformance without openxFactory's corpus.

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

## A first cut of the 48 modules

Not a proposal — a first reading, to find out whether the boundary is even
tractable. Where a module lands "by function" it means the file has to be split,
not moved.

### Plausibly openDox — the app (~24.3K LOC)

**Editing and canvas** — `doxbench_turns` 1,857 · `doxbench_threads` 1,417 ·
`doxbench_model` 1,343 · `canvas_drafts` 221 · `doxbench_abstract_store` 446 ·
`doxbench_hash` 112.

**Model plane** — `doxbench_bridge` 1,605 · `doxbench_provider` 906 ·
`doxbench_intake` 736 · `doxbench_binding` 557 · `doxbench_mcp` 567 ·
`doxbench_memory_gateway` 608 · `doxbench_telemetry` 380.

**Git and sessions** — `branch_session` 5,290 · `session_git` 1,199 ·
`session_pr` 443.

**Identity and app plumbing** — `actor_identity` 304 · `boundary` 377 ·
`action_errors` 45 · `fixtures` 101 · `doxbench_install` 339 · `__init__` 18.

**NotebookLM** — `notebook_action` 239.

### Plausibly openXdox — the integration (~15.0K LOC)

**Lifecycle projection** — `generator` 912 · `snapshot` 223 ·
`snapshot_registry` 1,318 · `completeness` 543 · `round_trip` 370 ·
`corpus_root` 101 · `register` 185.

**Gates** — `gate_console` 2,207 · `gate_routes` 3,552 · `kickoff` 1,006 ·
`record_binding` 259 · `human_seen` 476.

**Lanes** — `dashboard_refresh_lane` 2,071 · `intent_apply_lane` 744 ·
`nightly_lane` 589 · `register_edit_lane` 337.

**Corpus-shaped views** — `lens` 282 · `doxbench_scope` 841 ·
`doxbench_knowledge` 1,231 · `doxbench_packet` 1,375 · `doxbench_contracts` 780.

### The residue that does both (11.4K LOC, and this is the real work)

- **`serve.py` — 6,733 lines.** The HTTP server. It is simultaneously the app
  server (static assets, the canvas, the account menu, the chat routes,
  `/capabilities`) and the corpus server (snapshot routes, `/source`, the
  lifecycle projection endpoints). It imports `doc_health` three times. This
  file is the boundary; splitting it is not a refactor you do at the end.
- **`cli.py` — 2,456 lines.** The one entry point for generate, serve,
  gate verbs and lane invocations. Neutral verbs and governance verbs in one
  argument parser.
- **`workbench.py` — 1,575 lines.** Reference-set manifests, scratch notebooks
  and bounded actions. Four `doc_health` imports. Manifests and notebooks are
  neutral; what a reference set means in the promotion funnel is not.
- **`authoring.py` — 329 lines.** Header authoring. Two `doc_health` imports;
  `REQUIRED_HEADER_FIELDS` is co-authoritative with
  `doc_health.corpus.STATUS_SCAN_LINES`. Neutral machinery over a governed
  vocabulary — exactly the shape the adapter exists for.

That is 24.3K + 15.0K + 11.4K ≈ 50.7K against a measured 49.6K; the arithmetic
is approximate because three of the four residue modules are double-counted in
spirit. Treat the ratio, not the totals: roughly half the code is plausibly
neutral, a third is integration, and a sixth has to be cut by hand.

## The coupling — measured, both directions

**Outbound: 12 of 48 modules, 23 import statements.** `authoring` (2) ·
`cli` (1) · `completeness` (1) · `corpus_root` (1) · `doxbench_packet` (1) ·
`gate_console` (4) · `gate_routes` (1) · `generator` (3) · `round_trip` (1) ·
`serve` (3) · `snapshot_registry` (1) · `workbench` (4). What they pull:
`corpus` and `corpus.RealGit` (repo discovery, doc iteration, header parsing),
`lines.split_keepends` / `join_rows`, `derive_possibles`, `families.FAMILIES`,
`TAXONOMY`, `DEFAULT_THRESHOLDS`, `staging_seed`, `shared_identity`,
`pin_sentinels`, `ideation_readiness`, `runner.Context` / `run_suite`.

**Inbound: exactly two statements, and they are the good news.**
`doc_health/derive_possibles.py:857` and `doc_health/ideation_readiness.py:1351`
each do:

```python
from ideation_dashboard.boundary import OutputBoundary  # lazy: house guard
```

The whole back-edge is one class, in one 377-line module, imported lazily in two
places, with the comment already admitting what it is. Everything else in
`doc_health` that names `ideation_dashboard` is a prose comment recording
co-authoritative reading windows — `corpus.py:193-195`, `lines.py:46-50`,
`pin_sentinels.py:56`, `pin_class.py:413` — which are documentation debts, not
imports.

**So the cycle is asymmetric and cheap to break.** The expensive direction is
the 23 outbound imports; the cheap direction is two. Relocating `OutputBoundary`
(or its protocol) into a shared floor that both packages depend on removes the
cycle in a single change, before any repository exists. That is the first slice.

## The corpus adapter — naming the seam

The measured path literals in the dashboard package are the shape of the seam:
`ideation/staging` in 16 modules, `contracts/` in 15, `docs/` in 9,
`ideation/brainstorm` in 8, `openspec/changes` in 7, `ideation/dashboard` in 6,
`openspec/specs` in 2. Those are not incidental strings; they are the reader's
knowledge of openxFactory's tree layout, spread across a third of the package.

A **corpus adapter** is the interface that turns all of that into one
dependency:

- **Enumerate.** Give me the governed documents, each with a path, a digest, a
  lifecycle state and a set of topics. openDox does not know how the state was
  determined.
- **Read and write.** Fetch a document's bytes; write them back through a
  session (branch, commit, pull request) that openDox already owns.
- **Classify.** Ask the adapter what state a document is in and what
  transitions are legal from it. openXdox implements this against
  `document-lifecycle`; a plain openDox install implements it as a trivial
  `draft`/`published` pair.
- **Assess.** Ask for findings over the corpus. openXdox implements it by
  running doc-health; plain openDox returns none.
- **Act.** Record a governance act with an actor and a reason. openXdox maps
  this onto gate-action records and workflow-job descriptors; plain openDox
  records it in its own audit table.

Notice what that does to `doc_health` itself. Under the adapter, doc-health
becomes an openXdox concern that openDox never imports — which resolves the
inbound edge by construction and gives openXdox somewhere legitimate to hold
`FAMILIES` and `TAXONOMY`.

**But it may not stay in openxFactory.** doc-health is 27,123 lines and is
openxFactory's own gate (`scripts/doc_health/`, self-gating since
`adopt-neutral-tooling-home`, 2026-08-03). If openXdox becomes the home of
"reading a governed corpus", the argument that doc-health should travel with it
is uncomfortably strong — and openxFactory would then consume its own gate at a
pin, exactly as it now consumes the wallet validator. That is a much bigger
change than the ruling asked for, and this document raises it rather than
proposes it.

## The web tier

40 files, 30,410 lines, and it was not measured for this split. From the
promoted requirements the same fault line is visible: the account menu, the
canvas, the editor and chat, the docs tile and the theme controls are app
surface; the wheel, the funnel, the lens regions, the gate console and the drill
-in are lifecycle surface. The front end has no package boundary at all today,
so it will need one invented rather than discovered.

## What contradicts what

Marked as contradiction because this is a brainstorm and this is where it is
legal:

1. **`serve.py` is the boundary AND `serve.py` cannot be split first.** The
   split is only meaningful once the two route families are separated, and the
   file is the most-changed module in the package with five active changes
   touching it. Both statements are true and they conflict on sequencing.
2. **The LOC ratio and the requirement ratio agree, which may be luck.** Of the
   102 promoted requirements, the clusters that read as neutral (doxBench
   surface and editor 17, branch sessions 10, abstracts 8, provider and broker
   6, hosted actor and account 4, knowledge/compression/chat 4) total about 49;
   the governance clusters (gate console and verbs 17, projection/snapshot 8,
   funnel and wheel 7, lens 4) total about 36; projects are 9 and sit on the
   fence. Clusters overlap and the sum is under 102, so treat these as a
   reading of the titles rather than a partition — but roughly half neutral,
   roughly a third governance, matches the LOC cut above closely enough to be
   suspicious of both.
3. **Five active changes make any cut wrong.** `add-nightly-dashboard-refresh`
   (13 open tasks, cross-repo across three repositories, its lane has never
   produced a status artifact), `retire-doxbench-chat-turn-v1` (7 open, schema
   bytes already moved), `add-doxchat-model-intake` (built, not archived),
   `add-composed-view-authoring` and `add-lens-document-selection`. Every one of
   them carries a MODIFIED delta against a 102-requirement spec that would be
   split in two. A cut now strands or re-homes all five; waiting for all five
   means waiting on a lane that has failed three times.
