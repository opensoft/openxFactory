---
code_surface: openxFactory (`scripts/doc_health/modified_block_currency.py` — the marker parser gains a THIRD reserved form, `Modified over`, recognized by a complete prefix like the other two, naming no units and therefore excluded from unit suppression and from the marker-defect check while still being excluded from unit derivation in both canon and block; `sibling_titles` is widened to return the ADDING CHANGE ID beside each `(capability, title)` so the pairing can be named and self-pairing detected, rather than the bare title set it returns today; `fam_modified_block_currency`'s `if status == "pending": continue` is replaced by an emit for the new pairing class, the three comparison arms still NOT running against a pending block; a reader for active `## ADDED Requirements` blocks against the promoted index the family already builds, for the collision class; two new severity constants and two new action constants, named apart from `_LAUNCH_SEVERITY` on the module's own stated reason for `_RESOLUTION_SEVERITY`, `_LEDGER_SEVERITY` and `_DRIFT_SEVERITY` — a reason that has since been demonstrated rather than merely reserved, § 7.2's flip having landed at `7f656980` (PR #529, 2026-08-31) and moved `_LAUNCH_SEVERITY` alone; two new `_ArmTemplate` registrations appended to `_ARM_TEMPLATES`; two new `FindingClass` entries in `CLASSES`, inserted before the `unplaced` class so that "the gate-bearing arm reads FIRST" and "the drift class reads LAST" both stay true; two anchored `_CLASS_PATTERNS` entries; and the module's stale numerals — the docstring's class enumeration, "FIVE ENTRIES FOR SIX RULE SHAPES", and the arms-versus-classes counts. `tests/doc-health/test_modified_block_currency_reporting.py` — the class-registry pin, the rule-shapes pin, the verbatim class-row list, the last-row assertions and the `len(block)` pin all move by name. `tests/doc-health/test_modified_block_currency_self_gate.py` — `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree` no longer covers the new classes; a NAMED EXACT SET for the pairing class's four standing subjects joins `_LEDGER_SUBJECTS` under the same movement discipline, and the collision class gets a zero assertion with a positive control. New fixture trees under `tests/doc-health/fixtures/` for each reported state. `specs/022-modified-block-currency-reporting/contracts/report-section.md` — a byte-level contract enumerating the classes four times over, AMENDED by the realization rather than left false. `docs/doc-health.md` — the family paragraph names three arms plus a marker-defect class plus a fifth `unplaced` class and is amended. NO change to any other family, to `Finding`, to `report.render`, to the ranked-plan or finding grammars, to `families.FAMILY_SUMMARIES`, to `FAMILY_RESOLUTION` (the row `7f656980` added stays exactly where #529 put it — what moves is PROMOTED TEXT, in this packet's `doc-health` MODIFIED block, not this table), to the governed corpus, to the lifecycle scan set, or to any threshold. NO new deterministic check family, so the "Deterministic check families" enumeration and its numerals are untouched and unrestated.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-modified-block-currency-check`, `add-family-enumeration-check` and `add-unclassified-finding-class` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount § Impact predicts and in no other line. The change therefore ships ACTIVE and archives only after the merge — and, because its own MODIFIED blocks are written over `release-realization` and `doc-health` CANON rather than over any sibling's addition, its archive is not itself subject to the ordering obligation it adds.
Status: draft
Proposed: 2026-08-29
Origin: openxFactory issue #502, filed 2026-08-29 on Brett's in-session ruling "file the successor now" out of the §7.4 council sitting on PR #497 (`add-binding-consumer-identity`). The gap was raised by `lead-architect` under `cross_cutting_design` (LA-C2) and concurred by `lead-quality` (LQ-C5); both seats attached the condition that PR #497 must neither close it nor be delayed for it, recorded in the council record's §8.5 and §10 and honoured — #497 merged carrying only its own local stopgap. Related and already closed, for the defect family: #329 (sibling changes carrying latent scenario loss) and #330 (`promotion-fidelity`'s blind spot). Related and open: #318 (an origin taxonomy with no kind meaning "proposed, not approved" — the state this packet is in), #342.
---

# Proposal: govern-sibling-added-modified-deltas

## Standing

**THIS PACKET IS A PROPOSAL AND CLAIMS NO RATIFICATION.** `Status: draft`, no
`Ratified:` line. What Brett authorized on 2026-08-29 was the DECISION TO FILE
THE SUCCESSOR, verbatim "file the successor now"; `.openspec.yaml` records that
and says plainly that it does not reach this packet's content. Every design
decision the authoring session took is named in § Orchestrator Decisions for a
§7.4 council sitting and Brett's ratification to accept or reverse.

**IT DOES NOT CLOSE #502, and it does not close it here.** Issue #502's own
scope section carries both seats' condition that the change which SURFACED the
gap must not close it; that condition binds `add-binding-consumer-identity` and
it has been honoured. The successor is a different question: this change is the
one that fills the three holes, so **when it archives on merged-and-green
realization evidence it may say `Closes #502`, and this proposal states that
intent explicitly rather than leaving it to be inferred.** It is stated as
intent and not as an act: an unratified proposal closing a governance issue
would be exactly the shape #502 exists to complain about.

## Why

**A `## MODIFIED Requirements` block whose requirement exists only as an active
sibling's `ADDED` is governed by no promoted requirement, evaluated by no
doc-health arm, and declared by no marker.** Issue #502 measures the three holes
and this section re-measures them at this branch's catch-up merge with `main`,
whose `main`-side parent is `7f656980`.

**Hole 1 — no normative rule reaches it, and there is a plausible-looking one to
mis-cite.** `release-realization`'s "Ordered deltas and branch vocabulary" is the
rule an author naturally reaches for, and its antecedent is a requirement
*"already **modified** by an active ratified change"* — in the body and in its
only scenario, "Two changes touch one requirement", whose WHEN reads "a
requirement that an active ratified change already modifies". A sibling that
ADDS the requirement does not satisfy it. `document-lifecycle`'s restatement in
"A MODIFIED requirement block restates the requirement as canon currently states
it" adds *"two active **RATIFIED** writers"*, which narrows further. **Two of the
four live pairs cite that rule in their own delta preamble.** One cites it as
though it applied — `add-wallet-carried-review-authority` quotes the antecedent
verbatim and adds "with the scenario 'Two changes touch one requirement' making
it a MUST", of a scenario whose antecedent it does not meet. The other,
`add-binding-consumer-identity`, carries the corrected reading only because a
seat caught it in review: "a citation whose antecedent is *'already MODIFIED'*
while the custody change ADDS, so it is an EXTENSION of that rule to a shape no
promoted requirement reaches, not an application of it (LA-A3)". **The other two
pairs declare nothing at all** — `implement-keycloak-install-repo` and
`implement-openxpki-install-repo` open `## MODIFIED Requirements` with no
preamble, no citation and no note.

**Hole 2 — no arm evaluates it, and the silence reads as clearance.**
`scripts/doc_health/modified_block_currency.py`'s `resolve` returns `pending`
for this shape and `fam_modified_block_currency` drops the block before any arm
runs:

```python
if status == "pending":
    continue
```

The family's docstring gives the reason and the reason is correct on its own
terms — "pending means there is nothing to compare: the promoted requirement
does not exist yet" — and the 2026-08-27 ruling against synthesising a basis
from the sibling's ADDED text stands, for the good reason that it would measure
against text no promoted requirement carries. **What does not follow is dropping
the block before anything at all looks at it.** The carriage arms, the title arm
and the marker arm all skip it, so their silence is uncomparability rather than
clearance — and a packet can offer that silence as a safety fact, which is what
PR #497's LQ-A4 amendment corrected from "doc-health reports nothing" to
"doc-health DECLINES TO MEASURE".

**Hole 3 — the ordering obligation has no backstop in the only direction that
needs one.** `_arm_ordering` requires TWO RATIFIED `MODIFIED` blocks in a group.
A sibling's block is `ADDED`, so it is never collected into the group at all —
the group is size one FOREVER, not merely today.

| order | what happens |
| --- | --- |
| the adding sibling archives first (safe) | the requirement enters canon, `resolve` returns `canon`, the carriage arms run — a real backstop |
| the MODIFIED writer archives first (unsafe) | `resolve` returns `pending`, the ordering arm cannot fire, nothing checks anything |

**The one case a per-packet ordering obligation exists to guard is the one case
with no guard.** Today that obligation is prose in a task list, per packet, and
eight packets writing their own pre-archive `grep` is worse than one rule.

**The population, re-measured at the catch-up merge.** Run with the family's own
`resolve` at `7f656980`, the `main`-side parent of this branch's catch-up merge
of 2026-08-31:

```
TOTAL active MODIFIED blocks: 20
status: {'canon': 16, 'pending': 4}

PENDING pairs — the change that ADDS, and markers on each:
  add-binding-consumer-identity       | credential-contracts     | add-notebook-hosting-credential-custody | markers=0
  add-wallet-carried-review-authority | roles-authority-model    | add-substantive-review-lane             | markers=0
  implement-keycloak-install-repo     | repo-boundary-governance | add-identity-brokering                  | markers=0
  implement-openxpki-install-repo     | repo-boundary-governance | add-trust-anchor                        | markers=0
```

**THE TOTAL MOVED AND THE PENDING SET DID NOT, which is the fact worth
recording.** At `91cf0a46` the same run read 19/15/4. The twentieth block is
`add-structured-scope-substrate`'s (PR #525), over `release-realization`'s
"Realization axis declaration" — a DIFFERENT requirement of the same
specification this packet writes, resolving `canon` and outside this class
entirely. Nothing entered or left the pending set in the two days between the
two readings, so the four pairs above are the four #502 measured. Run over this
branch's own tree, with this packet present, the same resolver reads 22/18/4:
the twenty-first and twenty-second blocks are this packet's own — one over
`release-realization` canon and one over `doc-health` canon — and BOTH resolve
`canon`, which is § 4.2's assertion measured rather than restated.

**Four live pairs, zero markers, and every one of the four adding siblings is
`ratified`** — so the whole live population sits squarely inside the antecedent
`release-realization` would have if its antecedent reached ADDED, and the draft
case is prospective rather than populated. **The seats' figure reconciles as
#502 reconciles it, with one correction owed to the appendix:** LQ-C5 cited
eight, the family docstring's historical seven plus #497's own block; LA-C2's
own return says "**Four** blocks, zero markers". Four is the live number and
eight the cumulative one, and the difference is itself evidence that this class
turns over with nothing tracking it. **ONE OF THE FOUR HAS STOPPED BEING MERELY
STANDING**: `add-binding-consumer-identity` is fully realized and its archive is
blocked by exactly this rule's shape, while `contract-v2.4` has falsified a
scenario of the addition it waits on. That pair is worked below, under § The one
live pair this rule already disposes, because a rule tested against a live case
is a better thing to rule on than one tested against none.

**The proposal cross-reference already exists in 4 of 4 — and it is not enough.**
Every one of the four modifying proposals names its adding sibling as a whole
token, so `declarations()` would already resolve the pairing today at zero
authoring cost. It is still the wrong instrument, measured: those same four
proposals name **two to three** other active changes each as whole tokens, only
one of which is the adder. `implement-keycloak-install-repo` names
`add-identity-brokering` (its adder), `add-trust-anchor` (the OTHER pair's
adder) and `implement-openxpki-install-repo`. A change-level mention cannot say
which requirement rests on which sibling, and `add-notebook-projection-identity`
and `qualify-avatar-live-voice` already carry three and five MODIFIED blocks
respectively, so the ambiguity is not hypothetical.

## What Changes

- **`release-realization` gains the rule, by MODIFIED block, and its antecedent
  is EXTENDED rather than reinterpreted.** A proposal modifying a requirement an
  active ratified change ADDS references that change and declares its deltas
  relative to its outcome, on the same terms as the already-modified case; the
  two antecedents are disjoint by construction, a requirement being either one
  canon carries or one it does not. The block adds the archive-ordering
  obligation in the same requirement: such a change SHALL NOT archive while the
  requirement it modifies is unpromoted. **Two clauses keep that obligation from
  being escaped rather than met.** CONVERSION: re-shaping the block to
  `## ADDED` does not dissolve the obligation, the antecedent attaching to the
  pairing and not to the block's form, so conversion is lawful only as a PAIRED
  act ruled by the ratifying authority and amending both packets at once. This
  is what makes the general rule reach as far as the per-packet conversion text
  it replaces, rather than one sentence short of it. FALSIFICATION: where the
  repository's landed state contradicts a scenario of the unpromoted `## ADDED`
  block, the ADDING change amends that scenario before its archive promotes it,
  and the order still holds.
- **`document-lifecycle` gains ONE ADDED requirement**: the pairing is declared
  by a THIRD reserved marker form,
  ``**Modified over `<basis change-id>`'s addition by <change-id>
  (<YYYY-MM-DD>):**`` followed by ` — <reason>`, one paragraph inside the
  MODIFIED block, recognized by a complete prefix and never by prose. It names
  no units, so it suppresses nothing and can never be a defective marker; like
  every marker it is not a carriage unit. The proposal-level cross-reference
  stays owed and is explicitly not a substitute.
- **`doc-health` gains TWO ADDED requirements**: the pairing check that
  evaluates the `pending` shape in three reported states (undeclared,
  misdeclared, self-referential) and is SILENT on the fourth (declared and
  resolving); and the collision check that reports an active `## ADDED
  Requirements` block for a title canon already carries, which is the archive
  ordering's only possible mechanical backstop.
- **`doc-health` also gains ONE `## MODIFIED Requirements` block, and it is on
  NEITHER of the requirements D2 measures.** It is on "A modified-block-currency
  finding its own class map cannot place is itself a finding", whose promoted
  text says the family "SHALL remain absent from `FAMILY_RESOLUTION`"
  (`openspec/specs/doc-health/spec.md:2088`) with a scenario at `:2126` resting
  a MUST on that absence — an assertion `7f656980` (PR #529, 2026-08-31)
  falsified WITHOUT amending any specification. The block supersedes the absence
  rule, PRESERVES the protection it bought by re-seating it on the act that
  extends the class map, and thereby REGULARIZES #529: canon catches up with a
  row the code already carries, rather than the contradiction being named and
  left for a reader to arbitrate. Two units are dropped and both are declared by
  a `Removed from canon by` marker; the other thirty-three are restated
  byte-identical.
- **No `## MODIFIED Requirements` block on "Currency of an active change's
  MODIFIED requirement blocks" or on "Deterministic check families".** D2 below
  is the measurement that decided it, re-taken against today's canon, and the
  block above touches neither of them.
- **No fourth comparison arm, and the 2026-08-27 ruling is not reopened.** The
  new check compares no requirement text; its inputs are the delta's own marker
  and the set of active additions.
- **The implementation lands in this change**, as Speckit features sequenced by
  `tasks.md`, on the precedent its sibling families set.

## The one live pair this rule already disposes

**THE RULE IS NOT PROSPECTIVE FOR ONE OF THE FOUR, so the disposition is worked
here rather than left for the first archive gate to discover.**
`add-notebook-hosting-credential-custody` ADDS "Each consuming system reaches a
shared operated identity through its own binding";
`add-binding-consumer-identity` MODIFIES it; and custody's own task 6.2 holds it
open on `add-notebook-projection-identity` ("the generalization these
requirements presume promotes then"), which its own § Impact repeats — "the
generalization this builds on is unpromoted until `add-notebook-projection-identity`
archives". `add-binding-consumer-identity`'s task 7.3 records the same
dependency from the far end. **`add-binding-consumer-identity` is FULLY
REALIZED** — PR #516, squash `5e8a33cf`, the cut `contract-v2.4` at `afdf0e88`,
tags published and verified — and its archive is blocked by exactly this rule's
shape: its task 7.2's mechanical assertion greps
`openspec/specs/credential-contracts/spec.md` for the requirement title and
FAILS BY DESIGN, canon not carrying the title while custody is unarchived.

**DISPOSED AS (a), CHAIN ORDER**: `add-notebook-projection-identity` →
`add-notebook-hosting-credential-custody` → `add-binding-consumer-identity`.
Three obligations follow and all three are this packet's to STATE, none of them
this packet's to PERFORM:

- **Custody owes the fifth-scenario amendment, under the falsification clause.**
  Its ADDED block carries "The published binding shape cannot yet express the
  access identity", whose THEN reads "the shape carries no consumer or
  access-identity field, so the per-system authority is asserted by the
  binding's owner and its estate wiring rather than proven by the record".
  **`contract-v2.4` falsified it.** The published schema now declares
  `consumer:` with `holder_ref` and `fetch_identity`
  (`contracts/schemas/xfactory-credential-contracts.schema.yaml:185-229`), cut
  and recorded at `contracts/CHANGELOG.md` § `contract-v2.4 — 2026-08-31`.
  Archiving custody unamended in the chain order would promote into canon a
  scenario the repository's own published schema contradicts — the safe order
  delivering the loss the unsafe order was supposed to have a monopoly on, which
  is why the clause exists. `tasks.md` § 6.6 carries it, with custody's owner
  consenting as § 6.2 requires of every edit to a ratified packet.
- **`add-binding-consumer-identity` owes the `Modified over` marker**, already
  § 6.1, and its § 7.4 obliges the carriage diff to be re-run because the marker
  touches the block. A marker is not a carriage unit, so the diff's ANSWER does
  not move; the re-run is the packet's own discipline and is cheap.
- **Conversion without pairing was considered and is FORBIDDEN.** It is the one
  route that would unblock `add-binding-consumer-identity` today without waiting
  on custody, and the conversion clause refuses it: converting that block to
  `## ADDED` without a ruling that also amends custody would leave two active
  additions of one title, and after the archive an active addition for a title
  canon carries — which is the D5 collision class reporting its first instance
  ever, on a breach this packet's own rule forbade.

**WHAT THIS DISPOSITION IS AND IS NOT.** It is the rule applied to a pair that
already exists, written down so the council rules on a worked case rather than on
an abstraction. It is not an amendment to either packet: both are ratified, both
edits are post-ratification acts their owners consent to, and this packet OBLIGES
them without performing them.

## Impact

- **Affected specs**: `release-realization` (MODIFIED), `document-lifecycle`
  (ADDED), `doc-health` (ADDED **and MODIFIED** — two new requirements, plus one
  MODIFIED block over the promoted unplaced-class requirement whose
  `FAMILY_RESOLUTION`-absence rule #529 spent).
- **Affected code**: `scripts/doc_health/modified_block_currency.py`, its three
  test modules, new fixture trees, the byte-level report-section contract, and
  `docs/doc-health.md`.
- **Predicted severity movement: +4 `warning`, 0 `error`, 0 `critical`, 0
  `info`**, measured at `7f656980` with the family's own
  resolver: four `pending` blocks, all undeclared, none self-referential, so the
  pairing class reports four and the misdeclared and self-referential states
  report zero. The collision class reports **ZERO — measured, not assumed**: no
  active `## ADDED Requirements` block in this repository names a capability and
  requirement title the promoted specification already carries. A run configured
  `--fail-on error` or `--fail-on critical` is unaffected by construction, and
  the canon-share headline, the per-stage census, the inventory and the catalog
  are untouched because the family reads neither the governed corpus nor the
  lifecycle scan set. **THE FIGURE IS THE UNDISCHARGED ONE, and D4 asks for the
  order that makes it ZERO.** +4 is what the class would report if it landed
  against the population as measured. Under D4's sequencing — § 6's markers
  first, then F1 — the four are already declared when the class first runs and
  the movement is **0 `warning`**. Both numbers are stated because the archive
  gate has to know which one it is reading; § 8.1 reads the order actually
  taken.
- **Predicted movement from this PACKET's own delta: ZERO ACROSS BOTH ITS
  MODIFIED BLOCKS, and verified rather than argued.** Both are over CANON — one
  over `release-realization`, one over `doc-health` — so both resolve `canon`
  rather than `pending` and the pairing class can reach neither. The
  `release-realization` block restates both promoted body sentences and both
  promoted scenarios byte-identical and everything it adds is new text. The
  `doc-health` block restates 33 of that requirement's 35 promoted units
  byte-identical and DECLARES the other two by a `Removed from canon by` marker
  naming each as a code span, which is what this family's own discipline
  requires of a deletion; the marker is not a carriage unit and names no unit
  the block still carries, so it is not a marker defect either. Measured with
  the family's own arms over this tree with the packet present: **0 title
  findings, 0 ledger findings and 0 marker-defect findings** against
  `openspec/changes/govern-sibling-added-modified-deltas/specs/release-realization/spec.md`
  and against
  `openspec/changes/govern-sibling-added-modified-deltas/specs/doc-health/spec.md`.
  **RE-MEASURED AT THE CATCH-UP MERGE**, as § 4.2 obliges rather than permits:
  canon still carries the `release-realization` requirement at
  `openspec/specs/release-realization/spec.md:64-78` and the `doc-health` one at
  `openspec/specs/doc-health/spec.md:2055-2126`, both unmoved, and the family's
  run over the branch tree emits 8 findings, none of them at either path.
- **`_LEDGER_SUBJECTS` — the F3 exact set — GAINS NO ROW FROM THIS CHANGE.**
  That set has fallen due three times already (the archive of
  `add-modified-block-currency-check`, then `clean-doc-health-floor` and
  `declare-generated-projection-status` on consecutive days), so the honest
  thing to say is what this packet adds to it, which is nothing: zero ledger
  findings against either of its own two MODIFIED blocks means zero rows. What
  the REALIZATION adds is a different constant — a named exact set for the pairing class's four standing
  subjects, under the same movement discipline and with the same retirement
  condition written into it: each row retires when its declaring block carries a
  marker or its adding sibling archives.
- **`FAMILY_RESOLUTION` ALREADY CARRIES THE ROW, and this change adds none.**
  What this packet asserted on 2026-08-29 — that the family stays absent — was
  SPENT TWO DAYS LATER and is corrected here rather than carried:
  `scripts/doc_health/families.py:117` reads
  `"modified-block-currency": CONTESTED`, landed at `7f656980` (PR #529,
  2026-08-31) as the second half of `add-modified-block-currency-check` § 7.2's
  reserved flip, together with `_LAUNCH_SEVERITY`'s move to `error`. **That
  table has NO PER-CLASS GRAIN** — `runner.main` applies it by `Finding.family`
  alone, one string every arm of the module shares — so the row reaches both
  classes this change adds, and no choice available to this packet can launch
  them `auto-fixable`. Measured on the branch tree: all 8 findings the family
  emits today carry `class="contested"`. **AND CANON NOW SAYS SO**: the
  `doc-health` MODIFIED block above supersedes the promoted absence rule, so
  this packet no longer rests on a corpus that says one thing in
  `families.py` and the opposite at `openspec/specs/doc-health/spec.md:2088`.
- **THE CONSEQUENCE OF THAT ROW FOR THE PAIRING CLASS, stated rather than left
  to be discovered.** A pairing finding discharged by its marker is a
  `contested` finding that vanishes between reports, and
  `report.uncited_resolutions` keys on `(family, repo, path)` — so unless that
  path still carries another finding of this family, or
  `health/dispositions.yaml` names it with a `cite`, the discharge raises an
  `error` on the night the marker lands. **It is measured that none of the four
  pending delta paths carries another finding of this family**: each of the four
  changes holds exactly ONE MODIFIED block, and a pending block is dropped
  before the arms run, so all four keys would vanish outright. This is the back
  door D4 named when the family was absent, arriving from a direction D4 did not
  have to consider. D4 below answers it — and answers it in an ORDER, because a
  disposition is not a free instrument here: `promotion_fidelity.disposed` is
  consulted BEFORE a block is resolved and its entries have family/repo/path
  grain with an optional REQUIREMENT narrowing and NO finding-class grain, so an
  entry recorded to answer a pairing finding also silences the three comparison
  arms over that block — including after the basis archives, which is the one
  moment those arms have ever been able to read it. The delta therefore makes
  sequencing THE route, and where the citation is unavoidable it carries a grain
  and a retirement so it cannot outlive the pairing it answers.
- **The "Deterministic check families" enumeration and its numerals are
  untouched and unrestated**, no new family being registered — the same shape
  `add-unclassified-finding-class` and "A declared unrecoverable pin loss is
  discharged by a superseding record" both take, and the reason the
  `family-enumeration` gate stays green through this packet.
- **Measured effect on every other repository: unknown until an aggregation
  run, and deliberately so.** § 5 of `tasks.md` makes that measurement a task
  rather than a prediction; that is why the launch BAND is advisory rather than
  a claim this proposal makes. The resolution class is not this packet's to set
  either way (§ `FAMILY_RESOLUTION` above), which is precisely why a population
  found elsewhere matters more than it did when this bullet was written: it
  would arrive `contested` on its first emit, and D4's second limb is what
  answers for it.

## Orchestrator Decisions — FLAGGED FOR VETO

Brett authorized the FILING. The five decisions below were taken by the
authoring session under standing patterns and are named so they can be reversed
on a word.

**D1 — `release-realization` owns the rule, by EXTENDED ANTECEDENT, and
`document-lifecycle` owns the declaration.** #502's first question offers two
shapes: extend the antecedent, or state plainly that no rule governs the shape
and the placement rests on the author's argument. The second is not available in
a corpus that already reports an unresolved MODIFIED title as a defect: a shape
the estate admits and does not govern is the shape a packet mis-cites, and two
of the four live pairs did. Between the capabilities, the split follows what
each already owns — `release-realization` owns ORDERING BETWEEN CHANGES ("Changes
SHALL sequence explicitly"), and this gap is an ordering gap; `document-lifecycle`
owns what a delta must CARRY and already defines every reserved marker in the
corpus, so the marker goes there. **The cost of the veto is named**: if the rule
is instead placed wholly in `document-lifecycle`, `release-realization` keeps an
antecedent that reaches half its own subject and the next author reads it the
way `add-wallet-carried-review-authority` did.

**D2 — NO MODIFIED BLOCK ON EITHER CURRENCY REQUIREMENT, and this was measured
rather than preferred.**
The obvious shape for "a new finding class" is a MODIFIED block on "Currency of
an active change's MODIFIED requirement blocks", restating its ~290 lines and 14
scenarios byte-for-byte. It is not owed. Canon's own scenario for this shape says
the block "MUST NOT be reported **as unresolved**" — grepped at
`openspec/specs/doc-health/spec.md:1790`, and the qualifier is in the promoted
text. It does not say the block must not be reported at all, and it does not say
the family emits nothing for it. Canon likewise never enumerates the family's
finding classes: it says the family "SHALL implement three comparison arms" and
names the three ARMS, and the module has carried non-arm classes since launch
(marker defects, then `unplaced`). The new classes are non-arm classes of the
same kind, and the sentence mapping arms to bands stays true word for word
because `warning` is a band it already names. This is the identical measurement
`add-unclassified-finding-class` recorded as its D1, re-taken against today's
canon rather than cited from memory. **The cost of the veto is named**: if D2 is
vetoed this packet grows a MODIFIED block over the corpus's largest requirement,
the carriage ledger reports this packet's own delta for whatever it rewords, the
predicted movement stops being zero, and `_LEDGER_SUBJECTS` gains a row.

**D2 IS ABOUT THOSE TWO REQUIREMENTS AND NOT ABOUT THE CAPABILITIES, and one
MODIFIED block IS opened — on a third requirement and for a different reason.** "A
modified-block-currency finding its own class map cannot place is itself a
finding" says the family "SHALL remain absent from `FAMILY_RESOLUTION`"
(`:2088`) and rests a MUST on that absence at `:2126`; `7f656980` (PR #529,
2026-08-31) added the row and amended no specification. That is a canon/code
contradiction on `main`, and the earlier draft of this packet NAMED it and left
it — a posture that was defensible only while this packet had no stake in it.
It has one: both classes it adds are `contested` BY that row, and its whole
discharge design is built on the row being real. A packet cannot build on a fact
its own capability's promoted text denies and then archive beside it. So the
absence rule is superseded HERE, the protection it bought is preserved as an
obligation on the act that extends the class map, and #529 is regularized by the
successor rather than reverted. **The cost of THIS half of D2 is named
separately**: the packet takes on a carriage obligation it did not have —
thirty-five promoted units, two of them dropped under a marker — and it is met
and measured (§ Impact), not asserted.

**AND THE THIRD `FAMILY_RESOLUTION` MENTION IS ANSWERED RATHER THAN STEPPED
OVER, because the rule just stated would otherwise reach it.** Canon names the
table in three places; the block above supersedes two. The third is `:1726`,
inside the very requirement D2 declines to open — "the family is deliberately
absent from `FAMILY_RESOLUTION`, so its findings are not classified
`contested`". It is not in the same position, and the difference is in the
promoted text rather than in this packet's convenience: `:1726` sits under "This
family SHALL be advisory AT LAUNCH" and the same paragraph RESERVES its own
reversal — "Raising the scenario-completeness arm to `error` and adding the
contested classification are ONE later decision taken together by ruling, and
SHALL follow the discharge of the standing population rather than precede it".
`7f656980` is that decision, taken together and on a measured population of
zero. A launch state whose own requirement provides for leaving it is SPENT when
the reserved act is taken; `:2088` provides for nothing, being an unconditional
SHALL with a MUST resting on it, and that is why it alone is superseded.
**Recorded as a decision, not as an oversight**: a seat that reads it the other
way is asking for the ~290-line restatement D2 measured, and should say so.

**D3 — A THIRD MARKER FORM, not a proposal cross-reference and not a delta
header key.** #502's second question lists three instruments. The proposal
cross-reference is already there in 4 of 4 and is measured over-broad in the same
four packets (two to three unrelated active change ids each), it is per-change
where the fact is per-requirement, and it lives in the document that does NOT
promote. A new key in the delta header would be a fourth declaration grammar for
a corpus that has three. The marker is per-requirement, sits inside the block
that makes the claim, is read by a parser that already exists, and inherits the
whole falsifiability discipline — form not prose, complete prefix, not a carriage
unit. **Its cost is named**: the marker promotes into canon with the requirement
and is then a superseded pairing recorded in a promoted spec. Bounded, because a
marker is not a carriage unit and any later block may drop it declaring nothing,
but real, and OQ-2 below asks whether it should be dropped at promotion instead.

**D4 — Advisory in the half this packet still owns, and NO FLIP IS PROPOSED
HERE. The other half is no longer available, and this decision is re-argued from
that ground rather than from the ground it was drafted on.** Both new classes
carry `warning`, each on its own severity constant. The band argument is
unchanged and stands on its own: the standing population is four, none of it
authored under a rule that existed, and flipping a band onto four packets that
could not have complied is how a check gets dispositioned instead of obeyed. The
flip is one later decision taken by ruling AFTER the four are discharged. What
HAS changed is the second half — "the family stays absent from
`FAMILY_RESOLUTION`" is a posture this packet can no longer adopt, § 7.2's
reserved flip having landed at `7f656980` and taken the family's row with it
(§ Impact). Both new classes are therefore `contested` from their first emit,
and `add-modified-block-currency-check` § 7.2 is SPENT rather than owed. The
packet now says that IN CANON and not only in its own prose: the `doc-health`
MODIFIED block supersedes the promoted sentence that denies the row.

**THE DISCHARGE PATH, WORKED FROM HOW THIS FAMILY'S EXISTING CLASSES DISCHARGE
TODAY, because the marker is this class's whole remedy and a remedy that raises
an `error` is not one.** The estate's answer for a `contested` finding that stops
being emitted is the one `doc-health`'s own contested-finding rule gives — the
resolution cites an OpenSpec change or a recorded human disposition — and two
things follow from it, in this order:

1. **§ 6 IS SEQUENCED BEFORE THE CLASS LANDS, so it launches at a population of
   ZERO.** A finding never emitted never vanishes. The four standing pairs can be
   discharged the moment this packet is ratified: the marker form is defined by
   the `document-lifecycle` requirement here, and adding one is an amendment to a
   ratified proposal rather than a code change. It is also mechanically safe
   before F1 — a `Modified over` paragraph a parser does not yet recognize is
   read as ONE dated bold note, an EXTRA body unit of the block, and the carriage
   arms report units canon carries that a block LACKS, never the reverse. This is
   the discipline the estate already keeps: `promotion-fidelity` and
   `duplicate-packet` each joined `FAMILY_RESOLUTION` only after their measured
   population was discharged, and so did THIS family, on the scenario-title
   arm's own flip two days ago. **`tasks.md` § 6 is
   therefore a PRECONDITION of § 2 rather than a follow-up to it**, and § 2.11's
   named exact set launches empty.
2. **Where sequencing is not available, the citation is — AS AN EXCEPTION THAT
   CARRIES ITS OWN RETIREMENT, not as a second equal route.** A pair arising
   after the class lands, and a nonzero population in one of the repositories
   § 5 measures, cannot be discharged before the first emit. There the act that
   ADDS the marker records the citation in the same act — an entry in
   `health/dispositions.yaml` naming `modified-block-currency`, the repository,
   that delta path AND, narrowing it, the requirement, citing the change under
   which the marker was added.
   **`tasks.md` § 6.4's prohibition is NARROWED, not lifted, and the narrowing is
   what it always guarded**: no disposition may stand IN PLACE OF a marker. A
   citation recorded on the act that lands the marker suppresses nothing — there
   is nothing left to suppress — and is the contested-finding rule's own
   requirement rather than a way around it.
   **AND IT IS BOUNDED IN TIME, because the machinery gives it no boundary of
   its own.** `promotion_fidelity.disposed` is consulted BEFORE the block is
   resolved and matches on family/repo/path with an optional REQUIREMENT
   narrowing — never on a finding class — so an entry recorded for a pairing
   finding suppresses the three comparison arms over that block too, and would
   go on suppressing them AFTER the declared basis archives and the block became
   comparable for the first time. That is the defect family the arms exist for:
   a stale MODIFIED block silently deleting clauses and scenarios that reached
   canon while it sat. The delta therefore requires the entry to be recorded at
   REQUIREMENT grain and RETIRED when the basis archives, makes the retirement
   the archiving change's own act evidenced at its archive gate, and makes the
   modifying change's archive gate confirm that no such entry stands over its
   block. A scenario states the falsification directly: the basis archives, the
   entry remains, and the run's silence is suppression rather than clearance.

**AND THE CONTRADICTION THIS PACKET WILL NOT LEAVE STANDING UNDER ITSELF.** PR
#529 landed the row and amended no specification, so promoted `doc-health` canon
still reads "The family SHALL remain absent from `FAMILY_RESOLUTION`"
(`openspec/specs/doc-health/spec.md:2088`), with its own scenario at `:2126`
requiring that a disappearance "MUST NOT be reported as an uncited resolution,
the family being deliberately absent". **Canon and code contradict each other on
`main` today, and an earlier draft of this section named that and stepped
around it.** Stepping around it is no longer honest, because this packet's whole
discharge design rests on the row being real: both new classes are `contested`
BY it, and a packet that builds on a fact its own capability's promoted text
denies would archive two requirements into one specification that contradict
each other. So the absence rule is SUPERSEDED by this packet's `doc-health`
MODIFIED block (§ What Changes), which cites `7f656980` as the landing, keeps
the protection the absence bought — a finding designed to stop being emitted
must never become an uncited-resolution error for having worked — and re-seats
it on the ACT that extends the class map, on the same grain-and-retirement terms
the pairing class's citation carries. **That is #529 regularized rather than
reverted**, and it is the successor doing what #529's own landing left owed.
**The cost of the veto is named**: vetoing D4 means proposing a band flip onto
four packets authored before the rule existed and, under the row as it stands,
an `error` on the night each of them is corrected; vetoing the supersession
specifically means either reverting the row in code or archiving this packet
beside a promoted sentence its own design contradicts.

**D5 — The COLLISION CHECK is in scope, and it is the decision most worth
vetoing.** #502's fourth question asks what enforces the archive ordering
generically, and the honest answer is that no checker can gate an archive act
from inside a health run. What it can do is read the surviving evidence of the
unsafe order — an active ADDED block for a title canon now carries — which
nothing in the estate reads today. It costs one lookup against an index the
family already builds, its population is ZERO on this tree, and it is in place
before the first instance rather than after, which for this shape matters more
than usual because an archive act cannot be taken back. **The cost of the veto is
named and it is small**: strike the second `doc-health` requirement and § 3 of
`tasks.md`, and the packet still closes holes 1 and 2 and leaves the archive
ordering resting on the normative rule alone — which is where it rests today,
minus the rule.

## Open questions this proposal does not settle

- **OQ-1 — the post-archive detector for the MODIFIED writer's own delta.** Once
  the modifying change archives, its delta is under `archive/` and this family
  reads no archived path; `promotion-fidelity` compares that delta to a canon
  that IS that delta and agrees. The collision check sees the SIBLING's side and
  not the writer's. Whether a third reading is owed is a different document pair
  and, on this corpus's own precedent, a different family. Not decided here.
- **OQ-2 — whether a `Modified over` marker should survive promotion.** This
  proposal keeps it, on consistency with the two existing forms. The argument
  the other way is that a removal marker records a governance act worth keeping
  and a pairing marker records a transient relation that is FALSE the moment the
  basis promotes.
- **OQ-3 — two or more active changes adding one title.** The rule as written
  lets the marker name one of them and reports nothing further. Whether two
  active additions of one requirement is itself a defect — it looks like one —
  is left open; the population is zero today. **STILL OPEN, and the population
  stays zero by this packet's own disposition rather than by luck**: chain order
  leaves exactly ONE `## ADDED` block for the title throughout, so disposition
  (a) creates no second addition, and the conversion clause forecloses the one
  route — an unpaired conversion of a MODIFIED block to `## ADDED` — that would
  have manufactured a second one without a ruling. The question stays open for
  the shape that arrives some other way.
- **OQ-4 — whether the four standing pairs should be repaired by their own
  authors or by one sweep.** Four ratified packets would each gain one marker
  paragraph. `tasks.md` § 6 stages it as a sweep with per-packet consent; a
  council may prefer to route one task to each owner.
- **OQ-5 — the aggregation population.** Fourteen submodules carry
  `openspec/changes/`. This packet measures openxFactory and predicts nothing
  about the rest; § 5 makes that a task, and a large population elsewhere is a
  reason to revisit D4's band before the flip, not after.

## What this proposal does NOT claim

It does not claim the four live pairs are defects. All four are deliberate,
three of the four state their basis somewhere, and what the check adds is that
the pairing becomes declared, per-requirement, and machine-readable. **IT NO
LONGER CLAIMS ALL FOUR ARE BENIGN, and the one that stopped being so is named
rather than averaged back into the four**: the custody /
`add-binding-consumer-identity` pair now carries a scenario that `contract-v2.4`
has FALSIFIED, so its safe-order archive would promote text the repository's own
published schema contradicts unless custody amends it first. The pairing is
still deliberate; what it carries is an amendment owed under the obligation this
packet adds, worked in § The one live pair this rule already disposes.

It does not claim to make the archive ordering enforceable by tooling. It makes
the obligation normative and the pair findable; the act itself stays where
archive acts are, in a human gate reading a report.

It does not claim to reopen the 2026-08-27 ruling against synthesising a basis
from a sibling's ADDED text. Nothing here compares requirement text.

It does not claim to reverse #529 or to re-open the flip that landed with it.
The `doc-health` MODIFIED block RECORDS that landing in canon and supersedes the
one sentence and the one bullet it falsified, keeping the protection they bought
by re-seating it on the act that extends the class map. The row stays exactly
where #529 put it, and the severity `_LAUNCH_SEVERITY` moved to is untouched.

It does not claim to close #330's post-archive half, which stays open, or #318,
whose gap this packet is once again sitting in.

It does not claim to have measured the domain factories. This change's evidence
is openxFactory's own active changes at `7f656980`, re-read at every catch-up
merge as § 4.2 obliges.

And it does not close #502. It is the successor that may close it on archive,
and it says so above rather than doing so here.
