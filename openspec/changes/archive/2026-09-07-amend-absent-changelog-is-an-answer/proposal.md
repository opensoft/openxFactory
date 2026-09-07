---
code_surface: openxFactory — ONE guard is SPLIT in `scripts/doc_health/release_tag_publication.py`, and the tests that pin it in `tests/doc-health/test_release_tag_publication.py`. The `if changelog is None:` arm that returned a `Skip` above the `in_scope` loop now returns one only where the document's own absence has NOT been established — the commit not held, the tree at it carrying the path with no readable blob coming back, or the tree not listable — and otherwise falls through so the loop grades the bundles with no declarations, which `read_changelog(None)` already answers. ONE bounded `ls_tree_paths` call is added on that arm and nowhere else. ONE `info` is ADDED, on `contracts/CHANGELOG.md`, carrying the fact the retired skip carried — this is the only new finding, it is `info`, and it cannot redden a `--fail-on error` run. NOTHING ELSE MOVES: no severity of an existing finding, no threshold, no enforcement floor, no path of an existing finding, no other arm, no workflow, no contract member and no other family. Six tests are ADDED and ONE is CONVERTED (its subject — the skip in the established-absence case — is what this packet retires), `tests/doc-health/test_release_tag_publication.py` 146 → 152.
target_release: implemented (the openxFactory main line). No contract bundle is cut, no release tag is owed, nothing under `contracts/` is touched and no digest set moves. Under `release-realization` a non-empty code surface archives on merged-plus-green realization evidence rather than on landing; the tasks are individually executable, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` and doc-health runs.
Status: ratified
Proposed: 2026-09-07
Ratified: 2026-09-07 by Brett Heap (openxFactory operator authority) — "merge them when green, then ratify 753"; record at review/ratification-2026-09-07.md
Origin: openxFactory issue **#750** and the ARCHIVED `amend-unreadable-read-sibling-scenarios`, whose `design.md` **D6** and `tasks.md` § 6 record this successor as OWED and write down the reading it needs. THE ORIGIN IS NOT THE RATIFICATION: an archived packet's record of what it left undone puts a successor in the QUEUE and decides nothing about its text, and issue #750 records a defect and the shape of a remedy rather than approving a word of it — that record is what put this packet in the queue; ratification followed as a SEPARATE act on 2026-09-07, cited ONCE in the line above and recorded at `review/ratification-2026-09-07.md`. `.openspec.yaml` keeps the drafting provenance it was authored with — `kind` and `id` never move — and the approval pair is ADDED beside it, which is the shape `add-drafted-proposal-origin` defined for exactly this transition. The decision the word reaches is `design.md` **D1**: option A (split the arm and grade) against option B (keep the skip and give it a distinct reason class), carried as this packet's veto point in the pull request body, in `tasks.md` § 1.2 and in the README row — **and NOT vetoed**. `design.md` **D2**, the retired skip's fact re-reported at `info` rather than dropped, was carried separately so it could be vetoed on its own — **and was not vetoed either**.
---

# Proposal: amend-absent-changelog-is-an-answer

Status: ratified
Proposed: 2026-09-07, in lane `openxfactory-1`, as the successor
`amend-unreadable-read-sibling-scenarios` named before it landed.
Origin: openxFactory issue **#750** and that packet's own `design.md` **D6** /
`tasks.md` § 6. The origin is a record of what is owed, not an approval; the
ratification was a SEPARATE act and it has now happened — **ONE citation line
for this document**, in the front matter, which is what `ratified-provenance`
counts. § Ratification records the act and what it settled; the record is
`review/ratification-2026-09-07.md`.

## Why

**The amendment that proved the read was an ANSWER left it reported as a
question, and a question returns before the bundles are graded.**

`amend-unreadable-read-sibling-scenarios` (PR **#688**, merged `a59d5463`,
archived by **#703**) settled which of two facts the changelog read's per-path
`None` stands for. Its own words, promoted into canon:

> by the time the changelog answers nothing the unfetched fact is not merely the
> rarer one: IT IS EXCLUDED, and the only fact left standing is a tip this
> checkout HOLDS at which no readable `contracts/CHANGELOG.md` blob came back.

That is an ANSWER about declarations — a tip this clone holds, at which no
document came back to carry one, has **no SPENT declaration**. The packet made
the skip SAY so and, deliberately, left it a skip. **And a skip returns.**
`scripts/doc_health/release_tag_publication.py`'s `if changelog is None:` guard
stands ABOVE the `in_scope` loop, so a repository whose published tip this clone
holds, which declares an in-scope bundle and carries no readable changelog, was
answered with a skip INSTEAD OF the tag findings the loop would have emitted.

**THE MEASUREMENT, WHICH IS D6'S OWN AND IS RE-TAKEN HERE ON THIS TREE.** One
shim, two runs differing in a single blob:

| the shim's `contracts/CHANGELOG.md` | today | with this packet |
| --- | --- | --- |
| absent (per-path `None` at a HELD tip) | one `Skip`, nothing graded | one `error` naming the untagged bundle, and one `info` recording the read |
| present and empty | one `error` naming the untagged bundle | unchanged — one `error` |

A document that is provably not there and a document that says nothing carry the
SAME fact about declarations. One of them was being graded and the other was
not, and the one that was not is the one whose absence is easier to arrange.

**CANON DESCRIBES THE SKIP, WHICH IS WHY THIS IS A PACKET AND NOT A FIX.** The
promoted scenario *The changelog cannot be read at the published tip* says with
a MUST that the family *"report a skip naming that read"*, and the bullet below
it says with a MUST that *"where the commit IS held, the skip MUST SAY THAT"*.
Moving the guard alone would put running code out of agreement with promoted
canon — the checker out-running canon, the inverse of the defect #678 and #688
were written to avoid — so the remedy is a MODIFIED requirement retiring those
two bullets, with the realization in the same pull request under
`release-realization`'s merged-plus-green rule.

## What Changes

**TWO BULLETS OF ONE SCENARIO, inside ONE `## MODIFIED` requirement — and the
guard they describe, in the same pull request.**

The delta restates `doc-health`'s *Release-tag publication* in full — every body
unit and all 30 promoted scenario titles, byte-faithful, INCLUDING #678's and
#688's amendment notes and their `Removed from canon by` markers, which promoted
into canon with the requirement and are CARRIED rather than restated — and
changes exactly this, in the scenario *The changelog cannot be read at the
published tip*:

- the promoted **`THEN`** is REPLACED. It keeps the unfetched half — the family
  MUST NOT treat the absence of a declaration it COULD NOT LOOK FOR as the
  absence of a declaration — and generalizes it to the rule the grading needs:
  the skip stands WHEREVER THE DOCUMENT'S OWN ABSENCE HAS NOT BEEN ESTABLISHED
  (the commit not held; held with the tree carrying the path and no readable blob
  coming back; the tree not listable at all), and a declaration the family DID
  look for, at a commit this checkout holds whose TREE carries no such path, is
  ABSENT — so the bundles in scope are graded with no declarations rather than
  skipped past;
- the **`AND`** below it is REPLACED. Its subject was the wording of a skip the
  established-absence case no longer emits. Its NARROWING is carried and
  STRENGTHENED — the presence stated, a file absence NEVER asserted on the held
  commit alone, and the tree listing that establishes it named — and re-pointed
  at the record that takes the skip's place: the fact MUST still be recorded, at
  `info`, BESIDE the grading rather than instead of it.

The scenario's `WHEN` bullets and its closing `AND` (*"not fetched is not an
answer, in either direction"*) are carried **byte-identical**, and no other
scenario is touched, added, removed or retitled.

**TWO CANON UNITS ARE DROPPED, AND EACH IS DECLARED** by its own reserved
marker, `**Removed from canon by amend-absent-changelog-is-an-answer
(2026-09-07):**`, naming the retired bullet verbatim as a double-backtick code
span with the reason. TWO markers and not one: under the boundary
`amend-marker-reason-boundary` promoted (PR **#719**, archived `#739`) a marker's
names are the code spans closing BEFORE its first ` — ` standing outside every
span, so two units separated by that sequence would declare only the first.
Each marker's reason is written with NO code span in it, so the retired grammar
and the amended one derive the same single name from each — `design.md` **D4**,
the self-reference hazard.

## Why the code surface is NOT `none`

Because the amended `THEN` is a `MUST` about findings the family does not
currently emit. This packet is the mirror image of #688's D2 question and it
answers it the same way: the words are made true HERE, in the smallest edit that
makes them true, rather than declared and left owing.

The edit is one comparison, one bounded tree listing and one fall-through.
`read_changelog(None)` already returns an empty read — no declarations, no
refusal — which is exactly what the loop is owed for a tip whose tree carries no
document, so nothing is guessed. **THE TREE LISTING IS NOT OPTIONAL AND IT IS
CODEX'S FINDING, TAKEN**: a held commit licenses *"no readable blob came back at
this path"* and never *"the commit carries no such file"*, and GRADING is a claim
about the file — so a store that holds the commit and its trees but not the blob
would have a REAL SPENT declaration read as absent, answering an EXTINGUISHED
obligation with an `error` telling an operator to publish a tag that cannot be
published. `ls_tree_paths` reads the TREE object rather than the blob, so it
answers for exactly that state; the family grades only where the tree carries no
such path, and keeps the skip where it carries it or cannot be listed.
`design.md` **D3a** carries the finding and the decision. What is ADDED besides
is the `info` that keeps the fact on the report; § *What the record costs* says
why it is not optional.

## What the record costs, and why it is not optional

`fam_release_tag_publication` turns every per-repository `Skip` into an `info`
whose text is the skip's reason, and it does that on purpose: the family's own
docstring says a skip is *"reported, not dropped"*, for the reason
`release-inventory-drift` records for the same shape. Retiring the skip without
putting the fact anywhere would therefore DROP that record — and with it the
obligation #688 ratified, that the held case state the presence.

So the fact is stated as an `info` on `contracts/CHANGELOG.md`. **Not on the
manifest**, where every other finding of this family lands: a finding's identity
in this capability is `(family, repository, path)`, and a trace sharing the
manifest's identity with the grading findings it accompanies would be masked by
any one of them. **And it claims no more than the presence gives it** — the
commit is held and no readable blob came back at that path, never *"the commit
carries no such file"*, which a store holding the commit and its trees can still
fail to license. That narrowing is #688's, and it is carried rather than
re-derived.

**IT IS AN `info`, AND THAT IS THE WHOLE OF ITS BLAST RADIUS.** It cannot redden
a `--fail-on error` run, it cannot fail the cut-time release-tag gate (which
refuses on `error` and `warning`), and it is emitted only where a bundle is
actually in scope — a repository below the enforcement floor with no changelog
is answered with silence, exactly as it always was.

## Impact

**Behaviour: one reachable state, and it gains the grading it was owed.** A
repository whose published tip this clone HOLDS, which declares or has cut a
bundle at or above the enforcement floor, and at which no readable
`contracts/CHANGELOG.md` blob is reachable, is no longer skipped: its bundles
are graded exactly as they are graded at an empty changelog, and one `info`
records why no declaration was read. Where the commit is NOT held the skip
stands, in the words it had. No severity, threshold, floor, path or arm of any
existing finding moves.

**Nothing in this repository changes, measured rather than assumed.**
openxFactory carries a readable `contracts/CHANGELOG.md` at its published tip,
so it never reaches this arm: `python3 scripts/doc-health.py --single-repo .
--family release-tag-publication` returns the same single `info` (the
`contract-v2.6` SPENT record) before and after. **No run that is green today
turns red**, and no `--fail-on error` run can, the one new finding being `info`.
Whether a REAL untagged bundle at a held tip exists anywhere in the estate is
the estate-wide question this lane cannot take from one clone — see
`tasks.md` § 6.1, where it is named as owed at landing rather than claimed.

**Tests:** six ADDED, one CONVERTED, 146 → 152 in that module. The converted
one is `test_an_absent_changelog_says_the_tip_is_held_rather_than_unfetched`,
whose subject was the held case's SKIP; every literal it pinned — the held
words, the unreachability words, and the two negative pins against the manifest
arm's fetch wording and against the over-claiming tree assertion — is asserted
unchanged, on the `info` that now carries them. § *What was edited and why* in
`design.md` D5 records that this is the only existing test touched, and carries
the THREE mutation probes re-taken at the fix-round head — the held-tip split
(5 failed), D3a's tree consultation (3 failed), and the `in_scope` gate on that
consultation (1 failed, and unpinned until this round's sixth added test).

**Doc-health:** the `modified-block-currency` family reads this new active
delta. It drops two canon units, each is named by its own reserved marker, and
every other unit and all 30 scenario titles are carried — so the block is
expected to raise **no** currency finding. The mutation probe that proves the
family read the block at all is recorded in the pull request.

**OpenSpec 1.12:** the pinned CLI's scenario-currency check refuses a
`## MODIFIED` block that OMITS a scenario the current spec still carries. This
block omits none and RETITLES none — it replaces two bullets inside one — so it
adds no undispositioned failure to
`scripts/validate-openspec-cli-pin.py --all --no-cache`.

**No file is added under `openspec/specs/`**, so no codexFactory floor advance
is owed.

## Sequencing

`sequenced_after` is **ELECTIVE HERE AND IS NOT DECLARED**, and the reading is
stated rather than left to inference. Every other writer of this requirement —
`add-release-tag-publication-check`, `declare-spent-bundle-state`,
`add-release-tag-gate`, `amend-published-tip-unreadable-scenario` and
`amend-unreadable-read-sibling-scenarios` — is ARCHIVED, and their text is
already in the canon this block restates. No ACTIVE change writes *Release-tag
publication*; the ledger classes this row `co-modifier` on the archived
partners, exactly as #678's and #688's rows were classed, so **no partner flips
and no MOVEMENT LOG entry is owed.**

## Ratification

**RATIFIED 2026-09-07 by Brett Heap (openxFactory operator authority), in
session, verbatim: _"merge them when green, then ratify 753"_.** The first clause
of that word landed three pull requests — openxFactory **#752** (`3a28face`) and
**#755** (`64aad02e`), and xFactory-Hermes-Install **#72** (`06c9083d`) — and the
second clause is this act. The citation is the front matter's single `Ratified:`
line and the record is `review/ratification-2026-09-07.md`; the verification run
captured beside it is `review/verification-2026-09-07.md`. Issue **#750** and the
archived predecessor's **D6** remain the ORIGIN — they record a defect and name a
successor as owed, and they decide no wording; this word is the separate act that
ratifies the text.

**THE VETO POINT WAS PUT AND WAS NOT TAKEN.** `design.md` **D1** — option **A**
(split the arm on the fact the read already establishes, and GRADE the
held-and-absent case) against option **B** (keep the skip and give the held case
a distinct reason class only) — was carried as this packet's veto point in the
pull request body, in `tasks.md` § 1.2 and in the README row, with B written out
beside A carrying its cost. The word ratifies **option A as designed**, **and it
ratifies A's stated cost with it**: A changes which findings an in-scope
repository receives, which is exactly why D6 refused to take it inside a packet
whose claim was "one skip's TEXT", and the direction is the conservative one — a
`Skip` becomes the grading an empty document already receives, so nothing this
family reports today becomes quieter.

**AND THE SECOND DECISION WAS PUT SEPARATELY, AND WAS NOT VETOED EITHER**:
`design.md` **D2**, whether the retired skip's fact is carried onto an `info` or
simply stops being reported. D2 takes the `info` — one finding, at `info`, on
`contracts/CHANGELOG.md`, gated on `in_scope` — and the alternative is written
out beside it with the ratified obligation it would silently drop.

**WHAT THE WORD DOES NOT REACH.** It does not archive this packet: `code_surface`
is non-empty, so under `release-realization` the archive is a separate act on
merged-plus-green realization evidence and on a separate word (`tasks.md`
§ 6.4), which is why the pull request says `Refs #750` and not `Closes`. It does
not reach the estate-wide run (§ 6.1), the floor exemption over the skip
(§ 6.5), the late-`Skip` trace drop and its two named remedies (§ 6.6), or the
other arms of this family (§ 6.2). All five were present in the text the word was
given over, and all five remain owed.

## What this proposal does NOT claim

- It does not change what the family READS, at which severity it reports any
  existing finding, or which repositories it speaks about.
- It does not add, move or strengthen a presence probe. `obtain_commit` runs
  above both reads and this packet consumes its answer; no second round trip is
  introduced, and the arm it gates costs one comparison.
- It does not touch the UNFETCHED half. Where the commit is not held the skip
  stands, and the test that pins it is unchanged.
- It does not claim the state it grades is common. In this repository it is
  unreachable, and on the aggregation nightly nine of the ten governed
  repositories return at the MANIFEST arm long before this one — a fact recorded
  by #612 and carried in canon, and cited here rather than re-measured, because
  a doc-health run over the aggregation FETCHES into every governed clone and
  this lane will not write into checkouts it does not own (`tasks.md` § 6.1).
- It does not touch `verify_tag` or issue **#338**. The manifest scenario's
  closing `AND` that names them is canon and is carried byte-identical.
- **It does not amend the archived deltas that carry the retired bullets.**
  `openspec/changes/archive/2026-09-05-amend-unreadable-read-sibling-scenarios/specs/doc-health/spec.md`
  is an archived record of what was ratified; editing it would mutate history
  and put the archived delta out of agreement with the canon
  `promotion-fidelity` compares it against. The remedy is in canon, where the
  live rule is.
- **It does not report a marker that names something no unit matches.** That
  silence is `suppression`'s third resolution and it is openxFactory **#729**'s
  subject, not this packet's. Both markers here name units this block genuinely
  drops, and the pull request carries the measurement showing the family read
  them.
