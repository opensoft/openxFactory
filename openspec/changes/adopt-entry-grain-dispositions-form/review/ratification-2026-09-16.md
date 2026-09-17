# Proposal Ratification: adopt-entry-grain-dispositions-form

Status: ratified
Kind: report
Decision date: 2026-09-16
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-16T13:43:18Z by Brett Heap (openxFactory repository
owner), first-hand, in session, lane `openxfactory-2` (display
`openXfactory-2`), verbatim ***"ratify 1052 when green, then 1050"*** — this
record is the "then 1050" half of that word; the "ratify 1052" half ratifies
a separate change in this repository and is no part of this record. Recorded,
and THE ONE CITATION for this record: openxFactory #1045, comment
https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5698480736.

**AMENDED SINCE — BY THE RATIFIER, THREE TIMES, 2026-09-17.** THREE
post-ratification acts have moved normative text since this ratifying
commit, IN ORDER, and this pointer does not contradict any of them by
naming only one.

FIRST, THE CARRIAGE: on Brett Heap's word ***"route plus re-base"***
(openxFactory #1050, comment 5714145269, 2026-09-17T12:12:49Z),
`specs/document-lifecycle/spec.md`'s `## MODIFIED` block was re-based onto
`scope-pinned-arm-root-naming`'s own ratified outcome, its measurement
against this record's ratified tip moving from EMPTY to 21 insertions / 8
deletions — see § "Addendum, 2026-09-17 — carriage on the ratifier's word"
at the foot of this record.

SECOND, THE CARRIED WHEN RE-BASED ON ITS OWN RATIFIER'S AMENDMENT: on
Brett Heap's word ***"Apply the narrowing"*** (openxFactory #1047, comment
5714432684, 2026-09-17T12:34:53Z), the sibling scenario *A pinned target
names a pin no resolution root carries* — carried into this block VERBATIM
on `scope-pinned-arm-root-naming`'s ordering, not authored here — had its
WHEN moved with the amendment that packet's own ratifier made to it in the
same act that archived it — see § "Addendum 2, 2026-09-17 — THE CARRIED
WHEN RE-BASED ON ITS RATIFIER'S AMENDMENT" at the foot of this record.

THIRD, THE AMENDMENT THIS POINTER PRIMARILY TRACKS: the SAME block's
positive-resolution scenario *A marker names a capability of a pinned
neutral product* — its WHEN and disjointness bullet partitioned against
this packet's own added refusal scenario over the SAME input (the overlap
this record itself filed below, unresolved, for Brett Heap's word) — ruled
by Brett Heap on 2026-09-17T12:34:55Z, ***"Apply the partition"***
(openxFactory #1045, comment 5714433011), with the contradiction before him
and consented to as the amendment of a ratified packet BY ITS OWN RATIFIER
— see § "Addendum, 2026-09-17 — THE POST-RATIFICATION CONSENTED AMENDMENT"
at the foot of this record.

The citation immediately above remains THE ONE CITATION for the ORIGINAL
ratifying act and is UNCHANGED; each of the three amendments carries its
own citation, given in its own Addendum.

## Decision

**RATIFIED — D-1, D-2 AND D-3 AS FILED; NO DECISION REOPENED**, by Brett
Heap.

## The word, and exactly what it ratifies

Brett Heap's instruction was ONE SENTENCE naming two packets in sequence:

> **"ratify 1052 when green, then 1050"**

— first-hand, in session, lane `openxfactory-2` (display `openXfactory-2`),
2026-09-16T13:43:18Z, recorded on openxFactory #1045, comment
https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5698480736.
**THIS RECORD IS THE "THEN 1050" HALF** — the half naming this packet,
`adopt-entry-grain-dispositions-form`, filed as openxFactory pull request
[#1050](https://github.com/opensoft/openxFactory/pull/1050). The word was put
to him over the packet AS FILED and as fixed through four review rounds
answering Copilot, at that pull request's pre-ratification head, commit
`2a93c0d3`. The "ratify 1052" half ratifies a separate change under a
separate word-half and is no part of this record.

**NO VETO AND NO AMENDMENT.** The word ratifies the packet exactly as
`2a93c0d3` carried it: `design.md`'s D-1 (the measured pure entry-grain
guard), D-2 (the entry-grain reading is the optional member's FORM, not a
new required member) and D-3 (act at all, rather than leave the adapter as
the round-8 ruling left it) stand AS FILED, and `tasks.md` § 1's four
RULE/CONFIRM questions (1.1-1.4) are all answered by this one word.

## What is ratified

The proposal as written at commit `2a93c0d3` on pull request #1050, and the
decisions `design.md` carries:

- **D-1 — THE MEASURED PURE ENTRY-GRAIN GUARD.** `pinned_dispositions`
  (`scripts/validate-openspec-cli-pin.py:787-857`) is a pure, source-free
  function of the record, called as part of check 1 before any fetch
  (`:1966`, ahead of `repository_identity` at `:1973`). Its guard REFUSES TEN
  measured entry-grain records that `scripts/doc_health/pin_shapes.py`'s
  `_is_disposition_list` ACCEPTS today, and refuses ZERO that the adapter
  refuses: row 2's `[null]`, `["a"]`; row 3's `[{}]`, an entry without
  `cited_to`, `cited_to: []`, `why: ""`; row 4's `cited_to: "x"`; row 5's
  `level: "WARNING"`, `level: ""`; and row 6's entry naming no authority. The
  adapter is NARROWER than the guard on the entries and nowhere WIDER.
- **D-2 — THIS IS THE OPTIONAL MEMBER'S FORM, NOT A NEW REQUIRED MEMBER.**
  `_is_disposition_list` gains the entry grain and the failure representation
  gains the entry index/key; `dispositions:` stays OPTIONAL and stays OUT of
  the shape-guard-required set, and the measured `(29, 27, 2)` table split
  does not move.
- **D-3 — ACT AT ALL, RATHER THAN LEAVE IT AS THE ROUND-8 RULING LEFT IT.**
  Adopted. The two refused alternatives — restating the verifier's entry
  rules as PROSE in canon, and having the adapter CALL the verifier instead
  of transcribing it — are both refused on canon's own words.

**BOXES TICKED BY THIS RATIFICATION: 1.1, 1.2, 1.3, 1.4.** No box in
`tasks.md` § 1 stays open. § 2's CHECKBOXES stand exactly as the filing pull
request left them, and § 3 and § 4 stay open — the non-checkbox consistency
corrections below touch prose inside § 1's header and § 2.2's evidence line,
and move no box.

**THIS RATIFYING ACT ALSO CARRIES FIVE NON-DECISION CONSISTENCY
CORRECTIONS**, found by the lane from Copilot's suppressed review comments at
successive heads on this pull request. None is a design decision, none moves
a checkbox, and none reopens D-1, D-2, D-3 or any other scope:

1. `design.md` D-1's "THE GAP, COUNTED" tally and enumerated list corrected
   from EIGHT to TEN measured records — the table above it always carried
   `why: ""` and `level: ""`; the tally had dropped them — carried through to
   `proposal.md`'s own headline count and to the README "Active changes"
   bullet's count and enumeration.
2. In `proposal.md`, the "moves no byte of … any test" claim narrowed to name
   the realization test files under `tests/doc-health/`
   (`test_pin_shape_adapter.py`, `test_tag_hygiene_pinned_targets.py`)
   specifically, distinct from the `tests/sequenced_after/corpus-ledger.yaml`
   sweep-ledger bookkeeping the filing pull request already moved (task 2.6)
   — bookkeeping the self-gate requires of any filing that touches a
   promoted block, not test implementation for this arm.
3. `tasks.md` task 2.2's own evidence line corrected the same way, from EIGHT
   to TEN accepted-that-the-guard-refuses, naming `why: ""` and `level: ""`
   as the two the first tally dropped. The task's checkbox — already `[x]`
   from the filing pull request — does not move.
4. `.openspec.yaml`'s `origin.reason` carried the same pre-correction tally in
   two places — the main enumerated list and the closing "the eight measured
   entry-grain records … still accepted" sentence — both corrected to TEN to
   match. Pre-landing text corrections of the packet's own evidence, made
   before the ratifying merge exists, so neither is an origin mutation; every
   other origin key, including `proposed_by`'s filing-time wording, is
   unmoved.
5. `tasks.md`'s post-header paragraph, which had read "NOTHING IN § 1 IS
   TICKED … this lane ticks no box in it" under a "kept verbatim as history"
   marker, is rewritten to state the ratified fact directly instead of
   preserving that now-stale framing: ratified 2026-09-16 on the citation
   above, § 1 ticked (1.1-1.4); § 2's CHECKBOXES stand as filed (item 3
   above is § 2.2's own non-checkbox evidence-line correction, not a
   checkbox move); § 3 realization and § 4 archive stay open.

**A NORMATIVE PARTITION WAS APPLIED AT ROUND 5 (`a2640c9d`) AND REVERTED AT
ROUND 6.** Copilot found that `specs/document-lifecycle/spec.md`'s scenario
*A marker names a capability of a pinned neutral product* and the added
scenario *A pin record's optional dispositions member carries a malformed
entry*, AS FILED, prescribe TWO DIFFERENT OUTCOMES FOR THE SAME INPUT — a
record complete for its required shape members, carrying a well-formed,
non-empty `capabilities:` enumeration naming `<capability>`, whose OPTIONAL
`dispositions:` is `[{}]`: the first scenario's WHEN says nothing about
optional members, so this record satisfies it and its THEN requires the
target to RESOLVE; the second scenario's WHEN was written exactly for this
record and its THEN requires the target NOT TO RESOLVE. Round 5 partitioned
the two by editing the first (ratified) scenario's WHEN and disjointness
bullet. **ROUND 6 REVERTS THAT EDIT.** A packet carrying `Status: ratified`
cannot itself amend RATIFIED normative text on a reviewer's finding: ratified
text is the RATIFIER's to amend, not the lane's — precedent
`add-requirement-ref-resolution-integrity`'s 2026-09-01 amendment, ruled by
the ratifier. `specs/document-lifecycle/spec.md`'s `## MODIFIED` block now
lands EXACTLY AS RATIFIED at `4c32b183` — byte-identical, `git diff
4c32b183:…/spec.md` against the working tree is empty — and
`tests/doc-health/test_modified_block_currency_self_gate.py` carries no
`_LEDGER_SUBJECTS` row for it, the self-gate proving clean at zero without
one (it demanded the row only while the promoted scenario's body was edited).

**THIS PARAGRAPH IS HISTORY, NOT THE BRANCH TIP — SUPERSEDED 2026-09-17 BY
§ "Addendum, 2026-09-17 — carriage on the ratifier's word" AT THE FOOT OF
THIS RECORD. READ THAT WITH THIS.** The byte-identical measurement stood
until that date; it does not describe the packet after Brett Heap's word
carried `scope-pinned-arm-root-naming`'s ratified block into this one.

**THE OVERLAP ITSELF IS UNRESOLVED AND IS FILED FOR BRETT HEAP'S WORD, NOT
DECIDED HERE.** The lane is posting it as a RULING NEEDED comment on
openxFactory #1045: the ratified positive scenario, restating canon, resolves
a target whose record is complete for its required shape members and
capabilities enumeration even where its OPTIONAL `dispositions:` is present
and malformed, while the packet's own added scenario, over the SAME record,
refuses it. This MUST be settled by Brett Heap's word before realization —
§ 3 stays open regardless, but a realization built on the unresolved overlap
would realize one scenario's outcome while the other still contradicts it in
canon. Whichever way he rules, this record will be updated with the citation
and the outcome.

## What this ratification does NOT do

- **NO REALIZATION.** No byte of `scripts/doc_health/pin_shapes.py` moves, no
  byte of `tests/doc-health/test_pin_shape_adapter.py` or
  `tests/doc-health/test_tag_hygiene_pinned_targets.py` moves, no pin
  verifier is edited, and no record under `contracts/` changes. Realization
  is a LATER pull request in this same repository, on a separate word.
- **NO ARCHIVE.** `code_surface` is non-empty
  (`scripts/doc_health/pin_shapes.py` and its tests), so under
  `release-realization` this packet archives only on merged-plus-green
  realization evidence — not on this ratifying commit. Every box in
  `tasks.md` § 3 and § 4 stays unticked.
- **NO CHANGE TO ANY PIN RECORD.** `contracts/openspec-cli-pin.yaml` is the
  only record in this tree carrying `dispositions:` (measured, all six
  `*-pin.yaml` files); its six entries pass the guard today and pass the
  proposed entry-grain form unchanged.
- **NO `neutral-product-pin` DELTA.** That capability's ratified text
  (`:577`, `:578`, `:586-588`, `:633-636`) is READ and CITED by `design.md`
  D-1 and is not modified: the gap is the OFFLINE RESOLVER's reading, and the
  resolver is `document-lifecycle`'s grammar.
- **NO MERGE.** This record ratifies text at one head. Landing pull request
  #1050 is a SEPARATE act under this repository's Rule 6 landing-window
  protocol, because this change touches `openspec/changes/`.

## Records

- Governing issue, and the finding this packet answers: openxFactory
  [#1045](https://github.com/opensoft/openxFactory/issues/1045) — THE ONE
  CITATION for this ratification
  (https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5698480736).
- The packet this ratifies: openxFactory pull request
  [#1050](https://github.com/opensoft/openxFactory/pull/1050), at its
  pre-ratification head `2a93c0d3` (four fix rounds answering Copilot
  review).
- The cause: openxFactory pull request
  [#1040](https://github.com/opensoft/openxFactory/pull/1040) round 8, whose
  automated review raised `scripts/doc_health/pin_shapes.py:223` against the
  `extend-prose-tagging-target-to-pinned-capabilities` realization and was
  RULED STANDS by the lane, naming this packet's delta verbatim as "a
  legitimate later delta … noted, not filed."

## Addendum, 2026-09-17 — carriage on the ratifier's word

**WHY AN ADDENDUM AND NOT A SILENT REWRITE OF THE PARAGRAPH ABOVE.** "ROUND 6
REVERTS THAT EDIT" and its byte-identical measurement against `4c32b183` were
true that day, at that head, and are left exactly as measured: rewriting them
to match what follows would destroy the evidence that a real state existed in
which this packet's ratified block was untouched since ratification. That
state ended by the ratifying owner's own later word, recorded here rather
than folded silently into the body.

**THIS DIFFERS FROM BOTH NAMED PRECEDENTS, AND IT SITS BETWEEN THEM.**
`add-requirement-ref-resolution-integrity`'s 2026-09-01 addendum records a
POST-MERGE scope amendment the ratifying owner ruled on directly, in session,
with the contradiction before him. `scope-pinned-arm-root-naming`'s own
2026-09-16 addendum records four PRE-LANDING corrections made getting a
still-open pull request to green, one of them a lane-authored narrowing of
ratified text that packet's OWN round 6 reverted, on the same ground this
packet's round 6 invoked above. This packet's case is the first kind, not the
second: `adopt-entry-grain-dispositions-form` (landed as openxFactory #1050,
`fa39141c`, confirmed an ancestor of `main`) was already MERGED and its
`## MODIFIED` block already `Status: ratified` when the carriage below was
made — after landing, to a landed and ratified block, on a direct word from
the ratifying owner, the same authority `add-requirement-ref-resolution-integrity`
names and exercised the same way.

**WHAT WAS PUT, AND WITH WHAT IN FRONT OF HIM.** openxFactory #1075
(`chore/order-adopt-entry-grain-after-scope-pinned`) filed the CROSS-REFERENCE
ROUTE Brett Heap ruled on 2026-09-16 for the two unnamed
`modified-block-currency` ordering findings between this packet and
`scope-pinned-arm-root-naming` — both packets ratifying on the same verbatim
word and landing two minutes apart. Measuring that route exposed two things
openxFactory #1075 itself flagged rather than repaired: its carry runs WIDER
than that ruling's own summary ("one line of metadata … no normative text
changes"), and it makes `tasks.md` § 1.3's ticked, ratified evidence line
read false (see that section's own 2026-09-17 note, above in this packet).
Lane `openxfactory-2` — owner of both packets — put the contradiction back to
Brett Heap on openxFactory #1050: the earlier word was given on a premise the
measurement shows false, so the decision was put again with the TRUE
consequence in front of him, among four measured options — route plus
re-base with an addendum (the only measured green state), route only (opens
an ERROR-band finding), the pin route (already tried as openxFactory #1072
and closed unmerged), or something else (for instance archiving either
packet).

**THE RULING — ROUTE PLUS RE-BASE.** Brett Heap ruled ***"route plus
re-base"*** — openxFactory #1050, comment
https://github.com/opensoft/openxFactory/pull/1050#issuecomment-5714145269.
On that word, lane `openxfactory-2` carried the re-base below onto openxFactory
#1075's branch as a second commit, together with the two consequential
non-normative corrections the ruling itself names: this addendum, and
`tasks.md` § 1.3's dated note.

**WHAT MOVED.** `proposal.md` gains the ORDERED AFTER `scope-pinned-arm-root-naming`
declaration, and `specs/document-lifecycle/spec.md`'s `## MODIFIED` block is
re-based to carry that packet's ratified outcome whole: the root-precedence
citation restated as `_resolve_capability`/`_pin_roots`; the root-naming
sentence narrowed to findings emitted AFTER ROOT SELECTION, with its added
clause for the two findings emitted before any root is selected; the
selected-root narrowing of scenario *A pinned target names a pin no
resolution root carries*'s `WHEN` bullet; and the new scenario *A finding
emitted before root selection names what it judged*. None of the four is
this packet's authorship — each is `scope-pinned-arm-root-naming`'s own
ratified wording, carried verbatim. Measured: `git diff
4c32b183:…/specs/document-lifecycle/spec.md` against the branch, EMPTY at
ratification and reported so above, now reads **21 insertions / 8
deletions** — the byte-identical claim above no longer holds and is
superseded by this paragraph, not rewritten to erase it. Family-level, on a
clean `origin/main` checkout (`c6997f12`, the tip carrying both packets
landed) plus this carriage: `doc-health.py --single-repo . --family
modified-block-currency` goes from 0 critical / 0 error / **2 warning** / 15
info to 0 critical / 0 error / **0 warning** / 15 info — the two
unnamed-ordering-subject rows this repair exists to close.

**WHAT DID NOT MOVE.** This packet's own delta is still the ONE scenario *A
pin record's optional dispositions member carries a malformed entry*,
unedited by the carry and unedited by this addendum. D-1, D-2 and D-3 stand
as ratified; no `tasks.md` box outside § 1.3's dated note moves, § 1.3's
checkbox stays `[x]`, and § 3 and § 4 stay open. `_ORDERING_SUBJECTS` stays
`set()` and `_LEDGER_SUBJECTS` is unmoved — the repair NAMES the ordering, it
does not pin the finding away. No test file is touched, and
`scope-pinned-arm-root-naming`'s own delta is not edited at all: the carried
text is copied out of that packet's own ratified block, not authored here.
**THE OVERLAP FILED FOR BRETT HEAP'S WORD ABOVE (§ "THE OVERLAP ITSELF IS
UNRESOLVED…") IS UNTOUCHED BY THIS ADDENDUM AND STAYS OPEN ON ITS OWN
CITATION** — a different finding, from a different round, awaiting its own
word.

**THE ONE RATIFICATION CITATION FOR THIS RECORD IS UNCHANGED.** Everything in
this record, above and including this addendum, ratifies on, and only on,
openxFactory #1045 comment
https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5698480736.
The citation immediately above names a SEPARATE, LATER ruling — the "route
plus re-base" word — and is not a second ratification of this packet.

## Addendum 2, 2026-09-17 — THE CARRIED WHEN RE-BASED ON ITS RATIFIER'S AMENDMENT

**THE SECOND ADDENDUM OF THE SAME DAY, AND IT FOLLOWS THE ONE ABOVE.** The
addendum above records the ROUTE PLUS RE-BASE carriage (PR #1082 → `98b172e5`,
word 5714145269). This one records a LATER word of the same ratifier, given
after it, moving ONE bullet of the text that carriage brought in.

PR [#1075](https://github.com/opensoft/openxFactory/pull/1075) → `a93d2682`
ordered this packet AFTER `scope-pinned-arm-root-naming` and carried that
packet's ratified units into this block VERBATIM, one of them the sibling
scenario *A pinned target names a pin no resolution root carries*'s WHEN. On
2026-09-17 that WHEN was AMENDED BY ITS OWN RATIFIER — Brett Heap, first-hand,
in session, an interactive multiple-choice selection, verbatim ***"Apply the
narrowing"***, openxFactory
[#1047 comment 5714432684](https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5714432684)
— from "…and at least one resolution root was selected for the run" to "…and
at least one selected root whose boundary was successfully searched". **THE
CARRIED COPY IS RE-BASED TO THE AMENDED TEXT IN THE SAME COMMIT AS THE
AMENDMENT, UNDER THAT SAME RULING, AND AUTHORS NOTHING:** a carried copy left
at the superseded wording would be precisely the drift the carriage was
performed to prevent. **NO DECISION, SCOPE, `tasks.md` BOX, ORIGIN FIELD OR
OBLIGATION OF THIS PACKET MOVES** — this packet still adds EXACTLY ONE
scenario of its own, *A pin record's optional dispositions member carries a
malformed entry*. Measured after the re-base, against canon as promoted by the
archive of `scope-pinned-arm-root-naming`: canon 215 units, this block 223,
TWO uncarried units and TEN new. **THE CARRIAGE IS WHOLE, AND THE TWO
UNCARRIED UNITS ARE NOT ITS** — the re-based sibling WHEN matches canon
exactly, and EIGHT of the ten new units are this packet's own scenario title
and its seven bullets. The two uncarried units, and the remaining two new
ones, are the positive-resolution scenario's WHEN and its disjointness bullet,
which THIS PACKET'S OWN RATIFIER amended on ***"Apply the partition"*** — the
Addendum that follows this one — and which the re-base neither authored nor
moved. (Measured at the commit that merged `origin/main` at `5dd0a8dc`, the
partition amendment having landed as PR #1088 → `893abe97`; before that merge
the same measurement read ZERO uncarried and EIGHT new.)

## Addendum, 2026-09-17 — THE POST-RATIFICATION CONSENTED AMENDMENT

**A SECOND ACT OF THE SAME RATIFIER, THE DAY AFTER THE FIRST, ON THE ONE
OVERLAP THE RATIFYING RECORD LEFT UNRESOLVED.** It is recorded as an
addendum rather than folded into the body above, because a record that
quietly rewrites itself to match a later ruling destroys the evidence that
the ruling was needed.

**WHAT WAS PUT, AND WITH WHAT IN FRONT OF HIM.** The body above already
records the overlap Copilot found on this pull request: the ratified
positive-resolution scenario *A marker names a capability of a pinned
neutral product*, AS RATIFIED, says nothing about optional members, so it
RESOLVES a record complete for its required shape members and a well-formed,
non-empty `capabilities:` enumeration even where that record's OPTIONAL
`dispositions:` is `[{}]`; the packet's own added scenario, *A pin record's
optional dispositions member carries a malformed entry*, judges the SAME
record and REFUSES it — two normative outcomes for one input. Round 5
(`a2640c9d`) partitioned the two by editing the ratified scenario's WHEN and
disjointness bullet; round 6 (`73864686`) reverted that edit, because a
packet carrying `Status: ratified` cannot itself amend ratified normative
text on a reviewer's finding, and filed the overlap instead as a RULING
NEEDED comment on openxFactory
[#1045](https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5701323247),
with an addendum
([#1045](https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5701410009))
adding one further fact for whichever way the ruling went. THAT ADDENDUM
ASSERTED that a FALSEY `pinned_by_commit_only:` — `null`, `""` — must count
as EMPTY rather than as a present, malformed sequence, because the
entry-grain guard the ratified D-1 already reaches reads that member with an
ABSENT-IS-EMPTY default; and it contrasted `dispositions:`, which draws the
line differently: OF VALUES PRESENT, only an explicit `null` is EMPTY — the
same `pin.get(...)` call that yields `None` for an ABSENT member yields it
for an explicit `null` too, so the two are one case under the guard's `raw
is None` check (`scripts/validate-openspec-cli-pin.py:801-803`), not two —
and every other PRESENT falsey NON-SEQUENCE value that is not `null` —
`""`, `0`, `false`, `{}` — stays malformed, an empty sequence `[]` being
EMPTY, accepted as absence is. **THE `dispositions:` HALF OF THAT ADDENDUM IS
MEASURED AND STANDS; THE `pinned_by_commit_only:` HALF WAS THE LANE'S OWN
PREMISE AND IS WRONG**, and the NOTE below records what is measured instead.
It is left standing here, reported rather than rewritten, because the
correction is only legible against the claim it corrects.

**THE RULING — APPLY THE PARTITION.** Brett Heap, 2026-09-17, in session to
lane `openxfactory-2`, by interactive multi-choice:
[openxFactory #1045, comment
5714433011](https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5714433011)
— ***"Apply the partition"***: the positive-resolution scenario's WHEN
additionally requires every OPTIONAL member the matched shape admits that is
PRESENT to conform at its entry grain to the shape's own in-tree verifier's
PURE guard; the refusal scenario is unchanged; the disjointness bullet
extended. The same comment also carries the second, independent word on
realization timing (`tasks.md` § 3), which is no part of this record.

**THE PARTITION IS DEFINED BY THE GUARD, SO IT REACHES ONLY MEMBERS THAT
HAVE ONE — TODAY `dispositions:` ALONE.** The clause as first drafted named
`pinned_by_commit_only:` too, on the lane's addendum above. Measured on this
tree, that member has NO pure, source-free guard: both verifiers judge it
inside their source-dependent `verify()`, after the source is resolved and
reaching `source.read()` / `target.exists()`
(`scripts/validate-openreposhape-pin.py:481-508`,
`scripts/verify-openxwallet-pin.py:443-457`), and the shared adapter's own
citations for it carry NO `guard` name for exactly that reason, the comment
above them saying so in terms (`scripts/doc_health/pin_shapes.py:355-365`).
`dispositions:` does have one — `pinned_dispositions`, whose only input is
the record (`scripts/validate-openspec-cli-pin.py:787-803`) — which is why
the packet's own refusal scenario could already name it. The clause is
therefore narrowed to members for which such a guard exists; the ruling's
substance is untouched, the positive scenario still ceasing to accept the
one input the refusal scenario refuses. Recorded, with the lane's own
premise named as the thing corrected, on openxFactory
[#1045, comment 5715775376](https://github.com/opensoft/openxFactory/issues/1045#issuecomment-5715775376).

**NOTE — `pinned_by_commit_only:`, AND WHAT THIS AMENDMENT DOES NOT SAY
ABOUT IT.** Nothing here changes how that member is read. The shared
adapter's `_is_path_only_list` accepts ANY falsey value outright — `if not
value: return True`, before it ever checks for a list, so `None`, `""`,
`false`, `0` and `{}` are all empty to the adapter
(`scripts/doc_health/pin_shapes.py:151-171`) — and that is unchanged by this
amendment. The two verifiers, however, DIFFER AT THE FILE BOUNDARY, which is
why the amendment states no falsey-is-empty rule about them:
`validate-openreposhape-pin.read_pin()` parses the pin's own narrow grammar
and keeps top-level scalars as STRINGS (`:201`), so `pinned_by_commit_only:
null`, `false`, `0` or `{}` reaches `verify()` as a truthy string and is
refused there despite `pin.get(...) or []`, only a quoted `""` parsing as
empty; the wallet verifier loads the same member with `yaml.safe_load`
(`scripts/verify-openxwallet-pin.py:171`) and therefore does see Python
falsey values. Both facts are measurements of today's tree, recorded so no
reader takes the narrowed clause for a claim about either verifier.

**THIS IS A CONSENTED AMENDMENT, AND THE CONSENT IS THE WHOLE OF ITS
AUTHORITY.** Brett Heap is the ratifying owner of this packet; he ruled with
the contradiction already before him, recorded in this same file since
2026-09-16, rather than being asked to approve a repair he had not seen; and
the amendment is applied in a separate, ordinary pull request on the
2026-09-01 `add-requirement-ref-resolution-integrity` precedent's form,
landing under this repository's Rule 6 when its required checks are green.

**WHAT MOVED.** The `## MODIFIED` block's positive-resolution scenario, and
only it:

- The scenario's WHEN gained one clause. AS RATIFIED it read (in relevant
  part) *"…AND which carries a well-formed, NON-EMPTY `capabilities:` member
  in which `<capability>` appears"*. It now reads *"…AND which carries a
  well-formed, NON-EMPTY `capabilities:` member in which `<capability>`
  appears, AND every OPTIONAL member the matched shape admits that is
  PRESENT and for which that shape's own in-tree verifier exposes a PURE,
  SOURCE-FREE guard — one whose only input is the record, callable before any
  checkout, `git` call or network read — conforms at its entry grain to that
  guard: today `dispositions:` alone, whose guard reads an explicit `null` as
  EMPTY exactly as absence does and otherwise requires a sequence whose every
  entry it accepts, every other PRESENT falsey NON-SEQUENCE value (`""`,
  `0`, `false`, `{}`) staying malformed — an empty sequence `[]` is EMPTY,
  accepted as absence is; an optional member for which NO such guard exists,
  `pinned_by_commit_only:` today, is NOT reached by this clause"*.
- Its disjointness bullet gained the matching exclusion. AS RATIFIED it read
  *"an ABSENT enumeration, a malformed enumeration, and a well-formed
  enumeration in which `<capability>` does not appear, are OUTSIDE this
  scenario…"*. It now reads *"an ABSENT enumeration, a malformed
  enumeration, a well-formed enumeration in which `<capability>` does not
  appear, and a PRESENT optional member malformed at its entry grain against
  a pure, source-free guard this scenario's WHEN reaches, are OUTSIDE this
  scenario…"*.
- `tests/doc-health/test_modified_block_currency_self_gate.py`'s
  `_LEDGER_SUBJECTS` gains one row for
  `("adopt-entry-grain-dispositions-form", "document-lifecycle", "Prose
  tagging marker hygiene")`, with a comment recording why — bookkeeping the
  self-gate requires of editing an already-promoted scenario's body, not
  realization work, the same convention `scope-pinned-arm-root-naming`'s own
  row on this requirement already uses.

**WHAT DID NOT MOVE, stated so no reader has to diff for it.** The packet's
OWN added scenario — *A pin record's optional dispositions member carries a
malformed entry* — is BYTE-UNCHANGED: its WHEN, its THEN and all five of its
AND bullets stand exactly as ratified, and this amendment reopens no part of
it. D-1, D-2 and D-3 stand as ratified. `tasks.md` § 1's four ticked boxes
(1.1–1.4) are untouched, as is every non-checkbox correction the ratifying
commit made. § 2 stands exactly as the filing pull request left it, and § 3
and § 4 stay open — this amendment realizes and archives nothing.
`proposal.md`, `design.md` and the README carry no paraphrase of the
positive scenario's WHEN (checked again against the current, rebased block);
none needed alignment. And the block's OTHER content — the root-selection
prose and the two scenarios PR #1075 (`a93d2682`) carried in on
`scope-pinned-arm-root-naming`'s ordering — is untouched by this amendment,
which reaches only the one scenario the overlap named.

**THE OVERLAP IS NOW RESOLVED, NOT ROUTED.** Where the body above filed the
contradiction for Brett Heap's word and left both scenarios standing in
tension, this addendum records that word taken: a record complete for its
required shape members and capabilities enumeration, whose optional
`dispositions:` is `[{}]`, now satisfies ONLY the refusal scenario, the
positive scenario's WHEN no longer matching it. No other scenario in the
block shares this overlap; each already excludes what the others require.

**NO BENCH HAD READ THIS AMENDMENT AT THIS ADDENDUM'S WRITING.** It was new
text as of this addendum, carried on its own pull request under Rule 6, and
gated at that commit — `openspec validate` strict on this change and
`--all --strict`, the self-gate, `proposal-support.py . verify` and
`validate-sequenced-after.py . --ledger-diff` — were recorded there and not
pre-asserted here.

**ROUND 5, 2026-09-17: MEASURED, NOT PRE-ASSERTED.** Run in the foreground
at this round's head, after a plain `git merge origin/main` that landed no
new commits (`origin/main` was already an ancestor):
`pytest -q -p no:cacheprovider tests/doc-health/test_modified_block_currency_self_gate.py`
— NINETEEN passed; `python3 scripts/doc-health.py --single-repo . --family
modified-block-currency` — 0 critical, 0 error, 0 warning, SIXTEEN info,
the SAME sixteen named subjects this file's own self-gate asserts;
`OPENSPEC_TELEMETRY=0 openspec validate adopt-entry-grain-dispositions-form
--strict` — valid; `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
— 109 passed, 2 failed (111 items), the SAME pre-existing pair as
`origin/main` and neither this amendment's — `add-chain-attestation` and
`add-composed-view-authoring`; `python3 scripts/proposal-support.py .
verify` — "proposal support verification ok"; `python3
scripts/validate-sequenced-after.py . --ledger-diff` — the per-change sweep
ledger consistent with the corpus, 218 rows.
