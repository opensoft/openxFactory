# Tasks: extend-credential-binding-authority

Status: draft

NOTHING BELOW RUNS BEFORE RATIFICATION. This packet's own diff is the four
records and one README entry; every task here is authorized by a ratification
that has not happened yet. **No task creates, moves, or reads a live secret**:
the whole realization surface is a schema, a validator, three fixtures and a
test.

## 1. The schema carries the authority

- [ ] 1.1 Add three ADDITIVE OPTIONAL string properties to each entry of
  `credential_bindings` in `xfactory_credential_binding_template`
  (`contracts/schemas/xfactory-credential-contracts.schema.yaml`): `consumer`,
  `fetch_identity`, `requirement_id`. The `required` list is UNCHANGED —
  adding a required field is the breaking class and is not this cut.
- [ ] 1.2 Describe each property in the schema itself, in the style the
  `issuance_preconditions` block set: what the field means, and why the record
  needs it rather than review. Name `fetch_identity` as the family's single
  record spelling and "access identity" as its prose synonym, so a reader
  arriving from the custody requirement is not left wondering whether two
  fields are meant.
- [ ] 1.3 Do NOT add `additionalProperties: false` to the binding object.
  Closing it would invalidate records that are valid today — including the
  shipped `resolution:` block in
  `contracts/avatar-client/broker-server-key-binding.template.yaml` — and
  narrowing is a major-version act. Decision 6; the limit is stated in the
  requirement rather than left for a reader to find.
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
  only on both — the two are refused together at the next major, so a record
  declaring one and omitting the other must be warned or it breaks there with no
  notice. The message names whichever is missing and states the removal version
  allocated at 5.2; a deprecation warning that does not say when it becomes an
  error is not a migration path. NOT raised for a missing `requirement_id` —
  warning on it would put it on the deprecation path this packet deliberately
  keeps it off. The message names BOTH fields and states the
  removal version allocated at 5.2 — a deprecation warning that does not say
  when it becomes an error is not a migration path.
- [ ] 2.3 `shared-fetch-identity` (ERROR): within one document, two bindings
  declaring equal `fetch_identity` while both declare `consumer` and the
  consumers differ. NOT raised when either side omits `consumer`: the record
  cannot distinguish one consumer from two, 2.2's warning already stands on
  that binding, and inventing a verdict from an absent field is how a check
  earns distrust.
- [ ] 2.4 Refine `shared-secret-identity` (ERROR): group bindings by
  `secret_ref`; a group of size > 1 raises UNLESS every member declares an equal
  `requirement_id` and pairwise-distinct `consumer` and `fetch_identity`. The
  exemption is UNANIMOUS — one unaccounted member in a group of three is a
  refusal. Keep the existing message for the unexempted case; it is the same
  finding.
- [ ] 2.5 Assert the backward-compatibility property as a test, not as a claim:
  a record declaring none of the three fields is adjudicated exactly as it was
  before this change.

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
- [ ] 3.4 Register both negatives in `NEGATIVE_EXPECTATIONS`; an unregistered
  negative is already a self-test error, by design.
- [ ] 3.5 Leave `negative/dispatch-reuses-content-secret.yaml` UNCHANGED and
  RED. It is the backward-compatibility proof, and a green result there means
  the exemption was written wrong.
- [ ] 3.6 Update `tests/credential_contracts/test_dispatch_credential_contract.py`
  IN THE SAME COMMIT: the self-test count string moves "3 positive + 5 negative"
  → "4 positive + 7 negative", and the fixture-presence test gains the three new
  filenames. The custody packet's task 4.1 named this coupling in advance.
- [ ] 3.7 Add a test that a positive fixture carrying no authority fields
  produces a WARNING and still exits 0 — the deprecation's own proof, in both
  directions.

## 4. Documentation

- [ ] 4.1 `docs/domain-factory-starter-pack.md` § 9: the
  `credentials/bindings.template.yaml` example gains the three fields, so the
  scaffold a domain copies is the conforming one rather than the minimal one.
  **Sweep the guidance bullets beneath it in the same edit** — the list says
  bindings belong to deployments and to use references, and it must now also
  say which authority reaches them; a definition gaining a conjunct leaves
  every one-conjunct sentence beside it stale.
- [ ] 4.2 `docs/credential-access-model.md`: record that per-system authority is
  now a property of the RECORD rather than of review, and that the declaration
  is an assertion by the binding's owner which nothing here verifies against the
  store.
- [ ] 4.3 Do NOT edit `docs/lifecycle-notebook-projection.md` or any ratified
  custody text to change "access identity" to "fetch identity". The synonymy is
  declared in the requirement; a ratified record is not rewritten for a
  successor's convenience.

## 5. The contract release ritual

- [ ] 5.1 Assert the precondition before cutting: `contracts/` is untouched by
  the PROPOSAL commit series, so ratifying this packet drifts no release
  inventory. Re-verify at realization rather than trusting this line — the
  release surface moves.
- [ ] 5.2 ALLOCATE THE MINOR AT REALIZATION, BY MERGE ORDER, not before.
  `contract-v2.2` is expected; it is not reserved, because
  `add-credential-escrow-checkout` edits the same schema and owes the same
  minor. Bump `contract_bundle_version` in `contracts/manifest.yaml` and write
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
- [ ] 5.5 Assert what does NOT move: no required field is added, no shape is
  removed, no vocabulary is reinterpreted, `contract_schema_version` is
  unchanged, and a consumer pinned at the previous bundle stays conformant until
  it deliberately upgrades. State it as the four properties, not as the word
  "additive".
- [ ] 5.6 Rebuild the inventory wholesale —
  `scripts/validate-contract-release.py build --tag <tag> --output
  contracts/releases/<tag>.digests.yaml` — then `verify-commit --commit <sha>`
  green, then `verify-promotion` before tagging, then the annotated tag, then
  `verify-tag` from an INDEPENDENT clone. The tag points at the realized
  commit; a bundle is not published until its tag exists.

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
- [ ] 7.3 Revisit task 4.1's declined fixture: its stated reason ("would TRIP
  the validator") no longer holds, and 3.1 packages the example it wanted.

## 8. NOT part of this change

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
