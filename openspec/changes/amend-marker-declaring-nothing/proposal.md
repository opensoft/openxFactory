---
code_surface: openxFactory — `scripts/doc_health/modified_block_currency.py` and the tests that pin it in `tests/doc-health/test_modified_block_currency.py`. TWO REPORTING GROUNDS ARE ADDED to the marker-defect class and nothing else moves: `suppression`'s existing `if name not in block_texts:` guard gains its `else` half, collecting the names that ARE in the block's own texts and match no canon unit; a second check fires where a `Removed from canon` marker carries neither a name nor a quoted span; and `_arm_marker_defects` renders both through the class's EXISTING template — whose text is unchanged, so the existing `CLASS_MARKERS` probe places every new finding, `_ARM_TEMPLATES` stays at EIGHT and the seventh class (`unplaced-finding drift`) stays silent. NOTHING ELSE MOVES: no parse, no `Marker` field, no severity, no threshold, no arm, no finding class, no template entry, no path, no disposition rule, no workflow, no contract member and no other family. FIVE tests are ADDED beside the existing ones (`tests/doc-health/test_modified_block_currency.py` 139 → 144), ONE assertion is FLIPPED rather than loosened — the test that PINNED the silence issue #856 reports, its fixture unchanged — and ONE test is RENAMED with no assertion and no fixture moved, because its title claimed three grounds. The delta ALSO ADDS TWO SCENARIOS to the MODIFIED block, at its end, one for each ground; no promoted scenario moves, is retitled or loses a bullet.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves and no release tag is owed. Under `release-realization` a non-empty code surface archives on merged-plus-green realization evidence rather than on landing, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` and doc-health runs.
sequenced_after: []
---

# Proposal: amend-marker-declaring-nothing

Status: draft
Proposed: 2026-09-10, in lane `openxfactory-1` (display `openXfactory-1`), on
Brett Heap's word of 2026-09-10, verbatim **"do the 860 856 batch, land each
when green"**, given in session.
Origin: openxFactory
[#856](https://github.com/opensoft/openxFactory/issues/856) and
[#860](https://github.com/opensoft/openxFactory/issues/860), both filed by this
lane at the archive of `amend-marker-defect-reporting`
([#850](https://github.com/opensoft/openxFactory/pull/850) → `250d93d7`), which
owed them as residue `tasks.md` § 5.2 and § 5.7.
**THAT WORD AUTHORIZES THE AUTHORING, NOT THE CONTENT.** It names a batch and a
landing condition; it ratifies no wording and takes neither of the two design
decisions this packet carries. This proposal is therefore a **DRAFT** and
carries **NO APPROVAL PAIR** — `.openspec.yaml` keeps drafting provenance alone
(`proposed_by` + `proposed_on`, no `approved_by`, no `approved_on`), which is
the lawful unapproved shape `add-drafted-proposal-origin` defined, and every
document in the packet carries `Status: draft` to match. Ratification,
promotion and archive are three later acts on three later words.

## Why

**A MARKER IS A DECLARATION, AND THE TWO REMAINING WAYS OF DECLARING NOTHING
ARE STILL SILENT — one of them pinned as a silence by the packet that reported
the other three, and one of them found by that packet's own adversarial pass
and unreachable by any ground it wrote.**

`doc-health`'s *Currency of an active change's MODIFIED requirement blocks*
gives a marker exactly THREE reporting grounds, and says so in terms:

> A MARKER SHALL ITSELF BE REPORTED ON ANY OF THREE GROUNDS, each of them one
> finding at the `info` band this family's marker-defect class already carries:
> it names a unit the block still carries; or a code span standing INSIDE its
> reason matches EXACTLY a unit of the requirement's basis that the block does
> not carry and that no marker declares removed …; or it names something
> matching no unit of the requirement's basis and no unit of the block.

Two other ways of declaring nothing fall outside all three, and BOTH ARE ON THE
RECORD AS DELIBERATE.

**THE FIRST IS A PINNED SILENCE** (openxFactory
[#856](https://github.com/opensoft/openxFactory/issues/856)). A name matching
NO canon unit but matching a unit the MODIFIED BLOCK ITSELF ADDS falls through
`suppression`'s guard and reaches no ground:

```python
matches = by_text.get(name)
if not matches:
    # NAMES NOTHING; BUYS NOTHING — and, where the block does not
    # state it either, the marker is now reported for it.
    if name not in block_texts:
        unmatched.append(name)
    continue
```

`amend-marker-defect-reporting`'s `design.md` D3 wrote the reason where the
decision stood: *"a marker declaring a unit of the block's own addition removed
declares something odd — but which reading is right depends on a rule nobody
has written … Inventing a fourth ground here would repeat exactly the fault
this packet exists to correct, on the same afternoon."* It pinned the silence
with a test so a later act could overturn a DECISION rather than rediscover a
gap. This is that act, and this proposal is that rule.

**THE SECOND IS A MARKER OF CORRECT FORM THAT DECLARES NOTHING AT ALL**
(openxFactory [#860](https://github.com/opensoft/openxFactory/issues/860)). A
`Removed from canon` marker whose tail carries no code span parses to `names =
[]` and `quoted = []`; the per-name loop never runs, so `restated` stays false
and `unmatched` stays empty, and the second pass builds `offending` from
`marker.quoted`, which is empty. It reaches NONE of the three grounds. And the
paragraph is not merely unreported: this requirement's own rule that *"A
paragraph of RESERVED MARKER form … SHALL NOT be a unit of either kind, in
canon or in a block"* exempts it from carriage as well, so a paragraph that
declares nothing is also a paragraph nobody has to carry. That is exactly the
fault the three grounds exist to report, and it is the one case they cannot
reach.

## Why this is NOT a plain fix

**Because the requirement mandates exactly THREE reporting grounds, counts them
in the next sentence, and both new findings are additions to it rather than
implementations of it.** The clause a reader reaches for — *"a declaration that
does not describe the block"* — is the THEN's RATIONALE in canon's scenarios,
not a fourth WHEN. Neither new case satisfies any promoted WHEN: ground three's
scenario reads *"a marker names a code span matching no unit of the
requirement's basis **and no unit of the block**"*, which is precisely the
clause #856's case fails.

And the running code is not wrong about canon either — it says so itself.
`suppression`'s docstring records the block-adds case as *"left silent
deliberately (`design.md` D3): it is text the block ADDS, and reporting it is a
fourth ground nobody has ruled"*, and the promoted sentence was written to
claim what the three grounds REPORT rather than that every marker declaring
nothing is reported, precisely so that it does not claim #860's case.

**A FOURTH AND FIFTH OBLIGATION OVER THE SAME FACTS IS AN AMENDMENT OF THE
REQUIREMENT**, so the remedy is a `## MODIFIED` block with the realization in
the same pull request under `release-realization`'s merged-plus-green rule —
the shape `amend-published-tip-unreadable-scenario` (#685),
`amend-unreadable-read-sibling-scenarios` (#688), `amend-marker-reason-boundary`
(#719) and `amend-marker-defect-reporting` (#850) all took over this same
capability. Both origin issues say so in their own bodies: *"Either is a
`## MODIFIED` delta with its own ruling; neither is a plain fix."*

**ONE PACKET FOR TWO ISSUES, AND THE REASON IS MECHANICAL.** Both amend the
SAME SENTENCE of the same requirement. Two active changes carrying a
`## MODIFIED` block over one promoted requirement is the two-writers shape this
very requirement reports and `release-realization` requires a declaration for —
so splitting #856 and #860 into two packets would manufacture that collision
over a sentence neither could state alone. The two grounds remain SEVERABLE at
ratification, which is what `design.md` D1 and D2 are for.

**The sentence is promoted in ONE place, and that was checked in both
directions.** `document-lifecycle`'s marker grammar says how a deleted unit is
NAMED and says nothing about when a marker is reported, so it needs no
amendment and none is made — and that boundary is exactly what `design.md` D1's
ALTERNATIVE would cross, which is why the alternative is named as the larger
change rather than the smaller one.

## What Changes

**TWO BODY SENTENCES OF ONE PARAGRAPH, inside ONE `## MODIFIED` requirement,
plus two sentences added beside them in that same paragraph, plus two scenarios
at the end of the block.**

- **RETIRED:** the sentence that states THREE grounds and enumerates them, and
  the sentence that counts them (*"Each of the three is a declaration that does
  not describe the block …"*). Both are REPLACED, neither is dropped.
- **REPLACING THEM:** a marker SHALL itself be reported on any of FIVE grounds,
  each one finding at the `info` band the marker-defect class already carries —
  the three that stand, unchanged and in the same order and words, plus:
  **(4)** it names something matching no unit of the requirement's basis and a
  unit THE BLOCK ITSELF STATES, declaring removed from canon a unit canon never
  carried; and **(5)** it is of `Removed from canon` form and its tail carries
  NO code span at all, so that it names nothing, quotes nothing and declares
  nothing while occupying the one paragraph shape this requirement exempts from
  carriage.
- **AND TWO SENTENCES ARE ADDED BESIDE THEM**, one scoping each new ground.
  Ground four *"changes no suppression"* — a name matching no unit of the basis
  never suppressed anything and still suppresses nothing, and the block's own
  addition is not reported for being named. Ground five is read on the
  `Removed from canon` form ALONE: **the PAIRING form names no units by
  construction**, its whole tail being a reason, so a pairing marker carrying no
  code span declares exactly what that form declares and is NOT reported — a
  silence `amend-marker-defect-reporting` already ruled correct — and a
  `Merged into` marker whose tail names no superseded title is a question this
  requirement does not decide, its destination standing in the prefix where that
  form's declaration has always been read.

The two retired units are declared by the reserved marker
`**Removed from canon by amend-marker-declaring-nothing (2026-09-10):**`,
naming each verbatim as a CommonMark code span. The first contains a backtick
(`` `info` ``) so it is fenced with a longer run, exactly as canon's own rule
requires; the second contains none and a single-backtick fence names it whole.
The marker's reason carries NO code span, so the boundary leaves both names
before it and the marker parses to exactly two names and no quoted span —
verified mechanically rather than asserted (`tasks.md` § 4.3).

**TWO SCENARIOS ARE ADDED AT THE END OF THE BLOCK**, *A marker names a unit the
block itself adds* and *A marker of removal form declares nothing at all*.
Without them the two new grounds would promote with nothing exercising them and
would be pinned only by this packet's tests — running code standing in for
canon, which is the shape § *Why this is NOT a plain fix* refuses.

**WHAT IS KEPT AND IS STILL TRUE.** The narrow reading of ground two, the
carriage it preserves, the three-way resolution, the `Merged into` form, the
pairing form, the derivation, the suppression rules, the scenario-title cascade
and its `adds_new_title` gate, the disposition rule, the post-flip standing
paragraph `amend-modified-block-currency-standing` promoted this morning, and
every severity are untouched.

## The corpus measurement

Every marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md`, read through `derive_units` so that fenced
example markers are never offered — the same walk `_corpus_markers()` runs —
taken on 2026-09-10 on `main` @ `e0638f11`, the corpus AS IT STOOD BEFORE THIS
PACKET:

| measure | 2026-09-09 (`amend-marker-defect-reporting`) | 2026-09-10 (this packet) |
| --- | --- | --- |
| markers of any form in the corpus | — | **26** |
| unit-naming markers (`Removed from canon`, `Merged into`) | 16 | **17** |
| pairing-form markers | — | **9** |
| `Removed from canon` markers with an EMPTY tail (ground five) | — | **0** |
| unit-naming markers with an empty tail, any form | — | **0** |
| active MODIFIED blocks the family reads | — | **30** |
| of those, blocks carrying a unit-naming marker | 2 | **2** |
| marker-defect findings a run raises today | 0 | **0** |
| findings ground four would raise today | — | **0** |
| findings ground five would raise today | — | **0** |

**THE SHIPPING PATH IS WHERE THE ZERO IS MEASURED.** The family reads MARKERS
only inside active `## MODIFIED Requirements` blocks. Of the thirty active
blocks on this tree exactly TWO carry a unit-naming marker —
`add-chain-attestation` and `add-composed-view-authoring`, both `Merged into`,
one name each, each matching its resolved basis, neither quoting a code span in
a reason and neither naming a unit its own block adds. So both new grounds have
a population of ZERO today, measured rather than assumed, and the silences they
retire have never yet cost anybody a row.

## Impact

**Behaviour: none observable on this corpus today, by measurement.**
`python3 scripts/doc-health.py --single-repo .` returns a finding set **IDENTICAL
to `origin/main`'s, LINE FOR LINE** — 350 lines on both trees, the two
`- severity=` sets differing in nothing, this packet's own block included, which
raises ZERO findings from any family and adds no row of its own. Both new grounds have a population of
zero at landing, which is what makes them normative for the next marker written
rather than a sweep of the present one.

**Tests:** `tests/doc-health/test_modified_block_currency.py` **139 → 144**, and
**ONE existing assertion is FLIPPED**, named here rather than left to be found
in the diff: `test_a_name_matching_a_unit_the_BLOCK_adds_stays_SILENT` asserted
`findings == []` and was the pin `design.md` D3 put on the silence #856
reports. Its FIXTURE IS UNCHANGED — the same canon unit, the same block
addition, the same marker — only the assertion and the name move, to
`test_a_name_matching_a_unit_the_BLOCK_adds_reports_the_marker`, with the
reason written where the assertion stands. **ONE existing test is RENAMED and
not otherwise edited**: `test_a_well_formed_marker_is_silent_on_all_three_grounds`
→ `…_on_all_five_grounds`, no assertion and no fixture moved, because a title
claiming three grounds would tell the next reader the class had three. No other
existing test is edited. The full `tests/doc-health` suite goes **1684 → 1689**.

**Doc-health:** the `modified-block-currency` family reads this new active delta.
It drops two canon units, both are named by the reserved marker, every other
body unit, all nineteen promoted scenario titles and all their bullets are
carried, and the two scenario titles the block ADDS are titles the arms never
report — so the block raises ZERO findings from its own family, which is
MEASURED in the pull request rather than expected.

**AND THIS BLOCK IS ITS OWN SELF-REFERENCE TEST, IN THE SAME WAY ITS PREDECESSOR
WAS** (`design.md` D5). `amend-modified-block-currency-standing`'s promoted
`Removed from canon` marker names five sentences canon no longer carries, so
restating it in this block would make this block report ITSELF under ground
three. It is deliberately NOT restated, on this requirement's own rule that *"a
marker is NOT a carriage unit, in either direction"*, and the block's `AMENDED
BY` note says so in terms. **GROUND FOUR ADDS A SECOND EDGE OF THE SAME KIND**,
disclosed rather than left to be found: after this packet, a marker naming a
unit its own block adds is reportable, so an author who writes a declaration
and then writes the declared text into the same block is told about it.

**Severity and resolution: NOTHING MOVES.** The new findings carry the
marker-defect class's existing `info` band (`_LEDGER_SEVERITY`) and its existing
action, so no `--fail-on` configuration reds on them; and they inherit — as
every class of this family does since the flip of 2026-08-31 (issue #357) — the
family's `contested` row in `families.FAMILY_RESOLUTION`, which has no per-class
grain. **This packet claims no exemption from that and creates no new
mechanism**: a marker-defect finding that stops being reported without a citation
already owes one under `report.uncited_resolutions`, and with a population of
zero at landing there is nothing that can disappear. The per-class grain of that
rule is `amend-modified-block-currency-standing`'s owed successor
[#893](https://github.com/opensoft/openxFactory/issues/893) and is not this
packet's.

**OpenSpec 1.12:** the block omits no scenario and retitles none — it replaces
two body sentences, adds two beside them and appends two scenarios — so it adds
no undispositioned failure to `scripts/validate-openspec-cli-pin.py --all
--no-cache`, which is run in the pull request rather than assumed.

**No file is added under `openspec/specs/`**, so no codexFactory floor advance is
owed.

## Sequencing

`sequenced_after: []` is DECLARED, as an explicit root claim rather than an
omission, which is the shape the last writer of this requirement
(`amend-modified-block-currency-standing`) used and the shape three other rows
of the corpus ledger carry. **No ACTIVE change carries a `## MODIFIED` block for
this requirement**, grepped over `openspec/changes/` on the tree this packet is
authored on: the three active changes that name the requirement at all
(`prepare-openspec-1-12-readiness/tasks.md`,
`disposition-codexfactory-floor-relocation-retitle/design.md`,
`disposition-codexfactory-declared-renames/design.md`) mention it in prose and
carry no delta over it. Measured on the archive rather than recited: the
requirement was PROMOTED by `add-modified-block-currency-check` (an `## ADDED`
block, 2026-08-27) and exactly THREE archived changes carry a `## MODIFIED`
block for it — `amend-marker-reason-boundary`, `amend-marker-defect-reporting`
and `amend-modified-block-currency-standing` — all archived, their text already
in the canon this block restates. The ledger row is seeded with `--moved-by`
this pull request and classes `co-modifier` on those ARCHIVED partners only, so
no partner row flips and no MOVEMENT LOG entry is owed.

## Ratification

**NOT RATIFIED.** Brett Heap's word of 2026-09-10, verbatim *"do the 860 856
batch, land each when green"*, is the ORIGIN of the authoring: it names the
batch and a landing condition and decides no wording. No approval pair is
declared in `.openspec.yaml` and none is implied. **The two decisions most worth
a veto are `design.md` D1 (#860) and D2 (#856)**, each carried with the
recommended encoding first and the alternative with its cost written out beside
it, in the pull request body, in `tasks.md` § 1 and on both origin issues. A
veto of D1 is a veto of ground FIVE alone; a veto of D2 is a veto of ground FOUR
alone; the two rest on no shared predicate.

**WHAT A RATIFICATION WOULD NOT REACH.** `code_surface` is non-empty, so under
`release-realization` the archive is a separate act on merged-plus-green
realization evidence and on a separate word (`tasks.md` § 6), and openxFactory
**#856** and **#860** therefore close at archive rather than at this landing.

## What this proposal does NOT claim

- It does not claim either silence has ever hidden a real deletion. Neither has,
  and the measurement that says so is in this document and in a test.
- It does not change what a marker SUPPRESSES. Both new grounds report and
  suppress nothing; the three-way resolution is untouched.
- It does not change any parse. `parse_marker` and `Marker` are untouched, and
  no marker in the estate parses differently after this packet than before it.
- **It does not touch the PAIRING form.** That form names no units by
  construction, its silence was ruled correct by `amend-marker-defect-reporting`
  (`design.md` D3), and ground five is scoped away from it in canon, in the code
  and in a test.
- **It does not report a `Merged into` marker whose tail names no superseded
  title.** Its DESTINATION stands in the prefix, where that form's declaration
  has always been read, so whether such a paragraph declares nothing is a
  question nobody has ruled — and inventing a sixth ground here would repeat the
  fault the predecessor packet exists to correct. Left silent deliberately,
  pinned by a test, recorded as residue at `tasks.md` § 7.1.
- It does not amend `document-lifecycle`, whose marker grammar carries no
  reporting rule — and `design.md` D1's rejected alternative is precisely the
  amendment that would.
- It does not widen the uncited-resolution rule to finding-class grain, which is
  openxFactory #893 and belongs to the packet that filed it.
- **It does not edit the promoted markers it counts**, nor the archived deltas
  that carry them. They are records of ratified removals.
