# Tasks: 033-add-consent-custody-rederivation-record

**Branch**: `033-add-consent-custody-rederivation-record`
**Lane**: opsXfactory-1
**Realizes**: openxFactory OpenSpec change `add-consent-custody-rederivation-record`,
§§ 0–5 of its 46-box list.

**HOW THE TWO LISTS RELATE.** The packet's `tasks.md` is the GOVERNED list and
this one is the EXECUTABLE list. Every `T###` below names the packet box or
architect answer it discharges. A packet box is TICKED only by the `T###` that
performs its act, in the same commit as that act's evidence (architect ruling
Q5). Where this file and the packet differ, the packet governs.

**BOX ACCOUNTING, and it must sum to 46.**

| Class | Count | Boxes |
| --- | --- | --- |
| TICKED here | 35 | 0.1; 1.1–1.3; 2.1–2.5; 3.1–3.5 (incl. 3.4b, 3.4c); 4.1–4.9 (incl. 4.1b, 4.1c, 4.3b, 4.3c, 4.8b, 4.8c, 4.8d); 5.2, 5.3, 5.4 |
| NOT-OWED-HERE | 3 | 5.1 (lane claims the number), 5.5 (lane's landing bookkeeping), 5.6 (`[OPERATOR]` tag) |
| NOT-OWED | 8 | 6.1, 6.2, 6.2b, 6.3, 6.4; 7.1, 7.2, 7.3 |
| **Total** | **46** | |

`[P]` = parallelizable with its siblings (different files, no ordering
dependency).

---

## Phase A — the Speckit tree

- [ ] **T001** `spec.md` written and the twelve clarify answers applied.
      *(done at STOP A + the answer pass)*
- [ ] **T002** `clarify-questions.md` carries all twelve answers inline plus
      A1 and A2. *(done)*
- [ ] **T003** `plan.md` written, **including THE LANDING CONTRACT** (Q1).
      *(done)*
- [ ] **T004** `research.md` written — R1..R14, every figure with its command.
      *(done)*
- [ ] **T005** This file.
- [ ] **T006** `speckit-checklist` no-arg: one checklist per requirement-quality
      domain the feature touches, release-gate rigor, no item cap. Run each and
      tick it.
- [ ] **T007** `speckit-analyze` loop to ZERO findings, re-running after every
      fix.

## Phase B — § 2, the schema

**File**: `contracts/schemas/consent-instrument.schema.yaml`. One commit.

- [ ] **T010** *(box 2.1)* Add the top-level `custody_rederivations` property:
      `type: array`, items `type: object`, `additionalProperties: false`,
      `required: [at, commit, previous_locator, observed_locator,
      previous_sha256, observed_sha256, diff_class, reason, ruling_ref,
      recorded_by]` — TEN, in that order.
- [ ] **T011** *(box 2.1)* Field shapes exactly: `at` `type: string,
      format: date-time`; `commit` `pattern: "^[0-9a-f]{40}$"`; both locators
      `type: string, minLength: 1` with **no path grammar**; both digests
      `pattern: "^[0-9a-f]{64}$"`; `diff_class`
      `enum: [path_only, header_only, content]`; `reason`
      `enum: [lifecycle_header_edit, archive_move, other_ruled_edit]`;
      `ruling_ref` and `recorded_by` `type: string, minLength: 1`.
- [ ] **T012** *(box 2.3)* `contract_schema_version: 2` → `3`, with an in-file
      comment in the style of the existing `1 -> 2` note: what grew, that it is
      ADDITIVE, and that the record envelope's `schema_version` stays `const: 1`
      because moving it would invalidate every instrument in the estate.
- [ ] **T013** *(box 2.4)* In-file comment on the new property: WHY it is a
      SIBLING (ruling D9's closure argument, design C-1) and that `ruling_ref`
      is a DECLARED POINTER the validator does not resolve — the
      `dependent_refs.ref` posture.
- [ ] **T014** *(box 2.5)* In-file comment on the locator pair: `custody.locator`
      is OPAQUE and is NOT a path (C-6a); resolution runs through the consuming
      repository's DECLARED custody store mapping; the two legs are evaluated on
      opposite sides of the commit; an archive move is unadmittable without the
      pair. **Name the measurement** — every OpsxFactory locator carries an
      `opsx:opensoft/` scheme prefix and three of four targets resolve at no ref
      under their literal path.
- [ ] **T015** *(box 2.2)* **PROVE `custody` IS UNTOUCHED**: `git diff` over the
      file shows ZERO changed lines inside the `custody` object — its two
      properties, its `required`, its `additionalProperties: false` and its
      comment block byte-identical. Transcript to `evidence/`. **A diff touching
      `custody` fails this task.**
- [ ] **T016** *(Q4)* Confirm by diff that `$id`, the record envelope's
      `schema_version: const: 1` and the manifest row's `schema_version: 1` are
      all unmoved.
- [ ] **T017** *(Q5a)* Commit message STATES that
      `contracts/manifest.yaml`'s `consent-instrument` digest is now
      deliberately stale and names T060 as the commit that closes it.

## Phase C — § 3, the canonical validator

**File**: `scripts/validate-consent-instruments.py`. Codes adopted verbatim
(Q10).

- [ ] **T020** *(box 3.1)* A new check beside `check_custody` for the chain's
      INTERNAL legs, with DISTINCT codes per leg:
      - `custody-chain-unanchored` — `e₁.previous_sha256 != custody.sha256`
        **OR** `e₁.previous_locator != custody.locator` (BOTH halves);
      - `custody-chain-broken-link` — `eᵢ.previous_sha256 !=
        eᵢ₋₁.observed_sha256`;
      - `custody-chain-locator-gap` — `eᵢ.previous_locator !=
        eᵢ₋₁.observed_locator`;
      - `custody-chain-out-of-order` — `at` decreasing in declared order.
- [ ] **T021** *(box 3.2)* `custody-pin-rewritten` — refuse an instrument whose
      `custody.sha256` equals any entry's `observed_sha256` while a LATER entry
      exists, and more generally any state in which the pin has been advanced to
      a value the chain itself records as observed.
- [ ] **T022** *(box 3.4c)* `custody-path-class-digests-differ` — a `path_only`
      entry whose `previous_sha256 != observed_sha256` is refused.
- [ ] **T023** *(box 3.4b, Q2)* **MINT THE WITHHELD OUTCOME.** Add
      `custody-content-class-withheld` as a DISTINCT outcome on `Findings` —
      not an error, not a warning. A `content`-class entry with sound internal
      legs yields it.
- [ ] **T024** *(box 3.4b, Q2)* **THE EXIT STATUS, behind ONE named constant.**
      Define a single module constant (provisionally `EXIT_NEEDS_DECISION = 3`),
      return it from `report()` when a REAL instrument withholds and nothing
      errors, extend the module docstring's `Exit codes:` line **in this script
      only**, and write a comment recording that **the NUMBER is Brett Heap's
      ruling to make** (clarify Q2 is PARKED) so a different ruling moves the
      constant and nothing else. **The PACKAGED withheld fixture is EXEMPT** —
      an expected withholding is to the third bucket what an expected failure is
      to a negative — so the self-test still exits 0.
- [ ] **T025** *(box 3.4)* The report line for a chained instrument states what
      was checked and what was NOT, so a neutral pass is unreadable as a
      currency verdict (promoted scenario *The neutral pass is not a currency
      claim*). WITHHELD is named beside the error and warning counts.
- [ ] **T026** *(box 3.5, Q12)* **EXTEND `walk_strings` OVER THE ENTRY** — the
      whole entry MINUS the two digest fields (`previous_sha256`,
      `observed_sha256`), so both locators, `ruling_ref` and `recorded_by` are
      walked and `commit` / `at` / `diff_class` / `reason` ride along already
      bounded. Reuse `BASE64_BLOB_RX`, the `data:` prefix, `PDF_MAGIC_RX`, the
      multi-line predicate and the `embedded-original-content` code.
- [ ] **T027** *(box 3.3)* **NO GIT RE-DERIVATION IS ADDED.** The module opens no
      repository, shells out to no `git`, and reads no file named by a locator.
- [ ] **T028** *(box 3.4b)* `self_test` grows the THIRD expectation bucket
      (see T042); `repo_scan` reports WITHHELD as found (Q3b) and needs no
      bucket discipline.

## Phase D — § 4, the fixtures

**Directories**: `examples/consent-instrument/`, `.../negative/`, and a NEW
`.../withheld/` (Q3a).

### Positives `[P]`

- [ ] **T030** *(box 4.1)* A two-entry unbroken chain, `header_only` /
      `lifecycle_header_edit`, admitted by the internal legs.
- [ ] **T031** *(box 4.1b)* An `archive_move` / `path_only` entry whose locator
      pair DIFFERS and whose digests are EQUAL on both sides — design C-6a,
      `proposal.md` Example B.
- [ ] **T032** *(box 4.1c)* The TWO-ENTRY shape the real repair needs: e1
      `archive_move`/`path_only`, e2 `lifecycle_header_edit`/`header_only`,
      modelled on prescription I in `design.md` § *The consumer handoff*.
- [ ] **T033** *(box 4.2)* An EXISTING example left **byte-unchanged** and
      re-validated, proving the growth is additive for an instrument declaring
      no array. Evidence: the diff shows the file untouched and the self-test
      still passes it.

### Negatives, one per named refusal `[P]`

- [ ] **T034** *(box 4.3)* Broken digest link → `custody-chain-broken-link`.
- [ ] **T035** *(box 4.3b)* Locator gap with digests linking correctly →
      `custody-chain-locator-gap`.
- [ ] **T036** *(box 4.3c)* Entries out of recorded-time order →
      `custody-chain-out-of-order`.
- [ ] **T037** *(box 4.4)* TWO fixtures: a first entry whose `previous_sha256`
      is not the pin, and one whose `previous_locator` is not `custody.locator`
      → `custody-chain-unanchored` both, detail-pinned so each tests its own
      half.
- [ ] **T038** *(box 4.5)* TWO fixtures: an unknown `diff_class` member and an
      unknown `reason` member → `schema`, each detail-pinned on its field.
- [ ] **T039** *(box 4.6)* TWO fixtures: an entry omitting `ruling_ref` and one
      omitting `recorded_by` → `schema`, each detail-pinned.
- [ ] **T040** *(box 4.7)* An entry carrying an **ELEVENTH** property → `schema`,
      detail-pinned on `additionalProperties`. (Entry closure has TEN required
      fields since C-6a, so a "ninth" would not test closure at all.)
- [ ] **T041** *(box 4.8)* A rewritten pin — `custody.sha256` advanced to an
      observed digest while the chain still claims the original anchor →
      `custody-pin-rewritten`.
- [ ] **T042** *(box 4.8b)* TWO fixtures: a blob-shaped `ruling_ref` and a
      blob-shaped `recorded_by` → `embedded-original-content`. **This is the
      fixture pair that proves T026 landed.**
- [ ] **T043** *(box 4.8d)* A `path_only` entry whose two digests differ →
      `custody-path-class-digests-differ`.
- [ ] **T044** Every new negative registered in `EXPECTED_NEGATIVE_FINDINGS`
      with a detail substring wherever the code alone is too coarse (`schema` is
      satisfied by any schema error — the existing rule).

### The third bucket

- [ ] **T045** *(box 4.8c, Q3a)* Create `examples/consent-instrument/withheld/`
      and the WITHHELD fixture: an instrument whose LAST entry declares
      `diff_class: content` and whose internal legs are ALL SOUND. **Asserted as
      WITHHELD — not a pass and not an error.**
- [ ] **T046** *(box 4.8c, Q3a)* `self_test` grows `EXPECTED_WITHHELD_OUTCOMES`,
      **fail-closed BOTH ways** exactly as `EXPECTED_NEGATIVE_FINDINGS` is: a
      fixture on disk with no table entry and a table entry with no fixture are
      each errors. The self-test note reports THREE bucket counts.

### Corpus counts

- [ ] **T047** *(box 4.9, Q9)* `examples/consent-instrument/README.md`:
      Layout tree COMPLETE over the grown corpus; *Schema → example map* table
      complete **with a THIRD column for the withheld bucket**; *Named cases
      from the spec* grows **one bullet per refusal code (7) + one positive
      chain-shapes bullet + one withheld bullet**; counts RE-MEASURED by
      listing the directories, never by arithmetic.
- [ ] **T048** *(box 4.9)* `contracts/manifest.yaml`'s `consent-instrument`
      corpus comment (*"5 valid + 5 invalid + purpose probes"*) RE-MEASURED.
      **It is already false at 6/7 before this feature adds a byte** — do not
      increment it, re-count it.
- [ ] **T049** *(clarify A1 — named by NO ratified task)* `contracts/README.md`'s
      row for `scripts/validate-consent-instruments.py` +
      `examples/consent-instrument/` reads *"self-testing over 5 positives, 5
      indexed negatives, and 2 purpose probes"*. RE-MEASURE it over the three
      buckets. Carried as an ADDITIONAL realization act, not as a renumbering of
      the ratified list.

## Phase E — `tests/consent_instruments/` (Q7)

- [ ] **T050** *(box 3.3, Q7c)* **Source-level no-git ban**: assert the module
      imports no `subprocess`, contains no `git` token, and reads no file named
      by a locator.
- [ ] **T051** *(box 3.3, Q7c)* **Runtime patch**: patch `subprocess.run` and
      `Path.open` and prove neither is reached, exercised over **ALL THREE
      buckets** — positive, negative and withheld — since the withheld leg is
      the one most likely to reach for a repository.
- [ ] **T052** *(box 3.5, Q7b)* **Parametrized blob-walk test** proving the walk
      reaches each of the four free strings (`previous_locator`,
      `observed_locator`, `ruling_ref`, `recorded_by`).
- [ ] **T053** *(Q2)* A test pinning the WITHHELD exit status to the single
      named constant, so a change to the number is a one-line test edit and
      never a silent drift.
- [ ] **T054** `python3 -m pytest tests/consent_instruments -q` green, and then
      the full `python3 -m pytest tests/ -q -m "not postgres"` green.

## Phase F — Q8's README amendments  ⛔ BLOCKED

- [ ] **T055** **BLOCKER — the LANE must post the row-3 substrate note** on
      openxFactory issue #630 for the two SIBLING-row sentences before T057 and
      T058 are written. This packet's own row (T056) rides its standing row-3
      claim `5571680388` (2026-09-07). **Do not write T057/T058 until the note
      exists; report the block instead.**
- [ ] **T056** *(Q8a-1)* Amend this packet's own OpenSpec Records row —
      *"**all 46 boxes in `tasks.md` stay unticked**"* — in the `3b530009` form:
      block-quote the superseded sentence, name the un-superseded neighbour,
      marker `AMENDED 2026-09-09`.
- [ ] **T057** *(Q8a-3)* Amend `README.md:3022`'s present-tense box count, same
      form. **KEEP *"the three pins are still broken"*** — that half stays true,
      because the repair is § 6 and § 6 is the consumer's.
- [ ] **T058** *(Q8a-5, the load-bearing one)* Amend `README.md:2993` inside the
      `govern-archived-record-edits` row: *"the consent family's is PROPOSED
      only (`contract_schema_version: 2`, no `custody_rederivations` property,
      `contract-v3.4`, 46/46 boxes unticked)"* — **false on all four counts
      after this lands**, and the premise of that rule's TRANSITION CLAUSE.
- [ ] **T059** *(Q8a-2, Q8a-4)* **LEAVE** the past-tense *"left its 46"*
      (`README.md:2949`) and the dated *"measured 2026-09-09 UTC at `main`
      `6cc06288`"* (`README.md:3098`) as TRUE-WHEN-WRITTEN. Record the decision;
      do not edit them.

## Phase G — § 5, THE CUT (LAST)

**One candidate commit** (Q5a, policy step 2). Taken only after Phases B–F.

- [ ] **T060** *(box 5.1's MEASUREMENT — the CLAIM is the lane's)* Fetch,
      integrate onto the final integration point, then **RE-MEASURE** the next
      additive minor on all three surfaces (`contracts/manifest.yaml:3`,
      `contracts/releases/`, `git tag -l 'contract-v*'`). Report the result to
      the lane. **Re-measure at EVERY merge-from-main.** Do not post the claim.
- [ ] **T061** *(box 5.2)* `contracts/manifest.yaml`, ALL THREE edits in this
      one commit: `contract_bundle_version` → the allocated version; the
      `consent-instrument` row's `sha256` **re-derived by `sha256sum`** from the
      moved file (closing T017's deliberate staleness); and an APPENDED
      `consumption_rule` paragraph in the `contract-v1.33` style — what grew,
      that it is ADDITIVE, that the envelope stayed `const: 1`.
      **`consent-instrument-class-registry`'s row is untouched.**
- [ ] **T062** *(box 5.3, Q6)* `contracts/CHANGELOG.md` entry naming **what
      changed in the BUNDLE, not what this session intended**: all **4 additions
      and 14 modifications** under `contracts/` since `contract-v3.4`
      (`research.md` R6), each attributed to its originating change/PR —
      including the `publish-openspec-cli-pin-as-contract-member` **A-defer**
      registration that this bundle is what finally publishes. **Change class:
      ADDITIVE (minor)**, with the measurement that justifies it (one new
      optional property, one `contract_schema_version` bump, nothing removed,
      no enumeration narrowed, every existing instrument valid unchanged).
- [ ] **T063** *(box 5.2)* `contracts/releases/<version>.digests.yaml`
      **BUILT** by `python3 scripts/validate-contract-release.py build --tag
      <version> --output contracts/releases/<version>.digests.yaml`. **Never
      hand-edited.** Record the entry count and the delta against
      `contract-v3.4`'s 283.
- [ ] **T064** *(box 5.4, Q11)* Run **all five gates against the exact unchanged
      candidate**, transcripts to `evidence/`:
      `scripts/validate-release-tag-gate.py`;
      `python3 -m pytest tests/ -q -m "not postgres"`;
      `scripts/validate-manifest-digests.py`;
      `scripts/validate-contract-release.py verify-commit --commit <candidate>`;
      `scripts/validate-consent-instruments.py --strict`.
- [ ] **T065** *(box 5.5)* **NOT-OWED-HERE.** Landing the exact reviewed commit,
      and the post-merge gate re-run the merge commit forces, are the LANE's
      under the landing contract in `plan.md`. Dated NOT-OWED line, no tick.
- [ ] **T066** *(box 5.6)* **NOT-OWED-HERE.** The annotated tag and its
      independent verification are `[OPERATOR]` acts, targeting the LANDED MERGE
      COMMIT. Dated NOT-OWED line, no tick.

## Phase H — bookkeeping, evidence and the notes

- [ ] **T070** *(box 0.1)* TICK with evidence: commit `6cfe9ba6` re-stamped the
      ledger row to the real PR `#774`; the row reads
      `moved_by: "#774", moved_on: "2026-09-07"`; `--ledger-diff` reports the
      corpus consistent at 189 rows.
- [ ] **T071** *(box 1.1)* TICK with evidence: `review/ratification-2026-09-08.md`
      exists; `Status: ratified` on `proposal.md`, `design.md`, `tasks.md`; the
      `Ratified:` line present; the README Records row already flipped
      (`README.md:848`). **The citation states the MEASURED absence of a GitHub
      approving review** (`research.md` R12) and cites instead the in-repo
      record, Brett Heap's own merge (`merged_by brettheap`,
      `2026-09-08T03:48:44Z`, `543d47a9` over head `0d541576`) and his
      LANDING/LANDED comments.
- [ ] **T072** *(box 1.2)* TICK with evidence: the ratification record's *"no
      veto was exercised on any of the eleven"* rules all eleven veto points as
      written. Quote it exactly — never more.
- [ ] **T073** *(box 1.3)* TICK with evidence: the record's *"Task 1.3's operator
      veto was NOT exercised"* section, and the default that stands (no
      `amendments` entry; the three instruments stay `executed`).
- [ ] **T074** *(architect ruling Q1/Q10 form)* Amend the packet `tasks.md`'s
      ratified *"NOTHING BELOW IS DONE. EVERY BOX IS UNTICKED…"* preamble in the
      `3b530009` form **in the same commit as the first tick**: block-quote the
      superseded sentence, name the un-superseded neighbour, marker
      `AMENDED 2026-09-09`, tick marker `**TICKED 2026-09-09`.
- [ ] **T075** Dated NOT-OWED lines on §§ 6.1, 6.2, 6.2b, 6.3, 6.4 and 7.1, 7.2,
      7.3 — named as owed elsewhere, performed nowhere here.
- [ ] **T076** **Note classes SUM TO 46**: 35 ticked + 3 NOT-OWED-HERE + 8
      NOT-OWED. Assert the arithmetic in the evidence file.
- [ ] **T077** *(architect ruling Q10)* ONE additive dated realization note after
      `proposal.md`'s `Lane:` line, correcting any ratified ENUMERATION this
      realization falsifies (the *"every box in `tasks.md` stays unticked"*
      sentence). **`design.md`, `.openspec.yaml` and the delta stay frozen.**
- [ ] **T078** *(clarify A2 — state it, do not act on it)* A DATED note, in the
      realization evidence AND in the neighbourhood of § 7 in the packet's
      `tasks.md`, recording that landing this realization **DECLARES the consent
      family's re-derivation rule**, so under `govern-archived-record-edits`'
      transition clause an edit of a consent pinned target converts from
      **REPORTED** to **REFUSED** for that family **once F.2's gate exists**
      (§ 7.1, OpsxFactory's). **Build nothing, schedule nothing, tick nothing.**
- [ ] **T079** *(architect ruling Q4)* Evidence in BOTH trees:
      `specs/033-add-consent-custody-rederivation-record/evidence/` and
      `openspec/changes/add-consent-custody-rederivation-record/evidence/realization-2026-09-09.md`.
- [ ] **T080** *(architect ruling Q10)* **doc-health TWO-REPORT COMPARISON** —
      identical basenames, `--as-of` pinned to one date on both, `main` and this
      branch, finding sets diff-identical at every severity.
- [ ] **T081** Final gate sweep at the branch head: pinned CLI
      `--change … --strict` **and** `--all --strict` (zero UNDISPOSITIONED
      failures); `validate-consent-instruments.py --strict` over the corpus;
      `validate-sequenced-after.py .` and `--ledger-diff`;
      `validate-scope-globs.py`; `validate-manifest-digests.py`;
      `pytest tests/ -q -m "not postgres"`. Transcripts to `evidence/`.
- [ ] **T082** Push the branch. **No pull request, no comment, no merge, no
      tag** — every one of those is the lane's or Brett's.

## Dependencies

```text
A (T001-T007)
  └─> B (T010-T017)
        └─> C (T020-T028)
              └─> D (T030-T049)
                    └─> E (T050-T054)
                          ├─> F (T055-T059)   BLOCKED on the lane's substrate note
                          └─> G (T060-T066)   LAST; must not wait on F
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
