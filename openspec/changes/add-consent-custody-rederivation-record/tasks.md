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
  and it should be true. Re-run
  `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<real PR>'`
  once the number is known, and read the diff: exactly one row must move.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **[OPERATOR] Ratify or veto.** The F.1 ruling of 2026-09-07 ordered
  this authoring and chose the repair FORM; it approved no field name, no enum
  member, no closure posture and no chain rule. Ratification is a separate act.
  Record it at `review/ratification-<date>.md` in the neighbours' form, flip
  `Status: draft` → `Status: ratified` on `proposal.md`, `design.md` and this
  file, and add the `Ratified:` line plus the README row's status flip.
- [ ] 1.2 **[OPERATOR] The eight veto points, ruled individually or as a
  block:** C-1 sibling not member; C-2 the name `custody_rederivations`; C-3
  eight fields all required; C-4 `diff_class` members; C-5 `reason` members;
  C-6 the chain rule and the refusal posture; C-7 the validator split; C-8
  additive bump to `contract_schema_version: 3`. A veto on C-1, C-6 or C-7
  changes the delta; a veto on C-2, C-4 or C-5 changes only the schema text.

## 2. The schema edit

- [ ] 2.1 `contracts/schemas/consent-instrument.schema.yaml`: add the top-level
  `custody_rederivations` property — `type: array`, items `type: object` with
  `additionalProperties: false` and `required: [at, commit, previous_sha256,
  observed_sha256, diff_class, reason, ruling_ref, recorded_by]`. Shapes: `at`
  `type: string, format: date-time`; `commit` `pattern: "^[0-9a-f]{40}$"`;
  both digests `pattern: "^[0-9a-f]{64}$"`; `diff_class` `enum: [header_only,
  content]`; `reason` `enum: [lifecycle_header_edit, archive_move,
  other_ruled_edit]`; `ruling_ref` and `recorded_by` `type: string, minLength: 1`.
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

## 3. The canonical validator — internal legs only

- [ ] 3.1 `scripts/validate-consent-instruments.py`: a new check beside
  `check_custody` for the chain's INTERNAL legs — anchor (`e₁.previous_sha256 ==
  custody.sha256`), linkage (`eᵢ.previous_sha256 == eᵢ₋₁.observed_sha256`),
  non-decreasing `at` in declared order, and closed enums/shape via the schema
  layer. Distinct finding codes per leg, in the file's existing naming style
  (candidates: `custody-chain-unanchored`, `custody-chain-broken-link`,
  `custody-chain-out-of-order`).
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

## 4. Fixtures — positive and negative, one per named refusal

- [ ] 4.1 POSITIVE: `examples/consent-instrument/` gains an instrument carrying
  a two-entry unbroken chain (`header_only` / `lifecycle_header_edit`), admitted
  by the internal legs.
- [ ] 4.2 POSITIVE: an existing example is left UNCHANGED and re-validated, to
  prove the growth is additive for an instrument that declares no array.
- [ ] 4.3 NEGATIVE `examples/consent-instrument/negative/`: a broken link
  (`eᵢ.previous_sha256 != eᵢ₋₁.observed_sha256`).
- [ ] 4.4 NEGATIVE: a first entry whose `previous_sha256` is not the pin.
- [ ] 4.5 NEGATIVE: an unknown `diff_class` member, and an unknown `reason`
  member (schema-layer refusals).
- [ ] 4.6 NEGATIVE: an entry omitting `ruling_ref`, and one omitting
  `recorded_by`.
- [ ] 4.7 NEGATIVE: an entry carrying a ninth property (entry closure).
- [ ] 4.8 NEGATIVE: a rewritten pin — `custody.sha256` advanced to an observed
  digest while the chain still claims the original anchor.
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
- [ ] 6.2 `[OpsxFactory]` Write, per BROKEN instrument, one `amendments` entry
  (the human half the F.1 ruling asks for) and one `custody_rederivations` entry
  (the machine half): `commit: 57fd9fd2…`, `diff_class: header_only`,
  `reason: lifecycle_header_edit`, `previous_sha256` = the pin,
  `observed_sha256` = the target at that commit, `ruling_ref` citing
  `docs/packet-lifecycle-headers.md` § *Editing an archived packet* and the F.1
  ruling comment.
- [ ] 6.3 `[OpsxFactory]` Leave `opsx-farheap-node-inventory-reader-consent.yaml`
  ALONE. It is not broken; an entry on a current pin would be a false record of
  an event that did not occur.
- [ ] 6.4 `[OpsxFactory]` Discharge F.1 in the owed-findings register — which
  archives 2026-09-07 to
  `openspec/changes/archive/2026-09-07-add-pre-archive-citation-gate/supporting-docs/owed-findings.md`
  — by citing the change that performed the repair.

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
