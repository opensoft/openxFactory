---
code_surface: openxFactory (`scripts/doc_health/corpus.py` — a SECOND path set beside `GOVERNED_ROOTS`, named `LIFECYCLE_SCAN` and built by explicit glob rather than by directory, plus the loader that turns it into a second document list; `scripts/doc_health/runner.py` — `Context` gains one field carrying that list, and the four lifecycle-conformance families read it in addition to `ctx.docs`; `scripts/doc_health/families.py` — `fam_status_validity`, `fam_standard_backing`, `fam_ratified_provenance` and `fam_succession_integrity` iterate the union rather than `ctx.docs` alone, and nothing else in the module changes; `tests/doc-health/` — positive and negative cases for the set's membership, for each of the four families over it, for the exclusion of the other twelve, and for the invariant that `ctx.docs`, the per-stage census, the canon-share headline, the shared inventory and the catalog are byte-identical before and after, mutation-validated. `docs/document-lifecycle.md` is prose rather than runtime code, but it is the text the status rule implements and any ruling that makes proposal packets governance documents lands in the same slice.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, full stop — `python3 -m pytest tests/doc-health` and `tests/ideation-dashboard -k workbench` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts and in no other line. The bare `implementation_pending` token is deliberately NOT used: `docs/archive-record-discrepancies.md` C1 records that it is a house token the realization axis does not define, and Brett's 2026-08-22 ruling rewrote four archived proposals off it.
Status: draft
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

### Option (b) — a scoped lifecycle scan set — RECOMMENDED

A second path set beside `GOVERNED_ROOTS`, read only by the
lifecycle-conformance families. `ctx.docs` never changes, so the per-stage
census, the canon-share headline, the shared inventory and the catalog are
untouched — which is where 121 of option (a)'s 123 test failures and all of
its corpus-shape distortion came from.

The set is `openspec/changes/**/proposal.md` plus
`openspec/changes/**/review/*.md` — **118 documents, not all 663**. Measured
over that set:

| family | fires | severity |
| --- | --- | --- |
| `ratified-provenance` | **20** | critical |
| `status-validity` | **48** | error (47 missing header, 1 free-form) |
| `standard-backing` | 0 | — |
| `succession-integrity` | 0 | — |
| `location-conformance` | **0** | — the source-snapshot false positives are outside the set |
| `tag-hygiene` | 1 | the grammar-defining proposal — reason it stays out |

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
measurement picked.

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
   arbitrary, and it is the sentence Brett is actually being asked to ratify.
   The rest of the packet — `tasks.md`, `design.md`, spec deltas,
   `supporting-docs/`, `evidence/` — is deliberately NOT ruled here.
5. **The 68 standing violations are sequenced before the code lands**, not
   after. A gate that goes red on the commit that introduces it teaches
   people to skip the gate.

## Impact

- Affected specs: `doc-health` (MODIFIED `Deterministic check families`,
  ADDED `Governed corpus membership and the lifecycle scan set`);
  `document-lifecycle` (ADDED `Proposal packets carry the lifecycle header`).
- Affected code: `scripts/doc_health/{corpus,runner,families}.py`,
  `tests/doc-health/`. No contract schema, no digest set, no release tag.
- Affected docs: `docs/document-lifecycle.md` § Status Claim Rules, README
  Active row.
- Nightly: the canon-share metric does not move. Under option (a) it would
  fall 12.2 points on the six-repo aggregation, which would read as a corpus
  collapse and would be an artifact of the measurement changing.
- New standing findings on the day the code lands: 20 critical + 48 error,
  unless §5 of tasks discharges them first, which is what §5 is for.

## Open Questions

**OQ-1 — Which option?** RECOMMENDED: **(b), the scoped lifecycle scan set.**
(a) full membership costs 573 findings, 13 canon-share points and 123 test
failures, and fires falsely at least five times. (c) test-only costs the same
68 dispositions with no severity, no class and no disposition route.

**OQ-2 — What exactly is in the scan set?** RECOMMENDED:
`openspec/changes/**/proposal.md` + `openspec/changes/**/review/*.md`, 118
documents. Alternatives: proposal files alone (107 documents — drops
`ratified-provenance` from 20 fires to 17, losing the three review
ratification records, which are precisely the documents whose whole job is to
record a ratification); or the whole of `openspec/` (663 documents — adds 488
"missing status header" errors on working files and reintroduces the
source-snapshot and grammar-marker false positives).

**OQ-3 — Which families read it?** RECOMMENDED: the four lifecycle-conformance
families — `status-validity`, `standard-backing`, `ratified-provenance`,
`succession-integrity`. Explicitly out: `location-conformance` and
`tag-hygiene` (measured false positives), `staged-candidate-aging` (same),
`record-immutability` (its meaning over an archived packet is genuinely
unsettled — see OQ-6), and every census, word-count, canon-share, inventory
and catalog consumer.

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

**OQ-5 — The three `review/ratification-*.md` records use a THIRD vocabulary.**
They carry `Ratifier:` and `Decision date:` headers — better provenance than
most of the corpus, in a spelling no rule knows. RECOMMENDED: add a
conforming `Ratified:` line to each (they already name approver and date, so
this is one line and invents nothing). Alternative: sanction `Ratifier:` +
`Decision date:` as a third spelling, which reopens what
`sanction-ratified-record-spelling` closed six weeks ago. Alternative:
exclude `review/` from the set, which costs the three fires OQ-2 exists to
keep.

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
