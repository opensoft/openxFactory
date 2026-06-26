## Context

`openWorkflow` now owns repo-boundary governance and shared contract ownership.
The dogfood content migration plan defines the next phase: migrate canonical
policy, contracts, and reference examples from install/proof repos into
`openWorkflow` using the factory workflow itself.

The largest source repo is `opensoft/Omnigent-Install`, which still contains
cross-factory policy material, proof examples, schemas, policies, and local
implementation harnesses. `FarHeap/Hermes-Install` contains Hermes install and
runtime notes plus some governance and group semantics. The migration must
preserve working proof harnesses and avoid mixing policy migration with runtime
or generated-state movement.

## Goals / Non-Goals

**Goals:**

- Create an OpenSpec-governed migration.
- Move or summarize canonical policy into `openWorkflow`.
- Move shared contracts into `openWorkflow/contracts`.
- Decide where reference examples and proof harnesses belong.
- Mark install repo copies as implementation notes or legacy only after
  canonical replacements exist.
- Preserve traceability and merge readiness evidence for every slice.

**Non-Goals:**

- Do not delete source docs in the same PR that creates canonical docs.
- Do not move runtime code as part of policy migration.
- Do not move generated state, credentials, databases, or local workspaces.
- Do not change submodule pointers during content migration PRs.
- Do not resolve Hermes remote ownership unless a separate feature is approved.

## Decisions

### Decision: Use OpenSpec as the controlling record

All migration work will be tracked in `migrate-canonical-policy-to-openworkflow`.
This keeps the migration governed by the same process it is defining.

Alternative considered: direct cleanup PRs. Direct cleanup would be faster, but
would skip the dogfood test and weaken traceability.

### Decision: Migrate in small feature slices

The migration will use FEAT-MIG-001 through FEAT-MIG-008 from the dogfood plan.
Each feature has a source inventory, acceptance criteria, validation, branch
review, PR admission, and merge readiness report.

Alternative considered: one large migration PR. That would be hard to review,
risky to revert, and likely to mix canonical policy with implementation details.

### Decision: Copy-first, then mark source copies

Canonical material is copied or summarized into `openWorkflow` first. Source
docs remain until a later feature marks them implementation notes, legacy
copies, or operational runbooks.

Alternative considered: move/rename source files directly. That could break
links, proof harnesses, and install repo context.

## Risks / Trade-offs

- Policy duplication persists temporarily -> Mark `openWorkflow` canonical and
  follow with install repo link updates.
- Source material is misclassified -> Require source inventory and acceptance
  evidence per feature.
- Proof harness breaks -> Do not move proof harnesses until replacement
  validation exists.
- Contract migration breaks adapters -> Split contract copies from generated
  adapter changes.
- Scope creep -> Stop if a feature combines content migration with deletion,
  runtime changes, or submodule pointer changes.

## Migration Plan

1. Create this OpenSpec change.
2. Implement FEAT-MIG-001 roles and authority as the first slice.
3. Continue with stage ownership, PR/merge policy, decomposition/traceability,
   contracts, reference examples, install repo marking, and cleanup decisions.
4. Validate each slice independently and merge through GitHub PRs.
5. Archive the OpenSpec change only after all approved slices are complete.

## Open Questions

- Should proof harnesses eventually move to `openWorkflow/examples` or a
  separate `factory-lab` repo?
- Which contract files need strict schema validation beyond markdown/YAML
  syntax checks?
- Which install repo policy copies should be kept permanently as operational
  context rather than removed?
