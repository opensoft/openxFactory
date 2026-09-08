# Tasks: add-consent-custody-rederivation-record

Status: draft
Lane: opsXfactory-1

**NOTHING BELOW IS DONE. EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE
PACKET RATHER THAN AN OVERSIGHT.** This is a PROPOSAL. No schema byte moves, no
contract version is cut, no digest inventory is written, no validator leg is
added, no example is authored, no consumer pin advances, and no instrument takes
an entry.

**Tags.** Untagged = openxFactory. `[OpsxFactory]` = `opensoft/OpsxFactory` and
its own OpenSpec instance — listed as the CONSUMER'S owed acts, outside this
change's archive gate. `[OPERATOR]` = only Brett Heap can perform it: a
ratification, a human-only surface write, a tag.

## 0. Bookkeeping this branch already carries, and the one stamp that is provisional

- [ ] 0.1 **RE-STAMP THE SWEEP LEDGER ROW WITH THE REAL PULL-REQUEST NUMBER.**
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

- [ ] 1.1 **[OPERATOR] Ratify or veto.** The F.1 ruling of 2026-09-07 ordered
  this authoring and chose the repair FORM; it approved no field name, no enum
  member, no closure posture and no chain rule. Ratification is a separate act.
  Record it at `review/ratification-<date>.md` in the neighbours' form, flip
  `Status: draft` → `Status: ratified` on `proposal.md`, `design.md` and this
  file, and add the `Ratified:` line plus the README row's status flip.
- [ ] 1.2 **[OPERATOR] The eleven veto points, ruled individually or as a
  block:** C-1 sibling not member; C-2 the name `custody_rederivations`; C-3
  ten fields all required; C-4 `diff_class` members; C-5 `reason` members;
  C-6 the chain rule, the path pair and the ancestry leg; C-6a declared locator
  resolution plus the entry's locator pair; C-7 the validator split and the
  obligation to operate a check; C-8 additive bump to
  `contract_schema_version: 3`; C-9 a `content` class WITHHOLDS the verdict;
  C-10 a re-derivation is not an amendment. A veto on C-1, C-6, C-6a or C-7
  changes the delta; a veto on C-2, C-4 or C-5 changes only the schema text.
- [ ] 1.3 **[OPERATOR] C-10 SUPERSEDES ONE CLAUSE OF YOUR OWN F.1 RULING and
  needs your word specifically.** The ruling says the three instruments take
  *"their `amendments` entries plus the structured block"*. C-10 writes the
  structured block and NO `amendments` entry, because an amendment is a status
  TRANSITION (promoted requirement, ruling D7) and all four instruments are
  `status: executed` — so the prose half would move three executed consent
  instruments to `amended` to record that a repository moved a file underneath
  an unchanged pin. Keeping the `amendments` entry is yours to choose; the cost
  is that transition.

## 2. The schema edit

- [ ] 2.1 `contracts/schemas/consent-instrument.schema.yaml`: add the top-level
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
- [ ] 2.2 `custody` IS NOT EDITED. Confirm by diff that its two properties, its
  `required`, its `additionalProperties: false` and its comment block are
  byte-identical after the change. A diff touching `custody` fails this task.
- [ ] 2.3 `contract_schema_version: 2` → `3`, with the in-file comment written in
  the style of the existing `1 -> 2` note: what grew, that it is ADDITIVE, and
  that the RECORD envelope's `schema_version` stays `const: 1` because moving it
  would invalidate every instrument in the estate.
- [ ] 2.4 An in-file comment on the new property recording WHY it is a sibling
  (ruling D9's closure argument, design C-1) and that `ruling_ref` is a DECLARED
  POINTER the validator does not resolve — the `dependent_refs.ref` posture.
- [ ] 2.5 An in-file comment on the locator pair recording that `custody.locator`
  is OPAQUE and is NOT a path (C-6a): resolution runs through the consuming
  repository's DECLARED custody store mapping, the two legs are evaluated on
  opposite sides of the commit, and an archive move is unadmittable without the
  pair. Name the measurement: every OpsxFactory locator carries an
  `opsx:opensoft/` scheme prefix and three of four targets resolve at no ref
  under their literal path.

## 3. The canonical validator — internal legs only

- [ ] 3.1 `scripts/validate-consent-instruments.py`: a new check beside
  `check_custody` for the chain's INTERNAL legs — anchor in BOTH halves
  (`e₁.previous_sha256 == custody.sha256` AND `e₁.previous_locator ==
  custody.locator`), linkage in BOTH halves (`eᵢ.previous_sha256 ==
  eᵢ₋₁.observed_sha256` AND `eᵢ.previous_locator == eᵢ₋₁.observed_locator`),
  non-decreasing `at` in declared order, and closed enums/shape via the schema
  layer. Distinct finding codes per leg, in the file's existing naming style
  (candidates: `custody-chain-unanchored`, `custody-chain-broken-link`,
  `custody-chain-locator-gap`, `custody-chain-out-of-order`).
- [ ] 3.2 The rewritten-pin leg: refuse an instrument whose `custody.sha256`
  equals any entry's `observed_sha256` while a LATER entry exists, and more
  generally any state in which the pin has been advanced to a value the chain
  itself records as observed. Finding code candidate: `custody-pin-rewritten`.
- [ ] 3.3 **NO GIT RE-DERIVATION IS ADDED** (design C-7). Assert the absence:
  the validator opens no repository, shells out to no `git`, and reads no file
  named by `custody.locator`. A test pins that absence so a helpful later edit
  fails on the developer's machine first.
- [ ] 3.4 The neutral pass MUST NOT report itself as a currency verdict. The
  validator's report line for a chained instrument says what it checked and
  what it did not, per the promoted scenario *The neutral pass is not a currency
  claim*.
- [ ] 3.4b **MINT THE WITHHELD OUTCOME — it is mandated by the requirement and
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
- [ ] 3.4c A `path_only` entry whose `previous_sha256 != observed_sha256` is
  refused (finding code candidate `custody-path-class-digests-differ`). This leg
  is neutral because both digests are fields of the record; CONFIRMING a class
  against the measured diff needs the repository and belongs to the consumer's
  gate.
- [ ] 3.5 **EXTEND `walk_strings` OVER THE NEW FIELDS** (design C-1 as
  corrected). `check_custody`'s blob-shape walk is the family's only
  "wherever it hides" guard, and siting the array outside `custody` leaves
  `custody_rederivations[].ruling_ref` and `.recorded_by` — the two unbounded
  free strings in the entry — outside it. Extend the walk over both, reusing the
  existing `BASE64_BLOB_RX` / `data:` / PDF-magic / multi-line predicates and
  the `embedded-original-content` finding code. The locators are opaque
  POINTERS and are walked on the same footing as `custody.locator` is today.

## 4. Fixtures — positive and negative, one per named refusal

- [ ] 4.1 POSITIVE: `examples/consent-instrument/` gains an instrument carrying
  a two-entry unbroken chain (`header_only` / `lifecycle_header_edit`), admitted
  by the internal legs.
- [ ] 4.2 POSITIVE: an existing example is left UNCHANGED and re-validated, to
  prove the growth is additive for an instrument that declares no array.
- [ ] 4.1b POSITIVE: an instrument carrying an `archive_move` /
  `diff_class: path_only` entry whose locator pair DIFFERS and whose digests are
  EQUAL on both sides — the case a single-locator rule can never admit (design
  C-6a, `proposal.md` Example B).
- [ ] 4.1c POSITIVE: the TWO-ENTRY chain shape the real repair needs — e1
  `archive_move`/`path_only`, e2 `lifecycle_header_edit`/`header_only` — modelled
  on prescription I in `design.md` § *The consumer handoff*. No fixture in the
  corpus exercises a multi-entry chain today.
- [ ] 4.3 NEGATIVE `examples/consent-instrument/negative/`: a broken link
  (`eᵢ.previous_sha256 != eᵢ₋₁.observed_sha256`).
- [ ] 4.3b NEGATIVE: a locator gap (`eᵢ.previous_locator !=
  eᵢ₋₁.observed_locator`) with the digests linking correctly — the half of the
  chain an earlier draft could not express.
- [ ] 4.3c NEGATIVE: entries out of recorded-time order
  (`custody-chain-out-of-order`), so § 4's "one per named refusal" is true of
  that refusal too.
- [ ] 4.4 NEGATIVE: a first entry whose `previous_sha256` is not the pin, and
  one whose `previous_locator` is not `custody.locator`.
- [ ] 4.5 NEGATIVE: an unknown `diff_class` member, and an unknown `reason`
  member (schema-layer refusals).
- [ ] 4.6 NEGATIVE: an entry omitting `ruling_ref`, and one omitting
  `recorded_by`.
- [ ] 4.7 NEGATIVE: an entry carrying an ELEVENTH property (entry closure —
  the entry has TEN required fields since C-6a, so a "ninth" would not test the
  closure at all).
- [ ] 4.8 NEGATIVE: a rewritten pin — `custody.sha256` advanced to an observed
  digest while the chain still claims the original anchor.
- [ ] 4.8b NEGATIVE: a blob-shaped `ruling_ref` and a blob-shaped `recorded_by`
  (base64 run, `data:` URI, PDF magic or a multi-line body), each refused as
  `embedded-original-content` — the fixture that proves task 3.5 landed.
- [ ] 4.8c **WITHHELD (neither positive nor negative — the third outcome):** an
  instrument whose last entry declares `diff_class: content` and whose internal
  legs are ALL SOUND, asserted to yield WITHHELD — **not a pass and not an
  error**. This is the fixture that proves task 3.4b landed, and the self-test
  harness needs a third expectation bucket to hold it, since today it can only
  say "valid" or "invalid for its intended finding".
- [ ] 4.8d NEGATIVE: a `path_only` entry whose two digests differ.
- [ ] 4.9 `examples/consent-instrument/README.md` updated with the new corpus
  counts, and the corpus count in `contracts/manifest.yaml`'s
  `consent-instrument` comment (*"5 valid + 5 invalid + purpose probes"*)
  re-measured rather than adjusted by arithmetic.

## 5. The contract cut

- [ ] 5.1 **[OPERATOR-adjacent] CLAIM THE VERSION NUMBER on openxFactory issue
  #630, row 4 (Contract cuts), AT CUT TIME AND NOT BEFORE.** Row 4's rule is
  *"Claim the **version number**, not the files"*, and `docs/contract-versioning-policy.md`
  § *Bundle Realization Order* step 1 allocates it at the final integration
  point. Measured at authoring, the next additive minor is `contract-v3.5`
  (`contracts/manifest.yaml:3` declares `contract-v3.4`; `contracts/releases/`
  holds `contract-v3.4.digests.yaml` as its highest) — **a measurement, not a
  reservation**. Re-measure at the cut; a sibling cut may have taken it.
- [ ] 5.2 Realization order steps 1–2: fetch, integrate onto the final
  integration point, re-check availability, allocate, then move every release
  surface atomically in ONE candidate commit — `contracts/manifest.yaml`
  (`contract_bundle_version`, the `consent-instrument` row's `sha256` — today
  `13b0fe46…` — and its `consumption_rule`), `contracts/CHANGELOG.md`, and
  `contracts/releases/<version>.digests.yaml`.
- [ ] 5.3 The CHANGELOG entry names what changed in the bundle, not what this
  session intended: § *Version Identity* requires one entry per release listing
  every contract added, changed or deprecated, and a bundle is a commit's whole
  tree.
- [ ] 5.4 Step 3: run every gate against that exact unchanged candidate —
  `release-tag-gate` (which evaluates any PR touching `contracts/manifest.yaml`
  or `contracts/releases/`), `pytest-suite`, `scripts/validate-manifest-digests.py`,
  `scripts/validate-contract-release.py`, `scripts/validate-consent-instruments.py`.
- [ ] 5.5 Step 4: land the exact reviewed commit. If promotion creates a
  different commit, that commit becomes the candidate and every gate reruns.
- [ ] 5.6 **[OPERATOR]** Step 5: publish the annotated tag at the exact
  published commit and verify it from an independently refreshed checkout. The
  gate records the tag as OWED and does not require it before step 4; the
  obligation is on whoever lands step 4.

## 6. The consumer handoff — [OpsxFactory]'s OWED ACT, not this change's

**Listed for completeness and explicitly OUTSIDE this change's archive gate.**
This change archives on ITS realization evidence (§§ 2–5 merged and green); the
items below are OpsxFactory's, in OpsxFactory's own change, under OpsxFactory's
own gates.

- [ ] 6.1 `[OpsxFactory]` Advance `stack.yaml` `contract_ref` (today
  `724a2a4f…`) to the cut bundle's commit **in lockstep with the
  worker-enrollment-broker's runtime-shape validation** — the pin and the
  broker's declared shape move in one act, or the `pin_gap_misdeclared` guard
  fails the advance closed.
- [ ] 6.2 `[OpsxFactory]` Write the THREE PRESCRIPTIONS set out verbatim in
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
- [ ] 6.2b `[OpsxFactory]` **DECLARE THE CUSTODY STORE MAPPING** that resolves
  `opsx:<tenant>/<repo-relative path>`, which the ADDED requirement obliges of
  any repository holding instruments, and **operate the custody-digest check**
  that performs the re-derivation legs (the C-7 obligation; F.2's gate is where
  it lands).
- [ ] 6.3 `[OpsxFactory]` Write NO entry for `57fd9fd2` on
  `opsx-farheap-node-inventory-reader-consent.yaml`: its content pin is not
  broken. Its LOCATOR did move when `add-managed-service-mapping` archived
  (2026-08-26), so it is a candidate for a separate `archive_move` entry with a
  differing locator pair and an unchanged digest on both sides — the first real
  exercise of the path pair, and the consumer's call.
- [ ] 6.4 `[OpsxFactory]` Discharge F.1 in the owed-findings register — **(archive
  in flight; the live path until then is
  `openspec/changes/add-pre-archive-citation-gate/supporting-docs/owed-findings.md`)**
  — which archives 2026-09-07 to
  `openspec/changes/archive/2026-09-07-add-pre-archive-citation-gate/supporting-docs/owed-findings.md`,
  by citing the change that performed the repair.

## 7. Named as owed elsewhere, and deliberately not taken here

- [ ] 7.1 **F.2's custody-digest gate is NOT built here.** Ruled scope: *"every
  in-repo sha256 pointer to an in-repo target"*. Owner: OpsxFactory, its own
  change. This packet supplies only the consent-custody family's re-derivation
  rule, which that gate consumes.
- [ ] 7.2 **F.3 is NOT settled here.** The *"both at once"* ruling asks for an
  OpsxFactory change AND an openxFactory change amending the promoted
  `document-lifecycle` capability. This packet is neither and touches no
  `document-lifecycle` requirement.
- [ ] 7.3 **No other content-address family is given a re-derivation record.**
  Whether plan-acceptance desired-state refs, evidence digests, fence baselines
  or contract pins want the same shape is a question F.2's inventory answers,
  not this one.
