# Design: split-opendox-two-layer-product

Status: ratified
Ratified by: split-opendox-two-layer-product — 2026-09-05, Brett Heap, "ratify #666" (record `review/ratification-2026-09-05.md`)
Amended: 2026-09-05 — repository shape, by Brett Heap in session, verbatim "elect the shape for both, follow the pin chain, no family yet" (`opensoft/openxFactory`#656 comment `5552614170`); record `review/amendment-2026-09-05-repository-shape.md`. § D12 records the decision; § D8's drafted Amendment 3 text and the R-index below carry it.
Amended: 2026-09-09 — FLOOR PART 2 restated as a source→destination mapping with declared multiplicity, by Brett Heap by click-through in session `openXfactory-4`, verbatim "OQ-K → FLOOR PART 2 restated as a source→destination mapping with declared multiplicity for replicated files (a small amendment PR to the change)" (`opensoft/openxFactory`#656 comment `5609526215`); record `review/amendment-2026-09-09-floor-part-2-mapping.md`. § D6 (2) carries the restated text; RULING OQ-1 is not reopened and the floor still has four parts.

Companion to `proposal.md`. The proposal argues the doctrine, carries the eleven
2026-09-04 acts as LOCKED constraints and names the wave; this document records
the topology, the seam's shape, the three-column assignment, the three domain
mappings the direction demanded, the safety property that replaces byte
identity, the database and tenancy boundary, Amendment 3's drafted text, the
re-homing plan for five active changes, the substrate plan, the risks and the
ordered migration. Every code fact below was measured in the tree at
`origin/main` `a858e5b0` on 2026-09-04, or is cited to the measurement the
staging topic and the brainstorm packet took the same day at `bc1bd4ee`.

## R — the ruled basis, in the order it binds

The full text of all eleven acts is in `proposal.md` § Rulings carried as LOCKED
constraints. This table is the index this document's decisions cite.

| id | time (2026-09-04) | what it fixes | which decisions below rest on it |
| --- | --- | --- | --- |
| founding | issue body | two open-source layers, two repositories, descendants below, per-tenant install | D1, D7, D10 |
| **Q1** | 15:24Z | the database owns identity and coordination; git owns governed artifacts, written back only through the apply lane | D5, D2 (write-back), D9 |
| **Q2** | 15:31Z | FastAPI + Postgres on the `xFactory-Hermes-Install` pattern, OIDC through the Keycloak broker | D7 |
| **Q3** | 15:32Z | one instance and one database per tenant, always, both cases | D7, and the `domain-descendant-boundary` delta |
| **Q4** | 15:34Z | openDox DEFINES the adapter interface, openXdox IMPLEMENTS it, dependency one way | D2, and the `corpus-adapter-seam` capability |
| **Q5** | 15:48Z | the THREE-LAYER TEST; per-module assignment is design work under it | D3, D4 |
| **C1** | 17:46Z | the name collision is accepted knowingly; the repository is `opensoft/openDox` | D8 |
| **C2** | 17:47Z | openXdox is the domain-mapping core, PARAMETERIZED by a domain profile | D1, D3, D4, and `domain-mapping-declaration` |
| **C3** | 17:48Z | standalone openDox creates a plain local git repository per project | D5, D2 |
| **Q6** | 17:49Z | freeze the dashboard now and carve immediately; the five re-home | D9 |
| **Q7** | 17:51Z | `opensoft` owns both; both PUBLIC from day one under Apache-2.0 | D10 |
| **DQ-1** | 22:14Z (`#656` comment `5547049745`) | **`openxFactory` KEEPS its own adapter**; `doc-health` and OpenSpec stay here, a small package beside them implements the seam, `codexDox` is a thin descendant that pins openXdox and reuses it. The fifteen engineering rows stay in `openxFactory`; the shed (§ 5) precedes the first descendant (§ 7) | D1, D3, D3a, D9, and the successor map's third column |
| **OQ-1** | 22:15Z (`#656` comment `5547060378`) | **the FOUR-PART FLOOR**, as a requirement and not a recommendation: mapping manifest + per-file digests + a CLOSED edit-class list (import rewrites, path constants, adapter calls); test counts that SUM — **restated 2026-09-09 by RULING OQ-K as a source→destination MAPPING with declared multiplicity** (`#656` comment `5609526215`), the part unchanged and only its test moved; a neutral conformance corpus; a snapshot-equivalence run | D6 |
| **OQ-2** | 22:16Z (`#656` comment `5547067574`) | **ONE CHAIN** — inside the family openDox is pinned only by openXdox; outside it, openDox is used freely as open source. No third MODIFIED requirement on `neutral-product-pin` | D3a, and the `neutral-product-pin` delta's scope |
| **OQ-3** | 22:21Z (`#656` comment `5547107565`) | **no `document-lifecycle` delta now**; descendants declare lifecycles via `domain-mapping-declaration`; revisit at `MedxDox` | D3a, and the packet's declared-not-modified list |
| **SHAPE** | **2026-09-05** 14:52Z (`#656` comment `5552614170`) | **"elect the shape for both, follow the pin chain, no family yet"** — openDox and openXdox each elect the `openRepoShape` three-repository shape (six repositories, scaffolded, election recorded in `project.yaml`); a descendant's referent is reached through the DECLARED pin chain (`opensoft/openRepoShape`#40); NO family holder is created and the option stays open | **D12**, and D8, D10, D11 as amended |

> Amended 2026-09-05 — repository shape. The column head reads *time
> (2026-09-04)* because every act indexed here was taken that day; the SHAPE row
> above is the first from a later date and carries its own date in the cell. The
> eleven acts and the four `OQ`/`DQ` rulings are unchanged and are not reopened
> — the shape ruling adds a row rather than editing one.

## Context

**What is being cut, measured.** `scripts/ideation_dashboard/` — 48 modules,
49,605 LOC. `web/` — 40 files, 30,410 LOC excluding the vendored
`markdown-it.min.js`. `tests/ideation-dashboard/` — 125 files, 3,927 `def test_`,
**52% of this repository's 7,612 test functions**, plus a four-file
`tests/ideation_dashboard/` underscore spelling. `openspec/specs/ideation-dashboard/spec.md`
— 289,266 bytes, 102 requirements, 472 scenarios, the largest promoted spec in
the corpus (next is `doc-health` at 243,924 B / 43 requirements). Four contract
schemas, 142 packaged examples, five governance docs, **30 archived changes** and
**5 active changes** carrying a delta.

**The coupling, both directions, measured.** OUTBOUND: 12 of 48 modules carry 23
`scripts/doc_health/` import statements — `authoring` (2), `cli` (1),
`completeness` (1), `corpus_root` (1), `doxbench_packet` (1), `gate_console` (4),
`gate_routes` (1), `generator` (3), `round_trip` (1), `serve` (3),
`snapshot_registry` (1), `workbench` (4) — pulling `corpus`, `corpus.RealGit`,
`lines.split_keepends`/`join_rows`, `derive_possibles`, `families.FAMILIES`,
`TAXONOMY`, `DEFAULT_THRESHOLDS`, `staging_seed`, `shared_identity`,
`pin_sentinels`, `ideation_readiness` and `runner.Context`/`run_suite`. INBOUND:
**exactly two statements** — `doc_health/derive_possibles.py:857` and
`doc_health/ideation_readiness.py:1351`, each
`from ideation_dashboard.boundary import OutputBoundary  # lazy: house guard`.
Every other `ideation_dashboard` mention inside `doc_health`
(`corpus.py:193-195`, `lines.py:46-50`, `pin_sentinels.py:56`, `pin_class.py:413`)
is PROSE recording a co-authoritative reading window, not an import. **The
back-edge is ONE class, in ONE 377-line module, imported lazily in two places** —
which is why Q4's neutral module is small, and why the dependency can be made
one-way before any repository exists.

**The three departures from `split-openxwallet-repo`, and their standing.** R3's
seam rule and the one-repository shape are departed from BY RULING (the founding
ruling and C2). The byte-identity floor is departed from BY FORCE: a two-way
import across a proposed repository boundary is a design change before it is a
move. An implementer reading only R3 would keep the reader in `openxFactory`,
which is exactly the wrong place; the proposal states this and this document
restates it because it is the single most misreadable fact in the packet.

**Consumers running an instance today: zero.** codexFactory holds **0** tracked
files under `scripts/ideation_dashboard/` or `tests/ideation-dashboard/` at
`origin/main`, two DRAFT Speckit features (002, 010), and a comment-only doxBench
digest pin in `stack.yaml` stating a verified fact that is false. The wallet
precedent's own trigger has therefore NOT fired, and the rulings commission the
consumer rather than waiting for it. § 7 keeps that honest by making the first
descendant a task with a ruling checkbox.

**Live runtime state.** `openxdox.opensoft.dev` resolves and returns HTTP 401
(auth-gated, live). The QA dispatch minter passed 6/6 readiness on 2026-08-15 and
both readiness results are EXPIRED. `intent-apply.yml` on the aggregation has
**one run, ever** — 2026-08-15T01:22:04Z, success — which Q1 promotes to the only
governed write path. The nightly image-refresh worker has **three runs, zero
successes** and has never produced `refresh-status.json`. The snapshot lane is
green. OpsxFactory declares the four `dox` workloads at
`workflows/aks-administration.yaml:412-431`; the `openxdox` DNS A record exists on
the live zone and is ungoverned.

## Goals

- Fix the shape of everything the proposal names but leaves unspecified: the
  topology, the adapter's operations, the neutral module, the three-column
  assignment, the safety property, the schema boundary, the tenancy shape,
  Amendment 3's text, and each of the five re-homings.
- Break the two-way import FIRST, inside `openxFactory`, before any repository
  exists — the one piece of this arc that is worth doing whether or not the carve
  ever happens. Under RULING DQ-1 it is also where `openxFactory`'s own adapter
  starts: the seam is built here and stays here, and only the PRODUCT leaves.
- Keep every existing gate at today's strength: doc-health still reads a tree,
  OpenSpec still validates packets, the PR checks still gate on refs, and the
  database stays disposable relative to the corpus.
- Leave every contestable reading contestable: the successor map is per-row and
  the three-column assignment names the row that would move under the other
  reading. The four questions this packet put were RULED before ratification
  (§ Questions this document put), so they are now constraints — but the ROWS
  remain contestable one at a time, which is what the ratification read is for.

## Non-goals

- Deciding the per-requirement map by authority. It is a READING and ratification
  is over it.
- Building the model/scenario workbench, the evidence-and-provenance surface or
  the role-and-authority projection. They are named as openXdox's unbuilt centre
  of gravity and they are separate features.
- Any `document-lifecycle`, `doc-health` or `governed-derived-model` delta (§ OQ-3
  and `proposal.md` § Declared NOT modified).
- Resolving codexFactory's false `stack.yaml` digest declaration, or the
  `openxdox` DNS record's ungoverned status, beyond naming them.
- Reserving a contract bundle number.

## Decisions

### D1 — The topology, and the ONE place C2 leaves two lawful readings

```text
opensoft/openDox            the app. Defines the corpus-adapter INTERFACE.
        ^                   Useful ALONE (Q5, C3). Public, Apache-2.0.
        | pins (commit + digest)
opensoft/openXdox           the domain-mapping CORE, parameterized by a domain
        ^                   profile (C2). Implements the interface. Public.
        | pins (commit + digest)
  MedxDox  codexDox  LedgerxDox  AdxDox  OpsxDox
        ^             each: one domain-mapping declaration, deploy config,
        |             branding. Created LAZILY. Visibility follows its domain.
   <tenant> instance       one runtime, one database, always (Q3).
```

The dependency points ONE way at every level (Q4), and there is exactly ONE
pin of openDox inside the family (RULING OQ-2): openXdox pins it, and every
descendant pins openXdox. `openxFactory` consumes the products at pins and is NOT
in this chain as a layer — it is a CONSUMER whose own corpus is one corpus the
adapter can be pointed at, and under RULING DQ-1 it keeps the adapter that points
at it.

**RULED DQ-1 — `openxFactory` KEEPS ITS OWN ADAPTER** (`opensoft/openxFactory`
issue #656, 2026-09-04T22:14Z, comment `5547049745`). RULING C2 had said
engineering vocabulary *"belongs to the engineering descendant `codexDox`, **or**
stays in openxFactory as its own adapter over the corpus-adapter interface"* —
lawful in two ways, and this packet put the choice rather than making it. Brett
took the second: **`doc-health` and OpenSpec stay in `openxFactory`, and a small
adapter package beside them implements the corpus-adapter seam; `codexDox`
becomes a THIN DESCENDANT that pins openXdox and reuses that adapter.**

```text
openxFactory   corpus + governance (doc-health, OpenSpec, document-lifecycle)
               + its OWN engineering adapter, one conformant implementation
               of openDox's seam, with NO privileged route to its home corpus
               (`corpus-adapter-seam` requirement 4 — load-bearing, not
               precautionary, now that the adapter is permanent)
               consumes the products at pins, THROUGH openXdox (RULING OQ-2)
```

**Three consequences, each encoded rather than left to be inferred:**

1. **The fifteen engineering-vocabulary rows STAY IN `openxFactory`.** The
   successor map is **71 openDox / 16 openXdox / 15 openxFactory** — its third
   column was `codexDox` when this packet was first authored and is not any more.
   They still leave the CAPABILITY (`ideation-dashboard` exits whole) and are
   re-promoted here under the adapter's own successor capability, whose id the
   realization authors. `promotion_fidelity.py` keys on (capability, normalized
   title), so the successor is a distinct key and the removal stays visible to the
   checker rather than reading as a requirement that never left.
2. **§ 5 (the shed) PRECEDES § 7 (the first descendant).** Under the rejected
   alternative a descendant had to exist before the carve could complete, which
   collided with `domain-descendant-boundary`'s laziness rule while codexFactory
   holds zero tracked dashboard files. It no longer does: `openxFactory` sheds the
   dashboard on its own account, and `codexDox` follows when a domain has a
   profile.
3. **The R3 departure is NARROWER than this packet first stated, and the earlier
   phrasing is corrected rather than quietly dropped.** "The code that reads the
   corpus leaves entirely" was written before this ruling and is now false: what
   leaves is the PRODUCT. `openxFactory` keeps a reader — a small one, over one
   corpus, through the same interface every other implementation uses.

**Rejected:** `codexDox` owning the adapter and the fifteen rows, with the shed
waiting on the descendant.

**What this does NOT relax.** The adapter `openxFactory` keeps is ONE
implementation among others and gets no private door — no privileged direct call,
no bypass of the interface for the home corpus, no operation a domain
implementation cannot also declare. That rule was authored in
`corpus-adapter-seam` before this ruling and it is what keeps DQ-1 from
collapsing into "the reader never really left": an adapter with a private door is
the same repository it was extracted from, wearing an interface.

### D2 — The corpus-adapter seam: four operations, one neutral module, one way

**Whose standard.** Q4 gives the INTERFACE to openDox. This packet therefore
authors `corpus-adapter-seam` over the terms of consumption — the direction of
the dependency, fail-closed resolution, the governed write path, and no
privileged route for the home corpus — and NOT over the operation signatures.
The sketch below is DESIGN, to be ratified in openDox's own instance:

| operation | what it answers | what it must NOT know |
| --- | --- | --- |
| **list** | which documents a corpus holds, under a declared scope, with a stable identity per document | that `ideation/staging` or `openspec/changes` are meaningful paths |
| **read** | the bytes of one document at a declared revision, plus the revision it was read at | what a `Status:` header is |
| **write back** | a proposed change to one document, dispatched through the corpus's DECLARED governed write path, returning a correlation identifier — never a commit it made itself | that the write path is `intent-apply.yml`, or that a change has a proposal |
| **check** | the corpus's own verdict on a document or a set: findings with a severity and a subject | doc-health's family names, thresholds or taxonomy |

Two derived operations follow from the four and are named so they are not
reinvented per implementation: **classify** (what KIND is this document, and
which fields does its kind require — the operation `authoring.py`'s
`REQUIRED_HEADER_FIELDS` becomes, instead of a constant co-authoritative with
`doc_health.corpus.STATUS_SCAN_LINES`), and **resolve** (given a corpus
reference, which checkout and which revision — the operation `corpus_root.py`
performs today with a path literal).

**The neutral module, and it lands FIRST.** `OutputBoundary` — one class in
`ideation_dashboard/boundary.py`, 377 lines, imported lazily by
`doc_health/derive_possibles.py:857` and `doc_health/ideation_readiness.py:1351`
— moves to a small module BOTH sides import. It stays INSIDE `openxFactory` when
it lands (`tasks.md` § 2.1) and travels to openDox with the carve. This is the
smallest change in the arc and the only one that is unconditionally correct:
nothing else can start while the two packages import each other, and the
relocation pays for itself if the carve never happens.

**The 23 outbound imports are NOT a dependency to remove.** Under Q4 they become
the adapter's openXdox-side IMPLEMENTATION SURFACE — code that legitimately
imports doc-health, in the repository where importing doc-health is lawful. What
must not survive is the direction, not the calls.

**`serve.py` is the boundary and it cannot be split last.** 6,733 lines carrying
the app server AND the corpus server in one file, with three `doc_health`
imports, and five active changes touching the package. openDox keeps the server,
static and canvas routes, chat and model routes and `/capabilities`; openXdox
CONTRIBUTES snapshot, `/source` and projection routes through an EXTENSION POINT
openDox exposes. Without the extension point the integration layer forks the
server, which is a fork rather than a profile and breaks the same rule
`domain-descendant-boundary` applies one level down. `cli.py` (2,456) splits the
same way, with openXdox contributing subcommands.

### D3 — The three-column assignment, and every row that moves under the other reading

**The test (Q5).** For each module and each requirement: would someone with no
notion of factories, gates or tenants use it (openDox)? is it the machinery
COMMON to how Medx, Ledgerx and Adx map onto the workbench (openXdox)? or is it
one domain's own mapping (a descendant)?

**The 48 modules.** LOC measured; **PULL UP** marks a module Q5 asks to move up.

*openDox — the app a student or a lab assistant would use (~24.9K):*
editing and canvas — `doxbench_turns` 1,857 · `doxbench_threads` 1,417 ·
`doxbench_model` 1,343 · `canvas_drafts` 221 · `doxbench_hash` 112; research and
analysis — `doxbench_knowledge` 1,231 (**PULL UP**) · `doxbench_abstract_store`
446 (**PULL UP**) plus the abstract-generation surface inside `doxbench_turns`;
model plane — `doxbench_bridge` 1,605 · `doxbench_provider` 906 ·
`doxbench_intake` 736 · `doxbench_binding` 557 · `doxbench_mcp` 567 ·
`doxbench_memory_gateway` 608 · `doxbench_telemetry` 380; git and sessions —
`branch_session` 5,290 · `session_git` 1,199 · `session_pr` 443; identity and app
plumbing — `actor_identity` 304 · `boundary` 377 (its `OutputBoundary` is D2's
neutral module) · `action_errors` 45 · `fixtures` 101 · `doxbench_install` 339 ·
`__init__` 18; NotebookLM — `notebook_action` 239 (**PULL UP**); set-building —
the keyword-query half of `lens` 282 (**PULL UP**).

*openXdox — the machinery common to the three mappings (~10.9K, plus what does
not exist yet):* adapter implementation and projection mechanism — `corpus_root`
101 · `generator` 912 · `snapshot` 223 · `snapshot_registry` 1,318 · `register`
185 · `completeness` 543 · `round_trip` 370; the gate and commission loop —
`gate_console` 2,207 · `gate_routes` 3,552 · `kickoff` 1,006 · `record_binding`
259 · `register_edit_lane` 337; scope and ownership authority — `doxbench_scope`
841.

*`openxFactory`'s OWN ENGINEERING ADAPTER — the engineering mapping, which under
RULING DQ-1 stays HERE rather than moving to `codexDox` (~5.0K):*
`doxbench_packet` 1,375 · `doxbench_contracts` 780 · `human_seen` 476 ·
`nightly_lane` 589 · `dashboard_refresh_lane` 2,071 · `intent_apply_lane` 744.
The three lanes are the clearest engineering-mapping content in the package:
their whole subject is thawing `openxFactory`'s git corpus into a served
snapshot, one of them has never succeeded, and RULING Q1 makes the apply lane a
permanent fixture of the `openxFactory` mapping specifically. Under the ruling
they never leave the repository they read — which is also why the shed can happen
before any descendant exists.

*The residue that splits BY FUNCTION (10.9K, and this is the real work):*
`serve.py` 6,733 · `cli.py` 2,456 · `workbench.py` 1,575 (reference-set manifests
and scratch notebooks are openDox; what a reference set MEANS in a promotion
funnel is above; four `doc_health` imports) · `authoring.py` 329 (header
authoring is openDox; its required-field vocabulary comes from the adapter's
CLASSIFY operation).

24.9K + 10.9K + 5.0K + 10.9K against a measured 49.6K. **Treat the split as three
columns plus a seam, not four buckets.**

**The 102 requirements, by cluster.** Clusters overlap and the sum is under 102,
so this is a reading. Full per-requirement rows are the REMOVED delta itself.

| cluster | openDox | openXdox | openxFactory's adapter |
| --- | --- | --- | --- |
| doxBench surface and editor (17) | **yes** | | |
| branch sessions (10) | **yes** | the commit-per-gate-act row | the proposal-state row |
| abstracts (8) | **yes — PULL UP** | | |
| provider and broker (6) | **yes** | | |
| hosted actor and account (4) | **yes** | | |
| knowledge / compression / chat (4) | **yes — PULL UP** | | |
| projects (9) | **yes** | the tenant-catalog authority row | |
| lens (4) | the set-builder | the gate verbs | the candidate-register row |
| gate console and verbs (17) | | the LOOP | the verb vocabulary |
| projection and snapshot (8) | | the MECHANISM | the status vocabulary |
| funnel and wheel (7) | | the SHAPE | the stage names |

Totals: **71 openDox, 16 openXdox, 15 `openxFactory`** — the third column being
this repository's own adapter under RULING DQ-1, not a descendant. The LOC ratio
and the requirement ratio agree closely enough to be suspicious of both readings,
and the packet says so rather than presenting the agreement as corroboration.

**The pull-ups, ranked by value to a lab assistant who has never heard of a
factory.** (1) The knowledge and compression stack — assembling a bounded context
packet over a set of documents you selected, with declared fidelity, is the core
research move, and it is filed as governance ONLY because its input set is named
"the staged set". (2) Abstracts — deterministic abstracts that state their own
absences, plus a separately invoked model-derived distilled abstract verified
against the document's declared fields, cached by path-digest-model: a
literature-review tool living in a governance dashboard. (3) The lens
set-builder — naming an intensional set the machine clustering missed is how a
human organizes twenty papers. (4) The NotebookLM connection — named explicitly
by the direction, 239 lines; what must NOT come up is the stage-to-book mapping,
because a per-project book is the neutral shape. (5) The editor and chat bound to
the active buffer — the surface the other four are used through.
**Deliberately NOT pulled up:** Adx's `calibrated`-tier calibration loop (domain
machinery, and openDox has no outcome to read) and the gate console (a student
has nobody to gate against).

**The web tier is where a student-usable openDox is won or lost, and it was not
measured for this split.** 40 files, 30,410 lines, and NO package boundary at all
today — so its boundary must be INVENTED rather than discovered. The same three
columns are visible from the promoted requirements (account menu, canvas, editor,
chat, docs tile and theme controls are openDox; gate console and drill-in are the
gate loop; wheel, funnel and lens regions carry stage names that are one domain's
mapping), and `tasks.md` § 3.4 makes the front-end boundary its own task rather
than a consequence of the Python one.

### D3a — What RULING OQ-2 and RULING OQ-3 settle, and what each one does NOT

**RULED OQ-2 — ONE CHAIN** (`#656`, 2026-09-04T22:16Z, comment `5547067574`).
*"Inside the xFactory family there is ONE chain: openDox is pinned only by
openXdox, and every domain descendant pins openXdox."* The mapping core is never
bypassed, and there is one consumption shape to validate rather than two.

- **What it does NOT do:** it does not make openDox a closed product.
  *"Anyone outside the family uses openDox freely as open source — this ruling
  governs the pin chain only."* RULING Q7's public-from-day-one posture and
  DIRECTION Q5's standalone student are untouched, and RULING C3's plain local git
  repository per project is exactly that use. What the ruling forbids is a
  GOVERNED consumer inside this family reaching past the mapping core.
- **What it changes in the packet:** the recommendation this packet carried — a
  one-field "which layer do you pin" declaration added to
  `domain-descendant-boundary`'s pin requirement — is NOT taken, and the ruling
  says so in terms: *"No third MODIFIED requirement is added to
  `neutral-product-pin`."* This packet therefore modifies exactly TWO of that
  capability's nine promoted requirements, and the CHAIN clause it does add — each
  level declares only its DIRECT upstream, a transitive commit is derived and
  never a second authority — is the whole of what one chain needs. Recorded here
  so a later reader does not re-derive the declaration as an oversight.
- **Rejected:** a direct pin for docs-only installs; deferring to the first
  request.

**RULED OQ-3 — NO `document-lifecycle` DELTA NOW** (`#656`, 2026-09-04T22:21Z,
comment `5547107565`). `document-lifecycle` stays `openxFactory`'s governance
vocabulary, **exposed through its own adapter** — which is RULING DQ-1's adapter,
so the two rulings compose: the taxonomy does not need parameterizing because the
repository that owns it also owns the reader that reads it. Descendants declare
their own lifecycles via the `domain-mapping-declaration` capability this change
ADDS, and that capability's second requirement is where the parameterization
actually lives.

- **The revisit trigger is named, not open-ended:** the first non-engineering
  descendant, `MedxDox`, showing what a clinical lifecycle needs.
- **Rejected:** parameterizing in this change — *"a third writer on a spec two
  active changes hold"*, which is the collision this packet was already avoiding —
  and filing a named successor change now.

### D4 — The three domain mappings, worked, and the seven machineries they share

Q5(b) requires the common core to be EXTRACTED from three mappings rather than
asserted from one. Sources: `docs/domain-instantiation-pre-run-questionnaire.md`,
`contracts/policies/layer-vocabulary.yaml`, `docs/governed-derived-model.md`.

| | MedxFactory | LedgerxFactory | AdxFactory | codexFactory |
| --- | --- | --- | --- | --- |
| subject layer | Patient Hermes | Engagement Hermes | Advertiser Hermes | Project Hermes |
| tenant layer | Care Organization Hermes | Firm Hermes | Marketing Organization Hermes | Engineering Organization Hermes |
| domain objects | patient and care context | ledger, filing, report, transaction, obligation | campaign, audience, offer, channel, account | feature, repo, PR, release, incident |
| sensitive acts | care-affecting action, patient privacy, clinical authority | money movement, filing accuracy, audit, compliance | brand risk, external send, paid spend, privacy, attribution | merge, deploy, data exposure, production impact |
| derived-model family | Dream Object / Simulation Scenario — RATIFIED templates, `governed` | Counterparty Health Profile / Financial Scenario — staged | Persona / Campaign Simulation — `calibrated` | — |
| truth store the model may never write | the patient truth model | the ledger | brand truth | the repository |
| external enforcement | the clinical chart (openChart via MedxChart) | the ledger | the ad platform | branch protection |
| lifecycle, in the domain's own words | drafted → attested → filed → immutable-with-addenda | raised → researched → concluded → professionally reviewed → filed | drafted → brand-reviewed → spend-approved → launched → measured → retired | brainstorm → staged → ratified → archived |
| promoting authority | clinician of record; board for protocols | licensed professional; SoD/budget authority | launch and spend approver | operator authority |

**THE SEVEN MACHINERIES COMMON TO ALL THREE — this is the extraction Q5(b) asked
for, and it is openXdox's content.** (1) The corpus-adapter IMPLEMENTATION —
chart, firm document store, campaign repository: listed, read, written back and
checked. (2) The LIFECYCLE ENGINE — a controlled status vocabulary, legal
transitions, the authority each requires, and the point of
immutability-with-addenda; all three have one and only the WORDS differ, which is
the signature of something that should be data rather than code. (3) The
GATE-AND-COMMISSION LOOP — `workflow-gate-contract` plus the `workflow-job`
descriptor and the gate-action record; the dashboard's gate console is the only
UI for it that exists anywhere. (4) The EVIDENCE-AND-PROVENANCE SURFACE — a chart
citation, a ledger tie-out and an attribution chain are ONE machinery over
different nouns; `governed-derived-model` invariant 2 is the contract and nothing
renders it. (5) The MODEL/SCENARIO WORKBENCH — a `model` member and an optional
`scenario` member, a declared scope and isolation boundary, a truth store the
model may never write, output confined to
`hypothesis_proposed | no_signal | discarded`, and a named human promoting
authority. **It exists nowhere in the 80,000 lines and it is openXdox's centre of
gravity** — which changes the character of the work from "carve" to "carve and
build". (6) The ROLE-AND-AUTHORITY PROJECTION — clinician of record, licensed
professional, launch approver; the contracts exist and the workbench shows only a
per-serve console token and a loopback verdict. (7) The REVIEW LANE — a named
reviewer, a recorded verdict, and a merge that cannot clear without it;
codexFactory has the only realized instance and every domain needs one.

**Explicitly NOT common, and therefore not openXdox's:** reading
`ideation/staging/`, parsing `## ADDED Requirements`, running doc-health's check
families, and rendering the OpenSpec promotion funnel. RULING C2 is what makes
that list binding rather than an opinion.

**Research analysis is where the test bites hardest, in a good way.** A lab
assistant reading twenty papers, clustering them, summarizing them, keeping a
notebook and drafting a protocol is MedxFactory's OWN RESEARCH HALF with no
domain machinery at all — the strongest confirmation that "a student could use
openDox" is not a concession to hypothetical users but half of a real domain's
mapping.

**The domain profile is the artifact.** `domain-mapping-declaration`'s five axes
(artifact kinds; lifecycle vocabulary with transitions, authorities and the
immutability point; acts and their gates; evidence classes; promoting
authorities) are exactly the columns of the table above that differ per domain.
That is what a `<Domainx>Dox` descendant CONTAINS, and it is what gives "pin and
profile, never fork" something concrete to mean one level down.

### D5 — The database boundary: identity and coordination, and nothing else

**RULING Q1, restated as a boundary.** IN the openDox database: users, accounts
and memberships; projects; the project-to-repository mapping; sessions; unsaved
drafts. NOT in the database, ever: specs, changes, ideation documents, contracts
— read from repositories and written back ONLY through the apply lane. The
database is DISPOSABLE relative to the corpus: lose it and you lose coordination
state, not a governed artifact.

**Why this keeps every gate valid.** doc-health still reads a tree; OpenSpec still
validates packets; the PR checks still gate on refs; `governed-derived-model` and
`workflow-gate-contract` still have the reviewable artifact they assume; branch
protection, merge-gate floors and required checks still see the diff they act on.
An artifact whose gate verdict cannot be read by a required check on a pull
request is not enforced, it is advertised — and Q1 is what keeps that from
happening.

**The one genuinely new object is the USER, and it inverts a promoted rule.** Two
current requirements say in terms that the dashboard authorizes nothing on the
hosted actor and that identity presence changes no capability verdict — write
authority today is a property of WHERE the request came from (a loopback console
verdict), not WHO sent it. Q1 and Q2 together invert that: an account is a durable
row, authentication delegates to the Keycloak broker, and authorization stops
being a property of the request's origin. **This is the largest conceptual change
in the rulings and the easiest to under-read**, which is why the successor map's
row for *The dashboard authorizes nothing on the hosted actor* is marked
SUPERSEDED IN SUBSTANCE and RE-AUTHORED rather than promoted unchanged.

**C3 makes the standalone case real, and it is the same code path.** A student's
project is a PLAIN LOCAL GIT REPOSITORY openDox creates and manages: documents
are always git-backed, commits are the write path, a remote can be attached
later. That is the trivial conformant implementation of the adapter's write-back
operation — a corpus whose declared governed write path is "commit to this local
repository" — so the standalone case is not a mode, it is one adapter
implementation. Moving a project into a governed factory is a PUSH, not a
migration.

**The origin complaint's remaining half.** Q1 answers *"no good place to store my
projects"* with its COORDINATION half — projects, members and the
project-to-repository map live in a database every tenant install has — while the
specs still land in a repository. So **openDox must be able to CREATE that
repository as a first-class act**, or the complaint returns one level down.
Nothing in the rulings says who creates it; `tasks.md` § 3.6 makes it an
openDox-side task rather than leaving it implied.

**The residual nobody ruled.** The hybrid where ideas live in the database until
promoted was REJECTED, so an idea is a governed document in git from its first
save — consistent, and heavier than a lab assistant may want. Whether openDox
needs a pre-governed scratch space that is NOT "a draft of a document" is a real
residual, it is not one of the open questions, and it is recorded here rather
than resolved.

### D6 — What replaces byte identity: the RULED four-part floor, plus the map

The wallet floor was *"a move whose diff is not provably empty cannot be bisected
against"*. Unavailable here. **RULED OQ-1** (`#656`, 2026-09-04T22:15Z, comment
`5547060378`): the replacement is **the four-part floor**, and it is a
REQUIREMENT of this change rather than a recommendation in it. Each part has its
own evidence line and **none of them is "the tests passed"**. Brett rejected both
single-instrument alternatives on the record, and the reasons are the reason the
floor has four parts: **manifest-with-digests only** *"proves files moved, not
behaviour"*; **snapshot-equivalence only** lets *"a dropped module without test
coverage go unnoticed"*.

**(1) THE MAPPING MANIFEST — a source→destination row per moved file, with a
per-file digest at the cut and a CLOSED edit-class list.** Before any file moves,
the carve emits `docs/opendox-carve-manifest.yaml` in `openxFactory` naming, for
every file under the moved paths: its `openxFactory` path, its `sha256` at the
NAMED CARVE COMMIT, its destination repository, its destination path, and one of
exactly three dispositions — `moved_verbatim` (bytes identical at the
destination), `moved_with_declared_edit`, or `not_moved` (with the reason).
**THE EDIT-CLASS LIST IS CLOSED AND IS THE RULING'S OWN, VERBATIM: `import
rewrites`, `path constants`, `adapter calls`.** Three classes, not four — the
packet had proposed a fourth ("vocabulary parameterization") and the ruling does
not carry it, so a parameterization edit is either expressible as one of the
three or it is not a carve edit at all and belongs to a later change. **A file in
no row, or an edit in no class, is an UNDECLARED MOVEMENT and the carve
REFUSES.** This is the closest available analogue to a provable empty diff for a
move that cannot be empty: it does not prove the bytes did not change, it proves
**every changed byte is inside a declared class** and every file has exactly one
destination.

**Note the third class is why the fifteen `openxFactory` rows are cheap.** Under
RULING DQ-1 they do not move repository at all; the only edit they take is
re-expressing the reader's path literals as `adapter calls` — one of the three,
by name.

**(2) A SOURCE→DESTINATION TEST MAPPING WITH DECLARED MULTIPLICITY.** Every file
in the carve manifest's declared surface that carries at least one `def test_`
maps to the destination or destinations its OWN ROW names, and that mapping — not
a scalar equality — is the floor. Four clauses:

**(a) TOTAL COVERAGE — no test is lost.** Every source file carrying tests has at
least ONE post-split home. A file with tests and no home is a LOST TEST and the
carve REFUSES. This is the intent the ratified text was reaching for, stated
directly instead of inferred from an arithmetic identity.

**(b) DECLARED MULTIPLICITY.** A row dispositioned
`not_moved / replicated_at_destination` DECLARES the set of repositories its
replica lands in, INCLUDING the retained `openxFactory` copy; its multiplicity
`m` is that set's size. Multiplicity is declared IN THE ROW and never inferred at
arrival: an undeclared replica set makes the check uncomputable, which is a
refusal and not a pass. This is one obligation on FLOOR PART 1, carried at
`tasks.md` § 5.4a as the input part 2 reads — the manifest edit lands in its own
pull request, not in this amendment.

**(c) THE SUM CHECK, OVER DECLARED MULTIPLICITIES.** Collected `def test_` at
openDox plus openXdox plus whatever remains in `openxFactory` (which under RULING
DQ-1 includes the adapter's own tests, and the retained replicas)

> Σ(destinations) = source_count + Σ over replicated rows of (m − 1) × row_test_count

with every term read from the manifest at the carve commit. Measured against the
LANDED manifest (PR #865) at `carve_commit b075fd91`: source 4,411 across 146
`.py` rows; destinations 1,128 + 2,345 + 998 = 4,471; three replicated test
modules carrying 30 `def test_` at `m = 3` each; `4,471 = 4,411 + 60`. ✔

**(d) PINNED BY TEST** at each destination and in `openxFactory`, the way
`pytest-suite.yml` already pins this repository's collection triple.

This still catches the most likely way a large suite loses coverage in a carve —
tests dropped silently rather than moved, the part whose absence Brett named when
he rejected snapshot-equivalence alone — and it no longer punishes the replicas
§ 3.7 requires.

> Amended 2026-09-09. This first read *"TEST COUNTS THAT MUST SUM ACROSS THE
> THREE REPOSITORIES. 3,927 `def test_` across 125 files — 52% of this
> repository's 7,612. Post-split collection counts … SHALL SUM to the pre-split
> count"*. RULING OQ-K (`#656` comment `5609526215`, 2026-09-09T22:19:57Z, record
> `review/amendment-2026-09-09-floor-part-2-mapping.md`) restates it, because the
> equality is false twice. It is false BY DESIGN: the landed manifest's 18
> `replicated_at_destination` rows include three test modules carrying 30
> `def test_`, and § 3.7 requires EVERY destination to pass the conformance
> corpus, so those 30 have three homes each and the post-split sum exceeds the
> pre-split count by exactly 60 on its first run — an equality that would be
> "fixed" by deleting replicas, breaking FLOOR PART 3 to satisfy FLOOR PART 2.
> And it is false by STALENESS: `3,927 / 125 / 7,612` were measured at
> `a858e5b0` on 2026-09-04; at `carve_commit b075fd91`
> `tests/ideation-dashboard/` alone holds 4,169 `def test_` across 140 `.py`
> files and the repository holds 8,731. A scalar in a ratified document is
> re-falsified by every merge; a mapping over the manifest is re-evaluated from
> the manifest. RULING OQ-1 is NOT reopened — four parts, part 2 still about
> tests, both rejected single-instrument alternatives still rejected; only part
> 2's TEST moved.

**(3) A NEUTRAL CONFORMANCE CORPUS EVERY DESTINATION PASSES**, on the wallet
extraction's own pattern of positives plus negative confirmations — a corpus with
no `openspec/`, no `contracts/`, no lifecycle headers. The ruling says *"every
destination"*, so it is not openDox's alone: openXdox's adapter implementation
and `openxFactory`'s own adapter run it too, which is the only mechanical proof
that `corpus-adapter-seam`'s no-privileged-route requirement holds for the home
corpus. This is also what makes openDox verifiable independently rather than only
against this repository, which Q5's standalone test requires anyway.

**(4) A SNAPSHOT-EQUIVALENCE RUN** proving the new stack renders the SAME
dashboard snapshot as the old: the same corpus served by the pre-split tree and by
the post-split stack produces the same snapshot digests. For a system whose output
is a projection, this is the closest analogue to "the diff is provably empty".

**The cost is that all four must exist before the carve, which is the point.**
And the SPECIFICATION-side floor is the per-requirement successor map itself:
instead of proving the bytes did not change, prove every requirement has exactly
one home.

**WHY NO PROMOTED REQUIREMENT IS AUTHORED FOR THE FLOOR, stated so the omission
is a decision and not a gap.** The floor is RULED and it binds this change; it is
not a general rule about extractions, and the capability that would host one —
`release-realization`'s archive gate — is held by TWO active changes
(`add-sequenced-after-substrate`, `add-structured-scope-substrate`), so a third
writer would be exactly the collision this packet spends its delta preamble
avoiding. It binds instead as an obligation of this change: named here, carried as
build tasks at `tasks.md` § 3.1, § 3.7, § 5.4 and § 5.5, and gating the archive at
§ 8.2 with one evidence line per part. If a later extraction wants it as doctrine,
that is that change's ADDED requirement to author.

### D7 — Install and tenancy: the Hermes pattern, one instance per tenant, two Apps

**The shape openDox copies (Q2).** `xFactory-Hermes-Install` runs FastAPI +
Postgres on AKS serving two hosts, with `migrations/` (ordered SQL, `0001` pinned
canonical plus additive), per-client instance trees under `config/clients/<client>/`
validated by `openxFactory`'s validator from a pinned checkout, `deploy/compose/`
for single-node and `deploy/kubernetes/` for AKS, and one lifecycle CLI with 20
verbs. Its README states the discipline worth copying verbatim: layer contracts
are owned by `openxFactory` and *"this repo only installs and configures the
runtime that implements them."*

**The tenancy shape (Q3).** One instance and one database per tenant, ALWAYS, in
both cases — Case A, Opensoft operates it under the operator vault; Case B, the
tenant operates it under its own provider. Brett said *"its own db"*, not "its own
schema" or "its own rows": the boundary is PHYSICAL, not a row filter. The bill
is N deployments, N databases, N migration runs per release, N backup-and-restore
policies and N credential sets — which is exactly why the modified
`domain-descendant-boundary` requires the operating cost to be DECLARED at
descendant creation.

**The two GitHub Apps stay two, and that is a SECURITY INVARIANT** — folded from
the `openxdox-install-app-provisioning` staged topic (staged 2026-08-14, gate met
2026-08-15, exit unraised). The exposed inbox must NEVER hold a
contents-write-capable key, so the DISPATCH App and the CONTENT App are separate
least-privilege bindings. GitHub has no app-creates-app API, so the **App Manifest
flow** is the mechanism: the installer ships a manifest with permissions
pre-filled, the tenant names and confirms, GitHub creates the App IN THE TENANT'S
ORG — which is the structural form of tenant sovereignty — and credentials are
captured within the hour. App names are globally unique, hence the convention
`openXdox — <tenant>`. Q3 STRENGTHENS all of it: the manifest flow now runs once
per tenant by construction. And RULING Q1 settles what that topic left open —
**the dispatch App does NOT become moot**, because git remains authoritative for
governed content and the credential-free serving tier still must not hold a
contents-write key.

**What `domain-descendant-boundary` must grow, and why nothing existing covers
it.** Every descendant the standard was written for — `MedxAvatar`, `MedxChart`,
`MedxPractice`, `LedgerxWallet` — is a CONTRACT-FAMILY descendant: YAML profiles
over pinned YAML contracts, where a fork is a diff and the pin's digests detect
it. A descendant of a product with a SCHEMA is different in kind: a database
diverges silently and only at the next upgrade, so an extra `ALTER TABLE` that has
already run is invisible to every digest. Hence the two MODIFIED requirements: the
migration set is PINNED CONTENT, domain fields go through a DECLARED EXTENSION
POINT, and a descendant-authored migration is a fork of the schema. And hence the
second: a committed TENANT INSTALL is a profile artifact, which is what reconciles
Q3's commissioned descendants with the standard's own laziness rule — the two
looked like they disagreed and they do not, once "which fact discharges the gate"
is stated for a runtime product.

**The folded predecessors.** `ideation/staging/openxdox-install-app-provisioning/`
STAYS staged and is not deleted or rewritten by this packet; it is named as a
predecessor and its five open questions are either carried here (its Q1, the
contract home, is answered by this change, because a per-tenant install
provisions a DATABASE as well as two Apps) or explicitly left staged.
**codexFactory issue #89** ("Plan openXdox standalone project migration", open
since 2026-08-25) is FOLDED, not duplicated — its obligations list reads as a
checklist for this realization (preserve stable project, repository, subject and
work-item identities; re-parent openXdox out of xFactory; update repository and
submodule topology; update dashboard projections and project-register
relationships; migrate policy, ownership and governance bindings; record a
complete audit trail and a rollback plan) and it stays open as codexFactory's own
record of the migration operation. Its topology diagram predates the two-layer
ruling and needs a third level; and RULING Q1 changes its subject, since the
project register itself becomes database-held coordination state.

### D8 — Amendment 3, drafted here and APPLIED AT REALIZATION

`docs/openxdox-naming.md` is `Status: ratified` (LOCKED 2026-08-13) and rejected
`openDox` as "the taken name", building the `openX` + `dox` argument on the
rejection: *"the splitting `X` distinguishes it from the taken name `openDox`."*
RULING C1 overrides that. Because the record is `ratified`, the correction is an
AMENDMENT — the discipline `split-openxwallet-repo` used for Amendment 2 — and it
travels with the act it describes. **The text below is DRAFTED, NOT APPLIED;
`tasks.md` § 1.6 applies it in the pull request that creates the repository.**

> Amended 2026-09-05 — repository shape. The drafted text below now carries the
> SIX repository names and the election, because the ruling of
> 2026-09-05T14:52Z made each layer a three-repository project. The amendment is
> still DRAFTED and still applied at § 1.6; only its content grew. `openXdox`'s
> own name, its lowercase wire label, its `dox` handle, its host and
> `openXdox-Install` are all unchanged by it.

> ## Amendment 3 — `openDox` is taken knowingly (2026-<MM>-<DD>)
>
> **The core is the `opensoft/openDox` PROJECT, and the collision is accepted
> rather than absent.** Brett's ruling of 2026-09-04 (RULING C1 on
> `opensoft/openxFactory` issue #656, 17:46Z), taken because the
> document-and-ideation workbench becomes two open-source layers and the neutral
> core needs the neutral name.
>
> **The facts, as measured on 2026-09-04 rather than asserted.** A GitHub
> ORGANIZATION named `opendox` EXISTS — created 2026-03-20, holding one public
> repository `opendox/dox` ("Rethinking Amazon Product Performance
> Intelligence", 357 KB, last pushed 2026-05-31) on an unrelated subject. GitHub
> search returns SIX repositories named `opendox`: `noitran/opendox` (22 stars, a
> Laravel/Lumen OpenAPI package, last pushed 2022-02-10 — the largest and
> dormant), `fum4/opendox` (0 stars, pushed 2026-07-16, "Spec + CLI + skill for
> agent-written repo docs" — an ACTIVE 2026 project in the ADJACENT
> agent-written-docs space), `dibinraj2003/opendox` (0 stars, 2026-08-10),
> `andymadson/opendox` (1 star, 2025-08-27), `mfbmina/opendox` (2023-01-04) and
> `ritskush1/opendox` (2017-05-22). GitHub namespaces repositories PER OWNER, so
> none of these blocks `opensoft/openDox`; the ORGANIZATION name is unavailable
> and **no claim is made on it**. The brand lives under `opensoft`.
>
> **What is accepted.** The adjacent-subject overlap with `fum4/opendox` is known
> and accepted; which specific abandoned repository originally prompted the word
> "dead" is immaterial to this record. `openXnotes` stays documented as the
> considered alternative and remains unused.
>
> **The record above is amended rather than rewritten.** The sentence "the
> splitting `X` distinguishes it from the taken name `openDox`" was written on
> 2026-08-13 against a one-word claim that nobody had measured; the measurement
> is above and the distinction it drew is now a deliberate two-layer
> relationship rather than an avoidance. `openXdox` keeps its name, its
> lowercase wire label, its `dox` handle and its host; what changed is that the
> neutral layer below it is now also named.
>
> **SIX REPOSITORY NAMES, AND THE ELECTION THAT PRODUCED THEM.** Brett's ruling
> of 2026-09-05T14:52Z (`opensoft/openxFactory` issue #656, comment
> `5552614170`), verbatim *"elect the shape for both, follow the pin chain, no
> family yet"*, ELECTS the `openRepoShape` three-repository shape for both
> layers. The names this record registers are therefore six:
> `openDox`, `openDox-spec`, `openDox-code`, `openXdox`, `openXdox-spec` and
> `openXdox-code`. The election is recorded where the doctrine says it lives —
> each assembly root's `project.yaml`, `elected_by: Brett Heap`,
> `elected_on: 2026-09-05`, `reference: openxFactory docs/project-repo-schema.md` — and this
> record only registers the NAMES.
>
> **The leg suffixes are not new brands.** `-spec` and `-code` are lowercase and
> hyphenated precisely so they sit in a different naming family from every
> CamelCase product name this record governs: `openDox-code` is a LEG of the
> openDox project, not a product called "openDox-code", and the `openX` + `dox`
> reasoning above does not apply to it. **Electing the shape confers nothing** —
> no gate, no floor, no grant, no authority — so nothing else in this record
> moves with it. `openXdox-Install` keeps its own form and its own rule: it is
> an INSTALL name, not a leg, and it is still registered with no repository
> created.
>
> **The descendant spelling is unaffected.** The transcript spells the
> descendants `medXdox` and `CodeXdox`; the ratified `<Domainx><Product>` form
> governs, so they are `MedxDox`, `codexDox`, `LedgerxDox`, `AdxDox` and
> `OpsxDox` — registered as NAMES here with no repository created, on the same
> rule that registered `openXwallet-Install`. A descendant scaffolded the same
> way carries the same two legs, so its leg names are registered beside it —
> `codexDox-spec`, `codexDox-code`, `MedxDox-spec`, `MedxDox-code`, and so on
> for `LedgerxDox`, `AdxDox` and `OpsxDox` — and, again, no repository is
> created for any of them.

**The contradiction the record has carried since before the ruling, and it is
worth stating in the amendment's own paragraph:** the promoted `ideation-dashboard`
requirement *The openDox project-first header* already says the header "SHALL
brand as 'Opensoft openDox'". So the naming record rejected `openDox` as taken
while a promoted requirement was already shipping it as the product name. The
ruling REGULARIZES an existing name rather than introducing one.

### D9 — Re-homing the five frozen changes (RULING Q6), one by one

Q6: the five stop where they stand; their live deltas and open tasks re-home.
For each, the destination, what happens to its delta, and the bookkeeping.

| change | standing | delta on `ideation-dashboard` | destination | disposition |
| --- | --- | --- | --- | --- |
| **`add-nightly-dashboard-refresh`** | ratified 2026-08-25, re-ratified 2026-09-04; archive gate OPEN, **13 open tasks**; cross-repo across three repositories | 1 ADDED + 1 MODIFIED (*Runtime snapshot fetch…*), **plus 7 ADDED on `doc-health`** | **openXdox** (the refresh lane is projection-mechanism work) with the aggregation-side worker staying in the aggregation | CLOSED as re-homed. Its 7 `doc-health` requirements do NOT travel: they were authored on the dashboard's behalf, and Q4 points that dependency one way — the refresh lane in openXdox reads the corpus through the adapter, so the requirements are re-authored against the adapter IN openXdox rather than added to `openxFactory`'s `doc-health`. **This is the one genuine conflict Q6 names, and this is its resolution.** |
| **`retire-doxbench-chat-turn-v1`** | ratified 2026-09-01; archive gate OPEN, **7 open tasks**; schema bytes ALREADY MOVED at `contract-v3.0` | 2 ADDED + 1 MODIFIED (*The chat-turn contract release…*) | **openDox** (the chat-turn envelope travels with the app) | **NOT simply closed — it is the one that CANNOT be.** Its schema removal is already realized in `openxFactory` bytes and its `contract-v3.0` tag is published, so its remaining 7 tasks are `openxFactory` bookkeeping that must complete HERE. It archives in `openxFactory` on its own evidence, and only its FORWARD half (the surviving `-v2` family's requirements) re-homes to openDox. § 6.2 sequences it BEFORE this change's archive. |
| **`add-doxchat-model-intake`** | ratified, built 2026-08-26, NOT archived; `target_release: contract-v1.45` | 1 MODIFIED (*doxBench model catalog…*) + 4 ADDED | **openDox** (the model plane) | CLOSED as re-homed; its built code moves with the carve as `moved_with_declared_edit` rows in the manifest, and its four ADDED requirements are re-authored in openDox. Its one additive schema enum member is already `openxFactory` contract bytes and stays. |
| **`add-composed-view-authoring`** | ratified; `target_release: none` | 1 MODIFIED (*Composed views are read-only…*) | **openDox** (projects and composed views) | CLOSED as re-homed. No contract bytes, no release identity — the cheapest of the five. |
| **`add-lens-document-selection`** | ratified; `target_release: none` | 5 ADDED | **openDox** (the set-builder half) — EXCEPT its `doc_health.staging_seed` drafter and route, which stays in `openxFactory`'s own adapter under RULING DQ-1 | CLOSED as re-homed, SPLIT across two destinations, which is why it is listed last: it is the only one of the five whose content does not land in one place. |

**`add-ideation-intent-plane` — ratified 2026-07-23, part-realized, and its
capability `ideation-intent-plane` is ABSENT from `openspec/specs/` for 43 days.**
It is NOT one of the five and it is NOT re-homed: RULING Q1 makes its apply lane
the ONLY governed write path, so it stays `openxFactory`'s and its capability
must reach canon. **A capability that is ratified and absent from canon cannot be
assigned a successor home**, which is why `tasks.md` § 0.6 makes its promotion —
or a RECORDED non-promotion under `document-lifecycle`'s deliberate-non-promotion
scenario — a GATE on the successor map's realization rather than a follow-up.

**The ledger and README consequences of the five.** Each closure moves that
change's row in `tests/sequenced_after/corpus-ledger.yaml` (`state`, and `class`
where a partner flips from co-modifier to sole), removes its "Active changes"
entry from the README "OpenSpec Records" block, and — for the two with contract
identities — leaves `contracts/CHANGELOG.md` entries that stay true and are not
rewritten. All five are Rule 7 substrate row 2 and row 3 movements at the time
they land, claimed then rather than now.

### D10 — Repository bootstrap (Q7): public, Apache-2.0, `opensoft`, from day one

Both repositories are created under `opensoft`, PUBLIC, under Apache-2.0 — the
patent grant being the reason to prefer it for an organization shipping
governance tooling, and matching `openChart`, `openPractice` and `openRepoShape`.
Descendants follow their domain repositories' visibility.

**"Two layers of opensource" has no in-house precedent and that is a real cost.**
`opensoft/openxFactory` is PRIVATE with NO license, and `opensoft/openXwallet`,
created days ago under a ruling that called it a neutral open-source product, is
likewise private and unlicensed. So openDox and openXdox are the first genuinely
public repositories in this family that were MEANT to be, and public from day one
means a CONTRIBUTION POSTURE and a SECURITY-REPORT POLICY must exist at creation
rather than after the first outside issue. `tasks.md` § 1.4 makes both artifacts
part of the bootstrap, not a follow-up: retro-licensing a repository that has
taken outside contributions is materially harder than choosing at creation, and
the family's current posture shows how easily "open" stays nominal by default.

Each repository gets, at bootstrap: `README.md`, `LICENSE` (Apache-2.0),
`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `AGENTS.md`/`CLAUDE.md`,
`.github/CODEOWNERS`, its own OpenSpec instance, its own `contracts/manifest.yaml`
and `CHANGELOG.md`, one required check created in EVALUATE mode and promoted to
ACTIVE once it has reported, and — for openXdox — `contracts/opendox-pin.yaml`.

> Amended 2026-09-05 — repository shape. "Each repository" is now each PROJECT,
> and the list above distributes across its three repositories rather than
> sitting in one: § D12 records the election, `tasks.md` § 1.3 says exactly what
> `scaffold-project.py` writes and what stays a hand act, and § 1.4 places the
> posture files (LICENSE and SECURITY.md in all six; CONTRIBUTING.md and
> CODE_OF_CONDUCT.md in the two assembly roots). The OpenSpec instance lands in
> each `-spec` leg; `contracts/manifest.yaml`, `CHANGELOG.md` and
> `contracts/opendox-pin.yaml` in the assembly root. Q7's substance — public,
> Apache-2.0, `opensoft`-owned, posture at creation — is unchanged, and it now
> binds six repositories instead of two.

### D11 — The Rule 7 substrate plan (issue #630)

| row | substrate | claimed when | why |
| --- | --- | --- | --- |
| **1** | codexFactory review-authority floor + its openxFactory pin | **AT REALIZATION, not now** | This packet adds and removes NO path under `openspec/specs/`. The archive does BOTH — it removes `openspec/specs/ideation-dashboard/` and adds two capability directories — and the floor is exact-set-equality. Its own runbook says **DE-FLOOR BEFORE YOU REMOVE**: the codexFactory pull request lands FIRST, then the openxFactory pin's five sites in one reviewed diff, then the removal. `tasks.md` § 5.6 and § 8.4. |
| **2** | `tests/sequenced_after/corpus-ledger.yaml` + the MOVEMENT LOG | **NOW** | This packet adds one change directory, so it adds one ledger row and may flip partners' `class` where its REMOVED block shares requirement keys. Seeded with `--seed-ledger --moved-by '#<PR>'` once the PR number exists. **Amended 2026-09-05.** This row first said *"No MOVEMENT LOG entry is owed: a row added is a move the diff itself states."* That was measured wrong and `tasks.md` § 0.9 already carries the correction (Copilot round 5, 2026-09-05): the seeding moved TEN rows, not one — this change's own row enters as an ACTIVE co-modifier and NINE ARCHIVED rows flip `sole` -> `co-modifier` in the same act, because a `## REMOVED Requirements` block naming all 102 `ideation-dashboard` titles shares a requirement key with every change that ever solely added one. Nine partner rows moving for somebody else's delta is not legible from the row diff alone, which is the condition the log entry exists for, **so an entry IS owed and § 0.9 writes it.** Nothing else in this row moves, and this correction is not part of the shape ruling — it is a stale sentence in a table the shape amendment was editing anyway, fixed rather than left to contradict the tasks file. |
| **3** | README "OpenSpec Records" block | **NOW** | One row under Active changes. Two PRs editing the same lines conflict on merge; Rule 6's landing window is the merge-time half. |
| **4** | contract cuts | **AT THE CUT** | The MAJOR is claimed by NUMBER at § 5.7, not by this packet. |

### D12 — Repository shape: both layers elect the three-repository shape (2026-09-05)

**RULED — Brett Heap, 2026-09-05T14:52Z, in session, after a read of
`opensoft/openRepoShape` against this ratified packet.** Verbatim: **"elect the
shape for both, follow the pin chain, no family yet"** — recorded on
`opensoft/openxFactory` issue #656, comment `5552614170`. This section records
the decision, what was put beside it, and what it costs. It is an AMENDMENT to a
ratified document: nothing above is rewritten, and D1's topology, D2's seam,
D3's three-column assignment, D6's four-part floor and D9's re-homing plan are
untouched.

**The decision.** `openDox` and `openXdox` are each a THREE-REPOSITORY project in
the sense `docs/project-repo-schema.md` ratified on 2026-09-02: an assembly root
carrying `project.yaml`, the two legs as submodules, the pins and the `validate`
gate, plus a `<Project>-spec` leg and a `<Project>-code` leg. Six repositories,
created by `scaffold-project.py` rather than by hand, PUBLIC and Apache-2.0 as
RULING Q7 already required, with the election recorded in each `project.yaml`
(`elected_by: Brett Heap`, `elected_on: 2026-09-05`,
`reference: openxFactory docs/project-repo-schema.md`). Descendants are scaffolded the same
way with `--pin openXdox@<sha>`. **No family holder is created.**

**Electing confers nothing, and that is why this is an amendment and not a
re-ratification.** The doctrine's own first sentence: the shape changes no gate,
no floor, no grant and no authority. Every boundary this packet ratified — what
leaves, what stays, the adapter seam, the floor, the pin direction — reads
identically before and after. What moved is where files sit and how many
repositories the bootstrap creates.

**The alternatives Brett was shown, and why each was not taken.**

| put | what it was | why not taken |
| --- | --- | --- |
| **two single repositories, on the neutral-product precedent** | every `open*` neutral product in `opensoft` today is ONE repository — `openxFactory`, `openXwallet`, `openChart`, `openPractice`, `openRepoShape`. Keeping openDox and openXdox single would have made them ordinary members of that set and cost nothing to start | NOT TAKEN. openDox is not a contract family; it is an APPLICATION WITH A SCHEMA whose requirements and whose code have different reviewers, different cadences and different floors — the gap the proposal's own § Impact names in the aggregation's working rule #1. The shape gives the split a reviewed boundary instead of a directory convention, and gives a consumer one commit that names both halves |
| **a `Dox` family holder** | `openRepoShape` has a family form — a holder repository carrying `family.yaml` (`kind: family-manifest`) naming the members it pins, with its own templates and validator. It would have held `openDox`, `openXdox` and the descendants as one named set | NOT TAKEN — *"no family yet"*. Three members, one of which does not exist, is not a family; the holder would be a repository whose only content is a list nobody reads yet. **The option stays deliberately OPEN**: nothing here forecloses it, and a holder can be created later over repositories that already exist, which is the cheap direction. It is recorded as an open option rather than a rejected one |
| **elect for openXdox only** | openXdox is the layer with two audiences (the mapping core and its descendants), so it has the stronger case for a spec/code split; openDox could have stayed single | NOT TAKEN by the ruling's own word — *"for both"*. A neutral core whose requirements live inside its code repository while its integration layer's do not is exactly the asymmetry a descendant would have to learn twice |

**The pin chain, and what this packet depends on.** `openXdox`'s `project.yaml`
declares `neutral_product_pins: [openDox]`; every descendant declares
`[openXdox]`. That is RULING OQ-2 expressed as tree facts — inside the family
openDox is pinned only by openXdox, and no descendant pins openDox directly.
`openRepoShape`'s descendant-referent rule derives the referent from the NAME.
**`opensoft/openRepoShape`#40 is the amendment that makes the referent follow the
DECLARED CHAIN** (`codexDox` → `openXdox` → `openDox`, every link an offline fact
in a tree, the chain recorded rather than inferred).

**What the tool does TODAY is not what #40's own issue body says, and this
amendment corrects the record rather than repeating it.** #40 states that
`openXdox` *"is never a referent for `<Domainx>Dox`"*, so `codexDox` would
classify as a plain assembly root. Measured in this session at openRepoShape
`main` `f9ff3f8`: `codexDox` with `neutral_product_pins: [openXdox]` classifies
as `domain-descendant / assembly` — it PASSES — and
`templates/assembly-root/scripts/validate-manifest.py` accepts the manifest it
writes. It passes by ACCIDENT. The descendant family admits an x-stem spelling of
the referent (`contracts/repository-naming.yaml`, `also_accepted: openx{product}`,
there so `codexFactory` may descend from `openxFactory`), the referent test
compares CASE-FOLDED, and `openXdox`.casefold() equals `openxDox`.casefold(). The
pin on the INTEGRATION layer therefore satisfies the referent test for the
NEUTRAL CORE, and the manifest records `descendant_referent: openDox`,
`referent_declared: true` in a tree that declares no openDox pin at all. The
classification is right and its stated reason is false — which is worse than a
refusal, because nothing surfaces it.

That does not weaken #40; it is the argument for it, and #40 is now RESOLVED —
openRepoShape PR #42, merge commit `c2cc9e25`, merged 2026-09-05T16:26:49Z —
making the same classification TRUE by naming the chain the descendant
actually relies on, and removing a pass that would have evaporated the moment
anyone tightened the x-stem rule or compared spellings exactly. `tasks.md`
§ 1.10 records the interim this lane decided rather than leaving it to the
session that hit it: the descendant scaffolds WITH `--referent-chain
openXdox,openDox`, and the chain it relies on is RECORDED in its own manifest —
written by that flag alone, never inferred — so the accidental pass is never
left standing as the explanation, until the re-pin below carries #42's fix into
this repository. What the interim does not permit is adding a direct `openDox` pin
to force the classification.

**A second dependency, measured while authoring this amendment and now also
RESOLVED: `opensoft/openRepoShape`#41.** `scaffold-project.py` REFUSED both
invocations at the commit this repository pins — it printed `REFUSED
naming-role-mismatch` and exited, saying `openDox` classifies as a neutral
product rather than as the assembly form of a project leg — because
`accepts_role()` admitted only `project-leg/<role>` and
`domain-descendant/assembly`. Verified at openRepoShape `main` `f9ff3f8` and at
`122d729bc0c2f2e0ded0bb61b6b97f49512f613e`, the commit
`contracts/openreposhape-pin.yaml` pins, so it was not a tip regression. The
standard already computed the resolution it needed (`--explain openDox`
reported `also_matches: project-leg/assembly`) and then discarded it. #41
asked for the admission — a neutral product may elect the shape and be its own
assembly root, on the same reasoning that already lets a declared descendant
be one — and openRepoShape PR #45, *A neutral product may elect the shape and
be its own assembly root (#41)*, merge commit `5ffa8d58`, merged
2026-09-05T17:19:11Z (issue #41 closed 17:19:12Z), authored by lane `xfactory-2`, is that admission.
`355f6ef4` (#47) and every descendant commit carry both `c2cc9e25`
and `5ffa8d58`. **That re-pin has LANDED** *(reality check 2026-09-05, second
run, claims C38/C39)*: PR #700, commit `303bfd53` (2026-09-05T17:50-04:00),
moved this repository's `contracts/openreposhape-pin.yaml` to
`e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63` — a descendant of `355f6ef4`
carrying both #42 and #45, verifying clean (31 digests / 45 path-only / 76
files declared). **No blocker remains; `tasks.md` § 1.1a records the
discharge.** This packet performs nothing, so nothing else was ever blocked
by it.

**Where `contracts/manifest.yaml` and the bundle tag live, and why.** In the
ASSEMBLY ROOT of each project, with the release cut there. The assembly root is
the only object whose single commit names both legs, so it is the only place a
release identity can describe THE PROJECT rather than half of it; a tag on
`openDox-code` says nothing about the requirements that shipped with it.
`neutral-product-pin` makes a consumer pin a commit and a digest, so the commit a
consumer pins has to be the one that answers *what was this project at that
moment* — which is the assembly root's commit, and it is what openXdox's
`contracts/opendox-pin.yaml` names, and what `openxFactory`'s ONE pin file —
`contracts/openxdox-pin.yaml` — also names for openXdox (RULING F, `#656`,
2026-09-05, "rule F openXdox only"): `openxFactory` carries no
`contracts/opendox-pin.yaml` of its own, and openDox's commit there is a
DERIVED value read through openXdox's own pin.
The legs are pinned by their own assembly root, twice and in one commit (gitlink
plus `contracts/<role>-pin.yaml`), under the lockstep invariant the doctrine
already ratified.

**The cost accepted, stated rather than discovered.** A change to openDox's code
is not visible to openXdox until TWO pins move: openDox's assembly root advances
its own `code` pin (gitlink plus `contracts/code-pin.yaml`, same commit), and
openXdox then bumps `contracts/opendox-pin.yaml`. A single-repository `openDox`
would still need the second move — a consumer pins a neutral product by commit
and tree digest whatever its internal shape, which is why `openxFactory` bumps
`contracts/openreposhape-pin.yaml` and `contracts/openxwallet-pin.yaml` by hand
for two single-repository products today. What the shape election adds is the
first move alone. *(reality check 2026-09-05, second run, claims C27/C41.)*
This is the aggregation's own gitlink-trap discipline one level
down — the invariant that went unwritten for months and left `validate` red on
seven consecutive pin-syncs — and the reason the doctrine makes the assembly
root's gate refuse when the three parts disagree. It is a real cost and it buys a
reviewed boundary between requirements and implementation for a product whose
whole purpose is governing that boundary for other people.

**What this decision does NOT change.** The successor map's 102 rows and its
71/16/15 split; the corpus-adapter seam and its four operations; the four-part
floor; the database boundary; the tenancy model; the re-homing plan for the five
frozen changes; the two MODIFIED capabilities and the two ADDED ones; RULING
OQ-2's single pin chain; and the naming record's `openXdox` spelling, wire label
and handle. `tasks.md` groups 2, 5, 6 and 8 do not move, save the two § 8
evidence lines that COUNT repositories.

## Risks and trade-offs

1. **The successor map is 102 hand-authored rows and it is the highest-risk
   bookkeeping in the change.** Mitigation: the titles are GENERATED from the
   promoted spec rather than retyped (one character of drift leaves the promoting
   writer authoritative and the removal invisible to `promotion_fidelity.py`), and
   each row carries its own reason so a row can be contested alone.
2. **Five ratified deltas are frozen mid-flight and one of them is already
   partly realized in contract bytes.** `retire-doxbench-chat-turn-v1` cannot
   simply close (§ D9). Mitigation: it archives in `openxFactory` on its own
   evidence BEFORE this change archives, and § 6.2 sequences it.
3. **`serve.py` is the critical path and the most-changed module in the package.**
   Mitigation: the extension point is landed as its own task (§ 3.3) with the
   route families separated inside `openxFactory` before either repository holds
   any of it.
4. **The apply lane has one dispatch in its history and Q1 makes it every
   tenant's every governed write.** Mitigation: § 2.5 hardens it as a
   PRECONDITION, and the change does not archive on a lane proven by a dry run —
   the evidence bar the wallet arc and the nightly-refresh lane both established.
5. **N tenants is N of everything.** Mitigation: the modified
   `domain-descendant-boundary` makes the cost DECLARED at creation, and Q2's
   pattern reuse means the Hermes install's ordered migrations and lifecycle CLI
   are copied rather than reinvented.
6. **openXdox may be largely UNBUILT under RULING C2**, since three of its seven
   machineries do not exist. Mitigation: stated plainly rather than discovered —
   the character of the work is "carve AND build", § 4 is sized accordingly, and
   the three unbuilt machineries are named as separate features rather than
   folded into the carve.
7. **The front end has no package boundary to discover.** Mitigation: § 3.4 makes
   inventing one its own task, and names it as where a student-usable openDox is
   won or lost.
8. **A named-and-absent repository is a thing people create by hand at 2am.**
   Mitigation: the descendant names are REGISTERED in the naming record and no
   repository is created — the wallet arc's own treatment.

## Migration plan

`tasks.md`'s groups, in order, each a Speckit feature on the standing rule that
OpenSpec ratifies the boundary and Speckit builds it. Rollback per step:

0. **Ratification read + Amendment 3 drafted** — rollback: none needed; nothing
   outside `openspec/` has moved.
1. **Repository bootstrap** — rollback: delete two empty repositories.
2. **The seam, INSIDE `openxFactory`** — the neutral module, the adapter's
   operations, the `serve.py`/`cli.py` extension points, the apply lane hardened.
   Rollback: revert; every piece is independently correct.
3. **The openDox carve**, with the mapping manifest. Rollback: the manifest is the
   inverse map; `openxFactory` has not shed yet.
4. **The openXdox mapping core.** Rollback: as above.
5. **`openxFactory` consumes and sheds; the MAJOR is cut.** BREAKING, one atomic
   pull request, de-floored first. Rollback: revert the shed; the pins stay valid.
6. **The five re-homings.** Rollback: per change.
7. **The first descendant** — gated on a ruling, not on this plan.
8. **The archive gate.** No rollback: it is a gate, not an act.

## Questions this document put — ALL FOUR RULED, 2026-09-04

This document and `proposal.md` put four questions at PR #666. **Brett Heap ruled
every one of them the same evening**, on `opensoft/openxFactory` issue #656,
before ratification — see the R table above for the comment ids, and
`proposal.md` § Questions put for ruling for the full statements and the rejected
alternatives.

| question | ruled | where it is encoded here |
| --- | --- | --- |
| **DQ-1** — where `openxFactory`'s own engineering adapter lives | `openxFactory` KEEPS it; `codexDox` is a thin descendant that reuses it | § D1 (with the topology and the three consequences), § D3's third column, § D9's lens split |
| **OQ-1** — what replaces byte identity | the FOUR-PART FLOOR, as a requirement of this change | § D6, with the ruling's own CLOSED edit-class list and the reason there is no promoted requirement for it |
| **OQ-2** — may a governed consumer pin openDox directly | NO; one chain, and no third MODIFIED requirement on `neutral-product-pin` | § D3a, and the `neutral-product-pin` delta's declared scope |
| **OQ-3** — does `document-lifecycle` parameterize now | NO delta now; descendants declare via `domain-mapping-declaration` | § D3a, and `proposal.md` § Declared NOT modified |

**NOTHING IN THIS PACKET IS NOW OPEN.** Two residuals are recorded rather than
asked, because neither is a question the packet needs answered to be ratified:
the pre-governed scratch space a lab assistant may want (§ D5, a consequence of
the rejected ideas-in-the-database hybrid), and the front end's absent package
boundary (§ D3, which `tasks.md` § 3.4 makes its own task). Brett's ratification
word on the proposal as a whole — *"ratify #666"*, 2026-09-05T01:38Z, over head
`6935fb8b` — has since been given, and the 102-row successor map is what that
read was over. Both residuals survive it, recorded and not resolved.
