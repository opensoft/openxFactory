---
code_surface: none — MEASURED, not assumed, on the clone of `main` @ `38c076d1` this packet was authored against. THE PACKET STATES IN CANON WHAT THE FAMILY ALREADY DOES, and neither artifact that carries it is edited: `scripts/doc_health/modified_block_currency.py`'s `suppression()` resolves the third ground BY NAME against the requirement's basis and against the block — `the name matches NO canon unit -> nothing suppressed, and ... the MARKER is reported where the name matches no unit of the block either` — so a carried-forward spent marker is reported today, by the shipped predicate, with no edit; and DROPPING a marker is the absence of an edit rather than an edit, so the option this packet rules lawful costs the module nothing at all. Evidence for the negative: `grep -rn "spent\b.*marker\|inherited marker\|carriage unit" scripts tests` returns the promoted prose's own wording in no production path — promoted prose is read by no script in this repository — and this packet adds no predicate, no `_WHY_*` template, no finding class and no test. NO PRODUCTION FILE AND NO TEST IS TOUCHED: the diff is `openspec/changes/rule-inherited-unit-naming-marker-spent/**`, one README row and one per-change sweep ledger row. The one mechanical consumer of the delta is `doc-health`'s own modified-block-currency family, which reads every active `## MODIFIED` block by construction — a GATE over this packet, not a surface it changes. Under `release-realization` an empty code surface archives ON LANDING plus its own task list rather than on merged-plus-green realization evidence.
target_release: implemented — canon's own doc-only default, quoted rather than inferred: `release-realization` *Realization axis declaration* admits `implemented` (the affected repositories' main lines) or a named aggregation release, and says in the same breath that `A proposal without the declarations is a doc-only change (code_surface: none, target_release: implemented) by default`. The affected repository's main line is openxFactory and nothing else. No contract bundle is cut, nothing under `contracts/` moves, no `contracts/releases/<tag>.digests.yaml` changes, no `contract_bundle_version` is spent, no release tag is owed and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on a separate word.
sequenced_after: [amend-merged-into-empty-tail-standing]
---

# Proposal: rule-inherited-unit-naming-marker-spent

Status: draft
Proposed: 2026-09-11, in lane `openxfactory-1` (display `openXfactory-1`), on
Brett Heap's word of 2026-09-11, verbatim **"land each when green, archive both
when landed, claim 955 and 956"**, given in session at 2026-09-11T12:08:24Z and
recorded on openxFactory
[#955](https://github.com/opensoft/openxFactory/issues/955).
Origin: openxFactory
[#955](https://github.com/opensoft/openxFactory/issues/955), filed UNCLAIMED by
this lane at the archive of `amend-repo-boundary-governance-scope-first-line`
([#958](https://github.com/opensoft/openxFactory/pull/958)), which owed it as
residue `tasks.md` § 6.1 and `design.md` D2b.

**THE WORD COMMISSIONS THE AUTHORING AND RATIFIES NOTHING.** *"Claim 955"*
directs a lane to take the issue; it decided no sentence, no scenario and no
scoping, none of which existed when it was given, and it is recorded here as
the ORIGIN of the AUTHORING and read as nothing more. `.openspec.yaml` carries
drafting provenance with **no approval pair**, every document in the packet
says `Status: draft`, and `tasks.md` § 1 is OPEN. **`design.md` D1 is the
owner's decision and it can end this packet**: it is put as a multiple choice
with the recommendation first, and option 2 would be a re-authoring rather than
an edit. Ratification, promotion and archive are three later acts on three
later words, and openxFactory #955 closes at the ARCHIVE.

## Why

**CANON GIVES A LATER AMENDER TWO OPTIONS AND NAMES NEITHER AS THE ONE IT
OWES.** Two promoted sentences of *Currency of an active change's MODIFIED
requirement blocks* decide it between them. The third of the five marker-defect
grounds reports a marker that

> names something matching no unit of the requirement's basis and no unit of
> the block

and the carriage rule says

> **A marker is NOT a carriage unit, in either direction.** A marker promotes
> into canon with the requirement that carries it, and if it were a unit every
> later block would have to restate every marker any predecessor ever wrote,
> forever. The durable record of a deletion is the archived delta, which is
> where every other archived governance act is read from.

Put together: a requirement whose promoted text carries a unit-naming marker
hands its next amender exactly TWO options — DROP the marker, which the
carriage rule expressly permits, or CARRY IT and take an `info` third-ground
finding, because the unit it names left canon by the act the marker declares
and a block does not restate a retired unit. **There is no third option today
for that form, and canon does not say which of the two an author owes.**

**THAT IS A MEASUREMENT AND NOT AN ARGUMENT.** `design.md` D0 re-takes it on
this tree: **every single unit-naming marker in promoted canon is already
spent** — 16 of them, across 13 requirements in 7 promoted specifications, and
for every one of them every unit it names is absent from the requirement that
carries it. `amend-repo-boundary-governance-scope-first-line`'s D2b took the
same measurement on one real pair and its packet dropped the inherited marker
on canon's own sentence, measuring 0 marker defects.

**AND THIS PACKET IS ITS OWN WITNESS.** Its block inherits a `Removed from
canon` marker from its ordered-delta parent and faces exactly the choice the
issue describes; `design.md` D2 measures BOTH branches on this block's own
bytes rather than reasoning about them, and encodes the drop.

## Why this is NOT a plain fix

**THE SENTENCES ARE PROMOTED, RATIFIED CANON.** Working rule 3 and this
corpus's own document lifecycle admit exactly one instrument for changing a
promoted requirement — a ratified change carrying a `## MODIFIED` block — and
the family whose rule is being stated is the one that reads MODIFIED blocks for
a living. Editing the promoted file directly would be the defect this
capability exists to report.

**AND THE CHECKER IS NOT WRONG ABOUT CANON, WHICH IS WHY THIS IS A PACKET AND
NOT A PATCH.** `suppression()` conforms to the promoted sentence exactly: it
resolves a name against the basis and against the block, and a spent marker's
name matches neither, so the third-ground report is the promoted sentence
working as written. What is missing is not behaviour but a RULING — which of
the two reachable states a later author owes — and a ruling over a promoted
requirement is an amendment of it.

## What Changes

**ONE `## MODIFIED` BLOCK, A PURE ADDITION: FOUR SENTENCES AND TWO SCENARIOS.**
The block is GENERATED by taking the ordered-delta parent's block and applying
three exact single-occurrence edits, never transcribed (`tasks.md` § 3).

- **ADDED, AT THE END OF THE CARRIAGE PARAGRAPH:** four sentences. A
  unit-naming marker is SPENT once the unit it names has left canon by a
  declared act, so a later block SHALL NOT be required to restate it and SHALL
  NOT be reported for omitting it — dropping it is the lawful carriage. Where a
  later block carries a spent marker forward instead, the THIRD ground reports
  that marker and the report is the class working as written. No ground is
  added, none is withdrawn and no suppression moves. And it is read on a marker
  that NAMES a unit and on no other.
- **ADDED, AT THE END OF THE BLOCK:** two scenarios, *A later block drops an
  inherited unit-naming marker* and *A later block carries an inherited
  unit-naming marker forward* — one per half of the rule, because a rule no
  scenario exercises is a rule the next author re-deriving this class has
  nothing to test against, and because pinning one half of a two-option rule
  invites a reader to take that half for the whole.
- **NO UNIT IS RETIRED, AND THEREFORE NO `Removed from canon` MARKER IS OWED
  AND NONE IS WRITTEN** (`design.md` D2, measured through `derive_units`).
- **THE PARENT'S OWN MARKER IS DROPPED**, under the rule this block writes, and
  the `AMENDED BY` note says so in terms.
- **NOT CHANGED:** no ground is added or withdrawn — the class still states
  FIVE — no severity, no threshold, no arm, no finding class, no template, no
  parse, no marker grammar, no disposition rule, and no line of
  `scripts/doc_health/` or `tests/doc-health/`.

## The corpus measurement

Taken 2026-09-11 on the clone of `main` @ `38c076d1` this packet was authored
against, through the family's own `derive_units` so that fenced example markers
are never offered — exactly as they are never offered to a run. The scope is
the corpus **before** this packet.

| measure | count |
| --- | --- |
| promoted requirements scanned | 641 |
| markers in promoted specifications | **18** |
| of `Removed from canon` form | 15 |
| of `Merged into` form | 1 |
| of the pairing form | 2 |
| **unit-naming markers (naming at least one unit)** | **16** |
| **of those, SPENT — every unit they name absent from the requirement carrying them** | **16** |
| promoted requirements carrying at least one spent marker | **13** |
| promoted specifications carrying at least one | 7 |
| active MODIFIED blocks the family reads | 29 |
| of those, blocks carrying a unit-naming marker | 2 |
| marker-defect findings a run raises | **0** |

**EVERY UNIT-NAMING MARKER IN PROMOTED CANON IS ALREADY SPENT**, which is not a
coincidence but the construction: a marker declares a REMOVAL, so the unit it
names is gone from the requirement the moment the declaring block promotes.
**AND THE DEFECT POPULATION IS ZERO**, because no active block has yet carried
one forward — the two active blocks carrying a unit-naming marker,
`add-chain-attestation` and `add-composed-view-authoring`, are both `Merged
into` and each names one unit that matches its resolved basis. So this is a
rule written at the moment it costs nothing and before the first author pays
for its absence.

## Sequencing

`sequenced_after: [amend-merged-into-empty-tail-standing]`, declared rather
than inferred. That change is an ACTIVE RATIFIED writer of THIS requirement
(PR [#947](https://github.com/opensoft/openxFactory/pull/947)), so
`release-realization`'s *Ordered deltas and branch vocabulary* obliges this
later proposal to reference it and to declare its deltas relative to that
change's OUTCOME — and this requirement's own two-writers arm reads that
declaration as the order, "BY DECLARATION AND NEVER BY DATE". **So this
block's PRE-text is the parent's block and not the promoted text the parent
replaces**, read at `a6d373e9` (`design.md` D5). The change id also occurs as a
whole token in this prose, which is the second of the two equivalent
declaration sites `release-realization` admits.

The sibling search is pasted in `design.md` D5 rather than summarized. No other
active change carries a `## MODIFIED` block for this requirement.

## Impact

- **Promoted canon** gains four sentences in one paragraph and two scenarios,
  and loses nothing. No other requirement of `doc-health` is touched, and
  `document-lifecycle` — which owns the marker GRAMMAR — is not amended, this
  packet stating when a marker is SPENT and not how one is written.
- **Running code**: nothing. The third ground already reports the carried case
  and dropping is the absence of an edit, which `tasks.md` § 4 measures rather
  than asserts.
- **Every governed repository's nightly**: no finding starts being emitted and
  none stops on account of the RULE — it changes no predicate — so no
  repository gains or loses a row from it, and the uncited-resolution rule has
  nothing to fire on. The ONE row this packet's own delta raises while it is a
  draft is measured and disclosed in `design.md` D2 and in the pull request
  body rather than dispositioned, and it clears itself.
- **Authors** gain a decision where they previously found two reachable states
  and no rule, which is what #955 reports.

## Ratification — NOT GIVEN

**`design.md` D1 IS THE QUESTION, AND IT IS PUT AS A MULTIPLE CHOICE WITH THE
RECOMMENDATION FIRST.** Option 1 (recommended and encoded) rules the two-option
state correct in four sentences and two scenarios, with no code surface. Option
2 adds a THIRD option — a suppression for an inherited marker whose named unit
left canon by a declared act — which is one predicate, one `_WHY_*` template,
its own scenario and a CODE SURFACE, and which would change this packet's
archive rule. **If Brett Heap takes option 2 this packet is RE-AUTHORED, not
amended.** Nothing here is ratified until he rules, and the ruling is his act
and never this lane's judgment.

## What this proposal does NOT claim

- **The commissioning word is not read as an approval.** *"Claim 955 and 956"*
  directed the authoring. No sentence existed when it was given.
- **It does not add a ground, a severity, a threshold or a suppression.** The
  class still states FIVE grounds; the added sentences state which of two
  already-reachable outcomes is the lawful carriage and name what the other
  costs.
- **It does not reach a marker that names NOTHING.** The pairing form's whole
  tail is a reason by construction, and a `Merged into` marker whose tail names
  no superseded title is `amend-merged-into-empty-tail-standing`'s question and
  is answered there. A marker with no names reaches the third ground through no
  name at all, so nothing here decides anything about it (`design.md` D6).
- **It does not sweep the sixteen spent markers already in promoted canon.**
  They are correct records of ratified removals; the rule speaks to what a
  LATER BLOCK owes, and no promoted byte is edited by this packet.
- **It does not touch `document-lifecycle`**, whose marker grammar says how a
  unit is NAMED and carries no reporting rule.
- **It closes no issue.** openxFactory #955 closes at the ARCHIVE, which is a
  separate act on a separate word, and this pull request's body carries `refs`
  and no closing keyword.
