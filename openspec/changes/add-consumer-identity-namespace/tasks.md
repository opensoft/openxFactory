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
  **EXECUTED** — nineteen tests, all named for the claim they make.
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
- [ ] 5.3 `[#511]` **THE CUT — NOT THIS CHANGE.** The ruling excludes it in
  terms. Whoever cuts owes, in one act: the number (allocated by merge order —
  `contract-v3.1` is being spent by PR #616 as this is written), a
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
- [ ] 5.4 `[#511]` Two `release-inventory-drift` findings — `contracts/manifest.yaml`
  and `docs/contract-versioning-policy.md`, both members of the standing
  `contract-v3.0` inventory — are RAISED by this branch and are DISCHARGED BY
  § 5.3, not by this packet. **UNTICKED RATHER THAN TICKED WITH AN EXCUSE.** The
  family's own remedy line is *"cut a release through the bundle realization
  order; never hand-edit an inventory or `contract_bundle_version` to make this
  comparison pass"*, and `add-binding-consumer-identity` § 6.3 took exactly these
  two findings for exactly this reason.

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
  **EXECUTED**: **239 passed**.
- [x] 7.5 doc-health, branch against a same-clock `origin/main` baseline from an
  IDENTICALLY-NAMED checkout (the finding identity is `(family, repo, path)` and
  the repo is the basename, so a differently-named baseline manufactures
  phantoms). **EXECUTED** — figures and the both-directions set difference are
  recorded in § 8.
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
- **`pytest tests/credential_contracts tests/manifest_digests`**: 239 passed.
- **doc-health** and **`pytest tests/doc-health`**: § 8.1 and § 8.2 below.

### 8.1 doc-health delta

Both sides run with `--single-repo`, both checkouts named exactly `openxFactory`,
both `--as-of 2026-09-03`.

| | critical | error | warning | info | total |
| --- | --- | --- | --- | --- | --- |
| baseline (`origin/main` `ea117d4e`) | 6 | 6 | 39 | 13 | 64 |
| branch (`14cfbad2`) | 6 | 6 | 39 | 16 | 67 |

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

The set difference was taken in BOTH directions over the machine block: the
branch **removes** nothing, and family counts are identical on both sides except
`modified-block-currency` 8 -> 10 and `release-inventory-drift` 3 -> 4 —
staged-topic-template 26/26, register-lifecycle-consistency 10/10, tag-hygiene
4/4, staged-candidate-aging 4/4, record-immutability 4/4, ratified-provenance
2/2, release-tag-publication 1/1, ideation-routing 1/1, document-catalog 1/1.

### 8.2 `pytest tests/doc-health`

**1500 passed, 7 warnings** in 487s. The FIRST run of this suite reported **1
failed** — `test_every_carriage_ledger_finding_over_the_real_tree_is_named`,
which is the corpus-movement gate doing its job: it compares the named subject
set with `==`, and this packet added two subjects it had not been told about.
Discharged by § 4.4a exactly as that gate's failure message prescribes — the
subjects NAMED, in the same commit, with the reason. No test was added, removed,
renamed or weakened, and no assertion was loosened.

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
