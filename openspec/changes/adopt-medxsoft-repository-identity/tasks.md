# Tasks: adopt-medxsoft-repository-identity

**NOTHING IN THIS FILE IS PERFORMED BY THE PROPOSAL.** Every rename below is
implementation work for a later apply step. The proposal declares the identity
and the disposition; the tasks execute them.

## 1. The transfer mapping contract

- [ ] 1.1 Author `contracts/policies/repository-identity.yaml`, sibling of
      `contracts/policies/layer-vocabulary.yaml`: `schema_version: 1`,
      `kind: repository_identity`, `policy_id: repository-identity-v1`, a
      header naming this change as the ratifying change, and a `transfers:`
      list carrying both 2026-08-26 moves —
      `opensoft/MedxFactory -> MedxSoft/MedxFactory` and
      `opensoft/MedxEHR -> MedxSoft/MedxEHR` — each with `former`, `current`,
      `transferred_on: 2026-08-26`, and a `redirect` note stating that the
      provider redirect lapses if `opensoft` reuses the name.
- [ ] 1.2 Record in the same file that a transfer moves the OWNER segment only:
      bare repository names, commits, repository-relative paths and blob
      digests are unchanged by a transfer, so surfaces carrying those are not
      edited.
- [ ] 1.3 Register the file in `contracts/manifest.yaml` — `type: policy`,
      `schema_version: 1`, per-file `sha256`, `adapter_owner: openxFactory`,
      `compatibility: canonical_openxfactory_contract`, and a
      `consumption_rule` stating that a former identity is READ through this
      mapping and that an immutable or dated record is never respelled to match
      it. Mirror `layer-vocabulary`'s entry shape exactly.

## 2. Rename the live normative contract surfaces

Do 2.1 and 2.2 in ONE commit: the test pins the fixture row-for-row and in
document order, so a split commit is red by construction.

- [ ] 2.1 `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`:
      respell the `repository:` of the medx entry to `MedxSoft/MedxFactory`
      **and move that entry to the head of `entries`** — the list is bytewise
      sorted by repository and `M` (0x4D) sorts before `o` (0x6F). Leave
      `commit`, `stack_path`, `stack_digest`, `domain_id`,
      `expected_contract_ref`, `expected_contract_schema_version` and
      `expected_result` byte-identical: the repository content did not move.
      Leave the `opensoft/LegalxFactory` exclusion row untouched.
- [ ] 2.2 `tests/hermes_runtime_contracts/test_domain_regression.py`: respell
      and REORDER `PINNED_TABLE` to match, keeping its "bytewise sorted by
      repository" comment true. Confirm
      `test_realized_inventory_matches_the_pinned_table_value_for_value`
      (line 238, which `zip`s the table against `entries` in document order)
      and its `sorted(..., key=lambda value: value.encode("utf-8"))` assertion
      at line 259 both pass.
- [ ] 2.3 Respell the medx `repository:` in the three negative fixtures
      `contracts/hermes-runtime/fixtures/regression/digest-mismatch.yaml`,
      `duplicate-repository.yaml`, and `missing-exclusion-reason.yaml`. Verify
      each still produces EXACTLY the finding it exists to produce — the
      deliberate duplicate in `duplicate-repository.yaml` is
      `opensoft/AdxFactory` and must stay the reported one.
- [ ] 2.4 `contracts/hermes-runtime/README.md` (~line 126): respell the
      denominator enumeration and put the name in its new sorted position in
      the prose list, so README order and fixture order agree.
- [ ] 2.5 `contracts/omnigent/examples/fixtures/negative/manifest-dual-domain-overlay.yaml`
      (~line 18): respell `repository:`. Confirm the fixture still fails for
      the dual-domain-overlay reason and for no other.
- [ ] 2.6 `examples/installation/domain-overlay-examples.yaml` (~line 8):
      respell `domain_factory_repo:`.

## 3. Rename the live documents

- [ ] 3.1 `docs/architecture.md` (~line 24) — the DomainxFactory enumeration.
- [ ] 3.2 `docs/workflow-contract.md` (~line 111).
- [ ] 3.3 `docs/terminology-and-repo-topology.md` (~line 208).
- [ ] 3.4 `docs/omnigent-constitution.md` (~line 45).
- [ ] 3.5 `docs/contract-versioning-policy.md` (~line 230) — the
      supported-domain regression denominator enumeration. Keep the enumeration
      order consistent with the re-sorted fixture.
- [ ] 3.6 `docs/xfactory-domain-factory-model.md` — FIVE occurrences (~297,
      ~872, ~874, ~908, ~1479), including the
      `https://github.com/opensoft/MedxFactory` URL and the
      `stack_repo: github.com/opensoft/MedxFactory` line.
- [ ] 3.7 `README.md` — TWO occurrences (~222, ~289).
- [ ] 3.8 Add a one-line note to `docs/terminology-and-repo-topology.md`
      pointing at `contracts/policies/repository-identity.yaml` as the resolver
      for former identities, so the freeze rule is discoverable from the
      topology document rather than only from this packet.

## 4. Verify the freeze — the surfaces that MUST NOT move

- [ ] 4.1 Assert, with a diff rather than by inspection, that these ten
      occurrences across eight files are byte-unchanged after tasks 2 and 3:
      `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/evidence/provider-verification.yaml:118`
      and `.../evidence/legacy-source-path-consumer-audit.md:67`;
      `docs/decisions/0002-xfactory-aggregation-repo.md:86`;
      `specs/005-customer-subject-runtime/research.md:217`,
      `specs/005-customer-subject-runtime/contracts/release-and-consumer-pin.md:64`,
      `specs/005-customer-subject-runtime/us4-provider-handoff/shared-interface-contract.md:111`;
      `scripts/ideation_dashboard/session_pr.py:209`; and
      `tests/ideation-dashboard/test_session_confinement.py` (3 occurrences).
- [ ] 4.2 Confirm the arithmetic closes: 30 occurrences across 23 files before,
      20 renamed across 15 files, 10 frozen across 8 files, 0 remaining live
      occurrences of `opensoft/MedxFactory` outside the frozen set.
- [ ] 4.3 Confirm no BARE `MedxEHR` or `MedxFactory` member name was edited —
      `--aggregate-members MedxFactory,openChart,MedxEHR,HealthLinc` in the
      doc-health workflow, the `medx-clinical` dashboard grouping, and their
      tests are correct before and after, a transfer moving only the owner.

## 5. Cut the contract bundle

- [ ] 5.1 Run `python3 -m pytest tests/hermes_runtime_contracts` and
      `scripts/validate-hermes-runtime-contracts.py` green on the renamed tree
      BEFORE touching any release surface.
- [ ] 5.2 Follow `docs/contract-versioning-policy.md` § Bundle Realization
      Order: rebase onto the final integration point, recheck availability, and
      allocate the next available additive minor after `contract-v2.0` THEN —
      no number is reserved by this packet.
- [ ] 5.3 In one atomic candidate commit: `contracts/manifest.yaml`
      (`contract_bundle_version` plus the new policy entry from 1.3),
      `contracts/CHANGELOG.md` (one entry naming the transfer, the six moved
      members, the new policy, and the `--domain-repo` key migration note), and
      the realized `contracts/releases/<bundle-tag>.digests.yaml` built by
      `scripts/validate-contract-release.py build --tag <tag>`. **Never
      hand-edit an existing inventory to make a comparison pass.**
- [ ] 5.4 `scripts/validate-contract-release.py verify-commit --commit <sha>`
      clean at the candidate; `verify-promotion` before tagging; publish the
      annotated tag at the exact published commit and `verify-tag` from a fresh
      checkout.
- [ ] 5.5 Re-run doc-health and record `release-inventory-drift` at **0
      findings** after the cut. Record the transient too: between task 2 and
      task 5.3 the family reports six `ERROR` findings (the six non-editorial
      members), which is the family working and is the reason the cut is
      sequenced inside this change.

## 6. Corpus bookkeeping

- [ ] 6.1 Add the one-line active-change entry to the README "OpenSpec Records"
      block (done in the proposing commit) and keep the README doc index
      current for `contracts/policies/repository-identity.yaml`.
- [ ] 6.2 `OPENSPEC_TELEMETRY=0 openspec validate adopt-medxsoft-repository-identity --strict`
      and `--all --strict` green.
- [ ] 6.3 Run `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply`
      after the doc changes land, per the projection workflow.

## 7. Named follow-ons — NOT performed here

- [ ] 7.1 `installs/hermes-install`
      `config/negative/duplicate-domain-layer.manifest.yaml` names the old
      owner. That repository consumes openxFactory BY PIN and is untouched
      until its next pin bump; a separate act in that repository, on the same
      disposition `adopt-subject-tenant-domain-vocabulary` gave it in 2026-07.
- [ ] 7.2 Whether a deterministic check family should verify that no live
      surface names a mapped former identity. The mapping published by task 1
      is the input such a family needs; building it here would be a second
      change riding a first.
