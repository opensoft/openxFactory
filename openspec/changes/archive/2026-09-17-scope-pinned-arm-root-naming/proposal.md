---
Status: ratified
code_surface: none — MEASURED, not assumed, on the clone of `main` @ `8944758c` this packet was authored against. THE PACKET STATES IN CANON WHAT THE REALIZED ARM ALREADY DOES, and no production file is touched. The two findings this delta names are emitted today, by the shipped code, exactly as the clarified sentence reads — the lexically malformed pinned target at `scripts/doc_health/families.py:1573-1576` (refused at `:1572`, BEFORE the `value.split("/", 1)` of `:1578` and the `_pin_roots(...)` call of `:1580`), naming the VALUE; and the empty-root-set finding at `:1587-1592` (reached only where `_pin_roots` returned nothing at `:1580-1581`), naming the REPOSITORY. Every one of the arm's other thirteen findings names its root already (`:1606-1611`, `:1618-1625`, `:1634-1638`, and all ten of `_judge_pinned_record`, `:1653-1736`), so the clarified obligation refuses nothing the arm emits and demands nothing it does not. Evidence for the negative — the diff is `openspec/changes/scope-pinned-arm-root-naming/**`, one README bullet and one per-change sweep-ledger row, plus (if the corpus opens one) a named row in `tests/doc-health/test_modified_block_currency_self_gate.py`'s `_LEDGER_SUBJECTS`, which is bookkeeping this repository's own self-gate demands of every active MODIFIED block and never a predicate, a severity, a threshold or an assertion. No script under `scripts/doc_health/` is edited, no test asserts new behaviour, and nothing is left to realize after this pull request lands, which is the test `release-realization`'s archive gate applies to an empty code surface.
target_release: implemented — the affected repository's main line (openxFactory) and nothing else. `release-realization`'s *Realization axis declaration* admits `implemented`, a named aggregation release, or `deferred-allocation`, and makes a doc-only change (`code_surface: none`, `target_release: implemented`) the DEFAULT; `none` is NOT a sanctioned token and the house gate refuses it (`scripts/target_release.py:93,110,155` — the same reading the sibling packet `repoint-chain-anchoring-medxchain-citation` recorded on PR #998). No contract bundle is cut, nothing under `contracts/` moves, no release tag is owed and no consumer's pin advances to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on a separate word.
sequenced_after: []
---

# Proposal: scope-pinned-arm-root-naming

Status: ratified
Ratified: 2026-09-16T13:43:18Z by Brett Heap (openxFactory repository
owner), first-hand, in session to lane `openxfactory-2` (display
`openXfactory-2`, session c0d09b6d) — A TYPED SENTENCE, NOT A SELECTION,
verbatim: "ratify 1052 when green, then 1050". THE ONE CITATION: openxFactory
#1047, comment
https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379.
Record: `review/ratification-2026-09-16.md`. **RATIFIED — OQ-1 OPTION (a) AS
FILED, AT THE HEAD THE WORD MET (`92d3e0e2`).** No byte of the delta moves by
this act; `tasks.md` § 1.1 is ticked on this word and no other box moves.
Realization and archive remain separate later acts on Brett Heap's word
(`#1050` is a separate packet, named by the word's ordering clause and
outside the scope of this origin).
Amended: 2026-09-17 by Brett Heap, the same ratifier, first-hand, in session —
an interactive multiple-choice selection, verbatim ***"Apply the narrowing"***,
answering the RULING NEEDED this packet's own record posted. THE ONE CITATION:
openxFactory #1047, comment
https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5714432684.
**ONE BULLET MOVES AND ONLY ITS WHEN** — the sibling scenario *A pinned target
names a pin no resolution root carries*, narrowed to "…and at least one
selected root whose boundary was successfully searched". Record:
`review/ratification-2026-09-16.md` § Addendum, 2026-09-17. No decision, no
scope, no `tasks.md` § 1 box and no origin field is reopened by it.

**THE PARAGRAPH IMMEDIATELY BELOW RECORDS THE AT-FILING STATE (2026-09-15)
AND IS KEPT VERBATIM AS HISTORY.** Its present-tense claims — "NO RATIFYING
WORD HAS BEEN GIVEN", carrying `Status: draft` — were true at filing and are
superseded by the ratification recorded above.

Proposed: 2026-09-15, in lane `openxfactory-2` (display `openXfactory-2`), from
openxFactory [#1047](https://github.com/opensoft/openxFactory/issues/1047), a
finding FILED UNCLAIMED at the completion of the
`extend-prose-tagging-target-to-pinned-capabilities` arc and claimed by this
lane on 2026-09-15T20:43:33Z. **NO RATIFYING WORD HAS BEEN GIVEN.** Nothing
here is ratified, promoted or archived by this filing; `tasks.md` § 1 is Brett
Heap's act and is not ticked by this lane.

## Why

**CANON SAYS `EVERY` AND THE REALIZED ARM EMITS TWO FINDINGS THAT CANNOT OBEY
IT.** The promoted `document-lifecycle` requirement *Prose tagging marker
hygiene* states, at `openspec/specs/document-lifecycle/spec.md:478-481`:

> and EVERY finding the pinned arm emits SHALL NAME THE ROOT OR ROOTS it
> resolved against, or failed to, since under two roots a bare "no pin record"
> sentence cannot be acted on and under one root the named root is what makes
> the difference readable.

Two of the fifteen findings `_pinned_arm` and its record judge emit are reached
BEFORE ANY ROOT IS SELECTED, so there is no root for them to name:

- **The lexically malformed pinned value.** `scripts/doc_health/families.py:1572`
  refuses the value on `_PINNED_VALUE.fullmatch` and the finding at `:1573-1576`
  names THE VALUE (`malformed pinned target={target} at line {lineno}`). That
  refusal precedes the `pin_id, capability = value.split("/", 1)` of `:1578`
  and the `_pin_roots(ctx, doc.repo)` of `:1580`, which is not an implementation
  choice but the SAME requirement's own order, stated twice — "the deterministic
  pass MUST make that judgement BEFORE it constructs any pin-record path,
  performs any pin lookup, or reads any file for it" (`:241-245`), and the
  scenario *A pinned target is lexically malformed* (`:587-590`), "the pass MUST
  NOT construct a pin-record path, perform a pin lookup, or read any file for
  that value".
- **The document whose repository has no resolution root in the run.**
  `_pin_roots` returns an empty list at `:1580` where the run's `repo_paths`
  carries neither the document's repository nor `openxFactory`, and the finding
  at `:1587-1592` names THE REPOSITORY (`no resolution root for repository
  {doc.repo} in this run`). The EMPTY ROOT SET IS THE FINDING'S WHOLE SUBJECT,
  so a root named here would be a root the run does not have.

**THE OTHER THIRTEEN NAME THEIR ROOT ALREADY**, measured over every `hit(ERROR`
in the arm on this tree — the boundary refusal (`:1606-1611`, `root {name}`),
the containment refusal (`:1618-1625`, through the `rule` built at `:1617-1622`),
the searched-roots miss (`:1634-1638`, `under root(s) {', '.join(searched)}`)
and all ten findings of `_judge_pinned_record` (`:1653-1736`, `in root {root}`).
So the obligation is doing its work everywhere it CAN be obeyed.

**IT WAS RAISED AND RULED STANDS AT THE ARCHIVE, WHICH IS WHY IT IS A PACKET
AND NOT A PATCH.** The defect was surfaced by Copilot on the archive pull
request [#1042](https://github.com/opensoft/openxFactory/pull/1042) (merged
2026-09-15T19:35:11Z → `8944758c`) and ruled STANDS there — the sentence is
ratified canon promoted BYTE-IDENTICAL, and an archive act may not edit the
text it promotes. openxFactory #1047 records that ruling and files the
successor, which is this packet. Editing the promoted file directly would be
the defect `document-lifecycle` exists to report.

**AND THE SENTENCE'S OWN RATIONALE IS ABOUT FINDINGS THAT HAVE A ROOT.** The
archived design paragraph that wrote it says so in its own words
(`openspec/changes/archive/2026-09-15-extend-prose-tagging-target-to-pinned-capabilities/design.md`,
D-2, the ROOT paragraph):

> And because there can be two roots, EVERY finding the pinned arm emits names
> the root it resolved against or failed to: under an aggregate run a bare "no
> pin record for `<pin-id>`" cannot be acted on.

A root makes a RESOLUTION ATTEMPT readable. A finding emitted before any
resolution attempt exists has no attempt to make readable, and naming a root
there would be inventing evidence rather than supplying it.

## What Changes

**ONE `## MODIFIED` BLOCK OVER `document-lifecycle` *Prose tagging marker
hygiene*, RESTATING CANON IN FULL, MOVING THE ROOT-NAMING SENTENCE, REFRESHING
ONE STALE SOURCE-CITATION POINTER BESIDE IT (fix round 5), NARROWING ONE
CLAUSE OF A SIBLING SCENARIO'S WHEN (round 1, NARROWED AGAIN 2026-09-17 BY THE
RATIFIER), AND ADDING ONE SCENARIO.** The block was GENERATED from canon at
filing by a script that sliced the promoted requirement whole and applied, AT
FILING, EXACTLY ONE single-occurrence replacement — the root-naming sentence —
before appending ONE scenario; the WHEN clause below was NOT the filing
generator's work but fix round 1's, which added the script's second
single-occurrence replacement (`tasks.md` § 2.2). Nothing was transcribed at
any round. Fix round 5 then hand-applied the pointer refresh as a further
single-occurrence textual correction. Fix round 5 ALSO narrowed the WHEN clause
a second time, and fix round 6 REVERTED that second narrowing — ratified
normative text is the ratifier's to amend, not the lane's
(`review/ratification-2026-09-16.md` § Addendum, 2026-09-16).
**AND ON 2026-09-17 THE RATIFIER HIMSELF APPLIED IT**, verbatim *"Apply the
narrowing"* — openxFactory
[#1047 comment 5714432684](https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5714432684),
recorded at `review/ratification-2026-09-16.md` § Addendum, 2026-09-17 — so the
WHEN below lands AS AMENDED BY ITS RATIFIER, and no longer as ratified at
`92d3e0e2`.

- **CHANGED — ONE BODY SENTENCE.** The root-naming obligation is scoped to the
  findings that reach root selection, and the two that do not are named with
  what each names instead: a pinned value the lexical grammar refuses names THE
  VALUE, no path having been built and no root having been chosen for it; a
  document whose repository has no resolution root in the run names THE
  REPOSITORY, the run's root set for it being empty. The sentence's first half
  (the root set is the run's input, not the arm's choice) and its whole
  rationale clause are carried word for word.
- **CORRECTED — ONE STALE SOURCE-CITATION POINTER, MECHANICAL AND NOT A
  NORMATIVE CHANGE (fix round 5).** The paragraph carrying the root-naming
  obligation opens with canon's own citation of where capability resolution
  reads the root precedence: `scripts/doc_health/families.py:1317-1321`.
  THAT POINTER IS STALE IN CANON ITSELF — line range `:1317-1321` is
  `_topic_outcome` on `main` today, an unrelated function; the root-precedence
  logic this sentence describes now lives in `_resolve_capability` (~:1490)
  and `_pin_roots` (~:1548), moved there since the sentence was written. This
  delta corrects the citation to name the two functions directly, with no
  line numbers to drift again, SO THE BLOCK PROMOTES A TRUE CITATION RATHER
  THAN REPEATING CANON'S DRIFTED ONE. Nothing else in the sentence moves — no
  SHALL, no obligation, no root-precedence claim, and no scenario.
- **CHANGED — ONE CLAUSE OF A SIBLING SCENARIO'S WHEN (round 1, THEN AMENDED
  BY THE RATIFIER 2026-09-17).** The restated scenario *A pinned target names
  a pin no resolution root carries* keeps its THEN and both its other AND
  bullets untouched; only its WHEN moves. Unscoped, that WHEN — "no pin record
  for `<pin-id>` exists under any root of the run's precedence" — is ALSO true
  of the empty-root-set case, which the new scenario below gives a DIFFERENT
  outcome (no root named, by design), so ROUND 1 added "…and at least one
  resolution root was selected for the run", excluding the empty-root-set case.
  **THAT CLAUSE IS NOT ENOUGH, AND BRETT HEAP RULED THE NARROWING IN.** Root
  SELECTION alone satisfies it, but `_pinned_arm` appends a root to `searched`
  only AFTER that root's `contracts/` directory clears `boundary_dir`
  (`scripts/doc_health/families.py:1604-1613`); a root whose boundary check
  fails draws its OWN finding instead (*A root's contracts directory is itself
  a symlink*) and never reaches `searched`. Where EVERY root `_pin_roots`
  returns fails that check, `searched` stays empty, the trailing `if searched:`
  guard (`:1633`) never fires, and NO aggregate "unresolved pinned target: no
  record under root(s)" finding is emitted at all — so the round-1 WHEN
  described, on that one path, a finding the realized arm does not emit, which
  is the exact collision `design.md` D-1 exists to prevent. **THE WHEN NOW
  READS "…and at least one selected root whose boundary was successfully
  searched"**, which excludes the all-roots-boundary-refused case and leaves
  the scenario's own subject — a `<pin-id>` absent from every root the run
  ACTUALLY SEARCHED — exactly as it was, still requiring the finding to name
  the root or roots searched. Nothing is left uncovered: the independent
  scenario *A root's contracts directory is itself a symlink* already requires
  the per-root boundary finding for each refused root.
  **THE HISTORY OF THIS ONE CLAUSE, BECAUSE THE AUTHORITY MATTERS MORE THAN
  THE TEXT.** Fix round 5 applied exactly this narrowing IN THE LANE'S OWN
  NAME; fix round 6 REVERTED it, ratified normative scenario text being the
  ratifier's act to amend and not the lane's, and posted a RULING NEEDED to
  openxFactory #1047. Brett Heap answered it on 2026-09-17 — an interactive
  multiple-choice selection, verbatim *"Apply the narrowing"*, openxFactory
  [#1047 comment 5714432684](https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5714432684)
  — so the clause above is BYTE-FOR-BYTE round 5's text applied under the
  authority round 5 lacked. `review/ratification-2026-09-16.md` § Addendum,
  2026-09-17 carries the word, the contradiction as it was put, and what did
  and did not move.
- **ADDED — ONE SCENARIO**, at the end of the block: *A finding emitted before
  root selection names what it judged* — five bullets, naming what each of the
  two findings names, that neither is required to name a root, and that the run
  completes; the last bullet restates that every finding AFTER root selection
  still names its root, so no reader takes the exception for the rule.
- **MEASURED THROUGH THE FAMILY'S OWN `derive_units`**, RE-RUN AFTER THE
  RATIFIER'S 2026-09-17 AMENDMENT, over canon's block and this block alike —
  canon 209 units (unchanged: canon is not edited), this block 215 (unchanged
  throughout: no round added or removed a bullet), **EXACTLY THREE UNCARRIED
  UNITS** (the pointer-bearing sentence, kept from round 5; the sibling
  root-naming sentence being scoped; and the sibling scenario's WHEN bullet,
  its wording AS AMENDED — the WHEN bullet has been uncarried against canon
  since round 1, canon carrying no such clause at all, regardless of which
  wording it holds) and NINE new ones (the pointer sentence's corrected
  successor; the root-naming sentence's successor; the WHEN bullet as amended;
  and the new scenario's title and its five bullets). A unified diff of the
  generated block against canon's is FOUR hunks — the pointer-bearing sentence
  (kept from round 5), the root-naming sentence, the one WHEN clause, and the
  appended scenario, each at a different place in the file — and `git diff
  --numstat` against canon's block reads **21 added, 8 removed**. **EVERY ONE
  OF THESE FIGURES IS THE SAME UNDER EITHER WORDING OF THE WHEN**, the clause
  being one physical line either way — so round 6's revert and the ratifier's
  2026-09-17 re-application both leave them where fix round 5 first put them.
  **THE FIGURES BY ROUND, LABELLED RATHER THAN CONFLATED:** at filing, TWO
  hunks, 17 added / 4 removed, canon 209, block 215, ONE uncarried, SEVEN new;
  after round 1's WHEN clause, THREE hunks, 18 added / 5 removed, TWO
  uncarried, EIGHT new; from round 5's pointer refresh onward — round 6's
  revert and the 2026-09-17 amendment included — FOUR hunks, 21 added / 8
  removed, THREE uncarried, NINE new. No scenario title, no OTHER scenario
  bullet and no other body sentence moves. No `Removed from canon` or `Merged
  into` marker is owed: nothing is deleted — every uncarried unit has a
  successor in the same block that says MORE, or a truer citation, and never
  less (`design.md` D-1).
- **NOT CHANGED — BEHAVIOUR.** No predicate, severity, threshold, finding
  class, remedy line, marker grammar or root precedence moves, and no line of
  `scripts/doc_health/` is edited. The realized arm already matches the
  clarified reading; that is the measurement above and not an argument.
- **NOT CHANGED — THE OTHER ARMS.** The supersedes refusal for a reserved
  `pinned:` prefix (`scripts/doc_health/families.py:1806-1811`) is emitted by
  `fam_tag_hygiene` and not by the pinned arm, carries its own promoted
  scenario, and is outside this sentence both before and after this delta.

## Sequencing

`sequenced_after: []` is a CORROBORATED ROOT CLAIM, taken at authoring on
`8944758c`: NO OTHER ACTIVE CHANGE HOLDS A `## MODIFIED` BLOCK OVER *Prose
tagging marker hygiene* — that is the fact the claim rests on, not a count of
where the title appears, and the qualifier is load-bearing: read in the
indexed tree, this packet IS the one active change that now holds such a
block, so the claim is about every OTHER active change and not about this one.
Measured at `8944758c` (before this packet's own delta existed), the
requirement title occurs under `openspec/specs/` and
`openspec/changes/` in exactly THREE places: canon itself
(`openspec/specs/document-lifecycle/spec.md:218`) and TWO ARCHIVED
packets — the one that promoted this very sentence
(`openspec/changes/archive/2026-09-15-extend-prose-tagging-target-to-pinned-capabilities/specs/document-lifecycle/spec.md:5`)
and the earlier one that first added the requirement
(`openspec/changes/archive/2026-07-09-concretize-prose-tagging-syntax/specs/document-lifecycle/spec.md:35`,
an `## ADDED` requirement). NEITHER ARCHIVED PACKET IS ACTIVE AND NEITHER
CARRIES A LIVE `## MODIFIED` BLOCK, so neither is a sibling this packet must
sequence after; once this packet's own delta exists it is a fourth occurrence
of the title, and it is the writer in question rather than a co-writer of it.
The only OTHER active change carrying a `document-lifecycle` delta at all is
`prepare-openspec-1-12-readiness`, whose delta is an `## ADDED` requirement
(*A promoted specification carries a written Purpose, repaired in the
promoted specification*) and touches no requirement this packet writes.

## Impact

- **Promoted canon** gains a scoped obligation and one scenario, and loses
  nothing. No other requirement of `document-lifecycle` is touched, and
  `doc-health` — which owns the reporting families — is not amended.
- **Running code**: nothing. Both findings this delta names are emitted today
  in exactly the shape the clarified sentence describes.
- **Every governed repository's nightly**: no finding starts being emitted and
  none stops. The one `info` row this packet's own MODIFIED block raises while
  it is active is the carriage-ledger arm's audit trail for the restatement,
  disclosed here and in the pull request body rather than dispositioned, and it
  retires when this packet archives and its block is promoted.
- **Authors and stewards** gain a sentence that can be obeyed by every finding
  it reaches, instead of one that two findings falsify by construction.

## The decision, put for a veto (one question)

**OQ-1 — the shape of the fix.** Put with the recommendation first;
`design.md` D-1, D-2 and D-3 carry the reasoning.

- **(a) RECOMMENDED, AND WHAT THIS DELTA ENCODES.** Scope the sentence to
  findings that reach root selection and name the two pre-selection findings
  with what each names instead; narrow one clause of a sibling scenario's WHEN
  so the empty-root case keeps one outcome, not two; and add one scenario. No
  code surface.
- **(b) Widen the ARM instead**, so that both findings name a root. REFUSED in
  `design.md` D-2 — a root cannot be named before it exists, and reaching one
  would require selecting roots before the lexical grammar refuses the value,
  which two ratified sentences forbid.
- **(c) Delete the sentence.** REFUSED in `design.md` D-3 — it is the sentence
  that makes a two-root finding actionable, and the promoted scenario *A pinned
  target's record lives only in the root a single-repository run does not have*
  (`:654-658`) would be left standing alone on an obligation nothing states.

## What this proposal does NOT claim

- **It promotes nothing.** The block reaches
  `openspec/specs/document-lifecycle/spec.md` at the ARCHIVE act, on a separate
  word, and not on this pull request landing.
- **It rules nothing about the archive act of #1042.** That ruling — the
  sentence promoted byte-identical, the archive not editing it — STANDS and is
  the reason this packet exists.
- **It does not touch `doc-health`**, which owns the finding families, nor any
  requirement of `neutral-product-pin`.
- **It does not reach the supersedes arm** or any finding outside the pinned
  arm.
- **It closes no issue.** openxFactory #1047 closes at the ARCHIVE, a separate
  act on a separate word; this pull request's body carries `refs` and no
  closing keyword.
