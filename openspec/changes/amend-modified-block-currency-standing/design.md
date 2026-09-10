# Design: amend-modified-block-currency-standing

Status: draft
Date: 2026-09-10
Kind: design

## 0. The brief

Two owed residues of one flip, filed by the lane that archived
`amend-marker-defect-reporting` and named in that packet's ratified `tasks.md`:

- openxFactory [#857](https://github.com/opensoft/openxFactory/issues/857)
  (§ 5.3) — promoted `doc-health` canon still calls this family advisory and
  unclassified.
- openxFactory [#858](https://github.com/opensoft/openxFactory/issues/858)
  (§ 5.4) — `specs/019` FR-018 still states the ONE-ground marker rule.

Brett Heap's word of 2026-09-10, verbatim **"do 1, then 2"**, commissions the
authoring of both as one packet. It ratifies nothing. This document records what
was measured, what is proposed, and — for the two decisions where a reasonable
owner could rule the other way — what the alternative costs.

## D0 — the measurement, taken before the design, and the correction it forces

**SIX SEVERITY CONSTANTS AND ONE RESOLUTION ROW, READ OUT OF THE MODULE AT
`main`** (`scripts/doc_health/modified_block_currency.py`,
`scripts/doc_health/families.py`, 2026-09-10):

| constant / row | value | line | moved by the flip? |
| --- | --- | --- | --- |
| `_LAUNCH_SEVERITY` — scenario-title completeness | `ERROR` | `:229` | **YES**, `WARNING` → `ERROR` |
| `_RESOLUTION_SEVERITY` — title resolution and ordering | `WARNING` | `:230` | no |
| `_LEDGER_SEVERITY` — carriage ledger, and marker defects | `INFO` | `:231` | no |
| `_DRIFT_SEVERITY` — unplaced-finding drift | `WARNING` | `:232` | no |
| `_PAIRING_SEVERITY` | `WARNING` | `:253` | no |
| `_COLLISION_SEVERITY` | `WARNING` | `:254` | no |
| `FAMILY_RESOLUTION["modified-block-currency"]` | `CONTESTED` | `families.py:117` | **YES**, the row was ADDED |

**THIS CORRECTS THE REMEDY ISSUE #857 ITSELF PROPOSES.** #857's "smallest
remedy" asks canon to state *"`error` for the scenario-completeness and
title-resolution arms and `info` for the carriage ledger"*. **The
title-resolution arm is `warning`.** It was deliberately not dragged: the
severities are separate module attributes precisely so the flip could move one
arm, orchestrator decision O8
(`specs/019-modified-block-currency-family/plan.md`) reserved them that way —
*"so § 7.2's flip moves the scenario-title arm alone. A veto (one constant)
drags the title-resolution arm to `error` on a flip nobody asked for"* — and PR
#529's own body records that `_RESOLUTION_SEVERITY`, `_LEDGER_SEVERITY` and
`_DRIFT_SEVERITY` were left unchanged for that reason. Encoding the issue's
wording would have replaced one false sentence with another. **The delta states
the arm-by-arm truth**, and names the two classes that did not exist when the
paragraph was written (drift, pairing, collision) by the rule that each keeps
the band its own requirement states rather than by re-enumerating them here — a
list of six in this paragraph would go stale on the seventh class.

**THE RESOLUTION ROW HAS NO PER-CLASS GRAIN, AND THAT IS LOAD-BEARING.**
`runner.main` applies it as `FAMILY_RESOLUTION.get(f.family, f.resolution)`,
keyed on `Finding.family` alone, and every arm of the module shares one `FAMILY`
string. PR #529 flagged this explicitly when it added the row, and the promoted
*A modified-block-currency finding its own class map cannot place is itself a
finding* states it as canon at `:2300-2303`. So the classification reaches the
`info` carriage ledger as surely as the `error` scenario arm — which is why D4
adds a scenario for it.

## D1 — THE VETO POINT: four sites, or the one paragraph #857 quotes

**RECOMMENDED AND ENCODED: all four.** The flip is misstated in FOUR places
inside ONE requirement, and the packet corrects all of them:

| # | site | the false claim | in the delta |
| --- | --- | --- | --- |
| 1 | `:1615` | "the arms below are advisory" | retired, sentence restated |
| 2 | `:1816-1823` | `warning` severities; "deliberately absent from `FAMILY_RESOLUTION`" | retired, two paragraphs replace it |
| 3 | `:1824-1826` | the raising and the classification "are ONE later decision" | retired, the history paragraph records the decision as taken |
| 4 | `:1922-1923` | the scenario's `warning` finding, and "MUST NOT cause a run configured `--fail-on error` ... to fail" | two bullets replaced, one added |

**THE ALTERNATIVE, WRITTEN OUT WITH ITS COST.** Take site 2 alone — the
paragraph #857 quotes — and leave 1, 3 and 4. The packet would then be three
retired units smaller and would carry no added scenario. What it would produce
is a requirement whose body says the scenario-title arm carries `error` and
whose first scenario says the run "MUST emit a `warning` finding" that "MUST NOT
cause a run configured `--fail-on error` ... to fail" — **a promoted requirement
contradicting itself about a gate**, in the specification of the family whose
whole job is to report blocks that do not match canon. And it would owe a third
successor issue for the same flip, four days after the second one was filed.

**A VETO IS CHEAP AND IS SCOPED.** Dropping sites 1, 3 and 4 removes three names
from the marker, restores three canon units verbatim, and deletes the added
scenario; site 2's replacement paragraphs stand unchanged either way.

## D2 — the replacement wording is COPIED, not invented

Two promoted families have made this exact move before —
`promotion-fidelity` and `duplicate-packet`, both flipped from advisory to
enforcing-and-contested — and canon carries their post-flip wording at
`openspec/specs/doc-health/spec.md:1080-1100` and `:1233-1254`:

> **This family SHALL be enforcing, in both halves of what that means.** Every
> finding it emits SHALL carry `error` severity ... and the family SHALL be
> classified `contested` ... The two SHALL move together and MUST NOT be taken
> apart ...
>
> The family SHIPPED ADVISORY and was flipped by ruling, which is the sequence
> this requirement records rather than a history it has replaced. ...

The delta follows that shape sentence for sentence, with ONE structural
difference forced by the facts: those two families are uniformly `error`, and
this one is **enforcing in one arm and advisory in the rest**, so the first
paragraph is arm-by-arm where theirs is whole-family. Copying a promoted
formulation is deliberate — a third wording for the same idea would be a third
thing for a later reader to reconcile.

**AND THE HISTORY IS KEPT AS HISTORY.** The launch state is not deleted from
canon; it is moved into the sequence paragraph, exactly as the two precedents
did. The `SHALL` about HOW such a flip is taken — one decision by ruling, after
the population is discharged, never as a judgement call inside an
implementation — is kept in force for any future flip of the remaining arms.

## D3 — the paragraph's third sentence is CARRIED, not retired

*"**No flip is proposed for the carriage ledger in this change**, whose
population is standing by construction — every legitimate MODIFIED block edits
something — so an editorial band is the honest launch state; a later flip
remains available and is a ruling like any other."*

**It is TRUE and it is carried unchanged.** No flip has been ruled for the
ledger, its constant reads `INFO`, and the sentence's "this change" names
`add-modified-block-currency-check`, which promoted this requirement. Retiring a
true unit is a change truth does not require, and the family's own doctrine is
that a MODIFIED block replaces what is false and carries the rest.

**THE ONE RISK IS THE DEICTIC**, and the block answers it in the open: a reader
could take "this change" for the amending change. The `AMENDED BY` note says
which change it names, in the same breath as the rest of its accounting, rather
than editing a true sentence to remove an ambiguity that predates this packet.

## D4 — ONE scenario added, at the END of the block

> #### Scenario: This family stops reporting a path without a citation

The `contested` row reaches every class the family emits, the `info` carriage
ledger included, and **no scenario exercised that**. The added scenario states
the consequence (an uncited disappearance is the uncited-resolution `error`) and
the thing most easily misread beside it — that the resolution class does NOT
move the finding's own severity, the two being separate fields. A normative rule
no scenario exercises is a rule the next author re-deriving this family has
nothing to test against.

**IT IS STATED AT THE GRAIN THE RULE ACTUALLY KEYS ON, WHICH IS NOT THE CLASS**
(bench round 1, PR #887 thread T2). `report.uncited_resolutions` iterates the
previous report's contested keys and skips any key a current finding still
carries; the key is `Finding.match_key()` — `(family, repository, path)`,
`scripts/doc_health/__init__.py:187` — so a finding of ONE class ceasing while
another finding of this family is still emitted at that path raises NOTHING. An
earlier draft of this scenario promised the error for any class's disappearance
and would have put a promise in canon that the checker does not keep. Both the
scenario and the standing paragraph now say what the machinery does, and they say
it in the words promoted canon already uses for this family's key — *A
modified-block-currency finding its own class map cannot place is itself a
finding* at `openspec/specs/doc-health/spec.md:2334-2341` and its scenario at
`:2379`. **WHETHER THE CHECKER SHOULD TRACK DISAPPEARANCE PER CLASS IS A CODE
DECISION AND IS REFUSED HERE**, named as residue at `tasks.md` § 5.3: it would
move `match_key`, the ranked-plan grammar `parse_previous` reads, and every
family keyed on it, and this packet's charter is canon truthfulness about
shipped behaviour.

**ADDING A SCENARIO DOES NOT WEAKEN THE MARKER.** The rule that a `Removed from
canon` marker stops carrying a removed TITLE's bullets when the block adds a new
title is scoped to that title-extension; units NAMED INDIVIDUALLY are suppressed
either way, which the requirement states (*"unless it is itself named in a
`Removed from canon` marker as a bullet"*) and `suppression()` implements. The
two retired bullets are named individually.

## D5 — the marker: five names, one paragraph, no code span in the reason

One `**Removed from canon by amend-modified-block-currency-standing
(2026-09-10):**` marker names all five retired units as code spans, each fenced
with a doubled backtick run because every one of them contains a backtick.

**THE REASON CARRIES NO CODE SPAN AT ALL, DELIBERATELY.** Since
`amend-marker-defect-reporting` a code span standing inside a reason is reported
where it exactly matches a promoted unit the block does not carry and no marker
declares removed. A reason with no code span cannot trip that ground under any
reading, and it is the form `amend-marker-defect-reporting`'s own marker chose
for the same reason. `FAMILY_RESOLUTION`, `_LAUNCH_SEVERITY` and the rest are
therefore written as bare words in the reason.

**AND THE PREDECESSOR'S MARKER IS NOT RESTATED.** `amend-marker-defect-reporting`'s
`Removed from canon` marker is promoted into canon at `:1918`. A marker is not a
carriage unit in either direction, so dropping it costs nothing; restating it
would declare a removal this change did not perform, and the unit it names — a
sentence canon no longer carries — matches no unit of the requirement and none of
this block, which is the THIRD ground reporting this block for copying a
predecessor's declaration forward. The predecessor recorded the identical
reasoning about ITS predecessor's marker, and this block follows it.

## D6 — #858 rides this pull request as a SEVERABLE commit

**THE SUBSTANCE FOLLOWS PR #827 EXACTLY; ONLY THE VEHICLE DIFFERS, AND THAT IS
STATED RATHER THAN ELIDED.**

`specs/019-modified-block-currency-family/` is a Speckit feature record — a
build record of what `add-modified-block-currency-check` specified and was
implemented against — not promoted canon, pinned by no test and by no gate
(`scripts/doc_health/corpus.py`'s `GOVERNED_ROOTS` never includes `specs/`, so
no doc-health family reads it). The predecessor's identical residue, #730, was
taken at PR #827 as a plain documentation fix: FR-016 restated to canon, canon's
sentence quoted with its line numbers, and a dated note left beside it —
*"(Amended 2026-09-09 to match canon after `amend-marker-reason-boundary`
(#739); this bullet previously stated the retired last-code-span rule.)"* — under
the explicit heading **"No OpenSpec change — a build record catching up with
promoted canon"**. FR-018 gets the same treatment, in the same file, in the same
form, citing `amend-marker-defect-reporting` (#850).

**WHY IT IS IN THIS PULL REQUEST AND NOT A SECOND ONE.** One lane claimed #857
and #858 as one act on one word, and a second pull request for a twelve-line
documentation edit would buy a second review, a second landing window and a
second record for work already claimed here.

**AND WHY THAT COSTS NOTHING IF THE PACKET STALLS.** The FR-018 commit depends
on no part of this delta. It catches up with canon PROMOTED AT `250d93d7` on
2026-09-09 — it would be correct even if this packet were vetoed outright — so
it is a self-contained commit that can be cherry-picked and landed alone. It is
recorded as taken in `tasks.md` § 3, not as a realization of the delta, because
there is nothing in the delta for it to realize.

**IT IS NOT A CODE SURFACE.** `code_surface: none` is a claim about scripts,
tests, workflows, contracts, schemas and examples; a Speckit build record is a
document, and the front matter says so.

## D7 — what is MEASURED and deliberately NOT taken here

- **`specs/019` FR-024 and FR-026** state the LAUNCH severities and the family's
  absence from `FAMILY_RESOLUTION`. They are NOT edited. Unlike FR-018 they
  FORESEE the flip in their own words — FR-024 asks for the arm's severity to be
  a distinct constant *"so that the later flip ... is one line beside one row"*,
  and the feature's out-of-scope list at `:679` names *"any flip of severity or
  `FAMILY_RESOLUTION` membership (packet § 7.2 — a later ruling)"* — so they read
  as a record of what was built rather than as a statement of current behaviour.
  Whether a build record should nonetheless be annotated where the world moved
  past it is a judgement for the owner of that record, and it is residue of the
  FLIP (#357), not of either issue this packet takes.
- **The archived deltas that carried the false paragraph byte-faithfully** are
  not edited. An archived delta is a record of what was ratified.
- **The promoted requirements that already state the post-flip truth** — *A
  modified-block-currency finding its own class map cannot place is itself a
  finding*, and the pairing and collision requirements, which say the class is
  `contested` "by the family's standing `FAMILY_RESOLUTION` row" — are not
  touched and are not restated. They are the reason this packet is a catch-up
  rather than a decision.
- **No flip of any remaining arm is proposed.** The title-resolution, drift,
  pairing and collision classes keep `warning` and the ledger keeps `info`. A
  later flip of any of them remains one ruling, after a measurement, exactly as
  the delta's sequence paragraph keeps in force.
- **The severity-to-band rendering, the class map, the finding set and the
  ranked plan** are untouched: nothing this packet writes changes what any run
  EMITS. **The one thing promotion does move is the report's HEADLINE**, and it
  is arithmetic rather than rule: `runner.main` sums the words of every promoted
  specification into `spec_words` (`scripts/doc_health/runner.py:807-810`) and
  `report.render` folds that into the canon-share line (`report.py:474,
  496-498`), so replacing a 5,348-word requirement with a 6,564-word one moves
  `openspec/specs/doc-health/spec.md` by +1,216 words (44,684 → 45,900) at the
  ARCHIVE act. Every promotion of prose does this; `proposal.md` § Impact states
  it rather than claiming a report-wide invariance the machinery does not give
  (bench round 2, PR #887 thread T5).
