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

**AFTER PHASE 5 THE THIRD ONE INVERTS, and the manifest says so itself.** The
shed deletes 319 of the 456 rows' source paths by construction, so a
`carve`-phase manifest refuses every run from the shed commit onward. § 5.2
therefore flips `phase: post-shed` in the manifest **in the same commit as the
deletions**: a MOVED row and the one `deleted_at_carve` row are then EXPECTED
to be absent, and one that is STILL PRESENT refuses `carve-shed-incomplete`.
Nothing else moves — `carve_commit` stays `b075fd91`, `carve_tag` stays
`opendox-carve-0`, all 318 digests are still recomputed from the referent's
own bytes on every run, and every `stays_*` and `replicated_at_destination`
row is still required to be present. The declaration is symmetric in both
directions, which is what makes § 8's "no ordering of two commits leaves a
green intermediate" a thing this floor CHECKS rather than a thing the lane is
asked to remember. **`--at <carve_commit>` stops answering once the phase
flips** — at that revision every source path is present, which a post-shed
manifest refuses — so the second invocation below is the pre-shed one.

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
| `moved_verbatim` | **143** | the arrived blob's `sha256` and mode EQUAL the row's |
| `moved_with_declared_edit` | **175** | commit A byte-identical; commit B's diff against the carve blob touches ONLY that row's `edits[].lines` |
| `not_moved` | **138** | absent at every destination — except the **20** `replicated_at_destination` rows, which are present at the destination AND retained here; **one of them declares lines** (RULED Q-L7 (a) — one line at that ruling, two today) and its copies are held to them |

**318 rows move. 2621 declared edit lines**: `import rewrites` 726, `path
constants` 246, `adapter calls` 1649. **176 rows carry `edits:`** — the 175
`moved_with_declared_edit` rows and, since RULED Q-L7 (a), one replica row.
The § 3.4 slice-S5 annotation moved all four figures: +162 declared lines, and
`views/staging-workbench.js` converted `moved_verbatim` -> declared, which is
the one row that moves BOTH disposition counts and the carrier count at once.
The § 3.4 slice-S7 annotation moved them again and by the largest margin of
any act so far: **+782 declared lines over 33 `opendox_code` rows, 17 of them
converted `moved_verbatim` -> declared** — "parameterize class C" edits every
file in the served bundle, because every one of them rendered a word.
The § 3.4 slice-S8 annotation then moved ONE figure only: +40 `path constants`
lines over thirteen rows that were already carriers, so the row counts and the
carrier count stand where slice S7 left them.
The PRE-EXISTING `openxdox_code` annotation (`#656` CLAIM `5656688910`) then
added **+48 declared lines and moved nothing else**: the four rows it declares
— three moved rows and the conftest replica — ALL carried `edits:` already, so
neither disposition count nor the carrier count moves with it. It is not a
slice's annotation — and not the FIRST act on this document that is not one
either: § 2's dated history below records the earlier ASK-7 declared-edit
window (`#656` comment `5635150678`, PR #995). The two differ in what they
declare. ASK-7's four lines were RULED to be left and *"fixed at the next
declared-edit window"*, so they were owed to someone from the day of that
ruling; these were scheduled by no ruling at all — they landed at openXdox-code
BEFORE Q-L1's pairing became general (`#656` comment `5642758731`, 2026-09-12
02:07Z), which is why no slice ever owned them.
THE RETIREMENT ACT (RULED 5656343213, `#656` CLAIM `5656690570`) then added
**+167 declared lines and moved nothing else**: the ENDING REPLAY removed from
`tests/ideation-dashboard/test_staging_workbench.py` is declared on that row's
own `edits[]`, and that row has carried `edits:` since slice S5, so neither
disposition count nor the carrier count moves with it. The removed block spans
**177** carve lines; ten of them slice S5 already declared on this row, and a
line is declared once per row — the aggregate sums line ENTRIES — so this act's
entry carries the other 167 and the row declares 196 distinct lines. The two rows the same
act RETIRES move no figure here at all, because `retired:` touches no `edits[]`
and a retirement is a fact about a DESTINATION. **The per-destination table
below DOES move with it**: slice S7 made that table a measurement again and
pinned it cell by cell, so this act takes its own cell rather than registering
the table as stale, which is what an earlier draft of this paragraph did and
what S7's pin now forbids.
**AND THE TABLE ABOVE IS THE CARVE'S RECORD, NOT A LIST OF ARRIVAL
OBLIGATIONS** — a distinction this act is the first to make visible, because it
is the first whose rows owe the OPPOSITE of the proof written beside them. A
`disposition` says what the CARVE did with a file. Two of the **175**
`moved_with_declared_edit` rows are now RETIRED, and at their leg neither
half of that proof is owed: `rows_for()` drops a retired row before the
destination is asked anything, so no commit-A identity and no commit-B
declared-line diff is required of it, and what § 5.8 requires instead is that
`retired.at_path` be ABSENT — `arrival-not-retired`, whose remedy is the
deletion and not a diff. The row keeps its disposition, its digest and its
`edits[]`, which is the whole reason the ruling made a retirement a FIELD, so
the count above does not move. RULED Q6's **4** re-destined rows make the
milder version of the same point: their proof is owed at the leg
`re_destined.to` names and not at the one `destination:` still does. Read the
counts as the carve's ledger and the per-destination table below — with the two
subtractions its own paragraph states — as what each leg is actually asked for.

**AND A MOVED ROW MAY CARRY `re_destined:` (RULED Q6, Brett Heap, 2026-09-12,
`#656` comment `5648044785`).** Where a RULING has corrected the placement the
carve made, the row records it — `{from, from_path, to, to_path, ruling,
note}`, `to` held to the closed `destinations:` keys and the citation REQUIRED
— and **the proof owed at the destination moves with it**: the file must be
PRESENT at `to:to_path` under this same table's rules, and ABSENT at the
`from:from_path` it left (`arrival-not-vacated`). Nothing else moves —
`carve_commit`, `carve_tag`, every `sha256`, every disposition and every
declared line are claims about the SOURCE blob at the carve commit, and where
the file now lives says nothing about them. **FOUR ROWS CARRY IT TODAY**: §
3.4 slice S5 (`#656` CLAIM `5648073924`) is the first act to use the form,
RULED Q5 (`5648044785`) moving `gate.js`, `dispose.js`, `swb-create.js` and
`swb-session.js` from `opendox_code` to `openxdox_code`, and § 5.7 is the
general procedure this and any later re-destination follows.

**AND A MOVED ROW MAY CARRY `retired:` (RULED 5656343213, Brett Heap,
2026-09-13, `#656` comment `5656343213`, on the question slice S8's author put
in `#656` comment `5650335573` § 2).** Where a RULING has DELETED an arrival
the carve made — not moved it, as Q6 does, because the surface the arrived
file needed is at NO leg to move it to — the row records it: `{at, at_path,
ruling, surface, note}`, `at`/`at_path` held to the row's **EFFECTIVE**
arrival (so a row may be re-destined and THEN retired), `surface:` held to a
`not_moved` row of this manifest — under any reason but
`replicated_at_destination`, whose copies the legs place themselves — and the
citation REQUIRED. **The proof owed at the destination inverts**: the leg is
no longer asked for the file, and the file must be ABSENT at `at:at_path`
(`arrival-not-retired`). Be exact about what that leaves, because the two
tools answer differently (Copilot review of PR #1032): `rows_for()` drops a
retired row, so `verify-carve-arrival.py` does NOT digest it and does NOT diff
it at this leg — there is no file left here to digest or to diff. What goes on
unchanged is the SOURCE side, in `validate-carve-manifest.py`: `sha256`,
`git_mode`, `disposition` and `edits[]` stay untouched on the row, and check
3's two passes and check 4's surface walk ask of a retired row exactly what
they ask of any other moved row — a retirement is a fact about a DESTINATION,
and the row is still the record of a file that LEFT openxFactory. **TWO ROWS
CARRY IT TODAY**: the form landed ahead of its first use (PR #1032), exactly
as RULED Q6 did, and the first use is PR #1043 (`#656` CLAIM `5656690570`) —
`tests/ideation-dashboard/test_intent_tray_dom.py` and
`tests/ideation-dashboard/test_wheel_verbs_dom.py`, retired at `opendox_code`,
deleted there by opensoft/openDox-code#24. **The ruling's THIRD suite carries
no block**: only the ENDING REPLAY inside
`tests/ideation-dashboard/test_staging_workbench.py` goes, a PART of a file
whose other tests drive surfaces `openxdox_code` has, so that row goes on
arriving and the removal is an ORDINARY declared edit on its own `edits[]`
under `adapter calls` — the block SPANS **177** carve lines and the entry
declares **167** of them, slice S5 having already declared the other ten on
this row, which leaves the row declaring **196** distinct lines (the same three
figures the paragraph under the table states, and they are three questions, not
one); realized at opensoft/openXdox-code#20. § 5.8 is
the general procedure a retirement follows, and its "What the form CANNOT
express" is that third case, written from this act.

The table above states the file's CURRENT totals — see "Measured directly
against the landed manifest" below for how they are derived. What follows is
the file's history of amendments in landing order, starting with RULING Q-L1 on
2026-09-10 (`#656`, comment `5611834121`): the two § 2.4 extension-point seams
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
  row has carried** — `path constants`, line 25. A SECOND line joined it later,
  `:271` under `adapter calls`, when the pre-existing `openxdox_code`
  annotation declared openXdox-code#14's 27-line § 4.4 pytest fixture. **Each
  declared line is a PERMISSION at every replica of this file and an OBLIGATION
  at none** — `edits:` is a field of the ROW and a replica has no row of its
  own — so what the grammar bounds is the LINE, and which of them a given copy
  takes is that leg's own declared act: openXdox-code's takes both,
  openDox-code's takes `:25` alone (measured at `05bbde80`: 271 lines, the
  declared `:25` and nothing else). `REPO_ROOT = HERE.parent.parent` resolves
  outside the destination repository once the copy lands one directory
  shallower at `tests/conftest.py`, and must read `HERE.parent`; that one both
  `-code` legs owe, because both place the file at that depth — and where a
  line IS applied, its text is THAT PLACING LEG'S CLAIM and its own suite's,
  never an identity the grammar checks. What makes the two `-code` legs' `:25`
  the same text is the depth they share, the reason just given, and not a rule
  the floor enforces: two legs that applied one declared line DIFFERENTLY would
  both pass here all the same — § 5.5 says so, and
  `tests/carve_arrival/test_verify_carve_arrival.py::test_two_legs_may_apply_one_replicas_line_differently`
  records it — because `verify-carve-arrival.py` verifies one destination per
  run and compares no two legs' copies with each other.

The **two replica lines belong to no destination column below** — `:25` (the
1422nd declared line when this paragraph was written) and, since the
pre-existing `openxdox_code` annotation, `:271`: a replica row names no
destination at all, so the per-leg declared-line figures below exclude both and
sum to 2619 rather than 2621. **The two are owed differently, and a replica row
cannot say so**: `:25` is owed by every leg that places that conftest — both
`-code` legs — while `:271` is openXdox-code#14's § 4.4 fixture, PERMITTED at
every replica by the same row-wide grammar and owed at none. openXdox-code
takes it; openDox-code does not, and its arrival run answers `OK` all the same
(measured at `8efb3cf5`). **The PRE-EXISTING `openxdox_code` ANNOTATION moved
the per-destination cell it owed — that destination's declared-line figure,
703 -> 750 — and that was
a change of kind from how this paragraph was written** (Copilot review, round
twenty-six: the sentence said "this act", which in THIS pull request is the
retirement, whose own figures are the paragraph below's 167 and 750 -> 917):
when it was written, that table was stale, this paragraph registered it as
stale, and the redistribution was reserved for "one later act" because slices
S7 and S8 were in flight over the same cells. The
§ 3.4 slice-S7 annotation IS that act: it re-derived every cell and pinned all
five columns with
`tests/carve_arrival/test_verify_carve_arrival.py::test_the_runbook_per_destination_table_is_the_manifests_own_sum`.
So the cells are a MEASUREMENT again, a run can be compared against them once
the RULED Q6 four are read off the paragraph under the table, and an act that
moves the aggregate moves them with it — 47 of that annotation's 48 lines
fall on three `openxdox_code` rows, and the forty-eighth is the `:271` above,
which belongs to no column at all.
**THE RETIREMENT ACT MOVES ONE CELL AND NEITHER REPLICA LINE.** Its 167
declared lines all fall on a SINGLE `openxdox_code` row — the ending replay
inside `tests/ideation-dashboard/test_staging_workbench.py` — so the only cell
below that moves is that destination's, and `:25` and `:271` are untouched by
it: a retirement declares no line at all, and the one row this act DOES declare
names a destination, so the per-leg figures go on summing to two less than the
aggregate.
**Under every other `not_moved`
reason `edits:` is still a refusal**: RULING OQ-B's three
`stays_openxfactory_governance` rows stay here and take their import rewrite in
openxFactory, so they go on recording it in `evidence:`. And this is **not**
RULING OQ-K's owed FLOOR PART 2 field (§ 9): that one names REPOSITORIES on a
test-bearing replica row for the multiplicity sum, and both files here carry
zero `def test_` at the carve commit.

**Measured directly against the landed manifest, and CURRENT TO THE
RETIREMENT ACT of 2026-09-16** (rather than hand-chained through every
intervening amendment): the table and the two paragraphs above, and the
per-destination table below, state the totals as of THIS act — RULED
5656343213's retirement act (`#656` CLAIM `5656690570`), and behind it the
pre-existing `openxdox_code` row annotation (`#656` CLAIM `5656688910`), the § 3.4 slice-S8 annotation (RULED `#656`
comment `5656343213`) and the § 3.4 slice-S7 row annotation (RULED Q1/Q2/Q7,
`#656` comment `5648049748`; S7 CLAIM `#656` comment `5649148461`) — which is
the § 3.4 SLICE-S3 row annotation
(`#656` comment `5642758731`, openxFactory PR #1001) merged with every row
annotation since RULED Q-L7 (a) above —
among them BUILD slice 2's nine openDox-code back-imports, a second Q-L1
annotation round (`#656` comment `5628560136`), the ASK-7 declared-edit
window (`#656` comment `5635150678`, PR #995), the § 3.4 SLICE S2
intent-chips annotation (RULED Q5, `#656` comment `5642758731`, openxFactory
PR #1002, landing first per Q-L1's own landing order), PR #1001's own
post-landing extension catching up the openDox-code #14 fix round's one-line
`test_doc_surfaces.py` edit, and the § 3.4 SLICE S6 annotation (RULED Q4,
`#656` comment `5642758731`) declaring the `/source` re-homing's ten
`serve.py` lines and 122 matching `serve_projection.py` deletions, on the same
two rows' existing `edits:` and no new row, and the § 3.4 SLICE S4 annotation
(RULED Q3, `#656` comment `5642758731`) declaring the thirteen gate-route
constants it counts across the three RULED `SPLIT` files — twelve travel to
a new home or are removed, one (`ACTIONS_REFRESH_ROUTE`) stays in
`repo-selector.js` — over seven rows (two already carriers, five new) and
four admitted files, three of them class-B modules, the § 3.4 SLICE S5
annotation (RULED Q5/Q6, `#656` comment `5648044785`, openxFactory PR #1023
@ `ee251d6c`) — the first act to use the `re_destined:` form, +162 declared
lines, and the one `views/staging-workbench.js` conversion that moves both
disposition counts and the carrier count at once — and the § 3.4 SLICE S7
annotation THIS ACT CARRIES: +782 declared lines over 33 `opendox_code` rows,
17 of them converted `moved_verbatim` -> declared, and three admitted files.
The list is complete THROUGH SLICE S7, and deliberately stops there: the § 3.4
slice-S8 annotation, the pre-existing `openxdox_code` annotation and RULED
5656343213's RETIREMENT ACT have moved the aggregate since, and each is stated
ONCE, in the current-totals paragraph
above this history, which is where the aggregate is read. Two acts restating
one set of absolutes is how a count becomes wrong in a merge, and this history
is the hand-maintained copy that warning is about — so the paragraph dates the
figures at its own head rather than growing a second enumeration here.
Rather than
re-narrate each one here — this table is exactly the hand-maintained
copy RULED Q-L1's own "two acts restating one set of absolutes is how a
count becomes wrong in a merge" warns about — the figures above are the
same measurement
`scripts/validate-carve-manifest.py` prints and
`tests/carve_manifest/test_carve_manifest.py::test_the_real_manifest_carries_the_ruled_q_l7_amendment`
pins, computed the same way every time: a transcribed count is a claim, a
summed one is a measurement.

Per destination, counted at the `destination:` each row names — which is what
each leg's arrival run reports, save where RULED Q6 has re-destined rows or
RULED 5656343213 has retired them (below):

| destination | rows | verbatim / edited | declared edit lines | declared roots |
| --- | ---: | ---: | ---: | --- |
| `opendox_code` | 123 | 35 / 88 | 1667 | `src/opendox`, `tests` |
| `opendox_spec` | 56 | 55 / 1 | 26 | `contracts/schemas`, `docs`, `examples/ideation-dashboard` |
| `openxdox_code` | 92 | 9 / 83 | 917 | `scripts`, `src/openxdox`, `tests` |
| `openxdox_spec` | 47 | 44 / 3 | 9 | `contracts/schemas`, `examples/ideation-dashboard` |
| `opendox_root` | 0 | — | — | none — the release identity only (§ 3.8) |

The numeric columns are summed over the rows whose `destination:` names that
leg, re-derived here rather than carried forward. TWO ROWS OF IT WERE STALE
and both are corrected in the same act, because the correction IS the
measurement: the table was last current at `880c821c`, where `opendox_code`
read `53 / 70 | 727` and `openxdox_code` read `9 / 83 | 659`; the § 3.4
slice-S5 annotation (`ee251d6c`) moved BOTH — to `52 / 71 | 874` and
`9 / 83 | 674` — and moved neither cell. The slice-S7 annotation moves
`opendox_code` again, to `35 / 88 | 1656`, and leaves `openxdox_code` where S5
put it. The slice-S8 annotation then moves BOTH declared-line cells and
NEITHER `verbatim / edited` cell: its forty `path constants` lines fall
11 at `opendox_code` and 29 at `openxdox_code`, every one of them on a row
that already carried `edits:`, giving the `1667` this table still carries and
the `703` it carried until the act below. The pre-existing `openxdox_code`
annotation then moves
`openxdox_code`'s declared-line cell ALONE, to `750`: 47 of its 48 lines fall
on three rows this leg already edits, and the forty-eighth is a second line on
the conftest REPLICA row, which names no destination and belongs in no column.
THE RETIREMENT ACT then moves that same cell ALONE again, from `750` to `917`:
every one of its declared lines falls on ONE `openxdox_code` row — the ending replay
inside `tests/ideation-dashboard/test_staging_workbench.py` — and the two rows the
same act RETIRES move no cell at all, because a retirement declares no line: it is
a fact about a DESTINATION, and the rows go on naming theirs.
The four destination figures now sum to 2619, and the TWO lines the replica row
`tests/ideation-dashboard/conftest.py` declares — which name no destination at
all — make 2621.
`tests/carve_arrival/test_verify_carve_arrival.py::test_the_runbook_per_destination_table_is_the_manifests_own_sum`
asserts all four numeric columns, the fifth ROOTS column and that sum against
the landed manifest, so every cell of this table is now read FROM THE TABLE;
until the slice-S7 annotation nothing checked the numbers, which is how two
cells sat wrong through two acts. THE ROOTS COLUMN HAD ONLY LOOKED CHECKED:
`test_the_real_manifest_declares_the_roots_the_runbook_names` holds the
manifest to a list hard-coded in the test and never opens this file, so a roots
cell gone stale or gone unbackticked passed it. It stays where it is — two pins
on one fact, one either side of the runbook — and the roots cell is now
compared with `declared_roots(rows_for(...))`, the walk each leg's arrival run
actually performs.

A row RE-DESTINED by ruling still counts at the `destination:` it declares, and
so does a row a ruling RETIRED, so this table and a leg's arrival run count
different sets — **by two subtractions now, not one**. RULED Q6 moved four rows
off `opendox_code` and onto `openxdox_code`; RULED 5656343213 RETIRED two more of
`opendox_code`'s, and a retired row is owed at no leg at all. In ARRIVED ROWS,
the first figure a run prints, `opendox_code` reports SIX FEWER than this table's
count, 117 against 123, and `openxdox_code` FOUR MORE, 96 against 92: one ruling
moved the placement and the other deleted it, and neither moved the row. All six
carry `edits:`, so they take the `verbatim / edited` split with them — the four
re-destined ones carrying their declared lines to the other leg and the two
retired ones taking theirs out of every leg's reckoning while the row goes on
recording them — and the EFFECTIVE edited counts are 82 and 87 against this
table's 88 and 83. What a run PRINTS as `declared-edit row(s) within their
lines` is a THIRD count again — the rows that arrived CARRYING the edit, so the
`unapplied` rows and the declared replicas each move it — and § 5.5 is where
that line is read, against the phase-B example's own four figures.

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

Its seven findings and one environment code:

| code | what it refuses |
| --- | --- |
| `arrival-missing` | a row for this destination has no file at its EFFECTIVE `destination_path` — `re_destined.to_path` where a ruling has moved the placement (RULED Q6), else the row's own |
| `arrival-digest-mismatch` | the arrived bytes or mode are not the row's (phase A for every moved row; both phases for `moved_verbatim`) |
| `arrival-undeclared-edit` | phase B: the arrived blob differs from the carve blob on a line no `edits[].lines` declares — **the refusal names the lines** |
| `arrival-not-vacated` | `arrival-missing` read in the mirror, and the LOSING half of RULED Q6: a row re-destined AWAY from this destination still has a file (or a symlink — the test is `lexists`) at the `re_destined.from_path` it left. A re-destination is one act with two halves, and a copy kept here is the same bytes at two legs with the floor standing behind one |
| `arrival-not-retired` | `arrival-missing` read in the mirror again, for RULED 5656343213: a row whose `retired:` block says a RULING DELETED its arrival at THIS destination still has a file (or a symlink — the test is `lexists` here too) at `retired.at_path`. The difference from `arrival-not-vacated` is where the bytes went — a re-destination moves them to another leg and a retirement moves them nowhere — and they are two codes because the remedies differ: one deletion completes a move, the other completes a removal |
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
`grep -n`'s, and the one the manifest's declared lines have been written in
from the start — 794 of them at this ruling's own landing, 2621 now.
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
| a `replicated_at_destination` row **declaring lines** (1 row: the conftest's `:25` and `:271`) | may name it, at any destination | byte-identical — commit A places the copy | the diff against the carve blob touches ONLY the declared lines, else `arrival-undeclared-edit` naming them | its APPLIED bytes are no replica's, so it **refuses** `arrival-undeclared-file` — an edited replica must be declared |
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
and are admitted so that every unplaced file at a destination is either
admitted by a rule or written down as an admission somewhere reviewable.

**The GOVERNED form of that admission (RULED — the arrival-admission repair,
Brett Heap, 2026-09-11, `#656` comment 5639058687) is a `created:` entry in
the destination's own block of `docs/opendox-carve-admissions.yaml`**, read
automatically by `scripts/verify-carve-arrival.py` (the default path, beside
this manifest; `--admissions` overrides it) and applied exactly as
`--allow-created` admits. A NEW admission is then a reviewed ONE-LINE diff in
the pull request that bumps the destination's pin:

```diff
       openxdox_code:
         created:
+          - path: src/openxdox/new_module.py
+            reason: "added by opensoft/openXdox-code#N"
+            since: "<the leg commit that introduced it, 40 hex>"
```

`--allow-created <path>` on the command line still works, for an ad-hoc run
over a tree with no admissions file yet, and the verifier prints a one-line
notice that the declared form is the governed one. § 5.6 below is the
historical, hand-typed list this file replaces as the source of truth for
what each `-code` leg has admitted; read
`docs/opendox-carve-admissions.yaml` itself for the CURRENT state.

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

### 2.2 FLOOR PART 3 — the conformance runner

FLOOR PART 1 is a claim about BYTES and § 2.1 is what proves it. **FLOOR
PART 3 is a claim about a READER** — design § D6 (3), "A NEUTRAL CONFORMANCE
CORPUS EVERY DESTINATION PASSES ... a corpus with no `openspec/`, no
`contracts/`, no lifecycle headers" — and the ruling's word is EVERY:
`tasks.md` § 3.7 names three destinations, openDox, openXdox's adapter
implementation, and **openxFactory's own adapter from § 2.2a**, that last one
being "the only mechanical proof that the home corpus has no privileged
route".

**The corpus's DOCUMENTS already existed and do not move.** RULED OQ-3
(2026-09-06) seeded them beside the § 2.2a suite —
`tests/corpus-adapter/fixtures/`: three documents in two roots of their own
(`notes/`, `papers/`) under a two-field header vocabulary (`Type:`, `Title:`)
belonging to no governed repository, one of them classifying completely, one
missing a field its kind obliges and one carrying no kind at all; plus an
`empty/` sibling and a `not-a-directory` file. Eleven manifest rows name those
exact paths `not_moved / replicated_at_destination`, so the corpus is NOT
relocated and no second copy is authored: a floor with two corpora cannot
answer "every destination passes IT".

**What § 3.7 adds is the way to put a reader openxFactory did not author
through them**, because the seed runs under `pytest` against a factory named
in the file — one reader, in one checkout, chosen at author time. Two files:

* `scripts/carve_conformance.py` — the corpus as a closed set of **17 checks**,
  10 positives and 7 negative confirmations, over any reader. Standard library
  plus `corpus_adapter` and nothing else, and no home vocabulary anywhere in
  its source text: the same scan the interface itself is held to, because
  every destination runs this module and two of them hold nothing else of
  openxFactory's. A destination that would rather run the checks inside its
  own suite imports THIS and never the runner.
* `scripts/verify-carve-conformance.py` — the operator's way in, in § 2.1's
  idiom: exit 0 or 2 and nothing else, named refusal codes with a remediation
  trailer, a `--json` seat, and the same seat-holding pass (no
  `--destination` prints `NO DESTINATION` and exits 0). **It lives in
  openxFactory and is never copied into six repositories**, for § 2.1's
  reason.

```sh
python3 scripts/verify-carve-conformance.py \
    --destination openxfactory \
    --dest-root   .            \
    --adapter     home_factory:neutral_reader \
    --sys-path    tests/carve_conformance
```

**`--destination` takes a manifest key, plus `openxfactory`** — § 3.7's third
destination, which the manifest gives no key because it RECEIVES no row and
retains its own reader instead. That is the escape § 2.1 cuts for an assembly
root, for the same reason: the document is a map of where rows GO.

**THE READER IS DECLARED, NEVER DISCOVERED**, on `--allow-created`'s and
`--replica-at`'s reasoning — the operator names it and the pull request
records what was run. `--adapter <module>:<factory>`, where a factory is a
callable of `(name, location)` returning a reader pointed at it; four
locations get pointed at because three of the negative confirmations are about
what happens at RESOLUTION time. A convention this runner went looking for
instead would be openxFactory deciding how another repository lays its reader
out, which is `corpus-adapter-seam` requirement 4's privileged route wearing a
helpful face — and it could not be satisfied by a destination not yet written.
openxFactory's own declaration is `tests/carve_conformance/home_factory.py`,
nine lines, and it is the worked example a destination copies.

Its five refusal codes:

| code | what it refuses |
| --- | --- |
| `conformance-adapter-undeclared` | no `--adapter`: FLOOR PART 3 is a claim about a reader, and a run with none named has nothing to put through the corpus. **Silence must never read as a pass** |
| `conformance-adapter-unresolvable` | the module or the factory cannot be imported, is not `<module>:<factory>`, or is not callable — the refusal names the import roots searched |
| `conformance-corpus-missing` | the corpus is absent or PARTIAL, refused before any reader is blamed: a run over three of the four states would report checks that were never put |
| `conformance-check-failed` | one or more of the 17 did not pass — **the refusal names each one and what came back** |
| `conformance-unreadable` | the environment, an unknown `--destination`, a `--dest-root` that is not a directory; also the CATCH-ALL holding the exit contract, so any unnamed exception arrives as this code and exit 2 rather than as a traceback and exit 1 |

**Remediation is FIXED IN ONE DIRECTION: fix the reader, never the corpus.** A
corpus edited to match a reader that answered wrong is FLOOR PART 3 deleted,
because the ruling's word is that every destination passes THE SAME corpus.
Where a destination has authored no reader at all, that is that destination's
build task and not a finding against the corpus.

**Measured 2026-09-10 at each destination's then-current main**, and this is
the state of part 3 rather than a worked example:

| destination | main | verdict |
| --- | --- | --- |
| `openxfactory` (§ 2.2a) | this branch | **OK — 17 of 17** |
| `opendox_code` | `8e9ffa62` | `conformance-adapter-undeclared` — it holds the INTERFACE replica at `src/opendox/corpus_adapter.py`, byte-identical to the carve blob, and no implementation of it |
| `openxdox_code` | `59600412` | `conformance-adapter-undeclared` — the corpus-adapter non-placement leg 3 recorded and its verifier confirmed |
| `opendox_spec` | `41d570e9` | `conformance-adapter-undeclared` — a documentation leg, no Python |
| `openxdox_spec` | `03eacc61` | `conformance-adapter-undeclared` — a documentation leg, no Python |

**So FLOOR PART 3 is NOT green, and § 3.7 is not ticked.** One of its three
destinations passes; the other two have authored no reader for the corpus to
be run against — openDox's is `tasks.md` § 3.6's "trivial conformant adapter
implementation" and openXdox's is the § 4 mapping core's. The runner is what
makes that a MEASURED statement with a date on it instead of a reading, and it
is what those two build tasks report against when they land. § 3.8's tag waits
on all four parts.

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
that is the difference between publishing the 117 files this leg's path file
names and publishing the repository — `openspec/`, `contracts/`, `.github/`
and every other path would ride into a PUBLIC destination, and the arrival
verifier would not catch them, because its walk is scoped to that
destination's declared roots. So emit BOTH:
the bare `source_path` to SELECT it, and the rename to PLACE it. **0 rows
change a basename**, so every rename here is a relocation.

**AND BY THE EFFECTIVE, NOT-RETIRED ARRIVAL — `destination:` ALONE IS NOT
THE KEY** (Copilot review, round twenty-five on PR #1043). A RULED
re-destination (§ 5.7) and a RULED retirement (§ 5.8) both leave
`destination:` and `destination_path:` exactly as the carve wrote them —
they are the record of what MOVED, which is what § 2's table counts and what
every digest is keyed by — so a file keyed on that field alone states the
CARVE's placement and not today's. Measured on the landed manifest: at
`opendox_code` that key emits 123 rows / 246 lines where the leg is owed
117 / 234, the four rows RULED Q6 re-destined away and the two RULED
5656343213 retired among them, and commit A below would place all six for
the phase-A run to refuse before it can print the line § 5.5 promises. **ONE
refusal per run**: both checks raise on the first row they find, so the six
leftovers cost six runs — `arrival-not-vacated` while any re-destined file
stands (§ 5.7's order: the losing half is asked first), then
`arrival-not-retired` for each retired one. The other half fails SILENTLY:
`openxdox_code` reads 92 where `rows_for()` requires 96, so the four files
that ruling sent there would be missing from the carve ref that is supposed
to place them. The generator therefore asks the question the verifier asks —
`verify-carve-arrival.py`'s own `rows_for()`, spelled out because a heredoc
cannot import a hyphenated script — and the two `-spec` legs, which no
ruling has touched, are unchanged at 56 and 47.

**And it resolves the KEY rather than comparing it** (Copilot review, round
twenty-six). A `destinations:` key is a LABEL and never a referent —
`check_shape` deliberately admits two keys sharing one `{repository, leg}`
body — so `$DEST` given as the other spelling of a leg would match no row at
all and emit an EMPTY path file, while the verifier, which resolves both to
one identity, goes on expecting every row. That is the label-comparison
defect RULED Q-L8 (c) repaired in the tools and `#1032`'s round 9 found in
the last selector still making it; this generator was making it too. The
RETIREMENT half below still compares labels, deliberately and like
`retired_arrival()`: the block names the placement ITS OWN ROW makes, and
`validate-carve-manifest.py`'s check 6 is where a block naming another one is
refused. `test_the_runbook_path_file_generator_is_the_verifiers_own_predicate`
RUNS this program on the landed manifest for every destination — and on a
generated document carrying an ALIAS, because the landed one carries none —
and compares its lines with that predicate, because a generator and a
verifier that disagree about which rows a leg is owed cannot be caught by
reading either alone.

**The two `-code` legs were carved BEFORE both rulings**, which is why their
real history carries those six removals as later commits — § 5.7 step 4's
LOSING half and § 5.8 step 4 — rather than as an arrival that never placed
them. A leg carved today never places them and has nothing there to delete.

```sh
python3 - "$DEST" "$OXF/docs/opendox-carve-manifest.yaml" > paths-$DEST.txt <<'PY'
import sys, yaml
dest = sys.argv[1]
doc = yaml.safe_load(open(sys.argv[2]))
def resolved(key):                                       # a KEY is a LABEL:
    body = (doc.get("destinations") or {}).get(key)      # two of them may
    if isinstance(body, dict):                           # share one body
        return (body.get("repository"), body.get("leg"))
    return (key,)                                        # unknown: itself
here = resolved(dest)
for row in doc["rows"]:
    moved = row.get("re_destined") or {}                 # RULED Q6, § 5.7
    if moved.get("to") and moved.get("to_path"):
        at, at_path = moved["to"], moved["to_path"]
    else:
        at, at_path = row.get("destination"), row.get("destination_path")
    if resolved(at) != here:                             # not this leg's today
        continue
    gone = row.get("retired") or {}                      # RULED 5656343213
    if (gone.get("at"), gone.get("at_path")) == (at, at_path):
        continue                                         # deleted, never placed
    print(row["source_path"])                            # SELECT
    print(f'{row["source_path"]}==>{at_path}')           # PLACE
PY
wc -l paths-$DEST.txt        # 2 x 117 = 234 for opendox_code today
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
git -C oxf-carve-src.git ls-tree -r --name-only carve-src | wc -l   # = § 5.3's row count
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

* **Commit A** places every EFFECTIVE, NOT-RETIRED arrival's blob
  byte-identical to `carve_commit` — exactly the set § 5.3's path file selects
  — so the arrival verifier can prove **every moved row of that destination
  NOT RETIRED BY RULING at phase A**: the strongest statement available, and
  the analogue of the wallet's *"100/100 at the carve layer"*. **The
  qualification is RULED 5656343213's** (Copilot review, round twenty-seven),
  and it is the same one `rows_for()`, the verifier's module docstring and
  `--phase`'s own `--help` now carry: a row retired at its own effective
  arrival is dropped before either phase asks anything, so it is not placed,
  not digested and not diffed, and what is required of it instead is that its
  path be ABSENT (§ 5.8). An unqualified "every row" here and a 117-row
  expectation below are two incompatible placement contracts in one section.
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
    -m "Commit A — the openDox-code arrival at opendox-carve-0 (117 rows, byte-identical)"
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
# expect exit 0: 117 row(s) arrived … 117 digest(s) verified …
#                scaffold admissions checked against <origin/main>
```

**Those two figures are this leg's EFFECTIVE arrival and not § 2's row count
for it** (Copilot review, round ten on PR #1030). § 2's table counts a
re-destined row at the `destination:` it still names, and it counts a RETIRED
row there too; RULED Q6 moved four of `opendox_code`'s 123 rows AWAY and RULED
5656343213 RETIRED two more; and a run reports what it PLACES — 117, the four
fewer § 2's own paragraph names and the two this act retires. Both subtractions
are the same point: § 2 records what the CARVE moved, a run reports what this
leg PLACES, and every ruling that re-aims or retires an arrival widens the gap. At phase A every arrived row is
digest-checked, so the two numbers are one number twice.
`test_the_runbook_phase_examples_are_the_arrival_the_manifest_produces`
re-derives both of § 5.5's expected lines from the landed manifest and
composes them with the verifier's OWN summary line, elision by elision: these
two comments were written when the runbook landed (`a970fd9d`) and never
touched again, so they aged through every annotation act that moved the
figures — the § 2 table's defect exactly, one section down, and the phase-B
line below had drifted from the tool's wording as well as its numbers.

**AND NO `--replica-at` AT PHASE A** (Copilot review, round eleven on PR
#1030, reading § 5.6's "both `-code` legs owe" against this block). The copies
are what COMMIT B places — § 5.6 is titled for it — so a phase-A run that
declared one would refuse `arrival-missing` on a lawful tree. Measured in this
leg's own history: `tests/conftest.py` and the three neutral-module copies the
phase-B block declares are absent at commit A (`8e8983d`, the re-cut merged as
`ce53b489`) and all four first appear at commit B (`749c926`). A replica is
declarable exactly once it has been PLACED, which is the phase below.

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
    --replica-at scripts/wire_messages.py=src/opendox/wire_messages.py \
    --replica-at tests/ideation-dashboard/conftest.py=tests/conftest.py
# expect exit 0: 117 row(s) arrived, 35 digest(s) verified, 83 declared-edit
# row(s) within their lines, 0 unapplied; 4 of 4 declared replica(s) verified
# (byte-identical, or — where the row declares lines — differing only on them)
```

The old comment here read `62 edited row(s), declared-lines-only`, which is
not a phrase this verifier prints — neither script carries the words “edited
row(s)” or “declared-lines-only” at all. A quotation of a tool's output that
the tool would not produce cannot be compared with a run, which is why the
test composes these lines through `_print_ok` rather than matching them
against a literal of its own. `0 unapplied` is not a manifest figure: it is
the standard for a COMPLETE commit B — a declared-edit row the run finds
byte-identical to the carve blob is an edit this leg did not apply, and the
leg is not done until that count is zero. **The `83` is `82` moved rows plus the Q-L7 replica the fourth `--replica-at`
declares**: a replica whose ROW declares lines is answered exactly as a moved
row is and is counted with the moved rows' edits at phase B (`check_replicas`
-> `counts["diffed"]`), which is why this figure is ONE ABOVE the EFFECTIVE
edited count for this leg — not above the `verbatim / edited` column § 2's
per-destination table states, which counts at the `destination:` each row names
and is six rows higher. It read `85` = `84` + 1 until RULED 5656343213 retired
two of this leg's edited rows; the replica's own contribution is unchanged and
always was.

**BOTH FIGURES ARE THE COMPLETE COMMIT B's, AND A RUN AT AN UNFINISHED LEG
PRINTS NEITHER** — which the `0 unapplied` sentence above says of itself and
the `83` did not (Copilot review, PR #1043). Measured by running the command
above verbatim against openDox-code#24 at `e2d5ac46`, the head that carries
this act's deletion: `117 row(s) arrived, 35 digest(s) verified, 82
declared-edit row(s) within their lines, 1 unapplied; 4 of 4 declared
replica(s) verified`. That is this leg ONE EDIT SHORT OF DONE, and the
arithmetic is the same arithmetic: of the `82` effective edited rows ONE is
byte-identical to its carve blob, so it counts as `unapplied` and not as
`diffed`, leaving 81; the line-declaring replica DOES differ, on its own
declared `path constants` line 25, and is counted with the moved rows. `81 + 1
= 82` today; `82 + 1 = 83` the day that last edit lands. **An operator reads
the gap as the leg's REMAINING WORK**, which is what `0 unapplied` is for —
and the pin composes this line from the MANIFEST, holding no destination
checkout, so it cannot see a leg's progress and deliberately does not try: a
floor's documentation must not move every time a leg commits.

A replica left `unapplied` is the one lawful way that count is not zero, and it
is not this leg's state — see the replica paragraph below.

**This `--allow-created pytest.ini --allow-created conftest.py` is the ad-hoc
form on purpose, not a stale example** (Copilot review, PR #979; its PREMISE
re-measured on Copilot's round-ten review of PR #1030). What keeps the flag
correct is not that `opendox_code` declares no admissions — this note said
its block in `docs/opendox-carve-admissions.yaml` was `created: []` long after
BUILD slice 2 began filling it, and THIS act adds three more entries to it —
but that neither `pytest.ini` nor `conftest.py` is among the paths it
declares. Those two Phase-1 files still have no reviewed declaration to read,
so the command-line flag remains this leg's live, correct admission, exactly
as § 5.6 and the admissions file's own header say `--allow-created` still
does for a path nothing declares. It is not an operator falling back to a
form the file has already replaced here; it becomes one once a future PR adds
`pytest.ini` and `conftest.py` to `opendox_code`'s `created:` list, at which
point this example should drop the flag and this note should go with it — and
the same test reads both of these flags against the landed admissions file,
so that day is a FAILURE here rather than a sentence nobody re-reads.

The human line says `verified (byte-identical, or …)` and not
`byte-identical` since RULED Q-L7 (a), because one replica row now declares
lines and a copy that arrived carrying them is not byte-identical. **A leg that
places `tests/ideation-dashboard/conftest.py` declares it too** —
`--replica-at tests/ideation-dashboard/conftest.py=tests/conftest.py` — and at
phase B the run then reports it as a declared-edit row. **That row declares TWO
lines** — `:25`, the depth constant, and, since the pre-existing
`openxdox_code` annotation, `:271`, openXdox-code#14's § 4.4 fixture — and the
verifier asks ONE question of the pair: `diffed` where the copy differs from
the carve blob AT ALL, and then every line it differs on must be one of the
two, else `arrival-undeclared-edit` naming the rest; `unapplied` where the copy
is BYTE-IDENTICAL with the carve blob. That is the whole of what the count can
see — `check_replicas` compares the arrived bytes and nothing else, so a
declared line never applied and one applied and later reverted are the same
event to it, and neither is a refusal. **A declared line is a
permission and never an obligation**, so a leg that takes one and not the other
is `diffed` and lawful: openDox-code's copy takes `:25` alone — measured at
`05bbde80` and unchanged at `8efb3cf5`, 271 lines and that one hunk — and
openXdox-code's takes both. Leg 1 (openDox-code #6, merge `ce53b489`) landed
BEFORE that grammar existed and was **not re-cut** for it — **and the later
declared act that ruling sequenced HAS SINCE HAPPENED**: openDox-code
`3954d78` (#19, 2026-09-12) took the depth fix on the row's own `:25` and
nothing else, leaving `ce53b489`'s `HERE.parent.parent` where it stood. So the
flag is no longer optional at this leg and § 5.5's example above declares it
(Copilot review, round eleven on PR #1030). MEASURED with the example's own
other flags against openDox-code at `c7a216c7`: WITHOUT it the run refuses
`arrival-undeclared-file` at `tests/conftest.py` — "its bytes are no replica's
at the carve commit", the applied `:25` line being exactly why the
byte-identity admission can no longer see it — and WITH it the run answers `OK
… 4 of 4 declared replica(s) verified`.

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

Files CREATED at a destination get no row (RULED OQ-C). **As of RULED #656
(2026-09-11, `#656` comment 5639058687) the admission of record is
`docs/opendox-carve-admissions.yaml`'s `created:` list for the destination —
read automatically by `scripts/verify-carve-arrival.py`, applied exactly as
`--allow-created` admits, and updated by a one-line diff in the pull request
that bumps the destination's pin.** `--allow-created` on the command line
remains for an ad-hoc run over a tree with no admissions file yet. The
categories below are what a "created" file typically IS at each leg, kept for
that context; for the CURRENT admitted set at each destination, read the
admissions file itself rather than this list — a leg's own PR after this one
lands is not obliged to update this prose, only the declared file.

* both `-code` legs: `pytest.ini` (the rootdir anchor) and a root `conftest.py`
  — **unless Phase 1 already landed them, which is where they belong**;
* the `replicated_at_destination` copies — DECLARE each pure copy with
  `--replica-at <source_path>=<destination path>`, which makes its presence and
  its bytes checkable; leave `tests/corpus-adapter/test_conformance.py`
  undeclared, because its implementation-aware block is rewritten here by
  design, and name it with `--allow-created` once that rewrite has begun;
* **the two RULED Q-L7 (a) placements — the conftest one BOTH `-code` legs
  owe, the `session_fixtures` one openXdox-code's ALONE** —
  `--replica-at tests/ideation-dashboard/conftest.py=tests/conftest.py` (the
  replica whose row declares `:25` — so its copy must read
  `REPO_ROOT = HERE.parent`, which openDox-code took at `3954d78`, #19 — and,
  since the pre-existing `openxdox_code` annotation, `:271`, which is
  openXdox-code#14's § 4.4 fixture and is a PERMISSION at every replica rather
  than an obligation at any; it is `arrival-undeclared-file` if placed edited
  and left undeclared) and, **at openXdox-code only**,
  `--replica-at tests/ideation-dashboard/session_fixtures.py=tests/session_fixtures.py`
  (the moved row `also_replicated_to: [openxdox_code]`, with the same four
  `ideation_dashboard.X` → `opendox.X` rewrites its `opendox_code` arrival
  takes — `opendox`, not `openxdox`, because openXdox pins openDox). Neither is
  an `--allow-created`: the carve ships both files, and `--allow-created` would
  record that the destination assembled them. At openDox-code the second is the
  row's own move and arrives as `tests/session_fixtures.py` with no flag at
  all — and passing it there is not merely redundant but REFUSED, measured:
  `arrival-unreadable`, *"--replica-at names
  'tests/ideation-dashboard/session_fixtures.py', which at destination
  'opendox_code' is neither a not_moved / replicated_at_destination row of this
  manifest nor a moved row whose also_replicated_to: lists this destination"* —
  because a flag that could name a moved row at its own destination would let a
  caller re-point an arrival the manifest already declared;
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

### 5.7 A RULED re-destination — the `re_destined:` act

**RULED Q6** (Brett Heap, 2026-09-12, by interactive multi-choice; `#656`
comment `5648044785`, adopting the RECOMMENDED answer of openDox-spec
`docs/front-end-package-boundary.md` § 6 Q6 at `7d12428c`). A row's placement
may turn out to be wrong — RULED OQ-G's TEST HOMES rule placed 70 files at
openXdox by a rule about imports, and § 1.2(d) of that note measured that 23 of
them landed where nothing can run them. **Correcting a ruled placement is
DECLARED, never re-cut** (§ 11 is for a SOURCE-side fact, and a `post-shed`
manifest re-emitted at a post-shed commit would carry no moved rows at all).
This is the procedure; § 3.4 slice S5 (`#656` CLAIM `5648073924`) is the act
that first ran it, moving `gate.js`, `dispose.js`, `swb-create.js` and
`swb-session.js` from `opendox_code` to `openxdox_code` under RULED Q5
(`5648044785`) — a later slice, S8 among them, follows the same five steps
below.

**It is not a way to move a file for convenience.** The `ruling:` field is
required and is validated PRESENT for exactly that reason: a re-destination
with no ruling behind it refuses `carve-re-destined-unruled`, and there is no
second form. Amend, never chain: a row already re-destined is amended IN PLACE
to name where the file actually ends, citing the later ruling
(`carve-re-destined-chain`).

1. **The ruling first.** Brett Heap's word, on `#656` or on the pull request
   that asks for it, naming the rows and the destination. Record the comment id
   — it is what every row below cites.
2. **ONE openxFactory row-amendment pull request, and it lands FIRST** — the
   pairing § 5 requires of every slice. On each affected row add:

   ```yaml
       re_destined:
         from: openxdox_code                     # the row's own `destination`
         from_path: tests/test_x.py              # its own `destination_path`
         to: opendox_code
         to_path: tests/test_x.py
         ruling: "`#656` comment 5648044785"
         note: "RULED Q6 — the census says this bundle file's tests belong at
           the leg that owns it (§ 1.2(d))."
   ```

   **Edit nothing else.** `destination:` and `destination_path:` stay as the
   carve made them — they are the record of what happened and the path the
   losing leg must vacate — and `disposition`, `sha256`, `git_mode`,
   `edits[]`, `carve_commit` and `carve_tag` are untouched. An import rewrite
   the new leg needs is an ORDINARY declared line under `import rewrites`, on
   this same row, taken in the same window.
3. **Verify the document**: `python3 scripts/validate-carve-manifest.py` must
   print `OK` and end `; N row(s) RE-DESTINED by ruling (RULED Q6)`. A refusal
   here is a document defect and never a reason to edit a digest.
4. **The GAINING leg, then the LOSING leg — in that order.** Each is its own
   pull request, § 5.5's two commits apply to the gaining one (place the carve
   blob, then apply the declared edits), and the order is chosen so the estate
   never has a window with the bytes at NO leg: a window with them at two is
   recoverable and one at none breaks every importer downstream.
   * **GAINING**: place the blob at `to_path` from the carve commit, apply the
     row's declared edits in commit B, then

     ```sh
     python3 scripts/verify-carve-arrival.py \
         --destination <to> --dest-root /path/to/<to leg> \
         --manifest docs/opendox-carve-manifest.yaml --source-repo . --phase A
     ```

     whose line must carry `N row(s) re-destined HERE`. Run `--phase B` after
     commit B. A missing file here refuses `arrival-missing` and names the
     ruling that made this leg owe it.
   * **LOSING**: delete the file at `from_path` — that deletion is the whole
     content of the commit — UNLESS another row's own effective arrival or a
     declared `--replica-at` replica already claims `from_path` at this same
     leg (a lawful refill: `check_vacated` excludes a path either one claims,
     leaving the arriving question to `check_arrivals`/`check_replicas`
     instead), in which case there is nothing here to delete and the file's
     presence is that arrival's or replica's own commit, not this one's. Either
     way, re-run the same invocation with `--destination <from>`. Its line must
     carry `N re-destined AWAY and verified vacated`. A copy left behind that
     no other row or declared replica claims refuses `arrival-not-vacated`.
5. **Both legs' own `validate` green, and both pull requests admin-merged on
   Brett's word** (§ 12 act 1), exactly as every other arrival is.

**What the floor does NOT prove here, stated so the evidence is not read wider
than it is.** `verify-carve-arrival.py` verifies ONE destination per run, so
the vacated-here and arrived-there halves are two runs and nothing compares
them with each other: it is this procedure — both runs, on the record, in the
two pull requests — that closes the pair, not the tool.

### 5.8 A RULED retirement — the `retired:` act

**RULED 5656343213** (Brett Heap, 2026-09-13, by interactive multi-choice, on
the question slice S8's author put in `#656` comment `5650335573` § 2). An
arrival may turn out to have nothing left to be: three suites reached their
legs NEEDING `views/intent-feed.js`, RULED OQ-F `not_moved` — so it stayed
HERE and arrived at NEITHER leg. (NEEDING, not driving, and the distinction is
the first use's own: the tray suite DROVE that module, while the wheel suite's
comment says it "rides along because dispose.js imports it" and that the probe
"drives the LOCAL path only". Both need it; one drives it; and the grammar's
`surface:` asks for what an arrival NEEDS and cannot obtain — see the manifest
header) — and slice S2 replaced the surface openDox
does have with `views/intent-binding.js`. The suites test a surface that is
not there. **TWO of the three end as RETIREMENTS here, and the third does
not** (Copilot review, round twenty-seven): openXdox-code's
`tests/test_staging_workbench.py` loses only the ENDING REPLAY inside it and
the rest of that file goes on arriving and driving surfaces that leg HAS, so
it takes an ordinary declared edit and no `retired:` block at all — "What the
form CANNOT express" below is that case, and a retirement is a fact about a
FILE's arrival. **§ 5.7 cannot say so**: `re_destined.to` is held to the closed
`destinations:` keys, openxFactory is the SOURCE and not one of them, and
`re_destined:` on a `not_moved` row refuses `carve-re-destined-not-moved`.
Deleting the arrived file with NO form at all was the other option, and it is
the one this floor exists to refuse — a file at no leg, in a row that says it
arrived there, is RULING OQ-1's UNDECLARED MOVEMENT read backwards.

**It is not a way to delete an arrived file for convenience**, and it is
gated twice rather than once. `ruling:` is required and validated PRESENT, on
§ 5.7's reasoning exactly (`carve-retired-unruled`). And `surface:` must name
a `not_moved` row of this manifest (`carve-retired-surface-live`): the claim a
retirement rests on is that the surface the arrived file NEEDED is gone from
BOTH legs, and a `not_moved` row is the one way this document can answer that
without reading a leg. A surface that is a MOVED row is LIVE at a leg; a
surface in no row is one the manifest never declared, and "this document
cannot say" is not "gone". **And one `not_moved` reason is excluded with the
moved rows**: `replicated_at_destination` (RULED OQ-C) means every destination
places its OWN copy — `--replica-at` admits them, and RULED Q-L7 (a) lets the
row declare the edits they carry — so such a surface is LIVE at each leg that
placed one, and citing it would rest the claim on a row that says the
opposite.

1. **The ruling first.** Brett Heap's word, on `#656` or on the pull request
   that asks for it, naming the rows, the surface they NEED and cannot obtain
   at their leg, and the evidence that the surface is at no leg. (A ruling
   asked for the surface they DRIVE would be asked a narrower question than
   the grammar answers, and the first act to use this form had one row of two
   that could not answer it.) Record the comment id — it is what every row
   below cites.
2. **ONE openxFactory row-amendment pull request, and it lands FIRST** — the
   same pairing § 5.7 requires. On each affected row add:

   ```yaml
       retired:
         at: opendox_code                        # the row's EFFECTIVE arrival
         at_path: tests/test_intent_tray_dom.py  # its own `destination_path`,
                                                 # or `re_destined.to_path`
         ruling: "`#656` comment 5656343213"
         surface: scripts/ideation_dashboard/web/views/intent-feed.js
         note: "RULED OQ-F kept the surface at openxFactory; S2 replaced the
           one openDox has with views/intent-binding.js."
   ```

   **Edit nothing else ON A ROW YOU RETIRE.** `destination:`,
   `destination_path:` and any `re_destined:` stay exactly as they were — they
   are the record of where the carve put the file and where a ruling moved it
   — and `disposition`, `sha256`, `git_mode`, `edits[]`, `carve_commit` and
   `carve_tag` are untouched. A retirement is a fact about a DESTINATION; the
   source side does not move.

   **THAT PROHIBITION IS THE RETIRED ROW'S, AND THE SAME ACT MAY STILL DECLARE
   AN EDIT ELSEWHERE** — measured on the first act to use this form, which
   retired two rows and declared a PARTIAL removal on a third. A ruling that
   takes part of an arrived file out has no retirement to record (the row goes
   on arriving), so it lands as an ORDINARY declared edit on THAT row's
   `edits[]` under an existing class: a different row, a different grammar, and
   nothing on it that this step forbids. The rule is one row at a time — what
   a row that is RETIRED may not carry says nothing about a row that is not.
   "What the form CANNOT express" below is that case in full.
3. **Verify the document**: `python3 scripts/validate-carve-manifest.py` must
   print `OK` and end `; N row(s) RETIRED by ruling (RULED 5656343213)`. The
   count prints in every state, zero included, so the document's own state is
   never the state no log records.
4. **ONE leg, and the deletion is one commit of its own.** Unlike § 5.7 there
   is no gaining half — the bytes go nowhere — so there is no ordering
   question and no window with the file at two legs. Delete the file at
   `at_path` on the leg `at` names; that deletion is the whole content of THAT
   commit. **And where the leg's own PROSE named the file, a SECOND commit in
   the same pull request repairs it** — measured on the first act to use this
   form, which found three sentences at openDox-code that the deletion
   falsified: a `validate.yml` comment calling the two suites "narrowed out"
   of its selection, when after the act they are not narrowed but ABSENT, and
   two sibling suites citing them as an EXISTING precedent for the
   node-driven DOM-probe pattern. A comment naming a file the same pull
   request deletes is a reference to nothing, and the next reader greps for it
   and finds a hole. Two commits and not one, for § 5.7's reason exactly: a
   reviewer reads the deletion by itself, in its own diff, and the repair
   beside it. Prose that is HISTORICAL — "this instrument came from X" — may
   stay as it is, and is worth a word saying the file is retired rather than
   missing.

   **AND THE REPAIR STOPS AT A CARVED FILE.** Measured one round later at
   that same act: two of the falsified sentences sat in files that THEMSELVES
   ARRIVED — `tests/test_account_menu_dom.py:4` and
   `tests/test_doxbench_tile_verbs.py:18-20` — and at a leg every line on
   which an arrived file differs from its carve blob must be declared in its
   openxFactory row under one of RULING OQ-1's three CLOSED classes: `import
   rewrites`, `path constants`, `adapter calls`. A comment naming a retired
   sibling is none of the three, and filing it as one would put a false
   description in the floor's own record to make a comment read better. The
   verifier says so in the sentence it would use for any other undeclared
   line — `arrival-undeclared-edit — tests/test_account_menu_dom.py was
   edited at carve-commit line(s) [4] … it declares [30] under class(es) path
   constants` — so the repair commit touches only the prose THE LEG OWNS: its
   workflow files, and the files it created under a declared admission
   (`docs/opendox-carve-admissions.yaml`). A stale sentence inside a CARVED
   file STAYS, named in the pull request as a known cost, until a ruling
   widens the class vocabulary or some other act amends that row for a reason
   the vocabulary already covers. Withdrawing such a repair is not a retreat
   — it is the floor holding, one act after the form that tested it. Then

   ```sh
   python3 scripts/verify-carve-arrival.py \
       --destination <at> --dest-root /path/to/<at leg> \
       --manifest docs/opendox-carve-manifest.yaml --source-repo . --phase B
   ```

   whose line must carry `N row(s) RETIRED here by ruling and verified
   absent`. A copy left behind refuses `arrival-not-retired` and names the
   ruling rather than the filename — UNLESS another row's own effective
   arrival or a declared `--replica-at` replica claims `at_path` at this same
   leg, which is a lawful refill exactly as § 5.7's is: the path a retirement
   empties may be legitimately re-occupied, and the entry there is then that
   row's or that replica's, verified on its own terms.

   **And a block the leg cannot read refuses BEFORE it is believed**
   (`arrival-unreadable`, naming `validate-carve-manifest.py`): an `at_path`
   that is not a plain path inside `--dest-root`, and a block whose
   `at`/`at_path` are not the row's own effective arrival. Step 3 is what
   normally catches both — they are `_require_closed_relative_path` and check
   6's `carve-disposition-inconsistent` — but the verifier runs at a LEG on a
   manifest it deliberately does not revalidate, and the question it asks of a
   retirement is "is this path EMPTY", to which every unread field answers
   "yes": a `../` path is absent because it is outside the tree, and a block
   naming another row's placement proves empty a path no ruling emptied. If
   you meet either, the repair is in the openxFactory row, not at the leg.
5. **The leg's own `validate` green, and both pull requests admin-merged on
   Brett's word** (§ 12 act 1), exactly as every other arrival is.

**What the form CANNOT express, stated because the first act to use it hit
it.** `retired:` retires a ROW, and a row is a FILE. A leg that must lose only
PART of an arrived file — one replay block at the end of a suite, say, driving
a surface the ruling retires, in a file whose other tests drive live surfaces
— has no retirement to declare, because the row's bytes do not stop arriving.
The minimal reading, and the one this floor already has a form for, is an
ORDINARY declared edit: a `moved_with_declared_edit` row whose `edits[]`
names the removed lines under an existing class, verified by
`arrival-undeclared-edit` like every other declared edit. Widening `retired:`
to a line range would put a SECOND line-bearing grammar beside `edits[]` and
give one row two readings of what its bytes are; that is a ruling's act, not
an author's.

**And `surface:` names ONE absence where a retirement may rest on two**, which
the first act also hit. The field is held to a `not_moved` row because that is
how THIS document answers "gone from BOTH legs" without reading a leg. The
wheel suite RULED 5656343213 retires is unrunnable at `opendox_code` for two
reasons, and only one of them is sayable: `views/intent-feed.js` is RULED OQ-F
`not_moved`, at neither leg, and is the `surface:` the row cites; and
`views/dispose.js`, which that suite really drives, went to `openxdox_code` at
§ 3.4 slice S5 — absent at this leg, but present at a leg, so naming it would
refuse `carve-retired-surface-live` and would be right to. The row's `note:`
carries the second absence in prose. A `surface:` list, or a second field for
"moved to another leg", would be the fix; both are a ruling's act.

**WHAT THE FIRST ACT LEFT BEHIND, named here because the next reader greps
for these names and finds a hole.** The rule above says a stale sentence
inside a carved file STAYS and is named in the pull request as a known cost;
this is that list for RULED 5656343213 (`#656` CLAIM `5656690570`,
openxFactory PR #1043), measured at the leg heads that carry the deletion —
openDox-code#24 at `e2d5ac46` and openXdox-code#20 at `15e8115d`.

* `tests/test_account_menu_dom.py`:4 sends a reader to
  `test_wheel_verbs_dom.py` for the DOM shim, and
  `tests/test_doxbench_tile_verbs.py`:19 names it as an instrument in use.
  Both files are `moved_with_declared_edit` rows whose only declared edit is
  `path constants`, at carve lines [30] and [34]; the repair is refused by
  name, and the second sentence is the sharper case — it also names
  `test_staging_workbench.py`, which arrived at the OTHER leg, so before this
  act it already named one file its reader could not open and after it names
  two. Both stay, and openDox-code#24's `validate.yml` comment records them at
  the leg as well.
* The prose THIS repository owns is repaired in the ANNOTATION pull request
  instead, because "the repair stops at a carved file" bounds the LEG's act
  and not openxFactory's own record:
  `docs/opendox-carve-admissions.yaml`'s `tests/test_intent_binding_dom.py`
  entry described the two retired suites as its "narrowed out of validate.yml"
  siblings. **Narrowing and retirement are different facts and the repair says
  so**: the leg's allow-list never named those two and still does not — the
  deletion deliberately leaves it alone — so what the entry now records is not
  an un-narrowing but the retirement, the absence it makes the floor require,
  and the pull request that answers it.
* `views/intent-feed.js` STAYS here, RULED OQ-F. A retirement deletes an
  ARRIVAL, never a surface; this act asks nothing of the surface row except
  that it still read `not_moved`, which is the gate.

**THE WINDOW BETWEEN THE TWO MERGES, in both of its shapes.** The annotation
lands first (step 2), so until the leg's deletion merges, that leg's own
arrival run REFUSES — measured against openDox-code `8efb3cf5` with this
manifest: `arrival-not-retired … still exists`, naming the ruling. It is
§ 5.7's window in its other form, and it closes by merging the deletion,
never by touching the manifest. The PARTIAL case is gentler: a declared edit
that has not yet been applied is no refusal at all, so between the two merges
the ending replay's lines simply read as not-yet-applied inside a row that is
still within its declared lines (measured at openXdox-code `c1ad341a`: 29 of
that row's **196 DISTINCT** declared carve lines differ, none undeclared —
distinct because A LINE IS DECLARED ONCE PER ROW: slice S5's ten sit INSIDE
this act's range and this act's entry deliberately does NOT repeat them, so the
row's four entries carry 196 line entries over the same 196 lines — 12 `import
rewrites`, 7 `path constants`, S5's 10 `adapter calls` and this act's 167 — and
the removed block's 177-line extent is stated in the two entries' NOTES rather
than by declaring ten numbers twice. The aggregate in § 2 sums line ENTRIES, so
a repeat would have published ten lines this act does not add while the row's
declared SET stood still, which is the defect
`test_the_real_manifest_carries_the_ruled_q_l7_amendment` pins against).

**And what the floor does NOT prove, on § 5.7's own terms.**
`verify-carve-arrival.py` verifies ONE destination per run, so a retirement at
one leg says nothing about any other; nothing at the destination reads the
SURFACE the block cites, which is a claim about openxFactory's own tree and is
`validate-carve-manifest.py`'s `carve-retired-surface-live`; and the check
does not prove the arrived test was the surface's only reader, or that no
other file should follow it. The form RECORDS a ruled act and bounds it; it
does not discover one.

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

**AMENDMENT, 2026-09-10 — RULED Q7 SUPERSEDES RULING F FOR OPENDOX ONLY.**
The paragraph above's *"openxFactory pins openXdox and nothing else … openDox's
commit is a DERIVED value read through openXdox's own `contracts/opendox-
pin.yaml` and is never separately declared, pinned or mounted here"* no longer
holds for openDox. Brett Heap's Q7 ruling (`opensoft/openxFactory#656` comment
[5626248666](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5626248666),
2026-09-10), verbatim: *"RULED (i): SECOND SUBMODULE — openxFactory mounts the
openDox assembly root (gitlink → opensoft/openDox main `49a99df2…` +
`contracts/opendox-pin.yaml`, mirroring the openXdox pin of #917); both legs'
`src/` become reachable and the re-point rides in PR-2. openxFactory then
declares two direct upstreams (openDox, openXdox)."* Placement was ruled
separately (`#656` comment
[5626260214](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5626260214)):
*"OWN PR FIRST, MERGE WHEN GREEN … plain gate unless it touches
`openspec/changes/`"* — landed as its own pull request, PR #932, rather than
riding inside § 8's atomic PR.

**THE LOCKSTEP INVARIANT this second direct pin adds.** openxFactory's own
`contracts/opendox-pin.yaml` `commit:` MUST EQUAL the commit openXdox's own
`contracts/opendox-pin.yaml` names, at whatever commit the `openXdox` gitlink
here records. Two independent, direct declarations of one product's bytes are
exactly the defect `neutral-product-pin`'s chain clause exists to end, unless
something holds them equal: `scripts/verify-opendox-pin.py`'s fifth check is
that something. It reads openXdox's own derived pin as a git blob out of the
mounted `openXdox/` submodule's own object store, AT THE COMMIT THE `openXdox`
GITLINK RECORDS — never openXdox's mutable working tree, so an operator
editing that file on disk without moving the gitlink cannot fool the check —
and refuses `opendox-pin-lockstep-mismatch` the moment the two commits
disagree. `contracts/openxdox-pin.yaml` and `scripts/verify-openxdox-pin.py`
are UNCHANGED by this amendment: RULING F still governs THAT pin (openXdox
pins openXdox and nothing about openDox); the second, independent pin is
openxFactory's own new declaration, not an edit to the first.

`openspec/changes/split-opendox-two-layer-product/design.md`'s matching
sentence (§ D-pin: *"openxFactory's ONE pin file — `contracts/openxdox-
pin.yaml` — also names \[openDox] for openXdox (RULING F …): openxFactory
carries no `contracts/opendox-pin.yaml` of its own, and openDox's commit there
is a DERIVED value read through openXdox's own pin"*) is amended by PR-2's
packet patch, **not here** — this paragraph is the runbook's own record of the
ruling, and the design document's own text is a separate, later edit under its
own change control.

---

## 8. Phase 5 — openxFactory § 5, ONE ATOMIC PULL REQUEST

**ROLLBACK (written first): revert the § 5 pull request.** It is one commit set
by construction, so the revert is one act; the destinations keep everything they
were given, because this phase gives them nothing.

The wallet's P3 reasoning applies for the same reason — *no ordering of two
commits leaves a green intermediate* — so the pin, the gitlink, the shed, the
floor re-cut and the workflow conversion land together:

* `contracts/openxdox-pin.yaml` + the gitlink;
* the shed of the carve surface's stays-nothing half — **and, in the same
  commit, `phase: post-shed` in `docs/opendox-carve-manifest.yaml`**, which is
  what keeps FLOOR PART 1 green over the tree the shed leaves. It is not a
  re-cut: no digest, no disposition, no `carve_commit` and no `carve_tag`
  moves, and the label stays `opendox-carve-0`;
* **the floors, re-cut as a deliberate act with its own evidence row.**
  `.github/workflows/pytest-suite.yml` carries `MIN_SELECTED: "7090"` and
  `MIN_PASSED: "7070"` (floors that may only rise) and `EXPECT_SKIPPED: "21"`
  (pinned EXACTLY, and a SUM). The shed removes **3,404** `def test_` — this
  section said 3,426 until it was MEASURED, over the 319 paths the manifest's
  own rows derive, at `main` `554536f6`; the count below supersedes the older
  figure and is never to be carried by hand:

  ```sh
  python3 - <<'PY'
  import pathlib, re, yaml
  doc = yaml.safe_load(pathlib.Path("docs/opendox-carve-manifest.yaml").read_text())
  shed = [r["source_path"] for r in doc["rows"]
          if r["disposition"] in ("moved_verbatim", "moved_with_declared_edit")
          or r.get("reason") == "deleted_at_carve"]
  n = sum(len(re.findall(r"^\s*def test_",
                         pathlib.Path(p).read_text(errors="replace"), re.M))
          for p in shed)
  print(f"{len(shed)} shed paths, {n} def test_")   # 319 shed paths, 3404 def test_
  PY
  ```

  So both
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

**HOW TO VERIFY IT**, and it is TWO questions rather than one asked twice.
`scripts/verify-carve-test-mapping.py` (design record in
`scripts/carve_test_mapping.py`'s docstring) answers the SOURCE side from the
manifest and this repository's history alone —

```
python3 scripts/verify-carve-test-mapping.py
```

— printing every term of the sum, and the DESTINATION side one leg per run,
never as a cross-repository equality:

```
python3 scripts/verify-carve-test-mapping.py \
    --destination openxdox_code --dest-root ../openXdox-code
```

and, where a replica is placed at that destination, the same command with the
placement declared — the flag is repeatable and the block above is COPYABLE,
which the bracketed form it replaces was not (argparse reads `[--replica-at`
as a flag and fails before the destination is looked at):

```
python3 scripts/verify-carve-test-mapping.py \
    --destination openxdox_code --dest-root ../openXdox-code \
    --replica-at tests/corpus-adapter/test_conformance.py=tests/test_conformance.py
```

`--destination` takes a `destinations:` key or the literal `openxFactory` for
the retained column, whose `--dest-root` defaults to this repository. A replica
joins a destination's floor only where `--replica-at` declares its placement,
on the rule § 2.1 already states for `verify-carve-arrival.py`: RULED OQ-C
gives a replica no `destination_path`, so there is nothing to derive one from.

**THE SAME FLAG SPELLING, A DIFFERENT QUESTION, and the one row where the two
tools give OPPOSITE instructions is the row that matters most.** § 2 tells the
operator NOT to declare `tests/corpus-adapter/test_conformance.py` to
`verify-carve-arrival.py` — its implementation-aware block (`:72-84`) imports
the home factory and MUST be rewritten at each destination, so it is neither
verbatim nor declared-edit by construction and a declaration would refuse it on
its digest. THIS floor compares no bytes: it counts `def test_`, which that
rewrite does not touch. So the row the arrival verifier must not be given is
exactly the row this one must — **20 of the 30 replicated test functions are in
it** — and an operator who carries § 2's instruction across to this flag would
silently leave two thirds of the replica term out of every leg's floor.
The four refusals are `test-home-missing`, `test-home-deleted-at-carve`,
`replica-multiplicity-undeclared` and `destination-test-shortfall`, with
`test-mapping-unreadable` for a question the floor cannot ask — and an
uncomputable check is never a pass.

**AND THE DOCUMENT IS READ BEFORE IT IS BELIEVED**, because every one of
these was measured to pass on the landed manifest before it was refused:
a `carve_commit:` that is not 40 lowercase hex (it is interpolated into a
`git cat-file --batch` request, so a line terminator in it injects a second
request per row — measured: `source_count 0`, identity `0 = 0`, **exit 0**
over a surface carrying 4,411 `def test_`); a `source_path:` declared by two
rows (counted twice, 4,411 → 4,446, identity still balancing); a row with no
`source_path:` at all (a traceback, where the contract is a named refusal);
a `moved_paths:` naming a prefix NO row lies under (every row outside the
surface, `rows_in_surface 0`, exit 0); and, at a destination, a `retired:`
block or a `destination:` naming a key the manifest does not carry — which
took the openDox-code leg from 117 rows / 1,067 declared to 116 / 1,045 and
exited 0, a leg passing because a live arrival had been silenced by a key
naming nothing. A `--replica-at` placement is admitted only for a row under
the declared surface, for the same reason in the other direction: a floor is
neither lowered inside the set it is quantified over nor raised outside it.
Every row's `disposition:`/`reason:` must be IN FLOOR PART 1's vocabulary — the
source side refuses an unknown one by name, and a LEG read it as another
destination's business and passed without ever asking for that arrival — and
every `destinations:` key must be a non-empty string naming a map with both a
`repository:` and a `leg:`, because an incomplete identity compares equal to
nothing and a leg named by it is asked for no arrival at all. And the surface
must cover the WHOLE document — a `moved_paths:` that omits
some of its own rows reports `0 = 0` over the part it omits, which at the limit
is a prefix matching one zero-test row; the landed manifest's 456 rows are all
under its surface, and that was asserted only in pytest until this round made
it a refusal the runbook's own invocation makes.
`tests/carve_test_mapping/test_carve_test_mapping.py` drives the source side on
every required-suite pass, the seat `tests/carve_manifest/` holds for FLOOR
PART 1.

**MEASURED 2026-09-16, and every figure re-derived rather than recited.**
Source **4,411** `def test_` over **146** test-bearing rows of the declared
surface — **144 homed and 2 RULED-retired, and the two counts are disjoint
and exhaust the 146**: a retirement deletes the row's OWN arrival, so a
retired row is never counted among the homed — not even where
`also_replicated_to:` copies of it survive elsewhere, which is the case the
report now names copy by copy. Three test-bearing replicas carry **30** at
`m = 3`. At the destinations, against their own rows'
declarations: openDox-code `0b4e8bb` **1,067 / 1,067**, openXdox-code
`0a0265f` **2,315 / 2,319**, the retained openxFactory column **998 / 1,018**.
The sum carries a FOURTH term, which is arithmetic and not an amendment: § 5.4
was amended 2026-09-09, the `retired:` form was RULED `5656343213` on
2026-09-13, and its first use (openxFactory PR #1043) retires two TEST-BEARING
rows carrying **31** between them, so

```
Σ(destinations) = source_count + Σ over EVERY row of (|homes| − 1) × tests

  source_count             4,411
+ replica excess (m − 1)      60   `replicated_at_destination` rows
+ also-replicated excess       0   RULED Q-L7 (a) moved-AND-replicated rows
+ retired term               −31   the same rule over retired rows
= Σ(destinations)          4,440
```

**ONE RULE, four buckets, and the tool prints all of them on every run.**
§ 5.4 states the last two as a subtraction — *"− Σ over RETIRED rows of
row_test_count"* — and that is exact for every row that has landed, because
each retired row's only home is the one the ruling deleted. It is NOT exact
for a row that is retired AND replicated: retirement deletes the row's own
ARRIVAL and not the copies its `also_replicated_to:` places elsewhere, so
such a row's term is `(1 − 1) × tests = 0` rather than `−tests`. Apply the
one rule, not the subtraction, and the two agree wherever the subtraction is
right.

A retired row is not a lost test: the form REQUIRES a `ruling:` and reads as no
retirement without one, so the deletion is the RULED decision clause (a)
demands rather than one inferred from a disposition — and the tool NAMES every
one of them, with its path, its count and its ruling, on every run.

**THE REFUSAL IS THE DESTINATION TOTAL AND NOT A PER-ROW EQUALITY, decided by
measurement.** `tests/ideation-dashboard/test_serve_column_split.py` is a
`not_moved / stays_openxfactory_adapter` row declaring 9 `def test_` at the
carve commit and carrying 8 today: § 3.4 slice S6 (RULED Q4, `#656` comment
`5642758731`) moved that test's SUBJECT out of the file's domain and the
successor runs at `opensoft/openDox-code`'s
`tests/test_source_core_arm.py::test_route_dispatches_the_exact_arm_before_the_prefix_arm`.
A per-row equality would go red on a RULED re-homing that lost nothing. So the
total is the refusal and the per-row deltas are REPORTED BY NAME on every run,
because a canceling pair holds a total while a file loses coverage — **and in
BOTH SIGNS, which cost a round to get right**: only the shortfalls were printed
until 2026-09-17, so the retained column's `+20` named no arrival at all and
the canceling pair the sentence above is about could not be inspected. It
resolves to SIX rows carrying `+21` between them, each named with its declared
and its found count, against that one `−1`. A row ABOVE its declaration is not a fault — a leg may add tests
to a file it received — it is the other half of the evidence.

**CLAUSE (d) — HALF BUILT, HALF BLOCKED, and the blocker is the BUILD arc.**
openxFactory's half is `.github/workflows/pytest-suite.yml`'s pinned triple —
SKIPPED exactly, SELECTED and PASSED as floors, failures and errors zero.
Neither leg can carry its half today: `opensoft/openDox-code` and
`opensoft/openXdox-code` both run `python -m pytest -q <named files>
--noconftest` in `validate.yml`, with no JUnit report and no totals, and both
workflows record the reason in their own words — *"with the root conftest in
play the tree is 1188 errors and 0 passed"* and *"THIRTY-SEVEN of this leg's 88
test files fail COLLECTION"*, each naming `split-opendox` § 3.5/§ 3.6 as what
the narrowing waits on. A triple pinned over a tree that cannot be collected is
a required check held red by another act's defect, which is the deadlock class
clause (d) itself refuses by name. **The leg half of clause (d) is therefore
owed to each leg's own pull request AFTER the BUILD arc lands, and § 5.4 does
not close until it does.**

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
`carve-digest-mismatch`, `carve-file-undeclared` or `carve-path-absent`
(a `carve-shed-incomplete` is NOT this: it says the manifest's declared phase
and the tree disagree, and its remedy is inside § 5.2, never a re-cut) — the
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
| 4 | **The tags** — `dox-v1.0`, `xdox-v1.0`, and openxFactory's MAJOR | Phase 6 (§ 9) |
| 5 | **Re-cutting `carve_commit`** if `main` moves under the carve | § 11 |
| 6 | The openxFactory § 5 merge — the largest diff in this repository's history | Phase 5 |

**The lane's, as pull requests:** the arrival commits and declared edits at the
four legs; the assembly-root pin/gitlink commits; this runbook; the arrival
verifier; the scaffold levelling; the openxFactory § 5 diff. **None of them
merges without act 1.**
