# Verification record: amend-neutral-product-pin-lockfile-first-line, ratified tree 2026-09-10

Status: record
Kind: report
Date: 2026-09-10
Ratified by: amend-neutral-product-pin-lockfile-first-line — 2026-09-10, Brett Heap, "ratify as encoded" (record `review/ratification-2026-09-10.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-10.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one.

**IT IS ALSO A ONE-SHOT CAPTURE.** `document-lifecycle` holds that a dated run
report keeps `record` and that *"a second run of such a generator writes a
different path rather than rewriting the same one"*. This is the packet's FIRST
and only gate capture and it is written at its own dated path; a later re-run
writes `verification-<later date>.md` beside it rather than editing this file.

**EVERY FIGURE BELOW WAS TAKEN ON THE RATIFIED TREE, AFTER THE ENCODE, IN A
FRESH CLONE, WITH BOTH RECORDS PRESENT IN THE LIFECYCLE SCAN SET.** Nothing is
carried forward from the pull request body's earlier gate tables; where a figure
matches one of those, it matches because it was measured again and came out the
same. **EVERY FIGURE WAS THEN RE-DERIVED A SECOND TIME AFTER THIS FILE'S OWN
TEXT WAS WRITTEN**, so that the tree these numbers describe is the tree that
carries them, and every one of them came out the same — the only values that
moved between the two rounds are pytest's wall-clock durations.

**ON PATHS.** Command lines are pasted as run. Where a tool echoes the absolute
path of the working clone, that path is written here as `<clone>` — it is a
machine-local scratch directory of no interest to a later reader, and nothing
else in any pasted line is altered.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| clone | fresh `https://github.com/opensoft/openxFactory.git`, isolated from any shared checkout |
| head the ratification was authorized on | `0125741d` — the frozen bench head, the tree Brett Heap ruled on |
| merge from `main` | **ONE, AND IT IS ITS OWN COMMIT.** `origin/main` moved to `52e42be9` while the packet awaited the word, so the branch was merged up at `45b02e31` BEFORE the ratification commit. NO CONFLICT: `52e42be9` ticks three boxes of another lane's `relocate-review-authority-floor-mirror` `tasks.md` and touches no file this packet writes |
| pre-ratification tree | `45b02e31` — the merge commit; the same tree MINUS this encode, in its own worktree |
| tree these figures were taken on | the ratification encode, committed on `change/amend-neutral-product-pin-lockfile-first-line` and carrying this file |
| `origin/main` at this verification | `52e42be9` |
| `--all --strict` control | a separate worktree of `origin/main` `52e42be9` |
| `doc-health` control | the PRE-RATIFICATION tree `45b02e31` |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `openspec` CLI on `PATH` **1.2.0**, pinned CLI **1.12.0**, Python **3.12.3**, node **v22.22.2**, npm **11.19.0** |

**BOTH BINARIES ARE MEASURED HERE, BECAUSE `design.md` D6 IS ABOUT THE
DIFFERENCE BETWEEN THEM** and D6 is the decision the word resolved first. § 2 is
the 1.2.0 binary on `PATH`, where this specification FAILS; § 3 is the pinned
1.12.0 the required check actually runs, where it PASSES. Neither figure moves
at this ratification, and § 2 says why.

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-neutral-product-pin-lockfile-first-line --strict`

```
Change 'amend-neutral-product-pin-lockfile-first-line' is valid
```

**Exit code 0.** The packet's own delta is strict-valid on the ratified tree.
The encode touched no file under the packet's `specs/` directory — § 10 measures
that as an EMPTY diff — so this is the same delta the bench reviewed, validated
again.

## 2. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` (1.2.0 on `PATH`)

```
Totals: 98 passed, 4 failed (102 items)
```

**Exit code 1**, and **the failure SET is IDENTICAL to `origin/main`'s**. The
four failures, on both sides:

| failing item | on `origin/main` `52e42be9` | on the ratified tree |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `change/disposition-codexfactory-floor-relocation-retitle` | ✗ | ✗ |
| `spec/neutral-product-pin` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control, run in a separate worktree of `52e42be9`, reports
`Totals: 97 passed, 4 failed (101 items)`, exit code 1. **The ratified tree
differs by exactly ONE item and that item PASSES** — this change itself, which
renders `✓ change/amend-neutral-product-pin-lockfile-first-line`. `diff` over
the two sorted `✗` lists is EMPTY. **This packet adds nothing to the failure set
and removes nothing from it.**

### `spec/neutral-product-pin` STILL FAILS, AND THAT IS THE CORRECT STATE

It is the very failure this packet exists to answer:

```
$ OPENSPEC_TELEMETRY=0 openspec validate neutral-product-pin --strict --type spec
Specification 'neutral-product-pin' has issues
✗ [ERROR] requirements.16.text: Requirement must contain SHALL or MUST keyword
```

**A DELTA DOES NOT EDIT THE PROMOTED SPECIFICATION.** Nothing under
`openspec/specs/` is touched by this pull request, so the promoted requirement
still opens its body with `Where a pinned external neutral product …` and 1.2.0
still errors on it. **THE ARCHIVE ACT IS WHAT CLEARS THIS**, by promoting the
`## MODIFIED` block into the specification — a separate act on a separate word,
`tasks.md` § 5. This record states it rather than letting a later reader
discover a red item and read it as a regression. The other three failures are
pre-existing, none is a `doc-health` item, and this packet edits no file any of
them reads.

## 3. `python3 scripts/validate-openspec-cli-pin.py --all --no-cache` (the pinned 1.12.0)

This is the form `.github/workflows/openspec-cli-pin-gate.yml` runs. The
entrypoint's own `--strict` flag is *"accepted and IGNORED: strict is always
on"*, so `tasks.md` § 4.3's `--all --strict` and this `--all --no-cache` are the
same act with and without artifact reuse.

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
-> …/node_modules/.bin/openspec validate --all --strict --json  (in <clone>)
…
Totals: 100 passed, 2 failed (102 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

**Exit code 0.** The `origin/main` `52e42be9` control, run the same way in its
own worktree, reports `Totals: 99 passed, 2 failed (101 items)`, **exit code
0** — one item fewer, and the one item is this change, which passes.

**`spec/neutral-product-pin` IS AMONG THE PASSES ON THIS BINARY**, carrying INFO
notes only (`Requirement text is very long (>500 characters)`, nineteen of them
across the file) and no `✗`. **THAT IS D6's WHOLE POINT**: the failure this
amendment answers is real on the binary an engineer or an agent has on `PATH`
and is reported by NO required check. The ruling of 2026-09-10 amended anyway,
with this measurement in front of the owner.

The two failures are the two DISPOSITIONED scenario-omission findings accepted
on Brett Heap's word of 2026-09-05 *"take exit 2"* — `add-chain-attestation` /
`signed-execution-chain` and `add-composed-view-authoring` /
`ideation-dashboard`. Neither is this packet's, neither is related to this
requirement, and this packet neither renews nor retires either one.

## 4. `python3 scripts/proposal-support.py . verify amend-neutral-product-pin-lockfile-first-line`

```
proposal support verification ok
```

**Exit code 0**, on the ratified tree — so the support manifest, whose `kind`
and `id` repeat `.openspec.yaml`'s, still agrees with the packet after the
approval pair was ADDED beside a fixed origin identity. That agreement is the
reason the addition-not-rewrite shape is used, and this run is the measurement
of it rather than the argument for it.

## 5. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (40 active changes, 10 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for the UTC date of the commit that added it, or is dispositioned in place; 12 disposition(s) in force, enforcement error).
```

**Exit code 0.** And `python3 scripts/validate-sequenced-after.py . --ledger-diff`:

```
per-change sweep ledger consistent with the corpus (196 rows).
```

**Exit code 0.** The ledger is unchanged by this encode — `git diff 0125741d --
tests/sequenced_after/corpus-ledger.yaml` is EMPTY — because the two rows this
pull request moves were seeded at `44020530`, before the freeze, through the
sanctioned `--seed-ledger --moved-by '#923'` path. This change is one of the
corpus's **4** explicit `[]` root claims, and one of **21** changes declaring
the `sequenced_after:` field.

## 6. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 7. `python3 scripts/doc-health.py --single-repo .`

```
Canon share by words: 39.7% (367584 canon words / 924910 governance words, promoted specs included).
Findings: 32 critical, 5 error, 47 warning, 16 info. New regressions vs previous report: 0.
```

**Exit code 0**, and **NO FINDING NAMES THIS CHANGE**: `grep -c
amend-neutral-product-pin-lockfile-first-line` over the report is **0**.

**THE FINDING-LINE DIFF AGAINST THE PRE-RATIFICATION TREE `45b02e31` IS EMPTY**
— **100 finding lines on each side, byte-identical** once the repository label
(the clone's directory name) is normalized. The ratification encode therefore
adds no finding and removes none, which is measured here rather than asserted.

By family, on the ratified tree: `ratified-provenance` **28** (all critical,
**none of them this change**), `staged-candidate-aging` 24,
`staged-topic-template` 22, `modified-block-currency` **11**,
`record-immutability` **4** (**none of them this change**), `tag-hygiene` 4,
`ideation-routing` 4, `status-validity` 1, `release-tag-publication` 1,
`document-catalog` 1. **`marker-defect`: 0 findings in the whole run.**

**THE FAMILY THAT READS THIS VERY BLOCK REPORTS NOTHING ABOUT IT.**
`modified-block-currency` reads every active `## MODIFIED` block by
construction and reports 11 findings across **NINE other active changes** in
this same run — `add-chain-attestation`, `add-composed-view-authoring`,
`add-credential-escrow-checkout`, `add-doxchat-model-intake`,
`adopt-configured-notebook-hosting-identity`,
`amend-mirror-floor-regeneration-merge-authority`,
`declare-client-standing-policy-contract`, `qualify-avatar-live-voice` and
`relocate-review-authority-floor-mirror` — and **nothing** about this one.

### 7.1 ONE FIGURE OF `tasks.md` § 4.7 IS CORRECTED AT THIS RATIFICATION

`tasks.md` § 4.7 was authored reading *"**exit 1** on both trees (its ordinary
state on this corpus, which reports findings rather than gating on zero)"*.
**THAT EXIT CODE IS WRONG AND IT IS CORRECTED IN PLACE, WITH THE SUPERSEDED
CLAUSE QUOTED RATHER THAN DELETED.** The mechanism is in the tool:
`scripts/doc_health/runner.py` returns 1 only under `--fail-on` (`if
args.fail_on: … return 1`) and returns `0` otherwise, and this command passes no
`--fail-on`. Measured on both trees at this verification:

```
$ python3 scripts/doc-health.py --single-repo .   # ratified tree
EXIT=0
$ python3 scripts/doc-health.py --single-repo .   # pre-ratification tree 45b02e31
EXIT=0
```

**EVERY OTHER FIGURE IN THAT BOX WAS RE-MEASURED AND IS CORRECT**: the four
severity counts, the zero new regressions, the zero findings naming this change,
the 100 byte-identical finding lines, and the eleven `modified-block-currency`
findings across nine other active changes. Only the exit code was misread. The
correction moves no delta byte, no requirement, no marker and no decision, and
it is disclosed here and in the pull request body rather than made quietly.

## 8. `python3 -m pytest tests/doc-health -q`

```
1684 passed, 7 warnings in 413.77s (0:06:53)
```

**Exit code 0.** And the three suites `tasks.md` § 4.8 names, `python3 -m pytest
tests/sequenced_after tests/scope_globs tests/proposal-support -q`:

```
489 passed, 67 subtests passed in 63.94s (0:01:03)
```

**Exit code 0.** Both suites were run twice, before and after this file's own
text was written, and the PASS COUNTS — which are what is being verified — are
identical across the pair; only the wall-clock durations differ, and the lines
pasted above are from the second run, on the tree that carries this file.

## 9. `modified-block-currency` — the family that reads this very block, re-derived

Run against `scripts/doc_health/modified_block_currency.py` on the ratified
tree, resolving the block against promoted canon (`resolve` status `canon`,
basis `openspec/specs/neutral-product-pin/spec.md`):

| measure | value |
| --- | --- |
| canon units in the promoted requirement | **25** — 9 body, 4 scenario titles, 12 scenario bullets |
| units in this change's block | **25** — 9 body, 4 scenario titles, 12 scenario bullets |
| uncarried canon units | **1** — the retired first sentence, `Where a pinned external neutral product …` |
| added block units | **1** — its replacement, `The pin SHALL carry a VENDORED RESOLUTION where …` |
| markers in the block | **1** |
| suppressed | **1** |
| **marker defects** | **0** |
| undeclared-unit set (the ledger arm) | **EMPTY** |
| marker form / change id / date | `removed` / `amend-neutral-product-pin-lockfile-first-line` / `2026-09-10` |
| marker names / quoted spans | **1** / **0** |
| code spans in the marker's reason | **0**, in a **1,167**-character reason |
| the four canon scenario titles | carried, **equal in order** |

**EVERY NUMBER `tasks.md` § 3.3 AND § 3.6 CLAIM IS REPRODUCED ON THE RATIFIED
TREE**, and the marker's shape is what keeps it unreportable under the existing
second marker-defect ground and under both grounds the ACTIVE
`amend-marker-declaring-nothing` (PR #908) adds.

## 10. What the encode does NOT move — verified by diff, not by assertion

Against the frozen bench head `0125741d`, on the ratified tree:

| diff | result |
| --- | --- |
| `git diff 0125741d -- openspec/changes/amend-neutral-product-pin-lockfile-first-line/specs/` | **EMPTY** — the delta the bench reviewed is the delta that is ratified |
| `git diff 0125741d -- openspec/specs/` | **EMPTY** — no promoted canon is touched |
| `git diff 0125741d -- scripts/ tests/ contracts/ .github/ specs/` | **EMPTY** — no script, test, contract, workflow, schema or Speckit build record moves |
| `git diff 0125741d -- tests/sequenced_after/corpus-ledger.yaml` | **EMPTY** — no ledger row moves |
| `git diff --name-only 0125741d -- openspec/changes/archive/` | **EMPTY** — no archived change is touched |

**THE ENCODE ITSELF TOUCHES EXACTLY FIVE TRACKED FILES AND ADDS TWO**, measured
against the merge commit `45b02e31` with `git diff --numstat`:

```
33  13  README.md
48   0  openspec/changes/amend-neutral-product-pin-lockfile-first-line/.openspec.yaml
53  10  openspec/changes/amend-neutral-product-pin-lockfile-first-line/design.md
45  18  openspec/changes/amend-neutral-product-pin-lockfile-first-line/proposal.md
95  57  openspec/changes/amend-neutral-product-pin-lockfile-first-line/tasks.md
```

plus the two new records under `review/`. **`.openspec.yaml` READS `48 0` — A
PURE ADDITION**, which is the addition-not-rewrite shape stated as a number: the
`origin:` block's `kind`, `id`, `reason`, `proposed_by` and `proposed_on` are
byte-unmoved, and the approval pair is appended beside them. The one other
active change appearing in a diff against `0125741d` —
`relocate-review-authority-floor-mirror/tasks.md` — is `52e42be9` arriving
through the merge commit, not the encode: it is absent from the diff against
`45b02e31` above.

`tasks.md` § 5 (archive) and § 6.1 stay UNTICKED. The archive is a separate act
on a separate word, so openxFactory #882 closes AT THE ARCHIVE and not at this
landing, which is why this pull request carries no closing keyword and
`closingIssuesReferences` is `[]`.

## 11. Independent review, as it stood

Copilot's last verdict on the ruled head `0125741d`, 2026-09-10T19:36:54Z:
*"🟢 Approval recommended — The changes are internally consistent, limited to
adding a draft OpenSpec packet plus its index/ledger entries, and I did not find
any concrete defects in the modified files."* — 7/7 files reviewed, 0 new
comments. Three review threads were raised across three rounds and **all three
were TAKEN and resolved** before the freeze; they are tabulated in
`review/ratification-2026-09-10.md` § 4.

Codex never reviewed this pull request: the one request, at 19:27:24Z, drew a
usage-limit notice ten seconds later and no review. **That is recorded as an
ABSENCE, not as clearance.** The SonarCloud quality gate passed; Sourcery
produced a reviewer's guide and raised no finding.
