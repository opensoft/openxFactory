---
code_surface: openxFactory — FOUR artifacts, all under this repository's own tooling and test tree, none of them a neutral contract any consumer pins. (1) `scripts/sequenced_after.py` GAINS a per-change classifier (`classify_corpus`, `Reading`), a fold from those readings back to the existing `Sweep` (`sweep_from_readings`), a field-naming comparator (`sweep_mismatches`), and the ledger's strict reader/renderer (`load_ledger`, `ledger_problems`, `render_ledger`) — the existing `corpus_sweep` is NOT refactored and NOT touched, deliberately, so the two computations stay independent and their agreement is a cross-check rather than a tautology. (2) `scripts/validate-sequenced-after.py` gains `--ledger-diff` (report, exit 1 when stale) and `--seed-ledger` (rewrite, preserving unmoved rows' provenance); `--sweep` output is unchanged. (3) `tests/sequenced_after/corpus-ledger.yaml` is NEW — one row per change id in the active and archived corpora both. (4) `tests/sequenced_after/test_sweep.py` replaces its five live scalar assertions with row-wise ones and keeps its MOVEMENT LOG, verbatim, in the one place it has always lived. NO spec is promoted, no contract bundle member moves, no domain repository is touched, and the measurement itself — what the sweep counts and how — is not changed by one line.
target_release: implemented (the affected repository's main line — openxFactory. Realization = the ledger exists, the pytest gate derives the totals from it and asserts them row by row against the live corpus on every pull request, and `--ledger-diff` re-runs the same check from the CLI. The change archives on merged-plus-green per `release-realization`'s realization archive gate. There is no aggregation-repo release bundle: nothing here is a member of `contracts/manifest.yaml` or of any `contracts/releases/*.digests.yaml` inventory.)
sequenced_after: [add-sequenced-after-substrate]
Status: draft
Proposed: 2026-09-03
Origin: openxFactory issue #618, and Brett Heap's ruling on it the same day, in session, lane `openxfactory-max001`, verbatim: *"do 1 and 3, keep the log in one place"*. Item 3 is this packet; item 1 is a lane-collision-protocol amendment outside this repository. THAT INSTRUCTION IS AN ADMISSION INTO THE PROPOSAL QUEUE AND NOT A RATIFICATION OF CONTENT.
---

# Proposal: add-per-change-sweep-ledger

Status: draft
Proposed: 2026-09-03, on Brett Heap's in-session ruling of the same day — lane
`openxfactory-max001`, verbatim *"do 1 and 3, keep the log in one place"* —
given on openxFactory issue **#618**, which states the problem and rules the
remedy. That instruction supplies the origin and approval pair the
proposal-origin contract requires and nothing more: this packet carries no
ratification citation and owes none, the promoted lifecycle rule requiring one
only for `Status: ratified`.

## Why

**The corpus-sweep pin is right, and the way it is pinned serializes every
change-dir pull request.**

`add-sequenced-after-substrate` (ratified 2026-09-01) requires that a gate's
bound be MEASURED rather than asserted, and that the measurement be RECORDED and
re-runnable. `scripts/sequenced_after.py`'s `corpus_sweep` is that measurement
and `scripts/validate-sequenced-after.py --sweep` is the re-runnable report.
Neither is in question here and neither changes.

What this packet changes is how the measurement is PINNED. Today
`tests/sequenced_after/test_sweep.py` asserts five corpus-wide TOTALS as
literals — `co_modified == 109`, `active_co_modified == 21`,
`change_ids - 1 == 157`, `sole_modifiers - 1 == 48`, `active_sole - 1 == 11` —
plus four more scalar readings (`declaring`, `declaring_ids`, `root_claims`,
the prose-header pair) and a pinned deepest chain. **A total is a shared
mutable, and every change-dir pull request writes to it.** Authoring a change
moves the population; adopting one moves it again; archiving one moves the
active split; and RATIFYING an already-active change moves the co-modified
readings without moving any population count at all, so two pull requests that
look disjoint still collide. Git cannot auto-merge two edits to one assertion
line, so whichever lands second owes a merge-from-main, a re-derived pin, a new
MOVEMENT LOG entry, and re-derived `Status: record` files if it carries any —
one CI window per round.

**The evidence is on the record rather than argued.** Issue #618 records it: PR
#608 needed three merge-from-main rounds on 2026-09-03; #616 went CONFLICTING
the moment #608 and #609 landed; thirteen commits moved the pin between
2026-08-20 and 2026-09-03. The MOVEMENT LOG in `test_sweep.py` is itself the
artifact of that cost — several of its entries exist only to reconcile two
branches' readings of the same corpus, and one entry had to REPLACE an earlier
one because the arithmetic in it went stale between authoring and merge.

**A merge queue does not fix it.** GitHub's merge queue serializes MERGES and
re-runs CI; it does not resolve a textual conflict. Two branches editing the
same assertion line still conflict, and the queue simply refuses the second
rather than the maintainer doing so. That was assessed on its own in #618 and
rejected.

## What changes

**One ledger, one row per change id.** `tests/sequenced_after/corpus-ledger.yaml`
carries exactly one row for every change id in the active and archived corpora
both, SORTED by change id, each row on ONE LINE. A row records what the sweep
reads about that change — `state` (active/archived), `class` (sole/co-modifier),
`declares` (`absent`, or the declared parents, with `[]` kept distinct from
absence as the positive root claim), `depth` (the resolved chain depth, present
only when the change declares), `prose` (the legacy free-text header) — plus
`moved_by` and `moved_on`, the pull request that last moved that row's derived
keys and the date.

**Every total is derived; none is asserted.** `sweep_from_readings` folds the
rows back into the same fifteen-field `Sweep` the measurement produces, and the
test asserts (a) that the derived reading equals `corpus_sweep`'s, field by
field, (b) that the ledger holds exactly the corpus's change ids, (c) that each
row's keys equal the live reading, and (d) that the rows are sorted. Every
failure NAMES the change id — and, for a stale value, the key with the ledger's
reading beside the live one. **An author reads which row to move off the failure
instead of re-deriving a total to find out.**

**A pull request edits its own row.** Two changes authored in parallel insert
two rows at two alphabetical positions and merge without a conflict. A change
whose `## MODIFIED Requirements` block flips an earlier writer from sole to
co-modifier moves TWO rows — its own and that partner's — in the same commit,
which is correct and is exactly what the ledger makes visible. Two pull requests
that really do disagree about one row still collide, and that collision is a
real disagreement rather than a bookkeeping artifact.

**The MOVEMENT LOG stays one hand-written ledger, in one place** — Brett's
constraint, and the one part of the shape that is ruled rather than designed. It
keeps its home in `test_sweep.py` and every existing entry is retained VERBATIM
as history. Only its RULE changes: an entry is owed when a move is NOT explained
by the row diff itself — a counting-method change, a partner's class flipping
because of someone else's delta, a global reading moving, or a re-seeding — and
is NOT owed for a move the diff already states. The seeding entry is added.

**Records cite rows, not totals.** A `Status: record` file citing the sweep
cites its own change's row (or rows) and "the ledger is consistent with the
corpus at `<sha>`", never a corpus-wide total. A total moves whenever anyone
else lands, so a record that quotes one owes re-derivation on every merge from
main; a row moves only when the fact it states about that change moves. Records
already written are historical and are NOT rewritten.

## What this deliberately does not change

- **The measurement.** `corpus_sweep` is not refactored, not re-scoped and not
  re-counted. It is left as the ratified realization of the measured-bound
  requirement, and the new classifier walks the corpus INDEPENDENTLY so that
  their agreement is a cross-check rather than a restatement.
- **`--sweep`'s output.** The re-runnable report the substrate's task 5.4 ships
  prints exactly what it printed before, byte for byte.
- **The synthetic-corpus tests.** Every `tmp_path` test in `test_sweep.py` that
  proves the counting method — requirement-granular co-modification, title
  normalization, the population count across both corpora, declarations versus
  root claims, the deepest chain, the ZERO-EVIDENCE note, the prose headers, and
  that the sweep never gates — is kept unchanged.
- **The residual serialization points.** The README "OpenSpec Records" block and
  the rare MOVEMENT LOG narrative append still serialize, and are left to the
  lane-collision protocol's landing window (issue #618's item 1) rather than
  engineered away here.

## The sibling rule, measured

**This delta is ALL-ADDED, and that is a reading of the requirement rather than
a preference.** The requirement a MODIFIED block would naturally have taken is
`add-sequenced-after-substrate`'s "Chain-walk policy belongs to the consumer,
and its bound SHALL be measured". Its normative text obliges four things: that
the substrate declare no ceiling, cap or composition operator; that a consuming
gate declare its own as operative numbers; that a gate's bound be MEASURED
against honest chains and the measurement RECORDED; and that the first corpus
sweep after adoption record the deepest chain it resolves. **Not one of those
sentences binds the MECHANISM by which the recorded measurement is pinned in a
test.** The scalar pin is a realization choice made in that change's tasks 5.4
and 5.5 and in `test_sweep.py`'s own prose, and this packet changes the choice
without changing the obligation: after it, the measurement is still measured,
still recorded, still re-runnable, and its deepest chain is still reported. A
`## MODIFIED Requirements` block restating that requirement would restate it
UNCHANGED, which is what makes the block dishonest rather than merely redundant.

The delta therefore ADDs one requirement over a NOVEL title, restates no
promoted text, drops none, and owes no `Modified over`, `Removed from canon by`
or `Merged into` marker — the same shape, and the same reasoning, that
`add-sequenced-after-substrate`'s own delta recorded under this heading.

**The declaration is owed anyway, and is made.** Front matter declares
`sequenced_after: [add-sequenced-after-substrate]`. Being ALL-ADDED makes this
change a SOLE modifier at requirement granularity, so no rule compels the field;
the substrate's own doctrine does — *declaring must never be worth less than
omitting* — and this packet is in substance an ordered delta on that change's
outcome: it exists because that change's realization pinned its measurement one
way, and it changes the pin. The substrate declared its own parent for exactly
this reason while itself being sole.

## Ratification

**NOT RATIFIED.** `Status: draft`. Ratification is the convener's separate act
and has not happened. The 2026-09-03 ruling admitted the packet to the queue and
settled its SHAPE (one ledger, per-change rows, the log kept in one place); it
did not ratify this text.
