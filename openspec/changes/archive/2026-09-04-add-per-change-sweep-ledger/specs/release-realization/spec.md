# release-realization Specification Delta

This delta ADDS one requirement about HOW A MEASURED CORPUS BOUND IS PINNED. It
changes nothing about WHAT is measured.

`add-sequenced-after-substrate`'s "Chain-walk policy belongs to the consumer,
and its bound SHALL be measured" obliges that a bound be measured against honest
chains, that the measurement be recorded, and that the first corpus sweep after
adoption record the deepest chain it resolves. That requirement is untouched
here, and the reading is recorded rather than assumed: none of its sentences
binds the mechanism by which the recorded measurement is pinned in a test. The
scalar pin was a REALIZATION choice, and this requirement replaces it.

THE DELTA IS ALL-ADDED over a NOVEL requirement title. It restates no promoted
text, drops none, and therefore owes no `Modified over`, `Removed from canon by`
or `Merged into` marker — the same shape, and the same reasoning, that the
substrate's own delta recorded.

## ADDED Requirements

### Requirement: A pinned corpus measurement is carried per subject, never as a shared total
A corpus measurement that a committed check PINS SHALL be carried as ONE ROW PER
MEASURED SUBJECT, and every total a check asserts SHALL be DERIVED from those
rows rather than asserted as a literal. A total is a shared mutable that every
contributor writes: two changes moving two different subjects' readings edit the
same line, cannot be auto-merged, and serialize on each other for one continuous
integration window per round — a cost paid by whichever lands second, repeatedly,
and paid for bookkeeping rather than for any disagreement about the corpus.

THE ROW IS THE UNIT OF THE PIN. A row SHALL record what the measurement reads
ABOUT ITS OWN SUBJECT and SHALL record, as provenance, the pull request that
last moved it and the date. Rows SHALL be ordered deterministically by subject
identity, so that two subjects entering the corpus insert at two positions
rather than at one growing tail. A change SHALL move its own row, and SHALL move
another subject's row in the SAME COMMIT when its own delta is what moved that
subject's reading — a partner flipping class because of this change's delta is
this change's move to make, not a drift for a later sweep to find.

THE DERIVATION SHALL BE CROSS-CHECKED AGAINST THE MEASUREMENT IT PINS, by a
computation independent of it, and the two SHALL be compared FIELD BY FIELD with
the field and both values named on a disagreement. A derivation refactored out of
the measurement it checks agrees with itself by construction and proves nothing;
naming only that "something moved" tells an author to re-derive a total to find
out what, which is the cost this requirement exists to remove.

EVERY FAILURE SHALL NAME THE SUBJECT. A row absent for a subject in the corpus, a
row for a subject that is not, a row whose recorded value differs from the live
reading, and rows out of order SHALL each be reported naming the subject — and,
for a differing value, naming the key with the recorded value beside the live
one.

A VERIFICATION OR RECORD FILE SHALL CITE ITS OWN SUBJECT'S ROW AND THE
CONSISTENCY OF THE LEDGER WITH THE CORPUS AT A NAMED COMMIT, and SHALL NOT cite a
corpus-wide total. A total moves whenever any other contributor lands, so a
record quoting one owes re-derivation on every merge from the main line, for a
number that was never that record's claim.

THE NAMED COMMIT SHALL BE ONE AT WHICH THE CONSISTENCY CHECK WAS ACTUALLY RUN
AND PASSED, and SHALL NOT be a seeding or creation stamp the ledger happens to
carry. A stamp recording where a file came from is preserved as history and goes
further out of date with every landing; citing it would name a commit at which
the ledger is provably INCONSISTENT, while reading as though it had been
checked.

A DATED HAND-WRITTEN NARRATIVE SHALL BE KEPT IN EXACTLY ONE PLACE and SHALL be
appended only where a move is NOT explained by the row diff itself — a change to
the counting method, a subject whose reading moved because of another subject's
delta, a reading that is not per-subject, or a re-seeding of the ledger. Where
the row diff states the move, no entry is owed, and generating the narrative from
the diff is not permitted: a narrative that restates what the diff already says
is noise that hides the entries that carry judgement.

#### Scenario: Two changes move two different subjects' readings
- **WHEN** two changes in flight each move only their own subject's row, and their rows are not adjacent in the ordering
- **THEN** each edits its own row and the two merge without a textual conflict
- **AND** neither is required to re-derive a total the other moved

#### Scenario: Two new subjects sort adjacently
- **WHEN** two changes each ADD a row and their identities sort with no existing row between them
- **THEN** they share one insertion point and MAY still conflict, which the ordering reduces rather than removes
- **AND** that residue MUST be resolved by the repository's landing convention rather than by re-deriving a total

#### Scenario: A change flips another subject's reading
- **WHEN** a change's own delta is what moves another subject's recorded reading
- **THEN** it MUST move that subject's row in the same commit as its own
- **AND** the check's failure MUST name both subjects rather than report a moved total

#### Scenario: The ledger disagrees with the corpus
- **WHEN** a row is missing, extra, or differs from the live reading
- **THEN** the check MUST fail naming the subject, and for a differing value the key with the recorded value beside the live one
- **AND** the derived totals MUST be compared field by field against the independent measurement, naming any field that disagrees

#### Scenario: A record cites the measurement
- **WHEN** a verification or record file cites the corpus measurement
- **THEN** it MUST cite its own subject's row and the ledger's consistency with the corpus at a named commit
- **AND** it MUST NOT cite a corpus-wide total

#### Scenario: A move the row diff already explains
- **WHEN** a change's move is fully stated by the row diff
- **THEN** no narrative entry is owed
- **AND** where a move is NOT so explained — a counting-method change, a partner's flip, a non-per-subject reading, or a re-seeding — a dated entry in the single narrative is owed
