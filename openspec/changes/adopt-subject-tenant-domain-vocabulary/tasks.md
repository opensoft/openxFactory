# Tasks: adopt-subject-tenant-domain-vocabulary

## 1. Vocabulary contract

- [x] 1.1 Author `contracts/policies/layer-vocabulary.yaml` (`schema_version: 1`,
      `kind: layer_vocabulary`): canonical names with one-line role
      definitions, legacy-to-canonical mapping
      (`customer → subject`, `client → tenant`, `domain → domain`), the
      frozen-identifier inventory (role kinds, `customer_subject`,
      `customer_subject_ref`, `contracts/hermes-runtime/` `$id`s), and the
      per-domain alias table (Medx patient, codex project, Ops managed
      system/tenant, Ledgerx client company, Adx brand audience).
- [x] 1.2 Register the new file per the contract versioning policy
      (contracts/README.md holding area until the allocated additive release;
      manifest digest at release).

## 2. Canon documentation

- [x] 2.1 Update `docs/terminology-and-repo-topology.md` to
      Subject/Tenant/Domain throughout, with one legacy-vocabulary note
      mapping the old names.
- [x] 2.2 Sweep remaining openxFactory `docs/` layer prose (architecture,
      avatar-first-ui-standard, memory-model docs, starter pack, checklists)
      to the canonical vocabulary; leave commercial-relationship prose
      ("client of Opensoft") untouched.
- [x] 2.3 Link this change in the README OpenSpec Records block and keep the
      doc index current.

## 3. Downstream follow-ups (filed, not executed in this change)

- [x] 3.1 File the machine-identifier migration change for the next major
      contract bundle (`customer_subject_ref → subject_ref`, role kind enums,
      schema `$id`s, migration + mapping manifest per the existing v1-to-v2
      pattern).
- [x] 3.2 File per-repo migration changes for the five DomainxFactories
      (stack.yaml keys, directory names, README prose) — this also closes the
      review §A1 Ledgerx collision and folds into fix priority #2.
- [x] 3.3 Coordinate with `installs/hermes-install`: no action while it
      consumes openxFactory by pin; adopt the vocabulary at its first pin bump
      after the Track 2 realization of
      `add-hermes-customer-subject-runtime-contract` lands.

Filing record (2026-07-23): tasks 3.1–3.3 are filed as the staging topic
`ideation/staging/layer-vocabulary-machine-migration/` (dormant by design;
rides the next major bundle). Track 2 landed + archived 2026-07-19, so 3.3
reduces to "hermes-install migrates at its pin bump onto the major" —
recorded in the topic's claims. Ledgerx prose sweep landed 2026-07-23.
