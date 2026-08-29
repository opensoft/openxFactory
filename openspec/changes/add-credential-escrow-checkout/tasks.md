# Tasks: add-credential-escrow-checkout

Governance-level and dependency-ordered. **This change is not implemented
here**: § 1 and § 2 are done at authoring, § 3 onwards belong to the realizing
sessions and repositories. Every fact quoted below was verified on 2026-08-28
in a fresh worktree off `origin/main` at `c79d6e54` and re-verified after
`origin/main` was merged in at the OD-2 veto; a task that cites a line number
owes a re-read at realization, not a copy of the number.

**THIS FILE CHANGED SHAPE ON 2026-08-28.** Brett vetoed OD-2 over PR #479, so
§ 4 became a SCHEMA realization rather than a fixture pass, § 3 shed the schema
work it was holding for the successor, and the five ruled open questions landed
as concrete obligations in § 3 and § 5.

## 1. Spec delta (THIS CHANGE)

- [x] 1.1 `credential-contracts` — NINE ADDED requirements and ONE MODIFIED, 46
      scenarios (38 ADDED, 8 in the MODIFIED block). Authored as seven ADDED / 28
      / no MODIFIED block; requirements 8 and 9 and the MODIFIED block were added
      at the OD-2 veto. The seven authored:
      break-glass checkout as an administration-tier custody act; the three
      correlated records with the decrypted-object enumeration; the two-bound
      policy window; after-use rotation scoped to what was decrypted; escrow
      recipients disjoint from runtime decryption controllers; the rehearsed
      drill as the realization gate; the re-mint test. Added at the veto: the
      escrow relationship on the binding template (never a custody tier), and the
      escrow entry's shape.
- [x] 1.2 Verify no active change modifies a requirement this delta touches.
      Measured at authoring: `add-notebook-hosting-credential-custody` ADDs two
      differently named requirements to the same capability, and
      `add-notebook-projection-identity` MODIFIES "The credential vault operator
      is an execution binding, never contract content", which this delta does not
      touch. All TEN requirement names here — the nine ADDED and the one MODIFIED
      — are unique against the promoted spec and both active deltas. RE-MEASURED
      after the veto: see 1.6.
- [x] 1.3 Verify the delta's shape by measurement rather than by preference. As
      authored the claim was that the delta is ALL-ADDED; the OD-2 veto made that
      false, so the claim is now the narrower and more useful one: **exactly ONE
      promoted requirement is edited, and the edit is FORCED rather than
      preferred** — a promoted requirement enumerating five record kinds is
      falsified by a sixth, so it is amended and nothing else in canon moves. The
      promoted SOPS ciphertext requirement is still CITED by requirements 4 and 5
      and re-legislated by neither, and `deployment-handoff-boundary` and
      `roles-authority-model` are still consumed rather than modified (OD-5,
      CLEARED, and unaffected by the veto because the MODIFIED block landed on
      `credential-contracts`).
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-credential-escrow-checkout
      --strict` and `--all --strict` green, before and after the veto.
- [x] 1.5 MODIFIED "Canonical credential record shapes" — five kinds become six,
      `xfactory_credential_escrow_entry` added to the enumeration, a closing
      paragraph declaring both additions additive, the two promoted scenarios
      carrying "five" amended to "six" (the only promoted words that move), and
      two scenarios added pinning the additive property. The requirement is
      reproduced WHOLE, including the `issuance_preconditions` paragraph and all
      six promoted scenarios, because a MODIFIED block replaces rather than
      patches.
- [x] 1.6 Re-collision-check after the veto, for the RECORD-SHAPES requirement
      and the BINDING TEMPLATE specifically, measured against `origin/main` as it
      stood when this branch merged it rather than against the tree the packet
      was authored on. Enumerated every non-archived change carrying a
      `specs/credential-contracts/spec.md`: there are exactly TWO besides this
      one. `add-notebook-hosting-credential-custody` is all-ADDED with two
      differently named requirements; `add-notebook-projection-identity` MODIFIES
      only "The credential vault operator is an execution binding, never contract
      content". Swept every MODIFIED requirement heading in every active change's
      deltas across the whole tree: **no other active change carries a MODIFIED
      block on "Canonical credential record shapes"**, so this delta is the sole
      editor of it. `add-trust-anchor` is ACTIVE and was checked by name because
      its OQ2 ruling is what sent escrow here: it carries deltas on `trust-anchor`
      and `repo-boundary-governance` ONLY and no `credential-contracts` delta at
      all, so its promise of no schema change there is kept in both directions. A
      tree-wide grep for `xfactory_credential_binding_template` across every
      active change's `specs/` returns NOTHING, so this delta is the only one
      touching that kind. Re-measure at realization rather than trusting these
      sentences — active changes land daily.
- [x] 1.7 Add the live-refusal element to the drill definition, per OQ5's
      ruling — the one ruling that went against this packet's own
      recommendation. Landed in requirement 6's body, in two new scenarios (a
      drill proving only the success path does not discharge the gate; a drill
      demonstrating a refusal does), in `design.md` § 6 as a fifth exercised
      element, and in § 5.5 below.

## 2. Bookkeeping and provenance (THIS CHANGE)

- [x] 2.1 `.openspec.yaml` recording the ad-hoc origin: the read-only
      decision-round mechanism, the four rulings as selected, the two voices kept
      apart, and what the citation does and does not cover.
- [x] 2.2 Repository README "OpenSpec Records" active entry.
- [x] 2.3 `ideation/staging/INDEX.md` — update the topic's row and detail section
      for a partial promotion at exit 1, per the maintenance rules at
      `INDEX.md:11-29`. The topic doc stays staged for the successor, so no file
      moves and the row is not retired.
- [x] 2.4 Record the coordination with `add-trust-anchor` (ACTIVE): its OQ2
      ruling deferred escrow here and promised no schema change there; this
      packet touches no `contracts/trust-anchor/` file.
- [x] 2.5 Record the inherited obligations this packet does NOT discharge, so
      they cannot be lost between packets — ruling C's canonical home, the
      grandfathered `Opensoft-Tenant-openxpki-qa` escrow exception and its
      migration, and the three escalation tests. All named in `proposal.md`
      § Impact as the successor's. **Ruling A's schema surface was on this list
      as authored and is NOT on it any more** — the OD-2 veto moved it into this
      packet, and the line is corrected rather than left to say the opposite of
      what § 4 now does.
- [x] 2.6 Register the MODIFIED block's carriage-ledger finding as a NAMED
      SUBJECT in `tests/doc-health/test_modified_block_currency_self_gate.py`,
      in the commit that adds the block. The family reports 3 uncarried units
      for it, and they are exactly the three occurrences of "five" the
      amendment rewrites to "six"; measured with
      `python3 scripts/doc-health.py --single-repo . --family
      modified-block-currency`. The gate compares the ledger by EXACT SET, so an
      unregistered block reds the suite by design — this is the mechanism
      working, not a test edited to pass.

## 3. Successor packet (`add-credential-escrow-registry`)

- [x] 3.1 ~~Ruling A's schema surface.~~ **MOVED TO THIS PACKET BY THE OD-2 VETO,
      2026-08-28.** See § 4. Struck rather than deleted so the successor's scope
      reads as it was drawn and as it changed.
- [ ] 3.2 Ruling C (OD-3, expressly reaffirmed when OD-2 fell): the canonical Client Hermes home
      `config/clients/<client_ref>/credentials/`; the grandfathered openxpki
      exception as a named disposition with a migration milestone, on the
      phased-never-gapped device; and the three structural escalation tests
      (readership breadth; whether the home can fall inside the client estate;
      reviewer-set enforceability), any one of which forces a dedicated registry
      repository.
- [ ] 3.3 Inventory completeness and the readiness binding: a managed
      (`opsxfactory_executed`) install is not `ready` until every MUST-escrow
      credential has an entry, with the re-mint test of requirement 7 as the
      classifier.
- [ ] 3.4 The decryption-free lint: entry structure, recipient set, no plaintext,
      and the disjointness of requirement 5 — all checkable with no decryption
      capability. **Scope the drift audit to DECLARED escrow entries**, never to
      parsed `vaultref://` strings, so it does not depend on either of the two
      incompatible grammars (`proposal.md` § Named follow-ups).
- [ ] 3.5 The repository-policy carve-out for SOPS ciphertext under the registry
      path, stated as policy rather than left as precedent.
- [ ] 3.6 Carry the RULED OQ1 and OQ2 as obligations rather than questions:
      **OQ1** — each managed client's first escrow entry owes its OWN
      per-client-recipient drill before that install is `ready` (this packet's
      single drill discharges the capability gate and the boundary milestone, not
      every client's). **OQ2** — the drill cadence is on every escrow-identity
      rotation plus at least annually, set alongside the rotation runbook because
      rotation is what it is anchored to.
- [ ] 3.7 Carry the RULED OQ4: the operator root recipient's own custody, owned
      by the successor's rotation runbook, at a floor at least as strong as the
      per-client key's — an OFFLINE copy, NOT a second password-manager item
      beside the per-client keys, since a password-manager compromise would
      otherwise take both halves of the topology at once.

## 4. Realization: openxFactory SCHEMA and contract surface

**This section was a fixture pass as authored. The OD-2 veto made it a schema
change**, and the schema edit is the cut's cause.

- [ ] 4.1 `contracts/schemas/xfactory-credential-contracts.schema.yaml` — add the
      ADDITIVE OPTIONAL `escrow:` block to `xfactory_credential_binding_template`:
      the escrow entry reference, the escrow scope, and the classification
      (`must_escrow` / `should_escrow`) with the retained authority a SHOULD must
      name. **Optional at every level** — a binding declaring no block MUST still
      validate, which is the property the MODIFIED block's added scenario pins
      and the property the additive class depends on.
- [ ] 4.2 Same schema — add the SIXTH record kind
      `xfactory_credential_escrow_entry` to the `kind` union: `source` (kind,
      owner, credential requirement reference, non-secret fingerprint only),
      `runtime_target` (provider coordinates and secret name), `escrow` (format,
      file, and encrypted FIELD NAMES), and `restore` (target plus the structural
      validations a restore must pass). Shaped on the running prior art at
      `Opensoft-Tenant-openxpki-qa` `escrow/**/inventory.yaml` and
      `restore-map.yaml` — generalize it, do not redesign it.
- [ ] 4.3 **Schema-level refusal of secret material in the entry**: the entry
      shape must make a value-carrying entry structurally invalid where it can,
      and where it cannot, the refusal is a validator check rather than prose.
      `encrypted_fields` holds NAMES; a schema that permits values there has
      built the thing the record exists to avoid.
- [ ] 4.4 `scripts/validate-credential-contracts.py` — teach it the sixth kind
      and the optional block, and confirm it still skips-with-notice any kind
      outside the now-six.
- [ ] 4.5 Author the positive fixtures under a new `contracts/credentials/examples/`
      tree: the escrow decryption identity's requirement record, its custody
      binding, the time-boxed scope-named checkout grant template, the
      break-glass audit policy declaring the decrypted-object enumeration among
      its `minimum_fields`, a binding template CARRYING an `escrow:` block, and
      an escrow entry.
- [ ] 4.6 Author the negative fixtures, now SEVEN refusals rather than four —
      the three added ones come from requirements 8 and 9: a runtime
      decryption-controller recipient reused as an escrow recipient; a checkout
      grant with no recorded human-and-domain approval; an audit policy omitting
      the enumeration; a SHOULD-escrow classification naming no retained
      authority; **an escrow discriminator added to a custody or assurance axis**;
      **an entry carrying a value or a private identity**; **an entry with no
      restore target**. Each carries its expected-failure marker on the
      trust-anchor fixture pattern.
- [ ] 4.7 Prove the additive claim rather than asserting it: revalidate every
      EXISTING credential-contract record in the family against the six-kind
      schema and confirm none is narrowed. A single pre-existing binding that
      stops validating means the change is not additive and the class is wrong.
- [ ] 4.8 Register the schema change and the fixtures in `contracts/manifest.yaml`
      (fixtures as `type: fixture` members with `sha256` and consumption rules, on
      the precedent at `contracts/manifest.yaml:553-600`; the
      `credential-contracts` entry at `:2079-2094` gains the sixth kind in its
      consumption rule) and cut the additive bundle with its
      `contracts/CHANGELOG.md` entry and verified annotated tag. **Record the cut's
      real cause in the CHANGELOG**: measured at filing,
      `contracts/schemas/xfactory-credential-contracts.schema.yaml` is NOT among
      the 192 entries of `contracts/releases/contract-v2.0.digests.yaml` (the
      closure is `contracts/hermes-runtime/contract-index.yaml` `release_member`
      entries, and it holds no credential entry), so the cut is owed by the
      VERSIONING POLICY's additive class and not by release-inventory-drift.
      Re-measure this at realization rather than trusting the sentence.
- [ ] 4.9 Run the gates a `contracts/` schema edit owes at realization —
      including the wallet gates and a release-membership re-parse — and record
      the numbers. None were owed at AUTHORING, because this packet edits no file
      under `contracts/`.

## 5. Realization: Client Hermes and the drill

- [ ] 5.1 Establish the recipient topology for the opensoft scope: a per-client
      escrow recipient and the operator root, both public halves committed, and
      verify DISJOINTNESS from every runtime decryption-controller recipient —
      including the live QA Flux reconciler recipient in
      `Omnigent-Install/.sops.yaml`, which must never appear.
- [ ] 5.2 Record the operator root's worst-case blast radius (every client scope
      it appears on) as an accepted cost, per requirement 5's fourth scenario.
- [ ] 5.3 Create `config/clients/opensoft/credentials/` in `xFactory-Hermes-Install`
      and land the four checkout records of § 4.1 instantiated for the opensoft
      scope. **This closes a live gap**: the QA install has read
      `execution_binding.mode: opsxfactory_executed` at `status: completed` since
      2026-07-20 and this directory does not exist.
- [ ] 5.4 **RULED OQ3, a hard precondition of the drill:** extend the
      `thin-independent-approval` accepted-risk record by an EXPLICIT SCOPE
      AMENDMENT covering escrow checkout, never a silent reuse — its
      `scope.applies_to` names only `cir-opensoft-qa-codexfactory-install` and
      `codexfactory-qa-corebackup`, and neither is an escrow checkout. Its honest
      effect is to make the drill's thin approval VISIBLE, not to fix it.
- [ ] 5.5 **RUN THE DRILL** and record it: fresh clone with no prior local state;
      the PER-CLIENT escrow identity retrieved through a real approval-and-grant
      cycle (never the operator root — requirement 5's third scenario); at least
      one escrowed object decrypted and its value verified against its declared
      restore target; **AT LEAST ONE LIVE REFUSAL DEMONSTRATED (RULED OQ5 — the
      one ruling that went against this packet's recommendation), the natural one
      being a checkout attempted with no recorded human-and-domain approval**; the
      three correlated records produced; after-use rotation dispatched for every
      enumerated object; and the retroactive `client_infrastructure_request`
      opened inside 24 hours and disposed inside 5 business days. **The drill
      needs Brett's hands on real material and is a LATER COMMISSION**, not this
      packet's merge.
- [ ] 5.6 On the recorded drill, set the DATED MILESTONE that removes the
      operator's standing administrative assignments, and close
      `deployment-handoff-boundary`'s named, dispositioned standing-admin
      exception. Standing access is not removed before 5.5 is recorded.

## 6. Downstream handoff (successor changes, not this surface)

- [ ] 6.1 `Omnigent-Install`: the escrow write step in its secret-handling
      runbook, executed in the SAME gated step that sets the runtime secret, and
      needing only the committed public recipient.
- [ ] 6.2 OpsxFactory: the managed-install escrow obligation in its workflow
      contracts, and the evidence-correlation audit that actually computes the
      policy window (`design.md` § Risks names this as the window's missing
      detector).
- [ ] 6.3 Classify the QA Flux deploy key SHOULD-escrow under requirement 7 and
      NAME its retained authority (operator-held GitHub organization ownership,
      per `Omnigent-Install`
      `clients/opensoft/docs/qa-subscription-migration-handoff.md:159-162`), so
      the classification is falsifiable if that ownership ever moves inside the
      client estate.
- [ ] 6.4 Cross-repo follow-up owned by neither packet: reconcile the two
      `vaultref://` grammars (`xFactory-Hermes-Install`
      `config/runtime-manifest.schema.yaml:236` versus `Omnigent-Install`
      `schemas/worker-host-manifest.schema.yaml:361`).

## 7. Ratification and archive

- [x] 7.1 **DONE 2026-08-28**: all seven § Orchestrator decisions ruled (OD-2
      VETOED; OD-4 APPROVED as authored; OD-1, OD-3, OD-5, OD-6, OD-7 CLEARED as
      authored) and all five § Open Questions answered, by a four-question
      multi-choice put to Brett over PR #479. Merge on green approved, to be
      performed by the orchestrating session.
- [ ] 7.2 Archive gate — merge plus green PLUS THE CUT PLUS the drill: § 4 and
      § 5 complete, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green,
      `pytest tests/doc-health` green, `contracts/manifest.yaml` /
      `contracts/CHANGELOG.md` / the digest inventory / a verified annotated tag
      agreeing on the new bundle, and the § 5.5 drill recorded WITH its refusal.
      This change stays ACTIVE until then.
