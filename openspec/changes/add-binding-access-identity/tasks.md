# Tasks: add-binding-access-identity

Status: draft

NOTHING BELOW §2 RUNS BEFORE RATIFICATION. This change's own diff is the spec
delta and these records; §1 and §2 are what the authoring commit contains, §3
onward is realization that the ratification AUTHORIZES and does not perform.

**No task here creates, reads, moves or names a live secret.** Both new fields
name PRINCIPALS, the fixtures are neutral, and the one live estate act this line
of work implies — placing an operated identity's credential into a vault — was
already routed to an operator by `add-notebook-hosting-credential-custody`
tasks §4.4 and is not re-scheduled here.

## 1. Spec delta (THIS CHANGE)

- [x] 1.1 THREE ADDED requirements on `credential-contracts`, twelve scenarios,
      no requirement MODIFIED: the access-identity declaration, the discriminated
      shared-reference refusal, and the core rule reaching the new fields.
- [x] 1.2 NO `## MODIFIED Requirements` BLOCK, and the reason is stated at the
      top of the delta file rather than left to be inferred:
      `add-credential-escrow-checkout` holds a live MODIFIED block on
      `Canonical credential record shapes`
      (`openspec/changes/add-credential-escrow-checkout/specs/credential-contracts/spec.md:5`),
      and the custody ratification's stated discipline is that two active changes
      never hold two live deltas on one requirement text
      (`review/ratification-2026-08-23.md:46-48`).
- [x] 1.3 Consequence of 1.2, recorded rather than assumed: this packet is NOT a
      subject of the `modified-block-currency` carriage ledger, because it
      carries no MODIFIED block. It therefore does NOT edit
      `tests/doc-health/test_modified_block_currency_self_gate.py` — the sibling
      packet had to, and the difference is exactly that it carries a block and
      this one does not. If §2.3 ever moves a MODIFIED block into this packet,
      that registration rides with it IN THE SAME COMMIT.

## 2. Bookkeeping and provenance (THIS CHANGE)

- [x] 2.1 `.openspec.yaml` with the durable origin. `kind: ad_hoc`; the approval
      act is Brett Heap's 2026-08-23 ratification of
      `add-notebook-hosting-credential-custody`, whose Decision item 3 names this
      successor. NO staging origin is claimed: searched `ideation/staging/` and
      its `INDEX.md`, no topic covers the binding shape or the access-identity
      gap, and `kind: staged` would claim a source that cannot resolve.
- [x] 2.2 README "OpenSpec Records" — add this change to the active list.
- [ ] 2.3 **THE OWED SHAPE-OWNERSHIP SENTENCE, and the sequencing that discharges
      it.** `Canonical credential record shapes` names what the schema owns.
      After both this packet and `add-credential-escrow-checkout` archive, that
      requirement must name the two new optional fields alongside the sixth kind
      and the `escrow:` block. WHICHEVER OF THE TWO ARCHIVES SECOND CARRIES THE
      MODIFIED BLOCK, and it must be SCENARIO-COMPLETE against canon AS IT THEN
      STANDS — restating every scenario the requirement holds at that moment,
      including the ones the first packet's promotion added. This is written as a
      task and not as an assumption because the silent-scenario-loss class
      (#329/#330) is precisely what an unwritten sequencing obligation produces.
- [ ] 2.4 If this packet archives FIRST, re-read
      `add-credential-escrow-checkout`'s MODIFIED block before ITS archive:
      canon will have moved under it, which is the `modified-block-currency`
      family's whole subject.

## 3. Realization: the schema and the validator

- [ ] 3.1 `contracts/schemas/xfactory-credential-contracts.schema.yaml`: add
      `access_identity` and `operated_identity` as OPTIONAL string properties on
      the `credential_bindings` `additionalProperties` object of
      `xfactory_credential_binding_template` (currently `:135-146`,
      `required: [provider, secret_ref, owner, rotation_policy]` with optional
      `vault`). `required` is UNCHANGED. Assert by revalidating the existing
      packaged positives untouched.
- [ ] 3.2 `scripts/validate-credential-contracts.py`: replace the
      `shared-secret-identity` single-fact refusal (`:115-129`) with the
      three-fact conjunction. Group bindings by `secret_ref`; for each group of
      size > 1, the group is LICIT only when every member declares the SAME
      non-empty `operated_identity` AND the members' `access_identity` values are
      all present and pairwise distinct. Otherwise the finding fires. Keep the
      EXISTING finding code and the existing message for the undeclared case so
      a pre-extension repository's output is byte-identical; use distinct message
      text for the two new sub-cases so a reader can tell which conjunct failed.
- [ ] 3.3 Extend `baked-secret` to the two new fields: `_looks_like_raw_secret`
      already exists (`:60-62`) and today is applied to `secret_ref` only.
- [ ] 3.4 Packaged fixtures under `examples/credential-contracts/`. ONE positive:
      the two-consumer template that could not be shipped when the operated-
      identity requirement landed — one `secret_ref`, one declared
      `operated_identity`, two distinct `access_identity` values. FOUR negatives,
      registered in `NEGATIVE_EXPECTATIONS` (`:42-48`): shared reference with no
      operated identity declared (must keep raising the EXISTING code — this is
      the regression probe for 3.2, not a new case); shared reference declared by
      only one member; same operated identity with one shared access identity;
      credential material in an `access_identity`.
- [ ] 3.5 `tests/credential_contracts/test_dispatch_credential_contract.py:35`
      asserts `"self-test: 3 positive + 5 negative example(s) confirmed"`. It
      moves to 4 + 9 IN THE SAME COMMIT as 3.4 — the custody change's task 4.1
      named this consequence in advance and it is not discovered here.
- [ ] 3.6 Add a test that a binding template carrying NEITHER new field validates
      and raises nothing, and that the existing
      `negative/dispatch-reuses-content-secret.yaml` still raises
      `shared-secret-identity`. THE SECOND IS THE ONE THAT MATTERS: it is the
      executable form of the claim that the discrimination refines the check
      rather than regressing it.

## 4. Realization: the contract-release ritual

- [ ] 4.1 The ritual is OWED and task 4.5 of the custody change named every step:
      CHANGELOG allocation, manifest digest, `contract_bundle_version` bump,
      inventory rebuild, verify-commit, tag.
- [ ] 4.2 ALLOCATE THE NUMBER AT REALIZATION, by merge order, per
      `docs/contract-versioning-policy.md`. Do NOT reuse the stale `contract-v1.45`
      designation this successor was queued under: it was cut 2026-08-26 by
      `add-doxchat-model-intake` and the declared bundle is now `contract-v2.1`
      (`contracts/manifest.yaml:3`). Re-parse the CHANGELOG and
      `contracts/releases/` at the cut — `add-credential-escrow-checkout` is
      spending an additive minor against the same schema file in parallel.
- [ ] 4.3 `contracts/manifest.yaml` `credential-contracts` row (`:2079-2084`):
      new `sha256`, and the `consumption_rule` records the growth in the same
      voice as its existing `issuance_preconditions` paragraph.
- [ ] 4.4 CHANGELOG entry stating the ADDITIVE class and the three compatibility
      facts explicitly: `required` unchanged, `contract_schema_version` unchanged,
      and every new refusal reachable only through a field no earlier record
      could carry.
- [ ] 4.5 Re-verify at the cut whether the schema is a release-inventory member.
      Measured 2026-08-29 by parse: it is NOT — the membership closure is built
      from `contracts/hermes-runtime/contract-index.yaml` `release_member`
      entries and carries no credential entry. So `release-inventory-drift` will
      NOT force this cut and the versioning policy does. If that membership has
      changed by the cut, the forcing reason changes with it and the CHANGELOG
      must say which one applied.

## 5. Documentation

- [ ] 5.1 `docs/credential-access-model.md` owns the semantic invariants
      (`contracts/manifest.yaml:2088`, and the doc says so at its own
      "Record shapes" note). Record the two fields and the discriminated refusal
      there, including the honest limit: the record carries the CLAIM of separate
      authority; the store carries the fact.
- [ ] 5.2 Do NOT restate the invariant in `docs/domain-factory-starter-pack.md`
      or the implementation checklist beyond a pointer — three copies of a
      semantic rule is the contract-copy-drift family's subject.

## 6. Validate green

- [ ] 6.1 `OPENSPEC_TELEMETRY=0 openspec validate add-binding-access-identity
      --strict` and `--all --strict`.
- [ ] 6.2 `python3 scripts/validate-credential-contracts.py .` clean, with the
      new self-test counts confirmed in its own output line.
- [ ] 6.3 `pytest tests/credential_contracts tests/doc-health`.
- [ ] 6.4 doc-health zero-new against a fresh same-clock `origin/main` baseline
      whose worktree BASENAME MATCHES this clone's (issue #342: report identity
      is `(family, repo, path)` with the repo read from the basename, so a
      mismatched baseline manufactures phantom regressions).
- [ ] 6.5 `verify-commit` green at the cut commit, and the tag verified from an
      independent clone.

## 7. Ratification and archive

- [ ] 7.1 **COUNCIL REVIEW PRECEDES RATIFICATION.** This packet is the first
      subject of the §7.4-shaped council-reviewed-but-human-approved path, the
      continuation of the 2026-08-28 gate-rules ruling. The council read happens
      OUTSIDE the pipeline, on the 2026-08-28 procedure.
- [ ] 7.2 **Brett Heap's approve is the merge act and the ratification act.**
      Until it happens this packet is `Status: draft` and carries no ratification
      citation — the promoted lifecycle rule requires one only for
      `Status: ratified`.
- [ ] 7.3 On ratification, write `review/ratification-<date>.md` in the house
      shape (Ratifier, Ratified baseline naming the exact files and requirement
      counts, the flagged items that were in view) and set `Status: ratified` +
      `Ratified:` on proposal, design and tasks.
- [ ] 7.4 Archive on merged + green realization evidence per
      `release-realization`, which for a code surface means the cut and its
      verified tag, not the proposal's merge.
- [ ] 7.5 At archive, tick `add-notebook-hosting-credential-custody` tasks §4.5
      and §4.1 as DISCHARGED BY THIS CHANGE, naming it. An owed successor that
      lands without closing the record that owed it leaves the obligation
      readable as still open.
