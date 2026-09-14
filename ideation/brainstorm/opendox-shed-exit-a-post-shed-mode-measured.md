# The § 5.2 shed's blocking prerequisite — exit (a) MEASURED, with (b) and (c) costed — Brainstorm

Status: brainstorm
Kind: report
Summary: Measures the § 5.2 shed prerequisite of
`split-opendox-two-layer-product` (issue #656) in a throwaway clone at `main`
`52e42be9`: exit (a) POST-SHED MODE works — one optional `phase: post-shed`
manifest key with no CLI flag and no `shed_commit`, the validator answers `OK`
over the full 319-row shed tree with both carve suites green (`209 passed`),
zero rows change disposition, digests frozen at `b075fd91`/`opendox-carve-0`,
and a 482-line-added/17-removed diff across 4 files; the shed also exposes an
unbudgeted adapter re-point — 104 import sites across 32 files naming 32 shed
modules, 17 with no reachable home in openxFactory's CI, a retained
`tests/ideation-dashboard/conftest.py:106` import that aborts collection, and
a six-schema `contracts/schemas/` family still named by 127 tracked files;
exits (b) RE-CUT and (c) RETIREMENT are costed against the same tree; and
eight open questions go to Brett Heap.
Topics: opendox, openxdox, split-opendox-two-layer-product,
opendox-carve-manifest, carve-manifest-shed, post-shed-mode, carve-validator,
adapter-re-point, measurement
Repository context: openxFactory — measures `scripts/validate-carve-manifest.py`,
`scripts/verify-carve-arrival.py`, and `docs/opendox-carve-manifest.yaml`, all
owned here; governing record is issue #656 and the ratified, active
`split-opendox-two-layer-product` OpenSpec change (its `tasks.md` § 5.2 and
`docs/opendox-cutover-runbook.md`).
Captured: 2026-09-10
Participants: a measurement agent, in a throwaway clone
Purpose: put measured numbers under Brett Heap's choice among exits (a), (b)
and (c) for the § 5.2 shed prerequisite, rather than three descriptions.

## Provenance

The addendum on `opensoft/openxFactory` issue #656 comment
[5625144570](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5625144570)
(2026-09-10T20:40:44Z) named this note filable "into the packet on request";
this pull request is that filing. It answers the ruling request opened the
same day in comment
[5624521801](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5624521801)
(2026-09-10T19:48:51Z). Measured in a throwaway clone; the spike branches were
never pushed.

**The measured spike implementation itself is not pushed, committed to any
remote, or proposed as landed** — only this design note describing it is,
which is this pull request's own act of filing it. Verified at the end of
the measurement run: the only clone with a GitHub `origin` carried `main` at
`origin/main` and no other branch; the spike branches existed only in clones
whose `origin` was a local path; the lane's long-lived shared checkout was
byte-for-byte as that session found it. **It decides nothing** — the choice
among exits (a), (b) and (c) is Brett Heap's, and this note exists only so
that the ruling has measured numbers under it rather than three
descriptions.

**Every figure below was produced by a command in a disposable clone of
`opensoft/openxFactory` at `main` = `52e42be98c9e5bb4a5b1fc5cf89e235d5a349c5b`.**
Where a number differs from an earlier record's, the command output is the
finding. Spike branch (local only, never pushed):
`spike/exit-a` → `05ef9236` (validator + tests) → `88caf62e` (the shed +
the declaration, one commit) → `b27f0555` (runbook + manifest header).

---

## 1. The refusal as measured

### 1.1 The six checks, and which two refuse a post-shed tree

`scripts/validate-carve-manifest.py` runs six ordered checks, first failure
wins (`validate()`, lines ~1540). Ran individually against a tree with the
319 manifest-derived shed paths deleted (`ceee7db9b365`, a throwaway commit
off `main`):

| # | check | what tree/revision it walks | over the shed tree |
| --- | --- | --- | --- |
| 1 | SHAPE (`check_shape`) | **the document only** — no git call | **PASS** |
| 2 | REVISION (`check_revision`) | `carve_commit` must be a commit object the repository CARRIES and an ANCESTOR of the revision under test | **PASS** — the shed deletes files from a tree, not a commit from a history |
| 3 | DIGEST (`check_digests`) | PASS 1 at `carve_commit`; PASS 2 at the revision under test | **REFUSE `carve-path-absent`** — pass 2, `if path not in tested`, for each of the 318 MOVED rows |
| 4 | SURFACE (`check_surface`) | `git ls-tree -r` under every `moved_paths:` prefix at BOTH revisions | **REFUSE `carve-path-absent`** — the `vanished` arm, `surface - tested_surface`, 319 rows |
| 5 | VOCABULARIES (`check_vocabularies`) | the document only | **PASS** |
| 6 | DISPOSITION CONSISTENCY | the document only | **PASS** |

**Exactly two arms refuse, both `carve-path-absent`, both about absence at the
revision under test.** Check 3's is the one a real run reaches, because check 3
runs before check 4.

Three arms that a reader might expect to fire do **not**, and each is
load-bearing for exit (a):

* `check_surface`'s `moved_paths:` vacuity check is **keyed on the referent**
  ("`moved_paths:` is a claim about the tree the digests were taken at"), so
  the 9 prefixes the shed empties do not refuse `carve-surface-vacuous`.
* `check_surface`'s `appeared` arm (`tested_surface - surface`) is unchanged
  by a deletion.
* Check 3 PASS 1 — the 318 digest recomputes and the 794 declared-line bounds
  at `carve_commit` — is untouched: `git cat-file blob b075fd91:<path>`
  answers after the shed exactly as before.

### 1.2 Verbatim

Unmodified validator, shed tree:

```
$ python3 scripts/validate-carve-manifest.py
FAIL …/docs/opendox-carve-manifest.yaml: carve-path-absent — contracts/schemas/gate-action-record.schema.yaml: DELETED SINCE THE CARVE — rows[0] declares it `moved_verbatim` at b075fd91dc8f, and ceee7db9b365 no longer carries it as a file. The carve ships the bytes at the carve commit, so a source the tree has since dropped is a move nobody can review at the destination: re-cut the manifest at a new carve commit
Remediation: re-cut the manifest AT the carve commit — recompute every sha256 from the real bytes (`git cat-file blob <carve_commit>:<path> | sha256sum`), never edit a digest to make this pass — or, where the tree has moved since, name a NEW carve_commit and recompute the whole file: the § 6 ceremony re-cuts, it never carries digests forward. Verify at a specific revision with `--at <sha>`.
exit=2
```

Check 4's arm, reached by calling the checks directly:

```
check 4 surface: REFUSE carve-path-absent | 319 row(s) name path(s) DELETED SINCE THE CARVE — under the surface at b075fd91dc8f, absent at ceee7db9b365: contracts/schemas/gate-action-record.schema.yaml, … [10 named, then " …"]
```

The § 8.2 seat, unmodified, over the shed tree:

```
$ python3 -m pytest tests/carve_manifest tests/carve_arrival -q
FAILED tests/carve_manifest/test_carve_manifest.py::test_the_real_repository_answers_at_the_ruled_path
1 failed, 197 passed in 55.29s
```

**This reproduces PR #924's probe 2 exactly** (`1 failed, 197 passed`, same
rows[0], same wording), at a later `main`.

### 1.3 The remediation text the validator prints

`REMEDIATION`, the fixed trailer on every refusal
(`scripts/validate-carve-manifest.py`, the `REMEDIATION` constant):

> Remediation: re-cut the manifest AT the carve commit — recompute every sha256
> from the real bytes (`git cat-file blob <carve_commit>:<path> | sha256sum`),
> never edit a digest to make this pass — or, where the tree has moved since,
> name a NEW carve_commit and recompute the whole file: the § 6 ceremony
> re-cuts, it never carries digests forward. Verify at a specific revision with
> `--at <sha>`.

Check 3 pass 2's own detail adds *"re-cut the manifest at a new carve commit"*;
check 4's `vanished` arm adds *"Check 3 reports this for a MOVED row, with its
digest; this is what reports it for a `not_moved` row, which the digest loop
never reads at all."* **Both name only the re-cut, which is exit (b).**

### 1.4 The shed set, derived rather than listed

456 rows: 172 `moved_verbatim` + 146 `moved_with_declared_edit` + 138
`not_moved` (103 `stays_openxfactory_adapter`, 20
`replicated_at_destination`, 14 `stays_openxfactory_governance`,
1 `deleted_at_carve` = `scripts/ideation_dashboard/profile_openxfactory.py`).
**Shed = 318 moved + 1 `deleted_at_carve` = 319**; 137 rows stay.
By top-level directory: `tests` 119, `scripts` 97, `examples` 96,
`contracts` 6, `docs` 1. `def test_` inside the 319 shed paths: **3,404**
(runbook § 8 says 3,426 — a 22-test drift, unresolved here).

---

## 2. Exit (a) design

### 2.1 The declaration is IN the manifest, and it is symmetric

```yaml
schema_version: 1
kind: opendox-carve-manifest

phase: post-shed        # OPTIONAL; absent == `carve`
```

**One optional top-level key, closed to two values** (`carve`, `post-shed`),
validated by check 1 as `carve-shape-invalid` — check 1 owns document-level
consts (`digest_algorithm` and friends); check 5 owns the closed vocabularies
of a ROW, so a mistyped phase must not reach check 3 and refuse there under a
code naming a file.

**In the manifest, not on a command line**, for three measured reasons:

1. A `--phase` flag would mean the same tree verifies or refuses depending on
   which job invoked the tool. The § 8.2 seat runs the tool with **no
   arguments** (`subprocess.run([sys.executable, str(SCRIPT)], cwd=REPO_ROOT)`),
   so a flag could never reach the required-suite seat at all.
2. The declaration and the deletions then land in one reviewable diff, which is
   runbook § 8's *"no ordering of two commits leaves a green intermediate"*.
3. `verify-carve-arrival.py` reads the same document and deliberately does not
   close its top-level key set (*"This file does not re-own the manifest's
   shape"*), so the key costs it **zero lines** — measured, below.

**No `shed_commit:`.** It is unknowable at authoring time (the shed commit
contains the manifest edit that would have to name it), and it buys nothing the
symmetry does not already buy.

**The declaration is symmetric, which is what makes it a floor and not a mute.**
Under `post-shed` a moved row's source path that is STILL PRESENT refuses a new
code, `carve-shed-incomplete`. So the phase cannot be flipped ahead of the
deletions to buy silence for 319 rows at once, and the deletions cannot land
ahead of the phase without refusing.

### 2.2 What changes semantics, and what does not

| row class | rows | `carve` (today) | `post-shed` |
| --- | ---: | --- | --- |
| `moved_verbatim` + `moved_with_declared_edit` | 318 | present at source, blob+mode == the referent's | **absent EXPECTED**; present → `carve-shed-incomplete` |
| `not_moved / deleted_at_carve` | 1 | present at source | **absent EXPECTED**; present → `carve-shed-incomplete` (check 4, because the digest loop never reads a `not_moved` row) |
| `not_moved / stays_openxfactory_adapter` | 103 | present at source REQUIRED | **unchanged** |
| `not_moved / stays_openxfactory_governance` | 14 | present at source REQUIRED | **unchanged** |
| `not_moved / replicated_at_destination` | 20 | present at source REQUIRED (the retained copy) | **unchanged** |

Unchanged in both phases, and this is most of the floor:

* **Check 2 (ANCESTOR) is untouched.** `carve_commit` must still be a commit
  object this repository carries and an ancestor of the revision under test.
  Ancestry survives the shed by construction.
* **Check 3 PASS 1 is untouched** — all **318 digests recomputed** from the
  referent's real bytes on every run, and all **794 declared lines** still
  bounded by the carve blob's line count.
* **Check 4's referent walk is untouched** — all **456 files** under the
  surface at `b075fd91` still in exactly one row, no duplicate arrivals.
* **Check 4's `appeared` arm is untouched** — a file that appears under the
  carve surface still refuses `carve-file-undeclared`.
* **Checks 1, 5 and 6 never read the tree.**
* **The digests stay frozen at `b075fd91` and the label stays
  `opendox-carve-0`.** No row changes disposition, no `sha256` moves, no tag
  is cut.

### 2.3 What exit (a) gives up, stated plainly

For the **318 moved rows only**, it stops asking *"has this file drifted on
`main` since the carve"* — the scout memo's § 6 step 3 pressure. That question
cannot be asked of a deleted file by any mechanism, under any exit. The answer
it was buying is discharged once and elsewhere: at the four destinations, by
`verify-carve-arrival.py`, against blobs read at `carve_commit` from this
repository's own history. **The 137 rows that stay keep every guarantee they
had.**

### 2.4 Arrival — measured, not designed

The brief asked whether post-shed mode should REQUIRE moved rows present at
destination via the arrival digests. **It cannot, and it does not need to.**

* `verify-carve-arrival.py` needs a destination CHECKOUT (`--dest-root`).
  openxFactory mounts no destination: `opensoft/openXdox`'s `.gitmodules`
  nests only `code` → `openXdox-code` `59600412` and `spec` → `openXdox-spec`
  `03eacc61`, and its `contracts/opendox-pin.yaml` is
  `materialization: referenced`. So the validator cannot see openDox at all.
* The shed does not disturb the arrival half. Run from the **post-shed** tree
  against the four leg clones and from the **pre-shed** tree, the summary lines
  are **byte-identical** for the three legs that need no `--replica-at`:

```
IDENTICAL  openxdox_spec
IDENTICAL  opendox_spec
IDENTICAL  opendox_code
```

```
$ python3 scripts/verify-carve-arrival.py --destination opendox_code \
      --dest-root …/openDox-code --source-repo . --phase B     # post-shed tree
OK …: opendox_code (opensoft/openDox-code) at opensoft/openxFactory@b075fd91dc8f (opendox-carve-0), phase B — 123 row(s) arrived, 61 digest(s) verified, 61 declared-edit row(s) within their lines, 1 unapplied; 0 of 0 declared replica(s) verified …; 132 file(s) under src/opendox, tests with none undeclared (1 scaffold, 8 replica, 0 created)
$ … --destination openxdox_spec …
OK …: phase B — 47 row(s) arrived, 47 digest(s) verified, 0 declared-edit row(s) within their lines, 0 unapplied; … 47 file(s) under contracts/schemas, examples/ideation-dashboard with none undeclared
$ … --destination opendox_spec …
OK …: phase B — 56 row(s) arrived, 55 digest(s) verified, 1 declared-edit row(s) within their lines, 0 unapplied; … 57 file(s) under contracts/schemas, docs, examples/ideation-dashboard with none undeclared
$ … --destination openxdox_code …
FAIL …: arrival-undeclared-file — tests/conftest.py sits under a declared root and no row places it …
```

`openxdox_code` needs its recorded `--replica-at`/`--allow-created` flags, in
both phases identically — a command-line matter, not a shed matter.

**So arrival stays where it is: `verify-carve-arrival.py`, run per destination
by hand at the shed PR, its output quoted as evidence.** Recording the four
arrival commits IN the manifest would be bookkeeping the validator could check
for well-formedness only, not proof; it is not proposed here.

### 2.5 What FLOOR PART 1's required-suite seat asserts in each phase

`tests/carve_manifest/test_carve_manifest.py::test_the_real_repository_answers_at_the_ruled_path`
— the § 8.2 seat, a BRANCH and never a skip. Under exit (a) it gains a
phase clause:

* **manifest absent** → `NO MANIFEST … (nothing to validate)`, exit 0
  (unchanged, the seat-holding pass).
* **manifest present** → exit 0, `OK …`, **and the phase the run REPORTS must
  equal the phase the file DECLARES**, read out of the YAML. This is what makes
  the seat non-vacuous in both phases: a phase-blind run, or a run that
  silently fell back to the default, fails here.
* **`phase: carve`** → the `OK` line must NOT carry a shed count.
* **`phase: post-shed`** → the `OK` line must carry
  `"shed row(s) absent at source as declared"`. That sentence is only printed
  after check 3's post-shed arm has proved every one of those rows ABSENT, so
  the number is a claim about the tree, not a row count copied out of the
  document.

The `OK` line now names the phase on **every** run, in both phases — a reader
of a CI log must be able to tell which semantics answered without opening the
manifest, and a line that said nothing under the default would make the default
the one state no log records.

### 2.6 Refusal vocabulary

`REFUSAL_CODES` gains exactly one member, `carve-shed-incomplete`, inserted
before `carve-unreadable`. The tuple is described in the source as *"FIXED,
COMPLETE and ordered by the check that raises it"* and
`tests/carve_manifest/test_carve_manifest.py`'s `RATIFIED_CODES` restates it as
a literal, so **adding a code is a deliberate, test-visible act and is flagged
as such** (open question Q4). `REMEDIATION` gains one sentence naming the
opposite remedy for the new code, because the standing trailer's advice
("re-cut the manifest") is wrong for it.

---

## 3. Spike results, verbatim

Environment: a disposable clone at `main` `52e42be9`; Python 3.12.3; venv built
from the repository's own documented lock
(`pip install --require-hashes -r requirements/hermes-runtime-contracts.lock`);
node v22.22.2 and the `openspec` CLI on PATH.

### 3.1 The validator, over the shed tree, under exit (a)

```
$ python3 scripts/validate-carve-manifest.py
OK docs/opendox-carve-manifest.yaml: phase post-shed, 456 row(s) at opensoft/openxFactory@b075fd91dc8f (opendox-carve-0), verified at b27f05558ef7 — 172 moved_verbatim, 146 moved_with_declared_edit, 138 not_moved; 318 digest(s) recomputed; 456 file(s) in the declared surface with none undeclared; 319 shed row(s) absent at source as declared
exit=0
```

```
$ python3 scripts/validate-carve-manifest.py --json
{"result": "ok", "manifest": "…/docs/opendox-carve-manifest.yaml", "phase": "post-shed", "shed_rows": 319, "carve_commit": "b075fd91dc8fced8e1373825ba80220c33536bae", "verified_at": "88caf62ecfe4fb16e78024a2dd99300a6f79a93f", "carve_tag": "opendox-carve-0", "source_repository": "opensoft/openxFactory", "rows": 456, "dispositions": {"moved_verbatim": 172, "moved_with_declared_edit": 146, "not_moved": 138}, "digests_recomputed": 318, "surface": 456}
```

> **Editor's note (filing, 2026-09-10):** The plain-text run's "verified at
> `b27f05558ef7`" and the `--json` run's `"verified_at":
> "88caf62ecfe4fb16e78024a2dd99300a6f79a93f"` name two different commits on
> the same `spike/exit-a` chain, not one disputed tree:
> `88caf62ecfe4fb16e78024a2dd99300a6f79a93f` is the shed + `phase: post-shed`
> declaration commit, and `b27f05558ef773e2aea2ee29bd095d721a0aecce` is the
> later, docs-only commit (runbook + manifest-header prose; see Provenance).
> `git show --stat` on both, in the spike's throwaway clone, confirms
> `b27f0555` touches only `docs/opendox-carve-manifest.yaml` and
> `docs/opendox-cutover-runbook.md` — not the shed set, the carve commit, or
> any disposition — so the JSON block's row counts, dispositions and digest
> count hold at either commit. `verified_at` should read
> `b27f05558ef773e2aea2ee29bd095d721a0aecce` to match the plain-text run
> captured in the same block; the field is left as measured here rather than
> silently corrected, per the "leaving this thread open for that follow-up"
> reply already on this pull request's review thread. Raised by a Copilot
> review comment on pull request #929.

**One cost, measured and not designed around.** The ceremony's own documented
invocation stops answering once the phase flips:

```
$ python3 scripts/validate-carve-manifest.py --at b075fd91dc8fced8e1373825ba80220c33536bae
FAIL …: carve-shed-incomplete — contracts/schemas/gate-action-record.schema.yaml: STILL PRESENT UNDER A POST-SHED MANIFEST — rows[0] declares it `moved_verbatim` at b075fd91dc8f, the manifest declares `phase: post-shed`, and b075fd91dc8f still carries it as a file. …
```

At the carve commit every source path IS present, which a post-shed manifest
refuses. That line is in the manifest's own header block and in runbook § 0.4;
the spike corrects both (open question Q3).

### 3.2 The carve suites

```
$ python3 -m pytest tests/carve_manifest tests/carve_arrival -q      # exit-(a) tree, POST-SHED
209 passed in 62.38s
```

Baseline for comparison: `198 passed` on `main`; `1 failed, 197 passed` on the
shed tree with the unmodified validator. The 11 added tests are the post-shed
cases (§ 3.5). **`tests/carve_arrival` is unchanged at 91 tests and 0 failures
in every run.**

### 3.3 The arrival verifier

See § 2.4. Three legs byte-identical pre- and post-shed; the fourth needs its
recorded flags in both phases identically. **`scripts/verify-carve-arrival.py`,
`scripts/carve_lines.py` and `tests/carve_arrival/` change by ZERO lines**
(`git diff --numstat main HEAD -- …` returns no rows for any of them).

### 3.4 The full suite

`pytest-suite.yml`'s exact invocation is
`python3 -m pytest tests/ -q -m "not postgres" --junitxml=pytest-report.xml`,
with `MIN_SELECTED: "7090"`, `MIN_PASSED: "7070"` (floors, may only rise) and
`EXPECT_SKIPPED: "21"` (pinned EXACTLY, as a SUM).

**That exact invocation over the exit-(a) tree ABORTS AT COLLECTION and runs
nothing:**

```
$ python3 -m pytest tests/ -q -m "not postgres" -p no:cacheprovider --junitxml=…
ERROR tests/corpus-adapter/test_openxfactory_adapter.py
ERROR tests/ideation-dashboard - ModuleNotFoundError: No module named 'sessio...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
2 skipped, 338 deselected, 2 warnings, 2 errors in 7.01s
exit code = 2
```

**This is not a floor problem, it is an abort.** No JUnit triple is produced,
so `MIN_SELECTED`/`MIN_PASSED`/`EXPECT_SKIPPED` are never evaluated; the job
fails at the pytest step.

With `--continue-on-collection-errors` added so the rest runs
(**this host, NOT CI's runner** — no `PINNED_CORE_CHECKOUT`, no `openXwallet`
gitlink, no `pytest-subtests`, and the clone is not named `openxFactory`, so
the absolute numbers are not CI's and only the DELTA is meaningful):

```
baseline  (main 52e42be9)  selected=11119 passed=10863 skipped=110 failures=96 errors=50   (39m37s)
exit-(a)  (post-shed)      selected=5725  passed=5466  skipped=83  failures=114 errors=62  (19m19s)
```

Diffing the two JUnit reports by test id: **31 NEW failures/errors, 1 gone**
(a baseline failure whose own test the shed removed).

**Of the 31, three are an artefact of my clone-of-a-clone and not the shed** —
`tests/doc-health/test_pin_reachability` ×3, whose `origin` is a local path
advertising 0 `refs/retention/*` where GitHub advertises 4. **28 are genuinely
shed-caused**, and they fall into three families:

| family | count | cause |
| --- | ---: | --- |
| **A — adapter imports** | 6 | 2 collection errors (`tests/ideation-dashboard` whole directory; `tests/corpus-adapter/test_openxfactory_adapter.py`) + 4 failures reaching a shed module through a RETAINED one |
| **B — the six shed `contracts/schemas/` files** | 20 | 14 × `tests/hermes_runtime_contracts/test_validator_cli.py`, 4 × `tests/doc-health/test_ideation_readiness.py` + `test_readiness_dispatch.py`, `tests/intent-compliance/test_release_boundary.py`, `tests/manifest_digests/test_manifest_digest_sweep.py` |
| **C — doc-health corpus** | 2 | `tests/doc-health/test_sentinel_vocabulary.py` ×2 (`composed: no scripts/ideation_dashboard/snapshot_registry.py`) |

**Family B is not named anywhere in runbook § 8, in tasks.md § 5.2, or in
PR #924's record, and it belongs to the shed itself under EVERY exit.** Six
schemas are `moved_*` rows — `gate-action-record`,
`ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`,
`ideation-workbench`, `xfactory-workbench-chat-turn`,
`xfactory-workbench-model-catalog` — and **127 tracked files name them**: 35
frozen `contracts/releases/contract-v*.digests.yaml` inventories, 34 immutable
`openspec/changes/archive/` records, and ~58 live files including
`contracts/manifest.yaml`, `contracts/hermes-runtime/contract-index.yaml`,
`contracts/CHANGELOG.md`, `contracts/README.md`, three
`contracts/domain-ontology/core/**/concepts.yaml`, and 26 live
`ideation/dashboard/gate-records/**` records. Sample refusal:

```
tests.manifest_digests.test_manifest_digest_sweep::test_the_real_manifest_verifies_run_the_documented_way
  FAIL contracts/schemas/ideation-dashboard-snapshot.schema.yaml: recorded in the manifest but missing on disk
tests.intent-compliance.test_release_boundary::…
  ContentResolutionError: release member is not a regular file: contracts/schemas/gate-action-record.schema.yaml
```

**Zero of the 31 is caused by the validator change.** Both carve suites are
green inside the full run in both trees (baseline 198/0 failing; exit-(a)
209/0 failing).

### 3.5 The 11 added tests

All subprocess-driven against real throwaway git trees, on the file's own
discipline. The shed set inside each is derived from the fixture document's own
rows, never listed by hand.

```
test_the_shed_refuses_under_the_default_phase
test_a_post_shed_manifest_verifies_over_a_shed_tree
test_a_post_shed_manifest_over_an_unshed_tree_refuses
test_a_post_shed_deleted_at_carve_row_still_present_refuses
test_a_row_that_stays_may_not_be_deleted_by_the_shed
test_a_file_appearing_under_the_surface_still_refuses_post_shed
test_the_carve_commits_own_line_still_verifies_post_shed
test_an_unknown_phase_refuses
test_an_absent_phase_is_the_carve_phase
test_json_reports_the_post_shed_phase
test_the_phase_is_the_manifests_and_not_a_command_line_flag
```

---

## 4. Adapter re-point as measured

### 4.1 The floor does not block it — the estate does

**A RETAINED row's CONTENT may be edited freely, in both phases.** Probed
directly: appended a line to `tests/ideation-dashboard/conftest.py` (a
`replicated_at_destination` row) and to
`scripts/ideation_dashboard/intent_apply_lane.py` (a
`stays_openxfactory_adapter` row), committed, and the validator still printed
`OK`, exit 0. The reason is in the code: check 3 pass 2 skips every non-MOVED
row, and check 4 reads only PRESENCE. **So the re-point's import rewrites are
lawful under FLOOR PART 1 and can live in the same commit as the shed.**

PR #924's *"the repair is unavailable inside this act"* is correct as written —
it is about editing `cli.py` and `serve.py`, which ARE moved rows — but it does
not extend to the retained files, and post-shed `cli.py` is gone anyway.

### 4.2 The size of the re-point

| | files | sites |
| --- | ---: | ---: |
| retained `scripts/ideation_dashboard/*.py` importing a shed module | 4 | 15 |
| retained `tests/ideation-dashboard/test_*.py` | 23 | 80 |
| retained `tests/corpus-adapter/` | 1 | 1 |
| retained `tests/notebooklm/` | 3 | 7 |
| subtotal — sites naming a shed `scripts/ideation_dashboard/` module | **31** | **103** |
| **plus** `tests/ideation-dashboard/conftest.py` → `from session_fixtures import …` at `:106` | 1 | 1 |
| **total** | **32** | **104** |

Those 103 `scripts/ideation_dashboard/` sites name **32 distinct shed
modules**, and they do not have one
home:

* **14 land at `openxdox`** (`cli_gate`, `corpus_root`, `doxbench_scope`,
  `gate_console`, `gate_routes`, `generator`, `kickoff`, `openxdox_surface`,
  `register`, `register_edit_lane`, `serve_gate`, `serve_projection`,
  `snapshot`, `snapshot_registry`);
* **17 land at `opendox`** (`action_errors`, `authoring`, `boundary`,
  `branch_session`, `cli`, `cli_model_binding`, `cli_project`, `doxbench_hash`,
  `doxbench_model`, `doxbench_packet`, `doxbench_turns`, `lens`, `serve`,
  `serve_wire`, `session_git`, `session_pr`, `workbench`);
* **1 lands nowhere** — `profile_openxfactory`, the single `deleted_at_carve`
  row, named at 3 retained test sites. PR #924 measured that openXdox declares
  no replacement.

### 4.3 The three blockers, measured

**(i) `opendox` is not reachable from an openxFactory checkout.** openxFactory
mounts openXdox only (RULING F); openXdox nests `code` and `spec` and NOT
openDox; `contracts/opendox-pin.yaml` is `materialization: referenced`.
`openXdox-code`'s `pyproject.toml` declares `opendox @ git+…@8e9ffa62` as a
runtime dependency, but `pytest-suite.yml` installs with
`pip install --require-hashes -r requirements/hermes-runtime-contracts.lock`,
and a `git+` URL cannot carry a hash in a `--require-hashes` lock. **So 17 of
the 32 modules have no reachable home in openxFactory's CI as it stands.**

**(ii) Even the openXdox half does not import.** With only
`openXdox-code/src` on `sys.path`: **3 of 17 modules import**; the other 14
fail on `doc_health` (9) or `opendox` (5). With openxFactory's own `scripts/`
also on the path so `doc_health` resolves: **7 of 17**; the remaining 10 fail
on `opendox`. With BOTH legs' `src/` on the path: **17 of 17** openxdox
modules and **36 of 39** opendox modules import — the three that still fail
(`opendox.cli`, `opendox.serve`, `opendox.notebook_action`) fail on
`ideation_dashboard.snapshot_registry`, i.e. the pinned openDox still reaches
back into the pre-carve package (37 `ideation_dashboard` references and 22
`openxdox` back-imports across `src/opendox/*.py` at `8e9ffa62`).

**(iii) CI does not check the leg out.** `.github/workflows/pytest-suite.yml:339`
is `git submodule update --init openXwallet` and names no other gitlink. Until
a step inits `openXdox` **recursively**, `openXdox/code/` is empty on the
runner. (Unchanged from PR #924's finding.)

> **Editor's note (filing, 2026-09-10):** True at the spike's base, `main`
> `52e42be98c9e5bb4a5b1fc5cf89e235d5a349c5b` — at that commit,
> `.github/workflows/pytest-suite.yml`'s init step (there at lines 338–339)
> is `git submodule update --init openXwallet` and names no other gitlink,
> exactly as measured. PR #917 →
> `edf0e24f45b6e7baf5322023cbc1c43d28ff46cd`, one commit later on `main`,
> mounted the `openXdox` submodule and widened that same step (now at
> `pytest-suite.yml:359–360`) to
> `git submodule update --init openXwallet openXdox`. The two-level
> `openXdox/code/src` reach (§ 4.3(i)–(ii)) and the `doc_health` import
> failures stay open regardless — a non-recursive init of `openXdox` does
> not check out its own `code`/`spec` legs, so § 4.5's collection-error
> count is unaffected by this correction. Raised by a Copilot review
> comment on pull request #929 against current `main`, which had by then
> moved past the commit this note is pinned to.

### 4.4 The conftest, which is new since PR #924's probe

PR #924 probed deleting the one `deleted_at_carve` row and measured 4
collection ERRORS. **The full shed is worse in kind, not only in degree:**
`tests/ideation-dashboard/conftest.py` — a RETAINED
`replicated_at_destination` row — imports `session_fixtures` unconditionally at
`:106`, and `tests/ideation-dashboard/session_fixtures.py` is a
`moved_with_declared_edit` row to `opendox_code` (with
`also_replicated_to: [openxdox_code]`, RULED Q-L7 (a)). After the shed the
retained conftest imports a module openxFactory no longer has:

```
ImportError while loading conftest '…/tests/ideation-dashboard/conftest.py'.
tests/ideation-dashboard/conftest.py:106: in <module>
    from session_fixtures import (  # noqa: E402,F401  (fixture registration)
E   ModuleNotFoundError: No module named 'session_fixtures'
```

**RULED Q-L7 (a) fixed the DESTINATION side of exactly this pairing and left
the RETAINED side unfixed.** Naming the directory directly aborts the whole
pytest session before anything runs; naming `tests/` reports it as one
directory-level collection error that takes all 42 remaining files with it.

### 4.5 What is behind that one error

39 retained test modules under the three directories carry **1,104 `def test_`**:

* **7 files / 219 tests** reach ONLY shed modules;
* **21 files / 682 tests** reach BOTH shed and retained modules;
* **11 files / 203 tests** reach no shed module.

So **28 files and 901 tests** cannot run until the re-point resolves — which is
the real size of the thing, against `MIN_PASSED: "7070"` as a floor that may
only rise.

### 4.6 Can it live in the same atomic PR as the shed under exit (a)?

**Under exit (a) the FLOOR permits it and the ESTATE does not.** Three
sub-answers, each measured:

* **The mechanical rewrite of all 104 sites is lawful and in-scope** — retained
  rows' content is unconstrained by FLOOR PART 1 in either phase (§ 4.1).
* **Its target does not exist for 17 of the 32 modules**, and for the 1
  `profile_openxfactory` it exists nowhere. No sequencing of the same PR fixes
  that; it needs either openDox mounted/vendored in openxFactory (a pin-shape
  decision, RULING F says openxFactory declares only its DIRECT upstreams) or
  the § 3.5/§ 3.6 BUILD arc.
* **The alternatives both move a pinned number.** Making the 901 tests SKIP
  when the leg is absent moves `EXPECT_SKIPPED`, which is pinned EXACTLY as a
  SUM. Deleting the 28 files instead means changing their rows from
  `stays_openxfactory_adapter` to `deleted_at_carve` — a disposition change on
  28 rows, which is the "no row changes disposition" property of exit (a) given
  up, and which RULING DQ-1 ("the openxFactory remainder now includes the
  adapter's own tests") would have to be read against.

---

## 5. Diff size

Measured with `git diff --numstat main HEAD` on the spike branch, **excluding
the shed's own 319 deletions**, which belong to § 5.2 and not to any exit:

| file | + | − | of the additions |
| --- | ---: | ---: | --- |
| `scripts/validate-carve-manifest.py` | 199 | 11 | 128 non-comment, 61 comment, 10 blank |
| `tests/carve_manifest/test_carve_manifest.py` | 241 | 3 | 175 non-comment, 33 comment, 33 blank |
| `docs/opendox-carve-manifest.yaml` | 18 | 1 | **1 non-comment** (`phase: post-shed`), 15 comment, 2 blank |
| `docs/opendox-cutover-runbook.md` | 24 | 2 | prose in three hunks: § 0.4 (16), § 8 (5), § 11 (3) |
| **total** | **482** | **17** | of which **304 lines are executable** |

**Zero lines** in `scripts/verify-carve-arrival.py`, `scripts/carve_lines.py`,
`tests/carve_arrival/test_verify_carve_arrival.py` and
`.github/workflows/pytest-suite.yml` (verified by an empty `--numstat`).

**Manifest rows changing disposition: NONE.** 456 rows, 172/146/138 unchanged;
every `sha256` unchanged; `carve_commit: b075fd91…` unchanged; **`carve_tag:
opendox-carve-0` remains the label**, no new tag is cut, and no § 1 provenance
record moves.

`pytest-suite.yml` needs no edit FOR EXIT (a): the 11 added tests raise
SELECTED and PASSED, which are floors that may only rise, and add no skip
(`209 passed`, 0 skipped). The floors and `EXPECT_SKIPPED` do move for the
SHED — 3,404 `def test_` leave — but that is § 5.2's own act, already in
runbook § 8.

---

## 6. Exits (b) and (c) costed

### 6.1 Exit (b) — RE-CUT at the shed

Runbook § 11's procedure is six steps and two of them are Brett Heap's acts
(§ 12 act 5): name a new 40-hex `carve_commit` at a green `pytest-suite`, and
cut `opendox-carve-1` as an annotated tag from a fresh detached worktree,
pushed as the tag alone. **The decisive fact is what a re-cut AT the shed can
describe:** at the post-shed commit the 319 shed paths do not exist, and a row
for an absent path refuses in pass 1 (*"a digest of nothing is not a digest"*)
and in check 4. Measured against the exit-(a) tree — the surface at the
post-shed commit is **137 files, down from 456**; **9 of the 39 `moved_paths:`
prefixes match nothing** at the new referent and would refuse
`carve-surface-vacuous` (`tests/ideation_dashboard/`,
`scripts/validate-ideation-dashboard-contracts.py`, six `contracts/schemas/*`,
`docs/ideation-dashboard-session-runbook.md`); the re-cut document can carry
**0 moved rows** (was 318) and **0 declared edit lines** (was 794). So the
re-cut manifest is not a re-cut of the mapping — **it is a document with the
mapping deleted**, and § 11 step 6 ("any leg already arrived is re-verified
against the new manifest — a leg whose arrival was proved against a superseded
referent is proved against nothing") then has nothing to re-verify at any of
the four landed legs. Step 5 ("update EVERY record of § 1 that has already
landed") reaches **15 files / 40 lines across four repositories** naming
`b075fd91` or `opendox-carve-0` — openxFactory 11 files/34 lines (of which 1
is an archived record that must be ANNOTATED, not edited:
`openspec/changes/archive/2026-09-10-mirror-floor-regeneration-automation/tasks.md`),
`opensoft/openXdox` 2 files (`contracts/manifest.yaml`,
`contracts/opendox-pin.yaml`), `opensoft/openDox` 1
(`contracts/manifest.yaml`), `opensoft/openXdox-code` 1 (`pyproject.toml`) —
each a pull request that is Brett Heap's admin-merge under § 12 act 1.

### 6.2 Exit (c) — DECLARED RETIREMENT of the manifest

Measured by deleting `docs/opendox-carve-manifest.yaml` in the same commit as
the shed, with no code change at all:

```
$ python3 scripts/validate-carve-manifest.py
NO MANIFEST …/docs/opendox-carve-manifest.yaml (nothing to validate)
exit=0
$ python3 -m pytest tests/carve_manifest tests/carve_arrival -q
198 passed in 47.80s
```

**Retirement costs zero lines of code and produces a fully green suite; not one
test fails, and nothing is left that could ever go red.** It reaches green
through the one branch the validator's own docstring calls *"the one place here
that is not fail-closed … a deliberate seat-holding pass"*, written for the
window BEFORE the manifest existed. What disappears with it: the 318 digests
recomputed at the referent on every run; the 794 declared edit lines bounded
against the carve blob; the 456-file surface-completeness walk and its
`carve-file-undeclared` guard against anything appearing under the surface; and
the requirement that the 137 retained `stays_*` and `replicated_at_destination`
rows still be PRESENT — after which deleting a retained adapter file is silent.
**Seven real-manifest tests go vacuous** (3 in `tests/carve_manifest`, 4 in
`tests/carve_arrival`, each an `if manifest.is_file()` branch), and
`verify-carve-arrival.py` stops running at all — every destination becomes
`arrival-unreadable: the manifest … could not be read`, so the four landed legs
can never be re-verified against the document that admitted them.

---

## 7. Open questions for Brett

**Q1 — the exit.** (a), (b) or (c). Measured: (a) = 482 added / 17 removed
lines over 4 files, no row's disposition moves, digests frozen at `b075fd91`,
`opendox-carve-0` stays the label, validator and both carve suites green over
the shed tree (`209 passed`). (b) = a re-cut whose document carries 137 rows,
0 moved rows and 0 declared lines, plus 15 files / 40 lines of provenance
across four repositories and two of Brett Heap's own acts. (c) = zero lines,
green by absence, and the guarantees in § 6.2 gone.

**Q2 — the shed's own unbudgeted cost, under EVERY exit.** Family B: six
`contracts/schemas/*.schema.yaml` files are `moved_*` rows and 127 tracked
files name them (35 frozen release-digest inventories, 34 immutable archive
records, ~58 live including `contracts/manifest.yaml` and
`contracts/hermes-runtime/contract-index.yaml`). 20 tests in four suites go red
on the shed for this reason alone. It is named nowhere in runbook § 8, tasks.md
§ 5.2 or PR #924. Does it join the one atomic § 5 pull request, or does it get
its own act first?

**Q3 — the ceremony's own invocation.** Under (a), `--at <carve_commit>`
refuses once the phase flips, because at the carve commit every source path is
present. The spike corrects the two places that document it (the manifest's own
header block and runbook § 0.4) to say so. Is that acceptable, or should
`post-shed` admit `--at` at a pre-shed revision as a special case? (The spike
does NOT special-case it: a phase that could be satisfied two ways is a phase
that says less.)

**Q4 — a seventh refusal code.** (a) adds `carve-shed-incomplete` to a tuple
the source calls "FIXED, COMPLETE" and the tests restate as a literal. Adding
one is deliberate and test-visible, but it is a vocabulary change and other
code may branch on the codes.

**Q5 — the frozen surface, post-shed.** `check_surface`'s `appeared` arm
already refuses any NEW file under a `moved_paths:` prefix, in both phases and
today. Post-shed it bites harder: the surviving 137 files are openxFactory's
own live adapter, and adding a file beside them refuses `carve-file-undeclared`
until a row is added. Keep it (the surface is frozen), narrow it post-shed, or
drop it post-shed?

**Q6 — the retained conftest.** `tests/ideation-dashboard/conftest.py` (a
retained replica row) imports the shed `session_fixtures` at `:106`. RULED
Q-L7 (a) fixed the destination side of this exact pairing and left the retained
side. Options: edit the retained conftest (lawful in both phases, § 4.1); or
change `tests/ideation-dashboard/session_fixtures.py` from
`moved_with_declared_edit` + `also_replicated_to` to `not_moved /
replicated_at_destination` + `edits:` — one row, but a disposition change, and
the arrival contract at `opendox_code` would move from a placed row to a
`--replica-at` declaration.

**Q7 — the adapter re-point's scope.** 104 import sites in 32 files, 32 shed
modules split 17 `opendox` / 14 `openxdox` / 1 nowhere; 901 of 1,104 retained
tests behind them; `opendox` unreachable from openxFactory as pinned, and
`--require-hashes` will not take a `git+` URL. Is the re-point (i) deferred to
the BUILD arc with those 901 tests deleted or skipped in the meantime — both of
which move a pinned number — or (ii) does openxFactory gain a reach to openDox,
which RULING F's "declare only your DIRECT upstreams" reads against?

**Q8 — the 22-test drift.** Runbook § 8 says the shed removes 3,426 `def
test_`; measured over the 319 manifest-derived paths at `main` it is **3,404**.
Not resolved here.

---

## Appendix — how to reproduce

Disposable clone, nothing pushed:

```sh
git clone https://github.com/opensoft/openxFactory oxf && cd oxf
python3 -m venv ../venv && ../venv/bin/pip install --require-hashes \
    -r requirements/hermes-runtime-contracts.lock
# the shed list, derived from the manifest and never by hand
python3 - <<'PY' > /tmp/shed-paths.txt
import yaml, pathlib
doc = yaml.safe_load(pathlib.Path("docs/opendox-carve-manifest.yaml").read_text())
print("\n".join(r["source_path"] for r in doc["rows"]
                if r["disposition"] in ("moved_verbatim", "moved_with_declared_edit")
                or r.get("reason") == "deleted_at_carve"))
PY
git rm -q $(tr '\n' ' ' < /tmp/shed-paths.txt) && git commit -q -m probe
python3 scripts/validate-carve-manifest.py            # carve-path-absent, exit 2
```

> **Editor's note (filing, 2026-09-10):** This recipe clones whatever commit
> is current on `main` when run; it does not check out the pinned commit
> this note measures against, `main`
> `52e42be98c9e5bb4a5b1fc5cf89e235d5a349c5b` (see the header `Summary:` and
> § 3's environment line). Run
> `git checkout 52e42be98c9e5bb4a5b1fc5cf89e235d5a349c5b` immediately after
> the `clone`/`cd` line and before deriving `/tmp/shed-paths.txt`, or the
> manifest, the shed list and the validator's refusal can all differ from
> what is reported here — `main` has moved since (PR #917 →
> `edf0e24f45b6e7baf5322023cbc1c43d28ff46cd` alone added a submodule; see
> the § 4.3(iii) note above). Raised by a Copilot review comment on pull
> request #929 against the fix-round commit that added the other two
> notes.

The exit-(a) spike lives on the local branch `spike/exit-a`
(`05ef9236` → `88caf62e` → `b27f0555`) in the throwaway clone only. **It is not
pushed and is not proposed for landing as it stands.**
