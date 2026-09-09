# Tasks: add-consent-custody-rederivation-record

Status: ratified
Ratified by: add-consent-custody-rederivation-record — 2026-09-08, Brett Heap, "ratify 774, merge it and land it" (record `review/ratification-2026-09-08.md`)
Lane: opsXfactory-1

**AMENDED 2026-09-09 — ONE NAMED SENTENCE ABOVE IS SUPERSEDED, AND IT IS QUOTED
IN PLACE RATHER THAN DELETED.** The superseded sentence is exactly this one, and
no other:

> **NOTHING BELOW IS DONE. EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE
> PACKET RATHER THAN AN OVERSIGHT.**

Realization began on 2026-09-09 under Speckit feature
`specs/033-add-consent-custody-rederivation-record`, lane `opsXfactory-1`, and
the boxes below are ticked as their acts land — each in the same commit as its
evidence.

The clause that FOLLOWED it in the same paragraph — *"no consumer pin advances,
and no instrument takes an entry"* — is **NOT** superseded. It still holds and
will keep holding: those are § 6's acts, § 6 is the CONSUMER's, and nothing in
this realization reaches an OpsxFactory file. The rest of the original sentence
is superseded only as each act lands: this is a PROPOSAL no longer, schema bytes
have moved, and the remaining clauses fall one at a time with their boxes.

**TICKED 2026-09-09** — every tick below carries a note naming the act, the
commit or record that performed it, and the evidence transcript that proves it.

**Tags.** Untagged = openxFactory. `[OpsxFactory]` = `opensoft/OpsxFactory` and
its own OpenSpec instance — listed as the CONSUMER'S owed acts, outside this
change's archive gate. `[OPERATOR]` = only Brett Heap can perform it: a
ratification, a human-only surface write, a tag.

## 0. Bookkeeping this branch already carries, and the one stamp that is provisional

- [x] **TICKED 2026-09-09.** 0.1 **RE-STAMP THE SWEEP LEDGER ROW WITH THE REAL PULL-REQUEST NUMBER.**
  `tests/sequenced_after/corpus-ledger.yaml` carries this change's row —
  `{state: active, class: co-modifier, declares: [add-consent-instrument],
  depth: 1}` — and the DERIVED keys are measured and correct
  (`--ledger-diff` exits 0 at this branch's head). Its `moved_by: "#757"` is
  **PROVISIONAL**: no pull request was opened by the authoring session, and
  `#757` is the next number measured at 2026-09-07T14:1xZ (the highest existing
  was `#756`) rather than an observed one. The ledger's own doctrine makes
  `moved_by` AUTHOR-SUPPLIED AND UNVERIFIED — only its shape is checked — so
  this does not red any gate; it is a pointer for a human reading the history
  and it should be true. **It is now known to be WRONG: `#757` was taken by
  another lane's pull request while this packet was in review**, so the re-stamp
  is MANDATORY rather than tidy-up. Re-run
  `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<real PR>'`
  once the number is known, and read the diff: exactly one row must move.

## 1. Ratification — OWED, NOT GIVEN

- [x] **TICKED 2026-09-09.** 1.1 **[OPERATOR] Ratify or veto.** The F.1 ruling of 2026-09-07 ordered
  this authoring and chose the repair FORM; it approved no field name, no enum
  member, no closure posture and no chain rule. Ratification is a separate act.
  Record it at `review/ratification-<date>.md` in the neighbours' form, flip
  `Status: draft` → `Status: ratified` on `proposal.md`, `design.md` and this
  file, and add the `Ratified:` line plus the README row's status flip.
- [x] **TICKED 2026-09-09.** 1.2 **[OPERATOR] The eleven veto points, ruled individually or as a
  block:** C-1 sibling not member; C-2 the name `custody_rederivations`; C-3
  ten fields all required; C-4 `diff_class` members; C-5 `reason` members;
  C-6 the chain rule, the path pair and the ancestry leg; C-6a declared locator
  resolution plus the entry's locator pair; C-7 the validator split and the
  obligation to operate a check; C-8 additive bump to
  `contract_schema_version: 3`; C-9 a `content` class WITHHOLDS the verdict;
  C-10 a re-derivation is not an amendment. A veto on C-1, C-6, C-6a or C-7
  changes the delta; a veto on C-2, C-4 or C-5 changes only the schema text.
- [x] **TICKED 2026-09-09.** 1.3 **[OPERATOR] C-10 SUPERSEDES ONE CLAUSE OF YOUR OWN F.1 RULING and
  needs your word specifically.** The ruling says the three instruments take
  *"their `amendments` entries plus the structured block"*. C-10 writes the
  structured block and NO `amendments` entry, because an amendment is a status
  TRANSITION (promoted requirement, ruling D7) and all four instruments are
  `status: executed` — so the prose half would move three executed consent
  instruments to `amended` to record that a repository moved a file underneath
  an unchanged pin. Keeping the `amendments` entry is yours to choose; the cost
  is that transition.

**§ 0 AND § 1 EVIDENCE, 2026-09-09.** These four boxes record acts ALREADY
PERFORMED before realization began; they are ticked here because the acts are
done and cited, not because this session did them.

- **0.1 — the re-stamp LANDED at `6cfe9ba6`.** The row now reads
  `moved_by: "#774", moved_on: "2026-09-07"`, the real pull request rather than
  the provisional `#757` another lane had taken.
  `validate-sequenced-after.py . --ledger-diff`: *per-change sweep ledger
  consistent with the corpus (**189 rows**)*, rc=0.
- **1.1 — ratified, and the citation states what is MEASURED ABSENT.** The
  record is `review/ratification-2026-09-08.md`; `Status: ratified` stands on
  `proposal.md`, `design.md` and this file; the `Ratified:` line is
  `proposal.md:10`; the README Records row is flipped. **There is NO approving
  GitHub review on PR #774** (`research.md` R12) — so the ratification rests on
  the in-repo record, on Brett Heap's OWN MERGE (`merged_by brettheap`,
  `2026-09-08T03:48:44Z`, `543d47a9` over head `0d541576`) and on his
  LANDING/LANDED comments, and the absence is named rather than papered over.
- **1.2 — all eleven ruled, as a block.** The record's words, quoted exactly and
  never more: *"Every other decision likewise stands as recommended; no veto was
  exercised on any of the eleven."*
- **1.3 — the operator veto was NOT exercised**, under the record's own heading
  *"Task 1.3's operator veto was NOT exercised"*, so **the default stands**: no
  `amendments` entry is written for a custody re-derivation, and the three
  OpsxFactory instruments stay `status: executed`.

## 2. The schema edit

- [x] 2.1 **TICKED 2026-09-09.** `contracts/schemas/consent-instrument.schema.yaml`: add the top-level
  `custody_rederivations` property — `type: array`, items `type: object` with
  `additionalProperties: false` and `required: [at, commit, previous_locator,
  observed_locator, previous_sha256, observed_sha256, diff_class, reason,
  ruling_ref, recorded_by]` (TEN, per design C-3 as revised by C-6a). Shapes:
  `at` `type: string, format: date-time`; `commit` `pattern: "^[0-9a-f]{40}$"`;
  both locators `type: string, minLength: 1` (OPAQUE — no path grammar is
  imposed here, per C-6a); both digests `pattern: "^[0-9a-f]{64}$"`;
  `diff_class` `enum: [path_only, header_only, content]` (THREE — `path_only` is
  the pure relocation, which changes zero bytes and therefore has no truthful
  class among the other two); `reason`
  `enum: [lifecycle_header_edit, archive_move, other_ruled_edit]`; `ruling_ref`
  and `recorded_by` `type: string, minLength: 1`.
- [x] 2.2 **TICKED 2026-09-09.** `custody` IS NOT EDITED. Confirm by diff that its two properties, its
  `required`, its `additionalProperties: false` and its comment block are
  byte-identical after the change. A diff touching `custody` fails this task.
- [x] 2.3 **TICKED 2026-09-09.** `contract_schema_version: 2` → `3`, with the in-file comment written in
  the style of the existing `1 -> 2` note: what grew, that it is ADDITIVE, and
  that the RECORD envelope's `schema_version` stays `const: 1` because moving it
  would invalidate every instrument in the estate.
- [x] 2.4 **TICKED 2026-09-09.** An in-file comment on the new property recording WHY it is a sibling
  (ruling D9's closure argument, design C-1) and that `ruling_ref` is a DECLARED
  POINTER the validator does not resolve — the `dependent_refs.ref` posture.
- [x] 2.5 **TICKED 2026-09-09.** An in-file comment on the locator pair recording that `custody.locator`
  is OPAQUE and is NOT a path (C-6a): resolution runs through the consuming
  repository's DECLARED custody store mapping, the two legs are evaluated on
  opposite sides of the commit, and an archive move is unadmittable without the
  pair. Name the measurement: every OpsxFactory locator carries an
  `opsx:opensoft/` scheme prefix and three of four targets resolve at no ref
  under their literal path.

**§ 2 EVIDENCE, 2026-09-09.** All five acts landed in ONE commit on branch
`033-add-consent-custody-rederivation-record`. Transcripts:
`specs/033-add-consent-custody-rederivation-record/evidence/T015-T016-schema-proofs.txt`
and `.../evidence/T017-manifest-digests.txt`.

- **2.2 is PROVEN, not asserted.** `git diff -U0` over the schema reports
  exactly TWO hunks — line 14 (`contract_schema_version` and its `2 -> 3` note)
  and an APPEND at 354 (the new property). The `custody` object occupies lines
  180–196 and lies in NEITHER. The sha256 of the `custody` block is
  `2bd85913c3640dee61b8c66ca93fb0d68b03d22308cc9f04594678a80ab4bd3c` at HEAD and
  the same in the working tree.
- **The three identity fields stay put** (`$id` at line 7, the record envelope's
  `schema_version: const: 1` at 72–73, and `contracts/manifest.yaml`'s row-level
  `schema_version: 1` at 2041), as the `contract-v1.33` precedent left them.
- **The `consent-instrument` row's `sha256` was RE-DERIVED IN THIS SAME COMMIT**
  — `13b0fe46…` → `2b834492…` — because a per-file digest is integrity
  bookkeeping for the edited file, not a release surface. The commit that made
  it stale is the commit that closes it, so no commit on this branch is left
  with a stale digest. `validate-manifest-digests.py`: **189 per-file digests
  verify, rc=0**.
- **The growth is ADDITIVE, measured**: `validate-consent-instruments.py
  --strict` reports **0 errors, 0 warnings**, with all SIX existing valid
  examples still valid and unedited — none declares the new array.

## 3. The canonical validator — internal legs only

- [x] **TICKED 2026-09-09.** 3.1 `scripts/validate-consent-instruments.py`: a new check beside
  `check_custody` for the chain's INTERNAL legs — anchor in BOTH halves
  (`e₁.previous_sha256 == custody.sha256` AND `e₁.previous_locator ==
  custody.locator`), linkage in BOTH halves (`eᵢ.previous_sha256 ==
  eᵢ₋₁.observed_sha256` AND `eᵢ.previous_locator == eᵢ₋₁.observed_locator`),
  non-decreasing `at` in declared order, and closed enums/shape via the schema
  layer. Distinct finding codes per leg, in the file's existing naming style
  (candidates: `custody-chain-unanchored`, `custody-chain-broken-link`,
  `custody-chain-locator-gap`, `custody-chain-out-of-order`).
- [x] **TICKED 2026-09-09.** 3.2 The rewritten-pin leg: refuse an instrument whose `custody.sha256`
  equals any entry's `observed_sha256` while a LATER entry exists, and more
  generally any state in which the pin has been advanced to a value the chain
  itself records as observed. Finding code candidate: `custody-pin-rewritten`.
- [x] **TICKED 2026-09-09.** 3.3 **NO GIT RE-DERIVATION IS ADDED** (design C-7). Assert the absence:
  the validator opens no repository, shells out to no `git`, and reads no file
  named by `custody.locator`. A test pins that absence so a helpful later edit
  fails on the developer's machine first.
- [x] **TICKED 2026-09-09.** 3.4 The neutral pass MUST NOT report itself as a currency verdict. The
  validator's report line for a chained instrument says what it checked and
  what it did not, per the promoted scenario *The neutral pass is not a currency
  claim*.
- [x] **TICKED 2026-09-09.** 3.4b **MINT THE WITHHELD OUTCOME — it is mandated by the requirement and
  represented by nothing today.** `Findings` carries `error` / `warning` / `note`
  only, so a `content`-class entry with sound internal legs would silently pass.
  Add `custody-content-class-withheld` as a DISTINCT OUTCOME, not an error and
  not a warning: the record is correct and the INSTRUMENT is what needs
  attention, so an error would send it to whoever maintains the chain. Represent
  it as a NAMED OUTCOME in the report line that task 3.4 defines — the run says
  `WITHHELD: <instrument>` beside its error and warning counts, and its exit
  status is the one the repository rules for "needs a human decision" rather
  than "is malformed". **Task 3.3's no-git assertion is untouched**: the class is
  a field of the record, so the withholding is computed without opening a
  repository.
- [x] **TICKED 2026-09-09.** 3.4c A `path_only` entry whose `previous_sha256 != observed_sha256` is
  refused (finding code candidate `custody-path-class-digests-differ`). This leg
  is neutral because both digests are fields of the record; CONFIRMING a class
  against the measured diff needs the repository and belongs to the consumer's
  gate.
- [x] **TICKED 2026-09-09.** 3.5 **EXTEND `walk_strings` OVER THE NEW FIELDS** (design C-1 as
  corrected). `check_custody`'s blob-shape walk is the family's only
  "wherever it hides" guard, and siting the array outside `custody` leaves
  `custody_rederivations[].ruling_ref` and `.recorded_by` — the two unbounded
  free strings in the entry — outside it. Extend the walk over both, reusing the
  existing `BASE64_BLOB_RX` / `data:` / PDF-magic / multi-line predicates and
  the `embedded-original-content` finding code. The locators are opaque
  POINTERS and are walked on the same footing as `custody.locator` is today.

## 4. Fixtures — positive and negative, one per named refusal

- [x] **TICKED 2026-09-09.** 4.1 POSITIVE: `examples/consent-instrument/` gains an instrument carrying
  a two-entry unbroken chain (`header_only` / `lifecycle_header_edit`), admitted
  by the internal legs.
- [x] **TICKED 2026-09-09.** 4.2 POSITIVE: an existing example is left UNCHANGED and re-validated, to
  prove the growth is additive for an instrument that declares no array.
- [x] **TICKED 2026-09-09.** 4.1b POSITIVE: an instrument carrying an `archive_move` /
  `diff_class: path_only` entry whose locator pair DIFFERS and whose digests are
  EQUAL on both sides — the case a single-locator rule can never admit (design
  C-6a, `proposal.md` Example B).
- [x] **TICKED 2026-09-09.** 4.1c POSITIVE: the TWO-ENTRY chain shape the real repair needs — e1
  `archive_move`/`path_only`, e2 `lifecycle_header_edit`/`header_only` — modelled
  on prescription I in `design.md` § *The consumer handoff*. No fixture in the
  corpus exercises a multi-entry chain today.
- [x] **TICKED 2026-09-09.** 4.3 NEGATIVE `examples/consent-instrument/negative/`: a broken link
  (`eᵢ.previous_sha256 != eᵢ₋₁.observed_sha256`).
- [x] **TICKED 2026-09-09.** 4.3b NEGATIVE: a locator gap (`eᵢ.previous_locator !=
  eᵢ₋₁.observed_locator`) with the digests linking correctly — the half of the
  chain an earlier draft could not express.
- [x] **TICKED 2026-09-09.** 4.3c NEGATIVE: entries out of recorded-time order
  (`custody-chain-out-of-order`), so § 4's "one per named refusal" is true of
  that refusal too.
- [x] **TICKED 2026-09-09.** 4.4 NEGATIVE: a first entry whose `previous_sha256` is not the pin, and
  one whose `previous_locator` is not `custody.locator`.
- [x] **TICKED 2026-09-09.** 4.5 NEGATIVE: an unknown `diff_class` member, and an unknown `reason`
  member (schema-layer refusals).
- [x] **TICKED 2026-09-09.** 4.6 NEGATIVE: an entry omitting `ruling_ref`, and one omitting
  `recorded_by`.
- [x] **TICKED 2026-09-09.** 4.7 NEGATIVE: an entry carrying an ELEVENTH property (entry closure —
  the entry has TEN required fields since C-6a, so a "ninth" would not test the
  closure at all).
- [x] **TICKED 2026-09-09.** 4.8 NEGATIVE: a rewritten pin — `custody.sha256` advanced to an observed
  digest while the chain still claims the original anchor.
- [x] **TICKED 2026-09-09.** 4.8b NEGATIVE: a blob-shaped `ruling_ref` and a blob-shaped `recorded_by`
  (base64 run, `data:` URI, PDF magic or a multi-line body), each refused as
  `embedded-original-content` — the fixture that proves task 3.5 landed.
- [x] **TICKED 2026-09-09.** 4.8c **WITHHELD (neither positive nor negative — the third outcome):** an
  instrument whose last entry declares `diff_class: content` and whose internal
  legs are ALL SOUND, asserted to yield WITHHELD — **not a pass and not an
  error**. This is the fixture that proves task 3.4b landed, and the self-test
  harness needs a third expectation bucket to hold it, since today it can only
  say "valid" or "invalid for its intended finding".
- [x] **TICKED 2026-09-09.** 4.8d NEGATIVE: a `path_only` entry whose two digests differ.
- [x] **TICKED 2026-09-09.** 4.9 `examples/consent-instrument/README.md` updated with the new corpus
  counts, and the corpus count in `contracts/manifest.yaml`'s
  `consent-instrument` comment (*"5 valid + 5 invalid + purpose probes"*)
  re-measured rather than adjusted by arithmetic.

**§ 3 AND § 4 EVIDENCE, 2026-09-09.** Landed in ONE commit on branch
`033-add-consent-custody-rederivation-record` — **and the
`tests/consent_instruments/` package rides that SAME commit, because box 3.3
asks for a TEST that pins the absence, so its tick cannot precede the test that
is its evidence.** Transcripts under
`specs/033-add-consent-custody-rederivation-record/evidence/`:
`phaseD-consent-validator.txt`, `phaseC-exit-vocabulary.txt`,
`phaseE-pytest-consent-instruments.txt`, `phaseE-pytest-full.txt`,
`phaseE-baseline-preexisting-failures.txt`, `phaseD-manifest-digests.txt`,
`phaseD-scope-globs.txt`.

- **THE CORPUS, MEASURED by listing the directories** rather than by arithmetic:
  **9 valid** examples (7 instruments, 1 class registry, 1 purpose model),
  **21 indexed negatives**, **1 WITHHELD fixture** in the new third bucket, and
  2 purpose probes. `validate-consent-instruments.py --strict`: **0 errors, 0
  warnings, rc=0**.
- **The seven finding codes are adopted verbatim** and each has a fixture:
  `custody-chain-unanchored` (TWO fixtures, one per anchor half),
  `custody-chain-broken-link`, `custody-chain-locator-gap`,
  `custody-chain-out-of-order`, `custody-pin-rewritten` (multi-entry),
  `custody-path-class-digests-differ`, `custody-content-class-withheld`.
- **THE EXIT VOCABULARY IS MEASURED ON ALL FOUR PATHS**: a real instrument that
  withholds exits **3**; the packaged self-test exits **0** (the fixture is
  EXEMPT — an expected withholding is to the third bucket what an expected
  failure is to a negative); an instrument that withholds AND errors exits
  **1**, errors dominating; errors alone exit **1**. `3` is Brett Heap's ruling
  of 2026-09-09, verbatim *"Exit 3 = needs a human decision (Recommended)"*,
  held in ONE named constant.
- **§ 3.3's absence is pinned by 11 tests**, argument-scoped both ways: the
  source ban allowlists `SKIP_DIR_NAMES`' `".git"` by EXACT TOKEN (a
  directory-name exclusion is the opposite of reading a repository), and the
  runtime half patches `subprocess.run/Popen/check_output` and wraps
  `Path.open`/`open` to assert every opened path resolves UNDER the repository
  root — over all THREE buckets. `pytest tests/consent_instruments -q`: **34
  passed, rc=0**.
- **THE FULL SUITE WAS RUN, NOT ASSUMED**: `pytest tests/ -q -m "not postgres"`
  — **10512 passed, 36 skipped, 2 failed, rc=1**. **Neither failure names a
  consent surface, and BOTH are proven pre-existing by a BASELINE rather than by
  assertion**: the same two node ids fail identically in a separate clone at
  pristine `origin/main` (`e86eca35`), which carries none of this branch's
  bytes. One is a 30-second subprocess ceiling on a loaded workstation; the
  other resolves a pinned checkout that exists only in an aggregation workspace
  layout — a developer-worktree/runner divergence `pytest-suite.yml` itself
  records as expected rather than as a regression. **An uninitialized
  `openXwallet` gitlink is an ENVIRONMENT prerequisite of this gate**: it made a
  first attempt report 146 failures and errors that were entirely its absence,
  and CI initializes it in a dedicated App-token step before the suite.
- **§ 3.5's walk is proven over all four free strings × four blob predicates**,
  and proven NOT to fire on the two digests.

**ONE DEFECT IN A RATIFIED TASK'S PARAPHRASE WAS FOUND AND IS RECORDED, NOT
CODED AROUND.** Task 3.2's shorthand — *"custody.sha256 equals any entry's
observed_sha256 while a LATER entry exists"* — refuses `design.md` prescription
I, the estate's own measured repair, because a `path_only` move changes zero
bytes and so makes the pin equal e1's observed digest BY CONSTRUCTION. Applied
literally it would make `reason: archive_move` unusable by any conforming
record — the exact failure C-6a was raised to fix. The delta governs: it speaks
of a digest *"written back into custody.sha256"* and of leaving the pin
*"verbatim"*, so the implemented leg is ANCHOR-RELATIVE. Full write-up:
`specs/033-add-consent-custody-rederivation-record/evidence/FINDING-pin-leg-contradiction-2026-09-09.md`.

## 5. The contract cut

- [ ] **NOT-OWED-HERE 2026-09-09 — the LANE's act, reported not performed.** 5.1 **[OPERATOR-adjacent] CLAIM THE VERSION NUMBER on openxFactory issue
  #630, row 4 (Contract cuts), AT CUT TIME AND NOT BEFORE.** Row 4's rule is
  *"Claim the **version number**, not the files"*, and `docs/contract-versioning-policy.md`
  § *Bundle Realization Order* step 1 allocates it at the final integration
  point. Measured at authoring, the next additive minor is `contract-v3.5`
  (`contracts/manifest.yaml:3` declares `contract-v3.4`; `contracts/releases/`
  holds `contract-v3.4.digests.yaml` as its highest) — **a measurement, not a
  reservation**. Re-measure at the cut; a sibling cut may have taken it.
- [x] **TICKED 2026-09-09.** 5.2 Realization order steps 1–2: fetch, integrate onto the final
  integration point, re-check availability, allocate, then move every release
  surface atomically in ONE candidate commit — `contracts/manifest.yaml`
  (`contract_bundle_version`, the `consent-instrument` row's `sha256` — today
  `13b0fe46…` — and its `consumption_rule`), `contracts/CHANGELOG.md`, and
  `contracts/releases/<version>.digests.yaml`.
- [x] **TICKED 2026-09-09.** 5.3 The CHANGELOG entry names what changed in the bundle, not what this
  session intended: § *Version Identity* requires one entry per release listing
  every contract added, changed or deprecated, and a bundle is a commit's whole
  tree.
**§ 5.2 AND § 5.3 EVIDENCE, 2026-09-09.** The candidate is ONE commit on branch
`033-add-consent-custody-rederivation-record`, taken after Phases B–F, over the
integration point `9d658813` (a MERGE of `origin/main@587f21a0`, never a
rebase). Transcripts:
`specs/033-add-consent-custody-rederivation-record/evidence/phaseG-T060-measurement.txt`
and `.../phaseG-T061a-T061c-coupling.txt`.

- **THE NUMBER WAS MEASURED AT THE INTEGRATION POINT, NOT RESERVED BEFORE IT.**
  `contract-v3.4` on all three surfaces — `contracts/manifest.yaml:3`, the
  highest `contracts/releases/` inventory, and the highest `contract-v*` tag —
  so **`contract-v3.5` is free**. Main had moved 39 commits, SEVEN under
  `contracts/`, since the previous measurement; this is the one that counts.
  **The CLAIM on issue #630 row 4 is the LANE's and is not made here** (box 5.1).
- **EVERY RELEASE SURFACE MOVES IN THE ONE COMMIT**: `contract_bundle_version`
  → `contract-v3.5`; the `consent-instrument` row's new `consumption_rule`
  paragraph, inserted BEFORE the closing sentence in the `contract-v1.33` slot;
  `contracts/CHANGELOG.md`; and `contracts/releases/contract-v3.5.digests.yaml`,
  **BUILT by `validate-contract-release.py build`, never hand-edited** — 283
  entries, delta ZERO against `contract-v3.4`'s 283.
  **The row's `sha256` needed no move**: `2b834492…` was re-derived in § 2's own
  commit, so it is verified current here rather than edited, and no commit on
  this branch was ever left with a stale digest.
- **THE CUT-COUPLED TESTS ARE MEASURED FROM THE LAST CUT, NOT ASSUMED.**
  `807a4f47` moved SIX files, not four. `test_release_boundary.py` takes all
  three edits — the `FEATURE_SUCCESSOR_9` member, BOTH match arms, and a
  hand-written paragraph whose "membership unchanged" claim is measured twice
  over (three registered rows differ at this candidate, none of them an
  intent-compliance member; and the member set itself returns ZERO changed
  paths since `contract-v3.4`). `test_clearing_manifest_rows.py` takes **NO
  EDIT**, measured by running it: its only failure was the absent inventory,
  which `build` then created — the outcome `807a4f47` engineered when it
  repaired that file's bundle-version equality rather than re-pinning a number
  that would fail again here.
- **THE CHANGELOG NAMES THE BUNDLE, NOT THE SESSION.** Nineteen paths — 4
  additions, 15 modifications — each attributed to its originating change or
  pull request, and the ADDITIVE class argued row by row rather than asserted:
  the consent schema is the ONLY `*.schema.yaml` in the bundle and grows one
  optional property; `manifest.yaml` and `contracts/README.md` are editorial;
  the eight `examples/` files are corpus under a rename sweep; the four pin
  files change a TARGET and not a shape. Nothing removed, no enumeration
  narrowed, nothing deprecated. The entry also records what the bundle does NOT
  do: the rule is declared and enforced nowhere, and no custody pin is repaired.

- [x] **TICKED 2026-09-09.** 5.4 Step 3: run every gate against that exact unchanged candidate —
  `release-tag-gate` (which evaluates any PR touching `contracts/manifest.yaml`
  or `contracts/releases/`), `pytest-suite`, `scripts/validate-manifest-digests.py`,
  `scripts/validate-contract-release.py`, `scripts/validate-consent-instruments.py`.
- [ ] **NOT-OWED-HERE 2026-09-09 — the LANE's act under `plan.md`'s landing contract.** 5.5 Step 4: land the exact reviewed commit. If promotion creates a
  different commit, that commit becomes the candidate and every gate reruns.
- [ ] **NOT-OWED-HERE 2026-09-09 — an [OPERATOR] act at the LANDED MERGE COMMIT.** 5.6 **[OPERATOR]** Step 5: publish the annotated tag at the exact
  published commit and verify it from an independently refreshed checkout. The
  gate records the tag as OWED and does not require it before step 4; the
  obligation is on whoever lands step 4.

**§ 5.4 EVIDENCE, 2026-09-09.** All five gates were run against the EXACT
UNCHANGED candidate `d54d89ca`, nothing edited between forming it and running
them. Transcript:
`specs/033-add-consent-custody-rederivation-record/evidence/phaseG-T064-gates.txt`.

- **`release-tag-gate` — rc=0**, *"the release-tag obligation holds over the
  merge tree d54d89caf: no error, no warning"*, run with an **EXPLICIT
  `--base 587f21a0`**. The default resolves `--base` to the head's FIRST PARENT,
  which on a branch that integrated by merging `main` INTO it is this branch's
  own prior tip — it would diff the wrong tree and return a near-empty result
  that LOOKS like a pass. `TAG OWED` is the expected state, not a finding: the
  tag is step 5 and box 5.6's, at the landed merge commit.
- **the full suite — 10662 passed, 36 skipped, 1 failed**, and that one failure
  is PROVEN pre-existing by a baseline in a separate clone at pristine
  `origin/main`. It resolves a pinned checkout that exists only in an
  aggregation workspace layout. **Both cut-coupled tests pass at the candidate**
  — `test_release_boundary.py` with its three edits, `test_clearing_manifest_rows.py`
  with NONE.
- **`validate-manifest-digests.py` — rc=0**, 189 per-file digests verify.
- **`validate-contract-release.py verify-commit --commit d54d89ca` — rc=0**,
  the inventory re-derived against the candidate itself rather than trusted.
- **`validate-consent-instruments.py --strict` — rc=0**, 0 errors, 0 warnings,
  0 withheld.
- **doc-health, as a TWO-REPORT PAIR** with identical report and checkout
  basenames and one pinned `--as-of`: **ZERO findings added at any severity in
  any family**, and THREE `release-inventory-drift` findings REMOVED — the same
  three registered rows the § 5.2 measurement independently found had moved.
  The new `withheld/` bucket, the eighteen fixtures and the new test package
  trip no family at all. Transcript: `.../evidence/phaseH-T080-doc-health.txt`.

## 6. The consumer handoff — [OpsxFactory]'s OWED ACT, not this change's

**Listed for completeness and explicitly OUTSIDE this change's archive gate.**
This change archives on ITS realization evidence (§§ 2–5 merged and green); the
items below are OpsxFactory's, in OpsxFactory's own change, under OpsxFactory's
own gates.

- [ ] **NOT-OWED 2026-09-09 — the CONSUMER's, in OpsxFactory's own change.** 6.1 `[OpsxFactory]` Advance `stack.yaml` `contract_ref` (today
  `724a2a4f…`) to the cut bundle's commit **in lockstep with the
  worker-enrollment-broker's runtime-shape validation** — the pin and the
  broker's declared shape move in one act, or the `pin_gap_misdeclared` guard
  fails the advance closed.
- [ ] **NOT-OWED 2026-09-09 — the CONSUMER's, in OpsxFactory's own change.** 6.2 `[OpsxFactory]` Write the THREE PRESCRIPTIONS set out verbatim in
  `design.md` § *The consumer handoff* — and **NO `amendments` entry** anywhere
  (design C-10). **They are NOT uniform**, and an earlier draft of this task
  wrongly prescribed one entry apiece with equal locators. Two of the three
  targets had ALREADY moved before `57fd9fd2` (`add-tenant-reader-grant-pipeline`
  archived at `a98fca5b`, `add-managed-service-inventory` at `0ebb1191`, both
  ancestors of `57fd9fd2`), so their `custody.locator` is a pre-archive path
  absent on BOTH sides of `57fd9fd2` and a single entry is refused whichever
  locator it names:
  - **`opensoft-exchange-monitor`** — TWO entries: e1 `archive_move`/`path_only`
    at `a98fca5b…` (locators differ, both digests `bb8f89ea…`); e2
    `lifecycle_header_edit`/`header_only` at `57fd9fd2…` (both locators the
    archive path, `bb8f89ea…` → `5c87d547…`). HEAD = `5c87d547…`.
  - **`opsx-farheap-service-discovery`** — TWO entries: e1 at `0ebb1191…` (both
    digests `b5d4ab55…`); e2 at `57fd9fd2…` (`b5d4ab55…` → `d9eecee3…`).
    HEAD = `d9eecee3…`.
  - **`opsx-opensoft-node-inventory`** — ONE entry, the only uniform case: never
    archived, both locators = `custody.locator`, `31e4f889…` → `7fc4bb21…`.
    HEAD = `7fc4bb21…`.
  Re-measure each digest at write time rather than copying these; they were
  taken at the OpsxFactory tree on 2026-09-07.
- [ ] **NOT-OWED 2026-09-09 — the CONSUMER's, in OpsxFactory's own change.** 6.2b `[OpsxFactory]` **DECLARE THE CUSTODY STORE MAPPING** that resolves
  `opsx:<tenant>/<repo-relative path>`, which the ADDED requirement obliges of
  any repository holding instruments, and **operate the custody-digest check**
  that performs the re-derivation legs (the C-7 obligation; F.2's gate is where
  it lands).
- [ ] **NOT-OWED 2026-09-09 — the CONSUMER's, in OpsxFactory's own change.** 6.3 `[OpsxFactory]` Write NO entry for `57fd9fd2` on
  `opsx-farheap-node-inventory-reader-consent.yaml`: its content pin is not
  broken. Its LOCATOR did move when `add-managed-service-mapping` archived
  (2026-08-26), so it is a candidate for a separate `archive_move` entry with a
  differing locator pair and an unchanged digest on both sides — the first real
  exercise of the path pair, and the consumer's call.
- [ ] **NOT-OWED 2026-09-09 — the CONSUMER's, in OpsxFactory's own change.** 6.4 `[OpsxFactory]` Discharge F.1 in the owed-findings register — **(archive
  in flight; the live path until then is
  `openspec/changes/add-pre-archive-citation-gate/supporting-docs/owed-findings.md`)**
  — which archives 2026-09-07 to
  `openspec/changes/archive/2026-09-07-add-pre-archive-citation-gate/supporting-docs/owed-findings.md`,
  by citing the change that performed the repair.

## 7. Named as owed elsewhere, and deliberately not taken here

- [ ] **NOT-OWED 2026-09-09 — named as owed elsewhere, performed nowhere here.** 7.1 **F.2's custody-digest gate is NOT built here.** Ruled scope: *"every
  in-repo sha256 pointer to an in-repo target"*. Owner: OpsxFactory, its own
  change. This packet supplies only the consent-custody family's re-derivation
  rule, which that gate consumes.
- [ ] **NOT-OWED 2026-09-09 — named as owed elsewhere, performed nowhere here.** 7.2 **F.3 is NOT settled here.** The *"both at once"* ruling asks for an
  OpsxFactory change AND an openxFactory change amending the promoted
  `document-lifecycle` capability. This packet is neither and touches no
  `document-lifecycle` requirement.
- [ ] **NOT-OWED 2026-09-09 — named as owed elsewhere, performed nowhere here.** 7.3 **No other content-address family is given a re-derivation record.**
  Whether plan-acceptance desired-state refs, evidence digests, fence baselines
  or contract pins want the same shape is a question F.2's inventory answers,
  not this one.

---

**NOTE, 2026-09-09 — WHAT LANDING THIS DECLARES, AND WHAT IT DOES NOT ARM.**
Landing this realization **DECLARES** the consent family's re-derivation rule.
Under `govern-archived-record-edits`' TRANSITION CLAUSE that matters: an edit of
a consent pinned target converts from **REPORTED** to **REFUSED** for that
family. **It converts ONCE F.2's GATE EXISTS, and that gate is § 7.1's —
OpsxFactory's own.** Nothing here builds it, schedules it, or arms it, and no
consequence of this note is takeable in this repository. It is recorded so that
the conversion is a known consequence of landing rather than a surprise found
later. The same note is carried in the realization evidence.

**OWED FINDING, 2026-09-09 — THE IDENTICAL-LOCATORS `path_only` GAP. RECORDED,
DELIBERATELY NOT CLOSED.**

- **(a) The defect.** `diff_class: path_only` means *only the locator changed*.
  An entry declaring it with `previous_locator == observed_locator` — and
  therefore, by task 3.4c's leg, equal digests on both sides — records an event
  that DID NOT OCCUR: nothing moved and nothing changed. Nothing in the schema,
  in the validator as realized, or in the ratified delta refuses it.
- **(b) The leg it would need, and why that leg is NEUTRAL.** A check that
  `previous_locator != observed_locator` whenever `diff_class: path_only`.
  **Design C-7's placement test puts it on THIS side of the line**: both
  locators are fields of the record, so the contradiction is derivable from the
  record's own bytes without opening a repository — the identical test that
  placed `path_only` digest equality (task 3.4c) here rather than with the
  consumer.
- **(c) Its home.** F.2's custody-digest gate (§ 7.1, OpsxFactory's) or a
  SUCCESSOR openxFactory change. **It is owed somewhere; it is not owed here** —
  no ratified task names it, and this packet's rule is realize-what-was-ratified.
  **DO NOT add the refusal leg under this change.**

**OWED FINDING #3, 2026-09-09T20:31Z — THE `status`/`custody_rederivations`
CONFLICT IS UNREFUSED. RECORDED, NOT CLOSED.** Raised by the refutation panel on
`528c690c`.

- **(a) The defect.** The ratified delta's scenario *A re-derivation does not
  amend the instrument* ends: *"an instrument transitioned to `amended` solely
  for a custody re-derivation is nonconformant, because nothing the parties
  agreed has changed."* **Nothing refuses it.** The scenario is recorded in the
  feature's traceability table as realized *"as an ABSENCE, asserted by diff"* —
  which is true of its FIRST half only (this change writes no `amendments` entry
  and moves no status). The AND-clause is a REFUSAL, and no refusal was built.
- **(b) The leg it would need, and why it is NEUTRAL.** `status`,
  `amendments` and `custody_rederivations` are ALL fields of the record, so
  **design C-7's placement test puts the leg on THIS side of the line** — the
  same test that placed `path_only` digest equality and the entry-closure legs
  here. The DERIVABLE form, stated precisely because the ratified wording is
  not fully derivable: an instrument whose `status` is `amended`, which declares
  `custody_rederivations`, and whose `amendments` array is absent or empty, has
  **no recorded amendment to justify the transition** — and that is decidable
  from the record's own bytes. The literal wording's *"solely"* is NOT decidable
  in the general case: an instrument may be legitimately `amended` AND carry a
  re-derivation, and the record does not say which act moved the status. A leg
  built to the literal wording would over-refuse; the empty-`amendments` form is
  the honest neutral approximation, and choosing between them is a contract
  question rather than an implementation one.
- **(c) Its home.** F.2's custody-digest gate (§ 7.1, OpsxFactory's) or a
  SUCCESSOR openxFactory change, together with the ruling on (b)'s two forms.
  **NO LEG WAS ADDED HERE**: no ratified task names one, and this packet's rule
  is realize-what-was-ratified.

**OWED FINDING #4, 2026-09-09T20:31Z — THE CONSENT SCHEMA IS NOT A RELEASE
INVENTORY MEMBER, AND THE POLICY SAYS IT SHOULD BE. PRE-EXISTING, NOT THIS
CUT'S.** Also raised by the panel.
`contracts/releases/contract-v3.5.digests.yaml` carries **283** entries and
**none of them is `contracts/schemas/consent-instrument.schema.yaml`** —
`grep -c consent-instrument` over the built inventory returns 0. The cause is
STATIC MEMBERSHIP: `scripts/hermes_runtime_validation/release.py` enumerates the
inventory from fixed tuples (`AUXILIARY_MEMBERS`, `NORMATIVE_DOCS`,
`RELEASE_SURFACE_PATHS` and the hermes-runtime / intent-compliance families),
so a normative contract outside those families is never a member however much it
moves. `docs/contract-versioning-policy.md` speaks of every modified normative
contract. **THE TWO DIVERGE, AND THEY DIVERGED BEFORE THIS CUT** — the schema
was equally absent from `contract-v1.30`'s, `contract-v1.33`'s and
`contract-v3.4`'s inventories, at every bundle that carried it. It is recorded
as a tool/policy divergence owed to whoever owns that membership list, and it is
**NOT** repaired here: hand-adding a row to a BUILT inventory is precisely the
edit the versioning policy forbids.

**BOX ACCOUNTING, 2026-09-09 — AND IT SUMS TO 46.**
**35 TICKED** (0.1; 1.1–1.3; 2.1–2.5; 3.1–3.5 incl. 3.4b and 3.4c; 4.1–4.9 incl.
4.1b, 4.1c, 4.3b, 4.3c, 4.8b, 4.8c, 4.8d; 5.2, 5.3, 5.4)
**+ 3 NOT-OWED-HERE** (5.1 the lane claims the number, 5.5 the lane's landing
bookkeeping, 5.6 the `[OPERATOR]` tag)
**+ 8 NOT-OWED** (6.1, 6.2, 6.2b, 6.3, 6.4; 7.1, 7.2, 7.3)
**= 46.** Every tick rides the same commit as its evidence, proven from history
rather than asserted at `.../evidence/phaseH-T083-tick-audit.txt`.
**THAT AUDIT COVERS THE PACKET'S 46 BOXES.** The Speckit feature tree's own 79
`T###` boxes are a separate list, ticked 2026-09-09T20:31Z with per-phase dated
evidence pointers; two of them (T065, T066) carry NOT-OWED-HERE lines because
they mirror boxes 5.5 and 5.6, which are the lane's and the operator's.
