# Staged: a deferred document stays owed — the semantic sweep's carry-over, with its cursor beside the inventory

Status: staged
Kind: capability-proposal
Summary: `add-worker-input-budget` bounds the doc-health nightly's analysis
prompt at 1,900,000 bytes and CAPS AND RECORDS: it packs whole documents in a
deterministic `(repo, path)` order, defers the rest, and names every deferral
in the bundle's `meta.json` and in the dated report. It carries nothing
forward. The semantic sweep keeps no cursor, and its incremental scope is a
content-hash diff against the last committed `health/inventory/<date>.json`,
which `finalize` emits unconditionally, so a deferred document is either
re-selected and deferred again by the same order (measured 2026-09-24, while
the committed baseline stood at 2026-09-04: 219 documents deferred on both
budgeted nights) or, once the baseline advances, dropped from the next
night's selection without ever being analyzed. Brett Heap ruled on 2026-09-26
that the budget packet caps and records, and that the carry-over is this
separate packet, with the cursor as its own committed record beside the
inventory. This topic stages that carry-over: a document that CHANGED
stays OWED until the sweep has actually analyzed it.
Topics: doc-health, semantic-sweep, worker-input-budget, sweep-cursor,
carry-over, deferred-documents, inventory-baseline, incremental-scope,
grounding-share, nightly-report
Repository context: openxFactory owns everything except where the records
land. The `doc-health` capability, the packer and the scope selection
(`scripts/doc_health/semantic.py`), the runner and the report, and the
reusable workflow whose `prepare` job diffs against the newest committed
inventory and whose `finalize` job emits the next one
(`.github/workflows/doc-health-reusable.yml`) are all openxFactory's. The
committed records land in the CALLING repository, `opensoft/xFactory`, whose
thin `doc-health-nightly.yml` calls that workflow; they go under `health/`
through the rolling `doc-health/nightly` pull request, and a cursor
committed beside the inventory would land the same way.
Staging ID: openxFactory:staging:doc-health-sweep-carry-over
Captured: 2026-09-26
Source: Brett Heap's ruling of 2026-09-26, in session to lane
`openxfactory-1` by structured choice, on `add-worker-input-budget` OQ-2,
recorded verbatim under "The ruling" below, on opensoft/xFactory#480
(comment 5850005209, item 3) and as a RULED line on the lane register. The
evidence is that packet's own OQ-2 measurement of 2026-09-24 and the code
read for this fragment on 2026-09-26 at openxFactory `main` `1c6662e7`.
Target capabilities: MODIFIED `doc-health` (a changed document the semantic
sweep's input budget defers stays owed: a sweep cursor committed as its own
record beside `health/inventory/<date>.json` offers it again on the next night
until it is analyzed, and the report states what was carried and for how long)

## Last proposal attempt (round-trip provenance)

<!-- Stays "none yet" until this topic first reaches proposal. On DEMOTE,
     replace every field below with the ACTUAL values from the demoted
     change — never re-blank them; that is the whole point of this slot. -->

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## The ruling

Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

Brett Heap, 2026-09-26, in session to lane `openxfactory-1`, by structured
choice. The RULING NEEDED of 2026-09-24 (opensoft/xFactory#480, comment
5820150177) put `add-worker-input-budget` OQ-2 as three options, stated as
they were put: *(a) cap-and-record here + stage the carry-over packet, (b)
cap-and-record alone, or (c) fold carry-over into this packet* — with a lane
recommendation for (a) and one design constraint, verbatim: *the cursor is
its own committed record beside the inventory (for example
`health/sweep-cursor/<date>.json`, written from the bundle's `meta.json`
`deferred` list in the same report commit), never a field of
`health/inventory/<date>.json`, which `finalize` rewrites unconditionally
every night.*

**Brett chose, verbatim, "Accept both, land #1160"**: both of the packet's
recommendations, OQ-1's and OQ-2's. The record (comment 5850005209, item 3)
glosses the OQ-2 half, verbatim: *"OQ-2, cap-and-record plus the separate
carry-over packet at `ideation/staging/doc-health-sweep-carry-over/` with the
cursor as its own record beside the inventory"*. That is option (a), and this
folder is the packet it names. The OQ-1 half keeps the grounding share at
0.5, which this topic takes as given.

The same ruling set's item 4 (answering comment 5819739722), verbatim
*"Approve, nightly wins"*, rules that opensoft/xFactory#396 lands with the
nightly's content winning, so the committed inventory baseline, held at
`health/inventory/2026-09-04.json` since that day, unsticks once it lands.
This topic does not depend on that; see Claim 3.

## Claims

<!-- Settled context the open questions below should NOT reopen. -->

1. **Cap-and-record is RULED for the budget packet and is not reopened
   here.** `add-worker-input-budget` bounds and records and carries nothing
   forward, by the ruling above. This topic adds the carry-over BESIDE that
   packet and weakens none of its obligations: the budget, the whole-document
   packing, the named deferral, the worker's refusal of an over-budget input,
   and the protection of a deferred document's prior findings all stand.
   FALSIFIABLE BY: a draft of this topic's change that relaxes any of them.
2. **The cursor is its own committed record BESIDE the inventory, never a
   field of it**, the ruled design constraint. `finalize` runs `if: always()`
   and emits `health/inventory/<date>.json` from the full current inventory
   on every run it reaches (`--emit-inventory`), so a cursor folded into that
   file would be overwritten by the next emit. FALSIFIABLE BY: a design whose
   carry-over state is read from, or written into,
   `health/inventory/<date>.json`.
3. **The carry-over is owed whatever the baseline does.** While the baseline
   is stuck, a deferred document is re-selected every night and the
   deterministic packing order defers it again: 219 documents (151 changed
   documents, 68 promoted specs) were deferred on both budgeted nights
   measured, 2026-09-23 and 2026-09-24, against
   `health/inventory/2026-09-04.json`. Once the baseline advances, a deferred
   document leaves the next night's diff and is not selected again until its
   content changes. The first state spends the budget on the same documents
   every night; the second loses the deferred ones silently. Nothing in the
   current design obliges a deferred document ever to be analyzed.
   FALSIFIABLE BY: a code path in `scripts/doc_health/` that reads an earlier
   run's deferral record when selecting or ordering the next run's corpus.
4. **The deferral record the cursor needs already exists.** For every
   held-back document the bundle's `meta.json` carries `repo`, `path`,
   `bytes` and `population` (`corpus` or `grounding`): `pack_within_budget`
   builds that list and `prepare_bundle` writes it. The dated report names
   every deferred document as well. The carry-over consumes that record; it
   does not add a second measurement of what was held back. FALSIFIABLE BY: a
   deferral in a nightly bundle that its `deferred` list does not name.
5. **A carry-over is not capacity.** At share 0.5 each population is offered
   948,920 bytes a night: the 1,900,000-byte budget, less the 2,160-byte
   prompt scaffold, halved. The 2026-09-24 changed-docs selection, 196
   documents costing 5,051,588 bytes at `document_cost`, is about five and a
   third nights of the changed-docs share; the promoted-spec grounding, 127
   specs costing 2,984,532 bytes, is a little over three nights of its own.
   A cursor orders what is owed and makes the backlog visible. It cannot
   drain a corpus that changes faster than the budget sends. (Arithmetic from
   the measured figures, not a measurement of any night.) FALSIFIABLE BY: a
   design claiming a drain time shorter than the owed bytes divided by the
   nightly share.
6. **`doc_health` already has two carry-over precedents, and the semantic
   sweep uses neither.** The neutrality lane's stage-2 selection reads a
   per-document JUDGED-DIGEST state, so an undispatched survivor
   "re-qualifies next run" by staying unjudged (`select_for_review` in
   `scripts/doc_health/neutrality.py`, bounded by `MAX_CANDIDATES_PER_RUN =
   8` in `neutrality_dispatch.py`). The document-catalog baseline persists a
   resume CURSOR, the last locator processed, in immutable shard artifacts
   under `health/document-catalog/baseline/` (`catalog_baseline.py`).
   FALSIFIABLE BY: a cursor, a carried-over count or a judged-state read
   anywhere in the semantic sweep's selection or packing in `semantic.py`.

## Why

<!-- xspec:candidate target=doc-health -->
The semantic sweep's input budget made the doc-health analysis lane work
again. The analysis child had failed every night since 2026-08-30 except the
two 2026-09-02 runs, on a prompt that had outgrown the model's context window;
the sweep now packs whole documents into 1,900,000 bytes and defers the rest,
and because every deferral must be named, nothing is dropped silently within a
night. Across nights, nothing is carried. The incremental scope is a
content-hash diff against the last committed inventory, and `finalize` emits
the next inventory unconditionally, so what becomes of a deferred document is
decided by the report cadence rather than by the sweep. While the committed
baseline stood at 2026-09-04 the same documents were re-selected and deferred
again every night (219 on both budgeted nights measured); once the baseline
advances, a deferred document leaves the diff and is never selected again
until someone edits it. The packing order is `(repo, path)`, so the deferred
documents are the same ones every time: at the built share of 0.5, none of
openxFactory's 109 changed documents and one of its 66 promoted specs were
sent on the 2026-09-24 inventory, and no share repairs that, because the order
causes it. A document the report names as deferred every night and nothing
ever sweeps is a finding the sweep will never make. The sweep needs to
remember what it owes.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=doc-health -->
The semantic sweep gains a SWEEP CURSOR: a committed record, separate from the
inventory and delivered in the same report commit, of every document the sweep
still OWES: one that changed, was selected on some night, and has not been in
a completed analysis since. Each night's selection is what its scope selects
today, together with every document the previous cursor carries that is still
in the inventory; a full-sweep night enrols only the deferred documents that
also changed since the previous inventory, so the owed set never grows into
the corpus. Within each population's reserved share the packer offers owed
documents first, oldest deferral first, then tonight's newly changed documents
in `(repo, path)` order, first fit and whole documents only, as now. An owed
document larger than the whole usable budget, which no packing can ever send,
is recorded as OVERSIZED instead: named in every report and left out of the
queue until its content or the budget changes. One larger only than its
population's share stays owed and queued for the packer's third phase, and is
reported apart. The next cursor is whatever is still owed after the night. A
document leaves the cursor only when the analysis worker completed on a prompt
that contained it, so a night whose sweep was skipped or failed discharges
nothing, and everything that night would have enrolled stays owed, sent or
not. A document whose content changes while it is owed is owed once, keeping
its first deferral date; a document deleted from the inventory leaves the
cursor with the reason recorded. Promoted specs deferred from the grounding
population are recorded too, but they rotate rather than accrue debt: last
night's deferred specs are offered first in tonight's grounding phase. The
report states how many documents were carried in, how many were discharged,
how many are still owed, and how many nights the oldest has waited. The cursor
never enters `health/inventory/<date>.json`, and the inventory's meaning, the
snapshot both passes report against, does not change.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=doc-health -->
- Affected specs: `doc-health` (MODIFIED, *Sweep sequencing and snapshot
  consistency*: its changed-docs set is "derived from inventory hash diffs
  against the previous report" and gains the carried set; and the budget
  packet's *Bounded worker input budget*, once promoted, whose deferral
  record becomes the cursor's input).
- Affected code: `scripts/doc_health/semantic.py` (the selection and the
  packing order), `scripts/doc_health/runner.py` (a cursor input and
  output), `scripts/doc_health/report.py` (the carried line), and
  `.github/workflows/doc-health-reusable.yml` (`prepare` reads the newest
  committed cursor beside the inventory it already reads; `finalize` writes
  the next cursor into the report commit), with tests under
  `tests/doc-health/`.
- Records: one new dated file per night beside `health/inventory/` in the
  calling repository, for example `health/sweep-cursor/<date>.json`,
  immutable per date like the inventory and the report.
- Not affected: the budget, the grounding share (ruled 0.5), whole-document
  packing, the finding families, the finding contract, the worker's refusal,
  the job envelope, the inventory's content, and the catalog and neutrality
  lanes.
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

<!-- Free-form thoughts that have not earned a claim, a question, or a
     proposal line yet. Anyone — human or agent — may append. -->

- The honest name for the record is an OWED SET, not a cursor. A cursor is a
  position in an ordered walk (the catalog baseline's `start_after` is one);
  what the sweep needs is a set of documents with a debt against each. The
  word "cursor" stays because it is the ruling's word, and the record keeps
  a path that says so. — Added-by: Claude Opus 5.5 (lane openxfactory-1) ·
  2026-09-26
- The neutrality lane's judged-digest state is the tempting other shape:
  record the content hash each document was last ANALYZED at, and select
  every document whose current hash differs. Deferral, a failed night, and a
  stuck or jumping baseline would all fall out of one rule. It is recorded as
  the road not recommended in Q1, not a rejected one, because it REPLACES
  the incremental scope's basis instead of adding to it. — Added-by: Claude
  Opus 5.5 (lane openxfactory-1) · 2026-09-26
- The deterministic order is doing two jobs, and the carry-over should take
  one of them away. Determinism makes a night reproducible (the budget
  packet's repack rebuilt both nightly prompts byte for byte); `(repo, path)`
  is only the tiebreak that achieves it. Oldest-owed-first is just as
  deterministic given the cursor, and it stops the alphabet deciding which
  repository is never swept. — Added-by: Claude Opus 5.5 (lane
  openxfactory-1) · 2026-09-26
- A report line is the cheapest instrument this topic owns. Owed count,
  discharged count and oldest-owed age, each night, would show whether the
  budget keeps up with the corpus long before anyone asks whether the share
  or the budget is wrong. — Added-by: Claude Opus 5.5 (lane openxfactory-1) ·
  2026-09-26

## Conflicts

<!-- Honest tensions this topic has NOT resolved: with another staged
     topic, with a promoted spec, with itself. -->

- **This topic modifies a requirement the budget packet is still
  modifying.** `add-worker-input-budget` is `Status: draft`, its two deltas
  unratified (its task 0.4), and it MODIFIES *Sweep sequencing and snapshot
  consistency*, the requirement this topic has to modify again. Two changes
  holding MODIFIED blocks over one requirement is the collision the
  MODIFIED-block currency check exists to catch. The resolution is
  sequencing, not drafting: this topic's change is proposed after that
  packet archives, and it modifies the promoted text. — Added-by: Claude
  Opus 5.5 (lane openxfactory-1) · 2026-09-26
- **The Hermes-owned scope set names no carry-over.** *Hermes-layer sweep
  scope resolution* makes scope Hermes-owned policy chosen from
  `incremental | full-weekly | full-nightly`. The budget packet had to
  reconcile a second axis NARROWING the swept set that no scope value names;
  a carry-over WIDENS the swept set beyond tonight's diff on an axis no scope
  value names, the mirror image of the same conflict. Q6 takes the position
  that the carry-over is an obligation of whichever scope was chosen, not a
  fourth value, but until a change states that, the contradiction with the
  promoted text is real. — Added-by: Claude Opus 5.5 (lane openxfactory-1) ·
  2026-09-26
- **Owed documents compete with tonight's changes for one fixed share.**
  Oldest-first bounds how long a document that fits its share stays owed,
  and only while the corpus changes more slowly than the share drains it
  (Claim 5; Q3 reports apart the documents too large for their share, and
  takes those too large for the whole budget out of the queue). A night
  with more changed bytes than the share puts new changes behind old debt.
  Nothing here resolves that; it is recorded so the change carries a report
  line for it instead of an assumption. — Added-by: Claude Opus 5.5 (lane
  openxfactory-1) · 2026-09-26
- **The cursor inherits the report's landing cadence.** It lands in the same
  rolling `doc-health/nightly` pull request as the inventory, and that pull
  request stayed open from 2026-09-10 until at least 2026-09-26
  (opensoft/xFactory#396). While a report commit is unlanded, cursor and
  inventory go stale together. They stay consistent with each other, which
  is the point of landing them together, but a night's `prepare` reads the
  newest COMMITTED pair, so the carry-over is only as current as the last
  landed report. — Added-by: Claude Opus 5.5 (lane openxfactory-1) ·
  2026-09-26

## Open questions

<!-- The section read most closely. Every question gets all four
     sub-fields below, in this order, even when the answer feels
     obvious — "obvious" is exactly when a wrong disposition ships
     silently. -->

### Q1. What does the cursor record: the owed set, or the swept state?

Context: The ruling fixes WHERE the record lives, as its own record beside
the inventory, and the recommendation it accepted gave an example:
`health/sweep-cursor/<date>.json`, written from the bundle's `meta.json`
`deferred` list. Two shapes satisfy that. An OWED SET lists each document
still owed, with its population, the content hash it was selected at, and
the date it was first deferred. A SWEPT STATE records every document's
content hash as of its last completed analysis (the neutrality lane's
judged-digest shape), and the owed set is derived as every document whose
current hash differs.
Recommended answer: The OWED SET: one entry per owed document carrying
`repo`, `path`, `population`, the `content_sha256` it was selected at, its
`first_deferred` date and `nights_owed`, written from the deferral record
and the night's outcome, and read as an addition to tonight's diff.
Explanation: It is the shape the ruling's example names. It leaves the
incremental scope's basis, the previous report, exactly as promoted and ADDS
to it, and it stays small: hundreds of entries rather than the whole corpus.
The swept state is cleaner in one respect, since deferral, failure and a
jumping baseline all fall out of one rule, but it replaces the scope's basis
rather than extending it, reopening a promoted requirement further than the
ruling asked, and it commits a whole-corpus record every night. The owed set
gets the same failure safety from Q5's rule, at the cost of one branch.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

### Q2. Which population does the cursor carry: changed documents only, or promoted specs too?

Context: The packer defers from two populations. A changed document is the
sweep's SUBJECT. A promoted spec is grounding: the finding contract drops
any finding outside the swept corpus, so a spec owes no analysis of its own.
But the deterministic order defers the same specs every night, so
`semantic-contradiction` is never grounded against the late-sorting ones: at
the built share of 0.5, one of openxFactory's 66 promoted specs was sent on
the 2026-09-24 inventory.
Recommended answer: Changed documents are OWED and carried until analyzed.
Grounding deferrals are recorded in the same cursor but ROTATE: the specs
deferred last night are offered first in tonight's grounding phase, and they
never accrue debt.
Explanation: Owing a spec would let grounding debt compete with subject debt
for no finding a spec could ever produce. Ignoring grounding deferrals would
leave the contradiction check blind to the same specs forever, which is the
`(repo, path)` effect that the budget packet's OQ-1 measurement found no
share repairs. Rotation offers every spec within about four nights at
2026-09-24 sizes (2,984,532 bytes of specs, a little over three nights of
the grounding share) without creating a debt.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

### Q3. In what order does the packer offer owed documents against tonight's newly changed ones?

Context: Within each population's share the packer walks first fit in
`(repo, path)` order. With a cursor it has two groups to order: documents
owed from earlier nights and documents newly changed tonight. The order
decides who waits when the share is short (Claim 5). Two kinds of document
fall outside any ordering. One whose own `document_cost` exceeds the usable
budget (the budget less the prompt scaffold, 1,897,840 bytes today) can
never be sent at all. One whose cost exceeds only its population's reserved
share (948,920 bytes at 0.5) can be sent only by the packer's third phase,
on a night when everything else packed leaves at least its cost unused;
while the grounding population (2,984,532 bytes of specs) fills its own
share, that night does not come. Either way `_pack_first_fit` defers it
whole and walks on, which is the budget packet's required behaviour.
Recommended answer: Owed documents first, oldest `first_deferred` first with
`(repo, path)` as the tiebreak; then tonight's newly changed documents in
`(repo, path)` order; first fit throughout, whole documents only, as today.
An owed document whose cost exceeds the usable budget leaves that queue. The
cursor records it as OVERSIZED with its size, the report names it every
night as a document the sweep cannot reach at this budget, its prior
findings stay protected exactly as a deferred document's are, and it is
looked at again only when its content changes or the budget does. An owed
document larger than its share but within the usable budget stays owed and
queued, because the third phase can still send it, but the report names it
apart with its own age instead of letting it set the oldest-owed age. A
promoted spec in either position is named the same way, though it owes
nothing.
Explanation: Oldest-first bounds how long a document that fits its share
stays owed, whenever the backlog drains at all, and given the cursor it is
exactly as deterministic as the current order, so a night stays reproducible
from its inputs. The other two kinds have no such bound under any order: the
packer defers them and moves on, deliberately. One that can never fit would
sit at the head of the queue forever. Its remedy is a human act (split the
document, or change the budget), not waiting, so it is named instead of
queued. One larger than its share can still go out on a light night, so it
keeps its place, but its wait measures the other population's demand, not
the backlog, so it is reported apart and the oldest-owed age keeps meaning
what it says. Newest-first would starve the backlog the way the alphabet
does now, and interleaving adds a policy dial nobody has asked for. Where
the share is too small for the owed set, tonight's changes wait, and the
report's oldest-owed age is what makes that visible rather than silent.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

### Q4. Where does the cursor live, and which job writes and reads it?

Context: The ruling says beside the inventory. The inventory is
`health/inventory/<date>.json` in the calling repository, emitted by the
reusable workflow's `finalize` job and delivered by the rolling
`doc-health/nightly` pull request; `prepare` reads the newest committed
inventory as its diff basis.
Recommended answer: `health/sweep-cursor/<date>.json` in the calling
repository. `finalize` writes it into the same report commit as the
inventory and the report, and `prepare` reads the newest committed cursor,
so the two are always read as a pair. A same-day rerun redirects the cursor
to a temporary path, exactly as it does the inventory and the report.
Explanation: Landing cursor and inventory in one commit means they can never
describe different nights. If the report pull request does not land,
neither advances, and the next night recomputes from a consistent older
pair. A cursor committed anywhere else could run ahead of, or lag behind,
the baseline it is read against.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

### Q5. What does a night whose sweep was skipped or failed do to the cursor?

Context: `finalize` runs `if: always()`, and a failed or missing worker
artifact becomes a recorded skip reason in the report
(`--semantic-unavailable-reason`). The deferral record names only what the
PACKER held back. A document sent to a worker that then failed was never
analyzed either, which was the shape of every night from 2026-08-30 to
2026-09-21 except the two 2026-09-02 runs.
Recommended answer: A document is discharged only when the analysis worker
COMPLETED on a prompt containing it. On a skipped or failed night nothing is
discharged, and every document the night would have enrolled joins the owed
set whether it was sent or deferred: on an incremental night, everything it
selected; on a full-sweep night, the changed documents only (Q7).
Explanation: A cursor written from the deferral list alone would, on a
failed night, silently drop everything the packer DID send: the same silent
loss the budget packet was filed to end. The skip reason is already in hand
at `finalize`, so the rule costs one branch.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

### Q6. Is the carry-over a fourth Hermes scope value, or an obligation of the scope already chosen?

Context: *Hermes-layer sweep scope resolution* makes scope Hermes-owned
policy chosen from `incremental | full-weekly | full-nightly`. A carry-over
widens the swept set beyond tonight's diff on an axis no scope value names
(Conflicts).
Recommended answer: An obligation of the chosen scope, stated in *Sweep
sequencing and snapshot consistency*: a document that CHANGED since the
previous inventory, and that a night selected and did not analyze, stays
owed until it is analyzed, whatever the scope. On an incremental night
everything the scope selects changed; on a full-sweep night only the changed
ones are enrolled (Q7). No new scope value.
Explanation: A scope value answers which documents a night selects. The
carry-over answers whether a changed document that was selected and not
analyzed has been discharged, which is a different question. As a scope
value, a Hermes layer could turn it OFF, and that would reinstate the silent
loss as policy. Tying the obligation to change rather than to selection is
what lets a full sweep offer the whole corpus without making all of it owed.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

### Q7. Does the weekly full sweep enrol its own deferrals in the owed set?

Context: On the weekly day the selection is the whole governed corpus. The
budget packet's 2026-09-24 repack of a Sunday sweep over that inventory
found 738 governed documents costing 9,416,787 bytes, of which 127 are sent
at share 0.5.
Recommended answer: Only the changed ones. A full sweep reads the cursor
like any other night, offers owed documents first and discharges whatever it
analyzes, and it enrols a deferral only where that document is also in the
night's incremental diff against the previous inventory, meaning the
document actually changed. The rest of the corpus it offered is not
enrolled.
Explanation: A full sweep selects everything, not only what changed.
Enrolling all of its deferrals would add roughly 8.5 MB, about nine nights
of the changed-docs share, every seven days (arithmetic from the figures
above), so the owed set would become the corpus, never drain, and bury every
weekday's changes behind it. Enrolling none would lose a document that
changed the day before the full sweep and was deferred on it, because the
next night's diff runs against an inventory that already holds its new
content. Enrolling exactly the changed deferrals keeps the one invariant
this topic exists for: every changed document stays owed until it is
analyzed.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

### Q8. What seeds the first cursor?

Context: The baseline stood at `health/inventory/2026-09-04.json` through
every budgeted night measured, and opensoft/xFactory#396 is ruled to land,
which advances it in one step. At that moment every document deferred under
the stuck baseline leaves the diff; a cursor that ships later and starts
empty never learns they were owed. The budgeted nights' `semantic-sweep-bundle`
artifacts live in the calling repository and expire 90 days after each run
started, the repository default the reusable workflow's own comment records.
Recommended answer: Replay the cursor's own rule over every retained
budgeted night, oldest first, from the recorded bundles and each night's
recorded sweep outcome. For the case in hand that reduces to the deferral
list of the last night selected against the stuck baseline. If no budgeted
bundle is retained, start empty and say so in the first report.
Explanation: A seed replayed from recorded artifacts is exactly as grounded
as every later cursor, with nothing recomputed or remembered by hand.
Starting empty would forget precisely the documents this topic was raised
for. An expired seed is reported rather than reconstructed, because a
guessed owed set would be a claim the evidence does not carry.
Disposition status: open
Added-by: Claude Opus 5.5 (lane openxfactory-1) · 2026-09-26

## Exit

One OpenSpec change MODIFYING `doc-health`, proposed only after the budget
packet this topic was split from has archived, since its deltas are the text
this change modifies. The realization is in openxFactory (the packer's
selection and order, the runner, the report, and the reusable workflow's
`prepare` and `finalize`), and the first cursor lands in the calling
repository's report commit. The proposal gate is every open question above
carrying a disposition other than `open`.
