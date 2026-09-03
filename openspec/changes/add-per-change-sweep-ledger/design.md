# Design: add-per-change-sweep-ledger

Status: draft

## 0. The convener brief

Brett Heap ruled the SHAPE on 2026-09-03 (lane `openxfactory-max001`, in
session, on issue #618): *"do 1 and 3, keep the log in one place"*. Item 3 is
this packet. The ruling settles three things and this document decides the rest:

1. the pin becomes a per-change ledger keyed by change id, one row per change;
2. the totals are DERIVED from the rows and asserted against the live sweep;
3. **the MOVEMENT LOG stays ONE hand-written ledger in ONE place** — it is not
   scattered across change directories and it is not generated.

## D1 — ADDED, not MODIFIED: the reading of the requirement

**The question.** `add-sequenced-after-substrate` is ACTIVE (ratified
2026-09-01, realized, not yet archived) and its `release-realization` delta
holds the requirement "Chain-walk policy belongs to the consumer, and its bound
SHALL be measured". If this packet's change is a change to THAT requirement, it
owes a `## MODIFIED Requirements` block restating it in full, and both changes
become co-modifiers, which would make `sequenced_after:` compulsory rather than
elective.

**The reading, taken from the text rather than from the topic.** That
requirement's normative sentences are:

| sentence | what it binds |
| --- | --- |
| "This substrate SHALL declare NO depth ceiling, NO fan-out cap, and NO … composition operator" | the substrate's silence on policy |
| "a consuming gate SHALL declare its own and SHALL record them as OPERATIVE NUMBERS" | the consumer's specification |
| "A GATE'S DEPTH BOUND SHALL BE MEASURED AGAINST HONEST CHAINS RATHER THAN MERELY ASSERTED, and the measurement SHALL be recorded" | that a measurement exists and is recorded |
| "The FIRST corpus sweep after adoption SHALL record the deepest chain it resolves" | that the first reading is recorded |
| "a raise of any gate's ceiling SHALL be a specification change with a recorded disposition" | how a ceiling moves |

**None of them binds the mechanism by which the recorded measurement is PINNED
in a committed check.** The scalar pin is a realization choice, made in that
change's tasks 5.4/5.5 and in `test_sweep.py`'s own prose ("THE LIVE PIN IS THIS
TEST, and only this test"), not in the requirement. After this packet the
measurement is still measured, still recorded, still re-runnable, and the
deepest chain it resolves is still reported — from the rows rather than from a
literal. A MODIFIED block would restate the requirement UNCHANGED, which is what
makes it dishonest rather than merely redundant.

**Decision: `## ADDED Requirements`, one novel title, in `release-realization`.**

**AND THIS DEPARTS FROM THE ISSUE, KNOWINGLY.** Issue #618's "Shape of the
packet" paragraph specified the opposite: *"`sequenced_after:
[add-sequenced-after-substrate]` (it MODIFIES that change's still-active '…bound
SHALL be measured' requirement, so both are co-modifiers and the declaration is
owed)"*. This packet delivers ALL-ADDED, both rows read `class: sole`, and the
declaration is ELECTIVE rather than owed (D2). The issue's paragraph was written
before the requirement's text was read line by line; the reading above is the one
taken here, and it is recorded as a DEPARTURE rather than quietly delivered, so
that ratifying this packet ratifies the departure knowingly. If the convener
prefers the issue's shape, the change is a MODIFIED restatement plus the two
class flips that follow, and it is a different packet from this one.

**What the choice costs and buys, stated so it is not read as convenience.** It
buys the estate's "one requirement, one writer" preference (the shape
`create-medxpractice-overlay-boundary` took when it cited rather than modified)
and it avoids `govern-sibling-added-modified-deltas`' archive-order hold on a
MODIFIED block declared against an active sibling's outcome. It costs the
explicitness of a restatement: a reader of the substrate's requirement is not
told, at that requirement, that the pin mechanism moved. That is paid for in
this delta's preamble and in § The sibling rule, measured of `proposal.md`,
which name the requirement and record the reading — and by the
`sequenced_after: [add-sequenced-after-substrate]` declaration, which makes the
ordered-delta relation MACHINE-WALKABLE even though no rule compels it.

**Doc-health `modified-block-currency` does not arise.** That family attaches to
a `## MODIFIED` block; this delta has none. The question of what a MODIFIED
block against ANOTHER ACTIVE CHANGE'S DELTA (rather than against canon) would
owe is therefore not answered here and is left open: `release-realization` holds
no promoted requirement of this name, so the marker vocabulary — which is
written for a restatement of PROMOTED text — has no obvious referent for that
case.

## D2 — The declaration is made though the packet is sole

Being ALL-ADDED over a novel title makes this change a SOLE modifier at
requirement granularity, so the substrate's rule does not compel
`sequenced_after:`. It is declared anyway, naming
`add-sequenced-after-substrate`, on the substrate's own doctrine that
*declaring must never be worth less than omitting* — and because the relation is
real: this packet exists because that change's realization pinned its
measurement one way, and it changes the pin. The substrate declared its own
parent while itself being sole, for exactly this reason.

Consequences, all of them row-derived rather than pinned: `declaring` moves
1 → 2, `declaring_ids` gains this change, and the DEEPEST DECLARED CHAIN moves
1 → 2 hops (this change → `add-sequenced-after-substrate` →
`add-structured-scope-substrate`), with `deepest_chain_change` moving to this
change. Under the old shape each of those three was a literal in the test and
each would have been a third, fourth and fifth line to hand-edit.

## D3 — The classifier is INDEPENDENT of the sweep, deliberately

`corpus_sweep` is left exactly as ratified. `classify_corpus` walks the corpus
again and `sweep_from_readings` folds the per-change readings into the same
fourteen-field `Sweep`. The test asserts the two are equal field by field.

The alternative — refactor `corpus_sweep` into
`sweep_from_readings(classify_corpus(...))` — is shorter and removes the
duplication, and it was rejected: the equality would then hold by construction
and the test would prove nothing. A classifier bug would silently populate a
ledger that agrees with itself, and the ledger is what every future author
reads. The cost is one extra traversal of a few hundred directories, measured at
well under a second on the live corpus.

**Two derivations, and they are not the same one.** `classify_corpus` reads the
CORPUS; `readings_from_ledger` reads the LEDGER. The check that discharges the
requirement folds the LEDGER's readings and compares them to `corpus_sweep`'s
measurement — that is the pin, with the rows in place of the literals — while
`ledger_problems` ties the two readings together row by row so a failure names
the row rather than the total. A row too malformed to read is REFUSED rather
than defaulted: a defaulted row is an invented reading, and the ledger is what
every later author reads.

**The duplication is bounded and guarded.** The two computations are ~40 lines
each, sit adjacent in one module, and any drift between them fails
`test_the_DERIVED_totals_equal_the_MEASURED_sweep` on the live corpus and on
five synthetic corpora.

## D4 — The row key set, and why each key is there

One row per change id, over the ACTIVE and ARCHIVED corpora both, sorted by
change id, ONE LINE per row.

| key | why it is a row property |
| --- | --- |
| `state` | `active`/`archived` — the sweep's `active`, `archived`, `active_co_modified`, `active_sole` and `prose_headers_archived` all read it per change |
| `class` | `sole`/`co-modifier` — the sweep's `co_modified` and `sole_modifiers`, at requirement granularity. Membership is BOOLEAN: three shared titles with one partner flip a change once |
| `declares` | `absent`, or the declared parents. `[]` is the POSITIVE root claim and is kept distinct from absence, which the whole root-proof doctrine rests on. Feeds `declaring`, `declaring_ids`, `root_claims` |
| `depth` | the longest resolvable declared chain from this change, in hops. Feeds `deepest_chain` and `deepest_chain_change`. **Present only when the change declares** — a change with no declaration has no chain depth, and `0` would read as a resolved root claim |
| `prose` | whether the proposal carries a legacy free-text `Sequenced-after:` header. Feeds `prose_headers` and `prose_headers_archived` |
| `moved_by` | the pull request that last moved this row's derived keys |
| `moved_on` | the date it did |

**Every `Sweep` field is row-derived and none survives as a scalar assertion.**
`change_ids`, `active`, `archived`, `co_modified`, `sole_modifiers`,
`active_co_modified`, `active_sole`, `declaring`, `root_claims`,
`prose_headers`, `prose_headers_archived`, `deepest_chain`,
`deepest_chain_change` and `declaring_ids` are all folds over the rows.

**One reading is left as a FLOOR rather than a pin, and it is named here as
required.** `test_the_live_sweep_records_a_NON_ZERO_deepest_chain` asserted
`deepest_chain == 1` and `deepest_chain_change == "add-sequenced-after-substrate"`.
Both are now derived, and what that test asserts on the live corpus is
`deepest_chain >= 1`. The doctrine at stake in it is that the reading is NO
LONGER "0 hops BY CONSTRUCTION" — a floor states that exactly, and a pin would
re-serialize on every change that declares the field.

**The exact depth is still pinned, and NOT by that test.** It is pinned by the
declaring change's OWN LEDGER ROW, checked in
`test_the_LIVE_corpus_and_the_LEDGER_agree_row_by_row`: setting `depth: 9` on
that row fails THAT test, naming the row, the key and both values. This is
stated carefully because an earlier draft of it was wrong: the deepest-chain
test's second assertion reads `classify_corpus` and never opens the ledger, so
`deepest.depth == sweep.deepest_chain` holds BY CONSTRUCTION of
`sweep_from_readings`. It is kept for what it does prove — that the fold names a
row that DECLARES and reports THAT row's depth rather than some other row's
number — and is labelled in the test as a self-consistency check on the fold,
not a ledger check.

**Absence is spelled `absent`, not `~`.** `sequenced_after:` can carry a null
value (a key with no value), which `read_declaration` returns as `None` and
`validate_shape` refuses; a ledger spelling absence `~` could not tell the two
apart. A declaration is always a sequence, so the bare word cannot collide with
one. Note the conflation the ledger DOES carry, faithfully: the sweep reads a
strict-loader-REFUSED declaration as absence too, because a measurement is not a
gate — `validate-sequenced-after.py` with no flag is where a refusal is
reported, and it stays red independently.

## D5 — One line per row, and the file's shape

A row is one flow mapping on one line. Two changes inserting two rows at two
alphabetical positions produce two non-adjacent single-line insertions, which
git merges without a conflict; a block-style row would spread each insertion
over six lines and widen the window in which two insertions become adjacent
hunks. Sorted order is what keeps the positions apart — an append-ordered file
would put every insertion at one growing tail, which is the failure being
removed.

The file carries `schema_version` and `kind` like every YAML in this estate, a
header comment stating the row grammar and the re-seeding command, and
`seeded_from:` naming the commit the initial seeding read. `seeded_from` is a
HISTORICAL fact and is never updated; `--seed-ledger` preserves it.

**It is read through the strict loader's `StrictLoader`, not `yaml.safe_load`.**
A duplicate change id is the one failure a permissive loader hides:
last-duplicate-wins would show a reviewer the first row and check the second —
the same defect the realization-axis front-matter loader exists to refuse. The
front-matter BYTE CEILING is deliberately NOT applied: it bounds an
authorization surface a human wrote, while this file's size is a function of how
many changes the corpus holds and grows by construction. A ceiling here would
convert corpus growth into a refusal.

## D6 — `--seed-ledger` is a permanent authoring tool, not a one-off script

The seeding is mechanical, and the mechanism is kept rather than deleted after
use, because the same operation is what an author runs to MOVE a row:

```
python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#620'
```

It rewrites the file from the live corpus and stamps `moved_by`/`moved_on` ONLY
on rows whose derived keys actually changed, PRESERVING the provenance of every
row that did not. The diff is then exactly the list of rows the change moved,
which is both the author's answer and the reviewer's. `--ledger-diff` reports
the same finding set without writing anything and exits non-zero when stale, so
the check is re-runnable from the CLI and not only from pytest.

A one-off script deleted after seeding would have forced the first author who
had to move a row after a merge to hand-edit YAML, which is the class of work
this packet exists to remove.

## D7 — The MOVEMENT LOG: one place, new rule, history verbatim

The log stays in `tests/sequenced_after/test_sweep.py`, in a test docstring, as
it always has. Every existing entry is retained VERBATIM — they are the record
of moves that really happened, including the entry that had to correct an
earlier one, and the correction is instructive.

The log moves to the docstring of the test that now carries the live pin
(`test_the_LIVE_corpus_and_the_LEDGER_agree_row_by_row`), because the test whose
docstring held it no longer exists under its old name. That is the same file and
the same kind of home; it is not a scattering.

**The new rule, stated at the head of the log.** An entry is owed only when a
move is NOT explained by the row diff itself:

- a change to the COUNTING METHOD (what `class`, `depth` or `prose` mean);
- a PARTNER'S row moving because of someone else's delta, where the reason is
  not legible from the two rows alone;
- a reading that is not per-change moving;
- a RE-SEEDING of the ledger, or a repair to it.

A move the row diff states — a row added, a row's `state` flipping on archive, a
row's `class` flipping on ratification — owes NO entry. Generating the narrative
from the diff is refused: a narrative that restates the diff is noise that hides
the entries carrying judgement. The seeding entry is added, dated, naming the
commit seeded from and this pull request.

## D8 — Records cite rows

A `Status: record` or verification file citing the sweep cites its own change's
row (or rows) and "the ledger is consistent with the corpus at `<sha>`" — never
a corpus-wide total. Stated in `proposal.md`, in the requirement, and in the
ledger's own header comment, which is where the next author will look.

**`<sha>` IS THE HEAD `--ledger-diff` LAST RAN CLEAN ON, AND IS NOT
`seeded_from`.** The ledger carries `seeded_from`, the commit the file was first
seeded from. It is preserved across re-seeds, so it goes further out of date with
every landing, and the ledger is NOT consistent with the corpus at it — diffing
this branch's ledger at `995c0ad5` reports eleven findings (this change's own row
is extra there, `add-project-repo-schema` has since archived, the deepest chain
was 1 and is 2, …). A record author reaching for the nearest sha in the file
would therefore cite a commit at which the claim is FALSE, while the sentence
read as though it had been checked. `seeded_from` is documented as history in
the header's own FILE KEYS block for exactly that reason, and the requirement
says the cited commit must be one at which the check was actually run and
passed.

**Records already written are NOT rewritten.** Two live packets cite scalar
totals in verification records (`create-medxchart-overlay-boundary`,
`create-medxpractice-overlay-boundary`). Those are historical measurements,
true at the commit they name, and a `Status: record` file is not edited to
match a later mechanism. The guidance is forward-looking.

## D8a — An estate defect this packet ran into, and does not own

`python3 -m pytest -q` (no path argument) fails COLLECTION on `main` with 19
`ModuleNotFoundError: avatar_f0` under `experiments/avatar-brokered-call/`,
independent of this change. CI runs `python3 -m pytest tests/ -q -m
"not postgres"` (`.github/workflows/pytest-suite.yml:414`), which does not reach
that tree. Recorded because a reviewer running the bare command will see red that
is not this packet's; filed separately by the coordinator, and NOT fixed here.

## D9 — What is NOT solved, and is left to the landing window

Two serialization points survive and are left to issue #618's item 1 (the
lane-collision protocol's landing window, amended operator-locally):

1. **The README "OpenSpec Records" block.** Every change-dir pull request adds
   or edits a narrative row, and two rows added at the same position conflict.
   Making that block a derived artifact is a different packet with a different
   cost/benefit, and it is not attempted here.
2. **The rare MOVEMENT LOG append.** Under the new rule most changes append
   nothing, so the collision surface shrinks by construction rather than by
   engineering — but two changes that both owe an entry still collide at the
   tail.
3. **Two NEW rows that sort ADJACENTLY.** Measured on a 159-row base, the size
   of the live ledger, by varying the number of EXISTING rows between the two
   insertion points:

   | existing rows between the two new ones | git merge |
   | --- | --- |
   | 0 (they sort adjacent) | **CONFLICT** |
   | 1 | clean |
   | 2, 3, 4, 5 | clean |

   **ONE INTERVENING ROW IS ENOUGH**, because git needs surrounding context
   lines to treat two insertions as separate hunks and a one-line row supplies
   them. So the residue is narrow and exactly stated: two changes whose ids sort
   with NOTHING between them share one insertion point and still collide.
   Sorted order shrinks the collision surface from "every change-dir pull
   request" to that case, which is the whole of the claim this design makes; it
   does not remove it, the requirement carries a scenario saying so, and the
   remainder is the landing window's.

   (The same measurement on a TWO-row base conflicts at every gap, which is an
   artifact of there being too few context lines to separate any two hunks, not
   a property of the ledger. It is recorded because the first run of this
   experiment used such a base and briefly read as though separation never
   helped.)

**And a merge queue does not address either.** GitHub's merge queue serializes
merges and re-runs CI; it does not resolve a textual conflict. Two branches
editing the same line still conflict, with the queue refusing the second instead
of a maintainer doing so. It was assessed on its own in #618 and rejected there;
nothing in this design depends on it, and adopting one later would compose with
this change rather than substitute for it.
