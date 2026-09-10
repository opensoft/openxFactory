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
| `not_moved` | **138** | absent at every destination — except the **20** `replicated_at_destination` rows, which are present at the destination AND retained here; **one of them declares a line** (RULED Q-L7 (a)) and its copies are held to it |

**318 rows move. 794 declared edit lines**: `import rewrites` 636, `path
constants` 132, `adapter calls` 26. **147 rows carry `edits:`** — the 146
`moved_with_declared_edit` rows and, since RULED Q-L7 (a), one replica row.

The row and line totals above are the file AS AMENDED on 2026-09-10 under
RULING Q-L1 (`#656`, comment `5611834121`): the two § 2.4 extension-point seams
joined the `replicated_at_destination` rows, and eleven lines over seven
`opendox_code` rows were declared — ten of them citations too short to express
the edit their row's own note described, plus the seam file's own path
constant. The digest total does not move with them — a `not_moved` row carries
none.

**And AS AMENDED the same day under RULED Q-L7 (a)** (`#656`, comment
`5618683833`, verbatim *"rule Q-L7 (a)"*), which moved the line total by one and
the row total by none. Two grammar additions, both about the same pair of
test-layout files that carve leg 1 measured:

* `tests/ideation-dashboard/session_fixtures.py` — a `moved_with_declared_edit`
  row to `opendox_code` — gains **`also_replicated_to: [openxdox_code]`**. The
  replicated `tests/ideation-dashboard/conftest.py` imports it unconditionally
  at `:106`, so collecting `tests/` at openXdox-code would have failed at
  import on a file no row placed there. It stays ONE row with ONE destination;
  the list adds a REPLICA, whose placement is the leg's and is declared with
  `--replica-at`. Its four `import rewrites` lines are the correct text at both
  legs: the three modules they name all arrive at `src/opendox/`, so
  `opendox.X` is right at openDox-code (its own package) and at openXdox-code
  (which pins openDox), and `openxdox.X` would name modules openXdox does not
  own.
* `tests/ideation-dashboard/conftest.py` gains the first **`edits:` any replica
  row has carried** — `path constants`, line 25. `REPO_ROOT =
  HERE.parent.parent` resolves outside the destination repository once the copy
  lands one directory shallower at `tests/conftest.py`, and must read
  `HERE.parent`. It is applied identically at every replica, which is a bound on
  the LINE: `verify-carve-arrival.py` verifies one destination per run and
  compares no two legs' copies with each other.

The **794th line belongs to a replica row and therefore to no destination
column below**: a replica row names no destination at all, so the per-leg
declared-line figures still sum to 793, and the extra line is owed by every leg
that places that conftest — both `-code` legs. **Under every other `not_moved`
reason `edits:` is still a refusal**: RULING OQ-B's three
`stays_openxfactory_governance` rows stay here and take their import rewrite in
openxFactory, so they go on recording it in `evidence:`. And this is **not**
RULING OQ-K's owed FLOOR PART 2 field (§ 9): that one names REPOSITORIES on a
test-bearing replica row for the multiplicity sum, and both files here carry
zero `def test_` at the carve commit.

Per destination, and these are the numbers each leg's arrival run must report:

| destination | rows | verbatim / edited | declared edit lines | declared roots |
| --- | ---: | ---: | ---: | --- |
| `opendox_code` | 123 | 61 / 62 | 250 | `src/opendox`, `tests` |
| `opendox_spec` | 56 | 55 / 1 | 6 | `contracts/schemas`, `docs`, `examples/ideation-dashboard` |
| `openxdox_code` | 92 | 9 / 83 | 537 | `scripts`, `src/openxdox`, `tests` |
| `openxdox_spec` | 47 | 47 / 0 | 0 | `contracts/schemas`, `examples/ideation-dashboard` |
| `opendox_root` | 0 | — | — | none — the release identity only (§ 3.8) |

The declared-roots column is spelled **exactly as a run prints it** — no
trailing slash — because an operator's first act after a leg lands is to read
`… file(s) under <roots> …` off the verifier's own line and compare it with
this table. `tests/carve_arrival/test_verify_carve_arrival.py::test_the_real_manifest_declares_the_roots_the_runbook_names`
asserts these five cells against the landed manifest, so the table is checked
rather than described.

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

An ASSEMBLY ROOT is addressed by the repository it is, because `destinations:`
is a map of the places rows GO and openXdox's root receives none:

```sh
python3 scripts/verify-carve-arrival.py \
    --assembly-root opensoft/openXdox \
    --dest-root     /path/to/openXdox
```

Its five findings and one environment code:

| code | what it refuses |
| --- | --- |
| `arrival-missing` | a row for this destination has no file at `destination_path` |
| `arrival-digest-mismatch` | the arrived bytes or mode are not the row's (phase A for every moved row; both phases for `moved_verbatim`) |
| `arrival-undeclared-edit` | phase B: the arrived blob differs from the carve blob on a line no `edits[].lines` declares — **the refusal names the lines** |
| `arrival-undeclared-file` | an ENTRY under a declared root that no row places and no admission rule admits — a file, a symlink, or a **symlink to a directory** (git stores it as a `120000` blob, and `os.walk` would hand it to `dirnames` and never read it); also a file admitted as SCAFFOLD whose bytes are not the destination's own at `--dest-base` |
| `arrival-carved-from-mismatch` | an assembly root's `contracts/manifest.yaml` carries no `carved_from`, or one naming another repository or another commit |
| `arrival-unreadable` | the environment and the encoding: no git, an unreadable manifest, an unknown `--destination`, a `--dest-root` that is not a directory, a `--dest-base` that resolves to no commit, `--destination` and `--assembly-root` together, a source repository that does not carry `carve_commit`. It is also the CATCH-ALL that holds the exit contract: any exception the checks did not name arrives as this code and exit 2, never as a traceback and exit 1 |

**It lives in openxFactory and is never copied into six repositories.** The
manifest lives here; a verifier copied six ways is six things to keep in step
with one document.

**WHAT A LINE IS, for the whole floor (RULED Q-L8 (c), 2026-09-10).** Wherever
the floor names a line — `edits[].lines` in the manifest, the bound
`validate-carve-manifest.py` holds them to, the numbers a
`verify-carve-arrival.py` refusal prints — **a line is a `\n`-terminated record
of the raw bytes, line N is the Nth such record counting from 1, a trailing
newline closes the last record without opening another, and `\r` is content and
not a terminator.** The definition lives in `scripts/carve_lines.py` and both
tools import it; neither carries a second one. It is `git diff`'s numbering,
`grep -n`'s, and the one the manifest's 794 declared lines were written in.
Before the ruling the arrival verifier numbered with `str.splitlines()`, which
also breaks on `U+2028`, `U+2029`, `\v`, `\f`, `\x1c`-`\x1e` and `\x85`: the
three rows whose blobs carry `U+2028` inside a line were 522 / 2367 / 738
lines long to one half of the floor and 521 / 2364 / 734 to the other, so six
declared lines over the two `moved_with_declared_edit` rows among them
(`test_gate_console.py` 870, 1627, 1785, 1786, 1810 and `test_round_trip.py`
728) could not be applied at `openxdox_code` — carve leg 3's finding 5,
confirmed by its independent verification. **No row was re-declared:** measured
line by line at `carve_commit`, all six already named exactly the `import
rewrites` / `path constants` text their classes describe under this definition,
so the numbering moved and the document did not. The one difference this
definition cannot express is a final newline gained or lost, and the verifier
keeps a refusal for it.

**What it deliberately does NOT prove, and what the operator can make it
prove.** A `replicated_at_destination` row carries no `destination`, no
`destination_path` and no digest — by the row grammar, because the manifest
declares what LEAVES and a replica is a copy the destination assembles.
Measured over the landed manifest, all **20** such rows carry none of the four.
So nothing in the document says where a replica landed, and the verifier does
not guess: a derivation like `src/<pkg>/<basename>` would be inventing the
answer it then checked.

Two readings, both available, and the choice is per replica:

* **Undeclared** — the verifier ADMITS a destination file whose bytes equal a
  replica's **non-empty** blob at `carve_commit` and reports the count. It
  cannot say whether the replica is there at all, and it cannot refuse one that
  drifted. **Empty bytes identify nothing and admit nothing**: two of the 20
  rows are `fixtures/empty/*/.gitkeep`, so an empty-digest admission would let
  any empty created file — an `__init__.py`, a truncated module — in as "a
  replica", which is true of the bytes and false of the file. An empty replica
  is admitted only by declaring it.
* **Declared**, with `--replica-at <source_path>=<destination path>` — the
  per-leg table below in machine form, restated in the pull request that places
  it. A declared replica is answered with the two codes a ROW is answered with,
  `arrival-missing` and `arrival-digest-mismatch`, and is admitted in the walk
  by NAME rather than by a coincidence of bytes. Declare every replica that is
  a pure copy.

The one replica that must NOT be declared is
`tests/corpus-adapter/test_conformance.py`: its implementation-aware block
(`:72-84`) imports the home factory and MUST be rewritten at each destination
to that destination's own, so it is neither verbatim nor declared-edit by
construction. Leaving it undeclared leaves it exactly where it was.

**The two shapes RULED Q-L7 (a) added, and exactly what a run proves about
them.** Both reach the arrival verifier, and neither adds a refusal code:

| the shape | `--replica-at` | phase A | phase B | undeclared in the walk |
| --- | --- | --- | --- | --- |
| a `replicated_at_destination` row with **no** `edits:` (19 rows) | may name it, at any destination | byte-identical to the carve blob | byte-identical | admitted by identity with its non-empty carve blob |
| a `replicated_at_destination` row **declaring lines** (1 row: the conftest's `:25`) | may name it, at any destination | byte-identical — commit A places the copy | the diff against the carve blob touches ONLY the declared lines, else `arrival-undeclared-edit` naming them | its APPLIED bytes are no replica's, so it **refuses** `arrival-undeclared-file` — an edited replica must be declared |
| a **moved** row with `also_replicated_to:` (1 row: `session_fixtures.py`) | may name it **iff** the destination being verified is in that list and is not the row's own — else `arrival-unreadable` | byte-identical, and its `git_mode` is compared (a moved row declares one) | its own declared lines, exactly as at the destination it moves to | admitted by identity with its carve blob, at the listed destinations only |

**An UNAPPLIED declared edit on a replica does not refuse**, and that is
deliberate rather than an oversight: its diff touches no undeclared line, which
is the only question RULING OQ-1's sentence asks, and it is the same rule a
moved row's unapplied edit has always had. It is COUNTED — in
`declared_edits_unapplied`, beside the moved rows' — because a phase-B run in
which the conftest's depth line was applied and one in which it was not are
very different events wearing the same `OK`. **What refuses an unapplied
`REPO_ROOT = HERE.parent.parent` is the destination's own suite**, where a root
pointing outside the repository is hundreds of setup errors and not an opinion,
so read the `unapplied` figure before reading the leg as done.

**"Applied identically at every replica" is a bound on LINES.** One destination
is verified per run — that is what `--destination` means — so two legs that
edited the same declared line differently would BOTH pass here. The identity of
the applied text is the placing pull request's claim plus each leg's own
`validate`; the verifier's own docstring says so, and
`tests/carve_arrival/test_verify_carve_arrival.py::test_two_legs_may_apply_one_replicas_line_differently`
records the limit rather than leaving a reader to discover it.

Files CREATED at a destination (RULED OQ-C — `pyproject.toml`, `conftest.py`,
`pytest.ini`, openXdox-code's `openxfactory_surface.py`) have no row either,
and are named on the command line with `--allow-created`, once each, so that
every unplaced file at a destination is either admitted by a rule or written
down in the pull request that admits it.

**The scaffold's own files are admitted without `--allow-created`**, and the
distinction is load-bearing rather than convenience: `--allow-created` records
in the pull request that the destination ASSEMBLED the file, which is false of
anything the scaffold shipped before the carve began. The verifier reads each
leg's `tests/test_leg_shape.py` `REQUIRED_FILES` from the destination itself
(never a second copy here, and parsed rather than imported), admits any
`.gitkeep` by name, and carries one named document the lists cannot supply:
**`docs/branch-protection.md`**. That one matters because `docs/` IS a declared
root for `opendox_spec` — it receives `docs/ideation-dashboard-session-runbook.md`
— so before that admission a perfectly arrived openDox-spec leg refused
`arrival-undeclared-file` on the scaffold's own posture document. Measured
against the landed manifest, not reasoned about.

**A name is not a licence to carry content, and `--dest-base` is what makes the
name safe.** Every scaffold admission is by NAME, so the name alone would admit
whatever is written at it: `SECRET CARVE PAYLOAD` at
`docs/branch-protection.md` returned `OK`; a `.gitkeep` with content is
admitted anywhere under a root; and `REQUIRED_FILES` was read from the
destination's own WORKING TREE, so an arrival commit that added a path to its
own `tests/test_leg_shape.py` admitted that path — a check taking its allowlist
from the thing it is checking. All three were demonstrated on 2026-09-09. So
the allowlist is read from `--dest-base` (default `origin/main` where the
destination is a git repository carrying it) and every scaffold admission's
BYTES must equal the destination's own copy at that revision. Where there is no
baseline the run still passes, and BOTH the summary and the human line say
`scaffold admissions by NAME ONLY` — the weaker claim never passes for the
stronger one.

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

A **fresh MIRROR**, never the shared checkout and never a worktree of it: a
carve must read a tree nobody else is editing, and `git filter-repo` REFUSES a
clone that is not fresh. Measured against `git-filter-repo ed61b405`, the
installed one:

> Aborting: Refusing to destructively overwrite repo history since this does
> not look like a fresh clone. (expected at most one entry in the reflog for
> HEAD) … If you want to proceed anyway, use `--force`.

`git clone` followed by `git checkout "$CARVE_COMMIT"` leaves TWO HEAD reflog
entries and is exactly that case, so the carve stops before it starts — the
sequence an earlier draft of this section printed does not run. A `--mirror`
clone has no working tree to check out, leaves one reflog entry, and is the
shape filter-repo documents; it needs no `--force`. **`--force` is the
fallback and not the default**: the freshness check exists to stop a rewrite
landing in a repository somebody is working in, so it may be overridden only in
a throwaway clone made for this carve — a re-run in a clone already used — and
never in a checkout anyone else can reach.

```sh
CARVE_COMMIT=b075fd91dc8fced8e1373825ba80220c33536bae
DEST=opendox_code                       # one destination per pass
OXF=$PWD                                # the openxFactory checkout you stand in

git clone --mirror https://github.com/opensoft/openxFactory.git oxf-carve-src.git
```

**The control, before the carve.** Re-verify the manifest against the mirror at
the carve commit. Without this control a post-carve match proves the manifest
stale rather than the carve faithful.

**`--manifest` is NOT optional here, and leaving it off is a control that goes
green having checked nothing.** `validate-carve-manifest.py` defaults its
manifest to `<repo>/docs/opendox-carve-manifest.yaml` and holds a seat when
that path is not a file: it prints `NO MANIFEST … (nothing to validate)` and
exits **0**. A mirror has no working tree, and the manifest does not exist at
the carve commit in any case — it landed at `17167481`, AFTER `b075fd91` — so
the bare invocation selects that branch. Name the manifest in the checkout you
are standing in, absolutely:

```sh
python3 "$OXF/scripts/validate-carve-manifest.py" \
    --repo oxf-carve-src.git --at "$CARVE_COMMIT" \
    --manifest "$OXF/docs/opendox-carve-manifest.yaml"
# expect: OK … 456 row(s) … 318 digest(s) recomputed
```

### 5.3 The path file, generated FROM THE MANIFEST

The destination tree must be a function of the document, which is the whole
difference between this carve and the wallet's twelve hand-listed path sets.

**TWO LINES PER ROW, and the rename line alone is not enough.**
`--paths-from-file` reads a plain line as a path SELECTOR and a line containing
`==>` as a path RENAME. `git filter-repo -h` describes `==>` as a renaming
directive rather than a selector, and a file of rename directives renames what
it names and **keeps everything else**. Measured on a scratch repository of
three files with one listed: the rename-only file kept all three; the file
carrying the bare path beside the rename kept exactly one. Against openxFactory
that is the difference between publishing 123 files and publishing the
repository — `openspec/`, `contracts/`, `.github/` and every other path would
ride into a PUBLIC destination, and the arrival verifier would not catch them,
because its walk is scoped to that destination's declared roots. So emit BOTH:
the bare `source_path` to SELECT it, and the rename to PLACE it. **0 rows
change a basename**, so every rename here is a relocation.

```sh
python3 - "$DEST" "$OXF/docs/opendox-carve-manifest.yaml" > paths-$DEST.txt <<'PY'
import sys, yaml
dest = sys.argv[1]
doc = yaml.safe_load(open(sys.argv[2]))
for row in doc["rows"]:
    if row.get("destination") == dest:
        print(row["source_path"])                                   # SELECT
        print(f'{row["source_path"]}==>{row["destination_path"]}')  # PLACE
PY
wc -l paths-$DEST.txt        # 2 x 123 = 246 for opendox_code; see § 2's table
```

### 5.4 The carve, onto a NAMED ref

**`--refs` takes REFS, and a raw object id is not one.** `--refs
"$CARVE_COMMIT"` rewrites the history reachable from that commit into new
objects and then has no ref to update, so `refs/heads/main` keeps the
UNFILTERED tree and § 5.5's merge takes unfiltered history. Reproduced on a
scratch repository: after the run, `main` was byte-for-byte the source and **no
ref carried the rewrite at all**. Create a branch AT the carve commit and
rewrite THAT.

```sh
git -C oxf-carve-src.git branch carve-src "$CARVE_COMMIT"
git -C oxf-carve-src.git filter-repo \
    --paths-from-file ../paths-$DEST.txt --refs carve-src

# the control on the carve itself, before anything is fetched from it
git -C oxf-carve-src.git ls-tree -r --name-only carve-src | wc -l   # = the row count
```

`--refs` implies filter-repo's PARTIAL mode, and two of its consequences bite at
§ 5.5. The mirror's OTHER refs are left alone — `main`, every branch and every
backup ref a mirror carries, all still unfiltered — so the destination must
fetch ONE ref by refspec rather than `git fetch carved`. And **`origin` is NOT
removed**: an earlier draft of this section said filter-repo removes it when it
finishes, and that did not hold in any run made for this document; the claim is
withdrawn, and the mirror is disposable rather than de-fanged.

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
git remote add carved ../oxf-carve-src.git
# ONE REF, BY REFSPEC. The mirror still carries the unfiltered `main` and every
# other ref (§ 5.4), and a bare `git fetch carved` brings all of them within
# reach of a mistyped merge.
git fetch carved carve-src:refs/remotes/carved/carve-src
git merge --allow-unrelated-histories carved/carve-src \
    -m "Commit A — the openDox-code arrival at opendox-carve-0 (123 rows, byte-identical)"
```

Then, in openxFactory, with the destination checkout in hand. `--manifest` is
named for § 5.2's reason — `--source-repo` is a MIRROR and carries no working
tree, so the default `<source-repo>/docs/…` path is not a file — and unlike the
manifest validator this verifier is fail-closed about it and refuses
`arrival-unreadable` rather than holding a seat:

```sh
python3 scripts/verify-carve-arrival.py --destination opendox_code \
    --manifest "$OXF/docs/opendox-carve-manifest.yaml" \
    --dest-root ../dest-openDox-code --source-repo ../oxf-carve-src.git --phase A
# expect exit 0: 123 row(s) arrived … 123 digest(s) verified …
#                scaffold admissions checked against <origin/main>
```

`--dest-base` defaults to the destination's own `origin/main`, which after the
clone above is its PRE-CARVE main, and every SCAFFOLD admission's bytes are
checked against it. If the line says `scaffold admissions by NAME ONLY` the
destination had no such ref and the run made the weaker claim: name the
baseline explicitly (`--dest-base <sha>`) before reading the result as proof.

**Only then** apply the declared edits as commit B, and re-verify at phase B:

```sh
python3 scripts/verify-carve-arrival.py --destination opendox_code \
    --manifest "$OXF/docs/opendox-carve-manifest.yaml" \
    --dest-root ../dest-openDox-code --source-repo ../oxf-carve-src.git --phase B \
    --allow-created pytest.ini --allow-created conftest.py \
    --replica-at scripts/output_boundary.py=src/opendox/output_boundary.py \
    --replica-at scripts/path_slug.py=src/opendox/path_slug.py \
    --replica-at scripts/wire_messages.py=src/opendox/wire_messages.py
# expect exit 0: 62 edited row(s), declared-lines-only; 3 of 3 declared
# replica(s) verified (byte-identical, or — where the row declares lines —
# differing only on them)
```

The human line says `verified (byte-identical, or …)` and not
`byte-identical` since RULED Q-L7 (a), because one replica row now declares a
line and a copy that arrived carrying it is not byte-identical. **A leg that
places `tests/ideation-dashboard/conftest.py` declares it too** —
`--replica-at tests/ideation-dashboard/conftest.py=tests/conftest.py` — and at
phase B the run then reports it as a declared-edit row: `diffed` where the `:25`
depth line was applied, `unapplied` where it was not. Leg 1 (openDox-code #6,
merge `ce53b489`) landed BEFORE that grammar existed and is **not re-cut** for
it: openDox-code takes the depth fix in a later declared act, which is the
ruling's own sequencing.

**§ 5.2-5.5 PROVED END TO END, 2026-09-09**, against the landed manifest and a
fresh mirror: the `opendox_spec` leg's 112-line path file carved `carve-src`
down to exactly its **56** files under `contracts/`, `docs/` and `examples/`
and nothing else; the single-refspec fetch and the unrelated-histories merge
placed them on a scaffold branch; and phase A reported **56 row(s) arrived, 56
digest(s) verified, 57 file(s) … none undeclared (1 scaffold)**. The same three
steps run as this section printed them before this round produced, in order: a
refusal to start, a rewrite no ref pointed at, and a tree still holding all
5,404 files.

One `--replica-at` per replica this leg places, at the path it was placed —
every pure copy, and (since RULED Q-L7 (a)) every copy whose ROW declares the
lines it must differ on, which is the only way such a copy can be read as a
replica at all: its applied bytes match no blob at the carve commit, so
undeclared it refuses `arrival-undeclared-file`. The three neutral modules
above are permanent replicas (RULED OQ-A); `scripts/corpus_adapter.py` is a
replica now and is retired after the OQ-L pin lands (RULED OQ-Q, 2026-09-09
~22:3xZ), so it is declared while it is one.
**RULING Q-L1 (2026-09-10) added two more permanent replicas** —
`scripts/route_extension.py` and `scripts/subcommand_extension.py`, the § 2.4
extension-point seams — after carve leg 1 found them imported at module level by
arrived rows with no row of their own; both `-code` legs place them and declare
the placement the same way. **Place each ON the `src/` import root and BESIDE
the package** — `src/route_extension.py`, `src/subcommand_extension.py`, the
mirror of `scripts/*.py` beside `scripts/ideation_dashboard/` here — and never
inside `src/<pkg>/`: every importer is a bare top-level `import` on a line no
row declares, so a copy inside the package would need an import rewrite the
manifest does not authorize while a copy on the import root resolves unedited. Their arrival needs no import rewrite: every
importer spells a BARE top-level `import route_extension` /
`import subcommand_extension`, which is what the modules' own docstrings ask for.

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
* the `replicated_at_destination` copies — DECLARE each pure copy with
  `--replica-at <source_path>=<destination path>`, which makes its presence and
  its bytes checkable; leave `tests/corpus-adapter/test_conformance.py`
  undeclared, because its implementation-aware block is rewritten here by
  design, and name it with `--allow-created` once that rewrite has begun;
* **the two RULED Q-L7 (a) placements, which BOTH `-code` legs owe** —
  `--replica-at tests/ideation-dashboard/conftest.py=tests/conftest.py` (the
  replica whose row declares `:25`, so its copy must read
  `REPO_ROOT = HERE.parent`, and it is `arrival-undeclared-file` if placed
  edited and left undeclared) and, **at openXdox-code only**,
  `--replica-at tests/ideation-dashboard/session_fixtures.py=tests/session_fixtures.py`
  (the moved row `also_replicated_to: [openxdox_code]`, with the same four
  `ideation_dashboard.X` → `opendox.X` rewrites its `opendox_code` arrival
  takes — `opendox`, not `openxdox`, because openXdox pins openDox). Neither is
  an `--allow-created`: the carve ships both files, and `--allow-created` would
  record that the destination assembled them. At openDox-code the second is the
  row's own move and arrives as `tests/session_fixtures.py` with no flag at
  all;
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
# openDox's root HAS a destinations: key, because rows point at it
python3 scripts/verify-carve-arrival.py --destination opendox_root \
    --dest-root ../dest-openDox --source-repo . --phase A
# the carved_from check is this destination's whole job: it declares 0 rows

# openXdox's root has NO key — the manifest declares opendox_code, opendox_root,
# opendox_spec, openxdox_code, openxdox_spec and nothing else, because no row
# lands in openXdox's assembly root. It is addressed by the repository it is,
# so BOTH of RULED OQ-I's records are machine-checked rather than one of them:
python3 scripts/verify-carve-arrival.py --assembly-root opensoft/openXdox \
    --dest-root ../dest-openXdox --source-repo .
```

**Both roots, or the ruling is half kept.** RULED OQ-I puts `carved_from:` in
EACH assembly root. A manifest key exists only where rows land, so a
key-addressed check reaches openDox's record and not openXdox's; the
`--assembly-root` mode is why § 7's record is verified by running code rather
than read by eye.

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
commit and tree digest. **openXdox's own `carved_from:` record is verified with
`--assembly-root opensoft/openXdox`** (§ 6): its assembly root receives no row
and therefore has no `destinations:` key, so that is the only address the
verifier has for it. **The estate's submodule discipline applies unchanged**:
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
as written: the `replicated_at_destination` rows carry test functions that
exist at two or three destinations at once, so the post-split sum EXCEEDS the
pre-split count by design. (Re-measured 2026-09-10 against the amended
manifest: **20** such rows — 18 when RULING OQ-K was measured, plus RULING
Q-L1's two § 2.4 seams — of which **three** are test-bearing and carry the same
**30** `def test_` between them, so every figure in OQ-K's arithmetic stands
and only the row total moved. RULED Q-L7 (a)'s two amended rows are zero-test
and enter no term.) The floor is **a source→destination mapping plus a
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
