# Verification record: amend-modified-block-currency-standing, ratified tree 2026-09-10

Status: record
Kind: report
Date: 2026-09-10
Ratified by: amend-modified-block-currency-standing — 2026-09-10, Brett Heap, "Ratify as encoded, all four sites" (record `review/ratification-2026-09-10.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-10.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one. The distinction is now MECHANICAL as
well as contractual: since `804a9170` (#878) `ratified-provenance` reads a
`review/ratification-*` record's SUBJECT whatever status it carries, and it
leaves a `verification-*` capture alone.

**IT IS ALSO A ONE-SHOT CAPTURE.** `document-lifecycle` holds that a dated run
report keeps `record` and that *"a second run of such a generator writes a
different path rather than rewriting the same one"*. This is the packet's FIRST
and only gate capture and it is written at its own dated path; a later re-run
writes `verification-<later date>.md` beside it rather than editing this file.

**EVERY FIGURE BELOW WAS TAKEN ON THE RATIFIED TREE, AFTER THE ENCODE, IN A
FRESH CLONE.** Nothing is carried forward from the pull request body's earlier
gate tables; where a figure matches one of those, it matches because it was
measured again and came out the same.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| clone | fresh `https://github.com/opensoft/openxFactory.git`, isolated from any shared checkout |
| head the ratification was authorized on | `ab8247fa` — the frozen bench head, unchanged from the tree Brett Heap ruled on |
| tree these figures were taken on | the ratification encode, committed on `change/amend-modified-block-currency-standing` and carrying this file |
| `origin/main` at this verification | `804a9170` |
| `--all --strict` control | a separate worktree of `origin/main` `804a9170` |
| `doc-health` control | the PRE-RATIFICATION tree `ab8247fa` — the same tree minus this encode |
| merge from `main` | **NONE OWED.** `origin/main` was `804a9170` when the branch was frozen and is `804a9170` now, so the branch already carries current `main` and no merge-and-re-measure is owed at landing |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `TZ=UTC`, `openspec` CLI **1.2.0**, Python **3.12.3** |

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-modified-block-currency-standing --strict`

```
Change 'amend-modified-block-currency-standing' is valid
```

**Exit code 0.** The packet's own delta is strict-valid on the ratified tree.
The encode touched no file under the packet's `specs/` directory — § 9 measures
that as an EMPTY diff — so this is the same delta the bench reviewed, validated
again.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 98 passed, 3 failed (101 items)
```

**Exit code 1**, and **the failure SET is IDENTICAL to `origin/main`'s**. The
three failures, on both sides:

| failing item | on `origin/main` `804a9170` | on the ratified tree |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control, run in a separate worktree of `804a9170`, reports
`Totals: 97 passed, 3 failed (100 items)`. **The ratified tree differs by
exactly ONE item and that item PASSES** — this change itself, which is the 101st
item and renders `✓ change/amend-modified-block-currency-standing`. **This
packet adds nothing to the failure set and removes nothing from it**, and the
two `✗` lists `diff` to zero.

### The three failures are pre-existing and none of them is this packet's

None of the three is a `doc-health` item, and this packet edits no file any of
them reads. The `spec/neutral-product-pin` failure is the
`requirements.16.text` *"Requirement must contain SHALL or MUST keyword"*
defect openxFactory [#882](https://github.com/opensoft/openxFactory/issues/882)
names — a promoted requirement whose first body line carries neither keyword,
which is the parser's documented limit and a structural defect of another
capability entirely. Fixing any of the three would edit promoted canon or
another packet's delta with no word behind it.

## 3. `python3 scripts/proposal-support.py . verify amend-modified-block-currency-standing`

```
proposal support verification ok
```

**Exit code 0.** This is the mechanical half of the origin-block rule: the
gate's origin-retention arm reads `kind`, `id`, `reason` and `proposed_by` as
the drafting lane declared them, and the encode adds `approved_by` and
`approved_on` BESIDE them without touching a byte of the four —
`git diff --numstat ab8247fa -- .../.openspec.yaml` is **`37 0`**, thirty-seven
lines added and **zero removed** (§ 9).

`proposal-support`'s refuse-any-open-box rule applies **at archive**, not here;
`tasks.md` § 5 and § 6.1–§ 6.2 are open by design and this gate passes with them
open because the packet is not being archived.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (39 active changes, 9 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0.**

### `--ledger-diff`

```
change ids (39 active + 153 archived): 192
co-modified at requirement granularity (each would owe a declaration): 140
sole modifiers (each would declare `sequenced_after: []`): 52
ACTIVE changes: co-modified / sole: 26 / 13
declaring `sequenced_after:`: 17 (… amend-modified-block-currency-standing …)
declaring an explicit `[]` root claim: 2
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 3 hop(s), from amend-mirror-floor-regeneration-merge-authority

per-change sweep ledger consistent with the corpus (192 rows).
```

**Exit code 0.** The ledger is consistent at **192 rows** and **ZERO rows moved
by the encode** — a sweep-ledger row's derived keys read neither a lifecycle
status nor a citation line, so a `draft`→`ratified` flip moves no row. This
change is one of the corpus's **two** explicit `[]` root claims (the other is
`amend-neutral-product-pin-interim-copy-vocabulary`, which landed on `main`
before this verification); its row was seeded by the sanctioned tool at
`0cb10273` and is untouched here.

## 5. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 6. `python3 scripts/doc-health.py --single-repo .`

```
Findings: 11 critical, 5 error, 47 warning, 14 info. New regressions vs previous report: 0.
```

**Exit code 0.** **NO FINDING NAMES THIS CHANGE** —
`grep -c 'amend-modified-block-currency-standing'` over the full report returns
**0**, with BOTH new records inside the lifecycle scan set.

### The control that matters: the finding-line diff against the PRE-RATIFICATION tree

`doc-health --single-repo` was run on the pre-ratification tree `ab8247fa` — the
same tree minus this encode — and the two reports' finding lines were compared:

```
--- pre-ratification (ab8247fa) vs ratified ---
IDENTICAL   (77 finding lines on both sides)
```

**THE FINDING-LINE DIFF IS EMPTY.** Flipping three documents from
`Status: draft` to `Status: ratified`, adding one `Ratified:`/`Ratified by:`
citation to each, adding the approval pair and adding two `review/` records adds
**ZERO** findings and removes **ZERO**. The headline counts are identical on
both sides (11 critical, 5 error, 47 warning, 14 info), and *"New regressions vs
previous report: 0"*.

### The `ratified-provenance` family — the family this encode is most exposed to

`python3 scripts/doc-health.py --single-repo . --family ratified-provenance`,
**exit code 0**: **7 critical, and NONE of them this change** (named 0 times).
The seven, verbatim from the report:

```
- [critical] openspec/changes/add-sequenced-after-substrate/proposal.md — Ratified by: missing or does not resolve to an OpenSpec change
- [critical] openspec/changes/add-structured-scope-substrate/proposal.md — ratified header carries no citation in either sanctioned spelling
- [critical] openspec/changes/adopt-configured-notebook-hosting-identity/proposal.md — Ratified: names none of an approver, a date, or a resolvable record path
- [critical] openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/proposal.md — ratified header carries no citation in either sanctioned spelling
- [critical] openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/review/ratification-2026-09-05.md — ratified header carries no citation in either sanctioned spelling
- [critical] openspec/changes/archive/2026-09-10-adopt-codexfactory-repository-identity/proposal.md — ratified header carries no citation in either sanctioned spelling
- [critical] openspec/changes/mirror-floor-regeneration-automation/proposal.md — ratified header carries no citation in either sanctioned spelling
```

All seven are pre-existing and belong to other packets; the count is identical
on the pre-ratification tree. **THE FAMILY SCORES FOUR OF THIS PACKET'S
DOCUMENTS AND EACH CARRIES EXACTLY ONE CITATION**, which is what the family
counts — one total across both sanctioned spellings:

| document | header | citation |
| --- | --- | --- |
| `proposal.md` | `Status: ratified` | `Ratified:` — one line (approver, date, verbatim word, record path) |
| `design.md` | `Status: ratified` | `Ratified by:` — one line (change id, date, approver, word, record) |
| `tasks.md` | `Status: ratified` | `Ratified by:` — one line (change id, date, approver, word, record) |
| `review/ratification-2026-09-10.md` | `Status: ratified` | `Ratified:` — one line inside the 15-line header window, with `Ratifier:` and `Decision date:` accompanying it as `document-lifecycle` expressly permits |
| `review/verification-2026-09-10.md` (this file) | `Status: record` | `Ratified by:` — scored only if the status were `ratified`; the SUBJECT arm does not reach a `verification-*` capture |
| the README row | — | full repo-relative paths to BOTH records |

**THE SUBJECT ARM WAS THE ONE TO GET RIGHT, AND IT IS WHY THE RATIFICATION
RECORD IS `Status: ratified` FROM ITS FIRST COMMIT.** `804a9170` (#878, out of
#877) added a reader that recognizes a ratification record by its PATH
(`review/ratification-*`) or its H1 (`# Proposal Ratification:`) and reports it
CRITICAL whatever status it carries, precisely because a value-scoped family
never opened the fourteen archived records that had drifted to `Status: record`.
This record satisfies both arms on its first commit: `Status: ratified`, one
citation, the H1 the template writes.

### The `record-immutability` family — measured, and it does not reach these records

`python3 scripts/doc-health.py --single-repo . --family record-immutability`,
**exit code 0**: **4 critical, and NONE of them this change** (named 0 times):

```
- [critical] docs/archive-record-discrepancies.md — record document changed after capture
- [critical] docs/domain-ontology-adoption-handoff.md — record document changed after capture
- [critical] docs/domain-ontology-pilot-report.md — record document changed after capture
- [critical] docs/notebook-projection-migration-evidence-2026-08-24.md — record document changed after capture
```

The family iterates the GOVERNED CORPUS (`contracts/`, `docs/`, `examples/`,
`ideation/`, `templates/`) while a `review/` record under a change packet lives
in the LIFECYCLE scan set, so it does not read either record here. **THAT
SILENCE IS A COVERAGE GAP RATHER THAN A LICENCE**, and it is why this capture is
written once at a dated path instead of being rewritten by any later run.

## 7. `python3 -m pytest tests/sequenced_after tests/scope_globs tests/doc-health -q`

```
1979 passed, 7 warnings in 445.81s (0:07:25)
```

**Exit code 0.** All three suites green on the ratified tree: `tests/doc-health`
(which owns `ratified-provenance`, `record-immutability` and
`modified-block-currency`), `tests/sequenced_after` (the `[]` root claim and the
sweep ledger) and `tests/scope_globs`. **No test was added, changed, skipped or
xfailed by this ratification** — `code_surface: none`, and § 9 shows the encode
touches no file under `scripts/` or `tests/`. The three suites read `tests/`
fixtures and the `scripts/` modules under test, both byte-identical to
`ab8247fa` (§ 9), so this figure holds for the committed tree: no markdown this
encode writes is an input to any of them.

## 8. `modified-block-currency` — the family that reads this very block

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

**ALL SEVEN CLASSES ARE ZERO ON THIS BLOCK**, `marker defects: 0`, and this
change is named **0** times in the whole family report — none of the nine `info`
carriage-ledger rows is this packet's; all nine are other active changes
(`add-chain-attestation`, `add-composed-view-authoring`,
`add-credential-escrow-checkout`, `add-doxchat-model-intake`,
`adopt-configured-notebook-hosting-identity`,
`declare-client-standing-policy-contract` and `qualify-avatar-live-voice` ×3).
**The rendered caption *"(`error` — the arm carrying this family's gate)"* is
the running code's own answer to the paragraph this packet retires**, printed by
the checker whose specification the block corrects.

The encode moved no byte of the block, so the family reads the same block it
read at `ab8247fa`: 143 canon units, 154 block units, 5 uncarried, all 5 named
by the marker and suppressed, 0 marker defects, no missing scenario title.

## 9. What the encode does NOT move — verified by diff, not by assertion

Diffed against `ab8247fa`, the frozen head Brett Heap's word was given on:

| surface | command | result |
| --- | --- | --- |
| the ratified delta | `git diff ab8247fa -- openspec/changes/amend-modified-block-currency-standing/specs/` | **EMPTY** |
| promoted canon | `git diff ab8247fa -- openspec/specs/` | **EMPTY** |
| the Speckit build records (`specs/019` included) | `git diff ab8247fa -- specs/` | **EMPTY** |
| `scripts/` and `tests/` | `git diff ab8247fa -- scripts/ tests/` | **EMPTY** |
| contracts and workflows | `git diff ab8247fa -- contracts/ .github/` | **EMPTY** |
| `.openspec.yaml` | `git diff --numstat ab8247fa -- …/.openspec.yaml` | **`37  0`** — thirty-seven lines ADDED, zero removed |

**NO NORMATIVE UNIT OF THE DELTA MOVED, AND THE ORIGIN BLOCK IS BYTE-UNCHANGED.**
The whole encode is five files:

```
README.md
openspec/changes/amend-modified-block-currency-standing/.openspec.yaml
openspec/changes/amend-modified-block-currency-standing/design.md
openspec/changes/amend-modified-block-currency-standing/proposal.md
openspec/changes/amend-modified-block-currency-standing/tasks.md
```

plus the two records this commit adds under
`openspec/changes/amend-modified-block-currency-standing/review/`. No archived
change is touched, no promoted specification is touched, no other active
change's files are touched, and the per-change sweep ledger is not touched.

## 10. Independent review

**SIX THREADS ACROSS SEVEN BENCH ROUNDS, ALL SIX TAKEN, ZERO UNRESOLVED**, every
one of them standing on the pull request before the ratifying word and
dispositioned at the freeze of 2026-09-10T04:45:26Z. Two were Codex findings
(one **P1**, one **P2**, plus a second-round **P2**) and four were Copilot
comments; the full table with each disposition is
`review/ratification-2026-09-10.md` § 4.2, and the ONE thing refused — per-class
disappearance tracking in the checker, a CODE decision out of a
`code_surface: none` packet — is argued at § 4.3 and owed as an OPEN box at
`tasks.md` § 5.3.

**COPILOT'S LAST VERDICT ON THE FROZEN HEAD IS 🔵 *"Needs a closer look"* WITH
ZERO NEW COMMENTS**, on the ground that the packet's correctness *"is primarily
semantic/normative and should receive final human review despite passing
mechanical validation"* — which is the standing of a packet awaiting a
ratification word, and what the word of 2026-09-10 supplies. **CODEX NEVER
REVIEWED `ab8247fa`**: a second `@codex review` at 04:21:10Z drew a usage-limit
notice at 04:21:18Z and no review in twenty-four minutes of bounded polling, and
that is recorded as an ABSENCE rather than as approval
(`review/ratification-2026-09-10.md` § 4.4).

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE.** The Rule 6 LANDING/LANDED
post belongs to the landing lane on a separate landing word.
