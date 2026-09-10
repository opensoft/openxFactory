# Design: amend-marker-declaring-nothing

Status: ratified
Ratified by: amend-marker-declaring-nothing — 2026-09-10, Brett Heap, "ratify as encoded" (record `review/ratification-2026-09-10.md`)
Date: 2026-09-10
Kind: design

## 0. The brief

openxFactory issues **#856** and **#860**, filed for the queue on 2026-09-09 at
the archive of `amend-marker-defect-reporting` (PR #850 → `250d93d7`), which
owed them at its own `tasks.md` § 5.2 and § 5.7. Brett Heap's word of
2026-09-10, verbatim **"do the 860 856 batch, land each when green"**,
commissioned this authoring and ratified nothing — it stays recorded as the
ORIGIN of the AUTHORING.

**THE PACKET HAS SINCE BEEN RATIFIED**, by a second word of 2026-09-10 —
verbatim **"ratify as encoded"**, recorded on PR
[#908](https://github.com/opensoft/openxFactory/pull/908#issuecomment-5623230781)
at 2026-09-10T18:06:52Z, record `review/ratification-2026-09-10.md` — which
reaches **D1** and **D2** below and resolves BOTH as **A**.

Each issue offered TWO encodings and asked for a ruling first. This document
took one of each, wrote the other out beside it with its cost, and named the
choice as that issue's veto point. **D1 IS #860's AND D2 IS #856's, AND THEY
WERE INDEPENDENT**: a veto of D1 would have been a veto of ground FIVE alone and
a veto of D2 a veto of ground FOUR alone, because the two grounds share no
predicate, no field and no branch. **NEITHER VETO LANDED**, so both grounds
stand exactly as encoded and this page's alternatives are the record of what was
put and declined.

## D0 — the measurement, taken before the design

Every marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md`, read through `derive_units` (so this
requirement's own written-out examples, which are complete markers, are never
offered — exactly as they are never offered to a run). Taken 2026-09-10 on
`main` @ `e0638f11`, the corpus BEFORE this packet:

| measure | 2026-09-09 | 2026-09-10 |
| --- | --- | --- |
| markers of any form | — | **26** |
| unit-naming markers (`Removed from canon`, `Merged into`) | 16 | **17** |
| pairing-form markers | — | **9** |
| `Removed from canon` markers with an EMPTY tail | — | **0** |
| unit-naming markers with an empty tail, either form | — | **0** |
| active MODIFIED blocks the family reads | — | **30** |
| of those, blocks carrying a unit-naming marker | 2 | **2** |
| marker-defect findings a run raises | 0 | **0** |

**THE SHIPPING PATH IS WHERE BOTH ZEROS LIVE.** The family reads MARKERS only
inside active `## MODIFIED Requirements` blocks. Of the thirty active blocks
exactly TWO carry a unit-naming marker — `add-chain-attestation` and
`add-composed-view-authoring`, both `Merged into`, one name each matching its
resolved basis, neither quoting a code span in a reason and neither naming a
unit its own block adds. So both grounds have a population of ZERO today,
measured rather than assumed, and neither silence has yet cost anybody a row.

**AND THE ZEROS ARE ASSERTED AS TESTS, NOT ONLY AS FIGURES**
(`test_no_marker_in_this_corpus_raises_either_ground_ADDED_HERE_today`), as
CEILINGS rather than exact counts so that an unrelated marker landing later is
not read as a regression of these grounds.

## D1 — RULED A (#860): report it (doc-health), NOT un-form it (document-lifecycle)

**RULED 2026-09-10 by Brett Heap, verbatim *"ratify as encoded"*, as a
MULTIPLE-CHOICE ruling over this decision** (given in session and recorded on PR
#908 at 2026-09-10T18:06:52Z; record `review/ratification-2026-09-10.md`).
**THE RECOMMENDATION WAS TAKEN, SO NOTHING IN THE DELTA MOVES**: ground five
stands as encoded, its scenario stands, its two tests stand, and
`document-lifecycle` is not amended. Option B is retained on this page as the
record of what was put and declined rather than as work owed — and it is what
made the choice a choice rather than an author's preference.

**A — RECOMMENDED, AND WHAT THE DELTA ENCODES.** A paragraph of
`Removed from canon` form whose tail carries no code span stays a MARKER and is
REPORTED, as a fifth ground of the marker-defect class, at the same `info` band
through the same template.

- **It is the fault the grounds already exist to report.** The other four all
  say one thing: a declaration that does not describe the block is unusable as
  evidence about the block. A marker that names nothing describes the block
  LESS than any of them, and reporting it needs no new concept, no new class,
  no new action and no new template.
- **It leaves the grammar where the grammar is.** `document-lifecycle` says how
  a deleted unit is NAMED; `doc-health` says when a marker is REPORTED. This
  keeps that boundary, which `amend-marker-defect-reporting` § 2.4 checked in
  both directions and left untouched.
- **It costs one predicate and no parse.** `marker.form == "removed" and not
  marker.names and not marker.quoted` — three fields the parser already
  derives. No `Marker` field is added, no regex moves, and every marker in the
  estate parses exactly as it did.
- **Its failure direction is a report, never a silence.** Nothing stops being
  checked; one paragraph starts being reported.

**B — REJECTED FOR ITS COST, AND IT IS THE ISSUE'S OWN SECOND OPTION RATHER
THAN A STRAW ONE.** Write a GRAMMAR rule in `document-lifecycle` that a
`Removed from canon` paragraph carrying no code span is NOT of marker form —
the issue calls it *"the cheaper encoding and the larger semantic change, which
is why it needs the ruling first"*, and that is exactly right:

1. **It is cheaper to encode and larger in effect.** In canon it is one clause
   added to the form anchor. In the code it is a `return None` in
   `parse_marker`. But the paragraph does not become nothing — **it becomes
   PROSE**, and prose in a MODIFIED block is a BODY UNIT.
2. **So the paragraph enters the carriage arms, in both documents.** As a unit
   of the block it must be carried; as a unit of CANON, once such a block
   promotes, every later block must restate it forever — which is precisely
   what this requirement's *"A marker is NOT a carriage unit, in either
   direction"* paragraph exists to prevent, and which it justifies by saying
   the alternative would make *"every later block … restate every marker any
   predecessor ever wrote, forever"*.
3. **The author is told the wrong thing.** Under B the finding is a carriage
   ledger row saying the block does not carry a paragraph — pointing at the
   BLOCK's completeness rather than at the empty declaration. Under A the
   finding names the marker, its change id and its date, and hands the author
   this class's fixed action: *"name a unit the block does not restate, or drop
   the declaration"*, which is the actual remedy.
4. **The rule moves to a capability that carries no reporting rule at all**,
   so `doc-health` would then be silent about a defect `document-lifecycle`
   defines — the split `amend-marker-defect-reporting` § 2.4 deliberately did
   not make.
5. **It is not reversible by wording.** A ratified grammar rule that such a
   paragraph is not a marker makes it a unit; retiring that later means
   retiring a UNIT from canon, with a marker, in another `## MODIFIED` block
   over the same requirement.

**THE COST OF VETOING A, AND IT DID NOT LAND.** A veto would have withdrawn
ground five from the delta and from `suppression`; the two `Removed from
canon`-with-no-span tests would have come out; canon would have kept FOUR
grounds with the sentence re-authored to say so; and the case would have been
filed back as an unruled grammar question against `document-lifecycle`, where it
needs its own packet, its own scenarios and a migration story for any paragraph
the new grammar reclassifies. **NOTHING ELSE IN THIS PACKET WOULD HAVE MOVED**:
ground four, its scenario, its test and its measurement were untouched either
way, because D1 and D2 share no predicate. The ruling of 2026-09-10 took A, so
none of that was performed.

## D2 — RULED A (#856): report it, NOT rule the silence correct

**RULED 2026-09-10 by Brett Heap, verbatim *"ratify as encoded"*, as a
MULTIPLE-CHOICE ruling over this decision** (given in session and recorded on PR
#908 at 2026-09-10T18:06:52Z; record `review/ratification-2026-09-10.md`).
**THE RECOMMENDATION WAS TAKEN, SO NOTHING IN THE DELTA MOVES**: ground four
stands as encoded, its scenario stands, and the assertion this packet flipped
STAYS FLIPPED — the silence the predecessor pinned is overturned, which is what
the pin was written for. Option B is retained on this page as the record of what
was put and declined.

**A — RECOMMENDED, AND WHAT THE DELTA ENCODES.** A name matching NO unit of the
requirement's basis and matching a unit THE BLOCK ITSELF ADDS is REPORTED, as a
fourth ground, at the same `info` band through the same template.

- **A block cannot lawfully declare removed from canon a unit canon never
  carried.** The marker's own words are *"Removed from canon by"*. Naming the
  block's own addition asserts a removal that never happened, of text that was
  never there.
- **It is the OTHER HALF of a branch that already reports.** `suppression`'s
  guard is `if name not in block_texts: unmatched.append(name)`. Ground three
  reports the `if`; ground four reports the `else`. The two are disjoint by
  construction — a name matching no canon unit is either stated by the block or
  it is not — so a marker cannot be double-reported and the two rows are two
  different edits.
- **It costs one list and one branch**, no parse, no field, no template.
- **The silence was PINNED, not overlooked.** `design.md` D3 of the predecessor
  put a test on it so *"the silence is a decision a later act can overturn
  rather than a gap it has to rediscover"*, and filed #856 to overturn it. This
  is the act that test was written for, and flipping it is the whole edit.

**B — REJECTED, AND IT IS THE ISSUE'S OWN SECOND OPTION.** Rule the silence
CORRECT and say so in canon in one sentence: *"a name matching a unit the block
ADDS is out of scope"*. Its cost, written out:

1. **It ratifies a shape with no honest reading.** Nobody has offered an
   account of what a marker naming the block's own addition MEANS. B would
   promote a rule that such a marker is fine while leaving the question of what
   it declares permanently unanswered.
2. **It is silent in the direction that hides.** The author gets NO row: not for
   the marker, not for the addition (an addition is text no arm reads), not for
   anything. Under A they get one `info` row naming the marker.
3. **It costs the same amendment.** B is also a `## MODIFIED` block over the
   same sentence with its own ruling and its own scenario — the issue says so —
   so it buys no work, only a different answer.
4. **It is the harder rule to retire.** A ratified out-of-scope clause is a
   ratified permission; withdrawing it later means retiring a unit from canon
   under a marker, in a third amendment of this sentence in five days.

**THE COST OF VETOING A, AND IT DID NOT LAND.** A veto would have withdrawn
ground four; the flipped test would have flipped back to its ratified silence
and kept its old name;
`test_a_name_matching_a_unit_the_BLOCK_adds_reports_the_marker`'s
two-shapes-in-one-marker half would have come out; and canon would have gained,
instead, the one sentence B asks for, so that the next reader found a decision
rather than a gap. **NOTHING ELSE IN THIS PACKET WOULD HAVE MOVED**: ground
five, its scenario, its tests and its exclusions were untouched either way. The
ruling of 2026-09-10 took A, so none of that was performed.

## D3 — the band: `info`, the same as grounds two and three, and why not `warning`

Both new findings carry `_LEDGER_SEVERITY` (`info`) and the marker-defect
class's existing action, so no `--fail-on` configuration reds on them and the
class needs no new registration.

`warning` was considered and refused on THIS family's own precedent: exactly
ONE arm of it carries `error` — the scenario-title arm, the one that carries the
gate — and it got there by the ruling of 2026-08-27, *"MEASURE FIRST, THEN
FLIP"*, after two nightly runs measured its population at zero across every
governed repository. A ground landing at a gating band on the day it is written
would be the shape that ruling exists to refuse. The population of both new
grounds is zero today, so the honest launch band is the one the class already
carries, and a flip remains available later as a ruling like any other.

**AND THEY INHERIT THE FAMILY'S `contested` ROW, WHICH IS SAID PLAINLY BECAUSE
IT IS ALREADY TRUE.** `families.FAMILY_RESOLUTION` has carried
`"modified-block-currency": CONTESTED` since 2026-08-31 (issue #357), that table
has no per-class grain, and `runner.main` applies it by `Finding.family` alone —
which promoted canon now states in terms, `amend-modified-block-currency-standing`
having landed that sentence this morning. This packet claims no exemption and
creates no new mechanism, and with a population of zero at landing there is
nothing that can disappear between two reports. The per-class grain of the
uncited-resolution rule is openxFactory #893 and is not this packet's.

## D4 — ONE TEMPLATE FOR FIVE GROUNDS, and its opening does not move

The five grounds share a band (`info`), a class (`marker-defects`) and an ACTION
(*"name a unit the block does not restate, or drop the declaration"*). This
module already ruled what that means, in `TEMPLATE_PAIRING`'s own comment, on
Brett's amendment of 2026-08-28 (*"Amend: shape = arm template, all
interpolations masked"*): one SHAPE is one TEMPLATE is one map entry, and the
count of `_ARM_TEMPLATES` is a count of REMEDIES.

So `TEMPLATE_MARKERS`' TEXT IS NOT EDITED AT ALL by this packet — the two new
clauses go into the `{why}` field `amend-marker-defect-reporting` already added.
Three consequences, all checked rather than argued:

- **The existing `CLASS_MARKERS` probe places every new finding.** It reads
  `_BLOCK_HEAD + r"carries a '\w+' marker by "`, which is the template's
  unchanged opening — so the seventh class (`unplaced-finding drift`) stays
  silent and no map entry is owed.
- **`_ARM_TEMPLATES` stays at EIGHT**, so the standing count assertions and the
  drift grain hold untouched.
- **Neither new WHY clause may carry another template's fixed prose in order**,
  or one rule text could match two templates and red the partition the shape
  mask rests on. `test_each_ground_added_here_matches_exactly_one_arm_template`
  holds that property instead of trusting the wording.

Ground five's clause is the module's first WHY with NO interpolation
(*"which names no unit and quotes no span, its tail carrying no code span at
all"*), which is correct rather than an omission: there is no name and no span
to name, and a `{}`-free constant is what says so.

## D5 — the self-reference hazard, discharged the same way its predecessor discharged it

`amend-modified-block-currency-standing`'s promoted `Removed from canon` marker
names five sentences canon no longer carries — the removal is what the marker
declares — so those names match no unit of the requirement. **Restating that
marker in this block would make this block report ITSELF under ground three.**
It is deliberately NOT restated, on this requirement's own rule that *"a marker
is NOT a carriage unit, in either direction"*, and the block's `AMENDED BY` note
says so in terms, so a reader does not read the omission as an oversight.

**GROUND FOUR ADDS A SECOND EDGE OF THE SAME KIND, DISCLOSED HERE RATHER THAN
DISCOVERED LATER**: after this packet, a block that names a unit its own text
adds is reportable. Measured on this tree: no active block does it, so the
population of that consequence is also zero today.

**THIS PACKET'S OWN MARKER IS WRITTEN TO SURVIVE ITS OWN RULES, AND THAT IS
MEASURED RATHER THAN ASSERTED** (`tasks.md` § 4.3). Two names, each matching a
canon unit the block does not carry (so ground one cannot fire and grounds three
and four cannot be reached); a reason CARRYING NO CODE SPAN AT ALL (so ground
two has nothing to resolve); and names present (so ground five is vacuous). The
family's own derivation over the branch reports **0 marker defects** on it.

## D6 — the two exclusions ground five is written around

**THE PAIRING FORM IS NOT THIS CASE, AND ITS SILENCE STAYS RULED CORRECT.**
``**Modified over `<basis>`'s addition by …**`` names NO units by construction —
its whole tail is a reason, which is why `parse_marker` gives it its own branch
and why `Marker.quoted` is empty for it. `amend-marker-defect-reporting`'s
`design.md` D3 ruled that silence correct, and ground five does not disturb it:
the ground is read on the `Removed from canon` form ALONE, in canon, in the code
(`marker.form == "removed"`) and in a test.

**AND THE `Merged into` FORM WITH AN EMPTY TAIL IS DELIBERATELY LEFT ALONE.**
Such a marker names no superseded title, but its DESTINATION stands in the
prefix, where that form's declaration has always been read — so whether it
declares nothing, or declares a destination that absorbed nothing named here, is
a question nobody has ruled. #860 scopes itself to the `Removed from canon`
form; inventing a sixth ground here would repeat the fault the predecessor
packet exists to correct, on the day after it corrected it. Left silent
deliberately, PINNED by
`test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT` so the silence is a
decision a later act can overturn, and recorded as residue at `tasks.md` § 7.1.
Population zero, measured with the rest.

## D7 — ONE PACKET FOR TWO ISSUES, and the reason is mechanical

Both issues amend the SAME SENTENCE of the same promoted requirement. Two active
changes carrying a `## MODIFIED` block over one promoted requirement is the
two-writers shape THIS VERY REQUIREMENT reports — *"EXACTLY ONE of two active
RATIFIED writers SHALL declare"* — and that `release-realization` requires a
declaration for. Splitting #856 and #860 would manufacture that collision over a
sentence neither could state alone: each block would have to restate the other's
new ground or be measured against canon that lacks it, and whichever landed
second would be stale on arrival.

**THEY REMAIN SEVERABLE WHERE IT MATTERS**, which is at ratification: D1 and D2
are separate rulings, either can be vetoed alone, and the delta's two grounds,
two scenarios, two branches and two test groups are disjoint. What is NOT
severable is the sentence they both replace, and that is why they share a packet.

## D8 — why the realization rides the same pull request

`code_surface` is non-empty, so under `release-realization` this packet archives
on merged-plus-green realization evidence rather than on landing, and the tasks
are individually executable — so it realizes through its own task list rather
than through a feature DAG. That is the shape `amend-published-tip-unreadable-scenario`
(#685), `amend-unreadable-read-sibling-scenarios` (#688),
`amend-marker-reason-boundary` (#719) and `amend-marker-defect-reporting` (#850)
all took over this same capability, and it is the only shape under which the
population claim can be MEASURED rather than promised: canon and checker land in
one commit, and the doc-health run in the pull request is the evidence.

## D9 — what is NOT taken here

- **The promoted markers are not edited**, nor the archived deltas that carry
  them. They are records of ratified removals, and every one of them is correct
  under both new grounds.
- **`document-lifecycle` is not amended.** Its marker grammar says how a unit is
  named and carries no reporting rule, checked on this tree — and amending it is
  exactly D1's rejected alternative.
- **No parse moves.** `parse_marker`, `Marker` and the reason boundary are
  untouched; both grounds read fields the parser already derives.
- **No severity moves and no class is added.** Five grounds, one class, one
  action, one template, `_ARM_TEMPLATES` at eight.
- **The action string is not re-worded.** It already names the remedy for all
  five grounds, and a per-ground action would break the class's own pin
  (`test_every_finding_carries_its_class_s_band_and_action`) for no reader's
  benefit.
- **The uncited-resolution rule is not widened to finding-class grain.** That is
  openxFactory #893, filed by the packet that found it.
