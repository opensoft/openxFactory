# openDox cutover runbook — the CARVE arc

Status: draft
Kind: runbook
Repository context: openxFactory
Backed by: `openspec/changes/split-opendox-two-layer-product` § 3.2–3.8 and
  § 4, authored on **RULED OQ-J** (Brett Heap, `opensoft/openxFactory` #656,
  2026-09-09, by click-through: *"author `docs/opendox-cutover-runbook.md`
  before the first move"*), against the moves memo
  `opendox-carve-3-2-moves-memo-2026-09-09.md` and the § 3.1 manifest
  [`docs/opendox-carve-manifest.yaml`](opendox-carve-manifest.yaml)

**This document is authored BEFORE the carve it describes, and each phase
carries a rollback written before that phase is taken.** That discipline is the
openXwallet extraction's, task 3.2 verbatim — *"authored BEFORE the carve it
describes, with a rollback written before each phase is taken"* — and its
product, [`opensoft/openXwallet`'s `docs/openxwallet-cutover-runbook.md`][wallet],
is the model this file follows. A rollback written afterwards is not a rollback;
it is a description of what happened.

**Why `draft` and not `ratified`.** § 3 of the ratifying change has no task
naming this file: OQ-J created the obligation, and the change's own text is
amended by a later act, not by this runbook. The procedure below is written
against settled rulings and following it produces a checkable act — but no gate
in this estate refuses a carve step that skips this document. That sentence
belongs on every walk record this runbook produces.

[wallet]: https://github.com/opensoft/openXwallet/blob/main/docs/openxwallet-cutover-runbook.md

---

## 0. Preconditions — every one of them measured before Phase 1

| # | Precondition | State |
| --- | --- | --- |
| 0.1 | The manifest has LANDED | openxFactory PR **#865** → `17167481e9d69dec9347f1d26699b6218a697f53`, 2026-09-09T22:20:29Z |
| 0.2 | `carve_commit` is named and is a 40-hex commit, never `HEAD` | `b075fd91dc8fced8e1373825ba80220c33536bae` |
| 0.3 | The carve tag exists as a LABEL beside it | `opendox-carve-0` (annotated; tag object `a2b6d4ac`) |
| 0.4 | The manifest verifies at the revision being carved from | `python3 scripts/validate-carve-manifest.py` prints `OK` |
| 0.5 | The arrival verifier is landed and green | `python3 -m pytest tests/carve_arrival -q` |
| 0.6 | All six destination scaffolds are LEVEL | Phase 1 below (RULED OQ-O) |
| 0.7 | `git-filter-repo` is installed | `git filter-repo --version` (`/usr/bin/git-filter-repo`) |

**0.4 is the gate, not a courtesy.** `validate-carve-manifest.py` reads check 2
as ANCESTRY since § 3.1 part 1b, so it answers from any descendant of
`carve_commit`, and its checks 3 and 4 are where the pressure lives: a file
under the carve surface that has CHANGED on `main` since the carve refuses
`carve-digest-mismatch`, a file that has APPEARED refuses
`carve-file-undeclared`, and a row whose path has been DELETED refuses
`carve-path-absent`. **Any of the three means the carve commit is stale and
§ 11 (re-cutting) applies** — it does not mean the validator is wrong.

```sh
python3 scripts/validate-carve-manifest.py                 # from any descendant
python3 scripts/validate-carve-manifest.py --at b075fd91dc8fced8e1373825ba80220c33536bae
```

---

## 1. The NAMED CARVE COMMIT, and the THREE provenance records (RULED OQ-I)

```
CARVE_COMMIT = b075fd91dc8fced8e1373825ba80220c33536bae
CARVE_TAG    = opendox-carve-0          # a LABEL beside the commit, NEVER the referent
SOURCE       = opensoft/openxFactory    # PUBLIC since 2026-09-09 (see § 5.0)
```

`b075fd91` is `main` at the merge of the last pre-carve split (#855), with its
`pytest-suite` green (run 34387905421). **Never "HEAD"** — HEAD is not a
referent across a multi-pull-request wave, and this one spans at least eleven.

RULED OQ-I (Brett Heap, #656, 2026-09-09) places the referent in **three**
records, the openXwallet extraction's three shapes one level down:

1. **`carved_from:` in each ASSEMBLY ROOT's hand-authored
   `contracts/manifest.yaml`** — the machine-read record, at the one object
   whose single commit names both legs (Phase 3). Not in the legs: measured
   2026-09-09, only `opensoft/openDox` and `opensoft/openXdox` carry
   `contracts/` at all.
2. **`carve_commit:` in BOTH pin files** — openXdox's
   `contracts/opendox-pin.yaml` at its § 4.2 bump, and openxFactory's new
   `contracts/openxdox-pin.yaml` at § 5.1. The wallet's task 7.3 reason
   holds unchanged: the byte-identity referent must survive into the tree the
   gate reads, not only into a runbook.
3. **This runbook** — the procedure.

**No bare `CARVE_COMMIT` file.** The wallet extraction rejected that by name: an
unschema'd file nothing reads is the failure class a governance floor exists to
avoid.

### 1.1 The shape of `carved_from:`

Hand-authored and validated by nothing — `scripts/validate-manifest.py` in each
assembly root reads `project.yaml` (`kind: project-manifest`), not
`contracts/manifest.yaml`, and it is digest-pinned by `contracts/shape-pin.yaml`
so **it must not be edited to make it read one**. Adding a key therefore costs
nothing and is checked by nothing *except* `verify-carve-arrival.py`, which is
why the arrival verifier carries the `arrival-carved-from-mismatch` refusal.

```yaml
# opensoft/openDox — contracts/manifest.yaml
schema_version: 1
kind: contract-manifest
project: opendox
contract_bundle_version: none
entries: []

carved_from:
  repository: opensoft/openxFactory
  commit: "b075fd91dc8fced8e1373825ba80220c33536bae"
  carve_tag: opendox-carve-0
  manifest: docs/opendox-carve-manifest.yaml
  legs: {code: 123, spec: 56}
```

openXdox's is the same block with `legs: {code: 92, spec: 47}`.

---

## 2. What the floor is, and what proves it at the destination

FLOOR PART 1 (RULED OQ-1) replaced the wallet's byte-identity floor with a
mapping manifest. Measured in the landed file:

| disposition | rows | the proof owed at the destination |
| --- | ---: | --- |
| `moved_verbatim` | **172** | the arrived blob's `sha256` and mode EQUAL the row's |
| `moved_with_declared_edit` | **146** | commit A byte-identical; commit B's diff against the carve blob touches ONLY that row's `edits[].lines` |
| `not_moved` | **136** | absent at every destination — except the **18** `replicated_at_destination` rows, which are present at the destination AND retained here |

**318 rows move. 782 declared edit lines**: `import rewrites` 635, `path
constants` 121, `adapter calls` 26.

Per destination, and these are the numbers each leg's arrival run must report:

| destination | rows | verbatim / edited | declared edit lines | declared roots |
| --- | ---: | ---: | ---: | --- |
| `opendox_code` | 123 | 61 / 62 | 239 | `src/opendox/`, `tests/` |
| `opendox_spec` | 56 | 55 / 1 | 6 | `contracts/schemas/`, `docs/`, `examples/ideation-dashboard/` |
| `openxdox_code` | 92 | 9 / 83 | 537 | `scripts/`, `src/openxdox/`, `tests/` |
| `openxdox_spec` | 47 | 47 / 0 | 0 | `contracts/schemas/`, `examples/ideation-dashboard/` |
| `opendox_root` | 0 | — | — | none — the release identity only (§ 3.8) |

### 2.1 The arrival verifier

`scripts/validate-carve-manifest.py` validates the manifest AGAINST
openxFactory. **Nothing checked the arrival**, which is the half of FLOOR
PART 1 that lives at the destination, so this arc adds
`scripts/verify-carve-arrival.py` — same refusal-code idiom, exit 0 or 2 and
nothing else, run from openxFactory with a destination checkout in hand:

```sh
python3 scripts/verify-carve-arrival.py \
    --destination opendox_code \
    --dest-root   /path/to/openDox-code \
    --source-repo .                       \
    --phase A
```

Its five findings and one environment code:

| code | what it refuses |
| --- | --- |
| `arrival-missing` | a row for this destination has no file at `destination_path` |
| `arrival-digest-mismatch` | the arrived bytes or mode are not the row's (phase A for every moved row; both phases for `moved_verbatim`) |
| `arrival-undeclared-edit` | phase B: the arrived blob differs from the carve blob on a line no `edits[].lines` declares — **the refusal names the lines** |
| `arrival-undeclared-file` | a file under a declared root that no row places and no admission rule admits |
| `arrival-carved-from-mismatch` | an assembly root's `contracts/manifest.yaml` carries no `carved_from`, or one naming another repository or another commit |
| `arrival-unreadable` | the environment and the encoding: no git, an unreadable manifest, an unknown `--destination`, a `--dest-root` that is not a directory, a source repository that does not carry `carve_commit` |

**It lives in openxFactory and is never copied into six repositories.** The
manifest lives here; a verifier copied six ways is six things to keep in step
with one document.

**What it deliberately does NOT prove.** A `replicated_at_destination` row
carries no `destination`, no `destination_path` and no digest — by the row
grammar, because the manifest declares what LEAVES and a replica is a copy the
destination assembles. So the verifier ADMITS a destination file whose bytes
equal a replica's blob at `carve_commit` and reports the count, and it cannot
refuse a replica that drifted. That is the manifest's limit, not the verifier's:
`tests/corpus-adapter/test_conformance.py`'s implementation-aware block MUST be
rewritten at each destination to that destination's own factory, so a replica is
neither verbatim nor declared-edit by construction. Files CREATED at a
destination (RULED OQ-C — `pyproject.toml`, `conftest.py`, `pytest.ini`,
openXdox-code's `openxfactory_surface.py`) have no row either, and are named on
the command line with `--allow-created`, once each, so that every unplaced file
at a destination is either admitted by a rule or written down in the pull
request that admits it.

---

## 3. Phase 0 — the manifest. **DONE.**

**ROLLBACK (written first): revert PR #865.** Nothing consumed the manifest
before Phase 2, so a revert restores the world.

Landed at `17167481` on Brett Heap's word *"merge 1b when green, then the
manifest"*. § 3.1 is complete: the pre-carve splits (S-1 #837, S-2 #836, S-3
#835, B-1 #843, B-2 #852, B-4 #855), the validator (#839) with its ancestry
amendment (#864), the carve-commit ceremony, and the manifest itself.

---

## 4. Phase 1 — level the six scaffolds (RULED OQ-O). **BEFORE any arrival.**

**ROLLBACK (written first): revert the levelling pull request.** Nothing has
been carved; each of the six repositories returns to its 2026-09-06 scaffold and
openxFactory is untouched.

One small pull request per repository, so that **a carve failure is never
confounded with a scaffold difference**. Measured 2026-09-09, the differences
that are load-bearing:

| gap | where | why it bites |
| --- | --- | --- |
| no `docs/` and no `docs/branch-protection.md` | `openXdox`, `openXdox-spec`, `openXdox-code` | the openDox family has all three; a leg with no `docs/` cannot take `opendox_spec`'s one `docs/` row's sibling convention |
| no `openspec/project.md` | `openXdox-spec` | it is the leg that RECEIVES openXdox's requirements |
| `strict_required_status_checks_policy` | `false` in the openDox family, `true` in the openXdox family | `true` means the branch must be up to date with `main` before merge — a sequencing cost, not a defect, but it must be known before it is met |
| pytest unpinned | `openXdox-code` (openDox-code pins `pytest>=8,<9`) | an unpinned pytest major is how a 74-file arrived suite goes red for a reason that has nothing to do with the carve |
| `permissions:` absent | `openXdox-code`'s `validate.yml` | openDox-code declares `contents: read` |

**The import root rides this phase, not the arrival.** Both `-code` legs use a
`src/` layout — `tests/test_leg_shape.py::test_role_directory_exists` asserts
`src/` is a directory, inside the required `validate` check — and neither leg has
`pyproject.toml`, `conftest.py`, `pytest.ini` or any `PYTHONPATH`. With `src/`
and none of those, `import opendox` does not resolve and `validate` goes red on
the first carved commit. Copy openxFactory's own idiom: a `pytest.ini` **rootdir
anchor** plus a root `conftest.py` that inserts `src/` on `sys.path`. Copying
the anchor is not optional — `tests/hermeticity.py`'s conftest-chain guarantee
does not survive without it.

**Verification:** each leg's own `validate` check, green, on the levelling pull
request. **Brett's acts:** every one of the six pull requests is admin-merged on
his word (§ 12).

---

## 5. Phase 2 — the legs, ONE DESTINATION AT A TIME (RULED OQ-H)

**ROLLBACK (written first): close the pull request, or revert it if it merged;
delete the scratch mirror.** The legs pin nothing and are pinned by nothing
until Phase 3, so a reverted arrival leaves a scaffold. **openxFactory is
untouched by this whole phase** — the carve COPIES and deletes nothing; the
shed is § 5 (Phase 5 below), and `design.md`'s own rollback line agrees: *"the
manifest is the inverse map; openxFactory has not shed yet."*

### 5.0 Why history, and why the wallet's shape does not transfer whole

RULED OQ-H (Brett Heap, #656, 2026-09-09): **history-preserving `git
filter-repo` over the manifest's rows**, the openXwallet method.

The scout memo had recommended a tree copy, on the reading that a
history-preserving filter publishes a PRIVATE repository's 181+ commits — their
messages, their author identities and every openxFactory issue number they cite
— into six public repositories. **That objection died when the source went
public.** `opensoft/openxFactory` was flipped to public by Brett Heap on
2026-09-09 (~22:0xZ, Apache-2.0, after a clean full-history secret scan), so the
wallet precedent transfers exactly: openXwallet's own oldest commits predate the
repository, because they are rewritten openxFactory history carried by
filter-repo.

**One thing does NOT transfer, and it decides the branch shape.** The wallet's
task 3.4 created `opensoft/openXwallet` EMPTY and the filtered history became
that repository's history — no graft, and `main` was the carve. All six
destinations here were scaffolded on 2026-09-06 and already carry history, a
`.github/CODEOWNERS` of `* @brettheap`, and an org ruleset (`18834180`,
`require_code_owner_review: true`) on `~DEFAULT_BRANCH`. So:

> **The filtered history is joined to the scaffold with
> `git merge --allow-unrelated-histories` and lands as a PULL-REQUEST BRANCH.
> The scaffold's `main` is never rewritten and never force-pushed.**

The result is a repository with two roots. That is accepted, in writing, as the
price of both the ruled method and an unrewritten protected branch. Record with
it what history does *not* buy here: filter-repo's rename directives apply to
**all** history, so a path that did not exist at its carve-commit spelling
carries partial or no blame continuity — `serve_workbench.py` and
`serve_project.py` are § 2.4 creations, and `doxbench_scope_types.py`,
`lens_submission.py` and `openxdox_surface.py` are days old. RULED OQ-1 already
declared bisectability unavailable here; history is carried because it is cheap
and because the wallet carried it, not because it makes the carve bisectable.

### 5.1 The order, which is HARD

```
opendox_code → openDox root pin → openxdox_code → openXdox root pins
             → openXdox's contracts/opendox-pin.yaml bump → openxFactory § 5
```

openXdox imports openDox; **two pin moves per hop**, as design D12 accepted in
writing. The spec legs (`opendox_spec`, `openxdox_spec`) have no import edges
and may run beside their code legs. **Hold `openxdox_spec` for its open PR #3**
and take a merge-from-main first: it is the one destination with a live pull
request, and `strict_required_status_checks_policy: true` there means the branch
must be up to date with `main` before it can merge.

### 5.2 The mirror, and the control

A **fresh** mirror, never the shared checkout and never a worktree of it: a
carve must read a tree nobody else is editing, and `git filter-repo` refuses an
unfresh clone by design.

```sh
CARVE_COMMIT=b075fd91dc8fced8e1373825ba80220c33536bae
DEST=opendox_code                       # one destination per pass

git clone https://github.com/opensoft/openxFactory.git oxf-carve-src
git -C oxf-carve-src checkout "$CARVE_COMMIT"
```

**The control, before the carve.** Re-verify the manifest against the mirror at
the carve commit. Without this control a post-carve match proves the manifest
stale rather than the carve faithful.

```sh
python3 scripts/validate-carve-manifest.py --repo oxf-carve-src --at "$CARVE_COMMIT"
# expect: OK … 454 row(s) … 318 digest(s) recomputed
```

### 5.3 The path file, generated FROM THE MANIFEST

The destination tree must be a function of the document, which is the whole
difference between this carve and the wallet's twelve hand-listed path sets.
`--paths-from-file` takes one literal path per line and `old==>new` renames;
**0 rows change a basename**, so every directive here is a relocation.

```sh
python3 - "$DEST" <<'PY' > paths-$DEST.txt
import sys, yaml
dest = sys.argv[1]
doc = yaml.safe_load(open("docs/opendox-carve-manifest.yaml"))
for row in doc["rows"]:
    if row.get("destination") == dest:
        print(f'{row["source_path"]}==>{row["destination_path"]}')
PY
wc -l paths-$DEST.txt        # 123 for opendox_code; see § 2's table
```

### 5.4 The carve

```sh
git -C oxf-carve-src filter-repo --paths-from-file ../paths-$DEST.txt --refs "$CARVE_COMMIT"
```

`--refs "$CARVE_COMMIT"` keeps the rewrite anchored on the carve commit's own
history rather than on whatever `main` has become. filter-repo removes `origin`
when it finishes; that is the tool refusing to let a rewritten history be pushed
back over its source, and it must not be worked around.

### 5.5 The two commits, and why they are two

**Move first, edit second, at the destination, in the same pull request.**

* **Commit A** places every row's blob byte-identical to `carve_commit`, so the
  arrival verifier can prove **every moved row of that destination at phase A**
  — the strongest statement available, and the analogue of the wallet's
  *"100/100 at the carve layer"*.
* **Commit B** applies that destination's declared edits AND NOTHING ELSE. Its
  diff is then mechanically checkable line-for-line against `edits[].lines`, and
  a reviewer reads 239 lines rather than 97,120.

```sh
git clone https://github.com/opensoft/openDox-code.git dest-openDox-code
cd dest-openDox-code || exit 1
git checkout -b carve/opendox-code-arrival
git remote add carved ../oxf-carve-src
git fetch carved
git merge --allow-unrelated-histories carved/main \
    -m "Commit A — the openDox-code arrival at opendox-carve-0 (123 rows, byte-identical)"
```

Then, in openxFactory, with the destination checkout in hand:

```sh
python3 scripts/verify-carve-arrival.py --destination opendox_code \
    --dest-root ../dest-openDox-code --source-repo ../oxf-carve-src --phase A
# expect exit 0: 123 row(s) arrived … 123 digest(s) verified
```

**Only then** apply the declared edits as commit B, and re-verify at phase B:

```sh
python3 scripts/verify-carve-arrival.py --destination opendox_code \
    --dest-root ../dest-openDox-code --source-repo ../oxf-carve-src --phase B \
    --allow-created pytest.ini --allow-created conftest.py
# expect exit 0: 62 edited row(s), declared-lines-only
```

The dominant edit is mechanical — `ideation_dashboard.X` → `opendox.X` /
`openxdox.X` on the `import rewrites` rows, plus the dead
`sys.path.insert(0, _SCRIPTS_DIR)` shims (`serve.py:109-111`,
`serve_gate.py:40-42`, `serve_projection.py:47-49`), which exist only because
`scripts/` is not a package and are dead under `src/<pkg>/`. The **26
`adapter calls` lines are the ones that need judgement**: `serve.py:618`
(`doc_health.corpus.RealGit` → D2's `resolve`), `cli_gate.py:251`,
`workbench.py:82-83, 745, 1406-1408`, `corpus_root.py:34, 43`,
`authoring.py:317-318`. A corpus-shaped literal is an `adapter calls` edit and
never a `path constant`: filing it as a path constant would let openDox ship
openxFactory's tree shape as a literal, which is `corpus-adapter-seam`
requirement 4's failure exactly.

### 5.6 What lands with commit B and has NO row

Files CREATED at a destination get no row (RULED OQ-C). Each one is named to
the verifier with `--allow-created`, and the pull request says why:

* both `-code` legs: `pytest.ini` (the rootdir anchor) and a root `conftest.py`
  — **unless Phase 1 already landed them, which is where they belong**;
* the `replicated_at_destination` copies — admitted automatically when their
  bytes still equal the carve blob, and named with `--allow-created` once
  their destination-side rewrite has begun;
* **`openxdox-code/src/openxdox/openxfactory_surface.py`** — the mirror of
  `openxdox_surface.py`, the re-export surface openxFactory's own adapter
  reaches after the shed (RULED OQ-L). One line plus its reason per name, on
  `openxdox_surface.py`'s own stated discipline. It does not exist yet and it
  is nobody's task but § 4.1's.

**Verification, per leg:** phase A run, phase B run, and the leg's own
`validate` check green. **Brett's acts:** the pull request is admin-merged on
his word — `gh` opens pull requests as `brettheap`, so the code-owner
requirement cannot clear on his own click and admin merge with a recorded
`OrganizationAdmin` bypass actor is the standing pattern (§ 12).

---

## 6. Phase 3 — the assembly roots: `carved_from` + gitlink + pin, ONE COMMIT

**ROLLBACK (written first): revert the root commit.** The legs are unchanged by
it and nothing outside the root reads it yet; openxFactory still pins nothing.

Per assembly root, in a single commit — this is the doctrine's lockstep
invariant and the aggregation's own gitlink trap one level down:

1. the leg **gitlink** at `submodule_path` (`code`, `spec`);
2. `contracts/code-pin.yaml` / `contracts/spec-pin.yaml` — `commit:` and
   `digests.tree_sha256:` (`sorted-ls-tree-r-v1`);
3. `carved_from:` in `contracts/manifest.yaml` (§ 1.1).

**Verify the gitlink object EXISTS before pushing.** Git stores a submodule
gitlink without checking that the object is present in the submodule, so a wrong
pin commits and pushes clean:

```sh
git -C code cat-file -t <sha>      # must print: commit
```

**openXdox's root additionally BUMPS `contracts/opendox-pin.yaml`** (§ 4.2) to
openDox's root commit and tree digest, and adds `carve_commit:` to it (record 2
of § 1). Today it pins `bad2d2ad4c93c2d0cc3ed82ec56de3e5eecbc2fe`.

**Verification:** each root's own `validate` (`validate-manifest.py`,
`validate-pins.py`, `validate-repository-naming.py`), plus

```sh
python3 scripts/verify-carve-arrival.py --destination opendox_root \
    --dest-root ../dest-openDox --source-repo . --phase A
# the carved_from check is this destination's whole job: it declares 0 rows
```

**Brett's acts:** the pin is a pin act and the estate hand-bumps pins; the pull
request is admin-merged on his word.

---

## 7. Phase 4 — the openXdox SUBMODULE in openxFactory (RULED OQ-L)

**ROLLBACK (written first): `git submodule deinit` the gitlink and revert the
pin commit.** One revert in the consumer; the destinations are untouched.

RULED OQ-L: Brett chose a **GIT SUBMODULE of the openXdox ASSEMBLY ROOT** over
the memo's recommended installable package. openxFactory pins openXdox and
**nothing else** (RULING F, 2026-09-05, *"rule F openXdox only"*); openDox's
commit is a DERIVED value read through openXdox's own `contracts/opendox-pin.yaml`
and is never separately declared, pinned or mounted here.

The gitlink IS the commit pin RULING F requires. `contracts/openxdox-pin.yaml`
is § 5.1's new file and carries `carve_commit:` (record 2 of § 1) beside the
commit and tree digest. **The estate's submodule discipline applies unchanged**:
the gitlink, the pin file and every workflow reference of the form
`<org>/<repo>/…@<sha>` move in ONE commit, and `git cat-file -t <sha>` inside
the submodule is what says the pin names a real object.

**The mechanism the memo flagged as undeclared is declared here.** A submodule
mounts a REPOSITORY, and openXdox's code is one level further down, inside its
own `code` submodule. So openxFactory's 27 stays-column files with 124 import
sites into travelling modules resolve `openxdox` through **the mounted leg's
`src/`**, declared once in § 5.1's `tests/conftest.py` path idiom rather than
discovered file by file. openXdox-code owes the re-export surface module
(§ 5.6) or there is nothing lawful to import.

---

## 8. Phase 5 — openxFactory § 5, ONE ATOMIC PULL REQUEST

**ROLLBACK (written first): revert the § 5 pull request.** It is one commit set
by construction, so the revert is one act; the destinations keep everything they
were given, because this phase gives them nothing.

The wallet's P3 reasoning applies for the same reason — *no ordering of two
commits leaves a green intermediate* — so the pin, the gitlink, the shed, the
floor re-cut and the workflow conversion land together:

* `contracts/openxdox-pin.yaml` + the gitlink;
* the shed of the carve surface's stays-nothing half;
* **the floors, re-cut as a deliberate act with its own evidence row.**
  `.github/workflows/pytest-suite.yml` carries `MIN_SELECTED: "7090"` and
  `MIN_PASSED: "7070"` (floors that may only rise) and `EXPECT_SKIPPED: "21"`
  (pinned EXACTLY, and a SUM). The shed removes 3,426 `def test_`, so both
  floors fail by construction and `EXPECT_SKIPPED` moves twice — the
  `find_spec`-guarded skips in `tests/notebooklm/` and `tests/hermeticity.py`
  APPEAR while the dashboard suite's own skips VANISH. Re-cut downward with the
  reason in the commit message and the reason for each skip named. **Never
  "lowered to make it green."**
* de-floor FIRST per § 5.6: `contracts/review-lane-floor-snapshot.yaml`'s
  machine-generated block enumerates every tracked path under
  `openspec/specs/`, and it must account for BOTH directions — the removed
  capability directory and the added ones. Never hand-edited.
* `tests/hermeticity.py`'s replacement: `runner_seams()` self-degrades to `()`
  when the package is gone, and `CONFTEST_HOOKUPS` still names a directory the
  shed deletes, while the test that pins that tuple is deleted by the same act.
  **The guard's own proof leaves with the thing it guards**, and § 5 owes a
  replacement rather than an absence.

**Not touched by the carve, and named here so it is not conflated during
review:** `.github/merge-approval-envelope.yml` and
`merge-master-approval.yml:86-87` enroll `ideation/dashboard/intents/**` and
`ideation/dashboard/gate-records/**` — a live DATA directory, not
`scripts/ideation_dashboard/`.

---

## 9. Phase 6 — the tags (§ 3.8 and § 4.6). **BRETT'S ACT, ALWAYS.**

**ROLLBACK (written first): delete the tag, locally and on the remote —
but ONLY before anything pins it.** From the moment a bundle is published the
honest reversal is a FOLLOWING RELEASE, never a revert of a cut: *a published
bundle is not unpublished.*

`dox-v1.0` in `opensoft/openDox` and `xdox-v1.0` in `opensoft/openXdox`,
annotated, **in the ASSEMBLY ROOT** (amended 2026-09-05) over the commit that
names both legs — a tag on a leg describes half a project — verified from an
independently refreshed checkout, with `contracts/CHANGELOG.md` and
`contracts/manifest.yaml` entries beside it. *"Annotated tags cut by the
operator and no workflow makes them."*

**Sequencing, stated because § 3.8's own text misleads.** § 3.8 gates the tag on
"the floor's four parts green", and floor parts 2 and 4 are § 5.4 and § 5.5 —
openxFactory-side work. **§ 3.8 therefore cannot close inside § 3**, and RULED
OQ-N's split says so: the CARVE arc is § 3.2–3.4, § 3.7's arrival and § 3.8's
`carved_from` bookkeeping; the BUILD arc (§ 3.5's FastAPI + Postgres runtime,
§ 3.6's repository-creation act) follows, as openDox-code's own changes under
openDox-spec's own OpenSpec instance. Nothing in § 4 or § 5 waits on the build.

**FLOOR PART 2, as RULED OQ-K restates it.** § 5.4's *"openDox + openXdox + the
openxFactory remainder SHALL equal the pre-split count"* is arithmetically false
as written: the 18 `replicated_at_destination` rows carry test functions that
exist at two or three destinations at once, so the post-split sum EXCEEDS the
pre-split count by design. The floor is **a source→destination mapping plus a
declared replica multiplicity** — every pre-split test function has ≥1
post-split home, no home is lost, and the replica set is enumerated with its
multiplicity — pinned with `pytest-suite.yml`'s existing triple idiom at each
destination. The equality reading fails on its first run and would be "fixed" by
deleting replicas, which is the wrong repair. RULED OQ-K is carried by a small
amendment pull request to the change, not by this runbook.

---

## 10. Rollback, collected per phase

| Phase | Rollback | Cost |
| --- | --- | --- |
| 0 — the manifest | revert #865 | zero; nothing consumed it |
| 1 — scaffold levelling | revert the levelling pull request | zero; six scaffolds, unchanged |
| 2 — a leg's arrival | close or revert the pull request; delete the scratch mirror | zero; the legs pin nothing and are pinned by nothing |
| 3 — an assembly root | revert the root commit (gitlink + pin + `carved_from` together) | zero outside that root |
| 4 — the openxFactory submodule | `git submodule deinit` + revert the pin commit | one revert in the consumer |
| 5 — openxFactory § 5 | revert the single atomic pull request | one revert; the destinations keep what they were given |
| 6 — the tags | delete the tag, **only before anything pins it** | after that: a following release, never a revert |

**The arc-wide rollback through Phase 4**: every destination is additive at a
repository that pins nothing yet. **openxFactory is untouched until Phase 5**,
so through Phase 4 the reversal is "leave the legs unpinned" and costs the
source repository nothing at all.

---

## 11. Re-cutting `carve_commit`

If `main` moves under the carve — precondition 0.4 refuses with
`carve-digest-mismatch`, `carve-file-undeclared` or `carve-path-absent` — the
manifest is **re-cut at a NEW `carve_commit` and every digest is RECOMPUTED,
never carried forward**. That sentence is `contracts/openxwallet-pin.yaml`'s
own, and the manifest's header repeats it.

The procedure:

1. **STOP.** Do not carve against a refused manifest and do not edit a digest to
   make the validator pass.
2. Name the new commit — one 40-hex sha, `main` at a green `pytest-suite`, never
   `HEAD`. **Brett's act** (§ 12).
3. Cut a new annotated tag beside it, `opendox-carve-<n>`, from a fresh detached
   worktree of that sha, pushed as the tag alone. **A LABEL, never the
   referent.**
4. Re-emit the manifest at that commit, as the last thing on that tree, and
   re-verify with `--at <new sha>`.
5. Update **every** record of § 1 that has already landed: `carved_from:` in any
   assembly root that has one, `carve_commit:` in any pin file that has one, and
   this runbook's § 1.
6. Any leg already arrived is re-verified against the new manifest — a leg whose
   arrival was proved against a superseded referent is proved against nothing.

Steps 5 and 6 are why the re-cut gets cheaper the earlier it happens, and why
precondition 0.4 is run before every phase and not only before Phase 2.

---

## 12. Brett Heap's acts, collected

Nothing in this arc is performed by a lane without one of these:

| # | Act | Where |
| --- | --- | --- |
| 1 | **Every destination pull request, admin-merged on his word.** Org ruleset `18834180` requires code-owner review on all six, `.github/CODEOWNERS` is `* @brettheap`, and `gh` opens pull requests AS `brettheap` — so the requirement cannot clear on his own click. Admin merge with a recorded `OrganizationAdmin` bypass actor is the standing pattern | Phases 1, 2, 3 |
| 2 | Ruleset promotion to ACTIVE, and any required-check change, at the six | Phase 1 |
| 3 | **The pins** — openXdox's `opendox-pin.yaml` bump and openxFactory's new `openxdox-pin.yaml`; the estate hand-bumps pins | Phases 3, 4 |
| 4 | **The tags** — `dox-v1.0`, `xdox-v1.0`, and openxFactory's MAJOR | Phase 6, § 5.7 |
| 5 | **Re-cutting `carve_commit`** if `main` moves under the carve | § 11 |
| 6 | The openxFactory § 5 merge — the largest diff in this repository's history | Phase 5 |

**The lane's, as pull requests:** the arrival commits and declared edits at the
four legs; the assembly-root pin/gitlink commits; this runbook; the arrival
verifier; the scaffold levelling; the openxFactory § 5 diff. **None of them
merges without act 1.**
