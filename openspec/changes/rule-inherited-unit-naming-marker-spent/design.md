# Design: rule-inherited-unit-naming-marker-spent

Status: ratified
Ratified by: rule-inherited-unit-naming-marker-spent — 2026-09-12, Brett Heap, "do all as recomended" (record `review/ratification-2026-09-12.md`)
Kind: design

## 0. The brief

openxFactory [#955](https://github.com/opensoft/openxFactory/issues/955),
filed UNCLAIMED at the archive of
`amend-repo-boundary-governance-scope-first-line`
([#958](https://github.com/opensoft/openxFactory/pull/958)) as residue that
packet's `tasks.md` § 6.1 and `design.md` D2b owed and named rather than
decided. Brett Heap directed this lane to CLAIM it on 2026-09-11 at
12:08:24Z, verbatim **"land each when green, archive both when landed, claim
955 and 956"** — a word that COMMISSIONS THE AUTHORING and ratifies nothing.

The question, stated narrowly: **a later amendment of a requirement whose
PROMOTED text already carries a unit-naming marker has exactly TWO options and
there is no third today.** Drop the inherited marker, which this requirement's
own carriage sentence expressly permits, or carry it forward and take an `info`
marker-defect finding on the THIRD ground, because the unit that marker names
is by construction absent from canon (the declared act removed it) and absent
from the block (a block does not restate a retired unit). Canon says which
report fires; canon does not say which option an author OWES.

**D1 was the owner's decision and it could end this packet.** It was put below
as a multiple choice with the recommendation first; option 2 would have been a
re-authoring, not an edit. **BRETT HEAP TOOK OPTION 1** — verbatim *"do all as
recomended"*, recorded on PR #962 at 2026-09-12T15:45:16Z (comment
`5646922185`) — so the packet is amended exactly as encoded below and the
wording stands unchanged; D2b (no marker owed) is confirmed by the same word.

## D0 — the measurement, taken before the design

Taken 2026-09-11 on this clone of `main` @ `38c076d1` and **RE-TAKEN AFTER
EACH OF THE TWO MERGES FROM `main`, the second at `ac688c40`**, through the family's own `derive_units` so
that fenced example markers are never offered — exactly as they are never
offered to a run. Scope: the corpus BEFORE this packet. **EVERY MARKER FIGURE
HELD ACROSS THE MERGE** — 18 markers, 16 unit-naming, 16 spent, 0 partially
spent, 13 requirements, 7 specifications, 641 requirements in 62 promoted
specifications — and the ONE figure that moved is the active-block count,
**29 → 31**, PR #945's landing bringing two further blocks the family reads,
neither of them carrying a marker; the second merge (PR #960's landing) moved
no figure at all, 31 re-measured as 31. The table states the re-taken values.

**THE POPULATION OF THE SHAPE #955 REPORTS:**

| measure | count |
| --- | --- |
| promoted specifications scanned | 62 |
| promoted requirements scanned | 641 |
| markers in promoted specifications | **18** |
| — of `Removed from canon` form | 15 |
| — of `Merged into` form | 1 |
| — of the pairing form | 2 |
| **unit-naming markers (naming at least one unit)** | **16** |
| **of those, SPENT — EVERY unit they name absent from the requirement carrying them** | **16** |
| of those, PARTIALLY spent (some names still present in canon) | **0** |
| promoted requirements carrying at least one spent marker | **13** |
| promoted specifications carrying at least one | **7** |
| active MODIFIED blocks the family reads | 31 |
| — of those carrying a unit-naming marker | 2 |
| marker-defect findings a run raises today | **0** |

**SIXTEEN OF SIXTEEN, AND THAT IS THE CONSTRUCTION RATHER THAN A COINCIDENCE.**
A `Removed from canon` marker declares a REMOVAL, so every unit it names is
gone from the requirement the moment the declaring block promotes. Every
unit-naming marker that reaches promoted canon is therefore spent on arrival,
and every later amender of one of those thirteen requirements faces #955's
choice. **AND NOT ONE OF THEM IS PARTIALLY SPENT**, which is measured in the
same pass rather than assumed: the run classifies a marker only SOME of whose
named units are absent separately and finds NONE, so the ALL-NAMES condition
the block states is the condition this whole population already meets and the
restatement changes the reading of no marker that exists. By file:

| promoted specification | spent unit-naming markers |
| --- | --- |
| `openspec/specs/doc-health/spec.md` | 6 |
| `openspec/specs/repo-boundary-governance/spec.md` | 3 |
| `openspec/specs/neutral-product-pin/spec.md` | 2 |
| `openspec/specs/shared-contract-ownership/spec.md` | 2 |
| `openspec/specs/canonical-contract-migration/spec.md` | 1 |
| `openspec/specs/document-lifecycle/spec.md` | 1 |
| `openspec/specs/domain-descendant-boundary/spec.md` | 1 |

**THE PAIR D2b MEASURED, RE-MEASURED HERE.**
`openspec/specs/repo-boundary-governance/spec.md:34` — *Install repository
scope* — carries exactly one unit-naming marker today, `Removed from canon by
amend-repo-boundary-governance-scope-first-line (2026-09-11)`, naming ONE unit,
and that unit is absent from the requirement's canon text. That packet is the
one that took D2b's measurement and DROPPED the marker it had inherited from
`refresh-install-repository-enumerations`; the marker now standing is its own,
and it is already spent for whoever amends that requirement next.

**AND A SECOND, WHICH IS THIS PACKET'S OWN SUBJECT.**
`openspec/specs/doc-health/spec.md:1588` — *Currency of an active change's
MODIFIED requirement blocks*, the requirement this block amends — carries
`Removed from canon by amend-marker-declaring-nothing (2026-09-10)`, naming TWO
units, both absent from canon. Its five consecutive amendments have each
dropped their predecessor's marker, and the last four say so in terms in their
`AMENDED BY` notes. **The practice is unanimous and unwritten, which is exactly
what #955 reports.**

**THE DEFECT POPULATION IS ZERO TODAY, MEASURED AND NOT ASSUMED.**
`python3 scripts/doc-health.py --single-repo .` on `main` @ `38c076d1` (exit 0)
reports `marker defects: 0 (info)`; the two active blocks carrying a
unit-naming marker at all are `add-chain-attestation` and
`add-composed-view-authoring`, both `Merged into`, each naming one unit that
matches its resolved basis. **So this is a rule written at the moment it costs
nothing**, before the first author pays for its absence — the same shape
`amend-marker-declaring-nothing` and `amend-merged-into-empty-tail-standing`
both landed on.

## D1 — THE VETO POINT, PUT AS A MULTIPLE CHOICE: what canon is to say

**RECOMMENDATION FIRST. OPTION 1 IS ENCODED IN THIS PACKET; OPTION 2 IS
WRITTEN OUT AND NOT ENCODED.**

### Option 1 — RULE THE TWO-OPTION STATE CORRECT (RECOMMENDED, AND ENCODED)

**FIVE SENTENCES, DERIVING AS FIVE CARRIAGE UNITS, ADDED TO THE PARAGRAPH
THAT ALREADY RULES A MARKER NO CARRIAGE UNIT, AND TWO SCENARIOS AT THE END OF
THE BLOCK.** (The two counts are equal, and that is a fix rather than a
coincidence: `split_sentences()` breaks at a terminator followed by WHITESPACE,
so a bold lead-in that closes its emphasis AFTER the period derives together
with the explanation that follows it. The lead-in here closes BEFORE the
period, so the sentence boundary this packet claims is the unit boundary the
family derives — `tasks.md` § 3.11.) In the family's own voice, beside the
carriage sentence rather than in the grounds paragraph, because this is a
carriage rule and a READING of the third ground, not a sixth ground.

**FIVE ENTRIES FOR FIVE UNITS, one per sentence the block adds and in the
order the block adds them**, so that this record, `tasks.md` § 3.6 and the
generated block all enumerate the same five things:

1. **The condition** — a unit-naming marker is SPENT once EVERY unit it names
   has left canon by a declared act, and dropping it is therefore the LAWFUL
   carriage. (Its emphasis closes before its terminator, which is why it
   derives as its own unit rather than merging with 2 — § 3.11.)
2. **What the condition buys the later block** — the act the marker declares
   is complete and every unit it names is gone from the promoted text, so a
   later block SHALL NOT be required to restate it, SHALL NOT be reported for
   omitting it, and loses no record by dropping it, the archived delta named
   above being where that record is read.
3. **The other half of the two-option state** — where a later block carries a
   spent marker forward instead, the THIRD ground reports that marker, and the
   report is THIS CLASS WORKING AS WRITTEN rather than a defect of the later
   author's care, its names matching no unit of the basis (the act removed
   them) and no unit of the block (a block does not restate a retired unit).
4. **What does NOT move** — NO ground is added, NONE is withdrawn and NO
   suppression moves: the count stays at FIVE, a spent name suppresses nothing
   and never has, and both carriage arms are untouched.
5. **The limit** — it is read on a marker EVERY ONE of whose named units has
   left canon and on no other; the third ground being resolved BY NAME, a
   marker that names nothing NEVER REACHES IT, and a marker one of whose names
   the basis still carries is not spent — D6.

**THE CONDITION IS ALL-NAMES AND NOT ONE-NAME, AND THAT IS THE WHOLE OF WHAT
COPILOT'S ROUND ON [#962](https://github.com/opensoft/openxFactory/pull/962)
MOVED IN THIS PACKET.** A marker's tail names units in the PLURAL — four of
this corpus's eighteen promoted markers name more than one — so a condition
written on "the unit it names" reads, on a marker naming one retired and one
still-present unit, as licence to drop a marker that is still doing suppression
work for the name the basis carries. The population was already MEASURED
all-names (D0: sixteen of sixteen, every named unit of every one of them absent,
zero partial), the scenario was already written all-names (*every unit that
marker names has left canon*), and it was the one sentence that was not. It is
now, in all four of its places: the condition, its explanation, the
carried-forward reading and the scope clause.

Plus `#### Scenario: A later block drops an inherited unit-naming marker` and
`#### Scenario: A later block carries an inherited unit-naming marker forward`,
one per half of the rule.

**COST: NOTHING BUT THE WORDS, PLUS ONE ROW OF BOOKKEEPING.**
`code_surface: none`, measured; **no predicate, no template, no finding class,
and no NEW test** — the one test file the diff touches is the
modified-block-currency self-gate's named-subject list, whose row this packet
opened at drafting and whose `==` comparison obliges every lane to name it (D4 below,
`tasks.md` § 3.13); no assertion in that module moves. The packet archives ON
LANDING plus its own task list.

**WHY IT IS RECOMMENDED, in four reasons and not in one.**

- **It matches the shape the owner has just taken twice.**
  `amend-merged-into-empty-tail-standing` ruled a silence correct in canon
  rather than inventing a report for it, on Brett Heap's *"Rule the silence
  correct in canon"* of 2026-09-11; this packet rules a PRACTICE correct on the
  same terms.
- **The durable record already exists**, and canon already says where to read
  it: *"The durable record of a deletion is the archived delta, which is where
  every other archived governance act is read from."* Nothing is lost by
  dropping a spent marker that is not already available where canon points.
- **It is unanimous practice waiting to be written down.** Sixteen of sixteen
  promoted unit-naming markers are spent; the five consecutive amendments of
  this very requirement each dropped their predecessor's; the defect population
  is ZERO. The rule ratifies what every author has already done.
- **It adds no machinery to a class whose whole recent history is grounds
  being added.** Four of the five grounds arrived in the last two weeks. A
  fifth mechanism here would be the fault `amend-marker-defect-reporting`'s D3
  and `amend-merged-into-empty-tail-standing`'s D6 both declined to repeat.

### Option 2 — ADD A THIRD OPTION: a suppression for a DECLARED-act marker (NOT ENCODED)

**WHAT IT WOULD SAY.** An inherited unit-naming marker whose named unit left
canon by a DECLARED act SHALL be resolvable against the archived delta that
declared it, and where it resolves, carrying it forward SHALL NOT be reported —
a THIRD lawful option beside dropping and beside taking the finding.

**WHAT IT WOULD COST, stated so the choice is real:**

- **A CODE SURFACE.** One predicate in
  `scripts/doc_health/modified_block_currency.py` (`suppression()`'s
  name-resolution branch), one `_WHY_*` template so the finding can say why it
  did NOT fire, tests in `tests/doc-health/`, and its own scenario.
  `code_surface:` becomes `openxFactory` and the packet's archive rule changes
  from **on landing** to **merged plus green realization evidence** under
  `release-realization`'s *Realization archive gate*.
- **A NEW BASIS FOR THE CHECKER.** The family today reads the CHECKED-OUT
  tree's promoted spec and active deltas, and canon says so in terms. Resolving
  a marker against `openspec/changes/archive/**` makes it read a third document
  class to decide a suppression — a widening of this family's basis, which its
  own promoted text narrows deliberately ("This family SHALL measure the
  checked-out tree").
- **A FAIL-OPEN DIRECTION.** A suppression that resolves against an archived
  delta suppresses a report; if the resolution is wrong the block is silently
  accepted. The two options canon has today both fail CLOSED — the author
  either drops the paragraph or is told about it.
- **A POPULATION OF ZERO to serve.** Nobody is carrying an inherited marker
  today, so the machinery would ship unused, and the shape it serves is one
  canon already permits an author to avoid with a deletion.

**IF BRETT HEAP PICKS OPTION 2 THE PACKET IS RE-AUTHORED, NOT AMENDED**: a
different `code_surface:`, a different archive rule, a different task list and
a different delta. That is said here rather than discovered at the gate.

### What a veto of the WORDING alone would cost

Vetoing option 1's wording while keeping its direction costs the five added
sentences and the two scenarios and leaves the block empty — there is nothing
else in it, this being a pure addition. The packet would then be closed rather
than trimmed.

## D2 — the marker THIS block owes, and the one it INHERITS

### D2a — owed: NONE, and that is measured

**THIS AMENDMENT RETIRES NO UNIT.** Five sentences — five carriage units — are
appended to the END of one paragraph and two scenarios to the END of the block;
no existing sentence is reworded, moved, split or dropped. `derive_units` over
this block against its basis reads **0 canon units uncarried**, so **no `Removed from canon`
marker is owed and none is written** — which is `document-lifecycle`'s grammar
read directly (a marker declares a DELETION) rather than a marker written for
symmetry with the predecessors.

**THE PARAGRAPH IS RE-WRAPPED AND THAT IS UNIT-IDENTICAL BY CANON'S OWN
RULE** — *"a re-wrapped paragraph compares equal to the same paragraph wrapped
differently"* — proven rather than trusted: both pre-existing units of the
carriage paragraph derive byte-identically on both sides (`tasks.md` § 3.2).

**Rejected: writing a marker anyway.** A marker naming a unit this block does
not remove would be reported on the FIRST ground (it names a unit the block
still carries) or on the THIRD (it names nothing canon has). A marker is owed
by a deletion and by nothing else.

### D2b — inherited: DROPPED, under the rule this block is writing

**THE ORDERED-DELTA PARENT'S BLOCK ENDS WITH A MARKER THAT IS NOT THIS
PACKET'S**: `Removed from canon by amend-merged-into-empty-tail-standing
(2026-09-11)`, naming the one fifth-ground sentence that change retired. This
block does NOT carry it, on this requirement's own rule that a marker is not a
carriage unit in either direction — and, once option 1 is ruled, on the
sentence this very block adds. **It is the first packet in the corpus to drop
an inherited marker under the rule it is itself writing, and the `AMENDED BY`
note says so.**

**BOTH BRANCHES ARE MEASURED ON THIS BLOCK'S OWN BYTES RATHER THAN REASONED
ABOUT.** Run through the family's own `derive_units`, `carried()` and
`suppression()`:

| this block | basis = CANON @ `38c076d1` | basis = the PARENT's outcome |
| --- | --- | --- |
| **marker DROPPED (encoded)** | 1 uncarried-and-unsuppressed body unit; **0 marker defects** | 0 uncarried; **0 marker defects** |
| marker CARRIED (counterfactual) | 0 uncarried-and-unsuppressed; 0 marker defects | 0 uncarried; **1 third-ground MARKER DEFECT** |

**THAT TABLE IS #955'S CLAIM, MEASURED ON THE PACKET THAT REPORTS IT.** Against
the basis this block is written over — the parent's outcome, which is what
canon will carry the moment the parent archives — carrying the marker forward
costs exactly one third-ground marker defect and dropping it costs nothing. The
two options and no third.

**THE ONE ROW THE DROP COST AT AUTHORING WAS DISCLOSED RATHER THAN HIDDEN, AND
IT WAS TRANSIENT.** While this packet was `Status: draft` (before this
ratification), `_arm_ordering` applied no basis override — `release-realization` scopes the two-writers rule to active
RATIFIED changes and this family does not widen it — so the run measures this
block against CANON, where the sentence the PARENT retired is uncarried and
unsuppressed: **one `info` carriage-ledger finding against this delta's own
path, naming one unit**, disclosed in the pull request body rather than
dispositioned. **IT CLEARS ON EITHER OF TWO EVENTS, AND THE FIRST OF THEM TAKES
TWO THINGS AND NOT ONE — WHICH IS WORTH SAYING EXACTLY, BECAUSE THE OBVIOUS
READING IS WRONG.** (a) BOTH WRITERS ACTIVE AND RATIFIED IN THE CHECKED-OUT
CORPUS: `_arm_ordering` takes `ratified = [b for b in group if b.standing ==
_RATIFIED]` and returns NO override where `len(ratified) < 2`
(`scripts/doc_health/modified_block_currency.py:2147-2149`), so ratifying THIS
packet while the parent is still off `main` leaves the group with ONE ratified
writer and the row exactly where it is. The parent must be in the active
corpus AND this packet ratified — the order between them does not matter, the
second of the two is what clears it. (b) The parent ARCHIVING, which needs
nothing of this packet at all: canon becomes the parent's outcome and the
uncarried sentence is gone from the basis → 0. Since the parent (#947) lands
before it archives, the practical sequence is: #947 lands → this branch merges
`main` → ratification clears the row under (a), or #947's archive clears it
under (b), whichever comes first. **Carrying the marker to silence it today would buy
one clean row now at the price of a third-ground defect the day the parent
archives**, which is the trade #955 exists to end.

**THE ROW CLEARED UNDER (b), NOT (a).** The parent archived to
`openspec/changes/archive/2026-09-11-amend-merged-into-empty-tail-standing/`
(openxFactory PR #973, merged 2026-09-11T18:24:42Z) before this packet's own
ratification; this branch's merge of `origin/main` (67b8011f) brought that
archive in, and `--single-repo --family modified-block-currency` read TEN
rows with this one among them at the freeze (`51edde81`,
issuecomment-5636697848) and NINE with this one gone immediately after the
merge, before a single ratification edit was made. The row is removed from
`tests/doc-health/test_modified_block_currency_self_gate.py`'s
`_LEDGER_SUBJECTS` in the same encode.

## D3 — why an OpenSpec change and not a patch

**Because the sentences are PROMOTED, RATIFIED CANON, and this estate has a
standing refusal on exactly this point.** Working rule 3 routes contract,
boundary and policy changes through OpenSpec; `document-lifecycle` makes the
`## MODIFIED` block the instrument; and the precedent is not abstract — Codex
raised a vocabulary defect in a promoted specification on PR #780 and this lane
refused to fix it there, because **amending promoted canon is an amendment
packet's act, on its own ratification**.

**AND THE CHECKER IS NOT WRONG, WHICH IS THE SECOND HALF.** `suppression()`
resolves the third ground by name against the basis and against the block, and
a spent marker's name matches neither. The report it emits is the promoted
sentence working as written. What is missing is a RULING over which of two
reachable states an author owes — and a ruling over a promoted sentence is an
amendment of the requirement, not a change of behaviour. A packet that quietly
`sed`-ed one paragraph of `openspec/specs/` would be the act that refusal
refused.

## D4 — `code_surface: none`, `target_release: implemented`, and what they decide

**`code_surface: none` IS MEASURED.** The two options this packet rules between
are both reachable today with no edit: the third ground already reports a name
matching no unit of the basis and no unit of the block (that is what
`suppression()` does), and DROPPING a marker is the absence of an edit rather
than an edit. No predicate moves, no `_WHY_*` template is added, no finding
class is added and no severity moves. The diff is this packet's directory, one
README row, one per-change sweep ledger row and ONE NAMED ROW IN A SELF-GATE'S
CORPUS LEDGER.

**THE SELF-GATE ROW IS DISCLOSED HERE RATHER THAN LEFT TO THE DIFF, AND THE
READING IS OFFERED FOR VETO RATHER THAN ASSERTED AS A DEFINITION.**
`tests/doc-health/test_modified_block_currency_self_gate.py`'s
`_LEDGER_SUBJECTS` compares the family's `info` population with `==` and never
`<=`, so an active MODIFIED block that opens a row and does not name it reds
the required `pytest-suite` check for every lane, not only for this one — the
assertion's own message says to *"update the named subjects in this module, in
the same commit"*, which is what § 3.13 does. It is read as NOT a code surface
because `release-realization` scopes `code_surface:` to *"the repositories
whose runtime artifacts it changes"* and this edit changes no predicate, no
severity, no threshold and no assertion: it records WHICH SUBJECTS THE CORPUS
CURRENTLY REPORTS, exactly as the README row and the sweep-ledger row do, and
it RETIRES — on the parent's archive, or on this packet's ratification once the
parent is in the active corpus (D2b states the two-writer condition exactly) —
rather than standing as behaviour. There is also nothing left to realize once this pull
request lands, which is the test the realization archive gate actually applies.
**IF BRETT HEAP READS IT THE OTHER WAY, the remedy is one front-matter line —
`code_surface: openxFactory` naming that test module — and the archive rule
becomes merged-plus-green; the packet's text does not move either way.**

**`target_release: implemented` IS CANON'S OWN VOCABULARY, QUOTED RATHER THAN
INFERRED.** `release-realization` *Realization axis declaration*:

> A proposal without the declarations is a doc-only change (`code_surface:
> none`, `target_release: implemented`) by default.

`none` is outside the vocabulary for that field, and this packet does not use
it. (The corpus-wide divergence on that value is another packet's residue and
is not swept here.)

**WHAT `code_surface: none` DECIDES.** Under `release-realization` an empty
code surface archives **ON LANDING plus its own task list** rather than on
merged-plus-green realization evidence. That is why `tasks.md` § 5 is one
archive act rather than a realization group — and **the archive is still a
separate act on a separate word**, at which openxFactory #955 closes.

## D5 — sequencing: the parent declaration, and the sibling search pasted

**`sequenced_after: [amend-merged-into-empty-tail-standing]`.** That change
WAS an ACTIVE RATIFIED writer of THIS requirement AT THIS PACKET'S AUTHORING
(PR #947, `Status: ratified` 2026-09-11, `code_surface: none`) — **IT HAS
SINCE ARCHIVED** (PR #973, merged 2026-09-11T18:24:42Z, to
`openspec/changes/archive/2026-09-11-amend-merged-into-empty-tail-standing/`).
At authoring, two active MODIFIED blocks stood over one promoted requirement
and `release-realization`'s *Ordered deltas and branch vocabulary* obliged the
later proposal to reference the earlier and declare its deltas relative to
that change's OUTCOME. This requirement's own two-writers arm then read that
declaration as the order — **"BY DECLARATION AND NEVER BY DATE"** — and
measured the declaring block against the declared sibling's outcome. The
declaration is UNCHANGED by the parent's archive:
`scripts/validate-sequenced-after.py` resolves a declared parent in the
ACTIVE and the ARCHIVED corpora both (confirmed below), which is why this
packet's own `sequenced_after:` still names the parent by its unprefixed
change id and the corpus ledger now resolves it at `depth: 1`.

**SO THE PRE-TEXT OF THIS BLOCK IS THE PARENT'S BLOCK, NOT CANON'S TEXT.** It
was read with
`git show origin/change/amend-merged-into-empty-tail-standing:openspec/changes/amend-merged-into-empty-tail-standing/specs/doc-health/spec.md`
at **`a6d373e9`** (PR #947's head at authoring; the change had not yet landed,
so `origin/main` did not carry it), sha256
`16031348e476198b185dfbf4a9e391bd468e5124dc530c25e3d94ece14e11030`, 48,507
bytes. `scripts/validate-sequenced-after.py` resolves parents in the ACTIVE and
the ARCHIVED corpora both, so the declaration survives the parent's archive.

**THE DECLARATION STANDS AT BOTH EQUIVALENT SITES** that
`release-realization`'s *Equivalent declaration sites for the ordered-delta
parent declaration* admits: the `---`-fenced realization-axis front matter
above, and — for the whole-token prose match `declarations()` reads — the
change id occurring as a whole token in `proposal.md`'s own § Sequencing.

**THE SIBLING SEARCH, PASTED RATHER THAN SUMMARIZED**, taken on this clone at
`38c076d1` with 39 active changes:

- **Active changes carrying a `doc-health` spec delta**, `ls -d
  openspec/changes/*/specs/doc-health | grep -v '/archive/'` — THREE paths,
  one of them this packet's own: `add-nightly-dashboard-refresh`, this packet,
  and `settle-aging-staging-topics`. Read by HEADING rather than by name:
  `add-nightly-dashboard-refresh` is `## ADDED Requirements` with SEVEN
  requirements, all of the refresh lane (*Ideation-dashboard image refresh
  lane* and six more); `settle-aging-staging-topics` is `## MODIFIED
  Requirements` over *Aging threshold defaults*. **NEITHER IS THIS
  REQUIREMENT.**
- **The requirement key across every active delta:** `grep -rln "Currency of an
  active change's MODIFIED requirement" openspec/changes/ | grep -v
  '/archive/'` returns this packet's own delta and THREE prose mentions that
  carry no delta over it —
  `disposition-codexfactory-floor-relocation-retitle/design.md`,
  `prepare-openspec-1-12-readiness/tasks.md` and
  `disposition-codexfactory-declared-renames/design.md`.
- **Open pull requests, all NINE of them**, each read with `gh pr view <n>
  --json files`: **#947** carries
  `openspec/changes/amend-merged-into-empty-tail-standing/specs/doc-health/spec.md`
  — THIS REQUIREMENT, and it is the declared parent; **#945**
  (`honour-grandfather-dispositions-in-ratified-provenance`) carries a
  `doc-health` delta over *Governed corpus membership and the lifecycle scan
  set*, a DIFFERENT requirement; #960 carries a `review-authority-intake`
  delta, #959 a `roles-authority-model` delta, #594 a `worker-fleet-health`
  delta; and #961, #940, #888 and #518 carry no spec delta at all.

**ONE OTHER ACTIVE WRITER OF THIS REQUIREMENT EXISTED AT THAT SEARCH, IT WAS
DECLARED, AND NOTHING ELSE COLLIDED** — that writer has since archived (PR
#973), as this section's opening now records, and nothing else has since
appeared to collide either.

## D6 — the LIMIT: this reaches a marker every one of whose named units has left canon, and no other

**THE RULE IS KEYED ON THE NAME, WHICH IS WHAT THE THIRD GROUND IS KEYED ON.**
Canon's third ground reports a marker that "names something matching no unit of
the requirement's basis and no unit of the block" — a resolution BY NAME. A
marker that names nothing never reaches it. So the added sentences say, in
terms, that they are read "ON A MARKER EVERY ONE OF WHOSE NAMED UNITS HAS LEFT
CANON AND ON NO OTHER", and say the never-reaches half in the same breath:
"the third ground is resolved BY NAME, so a marker that names nothing NEVER
REACHES IT".

**WHAT THAT LEAVES OUT, MEASURED RATHER THAN GLOSSED:**

- **THE PAIRING FORM.** Its "whole tail being a reason" by construction, it
  names no units at all, and canon already excludes it from the fifth ground
  for that reason. Two of the 18 promoted markers are of this form, neither
  names a unit, and nothing here decides anything about either.
- **A `Merged into` MARKER WHOSE TAIL NAMES NO SUPERSEDED TITLE.** That is
  `amend-merged-into-empty-tail-standing`'s question and it is answered in that
  change's own block, in the grounds paragraph, which this block carries word
  for word: such a marker "is SILENT BY RULE rather than by OMISSION", its
  destination standing complete in its prefix. **This packet neither widens nor
  narrows that by one clause**, and the added sentences point back to the
  grounds paragraph for it rather than restating it.
- **A MARKER ONLY SOME OF WHOSE NAMED UNITS HAVE LEFT CANON.** It is not
  spent, the scope clause says so in terms, and this packet writes NOTHING
  ELSE about it: the five grounds read it exactly as they read any other
  marker, and no obligation to carry it is created here or anywhere — a marker
  is not a carriage unit in either direction and that sentence is untouched.
  The population is ZERO today (D0, measured in the same pass as the sixteen),
  so nothing in the corpus turns on it; if one is ever written, what an author
  owes for it is a later ruling on a later word and not a silence this packet
  is passing off as an answer.
- **#955'S OWN FRAMING IS CORRECTED IN PASSING.** The issue writes "it does not
  reach the PAIRING form" and then describes a `Merged into` marker — but canon
  uses "the pairing form" for a THIRD form, whose whole tail is a reason, and
  the `Merged into` form DOES name units when its tail carries them. Measured
  here: 15 `Removed from canon`, 1 `Merged into` and 2 pairing markers in
  promoted canon, of which 16 name a unit — the 15 removal-form markers AND the
  one `Merged into`. **So the rule is written on the unit-naming PROPERTY and
  not on the removal FORM alone**, because scoping it to `Removed from canon`
  would leave `document-lifecycle`'s own spent `Merged into` marker
  (*Controlled document status taxonomy*, `declare-generated-projection-status`,
  2026-08-28) unruled while its neighbour is ruled, for no reason a reader
  could name. Both populations are now stated apart.

## D7 — what is measured and deliberately NOT taken here

- **THE SIXTEEN SPENT MARKERS IN PROMOTED CANON ARE NOT SWEPT.** They are
  correct records of ratified removals, every one of them, and no promoted byte
  is edited by this packet. The rule speaks to what a LATER BLOCK owes.
- **NO PREDICATE, NO TEMPLATE, NO NEW TEST.** Option 2's machinery is written
  out in D1 and is not built. If it is ruled, it is a re-authoring. (The one
  test file this packet does touch carries no assertion of option 2's and no
  assertion at all that this packet wrote — it is the self-gate's corpus row,
  § 3.13.)
- **`scripts/doc_health/modified_block_currency.py` IS NOT EDITED**, and no
  comment in it goes stale at this promotion: `suppression()`'s third-ground
  branch already describes the behaviour this packet rules correct, in its own
  docstring, and the packet adds no case it does not handle. Checked rather
  than assumed.
- **`document-lifecycle` IS NOT AMENDED.** It owns the marker GRAMMAR — how a
  deleted unit is NAMED — and carries no reporting rule; the boundary
  `amend-marker-defect-reporting` § 2.4 checked in both directions is left
  standing.
- **THE ONE TRANSIENT `info` ROW THIS DELTA RAISED** while it was a draft
  (D2b), before this ratification, was disclosed in the pull request body and
  was NOT dispositioned rather than suppressed. **IT HAS SINCE RETIRED**, on
  the parent's archive rather than on this ratification — D2b's addendum.
