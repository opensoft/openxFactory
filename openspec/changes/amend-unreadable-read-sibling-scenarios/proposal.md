---
code_surface: openxFactory — ONE skip string and its comment in `scripts/doc_health/release_tag_publication.py`, plus the test that pins it in `tests/doc-health/test_release_tag_publication.py`. The reading that decides this is § Why the code surface is NOT `none`, and it is the reading `amend-published-tip-unreadable-scenario` said this successor owed before it copied the wording across. The PRESENCE PROBE the amended scenario requires is already there and is NOT added here — `obtain_commit` runs before both `manifest is None` arms (PR #646, `2177b2a2`) and the changelog read inherits it completely. What is NOT already there is the OTHER half of the same shape: the manifest read answers its present-and-empty case in words that STATE the presence, and the changelog read answers the identical state in words that do not, so canon written in the manifest scenario's shape would out-run the checker by one bullet. That bullet is made true in this packet rather than owed by it. NOTHING ELSE MOVES: no severity, no threshold, no enforcement floor, no finding path, no arm, no workflow, no contract member, and no other family. The skip's substrings that the suite already pins (`contracts/CHANGELOG.md could not be read at the published tip`, `not the same fact as there being none`, and the in-scope bundle name) are all still carried, so the existing assertions hold unchanged and the new ones are ADDED beside them.
target_release: implemented (the openxFactory main line). No contract bundle is cut, no release tag is owed, nothing under `contracts/` is touched, and no digest set moves. Under `release-realization` a non-empty code surface archives only on merged-plus-green realization evidence; the tasks are individually executable, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green pytest and doc-health runs.
Status: draft
Proposed: 2026-09-05
Origin: openxFactory issue **#662** and the ARCHIVED `amend-published-tip-unreadable-scenario`, whose `tasks.md` § 4.2 records this sibling as an OWED SUCCESSOR and states the one reading it owes first. **THIS PACKET IS NOT APPROVED AND DOES NOT CLAIM TO BE.** `.openspec.yaml` carries drafting provenance and no approval pair — the lawful unapproved shape `add-drafted-proposal-origin` added — and this document carries `Status: draft`. No word of Brett Heap's ratifies it; § Ratification names what is owed.
---

# Proposal: amend-unreadable-read-sibling-scenarios

Status: draft
Proposed: 2026-09-05, in lane `openxfactory-1`, as the successor
`amend-published-tip-unreadable-scenario` named before it landed.
Origin: openxFactory issue **#662** (the defect class) and that packet's own
`tasks.md` § 4.2 (this sibling, named as owed). **NOT RATIFIED.** The origin is
a record of what is owed, not an approval of this text; ratification is a
separate act and has not happened.

## Why

**The clause `amend-published-tip-unreadable-scenario` retired was written
twice, and only one copy was removed.**

`doc-health`'s promoted *Release-tag publication* carried the scenario *The
manifest cannot be read at the published tip* with a `WHEN` that named ONE
cause for a read that answers nothing:

> the blob read for the manifest at the published tip answers nothing — **the
> commonest cause being a checkout that has not fetched that commit**

PR **#678** replaced that bullet with one naming BOTH facts, added the
`WHEN`-side obligation to establish which holds, and added the bullet requiring
the present-but-empty case to be answered in ITS OWN WORDS. The measurement
behind it is openxFactory **#612**: on the aggregation nightly the commit WAS
fetched and nine of the ten governed repositories simply carry no
`contracts/manifest.yaml` at all, so the retired parenthetical sent every reader
of the report to look for a fetch defect that was not there.

**The sibling scenario carries the identical clause, word for word, over
`contracts/CHANGELOG.md`** — `openspec/specs/doc-health/spec.md:2818`. #678's
own `proposal.md` records finding it, records that it did NOT widen its ratified
scope to take it, and names it as the successor this packet is. It also names
the one reading the successor owes first, which § below answers.

## What Changes

**ONE scenario's bullets, inside ONE `## MODIFIED` requirement — and ONE skip
string in the family, so canon does not out-run the checker.**

The delta restates `doc-health`'s *Release-tag publication* in full — every body
unit and all 30 promoted scenario titles, byte-faithful, INCLUDING #678's
amendment note and its `Removed from canon by` marker, which promoted into canon
with the requirement and are carried rather than restated — and changes exactly
this, in the scenario *The changelog cannot be read at the published tip*:

- the `WHEN` bullet is **REPLACED**, from naming one cause as commonest to
  naming **both facts** the single answer stands for;
- an `AND` bullet is **ADDED** on the `WHEN` side requiring that the family have
  **established which of the two holds** before choosing its words — and saying
  how it is established HERE: by inheritance, and completely;
- a second `AND` bullet is **ADDED** requiring that where the commit IS held and
  the file is simply absent, the skip say THAT and state the presence.

The promoted `THEN` and the promoted closing `AND` (*"not fetched is not an
answer, in either direction"*) are carried **byte-identical**.

**ONE canon unit is dropped, and it is declared** by the reserved marker
`**Removed from canon by amend-unreadable-read-sibling-scenarios
(2026-09-05):**`, naming the old `WHEN` verbatim as a code span with the reason.
Same shape, same reason, one document over from #678's.

**And the family's changelog skip is made to say the fact it already has.**

## The reading the successor owed, and its answer

#678's `tasks.md` § 4.2: *"the changelog read has no presence probe of its own,
it inherits the manifest read's."* That is the reading, and it comes back in two
halves that point opposite ways.

**THE PROBE: INHERITED, AND COMPLETE.** `check_repo` calls `obtain_commit` for
the published tip BEFORE any read, and both `manifest is None` arms return
before the changelog is looked at. So the changelog guard is only ever reached
with a manifest that READ at that same commit — and `blobs_at` sends
`<commit>:<path>` to `cat-file --batch`, which answers *missing* for EVERY spec
of a commit the clone does not hold. A manifest that read is therefore proof the
commit is held. At this read the unfetched fact is not the rarer one: **it is
excluded.** The `WHEN`-side establishing obligation is satisfied by the code as
it stands, and this packet adds no probe.

**THE WORDS: NOT INHERITED.** The manifest read has TWO skips and the
present-and-empty one states the presence in as many words. The changelog read
has ONE, and it says only that the file *"could not be read at the published
tip"* — the shape a reader is entitled to read as a fetch defect, which is
exactly #612's cost, one document over. The comment above it still names *"a
checkout that has not fetched the published tip"* as the commonest cause, which
at that position cannot be the cause at all.

## Why the code surface is NOT `none`

Because the third bullet of the shape is a `MUST` about words the family does
not currently use. Writing *"the skip MUST say THAT and MUST state the
presence"* into canon while the checker says something else would make this
packet the inverse of #678: canon out-running the machinery instead of catching
up to it. **So the words are made true here, in the smallest possible edit** —
one `Skip` reason and the comment above it — and the packet declares the
surface rather than declaring `none` and leaving a gap for a later reader to
find.

**The alternative was considered and is recorded in `design.md` D2**: write only
the two bullets the code already satisfies and leave the third out. It was not
taken, and the reason is that it would encode the defect — a canon that permits
answering a held tip in a read-failure's words is the canon #612 was filed
against.

## Impact

**Behaviour: one skip's TEXT, for one reachable state.** A repository whose
published tip declares an in-scope bundle and carries no
`contracts/CHANGELOG.md` is skipped exactly as before, at the same place, with
the same consequence; the reason now says the commit is held and the file is
absent. No severity, threshold, path, arm or finding moves, and the state is not
reachable at all for a repository below the enforcement floor (which returns
`[]`, unchanged).

**Tests:** the three literals the existing changelog test pins are all still
carried, so it passes unchanged; one test is ADDED pinning the two new fragments
and asserting the reason is not mistakable for the manifest arm's
fetch-was-attempted words. `tests/doc-health/test_release_tag_publication.py`
goes 145 → 146.

**Doc-health:** the `modified-block-currency` family reads this new active
delta. It drops one canon unit, that unit is named by the reserved marker, and
every other unit and all 30 scenario titles are carried — so the block is
expected to raise **no** currency finding. The mutation probe that proves the
family read the block at all is recorded in the pull request.

**OpenSpec 1.12:** the pinned CLI's scenario-currency check refuses a
`## MODIFIED` block that OMITS a scenario the current spec still carries. This
block omits none and RETITLES none — it replaces a bullet inside one — so it
adds no undispositioned failure to
`scripts/validate-openspec-cli-pin.py --all --no-cache`. The two failures that
run reports are `#677`'s pre-existing dispositions and are not this packet's.

**No file is added under `openspec/specs/`**, so no codexFactory floor advance
is owed.

## Sequencing

`sequenced_after` is **ELECTIVE HERE AND IS NOT DECLARED**, and the reading is
stated rather than left to inference. The requirement's other writers —
`add-release-tag-publication-check`, `declare-spent-bundle-state`,
`add-release-tag-gate` and `amend-published-tip-unreadable-scenario` — are ALL
ARCHIVED, and their text is already in the canon this block restates. No ACTIVE
change writes *Release-tag publication*; the ledger classes this row
`co-modifier` on the archived partners, exactly as #678's row was classed, so
**no partner flips and no MOVEMENT LOG entry is owed.**

## Ratification

**NOT RATIFIED. NOTHING BELOW HAS BEEN GIVEN.** This packet is authored and
pushed for review; it owes a separate ratification act, and until one exists
every document in it carries `Status: draft` and `.openspec.yaml` carries
drafting provenance with no approval pair. The decision most worth a veto is
`design.md` **D2** — whether the third bullet (and with it the code surface) is
in scope at all, or whether the successor should carry only the two bullets the
checker already satisfies.

## What this proposal does NOT claim

- It does not change what the family reads, at which severity, or which
  repositories it speaks about.
- It does not add, move or strengthen a presence probe. The probe exists; the
  packet's own § reading says so and says why it is complete at this read.
- It does not touch `verify_tag` or issue **#338**. The closing `AND` of the
  manifest scenario that names them is canon and is carried byte-identical.
- It does not claim the promoted `THEN` bullet reads perfectly under the new
  `WHEN`. It is carried verbatim for the same reason #678 carried its own — see
  `design.md` D1, which inherits that decision rather than re-taking it.
- **It does not amend the archived delta of `amend-published-tip-unreadable-scenario`,
  which carries the same clause at
  `openspec/changes/archive/2026-09-05-amend-published-tip-unreadable-scenario/specs/doc-health/spec.md:484`.**
  That file is an archived record of what was ratified; editing it would mutate
  history and would put the archived delta out of agreement with the canon
  `promotion-fidelity` compares it against. The successor's remedy is in canon,
  where the live rule is, and the archived record is left exactly as it landed.
