# Proposal Ratification: split-opendox-two-layer-product

Status: ratified
Decision date: 2026-09-05
Lane: openxfactory-opendox
Ratifier: Brett Heap (repository owner), in session, lane
`openxfactory-opendox`, session `01Ku6jmLxwesiWs4bQwRS3c4`.
Ratified: 2026-09-05 by Brett Heap (repository owner) — in-session, verbatim:
*"ratify #666"* at 2026-09-05T01:38Z, recorded on `opensoft/openxFactory`
issue #656 comment `5548470629` and mirrored on pull request #666 comment
`5548470786`.
Ratified baseline: head `6935fb8b` — "Take Copilot's three findings: two
records still described a packet with open questions" — the packet exactly as
it stood at that commit: `proposal.md`, `design.md`, `tasks.md`,
`.openspec.yaml`, and five spec delta files —
`specs/ideation-dashboard/spec.md` (REMOVED, 102 requirements),
`specs/corpus-adapter-seam/spec.md` (ADDED, 4 requirements / 11 scenarios),
`specs/domain-mapping-declaration/spec.md` (ADDED, 3 / 9),
`specs/domain-descendant-boundary/spec.md` (MODIFIED, 2 / 9) and
`specs/neutral-product-pin/spec.md` (MODIFIED, 2 / 10) — together with the
`ideation/staging/INDEX.md` row recording the topic's exit and the README
"OpenSpec Records" entry. There was no `review/` folder at that head; this
record is the first file in it.

## Decision

**RATIFY.** Brett's word was one word — *"ratify #666"* — and it carries one
act. **LANDING IS A SEPARATE ACT ON THE SAME WORD**, performed under
lane-collision-protocol Rule 6 (admin merge: the pull request is
`brettheap`-authored and cannot self-clear the code-owner review), and it is
not performed by this record. The ratification comment itself sequences the
three acts that follow it: (1) flip `proposal.md` to `Status: ratified` and
write this record quoting the rulings, (2) the Rule 6 landing of #666, (3)
realization by `tasks.md` groups, each its own Speckit feature, starting with
the corpus-adapter seam — and it states that realization is NOT started in
that window.

Unlike `add-cpc-clearing-boundary`'s ratification (`review/
ratification-2026-09-02.md`), where one word carried both ratify and merge,
this packet's own merge is a governed act with its own gate rather than a
second half of the same instruction. Nothing about it is contingent on a
review that has not run: the packet carries no code surface at all in its own
diff, and its `openspec validate --strict`, `--all --strict`,
`proposal-support.py verify`, doc-health and `tests/sequenced_after` runs are
green at the head this record is written on (recorded under Verification).

## What is ratified

**The two-layer doctrine.** `opensoft/openDox` is the neutral core — a hosted,
installable app with its own database, users and projects, document and idea
management, git and NotebookLM integration — useful ALONE to a student or a
lab assistant (DIRECTION Q5's three-layer test). `opensoft/openXdox` is the
domain-mapping core, PARAMETERIZED by a domain profile (RULING C2), holding
what is COMMON to how MedxFactory, LedgerxFactory and AdxFactory map onto the
workbench. Descendants (`MedxDox`, `codexDox`, …) hold the domain-specific
mapping and pin openXdox. `openxFactory` keeps the CORPUS, its GOVERNANCE and
— under RULING DQ-1 — ITS OWN ADAPTER over that corpus; what leaves is the
PRODUCT.

**The corpus's first three-way capability exit.** A `## REMOVED Requirements`
block over **ALL 102** promoted `ideation-dashboard` requirements — the
largest promoted specification in this corpus (289,266 B / 102 requirements /
472 scenarios) — each row naming its successor destination and the reason it
reads that way. Measured on the ratified tree: **71 openDox, 16 openXdox, 15
`openxFactory`'s own engineering adapter**. The third column is this
repository's own adapter package under RULING DQ-1, so those fifteen leave the
CAPABILITY and not the repository. No stub is left behind.

**Two ADDED capabilities.**

- `corpus-adapter-seam` — 4 requirements, 11 scenarios: a corpus reader is an
  external pinned product and the dependency points ONE way; a reader over a
  corpus it does not own fails closed and distinguishes "empty" from "could
  not look"; the governed write path is the only write path and the adapter
  declares it; and `openxFactory`'s own adapter is one conformant
  implementation with NO privileged route. **The INTERFACE ITSELF is not
  authored here** — RULING Q4 gives its definition to openDox.
- `domain-mapping-declaration` — 3 requirements, 9 scenarios: the five axes a
  `<Domainx>Dox` descendant declares (artifact kinds; lifecycle vocabulary
  with transitions, authorities and the immutability point; acts and their
  gates; evidence classes; promoting authorities), and the rule that the
  neutral layer ships no domain's vocabulary.

**Four MODIFIED requirements across two capabilities.**

- `domain-descendant-boundary`, 2 of 5 promoted requirements — the migration
  set is PINNED CONTENT and a descendant-authored migration is a fork of the
  schema (the harder fork to detect, because a database diverges silently);
  and a committed TENANT INSTALL is a profile artifact, which reconciles
  RULING Q3 with the standard's own laziness rule.
- `neutral-product-pin`, 2 of 9 promoted requirements — a pin whose
  consumption is a DEPLOYMENT declares its migration range, reversibility and
  runbook, and completes when the operation runs rather than when the file
  merges; and a pin CHAIN is resolved one hop at a time, each level declaring
  only its DIRECT upstream.

**The re-homing plan for the five frozen `ideation-dashboard` changes**
(RULING Q6, `design.md` § D9, `tasks.md` § 6): `add-nightly-dashboard-refresh`
→ openXdox, closed as re-homed, its SEVEN `doc-health` requirements NOT
travelling but re-authored against the adapter in openXdox — the one genuine
conflict Q6 names, and its resolution; `retire-doxbench-chat-turn-v1` →
openDox for its forward half only, and it is the one that CANNOT simply close
(its schema removal is already realized in `openxFactory` bytes at
`contract-v3.0`), so it archives HERE on its own evidence first;
`add-doxchat-model-intake` → openDox; `add-composed-view-authoring` → openDox;
`add-lens-document-selection` → openDox EXCEPT its `doc_health.staging_seed`
drafter and route, which stays in `openxFactory`'s own adapter under DQ-1 —
the only one of the five that splits across two destinations.

**The four-part floor replacing byte identity** (RULING OQ-1, `design.md` §
D6, gated one evidence line per part at `tasks.md` § 8.2): (1) a mapping
manifest listing every source path to its destination with per-file digests at
the cut, plus a CLOSED list of permitted edit classes — import rewrites, path
constants, adapter calls; (2) test counts that must SUM across the three
repositories; (3) a neutral conformance corpus EVERY destination passes,
including `openxFactory`'s own adapter; (4) a snapshot-equivalence run. Byte
identity is unavailable here — twelve of forty-eight modules import
`doc_health`, `doc_health` imports back twice at `derive_possibles.py:857` and
`ideation_readiness.py:1351`, and the destinations gain a database and a
runtime — and both single-instrument alternatives were rejected on the record.

## The rulings

Every ruling on the governing record `opensoft/openxFactory` issue #656,
quoted verbatim with its comment id and UTC timestamp. Each comment's trailing
`Lane: openxfactory-opendox` trailer is the only text dropped; nothing else is
paraphrased, elided or reordered.

**THE FOUNDING RULING** — the issue body, 2026-09-04T15:18:55Z, recorded
verbatim by Brett Heap in session (lane `openxfactory-opendox`):

> "we do not have a place to store projects. If i want to start a new project
> in a new repo, and make some specs, we have no good place to store my
> projects. I think we need to make this an app that installs and is hosted
> with a db. we should have users and projects and can expand the feature
> set."
>
> "openDox is a dead project. it has almost empty repo. I think someone
> started with idea and stopped after a few days. lets use that name as the
> core opensource repo. we have two layers of opensource openDox and openXdox.
> The openXdox is openDox tuned for use with openXfactory. we will make
> openDox work to just manage documents and ideas. it will keep the
> integration with git and notebook lm etc and have all tools that help for
> document management and ideation. then openXdox will integrate with
> openXfactory."
>
> Earlier in the same sitting: "We then further pin that down to medxDox and
> CodeXdox for use in those domain factories. If I install MedxFacotry, then I
> get a medXdox install running in the installed tenand with its own db."

**RULING Q1** — comment `5542694957`, 2026-09-04T15:24:37Z:
> RULING Q1 — Brett Heap, 2026-09-04T15:24Z, in session (lane
> openxfactory-opendox), on the question "what does the openDox database own
> as the source of truth, versus git?": **the database owns identity and
> coordination; git owns governed artifacts.** Users, memberships, projects,
> the project-to-repository mapping, sessions and unsaved drafts live in the
> openDox database. Specs, changes, ideation documents and contracts stay in
> git, read from repositories and written back only through the apply lane.
> Every existing gate (doc-health, OpenSpec, the PR checks) therefore stays
> valid; the database is disposable relative to the corpus. Rejected:
> documents in the database with git as an export; and the hybrid (ideas in
> the DB until promoted).

**RULING Q2** — comment `5542792997`, 2026-09-04T15:31:37Z:
> RULING Q2 — Brett Heap, 2026-09-04T15:31Z, in session (lane
> openxfactory-opendox), on the runtime shape: **reuse the Hermes install
> pattern** — FastAPI + Postgres, deployed the way `xFactory-Hermes-Install`
> is (live on AKS since 2026-07-19), OIDC through the Keycloak broker being
> adopted in QA; the OpsxFactory `dox` workload set (auth, dashboard,
> intent-inbox, token-minter) is the deployment shape it grows into. Rejected:
> bolting a database onto today's stdlib `serve.py` monolith; a new full-stack
> platform.

**RULING Q3** — comment `5542805602`, 2026-09-04T15:32:36Z:
> RULING Q3 — Brett Heap, 2026-09-04T15:32Z, in session (lane
> openxfactory-opendox), on instance topology: **one instance and one database
> per tenant, always.** Every domain-factory install brings its own descendant
> instance (`MedxDox`, `codexDox`, …) and its own database inside the tenant,
> whether Opensoft operates it (the runbook's Case A) or the tenant does (Case
> B). No cross-tenant data ever shares a store. Rejected: a shared
> multi-tenant openDox with row-level isolation; a per-tenant default with a
> pooled option for operator-hosted tenants.

**RULING Q4** — comment `5542823211`, 2026-09-04T15:34:03Z:
> RULING Q4 — Brett Heap, 2026-09-04T15:34Z, in session (lane
> openxfactory-opendox), on the seam: **openDox defines a corpus-adapter
> interface; openXdox implements it.** openDox declares how documents are
> listed, read, written back and checked, with no knowledge of OpenSpec or
> doc-health; openXdox implements that interface over openxFactory's corpus
> and check families. The two back-imports from `scripts/doc_health/` into
> `ideation_dashboard.boundary` (`derive_possibles.py`,
> `ideation_readiness.py`) move into a small neutral module both sides depend
> on. The dependency points ONE way: openXdox depends on openDox, never the
> reverse. Rejected: openDox pinning doc-health as a library (inverts the
> layering); openXdox as a tuned copy with no shared interface (divergence,
> fixes land twice).

**DIRECTION Q5** — comment `5542993375`, 2026-09-04T15:48:18Z:
> DIRECTION Q5 — Brett Heap, 2026-09-04T15:48Z, in session (lane
> openxfactory-opendox), on the module split, verbatim:
>
> > "we want to make openDox useful on its own, it shoudl be able to still
> > manage docs and do brainstorming and connect to notebook lm. it is domain
> > neutral and external from openXfactory. we need to make sure openXfactory
> > brings in the core machinery to map to domains. we need to think how a
> > patient managment and research maps to the openXdox. and how a finacial
> > simulations or accounting questions would map in ledgerXfactory. same for
> > marketing analysis in adXfactory. what is core to these that we pull out
> > and put in openXdox. and what can pull up to openDox that does not rely on
> > openXfactory. and what do we need to try to pull from openXdox to openDox
> > to make openDox more useful as a braintorming and reserch analysis tool. a
> > student could use openDox or a lab assistant. so we want that to still be
> > useful on its own"
>
> What this settles (a THREE-layer test, not a two-way split):
> 1. **openDox** must be useful alone to a student or a lab assistant: manage
>    documents, brainstorm, research analysis, NotebookLM connection.
>    Domain-neutral and external to openxFactory. The test for a module: would
>    someone with no notion of factories, gates or tenants use it? Then it
>    belongs here — and the brainstorm must actively look for what to PULL UP
>    from today's dashboard into openDox to make it a better brainstorming and
>    research-analysis tool.
> 2. **openXdox** holds the core machinery openxFactory brings to map a domain
>    onto the workbench — what is COMMON to how MedxFactory (patient
>    management and research), LedgerxFactory (financial simulations,
>    accounting questions) and AdxFactory (marketing analysis) would each map.
>    The brainstorm must work those three mappings explicitly and extract the
>    common core.
> 3. **Descendants** (`MedxDox`, `LedgerxDox`, `AdxDox`, `codexDox`) hold the
>    domain-specific mapping.
>
> The per-module assignment is therefore design work under this test, carried
> by the brainstorm set and the staging topic, not ruled here module by
> module.

**RULING C1** — comment `5544359573`, 2026-09-04T17:46:23Z:
> RULING C1 — Brett Heap, 2026-09-04T17:46Z, in session (lane
> openxfactory-opendox), on the recorded conflict "which openDox is dead":
> **the collision is accepted knowingly; the repository is
> `opensoft/openDox`.** Amendment 3 to `docs/openxdox-naming.md` records the
> measured facts — six GitHub repositories carry the name, and the GitHub
> organization `opendox` belongs to an unrelated Amazon-analytics project —
> and Brett's acceptance of them; no claim is made on the organization name;
> the brand lives under `opensoft`. Which specific abandoned repository
> prompted the word "dead" is immaterial to the record. Rejected: citing a
> specific dead repo as the basis; reconsidering the name (the `openXnotes`
> fallback stays documented, unused).

**RULING C2** — comment `5544370242`, 2026-09-04T17:47:26Z:
> RULING C2 — Brett Heap, 2026-09-04T17:47Z, in session (lane
> openxfactory-opendox), on the recorded conflict "what is openXdox":
> **openXdox is the domain-mapping core, parameterized.** It holds what every
> domain factory shares — typed artifact kinds, a governed lifecycle engine
> (statuses, gates, roles, evidence) and the dispatch/apply lane —
> parameterized by a domain profile that a descendant supplies. Engineering
> vocabulary ("requirement", "OpenSpec change", the doc-health check families)
> belongs to the engineering descendant `codexDox`, or stays in openxFactory
> as its own adapter over the corpus-adapter interface; a clinician using
> `MedxDox` never sees the word "requirement". This resolves the founding
> words "openDox tuned for openxFactory" as: tuned for the xFactory FAMILY's
> way of mapping domains, not for openxFactory's engineering corpus
> specifically. Rejected: openXdox as today's dashboard minus the pull-ups
> (every descendant would inherit engineering vocabulary); one repo with two
> packages (a boundary that is only a package line).

**RULING C3** — comment `5544381563`, 2026-09-04T17:48:32Z:
> RULING C3 — Brett Heap, 2026-09-04T17:48Z, in session (lane
> openxfactory-opendox), on the recorded conflict "the standalone student
> under Q1": **standalone openDox creates and manages a plain local git
> repository per project.** Documents are always git-backed; commits are the
> write path; a remote can be attached later. Q1 holds unchanged (the database
> never holds documents), and moving a student or lab-assistant project into a
> governed factory is a push, not a migration. Rejected: a loose-documents
> mode with the database holding content until a repository is attached;
> requiring a repository before the first save.

**RULING Q6** — comment `5544396528`, 2026-09-04T17:49:58Z:
> RULING Q6 — Brett Heap, 2026-09-04T17:49Z, in session (lane
> openxfactory-opendox), on sequencing against the five active
> `ideation-dashboard` changes: **freeze the dashboard now and carve
> immediately.** The five active changes (`add-composed-view-authoring`,
> `add-doxchat-model-intake`, `add-lens-document-selection`,
> `add-nightly-dashboard-refresh`, `retire-doxbench-chat-turn-v1`) stop where
> they stand in openxFactory; their live deltas and open tasks (20 across the
> two with open archive gates) are RE-HOMED into the extraction change and the
> new repositories as part of the carve. No new dashboard change opens in
> openxFactory. The lane's recommendation (let the five finish in place, carve
> after the two gated ones archive) was put and NOT taken; the cost accepted
> is re-homing 20 open tasks and the never-green nightly-refresh lane
> mid-flight.

**RULING Q7** — comment `5544413838`, 2026-09-04T17:51:36Z:
> RULING Q7 — Brett Heap, 2026-09-04T17:51Z, in session (lane
> openxfactory-opendox), on ownership, visibility and license: **`opensoft`
> owns both repositories; both are PUBLIC from day one under Apache-2.0**,
> matching the three public product repos (`openChart`, `openPractice`,
> `openRepoShape`). Descendants (`MedxDox`, `codexDox`, …) follow their domain
> repositories' visibility. Rejected: openXdox private until the descendants
> prove the boundary; MIT or AGPL-3.0.
>
> **All questions the staging topic carried are now ruled: Q1–Q7 and conflicts
> C1–C3.** The topic's exit path (an OpenSpec change on the
> `split-openxwallet-repo` shape, adapted to a two-repo, non-byte-identical
> extraction that also re-homes the five active `ideation-dashboard` changes
> per Q6) is unblocked.
>
> CLAIMED — lane openxfactory-opendox, session 01TF54UA1RBYrVC8E677z6zm,
> 2026-09-04T17:51Z, for (a) recording these dispositions in the staging
> fragment + INDEX row (doc slice, now) and (b) authoring the OpenSpec change
> that exits the topic (proposal/design/tasks/deltas; Amendment 3 to the
> naming record rides with it). No repository is created and no code moves in
> (a) or (b); creation and the carve are that change's realization after
> ratification. Stale after 4h with no PR.

**RULING DQ-1** — comment `5547049745`, 2026-09-04T22:14:35Z:
> RULING DQ-1 — Brett Heap, 2026-09-04T22:14Z, in session (lane
> openxfactory-opendox), on PR #666's design question "where does
> openxFactory's own engineering adapter live": **openxFactory keeps its own
> adapter.** doc-health and OpenSpec stay in openxFactory, and a small adapter
> package beside them implements the corpus-adapter seam; `codexDox` becomes a
> thin descendant that pins openXdox and reuses that adapter. Consequences for
> the packet: the 15 engineering-vocabulary rows in the successor map stay in
> openxFactory (not codexDox); openxFactory sheds the dashboard first (tasks §
> 5) and the first descendant follows (§ 7). Rejected: codexDox owning the
> adapter and the 15 rows, with the shed waiting on the descendant.

**RULING OQ-1** — comment `5547060378`, 2026-09-04T22:15:49Z:
> RULING OQ-1 — Brett Heap, 2026-09-04T22:15Z, in session (lane
> openxfactory-opendox), on PR #666's open question "what replaces the
> byte-identical floor": **the four-part floor.** (1) A mapping manifest
> listing every source path to its destination with per-file digests at the
> cut, plus a CLOSED list of permitted edit classes (import rewrites, path
> constants, adapter calls); (2) test counts that must sum across the three
> repositories; (3) a neutral conformance corpus every destination passes; (4)
> a snapshot-equivalence run proving the new stack renders the same dashboard
> snapshot as the old. Rejected: manifest-with-digests only (proves files
> moved, not behaviour); snapshot-equivalence only (a dropped module without
> test coverage goes unnoticed).

**RULING OQ-2** — comment `5547067574`, 2026-09-04T22:16:38Z:
> RULING OQ-2 — Brett Heap, 2026-09-04T22:16Z, in session (lane
> openxfactory-opendox), on PR #666's open question "may a governed consumer
> pin openDox directly": **No. Inside the xFactory family there is ONE chain:
> openDox is pinned only by openXdox, and every domain descendant pins
> openXdox.** The mapping core is never bypassed; one consumption shape to
> validate. Anyone outside the family uses openDox freely as open source —
> this ruling governs the pin chain only. No third MODIFIED requirement is
> added to `neutral-product-pin`. Rejected: a direct pin for docs-only
> installs; deferring to the first request.

**RULING OQ-3** — comment `5547107565`, 2026-09-04T22:21:31Z:
> RULING OQ-3 — Brett Heap, 2026-09-04T22:21Z, in session (lane
> openxfactory-opendox), on PR #666's open question "does the
> document-lifecycle taxonomy become parameterized now": **no delta now.**
> `document-lifecycle` stays openxFactory's governance vocabulary, exposed
> through its own adapter (DQ-1); descendants declare their own lifecycles via
> the `domain-mapping-declaration` capability this change adds. Revisit when
> the first non-engineering descendant (`MedxDox`) shows what a clinical
> lifecycle needs. Rejected: parameterizing in this change (a third writer on
> a spec two active changes hold); a named successor change filed now.
>
> **All four questions PR #666 put for the ratification read are now ruled
> (DQ-1, OQ-1, OQ-2, OQ-3).** The packet is being updated to encode them;
> ratification of the proposal itself is Brett's separate word.

**RULING — RATIFICATION** — comment `5548470629`, 2026-09-05T01:38:15Z:
> RULING — RATIFICATION — Brett Heap, 2026-09-05T01:38Z, in session (lane
> openxfactory-opendox, session 01Ku6jmLxwesiWs4bQwRS3c4), on PR #666
> `change/split-opendox-two-layer-product` at head 6935fb8b: **"ratify
> #666"**.
>
> The extraction proposal `split-opendox-two-layer-product` is RATIFIED as it
> stands at 6935fb8b, with every ruling on this record (Q1–Q7, C1–C3, DQ-1,
> OQ-1..3) already encoded in the packet. Acts that follow, in order: (1) flip
> `proposal.md` to `Status: ratified` and add
> `review/ratification-2026-09-04.md` quoting the rulings here; (2) Rule 6
> LANDING of #666 into openxFactory main (admin merge on this word — PR is
> brettheap-authored and cannot self-clear the code-owner review); (3)
> realization by tasks groups, each its own Speckit feature/PR, starting with
> the corpus-adapter seam. Realization is NOT started in this window (budget
> breakpoint); the handoff carries it.

**One transcription note, recorded rather than silently corrected.** That
comment names the record it asks for as `review/ratification-2026-09-04.md`.
The word was given at 2026-09-05T01:38Z UTC and the decision date is
2026-09-05, so the record carries the date of the act:
`review/ratification-2026-09-05.md`. Nothing else about the instruction is
read differently.

## Review history

**Stated truthfully rather than flatteringly: no council round and no
adversarial round ran on this packet.** What ran was Copilot's reviewer and
Brett's own reading across the recorded rulings, and that is the whole of it.

1. **Sourcery** — 2026-09-04T20:05:30Z, commit `40ecda2b`. Not a review: the
   provider replied that a private repository has no Sourcery access, the
   standing upsell stub this repository already knows.
2. **Copilot errored three times, provider-side** — 20:06:15Z (`40ecda2b`),
   20:07:53Z (`9386a039`) and 20:19:14Z (`ec35f71f`), each returning
   "Copilot encountered an error and was unable to review this pull request."
   No findings; no review content of any kind.
3. **Copilot round 4** — 22:45:16Z, commit `b21d8afe`, 🟡 *Changes
   recommended*, 12/13 files reviewed, **3 comments**. All three were
   record-consistency defects in bookkeeping surfaces, and all three were
   TAKEN at `6935fb8b` ("Take Copilot's three findings: two records still
   described a packet with open questions"): an orphaned "The" breaking a
   README paragraph; the INDEX row's short "Moved by" summary still saying
   "possibly MODIFIED `document-lifecycle` + `governed-derived-model`" after
   OQ-3 had ruled otherwise; and `.openspec.yaml` still saying "the three
   carried open questions are DECLARED, not decided" when the packet carries
   four, all ruled.
4. **Copilot round 5** — 23:07:26Z, over commit `6935fb8b` — the RATIFIED
   BASELINE — 🟡 *Changes recommended*, **1 comment**: `tasks.md` § 0.9 said
   "No MOVEMENT LOG entry is owed" while the seeding commit `9386a039` had in
   fact written one, because it moved TEN ledger rows and not one (this
   change's own row in, plus nine ARCHIVED rows flipping `sole` →
   `co-modifier`, which is not legible from the row diff alone). **That
   finding was still open at the moment of ratification and is TAKEN IN THIS
   ACT** — § 0.9 now states that a MOVEMENT LOG entry IS owed and is written,
   with the ten-row arithmetic. It corrects a false sentence about this
   packet's own bookkeeping; it moves no ruling, no requirement and no row of
   the successor map.
5. **Copilot round 6** — 2026-09-05T01:51:12Z, over the caught-up head
   `b68a4e92`, 🔵 *Needs a closer look*, **0 new comments**. Its stated reason
   is that the packet "requires careful human ratification for correctness and
   downstream implications" — which is what had happened thirteen minutes
   earlier.
6. **Codex was never requested.** Its quota was exhausted for this account and
   asking would have produced a refusal, not a review. Recorded as an absence,
   not as a silence to be read as assent.
7. **Brett Heap reviewed in session**, across the recorded rulings: eleven acts
   on 2026-09-04 before the packet existed or while it was being authored
   (the founding ruling, Q1–Q4, DIRECTION Q5, C1–C3, Q6, Q7), then the FOUR
   questions the packet itself put — DQ-1, OQ-1, OQ-2, OQ-3 — all ruled the
   same evening between 22:14Z and 22:21Z, before ratification. The
   ratification read was over the 102-row successor map and not only the
   doctrine (`tasks.md` § 0.2). **No row was contested.**

**One measured correction is taken in this act alongside the § 0.9 fix.**
`proposal.md` § New Capabilities said `corpus-adapter-seam` carries "13
scenarios"; the delta file carries **11** (counted `#### Scenario:` headings at
this head). The count is corrected to 11. It is a measurement, not a decision,
and it follows the house practice of re-measuring a stale count rather than
carrying it (`9e869acc`, 2026-09-05, on the pin's divergence paragraph).

## Ordering facts

- **`opensoft/openxFactory#659` MERGED FIRST** — 2026-09-04T17:39:35Z, squash
  commit `bca340b9`: the brainstorm set and the staging topic
  `opendox-two-layer-product` this packet exits.
- **`opensoft/openxFactory#661`** — merged 2026-09-04T18:48:06Z, squash commit
  `31cb5011`: Brett's 2026-09-04 rulings recorded as dispositions on the
  staging fragment. Both preconditions the topic's Exit section named (Q6 and
  Q7) were met there, which is what unblocked authoring.
- **`contract-v3.4` landed mid-authoring**, at `807a4f47` (PR #653). That is
  the reason `target_release:` names the next **MAJOR** and deliberately does
  NOT number it: § Version Identity forbids reserving a number before merge
  order is known, and what cuts next depends on what else cuts first.
- **The five frozen changes archive BEFORE this one.** The archive order runs
  the OPPOSITE way from the promoted sibling rule: a sibling `## MODIFIED`
  block promoting into a removed capability would be reported forever as a
  requirement present after its ratified removal. `tasks.md` § 8.5 gates on
  all five being dispositioned, with `retire-doxbench-chat-turn-v1` archived
  in `openxFactory` on its own evidence first. **This change archives LAST.**
- **Two catch-up merges of `origin/main` happened AFTER the word**, and both
  are re-validations rather than re-decisions: `b68a4e92` (2026-09-05T01:48Z,
  bringing the branch to 0 behind main) and `e92daabe` (this act, merging the
  eleven commits main gained after that, including `add-release-tag-gate`'s
  ratification and realization at `7ee0e73d`). One README conflict, in the
  "OpenSpec Records" list where both lines had added an entry at the same
  position; resolved by KEEPING BOTH entries. No packet file conflicted and no
  ratified byte moved.
- **Rule 7 substrate**: rows 2 (`tests/sequenced_after/corpus-ledger.yaml` plus
  the MOVEMENT LOG) and 3 (README "OpenSpec Records") are claimed by this
  packet on issue #630. **Row 1 — the codexFactory review-authority floor — is
  NOT claimed now**: this packet adds and removes no path under
  `openspec/specs/`, and the floor's runbook says DE-FLOOR BEFORE YOU REMOVE,
  so it is claimed at realization (`tasks.md` § 5.6, gated at § 8.4).

## What ratification authorizes

`tasks.md` groups 1–8, each a Speckit feature on the convener's standing rule
that **OpenSpec ratifies the boundary and Speckit builds it**. Ratification
authorizes every one of them and PERFORMS NONE of them:

1. **Repository bootstrap** — two repositories, PUBLIC, Apache-2.0,
   `opensoft`-owned (RULING Q7).
2. **The seam, landed INSIDE `openxFactory` before anything moves** — the
   neutral module that breaks the two-way `doc_health` ↔ `ideation_dashboard`
   import, the adapter's operations, the `serve.py`/`cli.py` extension points.
3. **The openDox carve**, with the mapping manifest.
4. **The openXdox mapping core.**
5. **`openxFactory` consumes and sheds; the MAJOR is cut.** BREAKING, one
   atomic pull request, de-floored first.
6. **Re-home the five frozen changes** (RULING Q6).
7. **The first descendant** — a task carrying a RULING CHECKBOX, not a
   decision.
8. **The archive gate** — merged plus green realization evidence, one evidence
   line per part of the four-part floor.

Group 0 is this packet's own bookkeeping. Its § 0.6 GATE — `ideation-intent-
plane` reaching canon, or its non-promotion RECORDED — gates § 3 onward and not
this ratification.

## What this ratification does not do

- **It creates no repository.** `opensoft/openDox` and `opensoft/openXdox` do
  not exist and are not created by this act.
- **It moves no code and no contract byte.** Nothing outside `openspec/`, the
  staging INDEX and the README changes in this packet's own diff.
- **It promotes and removes no capability.** The REMOVED block over the 102
  `ideation-dashboard` requirements takes effect when this change ARCHIVES,
  which is gated on merged-plus-green evidence across the affected
  repositories and on all five frozen siblings being dispositioned first.
- **It does not edit `docs/openxdox-naming.md`.** Amendment 3's text is
  DRAFTED at `design.md` § D8 and APPLIED in the pull request that creates the
  repository — amending a `ratified` record ahead of the act it describes would
  leave the record describing a repository that does not exist.
- **It does not land the pull request.** The Rule 6 landing of #666 is a
  separate act on the same word.
- **It does not reopen the rulings.** Q1–Q7, C1–C3, DQ-1 and OQ-1..3 were
  constraints on the packet, not questions in it; a reviewer may contest how
  the packet CONSTRUCTS them, and ratification does not reopen them.
- **It does not decide the per-requirement map by authority.** The map is a
  READING; each row carries its own reason so it can be contested individually
  at realization without reopening the split.

## Residuals carried

Two, both recorded in the ratified text rather than resolved, and neither a
question the packet needed answered to be ratified:

- **The pre-governed scratch space** (`design.md` § D5). RULING Q1 rejected the
  hybrid where ideas live in the database until promoted, so an idea is a
  governed document in git from its first save — consistent, and heavier than a
  lab assistant may want. Whether openDox needs a scratch space that is NOT "a
  draft of a document" is a real residual, and it is recorded rather than
  resolved.
- **The front end's absent package boundary** (`design.md` § D3). The web tier
  is 40 files and 30,410 lines with NO package boundary at all today, so its
  boundary must be INVENTED rather than discovered — and it was not measured
  for this split. `tasks.md` § 3.4 makes the front-end boundary its own task
  rather than a consequence of the Python one.

Both survive ratification untouched.

## The one thing this act broke, and how it was fixed

**`tests/doc-health/test_modified_block_currency_self_gate.py::
test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
FAILED on the flip, and it was RIGHT to.** That file is the self-gate: it
asserts, by NAMED SUBJECT, every row the `modified-block-currency` family draws
over this checkout, and it had asserted the two-writers ordering class as an
EMPTY band. Ratifying this packet made it the second ACTIVE RATIFIED writer of
`neutral-product-pin`'s *An external neutral product is pinned by commit and
digest, never by tag*, so the arm — which returns early below two ratified
writers — began reporting, and the empty band failed.

**Fixed the way the gate's own failure message prescribes, not by loosening
it.** `_ORDERING_SUBJECTS` is a NAMED EXACT SET of the two subjects, compared
with `==` and never `<=`, on `_LEDGER_SUBJECTS`' and `_PAIRING_SUBJECTS`'
discipline, with both directions failing by name and its own retirement
condition written down: the rows go when the ordering declaration is made or
when either change archives, and when they go the carriage ledger is where the
divergence surfaces next. `_ORDERING_TITLE` is the fifth regex this gate owns —
declared, explained, and proven by the guard's own structural probe to be a
read of the family's own sentence rather than a parser of requirement
structure; a widened `_TITLE` was the alternative and was rejected because
`_subject` feeds two other exact sets that must not silently start collecting
this arm's findings. The test's docstring and
`specs/021-modified-block-currency-self-gate/contracts/self-gate-contract.md`'s
row for it are amended rather than left stating a zero that is no longer true.
The function keeps its name: it is pinned in that contract and in two archived
packets, and a rename would move more text than the fact does.

**No other test moved.** The whole self-gate file is green (19 passed), and the
carriage-ledger, pairing and collision exact sets are untouched — the flip
added no `info` finding and retired none.

## Verification (at the pushed head, this act)

Run in the branch worktree after the catch-up merge of `origin/main` and the
ratification edits.

- `OPENSPEC_TELEMETRY=0 openspec validate split-opendox-two-layer-product
  --strict`: **valid**, zero issues.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: **91 passed, 0
  failed** (91 items; 90 before `add-release-tag-gate` landed on main and the
  merge brought it in).
- `python3 scripts/proposal-support.py . verify`: **proposal support
  verification ok**.
- `python3 -m pytest -q`: **THE SUBSET PATH, and it is said rather than
  implied.** The full suite does not finish in eight minutes on this host —
  five other sessions were running pytest concurrently and two attempts at the
  whole suite reached 28% and 5% before being stopped — so the modules that
  read `openspec/changes/*/proposal.md` were run directly, plus
  `tests/sequenced_after`: `tests/sequenced_after tests/doc-health
  tests/proposal-support tests/credential_contracts tests/notebooklm
  tests/scope_globs` — **2319 passed, 0 failed, 39 subtests passed**, 5m54s.
  The one module that reads `proposal.md` and is NOT in that list is
  `tests/ideation-dashboard` (3,927 test functions, 52% of this repository's
  suite); it is covered by the required `pytest-suite` check on this head, and
  the pull-request comment records that check's verdict.
- **Doc-health**, `python3 scripts/doc-health.py --single-repo <tree>`, this
  tree against a fresh detached worktree of `origin/main` (`9e869acc`):

  | | critical | error | warning | info |
  | --- | --- | --- | --- | --- |
  | `origin/main` `9e869acc` | 6 | 6 | 30 | 13 |
  | this tree | 6 | 6 | **32** | 13 |

  **The delta is +2 `warning`, one family, and it is NOT zero — stated plainly
  rather than rounded to "no regressions".** Both are
  `modified-block-currency`, resolution class `contested`, and both are the
  SAME finding reported against each of the two blocks it concerns: *the
  ordering of MODIFIED blocks for 'An external neutral product is pinned by
  commit and digest, never by tag' is undecided: `add-openspec-cli-pin`,
  `split-opendox-two-layer-product` — neither names the other*. **THE FLIP
  ITSELF IS THE CAUSE, and the cause is lawful.** That arm scopes to ACTIVE
  RATIFIED writers (`modified_block_currency.py`: `ratified = [...]`, `if
  len(ratified) < 2: return`), so at `b68a4e92` — this packet still `draft` —
  the group held ONE ratified writer and reported nothing; ratifying this
  packet makes it the second. `add-openspec-cli-pin` ratified 2026-09-04 and
  landed as #667 AFTER this packet's own sibling check was taken at
  `a858e5b0`, which is why the delta's preamble said no active change carried
  a delta on this capability. That measurement is now DATED IN PLACE rather
  than left standing as a false claim, and the ordering declaration it now
  owes is named as OWED and deliberately NOT made in this act:
  `release-realization`'s *Ordered deltas and branch vocabulary* puts the
  declaration in the later writer's proposal, and choosing which of two
  ratified siblings carries the other's additions to that requirement is a
  decision, not a bookkeeping correction to a ratified delta.
  **No other family, severity or count moves — the `info` row included.**
- The one `error` this tree carries that `b68a4e92` did not
  (`release-inventory-drift`) is inherited from `origin/main`, which reports
  it identically; the catch-up merge brought it in and this packet neither
  causes nor cures it.

## Next

1. **The Rule 6 LANDING of `opensoft/openxFactory#666`** — a separate act on
   the same word, admin-merged because the pull request is
   `brettheap`-authored and cannot self-clear the code-owner review. Not
   performed by this record.
2. **The ordering declaration owed on `neutral-product-pin`** — one of
   `add-openspec-cli-pin` and `split-opendox-two-layer-product` names the
   other in its own `proposal.md`, which is what decides which block is
   measured against the other's outcome. Until it is made, the two contested
   warnings above stand and this record is their citation.
3. **Realization by `tasks.md` groups**, each its own Speckit feature,
   starting with **§ 2, the corpus-adapter seam landed INSIDE `openxFactory`**
   — the ratification comment's own sequencing, and the only order in which
   the two-way `doc_health` ↔ `ideation_dashboard` import is broken before
   anything moves.
4. **§ 0.6's GATE before § 3 onward** — `ideation-intent-plane` reaches canon,
   or its non-promotion is RECORDED under `document-lifecycle`'s
   deliberate-non-promotion scenario.
5. **Archive LAST**, per `tasks.md` § 8: merged plus green realization
   evidence, all four parts of the RULED floor evidenced separately, all five
   re-homed siblings dispositioned, and the codexFactory floor DE-FLOORED
   BEFORE the removal.
