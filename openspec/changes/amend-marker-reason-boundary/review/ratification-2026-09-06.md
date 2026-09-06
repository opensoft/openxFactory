# Proposal Ratification: amend-marker-reason-boundary

Status: record
Kind: report
Decision date: 2026-09-06
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-06 by Brett Heap (openxFactory operator authority) —
in-session, lane `openxfactory-1`, verbatim: *"merge 705 when green, then ratify
692"*. The first clause landed openxFactory PR **#723** (merge `6295e387`,
14:43:56Z, closing **#705**); the second clause is this act. It was given after
a presentation that carried `design.md` **D1** as the packet's veto point —
option **A**, the reason beginning at the first ` — ` standing outside every
code span, against option **B**, requiring the removed units in a fenced list —
with both options written out and B's four costs beside A's. **D1 was not
vetoed.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE MODIFIED requirement**, *"Currency of an active
change's MODIFIED requirement blocks"*, restated in full with all 50 body units,
14 scenario titles and 40 scenario bullets byte-faithful, **ONE body sentence
replaced**, that sentence declared by a reserved `Removed from canon by` marker,
and **TWO scenarios ADDED at the end of the block**) — together with the CODE
this packet's `code_surface` declares
(`scripts/doc_health/modified_block_currency.py`: `_reason_boundary` added and
the unit-naming tail split moved onto it) and its tests
(`tests/doc-health/test_modified_block_currency.py`: 121 → 128, seven added and
none edited), plus `README.md` and this change's row in
`tests/sequenced_after/corpus-ledger.yaml`, with
`openspec validate amend-marker-reason-boundary --strict` and `--all --strict`
green and the verification run captured beside this file at
`verification-2026-09-06.md`.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-06.md` was
re-derived on the tree this record sits in, after this branch's merge from `main`
taking `origin/main` **`6295e387`** — the head that carries #723 (the scope-globs
archive-gate repair), #721, #724, #720 and #716. A commit cannot write its own
hash into its own tree, so the ratification commit is named by its subject and
its position on the branch rather than by a hash.

## 1. What was ratified, and what it says

**ONE requirement is MODIFIED and none is added.** `doc-health`'s promoted
*Currency of an active change's MODIFIED requirement blocks* is restated in full
— every body unit, all 14 scenario titles and all 40 scenario bullets, INCLUDING
the fenced block that writes the two marker forms out — and exactly one body
sentence changes.

**RETIRED:**

> The parser SHALL extract the code spans following the colon, in order, per
> CommonMark; the reason is everything after the last code span's following
> ` — `.

**REPLACING IT:**

> The parser SHALL extract the code spans following the colon, in order, per
> CommonMark, and THE REASON SHALL BEGIN AT THE FIRST ` — ` SEPARATOR STANDING
> OUTSIDE EVERY CODE SPAN: the units named are the spans that close before that
> separator, the reason is everything after it, and a code span that falls
> inside the reason is prose the reason quotes rather than a unit the marker
> names. Where no such separator stands, every span names a unit and the marker
> carries no reason, which is what the written-out `Merged into` example below
> is. The boundary is read the same way in both forms, the `Merged into`
> destination being matched in the prefix and the tail after the closing colon
> being parsed identically.

**TWO SCENARIOS ARE ADDED, AT THE END OF THE BLOCK** — *A marker's reason quotes
a code span* and *A marker's tail carries no separator outside a code span* — so
the new normative rule is pinned in CANON and not only in this packet's tests.
No promoted scenario moves, is retitled or loses a bullet.

**THE REPLACED UNIT IS DECLARED.** The block carries
`**Removed from canon by amend-marker-reason-boundary (2026-09-06):**` naming the
retired sentence verbatim in a DOUBLE-backtick span — double because the unit
itself cites ` — ` as a code span and CommonMark closes a run of N backticks only
on a run of exactly N — with a reason that contains **no code span anywhere**, so
that the RETIRED grammar on `main` and the AMENDED grammar here derive the same
one name and the same reason (`design.md` D4; measured in
`verification-2026-09-06.md` § 7).

**No file is added under `openspec/specs/`, so no codexFactory floor advance is
owed.**

## 2. Why the packet exists, in one finding and one measurement

**A marker's reason is prose, prose in this corpus quotes, and the retired
sentence turned every quotation into a declaration of removal.** openxFactory
issue **#692**, filed out of the adversarial review of PR **#685**, found that
`parse_marker` measures the reason from BEHIND — from the LAST code span — so
every span an author writes INSIDE the reason is harvested as a declared-removed
NAME. The live instance is the marker #685 promoted at
`openspec/specs/doc-health/spec.md:2716`: its author declared ONE unit, the
parser derives **three** (the intended `WHEN` bullet plus the words `WHEN` and
`AND` the reason quotes) and derives **no reason at all**. The sibling marker
#688 promoted at `:2755` is the same shape.

**IT IS INERT TODAY AND THAT IS AN ACCIDENT OF THE CORPUS, measured rather than
assumed.** Across every promoted specification and every active delta OTHER THAN
THIS PACKET'S OWN as the corpus stood BEFORE this packet — **108 files**,
**17,566 derived units** — **none** is literally `WHEN` or `AND`, and none of the
units this packet's own delta adds is either. So `suppression`'s third resolution
(*"the name matches no canon unit → nothing suppressed, nothing reported"*) has
been absorbing the defect by luck. Of the **SEVEN** unit-naming markers in that
corpus, **TWO change** (each 3 names → 1, reason `None` → the author's text) and
**FIVE are unaffected**; **no marker anywhere separates its NAMES with ` — `**, so
none loses a name its author meant to declare.

## 3. The decision ratified knowingly

### D1 — option A (the boundary), against option B (a fenced list)

- **Option A, TAKEN AND RATIFIED.** The names are the spans that close before the
  first ` — ` standing OUTSIDE every code span; the reason is everything after
  it; a span inside the reason is prose the reason quotes. It rewrites no marker
  (all seven parse under it, five to the same answer and two to the answer their
  authors wrote), rewrites no template, and keeps the promoted claim that
  survives — extraction of units is still by code span, and what the amendment
  adds is where extraction STOPS.
- **Option B, REJECTED FOR COST and written out beside A rather than strawed.**
  Requiring the removed units in a fenced list would (1) rewrite every existing
  marker including those inside `openspec/changes/archive/`, which are records of
  ratified acts and must not be edited, so B needs a grandfather clause and a
  grammar with one has two grammars; (2) rewrite both prose templates that
  promote into canon, in `doc-health` and in `document-lifecycle`; (3) collide
  with `fenced_regions`, the rule that stops written-out marker examples from
  parsing at all; and (4) still need a boundary rule for the reason trailing the
  list — so B is A plus a corpus rewrite.

**THE COST IS PUT WITH THE DECISION AND IS RESTATED HERE SO RATIFICATION CANNOT
BE READ AS UNAWARE OF IT.** A NARROWS what `document-lifecycle`'s *"naming each
deleted unit as a CommonMark code span"* reaches: a span standing AFTER the
boundary names nothing, so a `document-lifecycle`-conforming author who separates
two names with ` — ` now declares only the first. **That is a NEW failure mode
this amendment creates.** Its direction is the conservative one — the second unit
suppresses nothing and is therefore REPORTED rather than silently dropped, and
the amended names are always a SUBSET of the retired ones — and the corpus
carries no marker written that way, so the cost is prospective. But it is a
**SILENT** correction today, because `suppression`'s third resolution says nothing
about a name matching no unit, so the author sees only this family's fixed action
string telling them to add a marker they already wrote. Reporting it is scoped
into the owed successor at `tasks.md` § 5.1, named there as this amendment's own
consequence rather than only as the pre-existing silence.

**Ratified as designed. The reversal was NOT taken.**

## 4. What is NOT ratified, and the residue this word does not reach

1. **`specs/019-modified-block-currency-family/spec.md` FR-016 and ratified-reading
   A1 still state the retired sentence, and are deliberately not edited**
   (`tasks.md` § 5.3, UNTICKED). They are a BUILD RECORD of what
   `add-modified-block-currency-check` specified and was implemented against —
   not promoted canon, pinned by no test and by no gate — and the precedent
   `amend-unreadable-read-sibling-scenarios` (#688) likewise edited no feature
   spec when it amended the canon those specs describe.
2. **The estate-wide doc-health run is owed and is not taken here** (§ 5.4,
   UNTICKED). `active_blocks()` takes a repository root and the aggregation
   nightly reads every submodule; this lane is confined to its own clone, so the
   measurement here covers openxFactory only. The direction is safe by
   construction — the amended names are always a subset of the retired ones, so
   suppression can only shrink and a unit can only become MORE visible — and both
   affected arms are `info`/`warning`, so no `--fail-on error` run can red on it.
3. **`suppression`'s third resolution is untouched** (§ 5.1, UNTICKED): a name
   matching no canon unit stays silent. A family that reported *"this marker names
   something no unit of the requirement matches"* would have surfaced `WHEN` and
   `AND` the day they were written. That is an owed successor with its own
   scenarios, now scoped to report a code span INSIDE a reason as well.
4. **The two promoted markers, and the archived deltas that carry them, are not
   edited** (§ 5.2). They are records of ratified removals; what is wrong is how
   they are READ.
5. **THE ARCHIVE IS A SEPARATE ACT** (§ 5.5, UNTICKED). `code_surface` is
   non-empty, so under `release-realization` this packet archives on
   merged-plus-green realization evidence rather than on landing, and on a
   separate word. **This word ratifies; it does not archive.** openxFactory
   **#692** therefore closes at archive, not at this landing, which is why the
   pull request says `Refs #692` and not `Closes`.

**Codex is ABSENT, twice, and it is recorded as absence rather than as
clearance.** `@codex review` was requested on this pull request at 10:52:12Z and
the connector answered *"You have reached your Codex usage limits for code
reviews"*; a second request at 12:09:00Z drew the identical refusal
(12:09:08Z). **No Codex round ran on this packet.**

## 5. The bench, and the adversarial review folded before this record

- **Three adversarial review lenses on the pushed head returned
  MERGEABLE_AFTER_FIXES** — four MINOR findings and five NOTE-level ones, nothing
  MAJOR, and no hard limit found breached. **Six were taken, in the review-round
  commit `c5d33422`, so the ratified baseline is the folded text and not the text
  reviewed:**
  1. the **two missing scenarios** — the amended sentence was promoting with no
     scenario exercising it and would have been pinned only by this packet's
     tests, running code standing in for canon;
  2. the **corpus figures scoped to the tree they were taken on**, in every place
     they appear including the `**AMENDED BY …**` note that promotes into canon;
  3. the **`document-lifecycle` narrowing disclosed** as a NEW failure mode this
     amendment creates, with its reporting scoped into `tasks.md` § 5.1;
  4. a **`suppression`-level test** — the defect's harm lands at suppression, not
     at parse — plus a docstring saying the corpus test's unit set is a PROXY for
     the promoted requirement's units;
  5. **`_REASON_SEP` used in the pairing branch too**, so one grammar token has
     one spelling in the function, with that branch's behaviour untouched;
  6. **two pieces of residue named** — `specs/019` FR-016 (§ 5.3) and the
     estate-wide run (§ 5.4).
  **Re-verified after the fold: MERGEABLE.**
- **Three were refused, with reasons:** the vendored-`scope_globs.py` re-vendor
  note belongs to PR #723 and not to this pull request, which touches no vendored
  module; the estate-wide MEASUREMENT itself, which is outside this lane's clone
  and is therefore RECORDED as owed rather than claimed; and the merge-from-`main`
  and re-measure, which was owed at landing on Brett Heap's word — **and which
  this ratification commit's parent merge has now taken, against `origin/main`
  `6295e387`, with every number re-derived in `verification-2026-09-06.md`.**
- **Copilot: two rounds, one thread, taken and resolved.** Round 1 (10:19:12Z) and
  round 2 (11:30:49Z). The one inline thread it opened was a precedence pitfall in
  the pairing branch's conditional — `normalize(tail[3:])` evaluated even when the
  tail does not carry the separator — and it is fixed and the thread is RESOLVED.
- **Sourcery:** the private-repo upsell stub, as on every packet in this arc.

## 6. The landing obligation

**Rule 6 applies.** This pull request adds a README OpenSpec Records entry and
creates a directory under `openspec/changes/`, so lane `openxfactory-1` posts
`LANDING — lane openxfactory-1, session <id>, <UTC>, PR #719 into openxFactory
main` on the pull request and in `~/projects/xFactory/LANES.md` before the merge,
and `LANDED — lane openxfactory-1, <UTC>, PR #719 → <merge sha>` after it. The
landing is the coordinator's act, not this author's.

**The pull request is self-authored and is merged under the B2 provenance
pattern**: `gh` opens pull requests as `brettheap`, so a code-owner ruleset never
clears on Brett Heap's own click; the merge is an admin merge on his recorded
word, with that word — *"merge 705 when green, then ratify 692"* — quoted in the
merge provenance. `openspec validate --all --strict` and the pinned 1.12
entrypoint are green at the ratified head, and the CI rollup is observed rather
than expected.
