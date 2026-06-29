# Domain Factory Implementation Checklist

Status: shared xFactory standard  
Repository context: openxFactory  
Purpose: define how to generate, specialize, validate, and operate a domain
factory without blurring what belongs in the parent `openxFactory` contract and
what belongs in a domain stack.

## 1. Scope

This checklist applies to every xFactory domain stack, including:

- `openCodexFactory`
- `MedxFactory`
- `LedgerxFactory`
- `AdxFactory`
- future domain factories

A domain factory is implementation-ready when a new implementer can create a
tenant, model a customer-item interaction, run approved intent through a
documented workflow, generate valid artifacts, and know whether the work is
admissible to the next gate.

## 2. Parent Versus Domain Boundary

`openxFactory` owns the generic grammar of factories:

- the three-Hermes-layer contract: customer, client, domain
- the customer-item interaction model
- Hermes monitoring and self-initiation rules
- domain-specific business boundary rules
- neutral workflow, gate, approval, traceability, and handoff vocabulary
- base manifest and schema conventions
- required folder surface for generated domain factories
- validation rules and readiness levels
- compatibility rules for domain factories that consume `openxFactory`

Domain factories own the domain nouns and domain behavior:

- layer aliases, such as Patient Hermes, Clinic Hermes, or Medical Domain Hermes
- customer kinds, client kinds, focal item kinds, journey states, outcomes, and interventions
- domain Hermes policies, review standards, escalation rules, and memory boundaries
- client and customer Hermes templates
- domain workflows, checks, examples, and tenant/profile examples
- domain execution overlay, expert routing, validation checks, and output templates

Domain factories must not fork or redefine neutral `openxFactory` contracts.
They specialize them through overlays, profiles, models, workflows, policies,
schemas, examples, and execution configuration.

## 3. Generation Minimum

A new domain factory generator should require only these inputs:

```yaml
domain_id: medx
product_name: MedxFactory
display_name: Medx Factory
category: medical

domain_layer_name: Medical Domain Hermes
client_layer_name: Clinic Hermes
customer_layer_name: Patient Hermes

client_kinds:
  - clinic
  - hospital

customer_kinds:
  - patient

focal_item_kinds:
  - disease
  - treatment
  - care_plan

journey_states:
  - intake
  - diagnosis
  - treatment_planning
  - active_treatment
  - monitoring

outcome_measures:
  - diagnostic_confidence
  - adherence
  - readmission_risk

intervention_kinds:
  - follow_up
  - care_gap_review
  - clinician_review_packet

starter_workflows:
  - intake
  - review
  - follow_up
```

The generator should create a domain repo that is coherent but intentionally
thin. Domain teams fill in policy, workflow details, examples, and validation
after generation.

## 4. Generated Directory Surface

Every generated domain factory should start with this shape:

```text
<Domain>Factory/
  README.md
  stack.yaml

  docs/
    boundary.md
    customer-item-model.md
    hermes-self-initiation.md
    implementation-guide.md

  hermes/
    domain/
      overlay.yaml
      memory-boundaries.yaml
      escalation-rules.yaml

    client/
      template.yaml
      memory-boundaries.yaml
      policy-overrides.yaml
      integration-boundaries.yaml

    customer/
      template.yaml
      memory-boundaries.yaml
      consent-model.yaml

  models/
    customer-kinds.yaml
    client-kinds.yaml
    focal-items.yaml
    journey-states.yaml
    outcomes.yaml
    interventions.yaml

  workflows/
    README.md

  profiles/
    <profile>.yaml

  tenants/
    README.md
    examples/

  omnigent/
    domain-overlay.yaml
    expert-routing/
    validation-checks/
    output-templates/

  examples/
  scripts/
```

Domain repos may add domain-specific aliases when helpful, such as
`hermes/patient/` or `hermes/clinic/`, but the logical three-layer mapping must
remain explicit in `stack.yaml` and `docs/boundary.md`.

## 5. Required `stack.yaml`

`stack.yaml` must declare:

- `schema_version`
- `kind: xfactory_domain_stack`
- domain ID, product name, display name, and category
- consumed `openxFactory` repo and version, tag, or commit
- domain, client, and customer Hermes layer names
- paths to domain, client, and customer Hermes overlays
- domain execution overlay path
- client kinds and customer kinds
- focal item kinds, journey states, outcome measures, and intervention kinds
- tenant isolation defaults
- rule that tenant overrides cannot weaken base domain gates unless governance explicitly allows it

## 6. Core Docs

The root `README.md` must explain:

- domain purpose
- layer mapping
- how the domain consumes `openxFactory`
- quick start for generating or configuring a tenant
- links to canonical docs, workflows, models, examples, validation commands, and contributor guidance

`docs/boundary.md` must state:

- what `openxFactory` owns
- what the domain factory owns
- what domain Hermes owns
- what client Hermes owns
- what customer Hermes owns
- what the execution overlay owns
- what the final enforcement or handoff system owns
- which business-looking concerns are inside the domain boundary
- which general business concerns must route to another domain stack
- non-goals

`docs/customer-item-model.md` must define:

- customer kinds
- client kinds
- focal item kinds
- customer-item relationship semantics
- interaction event types
- journey states
- outcome measures
- prediction types
- intervention types
- learning and memory promotion rules

`docs/hermes-self-initiation.md` must define:

- what each Hermes layer monitors
- which events each layer may self-initiate from
- which actions each layer may take under standing approval
- which actions require client, domain, or human review
- core customer Hermes team roles
- rules for dynamically adding and retiring customer Hermes agents
- client Hermes domain-specific monitoring scope
- out-of-domain routing rules for general business concerns

`docs/implementation-guide.md` must explain:

- how to create a tenant
- how to create or import a customer record
- how to create a focal item
- how to run a starter workflow
- how to validate artifacts
- how to know whether a gate is pass, fail, pending, or not applicable

## 7. Customer-Item Model

Every domain factory must specialize the generic customer-item model.

Required model files:

- `models/customer-kinds.yaml`
- `models/client-kinds.yaml`
- `models/focal-items.yaml`
- `models/journey-states.yaml`
- `models/outcomes.yaml`
- `models/interventions.yaml`

Required record families:

- `customer_profile`
- `client_profile`
- `focal_item`
- `customer_item_relationship`
- `interaction_event`
- `journey_state_snapshot`
- `prediction`
- `intervention_plan`
- `outcome_observation`

Each record family must define:

- `schema_version`
- `kind`
- stable `id`
- owner layer
- required fields
- optional fields
- reference fields
- audit timestamp semantics
- examples

## 8. Hermes Overlays

The three Hermes layers are mandatory even when one physical Hermes runtime
hosts more than one layer.

Domain Hermes must declare:

- domain identity
- domain policy
- domain-specific law, standard, or capability rule ownership
- focal item type ownership
- journey state ownership
- outcome measure ownership
- prediction standards
- intervention standards
- approval scope kinds
- authority boundaries
- self-initiation triggers
- escalation routing
- review standards
- domain memory boundaries

Client Hermes must declare:

- supported client kinds
- required client fields
- tenant isolation rules
- client policy override rules
- integration boundary rules
- domain-specific business monitoring scope
- general business exclusions
- customer roster and relationship rules
- staff, credential, privilege, or capability assignment rules where domain-relevant
- client-side approval and escalation rules
- self-initiation triggers
- client memory boundaries

Customer Hermes must declare:

- supported customer kinds
- required customer fields
- consent, authorization, and data-sharing rules
- customer-item relationship rules
- interaction history rules
- journey state snapshot rules
- customer prediction and outcome observation rules
- core customer team roles
- dynamic customer agent assignment rules
- self-initiation triggers
- customer memory boundaries

## 9. Workflow Contracts

`workflows/README.md` must index all domain workflows.

Each workflow must define:

- purpose
- required inputs
- customer, client, focal item, and approved intent references
- states
- transitions
- gates
- required outputs
- blocking conditions
- traceability requirements
- approval requirements
- handoff or archive behavior

The workflow set should cover these generic phases:

- intake
- modeling
- planning
- execution
- validation
- review
- admission
- readiness or handoff
- archive or follow-up

Domain names may differ, but the mapping back to these generic phases must be
documented.

## 10. Artifact Schemas

`schemas/` is required when the domain emits structured artifacts beyond the
base `openxFactory` records.

Every persisted artifact must have:

- `schema_version`
- `kind`
- stable `id`
- creation time or equivalent audit timestamp
- explicit required fields
- explicit optional fields
- explicit enum values
- owner layer
- source references
- traceability references

Check artifacts must define pass, fail, pending, and not-applicable semantics.
Schema versioning rules must be documented. Examples must exist for every
required artifact family.

## 11. Traceability

Executable artifacts must preserve:

- approved intent reference
- customer reference
- client reference
- focal item reference
- customer-item relationship reference when applicable
- workflow state reference
- prediction, intervention, and outcome references when applicable
- validation evidence
- review evidence
- admission evidence
- readiness or handoff state

The trace chain must be auditable end to end from approved intent to final
handoff or observed outcome.

## 12. Decomposition Standard

Domain work must be decomposed into bounded slices.

Each slice must be:

- reviewable
- testable or otherwise verifiable
- owned by a declared agent or role
- traceable to approved intent
- traceable to customer, client, focal item, and outcome objective when applicable
- assigned a risk level
- assigned an estimated size or complexity
- linked to acceptance criteria

Dependencies must be represented as a DAG or equivalent ordering model. Cycles
are disallowed or explicitly blocked. Bug, issue, exception, or repair work
must map back to a feature, case, task, customer-item relationship, or repair
slice.

## 13. Profiles And Tenants

At least one deployment profile must exist.

Each profile must declare:

- enabled workflows
- enabled client kinds
- enabled customer kinds
- allowed focal item kinds
- required checks or validation gates
- agent or worker classes
- artifact storage locations
- admission policy
- readiness or final handoff policy

Tenant docs must define required tenant fields. Tenant records must pin the
consumed `openxFactory` version, tag, or commit. Tenant overrides must be
explicit and must not weaken base domain gates unless governance explicitly
allows it.

## 14. Execution Overlay

The execution overlay must declare:

- domain orchestrator profile
- agent or worker roster
- worker responsibilities
- worker inputs
- worker outputs
- worker permissions
- worker stop conditions
- ambiguity routing rules
- prediction, simulation, recommendation, or generation boundaries
- escalation hooks back to Hermes

The execution overlay must prohibit production secrets and long-lived
credentials unless access is delegated through safe references.

## 15. Checks And Gates

Required checks must be defined by change type, work type, risk class, or
workflow phase.

Checks must have:

- standardized names
- pass/fail/pending/not-applicable semantics
- rationale requirements for `not_applicable`
- owner layer
- required evidence
- traceability references

Admission requires all required checks to pass or be explicitly marked
not-applicable with rationale. Admission requires review evidence and
traceability evidence. Readiness requires downstream system state, such as CI,
human review, board review, clinical review, campaign approval, financial
review, or domain equivalent.

Final enforcement remains with the enforcement system named by the domain.

## 16. Examples

Every domain factory must include:

- golden-path example
- blocked-path example
- repair, bugfix, or exception example
- tenant example
- customer-item interaction example

The golden path must start from approved intent and include:

- customer, client, and focal item records
- customer-item relationship
- journey state snapshot
- decomposition or work slicing
- execution artifacts
- validation evidence
- review evidence
- admission evidence
- readiness, handoff, or outcome observation evidence

Examples must preserve the same approved scope reference across the trace chain.

## 17. Validation And CI

A local validation command must be documented.

Local validation must:

- check required files
- parse `stack.yaml`
- parse model files
- parse schemas
- check workflow shape
- check examples
- verify three-layer Hermes mapping
- verify customer-item model completeness
- run without production secrets

CI expectations must be documented. The repo must state which checks are
advisory versus required.

## 18. Implementation Readiness Review

Before a domain factory is marked implementation-ready, answer:

- [ ] Can a new tenant be created from the docs alone?
- [ ] Can a customer, client, and focal item be represented?
- [ ] Can a customer-item relationship be modeled?
- [ ] Can an approved intent be converted into a domain work item?
- [ ] Can the domain infer or record a journey state?
- [ ] Can the domain represent a prediction, intervention, and outcome observation?
- [ ] Can the domain split work into bounded slices?
- [ ] Can each slice produce required artifacts?
- [ ] Can required checks be selected and run or marked not applicable with rationale?
- [ ] Can a reviewer determine whether admission is allowed?
- [ ] Can a readiness packet, final handoff record, or outcome observation be produced?
- [ ] Can an auditor trace final output back to approved scope?
- [ ] Can the domain explain what it does not own?

## 19. Completion Levels

Use these levels when auditing a domain factory:

| Level | Meaning |
| --- | --- |
| `L0 concept` | Domain purpose exists, but implementation contracts are missing. |
| `L1 generated` | The generated skeleton, stack manifest, three Hermes layers, and model files exist. |
| `L2 specialized` | Domain nouns, focal item types, journey states, outcomes, interventions, workflows, and overlays are filled in. |
| `L3 implementable` | Required schemas, workflows, profiles, overlays, examples, and validation exist. |
| `L4 validated` | Local validation and example checks run successfully. |
| `L5 tenant-ready` | A tenant can be configured with pinned `openxFactory` contracts and domain checks. |
| `L6 operational` | The domain has run real work through admission, readiness or handoff, and outcome observation. |

A new domain factory should not be treated as tenant-ready before `L5`.
