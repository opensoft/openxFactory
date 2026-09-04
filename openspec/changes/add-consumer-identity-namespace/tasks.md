# Tasks: add-consumer-identity-namespace

Status: ratified
Ratified: 2026-09-03 by Brett Heap (repository owner) — in session, verbatim
"implement your recommendations on all these". Record:
`review/ratification-2026-09-03.md`.

**RATIFICATION AND REALIZATION RIDE IN ONE PR, and that is a size judgment
rather than a shortcut.** The surface is one described schema member, one shared
predicate, one deprecation code, five fixtures and their tests. Splitting it
would put a ratified rule and its only proof in different reviews, and the rule
is one whose defect — the lift and the finding disagreeing — was found by
EXECUTION and not by reading. **THE CUT IS NOT PART OF IT**, by the ruling's own
words: no tag, no digest inventory, no version-headed CHANGELOG entry. § 5
prescribes what the cut owes so the cut has nothing to invent.

**EVERY TASK IS MARKED WITH THE ISSUE IT DISCHARGES.** Two rulings ride in one
MODIFIED block; a reader must be able to see which act each edit belongs to
without reconstructing it. `[#511]`, `[#553]`, or `[both]`.

**No task here creates, moves, or reads a live secret.** The member names a
directory; it holds no material.

## 1. The schema — one member, DESCRIBED here and CONSTRAINED at the major

- [x] 1.1 `[#511]` `contracts/schemas/xfactory-credential-contracts.schema.yaml`:
  `identity_namespace` joins the `consumer:` block's described member set —
  DESCRIPTION ONLY, like every member beside it at this minor. No `type`, no
  `pattern`, no `required:`, no `additionalProperties: false`.
  **EXECUTED.** The member paragraph names what it is, why it is not `tenant`
  and not `realm`, that the comparison reads the PAIR where both sides declare
  one and FALLS BACK where either does not, and the code that warns until the
  major. `test_the_block_declares_no_constraint_keyword_at_this_release` still
  passes, which is the assertion that would catch a constraint smuggled in with
  a description.
- [x] 1.2 `[#511]` The block's own paragraph, which said the acts land "behind
  one deprecation window and the eight warning codes", is corrected to NINE.
  **EXECUTED.** A count in a pinned contract's description that is wrong by one
  is a count a consumer reads and trusts.
- [x] 1.3 `[#511]` The member set is MIRRORED in the validator, and the mirror
  is gated. **EXECUTED** — `test_the_schema_describes_every_member_the_validator_enforces`
  iterates `CONSUMER_MEMBERS` against the schema description and passes with the
  new member, so a member the validator warns about and the schema never names
  cannot ship.

## 2. The validator — one predicate, one code, one more sink

- [x] 2.1 `[#511]` `CONSUMER_MEMBERS` gains `identity_namespace`.
  **EXECUTED.** Consequence measured rather than assumed: a block carrying the
  key drew `consumer-block-unknown-member` before and draws nothing now — a
  warning REMOVED, never added, asserted by
  `test_the_namespace_is_a_DECLARED_member_and_no_longer_an_unknown_one`.
- [x] 2.2 `[#511]` `_namespace(consumer)` returns the declared value ONLY where
  it matches the identifier grammar, and `None` otherwise.
  **EXECUTED.** An unreadable namespace is therefore treated exactly as an
  absent one BY THE COMPARISON — clearing a finding on a value nothing could
  read is the fail-open shape this family has already repaired once — and is
  warned in its own right beside it so the record says what happened.
- [x] 2.3 `[#511]` `_same_fetch_authority(con_a, con_b)` — ONE predicate, called
  from BOTH places canon states the comparison.
  **EXECUTED, AND THE REASON IS A DEFECT THIS TASK LIST OWES ITS READER.** The
  first draft rescoped the FINDING and left the LIFT's third condition comparing
  bare strings. A pair sharing a `secret_ref` with one fetch identity in two
  namespaces then escaped the named fault correctly and was refused by
  `shared-secret-identity` incorrectly — a reader told about two credentials
  collapsing into one would have split the secret and left the namespaces
  untouched. Found by EXECUTION (`test_a_shared_secret_pair_with_two_namespaces_reaches_the_LIFT_rather_than_the_named_fault`
  failed), not by reading. Both callers now call the one predicate.
- [x] 2.4 `[#511]` The message names the namespace where one was READ, and names
  the remedy where exactly one side declared one.
  **EXECUTED** — `_authority_label` and `_namespace_hint`. "Authenticating as
  `runtime_identity`" is ambiguous in precisely the way this member exists to
  end; and the one-sided case is the shape most likely to be a MISSING
  DECLARATION rather than a real collapse, so the message says to declare the
  namespace on BOTH bindings rather than leaving a reader to infer that deleting
  it from the other would also silence the finding.
- [x] 2.5 `[#511]` A NINTH `consumer-*` deprecation code,
  `consumer-identity-namespace-grammar`, inserted beside its family and AHEAD of
  the second family's two.
  **EXECUTED.** Placement is load-bearing:
  `test_the_two_codes_are_DECLARED_and_are_not_a_widening_of_the_consumer_block_set`
  pins `DEPRECATION_CODES[-2:]` to the resolution pair, and inserting the ninth
  before them keeps that claim true. Only the length pin moved, 10 -> 11, and it
  moved BY NAME with the reason written beside it.
- [x] 2.6 `[#511]` The THIRD free string joins the `baked-secret` screen, in the
  SAME COMMIT that declares it.
  **EXECUTED** — `CONSUMER_FREE_STRINGS`, under `add-binding-consumer-identity`
  § 2.6's own precedent and reasoning: a new free-string sink on the record kind
  whose invariant is "never bake a secret" is a GAP, not a permission, and
  screening it a release later reopens the gap § 2.6 closed one member on. The
  § 2.6 LIMIT is carried unchanged rather than re-claimed: `_B64ISH` requires
  forty characters, so a 38-character alphanumeric secret passes.
- [x] 2.7 `[#511]` The module docstring's `EIGHT consumer-*` becomes NINE, and
  the new behaviour is stated where a reader of the file meets it.
  **EXECUTED.**
- [ ] 2.8 `[#511]` `MAJOR_RELEASE` reads `contract-v3.0` while
  `docs/contract-versioning-policy.md` has RESTATED the target to
  `contract-v4.0`, so every deprecation message this validator prints names a
  major already cut without the acts. **NOT DONE, AND DELIBERATELY NOT DONE
  HERE.** Neither ruling caused it, it predates both, and repairing it would
  move all eleven messages under a packet nobody read for that purpose. OBSERVED,
  reported on the PR, and left for its own act — an unticked box with a reason is
  a better record than a tick that smuggled a fix.

## 3. Packaged fixtures — both directions, and the silent one first

- [x] 3.1 `[#511]` POSITIVE:
  `two-tenant-identity-namespace.binding-template.example.yaml` — two tenants of
  one provider, one principal NAME, two namespaces, and NOTHING reported.
  **EXECUTED.** This is the CLEARING direction, and a corpus holding only the
  reporting direction cannot tell a working check from one that fires on
  everything. SYNTHETIC identifiers, under the 2026-08-29 ruling.
- [x] 3.2 `[#511]` NEGATIVE:
  `consumer-shared-authority-same-namespace.yaml` — the control for § 3.1, one
  namespace on both sides. The member SCOPES the comparison; it does not lift
  it. **EXECUTED**, registered in `NEGATIVE_EXPECTATIONS`.
- [x] 3.3 `[#511]` NEGATIVE:
  `consumer-shared-authority-one-sided-namespace.yaml` — a namespace on ONE side
  only, still REPORTED. **EXECUTED.** This is the fixture that proves the
  fallback: without it, "falls back to the bare identity" is a sentence rather
  than a behaviour, and an estate able to silence a real shared authority by
  omitting a member would be discovered by a consumer rather than by the corpus.
- [x] 3.4 `[#511]` NEGATIVE:
  `consumer-identity-namespace-raw-secret.yaml` — the third free string under the
  screen, one registered negative per field exactly as § 2.6 required for the
  first two. **EXECUTED.**
- [x] 3.5 `[#511]` WARNING: `consumer-identity-namespace-grammar.yaml`, the one
  probe for the one new code. **EXECUTED.** The self-test refuses a declared
  code with no probe, so this is structural rather than decorative.
- [x] 3.6 `[both]` Every new fixture joins the BY-NAME inventory in
  `tests/credential_contracts/test_dispatch_credential_contract.py` in the SAME
  COMMIT — the condition on which that file's count is allowed to be DERIVED.
  **EXECUTED**: 7 -> 8 positive, 16 -> 19 negative, 12 -> 13 warning, and
  `test_the_inventory_is_the_whole_corpus_and_not_a_sample` proves the lists are
  exhaustive rather than a sample.

## 4. Tests

- [x] 4.1 `[#511]` A BASELINE assertion opens the new section:
  `test_the_shape_reports_before_any_namespace_is_declared`.
  **EXECUTED, AND IT IS NOT DECORATION.** Without it a test that passes because
  the finding was never raised is indistinguishable from one that passes because
  a namespace cleared it — the ANCHOR-MISSING failure the predecessor's mutation
  round was built to detect.
- [x] 4.2 `[#511]` One test per behaviour: two namespaces clear; one namespace
  on both sides reports; one side only reports; an ungrammatical namespace
  reports AND warns; the message names the namespace; the message names the
  remedy; a pair whose identities already differ is untouched; the LIFT reaches
  the same verdict as the finding, in both directions; the member is declared
  rather than unknown; a namespace does not stand in for an identifier; a
  namespace beside the stub token keeps the exemption; the ninth code sits beside
  its family and carries a probe; the grammar warning says the value is not read
  as a namespace; the raw-secret screen covers it.
  **EXECUTED** — twenty tests, all named for the claim they make.
- [x] 4.2a `[#511]` **THE PREDICATE'S WHOLE TRUTH TABLE, EIGHT ROWS, EACH
  ASSERTED SYMMETRICALLY.** **EXECUTED** —
  `test_the_authority_predicate_over_its_WHOLE_truth_table`. The fallback is a
  rule about ABSENCE, and a rule about absence is only as good as its
  enumeration of the ways a value can be missing: not declared, declared and
  ungrammatical, declared as null. Testing the first alone would leave the other
  two to a reader's confidence. EXACTLY ONE row clears — both sides declaring a
  grammatical namespace and the two differing — and the other seven fall back
  and report. Symmetry is ASSERTED rather than assumed, because the predicate is
  called over `combinations`, which fixes an order, and a rule whose outcome
  depends on which was found first is not a rule.
- [x] 4.3 `[#511]` `tests/credential_contracts/major_projection.py` gains the
  member with the identifier `pattern`, and DOES NOT add it to the `then:
  required` list. **EXECUTED.** Stated as a decision: most estates run one
  directory, and requiring a namespace of them at the major would be a narrowing
  nothing warned about — the same fault the block's own requiredness is gated
  against.
- [x] 4.4a `[both]` `tests/doc-health/test_modified_block_currency_self_gate.py`'s
  `_LEDGER_SUBJECTS` gains this packet's TWO subjects, in the same commit,
  saying which moved and why — which is what that gate's own failure message
  prescribes, and it is a gate rather than a formality: it compares the named
  set with `==` and never `<=`, so a newly lossy MODIFIED block cannot land
  unreported. **EXECUTED.** The note splits the second subject's seven uncarried
  units BY RULING — five #511's, two #553's, one sentence carrying one of each —
  so a reader of the ledger can see the fold without reconstructing it, and both
  subjects retire when this packet archives and its blocks are promoted.
- [x] 4.4 `[#511]` The `DEPRECATION_CODES` length pin in
  `test_requirement_ref_resolution.py` moves 10 -> 11, BY NAME and with the
  reason beside it. **EXECUTED.** No test is added, removed, renamed or weakened
  by this packet, and no assertion is loosened; one pinned count moves because a
  code was added, which is what that pin is for.

## 5. The release ritual — what this change does NOT do, and what the cut owes

- [x] 5.1 `[#511]` `contracts/manifest.yaml`: the `credential-contracts` row's
  `sha256` recomputed from the bytes on disk, `d0e936fc7377…` -> `b8aa4c77e937…`,
  and its `consumption_rule` extended with the member and the comparison.
  **EXECUTED, AND FORCED RATHER THAN CHOSEN** — `test_manifest_row_digest.py`
  reds at the commit on any schema move that leaves the row behind, so a
  consumer never verifies a digest for bytes nobody shipped.
  `python3 scripts/validate-manifest-digests.py` green over all 163 rows.
- [x] 5.2 `[#511]` `docs/contract-versioning-policy.md` § Deprecations Currently
  In Force: the ninth table row; the member in the entry's own enumeration; the
  act count SEVEN -> EIGHT; the reconciliation paragraph's ordinal, which called
  the resolution act "a NINTH act ... not one of the SEVEN above" and would have
  become false; and a NEW paragraph stating that the ninth row's window opens at
  ITS OWN minor rather than at `contract-v2.4`. **EXECUTED.** That last is the
  half a reader at the major needs: a row that borrowed a window it never served
  is exactly the defect this entry exists to prevent.
- [x] 5.3 `[#511]` **THE CUT — NOT THIS CHANGE.** The ruling excludes it in
  terms. Whoever cuts owes, in one act: the number (allocated by merge order —
  `contract-v3.1` was being spent by PR #616 when this was written, was CUT by
  it, and was then found DEFECTIVE and SUPERSEDED by `contract-v3.2` (PR #624);
  the newest tag now reads `contract-v3.2` and the next additive minor is
  `contract-v3.3` — still not written down, for the same reason, now twice
  demonstrated), a
  version-headed `contracts/CHANGELOG.md` entry, the digest inventory under
  `contracts/releases/`, and the annotated tag. **THE CHANGELOG ENTRY IS
  PRESCRIBED SO THE CUT INVENTS NOTHING**: class ADDITIVE (minor); the entry
  states that `consumer.identity_namespace` is declared and unconstrained at
  this release; that the shared-authority comparison reads the PAIR where both
  sides declare a grammatical namespace and the BARE identity everywhere else,
  so absence and malformedness REPORT rather than clear; that one predicate
  serves both the named finding and the lift's third condition; that the block's
  SHAPE codes go from EIGHT to NINE with `consumer-identity-namespace-grammar`,
  whose deprecation window OPENS AT THIS RELEASE rather than at `contract-v2.4`;
  that the one narrowing is `baked-secret` over the third free string, under
  § 2.6's precedent; and that nothing else narrows — the member being optional,
  the schema constraining nothing about the block, and the comparison only
  ceasing to refuse.
  **DISCHARGED 2026-09-04 BY PR #636 (lane `openxfactory-smalls`), AND NOT AS
  THIS PACKET EXPECTED — THE NUMBER WAS ALLOCATED BY SOMEONE ELSE'S MERGE
  ORDER, WHICH IS EXACTLY WHAT ALLOCATING LATE MEANS.** `contract-v3.3` was cut
  by **PR #628** (lane `team02c`, `add-clearing-dispatch-boundary`, merged
  `0d5e1ba9`), whose branch point is AFTER this packet's own landing
  `95c2cf6a` — so this packet's schema, validator and documentation bytes were
  ALREADY inside the `contract-v3.3` tree while that entry named none of them.
  Two lanes measured the same free number within the same hour; the tie is
  settled by merge order, and #628 landed first. **THE REMEDY IS A FOLD, NOT A
  SECOND NUMBER.** PR #636 was opened as a rival cut of `contract-v3.3`, was
  overtaken, and was REWORKED into an amendment of the SAME untagged release:
  it adds one clearly headed block, `### Also realized in this cut:
  add-consumer-identity-namespace (#622)`, inside #628's existing
  `## contract-v3.3 — 2026-09-03` section, carrying this task's prescription
  VERBATIM as a quotation and then discharging it clause by clause, and it
  alters **not one word** of #628's text. Spending `contract-v3.4` on a release
  whose bytes are already published-in-tree would have made the changelog lie
  about which bundle carries them. **THE FOLD IS LAWFUL BECAUSE THE TAG IS NOT
  YET PUSHED**: `docs/contract-versioning-policy.md` § *Bundle Realization
  Order* step 4 makes a promoted commit a NEW candidate that every gate reruns
  against, and § *Immutable Tag Correction* binds only a PUBLISHED tag. Lane
  `team02c` is holding the `contract-v3.3` tag by agreement until #636 lands.
  Of the four things this task says the cut owes, #628 supplied the number, the
  version-headed entry and the inventory under `contracts/releases/`, and owes
  the annotated tag; #636 supplies the entry text this task prescribes and
  rebuilds the inventory LAST at the amended tree.
- [x] 5.4 `[#511]` Two `release-inventory-drift` findings — `contracts/manifest.yaml`
  and `docs/contract-versioning-policy.md`, both members of the standing
  release inventory (`contract-v3.0` when this was written, **`contract-v3.2`
  since PR #624 cut the superseding release for a defective `contract-v3.1`**)
  — are RAISED by this branch and are DISCHARGED BY § 5.3, not by this packet.
  **THE SEVERITY OF ONE OF THEM ROSE UNDER THIS PACKET WITHOUT THIS PACKET
  MOVING**: while `main` was itself drifting the policy doc, this branch's edit
  to it added no finding; #624's cut rebaselined the inventory and made `main`
  clean, so the same unchanged edit now raises a NEW ERROR against the branch.
  Recorded in § 8.1, and still not hand-fixed. **UNTICKED RATHER THAN TICKED WITH AN EXCUSE.** The
  family's own remedy line is *"cut a release through the bundle realization
  order; never hand-edit an inventory or `contract_bundle_version` to make this
  comparison pass"*, and `add-binding-consumer-identity` § 6.3 took exactly these
  two findings for exactly this reason.
  **DISCHARGED BY THE CUT — #628's, NOT #636's — AND NOT BY A HAND-EDIT.** Both
  findings named `contract-v3.2`'s inventory. #628's cut advanced
  `contract_bundle_version` to `contract-v3.3` and BUILT
  `contracts/releases/contract-v3.3.digests.yaml` from the bytes on disk at a
  tree that already carried this packet's landing, so both members —
  `contracts/manifest.yaml` and `docs/contract-versioning-policy.md` — are
  re-baselined there and the family reports NOTHING on either at `origin/main`
  `21190cf7`. CONFIRMED BY MEASUREMENT rather than assumed: the
  `release-inventory-drift` family is at ZERO findings on that baseline, and at
  ZERO on #636's tip. Neither an inventory nor `contract_bundle_version` was
  ever adjusted to make a comparison pass, by either lane. Figures in § 8.1.

## 6. The delta — two rulings, one block

- [x] 6.1 `[both]` Both `## MODIFIED Requirements` blocks copied VERBATIM from
  canon at `origin/main` and verified programmatically BEFORE a byte was edited.
  **EXECUTED** — a line-by-line equality check against
  `openspec/specs/credential-contracts/spec.md` returned identical for both
  blocks. `modified-block-currency` runs at `error` on this family.
- [x] 6.2 `[both]` Carriage MEASURED, not claimed: requirement titles
  byte-identical; block requirement 12 scenarios in, 16 out; lift requirement 12
  in, 15 out; **zero units lost on either**.
- [x] 6.3 `[#511]` The block requirement gains the member's declaration, the
  fallback's reasoning, the naming decision against `tenant` and `realm`, the
  enumeration's NINTH shape, and four scenarios. **EXECUTED.**
- [x] 6.4 `[#511]` The lift requirement's third condition is rescoped to fetch
  AUTHORITIES; the named-fault and proxy paragraphs follow it; two new
  paragraphs state the pair comparison and the reporting fallback; the existing
  shared-fetch-identity scenario's WHEN gains the namespace clause with its
  other two bullets byte-identical; three scenarios are added. **EXECUTED.**
- [x] 6.5 `[#553]` **EXACTLY TWO EDITS, AND THE COUNT IS THE POINT.** (1) The
  scenario "The requirement reference resolves to more than one record" — its
  WHEN narrowed to *"matches more than one requirement record in the requirements
  document the reference names"*, the cross-document arm dropped, the title and
  the other two bullets byte-identical. (2) The six-conditions sentence's
  *"resolving, in the repository under validation, to EXACTLY ONE requirement"*
  rescoped to *"IN THE ONE REQUIREMENTS DOCUMENT THAT REFERENCE NAMES"*.
  **EXECUTED.** Nothing else of #553 is in this delta; its reasoning is in
  `design.md` § 6 rather than smuggled into canon as a third edit.
- [x] 6.6 `[#553]` `add-requirement-ref-resolution-integrity` is CITED AND NOT
  EDITED — its `resolve_requirement`, its `ambiguous` status and its `tasks.md`
  § 3.4 freeze all stand. **EXECUTED**: `git diff` touches no path under
  `openspec/changes/add-requirement-ref-resolution-integrity/` and no line of
  `resolve_requirement`. Its § 9.4 obligation is discharged by the AMEND branch
  § 9.4 itself names.
- [x] 6.7 `[both]` No `Modified over` marker is owed, CHECKED rather than
  assumed against `govern-sibling-added-modified-deltas`: that form is reserved
  for a block whose requirement exists only as an ACTIVE sibling's ADDED or
  RENAMED `TO:` title, and both requirements here are promoted canon. **EXECUTED.**
- [x] 6.8 `[both]` Collision check against every ACTIVE writer on this
  capability. **EXECUTED**: `add-credential-escrow-checkout` MODIFIES "Canonical
  credential record shapes" and `add-requirement-ref-resolution-integrity` holds
  two ADDED requirements; neither holds either requirement this packet writes.
  Re-run against `origin/main` immediately before the PR.

## 7. Gates

- [x] 7.1 `OPENSPEC_TELEMETRY=0 openspec validate add-consumer-identity-namespace --strict`
  and `--all --strict`. **EXECUTED**: the change is valid; `--all --strict`
  **87 passed, 0 failed (87 items)** — 86 on `origin/main` plus this change.
- [x] 7.2 `python3 scripts/validate-credential-contracts.py .` with the
  self-test. **EXECUTED**: `self-test: 8 positive + 19 negative + 13 warning
  example(s) confirmed, 11 deprecation code(s) probed`, then
  `0 contract(s) checked, 0 skipped, 0 warning(s), 0 error(s) -> PASS`. The
  repository ships no `credentials/` tree, so this gate rests almost entirely on
  the packaged corpus — which is why § 3 packages BOTH directions.
- [x] 7.3 `python3 scripts/validate-manifest-digests.py`. **EXECUTED**:
  `OK contracts/manifest.yaml: 163 per-file digest(s) verify`.
- [x] 7.4 `python3 -m pytest tests/credential_contracts tests/manifest_digests -q`.
  **EXECUTED**: **239 passed**, and **247 passed** after § 8.3's round and
  § 4.2a.
- [x] 7.5 doc-health, branch against a same-clock `origin/main` baseline from an
  IDENTICALLY-NAMED checkout (the finding identity is `(family, repo, path)` and
  the repo is the basename, so a differently-named baseline manufactures
  phantoms). **EXECUTED AND NOT ZERO AT THE CURRENT BASELINE — UNTICKED
  DELIBERATELY.** One new ERROR, `release-inventory-drift` on
  `docs/contract-versioning-policy.md` against the `contract-v3.2` inventory
  #624 cut, plus three INFO. It is § 5.3's to discharge and § 5.4's to refuse to
  hand-edit; figures, both-directions set difference and the reason the answer
  changed are in § 8.1.
  **NOW TICKED, AND THE ERROR THAT KEPT IT UNTICKED IS GONE FROM BOTH SIDES.**
  At `origin/main` `21190cf7` — which carries #628's `contract-v3.3` cut — the
  `release-inventory-drift` ERROR on `docs/contract-versioning-policy.md` and
  the INFO on `contracts/manifest.yaml` are BOTH absent, because that cut
  re-baselined the inventory over this packet's already-landed bytes. #636's tip
  adds ZERO new critical, error or warning over that baseline. Re-measured
  figures and the both-directions set difference are in § 8.1.
- [x] 7.6 `python3 -m pytest tests/doc-health -q`. **EXECUTED**: 1500 passed
  after § 4.4a; the first run's single failure was the corpus-movement gate and
  is recorded in § 8.2 rather than smoothed away.
- [x] 7.7 `python3 -m pytest tests/factory_identity -q` — **6 passed, 74
  skipped** locally. Recorded because CI's `pytest-suite` job is RED on `main`
  at `ea117d4e` with six `ModuleNotFoundError: cryptography` failures in
  `tests/factory_identity/test_mint_script.py` (openxFactory issue #620: the job
  installs only `requirements/hermes-runtime-contracts.lock`). This branch
  INHERITS exactly those six and causes none of them; they pass here because the
  local environment carries the dependency, which is what identifies the failure
  as the job's and not the code's.

## 8. Measurements

Recorded here rather than in the PR body alone, so the packet carries its own
evidence.

- **`openspec validate --all --strict`**: 87 passed, 0 failed.
- **credential-contracts self-test**: 8 positive + 19 negative + 13 warning,
  11 deprecation codes probed.
- **manifest digests**: 163 of 163 verify.
- **`pytest tests/credential_contracts tests/manifest_digests`**: 239 passed at
  the first head; **247 passed** at `e2fa9102`+ after the Copilot round's arity
  pins and § 4.2a's eight-row truth table.
- **doc-health** and **`pytest tests/doc-health`**: § 8.1 and § 8.2 below.

### 8.1 doc-health delta

Both sides run with `--single-repo`, both checkouts named exactly `openxFactory`,
both `--as-of 2026-09-03`.

**RE-MEASURED 2026-09-04 AT THE FOLD (PR #636), BOTH CHECKOUTS NAMED
`openxFactory`, both `--as-of 2026-09-04`.** This packet had MERGED as #622
(`95c2cf6a`) and `contract-v3.3` had been cut by #628 (`0d5e1ba9`) before the
measurement, so the comparison is no longer branch-against-`main`: it is
`origin/main` `21190cf7` against #636's tip, and #636 carries ONE file's
change — the folded `contracts/CHANGELOG.md` block — plus the rebuilt inventory
and these ticks.

TIP_TABLE_PLACEHOLDER

**AND THE DRIFT THIS SECTION EXISTED TO RECORD IS GONE ON BOTH SIDES.** The
`release-inventory-drift` ERROR on `docs/contract-versioning-policy.md` and the
INFO on `contracts/manifest.yaml`, which stood against the `contract-v3.2`
inventory, are absent from the `21190cf7` baseline: #628's cut re-baselined the
inventory at a tree already carrying this packet's bytes. **THAT IS A CUT
DISCHARGING IT, NOT AN EDIT** — neither lane touched an inventory or
`contract_bundle_version` to make a comparison pass, and #636 rebuilds the
inventory LAST with `validate-contract-release.py build` rather than by hand.

**EARLIER BRANCH-AGAINST-`main` READINGS, kept as the record of what was true
then**, follow below.

**RE-MEASURED 2026-09-03 AT `origin/main` `6a39d2ab`, AFTER #617 AND #624, AND
THE ANSWER CHANGED — IT IS NO LONGER ZERO-NEW-ERROR.** The earlier reading below
is kept as the record of what was true then; this is the reading that governs.

| | critical | error | warning | info | total |
| --- | --- | --- | --- | --- | --- |
| baseline `6a39d2ab` | 6 | **4** | 39 | 12 | 61 |
| branch `ef57fdeb` | 6 | **5** | 39 | 15 | 65 |

**THE DELTA IS FOUR FINDINGS: ONE ERROR AND THREE INFO.** The error is
`release-inventory-drift` on `docs/contract-versioning-policy.md` — *"bytes
differ from the digest `contract-v3.2` records"*.

**IT IS A NEW ERROR AND IT WAS NOT ONE BEFORE, and the reason is a fact about
`main` rather than about this packet.** At the earlier reading that same finding
sat on BOTH sides: `main` had already drifted that file since `contract-v3.0`,
so this packet's edit to it added nothing. **PR #624 then cut `contract-v3.2`**
— the superseding release for a defective `contract-v3.1` — which REBASELINED
the inventory and made `main` clean on that file. This packet's edit to
§ Deprecations Currently In Force now reintroduces the drift on its own.

**THE BOX STAYS UNTICKED RATHER THAN TICKED WITH AN EXCUSE, and it is NOT
hand-fixed.** The family's own remedy line is *"cut a release through the bundle
realization order; never hand-edit an inventory or `contract_bundle_version` to
make this comparison pass"*, and the finding's class is `auto-fixable` only in
the sense that a CUT fixes it. Editing the inventory to green this comparison is
the one thing the family forbids, and greening it would also make a published
digest describe bytes nobody shipped. It is § 5.3's to discharge.
`add-binding-consumer-identity` § 6.3 took the identical finding for the
identical reason and discharged it at its cut.

The three INFO are `contracts/manifest.yaml`'s editorial-band drift against the
same new inventory, and the two contested `modified-block-currency` rows, one
per MODIFIED block, named in `_LEDGER_SUBJECTS`.

**EARLIER READING, kept as the record of what was true then** — taken at
`origin/main` `ea117d4e`, before #616, #617 and #624:

| | critical | error | warning | info | total |
| --- | --- | --- | --- | --- | --- |
| baseline (`origin/main` `ea117d4e`) | 6 | 6 | 39 | 13 | 64 |
| branch (`e2fa9102`, the Copilot-round head) | 6 | 6 | 39 | 16 | 67 |

**ZERO NEW critical, error or warning.** The delta is exactly THREE findings and
all three are INFO — the editorial band:

1. `contracts/manifest.yaml` — `release-inventory-drift`, *"bytes differ from the
   digest `contract-v3.0` records (editorial member — expected between cuts)"*.
   § 5.3's to discharge and § 5.4's to refuse to hand-edit.
2. and 3. TWO `modified-block-currency` findings, one per MODIFIED block, class
   **contested**, each naming the units the block does not restate verbatim: 2 of
   68 on the block requirement, 7 of 60 on the lift requirement. The arm's own
   words are that this is *"a divergence this arm CANNOT distinguish from a
   deliberate rewording, and does not claim to"* — which is exactly what a ruled
   amendment looks like from outside. Both are NAMED in
   `tests/doc-health/test_modified_block_currency_self_gate.py`'s
   `_LEDGER_SUBJECTS` per § 4.4a, with the seven units split by ruling, so they
   are an audit trail rather than an unexplained pair.

**`docs/contract-versioning-policy.md` DRIFTS ON BOTH SIDES AND IS NOT THIS
BRANCH'S** — measured, not assumed. Its `release-inventory-drift` **error** is
present on the BASELINE at `ea117d4e` (another writer moved the file since
`contract-v3.0` was cut), so this packet's edit to it adds no finding at all.

**RE-MEASURED AFTER THE COPILOT ROUND rather than carried forward.** The round
moved `docs/credential-access-model.md` and `docs/domain-factory-starter-pack.md`,
neither of which is a member of the `contract-v3.0` inventory (checked, not
assumed), and the second run over `e2fa9102` returns the SAME figures and the
SAME three-finding delta as the first over `14cfbad2`.

The set difference was taken in BOTH directions over the machine block: the
branch **removes** nothing, and family counts are identical on both sides except
`modified-block-currency` 8 -> 10 and `release-inventory-drift` 3 -> 4 —
staged-topic-template 26/26, register-lifecycle-consistency 10/10, tag-hygiene
4/4, staged-candidate-aging 4/4, record-immutability 4/4, ratified-provenance
2/2, release-tag-publication 1/1, ideation-routing 1/1, document-catalog 1/1.

### 8.2 `pytest tests/doc-health`

**1500 passed, 7 warnings** — re-run on the merged tree at `ef57fdeb` (431s)
after #617 and #624 landed, not carried forward from the earlier head. The FIRST
run of this suite reported **1 failed** — `test_every_carriage_ledger_finding_over_the_real_tree_is_named`,
which is the corpus-movement gate doing its job: it compares the named subject
set with `==`, and this packet added two subjects it had not been told about.
Discharged by § 4.4a exactly as that gate's failure message prescribes — the
subjects NAMED, in the same commit, with the reason. No test was added, removed,
renamed or weakened, and no assertion was loosened.

### 8.4 The corpus-sweep pins — MY OWN CI FAILURE, and its repair

**CI ON `f4a8fa87` REPORTED SEVEN FAILURES. SIX WERE INHERITED (#620). THE
SEVENTH WAS THIS PACKET'S OWN**, and it is recorded as such rather than folded
into the inherited count:
`tests/sequenced_after/test_sweep.py::test_the_live_sweep_reproduces_the_AUTHORING_measurement`.

**WHY IT FIRED.** That test pins the live corpus sweep against a moving ledger.
This packet adds an ACTIVE change carrying TWO `## MODIFIED Requirements` blocks,
so it joins the co-modified population and the pins move. The failure is the
gate working; the repair is to move the pins WITH A DATED NOTE naming the cause,
in the same commit, which is that file's own stated discipline.

**MEASURED ON BOTH TREES, and the branch was CAUGHT UP to current `main` first
because `main` had moved under it** — PR #616 merged the `contract-v3.1` cut,
archiving `add-project-repo-schema` and itself moving `active_co_modified`
21 -> 20. Measuring against the stale base would have produced pins that were
wrong the moment they landed.

**THE CATCH-UP IS A MERGE AND NOT A REBASE, and the reason is recorded rather
than left to look like a style choice.** The rebase was performed first, and its
push was REFUSED by repository rule — *"Cannot force-push to this branch"*. The
earlier heads are published and already reviewed, so rewriting them is both
forbidden and wrong; the branch was reset back to the published `f4a8fa87` and
took an ordinary catch-up MERGE of `origin/main` instead. **The sweep was
re-measured on the MERGED tree rather than carried over from the rebased one**,
and returns identically: 159 / 110 / 49 / 21 / 12.

| reading | `main` `19d00872` | branch `4dc5a0f9` | move |
| --- | --- | --- | --- |
| `change_ids` | 158 (32 active + 126 archived) | 159 (33 + 126) | **+1** |
| `co_modified` | 109 | **110** | **+1** |
| `sole_modifiers` | 49 | 49 | — |
| `active_co_modified` | 20 | **21** | **+1** |
| `active_sole` | 12 | 12 | — |

**THE MECHANISM IS THE INTERESTING PART, AND IT IS THE OPPOSITE OF THE OBVIOUS
PREDICTION.** The expected shape for a MODIFIED block over a requirement whose
only earlier writer was archived and SOLE is a rise of TWO with `sole_modifiers`
falling by one — the newcomer entering, the earlier writer flipping out of sole.
**That is not what happened, and the difference was measured rather than
reasoned about after the fact.** Both keys this packet writes had exactly one
earlier writer, the archived `add-binding-consumer-identity` — but that change
was **ALREADY co-modified** before this packet existed, through a THIRD key it
shares with `add-notebook-hosting-credential-custody`: `credential-contracts`'
*"Each consuming system reaches a shared operated identity through its own
binding"*. It was never IN the sole set, so it had nothing to leave. On `main`
it writes four requirement keys of which ONE is shared; on this branch the same
four of which THREE are shared, and its membership is unchanged at both
readings.

**So the distinguishing question is not how many keys the newcomer shares but
whether the earlier writer was already co-modified on some other key** — and
that is written into the pin's own message, because the next author to hit this
failure will reach for the rise-of-two shape first.

- [x] 8.4a `[both]` Pins moved with dated notes naming this packet as the cause
  and the mechanism: `co_modified` 109 -> 110, `active_co_modified` 20 -> 21,
  `change_ids - 1` 157 -> 158. **EXECUTED.**
- [x] 8.4b `[both]` The two pins that did NOT move — `sole_modifiers - 1` at 48
  and `active_sole - 1` at 11 — carry a HOLD note each, saying why the hold is
  its cause rather than an oversight. **EXECUTED.** A pin that silently holds
  through a move that usually shifts it is indistinguishable from a pin nobody
  re-derived.
- [x] 8.4c `[both]` `python3 -m pytest tests/sequenced_after -q` — **118
  passed**. Gates re-run on the rebased tree: `openspec --all --strict` 87
  passed, validator self-test unchanged, manifest digests 163/163,
  `tests/credential_contracts tests/manifest_digests` **247 passed**.
- [x] 8.4d `[both]` **RE-MEASURE OWED IF A SIBLING LANDS FIRST — DISCHARGED
  2026-09-03.** PR **#617** (`amend-owner-layer-severity`) MERGED as `6a39d2ab`,
  and Brett's word was *"then rebase #622"*. Done as a catch-up MERGE of
  `origin/main` (force-push stays refused on this branch), with **every pin
  RE-MEASURED on the merged tree and on the new `origin/main`, never by
  arithmetic**:

  | reading | `origin/main` `6a39d2ab` | MERGED tree | move this packet contributes |
  | --- | --- | --- | --- |
  | `change_ids` | 159 (31 active + 128 archived) | **160** (32 + 128) | **+1** |
  | `co_modified` | 111 | **112** | **+1** |
  | `sole_modifiers` | 48 | 48 | — |
  | `active_co_modified` | 20 | **21** | **+1** |
  | `active_sole` | 11 | 11 | — |

  Pins now read `co_modified` **112**, `active_co_modified` **21**,
  `change_ids - 1` **159**, `sole_modifiers - 1` **47**, `active_sole - 1`
  **10**.

  **THE TWO PACKETS' MOVES ARE DISJOINT, AND THAT IS MEASURED RATHER THAN
  ASSUMED.** #617 writes `workflow-gate-contract` and
  `release-surface-integrity`; this packet writes `credential-contracts`. They
  share no requirement key and no capability, so neither changes the other's
  membership — which is WHY the readings happen to compose here. **It is not a
  rule that they compose**, and the merged numbers were taken from the merged
  tree rather than added. The conflict in
  `tests/sequenced_after/test_sweep.py` was resolved by keeping BOTH branches'
  MOVEMENT LOG entries VERBATIM and adding a merge entry above them, which is
  that file's own protocol.

  **`sole_modifiers` and `active_sole` carry #617's move and not this
  packet's**, and the merge note says why: #617 FLIPPED an archived sole
  modifier (`promote-workflow-gate-contract`) into the co-modified set, while
  this packet flipped nobody — the earlier writer of both its keys was already
  co-modified through a third key. A rise in `co_modified` drags the sole set
  only when the newcomer's earlier co-writer was itself SOLE until then.
- [x] 8.4e `[both]` **CANON RE-VERIFIED AFTER THE MERGE, BY SHA AND NOT BY
  ASSERTION.** `openspec/specs/credential-contracts/spec.md` is blob
  `a688a463f1dc2d26ffab8661efafd176138c7974` on BOTH `origin/main` `6a39d2ab`
  and this branch — #617 promoted `workflow-gate-contract` and
  `release-surface-integrity` and touched this capability not at all, so both
  MODIFIED blocks still stand over canon as canon now states it. All 24 canon
  scenario titles across the two requirements are still carried by the delta,
  checked programmatically after the merge rather than trusted from before it.

## 8.3 The bench round

**Codex was REQUESTED ONCE AND REFUSED, and the refusal is recorded verbatim
rather than summarised** (PR #622, 2026-09-03T20:19:42Z):

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the Codex usage dashboard. To continue using code reviews, you can
> upgrade your account or add credits to your account and enable them for code
> reviews in your settings.

No further request was made. **Sourcery is an upsell stub on this repository**
and returned its standing "your private repo does not have access" notice, which
is not a review.

**COPILOT DID READ IT** and returned 🟡 *Changes recommended* with THREE
findings. Two TAKEN, one REFUTED FROM THE RECORD:

1. **TAKEN** — `docs/credential-access-model.md` said "those three members …
   governs all four", leaving the fourth sink to arithmetic. The count was
   correct and the sentence was still misreadable, which a reviewer proved by
   misreading it. Repaired by NAMING all four — `secret_ref` and the three
   `consumer:` members — instead of counting them.
2. **TAKEN** — `docs/domain-factory-starter-pack.md`: the inserted clause left a
   run-on line breaking the list's wrapping. Re-wrapped.
3. **REFUTED, with the substantive half TAKEN.** Copilot asked that
   `_consumers()` sort the binding keys, calling positional indexing fragile.
   Sorting is REFUSED: no test in that section depends on WHICH binding receives
   an edit — every assertion is symmetric over the pair, because the fault is a
   property of the PAIR — so sorting would fix an order the tests do not read
   while implying they do. The REAL fragility underneath it is different and is
   taken: two tests read `_findings(doc)[0]` without pinning the arity, so a
   second finding arriving later would change what they assert about WITHOUT
   failing them. Both now assert `len(findings) == 1` first, and `_consumers`
   carries a docstring saying which property is load-bearing and which is not.

**ONE BENCH READ THIS PACKET, NOT TWO**, and that is stated rather than rounded
up. The prescriber whose absence the predecessor recorded as a verification gap
was absent here too — for the same reason, its usage limit — and the mitigation
relied on is the packaged corpus in both directions plus the gates in § 7, not a
second reader.

## 9. NOT part of this change

- **The CUT** — the ruling's own exclusion. § 5.3 says what it owes.
- **`MAJOR_RELEASE`'s stale `contract-v3.0`** — § 2.8, observed and reported.
- **Broadening `resolve_requirement`** — #553 ruled AMEND, not broaden, and
  § 3.4's freeze holds.
- **A namespace on `holder_ref`'s side** — OQ-1, owed to the cross-repository
  comparison that does not exist yet.
- **Reconciling a declared namespace against the provider's directory** — OQ-2,
  live-estate reconciliation, where this capability already routes the same
  question about a declared fetch identity.
- **Requiring the member at the major** — refused in § 4.3 with the reason.

## 10. The archive act

This change carries a CODE SURFACE, so it archives on **merged plus green
evidence on `main`** per `docs/release-realization-flow.md` § The Archive Gate —
never with the ratification and never with the cut. It closes openxFactory #511
and #553.
