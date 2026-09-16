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
