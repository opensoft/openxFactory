# Proposal Ratification: amend-modified-block-currency-standing

Status: ratified
Kind: report
Decision date: 2026-09-10
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-10 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), verbatim: *"Ratify as encoded, all
four sites"*, given in session at approximately **04:5xZ** and recorded on
openxFactory PR [#887](https://github.com/opensoft/openxFactory/pull/887) at
**2026-09-10T11:35:59Z** (comment `5618026792`), with the same recording carried
to issues [#857](https://github.com/opensoft/openxFactory/issues/857) and
[#858](https://github.com/opensoft/openxFactory/issues/858). **THE WORD IS A
MULTIPLE-CHOICE RULING**, given over a presentation that carried `design.md`
**D1** as the packet's declared veto point — **ALL FOUR SITES** of the
2026-08-31 flip inside the one requirement (recommended and encoded) against
**THE ONE PARAGRAPH ISSUE #857 QUOTES** — with the alternative written out
beside the recommendation and the full cost of taking it tabulated site by site.
**D1 IS RESOLVED AS ALL FOUR SITES, WHICH IS THE OPTION THE PACKET ALREADY
ENCODED, SO THE DELTA'S WORDING STANDS UNCHANGED AND NOTHING WAS RESTORED.**

**THE WORD AND ITS RECORDING ARE SEPARATED BY ABOUT SEVEN HOURS, AND BOTH TIMES
ARE STATED RATHER THAN COLLAPSED.** Brett Heap gave the word in session at
approximately 2026-09-10T04:5xZ, shortly after this lane's freeze comment of
2026-09-10T04:45:26Z put the question in `design.md`'s terms. It was recorded on
the pull request at 2026-09-10T11:35:59Z, by which time the session that heard
it had ended. Nothing turns on the gap: both instants fall inside the same UTC
day, so the `Decision date:`, `approved_on`, this file's name and its sibling
capture's name are all **2026-09-10**, and there is no boundary to reconcile.
The recording comment is the citable artifact; the session utterance is what it
records, and this record says so in as many words rather than presenting the
recording timestamp as the moment of decision.

Ratified baseline: this change as committed on the branch
`change/amend-modified-block-currency-standing` at the frozen head **`ab8247fa`**
— `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE `## MODIFIED` requirement**, *Currency of an
active change's MODIFIED requirement blocks*, restated over canon
byte-faithfully with **FIVE units replaced in place at FOUR sites** under **ONE
`Removed from canon` marker** and **ONE scenario added** at the end of the
block). The delta's normative units are **byte-identical** to the tree Brett
Heap ruled on: `git diff ab8247fa -- openspec/changes/amend-modified-block-currency-standing/specs/`
is **EMPTY**, and this ratification adds no line to it (§ 3, and
`review/verification-2026-09-10.md` § 9, which measures it rather than asserting
it).

## 1. The two words, and exactly what each decided

### 1.1 The ratifying word — given ~2026-09-10T04:5xZ, recorded 11:35:59Z

Brett Heap, 2026-09-10, verbatim:

> Ratify as encoded, all four sites

It is one utterance and it does two things at once. It **ratifies the packet**,
and it **answers the packet's own multiple-choice question** — the choice
`design.md` D1 put and refused to take on his behalf. Both halves are needed to
read the act correctly:

- **The ratification half.** The packet was a DRAFT: `.openspec.yaml` carried
  drafting provenance with no approval pair, every document carried
  `Status: draft`, and `tasks.md` § 1 was entirely open and closed to the
  authoring lane by its own terms. This word is the operator's act that flips
  that, and it is the FIRST word to reach the packet's *content*.
- **The D1 half.** The word names a SCOPE — *all four sites* — and that scope is
  one of exactly two options D1 put. It is therefore a ruling on D1 and not
  merely an approval that happens to mention the packet's subject. The words
  *"as encoded"* say the same thing a second way: the recommendation, not the
  alternative.

**The earlier word is the ORIGIN of the authoring and is NOT read as an
approval.** Brett Heap's *"do 1, then 2"*, also of 2026-09-10, given in session
with item 2 naming issues #857 and #858 as one amendment packet, commissioned a
lane to WRITE this remedy. It ratified no wording and took no design decision,
which is why the packet was authored as a draft with no approval pair. That word
stays recorded as the origin in `proposal.md`'s `Proposed:` line, in
`.openspec.yaml`'s `proposed_by`, and in `tasks.md` § 1.1.

### 1.2 What the recording comment adds, and what it does not

The recording comment of 2026-09-10T11:35:59Z states the resolution of every
decision the packet carried, and it is quoted here because it is the artifact
this record cites:

> **"Ratify as encoded, all four sites"** — design.md D1 resolved: correct every
> site of the 2026-08-31 flip inside the one requirement; D0 arm-by-arm truth
> stands; the added scenario at the (family, repository, path) grain stands;
> #858's specs/019 FR-018 rides as the severable commit `2f384fd1`.

**IT ADDS NO NEW RULE AND CHANGES NO WORDING.** Each clause names a decision the
packet had already encoded and put for veto, and records that it stands. The
comment also names the encode as the next act and the Rule 6 landing as a
separate, later one on a separate word — which is why this record exists and why
this lane does not merge.

## 2. D1 as it was put, and D1 as it is resolved

### What was on the table

`design.md` D1 — **THE VETO POINT: four sites, or the one paragraph #857
quotes**:

- **ALL FOUR SITES** — recommended, and written into the delta. The 2026-08-31
  flip (openxFactory issue #357, PR #529, `7f656980`) is misstated in FOUR
  places inside ONE promoted requirement, and the packet corrects all of them:
  the lifecycle-standing clause *"the arms below are advisory"* at `:1615`; the
  *advisory at launch* paragraph's first sentence at `:1816-1823` (`warning`
  severities and *"deliberately absent from `FAMILY_RESOLUTION`"*); that
  paragraph's *"ONE later decision"* sentence at `:1824-1826`; and the first
  scenario's `warning` bullet and its *"MUST NOT cause a run configured
  `--fail-on error` ... to fail"* bullet at `:1922-1923`.
- **THE ONE PARAGRAPH #857 QUOTES** — the alternative, and **not a straw
  option**: it is the remedy the origin issue itself asks for, in as many words,
  and it is the smallest edit that answers the issue as filed. That is why the
  decision was put for veto rather than simply taken.

**THE COST OF THE ALTERNATIVE, AS D1 WROTE IT OUT.** Taking site 2 alone would
have left a promoted requirement whose body says the scenario-title arm carries
`error` and whose first scenario says the run *"MUST emit a `warning` finding"*
that *"MUST NOT cause a run configured `--fail-on error` ... to fail"* — **a
promoted requirement contradicting itself about a gate**, in the specification of
the family whose whole job is to report blocks that do not match canon. And it
would have owed a third successor issue for the same flip, four days after the
second one was filed.

### The resolution

**ALL FOUR SITES.** The scope Brett Heap named is the recommended and
already-encoded option, so the ruling is applied **by leaving the text alone**.
The narrowing D1 described — dropping sites 1, 3 and 4, which would have removed
three names from the marker, restored three canon units verbatim and deleted the
added scenario — was **NOT** performed. The five retired units, the marker's five
names and the one added scenario are ratified **exactly as the bench reviewed
them**, and that is verified by diff rather than asserted:
`git diff ab8247fa -- .../specs/doc-health/spec.md` is **EMPTY**.

**Why the tabulation mattered even though nothing moved.** D1's site-by-site
table was not decoration: it is what made the choice mechanical rather than a
judgment call, and it is the reason a narrow ruling could have been applied
faithfully — restoring only SOME of the units would have left canon
contradicting itself inside one requirement, the exact defect this packet
closes, so a veto applied to a wrong set would have re-created it.

### What D1 did NOT decide

**D0 STANDS, AND THE RECORDING SAYS SO.** D0 is the measurement taken before the
design — six severity constants and one resolution row read out of
`scripts/doc_health/modified_block_currency.py` and `scripts/doc_health/families.py`
— and it CORRECTS the remedy issue #857 itself proposed. #857 asks canon to state
*"`error` for the scenario-completeness and title-resolution arms"*; the
title-resolution arm's constant is `warning` and was deliberately not dragged by
the flip (orchestrator decision O8, and PR #529's own body records it). The delta
states the arm-by-arm truth instead. Encoding the issue's wording would have
replaced one false sentence with another.

**D2 THROUGH D7 WERE CARRIED BESIDE D1 AND NONE WAS VETOED.** D2 (the
replacement wording copied from the promoted `promotion-fidelity` and
`duplicate-packet` paragraphs rather than invented), D3 (the paragraph's third
sentence CARRIED unchanged because it is still true), D4 (ONE scenario added, at
the `(family, repository, path)` grain the uncited-resolution rule actually keys
on), D5 (the marker: five names, one paragraph, no code span in its reason, and
the predecessor's marker deliberately not restated), D6 (#858's `specs/019`
FR-018 restatement riding this pull request as a severable commit) and D7 (what
is measured and deliberately not taken) each stand as designed. `tasks.md` § 1.3
records that.

## 3. THE RATIFIED SURFACE

**ONE `## MODIFIED` REQUIREMENT, FIVE UNITS REPLACED IN PLACE AT FOUR SITES, ONE
SCENARIO ADDED, ONE MARKER.** The requirement is *Currency of an active change's
MODIFIED requirement blocks* of `doc-health`, and the block is byte-faithful to
canon by CONSTRUCTION — generated by slicing
`openspec/specs/doc-health/spec.md` lines 1588–2009 and applying each
replacement as an exact single-occurrence substitution, so every unit not named
by the marker is canon's own bytes.

| site | canon (retired) | ratified (replaced in place) |
| --- | --- | --- |
| 1 — `:1615` | the lifecycle-standing sentence carrying *"the arms below are advisory"* | the same SHALL, with the rationale corrected: a finding against a draft costs its author one line, *"the scenario-title arm below now carrying an `error` that reds any run configured to fail on it"* |
| 2 — `:1816-1823` | *"This family SHALL be advisory at launch, in both halves of what that means."* + the `warning`/`info` severities and *"deliberately absent from `FAMILY_RESOLUTION`"* | a standing paragraph stating the ARM-BY-ARM truth (`error` for the scenario-title-completeness arm, `warning` for title resolution and ordering, `info` for the carriage ledger and marker defects) and the whole-family `contested` classification, with the resolution row's absence of per-class grain stated as the reason it reaches every class |
| 3 — `:1824-1826` | *"Raising the scenario-completeness arm to `error` and adding the contested classification are ONE later decision …"* | a history paragraph recording the decision as TAKEN: *"MEASURE FIRST, THEN FLIP"* (2026-08-27), the population read at ZERO by the nightly runs of 2026-08-30 and 2026-08-31, the order of 2026-08-31, and the one commit that moved severity and row together |
| 4 — `:1922-1923` | the first scenario's `THEN` *"MUST emit a `warning` finding"* and its `AND` *"MUST NOT cause a run configured `--fail-on error` … to fail"* | three bullets mirroring the promoted `promotion-fidelity` and `duplicate-packet` scenarios: an `error` finding, a run configured `--fail-on error` failing while `--fail-on critical` does not, and the `contested` resolution class |

**THE PARAGRAPH'S THIRD SENTENCE IS CARRIED UNCHANGED AND THAT IS PART OF WHAT
WAS RATIFIED** (D3) — *"No flip is proposed for the carriage ledger in this
change"* — because it is TRUE: no flip has been ruled for that arm and its
constant reads `INFO`. Retiring a true unit is a change truth does not require.

**ONE SCENARIO IS ADDED, AT THE END OF THE BLOCK** (D4) — *This family stops
reporting a path without a citation* — because the `contested` row reaches every
class the family emits, the `info` carriage ledger included, and no scenario
exercised that. It is stated at the `(family, repository, path)` grain
`Finding.match_key()` keys on, with the negative case in its own bullet, so canon
promises only the disappearance the checker detects.

**ONE `Removed from canon by amend-modified-block-currency-standing
(2026-09-10):` MARKER** names all five retired units as code spans and carries
**no code span at all in its reason** (D5), so under the grammar this very
requirement defines it names exactly five units and reports on none of the three
marker-defect grounds. `amend-marker-defect-reporting`'s own marker is
deliberately NOT restated, on this requirement's rule that a marker is not a
carriage unit in either direction.

**AND ONE DOCUMENT COMMIT RIDES THIS PULL REQUEST, SEVERABLE FROM THE DELTA AND
NAMED BY THE RULING.** `2f384fd1` restates
`specs/019-modified-block-currency-family/spec.md` FR-018 to canon's three
marker-defect grounds, quoting the promoted sentence with its line range
(`openspec/specs/doc-health/spec.md:1744-1751`) and leaving a dated amendment
note beside it, in the exact form PR
[#827](https://github.com/opensoft/openxFactory/pull/827) established for the
predecessor's identical residue (#730). `specs/019` is a Speckit build record —
not promoted canon, pinned by no test and by no gate, since
`scripts/doc_health/corpus.py`'s `GOVERNED_ROOTS` never includes `specs/` — so it
is a document catching up with canon promoted at `250d93d7` rather than an
OpenSpec change. It depends on NO part of this delta and is landable alone; the
recording comment names it as riding this pull request, which is the ruling on
D6.

## 4. The bench, and what it settled before the word arrived

### 4.1 The rounds

| bench | commit | verdict |
| --- | --- | --- |
| Copilot round 1 | `0cb10273` (2026-09-10T02:51:38Z) | 🟢 **Approval recommended** — *"The changes are documentation/spec artifacts aligning canon with already-shipped checker behavior; only a minor terminology-consistency nit was found."* One comment (**T1**) |
| Codex round 1 | `0cb10273` (2026-09-10T02:54:45Z) | one **P1** and one **P2** — **T2**, **T3**; both TAKEN |
| Copilot round 2 | `9bf1c649` (2026-09-10T03:48:28Z) | 🟢 **Approval recommended** — 8/8 files, one comment (**T4**) |
| Codex round 2 | `9bf1c649` (2026-09-10T03:56:41Z) | one **P2** — **T5**; TAKEN |
| Copilot round 3 | `b1e4feae` (2026-09-10T04:00:33Z) | 🔵 **Needs a closer look** — the long marker line, named in the review BODY under *"Suppressed comments (1) — Previously missed (1)"* and not yet raised as a thread |
| Copilot round 4 | `bf65954a` (2026-09-10T04:08:42Z) | 🟢 **Approval recommended** — 8/8 files, one comment, which is where **T6** was actually raised as a thread (04:08:42Z) |
| Copilot round 5 | `ab8247fa` (2026-09-10T04:18:34Z) | 🔵 **Needs a closer look** — 8/8 files, **0 new comments** (quoted verbatim at § 4.4) |
| Codex, second request | `ab8247fa` (requested 04:21:10Z) | **ABSENCE** — a usage-limit notice at 04:21:18Z, no review (§ 4.4) |
| Sourcery | `0cb10273` (02:48:57Z) | a Reviewer's Guide summary, not a finding set |

### 4.2 The six threads on the pull request, and their disposition

**SIX THREADS, ALL SIX TAKEN, ZERO UNRESOLVED at the freeze of
2026-09-10T04:45:26Z and zero unresolved at this ratification.** Each was
replied to and resolved as the lane. The thread list is the one the freeze
comment enumerates.

| # | bench | site | finding | disposition |
| --- | --- | --- | --- | --- |
| T1 | Copilot | `specs/doc-health/spec.md:262` | the standing paragraph named the arm two ways — *"Scenario-title completeness"* and *"scenario-title-completeness"* | **TAKEN** at `0441d39e` — the arm now carries canon's own spelling and the module's registered class string, `scenario-title completeness` |
| T2 | Codex **P1** | `specs/doc-health/spec.md:512` | the added scenario promised an uncited-resolution `error` for ANY class's disappearance, which `report.uncited_resolutions` does not deliver: it keys on `Finding.match_key()` = `(family, repository, path)` and skips a prior key any current finding still carries | **TAKEN** at `0441d39e` — narrowed to the path-level key, with the negative case in its own bullet; **the standing paragraph carried the same over-promise and was corrected with it**. The per-class-grain question is a CODE decision and is **REFUSED** as a widening, named as residue at `tasks.md` § 5.3 (§ 4.3) |
| T3 | Codex P2 | `specs/doc-health/spec.md:278` | *"EXACTLY ONE HALF WAS FLIPPED"* was false history — `7f656980` raised `_LAUNCH_SEVERITY` **and** added the `contested` row in one commit | **TAKEN** at `0441d39e` — reworded to *"WAS FLIPPED IN BOTH BY ONE RULING, WHICH RAISED EXACTLY ONE SEVERITY ARM"* |
| T4 | Copilot | `specs/doc-health/spec.md:63` | a 107-character line left by bench round 1's substitution, read as a missing sentence break | **TAKEN** at `b1e4feae` — two paragraphs rewrapped to 79 columns. Whitespace only, and the family's `normalize` collapses whitespace runs and does nothing else, so no unit can move |
| T5 | Codex P2 | `proposal.md:167` | the report-invariance claim was false of the checker's own output: `runner.main` sums every promoted specification's words into `spec_words` and `report.render` folds it into the canon-share headline, so promotion moves the headline | **TAKEN** at `bf65954a` — the claim is split: the FINDING LIST is invariant (a control run over `main` renders the family's whole block byte-identically), the HEADLINE is arithmetic and moves at promotion (+1,216 words, 44,684 → 45,900). `design.md` D7 carried the same phrasing and was corrected with it |
| T6 | Copilot | `specs/doc-health/spec.md:430` | the new `Removed from canon` marker was 2,289 characters on one physical line | **TAKEN** at `ab8247fa` — wrapped to 30 lines and still ONE paragraph, which is the file's own form (six of the eight unit-naming markers in the promoted spec are wrapped). **Parse proven**: no wrapped line matches `_BULLET`, no blank line, and `derive_units` + `suppression` give the identical tuple before and after — 143 canon units, 154 block units, 5 uncarried, 5 suppressed, 0 marker defects, the same five names and the same 871-character reason |

### 4.3 The one thing REFUSED, and why it is residue rather than work

Codex's alternative on **T2** — *"change the implementation and tests to track
individual findings/classes"* — is **REFUSED**, and the refusal is the packet's
charter rather than a preference.

- **It is a CODE decision out of a `code_surface: none` packet.** It would move
  `Finding.match_key`, the ranked-plan grammar `parse_previous` reads and
  writes, and every family keyed on it. This packet's `code_surface: none` is
  MEASURED, and its charter is canon truthfulness about SHIPPED behaviour.
- **The shipped behaviour is what canon now states.** Promoted canon already
  records the same key at `openspec/specs/doc-health/spec.md:2334-2341` and its
  scenario at `:2379`, so the delta's standing paragraph and its added scenario
  are written TO the machinery rather than past it. Promising more would put a
  promise in canon the checker does not keep — which is exactly the defect class
  this packet exists to close.
- **It is owed, not dropped.** `tasks.md` § 5.3 carries it as an OPEN box, and
  under the ruling of 2026-09-06T23:10Z the box ticks ON THE RECORDING: at the
  archive act it ticks by NAMING a filed successor issue, or by the owner's word
  that the grain is correct as it stands. It is not ticked here.

### 4.4 Copilot's standing verdict, and Codex's ABSENCE — both recorded verbatim

**Copilot's last review on the frozen head `ab8247fa`** (2026-09-10T04:18:34Z,
8/8 files reviewed, **0 new comments**, effort level Lite), verbatim:

> ### 🔵 Needs a closer look
>
> The change introduces a large, high-impact specification amendment packet
> whose correctness is primarily semantic/normative and should receive final
> human review despite passing mechanical validation.

**That is the standing of a packet awaiting a ratification word, and it is what
the word of 2026-09-10 supplies.** The verdict asks for human review of
semantic/normative correctness; the operator's ruling on D1 is that review.

**CODEX DID NOT REVIEW THE FROZEN HEAD, AND THE SILENCE IS AN ABSENCE RATHER
THAN AN APPROVAL.** A second `@codex review` was requested at
2026-09-10T04:21:10Z. Codex replied at 04:21:18Z, verbatim:

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the Codex usage dashboard.

A further notice followed at 04:45:35Z (*"You have reached your Codex usage
limits."*). Twenty-four minutes of bounded polling drew no review. **No Codex
pass stands on `ab8247fa`**; its two rounds stand on `0cb10273` and `9bf1c649`,
and both of its findings on this pull request were TAKEN at `0441d39e` and
`bf65954a` respectively. This record states that rather than presenting silence
as assent.

## 5. Why the packet exists: two owed residues of one flip

**THE ORIGIN IS A PAIR OF RESIDUE ITEMS ON A DIFFERENT ACT.** Both issues were
filed by this lane at the archive of `amend-marker-defect-reporting` (PR
[#850](https://github.com/opensoft/openxFactory/pull/850) → `250d93d7`), which
named them in its own ratified `tasks.md` § 5.3 and § 5.4 rather than correcting
them:

- **#857 is the PROMOTED half.** `openspec/specs/doc-health/spec.md` still says
  the `modified-block-currency` family *"SHALL be advisory at launch, in both
  halves of what that means"* while the checker has read the opposite since
  2026-08-31. The flip landed at `7f656980` (PR #529, issue #357) and **AMENDED
  NO SPECIFICATION**, which is why promoted canon has contradicted running code
  for ten days — and contradicted ITSELF, the promoted *A
  modified-block-currency finding its own class map cannot place is itself a
  finding* having recorded the same row as PRESENT on the day the flip landed.
- **#858 is the BUILD-RECORD half.** `specs/019-modified-block-currency-family/`
  FR-018 still stated the ONE reporting ground a marker had before
  `amend-marker-defect-reporting` made it three.

**WHY AN OPENSPEC CHANGE FOR THE FIRST HALF AND NOT A PATCH.** The stale
sentences are PROMOTED, RATIFIED canon. Working rule 3 and this corpus's own
document lifecycle admit exactly one instrument for changing a promoted
requirement — a ratified change carrying a `## MODIFIED` block — and the family
whose standing is misstated is the one that reads MODIFIED blocks for a living.
Editing the promoted file directly would be the defect this capability exists to
report. **This record is the word that closes that loop at the RATIFICATION
step; it does not close #857 or #858**, which close at the archive (§ 7).

## 6. What is NOT ratified, and the residue this word does not reach

- **NOTHING IS PROMOTED.** This ratification edits no file under
  `openspec/specs/`, no script, no test, no contract, no schema and no workflow.
  The `## MODIFIED` block is a DELTA; canon still carries the stale sentences
  until the archive writes the block over it.
- **NO SEVERITY MOVES AND NO ROW IS ADDED.** Every band and the resolution row
  the delta states are read out of the module as it stands. The word ratifies
  canon catching up with running code, not a change of behaviour.
- **THE PER-CLASS DISAPPEARANCE GAP IS OWED, NOT TAKEN** (`tasks.md` § 5.3, open
  box, § 4.3 above). The successor is named at the archive act.
- **`specs/019` FR-024 AND FR-026 ARE NOT EDITED** (`tasks.md` § 6.1, open box).
  Unlike FR-018 they FORESEE the flip in their own words and the feature's
  out-of-scope list names it, so they read as a launch record rather than as a
  current rule; that residue belongs to the FLIP (#357), not to either issue
  this packet takes.
- **NO FLIP OF ANY REMAINING ARM IS PROPOSED** (`tasks.md` § 6.2, open box). The
  title-resolution, drift, pairing and collision classes keep `warning` and the
  ledger keeps `info`.
- **`tasks.md` § 5 (archive) STAYS ENTIRELY OPEN**, and § 6.1–§ 6.2 stay open as
  measured residue rather than work performed.
- **THE ARCHIVED DELTAS THAT CARRIED THE FALSE PARAGRAPH BYTE-FAITHFULLY ARE NOT
  EDITED.** An archived delta is a record of what was ratified.
- **THE `--all --strict` FAILURES ON `main` ARE NOT THIS PACKET'S AND ARE NOT
  FIXED HERE.** Three items fail `--strict` on `origin/main` `804a9170`
  (`change/disposition-codexfactory-declared-renames`, `spec/neutral-product-pin`
  — the `requirements.16.text` SHALL/MUST defect openxFactory #882 names — and
  `spec/repo-boundary-governance`). The failure SET on the ratified tree is
  IDENTICAL to `main`'s, this change is the one extra item and it PASSES, and
  none of the three is touched here (`review/verification-2026-09-10.md` § 2).

## 7. Sequencing, and the landing obligation this word does NOT carry

**NO ORDERING DECLARATION IS OWED, in either direction, and it is measured
rather than assumed.** Enumerated 2026-09-10 over every active
`openspec/changes/*/specs/*/spec.md`: two other active changes carry a
`doc-health` delta — `add-nightly-dashboard-refresh` (`## ADDED` only, seven
refresh-lane requirements) and `settle-aging-staging-topics` (`## MODIFIED` over
*Aging threshold defaults*) — and **neither writes this requirement's key**. The
two-writers ordering rule stated inside the very requirement being modified is
scoped to two ACTIVE writers, so it does not reach this pair. `sequenced_after:
[]` is therefore a POSITIVE root claim and not an omission, and
`scripts/validate-sequenced-after.py` passes on it
(`review/verification-2026-09-10.md` § 4).

**THE ARCHIVE IS A SEPARATE ACT ON A SEPARATE WORD, AND #857 AND #858 CLOSE
THERE.** Under `release-realization` an empty `code_surface` archives ON LANDING
plus its own task list rather than on merged-plus-green realization evidence —
but that archive is not performed by this commit and is not authorized by this
word. The pull request body carries **`refs #857, refs #858`** and **no closing
keyword anywhere**, which is what keeps both origin issues open through this
landing.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE.** The Rule 6 LANDING/LANDED
post belongs to the landing lane on a separate landing word, which the recording
comment of 2026-09-10T11:35:59Z names as a later act in as many words: *"then
bench; then Rule 6 landing on a separate landing word."*
