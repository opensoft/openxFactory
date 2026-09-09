# Feature Specification: The consent instrument grows a re-derivable custody record, and the bundle is cut on it

**Feature Branch**: `033-add-consent-custody-rederivation-record`
**Created**: 2026-09-09
**Status**: Draft
**Realizes**: openxFactory OpenSpec change `add-consent-custody-rederivation-record`
**Lane**: opsXfactory-1

**RATIFICATION CITATION — AND THE ONE PLACE IT DIFFERS FROM THIS TREE'S
PRECEDENT, STATED RATHER THAN GLOSSED.** The packet was ratified 2026-09-08 by
Brett Heap (reviewer of record; openxFactory operator authority), in session,
first-hand to lane `opsXfactory-1` (harness session
`ee808615-4d8a-475f-bcb3-6f92a89909f0`), verbatim *"ratify 774, merge it and
land it"*, recorded at
`openspec/changes/add-consent-custody-rederivation-record/review/ratification-2026-09-08.md`
against the ratified baseline `6cfe9ba6628b21649953c83c5b4fe1ade1eda76c`.

**THERE IS NO GITHUB APPROVING REVIEW ON #774, AND THAT IS MEASURED, NOT
ASSUMED.** `gh api repos/opensoft/openxFactory/pulls/774/reviews` returns
EXACTLY ONE review — `sourcery-ai[bot]`, state `COMMENTED`, 2026-09-08T03:26:05Z
at head `ab27744b` — and no `APPROVED` state from any user. The immediately
preceding realization in this tree (`specs/032-govern-archived-record-edits`)
could cite a CLI approval (`gh pr review 788 --approve`, review 5141756427,
APPROVED 2026-09-08T12:38:36Z); this one cannot, because none exists. What
exists instead, and what every § 1 evidence note in this feature cites:

- the in-repo ratification record named above, written by the same lane from the
  same session that heard the word (its own § *Ratification hygiene* says so);
- Brett Heap's own merge of #774 — `merged_by: brettheap`, `merged_at:
  2026-09-08T03:48:44Z`, merge commit `543d47a96970d48b1c988e2293927c800bb1ff08`
  over head `0d541576` (the PR was authored by `openxfactory[bot]`, so the merge
  is the operator's act and not a self-merge of his own authorship);
- his `LANDING` comment at 2026-09-08T03:48:41Z and `LANDED … PR #774 →
  543d47a9…` at 2026-09-08T03:50:16Z on the same pull request.

A note that cites a GitHub approval where none was given would be a false
record, so no note in this feature does.

**THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE.** Every requirement below
is a REALIZATION act. Nothing here restates, narrows or widens the ratified
delta in
`openspec/changes/add-consent-custody-rederivation-record/specs/consent-instrument/spec.md`
(ONE `## MODIFIED` + ONE `## ADDED`, 22 scenarios), and no act in this feature
edits it. Where this file and the packet appear to differ, the packet governs
and this file is the defect.

**Input**: Realize §§ 0–5 of the packet's 46-box task list — the schema growth
(§ 2), the canonical validator's internal legs and the WITHHELD outcome (§ 3),
the fixture corpus including a third expectation bucket (§ 4), and THE CONTRACT
CUT (§ 5) up to but not including the annotated tag — through to a branch whose
gates are green and whose evidence is recorded in both the Speckit tree and the
packet's `evidence/` directory.

## Measured baseline

Every figure below was measured on this branch at its creation point (`main`
`6df21737`, worktree
`.../openxFactory-worktrees/033-add-consent-custody-rederivation-record`), not
carried forward from the packet.

| Fact | Measured value |
| --- | --- |
| Feature number | `033` — `specs/` on `main` ends at `032-govern-archived-record-edits`; `git branch -r` shows no `033-*` on origin. No collision. |
| Packet task boxes | 46, ZERO ticked (§ 0: 1, § 1: 3, § 2: 5, § 3: 7, § 4: 16, § 5: 6, § 6: 5, § 7: 3). |
| Boxes in this feature's scope | **35 to TICK** (§ 0.1, § 1.1–1.3, § 2.1–2.5, § 3.1–3.5, § 4.1–4.9, § 5.2–5.4); **3 NOT-OWED-HERE** (§ 5.1 the lane's claim, § 5.2's number MEASURED and reported by me; § 5.5 the lane's landing bookkeeping; § 5.6 `[OPERATOR]` tag); **8 NOT-OWED** (§§ 6–7). 35 + 3 + 8 = 46. |
| `contract_schema_version` today | `2` (`contracts/schemas/consent-instrument.schema.yaml:16`). |
| `custody` object today | closed to exactly `{locator, sha256}`, `additionalProperties: false`. |
| Canonical validator | `scripts/validate-consent-instruments.py`, 862 lines; `Findings` carries `errors` / `warnings` / `notes` ONLY; exit codes documented `0 ok, 1 findings, 2 dependency/harness error`. |
| Validator baseline on this branch | `0 error(s), 0 warning(s)`; self-test reports **6 valid**, **7 negative**, 2 purpose probes. |
| Packaged corpus on disk | 6 `*.example.yaml` (4 of them instruments, 1 class registry, 1 purpose model) + 7 `negative/*.yaml`. |
| `contracts/manifest.yaml` `consent-instrument` row | `sha256: 13b0fe46fdb8791020b426dcd763aced2a3280a82923b32d3a0d0877ab6ad441`, and `sha256sum` over the file returns the same value — the pin is CURRENT and must be re-derived when the schema moves. |
| Manifest corpus comment | *"5 valid + 5 invalid + purpose probes"* — ALREADY FALSE against the 6/7 on disk, before this feature adds a byte. Task 4.9's *"re-measured rather than adjusted by arithmetic"* is why. |
| `contract_bundle_version` | `contract-v3.4` (`contracts/manifest.yaml:3`). |
| Highest release inventory | `contracts/releases/contract-v3.4.digests.yaml`, 283 entries. |
| Highest `contract-v*` tag | `contract-v3.4`, annotated, at `807a4f47` (squash merge of PR #653, 2026-09-04). |
| **Next additive minor, MEASURED** | **`contract-v3.5`** — free on all three surfaces. `contract-v2.6` is the SPENT number, not this one. |
| Is the consent schema a release-inventory member? | **NO.** `contract-v3.4.digests.yaml` carries five `contracts/schemas/*` paths and `consent-instrument.schema.yaml` is not among them. Membership is closed over what `scripts/hermes_runtime_validation/release.py` `_collect_members` enumerates from the catalog. So the schema edit re-bases the manifest's per-file `sha256` but adds no inventory row. |
| `contracts/` delta since `contract-v3.4` | **4 additions, 14 modifications** — `openspec-cli-pin.yaml`, `openspec-cli-pin.1.12.0.package-lock.json`, `policies/repository-identity.yaml`, `review-lane-repin-binding.template.yaml` added; `README.md`, `manifest.yaml`, `openreposhape-pin.yaml`, `openxwallet-pin.yaml`, `review-lane-pin.yaml`, `review-lane-floor-snapshot.yaml` and eight `hermes-domain-overlay`/`omnigent` example fixtures modified. **None of these is this session's**, and § 5.3 requires the CHANGELOG entry to name them anyway: a bundle is a commit's whole tree. |
| The deferred cut this bundle inherits | `2026-09-08-publish-openspec-cli-pin-as-contract-member` chose **A-defer** (register now, cut later) over **A-cut** (`contract-v3.5` in that PR), unvetoed. Its registration therefore rides THIS bundle. |
| Ledger row | `add-consent-custody-rederivation-record: {state: active, class: co-modifier, declares: [add-consent-instrument], depth: 1, prose: false, moved_by: "#774", moved_on: "2026-09-07"}` — `moved_by` is the REAL merged pull request. Task 0.1's act is DONE (commit `6cfe9ba6`). |
| Pinned OpenSpec CLI | `@fission-ai/openspec@1.12.0` via `scripts/validate-openspec-cli-pin.py`; `--change … --strict` returns **1 passed, 0 failed** at this branch's head. |
| CI test invocation | `python3 -m pytest tests/ -q -m "not postgres"` (`.github/workflows/pytest-suite.yml:462`). There is **no `tests/consent*` directory** — task 3.3's no-git assertion needs a new home. |

## User Scenarios & Testing *(mandatory)*

### User Story 1 — The contract can say that a pinned target moved (Priority: P1)

A repository holding an executed consent instrument discovers that the target
`custody.locator` names no longer hashes to `custody.sha256`, and the move was
authorized. Today the schema offers `amendments[].delta` free prose or nothing.
After this feature the schema offers a closed, machine-checkable sibling record.

**Why this priority**: nothing else in the packet is realizable until the shape
exists. The validator legs check it, the fixtures instantiate it, and the cut
publishes it.

**Independent test**: an instrument carrying a well-formed
`custody_rederivations` entry validates; the same instrument with an eleventh
property, an unknown `diff_class`, or a missing `ruling_ref` is refused at the
schema layer.

**Acceptance**:

1. **Given** the grown schema, **When** an instrument declares a
   `custody_rederivations` array of closed ten-field entries, **Then** it
   validates and `custody` still carries exactly `locator` and `sha256`.
2. **Given** the grown schema, **When** an existing instrument declares no
   array, **Then** it validates unchanged — the growth is additive.
3. **Given** the grown schema, **When** the record envelope is read, **Then**
   `schema_version` is still `const: 1` and `contract_schema_version` is `3`.

### User Story 2 — The canonical validator checks what it can see, says what it did not, and mints a third outcome (Priority: P1)

The neutral validator holds no consumer repository, so it can check the chain's
internal legs and nothing about the target's bytes. It must check every internal
leg, refuse a rewritten pin, report a `content`-class chain as WITHHELD rather
than as a pass or a plain error, and state in its own report line that a pass is
not a currency claim.

**Why this priority**: the packet's `code_surface` declaration names this file,
and the WITHHELD outcome is the CI-visible behaviour change every consumer of
this validator will see.

**Independent test**: run `scripts/validate-consent-instruments.py --strict` over
the packaged corpus and confirm the three outcome classes are distinguishable in
the report line and in the process exit status.

**Acceptance**:

1. **Given** a chain whose first entry's `previous_sha256` is not
   `custody.sha256`, **When** the validator runs, **Then** it reports
   `custody-chain-unanchored` and does not fall back to comparing HEAD.
2. **Given** a chain whose entries link in digest but not in locator, **When**
   the validator runs, **Then** it reports `custody-chain-locator-gap`.
3. **Given** an instrument whose `custody.sha256` equals an entry's
   `observed_sha256` while a later entry exists, **When** the validator runs,
   **Then** it reports `custody-pin-rewritten`.
4. **Given** an instrument whose last entry declares `diff_class: content` and
   whose internal legs are all sound, **When** the validator runs, **Then** the
   run names it WITHHELD beside its error and warning counts and exits in the
   status class that means "needs a human decision", not "is malformed".
5. **Given** a `ruling_ref` carrying a 200-character base64 run, **When** the
   validator runs, **Then** it reports `embedded-original-content` — the
   `walk_strings` guard followed the custody facts to their new home.
6. **Given** any instrument at all, **When** the validator runs, **Then** it
   opens no git repository, shells out to no `git`, and reads no file named by
   a locator — and a test asserts that absence.

### User Story 3 — The corpus carries one fixture per named refusal, and a third bucket (Priority: P2)

The packaged self-test today can express only "valid" or "invalid for its
intended finding". The WITHHELD case is neither.

**Why this priority**: the fixtures are what prove Stories 1 and 2 landed; the
third bucket is a shape change to `self_test`, not a row.

**Independent test**: the self-test's own note line reports the three bucket
counts, and removing any one fixture reddens it.

**Acceptance**:

1. **Given** the corpus, **When** the self-test runs, **Then** every positive
   validates, every negative fails for its declared finding, and every withheld
   fixture yields WITHHELD — not a pass and not an error.
2. **Given** a negative fixture on disk with no table entry (or vice versa),
   **When** the self-test runs, **Then** it fails closed, as it does today.
3. **Given** the README and the manifest comment, **When** they are read after
   this feature, **Then** their corpus counts are the MEASURED counts.

### User Story 4 — The bundle is cut on the whole tree, not on this session's intention (Priority: P2)

`contract-v3.5` is allocated at the final integration point, every release
surface moves in one candidate commit, the CHANGELOG entry names every contract
added or changed since `contract-v3.4` (including four this session did not
author), and the annotated tag is left OWED for the operator.

**Why this priority**: the cut is what makes the growth consumable, and
`release-tag-gate` evaluates any pull request touching the release surface.

**Independent test**: `validate-contract-release.py verify-commit --commit
<candidate>` and `validate-release-tag-gate.py` both pass on the exact
unchanged candidate.

**Acceptance**:

1. **Given** the final integration point, **When** the version is allocated,
   **Then** availability is RE-CHECKED at that point and not read from this
   file.
2. **Given** the candidate commit, **When** it is inspected, **Then**
   `contracts/manifest.yaml` (bundle version, the `consent-instrument` row's
   `sha256` and its `consumption_rule`), `contracts/CHANGELOG.md` and
   `contracts/releases/contract-v3.5.digests.yaml` all moved in it.
3. **Given** the digest inventory, **When** it is produced, **Then** it was
   BUILT by `validate-contract-release.py build` and never hand-edited.
4. **Given** the landed commit, **When** it differs from the reviewed candidate
   (a squash merge does differ), **Then** every gate reruns against the landed
   commit before the tag is owed against it.

## Primary flow, in one ordered narrative

1. § 0.1 and § 1.1–1.3 are TICKED with evidence — their acts are already
   performed and verifiable; nothing is re-performed to tick them.
2. The schema grows (§ 2), `custody` proven byte-identical by diff.
3. The validator grows its internal legs, the WITHHELD outcome and the extended
   blob walk (§ 3), with the no-git absence pinned by a test.
4. The corpus grows positives, negatives and the withheld fixture, and
   `self_test` grows a third expectation bucket (§ 4).
5. Gates run on the pre-cut tree.
6. The cut is taken LAST (§ 5.2–5.5): fetch, integrate, re-measure availability,
   allocate, move every release surface atomically, re-run every gate against
   that exact unchanged candidate.
7. Evidence is written to both trees; §§ 6–7 take dated NOT-OWED lines.

### Edge Cases

- **The version number is taken while this branch is open.** § 5.1's measurement
  is explicitly *"a measurement, not a reservation"*. The allocation step
  re-measures at the integration point and the branch re-numbers rather than
  landing a stale one.
- **A squash merge changes the commit.** The versioning policy's step 4 already
  rules this: the landed commit becomes the new candidate and gates rerun. This
  feature does not treat the pre-merge green as the post-merge green.
- **`self_test`'s third bucket changes a contract other repositories read.** The
  packet's `code_surface` says so in as many words; the CHANGELOG entry records
  it as a consumer-visible behaviour change of the validator.
- **The manifest corpus comment is already stale.** Re-measure, do not increment.
- **A `content`-class fixture must not redden CI — and the constraint turned out
  not to bind.** MEASURED at clarify round 1: **no caller reads this validator's
  exit code today** — not one of the twelve workflows, no pytest, and no
  OpsxFactory leg. So a new nonzero status for WITHHELD reddens nothing, and the
  PACKAGED withheld fixture is exempt from it in any case (an expected
  withholding is to the third bucket what an expected failure is to a negative).
- **The exit-code NUMBER is not this feature's to rule.** It is planned on `3`
  behind a single named constant, parked for Brett Heap. A different ruling
  moves the constant and nothing else.

## Clarifications

### Session 2026-09-09 — architect seat (lane `opsXfactory-1`), after cross-model adversarial review

Twelve questions asked and RULED; answers are written inline beneath each
question in
`specs/033-add-consent-custody-rederivation-record/clarify-questions.md`, with
two additions (A1, A2) the review raised. The binding effects on this
specification:

- **Q1** — ONE pull request carries §§ 2–5 (§ *Version Identity* requires the
  manifest and changelog to move atomically with the contract files). The
  version number is re-measured and CLAIMED BY THE LANE at the last
  merge-from-main before the merge; the PR body names `contract-v3.5` as a
  provisional MEASURED candidate. **The landing contract is recorded in
  `plan.md`.** § 5.5 and § 5.6 are NOT-OWED-HERE.
- **Q2** — **PARKED FOR BRETT**, planned on a new exit code for "needs a human
  decision", provisionally `3`, behind a single named constant. The refutation
  of the exit-0 reading is accepted: task 3.4b requires *"the exit status the
  repository rules"* and the delta says WITHHELD is *"never a pass"*, and the
  supposed CI constraint does not bind because no caller reads the code.
- **Q3** — `examples/consent-instrument/withheld/` +
  `EXPECTED_WITHHELD_OUTCOMES`, fail-closed both ways; `repo_scan` reports
  WITHHELD as found.
- **Q4** — only `contract_schema_version` moves.
- **Q5** — **NO SPLIT**: the manifest's digest re-derivation, bundle version and
  `consumption_rule` paragraph ALL ride the single § 5.2 candidate commit,
  because intermediate branch commits are ungated (CI runs at the PR head).
  § 2's commit leaves the digest stale on purpose and says so.
- **Q6** — the CHANGELOG attributes all 4 additions and 14 modifications since
  `contract-v3.4`; ADDITIVE minor.
- **Q7** — `tests/consent_instruments/`; BOTH fixture and parametrized pytest
  for the walk; BOTH source-level ban and runtime patch over ALL THREE buckets.
- **Q8** — amend three README sites in the `3b530009` form (this packet's own
  row; `README.md:3022`, keeping *"the three pins are still broken"*; and
  `README.md:2993`, the load-bearing premise of `govern-archived-record-edits`'
  transition clause). The LANE posts the substrate note for the two sibling-row
  sentences BEFORE they are written.
- **Q9** — tree and table complete, nine new *Named cases* bullets, a third
  table column.
- **Q10** — all seven finding codes adopted verbatim.
- **Q11** — § 5.4 ticks on the local run of all five gates against the exact
  candidate.
- **Q12** — walk the whole entry minus the two digest fields.
- **A1** — `contracts/README.md:102` carries a corpus count task 4.9 does not
  name, already false at 6/7; an ADDITIONAL realization act corrects it.
- **A2** — landing DECLARES the consent family's re-derivation rule, which under
  `govern-archived-record-edits`' transition clause converts that family from
  REPORTED to REFUSED once F.2's gate exists. **State it; do not act on it.**

## Requirements *(mandatory)*

### Functional Requirements — § 2, the schema

- **FR-001**: `contracts/schemas/consent-instrument.schema.yaml` MUST gain ONE
  top-level property `custody_rederivations`: `type: array`, items
  `type: object` with `additionalProperties: false` and `required` naming
  exactly the TEN fields `at`, `commit`, `previous_locator`,
  `observed_locator`, `previous_sha256`, `observed_sha256`, `diff_class`,
  `reason`, `ruling_ref`, `recorded_by`.
- **FR-002**: field shapes MUST be `at` `type: string, format: date-time`;
  `commit` `pattern: "^[0-9a-f]{40}$"`; both locators `type: string,
  minLength: 1` with NO path grammar imposed; both digests
  `pattern: "^[0-9a-f]{64}$"`; `diff_class`
  `enum: [path_only, header_only, content]`; `reason`
  `enum: [lifecycle_header_edit, archive_move, other_ruled_edit]`;
  `ruling_ref` and `recorded_by` `type: string, minLength: 1`.
- **FR-003**: the `custody` object MUST be byte-identical after the change — its
  two properties, its `required`, its `additionalProperties: false` and its
  comment block. A diff touching `custody` fails this requirement.
- **FR-004**: `contract_schema_version` MUST move `2` → `3` with an in-file
  comment in the style of the existing `1 -> 2` note: what grew, that it is
  ADDITIVE, and that the record envelope's `schema_version` stays `const: 1`.
- **FR-005**: in-file comments MUST record (a) why the array is a SIBLING
  (ruling D9's closure argument), (b) that `ruling_ref` is a DECLARED POINTER
  the validator does not resolve, and (c) that `custody.locator` is OPAQUE and
  not a path, that resolution runs through the consuming repository's DECLARED
  custody store mapping, that the two legs are evaluated on opposite sides of
  the commit, and that an archive move is unadmittable without the pair —
  naming the measurement (every OpsxFactory locator carries an `opsx:opensoft/`
  scheme prefix; three of four targets resolve at no ref under their literal
  path).

### Functional Requirements — § 3, the canonical validator

- **FR-010**: a new check beside `check_custody` MUST verify the chain's
  INTERNAL legs: anchor in BOTH halves (`e₁.previous_sha256 == custody.sha256`
  AND `e₁.previous_locator == custody.locator`), linkage in BOTH halves,
  non-decreasing `at` in declared order, with DISTINCT finding codes per leg in
  the file's existing naming style.
- **FR-011**: the validator MUST refuse a rewritten pin — `custody.sha256`
  equal to any entry's `observed_sha256` while a later entry exists, and more
  generally any state in which the pin has been advanced to a value the chain
  records as observed.
- **FR-012**: the validator MUST NOT open a repository, shell out to `git`, or
  read a file named by a locator. **TWO assertions pin the absence** (Q7c), both
  in `tests/consent_instruments/`: a SOURCE-LEVEL ban (no `subprocess` import,
  no `git` token, no locator-named file read anywhere in the module) AND a
  RUNTIME patch of `subprocess.run` and `Path.open` exercised over **all three
  buckets** — positive, negative and withheld — since the withheld leg is the
  one most likely to reach for a repository.
- **FR-013**: the validator's report line for a chained instrument MUST state
  what it checked and what it did not, so a neutral pass is not readable as a
  currency verdict.
- **FR-014**: a `content`-class entry with sound internal legs MUST yield
  `custody-content-class-withheld` as a NAMED OUTCOME distinct from error and
  from warning — reported beside the error and warning counts, with a **NEW exit
  status meaning "needs a human decision"**. The status MUST be a **single named
  module constant** (provisionally `3`; the NUMBER is parked for Brett Heap, so
  a different ruling moves the constant and nothing else), the script's
  `Exit codes:` docstring MUST be extended **in this script only**, and the
  design note MUST record that the number is his ruling. A withheld fixture in
  the PACKAGED corpus is EXEMPT from raising it — an expected withholding is to
  the third bucket what an expected failure is to a negative.
- **FR-015**: a `path_only` entry whose `previous_sha256 != observed_sha256`
  MUST be refused.
- **FR-016**: `walk_strings` MUST be extended over **the whole entry minus the
  two digest fields** (`previous_sha256`, `observed_sha256`) — so both locators,
  `ruling_ref` and `recorded_by` are walked, and `commit` / `at` / `diff_class` /
  `reason` ride along already bounded by a pattern, a format or a closed
  enumeration. It reuses the existing `BASE64_BLOB_RX` / `data:` / PDF-magic /
  multi-line predicates and the `embedded-original-content` finding code, and is
  proved BOTH by the § 4.8b fixture in the self-test AND by a **parametrized
  pytest** reaching each of the four free strings.

### Functional Requirements — § 4, the fixtures

- **FR-020**: POSITIVE fixtures MUST cover a two-entry `header_only` chain; an
  unchanged existing example re-validated; an `archive_move` / `path_only`
  entry with differing locators and equal digests; and the two-entry
  `archive_move` → `lifecycle_header_edit` shape the real repair needs.
- **FR-021**: NEGATIVE fixtures MUST cover, one per named refusal: a broken
  digest link; a locator gap with digests linking; entries out of recorded-time
  order; a first entry whose `previous_sha256` is not the pin AND one whose
  `previous_locator` is not `custody.locator`; an unknown `diff_class` member
  AND an unknown `reason` member; an entry omitting `ruling_ref` AND one
  omitting `recorded_by`; an entry carrying an ELEVENTH property; a rewritten
  pin; a blob-shaped `ruling_ref` AND a blob-shaped `recorded_by`; and a
  `path_only` entry whose two digests differ.
- **FR-022**: a WITHHELD fixture MUST live in a THIRD directory
  `examples/consent-instrument/withheld/` and MUST be asserted as WITHHELD —
  neither positive nor negative. `self_test` MUST grow an
  `EXPECTED_WITHHELD_OUTCOMES` table that is **fail-closed both ways**, exactly
  as `EXPECTED_NEGATIVE_FINDINGS` is: a fixture on disk with no table entry and
  a table entry with no fixture are each errors. `repo_scan` (layer 2) needs no
  bucket discipline — it reports WITHHELD as it finds it.
- **FR-023**: `examples/consent-instrument/README.md` and the
  `consent-instrument` corpus comment in `contracts/manifest.yaml` MUST carry
  RE-MEASURED counts, not arithmetic on the stale figures. The README's Layout
  tree and *Schema → example map* table MUST be COMPLETE over the grown corpus,
  the table MUST gain a **third column** for the withheld bucket, and *Named
  cases from the spec* MUST gain **one bullet per refusal code (7) + one
  positive chain-shapes bullet + one withheld bullet**.
- **FR-024** *(added at clarify A1, and NOT named by any ratified task)*:
  `contracts/README.md`'s row for `scripts/validate-consent-instruments.py` +
  `examples/consent-instrument/` MUST carry the RE-MEASURED counts. It reads
  *"self-testing over 5 positives, 5 indexed negatives, and 2 purpose probes"*
  and is **already false at 6/7 before this feature adds a byte**. It is carried
  as an ADDITIONAL realization act, not as an edit to the ratified task list's
  numbering.

### Functional Requirements — § 5, the cut

- **FR-030**: §§ 2–5 MUST land in **ONE pull request** — § *Version Identity*
  requires the manifest and changelog to be committed atomically with the
  contract files. The version MUST be allocated at the final integration point
  after a re-check of availability on all three surfaces (manifest,
  `contracts/releases/`, tags), never read from this document; the orchestrator
  **re-measures at every merge-from-main and reports**, and the PR body names
  `contract-v3.5` as an explicitly PROVISIONAL measured candidate. The CLAIM on
  issue #630 row 4 is the LANE's, at the last merge-from-main before the merge.
- **FR-031**: `contracts/manifest.yaml` (`contract_bundle_version`, the
  `consent-instrument` row's `sha256` re-derived from the moved file, and an
  APPENDED `contract-v3.5` `consumption_rule` paragraph in the `contract-v1.33`
  style), `contracts/CHANGELOG.md` and
  `contracts/releases/<version>.digests.yaml` MUST move atomically in ONE
  candidate commit — **all three manifest edits included, with NO split**.
  § 2's schema commit therefore leaves the digest STALE ON PURPOSE and its
  commit message MUST say so; intermediate branch commits are ungated because CI
  runs at the PR head. `consent-instrument-class-registry`'s row MUST be
  untouched.
- **FR-032**: the CHANGELOG entry MUST list every contract added, changed or
  deprecated in the bundle — including the four `contracts/` additions and
  fourteen modifications since `contract-v3.4` that this session did not author
  — each attributed to the change that made it.
- **FR-033**: the digest inventory MUST be BUILT by
  `scripts/validate-contract-release.py build --tag <version> --output
  contracts/releases/<version>.digests.yaml`, never hand-edited.
- **FR-034**: every gate MUST run against the exact unchanged candidate:
  `release-tag-gate` (`scripts/validate-release-tag-gate.py`), the pytest set CI
  runs, `scripts/validate-manifest-digests.py`,
  `scripts/validate-contract-release.py`, and
  `scripts/validate-consent-instruments.py`.
- **FR-035**: the annotated tag MUST be left OWED. This feature does not tag.
- **FR-036** *(the landing contract, ruled at Q1 and recorded in `plan.md`)*:
  landing is a **MERGE COMMIT** — there is no linear-history rule on this
  repository. The LANE performs the final merge-from-main inside its Rule 6
  window, RE-RUNS the gates against that merge commit (policy step 4: it IS "a
  different commit"), then merges. The annotated tag targets the LANDED MERGE
  COMMIT. If `main` advanced under `contracts/` between integration and merge,
  the lane REPEATS the integration.

### Functional Requirements — bookkeeping and evidence

- **FR-040**: every box in §§ 0–5 whose act is verifiably DONE MUST be ticked
  with a note citing the record and the timestamp; boxes owned elsewhere (§§ 6,
  7 and § 5.6) MUST take dated NOT-OWED lines; note classes MUST sum to 46.
- **FR-041**: a box MUST be ticked in the same commit as its evidence, or in
  neither.
- **FR-042**: evidence MUST be written to BOTH
  `specs/033-add-consent-custody-rederivation-record/evidence/` and
  `openspec/changes/add-consent-custody-rederivation-record/evidence/realization-<date>.md`.
- **FR-043**: ratified prose — `proposal.md`, `design.md`, `.openspec.yaml` and
  the delta — MUST stay frozen. `tasks.md`, the evidence file, and ONE additive
  dated realization note after the `Lane:` line in `proposal.md` correcting any
  ratified enumeration this realization falsifies are the only permitted edits.
- **FR-044**: any ratified "stays unticked" sentence amended by a tick MUST be
  amended in the SAME commit in the `3b530009` form — block-quote the
  superseded sentence, name the un-superseded neighbour, marker
  `AMENDED <UTC date>`, tick marker `**TICKED <UTC date>`.
- **FR-045**: doc-health MUST be compared as two reports with identical
  basenames and a pinned `--as-of`.
- **FR-046** *(ruled at Q8)*: THREE `README.md` sites MUST be amended in the
  `3b530009` form — this packet's own OpenSpec Records row (*"all 46 boxes …
  stay unticked"*); `README.md:3022`'s present-tense box count, **keeping
  "the three pins are still broken"** because that half stays true (the repair
  is § 6, the consumer's); and **`README.md:2993`**, the
  `govern-archived-record-edits` row's *"the consent family's is PROPOSED only
  (`contract_schema_version: 2`, no `custody_rederivations` property,
  `contract-v3.4`, 46/46 boxes unticked)"* — false on all four counts after this
  lands and the load-bearing premise of that rule's TRANSITION CLAUSE. The
  past-tense *"left its 46"* and the dated *"measured 2026-09-09 … at `main`
  `6cc06288`"* are LEFT as true-when-written. **The LANE posts the substrate
  note for the two sibling-row sentences BEFORE they are written**; this
  packet's own row rides its standing row-3 claim (`5571680388`).
- **FR-047** *(ruled at clarify A2 — state it, do not act on it)*: the
  realization evidence and the neighbourhood of § 7 in the packet's `tasks.md`
  MUST carry a DATED note recording that landing this realization **DECLARES the
  consent family's re-derivation rule**, so under `govern-archived-record-edits`'
  transition clause an edit of a consent pinned target converts from **REPORTED**
  to **REFUSED** for that family **once F.2's gate exists**. Nothing in this
  feature builds, schedules or ticks for it.

### Key Entities

- **`custody_rederivations` entry** — a closed ten-field record of one
  authorized divergence at one commit, carrying a locator pair and a digest
  pair evaluated on opposite sides of that commit.
- **The chain** — the declared-order sequence of entries, anchored to the pin
  AND the pin's locator, with no gap in either half.
- **WITHHELD** — a third outcome beside pass and refusal, meaning the record is
  correct and the INSTRUMENT needs attention.
- **The candidate commit** — the one commit carrying every release surface,
  against which every gate runs unchanged.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `scripts/validate-consent-instruments.py --strict` reports 0
  errors and 0 warnings over the grown corpus, and its self-test note reports
  THREE bucket counts.
- **SC-002**: the packet's `tasks.md` carries 46 notes summing exactly to
  **35 TICKED + 3 NOT-OWED-HERE (§ 5.1, § 5.5, § 5.6) + 8 NOT-OWED (§§ 6–7)**,
  with no box ticked whose act was not performed.
- **SC-003**: `git diff` of the schema shows ZERO lines inside the `custody`
  object.
- **SC-004**: `scripts/validate-manifest-digests.py` verifies every digest,
  including the re-derived `consent-instrument` row.
- **SC-005**: `scripts/validate-contract-release.py verify-commit --commit
  <candidate>` passes on the exact candidate.
- **SC-006**: the pinned CLI reports `--change … --strict` 1 passed / 0 failed
  and `--all --strict` with zero UNDISPOSITIONED failures.
- **SC-007**: `python3 -m pytest tests/ -q -m "not postgres"` is green,
  including the new `tests/consent_instruments/` package — the source-level
  no-git ban, the runtime patch over all three buckets, and the parametrized
  blob-walk test.
- **SC-010**: `scripts/validate-consent-instruments.py` over an instrument that
  WITHHOLDS exits in the new named status class, and the packaged corpus exits
  0 — the two are distinguishable from the command line.
- **SC-008**: doc-health's finding set on this branch is diff-identical to
  `main`'s at every severity, both reports taken with the same `--as-of`.
- **SC-009**: `scripts/validate-sequenced-after.py .` and `--ledger-diff` are
  consistent, and `scripts/validate-scope-globs.py` passes.

## Assumptions

- The reused architect rulings Q1, Q4, Q5, Q9 and Q10 from the F.3 realizations
  apply here unchanged; only what they do not settle is asked.
- `contract-v3.5` is free at the integration point unless a sibling lane takes
  it first; the allocation step re-measures rather than trusting this document.
- No consumer repository is touched by this feature.

## Out of scope

- **§ 5.1's CLAIM** of the version number on openxFactory issue #630 row 4 —
  this feature MEASURES the number and reports it at every merge-from-main; the
  LANE posts the claim at the last one before the merge.
- **§ 5.5** — landing the exact reviewed commit, and the post-merge gate re-run
  the merge commit forces. The LANE ticks it in a follow-up bookkeeping commit
  while the packet is still live.
- **§ 5.6** — the annotated tag and its independent verification are
  `[OPERATOR]` acts.
- **§ 6** — every `[OpsxFactory]` consumer act: the `stack.yaml` re-pin in
  lockstep with the worker-enrollment broker, the three non-uniform
  prescriptions, the declared custody store mapping, the operated
  custody-digest check, and the F.1 discharge in the owed-findings register.
- **§ 7** — F.2's gate, F.3's settlement, and any other content-address
  family's re-derivation record.
- Opening the pull request, posting any GitHub comment (the row-3/row-4
  substrate notes included), merging, tagging, or archiving the OpenSpec change.
- **Arming A2's cross-repo consequence.** Landing DECLARES the consent family's
  rule, which converts `govern-archived-record-edits`' posture for that family
  from REPORTED to REFUSED once F.2's gate exists. This feature RECORDS that and
  builds nothing for it.
