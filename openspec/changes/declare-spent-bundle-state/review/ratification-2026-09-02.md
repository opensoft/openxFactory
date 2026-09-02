# Proposal Ratification: declare-spent-bundle-state

Status: ratified
Decision date: 2026-09-02
Ratifier: Brett Heap (openxFactory repository owner) — in session, recorded on
PR #578
Ratified: 2026-09-02 by Brett Heap (repository owner) — in session, in TWO ACTS
over the two decisions this proposal declined to take by silence, then the
ratification of the packet on that basis; record: this file.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `tasks.md`, `.openspec.yaml`, this record, and the
single spec delta `specs/doc-health/spec.md`. **THE SPEC DELTA IS NOT
BYTE-UNCHANGED FROM THE TIP HE READ, AND THAT IS STATED FIRST RATHER THAN
BURIED.** Tip `2b66096c` was the tip the ruling was given over. Two Codex **P1**
findings on that tip moved normative text in the delta before this commit —
§ *The two P1s, taken into the requirement* — and both are NARROWINGS of what
was ruled rather than departures from it. The ratified baseline is therefore
this commit, and the difference from `2b66096c` is enumerated below rather than
left for a reader to diff.
Gates at the ratification commit, which are the COMMIT'S gates and not
`tasks.md` § 2's realization gates or § 5's archive gate:
`OPENSPEC_TELEMETRY=0 openspec validate declare-spent-bundle-state --strict`
VALID, and `--all --strict` **85 passed / 0 failed**;
`python3 scripts/proposal-support.py . verify declare-spent-bundle-state` ok;
`pytest tests/doc-health` **1384 passed / 0 failed** locally, and
`pytest tests/sequenced_after` **118 passed**. CI at `2b66096c`:
`merge-master-approval`, `signed-execution-chain-gate` and `wallet-validation`
**PASS**; `pytest-suite` **1 failed, 8620 passed** — the ONE failure being the
inherited #575 red, measured and proven not to be this packet's
(§ *The one red test*).

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER**, over the one
`## MODIFIED Requirements` block on `doc-health`'s promoted requirement
`Release-tag publication` — twenty-four scenarios, eleven of them canon's.

**Ratification authorizes realization and performs none of it.** `tasks.md`
§ 2 — the changelog declaration for `contract-v2.6`, the reader, the acceptance
ladder, the emits, the tests — is the realization slice and is NOT built by this
act. **No line of `scripts/doc_health/release_tag_publication.py` moves in the
ratifying commit, no test of the new scenarios is written, and no SPENT
declaration is authored anywhere.** OD-8 is the decision that makes that so, and
it is the reason this record exists on a PR whose own `pytest-suite` is red: the
packet describes the fix and performs none of it.

## The chain of authority, as SEPARATE ACTS

Recorded as a chain because no single act in it authorizes what the next one
does, and reading any of them as covering the others is the failure this estate
records against itself most often.

1. **The defect was DECLARED by a release cut, not discovered by a reviewer.**
   The `contract-v3.0` cut — PR **#573**, squash `ff9ed815`, 2026-09-02T07:59Z —
   met the collision while landing, wrote it in full in
   `contracts/CHANGELOG.md` § `contract-v3.0` (subsection *"`contract-v2.6`
   disposition — DECLARED, NEVER VERIFIABLE, NEVER PUBLISHED, SUPERSEDED
   HERE"*), and **filed issue #575 rather than relaxing the check inside a
   release cut**: *"a release cut quietly relaxing the one check that exists to
   stop bundles being walked away from is precisely the failure that check was
   built for."* The measurement of record for the bundle's unverifiability is PR
   **#565** comment `5502452624`, cited by everything downstream and re-derived
   by none of it.
2. **The SUPERSESSION ruling.** Brett Heap, 2026-09-02, in session, verbatim as
   quoted in #575: **"Supersede: v3.0 is the completion."** That act disposed of
   `contract-v2.6`. It said nothing about a checker, and #573's entry says so in
   terms: the shape of the vocabulary *"is design work that owes its own change
   and its own review."*
3. **The COMMISSIONING of this packet**, relayed to the authoring session
   verbatim: **"Merge now, fix #575 next"** — the first clause disposing of
   #573, the second authorizing the AUTHORING of a fix and nothing below it.
   Recorded in `.openspec.yaml`'s `approved_by` as authorization to author, with
   the disclaimer that field has carried since issue #318.
4. **The TWO RULINGS on the flagged decisions**, 2026-09-02, recorded on PR
   #578 — § *What was flagged, and how it was ruled*.
5. **THIS RATIFICATION**, on that basis, over the baseline named above.

**Act 2 does not authorize act 3, act 3 does not authorize act 5, and act 5
authorizes no code.** Each is written down where it happened.

## What was flagged, and how it was ruled

Nine orchestrator decisions were flagged for veto. Two were named as owed an
explicit ruling rather than acceptance by silence, in the shape the archived
`add-release-tag-publication-check` packet's D4 was carried rather than assumed.

| | Decision | Disposition |
|---|---|---|
| **OD-1** | the record is `contracts/CHANGELOG.md`, not `health/dispositions.yaml` | stands as drafted |
| **OD-2** | a reserved single-line marker, not a free-prose read | stands as drafted |
| **OD-3** | a correctly declared spent bundle is an `info`, not silence | **RULED: ACCEPTED AS PROPOSED** |
| **OD-4** | the successor guard, and the `warning` band | **RULED: ACCEPTED AS PROPOSED** |
| **OD-5** | the finding path and the `contested` class | **AMENDED before this commit** on a Codex P1 |
| **OD-6** | the policy-side paragraph rides the next cut | stands as drafted, and OVERTAKEN by #577 |
| **OD-7** | one MODIFIED block, not a new requirement or family | stands as drafted |
| **OD-8** | proposal only; the realization is a separate PR | stands as drafted |
| **OD-9** | the successor must be STRICTLY LATER | **ADDED before this commit** on a Codex P1 |

**OD-3, ruled verbatim**: *"ACCEPTED as proposed: a correctly declared spent
bundle emits `info` with its own finding key, not silence. The reader who finds
`contracts/releases/contract-v2.6.digests.yaml` with no matching tag is owed the
answer where they are looking, and the key is what makes the one permanent
finding auditable."* The alternative — silence — was put to him with its cost
named (a permanent `info` nobody can act on, which is the enforcement floor's own
argument turned back on this state) and was declined.

**OD-4, ruled verbatim**: *"ACCEPTED as proposed: an unpublished successor is a
`warning` — quiet only once the superseding bundle's tag is published, `warning`
while it is cut but untagged, `error` where the named successor was never cut.
The only way to make a bundle quiet is to publish its successor's tag."*

**OQ-1, OQ-2 and OQ-3 REMAIN OPEN**, the rulings having reached the decisions
without reaching the questions. OQ-1 is the one a later reader is most likely to
trip over: the promoted `Deterministic check families` requirement's document-set
sentence for this family is ALREADY STALE — it names *"the DECLARED BUNDLE and
the repository's PUBLISHED TAG REFS"* and omits the `contracts/releases/` read
the family's own accepted amendment added — so this change adds a third input to
a sentence that already omits the second. The staleness is INHERITED, the
sentence's operative conclusion stays true of all three inputs, and no check
reads the input enumeration. No second MODIFIED block was opened over an
eight-scenario requirement to repair another change's omission.

## The two P1s, taken into the requirement

Both were raised by Codex against tip `2b66096c` — the tip the ruling was given
over — and both are repaired IN the requirement rather than filed as successors,
because each is a hole in the guard the ruling had just accepted rather than an
extension of it. **Recorded as a difference from the ratified tip rather than
smoothed into it.**

**P1 — the successor guard was satisfiable BACKWARDS.** As ruled, the guard
required the named superseding bundle to be CUT and PUBLISHED. It never required
it to be LATER. A declaration for `contract-v2.6` written into `contract-v2.5`'s
entry and naming `contract-v2.5` — a bundle that was cut, is published, and
carries a valid annotated tag on a declaring commit — passed every mechanical
check, so an untagged bundle would have gone quiet with **no replacement
published at all**. The requirement now demands the superseding bundle's
`(major, minor)` be STRICTLY GREATER, with its own `error` and its own scenario.
**This does not reopen OD-4**: a decision whose stated purpose is *"the only way
to make a bundle quiet is to publish its successor's tag"* is not met by a tag
that already existed, so the narrowing serves the ruling rather than revising it.
Filed as **OD-9**.

**P1 — two spent bundles would have shared one finding identity.** As proposed,
OD-5 landed the spent findings on `contracts/CHANGELOG.md` to give the state a
key distinct from the family's manifest-path findings. Codex showed that is the
same defect one step over: `Finding.match_key()` is `(family, repo, path)` and
ignores the rule, so two bundles legitimately declared spent share THAT path too
— and removing one declaration while the other stood would leave the shared key
in `uncited_resolutions()`'s current set, raising nothing, which is exactly the
per-state disappearance detection the `contested` class was chosen for. The
findings now land on `contracts/releases/<bundle>.digests.yaml`, unique to the
bundle BY CONSTRUCTION because it is the artifact whose existence made the bundle
enumerable at all. One finding of the state keeps the changelog path because it
has no bundle inventory to land on — a declaration whose SUBJECT was never cut
disposes nothing and is reported at `warning` there.

**Three scenarios joined the delta for these two findings** — the not-later
refusal, the never-cut SUBJECT warning, and a scenario pinning that TWO spent
bundles carry DIFFERENT identities — taking it from twenty-one to twenty-four.
Tasks § 2.7 requires the two-bundle case to be PROVEN by a test, because a
single-bundle test cannot see the defect Codex found.

## The rest of the review, including one refusal

**Codex, round 1** (`3667ddfe`): *"Didn't find any major issues."* A verdict on
a NAMED HEAD, not a refusal.

**Codex, round 2** (`2b66096c`): the two P1s above.

**Copilot, round 1** — 🟡 *Changes recommended*, one inline finding TAKEN: the
reserved marker form was shown wrapped in double backticks, which a reader can
copy as part of the literal line. It is now an indented code block, and the
requirement says why in one clause rather than leaving the reason to a commit.

**Copilot, round 1 — one finding REFUSED, WITH A MEASUREMENT.** The finding says
the front matter's unquoted `#575` *"will be parsed as a comment and break/alter
metadata consumption"*. **Nothing parses that block as YAML, and if anything did
the estate would already be broken more than a hundred packets deep.** Measured
rather than argued: `yaml.safe_load` FAILS on the front matter of
`add-release-tag-publication-check`, `add-requirement-ref-resolution-integrity`
AND `add-clearing-dispatch-boundary` — every one, on `mapping values are not
allowed here`, because these blocks are markdown headers full of prose
containing colons, not YAML documents. The reader that exists is line-wise:
`corpus.STATUS_RE` is `^Status:\s*(.+?)\s*$`, applied within
`STATUS_SCAN_LINES = 15`. And **sixteen** proposals in this repository already
carry an unquoted `#<issue>` on their `Origin:` line, including
`add-release-tag-publication-check` — this packet's own basis. Quoting this one
line would make it the lone divergence from a convention with no YAML reader to
serve. **The YAML surface that IS parsed is correct**: `.openspec.yaml` is
loaded, and every prose field in it is a folded `>-` block precisely so a `#`
inside it stays literal.

**Copilot, round 2** — 🔵 *Needs a closer look*, 0 new comments: *"introduces
governance-significant canonical-spec amendments explicitly flagged as requiring
owner ruling."* Which is what this record is.

**Sourcery is an upsell stub on this repository** and reviewed nothing.

## The one red test, measured rather than waved past

`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`
is RED, and it is **THIS PACKET'S SUBJECT, INHERITED FROM `main`**, not its
defect. Proven three ways rather than asserted:

* it is red at `ff9ed815` in a detached worktree with no packet present;
* the family reads `origin/main`, so its answer does not depend on any branch;
* the finding it fires on names `contract-v2.6` and carries this family's
  `_SUPERSEDED_ACTION` retro-publication text, which is the exact finding #575
  is about.

The CI run at `2b66096c` reported **1 failed, 8620 passed** — that failure and
nothing else. **This proposal cannot clear it**: clearing it requires the
realization, and OD-8 defers the realization on purpose. A merge of this PR is
therefore a merge on a DISPOSITIONED RED, and the realization PR that follows it
merges fully green.

**A SECOND FAILURE WAS FOUND ON THE FIRST RUN AND WAS MINE, and it is recorded
rather than folded away.**
`tests/sequenced_after/test_sweep.py::test_the_live_sweep_reproduces_the_AUTHORING_measurement`
passes at `ff9ed815` and failed with the packet: AUTHORING an active change that
carries a MODIFIED block raises `co_modified` and `active_co_modified`. That is
the pin doing its job, and its own docstring prescribes the response — *"WHEN THE
CORPUS MOVES, THIS PIN MOVES WITH IT … in the SAME COMMIT"*, with a dated
MOVEMENT LOG entry. The pin moved with a log entry; the three counts that did NOT
move are asserted with their reasons so that a change adding itself to two
populations at once could not hide; and that file is the one thing in this PR
that is **corpus bookkeeping rather than the realization OD-8 defers**, which
`proposal.md`'s `code_surface` states rather than leaving to a diff. Recorded in
tasks § 4.7 as a MISS: the doc-health measurement was complete for doc-health and
was read as though it were complete for the repository.

## What this packet MOVES, measured

`--single-repo` doc-health, base a detached worktree at the merge base, head the
packet committed, same clock: **6 critical / 5 error / 29 warning / 12 info on
BOTH**, and the two reports **BYTE-IDENTICAL** once the repo-identity string is
normalized. `family-enumeration` silent — no family and no count moves, which is
OD-8's mechanical argument. `modified-block-currency` reports
`scenario-title completeness: 0`, its gate-bearing arm, independently agreeing
with the scenario-by-scenario verification. The census is unmoved because a
`proposal.md` sits in the LIFECYCLE SCAN SET rather than the governed corpus,
which `Deterministic check families` states in terms.

**The delta's fidelity to canon was verified mechanically and not by eye**: the
block is BUILT FROM CANON at named anchors rather than retyped, and checked
scenario-by-scenario — **11 of 11 promoted scenarios present, 10 byte-identical,
the eleventh differing by exactly ONE added `AND` bullet with nothing removed,
and all 67 canon body lines surviving.** Thirteen scenarios added; twenty-four in
total.

**ONE PROMOTED PARAGRAPH IS QUALIFIED RATHER THAN REPLACED**, and the delta says
so where it happens. *A SUPERSEDED BUNDLE IS NOT GRADED BY DISTANCE* still reads
*"reported at `error` without grading"*, byte-unchanged, and that remains exactly
what such a bundle reads as wherever no declaration names it — every bundle in
the estate's history but one, and the default forever.

## What ratification does NOT authorize

Stated as a list because a ratification record that leaves this implicit is how a
realization acquires scope nobody granted it.

1. **No code lands here.** Not one line of
   `scripts/doc_health/release_tag_publication.py`, not one new test, not one
   docs row. The realization is the NEXT PR.
2. **No SPENT declaration is authored here.** `contracts/CHANGELOG.md` is
   untouched by this commit. Tasks § 2.1 makes writing it the FIRST act of the
   realization, and requires the removal-and-re-run proof that `main` goes green
   because the bundle is EXPLICITLY DECLARED spent and never because an
   undeclared bundle started passing.
3. **No release surface moves.** `contracts/manifest.yaml`,
   `contracts/releases/contract-v2.6.digests.yaml` and the `contract-v2.6`
   changelog entry are untouched and stay untouched: they are the record of what
   was declared, and the family's own action text forbids editing them to match
   an absence.
4. **No bundle is cut and no tag is published.** `contract-v2.6` has no legal
   target, its number is never reused, and this change gives the absence a name
   rather than filling it.
5. **No retrofit.** The five instances the versioning policy records under
   § *Untagged Bundles After Enforcement Began* were all publishable and all
   published; the requirement forbids reading the state backwards onto them or
   onto any bundle below the enforcement line.
6. **Nothing else is relaxed.** The threshold stays five, the floor stays
   `contract-v1.7`, MISPLACED and LIGHTWEIGHT keep their own words and are
   explicitly beyond the reach of the SPENT state, and the declared bundle's
   distance grading is untouched.
7. **OQ-1 … OQ-3 are not disposed of** by this act and must not be read as
   accepted by it.

## Addendum — the parallel lane, recorded because it changed an argument

**PR #577** (merged `2898b104`, 2026-09-02) recorded `contract-v2.6`'s
supersession in `docs/contract-versioning-policy.md` as instance SIX. It is a
THIRD lane's act and this packet neither commissioned nor reviewed it, but it
touches two things here and they are recorded rather than left to collide later.

**It discharges half of tasks § 3.1.** A consumer reading the pinned policy now
learns that `contract-v2.6` is superseded and not dischargeable, and that half
MUST NOT be re-authored — *"two records of one measurement is how they drift
apart."* What #577 deliberately did NOT do is define the state or its
declaration form: *"No sentinel is invented … Building one here would be exactly
the failure that check exists to catch."* That definition is this packet's, and
it remains owed.

**And it makes OD-6's prediction true while spending its arithmetic.** OD-6
declined to edit that file between cuts because it is a NON-EDITORIAL member of
`contracts/releases/contract-v3.0.digests.yaml` and the edit would raise a
`release-inventory-drift` ERROR. #577 made that edit, and the family now reports
over `main`: **`[error] docs/contract-versioning-policy.md — bytes differ from
the digest 'contract-v3.0' records`**. The analysis is vindicated exactly and its
conclusion is overtaken in the same stroke: the error exists already, so the
INCREMENTAL cost of the SPENT-state paragraph is now ZERO and clears at the same
next cut either way. The decision is not rewritten retroactively — it was right
when taken and its reasoning is preserved — and the realization takes the routing
with the new measurement in hand.
