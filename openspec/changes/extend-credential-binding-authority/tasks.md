# Tasks: extend-credential-binding-authority

Status: draft

NOTHING BELOW RUNS BEFORE RATIFICATION. This packet's own diff is its FIVE
records — `.openspec.yaml`, `proposal.md`, `design.md`, `tasks.md` and the
`credential-contracts` spec delta — plus one README entry; every task here is
authorized by a ratification that has not happened yet. The count is stated
because it SCOPES what changes before ratification, so an enumeration that omits
a record understates exactly the thing it exists to bound.

**No task creates, moves, or reads a live secret.** The realization surface is
a schema, a validator, nine fixtures and a test — and, beyond that code surface,
the documentation of § 4, the contract-release ritual of § 5, and the validation
of § 6. Naming only the code half would let a reader skim past the ritual, which
is the largest obligation in this packet.

## 1. The schema carries the authority

- [ ] 1.1 Add FOUR ADDITIVE OPTIONAL string properties to each entry of
  `credential_bindings` in `xfactory_credential_binding_template`
  (`contracts/schemas/xfactory-credential-contracts.schema.yaml`): `consumer`,
  `fetch_identity`, `identity_namespace`, `requirement_id`. The `required` list is UNCHANGED —
  adding a required field is the breaking class and is not this cut.
- [ ] 1.2 Describe each property in the schema itself, in the style the
  `issuance_preconditions` block set: what the field means, and why the record
  needs it rather than review. Name `fetch_identity` as the family's single
  record spelling and "access identity" as its prose synonym, so a reader
  arriving from the custody requirement is not left wondering whether two
  fields are meant.
- [ ] 1.3 Do NOT add `additionalProperties: false` to the binding object — but
  NOT for the reason an earlier revision of this task gave. **That reason was
  measurably wrong and is corrected rather than deleted.** It claimed closing the
  object would invalidate the shipped `resolution:` block in
  `contracts/avatar-client/broker-server-key-binding.template.yaml`; review
  EXECUTED the closure against every shipped record and found that **nothing
  shipped becomes invalid** — `resolution:` is a DOCUMENT-level key and the
  closure applies to the per-binding object, which no shipped record extends.
  The only thing refused was `access_identity`, the second spelling this packet
  wants refused anyway. The real reason is the RULE, not a counterexample:
  closing an open object narrows what is valid, and narrowing is a
  major-version act regardless of whether anything in this tree happens to
  occupy the space today — a repository is not the population. Decision 6.
- [ ] 1.4 Leave `contract_schema_version` unchanged. Nothing previously valid
  becomes invalid, which is the test the versioning policy applies.

## 2. The validator compares authorities

- [ ] 2.1 Add the validator's FIRST WARNING CHANNEL. Warnings print with a
  `WARN` prefix, do NOT increment the error count, and do NOT change the exit
  code. Keep it structurally separate from `_semantic_findings` rather than
  smuggling a severity marker into the existing strings, so a caller cannot
  count a warning as an error by accident.
- [ ] 2.2 `binding-authority-undeclared` (WARNING): a binding that does not
  declare BOTH `consumer` and `fetch_identity`. FIRES ON EITHER ABSENCE, not
  only on both — the two are refused together at the next major version, so a
  record declaring one and omitting the other must be warned or it breaks there
  with no notice. The message NAMES WHICHEVER IS MISSING (both, when both are)
  and states the removal version allocated at 5.2; a deprecation warning that
  does not say when it becomes an error is not a migration path. NOT raised for
  a missing `requirement_id` — warning on it would put it on the deprecation
  path this packet deliberately keeps it off.
- [ ] 2.3 `shared-fetch-identity` (ERROR): within one document, two bindings
  whose QUALIFIED identity key `(provider, identity_namespace, fetch_identity)`
  is equal, while both declare `consumer` and the consumers differ. Where
  `identity_namespace` is undeclared on either side the key falls back to
  `(provider, fetch_identity)` — which REPORTS rather than clears, because
  silence is not distinctness. NEVER the bare string, and NEVER qualified by
  `vault`: `fetch_identity` is a name in the PROVIDER'S IDENTITY
  namespace, so two bindings labelling a principal `runtime_identity` against
  different providers are not one authority — but ONE principal granted on TWO
  vaults IS one authority, and a vault-qualified key would report nothing on
  exactly the record the ratified per-system rule forbids. NOT raised when either side omits `consumer`: the record
  cannot distinguish one consumer from two, 2.2's warning already stands on
  that binding, and inventing a verdict from an absent field is how a check
  earns distrust.
- [ ] 2.4 Refine `shared-secret-identity` (ERROR): group bindings by the
  QUALIFIED secret key `(provider, vault, secret_ref)` — not by the bare
  `secret_ref` it groups by today — **WITH A MANDATORY FALLBACK: where ANY member
  of a matching `(provider, secret_ref)` set omits `vault`, group that set by the
  BARE `secret_ref` instead and adjudicate on those terms.** A group of size > 1
  raises UNLESS every member declares an equal `requirement_id` and
  pairwise-distinct `consumer` and pairwise-distinct QUALIFIED `fetch_identity`
  on `(provider, identity_namespace, fetch_identity)` — the secret key carries
  `vault`, the identity key carries the namespace instead — **and where ANY
  member of a compared pair omits `identity_namespace`, compare that pair on
  `(provider, fetch_identity)` alone, exactly as 2.3 does for the collision
  rule. THE EXEMPTION MUST NOT OPEN ON AN INDETERMINATE QUALIFICATION.** Without
  this, two bindings on one secret and one requirement with distinct consumers,
  the SAME `fetch_identity` and the namespace on ONE side only have differing
  triples, read as "distinct", and the shared-secret refusal is LOST — the
  either-side scope is what keeps the two rules pointing the same way.
  **THE FALLBACK IS NOT OPTIONAL AND ITS ABSENCE WAS A DEFECT, NOT A
  SIMPLIFICATION.** An earlier revision of this task claimed the regrouping
  "only ever narrows a refusal, and only where the two secrets are genuinely
  distinct", and proved it against `dispatch-reuses-content-secret.yaml` as
  shipped. **The claim is false and the proof was one fixture wide**: delete the
  optional `vault:` line from ONE of that fixture's two bindings and an
  unconditional qualified key takes it from ERROR/exit 1 to clean/exit 0 — the
  backward-compatibility proof one deletion from going green. With the fallback
  the claim is true: no refusal in force today is removed, every genuine
  narrowing is kept, and `authority-scope-indeterminate` accompanies a verdict
  instead of replacing one. Decision 8.
  `requirement_id` is NOT qualified and must not be: it names a sibling record
  in the domain's own contract tree, not a name in a third party's namespace. The
  exemption is UNANIMOUS — one unaccounted member in a group of three is a
  refusal. Keep the existing message for the unexempted case; it is the same
  finding.
- [ ] 2.5 Assert the backward-compatibility property as a test, not as a claim:
  a record declaring none of the four fields is adjudicated exactly as it was
  before this change.

- [ ] 2.5a SEPARABLE COLLISION-ADJACENT WARNING (S-10): where a binding omits
  `consumer` AND its `fetch_identity` collides with another binding's — the exact
  case in which 2.3 fails open BECAUSE of that absence — the warning SHALL carry
  a distinct code or a distinct message clause from the estate-wide
  `binding-authority-undeclared` baseline. For a full minor that baseline fires
  on every legacy binding in the estate, so without a separable signal the one
  warning meaning "a refusal was suppressed here" is indistinguishable from
  thousands meaning "this record predates the field". It is the compensating
  control the rule-1 fail-open rests on, and a compensating control nobody can
  find is not one.
- [ ] 2.6 `authority-scope-indeterminate` (WARNING), SECRET COMPARISON ONLY: two
  bindings whose bare `secret_ref` matches under the same `provider`, where one
  declares a `vault` and the other omits it, so the record does not say whether
  they address one store. **IT ACCOMPANIES 2.4's FALLBACK VERDICT AND NEVER
  REPLACES IT** — on a shared bare reference the operator sees the ERROR *and*
  this warning, never this warning alone. Name both bindings and the missing
  `vault` so the remedy is obvious. It CANNOT arise on the identity key, whose
  own undeclared-qualifier case is handled by 2.3's fallback to
  `(provider, fetch_identity)` rather than by a warning — do not add a
  symmetrical identity branch here.

## 3. Fixtures and the count string, which move together

- [ ] 3.1 POSITIVE `examples/credential-contracts/notebook-hosting.binding-template.example.yaml`:
  two bindings, one `secret_ref`, one shared `requirement_id`, distinct
  `consumer` and distinct `fetch_identity`. This is the two-consumer shape the
  custody packet's task 4.1 DECLINED to package because the rule would trip it;
  packaging it here is the proof this change did its job. Use the estate's real
  vault and secret naming only where a fixture legitimately may — this is
  `examples/`, the same territory that already names
  `kv-opensoft-xfactory-qa` — and invent no fetch-identity value that asserts an
  estate fact not yet established.
- [ ] 3.2 NEGATIVE `negative/shared-fetch-identity.yaml`: two consumers, one
  fetch identity. Expect `shared-fetch-identity`.
- [ ] 3.3 NEGATIVE `negative/shared-secret-different-requirements.yaml`: two
  bindings sharing a `secret_ref` with distinct consumers AND distinct fetch
  identities but DIFFERENT `requirement_id`s. Expect `shared-secret-identity`.
  **This fixture is the executable form of the 4.1 argument** — green under the
  rejected discriminator, red under the ruled one — so the decision cannot be
  reversed later without a test going red.
- [ ] 3.4 Register EVERY new negative — all SIX (3.2, 3.3, 3.10, 3.11, 3.12, 3.13),
  not the two this task named before review added the others; an unregistered
  negative is already a self-test error by design. 3.11 registers a WARNING
  expectation and 3.12 registers BOTH an error and a warning, so both depend on
  3.15's widening.
- [ ] 3.5 Leave `negative/dispatch-reuses-content-secret.yaml` UNCHANGED and
  RED. It is the backward-compatibility proof, and a green result there means
  the exemption was written wrong.
- [ ] 3.6 Update `tests/credential_contracts/test_dispatch_credential_contract.py`
  IN THE SAME COMMIT as any fixture change: it asserts the self-test count string
  LITERALLY ("3 positive + 5 negative" today) and lists the fixture filenames, so
  both move with the fixtures. The final count is derived once, at 3.16, from
  what was actually added — 3.1-3.3 alone would make it "4 positive + 7
  negative", and 3.9-3.10 move it again, so no number is written here. The
  custody packet's task 4.1 named this coupling in advance.
- [ ] 3.7 Prove the warning on ALL THREE migration states, not just the empty
  one: a binding declaring NEITHER field, one declaring `consumer` ONLY, and one
  declaring `fetch_identity` ONLY. Each case asserts that a warning is raised,
  that it NAMES ONLY THE FIELD ACTUALLY MISSING, and that the run still exits 0.
  **A neither-only test cannot fail on the defect it exists to catch**: an
  implementation keeping a `not consumer and not fetch_identity` predicate stays
  silent on the half-declared binding and passes anyway, and an implementation
  that always names both fields passes while violating 2.2's message contract.
  That is this repository's own mutation-harness lesson — a proof that cannot go
  red on the fault is not a proof of the fault — and the half-declared shape is
  precisely where the review found the defect in the first place.
- [ ] 3.8 Pin 2.3's FAIL-OPEN the same way, because it has the same weakness:
  two bindings sharing a `fetch_identity` with `consumer` absent on one side must
  raise NO `shared-fetch-identity` error AND must still raise the
  `binding-authority-undeclared` warning, asserted together in one case.
  Asserting only the silence would pass for an implementation that had simply
  dropped the rule, and the whole justification for staying silent is that the
  warning is standing instead — so a test that does not check the warning is not
  testing the reasoning. Applying the lesson where it recurs rather than patching only the
  instance the review named.

- [ ] 3.9 POSITIVE, cross-provider: two bindings naming the SAME
  `fetch_identity` string under DIFFERENT providers, with different consumers.
  Must produce NO `shared-fetch-identity`. This is the fixture that proves the
  comparison is qualified; under the bare-string rule it is a false refusal, so
  it goes red the moment someone reverts the qualification.
- [ ] 3.10 NEGATIVE `negative/shared-fetch-identity-across-vaults.yaml`: two
  consumers, ONE provider, ONE `fetch_identity`, DIFFERENT `vault`s. Expect
  `shared-fetch-identity`. **This is the fixture that pins the identity key
  against re-acquiring `vault`** — it is green under the rejected
  vault-qualified key and red under the ruled one, so the decision cannot be
  silently reversed. Pair it with 3.9: together they prove the key is neither
  too wide nor too narrow, which no single fixture can.
- [ ] 3.11 NEGATIVE `negative/authority-scope-indeterminate.yaml`: same provider,
  same bare `secret_ref`, `vault` declared on one binding only, **AND the
  exemption's conditions all satisfied** (same `requirement_id`, distinct
  `consumer`s, distinct qualified `fetch_identity`s). Expect the WARNING and NO
  error. **ITS PREMISE CHANGED WITH THE FALLBACK AND THE FIXTURE IS RE-SPECIFIED
  RATHER THAN LEFT STALE**: before 2.4 gained the fallback, ANY undeclared-vault
  record warned without refusing, so this fixture was simply "vault on one side".
  Now that shape REFUSES too — that is 3.12 — so the warning-without-refusal case
  must be built deliberately, by satisfying the exemption. The two are NOT
  duplicates: 3.11 proves the warning stands alone where the record earns it,
  3.12 proves it never stands alone where the record does not.
  Registered against a WARNING rather than an error, which is what forces 3.15's
  widening.
- [ ] 3.12 NEGATIVE `negative/shared-secret-vault-undeclared.yaml` (S-2): ONE
  provider, ONE `secret_ref` shared by two bindings, `vault` declared on ONE side
  only. Expect `shared-secret-identity` (from 2.4's fallback grouping) AND
  `authority-scope-indeterminate` (accompanying it). **THIS IS THE FIXTURE THAT
  PINS THE FALLBACK**: it is GREEN under the rejected unconditional qualified
  grouping and RED under the ruled one, so the ruling lives in the tree and not
  only in a record. Assert BOTH findings, not just the error — asserting the
  error alone would pass for an implementation that dropped the warning, and
  asserting the warning alone is the very defect the fallback exists to prevent.
- [ ] 3.13 NEGATIVE `negative/exemption-one-sided-namespace.yaml` (LS-R3): one
  `secret_ref`, one `requirement_id`, DISTINCT consumers, the SAME
  `fetch_identity`, `identity_namespace` declared on ONE binding only. Expect
  `shared-secret-identity`. **This pins the exemption's either-side scope**: it
  is GREEN under the triple-only comparison — the exemption opens because the
  triples differ — and RED under the ruled one. It is the exemption-side twin of
  3.12, which pins the same principle on the grouping side, and the pair is why
  both rules can be said to point the same way rather than merely asserted to.
- [ ] 3.14 POSITIVE `two-namespaces.binding-template.example.yaml` (D3): two
  bindings, one provider, the SAME `fetch_identity` string, DISTINCT
  `identity_namespace` values, distinct consumers. Must produce NO
  `shared-fetch-identity`. This is what makes the "records the distinction"
  escape real rather than rhetorical, and it goes red if the namespace ever
  drops out of the identity key.
- [ ] 3.15 WIDEN THE SELF-TEST'S NEGATIVE ADJUDICATION, CONCRETELY (S-3). As it
  stands, `_self_test` reads `NEGATIVE_EXPECTATIONS.get(path.name)` → a single
  string, and checks `any(f.startswith(want) for f in _semantic_findings(doc))`.
  Task 2.1 requires warnings to be structurally separate from
  `_semantic_findings`, so that dict can NEVER express a warning expectation and
  3.11/3.12 have no home in it. **The mechanism: add a module-level
  `WARNING_EXPECTATIONS: dict[str, str]` beside `NEGATIVE_EXPECTATIONS`, and
  adjudicate each negative against BOTH** — every prefix registered in
  `NEGATIVE_EXPECTATIONS` must appear in `_semantic_findings(doc)`, every prefix
  registered in `WARNING_EXPECTATIONS` must appear in the warning channel, and a
  fixture named in NEITHER dict stays a self-test error exactly as an
  unregistered negative is today. A parallel dict is chosen over a tuple value on
  the existing dict so that the error path's shape and its `startswith`
  comparison are untouched — the widening adds a channel rather than editing the
  one the published check already adjudicates on.
- [ ] 3.16 Re-derive the self-test count string from the fixtures actually
  added, and update `tests/credential_contracts/` to match. Do NOT carry any
  earlier revision's number forward — this packet's fixture set has been
  restated four times under review, and the string is asserted LITERALLY.

## 4. Documentation

- [ ] 4.1 `docs/domain-factory-starter-pack.md` § 9: the
  `credentials/bindings.template.yaml` example gains the four fields, so the
  scaffold a domain copies is the conforming one rather than the minimal one.
  **Sweep the guidance bullets beneath it in the same edit** — the list says
  bindings belong to deployments and to use references, and it must now also
  say which authority reaches them; a definition gaining a conjunct leaves
  every one-conjunct sentence beside it stale.
- [ ] 4.2 `docs/credential-access-model.md`: record that per-system authority is
  now a property of the RECORD rather than of review, and that the declaration
  is an assertion by the binding's owner which nothing here verifies against the
  store. **Give this file the same treatment 4.1 gets** — the example AND the
  guidance bullets beneath it — rather than a prose note alone; a definition
  gaining a conjunct leaves every one-conjunct sentence beside it stale, and
  that rule does not stop at the starter pack.
- [ ] 4.2a EXTEND THE SWEEP TO THE TWO FILES REVIEW FOUND UNREACHED (S-9):
  `docs/notebook-projection-migration-runbook.md:104-106` and
  `docs/self-hosted-runtime-binding-plan.md:331-337`. Both carry one-conjunct
  binding descriptions that this change's four fields falsify, and **no task in
  any earlier revision reached either of them** — §7.2's five-occurrences-in-four-
  files sweep is correct for ITS fact (the custody packet's enforceability claim)
  and is not this sweep. Recorded as measured: promoted canon under
  `openspec/specs/` is CLEAN — zero occurrences of `secret_ref`,
  `rotation_policy`, `credential_bindings` or `shared-secret-identity` — so the
  sweep's whole surface is `docs/`, and it is these three files.
- [ ] 4.3 Do NOT edit `docs/lifecycle-notebook-projection.md` or any ratified
  custody text to change "access identity" to "fetch identity". The synonymy is
  declared in the requirement; a ratified record is not rewritten for a
  successor's convenience.

## 5. The contract release ritual

- [ ] 5.1 Assert the precondition before cutting: `contracts/` is untouched by
  the PROPOSAL commit series, so ratifying this packet drifts no release
  inventory. Re-verify at realization rather than trusting this line — the
  release surface moves.
- [ ] 5.2 ALLOCATE THE MINOR AT REALIZATION, BY MERGE ORDER, not before, and
  **FRESH-COUNT IT AGAINST `origin/main` AT THAT MOMENT RATHER THAN TRUSTING ANY
  NUMBER WRITTEN IN THIS PACKET.** This train moves faster than a proposal sits:
  this packet has already had `contract-v1.45`, `contract-v2.1` and
  `contract-v2.2` named as its expected allocation and outlived all three. As
  measured 2026-08-30, main declares `contract-v2.2` (cut and TAGGED) and the
  merged `add-signed-execution-chain` already names `contract-v2.3` as its own
  target, so the earliest number this packet could take is `contract-v2.4` — and
  that is a measurement, not a reservation. Read `contracts/manifest.yaml`,
  the `contracts/CHANGELOG.md` head and `git tag -l 'contract-v*'` on main, then
  take the next free minor. `add-credential-escrow-checkout` edits the same
  schema and owes a minor too. Bump `contract_bundle_version` in `contracts/manifest.yaml` and write
  the `contracts/CHANGELOG.md` entry ATOMICALLY with the contract files, per the
  policy's "The manifest and changelog update SHALL be committed atomically".
- [ ] 5.3 The CHANGELOG entry declares **change class ADDITIVE (minor)** and
  states, in the `contract-v2.1` entry's manner — membership established by
  PARSE rather than by grep — WHY the cut is owed: the schema is a registered
  bundle contract (`id: credential-contracts`) gaining optional fields and new
  validator warnings, which is the policy's additive class verbatim; it is NOT
  forced by `release-inventory-drift`, because the schema, its validator and
  `examples/` are none of them members of the declared bundle's digest
  inventory. Re-parse the inventory at realization and state the entry count
  observed; do not carry this packet's 192 forward as if it were still true.
- [ ] 5.4 The entry also records the DEPRECATION half: the authority-less
  binding shape is deprecated as of this cut, with the REMOVAL VERSION named
  (the next major) and the migration path stated — declare `consumer` and
  `fetch_identity`. The policy requires a deprecation to state both;
  `contract-v1.34` is the worked precedent, and its removal target was named in
  the same list this cut appends to.
  **AND NAME THE OBJECT-CLOSING'S REMOVAL VERSION IN THE SAME ENTRY (S-7).**
  Task 1.3 leaves the binding object OPEN, which is why a second spelling like
  `access_identity` validates silently at this minor. Left there, that is an
  open-ended promise that review will catch it. Instead the entry SHALL state
  that the binding object closes to unknown keys at the next major — the same
  release that makes `consumer` and `fetch_identity` required — so the second
  spelling carries a removal version rather than a standing intention.
  Recorded with it (LS-F10), because it bounds the risk and this packet did not
  previously claim it: the second spelling is not silent for long. From this cut
  a binding declaring `access_identity` and neither of the two real fields draws
  `binding-authority-undeclared` — the deprecation warning fires on exactly the
  record that misspelled the field, so the channel this change introduces is
  itself the compensating control for the gap task 1.3 leaves open.
- [ ] 5.5 Assert what does NOT move: no required field is added, no shape is
  removed, no vocabulary is reinterpreted, `contract_schema_version` is
  unchanged, and a consumer pinned at the previous bundle stays conformant until
  it deliberately upgrades. State it as the four properties, not as the word
  "additive".
- [ ] 5.6a REFRESH THE `credential-contracts` ROW'S `sha256` IN
  `contracts/manifest.yaml`, ATOMICALLY WITH THE SCHEMA EDIT (S-4). The manifest
  records a digest per registered contract, and this change edits the bytes that
  digest covers — so the row goes stale the moment 1.1 lands. **No earlier
  revision of § 5 named it**: the ritual listed the changelog, the bundle bump,
  the inventory rebuild, `verify-commit`, `verify-promotion` and the tag, and
  `verify-commit` does NOT read the manifest
  (`grep "manifest" scripts/validate-contract-release.py` → zero hits), so nothing
  would have caught it. Run `scripts/validate-manifest-digests.py` and READ ITS
  COUNT LINE. The versioning policy's own sentence makes this non-optional:
  consumers pin "the exact commit and required file digests".
  NOTE, and do not conflate the two: that checker is RED at head and at base on
  an unrelated row (`ideation-dashboard-snapshot.schema.yaml`, 1/145). That is a
  pre-existing defect owned elsewhere, NOT this change's, and it is routed
  separately — but it means a green run cannot be the acceptance signal here.
  Compare the `credential-contracts` row specifically.
- [ ] 5.6 Rebuild the inventory wholesale —
  `scripts/validate-contract-release.py build --tag <tag> --output contracts/releases/<tag>.digests.yaml` — then `verify-commit --commit <sha>`
  green, then `verify-promotion` before tagging, then the annotated tag, then
  `verify-tag` from an INDEPENDENT clone. The tag points at the realized
  commit; a bundle is not published until its tag exists.

- [ ] 5.7 THE REBASE OBLIGATION, WRITTEN DOWN NOW RATHER THAN MET AT A MERGE
  (D5). **Two sequential cuts, THIS PACKET FIRST**, with
  `add-credential-escrow-checkout` rebasing onto it. The coupling is CERTAIN, not
  conditional, and it is not where an earlier revision of this packet located it:
  it is in `_self_test` itself. `EXAMPLES_DIR` is HARD-CODED to
  `examples/credential-contracts` and `NEGATIVE_EXPECTATIONS` is a single
  module-level dict, so BOTH packets edit the same self-test count string and the
  same registry regardless of which tree their fixture files live in — the
  different-fixture-trees reasoning was about residency and never bore on this.
  Whichever lands second re-derives the count string and re-registers against the
  landed dict. **The party that owes it is `add-credential-escrow-checkout`**,
  because this packet cuts first. A dated one-line note is added to that packet's
  own `tasks.md` in this commit so the obligation is visible from the side that
  owes it; if that file is ever contended, the obligation still stands here.

## 6. Validate green

- [ ] 6.1 `python3 scripts/validate-credential-contracts.py .` clean, with the
  new self-test line printed and read.
- [ ] 6.2 `python3 -m pytest tests/credential_contracts tests/doc-health -q`.
- [ ] 6.3 `OPENSPEC_TELEMETRY=0 openspec validate extend-credential-binding-authority --strict`
  and `--all --strict`.
- [ ] 6.4 doc-health zero-new against a fresh `origin/main` baseline taken at
  the SAME as-of date and in a checkout whose BASENAME MATCHES the working
  one — report identity is `(family, repo, path)` with the repo read from the
  basename, so a mismatched baseline manufactures phantom regressions
  (issue #342).
- [ ] 6.5 Re-run every domain validator that reads this schema before the tag,
  not after.

## 7. Bookkeeping

- [ ] 7.1 README OpenSpec Records: this change is listed active on authoring and
  moves to archived when it archives.
- [ ] 7.2 At archive, tick task 4.5 of `add-notebook-hosting-credential-custody`
  and correct its § Impact sentence — "the per-system authority invariant is NOT
  machine-enforceable today" — which becomes false the moment this realizes.
  **That is a settled fact changing, so chase it to every place it is stated.**
  The set was MEASURED on 2026-08-29, not guessed, and it is FIVE statements in
  four files: that packet's `proposal.md` (§ Impact and its "no consumer or
  access-identity field" clause), its `design.md` § The binding shape these
  instances will use, its `tasks.md` § 4.5, and the scenario "The published
  binding shape cannot yet express the access identity" in its ratified delta.
  Re-measure at realization rather than trusting this list.
  TWO EXCLUSIONS, EACH DELIBERATE. This repository's README entry for that
  packet states the RULING and not the gap, so it needs no edit — chasing a fact
  means finding where it is stated, not editing every document that mentions the
  subject. And `review/ratification-2026-08-23.md` is `Status: record` and is
  NOT EDITED AT ALL: it records what was true and before the ratifier when he
  ruled, which is exactly what a later reader needs from it, on the same
  principle the versioning policy applies to `docs/archive-record-discrepancies.md`.
  Whether the ratified delta's now-false scenario is corrected by amendment or
  left standing as history is a lifecycle question for that packet's owner, not
  a silent edit by this one.
- [ ] 7.2a ARCHIVE ORDER IS A CONSTRAINT, NOT A PREFERENCE (S-14). This packet
  SHALL NOT archive before `add-notebook-hosting-credential-custody`. Its three
  ADDED requirements presume that packet's operated-identity framing, and that
  framing is NOT in promoted canon yet — measured: `grep -c "operated identity"`
  over `openspec/specs/` returns **0**. Archiving first would promote text
  resting on an obligation canon does not hold, which is a stale-canon defect
  created by ORDER alone and cured by order alone. Cheap to honour if written
  down, invisible if discovered at the archive gate.
- [ ] 7.2b STATE WHAT A VALIDATOR DOES WHEN THE MAP KEY AND `requirement_id`
  DISAGREE (S-13). A binding keyed `intent_dispatch` that declares
  `requirement_id: corpus_content_write` states the same fact twice and
  contradicts itself. The rule: REPORT the disagreement; do NOT silently prefer
  one. The requirement makes `requirement_id` authoritative for RESOLUTION, which
  is what a consumer needs, and that is not a licence for the checker to swallow
  a self-contradicting record — a record whose two statements of one fact
  conflict is a defect wherever the resolution lands.
- [ ] 7.3 Revisit task 4.1's declined fixture: its stated reason ("would TRIP
  the validator") no longer holds, and 3.1 packages the example it wanted.

## 8. NOT part of this change

- Constraining `fetch_identity`, `provider` or `vault` to a grammar. The
  qualification makes comparison sound WITHOUT narrowing what those strings may
  be; adding a format constraint would invalidate records valid today and is a
  major-version act.
- Cross-document authority comparison. Every rule here compares bindings within
  one template document, which was already true of `shared-secret-identity`.
  Estate-wide comparison needs a scan the validator does not perform; owed to a
  successor, and RECORDED as a limit rather than left implied.
- Verifying the declaration against the store. Nothing here reads a vault's
  grants, so a record naming two identities that are in fact one principal is
  conforming and wrong.
- Migrating `contracts/avatar-client/broker-server-key-binding.template.yaml`
  from its document-level `resolution.fetch_identity` to the per-binding field.
  `qualify-avatar-live-voice` is active and owns that record; it stays valid
  because this change narrows nothing.
- Closing the binding object to unknown keys. A narrowing, and a major-version
  act.
- Making `consumer` and `fetch_identity` required. The breaking class,
  scheduled for the next major after a full minor of warnings. `requirement_id`
  is NOT on that path: its absence never warns, so no major may require it, and
  it is obligatory only where a record claims the shared-secret exemption.
- Any edit to ratified custody text to align its "access identity" prose.
