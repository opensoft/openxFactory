---
code_surface: openxFactory, opensoft/openDox (NEW), opensoft/openXdox (NEW), xFactory (aggregation), Omnigent-Install, OpsxFactory, codexFactory — SEVEN repositories, two of which do not exist. (1) `opensoft/openDox` created from scratch — PUBLIC, Apache-2.0, `opensoft`-owned (RULING Q7) — carrying the app that leaves `openxFactory`: the editor and canvas family, the model plane, branch sessions and pull requests, accounts, projects, documents and ideas, the NotebookLM connection, the named PULL-UP wave (`doxbench_knowledge` 1,231 LOC, `doxbench_abstract_store` 446 plus its generation surface, the keyword-query half of `lens` 282, `notebook_action` 239), the app-server half of `serve.py` behind a route EXTENSION POINT, the neutral half of `cli.py`, the CORPUS-ADAPTER INTERFACE as openDox's own declaration, a FastAPI + Postgres runtime on the `xFactory-Hermes-Install` shape with `migrations/` (ordered SQL) and `deploy/{compose,kubernetes}/`, its own `contracts/manifest.yaml` and bundle tag, `.github/CODEOWNERS`, a required check from day one and a branch-protection ruleset. (2) `opensoft/openXdox` created from scratch — PUBLIC, Apache-2.0 — carrying the domain-mapping core PARAMETERIZED by a domain profile (RULING C2): the corpus-adapter IMPLEMENTATION and projection mechanism (`corpus_root`, `generator`, `snapshot`, `snapshot_registry`, `register`, `completeness`, `round_trip`), the gate-and-commission loop (`gate_console`, `gate_routes`, `kickoff`, `record_binding`, `register_edit_lane`), `doxbench_scope`, the routes it contributes to openDox's extension point, its own pin of openDox, and the three machineries that do not exist anywhere today — the model/scenario workbench for `governed-derived-model` families, the evidence-and-provenance surface, and the role-and-authority projection. (3) `openxFactory` SHEDS: all 48 modules of `scripts/ideation_dashboard/` (49,605 LOC), all 40 files of `web/` (30,410 LOC excluding the vendored `markdown-it.min.js`), all 125 files of `tests/ideation-dashboard/` (3,927 `def test_` — 52% of this repository's 7,612 test functions) and the four-file `tests/ideation_dashboard/` underscore spelling, `scripts/ideation-dashboard-nightly.py`, `scripts/validate-ideation-dashboard-contracts.py`, the four dashboard contract schemas and 142 packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and `openspec/specs/ideation-dashboard/spec.md` (289,266 B / 102 requirements / 472 scenarios); and GAINS `contracts/opendox-pin.yaml` + `contracts/openxdox-pin.yaml`, two gitlinks, `scripts/doc_health/` edits (the two back-imports at `derive_possibles.py:857` and `ideation_readiness.py:1351` relocate to a small neutral module BOTH sides depend on), `contracts/manifest.yaml` / `README.md` / `CHANGELOG.md` / `contracts/releases/<tag>.digests.yaml`, `.github/CODEOWNERS`, the dashboard workflows converted to consumer gates on the `openxwallet-consumer-gate` shape, `README.md`, and `docs/openxdox-naming.md` Amendment 3. (4) BRANCH-PROTECTION RULESET STATE in three repositories — a repository setting, not a tree fact, and therefore its own evidence line. (5) The xFactory aggregation: `.gitmodules`, two root gitlinks, `README.md`, `CLAUDE.md`, `project-register.yaml`. (6) Omnigent-Install: the per-tenant installer that provisions an instance, its database and its two GitHub Apps through the App Manifest flow, plus the intent inbox and minter. (7) OpsxFactory: the `dox` workload set (`workflows/aks-administration.yaml:412-431`) becomes per-tenant, and the ungoverned `openxdox` DNS record is governed. (8) codexFactory: two draft Speckit features (002, 010) and the false `stack.yaml` doxBench digest declaration, plus the review-authority FLOOR de-floor that must precede any removal under `openspec/specs/` (Rule 7 substrate row 1). Per `release-realization` this change archives ONLY on merged plus green realization evidence across the affected repositories, never on landing.
target_release: implementation_pending — the affected repositories' own main lines, plus release identities allocated AT THE CUT and deliberately NOT reserved here: `dox-v1.0` in `opensoft/openDox` and `xdox-v1.0` in `opensoft/openXdox` (each its first bundle tag, cut only after the behavioural floor is proven), and the next openxFactory contract bundle, which is a **MAJOR**. It is a major because `docs/contract-versioning-policy.md` § Change Classes makes "a shape is removed" BREAKING, and this change removes four contract schemas, 142 packaged examples and the largest promoted specification in the corpus — the same class the wallet extraction shed at `contract-v2.0`. The NUMBER is deliberately unnumbered here on the wallet precedent's own reasoning: § Version Identity forbids reserving a minor before merge order is known, and a MAJOR named in a proposal that will not be realized for several waves is a reservation in everything but spelling — `contract-v3.4` is the current bundle as of 2026-09-04 (it landed at `807a4f47` while this packet was being authored, which is exactly the reason not to name a number) and what follows it depends on what else cuts first. That bundle also owes a `contracts/releases/<tag>.digests.yaml` over its own release surface under `release-surface-integrity`, discharged at the cut and not by this packet.
---

# Proposal: split-opendox-two-layer-product

Status: draft
Proposed: 2026-09-04 — the exit of the staged topic
`ideation/staging/opendox-two-layer-product/`
(`openxFactory:staging:opendox-two-layer-product`, staged and fully
dispositioned the same day), on Brett Heap's eleven recorded acts of 2026-09-04
on the governing record `opensoft/openxFactory` issue #656.
Lane: `openxfactory-opendox`.

**THIS PACKET IS PROPOSAL ONLY AND IT IS NOT RATIFIED.** `Status: draft`. No
repository is created, no code moves, no capability is promoted or removed, and
`docs/openxdox-naming.md` is NOT edited by this packet — Amendment 3's text is
DRAFTED in `design.md` § D8 and APPLIED at realization, because amending a
`ratified` record ahead of the act it describes would leave the record
describing a repository that does not exist. What this packet asks for is a
ratification read over the doctrine, the 102-row successor map, the four
MODIFIED requirements, the two ADDED capabilities and the re-homing plan for
five active changes; FOUR questions are put for ruling in § Open questions and
none of them is decided here.

## Rulings carried as LOCKED constraints

Eleven acts, all 2026-09-04, all on `opensoft/openxFactory` issue #656. **They
are constraints on this proposal, not questions in it.** A reviewer may contest
how the proposal CONSTRUCTS them; ratification does not reopen them.

0. **THE FOUNDING RULING** (the issue body, recorded verbatim). Two utterances.
   The origin complaint: *"we do not have a place to store projects. If i want to
   start a new project in a new repo, and make some specs, we have no good place
   to store my projects. I think we need to make this an app that installs and is
   hosted with a db. we should have users and projects and can expand the feature
   set."* And the topology: *"openDox is a dead project … lets use that name as
   the core opensource repo. we have two layers of opensource openDox and
   openXdox. The openXdox is openDox tuned for use with openXfactory. we will
   make openDox work to just manage documents and ideas. it will keep the
   integration with git and notebook lm etc and have all tools that help for
   document management and ideation. then openXdox will integrate with
   openXfactory."* Plus, from earlier the same sitting: *"We then further pin
   that down to medxDox and CodeXdox for use in those domain factories. If I
   install MedxFacotry [sic], then I get a medXdox install running in the
   installed tenand [sic] with its own db."*
1. **RULING Q1 — 15:24Z — the database owns IDENTITY AND COORDINATION; git owns
   GOVERNED ARTIFACTS.** Users, memberships, projects, the project-to-repository
   mapping, sessions and unsaved drafts live in the openDox database. Specs,
   changes, ideation documents and contracts stay in git, read from repositories
   and **written back only through the apply lane**. Every existing gate stays
   valid and the database is DISPOSABLE relative to the corpus. Rejected:
   documents in the database with git as an export; the hybrid where ideas live
   in the database until promoted.
2. **RULING Q2 — 15:31Z — reuse the Hermes install pattern.** FastAPI +
   Postgres, deployed the way `xFactory-Hermes-Install` is (live on AKS since
   2026-07-19), OIDC through the Keycloak broker being adopted in QA; the
   OpsxFactory `dox` workload set is the deployment shape it grows into.
   Rejected: bolting a database onto today's stdlib `serve.py` monolith; a new
   full-stack platform.
3. **RULING Q3 — 15:32Z — one instance and one database per tenant, ALWAYS**,
   in both the operator-hosted case and the tenant-hosted case. **No cross-tenant
   data ever shares a store.** Rejected: a shared multi-tenant openDox with
   row-level isolation; a per-tenant default with a pooled option. Consequence:
   the descendant IS the deployment unit.
4. **RULING Q4 — 15:34Z — openDox DEFINES the corpus-adapter interface; openXdox
   IMPLEMENTS it.** openDox declares how documents are listed, read, written back
   and checked, with **no knowledge of OpenSpec or doc-health**. The two
   `scripts/doc_health/` back-imports move into a small neutral module both sides
   depend on. **The dependency points ONE way: openXdox depends on openDox, never
   the reverse.** Rejected: openDox pinning doc-health as a library; openXdox as a
   tuned copy with no shared interface.
5. **DIRECTION Q5 — 15:48Z — a THREE-LAYER TEST, and the per-module assignment is
   design work under it.** openDox must be useful ALONE to a student or a lab
   assistant, with an active obligation to find what to PULL UP; openXdox holds
   the machinery COMMON to how Medx, Ledgerx and Adx each map onto the workbench,
   and those three mappings must be worked explicitly; descendants hold the
   domain-specific mapping. The module test: *"would someone with no notion of
   factories, gates or tenants use it?"*
6. **RULING C1 — 17:46Z — the name collision is accepted knowingly; the
   repository is `opensoft/openDox`.** Amendment 3 records the MEASURED facts and
   Brett's acceptance of them; no claim is made on the `opendox` organization
   name; the brand lives under `opensoft`. Which specific abandoned repository
   prompted "dead" is immaterial. Rejected: citing a specific dead repo as the
   basis; reconsidering the name (`openXnotes` stays documented, unused).
7. **RULING C2 — 17:47Z — openXdox is the DOMAIN-MAPPING CORE, PARAMETERIZED.**
   It holds what every domain factory shares — typed artifact kinds, a governed
   lifecycle engine (statuses, gates, roles, evidence) and the dispatch/apply lane
   — parameterized by a domain profile a descendant supplies. Engineering
   vocabulary belongs to `codexDox`, or stays in `openxFactory` as its own adapter
   over the corpus-adapter interface; **a clinician using `MedxDox` never sees the
   word "requirement"**. Rejected: openXdox as today's dashboard minus the
   pull-ups; one repo with two packages.
8. **RULING C3 — 17:48Z — standalone openDox creates and manages a PLAIN LOCAL
   GIT REPOSITORY per project.** Documents are always git-backed, commits are the
   write path, a remote can be attached later; Q1 holds unchanged, and moving a
   student project into a governed factory is a PUSH, not a migration. Rejected:
   a loose-documents mode; requiring a repository before the first save.
9. **RULING Q6 — 17:49Z — FREEZE THE DASHBOARD NOW AND CARVE IMMEDIATELY.** The
   five active changes stop where they stand in `openxFactory`; their live deltas
   and open tasks (20 across the two with open archive gates) are RE-HOMED into
   this change and the new repositories as part of the carve. **No new dashboard
   change opens in `openxFactory`.** The lane's own recommendation — let the five
   finish, carve after the two gated ones archive — was put and NOT taken; the
   cost accepted is re-homing 20 open tasks and a never-green lane mid-flight.
10. **RULING Q7 — 17:51Z — `opensoft` owns both repositories; both are PUBLIC
    from day one under Apache-2.0**, matching `openChart`, `openPractice` and
    `openRepoShape`. Descendants follow their domain repositories' visibility.
    Rejected: openXdox private until the descendants prove the boundary; MIT or
    AGPL-3.0.

## Why

**Brett has nowhere to put a project, and the workbench that should be that home
is a reader.** Starting a new project in a new repository and writing some specs
today requires cloning the aggregation, choosing a submodule, placing the
document in that repository's ideation tree, and commissioning a row into a
register file that lives in a THIRD repository — and there is no answer at all
for a project that is not one of the eleven repositories the register knows
about. The workbench's 49,605 lines of Python and 30,410 lines of front end are
built on the assumption that the record already exists, in a git checkout, with
a lifecycle header, in a corpus whose paths are hardcoded across a third of its
modules: `ideation/staging` appears as a path literal in 16 modules, `contracts/`
in 15, `docs/` in 9, `ideation/brainstorm` in 8, `openspec/changes` in 7. It
renders a project as navigation over repositories and cannot let a project own
anything, because a project is a row in a YAML file the dashboard is forbidden
to write.

**The neutral half is substantial, finished, and unreachable.** A dual-buffer
editor with a per-buffer staleness guard, a chat bound to the active buffer,
branch sessions with commit-per-act and one pull request, share-session hand-off,
model bindings and broker-minted tokens, deterministic and distilled abstracts
with a path-digest-model cache, bounded knowledge packets over a selected
document set with declared fidelity, a keyword set-builder, a NotebookLM
connection. A student or a lab assistant would use every one of those with no
notion of factories, gates or tenants — and cannot, because they are filed as
governance features of a corpus reader. The measured pull-up wave is small and
specific: `doxbench_knowledge` at 1,231 LOC is filed as governance ONLY because
its input set is called "the staged set".

**The third layer is why the split cannot be deferred.** What `openxFactory`
brings to a domain — a lifecycle, a gate loop, an evidence trail, a
model-and-scenario pair, a role projection, a review lane — is machinery
MedxFactory, LedgerxFactory and AdxFactory each need IN THE SAME SHAPE WITH
DIFFERENT NOUNS. The three mappings were worked (`design.md` § D4) and they
differ in their WORDS, not their shape: a clinical note drafted → attested →
filed → immutable-with-addenda; an accounting question raised → researched →
concluded → professionally reviewed → filed as a defensible position; a campaign
brief drafted → brand-reviewed → spend-approved → launched → measured → retired.
Today that machinery exists once, hardcoded to one domain's vocabulary, inside a
reader no domain can install. And the largest piece of it does not exist at all:
all three domains declare a `governed-derived-model` family — Medx's Dream Object
/ Simulation Scenario at the `governed` tier with RATIFIED templates, Adx's
Persona / Campaign Simulation at `calibrated`, Ledgerx's Counterparty Health
Profile / Financial Scenario staged — and **there is no UI for a model or a
scenario anywhere in these 80,000 lines.**

**The recorded objection, kept rather than overwritten.** The 2026-09-04
read-only review recommended NOT NOW at medium-high confidence, on three
grounds: the wallet precedent's own trigger (a live consumer) has not fired —
codexFactory holds ZERO tracked files under `scripts/ideation_dashboard/` or
`tests/ideation-dashboard/` at `origin/main`; the move cannot be byte-identical;
five active changes are mid-flight with two open archive gates. **All three
facts are still true.** The rulings supersede the recommendation by COMMISSIONING
the consumer rather than waiting for it, and the three facts become this
change's sequencing constraints rather than being argued away: fact one is why
`tasks.md` § 7 is a task with a ruling checkbox rather than a decision; fact two
is why the byte-identity floor is replaced rather than weakened (§ D6); fact
three is what RULING Q6 disposes of and `tasks.md` § 6 executes.

## What changes

### What this change RATIFIES (its own diff)

Nothing outside `openspec/`, the staging INDEX and the README. Concretely: this
packet (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`), five spec
delta files, one INDEX row edit recording the exit, and one README "OpenSpec
Records" row. `docs/openxdox-naming.md` is NOT touched; no repository is created;
no module moves; no capability is promoted or removed until this change archives.

- **REMOVED-by-SPLIT `ideation-dashboard`** — all 102 promoted requirements leave
  this corpus, each with its successor destination and the reason it reads that
  way. 71 read as **openDox**, 16 as **openXdox**, 15 as **`codexDox`**. This is
  the corpus's first three-way capability exit and its second capability exit of
  any kind.
- **ADDED `corpus-adapter-seam`** — four requirements governing the half
  `openxFactory` cannot delegate: a corpus reader is an external pinned product
  and the dependency points ONE way; a reader over a corpus it does not own fails
  closed and distinguishes "empty" from "could not look"; the governed write path
  is the only write path and the adapter declares it; and `openxFactory`'s own
  adapter is one conformant implementation with no privileged route. **The
  INTERFACE ITSELF IS NOT AUTHORED HERE** — RULING Q4 gives its definition to
  openDox, and `design.md` § D2 carries the four-operation sketch as design.
- **ADDED `domain-mapping-declaration`** — three requirements naming the five axes
  a `<Domainx>Dox` descendant declares (artifact kinds; lifecycle vocabulary with
  transitions, authorities and the immutability point; acts and their gates;
  evidence classes; promoting authorities), and the rule that the neutral layer
  ships no domain's vocabulary. This is what gives `domain-descendant-boundary`'s
  "pin and profile, never fork" something concrete to mean one level down.
- **MODIFIED `domain-descendant-boundary`, two requirements** — *A descendant
  carries profile, never fork* grows the SCHEMA clause (the migration set is
  pinned content; domain fields go through a declared extension point; a
  descendant-authored migration is a fork of the schema, and the harder fork to
  detect because a database diverges silently); *A descendant is created on its
  first profile, not before* grows the DEPLOYMENT-UNIT clause (a committed tenant
  install IS a profile artifact, which reconciles RULING Q3 with the laziness rule
  the standard already carries) and a declared-operating-cost clause.
- **MODIFIED `neutral-product-pin`, two requirements** — *An external neutral
  product is pinned by commit and digest, never by tag* grows the DEPLOYMENT
  clause (a pin whose consumption is a migration declares the range, the
  reversibility and the runbook; the bump completes when the operation runs, not
  when the file merges); *The consuming repository's pin is authoritative among
  reachable checkouts* grows the CHAIN clause (each level declares only its DIRECT
  upstream; a transitive commit is derived, never a second authority).

### What this change AUTHORIZES as successors, each with its own evidence

`tasks.md` groups 1–8, each a Speckit feature on the convener's standing rule
that **OpenSpec ratifies the boundary and Speckit builds it**. Ratification
authorizes them and performs none of them. In order: the two repositories
bootstrapped public under Apache-2.0 (§ 1); the corpus-adapter operations named
and the neutral module landed INSIDE `openxFactory`, breaking the two-way import
before anything moves (§ 2); the openDox carve with its mapping manifest (§ 3);
the openXdox mapping core (§ 4); `openxFactory` consuming, shedding and cutting
its MAJOR (§ 5); the five re-homings (§ 6); the first descendant, gated on a
ruling (§ 7); and the archive gate (§ 8).

### The departures from the wallet precedent, and that each is RULED

`split-openxwallet-repo` is the house's only ratified capability-exit precedent
and this change departs from it in three places. Each departure is a ruling, not
an oversight, and the proposal says so rather than reasoning as if the precedent
applied.

| wallet precedent | here | the ruling |
| --- | --- | --- |
| **R3 — the integration seam STAYS in `openxFactory`** (`governance/review-authority/` never moved; only the product left) | the integration layer is ITSELF an open-source repository; `openxFactory` keeps the corpus and its governance, and the code that reads the corpus leaves entirely | the founding ruling, "two layers of opensource", reinforced by RULING C2 |
| **ONE new repository** | TWO, plus a named third layer of descendants | the founding ruling |
| **A BYTE-IDENTICAL floor** — eight artifact digests matching the named carve commit, one prose carve-out, "because a move whose diff is not provably empty cannot be bisected against" | UNAVAILABLE. Twelve of forty-eight modules import `doc_health`, `doc_health` imports back twice, and the destinations gain a database and a runtime. Replaced by the three-part BEHAVIOURAL floor of § D6 | not ruled — the FORCED consequence of the measured coupling, and **Q9 travels to the ratification read as OQ-1** |

An implementer reading only R3 would draw this boundary in the wrong place. That
is why the departure is stated here and again in `design.md` § Context rather
than left to be noticed.

## Capabilities

### New Capabilities

- **`corpus-adapter-seam`** — 4 requirements, 13 scenarios. Governs the terms on
  which a reader `openxFactory` does not own reads `openxFactory`'s corpus.
- **`domain-mapping-declaration`** — 3 requirements, 9 scenarios. Governs what a
  `<Domainx>Dox` descendant declares so the neutral layer can be parameterized
  rather than forked.

### Modified Capabilities

- **`domain-descendant-boundary`** — 2 of 5 promoted requirements MODIFIED, each
  restated as canon states it at `origin/main` `a858e5b0` and then edited. Three
  requirements deliberately untouched (§ delta preamble).
- **`neutral-product-pin`** — 2 of 9 promoted requirements MODIFIED, on the same
  discipline. Seven deliberately untouched.

### Removed Capabilities

- **`ideation-dashboard`** — all 102 requirements, with a per-requirement
  successor map. No stub is left in `openxFactory`: keeping one would leave this
  repository owning requirements about code it does not hold, which is the
  condition the split exists to end.

### Declared NOT modified, with the reason

- **`doc-health`** — stays `openxFactory`'s own capability and is not split. The
  two back-imports move to a neutral module (a CODE change, § 2), which needs no
  requirement. Two active changes hold `doc-health` deltas
  (`add-nightly-dashboard-refresh`, `settle-aging-staging-topics`) and a third
  writer here would be an avoidable collision.
- **`document-lifecycle`** — the staging topic flagged a POSSIBLE modification (if
  the nine-word taxonomy becomes one instance of a declared shape rather than the
  shape itself). It is NOT authored here: `domain-mapping-declaration` states the
  parameterization from the descendant's side without touching the taxonomy
  `openxFactory` owns for its own corpus, and `add-ideation-intent-plane` holds an
  active `document-lifecycle` delta. Carried as OQ-3.
- **`governed-derived-model`** — the model/scenario workbench is the largest
  unbuilt piece of the openXdox core, but it is a UI over a contract that already
  exists at the `governed` tier with ratified templates. Building it changes no
  requirement. If it turns out to need a contract surface, that is its own change.
- **`ideation-intent-plane`** — RATIFIED 2026-07-23, part-realized, and ABSENT
  from `openspec/specs/` for 43 days, which RULING Q1 has just made load-bearing.
  A capability not in canon cannot be removed from canon. `tasks.md` § 0.6 makes
  its promotion, or a RECORDED non-promotion, a gate on the successor map's
  realization.
- **`release-realization`**, **`repo-boundary-governance`**,
  **`shared-contract-ownership`** — reached as written. Two active changes hold
  `release-realization` deltas and five hold `repo-boundary-governance` deltas;
  none of them is needed here.

## Impact

- **Affected specs:** as enumerated above — one REMOVED (102 requirements), two
  ADDED (7 requirements), two MODIFIED (4 requirements).
- **Affected code:** the seven repositories of `code_surface:`. The largest single
  movement in this repository's history by every measure available: 80,015 lines
  of Python and front end, 52% of the test functions, and the largest promoted
  specification in the corpus.
- **NEW OPERATING SURFACE created by RULING Q3:** N runtime deployments, N
  databases, N migration runs per release, N backup-and-restore policies and N
  credential sets, in BOTH the operator-hosted and tenant-hosted cases. The Hermes
  install pays exactly this bill today, which is the practical force behind
  RULING Q2's pattern reuse and the reason the modified
  `domain-descendant-boundary` requires the cost to be DECLARED at descendant
  creation rather than discovered one tenant at a time.
- **The apply lane is promoted by RULING Q1 from a demo to the ONLY governed write
  path**, with ONE dispatch in its entire history (`intent-apply.yml` on the
  aggregation: one run, ever, 2026-08-15T01:22:04Z, success). Its hardening is a
  PRECONDITION of the carve, not a follow-up (`tasks.md` § 2.5).
- **Working-rule blast radius:** the aggregation's amended working rule #1 already
  accommodates a neutral `open*` product `openxFactory` pins. What it does NOT
  accommodate is a neutral product that is an APPLICATION WITH A SCHEMA rather
  than a contract family — the same gap the two MODIFIED capabilities fill, and
  the aggregation's `CLAUDE.md` owes the matching amendment at § 5.
- **Branch protection and required checks:** two new repositories each need a
  required check from day one; `openxFactory`'s dashboard-contract validation
  becomes a consumer gate over pinned tools, on the `openxwallet-consumer-gate`
  shape.
- **Rule 7 substrates (issue #630):** row 2 (`tests/sequenced_after/corpus-ledger.yaml`
  plus the MOVEMENT LOG) and row 3 (README "OpenSpec Records") are claimed BY THIS
  PACKET. **Row 1 — the codexFactory review-authority floor — is claimed at
  REALIZATION, not now**: this packet adds and removes no path under
  `openspec/specs/`, and the floor's own runbook says DE-FLOOR BEFORE YOU REMOVE,
  so the codexFactory pull request precedes the archive that removes
  `openspec/specs/ideation-dashboard/` and adds the two new capability
  directories.
- **The 30 archived changes carrying an `ideation-dashboard` delta are IMMUTABLE
  RECORDS that get ANNOTATED, never edited into agreement** — the treatment the
  wallet arc used, and the highest-volume bookkeeping in the realization.

## Realization evidence

Under `release-realization`'s archive gate this change is NOT archivable on
landing. The evidence, per `tasks.md` § 8, is: both repositories exist, public,
Apache-2.0, each with a required check that has reported once; the behavioural
floor's three parts each produced their own artifact (§ D6); `openxFactory`'s
shed merged and its MAJOR cut, tagged and verified from an independently
refreshed checkout; the aggregation's gitlinks landed; every one of the five
re-homed changes dispositioned with its destination named in the receiving
repository; and the codexFactory floor de-floored BEFORE the removal, in that
order.

## Open questions

FOUR travel to the ratification read. Two more that the staging topic carried are
settled by rulings and are recorded as settled rather than re-asked.

### OQ-1. What replaces the byte-identical floor as this extraction's safety property?

**Context.** The wallet extraction's ratified floor was a pure move — eight
artifact digests matching the named carve commit before the tag was cut, with
exactly one permitted prose carve-out, *"because a move whose diff is not
provably empty cannot be bisected against"*. A three-way split of a package whose
modules import a sibling that imports back cannot meet it, and neither can a
split that adds a database and a runtime. **No 2026-09-04 ruling touches this
question** — it is the one the staging topic says travels unchanged.
**Recommended answer:** the three-part BEHAVIOURAL floor of `design.md` § D6 —
test-count arithmetic that must SUM, a neutral conformance corpus for openDox,
and a named snapshot-equivalence run — plus the per-requirement successor map as
the specification-side floor. **Explanation:** the safety property must be
mechanically checkable, because that is the whole function byte-identity
performed; each part catches a different failure, and none of them is "the tests
passed".

### OQ-2. May a consumer pin openDox DIRECTLY, or is openXdox always the pinned layer?

**Context.** The founding ruling says descendants pin openXdox, and for the
DomainxFactories that is right. DIRECTION Q5 then requires openDox to be useful
ALONE, and RULING C3 gives that standalone case a real shape (a plain local git
repository per project). If nothing may pin openDox alone, openDox has exactly
one consumer and its independence is nominal. **RULING C3 reinforces the premise
without settling the mechanics. Recommended answer:** BOTH are pinnable and the
consumer DECLARES which layer it pins — a one-field addition to
`domain-descendant-boundary`'s pin requirement rather than a second pattern.
**Not authored here**, because it would be a third MODIFIED requirement in a
capability this packet already modifies twice, decided on the proposer's own
authority.

### OQ-3. Does `document-lifecycle`'s taxonomy become one instance of a declared shape?

**Context.** RULING C2 settles that openXdox carries a parameterized ENGINE and
that `openxFactory`'s nine-word `Status:` taxonomy is the ENGINEERING descendant's
declaration. What it does not settle is whether `document-lifecycle` — which owns
that taxonomy as a contract for `openxFactory`'s OWN corpus — must say so.
**Recommended answer:** NO delta now. `domain-mapping-declaration` states the
obligation from the descendant's side, `openxFactory`'s taxonomy remains correct
for `openxFactory`'s corpus, and `add-ideation-intent-plane` holds an active
`document-lifecycle` delta that a second writer would collide with. Revisit when
the first non-engineering descendant declares a vocabulary.

### OQ-4. Where does `openxFactory`'s own engineering adapter live — `codexDox`, or `openxFactory`?

**Context.** RULING C2 states BOTH in one sentence: engineering vocabulary
*"belongs to the engineering descendant `codexDox`, **or** stays in openxFactory
as its own adapter over the corpus-adapter interface"*. Both readings are lawful
under the ruling and they lead to different trees. Under **Reading A** the 15
`codexDox`-mapped requirements land in a descendant, `openxFactory` retains no
reader code at all, and "the code that reads the corpus leaves entirely" is
literally true — but a descendant must exist before the carve completes, which
collides with `domain-descendant-boundary`'s laziness rule while codexFactory
holds zero tracked dashboard files. Under **Reading B** `openxFactory` keeps a
small in-tree adapter over its own corpus — which `corpus-adapter-seam`'s fourth
requirement is written to make lawful and UNPRIVILEGED — and `codexDox` is created
later, when codexFactory stands an instance up. **This packet does not choose**,
and the successor map's 15 rows carry the ruling's own disjunction verbatim rather
than resolving it. The choice moves 15 requirements and decides whether
`tasks.md` § 7's first descendant precedes or follows § 5; it changes nothing
else. Full statement at `design.md` § D1 as **DQ-1**.

### Settled by ruling, recorded rather than re-asked

- **The successor-map mechanics (the topic's Q8)** — RULING C2 settled the
  destination boundary; the REMOVE-with-a-map-rather-than-a-stub mechanics are
  taken as recommended and are authored in the delta. A reviewer contesting a ROW
  contests a row, not the mechanism.
- **The lifecycle parameterization (the topic's Q11)** — fully settled by RULING
  C2 and realized in `domain-mapping-declaration`'s second requirement.

## Out of scope, deliberately

- **Any repository creation, code movement, or naming-record edit.** This is the
  claim's own boundary and it is repeated here because it is the easiest thing to
  read past.
- **The `opendox` GitHub ORGANIZATION.** RULING C1: no claim is made on it.
- **`openXdox-Install` as a repository.** The name may be registered in the naming
  record at realization on rule (d); no repository is created, exactly as the
  wallet arc treated `openXwallet-Install`.
- **The five re-homed changes' own content decisions.** § 6 names each one's
  destination; what its requirements say in the receiving repository is that
  repository's change to author.
- **Correcting codexFactory's false `stack.yaml` doxBench digest declaration**
  beyond naming it. It declares `0e6e7e94…`/`8386566e…` at `contract-v1.29` while
  the actual bytes at its own pinned commit are `e563cc9f…`/`350bfedc…` and
  `openxFactory` is at `contract-v3.4`. It is a real defect, it is codexFactory's,
  and it is filed rather than fixed inside a seven-repository extraction.
