# Verification record: amend-repo-boundary-governance-scope-first-line, ratified tree 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-repo-boundary-governance-scope-first-line — 2026-09-11, Brett Heap, "ratify as encoded" (record `review/ratification-2026-09-11.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-11.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one.

**IT IS A ONE-SHOT CAPTURE.** A dated run report keeps `record`, and a second
run writes a different path rather than rewriting this one. This is the packet's
FIRST and only gate capture; a later re-run writes `verification-<later
date>.md` beside it.

**EVERY FIGURE BELOW WAS TAKEN ON THE RATIFIED TREE, AFTER THE ENCODE AND AFTER
THE MERGE FROM `main`, IN A FRESH CLONE.** Nothing is carried forward from the
pull request body's earlier gate tables; where a figure matches one of those, it
matches because it was measured again and came out the same.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| branch | `change/amend-repo-boundary-governance-scope-first-line` |
| head the ratification word was given over | `d50a1251` |
| merge-from-`main` commit (its own commit, no conflict) | `42725ead` |
| `origin/main` merged in | `f0eea7ed` |
| control run for `--all --strict` | a second worktree at `origin/main` `f0eea7ed` |
| control run for `doc-health` | a second worktree at `42725ead`, the PRE-ratification tree |
| CLI on `PATH` | `openspec` **1.2.0** |
| pinned CLI | `@fission-ai/openspec@1.12.0`, content-verified, 80-package closure |

**BOTH BINARIES ARE RUN, BECAUSE `design.md` D6 IS THE DECISION THEY DISAGREE
ON.** The 1.2.0 binary on `PATH` is the one that reports the first-line defect;
the pinned 1.12.0 is the one every gate in this repository actually uses, and it
does not report it. Section 2 and section 8 are those two runs.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-repo-boundary-governance-scope-first-line --strict`

```
$ OPENSPEC_TELEMETRY=0 openspec validate amend-repo-boundary-governance-scope-first-line --strict
Change 'amend-repo-boundary-governance-scope-first-line' is valid
```

**exit 0.**

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the 1.2.0 binary on `PATH`

```
$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
✓ change/amend-repo-boundary-governance-scope-first-line
…
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
✗ spec/repo-boundary-governance
Totals: 98 passed, 3 failed (101 items)
```

**exit 1**, and the exit code is expected rather than a regression. **THE
FAILURE SET IS IDENTICAL TO `main`'s, NAME BY NAME.** Control run in a second
worktree at `origin/main` `f0eea7ed`:

```
✗ change/disposition-codexfactory-declared-renames
✗ change/disposition-codexfactory-floor-relocation-retitle
✗ spec/repo-boundary-governance
Totals: 97 passed, 3 failed (100 items)
```

**exit 1.** Three failed on both sides, the SAME three, and **this change is the
one extra item** — 100 items on `main`, 101 here — **and it PASSES**. The
pre-ratification tree `42725ead` returns `98 passed, 3 failed (101 items)` with
the same set, so **the ratification encode moved no strict-validation figure at
all**.

**`spec/repo-boundary-governance` IS STILL RED HERE, AND THAT IS THE POINT OF
THE ARCHIVE RATHER THAN A DEFECT OF THE RATIFICATION.** A delta does not edit
the promoted specification, so the requirement whose first body line lacks the
keyword is still the promoted one at this head. `tasks.md` § 5.1 owes the
before-and-after measurement at the archive, which is where the failure clears.

## 3. `python3 scripts/proposal-support.py . verify amend-repo-boundary-governance-scope-first-line`

```
$ python3 scripts/proposal-support.py . verify amend-repo-boundary-governance-scope-first-line
proposal support verification ok
```

**exit 0.** This is the gate that reads the origin declaration, so it is the
mechanical confirmation that the approval pair was ADDED beside a fixed `kind`
and `id` rather than substituted for them.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
$ python3 scripts/validate-sequenced-after.py .
sequenced_after validation passed (39 active changes, 9 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**exit 0.**

```
$ python3 scripts/validate-sequenced-after.py . --ledger-diff
sequenced_after corpus sweep
----------------------------
change ids (39 active + 159 archived): 198
co-modified at requirement granularity (each would owe a declaration): 144
sole modifiers (each would declare `sequenced_after: []`): 54
ACTIVE changes: co-modified / sole: 24 / 15
declaring `sequenced_after:`: 23 (… amend-repo-boundary-governance-scope-first-line …)
declaring an explicit `[]` root claim: 6
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (198 rows).
```

**exit 0.** The ledger row seeded at the bench survives the merge from `main`
unchanged: `main`'s new file landed inside an EXISTING change directory
(`register-gate-rules-council-seats`), so no new corpus row was owed and none
was written. `git diff` over `tests/sequenced_after/corpus-ledger.yaml` across
the ratification encode is **EMPTY** — 0 files.

## 5. `python3 scripts/validate-scope-globs.py .`

```
$ python3 scripts/validate-scope-globs.py .
scope_globs validation passed (all active changes conform).
```

**exit 0.**

## 6. `python3 scripts/doc-health.py --single-repo .`

**exit 0.** Headline, verbatim:

```
Canon share by words: 39.5% (369545 canon words / 934974 governance words, promoted specs included).
Findings: 32 critical, 5 error, 47 warning, 16 info. New regressions vs previous report: 0.
```

`modified-block-currency` — the family that reads this very block — reports, by
class:

```
- scenario-title completeness: 0 (`error` — the arm carrying this family's gate)
- carriage ledger: 10 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)
```

**MARKER-DEFECT FINDING COUNT: 0**, which is the figure `design.md` D2b turns
on — carrying the inherited marker forward would have drawn a ground-three
finding, and not carrying it draws none.

**NOT ONE FINDING IN THE WHOLE REPORT NAMES THIS PACKET.** `grep -c
amend-repo-boundary-governance-scope-first-line` over the report returns **0**,
and the ten `carriage ledger` `info` rows belong to seven other changes.

**THE FINDING-LINE DIFF AGAINST THE PRE-RATIFICATION TREE IS EMPTY.** Control
run at `42725ead` in a second worktree; both reports carry **100** finding lines
and, after normalising the `repo=` identity token (which is the checkout
directory's name and differs between worktrees by construction), `diff` returns
**0 lines**. The ratification encode introduced no finding and cleared none.

**WHY THE PER-STAGE TABLE AND THE CANON SHARE ARE BYTE-IDENTICAL PRE AND POST,
WHICH IS CORRECT AND NOT A STALE READ.** Those figures come from the governed
DOCUMENT corpus (399 documents: `docs/`, `ideation/`, and their kin), and that
corpus contains nothing under `openspec/changes/` — verified by loading the
module directly. The packet's files live in the separate LIFECYCLE SCAN SET
(`openspec/changes/**/proposal.md` and `openspec/changes/**/review/*.md`, 318
documents), and all three of this ratification's lifecycle documents are in it
with the statuses this encode gave them:

```
openspec/changes/amend-repo-boundary-governance-scope-first-line/proposal.md                      status='ratified'  kind=None
openspec/changes/amend-repo-boundary-governance-scope-first-line/review/ratification-2026-09-11.md status='ratified'  kind='report'
openspec/changes/amend-repo-boundary-governance-scope-first-line/review/verification-2026-09-11.md status='record'    kind='report'
```

So the families that read lifecycle documents — `ratified-provenance`,
`status-validity` — did see all three, and reported nothing against any of them.

## 7. `python3 -m pytest tests/doc-health -q`

```
$ python3 -m pytest tests/doc-health -q
1689 passed, 7 warnings in 420.83s (0:07:00)
```

**exit 0.**

**WHAT THIS IS NOT.** It is the `doc-health` suite, not the whole repository
suite. The full `pytest-suite` required check runs on the pull request in CI and
is the authority for the green this landing needs; this capture states the
locally-run subset and does not claim the rest.

## 8. The PINNED 1.12.0 binary — `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
…
spec/repo-boundary-governance
  ℹ [INFO] requirements[10]: Requirement text is very long (>500 characters). Consider breaking it down.
  ℹ [INFO] requirements[1]: Requirement text is very long (>500 characters). Consider breaking it down.
  ℹ [INFO] requirements[6]: Requirement text is very long (>500 characters). Consider breaking it down.
  ℹ [INFO] requirements[7]: Requirement text is very long (>500 characters). Consider breaking it down.
  ℹ [INFO] requirements[8]: Requirement text is very long (>500 characters). Consider breaking it down.
  ℹ [INFO] requirements[9]: Requirement text is very long (>500 characters). Consider breaking it down.
…
Totals: 99 passed, 2 failed (101 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

**exit 0.** **`spec/repo-boundary-governance` IS AMONG THE PASSES**, with
**six** `INFO` notes and no `ERROR` — the asymmetry `design.md` D6 was put on,
re-measured on the ratified tree rather than recalled. The two failures are the
two DISPOSITIONED scenario-omission findings accepted on Brett Heap's word of
2026-09-05 *"take exit 2"* (`add-chain-attestation` / `signed-execution-chain`,
`add-composed-view-authoring` / `ideation-dashboard`); neither is related to
this requirement and neither is touched here.

**SO THE RECORD STATES BOTH VERDICTS SIDE BY SIDE**, which is what the decision
required:

| binary | `spec/repo-boundary-governance` | corpus totals | exit |
| --- | --- | --- | --- |
| 1.2.0 on `PATH` | **✗ FAILS** — the first-line defect, cleared at the ARCHIVE and not here | 98 passed, 3 failed (101 items) | 1 |
| 1.12.0, pinned | **✓ PASSES** — six `INFO` notes, no error | 99 passed, 2 failed (101 items), both dispositioned | 0 |

## 9. What the encode does NOT move — verified by diff, not by assertion

| claim | proof |
| --- | --- |
| **The delta's bytes are untouched.** | `git diff --name-only -- openspec/changes/amend-repo-boundary-governance-scope-first-line/specs/` → **0 files**. D1 was ruled to the option already encoded, so the ruling is applied by leaving the text alone. |
| **The sweep ledger is untouched.** | `git diff --name-only -- tests/sequenced_after/corpus-ledger.yaml` → **0 files**. |
| **Nothing under `openspec/specs/` moves.** | No promoted file is in the change set; promotion is the ARCHIVE's act. |
| **The `origin:` block is byte-unmoved.** | `.openspec.yaml` lines 1–116 (`kind`, `id`, `reason`, `proposed_by`, `proposed_on`) hash to sha256 `34746842eefd8ebcc46109c3d1643ef59d9c1253984148a00a2da528c2a06afe` both before and after the encode. |
| **The approval pair is an ADDITION, not a rewrite.** | `git diff --numstat` on `.openspec.yaml` reads **`40  0`** — forty lines added, zero removed. |

Whole-encode `git diff --numstat`:

```
38	18	README.md
40	0	openspec/changes/amend-repo-boundary-governance-scope-first-line/.openspec.yaml
58	16	openspec/changes/amend-repo-boundary-governance-scope-first-line/design.md
42	18	openspec/changes/amend-repo-boundary-governance-scope-first-line/proposal.md
92	47	openspec/changes/amend-repo-boundary-governance-scope-first-line/tasks.md
```

plus the two new files under `review/`.

## 10. Independent review

Copilot reviewed every head of this pull request and its five threads were all
TAKEN before the word arrived; Codex never reviewed it at any head, having
answered the one review request with a usage-limit notice, which is recorded as
an ABSENCE and not as approval. The bench dispositions, including the one
suppressed finding REFUSED with its three reasons, are in
`review/ratification-2026-09-11.md` § 4 rather than repeated here.
