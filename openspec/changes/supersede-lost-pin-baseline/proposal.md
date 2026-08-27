---
code_surface: openxFactory (`scripts/doc_health/pin_class.py` — the `KnownLoss` row gains `superseding_record` and `discharged`, the new `discharging_record()` reads committed state for the cited record, `PinResult` gains `discharge`, `PinClassReport.lost_awaiting_record` is added and `fully_verified` consults it instead of `lost`, `summary()` reports the split, and one `NON_MEMBERS` row declares the supersession-record path; `tests/doc-health/test_pin_reachability.py` — five added tests, four on fixtures and one on this repository; `openspec/changes/supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml` — the record this change issues, which is the substance rather than the support; `README.md` — the records block. NO change to the declared `PIN_CLASS` rows, the ref set consulted, `known_loss()`'s matching, the retention namespace, `repair_route()`, the probe's verdicts on the readiness surface, the deterministic check family registry `scripts/doc_health/families.py`, the family enumeration or its numerals, `health/dispositions.yaml`, or one byte of the archived record being superseded.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle, measured rather than assumed: `grep`ing every `contracts/releases/*.digests.yaml` inventory for `pin_class` and `test_pin_reachability` returns nothing, so no schema moves, no digest set changes, and no release tag is owed. The archive gate is therefore merge-plus-green on main: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and the declared pin class reporting itself FULLY VERIFIED over a loss that is still declared, still measured and still reported. THE CHANGE SHIPS ACTIVE and archives only after that.
Status: ratified
Ratified: 2026-08-27 by Brett — in-session commission of the filing, selected verbatim from a multi-choice as "Commission the superseding record (Recommended)" and described in that choice as "A small follow-up change: supersede the archived record with one that acknowledges the lost baseline, plus the disposition — restores fully_verified truthfully rather than by silencing." THE CITATION COVERS THE DECISION TO FILE THIS CHANGE AND NOTHING ELSE; the four decisions in § Orchestrator decisions below were taken by the authoring session and are NOT covered by it, nor are the two questions in § Open Questions. The record this citation resolves against is this file, § Orchestrator decisions and § Open Questions. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and clears its three-way floor on all three axes rather than on the one it needs: approver (`by Brett`), date (`2026-08-27`), and a resolvable record path.
Proposed: 2026-08-27
Origin: The one governance act `govern-derived-pin-reachability` uncovered and could not perform. Its § 3.6 found a fourth orphaned pin whose object is gone from every store and every ref, declared the loss with the measurement, named the superseding record it owes, and marked it NEEDS BRETT — because a realization that wrote a superseding record for another packet's archived evidence would be inventing provenance. This packet writes it, on his commission, and builds the one linkage that lets the verification say so truthfully.
---

# Proposal: supersede-lost-pin-baseline

## Why

One committed pin in this repository names a commit that no longer exists
anywhere, and no code change can ever repair it.

`openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/evidence/provider-verification.yaml:15`
records `us3_baseline_commit: 66b14064bbd50d1af4e9585d10f8150f2bc352f0`. The
object is not merely unreferenced — it is absent from every store this workspace
holds, absent from all 573 refs the remote advertises, and the server itself
refuses to hand it over. The record carrying it is immutable evidence inside an
archived packet, so the pin may not be edited to name something reachable;
retention, the route this repository used for its other three orphaned pins, is
impossible because there is nothing left to retain.

That leaves a defect with no repair, and the honest report of it was already
built: `pin_class.KNOWN_LOSSES` declares the loss with its full measurement,
every run reports the site as LOST rather than clean, and the class holds
`fully_verified` at FALSE. What was left owed was the governance act that
answers it — a superseding record stating the loss, what the archived evidence
still verifies without that pin, and what it cannot — plus a disposition for the
standing report. `govern-derived-pin-reachability` recorded both as owed
(§ 3.6, § 5.5) and deliberately performed neither.

**AND THE LOSS TURNS OUT TO BE NARROWER THAN THE PIN IS.** The measurement this
packet owed produced something the declaration did not have: the baseline STATE
is reachable under a rewritten object name, identified by parentage and
corroborated by three counts the superseded record itself states. So the
superseding record is not an admission of a hole. It is the record of what the
evidence still stands on, and of exactly where it now stands on a weaker
warrant.

## What was measured

Every number here was measured on 2026-08-27 in a fresh worktree off
`origin/main` at `175682e2`, and re-measured rather than copied from the
declaration written the day before.

**THE LOSS, RE-MEASURED.** `git cat-file -t 66b14064…` fails with "could not
get object info" — in a worktree sharing the aggregation object store, which is
the store where all three of this repository's RECOVERABLE orphans answer
`commit`, so the failure is a real absence and not a clone artifact.
`git ls-remote origin` advertises 573 refs (406 of them `refs/pull/*`) and 0 of
them match the pin. `git fetch origin 66b14064…` is refused with
`fatal: remote error: upload-pack: not our ref`. No
`005-customer-subject-runtime` ref survives on the remote.
`git ls-remote origin 'refs/retention/*'` returns exactly three refs —
`74022ea5…`, `da9bf3b7…`, `f13a3b60…` — each at the commit its name states, and
none is this pin. **The ref count moved from 566 to 573 in one day and the
answer did not move**, which is the remote living rather than the measurement
decaying.

**THE CAUSE, IDENTIFIED.** Every commit of the landed
`005-customer-subject-runtime` line carries committer date
`2026-07-14T01:08:50+0000` while its author dates spread across the preceding
day — the signature of one rebase rewriting the whole branch at once. The
record was authored before that rewrite and carried through it unchanged, so it
kept naming its pre-rebase parent's object name while the branch that landed
carried the rewritten names. **Nobody failed to publish a retention ref: the
retention namespace was not ruled until 2026-08-27, six weeks later**, and the
rule that a landing re-derives the pins it orphans did not exist either. This
is the oldest instance of the defect class `govern-derived-pin-reachability` was
filed to end.

**THE BASELINE STATE, IDENTIFIED — the measurement that changes the record's
content.** `8f7c99f0db065fb153b7d9498eb1e16b3c3c306b`, subject "Implement US3
v1-to-v2 Hermes migration cutover (Gate G0 checkpoint)", is an ancestor of
`main` and is the PARENT of `e8ae366cda7b5814b73942891837175b5c43d929` — the
commit that added the superseded record, and the commit that record designates
by self-reference as `provider_commit: this-checkpoint`. The US3 baseline of the
US4 checkpoint is its parent by construction. Three independent counts the
superseded record states about its own baseline agree, each re-measured at both
commits:

| The record says | Measured at `8f7c99f0` | Measured at `e8ae366c` |
| --- | --- | --- |
| `catalog_members: 39 # was 34 at US3 baseline` | 34 `contracts` entries | 39 |
| `schema_members: 32 # was 27` | 27 entries of type `schema` | 32 |
| `fixture_cases: 110 # was 79` | 79 `cases` | 110 |

**AND THE ONE LOAD-BEARING CLAIM, RECOMPUTED.** The record's PostgreSQL section
justifies not re-running the both-majors matrix for US4 with
`inventory_intersection: []`, computed in its own comment as "US4 diff vs
66b1406 intersect PG inventory = empty". Recomputed against the identified
survivor, the US4 diff is 62 changed files and contains no PostgreSQL evidence
source: no `.sql` path, nothing under `contracts/hermes-runtime/migrations/`,
and no path matching `postgres`. The 78-member inventory it quantifies over is
declared in no committed artifact, and the two digests that would identify it
(`source_identity_digest`, `matrix_digest`) appear nowhere else in the
repository and are reproduced by no committed generator — **so that half was
never independently checkable at any commit, and its unavailability is not
caused by the loss.** The superseding record says both halves.

**THE DISPOSITION INSTRUMENT, MEASURED RATHER THAN ASSUMED.**
`health/dispositions.yaml` does not exist in openxFactory at all; it lives only
at the aggregation root. Its header states what the doc-health runner does with
it: a CONTESTED family finding absent from the current report is re-emitted as
an `uncited-resolution` error unless an entry cites its resolution, and entries
are matched to findings by the tuple `(family, repo, path)` with a non-empty
`cite`. **Pin reachability registers no check family** — deliberately, and
pinned by a test that asserts `pin_class` appears nowhere in the family registry
— so there is no family, no report finding, and no tuple for a `cite` to attach
to. A disposition file cannot dispose a finding that was never a family finding.

## The mechanism, stated exactly

The declaration already carried the measurement and the outstanding act. It
gains one thing: **the citation of the record that discharges it.**

1. A `KnownLoss` row may name `superseding_record` — path globs, live and
   archived, the same pair every hermes evidence member is declared with, so the
   citation survives its packet's archive — and `discharged`, which states what
   that record established.
2. `discharging_record()` READS committed state at the revision under test,
   finds the record at one of those paths, and requires it to NAME the pin.
   A citation of a record nobody committed, a record later deleted, or a stub
   that never mentions the lost object discharges nothing.
3. `fully_verified` consults `lost_awaiting_record` rather than `lost`. **Its
   own docstring already said this was the question** — "no declared loss
   awaiting its superseding record" — so the property is completed rather than
   redefined.
4. Everything else about a loss is untouched. The verdict stays LOST, the
   measurement is still rendered, the row is still re-measured by the test that
   fails the day the object turns out to be recoverable, and `summary()` now
   states the split — "1 lost (declared unrecoverable, 0 awaiting a superseding
   record)" — so a reader sees both facts at once.

The consequence worth stating: **deleting a row is not a route to a clean
report.** Remove the declaration and `known_loss()` answers None, the pin
reports as an ORPHAN, and the run FAILS on a repairable-defect verdict for a
defect nobody can repair. The only exit is the governance act.

## What this changes

- **The superseding record exists**, at
  `openspec/changes/supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml`:
  what was pinned, why it is unrecoverable, what caused it, the identified
  surviving state and the corroboration for that identification, what
  verification standing the archived record retains, what it loses, what was
  never checkable at any commit, and the disposition.
- **The archived record is not touched**, and the record says so in a field.
- **The class can report itself fully verified truthfully**, over a loss that is
  still declared, still measured, and still reported in every run.
- **Canon gains the discharge rule**, so the next reader cannot conclude that
  deleting a row is the way to a clean class.

## What this deliberately does not change

- **The archived record's bytes.** Not one. Re-pinning immutable evidence would
  make it state something the run that wrote it did not read.
- **The declared class, the ref set, the retention namespace, `repair_route()`.**
  A discharge is not a repair and does not pretend to be one.
- **`health/dispositions.yaml`.** Measured above: it is the wrong instrument for
  a report that is not a family finding. No entry is added there.
- **The deterministic check families and their numerals.** No family is added,
  removed or renumbered, and the enumeration requirement is not restated.
- **`govern-derived-pin-reachability`'s packet, in any way.** Its § 5.5 stays as
  written; this packet is the act it named, not an edit to its record of naming
  it.
- **The PostgreSQL evidence question.** This change re-justifies nothing about
  the both-majors matrix; it records precisely what can and cannot be
  re-derived, and leaves the forward route named.

### Named follow-ups, out of scope here

- **THE 78-MEMBER POSTGRESQL EVIDENCE INVENTORY IS DECLARED NOWHERE.** The
  superseded record quantifies over it and digests it twice, and no committed
  artifact defines it. That is a gap in the hermes-runtime evidence contract
  rather than a consequence of this loss, and it is the reason one claim in that
  record can only ever be corroborated. Worth a packet of its own; not this one.
- **NO OTHER ARCHIVED EVIDENCE RECORD WAS AUDITED FOR THE SAME SHAPE.** The
  declared class covers every committed pin it knows, and the one unrecoverable
  loss is the one declared. A differential audit of the hermes evidence family
  for pins whose keys the vocabulary still does not know is a sweep, not a
  supersession.
- **THE PREFLIGHT HALF OF THE ENFORCEMENT HOME STAYS UNWIRED**, for the three
  reasons the sibling packet's § 5.6 measured. Nothing here changes that
  balance; the discharge mechanism narrows what would be enforced, it does not
  argue for enforcing it.

## Orchestrator decisions, flagged for veto

**OD-1 — THE RECORD LIVES IN THIS PACKET'S `evidence/`, CITED BY A LIVE-PLUS-ARCHIVE GLOB PAIR.**
Rejected: adding a file to the archived packet being superseded (that packet is
closed, and a supersession that reaches into the archive is the edit it is
supposed to avoid); `health/` (that tree holds machine-generated lane records,
and this is a hand-written governance act). The path moves when this packet
archives, which is why the citation is a glob PAIR — exactly how every hermes
evidence member is already declared, so a citation that survives archiving is
the established shape here rather than an invention. **Alternative not taken:** a
Markdown record, which would need no non-member declaration because `**/*.md`
is already excluded as prose. YAML was chosen because the record supersedes a
YAML evidence record, carries the same structured fields, and is read by
tooling that already reads a `status:` field out of committed YAML.

**OD-2 — THE SUPERSESSION RECORD IS DECLARED A NON-MEMBER, WITH A REASON.**
Its subject IS a pin, so every pin-shaped value in it is a citation of another
artifact's derivation claim and none is its own. The module's own error text
offers exactly two conforming options — "declare the member, or declare the file
a non-member with a reason" — and this takes the second. **The alternative was a
dodge and is named as one:** choosing a key outside the sweep vocabulary
(`lost_pin:` rather than `commit:`) would have made the file invisible with no
declaration at all, which is precisely the silent-coverage defect
`us3_baseline_commit` proved. The trade is stated in the row: a future
supersession record that made a derivation claim about itself would go unswept.

**OD-3 — A SPEC DELTA RIDES, ON `doc-health`, ALL ADDED.** The obligation to
issue a superseding record is stated by the pin obligation's own capability and
is neither restated nor modified here. What that obligation does not state is
what the verification does afterwards — and "delete the row" was a real,
available, silencing route to a clean report that nothing forbade. One ADDED
requirement in the capability that owns the verification closes it.
**Alternative not taken:** shipping delta-less as a record-issuance plus code
change. Measured against house convention and declined: **all 107 archived
changes in this repository carry a spec delta**, and the discharge semantics
exist today only in a docstring, which is not where a rule that governs a future
session's judgment belongs.

**OD-4 — THE REGISTER ROW IS READ AS THE DISPOSITION THE PIN OBLIGATION CALLS
FOR.** That obligation asks for "a disposition for the standing finding" without
naming an instrument. Measured (§ What was measured): the disposition file cannot
match a report that is not a family finding. So the disposition is recorded where
the report is produced — in the row, citing the record — and the delta says that
in canon rather than leaving it as an inference. **If Brett reads that obligation
as requiring an entry in `health/dispositions.yaml` specifically, this is the
decision to veto**, and the remedy is small: add the entry at the aggregation
root and cite this record from it. The mechanism here does not conflict with
that; it would make it redundant.

## Open Questions

**Q1 — Should the identification of the surviving baseline state be stronger
than corroboration?** RECOMMENDATION: no, and the record says why. The object is
gone, so tree equality is unprovable by anybody; what stands is parentage plus
three counts the superseded record itself states, any one of which disagreeing
would have falsified the identification. A stronger claim would be a claim the
evidence does not support, and the record labels the warrant rather than
inflating it.

**Q2 — Does the discharge mechanism need a lifetime, so a citation cannot rot?**
RECOMMENDATION: not yet, and the reason is that the citation is re-read on every
run rather than trusted once. A record deleted later stops discharging the loss
the moment it stops being committed, and the acceptance test asserts no
declaration cites a record this repository does not carry. A separate aging rule
would add a clock to a mechanism that already re-measures.

## Impact

- **Affected specs:** `doc-health` (one ADDED requirement, no MODIFIED block, no
  family enumeration change).
- **Affected code:** `scripts/doc_health/pin_class.py`,
  `tests/doc-health/test_pin_reachability.py`.
- **Affected records:** one issued
  (`evidence/pin-loss-supersession.yaml`); one superseded and UNEDITED
  (the archived hermes provider verification).
- **Contract bundle:** none owed, measured.
- **Discharges:** `govern-derived-pin-reachability` § 3.6 and § 5.5, the one
  item that packet marked NEEDS BRETT.
