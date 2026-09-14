# Verification record: amend-merged-into-empty-tail-standing, ratified tree 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: amend-merged-into-empty-tail-standing — 2026-09-11, Brett Heap, "Ratify as encoded" (record `review/ratification-2026-09-11.md`)

**THIS FILE'S SUBJECT IS THE GATE RUN, NOT THE RATIFICATION**, which is why it
keeps `Status: record` while `review/ratification-2026-09-11.md` carries
`Status: ratified`. `document-lifecycle`'s *A review record records a
ratification* governs that file; the sibling scenario *A review record is not
about a ratification* governs this one.

**IT IS A ONE-SHOT CAPTURE.** This is the packet's FIRST gate capture and it is
written at its own dated path; a later re-run (for instance after a further
merge from `main` before landing) writes `verification-2026-09-11-post-merge.md`
beside it rather than editing this file.

**EVERY FIGURE BELOW WAS TAKEN ON THE RATIFICATION ENCODE, IN THIS LANE'S OWN
FRESH CLONE, AFTER THE ENCODE COMMIT.** Nothing is carried forward unmeasured
from `tasks.md` §§ 4.1–4.9 (the first authoring's own capture, frozen at
`546e2c97`, itself unedited by this ratification); where a figure here matches
one there, it matches because it was measured again on this tree and came out
the same.

## 0. Scope, tree and provenance of the numbers

| item | value |
| --- | --- |
| clone | fresh `https://github.com/opensoft/openxFactory.git`, isolated from any shared checkout (`enc-947b`) |
| head the ratifying word was given on | `546e2c97` (content freeze) — carried forward unchanged through three merge-from-main commits |
| merges carrying `main` into the branch since the freeze | `9dfa36f3` (main `1fb6d5cd`, a sibling lane pass that died before its own FREEZE), `6d10daed` (main `22efcbe8`, a second lane pass that also died before its own FREEZE), `1229006a` (main `22a2ecbc`, this lane's own merge, done before the ratification encode) |
| tree these figures were taken on | the ratification encode, committed on `change/amend-merged-into-empty-tail-standing` on top of `1229006a`, carrying this file |
| `origin/main` at this verification | `78d2c6f5` (moved past `22a2ecbc` between this lane's merge and this capture; a further merge-and-re-measure is owed before landing if it is not folded in first — see the Addendum below if one was performed) |
| `--all --strict` (PATH 1.2.0) control | a separate worktree of `origin/main` `78d2c6f5` |
| `doc-health` control | the same `origin/main` `78d2c6f5` worktree, directory-basename-independent (findings compared by line content, not by repo label) |
| lane | `openxfactory-1` (display `openXfactory-1`) |
| environment | `OPENSPEC_TELEMETRY=0`, `openspec` on PATH **1.2.0**, pinned `openspec` **1.12.0** via `scripts/validate-openspec-cli-pin.py` (reused verified cache), Python **3.12.3** |

## 1. `OPENSPEC_TELEMETRY=0 openspec validate amend-merged-into-empty-tail-standing --strict`

```
Change 'amend-merged-into-empty-tail-standing' is valid
```

**Exit code 0.** The packet's own delta is strict-valid on the ratified tree.
The encode touches no file under the packet's own `specs/` directory — § 9
measures that as an EMPTY diff — so this is the same delta the bench reviewed,
validated again.

## 2. `openspec validate --all --strict`, both binaries

### 2a. The pinned CLI, `1.12.0`, via `scripts/validate-openspec-cli-pin.py --all` (reused verified cache)

```
Totals: 101 passed, 2 failed (103 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md  (accepted by Brett Heap, 2026-09-05, "take exit 2")
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content
address; every target validated --strict with 0 UNDISPOSITIONED failures.
```

**Exit code 0.** Both failing items are pre-existing, dispositioned exceptions
(§ 2 of `tasks.md`; neither is this packet), and the wrapper's own content-address
verification passed before a single validation ran.

### 2b. PATH `1.2.0`, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`

```
Totals: 100 passed, 3 failed (103 items)
```

**Exit code 1**, and **the failure SET is IDENTICAL to `origin/main` `78d2c6f5`'s**:

| failing item | on `origin/main` `78d2c6f5` | on the ratified tree |
| --- | --- | --- |
| `change/disposition-codexfactory-declared-renames` | ✗ | ✗ |
| `change/disposition-codexfactory-floor-relocation-retitle` | ✗ | ✗ |
| `spec/repo-boundary-governance` | ✗ | ✗ |

The `origin/main` control (separate worktree, `78d2c6f5`) reports `Totals: 98
passed, 3 failed (101 items)`. **The two totals are not directly item-for-item
because this lane's branch is not yet caught up to `78d2c6f5`**: `main` archived
`state-header-window-budget` (PR #953) after this lane's own merge at
`1229006a` (main `22a2ecbc`), which the branch does not yet carry, so the
branch still counts that change as ACTIVE (+1 item, `✓`) where `main` no longer
lists it at all; this packet itself is the other +1 (a `✓` `main` does not
carry yet either). **Both extra items PASS**, and the `✗` name-lists diff to
EMPTY. `spec/repo-boundary-governance`'s `requirements.1` failure under 1.2.0
is the corpus's known, already-disclosed condition (README's
`prepare-openspec-1-12-readiness` record; also carried by
`amend-repo-boundary-governance-scope-first-line`, active and unrelated to this
packet) until that packet's own archive lands. Neither remaining failure is a
`doc-health` item and this packet edits no file either reads.

## 3. `python3 scripts/proposal-support.py . verify amend-merged-into-empty-tail-standing`

```
proposal support verification ok
```

**Exit code 0.** The mechanical half of the origin-block rule: the gate's
origin-retention arm reads `kind`, `id`, `reason` and `proposed_by` as the
drafting lane declared them, and the encode adds `approved_by` and
`approved_on` BESIDE them without touching a byte of the four —
`git diff --numstat 546e2c97 -- .../.openspec.yaml` is **`41  0`**,
forty-one lines added and **zero removed** (§ 9).

`proposal-support`'s refuse-any-open-box rule applies **at archive**, not here;
`tasks.md` § 5 and § 6.1–§ 6.4 are open by design and this gate passes with
them open because the packet is not being archived by this commit.

## 4. `python3 scripts/validate-sequenced-after.py .`

```
sequenced_after validation passed (41 active changes, 11 declaring the field).
archive-date agreement passed (no archived row's moved_on predates its directory).
archive-date-vs-commit agreement passed (every archived directory is named for
the UTC date of the commit that added it, or is dispositioned in place; 12
disposition(s) in force, enforcement error).
```

**Exit code 0.**

### `--ledger-diff`

```
change ids (41 active + 159 archived): 200
co-modified at requirement granularity (each would owe a declaration): 147
sole modifiers (each would declare `sequenced_after: []`): 53
ACTIVE changes: co-modified / sole: 26 / 15
declaring `sequenced_after:`: 25 (… amend-merged-into-empty-tail-standing …)
declaring an explicit `[]` root claim: 7
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 4 hop(s), from
admit-review-lane-repin-to-merge-approval-envelope

per-change sweep ledger consistent with the corpus (200 rows).
```

**Exit code 0.** The ledger is consistent at **200 rows** and **ZERO rows moved
by the encode** — a sweep-ledger row's derived keys read neither a lifecycle
status nor a citation line, so a `draft`→`ratified` flip moves no row. This
change's own row (`state: active, class: co-modifier, moved_by: "#947"`) was
seeded by the sanctioned tool at `tasks.md` § 3.8 and is untouched here.

## 5. `python3 scripts/validate-scope-globs.py .`

```
scope_globs validation passed (all active changes conform).
```

**Exit code 0.**

## 6. `python3 scripts/doc-health.py --single-repo .`

```
Findings: 32 critical, 5 error, 47 warning, 15 info. New regressions vs previous report: 0.
```

**Exit code 0.** **NO FINDING NAMES THIS CHANGE** —
`grep -c 'amend-merged-into-empty-tail-standing'` over the full report returns
**0**.

### The control that matters: the finding-line diff against `origin/main`

`doc-health --single-repo` was run on a separate `origin/main` `78d2c6f5`
worktree and the two reports' severity-tagged finding lines (`- [severity]
...` and the `Ranked Plan` rows) were compared after normalizing the two
`Repo-Identity` labels to the same token:

```
--- branch (this ratification) vs origin/main 78d2c6f5 ---
severity/finding lines: IDENTICAL, byte for byte
headline: IDENTICAL — 32 critical, 5 error, 47 warning, 15 info on both sides
```

The only non-identical lines in the two RAW reports are the `Canon share by
words` percentage and the `(promoted specs)` word count (369563 vs 369817
words) — both explained by `main` `78d2c6f5` carrying `state-header-window-budget`'s
archive-time promotion (PR #953), which this branch has not yet merged past
`22a2ecbc`; neither figure is a finding, and neither line is scored by any
family this packet touches. **Flipping three documents from `Status: draft` to
`Status: ratified`, adding one citation to each, adding the approval pair and
adding two `review/` records adds ZERO findings and removes ZERO.**

### The `modified-block-currency` family — the family that reads this very block

`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`,
**exit code 0**: `Findings: 0 critical, 0 error, 0 warning, 9 info`, and this
change is named **0** times. The nine `info` rows are all OTHER active
changes' pre-existing carriage-ledger divergences (`add-chain-attestation`,
`add-composed-view-authoring`, `add-credential-escrow-checkout`,
`add-doxchat-model-intake`, `amend-mirror-floor-regeneration-merge-authority`,
`declare-client-standing-policy-contract`, `qualify-avatar-live-voice` ×3) —
identical in count and content to the `origin/main` control. **THIS BLOCK
SCORES ZERO MARKER DEFECTS**, matching § 2.2 and § 4.9's measurement rather
than re-deriving a different one.

### The `ratified-provenance` family — the family this encode is most exposed to

`python3 scripts/doc-health.py --single-repo . --family ratified-provenance`,
**exit code 0**: `Findings: 28 critical, 0 error, 0 warning, 0 info`, **and
NONE of them this change** (named 0 times). All 28 are pre-existing and belong
to other packets, identical in count to the `origin/main` control. This
packet's four status-bearing documents (`proposal.md`, `design.md`,
`tasks.md`, `review/ratification-2026-09-11.md`) each carry `Status: ratified`
and exactly ONE citation in a sanctioned spelling, which is what the family
counts; `review/verification-2026-09-11.md` (this file) keeps `Status:
record`, which the family's SUBJECT arm does not score.

## 7. `python3 -m pytest tests/doc-health -q`

```
1689 passed, 7 warnings in 403.61s (0:06:43)
```

**Exit code 0**, and **IDENTICAL** to the dead second author's own pre-encode
control run on this same branch content (`1689 passed, 7 warnings`, saved
read-only at
`…/06ef28ec-…/scratchpad/pre-pytest-doc-health.txt`). No test was added,
changed, skipped or xfailed by this ratification — `code_surface: none`, and
§ 9 shows the encode touches no file under `scripts/` or `tests/`.

## 8. What the encode does NOT move — verified by diff, not by assertion

Diffed against `546e2c97`, the frozen content the ratifying word was given on
(three merge commits sit between that head and this ratification — § 0 — none
of them touching this packet's own directory or the specific files its design
and residue name):

| surface | command | result |
| --- | --- | --- |
| the ratified delta | `git diff --name-only 546e2c97 -- openspec/changes/amend-merged-into-empty-tail-standing/specs/` | **EMPTY** |
| the promoted requirement this block writes over | `git diff --stat 546e2c97 -- openspec/specs/doc-health/spec.md` | **EMPTY** |
| the predicate and test this delta cites | `git diff --stat 546e2c97 -- scripts/doc_health/modified_block_currency.py tests/doc-health/test_modified_block_currency.py` | **EMPTY** |
| `openspec/specs/` at large | `git diff --stat 546e2c97 -- openspec/specs/` | **NOT empty** — one unrelated file, `lifecycle-notebook-projection/spec.md` (1/1), landed by an already-ratified packet's own promotion via the intervening `main` merges |
| `scripts/` and `tests/` at large | `git diff --stat 546e2c97 -- scripts/ tests/` | **NOT empty** — fifteen files, all unrelated corpus movement (openDox/openXdox pin verifiers, the corpus adapter, the sweep ledger's own row additions, one doc-health self-gate test's redaction-tracking comment) carried in by the three merges from `main`; none of it is the two files named above |
| `.openspec.yaml` | `git diff --numstat 546e2c97 -- .../.openspec.yaml` | **`41  0`** — forty-one lines ADDED, zero removed |

**NO NORMATIVE UNIT OF THE DELTA MOVED, AND THE ORIGIN BLOCK IS
BYTE-UNCHANGED.** The ratification's own diff against `546e2c97` touches
exactly six files:

```
README.md
openspec/changes/amend-merged-into-empty-tail-standing/.openspec.yaml
openspec/changes/amend-merged-into-empty-tail-standing/design.md
openspec/changes/amend-merged-into-empty-tail-standing/proposal.md
openspec/changes/amend-merged-into-empty-tail-standing/tasks.md
openspec/changes/amend-merged-into-empty-tail-standing/review/ratification-2026-09-11.md  (new)
```

plus this file, `review/verification-2026-09-11.md` (new). No archived change
is touched, no promoted specification is touched, no other active change's
files are touched (the three merges' unrelated files are `main`'s own,
untouched by anything this commit does), and the per-change sweep ledger is
not re-touched by the encode itself (only by the § 3.8 seed, already committed
before the ratification).

**ONE CORRECTION OF FACT WAS MADE IN THIS SAME COMMIT, DISCLOSED HERE AND AT
`review/ratification-2026-09-11.md` § 5.6**: `tasks.md` § 6.2 and `design.md`
D6 previously stated that `specs/019-modified-block-currency-family/spec.md`'s
FR-018 still carried the ONE-ground text and that openxFactory #915 remained
open. Neither was true on this tree: FR-018 (`:442`) already states FIVE
grounds (restated by `8a2ed38c`/`125a7d96`, `refs #915`, landed 2026-09-10,
before this packet's own authoring), and #915 is CLOSED (2026-09-11T01:29:59Z).
Both sentences are corrected in this commit. The correction is prose-only,
confined to this packet's own `tasks.md` and `design.md`, and touches no file
under `openspec/specs/`, `scripts/` or `tests/`.

## 9. Independent review

**FIVE THREADS ACROSS EIGHT COPILOT ROUNDS, ALL FIVE TAKEN OR REFUSED WITH
REASON, ZERO UNRESOLVED** — the full table is
`review/ratification-2026-09-11.md` §§ 5.1–5.2. **CODEX IS AN ABSENCE**: one
review request (2026-09-11T03:24:38Z) drew a usage-limit refusal
(2026-09-11T03:24:48Z), quoted verbatim at § 5.3 of the ratification record;
per the relaunch instructions in force, no second request was made.

**COPILOT'S TWO LATEST ROUNDS (`9dfa36f3` at 10:28:54Z and `6d10daed` at
10:51:52Z) BOTH RESTATE, WITHOUT OPENING A NEW THREAD, THAT THE PACKET STILL
READ AS UNRATIFIED** — the exact condition this commit resolves. Neither round
is disposed of as a reply-and-resolve (no thread was opened; all comments
SUPPRESSED, 0 new in both rounds), and both are recorded rather than silently
superseded, at `review/ratification-2026-09-11.md` § 5.5.

**A TARGETED SEARCH FOR TWO FURTHER FINDINGS DESCRIBED IN PRIOR GUIDANCE FOR
THIS ENCODE — a doc-health regression-test request at
`specs/doc-health/spec.md:637`, and a dispute of `tasks.md` § 6.2's FR-018
premise — FOUND NEITHER AS AN ACTUAL COMMENT ON THIS PULL REQUEST.** Every
review body and issue comment (`gh api repos/opensoft/openxFactory/pulls/947/reviews`,
`.../pulls/947/comments`, `.../issues/947/comments`) was searched for
`"FR-018"`, `"regression test"` and `"already states FIVE"`: zero matches at
any round from `82cd3d64` through `6d10daed`. The FR-018 premise was checked on
its own merits regardless (§ 8's correction, above); no regression-test finding
was located to dispose of, so none is recorded as TAKEN or REFUSED — there is
nothing to cite.

**THIS LANE ENCODES AND FREEZES; IT DOES NOT MERGE OR LAND.** The Rule 6
LANDING/LANDED post belongs to the landing lane, on Brett Heap's standing word
"land each when green."
