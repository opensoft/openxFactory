# Proposal Ratification: amend-absent-changelog-is-an-answer

Status: record
Kind: report
Decision date: 2026-09-07
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-07 by Brett Heap (openxFactory operator authority) —
in-session, lane `openxfactory-1`, verbatim: *"merge them when green, then ratify
753"*. The first clause landed three pull requests — openxFactory **#752**
(merge `3a28face`, the archive-gate parity round 2) and **#755** (merge
`64aad02e`, `add-chain-attestation` § 5.8's task-text amendment), and
xFactory-Hermes-Install **#72** (merge `06c9083d`) — and the second clause is
this act. It was given after a presentation that carried BOTH of this packet's
veto points: `design.md` **D1** — option **A**, splitting the changelog arm on
the fact the read already establishes so a HELD tip with no readable changelog is
GRADED with no declarations, against option **B**, keeping the skip and giving
the held case a distinct reason class only — and `design.md` **D2**, named
separately so it could be vetoed on its own, whether the retired skip's fact is
re-reported at `info` beside the grading or simply stops being reported.
**NEITHER WAS VETOED.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE MODIFIED requirement**, *"Release-tag
publication"*, restated in full with all 232 body units and scenario bullets and
all 30 promoted scenario titles byte-faithful, **TWO bullets of ONE scenario
replaced**, each dropped unit declared by its own reserved `Removed from canon
by` marker) — together with the CODE this packet's `code_surface` declares
(`scripts/doc_health/release_tag_publication.py`: the `if changelog is None:`
guard split on `tip_present`, one bounded `ls_tree_paths` consultation added on
that arm alone, and one `info` appended) and its tests
(`tests/doc-health/test_release_tag_publication.py`: 146 → 152, six added and one
CONVERTED), plus `README.md` and this change's row in
`tests/sequenced_after/corpus-ledger.yaml`, with
`openspec validate amend-absent-changelog-is-an-answer --strict` green through
the pinned 1.12 route and the verification run captured beside this file at
`verification-2026-09-07.md`.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-07.md` was
re-derived on the tree this record sits in, at `origin/main` **`64aad02e`** — the
head this branch's third and last catch-up merge took. **THREE MERGES FROM
`main` STAND ON THIS BRANCH, AND ALL THREE ARE NAMED**: `787130fb` (taking
`44d8fbaf`, with one `README.md` conflict where both sides added a row at the top
of the *Active changes* block and BOTH rows were kept), `2f8f93d0` (taking
`d52e6b88`, an undocumented merge carrying git's bare default message and no
`Lane:` trailer, which brought only `main`'s own commits and touched nothing of
this packet) and `5f0154e6` (taking `64aad02e`). The ratification encode took no
fourth merge, `origin/main` having not moved past `64aad02e`. A commit cannot
write its own hash into its own tree, so the ratification commit is named by its
subject and its position on the branch rather than by a hash.

## 1. What was ratified, and what it says

**ONE requirement is MODIFIED and none is added.** `doc-health`'s promoted
*Release-tag publication* is restated in full — every body unit and all 30
promoted scenario titles, INCLUDING #678's and #688's amendment notes and their
`Removed from canon by` markers, which promoted into canon with the requirement
and are CARRIED rather than restated — and exactly TWO bullets of ONE scenario
change, *The changelog cannot be read at the published tip*.

**THE `THEN`, RETIRED:**

> - **THEN** the family MUST report a skip naming that read, and MUST NOT treat the absence of a declaration it could not look for as the absence of a declaration

**REPLACING IT:**

> - **THEN** the family MUST NOT treat the absence of a declaration it COULD NOT LOOK FOR as the absence of a declaration, and MUST report a skip naming that read WHEREVER THE DOCUMENT'S OWN ABSENCE HAS NOT BEEN ESTABLISHED — the commit not held, or held with the tree at it carrying the path and no readable blob coming back for it, or the tree not listable at all — and MUST treat a declaration it DID look for, at a commit this checkout holds whose tree carries no such path, as ABSENT: the bundles in scope MUST be graded with NO declarations, exactly as they are graded where the changelog reads and declares nothing, rather than skipped past

**THE `AND`, RETIRED:**

> - **AND** where the commit IS held, the skip MUST SAY THAT and MUST state the presence — naming the held commit and the read that returned nothing at it, and NOT asserting a file absence the held commit does not establish — because a tip this checkout holds is an ANSWER rather than a read that failed, and reporting it in the unfetched case's words sends a reader to look for a fetch defect that does not exist

**REPLACING IT:**

> - **AND** where the document's absence IS established, the fact MUST STILL BE RECORDED and MUST state the presence — naming the held commit, the read that returned nothing at it, and the tree listing that establishes the absence, NEVER asserting a file absence on the held commit alone, which does not establish it — but it MUST be recorded BESIDE the grading rather than INSTEAD of it, and at `info`, because a tip this checkout holds whose tree carries no such document is an ANSWER rather than a read that failed, and a family that answered it with a skip would withhold from it the very findings the same tip carrying an empty changelog receives

The scenario's `WHEN` bullets and its closing `AND` (*"not fetched is not an
answer, in either direction"*) are carried **byte-identical**, and no other
scenario is touched, added, removed or retitled.

**EACH DROPPED UNIT IS DECLARED BY ITS OWN MARKER, AND TWO MARKERS ARE A CHOICE
RATHER THAN A CONSTRAINT.** Both carry
`**Removed from canon by amend-absent-changelog-is-an-answer (2026-09-07):**`
and name the retired bullet verbatim in a DOUBLE-backtick span. A semicolon
would have worked — canon's own written-out example at
`openspec/specs/doc-health/spec.md:1778` separates two names with `; `, which
`amend-marker-reason-boundary`'s promoted boundary leaves intact — and two
markers are still the right shape here, because **a marker carries ONE reason and
these two removals have DIFFERENT ones**: the `THEN` is retired because the skip
it requires suppressed a grading, the `AND` because it constrains the wording of
a skip the ESTABLISHED-ABSENCE case no longer emits. **NEITHER REASON CARRIES A
CODE SPAN**, which is the self-reference hazard (`design.md` D4): with no span in
the reason, the RETIRED grammar and the AMENDED one derive the same single name
and the same reason from each. Measured on the ratified tree, through
`parse_marker`: **two markers, ONE name each, reason 388 and 496 characters, no
backtick in either** (`verification-2026-09-07.md` § 7).

**No file is added under `openspec/specs/`, so no codexFactory floor advance is
owed.**

## 2. Why the packet exists, in one brief and one measurement

**THE AMENDMENT THAT PROVED THE READ WAS AN ANSWER LEFT IT REPORTED AS A
QUESTION, AND A QUESTION RETURNS BEFORE THE BUNDLES ARE GRADED.**
`amend-unreadable-read-sibling-scenarios` (PR **#688**, merge `a59d5463`,
archived by **#703**) settled that the changelog read's per-path `None` stands,
at that arm, for a tip this clone HOLDS at which no readable
`contracts/CHANGELOG.md` blob is reachable — the unfetched fact being EXCLUDED,
the manifest having read at the same commit — and made the skip SAY so. Its own
`design.md` **D6** recorded the suppression it was leaving behind at full
strength and wrote this successor's brief: *split the arm on the fact the read
already has*. The `if changelog is None:` guard stands ABOVE the `in_scope` loop
and RETURNS, so a held tip declaring an in-scope bundle and carrying no readable
changelog was answered with a skip INSTEAD OF the tag findings the loop would
have emitted. openxFactory issue **#750** filed it.

**THE MEASUREMENT, D6'S OWN, RE-TAKEN ON THE TREE THAT LANDS.** One shim, two
runs differing in a single blob: an ABSENT `contracts/CHANGELOG.md` at a HELD tip
answered with ONE `Skip` and nothing graded; the SAME shim with an EMPTY
changelog answered with ONE `error` naming the untagged bundle. **A document that
is provably not there and a document that says nothing carry the SAME fact about
declarations**, and only one of them was being graded — the one whose absence is
easier to arrange. The six-state table, both sides, is
`verification-2026-09-07.md` § 6.

**CANON DESCRIBED THE SKIP, WHICH IS WHY THIS IS A PACKET AND NOT A PATCH.** The
promoted scenario said with a MUST that the family *"report a skip naming that
read"*, and the bullet below it said with a MUST that *"where the commit IS
held, the skip MUST SAY THAT"*. Moving the guard alone would have put running
code out of agreement with promoted canon — the checker out-running canon, the
inverse of the defect #678 and #688 were written to avoid — so the remedy is a
MODIFIED requirement retiring those two bullets, realized in the same pull
request under `release-realization`'s merged-plus-green rule.

## 3. The decisions ratified knowingly

### D1 — option A (split the arm and GRADE), against option B (keep the skip)

- **Option A, TAKEN AND RATIFIED.** Where the commit is held and the document's
  own absence is ESTABLISHED, the family treats the read as an ANSWER — no SPENT
  declaration exists — and runs the `in_scope` loop with an EMPTY declaration
  set, so the repository is graded exactly as it would be at an empty changelog.
  Where the commit is NOT held, the skip stands. `read_changelog(None)` already
  returns an empty read, so the fall-through invents nothing.
- **Option B, REJECTED FOR COST and written out beside A rather than strawed.**
  Leaving the guard where it is and giving the held case its own reason class
  leaves D6's suppression EXACTLY where D6 found it: the held-and-absent case
  still returns before the loop, an untagged bundle at such a tip still receives
  no finding, and a packet, a ratification and an archive act are spent improving
  the label on that silence.

**THE COST IS PUT WITH THE DECISION AND IS RESTATED HERE SO RATIFICATION CANNOT
BE READ AS UNAWARE OF IT.** A **CHANGES WHICH FINDINGS AN IN-SCOPE REPOSITORY
RECEIVES** — the reason D6 refused to take it inside a packet whose claim was
*"one skip's TEXT"*. The direction is the conservative one: a `Skip` becomes the
grading an EMPTY changelog already receives, so nothing this family reports today
becomes quieter, and the one new finding is `info` and can redden no
`--fail-on error` run and fail no cut-time gate. What A cannot promise from one
clone is the ESTATE: a repository that really does hold its published tip, carry
no readable `contracts/CHANGELOG.md` and declare an in-scope bundle would begin
receiving tag findings it was previously skipped past. **That is the finding this
packet exists to surface and not a regression**, and the estate-wide run is named
as owed at landing (`tasks.md` § 6.1) rather than claimed.

**Ratified as designed. The reversal was NOT taken.**

### D2 — the retired skip's FACT is re-reported at `info`

- **Option D2-b, TAKEN AND RATIFIED.** One finding, `info`, on
  `contracts/CHANGELOG.md` — NOT on `contracts/manifest.yaml`, because a
  finding's identity in this capability is `(family, repository, path)` and a
  trace sharing the manifest's identity with the grading findings beside it would
  be masked by any one of them — gated on `in_scope`, classed `auto-fixable`,
  carrying the words #688 ratified and claiming no more than the presence gives
  them.
- **Option D2-a, REJECTED.** Saying nothing silently drops a ratified
  obligation: `fam_release_tag_publication` turns every per-repository `Skip`
  into an `info` precisely so a reason is *"reported, not dropped"*, so retiring
  the skip without leaving the fact behind would retire #688's rule — that the
  held case STATE THE PRESENCE — while claiming to carry it. It is also a worse
  report: a reader of *"contract-v2.0 is declared and has no published annotated
  tag…"* would have no way to learn that this repository carries no changelog at
  all, which is the document the SPENT remedy would be written into.

**Ratified as designed. The `info` stands.**

### D3a — the three-way tree consultation, from Codex's P2, ratified with the rest

Codex's round-1 **P2** on this pull request was TAKEN IN FULL before the word was
given, and the text the word was given over carries it. A held commit and a
per-path `None` still stand for TWO facts — the tree at that commit carries no
such path, or the tree DOES carry it and the blob is missing or corrupt — and
**GRADING IS A CLAIM ABOUT THE FILE**, which the held commit alone does not
license. Grading a damaged object store as an absent document would read a REAL
SPENT declaration as absent and answer an EXTINGUISHED obligation with a FALSE
`error`, telling an operator to publish a tag that cannot be published. So
`ls_tree_paths` is consulted ONCE on that arm, with the document's own path as
its pathspec: the path NOT listed is an ESTABLISHED absence and grades; the path
LISTED with no readable blob is a READ THAT FAILED and keeps the skip; a listing
that cannot be performed is UNESTABLISHED and keeps the skip. Both kept skips
state the presence, because both stand BELOW the held-tip split. **The canon
says it and not the code alone**: the amended `THEN` names all three states and
the amended `AND` requires the record to name the tree listing that establishes
the absence.

## 4. What is NOT ratified, and the residue this word does not reach

1. **THE ARCHIVE IS A SEPARATE ACT** (`tasks.md` § 6.4, UNTICKED).
   `code_surface` is non-empty, so under `release-realization` this packet
   archives on merged-plus-green realization evidence rather than on landing, and
   on a separate word. **This word ratifies; it does not archive.** openxFactory
   **#750** therefore closes at archive, not at this landing, which is why the
   pull request says `Refs #750` and not `Closes`.
2. **The estate-wide doc-health run is owed and is not taken here** (§ 6.1,
   TICKED ON THE RECORDING ONLY). `doc-health.py --repo-root` reads every
   governed submodule and `obtain_commit` FETCHES into each clone whose published
   tip is absent — it WRITES INTO CHECKOUTS THIS LANE DOES NOT OWN, which is not
   a read-only measurement. #612's measurement is cited instead: nine of the ten
   governed repositories carry no `contracts/manifest.yaml` at all and return at
   the MANIFEST arm long before this one, so the expected estate delta is zero.
3. **The floor exemption over the SKIP is recorded, not widened** (§ 6.5;
   `design.md` D2). The amended `THEN` requires a skip *"wherever the document's
   own absence has not been established"* with no qualification, and a
   BELOW-FLOOR repository is given neither the skip nor the grading: nothing is
   in scope, the tree is never consulted, and the arm returns `[]`. **The reading
   is PRE-EXISTING and this packet does not disturb it** — the promoted `THEN`
   carried the same unconditional MUST over the same `if not in_scope: return []`,
   put there by `declare-spent-bundle-state` on Copilot's PR #584 round 3
   finding. Making the exemption explicit in canon is a unit this MODIFIED block
   does not declare and would want its own scenario. **The word is given over the
   disclosure, and it takes it as a disclosure.**
4. **A LATE `Skip` IN THE BUNDLE LOOP STILL DROPS THE TRACE — DISCLOSED, WITH
   TWO REMEDIES RECORDED AND NEITHER TAKEN** (§ 6.6; `design.md` D6). The `info`
   is APPENDED, and three arms below it `return Skip(...)` — unlistable tag refs,
   unlistable refs for a named superseding bundle, an unresolvable declaring
   commit — each discarding `findings` whole, so on those paths the amended
   `AND`'s *"the fact MUST STILL BE RECORDED"* is not honoured. **The shape is
   PRE-EXISTING and general**: `check_repo` returns `Skip | list[Finding]` and
   `fam_release_tag_publication` branches on `isinstance`, so no return carries a
   skip beside findings, and the raw-HTML `error`, every accepted-SPENT `info`
   and any earlier bundle's LIGHTWEIGHT or MISPLACED `error` die on those same
   returns today. This packet adds one member to that set; it does not create it.
   **TWO remedies are recorded and the successor is handed BOTH**: widen
   `check_repo`'s return contract so a partial skip travels WITH the findings
   already established (re-reading the family's `len(skips) == len(scoped)`
   accounting and ruling what a partial skip means to the cut-time gate, which
   fails closed on any skip); or **qualify the requirement** so it governs the
   case where the family answers for the repository at all — Copilot's round-5
   reading, a wording change inside a bullet this block ALREADY replaces, costing
   nothing in carriage. **NEITHER IS TAKEN HERE, AND THE REASON IS NOW A RECORD
   RATHER THAN A CONDITION.** `tasks.md` § 6.6 and `design.md` D6 give the fix
   round's reason in the fix round's tense — that a fix round does not move
   normative text on a bot's reading *"while a ratification word is
   outstanding"* — and those two sentences are left exactly as the word was given
   over them, because ratified bytes do not move to tidy a tense. The word has
   now been given, it was given over a text carrying BOTH remedies, and **it did
   not take either**: the qualification stays a SUCCESSOR, not a late edit to a
   ratified bullet.
5. **The other arms of this family are untouched** (§ 6.2). Unlistable refs, an
   unresolvable declaring commit, a whole-batch read failure: whether any of
   those is also an answer wearing a question's clothes is a separate reading
   with its own scenarios, and it is not opened here.
6. **The archived deltas that carry the retired bullets are not edited** (§ 6.3).
   They are records of ratified acts and `promotion-fidelity` compares them
   against canon; editing one would mutate history and manufacture the divergence
   that family reports.

## 5. The bench, and the adversarial review folded before this record

- **Three adversarial review lenses on the pushed head returned
  MERGEABLE_AFTER_FIXES** — eleven findings across code/delta correctness,
  canon/records and over-reach, nothing that breached a hard limit. **All eleven
  were taken or disclosed, in three commits — `4e237311` (the code surface),
  `446b4720` (the records) and `7313b45c` (Copilot round 5's second remedy) — so
  the ratified baseline is the folded text and not the text reviewed.** Two were
  taken as DISCLOSURES with named successors rather than as widenings (§ 4.3 and
  § 4.4 above), and that choice is stated rather than smoothed over. A
  re-verification pass over `7313b45c` returned **READY_TO_ENCODE**.
- **Codex: one round, one P2, TAKEN IN FULL.** *"Distinguish missing objects
  before grading the changelog"* is D3a above, and it is the difference between a
  correct grading and a FALSE `error` on a repository whose records are right.
  The thread was replied to and **resolved**.
- **Copilot: SEVEN rounds by head** (`6ec99c8c`, `48ecf6f4`, `72153d23`,
  `787130fb`, `446b4720`, `5f0154e6`, `7313b45c`), of which three carried
  comments: round 1's wording nit on `_NO_CHANGELOG_ACTION` (taken), round 2's
  suppressed comment that the `info`'s *"NO SPENT DECLARATION EXISTS"* was
  unqualified (taken twice — the missing-blob case was removed from the arm
  outright by D3a, and the remaining claim was qualified to the path it read),
  and round 5's independent raising of the late-`Skip` trace drop from the
  `AND`'s side, which named the second remedy § 4.4 records. **All threads are
  resolved and no thread is open.**
- **Sourcery:** the private-repo upsell stub, as on every packet in this arc.
- **Two pre-encode record corrections were taken while the packet was still
  draft, and both are citation corrections rather than substance.** `tasks.md`
  § 2.1 cited `d5a549e4` for the D0 baseline while `design.md` D0 said the
  baseline had been corrected to `d52e6b88`; § 2.1 now names `d52e6b88`, and the
  two modules the measurement runs through are BYTE-IDENTICAL at `d5a549e4`,
  `d52e6b88` and `64aad02e` (blobs `6f627cb0` and `71662937`), so nothing derived
  through them moved. `proposal.md` twice pointed at `tasks.md` § 5.2 for the
  estate-wide run, which lives at § 6.1; both pointers are corrected.

## 6. The landing obligation

**Rule 6 applies.** This pull request touches `openspec/changes/` and carries a
README OpenSpec Records entry, so lane `openxfactory-1` posts
`LANDING — lane openxfactory-1, session <id>, <UTC>, PR #753 into openxFactory
main` on the pull request and in `~/projects/xFactory/LANES.md` before the merge,
and `LANDED — lane openxfactory-1, <UTC>, PR #753 → <merge sha>` after it. **The
landing is the coordinator's act, not this author's.**

**The pull request is self-authored and is merged under the B2 provenance
pattern**: `gh` opens pull requests as `brettheap`, so a code-owner ruleset never
clears on Brett Heap's own click; the merge is an admin merge on his recorded
word, with that word — *"merge them when green, then ratify 753"* — quoted in the
merge provenance. The pinned 1.12 entrypoint is green at the ratified head and
the CI rollup is observed rather than expected.
