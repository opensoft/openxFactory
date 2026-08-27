---
code_surface: openxFactory (`scripts/doc_health/modified_block_currency.py` — a new module owning the twenty-second deterministic family: the ACTIVE-change delta reader, the promoted-requirement reader, the whitespace normalization and its unit split (body sentences, scenario titles, scenario bullets), the three comparison arms, the two-writers resolution against an active sibling's outcome, the in-delta deletion-declaration parser, and the disposition read; `scripts/doc_health/families.py` — one import, one registration line in `FAMILIES`, one note recording why the family is deliberately absent from `FAMILY_RESOLUTION`, and the module docstring's owner list; `scripts/doc_health/__init__.py` — one entry in `FAMILY_IDS` so the family gets its own report section; `tests/doc-health/test_modified_block_currency.py` plus `tests/doc-health/fixtures/modified-block-currency*/` — one fixture per finding class, the two REGRESSION fixtures reconstructing the historical true positives (#351's six clauses / two scenarios / one reverted line, and #329's one-of-eight scenario restatement), the declared-deletion negative, the two-writers negative, the pending-sibling negative, the self-gate assertion against this repository's own tree, and the structural pins on the advisory launch; `tests/doc-health/test_lifecycle_scan_set.py` — the twenty-second family classified as a non-reader of the lifecycle scan set. THE MODIFIED BLOCK ON `doc-health`'s "Deterministic check families" IS PART OF THIS SURFACE AND IS OWED AT REALIZATION, IN THE COMMIT THAT REGISTERS THE FAMILY — not in this proposal; the reason is measured in § Orchestrator Decisions D5. NO change to the governed corpus, the lifecycle scan set, any existing family's behaviour or measurement basis, the report schema, the regression-diff rule, or any threshold.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-family-enumeration-check` and `add-duplicate-packet-check` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts and in no other line. The change therefore ships ACTIVE and archives only after the merge.
Status: draft
Proposed: 2026-08-27
Origin: openxFactory issues #357 (the validator gap), #329 (two active changes carrying lossy MODIFIED blocks) and #330 (the promotion-fidelity blind spot), all three filed by Brett on 2026-08-25; PR #358, the manual repair of the #351 instance; and `openspec/changes/add-family-enumeration-check/tasks.md` § 5.3, which recorded this half by name and declined to fold it in — "the scenario-completeness half, which is the half that actually destroyed text ... NOT folded into this change: it is a different comparison against a different document pair".
---

# Proposal: add-modified-block-currency-check

## THIS IS A PROPOSAL. IT IS NOT RATIFIED.

`Status: draft` is the corpus's sanctioned spelling for a packet that has been
authored and not approved, and it is used here deliberately rather than for
want of a better one. The taxonomy in `docs/document-lifecycle.md` maps `draft`
to the lifecycle state "proposed (or awaiting proposal) — normative intent, not
yet ratified", and the promoted lifecycle rule requires a ratification citation
only for `Status: ratified`, so this packet owes none and carries none. No
`Ratified:` line appears anywhere in it.

Issue #318 — "a drafted-but-unapproved change packet has no lawful origin
shape" — is OPEN, and this packet sits in exactly the state it describes: the
`proposal-origin` family requires an `ad_hoc` origin to carry `approved_on`,
and no approval of this content exists to date. This packet resolves that the
way `create-medxchart-overlay-boundary` and `qualify-avatar-live-voice` resolve
it, which is the only shape the corpus currently sanctions: the `.openspec.yaml`
origin records ADMISSION OF THE DEFECT CLASS INTO THE PROPOSAL QUEUE and says
so in those words. Brett filed all three issues on 2026-08-25 and #357 proposes
this check in its own sentences; that filing is the approval recorded, and it is
recorded as an admission and NOT as a ratification of this packet's content or
of the five decisions in § Orchestrator Decisions. Nothing here should be read
as an approval that has not happened.

## Why

**A `MODIFIED` requirement block that restates stale canon passes every gate in
this repository and deletes canon on archive.** `openspec validate --strict`
checks a delta's SHAPE — the heading, the keyword on the first line, at least
one scenario — and never what promotion will do to the requirement being
replaced. `MODIFIED` REPLACES a requirement wholesale; it does not merge. So
whatever the block says is what canon says afterwards, and every clause and
scenario the block does not restate is deleted silently.

**It has happened four times in this repository in one week, and a human caught
it every time.**

| change | requirement | what the block was holding |
| --- | --- | --- |
| `add-doxchat-model-intake` (#351) | `ideation-dashboard` / doxBench model catalog and provider boundary | six body clauses, two scenarios, one reverted scenario line |
| `add-release-inventory-drift-check` (#329) | `doc-health` / Deterministic check families | 1 of 8 scenarios restated |
| `add-promotion-fidelity-check` (#329) | same | 1 of 8 restated |
| `add-duplicate-packet-check` (#329) | same | 1 of 8 restated |

**The class is a function of TIME, not of care.** `add-doxchat-model-intake`'s
block was written on 2026-08-21 against a pre-`02a71d6e` canon and was correct
when written. Canon moved; nothing re-read the block; four days later it was
holding a nine-item deletion with `validate --strict` green throughout. #357
states the gap in the sentence this change exists to retire: "a long-lived
active change that MODIFIES a requirement goes stale as canon moves".

**Counting does not see it.** The `add-release-inventory-drift-check` case was
found at its archive gate by a byte-for-byte per-requirement verification, and
it nearly escaped because the FILE-LEVEL scenario count did not move: that
change's own ADDED requirement brought seven scenarios and its MODIFIED block
was about to drop seven, so `doc-health/spec.md` read 98 → 98. Only
per-requirement accounting shows it — `Deterministic check families: 8 -> 1`.

**And the family whose whole job is delta-versus-spec fidelity is structurally
blind to it (#330).** `promotion-fidelity` compares an ARCHIVED delta to the
promoted spec. After the archive act canon IS the delta, so a block that
dropped seven scenarios and a canon that now lacks them agree perfectly: delta
scenarios 1, promoted 1, verdict AGREES, no finding. The direction that can see
the loss is a different document pair read at a different moment.

`add-family-enumeration-check` § 5.3 named this half and declined to fold it
in — correctly, and this change is the fix it named.

## What Changes

- **`document-lifecycle` gains the obligation.** ONE ADDED requirement stating
  that a MODIFIED block restates the requirement as canon currently states it,
  that currency is owed continuously for as long as the change is active rather
  than once at authoring, and that a deliberate deletion is declared in the
  delta itself. #330 says this explicitly — the authoring convention must be
  stated before a checker enforces it — and the requirement is the sibling of
  that capability's existing "Ratified spec deltas reach the promoted
  specification" and "A ruling is discharged once".
- **`doc-health` gains the twenty-second check family.** ONE ADDED requirement
  defining the check: three comparison arms (scenario-title completeness, the
  carriage ledger, title resolution and the two-writers rule), verbatim matching
  after whitespace normalization and nothing looser, the in-delta deletion
  declaration, the checkout basis, and the advisory launch.
- **NO `## MODIFIED Requirements` block on "Deterministic check families" in
  this packet.** It is owed, and it is owed at realization rather than here.
  D5 below is the measurement that decided it.
- **`promotion-fidelity` is NOT extended, and `release-realization` is NOT
  touched.** D1 and D4 give the reasons; both are canon-grounded rather than
  matters of taste.
- **The implementation lands in this change** on the precedent its four sibling
  families set, and it is Speckit work sequenced by `tasks.md`, never
  `/opsx:apply`.

## Impact

- **Affected specs**: `document-lifecycle` (ADDED), `doc-health` (ADDED here;
  MODIFIED at realization).
- **Affected code**: `scripts/doc_health/` (one new module, three one-line
  registrations), `tests/doc-health/`.
- **Predicted severity movement on this repository at launch** — measured by a
  throwaway implementation of the proposed matching rule run across every
  active change in this repository before this proposal was written, at
  `9be81a40`:

| arm | findings | severity |
| --- | --- | --- |
| scenario-title completeness | **1** | +1 `warning` |
| carriage ledger | **13 units across 10 requirements**, reported as 10 findings | +10 `info` |
| title resolution / two-writers | **0** | — |
| **total** | **11 findings** | **+1 warning, +10 info, 0 error, 0 critical** |

  A run configured `--fail-on error` or `--fail-on critical` is unaffected by
  construction. The canon-share headline, the per-stage census, the inventory
  and the catalog are untouched because the family reads neither the governed
  corpus nor the lifecycle scan set.

- **The one scenario-arm finding, named, because #329 asked for exactly this.**
  `add-composed-view-authoring` MODIFIES `ideation-dashboard` / "Composed views
  are read-only with a repository jump" and does not restate canon's scenario
  `Gate verbs hide on a composed view`. On inspection it is a deliberate RENAME
  — the block carries `Tile-bound gate verbs hide on a composed view` with an
  amended body — so it is not a defect, and **this proposal does not claim it
  is one.** It is the exact case the in-delta declaration exists for, and the
  remedy is one sentence in the block, not a code change. The two changes #329
  named have both since been corrected by their own sessions; this is the third
  instance of the class, and it was invisible until the rule was written down.
- **The carriage ledger's 13 units are all deliberate in-place edits**, and one
  of them is load-bearing evidence: against `add-doxchat-model-intake` the arm
  isolates exactly ONE scenario bullet — the widened "browser loads model
  choices" line — which is precisely the single-line residue PR #358's manual
  `canon ⊆ intake ⊆ B` verification reported after the repair. The mechanical
  arm reproduced a human verification's result on a real case.
- **Measured effect on every other repository**: unknown until an aggregation
  run, and deliberately so. That is the reason the launch is advisory rather
  than a claim this proposal makes.

## Orchestrator Decisions — FLAGGED FOR VETO

No ruling covers any of this. The three issues establish the DEFECT CLASS and
propose a check; the five decisions below were taken by the authoring session
under standing patterns and are named here so they can be reversed on a word.

**D1 — ONE new family, and `promotion-fidelity` is not extended.** #330 offers
two shapes: give that family a promoted→promoted arm at archive (its shape 1),
or require MODIFIED blocks to be scenario-complete and check them before
archive (its shape 2). This change takes shape 2, in a new family, on three
canon-grounded reasons. First, canon has already ruled the general question:
"One ruling, one discharge" argues in its own text that a different COMPARISON
is a different family — "the comparison that can see the class is between the
archived deltas themselves, which is why this is a separate family rather than
a wider reading of that one". This is the same argument with the same shape.
Second, shape 1 needs the promoted spec's state at the ARCHIVE COMMIT'S PARENT,
which is a third measurement basis, and "The promotion fidelity measurement
basis is declared" requires a run's report to state which of its TWO bases that
family measured, on every run; a third basis inside that family would make its
one declared basis line untrue of half its findings. Third, every part of
`promotion-fidelity` is archived-path-shaped — the latest-writer rule, the
ratification exemption, the disposition key — and a family whose findings all
name archived paths cannot report against an active change's delta, which is
where the remedy for this class lives. **What is given up is named**: shape 1's
post-archive safety net is not built here, so a lossy block authored anyway and
archived anyway is still not detected after the fact. It is an open box in
`tasks.md` § 5, with the reason, rather than folded in silently.

**D2 — Verbatim after whitespace normalization; three arms; the declaration
goes in the delta.** Matching is character-for-character once runs of
whitespace collapse to one space — the minimum that survives re-wrapping, which
a real block does constantly (`add-family-enumeration-check` re-wrapped the
enumeration paragraph to change one word). Nothing looser: a similarity rule
would accept a clause whose meaning had been reversed, and reversal is on this
class's record. The consequence is that the family cannot tell a deliberate
rewording from stale text, which is why the arms are split rather than summed —
the SCENARIO-TITLE arm compares short titled strings and is nearly
false-positive-free (measured: 1 finding across the whole active corpus), and
the CARRIAGE LEDGER compares prose and is a reviewer's list rather than a
verdict (measured: 13 units, all deliberate edits). "Explicitly named as
removed" is a dated bold note inside the MODIFIED block naming each deleted
scenario by exact title and quoting each deleted unit; that is not a new
marker but an existing convention made machine-read — canon's own
"Deterministic check families" already carries such a note naming its seven
lost scenarios verbatim in backticks. `health/dispositions.yaml` is the
fallback for a ratified delta that cannot be re-authored.

**D3 — Advisory at launch, and the flip is asked for ONE arm only.** Every
finding is `warning` (scenario-title, title-resolution) or `info` (carriage
ledger), and the family is deliberately absent from `FAMILY_RESOLUTION` so a
resolved finding cannot become an `error` through the uncited-resolution rule —
the same both-halves discipline the last four families launched under. The flip
gate: raising the SCENARIO-TITLE arm to `error` and adding the `contested`
classification is ONE later decision taken together by ruling, and follows the
discharge of the standing population — which here is exactly one finding, on
`add-composed-view-authoring`, so the gate is unusually cheap to reach. **No
flip is proposed for the carriage ledger, ever.** Its population is standing by
construction: every legitimate MODIFIED block edits something. Saying that out
loud is what stops a permanently yellow row from teaching readers to skip the
section.

**D4 — The two-writers rule REUSES `release-realization`'s spelling and adds no
second one.** That capability's "Ordered deltas and branch vocabulary" already
requires that "a proposal modifying a requirement already modified by an active
ratified change references that change and declares its deltas relative to that
change's outcome". This change writes no competing rule; it adds only the
consequence for currency — a block declared relative to another change's
outcome is measured against THAT outcome, and carries the earlier change's
additions. Measured: seven (capability, requirement) pairs are written by two
active changes today, and in **7 of 7** the modifying change's proposal already
names the sibling. All seven are the MODIFIED-over-a-sibling's-ADDED shape, so
zero titles resolve to nothing. **This arm emits 0 findings at launch**, and
compliance was measured rather than assumed.

**D5 — The enumeration MODIFIED block is owed AT REALIZATION, and writing it
here would red a standing gate. This was proven, not reasoned.** Canon still
enumerates: `openspec/specs/doc-health/spec.md` reads "twenty check families"
in prose, because `add-family-enumeration-check` is ACTIVE — its code has
landed and its delta has not been promoted. So a MODIFIED block IS owed. But
that change's own ratified rule requires an active delta's restatement to be
"consistent with the registry in its own tree", and a proposal that registers
no family would state a family the registry does not carry. The authoring
session wrote the block — the full current requirement carried forward from
`add-family-enumeration-check`'s outcome, twenty-one → twenty-two, all EIGHT
scenarios restated, per-requirement count 8 → 8 — and ran the check against it:

```
findings: 3
 - this active delta's restatement names check family 'modified-block currency',
   which resolves to 'modified-block-currency' and is not a registered family
 - this active delta's restatement says 'twenty-two' check families, but 21 are
   registered — expected 'twenty-one'
 - this active delta's restatement says 'Four' of 'twenty-two', but 21 families
   are registered
```

```
tests/doc-health/test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves FAILED
```

That test is a standing gate on `main`. The block was therefore withdrawn from
this packet and moved to `tasks.md` § 2 as the FIRST task of realization, to be
written in the same commit that registers the family, relative to
`add-family-enumeration-check`'s outcome, with the 8 → 8 per-requirement count
recorded at that gate. **This proposal does not commit the defect it targets:**
it carries no MODIFIED block at all, so it deletes nothing, and the reason it
carries none is a measurement rather than an omission. The ordering dependency
on `add-family-enumeration-check` is recorded here the way that change recorded
its own on `add-promotion-fidelity-check` — named, not papered over.

## What this proposal does NOT claim

It does not claim the eleven findings it predicts against this repository are
defects. All eleven are deliberate edits or one deliberate rename; the family's
value at launch is that they become VISIBLE and DECLARED, not that they are
wrong.

It does not claim to close #330 in both of that issue's shapes. The pre-archive
gate is built and the post-archive safety net is not; the reasoning is D1 and
the box is `tasks.md` § 5.

It does not claim the carriage ledger can distinguish a rewording from stale
text. It cannot, by construction, and the alternative that could — a similarity
rule — is the one this corpus has already ruled against.

It does not claim to have measured the domain factories. This change's evidence
is openxFactory's own active changes and a fixture corpus; what the pinned
domains' branches will say is the reason the launch is advisory.

And it does not claim that a currency check makes a MODIFIED block correct. It
verifies that a block carries what canon carries; whether what the block ADDS
is wise is a reviewer's question, and no family answers it.
