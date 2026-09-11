---
code_surface: none — MEASURED, not assumed, on the clone of `main` @ `96b4835b` this packet was authored against. The behaviour this packet states in canon IS ALREADY THE SHIPPED BEHAVIOUR and neither of the two artifacts that carry it is edited: `scripts/doc_health/modified_block_currency.py`'s fifth-ground predicate is `marker.form == "removed" and not marker.names and not marker.quoted`, so a `Merged into` marker never reaches it, and each of the other four grounds is reached through `marker.names` or `marker.quoted`, both empty for a tail carrying no code span; `tests/doc-health/test_modified_block_currency.py::test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT` has asserted `findings == []` on exactly that shape since 2026-09-10. NO PRODUCTION FILE AND NO TEST IS TOUCHED BY THIS PACKET: the diff is `openspec/changes/amend-merged-into-empty-tail-standing/**`, one README row and one per-change sweep ledger row. Evidence for the negative: `grep -rn "names no superseded title" scripts tests` returns the module docstring and the comment beside that predicate and NOTHING that reads the promoted sentence, promoted prose being read by no script in this repository. The one mechanical consumer of the delta is `doc-health`'s own modified-block-currency family, which reads every active `## MODIFIED` block by construction — a GATE over this packet, not a surface it changes. Under `release-realization` an empty code surface archives ON LANDING plus its own task list rather than on merged-plus-green realization evidence.
target_release: none — no code surface, no contract bundle, no digest set and no release tag. Nothing under `contracts/` is touched, no `contracts/releases/<tag>.digests.yaml` moves, and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on Brett Heap's word.
sequenced_after: []
---

# Proposal: amend-merged-into-empty-tail-standing

Status: draft
Proposed: 2026-09-11, in lane `openxfactory-1` (display `openXfactory-1`), on
Brett Heap's ruling of 2026-09-11, verbatim **"Rule the silence correct in
canon"**, given in session by multiple choice (~01:3xZ) and recorded on
openxFactory
[#914](https://github.com/opensoft/openxFactory/issues/914#issuecomment-5628349929)
at 2026-09-11T02:06:38Z.
Origin: openxFactory
[#914](https://github.com/opensoft/openxFactory/issues/914), filed UNCLAIMED by
this lane at the archive of `amend-marker-declaring-nothing`
([#926](https://github.com/opensoft/openxFactory/pull/926) → `114d6e3d`), which
owed it as residue `tasks.md` § 7.1 and `design.md` D6.

**THE RULING SETTLES THE DESIGN. IT DOES NOT RATIFY THIS TEXT, AND THIS PACKET
IS A `Status: draft` PROPOSAL EVERYWHERE.** Brett Heap chose between the two
options #914 put — *"Rule the silence correct"* and *"Report it as a sixth
ground"* — and took the first, which decides **`design.md` D1's DIRECTION**.
What it did not do, and could not, is approve a sentence nobody had written
when it was given. **NO APPROVAL PAIR IS DECLARED AND NONE IS IMPLIED:**
`.openspec.yaml` carries drafting provenance only — the lawful unapproved shape
`add-drafted-proposal-origin` (issue #318) defined — and ratification,
promotion and archive are three later acts on later words. The decision most
worth a veto is therefore not WHETHER but **HOW**: `design.md` **D1** is the
sentence's exact wording, put as a confirm-or-veto with the rejected
alternative written out beside it.

## Why

**CANON SAYS, IN TERMS, THAT IT DOES NOT DECIDE A QUESTION THAT IS NOW
DECIDED.** `openspec/specs/doc-health/spec.md`, inside *Currency of an active
change's MODIFIED requirement blocks*, states at `:1765-1771`:

> THE FIFTH GROUND SHALL BE READ ON THE `Removed from canon` FORM ALONE: the
> pairing form names no units by construction, its whole tail being a reason,
> so a pairing marker carrying no code span declares exactly what that form
> declares and SHALL NOT be reported on this ground; and a `Merged into` marker
> whose tail names no superseded title is a question this requirement does not
> decide, its destination standing in the prefix where that form's declaration
> has always been read.

That last clause is the residue `amend-marker-declaring-nothing` recorded
against itself. Its `design.md` D6 left the shape alone deliberately — #860
scoped itself to the removal form, and *"inventing a sixth ground here would
repeat the fault the predecessor packet exists to correct"* — and PINNED the
silence with `test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT` so
that it was *"a decision a later act can overturn rather than a gap it has to
rediscover"*. #914 is that later act, and Brett Heap's ruling of 2026-09-11
took the option that keeps the silence and writes it down.

**AFTER THAT RULING THE CLAUSE IS FALSE, AND A FALSE CLAUSE IN A NORMATIVE
SENTENCE IS NOT AN EDITORIAL MATTER.** A reader who reaches for the rule finds
canon saying the requirement does not decide it. The remedy is one sentence,
and it has to REPLACE that clause rather than sit beside it — which is
`design.md` D2, decided by measurement rather than by preference.

## Why this is NOT a plain fix

**THE SENTENCE IS PROMOTED, RATIFIED CANON.** Working rule 3 and this corpus's
own document lifecycle admit exactly one instrument for changing a promoted
requirement — a ratified change carrying a `## MODIFIED` block — and the family
whose rule is being stated is the one that reads MODIFIED blocks for a living.
Editing the promoted file directly would be the defect this capability exists
to report.

**AND THE CHECKER IS NOT WRONG ABOUT CANON, WHICH IS WHY THIS IS A PACKET AND
NOT A PATCH.** `suppression` conforms to the promoted sentence exactly: the
fifth ground reads `marker.form == "removed"`, and its own comment records the
merge form's empty tail as *"a question nobody has ruled"*. A ruling over that
question is an amendment of the requirement, not a change of behaviour — which
is why this packet moves no line of code and why its `code_surface` is empty.

## What Changes

**ONE `## MODIFIED` BLOCK, ONE SENTENCE REPLACED, ONE SENTENCE ADDED, ONE
SCENARIO ADDED.** The block is GENERATED by slicing the promoted requirement
and applying one exact single-occurrence substitution, never transcribed
(`tasks.md` § 3).

- **RETIRED AND REPLACED IN PLACE:** the fifth-ground sentence quoted above. Its
  replacement keeps the removal-form scoping and the whole pairing-form
  exclusion **word for word** and drops only the clause that says the merge
  form's empty tail is undecided.
- **ADDED, IN THE SAME PARAGRAPH:** one sentence stating the ruling — a
  `Merged into` marker declares its DESTINATION in its PREFIX and owes no tail;
  a tail naming no superseded title is SILENT BY RULE, not reported on the
  fifth ground and, where it carries no code span at all, reaching none of the
  other four either, so NO ground fires and NO ground is added. The sentence
  ends by keeping a code span the reason DOES quote subject to the second
  ground, so the silence is read at the shape and never at the form.
- **ADDED, AT THE END OF THE BLOCK:** one scenario, *A merge marker's tail names
  no superseded title*. A rule no scenario exercises is a rule the next author
  re-deriving this class has nothing to test against — and without it the
  ruling would be pinned only by a test, which is running code standing in for
  canon.
- **ONE `Removed from canon` MARKER**, naming the one retired unit, its reason
  carrying no code span at all (`design.md` D2 and `tasks.md` § 3.3).
- **NOT CHANGED:** no ground is added or withdrawn — the class still states
  FIVE — no severity, no threshold, no arm, no finding class, no template, no
  parse, no marker grammar, no disposition rule, and no line of
  `scripts/doc_health/` or `tests/doc-health/`.

## The corpus measurement

Taken 2026-09-11 on the clone of `main` @ `96b4835b`, through `derive_units` so
that fenced example markers are never offered — exactly as they are never
offered to a run. The scope is the corpus **before** this packet.

| measure | count |
| --- | --- |
| markers of any form | **27** |
| of `Removed from canon` form | 15 |
| of `Merged into` form | **3** |
| of the pairing form (`Modified over …`) | 9 |
| **`Merged into` markers whose tail carries no code span** | **0** |
| `Removed from canon` markers with an empty tail | 0 |
| pairing-form markers carrying no reason at all | 0 |
| active MODIFIED blocks the family reads | **29** |
| of those, blocks carrying a unit-naming marker | **2** |
| marker-defect findings a run raises | **0** |

**THE POPULATION OF THE RULED SHAPE IS ZERO**, which is what makes this a
ruling written before it is needed rather than a correction of live rows. All
three `Merged into` markers name exactly one superseded title each; the two
inside active blocks are `add-chain-attestation` and
`add-composed-view-authoring`, each naming one unit that matches its resolved
basis.

## Impact

- **Promoted canon** gains one sentence and one scenario and loses one clause.
  No other requirement of `doc-health` is touched, and `document-lifecycle` —
  which owns the marker GRAMMAR — is not amended, this packet stating when a
  marker is REPORTED and not how one is written.
- **Running code**: nothing. The module and its tests already behave exactly as
  the amended sentence states, which `tasks.md` § 4 measures rather than
  asserts.
- **Every governed repository's nightly**: nothing. Both directions of this
  amendment are silence — no finding starts being emitted and none stops — so
  no repository can gain or lose a row, and the uncited-resolution rule has
  nothing to fire on. The estate-wide run the predecessor owed at its landing
  is not owed here for that reason, and `design.md` D6 says so with its
  measurement.
- **Authors** gain a decision where they previously found a recorded
  non-decision.

## Sequencing

`sequenced_after: []`, an explicit root claim, MEASURED rather than assumed: no
OTHER active change carries a `## MODIFIED` block for this requirement — this
packet carries one, which is the delta itself and not a co-writer of it. The
three OTHER active changes that name it at all mention it in prose
(`prepare-openspec-1-12-readiness/tasks.md`,
`disposition-codexfactory-floor-relocation-retitle/design.md`,
`disposition-codexfactory-declared-renames/design.md`) and carry no delta over
it, so the two-writers ordering this very requirement reports is not in play.

## Ratification — OWED, NOT GIVEN

Brett Heap's ruling of 2026-09-11 decides `design.md` D1's DIRECTION and
authorizes this authoring. **IT IS NOT A RATIFICATION OF THIS WORDING**, and
this packet does not read it as one: every document carries `Status: draft`,
`.openspec.yaml` carries no `approved_by` and no `approved_on`, and `tasks.md`
§ 1 stays OPEN. The pull request is a DRAFT and asks one question — D1's
sentence, confirm or veto.

## What this proposal does NOT claim

- **It does not claim the ruling approved this text.** The ruling chose between
  two encodings; the sentence was written after it.
- **It does not add a sixth ground**, and the added sentence is written so that
  it cannot be read as one: it is a prohibition on reporting, the count of
  grounds is left at FIVE in the same paragraph, and the scenario's THEN bullet
  says MUST NOT report rather than MUST report.
- **It does not widen the silence to the form.** A `Merged into` marker whose
  reason quotes a code span is still subject to the second ground, said in the
  sentence and pinned by the scenario's last bullet.
- **It does not touch `document-lifecycle`**, whose marker grammar says how a
  unit is NAMED and carries no reporting rule — the boundary
  `amend-marker-defect-reporting` § 2.4 checked in both directions and left
  standing.
- **It does not edit the promoted markers or the archived deltas that carry
  them.** They are records of ratified removals and every one of them is
  correct under the amended sentence.
- **It closes no issue.** openxFactory #914 closes at the ARCHIVE, which is a
  separate act on a separate word, and this pull request's body carries `refs`
  and no closing keyword.
