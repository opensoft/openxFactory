# Staged: Layer-Vocabulary Machine-Identifier Migration

Status: staged
Kind: contracts
Summary: The deferred second half of `adopt-subject-tenant-domain-vocabulary`
(ratified + realized 2026-07-23): migrate the FROZEN legacy machine
spellings (`customer_subject*`, role kinds `customer|client|domain`, schema
`$id`s, `stack.yaml` `hermes.layers` keys) to the canonical
Subject/Tenant/Domain vocabulary at the next MAJOR contract bundle, plus
the residual per-repo prose/key sweeps. Filed as the vocabulary change's
tasks 3.1–3.3 deferral artifact; intentionally dormant until a major
bundle is scheduled for other reasons — the freeze plus the published
mapping (`contracts/policies/layer-vocabulary.yaml`) is the steady state
and nothing is broken while this waits.
Topics: layer-vocabulary, subject-tenant-domain, machine-identifiers,
contract-versioning, hermes-runtime, domain-stack-schema, hermes-install
Repository context: openxFactory (contracts/hermes-runtime/,
contracts/schemas/); realizations ripple to installs/hermes-install,
installs/omnigent-install, and all five DomainxFactory stack.yaml files
Staging ID: openxFactory:staging:layer-vocabulary-machine-migration
Source: `adopt-subject-tenant-domain-vocabulary` tasks 3.1–3.3 (deferral
filed 2026-07-23); layer-vocabulary contract's frozen_identifiers
inventory.

## Target capability and delta

- MODIFIED `layer-vocabulary` (the capability lands with the vocabulary
  change's bundle registration): retire the machine-identifier freeze for
  the surfaces migrated below; the mapping table remains for archived
  artifacts.
- MODIFIED (major, breaking) `contracts/hermes-runtime/` v2 family →
  next major: `customer_subject` → `subject`, `customer_subject_ref` →
  `subject_ref`, role kinds `customer|client|domain` →
  `subject|tenant|domain`, schema `$id`/`contract_id` renames, evidence
  register + conformance test id churn; migration + mapping manifest per
  the existing v1-to-v2 pattern (frozen source snapshot, reconciliation,
  quarantine).
- MODIFIED `contracts/schemas/xfactory-domain-stack.schema.yaml` (major):
  `hermes.layers` role keys — coordinated with all five domain repos'
  `stack.yaml` files in one migration window.

## Claims

1. Nothing needs this before a major bundle exists: pinned consumers are
   byte-stable, new surfaces are canonical from birth, and prose canon is
   swept. The migration rides the next major, never causes it.
2. The blast radius is bounded and known: the frozen_identifiers inventory
   in `contracts/policies/layer-vocabulary.yaml` is the authoritative
   list; hermes-install adopts at its first pin bump onto the major
   (Track 2 landed + archived 2026-07-19, so no lane conflict remains —
   the former task-3.3 coordination is simply "migrate at pin bump").
3. Per-repo residue after the 2026-07-23 sweeps: Ledgerx prose done
   (Engagement/Firm); codexFactory + MedxFactory canonical on all new
   surfaces (their overlays/specs); OpsxFactory prose partially legacy;
   AdxFactory fully pending (phantom middle layer, `pending_migration`
   aliases in the vocabulary contract). Ops/Adx prose sweeps can run
   before the major, key migrations only with it.

## Open questions

- Does the hermes-runtime major fold this in with other v3 drivers
  (deferred worker-host mutation verbs? federation?) or ship standalone?
- Do the `$id` URL renames keep server-side redirects/aliases for archived
  release digest inventories?

## Deferral with a named gate (recorded 2026-08-28)

**DEFERRED. The gate is the next hermes-runtime MAJOR, and it has not
fired.** The claim below — the migration RIDES a major and never causes one
— is the whole reason this topic cannot be scheduled on its own, and it was
tested in the month just past.

**`contract-v2.0` fired on 2026-08-27 WITHOUT this migration, and correctly
so.** The tag is a BREAKING bundle major, but its breakage is the openxWallet
split (the eight wallet artifacts leaving the bundle for
`opensoft/openXwallet`, realizing `split-openxwallet-repo` P3, preceded by
the deprecating minor `contract-v1.47`). Measured rather than assumed:
`git diff --stat contract-v1.47 contract-v2.0 -- contracts/hermes-runtime/
contracts/schemas/` reports NO files changed, so the major moved no
hermes-runtime schema and no v1 schema field, and there was nothing for the
frozen spellings to ride. The frozen inventory in
`contracts/policies/layer-vocabulary.yaml` is unchanged: the
`customer|client|domain` role kinds, `customer_subject`/`customer_subject_ref`,
the v2-family `$id`/`contract_id` values, the `hermes.layers` role keys, and
the released v1 field names all still stand.

(Recorded date corrected against the tree: the commission relayed this as
"contract-v2.0 fired 2026-08-28"; the tag and its commit both date
2026-08-27. The substance — that it fired without the migration — is
confirmed.)

**GATE: hermes-runtime v3 / domain-stack schema v2.** Nothing schedules that
major today. Prose sweeps in Ops/Adx may run before it; key migrations may
not.

**This deferral is a schedule, not a standing.** It changes no `Status:`,
and it does NOT stop the topic ageing in doc-health: there is no `deferred`
state for a staged topic and this change deliberately adds none.

## Exit

One openxFactory OpenSpec change per surface family at the scheduled major
(hermes-runtime v3; domain-stack schema v2), plus a mechanical per-repo
stack.yaml migration change in each DomainxFactory; archives when every
frozen identifier in the inventory is migrated or explicitly retained as
an archived-artifact-only spelling.
