---
code_surface: openxFactory (`scripts/doc_health/corpus.py` — a SECOND path set beside `GOVERNED_ROOTS`, named `LIFECYCLE_SCAN` and built by explicit glob rather than by directory, plus the loader that turns it into a second document list; `scripts/doc_health/runner.py` — `Context` gains one field carrying that list, and the four lifecycle-conformance families read it in addition to `ctx.docs`; `scripts/doc_health/families.py` — `fam_status_validity`, `fam_standard_backing`, `fam_ratified_provenance` and `fam_succession_integrity` iterate the union rather than `ctx.docs` alone, and nothing else in the module changes; `tests/doc-health/` — positive and negative cases for the set's membership, for each of the four families over it, for the exclusion of the other twelve, and for the invariant that `ctx.docs`, the per-stage census, the canon-share headline, the shared inventory and the catalog are byte-identical before and after, mutation-validated. `docs/document-lifecycle.md` is prose rather than runtime code, but it is the text the status rule implements and any ruling that makes proposal packets governance documents lands in the same slice.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, full stop — `python3 -m pytest tests/doc-health` and `tests/ideation-dashboard -k workbench` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts and in no other line. The bare `implementation_pending` token is deliberately NOT used: `docs/archive-record-discrepancies.md` C1 records that it is a house token the realization axis does not define, and Brett's 2026-08-22 ruling rewrote four archived proposals off it.
Status: ratified
Ratified: 2026-08-23 by Brett Heap — in-session, multiple-choice ruling round over all six Open Questions; OQ-1, OQ-2, OQ-3 and OQ-5 adopt the recommendation, OQ-4 and OQ-6 DEPART from it and rule the wider campaign in both cases; the round is recorded question by question in the Open Questions section of openspec/changes/govern-openspec-corpus-membership/proposal.md, which is this file. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and it clears that spelling's three-way floor on all three axes rather than on the one it needs: approver (`by Brett Heap`), date (`2026-08-23`), and a resolvable record path.
Proposed: 2026-08-23
---

# Proposal: govern-openspec-corpus-membership

## Why

**The last three slices each fixed a lifecycle-header defect that nothing
would have caught.** The register says so in its own words. Under
`docs/archive-record-discrepancies.md` § "What the tooling does and does not
enforce here":

> The doc-health `record-immutability` family does **not** reach any file
> under `openspec/`. It iterates `ctx.docs`, which `doc_health.corpus` builds
> from the governed roots `contracts/`, `docs/`, `examples/`, `ideation/`,
> `templates/` only […] Nor does any reader consult a proposal's `Status:`
> header.

That is the gap, stated by the record that measured it. `openspec/` holds 663
Markdown documents in this repository — more than twice the 327 the governed
roots reach — including every proposal whose `Status: ratified` header makes
a claim about approval. Not one of those headers is read by a live check.

The three most recent slices are the evidence that the gap costs something:

- `2026-08-22-add-doxbench-editing-phase-b` carried `Status: ratified` with no
  ratification citation anywhere in the file. Found by an adversarial review,
  fixed by hand as **PR #270**.
- `2026-08-22-add-roster-device-admission-surface` carried its `Status:` at
  real line 41 and its `Ratified:` at 42, both outside the fifteen-real-line
  window `corpus.STATUS_SCAN_LINES` sets — so every reader counted the
  document headerless. Found by the same review, fixed by hand by
  `roster-device-header-window`.
- `add-worker-credential-by-reference`'s `target_release` was rewritten off a
  house token the realization axis does not define, the sixth C1 item.

Each was found by a person reading carefully. `sanction-ratified-record-spelling`
task 5.1 parked the question of whether a machine should be reading instead:

> `openspec/` joining `GOVERNED_ROOTS` — the event that makes the 15 latent
> lines live. Separate decision, much larger blast radius.

That is the last unticked box of that change. Its siblings are all discharged.
This proposal takes the decision.

**One correction to the gap's shape, so the case is not overstated.** The
proposal `Status:` header and its ratification citation are read by nothing.
The *release-realization* front matter beside them IS read:
`scripts/ideation_dashboard/generator.py` sets
`HEADER_SCAN_LINES = corpus.STATUS_SCAN_LINES` and pulls `code_surface` and
`target_release` through that same fifteen-line window. That is why the
roster-device defect had a downstream effect at all — both fields read `None`
while the header sat at line 41 — and it is why the window, not just the
membership, is part of what this change has to reason about.

## The measurement

Every number below was taken in this worktree at `20f3e7e` (`origin/main`),
by monkey-patching `corpus.GOVERNED_ROOTS` in memory rather than editing a
tracked file, so no baseline was ever at risk. Restoration was verified two
ways: `git status --porcelain` clean, and a re-run whose report is
**byte-identical** to the baseline report.

### Baseline

`python3 scripts/doc-health.py --single-repo . --as-of 2026-08-23`

| | value |
| --- | --- |
| findings | **4 critical / 6 error / 68 warning / 4 info** = 82 |
| documents examined | 327 |
| governance words | 532,162 (promoted specs included) |
| canon words | 166,693 |
| canon share | **31.3%** |
| `pytest tests/doc-health` | 724 passed |

Per family: `record-immutability` 4C · `status-validity` 3E ·
`location-conformance` 2E · `proposal-origin` 1E + 30W ·
`staged-topic-template` 28W · `staged-candidate-aging` 10W + 1I ·
`ideation-routing` 2I · `document-catalog` 1I.

### Option (a) — full membership

`GOVERNED_ROOTS = (…, "openspec")`. One line.

| | baseline | full membership | delta |
| --- | --- | --- | --- |
| findings | 82 | **655** | **+573 (×8.0)** |
| critical | 4 | 27 | +23 |
| error | 6 | 556 | +550 |
| documents examined | 327 | 990 | +663 |
| governance words | 532,162 | 1,346,669 | +814,507 |
| canon share (this repo) | 31.3% | **18.1%** | **−13.2 pts** |
| canon share (six-repo aggregation) | 28.9% | **16.7%** | **−12.2 pts** |
| `pytest tests/doc-health` | 724 pass | **601 pass / 123 fail** | +123 failures |

Which families move, and whether the movement is real:

| family | baseline | full | new fires — what they are |
| --- | --- | --- | --- |
| `status-validity` | 3E | 539E | **+536.** 527 "missing status header" — every `tasks.md`, `design.md`, spec delta, supporting-doc, evidence file and review note in the packet — plus 12 free-form values. |
| `ratified-provenance` | 0 | 20C | **+20.** The real gap. Enumerated below. |
| `location-conformance` | 2E | 9E | **+7**, of which **2 are false**: `supporting-docs/source-snapshots/` byte-exact copies fire "staged fragment outside `ideation/`" for the `Status: staged` they exist to preserve. |
| `succession-integrity` | 0 | 4E | +4, all archived supporting-docs of one 2026-07-13 change. |
| `record-immutability` | 4C | 7C | +3, all `evidence/` files under one active change. |
| `tag-hygiene` | 0 | 2E | **+2, both false**: `archive/2026-07-09-concretize-prose-tagging-syntax` is the change that DEFINED the marker grammar and necessarily carries illustrative markers. |
| `staged-candidate-aging` | 10W+1I | +1E | **False, same document** — "supersedes without `change=` for 46 days" on the grammar-defining proposal. |
| `proposal-origin`, `staged-topic-template`, `ideation-routing`, `document-catalog` | — | — | **unchanged.** `proposal-origin` and `ideation-routing` already read `openspec/` directly, independent of `GOVERNED_ROOTS`. |

The 123 test failures are not 123 problems. **121 of them are one message** —
`ValueError: duplicate inventory key: ('alpha', 'openspec/specs/widget/spec.md')`
— a structural collision: promoted specs already enter the shared inventory
as `artifact_type: promoted_spec`, and making `openspec` a governed root
delivers the same file a second time as `governance_markdown`. The other two
are pinned invariants that full membership contradicts outright:

- `test_promoted_specs_join_without_expanding_the_governed_corpus` asserts
  `not any(d.path.startswith("openspec/") for d in docs)`. The corpus model
  has a written intention here, and it is the opposite of option (a).
- `test_source_snapshots_keep_their_staged_status`, a 2026-08-15 regression
  test whose docstring says a byte-exact snapshot "must not be reported for
  the status it records". Full membership re-breaks it through a second rule.

**Full membership costs 573 findings and 13 points of the canon-share
headline to buy 20 findings' worth of enforcement, and at least five of the
new fires are demonstrably wrong.** It is not the honest option.

### Option (b) — a scoped lifecycle scan set — RECOMMENDED, AND RULED 2026-08-23

A second path set beside `GOVERNED_ROOTS`, read only by the
lifecycle-conformance families. `ctx.docs` never changes, so the per-stage
census, the canon-share headline, the shared inventory and the catalog are
untouched — which is where 121 of option (a)'s 123 test failures and all of
its corpus-shape distortion came from.

The set is `openspec/changes/**/proposal.md` plus
`openspec/changes/**/review/*.md` — **118 documents, not all 663**. Measured
over that set (119 once this change's own `proposal.md` exists; it carries a
valid header and a floor-clearing citation, so it adds a document to the set
and no finding to the count — re-verified after ratification, both family
tallies below are unchanged):

| family | fires | severity |
| --- | --- | --- |
| `ratified-provenance` | **20** | critical |
| `status-validity` | **48** | error (47 missing header, 1 free-form) |
| `standard-backing` | 0 | — |
| `succession-integrity` | 0 | — |
| `location-conformance` | **0** | — the source-snapshot false positives are outside the set |
| `tag-hygiene` | (1)* | NOT a reader of the set — measured only to justify its exclusion |

\* `tag-hygiene` is outside the four ruled families, so its one would-be
fire (the grammar-defining proposal, a false positive) never surfaces; it is
shown here as the measurement that keeps it out, and it is NOT in the scoped
totals below.

| | baseline | scoped | delta |
| --- | --- | --- | --- |
| findings | 82 | **150** | +68 |
| critical / error / warning / info | 4/6/68/4 | 24/54/68/4 | +20C, +48E |
| documents examined | 327 | **327** | **0** |
| canon share | 31.3% | **31.3%** | **0** |
| `pytest tests/doc-health` | 724 pass | **724 pass** | **0 failures** |

**Why the set includes `status-validity` and not just `ratified-provenance`.**
Both pre-fix documents were replayed through the families to check this rather
than assumed:

- phase-b at `02a71d6`: `parse_status` reads `ratified`, and
  `ratified-provenance` emits "ratified header carries no citation in either
  sanctioned spelling". **Caught.**
- roster-device at `280fc8b`: `parse_status` reads `None`, because the header
  is at real line 41. `ratified-provenance` skips the document entirely and
  emits **nothing**; `status-validity` emits "missing status header".
  **Caught only by `status-validity`.**

A ratification family alone catches one of the two defects that prompted this
question. That is the whole argument for the wider four.

### Option (c) — stay out, with a standing regression test

Costs nothing in the report and nothing in the corpus. But the test is red
today on the identical 68 documents, so it carries option (b)'s whole content
cost with less standing: a failed assertion has no severity, no ranked-plan
row, no `auto-fixable`/`contested` class and no disposition route through
`health/dispositions.yaml`. It also re-implements the family wiring in test
code — a second rule beside the first, which is the exact hazard
`align-status-reader-to-real-lines` spent a change removing.

## What Changes

The recommendation is **option (b)**, at the scan set and family set the
measurement picked. **RULED as recommended on 2026-08-23** — see Open
Questions for the round in full, and items 5 and 6 below for the two places
where the ruling went WIDER than this section first proposed.

1. **`openspec/` does NOT join `GOVERNED_ROOTS`.** Corpus membership stays as
   it is, and the decision is recorded rather than left implicit — the
   promoted `doc-health` spec today never states which roots the corpus is
   built from, so the question this change answers has no written answer to
   contradict.
2. **A second, declared path set — the lifecycle scan set — is added:**
   `openspec/changes/**/proposal.md` and `openspec/changes/**/review/*.md`.
   Declared by explicit glob, not by directory, because the measurement shows
   the cost is entirely in the packet's working files and none of the benefit
   is.
3. **Exactly four families read it** in addition to `ctx.docs`:
   `status-validity`, `standard-backing`, `ratified-provenance`,
   `succession-integrity`. The other twelve do not, and the census, the
   word counts, the canon-share headline, the shared inventory, the document
   catalog, the semantic sweep and the aging lanes are all unchanged by
   construction.
4. **`document-lifecycle` states that a change's `proposal.md` and its
   `review/` ratification records are governance documents** subject to the
   controlled `Status:` taxonomy and to the ratification-citation rule. That
   is what makes the 48 `status-validity` fires legitimate rather than
   arbitrary, and it was the sentence Brett was actually being asked to
   ratify. He did, on 2026-08-23. The rest of the packet — `tasks.md`, `design.md`, spec deltas,
   `supporting-docs/`, `evidence/` — is deliberately NOT ruled here.
5. **All 68 standing violations are DISCHARGED before the code lands**, not
   after and not grandfathered. A gate that goes red on the commit that
   introduces it teaches people to skip the gate. This is the first of the
   two places the 2026-08-23 ruling went wider than the draft: the draft
   recommended discharging 24 by hand and reducing the other 44 to a
   `pre-contract legacy` severity class (OQ-6's recommendation), and the
   ruling took the backfill instead. There is therefore **no reduced-severity
   class in this change at all** — no contract date to set, no legacy rule
   string to write, and no residual backlog left visible-but-unfixed. The
   measured target at §2's merge is **zero CRITICAL and zero ERROR from the
   scoped scan**, with the whole-repo report standing at its unchanged
   baseline of 4 critical / 6 error / 68 warning / 4 info.
6. **Every one of the 17 record-citing `Ratified by:` lines is respelled**,
   active and archived alike, each justified from its own record. This is the
   second widening: the draft recommended rewriting the 6 active ones in
   place and covering the 11 archived ones with a single block ruling
   (OQ-4's recommendation), and the ruling requires the same per-record
   justification for all 17, with the archived eleven carrying the
   bookkeeping note the register's append discipline requires. The respell is
   a **prefix change only** — `Ratified by:` becomes `Ratified:` and the
   content after the colon is carried verbatim — because each of these lines
   is already substantively sound and merely spelled under the rule that does
   not fit it. **Extended 2026-08-23 to 33** by OQ-4's RULED-extension note:
   the 16 self-citing lines, which pass the family only by naming their own
   change id, are the same class and take the same respell. They are LATENT —
   they clear no finding — so the count of findings this change discharges is
   unchanged by the extension and only the count of edits grows.

## Impact

- Affected specs: `doc-health` (MODIFIED `Deterministic check families`,
  ADDED `Governed corpus membership and the lifecycle scan set`);
  `document-lifecycle` (ADDED `Proposal packets carry the lifecycle header`).
- Affected code: `scripts/doc_health/{corpus,runner,families}.py`,
  `tests/doc-health/`. No contract schema, no digest set, no release tag.
- Affected docs: `docs/document-lifecycle.md` § Status Claim Rules, README
  Active row, and — added by the 2026-08-23 ruling —
  `docs/archive-record-discrepancies.md`, which gains an entry for the 11
  archived respells and a successor entry to C2 for the 44 archived
  backfills. Up to 56 archived records are edited by this change's §5 (11
  proposal respells, 44 proposal backfills less whatever stops and reports,
  1 archived review record), and the register is where archived-record edits
  are accounted for. **Revised 2026-08-23 to up to 71** by OQ-4's
  RULED-extension: the 15 archived self-citers are archived-record edits too,
  and 5B.4's register entry accounts for 27 archived documents rather than 12.
- Nightly: the canon-share metric does not move. Under option (a) it would
  fall 12.2 points on the six-repo aggregation, which would read as a corpus
  collapse and would be an artifact of the measurement changing.
- New standing findings on the day the code lands: **zero.** The scan set
  carries 20 critical + 48 error today, and under the 2026-08-23 ruling §5 of
  tasks discharges all 68 before §2 may merge. That is what §5 is for, and it
  is now the whole of §5 rather than most of it.

## Open Questions

**OQ-1 — Which option?** RECOMMENDED: **(b), the scoped lifecycle scan set.**
(a) full membership costs 573 findings, 13 canon-share points and 123 test
failures, and fires falsely at least five times. (c) test-only costs the same
68 dispositions with no severity, no class and no disposition route.

**RULED (2026-08-23, Brett, in-session multiple choice): recommendation adopted — (b), the scoped lifecycle scan set.** Recorded honestly because the
route to the answer is part of the record: Brett's first lean was **(a), full
membership** — the larger, simpler claim — and he moved to (b) after reading
the measured costs, specifically the 121-of-123 `duplicate inventory key`
collision and the 12.2-point fall in the six-repo canon-share headline he
watches nightly. The measurement changed the ruling; that is what it was taken
for, and a ruling that merely confirmed a prior lean would be weaker evidence
that the numbers were read.

**OQ-2 — What exactly is in the scan set?** RECOMMENDED:
`openspec/changes/**/proposal.md` + `openspec/changes/**/review/*.md`, 118
documents. Alternatives: proposal files alone (107 documents — drops
`ratified-provenance` from 20 fires to 17, losing the three review
ratification records, which are precisely the documents whose whole job is to
record a ratification); or the whole of `openspec/` (663 documents — adds 488
"missing status header" errors on working files and reintroduces the
source-snapshot and grammar-marker false positives).

**RULED (2026-08-23, Brett, in-session multiple choice): recommendation adopted, unopposed in prose — the scan set is the two globs, `openspec/changes/**/proposal.md` and `openspec/changes/**/review/*.md`.** Neither alternative
was argued for. The set is declared as a pattern pair and not as a directory,
which is the claim design.md Decision 2 makes and the boundary tasks §3.6
mutation-pins.

**OQ-3 — Which families read it?** RECOMMENDED: the four lifecycle-conformance
families — `status-validity`, `standard-backing`, `ratified-provenance`,
`succession-integrity`. Explicitly out: `location-conformance` and
`tag-hygiene` (measured false positives), `staged-candidate-aging` (same),
`record-immutability` (its meaning over an archived packet is genuinely
unsettled — see OQ-6), and every census, word-count, canon-share, inventory
and catalog consumer.

**RULED (2026-08-23, Brett, in-session multiple choice): recommendation adopted, unopposed in prose — four families read the set: `status-validity`, `standard-backing`, `ratified-provenance`, `succession-integrity`.** The
exclusions stand as written, `record-immutability` included: OQ-6's ruling
requires 44 archived proposals to be edited, which is precisely the traffic
that would put the family's "revert the content edit" remedy against the
register's append discipline. Leaving it out was a hedge when this section
was drafted; after OQ-6 it is load-bearing.

**OQ-4 — The 17 `Ratified by:` lines that cite a record, not a change.**
These are the largest single block of new criticals, and they are the case
`sanction-ratified-record-spelling` task 5.3 parked ("Rewriting any existing
citation line to a preferred shape"). `docs/document-lifecycle.md` says the
record-citing `Ratified:` spelling "SHALL be used only where no approving
OpenSpec change exists to name" — and each of these 17 names an approver and
a date rather than a change, so each is substantively sound and spelled
wrong. RECOMMENDED: rewrite the **6 active** proposals in place (no archive
rule is engaged), and route the **11 archived** ones through the register's
citing-change-plus-ruling path, one ruling covering the block. Alternatives:
widen the family so a `Ratified by:` line that resolves to no change falls
back to the three-way floor (cheap, but it erases the spelling distinction
`sanction-ratified-record-spelling` was ratified to draw); or disposition the
17 as a closed legacy set.

**RULED (2026-08-23, Brett, in-session multiple choice): the recommendation was NOT adopted. Rewrite ALL 17 — 11 archived and 6 active — to the same standard.** The recommendation above is kept verbatim as history, and what
replaces it is this:

- **The edit is a prefix respell.** `Ratified by:` becomes `Ratified:` and
  everything after the colon is carried **verbatim**. Nothing is rephrased,
  nothing is added, nothing is dropped. Each of these lines already names an
  approver and a date, so each already clears the record-citing spelling's
  three-way floor on the day it is respelled; the defect being fixed is the
  spelling and only the spelling.
- **Each line is justified from its own record, all 17.** The recommendation
  would have covered the archived eleven with one block ruling. It is
  rejected because a block ruling records that a class was decided and not
  that any individual record supports its own line — and the one thing this
  whole change exists to make checkable is whether a document's citation is
  backed by something. Seventeen one-record justifications cost more and
  prove more.
- **The archived eleven travel under the B1/B2 append-correction
  discipline** (`docs/archive-record-discrepancies.md`, B1 and the C7
  execution note). A respell on a single-valued header cannot be an append
  for the mechanical reason B1 states, so each is an **in-place overwrite and
  an extension of Brett's 2026-08-10 append ruling, named as one**, and each
  carries a bookkeeping note that preserves the original line verbatim and
  travels with the change it corrects.
- **Boundary, measured rather than assumed.** The ruled set is the 17 the
  family fires on. A LATENT eighteenth exists and is deliberately outside it:
  `add-identity-brokering`'s `Ratified by:` line is substantively
  record-citing too, but it happens to name a path
  (`review/co-residence-finding-2026-08-21.md`) that resolves, so
  `fam_ratified_provenance`'s primary-spelling branch accepts it and it emits
  no finding. It is named here so a later reader who counts 18 by eye knows
  the 17 is the enforced set and not an arithmetic slip. Respelling it is not
  ruled.

**RULED — EXTENSION (2026-08-23, Brett, in-session, after the slice-5A
adversarial review): the 16 SELF-CITING `Ratified by:` lines are the same
class and take the same remedy. The ruled set grows from 17 to 33.**

The review found a shape the boundary paragraph above did not: a `Ratified by:`
line whose named change id is the DOCUMENT'S OWN change id. It passes
`fam_ratified_provenance` because the family's primary-spelling branch asks
only whether the line names *an* id in `ctx.change_ids` — and a proposal that
writes "user approval of \`add-hermes-domain-overlay-contract\` on 2026-07-23"
names one, its own. **A change is not its own approving change.** Substantively
these lines do exactly what the 17 do: they name an approver and a date, which
is the record-citing spelling's content written under the primary spelling's
prefix. Same defect, same remedy — prefix respell `Ratified by:` to
`Ratified:`, content carried VERBATIM, one per-record justification each, and
the archived ones under the B1/B2 append-correction discipline with a
bookkeeping note.

**The one difference from the 17, and it changes how the work is reported:
the 17 are LIVE CRITICALs and the 16 are LATENT.** The 16 emit nothing today,
so respelling them clears no finding from the census and 5D's zero gate does
not depend on them. Their respell is corrective, not finding-driven, and 5B
says so at the tick rather than claiming a discharge it did not make.

The 16, derived by replaying the primary-spelling resolution over the ruled
scan set through the real helpers and testing each line's named ids against
the document's own change id (and against its date-prefixed archive-folder
spelling) — **1 active, 15 archived**:

| # | change | the id its `Ratified by:` line names |
| --- | --- | --- |
| 1 | `add-hermes-customer-subject-runtime-contract` (ACTIVE) | itself, "user approval … on 2026-07-12" |
| 2 | `archive/2026-07-23-add-hermes-domain-overlay-contract` | itself, 2026-07-23 |
| 3 | `archive/2026-07-23-adopt-subject-tenant-domain-vocabulary` | itself, 2026-07-23 |
| 4 | `archive/2026-07-24-add-client-layer-tuning-contracts` | itself, 2026-07-24 |
| 5 | `archive/2026-07-24-add-hermes-domain-content-manifest` | itself, 2026-07-24 |
| 6 | `archive/2026-07-24-add-omnigent-domain-overlay` | itself, 2026-07-22 |
| 7 | `archive/2026-07-29-add-crystallizer-contracts` | itself, 2026-07-29 |
| 8 | `archive/2026-07-29-add-pattern-ledger` | itself, 2026-07-29 |
| 9 | `archive/2026-07-30-add-capability-steward` | itself, 2026-07-29 |
| 10 | `archive/2026-07-30-add-deployment-handoff-boundary` | itself, 2026-07-29 |
| 11 | `archive/2026-07-30-add-domain-ontology-layer` | itself, 2026-07-28 |
| 12 | `archive/2026-08-01-add-dashboard-repo-selector` | itself, 2026-07-29 |
| 13 | `archive/2026-08-01-add-workbench-branch-sessions` | itself, 2026-07-26 |
| 14 | `archive/2026-08-05-add-neutrality-drift-lane` | itself, 2026-08-04 |
| 15 | `archive/2026-08-05-adopt-neutral-tooling-home` | itself, 2026-08-03 |
| 16 | `archive/2026-08-06-add-consent-instrument` | itself, 2026-08-03 |

One correction to the review's own shape, made rather than inherited: the
review reported "16 archived proposals". The replay returns **15 archived and
1 active** — `add-hermes-customer-subject-runtime-contract` is a live change.
The count and the class are the review's; only the archived/active split is
corrected, and it matters because the active one takes no archive discipline.

**Boundary, measured rather than assumed, exactly as the 17's boundary was.**
Four further scan-set documents pass the primary spelling by naming some
OTHER change id in passing prose rather than an approving change:
`add-shared-identity-seeds` (its line names `add-repository-lens` as the
successor relationship, and its approval is Brett's "yes, lets start that now"
on 2026-08-07), and `archive/2026-07-30-add-omnigent-semantic-wiring`,
`archive/2026-07-30-add-ontology-term-lifecycle-enforcement` and
`archive/2026-07-30-publish-semantic-kernel`, each of which names
`add-domain-ontology-layer` as the change it follows on from. These are
substantively record-citing too, and they are NOT self-citers; they are
OUTSIDE the ruled 33 and respelling them is not ruled. They are named for the
same reason `add-identity-brokering` is named above — so a later reader who
counts 37 by eye knows which set was ruled and which was measured.

**OQ-5 — The three `review/ratification-*.md` records use a THIRD vocabulary.**
They carry `Ratifier:` and `Decision date:` headers — better provenance than
most of the corpus, in a spelling no rule knows. RECOMMENDED: add a
conforming `Ratified:` line to each (they already name approver and date, so
this is one line and invents nothing). Alternative: sanction `Ratifier:` +
`Decision date:` as a third spelling, which reopens what
`sanction-ratified-record-spelling` closed six weeks ago. Alternative:
exclude `review/` from the set, which costs the three fires OQ-2 exists to
keep.

**RULED (2026-08-23, Brett, in-session multiple choice): recommendation adopted — add a conforming `Ratified:` line to each of the three.** No third
spelling enters the rule. `Ratifier:` and `Decision date:` stay on the page
and keep saying what they say; they simply stop being the only thing that
says it. Each of the three already names its ratifier and its decision date,
so the conforming line is derived from the document's own headers and invents
nothing — which is the whole reason this one was cheap enough to rule as
recommended while OQ-4 and OQ-6 were not.

**OQ-6 — The 47 proposals with no `Status:` header at all** (44 archived, 3
active) are the whole of the `status-validity` cost bar one free-form value.
RECOMMENDED: **the `proposal-origin` precedent** — a contract date, ERROR
after it, WARNING with a "pre-contract legacy" rule string before it. That
pattern is already ratified and already running in this same suite, it costs
zero archived-record edits, and it leaves the backlog visible instead of
silent. Alternatives: backfill all 47 headers (44 are archive-record edits,
each needing the register's route — a large ruling round for a mechanical
gain); or rule that a headerless archived proposal is legal, which would mean
`document-lifecycle`'s "Every governance document SHALL carry a `Status:`
header" does not reach proposals, and OQ-1's whole premise with it.

**RULED (2026-08-23, Brett, in-session multiple choice): the recommendation was NOT adopted. Backfill ALL 47 — 44 archived and 3 active. No grandfather, no contract date, no reduced-severity class.** The recommendation above is kept
verbatim as history. What replaces it:

- **Every headerless proposal gets a `Status:` header derived from its own
  record**, in the same per-record way OQ-4 requires of the respells. The
  derivation sources are the ones the register already hunts: the packet's
  `.openspec.yaml`, the archive and ratification commits, the change's own
  `tasks.md`, the README row.
- **Where the derived status is `ratified`, a floor-satisfying citation is
  written in the SAME edit.** This is not an optional extra: the promoted
  rule holds that a bare, uncited `Status: ratified` is a violation whatever
  else the document says, so backfilling a status alone would convert a
  `status-validity` ERROR into a `ratified-provenance` CRITICAL and discharge
  nothing. **Measured: not one of the 47 carries a ratification citation
  anywhere in its file**, in either spelling, inside the header window or
  out. So the two axes are coupled for this whole population and the backfill
  writes up to two header lines per document, not one.
- **Where the record genuinely cannot support a status or a citation, the
  campaign STOPS AND REPORTS that document.** It does not invent one. The
  anti-invented-provenance principle survives this ruling unchanged — it is
  the principle C2 stated as "no invented provenance anywhere" and C7 as
  "nothing was inferred, and nothing was discovered", and widening the
  population does not weaken it. A stopped document is reported by name with
  what its record does and does not carry; it is not silently skipped, and it
  is not given a plausible-looking header.
- **This ruling supersedes the class half of C2's 2026-08-22 ruling, and says
  so.** One day earlier, C2 ruled the archived half of this same question
  narrowly: "backfill the seven true anomalies where the records allow, and
  only there … The
  forty-six-wide option was not taken." The wide option is now taken. What
  C2's execution FOUND is not superseded and is the campaign's best evidence
  about its own difficulty: of those seven, two were backfilled, and **five
  were examined record by record and left headerless** —
  `add-propose-verb` (its record names no ratifier and no ratification date
  at all), `add-staging-workbench`, `add-workbench-bullseye-and-create` and
  `add-wheel-action-verbs` (each carries an `origin:`-nested
  `approved_by`/`approved_on` pair that records permission to author without
  a staging source, dated six to eleven days before archive, plus a task
  sign-off — two near-misses, neither a ratification), and
  `add-workbench-integrated-editor-chat`, which is stronger than
  insufficient-evidence: its archive commit `354ded9` records a decision
  AGAINST writing a status value, and register entry A2 verifies that
  decision as deliberate. Those five are the first five stop-and-report
  candidates, already adjudicated once. The remaining 39 archived documents
  are the pre-convention population C2 explicitly left out of scope and
  nobody has yet examined.
- **The 3 active headerless proposals** — `add-dispatch-credential-contract`,
  `add-ideation-intent-plane`, `add-worker-enrollment-broker` — are current
  documents, not archived records, and take no discipline beyond deriving the
  right value. Two of the three additionally carry no `.openspec.yaml`, which
  is a `proposal-origin` matter and not this change's to fix.

## Non-Goals

- Changing `GOVERNED_ROOTS`, the canon-share formula, the per-stage census,
  the shared inventory, or the document catalog. The measurement's central
  finding is that every expensive consequence flows from `ctx.docs`, and this
  change does not touch it.
- Widening `STATUS_SCAN_LINES`. The fifteen-real-line window is shared by
  `parse_status`, `families._header_lines` and
  `ideation_dashboard.generator._header_value`, and moving it is its own
  measurement.
- Ruling on whether `tasks.md`, `design.md`, spec deltas, `supporting-docs/`
  or `evidence/` are governance documents. Deliberately left open; see What
  Changes item 4.
- Rewriting the ratification citation of any document this proposal does not
  enumerate.
