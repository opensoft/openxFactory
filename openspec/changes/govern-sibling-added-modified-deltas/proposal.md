---
code_surface: openxFactory (`scripts/doc_health/modified_block_currency.py` — the marker parser gains a THIRD reserved form, `Modified over`, recognized by a complete prefix like the other two, naming no units and therefore excluded from unit suppression and from the marker-defect check while still being excluded from unit derivation in both canon and block; `sibling_titles` is widened to return the ADDING CHANGE ID beside each `(capability, title)` so the pairing can be named and self-pairing detected, rather than the bare title set it returns today; `fam_modified_block_currency`'s `if status == "pending": continue` is replaced by an emit for the new pairing class, the three comparison arms still NOT running against a pending block; a reader for active `## ADDED Requirements` blocks against the promoted index the family already builds, for the collision class; two new severity constants and two new action constants, named apart so § 7.2's reserved flip of `_LAUNCH_SEVERITY` cannot drag them, which is the module's own stated reason for `_RESOLUTION_SEVERITY`, `_LEDGER_SEVERITY` and `_DRIFT_SEVERITY`; two new `_ArmTemplate` registrations appended to `_ARM_TEMPLATES`; two new `FindingClass` entries in `CLASSES`, inserted before the `unplaced` class so that "the gate-bearing arm reads FIRST" and "the drift class reads LAST" both stay true; two anchored `_CLASS_PATTERNS` entries; and the module's stale numerals — the docstring's class enumeration, "FIVE ENTRIES FOR SIX RULE SHAPES", and the arms-versus-classes counts. `tests/doc-health/test_modified_block_currency_reporting.py` — the class-registry pin, the rule-shapes pin, the verbatim class-row list, the last-row assertions and the `len(block)` pin all move by name. `tests/doc-health/test_modified_block_currency_self_gate.py` — `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree` no longer covers the new classes; a NAMED EXACT SET for the pairing class's four standing subjects joins `_LEDGER_SUBJECTS` under the same movement discipline, and the collision class gets a zero assertion with a positive control. New fixture trees under `tests/doc-health/fixtures/` for each reported state. `specs/022-modified-block-currency-reporting/contracts/report-section.md` — a byte-level contract enumerating the classes four times over, AMENDED by the realization rather than left false. `docs/doc-health.md` — the family paragraph names three arms plus a marker-defect class plus a fifth `unplaced` class and is amended. NO change to any other family, to `Finding`, to `report.render`, to the ranked-plan or finding grammars, to `families.FAMILY_SUMMARIES`, to `FAMILY_RESOLUTION`, to the governed corpus, to the lifecycle scan set, or to any threshold. NO new deterministic check family, so the "Deterministic check families" enumeration and its numerals are untouched and unrestated.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-modified-block-currency-check`, `add-family-enumeration-check` and `add-unclassified-finding-class` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount § Impact predicts and in no other line. The change therefore ships ACTIVE and archives only after the merge — and, because its own MODIFIED block is written over `release-realization` canon rather than over any sibling's addition, its archive is not itself subject to the ordering obligation it adds.
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
and this section re-measures them on this branch's base, `91cf0a46`.

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

**The population, re-measured on this branch's base.** Run with the family's own
`resolve` at `91cf0a46`:

```
TOTAL active MODIFIED blocks: 19
status: {'canon': 15, 'pending': 4}

PENDING pairs — the change that ADDS, and markers on each:
  add-binding-consumer-identity       | credential-contracts     | add-notebook-hosting-credential-custody | markers=0
  add-wallet-carried-review-authority | roles-authority-model    | add-substantive-review-lane             | markers=0
  implement-keycloak-install-repo     | repo-boundary-governance | add-identity-brokering                  | markers=0
  implement-openxpki-install-repo     | repo-boundary-governance | add-trust-anchor                        | markers=0
```

**Four live pairs, zero markers, and every one of the four adding siblings is
`ratified`** — so the whole live population sits squarely inside the antecedent
`release-realization` would have if its antecedent reached ADDED, and the draft
case is prospective rather than populated. **The seats' figure reconciles as
#502 reconciles it, with one correction owed to the appendix:** LQ-C5 cited
eight, the family docstring's historical seven plus #497's own block; LA-C2's
own return says "**Four** blocks, zero markers". Four is the live number and
eight the cumulative one, and the difference is itself evidence that this class
turns over with nothing tracking it.

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
  requirement it modifies is unpromoted.
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
- **No `## MODIFIED Requirements` block on "Currency of an active change's
  MODIFIED requirement blocks" or on "Deterministic check families".** D2 below
  is the measurement that decided it, re-taken against today's canon.
- **No fourth comparison arm, and the 2026-08-27 ruling is not reopened.** The
  new check compares no requirement text; its inputs are the delta's own marker
  and the set of active additions.
- **The implementation lands in this change**, as Speckit features sequenced by
  `tasks.md`, on the precedent its sibling families set.

## Impact

- **Affected specs**: `release-realization` (MODIFIED), `document-lifecycle`
  (ADDED), `doc-health` (ADDED).
- **Affected code**: `scripts/doc_health/modified_block_currency.py`, its three
  test modules, new fixture trees, the byte-level report-section contract, and
  `docs/doc-health.md`.
- **Predicted severity movement: +4 `warning`, 0 `error`, 0 `critical`, 0
  `info`**, measured on this branch's base at `91cf0a46` with the family's own
  resolver: four `pending` blocks, all undeclared, none self-referential, so the
  pairing class reports four and the misdeclared and self-referential states
  report zero. The collision class reports **ZERO — measured, not assumed**: no
  active `## ADDED Requirements` block in this repository names a capability and
  requirement title the promoted specification already carries. A run configured
  `--fail-on error` or `--fail-on critical` is unaffected by construction, and
  the canon-share headline, the per-stage census, the inventory and the catalog
  are untouched because the family reads neither the governed corpus nor the
  lifecycle scan set.
- **Predicted movement from this PACKET's own delta: ZERO, and verified rather
  than argued.** Its one MODIFIED block is over `release-realization` canon, so
  it resolves `canon` and not `pending` and the pairing class cannot reach it.
  Both promoted body sentences and both promoted scenarios are restated
  byte-identical and everything added is new text, so the carriage ledger and
  the scenario-title arm report nothing: run over this tree with the packet
  present, **0 title findings and 0 ledger findings** against
  `openspec/changes/govern-sibling-added-modified-deltas/specs/release-realization/spec.md`.
- **`_LEDGER_SUBJECTS` — the F3 exact set — GAINS NO ROW FROM THIS CHANGE.**
  That set has fallen due three times already (the archive of
  `add-modified-block-currency-check`, then `clean-doc-health-floor` and
  `declare-generated-projection-status` on consecutive days), so the honest
  thing to say is what this packet adds to it, which is nothing: zero ledger
  findings against its own delta means zero rows. What the REALIZATION adds is a
  different constant — a named exact set for the pairing class's four standing
  subjects, under the same movement discipline and with the same retirement
  condition written into it: each row retires when its declaring block carries a
  marker or its adding sibling archives.
- **`FAMILY_RESOLUTION` gains no row.** The family stays absent, which "A
  modified-block-currency finding its own class map cannot place is itself a
  finding" already requires of it and which this change does not disturb; a
  `contested` classification would route a pairing finding discharged by a
  marker into `report.uncited_resolutions` as an `error`, gating through the
  back door on the first block anyone corrected.
- **The "Deterministic check families" enumeration and its numerals are
  untouched and unrestated**, no new family being registered — the same shape
  `add-unclassified-finding-class` and "A declared unrecoverable pin loss is
  discharged by a superseding record" both take, and the reason the
  `family-enumeration` gate stays green through this packet.
- **Measured effect on every other repository: unknown until an aggregation
  run, and deliberately so.** § 5 of `tasks.md` makes that measurement a task
  rather than a prediction; that is why the launch is advisory rather than a
  claim this proposal makes.

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

**D2 — ADDED-only in `doc-health`, and this was measured rather than preferred.**
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

**D4 — Advisory at launch, in both halves, and NO FLIP IS PROPOSED HERE.** Both
new classes carry `warning` and the family stays absent from
`FAMILY_RESOLUTION`. The standing population is four, none of it authored under a
rule that existed, and flipping a band onto four packets that could not have
complied is how a check gets dispositioned instead of obeyed. The flip is one
later decision taken by ruling AFTER the four are discharged, exactly as
`add-modified-block-currency-check` § 7.2 reserves its own — which stays owed and
is untouched by this packet.

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
  is left open; the population is zero today.
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
the pairing becomes declared, per-requirement, and machine-readable.

It does not claim to make the archive ordering enforceable by tooling. It makes
the obligation normative and the pair findable; the act itself stays where
archive acts are, in a human gate reading a report.

It does not claim to reopen the 2026-08-27 ruling against synthesising a basis
from a sibling's ADDED text. Nothing here compares requirement text.

It does not claim to close #330's post-archive half, which stays open, or #318,
whose gap this packet is once again sitting in.

It does not claim to have measured the domain factories. This change's evidence
is openxFactory's own active changes at `91cf0a46`.

And it does not close #502. It is the successor that may close it on archive,
and it says so above rather than doing so here.
