## 1. Hard Spec Reconciliation

- [x] 1.1 Update canonical `canonical-policy-migration` requirements so `openxFactory` owns neutral stage/admission policy and `codexFactory` owns software Spec Kit and PR admission implementation.
- [x] 1.2 Update canonical `repo-boundary-governance` requirements so domain execution policy belongs in the owning DomainxFactory.
- [x] 1.3 Update canonical `shared-contract-ownership` requirements so shared contracts remain in `openxFactory` while domain-specific artifact schemas may live in DomainxFactories.

## 2. openxFactory Documentation Split

- [x] 2.1 Narrow `docs/roles-and-authority.md` so it contains cross-factory authority and points to DomainxFactory implementation policy instead of embedding Spec Kit mechanics.
- [x] 2.2 Narrow `docs/traceability-model.md` to a domain-neutral traceability chain and point engineering traceability to `codexFactory`.
- [x] 2.3 Verify `docs/spec-kit-stage-ownership.md`, `docs/pr-admission.md`, and `docs/workflow-contract.md` use neutral wording and point to domain implementations.

## 3. codexFactory Implementation Contracts

- [x] 3.1 Add machine-readable workflow YAML gate contracts for each existing `codexFactory/workflows/*.md` workflow.
- [x] 3.2 Add a `codexFactory` tenant example that references the software-team profile.
- [x] 3.3 Add a scaffolded `memory_gateway` block to `codexFactory/stack.yaml` that satisfies strict validation without selecting a production provider.

## 4. Memory Gateway Promotion

- [x] 4.1 Promote the completed memory-gateway requirements into canonical `openspec/specs/memory-gateway/spec.md`.
- [x] 4.2 Archive `openspec/changes/add-customer-memory-gateway-architecture` to the dated archive directory.
- [x] 4.3 Update `openxFactory/README.md` OpenSpec active, archived, and canonical spec lists.

## 5. Validation

- [x] 5.1 Run OpenSpec validation for all specs and active changes.
- [x] 5.2 Run openxFactory memory gateway validation.
- [x] 5.3 Run strict `codexFactory` domain validation and pin validation.
- [x] 5.4 Run `codexFactory` docs validation.
