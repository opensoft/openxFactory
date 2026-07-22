# Omnigent Contract Family

Status: draft
Kind: reference
Repository context: openxFactory
Owning change: `add-omnigent-domain-overlay` (ratified 2026-07-22; active
until realization archives)

The neutral contracts for the Omnigent execution layer's domain tier —
the "core omnigent + per-domain overlay + per-tenant instantiation" split
that mirrors the Hermes install pattern. New contract family: machine
identifiers use the canonical Subject/Tenant/Domain spellings from birth
(`adopt-subject-tenant-domain-vocabulary`); legacy `customer|client`
spellings appear only inside pinned upstream artifacts and are interpreted
via the published layer-vocabulary mapping.

## Files

| File | Purpose |
|---|---|
| `omnigent-domain-overlay.schema.yaml` | Per-domain Omnigent content payload: worker classes mapped to the five neutral archetypes (`frame`/`generate`/`verify`/`challenge`/`assemble_for_admission`), the generalized six-boolean permission matrix (constitutional `execute_final_action`/`access_secrets` false), credential tiers incl. `never_assignable`, prompt packs, toolchain bindings, domain validators, preseed and lane deltas, ambiguity routing, stop conditions |
| `omnigent-install-manifest.schema.yaml` | Install manifest: Hermes runtime manifest digest-pinned as the single stack identity, exactly one domain overlay (one tenant / one domain / N subject workloads), subject-workload registry with activation state + validator mode, pre-rendered effective-profile provenance, evidence root |
| `examples/*.example.yaml` | Conforming instantiation stubs |
| `examples/fixtures/negative/*.yaml` | Rejection fixtures, one violation each, with `# expect:` markers |

## Validation

```sh
python3 scripts/validate-omnigent-contracts.py
```

Schema-checks both contracts, validates the positive examples, asserts
every negative fixture fails for its marked reason, and enforces the
cross-file invariants (credential tier disjointness, unique worker ids,
canonical-vocabulary key lint).

## Registration

Pending realization per the
[Contract Versioning Policy](../../docs/contract-versioning-policy.md):
listed in the top-level `contracts/README.md` holding area; registered in
`contracts/manifest.yaml` / `contracts/CHANGELOG.md` when the owning
change archives at its allocated additive bundle release.

Consumers: `installs/omnigent-install` (manifest + compose/verify
realization), each DomainxFactory's `omnigent/` tree (overlay authoring —
codexFactory first, MedxFactory second-domain fixture from its staged
draft).
