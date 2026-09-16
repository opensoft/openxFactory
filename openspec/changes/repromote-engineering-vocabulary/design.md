# Design: repromote-engineering-vocabulary

Status: draft
Authored: 2026-09-16, lane `openxfactory-4` (display `openXfactory-4-openDox_extraction`), actor
`substrate52a`, against a fresh clone of `main` at `fa39141c`. Every count below was produced by a
script over that tree and is reproducible from it; none is read off prose.

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
| the ratified per-requirement map, **15 of 15** openxFactory rows, identical phrasing | *"openxFactory's OWN ENGINEERING ADAPTER, the small package beside `scripts/doc_health/` that implements openDox's corpus-adapter seam (RULING DQ-1)"* |
| `design.md` § D3 column head (:290) | *"`openxFactory`'s OWN ENGINEERING ADAPTER — the engineering mapping"* |
| `design.md` § D1 topology block (:172) | *"its OWN engineering adapter, one conformant implementation of openDox's seam"* |
| `proposal.md` (9) | *"a small ENGINEERING ADAPTER PACKAGE beside `scripts/doc_health/`"* |
| `tasks.md` :1248, :1356 | *"openxFactory's own engineering adapter"* · *"that DQ-1 ENGINEERING ADAPTER"* |
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

## D2 — THE SIX PATH LITERALS, AND THE SEAM OPERATION THAT ANSWERS FOR EACH

`tasks.md` § 5.2a: *"The only edit they take is re-expressing path literals as `adapter calls` — one of
RULING OQ-1's three classes, by name."* So the census comes first, and it is complete: of the 49
distinct backticked tokens in the fifteen, SEVEN are path-shaped, and they occur in four requirements.

**THE EDIT IS A REPLACEMENT OF A LAYOUT FACT BY THE OPERATION THAT HOLDS IT.** This is not a
stylistic de-pathing: every literal below is a datum the § 2.2a adapter ALREADY owns as data —
`scripts/corpus_adapter_openxfactory/home.py` carries `OBLIGED_PREFIX = "ideation/"`,
`PROMOTED_ROOT = "openspec"` and `REPO_ROOT`, and its module docstring names `home.py` as *"the only
module naming the home layout"*. A requirement that spells the layout states in canon what DQ-1 moved
into the adapter.

| # | requirement | OLD (promoted) | NEW (here) | operation |
|---|---|---|---|---|
| 1 | Staged-topic proposal commissioning | ``for a topic id with no directory under the checkout's `ideation/staging/` `` | ``for a topic id the corpus adapter's `list_documents` returns nothing for in the pinned checkout's staging area`` | `list_documents` |
| 2 | Accepted-possible promotion to staging | ``commissions the organization of that possible into `ideation/staging/<topic>/` as a fragment`` | `commissions the organization of that possible into a staging topic of the corpus the adapter resolves, as a fragment` | `resolve` |
| 3 | doxBench resolves its released contract … | ``then the existing walk up to an aggregation-relative `openxFactory/` `` | ``then the corpus adapter's `resolve` of the aggregation-relative home corpus`` | `resolve` |
| 4 | doxBench resolves its released contract … | ``the hosting repository is a publisher release and an aggregation-relative `openxFactory/` checkout also exists`` | `the hosting repository is a publisher release and an aggregation-relative home corpus the adapter could resolve also exists` | `resolve` |
| 5 | Demote refreshes a staged topic's outline … | ``for the proposal documents returning to the topic's `openspec/` workspace.`` | `for the proposal documents returning to the topic's OpenSpec workspace.` | promoted-root datum |
| 6 | Demote refreshes a staged topic's outline … | ``the proposal documents returning to the topic's `openspec/` workspace MUST still continue`` | `the proposal documents returning to the topic's OpenSpec workspace MUST still continue` | promoted-root datum |

**FOUR OF THE SIX NAME AN OPERATION; TWO NAME NO CALL, AND THAT IS DISCLOSED RATHER THAN DRESSED UP.**
Edits 1–4 sit where a READER looks, so the operation that looks is named: `list_documents` (design
§ D2's *list*, which must not know *"that `ideation/staging` or `openspec/changes` are meaningful
paths"*) and `resolve` (*"given a corpus reference, which checkout and which revision — the operation
`corpus_root.py` performs today with a path literal"*). Edits 5–6 sit in a STATUS rule about documents
a demote returns; no read and no write happens at those words, and inventing a call there would be
authoring rather than re-expressing. The path literal is removed and the governance noun the adapter
holds as its `PROMOTED_ROOT` datum stands in its place. Both shapes are inside OQ-1's one class — the
class is about which side of the seam the layout lives on — and the difference is stated here so a
reviewer counts four calls and two nouns and finds the packet said so first.

**TWO RECORDED NON-EDITS, because a silent omission is the defect here.**

* ``proposal.md`` (×4, requirement 11) is a DOCUMENT'S OWN IDENTITY, not a location. The seam's
  `read` returns *"the bytes of one document"* against a `DocumentId` whose `key` is declared OPAQUE
  (`scripts/corpus_adapter.py`:213-224 — *"a consumer may compare it, sort it and hand it back, and
  may not parse it"*), and `classify` answers *"what KIND is this document"*. Naming WHICH document a
  refresh reads survives the seam untouched.
* ``OPENXFACTORY_ROOT`` (×3, requirement 10) is an OPERATOR OVERRIDE's name and a rung of the very
  precedence ladder that requirement exists to state. `CorpusRef.location` is *"opaque here; the
  implementation interprets it"*, so the override is what a caller PASSES rather than a layout the
  reader walks. Deleting the rung's name would delete requirement content, which § 5.2a forbids.
* (``main``, ×1, requirement 1 — *"a main-resident cleanup record"* — is a git ref, not a path.)

**THE CARRY IS PROVED, NOT ASSERTED.** The delta is built by script
(`build_delta.py`, persisted with this lane's helpers): the fifteen are selected by the destination
the ratified map names, lifted from the promoted spec BY TITLE (never by line), each of the six edits
must match EXACTLY ONCE or the build aborts, and the build then REVERSES all six and asserts byte
equality against the promoted text. Measured: **102 promoted requirements; 71/16/15 map; 15 carried;
49,829 source bytes; 84 scenarios; 6/6 edits matched once; reversal proof passes.** Re-running it
after any merge from `main` re-proves the carry against the moved base — which is how this packet
stays current against `#1066`, the one open pull request that edits
`openspec/specs/ideation-dashboard/spec.md` (hunks at :2249, :2267 and an append after :2590; it
touches none of the fifteen).

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
