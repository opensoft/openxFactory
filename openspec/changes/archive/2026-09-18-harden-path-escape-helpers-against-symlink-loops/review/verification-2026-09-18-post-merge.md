# Verification record: harden-path-escape-helpers-against-symlink-loops, POST-MERGE run at the archive act of 2026-09-18

Status: record
Kind: report
Date: 2026-09-18
Ratified by: harden-path-escape-helpers-against-symlink-loops — 2026-09-18,
approximately 09:55Z, Brett Heap (openxFactory repository owner), verbatim
*"Ratify; land when green"* (record `review/ratification-2026-09-18.md`)

**THIS IS THE PACKET'S FIRST AND ONLY VERIFICATION CAPTURE, AND IT IS A
POST-MERGE ONE.** There is no earlier `review/verification-*.md` in this packet
to re-run: the proposal landed carrying `review/ratification-2026-09-18.md`
alone, and § 4's measurements were taken inside PR
[#1107](https://github.com/opensoft/openxFactory/pull/1107) and written into
`tasks.md` §§ 4.1–4.3 rather than into a separate record. So this file claims no
`Rerun of:` and supersedes nothing. What it records is the state of the world
at the ARCHIVE act — both merges landed, `main` green over a tree carrying them
— together with the byte-for-byte proof that the promotion moved the ratified
text and not a paraphrase of it.

**IT IS A `record` AND NOT A `draft`.** `document-lifecycle` holds that a dated
one-shot capture — a run report, a byte-exact evidence snapshot — carries
`Status: record`, and that a second run of such a generator writes a different
path rather than rewriting this one.

| item | value |
| --- | --- |
| act this capture belongs to | the ARCHIVE of `harden-path-escape-helpers-against-symlink-loops` |
| branch | `change/archive-harden-path-escape-helpers-against-symlink-loops`, cut from `origin/main` at **`e3647b6d`** in a FRESH clone |
| lane | `openxfactory-5` (display `openXfactory-5`) |
| environment | `TZ=UTC`, `OPENSPEC_TELEMETRY=0`, Python **3.12.3**, wrapper-resolved `openspec` **1.12.0** (content-addressed pin; `PATH` carries 1.13.1 and was NOT used for the archive) |
| the word this act still owes | **Brett Heap's SEPARATE ARCHIVE WORD, NOT GIVEN.** The pull request carrying this record is opened as a DRAFT and lands only on that word, by MERGE COMMIT |

## 1. The evidence the archive stands on

`code_surface: openxFactory` is NON-EMPTY, so under `release-realization` this
packet archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE and on a separate
word, never on landing and never on ratification. Both evidence halves are in
hand and each is cited rather than asserted.

| half | value | how it was checked |
| --- | --- | --- |
| Packet landing | PR [#1083](https://github.com/opensoft/openxFactory/pull/1083) -> merge **`ebcdbc0c20eb7368582d4bb8103001ab48316542`** on `main`, **2026-09-18T14:03:33Z** | `gh pr view 1083 --json mergeCommit,mergedAt` |
| Realization merge | PR [#1107](https://github.com/opensoft/openxFactory/pull/1107) -> merge **`c22c4fc355898d4e57eb1159f47d756b30875b66`** on `main`, **2026-09-18T17:06:27Z**, from head **`bc9ebf954f9629de25c6bb61cd5485937bdaaa54`** | `gh pr view 1107 --json mergeCommit,mergedAt,headRefOid` |
| Green at the realization head | `pytest-suite` run [`35362604810`](https://github.com/opensoft/openxFactory/actions/runs/35362604810) at `bc9ebf95`, conclusion **`success`**; the whole check set at that head is **15 SUCCESS, 1 SKIPPED** (`Sourcery review`), **0 failures**, across 14 distinct names | `gh run view 35362604810 --json conclusion,headSha`; `gh api .../commits/bc9ebf95.../check-runs --paginate` |
| **Green on `main`** | `pytest-suite` run [`35372664200`](https://github.com/opensoft/openxFactory/actions/runs/35372664200) at **`049d54a9e4d51fe2e1c0a8c97c1e22c5d2f3e694`**, conclusion **`success`**, **2026-09-18T17:09:27Z** | `gh run view 35372664200 --json conclusion,headSha,createdAt` |
| `main`'s green tree CONTAINS the realization merge | **YES** | `gh api repos/opensoft/openxFactory/compare/c22c4fc3...049d54a9 --jq .status` -> **`ahead`**; `git merge-base --is-ancestor c22c4fc3 049d54a9` -> exit **0** |

**THE THREE COMMITS ARE ONE ANCESTRY CHAIN, MEASURED LEG BY LEG.**
`ebcdbc0c` (#1083) -> `c22c4fc3` (#1107) -> `049d54a9` (the tree `main`'s green
run decided), each leg checked with `git merge-base --is-ancestor` and each
exiting 0. This branch's base `e3647b6d` is 22 commits beyond `049d54a9` and
contains all three.

**THE `tasks.md` § 4.4 NOTE NAMED A HEAD THAT WAS NOT THE MERGE HEAD, AND THAT
IS CORRECTED AT THE TICK RATHER THAN LEFT.** The note was written when #1107's
head was `8fb0fc99` (run `35359208240`, green). One commit followed — `bc9ebf95`,
the note's own commit — and that is the head the merge was taken from. Both
heads have a green `pytest-suite`, so no claim changes; the correction is to the
sha, not to the conclusion.

## 2. The promotion, compared and not eyeballed

Performed through the GOVERNED WRAPPER and never a bare `openspec archive`
(`tasks.md` § 5.2 forbids the bare invocation):

```
TZ=UTC python3 scripts/proposal-support.py . archive \
    harden-path-escape-helpers-against-symlink-loops --yes
```

Exit **0**. Its decisive lines, verbatim:

```
ORIGIN RETAINED harden-path-escape-helpers-against-symlink-loops (declaration unchanged since the ratifying commit ebcdbc0c20eb)
proposal-support: @fission-ai/openspec@1.12.0 from the pinned artifact (…); integrity sha512-oFE2Lj7WVSc87nSi… verified, over the pinned dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages, lockfile_integrity sha512-aw5lIN45tQq2WZll…, installed with `npm ci --ignore-scripts`)
Totals: 1 passed, 0 failed (1 items)
Task status: ✓ Complete
Specs to update:
  release-realization: update
Applying changes to openspec/specs/release-realization/spec.md:
  + 2 added
Totals: + 2, ~ 0, - 0, → 0
Specs updated successfully.
Change 'harden-path-escape-helpers-against-symlink-loops' archived as '2026-09-18-harden-path-escape-helpers-against-symlink-loops'.
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
NO SUPPORTING DOCS …/openspec/changes/harden-path-escape-helpers-against-symlink-loops (origin retained, nothing to package)
```

**ORIGIN RETAINED is the wrapper's own gate**, and it names `ebcdbc0c20eb` —
the packet's landing merge, which is the commit that carries the ratified
`.openspec.yaml` onto `main`. No origin disposition was needed and none was
written.

**`--date` WAS NOT PASSED**, so the wrapper took TODAY IN UTC, **2026-09-18**,
which is also the UTC day of the commit that adds the archive directory. That
identity is what `archive-date-vs-commit` measures, and it holds by construction
rather than by a hand-chosen date.

### 2.1 The two `## ADDED` requirements, ten scenarios, byte for byte

Both requirement blocks were extracted PROGRAMMATICALLY by heading from the
archived delta and from canon — never read side by side — and compared:

| requirement | scenarios | bytes | lines | sha256 (delta) | sha256 (canon) | `diff` |
| --- | --- | --- | --- | --- | --- | --- |
| *A containment guard answers every resolution failure and raises none* | **6** | **6,049** | 82 | `e12a9d9d54f64ac0c97d9c808f03df64583943f2d75760f0d3cb723ff33ffc7a` | **identical** | exit **0**, zero lines |
| *A symlink-loop proof is built at test time and never committed* | **4** | **3,198** | 46 | `f98402134c0b7eb855d30c57792f8219ea4f17a5e1ade176df0381194b19d625` | **identical** | exit **0**, zero lines |

**TEN SCENARIOS IN TOTAL, WHICH IS THE COUNT THE PROPOSAL, THE RATIFICATION
RECORD AND THE README ENTRY ALL CARRY**, and the count was re-taken from the
promoted text (`grep -c '^#### Scenario:'` on each extracted block: 6 and 4)
rather than copied forward.

**NO PROMOTED BYTE IS EDITED OR REMOVED.** `openspec/specs/release-realization/spec.md`
reads `--numstat` **+130 -0**, and `--numstat -w` reads the SAME `130 0`, so not
one changed line is whitespace-only. The delta carries no `## MODIFIED` block,
so no `Removed from canon by`, `Modified over` or `Merged into` marker is owed
and no modified-block-currency row is opened. The capability's requirement count
moves **17 -> 19**; every pre-existing requirement in that file is untouched.

### 2.2 The packet's own files moved and were not edited

Six files, all `R100` pure renames at **0 changed lines** — `.openspec.yaml`,
`design.md`, `proposal.md`, `specs/release-realization/spec.md`,
`review/ratification-2026-09-18.md` and this record — except `tasks.md`, whose
only change is § 4.4's and § 5's ticks, written in the commit BEFORE the move
because `scripts/proposal-support.py`'s `archive_change()` refuses any literal
`- [ ]` line in `tasks.md` and there is no bypass flag. The ratification record
is moved and NOT edited.

**THE THREE `- [~]` BOXES OF § 6 STAY `- [~]`.** They document successors and
refused-not-owed work, not incomplete work; § 6.1's own text says so, and the
wrapper's refusal keys on `- [ ]` and not on `- [~]`, which is why the marker
exists.

## 3. What this record does NOT claim

- **It does not claim Brett Heap's archive word.** That word has not been given.
  This capture exists so that when it comes, the act is a merge and not a
  night's authoring.
- **It does not claim that #1074 is shut.** `Closes #1074` is written in the
  archive pull request's body and nowhere else; the issue shuts on that pull
  request's MERGE, which is the landing lane's act.
- **It does not re-open § 4.1–§ 4.3.** Those measurements were taken at
  `87eb684d`, PR #1107's intermediate merge of `origin/main` on that branch
  and NOT the realization head — the realization head was `bc9ebf95`, merged
  as `c22c4fc3` — and are recorded in `tasks.md`; they are cited here, not
  re-performed.
- **It moves no code.** `scripts/` and `tests/` are untouched by the archive but
  for the one machine-seeded sweep-ledger row, which changes no code byte.

## 4. Provenance

Written by lane `openxfactory-5` (display `openXfactory-5`) in the tick commit
of the archive pull request, in a fresh clone of `opensoft/openxFactory` at
`e3647b6d`, never in the shared checkout and never in a sibling lane's tree.
Every path in this file is repo-relative. The full gate transcripts at the
pushed head — `openspec validate
--all --strict`, `validate-sequenced-after.py` plain and `--ledger-diff`,
`validate-code-surface.py`, the four test packages and `doc-health.py`, each
diffed against this same clone at `origin/main` — are carried in that pull
request's body.
