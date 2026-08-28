# Tasks: add-credential-escrow-checkout

Governance-level and dependency-ordered. **This change is not implemented
here**: § 1 and § 2 are done at authoring, § 3 onwards belong to the realizing
sessions and repositories. Every fact quoted below was verified on 2026-08-28
in a fresh worktree off `origin/main` at `c79d6e54`; a task that cites a line
number owes a re-read at realization, not a copy of the number.

## 1. Spec delta (THIS CHANGE)

- [x] 1.1 `credential-contracts` — seven ADDED requirements, 28 scenarios:
      break-glass checkout as an administration-tier custody act; the three
      correlated records with the decrypted-object enumeration; the two-bound
      policy window; after-use rotation scoped to what was decrypted; escrow
      recipients disjoint from runtime decryption controllers; the rehearsed
      drill as the realization gate; the re-mint test.
- [x] 1.2 Verify no active change modifies a requirement this delta touches.
      Measured: `add-notebook-hosting-credential-custody` ADDs two differently
      named requirements to the same capability, and
      `add-notebook-projection-identity` MODIFIES "The credential vault operator
      is an execution binding, never contract content", which this delta does not
      touch. All seven requirement names here are unique against the promoted
      spec and both active deltas.
- [x] 1.3 Verify the delta is all-ADDED by measurement rather than by
      preference: the promoted SOPS ciphertext requirement is CITED by
      requirements 4 and 5 and re-legislated by neither, and
      `deployment-handoff-boundary` and `roles-authority-model` are consumed
      rather than modified (OD-5).
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-credential-escrow-checkout
      --strict` and `--all --strict` green.

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
      migration, and ruling A's schema surface. All named in `proposal.md`
      § Impact as the successor's.

## 3. Successor packet (`add-credential-escrow-registry`)

- [ ] 3.1 Ruling A's schema surface: the additive optional `escrow:` relationship
      block on `xfactory_credential_binding_template`, plus the escrow-entry
      record kind (inventory + restore target), shaped on the running prior art
      at `Opensoft-Tenant-openxpki-qa` `escrow/**/inventory.yaml` and
      `restore-map.yaml`.
- [ ] 3.2 Ruling C: the canonical Client Hermes home
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
- [ ] 3.6 Answer OQ1 (per-client drill obligation at install readiness) and OQ2
      (drill cadence anchored to escrow-identity rotation) if this packet's veto
      window closed without rulings on them.

## 4. Realization: openxFactory contract surface

- [ ] 4.1 Author the positive fixtures under a new `contracts/credentials/examples/`
      tree: the escrow decryption identity's requirement record, its custody
      binding, the time-boxed scope-named checkout grant template, and the
      break-glass audit policy declaring the decrypted-object enumeration among
      its `minimum_fields`.
- [ ] 4.2 Author the negative fixtures for the four named refusals: a runtime
      decryption-controller recipient reused as an escrow recipient; a checkout
      grant with no recorded human-and-domain approval; an audit policy omitting
      the enumeration; a SHOULD-escrow classification naming no retained
      authority. Each carries its expected-failure marker on the trust-anchor
      fixture pattern.
- [ ] 4.3 Confirm `scripts/validate-credential-contracts.py` accepts the positive
      fixtures and rejects the negatives, extending it only if the existing
      schema already carries the constraint; a refusal the schema cannot express
      stays a governance finding rather than becoming a schema change (that would
      reopen OD-2).
- [ ] 4.4 Register the fixtures in `contracts/manifest.yaml` as `type: fixture`
      members with `sha256` and consumption rules, on the precedent of the
      adopted deterministic fixtures at `contracts/manifest.yaml:553-600`, and
      cut the additive bundle with its `contracts/CHANGELOG.md` entry and
      verified annotated tag. `contract-v2.0` is the declared bundle; the minor
      is allocated at merge order and not reserved here.

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
- [ ] 5.4 Resolve OQ3 before the drill: extend the `thin-independent-approval`
      accepted-risk record by an explicit scope amendment covering escrow
      checkout, rather than reusing it silently — its `scope.applies_to` names
      only `cir-opensoft-qa-codexfactory-install` and `codexfactory-qa-corebackup`.
- [ ] 5.5 **RUN THE DRILL** and record it: fresh clone with no prior local state;
      the PER-CLIENT escrow identity retrieved through a real approval-and-grant
      cycle (never the operator root — requirement 5's third scenario); at least
      one escrowed object decrypted and its value verified against its declared
      restore target; the three correlated records produced; after-use rotation
      dispatched for every enumerated object; and the retroactive
      `client_infrastructure_request` opened inside 24 hours and disposed inside
      5 business days.
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

- [ ] 7.1 Clear the seven § Orchestrator decisions and rule the five § Open
      Questions, or record which stand as authored.
- [ ] 7.2 Archive gate — merge plus green PLUS the drill: § 4 and § 5 complete,
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green,
      `pytest tests/doc-health` green, the additive bundle cut and tagged, and
      the § 5.5 drill recorded. This change stays ACTIVE until then.
