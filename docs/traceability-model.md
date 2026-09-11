# Traceability Model

Status: draft

The factory must document traceability from approved intent through the final
admission, enforcement, and archive state. This document defines the
domain-neutral chain. DomainxFactory repos define their domain-specific
artifact names and evidence packets.

## Source Provenance

Reviewed sources:

- `docs/workflow-contract.md`
- `docs/feature-decomposition.md`
- `docs/pr-admission.md`
- `docs/merge-council.md`
- `openspec/specs/repo-boundary-governance/spec.md`
- `openspec/specs/shared-contract-ownership/spec.md`
- `codeXfactory/codexFactory/docs/feature-decomposition-traceability.md`

## Neutral Trace Chain

```text
approved intent
  -> decomposition approval
  -> bounded domain work unit
  -> domain execution artifact
  -> validation evidence
  -> domain review record
  -> admission decision
  -> external enforcement record, where applicable
  -> archive record
```

Domain examples:

```text
codexFactory
  bounded domain work unit = engineering feature
  domain execution artifact = Spec Kit artifacts, implementation diff, checks
  external enforcement record = GitHub PR, review action, merge commit

MedxFactory
  bounded domain work unit = clinical issue or hypothesis
  domain execution artifact = simulation, specialist review, reliability packet
  external enforcement record = clinician-facing review package
```

## Suggested Coordination Artifacts

Factory coordination artifacts should live separately from domain runtime data:

```text
.factory/
  intent.yaml
  work-units.yaml
  dependency-graph.yaml
  traceability.json
  admissions/
  reviews/
  enforcement/
  archive/
```

DomainxFactory repos may add their own artifact folders for implementation
evidence, but those artifacts must retain upstream `openxFactory` scope and gate
references.

## Work Unit Handoff Shape

Domain execution should receive a Hermes-approved and xFactory-gated work unit
contract before agents run.

```yaml
work_unit_id: WORK-0001
approved_by: hermes
approval_id: hermes-admission-2026-07-08-001
domain_factory: codexFactory
target_system: github.com/example/product
approved_scope_refs:
  - openxfactory://scope/SCOPE-001
scope:
  must:
    - Execute only the approved work unit behavior.
  must_not:
    - Expand scope without a new Hermes approval.
acceptance_refs:
  - openxfactory://acceptance/AC-001
```

## Minimum Traceability Fields

```yaml
intent_id:
approval_id:
domain_factory:
work_unit_id:
domain_execution_ref:
validation_evidence:
review_record:
admission_decision:
enforcement_ref:
archive_ref:
```

## Traceability Edge Contract

Traceability edges should be machine-readable and durable. At minimum, an edge
records:

```yaml
traceability_edge:
  from_type:
  from_id:
  relation:
  to_type:
  to_id:
  evidence:
    artifact_id:
    path:
```

Core relations:

| Relation | Meaning |
|---|---|
| `decomposes_to` | intent or phase decomposes to a bounded work unit |
| `approves` | Hermes or governance approval allows a gate transition |
| `produces` | job, worker, or agent produces an artifact |
| `implements` | domain execution artifact implements an accepted work unit |
| `verifies` | validation evidence verifies acceptance criteria |
| `reviews` | domain review record reviews evidence before admission |
| `admits` | governance or admission layer approves the next state |
| `enforces` | external enforcement system applies final state |
| `blocks` | finding or decision blocks progression |
| `must_precede` | one work unit must complete before another |
| `references` | artifact links to another artifact without ownership |

Required neutral edges:

```text
approved intent -> bounded domain work unit
decomposition approval -> work-unit packet
work unit -> domain execution artifact
domain execution artifact -> validation evidence
validation evidence -> review record
review record -> admission decision
admission decision -> external enforcement record, where applicable
final state -> archive record
```

## Traceability Report

Every work unit should have a traceability report that connects approved intent
to domain execution and final state evidence.

```markdown
# Work Unit Traceability Report

Work Unit: WORK-0001
Domain Factory: codexFactory
Approved Scope: openxfactory://scope/SCOPE-001

## Source Intent

- Intent: INTENT-001
- Approval: HA-2026-07-08-001
- Acceptance refs: openxfactory://acceptance/AC-001

## Domain Execution Evidence

- Domain artifact: domain-specific path or URI
- Validation evidence: .factory/admissions/WORK-0001/checks.md
- Review record: .factory/reviews/WORK-0001/review.md

## Admission And Enforcement

- Admission decision: .factory/admissions/WORK-0001/result.yaml
- Enforcement record: domain-specific path or URI

## Final State

Decision: READY
Archive: .factory/archive/WORK-0001/
```

## Acceptance Criteria Evidence Rules

Acceptance criteria should be tracked individually. A work unit is not traceable
if it only has a general statement such as "validated" or "reviewed."

Each acceptance criterion should include:

- criterion ID
- source artifact
- domain execution evidence
- validation evidence
- reviewer evidence, when applicable
- status
- notes

Allowed statuses:

```text
covered
partially_covered
not_covered
not_applicable
deferred
```

## Domain-Specific Traceability

Engineering-specific traceability lives in:

```text
codeXfactory/codexFactory/docs/feature-decomposition-traceability.md
codeXfactory/codexFactory/docs/pr-admission-merge-readiness.md
```

Those docs specialize this neutral model with engineering features, Spec Kit
artifacts, implementation branches, deterministic checks, GitHub PRs, merge
readiness packets, and merge commits.
