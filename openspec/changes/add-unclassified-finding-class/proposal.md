---
code_surface: openxFactory (`scripts/doc_health/modified_block_currency.py` — the class registry gains a FIFTH `FindingClass` for the drift finding and `_CLASS_PATTERNS` the anchored pattern that places it, and `fam_modified_block_currency` gains the emit: count the findings `classify` returns `UNCLASSIFIED` for, and where that count is nonzero append ONE `warning` finding carrying the count, the first unplaced rule text verbatim, that finding's repo and delta path, and the new action line. `classify`, `class_counts` and `class_summary` keep their signatures and their no-context discipline, and the residual row keeps rendering; `tests/doc-health/test_modified_block_currency_reporting.py` — the class-registry pin, the rule-shape-per-class pin and the block-length pin all move by one, and the four scenarios of this delta arrive as new tests including the anchoring case where the quoted rule text itself begins like an arm's. NO other family's behaviour, NO workflow file, NO change to `Finding`, to `report.render`, to the ranked-plan or finding grammars, to `families.FAMILY_SUMMARIES`, to `FAMILY_RESOLUTION`, to the governed corpus, to the lifecycle scan set, or to any threshold. NO `## MODIFIED Requirements` block on any promoted requirement — see § Orchestrator Decisions D1, which is the decision this packet's shape turns on.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-modified-block-currency-check` and `add-family-enumeration-check` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts — zero — and in no other line. The change therefore ships ACTIVE and archives only after the merge.
Status: ratified
Ratified: 2026-08-27 by Brett — in-session commissioning, verbatim: "Amend now". The citation covers the DECISION TO BUILD THIS AMENDMENT and nothing else; the three design decisions in § Orchestrator Decisions below were taken by the authoring session under standing patterns, are NOT covered by this citation, and are flagged there for veto. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-27`).
Proposed: 2026-08-27
Origin: the F4 report block landed by `add-modified-block-currency-check` § 5.1 (PR #433, squash `4def2274`), read in session on 2026-08-27. Its residual row — `scripts/doc_health/modified_block_currency.py`'s `_UNCLASSIFIED_LINE`, pinned by `test_a_finding_the_map_cannot_place_is_counted_and_named` — is the only report content this capability produces that is not a finding and cannot become work. Put to Brett as a choice between leaving it as a text row and making a nonzero count emit one `warning`, he answered "Amend now".
---

# Proposal: add-unclassified-finding-class

## Why

**The modified-block-currency family already detects that its own class map has
drifted, and then tells nobody who can act on it.** `classify` is fail-closed by
design: a rule text no pattern matches is NOT absorbed into a neighbouring class,
it returns `UNCLASSIFIED`, and `class_summary` renders a named residual row —

```
- unclassified: 2 — findings this family emitted that its own class map does not
  place; the map has drifted from the arms and the counts above are short by this many
```

— which is the honest thing for a tally to say about itself, and is where the
mechanism stops. That line is prose inside a family's report section. It has no
severity, so no `--fail-on` configuration reaches it. It is not a finding, so
`doc-health`'s own "Health report contract" — "every finding MUST appear in the
ranked plan as an actionable item, so report output feeds the ideation pipeline's
input" — does not reach it either. A session working a report's ranked plan, the
workflow this capability builds reports for, never sees it.

**And the thing it reports is a defect in this capability's own tooling.** The
residual is nonzero only where the family's arms and the map that describes them
disagree — the exact failure mode `add-modified-block-currency-check` § 5.1 built
the class block to prevent, which is "a wrong number on the one line § 5.1 exists
so a reader can trust without counting". The family emits a finding for a MODIFIED
block that drifted from canon by one clause, and stays silent when its own rule
text drifts from its own map.

**Nothing else in the corpus reports it.** The class map is a module constant
compared against rule texts constructed in the same module, so no other family
reads either side; `test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class`
and its real-tree sibling hold the line in CI, which is the right place for a
constant-versus-constant invariant — but a nightly aggregation run over eight
repositories is not CI, and it is where a rule text that only drifts on a corpus
nobody has a fixture for would first appear.

**It reads zero today, and that is the argument for building it now rather than
later.** Measured on this tree at `b5fb03f3`: `unclassified: 0`, the residual row
absent from the block. The population this change would report is empty, so the
amendment costs nothing to land and the standing state it pins is the one every
reader currently assumes.

## What Changes

- **`doc-health` gains ONE ADDED requirement**, "A modified-block-currency finding
  its own class map cannot place is itself a finding": a nonzero residual emits
  exactly one `warning` per run naming the count and the first unplaced rule text
  verbatim, with the action line "extend the class map, or fix the rule text
  drift"; the finding is itself placed by the map into a FIFTH class so it is
  never counted by the residual it reports; the pattern that places it is anchored
  at the start of the rule text, because the finding quotes a rule text that may
  itself begin in the shape of an arm; the residual row keeps rendering; the band
  is `warning` and the family stays absent from `FAMILY_RESOLUTION`.
- **NO `## MODIFIED Requirements` block, on any promoted requirement.** Canon does
  not enumerate this family's finding classes — measured, not assumed; D1 carries
  the measurement.
- **No new check family.** The finding is emitted by the twenty-second family,
  under its id, in its section. The "Deterministic check families" enumeration and
  its three numerals are untouched and unrestated, following
  "A declared unrecoverable pin loss is discharged by a superseding record" in the
  same capability, which declines the same restatement for the same reason.
- **The implementation lands in this change**, as ONE Speckit feature sequenced by
  `tasks.md`, on the precedent its sibling families set.

## Impact

- **Affected specs**: `doc-health` (ADDED only).
- **Affected code**: `scripts/doc_health/modified_block_currency.py`,
  `tests/doc-health/test_modified_block_currency_reporting.py`.
- **Predicted severity movement: ZERO, in every band.** Measured on this tree at
  `b5fb03f3` with `python3 scripts/doc-health.py --single-repo . --family
  modified-block-currency`: **1 `warning`, 7 `info`**, class counts
  `scenario-title completeness 1 / carriage ledger 7 / title resolution and
  ordering 0 / marker defects 0`, and **`unclassified` 0** — the residual row does
  not render. The finding this change adds fires only where that count is nonzero,
  so the run after realization emits the same eight findings, and the class block
  gains one row reading `0`. The canon-share headline, the per-stage census, the
  inventory and the catalog are untouched, because the family reads neither the
  governed corpus nor the lifecycle scan set.
- **Predicted movement from this PACKET's own delta: ZERO.** This packet carries an
  ADDED block and no MODIFIED block, and the family reads
  `## MODIFIED Requirements` blocks only. Verified by running the family over this
  tree with the packet present: **1 `warning`, 7 `info`, `unclassified` 0** —
  byte-identical to the baseline above, no finding naming any path under
  `openspec/changes/add-unclassified-finding-class/`.
- **Measured effect on every other repository**: unknown until an aggregation run,
  and by construction it is zero unless a rule text has drifted there — which is
  precisely the case this change exists to surface rather than to predict.

## Orchestrator Decisions — FLAGGED FOR VETO

Brett commissioned the amendment. The three decisions below were taken by the
authoring session under standing patterns and are named so they can be reversed
on a word.

**D1 — ADDED-ONLY. No MODIFIED block on "Currency of an active change's MODIFIED
requirement blocks", and this was measured rather than preferred.** The obvious
shape for "a fifth finding class" is a MODIFIED block on the requirement that
defines the family, restating all 14 of its scenarios and its ~90 lines of body
byte-for-byte with the addition. It is not owed, because **canon does not
enumerate the classes**. The promoted requirement says the family "SHALL implement
three comparison arms over one document pair, and SHALL report them as distinct
finding classes", and then names the three ARMS. It never says how many classes
there are, never names the class map, `classify`, `class_counts` or the residual
row, and never mentions `unclassified`. Grepped, not recalled: `class map`,
`finding classes`, `residual` and `class summary` occur in
`openspec/specs/doc-health/spec.md` at exactly one line between them — 1530, the
arms sentence — and `unclassified` occurs there only at 1001 and 1153, describing
two OTHER families' resolution classification. The four-classes-to-three-arms gap
is stated in the MODULE (`CLASSES`, and the comment "FOUR ENTRIES FOR FIVE RULE
SHAPES") and nowhere in canon.

The one sentence a strict reader might hold against this is in the advisory
paragraph: "Every finding carries `warning` severity for the scenario-completeness
and title-resolution arms and `info` for the carriage ledger". That sentence maps
ARMS to bands, and it is ALREADY not exhaustive over the family's emitted
findings: **marker defects are not an arm**, canon requires them reported ("A
marker naming a unit the block still carries declares nothing and SHALL itself be
reported", plus its own scenario) and states no band for them, and the module gives
them `info`. This change adds a second non-arm finding and gives it `warning` — one
of the two bands that sentence already names — so the sentence stays true word for
word, and its operative claim, that no `--fail-on` configuration reds on the
family, is unchanged because `warning` is what the gate-bearing arm already
carries.

So the cheapest honest shape is an ADDED requirement that references the currency
requirement by name and restates none of it. It is also the shape this capability
has already argued for in canon: "A declared unrecoverable pin loss is discharged
by a superseding record" declines to open a MODIFIED block on a large requirement
in exactly these words — "a `MODIFIED` block over a requirement every new family
must restate in full is exactly the hazard this capability now carries a family to
police". Writing one here to add two sentences would put 14 restated scenarios and
~90 restated lines at risk of the defect the family exists to catch, in order to
say something canon does not currently say. **The cost of the veto is named**: if
D1 is vetoed, this packet grows a MODIFIED block restating that requirement in
full, the carriage ledger will report this packet's own delta for whatever it
rewords, and the predicted movement above stops being zero.

**D2 — The new finding is a fifth CLASS, not an unclassified finding and not a
report-block line.** Three shapes were available. (a) Emit the finding and leave it
unplaced: it would then be counted by the residual it reports, so the count would
name itself and the tally still would not sum — rejected as incoherent. (b) Give
the residual row a severity: rejected because
`test_the_block_is_not_a_finding_and_cannot_become_one` pins, through
`report.parse_previous`, that the class block never re-enters the machinery that
reads findings back, and that pin is worth more than the shortcut. (c) A fifth
`FindingClass` with an anchored pattern, which is what this delta requires: the
map places its own drift finding, the residual keeps counting only the arms'
unplaced findings, and the counts sum. The anchoring is not decoration — the
finding QUOTES an unrecognized rule text, and an unanchored probe would file it
under whichever class the quotation resembles, which is the exact misfiling
`_BLOCK_HEAD` was measured into existence to prevent.

**D3 — One finding per RUN, carrying the first unplaced finding's repo and path.**
The alternative is one per repository. The class map is a module constant compiled
once per process, so the drift is one defect with one remedy — one edit to the map
— and a per-repository emit would put that one remedy into an aggregation run's
ranked plan once for every repository in scope. `family_enumeration` records the
same reading for its missing-direction invariant: "a runtime finding would fire
identically on every run for every repository and say nothing a reader of a report
could act on". The repo and path carried are the FIRST unplaced finding's, in the
family's own sort order, so the ordering is deterministic and a reader has a
document to open. What this gives up is named: on an aggregation run the finding
names one example, and a second repository's differently-drifted rule text is
counted but not quoted.

## What this proposal does NOT claim

It does not claim the class map has drifted. It reads zero on this tree today, and
the whole change is a pin on that state plus a route out of it if it ever moves.

It does not claim the residual row was wrong. The row is honest and it stays; what
it could not do is become work, and that is all this change adds.

It does not claim to make the family enforcing. The band is `warning`, the family
stays absent from `FAMILY_RESOLUTION`, and § 7.2 of `add-modified-block-currency-check`
— the flip of the scenario-title arm to `error` — is untouched and still owed.

It does not claim to have measured the domain factories. This change's evidence is
openxFactory's own tree and the fixture corpus.
