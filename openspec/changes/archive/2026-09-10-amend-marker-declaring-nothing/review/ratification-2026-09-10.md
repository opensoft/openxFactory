# Proposal Ratification: amend-marker-declaring-nothing

Status: ratified
Kind: report
Decision date: 2026-09-10
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-10 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), verbatim: *"ratify as encoded"*,
given in session and recorded on openxFactory PR
[#908](https://github.com/opensoft/openxFactory/pull/908#issuecomment-5623230781)
at **2026-09-10T18:06:52Z** (comment `5623230781`). **THE WORD IS A
MULTIPLE-CHOICE RULING**, given over a presentation that carried BOTH of this
packet's declared veto points — `design.md` **D1** (openxFactory #860) and
**D2** (openxFactory #856) — each with the recommendation stated FIRST and the
alternative written out beside it with its cost. **BOTH ARE RESOLVED AS OPTION
A, WHICH IS THE OPTION THE PACKET ALREADY ENCODED IN EACH CASE, SO THE DELTA'S
WORDING STANDS UNCHANGED AND NO SUBSTITUTION WAS PERFORMED.**

**THE WORD WAS GIVEN IN SESSION AND RECORDED AT THE SAME MINUTE, AND BOTH FACTS
ARE STATED RATHER THAN COLLAPSED.** Brett Heap gave the word in session on
2026-09-10 at approximately 18:06Z, and the lane recorded it on the pull request
at 18:06:52Z — the same minute, unlike this packet's predecessor, where the word
and its recording stood about seven hours apart. The recording comment is the
citable artifact; the session utterance is what it records, and this record says
so in as many words rather than presenting the recording timestamp as the moment
of decision. Both instants fall inside the same UTC day, so the
`Decision date:`, `approved_on`, this file's name and its sibling capture's name
are all **2026-09-10**, and there is no boundary to reconcile.

Ratified baseline: this change as committed on the branch
`change/amend-marker-declaring-nothing` at the frozen head **`5dd724f5`** —
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`specs/doc-health/spec.md` (**ONE `## MODIFIED` requirement**, *Currency of an
active change's MODIFIED requirement blocks*, restated over canon byte-faithfully
with **TWO body sentences replaced in place**, **TWO sentences added beside
them** in the same paragraph, **TWO scenarios added** at the end of the block and
**ONE `Removed from canon` marker** naming exactly the two retired units) and the
realization that rides the same pull request
(`scripts/doc_health/modified_block_currency.py` and
`tests/doc-health/test_modified_block_currency.py`). **THE RATIFIED SURFACE IS
BYTE-IDENTICAL TO THE TREE BRETT HEAP RULED ON**, and that is measured rather
than asserted: `git diff 5dd724f5 -- openspec/changes/amend-marker-declaring-nothing/specs/`
is **EMPTY**, and so is `git diff 5dd724f5 -- scripts/doc_health/ tests/doc-health/`
(§ 6, and `review/verification-2026-09-10.md` § 10, which measure it).

**TWO MERGES FROM `main` PRECEDE THIS ENCODE AND MOVE NONE OF IT.**
`origin/main` advanced from `e0638f11` — the tree every figure in this packet was
measured on — by THREE commits while the branch sat frozen at `5dd724f5`:
`40d2f821` and `bd1c54c6`, merged as `480fb996`, and then `ea34f22a`, merged as
`6aebb296`. Both merges are their own commits and both come BEFORE the
ratification commit. Those three commits touch the carve scripts and their
tests, the cutover runbook, the `lane-line` workflow and three merge-master
scripts with their tests; nothing under `openspec/`, nothing under
`scripts/doc_health/`, nothing under `tests/doc-health/` and not `README.md`.
The gate capture beside this file is therefore already a post-merge run, taken
on a tree carrying `main` @ `ea34f22a`, and no re-measure is owed at landing.

## 1. The two words, and exactly what each decided

### 1.1 The ratifying word — given and recorded 2026-09-10T18:06Z

Brett Heap, 2026-09-10, verbatim:

> ratify as encoded

It is one utterance and it does two things at once. It **ratifies the packet**,
and it **answers both of the packet's own multiple-choice questions** — the
choices `design.md` D1 and D2 put and refused to take on the author's behalf.
Both halves are needed to read the act correctly:

- **The ratification half.** The packet was a DRAFT: `.openspec.yaml` carried
  drafting provenance with no approval pair, every document carried
  `Status: draft`, and `tasks.md` § 1 was entirely open and closed to the
  authoring lane by its own terms. This word is the operator's act that flips
  that, and it is the FIRST word to reach the packet's *content*.
- **The two-decision half.** *"As encoded"* names a SIDE of each choice: the
  recommendation, not the alternative. D1 and D2 each put exactly two options
  with A recommended and encoded, so *"as encoded"* resolves both as A. It is
  therefore a ruling on D1 and D2 and not merely an approval that happens to
  mention the packet's subject.

**The earlier word is the ORIGIN of the authoring and is NOT read as an
approval.** Brett Heap's *"do the 860 856 batch, land each when green"*, also of
2026-09-10, given in session, commissioned a lane to WRITE this remedy against
two named issues. It named a batch and a landing condition, ratified no wording
and took neither design decision, which is why the packet was authored as a
draft with no approval pair. That word stays recorded as the origin in
`proposal.md`'s `Proposed:` line, in `.openspec.yaml`'s `proposed_by`, in
`design.md` § 0 and in `tasks.md` § 1.1 — and its *"land each when green"* half
is the LANDING condition, a separate act belonging to the landing lane under
Rule 6, not to this encode.

### 1.2 What the recording comment adds, and what it does not

The recording comment of 2026-09-10T18:06:52Z states the resolution of every
decision the packet carried, and it is quoted here because it is the artifact
this record cites:

> Brett Heap's word 2026-09-10T18:06Z (multiple choice over PR #908's design.md
> D1/#860 and D2/#856, recommendation presented first), verbatim: **"ratify as
> encoded"** — D1 resolved as A (report a `Removed from canon` marker with no
> code span as marker-defect ground FIVE, `info`); D2 resolved as A (report a
> name matching a unit the block itself adds as ground FOUR, `info`); both are
> the options the packet already encodes, so the delta's wording STANDS
> UNCHANGED and no substitution is performed; D3–D9 carried, none vetoed.

**IT ADDS NO NEW RULE AND CHANGES NO WORDING.** Each clause names a decision the
packet had already encoded and put for veto, and records that it stands. The
comment also names the encode as the next act and the Rule 6 landing as a
separate, later one on the already-recorded word *"land each when green"* —
which is why this record exists and why this lane does not merge.

## 2. D1 as it was put, and D1 as it is resolved

### What was on the table

`design.md` D1 — **THE VETO POINT FOR #860: report it (`doc-health`) against
un-form it (`document-lifecycle`)**:

- **A — REPORT IT, recommended and written into the delta.** A paragraph of
  `Removed from canon` form whose tail carries no code span stays a MARKER and
  is REPORTED, as a fifth ground of the marker-defect class, at the same `info`
  band through the same template. It is the fault the other four grounds already
  exist to report; it leaves the grammar in `document-lifecycle` and the
  reporting rule in `doc-health`, the boundary `amend-marker-defect-reporting`
  § 2.4 checked in both directions and left untouched; it costs one predicate
  over three fields the parser already derives and no parse; and its failure
  direction is a report, never a silence.
- **B — UN-FORM IT, and NOT a straw option**: a GRAMMAR rule in
  `document-lifecycle` that a `Removed from canon` paragraph carrying no code
  span is NOT of marker form at all. Issue #860 itself calls this *"the cheaper
  encoding and the larger semantic change, which is why it needs the ruling
  first"*, and that is exactly right — which is why the decision was put for
  veto rather than simply taken.

**THE COST OF THE ALTERNATIVE, AS D1 WROTE IT OUT.** Under B the paragraph does
not become nothing — it becomes PROSE, and prose in a MODIFIED block is a BODY
UNIT. So it enters the carriage arms in both documents: as a unit of the block it
must be carried, and as a unit of CANON, once such a block promotes, every later
block must restate it forever — precisely what this requirement's *"a marker is
NOT a carriage unit, in either direction"* paragraph exists to prevent. The
author is then handed a carriage-ledger row about the BLOCK's completeness rather
than a row naming the empty declaration and this class's fixed action; the rule
moves to a capability that carries no reporting rule at all, leaving `doc-health`
silent about a defect `document-lifecycle` defines; and it is not reversible by
wording, a ratified grammar rule that such a paragraph is not a marker making it
a UNIT, retirable later only from canon, under a marker, in another
`## MODIFIED` block over the same requirement.

### The resolution

**OPTION A.** *"As encoded"* names the recommended and already-encoded option,
so the ruling is applied **by leaving the text alone**. Ground five stands in
canon and in `suppression`, its added scenario stands, its two tests stand, and
`document-lifecycle` is NOT amended. The withdrawal D1 described — ground five
out of the delta and out of `suppression`, the two `Removed from
canon`-with-no-span tests out, canon re-authored to say FOUR grounds, and the
case filed back as an unruled grammar question needing its own packet, its own
scenarios and a migration story for every paragraph the new grammar reclassifies
— was **NOT** performed.

**Why the alternative's tabulation mattered even though nothing moved.** It is
what made the choice a choice rather than an author's preference, and it is what
would have made a veto applicable faithfully: B is a larger semantic change than
A despite being cheaper to encode, and that asymmetry is not visible from the
diff. A reader who finds only the encoded ground would not know an option was
declined; D1 keeps it on the page.

## 3. D2 as it was put, and D2 as it is resolved

### What was on the table

`design.md` D2 — **THE VETO POINT FOR #856: report it against ruling the silence
correct**:

- **A — REPORT IT, recommended and written into the delta.** A name matching NO
  unit of the requirement's basis and matching a unit THE BLOCK ITSELF ADDS is
  REPORTED, as a fourth ground, at the same `info` band through the same
  template. A block cannot lawfully declare removed from canon a unit canon never
  carried — the marker's own words are *"Removed from canon by"*. It is the OTHER
  HALF of a branch that already reports: `suppression`'s guard is
  `if name not in block_texts: unmatched.append(name)`, ground three reports the
  `if` and ground four the `else`, and the two are disjoint by construction, so a
  marker cannot be double-reported and the two rows are two different edits.
- **B — RULE THE SILENCE CORRECT, and it is the issue's own second option**: say
  so in canon in one sentence — *"a name matching a unit the block ADDS is out of
  scope"* — so the next reader finds a decision rather than a gap.

**THE COST OF THE ALTERNATIVE, AS D2 WROTE IT OUT.** B ratifies a shape with no
honest reading: nobody has offered an account of what a marker naming the block's
own addition MEANS, so B would promote a rule that such a marker is fine while
leaving the question of what it declares permanently unanswered. It is silent in
the direction that hides — the author gets NO row: not for the marker, not for
the addition (an addition is text no arm reads), not for anything. It costs the
SAME amendment, being also a `## MODIFIED` block over the same sentence with its
own ruling and its own scenario, so it buys no work and only a different answer.
And it is the harder rule to retire: a ratified out-of-scope clause is a ratified
permission, withdrawable later only by retiring a unit from canon under a marker,
in a third amendment of this sentence in five days.

### The resolution

**OPTION A.** Ground four stands as encoded, its added scenario stands, and
**the assertion this packet flipped STAYS FLIPPED**. That last point is the whole
point of the decision: `amend-marker-defect-reporting`'s `design.md` D3 PINNED
this silence with `test_a_name_matching_a_unit_the_BLOCK_adds_stays_SILENT` so
that *"the silence is a decision a later act can overturn rather than a gap it
has to rediscover"*, and filed #856 to overturn it. This ruling is the act that
test was written for. The reversal D2 described — ground four withdrawn, the
flipped test flipped back to its ratified silence under its old name, the
two-shapes-in-one-marker half removed, and canon gaining B's one sentence instead
— was **NOT** performed.

### What D1 and D2 did NOT decide

**D0's MEASUREMENT STANDS.** D0 is the corpus reading taken before the design, on
`main` @ `e0638f11`: **26 markers** of any form, **17** of the two unit-naming
forms and **9** of the pairing form; **ZERO** of `Removed from canon` form with
an empty tail and **ZERO** of either unit-naming form with an empty tail;
**THIRTY** active `## MODIFIED` blocks the family reads, of which exactly **TWO**
carry a unit-naming marker (`add-chain-attestation` and
`add-composed-view-authoring`, both `Merged into`, one name each matching its
resolved basis, neither quoting a code span in a reason and neither naming a unit
its own block adds); and **ZERO** marker-defect findings raised by a run, before
this packet and after it. **SO BOTH RATIFIED GROUNDS HAVE A POPULATION OF ZERO:
0 for ground four and 0 for ground five**, measured rather than assumed, which is
what makes them normative for the next marker written rather than a sweep of the
present corpus. Neither silence has yet cost anybody a row.

**D3 THROUGH D9 WERE CARRIED BESIDE D1 AND D2 AND NONE WAS VETOED**, and the
recording says so in as many words. D3 (the band: `info`, the class's existing
one, `warning` refused on this family's own *"MEASURE FIRST, THEN FLIP"* ruling
of 2026-08-27, and the family's `contested` row inherited rather than exempted
from), D4 (ONE template for five grounds, `TEMPLATE_MARKERS`' text unmoved so the
existing `CLASS_MARKERS` probe places every new finding and `_ARM_TEMPLATES`
stays at EIGHT), D5 (the self-reference hazard, and this block's own marker
written to survive its own rules), D6 (the two exclusions ground five is written
around — the PAIRING form, whose silence stays ruled correct, and the
`Merged into` form with an empty tail, left undecided as residue § 7.1), D7 (ONE
packet for two issues, and the mechanical reason), D8 (why the realization rides
the same pull request) and D9 (what is deliberately not taken) each stand as
designed. `tasks.md` § 1.4 records that.

## 4. THE RATIFIED SURFACE

**ONE `## MODIFIED` REQUIREMENT; TWO BODY SENTENCES REPLACED IN PLACE, TWO ADDED
BESIDE THEM, TWO SCENARIOS APPENDED, ONE MARKER.** The requirement is *Currency
of an active change's MODIFIED requirement blocks* of `doc-health`, and the block
is byte-faithful to canon by CONSTRUCTION — generated by slicing
`openspec/specs/doc-health/spec.md` lines 1588–1985 and 2018–2113 and applying
each replacement as an exact single-occurrence substitution (the build script
refuses on any other count), then re-wrapping ONLY the one paragraph the
substitutions touched, which canon itself makes unit-identical.

| unit | canon (retired) | ratified (replaced in place) |
| --- | --- | --- |
| 1 | the sentence stating **THREE** grounds and enumerating them | the same SHALL over **FIVE** grounds — the three that stand, unchanged and in the same order and words, plus ground FOUR (it names something matching no unit of the basis and a unit THE BLOCK ITSELF STATES) and ground FIVE (it is of `Removed from canon` form and its tail carries NO code span at all) |
| 2 | the sentence COUNTING them (*"Each of the three is a declaration that does not describe the block …"*) | the same sentence over five |

**AND TWO SENTENCES ARE ADDED BESIDE THEM IN THE SAME PARAGRAPH**, one scoping
each new ground. Ground four *"changes no suppression"* — a name matching no unit
of the basis never suppressed anything and still suppresses nothing, and the
block's own addition is not reported for being named. Ground five is read on the
`Removed from canon` form ALONE: the PAIRING form names no units by construction,
its whole tail being a reason, so a pairing marker carrying no code span declares
exactly what that form declares and is NOT reported — a silence
`amend-marker-defect-reporting` already ruled correct — and a `Merged into`
marker whose tail names no superseded title is a question this requirement does
not decide, its destination standing in the prefix where that form's declaration
has always been read.

**TWO SCENARIOS ARE ADDED AT THE END OF THE BLOCK**, *A marker names a unit the
block itself adds* and *A marker of removal form declares nothing at all*, the
second carrying the pairing-form exclusion in its own bullet. Without them the
two new grounds would promote with nothing exercising them and would be pinned
only by this packet's tests — running code standing in for canon, the exact shape
`proposal.md` § *Why this is NOT a plain fix* refuses. No promoted scenario moves,
is retitled or loses a bullet.

**ONE `Removed from canon by amend-marker-declaring-nothing (2026-09-10):`
MARKER** names the two retired units as CommonMark code spans and carries **no
code span at all in its reason**, so under the grammar this very requirement
defines it names exactly two units and reports on none of the five grounds — the
first name contains a backtick (`` `info` ``) and is fenced with a longer run
exactly as canon's own rule requires. The marker is assembled from `derive_units`'
own output rather than retyped, then re-parsed by `parse_marker` and asserted to
yield exactly those two names and an empty `quoted`.
`amend-modified-block-currency-standing`'s promoted marker is **deliberately NOT
restated**, on this requirement's own rule that a marker is not a carriage unit
in either direction, because restating it would make this block report ITSELF
under ground three; the block's `AMENDED BY` note says so in terms.

**AND THE REALIZATION IS RATIFIED WITH THE DELTA, IN THE SAME PULL REQUEST.**
`code_surface` is non-empty, so `scripts/doc_health/modified_block_currency.py`
and `tests/doc-health/test_modified_block_currency.py` ride here: ground four is
the `else` half of a guard that already reports, ground five is one predicate
over three fields the parser already derives, `TEMPLATE_MARKERS`' text is not
edited at all, `_ARM_TEMPLATES` stays at EIGHT, `_MARKER_ACTION` and
`_LEDGER_SEVERITY` (`info`) are unchanged, and no parse moves and no `Marker`
field is added. Tests **139 → 144** with ONE assertion FLIPPED (fixture
unchanged) and ONE test RENAMED and not otherwise edited.

## 5. The bench: five rounds before the word, one after it

### 5.1 The rounds, each named by the commit GitHub records the review against

| bench | commit the review is recorded against | verdict |
| --- | --- | --- |
| Codex, one request | `8d1bdce2`, the head when the request was posted (2026-09-10T17:45:40Z) | **ABSENCE** — a usage-limit notice at 17:45:50Z, no review (§ 5.4) |
| Copilot round 1 | `880df9a6` (2026-09-10T17:47:19Z) | 🟡 **Changes recommended** — one inline comment (**T1**) plus one suppressed comment |
| Copilot round 2 | `8d1bdce2` (2026-09-10T17:51:47Z) | 🟢 **Approval recommended** — *"The implementation and tests appear coherent and well-scoped"*; **0 new comments**, two suppressed |
| Copilot round 3 | `f59a462b` (2026-09-10T17:58:38Z) | 🟡 **Changes recommended** — one inline comment (**T2**) |
| Copilot round 4 | `bd5e5565` (2026-09-10T18:03:41Z) | 🔵 **Needs a closer look** — **0 new comments** |
| Copilot round 5 | `5dd724f5`, the FROZEN BENCH HEAD (2026-09-10T18:07:45Z) | 🔵 **Needs a closer look** — **0 new comments** (quoted verbatim at § 5.4); this is the last verdict standing when the word was given |
| Copilot round 6 | `480fb996`, the first merge from `main` (2026-09-10T18:29:30Z) | 🟡 **Changes recommended** — one inline comment (**T3**), AFTER the word, taken in this ratification commit |
| Sourcery | a Reviewer's Guide summary, not a finding set (§ 5.5) | |
| SonarCloud | Quality Gate **PASSED**; 8 new issues, all refused with a measurement (§ 5.6) | |

**THIS TABLE CORRECTS THE FREEZE COMMENT OF 18:11:11Z RATHER THAN REPEATING
IT.** That comment counted FOUR Copilot passes and named each by the commit that
FIXED it; the rounds are named here by the commit GitHub's own review record
carries, and the 18:07:45Z pass on the frozen head — which the freeze comment
omitted, having been written four minutes later — is included. The verdicts and
the two findings are unchanged by the correction: round 5's verdict is the same
🔵 **Needs a closer look** with 0 new comments as round 4's, so the freeze's
conclusion about the standing of the frozen head holds as stated.

### 5.2 The two threads on the pull request, and their disposition

**THREE THREADS, ALL THREE TAKEN.** Two were resolved at the freeze of
2026-09-10T18:11:11Z, both auto-resolved as OUTDATED when the fix moved the lines
they pointed at; the third arrived AFTER the word, on the merge head `480fb996`,
and is **TAKEN IN THIS RATIFICATION COMMIT** and resolved with a reply naming
it. All three are Copilot inline threads and all three were TAKEN on their merits
rather than aged out — the fix commits are named below.

| # | bench | site | finding | disposition |
| --- | --- | --- | --- | --- |
| T1 | Copilot, 17:47:19Z ([`r3981930694`](https://github.com/opensoft/openxFactory/pull/908#discussion_r3981930694)) | `scripts/doc_health/modified_block_currency.py` | *"In `suppression()`'s docstring the numbering is inconsistent ("AND A FIFTH" followed shortly by "AND A FOURTH RESOLUTION"). This makes it hard to map the prose back to the five marker-defect grounds and risks misleading future edits."* | **TAKEN in `f59a462b`** — real, and this packet created it: the docstring's ordinals count RESOLUTIONS while the amended sentence counts GROUNDS, and adding grounds four and five made the two collide on the page. Fixed by ORDER PLUS A MAPPING rather than a renumbering — the ground-five paragraph moves below the fourth resolution, both are labelled with the ground they carry, and the mapping is written out (three-way resolution carries grounds ONE, THREE and FOUR; the fourth carries ground TWO; the fifth carries ground FIVE). **No code moved.** `tasks.md` § 3.8 records it |
| T2 | Copilot, 17:58:38Z ([`r3982020462`](https://github.com/opensoft/openxFactory/pull/908#discussion_r3982020462)) | `tests/doc-health/test_modified_block_currency.py` | *"`test_no_marker_in_this_corpus_raises_either_ground_ADDED_HERE_today` is meant to be a ceiling for the two new grounds, but the ground-four half currently asserts `name not in texts` (block units) for every marker name. That predicate would also fail on an unrelated future regression of ground one … making the failure look like a ground-four regression even when it isn't."* | **TAKEN in `5dd724f5`**, and it was right about MISATTRIBUTION rather than about a false green: `name in block_texts` is the precondition of ground ONE as much as of ground four. The test now resolves each active block to its promoted basis exactly as the runner does and asserts on `suppression`'s OWN OUTPUT — narrower AND stronger: it cannot misattribute, and it measures the exact population instead of a bound on it. A floor (`compared >= 10`) keeps it from passing by resolving nothing; 25 of 31 active blocks resolve, 3 of those carry a unit-naming marker. `tasks.md` § 2.3 and § 3.6 record it |
| T3 | Copilot, 18:29:30Z ([`r3982265135`](https://github.com/opensoft/openxFactory/pull/908#discussion_r3982265135)) | `README.md`:545 | *"This sentence reads like the defect still exists on this branch, but this PR changes `modified_block_currency.py` to report both cases. Consider switching to past tense / scoping it to `main` so the record entry doesn't contradict the implementation in this PR."* | **TAKEN IN THE RATIFICATION COMMIT** — right, and the sentence it points at (*"THE DEFECT IS TWO MARKERS THAT DECLARE NOTHING AND ARE REPORTED AS NOTHING"*) was written of `main` @ `e0638f11` while standing in a row that describes this branch, which realizes both grounds. The row's defect paragraph is now PAST TENSE and named to that tree, its two per-issue sentences with it; the promoted-canon sentence says STILL and names the archive as where the block writes over it; and *"canon now states FIVE grounds"* becomes *"the block states FIVE grounds"*. **The delta, the realization and every record are untouched by the fix** — it moves README prose only. `tasks.md` § 4.7 records it |

### 5.3 Nothing was refused on the merits, and nothing is owed from the bench

All three findings were taken. No bench finding was declined, so this
ratification carries no bench residue — unlike its predecessor, which refused one widening and
owed it as an open box. The residue this packet DOES carry (`tasks.md` § 7) is
MEASURED design residue and not bench feedback: § 7.1 the `Merged into` empty
tail, § 7.2 the estate-wide run, § 7.3 `specs/019`, § 7.4 the per-class grain of
the uncited-resolution rule.

### 5.4 Copilot's standing verdict, and Codex's ABSENCE — both recorded verbatim

**Copilot's review ON THE FROZEN HEAD `5dd724f5`** — round 5,
2026-09-10T18:07:45Z, **0 new comments**, the verdict standing when the word was
given — verbatim:

> ### 🔵 Needs a closer look
>
> It combines normative spec amendment text with behavioral changes to a core
> doc-health checker path, which warrants final human review for
> semantic/contract correctness beyond what automated analysis can safely
> approve.

Round 4, on `bd5e5565` at 18:03:41Z, also read 🔵 **Needs a closer look** with 0
new comments and put the same point in different words (*"It changes normative
spec wording and core doc-health reporting logic in a highly coupled area, so it
should receive final human validation despite passing tests."*). Round 6, on the
merge head after the word, returned to 🟡 **Changes recommended** for the README
tense finding **T3** alone (§ 5.2) and raised nothing against the delta, the
realization or either record.

**That is the standing of a packet awaiting a ratification word, and it is what
the word of 2026-09-10 supplies.** The verdict asks for final human validation of
normative wording; the operator's ruling on D1 and D2 is that validation.

**CODEX DID NOT REVIEW THIS PULL REQUEST AT ALL, AND THE SILENCE IS AN ABSENCE
RATHER THAN AN APPROVAL.** One review request was posted at
2026-09-10T17:45:40Z. The reply came at 17:45:50Z, verbatim:

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the Codex usage dashboard. To continue using code reviews, you can
> upgrade your account or add credits to your account and enable them for code
> reviews in your settings.

**No Codex review exists on this pull request and none was waited out.** This
record states that rather than presenting silence as assent.

### 5.5 Sourcery's linked-issue reading is REFUSED

Sourcery produced a Reviewer's Guide and **no findings**. Its *"Possibly linked
issues"* section reads this pull request as *"directly resolves"* #856 and #860.
**That reading is REFUSED and the mechanism disagrees with it:** there is no
closing keyword anywhere in the body or in any commit, and
`closingIssuesReferences` is `[]`, verified through GraphQL. Both issues close at
the ARCHIVE (§ 7).

### 5.6 SonarCloud: gate PASSED, eight issues REFUSED with a measurement

The Quality Gate **passed**. Eight new issues were raised, all
`python:S9073` — *"Split this composite assertion into separate assertions"* — on
`tests/doc-health/test_modified_block_currency.py`, every one of the form
`assert m is not None and m.form == "removed"` or
`assert m.names == [] and m.quoted == []`. **REFUSED because it is the file's
standing style and splitting only the new ones would diverge from it**: the file
carries 33 composite assertions and **24 of them are on `origin/main`**,
including the two in the very test the new ones are modelled on. Counted rather
than asserted, with `grep -cE '^\s*assert .+ and '` over both trees. No issue is
a correctness finding.

## 6. What is NOT ratified, and what this word does not reach

- **NOTHING IS PROMOTED.** This ratification edits no file under
  `openspec/specs/`, no contract, no schema and no workflow —
  `git diff 5dd724f5 -- openspec/specs/` is EMPTY. The `## MODIFIED` block is a
  DELTA; canon still states THREE grounds until the archive writes the block
  over it.
- **NO SEVERITY MOVES, NO CLASS IS ADDED AND NO ROW IS ADDED.** Both new
  findings carry the marker-defect class's existing `info` band and its existing
  action; `TEMPLATE_MARKERS`' text is not edited at all; `_ARM_TEMPLATES` stays
  at EIGHT; and the family's `contested` resolution row is inherited rather than
  claimed an exemption from.
- **NO PARSE MOVES.** `parse_marker`, `Marker` and the reason boundary are
  untouched, and no marker in the estate parses differently after this packet
  than before it.
- **THE PAIRING FORM IS NOT REACHED.** Its silence stays ruled correct by
  `amend-marker-defect-reporting`, and ground five is scoped away from it in
  canon, in the code and in a test.
- **THE `Merged into` FORM WITH AN EMPTY TAIL IS NOT DECIDED** (`tasks.md`
  § 7.1, open box, successor named at 2026-09-10T18:15Z as openxFactory #914).
- **THE ESTATE-WIDE RUN IS NOT TAKEN HERE** (`tasks.md` § 7.2, open box). This
  packet's measurement covers openxFactory only, this lane being confined to its
  own clone.
- **`specs/019-modified-block-currency-family/` IS NOT EDITED** (`tasks.md`
  § 7.3, open box, successor named as openxFactory #915). Its FR-018 states the
  THREE grounds canon carries today.
- **THE PER-CLASS GRAIN OF THE UNCITED-RESOLUTION RULE IS NOT WIDENED**
  (`tasks.md` § 7.4, open box, openxFactory #893, filed by this packet's
  predecessor).
- **`document-lifecycle` IS NOT AMENDED** — that is D1's declined alternative,
  and the ruling declined it.
- **THE PROMOTED MARKERS THIS PACKET COUNTS ARE NOT EDITED**, nor the archived
  deltas that carry them. An archived delta is a record of what was ratified.
- **`tasks.md` § 6 (ARCHIVE) AND § 7 (RESIDUE) STAY ENTIRELY OPEN.**

## 7. What is owed at the archive, and why it is not owed here

**THE ARCHIVE IS A SEPARATE ACT ON MERGED-PLUS-GREEN REALIZATION EVIDENCE AND A
SEPARATE WORD.** `code_surface` is non-empty, so under `release-realization` this
packet does NOT archive on landing: the evidence is this pull request merged into
`main` plus a green `pytest-suite` run on that merge commit. At that act:

- `python3 scripts/proposal-support.py . archive amend-marker-declaring-nothing
  --date <YYYY-MM-DD> --yes` through the pinned CLI moves the packet under
  `openspec/changes/archive/` and writes the `## MODIFIED` block back into
  `openspec/specs/doc-health/spec.md` (`tasks.md` § 6.1).
- **openxFactory #856 AND #860 CLOSE THERE, NOT AT THIS LANDING** (`tasks.md`
  § 6.2), which is why this pull request carries `refs #856, refs #860` and no
  closing keyword and why its `closingIssuesReferences` is verified `[]`.
- The § 7 residue boxes tick ON THE RECORDING, by NAMING their successors:
  § 7.1 → openxFactory #914 and § 7.3 → openxFactory #915, both named on the
  pull request at 2026-09-10T18:15:34Z ahead of the archive act; § 7.4 already
  names #893; § 7.2's estate-wide run is being MEASURED against this head's code
  over the governed repositories at live `main`, and its recording lands on the
  pull request as its own comment. **NO § 7 BOX IS TICKED BY THIS ENCODE** —
  naming a successor is what ticks one, and that tick belongs to the archive act
  that reads the recording.

**AND THE LANDING IS NOT THIS LANE'S ACT EITHER.** The Rule 6 LANDING/LANDED
post belongs to the landing lane on the already-recorded word *"land each when
green"*, which the recording comment names as a later act in as many words. This
lane encodes and freezes; it does not merge.
