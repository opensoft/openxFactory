# Tasks: 033-add-consent-custody-rederivation-record

**Branch**: `033-add-consent-custody-rederivation-record`
**Lane**: opsXfactory-1
**Realizes**: openxFactory OpenSpec change `add-consent-custody-rederivation-record`,
§§ 0–5 of its 46-box list.

**HOW THE TWO LISTS RELATE.** The packet's `tasks.md` is the GOVERNED list and
this one is the EXECUTABLE list. Every `T###` below names the packet box or
architect answer it discharges. A packet box is TICKED only by the `T###` that
performs its act, in the same commit as that act's evidence (architect ruling
**032-Q5**; see `spec.md` § *Question-set naming convention*). Where this file and the packet differ, the packet governs.

**BOX ACCOUNTING, and it must sum to 46.**

| Class | Count | Boxes |
| --- | --- | --- |
| TICKED here | 35 | 0.1; 1.1–1.3; 2.1–2.5; 3.1–3.5 (incl. 3.4b, 3.4c); 4.1–4.9 (incl. 4.1b, 4.1c, 4.3b, 4.3c, 4.8b, 4.8c, 4.8d); 5.2, 5.3, 5.4 |
| NOT-OWED-HERE | 3 | 5.1 (lane claims the number), 5.5 (lane's landing bookkeeping), 5.6 (`[OPERATOR]` tag) |
| NOT-OWED | 8 | 6.1, 6.2, 6.2b, 6.3, 6.4; 7.1, 7.2, 7.3 |
| **Total** | **46** | |

`[P]` = parallelizable with its siblings (different files, no ordering
dependency).

**THIS FILE'S OWN BOXES WERE TICKED 2026-09-09T20:31Z, ON THE REFUTATION PANEL'S
FINDING R4, AND THEY ARE A SECOND LIST.** The packet's 46 boxes are the GOVERNED
list and their tick discipline is proven from history at
`evidence/phaseH-T083-tick-audit.txt`. These 79 `T###` boxes are the EXECUTABLE
list; realization ticked the packet's and left these standing, which made the
feature tree read as untouched work. Each is ticked with a dated one-line
pointer naming its phase, its commit and its evidence transcript — a POINTER,
not a second proof, since the act each one names is the same act the packet box
beside it already evidences. **77 ticked + 2 NOT-OWED-HERE (T065, T066, which
mirror boxes 5.5 and 5.6 — the lane's and the operator's) = 79.**

**TWO DISCIPLINES BIND EVERY TASK BELOW AND ARE NOT REPEATED ON EACH ONE.**
(1) **Every phase gate files a RAW transcript** to `evidence/` — the command
line, the summary line and the process's own return code, captured, never
paraphrased. Piping a run through `tail` returns `tail`'s exit code and pushes
the summary line out of the window, so a run captured that way proves nothing
(FR-042a/b). (2) **Every negative fixture is ISOLATED**: sound in every leg
except the one it is named for, because `self_test`'s `codes_of()` only requires
the expected code to be PRESENT, not exclusive (FR-021a).

---

## Phase A — the Speckit tree

- [x] **TICKED 2026-09-09 · Phase A, committed before realization; `speckit-analyze` reached ZERO.** **T001** `spec.md` written and the twelve clarify answers applied.
      *(done at STOP A + the answer pass)*
- [x] **TICKED 2026-09-09 · Phase A, committed before realization; `speckit-analyze` reached ZERO.** **T002** `clarify-questions.md` carries all twelve answers inline plus
      A1 and A2. *(done)*
- [x] **TICKED 2026-09-09 · Phase A, committed before realization; `speckit-analyze` reached ZERO.** **T003** `plan.md` written, **including THE LANDING CONTRACT** (Q1).
      *(done)*
- [x] **TICKED 2026-09-09 · Phase A, committed before realization; `speckit-analyze` reached ZERO.** **T004** `research.md` written — R1..R14, every figure with its command.
      *(done)*
- [x] **TICKED 2026-09-09 · Phase A, committed before realization; `speckit-analyze` reached ZERO.** **T005** This file.
- [x] **TICKED 2026-09-09 · Phase A, committed before realization; `speckit-analyze` reached ZERO.** **T006** `speckit-checklist` no-arg: one checklist per requirement-quality
      domain the feature touches, release-gate rigor, no item cap. Run each and
      tick it.
- [x] **TICKED 2026-09-09 · Phase A, committed before realization; `speckit-analyze` reached ZERO.** **T007** `speckit-analyze` loop to ZERO findings, re-running after every
      fix.

## Phase B — § 2, the schema

**File**: `contracts/schemas/consent-instrument.schema.yaml`. One commit.

- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T010** *(box 2.1)* Add the top-level `custody_rederivations` property:
      `type: array`, items `type: object`, `additionalProperties: false`,
      `required: [at, commit, previous_locator, observed_locator,
      previous_sha256, observed_sha256, diff_class, reason, ruling_ref,
      recorded_by]` — TEN, in that order.
- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T011** *(box 2.1)* Field shapes exactly: `at` `type: string,
      format: date-time`; `commit` `pattern: "^[0-9a-f]{40}$"`; both locators
      `type: string, minLength: 1` with **no path grammar**; both digests
      `pattern: "^[0-9a-f]{64}$"`; `diff_class`
      `enum: [path_only, header_only, content]`; `reason`
      `enum: [lifecycle_header_edit, archive_move, other_ruled_edit]`;
      `ruling_ref` and `recorded_by` `type: string, minLength: 1`.
- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T012** *(box 2.3)* `contract_schema_version: 2` → `3`, with an in-file
      comment in the style of the existing `1 -> 2` note: what grew, that it is
      ADDITIVE, and that the record envelope's `schema_version` stays `const: 1`
      because moving it would invalidate every instrument in the estate.
- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T013** *(box 2.4)* In-file comment on the new property: WHY it is a
      SIBLING (ruling D9's closure argument, design C-1) and that `ruling_ref`
      is a DECLARED POINTER the validator does not resolve — the
      `dependent_refs.ref` posture.
- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T014** *(box 2.5)* In-file comment on the locator pair: `custody.locator`
      is OPAQUE and is NOT a path (C-6a); resolution runs through the consuming
      repository's DECLARED custody store mapping; the two legs are evaluated on
      opposite sides of the commit; an archive move is unadmittable without the
      pair. **Name the measurement** — every OpsxFactory locator carries an
      `opsx:opensoft/` scheme prefix and three of four targets resolve at no ref
      under their literal path.
- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T015** *(box 2.2)* **PROVE `custody` IS UNTOUCHED**: `git diff` over the
      file shows ZERO changed lines inside the `custody` object — its two
      properties, its `required`, its `additionalProperties: false` and its
      comment block byte-identical. Transcript to `evidence/`. **A diff touching
      `custody` fails this task.**
- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T016** *(Q4)* Confirm by diff that `$id`, the record envelope's
      `schema_version: const: 1` and the manifest row's `schema_version: 1` are
      all unmoved.
- [x] **TICKED 2026-09-09 · Phase B, commit `f59a587d`; evidence/T015-T016-schema-proofs.txt, T017-manifest-digests.txt.** **T017** *(clarify Q5, AS REVISED BY PANEL F2)* **RE-DERIVE the
      `consent-instrument` row's `sha256` in THIS COMMIT**, from the moved file,
      by `sha256sum`. A per-file digest is INTEGRITY BOOKKEEPING FOR THE EDITED
      FILE, not a release surface — policy step 2's atomicity concerns VERSION
      IDENTITY — so the commit that makes it stale is the commit that closes it.
      **No commit on this branch is left with a stale digest and no deviation is
      declared**; `validate-manifest-digests.py` is green at every commit, and
      the commit message says which row moved and why it moved HERE rather than
      at the cut.

## Phase C — § 3, the canonical validator

**File**: `scripts/validate-consent-instruments.py`. Codes adopted verbatim
(Q10).

- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T020** *(box 3.1)* A new check beside `check_custody` for the chain's
      INTERNAL legs, with DISTINCT codes per leg:
      - `custody-chain-unanchored` — `e₁.previous_sha256 != custody.sha256`
        **OR** `e₁.previous_locator != custody.locator` (BOTH halves);
      - `custody-chain-broken-link` — `eᵢ.previous_sha256 !=
        eᵢ₋₁.observed_sha256`;
      - `custody-chain-locator-gap` — `eᵢ.previous_locator !=
        eᵢ₋₁.observed_locator`;
      - `custody-chain-out-of-order` — `at` decreasing in declared order.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T021** *(box 3.2)* `custody-pin-rewritten` — refuse an instrument whose
      `custody.sha256` equals any entry's `observed_sha256` while a LATER entry
      exists, and more generally any state in which the pin has been advanced to
      a value the chain itself records as observed.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T022** *(box 3.4c)* `custody-path-class-digests-differ` — a `path_only`
      entry whose `previous_sha256 != observed_sha256` is refused.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T023** *(box 3.4b, Q2)* **MINT THE WITHHELD OUTCOME.** Add
      `custody-content-class-withheld` as a DISTINCT outcome on `Findings` —
      not an error, not a warning. A `content`-class entry with sound internal
      legs yields it.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T024** *(box 3.4b; clarify Q2, RULED)* **THE EXIT STATUS — `3`, on
      Brett Heap's word.** Define a single module constant
      `EXIT_NEEDS_DECISION = 3` and return it from `report()` when a REAL
      instrument withholds and nothing errors. Extend the module docstring's
      line to **`Exit codes: 0 ok, 1 findings, 2 dependency/harness error, 3
      withheld — needs a human decision`** — exit 2 KEEPS its ratified wording
      *"dependency/harness error"*; do not narrow it to *"harness error"*
      (panel F10), **in this script only**, and state the
      PRECEDENCE on the next line: **`errors dominate — an instrument that both
      withholds and errors exits 1, because a malformed record is not a decision
      for a human to take`** (architect ruling, 2026-09-09, CONFIRMED). At the constant, cite
      the ruling: Brett Heap, 2026-09-09, in session, first-hand to lane
      `opsXfactory-1`, by multiple-choice selection, verbatim **"Exit 3 = needs
      a human decision (Recommended)"**, over the declined *"Exit 1, same as
      findings"* and *"Exit 0, report only"*; recorded by this lane at
      `2026-09-09T14:40:16Z`. **Say in the comment that this IS the repository
      rule ratified task 3.4b asked for** — the repository had ruled none before
      it. **The PACKAGED withheld fixture is EXEMPT** — an expected withholding
      is to the third bucket what an expected failure is to a negative — so the
      self-test still exits `0`.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T025** *(box 3.4)* The report line for a chained instrument states what
      was checked and what was NOT, so a neutral pass is unreadable as a
      currency verdict (promoted scenario *The neutral pass is not a currency
      claim*). WITHHELD is named beside the error and warning counts.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T026** *(box 3.5, Q12)* **EXTEND `walk_strings` OVER THE ENTRY** — the
      whole entry MINUS the two digest fields (`previous_sha256`,
      `observed_sha256`), so both locators, `ruling_ref` and `recorded_by` are
      walked and `commit` / `at` / `diff_class` / `reason` ride along already
      bounded. Reuse `BASE64_BLOB_RX`, the `data:` prefix, `PDF_MAGIC_RX`, the
      multi-line predicate and the `embedded-original-content` code.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T027** *(box 3.3)* **NO GIT RE-DERIVATION IS ADDED.** The module opens no
      repository, shells out to no `git`, and reads no file named by a locator.
- [x] **TICKED 2026-09-09 · Phase C, commit `f420cd50`; evidence/phaseC-exit-vocabulary.txt.** **T028** *(box 3.4b)* `self_test` grows the THIRD expectation bucket
      (built at T045/T046); `repo_scan` reports WITHHELD as found (Q3b) and needs no
      bucket discipline.

## Phase D — § 4, the fixtures

**Directories**: `examples/consent-instrument/`, `.../negative/`, and a NEW
`.../withheld/` (Q3a).

### Positives `[P]`

- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T030** *(box 4.1)* A two-entry unbroken chain, `header_only` /
      `lifecycle_header_edit`, admitted by the internal legs.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T031** *(box 4.1b)* An `archive_move` / `path_only` entry whose locator
      pair DIFFERS and whose digests are EQUAL on both sides — design C-6a,
      `proposal.md` Example B.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T032** *(box 4.1c; FR-020's equal-timestamp clause)* The TWO-ENTRY shape
      the real repair needs: e1 `archive_move`/`path_only`, e2
      `lifecycle_header_edit`/`header_only`, modelled on prescription I in
      `design.md` § *The consumer handoff*.
      **THIS FIXTURE CARRIES THE EQUAL-TIMESTAMP BOUNDARY**, and it is the right
      one to carry it: the two entries record ONE repair session, so an author
      writing both at the same recording moment is the realistic case rather
      than a contrivance. Give `e1.at == e2.at` and assert the instrument is
      ADMITTED — the requirement says the times *"do not decrease"*, so equality
      is legal and an untested boundary is an untested rule. T036 is its
      negative twin and must strictly DECREASE.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T033** *(box 4.2)* An EXISTING example left **byte-unchanged** and
      re-validated, proving the growth is additive for an instrument declaring
      no array. Evidence: the diff shows the file untouched and the self-test
      still passes it.

### Negatives, one per named refusal `[P]`

- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T034** *(box 4.3)* Broken digest link → `custody-chain-broken-link`.
      **Locator pair sound**, so the fixture tests the digest half alone.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T035** *(box 4.3b)* Locator gap with digests linking correctly →
      `custody-chain-locator-gap`.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T036** *(box 4.3c)* Entries out of recorded-time order →
      `custody-chain-out-of-order`. **Both digest and locator legs sound**, so
      only the ordering is under test. Equal timestamps are ADMITTED, so the
      fixture must DECREASE, not merely repeat.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T037** *(box 4.4)* TWO fixtures: a first entry whose `previous_sha256`
      is not the pin, and one whose `previous_locator` is not `custody.locator`
      → `custody-chain-unanchored` both, detail-pinned so each tests its own
      half.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T038** *(box 4.5)* TWO fixtures: an unknown `diff_class` member and an
      unknown `reason` member → `schema`, each detail-pinned on its field.
      **The FIVE `schema`-coded fixtures (T038, T039, T040) must carry MUTUALLY
      EXCLUSIVE detail substrings** — the self-test only checks that a
      registered detail appears somewhere in that fixture's errors, so two
      overlapping substrings would let one fixture satisfy another's assertion.
      Choose the substrings, then prove the exclusivity by cross-checking each
      against every other fixture's error text.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T039** *(box 4.6)* TWO fixtures: an entry omitting `ruling_ref` and one
      omitting `recorded_by` → `schema`, each detail-pinned.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T040** *(box 4.7)* An entry carrying an **ELEVENTH** property → `schema`,
      detail-pinned on `additionalProperties`. (Entry closure has TEN required
      fields since C-6a, so a "ninth" would not test closure at all.)
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T041** *(box 4.8)* A rewritten pin — `custody.sha256` advanced to an
      observed digest while the chain still claims the original anchor →
      `custody-pin-rewritten`. **MULTI-ENTRY chain, not single**: FR-011's
      sharper form is the pin advanced to an entry's `observed_sha256` *"while a
      LATER entry exists"*, and a one-entry fixture exercises only the general
      form.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T042** *(box 4.8b)* TWO fixtures: a blob-shaped `ruling_ref` and a
      blob-shaped `recorded_by` → `embedded-original-content`. **This is the
      fixture pair that proves T026 landed.**
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T043** *(box 4.8d)* A `path_only` entry whose two digests differ →
      `custody-path-class-digests-differ`.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T044** Every new negative registered in `EXPECTED_NEGATIVE_FINDINGS`
      with a detail substring wherever the code alone is too coarse (`schema` is
      satisfied by any schema error — the existing rule).

### The third bucket

- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T045** *(box 4.8c, Q3a)* Create `examples/consent-instrument/withheld/`
      and the WITHHELD fixture: an instrument whose LAST entry declares
      `diff_class: content` and whose internal legs are ALL SOUND. **Asserted as
      WITHHELD — not a pass and not an error.**
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T046** *(box 4.8c, Q3a)* `self_test` grows `EXPECTED_WITHHELD_OUTCOMES`,
      **fail-closed BOTH ways** exactly as `EXPECTED_NEGATIVE_FINDINGS` is: a
      fixture on disk with no table entry and a table entry with no fixture are
      each errors. **AND it must check the OUTCOME, not just the file**: the
      analogue of `negative-wrong-reason`. A withheld fixture that ERRORS, or
      that passes cleanly, is a self-test failure — "the fixture exists" is not
      "the fixture withholds". The self-test note reports THREE bucket counts.

### Corpus counts

- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T047** *(box 4.9, Q9)* `examples/consent-instrument/README.md`:
      Layout tree COMPLETE over the grown corpus; *Schema → example map* table
      complete **with a THIRD column for the withheld bucket**; *Named cases
      from the spec* grows **one bullet per refusal code (7) + one positive
      chain-shapes bullet + one withheld bullet**; counts RE-MEASURED by
      listing the directories, never by arithmetic. **THE SEVEN REFUSALS ARE NOT
      Q10's SEVEN CODES** — Q10's list contains `custody-content-class-withheld`,
      which already has its own bullet, so the seven are the six that refuse
      (`custody-chain-unanchored`, `custody-chain-broken-link`,
      `custody-chain-locator-gap`, `custody-chain-out-of-order`,
      `custody-pin-rewritten`, `custody-path-class-digests-differ`) plus
      **`embedded-original-content` under its newly extended reach**.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T048** *(box 4.9)* `contracts/manifest.yaml`'s `consent-instrument`
      corpus comment (*"5 valid + 5 invalid + purpose probes"*) RE-MEASURED.
      **It is already false at 6/7 before this feature adds a byte** — do not
      increment it, re-count it.
- [x] **TICKED 2026-09-09 · Phase D, commit `f420cd50`; evidence/phaseD-consent-validator.txt.** **T049** *(clarify A1 — named by NO ratified task)* `contracts/README.md`'s
      row for `scripts/validate-consent-instruments.py` +
      `examples/consent-instrument/` reads *"self-testing over 5 positives, 5
      indexed negatives, and 2 purpose probes"*. RE-MEASURE it over the three
      buckets. Carried as an ADDITIONAL realization act, not as a renumbering of
      the ratified list.

## Phase E — `tests/consent_instruments/` (Q7)

- [x] **TICKED 2026-09-09 · Phase E, commit `f420cd50`; evidence/phaseE-pytest-consent-instruments.txt, phaseE-pytest-full.txt.** **T050** *(box 3.3, Q7c — SCOPED PER PANEL F3)* **Source-level no-git
      ban**, argument-scoped because the naive form is unimplementable: assert
      the module does NOT `import subprocess`, contains no `subprocess.` /
      `os.system` / `os.popen` call, and contains no `git` COMMAND token.
      **ALLOWLIST THE EXACT TOKEN `".git"` in `SKIP_DIR_NAMES`** (validator
      line 735): it is a DIRECTORY-NAME EXCLUSION that makes the tree walk skip
      a git directory — the opposite of reading one — and a naive `git` grep
      would red forever on it. The allowlist is by exact token, not by
      substring.
- [x] **TICKED 2026-09-09 · Phase E, commit `f420cd50`; evidence/phaseE-pytest-consent-instruments.txt, phaseE-pytest-full.txt.** **T051** *(box 3.3, Q7c — SCOPED PER PANEL F3)* **Runtime assertion**, in
      two argument-scoped halves, because "reads no file" is false of a
      validator that must read its own corpus:
      (a) patch `subprocess.run`, `subprocess.Popen` and
      `subprocess.check_output` and assert **NONE is called**;
      (b) wrap `Path.open` and `open` and assert **every path opened resolves
      UNDER the corpus root passed to the run**. That is the checkable form of
      "reads no locator target": a locator names a file in a CONSUMER
      repository, so any open resolving outside the corpus root fails.
      Exercised over **ALL THREE buckets** — positive, negative and withheld —
      since the withheld leg is the one most likely to reach for a repository.
- [x] **TICKED 2026-09-09 · Phase E, commit `f420cd50`; evidence/phaseE-pytest-consent-instruments.txt, phaseE-pytest-full.txt.** **T052** *(box 3.5, Q7b)* **Parametrized blob-walk test** proving the walk
      reaches each of the four free strings (`previous_locator`,
      `observed_locator`, `ruling_ref`, `recorded_by`).
- [x] **TICKED 2026-09-09 · Phase E, commit `f420cd50`; evidence/phaseE-pytest-consent-instruments.txt, phaseE-pytest-full.txt.** **T053** *(clarify Q2, RULED; precedence CONFIRMED 2026-09-09)* A test pinning the WITHHELD exit status:
      the named constant equals `3`; a REAL withholding instrument exits `3`;
      the PACKAGED self-test exits `0`; and an instrument that both withholds
      AND errors exits `1`. **The precedence is CONFIRMED by the architect
      (2026-09-09), not inferred**: errors dominate, because a malformed record
      is not a decision for a human to take. All three exits asserted, and the
      assertion NAMES the precedence, so a later reader cannot read exit 1 there
      as a bug.
- [x] **TICKED 2026-09-09 · Phase E, commit `f420cd50`; evidence/phaseE-pytest-consent-instruments.txt, phaseE-pytest-full.txt.** **T054** `python3 -m pytest tests/consent_instruments -q` green, and then
      the full `python3 -m pytest tests/ -q -m "not postgres"` green.

## Phase F — Q8's README amendments  ✅ UNBLOCKED 2026-09-09

- [x] **TICKED 2026-09-09 · Phase F, commit `7c79f524`; evidence/phaseF-readme-amendments.txt.** **T055** **RESOLVED 2026-09-09 — PHASE F IS UNBLOCKED.** The lane posted
      the row-3 substrate note at [#630 comment 5603344475](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5603344475), covering the
      two SIBLING-row sentences (`README.md:3022`, `README.md:2993`), this
      change's own Records row, AND `contracts/README.md:102`. **Every
      amendment's dated clause CITES THAT COMMENT.** The text below is retained
      as the record of what was waited on, not as a live condition.
      *(Historical, discharged.)* The LANE had to post the row-3 substrate note
      on openxFactory issue #630 for the two SIBLING-row sentences before T057
      and T058 could be written. This packet's own row (T056) rides its standing row-3
      claim `5571680388` (2026-09-07). **Do not write T057/T058 until the note
      exists; report the block instead.**
      **CHANNEL AND CADENCE, stated rather than left to inference.** Posting is
      a LANE act, exactly as § 5.1's version claim is — this seat opens no pull
      request and posts no comment. The orchestrator does NOT poll: it RE-CHECKS
      whether the note has arrived at **each merge-from-main**, the same cadence
      the version re-measurement runs on (T060), and reports the state each time.
      **TERMINAL DISPOSITION if it had never arrived** *(retained as the rule,
      now moot)*: T056 taken regardless; T057/T058 taking a dated
      `REPORTED, NOT PERFORMED` line naming the block. It arrived, so the live
      instruction is: write all three amendments, each citing the comment above
      in its dated clause.
- [x] **TICKED 2026-09-09 · Phase F, commit `7c79f524`; evidence/phaseF-readme-amendments.txt.** **T056** *(Q8a-1)* Amend this packet's own OpenSpec Records row —
      *"**all 46 boxes in `tasks.md` stay unticked**"* — in the `3b530009` form:
      block-quote the superseded sentence, name the un-superseded neighbour,
      marker `AMENDED 2026-09-09`.
- [x] **TICKED 2026-09-09 · Phase F, commit `7c79f524`; evidence/phaseF-readme-amendments.txt.** **T057** *(Q8a-3)* Amend `README.md:3022`'s present-tense box count, same
      form. **KEEP *"the three pins are still broken"*** — that half stays true,
      because the repair is § 6 and § 6 is the consumer's.
- [x] **TICKED 2026-09-09 · Phase F, commit `7c79f524`; evidence/phaseF-readme-amendments.txt.** **T058** *(Q8a-5, the load-bearing one)* Amend `README.md:2993` inside the
      `govern-archived-record-edits` row: *"the consent family's is PROPOSED
      only (`contract_schema_version: 2`, no `custody_rederivations` property,
      `contract-v3.4`, 46/46 boxes unticked)"* — **false on all four counts
      after this lands**, and the premise of that rule's TRANSITION CLAUSE.
- [x] **TICKED 2026-09-09 · Phase F, commit `7c79f524`; evidence/phaseF-readme-amendments.txt.** **T059** *(Q8a-2, Q8a-4)* **LEAVE** the past-tense *"left its 46"*
      (**`README.md:2949–2950`** — the sentence SPANS both lines, which is why
      the ruling said 2949 and the earlier measurement said 2950; both are
      right about their own half) and the dated *"measured 2026-09-09 UTC at
      `main` `6cc06288`"* (`README.md:3098–3100`) as TRUE-WHEN-WRITTEN. Record
      the decision; do not edit them.
      **ALL FOUR sibling sentences sit in ONE README row** — the
      `govern-archived-record-edits` OpenSpec Records entry, `README.md:2854–3101`
      — so T057, T058 and this task are three edits to a SINGLE row, not to
      three rows, and the substrate note covers the row once (panel F9).

## Phase G — § 5, THE CUT (LAST)

**RE-CUT 2026-09-09 AS `contract-v3.6`. EVERY `contract-v3.5` SPELLING IN THIS
PHASE IS THE WITHDRAWN RECORD, KEPT IN PLACE RATHER THAN DELETED.** Brett Heap
ruled 2026-09-09T22:11Z, selected option verbatim *"#866 first, I re-cut as v3.6
(Recommended)"*; openxFactory PR #866 landed as `a37ae0cd` at 21:47:48Z and he
published the annotated tag `contract-v3.5`. Candidates `d54d89ca` and its remake
`e9a688d3` declared `contract-v3.5`, were never published, and are WITHDRAWN — an
audit also found three defects in the remake (a RED `release-tag-gate` misread
from a transcript header, two unattributed `NORMATIVE_DOCS` inventory members, and
a candidate that was not atomic). So read every box below against these live
values: the number is **`contract-v3.6`**; the integration point is **`fee36588`**
(`origin/main@17167481` merged in); the enum member is **`FEATURE_SUCCESSOR_10 =
"contract-v3.6"`**; the built inventory is
**`contracts/releases/contract-v3.6.digests.yaml`**, 283 entries; and the
attribution is an INVENTORY DIFF over all 283 members (four moved, one of them
outside `contracts/`), not a `git diff -- contracts/`.

**RE-FORMED 2026-09-09 AFTER AN ADVERSARIAL AUDIT. `d14b514f` IS ALSO WITHDRAWN,
AND `evidence/phaseI-recut-v3.6-*.txt` IS ITS RECORD, NOT THE LIVE ONE.** An Opus
adversarial audit (lane `opsXfactory-1`) read that candidate on twelve items and
failed exactly one: `contracts/CHANGELOG.md:33` said *"The candidate is its own
DECLARING commit and the branch tip, so the release-tag gate's first-parent
declaring distance is **zero**."* — true when written, false once `89a7c0de`,
`e6da37fa` and `3119f9ae` stacked above it, and shipped INSIDE the bundle because
`contracts/CHANGELOG.md` is a pinned inventory member. `31772616` withdrew the
release surface to `fee36588`'s exact bytes and the candidate was RE-FORMED, not
patched (**FR-034a**). The bundle number, the integration point, the enum member,
the built inventory and the attribution above are all UNCHANGED by the re-form;
the only bytes that moved are three prose hunks in the `## contract-v3.6` entry
and the CHANGELOG's own digest in the rebuilt inventory. Live transcripts:
`evidence/phaseJ-reform-*.txt`.

**One candidate commit** (Q5a, policy step 2). Taken only after Phases B–F.

- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T060** *(box 5.1's MEASUREMENT — the CLAIM is the lane's)* Fetch,
      integrate onto the final integration point, then **RE-MEASURE** the next
      additive minor on all three surfaces (`contracts/manifest.yaml:3`,
      `contracts/releases/`, `git tag -l 'contract-v*'`) — **and RE-MEASURE THE
      BUNDLE'S OWN CONTENTS**, `git diff --name-status contract-v3.4 HEAD --
      contracts/` **at the candidate commit** (`git diff --name-status
      contract-v3.4 <candidate> -- contracts/`). `research.md` R6's
      4-added/14-modified list was measured at BRANCH CREATION and moves every
      time another lane lands, so **T062 is written from THIS measurement and
      never from R6** (FR-032, panel F7). Report both to
      the lane. **Both are re-measured at EVERY merge-from-main.** Do not post
      the claim.
- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T061** *(box 5.2)* `contracts/manifest.yaml`, ALL THREE edits in this
      one commit: `contract_bundle_version` → the allocated version; the
      `consent-instrument` row's `sha256` **re-derived by `sha256sum`** from the
      moved file (closing T017's deliberate staleness); and a NEW
      `consumption_rule` paragraph in the `contract-v1.33` style — what grew,
      that it is ADDITIVE, that the envelope stayed `const: 1`.
      **INSERT IT BEFORE THE CLOSING SENTENCE, not after.** The rule's shape is
      [summary] → [`Registered at contract-v1.30; digest refreshed at
      contract-v1.33 …`] → [*"Consumed through the pinned openxFactory checkout
      with per-file sha256 verified before any copy is treated as current."*].
      The v1.33 paragraph sits BETWEEN the registration line and that closing
      sentence; the v3.5 paragraph goes in the same slot, after it.
      **`consent-instrument-class-registry`'s row is untouched.**
- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T061a** *(panel F1 — RE-MEASURE THE COUPLING, do not copy it)* Take
      `git show --stat --format='' 807a4f47` — the `contract-v3.4` cut — and
      read what a cut ACTUALLY moves. Measured at this branch: **SIX files**,
      not four — `contracts/CHANGELOG.md`, `contracts/README.md`,
      `contracts/manifest.yaml`, `contracts/releases/contract-v3.4.digests.yaml`,
      `tests/clearing/test_clearing_manifest_rows.py` and
      `tests/intent-compliance/test_release_boundary.py`. Derive the
      bundle-version-coupled edit set FOR THIS CANDIDATE from that measurement
      and record it in `evidence/`. **These are DECLARED cut-coupled acts
      attributed to the cut, not invented scope.**
- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T061b** *(panel F1)* `tests/intent-compliance/test_release_boundary.py`
      — the tripwire that would otherwise red T064's full-suite gate.
      `_release_state()` **fails LOUDLY on a bundle the enum does not name**, so
      moving `contract_bundle_version` without this edit reds the required
      suite. Three edits, mirroring what `807a4f47` did:
      (i) a new enum member `FEATURE_SUCCESSOR_9 = "contract-v3.5"` beside
      `FEATURE_SUCCESSOR_8` (line 115);
      (ii) the member added to **BOTH** match arms (lines ~207 and ~244) —
      there are TWO, and missing either hits `assert_never`;
      (iii) the **hand-written "what this cut moved" paragraph** in the enum's
      docstring, in the register the file already uses: what this bundle
      carries, and whether any intent-compliance member's bytes moved —
      **MEASURED against `contract-v3.4`'s inventory, never asserted**, because
      the file's own comment says *"unchanged" is the one fact the library
      cannot tell from "unnoticed"*.
- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T061c** *(panel F1)* `tests/clearing/test_clearing_manifest_rows.py` —
      **MEASURE whether it needs an edit; do not assume either way.** The
      expected answer is NO EDIT, and the reason is recorded in the file itself:
      `807a4f47` REPAIRED its bundle-version equality precisely so it would not
      need re-pinning again, *"rather than re-pinned to a number that would fail
      again at `contract-v3.5`"*. Its live assertions are that the declared
      bundle is NEVER BEHIND the rows' registering release, that both have an
      inventory beside them, and (line 95) that no row's `consumption_rule`
      mentions `contract-v3.5` — all satisfied by a v3.5 cut that creates the
      inventory and leaves the clearing rows alone. **Run it against the
      candidate and record the result**; if it does red, it is a cut-coupled
      edit and belongs in the same candidate commit.
- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T062** *(box 5.3, Q6)* `contracts/CHANGELOG.md` entry naming **what
      changed in the BUNDLE, not what this session intended**: all **4 additions
      and 14 modifications** under `contracts/` since `contract-v3.4`
      (`research.md` R6), each attributed to its originating change/PR —
      including the `publish-openspec-cli-pin-as-contract-member` **A-defer**
      registration that this bundle is what finally publishes. **Change class:
      ADDITIVE (minor)** — and **argue it over the WHOLE bundle, not only this
      session's schema.** The additions are additive by construction; **each
      MODIFICATION to an already-published contract must be checked
      INDIVIDUALLY** for a removed field, a narrowed enumeration or a newly
      required property, which is what the `contract-v3.4` entry did clause by
      clause. This session's own leg of that argument: one new optional
      property, one `contract_schema_version` bump, nothing removed, no
      enumeration narrowed, every existing instrument valid unchanged.
- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T063** *(box 5.2)* `contracts/releases/<version>.digests.yaml`
      **BUILT** by `python3 scripts/validate-contract-release.py build --tag
      <version> --output contracts/releases/<version>.digests.yaml`. **Never
      hand-edited.** Record the entry count and the delta against
      `contract-v3.4`'s 283.
- [x] **TICKED 2026-09-09 · Phase G, candidate `d54d89ca` — WITHDRAWN; RE-TAKEN 2026-09-09 at the `contract-v3.6` candidate `d14b514f` over the integration point `fee36588`, then RE-FORMED 2026-09-09 after the adversarial audit as **THIS COMMIT** (sha filed by the follow-up evidence commit) over the SAME integration point; evidence/phaseG-T060-measurement.txt, phaseG-T061a-T061c-coupling.txt, phaseG-T064-gates.txt (the withdrawn `d54d89ca` record), evidence/phaseI-recut-v3.6-*.txt (the withdrawn `d14b514f` record) and evidence/phaseJ-reform-*.txt (live record).** **T064** *(box 5.4, Q11)* Run **all five gates against the exact unchanged
      candidate**, transcripts to `evidence/`:
      `scripts/validate-release-tag-gate.py` **with an EXPLICIT
      `--base <main sha at the integration point>`** — its default resolves
      `--base` to the head's FIRST PARENT, right for a GitHub `pull_request`
      merge commit and WRONG for a candidate on a branch that integrated by
      merging `main` INTO it, where the first parent is this branch's own prior
      tip. The default would diff against the wrong tree and return a
      near-empty result that LOOKS like a pass;
      `python3 -m pytest tests/ -q -m "not postgres"`;
      `scripts/validate-manifest-digests.py`;
      `scripts/validate-contract-release.py verify-commit --commit <candidate>`;
      `scripts/validate-consent-instruments.py --strict`.
- [ ] **NOT-OWED-HERE 2026-09-09 — mirrors box 5.5 — the LANE's landing act under `plan.md`'s landing contract.** **T065** *(box 5.5)* **NOT-OWED-HERE.** Landing the exact reviewed commit,
      and the post-merge gate re-run the merge commit forces, are the LANE's
      under the landing contract in `plan.md`. Dated NOT-OWED line, no tick.
- [ ] **NOT-OWED-HERE 2026-09-09 — mirrors box 5.6 — an [OPERATOR] act at the LANDED MERGE COMMIT.** **T066** *(box 5.6)* **NOT-OWED-HERE.** The annotated tag and its
      independent verification are `[OPERATOR]` acts, targeting the LANDED MERGE
      COMMIT. Dated NOT-OWED line, no tick.

## Phase H — bookkeeping, evidence and the notes

- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T070** *(box 0.1)* TICK with evidence: commit `6cfe9ba6` re-stamped the
      ledger row to the real PR `#774`; the row reads
      `moved_by: "#774", moved_on: "2026-09-07"`; `--ledger-diff` reports the
      corpus consistent at 189 rows.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T071** *(box 1.1)* TICK with evidence: `review/ratification-2026-09-08.md`
      exists; `Status: ratified` on `proposal.md`, `design.md`, `tasks.md`; the
      `Ratified:` line present; the README Records row already flipped
      (`README.md:848`). **The citation states the MEASURED absence of a GitHub
      approving review** (`research.md` R12) and cites instead the in-repo
      record, Brett Heap's own merge (`merged_by brettheap`,
      `2026-09-08T03:48:44Z`, `543d47a9` over head `0d541576`) and his
      LANDING/LANDED comments.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T072** *(box 1.2)* TICK with evidence: the ratification record's *"no
      veto was exercised on any of the eleven"* rules all eleven veto points as
      written. Quote it exactly — never more.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T073** *(box 1.3)* TICK with evidence: the record's *"Task 1.3's operator
      veto was NOT exercised"* section, and the default that stands (no
      `amendments` entry; the three instruments stay `executed`).
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T074** *(architect rulings **032-Q1**/**032-Q10** form)* Amend the packet `tasks.md`'s
      ratified preamble in the `3b530009` form **in the same commit as the first
      tick**. **Superseded sentence**: *"NOTHING BELOW IS DONE. EVERY BOX IS
      UNTICKED, AND THAT IS THE STATE OF THE PACKET RATHER THAN AN OVERSIGHT."*
      **Un-superseded neighbour — NAMED HERE rather than left to execution-time
      judgement**: the same paragraph's closing clause *"no consumer pin
      advances, and no instrument takes an entry"*, which stays TRUE after this
      realization because those are § 6's acts and § 6 is the consumer's.
      Block-quote the superseded sentence, name that neighbour, marker
      `AMENDED 2026-09-09`, tick marker `**TICKED 2026-09-09`.
      **Each of T056–T058 CITES the substrate note
      [#630 comment 5603344475](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5603344475) in its dated clause**, and so does
      `contracts/README.md:102`'s correction (T049), which the same note
      covers.
      **T056–T058 name their own neighbours the same way**: for this packet's
      row, *"no consumer file is edited"*; for `README.md:3022`, *"the three
      pins are still broken"*; for `README.md:2993`, *"the register home
      `models/content-address-families.yaml` exists neither on OpsxFactory's
      `main` nor on the branch proposing it"*.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T075** Dated NOT-OWED lines on §§ 6.1, 6.2, 6.2b, 6.3, 6.4 and 7.1, 7.2,
      7.3 — named as owed elsewhere, performed nowhere here.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T076** **Note classes SUM TO 46**: 35 ticked + 3 NOT-OWED-HERE + 8
      NOT-OWED. Assert the arithmetic in the evidence file.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T077** *(architect ruling **032-Q10**)* ONE additive dated realization note after
      `proposal.md`'s `Lane:` line, correcting any ratified ENUMERATION this
      realization falsifies (the *"every box in `tasks.md` stays unticked"*
      sentence). **`design.md`, `.openspec.yaml` and the delta stay frozen.**
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T078** *(clarify A2 — state it, do not act on it)* A DATED note, in the
      realization evidence AND in the neighbourhood of § 7 in the packet's
      `tasks.md`, recording that landing this realization **DECLARES the consent
      family's re-derivation rule**, so under `govern-archived-record-edits`'
      transition clause an edit of a consent pinned target converts from
      **REPORTED** to **REFUSED** for that family **once F.2's gate exists**
      (§ 7.1, OpsxFactory's). **Build nothing, schedule nothing, tick nothing.**
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T079** *(architect ruling **032-Q4**)* Evidence in BOTH trees:
      `specs/033-add-consent-custody-rederivation-record/evidence/` and
      `openspec/changes/add-consent-custody-rederivation-record/evidence/realization-2026-09-09.md`.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T080** *(architect ruling **032-Q10**)* **doc-health TWO-REPORT COMPARISON.**
      `python3 scripts/doc-health.py --single-repo <checkout> --as-of <ONE
      pinned date> --report-out <dir>/doc-health.md`, run once against `main`
      and once against this branch. **The two `--report-out` basenames MUST BE
      IDENTICAL** and differ only in their directory, so the report's own
      self-reference cannot show up as a diff line and manufacture a finding
      difference that is really a filename difference. `--as-of` pinned to the
      same date on both, so a clock rollover between the runs cannot move an
      aging-class finding (the failure `specs/032`'s
      `doc-health-diff-INTERIM-superseded-clock-rollover.txt` records). The
      finding sets must be diff-identical at EVERY severity; both reports and
      the diff go to `evidence/`.
      **NAME THE BASELINE'S `main` SHA, and RE-TAKE IT IF `main` MOVES** before
      the final comparison — re-captured at the commit this branch last merged
      from, with BOTH shas recorded. A diff-identical comparison against a stale
      baseline is not a comparison.
      **The CHECKOUT DIRECTORY basenames must match too**, not only the report
      basenames: a path fragment differing between the two runs is a filename
      difference wearing a finding's clothes.
      **If the corpus growth itself trips a family** — a lifecycle-header or
      location-conformance scan reaching the new `withheld/` directory — that is
      a REAL finding this feature caused: fix it, or disposition it with a
      citation. Never wave it through as "expected, the corpus grew".
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T081** Final gate sweep at the branch head: pinned CLI
      `--change … --strict` **and** `--all --strict` (zero UNDISPOSITIONED
      failures); `validate-consent-instruments.py --strict` over the corpus;
      `validate-sequenced-after.py .` and `--ledger-diff`;
      `validate-scope-globs.py`; `validate-manifest-digests.py`;
      `pytest tests/ -q -m "not postgres"`. Transcripts to `evidence/`.
      **WHY THIS SWEEP IS NARROWER THAN T064's, stated so it reads as a choice.**
      It omits `validate-release-tag-gate.py` and
      `validate-contract-release.py verify-commit` because Phase H touches no
      path under `contracts/` — only `tasks.md`, `proposal.md`, `README.md` and
      `evidence/`. **VERIFY that premise rather than assume it**
      (`git diff --name-only <candidate>..HEAD -- contracts/` must be empty); if
      any Phase H commit did reach `contracts/`, the candidate is no longer the
      certified tree and BOTH release gates re-run here too.
      **A `pin-disposition-stale` refusal (exit 2) from `--all --strict` is a
      THIRD outcome**, distinct from a clean pass and from undispositioned
      findings: an accepted exception whose finding no longer occurs, usually
      because an unrelated change archived. It is corpus hygiene in a file this
      feature does not touch — REPORT it, do not silently repair it.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T084** *(architect ruling, 2026-09-09 — RECORD IT, DO NOT CLOSE IT)*
      **THE IDENTICAL-LOCATORS `path_only` GAP IS AN OWED FINDING**, written in
      TWO places: the realization evidence, and a DATED note beside § 7 in the
      packet's `tasks.md`. **DO NOT ADD A REFUSAL LEG** — no ratified task names
      it and this packet's rule is realize-what-was-ratified. The note carries
      all three of:
      (a) **the defect** — `path_only` means *"only the locator changed"*, so an
      entry declaring it with `previous_locator == observed_locator` (and
      therefore equal digests) records an event that did not occur, and nothing
      in the schema, the validator or the ratified delta refuses it;
      (b) **the leg it would need, and why that leg is NEUTRAL** — a check that
      `previous_locator != observed_locator` whenever `diff_class: path_only`.
      **Design C-7's placement test** puts it on this side of the line: both
      locators are fields of the record, so the contradiction is derivable from
      the record's own bytes without opening a repository — the same test that
      placed `path_only` digest equality (task 3.4c) here;
      (c) **its home** — F.2's custody-digest gate (§ 7.1, OpsxFactory's) or a
      SUCCESSOR openxFactory change. It is owed somewhere; it is not owed here.
      **Visible, not silently closed.**
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T083** *(FR-041)* **POST-HOC TICK/EVIDENCE AUDIT.** After every tick has
      landed, walk the commit history and PROVE — not assert — that no tick's
      commit precedes the commit carrying its evidence:
      `git log --format='%h %s' <base>..HEAD` plus a `git show --stat` per
      tick-bearing commit, each showing the tick and its evidence in the SAME
      commit. The audit transcript is itself evidence. The discipline is
      verified from history, never from the author's memory of the order things
      happened in.
- [x] **TICKED 2026-09-09 · Phase H, commits `c4a364d6`/`1401d512`; evidence/phaseH-T080-doc-health.txt, phaseH-T081-final-sweep.txt, phaseH-T083-tick-audit.txt.** **T082** Push the branch. **No pull request, no comment, no merge, no
      tag** — every one of those is the lane's or Brett's. **The branch merges
      forward and NEVER rebases pushed commits**: no `--force`, no
      `--force-with-lease`, no amend of anything already pushed. Integration
      with `main` is always a merge; opensoft ruleset 8981805 forbids
      non-fast-forward updates, so a rewrite is refused at the remote and a
      local one only produces a branch that cannot land.

## Traceability — every `spec.md` requirement to the tasks that discharge it

| Requirement | Tasks | Packet box |
| --- | --- | --- |
| FR-001 | T010 | 2.1 |
| FR-002 | T011 | 2.1 |
| FR-003 | T015 | 2.2 |
| FR-004 | T012 | 2.3 |
| FR-005 | T013, T014 | 2.4, 2.5 |
| FR-006 | T016 | *(none — clarify Q4)* |
| FR-007 | T015, T016 | *(none — ratified delta scenario 3)* |
| FR-010 | T020 | 3.1 |
| FR-011 | T021 | 3.2 |
| FR-012 | T027, T050, T051 | 3.3 |
| FR-013 | T025 | 3.4 |
| FR-014 | T023, T024, T053 | 3.4b |
| FR-015 | T022 | 3.4c |
| FR-016 | T026, T042, T052 | 3.5 |
| FR-020 | T030, T031, T032 *(equal-timestamp boundary)*, T033 | 4.1, 4.1b, 4.1c, 4.2 |
| FR-021a | T034, T036, T038, T039, T040, T041 | *(none — checklist finding)* |
| FR-021 | T034–T043, T044 | 4.3, 4.3b, 4.3c, 4.4, 4.5, 4.6, 4.7, 4.8, 4.8b, 4.8d |
| FR-022 | T028, T045, T046 | 4.8c |
| FR-023 | T047, T048 | 4.9 |
| FR-024 | T049 | *(none — clarify A1)* |
| FR-030 | T060 | 5.1 (measurement only) |
| FR-031 | T061 | 5.2 |
| FR-031a | T061a, T061b, T061c | 5.2 *(panel F1, cut-coupled)* |
| FR-032 | T062 | 5.3 |
| FR-033 | T063 | 5.2 |
| FR-034 | T064 | 5.4 |
| FR-034a | T061–T064 (the rule the phase follows) | *(none — checklist finding)* |
| FR-035 | T066 | 5.6 |
| FR-036 | T003 (recorded), T065, T066 | 5.5, 5.6 |
| FR-040 | T070, T071, T072, T073, T075, T076 | 0.1, 1.1, 1.2, 1.3, 6.x, 7.x |
| FR-041 | the tick discipline stated in this file's header; enforced at T070–T074; **AUDITED at T083** | — |
| FR-042 | T079 | — |
| FR-042a | every gate task; stated once in this file's header | — |
| FR-042b | the Phase B/C/D/E gates in `plan.md`'s sequence table | — |
| FR-043 | T077 | — |
| FR-044 | T074 | — |
| FR-045 | T080 | — |
| FR-045a | T080 | — |
| FR-046 | T055, T056, T057, T058, T059 | *(none — clarify Q8)* |
| FR-047 | T078 | *(none — clarify A2)* |
| FR-048 | T084 | *(none — architect ruling 2026-09-09)* |

**Every success criterion has a gate.** SC-001 → T064/T081; SC-002 → T076;
SC-003 → T015; SC-004 → T064/T081; SC-005 → T064; SC-006 → T081; SC-007 →
T054/T081; SC-008 → T080; SC-009 → T081; SC-010 → T053.

## Traceability — the ratified delta's 22 scenarios, one row each

**MEASURED: 7 scenarios on the `## MODIFIED` requirement, 15 on the `## ADDED`
one.** **13 are realized here; 9 are NOT-OWED.** The taxonomy was CORRECTED by
the consistency panel (F4) — an earlier count of 6 NOT-OWED was wrong, and it
was wrong in the direction that flatters this feature.

**THE CLASSIFYING TEST IS THE SCENARIO'S `THEN`, not its subject matter.** A
scenario whose THEN asserts *"custody is current"*, or asserts a re-derivation
that **design C-7 forbids the neutral validator from performing**, cannot be
satisfied by anything in this repository — openxFactory holds no consent
instruments and the validator opens no repository. Scenarios **8, 9 and 10** read
as "ours" because their internal legs live here, but each one's THEN is a
CURRENCY VERDICT, and the currency verdict is the consumer's by the same split
that put the git legs there. **One class per scenario, no scenario counted
twice.**

| # | Requirement | Scenario | Class | Realized by / why not |
| --- | --- | --- | --- | --- |
| 1 | MODIFIED | Custody is a pointer, not a payload | **HERE** | T015, T016 — pre-existing and PRESERVED; realized as the proof `custody` did not move |
| 2 | MODIFIED | A re-derivation is recorded beside custody, never inside it | **HERE** | T010, T013, T015 |
| 3 | MODIFIED | A re-derivation does not amend the instrument | **HERE** | FR-007 — T015, T016; realized as an ABSENCE, asserted by diff |
| 4 | MODIFIED | The executed pin is never rewritten to match the moved target | **HERE** | T021, T041 — `custody-pin-rewritten`, multi-entry fixture |
| 5 | MODIFIED | An unattributed or uncited acceptance is refused | **HERE** | T010, T039 |
| 6 | MODIFIED | An unknown class or reason is refused at the contract | **HERE** | T011, T038 |
| 7 | MODIFIED | An instrument that declares no re-derivations is unaffected | **HERE** | T033, and FR-001's ban on the top-level `required:` |
| 8 | ADDED | A direct pin verifies with no chain | **NOT-OWED** | THEN is *"custody is current"* — it needs the target hashed at HEAD, which C-7 puts in the consumer's gate |
| 9 | ADDED | An unbroken chain is admitted, link by link | **NOT-OWED** | THEN is *"custody is current"* AND *"the admission cites the commits it re-derived"* — both need the repository |
| 10 | ADDED | A path move is re-derived at both paths | **NOT-OWED** | THEN is *"the check resolves the starting locator at the commit's parent and the observed locator at the commit"* — the re-derivation C-7 forbids here. T014 writes the in-file COMMENT that states the rule; it does not satisfy the scenario |
| 11 | ADDED | A `path_only` entry whose digests differ is refused | **HERE** | T022, T043 — both digests are record fields, so the leg is neutral |
| 12 | ADDED | A `header_only` claim contradicted by the diff is refused | **NOT-OWED** | Needs the measured diff |
| 13 | ADDED | A locator pair that resolves at neither path is refused | **NOT-OWED** | Resolution runs through the consumer's DECLARED mapping |
| 14 | ADDED | A content-class divergence withholds the verdict | **HERE** | T023, T024, T045, T046, T053 — the class is a record field, so WITHHELD is computable without a repository |
| 15 | ADDED | A consumer gate propagates a withheld verdict and never upgrades it | **NOT-OWED** | It is the consumer's gate by construction (§ 6.2b) |
| 16 | ADDED | A broken link is refused, not repaired | **HERE** | T020, T034 |
| 17 | ADDED | A chain that does not anchor to the pin is refused | **HERE** | T020, T037 — one fixture per anchor half |
| 18 | ADDED | A chain on a commit that is not an ancestor of HEAD is refused | **NOT-OWED** | The ancestry leg needs git history |
| 19 | ADDED | A HEAD digest matching no terminus is refused | **NOT-OWED** | Needs the target's bytes at HEAD |
| 20 | ADDED | Entries out of recorded-time order are refused | **HERE** | T020, T036; equal timestamps ADMITTED, exercised at T032 |
| 21 | ADDED | A chain that cannot be re-derived is refused, never admitted | **NOT-OWED** | "Cannot re-derive" is a statement about a repository |
| 22 | ADDED | The neutral pass is not a currency claim | **HERE** | T025 — the eight-item report line, the scenario that makes the split legible |

**13 HERE + 9 NOT-OWED = 22.** Every one of the nine is git-dependent under the
test above, and all nine land with the consumer under § 7.1 / § 6.2b. **This is
the C-7 split the requirement itself states, not a gap** — but it is a LARGER
share of the delta than the first count admitted, and the honest figure is the
one that belongs here.

The locator-gap leg the ratified delta names in its refusal list but gives no
scenario of its own is realized anyway at T020/T035
(`custody-chain-locator-gap`), because the requirement's chained condition
states it in the body.

## Dependencies

```text
A (T001-T007)
  └─> B (T010-T017)
        └─> C (T020-T028)
              └─> D (T030-T049)
                    └─> E (T050-T054)
                          ├─> F (T055-T059)   UNBLOCKED 2026-09-09 (#630 c5603344475)
                          └─> G (T060-T066)   LAST, and INDEPENDENT of F
                                └─> H (T070-T082)
```

`[P]` groups: T030–T033 among themselves; T034–T043 among themselves;
T047/T048/T049 among themselves; T050–T053 among themselves.

## Definition of done

- All 35 in-scope packet boxes ticked, each in the same commit as its evidence.
- 11 boxes carrying dated NOT-OWED / NOT-OWED-HERE lines; classes sum to 46.
- `SC-001`..`SC-010` in `spec.md` all satisfied and evidenced.
- `speckit-analyze` reports ZERO findings.
- The branch is pushed and nothing else is done to it.
