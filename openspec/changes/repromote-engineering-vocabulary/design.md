# Design: repromote-engineering-vocabulary

Status: draft
Authored: 2026-09-16, lane `openxfactory-4` (display `openXfactory-4-openDox_extraction`), actor
`substrate52a`, against a fresh clone of `main` at `fa39141c`. Every count below was produced by a
script over that tree and is reproducible from it; none is read off prose.

**EVERY `design.md`/`tasks.md`/`proposal.md` CITATION BELOW IS THE GOVERNING PACKET'S, NOT THIS
ONE'S**, and each is written with its full path the first time it is used;
`openspec/changes/split-opendox-two-layer-product/` is meant wherever a bare `tasks.md § …` or
`design.md § D…` appears after that.

Governing text, in the order it binds: **RULING DQ-1** (`opensoft/openxFactory` issue #656,
2026-09-04T22:14Z, comment `5547049745`) · **RULING OQ-1** (22:15Z, comment `5547060378`, the CLOSED
edit-class list) · `split-opendox-two-layer-product` `tasks.md` **§ 5.2a** (:1527-1535) and **§ 2.2a**
(:661-676) · `design.md` **§ D1** (:167-199) and **§ D2** (:212-258) · the packet's ratified
`specs/ideation-dashboard/spec.md`, the per-requirement map (ratified 2026-09-05T01:38Z, record
`review/ratification-2026-09-05.md`).

## D1 — THE ID IS DERIVED, AND HERE IS THE DERIVATION

**`openxfactory-engineering-adapter`**

`tasks.md` § 5.2a says the successor capability's *"id this task authors"* and says nothing else about
it, so the id is read off what the packet CALLS the thing, not off preference.

| measured at `fa39141c` | what it names the adapter |
|---|---|
| the ratified per-requirement map, **15 of 15** openxFactory rows, identical phrasing (`openspec/changes/split-opendox-two-layer-product/specs/ideation-dashboard/spec.md`) | *"openxFactory's OWN ENGINEERING ADAPTER, the small package beside `scripts/doc_health/` that implements openDox's corpus-adapter seam (RULING DQ-1)"* |
| the governing packet's `design.md` § D3 column head (`openspec/changes/split-opendox-two-layer-product/design.md`:290) | *"`openxFactory`'s OWN ENGINEERING ADAPTER — the engineering mapping"* |
| the governing packet's `design.md` § D1 topology block (`openspec/changes/split-opendox-two-layer-product/design.md`:172) | *"its OWN engineering adapter, one conformant implementation of openDox's seam"* |
| the governing packet's `proposal.md`, clause (9) (`openspec/changes/split-opendox-two-layer-product/proposal.md`) | *"a small ENGINEERING ADAPTER PACKAGE beside `scripts/doc_health/`"* |
| the governing packet's `tasks.md` (`openspec/changes/split-opendox-two-layer-product/tasks.md`:1248, :1356) | *"openxFactory's own engineering adapter"* · *"that DQ-1 ENGINEERING ADAPTER"* |
| bigram count over the whole packet | **"engineering adapter" 22** · "engineering mapping" 1 · "corpus adapter" used as ITS name **0** |
| the LANDED § 2.2a package (#725 → `ea4e6ff2`) | directory `scripts/corpus_adapter_openxfactory/`; sole public class `OpenxFactoryCorpusAdapter`; tests `tests/corpus-adapter/` |
| the LANDED § 4.4 profile (#984 → `a1ef886f`) | `contracts/domain-profiles/openxfactory-engineering.yaml`, `mapping_id: openxfactory-engineering` |

**Head noun — `engineering-adapter`** — because that is the packet's own name for it, 22 times, and
because "engineering" is the one word RULINGS C2 and DQ-1 both turn on (*"a clinician using `MedxDox`
never sees the word 'requirement'"*).

**Qualifier — `openxfactory-`** — because `corpus-adapter-seam`'s fourth requirement, *"openxFactory's
own adapter is one implementation and carries no privileged path"*, is made LOAD-BEARING by DQ-1
(§ 2.2a's own words: *"which this ruling makes load-bearing"*). An unqualified `engineering-adapter`
would read as the NEUTRAL capability. The neutral one is openDox's under RULING Q4 and is not this,
and the whole point of DQ-1 is that this adapter is ONE implementation among others.

**Spelling — lowercase solid, kebab-joined** — not a choice either: both landed machine names spell it
that way (`corpus_adapter_openxfactory`, `openxfactory-engineering`), and a capability id is kebab-case
by house convention. Proper-noun-qualified ids are conventional here where the named thing IS the
subject: `medxchart-overlay-boundary`, `medxpractice-overlay-boundary`, `omnigent-install-manifest`,
`hermes-domain-overlay`.

**Rejected, each with its reason.**

* `corpus-adapter-seam` — openDox's, under RULING Q4 (*"Q4 gives the INTERFACE to openDox"*), and
  unpromoted in this corpus. Re-using it here would put this repository's own mapping inside the
  neutral standard it consumes.
* `engineering-adapter` — drops the qualifier requirement 4 makes load-bearing.
* `corpus-adapter-openxfactory` — mirrors the package DIRECTORY but inverts the ratified phrase's word
  order and buries "engineering".
* `openxfactory-engineering` — already in use as a `domain-mapping-declaration` mapping id; a
  capability sharing it would collide in a reader's eye and in every grep.

**Collision check at `fa39141c`**: 62 capabilities under `openspec/specs/`, none of them this;
`grep -rI "openxfactory-engineering-adapter"` over the tree returns **0** hits.

## D2 — SIX PATH LITERALS, TWO OF WHICH A SEAM OPERATION ANSWERS FOR — AND THAT IS THE FINDING

`tasks.md` § 5.2a: *"The only edit they take is re-expressing path literals as `adapter calls` — one
of RULING OQ-1's three classes, by name."* So the census comes first, and it is complete: of the 49
distinct backticked tokens in the fifteen, SEVEN are candidates — and only FOUR of the seven are
path literals, in four requirements, at SIX occurrences. The other three are classified out below
with their reasons (`proposal.md` is a document's identity, `OPENXFACTORY_ROOT` an operator
override's name, `main` a git ref), and they are named rather than dropped so the census can be
checked against the tree.

**NARROWED AFTER MEASUREMENT, AND THE NARROWING IS THE POINT.** This packet first re-expressed six
occurrences. An automated review contested two of them and, separately and more sharply, the
existence semantics of a third; both objections are CORRECT against the interface's own text, and
the packet was narrowed to what the seam can actually answer rather than argued into place. **The
finding stands on the record for § 3.7 and § 5.4 and for openDox, which owns the interface under
RULING Q4: four of the six path literals in the fifteen name a question the six-wide seam does not
answer as the requirement states it.**

### The two edits — both `resolve`, both in *doxBench resolves its released contract from the checkout it runs in*

| # | OLD (promoted) | NEW (here) |
|---|---|---|
| 1 | ``then the existing walk up to an aggregation-relative `openxFactory/` `` | ``then the corpus adapter's `resolve` of the aggregation-relative home corpus`` |
| 2 | ``the hosting repository is a publisher release and an aggregation-relative `openxFactory/` checkout also exists`` | `the hosting repository is a publisher release and an aggregation-relative home corpus the adapter could resolve also exists` |

These two are unambiguous: the governing `design.md` § D2 names `resolve` for exactly this literal —
*"**resolve** (given a corpus reference, which checkout and which revision — the operation
`corpus_root.py` performs today with a path literal)"* — and the requirement's whole subject is a
resolution ladder. Every rung survives, including the `OPENXFACTORY_ROOT` override; what changes is
which side of the seam holds the directory's name. The adapter already holds it:
`scripts/corpus_adapter_openxfactory/home.py` carries `REPO_ROOT`, `PROMOTED_ROOT = "openspec"` and
`OBLIGED_PREFIX = "ideation/"`, and its own docstring names `home.py` *"the only module naming the
home layout"*.

### The four recorded NON-edits, each with the operation it would have needed

| occurrence | requirement | why no adapter call answers for it |
|---|---|---|
| ``ideation/staging/`` (scenario *A missing topic is refused*) | Staged-topic proposal commissioning | The question is a topic's EXISTENCE. `list_documents` lists documents under a DECLARED scope; the home adapter declares `documents` and `lifecycle` (`home.py`), not a staging-topic scope, and the interface's own docstring insists *"an empty corpus is a legal `()` and must stay distinguishable from an unreadable one"* — so listing-emptiness cannot distinguish an ABSENT topic from an EMPTY one, which is precisely the distinction this scenario turns on. Re-expressing it through `list_documents` would state a refusal the seam cannot make. |
| ``ideation/staging/<topic>/`` | Accepted-possible promotion to staging | It names the DESTINATION of authoring the console explicitly must not perform (*"the console MUST NOT author the fragment"*). No seam operation is invoked at that word: `write_back` is a dispatch of a proposed document and this is a `workflow-job` commission. |
| ``openspec/`` ×2 (body and scenario) | Demote refreshes a staged topic's outline… | Both sit inside a STATUS rule about documents a demote returns. No read and no write happens there, so no operation answers; `PROMOTED_ROOT` is the adapter's implementation datum and not a call, and naming it in canon would state an implementation detail where the requirement states an obligation. |

**AND TWO FURTHER NON-EDITS, for completeness of the census.**

* ``proposal.md`` (×4, requirement 11) is a DOCUMENT'S OWN IDENTITY, not a location. The seam's
  `read` returns *"the bytes of one document"* against a `DocumentId` whose `key` is declared OPAQUE
  (`scripts/corpus_adapter.py`:213-224 — *"a consumer may compare it, sort it and hand it back, and
  may not parse it"*), and `classify` answers *"what KIND is this document"*. Naming WHICH document a
  refresh reads survives the seam untouched.
* ``OPENXFACTORY_ROOT`` (×3, requirement 10) is an OPERATOR OVERRIDE's name and a rung of the very
  precedence ladder that requirement exists to state. `CorpusRef.location` is *"opaque here; the
  implementation interprets it"*, so the override is what a caller PASSES rather than a layout the
  reader walks. Deleting the rung's name would delete requirement content.
* (``main``, ×1, requirement 1 — *"a main-resident cleanup record"* — is a git ref, not a path.)

**WHAT WOULD UNBLOCK THE FOUR**, named so the next box does not have to rediscover it: a scope the
corpus DECLARES for staged topics (`ResolvedCorpus.scopes` is return data, so a home adapter may
declare one without widening the six), or an existence-capable answer that keeps *absent* and *empty*
apart. Both are openDox's to declare under RULING Q4 and neither is § 5.2a's to invent. `tasks.md`
§ 4.5 carries it as a BLOCKED box, in the shape § 6.1's and § 6.5's closures used for the same class
of "named, not performed" work.

**THE CARRY IS PROVED, NOT ASSERTED.** The delta is built by
`review/build-delta.py`, committed INSIDE this packet so the proof is reproducible from this checkout
alone: the fifteen are selected by the destination the ratified map names, lifted from the promoted
spec BY TITLE (never by line), each declared edit must match EXACTLY ONCE or the build aborts, and
the build then REVERSES every edit and asserts byte equality against the promoted text. Measured:
**102 promoted requirements; 71/16/15 map; 15 carried; 49,829 source bytes; 84 scenarios; 2/2 edits
matched once; reversal proof passes.** Re-running it after any merge from `main` re-proves the carry
against the moved base — which is how this packet stays current against **#1066**, the one open pull
request that edits `openspec/specs/ideation-dashboard/spec.md` (hunks at `:2249`, `:2267` and an
append after `:2590`; it touches none of the fifteen).

## D3 — WHY THIS PACKET AUTHORS NO SECOND `## REMOVED` BLOCK

The fifteen leave `ideation-dashboard`. This packet does not remove them from it, and the reasons are
three, any one of which is sufficient.

1. **THE REMOVAL ALREADY HAS A SINGLE, RATIFIED WRITER.** The packet's
   `specs/ideation-dashboard/spec.md` removes all 102 requirements with a per-requirement successor
   map, ratified 2026-09-05, and calls that map *"deliberately the change's largest artifact: it is
   what substitutes for the byte-identity floor the extraction cannot meet"*. § 5.2a's own sentence
   assigns this box the RE-PROMOTION (*"are re-promoted HERE … not shed"*), not the removal.
2. **A SIXTH WRITER WOULD BE AN UNDECLARED SIBLING COLLISION.** That delta carries a whole section,
   `## THE SIBLING COLLISION, DECLARED RATHER THAN PAPERED OVER`, enumerating the FIVE active changes
   that write `ideation-dashboard` and handling each. A sixth writer removing the same fifteen titles
   would have to be declared THERE — and amending the packet's ratified delta is not § 5.2a's box.
   The packet states the principle for the neighbouring case itself: of `ideation-intent-plane`,
   *"a second writer would be a collision this change does not need"*.
3. **IN ONE OF THE TWO POSSIBLE ARCHIVE ORDERS IT BECOMES A REMOVAL OF NOTHING.** If this packet
   archived first with such a block, the split packet's own rows for those fifteen titles would later
   apply against a promoted document that no longer holds them — *"a removal of nothing, and `openspec
   archive` would apply it against a document that never held the title"*, which is the packet's own
   stated reason for NOT removing the twelve sibling-added titles in its block (b).

**AND THE FIDELITY SENTENCE IS SATISFIED WITHOUT IT.** § 5.2a's mechanism is
*"`promotion_fidelity.py` keys on (capability, normalized title), so the successor is a distinct key
and the REMOVED delta stays visible to the checker"* — the visibility being of the PACKET's removal.
Verified in the checker's own text: `promotion_fidelity.py` builds `writers.setdefault((capability,
norm(req.title)), [])` and resolves a latest writer per (capability, requirement) pair. The
re-promotion under a different capability therefore cannot mask the removal, and does not have to
perform it.

**THE MECHANICAL CORROBORATION IS THIS PACKET'S OWN SWEEP ROW.** `tests/sequenced_after/corpus-ledger.yaml`
computes `class: sole | co-modifier` as *"whether ANY requirement key this change writes (capability +
normalized requirement title) is also written by another change in the corpus"*. This packet seeds
**`class: sole`** — the corpus's own machinery agreeing that the fifteen keys it writes are new. Had
the second `## REMOVED` block been authored, the seeder would have flipped BOTH this row and
`split-opendox-two-layer-product`'s to `co-modifier`, recording the collision mechanically.

**IF THE RULING GOES THE OTHER WAY** — that § 5.2a is meant to perform the departure itself, with the
packet's fifteen rows reconciled at its § 8 archive sweep the way § 5.2's other stale clauses already
are — the block is one file and this lane will author it on the word. The judgment is put here rather
than resolved silently.

## D4 — THE ARCHIVE ORDER, AND THE WINDOW IT AVOIDS

This packet archives BEFORE `split-opendox-two-layer-product`. Re-promotion first, removal second:

* re-promotion first leaves a window in which the fifteen titles are carried by TWO capabilities —
  distinct keys, each independently resolved by the latest-writer rule, no finding on either side;
* removal first leaves a window in which fifteen RATIFIED requirements are in no capability at all,
  which is the loss `promotion_fidelity` exists to prevent and which no reader could distinguish from
  a silent drop.

The second is worse, so the order is the first. `tasks.md` § 3 carries it as a box rather than as
prose. It agrees with `tasks.md` § 8.4's own reading of the split packet's archive, which requires the
floor to account for *"`openspec/specs/ideation-dashboard/` removed, AND the two new capability
directories plus the § 5.2a adapter successor capability ADDED"* — the successor directory existing at
that moment is that clause's premise.

## D5 — THE `## Purpose` IS WRITTEN IN THE DELTA, BECAUSE THIS IS THE ONE ARCHIVE THAT READS ONE

A capability-CREATING delta is the only place a `## Purpose` is ever read.
`prepare-openspec-1-12-readiness`'s `document-lifecycle` delta states it and states the trap: *"A
`## Purpose` in a change's spec delta is read ONLY when the capability is created; on any later
archive it is ignored"*, and where none is supplied the archive act writes `TBD - created by
archiving change <X>. Update Purpose after archive.` — a sentence that *"tells a reader nothing the
directory name did not"* and that was undischarged on 39 of this corpus's promoted specifications
when they were counted on 2026-09-05. This delta creates the capability, so it carries a written
Purpose and the placeholder never lands.

**PROVED, in a throwaway copy of `openspec/` and never in the repository** (pinned CLI 1.12.0,
`archive --yes`): `openxfactory-engineering-adapter: create`, `+ 15 added`, `Totals: + 15, ~ 0, - 0,
→ 0`; the created promoted specification carries the written Purpose and **0** occurrences of the
placeholder sentence, **15 requirements and 84 scenarios**, all fifteen byte-identical to this
delta's text; and `openspec/specs/ideation-dashboard/spec.md` comes out of that run with an
UNCHANGED sha256 — which is § D3's claim, measured rather than argued.

## What this packet does NOT decide

* It does not TICK § 5.2a. Ticks ride the packet bookkeeper's own `tasks.md` amendment; no byte of
  `openspec/changes/split-opendox-two-layer-product/` is touched here.
* It does not decide § 5.2 (the shed), § 5.4 or § 5.5 (floor parts 2 and 4), § 5.6 (the de-floor) or
  § 8.4 (the floor accounting). It gives them the id they were waiting on and nothing else.
* It does not RE-AUTHOR any requirement's subject. Per the map's own Migration text, *"The subject
  stays `openxFactory SHALL` because the repository does not change."*
* It does not touch `docs/opendox-carve-manifest.yaml`, any pin, any gitlink or any submodule.
* It does not ratify and does not archive. Both are Brett Heap's word, and `tasks.md` § 1 and § 3 hold
  them as separate acts.
