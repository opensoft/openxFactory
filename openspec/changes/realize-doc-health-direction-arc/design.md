# Design: realize-doc-health-direction-arc

Status: draft
Authored: 2026-10-06, lane `openxfactory-4`, as plan 038's T070.
Kind: architecture

This design carries out a ruling. It does not reopen it. ARC-Q1–ARC-Q4 are
answered (`#656` `6003918488`), and so are ARC-1, ARC-5 and the tier-3
defaults ARC-2, ARC-3, ARC-4 and ARC-6 (`#656` `6013547504`). What remains is
HOW, and § 11 puts the seven choices this design makes for Brett's ratify
read, each with its alternative.

## 1. The rulings this change carries out

| ruling | answer, verbatim | what it fixes here |
|---|---|---|
| ARC-Q1 | *"Retarget all eight (Recommended)"* | §§ 3, 4, 6: the generic slice in openDox-code; the governed names through seams openXdox-code declares and openxFactory's host registers; the 7 tests respelled; `corpus-adapter-seam` unchanged |
| ARC-Q2 | *"Composed CI in openXdox-code (Recommended)"* | the composed home of whatever needs the host's implementations. Its declarations are #1144's (plan 038 T073), not this change's |
| ARC-Q3 | *"Own change, beside phase 5 (Recommended)"* | this change, its `code_surface:`, its owner (lane openxfactory-4), and that it gates nothing |
| ARC-Q4 | *"Confirm (Recommended)"* | the realization is not on 12.5's path |
| ARC-1 | *"implemented (Recommended)"* | `target_release: implemented` |
| ARC-5 | *"Archive with F9.2 open (Recommended)"* | § 7: F9.2's closure in this change's evidence, or in #1144 while #1144 is active |
| ARC-2, ARC-3, ARC-4, ARC-6 | *"Accept all as recommended (Recommended)"* | the id; `skip_specs: true` and the openXdox-spec condition (§ 5); the trailer and the surfaces check (§ 8); the opportunistic `lines` slice and the arc's own pin chain (§ 9) |

## 2. What was measured, and where

Every fact below was re-measured for this filing in fresh clones. openXdox-code
and openDox-code were still at the commits lane openXfactory-3's ask measured
(`lane-coord-034/r2/R2-ARC-ASK.md`, facts 1 and 2):

- openXdox-code `56e1c238681a7693a4d8d42a62c1523cf4d4ab91` (`main`, 2026-10-05)
- openDox-code `a9ac96f974d83c63908246e18592af52ca70907a` (`main`, 2026-10-05)
- openXdox-spec `f088b09732e236279898b53ab9fb0f5ebc89509a` (`main`, 2026-09-17)
- openDox-spec `f7ee3c763b3af4581daf1cd54406e5111e9358e6` (`main`, 2026-09-29)
- openxFactory `92010d3e67f2c556687e1c3583ed3ca1867f4b8b` (`main`, this branch's base)

**The surface: 13 statements over 8 modules.** In an openXdox-code clone:

    git grep -nE '^\s*(from doc_health|import doc_health)' 56e1c238 -- src/openxdox/

prints 13 lines. That equals `DOC_HEALTH_SURFACE`
(`tests/test_dependency_direction.py:353-363`): 7 at import time and 6
deferred.

| module | statements (import-time / deferred) | `doc_health` names it uses | class |
|---|---|---|---|
| `completeness.py` | `:81` (1 / 0) | `lines.split_keepends` | generic |
| `round_trip.py` | `:43` (1 / 0) | `lines.join_rows`, `split_keepends` | generic |
| `generator.py` | `:66`, `:67`, `:68` (3 / 0) | `corpus.Doc`, `load_docs`, `parse_status`, `STATUS_SCAN_LINES`; `RealGit`; `lines.split_keepends` | mixed: `lines` and `RealGit` generic, the rest governed |
| `corpus_root.py` | `:34` (1 / 0) | `corpus.GOVERNED_ROOTS`, `iter_doc_paths` | governed |
| `gate_console.py` | `:63` (1 / 0); `:1291`, `:2154`, `:2200` (0 / 3) | `corpus.STATUS_SCAN_LINES`; `derive_possibles.INDEX_REL`, `INDEX_MD_REL`, `REGISTER_KEY`, `apply_disposition`, `render_index_yaml`, `validate_index`, `DispositionError`; `ideation_readiness._render_markdown` | governed |
| `cli_gate.py` | `:251` (0 / 1) | `derive_possibles.INDEX_REL`, `INDEX_MD_REL` | governed |
| `gate_routes.py` | `:425` (0 / 1) | `derive_possibles.INDEX_REL`, `INDEX_MD_REL` | governed |
| `snapshot_registry.py` | `:311` (0 / 1) | `pin_sentinels.UNKNOWN` | governed (inferred from the broad scan) |

Two more facts sharpen fact 1 of the ask:

- **`generator.py` takes ONE read from `RealGit`, `head_sha`** (`:128`, inside
  `RealGitDates`). Its `commit_date` is already its own `git show -s
  --format=%cI` (`:139-141`). So "RealGit's few git reads" is one read.
- **`gate_console.py` reaches `split_keepends` and `join_rows` only through
  `round_trip`** (`:424`, `:432`, `:504`, `:515`, `:530`), so retargeting
  `round_trip.py` retargets those calls too.

**The declared exclusion: 66 files.** `tests/declared_exclusion.yaml` at
`56e1c238` holds 66 entries. By reason: `doc_health` 60,
`status-exemption-rail` 3, `openxfactory-contracts` 5. By single reason:
`doc_health` alone 58, the rail alone 2, the contracts alone 4. Measured by
loading the file with PyYAML and counting each entry's `reasons`.

**The 7 test files that import `doc_health` directly:**

    git grep -lE '^\s*(from doc_health|import doc_health)' 56e1c238 -- tests/

prints `test_completeness.py`, `test_doxbench_packet.py`,
`test_gate_console.py`, `test_header_value_readers.py`, `test_kickoff.py`,
`test_repo_root_guard.py` and `test_round_trip.py`. None is among 12.5's 16
protected suites (lane openXfactory-3's addendum to the ask). None is among
F5.2's seven generator suites either: `ls tests/test_generator.py
tests/test_snapshot*.py tests/test_session_snapshot.py` at `56e1c238` names
`test_generator`, `test_session_snapshot`, `test_snapshot`,
`test_snapshot_determinism`, `test_snapshot_registry`,
`test_snapshot_validation_launch` and `test_snapshot_validator_home`.

## 3. The generic slice, re-authored in openDox-code (plan 038 T072)

ONE new standard-library module in openDox-code (T072 names it). It carries:

- `split_keepends(text)` and `join_rows(rows)`, with the real-line rule
  openxFactory's `scripts/doc_health/lines.py:111`, `:132` implements: lines
  end at CR, LF or CRLF only, so `join_rows(split_keepends(t)) == t` for every
  `t`;
- `head_sha(repo)`, the one git read the generator takes from `RealGit`.

**It is a re-authoring, not a relocation.** openxFactory's `doc_health/lines.py`
stays, and so does every caller of it in openxFactory. That is what R2Q14 (a)
and #1144's 11.1 require: no edit to openxFactory outside host wiring, pin
pairs and the carve manifest's notes.

**Its falsifier is behavioural.** T072's tests assert the round trip over a
corpus of line endings (CR, LF, CRLF, none, mixed, and the exotic separators
`str.splitlines()` would wrongly split on: form feed, U+2028). A test that
compares the module with openxFactory's `lines.py` would need openxFactory and
belongs in the composed run, not in openDox-code's own suite.

**It is opportunistic (ARC-6).** It rides T061's 0.2.0 pin only if it has
already landed. T061 never waits for it. A later T072 rides the arc's own pin
chain (§ 9).

## 4. The seams openXdox-code declares, and the host that fills them

### 4.1 Four seams

| seam | what it supplies | consumers |
|---|---|---|
| S1 corpus loading and status reading | `load_docs` and the `Doc` objects it returns; `parse_status`; `STATUS_SCAN_LINES` (the lifecycle header window, 15 real lines today); `GOVERNED_ROOTS`; `iter_doc_paths` | `generator.py`, `corpus_root.py`, `gate_console.py` |
| S2 the possibles index and its disposition | `INDEX_REL`, `INDEX_MD_REL`, `REGISTER_KEY`, `apply_disposition`, `render_index_yaml`, `validate_index`, `DispositionError` | `gate_console.py`, `cli_gate.py`, `gate_routes.py` |
| S3 the readiness renderer | `ideation_readiness._render_markdown` | `gate_console.py` |
| S4 the pin sentinel | `pin_sentinels.UNKNOWN` | `snapshot_registry.py` |

These are the four groups ARC-Q1 (a) names. T074 declares them in openXdox-code
and names the module. Each takes ONE registration, as openDox's seams do: a
second registration of a different object is refused, and the same object
again is a no-op. Each has public calls that answer whether it holds a
registration and that empty it, because the host takes a registration back on
a refusal (§ 4.3).

### 4.2 Three rules every seam keeps

- **Read at USE, never at import (D2).** A host fills the seams at process
  start, after openXdox's modules have been imported, so no module-level value
  may be computed from a seam. Three are today:
  - `generator.py:77`, `HEADER_SCAN_LINES = corpus.STATUS_SCAN_LINES`;
  - `gate_console.py:76`, the same;
  - `corpus_root.py:43`, `SCANNED_ROOTS = tuple(sorted({*corpus.GOVERNED_ROOTS, "openspec"}))`.

  Each becomes a value read when it is used. openXdox-code already has the
  form: `projection_contributions` reads `corpus_root.SCANNED_ROOTS` "when it
  is used" (`src/openxdox/projection_contributions.py:158-198`).
- **An unregistered seam refuses BY NAME (D3).** A read from an empty seam
  raises an error naming the seam and what registers it. It never answers an
  empty list, a default value or a skip. This is the posture
  `corpus-adapter-seam`'s second requirement takes for an unresolvable corpus
  (`spec.md:47-68`): an unanswerable question is never an implicit pass.
- **Types keep their identity.** `Doc` and `DispositionError` are the
  governed modules' own objects, read through the seam, so `isinstance` and
  `except` hold by identity. That is how `column_contributions` already treats
  the gate's classes (`src/openxdox/column_contributions.py:69-74`).

### 4.3 The host fills them (plan 038 T075)

openxFactory's `scripts/opendox_host.py` lists every seam it fills in
`seams()`, as `(module, registration call, what it registers)`
(`:518-533` at `92010d3e`). It checks that each declared seam's take-back calls
exist before it writes anything (`_TAKE_BACK`, `:541-554`), and on a refusal it
empties what it wrote, in reverse order (`register_seams()`, `:665-759`).
T075 adds the four seams to that list, with their `_TAKE_BACK` rows, and
registers openxFactory's own `doc_health` implementations at them.

**Two orderings matter:**

- **The four are their own all-or-none group (D7).** `register_seams()` today
  refuses a leg that declares some of its six openDox seams and not others,
  because those six arrive at openDox-code commits (its docstring at `:668`;
  the refusal at `:718-731`). openXdox's
  four arrive at ONE openXdox-code commit, T074's. A leg before T074 declares
  none of them, and that is "a leg, not a gap". A leg declaring some of the
  four is refused by name.
- **The governed seams are filled before the host's column call, and taken
  back if it refuses.** The host calls `column_contributions.register()`
  itself, after its projection call (`column_contributions.py:49-51`). Under
  D4 (a), that call reads whether the governed seams are registered, so they
  must be filled first. That REVERSES today's order: `register_openxfactory()`
  makes its projection and column calls BEFORE `register_seams()`
  (`opendox_host.py:920-957`), so that their refusal leaves no host seam
  written. T075 keeps that property with a cross-call take-back: the four
  governed seams are registered as their own step before the column call, and
  if that call returns nothing or raises, they are emptied again, in reverse
  order, before the refusal reaches the caller. The host-wiring test (T075)
  covers both outcomes.

**The pin pair travels with it.** The openXdox root first moves its `code`
pin to T074's openXdox-code commit, in its own PR (§ 9, step 5). Then ONE
openxFactory PR carries the registration together with openxFactory's
`openXdox` pin pair, naming that root commit (step 6), so openxFactory's
`main` never runs an openXdox that declares seams it does not fill.

### 4.4 Between T074 and T075: the composed conftest

openXdox-code's composed run (U-9, T029) imports openxFactory's `scripts/`
from the pinned composed tree. Once T074 lands, the 12.5 suites in that run
would meet empty seams. So until T075 lands, the composed conftest registers
openxFactory's governed implementations from the composed tree's `scripts/`
(plan 038 T074, ADV-19). That interim registration leaves in the openXdox-code
PR that next advances `tests/composed_host_pin.yaml` past T075's openxFactory
commit.

### 4.5 A lone openXdox-code checkout after T074

Every module imports: `python -c "import openxdox.gate_console"` exits 0 with
no openxFactory on the path, which T074's falsifier checks (`tasks.md` group
3). Governed
BEHAVIOUR refuses at the first empty seam, by name (D3). The four governed
columns follow D4.

## 5. Why no openXdox-spec delta (ARC-3; D1)

ARC-3 asks for an openXdox-spec delta only "if the seams need contract text".
Measured, they do not:

- **The precedent is uniform.** The six seams openxFactory's host fills today
  (`opendox_host.py:518-533`), and openXdox's own column and projection
  registrations at openDox's seams (`column_contributions.py`,
  `projection_contributions.py`), landed in release 1 with no spec-leg text.
  openDox-spec promotes no capability (`openspec/specs/` is empty at
  `f7ee3c76`). openXdox-spec promotes one, `openxdox-projection-surfaces`,
  whose single requirement governs how projection surfaces render, not how a
  module is registered, and its last commit, `f088b097` of 2026-09-17,
  predates those seams. Their first commits, by `git log` in each clone:
  openDox-code's `register_health_check` and `register_status_exemption`
  2026-09-26 (`582ed07`, `8017cd5`); openxFactory's `seams()` 2026-09-29
  (`f56c87c6`); openXdox-code's `projection_contributions.py` 2026-09-30
  (`839492d`) and `column_contributions.py` 2026-10-05 (`56e1c23`).
- **What governs the seams is already written.** `corpus-adapter-seam`
  Requirement 1 fixes the direction, and its second requirement fixes the
  fail-closed posture. #1144's 11.1 names host wiring as an admitted
  openxFactory surface. The host-wiring test under `tests/domain_profile/`
  (T075) is the check, as it is for the six existing seams.
- **The seams cross no file, wire or schema boundary.** They are Python
  registration points inside one process, filled by trusted installed code,
  which R2Q16 (a) rules runs in process.

**Where this stops being true.** If T074 finds that a seam must carry a value
across a file, wire or schema boundary, or changes behaviour that
`openxdox-projection-surfaces` specifies, T074 stops. The change then gains an
openXdox-spec delta for Brett's word before the slice continues. No such case
was found at filing.

## 6. The 7 respelled tests (T074)

None is protected (§ 2). What each imports, at `56e1c238`:

| file | `doc_health` imports |
|---|---|
| `test_completeness.py` | `:33` `corpus` |
| `test_doxbench_packet.py` | `:592`, `:641` `corpus.parse_status`; `:616` `corpus.STATUS_SCAN_LINES`, `parse_status`; `:617` `lines.split_keepends` |
| `test_gate_console.py` | `:47` `families`; `:1888`, `:2183` `derive_possibles` |
| `test_header_value_readers.py` | `:17` `corpus` |
| `test_kickoff.py` | `:335` `derive_possibles` |
| `test_repo_root_guard.py` | `:49` `corpus` |
| `test_round_trip.py` | `:31` `families` |

Each import is respelled to one of three homes, chosen per import at T074:

1. **T072's openDox-code module**, for the generic names (`split_keepends`).
2. **The seam**, for a governed name the module under test reads. The test
   then needs the host's implementation, so it runs composed.
3. **The governed module itself, as an ORACLE**, where the test compares
   openXdox's behaviour with openxFactory's (`families` in
   `test_gate_console.py:47` and `test_round_trip.py:31`; `parse_status` in
   `test_doxbench_packet.py`). The oracle is openxFactory's by design, so the
   comparison runs composed, as ARC-Q2 (a) provides. It is not rewritten to
   read the seam it is testing.

## 7. F9.2 and its three removals (T074, T076; ARC-5 (a))

F9.2 is #1144's falsifier for 9.3's integration tests. In an openXdox-code
checkout with openDox arriving ONLY through the pin, its last line runs
`tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_32_entry_tree_the_manifest_records`,
which fails today because `cli_gate` imports `gate_console`, which imports
`doc_health` at load time. Three things hold it open, and the realization
removes all three:

1. **The required check's deselect.** openXdox-code's
   `.github/workflows/validate.yml` passes that node to `--deselect` as
   `LEFT_OUT` (`:161-164` at `56e1c238`). T074 removes it.
2. **The guard test beside it.**
   `test_the_help_tree_is_left_out_only_while_its_stated_reason_holds`
   (`tests/integration/test_assembled_surface.py:257`) passes only while the
   child fails for the stated reason, so it fails once T074 lets the command
   line build. The PR that clears the reason takes the deselect and the guard
   out together. T074 removes it.
3. **F9.1's `--deselect`,** batch J's, in #1144's `tasks.md`
   (`5870594693`, citing `5859927858`). T076 removes it and ticks F9.2 there,
   under a Rule 6 window, ONLY while #1144 is active. If #1144 has archived,
   its archived `tasks.md` is never edited, and F9.2's closure lives in this
   change's evidence alone (ARC-5 (a); ADV-20).

T076 re-runs F9.2 after T074 and T075 and quotes it, exit 0, in this change's
`evidence/`.

## 8. The trailer and the surfaces check over this change's own landings (ARC-4; ADV-37; D5)

**The trailer.** Every realization landing, in every repository this change
touches, carries `Arc: realize-doc-health-direction-arc`: T072 in openDox-code;
T074 in openXdox-code, and the openXdox-code PR that advances the composed pin
past T075 and removes § 4.4's interim registration (`tasks.md` 4.4); T075 in
openxFactory and the openXdox root; and the arc's own root and pin commits if
ARC-6 needs them. When T072 rides T061's pin instead, the pin landings are
plan 038's T062 and T063: #1144's realization, under #1144's trailer and never
this change's, so #1144's own guards still see them. A squash landing carries
it because the PR body does, and a merge landing because the lander writes it
into the merge message. Bookkeeping, evidence, this filing, T071's record,
T076's #1144 edit and T077's archive carry none.

**Why a check of its own.** #1144's guards find #1144's landings by #1144's
trailer: F11.1 in openxFactory, and F5.2's and 12.5's protected-suite oracle
in openXdox-code (`scripts/protected_suites.py`, which takes the landings as
a list). Neither sees a landing under this change's trailer. So this change
runs both guards over its OWN landings:

- **In openxFactory: F11.1's guard, re-selected.** #1144's F11.1 command, as
  it stands at this change's filing base, with three substitutions:
  1. the grep reads `--grep='^Arc: realize-doc-health-direction-arc$'`;
  2. the base is this change's own filing merge commit (`CHANGE_MERGE`), not
     #1144's `PACKET_MERGE`, so this filing's own README bullet and ledger row
     lie outside the range;
  3. `COMPOSITION_TESTS` and `ADMITTED_ARC_EDITS` are EMPTY. Those two lists
     were admitted for #1144's phases by name (R1Q2 (a); `5890601202`, "Named
     closed list"), and this change inherits neither. Each grows only by a
     ruling.

  The three declared surfaces are unchanged: host wiring
  (`scripts/opendox_host.py`, `scripts/profile_openxfactory.py`, tests under
  `tests/domain_profile/`), the two pin pairs, and the carve manifest's notes.
  A declared surface may be edited and never removed. It must print
  `requirement 1 holds`. `tasks.md` 4.3 carries the full command.
- **In openXdox-code: the protected-suite oracle over this change's
  landings.**
  `python3 scripts/protected_suites.py --landings=<this change's openXdox-code landings> --suites=<12.5's 16>`,
  and the same with `--chains --suites=<F5.2's 7>`. Both must exit 0. T074
  touches no protected suite (§ 2), so both are expected to pass with no
  allow-list entry. A failure stops the archive.

It is quoted in T075's PR, and again at the archive (T077) with `ARC_TIP` the
last realization landing.

## 9. Pins and landing order (ARC-6)

Plan 038 § "Pins and landing order" holds. For this change:

| step | what | when |
|---|---|---|
| 1 | openDox-code lands T072 | after T071 |
| 2 | openDox root: `code` gitlink and `contracts/code-pin.yaml` | rides T062 if T072 landed before T061; otherwise the arc's own root commit |
| 3 | openXdox-code `pyproject.toml` `opendox @ git+https://github.com/opensoft/openDox-code@<sha>` to step 1's openDox-code commit, the one step 2's `code-pin.yaml` records (never the root's own commit) | rides T063, or the arc's own |
| 4 | openXdox-code lands T074 | after T071, step 3, T021 and T073 |
| 5 | openXdox root, in its own PR: `code` gitlink and `code-pin.yaml` to T074; `opendox-pin.yaml` to step 2's commit only if step 2 was the arc's own (a step 2 that rode T062 is already pinned there by T064) | T075, landed first |
| 6 | openxFactory, in ONE PR with the host registration: the `openXdox` pin pair naming step 5's root commit, and the `openDox` pair if step 2 was the arc's own, one commit per pair | T075 |
| 7 | the aggregation's routine pin-sync | after T075, with the three-way openDox/openXdox gitlink parity (`opensoft/xFactory` CLAUDE.md, working rule 2) |

T061 never waits for T072, T071 or any later step (ARC-6; ARC-Q3 (a)).

## 10. Measured at filing: what the realization touches beyond plan 038's T074 `Files` line

Plan 038's T074 names the eight modules, the seam declarations, the 7 tests,
`tests/test_dependency_direction.py`, `tests/declared_exclusion.yaml`,
`tests/conftest.py`, `.github/workflows/composed.yml` and, if ARC-6 needs it,
`pyproject.toml`. At openXdox-code `56e1c238`, seven files name the arc as
the pending cause (15 occurrences of `plan 034('s)? T008` or `direction arc`).
This command lists them:

    git grep -lE "plan 034('s)? T008|direction arc" 56e1c238 -- src/ tests/ scripts/ .github/

Six of the seven are outside that `Files` line (`tests/declared_exclusion.yaml`
is the one inside it):

- **`.github/workflows/validate.yml`.** The help-tree `--deselect` (`LEFT_OUT`,
  `:161-164`) and its notes (`:97`, `:111`) are here. `composed.yml` does not
  exist yet (T029 creates it). Removal 1 of § 7 lands in whichever workflow
  carries `LEFT_OUT` at T074's base.
- **`tests/integration/test_assembled_surface.py`.** Removal 2 of § 7 (`:257`;
  its notes at `:70`, `:260`).
- **`src/openxdox/column_contributions.py`.** Its `_why_not_importable()`
  (`:164-179`) answers "`gate_console` imports `doc_health`" and keeps
  openXdox's four governed columns unregistered where it cannot import. After
  T074 `gate_console` always imports, so that reason never fires. D4 decides
  what replaces it.
- **`tests/test_column_contributions.py`.** It pins that reason's text
  (`:245-246`).
- **`src/openxdox/projection_contributions.py`.** Its docstring (`:59-70`)
  explains its use-time adapters by the `doc_health` import. The behaviour
  stands; the explanation changes.
- **`tests/test_declared_exclusion.py`.** It carries the `open_until` value
  "the doc_health direction arc (plan 034 T008)" (`:1093`, `:1097`, `:1101`),
  as `tests/declared_exclusion.yaml` does (`:68`, `:72`, `:76`). Those values
  are T073's to rewrite for the rail and contracts reasons, and T074's for the
  `doc_health` reason.

This packet records these files. Amending plan 038's T074 `Files` line is the
holder's act. The realization edits them under this change's ratification.

## 11. Decisions put for the ratify read

Each lists the recommendation first, then the alternative and its cost.

**D1. No openXdox-spec delta; `skip_specs: true`** (§ 5).
*Alternative:* an ADDED requirement in openXdox-spec declaring the four
seams. *Cost:* the first spec-leg text for a registration seam anywhere in the
estate, written for a surface whose six siblings carry none, and a bundle
question (plan 038's Principle VI row) for a change ARC-1 ruled `implemented`.

**D2. Every seam is read at USE, never at import** (§ 4.2).
*Alternative:* openXdox re-declares the three constants as its own values,
with a composed test that they equal the governed ones. *Cost:* a second
definition of governed values (the lifecycle header window, the governed
roots), which ARC-Q1 (a) routes through seams, and which can drift between
composed runs.

**D3. An unregistered seam refuses by name** (§ 4.2).
*Alternative:* an empty seam answers a neutral default. *Cost:* a governed
operation in an unhosted process would answer as if the corpus were empty, the
lie `corpus-adapter-seam`'s second requirement refuses.

**D4. A lone checkout's governed columns are keyed on the governed seams**
(§ 10).
- **(a) (Recommended)** `column_contributions.register()` writes openXdox's
  four governed columns only where the governed seams are registered.
  Elsewhere it writes nothing, `SKIPPED` names the empty seams, and openDox's
  defaults stand at the four column seams, as they do today. The host fills
  the governed seams before its column call and takes them back if that call
  refuses (§ 4.3). *Consequence:* a lone
  checkout behaves as it does today, and the ruled T086 Q1 (a) purpose (the
  four registered together, only where they can work) holds with its cause
  updated.
- **(b)** The four register wherever openXdox registers, and a governed
  operation refuses at the empty seam. *Consequence:* a lone checkout loses
  openDox's usable defaults at the four columns, in exchange for a refusal.

**D5. The surfaces check** (§ 8): F11.1's guard re-selected by this change's
trailer and filing base, with `COMPOSITION_TESTS` and `ADMITTED_ARC_EDITS`
empty, plus the protected-suite oracle over this change's openXdox-code
landings.
*Alternative:* inherit #1144's two named lists. *Cost:* paths admitted by
name for #1144's phases would be admitted here without a ruling.

**D6. The staged topic stays staged until T077, as this change's `staged`
origin.** `.openspec.yaml` declares `kind: staged`, because an organized
source exists and ad hoc "is never a substitute when organized source material
exists" (`docs/document-lifecycle.md:436-438`). The folder stays in place, as
`split-openxwallet-repo` and `split-opendox-two-layer-product` left theirs, and
T077 exits it.
*Alternative:* move the fragment into `supporting-docs/` now. *Cost:* T070
would edit the staging folder and its INDEX row, which plan 038 gives to T077.

**D7. The host fills openXdox's four seams as their own all-or-none group**
(§ 4.3).
*Alternative:* fold them into the existing all-or-none check of openDox's six.
*Cost:* a leg pair with openDox's six and none of openXdox's four (every pin
before T074) would be refused as a partial leg.
