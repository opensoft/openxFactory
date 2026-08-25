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
| `omnigent-domain-overlay.schema.yaml` | Per-domain Omnigent content payload: worker classes mapped to the five neutral archetypes (`frame`/`generate`/`verify`/`challenge`/`assemble_for_admission`), the generalized six-boolean permission matrix (constitutional `execute_final_action`/`access_secrets` false), credential tiers incl. `never_assignable`, prompt packs, toolchain bindings, domain validators, preseed and lane deltas, ambiguity routing, stop conditions, and the optional per-worker `semantic_context` declaration (`add-omnigent-semantic-wiring`): profile identity only — the worker-scoped `xfactory_semantic_context_profile` lives inventoried in the domain's own ontology package, digests ride compiled contexts, and the declaration carries no permission field |
| `omnigent-install-manifest.schema.yaml` | Install manifest: Hermes runtime manifest digest-pinned as the single stack identity, exactly one domain overlay (one tenant / one domain / N subject workloads), subject-workload registry with activation state + validator mode, pre-rendered effective-profile provenance, evidence root, and the optional `semantic_contexts` section: exact kernel + domain ontology pins with one compiled `xfactory_semantic_context` artifact per declaring worker (both-direction completeness and per-artifact pin/digest/scope agreement enforced by the canonical wiring checks) |
| `examples/*.example.yaml` | Conforming instantiation stubs |
| `examples/fixtures/negative/*.yaml` | Rejection fixtures, one violation each, with `# expect:` markers |

## Validation

```sh
python3 scripts/validate-omnigent-contracts.py                    # family suite
python3 scripts/validate-omnigent-contracts.py <domain-repo>      # repo mode
python3 scripts/test-omnigent-semantic-wiring.py                  # wiring suite
```

Schema-checks both contracts, validates the positive examples, asserts
every negative fixture fails for its marked reason, and enforces the
cross-file invariants (credential tier disjointness, unique worker ids,
canonical-vocabulary key lint, crystallized-executor authority
conservation, unique rung-ceiling categories, unique semantic-context
worker classes). Repo mode validates a DomainxFactory's
`omnigent/domain-overlay.yaml` and resolves every worker
`semantic_context` declaration against the repo's
`hermes/domain/ontology/` package (inventoried profile, declared
package_id, worker_scope archetype-or-class agreement — unresolved or
mismatched declarations fail). The wiring suite proves the install-side
checks over constructed trees with a REAL compiled artifact: declaring
worker without a pinned context, unclaimed entries, digest/pin/scope
disagreements, drifted-bytes compile refusal (F20), and transitive
truncation itemization (F19).

## Registration

Registered in `contracts/manifest.yaml` / `contracts/CHANGELOG.md` since
contract-v1.16 (family), refreshed at contract-v1.20
(crystallized-executor binding + rung ceilings) and contract-v1.23
(semantic wiring), per the
[Contract Versioning Policy](../../docs/contract-versioning-policy.md).

Consumers: each DomainxFactory's `omnigent/` tree (overlay authoring —
codexFactory conforms; MedxFactory conforms AND wires worker semantic
contexts: two inventoried profiles + declarations on
`data_reverification_agent` and `case_framing_agent`); Omnigent install
repositories consume overlays by digest pin and, when their pinned
overlay declares semantic context, pin the compiled per-worker artifacts
through the manifest's `semantic_contexts` section.
