# Staged: Credential Contracts Neutralization (DTN-004)

Status: staged
Kind: architecture
Repository context: openxFactory
Source: [Domain Neutralization Candidate Register](../../../docs/domain-neutralization-candidate-register.md)
entry DTN-004 (`split`, P1).
Target capability: new `credential-contracts` (delta: ADDED).
Evidence: OpsxFactory `credentials/` — the five record kinds already carry
neutral `xfactory_*` names (broker contract, runtime capability grant,
binding, requirements, audit policy); openxFactory
`docs/credential-access-model.md` owns the semantic invariants. Note:
LedgerxFactory once carried a parallel tree but was slimmed 2026-07-02;
Ops is the sole origin today.

## Claims

1. One canonical schema (`xfactory-credential-contracts.schema.yaml`,
   discriminated by kind) covers the five record kinds; domain content —
   credential families, scopes, providers, workflow/action names — stays
   domain-local.
2. The three Ops policy kinds (approval/revocation/rotation) are OUT of
   scope: skipped-with-notice, a future register candidate.
3. Semantic invariants (no raw secrets, short-lived scoped grants, audit,
   revocation) remain owned by docs/credential-access-model.md; the schema
   constrains shape only.
4. Neutrality test: all five Ops contract files validate unchanged.
5. Provenance: OpsxFactory declares `promoted_from` (DTN-004).

## Exit

Satisfied by
[promote-credential-contracts](../../../openspec/changes/archive/2026-07-09-promote-credential-contracts/proposal.md)
(2026-07-09). Register DTN-004: `adopted`.
