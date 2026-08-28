---
code_surface: openxFactory (`scripts/doc_health/modified_block_currency.py` — a FOURTH severity constant `_DRIFT_SEVERITY = WARNING` (named apart so § 7.2's flip of `_LAUNCH_SEVERITY` cannot drag it, which is the module's own stated reason for `_RESOLUTION_SEVERITY` and `_LEDGER_SEVERITY`) and a `_DRIFT_ACTION`; a FIFTH `FindingClass` in `CLASSES`, id `unplaced`, label `unplaced-finding drift`, appended last and carrying no gloss; the anchored pattern that places it in `_CLASS_PATTERNS`; and in `fam_modified_block_currency` the emit — group the findings `classify` returns `UNCLASSIFIED` for by shape, and per shape append ONE `warning` carrying the count, the first instance's rule text verbatim, its repo and its delta path. `classify`, `class_counts` and `class_summary` keep their signatures and their no-context discipline; the residual row keeps rendering; the module's stale numerals move (`:40` three-arms/four-classes, `:137` "THREE OF THEM", `:1299`, the `:1315` gloss sentence, `:1349` "FOUR ENTRIES FOR FIVE RULE SHAPES"). `tests/doc-health/test_modified_block_currency_reporting.py` — the five scenarios of this delta arrive as new tests, and six standing pins move by name: the class-registry pin (`:115`), the rule-shapes pin (`:150`), the verbatim four-row list (`:287-294`), the marker-defects-is-the-last-row assertions (`:422`), `test_every_finding_carries_its_class_s_band_and_action`'s `all(checked.values())` (`:538-547`), and the `len(block) == 5` pin inside `test_the_block_is_not_a_finding_and_cannot_become_one` (`:707`); plus the numerals at `:5`, `:39`, `:116-117`, `:151`, `:429`. `tests/doc-health/fixtures/modified-block-currency-unplaced/` — the new fixture tree that exercises the fifth class behaviourally. `tests/doc-health/test_modified_block_currency_self_gate.py` — a FOURTH probe with its positive control in `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree` (`:661-702`). `tests/doc-health/test_modified_block_currency_fixtures.py` — the FR-023 snapshot (`:1127-1146`) gains `_DRIFT_SEVERITY` in its severity tuple, and its `:1117` numeral is corrected; the public-callable list is UNCHANGED, the emit adding no public callable. `specs/022-modified-block-currency-reporting/contracts/report-section.md` — the byte-level report contract enumerates the four classes verbatim (`:17-24` the bullets, `:33-45` the worked example, `:98-109` the class map, `:116-123` the action-line table) and is AMENDED by the realization rather than left to drift. NO other family's behaviour, NO workflow file, NO change to `Finding`, to `report.render`, to the ranked-plan or finding grammars, to `families.FAMILY_SUMMARIES`, to `FAMILY_RESOLUTION`, to the governed corpus, to the lifecycle scan set, or to any threshold. NO `## MODIFIED Requirements` block on any promoted requirement — see § Orchestrator Decisions D1, which is the decision this packet's shape turns on.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-modified-block-currency-check` and `add-family-enumeration-check` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts — zero — and in no other line. The change therefore ships ACTIVE and archives only after the merge.
Status: ratified
Ratified: 2026-08-27 by Brett — in-session commissioning, verbatim: "Amend now". The citation covers the DECISION TO BUILD THIS AMENDMENT and nothing else; the three design decisions in § Orchestrator Decisions below were taken by the authoring session under standing patterns, are NOT covered by this citation, and are flagged there for veto. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-27`).
Amended: 2026-08-28 by Brett — in-session commissioning, verbatim: "Amend: shape = arm template, all interpolations masked". D3's shape-identity rule is widened from quoted-spans-plus-digit-runs to EVERY field the arm's template interpolates; the measured cause is recorded in § Orchestrator Decisions and in `specs/026-unplaced-finding-drift/plan.md` § OPEN-1. Nothing else in this packet moves and the predicted severity movement stays ZERO.
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
constant-versus-constant invariant — but a nightly aggregation run over the
FOURTEEN submodules that carry `openspec/changes/` (of the nineteen in
`.gitmodules`) is not CI, and it is where a rule text that only drifts on a corpus
nobody has a fixture for would first appear.

**It reads zero today, and that is the argument for building it now rather than
later.** Measured on this tree at `b5fb03f3`, and re-measured at each catch-up
merge since (`d808974d`, then `45ba637a`): `unclassified: 0` every time, the
residual row absent from the block. The arms' own population moved under this
packet while it was in review — PR #444 declared
`add-composed-view-authoring`'s rename with a `Merged into` marker and took the
scenario arm's standing population to zero — and the residual did not move,
because it never depended on any arm reading anything. The population this change would report is empty, so the
amendment costs nothing to land and the standing state it pins is the one every
reader currently assumes.

## What Changes

- **`doc-health` gains ONE ADDED requirement**, "A modified-block-currency finding
  its own class map cannot place is itself a finding": an unplaced rule text emits
  one `warning` PER DISTINCT SHAPE per run, naming that shape's count and the first
  instance's rule text verbatim and carrying its repo and delta path, with the
  action line "extend the class map in
  `scripts/doc_health/modified_block_currency.py`, or fix the drifted rule text the
  finding names"; the finding is itself placed by the map into a FIFTH class so it
  is never counted by the residual it reports; the pattern that places it is
  anchored at the start of the rule text; the residual row keeps rendering; the
  band is `warning` and the family stays absent from `FAMILY_RESOLUTION`.
- **NO `## MODIFIED Requirements` block, on any promoted requirement.** Canon does
  not enumerate this family's finding classes — measured, not assumed; D1 carries
  the measurement.
- **The requirement BODY is deliberately lean** — 36 lines where the first draft
  ran to 70. Every body line of a promoted requirement is carriage-ledger surface
  that a future MODIFIED block must restate byte-for-byte, so rationale that a
  reader can get from this proposal does not belong in canon. The body keeps the
  SHALLs, the shape definition, the anchor clause and the not-contested clause; the
  arguments for them are in § Orchestrator Decisions below.
- **The realization AMENDS `specs/022-modified-block-currency-reporting/contracts/report-section.md`.**
  That contract is byte-level ("everything here is asserted by a test; nothing is a
  suggestion") and enumerates the four classes four times over. A fifth class that
  landed without touching it would leave the corpus carrying a byte-level contract
  that is false about the code it describes.
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
  `tests/doc-health/test_modified_block_currency_reporting.py`, a new fixture tree
  `tests/doc-health/fixtures/modified-block-currency-unplaced/`, one probe in
  `tests/doc-health/test_modified_block_currency_self_gate.py`, the FR-023 snapshot
  in `tests/doc-health/test_modified_block_currency_fixtures.py`, and
  `specs/022-modified-block-currency-reporting/contracts/report-section.md`.
- **Predicted severity movement: ZERO, in every band.** Measured with
  `python3 scripts/doc-health.py --single-repo . --family
  modified-block-currency` at the current base `45ba637a`: **0 `warning`,
  7 `info`**, class counts `scenario-title completeness 0 / carriage ledger 7 /
  title resolution and ordering 0 / marker defects 0`, and **`unclassified` 0** —
  the residual row does not render. (At `b5fb03f3` and `d808974d` the same run
  read **1 `warning`, 7 `info`** with the scenario arm at 1; PR #444 discharged
  that finding by declaring the rename with a `Merged into` marker, which is the
  arm working as designed and is unrelated to this change.) The finding this
  change adds fires only where the residual count is nonzero, so the run after
  realization emits the same seven findings, and the class block gains one row
  reading `0`. The canon-share headline, the per-stage census, the inventory and
  the catalog are untouched, because the family reads neither the governed corpus
  nor the lifecycle scan set.
- **Predicted movement from this PACKET's own delta: ZERO.** This packet carries an
  ADDED block and no MODIFIED block, and the family reads
  `## MODIFIED Requirements` blocks only. Verified by running the family over this
  tree with the packet present: **0 `warning`, 7 `info`, `unclassified` 0** —
  byte-identical to the baseline above, no finding naming any path under
  `openspec/changes/add-unclassified-finding-class/`.
- **Measured effect on every other repository**: unknown until an aggregation run,
  and by construction it is zero unless a rule text has drifted there — which is
  precisely the case this change exists to surface rather than to predict.

## Orchestrator Decisions — FLAGGED FOR VETO

Brett commissioned the amendment. The three decisions below were taken by the
authoring session under standing patterns and are named so they can be reversed
on a word. D3 was rewritten at packet review on 2026-08-27; the flag stays.

**Amended 2026-08-28 by Brett** — in-session commissioning, verbatim: "Amend:
shape = arm template, all interpolations masked" — D3's identity rule widened
from quoted-spans+digits to every interpolated field; measured cause (6 rows for
1 remedy on the 2026-08-28 tree) recorded in
`specs/026-unplaced-finding-drift/plan.md` § OPEN-1.

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
name itself, the next run would report a drift the map had just been extended to
describe, and the tally still would not sum — rejected as incoherent. (b) Give the
residual row a severity: rejected because
`test_the_block_is_not_a_finding_and_cannot_become_one` pins, through
`report.parse_previous`, that the class block never re-enters the machinery that
reads findings back, and that pin is worth more than the shortcut. (c) A fifth
`FindingClass` with an anchored pattern, which is what this delta requires: the map
places its own drift finding, the residual keeps counting only the arms' unplaced
findings, and the counts sum.

Three consequences of (c) are decisions in their own right and are recorded here
rather than in the requirement body. **The anchoring is not decoration** — the
finding QUOTES an unrecognized rule text, and an unanchored probe would file it
under whichever class the quotation resembles, which is the exact misfiling
`_BLOCK_HEAD` was measured into existence to prevent. **The residual row stays**
beside the finding rather than being replaced by it: the row is what makes the
tally sum to the rows it is printed above, which is the reason it exists, and a
reader with the block in front of them must not have to reconstruct it from the
ranked plan. **The class id is `unplaced` and its label is `unplaced-finding
drift`**, neither containing the substring `unclassified`, because
`test_a_finding_the_map_cannot_place_is_counted_and_named` asserts that string's
ABSENCE from a fully-classified summary and a class label renders even at a count
of zero — the obvious name would have reddened a standing pin for a real reason.

**D3 — ONE finding per DISTINCT UNPLACED RULE SHAPE per run, a shape being the
ARM'S TEMPLATE with every interpolated field masked.** *(Rewritten at packet
review, 2026-08-27; previously one per run. Shape identity widened by Brett's
amendment of 2026-08-28, above; as first ratified the mask covered quoted spans
and digit runs only.)* Three readings were on the
table: one per repository, one per run, and one per shape. Per repository is wrong
because the class map is a module constant compiled once per process, so a
per-repository emit would put ONE remedy into an aggregation run's ranked plan once
for every repository in scope — `family_enumeration` records the same reading for
its missing-direction invariant, "a runtime finding would fire identically on every
run for every repository and say nothing a reader of a report could act on". One
per run is wrong in the other direction: two genuinely different drifted rule
shapes are two map entries to write, and collapsing them reports one remedy where
two are owed and quotes only one of them. **Per shape is the count of remedies**,
which is what a ranked plan is a list of. Shape identity is mechanical and stated
in the delta — rule texts equal after EVERY FIELD THE ARM'S TEMPLATE
INTERPOLATES is replaced by a fixed placeholder: quoted spans, digit runs,
repository-relative paths, change identifiers, unit-kind lists, and whatever
else an arm substitutes into its fixed prose — so one shape is one arm template,
which is one map entry to write. The mask is derived FROM THE ARM TEMPLATES
THEMSELVES (the fixed prose is the shape; the interpolations are not), so it
cannot drift from the code the way a hand-listed mask would.

**Why the mask is the whole template and not only the quoted spans.** The
narrower rule was measured during realization (Speckit 026) and it does not
count remedies: the arms interpolate the promoted spec's path (`basis.spec_rel`),
the `[body]`/`[bullet]` unit-kind list a carriage-ledger finding quotes, a
change-id list in the ordering arm, and an unresolved block's `why` clause,
none of which the quoted-span-and-digit mask touches. On the 2026-08-28
openxFactory tree, ONE dropped class-map entry (`carriage-ledger`) yielded SEVEN
unplaced findings in SIX shapes — six `warning` rows in the ranked plan for ONE
map entry to write. The measured table, including
`-two-writers` 9 unplaced → 4 shapes, `-markers` 3 → 3 and this feature's own
`-unplaced` tree 3 → 1, is in `specs/026-unplaced-finding-drift/plan.md`
§ OPEN-1. Under the amended mask the real tree reads ONE. The realization could
not apply the wider mask on its own, the third scenario as first ratified
pinning the narrower one, which is why this amendment exists. The emitted finding's
identity is (family, repo, path of the FIRST instance of that shape in the family's
own report order), which is deterministic; and because the band is `warning`, that
identity never reaches `regressions()`, which matches `critical` and `error`
findings only, so no issue is opened and no per-run identity churn can create one.
What this gives up is named: on an aggregation run one finding names one example
per shape, so a second repository's instance of the SAME shape is counted but not
quoted.

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
