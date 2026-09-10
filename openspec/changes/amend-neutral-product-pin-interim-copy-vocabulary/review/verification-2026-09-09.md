# Verification record: amend-neutral-product-pin-interim-copy-vocabulary, 2026-09-09

Status: record
Kind: report
Date: 2026-09-09
Ratified by: amend-neutral-product-pin-interim-copy-vocabulary — 2026-09-09, Brett Heap, "Ratify with TOLERATED" (record `review/ratification-2026-09-09.md`)

**RE-RUN 2026-09-10T00:35Z ON `5525a40e` PLUS THE RE-DERIVE COMMIT THAT CARRIES
THIS RECORD.** Every figure below was taken again, from zero, on the corrected
tree — after the bench fixes of `feeba1aa`, after `origin/main` was merged at
`5525a40e`, and after BOTH records were rewritten, so both are inside the
lifecycle scan set the doc-health figures are taken over. **NOTHING IS CARRIED
FORWARD** from the run recorded at `d0ddb126`; where a figure is unchanged from
that run it is unchanged because it was measured again and came out the same.

**THE DECISION DATE IS STILL 2026-09-09; THE RE-RUN IS 2026-09-10.** Brett
Heap's ratifying word was recorded on PR #870 at 2026-09-09T23:31:12Z, so the
`Decision date:`, `approved_on`, and both record file names stay 2026-09-09. The
two CORRECTIVE rulings — *"Keep the clause, fix the accounting"* and *"Follow
canon: Status: ratified"* — were given at 2026-09-10T00:20:16Z, and this re-run
is their evidence. The UTC day boundary is crossed by the CORRECTION, never by
the ratification.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| clone | fresh `https://github.com/opensoft/openxFactory.git`, isolated from the shared checkout |
| head the ratification was authorized on | `d42dbf6b` (word), encoded at `d0ddb126` |
| bench-fix commit | `feeba1aa` — *"Say what the two bullets actually change, and drop the stale draft wording from the ratified proposal (#870 bench)"* |
| merge taken BEFORE the re-derive | `5525a40e` (`Merge origin/main into change/amend-neutral-product-pin-interim-copy-vocabulary`) |
| `origin/main` at this verification | `9c0e2cda` (was `8480378a` at the `d0ddb126` run) |
| doc-health control tree | `5525a40e` — the SAME tree minus the re-derived records |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `TZ=UTC`, `openspec` CLI **1.2.0** |

**THE MERGE WAS TAKEN FIRST, ON PURPOSE, AND FOR THE SECOND TIME.**
`origin/main` had moved from `8480378a` to `9c0e2cda` while the bench ran, so it
was merged at `5525a40e` BEFORE the records were re-derived. Every figure here
is therefore derived on a tree that already carries current `main`, and **no
merge-and-re-measure is owed at landing**.

## 1. `openspec validate amend-neutral-product-pin-interim-copy-vocabulary --strict`

```
Change 'amend-neutral-product-pin-interim-copy-vocabulary' is valid
```

**Exit code 0.** The packet's own delta is strict-valid on the corrected tree.
The corrective commit `feeba1aa` touched ONE line of
`specs/neutral-product-pin/spec.md` — line 188, the `Removed from canon`
marker's REASON text — and no scenario title, no `WHEN`/`THEN`/`AND` bullet, no
requirement body paragraph and no requirement header moved.

## 2. `openspec validate --all --strict`

```
Totals: 98 passed, 3 failed (101 items)
```

**Exit code 1**, and **the failure SET is byte-identical to `origin/main`'s**.
The three failures, on both sides:

| failing item | on `origin/main` `9c0e2cda` | on the re-derived tree |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control, run in a separate worktree of `9c0e2cda`, reports
`Totals: 97 passed, 3 failed (100 items)`. **The re-derived tree differs by
exactly ONE item and that item PASSES** — this change itself, which is the 101st
item and is counted in the 98. **This packet adds nothing to the failure set and
removes nothing from it.**

### `spec/neutral-product-pin` fails on `main` today, and this packet neither inherits nor fixes it

```
Specification 'neutral-product-pin' has issues
✗ [ERROR] requirements.16.text: Requirement must contain SHALL or MUST keyword
```

**THIS IS A PRE-EXISTING FAILURE OF PROMOTED CANON AND IT IS NOT THIS PACKET'S.**
It is stated here because the packet modifies a requirement of that same
specification and the coincidence would otherwise be read as inheritance:

- **It is a DIFFERENT requirement.** `requirements.16` is *A pinned artifact
  that resolves dependencies at install time carries a vendored lockfile, and
  the install runs through it* (`openspec/specs/neutral-product-pin/spec.md:645`),
  whose first body line opens *"Where a pinned external neutral product is
  distributed as a published artifact"* — no SHALL, no MUST. **This packet
  modifies requirement index 9**, *A consumption pin that another repository
  reads is a PUBLISHED contract member, adopted by pin-sync*, whose first body
  line is *"A consumption pin SHALL be a PUBLISHED contract member…"*.
- **It is a DIFFERENT KIND of defect.** The failure is structural — the parser
  reads only the FIRST LINE of a requirement's body when checking for
  SHALL/MUST, and requirement 16's first line carries neither keyword. This
  packet's defect is a vocabulary collision inside a requirement that already
  validates.
- **NOT INHERITED**: the packet's own change item validates clean (§ 1) —
  `openspec` scores a change delta on the delta, not on the state of the
  specification it will eventually be promoted into.
- **NOT FIXED, AND DELIBERATELY SO.** Repairing requirement 16's first line
  would edit promoted, ratified canon, which needs its own word under working
  rule 3. `tasks.md` § 5.2 records it as an OWED SUCCESSOR and leaves the box
  OPEN. Neither *"Ratify with TOLERATED"* nor either corrective ruling of
  2026-09-10 reaches it.

## 3. `python3 scripts/proposal-support.py . verify amend-neutral-product-pin-interim-copy-vocabulary`

```
proposal support verification ok
```

**Exit code 0.** This is the gate that reads the origin declaration, so it is
the gate that confirms the approval pair was ADDED beside the drafting
provenance rather than substituted for it: `kind: ad_hoc` and
`id: openxFactory:adhoc:2026-09-09-amend-neutral-product-pin-interim-copy-vocabulary`
are unmoved, `reason`/`proposed_by`/`proposed_on` are byte-unchanged, and
`approved_by`/`approved_on` are new keys following `proposed_on`.

**THIS GATE IS THE MECHANICAL HALF OF THE T2 REFUSAL** (`ratification-2026-09-09.md`
§ 4.4). Copilot asked for `origin.reason`'s drafting-time tense to be rewritten
now that the approval pair exists; the origin-retention arm this gate runs is
written to find those three fields BYTE-UNCHANGED across the ratification, so a
tense edit is a change to a field a gate exists to hold still. `feeba1aa` leaves
`.openspec.yaml` untouched and this gate passes on the corrected tree.

`proposal-support`'s refuse-any-open-box rule applies **at archive**, not here;
`tasks.md` § 4 and § 5.2–§ 5.4 are open by design and this gate passes with them
open because the packet is not being archived.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0.**

### `--ledger-diff`

```
change ids (40 active + 151 archived): 191
co-modified at requirement granularity (each would owe a declaration): 139
sole modifiers (each would declare `sequenced_after: []`): 52
ACTIVE changes: co-modified / sole: 26 / 14
declaring `sequenced_after:`: 16 (… amend-neutral-product-pin-interim-copy-vocabulary …)
declaring an explicit `[]` root claim: 1
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 3 hop(s), from amend-mirror-floor-regeneration-merge-authority

per-change sweep ledger consistent with the corpus (191 rows).
```

**Exit code 0.** The ledger is consistent at **191 rows** and **ZERO rows moved
in the corrective or re-derive commits** — a sweep-ledger row's derived keys read
neither a lifecycle status nor a marker's reason text, so neither a draft→ratified
flip nor the accounting correction moves a row. This change is the corpus's
**one** explicit `[]` root claim.

## 5. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 6. `python3 scripts/doc-health.py --single-repo .`

```
Findings: 10 critical, 6 error, 47 warning, 14 info. New regressions vs previous report: 0.
```

**Exit code 0.** **NO FINDING NAMES THIS CHANGE** —
`grep -c 'amend-neutral-product-pin-interim-copy-vocabulary'` over the full
report returns **0**, with both re-derived records inside the scan set.

### The control that matters: the finding-line diff against the PRE-RE-DERIVE tree

`doc-health --single-repo` was run again on a separate worktree of `5525a40e` —
the SAME tree minus the re-derived records and the `tasks.md` alignment — and the
two reports' finding lines were normalized for the worktree name and diffed:

```
Findings: 10 critical, 6 error, 47 warning, 14 info. New regressions vs previous report: 0.
--- diff pre vs post (re-derived) ---
IDENTICAL   (77 finding lines on both sides)
```

**THE FINDING-LINE DIFF IS EMPTY.** Flipping this record's sibling from
`Status: record` to `Status: ratified` adds **ZERO** findings and removes
**ZERO**. That is the measurement Codex's P1 asked for, taken the other way
round: the earlier `Status: record` header did not merely look wrong, it kept
the ratification record OUT of the `ratified-provenance` arm entirely, and the
corrected header now puts it IN — at no cost, because the citation it already
carried clears the floor.

### The `ratified-provenance` family — the family Codex's P1 named

`python3 scripts/doc-health.py --single-repo . --family ratified-provenance`,
**exit code 0**: **6 critical, and NONE of them this change** (named 0 times).
The six, verbatim from the report:

```
- [critical] openspec/changes/add-sequenced-after-substrate/proposal.md — Ratified by: missing or does not resolve to an OpenSpec change
- [critical] openspec/changes/add-structured-scope-substrate/proposal.md — ratified header carries no citation in either sanctioned spelling
- [critical] openspec/changes/adopt-configured-notebook-hosting-identity/proposal.md — Ratified: names none of an approver, a date, or a resolvable record path
- [critical] openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/proposal.md — ratified header carries no citation in either sanctioned spelling
- [critical] openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/review/ratification-2026-09-05.md — ratified header carries no citation in either sanctioned spelling
- [critical] openspec/changes/mirror-floor-regeneration-automation/proposal.md — ratified header carries no citation in either sanctioned spelling
```

All six are pre-existing and belong to other packets; the count is unchanged
from the `d0ddb126` run.

**THE ARM NOW SCORES THIS RECORD'S SIBLING, WHICH IS THE POINT OF RULING (2).**
Six documents in this packet carry a ratified-or-record header, and each carries
**EXACTLY ONE** citation line — which is what the family counts, one total across
both sanctioned spellings:

| document | header | citation |
| --- | --- | --- |
| `proposal.md` | `Status: ratified` | `Ratified:` (approver, date, verbatim word, record path) |
| `design.md` | `Status: ratified` | `Ratified by:` (change id, date, approver, word, record) |
| `tasks.md` | `Status: ratified` | `Ratified by:` (change id, date, approver, word, record) |
| `review/ratification-2026-09-09.md` | **`Status: ratified`** (was `record`) | `Ratified:` — one line, inside the 15-line header window, with `Ratifier:` and `Decision date:` accompanying it as `document-lifecycle` expressly permits |
| `review/verification-2026-09-09.md` (this file) | `Status: record` | `Ratified by:` |
| the README row | — | full paths to BOTH records (T1) |

### The `record-immutability` family — measured, and it does not reach these records

`python3 scripts/doc-health.py --single-repo . --family record-immutability`,
**exit code 0**: **4 critical, and NONE of them this change** (named 0 times):

```
- [critical] docs/archive-record-discrepancies.md — record document changed after capture
- [critical] docs/domain-ontology-adoption-handoff.md — record document changed after capture
- [critical] docs/domain-ontology-pilot-report.md — record document changed after capture
- [critical] docs/notebook-projection-migration-evidence-2026-08-24.md — record document changed after capture
```

**REWRITING THIS `Status: record` FILE RAISES NO FINDING, AND THE REASON IS
STRUCTURAL RATHER THAN LUCKY.** `govern-openspec-corpus-membership` declares two
document sets. `fam_record_immutability` iterates `ctx.docs`, the GOVERNED CORPUS
— `contracts/`, `docs/`, `examples/`, `ideation/`, `templates/` — while a
`review/` record under an OpenSpec change packet lives in the LIFECYCLE SCAN SET
(`openspec/changes/**/proposal.md` and `openspec/changes/**/review/*.md`), which
`scripts/doc_health/families.py`'s `_lifecycle_scope` serves to exactly four
families: status validity, standard backing, ratified provenance and succession
integrity. Record immutability is not one of them. All four criticals above are
`docs/` documents, and the measurement was taken directly as well as read off the
source: a probe line appended to this file before the re-derive produced no
finding.

## 7. `python3 -m pytest tests/sequenced_after tests/scope_globs tests/doc-health -q`

```
1979 passed, 7 warnings in 412.75s (0:06:52)
```

**Exit code 0.** All three suites green on the re-derived
tree: `tests/doc-health` (which owns `ratified-provenance`,
`record-immutability` and `modified-block-currency`), `tests/sequenced_after`
(the `[]` root claim and the sweep ledger) and `tests/scope_globs`. **No test was
added, changed, skipped or xfailed by this ratification or by its correction** —
`code_surface: none`, and § 9 shows neither commit touches a file under
`scripts/` or `tests/`.

## 8. `modified-block-currency` — the family that reads the marker

`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`,
**exit code 0**, with the class counts the family prints:

```
- scenario-title completeness: 0 (`error` — the arm carrying this family's gate)
- carriage ledger: 9 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)
```

**`marker defects: 0`, and this change is named 0 times in the whole family
report** — none of the nine `carriage ledger` info rows is this packet's. The
corrected reason still carries **NO CODE SPAN**: `parse_marker` splits a
unit-naming marker at the FIRST ` — ` standing outside a code span, reads every
span BEFORE the cut as a named unit and reports every span AFTER it under the
marker-defect class's second ground (`amend-marker-defect-reporting`, issue
#729). Measured on the corrected line: **8 backticks before the cut** — the two
named units, one of them fenced with a doubled run because it contains
`` `openxFactory` `` — and **0 backticks after it**. The marker therefore still
names exactly two units, which is what `tasks.md` § 2.2 claims.

## 9. What these commits do NOT move — verified by diff, not by assertion

Diffed against `d0ddb126`, the head Brett Heap's word of 2026-09-09 was encoded
on:

| surface | command | result |
| --- | --- | --- |
| the ratified delta's NORMATIVE units | `git diff d0ddb126 -- …/specs/` | **ONE LINE: 188, the marker's REASON** |
| promoted canon | `git diff d0ddb126 -- openspec/specs/` | **EMPTY** |
| `.openspec.yaml` (frozen origin + approval pair) | `git diff d0ddb126 -- …/.openspec.yaml` | **EMPTY** |
| `scripts/` and `tests/` | `git diff d0ddb126 --stat -- scripts/ tests/` | **EMPTY** apart from what `5525a40e` merged FROM `origin/main` |

**NO NORMATIVE UNIT OF THE DELTA MOVED.** Ruling (1) was *"Keep the clause, fix
the accounting"*, and that is exactly the shape of the diff: the appended
reservation clause in the `THEN` bullet stands as ratified, and the only edit
inside `specs/` is the marker's reason — a DECLARATION ABOUT the edit, not one of
the units it declares. The seven `TOLERATED`/`tolerated` occurrences D1
enumerated are still at lines 121, 133, 134, 170, 171, 185 and 186.

The corrective commit `feeba1aa` touches four files:

```
README.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/proposal.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/tasks.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/specs/neutral-product-pin/spec.md
```

The re-derive commit carrying this record touches three:

```
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/tasks.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/review/ratification-2026-09-09.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/review/verification-2026-09-09.md
```

No archived change is touched, no promoted specification is touched, and no
other active change's files are touched.

## 10. Independent review

Six review threads stood on the ratified head `d0ddb126` — three from Copilot,
three from Codex (one P1, two P2). **FIVE ARE TAKEN AND ONE IS REFUSED**, and the
full table with each disposition is `ratification-2026-09-09.md` § 4.3, with the
refusal argued at § 4.4. The earlier rounds — Copilot "Approval recommended"
twice (`9c26a97c`, `d42dbf6b`) and one Codex round on `9c26a97c` whose two
findings were taken at `d42dbf6b` — are recorded at § 4.1–4.2. Sourcery is an
upsell stub on this repository and its comment is an ABSENCE, not a review.

**A FRESH `@codex review` IS REQUESTED ON THE RE-DERIVED HEAD** in the same
comment that announces these records, and dispositioning it is a freeze
obligation on this lane rather than a claim this record makes. **This lane
encodes, corrects and freezes; it does not merge.**
