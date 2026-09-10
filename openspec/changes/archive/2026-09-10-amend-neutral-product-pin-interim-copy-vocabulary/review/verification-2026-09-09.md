# Verification record: amend-neutral-product-pin-interim-copy-vocabulary, 2026-09-09

Status: record
Kind: report
Date: 2026-09-09
Ratified by: amend-neutral-product-pin-interim-copy-vocabulary — 2026-09-09, Brett Heap, "Ratify with TOLERATED" (record `review/ratification-2026-09-09.md`)

**EVERY FIGURE BELOW IS RE-DERIVED ON THE RATIFIED TREE**, after the status
flips, the citation lines, the approval pair, the README row and BOTH records
were written — so both of these records are inside the lifecycle scan set the
doc-health figures are taken over. Nothing is carried forward from the
pre-ratification measurement in the pull request body.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| clone | fresh `https://github.com/opensoft/openxFactory.git`, isolated from the shared checkout |
| frozen head the ratification was authorized on | `d42dbf6b` |
| `origin/main` at verification | `8480378a` |
| merge taken BEFORE the ratification commit | `ce35a098` (`Merge origin/main into change/amend-neutral-product-pin-interim-copy-vocabulary`) |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `TZ=UTC`, `openspec` CLI **1.2.0** |

**THE MERGE WAS TAKEN FIRST, ON PURPOSE.** `origin/main` had moved past the
branch's previous merge, so `origin/main` was merged at `ce35a098` BEFORE the
ratification encode. Every figure in this record is therefore derived on a tree
that already carries current `main`, and **no merge-and-re-measure is owed at
landing** — which is the one obligation the comparable record of
`amend-marker-defect-reporting` had to carry forward.

**A NOTE ON THE DATE, STATED RATHER THAN LEFT TO BE FOUND.** The ratification
date, both record file names and `approved_on` are all **2026-09-09**, and so is
the encode: Brett Heap's word was recorded on PR #870 at **2026-09-09T23:31:12Z**
and the ratification commit's own author timestamp is **2026-09-09T23:47:07Z**.
The word, the encode and every date written into the packet therefore fall on
ONE UTC day, with no boundary crossed and nothing to reconcile — consistent
across `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, the README row
and both record file names.

## 1. `openspec validate amend-neutral-product-pin-interim-copy-vocabulary --strict`

```
Change 'amend-neutral-product-pin-interim-copy-vocabulary' is valid
```

**Exit code 0.** The packet's own delta is strict-valid on the ratified tree.

## 2. `openspec validate --all --strict`

```
Totals: 98 passed, 3 failed (101 items)
```

**Exit code 1**, and **the failure SET is byte-identical to `origin/main`'s**.
The three failures, on both sides:

| failing item | on `origin/main` `8480378a` | on the ratified tree |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control, run in a separate worktree of `8480378a`, reports
`Totals: 97 passed, 3 failed (100 items)`. **The ratified tree differs by
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
  OPEN. Brett Heap's *"Ratify with TOLERATED"* does not reach it.

## 3. `python3 scripts/proposal-support.py . verify amend-neutral-product-pin-interim-copy-vocabulary`

```
proposal support verification ok
```

**Exit code 0.** This is the gate that reads the origin declaration, so it is
the gate that confirms the approval pair was ADDED beside the drafting
provenance rather than substituted for it: `kind: ad_hoc` and
`id: openxFactory:adhoc:2026-09-09-amend-neutral-product-pin-interim-copy-vocabulary`
are unmoved, `reason`/`proposed_by`/`proposed_on` are byte-unchanged, and
`approved_by`/`approved_on` are new keys following `proposed_on`. The support
manifest that repeats `kind` and `id` therefore does not come to disagree with
the packet, and the archive gate's origin-retention arm reads the declaration
this commit establishes.

`proposal-support`'s refuse-any-open-box rule applies **at archive**, not here;
`tasks.md` § 4 and § 5.2–§ 5.4 are open by design and this gate passes with them
open because the packet is not being archived.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0.** `sequenced_after: []` stands as a POSITIVE root claim, which is
the machine-readable form of the ordering measurement quoted in
`ratification-2026-09-09.md` § 6: `split-opendox-two-layer-product` is the only
other active `neutral-product-pin` delta, it modifies two OTHER requirements of
the same specification, the two blocks share a spec FILE and no requirement key,
and no ordering declaration is owed in either direction.

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
in this commit** — a sweep-ledger row's derived keys read no lifecycle status, so
a draft→ratified flip moves no row. This change is the corpus's **one** explicit
`[]` root claim.

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
report returns **0**, with both new records inside the scan set.

### The control that matters: the finding-line diff against the PRE-RATIFICATION tree

`doc-health --single-repo` was run again on a separate worktree of `ce35a098` —
the SAME tree minus the ratification encode — and the two reports' finding lines
were normalized for the worktree name and diffed:

```
Findings: 10 critical, 6 error, 47 warning, 14 info. New regressions vs previous report: 0.
--- diff pre vs post (ratified) ---
IDENTICAL
```

**THE FINDING-LINE DIFF IS EMPTY.** The status flips, the five citation lines,
the approval pair, the README row and both new records add **ZERO** findings and
remove **ZERO** findings. A ratification is exactly the kind of edit that can
introduce a `ratified-provenance` critical or a missing-status-header finding by
accident; this one introduces neither, and the proof is a byte-level diff rather
than a matching total.

### The `ratified-provenance` family — the family this act could have broken

`python3 scripts/doc-health.py --single-repo . --family ratified-provenance`,
**exit code 0**: **6 critical, and NONE of them this change** (named 0 times).
The family's rule is *"ratified header carries no citation in either sanctioned
spelling"*, and the six criticals it reports belong to other packets
(`archive/2026-09-05-mirror-floor-addition-grace` and
`mirror-floor-regeneration-automation` among them) and are pre-existing.

**This is the arm that scores the encode**, because a `Status: ratified` header
with no citation, or with more than the sanctioned one, is exactly what a
careless ratification produces. Five documents in this packet now carry a
ratified-or-record header and each carries **EXACTLY ONE** citation line:

| document | header | citation |
| --- | --- | --- |
| `proposal.md` | `Status: ratified` | `Ratified:` (approver, date, verbatim word, record path) |
| `design.md` | `Status: ratified` | `Ratified by:` (change id, date, approver, word, record) |
| `tasks.md` | `Status: ratified` | `Ratified by:` (change id, date, approver, word, record) |
| `review/ratification-2026-09-09.md` | `Status: record` | `Ratified:` |
| `review/verification-2026-09-09.md` | `Status: record` | `Ratified by:` |

## 7. `python3 -m pytest tests/sequenced_after tests/scope_globs tests/doc-health -q`

```
1968 passed, 7 warnings in 388.78s (0:06:28)
```

**Exit code 0.** All three suites green on the ratified tree: `tests/doc-health`
(which owns `ratified-provenance` and `modified-block-currency`),
`tests/sequenced_after` (the `[]` root claim and the sweep ledger) and
`tests/scope_globs`. **No test was added, changed, skipped or xfailed by this
ratification** — `code_surface: none`, and § 8 shows the commit touches no file
under `scripts/` or `tests/`.

## 8. What this commit does NOT move — verified by diff, not by assertion

Diffed against the frozen head `d42dbf6b` the word was given on:

| surface | command | result |
| --- | --- | --- |
| the ratified DELTA's wording | `git diff d42dbf6b -- openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/specs/` | **EMPTY** |
| promoted canon | `git diff d42dbf6b -- openspec/specs/` | **EMPTY** |

**THE DELTA'S BYTES ARE UNTOUCHED, WHICH IS WHAT THE RULING REQUIRED.** D1 was
resolved as TOLERATED — the option already encoded — so the ruling is applied by
leaving the requirement text exactly as the bench reviewed it. The seven
enumerated occurrences at `specs/neutral-product-pin/spec.md` lines 121, 133,
134, 170, 171, 185 and 186 stand as written. **No promoted canon, no script, no
test, no contract, no schema and no workflow is edited by this ratification.**

The commit's complete file set is five modified files and two new records:

```
README.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/.openspec.yaml
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/design.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/proposal.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/tasks.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/review/ratification-2026-09-09.md
openspec/changes/amend-neutral-product-pin-interim-copy-vocabulary/review/verification-2026-09-09.md
```

No archived change is touched and no other active change's files are touched.

## 9. Independent review

The bench standing on this pull request is recorded in
`ratification-2026-09-09.md` § 4: **Copilot "Approval recommended" twice**
(`9c26a97c` at 21:55:37Z and `d42dbf6b` at 22:12:59Z, the second over 7/7 files
with 0 new comments), and **one Codex round on `9c26a97c`** whose two findings
were TAKEN at `d42dbf6b` — the README code-span edit and the D1 replacement-set
count. **As of this record Codex has NOT reviewed `d42dbf6b`**, so no Codex pass
stands on the tree that carries its own fixes; a fresh `@codex review` is
requested on the ratification-encoded head, and dispositioning it is a freeze
obligation rather than a claim this record makes. Sourcery is an upsell stub on
this repository and its comment is an ABSENCE, not a review.
