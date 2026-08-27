---
code_surface: openxFactory (`scripts/doc_health/modified_block_currency.py` — a new module owning the twenty-second deterministic family: the active-change delta reader, the promoted-requirement reader, the normative unit derivation (backtick masking, the sentence split, bullet units, the undivided dated note), the same-kind exact matcher, the three comparison arms, the two-writers resolution against an active sibling's outcome, the reserved-marker parser and its two forms, and the disposition read; `scripts/doc_health/families.py` — one import, one registration line in `FAMILIES`, one note recording why the family is deliberately absent from `FAMILY_RESOLUTION`, and the module docstring's owner list; `scripts/doc_health/__init__.py` — one entry in `FAMILY_IDS` so the family gets its own report section; `tests/doc-health/test_modified_block_currency.py` plus `tests/doc-health/fixtures/modified-block-currency*/` — one fixture per finding class, the two regression fixtures reconstructing the historical true positives (#351's six clauses / two scenarios / one reverted line, and #329's one-of-eight scenario restatement), the retitle-and-gut red test, the tokenization fixture, the marker negatives, the two-writers case, the self-gate against this repository's own tree, and the structural pins on the advisory launch; `tests/doc-health/test_lifecycle_scan_set.py` — the twenty-second family classified as a non-reader of the lifecycle scan set. The MODIFIED block on `doc-health`'s "Deterministic check families" is part of this surface and is owed at realization, in the commit that registers the family — not in this proposal; the reason is measured in § Orchestrator Decisions D5. No change to the governed corpus, the lifecycle scan set, any existing family's behaviour or measurement basis, the report schema, the regression-diff rule, or any threshold.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-family-enumeration-check` and `add-duplicate-packet-check` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts and in no other line. The change therefore ships ACTIVE and archives only after the merge.
Status: ratified
Ratified: 2026-08-27 by Brett — in-session ratification, verbatim: "Ratify as-is". THE CITATION COVERS THE PACKET AS WRITTEN AT `06c7475a`, which is what was put to him and what he ratified. The five decisions in § Orchestrator Decisions were flagged for veto and were NOT VETOED at that ratification; they are not thereby affirmatively ruled, and the flags stay exactly where they were. Two questions the packet left open WERE ruled in the same round and are recorded as rulings rather than as decisions: § 7.3, two-writer ordering, verbatim "By declaration"; and § 7.5, this packet's own origin, verbatim "Record your admission now". No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-27`).
Proposed: 2026-08-27
Origin: openxFactory issues #357 (the validator gap), #329 (two active changes carrying lossy MODIFIED blocks) and #330 (the promotion-fidelity blind spot), all three filed by Brett on 2026-08-25; PR #358, the manual repair of the #351 instance; and `openspec/changes/add-family-enumeration-check/tasks.md` § 5.3, which recorded this half by name and declined to fold it in — "the scenario-completeness half, which is the half that actually destroyed text" and "NOT folded into this change: it is a different comparison against a different document pair".
---

# Proposal: add-modified-block-currency-check

## Standing

**Ratified in session by Brett on 2026-08-27, verbatim "Ratify as-is"**, on the
packet as written at `06c7475a`. The front-matter carries the citation in the
record-citing spelling, there being no approving OpenSpec change to name. The
five decisions in § Orchestrator Decisions were flagged for veto and were not
vetoed; that is not the same as being affirmatively ruled, and the flags stay.

**The #318 origin gap is closed for this packet, by ruling.** It was authored
and reviewed while unapproved, which is exactly the state issue #318 describes:
the `proposal-origin` family requires an `ad_hoc` origin to carry `approved_on`,
and until 2026-08-27 no approval existed to record. Asked whether to leave the
packet in that state or to record his admission, Brett chose "Record your
admission now", so `.openspec.yaml` names him as approver on 2026-08-27 in the
same shape `create-medxchart-overlay-boundary` uses. #318 itself stays open —
the taxonomy still has no origin kind meaning "proposed, not approved", and the
next packet drafted before approval will sit in the same gap. `tasks.md` § 7.5
records that.

## Why

**A `MODIFIED` requirement block that restates stale canon passes every gate in
this repository and deletes canon on archive.** `openspec validate --strict`
checks a delta's shape — the heading, the keyword on the first line, at least
one scenario — and never what promotion will do to the requirement being
replaced. `MODIFIED` replaces a requirement wholesale; it does not merge. So
whatever the block says is what canon says afterwards, and every clause and
scenario the block does not restate is deleted silently.

**It has happened four times in this repository in one week, and a human caught
it every time.**

| change | requirement | what the block was holding |
| --- | --- | --- |
| `add-doxchat-model-intake` (#351) | `ideation-dashboard` / doxBench model catalog and provider boundary | six body clauses, two scenarios, one reverted scenario line |
| `add-release-inventory-drift-check` (#329) | `doc-health` / Deterministic check families | 1 of 8 scenarios restated |
| `add-promotion-fidelity-check` (#329) | same | 1 of 8 |
| `add-duplicate-packet-check` (#329) | same | 1 of 8 |

**The class is a function of time, not of care.** `add-doxchat-model-intake`'s
block was written on 2026-08-21 against a pre-`02a71d6e` canon and was correct
when written. Canon moved; nothing re-read the block; four days later it was
holding a nine-item deletion with `validate --strict` green throughout. #357
states the gap in the sentence this change exists to retire: "a long-lived
active change that MODIFIES a requirement goes stale as canon moves".

**Counting does not see it.** The `add-release-inventory-drift-check` case was
found at its archive gate by a byte-for-byte per-requirement verification, and
it nearly escaped because the file-level scenario count did not move: that
change's own ADDED requirement brought seven scenarios and its MODIFIED block
was about to drop seven, so `doc-health/spec.md` read 98 → 98. Only
per-requirement accounting shows it — `Deterministic check families: 8 -> 1`.

**And the family whose whole job is delta-versus-spec fidelity is structurally
blind to it (#330).** `promotion-fidelity` compares an archived delta to the
promoted spec. After the archive act canon is the delta, so a block that
dropped seven scenarios and a canon now missing them agree perfectly: delta
scenarios 1, promoted 1, verdict AGREES, no finding. The direction that can see
the loss is a different document pair read at a different moment.

`add-family-enumeration-check` § 5.3 named this half and declined to fold it
in — correctly, and this change is the fix it named.

## What Changes

- **`document-lifecycle` gains the obligation.** One ADDED requirement stating
  that a MODIFIED block restates the requirement as canon currently states it,
  that currency is owed continuously for as long as the change is active rather
  than once at authoring, and that a deliberate deletion is declared by a
  reserved marker in the delta. #330 asks for exactly this ordering: the
  authoring convention stated before a checker enforces it.
- **`doc-health` gains the twenty-second check family.** One ADDED requirement
  defining the check: three comparison arms, same-kind exact matching, the
  normative unit derivation, the reserved marker and its two forms, the
  checkout basis, and the advisory launch.
- **No `## MODIFIED Requirements` block on "Deterministic check families" in
  this packet.** It is owed, and it is owed at realization rather than here.
  D5 below is the measurement that decided it.
- **`promotion-fidelity` is not extended, and `release-realization` is not
  touched or widened.** D1 and D4 give the reasons; both are canon-grounded.
- **The implementation lands in this change** on the precedent its sibling
  families set, and it is Speckit work sequenced by `tasks.md`.

## Impact

- **Affected specs**: `document-lifecycle` (ADDED), `doc-health` (ADDED here;
  MODIFIED at realization).
- **Affected code**: `scripts/doc_health/` (one new module, three one-line
  registrations), `tests/doc-health/`.
- **Predicted severity movement**, measured by a throwaway implementation of
  the matching rule **exactly as the delta writes it** — same-kind exact units,
  backtick-masked sentence split, scenario bullets compared across the whole
  block — run over all 23 MODIFIED requirements in this repository's active
  changes at `9be81a40`:

| arm | at this branch point | with § 2.1's block, at realization |
| --- | --- | --- |
| scenario-title completeness | **1** finding | **1** |
| carriage ledger | **14 units / 10 requirements** → 10 findings | **16 units / 11 requirements** → 11 findings |
| title resolution / two-writers | **0** | **0** — one two-writers pair, exactly one declaring |
| **movement** | **+1 `warning`, +10 `info`** | **+1 `warning`, +11 `info`, 0 `error`, 0 `critical`** |

  Ledger units split **10 body / 4 scenario-bullet** at the branch point. A run
  configured `--fail-on error` or `--fail-on critical` is unaffected by
  construction, and the canon-share headline, the per-stage census, the
  inventory and the catalog are untouched because the family reads neither the
  governed corpus nor the lifecycle scan set.

- **The one scenario-arm finding, named, because #329 asked for the live
  population.** `add-composed-view-authoring` MODIFIES `ideation-dashboard` /
  "Composed views are read-only with a repository jump" and does not restate
  canon's scenario `Gate verbs hide on a composed view`. On inspection it is a
  deliberate rename — the block carries `Tile-bound gate verbs hide on a
  composed view` with an amended body — so it is not a defect, and this
  proposal does not claim it is one. It is the case the reserved marker exists
  for, and the same change also drops one of that scenario's two bullets, which
  the ledger reports separately: the rename and the bullet loss are different
  facts and the arms keep them apart.
- **The ledger reproduced a human verification.** Against
  `add-doxchat-model-intake` the bullet arm isolates exactly one unit — canon's
  `**THEN** the selector MUST show exactly the available catalog entries and
  their data-handling badges`, replaced by a widened line — which is precisely
  the single-bullet residue PR #358's manual `canon ⊆ intake ⊆ B` verification
  reported after the repair. This holds only because matching is exact rather
  than substring: canon's bullet is a substring of the widened one, so a
  containment rule would report nothing here, which is why the delta forbids
  containment in normative text.
- **Measured effect on every other repository**: unknown until an aggregation
  run, and deliberately so. That is why the launch is advisory rather than a
  claim this proposal makes.

## What each arm would do to #351's nine items

The instance that produced #357 is the clearest statement of what this family
does and does not gate. Its nine items divide as follows.

| # | items | arm | at launch | after the flip D3 asks for |
| --- | --- | --- | --- | --- |
| 2 | scenarios `The menu offers a routing rule`, `A fourth provider verb is proposed` | scenario-title completeness | `warning` | **`error` — gated** |
| 6 | body clauses (three-member port surface; no fourth provider verb; the `auto` routing rule; the broker-lane credential clause; `thread file` in the leak list; the hosted-plane sentence) | carriage ledger | `info` | `info` — no flip proposed here |
| 1 | the reverted scenario line ("every loaded editor" → "the Outline and Document editors") | carriage ledger | `info` | `info` — no flip proposed here |

**So two of the nine would be gated and seven reported.** That is the honest
scope of this change and it is stated here rather than left to be inferred: the
gate catches deletion of a titled scenario, and everything at clause and bullet
granularity is reported for a human to read at authoring time. Whether the
ledger should ever gate is a later ruling, not a decision this packet takes —
see D3.

## Orchestrator Decisions — FLAGGED FOR VETO

The three issues establish the defect class and #357 proposes a check. The five
decisions below were taken by the authoring session under standing patterns and
are named so they can be reversed on a word.

**NONE OF THE FIVE WAS VETOED AT THE RATIFICATION OF 2026-08-27, AND NONE WAS
AFFIRMATIVELY RULED.** Brett ratified the packet as written, which put these
decisions on `main` without putting a ruling behind any of them. The flags
therefore stay exactly where they were: reverting any one of them is an edit to
this change rather than a new one, and no later reader should cite this
ratification as having decided them.

**D1 — One new family, and `promotion-fidelity` is not extended.**
*(Not vetoed at ratification 2026-08-27.)* #330 offers
two shapes: give that family a promoted→promoted arm at archive (its shape 1),
or require MODIFIED blocks to be scenario-complete and check them before
archive (its shape 2). This change takes shape 2, in a new family, on three
canon-grounded reasons. First, canon has already ruled the general question:
"One ruling, one discharge, across archived packets" argues in its own text
that a different comparison is a different family — "the comparison that can
see the class is between the archived deltas themselves, which is why this is a
separate family rather than a wider reading of that one". Second, shape 1 needs
the promoted spec's state at the archive commit's parent, which is a third
measurement basis, and "The promotion fidelity measurement basis is declared"
requires a run's report to state which of its two bases that family measured,
on every run; a third basis would make that line untrue of half its findings.
Third, every part of `promotion-fidelity` is archived-path-shaped — the
latest-writer rule, the ratification exemption, the disposition key — and a
family whose findings all name archived paths cannot report against an active
change's delta, which is where the remedy for this class lives. What is given
up is named: shape 1's post-archive safety net is not built here, so **#330
stays open**, with an owner and a trigger in `tasks.md` § 7.1.

**D2 — Same-kind exact units; three arms; a reserved marker for deletion.**
*(Not vetoed at ratification 2026-08-27.)* A
canon unit is carried only by a block unit of the SAME KIND — a body unit by a
body unit, a scenario title by a scenario title, a scenario bullet by a
scenario bullet — matched in full after whitespace normalization, which is the
minimum that survives re-wrapping. **Containment is forbidden in normative
text**: a block bullet that contains canon's bullet has replaced it, which is
how #351's widened line entered, and a containment rule reports nothing there.
Similarity is forbidden too: it would accept a clause whose meaning had been
reversed, also on this record. Unit derivation is normative, not left to an
implementation — backticked spans are masked before any sentence split, bullets
are units, and a dated bold note is one undivided unit. Scenario bullets are
compared across ALL bullets of the block rather than scenario by scenario, so a
retitle cannot carry its bullets away with it. And "named as removed" is a NEW
reserved marker read by form, in two spellings — `Removed from canon by …` and
``Merged into `<destination>` by …`` — naming units as CommonMark code spans
(with a longer fence where a unit itself contains backticks), suppressing only
units it names AND that are actually absent, and never itself becoming a
carriage unit. The corpus's existing dated-note convention is deliberately
NOT reused: every such note today records a caught near-miss and a restoration,
one of them naming seven scenario titles in backticks as restored, so a
prose-reading rule would read a faithful restatement of `doc-health`'s own
"Deterministic check families" as declaring seven deletions — on the very
requirement #329 is about.

**D3 — Advisory at launch, and the flip is asked for one arm.**
*(Not vetoed at ratification 2026-08-27.)* Every finding
is `warning` (scenario-title, title-resolution) or `info` (carriage ledger),
and the family is deliberately absent from `FAMILY_RESOLUTION` so a resolved
finding cannot become an `error` through the uncited-resolution rule — the
both-halves discipline three families have now launched under. The flip gate:
raising the scenario-title arm to `error` and adding the `contested`
classification is one later decision taken together by ruling, and follows the
discharge of the standing population — here exactly one finding, on
`add-composed-view-authoring`, so the gate is unusually cheap to reach. **No
flip is proposed for the carriage ledger in this packet.** Its population is
standing by construction: every legitimate MODIFIED block edits something. The
consequence is stated plainly above — seven of #351's nine items stay advisory
under this packet — and a later flip remains available as a ruling like any
other rather than being ruled out here.

**D4 — The two-writers rule reuses `release-realization` and widens nothing.**
*(Not vetoed at ratification 2026-08-27.)*
That capability's "Ordered deltas and branch vocabulary" requires that "a
proposal modifying a requirement already modified by an active ratified change
references that change and declares its deltas relative to that change's
outcome". The word `ratified` is carried verbatim: this change adds no
obligation on unratified packets, and adds only the consequence for currency —
a block declared relative to another change's outcome is measured against that
outcome and must carry its additions. **RULED 2026-08-27 by Brett, verbatim
"By declaration": the declaration IS the ordering.** The change that writes
"relative to <sibling>" is the later writer, and the check verifies only that
exactly one of two active ratified writers declares and that the declaring
block carries the other's additions. No date arithmetic, no folder name, no
`created:` field — the packet's earlier reading, which resolved "later" by
`.openspec.yaml` `created:`, is withdrawn. Neither writer declaring is the
reported asymmetry; both declaring is reported too. Separately and NOT as a widening of that
obligation, the family's three arms READ every active change regardless of
lifecycle standing, because they are advisory and a `draft` block is as capable
of restating stale canon as a ratified one. The reference is read mechanically:
the earlier change's id occurring as a whole token in the later change's own
`proposal.md`, the whole-token match `duplicate-packet` already uses. Measured:
seven (capability, requirement) pairs are written by two active changes today,
in **7 of 7** the modifying proposal already names the sibling, all seven are
the MODIFIED-over-a-sibling's-ADDED shape, and zero titles resolve to nothing —
so this arm emits nothing today, and compliance was measured rather than
assumed.

**D5 — The enumeration MODIFIED block is owed at realization, and writing it
here reds a standing gate. This was proven, not reasoned.** *(Not vetoed at
ratification 2026-08-27.)* Canon still
enumerates: `openspec/specs/doc-health/spec.md` reads "twenty check families"
in prose, because `add-family-enumeration-check` is active — its code has
landed and its delta is not promoted. So a MODIFIED block is owed. But that
change's own rule requires an active delta's restatement to be "consistent with
the registry in its own tree", and a proposal that registers no family would
state a family the registry does not carry. The block was written — carried
forward from `add-family-enumeration-check`'s outcome per D4, twenty-one →
twenty-two, all eight scenarios restated, per-requirement count 8 → 8 — and the
check was run against it:

```
findings: 3
 - this active delta's restatement names check family 'modified-block currency',
   which resolves to 'modified-block-currency' and is not a registered family
 - this active delta's restatement says 'twenty-two' check families, but 21 are
   registered — expected 'twenty-one'
 - this active delta's restatement says 'Four' of 'twenty-two', but 21 families
   are registered

tests/doc-health/test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves
FAILED
```

That test is a standing gate on `main`. The block was therefore withdrawn from
this packet and moved to `tasks.md` § 2.1, to be written in the same commit
that registers the family, relative to `add-family-enumeration-check`'s
outcome, with the 8 → 8 count recorded at that gate. This proposal does not
commit the defect it targets: it carries no MODIFIED block at all, so it
deletes nothing, and the reason it carries none is a measurement rather than an
omission. Two consequences are carried forward rather than hidden: § 2.1's
block adds one carriage-ledger finding against this change's own delta (the
+11 column above), and it creates the corpus's first two-writers instance
between two ACTIVE changes. That case had no ordering rule when the packet was
written and now has one: Brett ruled "By declaration" on 2026-08-27, and this
change's own proposal declares itself relative to `add-family-enumeration-check`
while that change names nothing — exactly one declaration, so the arm reads
zero. Measured under the ruled rule: 0 two-MODIFIED pairs at the branch point,
1 pair with § 2.1 present, **0 findings either way**.

## What this proposal does NOT claim

It does not claim the findings it predicts are defects. All of them are
deliberate edits or one deliberate rename; the family's value at launch is that
they become visible and declared.

It does not claim to close #330 in both of that issue's shapes. The pre-archive
gate is built and the post-archive safety net is not; #330 stays open with an
owner.

It does not claim the carriage ledger can distinguish a rewording from stale
text. It cannot, by construction, and the alternatives that could — containment
or similarity — are both forbidden in the delta for reasons that are on the
record.

It does not claim to have measured the domain factories. This change's evidence
is openxFactory's own active changes and a fixture corpus.

And it does not claim that a currency check makes a MODIFIED block correct. It
verifies that a block carries what canon carries; whether what the block adds
is wise is a reviewer's question, and no family answers it.
